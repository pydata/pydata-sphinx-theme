=======================
Theme variables and CSS
=======================

.. _pydata-css-variables: https://github.com/pydata/pydata-sphinx-theme/blob/main/src/pydata_sphinx_theme/assets/styles/variables/
.. _css-variable-help: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

This section covers a few ways that you can control the look and feel of your theme via your own CSS and theme variables.

.. _custom-css:

Custom CSS Stylesheets
======================

You can customize the theme's CSS by creating a custom stylesheet. This stylesheet will be used by Sphinx while building your site.
Any rules in this style sheet will override the default theme rules.

.. seealso::

   For a more in-depth guide in linking static CSS and JS assets in your site, see :doc:`static_assets`.


To add a custom stylesheet, follow these steps:

1. **Create a CSS stylesheet** in ``_static/css/custom.css``, and update the CSS rules as desired.
2. **Attach the stylesheet to your Sphinx build**. Add the following to ``conf.py``:

   .. code-block:: python

       html_static_path = ['_static']

       html_css_files = [
           'css/custom.css',
       ]

When you build your documentation, this stylesheet should now be activated.

CSS theme variables
===================

This theme defines several `CSS variables <css-variable-help_>`_ that can be
used to quickly control behavior and display across your documentation.

These are based on top of the basic `Bootstrap CSS variables <https://getbootstrap.com/docs/4.0/getting-started/theming/#css-variables>`_
extended with some theme-specific variables.

Base variables
--------------

Follow these steps to update the base variables:

1. :ref:`Add a custom CSS stylesheet <custom-css>`. This is where we'll configure the variables.
2. Underneath a ``html`` section, add the variables you wish to update. For example, to change the base font size you would add the following to your ``custom.css`` file :

   .. code-block:: css

       html {
           --pst-font-size-base: 17px;
       }

.. important::

   Note that the theme is defined with `CSS variables <css-variable-help_>`_
   and **not** `SASS variables <https://sass-lang.com/documentation/variables>`_.

   Refer to :ref:`the managing themes section in this documentation <manage-themes>` if
   you desire a different behavior between the light and dark theme.

For a complete list of the theme variables that you may override, see the
`theme variables defaults CSS file <pydata-css-variables_>`_:

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/variables/_layout.scss
  :language: scss

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/variables/_fonts.scss
  :language: scss

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/variables/_icons.scss
  :language: scss

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/variables/_admonitions.scss
  :language: scss

.. literalinclude:: ../../src/pydata_sphinx_theme/assets/styles/variables/_versionmodified.scss
  :language: scss

.. _color-variables:

Color variables
---------------

This theme specifies color variables for the primary and secondary colors (``--pst-color-primary`` and ``--pst-color-secondary``, respectively).
These are meant to complement one another visually across the theme, if you modify these, choose colors that look good when paired with one another.
There are also several other color variables that control the color for admonitions, links, menu items, etc.

Each color variable has two values, one corresponding to the "light" and one for the "dark" theme.
These are used throughout many of the theme elements to define text color, background color, etc.

Here is an overview of the colors available in the theme (change theme mode to switch from light to dark versions).


.. raw:: html

    <style>
      span.pst-primary {background-color: var(--pst-color-primary);}
      span.pst-secondary {background-color: var(--pst-color-secondary);}
      span.pst-accent {background-color: var(--pst-color-accent);}
      span.pst-success {background-color: var(--pst-color-success);}
      span.pst-info {background-color: var(--pst-color-info);}
      span.pst-warning {background-color: var(--pst-color-warning);}
      span.pst-danger {background-color: var(--pst-color-danger);}
      span.pst-background {background-color: var(--pst-color-background);}
      span.pst-on-background {background-color: var(--pst-color-on-background);}
      span.pst-surface {background-color: var(--pst-color-surface);}
      span.pst-on-surface {background-color: var(--pst-color-on-surface);}
      span.pst-target {background-color: var(--pst-color-target);}
    </style>

    <p>
      <span class="sd-badge pst-badge pst-primary sd-bg-text-primary">primary</span>
      <span class="sd-badge pst-badge pst-secondary sd-bg-text-secondary">secondary</span>
      <span class="sd-badge pst-badge pst-accent sd-bg-text-secondary">accent</span>
      <span class="sd-badge pst-badge pst-success sd-bg-text-success">success</span>
      <span class="sd-badge pst-badge pst-info sd-bg-text-info">info</span>
      <span class="sd-badge pst-badge pst-warning sd-bg-text-warning">warning</span>
      <span class="sd-badge pst-badge pst-danger sd-bg-text-danger">danger</span>
      <span class="sd-badge pst-badge pst-background">background</span>
      <span class="sd-badge pst-badge pst-on-background">on-background</span>
      <span class="sd-badge pst-badge pst-surface">surface</span>
      <span class="sd-badge pst-badge pst-on-surface sd-bg-text-primary">on-surface</span>
      <span class="sd-badge pst-badge pst-target">target</span>
    </p>


