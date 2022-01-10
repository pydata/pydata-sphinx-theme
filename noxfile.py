import nox
from pathlib import Path

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
    force_reinstall = "reinstall" in session.posargs
    should_install = not sphinx_is_installed or force_reinstall
    if should_install:
        session.log("Installing fresh environment...")
    else:
        session.log("Skipping environment install...")
    return should_install


@nox.session
def compile(session):
    if _should_install(session):
        session.install(".")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "compile")


@nox.session
def docs(session):
    if _should_install(session):
        session.install(".[doc]")
    session.run("sphinx-build", "-b=html", "docs/", "docs/_build/html")


@nox.session(name="docs-live")
def docs_live(session):
    if _should_install(session):
        session.install(".[doc]")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "serve", "docs", "--open-browser")


@nox.session(name="test")
def test(session):
    if _should_install(session):
        session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)
