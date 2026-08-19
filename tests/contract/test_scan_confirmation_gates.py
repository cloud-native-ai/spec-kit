"""Contract tests for scripts/python/scan-confirmation-gates.py.

Contract: .specify/specs/044-reduce-confirmation-flows/contracts/gate-scanner-contract.md C-7.
Uses synthetic trees (--root) for determinism; no mirror surfaces involved.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

SCHEMA_KEYS = {"total", "gates", "by_class", "by_verdict", "baseline_delta", "violations"}
GATE_KEYS = {"id", "file", "line", "trigger", "action_class", "verdict", "evidence"}

BLOCKING_LINE = "流程 MUST 等待用户确认后才继续执行。"
DESTRUCTIVE_LINE = "删除文件前 MUST 等待用户确认。"


def run_scanner(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCANNER), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


def make_tree(root: Path) -> None:
    (root / "templates" / "commands").mkdir(parents=True)
    (root / "templates" / "commands" / "sample.md").write_text(
        f"# Sample\n\nline2\n{BLOCKING_LINE}\n", encoding="utf-8"
    )
    (root / "skills" / "sample-skill").mkdir(parents=True)
    (root / "skills" / "sample-skill" / "SKILL.md").write_text(
        f"# Skill\n\n{DESTRUCTIVE_LINE}\n", encoding="utf-8"
    )
    (root / "shared" / "workflow").mkdir(parents=True)
    (root / "shared" / "workflow" / "sample.md").write_text(
        "# Shared\n\nno gates here\n", encoding="utf-8"
    )
    # mirror surfaces that MUST be excluded from scanning
    (root / ".specify" / "templates" / "commands").mkdir(parents=True)
    (root / ".specify" / "templates" / "commands" / "sample.md").write_text(
        BLOCKING_LINE, encoding="utf-8"
    )
    (root / ".qoder" / "commands").mkdir(parents=True)
    (root / ".qoder" / "commands" / "speckit.sample.md").write_text(
        BLOCKING_LINE, encoding="utf-8"
    )


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    make_tree(tmp_path)
    return tmp_path


def test_schema_keys_complete(tree: Path) -> None:
    proc = run_scanner("--root", str(tree), "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert SCHEMA_KEYS <= set(payload), f"missing keys: {SCHEMA_KEYS - set(payload)}"
    assert payload["total"] == len(payload["gates"])
    for gate in payload["gates"]:
        assert GATE_KEYS <= set(gate), f"gate missing keys: {GATE_KEYS - set(gate)}"


def test_mirror_roots_excluded(tree: Path) -> None:
    payload = json.loads(run_scanner("--root", str(tree), "--json").stdout)
    files = {g["file"] for g in payload["gates"]}
    assert all(not f.startswith(".specify/") for f in files)
    assert all(not f.startswith(".qoder/") for f in files)
    assert payload["total"] == 2  # templates/commands + skills only


def test_taxonomy_deterministic_classification(tree: Path) -> None:
    payload = json.loads(run_scanner("--root", str(tree), "--json").stdout)
    by_file = {g["file"]: g for g in payload["gates"]}
    destructive = by_file["skills/sample-skill/SKILL.md"]
    assert destructive["action_class"] == "destructive"
    assert destructive["verdict"] == "keep_gate"
    reversible = by_file["templates/commands/sample.md"]
    assert reversible["action_class"] == "reversible"
    assert reversible["verdict"] == "auto_execute"


def test_governance_kept_paths(tree: Path) -> None:
    (tree / "templates" / "commands" / "interview.md").write_text(
        f"# Interview\n\n{BLOCKING_LINE}\n", encoding="utf-8"
    )
    payload = json.loads(run_scanner("--root", str(tree), "--json").stdout)
    gate = next(g for g in payload["gates"] if g["file"].endswith("interview.md"))
    assert gate["action_class"] == "governance_kept"
    assert gate["verdict"] == "keep_gate"


def test_doubtful_defaults_to_destructive(tree: Path) -> None:
    # ambiguous verb with no destructive keyword and no governance path
    (tree / "templates" / "commands" / "vague.md").write_text(
        "# Vague\n\n提交外部注册表前 MUST 等待用户确认。\n", encoding="utf-8"
    )
    payload = json.loads(run_scanner("--root", str(tree), "--json").stdout)
    gate = next(g for g in payload["gates"] if g["file"].endswith("vague.md"))
    assert gate["action_class"] == "destructive", "doubtful must default to destructive"
    assert gate["verdict"] == "keep_gate"


def test_baseline_delta(tree: Path, tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.json"
    first = run_scanner("--root", str(tree), "--json")
    baseline.write_text(first.stdout, encoding="utf-8")
    # remediate the reversible gate, keep the destructive one
    (tree / "templates" / "commands" / "sample.md").write_text(
        "# Sample\n\nline2\n已改为自动执行。\n", encoding="utf-8"
    )
    proc = run_scanner("--root", str(tree), "--json", "--baseline", str(baseline))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["baseline_delta"] is not None
    assert payload["baseline_delta"]["total"] == -1
    assert payload["violations"] == []


def test_exit_code_2_on_backflow(tree: Path, tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.json"
    baseline.write_text(
        run_scanner("--root", str(tree), "--json").stdout, encoding="utf-8"
    )
    # reversible gate still present post-governance -> violation -> exit 2
    proc = run_scanner("--root", str(tree), "--json", "--baseline", str(baseline))
    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert len(payload["violations"]) == 1
