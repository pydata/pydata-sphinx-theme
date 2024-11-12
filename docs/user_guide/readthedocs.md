# Read the Docs functionality

This theme comes with support for {{ rtd }}, a popular service for hosting documentation in the scientific Python community.

## Version switcher

Read the Docs provides a version switcher by default to projects as part of a
[flyout menu](https://docs.readthedocs.io/en/stable/flyout-menu.html) that can
be disabled.

This means that you have one of three options if you are hosting a PyData
Sphinx Theme-enabled site on Read the Docs:

1. Use only the Read the Docs version switcher. You must disable the [version
   switcher that this theme provides](version-dropdown.rst) if you previously
   enabled it.
2. Use only this theme's version switcher. You must disable the Read the Docs
   version switcher by going to your project's [Read the Docs
   dashboard](https://app.readthedocs.org/dashboard/). Then go to
   `Settings > Addons > Flyout menu` and uncheck the "Flyout enabled" box.
3. Not recommended: use both version switchers.

Be aware that the two version switchers are not feature equivalent. For example,
the Read the Docs flyout provides a translation switcher in addition to a
version switcher. On the other hand, the Read the Docs switcher is not styled to
match the look and feel of this theme. And there are other differences.

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
