.. INSPIRED FROM sphinx-design documentation

Web components
==============

Cards and tabs are a key functionalities in many documentations depending on pydata-sphinx-theme. Both `sphinx-design <>`__ and `sphinx-panels <>`__ can be used with this theme. We overwrote some of their display features to make them compatible with our supported themes. For usage, please refer to their documentations.

.. danger::

    To use the :code:`sphinx-panels` extention, you need to integrate theses lines to overwrite the shadows of the panels in your custom :code:`.css` file:

    .. code-block:: css

        /* overwrite panels shadows using pydata-sphinx-theme variable */
        .shadow {
            box-shadow: 0 0.5rem 1rem var(--pst-color-shadow) !important;
        }

    This modification is not needed when using the :code:`sphinx-design` extention.

Here you can find some examples of the **cards** and **tabs** created with the :code:`sphinx-design` extention.

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
