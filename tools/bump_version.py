"""Bump the theme version and update the version switcher.

Usage:
    python tools/bump_version.py <new_version>

Updates __init__.py.

Updates switcher.json:
- stable to stable: update preferred entry to new version, create entry for the previous
- rc to stable: update preferred entry to new version, remove the rc.
- stable to rc: don't touch the preferred entry, add the rc
- rc to rc: don't touch the preferred entry, replace the old rc by the new rc.
"""

import json
import re
import sys

from pathlib import Path


ROOT = Path(__file__).parent.parent
INIT_PY = ROOT / "src/pydata_sphinx_theme/__init__.py"
SWITCHER_JSON = ROOT / "docs/_static/switcher.json"
DOCS_URL = "https://pydata-sphinx-theme.readthedocs.io"


def read_version():
    """Read the current `__version__` from `__init__.py`."""
    return re.search(r'__version__ = "(.*)"', INIT_PY.read_text()).group(1)


def write_version(new_version):
    """Overwrite `__version__` in `__init__.py` with `new_version`."""
    pattern = r'__version__ = ".*"'
    text = re.sub(pattern, f'__version__ = "{new_version}"', INIT_PY.read_text())
    INIT_PY.write_text(text)


def compute_new_entries(entries, old_version, new_version):
    """Update the switcher `entries` in place for `old_version` -> `new_version`."""
    current = next((e for e in entries if e["version"] == f"v{old_version}"), None)
    was_rc = current is not None and not current.get("preferred")

    if "rc" in new_version:
        if was_rc:
            # Another candidate for the same release: update it in place.
            current["name"] = new_version
            current["version"] = f"v{new_version}"
            current["url"] = f"{DOCS_URL}/en/v{new_version}/"
        else:
            entries.insert(
                1,
                {
                    "name": new_version,
                    "version": f"v{new_version}",
                    "url": f"{DOCS_URL}/en/v{new_version}/",
                },
            )
        return entries

    if was_rc:
        stable = next(e for e in entries if e.get("preferred"))
        stable["name"] = stable["version"].removeprefix("v")
        stable["url"] = f"{DOCS_URL}/en/{stable['version']}/"
        del stable["preferred"]
    else:
        # No release candidate preceded this release: demote it ourselves.
        entries.insert(
            entries.index(current) + 1,
            {
                "name": old_version,
                "version": f"v{old_version}",
                "url": f"{DOCS_URL}/en/v{old_version}/",
            },
        )

    current["name"] = f"{new_version} (stable)"
    current["version"] = f"v{new_version}"
    current["url"] = f"{DOCS_URL}/en/stable/"
    current["preferred"] = True
    return entries


def main(new_version):
    """Bump `__init__.py` and the switcher to `new_version`."""
    old_version = read_version()
    write_version(new_version)

    switcher = json.loads(SWITCHER_JSON.read_text())
    entries = compute_new_entries(switcher, old_version, new_version)
    SWITCHER_JSON.write_text(json.dumps(entries, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(f"usage: {sys.argv[0]} <new_version>")
    main(sys.argv[1])
