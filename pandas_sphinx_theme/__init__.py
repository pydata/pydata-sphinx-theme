"""
Sphinx Bootstrap theme.

Adapted for the pandas documentation.
"""
import os

from .bootstrap_html_translator import BootstrapHTML5Translator


__version__ = "0.0.1.dev0"


def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = os.path.abspath(os.path.dirname(__file__))
    return [theme_path]


def setup(app):
    theme_path = get_html_theme_path()[0]
    app.add_html_theme("pandas_sphinx_theme", theme_path)
    app.set_translator("html", BootstrapHTML5Translator)
