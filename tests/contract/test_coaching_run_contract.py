"""Contract tests for the coaching run (Feature 078, User Story 1).

Clause source: ``.specify/specs/078-coaching-skills/contracts/coaching-run.contract.md``
(C-1..C-14). Each test names its clause; the clause numbering is the green-point order
declared by ``tasks.md`` T009..T013.

The skill is a prompt contract, not a program, so every assertion is structural: a
required section or literal must exist in ``SKILL.md`` / its references, and the
artifact-shape helpers below are exercised on a compliant fixture run and on four
counterexamples that MUST be judged red. A validator that accepts everything proves
nothing; the counterexample band is what makes the compliant case discriminating.

Literal authority for every shared string and closed status value is
``requirements.md`` § Shared Strings (STR-001..STR-017); this file uses the literals
directly because it is the guard copy that pins them.
"""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "external" / "coaching-skills" / "SKILL.md"

#: Feature baseline (immediately before this implement run). C-13 judges the added
#: lines of ``git diff <base>`` inside the scanner's surface, never a total count.
FEATURE_BASE = "a7aa0793"

ARTIFACTS = ("expectation.md", "observation.md", "deviations.md", "improvement-plan.md")
RUN_DOMAINS = ("success", "partial", "failed")
OPTIMIZATION_DOMAINS = ("applied", "skipped", "unavailable", "failed")
FAILURE_STATES = ("failed", "timeout", "refused")


