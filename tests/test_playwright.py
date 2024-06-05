"""Using Axe-core, scan the Kitchen Sink pages for accessibility violations."""

from pathlib import Path
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


def _is_overflowing(element):
    """Check if an element is being shortened via CSS due to text-overflow property.

    We can't check the rendered text because we can't easily get that; all we can get
    is the text as it exists in the DOM (prior to its truncation/elision). Thus we must
    directly compare the rendered clientWidth to the scrollWidth required to display the
    text.
    """
    return element.evaluate("e => e.clientWidth < e.scrollWidth", element)


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


def test_breadcrumb_expansion(page: Page, url_base: str) -> None:
    """Test breadcrumb text-overflow."""
    page.set_viewport_size({"width": 1440, "height": 720})
    page.goto(urljoin(url_base, "community/topics/config.html"))
    expect(page.get_by_label("Breadcrumb").get_by_role("list")).to_contain_text(
        "Update Sphinx configuration during the build"
    )
    el = page.get_by_text("Update Sphinx configuration during the build").nth(1)
    assert not _is_overflowing(el)
    expect(el).to_have_css("overflow-x", "hidden")
    expect(el).to_have_css("text-overflow", "ellipsis")
    page.set_viewport_size({"width": 20, "height": 720})
    assert _is_overflowing(el)


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
        assert _is_overflowing(el)
        # footer containers will never trigger ellipsis overflow because... their min-width is content? TODO
        el = page.locator(".footer-items__center > .footer-item")
        assert not _is_overflowing(el)
    finally:
        symlink_path.unlink()
        symlink_path.parent.rmdir()
