"""Shortening url tests."""

import pytest

from pydata_sphinx_theme.short_link import shorten_url


@pytest.mark.parametrize(
    "platform,url,expected",
    [
        ("github", "https://github.com", "https://github.com"),
        ("github", "https://github.com/github", "https://github.com/github"),
        ("github", "https://github.com/pydata", "https://github.com/pydata"),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme",
            "https://github.com/pydata/pydata-sphinx-theme",
        ),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme/pull/1012",
            "pydata/pydata-sphinx-theme#1012",
        ),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme/issues",
            "https://github.com/pydata/pydata-sphinx-theme/issues",
        ),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme/commit/3caf346cacd2dad2a192a83c6cc9f8852e5a722e",
            "pydata/pydata-sphinx-theme@3caf346",
        ),
        (
            "github",
            "https://github.com/orgs/pydata/projects/2",
            "https://github.com/orgs/pydata/projects/2",
        ),
        ("github", "https://github.com/pydata/projects/pull/2", "pydata/projects#2"),
        # issues and pulls are the same, so it's ok to normalise to the same here
        ("github", "https://github.com/pydata/projects/issues/2", "pydata/projects#2"),
        # Gitlab
        (
            "gitlab",
            "https://gitlab.com/tezos/tezos/-/issues",
            "https://gitlab.com/tezos/tezos/-/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/tezos/tezos/issues",
            "https://gitlab.com/tezos/tezos/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/375583",
            "gitlab-org/gitlab#375583",
        ),
        (
            # non canonical url - not supported
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues/375583",
            "https://gitlab.com/gitlab-org/gitlab/issues/375583",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/",
        ),
        (
            # non canonical url
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues/",
            "https://gitlab.com/gitlab-org/gitlab/issues/",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues",
            "https://gitlab.com/gitlab-org/gitlab/-/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues",
            "https://gitlab.com/gitlab-org/gitlab/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/merge_requests/84669",
            "gitlab-org/gitlab!84669",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/pipelines/511894707",
            "https://gitlab.com/gitlab-org/gitlab/-/pipelines/511894707",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-com/gl-infra/production/-/issues/6788",
            "gitlab-com/gl-infra/production#6788",
        ),
        # Bitbucket
        ("bitbucket", "https://bitbucket.org", "https://bitbucket.org"),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian",
            "https://bitbucket.org/atlassian",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/workspace/overview",
            "https://bitbucket.org/atlassian/workspace/overview",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui",
            "https://bitbucket.org/atlassian/aui",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/",
            "https://bitbucket.org/atlassian/aui/",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/pull-requests/4758",
            "atlassian/aui#4758",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/issues/375583",
            "atlassian/aui!375583",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/issues",
            "https://bitbucket.org/atlassian/aui/issues",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/issues/",
            "https://bitbucket.org/atlassian/aui/issues/",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/commits/de41ded719e579d0ed4ffb8a81c29bb9ada10011",
            "atlassian/aui@de41ded",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/branch/future/10.0.x",
            "https://bitbucket.org/atlassian/aui/branch/future/10.0.x",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/pipelines",
            "https://bitbucket.org/atlassian/aui/pipelines",
        ),
        (
            "bitbucket",
            "https://bitbucket.org/atlassian/aui/pipelines/results/14542",
            "https://bitbucket.org/atlassian/aui/pipelines/results/14542",
        ),
    ],
)
def test_shorten(platform, url, expected):
    """Unit test for url shortening.

    Usually you also want a build test in `test_build.py`
    """
    assert shorten_url(platform, url) == expected
