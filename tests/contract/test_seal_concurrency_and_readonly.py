"""Contract tests for seal concurrency and read-only measurement (Feature 099, P5).

Contract: ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
Clauses:  C-037 (parallel writers touch disjoint paths; no lock file),
          C-039 (``dirty-spec-tree`` names the path it refuses on) and
          C-040 (review records and slice measurement files stay read-only).

Fixture trees: ``tests/fixtures/seal/single-spec/`` (duplicated into two sibling
specs for the parallel-writer leg) and ``tests/fixtures/seal/merged-clean/``
(a merged parent whose slice carries dated measurement files).

Red-first: this file landed before the ``seal`` action body existed; the red
reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal"

CLEAN = "099-fixture-clean"
MERGED = "099-fixture-merged"
SLICE = "099a-fixture-slice"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    argv = ["git", "-C", str(repo),
            "-c", "user.name=seal-fixture",
            "-c", "user.email=seal-fixture@example.com",
            "-c", "commit.gpgsign=false",
            "-c", "init.defaultBranch=main"] + list(args)
    return subprocess.run(argv, capture_output=True, text=True, check=True)


def _commit(repo: Path, message: str = "fixture baseline") -> str:
    if not (repo / ".git").is_dir():
        _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _seal_argv(repo: Path, spec_slug: str) -> list:
    return [sys.executable, str(ENGINE), "--action", "seal",
            "--spec-dir", str(repo / ".specify" / "specs" / spec_slug),
            "--repo", str(repo), "--json"]


def _seal(repo: Path, spec_slug: str) -> tuple:
    proc = subprocess.run(_seal_argv(repo, spec_slug), cwd=str(repo),
                          capture_output=True, text=True, encoding="utf-8",
                          check=False)
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}")
    return proc, json.loads(proc.stdout)


def _snapshot(root: Path, skip_dirs=()) -> dict:
    skip = {tuple(path.resolve().parts) for path in skip_dirs}
    entries = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = path.resolve().parts
        if ".git" in path.parts or any(parts[:len(item)] == item for item in skip):
            continue
        entries[str(path.relative_to(root))] = hashlib.sha256(
            path.read_bytes()).hexdigest()
    return entries


def _hashes(root: Path, names) -> dict:
    return {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in names
    }


def _receipt_core(spec_dir: Path) -> dict:
    text = (spec_dir / "seal.md").read_text(encoding="utf-8")
    block = re.search(r"```json\n(.*?)\n```", text, re.S)
    assert block is not None, "C-032: seal.md carries one machine-readable core block"
    return json.loads(block.group(1))


# ---------------------------------------------------------------------------
# C-037 — two parallel writers, disjoint paths, no shared aggregate
# ---------------------------------------------------------------------------

def test_parallel_seals_write_disjoint_paths(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURES / "single-spec", repo)
    specs = repo / ".specify" / "specs"
    base = specs / CLEAN
    writers = []
    for suffix in ("a", "b"):
        slug = "099-fixture-clean-%s" % suffix
        target = specs / slug
        shutil.copytree(base, target)
        for path in target.rglob("*"):
            if path.is_file():
                path.write_text(
                    path.read_text(encoding="utf-8").replace(CLEAN, slug),
                    encoding="utf-8")
        writers.append(slug)
    shutil.rmtree(base)
    _commit(repo)
    spec_dirs = [specs / slug for slug in writers]
    before = _snapshot(repo, skip_dirs=spec_dirs)

    processes = [
        subprocess.Popen(_seal_argv(repo, slug), cwd=str(repo),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8")
        for slug in writers
    ]
    outputs = [process.communicate() for process in processes]
    for process, (stdout, stderr) in zip(processes, outputs):
        assert process.returncode == 0, (
            "C-037: two seals of different specs MUST both succeed; "
            f"exit={process.returncode} stderr={stderr[-500:]!r}")
        assert json.loads(stdout)["seal"]["outcome"] == "sealed"

    after = _snapshot(repo, skip_dirs=spec_dirs)
    assert after == before, (
        "C-037: the writes land only inside each spec directory; no shared mutable "
        "aggregate and no lock file appears elsewhere")

    receipts = [_receipt_core(specs / slug) for slug in writers]
    for slug, core in zip(writers, receipts):
        assert slug in core["engine"]["command"], (
            "C-037: each writer records its own target path")
    assert receipts[0]["engine"]["command"] != receipts[1]["engine"]["command"], (
        "the two receipts are distinct files with distinct provenance")


# ---------------------------------------------------------------------------
# C-040 — review records and slice measurements stay byte-identical
# ---------------------------------------------------------------------------

def test_review_and_measurement_files_stay_byte_identical(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURES / "merged-clean", repo)
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / MERGED
    slice_dir = repo / ".specify" / "specs" / SLICE
    watched = {
        spec_dir: ("review.md", "code-review.md", "merge-manifest.json"),
        slice_dir: (
            "review.md",
            "verification.md",
            "test-evidence/run-2026-11-05.txt",
        ),
    }
    before = {str(root): _hashes(root, names) for root, names in watched.items()}
    proc, payload = _seal(repo, MERGED)
    assert proc.returncode == 0, (
        f"the merged fixture MUST seal; exit={proc.returncode} payload={payload}")
    after = {str(root): _hashes(root, names) for root, names in watched.items()}
    assert after == before, (
        "C-040: seal reads review records and slice measurements; it never rewrites "
        "or re-verdicts them")


# ---------------------------------------------------------------------------
# C-039 — dirty spec tree refuses and names the path
# ---------------------------------------------------------------------------

def test_dirty_spec_tree_refuses_and_names_the_path(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURES / "seal-refusals" / "dirty-spec-tree", repo)
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / CLEAN
    plan = spec_dir / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\nAn uncommitted local edit.\n",
                    encoding="utf-8")
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1, (
        "C-039: an uncommitted change under the parent spec tree MUST refuse the seal")
    conditions = [item for item in payload["conditions"]
                  if item["code"] == "dirty-spec-tree"]
    assert conditions, (
        f"C-039: the refusal is named dirty-spec-tree; got "
        f"{sorted({item['code'] for item in payload['conditions']})}")
    assert ".specify/specs/%s/plan.md" % CLEAN in conditions[0]["evidence"], (
        "C-039: the refusal names the offending path")
    assert not (spec_dir / "seal.md").exists(), "C-039: nothing is stamped on a moving tree"
