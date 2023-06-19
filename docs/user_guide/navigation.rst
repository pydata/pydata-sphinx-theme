.. _navigation-depth:

Navigation depth and collapsing sidebars
========================================

By default, this theme allows expanding/collapsing subsections in the primary
sidebar navigation (without actually navigating to the page itself), and this extends
up to 4 levels deep:

.. image:: /_static/demo-expandable-navigation.gif


Control how many navigation levels are shown by default
-------------------------------------------------------

You can control how many navigation levels are shown when a page is
loaded. By default, this level is 1, and only top-level pages are shown,
with drop-boxes to reveal their children. To make their children show up by
default, you can use the following configuration in ``conf.py``:

.. code:: python

   html_theme_options = {
     "show_nav_level": 2
   }

This will make the first two navigation levels show up by default (AKA, top-level
pages and their immediate children).

Collapse entire toctree captions/parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your ``toctree`` elements have captions assigned to them (with ``:caption:``), you may
collapse navigation items so that only the caption is visible. Clicking on the
caption will display the items below.

To enable this behavior, set the ``show_nav_level`` value to 0, like below:

.. code:: python

   html_theme_options = {
      "show_nav_level": 0
   }

You can only collapse your ``toctree`` items underneath their caption if a caption is defined for them!
If your ``toctree`` does not have a caption defined, then all the pages underneath it will be displayed
(the same as the default theme behavior). See `the toctree documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`_
for more details.

.. note::

   In some Sphinx sites, the top-level ``toctree`` groupings make up "parts" in the documentation, with
   each page beneath making up a "chapter".

.. _navigation-levels:

Control the number of navigation levels
---------------------------------------

In addition, you can also control how many levels of the navigation are shown
in the sidebar (with a default of 4):

.. code:: python

   html_theme_options = {
     "navigation_depth": 2
   }


Remove reveal buttons for sidebar items
---------------------------------------

It is possible to turn off the expandable navigation entirely by setting
the `collapse_navigation` config option to True:

.. code:: python

   html_theme_options = {
     "collapse_navigation": True
   }
