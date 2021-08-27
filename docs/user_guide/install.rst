************
Installation
************

The theme is available on PyPI and conda-forge, and can thus be installed with:

.. code:: console

    $ pip install pydata-sphinx-theme

.. code:: console

    $ conda install pydata-sphinx-theme --channel conda-forge

Then, in the ``conf.py`` of your sphinx docs, you update the ``html_theme``
configuration option:

.. code:: python

    html_theme = "pydata_sphinx_theme"


If you want to track the development version of the theme, you can
install it from the git repo:

.. code:: console

    $ pip install git+https://github.com/pydata/pydata-sphinx-theme.git@master

or in a conda environment yml file, you can add:

.. code:: none

    - pip:
      - git+https://github.com/pydata/pydata-sphinx-theme.git@master

.. meta::
    :description lang=en:
        Detailed instructions for installing pydata-sphinx-theme.
