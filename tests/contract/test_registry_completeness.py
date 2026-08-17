"""Contract test: instructions registries are gone; features count stays pinned.

F5 remediation originally pinned the AGENTS/SKILLS/TOOLS registry tables to
their filesystem sources. Since 2026-08-17 no registration tables exist —
skills and tools are discovered via their directories (`.specify/skills/`,
`.specify/memory/tools/`; see `.specify/skills.md` / `.specify/tools.md`) — so
c1/c2 became a regression guard that the legacy markers never come back. The
features header-count pin (c3) is registry-independent and stays.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE = REPO_ROOT / ".specify" / "instructions.md"

LEGACY_MARKERS = ("AGENTS_REGISTRY", "SKILLS_REGISTRY", "TOOLS_REGISTRY")


@pytest.mark.contract
def test_c1_no_legacy_registry_markers_in_template_or_live():
    for name, path in (("template", TEMPLATE), ("live", LIVE)):
        text = path.read_text(encoding="utf-8")
        for marker in LEGACY_MARKERS:
            assert marker not in text, f"legacy {marker} marker re-introduced in {name} instructions"
        assert "## Resource Registry" not in text, \
            f"legacy Resource Registry section re-introduced in {name} instructions"
    template = TEMPLATE.read_text(encoding="utf-8")
    assert "## Skills & Tools" in template, "template must carry the Skills & Tools pointer section"
    assert ".specify/skills.md" in template and ".specify/tools.md" in template, \
        "Skills & Tools section must point at the explanation docs"


@pytest.mark.contract
def test_c2_discovery_docs_exist():
    """Directory discovery replaces registries; the two explanation docs must ship."""
    for rel in (".specify/skills.md", ".specify/tools.md"):
        assert (REPO_ROOT / rel).is_file(), f"missing discovery explanation doc: {rel}"
    for rel in ("templates/skills.md", "templates/tools.md"):
        assert (REPO_ROOT / rel).is_file(), f"missing canonical source: {rel}"


@pytest.mark.contract
def test_c3_features_header_count_matches_rows():
    text = (REPO_ROOT / ".specify/memory/features.md").read_text(encoding="utf-8")
    m = re.search(r"\*?\*?Total Features\*?\*?:\s*(\d+)", text)
    assert m, "features.md header lacks Total Features count"
    rows = len(re.findall(r"^\| \d{3} \|", text, re.M))
    assert int(m.group(1)) == rows, \
        f"header says {m.group(1)} but {rows} feature rows exist"
