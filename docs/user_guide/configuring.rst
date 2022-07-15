.. _configuration:

*************
Configuration
*************

There are a number of options for configuring your site's look and feel.
All configuration options are passed with the ``html_theme_options`` variable
in your ``conf.py`` file. This is a dictionary with ``key: val`` pairs that
you can configure in various ways. This page describes the options available to you.

Customize logo and title
========================

By default the theme will use the value of ``project`` on the left side of the header navbar.
This can be replaced by a Logo image, and optionally a custom ``html_title`` as well.

Single logo for light and dark mode
-----------------------------------

To use a local image file, put an image in a folder that is in `html_static_path`, and use the following configuration:

.. code:: python

   html_static_path = ["_static"]
   html_logo = "_static/logo.png"

To use an external link to an image, make sure the ``html_logo`` begins with ``http``.
For example:

.. code:: python

   html_logo = "https://pydata.org/wp-content/uploads/2019/06/pydata-logo-final.png"

Different logos for light and dark mode
---------------------------------------

You may specify use a different version of your logo image for "light" and "dark" modes.
This is useful if your logo image is not adapted to a dark mode (light background, not enough contrast, etc...).

To do so, put the 2 image files in a folder that is in ``html_static_path`` and configure the relative path to each image with ``logo.image_light`` and ``logo.image_dark`` in ``html_theme_options``, like so:

.. code-block:: python

   html_static_path = ["_static"]
   html_theme_options = {
      "logo": {
         "image_light": "logo-light.png",
         "image_dark": "logo-dark.png",
      }
   }

.. note::

   ``image_light`` and ``image_dark`` will override the ``html_logo`` setting. If you only specify one of them, but not the other, then the un-specified setting will re-use ``html_logo``.

Customize logo link
-------------------

The logo links to ``root_doc`` (usually the first page of your documentation) by default.
You can instead link to a local document or an external website.
To do so, use the ``html_theme_options["logo"]["link"]`` option and provide a new link.

For example, to reference another local page:

.. code-block:: python

   html_theme_options = {
       "logo": {
           "link": "some/other-page",
       }
   }

To reference an external website, make sure your link starts with ``http``:

.. code-block:: python

   html_theme_options = {
       "logo": {
           "link": "https://pydata.org",
       }
   }

Add a logo title
----------------

To add a title in the brand section of your documentation, define a value for ``html_theme_options.logo["text"]``
This will appear just after your logo image if it is set.

.. code-block:: python

   html_theme_options = {
       "logo": {
           "text": "My awesome documentation",
       }
   }

.. note:: The ``html_title`` field will work as well if no logo images are specified.


Configure default theme mode
============================

By default, visitors to your documentation will use the theme mode ``auto``.
This will choose a theme based on the user's system settings, and default to ``light`` if not settings are present.

If you wish to use a different default theme mode, set the ``default_mode`` configuration to one of ``auto``, ``dark``, ``light``.
For example:

.. code-block:: python

   html_context = {
      # ...
      "default_mode": "light"
   }

For more information, see :ref:`manage-themes`.

.. tip::

   To completely remove the theme management, configure ``default_mode`` to the value you want in your documentation (``light`` or ``dark``) and then remove the theme-switcher from the ``navbar_end`` section of the header navbar configuration:

   .. code-block:: python

      html_theme_options {
          # ...
          # Note we have omitted `theme-switcher` below
          "navbar_end": ["navbar-icon-links"]
      }

Configure pygment theme
=======================

As the Sphinx theme supports multiple modes, the code highlighting colors can be modified for each one of them by modifying the ``pygment_light_style`` and ``pygment_dark_style``. You can check available Pygments colors on this `page <https://help.farbox.com/pygments.html>`__.

.. code-block:: python

   html_theme_options = {
      ...
      "pygment_light_style": "tango",
      "pygment_dark_style": "native"
   }

.. danger::

   The native Sphinx option ``pygments_style`` will be overwritten by this theme.

Announcement banners
====================

You can add an announcement banner that draws extra attention from your reader.
It will be displayed at the top of the screen, but will disappear once you start scrolling.

To add an announcement banner, use the ``html_theme_options["announcement"]`` configuration.
There are two ways to use this.

Provide local HTML in your theme
--------------------------------

By default, the value of your ``html_theme_options["announcement"]`` will be inserted directly into your announcement banner as raw HTML.

For example, the following configuration adds a simple ``<p>`` with an announcement.

.. code-block:: python

   html_theme_options = {
      ...
      "announcement": "<p>Here's a <a href='https://pydata.org'>PyData Announcement!</a></p>",
   }

