"""Integration tests for the real 074 split → merge-back → seal round (Feature 099, P8).

Contract: ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
Clauses:  C-043 — the round's adjudication is reproducible: the merge manifest, the
          seal receipt or refusal list and the front-end status agree; a rerun in
          the blocked state MUST reproduce the same list, never a different verdict.

Scope: read-only. The test drives ``merge-plan`` (a zero-write action) against the
real ``.specify/specs/074-goal-team-sdd-unification/`` tree and reads the round's
recorded evidence. It MUST NOT write into the 074 tree; the git-status comparison
below turns a write into a red assertion.

The C-112 equivalence leg replays the round on a temporary copy of the parent and
both slices (``git init`` + commits), moves the slices into ``slices/`` there and
writes the archive record in place. The live 074 tree is still never touched.

Evidence the round produced (captured by T039/T041/T043):

* ``test-evidence/074-merge-plan-before.json`` — the pre-fix plan, whose
  ``conflicts[]`` names the ``factory-doc-ref-ambiguous`` class 36 times.
* ``test-evidence/074-merge-plan-after.json`` — the post-fix plan (0 open conflicts).
* ``test-evidence/074-round-20261110.txt`` — the pre-fix round's adjudication,
  kept unchanged as the before snapshot of the P8b rerun.
* ``test-evidence/074-round-rerun-20261111.txt`` — the rerun on the repaired
  engine: two seal runs, the same refusal list, the FR-027 floor covered.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
EVIDENCE = REPO_ROOT / ".specify" / "specs" / "099-speckit-seal" / "test-evidence"
PARENT = REPO_ROOT / ".specify" / "specs" / "074-goal-team-sdd-unification"
SLICE_A = "074a-authorized-routing"
SLICE_B = "074b-nested-governance"
ROUND_EVIDENCE = EVIDENCE / "074-round-rerun-20261111.txt"

#: The declared mappings the round MUST honour (074a / 074b `## Parent Mapping`).
DECLARED_STR_MAPPINGS = {
    (SLICE_A, "STR-010"): "STR-011",
    (SLICE_B, "STR-004"): "STR-007",
    (SLICE_B, "STR-005"): "STR-008",
    (SLICE_B, "STR-006"): "STR-009",
    (SLICE_B, "STR-007"): "STR-010",
}


def _git_status_074() -> str:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--", str(PARENT)],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.returncode == 0, f"git status failed: {proc.stderr[-400:]!r}"
    return proc.stdout


def _run_plan() -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "merge-plan",
         "--spec-dir", str(PARENT), "--repo", str(REPO_ROOT), "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8",
        check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# The live, read-only merge-plan face
# ---------------------------------------------------------------------------


def test_live_plan_identifies_both_slices_from_the_split_record():
    proc, payload = _run_plan()
    plan = payload["plan"]
    assert proc.returncode == 0, (
        "the settled round must leave a conflict-free plan; exit=%d payload=%r"
        % (proc.returncode, payload.get("conditions"))
    )
    slices = plan["slices"]
    assert [item["slug"] for item in slices] == [SLICE_A, SLICE_B], (
        "C-012: the split record's declared order (074a → 074b) decides the order"
    )
    assert [item["order"] for item in slices] == [1, 2]
    assert {item["order_basis"] for item in slices} == {"split-record"}, (
        "C-012: the order MUST be taken from `.specify/state/074-*.md` § 拆分记录"
    )
    assert plan["checks"]["open_conflicts"] == 0, (
        "the round's disposed conflicts must not reappear: %r"
        % payload.get("conditions")
    )


def test_declared_str_mappings_are_honoured_in_the_id_maps():
    _proc, payload = _run_plan()
    str_entries = {
        (entry["slice"], entry["slice_id"]): entry["parent_id"]
        for entry in payload["plan"]["id_maps"]["STR"]
    }
    for key, parent_id in DECLARED_STR_MAPPINGS.items():
        assert str_entries.get(key) == parent_id, (
            "C-016: the slice's declared `## Parent Mapping` decides the target; "
            f"{key} must map to {parent_id}, got {str_entries.get(key)!r}"
        )


def test_the_round_named_the_factory_doc_conflict_class_it_disposed():
    before_path = EVIDENCE / "074-merge-plan-before.json"
    assert before_path.is_file(), (
        "T039's pre-fix capture is part of the round record; it is what names the "
        "conflict classes before disposal"
    )
    before = json.loads(before_path.read_text(encoding="utf-8"))
    conflicts = before["plan"]["conflicts"]
    ambiguous = [c for c in conflicts if c["code"] == "factory-doc-ref-ambiguous"]
    assert len(ambiguous) == 36, (
        "the pre-fix plan names 36 factory-doc-ref-ambiguous records "
        "(18 source references × source/mirror scan); got %d" % len(ambiguous)
    )
    units = {c["unit"] for c in ambiguous}
    assert {"STR-004", "STR-005", "STR-006", "STR-007"} <= units, (
        "the two same-number groups the round disposes MUST be named by id: %r" % units
    )


# ---------------------------------------------------------------------------
# Blocked-state rerun consistency (C-043)
# ---------------------------------------------------------------------------


def _adjudication_blocks(text: str) -> list[dict]:
    """The two recorded seal runs, split on the round's own run separators."""
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("=== RUN "):
            if current is not None:
                blocks.append(current)
            current = {"header": line, "lines": []}
            continue
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        blocks.append(current)
    return blocks


