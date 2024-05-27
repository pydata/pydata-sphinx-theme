# PyData Sphinx tests

This directory contains the Python tests for the theme. These tests are built with [pytest](https://docs.pytest.org/en/stable/) and are called through `tox`.

- `test_build.py` checks that the static HTML output of the build process conforms
  to various expectations. It builds static HTML pages based on configurations in
  the `sites/` directory. The tests run various assertions on the static HTML
  output, including snapshot comparisons with previously compiled outputs that are
  stored in `test_build/`. In other words, it uses
  [`pytest-regressions`](https://pytest-regressions.readthedocs.io/) to compare
  the output created during the test run with a previously known and verified output
  (stored under `test_build`) to make sure nothing has changed.

- `test_a11y.py` checks PyData Sphinx Theme components for accessibility issues.
  It's important to note that [only a fraction of accessibility issues can be
  caught with automated
  testing](https://accessibility.blog.gov.uk/2017/02/24/what-we-found-when-we-tested-tools-on-the-worlds-least-accessible-webpage/).
  In contrast to the build test suite, the accessibility suite checks components as
  they appear in the browser, meaning with any CSS and JavaScript applied. It does
  this by building the PyData Sphinx Theme docs, launching a local server to the
  docs, and then checking the "Kitchen Sink" example pages with
  [Playwright](https://playwright.dev), a program for developers that allows
  loading and manipulating pages with various browsers, such as Chrome (chromium),
  Firefox (gecko), Safari (WebKit).

The ["Kitchen Sink" examples](https://pydata-sphinx-theme.readthedocs.io/en/stable/examples/kitchen-sink/index.html)
are taken from [sphinx-themes.org](https://sphinx-themes.org/) and showcase
components of the PyData Sphinx Theme, such as admonitions, lists, and headings.

## Visually debugging the test pages

It can be useful to build and inspect the test pages in the browser.

By default, `tox run -m tests` (or any other `tox` command that runs our tests) will build the HTML in a temporary directory.
You can change this by using the `PST_TEST_HTML_DIR` environment variable.

For example:

```bash
$ PST_TEST_HTML_DIR=./debug-test-theme/ tox run -m tests
```

Will save all the generated HTML in the folders `./debug-test-theme/<test-name>/<site-name>`
