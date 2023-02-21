"""
A custom Sphinx HTML Translator for Bootstrap layout
"""
from functools import partial
from packaging.version import Version

import sphinx
from sphinx.util import logging
from sphinx.ext.autosummary import autosummary_table
from docutils.nodes import Element

logger = logging.getLogger(__name__)


class BootstrapHTML5TranslatorMixin:
    """
    Mixin HTML Translator for a Bootstrap-ified Sphinx layout.
    Only a couple of functions have been overridden to produce valid HTML to be
    directly styled with Bootstrap, and fulfill acessibility best practices.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.settings.table_style = "table"

    def starttag(self, *args, **kwargs):
        """ensure an aria-level is set for any heading role"""
        if kwargs.get("ROLE") == "heading" and "ARIA-LEVEL" not in kwargs:
            kwargs["ARIA-LEVEL"] = "2"
        return super().starttag(*args, **kwargs)

    def visit_table(self, node):
        """
        copy of sphinx source to *not* add 'docutils' and 'align-default' classes
        but add 'table' class
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

    def visit_section(self, node):
        """Handle section nodes, parsing ``ids`` to replace dots with underscores.

        This will modify the ``id`` of HTML ``<section>`` tags, e.g. where Python modules are documented.
        Replacing dots with underscores allows the tags to be recognized as navigation targets by ScrollSpy.
        """
        if "ids" in node:
            node["ids"] = [id_.replace(".", "_") for id_ in node["ids"]]
        super().visit_section(node)

    def visit_desc_signature(self, node):
        """Handle function & method signature nodes, parsing ``ids`` to replace dots with underscores.

        This will modify the ``id`` attribute of HTML ``<dt>`` & ``<dd>`` tags, where Python functions are documented.
        Replacing dots with underscores allows the tags to be recognized as navigation targets by ScrollSpy.
        """
        if "ids" in node:
            ids = node["ids"]
            for i, id_ in enumerate(ids):
                ids[i] = id_.replace(".", "_")
        super().visit_desc_signature(node)

    def visit_reference(self, node):
        """Handle reference nodes, parsing ``refuri`` and ``anchorname`` attributes to replace dots with underscores.

        This will modify the ``href`` attribute of internal HTML ``<a>`` tags, e.g. the sidebar navigation links.
        """
        try:
            # We are only interested in internal anchor references
            internal, anchorname = node["internal"], node["anchorname"]
            if internal and anchorname.startswith("#") and "." in anchorname:
                # Get the root node of the current document
                document = self.builder.env.get_doctree(self.builder.current_docname)

                # Get the target anchor ID
                target_id = anchorname.lstrip("#")
                sanitized_id = target_id.replace(".", "_")
                # Update the node `href`
                node["refuri"] = node["anchorname"] = "#" + sanitized_id

                # Define a search condition to find the target node by ID
                def find_target(search_id, node):
                    return (
                        isinstance(node, Element)
                        and ("ids" in node)
                        and (search_id in node["ids"])
                    )

                # NOTE: Replacing with underscores creates the possibility for conflicting references
                # We should check for these and warn the user if any are found
                if any(document.traverse(condition=partial(find_target, sanitized_id))):
                    logger.warning(
                        f'Sanitized reference "{sanitized_id}" for "{target_id}" conflicts with an existing reference!'
                    )

                # Find nodes with the given ID (there should only be one)
                targets = document.traverse(condition=partial(find_target, target_id))
                # Replace dots with underscores in the target node ID
                for target in targets:
                    # NOTE: By itself, modifying the target `ids` here seems to be insufficient, however it helps
                    # ensure that the reference `refuri` and target `ids` remain consistent during the build process
                    target["ids"] = [
                        sanitized_id if id_ == target_id else id_
                        for id_ in target["ids"]
                    ]
        except KeyError:
            pass
        super().visit_reference(node)
