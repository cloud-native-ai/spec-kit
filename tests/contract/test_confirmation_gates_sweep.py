"""Framework-wide gate-governance sweep (structural contract).

Contract: confirmation-taxonomy-contract.md C-7 + FR-007/FR-011 (requirement 044).
Drives the real scanner (Program-First measurement) and pins the protected keep list.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
BASELINE = (
    REPO_ROOT
    / ".specify/specs/044-reduce-confirmation-flows/baseline.json"
)

# (file, marker) — every protected gate MUST keep a stable textual anchor
KEEP_LIST = [
    ("templates/commands/feedback.md", "confirmation of the report"),
    ("templates/commands/docs.md", "stop-and-confirm"),
    ("templates/commands/session.md", "same-name"),
    ("templates/commands/feature.md", "status"),
    ("templates/commands/analyze.md", "explicitly approve"),
    ("templates/commands/interview.md", "confirm"),
    ("templates/constitution-template.md", "irreversible"),
    ("templates/commands/todo.md", "only execute on explicit user approval"),
    ("templates/commands/implement.md", "only execute on explicit user approval"),
    ("templates/commands/implement.md", "CONFIRM"),
    ("templates/commands/tools.md", "confirm"),
    ("skills/git-workflow/SKILL.md", "force-with-lease"),
    ("shared/workflow/glossary.md", "--confirmed-resolution"),
    ("shared/definitions/tool-definitions.md", "Execution never happens before user confirmation via preview gate"),
    ("skills/create-team/references/operating-loops.md", "分级确认"),
    ("templates/commands/sanitize.md", "等待用户确认后才执行"),
]


def run_scanner() -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(REPO_ROOT), "--json"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_no_reversible_gates_remain_blocking() -> None:
    payload = run_scanner()
    reversible = [g for g in payload["gates"] if g["action_class"] == "reversible"]
    assert reversible == [], (
        "reversible gates still present in blocking form: "
        + ", ".join(f"{g['file']}:{g['line']}" for g in reversible[:10])
    )


def test_residual_total_within_sc002_target() -> None:
    if not BASELINE.is_file():
        pytest.skip("baseline.json not present (pre-implementation checkout)")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    payload = run_scanner()
    cap = baseline["total"] * 0.25
    assert payload["total"] <= cap, (
        f"SC-002 target missed: residual {payload['total']} > 25% of baseline {baseline['total']}"
    )


@pytest.mark.parametrize("rel_path,marker", KEEP_LIST)
def test_protected_gate_preserved(rel_path: str, marker: str) -> None:
    path = REPO_ROOT / rel_path
    assert path.is_file(), f"protected surface missing: {rel_path}"
    text = path.read_text(encoding="utf-8")
    assert marker in text, f"protected gate marker lost in {rel_path}: {marker!r}"
