"""Shortening url tests."""

from urllib.parse import urlparse

import pytest
from pydata_sphinx_theme.short_link import ShortenLinkTransform


class Mock:
    """mock object."""

    pass


@pytest.mark.parametrize(
    "platform,url,expected",
    [
        # TODO, I belive this is wrong as both github.com and github.com/github
        # shorten to just github.
        ("github", "https://github.com", "github"),
        ("github", "https://github.com/github", "github"),
        ("github", "https://github.com/pydata", "pydata"),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme",
            "pydata/pydata-sphinx-theme",
        ),
        (
            "github",
            "https://github.com/pydata/pydata-sphinx-theme/pull/1012",
            "pydata/pydata-sphinx-theme#1012",
        ),
        # TODO, I belive this is wrong as both orgs/pydata/projects/2 and pydata/projects/issue/2
        # shorten to the same
        ("github", "https://github.com/orgs/pydata/projects/2", "pydata/projects#2"),
        ("github", "https://github.com/pydata/projects/pull/2", "pydata/projects#2"),
        # issues and pulls are athe same, so it's ok to normalise to the same here
        ("github", "https://github.com/pydata/projects/issues/2", "pydata/projects#2"),
        # Gitlab
        ("gitlab", "https://gitlab.com/tezos/tezos/-/issues", "tezos/tezos/issues"),
        ("gitlab", "https://gitlab.com/tezos/tezos/issues", "tezos/tezos/issues"),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/375583",
            "gitlab-org/gitlab#375583",
        ),
        (
            # TODO, non canonical url, discuss if should maybe  be shortened to
            # gitlab-org/gitlab#375583
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues/375583",
            "gitlab-org/gitlab/issues/375583",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/",
            "gitlab-org/gitlab/issues",
        ),
        (
            # TODO, non canonical url, discuss if should maybe  be shortened to
            # gitlab-org/gitlab/issues (no trailing slash)
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues/",
            "gitlab-org/gitlab/issues/",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues",
            "gitlab-org/gitlab/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/issues",
            "gitlab-org/gitlab/issues",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/merge_requests/84669",
            "gitlab-org/gitlab!84669",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/pipelines/511894707",
            "gitlab-org/gitlab/-/pipelines/511894707",
        ),
        (
            "gitlab",
            "https://gitlab.com/gitlab-com/gl-infra/production/-/issues/6788",
            "gitlab-com/gl-infra/production#6788",
        ),
    ],
)
def test_shorten(platform, url, expected):
    """Unit test for url shortening.

    Usually you also want a build test in `test_build.py`
    """
    document = Mock()
    document.settings = Mock()
    document.settings.language_code = "en"
    document.reporter = None

    sl = ShortenLinkTransform(document)
    sl.platform = platform

    URI = urlparse(url)

    assert sl.parse_url(URI) == expected
