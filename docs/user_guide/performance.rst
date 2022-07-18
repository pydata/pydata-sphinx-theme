
Build performance and size
==========================

By default this theme includes all of your documentation links in a collapsible sidebar.
However, this may slow down your documentation builds considerably if you have a lot of documentation pages.
This is most common with documentation for projects with a large API, which use the ``.. autosummary::`` directive to generate API documentation.

To improve the performance of your builds in these cases, first try modifying the navigation depth in the sidebar (see :ref:`navigation-depth`).
If that doesn't work, try the fix in the section below.

.. _remove_toctrees:

Selectively remove pages from your sidebar
------------------------------------------

You can prevent pages from showing up in the navigation bar using a Sphinx
extension called `sphinx-remove-toctrees <https://github.com/executablebooks/sphinx-remove-toctrees>`_.
This is useful if your documentation generates lots of "stub pages" in a folder,
which is common with API documentation.

This lets you add a configuration like so:

.. code-block::

   remove_from_toctrees = ["folder_one/generated/*"]

and any pages that are inside of ``folder_one/generated/`` will not show up in the sidebar.

Check out the `sphinx-remove-toctrees documentation <https://github.com/executablebooks/sphinx-remove-toctrees#install>`_
for information about how to install and use this extension.
