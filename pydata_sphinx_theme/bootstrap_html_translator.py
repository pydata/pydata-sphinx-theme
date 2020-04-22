"""A custom Sphinx HTML Translator for Bootstrap layout
"""
from docutils import nodes

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
        """Allows admonition blocks to have a `names` attribute to style them."""
        # We'll always wrap admonitions in `alert` classes to behave like the alerts
        classes = ["alert"]

        # If `name` is given, then the alert directive was called, not admonition
        if name:
            alert_name = name
        else:
            if node.attributes.get("names"):
                # If `name` is specified, try to look it up in the list of alerts
                alert_name = node.attributes.get("names")[0]
            else:
                # If no `name` is specified, style it as `note`
                alert_name = "note"

            if alert_name not in alert_classes:
                logger.warning(
                    f"Unsupported admonition name: `{alert_name}`. Using style `note`.",
                    location=(self.docnames[0], node.children[0].line),
                )
                alert_name = "note"

        # Find the proper class name and add it to a wrapper div for this admonition
        classes.append("alert-{}".format(alert_classes[alert_name]))

        self.body.append(self.starttag(node, "div", CLASS=" ".join(classes)))

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
