=================
Branding and logo
=================

Customize logo and title
========================

By default the theme will use the value of ``project`` on the left side of the header navbar.
This can be replaced by a logo image, and optionally a custom ``html_title`` as well.

Single logo for light and dark mode
-----------------------------------

To use a **local image file**, use ``html_logo`` as specified in the `Sphinx documentation <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_logo>`__.
The file must be relative to ``conf.py``.
For example, if your documentation had a logo in ``_static/logo.png``:

.. code:: python

   html_logo = "_static/logo.png"

To use an **external link** to an image, make sure the ``html_logo`` begins with ``http``.
For example:

.. code:: python

   html_logo = "https://pydata.org/wp-content/uploads/2019/06/pydata-logo-final.png"

Different logos for light and dark mode
---------------------------------------

You may specify a different version of your logo image for "light" and "dark" modes.
This is useful if your logo image is not adapted to a dark mode (light background, not enough contrast, etc...).

To do so, use the ``logo["image_light"]`` and ``logo["image_dark"]`` options in ``html_theme_options``.
For each, provide a path relative to ``conf.py`` like so:

.. code-block:: python

   # Assuming your `conf.py` has a sibling folder called `_static` with these files
   html_theme_options = {
      "logo": {
         "image_light": "_static/logo-light.png",
         "image_dark": "_static/logo-dark.png",
      }
   }

.. note::

   ``image_light`` and ``image_dark`` will override the ``html_logo`` setting.
   If you only specify one of the light or dark variants, the un-specified variant will fall back to the value of ``html_logo``.

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

Customize logo alternative text
-------------------------------

You may set a custom ``alt text`` to use with your logo to replace the default ("logo image").
This can make the logo more accessible to those using screen readers or other assistive tech.
To do so, use ``html_teme_options["logo"]["alt_text"]`` as in the following example:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
       "logo": {
           "alt_text": "foo",
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