# --------------------------------------------------------------------------- #
# markdown helpers
# --------------------------------------------------------------------------- #


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str | None:
    """Return the body of ``## <heading>`` up to the next ``## `` heading."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _require_section(text: str, heading: str) -> str:
    body = _section(text, heading)
    assert body is not None and body.strip(), f"missing required section: ## {heading}"
    # Prose wraps at ~80 columns; phrase assertions are about content, not layout.
    return re.sub(r"\s+", " ", body).strip()


def _get(text: str, pattern: str, flags: int = re.IGNORECASE) -> re.Match[str]:
    match = re.search(pattern, text, flags)
    assert match is not None, f"missing required pattern: {pattern}"
    return match


# --------------------------------------------------------------------------- #
# run-shape validator (compliant fixture + counterexamples)
# --------------------------------------------------------------------------- #


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def _dispatch_at(observation: str) -> list[datetime]:
    return [
        _parse_iso(match.group(1))
        for match in re.finditer(r"dispatched-at:\s*(\S+)", observation)
    ]


def validate_run(
    run_dir: Path,
    *,
    primary_artifact_exists: bool,
    oc1_met: bool,
) -> list[str]:
    """Judge one run directory against the shape fixed by C-3/C-4/C-10/C-11.

    The function is deliberately small and deterministic: it checks the artifact set,
    the expectation-before-dispatch order, the single-dispatch cardinality, the closed
    status domains, and the FR-017 boundary (optimization never fails or caps a
    completed execution).
    """
    errors: list[str] = []
    present = {path.name for path in run_dir.glob("*.md")}
    missing = [name for name in ARTIFACTS if name not in present]
    if missing:
        errors.append("missing artifacts: " + ", ".join(missing))
        return errors
    extra = sorted(present.difference(ARTIFACTS))
    if extra:
        errors.append("artifact set is not exactly four: " + ", ".join(extra))

    expectation = (run_dir / "expectation.md").read_text(encoding="utf-8")
    for heading in ("Outcome Correctness", "Process Efficiency"):
        if _section(expectation, heading) is None:
            errors.append(f"expectation.md lacks ## {heading}")

    observation = (run_dir / "observation.md").read_text(encoding="utf-8")
    dispatched = _dispatch_at(observation)
    if len(dispatched) != 1:
        errors.append(f"exactly one dispatch required, found {len(dispatched)}")
    elif (run_dir / "expectation.md").stat().st_mtime > dispatched[0].timestamp():
        errors.append("expectation.md is not older than the dispatch")

    plan = (run_dir / "improvement-plan.md").read_text(encoding="utf-8")
    status = _section(plan, "Run Status")
    if status is None:
        errors.append("improvement-plan.md lacks ## Run Status")
        return errors
    run_match = re.search(r"run:\s*(\S+)", status)
    optimization_match = re.search(r"optimization:\s*(\S+)", status)
    if run_match is None or run_match.group(1) not in RUN_DOMAINS:
        errors.append("run value outside the closed domain")
    if optimization_match is None or optimization_match.group(1) not in OPTIMIZATION_DOMAINS:
        errors.append("optimization value outside the closed domain")
    if run_match is None or optimization_match is None:
        return errors

    run_value = run_match.group(1)
    optimization = optimization_match.group(1)
    returned = re.search(r"returned:\s*(\S+)", observation)
    if returned is not None and returned.group(1) in FAILURE_STATES and run_value == "success":
        errors.append("failure narrated as completion")

    has_observable_step = bool(re.search(r"\b(host-event|self-report)\b", observation))
    if primary_artifact_exists and oc1_met:
        if run_value == "failed":
            errors.append("a completed primary artifact must not yield run: failed")
        if has_observable_step and run_value != "success":
            errors.append("optimization status capped a completed execution")
    if not has_observable_step and run_value == "success":
        errors.append("zero observation evidence must not yield run: success")
    if optimization == "failed" and "claim" in plan and "conflict" not in plan:
        errors.append("claim conflict recorded without naming it")
    return errors


def _write_run(
    root: Path,
    *,
    dispatch_count: int = 1,
    returned: str = "completed",
    run: str = "success",
    optimization: str = "skipped",
    observation_source: str = "host-event",
) -> Path:
    run_dir = root / "20261030T101500Z-fixture-trainee"
    run_dir.mkdir(parents=True)
    (run_dir / "expectation.md").write_text(
        "## Run header\n- run-id: 20261030T101500Z-fixture-trainee\n\n"
        "## Outcome Correctness\n| id | object |\n|---|---|\n| OC-1 | checklist.md |\n\n"
        "## Process Efficiency\n| id | steps |\n|---|---|\n| PE-1 | ~5-8 |\n",
        encoding="utf-8",
    )
    dispatch_blocks = "\n".join(
        f"## Dispatch\n- mode: native\n- dispatched-at: 2026-10-30T10:15:0{index}Z\n"
        f"- returned: {returned}\n"
        for index in range(dispatch_count)
    )
    (run_dir / "observation.md").write_text(
        dispatch_blocks + "\n## Steps\n| step | source |\n|---|---|\n"
        f"| S1 | {observation_source} |\n",
        encoding="utf-8",
    )
    (run_dir / "deviations.md").write_text(
        "## Deviations\n| id | dimension | class | evidence |\n|---|---|---|---|\n"
        "| D-1 | correctness | result-deviation | S1 |\n",
        encoding="utf-8",
    )
    (run_dir / "improvement-plan.md").write_text(
        "## Improvement Plan\n| priority | target-location | tweak | evidence |\n"
        "|---|---|---|---|\n| 1 | SKILL.md#Workflow | one tweak | D-1 |\n\n"
        f"## Run Status\n- run: {run}\n- optimization: {optimization}\n",
        encoding="utf-8",
    )
    # Make the ordering premise true for the compliant fixture: the expectation is
    # written before the dispatch it predicts.
    old = _parse_iso("2026-10-30T10:14:00Z").timestamp()
    os.utime(run_dir / "expectation.md", (old, old))
    return run_dir


# --------------------------------------------------------------------------- #
# C-1 Inputs
# --------------------------------------------------------------------------- #


def test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work():
    body = _require_section(_text(SKILL), "Inputs")
    assert "<trainee-name|trainee-path>" in body
    assert "<work>" in body
    assert "non-empty" in body
    assert re.search(r"missing or empty parameter fails closed", body, re.IGNORECASE)
    assert re.search(r"names the missing parameter", body, re.IGNORECASE)
    assert re.search(r"verbatim", body, re.IGNORECASE)
    assert re.search(r"never substitute one parameter for the other", body, re.IGNORECASE)
    assert re.search(r"one-sentence clarification", body, re.IGNORECASE)
    assert re.search(r"not a confirmation step", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-2 Trainee Resolution
# --------------------------------------------------------------------------- #


def test_c2_resolution_reuses_the_run_skills_ladder_without_a_second_rule():
    body = _require_section(_text(SKILL), "Trainee Resolution")
    ordered = [
        "canonical internal",
        "canonical external",
        "installed internal",
        "installed external",
    ]
    positions = [body.lower().find(item) for item in ordered]
    assert all(position >= 0 for position in positions), "resolution ladder incomplete"
    assert positions == sorted(positions), "resolution ladder out of order"
    assert "run-skills" in body
    assert re.search(r"no second resolution rule", body, re.IGNORECASE)


def test_c2_hit_counting_and_fail_closed_cases():
    body = _require_section(_text(SKILL), "Trainee Resolution")
    assert re.search(r"source hit and its installed mirror hit are one hit", body, re.IGNORECASE)
    assert re.search(r"two hits.*fail closed naming both candidate paths", body, re.IGNORECASE | re.DOTALL)
    assert re.search(r"zero hits.*searched coordinates", body, re.IGNORECASE | re.DOTALL)
    assert re.search(r"no readable `SKILL.md`", body, re.IGNORECASE)
    assert re.search(r"frontmatter is invalid", body, re.IGNORECASE)
    assert re.search(r"before the expectation phase", body, re.IGNORECASE)
    assert re.search(r"resolves to `coaching-skills` itself", body, re.IGNORECASE)
    assert re.search(r"recursion depth is 1", body, re.IGNORECASE)
    assert re.search(r"explicit-path mode", body, re.IGNORECASE)
    assert re.search(r"DispatchRecord `mode`", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-3 Run Identity and Directory
# --------------------------------------------------------------------------- #


def test_c3_run_id_shape_directory_and_fail_closed_on_existing_directory():
    body = _require_section(_text(SKILL), "Run Identity")
    assert "YYYYMMDDTHHMMSSZ-<trainee-slug>" in body
    assert "UTC timestamp" in body
    assert "lowercase kebab slug" in body
    assert ".specify/memory/coaching/<run-id>/" in body
    assert re.search(r"already exists.*fails closed naming the existing path", body, re.IGNORECASE | re.DOTALL)
    assert re.search(r"MUST NOT append\s+a suffix", body)
    assert re.search(r"no artifact path escapes it", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-4 Artifact Set and Ordering
# --------------------------------------------------------------------------- #


def test_c4_four_artifacts_in_order_with_dispatch_evidence():
    body = _require_section(_text(SKILL), "Artifacts and Order")
    positions = [body.find(name) for name in ARTIFACTS]
    assert all(position >= 0 for position in positions), "an artifact name is missing"
    assert positions == sorted(positions), "artifact names are out of order"
    assert re.search(
        r"before the first action of the dispatched subagent", body, re.IGNORECASE
    )
    assert re.search(r"`dispatched-at` is the ordering evidence", body, re.IGNORECASE)
    assert re.search(r"missing file fails the\s+run", body, re.IGNORECASE)
    assert re.search(r"improvement-plan\.md` § Run Status", body)


def test_c4_validator_accepts_the_compliant_run(tmp_path: Path):
    run_dir = _write_run(tmp_path)
    assert validate_run(run_dir, primary_artifact_exists=True, oc1_met=True) == []


def test_c4_validator_rejects_missing_expectation_and_second_dispatch(tmp_path: Path):
    missing = _write_run(tmp_path / "missing")
    (missing / "expectation.md").unlink()
    errors = validate_run(missing, primary_artifact_exists=True, oc1_met=True)
    assert any("missing artifacts: expectation.md" in error for error in errors)

    twice = _write_run(tmp_path / "twice", dispatch_count=2)
    errors = validate_run(twice, primary_artifact_exists=True, oc1_met=True)
    assert any("exactly one dispatch required, found 2" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-5 Execution-First Priority
# --------------------------------------------------------------------------- #


def test_c5_execution_is_primary_and_optimization_never_shortens_it():
    body = _require_section(_text(SKILL), "Execution First")
    assert re.search(r"Trainee's real work completed and its primary artifact exists", body, re.IGNORECASE)
    assert re.search(r"Optimization MUST NOT be a precondition of execution", body)
    assert re.search(r"MUST NOT shorten, redirect, or\s+simplify the execution", body, re.IGNORECASE)
    assert re.search(r"MUST NOT run any Trainee step in parallel with the subagent", body)


# --------------------------------------------------------------------------- #
# C-6 Single Dispatch, No Re-Run
# --------------------------------------------------------------------------- #


def test_c6_exactly_one_dispatch_and_no_retry_after_failure():
    body = _require_section(_text(SKILL), "Single Dispatch")
    assert re.search(r"exactly one subagent per run", body, re.IGNORECASE)
    assert re.search(r"failed, timed-out, or refused dispatch", body, re.IGNORECASE)
    assert re.search(r"never retried inside the same run", body, re.IGNORECASE)
    assert re.search(r"continue into `deviations\.md` and `improvement-plan\.md`", body, re.IGNORECASE)
    assert re.search(r"never executes Trainee steps itself", body, re.IGNORECASE)
    assert re.search(r"never injects side effects", body, re.IGNORECASE)


def test_c6_failure_is_not_narrated_as_completion(tmp_path: Path):
    failed = _write_run(tmp_path, returned="failed", run="success")
    errors = validate_run(failed, primary_artifact_exists=True, oc1_met=False)
    assert "failure narrated as completion" in errors


# --------------------------------------------------------------------------- #
# C-7 Deviations
# --------------------------------------------------------------------------- #


def test_c7_both_dimensions_evidence_and_two_deviation_classes():
    body = _require_section(_text(SKILL), "Compare")
    assert "Outcome Correctness" in body
    assert "Process Efficiency" in body
    assert re.search(r"cites concrete evidence from `observation\.md`", body, re.IGNORECASE)
    assert "result-deviation" in body
    assert "process-deviation" in body
    assert re.search(r"partially completed\s+Trainee flow separates the two classes", body, re.IGNORECASE)
    assert re.search(r"coach's reading of `<work>`", body, re.IGNORECASE)
    assert re.search(r"materially diverged", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-8 Improvement Plan
# --------------------------------------------------------------------------- #


def test_c8_entries_name_a_location_and_are_still_produced_without_evidence():
    body = _require_section(_text(SKILL), "Improvement Plan")
    assert re.search(r"concrete Trainee file and section plus one concrete tweak", body, re.IGNORECASE)
    assert re.search(r"generic advice", body, re.IGNORECASE)
    assert re.search(r"cites `D-\*` findings", body, re.IGNORECASE)
    assert re.search(r"`evidence: none`", body, re.IGNORECASE)
    assert re.search(r"When observation is empty the plan is still produced", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-9 Optimization Application (protocol owner is data-model.md)
# --------------------------------------------------------------------------- #


def test_c9_optimization_uses_the_entry_and_points_at_the_single_claim_owner():
    text = _text(SKILL)
    body = _require_section(text, "Optimization")
    assert "improve-skills" in body
    assert "Trainee target" in body
    assert "deviation evidence" in body
    assert re.search(r"sole owner is `data-model\.md` § Optimization claim", body, re.IGNORECASE)
    assert re.search(r"states no second version", body, re.IGNORECASE)
    assert re.search(r"record `optimization: failed`", body, re.IGNORECASE)
    assert re.search(r"name the conflicting\s+run-id", body, re.IGNORECASE)
    assert re.search(r"never retry in a loop", body, re.IGNORECASE)


def test_c9_the_claim_protocol_is_referenced_not_restated():
    text = _text(SKILL)
    for duplicate in (".optimization-claims", "O_CREAT", "O_EXCL", "EEXIST"):
        assert duplicate not in text, (
            f"claim protocol restated in SKILL.md ({duplicate}); owner is data-model.md"
        )


# --------------------------------------------------------------------------- #
# C-10 Run Status
# --------------------------------------------------------------------------- #


def test_c10_closed_domains_recording_location_and_fr017_boundary():
    body = _require_section(_text(SKILL), "Run Status")
    for value in RUN_DOMAINS:
        assert f"`{value}`" in body
    for value in OPTIMIZATION_DOMAINS:
        assert f"`{value}`" in body
    assert "`improvement-plan.md` § Run Status" in body
    assert re.search(
        r"never turns a completed Trainee execution into `failed`", body, re.IGNORECASE
    )
    assert re.search(r"verdict ladder itself is owned by `data-model\.md` § RunStatus", body, re.IGNORECASE)
    assert re.search(r"names the four artifact paths", body, re.IGNORECASE)


def test_c10_optimization_unavailable_never_fails_a_completed_execution(tmp_path: Path):
    run_dir = _write_run(tmp_path, run="failed", optimization="unavailable")
    errors = validate_run(run_dir, primary_artifact_exists=True, oc1_met=True)
    assert any("optimization status capped a completed execution" in error for error in errors) or any(
        "completed primary artifact must not yield run: failed" in error for error in errors
    )


# --------------------------------------------------------------------------- #
# C-11 Degradation Ladder
# --------------------------------------------------------------------------- #


def test_c11_ladder_is_closed_and_zero_observation_keeps_the_plan():
    body = _require_section(_text(SKILL), "Degradation Ladder")
    assert "host-event" in body
    assert "self-report" in body
    assert "observation-gap" in body
    assert re.search(r"counted in the gap list, never invented", body, re.IGNORECASE)
    assert re.search(r"every entry is `evidence: none`", body, re.IGNORECASE)
    assert re.search(r"`run: partial`", body)
    assert re.search(r"`data-model\.md` § RunStatus", body)


# --------------------------------------------------------------------------- #
# C-12 Dispatch Mechanism Boundary
# --------------------------------------------------------------------------- #


def test_c12_one_dispatch_mechanism_with_a_recorded_mode():
    body = _require_section(_text(SKILL), "Boundaries")
    assert re.search(r"host-native subagent capability first", body, re.IGNORECASE)
    assert re.search(r"`run-agent` is the fallback", body, re.IGNORECASE)
    assert re.search(r"`run-skills` only resolves and executes the Trainee", body, re.IGNORECASE)
    assert re.search(r"no second\s+mechanism", body, re.IGNORECASE | re.DOTALL)
    assert re.search(r"mode used is recorded in the DispatchRecord", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-13 Governance Budget
# --------------------------------------------------------------------------- #


def _scanner_pattern():
    path = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
    spec = importlib.util.spec_from_file_location("_scan_gates_078", path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOCKING_RE


def test_c13_skill_stays_external_and_new_lines_add_no_blocking_gate():
    text = _text(SKILL)
    assert "classification: external" in text
    body = _require_section(text, "Boundaries")
    assert re.search(r"governance-kept relay", body, re.IGNORECASE)
    assert re.search(r"subagent never self-approves", body, re.IGNORECASE)

    diff = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", FEATURE_BASE, "--", "skills", "shared",
         "templates/commands", "templates"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert diff.returncode == 0, diff.stderr
    added = [
        line[1:].rstrip("\n")
        for line in diff.stdout.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    pattern = _scanner_pattern()
    hits = [(number, line) for number, line in enumerate(added, start=1) if pattern.search(line)]
    assert hits == [], f"new blocking confirmation phrasing: {hits}"


# --------------------------------------------------------------------------- #
# C-14 Dual Independent Context
# --------------------------------------------------------------------------- #


def test_c14_payload_carries_only_the_two_readings_and_never_the_coach_conclusions():
    body = _require_section(_text(SKILL), "Boundaries")
    assert re.search(r"coach forms the expectation from its own reading", body, re.IGNORECASE)
    assert re.search(r"dispatch payload carries `<work>` verbatim", body, re.IGNORECASE)
    assert re.search(r"execute per the Trainee's own `SKILL\.md`", body, re.IGNORECASE)
    assert re.search(r"never carries the expectation, deviation guesses", body, re.IGNORECASE)
    assert re.search(r"never pre-digests `<work>`", body, re.IGNORECASE)
    assert re.search(r"divergence is a reportable\s+finding", body, re.IGNORECASE)
