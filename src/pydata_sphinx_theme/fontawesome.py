r"""Subset FontAwesome woff2 files to only the glyphs used in the built docs.

Glyph sources:
1. HTML class names (fa-solid fa-bars)
2. Raw codepoints in _icons.scss (--pst-icon-*: "\fXXX")
"""

import re

from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont


_ICONS_SCSS = Path(__file__).parent / "assets" / "styles" / "variables" / "_icons.scss"
_PKG_FONTS = (
    Path(__file__).parent
    / "theme"
    / "pydata_sphinx_theme"
    / "static"
    / "vendor"
    / "fontawesome"
    / "webfonts"
)

_FONT_FILES = {
    "solid": "fa-solid-900.woff2",
    "brands": "fa-brands-400.woff2",
}

_PREFIX_TO_FAMILY = {
    "fa-solid": "solid",
    "fa-brands": "brands",
    "fas": "solid",
    "fab": "brands",
}


_FA_RULE = re.compile(
    r"([^{}]+)"  # selectors before the opening brace
    r"\{"  # opening brace
    r'[^}]*--fa:\s*"\\'  # --fa: property prefix
    r"([0-9a-fA-F]+)"  # codepoint
    r'"'  # closing quote
    r"[^}]*\}"  # rest of the block
)
_FA_CLASS = re.compile(r"fa-[\w-]+")


def build_css_icon_map(css: str) -> dict[str, str]:
    r"""Return {icon-name: codepoint} from the compiled FA CSS.

    FA7 stores codepoints as --fa custom properties:
        .fa-bars,.fa-navicon{--fa:"\f0c9"}
    Family is not in the icon rule — it comes from the HTML prefix class.
    """
    icon_map: dict[str, str] = {}
    for rule in _FA_RULE.finditer(css):
        selectors, codepoint = rule.group(1), rule.group(2)
        for name in _FA_CLASS.finditer(selectors):
            icon_map[name.group()] = codepoint
    return icon_map


def collect_html_glyphs(
    icon_map: dict[str, str], build_dir: Path
) -> dict[str, set[str]]:
    """Scan built HTML for FA class usage, return {family: {codepoints}}."""
    used: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    pattern = re.compile(
        r'class="[^"]*?(fa-(?:solid|brands|regular)|fab|fas|far)\s+(fa-[\w-]+)'
    )

    for html_file in build_dir.rglob("*.html"):
        for match in pattern.finditer(html_file.read_text(errors="ignore")):
            prefix, icon = match.group(1), match.group(2)
            if icon in icon_map:
                used[_PREFIX_TO_FAMILY[prefix]].add(icon_map[icon])

    return used


def collect_scss_glyphs() -> dict[str, set[str]]:
    r"""Extract codepoints from _icons.scss, partitioned by font family.

    Each line has an inline comment identifying the family, e.g.:
        --pst-icon-github: "\f09b"; // fa-brands fa-github
    Lines without a recognisable prefix default to solid.
    """
    result: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    for line in _ICONS_SCSS.read_text(encoding="utf-8").splitlines():
        match = re.search(r'"\\([0-9a-fA-F]+)"', line)
        if not match:
            continue
        codepoint = match.group(1)
        comment = line.split("//", 1)[1] if "//" in line else ""
        family = next(
            (fam for prefix, fam in _PREFIX_TO_FAMILY.items() if prefix in comment),
            "solid",
        )
        result[family].add(codepoint)
    return result


def _subset_font(src: Path, dst: Path, codepoints: set[str]) -> None:
    """Subset *src* to *codepoints* and write the result to *dst*."""
    if not codepoints or not src.exists():
        return
    before = src.stat().st_size
    font = TTFont(str(src))
    options = Options(flavor="woff2")
    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=[int(cp, 16) for cp in codepoints])
    subsetter.subset(font)
    font.save(str(dst))
    after = dst.stat().st_size
    kept = len(codepoints)
    saved = f"{before / 1024:.1f} KB → {after / 1024:.1f} KB ({kept} glyphs)"
    print(f"  {dst.name}: {saved}")


def subset_font(font_path: Path, codepoints: set[str]) -> None:
    """Subset a woff2 font file in-place to only the given codepoints."""
    _subset_font(font_path, font_path, codepoints)


_CSS_CODEPOINT = re.compile(r'"\\([0-9a-fA-F]{4,5})"')
_SKIP_CSS = {"pydata-sphinx-theme.css", "theme.css"}


def collect_user_css_glyphs(build_dir: Path) -> set[str]:
    """Scan user CSS in the output for raw FA codepoints.

    Skips PST and FA vendor CSS. Family is unknown so the caller adds codepoints
    to both solid and brands.
    """
    codepoints: set[str] = set()
    for css_path in (build_dir / "_static").rglob("*.css"):
        if css_path.name in _SKIP_CSS or "fontawesome" in css_path.parts:
            continue
        for match in _CSS_CODEPOINT.finditer(
            css_path.read_text(encoding="utf-8", errors="ignore")
        ):
            codepoints.add(match.group(1))
    return codepoints


def subset_all(build_dir: Path) -> None:
    """Subset all FA woff2 fonts in *build_dir* to glyphs actually used."""
    fonts_dir = build_dir / "_static" / "vendor" / "fontawesome" / "webfonts"
    css_file = build_dir / "_static" / "styles" / "pydata-sphinx-theme.css"

    if not css_file.exists():
        return

    css = css_file.read_text(encoding="utf-8")
    icon_map = build_css_icon_map(css)
    glyphs = collect_html_glyphs(icon_map, build_dir)
    for family, codepoints in collect_scss_glyphs().items():
        glyphs[family] |= codepoints
    for codepoint in collect_user_css_glyphs(build_dir):
        glyphs["solid"].add(codepoint)
        glyphs["brands"].add(codepoint)

    print("Subsetting FontAwesome fonts...")
    for family, filename in _FONT_FILES.items():
        _subset_font(_PKG_FONTS / filename, fonts_dir / filename, glyphs[family])
