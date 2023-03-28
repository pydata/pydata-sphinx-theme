import pytest
import time
from pathlib import Path
from subprocess import Popen, PIPE
from http.client import HTTPConnection
from playwright.sync_api import Page
from urllib.parse import urljoin
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
path_docs_build = path_repo / "docs" / "_build_a11y_test" / "html"


@pytest.fixture(scope="module")
def url_base(base_url):
    """
    Return the the base URL provided via pytest-base-url plugin, or if the base
    URL is not provided, then try starting a local server and if successful,
    return the localhost URL to that server as the base URL.
    """

    # If the base_url was already specified on the command line, use it instead
    # of firing up a server on localhost
    if base_url:
        yield base_url
        return

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


@pytest.fixture(params=["light", "dark"])
def page(request, page: Page, url_base: str) -> Page:
    """
    Takes the pytest-playwright provided page and the provided url base, loads
    the page at the URL path marked on the currently running test, injects
    Axe-core into the page, sets the light/dark theme on the page, and then
    returns the page, ready for testing.
    """

    # Get the URL path from the metadata marked on the currently running test
    url_path = request.node.get_closest_marker("url_path").args[0]

    # Load the page at the provided path
    page.goto(urljoin(url_base, url_path))

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{request.param}'")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    return page


@pytest.mark.url_path("/examples/kitchen-sink/admonitions.html")
def test_axe_core_kitchen_sink_admonitions(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Admonitions page for accessibility
    violations.
    """

    # Run the Axe-core library against the Admonitions section of the page
    # (Don't run it against the whole page because in this test we're not trying
    # to find accessibility violations in the nav, sidebar, footer, or other
    # parts of the PyData Sphinx Theme documentation website.)
    results = page.evaluate("axe.run('#admonitions')")

    # Expect Axe-core to have found 0 accessibility violations
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/api.html")
def test_axe_core_kitchen_sink_api_documentation(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - API documentation page for
    accessibility violations.
    """
    results = page.evaluate("axe.run('#api-documentation')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/blocks.html")
def test_axe_core_kitchen_sink_blocks(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Blocks page for accessibility
    violations.
    """
    results = page.evaluate("axe.run('#blocks')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/generic.html")
def test_axe_core_kitchen_sink_generic_items(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Generic items page for accessibility
    violations.
    """
    results = page.evaluate("axe.run('#generic-items')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/images.html")
def test_axe_core_kitchen_sink_images_figures(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Images & Figures page for
    accessibility violations.
    """
    results = page.evaluate("axe.run('#images-figures')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/lists.html")
def test_axe_core_kitchen_sink_lists(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Lists page for accessibility
    violations.
    """
    results = page.evaluate("axe.run('#lists')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/structure.html")
def test_axe_core_kitchen_sink_structural_elements(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Structural Elements page for
    accessibility violations.
    """
    results = page.evaluate("axe.run('#structural-elements')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/structure.html")
def test_axe_core_kitchen_sink_structural_elements_2(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Structural Elements page (2nd
    section) for accessibility violations.
    """
    results = page.evaluate("axe.run('#structural-elements-2')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/tables.html")
def test_axe_core_kitchen_sink_tables(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Tables page for accessibility
    violations.
    """
    results = page.evaluate("axe.run('#tables')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


@pytest.mark.url_path("/examples/kitchen-sink/typography.html")
def test_axe_core_kitchen_sink_typography(page: Page):
    """
    Using Axe-core, scan the Kitchen Sink - Typography page for accessibility
    violations.
    """
    results = page.evaluate("axe.run('#typography')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)
