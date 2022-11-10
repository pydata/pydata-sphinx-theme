import os
import re
from pathlib import Path
from shutil import copytree

import pytest
import sphinx.errors
from bs4 import BeautifulSoup
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

path_tests = Path(__file__).parent


def escape_ansi(string):
    """helper function to remove ansi coloring from sphinx warnings"""
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    return ansi_escape.sub("", string)


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self, no_warning=True):
        self.app.build()
        if no_warning is True:
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
            srcdir=sphinx_path(os.path.abspath(tmp_path / src_folder)), **kwargs
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

    # Sidebar subpage
    sidebar = subpage_html.select(".bd-sidebar")[0]
    file_regression.check(
        sidebar.prettify(), basename="sidebar_subpage", extension=".html"
    )

    # Secondary sidebar should not have in-page TOC if it is empty
    assert not sphinx_build.html_tree("page1.html").select("div.onthispage")

    # Secondary sidebar should not be present if page-level metadata given
    assert not sphinx_build.html_tree("page2.html").select("div.bd-sidebar-secondary")


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
            {
                "name": "URL",
                "url": "https://site5.org",
                "icon": "https://site5.org/image.svg",
                "type": "url",
            },
            {
                "name": "FONTAWESOME",
                "url": "https://site1.org",
                "icon": "FACLASS",
                "type": "fontawesome",
                "attributes": {
                    # This should over-ride the href above
                    "href": "https://override.com",
                    # This should add a new icon link attribute
                    "foo": "bar",
                    # CSS classes should be totally overwritten
                    "class": "overridden classes",
                },
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


def test_logo_basic(sphinx_build_factory):
    """Test that the logo is shown by default, project title if no logo."""
    sphinx_build = sphinx_build_factory("base").build()

    # By default logo is shown
    index_html = sphinx_build.html_tree("index.html")
    assert index_html.select(".navbar-brand img")
    assert "emptylogo" in str(index_html.select(".navbar-brand")[0])
    assert not index_html.select(".navbar-brand")[0].text.strip()


def test_logo_no_image(sphinx_build_factory):
    """Test that the text is shown if no image specified."""
    confoverrides = {"html_logo": ""}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    assert "PyData Tests" in index_html.select(".navbar-brand")[0].text.strip()
    assert "emptylogo" not in str(index_html.select(".navbar-brand")[0])


def test_logo_two_images(sphinx_build_factory):
    """Test that the logo image / text is correct when both dark / light given."""
    # Test with a specified title and a dark logo
    confoverrides = {
        "html_theme_options": {
            "logo": {
                "text": "Foo Title",
                "image_dark": "emptydarklogo.png",
            }
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert "emptylogo" in index_str
    assert "emptydarklogo" in index_str
    assert "Foo Title" in index_str


def test_logo_external_link(sphinx_build_factory):
    """Test that the logo link is correct for external URLs."""
    # Test with a specified external logo link
    test_url = "https://secure.example.com"
    confoverrides = {
        "html_theme_options": {
            "logo": {
                "link": test_url,
            }
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert f'href="{test_url}"' in index_str


def test_logo_external_image(sphinx_build_factory):
    """Test that the logo link is correct for external URLs."""
    # Test with a specified external logo image source
    test_url = "https://pydata.org/wp-content/uploads/2019/06/pydata-logo-final.png"
    confoverrides = {
        "html_theme_options": {
            "logo": {
                "image_dark": test_url,
            }
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert f'src="{test_url}"' in index_str


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
        'rel="icon" sizes="16x16" type="image/png">'
    )
    icon_32 = (
        '<link href="_static/favicon-32x32.png" rel="icon" sizes="32x32" '
        'type="image/png">'
    )
    icon_180 = (
        '<link href="_static/apple-touch-icon-180x180.png" '
        'rel="apple-touch-icon" sizes="180x180" type="image/png">'
    )
    assert icon_16 in str(index_html.select("head")[0])
    assert icon_32 in str(index_html.select("head")[0])
    assert icon_180 in str(index_html.select("head")[0])


def test_navbar_align_default(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    sphinx_build = sphinx_build_factory("base").build()
    index_html = sphinx_build.html_tree("index.html")
    assert "col-lg-9" in index_html.select(".navbar-header-items")[0].attrs["class"]


def test_navbar_align_right(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    confoverrides = {"html_theme_options.navbar_align": "right"}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("index.html")
    assert "col-lg-9" not in index_html.select(".navbar-header-items")[0].attrs["class"]
    assert "ml-auto" in index_html.select("div#navbar-center")[0].attrs["class"]


def test_navbar_no_in_page_headers(sphinx_build_factory, file_regression):
    # https://github.com/pydata/pydata-sphinx-theme/issues/302
    sphinx_build = sphinx_build_factory("test_navbar_no_in_page_headers").build()

    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul#navbar-main-elements")[0]
    file_regression.check(navbar.prettify(), extension=".html")


@pytest.mark.parametrize("n_links", (0, 4, 8))  # 0 = only dropdown, 8 = no dropdown
def test_navbar_header_dropdown(sphinx_build_factory, file_regression, n_links):
    """Test whether dropdown appears based on number of header links + config."""
    extra_links = [{"url": f"https://{ii}.org", "name": ii} for ii in range(3)]

    confoverrides = {
        "html_theme_options": {
            "external_links": extra_links,
            "header_links_before_dropdown": n_links,
        }
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul#navbar-main-elements")[0]
    if n_links == 0:
        # There should be *only* a dropdown and no standalone links
        assert navbar.select("div.dropdown") and not navbar.select(
            ".navbar-nav > li.nav-item"
        )  # noqa
    if n_links == 4:
        # There should be at least one standalone link, and a dropdown
        assert navbar.select(".navbar-nav > li.nav-item") and navbar.select(
            "div.dropdown"
        )  # noqa
    if n_links == 8:
        # There should be no dropdown and only standalone links
        assert navbar.select(".navbar-nav > li.nav-item") and not navbar.select(
            "div.dropdown"
        )  # noqa


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


def test_sidebars_level2(sphinx_build_factory, file_regression):
    """Sidebars in a second-level page w/ children"""
    confoverrides = {"templates_path": ["_templates_sidebar_level2"]}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    subindex_html = sphinx_build.html_tree("section1/subsection1/index.html")

    # Sidebar structure
    sidebar = subindex_html.select("nav#bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_show_nav_level0(sphinx_build_factory, file_regression):
    """
    Regression test for show_nav_level:0 when the toc is divided into parts.
    Testing both home page and a subsection page for correct elements.
    """
    confoverrides = {"html_theme_options.show_nav_level": 0}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    # 1. Home Page
    index_html = sphinx_build.html_tree("section1/index.html")
    sidebar = index_html.select("nav#bd-docs-nav")[0]

    # check if top-level ul is present
    ul = sidebar.find("ul")
    assert "list-caption" in ul.attrs["class"]

    # get all li elements
    li = ul.select("li")

    # part li
    assert "toctree-l0 has-children" in " ".join(li[0].attrs["class"])
    assert "caption-text" in li[0].select("p span")[0].attrs["class"]
    assert "label-parts" in li[0].find("label").attrs["class"]

    # basic checks on other levels
    assert "toctree-l1 has-children" in " ".join(li[1].attrs["class"])
    assert "toctree-l2" in li[2].attrs["class"]

    # 2. Subsection Page
    subsection_html = sphinx_build.html_tree("section1/subsection1/index.html")
    sidebar = subsection_html.select("nav#bd-docs-nav")[0]

    # get all input elements
    input_elem = sidebar.select("input")

    # all input elements should be collapsed in this page
    for ii in input_elem:
        assert "checked" in ii.attrs


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

# these are "good" context fragments that should yield a working link
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


@pytest.mark.parametrize(
    "provider,tags",
    [
        # google analytics
        (
            {"html_theme_options.analytics": {"google_analytics_id": "G-XXXXX"}},
            ["gtag", "G-XXXXX"],
        ),
        # google and plausible
        (
            {
                "html_theme_options.analytics": {
                    "google_analytics_id": "G-XXXXX",
                    "plausible_analytics_domain": "toto",
                    "plausible_analytics_url": "http://.../script.js",
                }
            },
            ["gtag", "G-XXXXX"],
        ),
    ],
)
def test_analytics(sphinx_build_factory, provider, tags):

    confoverrides = provider
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")

    # Search all the scripts and make sure one of them has the Google tag in there
    tags_found = False
    for script in index_html.select("script"):
        if script.string and tags[0] in script.string and tags[1] in script.string:
            tags_found = True
    assert tags_found is True


def test_plausible(sphinx_build_factory):
    provider = {
        "html_theme_options.analytics": {
            "plausible_analytics_domain": "toto",
            "plausible_analytics_url": "http://.../script.js",
        }
    }
    confoverrides = provider
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")

    # Search all the scripts and make sure one of them has the Google tag in there
    attr_found = False
    for script in index_html.select("script"):
        if script.attrs.get("data-domain") == "toto":
            attr_found = True
    assert attr_found is True


def test_show_nav_level(sphinx_build_factory):
    """The navbar items align with the proper part of the page."""
    confoverrides = {"html_theme_options.show_nav_level": 2}
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("section1/index.html")

    for checkbox in index_html.select("li.toctree-l1.has-children > input"):
        assert "checked" in checkbox.attrs


switcher_files = ["switcher.json", "http://a.b/switcher.json", "missing_url.json"]
"the switcher files tested in test_version_switcher, not all of them exist"


@pytest.mark.parametrize("url", switcher_files)
def test_version_switcher(sphinx_build_factory, file_regression, url):
    """Regression test the version switcher dropdown HTML.

    Note that a lot of the switcher HTML gets populated by JavaScript,
    so we will not test the final behavior. This just tests for the basic
    structure.

    TODO: Find a way to test Javascript's behavior in populating the HTML.
    """
    confoverrides = {
        "html_theme_options": {
            "navbar_end": ["version-switcher"],
            "switcher": {
                "json_url": url,
                "version_match": "0.7.1",
            },
        }
    }
    factory = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build = factory.build(no_warning=False)

    if url == "switcher.json":  # this should work
        index = sphinx_build.html_tree("index.html")
        switcher = index.select(".version-switcher__container")[0]
        file_regression.check(
            switcher.prettify(), basename="navbar_switcher", extension=".html"
        )

    elif url == "http://a.b/switcher.json":  # this file doesn't exist"
        not_read = 'WARNING: The version switcher "http://a.b/switcher.json" file cannot be read due to the following error:\n'  # noqa
        assert not_read in escape_ansi(sphinx_build.warnings).strip()

    elif url == "missing_url.json":  # this file is missing the url key for one version
        missing_url = 'WARNING: The version switcher "missing_url.json" file is malformed at least one of the items is missing the "url" or "version" key'  # noqa
        assert escape_ansi(sphinx_build.warnings).strip() == missing_url


def test_theme_switcher(sphinx_build_factory, file_regression):
    """Regression test the theme switcher btn HTML"""

    sphinx_build = sphinx_build_factory("base").build()
    switcher = sphinx_build.html_tree("index.html").select(".theme-switch-button")[0]
    file_regression.check(
        switcher.prettify(), basename="navbar_theme", extension=".html"
    )


def test_shorten_link(sphinx_build_factory, file_regression):
    """regression test the shorten links html"""

    sphinx_build = sphinx_build_factory("base").build()

    github = sphinx_build.html_tree("page1.html").select(".github-container")[0]
    file_regression.check(github.prettify(), basename="github_links", extension=".html")

    gitlab = sphinx_build.html_tree("page1.html").select(".gitlab-container")[0]
    file_regression.check(gitlab.prettify(), basename="gitlab_links", extension=".html")


def test_math_header_item(sphinx_build_factory, file_regression):
    """regression test the math items in a header title"""

    sphinx_build = sphinx_build_factory("base").build()
    li = sphinx_build.html_tree("page2.html").select("#navbar-main-elements li")[1]
    file_regression.check(li.prettify(), basename="math_header_item", extension=".html")


def test_deprecated_build_html(sphinx_build_factory, file_regression):
    """Test building the base html template with all the deprecated configs"""

    sphinx_build = sphinx_build_factory("deprecated")  # type: SphinxBuild

    # Basic build with defaults
    sphinx_build.build(no_warning=False)
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    # check the deprecation warnings
    warnings = sphinx_build.warnings.split("WARNING: ")
    assert len(warnings) == 5  # testing the text of the warning is not necessary here

    index_html = sphinx_build.html_tree("index.html")
    subpage_html = sphinx_build.html_tree("section1/index.html")

    # Navbar structure
    navbar = index_html.select("div#navbar-center")[0]
    file_regression.check(navbar.prettify(), basename="navbar_ix", extension=".html")

    # Sidebar subpage
    sidebar = subpage_html.select(".bd-sidebar")[0]
    file_regression.check(
        sidebar.prettify(), basename="sidebar_subpage", extension=".html"
    )

    # Secondary sidebar should not have in-page TOC if it is empty
    assert not sphinx_build.html_tree("page1.html").select("div.onthispage")

    # Secondary sidebar should not be present if page-level metadata given
    assert not sphinx_build.html_tree("page2.html").select("div.bd-sidebar-secondary")
