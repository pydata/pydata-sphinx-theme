# Web assets (CSS/JS/Fonts)

This theme includes several web assets to ease development and design.
The configuration for our asset compilation is in `webpack.config.js`.

## Compile and bundle assets

When assets are compiled, static versions are placed in various places in the theme's static folder:

```
src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static
```

For many assets, a `<hash>` is generated and appended to the end of its reference in the HTML templates of the theme.
This ensures the correct asset versions are served when viewers return to your
site after upgrading the theme.

To compile the assets and bundle them with the theme, run this command:

```console
$ tox -e run compile
```

## Styles (SCSS) and Scripts (JS)

There are two relevant places for CSS/JS assets:

- `src/pydata_sphinx_theme/assets/styles` has source files for SCSS assets. These will be compiled to CSS.
- `src/pydata_sphinx_theme/assets/scripts` has source files for JS assets. These will be compiled to JS and import several vendored libraries (like Bootstrap).
- `src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static` has compiled versions of these assets (e.g. CSS files). This folder is not tracked in `.git` history, but it is bundled with the theme's distribution.

## Vendored scripts

We vendor several packages in addition to our own CSS and JS.
For example, Bootstrap, JQuery, and Popper.
This is configured in the `webpack.config.js` file, and imported in the respective `SCSS` or `JS` file in our assets folder.

## FontAwesome icons

Three "styles" of the [FontAwesome 6 Free](https://fontawesome.com/icons?m=free)
icon font are used for {ref}`icon links <icon-links>` and admonitions and is
the only `vendored` font.

- It is managed as a dependency in `package.json`
- Copied directly into the site statics at compilation, including licenses
- Partially preloaded to reduce flicker and artifacts of early icon renders
- Configured in `webpack.config.js`

## Jinja macros

Our Webpack build generates a collection of [Jinja macros](https://jinja.palletsprojects.com/en/3.0.x/templates/#macros) in the `static/webpack-macros.html` file.

These macros are imported in the main `layout.html` file, and then inserted at various places on the page to link the static assets.

Some assets [are "preloaded"](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/preload), meaning that the browser begins requesting these resources before they're needed.
In particular, our JavaScript assets are preloaded in `<head>`, and the scripts are loaded at the end of `<body>`.