def test_blocked_state_rerun_is_identical_and_names_the_same_verdict():
    assert ROUND_EVIDENCE.is_file(), (
        "the blocked round's adjudication is carried by "
        "`test-evidence/074-round-rerun-20261111.txt` (P8b rerun; the pre-fix "
        "round stays as `074-round-20261110.txt`)"
    )
    blocks = _adjudication_blocks(ROUND_EVIDENCE.read_text(encoding="utf-8"))
    assert len(blocks) == 2, (
        "T043 records exactly two seal runs (verdict + reproducibility rerun); "
        "found %d" % len(blocks)
    )
    first = [line for line in blocks[0]["lines"] if line.strip()]
    second = [line for line in blocks[1]["lines"] if line.strip()]
    assert first == second, (
        "C-043: a rerun in the blocked state MUST reproduce the same refusal list"
    )
    body = "\n".join(first)
    assert "closure-input-defect" in body, (
        "the round's recorded refusal names the closure input defect it found"
    )
    for item in ("FR-027(a)", "FR-027(b)", "FR-027(c)", "FR-027(d)", "FR-027(e)"):
        assert item in body, (
            "SC-006: the refusal list covers the FR-027 floor item by item; "
            f"{item} is not named"
        )


# ---------------------------------------------------------------------------
# Read-only: the test never rewrites the 074 tree
# ---------------------------------------------------------------------------


def test_the_round_probe_writes_nothing_into_the_074_tree():
    before = _git_status_074()
    _run_plan()
    after = _git_status_074()
    assert before == after, (
        "T042: this test MUST NOT rewrite the 074 tree; git status changed from "
        f"{before!r} to {after!r}"
    )


# ---------------------------------------------------------------------------
# C-112 — the archived round is the same round (T035 replay)
# ---------------------------------------------------------------------------

PARENT_REL = ".specify/specs/074-goal-team-sdd-unification"
DETAIL = REPO_ROOT / ".specify" / "features" / "074-goal-team-sdd-unification.md"
REGISTRY = REPO_ROOT / ".specify" / "features.md"
GIT_IDENTITY = ["-c", "user.email=seal-test@example.com", "-c", "user.name=seal-test"]


def _git(repo: Path, *arguments: str) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", "-C", str(repo)] + list(arguments),
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.returncode == 0, (
        "git %s failed: %r" % (" ".join(arguments), proc.stderr[-400:])
    )
    return proc


def _commit(repo: Path, message: str) -> None:
    _git(repo, *GIT_IDENTITY, "add", "-A")
    _git(repo, *GIT_IDENTITY, "commit", "-q", "-m", message)


