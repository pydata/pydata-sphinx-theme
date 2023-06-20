:py:mod:`pydata_sphinx_theme.logo`
==================================

.. py:module:: pydata_sphinx_theme.logo

.. autoapi-nested-parse::

   customize events for logo management.

   we use one event to copy over custom logo images to _static
   and another even to link them in the html context

   ..
       !! processed by numpydoc !!


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.logo.copy_logo_images
   pydata_sphinx_theme.logo.setup_logo_path



Attributes
~~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.logo.logger


.. py:function:: copy_logo_images(app, exception=None)

   
   Copy logo image to the _static directory.

   If logo image paths are given, copy them to the `_static` folder Then we can link to them directly in an html_page_context event.















   ..
       !! processed by numpydoc !!

.. py:function:: setup_logo_path(app, pagename, templatename, context, doctree)

   
   Set up relative paths to logos in our HTML templates.

   In Sphinx, the context["logo"] is a path to the `html_logo` image now in the output
   `_static` folder.

   If logo["image_light"] and logo["image_dark"] are given, we must modify them to
   follow the same pattern. They have already been copied to the output folder
   in the `update_config` event.















   ..
       !! processed by numpydoc !!

.. py:data:: logger

   

