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

Plausible Analytics
===================

Alternatively https://plausible.io can be used to gather simple
and privacy-friendly analytics for the site. The dashboard can be accessed
at ``url/domain``.
The Scientific-Python community can offer a self-hosted server.

Plausible' javascript is included in the html pages.

.. code:: python

   html_theme_options = {
       "plausible_analytics_domain": "my-domain",
       "plausible_analytics_url": "https://.../script.js",
   }
