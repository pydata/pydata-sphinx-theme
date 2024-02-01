=================
Branding and logo
=================

Customize logo and title
========================

By default, the theme will use the value of ``project`` on the left side of the header navigation bar.
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

Logo title and alternative text
-------------------------------

If you provide a logo image, it replaces ``project`` or ``html_title`` in the
header nav bar. If you want to display both your site's logo and title (or any
other text) next to the logo, you provide it with the ``text`` property like so:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
       "logo": {
           "text": "My awesome documentation",
           "image_light": "_static/logo-light.png",
           "image_dark": "_static/logo-dark.png",
       }
   }

But if you only want to display the logo and not the site title, then it's good
practice to provide alt text, which helps blind visitors and others who rely on
screen readers:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
       "logo": {
           # Because the logo is also a homepage link, including "home" in the
           # alt text is good practice
           "alt_text": "My awesome documentation - Home",
           "image_light": "_static/logo-light.png",
           "image_dark": "_static/logo-dark.png",
       }
   }

In most cases, you will provide either ``text`` or ``alt_text``, not both, but
there are some circumstances in which it may make sense to provide both:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
       "logo": {
           # In a left-to-right context, screen readers will read the alt text
           # first, then the text, so this example will be read as "P-G-G-P-Y
           # (short pause) Home A pretty good geometry package"
           "alt_text": "PggPy - Home",
           "text": "A pretty good geometry package",
           "image_light": "_static/logo-light.png",
           "image_dark": "_static/logo-dark.png",
       }
   }

If you do not provide ``text`` or ``alt_text``, the theme will provide some
default alt text (otherwise, your homepage link would appear to assistive tech
as something like "Unlabeled image"). The default alt text is "`docstitle
<https://www.sphinx-doc.org/en/master/development/templating.html#docstitle>`_ -
Home", but if you provide a logo title (``text``) the default alt text will be an
empty string (the assumption is that if you provide a logo title, the title is
probably doing the work of the alt text, and as shown above, you can override
this assumption by supplying both ``text`` and ``alt_text``).

Add favicons
============

``pydata_sphinx_theme`` supports the `standard sphinx favicon configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_favicon>`_, using ``html_favicon``.
Support for complex and multiple favicons was dropped in version 0.15.3. Instead, use the `sphinx-favicon <https://sphinx-favicon.readthedocs.io/en/stable/>`__ extension.
It provides the same functionality using more flexible parameters.
