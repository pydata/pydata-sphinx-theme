"""General helpers for the management of config parameters."""

from typing import Any, Dict

from bs4 import BeautifulSoup, ResultSet
from sphinx.application import Sphinx


def get_theme_options(app: Sphinx) -> Dict[str, Any]:
    """Return theme options for the application w/ a fallback if they don't exist.

    In general we want to modify app.builder.theme_options if it exists, so prefer that first.
    """
    if hasattr(app.builder, "theme_options"):
        # In most HTML build cases this will exist except for some circumstances (see below).
        return app.builder.theme_options
    elif hasattr(app.config, "html_theme_options"):
        # For example, linkcheck will have this configured but won't be in builder obj.
        return app.config.html_theme_options
    else:
        # Empty dictionary as a fail-safe.
        return {}


def config_provided_by_user(app: Sphinx, key: str) -> bool:
    """Check if the user has manually provided the config."""
    return any(key in ii for ii in [app.config.overrides, app.config._raw_config])


def soup_to_python(soup: BeautifulSoup, only_pages: bool = False) -> Dict[str, Any]:
    """Convert the toctree html structure to python objects which can be used in Jinja.

    Parameters:
    soup : BeautifulSoup object for the toctree
    only_pages : Only include items for full pages in the output dictionary. Exclude anchor links (TOC items with a URL that starts with #)

    Returns:
        The toctree, converted into a dictionary with key/values that work within Jinja.
    """
    # toctree has this structure (caption only for toctree, not toc)
    #   <p class="caption">...</span></p>
    #   <ul>
    #       <li class="toctree-l1"><a href="..">..</a></li>
    #       <li class="toctree-l1"><a href="..">..</a></li>
    #       ...

    def extract_level_recursive(ul: ResultSet, navs_list: list) -> None:
        for li in ul.find_all("li", recursive=False):
            ref = li.a
            url = ref["href"]
            title = "".join(map(str, ref.contents))
            active = "current" in li.get("class", [])

            # If we've got an anchor link, skip it if we wish
            if only_pages and "#" in url and url != "#":
                continue

            # Converting the docutils attributes into jinja-friendly objects
            nav = {}
            nav["title"] = title
            nav["url"] = url
            nav["active"] = active

            navs_list.append(nav)

            # Recursively convert children as well
            nav["children"] = []
            ul = li.find("ul", recursive=False)
            if ul:
                extract_level_recursive(ul, nav["children"])

    navs = []
    for ul in soup.find_all("ul", recursive=False):
        extract_level_recursive(ul, navs)

    return navs
