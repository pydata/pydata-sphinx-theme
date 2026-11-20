"""Tests for the HTML translator setup."""


def test_table_classes(sphinx_build_factory) -> None:
    """The theme translator is used even with translators for other builders.

    The test site registers a translator for a builder we do not build with.
    The presence of that translator must not stop the theme from installing
    its translator for the HTML builder.  Regression test for
    https://github.com/pydata/pydata-sphinx-theme/issues/1418
    """
    sphinx_build = sphinx_build_factory("table").build()

    index_html = sphinx_build.html_tree("index.html")
    table = index_html.select_one("table")
    assert table is not None, "No table in the built page"
    assert "table" in table["class"]
    assert "docutils" not in table["class"]
    assert index_html.select_one("div.pst-scrollable-table-container") is not None
