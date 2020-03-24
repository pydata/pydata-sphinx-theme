"""
Sphinx Bootstrap theme.

Adapted for the pandas documentation.
"""
import os

import sphinx.builders.html
from sphinx.errors import ExtensionError
from sphinx.environment.adapters.toctree import TocTree
from sphinx import addnodes
from docutils import nodes
from pathlib import Path

from .bootstrap_html_translator import BootstrapHTML5Translator
import docutils

__version__ = "0.1.1"


def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects.
    
    This converts the docutils nodes into a nested dictionary that Jinja can
    use in our templating.
    """

    def get_nav_object(maxdepth=None, collapse=True, subpage_caption=False, **kwargs):
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
        toc = TocTree(app.env)
        toctree = toc.get_toctree_for(
            pagename, app.builder, collapse=collapse, maxdepth=maxdepth, **kwargs
        )

        # If no toctree is defined (AKA a single-page site), skip this
        if toctree is None:
            return []

        # Grab all of the first-level pages from the index toctree
        toctrees_root = app.env.tocs[app.env.config['master_doc']]
        first_pages = []
        for toctree_root in toctrees_root.traverse(addnodes.toctree):
            for _, path_first_page in toctree_root.attributes.get("entries", []):
                first_pages.append(path_first_page)

        # Now find the toctrees for each first page and see if it has a caption
        caption_pages = []
        for first_page in first_pages:
            toctrees_first_page = app.env.tocs[first_page]
            for toctree_first_page in toctrees_first_page.traverse(addnodes.toctree):
                # If the toctree has a caption, keep track of the first page
                caption = toctree_first_page.attributes.get("caption")
                if caption:
                    _, first_entry = toctree_first_page.attributes.get("entries", [])[0]
                    caption_pages.append((first_entry, caption))

        # toctree has this structure
        #   <caption>
        #   <bullet_list>
        #       <list_item classes="toctree-l1">
        #       <list_item classes="toctree-l1">
        # `list_item`s are the actual TOC links and are the only thing we want
        toc_items = []
        for child in toctree.children:
            if isinstance(child, docutils.nodes.bullet_list):
                for list_entry in child:
                    if isinstance(list_entry, docutils.nodes.list_item):
                        # Grab the toc path relative to the current page
                        list_entry_ref = list(list_entry.traverse(nodes.reference))[0]
                        ref_uri = list_entry_ref.attributes.get('refuri')
                        if ref_uri == "":
                            # Will be "" for the *current* page
                            ref_uri = pagename
                        # Parent folder of current page
                        path_pagename_parent = Path(pagename).parent.resolve()
                        # Absolute path of the entry
                        path_entry = path_pagename_parent.joinpath(Path(ref_uri)).resolve()
                        # Absolute path of docs root
                        path_root = Path(app.env.config['master_doc']).parent.resolve()
                        # Path relative to docs root of the entry
                        path_entry_rel_root = path_entry.relative_to(path_root).with_suffix("")
                        
                        # Check whether the entry path is one of the pages that should have a caption first
                        for path_caption_page, icaption in caption_pages:
                            if path_caption_page == str(path_entry_rel_root):
                                toc_items.append({'caption': icaption})

                        toc_items.append(list_entry)

        # Now convert our docutils nodes into dicts that Jinja can use
        nav = [docutils_node_to_jinja(child, only_pages=True) for child in toc_items]
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
    # If a caption, pass it through
    if isinstance(list_item, docutils.nodes.caption):
        nav = {"text": list_item.astext(), "type": "caption"}
        return nav

    # Else, we assume it's a list item and need to parse the item content
    if not list_item.children:
        return None

    # We assume this structure of a list item:
    # <list_item>
    #     <compact_paragraph >
    #         <reference> <-- the thing we want
    reference = list_item.children[0].children[0]
    title = reference.astext()

    url = reference.attributes.get("refuri", "")
    active = "current" in list_item.attributes["classes"]

    # If we've got an anchor link, skip it if we wish
    if only_pages and "#" in url:
        return None

    # Converting the docutils attributes into jinja-friendly objects
    nav = {}
    nav["title"] = title
    nav["url"] = url
    nav["active"] = active
    nav["type"] = "ref"

    # Recursively convert children as well
    # If there are sub-pages for this list_item, there should be two children:
    # a paragraph, and a bullet_list.
    nav["children"] = []
    if len(list_item.children) > 1:
        child_pages = list_item.children[1:]
        for child in child_pages:
            # Will either be a caption or another bullet list
            if isinstance(child, nodes.bullet_list):
                for subpage in child.children:
                    this_nav = docutils_node_to_jinja(subpage, only_pages=only_pages)
                    nav["children"].append(this_nav)
            else:
                this_nav = docutils_node_to_jinja(child, only_pages=only_pages)
                nav["children"].append(this_nav)
    return nav


# -----------------------------------------------------------------------------


def setup_edit_url(app, pagename, templatename, context, doctree):
    """Add a function that jinja can access for returning the edit URL of a page."""

    def get_edit_url():
        """Return a URL for an "edit this page" link."""
        required_values = ["github_user", "github_repo", "github_version"]
        for val in required_values:
            if not context.get(val):
                raise ExtensionError(
                    "Missing required value for `edit this page` button. "
                    "Add %s to your `html_context` configuration" % val
                )

        github_user = context["github_user"]
        github_repo = context["github_repo"]
        github_version = context["github_version"]
        file_name = f"{pagename}{context['page_source_suffix']}"

        # Make sure that doc_path has a path separator only if it exists (to avoid //)
        doc_path = context.get("doc_path", "")
        if doc_path and not doc_path.endswith("/"):
            doc_path = f"{doc_path}/"

        # Build the URL for "edit this button"
        url_edit = f"https://github.com/{github_user}/{github_repo}/edit/{github_version}/{doc_path}{file_name}"
        return url_edit

    context["get_edit_url"] = get_edit_url


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
    app.set_translator("readthedocsdirhtml", BootstrapHTML5Translator, override=True)
    app.connect("html-page-context", setup_edit_url)
    app.connect("html-page-context", add_toctree_functions)
