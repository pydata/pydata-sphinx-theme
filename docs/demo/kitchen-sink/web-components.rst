.. INSPIRED FROM sphinx-design documentation

Web components
==============

Cards and tabs provide some extra UI flexibility for your content. Both `sphinx-design <https://sphinx-design.readthedocs.io/en/latest/index.html>`__ and `sphinx-panels <https://sphinx-panels.readthedocs.io/en/latest/>`__ can be used with this theme. This theme provides custom CSS to ensure that their look and feel is consistent with this theme.

.. seealso::

   For more about how to use these extensions, see `the sphinx-design documentation <https://sphinx-design.readthedocs.io/en/latest/index.html>`_.

.. danger::

   ``sphinx-panels`` is no longer maintained and recommend you switch to ``sphinx-design``.
   We will deprecate support for sphinx-panels soon.

   To use the :code:`sphinx-panels` extention, add these lines to your custom CSS to overwrite the shadows of the panels:

   .. code-block:: css

       /* overwrite panels shadows using pydata-sphinx-theme variable */
       .shadow {
           box-shadow: 0 0.5rem 1rem var(--pst-color-shadow) !important;
       }

   This modification is not needed when using the :code:`sphinx-design` extention.

Below you can find some examples of the **cards** and **tabs** created with the :code:`sphinx-design` extention.

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
