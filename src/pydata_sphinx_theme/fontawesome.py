r"""Subset FontAwesome assets to only the icons used in the built docs.

Glyph sources:
1. HTML class names (fa-solid fa-bars)
2. Raw codepoints in _icons.scss (--pst-icon-*: "\fXXX")

Icons injected by JavaScript at runtime (e.g. fa-xmark for banner close buttons)
are NOT detected by the scan. They will render via webfont fallback. Document them
in _icons.scss so the woff2 subsetter keeps their glyph.
"""

import json
import re

from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

_FA_ICON_DATA = Path(__file__).parent / "fa-icon-data.json"

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


def build_css_icon_map(css: str) -> dict[str, str]:
    r"""Return {icon-name: codepoint} from the compiled FA CSS.

    FA7 stores codepoints as --fa custom properties:
        .fa-bars,.fa-navicon{--fa:"\f0c9"}
    Family is not in the icon rule — it comes from the HTML prefix class.
    """
    icon_map: dict[str, str] = {}
    for match in re.finditer(r'((?:\.[a-z][\w-]*,)*\.(fa-[\w-]+))\{[^}]*--fa:\s*"\\([0-9a-fA-F]+)"', css):
        codepoint = match.group(3)
        # capture every .fa-* class in the selector (FA lists aliases before canonical names)
        for cls in re.findall(r'\.(fa-[\w-]+)', match.group(1)):
            icon_map[cls] = codepoint
    return icon_map


def collect_html_glyphs(
    icon_map: dict[str, str], build_dir: Path
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Scan built HTML for FA class usage.

    Returns (glyphs, icon_names) where:
    - glyphs: {family: {codepoints}} for woff2 subsetting
    - icon_names: {family: {icon-names}} for JS generation
    """
    glyphs: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    icon_names: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    pattern = re.compile(
        r'class="[^"]*?(fa-(?:solid|brands|regular)|fab|fas|far)\s+(fa-[\w-]+)'
    )

    for html_file in build_dir.rglob("*.html"):
        for match in pattern.finditer(html_file.read_text(errors="ignore")):
            prefix, icon = match.group(1), match.group(2)
            if icon in icon_map:
                family = _PREFIX_TO_FAMILY[prefix]
                glyphs[family].add(icon_map[icon])
                icon_names[family].add(icon.removeprefix("fa-"))

    return glyphs, icon_names


def collect_scss_glyphs() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    r"""Extract codepoints and icon names from _icons.scss, partitioned by font family.

    Each line has an inline comment identifying the family and icon name, e.g.:
        --pst-icon-github: "\f09b"; // fa-brands fa-github
    Lines without a recognisable prefix default to solid.
    Icon names are extracted for JS generation when the comment ends with the icon
    name (e.g. "// fa-solid fa-github"). Icons whose comment has trailing text
    (e.g. "// fa-solid fa-xmark (dynamically injected by JS ...)") do not match
    the end-anchored pattern and are skipped in JS generation — they keep their
    woff2 glyph and render via webfont fallback.
    """
    glyphs: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    icon_names: dict[str, set[str]] = {family: set() for family in _FONT_FILES}
    icon_pattern = re.compile(r"fa-([\w-]+)$")
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
        glyphs[family].add(codepoint)
        icon_match = icon_pattern.search(comment.strip())
        if icon_match:
            icon_names[family].add(icon_match.group(1))
    return glyphs, icon_names


def _subset_font(src: Path, dst: Path, codepoints: set[str]) -> None:
    """Read *src*, subset to *codepoints*, write to *dst*."""
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


def collect_user_css_glyphs(build_dir: Path) -> set[str]:
    """Scan user CSS in the output for raw FA codepoints.

    Skips PST and FA vendor CSS. Family is unknown so the caller adds codepoints
    to both solid and brands.
    """
    _SKIP_CSS = {"pydata-sphinx-theme.css", "theme.css"}
    _CSS_CODEPOINT = re.compile(r'"\\([0-9a-fA-F]{4,5})"')
    codepoints: set[str] = set()
    for css_path in (build_dir / "_static").rglob("*.css"):
        if css_path.name in _SKIP_CSS or "fontawesome" in css_path.parts:
            continue
        for match in _CSS_CODEPOINT.finditer(
            css_path.read_text(encoding="utf-8", errors="ignore")
        ):
            codepoints.add(match.group(1))
    return codepoints


def generate_user_icons_js(icon_names: dict[str, set[str]], out_dir: Path) -> None:
    """Write fontawesome-user-icons.js with library.add() for all scanned icons.

    Icons not found in fa-icon-data.json (FA Pro, custom) are silently skipped;
    they render via webfont fallback.
    """
    if not _FA_ICON_DATA.exists():
        return

    fa_data = json.loads(_FA_ICON_DATA.read_text(encoding="utf-8"))
    prefix_map = {"solid": "fas", "brands": "fab"}

    entries = []
    for family, names in icon_names.items():
        family_data = fa_data.get(family, {})
        prefix = prefix_map[family]
        for name in sorted(names):
            icon = family_data.get(name)
            if icon:
                entries.append(
                    f'  {{prefix:"{prefix}",iconName:"{name}",icon:{json.dumps(icon)}}}'
                )

    if not entries:
        return

    js = (
        "// auto-generated by pydata-sphinx-theme — do not edit\n"
        "(function(){\n"
        "  var FA=window.FontAwesome;if(!FA)return;\n"
        "  FA.library.add(\n"
        + ",\n".join(entries)
        + "\n  );\n"
        "  FA.dom.i2svg();\n"
        "})();\n"
    )

    scripts_dir = out_dir / "_static" / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "fontawesome-user-icons.js").write_text(js, encoding="utf-8")
    print(f"  fontawesome-user-icons.js: {len(entries)} icons")


def subset_all(build_dir: Path) -> None:
    """Subset all FA woff2 fonts in *build_dir* to glyphs actually used,
    and generate fontawesome-user-icons.js for SVG rendering."""
    fonts_dir = build_dir / "_static" / "vendor" / "fontawesome" / "webfonts"
    css_file = build_dir / "_static" / "styles" / "pydata-sphinx-theme.css"

    if not css_file.exists():
        return

    css = css_file.read_text(encoding="utf-8")
    icon_map = build_css_icon_map(css)
    glyphs, icon_names = collect_html_glyphs(icon_map, build_dir)
    scss_glyphs, scss_names = collect_scss_glyphs()
    for family in _FONT_FILES:
        glyphs[family] |= scss_glyphs[family]
        icon_names[family] |= scss_names[family]
    for codepoint in collect_user_css_glyphs(build_dir):
        glyphs["solid"].add(codepoint)
        glyphs["brands"].add(codepoint)

    print("Subsetting FontAwesome fonts...")
    for family, filename in _FONT_FILES.items():
        _subset_font(_PKG_FONTS / filename, fonts_dir / filename, glyphs[family])

    generate_user_icons_js(icon_names, build_dir)
