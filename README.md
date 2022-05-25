# pydata-sphinx-theme

![pypi](https://img.shields.io/pypi/v/pydata-sphinx-theme) [![conda-forge](https://img.shields.io/conda/vn/conda-forge/pydata-sphinx-theme.svg)](https://anaconda.org/conda-forge/pydata-sphinx-theme) [![continuous-integration](https://github.com/pydata/pydata-sphinx-theme/actions/workflows/tests.yml/badge.svg)](https://github.com/pydata/pydata-sphinx-theme/actions/workflows/tests.yml) [![docs](https://readthedocs.org/projects/pydata-sphinx-theme/badge/)](https://readthedocs.org/projects/pydata-sphinx-theme/builds/) [![codecov](https://codecov.io/gh/pydata/pydata-sphinx-theme/branch/master/graph/badge.svg?token=NwOObjYacn)](https://codecov.io/gh/pydata/pydata-sphinx-theme)

A Bootstrap-based Sphinx theme from the PyData community.

Demo site: https://pydata-sphinx-theme.readthedocs.io/en/latest/

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

> **Note**
> This theme may not work with the latest major versions of Sphinx, especially
> if they have only recently been released. Please give us a few months of
> time to work out any bugs and changes when new releases are made.
> See [our contributing documentation](docs/contribute/topics.md) for more information.

## Contribute to and develop the theme

Contributions are very welcome! Installing the development version, building
the demo docs and developing the css/js of the theme, etc, is explained in
more detail in the contributing section of the documentation:

- [Contributing documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/contribute/index.html)
