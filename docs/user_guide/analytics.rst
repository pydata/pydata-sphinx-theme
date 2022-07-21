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
and privacy-friendly analytics for the site. The configuration consists in
a server URL and a specific domain. Plausible' javascript will be included in
all html pages to gather metrics. And the dashboard can be accessed at
``https://url/my_domain``.

The Scientific-Python community can offer a self-hosted server. Contact the
team on social media following https://scientific-python.org for assistance.

.. code:: python

   html_theme_options = {
       "plausible_analytics_domain": "my-domain",
       "plausible_analytics_url": "https://.../script.js",
   }
