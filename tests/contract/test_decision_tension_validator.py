"""Contract tests for ``scripts/python/validate-decision-tensions.py`` (Feature 076).

The checker is a runnable artifact, so this suite drives it through its real CLI
(``--spec <dir> [--json]``) and asserts exit codes, the closed six-label output and the
record-level dedup / cross-label precedence. It never re-implements the checker's parsing
in the test: a second copy of the grammar would be a second source of truth.

Fixtures are built as literals inside ``tmp_path`` (never checked in): one compliant plan
plus the inverse samples FR-017 requires. Each inverse sample is one textual mutation of
the compliant plan, so a red verdict names the mutation, not a fixture-maintenance issue.

Inverse samples (each a separate run):
  * delete any of the six field labels              -> ``dtr-record-incomplete``
  * ``expected_sacrifice: none``                    -> ``dtr-rejected-form``
  * undecidable wording instead of a trade-off      -> ``dtr-rejected-form``
  * duplicate ``tension_id``                        -> ``dtr-tension-id``
  * skipped ``tension_id`` (``T-001`` then ``T-003``) -> ``dtr-tension-id``
  * ``expected_sacrifice`` pointing at no declared source -> ``expected-sacrifice-unmapped``
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "python" / "validate-decision-tensions.py"

# The closed six-item label set, in the order the contract declares (FR-016 / C-2).
LABELS = (
    "dtr-anchor",
    "dtr-section-missing",
    "dtr-record-incomplete",
    "dtr-tension-id",
    "dtr-rejected-form",
    "expected-sacrifice-unmapped",
)

PLAN_HEAD = """# Implementation Plan: fixture

## Summary

Fixture plan for the decision-tension validator.

## Constitution Check

*GATE: fixture.*

"""

PLAN_TAIL = """
## Project Structure

Fixture structure.
"""

VALID_RECORD = """### T-001 — fixture decision

- **decision**: 选择方案 A，因为它在夹具里可判定。
- **antithesis**: 方案 B 是可独立采纳的具名方案；当吞吐需求高于 1k/s 时它更优。
- **binding_constraints**:
  - pole_a: 结果必须逐字节可复现。
  - pole_b: 实现必须能用现有工具链构建。
- **discriminating_evidence**: 运行一次 `pytest -q` 并比较退出码，结果二值。
- **expected_sacrifice**: SC-001 Source ↓ 低于阈值 90% 即重开。
- **revision_trigger**: 连续两次低于阈值 → 重开并复核。
"""

VALID_REQUIREMENTS = """# Requirements: fixture

## Success Criteria

- **SC-001**: fixture criterion.

### Measurement Sources & Collection Methods

