"""
Sphinx Bootstrap theme.

Adapted for the pandas documentation.
"""
import os

import sphinx.builders.html
from sphinx.errors import ExtensionError

from .bootstrap_html_translator import BootstrapHTML5Translator
import docutils

__version__ = "0.1.1"


def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects.
    
    This converts the docutils nodes into a nested dictionary that Jinja can
    use in our templating.
    """
    from sphinx.environment.adapters.toctree import TocTree

    def get_nav_object(maxdepth=None, collapse=True, **kwargs):
        """Return a list of nav links that can be accessed from Jinja.

        Parameters
        ----------
        maxdepth: int
            How many layers of TocTree will be returned
        collapse: bool
            Whether to only include sub-pages of the currently-active page,
            instead of sub-pages of all top-level pages of the site.
        kwargs: key/val pairs
            Passed to the `TocTree.get_toctree_for` Sphinx method
        """
        # The TocTree will contain the full site TocTree including sub-pages.
        # "collapse=True" collapses sub-pages of non-active TOC pages.
        # maxdepth controls how many TOC levels are returned
        toctree = TocTree(app.env).get_toctree_for(
            pagename, app.builder, collapse=collapse, maxdepth=maxdepth, **kwargs
        )

        # toctree has this structure
        #   <caption>
        #   <bullet_list>
        #       <list_item classes="toctree-l1">
        #       <list_item classes="toctree-l1">
        # `list_item`s are the actual TOC links and are the only thing we want
        toc_items = [item for child in toctree.children for item in child
                     if isinstance(item, docutils.nodes.list_item)]

        # Now convert our docutils nodes into dicts that Jinja can use
        nav = [docutils_node_to_jinja(child, only_pages=True)
               for child in toc_items]

        return nav

    def get_page_toc_object():
        """Return a list of within-page TOC links that can be accessed from Jinja."""
        self_toc = TocTree(app.env).get_toc_for(pagename, app.builder)

        try:
            nav = docutils_node_to_jinja(self_toc.children[0])
            return nav
        except:
            return {}

    context["get_nav_object"] = get_nav_object
    context["get_page_toc_object"] = get_page_toc_object

def docutils_node_to_jinja(list_item, only_pages=False):
    """Convert a docutils node to a structure that can be read by Jinja.

    Parameters
    ----------
    list_item : docutils list_item node
        A parent item, potentially with children, corresponding to the level
        of a TocTree.
    only_pages : bool
        Only include items for full pages in the output dictionary. Exclude
        anchor links (TOC items with a URL that starts with #)

    Returns
    -------
    nav : dict
        The TocTree, converted into a dictionary with key/values that work
        within Jinja.
    """
    if not list_item.children:
        return None

    # We assume this structure of a list item:
    # <list_item>
    #     <compact_paragraph >
    #         <reference> <-- the thing we want
    reference = list_item.children[0].children[0]
    title = reference.astext()
    url = reference.attributes["refuri"]
    active = "current" in list_item.attributes["classes"]

    # If we've got an anchor link, skip it if we wish
    if only_pages and '#' in url:
        return None

    # Converting the docutils attributes into jinja-friendly objects
    nav = {}
    nav["title"] = title
    nav["url"] = url
    nav["active"] = active

    # Recursively convert children as well
    # If there are sub-pages for this list_item, there should be two children:
    # a paragraph, and a bullet_list.
    nav["children"] = []
    if len(list_item.children) > 1:
        # The `.children` of the bullet_list has the nodes of the sub-pages.
        subpage_list = list_item.children[1].children
        for sub_page in subpage_list:
            child_nav = docutils_node_to_jinja(sub_page, only_pages=only_pages)
            if child_nav is not None:
                nav["children"].append(child_nav)
    return nav


# -----------------------------------------------------------------------------

def setup_edit_url(app, pagename, templatename, context, doctree):
    """Add a function that jinja can access for returning the edit URL of a page."""
    def get_edit_url():
        """Return a URL for an "edit this page" link."""
        required_values = ["github_user", "github_repo", "github_version"]
        for val in required_values:
            if not context.get(val):
                raise ExtensionError("Missing required value for `edit this page` button. "
                                        "Add %s to your `html_context` configuration" % val)

        github_user = context['github_user']
        github_repo = context['github_repo']
        github_version = context['github_version']
        file_name = f"{pagename}{context['page_source_suffix']}"

        # Make sure that doc_path has a path separator only if it exists (to avoid //)
        doc_path = context.get("doc_path", "")
        if doc_path and not doc_path.endswith("/"):
            doc_path = f"{doc_path}/"

        # Build the URL for "edit this button"
        url_edit = f"https://github.com/{github_user}/{github_repo}/edit/{github_version}/{doc_path}{file_name}"
        return url_edit

    context['get_edit_url'] = get_edit_url


# -----------------------------------------------------------------------------


def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = os.path.abspath(os.path.dirname(__file__))
    return [theme_path]


def setup(app):
    theme_path = get_html_theme_path()[0]
    app.add_html_theme("pydata_sphinx_theme", theme_path)
    app.set_translator("html", BootstrapHTML5Translator)

    # Read the Docs uses ``readthedocs`` as the name of the build, and also
    # uses a special "dirhtml" builder so we need to replace these both with
    # our custom HTML builder
    app.set_translator("readthedocs", BootstrapHTML5Translator, override=True)
    app.set_translator('readthedocsdirhtml', BootstrapHTML5Translator, override=True)
    app.connect("html-page-context", setup_edit_url)
    app.connect("html-page-context", add_toctree_functions)
