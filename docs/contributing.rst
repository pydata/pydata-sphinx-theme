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


Contributing changes
====================

We follow the typical GitHub workflow of forking a repo, creating a branch,
opening pull requests (https://guides.github.com/introduction/flow/).

For each pull request, the demo site gets build to make it easier to preview
the changes in the PR. To access this, click on "Details" of the "build_docs artifact"
job of Circle CI:

.. image:: _static/pull-request-preview-link.png


Ensuring correct commits with pre-commit hooks
==============================================

To ensure all source files have been correctly build, a `pre-commit <https://pre-commit.com/>`__
hook is available to use.

To set this up, first install the ``pre-commit`` package::

    # with pip
    pip install pre-commit
    # or with conda
    conda install pre-commit -c conda-forge

and then running from the root of this repo::

    pre-commit install

Now all of the checks will be run each time you commit changes.

Note that if needed, you can skip these checks with ``git commit --no-verify``.
