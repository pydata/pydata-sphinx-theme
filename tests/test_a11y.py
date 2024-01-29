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


def fingerprint_violations(accessibility_page_scan_violations):
    """Create a fingerprint of the Axe violations array.

    https://playwright.dev/docs/accessibility-testing#using-snapshots-to-allow-specific-known-issues
    """
    return [
        {
            "id": violation["id"],
            "help": violation["help"],
            "helpUrl": violation["helpUrl"],
            "targets": [node["target"] for node in violation["nodes"]],
        }
        for violation in accessibility_page_scan_violations
    ]


@pytest.mark.a11y
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(
    "url_pathname,selector",
    [
        (
            "/examples/kitchen-sink/admonitions.html",
            "#admonitions",
        ),
        (
            "/examples/kitchen-sink/api.html",
            "#api-documentation",
        ),
        ("/examples/kitchen-sink/blocks.html", "#blocks"),
        (
            "/examples/kitchen-sink/generic.html",
            "#generic-items",
        ),
        (
            "/examples/kitchen-sink/images.html",
            "#images-figures",
        ),
        ("/examples/kitchen-sink/lists.html", "#lists"),
        (
            "/examples/kitchen-sink/structure.html",
            "#structural-elements",
        ),
        (
            "/examples/kitchen-sink/structure.html",
            "#structural-elements-2",
        ),
        ("/examples/kitchen-sink/tables.html", "#tables"),
        (
            "/examples/kitchen-sink/typography.html",
            "#typography",
        ),
        ("/examples/pydata.html", "#pydata-library-styles"),
        (
            "/user_guide/theme-elements.html",
            "#theme-specific-elements",
        ),
        (
            "/user_guide/web-components.html",
            "#sphinx-design-components",
        ),
        (
            "/user_guide/extending.html",
            "#extending-the-theme",
        ),
        (
            "/user_guide/styling.html",
            "#theme-variables-and-css",
        ),
        # Using one of the simplest pages on the site, select the whole page for
        # testing in order to effectively test repeated website elements like
        # nav, sidebars, breadcrumbs, footer
        ("/user_guide/page-toc.html", ""),
    ],
)
def test_axe_core(
    data_regression,
    theme: str,
    url_base: str,
    url_pathname: str,
    selector: str,
    page: Page,
):
    """Should have no Axe-core violations at the provided theme and page section."""
    # Load the page at the provided path
    url_full = urljoin(url_base, url_pathname)
    page.goto(url_full)

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against a section of the page. (Don't run it
    # against the whole page because in this test we're not trying to find
    # accessibility violations in the nav, sidebar, footer, or other parts of
    # the PyData Sphinx Theme documentation website.)
    results = page.evaluate("axe.run()" if selector == "" else f"axe.run('{selector}')")

    # Check found violations against known violations that we do not plan to fix
    data_regression.check(fingerprint_violations(results["violations"]))


def test_version_switcher_highlighting(page: Page, url_base: str) -> None:
    """This isn't an a11y test, but needs a served site for Javascript to inject the version menu."""
    page.goto(url=url_base)
    # no need to include_hidden here ↓↓↓, we just need to get the active version name
    button = page.get_by_role("button").filter(has_text="dev")
    active_version_name = button.get_attribute("data-active-version-name")
    # here we do include_hidden, so sidebar & topbar menus should each have a matching entry:
    entries = page.get_by_role("option", include_hidden=True).filter(
        has_text=active_version_name
    )
    assert entries.count() == 2
    # make sure they're highlighted
    for entry in entries.all():
        light_mode = "rgb(10, 125, 145)"  # pst-color-primary
        # dark_mode = "rgb(63, 177, 197)"
        expect(entry).to_have_css("color", light_mode)
