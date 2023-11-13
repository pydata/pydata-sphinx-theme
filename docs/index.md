---
myst:
  html_meta:
    "description lang=en": |
      Top-level documentation for pydata-sphinx theme, with links to the rest
      of the site..
html_theme.sidebar_secondary.remove: true
---

# The PyData Sphinx Theme

A clean, Bootstrap-based Sphinx theme by and for [the PyData community](https://pydata.org).

```{gallery-grid}
:grid-columns: 1 2 2 3

- header: "{fab}`bootstrap;pst-color-primary` Built with Bootstrap"
  content: "Use Bootstrap classes and functionality in your documentation."
- header: "{fas}`bolt;pst-color-primary` Responsive Design"
  content: "Site sections will change behavior and size at different screen sizes."
- header: "{fas}`circle-half-stroke;pst-color-primary` Light / Dark theme"
  content: "Users can toggle between light and dark themes interactively."
- header: "{fas}`palette;pst-color-primary` Customizable UI and themes"
  content: "Customize colors and branding with CSS variables, and build custom UIs with [Sphinx Design components](user_guide/web-components)."
- header: "{fab}`python;pst-color-primary` Supports PyData and Jupyter"
  content: "CSS and UI support for [Jupyter extensions](examples/execution) and [PyData execution outputs](examples/pydata.ipynb)."
- header: "{fas}`lightbulb;pst-color-primary` Example Gallery"
  content: "See [our gallery](examples/gallery.md) of projects that use this theme."
```

```{seealso}
If you are looking for a Sphinx theme that puts all of its sub-pages in the sidebar, the [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/) has a similar look and feel, and [Furo](https://pradyunsg.me/furo/quickstart/) is another excellent choice. You can also see [the Sphinx Themes Gallery](https://sphinx-themes.org) for more ideas.
```

## User Guide

Information about using, configuration, and customizing this theme.

```{toctree}
:maxdepth: 2

user_guide/index
```

## Community and contribution guide

Information about the community behind this theme and how you can contribute.

```{toctree}
:maxdepth: 2

community/index
```

## Examples

Several example pages to demonstrate the functionality of this theme when used alongside other Sphinx extensions.

```{toctree}
:maxdepth: 2

examples/index
```

```{toctree}
:hidden:

Changelog <https://github.com/pydata/pydata-sphinx-theme/releases>
```

## API

The content of the exposed `pydata_sphinx_theme` API.

```{toctree}
:maxdepth: 2

API <api/index>
```
