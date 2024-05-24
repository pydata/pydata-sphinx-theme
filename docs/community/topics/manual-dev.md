(manual-environment)=

# Set up a manual development environment

If you prefer not to use automation tools like `tox`, or want to have more control over the specific version of packages that you'd like installed,
you may set your local development environment manually.

To do so, follow the instructions on this page.

## Create a new development environment

This is optional, but it's best to start with a fresh development environment so that you've isolated the packages that you're using for this repository.

To do so, use a tool like [conda](https://docs.conda.io/en/latest/), [mamba](https://github.com/mamba-org/mamba), or [virtualenv](https://virtualenv.pypa.io/).

## Pre-requisites

Before you start, ensure that you have the following installed:

- Python >= 3.9
- [Pandoc](https://pandoc.org/installing.html): we use `nbsphinx` to support notebook (.ipynb) files in the documentation, which requires [installing Pandoc](https://pandoc.org/installing.html) at a system level (or within a Conda environment).

## Clone the repository locally

First clone this repository from the `pydata` organization, or from a fork that you have created:

```console
$ git clone https://github.com/pydata/pydata-sphinx-theme
$ cd pydata-sphinx-theme
```

## Install this theme locally

Next, install this theme locally so that we have the necessary dependencies to build the documentation and testing suite:

```console
$ pip install -e ".[dev]"
```

Note that the `sphinx-theme-builder` will automatically install a local copy of `nodejs` for building the theme's assets.
This will be placed in a `.nodeenv` folder.

## Build the documentation

To manually build the documentation, run the following command:

```console
$ sphinx-build docs docs/_build/html
```

## Compile web assets (JS/CSS)

To compile the JavaScript and CSS assets for the theme, run the following command:

```console
$ stb compile
```

This will compile everything in the `src/pydata_sphinx_theme/assets` folder and place them in the appropriate places in our theme's folder structure.

## Start a live server to build and serve your documentation

To manually open a server to watch your documentation for changes, build them, and display them locally in a browser, run this command:

```console
$ stb serve docs --open-browser
```

## Run the tests

To manually run the tests for this theme, first set up your environment locally, and then run:

```console
$ pytest
```
