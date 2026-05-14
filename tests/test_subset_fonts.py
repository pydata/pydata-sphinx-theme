"""Tests for docs/scripts/subset_fonts.py."""

from docs.scripts.subset_fonts import (
    build_css_icon_map,
    collect_html_glyphs,
    collect_scss_glyphs,
    subset_font,
)


SAMPLE_CSS = """
.fa-bars,.fa-navicon{--fa:"\\f0c9"}
.fa-github{--fa:"\\f09b"}
.fa-moon{--fa:"\\f186"}
"""


def test_build_css_icon_map_finds_icons():
    """Codepoints are extracted for all icon names in the CSS."""
    icon_map = build_css_icon_map(SAMPLE_CSS)
    assert icon_map["fa-bars"] == "f0c9"
    assert icon_map["fa-github"] == "f09b"
    assert icon_map["fa-moon"] == "f186"


def test_collect_html_glyphs_finds_classes(tmp_path):
    """Icons in HTML are mapped to the correct font family."""
    (tmp_path / "page.html").write_text(
        '<i class="fa-solid fa-bars"></i><i class="fa-brands fa-github"></i>'
    )
    icon_map = {"fa-bars": "f0c9", "fa-github": "f09b"}
    glyphs = collect_html_glyphs(icon_map, tmp_path)
    assert "f0c9" in glyphs["solid"]
    assert "f09b" in glyphs["brands"]


def test_collect_html_glyphs_ignores_unknown_icons(tmp_path):
    """Icons not present in the CSS map produce no codepoints."""
    (tmp_path / "page.html").write_text('<i class="fa-solid fa-does-not-exist"></i>')
    glyphs = collect_html_glyphs({}, tmp_path)
    assert all(len(v) == 0 for v in glyphs.values())


def test_collect_scss_glyphs_partitions_by_family():
    """SCSS codepoints are split into solid vs brands based on inline comments."""
    glyphs = collect_scss_glyphs()
    # solid: external-link arrow is a known fixture
    assert "f35d" in glyphs["solid"]
    # brands: github and gitlab icons are defined with fa-brands comments
    assert "f09b" in glyphs["brands"]
    assert "f296" in glyphs["brands"]


def test_subset_font_skips_missing_file(tmp_path):
    """No exception is raised when the font file does not exist."""
    subset_font(tmp_path / "nonexistent.woff2", {"f0c9"})


def test_subset_font_skips_empty_codepoints(tmp_path):
    """Font file is left untouched when the codepoint set is empty."""
    font = tmp_path / "fa-solid-900.woff2"
    font.write_bytes(b"fake")
    subset_font(font, set())
    # file must be untouched
    assert font.read_bytes() == b"fake"
