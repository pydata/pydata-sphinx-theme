# Test of no sidebar

This page shows off what the documentation looks like when you explicitly tell Sphinx not to include any sidebars via the following configuration:

```python
html_sidebars = {
  "path/to/page": [],
}
html_theme_options = {
    "secondary_sidebar_items": {
        "path/to/page": [],
    },
}
```

Both the primary and secondary sidebars should be entirely gone, and the main content should expand slightly to make up the extra space.
