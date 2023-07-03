# Page-level configuration

In some areas we support page-level configuration to control behavior on a per-page basis.
Try to make this configuration follow the `html_theme_options` structure of our configuration as much as possibl.
Begin them with `html_theme`, and separate "nested" configuration sections with periods (`.`).
This is [similar to how the TOML language defines nested configuration](https://toml.io/en/v1.0.0#keys).

For example, to remove the secondary sidebar, we use a page metadata key like this:

`````{tab-set}
````{tab-item} rST
```rst
:html_theme.sidebar_secondary.remove: true
```
````
````{tab-item} Markdown
```md
---
html_theme.sidebar_secondary.remove: true
---
```
````
`````

Note how the period naturally separates nested sections, and looks very similar to what we'd expect if we put this in a Python dictionary in `conf.py`:

```python
html_theme_options = {
   "sidebar_secondary": {"remove": "true"}
}
```
