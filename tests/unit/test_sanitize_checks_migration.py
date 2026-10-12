"""Unit tests: init migration-residue checkers (detection-rules §4a, 2026-10-12).

Pins C-22 (legacy install residue: legacy skill dirs / pre-B2a git-workflow
state files / old tools-registry directory), C-23 (flat duplicates of the
nested internal layer), the C-10 extension to .qoder/skills and .claude/skills,
and the LEGACY_SKILL_NAMES drift guard against the CLI's _OBSOLETE_SKILLS.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402


def _skill_dir(base: Path, name: str, marker: str = "# skill\n") -> Path:
    d = base / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(marker, encoding="utf-8")
    return d


# --- C-23 flat duplicates of the nested internal layer --------------------------

def test_flat_internal_duplicate_detected(tmp_path):
    nested = _skill_dir(tmp_path / ".specify" / "skills" / "internal", "code-review")
    _skill_dir(tmp_path / ".specify" / "skills", "code-review")
    findings = su.check_flat_internal_duplicates(tmp_path)
    assert [f["target"] for f in findings] == [".specify/skills/code-review"]
    f = findings[0]
    assert f["category"] == "redundant" and f["disposition"] == "archive"
    assert f["severity"] == "medium"
    assert su.validate_finding(f, tmp_path) == []


def test_no_flat_twin_no_finding(tmp_path):
    _skill_dir(tmp_path / ".specify" / "skills" / "internal", "code-review")
    assert su.check_flat_internal_duplicates(tmp_path) == []


def test_flat_symlink_not_a_candidate(tmp_path):
    _skill_dir(tmp_path / ".specify" / "skills" / "internal", "code-review")
    real = tmp_path / "elsewhere" / "code-review"
    real.mkdir(parents=True)
    (tmp_path / ".specify" / "skills" / "code-review").symlink_to(real)
    assert su.check_flat_internal_duplicates(tmp_path) == []


def test_no_internal_layer_no_finding(tmp_path):
    _skill_dir(tmp_path / ".specify" / "skills", "code-review")
    assert su.check_flat_internal_duplicates(tmp_path) == []


# --- C-22 legacy skill directories ------------------------------------------------

def test_legacy_skill_dir_via_builtin_constant(tmp_path):
    # Client workspace: no src/ tree -> the LEGACY_SKILL_NAMES fallback applies.
    _skill_dir(tmp_path / ".specify" / "skills", "draw-mermaid")
    _skill_dir(tmp_path / ".specify" / "skills", "my-own-skill")  # user-authored
    findings = su.check_legacy_install_residue(tmp_path)
    targets = [f["target"] for f in findings]
    assert ".specify/skills/draw-mermaid" in targets
    assert ".specify/skills/my-own-skill" not in targets
    f = next(f for f in findings if f["target"] == ".specify/skills/draw-mermaid")
    assert f["category"] == "stale-residue" and f["disposition"] == "archive"
    assert "draw-diagram" in f["summary"]  # successor hint
    assert su.validate_finding(f, tmp_path) == []


def test_legacy_names_registry_wins_when_framework_source_present(tmp_path):
    cli = tmp_path / "src" / "specify_cli"
    cli.mkdir(parents=True)
    (cli / "__init__.py").write_text(
        "# OBSOLETE-ASSET-REGISTRY:START\n"
        '_OBSOLETE_SKILLS = (\n    "custom-retired",\n)\n'
        "# OBSOLETE-ASSET-REGISTRY:END\n",
        encoding="utf-8",
    )
    _skill_dir(tmp_path / ".specify" / "skills", "custom-retired")
    _skill_dir(tmp_path / ".specify" / "skills", "draw-mermaid")
    targets = [f["target"] for f in su.check_legacy_install_residue(tmp_path)]
    assert ".specify/skills/custom-retired" in targets
    assert ".specify/skills/draw-mermaid" not in targets  # registry precedence


def test_legacy_skill_symlink_skipped(tmp_path):
    real = tmp_path / "elsewhere" / "git-workflow"
    real.mkdir(parents=True)
    (tmp_path / ".specify" / "skills").mkdir(parents=True)
    (tmp_path / ".specify" / "skills" / "git-workflow").symlink_to(real)
    assert su.check_legacy_install_residue(tmp_path) == []


def test_framework_source_present_defers_to_mirror_drift(tmp_path):
    # In a framework repo the flat legacy-named dir is a MIRROR orphan (C-12);
    # the residue checker must not double-report it with a conflicting disposal.
    _skill_dir(tmp_path / "skills" / "external", "create-docs")
    _skill_dir(tmp_path / ".specify" / "skills", "draw-mermaid")
    assert not any(f["target"] == ".specify/skills/draw-mermaid"
                   for f in su.check_legacy_install_residue(tmp_path))


# --- C-22 legacy git-workflow state files -----------------------------------------

def test_legacy_gitworkflow_state_flagged_only_when_new_state_exists(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "git-workflow.md").write_text("# state\n", encoding="utf-8")
    (tmp_path / ".specify" / "memory").mkdir(parents=True)
    (tmp_path / ".specify" / "git-workflow.md").write_text("# old\n", encoding="utf-8")
    (tmp_path / ".specify" / "memory" / "git-workflow.md").write_text(
        "# old\n", encoding="utf-8")
    targets = [f["target"] for f in su.check_legacy_install_residue(tmp_path)]
    assert ".specify/git-workflow.md" in targets
    assert ".specify/memory/git-workflow.md" in targets
    for f in su.check_legacy_install_residue(tmp_path):
        assert f["disposition"] == "archive"
        assert su.validate_finding(f, tmp_path) == []


def test_pre_migration_project_not_flagged(tmp_path):
    # Only the old state file exists (docs/ state never landed): a genuinely
    # old-generation project, not migration residue.
    (tmp_path / ".specify").mkdir(parents=True)
    (tmp_path / ".specify" / "git-workflow.md").write_text("# old\n", encoding="utf-8")
    assert su.check_legacy_install_residue(tmp_path) == []


# --- C-22 legacy tools-registry directory -----------------------------------------

def test_legacy_tools_dir_flagged_only_when_new_home_exists(tmp_path):
    (tmp_path / ".specify" / "tools").mkdir(parents=True)
    (tmp_path / ".specify" / "tools" / "shell.json").write_text("{}", encoding="utf-8")
    assert su.check_legacy_install_residue(tmp_path) == []  # no new home yet
    (tmp_path / ".specify" / "memory" / "tools").mkdir(parents=True)
    findings = [f for f in su.check_legacy_install_residue(tmp_path)
                if f["target"] == ".specify/tools"]
    assert len(findings) == 1
    assert findings[0]["disposition"] == "archive"
    assert su.validate_finding(findings[0], tmp_path) == []


# --- C-10 extension: agent skills links -------------------------------------------

def test_agent_skills_link_form_drift(tmp_path):
    (tmp_path / ".qoder" / "skills").mkdir(parents=True)  # real dir, not a link
    (tmp_path / ".claude").mkdir()  # tool surface present, link missing
    targets = [(f["category"], f["target"])
               for f in su.check_broken_symlinks(tmp_path)]
    assert ("broken-symlink", ".qoder/skills") in targets
    assert ("broken-symlink", ".claude/skills") in targets


def test_agent_skills_absent_tool_surface_not_flagged(tmp_path):
    (tmp_path / ".specify").mkdir(parents=True)
    assert not any(f["target"] == ".claude/skills"
                   for f in su.check_broken_symlinks(tmp_path))


# --- drift guard: engine constant vs CLI registry ----------------------------------

def test_legacy_names_superset_of_cli_obsolete_skills():
    sys.path.insert(0, str(ROOT / "src"))
    import specify_cli

    missing = set(specify_cli._OBSOLETE_SKILLS) - set(su.LEGACY_SKILL_NAMES)
    assert not missing, f"LEGACY_SKILL_NAMES lags the CLI registry: {sorted(missing)}"
