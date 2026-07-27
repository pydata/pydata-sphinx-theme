"""Tests for tools/bump_version.py."""

import importlib.util

from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "bump_version", Path(__file__).parents[1] / "tools" / "bump_version.py"
)
bump_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bump_version)

DEV = {"version": "dev", "url": f"{bump_version.DOCS_URL}/en/latest/"}


def stable_entry(version):
    """Build the switcher entry for the current stable `version`."""
    return {
        "name": f"{version} (stable)",
        "version": f"v{version}",
        "url": f"{bump_version.DOCS_URL}/en/stable/",
        "preferred": True,
    }


def archived_entry(version):
    """Build the switcher entry for a past, non-stable `version`."""
    return {
        "name": version,
        "version": f"v{version}",
        "url": f"{bump_version.DOCS_URL}/en/v{version}/",
    }


def test_bump_to_rc_inserts_a_new_entry():
    """A release candidate bump inserts a new entry, keeping stable in place."""
    entries = [DEV, stable_entry("0.18.0")]

    entries = bump_version.compute_new_entries(entries, "0.18.0", "0.19.0rc0")

    assert entries == [
        DEV,
        {
            "name": "0.19.0rc0",
            "version": "v0.19.0rc0",
            "url": f"{bump_version.DOCS_URL}/en/v0.19.0rc0/",
        },
        stable_entry("0.18.0"),
    ]


def test_bump_rc_to_rc_updates_in_place():
    """A new candidate for the same release updates the rc entry in place."""
    entries = [DEV, archived_entry("0.19.0rc0"), stable_entry("0.18.0")]

    entries = bump_version.compute_new_entries(entries, "0.19.0rc0", "0.19.0rc1")

    assert entries == [DEV, archived_entry("0.19.0rc1"), stable_entry("0.18.0")]


def test_bump_from_rc_to_final_promotes_and_demotes():
    """A final release promotes its rc entry and demotes the old stable."""
    entries = [DEV, archived_entry("0.19.0rc0"), stable_entry("0.18.0")]

    entries = bump_version.compute_new_entries(entries, "0.19.0rc0", "0.19.0")

    assert entries == [DEV, stable_entry("0.19.0"), archived_entry("0.18.0")]


def test_bump_without_a_preceding_rc_demotes_current_stable():
    """With no rc entry to promote, the current stable itself is demoted."""
    entries = [DEV, stable_entry("0.18.0")]

    entries = bump_version.compute_new_entries(entries, "0.18.0", "0.18.1")

    assert entries == [DEV, stable_entry("0.18.1"), archived_entry("0.18.0")]