- **SC-001 Source**: fixture measurement source.
"""


# --------------------------------------------------------------------------- #
# fixture builders
# --------------------------------------------------------------------------- #

def plan(*records: str) -> str:
    """A plan whose `##` sequence is Constitution Check -> Decision Tensions -> Project Structure."""
    body = "## Decision Tensions\n\n" + "\n".join(records) + "\n"
    return PLAN_HEAD + body + PLAN_TAIL


def record(tension_id: str = "T-001") -> str:
    return VALID_RECORD.replace("### T-001", f"### {tension_id}", 1)


def drop_field(record_id: str, field: str) -> str:
    """Delete one field label line — the record then misses that label entirely."""
    return "\n".join(
        line for line in record(record_id).splitlines()
        if not line.startswith(f"- **{field}**:")
    ) + "\n"


def set_value(record_id: str, field: str, value: str) -> str:
    lines = []
    for line in record(record_id).splitlines():
        if line.startswith(f"- **{field}**:"):
            lines.append(f"- **{field}**: {value}")
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def write_spec(tmp_path: Path, plan_text: str, requirements_text: str = VALID_REQUIREMENTS) -> Path:
    spec = tmp_path / "spec"
    spec.mkdir(parents=True)
    (spec / "plan.md").write_text(plan_text, encoding="utf-8")
    (spec / "requirements.md").write_text(requirements_text, encoding="utf-8")
    return spec


def run(spec_dir: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--spec", str(spec_dir), *extra],
        capture_output=True,
        text=True,
    )


def payload_of(proc: subprocess.CompletedProcess) -> dict:
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:  # pragma: no cover - surfaced as a readable failure
        raise AssertionError(
            f"--json did not print JSON; exit={proc.returncode} stdout={proc.stdout!r} "
            f"stderr={proc.stderr!r}"
        )


def counts_of(payload: dict) -> dict:
    return {check["label"]: check["count"] for check in payload["checks"]}


def load_module():
    """Import the real checker as a library — never a re-implementation of its parser."""
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    spec = importlib.util.spec_from_file_location("_decision_tension_validator", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- #
# C-1 — CLI contract and exit codes
# --------------------------------------------------------------------------- #

def test_cli_contract_and_exit_codes(tmp_path):
    spec = write_spec(tmp_path, plan(VALID_RECORD))

    ok = run(spec)
    assert ok.returncode == 0, f"compliant plan must exit 0:\n{ok.stdout}\n{ok.stderr}"
    assert re.search(r"(?m)^status: ok$", ok.stdout), ok.stdout

    (spec / "requirements.md").unlink()
    missing_requirements = run(spec)
    assert missing_requirements.returncode == 2, (
        "a missing requirements.md is unreadable input (2), not a record verdict (1):\n"
        f"{missing_requirements.stdout}"
    )

    write_spec(tmp_path / "second", plan(VALID_RECORD))
    second = tmp_path / "second" / "spec"
    (second / "plan.md").unlink()
    missing_plan = run(second)
    assert missing_plan.returncode == 2, "a missing plan.md is unreadable input (2)"

    write_spec(tmp_path / "third", plan(VALID_RECORD))
    third = tmp_path / "third" / "spec"
    (third / "plan.md").write_text("", encoding="utf-8")
    empty = run(third)
    assert empty.returncode == 2, "a plan without content lines is unreadable input (2)"

    write_spec(tmp_path / "fourth", plan(VALID_RECORD))
    fourth = tmp_path / "fourth" / "spec"
    (fourth / "plan.md").write_bytes(b"\xff\xfe\x00\x00 binary")
    undecodable = run(fourth)
    assert undecodable.returncode == 2, "an undecodable plan is unreadable input (2)"


# --------------------------------------------------------------------------- #
# C-2 — closed label set, dedup and cross-label precedence
# --------------------------------------------------------------------------- #

def test_label_set_closed_and_dedup_precedence(tmp_path):
    compliant = run(write_spec(tmp_path / "a", plan(VALID_RECORD)))
    printed = re.findall(r"\[([a-z-]+)\] (pass|fail) \((\d+)\)", compliant.stdout)
    assert [label for label, _status, _count in printed] == list(LABELS), (
        "the human output must print exactly the closed six labels, in the declared order; "
        f"found {printed!r}"
    )

    # (1) missing section: the anchor assertion necessarily reds, so it MUST be suppressed and
    # only `dtr-section-missing` may be reported (one root cause, one finding).
    no_section = run(
        write_spec(tmp_path / "b", PLAN_HEAD + PLAN_TAIL.lstrip("\n")), "--json"
    )
    no_section_payload = payload_of(no_section)
    no_section_counts = counts_of(no_section_payload)
    assert no_section.returncode == 1
    assert no_section_counts["dtr-section-missing"] == 1
    assert no_section_counts["dtr-anchor"] == 0, (
        "a missing section must suppress dtr-anchor (the adjacency assertion cannot pass)"
    )

    # (2) one record, one label, at most one finding: two missing field labels still yield a
    # single `dtr-record-incomplete` finding for that record.
    two_missing = drop_field("T-001", "decision")
    two_missing = "\n".join(
        line for line in two_missing.splitlines()
        if not line.startswith("- **revision_trigger**:")
    ) + "\n"
    dedup = run(write_spec(tmp_path / "c", plan(two_missing)), "--json")
    dedup_counts = counts_of(payload_of(dedup))
    assert dedup.returncode == 1
    assert dedup_counts["dtr-record-incomplete"] == 1, (
        "one record with two missing field labels must report ONE finding for that label"
    )


def test_anchor_requires_three_adjacent_headings(tmp_path):
    # Section present, but placed after `## Project Structure` — the sequence is not adjacent.
    moved = PLAN_HEAD + PLAN_TAIL + "\n## Decision Tensions\n\n" + VALID_RECORD
    proc = run(write_spec(tmp_path, moved), "--json")
    counts = counts_of(payload_of(proc))
    assert proc.returncode == 1
    assert counts["dtr-anchor"] == 1, (
        "a section that is not the direct successor of `## Constitution Check` must red the "
        f"anchor check; counts={counts!r}"
    )
    assert counts["dtr-section-missing"] == 0, (
        "the section exists, so the missing-section label must stay green"
    )


# --------------------------------------------------------------------------- #
# C-3 — output shape (human and --json)
# --------------------------------------------------------------------------- #

def test_output_shape_human_and_json(tmp_path):
    spec = write_spec(tmp_path, plan(VALID_RECORD))
    human = run(spec).stdout
    assert re.search(r"(?m)^status: ok$", human), human
    for label in LABELS:
        assert re.search(rf"(?m)^\s*\[{re.escape(label)}\] (pass|fail) \(\d+\)$", human), (
            f"missing per-label line for {label!r}:\n{human}"
        )
    # The channel mapping is printed by the program, so a report records its verdict instead of
    # a table a consumer fills in (review F4). The value domain is the declared HIGH-or-0.
    assert re.search(r"(?m)^channel: value_domain=HIGH-or-0, high=0$", human), human

    proc = run(spec, "--json")
    payload = payload_of(proc)
    # The six keys C-3 pins are all present; `channel` and `findings` are the additive surface
    # the analyze channel's severity mapping needs (every finding carries its own severity, and
    # the aggregate is HIGH-or-0). Nothing C-3 names was renamed or dropped.
    assert {
        "spec", "status", "checks", "errors", "warnings", "scanned",
    } <= set(payload), f"the C-3 envelope lost a declared key; got {sorted(payload)}"
    assert set(payload) == {
        "spec", "status", "checks", "errors", "warnings", "scanned", "channel", "findings",
    }, f"the --json envelope carries an undeclared field; got {sorted(payload)}"
    assert payload["status"] == "ok"
    assert payload["errors"] == 0 and payload["warnings"] == 0
    assert [check["label"] for check in payload["checks"]] == list(LABELS)
    assert all(set(check) == {"label", "status", "count", "severity"} for check in payload["checks"]), (
        "each check entry carries label/status/count plus its channel severity"
    )
    assert payload["channel"] == {"value_domain": "HIGH-or-0", "high": 0}, payload["channel"]
    assert [check["severity"] for check in payload["checks"]] == [0] * len(LABELS), (
        "a label that did not fire counts 0 — there is no advisory tier below HIGH"
    )


def test_channel_severity_is_high_per_finding_and_zero_for_quiet_labels(tmp_path):
    """The mapping is the program's, and it is the declared domain: HIGH or 0, nothing between."""
    spec = write_spec(tmp_path, PLAN_HEAD + PLAN_TAIL.lstrip("\n"))  # section absent
    proc = run(spec, "--json")
    payload = payload_of(proc)
    assert proc.returncode == 1
    assert payload["channel"]["value_domain"] == "HIGH-or-0"
    assert payload["channel"]["high"] == 1, (
        f"the program must count the channel's HIGH findings itself; got {payload['channel']!r}"
    )
    assert [finding["label"] for finding in payload["findings"]] == ["dtr-section-missing"]
    assert all(finding["severity"] == "HIGH" for finding in payload["findings"]), (
        f"every finding of this channel is HIGH; got {payload['findings']!r}"
    )
    fired = {check["label"]: check["severity"] for check in payload["checks"]}
    assert fired["dtr-section-missing"] == "HIGH"
    assert {label: value for label, value in fired.items() if label != "dtr-section-missing"} == {
        label: 0 for label in LABELS if label != "dtr-section-missing"
    }, f"a quiet label must read 0, never a lower tier: {fired!r}"


