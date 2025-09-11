"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------
import os
import sys

from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.locale import _

import pydata_sphinx_theme


sys.path.append(str(Path(".").resolve()))

# -- Project information -----------------------------------------------------

project = "PyData Theme"
copyright = "2019, PyData Community"
author = "PyData Community"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.graphviz",
    "sphinxext.rediraffe",
    "sphinx_design",
    "sphinx_copybutton",
    "autoapi.extension",
    # custom extentions
    "_extension.gallery_directive",
    "_extension.component_directive",
    # For extension examples and demos
    "myst_parser",
    "ablog",
    "jupyter_sphinx",
    "sphinxcontrib.youtube",
    "nbsphinx",
    "numpydoc",
    "sphinx_togglebutton",
    "jupyterlite_sphinx",
    "sphinx_favicon",
]

jupyterlite_config = "jupyterlite_config.json"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

intersphinx_mapping = {"sphinx": ("https://www.sphinx-doc.org/en/master", None)}

# -- Sitemap -----------------------------------------------------------------

# ReadTheDocs has its own way of generating sitemaps, etc.
if not os.environ.get("READTHEDOCS"):
    extensions += ["sphinx_sitemap"]

    html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"

# -- MyST options ------------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence", "linkify", "substitution"]
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = "en"

# -- Ablog options -----------------------------------------------------------

blog_path = "examples/blog/index"
blog_authors = {
    "pydata": ("PyData", "https://pydata.org"),
    "jupyter": ("Jupyter", "https://jupyter.org"),
}


# -- sphinx_ext_graphviz options ---------------------------------------------

graphviz_output_format = "svg"
inheritance_graph_attrs = dict(
    rankdir="LR",
    fontsize=14,
    ratio="compress",
)

# -- sphinx_togglebutton options ---------------------------------------------
togglebutton_hint = str(_("Click to expand"))
togglebutton_hint_hide = str(_("Click to collapse"))

# -- Sphinx-copybutton options ---------------------------------------------
# Exclude copy button from appearing over notebook cell numbers by using :not()
# The default copybutton selector is `div.highlight pre`
# https://github.com/executablebooks/sphinx-copybutton/blob/master/sphinx_copybutton/__init__.py#L82
copybutton_exclude = ".linenos, .gp"
copybutton_selector = ":not(.prompt) > div.highlight pre"

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"
html_sourcelink_suffix = ""
html_last_updated_fmt = ""  # to reveal the build date in the pages meta

# Define the json_url for our version switcher.
json_url = "https://pydata-sphinx-theme.readthedocs.io/en/latest/_static/switcher.json"

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("READTHEDOCS_VERSION")
release = pydata_sphinx_theme.__version__
# If READTHEDOCS_VERSION doesn't exist, we're not on RTD
# If it is an integer, we're in a PR build and the version isn't correct.
# If it's "latest" → change to "dev" (that's what we want the switcher to call it)
if not version_match or version_match.isdigit() or version_match == "latest":
    # For local development, infer the version to match from the package.
    if "dev" in release or "rc" in release:
        version_match = "dev"
        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "_static/switcher.json"
    else:
        version_match = f"v{release}"
elif version_match == "stable":
    version_match = f"v{release}"

html_theme_options = {
    "external_links": [
        {
            "url": "https://pydata.org",
            "name": "PyData Website",
        },
        {
            "url": "https://numfocus.org/",
            "name": "NumFocus",
        },
        {
            "url": "https://numfocus.org/donate",
            "name": "Donate to NumFocus",
        },
    ],
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "X",
            "url": "https://x.com/PyData",
            "icon": "fa-brands fa-x-twitter",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/pydata/pydata-sphinx-theme",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pydata-sphinx-theme",
            "icon": "fa-custom fa-pypi",
        },
        {
            "name": "PyData",
            "url": "https://pydata.org",
            "icon": "fa-custom fa-pydata",
        },
    ],
    # alternative way to set twitter and github header icons
    # "github_url": "https://github.com/pydata/pydata-sphinx-theme",
    # "twitter_url": "https://twitter.com/PyData",
    "logo": {
        "text": "PyData Theme",
        "image_dark": "_static/logo-dark.svg",
    },
    "use_edit_page_button": True,
    "show_toc_level": 1,
    # [left, content, right] For testing that the navbar items align properly
    "navbar_align": "left",
    # "show_nav_level": 2,
    "announcement": "https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/main/docs/_templates/custom-template.html",
    "show_version_warning_banner": True,
    "navbar_center": ["version-switcher", "navbar-nav"],
    # "navbar_start": ["navbar-logo"],
    # "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # "navbar_persistent": ["search-button"],
    # "primary_sidebar_end": ["custom-template", "sidebar-ethical-ads"],
    # "article_footer_items": ["test", "test"],
    # "content_footer_items": ["test", "test"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
        "examples/no-sidebar": [],
    },
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
    # "back_to_top_button": False,
    "search_as_you_type": True,
}

html_sidebars = {
    "community/index": [
        "sidebar-nav-bs",
        "custom-template",
    ],  # This ensures we test for custom sidebars
    "examples/no-sidebar": [],  # Test what page looks like with no sidebar items
    "examples/persistent-search-field": ["search-field"],
    # Blog sidebars
    # ref: https://ablog.readthedocs.io/manual/ablog-configuration-options/#blog-sidebars
    "examples/blog/*": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/authors.html",
        "ablog/languages.html",
        "ablog/locations.html",
        "ablog/archives.html",
    ],
}

html_context = {
    "github_user": "pydata",
    "github_repo": "pydata-sphinx-theme",
    "github_version": "main",
    "doc_path": "docs",
}

