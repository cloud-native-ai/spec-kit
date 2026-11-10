"""Contract tests for the seal engine's ``seal`` action (Feature 099, work package P5).

Contract: ``.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md``
          ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
Clauses:  C-005 … C-010, C-032 … C-034, C-038, C-042, C-044 — the two-phase
          judgment/write split, the flat refusal report with the closed code set,
          ``already-sealed`` idempotence, the closed ``seal.md`` field set, the
          ``supersedes`` replacement, atomic batch restore, and the P0 disposition
          form (a resolvable ``- **Fix**:`` pointer or a user waiver on BOTH
          carriers).

Fixture trees: ``tests/fixtures/seal/single-spec/`` (clean, zero slices),
``tests/fixtures/seal/merged-clean/`` (one slice already merged back) and
``tests/fixtures/seal/seal-refusals/`` (one injected defect per case).

Red-first: this file landed before the ``seal`` action body existed; the red
reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
CLOSURE = REPO_ROOT / "scripts" / "python" / "closure-acceptance-check.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal"

CLEAN = "099-fixture-clean"
MERGED = "099-fixture-merged"
SLICE = "099a-fixture-slice"

RECEIPT_KEYS = {
    "judged_at", "pinned_commit", "from_status", "to_status", "review",
    "closure", "merge", "waivers", "engine",
}
FINAL_PATH_KEYS = {"pass", "blocked", "deferred", "partial", "fail", "unknown", "total"}
REVIEW_COUNT_KEYS = {"p0_unresolved", "p1", "p2", "blocking"}

#: (fixture case, spec slug it targets, expected named code, expected process exit)
REFUSALS = (
    ("from-status-invalid", CLEAN, "from-status-invalid", 1),
    ("p0-unresolved", CLEAN, "p0-unresolved", 1),
    ("closure-refused", CLEAN, "closure-refused", 1),
    ("closure-input-defect", CLEAN, "closure-input-defect", 2),
    ("conflict-open", MERGED, "conflict-open", 1),
    ("slice-unclosed", CLEAN, "slice-unclosed", 1),
    ("three-minus-one", CLEAN, "closure-refused", 1),
    ("state-drift", CLEAN, "state-drift", 2),
)

USER_WAIVER = "- **User waiver**: F1 — user ruling recorded by the fixture run."


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _copy_fixture(name: str, target: Path) -> Path:
    source = FIXTURES / name
    assert source.is_dir(), f"fixture tree missing: {source}"
    shutil.copytree(source, target)
    return target


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


def _seal(repo: Path, spec_slug: str) -> tuple:
    spec_dir = repo / ".specify" / "specs" / spec_slug
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "seal", "--spec-dir", str(spec_dir),
         "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _closure_accept(repo: Path, spec_slug: str) -> dict:
    spec_dir = repo / ".specify" / "specs" / spec_slug
    proc = subprocess.run(
        [sys.executable, str(CLOSURE), "--spec-dir", str(spec_dir), "--repo", str(repo),
         "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.returncode == 0, f"fixture must stay closure-accepting: {proc.stdout}"
    return json.loads(proc.stdout)


def _snapshot(root: Path) -> dict:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }


def _receipt_core(spec_dir: Path) -> dict:
    text = (spec_dir / "seal.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    assert len(blocks) == 1, (
        f"C-032: seal.md carries exactly one machine-readable core block; got {len(blocks)}"
    )
    return json.loads(blocks[0])


def _status_pair(spec_dir: Path) -> tuple:
    detail = next(
        line for line in (spec_dir / "feature-detail.md").read_text(
            encoding="utf-8").splitlines() if line.startswith("**Status**:"))
    registry_row = next(
        line for line in (spec_dir / "feature-registry.md").read_text(
            encoding="utf-8").splitlines()
        if line.startswith("| 099 |"))
    cells = [cell.strip() for cell in registry_row.strip().strip("|").split("|")]
    return detail.split(":", 1)[1].strip(), cells[3], cells[6]


def _context_codes(payload: dict) -> set:
    return {condition["code"] for condition in payload["conditions"]}


def _write_p0(repo: Path, spec_slug: str, waiver_carrier: str = "") -> None:
    """Inject one P0 finding; ``waiver_carrier`` is '', 'detail', 'review' or 'both'.

    Idempotent on every carrier: repeated calls never duplicate the finding or a
    waiver line, so the sequence '' -> 'detail' -> 'review' isolates one carrier at
    a time.
    """
    spec_dir = repo / ".specify" / "specs" / spec_slug
    review = spec_dir / "review.md"
    text = review.read_text(encoding="utf-8")
    text = text.replace("| P0 | 0 |", "| P0 | 1 |")
    if "### F1 —" not in text:
        text = text.rstrip("\n") + (
            "\n\n### F1 — A P0 finding raised by the mutation run\n\n"
            "- **Severity**: P0\n"
            "- **Category**: Workflow\n"
            "- **Why it's a problem**: the mutation needs one P0 with a controllable "
            "disposition.\n"
            "- **Waiver**: 显式豁免（P0 waiver）— the driver confirmed; this narrative "
            "never counts.\n"
        )
    if waiver_carrier in ("review", "both") and USER_WAIVER not in text:
        text = text.replace(
            "\n## 3. Findings", "\n" + USER_WAIVER + "\n\n## 3. Findings", 1)
    review.write_text(text, encoding="utf-8")
    if waiver_carrier in ("detail", "both"):
        detail = spec_dir / "feature-detail.md"
        detail_text = detail.read_text(encoding="utf-8")
        if USER_WAIVER not in detail_text:
            detail_text = detail_text.rstrip("\n") + "\n" + USER_WAIVER + "\n"
        detail.write_text(detail_text, encoding="utf-8")


# ---------------------------------------------------------------------------
# C-005 / C-032 / C-033 — the success path and the receipt
# ---------------------------------------------------------------------------

def test_clean_single_spec_seals_and_writes_the_three_surfaces(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    head = _commit(repo)
    closure = _closure_accept(repo, CLEAN)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 0, (
        f"a clean Ready-for-Review spec MUST seal; exit={proc.returncode} "
        f"payload={json.dumps(payload, ensure_ascii=False)[:900]}"
    )
    assert payload["verdict"] == "ok"
    assert payload["seal"]["outcome"] == "sealed"
    assert payload["seal"]["writes"]

    spec_dir = repo / ".specify" / "specs" / CLEAN
    assert (spec_dir / "seal.md").is_file(), "C-032: seal.md lands in the parent spec dir"
    core = _receipt_core(spec_dir)
    assert set(core) == RECEIPT_KEYS, (
        f"C-032/V5: the receipt field set is closed; measured {sorted(core)}"
    )
    assert core["from_status"] == "Ready for Review" and core["to_status"] == "Sealed"
    assert core["pinned_commit"] == head, (
        "the receipt pins the commit the judgment read (git rev-parse HEAD)")
    assert core["review"]["paths"] == [
        ".specify/specs/%s/review.md" % CLEAN,
        ".specify/specs/%s/code-review.md" % CLEAN,
    ], "FR-010: the receipt references the current review records"
    assert set(core["review"]["counts"]) == REVIEW_COUNT_KEYS
    assert core["review"]["counts"] == {
        "p0_unresolved": 0, "p1": 1, "p2": 0, "blocking": 0}
    assert core["closure"]["exit_code"] == 0
    assert core["closure"]["final_path"] == closure["final_path"], (
        "FR-007/E9: the closure receipt is copied verbatim from the closure engine")
    assert set(core["closure"]["final_path"]) == FINAL_PATH_KEYS, (
        "E9: the seven-key final_path record is copied unchanged")
    assert "closure-acceptance-check.py" in core["closure"]["command"]
    assert core["merge"] == {
        "manifest": None,
        "slices": [],
        "status": "not-applicable",
        "basis": core["merge"]["basis"],
    }, "FR-008: an empty slice set is recorded as not-applicable with its basis"
    assert core["merge"]["basis"].strip(), "FR-008: the basis is stated, never implied"
    assert core["waivers"] == []
    assert core["engine"]["identity"] == "seal-utils.py"
    assert core["engine"]["version"].strip()
    assert "--action seal" in core["engine"]["command"]
    assert "supersedes" not in core, "C-033: supersedes appears only on a re-seal"

    detail, registry_status, updated = _status_pair(spec_dir)
    assert detail == registry_status == "Sealed", (
        "C-005/E10: the registry row and the detail flip to Sealed in the same batch")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated), (
        "E10: Last Updated carries the judgment date")
    detail_text = (spec_dir / "feature-detail.md").read_text(encoding="utf-8")
    assert "Sealed by /speckit.seal" in detail_text, (
        "E10: exactly one sealing entry is appended under ## Latest Review")


def test_merged_spec_seals_with_a_complete_manifest(tmp_path):
    repo = _copy_fixture("merged-clean", tmp_path / "repo")
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / MERGED
    manifest_before = (spec_dir / "merge-manifest.json").read_bytes()
    proc, payload = _seal(repo, MERGED)
    assert proc.returncode == 0, (
        f"a merged spec MUST seal when the manifest is complete; exit={proc.returncode} "
        f"payload={json.dumps(payload, ensure_ascii=False)[:900]}"
    )
    core = _receipt_core(spec_dir)
    assert core["merge"]["status"] == "merged"
    assert core["merge"]["slices"] == [SLICE]
    assert core["merge"]["manifest"] == ".specify/specs/%s/merge-manifest.json" % MERGED
    assert "basis" not in core["merge"], "the basis key belongs to not-applicable only"
    assert (spec_dir / "merge-manifest.json").read_bytes() == manifest_before, (
        "C-032/C-034: seal references the manifest and never rewrites it")


def test_reseal_is_idempotent_already_sealed(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / CLEAN
    first, _payload = _seal(repo, CLEAN)
    assert first.returncode == 0
    receipt = (spec_dir / "seal.md").read_bytes()
    pair = _status_pair(spec_dir)
    second, payload = _seal(repo, CLEAN)
    assert second.returncode == 0, "C-007: already-sealed is a success, not a refusal"
    assert payload["verdict"] == "ok"
    assert payload["seal"]["outcome"] == "already-sealed"
    assert payload["seal"]["writes"] == []
    assert (spec_dir / "seal.md").read_bytes() == receipt, (
        "C-007: no second receipt and no rewrite of the current one")
    assert _status_pair(spec_dir) == pair, "C-007: the status faces stay untouched"


def test_supersedes_is_recorded_when_the_receipt_is_replaced(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / CLEAN
    first, _payload = _seal(repo, CLEAN)
    assert first.returncode == 0
    pinned = _receipt_core(spec_dir)["pinned_commit"]
    _commit(repo, "seal receipt")

    for name in ("feature-detail.md", "feature-registry.md"):
        path = spec_dir / name
        path.write_text(
            path.read_text(encoding="utf-8").replace("Sealed", "Ready for Review", 1),
            encoding="utf-8")
    _commit(repo, "audit correction")

    second, payload = _seal(repo, CLEAN)
    assert second.returncode == 0, (
        "C-033: the only backward transition re-enables a replace")
    assert payload["seal"]["outcome"] == "sealed"
    core = _receipt_core(spec_dir)
    assert core["supersedes"] == pinned, (
        "C-033: the machine core names the superseded receipt's pinned commit")
    assert _status_pair(spec_dir)[:2] == ("Sealed", "Sealed")
    assert (spec_dir / "seal.md").read_text(encoding="utf-8").count("```json") == 1, (
        "C-033: one current receipt, never an appended history")


# ---------------------------------------------------------------------------
# C-006 / C-042 — the refusal matrix: every condition named, nothing persisted
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case,slug,code,exit_code", REFUSALS)
def test_refusal_fixtures_name_the_closed_codes_and_persist_nothing(
        case, slug, code, exit_code, tmp_path):
    repo = _copy_fixture("seal-refusals/%s" % case, tmp_path / case / "repo")
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / slug
    before = _snapshot(repo / ".specify" / "specs")
    proc, payload = _seal(repo, slug)
    assert proc.returncode == exit_code, (
        f"C-042: {case} exits {exit_code}; got {proc.returncode}; "
        f"payload={json.dumps(payload, ensure_ascii=False)[:900]}")
    assert payload["exit_code"] == exit_code
    assert payload["verdict"] == ("error" if exit_code == 2 else "refused")
    assert code in _context_codes(payload), (
        f"C-042: {case} MUST be named {code!r}; got {sorted(_context_codes(payload))}")
    for condition in payload["conditions"]:
        assert condition["code"] and condition["evidence"]
        assert condition["fix_path"] and condition["rerun"], (
            "C-006: every unmet condition carries its fix path and rerun form")
    after = _snapshot(repo / ".specify" / "specs")
    assert after == before, (
        f"C-006: a refusal of {case} MUST NOT write anything (state unchanged)")
    assert not (spec_dir / "seal.md").exists(), "C-006: no receipt on refusal"


def test_slice_unclosed_also_names_the_missing_merge_record(tmp_path):
    repo = _copy_fixture("seal-refusals/slice-unclosed", tmp_path / "repo")
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    codes = _context_codes(payload)
    assert "slice-unclosed" in codes, "FR-008: the unclosed slice is named"
    assert "merge-incomplete" in codes, (
        "C-006: every unmet condition is named together, not only the first")


def test_refusal_report_is_rerun_stable(tmp_path):
    repo = _copy_fixture("seal-refusals/closure-refused", tmp_path / "repo")
    _commit(repo)
    first, _ = _seal(repo, CLEAN)
    second, _payload = _seal(repo, CLEAN)
    assert first.returncode == second.returncode == 1
    assert first.stdout == second.stdout, (
        "C-006/C-038: the same input reproduces the same report, byte for byte")


def test_code_review_blocking_entry_refuses(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    spec_dir = repo / ".specify" / "specs" / CLEAN
    code_review = spec_dir / "code-review.md"
    code_review.write_text(
        code_review.read_text(encoding="utf-8")
        + "\n### 🔴 [BLOCKING] .specify/specs/099-fixture-clean/plan.md (Line 5)\n\n"
          "> The fixture injects one blocking entry.\n",
        encoding="utf-8")
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    assert "code-review-blocking" in _context_codes(payload)


def test_missing_review_record_refuses(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    (repo / ".specify" / "specs" / CLEAN / "review.md").unlink()
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    assert "review-missing" in _context_codes(payload), (
        "FR-006: a missing current review record is named, pointing at /speckit.review")


def test_a_slice_directory_is_never_the_seal_subject(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    requirements = repo / ".specify" / "specs" / CLEAN / "requirements.md"
    requirements.write_text(
        requirements.read_text(encoding="utf-8")
        + "\n**Parent spec**: `099-fixture-clean-parent`\n", encoding="utf-8")
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    assert "slice-not-sealable" in _context_codes(payload), (
        "FR-005: a slice is refused and its parent named as the correct target")


# ---------------------------------------------------------------------------
# C-044 — P0 disposition: fix pointer or user waiver on BOTH carriers
# ---------------------------------------------------------------------------

def test_user_waiver_needs_both_carriers(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _write_p0(repo, CLEAN, waiver_carrier="")
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    assert "p0-unresolved" in _context_codes(payload), (
        "C-044: a driver-recorded waiver narrative never disposes of a P0")

    _write_p0(repo, CLEAN, waiver_carrier="detail")
    _commit(repo, "detail-only waiver")
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 1
    assert "p0-unresolved" in _context_codes(payload), (
        "C-044: a single carrier never counts as the user's waiver")

    _write_p0(repo, CLEAN, waiver_carrier="review")
    _commit(repo, "the second carrier")
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 0, (
        "C-044: the literal `- **User waiver**:` line on BOTH carriers disposes of the P0")
    core = _receipt_core(repo / ".specify" / "specs" / CLEAN)
    assert core["review"]["counts"]["p0_unresolved"] == 0
    assert [entry["finding"] for entry in core["waivers"]] == ["F1"]
    assert core["waivers"][0]["form"] == "user-waiver"
    assert "review.md" in core["waivers"][0]["source"]
    assert "feature-detail.md" in core["waivers"][0]["source"]


# ---------------------------------------------------------------------------
# C-005 — atomic batch: a failed write restores every byte it wrote
# ---------------------------------------------------------------------------

@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permission bits")
def test_write_failure_restores_the_batch(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _commit(repo)
    spec_dir = repo / ".specify" / "specs" / CLEAN
    detail = spec_dir / "feature-detail.md"
    registry = spec_dir / "feature-registry.md"
    registry_before = registry.read_bytes()
    detail.chmod(0o444)
    try:
        proc, payload = _seal(repo, CLEAN)
    finally:
        detail.chmod(0o644)
    assert proc.returncode == 2, (
        "C-005/C-038: a write failure ends at exit 2, never a half-sealed state")
    assert payload["verdict"] == "error"
    assert "seal-write-failed" in _context_codes(payload)
    assert registry.read_bytes() == registry_before, (
        "C-005: the already-written registry file is restored byte for byte")
    assert not (spec_dir / "seal.md").exists(), (
        "C-005: the receipt write is the last step, so a failure leaves no receipt")


def test_closure_input_defect_is_not_read_as_accept(tmp_path):
    repo = _copy_fixture("seal-refusals/closure-input-defect", tmp_path / "repo")
    _commit(repo)
    proc, payload = _seal(repo, CLEAN)
    assert proc.returncode == 2, (
        "FR-007/DoD-5: a closure-engine input defect (exit 2) is reported as exit 2, "
        "never read as accept")
    assert payload["verdict"] == "error"
    assert "closure-input-defect" in _context_codes(payload)
