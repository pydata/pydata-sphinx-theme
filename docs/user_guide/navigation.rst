.. _navigation-depth:

Navigation depth and collapsing sidebars
========================================

By default, this theme enables to expand/collapse subsections in the primary
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

This will make the first two navigations show up by default (AKA, top-level
pages and their immediate children).

Collapse entire toctree captions / parts
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
If your ``toctree`` does not have a caption defined, then all of the pages underneath it will be displayed
(the same as the default theme behavior). See `the toctree documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`_
for more details.

.. image:: /_static/demo-show_nav_level-0.gif

.. note::

   In some Sphinx sites, the top-level ``toctree`` groupings make up "parts" in the documentation, with
   each page beneath making up a "chapter".

.. _toc-caption-levels:

Categorize sub-pages with toctree captions
------------------------------------------

It is possible to categorize pages in the :ref:`Primary Sidebar<layout-sidebar-primary>` by placing all pages on a specific topic in their own ``toctree`` with a ``:caption:`` that is used as the category title. 

An example that will generate output similar to this website may look something like this:

.. code:: restructuredtext

   .. toctree::
      :caption: Get started

      install
      layout

   .. toctree::
      :caption: Navigation and links

      navigation
      page-toc

By default, this behavior is only present for pages on the second navigation level 
(i.e. the first navigation level that is shown in the primary sidebar). 
To show categories at deeper levels, set the ``toc_caption_maxdepth`` option to your desired depth:

.. code:: python

   html_theme_options = {
     "toc_caption_maxdepth": 3
   }

.. image:: /_static/demo-toc_caption_maxdepth-3.gif

.. note::
   Changing the ``toc_caption_maxdepth`` is not supported when collapsible toc captions are enabled with ``"show_nav_level": 0``

.. _navigation-levels:

Control the number of navigation levels
---------------------------------------

In addition, you can also control how many levels of the navigation are shown
in the sidebar (with a default of 4):

.. code:: python

   html_theme_options = {
     "navigation_depth": 2
   }

Control the navigation startdepth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   This functionality is not supported when collapsible toc captions are enabled with ``"show_nav_level": 0``

By default, the ``toctree`` displayed in the :ref:`Primary Sidebar<layout-sidebar-primary>` starts at the second navigation level, while the first navigation level is shown only in the :ref:`layout-header`.  
It is possible to override this behavior by explicitly setting a navigation startdepth:

.. code:: python

   html_theme_options = {
     "navigation_startdepth": 0
   }

To preserve the default behavior for categories made with toctree captions (see :ref:`toc-caption-levels`), it is necessary to edit the ``toc_caption_maxdepth`` parameter correspondingly (default = 1):

.. code:: python

   html_theme_options = {
     "navigation_startdepth": 0,
     "toc_caption_maxdepth": 2
   }

.. image:: /_static/demo-navigation_startdepth-0.gif

Remove reveal buttons for sidebar items
---------------------------------------

It is possible to turn off the expandable navigation entirely by setting
the `collapse_navigation` config option to True:

.. code:: python

   html_theme_options = {
     "collapse_navigation": True
   }
