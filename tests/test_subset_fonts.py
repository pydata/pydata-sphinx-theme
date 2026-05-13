"""Tests for pydata_sphinx_theme.fontawesome."""

import json

from pydata_sphinx_theme.fontawesome import (
    build_css_icon_map,
    collect_html_glyphs,
    collect_scss_glyphs,
    collect_user_css_glyphs,
    generate_user_icons_js,
    subset_font,
)


SAMPLE_CSS = """
.fa-bars,.fa-navicon{--fa:"\\f0c9"}
.fa-github{--fa:"\\f09b"}
.fa-moon{--fa:"\\f186"}
"""


# ---------------------------------------------------------------------------
# build_css_icon_map
# ---------------------------------------------------------------------------


def test_build_css_icon_map_finds_icons():
    icon_map = build_css_icon_map(SAMPLE_CSS)
    assert icon_map["fa-bars"] == "f0c9"
    assert icon_map["fa-github"] == "f09b"
    assert icon_map["fa-moon"] == "f186"


# ---------------------------------------------------------------------------
# collect_html_glyphs
# ---------------------------------------------------------------------------


def test_collect_html_glyphs_returns_codepoints_and_names(tmp_path):
    (tmp_path / "page.html").write_text(
        '<i class="fa-solid fa-bars"></i><i class="fa-brands fa-github"></i>'
    )
    icon_map = {"fa-bars": "f0c9", "fa-github": "f09b"}
    glyphs, names = collect_html_glyphs(icon_map, tmp_path)
    assert "f0c9" in glyphs["solid"]
    assert "f09b" in glyphs["brands"]
    assert "bars" in names["solid"]
    assert "github" in names["brands"]


def test_collect_html_glyphs_finds_short_prefix_classes(tmp_path):
    (tmp_path / "page.html").write_text(
        '<span class="fab fa-github"></span><span class="fas fa-bars"></span>'
    )
    icon_map = {"fa-github": "f09b", "fa-bars": "f0c9"}
    glyphs, names = collect_html_glyphs(icon_map, tmp_path)
    assert "f09b" in glyphs["brands"]
    assert "f0c9" in glyphs["solid"]
    assert "github" in names["brands"]
    assert "bars" in names["solid"]


def test_collect_html_glyphs_ignores_unknown_icons(tmp_path):
    (tmp_path / "page.html").write_text('<i class="fa-solid fa-does-not-exist"></i>')
    glyphs, names = collect_html_glyphs({}, tmp_path)
    assert all(len(v) == 0 for v in glyphs.values())
    assert all(len(v) == 0 for v in names.values())


# ---------------------------------------------------------------------------
# collect_scss_glyphs
# ---------------------------------------------------------------------------


def test_collect_scss_glyphs_partitions_by_family():
    glyphs, names = collect_scss_glyphs()
    assert "f35d" in glyphs["solid"]
    assert "f09b" in glyphs["brands"]
    assert "f296" in glyphs["brands"]


def test_collect_scss_glyphs_returns_icon_names():
    _, names = collect_scss_glyphs()
    assert "github" in names["brands"]
    assert "gitlab" in names["brands"]


# ---------------------------------------------------------------------------
# collect_user_css_glyphs
# ---------------------------------------------------------------------------


def test_collect_user_css_glyphs_finds_codepoints(tmp_path):
    static = tmp_path / "_static"
    (static / "styles").mkdir(parents=True)
    (static / "vendor" / "fontawesome").mkdir(parents=True)

    (static / "custom.css").write_text('html { --my-icon: "\\f999"; }')
    (static / "styles" / "pydata-sphinx-theme.css").write_text(
        'html { --pst: "\\faaa"; }'
    )
    (static / "vendor" / "fontawesome" / "all.css").write_text('.x { --fa: "\\fbbb"; }')

    codepoints = collect_user_css_glyphs(tmp_path)
    assert "f999" in codepoints
    assert "faaa" not in codepoints
    assert "fbbb" not in codepoints


# ---------------------------------------------------------------------------
# generate_user_icons_js
# ---------------------------------------------------------------------------


