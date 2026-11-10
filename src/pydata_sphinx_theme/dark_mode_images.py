"""Automatically show a dark mode variant of local images, if there is one."""

from pathlib import PurePosixPath

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.transforms.post_transforms import SphinxPostTransform

from .utils import get_theme_options_dict


THEMED_CLASSES = {"only-light", "only-dark", "dark-light"}


def _get_suffix(app: Sphinx) -> str:
    """Return the ``dark_mode_image_suffix`` theme option, empty if disabled."""
    # Non-HTML builders (e.g. sphinx-build -b gettext, MessageCatalogBuilder)
    # have no theme
    if not hasattr(app.builder, "theme"):
        return ""
    theme_conf_options = app.builder.theme.get_options()
    theme_options = theme_conf_options | get_theme_options_dict(app)
    return theme_options.get("dark_mode_image_suffix") or ""


def _get_dark_uri(env: BuildEnvironment, image: nodes.image, suffix: str) -> str | None:
    """Return the dark variant of a local image, relative to the source dir.

    ``None`` is returned if the image is remote, uses a wildcard extension, already
    is a dark variant or if the dark variant does not exist.
    """
    # set by the image collector, "*" means a single local file
    uri = image.get("candidates", {}).get("*")
    if uri is None:
        return None
    path = PurePosixPath(uri)
    if path.stem.endswith(suffix):
        return None
    dark_uri = str(path.with_stem(f"{path.stem}{suffix}"))
    if not (env.srcdir / dark_uri).is_file():
        return None
    return dark_uri


def _themed_root(image: nodes.image) -> nodes.Element | None:
    """Return the image with its enclosing link and figure, unless already themed."""
    node = image
    # links and figures can only hold one image, so they are duplicated with it
    while isinstance(node.parent, nodes.reference | nodes.figure):
        node = node.parent
    if THEMED_CLASSES & {*image["classes"], *node["classes"]}:
        return None
    return node


def note_dark_image_dependencies(app: Sphinx, doctree: nodes.document) -> None:
    """Rebuild a page when the dark variant of one of its images changes."""
    suffix = _get_suffix(app)
    for image in doctree.findall(nodes.image):
        if _themed_root(image) is None:
            continue
        if dark_uri := _get_dark_uri(app.env, image, suffix):
            app.env.note_dependency(dark_uri)


class DarkModeImageTransform(SphinxPostTransform):
    """Show ``name<suffix>.ext`` instead of ``name.ext`` in dark mode, if it exists.

    Each such image (with its link and figure, if any) is followed by a copy pointing
    to the dark file, and the two are tagged with the ``only-light`` / ``only-dark``
    classes. Images that already have one of these classes or ``dark-light`` are left
    alone.

    A labelled image or figure (e.g. with ``:name:``) is wrapped in a container that
    takes over its ids, so that links to it have a visible target in both modes. Both
    copies get derived ids and share the figure number of the original.

    This runs after the references are resolved, so that Sphinx takes the link text
    and figure number from the original node.
    """

    default_priority = 400
    formats = ("html",)
    #: the ``dark_mode_image_suffix`` theme option, set in setup_dark_mode_images
    suffix: str

    def run(self, **kwargs) -> None:
        """Run the transform."""
        suffix = self.suffix
        for image in list(self.document.findall(nodes.image)):
            node = _themed_root(image)
            if node is None:
                continue
            dark_uri = _get_dark_uri(self.env, image, suffix)
            if dark_uri is None:
                continue
            docname = self._get_docname(node)
            # register the file so that the builder copies it to the output
            self.env.images.add_file(docname, dark_uri)

            dark = node.deepcopy()
            dark_image = next(iter(dark.findall(nodes.image)))
            dark_image["uri"] = dark_uri
            dark_image["candidates"] = {"*": dark_uri}
            dark_image.attributes.pop("original_uri", None)
            # the copy must not repeat the ids of the light version
            for child in dark.findall(nodes.Element, include_self=False):
                child["ids"] = []
            # the theme styles img elements by class, so tag the wrappers and the image
            for light_node, dark_node in {(node, dark), (image, dark_image)}:
                light_node["classes"].append("only-light")
                dark_node["classes"].append("only-dark")

            ids = node["ids"]
            if not ids:
                node.parent.insert(node.parent.index(node) + 1, dark)
                continue
            wrapper = nodes.container(ids=ids, classes=["dark-mode-image"])
            node.parent.replace(node, wrapper)
            wrapper += [node, dark]
            node["ids"] = [f"{id_}-light" for id_ in ids]
            dark["ids"] = [f"{id_}-dark" for id_ in ids]
            for numbers in self.env.toc_fignumbers.get(docname, {}).values():
                if ids[0] in numbers:
                    numbers[node["ids"][0]] = numbers[dark["ids"][0]] = numbers[ids[0]]

    def _get_docname(self, node: nodes.Element) -> str:
        """Return the document of a node, also in the singlehtml builder."""
        ancestor = node.parent
        while ancestor is not None:
            if isinstance(ancestor, addnodes.start_of_file):
                return ancestor["docname"]
            ancestor = ancestor.parent
        return self.env.current_document.docname


def setup_dark_mode_images(app: Sphinx) -> None:
    """Enable the dark mode images if ``dark_mode_image_suffix`` is set."""
    if suffix := _get_suffix(app):
        # after the image collector made the image uris relative to the source dir
        app.connect("doctree-read", note_dark_image_dependencies, priority=600)
        attrs = {"suffix": suffix}
        app.add_post_transform(
            type("DarkModeImageTransform", (DarkModeImageTransform,), attrs)
        )