Insert remote HTML with JavaScript
----------------------------------

You can specify an arbitrary URL that will be used as the HTML source for your announcement.
When the page is loaded, JavaScript will attempt to fetch this HTML and insert it as-is into the announcement banner.
This allows you to define a single HTML announcement that you can pull into multiple documentation sites or versions.

If the value of ``html_theme_options["announcement"]`` begins with **``http``** it will be treated as a URL to remote HTML.

For example, the following configuration tells the theme to load the ``custom-template.html`` example from this documentation's GitHub repository:

.. code-block:: python

   html_theme_options = {
      ...
      "announcement": "https://github.com/pydata/pydata-sphinx-theme/raw/main/docs/_templates/custom-template.html",
   }

.. _icon-links:

Configure icon links
====================

You can add icon links to show up to the right of your main navigation bar.

These links take the following form:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               # Label for this link
               "name": "GitHub",
               # URL where the link will redirect
               "url": "https://github.com/<your-org>/<your-repo>",  # required
               # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
               "icon": "fab fa-github-square",
               # The type of image to be used (see below for details)
               "type": "fontawesome",
           }
      ]
   }

There are two kinds of icons you can use, described below:

FontAwesome icons
-----------------

`FontAwesome <https://fontawesome.com/>`_ is a collection of icons that are
commonly used in websites. They include both generic shape icons (e.g., "arrow-down"),
as well as brand-specific icons (e.g. "github").

You can use FontAwesome icons by specifying ``"type": "fontawesome"``, and
specifying a FontAwesome class in the ``icon`` value.
The value of ``icon`` can be any full
`FontAwesome 5 Free <https://fontawesome.com/icons?d=gallery&m=free>`__ icon.
In addition to the main icon class, e.g. ``fa-cat``, the "style" class must
also be provided e.g. `fab` for *branding*, or `fas` for *solid*.

Here are several examples:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/<your-org>/<your-repo>",
               "icon": "fab fa-github-square",
               "type": "fontawesome",
           },
           {
               "name": "GitLab",
               "url": "https://gitlab.com/<your-org>/<your-repo>",
               "icon": "fab fa-gitlab",
               "type": "fontawesome",
           },
           {
               "name": "Twitter",
               "url": "https://twitter.com/<your-handle>",
               "icon": "fab fa-twitter-square",
               # The default for `type` is `fontawesome` so it is not actually required in any of the above examples as it is shown here
           },
           {
               "name": "Mastodon",
               "url": "https://<your-host>@<your-handle>",
               "icon": "fab fa-mastodon",
               "attributes": {
                  "target" : "_blank",
                  "rel" : "noopener me",
               }
           },
       ],
       ...
   }

.. Hint::

   To get custom colors like "Twitter blue", use the following in your CSS,
   e.g. ``custom.css``:

   .. code:: css

      i.fa-twitter-square:before {
         color: #55acee;
      }

   This has already been added for the brands that have *shortcuts*.

Image icons
-----------

If you'd like to display an icon image that is not in the FontAwesome icons library,
you may instead specify a URL or a path to a local image that will be used for the icon.

**To display an image on the web**, use ``"type": "url"``, and provide a URL to an image in the ``icon`` value.
For example:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "Pandas",
               "url": "https://pandas.pydata.org",
               "icon": "https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/main/docs/_static/pandas-square.svg",
               "type": "url",
           },
       ],
       ...
   }


**To display a local image from a file path**, use ``"type": "local"``, and add a path to an image
relative to your documentation root in the ``icon`` value.
For example:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "PyData",
               "url": "https://pydata.org",
               "icon": "_static/pydata-logo-square.png",
               "type": "local",
           },
       ],
       ...
   }

.. tip::

   Use ``.svg`` images for a higher-resolution output that behaves similarly across screen sizes.

Icon Link Shortcuts
-------------------

There are a few shortcuts supported to minimize configuration for commonly-used services.
These may be removed in a future release in favor of ``icon_links``:

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

Add custom attributes to icon links
-----------------------------------

You can add custom attributes to the link element (``<a>``) of your icon links.
This is helpful if you need to add custom link behavior.
To do so, use the pattern ``"attributes": {"attribute1": "value1"}`` in a given icon link entry.

For example, to specify a custom ``target`` and ``rel`` attribute, and to define your own custom link classes:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "PyData",
               "url": "https://pydata.org",
               "icon": "_static/pydata-logo-square.png",
               "type": "local",
               # Add additional attributes to the href link.
               # The defaults of target, rel, class, title and href may be overwritten.
               "attributes": {
                  "target" : "_blank",
                  "rel" : "noopener me",
                  "class": "nav-link custom-fancy-css"
               }
           },
       ],
       ...
   }

