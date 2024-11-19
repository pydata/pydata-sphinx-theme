# Accessibility checks and manual auditing

As part of our commitment to making this theme accessible, we run automated
checks against all the pages under [](../../examples/kitchen-sink/index.rst).

The accessibility check is run every time that a pull request is created on
GitHub. We forbid merging a pull request into the codebase if it breaks this
check.

## Running the checks locally

If you are [developing the theme locally](../setup.md), the simplest way to run
the accessibility checks on your computer is:

```sh
tox run -m a11y
```

## Technical details

The main two technologies we use to write and run accessibility checks are
[Playwright for Python](https://playwright.dev/python/) and
[axe-core](https://github.com/dequelabs/axe-core).

Playwright is the successor to a similar library called Puppeteer. It provides a
way to programmatically script a web browser to open, operate, inspect, and test
web pages. Axe-core is a suite of accessibility checks written as a JavaScript
program. The program is meant to be injected into a web page. Once injected, it
examines the page for common accessibility failures, such as low contrast text.
Our accessibility test suite uses Playwright to inject Axe-core into each of the
Kitchen Sink pages plus a few other key pages in this documentation. We also
wrote a few other Playwright scripts to ensure that certain theme components can
be accessed using only the keyboard. All of our tests currently live in a file
called
[test_a11y.py](https://github.com/pydata/pydata-sphinx-theme/blob/main/tests/test_a11y.py).
:::{note}
We would love contributions that add more accessibility checks to our test
suite.
:::

We have also made these tests part of our continuous integration process, so
they are run in the cloud before we merge in new changes to the theme. We
use the following tools:

- GitHub Actions to provision machines in the cloud
- `tox` to install the needed dependencies on those machines
- `Pytest` with the Playwright plug-in to run the tests.

Look for the string "accessibility" in the file
[CI.yml](https://github.com/pydata/pydata-sphinx-theme/blob/main/.github/workflows/CI.yml)
to find how we have configured GitHub Actions.

## Known limitations and manual auditing

We are well aware that automated checks fall far short of comprehensive
accessibility auditing and testing, so we also conducted an accessibility audit
of three pages from the theme docs. We collected those findings in an issue on
GitHub, [May 2024 PyData Theme audit
findings](https://github.com/Quansight-Labs/czi-scientific-python-mgmt/issues/72)

Nearly all of the issues have been fixed, but of course things do break / have
already broken, and some things may have never been discovered, so please
[create a GitHub issue](https://github.com/pydata/pydata-sphinx-theme/issues/new) if you find something inaccessible.
