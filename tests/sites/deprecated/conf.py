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
html_logo = "emptylogo.png"
html_copy_source = True
html_sourcelink_suffix = ""

# Base options, we can add other key/vals later
html_theme_options = {
    "search_bar_position": "navbar",
    "logo_text": "DOCS",
    "page_sidebar_items": [
        "page-toc.html",
        "edit-this-page.html",
        "sourcelink.html",
    ],
    "footer_items": ["page-toc.html"],
}

html_sidebars = {"section1/index": ["sidebar-nav-bs.html"]}
