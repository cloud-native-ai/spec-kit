"""Integration tests: docs command deterministic scenarios (spec 033).

Covers the engine-verifiable parts of SC-001 (compliant skeleton passes
validate), SC-002 (repeat runs converge to zero new findings, audit always
written), and SC-006 (naming violations named).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "python" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs_command"

TYPE_DIRS = ["concepts", "tutorials", "tasks", "reference", "decisions", "contribute", "notes"]
ROOT_ENTRIES = {
    "README.md": "# Project\n\nSee [docs](docs/concepts/overview.md).\n",
    "ARCHITECTURE.md": "# Architecture\n\nSummary. See [overview](docs/concepts/overview.md).\n",
    "CONTRIBUTING.md": "# Contributing\n\nSee [dev setup](docs/contribute/dev-setup.md).\n",
    "CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n",
}


def run_engine(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def make_skeleton(root: Path) -> None:
    """Build the bootstrap skeleton the command template promises (SC-001 shape)."""
    for name, body in ROOT_ENTRIES.items():
        (root / name).write_text(body, encoding="utf-8")
    for d in TYPE_DIRS:
        (root / "docs" / d).mkdir(parents=True)
    (root / "docs" / "concepts" / "overview.md").write_text("# Overview\n", encoding="utf-8")
    (root / "docs" / "contribute" / "dev-setup.md").write_text("# Dev setup\n", encoding="utf-8")
    (root / "docs" / "decisions" / "README.md").write_text("# ADR index\n", encoding="utf-8")
    (root / "docs" / "decisions" / "template.md").write_text("# ADR-NNNN: title\n", encoding="utf-8")
    (root / "docs" / "notes" / "README.md").write_text(
        "# Notes\n\nfrontmatter required: title/created/expires/status\n", encoding="utf-8"
    )


@pytest.mark.integration
def test_sc001_compliant_skeleton_has_zero_violations(tmp_path: Path):
    make_skeleton(tmp_path)
    out = run_engine("--action", "validate", "--root", str(tmp_path))
    assert out["violations"] == [], f"skeleton must be clean: {out['violations']}"


@pytest.mark.integration
def test_sc002_repeat_run_zero_new_findings_but_audit_always_written(tmp_path: Path):
    make_skeleton(tmp_path)
    first = run_engine("--action", "validate", "--root", str(tmp_path))
    second = run_engine("--action", "validate", "--root", str(tmp_path))
    assert first == second, "validate must be idempotent (anti-churn)"
    a1 = run_engine("--action", "audit", "--root", str(tmp_path),
                    "--scope", "full", "--summary", "all dimensions within tolerance")
    a2 = run_engine("--action", "audit", "--root", str(tmp_path),
                    "--scope", "full", "--summary", "all dimensions within tolerance")
    audit_dir = tmp_path / ".specify" / "docs" / "audit"
    assert a1["written"] and a2["written"]
    assert len(list(audit_dir.glob("*.md"))) == 2, "every run must leave an audit trace"


@pytest.mark.integration
def test_sc006_naming_violations_all_named(tmp_path: Path):
    proj = tmp_path / "proj"
    shutil.copytree(FIXTURES / "messy_project", proj)
    out = run_engine("--action", "validate", "--root", str(proj))
    flagged = {(v["kind"], v["path"]) for v in out["violations"]}
    assert ("reserved-name-case", "readme.md") in flagged
    assert ("reserved-name-misuse", "DESIGN.md") in flagged
    broken = [v for v in out["violations"] if v["kind"] == "broken-link"]
    assert len(broken) >= 2, "both broken links must be reported"
