************
Contributing
************

The documentation for this theme (what you are looking at now) also serves
as a demo site for the theme.

.. Hint::

    The top-level `Demo site` section includes
    more pages with typical Sphinx content and structural elements.


Installing Python dependencies
==============================

To run the demo site, first install the Python dependencies, for example with ``pip``
or ``conda``:

.. code-block:: bash

    # with pip
    python -m pip install -r docs/requirements.txt
    # or with conda
    conda install -c conda-forge --file docs/requirements.txt


Installing this theme
=====================

Next, install this theme itself, a python package.
When developing, it is recommended to install in "development" or "editable" mode,
allowing changes in the repo to be directly tested with this documentation suite.

To install the package, from the root of this repo, run:

.. code-block:: bash

    python -m pip install --editable .


Building the demo site
======================

For a traditional Sphinx build of the demo site, navigate to the ``docs/`` directory,
and run:

.. code-block:: bash

    make html

Sphinx will build the HTML version of the site in the ``docs/_build/html`` directory.

.. Note::

    If you wish to customize the CSS or JS beyond what is available in the
    :ref:`configuration` and :ref:`customizing` sections of the user guide,
    extra steps are required. The next section covers the full workflow, from
    changing the source files, to seeing the updated site.


Developing the theme CSS and JS
===============================

The CSS and JS for this theme are built for the browser from ``src/*`` with
`webpack <https://webpack.js.org/>`__. The main entrypoints are:

- CSS: ``src/scss/index.scss``

  - the main part of the theme assets
  - customizes `Bootstrap <https://getbootstrap.com/>`__ with `Sass <https://sass-lang.com>`__
  - points to the ``font-face`` of vendored web fonts, but does not include their
    CSS ``@font-face`` declaration

- JS: ``src/js/index.js``

  - provides add-on Bootstrap features, as well as some custom navigation behavior

- webpack: ``webpack.common.js``

  - captures the techniques for transforming the JS and CSS source files in
    ``src/`` into the production assets in ``pydata_sphinx_theme/static/``

These entrypoints, and all files they reference, are bundled into
``pydata_sphinx_theme/static/{css,js}/index.<hash>.{css,js}``.

The ``<hash>`` ensures the correct asset versions are served when viewers return to your
site after upgrading the theme, and is reproducibly derived from ``src/**/*``,
``webpack.{common,prod}.js``, and the ``dependencies`` and ``devDependencies``
in ``package.json``/``yarn.lock``.

Web fonts, and their supporting CSS, are copied into
``pydata_sphinx_theme/static/vendor/<font name>/<font version>/``. Including
the ``<font version>`` also ensures the correct assets are served when upgrading.

The links to these unique file names are captured as Jinja2 macros in
``pydata_sphinx_theme/static/webpack-macros.html``.

Finally, all of these files are committed to the repo, in-place, along with the
rest of the code. This allows use of the theme directly from a ``git`` checkout,
without any of the finicky web development dependencies, or even a ``nodejs``
runtime.

.. Hint::

    Theme development was inspired by the
    `ReadTheDocs Sphinx theme <https://github.com/readthedocs/sphinx_rtd_theme>`__.


Steps to develop the theme
--------------------------

1. Install ``yarn``
2. Install theme dependencies
3. Run development server
4. Build production assets
5. Install the testing infrastructure

.. Attention::

    In order to commit changes to the theme, ensure you run
    ``yarn build:production`` so all built assets will be bundled, copied, or
    generated into ``pydata_sphinx_theme/static/``.


Installing ``yarn``
^^^^^^^^^^^^^^^^^^^

`Yarn <https://yarnpkg.com>`__ is a package manager for JS and CSS dependencies.
Yarn itself can be installed with a number of
`package managers <https://classic.yarnpkg.com/en/docs/install>`__, including
``conda``:

.. code-block:: bash

    conda install -c conda-forge yarn


Installing JS dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^

To install theme-related ``dependencies`` and ``devDependencies`` from ``package.json``,
from the root of this repo, run:

.. code-block:: bash

    yarn

After adding/updating dependencies with ``yarn add``, or manually changing ``package.json``
and re-running ``yarn``, the ``yarn.lock`` and ``package.json`` files will likely change.

.. Important::

    If changed, commit ``package.json`` and ``yarn.lock`` together to ensure
    reproducible builds.


Running the development server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To preview the frontend assets, from the root of this repo, run:

.. code-block:: bash

    yarn build:dev

This launches a development server at http://127.0.0.1:1919. When working
on the theme, saving changes to any of:

- ``src/js/index.js``
- ``src/scss/index.scss``
- ``docs/**/*.rst``
- ``docs/**/*.py``

...causes the development server to reload:

- bundle/copy the CSS, JS, and vendored fonts
- regenerate the Jinja2 macros
- re-run Sphinx


Building the production assets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build the new theme assets into the python package, from the root of this repo,
run:

.. code-block:: bash

    yarn build:production


Install the test infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This theme uses ``pytest`` for its testing, with a lightweight fixture defined
in the ``test_build.py`` script that makes it easy to run a Sphinx build using
this theme and inspect the results.

In addition, we use `pytest-regressions <https://pytest-regressions.readthedocs.io/en/latest/>`_
to ensure that the HTML generated by the theme is what we'd expect. This module
provides a ``file_regression`` fixture that will check the contents of an object
against a reference file on disk. If the structure of the two differs, then the
test will fail. If we *expect* the structure to differ, then delete the file on
disk and run the test. A new file will be created, and subsequent tests will pass.

