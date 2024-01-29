:html_theme.sidebar_secondary.remove: true

Test of in-page TOC with no right sidebar
=========================================

This page tests that the local contents directive looks okay.

.. attention::

    We **do not recommend** using this directive on pages that use this theme
    because PyData Theme provides an in-page table of contents in the right sidebar
    by default.

If you do choose to use an inline, in-page table of contents, we recommend that
you turn off the right sidebar as follows.

.. contents:: Page contents
    :local:


Add a local table of contents (in-page)
---------------------------------------

Add the local table of contents directive near the top of your ``.rst`` page:

.. code-block:: rst

    .. contents:: Page contents
        :local:

This directive will generate a table of contents for the section where this was
added, as shown on this page.


Turn off the right sidebar for a single page
--------------------------------------------

On the very top line of your ``.rst`` file, insert the following line:

.. code-block:: rst

    :html_theme.sidebar_secondary.remove: true

This will render the page without the right sidebar, also known as the secondary
sidebar, which contains the table of contents for that page.

Be aware that if you remove the sidebar you may also remove the "Edit on ..."
and "Show source" links for that page, since by default those are configured for
the right sidebar.