.. warning::
   This might make your icon links behave unexpectedly and might over-ride default behavior, so make sure you know what you're doing!

Header Navigation Bar
=====================

The header navigation bar is at the top of each page and contains top-level navigation across pages in your documentation, as well as extra links and components that you can add.
These sections cover a few things you can control with the Header Navigation Bar.

Add external links
------------------

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


Header dropdown links
---------------------

By default, this theme will display the first **five** navigation links in the header (including both top-level links and external links).
It will place the remaining header links in a **dropdown menu** titled "More".
This prevents the header links from taking up so much space that they crowd out the UI components or spill off screen.

To control how many header links are displayed before being placed in the dropdown, use the ``header_links_before_dropdown`` theme configuration variable.
For example, to change the number of displayed header links to be ``4`` instead of ``5``:abbr:

.. code-block:: python

   html_theme_options = {
     "header_links_before_dropdown": 4
   }

Add favicons
============

``pydata_sphinx_theme`` supports the `standard sphinx favicon configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_favicon>`_, using ``html_favicon``.

Additionally you may add any number of browser- or device-specific favicons of any size.
To do so, use the ``html_theme_options["favicons"]`` configuration key.
The only required argument is ``href``, which can be either an absolute URL (beginning with ``http``) or a local path relative to your ``html_static_path``.
In addition, you may specify a size with ``sizes``, specify a ``rel`` value, and specify a ``color``.
See `this blog post on SVG favicons for more information <https://medium.com/swlh/are-you-using-svg-favicons-yet-a-guide-for-modern-browsers-836a6aace3df>`_.

For example, below we define three extra favicons of different sizes and ``rel`` types, and one with a specific color.

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
            "href": "apple-touch-icon-180x180.png",
            "color": "#000000",
         },
      ]
   }

``pydata_sphinx_theme`` will add ``link`` tags to your document's ``head``
section, following this pattern:

.. code-block:: html+jinja

   <link rel="{{ favicon.rel }}" sizes="{{ favicon.sizes }}" href="{{ favicon.href }}" color="{{ favicon.color }}">


.. _configure-sidebar:

Configure the sidebar
=====================

``pydata_sphinx_theme`` provides two sidebar items by default:

- ``sidebar-nav-bs.html`` - a bootstrap-friendly navigation section.

   When there are no pages to show, it will disappear and potentially add extra space for your page's content.

- ``sidebar-ethical-ads.html`` - a placement for ReadTheDocs's Ethical Ads (will only show up on ReadTheDocs).

If you'd like to override this behavior and add / remove different components, or control the sidebar on a per-page basis, use the `Sphinx html-sidebars configuration value <https://www.sphinx-doc.org/en/master/usage/configuration.html?highlight=html_sidebars#confval-html_sidebars>`_.

.. _navigation-depth:

Navigation depth and collapsing the sidebar
===========================================

By default, this theme enables to expand/collapse subsections in the left
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

.. note::

   In some Sphinx sites, the top-level ``toctree`` groupings make up "parts" in the documentation, with
   each page beneath making up a "chapter".

.. _remove_toctrees:

Selectively remove pages from your sidebar
------------------------------------------

.. note::

   This and the following sections are useful for sites that have a lot of pages (such as API
   documentation with a lot of items). These take much longer to build and will have large
   output sizes because of all the toctree links. These sections help with this problem,
   ordered from least-to-most drastic.

You can prevent pages from showing up in the navigation bar using a Sphinx
extension called `sphinx-remove-toctrees <https://github.com/executablebooks/sphinx-remove-toctrees>`_.
This is useful if your documentation generates lots of "stub pages" in a folder,
which is common with API documentation.

This lets you add a configuration like so:

.. code-block::

   remove_from_toctrees = ["folder_one/generated/*"]

and any pages that are inside of ``folder_one/generated/`` will not show up in the sidebar.

Check out the `sphinx-remove-toctrees documentation <https://github.com/executablebooks/sphinx-remove-toctrees#install>`_
for information about how to install and use this extension.

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


Hiding the previous and next buttons
====================================

By default, each page of your site will have "previous" and "next" buttons
at the bottom. You can hide these buttons with the following configuration:

.. code:: python

   html_theme_options = {
     "show_prev_next": False
   }


Add a dropdown to switch between docs versions
==============================================