# --------------------------------------------------------------------------- #
# C-4 — inverse samples turn red (FR-017)
# --------------------------------------------------------------------------- #

INVERSE_SAMPLES = [
    pytest.param(lambda: plan(drop_field("T-001", f)), "dtr-record-incomplete",
                 id=f"delete-{f}") for f in (
                     "decision", "antithesis", "binding_constraints",
                     "discriminating_evidence", "expected_sacrifice", "revision_trigger",
                 )
] + [
    pytest.param(
        lambda: plan(set_value("T-001", "expected_sacrifice", "none")),
        "dtr-rejected-form",
        id="sacrifice-none",
    ),
    pytest.param(
        lambda: plan(set_value("T-001", "decision", "要平衡两方面的诉求，综合考虑后再定。")),
        "dtr-rejected-form",
        id="undecidable-wording",
    ),
    pytest.param(
        lambda: plan(record("T-001"), record("T-001")),
        "dtr-tension-id",
        id="duplicate-tension-id",
    ),
    pytest.param(
        lambda: plan(record("T-001"), record("T-003")),
        "dtr-tension-id",
        id="skipped-tension-id",
    ),
    pytest.param(
        lambda: plan(set_value("T-001", "expected_sacrifice", "SC-099 Source ↓ 无此来源")),
        "expected-sacrifice-unmapped",
        id="unmapped-measurement-source",
    ),
]


