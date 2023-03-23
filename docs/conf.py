# -- Path setup --------------------------------------------------------------
import os
import sys
import pydata_sphinx_theme

sys.path.append("scripts")
from gallery_directive import GalleryDirective

# -- Project information -----------------------------------------------------

project = "PyData Theme"
copyright = "2019, PyData Community"
author = "PyData Community"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinxext.rediraffe",
    "sphinx_design",
    "sphinx_copybutton",
    # For extension examples and demos
    "ablog",
    "jupyter_sphinx",
    "matplotlib.sphinxext.plot_directive",
    "myst_nb",
    "sphinxcontrib.youtube",
    # "nbsphinx",  # Uncomment and comment-out MyST-NB for local testing purposes.
    "numpydoc",
    "sphinx_togglebutton",
    "sphinx_favicon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Sitemap -----------------------------------------------------------------

# ReadTheDocs has its own way of generating sitemaps, etc.
if not os.environ.get("READTHEDOCS"):
    extensions += ["sphinx_sitemap"]

    html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"


# -- autosummary -------------------------------------------------------------

autosummary_generate = True


# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = "en"

# -- MyST options ------------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence", "linkify", "substitution"]
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

# -- Ablog options -----------------------------------------------------------

blog_path = "examples/blog/index"
blog_authors = {
    "pydata": ("PyData", "https://pydata.org"),
    "jupyter": ("Jupyter", "https://jupyter.org"),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"
html_sourcelink_suffix = ""

# Define the json_url for our version switcher.
json_url = "https://pydata-sphinx-theme.readthedocs.io/en/latest/_static/switcher.json"

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("READTHEDOCS_VERSION")
# If READTHEDOCS_VERSION doesn't exist, we're not on RTD
# If it is an integer, we're in a PR build and the version isn't correct.
if not version_match or version_match.isdigit():
    # For local development, infer the version to match from the package.
    release = pydata_sphinx_theme.__version__
    if "dev" in release or "rc" in release:
        version_match = "latest"
        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "_static/switcher.json"
    else:
        version_match = "v" + release

html_theme_options = {
    "external_links": [
        {
            "url": "https://pydata.org",
            "name": "PyData",
        },
        {
            "url": "https://numfocus.org/",
            "name": "NumFocus",
        },
        {
            "url": "https://numfocus.org/donate",
            "name": "Donate to NumFocus",
        },
    ],
    "github_url": "https://github.com/pydata/pydata-sphinx-theme",
    "twitter_url": "https://twitter.com/PyData",
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pydata-sphinx-theme",
            "icon": "fa-solid fa-box",
        },
        {
            "name": "PyData",
            "url": "https://pydata.org",
            "icon": "_static/pydata-logo.png",
            "type": "local",
            "attributes": {"target": "_blank"},
        },
    ],
    "logo": {
        "text": "PyData Theme",
        "image_dark": "_static/logo-dark.svg",
        "alt_text": "PyData Theme",
    },
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    "navbar_center": ["version-switcher", "navbar-nav"],
    "announcement": "https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/main/docs/_templates/custom-template.html",
    # "show_nav_level": 2,
    # "navbar_start": ["navbar-logo"],
    # "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # "navbar_persistent": ["search-button"],
    # "primary_sidebar_end": ["custom-template.html", "sidebar-ethical-ads.html"],
    # "article_footer_items": ["prev-next.html", "test.html", "test.html"],
    # "content_footer_items": ["prev-next.html", "test.html", "test.html"],
    # "footer_start": ["test.html", "test.html"],
    # "secondary_sidebar_items": ["page-toc.html"],  # Remove the source buttons
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
    # "search_bar_position": "navbar",  # TODO: Deprecated - remove in future version
}

html_sidebars = {
    "community/index": [
        "sidebar-nav-bs",
        "custom-template",
    ],  # This ensures we test for custom sidebars
    "examples/no-sidebar": [],  # Test what page looks like with no sidebar items
    "examples/persistent-search-field": ["search-field"],
    # Blog sidebars
    # ref: https://ablog.readthedocs.io/manual/ablog-configuration-options/#blog-sidebars
    "examples/blog/*": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/authors.html",
        "ablog/languages.html",
        "ablog/locations.html",
        "ablog/archives.html",
    ],
}

html_context = {
    "github_user": "pydata",
    "github_repo": "pydata-sphinx-theme",
    "github_version": "main",
    "doc_path": "docs",
}

rediraffe_redirects = {
    "contributing.rst": "community/index.rst",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["custom.css"]
todo_include_todos = True

# -- favicon options ---------------------------------------------------------

# see https://sphinx-favicon.readthedocs.io for more information about the
# sphinx-favicon extension
favicons = [
    # generic icons compatible with most browsers
    "favicon-32x32.png",
    "favicon-16x16.png",
    {"rel": "shortcut icon", "sizes": "any", "href": "favicon.ico"},
    # chrome specific
    "android-chrome-192x192.png",
    # apple icons
    {"rel": "mask-icon", "color": "#459db9", "href": "safari-pinned-tab.svg"},
    {"rel": "apple-touch-icon", "href": "apple-touch-icon.png"},
    # msapplications
    {"name": "msapplication-TileColor", "content": "#459db9"},
    {"name": "theme-color", "content": "#ffffff"},
    {"name": "msapplication-TileImage", "content": "mstile-150x150.png"},
]

# -- application setup -------------------------------------------------------


def setup_to_main(app, pagename, templatename, context, doctree):
    def to_main(link: str) -> str:
        """Transform "edit on github" links and make sure they always point to the main branch

        Args:
            link: the link to the github edit interface

        Returns:
            the link to the tip of the main branch for the same file
        """
        links = link.split("/")
        idx = links.index("edit")
        return "/".join(links[: idx + 1]) + "/main/" + "/".join(links[idx + 2 :])

    context["to_main"] = to_main


def setup(app):
    app.add_directive("gallery-grid", GalleryDirective)
    app.connect("html-page-context", setup_to_main)
