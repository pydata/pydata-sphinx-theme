# Theme-specific elements

There are a few elements that are unique or particularly important to this theme.
Some of these are triggered with configuration or markdown syntax that is unique to the theme, and we cover them below.

```{contents} Page contents
:local:
```

## Mathematics

Most Sphinx sites support math, but it is particularly important for scientific computing and so we illustrate support here as well.

Here is an inline equation: {math}`X_{0:5} = (X_0, X_1, X_2, X_3, X_4)` and {math}`another` and {math}`x^2 x^3 x^4` another. And here's one to test vertical height {math}`\frac{\partial^2 f}{\partial \phi^2}`.

Here is block-level equation:

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

You can add a link to equations like the one above: {eq}`My label` and {eq}`My label 2`.

## Code blocks

Code block styling is inspired by [GitHub's code block style](https://primer.style/css/components/markdown) and also has support for Code Block captions/titles.
See [the Sphinx documentation on code blocks](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block) for more information.

```python
print("A regular code block")
print("A regular code block")
print("A regular code block")
```

You can also provide captions with code blocks, which will be displayed just above the code.
For example, the following code:

````md
```{code-block} python
:caption: python.py

print("A code block with a caption.")
```
````

results in:

```{code-block} python
:caption: python.py

print("A code block with a caption.")
```

You can also display line numbers.
For example, the following code:

````md
```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```
````

results in:

```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```

## Code execution

This theme has support for Jupyter execution libraries so that you can programmatically update your documentation with each build.
For examples, see [](../examples/pydata.md).

## Admonition sidebars

```{admonition} A sidebar admonition!
:class: sidebar note
I was made with the `{admonition}` directive and a `sidebar` class.
```

```{sidebar} Sidebar title
I was made with the `{sidebar}` directive.
```

## Footnotes

Here's one footnote[^1] and another footnote [^2] and a named footenote[^named], symbol [^*].

[^1]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^2]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^named]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.
[^*]: Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar. Foo bar foo bar.

## Version changes

This theme supports a short-hand way of making **admonitions behave like sidebars**.
This can be a helpful way of highlighting content that lives to the side of your main text without interrupting the vertical flow as much.

For example, look to the right of an "admonition sidebar" and a traditional Sphinx sidebar.

To make an admonition behave like a sidebar, add the `sidebar` class to its list of classes.
For example, the admonition sidebar was created with the following markdown:

````md
```{admonition} A sidebar admonition!
:class: sidebar note
Some sidebar content.
```
````

## Link shortening for git repository services

Many projects have links back to their issues / PRs hosted on platforms like **GitHub** or **GitLab**. Instead of displaying these as raw links, this theme does some lightweight formatting for these platforms specifically. Here is an example from the issue requesting this feature: [https://github.com/pydata/pydata-sphinx-theme/issues/841](https://github.com/pydata/pydata-sphinx-theme/issues/841).

Links provided with a text body won't be changed.
