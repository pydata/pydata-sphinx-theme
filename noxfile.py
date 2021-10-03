import nox
from pathlib import Path
from yaml import safe_load

nox.options.reuse_existing_virtualenvs = True

# Parse the environment files we'll need later
environment = safe_load(Path("environment.yml").read_text())
conda = environment.get("dependencies")
requirements = conda.pop(-1).get("pip")
build_command = ["-b", "html", "docs", "docs/_build/html"]


@nox.session(venv_backend="conda")
def build(session):
    _install_environment(session)
    session.run("yarn", "--frozen-lockfile")
    session.run("yarn", "build")


@nox.session(venv_backend="conda")
def docs(session):
    _install_environment(session)
    session.run("yarn", "--frozen-lockfile")
    session.cd("docs")
    session.run("make", "html")


@nox.session(name="docs-live", venv_backend="conda")
def docs_live(session):
    _install_environment(session)
    session.run("yarn", "--frozen-lockfile")
    session.run("yarn", "build:dev")


@nox.session(name="docs-live", venv_backend="conda")
def tests(session):
    _install_environment(session)
    session.run("pytest")


def _install_environment(session):
    """Install the JS and Python environment needed to develop the theme."""
    session.conda_install("--channel", "conda-forge", *conda)
    for pkg in requirements:
        # We split each line in case there's a space for `-r`
        session.install(*pkg.split())
    session.install("-e", ".")
