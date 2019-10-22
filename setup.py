"""Sphinx Bootstrap Theme package."""
from setuptools import setup


setup(
    name="pandas-sphinx-theme",
    version="0.0.1.dev0",
    description="Sphinx Bootstrap Theme - pandas version.",
    url="https://github.com/pandas-dev/pandas-sphinx-theme",
    #
    packages=["pandas_sphinx_theme"],
    package_data={
        "pandas_sphinx_theme": [
            "theme.conf",
            "*.html",
            "static/sphinx-bootstrap.css_t",
            "static/css/*.css",
            "static/js/*.js",
            "static/img/*",
        ]
    },
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={"sphinx.html_themes": ["pandas_sphinx_theme = pandas_sphinx_theme"]},
    install_requires=["sphinx"],
)
