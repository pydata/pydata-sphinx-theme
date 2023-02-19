# Update Sphinx configuration during the build

Sometimes you want to update configuration values _during a build_.
For example, if you want to set a default if the user hasn't provided a value, or if you want to move the value from one keyword to another for a deprecation.

Here are some tips to do this the "right" way in Sphinx.

## Update config: use `app.config.__dict__`

For example, `app.config.__dict__["foot"] = "bar"`.

Even better, use our provided helper function:

```python
_set_config_if_not_provided_by_user(app, "foo", "bar")
```

## Update theme options: use `app.builder.theme_options`

For example, `app.builder.theme_options["logo"] = {"text": "Foo"}`.

## Check if a user has provided a default: `app.config._raw_config`

The `app.config._raw_config` attribute contains all of the **user-provided values**.
Use this if you want to check whether somebody has manually specified something.
