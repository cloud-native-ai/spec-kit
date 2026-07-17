"""Unit tests for the glossary engine `scripts/python/glossary-utils.py`
(spec 029 — Feature 031 Glossary Mechanism).

Exercises the CLI contract (contracts/glossary-utils-cli.md) via subprocess in
an isolated tmp workspace: init (create/non-destructive/force), validate, list,
detect-conflict, add (conflict- and precedence-guarded), remove.

TDD: authored before the engine actions were finalized; MUST fail against a tree
without the engine and pass once implemented.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "glossary-utils.py"
TEMPLATE = ROOT / "templates" / "glossary-template.md"


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), "--root", str(root), *args],
        capture_output=True, text=True,
    )


def out(cp: subprocess.CompletedProcess) -> dict:
    assert cp.returncode == 0, f"unexpected failure: {cp.stderr}"
    return json.loads(cp.stdout)


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "glossary-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / ".specify" / "memory").mkdir(parents=True)
    return tmp_path


def seeded(ws: Path) -> Path:
    out(run(ws, "--action", "init"))
    return ws / ".specify" / "memory" / "glossary.md"


def test_engine_exists():
    assert ENGINE.exists(), "glossary-utils.py engine is missing"


def test_init_creates_then_is_non_destructive(workspace: Path):
    first = out(run(workspace, "--action", "init"))
    assert first["created"] is True
    gloss = workspace / ".specify" / "memory" / "glossary.md"
    gloss.write_text(gloss.read_text() + "\n<!-- user marker -->\n")
    second = out(run(workspace, "--action", "init"))
    assert second["created"] is False and second["reason"] == "exists"
    assert "user marker" in gloss.read_text()  # preserved (FR-013)


def test_init_force_overwrites(workspace: Path):
    gloss = seeded(workspace)
    gloss.write_text(gloss.read_text() + "\n<!-- user marker -->\n")
    out(run(workspace, "--action", "init", "--force"))
    assert "user marker" not in gloss.read_text()


def test_validate_ok_and_empty_is_valid(workspace: Path):
    seeded(workspace)
    assert out(run(workspace, "--action", "validate"))["valid"] is True
    assert out(run(workspace, "--action", "list"))["count"] == 0  # placeholder excluded


def test_validate_rejects_bad_origin(workspace: Path):
    gloss = seeded(workspace)
    gloss.write_text(gloss.read_text().replace(
        "| None yet. | - | - | - | - |",
        "| Term | - | a meaning | bogus | confirmed |",
    ))
    cp = run(workspace, "--action", "validate")
    assert cp.returncode == 2 and "Origin" in cp.stderr


def test_add_and_list_roundtrip(workspace: Path):
    seeded(workspace)
    out(run(workspace, "--action", "add", "--canonical", "Spec Kit",
            "--variants", "speckit,speck it", "--meaning", "SDD toolkit",
            "--origin", "user", "--status", "confirmed"))
    listing = out(run(workspace, "--action", "list"))
    assert listing["count"] == 1
    e = listing["entries"][0]
    assert e["canonical"] == "Spec Kit" and "speck it" in e["variants"]


def test_detect_conflict_on_variant_bound_elsewhere(workspace: Path):
    seeded(workspace)
    out(run(workspace, "--action", "add", "--canonical", "Spec Kit",
            "--variants", "speckit", "--meaning", "SDD toolkit", "--origin", "user",
            "--status", "confirmed"))
    res = out(run(workspace, "--action", "detect-conflict", "--canonical", "speckit"))
    assert res["conflict"] is True and "Spec Kit" in res["collidesWith"]


def test_add_refuses_conflict_without_resolution(workspace: Path):
    seeded(workspace)
    # Existing term whose variant is "speckit".
    out(run(workspace, "--action", "add", "--canonical", "Spec Kit",
            "--variants", "speckit", "--meaning", "SDD toolkit", "--origin", "user",
            "--status", "confirmed"))
    # A NEW canonical "speckit" collides with the variant → conflict (not precedence).
    cp = run(workspace, "--action", "add", "--canonical", "speckit",
             "--meaning", "something else", "--origin", "auto")
    assert cp.returncode == 2 and "conflict" in cp.stderr
    # ... and succeeds with an explicit resolution.
    ok = out(run(workspace, "--action", "add", "--canonical", "speckit",
                 "--meaning", "something else", "--origin", "auto",
                 "--confirmed-resolution", "add-distinct"))
    assert ok["written"] is True


def test_auto_cannot_overwrite_user_without_confirmation(workspace: Path):
    seeded(workspace)
    out(run(workspace, "--action", "add", "--canonical", "Feature",
            "--meaning", "a capability", "--origin", "user", "--status", "confirmed"))
    cp = run(workspace, "--action", "add", "--canonical", "Feature",
             "--meaning", "auto guess", "--origin", "auto")
    assert cp.returncode == 2 and "user-authored" in cp.stderr


def test_remove_is_noop_when_absent(workspace: Path):
    seeded(workspace)
    res = out(run(workspace, "--action", "remove", "--canonical", "Nonexistent"))
    assert res["removed"] == 0
    out(run(workspace, "--action", "add", "--canonical", "Temp",
            "--meaning", "x", "--origin", "user", "--status", "confirmed"))
    res2 = out(run(workspace, "--action", "remove", "--canonical", "Temp"))
    assert res2["removed"] == 1 and res2["count"] == 0
