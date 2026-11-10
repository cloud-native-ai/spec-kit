"""Contract tests for Feature 081, slice 081b — runtime stack, premises, inherited blockers.

This is the slice's **single** test carrier (``plan.md`` § D10 names it). It judges the two
producers that must agree — ``skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`` at its
stage gates and ``scripts/python/closure-acceptance-check.py`` at closure — against one closed set.

=====  =======================================================================================
leg    what it pins
=====  =======================================================================================
(a)    the four findings fire on the four mutation fixtures, and every emitted instance is a
       member of the closed set by the **two-part test** of ``requirements.md`` § Shared
       Strings — byte-identical template prefix plus a well-formed argument — *including the
       reserved argument* ``runtime-stack``, which is the only argument slot that is a literal
       rather than an id
(a2)   the accepting fixtures (``positive``, ``inherited-clean``) emit none of the four: a judge
       that fires on everything is not a judge
(b)    the three ``in-scope`` duties are judged **at three different stages**: an empty or
       unresolvable ``FR`` cell is an input error (exit 2) and never a block; a missing
       joint-acceptance row naming that ``RS-NNN`` blocks at closure; the tasks-side duty is a
       **line-level** match, with a table-only counterexample that MUST NOT satisfy it
(c)    the ``inherited`` carrier rule on purpose-built row sets: empty, unparseable,
       unresolvable and ``supporting``-path-SC carriers are judged **the same** — one
       undisposed row under one reason — while ``task:<T-ID>+test:<path>`` and
       ``gate:<GATE-ID>`` pass
(c2)   the join key: a locator disposed twice is an input error; an extracted row with no
       disposition row is a finding; ``inherited-clean`` is the counterexample proving rows are
       really *discovered*, and its ``inherited-later`` row neither blocks nor reads as resolved
(d)    cross-producer agreement: for every mutation fixture both producers name the same instance
(e)    pin validity: a runner reading that differs from the recorded pin makes the comparison an
       input error, never a new failure
(f)    the A13 boundary is stated **once** and the two plan skeletons only point at it
(g)    the runtime-row class's three shapes are three verdicts — absent ⇒ exit 2, zero data
       rows ⇒ the reserved argument, an empty required cell ⇒ its own ``RS-NNN``
(h)    the prose rule's arms: marked + id fires; marked without an id is an input error; an
       unmarked narrative mention does not fire; a marker inside a fenced code block does not
       fire
=====  =======================================================================================

**Reason instances are read from the findings' message tail.** The finding shape is fixed at
``check`` / ``severity`` / ``path`` / ``line`` / ``message`` (``contracts/gate-wiring.contract.md``
GW-07), so a finding carries its reason instance in the message, introduced by the literal
``reason: `` and running to the end of the message. This module asserts that tail is a *member*,
never that it contains a substring: a checker that emitted a third spelling would pass a
substring test and fail this one.

Red-first (Constitution IV, ``tasks.md`` DoD-2): legs (a), (b-closure), (c), (c2), (d) and (g/h)
were red before T006/T008 landed the findings and the extraction. The measured red run — command,
output, exit status, failing count — is recorded in
``.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081b.md`` § 1.1; nothing here
claims a red that was not run.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process
import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
PRE = ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "pre-analyze-check.py"
CLOSURE = ROOT / "scripts" / "python" / "closure-acceptance-check.py"
FIXTURES = ROOT / "tests" / "fixtures" / "acceptance-hardening"
SPEC = ROOT / ".specify" / "specs" / "081-acceptance-hardening"
REQUIREMENTS = SPEC / "requirements.md"
OWNER = ROOT / "shared" / "workflow" / "acceptance-hardening.md"
PLAN_TEMPLATE = ROOT / "templates" / "plan-template.md"
PINS = SPEC / "test-evidence" / "plan-runner-pins.txt"

#: The seven templates' declaring ids, in table order (`## Shared Strings`, octets 008…014).
REASON_IDS = ("STR-008", "STR-009", "STR-010", "STR-011", "STR-012", "STR-013", "STR-014")

#: Argument grammars for the five argument-taking templates. `<feature>:<row>` admits no
#: whitespace because the locator is written by the dependency artifact exactly as it appears
#: there.
ARG_GRAMMAR = {
    "STR-009": r"SC-\d{3}",
    "STR-010": r"SC-\d{3}",
    "STR-011": r"RS-\d{3}",
    "STR-012": r"EP-\d{3}",
    "STR-013": r"\S+:\S+",
}

#: The one **reserved** argument slot: the zero-data-row shape has no `RS-NNN` to name
#: (`requirements.md` § Shared Strings). It is a member of STR-011 and of nothing else.
RESERVED_ARGUMENTS = {"STR-011": "runtime-stack"}

#: The four findings' fixed `check` names (`contracts/gate-wiring.contract.md` GW-07). Fixed so a
#: waiver key is writable and an accidental weakening is visible.
FINDING_CHECKS = (
    "runtime-stack-row",
    "runtime-contract-incomplete",
    "premise-undecided",
    "inherited-blocker",
)

#: The mutations the four findings are proved on, and the instances each must produce.
MUTATIONS = {
    "premise-mutation": ("falsified-premise-undecided: EP-001",),
    "runtime-gap-mutation": (
        "runtime-dependency-not-owned: RS-905",
        "runtime-dependency-not-owned: RS-001",
    ),
    "runtime-zero-row": ("runtime-dependency-not-owned: runtime-stack",),
    "inherited-mutation": (
        "inherited-blocker-undisposed: 901:SC-004_status",
        "inherited-blocker-undisposed: 901:SC-003_status",
    ),
}

#: The fixtures that MUST come out clean — the counter-examples that keep the judge honest.
ACCEPTING = ("positive", "inherited-clean")

#: The domain literals a plan skeleton MUST NOT carry (`contracts/artifact-schemas.contract.md`
#: AS-15: column names only, zero value-domain literals).
DOMAIN_LITERALS = (
    "in-scope",
    "signed-contract",
    "user-waived",
    "not-required",
    "verified",
    "unverified",
    "falsified",
    "resolve-in-scope",
    "user-waiver",
    "not-applicable",
    "resolved",
)

REASON_TAIL = re.compile(r"reason:\s*(\S.*)$")


# --------------------------------------------------------------------------- #
# The closed reason set — read from the owner of the literals, never copied here
# --------------------------------------------------------------------------- #
def _templates():
    """{STR-id: template} out of the declaring spec's Shared Strings table."""
    text = REQUIREMENTS.read_text(encoding="utf-8")
    rows = dict(re.findall(r"(?m)^\| `(STR-0\d\d)` \| `([^`]+)` \|", text))
    missing = [sid for sid in REASON_IDS if sid not in rows]
    assert not missing, "requirements.md no longer declares %r — the closed set moved" % (missing,)
    return {sid: rows[sid] for sid in REASON_IDS}


