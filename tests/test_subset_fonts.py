"""Tests for docs/scripts/subset_fonts.py."""

from pydata_sphinx_theme.fontawesome import (
    build_css_icon_map,
    collect_html_glyphs,
    collect_scss_glyphs,
    collect_user_css_glyphs,
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


def test_collect_html_glyphs_finds_short_prefix_classes(tmp_path):
    """sphinx-design short prefixes (fab, fas) are mapped to the correct family."""
    (tmp_path / "page.html").write_text(
        '<span class="fab fa-github"></span><span class="fas fa-bars"></span>'
    )
    icon_map = {"fa-github": "f09b", "fa-bars": "f0c9"}
    glyphs = collect_html_glyphs(icon_map, tmp_path)
    assert "f09b" in glyphs["brands"]
    assert "f0c9" in glyphs["solid"]


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


def test_collect_user_css_glyphs_finds_codepoints(tmp_path):
    """Codepoints in user CSS are returned, PST and vendor CSS are skipped."""
    static = tmp_path / "_static"
    (static / "styles").mkdir(parents=True)
    (static / "vendor" / "fontawesome").mkdir(parents=True)

    # user CSS
    (static / "custom.css").write_text('html { --my-icon: "\\f999"; }')
    # our CSS
    (static / "styles" / "pydata-sphinx-theme.css").write_text(
        'html { --pst: "\\faaa"; }'
    )
    # vendor FA CSS
    (static / "vendor" / "fontawesome" / "all.css").write_text('.x { --fa: "\\fbbb"; }')

    codepoints = collect_user_css_glyphs(tmp_path)
    assert "f999" in codepoints
    assert "faaa" not in codepoints
    assert "fbbb" not in codepoints


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
