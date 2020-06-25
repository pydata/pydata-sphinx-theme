.. _customizing:

**********************
Customizing the layout
**********************

In addition to the configuration options detailed at :ref:`configuration`, it
is also possible to customize the HTML layout and CSS style of the theme.


Replacing/Removing Fonts
========================

The theme contains custom web fonts, in several formats, for different purposes:

- "normal" body text, on ``body``
- page and section headers, on ``.header-style``
- icons, on ``.fa, .far, .fas``

While altering the icon font is presently somewhat involved, the body and header fonts,
often paired together, can be replaced (or removed altogether) by:

- configuring `template_path <https://www.sphinx-doc.org/en/master/theming.html#templating>`__
  in your ``conf.py``
- creating a custom ``layout.html`` Jinja2 template which overloads the ``fonts`` block

.. code-block:: html+jinja

    {% extends "pydata_sphinx_theme/layout.html" %}

    {% block fonts %}
        <!-- add `style` or `link` tags with your CSS `@font-face` declarations here -->
        <!-- ... and a `style` tag with setting `font-family` in `body` and `.header-style` -->
        <!-- ... and optionally preload the `woff2` for snappier page loads -->
        <!-- or add a `style` tag with a font fallback chain with good cross-platform coverage -->
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            }
            .header-style {
                font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
            }
        </style>
    {% endblock %}
