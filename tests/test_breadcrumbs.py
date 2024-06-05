"""Using Axe-core, scan the Kitchen Sink pages for accessibility violations."""

import time
from http.client import HTTPConnection
from pathlib import Path
from subprocess import PIPE, Popen
from urllib.parse import urljoin

import pytest

# Using importorskip to ensure these tests are only loaded if Playwright is installed.
playwright = pytest.importorskip("playwright")
from playwright.sync_api import Page, expect  # noqa: E402

# Important note: automated accessibility scans can only find a fraction of
# potential accessibility issues.
#
# This test file scans pages from the Kitchen Sink examples with a JavaScript
# library called Axe-core, which checks the page for accessibility violations,
# such as places on the page with poor color contrast that would be hard for
# people with low vision to see.
#
# Just because a page passes the scan with no accessibility violations does
# *not* mean that it will be generally usable by a broad range of disabled
# people. It just means that page is free of common testable accessibility
# pitfalls.

path_repo = Path(__file__).parent.parent
path_docs_build = path_repo / "docs" / "_build" / "html"


@pytest.fixture(scope="module")
def url_base():
    """Start local server on built docs and return the localhost URL as the base URL."""
    # Use a port that is not commonly used during development or else you will
    # force the developer to stop running their dev server in order to run the
    # tests.
    port = "8213"
    host = "localhost"
    url = f"http://{host}:{port}"

    # Try starting the server
    process = Popen(
        ["python", "-m", "http.server", port, "--directory", path_docs_build],
        stdout=PIPE,
    )

    # Try connecting to the server
    retries = 5
    while retries > 0:
        conn = HTTPConnection(host, port)
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield url
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1

    # If the code above never yields a URL, then we were never able to connect
    # to the server and retries == 0.
    if not retries:
        raise RuntimeError("Failed to start http server in 5 seconds")
    else:
        # Otherwise the server started and this fixture is done now and we clean
        # up by stopping the server.
        process.terminate()
        process.wait()


def test_breadcrumb_expansion(page: Page, url_base: str) -> None:
    """Foo."""
    page.set_viewport_size({"width": 1440, "height": 720})
    page.goto(urljoin(url_base, "community/topics/config.html"))
    expect(page.get_by_label("Breadcrumb").get_by_role("list")).to_contain_text(
        "Update Sphinx configuration during the build"
    )
    el = page.get_by_text("Update Sphinx configuration during the build").nth(1)
    assert el.evaluate("e => e.clientWidth === e.scrollWidth", el)
    expect(el).to_have_css("overflow-x", "hidden")
    expect(el).to_have_css("text-overflow", "ellipsis")
    page.set_viewport_size({"width": 20, "height": 720})

    # There is no good way to check if text-overflow has been applied other
    # than to directly compare the rendered clientWidth to the scrollWidth
    # required to display the text.
    assert el.evaluate("e => e.clientWidth < e.scrollWidth", el)


def test_breadcrumbs_everywhere(
    sphinx_build_factory, page: Page, url_base: str
) -> None:
    """Test building the base html template and config."""
    sphinx_build = sphinx_build_factory("breadcrumbs")

    # Basic build with defaults
    sphinx_build.build()
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")
    symlink_path = path_docs_build / "playwright_tests" / "breadcrumbs"
    symlink_path.parent.mkdir(exist_ok=True)
    try:
        symlink_path.symlink_to(sphinx_build.outdir, True)
        page.goto(
            urljoin(url_base, "playwright_tests/breadcrumbs/hansel/gretel/house.html")
        )
        # sidebar should overflow
        text = "In the oven with my sister, so hot right now. Soooo. Hotttt."
        el = page.locator("#main-content").get_by_text(text).last
        assert el.evaluate("e => e.clientWidth < e.scrollWidth", el)
        # footer containers will never trigger ellipsis overflow because... their min-width is content? TODO
        el = page.locator(".footer-items__center > .footer-item")
        assert el.evaluate("e => e.clientWidth === e.scrollWidth", el)
    finally:
        symlink_path.unlink()
        symlink_path.parent.rmdir()
