# Accessibility checks

The accessibility checking tools can find a number of common HTML patterns which
assistive technology can't help users understand.
We run a [Lighthouse](https://developers.google.com/web/tools/lighthouse) job in our CI/CD, which generates a "score" for all pages in our **Kitchen Sink** example documentation.
The configuration for Lighthouse is in:

- `.github/workflows/lighthouserc.json`

For more information about configuring lighthouse, see [the lighthouse documentation](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md).
For more information about Accessibility in general, see [](../../user_guide/accessibility.rst).
