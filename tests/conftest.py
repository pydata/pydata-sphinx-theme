pytest_plugins = [
    "sphinx.testing.fixtures",
    # paired with `pytest -p "no:hypothesispytest"`, ensures accurate coverage
    "hypothesis.extra.pytestplugin",
]
