"""Contract tests for the seal engine's ``archive-gate`` action (Feature 099, P6).

Contract: ``.specify/specs/099-speckit-seal/contracts/status-sealed.contract.md``
          (C-030 single admission owner, C-031 ``state-drift`` as input error)
          ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
          (C-035 four-way boundary, C-044 the literal waiver form)
          ``.specify/specs/099-speckit-seal/data-model.md`` § 9 (E11 verdict payload)

Rows: T030 (red-first: gate semantics + single-owner guard), with the structural
consumer-wiring legs for T032 (``sanitize-materials`` archive lane) and T033
(``manage-features`` archive-pointer form) landing in the same module because SC-007
names this file as its red-first module.

Semantics pinned here:

* ``Sealed`` (status pair agrees, receipt readable) → exit 0, ``pointer: seal.md``;
* any other status → exit 1, ``pointer: /speckit.seal``, a named reason;
* a legacy ``Completed`` row → exit 1 ``legacy-completed-unruled`` unless a C-044 literal
  ``- **User waiver**:`` line naming the feature exists on BOTH carriers (the current
  ``review.md`` code segment and the detail's ``## Latest Review``), in which case the
  row is admitted (exit 0, ``legacy-completed-ruled``);
* a ``Sealed`` pair whose receipt is missing or unreadable is an input defect (exit 2);
* the status pair disagreeing or missing a carrier is ``state-drift`` (exit 2);
* the admission criterion has exactly one implementation. The guard scans the consumer
  surfaces (``skills/`` and ``templates/commands/``) plus executable scripts for a
  second decision and turns red when one is injected.

Red-first (099 T030): written before the ``archive-gate`` action body landed. The red
reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md`` § 8.
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

#: E11 — the gate block's closed field set.
GATE_KEYS = {"target", "status", "allowed", "reason", "pointer", "exit"}

#: The refusal reason literals this module pins by name (closed vocabulary below).
NOT_SEALED = "not-sealed"
LEGACY_UNRULED = "legacy-completed-unruled"
LEGACY_RULED = "legacy-completed-ruled"
SEALED = "sealed"
STATE_DRIFT = "state-drift"
RECEIPT_INVALID = "seal-receipt-invalid"

SANITIZE_SKILL = REPO_ROOT / "skills" / "internal" / "sanitize-materials" / "SKILL.md"
MANAGE_FEATURES_SKILL = REPO_ROOT / "skills" / "internal" / "manage-features" / "SKILL.md"

#: The receiver-side query every archive lane must carry (C-030: by pointer only).
GATE_QUERY = "--action archive-gate"

WAIVER_LINE = (
    "- **User waiver**: %s — the user explicitly ruled that this legacy Completed row "
    "may be archived (contract fixture)." % CLEAN
)

#: Prose shapes that would BE the criterion, not a pointer to it.
PROSE_CRITERION_RES = (
    re.compile(r"(?i)\bonly\b[^\n]{0,60}\bsealed\b[^\n]{0,40}\b(?:archiv\w*|admitted)\b"),
    re.compile(r"(?i)\bsealed\b[^\n]{0,40}\b(?:is|are)\s+(?:the\s+)?only\b[^\n]{0,40}"
               r"\barchiv\w*"),
    re.compile(r"只有[^\n]{0,30}Sealed[^\n]{0,20}(?:可)?归档"),
)

#: Executable shapes that would recompute admission instead of querying the engine.
CODE_CRITERION_RES = (
    re.compile(r"(?m)^(?![ \t]*#)[^\n]*?(?:\ballowed\b|\badmit(?:ted)?\b|\bgate_ok\b)"
               r"\s*(?:=|:=|:)\s*[^\n]*?(?:\bstatus\b|\bSealed\b)"),
    re.compile(r"(?m)^(?![ \t]*#)[^\n]*?\bstatus\b\s*==\s*['\"]Sealed['\"]"),
    re.compile(r"(?m)^(?![ \t]*#)[^\n]*\[[^\n]*\bstatus\b[^\n]*=[^\n]*Sealed"),
)

#: Files allowed to name the gate's verdict vocabulary (engine + its evidence).
VERDICT_VOCABULARY = (NOT_SEALED, LEGACY_UNRULED, LEGACY_RULED, RECEIPT_INVALID)


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


def _run_engine(repo: Path, action: str, spec_slug: str):
    spec_dir = repo / ".specify" / "specs" / spec_slug
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", action, "--spec-dir", str(spec_dir),
         "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _gate(repo: Path, spec_slug: str = CLEAN):
    return _run_engine(repo, "archive-gate", spec_slug)


def _gate_block(payload: dict) -> dict:
    assert isinstance(payload.get("gate"), dict), (
        "E11: the archive-gate payload MUST carry its verdict block under `gate`; "
        f"got keys {sorted(payload)}"
    )
    return payload["gate"]


def _snapshot(root: Path) -> dict:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }


def _set_status(spec_dir: Path, status: str) -> None:
    detail = spec_dir / "feature-detail.md"
    text = detail.read_text(encoding="utf-8")
    updated = re.sub(r"(?m)^\*\*Status\*\*:\s*.+$", f"**Status**: {status}", text, count=1)
    assert updated != text, "the fixture detail carries no `**Status**:` line to rewrite"
    detail.write_text(updated, encoding="utf-8")

    registry = spec_dir / "feature-registry.md"
    lines = registry.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = False
    for index, line in enumerate(lines):
        if not line.startswith("| 099 "):
            continue
        cells = line.strip().strip("|").split("|")
        cells = [cell.strip() for cell in cells]
        cells[3] = status
        lines[index] = "| " + " | ".join(cells) + " |\n"
        changed = True
        break
    assert changed, "the fixture registry carries no row to rewrite"
    registry.write_text("".join(lines), encoding="utf-8")


def _insert_in_section(path: Path, heading_re: str, inserted: str) -> None:
    """Insert one line at the end of the heading's block (before the next heading)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    level = None
    for index, line in enumerate(lines):
        match = re.match(r"^(#{2,6})\s+(.*)$", line)
        if match and re.search(heading_re, match.group(2)):
            start, level = index, len(match.group(1))
            break
    assert start is not None, f"section {heading_re!r} not found in {path}"
    end = len(lines)
    for cursor in range(start + 1, len(lines)):
        match = re.match(r"^(#{2,6})\s+", lines[cursor])
        if match and len(match.group(1)) <= level:
            end = cursor
            break
    lines.insert(end, inserted)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _add_ruling(spec_dir: Path, carriers=("review", "detail")) -> None:
    if "review" in carriers:
        _insert_in_section(spec_dir / "review.md", r"Code Segment", WAIVER_LINE)
    if "detail" in carriers:
        _insert_in_section(spec_dir / "feature-detail.md", r"Latest Review", WAIVER_LINE)


