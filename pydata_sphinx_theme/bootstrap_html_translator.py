"""A custom Sphinx HTML Translator for Bootstrap layout
"""
import sys
import re

from docutils import nodes

from sphinx.locale import admonitionlabels, _
from sphinx.writers.html5 import HTML5Translator
from sphinx.util import logging

logger = logging.getLogger(__name__)


# Mapping of admonition classes to Bootstrap contextual classes
alert_classes = {
    "attention": "primary",
    "caution": "warning",
    "danger": "danger",
    "error": "danger",
    "hint": "info",
    "important": "primary",
    "note": "info",
    "seealso": "info",
    "tip": "primary",
    "warning": "warning",
    "todo": "info",
    "example": "info",
}


class BootstrapHTML5Translator(HTML5Translator):
    """Custom HTML Translator for a Bootstrap-ified Sphinx layout

    This is a specialization of the HTML5 Translator of sphinx.
    Only a couple of functions have been overridden to produce valid HTML to be
    directly styled with Bootstrap.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.settings.table_style = "table"

    def visit_admonition(self, node, name=""):
        # type: (nodes.Element, str) -> None
        # copy of sphinx source to add alert classes
        classes = ["alert"]

        # If we have a generic admonition block, style it as info
        if (
            any("admonition-" in iclass for iclass in node.attributes["classes"])
            and name == ""
        ):
            if node.attributes.get("names"):
                class_name = node.attributes.get("names")[0]
            else:
                class_name = alert_classes["note"]
            if class_name not in alert_classes:
                logger.warning(
                    f"Admonition name `{name}` is not supported. Defaulting to `note`."
                )
                class_name = alert_classes["note"]

            # Update altert_classes to use the proper class
            name = "admonition"
            alert_classes[name] = class_name

            # This removes the title and makes it behave like a "normal" admonition block
            title = node.children.pop(0)
            admonitionlabels[name] = title.astext()

        if name:
            classes.append("alert-{0}".format(alert_classes[name]))

        self.body.append(self.starttag(node, "div", CLASS=" ".join(classes)))
        if name:
            node.insert(0, nodes.title(name, admonitionlabels[name]))

    def visit_table(self, node):
        # type: (nodes.Element) -> None
        # copy of sphinx source to *not* add 'docutils' and 'align-default' classes
        # but add 'table' class
        self.generate_targets_for_table(node)

        self._table_row_index = 0

        classes = [cls.strip(" \t\n") for cls in self.settings.table_style.split(",")]
        # classes.insert(0, "docutils")  # compat
        # if 'align' in node:
        #     classes.append('align-%s' % node['align'])
        tag = self.starttag(node, "table", CLASS=" ".join(classes))
        self.body.append(tag)
