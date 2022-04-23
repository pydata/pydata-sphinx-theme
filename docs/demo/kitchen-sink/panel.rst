.. INSPIRED FROM sphinx-panel documentation

sphinx-Panels
=============

.. danger::

    Panels are a key functionality in many documentations depending on pydata-sphinx-theme.
    We overrided some of their fonctionalities to make them compatible with our supported themes. To use panels in your documentation, please refer to the `lib documentation <https://sphinx-panels.readthedocs.io/en/latest/#>`__.

Here you can find some examples of the **panels** and **tabs** created by the :code:`sphinx-panel` extention.

Panels
------

.. panels::

    Content of the top-left panel

    ---

    Content of the top-right panel

    :badge:`example,badge-primary`

    ---

    .. dropdown:: :fa:`eye,mr-1` Bottom-left panel

        Hidden content

    ---

    .. link-button:: https://example.com
        :text: Clickable Panel
        :classes: stretched-link

.. panels::

    panel 1 header
    ^^^^^^^^^^^^^^

    panel 1 content

    more content

    ++++++++++++++
    panel 1 footer

    ---

    panel 2 header
    ^^^^^^^^^^^^^^

    panel 2 content

    ++++++++++++++
    panel 2 footer


Tabs
----

.. tabbed:: c++

    .. code-block:: c++

        int main(const int argc, const char **argv) {
          return 0;
        }

.. tabbed:: python

    .. code-block:: python

        def main():
            return

.. tabbed:: java

    .. code-block:: java

        class Main {
            public static void main(String[] args) {
            }
        }

.. tabbed:: julia

    .. code-block:: julia

        function main()
        end

.. tabbed:: fortran

    .. code-block:: fortran

        PROGRAM main
        END PROGRAM main
