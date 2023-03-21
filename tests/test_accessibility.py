import pytest
import time
from pathlib import Path
from subprocess import Popen, PIPE
from http.client import HTTPConnection
from playwright.sync_api import Page
from utils import pretty_axe_results

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


@pytest.fixture(scope="module")
def url_base():
    path_repo = Path(__file__).parent.parent
    path_docs_static = path_repo / "docs" / "_build" / "html"
    port = "8213"
    host = "localhost"
    url = f"http://{host}:{port}"
    process = Popen(
        ["python", "-m", "http.server", port, "--directory", path_docs_static],
        stdout=PIPE,
    )
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

    if not retries:
        raise RuntimeError("Failed to start http server in 5 seconds")
    else:
        process.terminate()
        process.wait()


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_admonitions(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Admonitions page for accessibility violations."

    # Load the Admonitions page
    page.goto(f"{url_base}/examples/kitchen-sink/admonitions.html")

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against the Admonitions section of the page
    # (Don't run it against the whole page because we're not trying to find
    # accessibility violations in the nav, sidebar, footer, or other parts of
    # the PyData Sphinx Theme documentation website.)
    results = page.evaluate("axe.run('#admonitions')")

    # Expect Axe-core to have found 0 accessibility violations
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_api_documentation(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - API documentation page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/api.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#api-documentation')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_blocks(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Blocks page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/blocks.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#blocks')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_generic_items(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Generic items page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/generic.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#generic-items')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_images_figures(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Images & Figures page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/images.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#images-figures')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_lists(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Lists page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/lists.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#lists')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_structural_elements(
    page: Page, url_base: str, theme: str
):
    "Using Axe-core, scan the Kitchen Sink - Structural Elements page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/structure.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#structural-elements')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_structural_elements_2(
    page: Page, url_base: str, theme: str
):
    "Using Axe-core, scan the Kitchen Sink - Structural Elements page (2nd section) for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/structure.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#structural-elements-2')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_tables(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Tables page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/tables.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#tables')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)


# For comments explaining this test, go to the first test above.
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_typography(page: Page, url_base: str, theme: str):
    "Using Axe-core, scan the Kitchen Sink - Typography page for accessibility violations."
    page.goto(f"{url_base}/examples/kitchen-sink/typography.html")
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")
    results = page.evaluate("axe.run('#typography')")
    assert len(results["violations"]) == 0, pretty_axe_results(results)