def _seal_clean(repo: Path) -> dict:
    """Drive the real `seal` action so the gate is read against a sealed tree."""
    _commit(repo)
    proc, payload = _run_engine(repo, "seal", CLEAN)
    assert proc.returncode == 0, (
        "fixture setup: the clean single-spec fixture MUST seal; "
        f"exit={proc.returncode} payload={json.dumps(payload, ensure_ascii=False)[:800]}"
    )
    return payload


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _second_implementation_sites(root: Path):
    """Every consumer/executable surface that implements the admission criterion.

    A *pointer* names the query (``--action archive-gate``) and the outcome it returns;
    it never states the decision rule itself and never recomputes it. The scanner is the
    guard the mutation test drives red (T030).
    """
    hits = []
    for base in ("skills", "templates/commands"):
        directory = root / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in PROSE_CRITERION_RES:
                match = pattern.search(text)
                if match:
                    hits.append((str(path.relative_to(root)), match.group(0).strip()))
                    break
    scripts = root / "scripts"
    for base in ("python", "bash"):
        directory = scripts / base
        if not directory.is_dir():
            continue
        for path in sorted(list(directory.glob("*.py")) + list(directory.glob("*.sh"))):
            if path.name == "seal-utils.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in CODE_CRITERION_RES:
                match = pattern.search(text)
                if match:
                    hits.append((str(path.relative_to(root)), match.group(0).strip()))
                    break
    return hits


# ---------------------------------------------------------------------------
# the gate verdict (T030)
# ---------------------------------------------------------------------------