You can add a button to your site that allows users to
switch between versions of your documentation. The links in the version
switcher will differ depending on which page of the docs is being viewed. For
example, on the page ``https://mysite.org/en/v2.0/changelog.html``, the
switcher links will go to ``changelog.html`` in the other versions of your
docs. When clicked, the switcher will check for the existence of that page, and
if it doesn't exist, redirect to the homepage of that docs version instead.

The switcher requires the following configuration steps:

1. Add a JSON file containing a list of the documentation versions that the
   switcher should show on each page.

2. Add a configuration dictionary called ``switcher`` to the
   ``html_theme_options`` dict in ``conf.py``. ``switcher`` should have 2 keys:

   - ``json_url``: the persistent location of the JSON file described above.
   - ``version_match``: a string stating the version of the documentation that
     is currently being browsed.

3. Specify where to place the switcher in your page layout. For example, add
   the ``"version-switcher"`` template to one of the layout lists in
   ``html_theme_options`` (e.g., ``navbar_end``, ``footer_items``, etc).

Below is a more in-depth description of each of these configuration steps.


Add a JSON file to define your switcher's versions
--------------------------------------------------

First, write a JSON file stating which versions of your docs will be listed in
the switcher's dropdown menu. That file should contain a list of entries that
each can have the following fields:

- ``version``: a version string. This is checked against
  ``switcher['version_match']`` to provide styling to the switcher.
- ``url``: the URL for this version.
- ``name``: an optional name to display in the switcher dropdown instead of the
  version string (e.g., "latest", "stable", "dev", etc).

Here is an example JSON file:

.. code:: json

    [
        {
            "name": "v2.1 (stable)",
            "version": "2.1",
            "url": "https://mysite.org/en/2.1/index.html"
        },
        {
            "version": "2.1rc1",
            "url": "https://mysite.org/en/2.1rc1/index.html"
        },
        {
            "version": "2.0",
            "url": "https://mysite.org/en/2.0/index.html"
        },
        {
            "version": "1.0",
            "url": "https://mysite.org/en/1.0/index.html"
        }
    ]

See the discussion of ``switcher['json_url']`` (below) for options of where to
save the JSON file.


Configure ``switcher['json_url']``
----------------------------------

The JSON file needs to be at a stable, persistent, fully-resolved URL (i.e.,
not specified as a path relative to the sphinx root of the current doc build).
Each version of your documentation should point to the same URL, so that as new
versions are added to the JSON file all the older versions of the docs will
gain switcher dropdown entries linking to the new versions. This could be done
a few different ways:

- The location could be one that is always associated with the most recent
  documentation build (i.e., if your docs server aliases "latest" to the most
  recent version, it could point to a location in the build tree of version
  "latest"). For example:

  .. code:: python

      html_theme_options = {
          ...,
          "switcher": {
              "json_url": "https://mysite.org/en/latest/_static/switcher.json",
          }
      }

  In this case the JSON is versioned alongside the rest of the docs pages but
  only the most recent version is ever loaded (even by older versions of the
  docs).

- The JSON could be saved in a folder that is listed under your site's
  ``html_static_path`` configuration. See `the Sphinx static path documentation
  <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path>`_
  for more information.

- The JSON could be stored outside the doc build trees. This probably means it
  would be outside the software repo, and would require you to add new version
  entries to the JSON file manually as part of your release process. Example:

  .. code:: python

      html_theme_options = {
          ...,
          "switcher": {
              "json_url": "https://mysite.org/switcher.json",
          }
      }


Configure ``switcher['version_match']``
---------------------------------------

This configuration value tells the switcher what docs version is currently
being viewed, and is used to style the switcher (i.e., to highlight the current
docs version in the switcher's dropdown menu, and to change the text displayed
on the switcher button).

Typically you can re-use one of the sphinx variables ``version``
or ``release`` as the value of ``switcher['version_match']``; which one you use
depends on how granular your docs versioning is. See
`the Sphinx "project info" documentation
<https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information>`__
for more information). Example:

.. code:: python

    version = my_package_name.__version__.replace("dev0", "")  # may differ
    html_theme_options = {
        ...,
        "switcher": {
            "version_match": version,
        }
    }


Specify where to display the switcher
-------------------------------------

Finally, tell the theme where on your site's pages you want the switcher to
appear. There are many choices here: you can add ``"version-switcher"`` to one
of the locations in ``html_theme_options`` (e.g., ``navbar_end``,
``footer_items``, etc). For example:

.. code:: python

   html_theme_options = {
      ...,
      "navbar_start": ["navbar-logo", "version-switcher"]
   }


Alternatively, you could override one of the other templates to include the
version switcher in a sidebar. For example, you could define
``_templates/sidebar-nav-bs.html`` as:

