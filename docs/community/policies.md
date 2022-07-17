# Team policies and guidelines

## Merge and review policy

Our policy for merging and reviewing describes how we review one another's work, and when we allow others to merge changes into our main codebase.
It tries to balance between a few goals:

- Iterate on PRs and merge them relatively quickly, so that we reduce the debt associated with long-lasting PRs.
- Give enough time for others to provide their input and guide the PR itself, and to ensure that we aren't creating a problem with the PR.
- Value iterative improvement over creating the perfect Pull Request, so that we do not burden contributors with cumbersome discussion and minor revision requests.
- Recognize that we all have limited time and resources, and so cannot guarantee a full quality assurance process each time.
- Give general preference to the opinions from maintainers of projects in the PyData ecosystem, as a key stakeholder community of this theme.

We follow these guidelines in order to achieve these goals:

- Assume that all maintainers are acting in good faith and will use their best judgment to make decisions in the best interests of the repository.
- We can and will make mistakes, and so encourage best practices in testing and documentation to guard against this.
- It's important to share information, so give a best effort at telling others about work that you're doing.
- It's best to discuss and agree on important decisions at a high level before implementation, so give a best effort at providing time and invitation for others to provide feedback.

### Policy for moderate changes

These are changes that make modest changes to new or existing functionality, but that aren't going to significantly change the default behavior of the theme, user configuration, etc.
This is the majority of changes that we make.

PRs should:

- Refer to (and ideally close) an issue that describes the problem this change is solving.
- Have relevant testing and documentation coverage.

They can be merged when the above conditions are met, and one of these things happens:

- The PR has at least one approval from a core maintainer that isn't the PR author
- The PR author has signaled their intent to merge unless there are objections, and 48 hours have passed since that comment.

### Policy for major new features and breaking changes

These are changes that significantly alter the experience of the user, or that add significant complexity to the codebase.

All of the above, but PRs **must** have approval from at least one other core maintainer before merging.
In addition, the PR author should put extra effort into ensuring that the relevant stakeholders are notified about a change, so they can gauge its impact and provide feedback.

### Policy For minor changes and bugfixes

These are small changes that might be noticeable to the user, but in a way that is clearly an improvement.
They generally shouldn't touch too many lines of code.

Update the relevant tests and documentation, but PR authors are welcome to self-merge whenever they like without PR approval.

(policies:release)=

## Release policy

Our release policy describes how we decide when to make a new public release of the theme so that other projects may use new features and improvements.
It tries to balance between these goals:

- Release relatively frequently, so that we provide a continuous stream of improvement to projects that use the theme, and minimize the effort needed to upgrade.
- Do not surprise people (especially with negative surprises) and provide time for projects to provide feedback about upcoming features.
- Minimize the toil and complexity associated with releases, and reduce information silos and bottlenecks associated with them.

### Release policy guidelines

Here are the guidelines we follow when creating new releases:

- Encourage releases whenever a maintainer feels there has been a "significant" change in the codebase. The bar for this should be relatively low.
- Releases should be as automated as possible, and should not rely on a single person to have special permissions or credentails.
- Use the [{guilabel}`block-release`](https://github.com/pydata/pydata-sphinx-theme/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3Ablock-release) label to prevent a release from happening until an issue is resolved.
- Use [GitHub Milestones](https://github.com/pydata/pydata-sphinx-theme/milestones) to organize the issues that should be resolved as part of a new release.
- For non-trivial changes, **make a `release candidate`** and ask for feedback from users. This is important because we do not test much of the CSS and JavaScript-based functionality in our testing infrastructure.
- After a week or so, if there are no blocking issues that have been opened since the Release Candidate, we can make a full release.