def test_sealed_spec_is_admitted_and_points_at_the_receipt(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _seal_clean(repo)

    proc, payload = _gate(repo)

    assert proc.returncode == 0, (
        "C-030: a `Sealed` spec MUST be admitted; "
        f"exit={proc.returncode} payload={json.dumps(payload, ensure_ascii=False)[:800]}"
    )
    assert payload["verdict"] == "ok"
    gate = _gate_block(payload)
    assert set(gate) == GATE_KEYS, f"E11: the gate block's field set is closed; got {sorted(gate)}"
    assert gate["allowed"] is True
    assert gate["reason"] == SEALED
    assert gate["status"] == "Sealed"
    assert gate["pointer"] == "seal.md"
    assert gate["exit"] == 0
    assert gate["target"].endswith(CLEAN)
    assert payload["conditions"] == [], (
        "an admitted row carries no refusal conditions; the gate is not a refusal report"
    )


def test_ready_for_review_is_refused_by_name_and_points_back_to_seal(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")

    proc, payload = _gate(repo)

    assert proc.returncode == 1, (
        f"C-030: a non-Sealed spec MUST be refused with exit 1; exit={proc.returncode}"
    )
    assert payload["verdict"] == "refused"
    gate = _gate_block(payload)
    assert gate["allowed"] is False
    assert gate["reason"] == NOT_SEALED
    assert gate["status"] == "Ready for Review"
    assert gate["pointer"] == "/speckit.seal", (
        "C-030: a refusal MUST point back to `/speckit.seal`"
    )
    assert gate["exit"] == 1
    codes = [condition["code"] for condition in payload["conditions"]]
    assert NOT_SEALED in codes, f"the refusal MUST be named in conditions[]; got {codes}"
    assert "/speckit.seal" in " ".join(
        condition["fix_path"] for condition in payload["conditions"]
    )


def test_legacy_completed_without_a_user_ruling_is_refused_by_name(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    spec_dir = repo / ".specify" / "specs" / CLEAN
    _set_status(spec_dir, "Completed")

    proc, payload = _gate(repo)

    assert proc.returncode == 1, (
        f"C-030: a legacy `Completed` row without a user ruling MUST be refused; "
        f"exit={proc.returncode}"
    )
    gate = _gate_block(payload)
    assert gate["status"] == "Completed"
    assert gate["reason"] == LEGACY_UNRULED, (
        "the legacy row MUST be refused under its own named reason, not `not-sealed`"
    )
    assert gate["pointer"] == "/speckit.seal"
    evidence = " ".join(condition["evidence"] for condition in payload["conditions"])
    assert "Completed" in evidence and "waiver" in evidence.lower(), (
        f"the refusal MUST name the legacy row and the ruling it lacks; got {evidence!r}"
    )


def test_legacy_completed_with_the_two_carrier_ruling_is_admitted(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    spec_dir = repo / ".specify" / "specs" / CLEAN
    _set_status(spec_dir, "Completed")
    _add_ruling(spec_dir, carriers=("review", "detail"))

    proc, payload = _gate(repo)

    assert proc.returncode == 0, (
        "FR-023: a legacy `Completed` row carrying the user's explicit ruling on both "
        f"carriers MUST be admitted; exit={proc.returncode} "
        f"payload={json.dumps(payload, ensure_ascii=False)[:800]}"
    )
    gate = _gate_block(payload)
    assert gate["allowed"] is True
    assert gate["reason"] == LEGACY_RULED
    assert gate["exit"] == 0


def test_a_single_carrier_ruling_never_admits_a_legacy_row(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    spec_dir = repo / ".specify" / "specs" / CLEAN
    _set_status(spec_dir, "Completed")
    _add_ruling(spec_dir, carriers=("review",))

    proc, payload = _gate(repo)

    assert proc.returncode == 1, (
        "C-044: a waiver on a single carrier does not count; the legacy row stays refused"
    )
    gate = _gate_block(payload)
    assert gate["reason"] == LEGACY_UNRULED
    assert gate["allowed"] is False


def test_state_drift_is_an_input_error_not_a_one_sided_reading(tmp_path):
    repo = _copy_fixture("seal-refusals", tmp_path / "refusals")
    repo = repo / "state-drift"

    proc, payload = _gate(repo)

    assert proc.returncode == 2, (
        f"C-031: a drifting status pair MUST exit 2; exit={proc.returncode}"
    )
    assert payload["verdict"] == "error"
    gate = _gate_block(payload)
    assert gate["allowed"] is False
    assert gate["reason"] == STATE_DRIFT
    assert gate["status"] is None, (
        "C-031: drift never picks one carrier, so the verdict names no claimed status"
    )
    assert gate["exit"] == 2
    assert STATE_DRIFT in [condition["code"] for condition in payload["conditions"]]


def test_sealed_pair_without_a_readable_receipt_is_an_input_error(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    _seal_clean(repo)
    spec_dir = repo / ".specify" / "specs" / CLEAN
    (spec_dir / "seal.md").unlink()

    proc, payload = _gate(repo)

    assert proc.returncode == 2, (
        "FR-023: the gate queries the seal record as well as the status; a `Sealed` row "
        f"without a readable receipt is an input defect; exit={proc.returncode}"
    )
    gate = _gate_block(payload)
    assert gate["status"] == "Sealed"
    assert gate["reason"] == RECEIPT_INVALID
    assert gate["allowed"] is False


def test_archive_gate_is_read_only_and_rerun_stable(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    before = _snapshot(repo)

    first = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "archive-gate",
         "--spec-dir", str(repo / ".specify" / "specs" / CLEAN),
         "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    second = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "archive-gate",
         "--spec-dir", str(repo / ".specify" / "specs" / CLEAN),
         "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )

    assert first.returncode == second.returncode == 1
    assert first.stdout == second.stdout, (
        "C-038/E11: the same input MUST reproduce the same verdict (no timestamps)"
    )
    assert first.stderr == "" and second.stderr == ""
    assert _snapshot(repo) == before, (
        "C-001/C-008: `archive-gate` is read-only — zero writes on any verdict"
    )


def test_the_gate_payload_is_canonical_json(tmp_path):
    repo = _copy_fixture("single-spec", tmp_path / "repo")
    proc, _payload = _gate(repo)

    canonical = json.dumps(_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    assert proc.stdout == canonical, (
        "C-010: the machine form is one canonical JSON payload "
        "(indent=2, sort_keys=True, ensure_ascii=False)"
    )


# ---------------------------------------------------------------------------
# consumer wiring (T032 / T033): query by pointer, never by local judgment
# ---------------------------------------------------------------------------

def test_sanitize_materials_queries_the_gate_before_retiring_a_spec():
    text = _flat(SANITIZE_SKILL.read_text(encoding="utf-8"))
    assert "Archive admission gate" in text, (
        "T032: the sanitize archive lane MUST carry the admission-gate step as its own "
        "named step before a spec is retired or archived"
    )
    assert GATE_QUERY in text, (
        "T032: the lane MUST query `seal-utils.py --action archive-gate`"
    )
    assert "/speckit.seal" in text, "T032: a refusal MUST point back to `/speckit.seal`"
    for token in ("Exit `0`", "Exit `1`", "Exit `2`"):
        assert token in text, (
            f"T032: the lane MUST name the {token} branch; an engine that cannot be "
            "executed is an error, never a pass"
        )
    assert "never re-implement" in text, (
        "C-030: the lane MUST state that the criterion is never re-implemented locally"
    )


def test_manage_features_queries_the_gate_before_writing_an_archive_pointer():
    text = _flat(MANAGE_FEATURES_SKILL.read_text(encoding="utf-8"))
    assert "Archive-pointer admission" in text, (
        "T033: the `Relocated` archive-pointer form MUST carry its own gate step"
    )
    assert "Relocated" in text
    assert GATE_QUERY in text, (
        "T033: the archive-pointer action MUST query `--action archive-gate` first"
    )
    assert "/speckit.seal" in text, "T033: a refusal MUST point back to `/speckit.seal`"
    for token in ("Exit `0`", "Exit `1`", "Exit `2`"):
        assert token in text, f"T033: the pointer action MUST name the {token} branch"
    assert "never re-implement" in text, (
        "C-030: the reconcile stays here; admission is never re-implemented here"
    )


# ---------------------------------------------------------------------------
# single owner (C-030): the guard and its mutation
# ---------------------------------------------------------------------------

def test_no_second_implementation_of_the_admission_criterion():
    hits = _second_implementation_sites(REPO_ROOT)
    assert hits == [], (
        "C-030: the archive admission criterion MUST exist in the seal engine only; "
        f"consumer surfaces only query it. Second implementations found: {hits}"
    )


def test_the_guard_turns_red_when_the_criterion_is_copied(tmp_path):
    root = tmp_path / "copy"
    prose = root / "skills" / "internal" / "sanitize-materials" / "SKILL.md"
    prose.parent.mkdir(parents=True)
    prose.write_text(
        "# sanitize-materials (mutated copy)\n\n"
        "Only a `Sealed` spec may be archived; otherwise refuse.\n",
        encoding="utf-8",
    )
    code = root / "scripts" / "python" / "dup-gate.py"
    code.parent.mkdir(parents=True)
    code.write_text(
        "def admit(status, receipt):\n"
        "    allowed = status == \"Sealed\"\n"
        "    return allowed\n",
        encoding="utf-8",
    )

    hits = _second_implementation_sites(root)
    flagged = {path for path, _excerpt in hits}
    assert "skills/internal/sanitize-materials/SKILL.md" in flagged, (
        "the guard MUST flag a copied prose criterion"
    )
    assert "scripts/python/dup-gate.py" in flagged, (
        "the guard MUST flag a copied executable criterion"
    )


def test_no_consumer_carries_the_gate_verdict_vocabulary():
    allowed = {
        "scripts/python/seal-utils.py",
        ".specify/scripts/python/seal-utils.py",
    }
    hits = []
    for base in ("skills", "templates", "scripts", "shared"):
        directory = REPO_ROOT / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".py", ".sh"):
                continue
            relative = str(path.relative_to(REPO_ROOT))
            if relative in allowed or relative.startswith("tests/"):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in VERDICT_VOCABULARY:
                if token in text:
                    hits.append((relative, token))
    assert hits == [], (
        "C-030: the gate's verdict vocabulary belongs to the engine; a consumer "
        f"carrying it is a second implementation. Found: {hits}"
    )