def _split(template):
    """`(prefix, argument-placeholder-or-None)`; the split is on the FIRST `": "`."""
    prefix, sep, arg = template.partition(": ")
    return prefix, (arg if sep else None)


def _is_member(reason):
    """The two-part membership test: template match AND a well-formed argument.

    The reserved argument is admitted for the one template that declares it, and for no other:
    `runtime-stack` is not an `RS-NNN`, so a checker that emitted it under any other prefix
    would be outside the set.
    """
    for sid, template in _templates().items():
        prefix, arg = _split(template)
        if arg is None:
            if reason == prefix:
                return True
            continue
        if not reason.startswith(prefix + ": "):
            continue
        tail = reason[len(prefix) + 2:]
        if re.fullmatch(ARG_GRAMMAR[sid], tail):
            return True
        reserved = RESERVED_ARGUMENTS.get(sid)
        if reserved is not None and tail == reserved:
            return True
    return False


def _instance(reason):
    """`{code, target}` → the emitted instance, `code + ": " + target` (or the bare code)."""
    code = reason.get("code", "")
    target = reason.get("target") or ""
    return code if not target else "%s: %s" % (code, target)


def _reason_tail(finding):
    """The reason instance a `pre-analyze-check.py` finding carries, or None."""
    match = REASON_TAIL.search(finding.get("message", ""))
    return match.group(1).strip() if match else None


def _instances(record):
    """Every reason instance the gate emitted, in finding order (duplicates preserved)."""
    tails = [_reason_tail(f) for f in record.get("findings", []) if f.get("severity") == "error"]
    assert all(tails), (
        "every blocking finding MUST carry its reason instance in the message tail "
        "(`reason: <instance>`), got %r"
        % ([f for f in record.get("findings", []) if f.get("severity") == "error"],)
    )
    return tails


# --------------------------------------------------------------------------- #
# Running the two producers
# --------------------------------------------------------------------------- #
def _fixture(name):
    path = FIXTURES / name
    assert path.is_dir(), "fixture set %r is missing — T001 has not landed" % name
    return path


def _copy_fixture(name, tmp_path):
    """A private copy of one fixture, so a mutation never edits the declarative corpus."""
    target = tmp_path / name
    shutil.copytree(_fixture(name), target)
    return target


def _rewrite(path, old, new):
    """Replace `old` with `new` in `path`, asserting the edit target exists exactly once."""
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, (
        "%s: the edit target appears %d times, expected exactly 1: %r"
        % (path, text.count(old), old)
    )
    path.write_text(text.replace(old, new), encoding="utf-8")


