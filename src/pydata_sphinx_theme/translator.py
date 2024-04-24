"""A custom Sphinx HTML Translator for Bootstrap layout."""

import types

import sphinx
from docutils import nodes
from packaging.version import Version
from sphinx.application import Sphinx
from sphinx.ext.autosummary import autosummary_table
from sphinx.util import logging

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
        """Perform small modifications to tags.

        - ensure aria-level is set for any tag with heading role
        - ensure <pre> tags have tabindex="0".
        """
        if kwargs.get("ROLE") == "heading" and "ARIA-LEVEL" not in kwargs:
            kwargs["ARIA-LEVEL"] = "2"

        if "pre" in args:
            kwargs["data-tabindex"] = "0"

        return super().starttag(*args, **kwargs)

    def visit_literal_block(self, node):
        """Modify literal blocks.

        - add tabindex="0" to <pre> tags within the HTML tree of the literal
          block
        """
        try:
            super().visit_literal_block(node)
        except nodes.SkipNode:
            # If the super method raises nodes.SkipNode, then we know it
            # executed successfully and appended to self.body a string of HTML
            # representing the code block, which we then modify.
            html_string = self.body[-1]
            self.body[-1] = html_string.replace("<pre", '<pre data-tabindex="0"')
            raise nodes.SkipNode

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

    def visit_sidebar(self, node):
        """r/aside/div copy of Docutils html5 writer method.

        Link to original: https://github.com/docutils/docutils/blob/ff0b419256d6b7bfdd4363dd078c2255701de605/docutils/docutils/writers/html5_polyglot/__init__.py#L350
        """
        self.body.append(self.starttag(node, "div", CLASS="sidebar"))
        self.in_sidebar = True

    def depart_sidebar(self, node):
        """r/aside/div copy of Docutils html5 writer method.

        Link to original: https://github.com/docutils/docutils/blob/ff0b419256d6b7bfdd4363dd078c2255701de605/docutils/docutils/writers/html5_polyglot/__init__.py#L355
        """
        self.body.append("</div>\n")
        self.in_sidebar = False

    def visit_footnote(self, node) -> None:
        """r/aside/div copy of Sphinx-patched Docutils html5 writer method.

        Link to original: https://github.com/sphinx-doc/sphinx/blob/9ebc46a74fa766460c450bd60cdef46b98492939/sphinx/util/docutils.py#L185
        """
        label_style = self.settings.footnote_references
        if not isinstance(node.previous_sibling(), type(node)):  # type: ignore[attr-defined]
            self.body.append(f'<div class="footnote-list {label_style}">\n')
        self.body.append(
            self.starttag(node, "div", classes=[node.tagname, label_style], role="note")
        )

    def depart_footnote(self, node) -> None:
        """r/aside/div copy of Docutils html5 writer method.

        Link to original: https://github.com/sphinx-doc/sphinx/blob/9ebc46a74fa766460c450bd60cdef46b98492939/sphinx/util/docutils.py#L193
        """
        self.body.append("</div>\n")
        if not isinstance(node.next_node(descend=False, siblings=True), type(node)):
            self.body.append("</div>\n")


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
