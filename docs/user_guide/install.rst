************
Installation
************

This theme is not yet released as a package on PyPI, so for now you need to
install it from the git repo. You can do this with pip:

.. code:: console

    $ pip install git+https://github.com/pandas-dev/pandas-sphinx-theme.git@master

or in a conda environment yml file, you can add:

.. code:: none

    - pip:
      - git+https://github.com/pandas-dev/pandas-sphinx-theme.git@master


Then, in the ``conf.py`` of your sphinx docs, you update the ``html_theme``
configuration option:

.. code:: python

    html_theme = "pandas_sphinx_theme"