def _replay_tree(tmp_path: Path) -> Path:
    """A throwaway git replay of the 074 round (parent + both slices)."""
    repo = tmp_path / "replay"
    specs = repo / ".specify" / "specs"
    specs.mkdir(parents=True)
    for name in (PARENT.name, SLICE_A, SLICE_B):
        shutil.copytree(REPO_ROOT / ".specify" / "specs" / name, specs / name)
    _git(repo, "init", "-q")
    _commit(repo, "074 replay snapshot")
    return repo


def _run_action(repo: Path, action: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", action,
         "--spec-dir", str(repo / PARENT_REL), "--repo", str(repo),
         "--feature-detail", str(DETAIL), "--feature-registry", str(REGISTRY),
         "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload for {action}; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _slice_file_rows(slice_dir: Path) -> list:
    return [
        {"path": path.relative_to(slice_dir).as_posix(),
         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(slice_dir.rglob("*")) if path.is_file()
    ]


def _digest(document: dict) -> str:
    canonical = json.dumps(document, separators=(",", ":"), sort_keys=True,
                           ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _archive_replay(repo: Path, plan: dict) -> None:
    """Move the replay slices into `slices/` and land the C-202/C-203 record."""
    parent = repo / PARENT_REL
    slices_dir = parent / "slices"
    slices_dir.mkdir()
    entries = []
    for item in plan["slices"]:
        slug = item["slug"]
        _git(repo, "mv", ".specify/specs/%s" % slug,
             "%s/slices/%s" % (PARENT_REL, slug))
        slice_dir = slices_dir / slug
        files = _slice_file_rows(slice_dir)
        requirements = (slice_dir / "requirements.md").read_text(
            encoding="utf-8").splitlines()
        pointer_line = next(
            index for index, line in enumerate(requirements, 1)
            if line.startswith("**Merged into**:"))
        entries.append({
            "slug": slug,
            "from": ".specify/specs/%s" % slug,
            "to": "%s/slices/%s" % (PARENT_REL, slug),
            "order": item["order"],
            "file_count": len(files),
            "files": files,
            "merged_into_pointer": {
                "path": "%s/slices/%s/requirements.md" % (PARENT_REL, slug),
                "line": pointer_line,
            },
        })
    basis = plan["slices"][0]["order_basis"]
    source = (plan["slices"][0]["order_source"] if basis == "split-record"
              else "directory-name-order")
    merge_document = json.loads(
        (parent / "merge-manifest.json").read_text(encoding="utf-8"))
    merge_digest = _digest(merge_document)
    document = {
        "schema_version": 1,
        "spec": PARENT.name,
        "spec_path": PARENT_REL,
        "generated_by": {
            "engine": "seal-utils.py",
            "version": "replay",
            "command": "seal-utils.py --action archive-apply --spec-dir %s" % PARENT_REL,
        },
        "pinned_commit": _git(repo, "rev-parse", "HEAD").stdout.strip(),
        "order_basis": basis,
        "order_source": source,
        "slices": entries,
        "references": {
            "rows": [],
            "runtime": [
                {"carrier": ".specify/state/%s.md" % name,
                 "status": "absent",
                 "reason": "the replay tree carries no state record",
                 "updates": []}
                for name in (PARENT.name, SLICE_A, SLICE_B)
            ],
        },
        "merge_manifest": {
            "path": "merge-manifest.json",
            "digest_before": merge_digest,
            "digest_after": merge_digest,
        },
        "checks": {
            "preconditions": {
                "merge_status": "merged",
                "open_conflicts": 0,
                "slices_closed": True,
                "dirty_spec_tree": False,
                "side_presence": {entry["slug"]: "destination" for entry in entries},
            },
            "moved_files": sum(entry["file_count"] for entry in entries),
            "live_rewrite": 0,
            "dated_preserved": 0,
            "unclassified": 0,
            "unresolved_before": 0,
            "unresolved_after": 0,
            "runtime_carriers": 3,
            "files_match": True,
        },
    }
    document["digest"] = _digest(document)
    (parent / "archive-manifest.json").write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8")
    _commit(repo, "archive replay batch")


def _slice_identity(plan: dict) -> list:
    return [(entry["slug"], entry["order"], entry["order_basis"])
            for entry in plan["slices"]]


def _seal_facets(payload: dict) -> list:
    """Condition codes + evidence, with the archive move normalised out.

    The evidence carries carrier paths; after the move those read the `to` path.
    The judgment face this test compares is the code and its wording, not the
    location string that legitimately follows the archive.
    """
    archived_prefix = PARENT_REL + "/slices/"
    facets = []
    for condition in payload["conditions"]:
        evidence = condition["evidence"]
        for slug in (SLICE_A, SLICE_B):
            evidence = evidence.replace(archived_prefix + slug, ".specify/specs/" + slug)
        facets.append((condition["code"], evidence))
    return facets


def test_c112_merge_plan_after_archive_reports_the_same_slice_set(tmp_path):
    repo = _replay_tree(tmp_path)
    before_proc, before = _run_action(repo, "merge-plan")
    assert before_proc.returncode == 0, (
        "the replay's pre-archive plan must be conflict-free: %r"
        % before.get("conditions"))
    before_plan = before["plan"]
    assert [entry["slug"] for entry in before_plan["slices"]] == [SLICE_A, SLICE_B]

    _archive_replay(repo, before_plan)

    after_proc, after = _run_action(repo, "merge-plan")
    assert after_proc.returncode == 0, (
        "C-112: an archived tree is not an input error: %r"
        % after.get("conditions"))
    after_plan = after["plan"]
    assert _slice_identity(after_plan) == _slice_identity(before_plan), (
        "C-112: the archived slice set and its order are the same slice set"
    )
    assert after_plan["checks"]["open_conflicts"] == 0
    assert after_plan["checks"]["slice_count"] == 2
    assert all("/" not in entry["slug"] for entry in after_plan["slices"]), (
        "C-112: `slices/**` is never read as a new slice candidate"
    )


def test_c112_merge_apply_after_archive_is_an_idempotent_zero_write_rerun(tmp_path):
    repo = _replay_tree(tmp_path)
    plan = _run_action(repo, "merge-plan")[1]["plan"]
    before_proc, before = _run_action(repo, "merge-apply")
    assert before_proc.returncode == 0
    assert before["apply"]["idempotent"] is True

    _archive_replay(repo, plan)

    after_proc, after = _run_action(repo, "merge-apply")
    assert after_proc.returncode == 0, (
        "C-112: merge-apply after the archive is an idempotent success: %r"
        % after.get("conditions"))
    assert after["apply"]["idempotent"] is True
    assert after["apply"]["writes"] == [], (
        "C-112: the archived rerun performs zero writes"
    )
    assert after["apply"]["slices"] == [SLICE_A, SLICE_B]


def test_c112_seal_judgment_survives_the_archive(tmp_path):
    repo = _replay_tree(tmp_path)
    plan = _run_action(repo, "merge-plan")[1]["plan"]
    before_proc, before = _run_action(repo, "seal")
    assert [condition for condition in before["conditions"]
            if condition["code"] == "p0-unresolved"], (
        "the 074 round's P0 reading is the face this test compares")

    _archive_replay(repo, plan)

    after_proc, after = _run_action(repo, "seal")
    assert after_proc.returncode == before_proc.returncode, (
        "C-112: the seal verdict (P0 / blocking / closure) is unchanged by the archive"
    )
    assert after["verdict"] == before["verdict"]
    assert _seal_facets(after) == _seal_facets(before), (
        "C-112: seal keeps reading the original slice records, now at `to` paths; "
        "the condition list MUST stay byte-identical"
    )
    closure = [condition for condition in before["conditions"]
               if condition["code"].startswith("closure-")]
    assert closure, "the round's closure judgment is part of the compared face"
    assert [condition for condition in after["conditions"]
            if condition["code"].startswith("closure-")] == closure


def test_c112_empty_archive_directory_falls_back_to_the_sibling_scan(tmp_path):
    repo = _replay_tree(tmp_path)
    (repo / PARENT_REL / "slices").mkdir()
    proc, payload = _run_action(repo, "merge-plan")
    assert proc.returncode == 0
    assert [entry["slug"] for entry in payload["plan"]["slices"]] == [SLICE_A, SLICE_B], (
        "C-112: with no archive record and an empty `slices/`, discovery falls "
        "back to the sibling scan"
    )
