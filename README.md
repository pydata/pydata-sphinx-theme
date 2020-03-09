# pandas-sphinx-theme

A Bootstrap-based sphinx theme.

Demo site: https://pandas-sphinx-theme.readthedocs.io/en/latest/

**Note**: This theme is originally being developed for the pandas docs (hence the name),
but since there is uptake in other projects, we are working on making this more
generic and more easily extensible to suit the needs of the different projects
(and need a rename as well).

Sites that are using this theme:

- Pandas: https://dev.pandas.io/docs/
- Bokeh: https://docs.bokeh.org/en/dev/
- JupyterHub: http://z2jh.jupyter.org/en/latest/ and https://jupyterhub-team-compass.readthedocs.io/en/latest/

This repo holds a temporary (slimmed down) copy of the pandas documentation to
test the theme with on PRs. The result is hosted at the demo site.

## Installation and usage

This theme is not yet released as a package on PyPI, but you can already install
and use as follows:

- Install the `pandas-sphinx-theme` in your doc build environment from the git
  repo. You can do this manually with pip:

  ```
  pip install git+https://github.com/pandas-dev/pandas-sphinx-theme.git@master
  ```

  or in a conda environment yml file, you can add:

  ```
  - pip:
    - git+https://github.com/pandas-dev/pandas-sphinx-theme.git@master
  ```

- Then, in the `conf.py` of your sphinx docs, you update the `html_theme`
  configuration option:

  ```
  html_theme = "pandas_sphinx_theme"
  ```

And that's it!

Well, in principle at least. In practice, there are might still be a few
pandas-specific things that are right now hard-coded in the theme. We also need
to work on better configurability and extensibility. Feedback and contributions
are very welcome!

## Theme development

The theme is bundled via Webpack. In `./src/*` the theme related stylesheets and javascript is located. 2 entrypoints are available:

- Stylesheet: `./src/scss/index.scss'
- Javascript: `./src/js/index.js`

Both entrypoints will be bundled into `./pandas_sphinx_theme/static/{css,js}`.

Theme development was inspired by the [ReadTheDocs sphinx theme](https://github.com/readthedocs/sphinx_rtd_theme).

### Steps to develop the theme:

1. Install yarn
2. Install theme dependencies
3. Run development server
4. Build production assets

**Important:** in orde to commit changes to the theme, ensure you run `yarn build:production` so all assets will be bundled into `./pandas_sphinx_theme/static/`.

#### Install yarn

[Yarn](https://yarnpkg.com) is a package manager we use for managing Javascript and CSS dependencies.

Install via conda:

```bash
conda install yarn
```

Install alternative: https://classic.yarnpkg.com/en/docs/install.

#### Install theme dependencies

Install theme related dependencies:

```bash
yarn install
```

#### Run development server

```bash
yarn build:dev
```

A development server is available at http://localhost:1919. When working
on the theme, like editing stylesheets, javascript, .rst or .py files
every save reloads the development server. This reload includes bundling
stylesheets, javascript, and running sphinx again.

The following files will be watched and reloaded on change:

- ./src/js/index.js
- ./src/scss/index.scss
- ./docs/\*\*/\*.rst
- ./docs/\*\*/\*.py

#### Build production assets

To build the new theme assets into the theme, run the following command.

```bash
yarn build:production
```

## How is this theme working?

### The html layout

The "layout" included in this theme is originally mainly targetted towards
documentation sites with many pages, and where putting all navigation in a
single sidebar can therefore get unwieldy.

The current layout features 3 navigation elements:

- A top navbar with top-level navigation
- A left sidebar with subsequent navigation up to single pages
- A right sidebar with a local "On this page" table of contents

What is put where is determined by the sphinx "toctree" (and such depending on
the structure of your sphinx docs). The first level of the toctree is put in the
top navbar, and the second (and potentially) third level is put in the left
sidebar.

It should certainly be possible to make the exact used levels of the sphinx
toctree configurable.

### Implementation details

A second aspect of the design of this theme is that we are trying to make good
use of Bootstrap features and use as much as possible actual (templated) html
and css to define the theme, instead of relying on sphinx to do custom
formatting. This should make the theming and layouts more flexible to customize.

To this end, this package includes:

- A [`BootstrapHTML5Translator`](./pandas_sphinx_theme/bootstrap_html_translator.py),
  subclassing sphinx' translator, but overriding certain elements to generate
  Bootstrap-compatible html. Currently, this includes: converting admonitions to
  Bootstrap "alert" classes, and updating the classes used for html tables.
- A [sphinx "monkeypatch"](./pandas_sphinx_theme/__init__.py) to add toctree
  objects into the html context which is available in the html (jinja2)
  templates. This allows to put the structure of the navigation elements in the
  actual layout, instead of having to rely on the hard-coded formatting of
  sphinx (this is inspired on the navigation objects of mkdocs:
  https://www.mkdocs.org/user-guide/custom-themes/#nav). We would love to see
  this added to sphinx itself (instead of needing to monkeypatch), but for not
  did not yet get any reaction from the sphinx developers.

Those items also avoid writing javascript functions to "fix up" the html
generated by sphinx to make it suitable for theming.

### What's the difference with bootstrap-sphinx-theme ?

There is already a sphinx Bootstrap theme used by some project in the community:
https://github.com/ryan-roemer/sphinx-bootstrap-theme/

Currently, the main difference is that this theme is using Bootstrap 4 instead
of 3 and provides a different default layout. At some point, it would be good to
contribute changes to that package (or at least the parts that deal with
Bootstrap and sphinx that could be shared).
