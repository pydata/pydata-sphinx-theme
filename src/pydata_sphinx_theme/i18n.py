"""Compile the .mo file at build time."""

from pathlib import Path

from sphinx.application import Sphinx


def compile_translation(app: Sphinx, *args):
    """Compile the .mo file at build time.

    The property app.i18n_catalog_added is added to ensure that the catalog is added only once per run instead of once per HTML file.
    """
    if not app.i18n_catalog_added:
        locale_dir = (Path(__file__).parents[1] / "locale").resolve()
        app.add_message_catalog("messages", str(locale_dir))
        app.i18n_catalog_added = True
