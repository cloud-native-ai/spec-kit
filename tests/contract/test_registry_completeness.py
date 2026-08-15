"""Contract test: instructions.md registry completeness (F5 remediation).

The live instructions file's managed registries drifted from reality
(skills 11 rows vs 31 installed; tools 5 vs 7 records; features header 42
vs 44 rows). These guards pin registries to their filesystem sources of
truth so drift fails CI instead of accumulating.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"


def _registry_rows(marker: str) -> list[str]:
    text = INSTRUCTIONS.read_text(encoding="utf-8")
    m = re.search(
        rf"<!-- {marker}_START -->(.*?)<!-- {marker}_END -->", text, re.S)
    assert m, f"registry block {marker} missing"
    return [l for l in m.group(1).splitlines()
            if l.startswith("| ") and "---" not in l.split("|")[1]]


@pytest.mark.contract
def test_c1_skills_registry_covers_installed_skills():
    installed = {d.name for d in (REPO_ROOT / "skills").iterdir()
                 if (d / "SKILL.md").is_file()}
    listed = {row.split("|")[1].strip() for row in _registry_rows("SKILLS_REGISTRY")}
    missing = installed - listed
    assert not missing, f"skills installed but not in registry: {sorted(missing)}"


@pytest.mark.contract
def test_c2_tools_registry_covers_tool_records():
    records = {p.stem for p in (REPO_ROOT / ".specify/memory/tools").glob("*.md")}
    listed = {row.split("|")[1].strip() for row in _registry_rows("TOOLS_REGISTRY")}
    missing = records - listed
    assert not missing, f"tool records not in registry: {sorted(missing)}"


@pytest.mark.contract
def test_c3_features_header_count_matches_rows():
    text = (REPO_ROOT / ".specify/memory/features.md").read_text(encoding="utf-8")
    m = re.search(r"\*?\*?Total Features\*?\*?:\s*(\d+)", text)
    assert m, "features.md header lacks Total Features count"
    rows = len(re.findall(r"^\| \d{3} \|", text, re.M))
    assert int(m.group(1)) == rows, \
        f"header says {m.group(1)} but {rows} feature rows exist"
