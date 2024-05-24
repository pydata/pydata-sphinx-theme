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


def filter_ignored_violations(violations, url_pathname):
    """Filter out ignored axe-core violations.

    In some tests, we wish to ignore certain accessibility violations that we
    won't ever fix or that we don't plan to fix soon.
    """
    # we allow empty table headers
    # https://dequeuniversity.com/rules/axe/4.8/empty-table-header?application=RuleDescription
    if url_pathname == "/examples/pydata.html":
        return [v for v in violations if v["id"] != "empty-table-header"]
    elif url_pathname in [
        "/examples/kitchen-sink/generic.html",
        "/user_guide/theme-elements.html",
    ]:
        filtered = []
        for violation in violations:
            # TODO: eventually fix this rule violation. See
            # https://github.com/pydata/pydata-sphinx-theme/issues/1479.
            if violation["id"] == "landmark-unique":
                # Ignore landmark-unique only for .sidebar targets. Don't ignore
                # it for other targets because then the test might fail to catch
                # a change that violates the rule in some other way.
                unexpected_nodes = []
                for node in violation["nodes"]:
                    # If some target is not .sidebar then we've found a rule
                    # violation we weren't expecting
                    if not all([".sidebar" in target for target in node["target"]]):
                        unexpected_nodes.append(node)
                if unexpected_nodes:
                    violation["nodes"] = unexpected_nodes
                    filtered.append(violation)
            else:
                filtered.append(violation)
        return filtered
    else:
        return violations


def format_violations(violations):
    """Return a pretty string representation of Axe-core violations."""
    result = f"""

        Found {len(violations)} accessibility violation(s):
        """

    for violation in violations:
        result += f"""

            - Rule violated:
              {violation["id"]} - {violation["help"]}
                - URL: {violation["helpUrl"]}
                - Impact: {violation["impact"]}
                - Tags: {" ".join(violation["tags"])}
                - Targets:"""

        for node in violation["nodes"]:
            for target in node["target"]:
                result += f"""
                    - {target}"""

        result += "\n\n"

    return result


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
        ("/examples/pydata.html", "#PyData-Library-Styles"),
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
        (
            "/user_guide/page-toc.html",
            "",  # select whole page
        ),
    ],
)
def test_axe_core(
    page: Page,
    url_base: str,
    theme: str,
    url_pathname: str,
    selector: str,
):
    """Should have no Axe-core violations at the provided theme and page section."""
    # Load the page at the provided path
    url_full = urljoin(url_base, url_pathname)
    page.goto(url_full)

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Wait for CSS transitions (Bootstrap's transitions are 300 ms)
    page.wait_for_timeout(301)

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against a section of the page (unless the
    # selector is empty, then run against the whole page)
    results = page.evaluate("axe.run()" if selector == "" else f"axe.run('{selector}')")

    # Check found violations against known violations that we do not plan to fix
    filtered_violations = filter_ignored_violations(results["violations"], url_pathname)
    assert len(filtered_violations) == 0, format_violations(filtered_violations)


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


@pytest.mark.a11y
def test_code_block_tab_stop(page: Page, url_base: str) -> None:
    """Code blocks that have scrollable content should be tab stops."""
    page.set_viewport_size({"width": 1440, "height": 720})
    page.goto(urljoin(url_base, "/examples/kitchen-sink/blocks.html"))

    code_block = page.locator(
        "css=#code-block pre", has_text="from typing import Iterator"
    )

    # Viewport is wide, so code block content fits, no overflow, no tab stop
    assert code_block.evaluate("el => el.scrollWidth > el.clientWidth") is False
    assert code_block.evaluate("el => el.tabIndex") != 0

    page.set_viewport_size({"width": 400, "height": 720})

    # Resize handler is debounced with 300 ms wait time
    page.wait_for_timeout(301)

    # Narrow viewport, content overflows and code block should be a tab stop
    assert code_block.evaluate("el => el.scrollWidth > el.clientWidth") is True
    assert code_block.evaluate("el => el.tabIndex") == 0


@pytest.mark.a11y
def test_notebook_output_tab_stop(page: Page, url_base: str) -> None:
    """Notebook outputs that have scrollable content should be tab stops."""
    page.goto(urljoin(url_base, "/examples/pydata.html"))

    # A "plain" notebook output
    nb_output = page.locator("css=#Pandas > .nboutput > .output_area")

    # At the default viewport size (1280 x 720) the Pandas data table has
    # overflow...
    assert nb_output.evaluate("el => el.scrollWidth > el.clientWidth") is True

    # ...and so our js code on the page should make it keyboard-focusable
    # (tabIndex = 0)
    assert nb_output.evaluate("el => el.tabIndex") == 0


@pytest.mark.a11y
def test_notebook_ipywidget_output_tab_stop(page: Page, url_base: str) -> None:
    """Notebook ipywidget outputs that have scrollable content should be tab stops."""
    page.goto(urljoin(url_base, "/examples/pydata.html"))

    # An ipywidget notebook output
    ipywidget = page.locator("css=.jp-RenderedHTMLCommon").first

    # As soon as the ipywidget is attached to the page it should trigger the
    # mutation observer, which has a 300 ms debounce
    ipywidget.wait_for(state="attached")
    page.wait_for_timeout(301)

    # At the default viewport size (1280 x 720) the data table inside the
    # ipywidget has overflow...
    assert ipywidget.evaluate("el => el.scrollWidth > el.clientWidth") is True

    # ...and so our js code on the page should make it keyboard-focusable
    # (tabIndex = 0)
    assert ipywidget.evaluate("el => el.tabIndex") == 0
