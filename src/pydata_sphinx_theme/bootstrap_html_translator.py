"""A custom Sphinx HTML Translator for Bootstrap layout
"""
from packaging.version import Version

import sphinx
from sphinx.writers.html5 import HTML5Translator
from sphinx.util import logging
from sphinx.ext.autosummary import autosummary_table
from docutils import nodes

logger = logging.getLogger(__name__)


class BootstrapHTML5Translator(HTML5Translator):
    """Custom HTML Translator for a Bootstrap-ified Sphinx layout
    This is a specialization of the HTML5 Translator of sphinx.
    Only a couple of functions have been overridden to produce valid HTML to be
    directly styled with Bootstrap, and fulfill acessibility best practices.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.settings.table_style = "table"

    def starttag(self, *args, **kwargs):
        """
        Perform small modification on specific tags:
            - ensure an aria-level is set for any heading role
            - include the pst_atts in the final attributes
            - include the pst_class in the final classes
        """
        # update attributes using pst_atts
        if hasattr(self, "pst_atts"):
            for att, val in self.pst_atts.items():
                kwargs[att] = kwargs.pop(att, val)

        # update classes using pst_class
        if hasattr(self, "pst_class"):
            existing_classes = kwargs.get("CLASS", "").split(" ")
            classes = list(set(existing_classes + self.pst_class))
            kwargs["CLASS"] = " ".join(classes)

        # ensure an aria-level is set for any heading role
        if kwargs.get("ROLE") == "heading" and "ARIA-LEVEL" not in kwargs:
            kwargs["ARIA-LEVEL"] = "2"

        return super().starttag(*args, **kwargs)

    def visit_table(self, node: nodes.Element) -> None:
        """
        copy of sphinx source to *not* add 'docutils' and 'align-default' classes
        but add 'table' class
        """

        # init the attributes
        atts = {}

        # generate_targets_for_table is deprecated in 4.0
        if Version(sphinx.__version__) < Version("4.0"):
            self.generate_targets_for_table(node)

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

    def visit_literal_block(self, node: nodes.Element) -> None:
        """overwrite the literal-block element to make them focusable"""

        # add tabindex to the node
        pst_atts = getattr(node, "pst_atts", {})
        self.pst_atts = {**pst_atts, "tabindex": "0"}

        return super().visit_literal_block(node)
