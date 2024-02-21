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

import pydata_sphinx_theme
from sphinx.application import Sphinx

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
            "name": "PyData",
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
            "name": "Twitter",
            "url": "https://twitter.com/PyData",
            "icon": "fa-brands fa-twitter",
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
            "icon": "_static/pydata-logo.png",
            "type": "local",
            "attributes": {"target": "_blank"},
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
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
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
html_js_files = ["custom-icon.js"]
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

# -- application setup -------------------------------------------------------


def setup_to_main(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """Add a function that jinja can access for returning an "edit this page" link pointing to `main`."""

    def to_main(link: str) -> str:
        """Transform "edit on github" links and make sure they always point to the main branch.

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
