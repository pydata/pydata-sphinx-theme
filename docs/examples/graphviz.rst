========
Graphviz
========

Inheritance Diagram
-------------------

Using :mod:`sphinx.ext.inheritance_diagram`, inheritance diagrams can be generated
through :mod:`sphinx.ext.graphviz`.  If the output of the inheritance diagrams are
in SVG format, they can be made to conform to light or dark mode.

To have the inheritance-diagram render to SVG, inside ``conf.py``, you need
the following option.

.. code-block:: python

    # conf.py
    ...
    graphviz_output_format = 'svg'
    ...

Below is an example of the inheritance diagram for ``matplotlib.figure.Figure``

.. inheritance-diagram:: matplotlib.figure.Figure

See the sphinx inheritance-diagram `documentation`_ for more information.

.. _documentation: https://www.sphinx-doc.org/en/master/usage/extensions/inheritance.html
