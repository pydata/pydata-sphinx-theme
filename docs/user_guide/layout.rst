==========================
Theme Structure and Layout
==========================

This section describes some basic ways to control the layout and structure of your documentation.
This theme inherits its structure and section terminology from the `Sphinx Basic NG theme <https://sphinx-basic-ng.readthedocs.io/en/latest/>`__.

Overview of theme layout
========================

Below is a brief overview of the major layout of this theme.
Take a look at the diagram to understand what the major sections are called.
Where you can insert component templates in ``html_theme_options``, we include the variable name ``in inline code``.
Click on section titles to learn more about them and some basic layout configuration.

.. The directives below generate a grid-like layout that mimics the structure of this theme.
.. It uses Sphinx Design grids: https://sphinx-design.readthedocs.io/en/latest/grids.html

.. raw:: html

    <style>
    .content {
        min-height: 14rem;
        justify-content: space-between;
        display: flex;
        flex-direction: column;
    }
    </style>

.. grid::
    :gutter: 0
    :class-container: sd-text-center

    .. grid-item::
        :padding: 2
        :outline:
        :columns: 12

        .. grid::
            :margin: 0

            .. grid-item::
                :padding: 2
                :columns: 12

                .. button-ref:: layout-header
                    :color: primary
                    :outline:

            .. grid-item::
                :padding: 2
                :columns: 3

                Logo

                ``navbar_start``

            .. grid-item::
                :padding: 2
                :columns: 6

                Section links

                ``navbar_center``

            .. grid-item::
                :padding: 2
                :columns: 3

                Components

                ``navbar_end``

    .. grid-item::
        :padding: 2
        :outline:
        :columns: 4
        :class: primary-sidebar

        .. button-ref:: layout-sidebar-primary
            :color: primary
            :outline:

            Primary Sidebar

        Links between pages in the active section.

        ``sidebars``

        ``primary_sidebar_end``

    .. grid-item::
        :columns: 8

        .. grid::
            :margin: 0
            :gutter: 0

            .. grid-item::
                :class: content
                :padding: 2
                :columns: 6
                :outline:

                .. button-ref:: layout-article-header
                    :color: primary
                    :outline:

                    Article Header

                ``article_header_start``
                ``article_header_end``

                **Article Content**

                .. button-ref:: layout-article-footer
                    :color: primary
                    :outline:

                    Article Footer

            .. grid-item::
                :padding: 2
                :columns: 6
                :outline:
                :class: sidebar-secondary

                .. button-ref:: layout-sidebar-secondary
                    :color: primary
                    :outline:

                    Secondary Sidebar

                Within-page header links

                ``secondary_sidebar_items``

        .. grid::
            :margin: 0
            :gutter: 0
            :outline:

            .. grid-item::
                :padding: 2
                :columns: 12
                :class: footer-content

                .. button-ref:: layout-footer-content
                    :color: primary
                    :outline:

                    Footer content



    .. grid-item::
        :padding: 2
        :outline:
        :columns: 12
        :class: footer

        .. button-ref:: layout-footer
            :color: primary
            :outline:

            Footer

        ``footer_start``
        ``footer_end``

Horizontal spacing
------------------

By default the theme's three columns have fixed widths.
The ``primary sidebar`` will snap to the left, the ``secondary sidebar`` will snap to the right, and the ``article content`` will be centered in between.

- If one of the sidebars is not present, then the ``article content`` will be centered between the other sidebar and the side of the page.
- If neither sidebar is present, the ``article content`` will be in the middle of the page.

If you'd like the ``article content`` to take up more width than its default, use the ``max-width`` and ``flex-grow`` CSS variables with the ``.bd-content`` selector.
For example, to make the content grow to fit all available width, add a custom CSS rule like:

.. code-block:: css

   .bd-content {
     flex-grow: 1;
     max-width: 100%;
   }

Templates and components
========================

There are a few major theme sections that you can customize to add/remove
components, or add your own components. Each section is configured with a
list of *html templates* — these are snippets of HTML that are inserted into
the section by Sphinx.

You can choose which templates show up in each section, as well as the order in
which they appear. This page describes the major areas that you can customize.

.. note::

   When configuring templates in each section, you may omit the ``.html``
   suffix after each template if you wish.


.. _layout-header:

Header / Navigation Bar
=======================

Located in ``sections/header.html``.

The header is at the top of the page above all other content, and contains site-level information.

Header sections
---------------

The header is broken up into three sections.
Each section is configured in ``conf.py`` with the following configuration:

- Left section: ``html_theme_options['navbar_start']``
- Middle menu: ``html_theme_options['navbar_center']``
- Right section: ``html_theme_options['navbar_end']``
- Persistent right section: ``html_theme_options['navbar_persistent']``

By default, the following configuration is used:

.. code-block:: python

   html_theme_options = {
   ...
   "navbar_start": ["navbar-logo"],
   "navbar_center": ["navbar-nav"],
   "navbar_end": ["navbar-icon-links"],
   "navbar_persistent": ["search-button"]
   ...
   }

.. warning::

    The *Persistent right section* is placed next to the ``navbar_end`` but its elements will remain visible in the header even on small screens when all other elements are collapsed. It has been design for the ``search-button`` only and we cannot guarantee its compatibility with other components.

Configure the navbar center alignment
-------------------------------------

By default, the navigation bar center area will align with the content on your
page. This equals the following default configuration:

.. code-block:: python

   html_theme_options = {
      ...
      "navbar_align": "content"
      ...
   }

If instead you'd like these items to snap to the left (closer to the logo), use this
configuration:

.. code-block:: python

   html_theme_options = {
      ...
      "navbar_align": "left"
      ...
   }

If you'd like these items to snap to the right of the page, use this configuration:

