"""
Bootstrap-based sphinx theme from the PyData community
"""
import os
from pathlib import Path
from functools import lru_cache
import json
from urllib.parse import urlparse, urlunparse

import jinja2
from bs4 import BeautifulSoup as bs
from docutils import nodes
from sphinx import addnodes
from sphinx.environment.adapters.toctree import TocTree
from sphinx.addnodes import toctree as toctree_node
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher
from sphinx.errors import ExtensionError
from sphinx.util import logging
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
import requests
from requests.exceptions import ConnectionError, HTTPError, RetryError

from .bootstrap_html_translator import BootstrapHTML5Translator

__version__ = "0.12.0"

logger = logging.getLogger(__name__)


def update_config(app, env):
    theme_options = env.config.html_theme_options

    # DEPRECATE >= v0.10
    if theme_options.get("search_bar_position") == "navbar":
        logger.warning(
            "Deprecated config `search_bar_position` used."
            "Use `search-field.html` in `navbar_end` template list instead."
        )

    # DEPRECATE >= 0.11
    if theme_options.get("left_sidebar_end"):
        theme_options["primary_sidebar_end"] = theme_options.get("left_sidebar_end")
        logger.warning(
            "The configuration `left_sidebar_end` is deprecated."
            "Use `primary_sidebar_end`"
        )

    if theme_options.get("logo_text"):
        logo = theme_options.get("logo", {})
        logo["text"] = theme_options.get("logo_text")
        theme_options["logo"] = logo
        logger.warning(
            "The configuration `logo_text` is deprecated." "Use `'logo': {'text': }`."
        )

    if theme_options.get("page_sidebar_items"):
        theme_options["secondary_sidebar_items"] = theme_options.get(
            "page_sidebar_items"
        )
        logger.warning(
            "The configuration `page_sidebar_items` is deprecated."
            "Use `secondary_sidebar_items`."
        )

    # Validate icon links
    if not isinstance(theme_options.get("icon_links", []), list):
        raise ExtensionError(
            "`icon_links` must be a list of dictionaries, you provided "
            f"type {type(theme_options.get('icon_links'))}."
        )

    # Update the anchor link (it's a tuple, so need to overwrite the whole thing)
    icon_default = app.config.values["html_permalinks_icon"]
    app.config.values["html_permalinks_icon"] = ("#", *icon_default[1:])

    # Raise a warning for a deprecated theme switcher config
    if "url_template" in theme_options.get("switcher", {}):
        logger.warning(
            "html_theme_options['switcher']['url_template'] is no longer supported."
            " Set version URLs in JSON directly."
        )

    # check the validity of the theme switcher file
    is_dict = isinstance(theme_options.get("switcher"), dict)
    should_test = theme_options.get("check_switcher", True)
    if is_dict and should_test:
        theme_switcher = theme_options.get("switcher")

        # raise an error if one of these compulsory keys is missing
        json_url = theme_switcher["json_url"]
        theme_switcher["version_match"]

        # try to read the json file. If it's a url we use request,
        # else we simply read the local file from the source directory
        # display a log warning if the file cannot be reached
        reading_error = None
        if urlparse(json_url).scheme in ["http", "https"]:
            try:
                request = requests.get(json_url)
                request.raise_for_status()
                content = request.text
            except (ConnectionError, HTTPError, RetryError) as e:
                reading_error = repr(e)
        else:
            try:
                content = Path(env.srcdir, json_url).read_text()
            except FileNotFoundError as e:
                reading_error = repr(e)

        if reading_error is not None:
            logger.warning(
                f'The version switcher "{json_url}" file cannot be read due to the following error:\n'
                f"{reading_error}"
            )
        else:
            # check that the json file is not illformed,
            # throw a warning if the file is ill formed and an error if it's not json
            switcher_content = json.loads(content)
            missing_url = any(["url" not in e for e in switcher_content])
            missing_version = any(["version" not in e for e in switcher_content])
            if missing_url or missing_version:
                logger.warning(
                    f'The version switcher "{json_url}" file is malformed'
                    ' at least one of the items is missing the "url" or "version" key'
                )

    # Add an analytics ID to the site if provided
    analytics = theme_options.get("analytics", {})
    if analytics:
        # Plausible analytics
        plausible_domain = analytics.get("plausible_analytics_domain")
        plausible_url = analytics.get("plausible_analytics_url")

        # Ref: https://plausible.io/docs/plausible-script
        if plausible_domain and plausible_url:
            kwargs = {
                "loading_method": "defer",
                "data-domain": plausible_domain,
                "filename": plausible_url,
            }
            app.add_js_file(**kwargs)

        # Google Analytics
        gid = analytics.get("google_analytics_id")
        if gid:
            gid_js_path = f"https://www.googletagmanager.com/gtag/js?id={gid}"
            gid_script = f"""
                window.dataLayer = window.dataLayer || [];
                function gtag(){{ dataLayer.push(arguments); }}
                gtag('js', new Date());
                gtag('config', '{gid}');
            """

            # Link the JS files
            app.add_js_file(gid_js_path, loading_method="async")
            app.add_js_file(None, body=gid_script)


