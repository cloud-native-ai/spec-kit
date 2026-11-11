"""Fixture replay of the full archive round (Feature 100, P4).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-107 — the flow position is fixed: ``merge-plan → merge-apply →
          commit the merge batch → archive-plan → archive-apply → commit the
          archive batch → seal judgment``; a blocked seal judgment neither
          blocks the archive nor changes the blocking list.

Scope: a throwaway replay tree built from ``tests/fixtures/seal-archive/clean-pair``
under ``tmp_path``. The replay strips the pre-baked merge result so ``merge-apply``
performs a real write batch, commits it, archives, commits, and then judges seal
in its blocked state before and after. The live repository is never written.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal-archive"

PARENT = "100-fixture-parent"
ALPHA = "100a-fixture-alpha"
BETA = "100b-fixture-beta"
SPEC_REL = ".specify/specs/%s" % PARENT
MANIFEST_REL = SPEC_REL + "/archive-manifest.json"
MERGE_REL = SPEC_REL + "/merge-manifest.json"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    })
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
         *args],
        capture_output=True, text=True, encoding="utf-8", check=False, env=env,
    )


def _run(repo: Path, action: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", action,
         "--spec-dir", str(repo / SPEC_REL), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload for {action}; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _file_rows(directory: Path) -> list:
    return [
        {"path": path.relative_to(directory).as_posix(),
         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(directory.rglob("*")) if path.is_file()
    ]


def _name_status(repo: Path, commit: str) -> list:
    proc = _git(repo, "diff", "--name-status", "-M", commit)
    assert proc.returncode == 0, proc.stderr[-400:]
    rows = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0].startswith("R") and len(parts) == 3:
            rows.append(("R", parts[1], parts[2]))
        elif len(parts) == 2:
            rows.append((parts[0], parts[1], None))
    return rows


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _strip_merged_marker(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines()
             if not line.startswith("**Merged into**:")]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _prepare_replay(tmp_path: Path) -> Path:
    """A pre-merge copy of clean-pair: merge-apply then performs real writes."""
    repo = tmp_path / "replay"
    shutil.copytree(FIXTURES / "clean-pair", repo)
    parent = repo / SPEC_REL
    (parent / "merge-manifest.json").unlink()
    _write(parent / "requirements.md",
           "# Requirements: fixture parent\n\n"
           "- **FR-001**: The fixture parent owns the two-slice round.\n"
           "- **FR-002**: The parent second slot for fixture beta.\n")
    mappings = {
        ALPHA: "FR-001",
        BETA: "FR-002",
    }
    for slug, target in mappings.items():
        requirements = repo / ".specify/specs" / slug / "requirements.md"
        _strip_merged_marker(requirements)
        _write(requirements, requirements.read_text(encoding="utf-8")
               + "\n## Parent Mapping\n\n| Slice ID | Parent ID |\n"
                 "|----------|-----------|\n| FR-001 | %s |\n" % target)
    _write(repo / ".specify/features.md",
           "# Feature Registry\n\n"
           "| ID | Feature | Status | Last Updated |\n"
           "|----|---------|--------|--------------|\n"
           "| %s | Fixture parent | Ready for Review | 2026-11-11 |\n" % PARENT)
    _write(repo / ".specify/features" / ("%s.md" % PARENT),
           "# Feature 100 — fixture parent\n\n**Status**: Ready for Review\n")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "replay baseline").returncode == 0
    return repo


# ---------------------------------------------------------------------------
# C-107 — the round: merge commit → archive → archive commit → seal judgment
# ---------------------------------------------------------------------------

def test_the_round_registers_archives_and_keeps_the_seal_blocking_list(tmp_path):
    repo = _prepare_replay(tmp_path)
    seal_receipt = (repo / SPEC_REL / "seal.md").read_bytes()

    merge_proc, merge_payload = _run(repo, "merge-apply")
    assert merge_proc.returncode == 0, merge_payload.get("conditions")
    assert merge_payload["apply"]["writes"], (
        "C-107: the replay must exercise the real merge-apply batch before archive"
    )
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "merge batch").returncode == 0

    seal_proc, seal_before = _run(repo, "seal")
    assert seal_proc.returncode != 0 and seal_before["conditions"], (
        "the fixture must sit in a named blocking state before the archive"
    )

    plan_proc, plan_payload = _run(repo, "archive-plan")
    assert plan_proc.returncode == 0, plan_payload.get("conditions")
    assert plan_payload["outcome"] == "would-archive"
    pinned = plan_payload["archive"]["manifest"]["pinned_commit"]
    before = {slug: _file_rows(repo / ".specify/specs" / slug)
              for slug in (ALPHA, BETA)}

    apply_proc, apply_payload = _run(repo, "archive-apply")
    assert apply_proc.returncode == 0, apply_payload.get("conditions")
    assert apply_payload["outcome"] == "archived", (
        "C-107: a blocked seal judgment never blocks the archive"
    )
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == pinned, (
        "C-207: archive-apply itself never commits"
    )
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "archive batch").returncode == 0

    for slug in (ALPHA, BETA):
        destination = repo / SPEC_REL / "slices" / slug
        assert _file_rows(destination) == before[slug], (
            "SC-001: file count, per-file sha256 and relative paths are unchanged"
        )
        assert not (repo / ".specify/specs" / slug).exists()

    manifest = json.loads((repo / MANIFEST_REL).read_text(encoding="utf-8"))
    assert manifest["checks"]["files_match"] is True
    assert manifest["pinned_commit"] == pinned
    assert [entry["slug"] for entry in manifest["slices"]] == [ALPHA, BETA]

    rows = _name_status(repo, pinned)
    assert not [row for row in rows if row[0] == "D"], (
        "SC-001: the batch shows zero plain deletions"
    )
    expected_renames = {
        (".specify/specs/%s/%s" % (slug, item["path"]),
         "%s/slices/%s/%s" % (SPEC_REL, slug, item["path"]))
        for slug, files in before.items() for item in files
    }
    assert {(row[1], row[2]) for row in rows if row[0] == "R"} == expected_renames, (
        "SC-001: every moved file reads as one rename pair"
    )
    assert {row[1] for row in rows if row[0] == "A"} == {MANIFEST_REL}
    assert {row[1] for row in rows if row[0] == "M"} == {MERGE_REL}

    seal_proc, seal_after = _run(repo, "seal")
    assert seal_after["conditions"] == seal_before["conditions"], (
        "C-107: archiving never changes the seal blocking list"
    )
    assert seal_after["verdict"] == seal_before["verdict"]
    assert seal_after["exit_code"] == seal_before["exit_code"]
    assert (repo / SPEC_REL / "seal.md").read_bytes() == seal_receipt, (
        "C-110/SC-005: the parent seal receipt is byte-identical to before"
    )

    replay_proc, replay_payload = _run(repo, "archive-apply")
    assert replay_proc.returncode == 0
    assert replay_payload["outcome"] == "already-archived", (
        "FR-026: the archived round is reproducible"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


# ---------------------------------------------------------------------------
# C-107 / SC-004 — a blocked seal still archives; a refused merge does not start
# ---------------------------------------------------------------------------

BLOCKED_PAIR = FIXTURES / "blocked-pair"


def _replay_fixture(fixture: Path, tmp_path: Path) -> Path:
    """A committed copy of one fixture tree under ``tmp_path``."""
    repo = tmp_path / "replay"
    shutil.copytree(fixture, repo)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "fixture baseline").returncode == 0
    return repo


def _codes(payload: dict) -> list:
    return [condition["code"] for condition in payload["conditions"]]


def _snapshot(root: Path) -> dict:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def _seal_facets(payload: dict) -> list:
    """The blocking list with only the legitimate archived path normalised out."""
    archived = SPEC_REL + "/slices/"
    facets = []
    for condition in payload["conditions"]:
        evidence = condition["evidence"]
        for slug in (ALPHA, BETA):
            evidence = evidence.replace(archived + slug, ".specify/specs/" + slug)
        facets.append((condition["code"], evidence))
    return facets


def test_blocked_seal_still_archives(tmp_path):
    """C-107: the archive runs in a named blocking state and leaves it untouched."""
    repo = _replay_fixture(BLOCKED_PAIR, tmp_path)
    seal_proc, seal_before = _run(repo, "seal")
    assert seal_proc.returncode != 0, (
        "the blocked-pair fixture must sit in a seal blocking state"
    )
    assert "code-review-blocking" in _codes(seal_before), (
        "SC-004: the fixture's seal blocking is named, not inferred"
    )

    plan_proc, plan_payload = _run(repo, "archive-plan")
    assert plan_proc.returncode == 0, plan_payload.get("conditions")
    assert plan_payload["outcome"] == "would-archive"

    apply_proc, apply_payload = _run(repo, "archive-apply")
    assert apply_proc.returncode == 0, apply_payload.get("conditions")
    assert apply_payload["outcome"] == "archived", (
        "C-107: archiving MUST NOT require a Sealed judgment"
    )
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "archive batch").returncode == 0

    seal_after_proc, seal_after = _run(repo, "seal")
    assert seal_after_proc.returncode == seal_proc.returncode
    assert seal_after["verdict"] == seal_before["verdict"]
    assert _seal_facets(seal_after) == _seal_facets(seal_before), (
        "C-107: the archive never rewrites the seal blocking list"
    )
    assert (repo / MANIFEST_REL).is_file()
    assert not (repo / SPEC_REL / "seal.md").exists(), (
        "the archive record and the seal receipt are separate surfaces: archive-apply "
        "never creates or overwrites the receipt"
    )


def test_merge_refusal_does_not_start_archive(tmp_path):
    """C-102: a refused merge-apply leaves no settled state for the archive."""
    repo = _prepare_replay(tmp_path)
    beta_requirements = repo / ".specify/specs" / BETA / "requirements.md"
    text = beta_requirements.read_text(encoding="utf-8")
    assert "| FR-001 | FR-002 |" in text, (
        "the fixture baseline maps beta's FR-001 to parent FR-002"
    )
    beta_requirements.write_text(
        text.replace("| FR-001 | FR-002 |", "| FR-001 | FR-001 |"), encoding="utf-8")
    _git(repo, "add", "-A")
    assert _git(repo, "commit", "-qm", "both slices claim parent FR-001").returncode == 0

    merge_proc, merge_payload = _run(repo, "merge-apply")
    assert merge_proc.returncode == 1, merge_payload.get("conditions")
    assert "duplicate-mapping" in _codes(merge_payload), (
        "the upstream refusal is the duplicate parent claim this replay injects"
    )
    before = _snapshot(repo)

    plan_proc, plan_payload = _run(repo, "archive-plan")
    assert plan_proc.returncode == 2, plan_payload.get("conditions")
    assert "merge-manifest-missing" in _codes(plan_payload), (
        "C-102 ①: with no settled merge record the archive names the upstream block"
    )
    apply_proc, apply_payload = _run(repo, "archive-apply")
    assert apply_proc.returncode == 2, apply_payload.get("conditions")
    assert "merge-manifest-missing" in _codes(apply_payload)
    assert not (repo / MANIFEST_REL).exists()
    assert not (repo / SPEC_REL / "slices").exists(), (
        "SC-004: a refused merge never starts the archive"
    )
    assert _snapshot(repo) == before, "a refused archive persists nothing"
