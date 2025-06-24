"""A custom Transform object to shorten github and gitlab links."""

import re

from typing import ClassVar
from urllib.parse import unquote, urlparse

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
    if match := re.match(r"/([^/]+)/([^/]+)/pull/(\d+)", path):
        owner, repo, pr_id = match.groups()
        return f"{owner}/{repo}#{pr_id}"

    # Issue URL
    elif match := re.match(r"/([^/]+)/([^/]+)/issues/(\d+)", path):
        owner, repo, issue_id = match.groups()
        return f"{owner}/{repo}#{issue_id}"

    # Commit URL
    elif match := re.match(r"/([^/]+)/([^/]+)/commit/([a-f0-9]{7,40})", path):
        owner, repo, commit_hash = match.groups()
        return f"{owner}/{repo}@{commit_hash[:7]}"

    # Branch URL
    elif match := re.match(r"/([^/]+)/([^/]+)/tree/([^/]+)", path):
        owner, repo, branch = match.groups()
        return f"{owner}/{repo}:{unquote(branch)}"

    # Tag URL
    elif match := re.match(r"/([^/]+)/([^/]+)/releases/tag/([^/]+)", path):
        owner, repo, tag = match.groups()
        return f"{owner}/{repo}@{unquote(tag)}"

    # File URL
    elif match := re.match(r"/([^/]+)/([^/]+)/blob/([^/]+)/(.*)", path):
        owner, repo, ref, filepath = match.groups()
        return f"{owner}/{repo}@{ref}/{unquote(filepath)}"

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
    if (m := re.match(r"^/(.+)/([^/]+)/-/merge_requests/(\d+)$", path)) or (
        m := re.match(r"^/(.+)/([^/]+)/merge_requests/(\d+)$", path)
    ):
        namespace, project, mr_id = m.groups()
        return f"{namespace}/{project}!{mr_id}"

    # Issues
    if (m := re.match(r"^/(.+)/([^/]+)/-/issues/(\d+)$", path)) or (
        m := re.match(r"^/(.+)/([^/]+)/issues/(\d+)$", path)
    ):
        namespace, project, issue_id = m.groups()
        return f"{namespace}/{project}#{issue_id}"

    # Commits
    if (m := re.match(r"^/(.+)/([^/]+)/-/commit/([a-fA-F0-9]+)$", path)) or (
        m := re.match(r"^/(.+)/([^/]+)/commit/([a-fA-F0-9]+)$", path)
    ):
        namespace, project, commit_hash = m.groups()
        return f"{namespace}/{project}@{commit_hash[:7]}"

    # Branches (tree)
    if (m := re.match(r"^https://gitlab\.com/(.+)/([^/]+)/-/tree/(.+)$", path)) or (
        m := re.match(r"^https://gitlab\.com/(.+)/([^/]+)/tree/(.+)$", path)
    ):
        namespace, project, branch = m.groups()
        return f"{namespace}/{project}:{unquote(branch)}"

    # Tags
    if (m := re.match(r"^/(.+)/([^/]+)/-/tags/(.+)$", path)) or (
        m := re.match(r"^/(.+)/([^/]+)/tags/(.+)$", path)
    ):
        namespace, project, tag = m.groups()
        return f"{namespace}/{project}@{unquote(tag)}"

    # Blob (files)
    if (m := re.match(r"^/(.+)/([^/]+)/-/blob/([^/]+)/(.+)$", path)) or (
        m := re.match(r"^/(.+)/([^/]+)/blob/([^/]+)/(.+)$", path)
    ):
        namespace, project, ref, path = m.groups()
        return f"{namespace}/{project}@{ref}/{unquote(path)}"

    # No match — return the original URL
    return url


def shorten_bitbucket(url: str) -> str:
    """
    Convert a Bitbucket URL to a short form like team/repo#123 or
    team/repo@main.
    """
    path = urlparse(url).path

    # Pull request URL
    if match := re.match(r"/([^/]+)/([^/]+)/pull-requests/(\d+)", path):
        workspace, repo, pr_id = match.groups()
        return f"{workspace}/{repo}#{pr_id}"

    # Issue URL
    elif match := re.match(r"/([^/]+)/([^/]+)/issues/(\d+)", path):
        workspace, repo, issue_id = match.groups()
        return f"{workspace}/{repo}!{issue_id}"

    # Commit URL
    elif match := re.match(r"/([^/]+)/([^/]+)/commits/([a-f0-9]+)", path):
        workspace, repo, commit_hash = match.groups()
        return f"{workspace}/{repo}@{commit_hash[:7]}"

    # Branch URL
    elif match := re.match(r"/([^/]+)/([^/]+)/branch/(.+)", path):
        workspace, repo, branch = match.groups()
        return f"{workspace}/{repo}:{unquote(branch)}"

    # Tag URL
    elif match := re.match(r"/([^/]+)/([^/]+)/commits/tag/(.+)", path):
        workspace, repo, tag = match.groups()
        return f"{workspace}/{repo}@{unquote(tag)}"

    # File URL
    elif match := re.match(r"/([^/]+)/([^/]+)/src/([^/]+)/(.*)", path):
        workspace, repo, ref, path = match.groups()
        return f"{workspace}/{repo}@{ref}/{unquote(path)}"

    # No match — return the original URL
    return url
