.. _configuration:

*************
Configuration
*************

There are a number of options for configuring your site's look and feel.
All configuration options are passed with the ``html_theme_options`` variable
in your ``conf.py`` file. This is a dictionary with ``key: val`` pairs that
you can configure in various ways. This page describes the options available to you.

Configure project logo
==============================

To add a logo that's placed at the left of your nav bar, put a logo file under your
doc path's _static folder, and use the following configuration:

.. code:: python

   html_logo = "_static/logo.png"

The logo links to ``master_doc`` (usually the first page of your documentation) by default.
If you'd like it to link to another page or use an external link instead, use the following configuration:

.. code:: python

   html_theme_options = {
       "logo_link": "<other page or external link>"
   }


.. _icon-links:

Configure icon links
====================

If you'd like icon links to show up to the right of your main navigation bar, use the
following configuration:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/<your-org>/<your-repo>",
               "icon": "fab fa-github-square",
           },
           {
               "name": "GitLab",
               "url": "https://gitlab.com/<your-org>/<your-repo>",
               "icon": "fab fa-gitlab",
           },
           {
               "name": "Twitter",
               "url": "https://twitter.com/<your-handle>",
               "icon": "fab fa-twitter-square",
           },
       ],
       ...
   }


The value of ``icon`` can be any full
`FontAwesome 5 Free <https://fontawesome.com/icons?d=gallery&m=free>`__ icon.
In addition to the main icon class, e.g. ``fa-cat``, the "style" class must
also be provided e.g. `fab` for *branding*, or `fas` for *solid*.


.. Hint::

   To get custom colors like "Twitter blue", use the following in your CSS,
   e.g. ``custom.css``:

   .. code:: css

      i.fa-twitter-square:before {
         color: #55acee;
      }

   This has already been added for the brands that have *shortcuts*.

The below are shortcuts for commonly-used services, but may be removed in a future
release in favor of ``icon_links``:

.. code:: python

   html_theme_options = {
       ...
       "github_url": "https://github.com/<your-org>/<your-repo>",
       "gitlab_url": "https://gitlab.com/<your-org>/<your-repo>",
       "bitbucket_url": "https://bitbucket.org/<your-org>/<your-repo>",
       "twitter_url": "https://twitter.com/<your-handle>",
       ...
   }

Additionally, the screen-reader accessible label for this menu can be configured:

.. code:: python

   html_theme_options = {
       ...
       "icon_links_label": "Quick Links",
       ...
   }


Adding external links to your nav bar
=====================================

You can add external links to your navigation bar. These will show up to the right
of your site's main links, and will have a small icon indicating that they point to
an external site. You can add external links to the nav bar like so:

.. code:: python

   html_theme_options = {
     "external_links": [
         {"name": "link-one-name", "url": "https://<link-one>"},
         {"name": "link-two-name", "url": "https://<link-two>"}
     ]
   }

Adding favicons
===============

``pydata_sphinx_theme`` supports the
`standard sphinx favicon configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_favicon>`_,
using ``html_favicon``.

Additionally, ``pydata_sphinx_theme`` allows you to add any number of
browser- or device-specific favicons of any size. To define arbitrary favicons,
use the ``favicons`` configuration key. The ``href`` value can be either an
absolute URL (beginning with ``http``) or a local path relative to your
``html_static_path``:

.. code-block:: python

   html_theme_options = {
      "favicons": [
         {
            "rel": "icon",
            "sizes": "16x16",
            "href": "https://secure.example.com/favicon/favicon-16x16.png",
         },
         {
            "rel": "icon",
            "sizes": "32x32",
            "href": "favicon-32x32.png",
         },
         {
            "rel": "apple-touch-icon",
            "sizes": "180x180",
            "href": "apple-touch-icon-180x180.png"
         },
      ]
   }

``pydata_sphinx_theme`` will add ``link`` tags to your document's ``head``
section, following this pattern:

.. code-block:: html+jinja

   <link rel="{{ favicon.rel }}" sizes="{{ favicon.sizes }}" href="{{ favicon.href }}">


.. _configure-sidebar:

Configure the sidebar
=====================

``pydata_sphinx_theme`` provides two new sidebar items by default:

- ``sidebar-nav-bs.html`` - a bootstrap-friendly navigation section
- ``search-field.html`` - a bootstrap-friendly search bar

By default, this theme's sidebar has these two elements in it. If you'd like to
override this behavior and control the sidebar on a per-page basis, use the
`Sphinx html-sidebars configuration value <https://www.sphinx-doc.org/en/master/usage/configuration.html?highlight=html_sidebars#confval-html_sidebars>`_.


Configure the navigation depth and collapsing of the sidebar
============================================================

By default, this theme enables to expand/collapse subsections in the left
sidebar navigation (without actually navigating to the page itself), and this extends
up to 4 levels deep:

.. image:: /_static/demo-expandable-navigation.gif

