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
    force_reinstall = "reinstall" in session.posargs or "-r" in session.posargs
    should_install = not sphinx_is_installed or force_reinstall
    if should_install:
        session.log("Installing fresh environment...")
    else:
        session.log("Skipping environment install...")
    return should_install


@nox.session
def compile(session):
    if _should_install(session):
        session.install("-e", ".")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "compile")


@nox.session
def docs(session):
    if _should_install(session):
        session.install("-e", ".[doc]")
    session.run("sphinx-build", "-b=html", "docs/", "docs/_build/html")


@nox.session(name="docs-live")
def docs_live(session):
    if _should_install(session):
        session.install("-e", ".[doc]")
        session.install("sphinx-theme-builder[cli]")
    session.run("stb", "serve", "docs", "--open-browser")


@nox.session(name="test")
def test(session):
    if _should_install(session):
        session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)


@nox.session(name="profile")
def profile(session):
    """Generate a profile chart with py-spy.

    The chart will be placed at profile.svg and can be viewed in the browser.
    """
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