def prepare_html_config(app, pagename, templatename, context, doctree):
    """Prepare some configuration values for the HTML build.

    For some reason updating the html_theme_options in an earlier Sphinx
    event doesn't seem to update the values in context, so we manually update
    it here with our config.
    """

    # Prepare the logo config dictionary
    theme_logo = context.get("theme_logo")
    if not theme_logo:
        # In case theme_logo is an empty string
        theme_logo = {}
    if not isinstance(theme_logo, dict):
        raise ValueError(f"Incorrect logo config type: {type(theme_logo)}")

    # DEPRECATE: >= 0.11
    if context.get("theme_logo_link"):
        logger.warning(
            "DEPRECATION: Config `logo_link` will be deprecated in v0.11. "
            "Use the `logo.link` configuration dictionary instead."
        )
        theme_logo = context.get("theme_logo_link")

    context["theme_logo"] = theme_logo

    # update version number
    context["theme_version"] = __version__


def update_templates(app, pagename, templatename, context, doctree):
    """Update template names and assets for page build."""
    # Allow for more flexibility in template names
    template_sections = [
        "theme_navbar_start",
        "theme_navbar_center",
        "theme_navbar_persistent",
        "theme_navbar_end",
        "theme_footer_items",
        "theme_secondary_sidebar_items",
        "theme_primary_sidebar_end",
        "sidebars",
    ]
    for section in template_sections:
        if context.get(section):
            # Break apart `,` separated strings so we can use , in the defaults
            if isinstance(context.get(section), str):
                context[section] = [
                    ii.strip() for ii in context.get(section).split(",")
                ]

            # Add `.html` to templates with no suffix
            for ii, template in enumerate(context.get(section)):
                if not os.path.splitext(template)[1]:
                    context[section][ii] = template + ".html"

    # Remove a duplicate entry of the theme CSS. This is because it is in both:
    # - theme.conf
    # - manually linked in `webpack-macros.html`
    if "css_files" in context:
        theme_css_name = "_static/styles/pydata-sphinx-theme.css"
        if theme_css_name in context["css_files"]:
            context["css_files"].remove(theme_css_name)

    # Add links for favicons in the topbar
    for favicon in context.get("theme_favicons", []):
        icon_type = Path(favicon["href"]).suffix.strip(".")
        opts = {
            "rel": favicon.get("rel", "icon"),
            "sizes": favicon.get("sizes", "16x16"),
            "type": f"image/{icon_type}",
        }
        if "color" in favicon:
            opts["color"] = favicon["color"]
        # Sphinx will auto-resolve href if it's a local file
        app.add_css_file(favicon["href"], **opts)

    # Add metadata to DOCUMENTATION_OPTIONS so that we can re-use later
    # Pagename to current page
    app.add_js_file(None, body=f"DOCUMENTATION_OPTIONS.pagename = '{pagename}';")
    if isinstance(context.get("theme_switcher"), dict):
        theme_switcher = context["theme_switcher"]
        json_url = theme_switcher["json_url"]
        version_match = theme_switcher["version_match"]

        # Add variables to our JavaScript for re-use in our main JS script
        js = f"""
        DOCUMENTATION_OPTIONS.theme_switcher_json_url = '{json_url}';
        DOCUMENTATION_OPTIONS.theme_switcher_version_match = '{version_match}';
        """
        app.add_js_file(None, body=js)


