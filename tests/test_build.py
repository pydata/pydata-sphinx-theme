import os
from pathlib import Path
from shutil import copytree

import pytest
import sphinx.errors
from bs4 import BeautifulSoup
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

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
    navbar = index_html.select("div#navbar-center")[0]
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


def test_icon_links(sphinx_build_factory, file_regression):
    html_theme_options_icon_links = {
        "icon_links": [
            {
                "name": "FONTAWESOME",
                "url": "https://site1.org",
                "icon": "FACLASS",
                "type": "fontawesome",
            },
            {
                "name": "FONTAWESOME DEFAULT",
                "url": "https://site2.org",
                "icon": "FADEFAULTCLASS",
                # No type so we can test that the default is fontawesome
            },
            {
                "name": "LOCAL FILE",
                "url": "https://site3.org",
                "icon": "emptylogo.png",  # Logo is our only test site img
                "type": "local",
            },
            {
                "name": "WRONG TYPE",
                "url": "https://site4.org",
                "icon": "WRONG TYPE",
                # Because the type is inccorect, this should output an error `span`
                "type": "incorrecttype",
            },
        ]
    }
    confoverrides = {"html_theme_options": html_theme_options_icon_links}

    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    # Navbar should have the right icons
    icon_links = sphinx_build.html_tree("index.html").select("#navbar-icon-links")[0]
    file_regression.check(
        icon_links.prettify(), basename="navbar_icon_links", extension=".html"
    )


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


def test_favicons(sphinx_build_factory):
    """Test that arbitrary favicons are included."""
    html_theme_options_favicons = {
        "favicons": [
            {
                "rel": "icon",
                "sizes": "16x16",
                "href": "https://secure.example.com/favicon/favicon-16x16.png",
            },
            {
                "rel": "icon",
                "sizes": "32x32",
                "href": "favicon-32x32.png",
            },
            {
                "rel": "apple-touch-icon",
                "sizes": "180x180",
                "href": "apple-touch-icon-180x180.png",
            },
        ]
    }
    confoverrides = {"html_theme_options": html_theme_options_favicons}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    index_html = sphinx_build.html_tree("index.html")

    icon_16 = (
        '<link href="https://secure.example.com/favicon/favicon-16x16.png" '
        'rel="icon" sizes="16x16"/>'
    )
    icon_32 = '<link href="_static/favicon-32x32.png" rel="icon" sizes="32x32"/>'
    icon_180 = (
        '<link href="_static/apple-touch-icon-180x180.png" '
        'rel="apple-touch-icon" sizes="180x180"/>'
    )

    assert icon_16 in str(index_html.select("head")[0])
    assert icon_32 in str(index_html.select("head")[0])
    assert icon_180 in str(index_html.select("head")[0])


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
    assert "col-lg-9" in index_html.select("div#navbar-collapsible")[0].attrs["class"]


