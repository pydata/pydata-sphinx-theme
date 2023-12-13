"""All the tests performed in the pydata-sphinx-theme test suit."""

import re
from pathlib import Path

import pytest
import sphinx.errors
from pydata_sphinx_theme.utils import escape_ansi

COMMON_CONF_OVERRIDES = dict(
    navigation_with_keys=False,
    surface_warnings=True,
)


def test_build_html(sphinx_build_factory, file_regression) -> None:
    """Test building the base html template and config."""
    sphinx_build = sphinx_build_factory("base")

    # Basic build with defaults
    sphinx_build.build()
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    index_html = sphinx_build.html_tree("index.html")
    subpage_html = sphinx_build.html_tree("section1/index.html")

    # Navbar structure
    navbar = index_html.select("div.navbar-header-items__center")[0]
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


def test_toc_visibility(sphinx_build_factory) -> None:
    """Test that setting TOC level visibility works as expected."""
    confoverrides = {
        "html_theme_options.show_toc_level": 2,
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")

    # The 3rd level headers should be visible, but not the fourth-level
    assert "visible" in index_html.select(".toc-h2 ul")[0].attrs["class"]
    assert "visible" not in index_html.select(".toc-h3 ul")[0].attrs["class"]


def test_icon_links(sphinx_build_factory, file_regression) -> None:
    """Test that setting icon links are rendered in the documentation."""
    html_theme_options_icon_links = {
        "navigation_with_keys": False,
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
        ],
    }
    confoverrides = {"html_theme_options": html_theme_options_icon_links}

    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    # Navbar should have the right icons
    icon_links = sphinx_build.html_tree("index.html").select(".navbar-icon-links")[0]
    file_regression.check(
        icon_links.prettify(), basename="navbar_icon_links", extension=".html"
    )


@pytest.mark.parametrize(
    "confoverrides,expected_alt_text",
    (
        [dict(), "PyData Tests  documentation - Home"],
        [dict(html_theme_options=dict(logo=dict(text="Foo"))), ""],
        [dict(html_theme_options=dict(logo=dict(text="Foo", alt_text="Bar"))), "Bar"],
    ),
)
def test_logo_alt_text(sphinx_build_factory, confoverrides, expected_alt_text) -> None:
    """Test our alt-text fallback mechanism."""
    confoverrides["html_theme_options"] = (
        confoverrides.get("html_theme_options", False) or dict()
    )
    confoverrides["html_theme_options"].update({"navigation_with_keys": False})
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    logo_image = index_html.select(".navbar-brand img")[0]
    assert logo_image.attrs["alt"] == expected_alt_text


def test_logo_basic(sphinx_build_factory) -> None:
    """Test that the logo is shown by default, project title if no logo."""
    sphinx_build = sphinx_build_factory("base").build()

    # By default logo is shown
    index_html = sphinx_build.html_tree("index.html")
    assert index_html.select(".navbar-brand img")
    assert "emptylogo" in str(index_html.select(".navbar-brand")[0])
    assert not index_html.select(".navbar-brand")[0].text.strip()


