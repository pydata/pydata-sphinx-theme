.. _customizing:

*********************
Customizing the theme
*********************

In addition to the configuration options detailed at :ref:`configuration`, it
is also possible to customize the HTML layout and CSS style of the theme.

.. danger::

    This theme is still under active development, and we make no promises
    about the stability of any specific HTML structure, CSS variables, etc.
    Make these customizations at your own risk, and pin versions if you're
    worried about breaking changes!

.. _custom-css:

Custom CSS Stylesheets
======================

You may customize the theme's CSS by creating a custom stylesheet that Sphinx uses to build your site.
Any rules in this style-sheet will over-ride the default theme rules.

To add a custom stylesheet, follow these steps:

1. **Create a CSS stylesheet** in ``_static/css/custom.css``, and add the CSS rules you wish.
2. **Attach the stylesheet to your Sphinx build**. Add the following to ``conf.py``

   .. code-block:: python

       html_static_path = ['_static']

       html_css_files = [
           'css/custom.css',
       ]

When you build your documentation, this stylesheet should now be activated.

.. _manage-themes:

Manage light and dark themes
============================

You can change the major background / foreground colors of this theme according to "dark" and "light" modes.
These are controlled by a button in the navigation header, with the following options:

- A ``light`` theme with a bright background and dark text / UI elements
- A ``dark`` theme with a dark background and light text / UI elements
- ``auto``: the documentation theme will follow the system default that you have set

Customize the CSS of light and dark themes
------------------------------------------

.. danger::

    Theming is still a beta feature so the variables related to the theme switch are likely to change in the future. No backward compatibily is guaranteed when customization is done.


To customize the CSS of page elements in a theme-dependent manner, use the ``html[data-theme='<THEME>']`` CSS selector.
For example to define a different background color for both the light and dark themes:

.. code-block:: css

    /* anything related to the light theme */
    html[data-theme="light"] {

        /* whatever you want to change */
        background: white;
    }

    /* anything related to the dark theme */
    html[data-theme="dark"] {

        /* whatever you want to change */
        background: black;
    }

A complete list of the used colors for this theme can be found in the `pydata default css colors file <pydata-css-colors_>`__.

Use theme-dependent content
---------------------------

It is possible to use different content for light and dark mode, so that the content only shows up when a particular theme is active.
This is useful if your content depends on the theme's style, such as a PNG image with a light or a dark background.

There are **two CSS helper classes** to specify items on the page as theme-specific.
These are:

- :code:`only-dark`: Only display an element when the dark theme is active.
- :code:`only-light` Only display an element when the light theme is active.

For example, the following page content defines two images, each of which uses a different one of the classes above.
Change the theme and a new image should be displayed.

.. code-block:: rst

    .. image:: https://source.unsplash.com/200x200/daily?cute+cat
        :class: only-dark

    .. image:: https://source.unsplash.com/200x200/daily?cute+dog
        :class: only-light

.. image:: https://source.unsplash.com/200x200/daily?cute+cat
    :class: only-dark

.. image:: https://source.unsplash.com/200x200/daily?cute+dog
    :class: only-light

Define custom JavaScript to react to theme changes
--------------------------------------------------

You can define a JavaScript event hook that will run your code any time the theme changes.
This is useful if you need to change elements of your page that cannot be defined by CSS rules.
For example, to change an image source (e.g., logo) whenever the ``data-theme`` changes, a snippet like this can be used:

.. code-block:: rst

  .. raw:: html

    <script type="text/javascript">
      var observer = new MutationObserver(function(mutations) {
        const dark = document.documentElement.dataset.theme == 'dark';
        document.getElementsByClassName('mainlogo')[0].src = dark ? '_static/my_logo_dark.svg' : "_static/my_logo_light.svg";
      })
      observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
    </script>
    <link rel="preload" href="_static/my_logo_dark.svg" as="image">

  .. image:: _static/my_logo_light.svg
     :alt: My Logo
     :class: logo, mainlogo
     :align: center

The JavaScript reacts to ``data-theme`` changes to alter ``img``, and the ``link`` is used to preload the dark image.
See the `MutationObserver documentation <https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver>`_ for more information.

.. _css-variables:

CSS Theme variables
===================

This theme defines several `CSS variables <css-variable-help_>`_ that can be
used to quickly control behavior and display across your documentation.

These are based on top of the basic `Bootstrap CSS variables <https://getbootstrap.com/docs/4.0/getting-started/theming/#css-variables>`_
extended with some theme specific variables.

base variables
--------------

In order to change a variable, follow these steps:

1. :ref:`Add a custom CSS stylesheet <custom-css>`. This is where we'll configure the variables.
2. Underneath a ``:root`` section, add the variables you wish to update. For example, to update
   the base font size, you might add this to ``custom.css``:

   .. code-block:: css

       :root {
           --pst-font-size-base: 17px;
       }

.. important::

   Note that these are `CSS variables <css-variable-help_>`_ and not
   `SASS variables <https://sass-lang.com/documentation/variables>`_.
   The theme is defined with CSS variables, not SASS variables! Refer to the previous section if
   you desire a different behavior between the light and dark theme.

For a complete list of the theme variables that you may override, see the
`theme variables defaults CSS file <pydata-css-variables_>`_:

.. literalinclude:: ../../src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static/styles/theme.css
  :language: CSS

Color variables
---------------

Each color variable has two values, one corresponding to the "light" and one for the "dark" theme.
These are used throughout many of the theme elements to define text color, background color, etc.

You can control the colors used for these variables for each theme by
:ref:`adding a custom CSS stylesheet <custom-css>` and adding a structure like so:

.. code-block:: css

    html[data-theme="light"] {
        --pst-color-primary: black;
    }

    html[data-theme="dark"] {
        --pst-color-primary: white;
    }

For a complete list of the theme colors that you may override, see the
`color variables defaults CSS file <pydata-css-colors_>`_:

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/base/_color.scss
  :language: scss

Change footer display
=====================

Each footer element is wrapped in a ``<div>`` with a ``footer-item`` class, allowing you to style the structure of these items with custom CSS.

For example, by default the footer items are displayed as blocks that stack vertically.
To change this behavior so that they stack **horizontally**, add a rule like the following in your custom ``.css`` file.

.. code-block:: css

   // Make each footer item in-line so they stack horizontally instead of vertically
   .footer-item {
     display: inline-block;
   }

   // Add a separating border line for all but the last item
   .footer-item:not(:last-child) {
     border-right: 1px solid var(--pst-color-text-base);
     margin-right: .5em;
     padding-right: .5em;
   }

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

.. _pydata-css-variables: https://github.com/pydata/pydata-sphinx-theme/blob/master/src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static/styles/theme.css
.. _pydata-css-colors: https://github.com/pydata/pydata-sphinx-theme/blob/master/src/pydata_sphinx_theme/assets/styles/base/_color.scss
.. _css-variable-help: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

.. meta::
    :description lang=en:
        Advanced customization of pydata-sphinx-theme's HTML and CSS.
