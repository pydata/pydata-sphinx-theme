# Read the Docs functionality

This theme comes with support for {{ rtd }}, a popular service for hosting documentation in the scientific Python community.
Below are the supported integrations with {{ rtd }} functionality.

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

## Version switcher

{{ rtd }} has a built-in version switcher that normally appears in the bottom-right corner of the screen.
If your site is hosted on {{ rtd }} and you enabled the theme's native version switcher, the {{ rtd }} version switcher will be suppressed.
If your site is hosted on {{ rtd }} and you _did not_ enable the theme's native version switcher,
the {{ rtd }} version switcher will appear at the bottom of the left sidebar,
unless you have suppressed the left sidebar in which case it will be in {{ rtd }}'s default (bottom right corner) position.
