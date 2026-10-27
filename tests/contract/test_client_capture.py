"""Contract test: client capture — code-review findings into the client channel
(Feature 072, User Story 1).

Pins `contracts/capture-step.md` C-10…C-24 against the surfaces that own them:

* the **step enumeration** of the code segment's non-interactive path
  (`skills/internal/code-review/SKILL.md` § 非交互路径 — the one surface Feature
  072 is authorized to amend, C-10);
* the **`capture` subcommand** and the **`report --summary --format json`** form
  of `skills/internal/code-review/scripts/git-delta-review.sh` (C-11, C-17),
  driven for real inside the disposable client project built by
  `tests/fixtures/client_project.py` (the framework repository can never take
  the client branch of the hat predicate — C-58 — so every behavioural
  assertion here executes in the fixture, never as framework self-testing);
* the **feedback store** of that client project (entry count, pointer payload,
  idempotency) read back through the engine's own machine-readable list.

The armed-state branches not claimed by this group (unarmed / ambiguous /
explicit-unit-without-probe / registry-unavailable) are pinned by
`tests/contract/test_client_armed_state.py` (T009/T010); this group only needs
the armed path, the framework-hat refusal and the non-`run` refusal.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    ClientProject,
    make_client_project,
    make_framework_hat_twin,
)

pytestmark = pytest.mark.contract

REVIEW_SCRIPT = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
SKILL_MD = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "SKILL.md"
REPORT_TEMPLATE = FRAMEWORK_ROOT / "templates" / "review-template.md"

SPEC_DIR = ".specify/specs/072-demo"
RECORD_REL = f"{SPEC_DIR}/code-review.md"
STAMP = "20261027T000000Z"           # REVIEW_RUN_TIMESTAMP override (deterministic)
RUN_ID = "2026-10-27T00:00:00Z"      # the record header date stamp derived from it
UNIT = "custom:fixture/unit"

SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")

#: The closed five-value disclosure set (C-22 / STR-003/004/007/009/010).
FIVE_TOKENS = {
    "client-channel-armed",
    "client-channel-unarmed",
    "client-unit-ambiguous",
    "no-capture-object",
    "counts-unavailable",
}

#: Canonical subcommand surface (C-11).
CAPTURE_USAGE = "capture --review-file <record> --triage <value> [--unit <custom:owner/name>]"

HAT_OWNER_CITATION = "dogfooding-definitions.md"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def run_review(project: ClientProject, *args: str,
               extra_env: Optional[Dict[str, str]] = None):
    env = {"REVIEW_RUN_TIMESTAMP": STAMP}
    if extra_env:
        env.update(extra_env)
    return project.run_script(str(REVIEW_SCRIPT), *args, extra_env=env)


def capture_lines(stdout: str) -> List[str]:
    return [line for line in stdout.splitlines() if line.startswith("capture:")]


def external_count(project: ClientProject) -> int:
    return int(project.feedback_list_json(kind="external")["count"])


def entry_files(project: ClientProject) -> List[Path]:
    listing = project.feedback_list_json(kind="external")
    return [project.path / m["path"] for m in listing["matches"]]


def qualified_run(project: ClientProject):
    """Two commits with a code delta; triage=run; record created; two notes."""
    project.write("src/app.py", "def f():\n    return 1\n")
    project.commit("base", ["src/app.py"])
    project.write("src/app.py", "def f():\n    return 2\n")
    project.commit("change", ["src/app.py"])
    triage = run_review(project, "triage", "--since", "HEAD~1", "--head", "HEAD")
    assert triage.returncode == 0 and "triage=run" in triage.stdout, triage.describe()
    start = run_review(project, "start", "--spec", SPEC_DIR,
                       "--since", "HEAD~1", "--head", "HEAD", "--triage", "run")
    assert start.returncode == 0, start.describe()
    record = project.path / RECORD_REL
    assert record.is_file()
    for sev, comment in (("blocking", "defect body alpha"), ("praise", "nice work beta")):
        note = run_review(project, "note", "-s", sev, "-f", "src/app.py",
                          "-c", comment, "--review-file", RECORD_REL)
        assert note.returncode == 0, note.describe()
    receipt = run_review(project, "receipt", "--review-file", RECORD_REL,
                         "--since", "HEAD~1", "--head", "HEAD")
    assert receipt.returncode == 0, receipt.describe()
    return record


def armed_capture(project: ClientProject, *extra: str):
    return run_review(project, "capture", "--review-file", RECORD_REL,
                      "--triage", "run", *extra)


# --------------------------------------------------------------------------- #
# C-10 — the step enumeration is amended exactly once: four steps → five
# --------------------------------------------------------------------------- #

def test_c10_step_enumeration_is_five_steps_with_reason_and_cost():
    text = SKILL_MD.read_text(encoding="utf-8")
    heading_line = text.split("### 非交互路径", 1)[1].splitlines()[0]
    assert "五步" in heading_line, (
        f"the enumeration MUST read as five steps after the amendment; heading tail: {heading_line!r}"
    )
    section = text.split("### 非交互路径", 1)[1].split("\n## ", 1)[0]
    steps = re.findall(r"(?m)^\s*(\d+)\.\s+`(\w+)", section)
    assert [int(n) for n, _word in steps] == [1, 2, 3, 4, 5], (
        f"the non-interactive path MUST enumerate five ordered steps; found {steps!r}"
    )
    assert steps[4][1] == "capture", (
        "the fifth step MUST be the deterministic `capture` subcommand (client capture)"
    )
    assert "--review-file" in section and "--triage" in section, (
        "the fifth step MUST document the capture subcommand's parameter form"
    )
    assert "理由" in section and "代价" in section, (
        "C-10 requires the amendment to record its reason (理由) and cost (代价) at the revision point"
    )


# --------------------------------------------------------------------------- #
# C-11 — the capture subcommand surface
# --------------------------------------------------------------------------- #

def test_c11_capture_subcommand_parameter_form():
    with make_client_project() as project:
        run = run_review(project, "capture")
        assert "未知命令" not in run.stderr, "capture MUST be a subcommand of the existing script"
        assert run.returncode == 2, (
            f"capture with missing required args MUST exit 2 (input-error alphabet), got {run.returncode}"
        )
        assert "--review-file" in run.stderr and "--triage" in run.stderr, run.stderr
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    assert CAPTURE_USAGE in skill_text, (
        "the skill's fifth step MUST document the canonical parameter form "
        f"{CAPTURE_USAGE!r}"
    )


# --------------------------------------------------------------------------- #
# C-12 — trigger conjunction + exactly one entry; C-18 — (unit, run) idempotency
# --------------------------------------------------------------------------- #

def test_c12_capture_fires_once_and_is_idempotent():
    with make_client_project() as project:
        project.arm(UNIT)
        record = qualified_run(project)
        first = armed_capture(project, "--unit", UNIT)
        assert first.returncode == 0, first.describe()
        lines = capture_lines(first.stdout)
        assert len(lines) == 1, f"exactly one capture outcome line; got {lines!r}"
        assert "client-channel-armed" in lines[0] and "triage=run" in lines[0], lines[0]
        assert external_count(project) == 1, (
            "exactly one pointer entry regardless of the two notes (never per finding)"
        )
        listing = project.feedback_list_json(kind="external")
        entry = listing["matches"][0]
        assert entry["unit_id"] == UNIT and entry["run_id"] == RUN_ID, entry
        assert entry["kind"] == "external"
        # C-18/C-19: a second capture of the same record is answered by the
        # engine's duplicate result — no second entry, not an error.
        before = external_count(project)
        second = armed_capture(project, "--unit", UNIT)
        assert second.returncode == 0, second.describe()
        assert len(capture_lines(second.stdout)) == 1
        assert external_count(project) == before == 1


def test_c12_gate_deny_does_not_suppress_capture():
    """C-20 — a merge-gate denial (summary exit 1) still captures, verbatim counts."""
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        summary = run_review(project, "report", "--summary", "--file", RECORD_REL)
        assert summary.returncode == 1, (
            f"fixture run carries one blocking note — the gate MUST deny (exit 1); got {summary.returncode}"
        )
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert "client-channel-armed" in capture_lines(run.stdout)[0]
        assert external_count(project) == 1


# --------------------------------------------------------------------------- #
# C-13 — framework hat: no entry under any armed state, hat named, not a token
# --------------------------------------------------------------------------- #

def test_c13_framework_hat_writes_nothing_and_names_the_hat_verdict():
    with make_framework_hat_twin() as twin:
        twin.arm(UNIT)
        qualified_run(twin)
        run = armed_capture(twin, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert external_count(twin) == 0, (
            "the framework hat MUST gain zero external entries under any armed state"
        )
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        line = lines[0]
        assert "hat=framework" in line, line
        assert HAT_OWNER_CITATION in line, (
            "the refusal MUST cite the hat owner (dogfooding-definitions), not merely say skipped"
        )
        for token in FIVE_TOKENS:
            assert token not in line, (
                f"the hat-refusal line MUST NOT take the form of the five-value client token {token!r}"
            )


# --------------------------------------------------------------------------- #
# C-14 — applicability not `run`: no-capture-object, zero entries
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("triage_value", ["not-applicable", "not-evaluated"])
def test_c14_non_run_triage_discloses_no_capture_object(triage_value):
    with make_client_project() as project:
        project.arm(UNIT)
        run = run_review(project, "capture",
                         "--review-file", f"{SPEC_DIR}/code-review.md",
                         "--triage", triage_value, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0, "a non-run applicability MUST gain zero entries"
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        assert "no-capture-object" in lines[0], lines[0]
        assert f"triage={triage_value}" in lines[0], (
            "the disclosure MUST be visible together with the applicability value (C-22)"
        )
        assert "no record" in lines[0] or "无对象" in lines[0]


# --------------------------------------------------------------------------- #
# C-15 — the pointer payload's closed field set
# --------------------------------------------------------------------------- #

def test_c15_pointer_payload_is_a_closed_field_set_without_opinion_bodies():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        files = entry_files(project)
        assert len(files) == 1
        body = files[0].read_text(encoding="utf-8")
        review = body.split("## Review", 1)[1].split("## Optimization Points")[0].strip()
        expected = "\n".join([
            f"record={RECORD_REL}",
            "triage=run",
            "blocking=1",
            "important=0",
            "suggestion=0",
            "nitpick=0",
            "question=0",
            "praise=1",
            f"run={RUN_ID}",
            f"unit={UNIT}",
        ])
        assert review == expected, (
            "the entry MUST be a pointer with exactly the closed field set "
            "(record path, applicability, six counts, run id, unit); drift:\n"
            + "\n".join(
                f"  {a!r} != {b!r}" for a, b in zip(review.splitlines(), expected.splitlines())
                if a != b
            )
        )
        for forbidden in ("defect body alpha", "nice work beta", "src/app.py",
                          "changed_files", "judged_files", "gap_files",
                          "lines_added", "lines_deleted"):
            assert forbidden not in body, (
                f"the pointer entry MUST NOT carry {forbidden!r} (no bodies, per-file lists, file counts)"
            )


# --------------------------------------------------------------------------- #
# C-16 — the six counts are copied verbatim from the summary command's JSON
# --------------------------------------------------------------------------- #

def test_c16_six_counts_verbatim_from_summary_json_including_zeros():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        summary = run_review(project, "report", "--summary", "--file", RECORD_REL,
                             "--format", "json")
        assert summary.returncode == 1, summary.describe()  # one blocking note → deny
        payload = json.loads(summary.stdout.strip().splitlines()[-1])
        assert payload["record"] == RECORD_REL
        assert payload["gate"] == "deny"
        assert payload["blocking_entries"] == payload["counts"]["blocking"] == 1
        assert set(payload["counts"]) == set(SEVERITIES), (
            "the JSON form MUST carry all six severity levels, zero values included"
        )
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        body = entry_files(project)[0].read_text(encoding="utf-8")
        for sev in SEVERITIES:
            assert f"{sev}={payload['counts'][sev]}" in body, (
                f"the entry MUST copy the {sev!r} count verbatim from the summary JSON "
                f"({payload['counts'][sev]}), zeros included"
            )


# --------------------------------------------------------------------------- #
# C-17 — text output and the exit alphabet are unchanged by the JSON opt-in
# --------------------------------------------------------------------------- #

def test_c17_text_summary_output_and_exit_alphabet_unchanged():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        text = run_review(project, "report", "--summary", "--file", RECORD_REL)
        assert text.returncode == 1 and "gate=deny" in text.stdout
        assert "[blocking]" in text.stdout and "Review 汇总" in text.stdout
        assert '"counts"' not in text.stdout, (
            "without --format json the human text form MUST be byte-shaped as before"
        )
        bad = run_review(project, "report", "--summary", "--file", "no/such/record.md")
        assert bad.returncode == 2, (
            f"the input-error alphabet (2) MUST hold for the JSON form too; got {bad.returncode}"
        )


# --------------------------------------------------------------------------- #
# C-19 — no overreach: the record and its receipt block are never edited
# --------------------------------------------------------------------------- #

def test_c19_capture_never_edits_the_record_or_receipt_block():
    with make_client_project() as project:
        project.arm(UNIT)
        record = qualified_run(project)
        before = hashlib.sha256(record.read_bytes()).hexdigest()
        receipt_span = record.read_text(encoding="utf-8").split(
            "<!-- coverage-receipt:begin -->")[1]
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        after = hashlib.sha256(record.read_bytes()).hexdigest()
        assert before == after, "capture MUST NOT edit the code-segment record (no overreach)"
        assert receipt_span in record.read_text(encoding="utf-8"), (
            "the receipt's field block MUST survive capture untouched"
        )


# --------------------------------------------------------------------------- #
# C-21 — counts-unavailable on summary exit 2 or engine refusal; zero entries
# --------------------------------------------------------------------------- #

def test_c21_summary_exit_2_discloses_counts_unavailable():
    with make_client_project() as project:
        project.arm(UNIT)
        run = run_review(project, "capture",
                         "--review-file", f"{SPEC_DIR}/code-review.md",
                         "--triage", "run", "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0, "counts-unavailable MUST gain zero entries"
        line = capture_lines(run.stdout)[0]
        assert "counts-unavailable" in line and "triage=run" in line, line


def test_c21_engine_refusal_discloses_counts_unavailable_and_never_blocks():
    with make_client_project() as project:
        # No probe injected for the unit → the engine refuses the write.
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, (
            f"capture failure MUST NOT block the run (exit 0); got {run.returncode}: {run.describe()}"
        )
        assert external_count(project) == 0
        line = capture_lines(run.stdout)[0]
        assert "counts-unavailable" in line, line


# --------------------------------------------------------------------------- #
# C-22/C-23 — exactly one outcome line, named reason, no empty entry
# --------------------------------------------------------------------------- #

def test_c22_exactly_one_outcome_line_with_token_and_applicability_visible():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        token = next(t for t in FIVE_TOKENS if t in lines[0])
        assert token == "client-channel-armed"


def test_c23_no_phoenix_empty_entry_for_failed_capture():
    with make_client_project() as project:
        qualified_run(project)  # unarmed: engine would refuse
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0
        assert external_count(project) == 0
        body_words = entry_files(project)
        assert body_words == [], "no empty or zero-filled entry may substitute for the named reason"
        line = capture_lines(run.stdout)[0]
        assert "无发现" not in line and "no findings" not in line.lower()


# --------------------------------------------------------------------------- #
# C-24 — the disclosure stays out of the record and the report's closed lists
# --------------------------------------------------------------------------- #

def test_c24_disclosure_lives_only_in_the_run_conclusion():
    with make_client_project() as project:
        project.arm(UNIT)
        record = qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0
        record_text = record.read_text(encoding="utf-8")
        for token in FIVE_TOKENS:
            assert token not in record_text, (
                f"the disclosure MUST NOT be written into the record/receipt surface; found {token!r}"
            )
        template = REPORT_TEMPLATE.read_text(encoding="utf-8")
        subsection = template.split("### 2.1")[1]
        assert "capture" not in subsection and "client-channel" not in subsection, (
            "the report's code-subsection field list is a 071 closed surface and MUST NOT gain capture fields"
        )
