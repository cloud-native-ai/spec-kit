"""Unit tests for semantic-candidate collection (requirement 045 / Feature 047).

Pins contracts/sanitize-detection-rules.md §5 C-14..C-16: mechanical claims
extraction (frontmatter dates/status + declaration phrases), evidence-pack
assembly (bounded git log, path existence), and git-unavailable degradation.
The stale-todo fixture reproduces the motivating real case (a parked todo
claiming unlanded work while a later commit landed it).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "sanitize" / "stale-todo" / "parked-todo.md"


def git(root: Path, *args: str, date: str | None = None) -> str:
    env = dict(os.environ)
    if date:
        env["GIT_COMMITTER_DATE"] = date
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def assemble_workspace(tmp_path: Path, land_commit: bool = True) -> Path:
    """Build a mini repo around the fixture material: todo claims unlanded work
    that a later commit (dated after the claim) actually landed."""
    todo = tmp_path / ".specify" / "memory" / "todo" / "20260812-backlog.md"
    todo.parent.mkdir(parents=True, exist_ok=True)
    todo.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    target = tmp_path / "scripts" / "js" / "better-harness" / "session-analysis" / "platforms" / "claude.mjs"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("export const probeTranscript = 1;\n", encoding="utf-8")
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "chore: import material claiming five items unlanded",
        "--date", "2026-08-11T00:00:00", date="2026-08-11T00:00:00")
    if land_commit:
        target.write_text("export const probeTranscript = 2;\n", encoding="utf-8")
        git(tmp_path, "add", "-A")
        git(tmp_path, "commit", "-q", "-m", "feat: land all five items (P1-P5)",
            "--date", "2026-08-13T00:00:00", date="2026-08-13T00:00:00")
    return tmp_path


# --- claims extraction (C-15) ------------------------------------------------------

def test_extract_claims_pulls_frontmatter_status_and_date():
    claims = su.extract_claims(FIXTURE.read_text(encoding="utf-8"))
    assert any(c.startswith("status=parked") for c in claims)
    assert any(c.startswith("parked_at=2026-08-12") for c in claims)


def test_extract_claims_pulls_declaration_phrases():
    claims = su.extract_claims(FIXTURE.read_text(encoding="utf-8"))
    assert any("未落地" in c for c in claims)


def test_extract_claims_is_mechanical_no_semantic_induction():
    text = "---\nstatus: parked\n---\n一句话,无任何声明关键词。\n"
    claims = su.extract_claims(text)
    assert claims == ["status=parked"]


# --- path extraction ---------------------------------------------------------------

def test_extract_repo_paths_finds_known_prefixes():
    paths = su.extract_repo_paths(FIXTURE.read_text(encoding="utf-8"))
    assert "scripts/js/better-harness/session-analysis/platforms/claude.mjs" in paths
    assert "scripts/python/evidence-utils.py" in paths


# --- evidence pack (C-16) ------------------------------------------------------------

def test_evidence_pack_gitlog_bounded_and_path_existence(tmp_path):
    assemble_workspace(tmp_path)
    candidates, notes = su.collect_semantic_candidates(tmp_path)
    assert notes == []
    assert len(candidates) == 1
    pack = candidates[0]["evidencePack"]
    assert any("land all five items" in line for line in pack["gitLog"])
    assert all(line.split(" ", 1)[0].strip() for line in pack["gitLog"] if line)
    assert len(pack["gitLog"]) <= 20
    assert pack["pathExistence"]["scripts/js/better-harness/session-analysis/platforms/claude.mjs"] is True


def test_evidence_pack_covers_commits_predating_claim(tmp_path):
    """Absence-of-work claims are often contradicted by commits that PREDATE
    the claim date (the parking note copied a stale conclusion) — the pack
    must not be date-filtered (real-case regression: 1a090c72 vs 0801 todo)."""
    tmp = assemble_workspace(tmp_path)
    candidates, _ = su.collect_semantic_candidates(tmp)
    pack = candidates[0]["evidencePack"]
    assert any("import material" in line for line in pack["gitLog"]), \
        "commits older than the claim date must stay visible"


def test_evidence_pack_fragment_globs_reach_deep_paths(tmp_path):
    """Fragments without a rooted prefix (e.g. `platforms/claude.mjs`) glob to
    their deep counterparts for git evidence."""
    tmp = assemble_workspace(tmp_path)
    text = (tmp / ".specify" / "memory" / "todo" / "20260812-backlog.md").read_text(encoding="utf-8")
    # simulate a material that references only the bare fragment
    (tmp / ".specify" / "memory" / "todo" / "fragment-only.md").write_text(
        text.replace("scripts/js/better-harness/session-analysis/platforms/claude.mjs",
                     "platforms/claude.mjs"), encoding="utf-8")
    candidates, _ = su.collect_semantic_candidates(tmp)
    by_material = {c["material"]: c for c in candidates}
    pack = by_material[".specify/memory/todo/fragment-only.md"]["evidencePack"]
    assert any("land all five items" in line for line in pack["gitLog"]), \
        "fragment glob must reach the deep path's history"


# --- git-unavailable degradation ------------------------------------------------------

def test_collect_semantic_candidates_degrades_without_git(tmp_path, monkeypatch):
    assemble_workspace(tmp_path)

    def _no_git(root, args):
        return None

    monkeypatch.setattr(su, "_git", _no_git)
    candidates, notes = su.collect_semantic_candidates(tmp_path)
    assert candidates == []
    assert any("git unavailable" in n for n in notes)


def test_missing_roots_yield_no_candidates(tmp_path):
    candidates, notes = su.collect_semantic_candidates(tmp_path)
    assert candidates == []
    assert notes == []
