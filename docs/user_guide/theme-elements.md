# Theme-specific elements

There are a few elements that are unique or particularly important to this theme.
Some of these are triggered with configuration or Markdown syntax that is unique to the theme, and we cover them below.

## Mathematics

Most Sphinx sites support math, but it is particularly important for scientific computing, so we illustrate support here as well.

Here is an inline equation: {math}`X_{0:5} = (X_0, X_1, X_2, X_3, X_4)` and {math}`another` and {math}`x^2 x^3 x^4` another. And here's one to test vertical height {math}`\frac{\partial^2 f}{\partial \phi^2}`.
Here is a block-level equation:

```{math}
:label: My label

\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
```

And here is a really long equation with a label!

```{math}
:label: My label 2

\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
\nabla^2 f =
\frac{1}{r^2} \frac{\partial}{\partial r}
\left( r^2 \frac{\partial f}{\partial r} \right) +
\frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
\left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
\frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}
```

You can add a link to equations like the one above {eq}`My label` and {eq}`My label 2`.

## Code blocks

Code block styling is inspired by [GitHub's code block style](https://primer.style/components/markdown) and also has support for Code Block captions/titles.
See [the Sphinx documentation on code blocks](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block) for more information.

```python
print("A regular code block")
print("A regular code block")
print("A regular code block")
```

You can also provide captions with code blocks, which will be displayed right above the code.
For example, the following code:

``````{tab-set}
`````{tab-item} rST
````rst
.. code-block:: python
    :caption: python.py

    print("A code block with a caption.")
````
`````
`````{tab-item} Markdown
````md
```{code-block} python
:caption: python.py

print("A code block with a caption.")
```
````
`````
``````

results in:

```{code-block} python
:caption: python.py

print("A code block with a caption.")
```

You can also display line numbers.
For example, the following code:

``````{tab-set}
`````{tab-item} rST
````rst
..  code-block:: python
    :caption: python.py
    :linenos:

    print("A code block with a caption and line numbers.")
    print("A code block with a caption and line numbers.")
    print("A code block with a caption and line numbers.")
````
`````
`````{tab-item} Markdown
````md
```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```
````
`````
``````

results in:

```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```

## Inline code

When used directly, the `code` role just displays the text without syntax highlighting, as a literal. As mentioned in the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#inline-code-highlighting) you can also enable syntax highlighting by defining a custom role. It will then use the same highlighter as in the `code-block` directive.

``````{tab-set}
`````{tab-item} rst
````rst
.. role:: python(code)
   :language: python

In Python you can :python:`import sphinx`.
````
`````
`````{tab-item} markdown
````md
```{role} python(code)
:language: python
```

In Python you can {python}`import sphinx`.
````
`````
``````

```{role} python(code)
:language: python
```

In Python you can {python}`import sphinx`.

## Code execution

This theme has support for Jupyter execution libraries so that you can programmatically update your documentation with each build.
For examples, see [](../examples/pydata.ipynb).

## Admonition sidebars

```{admonition} A sidebar admonition!
:class: sidebar note
I was made with the `{admonition}` directive and a `sidebar` class.
```

```{sidebar} Sidebar title
I was made with the `{sidebar}` directive.
```

This theme supports a shorthand way of making **admonitions behave like sidebars**.
This can be a helpful way of highlighting content without interrupting the vertical flow as much.

For example, on the right are an "admonition sidebar" and a traditional Sphinx sidebar.

To make an admonition behave like a sidebar, add the `sidebar` class to its list of classes.
The admonition sidebar in this section was created with the following Markdown:

``````{tab-set}
`````{tab-item} rST
````rst
.. admonition:: A sidebar admonition!
    :class: sidebar note

    Some sidebar content.
````
`````
`````{tab-item} Markdown
````md
```{admonition} A sidebar admonition!
:class: sidebar note
Some sidebar content.
```
````
`````
``````

## Footnotes

Here's a numeric footnote[^1], another one (preceded by a space) [^2], a named footnote[^named], and a symbolic one[^*].
All will end up as numbers in the rendered HTML, but in the source they look like `[^1]`, `[^2]`, `[^named]` and `[^*]`.

[^1]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

[^2]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

[^named]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

[^*]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

## Link shortening for git repository services

Many projects have links back to their issues / PRs hosted on platforms like **GitHub** or **GitLab**.
Instead of displaying these as raw links, this theme does some lightweight formatting for these platforms specifically.

In **reStructuredText**, URLs are automatically converted to links, so this works automatically.

In **MyST Markdown**, by default, you must define a standard Markdown link and duplicate the URL in the link text.
You may skip the need to manually define the link text by [activating the MyST Linkify extension](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#linkify).

For example:

- **reStructuredText**

  - `https://github.com/pydata/pydata-sphinx-theme/pull/1012`
  - https://github.com/pydata/pydata-sphinx-theme/pull/1012

- **MyST Markdown (default)**

  - `[https://github.com/pydata/pydata-sphinx-theme/pull/1012](https://github.com/pydata/pydata-sphinx-theme/pull/1012)`
  - [https://github.com/pydata/pydata-sphinx-theme/pull/1012](https://github.com/pydata/pydata-sphinx-theme/pull/1012)

- **MyST Markdown with [MyST Linkify](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#linkify)**
  - `https://github.com/pydata/pydata-sphinx-theme/pull/1012`
  - https://github.com/pydata/pydata-sphinx-theme/pull/1012

There are a variety of link targets supported, here's a table for reference:

**GitHub**

- `https://github.com`: https://github.com
- `https://github.com/pydata`: https://github.com/pydata
- `https://github.com/pydata/pydata-sphinx-theme`: https://github.com/pydata/pydata-sphinx-theme
- `https://github.com/pydata/pydata-sphinx-theme/pull/1012`: https://github.com/pydata/pydata-sphinx-theme/pull/1012
- `https://github.com/orgs/pydata/projects/2`: https://github.com/orgs/pydata/projects/2

**GitLab**

- `https://gitlab.com`: https://gitlab.com
- `https://gitlab.com/gitlab-org`: https://gitlab.com/gitlab-org
- `https://gitlab.com/gitlab-org/gitlab`: https://gitlab.com/gitlab-org/gitlab
- `https://gitlab.com/gitlab-org/gitlab/-/issues/375583`: https://gitlab.com/gitlab-org/gitlab/-/issues/375583

Links provided with a text body won't be changed.
