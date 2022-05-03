==========
User Guide
==========

The user guide describes how to use and customize this theme.

How the theme is structured
===========================

This theme converts all **top-level toctree items** into links in the header navigation bar.
The sidebar will have no navigation links until one of these top-level links is active (e.g., if you are on a sub-page of a top-level link).
Once one of the top-level links is active, the sidebar will be populated with a list of pages that are underneath the top-level page.

For example, see the links in the sidebar for the other pages in this section.

.. toctree::
   :maxdepth: 2

   install
   configuring
   sections
   customizing
   accessibility

.. meta::
    :description lang=en:
        Documentation for users who wish to build sphinx sites with
        pydata-sphinx-theme.