def add_inline_math(node):
    """Render a node with HTML tags that activate MathJax processing.
    This is meant for use with rendering section titles with math in them, because
    math outputs are ignored by pydata-sphinx-theme's header.

    related to the behaviour of a normal math node from:
    https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/mathjax.py#L28
    """

    return (
        '<span class="math notranslate nohighlight">' rf"\({node.astext()}\)" "</span>"
    )


def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects."""

    @lru_cache(maxsize=None)
    def generate_header_nav_html(n_links_before_dropdown=5):
        """
        Generate top-level links that are meant for the header navigation.
        We use this function instead of the TocTree-based one used for the
        sidebar because this one is much faster for generating the links and
        we don't need the complexity of the full Sphinx TocTree.

        This includes two kinds of links:

        - Links to pages described listed in the root_doc TocTrees
        - External links defined in theme configuration

        Additionally it will create a dropdown list for several links after
        a cutoff.

        Parameters
        ----------
        n_links_before_dropdown : int (default: 5)
            The number of links to show before nesting the remaining links in
            a Dropdown element.
        """

        try:
            n_links_before_dropdown = int(n_links_before_dropdown)
        except Exception:
            raise ValueError(
                f"n_links_before_dropdown is not an int: {n_links_before_dropdown}"
            )
        toctree = TocTree(app.env)

        # Find the active header navigation item so we decide whether to highlight
        # Will be empty if there is no active page (root_doc, or genindex etc)
        active_header_page = toctree.get_toctree_ancestors(pagename)
        if active_header_page:
            # The final list item will be the top-most ancestor
            active_header_page = active_header_page[-1]

        # Find the root document because it lists our top-level toctree pages
        root = app.env.tocs[app.config.root_doc]

        # Iterate through each toctree node in the root document
        # Grab the toctree pages and find the relative link + title.
        links_html = []
        # TODO: just use "findall" once docutils min version >=0.18.1
        meth = "findall" if hasattr(root, "findall") else "traverse"
        for toc in getattr(root, meth)(toctree_node):
            for title, page in toc.attributes["entries"]:
                # if the page is using "self" use the correct link
                page = toc.attributes["parent"] if page == "self" else page

                # If this is the active ancestor page, add a class so we highlight it
                current = " current active" if page == active_header_page else ""

                # sanitize page title for use in the html output if needed
                if title is None:
                    title = ""
                    for node in app.env.titles[page].children:
                        if isinstance(node, nodes.math):
                            title += add_inline_math(node)
                        else:
                            title += node.astext()

                # set up the status of the link and the path
                # if the path is relative then we use the context for the path
                # resolution and the internal class.
                # If it's an absolute one then we use the external class and
                # the complete url.
                is_absolute = bool(urlparse(page).netloc)
                link_status = "external" if is_absolute else "internal"
                link_href = page if is_absolute else context["pathto"](page)

                # create the html output
                links_html.append(
                    f"""
                    <li class="nav-item{current}">
                      <a class="nav-link nav-{link_status}" href="{link_href}">
                        {title}
                      </a>
                    </li>
                """
                )

        # Add external links defined in configuration as sibling list items
        for external_link in context["theme_external_links"]:
            links_html.append(
                f"""
                <li class="nav-item">
                  <a class="nav-link nav-external" href="{ external_link["url"] }">
                    { external_link["name"] }
                  </a>
                </li>
                """
            )

        # The first links will always be visible
        links_solo = links_html[:n_links_before_dropdown]
        out = "\n".join(links_solo)

        # Wrap the final few header items in a "more" dropdown
        links_dropdown = links_html[n_links_before_dropdown:]
        if links_dropdown:
            links_dropdown_html = "\n".join(links_dropdown)
            out += f"""
            <div class="nav-item dropdown">
                <button class="btn dropdown-toggle nav-item" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    More
                </button>
                <div class="dropdown-menu">
                    {links_dropdown_html}
                </div>
            </div>
            """  # noqa

        return out

    # TODO: Deprecate after v0.12
    def generate_nav_html(*args, **kwargs):
        logger.warning(
            "`generate_nav_html` is deprecated and will be removed."
            "Use `generate_toctree_html` instead."
        )
        generate_toctree_html(*args, **kwargs)

    # Cache this function because it is expensive to run, and becaues Sphinx
    # somehow runs this twice in some circumstances in unpredictable ways.
    @lru_cache(maxsize=None)
    def generate_toctree_html(kind, startdepth=1, show_nav_level=1, **kwargs):
        """
        Return the navigation link structure in HTML. This is similar to Sphinx's
        own default TocTree generation, but it is modified to generate TocTrees
        for *second*-level pages and below (not supported by default in Sphinx).
        This is used for our sidebar, which starts at the second-level page.

        It also modifies the generated TocTree slightly for Bootstrap classes
        and structure (via BeautifulSoup).

        Arguments are passed to Sphinx "toctree" function (context["toctree"] below).

        ref: https://www.sphinx-doc.org/en/master/templating.html#toctree

        Parameters
        ----------
        kind : "sidebar" or "raw"
            Whether to generate HTML meant for sidebar navigation ("sidebar")
            or to return the raw BeautifulSoup object ("raw").
        startdepth : int
            The level of the toctree at which to start. By default, for
            the navbar uses the normal toctree (`startdepth=0`), and for
            the sidebar starts from the second level (`startdepth=1`).
        show_nav_level : int
            The level of the navigation bar to toggle as visible on page load.
            By default, this level is 1, and only top-level pages are shown,
            with drop-boxes to reveal children. Increasing `show_nav_level`
            will show child levels as well.

        kwargs: passed to the Sphinx `toctree` template function.

        Returns
        -------
        HTML string (if kind == "sidebar") OR
        BeautifulSoup object (if kind == "raw")
        """
        if startdepth == 0:
            toc_sphinx = context["toctree"](**kwargs)
        else:
            # select the "active" subset of the navigation tree for the sidebar
            toc_sphinx = index_toctree(app, pagename, startdepth, **kwargs)

        soup = bs(toc_sphinx, "html.parser")

        # pair "current" with "active" since that's what we use w/ bootstrap
        for li in soup("li", {"class": "current"}):
            li["class"].append("active")

        # Remove sidebar links to sub-headers on the page
        for li in soup.select("li"):
            # Remove
            if li.find("a"):
                href = li.find("a")["href"]
                if "#" in href and href != "#":
                    li.decompose()

        if kind == "sidebar":
            # Add bootstrap classes for first `ul` items
            for ul in soup("ul", recursive=False):
                ul.attrs["class"] = ul.attrs.get("class", []) + ["nav", "bd-sidenav"]

            # Add collapse boxes for parts/captions.
            # Wraps the TOC part in an extra <ul> to behave like chapters with toggles
            # show_nav_level: 0 means make parts collapsible.
            if show_nav_level == 0:
                partcaptions = soup.find_all("p", attrs={"class": "caption"})
                if len(partcaptions):
                    new_soup = bs("<ul class='list-caption'></ul>", "html.parser")
                    for caption in partcaptions:
                        # Assume that the next <ul> element is the TOC list
                        # for this part
                        for sibling in caption.next_siblings:
                            if sibling.name == "ul":
                                toclist = sibling
                                break
                        li = soup.new_tag("li", attrs={"class": "toctree-l0"})
                        li.extend([caption, toclist])
                        new_soup.ul.append(li)
                    soup = new_soup

            # Add icons and labels for collapsible nested sections
            _add_collapse_checkboxes(soup)

            # Open the sidebar navigation to the proper depth
            for ii in range(int(show_nav_level)):
                for checkbox in soup.select(
                    f"li.toctree-l{ii} > input.toctree-checkbox"
                ):
                    checkbox.attrs["checked"] = None

        return soup

    @lru_cache(maxsize=None)
    def generate_toc_html(kind="html"):
        """Return the within-page TOC links in HTML."""

        if "toc" not in context:
            return ""

        soup = bs(context["toc"], "html.parser")

        # Add toc-hN + visible classes
        def add_header_level_recursive(ul, level):
            if ul is None:
                return
            if level <= (context["theme_show_toc_level"] + 1):
                ul["class"] = ul.get("class", []) + ["visible"]
            for li in ul("li", recursive=False):
                li["class"] = li.get("class", []) + [f"toc-h{level}"]
                add_header_level_recursive(li.find("ul", recursive=False), level + 1)

        add_header_level_recursive(soup.find("ul"), 1)

        # Add in CSS classes for bootstrap
        for ul in soup("ul"):
            ul["class"] = ul.get("class", []) + ["nav", "section-nav", "flex-column"]

        for li in soup("li"):
            li["class"] = li.get("class", []) + ["nav-item", "toc-entry"]
            if li.find("a"):
                a = li.find("a")
                a["class"] = a.get("class", []) + ["nav-link"]

        # If we only have one h1 header, assume it's a title
        h1_headers = soup.select(".toc-h1")
        if len(h1_headers) == 1:
            title = h1_headers[0]
            # If we have no sub-headers of a title then we won't have a TOC
            if not title.select(".toc-h2"):
                out = ""
            else:
                out = title.find("ul").prettify()
        # Else treat the h1 headers as sections
        else:
            out = soup.prettify()

        # Return the toctree object
        if kind == "html":
            return out
        else:
            return soup

    def navbar_align_class():
        """Return the class that aligns the navbar based on config."""
        align = context.get("theme_navbar_align", "content")
        align_options = {
            "content": ("col-lg-9", "mr-auto"),
            "left": ("", "mr-auto"),
            "right": ("", "ml-auto"),
        }
        if align not in align_options:
            raise ValueError(
                "Theme option navbar_align must be one of"
                f"{align_options.keys()}, got: {align}"
            )
        return align_options[align]

    context["generate_header_nav_html"] = generate_header_nav_html
    context["generate_toctree_html"] = generate_toctree_html
    context["generate_toc_html"] = generate_toc_html
    context["navbar_align_class"] = navbar_align_class

    # TODO: Deprecate after v0.12
    context["generate_nav_html"] = generate_nav_html


def _add_collapse_checkboxes(soup):
    """Add checkboxes to collapse children in a toctree."""
    # based on https://github.com/pradyunsg/furo

    toctree_checkbox_count = 0

    for element in soup.find_all("li", recursive=True):
        # We check all "li" elements, to add a "current-page" to the correct li.
        classes = element.get("class", [])

        # expanding the parent part explicitly, if present
        if "current" in classes:
            parentli = element.find_parent("li", class_="toctree-l0")
            if parentli:
                parentli.select("p.caption ~ input")[0].attrs["checked"] = ""

        # Nothing more to do, unless this has "children"
        if not element.find("ul"):
            continue

        # Add a class to indicate that this has children.
        element["class"] = classes + ["has-children"]

        # We're gonna add a checkbox.
        toctree_checkbox_count += 1
        checkbox_name = f"toctree-checkbox-{toctree_checkbox_count}"

        # Add the "label" for the checkbox which will get filled.
        if soup.new_tag is None:
            continue

        label = soup.new_tag(
            "label", attrs={"for": checkbox_name, "class": "toctree-toggle"}
        )
        label.append(soup.new_tag("i", attrs={"class": "fa-solid fa-chevron-down"}))
        if "toctree-l0" in classes:
            # making label cover the whole caption text with css
            label["class"] = "label-parts"
        element.insert(1, label)

        # Add the checkbox that's used to store expanded/collapsed state.
        checkbox = soup.new_tag(
            "input",
            attrs={
                "type": "checkbox",
                "class": ["toctree-checkbox"],
                "id": checkbox_name,
                "name": checkbox_name,
            },
        )

        # if this has a "current" class, be expanded by default
        # (by checking the checkbox)
        if "current" in classes:
            checkbox.attrs["checked"] = ""

        element.insert(1, checkbox)


def _get_local_toctree_for(
    self: TocTree, indexname: str, docname: str, builder, collapse: bool, **kwargs
):
    """Return the "local" TOC nodetree (relative to `indexname`)."""
    # this is a copy of `TocTree.get_toctree_for`, but where the sphinx version
    # always uses the "root" doctree:
    #     doctree = self.env.get_doctree(self.env.config.root_doc)
    # we here use the `indexname` additional argument to be able to use a subset
    # of the doctree (e.g. starting at a second level for the sidebar):
    #     doctree = app.env.tocs[indexname].deepcopy()

    doctree = self.env.tocs[indexname].deepcopy()

    toctrees = []
    if "includehidden" not in kwargs:
        kwargs["includehidden"] = True
    if "maxdepth" not in kwargs or not kwargs["maxdepth"]:
        kwargs["maxdepth"] = 0
    else:
        kwargs["maxdepth"] = int(kwargs["maxdepth"])
    kwargs["collapse"] = collapse

    # FIX: Can just use "findall" once docutils 0.18+ is required
    meth = "findall" if hasattr(doctree, "findall") else "traverse"
    for toctreenode in getattr(doctree, meth)(addnodes.toctree):
        toctree = self.resolve(docname, builder, toctreenode, prune=True, **kwargs)
        if toctree:
            toctrees.append(toctree)
    if not toctrees:
        return None
    result = toctrees[0]
    for toctree in toctrees[1:]:
        result.extend(toctree.children)
    return result


def index_toctree(app, pagename: str, startdepth: int, collapse: bool = True, **kwargs):
    """
    Returns the "local" (starting at `startdepth`) TOC tree containing the
    current page, rendered as HTML bullet lists.

    This is the equivalent of `context["toctree"](**kwargs)` in sphinx
    templating, but using the startdepth-local instead of global TOC tree.
    """
    # this is a variant of the function stored in `context["toctree"]`, which is
    # defined as `lambda **kwargs: self._get_local_toctree(pagename, **kwargs)`
    # with `self` being the HMTLBuilder and the `_get_local_toctree` basically
    # returning:
    #     return self.render_partial(TocTree(self.env).get_toctree_for(
    #         pagename, self, collapse, **kwargs))['fragment']

    if "includehidden" not in kwargs:
        kwargs["includehidden"] = False
    if kwargs.get("maxdepth") == "":
        kwargs.pop("maxdepth")

    toctree = TocTree(app.env)
    ancestors = toctree.get_toctree_ancestors(pagename)
    try:
        indexname = ancestors[-startdepth]
    except IndexError:
        # eg for index.rst, but also special pages such as genindex, py-modindex, search
        # those pages don't have a "current" element in the toctree, so we can
        # directly return an empty string instead of using the default sphinx
        # toctree.get_toctree_for(pagename, app.builder, collapse, **kwargs)
        return ""

    toctree_element = _get_local_toctree_for(
        toctree, indexname, pagename, app.builder, collapse, **kwargs
    )
    return app.builder.render_partial(toctree_element)["fragment"]


def soup_to_python(soup, only_pages=False):
    """
    Convert the toctree html structure to python objects which can be used in Jinja.

    Parameters
    ----------
    soup : BeautifulSoup object for the toctree
    only_pages : bool
        Only include items for full pages in the output dictionary. Exclude
        anchor links (TOC items with a URL that starts with #)

    Returns
    -------
    nav : list of dicts
        The toctree, converted into a dictionary with key/values that work
        within Jinja.
    """
    # toctree has this structure (caption only for toctree, not toc)
    #   <p class="caption">...</span></p>
    #   <ul>
    #       <li class="toctree-l1"><a href="..">..</a></li>
    #       <li class="toctree-l1"><a href="..">..</a></li>
    #       ...

    def extract_level_recursive(ul, navs_list):

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


# -----------------------------------------------------------------------------


def setup_edit_url(app, pagename, templatename, context, doctree):
    """Add a function that jinja can access for returning the edit URL of a page."""

    def get_edit_url():
        """Return a URL for an "edit this page" link."""
        file_name = f"{pagename}{context['page_source_suffix']}"

        # Make sure that doc_path has a path separator only if it exists (to avoid //)
        doc_path = context.get("doc_path", "")
        if doc_path and not doc_path.endswith("/"):
            doc_path = f"{doc_path}/"

        default_provider_urls = {
            "bitbucket_url": "https://bitbucket.org",
            "github_url": "https://github.com",
            "gitlab_url": "https://gitlab.com",
        }

        edit_url_attrs = {}

        # ensure custom URL is checked first, if given
        url_template = context.get("edit_page_url_template")

        if url_template is not None:
            if "file_name" not in url_template:
                raise ExtensionError(
                    "Missing required value for `use_edit_page_button`. "
                    "Ensure `file_name` appears in `edit_page_url_template`: "
                    f"{url_template}"
                )

            edit_url_attrs[("edit_page_url_template",)] = url_template

        edit_url_attrs.update(
            {
                ("bitbucket_user", "bitbucket_repo", "bitbucket_version"): (
                    "{{ bitbucket_url }}/{{ bitbucket_user }}/{{ bitbucket_repo }}"
                    "/src/{{ bitbucket_version }}"
                    "/{{ doc_path }}{{ file_name }}?mode=edit"
                ),
                ("github_user", "github_repo", "github_version"): (
                    "{{ github_url }}/{{ github_user }}/{{ github_repo }}"
                    "/edit/{{ github_version }}/{{ doc_path }}{{ file_name }}"
                ),
                ("gitlab_user", "gitlab_repo", "gitlab_version"): (
                    "{{ gitlab_url }}/{{ gitlab_user }}/{{ gitlab_repo }}"
                    "/-/edit/{{ gitlab_version }}/{{ doc_path }}{{ file_name }}"
                ),
            }
        )

        doc_context = dict(default_provider_urls)
        doc_context.update(context)
        doc_context.update(doc_path=doc_path, file_name=file_name)

        for attrs, url_template in edit_url_attrs.items():
            if all(doc_context.get(attr) not in [None, "None"] for attr in attrs):
                return jinja2.Template(url_template).render(**doc_context)

        raise ExtensionError(
            "Missing required value for `use_edit_page_button`. "
            "Ensure one set of the following in your `html_context` "
            f"configuration: {sorted(edit_url_attrs.keys())}"
        )

    context["get_edit_url"] = get_edit_url

    # Ensure that the max TOC level is an integer
    context["theme_show_toc_level"] = int(context.get("theme_show_toc_level", 1))


# ------------------------------------------------------------------------------
# handle pygment css
# ------------------------------------------------------------------------------

# inspired by the Furo theme
# https://github.com/pradyunsg/furo/blob/main/src/furo/__init__.py


def _get_styles(formatter, prefix):
    """
    Get styles out of a formatter, where everything has the correct prefix.
    """

    for line in formatter.get_linenos_style_defs():
        yield f"{prefix} {line}"
    yield from formatter.get_background_style_defs(prefix)
    yield from formatter.get_token_style_defs(prefix)


def get_pygments_stylesheet(light_style, dark_style):
    """
    Generate the theme-specific pygments.css.
    There is no way to tell Sphinx how the theme handles modes
    """
    light_formatter = HtmlFormatter(style=light_style)
    dark_formatter = HtmlFormatter(style=dark_style)

    lines = []

    light_prefix = 'html[data-theme="light"] .highlight'
    lines.extend(_get_styles(light_formatter, prefix=light_prefix))

    dark_prefix = 'html[data-theme="dark"] .highlight'
    lines.extend(_get_styles(dark_formatter, prefix=dark_prefix))

    return "\n".join(lines)


def _overwrite_pygments_css(app, exception=None):
    """
    Sphinx is not build to host multiple sphinx formatter and there is no way
    to tell which one to use and when.
    So yes, at build time we overwrite the pygment.css file so that it embeds
    2 versions:
    - the light theme prefixed with "[data-theme="light"]" using tango
    - the dark theme prefixed with "[data-theme="dark"]" using monokai

    When the theme is switched, Pygments will be using one of the preset css
    style.
    """
    default_light_theme = "tango"
    default_dark_theme = "monokai"

    if exception is not None:
        return

    assert app.builder

    # check the theme specified in the theme options
    theme_options = app.config["html_theme_options"]
    pygments_styles = list(get_all_styles())
    light_theme = theme_options.get("pygment_light_style", default_light_theme)
    if light_theme not in pygments_styles:
        logger.warning(
            f"{light_theme}, is not part of the available pygments style,"
            f' defaulting to "{default_light_theme}".'
        )
        light_theme = default_light_theme
    dark_theme = theme_options.get("pygment_dark_style", default_dark_theme)
    if dark_theme not in pygments_styles:
        logger.warning(
            f"{dark_theme}, is not part of the available pygments style,"
            f' defaulting to "{default_dark_theme}".'
        )
        dark_theme = default_dark_theme

    pygment_css = Path(app.builder.outdir) / "_static" / "pygments.css"
    with pygment_css.open("w") as f:
        f.write(get_pygments_stylesheet(light_theme, dark_theme))


# ------------------------------------------------------------------------------
# customize rendering of the links
# ------------------------------------------------------------------------------


def _traverse_or_findall(node, condition, **kwargs):
    """Triage node.traverse (docutils <0.18.1) vs node.findall.
    TODO: This check can be removed when the minimum supported docutils version
    for numpydoc is docutils>=0.18.1
    """
    return (
        node.findall(condition, **kwargs)
        if hasattr(node, "findall")
        else node.traverse(condition, **kwargs)
    )


class ShortenLinkTransform(SphinxPostTransform):
    """
    Shorten link when they are coming from github or gitlab and add an extra class to the tag
    for further styling.
    Before::
        <a class="reference external" href="https://github.com/2i2c-org/infrastructure/issues/1329">
            https://github.com/2i2c-org/infrastructure/issues/1329
        </a>
    After::
        <a class="reference external github" href="https://github.com/2i2c-org/infrastructure/issues/1329">
            2i2c-org/infrastructure#1329
        </a>
    """  # noqa

    default_priority = 400
    formats = ("html",)
    supported_platform = {"github.com": "github", "gitlab.com": "gitlab"}
    platform = None

    def run(self, **kwargs):
        matcher = NodeMatcher(nodes.reference)
        # TODO: just use "findall" once docutils min version >=0.18.1
        for node in _traverse_or_findall(self.document, matcher):
            uri = node.attributes.get("refuri")
            text = next(iter(node.children), None)
            # only act if the uri and text are the same
            # if not the user has already customized the display of the link
            if uri is not None and text is not None and text == uri:
                uri = urlparse(uri)
                # only do something if the platform is identified
                self.platform = self.supported_platform.get(uri.netloc)
                if self.platform is not None:
                    node.attributes["classes"].append(self.platform)
                    node.children[0] = nodes.Text(self.parse_url(uri))

    def parse_url(self, uri):
        """
        parse the content of the url with respect to the selected platform
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
            if any(map(uri.path.__contains__, ["issues", "merge_requests"])):
                group_and_subgroups, parts, *_ = path.split("/-/")
                parts = parts.split("/")
                url_type, element_number, *_ = parts
                if url_type == "issues":
                    text = f"{group_and_subgroups}#{element_number}"
                elif url_type == "merge_requests":
                    text = f"{group_and_subgroups}!{element_number}"
            else:
                # display the whole uri (after "gitlab.com/") including parameters
                # for example "<group>/<subgroup1>/<subgroup2>/<repository>"
                text = uri._replace(netloc="", scheme="")  # remove platform
                text = urlunparse(text)[1:]  # combine to string and strip leading "/"

        return text


# -----------------------------------------------------------------------------


def setup(app):
    here = Path(__file__).parent.resolve()
    theme_path = here / "theme" / "pydata_sphinx_theme"

    app.add_html_theme("pydata_sphinx_theme", str(theme_path))

    app.add_post_transform(ShortenLinkTransform)

    app.set_translator("html", BootstrapHTML5Translator)
    # Read the Docs uses ``readthedocs`` as the name of the build, and also
    # uses a special "dirhtml" builder so we need to replace these both with
    # our custom HTML builder
    app.set_translator("readthedocs", BootstrapHTML5Translator, override=True)
    app.set_translator("readthedocsdirhtml", BootstrapHTML5Translator, override=True)

    app.connect("env-updated", update_config)
    app.connect("html-page-context", setup_edit_url)
    app.connect("html-page-context", add_toctree_functions)
    app.connect("html-page-context", update_templates)
    app.connect("html-page-context", prepare_html_config)
    app.connect("build-finished", _overwrite_pygments_css)

    # Include component templates
    app.config.templates_path.append(str(theme_path / "components"))

    return {"parallel_read_safe": True, "parallel_write_safe": True}
