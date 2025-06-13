"""Edit button unit tests."""

import pytest

from pydata_sphinx_theme.edit_this_page import adjust_forge_params


@pytest.fixture
def default_forge_urls():
    """Setup default edit URLs."""
    return {
        "forgejo_url": "https://codeberg.org",
        "gitea_url": "https://gitea.com",
        "gitlab_url": "https://gitlab.com",
    }


@pytest.mark.parametrize(
    "html_theme_options,modified_urls",
    [
        (
            {"forgejo_url": "https://my-forgejo.com/f-proj/f-repo"},
            {"forgejo_url": "https://my-forgejo.com"},
        ),
        (
            {"gitea_url": "https://my-gitea.com/g-proj/g-repo"},
            {"gitea_url": "https://my-gitea.com"},
        ),
        (
            {
                "gitlab_url": "https://my-gitlab.org/gl-proj/gl-repo",
                "forgejo_url": "https://my-forgejo.com/f-proj/f-repo",
            },
            {
                "forgejo_url": "https://my-forgejo.com",
                "gitlab_url": "https://my-gitlab.org",
            },
        ),
    ],
)
def test_adjust_forge_params_replace_urls(
    default_forge_urls, html_theme_options, modified_urls
):
    """Unit test for adjust_forge_params() url replacing."""
    forge_urls, forge_labels = adjust_forge_params(
        default_forge_urls, {}, html_theme_options
    )
    expected_urls = default_forge_urls | modified_urls

    assert forge_urls == expected_urls
    assert forge_labels == {}


@pytest.mark.parametrize(
    "html_theme_options,expected_labels",
    [
        ({"forgejo_url": "https://noreplace.com"}, {}),
        ({"forgejo_url": "https://codeberg.org"}, {"forgejo": "Codeberg"}),
    ],
)
def test_adjust_forge_params_relabel(
    default_forge_urls, html_theme_options, expected_labels
):
    """Unit test for adjust_forge_params() relabeling."""
    forge_urls, forge_labels = adjust_forge_params(
        default_forge_urls, {}, html_theme_options
    )

    assert forge_urls == default_forge_urls
    assert forge_labels == expected_labels
