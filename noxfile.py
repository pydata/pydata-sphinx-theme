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
    session.run("yarn", "build")


@nox.session(venv_backend="conda")
def docs(session):
    _install_environment(session)
    session.cd("docs")
    session.run("make", "html")


@nox.session(name="docs-live", venv_backend="conda")
def docs_live(session):
    _install_environment(session)
    session.run("yarn", "build:dev")


@nox.session(name="test", venv_backend="conda")
def tests(session):
    _install_environment(session, yarn=False)
    session.run("pytest")


def _install_environment(session, yarn=True):
    """Install the JS and Python environment needed to develop the theme."""
    # Assume that if sphinx is already installed, we don't need to re-install
    try:
        bin = Path(session.bin)
    except ValueError:
        # we are in a pass-through environment, just return an not install anything
        return

    if list(bin.rglob("sphinx-build")) and "reinstall" not in session.posargs:
        return

    # Install JS and Python dependencies
    session.conda_install("--channel", "conda-forge", *conda)
    for pkg in requirements:
        # We split each line in case there's a space for `-r`
        session.install(*pkg.split())
    session.install("-e", ".")

    # Build JS packages
    if yarn:
        session.run("yarn", "--frozen-lockfile")
