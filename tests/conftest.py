"""Configuration of the pytest session."""

import re

from collections.abc import Callable, Iterator
from contextlib import ExitStack, contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from os import environ
from pathlib import Path
from shutil import copytree
from threading import Thread
from typing import Self

import pytest

from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


pytest_plugins = "sphinx.testing.fixtures"

tests_path = Path(__file__).parent
repo_path = tests_path.parent
docs_build_path = repo_path / "docs" / "_build" / "html"

# -- Utils method ------------------------------------------------------------


def escape_ansi(string: str) -> str:
    """Helper function to remove ansi coloring from sphinx warnings."""
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    return ansi_escape.sub("", string)


# -- global fixture to build sphinx tmp docs ---------------------------------


class SphinxBuild:
    """Helper class to build a test documentation."""

    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self, no_warning: bool = True) -> Self:
        """Build the application."""
        self.app.build()
        if no_warning is True:
            assert self.warnings == "", self.status
        return self

    @property
    def status(self) -> str:
        """Returns the status of the current build."""
        return self.app._status.getvalue()

    @property
    def warnings(self) -> str:
        """Returns the warnings raised by the current build."""
        return self.app._warning.getvalue()

    @property
    def outdir(self) -> Path:
        """Returns the output directory of the current build."""
        return Path(self.app.outdir)

    def html_tree(self, *path) -> str:
        """Returns the html tree of the current build."""
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            raise ValueError(f"{path_page} does not exist")
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture()
def sphinx_build_factory(make_app: Callable, tmp_path: Path, request) -> Callable:
    """Return a factory builder pointing to the tmp directory."""

    def _func(src_folder: str, **kwargs) -> SphinxBuild:
        """Create the Sphinxbuild from the source folder."""
        no_temp = environ.get("PST_TEST_HTML_DIR")
        nonlocal tmp_path
        if no_temp is not None:
            tmp_path = Path(no_temp) / request.node.name / str(src_folder)
        srcdir = tmp_path / src_folder
        copytree(tests_path / "sites" / src_folder, tmp_path / src_folder)
        app = make_app(srcdir=srcdir, **kwargs)
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


class _HTTPServer(ThreadingHTTPServer):
    # Browsers fire off dozens of parallel requests when loading a page, and
    # SimpleHTTPRequestHandler speaks HTTP/1.0 so each one is a new connection.
    # With the default listen backlog of 5, macOS resets and Windows refuses
    # the overflowing connections (Linux makes the client retry instead), so
    # assets randomly fail to load and tests flake.
    request_queue_size = 128


@contextmanager
def _serve(directory: Path) -> Iterator[str]:
    """Serve a directory over HTTP and return the base URL."""
    # 127.0.0.1 rather than "" or "localhost": binding all interfaces makes
    # http.server reverse-resolve the hostname, which can take seconds.
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    server = _HTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture
def serve_directory() -> Iterator[Callable[[Path], str]]:
    """Return a function that serves a directory over HTTP and returns its URL."""
    with ExitStack() as stack:
        yield lambda directory: stack.enter_context(_serve(directory))


@pytest.fixture(scope="module")
def url_base() -> Iterator[str]:
    """Start local server on built docs and return its URL as the base URL."""
    with _serve(docs_build_path) as url:
        yield url
