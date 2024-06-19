# Accessibility checks

```{note}
April-2023: we are currently
[re-evaluating how we do accessibility checks](https://github.com/pydata/pydata-sphinx-theme/issues/1168)
and reporting, so this may change soon.
```

In general, accessibility-checking tools can find a limited number of common HTML patterns that assistive technology
can't help users understand.

## Accessibility checks as part of our development process

We run a [Lighthouse](https://developers.google.com/web/tools/lighthouse) job in our CI/CD, which generates a "score" for all pages in our **Kitchen Sink** example documentation.
The configuration for Lighthouse can be found in the `.github/workflows/lighthouserc.json` file.

For more information about configuring Lighthouse, see [the Lighthouse documentation](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md).
For more information about Accessibility in general, see [](../../user_guide/accessibility.md).

We have also recently added automated tests using [Playwright](https://playwright.dev/python/) and [axe-core](https://github.com/dequelabs/axe-core) to improve our accessibility testing and reporting.
