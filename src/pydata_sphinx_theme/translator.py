"""A custom Sphinx HTML Translator for Bootstrap layout."""

import types
from functools import partial

import sphinx
from docutils.nodes import Element
from packaging.version import Version
from sphinx.application import Sphinx
from sphinx.ext.autosummary import autosummary_table
from sphinx.util import logging

from .utils import traverse_or_findall

logger = logging.getLogger(__name__)


class BootstrapHTML5TranslatorMixin:
    """Mixin HTML Translator for a Bootstrap-ified Sphinx layout.

    Only a couple of functions have been overridden to produce valid HTML to be
    directly styled with Bootstrap, and fulfill acessibility best practices.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.settings.table_style = "table"

    def starttag(self, *args, **kwargs):
        """Ensure an aria-level is set for any heading role."""
        if kwargs.get("ROLE") == "heading" and "ARIA-LEVEL" not in kwargs:
            kwargs["ARIA-LEVEL"] = "2"
        return super().starttag(*args, **kwargs)

    def visit_table(self, node):
        """Custom visit table method.

        Copy of sphinx source to *not* add 'docutils' and 'align-default' classes but add 'table' class.
        """
        # init the attributes
        atts = {}

        if Version(sphinx.__version__) < Version("4.3"):
            self._table_row_index = 0
        else:
            self._table_row_indices.append(0)

        # get the classes
        classes = [cls.strip(" \t\n") for cls in self.settings.table_style.split(",")]

        # we're looking at the 'real_table', which is wrapped by an autosummary
        if isinstance(node.parent, autosummary_table):
            classes += ["autosummary"]

        # add the width if set in a style attribute
        if "width" in node:
            atts["style"] = f'width: {node["width"]}'

        # add specific class if align is set
        if "align" in node:
            classes.append(f'table-{node["align"]}')

        tag = self.starttag(node, "table", CLASS=" ".join(classes), **atts)
        self.body.append(tag)

    # NOTE: `visit_section`, `visit_desc_signature` & `visit_reference` are extended
    # here to resolve #1026 & #1207. There is an open issue with Sphinx to address this:
    # https://github.com/sphinx-doc/sphinx/issues/11208
    # If the issue is resolved within Sphinx, these methods can be removed.

    def visit_section(self, node):
        """Handle section nodes to replace dots with underscores.

        This will modify the ``id`` of HTML ``<section>`` tags, where Python modules
        are documented. Replacing dots with underscores allows the tags to be recognized
        as navigation targets by ScrollSpy.
        """
        if "ids" in node:
            node["ids"] = [id_.replace(".", "_") for id_ in node["ids"]]
        super().visit_section(node)

    def visit_desc_signature(self, node):
        """Handle function & method signature nodes to replace dots with underscores.

        This will modify the ``id`` attribute of HTML ``<dt>`` & ``<dd>`` tags, where
        Python functions are documented. Replacing dots with underscores allows the tags
        to be recognized as navigation targets by ScrollSpy.
        """
        if "ids" in node:
            ids = node["ids"]
            for i, id_ in enumerate(ids):
                ids[i] = id_.replace(".", "_")
        super().visit_desc_signature(node)

    def visit_reference(self, node):
        """Handle reference nodes to replace dots with underscores.

        This will modify the ``href`` attribute of any internal HTML ``<a>`` tags, e.g.
        the sidebar navigation links.
        """
        try:
            # We are only interested in internal anchor references
            internal, refid = node["internal"], node["refuri"]
            if internal and refid.startswith("#") and "." in refid:
                # Get the root node of the current document
                document = self.builder.env.get_doctree(self.builder.current_docname)

                # Get the target anchor ID
                first,target_id = refid.split("#")
                sanitized_id = target_id.replace(".", "_")
                # Update the node `href`
                node["refuri"] = first + "#" + sanitized_id

                # Define a search condition to find the target node by ID
                def find_target(search_id, node):
                    return (
                        isinstance(node, Element)
                        and ("ids" in node)
                        and (search_id in node["ids"])
                    )

                # NOTE: Replacing with underscores creates the possibility for
                # conflicting references. Here we check for these and warn the
                # user if any are found.
                if any(
                    traverse_or_findall(
                        document, condition=partial(find_target, sanitized_id)
                    )
                ):
                    logger.warning(
                        f'Sanitized reference "{sanitized_id}" for "{target_id}" '
                        "conflicts with an existing reference!"
                    )

                # Find nodes with the given ID (there should only be one)
                targets = traverse_or_findall(
                    document, condition=partial(find_target, target_id)
                )
                # Replace dots with underscores in the target node ID
                for target in targets:
                    # NOTE: By itself, modifying the target `ids` here seems to be
                    # insufficient, however it helps ensure that the reference `refuri`
                    # and target `ids` remain consistent during the build process
                    target["ids"] = [
                        sanitized_id if id_ == target_id else id_
                        for id_ in target["ids"]
                    ]
        except KeyError:
            pass
            
        try:
            refid = node["refid"]
            if "." in refid:
                # Get the root node of the current document
                document = self.builder.env.get_doctree(self.builder.current_docname)

                # Get the target anchor ID
                target_id = refid
                sanitized_id = target_id.replace(".", "_")
                # Update the node `href`
                node["refuri"] = "#" + sanitized_id

                # Define a search condition to find the target node by ID
                def find_target(search_id, node):
                    return (
                        isinstance(node, Element)
                        and ("ids" in node)
                        and (search_id in node["ids"])
                    )

                # NOTE: Replacing with underscores creates the possibility for
                # conflicting references. We should check for these and warn the
                # user if any are found.
                if any(document.traverse(condition=partial(find_target, sanitized_id))):
                    logger.warning(
                        f'Sanitized reference "{sanitized_id}" for "{target_id}" '
                        "conflicts with an existing reference!"
                    )

                # Find nodes with the given ID (there should only be one)
                targets = document.traverse(condition=partial(find_target, target_id))
                # Replace dots with underscores in the target node ID
                for target in targets:
                    # NOTE: By itself, modifying the target `ids` here seems to be
                    # insufficient, however it helps ensure that the reference `refuri`
                    # and target `ids` remain consistent during the build process
                    target["ids"] = [
                        sanitized_id if id_ == target_id else id_
                        for id_ in target["ids"]
                    ]
        
        except KeyError:
            pass
        
        try:
            refid = node["refuri"]
            if "." in refid:
                # Get the root node of the current document
                document = self.builder.env.get_doctree(self.builder.current_docname)

                # Get the target anchor ID
                parts = refid.split("#")
                if len(parts)>1:
                    first = parts[0]
                    target_id = parts[1]
                else:
                    first = ""
                    target_id = parts[0]
                sanitized_id = target_id.replace(".", "_")
                # Update the node `href`
                node["refuri"] = first + "#" + sanitized_id

                # Define a search condition to find the target node by ID
                def find_target(search_id, node):
                    return (
                        isinstance(node, Element)
                        and ("ids" in node)
                        and (search_id in node["ids"])
                    )

                # NOTE: Replacing with underscores creates the possibility for
                # conflicting references. We should check for these and warn the
                # user if any are found.
                if any(document.traverse(condition=partial(find_target, sanitized_id))):
                    logger.warning(
                        f'Sanitized reference "{sanitized_id}" for "{target_id}" '
                        "conflicts with an existing reference!"
                    )

                # Find nodes with the given ID (there should only be one)
                targets = document.traverse(condition=partial(find_target, target_id))
                # Replace dots with underscores in the target node ID
                for target in targets:
                    # NOTE: By itself, modifying the target `ids` here seems to be
                    # insufficient, however it helps ensure that the reference `refuri`
                    # and target `ids` remain consistent during the build process
                    target["ids"] = [
                        sanitized_id if id_ == target_id else id_
                        for id_ in target["ids"]
                    ]
        
        except KeyError:
            pass
        
        super().visit_reference(node)


def setup_translators(app: Sphinx):
    """Add bootstrap HTML functionality if we are using an HTML translator.

    This re-uses the pre-existing Sphinx translator and adds extra functionality defined
    in ``BootstrapHTML5TranslatorMixin``. This way we can retain the original translator's
    behavior and configuration, and _only_ add the extra bootstrap rules.
    If we don't detect an HTML-based translator, then we do nothing.
    """
    if not app.registry.translators.items():
        translator = types.new_class(
            "BootstrapHTML5Translator",
            (
                BootstrapHTML5TranslatorMixin,
                app.builder.default_translator_class,
            ),
            {},
        )
        app.set_translator(app.builder.name, translator, override=True)
    else:
        for name, klass in app.registry.translators.items():
            if app.builder.format != "html":
                # Skip translators that are not HTML
                continue

            translator = types.new_class(
                "BootstrapHTML5Translator",
                (
                    BootstrapHTML5TranslatorMixin,
                    klass,
                ),
                {},
            )
            app.set_translator(name, translator, override=True)
