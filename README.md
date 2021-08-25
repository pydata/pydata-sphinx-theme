# pydata-sphinx-theme

![pypi](https://img.shields.io/pypi/v/pydata-sphinx-theme) [![conda-forge](https://img.shields.io/conda/vn/conda-forge/pydata-sphinx-theme.svg)](https://anaconda.org/conda-forge/pydata-sphinx-theme) [![continuous-integration](https://github.com/pydata/pydata-sphinx-theme/actions/workflows/tests.yml/badge.svg)](https://github.com/pydata/pydata-sphinx-theme/actions/workflows/tests.yml) [![docs](https://readthedocs.org/projects/pydata-sphinx-theme/badge/)](https://readthedocs.org/projects/pydata-sphinx-theme/builds/) [![codecov](https://codecov.io/gh/pydata/pydata-sphinx-theme/branch/master/graph/badge.svg?token=NwOObjYacn)](https://codecov.io/gh/pydata/pydata-sphinx-theme)

A Bootstrap-based Sphinx theme from the PyData community.

Demo site: https://pydata-sphinx-theme.readthedocs.io/en/latest/

**Note**: This theme is originally being developed for the pandas docs (originally named "pandas-sphinx-theme"),
but since there is uptake in other projects, we are working on making this more
generic and more easily extensible to suit the needs of the different projects.

Sites that are using this theme:

- Pandas: https://pandas.pydata.org/docs/
- NumPy: https://numpy.org/devdocs/
- SciPy: https://scipy.github.io/devdocs/
- Bokeh: https://docs.bokeh.org/en/dev/
- JupyterHub and Binder: https://docs.mybinder.org/, http://z2jh.jupyter.org/en/latest/, https://repo2docker.readthedocs.io/en/latest/, https://jupyterhub-team-compass.readthedocs.io/en/latest/
- Jupyter Book beta version uses an extension of this theme: https://beta.jupyterbook.org
- CuPy: https://docs.cupy.dev/en/latest/
- MegEngine: https://megengine.org.cn/doc/stable/zh/
- Fairlearn: https://fairlearn.org/main/about/
- NetworkX: https://networkx.org/documentation/latest/
- MNE-Python: https://mne.tools/stable/index.html
- PyVista: https://docs.pyvista.org


## Installation and usage

The theme is available on PyPI and conda-forge. You can install
and use as follows:

- Install the `pydata-sphinx-theme` in your doc build environment:

  ```
  pip install pydata-sphinx-theme
  # or
  conda install pydata-sphinx-theme --channel conda-forge
  ```

- Then, in the `conf.py` of your sphinx docs, you update the `html_theme`
  configuration option:

  ```
  html_theme = "pydata_sphinx_theme"
  ```

And that's it!

Well, in principle at least. In practice, there are might still be a few
pandas-specific things that are right now hard-coded in the theme. We also need
to work on better configurability and extensibility. Feedback and contributions
are very welcome!

## Theme development

Contributions are very welcome! Installing the development version, building
the demo docs and developing the css/js of the theme, etc, is explained in
more detail in the contributing section of the documentation:
https://pydata-sphinx-theme.readthedocs.io/en/latest/contributing.html


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

- A [`BootstrapHTML5Translator`](./pydata_sphinx_theme/bootstrap_html_translator.py),
  subclassing sphinx' translator, but overriding certain elements to generate
  Bootstrap-compatible html. Currently, this includes: converting admonitions to
  Bootstrap "alert" classes, and updating the classes used for html tables.
- A [sphinx event](./pydata_sphinx_theme/__init__.py) to add navigation
  objects into the html context which is available in the html (jinja2)
  templates. This allows to put the structure of the navigation elements in the
  actual layout, instead of having to rely on the hard-coded formatting of
  sphinx (this is inspired on the navigation objects of mkdocs:
  https://www.mkdocs.org/user-guide/custom-themes/#nav). We would love to see
  this added to sphinx itself (instead of needing a sphinx event), but for now
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

The initial layout and css were inspired on the Bootstrap documentation site.
