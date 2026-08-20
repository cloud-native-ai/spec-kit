"""Integration test: US2 deterministic correctness checks (requirement 045 / Feature 047).

collect over the correctness fixture asserts all four categories with
detection=programmatic (SC-004), default severity mapping, auto-resolution of
externally fixed findings (C-10), and the partial-scan guard (C-14).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sanitize-utils.py"
FIXTURES = ROOT / "tests" / "fixtures" / "sanitize" / "correctness"
STORE_REL = Path(".specify") / "memory" / "sanitize" / "findings.json"


def run_engine(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(cwd), capture_output=True, text=True, timeout=180,
    )


def assemble(tmp_path: Path) -> Path:
    ws = tmp_path
    # dead-reference material (4 forms + exemptions)
    todo = ws / ".specify" / "memory" / "todo"
    todo.mkdir(parents=True, exist_ok=True)
    (todo / "material.md").write_text(
        FIXTURES.joinpath("material.md").read_text(encoding="utf-8"), encoding="utf-8")
    (ws / "scripts" / "python").mkdir(parents=True, exist_ok=True)
    (ws / "scripts" / "python" / "feedback-utils.py").write_text("#\n", encoding="utf-8")
    (ws / "templates" / "commands").mkdir(parents=True, exist_ok=True)
    (ws / "templates" / "commands" / "feedback.md").write_text("#\n", encoding="utf-8")
    (ws / "skills" / "create-docs").mkdir(parents=True, exist_ok=True)
    # index-inconsistency: features row 099 points to a missing detail file
    (ws / ".specify" / "memory" / "features").mkdir(parents=True, exist_ok=True)
    (ws / ".specify" / "memory" / "features.md").write_text(
        FIXTURES.joinpath("features-index.md").read_text(encoding="utf-8"), encoding="utf-8")
    (ws / ".specify" / "memory" / "features" / "098.md").write_text("# 098\n", encoding="utf-8")
    # broken-symlink: tool surfaces exist but their compat links do not
    (ws / ".claude").mkdir(exist_ok=True)
    (ws / ".github").mkdir(exist_ok=True)
    (ws / ".specify" / "instructions.md").write_text("# instructions\n", encoding="utf-8")
    # mirror-drift: unregistered + registered orphan mirror dirs
    mirror = ws / ".specify" / "skills"
    mirror.mkdir(parents=True, exist_ok=True)
    for name in ("ghost-skill", "registered-skill", "live-skill"):
        (mirror / name).mkdir(exist_ok=True)
        (mirror / name / "SKILL.md").write_text("#\n", encoding="utf-8")
    (ws / "skills" / "live-skill").mkdir(parents=True, exist_ok=True)
    cli = ws / "src" / "specify_cli"
    cli.mkdir(parents=True, exist_ok=True)
    (cli / "__init__.py").write_text(
        "# OBSOLETE-ASSET-REGISTRY:START\n"
        "_OBSOLETE_SKILLS = [\"registered-skill\"]\n"
        "# OBSOLETE-ASSET-REGISTRY:END\n",
        encoding="utf-8")
    return ws


def collect(ws: Path, *extra: str) -> dict:
    proc = run_engine(["--action", "collect", "--workspace-root", str(ws), *extra], cwd=ws)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(proc.stdout)


def store_of(ws: Path) -> list:
    return json.loads((ws / STORE_REL).read_text(encoding="utf-8"))["findings"]


def test_us2_all_four_categories_programmatic(tmp_path):
    ws = assemble(tmp_path)
    payload = collect(ws)
    findings = store_of(ws)
    categories = {f["category"] for f in findings}
    assert categories == {"dead-reference", "index-inconsistency", "broken-symlink", "mirror-drift"}, categories
    assert all(f["detection"] == "programmatic" for f in findings)  # SC-004
    assert payload["deterministic"]["added"] == len(findings)


def test_us2_severity_defaults_and_orphan_high(tmp_path):
    ws = assemble(tmp_path)
    collect(ws)
    findings = {f["target"]: f for f in store_of(ws)}
    ghost = findings[".specify/skills/ghost-skill"]
    assert ghost["severity"] == "high" and ghost["disposition"] == "delete"
    registered = findings[".specify/skills/registered-skill"]
    assert registered["severity"] == "medium" and registered["disposition"] == "delegate"
    assert ".specify/skills/live-skill" not in findings
    dead = next(f for t, f in findings.items() if "material.md#" in t)
    assert dead["severity"] == "medium"


def test_us2_auto_resolution_after_external_fix(tmp_path):
    ws = assemble(tmp_path)
    collect(ws)
    before = {f["id"]: f for f in store_of(ws)}
    dead_id = next(f["id"] for f in before.values() if "nope-utils.py" in f["target"])
    # external fix: create the previously missing path
    (ws / "scripts" / "python" / "nope-utils.py").write_text("#\n", encoding="utf-8")
    collect(ws)
    after = {f["id"]: f for f in store_of(ws)}
    assert after[dead_id]["state"] == "resolved"  # C-10 convergence
    assert "not re-detected" in " ".join(after[dead_id]["notes"])
    still_pending = [f for f in after.values() if f["state"] == "pending"]
    assert still_pending, "other findings must stay pending"


def test_us2_partial_scan_never_auto_resolves(tmp_path):
    ws = assemble(tmp_path)
    collect(ws)
    pending_before = sum(1 for f in store_of(ws) if f["state"] == "pending")
    assert pending_before > 0
    collect(ws, "--roots", "memory-todo")
    pending_after = sum(1 for f in store_of(ws) if f["state"] == "pending")
    assert pending_after == pending_before  # C-14 conservative rule


def test_us2_reopen_on_regression(tmp_path):
    ws = assemble(tmp_path)
    collect(ws)
    dead_id = next(f["id"] for f in store_of(ws) if "nope-utils.py" in f["target"])
    fixed = ws / "scripts" / "python" / "nope-utils.py"
    fixed.write_text("#\n", encoding="utf-8")
    collect(ws)
    assert {f["id"]: f for f in store_of(ws)}[dead_id]["state"] == "resolved"
    fixed.unlink()  # regression: the problem comes back
    collect(ws)
    assert {f["id"]: f for f in store_of(ws)}[dead_id]["state"] == "pending"  # C-11 reopen
