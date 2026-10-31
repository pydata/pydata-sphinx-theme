"""Test conf file."""

# -- Project information -----------------------------------------------------

project = "PyData Table Tests"
copyright = "2026, Pydata community"
author = "Pydata community"

root_doc = "index"

# -- General configuration ---------------------------------------------------

html_theme = "pydata_sphinx_theme"


def setup(app):
    """Register a translator for a builder we do not use.

    Some extensions register translators for their own builders; this must not
    prevent the theme from installing its translator for the builder we are
    actually building with.  See
    https://github.com/pydata/pydata-sphinx-theme/issues/1418
    """
    from docutils import nodes

    app.set_translator("other-extension-builder", nodes.NodeVisitor)
