==========
User Guide
==========

The user guide describes how to use and customize this theme.

How the theme is structured
===========================

Below is a brief overview of the major layout of this theme.
First, take a look at the diagram to understand what the major sections are called.
This theme inherits its structure and section terminology from the `Sphinx Basic NG theme <https://sphinx-basic-ng.readthedocs.io/en/latest/>`__.

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
        :outline:
        :columns: 12

        .. grid::
            :margin: 0

            .. grid-item::
                :columns: 12

                **Header**

            .. grid-item::
                :columns: 3

                Logo

            .. grid-item::
                :columns: 6

                Section links

            .. grid-item::
                :columns: 3

                Components

    .. grid-item::
        :outline:
        :columns: 4
        :class: primary-sidebar

        **Primary Sidebar**

        Links between pages in the active section.

    .. grid-item::
        :outline:
        :columns: 6
        :class: content

        **Article content**

        **Article footer**

    .. grid-item::
        :outline:
        :columns: 2
        :class: secondary-sidebar

        **Secondary sidebar**

        Within-page header links

    .. grid-item::
        :outline:
        :columns: 12
        :class: footer

        **Footer**

Most of the functionality of this theme is built into its header and sidebars, so each is explained briefly below.

- **Header**: Contains links for **each major section of your documentation**.
  These are generated from your documentation's top-level documentation toctree items.
  Also contains your site's logo and icon links and components that are site-wide.
- **Primary Sidebar**: Contains links **between pages in the active section**. These are the second-level ``toctree`` items in your documentation.
  This will only be displayed if there are other pages in a section or if no section is active (like on the landing page)
- **Secondary Sidebar**: Contains links **to headers within the current page** as well as **page-specific** source links.

Configure the theme
===================

You can configure the behavior, look, and feel of the theme in many ways.
The remaining pages in the user guide cover various ways of doing so.

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
