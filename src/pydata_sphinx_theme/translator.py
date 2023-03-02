"""
A custom Sphinx HTML Translator for Bootstrap layout
"""
from packaging.version import Version

import sphinx
from sphinx.util import logging
from sphinx.ext.autosummary import autosummary_table

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
