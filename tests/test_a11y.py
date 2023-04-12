"""Using Axe-core, scan the Kitchen Sink pages for accessibility violations."""

import time
from http.client import HTTPConnection
from pathlib import Path
from subprocess import PIPE, Popen
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page

from .utils.pretty_axe_results import pretty_axe_results

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
    """Start local server and return the localhost URL as the base URL."""
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


@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(
    "url_page,selector",
    [
        ("admonitions.html", "#admonitions"),
        ("api.html", "#api-documentation"),
        ("blocks.html", "#blocks"),
        ("generic.html", "#generic-items"),
        ("images.html", "#images-figures"),
        ("lists.html", "#lists"),
        ("structure.html", "#structural-elements"),
        ("structure.html", "#structural-elements-2"),
        ("tables.html", "#tables"),
        ("typography.html", "#typography"),
    ],
)
def test_axe_core_kitchen_sink(
    page: Page, theme: str, url_base: str, url_page: str, selector: str
):
    """Should have no Axe-core violations at the provided theme and page section."""
    # Load the page at the provided path
    url_base_kitchen_sink = urljoin(url_base, "/examples/kitchen-sink/")
    url_full = urljoin(url_base_kitchen_sink, url_page)
    page.goto(url_full)

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against a section of the page. (Don't run it
    # against the whole page because in this test we're not trying to find
    # accessibility violations in the nav, sidebar, footer, or other parts of
    # the PyData Sphinx Theme documentation website.)
    results = page.evaluate(f"axe.run('{selector}')")

    # Expect Axe-core to have found 0 accessibility violations
    assert len(results["violations"]) == 0, pretty_axe_results(results)
