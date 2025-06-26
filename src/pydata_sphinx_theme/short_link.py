"""A custom Transform object to shorten github and gitlab links."""

import re

from typing import ClassVar
from urllib.parse import urlparse

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher

from .utils import traverse_or_findall


class ShortenLinkTransform(SphinxPostTransform):
    """
    Shorten link when they are coming from github, gitlab, or bitbucket and add
    an extra class to the tag for further styling.

    Before:
        .. code-block:: html

            <a class="reference external"
                href="https://github.com/2i2c-org/infrastructure/issues/1329">
                https://github.com/2i2c-org/infrastructure/issues/1329
            </a>

    After:
        .. code-block:: html

            <a class="reference external github"
                href="https://github.com/2i2c-org/infrastructure/issues/1329">
                2i2c-org/infrastructure#1329
            </a>
    """

    default_priority = 400
    formats = ("html",)
    supported_platform: ClassVar[dict[str, str]] = {
        "github.com": "github",
        "gitlab.com": "gitlab",
        "bitbucket.org": "bitbucket",
    }

    @classmethod
    def add_platform_mapping(cls, platform, netloc):
        """Add domain->platform mapping to class at run-time."""
        cls.supported_platform.update({netloc: platform})

    def run(self, **kwargs):
        """Run the Transform object."""
        matcher = NodeMatcher(nodes.reference)
        # TODO: just use "findall" once docutils min version >=0.18.1
        for node in traverse_or_findall(self.document, matcher):
            uri = node.attributes.get("refuri")
            text = next(iter(node.children), None)
            # only act if the uri and text are the same
            # if not the user has already customized the display of the link
            if uri is not None and text is not None and text == uri:
                parsed_uri = urlparse(uri)
                # only do something if the platform is identified
                platform = self.supported_platform.get(parsed_uri.netloc)
                if platform is not None:
                    short = shorten_url(platform, uri)
                    if short != uri:
                        node.attributes["classes"].append(platform)
                        node.children[0] = nodes.Text(short)


def shorten_url(platform: str, url: str) -> str:
    """Parse the content of the path with respect to the selected platform.

    Args:
        platform: "github", "gitlab", "bitbucket", etc.
        url: the full url to the platform content, beginning with https://

    Returns:
        short form version of the url,
        or the full url if it could not shorten it
    """
    if platform == "github":
        return shorten_github(url)
    elif platform == "bitbucket":
        return shorten_bitbucket(url)
    elif platform == "gitlab":
        return shorten_gitlab(url)

    return url


def shorten_github(url: str) -> str:
    """
    Convert a GitHub URL to a short form like owner/repo#123 or
    owner/repo@abc123.
    """
    path = urlparse(url).path

    # Pull request URL
    # - Example:
    #   - https://github.com/pydata/pydata-sphinx-theme/pull/2068
    #   - pydata/pydata-sphinx-theme#2068
    if match := re.match(r"/([^/]+)/([^/]+)/pull/(\d+)", path):
        owner, repo, pr_id = match.groups()
        return f"{owner}/{repo}#{pr_id}"

    # Issue URL
    # - Example:
    #   - https://github.com/pydata/pydata-sphinx-theme/issues/2176
    #   - pydata/pydata-sphinx-theme#2176
    elif match := re.match(r"/([^/]+)/([^/]+)/issues/(\d+)", path):
        owner, repo, issue_id = match.groups()
        return f"{owner}/{repo}#{issue_id}"

    # Commit URL
    # - Example:
    #   - https://github.com/pydata/pydata-sphinx-theme/commit/51af2a27e8a008d0b44ed9ea9b45311e686d12f7
    #   - pydata/pydata-sphinx-theme@51af2a2
    elif match := re.match(r"/([^/]+)/([^/]+)/commit/([a-f0-9]+)", path):
        owner, repo, commit_hash = match.groups()
        return f"{owner}/{repo}@{commit_hash[:7]}"

    # No match — return the original URL
    return url


def shorten_gitlab(url: str) -> str:
    """
    Convert a GitLab URL to a short form like group/project!123 or
    group/project@abcdef7.

    Supports both canonical ('/-/') and non-canonical path formats.
    """
    path = urlparse(url).path

    # Merge requests
    # - Example:
    #   - https://gitlab.com/gitlab-org/gitlab/-/merge_requests/195598
    #   - gitlab-org/gitlab!195598
    if match := re.match(r"^/(.+)/([^/]+)/-/merge_requests/(\d+)$", path):
        namespace, project, mr_id = match.groups()
        return f"{namespace}/{project}!{mr_id}"

    # Issues
    # - Example:
    #   - https://gitlab.com/gitlab-org/gitlab/-/issues/551885
    #   - gitlab-org/gitlab#195598
    #
    # TODO: support hash URLs, for example:
    # https://gitlab.com/gitlab-org/gitlab/-/issues/545699#note_2543533261
    if match := re.match(r"^/(.+)/([^/]+)/-/issues/(\d+)$", path):
        namespace, project, issue_id = match.groups()
        return f"{namespace}/{project}#{issue_id}"

    # Commits
    # - Example:
    #   - https://gitlab.com/gitlab-org/gitlab/-/commit/81872624c4c58425a040e158fd228d8f0c2bda07
    #   - gitlab-org/gitlab@8187262
    if match := re.match(r"^/(.+)/([^/]+)/-/commit/([a-f0-9]+)$", path):
        namespace, project, commit_hash = match.groups()
        return f"{namespace}/{project}@{commit_hash[:7]}"

    # No match — return the original URL
    return url


def shorten_bitbucket(url: str) -> str:
    """
    Convert a Bitbucket URL to a short form like team/repo#123 or
    team/repo@main.
    """
    path = urlparse(url).path

    # Pull request URL
    # - Example:
    #   - https://bitbucket.org/atlassian/atlassian-jwt-js/pull-requests/23
    #   - atlassian/atlassian-jwt-js#23
    if match := re.match(r"^/([^/]+)/([^/]+)/pull-requests/(\d+)$", path):
        workspace, repo, pr_id = match.groups()
        return f"{workspace}/{repo}#{pr_id}"

    # Issue URL.
    # - Example:
    #   - https://bitbucket.org/atlassian/atlassian-jwt-js/issues/11/
    #   - atlassian/atlassian-jwt-js!11
    #
    # Deliberately not matching the end of the string because sometimes
    # Bitbucket issue URLs include a slug at the end, for example:
    # https://bitbucket.org/atlassian/atlassian-jwt-js/issues/11/nested-object-properties-are-represented
    elif match := re.match(r"^/([^/]+)/([^/]+)/issues/(\d+)", path):
        workspace, repo, issue_id = match.groups()
        return f"{workspace}/{repo}!{issue_id}"

    # Commit URL
    # - Example:
    #   - https://bitbucket.org/atlassian/atlassian-jwt-js/commits/d9b5197f0aeedeabf9d0f8d0953a80be65743d8a
    #   - atlassian/atlassian-jwt-js@d9b5197
    elif match := re.match(r"^/([^/]+)/([^/]+)/commits/([a-f0-9]+)$", path):
        workspace, repo, commit_hash = match.groups()
        return f"{workspace}/{repo}@{commit_hash[:7]}"

    # No match — return the original URL
    return url
