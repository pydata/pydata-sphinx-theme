# Making releases

(policies:release)=

## Our goals

Our release policy describes how we decide when to make a new public release of the theme so that other projects may use new features and improvements.
It tries to balance these goals:

- Release relatively frequently, so that we provide a continuous stream of improvement to projects that use the theme, and minimize the effort needed to upgrade.
- Do not surprise people (especially with negative surprises) and provide time for projects to provide feedback about upcoming features.
- Minimize the toil and complexity associated with releases, and reduce information silos and bottlenecks associated with them.

(releases:when)=

## When to make a release

Anybody is encouraged to make a new release if:

- It has been more than a month since the last release.
- OR a significant change has been made to our code that warrants a release.
- AND there are no open issues with a [{guilabel}`impact: block-release`](https://github.com/pydata/pydata-sphinx-theme/labels/impact%3A%20block-release) label.

### Release candidates

If a release includes complex or many changes (especially in JavaScript), make a `release candidate` and ask for feedback from users.
This is important because we do not test much of the CSS and JavaScript-based functionality in our testing infrastructure.
After a week or so, if there are no blocking issues that have been opened since the Release Candidate, we can make a full release.

## Process for making a release

This theme uses GitHub tags and releases to automatically push new releases to
PyPI.
Follow these steps to make a release:

- (optionally) **Create a [GitHub milestones](https://github.com/pydata/pydata-sphinx-theme/milestones)** to organize the issues that should be resolved as part of a new release.
- **Decide if it's time** to make a release be reading [](releases:when) and decide if it is time for a release.
- **Copy the [release checklist](https://github.com/pydata/pydata-sphinx-theme/blob/main/RELEASE.md) into a new issue**.
- **Complete the checklist**. That's it!

## Choosing a version increment

We use [semantic versioning](https://semver.org/) to decide whether it's a major, minor, or patch bump. Before we have released `1.0`, treat minor versions as breaking releases, and patch versions as feature / patch releases. **If this is a release candidate**, tag it like `0.1rc1`.
