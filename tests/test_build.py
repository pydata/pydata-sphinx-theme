from bs4 import BeautifulSoup
from pathlib import Path
from subprocess import run
from shutil import copytree, rmtree
import pytest


path_tests = Path(__file__).parent.resolve()
path_base = path_tests.joinpath("sites", "base")


@pytest.fixture(scope="session")
def sphinx_build(tmpdir_factory):
    class SphinxBuild:
        path_tmp = Path(tmpdir_factory.mktemp("build"))
        path_docs = path_tmp.joinpath("testdocs")
        path_build = path_docs.joinpath("_build")
        path_html = path_build.joinpath("html")
        path_pg_index = path_html.joinpath("index.html")
        cmd_base = ["sphinx-build", ".", "_build/html", "-a", "-W"]

        def copy(self, path=None):
            """Copy the specified book to our tests folder for building."""
            if path is None:
                path = path_base
            if not self.path_docs.exists():
                copytree(path, self.path_docs)

        def build(self, cmd=None):
            """Build the test book"""
            cmd = [] if cmd is None else cmd
            run(self.cmd_base + cmd, cwd=self.path_docs, check=True)

        def get(self, pagename):
            path_page = self.path_html.joinpath(pagename)
            if not path_page.exists():
                raise ValueError(f"{path_page} does not exist")
            return BeautifulSoup(path_page.read_text(), "html.parser")

        def clean(self):
            """Clean the _build folder so files don't clash with new tests."""
            rmtree(self.path_build)

    return SphinxBuild()


def test_build_book(file_regression, sphinx_build):
    """Test building the base book template and config."""
    sphinx_build.copy()

    # Basic build with defaults
    sphinx_build.build()
    index_html = sphinx_build.get("index.html")
    subpage_html = sphinx_build.get("section1/index.html")

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

    sphinx_build.clean()


def test_toc_visibility(file_regression, sphinx_build):
    sphinx_build.copy()

    # Test that setting TOC level visibility works as expected
    sphinx_build.build(["-D", "html_theme_options.show_toc_level=2"])
    index_html = sphinx_build.get("index.html")

    # The 3rd level headers should be visible, but not the fourth-level
    assert "visible" in index_html.select(".toc-h2 ul")[0].attrs["class"]
    assert "visible" not in index_html.select(".toc-h3 ul")[0].attrs["class"]


def test_logo_name(file_regression, sphinx_build):
    """Test that the logo is shown by default, project title if no logo."""
    sphinx_build.copy()

    # By default logo is shown
    sphinx_build.build()
    index_html = sphinx_build.get("index.html")
    assert index_html.select(".navbar-brand img")
    assert not index_html.select(".navbar-brand")[0].text.strip()
    sphinx_build.clean()

    # Test that setting TOC level visibility works as expected
    sphinx_build.build(["-D", "html_logo="])
    index_html = sphinx_build.get("index.html")
    assert "PyData Tests" in index_html.select(".navbar-brand")[0].text.strip()


def test_sidebar_visible(sphinx_build):
    """The sidebar is shrunk when no sidebars specified in html_sidebars."""
    sphinx_build.copy()

    sphinx_build.build()
    index_html = sphinx_build.get("page1.html")
    assert "col-md-3" in index_html.select(".bd-sidebar")[0].attrs["class"]

    sphinx_build.build(["-D", "html_sidebars.page1="])
    index_html = sphinx_build.get("page1.html")
    assert "col-md-1" in index_html.select(".bd-sidebar")[0].attrs["class"]
    sphinx_build.clean()


def test_navbar_snap_left(sphinx_build):
    """The sidebar is shrunk when no sidebars specified in html_sidebars."""
    sphinx_build.copy()

    sphinx_build.build()
    index_html = sphinx_build.get("index.html")
    assert "col-lg-9" in index_html.select("div#navbar-menu")[0].attrs["class"]

    sphinx_build.build(["-D", "html_theme_options.navbar_snap_left=True"])
    index_html = sphinx_build.get("index.html")
    assert "col-11" in index_html.select("div#navbar-menu")[0].attrs["class"]
    sphinx_build.clean()
