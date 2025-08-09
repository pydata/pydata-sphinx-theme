"""Create an "edit this page" url compatible with bitbucket, gitlab and github."""

import urllib

import jinja2

from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

from .utils import get_theme_options_dict


def setup_edit_url(
    app: Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    """Add a function that jinja can access for returning the edit URL of a page."""

    def get_edit_provider_and_url() -> None:
        """Return a provider name and a URL for an "edit this page" link."""
        file_name = f"{pagename}{context['page_source_suffix']}"

        # Make sure that doc_path has a path separator only if it exists (to avoid //)
        doc_path = context.get("doc_path", "")
        if doc_path and not doc_path.endswith("/"):
            doc_path = f"{doc_path}/"

        provider_urls = {
            "bitbucket_url": "https://bitbucket.org",
            "forgejo_url": "https://codeberg.org",
            "gitea_url": "https://gitea.com",
            "github_url": "https://github.com",
            "gitlab_url": "https://gitlab.com",
        }
        provider_labels = {
            "bitbucket": "Bitbucket",
            "forgejo": "Forgejo",
            "gitea": "Gitea",
            "github": "GitHub",
            "gitlab": "GitLab",
        }
        theme_options = get_theme_options_dict(app)
        provider_urls, provider_labels = adjust_forge_params(
            provider_urls, provider_labels, theme_options
        )

        edit_attrs = {}

        # ensure custom URL is checked first, if given
        url_template = context.get("edit_page_url_template")

        if url_template is not None:
            if "file_name" not in url_template:
                raise ExtensionError(
                    "Missing required value for `use_edit_page_button`. "
                    "Ensure `file_name` appears in `edit_page_url_template`: "
                    f"{url_template}"
                )
            provider_name = context.get("edit_page_provider_name")
            edit_attrs[("edit_page_url_template",)] = (provider_name, url_template)

        edit_attrs.update(
            {
                ("bitbucket_user", "bitbucket_repo", "bitbucket_version"): (
                    provider_labels["bitbucket"],
                    "{{ bitbucket_url }}/{{ bitbucket_user }}/{{ bitbucket_repo }}"
                    "/src/{{ bitbucket_version }}"
                    "/{{ doc_path }}{{ file_name }}?mode=edit",
                ),
                ("forgejo_user", "forgejo_repo", "forgejo_version"): (
                    provider_labels["forgejo"],
                    "{{ forgejo_url }}/{{ forgejo_user }}/{{ forgejo_repo }}"
                    "/_edit/{{ forgejo_version }}/{{ doc_path }}{{ file_name }}",
                ),
                ("gitea_user", "gitea_repo", "gitea_version"): (
                    provider_labels["gitea"],
                    "{{ gitea_url }}/{{ gitea_user }}/{{ gitea_repo }}"
                    "/_edit/{{ gitea_version }}/{{ doc_path }}{{ file_name }}",
                ),
                ("github_user", "github_repo", "github_version"): (
                    provider_labels["github"],
                    "{{ github_url }}/{{ github_user }}/{{ github_repo }}"
                    "/edit/{{ github_version }}/{{ doc_path }}{{ file_name }}",
                ),
                ("gitlab_user", "gitlab_repo", "gitlab_version"): (
                    provider_labels["gitlab"],
                    "{{ gitlab_url }}/{{ gitlab_user }}/{{ gitlab_repo }}"
                    "/-/edit/{{ gitlab_version }}/{{ doc_path }}{{ file_name }}",
                ),
            }
        )

        doc_context = dict(provider_urls)
        doc_context.update(context)
        doc_context.update(doc_path=doc_path, file_name=file_name)

        for attrs, (provider, url_template) in edit_attrs.items():
            if all(doc_context.get(attr) not in [None, "None"] for attr in attrs):
                return provider, jinja2.Template(url_template).render(**doc_context)

        raise ExtensionError(
            "Missing required value for `use_edit_page_button`. "
            "Ensure one set of the following in your `html_context` "
            f"configuration: {sorted(edit_attrs.keys())}"
        )

    context["get_edit_provider_and_url"] = get_edit_provider_and_url

    # Ensure that the max TOC level is an integer
    context["theme_show_toc_level"] = int(context.get("theme_show_toc_level", 1))


def adjust_forge_params(
    forge_urls: dict[str, str],
    forge_labels: dict[str, str],
    theme_options: dict[str, str],
) -> (dict[str, str], dict[str, str]):
    """Adjust labels and URLs for some of the more decentralized forges."""
    # use *_urls given in html_theme_options as authority (netloc)
    # instead of default if available
    for url_key in forge_urls:
        forge_url = theme_options.get(url_key)
        if forge_url:
            forge_url = urllib.parse.urlsplit(forge_url, allow_fragments=False)
            forge_url = f"{forge_url.scheme}://{forge_url.netloc}"
            forge_urls[url_key] = forge_url

    # use rebranded forge label instead of generic SW name where known
    if "forgejo_url" in theme_options:
        url = theme_options["forgejo_url"]
        if url.startswith("https://codeberg.org"):
            forge_labels["forgejo"] = "Codeberg"

    return forge_urls, forge_labels
