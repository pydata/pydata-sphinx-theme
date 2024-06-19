# Get started with development

This section covers the simplest way to get started developing this theme locally so that you can contribute.
It uses automation and as few steps as possible to get things done.

If you are comfortable with and prefer a more manual setup refer to the [](topics/manual-dev.md) section.

## Testing pre-release and nightly

You can test the alpha, beta
and release candidates of pydata sphinx theme on your your projects. To do so
simply install with pip using the `--pre` flag:

```console
$ pip install --pre pydata-sphinx-theme
```

If an `alpha`, `beta` or `rc` is available, pip will install it.

You can use the `--pre` flag in your project's continuous integration test suite
to catch regressions or bugs before their release.

If you are even more adventurous pydata-sphinx-theme has nightly builds, you can try following the
instructions provided [on the scientific-python/upload-nightly-action
Readme](https://github.com/scientific-python/upload-nightly-action?tab=readme-ov-file#using-nightly-builds-in-ci)
on installing nightly wheels.

Installing nightly wheels in your project's CI jobs is a great way to help theme developers catch bugs ahead of
time.

## Workflow for contributing changes

We follow a [typical GitHub workflow](https://guides.github.com/introduction/flow/)
of:

- create a personal fork and local clone of this repo
- create a branch for your contribution
- open a pull request
- fix findings of various linters and checks
- work through code review

For each pull request (PR), the documentation is built and deployed to make it easier to review the changes in the PR.
To access this preview, click on the {{ rtd }} preview in the CI/CD jobs (GitHub checks section
at the bottom of a PR, note you might need to click on "Show all checks" to access the job).

The sections below cover the contribution steps in more detail.

## Clone the repository

First off you'll need your copy of the `pydata-sphinx-theme` codebase.
You can clone it for local development like so:

1. **Fork the repository**, so you have your own copy on GitHub.
   See [the GitHub forking guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo) for more information.
2. **Clone the repository locally** so that you have a local copy to work from:

   ```console
   $ git clone https://github.com/{{ YOUR USERNAME }}/pydata-sphinx-theme
   $ cd pydata-sphinx-theme
   ```

## Install your tools

Building a Sphinx site uses a combination of Python and `Jinja` to manage `HTML`, `scss`, and `JavaScript`.
To simplify this process, we use a few helper tools:

- [The Sphinx Theme Builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) compiles web assets in an automated way.
- [pre-commit](https://pre-commit.com/) for automatically enforcing code standards and quality checks before commits.
- [tox](https://tox.wiki/en/latest/index.html) for automating common development tasks.
- [pandoc](https://pandoc.org/) the universal document converter.

In particular, `tox` can be used to automatically create isolated local development environments with all the correct packages installed to work on the theme.
The rest of this guide focuses on using `tox` to start with a basic environment.

```{seealso}
The information on this page covers the basics to get you started, for information about manually compiling assets, see [](topics/manual-dev.md).
```

### Setup `tox`

To start, install `tox`:

```console
$ pip install tox
```

You can call `tox` from the command line to perform common actions that are needed in building the theme.
`tox` operates with isolated environments, so each action has its packages installed in a local directory (`.tox`).
For common development actions, you'll only need to use `tox` and won't need to set up any other packages.

### Setup `pre-commit`

`pre-commit` allows us to run several checks on the codebase every time a new Git commit is made.
This ensures standards and basic quality control for our code.

Install `pre-commit` with the following command:

```console
$ pip install pre-commit
```

then navigate to this repository's folder and activate it like so:

```console
$ pre-commit install
```

This will install the necessary dependencies to run `pre-commit` every time you make a commit with Git.

```{note}
Your `pre-commit` dependencies will be installed in the environment from which you're calling `pre-commit`, `tox`, etc.
They will not be installed in the isolated environments used by `tox`.
```

Alternatively, if you do not want to install pre-commit and its dependencies globally, you can use `tox` to run the checks:

```python
tox -e run lint
```

The caveat to using `tox` is that this will not install the required hooks to run the checks automatically before each commit, so you need to run this manually.

## Build the documentation

Now that you have `tox` installed and cloned the repository, you should be able to build the documentation locally.

To build the documentation with `tox`, run the following command:

```console
$ tox run -e docs-dev
```

This will install the necessary dependencies and build the documentation located in the `docs/` folder.
The generated documentation will be placed in a `docs/_build/html` folder.
If the docs have already been built, it will only rebuild the pages that have been updated.
You can open one of the HTML files there to preview the documentation locally.

Alternatively, you can invoke the built-in Python [http.server](https://docs.python.org/3/library/http.server.html#module-http.server) with:

```console
$ python -m http.server -d docs/_build/html/
```

This will print a local URL that you can open in a browser to explore the HTML files.

### Change content and re-build

Now that you've built the documentation, edit one of the source files to see how the documentation updates with new builds.

1. **Make an edit to a page**. For example, add a word or fix a typo on any page.
2. **Rebuild the documentation** with `tox run -e docs-dev`

It should go much faster this time because `tox` is re-using the previously created environment, and because Sphinx has cached the pages that you didn't change.

## Compile the CSS/JS assets

The source files for CSS and JS assets are in `src/pydata_sphinx_theme/assets`.
These are then built and bundled with the theme (e.g., `scss` is turned into `css`).

To compile the CSS/JS assets with `tox`, run the following command:

```console
$ tox run -e compile
```

This will compile all assets and place them in the appropriate folder to be used with documentation builds.

```{note}
Compiled assets are **not committed to git**.
The `sphinx-theme-builder` will bundle these assets automatically when we make a new release, but we do not manually commit these compiled assets to Git history.
```

## Run a development server

You can combine the above two actions (build the docs and compile JS/CSS assets) and run a development server so that changes to `src/` are automatically bundled with the package, and the documentation is immediately reloaded in a live preview window.

To run the development server with `tox`, run the following command:

```console
$ tox run -e docs-live
```

When working on the theme, making changes to any of these directories:

- `src/js/index.js`
- `src/scss/index.scss`
- `docs/**/*.rst`
- `docs/**/*.md`
- `docs/**/*.py`

will cause the development server to do the following:

- bundle/copy the CSS, JS, and vendored fonts
- regenerate the Jinja2 macros
- re-run Sphinx

## Run the tests

This theme uses `pytest` and `playwright` for testing. There is a lightweight fixture defined
in the `test_build.py` script that makes it straightforward to run a Sphinx build using
this theme and inspect the results. There are also several automated accessibility checks in
`test_a11y.py`.

```{warning}
Currently, the automated accessibility tests check the Kitchen Sink page only.
We are working on extending coverage to the rest of the theme.
```

In addition, we use
[pytest-regressions](https://pytest-regressions.readthedocs.io/en/latest/) to
ensure that the HTML generated by the theme is what we'd expect. This module
provides a `file_regression` fixture that will check the contents of an object
against a reference file on disk. If the structure of the two differs, then the
test will fail. If we _expect_ the structure to differ, then delete the file on
disk and run the test. A new file will be created, and subsequent tests will
pass.

To run the build tests with `tox`, run the following command:

```console
# this will compile the assets and run the tests (with test coverage)
# note the use of the `-m` flag vs. other commands in this guide
$ tox run -m tests

# to run the tests only without pre-compiling the assets and without coverage (for example if you recently compiled the assets)
$ tox run -e tests-no-cov
```

To run the accessibility checks:

```console
# this will compile the assets, build the documentation, and run the accessibility tests
$ tox run -m a11y

# to run the tests without pre-compiling the assets and without re-building the docs (for example if you recently compiled the assets or built the docs)
$ tox run -e a11y-tests
```

## GitHub Codespaces

If you have good internet connectivity and want a temporary set-up, it is often faster to work on the PyData Sphinx Theme
in a Codespaces environment.
Once your Codespaces instance is set up, you can run the `tox` commands above to build the documentation, compile the assets, and run the tests.
For documentation on how to get started with Codespaces, see [the Codespaces documentation](https://docs.github.com/en/codespaces).