@pytest.mark.parametrize("mutate,label", INVERSE_SAMPLES)
def test_inverse_samples_turn_red(tmp_path, mutate, label):
    proc = run(write_spec(tmp_path, mutate()), "--json")
    payload = payload_of(proc)
    counts = counts_of(payload)
    assert proc.returncode == 1, (
        f"inverse sample {label!r} must exit 1 (a verdict, not unreadable input 2); "
        f"counts={counts!r} stdout={proc.stdout!r}"
    )
    assert counts[label] >= 1, (
        f"inverse sample {label!r} did not hit its declared label; counts={counts!r}"
    )


# --------------------------------------------------------------------------- #
# Cross-label precedence (FR-016 ①②③) — 「one root cause, one finding」
# --------------------------------------------------------------------------- #

def test_empty_value_or_literal_none_reports_only_the_rejected_form(tmp_path):
    """Precedence ③: an empty value has no decidable content, so nothing else may fire."""
    cases = {
        "blank-sacrifice": lambda: plan(set_value("T-001", "expected_sacrifice", "")),
        "literal-none": lambda: plan(set_value("T-001", "expected_sacrifice", "none")),
        "empty-pole": lambda: plan(set_value("T-001", "binding_constraints", "").replace(
            "  - pole_b: 实现必须能用现有工具链构建。", "  - pole_b:"
        )),
    }
    for name, mutate in cases.items():
        proc = run(write_spec(tmp_path / name, mutate()), "--json")
        counts = counts_of(payload_of(proc))
        assert proc.returncode == 1, f"{name}: a rejected form is a verdict (exit 1)"
        assert counts["dtr-rejected-form"] == 1, f"{name}: counts={counts!r}"
        assert counts["dtr-record-incomplete"] == 0, (
            f"{name}: an empty value must NOT also be counted as an incomplete record"
        )
        assert counts["expected-sacrifice-unmapped"] == 0, (
            f"{name}: an empty value must NOT also be counted as a failed mapping"
        )
        assert sum(counts.values()) == 1, f"{name}: exactly one finding; counts={counts!r}"


def test_missing_field_label_reports_only_the_record_incomplete(tmp_path):
    """Precedence ②: a missing label leaves no value to parse, so mapping never runs."""
    proc = run(write_spec(tmp_path, plan(drop_field("T-001", "expected_sacrifice"))), "--json")
    counts = counts_of(payload_of(proc))
    assert proc.returncode == 1
    assert counts["dtr-record-incomplete"] == 1, f"counts={counts!r}"
    assert counts["expected-sacrifice-unmapped"] == 0, (
        "a record missing the field label has no value to map; the mapping verdict is suppressed"
    )
    assert counts["dtr-rejected-form"] == 0, (
        "a missing field label is not an empty value; the rejected-form verdict stays silent"
    )
    assert sum(counts.values()) == 1, f"counts={counts!r}"


def test_undecidable_wording_still_leaves_the_mapping_verdict_running(tmp_path):
    """Undecidable wording is a rejected form, but the value stays parseable — both may fire."""
    mut = set_value("T-001", "decision", "要平衡两方面的诉求，综合考虑后再定。")
    mut = mut.replace(
        "- **expected_sacrifice**: SC-001 Source",
        "- **expected_sacrifice**: SC-099 Source",
    )
    proc = run(write_spec(tmp_path, plan(mut)), "--json")
    counts = counts_of(payload_of(proc))
    assert proc.returncode == 1
    assert counts["dtr-rejected-form"] == 1, f"counts={counts!r}"
    assert counts["expected-sacrifice-unmapped"] == 1, (
        "the undecidable-wording rejection must not suppress the mapping verdict; "
        f"counts={counts!r}"
    )


# --------------------------------------------------------------------------- #
# Record index export (T007) — one parser, two consumers (validator + ADR link check)
# --------------------------------------------------------------------------- #

def test_record_index_exported_for_adr_link_check():
    module = load_module()
    assert hasattr(module, "index_records"), (
        "the validator must export index_records() so the ADR dangling-link check reuses one "
        "parser instead of writing a second one (contracts/adr-reference.md C-2)"
    )
    index = module.index_records(plan(VALID_RECORD))
    assert set(index) == {"T-001"}, f"index keys must be tension ids; got {sorted(index)}"
    fields = index["T-001"]["fields"]
    assert fields["decision"].startswith("选择方案 A")
    assert fields["expected_sacrifice"].startswith("SC-001 Source")

    two = module.index_records(plan(record("T-001"), record("T-002")))
    assert set(two) == {"T-001", "T-002"}
