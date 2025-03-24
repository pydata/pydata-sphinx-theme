"""
Build minimal test sites with sphinx_build_factory and test them with Playwright.
When adding new tests to this file, remember to also add the corresponding test site
to `tests/sites/` or use an existing one.
"""

import re

from pathlib import Path
from typing import Callable
from urllib.parse import urljoin

import pytest


try:
    from pathlib import UnsupportedOperation  # added in Py 3.13
except ImportError:
    UnsupportedOperation = NotImplementedError

# Using importorskip to ensure these tests are only loaded if Playwright is installed.
playwright = pytest.importorskip("playwright")
from playwright.sync_api import Page, expect  # noqa: E402


repo_path = Path(__file__).parents[1]
test_sites_dir = repo_path / "docs" / "_build" / "html" / "playwright_tests"


# ------------------------- Helper functions -------------------------
def _is_overflowing(element):
    """Check if an element is being shortened via CSS due to text-overflow property.

    We can't check the rendered text because we can't easily get that; all we can get
    is the text as it exists in the DOM (prior to its truncation/elision). Thus we must
    directly compare the rendered clientWidth to the scrollWidth required to display the
    text.
    """
    return element.evaluate("e => e.clientWidth < e.scrollWidth", element)


def _build_test_site(site_name: str, sphinx_build_factory: Callable) -> None:
    """Helper function for building simple test sites (with no `confoverrides`)."""
    sphinx_build = sphinx_build_factory(site_name)
    sphinx_build.build()
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")
    return sphinx_build.outdir


def _check_test_site(site_name: str, site_path: Path, test_func: Callable):
    """Make the built test site available to Playwright, then run `test_func` on it."""
    # Need to ensure parent directories exist in CI
    test_sites_dir.mkdir(exist_ok=True, parents=True)
    symlink_path = test_sites_dir / site_name
    try:
        symlink_path.symlink_to(site_path, True)
    except UnsupportedOperation:
        pytest.xfail("filesystem doesn't support symlinking")
    else:
        test_func()
    finally:
        symlink_path.unlink()
        test_sites_dir.rmdir()


# ------------------------- Test functions: style -------------------------
def test_version_switcher_highlighting(
    sphinx_build_factory: Callable, page: Page, url_base: str
) -> None:
    """
    In sidebar and topbar - version switcher should apply highlight color to currently
    selected version.
    """
    site_name = "version_switcher"
    site_path = _build_test_site(site_name, sphinx_build_factory=sphinx_build_factory)

    def check_version_switcher_highlighting():
        page.goto(urljoin(url_base, f"playwright_tests/{site_name}/index.html"))
        # no need to include_hidden here ↓↓↓, we just need to get the active
        # version name
        button = page.get_by_role("button").filter(has_text="dev")
        active_version_name = button.get_attribute("data-active-version-name")

        # here we do include_hidden, since we are not adding this in the sidebar
        # we should only get one entry
        entries = page.get_by_role("option", include_hidden=True).filter(
            has_text=active_version_name
        )
        assert entries.count() == 1
        # make sure they're highlighted
        for entry in entries.all():
            light_mode = "rgb(10, 125, 145)"  # pst-color-primary
            # dark_mode = "rgb(63, 177, 197)"
            expect(entry).to_have_css("color", light_mode)

    _check_test_site(site_name, site_path, check_version_switcher_highlighting)


def test_colors(sphinx_build_factory: Callable, page: Page, url_base: str) -> None:
    """Test that things get colored the way we expect them to.

    Note: this is not comprehensive! Please feel free to add to this test by editing
    `../sites/colors/index.rst` and adding more `expect` statements below.
    """
    site_name = "colors"
    site_path = _build_test_site(site_name, sphinx_build_factory=sphinx_build_factory)

    def check_colors():
        page.goto(urljoin(url_base, f"playwright_tests/{site_name}/index.html"))
        primary_color = "rgb(10, 125, 145)"
        hover_color = "rgb(128, 69, 229)"
        spans = {
            "text link": primary_color,
            "cross reference link": primary_color,
            "inline code": "rgb(145, 37, 131)",
            "code link": "rgb(8, 93, 108)",  # teal-600, AKA #085d6c
        }
        for text, color in spans.items():
            el = page.get_by_text(text).first
            expect(el).to_have_css("color", color)
            if "link" in text:
                el.hover()
                expect(el).to_have_css("color", hover_color)

    _check_test_site(site_name, site_path, check_colors)


