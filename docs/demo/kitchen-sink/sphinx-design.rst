.. INSPIRED FROM sphinx-design documentation

sphinx-design
=============

.. danger::

    Cards are a key functionality in many documentations depending on pydata-sphinx-theme.
    We overrided some of their fonctionalities to make them compatible with our supported themes. To use panels in your documentation, please refer to the `lib documentation <https://sphinx-design.readthedocs.io/en/sbt-theme/index.html>`__.

Here you can find some examples of the **cards** and **tabs** created by the :code:`sphinx-design` extention.

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
