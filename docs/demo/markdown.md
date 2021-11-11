# Markdown syntax

Sphinx can also generate pages from Markdown, using the [MyST Parser](https://myst-parser.readthedocs.io).
This page shows a few markdown-specific pieces of syntax.
For a description of other markdown syntax that you can use with Sphinx, see [the `myst-parser` reference](https://myst-parser.readthedocs.io/en/latest/syntax/reference.html).

## Horizontal rules

Here's a horizontal rule:

---

It separates major sections of content.

## Footnotes

Here's a footnote [^myfootnote]. And it should show up at the bottom!

[^myfootnote]: Here's the text for the footnote!

## Tables

| Syntax    | Description |   Test Text |
| :-------- | :---------: | ----------: |
| Header    |    Title    | Here's this |
| Paragraph |    Text     |    And more |
