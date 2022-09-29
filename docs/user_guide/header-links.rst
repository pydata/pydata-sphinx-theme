============
Header links
============

The header navigation bar is at the top of each page and contains top-level navigation across pages in your documentation, as well as extra links and components that you can add.
These sections cover a few things you can control with the Header Navigation Bar.

Navigation Bar External links
=============================

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


Navigation bar dropdown links
=============================

By default, this theme will display the first **five** navigation links in the header (including both top-level links and external links).
It will place the remaining header links in a **dropdown menu** titled "More".
This prevents the header links from taking up so much space that they crowd out the UI components or spill off screen.

To control how many header links are displayed before being placed in the dropdown, use the ``header_links_before_dropdown`` theme configuration variable.
For example, to change the number of displayed header links to be ``4`` instead of ``5``:abbr:

.. code-block:: python

   html_theme_options = {
     "header_links_before_dropdown": 4
   }

.. _icon-links:

Icon links
==========

Icon links are a collection of images and icons that each link to a page or external site.
They are helpful if you wish to display social media icons, GitHub badges, or project logos.

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
               "icon": "fa-brands fa-square-github",
               # The type of image to be used (see below for details)
               "type": "fontawesome",
           }
      ]
   }


Additionally, the screen-reader accessible label for this menu can be configured:

.. code:: python

   html_theme_options = {
       ...
       "icon_links_label": "Quick Links",
       ...
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
`FontAwesome 6 Free <https://fontawesome.com/icons?d=gallery&m=free>`__ icon.
In addition to the main icon class, e.g. ``fa-cat``, the "style" class must
also be provided e.g. `fa-brands` for *branding*, or `fa-solid` for *solid*.

Here are several examples:

.. code:: python

   html_theme_options = {
       ...
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/<your-org>/<your-repo>",
               "icon": "fa-brands fa-square-github",
               "type": "fontawesome",
           },
           {
               "name": "GitLab",
               "url": "https://gitlab.com/<your-org>/<your-repo>",
               "icon": "fa-brands fa-square-gitlab",
               "type": "fontawesome",
           },
           {
               "name": "Twitter",
               "url": "https://twitter.com/<your-handle>",
               "icon": "fa-brands fa-square-twitter",
               # The default for `type` is `fontawesome` so it is not actually required in any of the above examples as it is shown here
           },
           {
               "name": "Mastodon",
               "url": "https://<your-host>@<your-handle>",
               "icon": "fa-brands fa-mastodon",
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

   This has already been added for the brands that have *shortcuts* (:ref:`see below <icon-link-shortcuts>`).

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

.. _icon-link-shortcuts:

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
