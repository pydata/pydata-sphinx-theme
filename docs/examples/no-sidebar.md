# Test of no sidebar

This page shows off what the documentation looks like when you explicitly tell Sphinx not to include any sidebars via the following configuration:

```python
html_sidebars = {
  "path/to/page": [],
}
```

The left sidebar should be entirely gone, and the main content should expand slightly to make up the extra space.
