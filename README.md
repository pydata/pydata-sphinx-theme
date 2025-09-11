# The PyData Sphinx Theme

[![License badge](https://img.shields.io/badge/License-BSD_3--Clause-yellow?logo=opensourceinitiative&logoColor=white)](https://github.com/pydata/pydata-sphinx-theme/blob/main/LICENSE)
[![PyPI version badge](https://img.shields.io/pypi/v/pydata-sphinx-theme?logo=python&logoColor=white&color=orange)](https://pypi.org/project/pydata-sphinx-theme/)
[![conda-forge version badge](https://img.shields.io/conda/vn/conda-forge/pydata-sphinx-theme.svg?logo=anaconda&logoColor=white&color=orange)](https://anaconda.org/conda-forge/pydata-sphinx-theme)
[![GitHub Workflow test status badge](https://img.shields.io/github/actions/workflow/status/pydata/pydata-sphinx-theme/CI.yml?logo=github&logoColor=white)](https://github.com/pydata/pydata-sphinx-theme/actions/workflows/CI.yml)
[![Read the Docs build status badge](https://img.shields.io/readthedocs/pydata-sphinx-theme/latest?logo=readthedocs&logoColor=white)](https://readthedocs.org/projects/pydata-sphinx-theme/builds/)

A clean, three-column, Bootstrap-based Sphinx theme by and for the [PyData community](https://pydata.org).

- :books: Documentation: https://pydata-sphinx-theme.readthedocs.io/en/stable
- :bulb: Examples: https://pydata-sphinx-theme.readthedocs.io/en/stable/examples
- :raised_hands: Contribute: https://pydata-sphinx-theme.readthedocs.io/en/stable/community
- :globe_with_meridians: Translate: https://explore.transifex.com/12rambau/pydata-sphinx-theme/

[![PyData theme - Configure the search position demo image showcasing both the light and dark theme in a single image.](./docs/_static/theme-demo-screenshot.png)](https://pydata-sphinx-theme.readthedocs.io/en/stable)

## Installation and usage

The theme is available on PyPI and conda-forge. You can install
and use as follows:

- Install the `pydata-sphinx-theme` in your doc build environment:

  ```bash
  pip install pydata-sphinx-theme
  # or
  conda install pydata-sphinx-theme --channel conda-forge
  ```

- Then, in the `conf.py` of your sphinx docs, you update the `html_theme`
  configuration option:

  ```python
  html_theme = "pydata_sphinx_theme"
  ```

And that's it!

> [!NOTE]
> This theme may not work with the latest major versions of Sphinx, especially
> if they have only recently been released. Please give us a few months of
> time to work out any bugs and changes when new releases are made.
> See [our contributing documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/community/practices/versions.html#supported-sphinx-versions) for more information.

## Contribute to and develop the theme

Contributions are very welcome! Installing the development version, building
the example docs and developing the `CSS/JS` of the theme, etc., is explained in
more detail in the contributing section of the documentation:

- [Community and contributing documentation](https://pydata-sphinx-theme.readthedocs.io/en/latest/community/index.html)
