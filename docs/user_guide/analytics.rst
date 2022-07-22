Analytics and usage services
============================

The theme supports several web analytics services via the ``analytics`` option. It is configured
by passing a dictionary with options. See the sections bellow for relevant
options depending on the analytics provider that you want to use.

.. code:: python

   html_theme_options = {
       "analytics": analytics_options,
   }

Plausible Analytics (recommended)
=================================

https://plausible.io can be used to gather simple
and privacy-friendly analytics for the site. The configuration consists in
a server URL and a specific domain. Plausible' javascript will be included in
all html pages to gather metrics. And the dashboard can be accessed at
``https://url/my_domain``.

The Scientific-Python community can offer a self-hosted server. Contact the
team on social media following https://scientific-python.org for assistance.

.. code:: python

   # To be re-used in html_theme_options["analytics"]
   analytics_options = {
       "plausible_analytics_domain": "my-domain",
       "plausible_analytics_url": "https://.../script.js",
   }

Google Analytics
================

If the ``google_analytics_id`` config option is specified (like ``G-XXXXXXXXXX``),
Google Analytics' javascript is included in the html pages.

.. code:: python

   # To be re-used in html_theme_options["analytics"]
   analytics_options = {
       "google_analytics_id": "G-XXXXXXXXXX",
   }
