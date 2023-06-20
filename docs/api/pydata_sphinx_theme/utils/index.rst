:py:mod:`pydata_sphinx_theme.utils`
===================================

.. py:module:: pydata_sphinx_theme.utils

.. autoapi-nested-parse::

   General helpers for the management of config parameters.

   ..
       !! processed by numpydoc !!


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.utils.config_provided_by_user
   pydata_sphinx_theme.utils.get_theme_options_dict
   pydata_sphinx_theme.utils.soup_to_python
   pydata_sphinx_theme.utils.traverse_or_findall



.. py:function:: config_provided_by_user(app, key)

   
   Check if the user has manually provided the config.
















   ..
       !! processed by numpydoc !!

.. py:function:: get_theme_options_dict(app)

   
   Return theme options for the application w/ a fallback if they don't exist.

   The "top-level" mapping (the one we should usually check first, and modify
   if desired) is ``app.builder.theme_options``. It is created by Sphinx as a
   copy of ``app.config.html_theme_options`` (containing user-configs from
   their ``conf.py``); sometimes that copy never occurs though which is why we
   check both.















   ..
       !! processed by numpydoc !!

.. py:function:: soup_to_python(soup, only_pages = False)

   
   Convert the toctree html structure to python objects which can be used in Jinja.

   Parameters:
   soup : BeautifulSoup object for the toctree
   only_pages : Only include items for full pages in the output dictionary. Exclude anchor links (TOC items with a URL that starts with #)

   :returns: The toctree, converted into a dictionary with key/values that work within Jinja.















   ..
       !! processed by numpydoc !!

.. py:function:: traverse_or_findall(node, condition, **kwargs)

   
   Triage node.traverse (docutils <0.18.1) vs node.findall.

   TODO: This check can be removed when the minimum supported docutils version
   for numpydoc is docutils>=0.18.1.















   ..
       !! processed by numpydoc !!

