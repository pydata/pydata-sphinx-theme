.. INSPIRED FROM sphinx-design documentation

========================
Sphinx Design Components
========================

The PyData Sphinx Theme uses `sphinx-design <https://sphinx-design.readthedocs.io/en/latest/index.html>`__
to add several UI components and provide extra flexibility for content creation.
These include badges, buttons, cards, and tabs, among other components.
This theme provides custom CSS to ensure that `sphinx-design <https://sphinx-design.readthedocs.io/en/latest/index.html>`__ elements look and feel consistent with this theme.

.. seealso::

    For more information about how to use these extensions, see `the sphinx-design documentation <https://sphinx-design.readthedocs.io/en/latest/index.html>`_.

Below you can find some examples of the components created with the :code:`sphinx-design` extension.

.. _badges-buttons:

Badges and button-links
=======================

Here are some of the available badges:

:bdg-primary:`primary`
:bdg-secondary:`secondary`
:bdg-success:`success`
:bdg-primary-line:`primary outline`
:bdg-secondary-line:`secondary outline`
:bdg-success-line:`success outline`

Here are some of the available button-style links, also using semantic colors:

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
            :color: success
            :shadow:

            Success

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

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: light
            :shadow:

            Light

    .. grid-item::

        .. button-ref:: badges-buttons
            :ref-type: ref
            :color: dark
            :shadow:

            Dark

.. note::

   `Sphinx Design buttons
   <https://sphinx-design.readthedocs.io/en/latest/badges_buttons.html>`__
   are actually links, meaning they are rendered in HTML with ``<a>`` tags
   instead of ``<button>``. Use them if you need a link to look like a button,
   however, be aware that they do not follow accessibility best practices for
   native button components such as using the correct `ARIA attributes
   <https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/button_role>`__.

If in your site's `custom CSS file <custom-css>`_ you override the `CSS custom properties <css-variables>`_ ``--pst-color-*`` (where ``*`` is one of the semantic color names, such as ``primary``, ``danger``), badges and buttons will automatically use the custom color.

Cards
=====

.. grid::

    .. grid-item-card:: Only heading

    .. grid-item-card::

        Only body.

        But with multiple text paragraphs.

    .. grid-item-card:: Heading and body

        Content of the third card.

        :bdg-primary:`Sample badge`

.. grid::

    .. grid-item-card:: A card with a dropdown menu

        .. dropdown:: :fa:`eye me-1` Click to expand dropdown

            Hidden content

    .. grid-item-card:: A clickable card
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
====

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

Dropdowns
=========

Dropdowns look similar to admonitions, but they are clickable interactive elements that can be used to hide content.
See `the Sphinx Design Dropdown documentation <https://sphinx-design.readthedocs.io/en/latest/dropdowns.html>`__ for more information.

.. admonition:: An admonition for reference.

    And some admonition content.

.. dropdown::

   And with no title and some content!

.. dropdown:: With a title

   And some content!

.. dropdown:: With a title and icon
   :icon: unlock

   And some content and an icon!

.. dropdown:: A primary color dropdown
   :color: primary
   :icon: unlock

   And some content!

.. dropdown:: A secondary color dropdown
   :color: secondary
   :icon: unlock

   And some content!

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
