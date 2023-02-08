************
Installation
************

.. note::

   Each pydata-sphinx-theme release has a minimum required Sphinx version,
   which should be automatically handled by your package installer.
   It is also tested against newer versions of Sphinx that were available
   prior to that release of the pydata-sphinx-theme package.
   If you run into issues when trying to use a more recent version of Sphinx,
   please open an issue here: https://github.com/pydata/pydata-sphinx-theme/issues

The theme is available on PyPI and conda-forge, and can thus be installed with:

.. code:: console

    $ pip install pydata-sphinx-theme

.. code:: console

    $ conda install pydata-sphinx-theme --channel conda-forge

Then, in the ``conf.py`` of your sphinx docs, you update the ``html_theme``
configuration option:

.. code:: python

    html_theme = "pydata_sphinx_theme"

.. note::

   This theme may not work with the latest major versions of Sphinx, especially
   if they have only recently been released. Please give us a few months of
   time to work out any bugs and changes when new releases are made.

Development version
===================

If you want to track the development version of the theme, you can
install it from the git repo:

.. code:: console

    $ pip install git+https://github.com/pydata/pydata-sphinx-theme.git@main

or in a conda environment yml file, you can add:

.. code:: yaml

    - pip:
      - git+https://github.com/pydata/pydata-sphinx-theme.git@main

.. meta::
    :description lang=en:
        Detailed instructions for installing pydata-sphinx-theme.
