.. _customizing:

*********************
Customizing the theme
*********************

In addition to the configuration options detailed at :ref:`configuration`, it
is also possible to customize the HTML layout and CSS style of the theme.

.. _custom-css:

Custom CSS Stylesheets
======================

You may customize the theme's CSS by creating a custom stylesheet that Sphinx uses to build your site.
Any rules in this style-sheet will over-ride the default theme rules.

To add a custom stylesheet, follow these steps:

1. **Create a CSS stylesheet** in ``_static/css/custom.css``, and add the CSS rules you wish.
2. **Attach the stylesheet to your Sphinx build**. Add the following to ``conf.py``

   .. code-block:: rst

       html_static_path = ['_static']

       html_css_files = [
           'css/custom.css',
       ]

When you build your documentation, this stylesheet should now be activated.

CSS Theme variables
===================

This theme defines several `CSS variables <css-variable-help_>`_ that can be
used to quickly control behavior across your documentation.

These are based on top of the basic `Bootstrap CSS variables <https://getbootstrap.com/docs/4.0/getting-started/theming/#css-variables>`_
extended with some theme specific variables. An overview of all variables and
every default is defined in `the pydata default CSS variables file <pydata-css-variables_>`_.

In order to change a variable, follow these steps:

1. :ref:`Add a custom CSS stylesheet <custom-css>`. This is where we'll configure the variables.
2. Underneath a ``:root`` section, add the variables you wish to update. For example, to update
   the base font size, you might add this to ``custom.css``:
  
   .. code-block:: none

       :root {
           --font-size-base: 17px;
       }

For a complete list of the theme variables that you may override, see the
`theme variables defaults CSS file <pydata-css-variables_>`_.

.. important::

   Note that these are `CSS variables <css-variable-help_>`_ and not
   `SASS variables <https://sass-lang.com/documentation/variables>`_.
   For the difference between the two, see he theme is defined with CSS variables,
   not SASS variables!


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

.. _pydata-css-variables: https://github.com/pandas-dev/pydata-sphinx-theme/blob/master/pydata_sphinx_theme/static/css/theme.css
.. _css-variable-help: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties 