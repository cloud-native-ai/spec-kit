"""Contract test: evidence binding — every pass claim binds to archived evidence.

063-review-p1-governance, US4 (C-26/C-27/C-28, FR-019/FR-020/FR-021, SC-010).

C-26 — templates/verification-log-template.md gains a structured evidence-record
       section between `# -- /speckit.implement results --` and
       `# -- Success Criteria evaluation --`: one record per evaluation sample
       carrying sample_id / evidence_path (repo-relative) / evidence_sha256 /
       verdict; the template declares the deterministic hash algorithm (SHA-256
       over the archived file's bytes, sha256sum-compatible) and the rule that a
       `pass` verdict requires a complete evidence row. Existing section set and
       key-value conventions kept; the new section is additive.
C-27 — shared/definitions/probe-definitions.md registers
       gate-implement-evidence-binding ([[STR-001]]) beside the existing
       command-gate rows (class command-gate, unit /speckit.implement) with an
       h-gate-evidence HandlerBinding row at @point:confirm-gate — same shape as
       gate-implement-checklist-waiver, REUSING the existing handler id (no new
       subsystem); skills/internal/implement-feature/SKILL.md references the gate
       at its Step 9 (verification-log population), the step that owns the
       evidence the gate checks.
C-28 — red-semantics mutation drills: for every sample recorded `pass` the
       archived artifact MUST exist, be non-empty, and hash-match; each failure
       class is red naming the sample id and reason, never downgraded; a
       non-`pass` verdict carries no binding duty; a `pass` without a complete
       evidence row is `unverified` and MUST NOT be cited as passing evidence
       downstream.

The C-28 drills run a checker DERIVED FROM the template's declared section
(fields extracted from the template itself), so a template without the section
fails the drills too — the red run is genuine, and a hand-drifted template
declaration breaks its own gate semantics.
"""

import hashlib
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "verification-log-template.md"
REGISTRY = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
SKILL = REPO_ROOT / "skills" / "internal" / "implement-feature" / "SKILL.md"

GATE_ID = "gate-implement-evidence-binding"
SECTION_RE = re.compile(r"(?m)^# -- Evidence records.*--$")
SECTION_BLOCK_RE = re.compile(r"(?ms)^(# -- Evidence records.*?--\s*\n)(.*?)(?=^# -- |\Z)")


# --------------------------------------------------------------------------- #
# helpers — the declared format is the checker's only source
# --------------------------------------------------------------------------- #

def _template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _registry_text() -> str:
    return REGISTRY.read_text(encoding="utf-8")


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _skill_step9() -> str:
    text = _skill_text()
    m = re.search(r"(?ms)^### Step 9 .*?(?=^### |\Z)", text)
    assert m, "implement-feature SKILL.md lacks a Step 9 section"
    return m.group(0)


def _evidence_section(template_text: str) -> str:
    """The template's declared evidence-record section (C-26 artifact)."""
    m = SECTION_BLOCK_RE.search(template_text)
    assert m, (
        "verification-log-template.md lacks the `# -- Evidence records ... --` "
        "section (C-26: it MUST sit between the implement-results and SC "
        "evaluation markers)"
    )
    return m.group(0)


def _declared_fields(template_text: str) -> list:
    """Field names the template declares for one evidence record."""
    section = _evidence_section(template_text)
    fields = re.findall(r"(?m)^([a-z0-9_]+)=\[", section)
    assert fields, "the evidence-record section declares no `key=[PLACEHOLDER]` fields"
    return fields


def _gate_check(log_text: str, root: Path) -> dict:
    """The gate's check (C-28 semantics), parsing the format the template declares.

    Returns {"green": [sample_id...], "red": [(sample_id, reason)...],
    "unverified": [sample_id...]}.
    """
    fields = _declared_fields(_template_text())
    verdict_key = "verdict"
    id_key = "sample_id"

    m = SECTION_BLOCK_RE.search(log_text)
    if not m:
        # No evidence section at all: every `pass` in the SC evaluation is
        # unverified — MUST NOT be cited as passing evidence.
        unverified = re.findall(r"(?m)^(SC-[A-Za-z0-9-]+)_status=pass\b", log_text)
        return {"green": [], "red": [], "unverified": unverified}

    body = m.group(2)
    # Parse `key=value` lines whose value is NOT a template placeholder.
    records: list = []
    current: dict = {}
    for line in body.splitlines():
        kv = re.match(r"^([a-z0-9_]+)=(.+)$", line.strip())
        if not kv or kv.group(1) not in fields:
            # Any non-record line (blank line, comment) closes the current
            # record: the template declares a contiguous 4-key block shape.
            if current:
                records.append(current)
                current = {}
            continue
        if kv.group(2).lstrip().startswith("["):
            continue  # template placeholder, not a filled record
        current[kv.group(1)] = kv.group(2).strip()
    if current:
        records.append(current)

    green, red, unverified = [], [], []
    for rec in records:
        sid = rec.get(id_key, "<no sample_id>")
        verdict = rec.get(verdict_key, "")
        if verdict != "pass":
            continue  # non-pass verdicts carry no binding duty
        if any(not rec.get(f, "") for f in fields):
            unverified.append(sid)  # incomplete evidence row
            continue
        path = root / rec["evidence_path"]
        if not path.is_file():
            red.append((sid, "missing"))
            continue
        if path.stat().st_size == 0:
            red.append((sid, "empty"))
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != rec["evidence_sha256"].lower():
            red.append((sid, "mismatch"))
            continue
        green.append(sid)
    return {"green": green, "red": red, "unverified": unverified}


def _fixture_vlog(tmp_path: Path, records, with_section=True, sc_passes=("SC-001",)) -> str:
    """A filled verification.md in the template's declared shape."""
    lines = ["# Verification Log — FIXTURE", "", "# -- /speckit.implement results --",
             "", "implementation_date=2026-10-20", ""]
    if with_section:
        lines += ["# -- Evidence records --", ""]
        for rec in records:
            for key in ("sample_id", "evidence_path", "evidence_sha256", "verdict"):
                if rec.get(key) is not None:
                    lines.append(f"{key}={rec[key]}")
            lines.append("")
    lines += ["# -- Success Criteria evaluation --", ""]
    for i, sc in enumerate(sc_passes):
        status = "pass" if i < len(sc_passes) else "unknown"
        lines += [f"{sc}_status={status}", f"{sc}_value=fixture", f"{sc}_note=fixture", ""]
    return "\n".join(lines)


def _archive(tmp_path: Path, rel: str, content: bytes) -> str:
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


# --------------------------------------------------------------------------- #
# C-26 — the template's structured evidence-record section
# --------------------------------------------------------------------------- #

def test_c26_section_sits_between_results_and_sc_evaluation():
    text = _template_text()
    results_at = text.index("# -- /speckit.implement results --")
    evidence_at = text.index("# -- Evidence records")
    sc_at = text.index("# -- Success Criteria evaluation --")
    assert results_at < evidence_at < sc_at, (
        "the evidence-record section MUST sit between the implement-results and "
        "SC evaluation sections (C-26)"
    )


def test_c26_declares_the_four_record_fields():
    fields = _declared_fields(_template_text())
    for field in ("sample_id", "evidence_path", "evidence_sha256", "verdict"):
        assert field in fields, f"the section MUST declare the `{field}` field"


def test_c26_declares_sha256_over_the_archived_files_bytes():
    section = _evidence_section(_template_text())
    assert re.search(r"SHA-256", section), "the deterministic hash algorithm MUST be named"
    assert re.search(r"sha256sum", section), "the digest MUST be sha256sum-compatible"
    assert re.search(r"bytes|字节", section), "the hash domain MUST be the archived file's bytes"


def test_c26_evidence_path_is_declared_repo_relative():
    section = _evidence_section(_template_text())
    assert re.search(r"repo-relative", section), (
        "evidence_path MUST be declared repo-relative (resolvable from any checkout)"
    )


def test_c26_pass_requires_a_complete_evidence_row():
    section = _evidence_section(_template_text())
    flat = " ".join(section.split())
    assert re.search(r"pass.*complete|complete.*pass|完整证据行", flat, re.I), (
        "the section MUST declare that a `pass` verdict requires a complete "
        "evidence row"
    )
    assert re.search(r"unverified", section), (
        "the section MUST name the `unverified` class for a pass without a "
        "complete evidence row"
    )


def test_c26_existing_sections_preserved_additive_only():
    text = _template_text()
    markers = [
        "# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --",
        "# -- /speckit.implement results --",
        "# -- Success Criteria evaluation --",
        "# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --",
        "# -- Free-form notes --",
    ]
    ats = [text.index(m) for m in markers]
    assert ats == sorted(ats), "the pre-existing section set MUST keep its order"
    for marker in markers:
        assert marker in text


# --------------------------------------------------------------------------- #
# C-27 — gate registration and the Step 9 consumption point
# --------------------------------------------------------------------------- #

def test_c27_gate_row_registered_beside_the_checklist_waiver():
    lines = _registry_text().splitlines()
    waiver_at = next(i for i, l in enumerate(lines) if l.startswith("| gate-implement-checklist-waiver |"))
    row = f"| {GATE_ID} | command-gate | /speckit.implement | {GATE_ID} |"
    assert row in lines, "the gate row MUST exist in the Probe Object table"
    gate_at = lines.index(row)
    assert abs(gate_at - waiver_at) <= 2, (
        "the row MUST land beside the existing command-gate rows (form precedent: "
        "gate-implement-checklist-waiver)"
    )


def test_c27_handler_binding_row_at_confirm_gate():
    text = _registry_text()
    row_re = re.compile(
        rf"^\| h-gate-evidence \| @point:confirm-gate \| {GATE_ID} \| .+ \|$",
        re.M,
    )
    assert row_re.search(text), (
        "the h-gate-evidence HandlerBinding MUST subscribe to this gate at "
        "@point:confirm-gate"
    )


def test_c27_reuses_the_existing_handler_no_new_subsystem():
    """The binding reuses the EXISTING h-gate-evidence handler id — no new
    handler, engine, or store is introduced by this gate (C-27)."""
    text = _registry_text()
    new_handler = re.search(rf"^\| (?!h-gate-evidence\b)(h-[a-z-]+) \| [^|]* \| {GATE_ID} \|", text, re.M)
    assert not new_handler, (
        f"the gate MUST reuse the existing h-gate-evidence handler, not introduce "
        f"{new_handler and new_handler.group(1)}"
    )


def test_c27_skill_step9_references_the_gate():
    step = _skill_step9()
    assert GATE_ID in step, (
        "implement-feature Step 9 (the verification-log step) MUST reference the "
        "gate — the skill has no per-feature GATE numbering; this step owns the "
        "evidence the gate checks"
    )


def test_c27_skill_step9_states_the_check_and_the_observation_protocol():
    step = _skill_step9()
    assert re.search(r"exists|存在", step) and re.search(r"non-empty|非空", step), (
        "Step 9 MUST state the artifact-exists and non-empty checks"
    )
    assert re.search(r"SHA-256", step), "Step 9 MUST state the hash-match check"
    assert re.search(r"门控观察协议|Gate Observation Protocol", step), (
        "the firing evidence MUST be recorded per the existing gate observation "
        "protocol (reused mechanism)"
    )
    assert re.search(r"--lifecycle-point", step), (
        "the firing evidence MUST be recorded via the feedback engine with "
        "--lifecycle-point (reused mechanism, no new subsystem)"
    )


# --------------------------------------------------------------------------- #
# C-28 — red-semantics mutation drills (quickstart S8 shape)
# --------------------------------------------------------------------------- #