def test_logo_no_image(sphinx_build_factory) -> None:
    """Test that the text is shown if no image specified."""
    confoverrides = {
        "html_logo": "",
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    assert "PyData Tests" in index_html.select(".navbar-brand")[0].text.strip()
    assert "emptylogo" not in str(index_html.select(".navbar-brand")[0])


def test_logo_two_images(sphinx_build_factory) -> None:
    """Test that the logo image / text is correct when both dark / light given."""
    # Test with a specified title and a dark logo
    confoverrides = {
        "html_theme_options": {
            "navigation_with_keys": False,
            "logo": {
                "text": "Foo Title",
                "image_dark": "_static/emptydarklogo.png",
            },
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert "emptylogo" in index_str
    assert "emptydarklogo" in index_str
    assert "Foo Title" in index_str


def test_primary_logo_is_light_when_no_default_mode(sphinx_build_factory) -> None:
    """Test that the primary logo image is light when no default mode is set."""
    # Ensure no default mode is set
    confoverrides = {
        "html_context": {},
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar_brand = index_html.select(".navbar-brand")[0]
    assert navbar_brand.find("img", class_="only-light") is not None
    assert navbar_brand.find("script", string=re.compile("only-dark")) is not None


def test_primary_logo_is_light_when_default_mode_is_set_to_auto(
    sphinx_build_factory,
) -> None:
    """Test that the primary logo image is light when default is set to auto."""
    # Ensure no default mode is set
    confoverrides = {
        "html_context": {"default_mode": "auto"},
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar_brand = index_html.select(".navbar-brand")[0]
    assert navbar_brand.find("img", class_="only-light") is not None
    assert navbar_brand.find("script", string=re.compile("only-dark")) is not None


def test_primary_logo_is_light_when_default_mode_is_light(sphinx_build_factory) -> None:
    """Test that the primary logo image is light when default mode is set to light."""
    # Ensure no default mode is set
    confoverrides = {
        "html_context": {"default_mode": "light"},
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar_brand = index_html.select(".navbar-brand")[0]
    assert navbar_brand.find("img", class_="only-light") is not None
    assert navbar_brand.find("script", string=re.compile("only-dark")) is not None


def test_primary_logo_is_dark_when_default_mode_is_dark(sphinx_build_factory) -> None:
    """Test that the primary logo image is dark when default mode is set to dark."""
    # Ensure no default mode is set
    confoverrides = {
        "html_context": {"default_mode": "dark"},
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar_brand = index_html.select(".navbar-brand")[0]
    assert navbar_brand.find("img", class_="only-dark") is not None
    assert navbar_brand.find("script", string=re.compile("only-light")) is not None


def test_logo_missing_image(sphinx_build_factory) -> None:
    """Test that a missing image will raise a warning."""
    # Test with a specified title and a dark logo
    confoverrides = {
        "html_theme_options": {
            **COMMON_CONF_OVERRIDES,
            "logo": {
                # The logo is actually in _static
                "image_dark": "emptydarklogo.png",
            },
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        no_warning=False
    )
    assert "image logo does not exist" in escape_ansi(sphinx_build.warnings).strip()


def test_logo_external_link(sphinx_build_factory) -> None:
    """Test that the logo link is correct for external URLs."""
    # Test with a specified external logo link
    test_url = "https://secure.example.com"
    confoverrides = {
        "html_theme_options": {
            "navigation_with_keys": False,
            "logo": {
                "link": test_url,
            },
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert f'href="{test_url}"' in index_str


def test_logo_external_image(sphinx_build_factory) -> None:
    """Test that the logo link is correct for external URLs."""
    # Test with a specified external logo image source
    test_url = "https://pydata.org/wp-content/uploads/2019/06/pydata-logo-final.png"
    confoverrides = {
        "html_theme_options": {
            "navigation_with_keys": False,
            "logo": {
                "image_dark": test_url,
            },
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    index_str = str(index_html.select(".navbar-brand")[0])
    assert f'src="{test_url}"' in index_str


def test_logo_template_rejected(sphinx_build_factory) -> None:
    """Test that dynamic Sphinx templates are not accepted as logo files."""
    # Test with a specified external logo image source
    confoverrides = {
        "html_theme_options": {
            "navigation_with_keys": False,
            "logo": {
                "image_dark": "image_dark_t",
            },
        },
    }
    with pytest.raises(sphinx.errors.ExtensionError, match="static logo image"):
        sphinx_build_factory("base", confoverrides=confoverrides).build()


@pytest.mark.parametrize(
    "align,klass",
    [
        ("content", ("col-lg-3", "col-lg-9", "me-auto")),
        ("left", ("", "", "me-auto")),
        ("right", ("", "", "ms-auto")),
    ],
)
def test_navbar_align(align, klass, sphinx_build_factory) -> None:
    """The navbar items align with the proper part of the page."""
    confoverrides = {
        "html_theme_options.navbar_align": align,
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    if klass[0]:
        header_start = index_html.select(".navbar-header-items__start")[0]
        assert klass[0] in header_start.attrs["class"]
    if klass[1]:
        header_items = index_html.select(".navbar-header-items")[0]
        assert klass[1] in header_items.attrs["class"]
    header_center = index_html.select(".navbar-header-items__center")[0]
    assert klass[2] in header_center.attrs["class"]


def test_navbar_no_in_page_headers(sphinx_build_factory, file_regression) -> None:
    """Test navbar elements did not change (regression test)."""
    # https://github.com/pydata/pydata-sphinx-theme/issues/302
    sphinx_build = sphinx_build_factory("test_navbar_no_in_page_headers").build()

    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul.bd-navbar-elements")[0]
    file_regression.check(navbar.prettify(), extension=".html")


@pytest.mark.parametrize("n_links", (0, 4, 8))  # 0 = only dropdown, 8 = no dropdown
def test_navbar_header_dropdown(sphinx_build_factory, n_links) -> None:
    """Test whether dropdown appears based on number of header links + config."""
    extra_links = [{"url": f"https://{ii}.org", "name": ii} for ii in range(3)]

    confoverrides = {
        "html_theme_options": {
            "navigation_with_keys": False,
            "external_links": extra_links,
            "header_links_before_dropdown": n_links,
        }
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul.bd-navbar-elements")[0]
    dropdowns = navbar.select("li.dropdown")
    standalone_links = navbar.select(".navbar-nav > li.nav-item:not(.dropdown)")
    if n_links == 0:
        # There should be *only* a dropdown and no standalone links
        assert len(dropdowns) == 1 and not standalone_links
    if n_links == 4:
        # There should be `n_links` standalone links, and a dropdown
        assert len(standalone_links) == n_links and len(dropdowns) == 1
    if n_links == 8:
        # There should be no dropdown and only standalone links
        assert standalone_links and not dropdowns


@pytest.mark.parametrize("dropdown_text", (None, "Other"))  # None -> default "More"
def test_navbar_header_dropdown_button(sphinx_build_factory, dropdown_text) -> None:
    """Test whether dropdown button text is configurable."""
    if dropdown_text:
        confoverrides = {
            "html_theme_options": {
                "navigation_with_keys": False,
                "header_links_before_dropdown": 2,
                "header_dropdown_text": dropdown_text,
            }
        }
    else:
        confoverrides = {
            "html_theme_options": {
                "navigation_with_keys": False,
                "header_links_before_dropdown": 2,
            }
        }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    index_html = sphinx_build.html_tree("index.html")
    navbar = index_html.select("ul.bd-navbar-elements")[0]
    button_text = str(navbar.select("button")[0])
    if dropdown_text:
        # The dropdown text should be "Other"
        assert dropdown_text in button_text
    else:
        # The dropdown text should be "More"
        assert "More" in button_text


def test_sidebars_captions(sphinx_build_factory, file_regression) -> None:
    """Test that the captions are rendered."""
    sphinx_build = sphinx_build_factory("sidebars").build()

    subindex_html = sphinx_build.html_tree("section1/index.html")

    # Sidebar structure with caption
    sidebar = subindex_html.select("nav.bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_nested_page(sphinx_build_factory, file_regression) -> None:
    """Test that nested pages are shown in the sidebar."""
    sphinx_build = sphinx_build_factory("sidebars").build()

    subindex_html = sphinx_build.html_tree("section1/subsection1/page1.html")

    # For nested (uncollapsed) page, the label included `checked=""`
    sidebar = subindex_html.select("nav.bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_level2(sphinx_build_factory, file_regression) -> None:
    """Test sidebars in a second-level page w/ children."""
    confoverrides = {
        "templates_path": ["_templates_sidebar_level2"],
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    subindex_html = sphinx_build.html_tree("section1/subsection1/index.html")

    # Sidebar structure
    sidebar = subindex_html.select("nav.bd-docs-nav")[0]
    file_regression.check(sidebar.prettify(), extension=".html")


def test_sidebars_show_nav_level0(sphinx_build_factory) -> None:
    """Regression test for show_nav_level:0 when the toc is divided into parts.

    Testing both home page and a subsection page for correct elements.
    """
    confoverrides = {
        "html_theme_options.show_nav_level": 0,
        "html_theme_options.navigation_with_keys": False,
    }
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    # 1. Home Page
    index_html = sphinx_build.html_tree("section1/index.html")
    sidebar = index_html.select("nav.bd-docs-nav")[0]

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
    sidebar = subsection_html.select("nav.bd-docs-nav")[0]

    # get all input elements
    input_elem = sidebar.select("input")

    # all input elements should be collapsed in this page
    for ii in input_elem:
        assert "checked" in ii.attrs


def test_included_toc(sphinx_build_factory) -> None:
    """Test that Sphinx project containing TOC (.. toctree::) included via .. include:: can be successfully built."""
    # Regression test for bug resolved in #347.
    # Tests mainly makes sure that the sphinx_build.build() does not raise exception.
    # https://github.com/pydata/pydata-sphinx-theme/pull/347

    sphinx_build = sphinx_build_factory("test_included_toc").build()
    included_page_html = sphinx_build.html_tree("included-page.html")
    assert included_page_html is not None


def test_footer(sphinx_build_factory) -> None:
    """Test for expected footer contents."""
    overrides = {
        "html_theme_options.footer_start": ["copyright.html"],
        "html_theme_options.footer_center": ["sphinx-version.html"],
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=overrides).build()
    index_html = sphinx_build.html_tree("index.html")
    footer_sta = index_html.select("div.footer-items__start")[0]
    footer_ctr = index_html.select("div.footer-items__center")[0]
    footer_end = index_html.select("div.footer-items__end")[0]
    assert "Pydata community" in footer_sta.text
    assert "Created using" in footer_ctr.text
    assert "Built with the" in footer_end.text


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
        ("Edit on GitHub", "https://github.com/foo/bar/edit/HEAD/docs/index.rst"),
    ],
    [
        {
            "gitlab_user": "foo",
            "gitlab_repo": "bar",
            "gitlab_version": "HEAD",
            "doc_path": "docs",
        },
        ("Edit on GitLab", "https://gitlab.com/foo/bar/-/edit/HEAD/docs/index.rst"),
    ],
    [
        {
            "bitbucket_user": "foo",
            "bitbucket_repo": "bar",
            "bitbucket_version": "HEAD",
            "doc_path": "docs",
        },
        (
            "Edit on Bitbucket",
            "https://bitbucket.org/foo/bar/src/HEAD/docs/index.rst?mode=edit",
        ),
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
        # the text and URL do not change
        text_and_url,
    ]
    for html_context, text_and_url in good_edits
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
        (
            text,
            f"""https://{provider}.example.com/foo/{url.split("/foo/")[1]}""",
        ),
    ]
    for html_context, (text, url) in good_edits
    for provider in ["github", "gitlab", "bitbucket"]
    if provider in text.lower()
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
    for html_context, _ in good_edits
]

# a good custom URL template
good_custom = [
    [
        {
            "edit_page_url_template": (
                "https://dvcs.example.com/foo/bar/edit/HEAD/{{ file_name }}"
            )
        },
        ("Edit", "https://dvcs.example.com/foo/bar/edit/HEAD/index.rst"),
    ]
]

# a good custom URL template with an additional provider name
good_custom_with_provider = [
    [
        {
            "edit_page_url_template": (
                "https://dvcs.example.com/foo/bar/edit/HEAD/{{ file_name }}"
            ),
            "edit_page_provider_name": "FooProvider",
        },
        ("Edit on FooProvider", "https://dvcs.example.com/foo/bar/edit/HEAD/index.rst"),
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


@pytest.mark.parametrize("html_context,edit_text_and_url", all_edits)
def test_edit_page_url(sphinx_build_factory, html_context, edit_text_and_url) -> None:
    """Test the edit this page generated link."""
    confoverrides = {
        "html_theme_options.navigation_with_keys": False,
        "html_theme_options.use_edit_page_button": True,
        "html_context": html_context,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)

    if edit_text_and_url is None:
        with pytest.raises(
            sphinx.errors.ExtensionError, match="Missing required value"
        ):
            sphinx_build.build()
        return

    edit_text, edit_url = edit_text_and_url
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")
    edit_link = index_html.select(".editthispage a")
    assert edit_link, "no edit link found"
    assert edit_link[0].attrs["href"] == edit_url, f"edit link didn't match {edit_link}"
    # First child is the icon
    assert (
        list(edit_link[0].strings)[1].strip() == edit_text
    ), f"edit text didn't match {edit_text}"


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
def test_analytics(sphinx_build_factory, provider, tags) -> None:
    """Check the Google analytics."""
    confoverrides = provider
    confoverrides.update({"html_theme_options.navigation_with_keys": False})
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides)
    sphinx_build.build()
    index_html = sphinx_build.html_tree("index.html")

    # Search all the scripts and make sure one of them has the Google tag in there
    tags_found = False
    for script in index_html.select("script"):
        if script.string and tags[0] in script.string and tags[1] in script.string:
            tags_found = True
    assert tags_found is True


def test_plausible(sphinx_build_factory) -> None:
    """Test the Plausible analytics."""
    provider = {
        "html_theme_options.navigation_with_keys": False,
        "html_theme_options.analytics": {
            "plausible_analytics_domain": "toto",
            "plausible_analytics_url": "http://.../script.js",
        },
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


def test_show_nav_level(sphinx_build_factory) -> None:
    """The navbar items align with the proper part of the page."""
    confoverrides = {
        "html_theme_options.navigation_with_keys": False,
        "html_theme_options.show_nav_level": 2,
    }
    sphinx_build = sphinx_build_factory("sidebars", confoverrides=confoverrides).build()

    # Both the column alignment and the margin should be changed
    index_html = sphinx_build.html_tree("section1/index.html")

    for checkbox in index_html.select("li.toctree-l1.has-children > input"):
        assert "checked" in checkbox.attrs


# the switcher files tested in test_version_switcher_error_states, not all of them exist
switcher_files = ["switcher.json", "http://a.b/switcher.json", "missing_url.json"]


@pytest.mark.parametrize("url", switcher_files)
def test_version_switcher_error_states(
    sphinx_build_factory, file_regression, url
) -> None:
    """Regression test the version switcher dropdown HTML.

    Note that a lot of the switcher HTML gets populated by JavaScript,
    so we will not test the final behavior. This just tests for the basic
    structure.

    TODO: Find a way to test Javascript's behavior in populating the HTML.
    """
    confoverrides = {
        "html_theme_options": {
            **COMMON_CONF_OVERRIDES,
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
        switcher = index.select(".navbar-header-items")[0].find(
            "script", string=re.compile(".version-switcher__container")
        )
        file_regression.check(
            switcher.prettify(), basename="navbar_switcher", extension=".html"
        )

    elif url == "http://a.b/switcher.json":  # this file doesn't exist"
        not_read = 'WARNING: The version switcher "http://a.b/switcher.json" file cannot be read due to the following error:\n'
        assert not_read in escape_ansi(sphinx_build.warnings).strip()

    elif url == "missing_url.json":  # this file is missing the url key for one version
        missing_url = (
            'WARNING: The version switcher "missing_url.json" file is malformed; '
            'at least one of the items is missing the "url" or "version" key'
        )
        assert escape_ansi(sphinx_build.warnings).strip() == missing_url


def test_theme_switcher(sphinx_build_factory, file_regression) -> None:
    """Regression test for the theme switcher button."""
    sphinx_build = sphinx_build_factory("base").build()
    switcher = (
        sphinx_build.html_tree("index.html")
        .find(string=re.compile("theme-switch-button"))
        .find_parent("script")
    )
    file_regression.check(
        switcher.prettify(), basename="navbar_theme", extension=".html"
    )


def test_shorten_link(sphinx_build_factory, file_regression) -> None:
    """Regression test for "edit on <provider>" link shortening."""
    sphinx_build = sphinx_build_factory("base").build()

    github = sphinx_build.html_tree("page1.html").select(".github-container")[0]
    file_regression.check(github.prettify(), basename="github_links", extension=".html")

    gitlab = sphinx_build.html_tree("page1.html").select(".gitlab-container")[0]
    file_regression.check(gitlab.prettify(), basename="gitlab_links", extension=".html")


def test_math_header_item(sphinx_build_factory, file_regression) -> None:
    """Regression test for math items in a header title."""
    sphinx_build = sphinx_build_factory("base").build()
    li = sphinx_build.html_tree("page2.html").select(".bd-navbar-elements li")[1]
    file_regression.check(li.prettify(), basename="math_header_item", extension=".html")


@pytest.mark.parametrize(
    ("style_names", "keyword_colors"),
    (
        pytest.param(("fake_foo", "fake_bar"), ("#204a87", "#66d9ef"), id="fake"),
        pytest.param(
            ("a11y-high-contrast-light", "a11y-high-contrast-dark"),
            ("#7928a1", "#dcc6e0"),
            id="real",
        ),
    ),
)
def test_pygments_fallbacks(sphinx_build_factory, style_names, keyword_colors) -> None:
    """Test that setting color themes works.

    NOTE: the expected keyword colors for fake_foo and fake_bar are the colors
    from the fallback styles (tango and monokai, respectively).
    """
    confoverrides = {
        "html_theme_options": {
            **COMMON_CONF_OVERRIDES,
            "pygment_light_style": style_names[0],
            "pygment_dark_style": style_names[1],
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build(
        no_warning=False
    )
    warnings = sphinx_build.warnings.strip().split("\n")
    # see if our warnings worked
    if style_names[0].startswith("fake"):
        assert len(warnings) == 2
        re.match(r"Color theme fake_foo.*tango", warnings[0])
        re.match(r"Color theme fake_bar.*monokai", warnings[1])
    else:
        assert warnings == [""]
    # test that the rendered HTML has highlighting spans
    page_two = sphinx_build.html_tree("page2.html")
    keyword = (
        page_two.select(".highlight-python")[0].select(".highlight")[0].select(".k")[0]
    )
    assert str(keyword) == '<span class="k">as</span>'
    # test that the pygments CSS file specifies the expected colors
    css = Path(sphinx_build.outdir) / "_static" / "pygments.css"
    with open(css) as css_file:
        lines = css_file.readlines()
    assert lines[0].startswith('html[data-theme="light"]')
    for mode, color in dict(zip(["light", "dark"], keyword_colors)).items():
        regexp = re.compile(
            r'html\[data-theme="' + mode + r'"\].*\.k .*color: ' + color
        )
        matches = [regexp.match(line) is not None for line in lines]
        assert sum(matches) == 1


def test_deprecated_build_html(sphinx_build_factory, file_regression) -> None:
    """Test building the base html template with all the deprecated configs."""
    sphinx_build = sphinx_build_factory("deprecated")

    # Basic build with defaults
    sphinx_build.build(no_warning=False)
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    # check the deprecation warnings
    warnings = sphinx_build.warnings.strip("\n").split("\n")
    warnings = [w.lstrip("\x1b[91m").rstrip("\x1b[39;49;00m\n") for w in warnings]
    expected_warnings = (
        "The default value for `navigation_with_keys` will change",
        "The configuration `logo_text` is deprecated",
        "The configuration `favicons` is deprecated.",
        "`footer_items` is deprecated",
        "unsupported theme option 'logo_text'",
    )
    assert len(warnings) == len(expected_warnings)
    for exp_warn in expected_warnings:
        assert exp_warn in sphinx_build.warnings

    index_html = sphinx_build.html_tree("index.html")
    subpage_html = sphinx_build.html_tree("section1/index.html")

    # Navbar structure
    navbar = index_html.select("div.navbar-header-items__center")[0]
    file_regression.check(navbar.prettify(), basename="navbar_ix", extension=".html")

    # Sidebar subpage
    # This re-uses the same HTML template used above (w/o deprecated config)
    # because they should still be the same.
    sidebar = subpage_html.select(".bd-sidebar")[0]
    file_regression.check(
        sidebar.prettify(), basename="sidebar_subpage", extension=".html"
    )

    # Secondary sidebar should not have in-page TOC if it is empty
    assert not sphinx_build.html_tree("page1.html").select("div.onthispage")

    # Secondary sidebar should not be present if page-level metadata given
    assert not sphinx_build.html_tree("page2.html").select("div.bd-sidebar-secondary")


def test_empty_templates(sphinx_build_factory) -> None:
    """If a template is empty (e.g., via a config), it should be removed."""
    # When configured to be gone, the template should be removed w/ its parent.
    # ABlog needs to be added so we can test that template rendering works w/ it.
    confoverrides = {
        "html_theme_options.navigation_with_keys": False,
        "html_show_sourcelink": False,
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("page1.html")

    # We've set this to false in the config so the template shouldn't show up at all
    assert not html.select(".tocsection.sourcelink")

    # Should not be any icon link wrapper because none are given in conf
    assert not html.select(".navbar-icon-links")


def test_translations(sphinx_build_factory) -> None:
    """Test that basic translation functionality works.

    This will build our test site with the French language, and test
    that a few phrases are in French.

    We use this test to catch regressions if we change wording without
    changing the translation files.
    """
    confoverrides = {
        "language": "fr",
        "html_context": {
            "github_user": "pydata",
            "github_repo": "pydata-sphinx-theme",
            "github_version": "main",
        },
        "html_theme_options": {
            "navigation_with_keys": False,
            "use_edit_page_button": True,
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()

    # Use a section page so that we have section navigation in the sidebar
    index = sphinx_build.html_tree("section1/index.html")

    sidebar_primary = index.select(".bd-sidebar-primary")[0]
    assert "Navigation du site" in str(sidebar_primary)
    assert "Navigation de la section" in str(sidebar_primary)

    sidebar_secondary = index.select(".bd-sidebar-secondary")[0]
    assert "Montrer le code source" in str(sidebar_secondary)
    assert "Modifier sur GitHub" in str(sidebar_secondary)

    header = index.select(".bd-header")[0]
    assert "clair/sombre" in str(header)

    footer = index.select(".bd-footer")[0]
    assert "Copyright" in str(footer)
    assert "Créé en utilisant" in str(footer)
    assert "Construit avec le" in str(footer)

    footer_article = index.select(".prev-next-area")[0]
    assert "précédent" in str(footer_article)
    assert "page suivante" in str(footer_article)

    # Search bar
    # TODO: Add translations where there are english phrases below
    assert "Search the docs" in str(index.select(".bd-search")[0])
