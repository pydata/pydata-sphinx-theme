# Structure of this theme

## Location and structure of documentation

The documentation for this theme is in the `docs/` folder.
It is structured as a [Sphinx documentation site](https://sphinx-doc.org).
The content is written in a combination of reStructuredText and MyST Markdown.

## Location and structure of CSS/JS assets

The CSS and JS for this theme are built for the browser from `src/pydata_sphinx_theme/assets/*` with
[webpack](https://webpack.js.org/). The main entry points are:

- CSS: `src/pydata_sphinx_theme/assets/styles/pydata-sphinx-theme.scss`

  - the main part of the theme assets
  - customizes [Bootstrap](https://getbootstrap.com/) with [Sass](https://sass-lang.com)

- JS: `src/pydata_sphinx_theme/assets/scripts/pydata-sphinx-theme.js`

  - provides add-on Bootstrap features, as well as some custom navigation behavior

- webpack: `webpack.config.js`

  - captures the techniques for transforming the JS and CSS source files in
    `src/pydata_sphinx_theme/assets/*` into the production assets in `src/theme/pydata_sphinx_theme/static/`