.. code-block:: python

   html_theme_options = {
      ...
      "navbar_align": "right"
      ...
   }


.. _layout-article-header:

Article Header
==============

Located in ``sections/header-article.html``.

The article header is a narrow bar just above the article's content.
There are two sub-sections that can have component templates added to them:

- ``article_header_start`` is aligned to the beginning (left) of the article header.
  By default, this section has the ``breadcrumbs.html`` component which displays links to parent pages of the current page.
- ``article_header_end`` is aligned to the end (right) of the article header.
  By default, this section is empty.

.. _layout-sidebar-primary:

Primary sidebar (left)
======================

Located in ``sections/sidebar-primary.html``.

The primary sidebar is just to the left of a page's main content.
It is primarily used for between-section navigation.
By default it will show links to any sublings / children of the current active top-level section (corresponding to links in your header navigation bar).

Configuring it is a bit different from configuring the other sections, because configuring the sidebar is natively supported in Sphinx, via the ``html_sidebars`` configuration variable.

For the primary sidebar only, you can configure templates so that they only show
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
        "**": ["sidebar-nav-bs", "sidebar-ethical-ads"]
    }

- ``sidebar-nav-bs.html`` - a bootstrap-friendly navigation section.

  When there are no pages to show, it will disappear and potentially add extra space for your page's content.

- ``sidebar-ethical-ads.html`` - a placement for ReadTheDocs's Ethical Ads (will only show up on ReadTheDocs).

Primary sidebar end sections
----------------------------

There is a special ``<div>`` within the primary sidebar that appears at the
bottom of the page, regardless of the content that is above it.

To control the HTML templates that are within this div, use
``html_theme_options['primary_sidebar_end']`` in ``conf.py``.

By default, it has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "primary_sidebar_end": ["sidebar-ethical-ads"],
      ...
    }

Remove the primary sidebar from pages
-------------------------------------

If you'd like the primary sidebar to be removed from a page, you can use the
following configuration in ``conf.py``:

.. code-block:: python

   html_sidebars = {
     "pagename": []
   }

This works for glob-style patterns as well. For example:

.. code-block:: python

   html_sidebars = {
     "folder/*": []
   }

If you'd like to remove the primary sidebar from **all** pages of your documentation,
use this pattern:

.. code-block:: python

   html_sidebars = {
     "**": []
   }

.. _layout-footer-content:

Footer Content
==============

Located in ``sections/footer-content.html``.

The footer content is a narrow bar spanning the article’s content and secondary sidebar.
It does not contain anything immediately viewable to the reader, but is kept as a placeholder in case theme developers wish to re-use it in the future.


.. _layout-sidebar-secondary:

Secondary Sidebar (right)
=========================

Located in ``sections/sidebar-secondary.html``.

The in-page sidebar is just to the right of a page's article content, and is
configured in ``conf.py`` with ``html_theme_options['secondary_sidebar_items']``.

By default, it has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
      ...
    }

To learn how to further customize or remove the secondary sidebar, please check :doc:`page-toc`.

.. _layout-article-footer:

Article Footer
==============

Located in ``sections/footer-article.html``.

The article footer exists just below your page's article, and is primarily used for navigating between adjacent sections / pages.

Hide the previous and next buttons
----------------------------------

By default, each page of your site will have "previous" and "next" buttons
at the bottom. You can hide these buttons with the following configuration:

.. code:: python

   html_theme_options = {
     "show_prev_next": False
   }

.. _layout-footer:

Footer
======

Located in ``sections/footer.html``.

The footer is just below a page’s main content, and is configured in ``conf.py``
with ``html_theme_options['footer_start']`` and ``html_theme_options['footer_end']``.

By default, ``footer_end`` is empty, and ``footer_start`` has the following templates:

.. code-block:: python

    html_theme_options = {
      ...
      "footer_start": ["copyright", "sphinx-version", "theme-version"],
      ...
    }

Within each subsection, components will stack **vertically**.
If you'd like them to stack **horizontally** use a custom CSS rule like the following:

.. code-block:: css

   .footer-items__start, .footer-items__end {
     flex-direction: row;
   }

Change footer display
---------------------

Each footer element is wrapped in a ``<div>`` with a ``footer-item`` class, allowing you to style the structure of these items with custom CSS.

For example, by default the footer items are displayed as blocks that stack vertically.
To change this behavior so that they stack **horizontally**, add a rule like the following in your custom ``.css`` file.

.. code-block:: css

   /* Make each footer item in-line so they stack horizontally instead of vertically */
   .footer-item {
     display: inline-block;
   }

   /* Add a separating border line for all but the last item */
   .footer-item:not(:last-child) {
     border-right: 1px solid var(--pst-color-text-base);
     margin-right: .5em;
     padding-right: .5em;
   }


Built-in components to insert into sections
===========================================

Below is a list of built-in templates that you can insert into any section.
Note that some of them may have CSS rules that assume a specific section (and
will be named accordingly).

.. refer to files in: src/pydata_sphinx_theme/theme/pydata_sphinx_theme/components/

- ``breadcrumbs.html``
- ``copyright.html``
- ``edit-this-page.html``
- ``footer-article/prev-next.html``
- ``icon-links.html``
- ``last-updated.html``
- ``navbar-icon-links.html``
- ``navbar-logo.html``
- ``navbar-nav.html``
- ``page-toc.html``
- ``searchbox.html``
- ``search-button.html``
- ``search-field.html``
- ``sidebar-ethical-ads.html``
- ``sidebar-nav-bs.html``
- ``sourcelink.html``
- ``sphinx-version.html``
- ``theme-switcher.html``
- ``version-switcher.html``
- ``indices.html``
- ``theme-version.html``


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
