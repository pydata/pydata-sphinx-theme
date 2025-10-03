"""Interoperate with Myst-NB Sphinx extension."""

import hashlib

from importlib import resources
from pathlib import Path

from sphinx.application import Sphinx

from . import utils


replacement_css_filename = "myst-nb-pydata-theme.css"


def myst_nb_css_filename():
    """For projects using MyST-NB, get the name of MyST-NB's CSS file."""
    # Local import because not every project installs myst_nb
    from myst_nb import static

    with resources.as_file(resources.files(static).joinpath("mystnb.css")) as path:
        hash = hashlib.sha256(path.read_bytes()).hexdigest()
        return f"mystnb.{hash}.css"


def delete_myst_nb_css(app: Sphinx) -> None:
    """For projects using Myst-NB, delete MyST-NB's CSS.
    We replace it later with our own.
    """
    if "myst_nb" not in app.config.extensions:
        return

    myst_nb_css = Path(app.builder.outdir) / "_static" / myst_nb_css_filename()
    if myst_nb_css.exists():
        myst_nb_css.unlink()
    else:
        # Here is the main purpose of this function. The main purpose is not so
        # much to delete the MyST-NB CSS file (despite this function's name) as
        # to help us catch a breaking change on MyST-NB's side if they ever
        # rename or move its CSS file. This is important because the other
        # function in this file, which gets executed later in the build process,
        # also depends on MyST-NB's CSS being at a particular path. If it's not
        # there, then without this warning the CSS replacement would fail
        # silently, and projects using this theme would load MyST-NB's notebook
        # styles instead of this theme's.
        utils.maybe_warn(app, f"MyST-NB CSS not found in expected place: {myst_nb_css}")


def point_myst_nb_pages_to_our_css(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """For projects using MyST-NB, point to our notebook CSS."""
    if "myst_nb" not in app.config.extensions:
        return

    if "css_files" not in context:
        return

    myst_nb_css = "_static/" + myst_nb_css_filename()
    found = utils._delete_from_css_files(context["css_files"], myst_nb_css)
    if found:
        app.add_css_file("styles/" + replacement_css_filename)