def _pre(spec_dir, stage="plan"):
    """Run the stage gate. `--repo` is the checkout, so a `Contract` cell resolves for real."""
    cmd = ["--spec-dir", str(spec_dir), "--stage", stage, "--repo", str(ROOT)]
    return run_engine_in_process(PRE, cmd)


def _pre_record(proc):
    assert proc.stdout.strip(), "the gate printed no payload:\n%s" % proc.stderr
    return json.loads(proc.stdout)


def _closure(spec_dir, *args):
    cmd = [sys.executable, str(CLOSURE), "--spec-dir", str(spec_dir), "--json", *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


def _closure_payload(spec_dir, *args):
    proc = _closure(spec_dir, *args)
    assert proc.stdout.strip(), "no closure payload on stdout:\n%s" % proc.stderr
    return proc, json.loads(proc.stdout)


def _closure_instances(spec_dir):
    _, payload = _closure_payload(spec_dir)
    return [_instance(r) for r in payload.get("reasons", [])]


# --------------------------------------------------------------------------- #
# (a) the four findings, through the stage gate, on the four mutation fixtures
# --------------------------------------------------------------------------- #
def test_a_every_mutation_fixture_blocks_with_member_instances():
    """Each mutation blocks, each instance is a member, and no fifth finding class exists."""
    for name, expected in MUTATIONS.items():
        record = _pre_record(_pre(_fixture(name)))
        assert record["decision"] == "fail", (name, record)
        instances = _instances(record)
        assert set(expected) <= set(instances), (name, instances)
        for instance in instances:
            assert _is_member(instance), (
                "%s emitted %r, which is outside the closed set — membership is template match "
                "plus a well-formed argument, not a third spelling" % (name, instance)
            )
        checks = {f["check"] for f in record["findings"] if f["severity"] == "error"}
        assert checks <= set(FINDING_CHECKS), (
            "%s produced finding classes %r; the set is closed at the four named in GW-07"
            % (name, sorted(checks - set(FINDING_CHECKS)))
        )
        for finding in record["findings"]:
            if finding["check"] in FINDING_CHECKS:
                assert finding["severity"] == "error", (
                    "an `advisory` severity would let 'must block' degrade into a note nothing "
                    "reads (GW-07): %r" % (finding,)
                )


def test_a2_accepting_fixtures_emit_none_of_the_four():
    """`positive` and `inherited-clean` are the two counter-examples; both MUST come out clean.

    Without this leg the four findings could be an unconditional `add(...)` in disguise.
    """
    for name in ACCEPTING:
        record = _pre_record(_pre(_fixture(name)))
        assert record["decision"] == "pass", (name, record["findings"])
        assert not [f for f in record["findings"] if f["check"] in FINDING_CHECKS], (
            "%s must not fire a finding of any of the four classes: %r"
            % (name, record["findings"])
        )


def test_a3_the_reserved_argument_is_a_member_of_its_own_template_only():
    """Anti-vacuity for the membership test itself: the reserved slot is not a wildcard."""
    assert _is_member("runtime-dependency-not-owned: runtime-stack")
    assert _is_member("runtime-dependency-not-owned: RS-905")
    assert _is_member("inherited-blocker-undisposed: 901:SC-004_status")
    for outsider in (
        "runtime-dependency-not-owned: runtime_stack",
        "runtime-dependency-not-owned: runtime-stack-2",
        "falsified-premise-undecided: runtime-stack",
        "inherited-blocker-undisposed: runtime-stack",
        "runtime-dependency-not-owned:",
        "runtime-dependency-not-owned",
    ):
        assert not _is_member(outsider), "%r must not be a member of the closed set" % outsider


# --------------------------------------------------------------------------- #
# (b) the three `in-scope` duties, each at its own stage
# --------------------------------------------------------------------------- #
def test_b1_an_empty_fr_cell_is_an_input_error_and_never_a_block(tmp_path):
    """Duty ① at the requirements stage: a defective cell is a fact about the artifact."""
    spec = _copy_fixture("positive", tmp_path)
    _rewrite(spec / "requirements.md", "| FR-001 |", "|  |")
    proc = _pre(spec, stage="requirements")
    assert proc.returncode == 2, (
        "an `in-scope` row with an empty `FR` cell MUST be an input error (exit 2), never a "
        "`block`: %s%s" % (proc.stdout, proc.stderr)
    )
    assert "FR" in proc.stderr, proc.stderr


def test_b1b_an_unresolvable_fr_cell_is_an_input_error(tmp_path):
    """Duty ①'s second arm: the cell resolves to an FR that this specification does not define."""
    spec = _copy_fixture("positive", tmp_path)
    _rewrite(spec / "requirements.md", "| FR-001 |", "| FR-909 |")
    proc = _pre(spec, stage="requirements")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "FR-909" in proc.stderr, proc.stderr


def test_b2_a_missing_joint_acceptance_row_blocks_at_closure(tmp_path):
    """Duty ③ at closure: no stage gate takes `verification.md` as input, so closure judges it."""
    spec = _copy_fixture("positive", tmp_path)
    verification = spec / "verification.md"
    verification.write_text(
        re.sub(r"(?m)^RS-001_joint_acceptance=.*\n", "", verification.read_text("utf-8")),
        encoding="utf-8",
    )
    proc, payload = _closure_payload(spec)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    instances = [_instance(r) for r in payload["reasons"]]
    assert "runtime-dependency-not-owned: RS-001" in instances, instances


def test_b3_the_tasks_duty_is_line_level_and_a_table_row_never_satisfies_it(tmp_path):
    """Duty ② at the tasks stage, with the counterexample the requirement names.

    The `positive` fixture quotes `FR-001` in a **task row**; moving that mention into a table
    cell leaves the whole-file substring intact (asserted below) while the line-level match
    fails — which is exactly the judging rule FR-009 forbids substituting.
    """
    clean = _pre_record(_pre(_fixture("positive"), stage="tasks"))
    assert not [r for r in _instances(clean) if r.startswith("runtime-dependency-not-owned")], (
        clean["findings"]
    )

    spec = _copy_fixture("positive", tmp_path)
    tasks = spec / "tasks.md"
    _rewrite(
        tasks,
        "- [X] T001 Delivers FR-001: the fixture's runtime capability is in place.",
        "- [X] T001 Delivers the fixture's runtime capability.",
    )
    text = tasks.read_text(encoding="utf-8")
    tasks.write_text(
        text + "\n| Task | FR |\n|------|----|\n| T001 | FR-001 |\n", encoding="utf-8"
    )
    mutated = tasks.read_text(encoding="utf-8")
    assert "FR-001" in mutated, (
        "the counterexample must keep the whole-file substring intact, or it proves nothing"
    )

    record = _pre_record(_pre(spec, stage="tasks"))
    instances = _instances(record)
    assert "runtime-dependency-not-owned: RS-001" in instances, (
        "an FR named only in a table row MUST NOT satisfy the tasks-side duty: %r" % (instances,)
    )


# --------------------------------------------------------------------------- #
# (c) the `inherited` carrier rule — one reason for every way to fail
# --------------------------------------------------------------------------- #
CARRIER_CELL = (
    "| `task:T004+test:tests/contract/test_acceptance_premises.py` | `this-slice` |"
)


def _with_carrier(target_dir, carrier, slice_value="this-slice"):
    """A copy of `inherited-clean` whose row `IB-003` carries `carrier` instead."""
    spec = Path(target_dir)
    shutil.copytree(_fixture("inherited-clean"), spec)
    _rewrite(spec / "plan.md", CARRIER_CELL, "| %s | `%s` |" % (carrier, slice_value))
    return spec


def test_c1_carrier_failures_are_one_undisposed_row_under_one_reason(tmp_path):
    """Missing, unparseable, unresolvable and ineligible carriers are judged **the same**."""
    cases = {
        "missing": "",
        "unparseable": "`not-a-carrier`",
        "unresolvable-task-id": "`task:T999+test:tests/contract/test_acceptance_premises.py`",
        "unresolvable-test-path": "`task:T004+test:tests/contract/test_no_such_module.py`",
        "unresolvable-gate": "`gate:GATE-9`",
        "supporting-path-SC": "`SC-002`",
    }
    for label, carrier in cases.items():
        spec = _with_carrier(tmp_path / label, carrier)
        record = _pre_record(_pre(spec))
        instances = _instances(record)
        assert "inherited-blocker-undisposed: 901:SC-002_status" in instances, (
            "%s: an `inherited` row whose carrier cannot carry the measurement is judged as an "
            "undisposed row, under the same reason: %r" % (label, instances)
        )
        assert instances.count("inherited-blocker-undisposed: 901:SC-002_status") == 1, (
            "%s: one row yields one finding, not one per failed limb: %r" % (label, instances)
        )


def test_c2_the_two_legal_carrier_forms_pass(tmp_path):
    """`task:<T-ID>+test:<path>` (both parts) and `gate:<GATE-ID>` resolve, so nothing fires."""
    clean = _pre_record(_pre(_fixture("inherited-clean")))
    assert clean["decision"] == "pass", clean["findings"]

    plan = (_fixture("inherited-clean") / "plan.md").read_text(encoding="utf-8")
    assert "`gate:GATE-1`" in plan, "the passing gate-carrier form must stay exercised"
    assert CARRIER_CELL in plan, "the passing conjunctive task-carrier form must stay exercised"
    tasks = (_fixture("inherited-clean") / "tasks.md").read_text(encoding="utf-8")
    row = [line for line in tasks.splitlines()
           if line.startswith("- [") and "T004" in line]
    assert row and "tests/contract/test_acceptance_premises.py" in row[0], (
        "the conjunctive form's second limb is that the test path appears verbatim in the task "
        "row's own description: %r" % (row,)
    )

    gate_form = _with_carrier(tmp_path / "gate-form", "`gate:GATE-1`")
    record = _pre_record(_pre(gate_form))
    assert record["decision"] == "pass", (
        "a `gate:<GATE-ID>` carrier that resolves must pass: %r" % (record["findings"],)
    )


def test_c2b_the_supporting_path_criterion_really_is_supporting():
    """The ineligible carrier is only ineligible because the criterion is `supporting`."""
    text = (_fixture("inherited-clean") / "requirements.md").read_text(encoding="utf-8")
    line = [ln for ln in text.splitlines() if ln.startswith("- **SC-002**")]
    assert line, "the fixture must define SC-002"
    assert line[0].rstrip().endswith("**Path**: supporting"), (
        "an `inherited` carrier is ineligible precisely because a `supporting`-path SC may be "
        "deferred; the fixture must keep that shape: %r" % line[0]
    )


# --------------------------------------------------------------------------- #
# (c2) the join key
# --------------------------------------------------------------------------- #
def _append_inherited_row(path, row):
    lines = path.read_text(encoding="utf-8").splitlines()
    last = max(index for index, line in enumerate(lines) if line.startswith("| IB-"))
    lines.insert(last + 1, row)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_c3_a_locator_disposed_twice_is_an_input_error(tmp_path):
    """The join key must be unique, or no disposition can be joined to an extracted row."""
    spec = _copy_fixture("inherited-clean", tmp_path)
    _append_inherited_row(
        spec / "plan.md",
        "| IB-007 | `901:deferred_tasks` | resolved | — | — | a second disposition for one key |",
    )
    proc = _pre(spec)
    assert proc.returncode == 2, (
        "two dispositions for one locator is a defective cell, not a verdict: %s%s"
        % (proc.stdout, proc.stderr)
    )
    assert "901:deferred_tasks" in proc.stderr, proc.stderr


def test_c4_extraction_discovers_rows_and_inherited_clean_is_the_counterexample():
    """The pair is the anti-vacuity: same dependency side, one undisposed row apart.

    `inherited-mutation` leaves one extracted row without a disposition; `inherited-clean`
    disposes all six. A judge that only inspected the rows it was handed could not tell the two
    apart, so the difference proves extraction runs.
    """
    mutation = _instances(_pre_record(_pre(_fixture("inherited-mutation"))))
    assert "inherited-blocker-undisposed: 901:SC-004_status" in mutation, mutation
    clean = _instances(_pre_record(_pre(_fixture("inherited-clean"))))
    assert not [r for r in clean if r.startswith("inherited-blocker-undisposed")], clean


def test_c5_an_inherited_later_row_neither_blocks_nor_reads_as_resolved(tmp_path):
    """`Carrier slice` = a later slice is a *reading*: disclosed, non-blocking — and conditional.

    The condition is mechanical: a later slice is legal only while the parent feature's claimed
    status is `Blocked`. Flip that claim and the same row stops being `inherited-later`, so its
    `test:`-only carrier no longer resolves — which is what makes the reading a judgement and
    not a comment.
    """
    clean = _pre_record(_pre(_fixture("inherited-clean")))
    assert clean["decision"] == "pass", clean["findings"]

    spec = _copy_fixture("inherited-clean", tmp_path)
    _rewrite(spec / "feature-detail.md", "**Status**: Blocked", "**Status**: Implemented")
    record = _pre_record(_pre(spec))
    instances = _instances(record)
    assert "inherited-blocker-undisposed: 901:deferred_tasks" in instances, (
        "with the parent no longer `Blocked`, a later-slice carrier is illegal and the row "
        "becomes an undisposed row under the same reason: %r" % (instances,)
    )


# --------------------------------------------------------------------------- #
# (d) cross-producer agreement
# --------------------------------------------------------------------------- #
def test_d_both_producers_name_the_same_instance_for_every_mutation():
    """Two producers, one closed set of templates, no second spelling.

    This leg is what keeps the gate and the closure verdict from drifting: they are separate
    programs, and the only thing that ties them together is the instance set they emit.
    """
    for name, expected in MUTATIONS.items():
        gate = _instances(_pre_record(_pre(_fixture(name))))
        closure = _closure_instances(_fixture(name))
        for instance in expected:
            assert instance in gate, (name, "gate", gate)
            assert instance in closure, (name, "closure", closure)
        assert set(gate) == set(closure), (
            "%s: the two producers disagree — gate %r vs closure %r (one closed set of "
            "templates, no second spelling)" % (name, sorted(set(gate)), sorted(set(closure)))
        )


# --------------------------------------------------------------------------- #
# (d2) the real-spec shape, the declaration marker, and the absent sentinel
# --------------------------------------------------------------------------- #
def test_d2_the_real_spec_dir_emits_no_phantom_inherited_row():
    """The shape a real plan has — and the two ways the fixtures cannot reproduce it.

    A fixture declares dependency files by fixture-local names and carries a
    `feature-detail.md`; a real spec dir mentions its own `verification.md` in prose and reads its
    claimed status from the repository registry. Both producers must agree on the real dir with
    no fabricated `081:*` row (F1) and with the legal `inherited-later` row accepted (F2).
    """
    record = _pre_record(_pre(SPEC))
    assert record["decision"] == "pass", record["findings"]
    inherited = [f for f in record["findings"] if f["check"] == "inherited-blocker"]
    assert not inherited, inherited
    closure = _closure_instances(SPEC)
    assert not [r for r in closure if r.startswith("inherited-blocker-undisposed")], closure


def test_d3_a_dependency_set_without_the_declaration_block_is_an_input_error(tmp_path):
    """An absent declaration MUST NOT silently disable the fourth finding (F3)."""
    target = _copy_fixture("inherited-clean", tmp_path)
    plan = target / "plan.md"
    text = plan.read_text(encoding="utf-8")
    start = text.index("**Dependency artifacts")
    end = text.index("**Extraction reading**")
    plan.write_text(text[:start] + text[end:], encoding="utf-8")

    gate = _pre(target)
    assert gate.returncode == 2, (gate.returncode, gate.stderr)
    assert "Dependency artifacts" in gate.stderr
    closure = _closure(target)
    assert closure.returncode == 2, (closure.returncode, closure.stdout, closure.stderr)


def test_d4_a_dash_source_row_is_the_absent_sentinel(tmp_path):
    """`—` and `(none)` are two spellings of "this row disposes nothing" (F4)."""
    target = _copy_fixture("positive", tmp_path)
    _rewrite(target / "plan.md", "| IB-001 | (none) |", "| IB-001 | — |")

    gate = _pre(target)
    assert gate.returncode == 0, (gate.returncode, gate.stderr, gate.stdout)
    closure, payload = _closure_payload(target)
    assert closure.returncode == 0, (closure.returncode, payload)


def test_d5_the_declaration_marker_is_published_once_in_the_owner_and_the_skeleton():
    """The marker is a fixed literal, not an implementation detail (F3)."""
    marker = "**Dependency artifacts (declared, never implied)**"
    assert marker in OWNER.read_text(encoding="utf-8")
    assert marker in PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependency set: none" in OWNER.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# (e) pin validity
# --------------------------------------------------------------------------- #
class PinMismatch(Exception):
    """The **input-error** class: a stale pin invalidates the comparison (AS-07 / FR-023).

    Deliberately not an `AssertionError`: a mismatch is a defect of the comparison's input, and
    reading it as a new failure is the mistake the rule exists to prevent.
    """


def _pins():
    """{tool: reading} out of the recorded pin file."""
    text = PINS.read_text(encoding="utf-8")
    return dict(re.findall(r"(?m)^(pytest|git) --version\s*=>\s*(.+?)\s*$", text))


def _live_readings():
    git = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return {
        "pytest": "pytest %s" % getattr(pytest, "__version__", ""),
        "git": git.stdout.strip(),
    }


def _assert_pin(tool, reading):
    """Compare one reading against its recorded pin; a difference is an input error."""
    pins = _pins()
    if tool not in pins:
        raise PinMismatch("no recorded pin for %r in %s" % (tool, PINS))
    if reading.strip() != pins[tool].strip():
        raise PinMismatch(
            "%s reads %r but %s records %r — the comparison is invalid (input error, exit 2), "
            "which is not a new failure" % (tool, reading.strip(), PINS.name, pins[tool].strip())
        )
    return True


def test_e_a_stale_pin_invalidates_the_comparison_instead_of_failing_it():
    """The pin is valid only while re-reading it reproduces it — and a mismatch is exit-2 class."""
    for tool, reading in _live_readings().items():
        assert reading, "%s produced no reading; a pin comparison on nothing proves nothing" % tool
        assert _assert_pin(tool, reading)
    with pytest.raises(PinMismatch):
        _assert_pin("git", "git version 0.0.0 (not this machine)")
    with pytest.raises(PinMismatch):
        _assert_pin("no-such-runner", "whatever")
    assert not issubclass(PinMismatch, AssertionError), (
        "a stale pin MUST read as an input error, never as a new failure (FR-023)"
    )


# --------------------------------------------------------------------------- #
# (f) the A13 boundary — one fact, one carrier
# --------------------------------------------------------------------------- #
def _cells(line):
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator(line):
    cells = _cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _tables(text):
    """`[(header, rows)]` for every Markdown table in `text`."""
    tables, block = [], []
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2:
            header = _cells(block[0])
            rows = [_cells(row) for row in block[1:] if not _is_separator(row)]
            tables.append((header, rows))
        block = []
    return tables


def _section(text, heading):
    """The body of one `## heading` section."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            continue
        if start is not None and line.startswith("## "):
            return "\n".join(lines[start:index])
    assert start is not None, "owner lacks the section %r" % heading
    return "\n".join(lines[start:])


def test_f_the_three_carriers_are_stated_once_and_the_skeletons_only_point():
    owner = OWNER.read_text(encoding="utf-8")
    carrier_tables = [
        (header, rows) for header, rows in _tables(owner)
        if "carrier" in " ".join(header).lower() and "judges" in " ".join(header).lower()
    ]
    assert len(carrier_tables) == 1, (
        "the A13 boundary MUST be stated once; found %d carrier tables" % len(carrier_tables)
    )
    _, rows = carrier_tables[0]
    carriers = {row[0] for row in rows if row and row[0]}
    assert carriers == {
        "`plan.md` § Execution Premises",
        "`plan.md` § Inherited Blockers",
        "`tasks.md` § Environment Prerequisites",
    }, carriers

    for heading in ("## Execution Premises", "## Inherited Blockers"):
        body = _section(owner, heading)
        boundary = [line for line in body.splitlines() if "A13" in line]
        assert len(boundary) == 1, (
            "%s must point at the A13 boundary exactly once, got %r" % (heading, boundary)
        )
        assert "§ Gates" in boundary[0] and "§ The A13 boundary" in boundary[0], boundary[0]

    skeleton = PLAN_TEMPLATE.read_text(encoding="utf-8")
    for heading in ("## Execution Premises", "## Inherited Blockers"):
        body = _section(skeleton, heading)
        assert "shared/workflow/acceptance-hardening.md" in body, (
            "%s in the plan skeleton must reach its schema by path (AS-13)" % heading
        )
        for literal in DOMAIN_LITERALS:
            assert literal not in body, (
                "%s in the plan skeleton carries the value-domain literal %r — the skeleton may "
                "repeat the column set and nothing else (AS-15)" % (heading, literal)
            )


# --------------------------------------------------------------------------- #
# (g) three shapes, three verdicts — silence is not one of them
# --------------------------------------------------------------------------- #
def _drop_runtime_section(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    kept, skipping = [], False
    for line in lines:
        if re.match(r"^#{2,4}\s+Runtime Stack & Dependency Ownership", line):
            skipping = True
            continue
        if skipping and line.startswith("#"):
            skipping = False
        if not skipping:
            kept.append(line)
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def test_g1_an_absent_section_is_an_input_error_from_both_producers(tmp_path):
    spec = _copy_fixture("positive", tmp_path)
    _drop_runtime_section(spec / "requirements.md")
    gate = _pre(spec, stage="requirements")
    assert gate.returncode == 2, gate.stdout + gate.stderr
    closure = _closure(spec)
    assert closure.returncode == 2, (
        "an incomplete artifact is exit 2 at both producers, never a verdict: %s%s"
        % (closure.stdout, closure.stderr)
    )


def test_g2_zero_data_rows_blocks_under_the_reserved_argument():
    """The shape that measured as *silence* before this slice: a block, not a pass."""
    record = _pre_record(_pre(_fixture("runtime-zero-row")))
    assert record["decision"] == "fail"
    assert "runtime-dependency-not-owned: runtime-stack" in _instances(record)
    assert _closure_instances(_fixture("runtime-zero-row")) == [
        "runtime-dependency-not-owned: runtime-stack"
    ]


def test_g3_an_empty_required_cell_blocks_under_its_own_id(tmp_path):
    spec = _copy_fixture("positive", tmp_path)
    _rewrite(
        spec / "requirements.md",
        "| RS-001 | fixture runtime capability |",
        "| RS-001 |  |",
    )
    record = _pre_record(_pre(spec))
    assert "runtime-dependency-not-owned: RS-001" in _instances(record), record["findings"]
    assert "runtime-dependency-not-owned: RS-001" in _closure_instances(spec)


def test_g4_the_three_shapes_are_three_distinct_verdicts(tmp_path):
    """The three shapes never collapse: absent ⇒ 2, zero rows ⇒ reserved, empty cell ⇒ RS-NNN."""
    absent = _copy_fixture("positive", tmp_path / "absent")
    _drop_runtime_section(absent / "requirements.md")
    assert _pre(absent, stage="requirements").returncode == 2

    zero = _pre_record(_pre(_fixture("runtime-zero-row"), stage="requirements"))
    assert "runtime-dependency-not-owned: runtime-stack" in _instances(zero)

    empty = _copy_fixture("positive", tmp_path / "empty")
    _rewrite(
        empty / "requirements.md",
        "| RS-001 | fixture runtime capability |",
        "| RS-001 |  |",
    )
    at_requirements = _pre_record(_pre(empty, stage="requirements"))
    assert "runtime-dependency-not-owned: RS-001" in _instances(at_requirements)


def test_g5_the_table_is_exempt_for_an_expression_class_feature(tmp_path):
    """The exemption is mechanical because the class is declared — and it is not a silent pass.

    An `expression`-class feature may deliver prose and consume no runtime capability, so the
    table is not mandatory for it. The leg keeps the two producers honest in the other direction:
    absence is legal **only** for that class, so the same edit on an `execution`-class fixture is
    an input error (asserted just above).
    """
    spec = _copy_fixture("positive", tmp_path)
    _rewrite(spec / "requirements.md", "**Flow Class**: execution", "**Flow Class**: expression")
    _drop_runtime_section(spec / "requirements.md")
    gate = _pre(spec, stage="plan")
    assert gate.returncode == 0, gate.stdout + gate.stderr
    proc, payload = _closure_payload(spec)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert payload["verdict"] == "accept", payload
    assert "runtime-dependency-not-owned: runtime-stack" not in [
        _instance(r) for r in payload["reasons"]
    ], payload["reasons"]


# --------------------------------------------------------------------------- #
# (h) the prose rule's arms
# --------------------------------------------------------------------------- #
def test_h1_a_marked_declaration_with_an_id_fires_and_the_exclusions_do_not():
    """One fixture carries all four arms: marked+id, unmarked narrative, fenced marker."""
    instances = _instances(_pre_record(_pre(_fixture("runtime-gap-mutation"))))
    assert "runtime-dependency-not-owned: RS-905" in instances, instances
    assert not [r for r in instances if "RS-904" in r], (
        "an unmarked narrative mention of an id is not a declaration: %r" % (instances,)
    )
    assert not [r for r in instances if "RS-906" in r], (
        "a marker-shaped line inside a fenced code block is removed before the rule is applied: "
        "%r" % (instances,)
    )
    closure = _closure_instances(_fixture("runtime-gap-mutation"))
    assert "runtime-dependency-not-owned: RS-905" in closure, closure
    assert not [r for r in closure if "RS-904" in r or "RS-906" in r], closure


def test_h2_a_marked_declaration_without_an_id_is_an_input_error_naming_the_line(tmp_path):
    spec = _copy_fixture("positive", tmp_path)
    requirements = spec / "requirements.md"
    marker = "- **Runtime dependency**: a capability with no id — an owner outside this fixture"
    requirements.write_text(
        requirements.read_text(encoding="utf-8").replace(
            "## Success Criteria *(mandatory)*", marker + "\n\n## Success Criteria *(mandatory)*"
        ),
        encoding="utf-8",
    )
    proc = _pre(spec, stage="requirements")
    assert proc.returncode == 2, (
        "a prose declaration carrying no id cannot produce a valid instance, so it is an input "
        "error naming the line — never a silent pass and never an eighth reason: %s%s"
        % (proc.stdout, proc.stderr)
    )
    assert "prose runtime declaration" in proc.stderr.lower(), proc.stderr


def test_h3_the_fenced_exclusion_is_mechanical_not_a_reading(tmp_path):
    """Lift the fenced marker out of its fence and the same text fires — the fence is the rule."""
    spec = _copy_fixture("runtime-gap-mutation", tmp_path)
    requirements = spec / "requirements.md"
    text = requirements.read_text(encoding="utf-8")
    fenced = "```text\n- **Runtime dependency**: a marker-shaped line that lives inside a fenced code block — RS-906\n```"
    assert fenced in text, "the fixture must carry the fenced exclusion arm"
    requirements.write_text(
        text.replace(fenced, "- **Runtime dependency**: a marker-shaped line once fenced — RS-906"),
        encoding="utf-8",
    )
    instances = _instances(_pre_record(_pre(spec)))
    assert "runtime-dependency-not-owned: RS-906" in instances, instances
