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

If the value of ``html_theme_options["announcement"]`` begins with ``http`` it will be treated as a URL to remote HTML.

For example, the following configuration tells the theme to load the ``custom-template.html`` example from this documentation's GitHub repository:

.. code-block:: python
   :caption: conf.py

   html_theme_options = {
      ...
      "announcement": "https://github.com/pydata/pydata-sphinx-theme/raw/main/docs/_templates/custom-template.html",
   }

Update or remove announcement banner
------------------------------------

If you set ``html_theme_options["announcement"]`` to plain text or HTML, then to
update the announcement banner you need to modify this string and rebuild your
documentation pages. To remove the announcement banner, set this value to an
empty string and rebuild your documentation pages.

If you set ``html_theme_options["announcement"]`` to a URL string (starts with
``http``), then you can edit the file at that URL to update the announcement
banner. Saving an empty file at that URL will remove the announcement banner.
That's the main advantage of using a URL--you can change the announcement banner
without rebuilding and redeploying all of your documentation pages. For example,
if you point the announcement to the URL of a file in your repo, as we do on
this documentation site (see previous section), then you can edit, save and push
your changes to just that file (empty file = remove announcement) without
rebuilding and redeploying all your docs.

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

.. important::

    This functionality relies on the :ref:`version switcher <version-dropdowns>` to determine the version number of the latest stable release.
    *It will only work* if your version switcher ``.json`` has exactly one entry with property ``"preferred": true``
    and your entries have ``version`` properties that are parsable by the `compare-versions node module <https://www.npmjs.com/package/compare-versions>`__, for example:

    .. code-block:: json

        {
            "name": "stable",
            "version": "9.9.9",
            "url": "https://anything",
            "preferred": true
        }

If you want similar functionality for *older* versions of your docs (i.e. those built before the ``show_version_warning_banner`` configuration option was available), you can manually add a banner by prepending the following HTML to all pages (be sure to replace ``URL_OF_STABLE_VERSION_OF_PROJECT`` with a valid URL, and adjust styling as desired):

.. code-block:: html

    <div style="background-color: rgb(248, 215, 218); color: rgb(114, 28, 36); text-align: center;">
      <div>
        <div>This is documentation for <strong>an old version</strong>.
          <a href="{{ URL_OF_STABLE_VERSION_OF_PROJECT }}" style="background-color: rgb(220, 53, 69); color: rgb(255, 255, 255); margin: 1rem; padding: 0.375rem 0.75rem; border-radius: 4px; display: inline-block; text-align: center;">Switch to stable version</a>
        </div>
      </div>
    </div>
