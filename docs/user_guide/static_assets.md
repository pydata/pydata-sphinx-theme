# Add custom CSS and JS assets

If you'd like to modify this theme or sections on the page, you'll need to add custom CSS or JavaScript to your theme.
Since this is a common operation we cover a few ways to do this here.

````{admonition} Sample site structure
In all examples below, assume we have a site structure like this:

```
mysphinxsite/
├── _static
│   ├── mycss.css
│   └── myjs.js
└── conf.py
```
````

## First: define your `html_static_path`

Any folders that are listed in `html_static_path` will be treated as containing static assets for your build.
All files within these folders will be copied to your build's `_static` folder at build time.
For example, with an HTML builder, files will be copied to `_build/html/_static`.

These files are _flattened_ when they are copied, so any folder hierarchies will be lost.

Listing folders with your static assets must be done before any of the methods described below.
When you define asset names in the methods described below, they generally assume paths that are _relative to this `_static` output folder_.

## Define a list of assets in `conf.py`

The simplest way to add JS and CSS assets is to use [`html_css_files`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_css_files) and [`html_js_files`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_js_files) in your `conf.py` file.
Each can be a list of paths, _relative to your `html_static_path`_.
They will be added to the end of the `<head>` of your site.

For example:

```{code-block} python
---
caption: '`conf.py`'
---

html_static_path = ["_static"]
html_css_files = ["mycss.css"]
html_js_files = ["myjs.js"]
```

This will cause each to be linked in your `<head>`.

## Add assets to your setup function

Additionally, you may add assets manually, to do so, use the `app` object in [the Sphinx `setup()` function](https://www.sphinx-doc.org/en/master/extdev/appapi.html#extension-setup).
The `app` object has two relevant methods here:

[**`app.add_css_file`**](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_css_file) allows you to add CSS files directly.

[**`app.add_js_file`**](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_js_file) allows you to add JS files directly.

Both of them expect you to add files **relative to the `html_static_path`**.

In addition, `app.add_js_file` allows you to add _raw JavaScript_ in addition to linking files (see example below).
For example:

```{code-block} python
---
caption: '`conf.py`'
---

html_static_path = ["_static"]

def setup(app):
  app.add_css_file("mycss.css")
  app.add_js_file("myjs.js")

  # Add raw JavaScript
  rawjs = """
  let a = "foo";
  console.log(a + " bar")
  """
  app.add_js_file(None, body=rawjs)
```

## Use an event to add it to specific pages

If you'd like to use logic to only add a script to certain pages or to trigger different behavior depending on the page, use [a Sphinx event hook](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx-core-events).
This involves defining a function that runs when a particular event is emitted in the Sphinx build, and using [`app.connect()`](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.connect) to connect it to your build.

The event you'll likely want to use is [`html-page-context`](https://www.sphinx-doc.org/en/master/extdev/appapi.html#event-html-page-context).
This is triggered just before the HTML for an _individual page_ is created.
If you run `app.add_js_file` or `app.add_css_file`, it will _only be added for that page_.

For example:

```{code-block} python
---
caption: '`conf.py`'
---
html_static_path = ["_static"]

def add_my_files(app, pagename, templatename, context, doctree):
  if pagename == "dontaddonthispage":
    return

  app.add_css_file("mycss.css")

def setup(app):
  app.connect("html-page-context", add_my_files)
```

## Add it directly to the page content

Finally, you can add CSS or JS directly to a page's content.
If you're using reStructuredText you can use the `.. raw::` directive; if you're using MyST Markdown you can simply include the HTML content in-line with your Markdown-formatted content.

``````{tab-set}
`````{tab-item} rST
````{code-block} rst
:caption: some_page_in_my_site.rst
My title
========

Some text

.. raw:: html

    <style>
      /* Make h2 bigger */
      h2 {
        font-size: 3rem;
      }
    </style>

A bigger title
--------------

Some other text
````
`````
`````{tab-item} Markdown
````{code-block} md
:caption: some_page_in_my_site.md
# My title

Some text

<style>
  /* Make h2 bigger */
  h2 {
    font-size: 3rem;
  }
</style>

## A bigger title

Some other text
````
`````
``````
