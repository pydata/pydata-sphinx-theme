"""Sphinx Bootstrap Theme package."""
import codecs
import os
import re

from setuptools import setup


# from https://packaging.python.org/guides/single-sourcing-package-version/
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="pydata-sphinx-theme",
    version=find_version("pydata_sphinx_theme", "__init__.py"),
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
