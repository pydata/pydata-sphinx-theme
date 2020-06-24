.. _customizing:

**********************
Customizing the layout
**********************

In addition to the configuration options detailed at :ref:`configuration`, it
is also possible to customize the HTML layout and CSS style of the theme.


Replacing/Removing Fonts
========================

The theme contains custom web fonts, in several formats, for different purposes:

- "normal" body text
- page and section headers
- icons

While altering the icon font is not presently feasible, the body and header fonts,
often paired together, can be replaced (or removed altogether) by creating a
custom ``layout.html`` in your `template_path <https://www.sphinx-doc.org/en/master/theming.html#templating>`__:

.. code-block:: html+jinja

    {% extends "pydata_sphinx_theme/layout.html" %}

    {% block fonts %}
        <!-- insert link tags to your font CSS here -->
        <!-- ... and optionally preload the woff2 for snappier page loads -->
        <!-- ... or just specify a font fallback chain with a style tag -->
    {% endblock %}
