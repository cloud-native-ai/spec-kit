"""Unit tests: mirror-drift checker (requirement 045 / Feature 047).

Pins contracts/sanitize-detection-rules.md §4 C-11..C-13: sync-mirrors
--check output parsing, orphan-directory detection, and the
obsolete-asset-registry cross-check (unregistered rename residue = high).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402


# --- sync-mirrors output parsing (C-11) -----------------------------------------------

def test_parse_miss_diff_orphan_lines():
    text = (
        "ok    shared/ == .specify/shared/ (31 files)\n"
        "MISS  .specify/scripts/python/foo.py\n"
        "DIFF  .specify/skills/bar/SKILL.md\n"
        "ORPHAN .specify/scripts/python/legacy.py (no canonical scripts/ source)\n"
        "note  extra file only in mirror: .specify/templates/zzz.md\n"
        "sync  scripts/ -> .specify/scripts/ (5 files)\n"
    )
    items = su.parse_mirror_drift_lines(text)
    assert (".specify/scripts/python/foo.py", "MISS") in items
    assert (".specify/skills/bar/SKILL.md", "DIFF") in items
    assert (".specify/scripts/python/legacy.py", "ORPHAN") in items
    assert len(items) == 3


def test_parse_clean_output_yields_nothing():
    assert su.parse_mirror_drift_lines("ok    shared/ == .specify/shared/ (31 files)\n") == []


# --- orphan directory detection (C-12) --------------------------------------------------

def make_mirror_ws(tmp_path: Path, skills_dirs, source_dirs, registry=("registered-skill",)):
    mirror = tmp_path / ".specify" / "skills"
    mirror.mkdir(parents=True, exist_ok=True)
    for d in skills_dirs:
        (mirror / d).mkdir(exist_ok=True)
        (mirror / d / "SKILL.md").write_text("#\n", encoding="utf-8")
    src = tmp_path / "skills"
    src.mkdir(exist_ok=True)
    for d in source_dirs:
        (src / d).mkdir(exist_ok=True)
        (src / d / "SKILL.md").write_text("#\n", encoding="utf-8")
    return tmp_path, set(registry)


def test_orphan_mirror_dir_detected(tmp_path):
    ws, registry = make_mirror_ws(
        tmp_path, skills_dirs=["ghost-skill", "registered-skill", "live-skill"],
        source_dirs=["live-skill"], registry=("registered-skill",))
    findings = su.find_orphan_mirror_dirs(ws, registry)
    targets = {f["target"] for f in findings}
    assert ".specify/skills/ghost-skill" in targets
    assert ".specify/skills/registered-skill" in targets
    assert ".specify/skills/live-skill" not in targets


def test_unregistered_orphan_is_high_severity_delete(tmp_path):
    ws, registry = make_mirror_ws(
        tmp_path, skills_dirs=["ghost-skill"], source_dirs=[], registry=())
    findings = su.find_orphan_mirror_dirs(ws, registry)
    f = next(f for f in findings if f["target"] == ".specify/skills/ghost-skill")
    assert f["severity"] == "high"
    assert f["disposition"] == "delete"
    assert f["reversibility"] == "irreversible"


def test_registered_orphan_is_medium_delegated(tmp_path):
    ws, registry = make_mirror_ws(
        tmp_path, skills_dirs=["registered-skill"], source_dirs=[], registry=("registered-skill",))
    findings = su.find_orphan_mirror_dirs(ws, registry)
    f = next(f for f in findings if f["target"] == ".specify/skills/registered-skill")
    assert f["severity"] == "medium"
    assert f["disposition"] == "delegate"


def test_orphan_check_skipped_without_source_root(tmp_path):
    """Client projects have no skills/ source root — pair not applicable."""
    mirror = tmp_path / ".specify" / "skills"
    mirror.mkdir(parents=True, exist_ok=True)
    (mirror / "only-skill").mkdir(exist_ok=True)
    findings = su.find_orphan_mirror_dirs(tmp_path, set())
    assert findings == []


def test_agents_runtime_structure_not_flagged(tmp_path):
    """`.specify/agents/` carries legitimate runtime structure (templates/
    instances/execution per agent-definitions); orphan detection is scoped to
    the skills pair only (dogfood-driven refinement)."""
    mirror = tmp_path / ".specify" / "agents"
    for sub in ("templates", "instances", "execution"):
        (mirror / sub).mkdir(parents=True, exist_ok=True)
        (mirror / sub / "x.md").write_text("#\n", encoding="utf-8")
    (tmp_path / "agents").mkdir(exist_ok=True)
    findings = su.find_orphan_mirror_dirs(tmp_path, set())
    assert findings == []


# --- obsolete-asset registry cross-check (C-12) ------------------------------------------

def test_load_obsolete_registry_parses_markers(tmp_path):
    cli = tmp_path / "src" / "specify_cli"
    cli.mkdir(parents=True, exist_ok=True)
    (cli / "__init__.py").write_text(
        "# OBSOLETE-ASSET-REGISTRY-START\n"
        "_OBSOLETE_SKILLS = [\"extension-e2e-test\", \"organize-agents\"]\n"
        "_OBSOLETE_COMMANDS = [\"old-cmd\"]\n"
        "# OBSOLETE-ASSET-REGISTRY-END\n",
        encoding="utf-8")
    registry = su.load_obsolete_registry(tmp_path)
    assert "extension-e2e-test" in registry
    assert "organize-agents" in registry
    assert "old-cmd" in registry


def test_load_obsolete_registry_missing_file_returns_empty(tmp_path):
    assert su.load_obsolete_registry(tmp_path) == set()


def test_real_repo_registry_loads(tmp_path):
    """The real repo's registry parses and contains the known renamed skill."""
    registry = su.load_obsolete_registry(ROOT)
    assert isinstance(registry, set)
    assert registry, "real repo registry should be non-empty"


# --- checker wiring ------------------------------------------------------------------------

def test_check_mirror_drift_uses_injected_output(tmp_path, monkeypatch):
    ws, _ = make_mirror_ws(tmp_path, skills_dirs=[], source_dirs=[])
    monkeypatch.setattr(su, "run_sync_mirrors_check", lambda root: (2, "MISS  .specify/skills/x/SKILL.md\n"))
    findings = su.check_mirror_drift(ws)
    assert any(".specify/skills/x/SKILL.md" in f["target"] for f in findings)
    assert all(f["detection"] == "programmatic" for f in findings)