def test_generate_user_icons_js_creates_file(tmp_path, monkeypatch):
    from pydata_sphinx_theme import fontawesome as fa_mod

    icon_data = {
        "solid": {"bars": [448, 512, ["navicon"], "f0c9", "M0 0z"]},
        "brands": {"github": [496, 512, [], "f09b", "M0 0z"]},
    }
    monkeypatch.setattr(fa_mod, "_FA_ICON_DATA", tmp_path / "fa-icon-data.json")
    (tmp_path / "fa-icon-data.json").write_text(json.dumps(icon_data), encoding="utf-8")

    generate_user_icons_js({"solid": {"bars"}, "brands": {"github"}}, tmp_path)

    out = (tmp_path / "_static" / "scripts" / "fontawesome-user-icons.js").read_text()
    assert 'iconName:"bars"' in out
    assert 'iconName:"github"' in out
    assert 'prefix:"fas"' in out
    assert 'prefix:"fab"' in out
    assert "FA.dom.i2svg()" in out


def test_generate_user_icons_js_skips_unknown_icons(tmp_path, monkeypatch):
    """Icons not in fa-icon-data.json are silently omitted."""
    from pydata_sphinx_theme import fontawesome as fa_mod

    icon_data = {"solid": {}, "brands": {}}
    monkeypatch.setattr(fa_mod, "_FA_ICON_DATA", tmp_path / "fa-icon-data.json")
    (tmp_path / "fa-icon-data.json").write_text(json.dumps(icon_data), encoding="utf-8")

    generate_user_icons_js({"solid": {"fa-pro-icon"}, "brands": set()}, tmp_path)
    assert not (tmp_path / "_static" / "scripts" / "fontawesome-user-icons.js").exists()


def test_generate_user_icons_js_missing_data_file(tmp_path, monkeypatch):
    """No exception when fa-icon-data.json is absent."""
    from pydata_sphinx_theme import fontawesome as fa_mod

    monkeypatch.setattr(fa_mod, "_FA_ICON_DATA", tmp_path / "nonexistent.json")
    generate_user_icons_js({"solid": {"bars"}, "brands": set()}, tmp_path)


# ---------------------------------------------------------------------------
# subset_font
# ---------------------------------------------------------------------------


def test_subset_font_skips_missing_file(tmp_path):
    subset_font(tmp_path / "nonexistent.woff2", {"f0c9"})


def test_subset_font_skips_empty_codepoints(tmp_path):
    font = tmp_path / "fa-solid-900.woff2"
    font.write_bytes(b"fake")
    subset_font(font, set())
    assert font.read_bytes() == b"fake"


# ---------------------------------------------------------------------------
# Integration: subset_all writes both woff2 and user-icons JS
# ---------------------------------------------------------------------------


def test_subset_all_generates_user_icons_js(tmp_path, monkeypatch):
    """subset_all() produces fontawesome-user-icons.js alongside subsetted fonts."""
    from pydata_sphinx_theme import fontawesome as fa_mod
    from pydata_sphinx_theme.fontawesome import subset_all

    static = tmp_path / "_static"
    (static / "styles").mkdir(parents=True)
    (static / "scripts").mkdir(parents=True)
    (static / "vendor" / "fontawesome" / "webfonts").mkdir(parents=True)

    (static / "styles" / "pydata-sphinx-theme.css").write_text(
        '.fa-bars,.fa-navicon{--fa:"\\f0c9"}'
    )
    (tmp_path / "index.html").write_text('<i class="fa-solid fa-bars"></i>')

    monkeypatch.setattr(fa_mod, "_PKG_FONTS", static / "vendor" / "fontawesome" / "webfonts")

    icon_data = {"solid": {"bars": [448, 512, ["navicon"], "f0c9", "M0 0z"]}, "brands": {}}
    monkeypatch.setattr(fa_mod, "_FA_ICON_DATA", tmp_path / "fa-icon-data.json")
    (tmp_path / "fa-icon-data.json").write_text(json.dumps(icon_data), encoding="utf-8")

    subset_all(tmp_path)

    out = (static / "scripts" / "fontawesome-user-icons.js").read_text()
    assert 'iconName:"bars"' in out


def test_subset_all_skips_when_no_css(tmp_path):
    """subset_all() is a no-op when pydata-sphinx-theme.css is absent."""
    from pydata_sphinx_theme.fontawesome import subset_all

    subset_all(tmp_path)  # must not raise
