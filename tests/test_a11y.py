"""
Using Axe-core, scan the Kitchen Sink pages for accessibility violations.
Note that in contrast with the rest of our tests, the accessibility tests in this file
are run against a build of our PST documentation, not purposedly-built test sites.
"""

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
            # TODO: remove this exclusion once the following update to Axe is
            # released and we upgrade:
            # https://github.com/dequelabs/axe-core/pull/4469
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

    # On the PyData Library Styles page, wait for ipywidget to load and for our
    # JavaScript to apply tabindex="0" before running Axe checker (to avoid
    # false positives for scrollable-region-focusable).
    if url_pathname == "/examples/pydata.html":
        ipywidgets_pandas_table = page.locator("css=.jp-RenderedHTMLCommon").first
        expect(ipywidgets_pandas_table).to_have_attribute("tabindex", "0")

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against a section of the page (unless the
    # selector is empty, then run against the whole page)
    results = page.evaluate("axe.run()" if selector == "" else f"axe.run('{selector}')")

    # Check found violations against known violations that we do not plan to fix
    filtered_violations = filter_ignored_violations(results["violations"], url_pathname)

    # We expect notebook outputs on the PyData Library Styles page to have color
    # contrast failures.
    if url_pathname == "/examples/pydata.html":
        # All violations should be color contrast violations
        for violation in filtered_violations:
            assert (
                violation["id"] == "color-contrast"
            ), f"""Found {violation["id"]} violation (expected color-contrast):
                    {format_violations([violation])}"""

        # Now check that when we exclude notebook outputs, the page has no violations

        results_sans_nbout = page.evaluate(
            f"axe.run({{ include: '{selector}', exclude: '.nboutput > .output_area' }})"
        )
        violations_sans_nbout = filter_ignored_violations(
            results_sans_nbout["violations"], url_pathname
        )

        # No violations on page when excluding notebook outputs
        assert len(violations_sans_nbout) == 0, format_violations(violations_sans_nbout)

        # TODO: for color contrast issues with common notebook outputs
        # (ipywidget tabbed panels, Xarray, etc.), should we override
        # third-party CSS with our own CSS or/and work with NbSphinx, MyST-NB,
        # ipywidgets, and other third parties to use higher contrast colors in
        # their CSS?
        pytest.xfail("notebook outputs have color contrast violations")

    assert len(filtered_violations) == 0, format_violations(filtered_violations)


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

    # Narrow viewport, content overflows ...
    assert code_block.evaluate("el => el.scrollWidth > el.clientWidth") is True

    # ... and code block should be a tab stop.
    #
    # Note: expect() will wait until the expect condition is true (up to the
    # test timeout limit). This is important because the resize handler is
    # debounced.
    expect(code_block).to_have_attribute("tabindex", "0")


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
    # mutation observer
    ipywidget.wait_for(state="attached")

    # At the default viewport size (1280 x 720) the data table inside the
    # ipywidget has overflow...
    assert ipywidget.evaluate("el => el.scrollWidth > el.clientWidth") is True

    # ... and so our js code on the page should make it keyboard-focusable
    # (tabIndex=0).
    #
    # Note: expect() will wait until the expect condition is true (up to the
    # test timeout limit). This is important because the mutation callback that
    # sets tabIndex=0 is debounced.
    expect(ipywidget).to_have_attribute("tabindex", "0")


@pytest.mark.a11y
def test_search_as_you_type(page: Page, url_base: str) -> None:
    """Search-as-you-type feature should support keyboard navigation.

    When the search-as-you-type (inline search results) feature is enabled,
    pressing Tab after entering a search query should focus the first inline
    search result.
    """
    page.set_viewport_size({"width": 1440, "height": 720})
    page.goto(urljoin(url_base, "/examples/kitchen-sink/blocks.html"))
    # Click the search textbox.
    searchbox = page.locator("css=.navbar-header-items .search-button__default-text")
    searchbox.click()
    # Type a search query.
    query_input = page.locator("css=#pst-search-dialog input[type=search]")
    expect(query_input).to_be_visible()
    query_input.type("test")
    page.wait_for_timeout(301)  # Search execution is debounced for 300 ms.
    search_results = page.locator("css=#search-results")
    expect(search_results).to_be_visible()
    # Navigate with the keyboard.
    query_input.press("Tab")
    # Make sure that the first inline search result is focused.
    actual_focused_content = page.evaluate("document.activeElement.textContent")
    first_result_selector = "#search-results .search li:first-child a"
    expected_focused_content = page.evaluate(
        f"document.querySelector('{first_result_selector}').textContent"
    )
    assert actual_focused_content == expected_focused_content
