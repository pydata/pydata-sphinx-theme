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
        ("gitlab", "https://gitlab.com/tezos/tezos/-/issues", "tezos/tezos/issues"),
        ("gitlab", "https://gitlab.com/tezos/tezos/issues", "tezos/tezos/issues"),
        (
            "gitlab",
            "https://gitlab.com/gitlab-org/gitlab/-/issues/375583",
            "gitlab-org/gitlab#375583",
        ),
        (
            # todo, non cannonical url, needs extra parsing.
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
            # todo, non cannonical url, needs extra parsing.
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
