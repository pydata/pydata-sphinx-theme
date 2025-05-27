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
        # TODO, I belive this is wrong as both orgs/pydata/projects/2 and
        # pydata/projects/issue/2 shorten to the same
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
        # codeberg
        (
            "codeberg",
            "https://codeberg.org/",
            "codeberg",
        ),
        (
            "codeberg",
            "https://codeberg.org/f-org/f-proj/issues/42",
            "f-org/f-proj#42",
        ),
        # forgejo
        (
            "forgejo",
            "https://my-forgejo.com/",
            "forgejo",
        ),
        (
            "forgejo",
            "https://forgejo-host.org/f-org/f-proj/issues/42",
            "f-org/f-proj#42",
        ),
        (
            "forgejo",
            "https://forgejo-host.org/f-org/f-proj/pulls/43",
            "f-org/f-proj#43",
        ),
        # gitea
        (
            "gitea",
            "https://gitea.com",
            "gitea",
        ),
        (
            "gitea",
            "https://my-gitea.com/",
            "gitea",
        ),
        (
            "gitea",
            "https://gitea.com/gitea-org/g-proj/issues/42",
            "gitea-org/g-proj#42",
        ),
        (
            "gitea",
            "https://gitea.com/gitea-org/g-proj/pulls/43",
            "gitea-org/g-proj#43",
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


@pytest.fixture(scope="session")
def shortener():
    """Setup ShortenLinkTransform object for testing."""
    document = Mock()
    document.settings = Mock()
    document.settings.language_code = "en"
    document.reporter = None
    return ShortenLinkTransform(document)


@pytest.mark.parametrize(
    "url,html_options,expected",
    [
        # forgejo
        (
            "https://forgejo-instance.com/f-org/f-proj/pulls/43",
            {},
            "forgejo",
        ),
        (
            "https://forgejo-instance.com/f-org/",
            {},
            None,
        ),
        (
            "https://forgejo-instance.com/f-org/",
            {"forgejo_url": "https://forgejo-instance.com/f-org/f-proj"},
            "forgejo",
        ),
        # gitea
        (
            "https://gitea-instance.com/g-org/g-proj/pulls/43",
            {},
            "gitea",
        ),
        (
            "https://gitea-instance.com/g-org/",
            {},
            None,
        ),
        (
            "https://gitea-instance.com/g-org/",
            {"gitea_url": "https://gitea-instance.com/g-org/g-proj"},
            "gitea",
        ),
        # gitlab
        (
            "https://gitlab-instance.com/g-org/g-proj/-/merge_requests/43",
            {},
            "gitlab",
        ),
        (
            "https://gitlab-instance.com/g-org/",
            {},
            None,
        ),
        (
            "https://gitlab-instance.com/g-org/",
            {"gitlab_url": "https://gitlab-instance.com/g-org/g-proj"},
            "gitlab",
        ),
    ],
)
def test_identify_selfhosted(url, html_options, expected, shortener):
    """Unit test for self-hosted forges identification."""
    url = urlparse(url)

    assert shortener.identify_selfhosted(url, html_options) == expected
