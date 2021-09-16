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

.. _css-variables:

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
           --pst-font-size-base: 17px;
       }

.. important::

   Note that these are `CSS variables <css-variable-help_>`_ and not
   `SASS variables <https://sass-lang.com/documentation/variables>`_.
   The theme is defined with CSS variables, not SASS variables!

For a complete list of the theme variables that you may override, see the
`theme variables defaults CSS file <pydata-css-variables_>`_:

.. literalinclude:: ../../pydata_sphinx_theme/static/css/theme.css
  :language: CSS


Replacing/Removing Fonts
========================

The theme includes the `FontAwesome 5 Free <https://fontawesome.com/icons?m=free>`__
icon font (the ``.fa, .far, .fas`` styles, which are used for
:ref:`icon links <icon-links>` and admonitions).
This is the only `vendored` font, and otherwise the theme by default relies on
available system fonts for normal body text and headers.

.. Attention::

    Previously-included fonts like `Lato` have been removed, preferring
    the most common default system fonts of the reader's computer. This provides
    both better performance, and better script/glyph coverage than custom fonts,
    and is recommended in most cases.

The default body and header fonts can be changed as follows:

- Using :ref:`custom-css`, you can specify which fonts to use for body, header
  and monospace text. For example, the following can be added to a custom
  css file:

  .. code-block:: none

      :root {
          --pst-font-family-base: Verdana, var(--pst-font-family-base-system);
          --pst-font-family-heading: Cambria, Georgia, Times, var(--pst-font-family-base-system);
          --pst-font-family-monospace: Courier, var(--pst-font-family-monospace-system);
      }

  The ``-system`` variables are available to use as fallback to the default fonts.

- If the font you want to specify in the section above is not generally available
  by default, you will additionally need to ensure the font is loaded.
  For example, you could download and vendor the font in the ``_static`` directory
  of your Sphinx site, and then update the base template to load the font resources:

  - Configure the `template_path <https://www.sphinx-doc.org/en/master/theming.html#templating>`__
    in your ``conf.py``
  - Create a custom ``layout.html`` Jinja2 template which overloads the ``fonts`` block
    (example for loading the Lato font that is included in the ``_static/vendor`` directory):

    .. code-block:: html+jinja

      {% extends "pydata_sphinx_theme/layout.html" %}

      {% block fonts %}
        <!-- add `style` or `link` tags with your CSS `@font-face` declarations here -->
        <!-- ... and optionally preload the `woff2` for snappier page loads -->
        <link rel="stylesheet" href="{{ pathto('_static/vendor/lato_latin-ext/1.44.1/index.css', 1) }}">

      {% endblock %}

    To reduce the `Flash of Unstyled Content`, you may wish to explore various options for
    `preloading content <https://developer.mozilla.org/en-US/docs/Web/HTML/Preloading_content>`__,
    specifically the binary font files. This ensure the files will be loaded
    before waiting for the CSS to be parsed, but should be used with care.

.. _pydata-css-variables: https://github.com/pydata/pydata-sphinx-theme/blob/master/pydata_sphinx_theme/static/css/theme.css
.. _css-variable-help: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

.. meta::
    :description lang=en:
        Advanced customization of pydata-sphinx-theme's HTML and CSS.
