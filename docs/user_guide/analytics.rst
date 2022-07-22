Analytics and usage services
============================

The theme supports several web analytics services via the ``analytics`` option. It is configured
by passing a dictionary with options. See the sections bellow for relevant
options depending on the analytics provider that you want to use.

.. code:: python

   html_theme_options = {
       "analytics": analytics_options,
   }

Generally speaking we recommend using Plausible over Google Analytics because
it has a better story around user security and privacy. In addition, it is more
open-source and transparent. In fact,
`you can self-host a Plausible server <https://www.elvisduru.com/blog/how-to-self-host-plausible-analytics>`__.

.. admonition:: Get a self-hosted Plausible server at ``scientific-python.org``
   :class: tip

   If your documentation is for a package that is part of the SciPy / PyData
   ecosystem, they might be able to host a Plausible server for you at
   `<your-package>.scientific-python.org`.
   To ask about this, contact them on the social media platform of your choice
   and learn more at `scientific-python.org <https://scientific-python.org>`__.

Plausible Analytics
===================

https://plausible.io can be used to gather simple
and privacy-friendly analytics for the site. The configuration consists in
a server URL and a specific domain. Plausible' javascript will be included in
all html pages to gather metrics. And the dashboard can be accessed at
``https://url/my_domain``.

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
