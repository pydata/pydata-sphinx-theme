"""Subset FontAwesome woff2 files to only the glyphs used in the built docs.
Avoids loading a >1MB fontawesome font every time.

Glyph sources:
1. HTML class names (fa-solid fa-bars) → codepoint from compiled CSS --fa var
2. Raw codepoints in _icons.scss (--pst-icon-*: "\\fXXX") → family from inline comment
"""

import re
import sys

from pathlib import Path

from fontTools.subset import main as pyftsubset


BUILD_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/_build/html")
FONTS_DIR = BUILD_DIR / "_static/vendor/fontawesome/webfonts"
CSS_FILE = BUILD_DIR / "_static/styles/pydata-sphinx-theme.css"
ICONS_SCSS = (
    Path(__file__).parents[2]
    / "src/pydata_sphinx_theme/assets/styles/variables/_icons.scss"
)

FONT_FILES = {
    "solid": FONTS_DIR / "fa-solid-900.woff2",
    "brands": FONTS_DIR / "fa-brands-400.woff2",
    "regular": FONTS_DIR / "fa-regular-400.woff2",
}

PREFIX_TO_FAMILY = {"fa-solid": "solid", "fa-brands": "brands", "fa-regular": "regular"}


def build_css_icon_map(css: str) -> dict[str, str]:
    """Return {icon-name: codepoint} from the compiled FA CSS.

    FA7 stores codepoints as --fa custom properties:
        .fa-bars,.fa-navicon{--fa:"\\f0c9"}
    Family is not in the icon rule — it comes from the HTML prefix class.
    """
    icon_map: dict[str, str] = {}
    for match in re.finditer(r'\.(fa-[\w-]+)[,{][^}]*--fa:\s*"\\([0-9a-fA-F]+)"', css):
        icon_map[match.group(1)] = match.group(2)
    return icon_map


def collect_html_glyphs(
    icon_map: dict[str, str], build_dir: Path = BUILD_DIR
) -> dict[str, set[str]]:
    """Scan built HTML for FA class usage, return {family: {codepoints}}."""
    used: dict[str, set[str]] = {family: set() for family in FONT_FILES}
    pattern = re.compile(r'class="[^"]*?(fa-(?:solid|brands|regular))\s+(fa-[\w-]+)')

    for html_file in build_dir.rglob("*.html"):
        for match in pattern.finditer(html_file.read_text(errors="ignore")):
            prefix, icon = match.group(1), match.group(2)
            if icon in icon_map:
                used[PREFIX_TO_FAMILY[prefix]].add(icon_map[icon])

    return used


def collect_scss_glyphs() -> dict[str, set[str]]:
    """Extract codepoints from _icons.scss, partitioned by font family.

    Each line has an inline comment identifying the family, e.g.:
        --pst-icon-github: "\\f09b"; // fa-brands fa-github
    Lines without a recognisable prefix default to solid.
    """
    result: dict[str, set[str]] = {family: set() for family in FONT_FILES}
    for line in ICONS_SCSS.read_text().splitlines():
        match = re.search(r'"\\([0-9a-fA-F]+)"', line)
        if not match:
            continue
        codepoint = match.group(1)
        comment = line.split("//", 1)[1] if "//" in line else ""
        family = next(
            (fam for prefix, fam in PREFIX_TO_FAMILY.items() if prefix in comment),
            "solid",
        )
        result[family].add(codepoint)
    return result


def subset_font(font_path: Path, codepoints: set[str]) -> None:
    if not codepoints or not font_path.exists():
        return
    unicodes = ",".join(f"U+{cp.upper()}" for cp in codepoints)
    before = font_path.stat().st_size
    pyftsubset(
        [
            str(font_path),
            f"--unicodes={unicodes}",
            "--flavor=woff2",
            f"--output-file={font_path}",
        ]
    )
    after = font_path.stat().st_size
    print(
        f"  {font_path.name}: {before / 1024:.1f} KB → {after / 1024:.1f} KB ({len(codepoints)} glyphs)"
    )


if __name__ == "__main__":
    css = CSS_FILE.read_text()
    icon_map = build_css_icon_map(css)
    glyphs = collect_html_glyphs(icon_map)
    for family, codepoints in collect_scss_glyphs().items():
        glyphs[family] |= codepoints

    print("Subsetting FontAwesome fonts...")
    for family, codepoints in glyphs.items():
        subset_font(FONT_FILES[family], codepoints)
