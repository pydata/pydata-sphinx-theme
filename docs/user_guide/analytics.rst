============================
Analytics and usage services
============================

The theme supports several web analytics services via the ``analytics`` option. It is configured
by passing a dictionary with options. See the sections below for relevant
options depending on the analytics provider that you want to use.

.. code:: python

   html_theme_options = {
       # See below for options for each service
       "analytics": analytics_options,
   }

Generally speaking, we recommend using Plausible over Google Analytics because
it has a better story around user security and privacy. In addition, it is more
open-source and transparent. In fact,
`you can self-host a Plausible server <https://www.elvisduru.com/blog/how-to-self-host-plausible-analytics>`__.

.. admonition:: Get a self-hosted Plausible server at ``scientific-python.org``
   :class: tip

   If your documentation is for a package that is part of the SciPy / PyData
   ecosystem, they might be able to host a Plausible server for you at
   ``https://views.scientific-python.org/<your-package>``.
   To ask about this, contact them on the social media platform of your choice
   and learn more at `scientific-python.org <https://scientific-python.org>`__.

Plausible Analytics
===================

`plausible.io <https://plausible.io>`__ can be used to gather simple
and privacy-friendly analytics for the site. To configure, you will need to provide two things:

- A URL pointing to the JavaScript analytics script that is served by your Plausible server
- A domain that reflects where your documentation lives

Plausible's JavaScript will be included in all HTML pages to gather metrics.
The dashboard with analytics results will be accessible at ``https://<plausible-url>/<my-domain>``.

.. code:: python

   html_theme_options["analytics"] = {
       # The domain you'd like to use for this analytics instance
       "plausible_analytics_domain": "my-domain",
       # The analytics script that is served by Plausible
       "plausible_analytics_url": "https://.../script.js",
   }

.. seealso::

  See the `Plausible Documentation <https://plausible.io/docs/plausible-script>`__ for more information about this script.

Google Analytics
================

If the ``google_analytics_id`` config option is specified (like ``G-XXXXXXXXXX``),
Google Analytics' JavaScript is included in the HTML pages.

.. code:: Python

   html_theme_options["analytics"] = {
       "google_analytics_id": "G-XXXXXXXXXX",
   }
