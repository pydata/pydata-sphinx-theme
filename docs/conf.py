# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os

# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "PyData Sphinx Theme"
copyright = "2019, PyData Community"
author = "PyData Community"

import pydata_sphinx_theme


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "jupyter_sphinx",
    "myst_parser",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinxext.rediraffe",
    "sphinx_design",
    "sphinx.ext.viewcode",
]

# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"

# ReadTheDocs has its own way of generating sitemaps, etc.
if not os.environ.get("READTHEDOCS"):
    extensions += ["sphinx_sitemap"]

    # -- Sitemap -------------------------------------------------------------
    html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Extension options -------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
# html_logo = "_static/pandas.svg"  # For testing

# Define the json_url for our version switcher.
json_url = "https://pydata-sphinx-theme.readthedocs.io/en/latest/_static/switcher.json"

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("READTHEDOCS_VERSION")
# If READTHEDOCS_VERSION doesn't exist, we're not on RTD
# If it is an integer, we're in a PR build and the version isn't correct.
if not version_match or version_match.isdigit():
    # For local development, infer the version to match from the package.
    release = pydata_sphinx_theme.__version__
    if "dev" in release:
        version_match = "latest"
        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "/_static/switcher.json"
    else:
        version_match = "v" + release

html_theme_options = {
    "external_links": [
        {
            "url": "https://github.com/pydata/pydata-sphinx-theme/releases",
            "name": "Changelog",
        },
        {"url": "https://pandas.pydata.org/pandas-docs/stable/", "name": "Pandas Docs"},
    ],
    "github_url": "https://github.com/pydata/pydata-sphinx-theme",
    "twitter_url": "https://twitter.com/pandas_dev",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pydata-sphinx-theme",
            "icon": "fas fa-box",
        },
        {
            "name": "Pandas",
            "url": "https://pandas.pydata.org",
            "icon": "_static/pandas-square.svg",
            "type": "local",
        },
    ],
    "use_edit_page_button": True,
    "show_toc_level": 1,
    # "show_nav_level": 2,
    # "search_bar_position": "navbar",  # TODO: Deprecated - remove in future version
    # "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "navbar_start": ["navbar-logo", "navbar-version"],
    # "navbar_center": ["navbar-nav", "navbar-version"],  # Just for testing
    "navbar_end": ["theme-switcher", "version-switcher", "navbar-icon-links"],
    # "left_sidebar_end": ["custom-template.html", "sidebar-ethical-ads.html"],
    # "footer_items": ["copyright", "sphinx-version", ""]
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
}

html_sidebars = {
    "contribute/index": [
        "search-field",
        "sidebar-nav-bs",
        "custom-template",
    ],  # This ensures we test for custom sidebars
    "demo/no-sidebar": [],  # Test what page looks like with no sidebar items
}

myst_heading_anchors = 2

html_context = {
    "github_user": "pydata",
    "github_repo": "pydata-sphinx-theme",
    "github_version": "main",
    "doc_path": "docs",
}

rediraffe_redirects = {
    "contributing.rst": "contribute/index.rst",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# --- custom gallery of websites -----------------------------------------------
from pathlib import Path
import json
from shutil import copy
from playwright.sync_api import sync_playwright


gallery_item = (Path(__file__).parent / "_templates/gallery_item.rst").read_text()
gallery = json.loads((Path(__file__).parent / "_templates/gallery.json").read_text())
src = Path(__file__).parent / "_templates/gallery.rst"
dst = Path(__file__).parent / "user_guide/gallery.rst"
default = Path(__file__).parent / "_static/404.png"
copy(src, dst)


with dst.open("a") as f, sync_playwright() as p:

    for item in gallery:

        item["id"] = item["name"].lower().replace(" ", "_")
        screen = Path(f"_static/gallery/{item['id']}.png")
        if not screen.is_file():

            try:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(item["website"])
                page.screenshot(path=screen)
                browser.close()

            except TimeoutError:
                copy(default, screen)

        f.write(gallery_item.format(**item))

with sync_playwright() as p:

    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://colorlib.com/etc/404/colorlib-error-404-3/")
    page.screenshot(path="404_test.png")

    for item in gallery:

        item["id"] = item["name"].lower().replace(" ", "_")
        screen = Path(f"_static/gallery/{item['id']}.png")
        if not screen.is_file():

            try:
                page.goto(item["website"])
                page.screenshot(path=screen)

            except TimeoutError:
                copy(default, screen)

        f.write(gallery_item.format(**item))
