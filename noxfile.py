"""Automatically build our documentation or run tests.

Environments are re-used by default.
Re-install the environment from scratch:

    nox -s docs -- -r
"""
import os
import shutil as sh
import tempfile
from pathlib import Path
from shlex import split
from textwrap import dedent

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = []

# folders useful for translation-related sessions
root_dir = Path(__file__).parent
locale_dir = root_dir / "src" / "pydata_sphinx_theme" / "locale"
babel_cfg = root_dir / "babel.cfg"
pot_file = locale_dir / "sphinx.pot"


def session(default: bool = True, **kwargs):
    """Wrap the `nox.session` decorator to add a `default` parameter.
    
    Setting `default=False` will exclude a session from running when `nox` is
    invoked without a `--session` argument.

    related to https://github.com/wntrblm/nox/issues/654
    """

    def _session(fn):
        if default:
            nox.options.sessions.append(kwargs.get("name", fn.__name__))
        return nox.session(**kwargs)(fn)

    return _session


def _should_install(session: nox.Session) -> bool:
    """Decide if we should install an environment or if it already exists.

    This speeds up the local install considerably because building the wheel
    for this package takes some time.

    We assume that if `sphinx-build` is in the bin/ path, the environment is
    installed.

    Parameter:
        session: the current nox session
    """
    if session.bin_paths is None:
        session.log("Running with `--no-venv` so don't install anything...")
        return False
    bin_files = list(Path(session.bin).glob("*"))
    sphinx_is_installed = any("sphinx-build" in ii.name for ii in bin_files)
    force_reinstall = "reinstall" in session.posargs or "-r" in session.posargs
    should_install = not sphinx_is_installed or force_reinstall
    if should_install:
        session.log("Installing fresh environment...")
    else:
        session.log("Skipping environment install...")
    return should_install


@session()
def lint(session: nox.Session) -> None:
    """Check the themes pre-commit before any other session."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@session()
def compile(session: nox.Session) -> None:
    """Compile the theme's web assets."""
    if _should_install(session):
        session.install("-e", ".")
        session.install("sphinx-theme-builder[cli]")
        session.install("Babel")

    session.run("stb", "compile")
    session.run("pybabel", "compile", "-d", str(locale_dir), "-D", "sphinx")


@session()
def docs(session: nox.Session) -> None:
    """Build the documentation and place in docs/_build/html. Use --no-compile to skip compilation."""
    if _should_install(session):
        session.install("-e", ".[doc]")
        session.install("sphinx-theme-builder[cli]")
    if "no-compile" not in session.posargs:
        session.run("stb", "compile")

    session.run("sphinx-build", "-b=html", "docs/", "docs/_build/html", "-v")


@session(name="docs-live", default=False)
def docs_live(session: nox.Session) -> None:
    """Build the docs with a live server that re-loads as you make changes."""
    session.run(*split("pybabel compile -d src/pydata_sphinx_theme/locale -D sphinx"))
    if _should_install(session):
        session.install("-e", ".[doc]")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "serve", "docs", "--open-browser")


@session()
def test(session: nox.Session) -> None:
    """Run the test suite."""
    if _should_install(session):
        session.install("-e", ".[test]")
    session.run(*split("pybabel compile -d src/pydata_sphinx_theme/locale -D sphinx"))
    session.run("pytest", "-m", "not a11y", *session.posargs)


@nox.session()
def a11y(session: nox.Session) -> None:
    """Run the accessibility test suite only."""
    if _should_install(session):
        session.install("-e", ".[test, a11y]")
        # Install the drivers that Playwright needs to control the browsers.
        if os.environ.get("CI") or os.environ.get("GITPOD_WORKSPACE_ID"):
            # CI and other cloud environments are potentially missing system
            # dependencies, so we tell Playwright to also install the system
            # dependencies
            session.run("playwright", "install", "--with-deps")
        else:
            # But most dev environments have the needed system dependencies
            session.run("playwright", "install")
    # Build the docs so we can run accessibility tests against them.
    session.run("nox", "-s", "docs")
    # The next step would be to open a server to the docs for Playwright, but
    # that is done in the test file, along with the accessibility checks.
    session.run("pytest", "-m", "a11y", *session.posargs)


@session(name="test-sphinx", default=False)
@nox.parametrize("sphinx", ["4", "5", "6"])
def test_sphinx(session: nox.Session, sphinx: int) -> None:
    """Run the test suite with a specific version of Sphinx."""
    if _should_install(session):
        session.install("-e", ".[test]")
    session.install(f"sphinx=={sphinx}")
    session.run("pytest", *session.posargs)


@session()
def translate(session: nox.Session) -> None:
    """Update translation related files."""
    session.install("Babel", "jinja2")

    # fmt: off
    session.run(  # generate/update the .pot file
        "pybabel", "extract", ".",
        "-F", str(babel_cfg.relative_to(root_dir)),
        "-o", str(pot_file.relative_to(root_dir)),
    )
    # fmt: on

    # update the message catalog (.po)
    languages = [f.stem for f in locale_dir.iterdir() if f.is_dir()]
    # fmt: off
    cmd = [
        "pybabel", "update",
        "-i", str(pot_file.relative_to(root_dir)),
        "-d", str(locale_dir.relative_to(root_dir)),
    ]
    # fmt: on
    for lan in languages:
        session.run(*cmd, "-l", lan)


@session(default=False)
def add_language(session: nox.Session) -> None:
    """Add a language to the catalog using posargs."""
    session.install("Babel")

    # get the language name from posargs
    if len(session.posargs) != 1:
        raise ValueError(
            f"There should be only one posargs: the ISO code of the languge, {len(session.posargs)} given."
        )
    lan = session.posargs[0]

    # init new language
    # fmt: off
    session.run(
        "pybabel", "init",
        "-i", str(pot_file),
        "-d", str(locale_dir),
        "-l", lan,
    )
    # fmt: on


@session()
def profile(session: nox.Session) -> None:
    """Generate a profile chart with py-spy. The chart will be placed at profile.svg."""
    if _should_install(session):
        session.install("-e", ".[test]")
    session.install("py-spy")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy over our base test site to the temporary folder
        path_base = Path("tests/sites/base/")
        path_tmp = Path(tmpdir) / path_base
        sh.copytree(path_base, path_tmp)

        # Add a bunch of extra files to increase the build length
        index = path_tmp / "index.rst"
        text = index.read_text()
        text += dedent(
            """
        .. toctree::
            :glob:

            many/*
        """
        )
        index.write_text(text)
        (path_tmp / "many").mkdir()

        # Create a bunch of empty pages to slow the build
        n_extra_pages = 50
        for ii in range(n_extra_pages):
            (path_tmp / "many" / f"{ii}.rst").write_text("Test\n====\n\nbody\n")

        if "-o" in session.posargs:
            output = session.posargs[session.posargs.index("-o") + 1]
        else:
            output = "profile.svg"

        # Specify our output directory
        path_tmp_out = path_tmp / "_build"

        # Profile the build
        print(f"Profiling build with {n_extra_pages} pages with py-spy...")
        session.run(
            *f"py-spy record -o {output} -- sphinx-build {path_tmp} {path_tmp_out}".split()
        )
        print(f"py-spy profiler output at this file: {output}")
