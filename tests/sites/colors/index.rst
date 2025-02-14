Test of colors
==============

Some text with a `text link <https://pydata.org>`__.

Heading 1
---------

Some text with a :ref:`cross reference link <a-cross-reference>`

Heading 2
~~~~~~~~~

Some text with ``inline code``.


.. _a-cross-reference:

Heading 3
`````````

Some text with a |code link|_.

Heading 4
---------

Some other text

Heading 5
---------

Some other text

Heading 6
---------

Some other text

Heading 7
---------

Some other text


.. the below replacement is included to emulate what intersphinx / autodoc / numpydoc generate (links on text formatted as code), which (sadly) can't be done using nesting of standard rST markup.

.. |code link| replace:: ``inline code link``
.. _code link: https://pydata.org
