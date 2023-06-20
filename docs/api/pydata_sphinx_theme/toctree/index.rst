:py:mod:`pydata_sphinx_theme.toctree`
=====================================

.. py:module:: pydata_sphinx_theme.toctree

.. autoapi-nested-parse::

   Methods to build the toctree used in the html pages.

   ..
       !! processed by numpydoc !!


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.toctree.add_collapse_checkboxes
   pydata_sphinx_theme.toctree.add_inline_math
   pydata_sphinx_theme.toctree.add_toctree_functions
   pydata_sphinx_theme.toctree.get_local_toctree_for
   pydata_sphinx_theme.toctree.index_toctree



.. py:function:: add_collapse_checkboxes(soup)

   
   Add checkboxes to collapse children in a toctree.
















   ..
       !! processed by numpydoc !!

.. py:function:: add_inline_math(node)

   
   Render a node with HTML tags that activate MathJax processing.

   This is meant for use with rendering section titles with math in them, because
   math outputs are ignored by pydata-sphinx-theme's header.

   related to the behaviour of a normal math node from:
   https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/mathjax.py#L28















   ..
       !! processed by numpydoc !!

.. py:function:: add_toctree_functions(app, pagename, templatename, context, doctree)

   
   Add functions so Jinja templates can add toctree objects.
















   ..
       !! processed by numpydoc !!

.. py:function:: get_local_toctree_for(self, indexname, docname, builder, collapse, **kwargs)

   
   Return the "local" TOC nodetree (relative to `indexname`).
















   ..
       !! processed by numpydoc !!

.. py:function:: index_toctree(app, pagename, startdepth, collapse = True, **kwargs)

   
   Returns the "local" (starting at `startdepth`) TOC tree containing the current page, rendered as HTML bullet lists.

   This is the equivalent of `context["toctree"](**kwargs)` in sphinx
   templating, but using the startdepth-local instead of global TOC tree.















   ..
       !! processed by numpydoc !!

