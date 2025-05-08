"""Test conf file."""

# -- Project information -----------------------------------------------------

project = "PyData Tests"
copyright = "2020, Pydata community"
author = "Pydata community"

root_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []
html_theme = "pydata_sphinx_theme"
html_logo = "_static/emptylogo.png"
html_copy_source = True
html_sourcelink_suffix = ""

# Base options, we can add other key/vals later
html_sidebars = {"section1/index": ["sidebar-nav-bs.html"]}

html_theme_options = {
    "footer_start": ["breadcrumbs"],
    "footer_center": ["breadcrumbs"],
    "footer_end": ["breadcrumbs"],
    "primary_sidebar_end": ["breadcrumbs"],
    "secondary_sidebar_items": ["breadcrumbs"],
    "article_header_start": ["breadcrumbs"],
}

# see https://github.com/sphinx-doc/sphinx/issues/13462
linkcheck_allowed_redirects = {}
