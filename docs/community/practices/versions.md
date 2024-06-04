# Supported Python and Sphinx versions

Python and Sphinx are the two primary dependencies of this theme.
We have particular practices for deciding which versions of these we support (especially Sphinx, which tends to release breaking changes).

## Supported Python versions

For releases of Python, we aim to follow this approach[^1]:

> For a new major/minor release of this theme, we support any minor Python versions released in the last 3.5 years (42 months), as defined in [the EOL schedule for Python](https://endoflife.date/python)[^2].

We define "support" as testing against each of these versions so that users can be assured they will not trigger any bugs.

For example, if we made a minor release tomorrow, we'd [look at the EOL schedule for Python](https://endoflife.date/python) and support all the versions that fall within a 3.5-year window.

[^1]: Our support for Python versions is inspired by [NEP 029](https://numpy.org/neps/nep-0029-deprecation_policy.html).

[^2]: These policies are goals, not promises. We are a volunteer-led community with limited time. Consider these sections to be our intention, but we recognize that we may not always be able to meet these criteria if we cannot do so. We welcome contributions from others to help us more sustainably meet these goals!

## Supported Sphinx versions

For supported versions of Sphinx, we aim to follow this approach:

> We support the latest released version of Sphinx that is **older than 6 months**.
> We unofficially support earlier released versions of Sphinx, but may increase the lower-bound in our dependency pin without warning if needed[^2].

When a new pre-release of Sphinx is released, we should follow these steps:

- Ensure that our tests are passing. We run our tests with any **pre-releases** of Sphinx, so we can test major errors quickly and make the necessary changes.
- [Look at the Sphinx Changelog](https://www.sphinx-doc.org/en/master/changes.html) and make sure there are no changes that might break things that aren't captured by our tests.
- [Look at the deprecated API changes](https://www.sphinx-doc.org/en/master/extdev/deprecated.html) and make sure there are no changes that might break things that aren't captured by our tests.
- [Look at the docutils changelog](https://docutils.sourceforge.io/RELEASE-NOTES.html) in case there's a new docutils version supported that breaks something.

```{note}
This theme does not pin the upper version of Sphinx that it supports.
If a Sphinx release causes major breaking changes for our users, and we do not have the capacity to update our code and release a fix, we may temporarily pin the upper bound of Sphinx we support until this is fixed.
```
