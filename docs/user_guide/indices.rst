==============
Sphinx indices
==============

Sphinx generates indices named `genindex`, `modindex` and `py-modindex` when building a documentation. More information about them can be found in the `Sphinx documentation for indices <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-index>`__.

Add indices links
=================

By design the indices pages are not linked in a documentation generated with this theme. To include them in the primary sidebar of each page, add the following configuration to your ``conf.py`` file in ``html_theme_options`` and the available indices will be display at the bottom.

.. code-block:: python

    html_theme_options = {
        #[...]
        "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"]
        #[...]
    }

.. note::

    Don't forget to add back the ``"sidebar-ethical-ads.html"`` template if you are serving your documentation using `ReadTheDocs <https://readthedocs.org>`__.
