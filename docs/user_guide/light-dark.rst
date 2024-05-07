
.. _manage-themes:

Light and dark themes
=====================

You can change the major background/foreground colors of this theme using built-in "dark" and "light" modes.
These are controlled by a button in the navigation header, with the following options:

- A ``light`` theme with a bright background and dark text / UI elements
- A ``dark`` theme with a dark background and light text / UI elements
- ``auto``: the documentation theme will follow the system default that you have set


Configure default theme mode
----------------------------

By default, visitors to your documentation will use the theme mode ``auto``.
This will choose a theme based on the user's system settings, and default to ``light`` if no system setting is found.

If you wish to use a different default theme mode, set the ``default_mode`` configuration to one of ``auto``, ``dark``, ``light``.
For example:

.. code-block:: python

   html_context = {
      # ...
      "default_mode": "light"
   }

For more information, see :ref:`manage-themes`.

.. tip::

   To completely remove the theme management, configure ``default_mode`` to the value you want in your documentation (``light`` or ``dark``) and then remove the theme-switcher from the ``navbar_end`` section of the header navbar configuration:

   .. code-block:: python

      html_theme_options {
          ...
          # Note we have omitted `theme-switcher` below
          "navbar_end": ["navbar-icon-links"]
      }

Customize the CSS of light and dark themes
------------------------------------------

.. danger::

    Theming is still a beta feature, so the variables related to color theming are likely to change in the future. No backward compatibility is guaranteed when customization is done.


To customize the CSS of page elements in a theme-dependent manner, use the ``html[data-theme='<THEME>']`` CSS selector.
For example to define a different background color for both the light and dark themes:

.. code-block:: css

    /* anything related to the light theme */
    html[data-theme="light"] {

        /* whatever you want to change */
        background-color: white;
    }

    /* anything related to the dark theme */
    html[data-theme="dark"] {

        /* whatever you want to change */
        background-color: black;
    }

A complete list of the colors used in this theme can be found in the :doc:`CSS style section <styling>`.

Theme-dependent images and content
----------------------------------

It is possible to use different content for light and dark modes so that the content only shows up when a particular theme is active.
This is useful if your content depends on the theme's style, such as a PNG image with a light or dark background.

There are **two CSS helper classes** to specify items on the page as theme-specific.
These are:

- :code:`only-dark`: Only display an element when the dark theme is active.
- :code:`only-light` Only display an element when the light theme is active.

For example, the following page content defines two images, each of which uses a different one of the classes above.
Change the theme and a new image should be displayed.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. image:: https://source.unsplash.com/200x200/daily?cute+cat
                :class: only-dark

            .. image:: https://source.unsplash.com/200x200/daily?cute+dog
                :class: only-light

    .. tab-item:: markdown

        .. code-block:: md

            ```{image} https://source.unsplash.com/200x200/daily?cute+cat
            :class: only-dark
            ```

            ```{image} https://source.unsplash.com/200x200/daily?cute+dog
            :class: only-light
            ```

.. image:: https://source.unsplash.com/200x200/daily?cute+cat
    :class: only-dark

.. image:: https://source.unsplash.com/200x200/daily?cute+dog
    :class: only-light

Images and content that work in both themes
-------------------------------------------

When the **dark theme** is activated, images that do not support dark mode will
automatically have a white background added to ensure the image contents are
visible, and their brightness will be reduced by a filter.

If your image is suitable for the dark theme, add the CSS class
:code:`only-dark` as noted above. If your image is suitable for both light and
dark themes, add the CSS class :code:`dark-light` to make your image
theme-agnostic.

For example, here's an image without adding this helper class.
Change to the dark theme and a grey background will be present.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. image:: https://source.unsplash.com/200x200/daily?cute+cat
                :class: p-2

    .. tab-item:: markdown

        .. code-block:: md

            ```{image} https://source.unsplash.com/200x200/daily?cute+cat
            :class: p-2
            ```


.. image:: https://source.unsplash.com/200x200/daily?cute+cat
    :class: p-2

Here's the same image with this class added:

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. image:: https://source.unsplash.com/200x200/daily?cute+cat
                :class: dark-light

    .. tab-item:: markdown

        .. code-block:: md

            ```{image} https://source.unsplash.com/200x200/daily?cute+cat
            :class: dark-light p-2
            ```

.. image:: https://source.unsplash.com/200x200/daily?cute+cat
    :class: dark-light p-2

Define custom JavaScript to react to theme changes
--------------------------------------------------

You can define a JavaScript event hook that will run your code any time the theme changes.
This is useful if you need to change elements of your page that cannot be defined by CSS rules.
For example, to change an image source (e.g., logo) whenever the ``data-theme`` changes, a snippet like this can be used:

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. raw:: html

                <script type="text/javascript">
                var observer = new MutationObserver(function(mutations) {
                    const dark = document.documentElement.dataset.theme == 'dark';
                    document.getElementsByClassName('mainlogo')[0].src = dark ? '_static/my_logo_dark.svg' : "_static/my_logo_light.svg";
                })
                observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
                </script>
                <link rel="preload" href="_static/my_logo_dark.svg" as="image">

            .. image:: _static/my_logo_light.svg
                :alt: My Logo
                :class: logo, mainlogo
                :align: center

    .. tab-item:: markdown

        .. code-block:: md

            <script type="text/javascript">
            var observer = new MutationObserver(function(mutations) {
                const dark = document.documentElement.dataset.theme == 'dark';
                document.getElementsByClassName('mainlogo')[0].src = dark ? '_static/my_logo_dark.svg' : "_static/my_logo_light.svg";
            })
            observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
            </script>
            <link rel="preload" href="_static/my_logo_dark.svg" as="image">

            ```{image} _static/my_logo_light.svg
            :alt: My Logo
            :class: logo, mainlogo
            :align: center
            ```

The JavaScript reacts to ``data-theme`` changes to alter ``img``, and the ``link`` is used to preload the dark image.
See the `MutationObserver documentation <https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver>`_ for more information.
