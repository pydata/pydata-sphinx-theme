:py:mod:`pydata_sphinx_theme.translator`
========================================

.. py:module:: pydata_sphinx_theme.translator

.. autoapi-nested-parse::

   A custom Sphinx HTML Translator for Bootstrap layout.

   ..
       !! processed by numpydoc !!


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.translator.BootstrapHTML5TranslatorMixin



Functions
~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.translator.setup_translators



Attributes
~~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.translator.logger


.. py:class:: BootstrapHTML5TranslatorMixin(*args, **kwds)


   
   Mixin HTML Translator for a Bootstrap-ified Sphinx layout.

   Only a couple of functions have been overridden to produce valid HTML to be
   directly styled with Bootstrap, and fulfill acessibility best practices.















   ..
       !! processed by numpydoc !!
   .. py:method:: starttag(*args, **kwargs)

      
      Ensure an aria-level is set for any heading role.
















      ..
          !! processed by numpydoc !!

   .. py:method:: visit_desc_signature(node)

      
      Handle function & method signature nodes to replace dots with underscores.

      This will modify the ``id`` attribute of HTML ``<dt>`` & ``<dd>`` tags, where
      Python functions are documented. Replacing dots with underscores allows the tags
      to be recognized as navigation targets by ScrollSpy.















      ..
          !! processed by numpydoc !!

   .. py:method:: visit_reference(node)

      
      Handle reference nodes to replace dots with underscores.

      This will modify the ``href`` attribute of any internal HTML ``<a>`` tags, e.g.
      the sidebar navigation links.















      ..
          !! processed by numpydoc !!

   .. py:method:: visit_section(node)

      
      Handle section nodes to replace dots with underscores.

      This will modify the ``id`` of HTML ``<section>`` tags, where Python modules
      are documented. Replacing dots with underscores allows the tags to be recognized
      as navigation targets by ScrollSpy.















      ..
          !! processed by numpydoc !!

   .. py:method:: visit_table(node)

      
      Custom visit table method.

      Copy of sphinx source to *not* add 'docutils' and 'align-default' classes but add 'table' class.















      ..
          !! processed by numpydoc !!


.. py:function:: setup_translators(app)

   
   Add bootstrap HTML functionality if we are using an HTML translator.

   This re-uses the pre-existing Sphinx translator and adds extra functionality defined
   in ``BootstrapHTML5TranslatorMixin``. This way we can retain the original translator's
   behavior and configuration, and _only_ add the extra bootstrap rules.
   If we don't detect an HTML-based translator, then we do nothing.















   ..
       !! processed by numpydoc !!

.. py:data:: logger

   

