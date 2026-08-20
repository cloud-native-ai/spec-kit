"""Unit tests: dead-reference checker grammar (requirement 045 / Feature 047).

Pins contracts/sanitize-detection-rules.md §1 C-1..C-5: markdown links,
repo-prefixed paths, speckit command refs, skill refs; fenced-block and
placeholder exemptions; docs-tree lane reuse of docs-utils broken_links.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "sanitize" / "correctness"


def make_ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify" / "memory" / "todo").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "python").mkdir(parents=True, exist_ok=True)
    (tmp_path / "skills" / "create-docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "templates" / "commands").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "python" / "feedback-utils.py").write_text("#", encoding="utf-8")
    (tmp_path / "templates" / "commands" / "feedback.md").write_text("#", encoding="utf-8")
    (tmp_path / ".specify" / "memory" / "todo" / "material.md").write_text(
        FIXTURES.joinpath("material.md").read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def targets_of(findings):
    return {f["target"] for f in findings}


def test_dead_link_form_reported(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert any("material.md#" in f["target"] and "absent.md" in f["summary"]
               for f in findings), targets_of(findings)


def test_dead_repo_path_form_reported(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert any("nope-utils.py" in f["target"] or "nope-utils.py" in f["summary"] for f in findings)


def test_dead_command_form_reported(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert any("speckit.nonexistent" in f["summary"] for f in findings)


def test_dead_skill_form_reported(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert any("ghost-skill" in f["summary"] for f in findings)


def test_fenced_block_references_exempt(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert not any("also-missing.py" in f["summary"] for f in findings)


def test_placeholder_targets_exempt(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert not any("<path-to-file>" in f["summary"] or "{config_key}" in f["summary"]
                   for f in findings)


def test_valid_references_not_reported(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert not any("feedback-utils.py" in f["summary"] or "speckit.feedback" in f["summary"]
                   or "create-docs" in f["summary"] for f in findings)


def test_finding_shape_is_programmatic_repair(tmp_path):
    ws = make_ws(tmp_path)
    findings = su.check_dead_references(ws)
    assert findings
    for f in findings:
        assert f["detection"] == "programmatic"
        assert f["disposition"] == "repair"
        assert f["reversibility"] == "reversible"
        assert f["severity"] == "medium"
        assert f["state"] == "pending"
        assert f["id"] == su.stable_id(f["category"], f["target"])


def test_docs_lane_maps_broken_links(tmp_path):
    """Docs-tree dead links reuse docs-utils broken_links output (C-4)."""
    ws = make_ws(tmp_path)
    docs = ws / "docs" / "concepts"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "page.md").write_text("see [guide](./missing-guide.md)\n", encoding="utf-8")
    findings = su.check_dead_references(ws)
    assert any("docs/concepts/page.md" in f["target"] for f in findings), targets_of(findings)


def test_store_self_is_exempt_from_reference_scan(tmp_path):
    """The engine's own store dir is exempt from scanning (no recursion)."""
    ws = make_ws(tmp_path)
    store_dir = ws / ".specify" / "memory" / "sanitize"
    store_dir.mkdir(parents=True, exist_ok=True)
    (store_dir / "findings.json").write_text(
        '{"notes": "references scripts/python/never-exists.py"}', encoding="utf-8")
    findings = su.check_dead_references(ws)
    assert not any("findings.json" in f["target"] for f in findings)
