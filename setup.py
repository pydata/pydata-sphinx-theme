"""Sphinx Bootstrap Theme package."""
import codecs
import os
import re

from setuptools import setup


# from https://packaging.python.org/guides/single-sourcing-package-version/
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

tests_require = [
    line.strip()
    for line in read("docs", "requirements.txt").splitlines()
    if not line.strip().startswith("#")
]

setup(
    name="pydata-sphinx-theme",
    version=find_version("pydata_sphinx_theme", "__init__.py"),
    description="Bootstrap-based Sphinx theme from the PyData community",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydata/pydata-sphinx-theme",
    license="BSD",
    maintainer="Joris Van den Bossche",
    maintainer_email="jorisvandenbossche@gmail.com",
    #
    packages=["pydata_sphinx_theme"],
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={"sphinx.html_themes": ["pydata_sphinx_theme = pydata_sphinx_theme"]},
    install_requires=["sphinx", "beautifulsoup4", "docutils!=0.17.0"],
    extras_require={
        "test": tests_require,
        "coverage": ["pytest-cov", "codecov", *tests_require],
    },
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Theme",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
