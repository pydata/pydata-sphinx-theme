---
html_meta:
  "description lang=en": "How to become a contributor to the pydata-sphinx-theme."
---

# Contribute

These pages contain information about how you can get up-and-running with a development version of this theme, and how you can contribute to the project.

## Workflow for contributing changes

We follow a [typical GitHub workflow](https://guides.github.com/introduction/flow/)
of:

- create a personal fork of this repo
- create a branch
- open a pull request
- fix findings of various linters and checks
- work through code review

For each pull request, the demo site is built and deployed to make it easier to review
the changes in the PR. To access this, click on the "ReadTheDocs" preview in the CI/CD jobs.

## Location and structure of documentation

The documentation for this theme is in the `docs/` folder.
It is structured as a [Sphinx documentation site](https://sphinx-doc.org).
The content is written in a combination of reStructuredText and MyST Markdown.

## Location and structure of CSS/JS assets

The CSS and JS for this theme are built for the browser from `src/pydata_sphinx_theme/assets/*` with
[webpack](https://webpack.js.org/). The main entrypoints are:

- CSS: `src/pydata_sphinx_theme/assets/styles/index.scss`

  - the main part of the theme assets
  - customizes [Bootstrap](https://getbootstrap.com/) with [Sass](https://sass-lang.com)

- JS: `src/pydata_sphinx_theme/assets/scripts/index.js`

  - provides add-on Bootstrap features, as well as some custom navigation behavior

- webpack: `webpack.config.js`

  - captures the techniques for transforming the JS and CSS source files in
    `src/pydata_sphinx_theme/assets/*` into the production assets in `src/theme/pydata_sphinx_theme/static/`

**For more information** about developing this theme, see the sections below and in the left sidebar.

```{toctree}
:maxdepth: 2
setup
topics
manual
```
