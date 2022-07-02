.. INSPIRED FROM sphinx-design documentation

Web components
==============

Cards and tabs provide some extra UI flexibility for your content. Both `sphinx-design <https://sphinx-design.readthedocs.io/en/latest/index.html>`__ and `sphinx-panels <https://sphinx-panels.readthedocs.io/en/latest/>`__ can be used with this theme. This theme provides custom CSS to ensure that their look and feel is consistent with this theme.

.. seealso::

   For more about how to use these extensions, see `the sphinx-design documentation <https://sphinx-design.readthedocs.io/en/latest/index.html>`_.

.. danger::

   ``sphinx-panels`` is no longer maintained and we recommend you switch to ``sphinx-design``.
   We will deprecate support for sphinx-panels soon.

   To use the :code:`sphinx-panels` extention, add these lines to your custom CSS to overwrite the shadows of the panels:

   .. code-block:: css

       /* overwrite panels shadows using pydata-sphinx-theme variable */
       .shadow {
           box-shadow: 0 0.5rem 1rem var(--pst-color-shadow) !important;
       }

   This modification is not needed when using the :code:`sphinx-design` extention.

Below you can find some examples of the components created with the :code:`sphinx-design` extension.

.. _badges-buttons:

Badges and buttons
------------------

Here are some of the available badges:
:bdg-primary:`primary`
:bdg-secondary:`secondary`
:bdg-success:`success`
:bdg-primary-line:`primary outline`
:bdg-secondary-line:`secondary outline`
:bdg-success-line:`success outline`

Here are some buttons, also using semantic color names. **Note:** in this theme, ``info`` is defined to be the same color as ``primary``, and ``warning`` is the same color as ``secondary``.
If in your site's `custom CSS file <custom-css>`_ you override the `CSS custom properties <css-variables>`_ ``--pst-color-*`` (where ``*`` is one of the semantic color names, e.g., ``primary``, ``danger``, etc), badges and buttons will automatically use the custom color.

.. grid:: auto

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: info
            :shadow:

            Info

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: warning
            :shadow:

            Warning

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: danger
            :shadow:

            Danger

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: muted
            :shadow:

            Muted

Cards
-----

.. grid::

    .. grid-item-card:: Content of the first card

    .. grid-item-card:: Content of the second card

        :bdg-primary:`example`

    .. grid-item-card::

        .. dropdown:: :fa:`eye,mr-1` third card

            Hidden content

    .. grid-item-card:: Clickable  fourth Card
        :link: https://example.com

.. grid::

    .. grid-item-card::

        panel 1 header
        ^^^^^^^^^^^^^^
        panel 1 content
        more content
        ++++++++++++++
        panel 1 footer

    .. grid-item-card::

        panel 2 header
        ^^^^^^^^^^^^^^
        panel 2 content
        ++++++++++++++
        panel 2 footer


Tabs
----

.. tab-set::

    .. tab-item:: c++

        .. code-block:: c++

            int main(const int argc, const char **argv) {
                return 0;
            }

    .. tab-item:: python

        .. code-block:: python

            def main():
                return

    .. tab-item:: java

        .. code-block:: java

            class Main {
                public static void main(String[] args) {
                }
            }

    .. tab-item:: julia

        .. code-block:: julia

            function main()
            end

    .. tab-item:: fortran

        .. code-block:: fortran

            PROGRAM main
            END PROGRAM main

Copybuttons
===========

`sphinx-copybutton <https://sphinx-copybutton.readthedocs.io/en/latest/>`__ adds a copy button to each of your code cells.
You can see it in action by hovering over the code cell below:

.. code-block:: python

    print("A copybutton in the top-right!")

Toggle buttons
==============

`sphinx-togglebutton <https://sphinx-togglebutton.readthedocs.io/en/latest/>`__ allows you to convert admonitions into toggle-able elements.

.. admonition:: Click me to toggle!
   :class: dropdown

   This will be hidden until a click!

.. toggle::

    A standalone toggle button!
