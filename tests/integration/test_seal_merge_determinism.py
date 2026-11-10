"""Integration tests for ``merge-apply`` determinism (Feature 099, work package P4).

Contract: ``.specify/specs/099-speckit-seal/contracts/merge-back.contract.md``
Clauses:  C-014 / C-023 — the same input MUST produce byte-identical merged
          artifacts and manifest; a successful ``merge-apply`` rerun MUST be a
          zero-diff idempotent no-op; any decision that reads the return time,
          the directory enumeration order or a random source MUST turn the
          determinism comparison red.

Red-first: this file landed before the ``merge-apply`` body existed; the red
reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal"
PARENT = "099-fixture-parent"


def _copy_fixture(target: Path) -> Path:
    source = FIXTURES / "split-pair"
    assert source.is_dir(), (
        f"fixture tree missing: {source} — this is the expected red-first reading "
        "for T022 before the apply work package lands"
    )
    shutil.copytree(source, target)
    return target


def _spec(repo: Path) -> Path:
    return repo / ".specify" / "specs" / PARENT


def _run_apply(repo: Path):
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "merge-apply",
         "--spec-dir", str(_spec(repo)), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _snapshot(root: Path) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def _load_engine():
    assert ENGINE.is_file(), (
        "engine missing: scripts/python/seal-utils.py has not landed; this is the "
        "expected red-first reading for T022"
    )
    spec = importlib.util.spec_from_file_location("seal_utils_determinism", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _run_engine_in_process(module, repo: Path) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = module.main([
            "--action", "merge-apply",
            "--spec-dir", str(_spec(repo)),
            "--repo", str(repo),
            "--json",
        ])
    output = buffer.getvalue()
    assert code == 0, f"in-process apply exited {code}: {output[-800:]!r}"
    return output


# ---------------------------------------------------------------------------
# C-014 — two fresh runs agree byte for byte
# ---------------------------------------------------------------------------

def test_two_fresh_runs_are_byte_identical(tmp_path):
    first = _copy_fixture(tmp_path / "first")
    second = _copy_fixture(tmp_path / "second")
    proc_a, payload_a = _run_apply(first)
    proc_b, payload_b = _run_apply(second)
    assert proc_a.returncode == proc_b.returncode == 0
    assert payload_a["verdict"] == payload_b["verdict"] == "ok"
    names_a = _snapshot(first)
    names_b = _snapshot(second)
    assert names_a == names_b, (
        "C-014: the same input MUST produce byte-identical merged artifacts and "
        "manifest — including file names and sha256 values"
    )


# ---------------------------------------------------------------------------
# C-014 — a successful rerun is an idempotent zero-diff no-op
# ---------------------------------------------------------------------------

def test_rerun_in_place_is_zero_diff(tmp_path):
    repo = _copy_fixture(tmp_path / "repo")
    first_proc, first_payload = _run_apply(repo)
    assert first_proc.returncode == 0
    assert first_payload["apply"]["idempotent"] is False
    after_first = _snapshot(repo)
    manifest_path = _spec(repo) / "merge-manifest.json"
    manifest_bytes = manifest_path.read_bytes()

    second_proc, second_payload = _run_apply(repo)
    assert second_proc.returncode == 0, (
        "FR-013: a successful merge-apply rerun is an idempotent success"
    )
    assert second_payload["verdict"] == "ok"
    assert second_payload["apply"]["idempotent"] is True
    assert second_payload["apply"]["writes"] == []
    assert manifest_path.read_bytes() == manifest_bytes, (
        "C-014: the rerun MUST NOT rewrite the manifest (zero diff)"
    )
    assert _snapshot(repo) == after_first, (
        "SC-003: a rerun after a successful merge-apply MUST produce zero diff"
    )


# ---------------------------------------------------------------------------
# C-014 — a return-time-derived ordering key turns the check red
# ---------------------------------------------------------------------------

def test_return_time_sort_key_mutation_turns_the_comparison_red(tmp_path, monkeypatch):
    """Inject the canonical mutation: an ordering key that reads the return time.

    The comparison used by the determinism tests is the per-file sha256 map. If a
    sort key were replaced with ``time.time()``, two runs would disagree; this
    test proves the comparison reports that disagreement (i.e. the guard is not
    vacuous), rather than only asserting that today's engine is deterministic.
    """
    module = _load_engine()
    real_classify = module._classify_artifacts

    def time_keyed(repo, spec_dir, slices):
        rows = real_classify(repo, spec_dir, slices)
        stamp = time.time()
        for row in rows:
            row["order_stamp"] = stamp
        return sorted(rows, key=lambda row: row["order_stamp"])

    monkeypatch.setattr(module, "_classify_artifacts", time_keyed)

    first = _copy_fixture(tmp_path / "first")
    _run_engine_in_process(module, first)
    time.sleep(0.02)
    second = _copy_fixture(tmp_path / "second")
    _run_engine_in_process(module, second)

    assert _snapshot(first) != _snapshot(second), (
        "SC-003: a sort key that reads the return time MUST turn the determinism "
        "comparison red; the comparison reported equality, so it is vacuous"
    )

    # sanity: the same shake-up with a fixed key is still deterministic
    monkeypatch.setattr(module, "_classify_artifacts", real_classify)
    third = _copy_fixture(tmp_path / "third")
    fourth = _copy_fixture(tmp_path / "fourth")
    _run_engine_in_process(module, third)
    _run_engine_in_process(module, fourth)
    assert _snapshot(third) == _snapshot(fourth), (
        "the unmutated engine MUST stay byte-identical across runs"
    )
