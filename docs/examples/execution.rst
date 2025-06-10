Execution Libraries
===================

Many execution libraries can be used to display the output of IPython cells. We
used ``nbsphinx`` to parse and display the outputs presented in :doc:`./pydata`.
In this section we'll show alternatives that run code for you using a Jupyter
like kernel.

JupyterLite
-----------

.. warning::
    As of April 2025, we have not found a way to sync JupyterLite widgets with the theme's light/dark mode.
    You can see this for yourself if you change this page from light to dark mode. The rest of the page will
    appear in dark mode but the JupyterLite widget below will still be in light mode.
    Follow https://github.com/jupyterlite/jupyterlite-sphinx/issues/69 for more information.

``jupyterlite-sphinx`` brings the power of `JupyterLite
<https://jupyterlite.readthedocs.io/en/latest/>`__ to your Sphinx documentation.
It does a full JupyterLite deployment in your docs and provides some utilities
for using that deployment easily.

This section demonstrates how it displays in a **pydata-sphinx-theme** context:

.. replite::
    :kernel: python
    :height: 600px
    :prompt: Try Replite!

    print("it's a test")

jupyter-sphinx
--------------

Another common library is ``jupyter-sphinx``.
This section demonstrates a subset of functionality to make sure it behaves as expected.

.. jupyter-execute::

    import matplotlib.pyplot as plt
    import numpy as np

    rng = np.random.default_rng()
    data = rng.standard_normal((3, 100))
    fig, ax = plt.subplots()
    ax.scatter(data[0], data[1], c=data[2], s=3)