def test_navbar_align_right(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    confoverrides = {"html_theme_options.navbar_align": "right"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("index.html")
    assert "col-lg-9" not in index_html.select("div#navbar-center")[0].attrs["class"]
    assert "ml-auto" in index_html.select("div#navbar-center")[0].attrs["class"]


def test_navbar_no_in_page_headers(sphinx_build_factory, file_regression):
    # https://github.com/pydata/pydata-sphinx-theme/issues/302
    sphinx_build = sphinx_build_factory("test_navbar_no_in_page_headers").build()

    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul#navbar-main-elements")[0]
    file_regression.check(navbar.prettify(), extension=".html")


def test_sidebars_captions(sphinx_build_factory, file_regression):
    sphinx_build = sphinx_build_factory("sidebars").build()

    subindex_html = sphinx_build.html_tree("section1/index.html")

    # Sidebar structure with caption
    sidebar = subindex_html.select("nav#bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_nested_page(sphinx_build_factory, file_regression):
    sphinx_build = sphinx_build_factory("sidebars").build()

    subindex_html = sphinx_build.html_tree("section1/subsection1/page1.html")

    # For nested (uncollapsed) page, the label included `checked=""`
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


# html contexts for `show_edit_button`

# these are "good" context fragements that should yield a working link
good_edits = [
    [
        {
            "github_user": "foo",
            "github_repo": "bar",
            "github_version": "HEAD",
            "doc_path": "docs",
        },
        "https://github.com/foo/bar/edit/HEAD/docs/index.rst",
    ],
    [
        {
            "gitlab_user": "foo",
            "gitlab_repo": "bar",
            "gitlab_version": "HEAD",
            "doc_path": "docs",
        },
        "https://gitlab.com/foo/bar/-/edit/HEAD/docs/index.rst",
    ],
    [
        {
            "bitbucket_user": "foo",
            "bitbucket_repo": "bar",
            "bitbucket_version": "HEAD",
            "doc_path": "docs",
        },
        "https://bitbucket.org/foo/bar/src/HEAD/docs/index.rst?mode=edit",
    ],
]


# copy the "good" ones, ensure `doc_path` is agnostic to trailing slashes
slash_edits = [
    [
        {
            # add slashes to doc_path:
            key: f"{value}/" if key == "doc_path" else value
            for key, value in html_context.items()
        },
        # the URL does not change
        url,
    ]
    for html_context, url in good_edits
]

# copy the "good" ones, provide a `<whatever>_url` based off the default
providers = [
    [
        dict(
            # copy all the values
            **html_context,
            # add a provider url
            **{f"{provider}_url": f"https://{provider}.example.com"},
        ),
        f"""https://{provider}.example.com/foo/{url.split("/foo/")[1]}""",
    ]
    for html_context, url in good_edits
    for provider in ["gitlab", "bitbucket", "github"]
    if provider in url
]

# missing any of the values should fail
bad_edits = [
    [
        {
            # copy all the values
            key: value
            for key, value in html_context.items()
            # but not `<provider>_version`
            if "_version" not in key
        },
        None,
    ]
    for html_context, url in good_edits
]

# a good custom URL template
good_custom = [
    [
        {
            "edit_page_url_template": (
                "https://dvcs.example.com/foo/bar/edit/HEAD/{{ file_name }}"
            )
        },
        "https://dvcs.example.com/foo/bar/edit/HEAD/index.rst",
    ]
]

# a bad custom URL template
bad_custom = [
    [
        # it's missing a reference to {{ file_name }}
        {"edit_page_url_template": "http://has-no-file-name"},
        None,
    ]
]

all_edits = [
    *good_edits,
    *slash_edits,
    *bad_edits,
    *good_custom,
    *bad_custom,
    *providers,
]


@pytest.mark.parametrize("html_context,edit_url", all_edits)
def test_edit_page_url(sphinx_build_factory, html_context, edit_url):
    confoverrides = {
        "html_theme_options.use_edit_page_button": True,
        "html_context": html_context,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)

    if edit_url is None:
        with pytest.raises(sphinx.errors.ThemeError):
            sphinx_build.build()
        return

    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")
    edit_link = index_html.select(".editthispage a")
    assert edit_link, "no edit link found"
    assert edit_link[0].attrs["href"] == edit_url, f"edit link didn't match {edit_link}"


def test_new_google_analytics_id(sphinx_build_factory):
    confoverrides = {"html_theme_options.google_analytics_id": "G-XXXXX"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")
    # This text makes the assumption that the google analytics will always be
    # the second last script tag found in the document (last is the theme js).
    script_tag = index_html.select("script")[-2]

    assert "gtag" in script_tag.string
    assert "G-XXXXX" in script_tag.string


def test_old_google_analytics_id(sphinx_build_factory):
    confoverrides = {"html_theme_options.google_analytics_id": "UA-XXXXX"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")
    # This text makes the assumption that the google analytics will always be
    # the second last script tag found in the document (last is the theme js).
    script_tag = index_html.select("script")[-2]

    assert "ga" in script_tag.string
    assert "UA-XXXXX" in script_tag.string


def test_show_nav_level(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    confoverrides = {"html_theme_options.show_nav_level": 2}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("section1/index.html")

    for checkbox in index_html.select("li.toctree-l1.has-children > input"):
        assert "checked" in checkbox.attrs
