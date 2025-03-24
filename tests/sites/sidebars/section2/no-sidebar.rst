No Primary Sidebar
==================

This test fixture page has been configured to not have a primary sidebar via conf.py:

.. code-block:: python
    :caption: conf.py

    html_sidebars = {
        "no-sidebar": []  # Turn off primary/left sidebar
    }

Yes secondary
-------------

It can have a secondary sidebar.
