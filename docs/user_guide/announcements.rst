Announcement banners
====================

You can add an announcement banner that draws extra attention from your reader.
It will be displayed at the top of the screen, but will disappear once they start scrolling.

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
