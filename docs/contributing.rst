************
Contributing
************

The documentation of the theme (what you are looking at now) also serves
as a demo site for the theme. In the top-level "Demo site" section,
more pages with typical sphinx content and structural elements are included.

Installing
==========

To get this demo site up and running, you first need to install the requirements:
``/doc/requirements.txt`` (with for example pip or conda).

Then, you need to install the sphinx theme (the theme itself is a python package).
When developing, the easiest is to install it in "development" or "editable" mode,
which means you can make changes in the repo and directly test it with the docs.
To install, you can run this from the root of the repo::

    pip install --editable .

Building the demo docs
======================

Navigate to the `docs/` directory, and then run::

    make html

This will trigger sphinx to build the html version of the site. The output can
be found in the ``docs/_build/html`` directory.