.. code:: jinja

    {%- include 'version-switcher.html' -%}
    {{ super() }}

to insert a version switcher at the top of the left sidebar, while still
keeping the default navigation below it. See :doc:`sections` for more
information.

Style the switcher buttons
--------------------------

You may apply styles via CSS to any of the switcher buttons to control their look and feel.
Each button has two `HTML dataset entries <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset>`_
that you can use to apply CSS rules to subsets of buttons. These entries are:

.. code-block::

   data-version
   data-version-name

For example, the link for an entry with ``version="0.2"``,
and ``name="My version"`` would have metadata like so:

.. code-block:: html

   <a data-version-name="My version" data-version="0.2" class="<classes...>">

You can create CSS rules that select this metadata like so:

.. code-block:: scss

   // Style all links with a specific subset of versions
   #version_switcher a[data-version="0.2"],
   #version_switcher a[data-version="0.3"] {
      background-color: red;
   }
   // Style all links with `stable` in the version name
   #version_switcher a[data-version-name*="stable"] {
      background-color: green;
   }

In addition, the parent button of the dropdown list contains similar metadata
about the **current version**. This could be used to style the entire dropdown
a certain color based on the active version.

For example, if you wanted to style the dropdown button to use the theme's secondary color (PyData orange by default) if it was a ``dev``
version, you could use the following CSS selector:

.. code-block:: scss

   // If the active version has the name "dev", style it orange
   #version_switcher_button[data-active-version-name*="dev"] {
      background-color: var(--pst-color-secondary);
   }

.. seealso::

   See the `MDN documentation on dataset properties <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset>`_
   for more information on using and styling with these properties.

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

Search bar / search button
==========================

By default, the search input field is hidden, and there is a search button
(a magnifying glass icon :fas:`search`) in the top navbar.
The search input field will be displayed when a user either:

- Clicks the search button in the header.
- Presses the keyboard shortcut :kbd:`Ctrl` + :kbd:`K` (Linux, Windows) or :kbd:`⌘` + :kbd:`K` (macOS).

You can also configure some aspects of the search button and search field, described below.

Configure the search field position
-----------------------------------

The position of the search *button* is controlled by ``search-button`` and by default is included in ``html_theme_options["navbar_end"]``; you may move it elsewhere as befits your site's layout, or remove it. You can also add an always-visible search field to some/all pages in your site by adding ``search-field.html`` to one of the configuration variables (e.g., ``html_sidebars``, ``html_theme_options["footer_items"]``, etc).

For example, if you'd like the search field to be in your side-bar, add it to
the sidebar templates like so:

.. code:: python

    html_sidebars = {
        "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
    }

If instead you'd like to put the search field in the top navbar, use the
following configuration:

.. code:: python

   html_theme_options = {
       "navbar_end": ["navbar-icon-links.html", "search-field.html"]
   }

.. warning::

    If a page includes *both* the search button and an always-visible search field, the keyboard shortcuts will focus the always-visible field and the hidden search field overlay will not display. *This may not be what you want:* on small screens (i.e. mobile devices) the sidebars may be hidden in a drawer, and if the persistent search field is there, it may receive focus without actually being made visible. It is **strongly recommended** that you use *either* search button and the hidden/overlaid field that comes with it, *or* use a persistent search field in a place that makes sense for your layout.


Configure the search bar text
-----------------------------

To modify the text that is in the search bar before people click on it, add the
following configuration to your ``conf.py`` file:

.. code:: python

   html_theme_options = {
       "search_bar_text": "Your text here..."
   }


Google Analytics
================

If the ``google_analytics_id`` config option is specified (like ``G-XXXXXXXXXX``),
Google Analytics' javascript is included in the html pages.

.. code:: python

   html_theme_options = {
       "google_analytics_id": "G-XXXXXXXXXX",
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

Secondary Sidebar (Table of Contents)
=====================================

The secondary sidebar is to the right of your documentation content.
It is primarily for showing a within-page Table of Contents, as well as links that point to the source of the page.


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

To remove the Table of Contents, add ``:theme_html_remove_secondary_sidebar:`` to the `file-wide metadata <https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#file-wide-metadata>`_ at the top of a page.
This will remove the Table of Contents from that page only.

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

Improve build speed and performance
===================================

By default this theme includes all of your documentation links in a collapsible sidebar.
However, this may slow down your documentation builds considerably if you have
a lot of documentation pages. This is most common with documentation for projects
with a large API, which use the ``.. autosummary::`` directive to generate
API documentation.

To improve the performance of your builds in these cases, see :ref:`navigation-depth`.
