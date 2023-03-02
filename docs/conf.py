# -- Path setup ----------------------------------------------------------------
import os
import sys

sys.path.append(".")
from scripts.gallery_directive import GalleryDirective
import pydata_sphinx_theme

# -- Project information -------------------------------------------------------

project = "PyData Theme"
copyright = "2019, PyData Community"
author = "PyData Community"

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinxext.rediraffe",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx-favicon",
    # For extension examples and demos
    "ablog",
    "jupyter_sphinx",
    "matplotlib.sphinxext.plot_directive",
    "myst_nb",
    "sphinxcontrib.youtube",
    # "nbsphinx",  # Uncomment and comment-out MyST-NB for local testing purposes.
    "numpydoc",
    "sphinx_togglebutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Internationalization ------------------------------------------------------
language = "en"  # specifying the natural language

# -- Sitemap -------------------------------------------------------------------

# ReadTheDocs has its own way of generating sitemaps, etc.
if not os.environ.get("READTHEDOCS"):
    extensions += ["sphinx_sitemap"]

    html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"

# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_sourcelink_suffix = ""
html_static_path = ["_static"]
html_css_files = ["custom.css"]

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
        "postcard.html",
        "recentposts.html",
        "tagcloud.html",
        "categories.html",
        "authors.html",
        "languages.html",
        "locations.html",
        "archives.html",
    ],
}

html_context = {
    "github_user": "pydata",
    "github_repo": "pydata-sphinx-theme",
    "github_version": "main",
    "doc_path": "docs",
}

# -- pydata-sphinx-theme configuration -----------------------------------------

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

# set the options
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
    # "footer_start": ["test.html", "test.html"],
    # "secondary_sidebar_items": ["page-toc.html"],  # Remove the source buttons
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
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

# -- Autosumary configuration --------------------------------------------------
autosummary_generate = True

# -- Myst configuration --------------------------------------------------------
myst_enable_extensions = ["colon_fence", "linkify", "substitution"]
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

# -- Rediraffe configuration ---------------------------------------------------
rediraffe_redirects = {"contributing.rst": "community/index.rst"}

# -- ABlog configuration -------------------------------------------------------
blog_path = "examples/blog/index"
blog_authors = {
    "pydata": ("PyData", "https://pydata.org"),
    "jupyter": ("Jupyter", "https://jupyter.org"),
}

# -- todo configuration --------------------------------------------------------
todo_include_todos = True

# -- favicon configuration -----------------------------------------------------
favicons = [
    {
        "rel": "apple-touch-icon",
        "size": "180x180",
        "static-file": "favicon/apple-touch-icon.png",
    },
    {
        "size": "32x32",
        "static-file": "favicon/favicon-32x32.png",
    },
    {
        "size": "16x16",
        "static-file": "favicon/favicon-16x16.png",
    },
    {
        "rel": "mask-icon",
        "static-file": "favicon/safari-pinned-tab.svg",
        "color": "#459db9",
    },
    {"rel": "shortcut icon", "static-file": "favicon/favicon.ico"},
    {"rel": "manifest", "static-file": "favicon/site.webmanifest"},
    # soon supported (0.4)
    # <link rel="manifest" href="/_static/favicon/site.webmanifest">
    # <meta name="msapplication-TileColor" content="#459db9">
    # <meta name="msapplication-config" content="/_static/favicon/browserconfig.xml">
    # <meta name="theme-color" content="#ffffff">
]


# -- Application setup ---------------------------------------------------------
def setup(app):
    app.add_directive("gallery-grid", GalleryDirective)  # Add the gallery directive
