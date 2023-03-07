"""Automatically build our documentation or run tests.

Environments are re-used by default.

Re-install the environment from scratch:

    nox -s docs -- -r
"""
import nox
from pathlib import Path
from shlex import split

nox.options.reuse_existing_virtualenvs = True


def _should_install(session):
    """Decide if we should install an environment or if it already exists.

    This speeds up the local install considerably because building the wheel
    for this package takes some time.

    We assume that if `sphinx-build` is in the bin/ path, the environment is
    installed.
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


def _compile_translations(session):
    session.run(*split("pybabel compile -d src/pydata_sphinx_theme/locale -D sphinx"))


@nox.session(name="compile")
def compile(session):
    """Compile the theme's web assets with sphinx-theme-builder."""
    if _should_install(session):
        session.install("-e", ".")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "compile")


@nox.session(name="docs")
def docs(session):
    """Build the documentation and place in docs/_build/html."""
    if _should_install(session):
        session.install("-e", ".[doc]")
    session.run("sphinx-build", "-b=html", "docs/", "docs/_build/html", "-v")


@nox.session(name="docs-live")
def docs_live(session):
    """Build the docs with a live server that re-loads as you make changes."""
    _compile_translations(session)
    if _should_install(session):
        session.install("-e", ".[doc]")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "serve", "docs", "--open-browser")


@nox.session(name="test")
def test(session):
    """Run the test suite."""
    if _should_install(session):
        session.install("-e", ".[test]")
    _compile_translations(session)
    session.run("pytest", *session.posargs)


@nox.session(name="test-sphinx")
@nox.parametrize("sphinx", ["4", "5", "6"])
def test_sphinx(session, sphinx):
    """Run the test suite with a specific version of Sphinx."""
    if _should_install(session):
        session.install("-e", ".[test]")
    session.install(f"sphinx=={sphinx}")
    session.run("pytest", *session.posargs)


@nox.session()
def translate(session):
    """Translation commands. Available commands after `--` : extract, update, compile"""
    session.install("Babel")
    if "extract" in session.posargs:
        session.run(
            *split(
                "pybabel extract . -F babel.cfg -o src/pydata_sphinx_theme/locale/sphinx.pot -k '_ __ l_ lazy_gettext'"
            )
        )
    elif "update" in session.posargs:
        session.run(
            *split(
                "pybabel update -i src/pydata_sphinx_theme/locale/sphinx.pot -d src/pydata_sphinx_theme/locale -D sphinx"
            )
        )
    elif "compile" in session.posargs:
        _compile_translations(session)
    elif "init" in session.posargs:
        language = session.posargs[-1]
        session.run(
            *split(
                f"pybabel init -i src/pydata_sphinx_theme/locale/sphinx.pot -d src/pydata_sphinx_theme/locale -D sphinx -l {language}"
            )
        )
    else:
        print(
            "No translate command found. Use like: `nox -s translate -- COMMAND`."
            "\n\n Available commands: extract, update, compile, init"
        )


@nox.session(name="profile")
def profile(session):
    """Generate a profile chart with py-spy. The chart will be placed at profile.svg."""
    import shutil as sh
    import tempfile
    from textwrap import dedent

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
            *f"py-spy record -o {output} -- sphinx-build {path_tmp} {path_tmp_out}".split()  # noqa
        )
        print(f"py-spy profiler output at this file: {output}")
