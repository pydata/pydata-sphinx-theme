"""Sphinx Bootstrap Theme package."""
from setuptools import setup


setup(
    name="pydata-sphinx-theme",
    version="0.0.1.dev0",
    description="Sphinx Bootstrap Theme - pydata version.",
    url="https://github.com/pandas-dev/pydata-sphinx-theme",
    #
    packages=["pydata_sphinx_theme"],
    package_data={
        "pydata_sphinx_theme": [
            "theme.conf",
            "*.html",
            "static/css/*.css",
            "static/js/*.js",
            "static/img/*",
        ]
    },
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={"sphinx.html_themes": ["pydata_sphinx_theme = pydata_sphinx_theme"]},
    install_requires=["sphinx"],
)
