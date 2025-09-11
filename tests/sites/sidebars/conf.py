"""Test conf file."""

# -- Project information -----------------------------------------------------

project = "PyData Tests"
copyright = "2020, Pydata community"
author = "Pydata community"

root_doc = "index"

# -- General configuration ---------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_sidebars = {
    "section2/no-sidebar": [],  # Turn off primary/left sidebar
}

# see https://github.com/sphinx-doc/sphinx/issues/13462
linkcheck_allowed_redirects = {}