rediraffe_redirects = {
    "contributing.rst": "community/index.rst",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = [
    ("custom-icons.js", {"defer": "defer"}),
]
todo_include_todos = True

# -- favicon options ---------------------------------------------------------

# see https://sphinx-favicon.readthedocs.io for more information about the
# sphinx-favicon extension
favicons = [
    # generic icons compatible with most browsers
    "favicon-32x32.png",
    "favicon-16x16.png",
    {"rel": "shortcut icon", "sizes": "any", "href": "favicon.ico"},
    # chrome specific
    "android-chrome-192x192.png",
    # apple icons
    {"rel": "mask-icon", "color": "#459db9", "href": "safari-pinned-tab.svg"},
    {"rel": "apple-touch-icon", "href": "apple-touch-icon.png"},
    # msapplications
    {"name": "msapplication-TileColor", "content": "#459db9"},
    {"name": "theme-color", "content": "#ffffff"},
    {"name": "msapplication-TileImage", "content": "mstile-150x150.png"},
]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autodoc_typehints = "description"
autodoc_member_order = "groupwise"

# -- Options for autoapi -------------------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../src/pydata_sphinx_theme"]
autoapi_keep_files = True
autoapi_root = "api"
autoapi_member_order = "groupwise"

# -- Warnings / Nitpicky -------------------------------------------------------

nitpicky = True
bad_classes = (
    r".*abc def.*",  # urllib.parse.unquote_to_bytes
    r"api_sample\.RandomNumberGenerator",
    r"bs4\.BeautifulSoup",
    r"docutils\.nodes\.Node",
    r"matplotlib\.artist\.Artist",  # matplotlib xrefs are in the class diagram demo
    r"matplotlib\.figure\.Figure",
    r"matplotlib\.figure\.FigureBase",
    r"pygments\.formatters\.HtmlFormatter",
)
nitpick_ignore_regex = [
    *[("py:class", target) for target in bad_classes],
    # we demo some `urllib` docs on our site; don't care that its xrefs fail to resolve
    ("py:obj", r"urllib\.parse\.(Defrag|Parse|Split)Result(Bytes)?\.(count|index)"),
    # the kitchen sink pages include some intentional errors
    ("token", r"(suite|expression|target)"),
]

# -- application setup -------------------------------------------------------


def setup_to_main(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """
    Add a function that jinja can access for returning an "edit this page" link
    pointing to `main`.
    """

    def to_main(link: str) -> str:
        """
        Transform "edit on github" links and make sure they always point to the
        main branch.

        Args:
            link: the link to the github edit interface

        Returns:
            the link to the tip of the main branch for the same file
        """
        links = link.split("/")
        idx = links.index("edit")
        return "/".join(links[: idx + 1]) + "/main/" + "/".join(links[idx + 2 :])

    context["to_main"] = to_main


def setup(app: Sphinx) -> Dict[str, Any]:
    """Add custom configuration to sphinx app.

    Args:
        app: the Sphinx application
    Returns:
        the 2 parallel parameters set to ``True``.
    """
    app.connect("html-page-context", setup_to_main)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# -- linkcheck options ---------------------------------------------------------

linkcheck_anchors_ignore = [
    # match any anchor that starts with a '/' since this is an invalid HTML anchor
    r"\/.*",
]

linkcheck_ignore = [
    # The crawler gets "Anchor not found" for various anchors
    r"https://github.com.+?#.*",
    r"https://www.sphinx-doc.org/en/master/*/.+?#.+?",
    # sample urls
    "http://someurl/release-0.1.0.tar-gz",
    "http://python.py",
    # for whatever reason the Ablog index is treated as broken
    "../examples/blog/index.html",
    # get a 403 on CI
    "https://canvas.workday.com/styles/tokens/type",
    "https://unsplash.com/",
    r"https?://www.gnu.org/software/gettext/.*",
]

linkcheck_allowed_redirects = {
    r"http://www.python.org": "https://www.python.org/",
    # :source:`something` linking files in the repository
    r"https://github.com/pydata/pydata-sphinx-theme/tree/.*": r"https://github.com/pydata/pydata-sphinx-theme/blob/.*",
    r"https://github.com/sphinx-themes/sphinx-themes.org/raw/.*": r"https://github.com/sphinx-themes/sphinx-themes.org/tree/.*",
    # project redirects
    r"https://pypi.org/project/[A-Za-z\d_\-\.]+/": r"https://pypi.org/project/[a-z\d\-\.]+/",
    r"https://virtualenv.pypa.io/": "https://virtualenv.pypa.io/en/latest/",
    # catching redirects in rtd
    r"https://[A-Za-z\d_\-\.]+.readthedocs.io/": r"https://[A-Za-z\d_\-\.]+\.readthedocs\.io(/en)?/(stable|latest)/",
    r"https://readthedocs.org/": r"https://about.readthedocs.com/\?ref=app.readthedocs.org",
    r"https://app.readthedocs.org/dashboard/": r"https://app.readthedocs.org/accounts/login/\?next=/dashboard/",
    # miscellanenous urls
    r"https://python.arviz.org/": "https://python.arviz.org/en/stable/",
    r"https://www.sphinx-doc.org/": "https://www.sphinx-doc.org/en/master/",
    r"https://idtracker.ai/": "https://idtracker.ai/latest/",
    r"https://gitlab.com": "https://about.gitlab.com/",
    r"http://www.yahoo.com": "https://www.yahoo.com/",
    r"https://feature-engine.readthedocs.io/": "https://feature-engine.trainindata.com/en/latest/",
    r"https://picsum.photos/": r"https://fastly.picsum.photos/",
}

# we have had issues with linkcheck timing and retries on www.gnu.org
linkcheck_retries = 1
linkcheck_timeout = 5
linkcheck_report_timeouts_as_broken = True
