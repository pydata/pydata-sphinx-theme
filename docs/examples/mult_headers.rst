Top-level headers and the TOC
=============================

Your right table of contents will behave slightly differently depending on
whether your page has one top-level header, or multiple top-level headers. See
below for more information.

An example with multiple top-level headers
==========================================

If a page has multiple top-level headers on it, then the in-page Table of Contents
will show each top-level header.
**On this page, there are multiple top-level headers**. As a result, the top-level
headers all appear in the right Table of Contents. Here's an example of a page structure
with multiple top-level headers:


.. code-block:: rst

   My first header
   ===============

   My sub-header
   -------------

   My second header
   ================

   My second sub-header
   --------------------

And here's a second-level header
--------------------------------

Notice how it is nested *underneath* "Top-level header 2" in the TOC.


An example with a single top-level header
=========================================

If the page only has a single top-level header, it
is assumed to be the page title, and only the headers **underneath** the top-level
header will be used for the right Table of Contents.

On most pages in this documentation, only a single top-level header is used. For
example, they have a page structure like:

.. code-block:: rst

   My title
   ========

   My header
   ---------

   My second header
   ----------------


.. meta::
    :description lang=en:
        Examples of multiple headers in pydata-sphinx-theme.
