:py:mod:`pydata_sphinx_theme.pygment`
=====================================

.. py:module:: pydata_sphinx_theme.pygment

.. autoapi-nested-parse::

   Handle pygment css.

   inspired by the Furo theme
   https://github.com/pradyunsg/furo/blob/main/src/furo/__init__.py

   ..
       !! processed by numpydoc !!


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.pygment._get_styles
   pydata_sphinx_theme.pygment.get_pygments_stylesheet
   pydata_sphinx_theme.pygment.overwrite_pygments_css



Attributes
~~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.pygment.logger


.. py:function:: _get_styles(formatter, prefix)

   
   Get styles out of a formatter, where everything has the correct prefix.
















   ..
       !! processed by numpydoc !!

.. py:function:: get_pygments_stylesheet(light_style, dark_style)

   
   Generate the theme-specific pygments.css.

   There is no way to tell Sphinx how the theme handles modes.















   ..
       !! processed by numpydoc !!

.. py:function:: overwrite_pygments_css(app, exception=None)

   
   Overwrite pygments.css to allow dynamic light/dark switching.

   Sphinx natively supports config variables `pygments_style` and
   `pygments_dark_style`. However, quoting from
   www.sphinx-doc.org/en/master/development/theming.html#creating-themes

       The pygments_dark_style setting [...is used] when the CSS media query
       (prefers-color-scheme: dark) evaluates to true.

   This does not allow for dynamic switching by the user, so at build time we
   overwrite the pygment.css file so that it embeds 2 versions:

   - the light theme prefixed with "[data-theme="light"]"
   - the dark theme prefixed with "[data-theme="dark"]"

   Fallbacks are defined in this function in case the user-requested (or our
   theme-specified) pygments theme is not available.















   ..
       !! processed by numpydoc !!

.. py:data:: logger

   

