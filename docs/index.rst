=======================
The PyData Sphinx Theme
=======================

A clean, Bootstrap-based Sphinx theme from the PyData community.
This theme is designed for more complex documentation that breaks into natural sub-sections.

It puts all top-level pages in your ``toctree`` into the header navigation bar.
The sidebar will be populated with second-level pages when a top-level page is active.
This allows you to group your documentation into sub-sections without cluttering the sidebar.

.. seealso::

   If you are looking for a Sphinx theme that puts all of its sub-pages in the sidebar, the `Sphinx Book Theme <https://sphinx-book-theme.readthedocs.io/>`_ has a similar look and feel, and `Furo <https://pradyunsg.me/furo/quickstart/>`_ is another excellent choice.

This site is a guide for using the theme, and a demonstration for how it looks with various
elements.

Sites that use this theme
=========================

.. SORTED ALPHABETICALLY

- Binder: https://docs.mybinder.org/
- Bokeh: https://docs.bokeh.org/en/latest/
- JupyterLab: https://jupyterlab.readthedocs.io/en/latest/
- JupyterHub: https://jupyterhub.readthedocs.io/en/latest/
- Matplotlib: https://matplotlib.org/stable/
- NetworkX: https://networkx.org/documentation/latest/
- NumPy: https://numpy.org/doc/stable/
- Pandas: https://pandas.pydata.org/docs/
- SciPy: https://scipy.github.io/devdocs/
- JupyterHub and Binder: https://docs.mybinder.org/, http://z2jh.jupyter.org/en/latest/, https://repo2docker.readthedocs.io/en/latest/, https://jupyterhub-team-compass.readthedocs.io/en/latest/
- Jupyter Book beta version uses an extension of this theme: https://beta.jupyterbook.org
- Fairlearn: https://fairlearn.org/main/about/
- PyVista: https://docs.pyvista.org

Aknowledgment and inspirations
==============================

To build this theme we drew inspiration from other great projects on the web that we would like to acknowledge here:

- GitBook / Metaflow: https://docs.metaflow.org/introduction/what-is-metaflow
- Furo: https://pradyunsg.me/furo/quickstart (and we also draw a lot of implementation / code from this)
- Docker: https://docs.docker.com/engine/docker-overview/
- PyTorch: https://pytorch.org/docs/stable/notes/autograd.html

Thanks to `@drammock <https://github.com/drammock>`_ for initial design of the theme logo.

.. toctree::
   :caption: Theme Documentation
   :maxdepth: 2

   user_guide/index
   contribute/index

.. toctree::
   :maxdepth: 2
   :hidden:

   demo/index


.. meta::
    :description lang=en:
        Top-level documentation for pydata-sphinx theme, with links to the rest
        of the site.
