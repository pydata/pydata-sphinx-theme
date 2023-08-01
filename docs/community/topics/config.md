# Update Sphinx configuration during the build

Sometimes you want to update configuration values _during a build_.
For example, if you want to set a default if the user hasn't provided a value, or if you want to move the value from one keyword to another for a deprecation.

Here are some tips to do this the "right" way in Sphinx.

## Update config: use `app.config`

For example, `app.config.foo = "bar"`.
For some reason, when Sphinx sets things it directly uses `__dict__`, but this doesn't seem to be different from the pattern described here.

## Update theme options: use `app.builder.theme_options`

For example, `app.builder.theme_options["logo"] = {"text": "Foo"}`.

## Check if a user has provided a default: `app.config._raw_config`

The `app.config._raw_config` attribute contains all of the **user-provided values**.
Use this if you want to check whether somebody has manually specified something.
For example, `"somekey" in app.config._raw_config` will be `False` if a user has _not_ provided that option.

You can also check `app.config.overrides` for any CLI-provided overrides.

We bundle both checks in a helper function called `_config_provided_by_user`.

## Avoid the `config-inited` event

This theme is activated **after** `config-inited` is triggered, so if you write an event that depends on it in this theme, then it will never occur.
The earliest event you can use is `builder-inited`.
