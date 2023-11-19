Page Table of Contents
======================

Show more levels of the in-page TOC by default
----------------------------------------------

Normally only the 2nd-level headers of a page are shown in the right
table of contents and deeper levels are only shown when they are part
of an active section (when it is scrolled on screen).

You can show deeper levels by default by using the following configuration, indicating how many levels should be displayed:

.. code-block:: python

   html_theme_options = {
     "show_toc_level": 2
   }

All headings up to and including the level specified will now be shown
regardless of what is displayed on the page.

Remove the Table of Contents
----------------------------

To remove the Table of Contents, add ``:html_theme.sidebar_secondary.remove:`` to the `file-wide metadata <https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#file-wide-metadata>`_ at the top of a page.
This will remove the Table of Contents from that page only.

Per-page secondary-sidebar content
----------------------------------

``html_theme_options['secondary_sidebar_items']`` accepts either a ``list`` of secondary sidebar
templates to render on every page:

.. code-block:: python

   html_theme_options = {
     "secondary_sidebar_items": ["page-toc", "sourcelink"]
   }

or a ``dict`` which maps page names to ``list`` of secondary sidebar templates:

.. code-block:: python

   html_theme_options = {
     "secondary_sidebar_items": {
       "**": ["page-toc", "sourcelink"],
       "index": ["page-toc"],
     }
   }

If a ``dict`` is specified, the keys can contain glob-style patterns; page names which
match the pattern will contain the sidebar templates specified. This closely follows the behavior of
the ``html_sidebars`` option that is part of Sphinx itself, except that it operates on the
secondary sidebar instead of the primary sidebar. For more information, see `the Sphinx
documentation <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_sidebars>`__.
