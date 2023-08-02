
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

The position of the search *button* is controlled by ``search-button`` and by default is included in ``html_theme_options["navbar_persistent"]``; you may move it elsewhere as befits your site's layout, or remove it.
You can also add an always-visible search field to some/all pages in your site by adding ``search-field.html`` to one of the configuration variables (e.g., ``html_sidebars``, ``html_theme_options["footer_start"]``, etc.).

For example, if you'd like the search field to be in your sidebar, add it to
the sidebar templates like so:

.. code:: python

    html_sidebars = {
        "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
    }

If instead, you'd like to put the search field in the top navbar, use the
following configuration:

.. code:: python

   html_theme_options = {
       "navbar_end": ["navbar-icon-links.html", "search-field.html"]
   }

.. warning::

    If a page includes *both* the search button and an always-visible search field, the keyboard shortcuts will focus on the always-visible field and the hidden search field overlay will not display. *This may not be what you want:* on small screens (i.e. mobile devices) the sidebars may be hidden in a drawer, and if the persistent search field is there, it may receive focus without actually being made visible. It is **strongly recommended** that you use *either* the search button and the hidden/overlaid field that comes with it, *or* use a persistent search field in a place that makes sense for your layout.


Configure the search bar text
-----------------------------

To modify the text that is in the search bar before people click on it, add the
following configuration to your ``conf.py`` file:

.. code:: python

   html_theme_options = {
       "search_bar_text": "Your text here..."
   }
