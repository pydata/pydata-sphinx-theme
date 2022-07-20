# Read the Docs functionality

This theme comes with support for {{ rtd }}, a popular service for hosting documentation in the scientific Python community.

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
