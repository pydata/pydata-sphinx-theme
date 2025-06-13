"""A custom Transform object to shorten github and gitlab links."""

from typing import ClassVar, Literal
from urllib.parse import ParseResult, urlparse, urlunparse

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher

from .utils import get_theme_options_dict, traverse_or_findall


class ShortenLinkTransform(SphinxPostTransform):
    """
    Shorten links leading to supported forges.
    Also attempt to identify self-hosted forge instances.
    Add an extra class to the tag for further styling.

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
        "codeberg.org": "codeberg",
        "gitea.com": "gitea",
        "github.com": "github",
        "gitlab.com": "gitlab",
    }
    platform = None

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
                uri = urlparse(uri)
                # only do something if the platform is identified
                self.platform = self.supported_platform.get(uri.netloc)
                # or we can make a reasonable guess about self-hosted forges
                if self.platform is None:
                    html_theme_options = get_theme_options_dict(self.app)
                    self.platform = self.identify_selfhosted(uri, html_theme_options)
                if self.platform is not None:
                    node.attributes["classes"].append(self.platform)
                    node.children[0] = nodes.Text(self.parse_url(uri))

    def identify_selfhosted(
        self, uri: ParseResult, html_theme_options: dict[str, str]
    ) -> Literal["forgejo", "gitea", "gitlab"] | None:
        """Try to identify what self-hosted forge uri leads to (if any).

        Args:
            uri: the link to the platform content
            html_theme_options: varia

        Returns:
            likely platform if one matches, None otherwise
        """
        # forge name in authority and known url part in the right place
        # unreliable but may catch any number of hosts
        path_parts = uri.path.strip("/").split("/")
        if len(path_parts) > 2 and path_parts[2] in ("pulls", "issues", "projects"):
            if "forgejo" in uri.netloc:
                return "forgejo"
            elif "gitea" in uri.netloc:
                return "gitea"
        if (
            len(path_parts) > 3
            and path_parts[2] == "-"
            and path_parts[3] in ("issues", "merge_requests")
        ):
            if "gitlab" in uri.netloc:
                return "gitlab"

        # url passed in *_url option
        # will only match project's own forge but that's
        # likely where most doc links will lead anyway
        str_url = f"{uri.scheme}://{uri.netloc}"
        selfhosted = ("forgejo", "gitea", "gitlab")
        for forge in selfhosted:
            known_url = html_theme_options.get(f"{forge}_url")
            if known_url and known_url.startswith(str_url):
                return forge

        return None

    def parse_url(self, uri: ParseResult) -> str:
        """Parse the content of the url with respect to the selected platform.

        Args:
            uri: the link to the platform content

        Returns:
            the reformated url title
        """
        path = uri.path
        if path == "":
            # plain url passed, return platform only
            return self.platform

        # if the path is not empty it contains a leading "/", which we don't want to
        # include in the parsed content
        path = path.lstrip("/")

        # check the platform name and read the information accordingly
        # as "<organisation>/<repository>#<element number>"
        # or "<group>/<subgroup 1>/…/<subgroup N>/<repository>#<element number>"
        if self.platform == "github":
            # split the url content
            parts = path.split("/")

            if parts[0] == "orgs" and "/projects" in path:
                # We have a projects board link
                # ref: `orgs/{org}/projects/{project-id}`
                text = f"{parts[1]}/projects#{parts[3]}"
            else:
                # We have an issues, PRs, or repository link
                if len(parts) > 0:
                    text = parts[0]  # organisation
                if len(parts) > 1:
                    text += f"/{parts[1]}"  # repository
                if len(parts) > 2:
                    if parts[2] in ["issues", "pull", "discussions"]:
                        text += f"#{parts[-1]}"  # element number

        elif self.platform == "gitlab":
            # cp. https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references
            if "/-/" in path and any(
                map(uri.path.__contains__, ["issues", "merge_requests"])
            ):
                group_and_subgroups, parts, *_ = path.split("/-/")
                parts = parts.rstrip("/")
                if "/" not in parts:
                    text = f"{group_and_subgroups}/{parts}"
                else:
                    parts = parts.split("/")
                    url_type, element_number, *_ = parts
                    if not element_number:
                        text = group_and_subgroups
                    elif url_type == "issues":
                        text = f"{group_and_subgroups}#{element_number}"
                    elif url_type == "merge_requests":
                        text = f"{group_and_subgroups}!{element_number}"
            else:
                # display the whole uri (after "gitlab.com/") including parameters
                # for example "<group>/<subgroup1>/<subgroup2>/<repository>"
                text = uri._replace(netloc="", scheme="")  # remove platform
                text = urlunparse(text)[1:]  # combine to string and strip leading "/"
        elif self.platform in ("codeberg", "forgejo", "gitea"):
            parts = path.rstrip("/").split("/")
            if len(parts) == 4 and parts[2] in ("issues", "pulls"):
                text = f"{parts[0]}/{parts[1]}#{parts[3]}"  # element number
            elif parts == [""]:
                text = self.platform
            else:
                text = uri._replace(netloc="", scheme="")  # remove platform
                text = urlunparse(text)[1:]  # combine to string and strip leading "/"

        return text
