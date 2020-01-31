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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Pandas Sphinx Theme'
copyright = '2019, PyData Community'
author = 'PyData Community'

# The full version, including alpha/beta/rc tags
release = '0.0.1dev0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'numpydoc',
    'recommonmark'
]

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pandas_sphinx_theme'
html_logo = '_static/pandas.svg'

html_theme_options = {
    "external_links": [
        {
            'url': "https://pandas.pydata.org/pandas-docs/stable/",
            "name": "Pandas Docs"
        }
    ],
    "github_url": "https://github.com/pandas-dev/pandas-sphinx-theme",
    "twitter_url": "https://twitter.com/pandas_dev",
    "use_edit_page_button": True
}

html_context = {
    "github_user": "pandas-dev",
    "github_repo": "pandas-sphinx-theme",
    "github_version": "master",
    "doc_path": "docs",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Auto-convert markdown pages to demo --------------------------------------
import recommonmark
from recommonmark.transform import AutoStructify

def setup(app):
    app.add_transform(AutoStructify)
