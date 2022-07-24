Analytics and usage services
============================

Google Analytics
================

If the ``google_analytics_id`` config option is specified (like ``G-XXXXXXXXXX``),
Google Analytics' javascript is included in the html pages.

.. code:: python

   html_theme_options = {
       "google_analytics_id": "G-XXXXXXXXXX",
   }
