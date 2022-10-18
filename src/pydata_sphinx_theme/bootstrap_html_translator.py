"""A custom Sphinx HTML Translator for Bootstrap layout
"""
from sphinx.writers.html5 import HTML5Translator
from sphinx.util import logging

logger = logging.getLogger(__name__)


class BootstrapHTML5Translator(HTML5Translator):
    """Custom HTML Translator for a Bootstrap-ified Sphinx layout
    This is a specialization of the HTML5 Translator of sphinx.
    Only a couple of functions have been overridden to produce valid HTML to be
    directly styled with Bootstrap, and fulfill acessibility best practices.
    """

    def starttag(self, *args, **kwargs):
        """ensure an aria-level is set for any heading role"""
        if kwargs.get("ROLE") == "heading" and "ARIA-LEVEL" not in kwargs:
            kwargs["ARIA-LEVEL"] = "2"
        return super().starttag(*args, **kwargs)