When having a site with many files and/or many levels, this can cause a long
build time and larger HTML file sizes. Therefore, it is possible to turn off
the expandable navigation by setting the `collapse_navigation` config option
to True:

.. code:: python

   html_theme_options = {
     "collapse_navigation": True
   }

In addition, you can also control how many levels of the navigation are shown
in the sidebar (with a default of 4):

.. code:: python

   html_theme_options = {
     "navigation_depth": 2
   }



Hiding the previous and next buttons
====================================

By default, each page of your site will have "previous" and "next" buttons
at the bottom. You can hide these buttons with the following configuration:

.. code:: python

   html_theme_options = {
     "show_prev_next": False
   }


Add an Edit this Page button
============================

You can add a button to each page that will allow users to edit the page text
directly and submit a pull request to update the documentation. To include this
button in the right sidebar of each page, add the following configuration to
your ``conf.py`` file in 'html_theme_options':

.. code:: python

   html_theme_options = {
       "use_edit_page_button": True,
   }

A number of providers are available for building *Edit this Page* links, including
GitHub, GitLab, and Bitbucket. For each, the default public instance URL can be
replaced with a self-hosted instance.


GitHub
------

.. code:: python

   html_context = {
       # "github_url": "https://github.com", # or your GitHub Enterprise interprise
       "github_user": "<your-github-org>",
       "github_repo": "<your-github-repo>",
       "github_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


GitLab
------

.. code:: python

   html_context = {
       # "gitlab_url": "https://gitlab.com", # or your self-hosted GitLab
       "gitlab_user": "<your-gitlab-org>",
       "gitlab_repo": "<your-gitlab-repo>",
       "gitlab_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


Bitbucket
---------

.. code:: python

   html_context = {
       # "bitbucket_url": "https://bitbucket.org", # or your self-hosted Bitbucket
       "bitbucket_user": "<your-bitbucket-org>",
       "bitbucket_repo": "<your-bitbucket-repo>",
       "bitbucket_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


Custom Edit URL
---------------

For a fully-customized *Edit this Page* URL, provide ``edit_page_url_template``,
a jinja2 template string which must contain ``{{ file_name }}``, and may reference
any other context values.

.. code:: python

   html_context = {
       "edit_page_url_template": "{{ my_vcs_site }}{{ file_name }}{{ some_other_arg }}",
       "my_vcs_site": "https://example.com",
       "some_other_arg": "?some-other-arg"
   }


Configure the search bar position
=================================

To modify the position of the search bar, add the ``search-field.html``
template to your **sidebar**, or to one of the **navbar** positions, depending
on where you want it to be placed.

For example, if you'd like the search field to be in your side-bar, add it to
the sidebar templates like so:

.. code:: python

    html_sidebars = {
        "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
    }

If instead you'd like to put the search bar in the top navbar, use the
following configuration:

.. code:: python

   html_theme_options = {
       "navbar_end": ["navbar-icon-links.html", "search-field.html"]
   }


.. note::

   By default the search bar is positioned in the sidebar since this is more
   suitable for large navigation bars.

Configure the search bar text
=============================

To modify the text that is in the search bar before people click on it, add the
following configuration to your ``conf.py`` file:

.. code:: python

   html_theme_options = {
       "search_bar_text": "Your text here..."
   }


Google Analytics
================

If the ``google_analytics_id`` config option is specified (like ``UA-XXXXXXX``),
Google Analytics' javascript is included in the html pages.

.. code:: python

   html_theme_options = {
       "google_analytics_id": "UA-XXXXXXX",
   }


Changing pages with keyboard presses
====================================

By default, ``pydata-sphinx-theme`` allows users to move to the previous/next
page using the left/right arrow keys on a keyboard. To disable this behavior,
use the following configuration:

.. code-block:: python

   html_theme_options = {
     "navigation_with_keys": False
   }


Show more levels of the in-page TOC by default
==============================================

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


Remove the sidebar from some pages
==================================

If you'd like the left sidebar to be removed from a page, you can use the
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

If you'd like to remove the left sidebar from **all** pages of your documentation,
use this pattern:

.. code-block:: python

   html_sidebars = {
     "**": []
   }

For information about configuring the sidebar's contents, see :ref:`configure-sidebar`.


Configure the navbar center alignment
=====================================

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

Adding ethical advertisements to your sidebar in ReadTheDocs
============================================================

If you're hosting your documentation on ReadTheDocs, you should consider
adding an explicit placement for their **ethical advertisements**. These are
non-tracking advertisements from ethical companies, and they help ReadTheDocs
sustain themselves and their free service.

Ethical advertisements are added to your sidebar by default. To ensure they are
there if you manually update your sidebar, ensure that the ``sidebar-ethical-ads.html``
template is added to your list. For example:

.. code:: python

   html_sidebars = {
       "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
   }


.. meta::
   :description lang=en:
       Configuration options for pydata-sphinx-theme
