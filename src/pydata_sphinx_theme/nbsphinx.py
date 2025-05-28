"""Interoperate with nbpshinx extension."""

from pathlib import Path

from sphinx.application import Sphinx

from . import utils


nbsphinx_css_filename = "nbsphinx-code-cells.css"
replacement_css_filename = "nbsphinx-pydata-theme.css"


def delete_nbsphinx_css(app: Sphinx) -> None:
    """For projects using nbsphinx, delete nbsphinx's CSS.
    We replace it later with our own.
    """
    if "nbsphinx" not in app.config.extensions:
        return

    nbsphinx_css = Path(app.builder.outdir) / "_static" / nbsphinx_css_filename
    if nbsphinx_css.exists():
        nbsphinx_css.unlink()
    else:
        # Here is the main purpose of this function. The main purpose is not so
        # much to delete the nbsphinx CSS file (despite this function's name) as
        # to help us catch a breaking change on nbsphinx's side if they ever
        # rename or move its CSS file. This is important because the other
        # function in this file, which gets executed later in the build process,
        # also depends on nbsphinx's CSS being at a particular path. If not it's
        # not there, then without this warning the CSS replacement mechanism
        # would fail silently, and projects using this theme would load
        # nbsphinx's notebook styles instead of this theme's.
        utils.maybe_warn(
            app, f"nbpshinx CSS not found in expected place: {nbsphinx_css}"
        )


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

    nbsphinx_css = "_static/" + nbsphinx_css_filename
    found = utils._delete_from_css_files(context["css_files"], nbsphinx_css)
    if found:
        app.add_css_file("styles/" + replacement_css_filename)
