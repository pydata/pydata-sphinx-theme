Announcement banners
====================

You can add an announcement banner that draws extra attention from your reader.
It will be displayed at the top of the screen but will disappear once they start scrolling.

To add an announcement banner, use the ``html_theme_options["announcement"]`` configuration.
There are two ways to use this.

Provide local HTML in your theme
--------------------------------

By default, the value of your ``html_theme_options["announcement"]`` will be inserted directly into your announcement banner as raw HTML.

For example, the following configuration adds a simple announcement.

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
      ...
      "announcement": "Here's a <a href='https://pydata.org'>PyData Announcement!</a>",
   }

Insert remote HTML with JavaScript
----------------------------------

You can specify an arbitrary URL that will be used as the HTML source for your announcement.
When the page is loaded, JavaScript will attempt to fetch this HTML and insert it as-is into the announcement banner.
This allows you to define a single HTML announcement that you can pull into multiple documentation sites or versions.

If the value of ``html_theme_options["announcement"]`` begins with **``http``** it will be treated as a URL to remote HTML.

For example, the following configuration tells the theme to load the ``custom-template.html`` example from this documentation's GitHub repository:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
      ...
      "announcement": "https://github.com/pydata/pydata-sphinx-theme/raw/main/docs/_templates/custom-template.html",
   }


.. _version-warning-banners:

Version warning banners
-----------------------

In addition to the general-purpose announcement banner, the theme includes a built-in banner to warn users when they are viewing versions of your docs other than the latest stable version. To use this feature, add the following to your ``conf.py``:

.. code-block:: python
    :caption: conf.py

    html_theme_options = {
        ...
        "show_version_warning_banner": True,
    }
.. warning::

    This functionality relies on the :ref:`version switcher <version-dropdowns>` to determine the version number of the latest stable release.
    *It will only work* if your version switcher ``.json`` has exactly one entry with property ``"preferred": true``
    and a ``name`` property that begins with a version string that is parsable by the `compare-versions node module <https://www.npmjs.com/package/compare-versions>`__, for example:

    .. code-block:: json

        {
            "name": "9.9.9 (current)",
            "version": "stable",
            "url": "https://anything"
        }
