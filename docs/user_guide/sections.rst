

Add/Remove items from theme sections
====================================

There are a few major theme sections that you can customize to add/remove
components, or add your own components. Each section is configured with a
list of *html templates* - these are snippets of HTML that are inserted into
the section by Sphinx.

You can choose which templates show up in each section, as well as the order in
which they appear. This page describes the major areas that you can customize.

.. note::
    
   When configuring templates in each section, you may omit the ``.html``
   suffix after each template if you wish.

The navbar items
================

The navbar is at the top of the page, and is broken up into three sections.
Each section is configured in ``conf.py`` with the following configuration:

- Left section: ``html_theme_options['navbar_left']``
- Middle menu: ``html_theme_options['navbar_menu']``
- Right section: ``html_theme_options['navbar_right']``

By default, the following configuration is used:

.. code-block:: python

   html_theme_options = {
   ...
   "navbar_left": ["navbar-logo"],
   "navbar_menu": ["navbar-menu-nav"],
   "navbar_right": ["navbar-menu-buttons"]
   ...
   }

The left sidebar
================

The left sidebar is just to the left of a page's main content.
Configuring it is supported natively in Sphinx, via the ``html_sidebars``
configuration variable.

By default, it has the following templates:

.. code-block:: python

    html_sidebars = ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]


The right in-page sidebar
=========================

The in-page sidebar is just to the right of a page's main content, and is
configured in ``conf.py`` with ``html_theme_options['page_sidebar_items']``.

By default, it has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "page_sidebar_items": ["page-toc", "edit-this-page"],
      ...
    }

The footer
==========

The footer is just below a page's main content, and is configured in ``conf.py``
with ``html_theme_options['footer_items']``.

By default, it has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "footer_items": ["copyright", "sphinx-version"],
      ...
    }

Add your own HTML templates to theme sections
=============================================

If you'd like to add your own custom template to any of these sections, you
could do so with the following steps:

1. Create an HTML file in a folder called ``_templates``. For example, if
   you wanted to display the version of your documentation using a Jinja
   template, you could create a file: ``_templates/version.html`` and put the
   following in it:

   .. code-block:: html

      <!-- This will display the version of the docs -->
      {{ version }}

1. Now add the file to your menu items for one of the sections above. For example:
   
   .. code-block:: python

      html_theme_options = {
      ...
      "navbar_left": ["version", "menu-logo"],
      ...
      }
