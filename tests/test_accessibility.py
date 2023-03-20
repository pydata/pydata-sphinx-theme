import pytest
from playwright.sync_api import Page
from utils import pretty_axe_results


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_axe_core_kitchen_sink_admonitions(page: Page, theme: str):
    "Using Axe-core, scan the Kitchen Sink Admonitions page for accessibility violations."

    # Load the Admonitions page
    page.goto("http://localhost:8000/examples/kitchen-sink/admonitions.html")

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against the Admonitions section of the page
    results = page.evaluate("axe.run('#admonitions')")

    # Expect Axe-core to have found 0 accessibility violations
    assert len(results["violations"]) == 0, pretty_axe_results(results)
