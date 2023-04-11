# Read the Docs functionality

This theme comes with support for {{ rtd }}, a popular service for hosting documentation in the scientific Python community.

## Version switcher

Projects hosted on {{ rtd }} can use the {{ rtd }} supplied version switcher instead of the [version switcher that this theme provides](version-dropdown.rst).
Its presence will be automatically detected by this theme, and placed in the `rtd-footer-container` node inside the primary sidebar.

```{warning}
The {{ rtd }} version switcher will be hidden any time the primary sidebar is hidden (see [this section](layout-sidebar-primary) for discussion of when the primary sidebar might get hidden automatically and how to hide it purposely).
We intend to make {{ rtd }} switcher placement more flexible; you can track progress toward that in [this issue](https://github.com/pydata/pydata-sphinx-theme/issues/705).
```

## Add ethical advertisements to your sidebar

If you're hosting your documentation on ReadTheDocs, you should consider
adding an explicit placement for their **ethical advertisements**. These are
non-tracking advertisements from ethical companies, and they help ReadTheDocs
sustain themselves and their free service.

Ethical advertisements are added to your sidebar by default. To ensure they are
there if you manually update your sidebar, ensure that the `sidebar-ethical-ads.html`
template is added to your list. For example:

```python
html_sidebars = {
    "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
}
```