Install the testing dependencies with:

.. code-block:: bash

   pip install pytest pytest-regressions

Then run the tests by calling ``pytest`` from the repository root.

Changing fonts
--------------

Three "styles" of the `FontAwesome 5 Free <https://fontawesome.com/icons?m=free>`__
icon font are used for :ref:`icon links <icon-links>` and admonitions, and is
the only `vendored` font. Further font choices are described in the :ref:`customizing`
section of the user guide, and require some knowledge of HTML and CSS.

.. Attention::

    Previously-included fonts like `Lato` have been removed, preferring
    the most common default system fonts of the reader's computer. This provides
    both better performance, and better script/glyph coverage than custom fonts,
    and is recommended in most cases.

The remaining vendored font selection is:

- managed as a dependency in ``package.json``

  - allowing the version to be managed centrally

- copied directly into the site statics, including licenses

  - allowing the chosen font to be replaced (or removed entirely) with minimal
    templating changes: practically, changing the icon font is difficult at this
    point.

- partially preloaded

  - reducing flicker and re-layout artifacts of early icon renders

- mostly managed in ``webpack.common.js``

  - allowing upgrades to be handled in a relatively sane, manageable way, to
    ensure the most recent icons


Upgrading a font
^^^^^^^^^^^^^^^^

If *only* the version of the `existing` font must change, for example to enable
new icons, run:

.. code-block:: bash

    yarn add <font name>@<version>
    yarn build:production

It *may* also be necessary to clear out old font versions from
``pydata_sphinx_theme/static/vendor/`` before committing.


Changing a font
^^^^^^^^^^^^^^^

If the above doesn't work, for example if file names for an existing font change,
or a new font variant altogether is being added, hand-editing of ``webpack.common.js``
is required. The steps are roughly:

- install the new font, as above, with ``yarn add``
- in ``webpack.common.js``:

  - add the new font to ``vendorVersions`` and ``vendorPaths``
  - add new ``link`` tags to the appropriate macro in ``macroTemplate``
  - add the new font files (including the license) to ``CopyPlugin``
  - remove references to the font being replaced/removed, if applicable

- restart the development server, if running
- rebuild the production assets, as above, with ``yarn build:production``
- potentially remove the font being replaced from ``package.json`` and re-run ``yarn``
- commit all of the changed files


Contributing changes
====================

We follow a `typical GitHub workflow <https://guides.github.com/introduction/flow/>`__
of:

- create a personal fork of this repo
- create a branch
- open a pull request
- fix findings of various linters and checks
- work through code review

For each pull request, the demo site is built and deployed to make it easier to review
the changes in the PR. To access this, click on the "ReadTheDocs" preview in the CI/CD jobs.


Ensuring correct commits
========================

To ensure all source files have been correctly built, a `pre-commit <https://pre-commit.com/>`__
hook is available.

To set this up, first install the ``pre-commit`` package:

.. code-block:: bash

    # with pip
    pip install pre-commit
    # or with conda
    conda install -c conda-forge pre-commit

Then, from the root of this repo, run:

.. code-block:: bash

    pre-commit install

Now all of the checks will be run each time you commit changes.

Note that if needed, you can skip these checks with:

.. code-block:: bash

    git commit --no-verify


Finding accessibility problems
==============================

The accessibility checking tools can find a number of common HTML patterns which
assistive technology can't help users understand.

In addition to `Lighthouse <https://developers.google.com/web/tools/lighthouse>`__
in CI, the ``pa11y`` stack is installed as part of the development environment.

The key components are:

- `pa11y <https://github.com/pa11y/pa11y>`__ which uses a headless browser to analyze
  an HTML page with a configurable set of rules based on publish standards
- `Pa11y-CI <https://github.com/pa11y/pa11y-ci>`__ runs ``pa11y`` on multiple pages
- `pa11y-reporter-html <https://github.com/pa11y/pa11y-reporter-html>`__ generates
  some nice HTML reports, suitable for review

.. Note::

    Presently, the *default* ``pa11y`` ruleset, ``WCAG2AA`` is used, a subset of
    the `Web Content Accessibility Guidelines <https://www.w3.org/TR/WCAG21>`__.
    The `Quick Reference <https://www.w3.org/WAI/WCAG21/quickref>`__ may provide
    lighter reading.

To run the accessibility problem finder locally:

.. code-block:: bash

    yarn build:production
    cd docs
    make html
    python a11y.py

The output of the last command includes:

- a short summary of the current state of the accessibility rules we are trying to maintain
- local paths to JSON and HTML reports which contain all of the issues found


Fixing accessibility errors
---------------------------

Start by checking for issues on the
`accessibility roadmap <https://github.com/pandas-dev/pydata-sphinx-theme/blob/master/docs/a11y-roadmap.txt>`__.
These are issues which are currently flagged by the toolset, but that have not yet
been fixed. If that file is empty (or just comments), hooray!

To start working on one of the accessibility roadmap items, comment out one of the
lines in `docs/a11y-roadmap.txt`, and re-run the audit to establish a baseline.

Then, fix the issue in either the HTML templates, CSS, or python code, and re-run
the audit until it is fixed.


Make a release
==============

This theme uses GitHub tags and releases to automatically push new releases to
PyPI. For information on this process, see `the release checklist <https://github.com/pydata/pydata-sphinx-theme/wiki/Release-checklist#release-instructions>`_.

.. meta::
    :description lang=en:
        How to become a contributor to the pydata-sphinx-theme.
