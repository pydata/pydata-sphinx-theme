.. _version-dropdowns:

Version switcher dropdowns
==========================

You can add a button to your site that allows users to
switch between versions of your documentation. The links in the version
switcher will differ depending on which page of the docs is being viewed. For
example, on the page ``https://mysite.org/en/v2.0/changelog.html``, the
switcher links will go to ``changelog.html`` in the other versions of your
docs. When clicked, the switcher will check for the existence of that page, and
if it doesn't exist, will redirect to the homepage instead (in the requested version of the docs).

The switcher requires the following configuration steps:

1. Add a JSON file containing a list of the documentation versions that the
   switcher should show on each page.

2. Add a configuration dictionary called ``switcher`` to the
   ``html_theme_options`` dict in ``conf.py``. ``switcher`` should have 2 keys:

   - ``json_url``: the persistent location of the JSON file described above.
   - ``version_match``: a string stating the version of the documentation that
     is currently being browsed.

3. Specify where to place the switcher in your page layout. For example, add
   the ``"version-switcher"`` template to one of the layout lists in
   ``html_theme_options`` (e.g., ``navbar_end``, ``footer_start``, etc.).

Below is a more in-depth description of each of these configuration steps.


Add a JSON file to define your switcher's versions
--------------------------------------------------

First, write a JSON file stating which versions of your docs will be listed in
the switcher's dropdown menu. That file should contain a list of entries that
each can have the following fields:

- ``version``: a version string. This is checked against
  ``switcher['version_match']`` to provide styling to the switcher.
- ``url``: the URL for this version.
- ``name``: an optional name to display in the switcher dropdown instead of the
  version string (e.g., "latest", "stable", "dev", etc.).
- ``preferred``: an optional field that *should occur on at most one entry* in the JSON file.
  It specifies which version is considered "latest stable", and is used to customize the message used on :ref:`version-warning-banners` (if they are enabled).

Here is an example JSON file:

.. code:: json

    [
        {
            "name": "v2.1 (stable)",
            "version": "2.1",
            "url": "https://mysite.org/en/2.1/"
        },
        {
            "version": "2.1rc1",
            "url": "https://mysite.org/en/2.1rc1/"
        },
        {
            "version": "2.0",
            "url": "https://mysite.org/en/2.0/"
        },
        {
            "version": "1.0",
            "url": "https://mysite.org/en/1.0/"
        }
    ]

See the discussion of ``switcher['json_url']`` (below) for options of where to
save the JSON file.


Configure ``switcher['json_url']``
----------------------------------

*The JSON file needs to be at a stable, persistent, fully-resolved URL* (i.e.,
not specified as a path relative to the sphinx root of the current doc build).
Each version of your documentation should point to the same URL, so that as new
versions are added to the JSON file all the older versions of the docs will
gain switcher dropdown entries linking to the new versions. This could be done
in a few different ways:

- The location could be one that is always associated with the most recent
  documentation build (i.e., if your docs server aliases "latest" to the most
  recent version, it could point to a location in the build tree of version
  "latest"). For example:

  .. code:: python

      html_theme_options = {
          ...,
          "switcher": {
              "json_url": "https://mysite.org/en/latest/_static/switcher.json",
          }
      }

  In this case, the JSON is versioned alongside the rest of the docs pages but
  only the most recent version is ever loaded (even by older versions of the
  docs).

- The JSON could be stored outside the doc build trees. This probably means it
  would be outside the software repo, and would require you to add new version
  entries to the JSON file manually as part of your release process. Example:

  .. code:: python

      html_theme_options = {
          ...,
          "switcher": {
              "json_url": "https://mysite.org/switcher.json",
          }
      }

- In theory the JSON could be saved in a folder that is listed under your site's
  ``html_static_path`` configuration, **but this is not recommended**. If you want to
  do it this way, see `the Sphinx static path documentation
  <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path>`_
  for more information but do so knowing that we do not support this use case.

By default, the theme is testing the :code:`.json` file provided and outputs warnings in the Sphinx build. If this test breaks the pipeline of your docs, the test can be disabled by configuring the :code:`check_switcher` parameter in :code:`conf.py`:

.. code-block:: python

    html_theme_options = {
        # ...
        "check_switcher": False
    }

Configure ``switcher['version_match']``
---------------------------------------

This configuration value tells the switcher what docs version is currently
being viewed, and is used to style the switcher (i.e., to highlight the current
docs version in the switcher's dropdown menu, and to change the text displayed
on the switcher button).

Typically, you can re-use one of the sphinx variables ``version``
or ``release`` as the value of ``switcher['version_match']``; which one you use
depends on how granular your docs versioning is. See
`the Sphinx "project info" documentation
<https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information>`__
for more information). Example:

.. code:: python

    version = my_package_name.__version__.replace("dev0", "")  # may differ
    html_theme_options = {
        ...,
        "switcher": {
            "version_match": version,
        }
    }


Specify where to display the switcher
-------------------------------------

Finally, tell the theme where on your site's pages you want the switcher to
appear. There are many choices here: you can add ``"version-switcher"`` to one
of the locations in ``html_theme_options`` (e.g., ``navbar_end``,
``footer_start``, etc). For example:

.. code:: python

   html_theme_options = {
      ...,
      "navbar_start": ["navbar-logo", "version-switcher"]
   }


Alternatively, you could override one of the other templates to include the
version switcher in a sidebar. For example, you could define
``_templates/sidebar-nav-bs.html`` as:

.. code:: jinja

    {%- include 'version-switcher.html' -%}
    {{ super() }}

to insert a version switcher at the top of the primary sidebar, while still
keeping the default navigation below it. See :doc:`layout` for more
information.

Style the switcher buttons
--------------------------

You may apply styles via CSS to any of the switcher buttons to control their look and feel.
Each button has two `HTML dataset entries <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset>`_
that you can use to apply CSS rules to subsets of buttons. These entries are:

.. code-block::

   data-version
   data-version-name

For example, the link for an entry with ``version="0.2"``,
and ``name="My version"`` would have metadata like so:

.. code-block:: html

   <a data-version-name="My version" data-version="0.2" class="<classes...>">

You can create CSS rules that select this metadata like so:

.. code-block:: scss

   // Style all links with a specific subset of versions
   .version-switcher__container a[data-version="0.2"],
   .version-switcher__container a[data-version="0.3"] {
      background-color: red;
   }
   // Style all links with `stable` in the version name
   .version-switcher__container a[data-version-name*="stable"] {
      background-color: green;
   }

In addition, the parent button of the dropdown list contains similar metadata
about the **current version**. This could be used to style the entire dropdown
a certain color based on the active version.

For example, if you wanted to style the dropdown button to use the theme's secondary color (PyData orange by default) if it was a ``dev``
version, you could use the following CSS selector:

.. code-block:: scss

   // If the active version has the name "dev", style it orange
   .version-switcher__button[data-active-version-name*="dev"] {
      background-color: var(--pst-color-secondary);
   }

.. seealso::

   See the `MDN documentation on dataset properties <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset>`_
   for more information on using and styling these properties.
