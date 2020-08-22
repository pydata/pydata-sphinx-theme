.. _customizing:

*********************
Customizing the theme
*********************

In addition to the configuration options detailed at :ref:`configuration`, it
is also possible to customize the HTML layout and CSS style of the theme.


Customizing the CSS
===================

The theme's CSS can be tweaked in 2 ways. The most straight forward way is to
change the theme variables. If you are looking for more customisation, you can
write your css in ``custom.css``.

Theme variables
---------------

This theme is based on top of the basic
`Bootstrap CSS variables <https://getbootstrap.com/docs/4.0/getting-started/theming/#css-variables>`__
extended with some theme specific variables. An overview of all variables and
every default is defined in ``/pydata_sphinx_theme/static/css/theme.css``.

In order to change a variable, simply update the value in `theme.css`. Just make
sure you keep all defined variables around, with the default value or you theme
value.

Important, the theme is defined with CSS variables, not SASS variables!

### Custom.css

If the theme variables are not sufficient to shape theme to you liking, you can take full control over the look and feel via `/pydata_sphinx_theme/static/css/custom.css`. This stylesheet is loaded last on top of the theme variables and the base styleheet.





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
