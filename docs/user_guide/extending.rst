===================
Extending the theme
===================

There are many extensions available for Sphinx that can enhance your site or provide powerful customization abilities. Here we describe a few customizations that are popular with ``pydata-sphinx-theme`` users.

Collapsible admonitions
=======================

The `sphinx-togglebutton <https://sphinx-togglebutton.readthedocs.io/en/latest/>`__ extension provides optional show/hide behavior for admonitions. Follow their installation instructions, then add it to the ``extentions`` list in your ``conf.py``:

.. code:: python

    extensions = [
        # [...]
        "sphinx_togglebutton"
    ]

Then add the ``dropdown`` class to any admonition directive (shown here on a ``note`` admonition):

.. begin-example-dropdown
.. note::
    :class: dropdown

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. end-example-dropdown

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-dropdown
            :end-before: .. end-example-dropdown
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ```{note}
            :class: dropdown

            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            ```


Custom admonition styles
========================

A `limited set <https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions>`__ of admonitions are built-in to docutils (the ``rST`` → ``HTML`` engine that underlies Sphinx). However, it is possible to create custom admonitions with their own default colors, icons, and titles.


Customizing the title
---------------------

Although most admonitions have a default title like ``note`` or ``warning``, a generic ``admonition`` directive is built-in to docutils/Sphinx. In this theme, its color defaults to the same color as ``note`` admonitions, and it has a bell icon:

.. begin-example-title
.. admonition:: Custom title!

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. end-example-title

The title is specified on the same line as the ``.. admonition::`` directive:

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-title
            :end-before: .. end-example-title
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ```{admonition} Custom title!

            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            ```

Styling with semantic color names
---------------------------------

You can re-style any admonition to match any of the built-in admonition types using any of the :ref:`theme's semantic color names <color-variables>` as a class (this is most useful for custom-titled admonitions):

.. begin-example-semantic
.. admonition:: Custom title with "warning" style
    :class: warning

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. end-example-semantic

Note that it updates both the color and the icon. See :doc:`./styling` for a list of all semantic color names.

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-semantic
            :end-before: .. end-example-semantic
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ```{admonition} Custom title with "warning" style
            :class: warning

            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            ```

This theme defines classes for `the standard docutils admonition types <https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions>`__ (``attention``, ``caution``, etc) and additionally supports ``seealso`` and ``todo`` admonitions (see :doc:`../examples/kitchen-sink/admonitions` for a demo of all built-in admonition styles).

Customizing the color
---------------------

Besides the pre-defined semantic color classes (see previous section) you can also add a bespoke color to any admonition by defining your own CSS class. Example:

.. begin-example-color
.. admonition:: Admonition with custom "olive" color
    :class: admonition-olive

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. end-example-color

To do this, you will need to add a class to your `custom.css <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_css_files>`__ file, as in the example below.
Be sure to use the same color for ``border-color`` and ``color`` and a different shade for ``background-color``:

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-color
            :end-before: .. end-example-color
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ```{admonition} Admonition with custom "olive" color
            :class: admonition-olive

            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            ```

And add the following to your ``custom.css`` file:

.. include:: ../_static/custom.css
    :start-after: begin-custom-color
    :end-before: /* end-custom-color
    :code: css
    :class: highlight-css


Using a custom icon
-------------------

Customizing the icon uses a similar process to customizing the color: create a new CSS class in your `custom.css <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_css_files>`__ file. The theme supports `fontawesome v6 icons <https://fontawesome.com/v6/search?o=r&m=free&f=brands>`__ ("free" and "brands" sets). To use an icon, copy its unicode value into your custom class as shown in the CSS tab below:

.. begin-example-icon
.. admonition:: Check out my custom icon
    :class: admonition-icon

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. end-example-icon

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-icon
            :end-before: .. end-example-icon
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ```{admonition} Check out my custom icon
            :class: admonition-icon

            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            ```

And add the following css to your ``custom.css`` file:

.. include:: ../_static/custom.css
    :start-after: begin-custom-icon
    :end-before: /* end-custom-icon
    :code: css
    :class: highlight-css


Combining all three customizations
----------------------------------

Here we demonstrate an admonition with a custom icon, color, and title (and also make it collapsible). Note that the multiple admonition class names are space-separated:

.. begin-example-youtube
.. admonition:: YouTube
    :class: dropdown admonition-youtube

    ..  youtube:: dQw4w9WgXcQ
.. end-example-youtube

.. tab-set::

    .. tab-item:: rst

        .. include:: ./extending.rst
            :start-after: begin-example-youtube
            :end-before: .. end-example-youtube
            :code: rst
            :class: highlight-rst

    .. tab-item:: markdown

        .. code-block:: md

            ````{admonition} YouTube
            :class: dropdown admonition-youtube

            ```{youtube} dQw4w9WgXcQ
            ```

            ````

And add the following css to your custom.css file:

.. include:: ../_static/custom.css
    :start-after: begin-custom-youtube
    :end-before: /* end-custom-youtube
    :code: css
    :class: highlight-css
