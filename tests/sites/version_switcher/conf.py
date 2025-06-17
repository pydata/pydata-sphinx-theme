"""Test conf file - basic site with version switcher."""

# -- Project information -----------------------------------------------------
project = "PyData Tests"
copyright = "2020, Pydata community"
author = "Pydata community"

root_doc = "index"

# -- General configuration ---------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]

# Add version switcher
html_theme_options = {
    "switcher": {
        "json_url": "_static/switcher.json",
        "version_match": "dev",
    },
    "navbar_start": ["navbar-logo", "version-switcher"],
}

# see https://github.com/sphinx-doc/sphinx/issues/13462
linkcheck_allowed_redirects = {}
