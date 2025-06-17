"""Test conf file."""

# -- Project information -----------------------------------------------------

project = "Test Self Hosted Version Control URLs"
copyright = "2020, Pydata community"
author = "Pydata community"

root_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []
html_theme = "pydata_sphinx_theme"
html_context = {
    "github_url": "https://github.pydata.org",
    "gitlab_url": "https://gitlab.pydata.org",
    "bitbucket_url": "https://bitbucket.pydata.org",
}
