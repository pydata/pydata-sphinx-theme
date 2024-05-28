========
Graphviz
========

Inheritance Diagram
-------------------

If you use :mod:`sphinx.ext.inheritance_diagram` to generate inheritance diagrams with
:mod:`sphinx.ext.graphviz`, and you output the inheritance diagrams in SVG format,
they will automatically adapt to this theme's light or dark mode.

To have the inheritance-diagram render to SVG, inside ``conf.py``, you need
the following option.

.. code-block:: python

    # conf.py
    ...
    graphviz_output_format = 'svg'
    ...

Below is an example of the inheritance diagram for ``matplotlib.figure.Figure``.
Try toggling light/dark mode to see it adapt!

.. inheritance-diagram:: matplotlib.figure.Figure

See the sphinx inheritance-diagram `documentation`_ for more information.

.. _documentation: https://www.sphinx-doc.org/en/master/usage/extensions/inheritance.html
