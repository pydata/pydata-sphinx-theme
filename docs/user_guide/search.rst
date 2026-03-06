
Search bar / search button
==========================

On narrow viewports, users can access search by clicking the magnifying glass
icon (:fas:`search`) in the :ref:`layout-header`. On wide viewports, the
magnifying glass icon, search input field, and keyboard shortcut for focusing
the search input field are all shown. The keyboard shortcut is:

* :kbd:`Ctrl` + :kbd:`K` (Linux, Windows)
* :kbd:`⌘` + :kbd:`K` (macOS)

You can also configure some aspects of the search button and search field, described below.

Configure the search field position
-----------------------------------

The position of the search *button* is controlled by ``search-button`` and by
default is included in ``html_theme_options["navbar_persistent"]``; you may move
it elsewhere as befits your site's layout, or remove it. You can also add an
always-visible search field to some/all pages in your site by adding
``search-field.html`` to one of the configuration variables (e.g.,
``html_sidebars``, ``html_theme_options["footer_start"]``, etc.).

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

    If a page includes *both* the search button and an always-visible search
    field, the keyboard shortcuts will focus on the always-visible field and the
    hidden search field overlay will not display. *This may not be what you want:*
    on small screens (i.e. mobile devices) the sidebars may be hidden in a drawer,
    and if the persistent search field is there, it may receive focus without
    actually being made visible. It is **strongly recommended** that you use
    *either* the search button and the hidden/overlaid field that comes with it,
    *or* use a persistent search field in a place that makes sense for your layout.


Configure the search bar text
-----------------------------

To modify the text that is in the search bar before people click on it, add the
following configuration to your ``conf.py`` file:

.. code:: python

   html_theme_options = {
       "search_bar_text": "Your text here..."
   }

Configure the inline search results (search-as-you-type) feature
----------------------------------------------------------------

Set the ``search_as_you_type`` HTML theme option to ``True``.

.. code:: python

   html_theme_options = {
       "search_as_you_type": True
   }

Disable the built-in search
---------------------------

If your site uses a third-party search backend (e.g. the `Read the Docs
server-side search addon <https://docs.readthedocs.com/platform/stable/addons.html>`_),
you may want to disable the built-in pydata search entirely. Set the
``disable_search`` HTML theme option to ``True``:

.. code:: python

   html_theme_options = {
       "disable_search": True
   }

This does two things automatically:

* The ``#pst-search-dialog`` overlay is omitted from the page, so the
  built-in search dialog never appears and keyboard shortcuts (:kbd:`Ctrl` +
  :kbd:`K` / :kbd:`⌘` + :kbd:`K`) do not open it.
* ``search-button-field`` is removed from ``navbar_persistent``, so the
  default search button is no longer rendered in the navbar.

.. note::

   ``disable_search`` only removes ``search-button-field`` (the full navbar
   button showing the search label and keyboard shortcut) from
   ``navbar_persistent``. It does not remove ``search-button`` (the icon-only
   variant) or ``search-field.html`` if you have placed either of those
   explicitly elsewhere in your layout. Remove them manually if needed.
