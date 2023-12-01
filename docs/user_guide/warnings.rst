
Theme changes, deprecations, and warnings
=========================================

Generally speaking, the best source of information about changes to the theme will be the release changelog.
We try to avoid raising warnings within theme code, which means sometimes the theme will change (perhaps significantly) without deprecation warnings or other alerts.
Still, we occasionally do warn about things like (upcoming) changes to the theme's default config values.
If you prefer *not* to receive such warnings, there is a config value to suppress them:

.. code-block::
    :caption: conf.py

    html_theme_options = {
        "surface_warnings": False
    }
