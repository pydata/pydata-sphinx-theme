import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def docs(session):
    session.install(".[doc]")
    session.run("sphinx-build", "-b=html", "docs/", "docs/_build/html")


@nox.session(name="docs-live")
def docs_live(session):
    session.install("sphinx-theme-builder[cli]")
    session.run("stb", "serve", "docs", "--open-browser")


@nox.session(name="test")
def test(session):
    session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)