# ------------------------- Test functions: layout & components -----------------------


def test_breadcrumb_expansion(
    sphinx_build_factory: Callable, page: Page, url_base: str
) -> None:
    """Test breadcrumb text-overflow."""
    site_name = "breadcrumbs"
    site_path = _build_test_site(site_name, sphinx_build_factory=sphinx_build_factory)

    def check_breadcrumb_expansion():
        # wide viewport width → no truncation
        page.set_viewport_size({"width": 1440, "height": 720})
        page.goto(urljoin(url_base, "community/topics/config.html"))
        expect(page.get_by_label("Breadcrumb").get_by_role("list")).to_contain_text(
            "Update Sphinx configuration during the build"
        )
        el = page.get_by_text("Update Sphinx configuration during the build").nth(1)
        expect(el).to_have_css("overflow-x", "hidden")
        expect(el).to_have_css("text-overflow", "ellipsis")
        assert not _is_overflowing(el)
        # narrow viewport width → truncation
        page.set_viewport_size({"width": 150, "height": 720})
        assert _is_overflowing(el)

        _check_test_site(site_name, site_path, check_breadcrumb_expansion)


def test_breadcrumbs_everywhere(
    sphinx_build_factory: Callable, page: Page, url_base: str
) -> None:
    """Test breadcrumbs truncate properly when placed in various parts of the layout."""
    site_name = "breadcrumbs"
    site_path = _build_test_site(site_name, sphinx_build_factory=sphinx_build_factory)

    def check_breadcrumb_truncation():
        page.goto(
            urljoin(url_base, f"playwright_tests/{site_name}/hansel/gretel/house.html")
        )
        # sidebar should overflow
        text = "In the oven with my sister, so hot right now. Soooo. Hotttt."
        el = page.locator("#main-content").get_by_text(text).last
        assert _is_overflowing(el)
        # footer containers never trigger ellipsis overflow because min-width is content
        el = page.locator(".footer-items__center > .footer-item")
        assert not _is_overflowing(el)

    _check_test_site(site_name, site_path, check_breadcrumb_truncation)


def test_article_toc_syncing(
    sphinx_build_factory: Callable,
    page: Page,
    url_base: str,
) -> None:
    """Test that the secondary sidebar TOC highlights the correct entry."""
    site_name = "version_switcher"
    site_path = _build_test_site(site_name, sphinx_build_factory=sphinx_build_factory)
    assert site_path

    def check_toc_syncing():
        page.goto(
            urljoin(url_base, f"playwright_tests/{site_name}/fixture_blocks.html")
        )

        # define locators and other variables
        toc = page.locator("#pst-page-toc-nav")
        first_toc_link = toc.get_by_role("link", name="Block Quotes")
        some_toc_link_with_active = toc.locator("a.active")
        some_toc_link_with_aria_current = toc.locator("a[aria-current]")
        first_heading = page.locator(str(first_toc_link.get_attribute("href")))
        active_re = re.compile("active")

        # click the first TOC link, check that it gets highlighted and that the
        # associated heading is in the viewport
        first_toc_link.click()
        expect(first_toc_link).to_have_class(active_re)
        expect(first_toc_link).to_have_attribute("aria-current", "true")
        expect(first_heading).to_be_in_viewport()

        # verify that one and only one TOC link is active/highlighted/current
        expect(some_toc_link_with_active).to_have_count(1)
        expect(some_toc_link_with_aria_current).to_have_count(1)

        # after clicking a link, the pydata-sphinx-theme.js script sets a 1
        # second timeout before processing intersection events again
        page.wait_for_timeout(1001)

        # scroll to the bottom of the page, check that the first TOC entry
        # becomes un-highlighted

        # for some reason, we have to use page.evaluate rather than:
        #
        #     page.locator("p.copyright").scroll_into_view_if_needed()
        #
        # seems like the Playwright scroll function does not trigger the
        # IntersectionObserver callback
        page.evaluate("document.querySelector('p.copyright').scrollIntoViewIfNeeded()")
        expect(first_toc_link).not_to_have_class(active_re)
        expect(first_toc_link).not_to_have_attribute("aria-current", re.compile("."))

        # verify that one and only one TOC link is active/highlighted/current
        expect(some_toc_link_with_active).to_have_count(1)
        expect(some_toc_link_with_aria_current).to_have_count(1)

    _check_test_site(site_name, site_path, check_toc_syncing)