**To modify the colors for these variables** for light and dark themes, :ref:`add a custom CSS stylesheet <custom-css>` with a structure like so:

.. code-block:: css

    html[data-theme="light"] {
        --pst-color-primary: black;
    }

    html[data-theme="dark"] {
        --pst-color-primary: white;
    }

This theme uses shadows to convey depth in the light theme mode and opacity in the dark one.
It defines 4 color variables that help build overlays in your documentation.

- :code:`background`: color of the back-most surface of the documentation
- :code:`on-background` elements that are set on top of this background (e.g. the header navbar on dark mode).
- :code:`surface` elements set on the background with a light-grey color in the light theme mode. This color has been kept in the dark theme (e.g. code-block directives).
- :code:`on-surface` elements that are on top of :code:`surface` elements (e.g. sidebar directives).

The following image should help you understand these overlays:

.. raw:: html

    <style>
      /* use https://unminify.com to check the indented version of the overlay component */
      .overlay-container {margin-top: 10%; left: 20%; --width: 80%; --height: 200px; width: var(--width); height: var(--height); position: relative;}
      .overlay-container .pst-overlay {position: absolute; border: 2px solid var(--pst-color-border);}
      .overlay-container .pst-background {background-color: var(--pst-color-background); width: var(--width); transform: skew(-45deg); height: var(--height);}
      .overlay-container .pst-on-background {background-color: var(--pst-color-on-background); height: var(--height); width: calc(var(--width) / 3); transform: skew(-45deg) translate(-2rem, -2rem);}
      .overlay-container .pst-surface {background-color: var(--pst-color-surface); height: var(--height); width: calc(var(--width) / 3); transform: skew(-45deg) translate(-2rem, -2rem); left: calc(var(--width) / 3 * 2);}
      .overlay-container .pst-on-surface {background-color: var(--pst-color-on-surface); width: calc(var(--width) / 3); height: calc(var(--height) * 0.66); transform: skew(-45deg) translate(-2rem, -4rem); left: calc(var(--width) / 3 * 2);}
      .overlay-container .label {position: absolute; bottom: 0.5rem; left: 50%; transform: skew(45deg) translateX(-50%); white-space: nowrap;}
    </style>

    <div class="overlay-container">
      <div class="pst-overlay pst-background">
        <p class="label">background</p>
      </div>
      <div class="pst-overlay pst-on-background">
        <p class="label">on-background</p>
      </div>
      <div class="pst-overlay pst-surface">
        <p class="label">surface</p>
      </div>
      <div class="pst-overlay pst-on-surface">
        <p class="label sd-bg-text-primary">on-surface</p>
      </div>
    </div>

.. it would be nice to have this `.. literalinclude::` here to actually show
   the file, but there's a pygments bug that fails to lex SCSS variables
   (specifically the `$` symbol that prepends SCSS variables, see
   https://github.com/pygments/pygments/issues/2130). So for now it's
   just a raw download link.

For a complete list of the theme colors that you may override, see the :download:`PyData theme CSS colors stylesheet <../../src/pydata_sphinx_theme/assets/styles/variables/_color.scss>`.

Configure pygments theme
========================

As the Sphinx theme supports multiple modes, the code highlighting colors can be modified for each one of them by modifying the ``pygments_light_style`` and ``pygments_dark_style``.
You can check available Pygments colors on this `pygments demo page <https://pygments.org/styles/>`__.

.. code-block:: python

   html_theme_options = {
      ...
      "pygments_light_style": "tango",
      "pygments_dark_style": "monokai"
   }

Note that the PyData Sphinx theme uses the `accessible pygments styles <https://github.com/Quansight-Labs/accessible-pygments>`__ for its default syntax highlighting themes.
The accessible pygments themes are designed to meet `WCAG AA or AAA standards for color contrast <https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html>`__ and some included themes are also suitable for colorblind users
or low-light conditions.
You can check all the available styles at the `accessible pygments demo page <https://quansight-labs.github.io/accessible-pygments/>`__.

.. danger::

   The native Sphinx option ``pygments_style`` will be overwritten by this theme.
