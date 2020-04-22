"""A custom Sphinx HTML Translator for Bootstrap layout
"""
from docutils import nodes

from sphinx.locale import admonitionlabels
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
            name = "admonition"
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

            # Add the "admonition" class to alert_classes so that it can be referenced
            alert_classes[name] = alert_classes[alert_name]

            # Remove the title from this admonition and add it to the admonitionlabels
            # Because this is how Sphinx inserts titles into admonitions
            title = node.children.pop(0)
            admonitionlabels[name] = title.astext()

        if name:
            classes.append("alert-{0}".format(alert_classes[name]))

        # This mimics what Sphinx does in its own `visit_admonition`
        # but wraps in `alert`
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
