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
ROOT = Path(__file__).parent


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


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Check the themes pre-commit before any other session."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session()
def compile(session: nox.Session) -> None:
    """Compile the theme's web assets with sphinx-theme-builder."""
    if _should_install(session):
        session.install("-e", ".")
        session.install("sphinx-theme-builder[cli]")

    session.run("stb", "compile")


@nox.session()
def docs(session: nox.Session) -> None:
    """Build the documentation and place in docs/_build/html. Use --no-compile to skip compilation."""
    if _should_install(session):
        session.install("-e", ".[doc]")
        session.install("sphinx-theme-builder[cli]")
    if "no-compile" not in session.posargs:
        session.run("stb", "compile")
    session.run(
        "sphinx-build",
        "-b=html",
        "docs/",
        "docs/_build/html",
        "-v",
        "-w",
        "warnings.txt",
        # suppress Py3.11's new "can't debug frozen modules" warning
        env=dict(PYDEVD_DISABLE_FILE_VALIDATION="1"),
    )
    session.run("python", "tests/utils/check_warnings.py")


@nox.session(name="docs-live")
def docs_live(session: nox.Session) -> None:
    """Build the docs with a live server that re-loads as you make changes."""
    session.run(*split("pybabel compile -d src/pydata_sphinx_theme/locale -D sphinx"))
    if _should_install(session):
        session.install("-e", ".[doc]")
        # quick hack to get the patched version of stb - need to remove once a stb release is cut
        session.install(
            "sphinx-theme-builder[cli]@git+https://github.com/pradyunsg/sphinx-theme-builder#egg=d9f620b"
        )
    session.run(
        "stb",
        "serve",
        "docs",
        "--open-browser",
        r"--re-ignore=locale|api|_build|\.jupyterlite\.doit\.db",
        # suppress Py3.11's new "can't debug frozen modules" warning
        env=dict(PYDEVD_DISABLE_FILE_VALIDATION="1"),
    )


@nox.session()
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


@nox.session(name="test-sphinx")
@nox.parametrize("sphinx", ["4", "5", "6"])
def test_sphinx(session: nox.Session, sphinx: int) -> None:
    """Run the test suite with a specific version of Sphinx."""
    if _should_install(session):
        session.install("-e", ".[test]")
    session.install(f"sphinx=={sphinx}")
    session.run("pytest", *session.posargs)


@nox.session()
def translate(session: nox.Session) -> None:
    """Translation commands. Available commands after `--` : extract, update, compile, init."""
    # get the command from posargs, default to "update"
    pybabel_cmd, found = ("update", False)
    for c in ["extract", "update", "compile", "init"]:
        if c in session.posargs:
            pybabel_cmd, found = (c, True)

    if found is False:
        print(
            "No translate command found. Use like: `nox -s translate -- COMMAND`."
            "\ndefaulting to `update`"
            "\nAvailable commands: extract, update, compile, init"
        )

    # get the language from parameters default to en.
    # it can be deceiving but we don't have a table of accepted languages yet
    lan = "en" if len(session.posargs) < 2 else session.posargs[-1]

    # get the path to the differnet local related pieces
    locale_dir = str(ROOT / "src" / "pydata_sphinx_theme" / "locale")
    babel_cfg = str(ROOT / "babel.cfg")
    pot_file = str(locale_dir / "sphinx.pot")

    # install deps
    session.install("Babel")

    # build the command from the parameters
    cmd = ["pybabel", pybabel_cmd]

    if pybabel_cmd == "extract":
        cmd += [ROOT, "-F", babel_cfg, "-o", pot_file, "-k", "_ __ l_ lazy_gettext"]

    elif pybabel_cmd == "update":
        cmd += ["-i", pot_file, "-d", locale_dir, "-D", "sphinx"]

    elif pybabel_cmd == "compile":
        cmd += ["-d", locale_dir, "-D", "sphinx"]

    elif pybabel_cmd == "init":
        cmd += ["-i", pot_file, "-d", locale_dir, "-D", "sphinx", "-l", lan]

    session.run(cmd)


@nox.session()
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
