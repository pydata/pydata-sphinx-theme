# PyData Sphinx Theme Styles Folder

This `assets/styles/` folder contains all of the CSS that the theme adds to
projects that use it.

It follows the [Sphinx Theme Builder's expected Filesystem
Layout](https://sphinx-theme-builder.readthedocs.io/en/latest/filesystem-layout/).

## How does it work?

The CSS is written in Sass (SCSS) and broken across multiple files for better
code organization. These files are imported into a single main file named
`pydata-sphinx-theme.scss`. That file is compiled into a plain CSS file when the
theme is installed or packaged. This is handled by the Sphinx Theme Builder when
it runs the `stb compile` command. This command in turns calls `webpack`, which
is configured in `webpack.config.js`.

How does `webpack` find the main SCSS file for compilation? The SCSS file is
imported by the main JavaScript file for this site, `pydata-sphinx-theme.js`,
and the path to that JavaScript file is in the `webpack` config file.

## Sub-folders

Here are some notes about some of the sub-folders in this directory:

- `abstracts/` contains SCSS variables (**not** CSS variables), functions,
  mixins and other re-usable SCSS constructs to be imported by other SCSS
- `extensions/` contains styles for Sphinx extensions that commonly co-occur
  with this theme
- `variables/` strictly for files that output CSS custom properties (variables)

## SCSS versus CSS variables

Read the [SCSS variables](https://sass-lang.com/documentation/variables/)
documentation for a summary of the differences between CSS and SCSS variables.

- SCSS variables that are meant to be shared across SCSS files go in
  `abstracts/_vars.scss`.
- CSS variables go into one of the files in the `variables/` folder. These
  variables will be defined on every web page that uses the theme.