def _s8_fixture(tmp_path: Path):
    """Four `pass` samples + one `fail` sample, per quickstart S8."""
    good_hash = _archive(tmp_path, "notes/run/SC-001.txt", b"matching evidence\n")
    _archive(tmp_path, "notes/run/fail-sample.txt", b"fail sample evidence\n")
    empty_hash = hashlib.sha256(b"").hexdigest()
    mismatch_hash = hashlib.sha256(b"not the archived content").hexdigest()
    records = [
        {"sample_id": "SC-001", "evidence_path": "notes/run/SC-001.txt",
         "evidence_sha256": good_hash, "verdict": "pass"},
        {"sample_id": "SC-002", "evidence_path": "notes/run/missing.txt",
         "evidence_sha256": good_hash, "verdict": "pass"},
        {"sample_id": "SC-003", "evidence_path": "notes/run/empty.txt",
         "evidence_sha256": empty_hash, "verdict": "pass"},
        {"sample_id": "SC-004", "evidence_path": "notes/run/SC-004.txt",
         "evidence_sha256": mismatch_hash, "verdict": "pass"},
        # fail verdict: no binding duty even though its artifact is absent here
        {"sample_id": "SC-005", "evidence_path": "notes/run/fail-sample.txt",
         "evidence_sha256": "0" * 64, "verdict": "fail"},
    ]
    _archive(tmp_path, "notes/run/empty.txt", b"")
    _archive(tmp_path, "notes/run/SC-004.txt", b"the real archived content\n")
    return records


def test_c28_matching_pass_is_green_and_only_that(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert out["green"] == ["SC-001"], out
    reds = dict(out["red"])
    assert reds == {"SC-002": "missing", "SC-003": "empty", "SC-004": "mismatch"}, out["red"]


def test_c28_missing_artifact_is_red_naming_sample_and_reason(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert ("SC-002", "missing") in out["red"], (
        "a missing archived artifact MUST be red naming the sample id and reason"
    )


def test_c28_empty_artifact_is_red_naming_sample_and_reason(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert ("SC-003", "empty") in out["red"]


def test_c28_hash_mismatch_is_red_naming_sample_and_reason(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert ("SC-004", "mismatch") in out["red"]


def test_c28_non_pass_verdict_carries_no_binding_duty(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert "SC-005" not in [sid for sid, _ in out["red"]], (
        "a non-`pass` verdict has no binding duty — its (absent) evidence is not red"
    )
    assert "SC-005" not in out["unverified"] and "SC-005" not in out["green"]


def test_c28_pass_without_evidence_section_is_unverified(tmp_path):
    records = _s8_fixture(tmp_path)
    log = _fixture_vlog(tmp_path, records, with_section=False,
                        sc_passes=("SC-001", "SC-002"))
    out = _gate_check(log, tmp_path)
    assert out["green"] == [], "no pass may count as green without the evidence section"
    assert sorted(out["unverified"]) == ["SC-001", "SC-002"], (
        "every `pass` without the evidence section is unverified"
    )


def test_c28_incomplete_evidence_row_is_unverified(tmp_path):
    records = _s8_fixture(tmp_path)
    records.append({"sample_id": "SC-006",
                    "evidence_path": "notes/run/SC-001.txt",
                    "verdict": "pass"})  # missing evidence_sha256
    log = _fixture_vlog(tmp_path, records)
    out = _gate_check(log, tmp_path)
    assert "SC-006" in out["unverified"], (
        "a `pass` with an incomplete evidence row is unverified — MUST NOT be "
        "cited as passing evidence downstream"
    )
    assert ("SC-006", "mismatch") not in out["red"]


def test_c28_red_is_not_downgraded_anywhere():
    """The no-downgrade rule is declared at both the template and the skill."""
    section = _evidence_section(_template_text())
    step = _skill_step9()
    assert re.search(r"MUST NOT be (cited|downgraded)|不得.*(引用|降级)", section + step, re.I), (
        "the unverified/downgrade prohibition MUST be declared"
    )
    assert re.search(r"downgrad|降级", step), (
        "Step 9 MUST declare that a red verdict is never downgraded to "
        "`self-disclosed and continue`"
    )
