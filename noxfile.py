import nox

nox.options.reuse_existing_virtualenvs = True

build_command = ["-b", "html", "docs", "docs/_build/html"]


@nox.session(venv_backend="conda")
def build(session):
    session.conda_install("--channel=conda-forge", "yarn=1.22.15")
    session.run("yarn")
    session.run("yarn", "build")


@nox.session(venv_backend="conda")
def docs(session):
    session.install("-r", "docs/requirements.txt")
    session.install("-e", ".")
    session.run("sphinx-build", "docs", "docs/_build/html")


@nox.session(name="docs-live", venv_backend="conda")
def docs_live(session):
    session.conda_install("--channel=conda-forge", "yarn=1.22.15")
    session.run("yarn")

    session.install("-r", "docs/requirements.txt")
    session.install("-e", ".")

    session.run("yarn", "build:dev")
