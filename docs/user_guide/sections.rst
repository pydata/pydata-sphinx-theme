====================================
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

- Left section: ``html_theme_options['navbar_start']``
- Middle menu: ``html_theme_options['navbar_center']``
- Right section: ``html_theme_options['navbar_end']``

By default, the following configuration is used:

.. code-block:: python

   html_theme_options = {
   ...
   "navbar_start": ["navbar-logo"],
   "navbar_center": ["navbar-nav"],
   "navbar_end": ["navbar-icon-links"]
   ...
   }

The left sidebar
================

The left sidebar is just to the left of a page's main content.
Configuring it is a bit different from configuring the other sections, because
configuring the sidebar is natively supported in Sphinx, via the ``html_sidebars``
configuration variable.

For the left sidebar only, you can configure templates so that they only show
up on certain pages. You do so via a configuration like so in ``conf.py``:

.. code-block:: python

    html_sidebars = {
        "<page_pattern>": ["list", "of", "templates"]
    }

Any pages that match ``<page_pattern>`` will have their respective templates
inserted. You can also ``*`` to do ``glob``-style matching, and may use ``**``
to match all pages.

By default, it has the following configuration:

.. code-block:: python

    html_sidebars = {
        "**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]
    }

Left sidebar end sections
=========================

There is a special ``<div>`` within the left sidebar that appears at the
bottom of the page, regardless of the content that is above it.

To control the HTML templates that are within this div, use
``html_theme_options['left_sidebar_end']`` in ``conf.py``.

By default, it has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "left_sidebar_end": ["sidebar-ethical-ads"],
      ...
    }


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

A list of built-in templates you can insert into sections
=========================================================

Below is a list of built-in templates that you can insert into any section.
Note that some of them may have CSS rules that assume a specific section (and
will be named accordingly).

- ``icon-links.html``
- ``search-field.html``
- ``copyright.html``
- ``edit-this-page.html``
- ``last-updated.html``
- ``navbar-icon-links.html``
- ``navbar-logo.html``
- ``navbar-nav.html``
- ``page-toc.html``
- ``sidebar-ethical-ads.html``
- ``sidebar-nav-bs.html``
- ``sphinx-version.html``
- ``version-switcher.html``
- ``theme-switcher.html``

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

2. Now add the file to your menu items for one of the sections above. For example:

   .. code-block:: python

      html_theme_options = {
      ...
      "navbar_start": ["navbar-logo", "version"],
      ...
      }
