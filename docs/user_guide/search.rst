
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

You can add an always-visible search field to some/all pages in your site by adding ``search-field.html`` to one of the configuration variables (e.g., ``html_sidebars``, ``html_theme_options["footer_items"]``, etc). If you include this, the built-in search button / overlay will be hidden and disabled on that page.

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

    On pages where you include an always-visible search field, the keyboard shortcuts will focus that field *even if it is offscreen*. For example, on small screens (i.e. mobile devices) the sidebars may be hidden in a drawer, and if the persistent search field is in the sidebar, it may receive focus without actually being made visible. Thus if you use the persistent search field, it is **strongly recommended** to place it in the main content area of your page.


Configure the search bar text
-----------------------------

To modify the text that is in the search bar before people click on it, add the
following configuration to your ``conf.py`` file:

.. code:: python

   html_theme_options = {
       "search_bar_text": "Your text here..."
   }
