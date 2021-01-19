"""
Bootstrap-based sphinx theme from the PyData community
"""
import os

from sphinx.errors import ExtensionError
from bs4 import BeautifulSoup as bs

from .bootstrap_html_translator import BootstrapHTML5Translator

__version__ = "0.4.2dev0"


def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects."""

    def get_nav_object(kind, **kwargs):
        """Return the navigation link structure in HTML. Arguments are passed
        to Sphinx "toctree" function (context["toctree"] below).

        We use beautifulsoup to add the right CSS classes / structure for bootstrap.

        See https://www.sphinx-doc.org/en/master/templating.html#toctree.

        Parameters
        ----------

        kind : ["navbar", "sidebar", "raw"]
            The kind of UI element this toctree is generated for.
        kwargs: passed to the Sphinx `toctree` template function.

        Returns
        -------

        nav_object : HTML string (if kind in ["navbar", "sidebar"]) or BeautifulSoup
                     object (if kind == "raw")
        """
        toc_sphinx = context["toctree"](**kwargs)
        soup = bs(toc_sphinx, "html.parser")

        # pair "current" with "active" since that's what we use w/ bootstrap
        for li in soup("li", {"class": "current"}):
            li["class"].append("active")

        if kind == "navbar":
            # Add CSS for bootstrap
            for li in soup("li"):
                li["class"].append("nav-item")
                li.find("a")["class"].append("nav-link")
            out = "\n".join([ii.prettify() for ii in soup.find_all("li")])

        elif kind == "sidebar":
            # Remove sidebar links to sub-headers on the page
            for li in soup.select("li.current ul li"):
                # Remove
                if li.find("a"):
                    href = li.find("a")["href"]
                    if "#" in href and href != "#":
                        li.decompose()

            # Join all the top-level `li`s together for display
            current_lis = soup.select("li.current.toctree-l1 li.toctree-l2")
            out = "\n".join([ii.prettify() for ii in current_lis])

        elif kind == "raw":
            out = soup

        return out

    def get_page_toc_object(kind="html"):
        """Return the within-page TOC links in HTML."""

        if "toc" not in context:
            return ""

        soup = bs(context["toc"], "html.parser")

        # Add toc-hN + visible classes
        def add_header_level_recursive(ul, level):
            if level <= (context["theme_show_toc_level"] + 1):
                ul["class"] = ul.get("class", []) + ["visible"]
            for li in ul("li", recursive=False):
                li["class"] = li.get("class", []) + [f"toc-h{level}"]
                ul = li.find("ul", recursive=False)
                if ul:
                    add_header_level_recursive(ul, level + 1)

        add_header_level_recursive(soup.find("ul"), 1)

        # Add in CSS classes for bootstrap
        for ul in soup("ul"):
            ul["class"] = ul.get("class", []) + ["nav", "section-nav", "flex-column"]

        for li in soup("li"):
            li["class"] = li.get("class", []) + ["nav-item", "toc-entry"]
            if li.find("a"):
                a = li.find("a")
                a["class"] = a.get("class", []) + ["nav-link"]

        # Keep only the sub-sections of the title (so no title is shown)
        title = soup.find("a", attrs={"href": "#"})
        if title:
            title = title.parent
            # Only show if children of the title item exist
            if title.select("ul li"):
                out = title.find("ul").prettify()
            else:
                out = ""
        else:
            out = ""

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
                (
                    "Theme optione navbar_align must be one of"
                    f"{align_options.keys()}, got: {align}"
                )
            )
        return align_options[align]

    context["get_nav_object"] = get_nav_object
    context["get_page_toc_object"] = get_page_toc_object
    context["navbar_align_class"] = navbar_align_class


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

        # Enable optional custom github url for self-hosted github instances
        github_url = "https://github.com"
        if context.get("github_url"):
            github_url = context["github_url"]

        github_user = context["github_user"]
        github_repo = context["github_repo"]
        github_version = context["github_version"]
        file_name = f"{pagename}{context['page_source_suffix']}"

        # Make sure that doc_path has a path separator only if it exists (to avoid //)
        doc_path = context.get("doc_path", "")
        if doc_path and not doc_path.endswith("/"):
            doc_path = f"{doc_path}/"

        # Build the URL for "edit this button"
        url_edit = (
            f"{github_url}/{github_user}/{github_repo}"
            f"/edit/{github_version}/{doc_path}{file_name}"
        )
        return url_edit

    context["get_edit_url"] = get_edit_url

    # Ensure that the max TOC level is an integer
    context["theme_show_toc_level"] = int(context.get("theme_show_toc_level", 1))


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

    # Update templates for sidebar
    pkgdir = os.path.abspath(os.path.dirname(__file__))
    path_templates = os.path.join(pkgdir, "_templates")
    app.config.templates_path.append(path_templates)

    return {"parallel_read_safe": True, "parallel_write_safe": True}
