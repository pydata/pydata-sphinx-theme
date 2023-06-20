:py:mod:`pydata_sphinx_theme.short_link`
========================================

.. py:module:: pydata_sphinx_theme.short_link

.. autoapi-nested-parse::

   A custom Transform object to shorten github and gitlab links.

   ..
       !! processed by numpydoc !!


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pydata_sphinx_theme.short_link.ShortenLinkTransform




.. py:class:: ShortenLinkTransform(document, startnode=None)


   Bases: :py:obj:`sphinx.transforms.post_transforms.SphinxPostTransform`

   
   Shorten link when they are coming from github or gitlab and add an extra class to the tag for further styling.

   Before:
       .. code-block:: html

           <a class="reference external" href="https://github.com/2i2c-org/infrastructure/issues/1329">
             https://github.com/2i2c-org/infrastructure/issues/1329
           </a>

   After:
       .. code-block:: html

           <a class="reference external github" href="https://github.com/2i2c-org/infrastructure/issues/1329">
              2i2c-org/infrastructure#1329
           </a>















   ..
       !! processed by numpydoc !!
   .. py:attribute:: default_priority
      :value: 400

      

   .. py:attribute:: formats
      :value: ('html',)

      

   .. py:attribute:: platform

      

   .. py:attribute:: supported_platform

      

   .. py:method:: parse_url(uri)

      
      Parse the content of the url with respect to the selected platform.

      :param uri: the link to the platform content

      :returns: the reformated url title















      ..
          !! processed by numpydoc !!

   .. py:method:: run(**kwargs)

      
      run the Transform object.
















      ..
          !! processed by numpydoc !!


