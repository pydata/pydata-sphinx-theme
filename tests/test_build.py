import os
from pathlib import Path
from shutil import copytree

from bs4 import BeautifulSoup

from sphinx.testing.util import SphinxTestApp
from sphinx.testing.path import path as sphinx_path

import pytest


path_tests = Path(__file__).parent


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self):
        self.app.build()
        assert self.warnings == "", self.status
        return self

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    @property
    def outdir(self):
        return Path(self.app.outdir)

    def html_tree(self, *path):
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            raise ValueError(f"{path_page} does not exist")
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture()
def sphinx_build_factory(make_app, tmp_path):
    def _func(src_folder, **kwargs):
        copytree(path_tests / "sites" / src_folder, tmp_path / src_folder)
        app = make_app(
            srcdir=sphinx_path(os.path.abspath((tmp_path / src_folder))), **kwargs
        )
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


def test_build_html(sphinx_build_factory, file_regression):
    """Test building the base html template and config."""
    sphinx_build = sphinx_build_factory("base")  # type: SphinxBuild

    # Basic build with defaults
    sphinx_build.build()
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    index_html = sphinx_build.html_tree("index.html")
    subpage_html = sphinx_build.html_tree("section1/index.html")

    # Navbar structure
    navbar = index_html.select("div#navbar-menu")[0]
    file_regression.check(navbar.prettify(), basename="navbar_ix", extension=".html")

    # Sidebar structure
    sidebar = index_html.select(".bd-sidebar")[0]
    file_regression.check(sidebar.prettify(), basename="sidebar_ix", extension=".html")

    # Sidebar subpage
    sidebar = subpage_html.select(".bd-sidebar")[0]
    file_regression.check(
        sidebar.prettify(), basename="sidebar_subpage", extension=".html"
    )


def test_toc_visibility(sphinx_build_factory):
    # Test that setting TOC level visibility works as expected
    confoverrides = {
        "html_theme_options.show_toc_level": 2,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")

    # The 3rd level headers should be visible, but not the fourth-level
    assert "visible" in index_html.select(".toc-h2 ul")[0].attrs["class"]
    assert "visible" not in index_html.select(".toc-h3 ul")[0].attrs["class"]


def test_logo(sphinx_build_factory):
    """Test that the logo is shown by default, project title if no logo."""
    sphinx_build = sphinx_build_factory("base").build()

    # By default logo is shown
    index_html = sphinx_build.html_tree("index.html")
    assert index_html.select(".navbar-brand img")
    assert not index_html.select(".navbar-brand")[0].text.strip()


def test_logo_name(sphinx_build_factory):
    """Test that the logo is shown by default, project title if no logo."""
    confoverrides = {"html_logo": ""}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    # if no logo is specified, use project title instead
    index_html = sphinx_build.html_tree("index.html")
    assert "PyData Tests" in index_html.select(".navbar-brand")[0].text.strip()


def test_sidebar_default(sphinx_build_factory):
    """The sidebar is shrunk when no sidebars specified in html_sidebars."""
    sphinx_build = sphinx_build_factory("base").build()

    index_html = sphinx_build.html_tree("page1.html")
    assert "col-md-3" in index_html.select(".bd-sidebar")[0].attrs["class"]


def test_sidebar_disabled(sphinx_build_factory):
    """The sidebar is shrunk when no sidebars specified in html_sidebars."""
    confoverrides = {"html_sidebars.page1": ""}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("page1.html")
    assert "col-md-1" in index_html.select(".bd-sidebar")[0].attrs["class"]


def test_navbar_align_default(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    sphinx_build = sphinx_build_factory("base").build()
    index_html = sphinx_build.html_tree("index.html")
    assert "col-lg-9" in index_html.select("div#navbar-menu")[0].attrs["class"]


def test_navbar_align_right(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    confoverrides = {"html_theme_options.navbar_align": "right"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("index.html")
    assert "col-lg-9" not in index_html.select("div#navbar-menu")[0].attrs["class"]
    assert "ml-auto" in index_html.select("ul#navbar-main-elements")[0].attrs["class"]


def test_navbar_no_in_page_headers(sphinx_build_factory, file_regression):
    # https://github.com/pydata/pydata-sphinx-theme/issues/302
    sphinx_build = sphinx_build_factory("test_navbar_no_in_page_headers").build()

    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul#navbar-main-elements")[0]
    file_regression.check(navbar.prettify(), extension=".html")


def test_sidebars_captions(sphinx_build_factory, file_regression):
    sphinx_build = sphinx_build_factory("sidebars").build()

    subindex_html = sphinx_build.html_tree("section1/index.html")

    # Sidebar structure
    sidebar = subindex_html.select("nav#bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_single(sphinx_build_factory, file_regression):
    confoverrides = {"templates_path": ["_templates_single_sidebar"]}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    index_html = sphinx_build.html_tree("index.html")

    # No navbar included
    assert not index_html.select("nav#navbar-main")
    assert not index_html.select(".navbar-nav")

    # Sidebar structure
    sidebar = index_html.select("nav#bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_level2(sphinx_build_factory, file_regression):
    confoverrides = {"templates_path": ["_templates_sidebar_level2"]}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    subindex_html = sphinx_build.html_tree("section1/subsection1/index.html")

    # Sidebar structure
    sidebar = subindex_html.select("nav#bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_included_toc(sphinx_build_factory):
    """Test that Sphinx project containing TOC (.. toctree::) included
    via .. include:: can be successfully built.
    """
    # Regression test for bug resolved in #347.
    # Tests mainly makes sure that the sphinx_build.build() does not raise exception.
    # https://github.com/pydata/pydata-sphinx-theme/pull/347

    sphinx_build = sphinx_build_factory("test_included_toc").build()
    included_page_html = sphinx_build.html_tree("included-page.html")
    assert included_page_html is not None
