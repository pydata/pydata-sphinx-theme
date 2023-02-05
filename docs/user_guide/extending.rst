===================
Extending the theme
===================

This theme can be extended using other sphinx extentions, their interaction with the pydata-sphinx-theme is described in this section.

Customize admonitions
=====================

Admonitions are based on the Sphinx admonition system described in :doc:`../examples/kitchen-sink/admonition`. They are fully customizable to render more complex configuration.

collapsing
----------

To make the admonitions collapsable, we suggest to rely on the `sphinx-togglebutton <https://sphinx-togglebutton.readthedocs.io/en/latest/>`__ extention. Follow the instalation instruction from their documentation and add it to the ``extentions`` in your ``conf.py``:

.. code-block:: python

    extentions = [
        # [...]
        "sphinx_togglebutton"
    ]

Then add the ``dropdown`` class to any admonition directive:

.. note::
    :class: dropdown

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. note::
                :class: dropdown

                Lorem ipsum dolor sit amet, consectetur adipiscing elit.

custom title
------------

By design, admonitions are using an automatic title to display next to the icon. By using the generic ``admonition`` directive, the first argument will be used as admonition title.
Default admonitions are rendered with your custom title, a :fas:`bell` icon and the "note" admonition coloring.

.. admonition:: custom

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. admonition:: custom

                Lorem ipsum dolor sit amet, consectetur adipiscing elit.

You can also use one of the predifined color-icon by adding one of the existing admonition class to your custom admonition. This theme supports:

-   ``attention``
-   ``caution``
-   ``warning``
-   ``danger``
-   ``error``
-   ``hint``
-   ``tip``
-   ``important``
-   ``note``
-   ``seealso``
-   ``admonition-todo``

So to display the previous custom admonition with the "warning" styling, add the class ``warning`` to the directive:

.. admonition:: custom
    :class: warning

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. admonition:: custom
                :class: warning

                Lorem ipsum dolor sit amet, consectetur adipiscing elit.

customize colors
----------------

If the available coloring are not fitting your requirements, create an extra css class in your ``custom.css`` file and update the colors of the admonition. Use the same color for both background and title the transparency is computed automatically by the theme.

.. admonition:: custom
    :class: admonition-olive

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. admonition:: custom
                :class: admonition-olive

                Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. tab-item:: css

        .. code-block:: css

            /* <your static path>/custom.css */

            div.admonition.admonition-olive {
              border-color: olive;
            }
            div.admonition.admonition-olive > .admonition-title:before {
              background-color: olive;
            }
            div.admonition.admonition-olive > .admonition-title:after {
              color: olive;
            }

customize icon
--------------

If the default :fas:`bell` icon not fitting your requirements, create an extra css class in your ``custom.css`` file and update the icon of the admonition. The theme support natively fontawesome V6 icons so go to their `website <https://fontawesome.com>`__ and copy the unicode value of your custom icon and set it in your custom class:

.. admonition:: custom
    :class: admonition-icon

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. admonition:: custom
                :class: admonition-icon

                Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. tab-item:: css

        .. code-block:: css

            /* <your static path>/custom.css */

            div.admonition.admonition-icon > .admonition-title:after {
              content: "\f24e" /* the fa-scale icon */
            }

complete customization
----------------------

Combine all of the above to get a fully customized admonition:

.. admonition:: youtube
    :class: dropdown admonition-youtube

    ..  youtube:: dQw4w9WgXcQ

.. tab-set::

    .. tab-item:: rst

        .. code-block:: rst

            .. admonition:: youtube
                :class: dropdown admonition-youtube

                ..  youtube:: dQw4w9WgXcQ

    .. tab-item:: css

        .. code-block:: css

            /* <your static path>/custom.css */

            div.admonition.admonition-youtube {
              border-color: #FF0000; /* the youtube red */
            }
            div.admonition.admonition-youtube > .admonition-title:before {
              background-color: #FF0000;
            }
            div.admonition.admonition-youtube > .admonition-title:after {
              color: #FF0000;
              content: "\f26c"; /* fa-brands fa-tv */
            }
