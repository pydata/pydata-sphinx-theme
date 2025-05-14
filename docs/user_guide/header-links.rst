============
Header links
============

The header navigation bar is at the top of each page and contains top-level navigation across pages in your documentation, as well as extra links and components that you can add.
These sections cover a few things you can control with the Header Navigation Bar.

Navigation Bar External links
=============================

You can add external links to your navigation bar. These will show up to the right
of your site's main links and will have a small icon indicating that they point to
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
This prevents the header links from taking up so much space that they crowd out the UI components or spill off-screen.

To control how many header links are displayed before being placed in the dropdown, use the ``header_links_before_dropdown`` theme configuration variable.
For example, to change the number of displayed header links to be ``4`` instead of ``5``:

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
and brand-specific icons (e.g. "GitHub").

You can use FontAwesome icons by specifying ``"type": "fontawesome"``, and
specifying a FontAwesome class in the ``icon`` value.
The value of ``icon`` can be any full
`FontAwesome 6 Free <https://fontawesome.com/search?o=r&m=free>`__ icon.
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
               # The default for `type` is `fontawesome`, so it is not required in the above examples
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

      svg.fa-square-twitter {
         color: #55acee;
      }

Image icons
-----------

If you'd like to display an icon image that is not in the FontAwesome icons library,
you may instead specify a URL or a path to a local image that will be used for the icon.
You may also use ``.svg`` images as if they were FontAwesome with a little additional setup.

Bitmap image icons
~~~~~~~~~~~~~~~~~~

For all bitmap image icons such as ``.png``, ``.jpg``, etc., you must specify ``type`` as local.

.. note::

    All icon images with ``"type": "local"`` are inserted into the document using ``<img>`` tags.
    If you need features specific to objects in the ``svg`` class please see :ref:`svg image icons <svg-image-icons>`

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

.. _svg-image-icons:

SVG image icons
~~~~~~~~~~~~~~~

In order to make use of the full feature set of ``.svg`` images provided by HTML you will need
to set up the ``.svg`` to be used as a FontAwesome type icon. This is a fairly straightforward process:

#. Copy `custom-icons.js`_ into an appropriate directory of your documentation
   source (typically ``source/js``). In that file you will find a list of custom
   icon definitions. Each definition looks like this:

   .. code:: javascript

     {
       prefix: "fa-custom",
       iconName: "pypi",
       icon: [
         17.313, // viewBox width
         19.807, // viewBox height
         [], // ligature
         "e001", // unicode codepoint - private use area
         "m10.383 0.2-3.239 ...", // svg path
       ],
     }

#. Remove the existing list of icon definitions and add your own using the same pattern as above:

   #.  Keep the value of ``prefix`` as "fa-custom"
   #.  Set the value of ``iconName``  to a short, sensible, lowercase name for your icon
   #.  Change the view box height and width to match that of your icon
   #.  For each custom icon you define in the list, increment the Unicode codepoint by 1: ``"e001"``, ``"e002"``, ``"e003"``...
   #.  Replace the SVG path string with the path that defines your custom icon

#. In ``conf.py``, add the relative path from your source directory to the custom javascript file:

   .. code:: python

      html_js_files = [
         ...
         ("js/custom-icons.js", {"defer": "defer"}),
         ...
      ]

   .. versionchanged:: v0.17.0

      ``defer`` attribute is required.

   .. important::

      Do not add more than one ``custom-icons.js`` file in your ``conf.py``.

      Each custom icon js file includes a call to ``FontAwesome.library.add()``.
      Your site's JavaScript can only call that function once. In our testing,
      subsequent calls to that function do not load additional icons.

#. Set up the icon link in the ``html_theme_options`` as a FontAwesome icon:

   .. code:: python

      html_theme_options = [
         ...
         "icon_links": [
            {
               "name": "PyPI",
               "url": "https://www.pypi.org",
               "icon": "fa-custom fa-pypi",
               "type": "fontawesome",
            },
         ],
         ...
      ]

That's it, your icon will now be inserted with the ``<svg>`` tag and not ``<img>``! You can reference your custom FontAwesome icon in CSS using the pattern ``.fa-<iconName>`` , for example ``.fa-pypi``.

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

For example, to specify a custom ``target`` and ``rel`` attribute, and to define your custom link classes:

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
               # The defaults of the target, rel, class, title, and href may be overwritten.
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
   This might make your icon links behave unexpectedly and might override the default behavior, so make sure you know what you're doing!

.. _custom-icons.js: ../_static/custom-icons.js
