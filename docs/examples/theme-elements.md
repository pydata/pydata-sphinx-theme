# Theme-specific elements

There are a few elements that are unique or particularly important to this theme.
This page is a reference for how these look.

```{contents} Page contents
:local:
```

## Mathematics

Most Sphinx sites support math, but it is particularly important for scientific computing and so we illustrate support here as well.

This is a test. Here is an inline equation: {math}`X_{0:5} = (X_0, X_1, X_2, X_3, X_4)` and {math}`another` and {math}`x^2 x^3 x^4` another.

Here is another:

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

```{code-block} python
:caption: python.py

print("A code block with a caption.")
print("A code block with a caption.")
print("A code block with a caption.")
```

```{code-block} python
:caption: python.py
:linenos:

print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
print("A code block with a caption and line numbers.")
```

## Code execution

See [](pydata.md).

## Embedding in admonitions

````{note}
Here's a note with:

- A nested list
- List item two

As well as:

```{warning}
A nested warning block to test nested admonitions.
```
````

## Version changes

You can write in your documentation when something has been changed,
added or deprecated from one version to another.

```{versionadded} 0.1.1
Something is new, use it from now.
```

```{versionchanged} 0.1.1
Something is modified, check your version number.
```

```{deprecated} 0.1.1
Something is deprecated, use something else instead.
```
