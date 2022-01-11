# Get started with development

This section covers the simplest way to get started developing this theme locally so that you can contribute.
It uses automation and as few steps as possible to get things done.
If you'd like to do more operations manually, see [](manual.md).

## Clone the repository

First off you'll need your own copy of the `pydata-sphinx-theme` codebase.
You can clone it for local development like so:

1. **Fork the repository** so you have your own copy on GitHub.
   See [the GitHub forking guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo) for more information.
2. **Clone the repository locally** so that you have a local copy to work from:

   ```console
   $ git clone https://github.com/{{ YOUR USERNAME }}/pydata-sphinx-theme
   $ cd pydata-sphinx-theme
   ```

## Install your tools

Building a Sphinx site uses a combination of Python and Jinja to manage HTML, SCSS, and Javascript.
To simplify this process, we use a few helper tools:

- [The Sphinx Theme Builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) to automatically perform compilation of web assets.
- [pre-commit](https://pre-commit.com/) for automatically enforcing code standards and quality checks before commits.
- [nox](https://nox.thea.codes/), for automating common development tasks.

In particular, `nox` can be used to automatically create isolated local development environments with all of the correct packages installed to work on the theme.
The rest of this guide focuses on using `nox` to start with a basic environment.

```{seealso}
The information on this page covers the basics to get you started, for information about manually compiling assets, see [](manual.md).
```

### Setup `nox`

To start, install `nox`:

```console
$ pip install nox
```

You can call `nox` from the command line in order to perform common actions that are needed in building the theme.
`nox` operates with isolated environments, so each action has its own packages installed in a local directory (`.nox`).
For common development actions, you'll simply need to use `nox` and won't need to set up any other packages.

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

:::{note}
Your `pre-commit` dependencies will be installed in the environment from which you're calling `pre-commit`, `nox`, etc.
They will not be installed in the isolated environments used by `nox`.
:::

## Build the documentation

Now that you have `nox` installed and cloned the repository, you should be able to build the documentation locally.

To build the documentation with `nox`, run the following command:

```console
$ nox -s docs
```

This will install the necessary dependencies and build the documentation located in the `docs/` folder.
They will be placed in a `docs/_build/html` folder.
If the docs have already been built, it will only build new pages that have been updated.
You can open one of the HTML files there to preview the documentation locally.

Alternatively, you can invoke the built-in Python [http.server](https://docs.python.org/3/library/http.server.html#module-http.server) with:

```console
$ python -m http.server -d docs/_build/html/
```

This will print a local URL that you can open in a browser to explore the HTML files.

### Change content and re-build

Now that you've built the documentation, edit one of the source files to see how the documentation updates with new builds.

1. **Make an edit to a page**. For example, add a word or fix a typo on any page.
2. **Rebuild the documentation** with `nox -s docs`

It should go much faster this time, because `nox` is re-using the old environment, and because Sphinx has cached the pages that you didn't change.

## Compile the CSS/JS assets

The source files for CSS and JS assets are in `src/pydata_sphinx_theme/assets`.
These are then built and bundled with the theme (e.g., `scss` is turned into `css`).

To compile the CSS/JS assets with `nox`, run the following command:

```console
$ nox -s compile
```

This will compile all assets and place them in the appropriate folder to be used with documentation builds.

```{note}
Compiled assets are **not committed to git**.
The `sphinx-theme-builder` will bundle these assets automatically when we make a new release, but we do not manually commit these compiled assets to git history.
```

## Run a development server

You can combine the above two actions and run a development server so that changes to `src/` are automatically bundled with the package, and the documentation is immediately reloaded in a live preview window.

To run the development server with `nox`, run the following command:

```console
$ nox -s docs-live
```

When working on the theme, saving changes to any of these directories:

- `src/js/index.js`
- `src/scss/index.scss`
- `docs/**/*.rst`
- `docs/**/*.py`

will cause the development server to do the following:

- bundle/copy the CSS, JS, and vendored fonts
- regenerate the Jinja2 macros
- re-run Sphinx

## Run the tests

This theme uses `pytest` for its testing, with a lightweight fixture defined
in the `test_build.py` script that makes it easy to run a Sphinx build using
this theme and inspect the results.

In addition, we use [pytest-regressions](https://pytest-regressions.readthedocs.io/en/latest/)
to ensure that the HTML generated by the theme is what we'd expect. This module
provides a `file_regression` fixture that will check the contents of an object
against a reference file on disk. If the structure of the two differs, then the
test will fail. If we _expect_ the structure to differ, then delete the file on
disk and run the test. A new file will be created, and subsequent tests will pass.

To run the tests with `nox`, run the following command:

```console
$ nox -s test
```
