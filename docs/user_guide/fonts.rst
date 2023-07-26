Fonts and FontAwesome
=====================

The theme includes the `FontAwesome 6 Free <https://fontawesome.com/icons?m=free>`__
icon font (the ``.fa-solid, .fa-regular, .fa-brands`` styles, which are used for
:ref:`icon links <icon-links>` and admonitions).
This is the only *vendored* font, and otherwise, the theme by default relies on
available system fonts for normal body text and headers.

The default body and header fonts can be changed as follows:

- Using :ref:`custom-css`, you can specify which fonts to use for the body, header,
  and monospaced text. For example, the following can be added to a custom
  CSS file:

  .. code-block:: css

      html {
          --pst-font-family-base: Verdana, var(--pst-font-family-base-system);
          --pst-font-family-heading: Cambria, Georgia, Times, var(--pst-font-family-base-system);
          --pst-font-family-monospace: Courier, var(--pst-font-family-monospace-system);
      }

  The ``*-system`` variables are available to use as a fallback to the default fonts.

- If the font you want to specify in the section above is not generally available
  by default, you will additionally need to ensure the font is loaded.
  For example, you could download and vendor the font in the ``_static`` directory
  of your Sphinx site, and then update the base template to load the font resources:

  - Configure the `template_path <https://www.sphinx-doc.org/en/master/development/theming.html#templating>`__
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

    Your text may quickly show up as "unstyled" before the fonts are loaded. To reduce this, you may wish to explore options for
    `preloading content <https://developer.mozilla.org/en-US/docs/Web/HTML/Preloading_content>`__,
    specifically the binary font files. This ensures the files will be loaded
    before the CSS is parsed, but should be used with care.

.. _pydata-css-variables: https://github.com/pydata/pydata-sphinx-theme/blob/main/src/pydata_sphinx_theme/assets/styles/variables/
.. _pydata-css-colors: https://github.com/pydata/pydata-sphinx-theme/blob/main/src/pydata_sphinx_theme/assets/styles/variables/_color.scss
.. _css-variable-help: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
