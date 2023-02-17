# PyData package support

This theme is designed by and for the PyData community, and so there are a few places where we special-case support for packages in this community.

We define CSS rules that ensure PyData content in Sphinx looks reasonable on both light and dark themes.
If we hear reports from maintainers that we could change something in this theme that would make their documentation look better, and if this change is sustainable for us, then we should do so.

We store our PyData-specific SCSS in two relevant files, both in the `src/pydata_sphinx_theme/assets/styles/` folder:

- `extensions/_execution.scss` - styles for Sphinx libraries that execute and insert code into the documentation. For example, MyST-NB, Jupyter Sphinx, and the Matplotlib `plot` directive. Most PyData support should go here via generic improvements that all packages benefit from.
- `extensions/_pydata.scss` - styles for specific libraries in the PyData ecosystem. In general we should try to keep this minimal because it is mostly special-casing single library quirks.
