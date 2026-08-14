"""Contract test: neutral vocabulary scan across the three agent directories.

SC-001 / C-3 / C-4: every frontmatter key in agents/,
skills/create-agent/templates/ and skills/create-team/templates/agents/
must be a kebab-case member of the neutral key set; the tool-dialect
vocabulary must have zero occurrences. Files without frontmatter (composable
snippets, schema docs) carry no metadata and are vacuously compliant.
"""

import re

import pytest
from pathlib import Path

from specify_cli import (
    FORBIDDEN_AGENT_METADATA_KEYS,
    NEUTRAL_AGENT_METADATA_KEYS,
    split_agent_frontmatter,
)

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

SCAN_DIRS = [
    REPO_ROOT / "agents",
    REPO_ROOT / "skills" / "create-agent" / "templates",
    REPO_ROOT / "skills" / "create-team" / "templates" / "agents",
]


def _frontmatter_key_lines():
    for directory in SCAN_DIRS:
        for path in sorted(directory.glob("*.md")):
            fm_lines, _body = split_agent_frontmatter(path.read_text())
            for line in fm_lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    yield path, stripped


def test_scan_dirs_exist():
    for directory in SCAN_DIRS:
        assert directory.is_dir(), directory


def test_no_forbidden_dialect_key_occurrences():
    offenders = []
    for path, line in _frontmatter_key_lines():
        key = line.split(":")[0].strip()
        if key in FORBIDDEN_AGENT_METADATA_KEYS:
            offenders.append(f"{path.relative_to(REPO_ROOT)}: {key}")
    assert not offenders, "\n".join(offenders)


def test_all_keys_are_neutral_set_members():
    offenders = []
    for path, line in _frontmatter_key_lines():
        key = line.split(":")[0].strip()
        if key not in NEUTRAL_AGENT_METADATA_KEYS:
            offenders.append(f"{path.relative_to(REPO_ROOT)}: {key}")
    assert not offenders, "\n".join(offenders)


def test_all_keys_are_kebab_case():
    offenders = []
    for path, line in _frontmatter_key_lines():
        key = line.split(":")[0].strip()
        if key != key.lower() or "_" in key or not re.match(r"^[a-z][a-z0-9-]*$", key):
            offenders.append(f"{path.relative_to(REPO_ROOT)}: {key}")
    assert not offenders, "\n".join(offenders)


def test_scan_surface_is_nontrivial():
    # Pin hygiene: the scan must actually see metadata-bearing files
    # (post-relocation surface: 17 files across the three directories).
    with_metadata = [
        path
        for path, _line in _frontmatter_key_lines()
    ]
    assert len(set(with_metadata)) >= 15
