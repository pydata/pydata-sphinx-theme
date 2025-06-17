Test conversion of a self-hosted GitHub URL
===========================================

This test ensures that a site using PyData Sphinx Theme can set a self-hosted
version control URL via the theme options and then when the site is built, that
the URLs that go to that self-hosted version control domain will be properly
shortened (just like for github.com, gitlab.com, and bitbucket.org).

.. toctree::
   :caption: My caption
   :numbered:

   links
