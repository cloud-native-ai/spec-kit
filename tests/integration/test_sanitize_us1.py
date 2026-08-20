"""Integration test: US1 full flow (requirement 045 / Feature 047).

collect → agent verdicts → record → status over the stale-todo fixture,
asserting SC-001 (stale-residue finding carries commit-level evidence),
SC-002 (checked materials unchanged; writes confined to the store), and the
insufficient-evidence rule (candidates the agent cannot ground are never
recorded).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sanitize-utils.py"
FIXTURE = ROOT / "tests" / "fixtures" / "sanitize" / "stale-todo" / "parked-todo.md"
STORE_REL = Path(".specify") / "memory" / "sanitize" / "findings.json"


def git(root: Path, *args: str, date: str | None = None) -> str:
    env = dict(os.environ)
    if date:
        env["GIT_COMMITTER_DATE"] = date
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def run_engine(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(cwd), capture_output=True, text=True, timeout=120,
    )


def assemble_workspace(tmp_path: Path) -> Path:
    todo = tmp_path / ".specify" / "memory" / "todo" / "20260812-backlog.md"
    todo.parent.mkdir(parents=True, exist_ok=True)
    todo.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    # a second material whose claims have no contradicting evidence — the
    # agent would judge it "insufficient evidence" and never record it
    vague = tmp_path / ".specify" / "memory" / "todo" / "20260812-vague.md"
    vague.write_text(
        "---\nstatus: parked\nparked_at: 2026-08-12\n---\n待办:考虑一下未来的事情。\n",
        encoding="utf-8")
    target = tmp_path / "scripts" / "js" / "better-harness" / "session-analysis" / "platforms" / "claude.mjs"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("export const probeTranscript = 1;\n", encoding="utf-8")
    # the material also references evidence-utils.py — keep it alive so the
    # US1 assertions see exactly one semantic finding and zero dead references
    evidence = tmp_path / "scripts" / "python" / "evidence-utils.py"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("# engine\n", encoding="utf-8")
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "chore: import materials",
        "--date", "2026-08-11T00:00:00", date="2026-08-11T00:00:00")
    target.write_text("export const probeTranscript = 2;\n", encoding="utf-8")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "feat: land all five items (P1-P5)",
        "--date", "2026-08-13T00:00:00", date="2026-08-13T00:00:00")
    return tmp_path


def test_us1_collect_record_status_flow(tmp_path):
    ws = assemble_workspace(tmp_path)
    before_all = {p.relative_to(ws).as_posix(): p.read_bytes()
                  for p in ws.rglob("*") if p.is_file()}

    # 1) collect: deterministic merge + semantic candidates with evidence packs
    proc = run_engine(["--action", "collect", "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    candidates = payload["semanticCandidates"]
    by_material = {c["material"]: c for c in candidates}
    backlog = by_material[".specify/memory/todo/20260812-backlog.md"]
    assert any("land all five items" in line for line in backlog["evidencePack"]["gitLog"])
    assert any("未落地" in claim for claim in backlog["claims"])
    landing_hash = next(
        line.split(" ", 1)[0] for line in backlog["evidencePack"]["gitLog"]
        if "land all five items" in line)

    # 2) agent verdicts: only the grounded material is judged stale-residue
    target = ".specify/memory/todo/20260812-backlog.md"
    finding = {
        "id": hashlib.sha1(f"stale-residue|{target}".encode()).hexdigest()[:12],
        "category": "stale-residue",
        "target": target,
        "severity": "high",
        "summary": f"claims five items unlanded while {landing_hash} landed them",
        "evidenceRefs": [{"kind": "commit", "ref": landing_hash}],
        "detection": "semantic",
        "disposition": "delete",
        "reversibility": "irreversible",
        "state": "pending",
    }
    verdicts = ws / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [finding]}), encoding="utf-8")
    proc = run_engine(
        ["--action", "record", "--file", str(verdicts), "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0, proc.stdout

    # 3) status digest shows the pending finding
    proc = run_engine(["--action", "status", "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 0
    digest = json.loads(proc.stdout)["store"]
    assert digest["byState"]["pending"] == 1
    assert digest["byCategory"]["stale-residue"] == 1

    # SC-001: the finding carries commit-level evidence
    store = json.loads((ws / STORE_REL).read_text(encoding="utf-8"))
    entry = store["findings"][0]
    assert entry["evidenceRefs"][0]["kind"] == "commit"
    assert entry["evidenceRefs"][0]["ref"] == landing_hash
    assert entry["state"] == "pending"

    # SC-002: full snapshot — no existing file changed; new files are exactly
    # the store plus the agent's verdicts file
    after_all = {p.relative_to(ws).as_posix(): p.read_bytes()
                 for p in ws.rglob("*") if p.is_file()}
    changed = [f for f in set(before_all) & set(after_all) if before_all[f] != after_all[f]]
    new_files = set(after_all) - set(before_all)
    assert changed == [], f"existing files modified: {changed}"
    assert new_files == {STORE_REL.as_posix(), "verdicts.json"}, f"unexpected writes: {new_files}"

    # insufficient-evidence material never entered the store
    assert all(f["target"] != ".specify/memory/todo/20260812-vague.md" for f in store["findings"])


def test_us1_record_rejects_ungrounded_semantic_finding(tmp_path):
    """A semantic verdict without commit/path evidence is schema-rejected (C-3)."""
    ws = assemble_workspace(tmp_path)
    run_engine(["--action", "collect", "--workspace-root", str(ws)], cwd=ws)
    target = ".specify/memory/todo/20260812-backlog.md"
    finding = {
        "id": hashlib.sha1(f"stale-residue|{target}".encode()).hexdigest()[:12],
        "category": "stale-residue", "target": target, "severity": "high",
        "summary": "judged stale after analysis",
        "evidenceRefs": [],  # no commit/path evidence — agent must not do this
        "detection": "semantic", "disposition": "delete",
        "reversibility": "irreversible", "state": "pending",
    }
    verdicts = ws / "verdicts.json"
    verdicts.write_text(json.dumps({"findings": [finding]}), encoding="utf-8")
    proc = run_engine(
        ["--action", "record", "--file", str(verdicts), "--workspace-root", str(ws)], cwd=ws)
    assert proc.returncode == 2
    store = json.loads((ws / STORE_REL).read_text(encoding="utf-8"))
    assert store["findings"] == []
