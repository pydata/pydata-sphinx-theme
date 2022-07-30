Page Table of Contents
======================

Show more levels of the in-page TOC by default
----------------------------------------------

Normally only the 2nd-level headers of a page are show in the right
table of contents, and deeper levels are only shown when they are part
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
