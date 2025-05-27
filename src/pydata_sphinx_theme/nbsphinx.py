"""Interoperate with nbpshinx extension."""

from pathlib import Path

from sphinx.application import Sphinx

from . import utils


# This function will allow us to catch during development or CI if nbsphinx ever
# changes the name of the CSS file where it outputs its notebook styles.
def delete_nbsphinx_css(app: Sphinx) -> None:
    """For projects using nbsphinx, delete nbsphinx's CSS.
    We replace it later with our own.
    """
    if "nbsphinx" not in app.config.extensions:
        return

    nbsphinx_css = Path(app.builder.outdir) / "_static" / "nbsphinx-code-cells.css"
    assert nbsphinx_css.exists()
    nbsphinx_css.unlink()


def point_nbsphinx_pages_to_our_css(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """For projects using nbsphinx, point to our notebook CSS.
    nbsphinx selectively adds its CSS to certain pages (the ones it converted
    from notebook files) by calling the Sphinx `add_css_file()` method on
    "html-page-context" event. Here we update those pages to point to our
    alternative CSS file.
    """
    if "nbsphinx" not in app.config.extensions:
        return

    if "css_files" not in context:
        return

    nbsphinx_css = "_static/nbsphinx-code-cells.css"
    found = utils._delete_from_css_files(context["css_files"], nbsphinx_css)
    if found:
        app.add_css_file("styles/nbsphinx-pydata-theme.css")
