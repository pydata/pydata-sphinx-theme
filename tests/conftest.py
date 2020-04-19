import pathlib
import shutil

import pytest


pytest_plugins = "sphinx.testing.fixtures"


srcdir = pathlib.Path(__file__).absolute().parent / "examples"


@pytest.fixture(autouse=True, scope="function")
def remove_sphinx_build_output():
    """
    Remove _build/ folders, if exist.
    Inspired by https://github.com/readthedocs/sphinx-hoverxref/
    """
    for path in srcdir.iterdir():
        build_dir = path / "_build"
        if build_dir.exists():
            shutil.rmtree(build_dir)
