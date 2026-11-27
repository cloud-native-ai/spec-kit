"""Contract guard — the prompt-adherence reading engine (US1, C-016, C-020…C-029, C-030, C-031, C-036).

Red-first (T010): authored before ``scripts/python/prompt-adherence.py`` exists (T011…T015 build
it). Every engine leg fails on the absent engine itself (the named ``_require_engine``
assertion), never on an import error: this module imports nothing from the mechanism and runs
the engine only as a subprocess.

Legs and their clauses:

- C-030 / C-031 — one documented invocation, the declared flag set, identical ``-h``/``--help``
  bodies with the four labels, a run-time ``--version`` line, and undeclared-option rejection
  (including after a bare ``--``, before any action).
- C-020 / C-023 / C-025 / C-026 — the per-run reading shape on the seeded fixture: resolved
  scope with its basis, exactly one observation per catalog row in catalog order, the mandatory
  coverage section, sorted-key JSON from the same computed structure, byte-identical rerun.
- C-021 / C-028 — the two explicit statuses (``no-data``, ``not-found``, both exit 0), the
  default-scope versus explicit-run absence split, and the ``--run`` + window input error.
- C-024 / C-027 — invalid records surface in ``invalid_sources`` with counts and no crash;
  duplicates are disclosed; no record prose reaches either output form.
- C-016 / C-044 — project-layer-only and indirect-only fixtures produce no host statement
  beyond ``Unobserved`` and no layer-level verdict; no adherence verdict, score or ranking.
- C-032 / C-036 — the engine reads its stores through the owning engines' read surfaces (their
  constant names appear at the read point), imports no network module, and resolves the owner
  document by its own copy form (a source-tree copy never reads the installed face).

The ``--check-coverage`` legs (T019/T020) extend this same file below; the longitudinal
window, audit-replay and advisory-only legs are later slices' rows (T027, T030, T032) and
extend this file there.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "prompt-adherence.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "prompt-adherence"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
RUN_DETERMINATION = REPO_ROOT / "scripts" / "python" / "run-determination.py"
EVIDENCE_UTILS = REPO_ROOT / "scripts" / "python" / "evidence-utils.py"

CATALOG_ORDER = (
    "run-determination-record",
    "exec-quant-record",
    "feedback-entry",
    "gate-observation-record",
    "evidence-finding",
    "probe-registry-declaration",
)
RUN_ID = "r20261126T000000Z-fixture"
DEVIANT_RUN = "r20261126T000030Z-deviant"
GATE_RUN = "gate:fixture-gate:2026-11-26T00:04:00Z"
PROJECT_ONLY_RUN = "r20261126T000000Z-projonly"
INDIRECT_ONLY_RUN = "r20261126T000000Z-indirectonly"
NEGATIVE_RUN = "r20261126T000000Z-negative"
BLIND_SPOTS = (
    "host-prompt-content",
    "host-rule-surfacing",
    "in-turn-rule-behavior",
    "anomaly-line-persistence",
    "gate-breach-and-silent-skip",
    "instruction-drift-between-reconciles",
)
POSITIVE_STATES = {"Present", "Wired", "Exercised", "Outcome-supported"}
PROSE_MARKERS = (
    "PROSE-MARKER-FEEDBACK-BODY",
    "PROSE-MARKER-FEEDBACK-POINT",
    "PROSE-MARKER-GATE-DECISION",
    "PROSE-MARKER-GATE-POINT",
    "PROSE-MARKER-FINDING-SUMMARY",
    "PROSE-MARKER-PROJECT-ONLY",
    "PROSE-MARKER-PROJECT-ONLY-POINT",
    "PROSE-MARKER-NEGATIVE",
)
VERDICT_TOKENS = re.compile(r"(?i)\b(adherent|deviant|composite|score|ranking)\b")

FIXTURE_PATHS = (
    "seeded/.specify/session/20261126T000030Z-run-determination-speckit-review-rdev.md",
    "seeded/.specify/session/20261126T000100Z-run-determination-speckit-plan-rfixture.md",
    "seeded/.specify/exec-quant/records/20261126T000200000000Z-00000001.json",
    "seeded/.specify/feedback/20261126T000300Z-fixture-plan.md",
    "seeded/.specify/feedback/20261126T000400Z-fixture-gate.md",
    "seeded/.specify/evidence/ev-20261126-fixture/findings.json",
    "seeded/.specify/evidence/ev-20261126-fixture/manifest.json",
    "seeded/.specify/shared/definitions/probe-definitions.md",
    "project-only/.specify/session/.gitkeep",
    "project-only/.specify/exec-quant/records/20261126T000200000000Z-00000001.json",
    "project-only/.specify/feedback/20261126T000300Z-project-plan.md",
    "project-only/.specify/shared/definitions/probe-definitions.md",
    "indirect-only/.specify/session/20261126T000100Z-run-determination-speckit-plan-ridir.md",
    "indirect-only/.specify/exec-quant/records/20261126T000200000000Z-00000001.json",
    "indirect-only/.specify/evidence/ev-20261126-indirect/findings.json",
    "indirect-only/.specify/evidence/ev-20261126-indirect/manifest.json",
    "indirect-only/.specify/shared/definitions/probe-definitions.md",
    "recordless/.specify/session/.gitkeep",
    "recordless/.specify/shared/definitions/probe-definitions.md",
    "negative/.specify/session/20261126T000100Z-run-determination-speckit-plan-rneg.md",
    "negative/.specify/exec-quant/records/20261126T000200000000Z-00000001.json",
    "negative/.specify/exec-quant/records/broken-unparsable.json",
    "negative/.specify/exec-quant/records/unknown-version.json",
    "negative/.specify/feedback/20261126T000300Z-neg-a.md",
    "negative/.specify/feedback/20261126T000300Z-neg-b.md",
    "negative/.specify/feedback/20261126T000310Z-neg-badtime.md",
    "negative/.specify/evidence/ev-neg-schema/findings.json",
    "negative/.specify/evidence/ev-neg-schema/manifest.json",
    "negative/.specify/evidence/ev-neg-nomanifest/findings.json",
    "negative/.specify/evidence/ev-neg-broken/findings.json",
    "negative/.specify/shared/definitions/probe-definitions.md",
    "multi-run/.specify/session/20261123T090000Z-run-determination-speckit-plan-multi-a.md",
    "multi-run/.specify/session/20261125T000000Z-run-determination-speckit-plan-multi-b.md",
    "multi-run/.specify/session/20261125T060000Z-run-determination-speckit-review-multi-d.md",
    "multi-run/.specify/session/20261126T000000Z-run-determination-speckit-plan-multi-c.md",
    "multi-run/.specify/exec-quant/records/20261124T100000000000Z-00000001.json",
    "multi-run/.specify/exec-quant/records/20261125T100000000000Z-00000002.json",
    "multi-run/.specify/feedback/20261124T110000Z-multi-plan-a.md",
    "multi-run/.specify/feedback/20261125T110000Z-multi-plan-b.md",
    "multi-run/.specify/feedback/20261125T120000Z-multi-gate.md",
    "multi-run/.specify/evidence/ev-multi-a/findings.json",
    "multi-run/.specify/evidence/ev-multi-a/manifest.json",
    "multi-run/.specify/evidence/ev-multi-b/findings.json",
    "multi-run/.specify/evidence/ev-multi-b/manifest.json",
    "multi-run/.specify/shared/definitions/probe-definitions.md",
)


# --------------------------------------------------------------------------- #
# red-first subject loaders (named failures, never import errors)
# --------------------------------------------------------------------------- #
def _require_engine():
    assert ENGINE.is_file(), (
        "red-first: scripts/python/prompt-adherence.py is absent (built in US1 / T011…T015); "
        "this leg may go green only once the engine exists"
    )
    return ENGINE


def _run(*args, cwd=REPO_ROOT):
    engine = _require_engine()
    return subprocess.run(
        [sys.executable, str(engine), *[str(arg) for arg in args]],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def _reading(fixture, *args):
    proc = _run("--workspace-root", FIXTURES / fixture, "--json", *args)
    assert proc.returncode == 0, (
        "expected exit 0 from the reading over fixture %r; rc=%d stdout=%r stderr=%r"
        % (fixture, proc.returncode, proc.stdout, proc.stderr)
    )
    return json.loads(proc.stdout)


def _human(fixture, *args):
    proc = _run("--workspace-root", FIXTURES / fixture, *args)
    assert proc.returncode == 0, (
        "expected exit 0 from the human-form reading over fixture %r; rc=%d stdout=%r stderr=%r"
        % (fixture, proc.returncode, proc.stdout, proc.stderr)
    )
    return proc.stdout


def _observation(reading, row):
    matches = [obs for obs in reading["observations"] if obs["row"] == row]
    assert len(matches) == 1, "expected exactly one observation for %r, got %r" % (
        row,
        [obs["row"] for obs in reading["observations"]],
    )
    return matches[0]


def _reader_module():
    spec = importlib.util.spec_from_file_location("pa_engine_guard_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fact_members(slug):
    body = _reader_module().load_fact(str(REPO_ROOT), slug)["body"]
    return {str(member) for member in body.get("statement") or []}


def _engine_constants():
    engine = _require_engine()
    tree = ast.parse(engine.read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in (
                "ROW_REASON_CAUSES", "INVALID_SOURCE_CAUSES",
            ):
                found[target.id] = tuple(str(item) for item in ast.literal_eval(node.value))
    for name in ("ROW_REASON_CAUSES", "INVALID_SOURCE_CAUSES"):
        assert name in found, "the engine does not declare the module-level %s schema constant" % name
    return found


def _keys_deep(node):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from _keys_deep(value)
    elif isinstance(node, list):
        for value in node:
            yield from _keys_deep(value)


def _copy_tree(target):
    _require_engine()
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(REPO_ROOT / "scripts" / "python", target / "scripts" / "python", ignore=ignore)
    shutil.copytree(REPO_ROOT / "shared", target / "shared", ignore=ignore)
    return target


# --------------------------------------------------------------------------- #
# T009 — the fixture family exists (authoring-time existence check)
# --------------------------------------------------------------------------- #
def test_fixture_family_paths_exist():
    missing = [rel for rel in FIXTURE_PATHS if not (FIXTURES / rel).is_file()]
    assert not missing, "the prompt-adherence fixture family lacks: %r" % missing


# --------------------------------------------------------------------------- #
# C-030 / C-031 — one documented invocation and its interface
# --------------------------------------------------------------------------- #
def test_help_surfaces_are_identical_and_carry_the_four_labels():
    short = _run("-h")
    long = _run("--help")
    assert short.returncode == 0 and long.returncode == 0, (
        "-h/--help must exit 0; rc=%r/%r" % (short.returncode, long.returncode)
    )
    assert short.stdout == long.stdout, "-h and --help must print an identical body"
    body = short.stdout.lower()
    for label in ("usage", "options", "side-effects", "exit-codes"):
        assert label in body, "the help body lacks the %r label" % label
    assert "none" in body, "the help body must state the side effects (none)"


def test_version_answers_one_identity_line():
    proc = _run("--version")
    assert proc.returncode == 0, "--version must exit 0; rc=%d stderr=%r" % (
        proc.returncode,
        proc.stderr,
    )
    line = proc.stdout.strip()
    assert re.match(r"^prompt-adherence\.py \S+$", line), "--version body is %r" % line
    assert line != "prompt-adherence.py unknown", (
        "the engine runs inside a versioned repository; --version must resolve the version"
    )


def test_undeclared_option_is_rejected_before_any_action():
    for args in (("--bogus-option",), ("--", "--bogus-option")):
        proc = _run(*args)
        assert proc.returncode == 2, (
            "an undeclared option must exit 2 for %r; rc=%d stdout=%r stderr=%r"
            % (args, proc.returncode, proc.stdout, proc.stderr)
        )
        assert proc.stdout.strip() == "", "an undeclared option must emit no reading: %r" % args
        assert proc.stderr.strip(), "an undeclared option must name the rejection on stderr: %r" % args


# --------------------------------------------------------------------------- #
# C-020 / C-023 / C-025 / C-026 — the seeded per-run reading
# --------------------------------------------------------------------------- #
def test_seeded_default_reading_shape_and_catalog_order():
    reading = _reading("seeded")
    assert set(reading) == {
        "reading_format",
        "engine",
        "declaration_set",
        "scope",
        "status",
        "observations",
        "coverage",
        "invalid_sources",
        "duplicates",
    }, "the reading carries an undeclared top-level field set: %r" % sorted(reading)
    assert reading["reading_format"] == 1
    assert set(reading["engine"]) == {"path", "version"}
    assert reading["engine"]["path"].endswith("scripts/python/prompt-adherence.py")
    assert reading["engine"]["version"]
    assert set(reading["declaration_set"]) == {"version", "facts"}
    assert re.match(r"^[0-9a-f]{64}$", reading["declaration_set"]["version"])
    assert reading["declaration_set"]["facts"] == sorted(reading["declaration_set"]["facts"])
    facts = reading["declaration_set"]["facts"]
    assert len(facts) == 5
    assert {
        Path(path).name for path in facts
    } == {
        "prompt-adherence-layers.yaml",
        "prompt-adherence-strengths.yaml",
        "prompt-adherence-signals.yaml",
        "prompt-adherence-deviation-classes.yaml",
        "prompt-adherence-reading-status.yaml",
    }, "the declaration set must name exactly the five facts: %r" % facts

    scope = reading["scope"]
    assert set(scope) == {"kind", "run", "window", "resolution", "basis"}
    assert scope["kind"] == "run"
    assert scope["run"] == RUN_ID
    assert scope["resolution"] == "most-recent"
    assert scope["basis"] == {
        "store": "evidence",
        "path": ".specify/evidence/ev-20261126-fixture/findings.json",
        "timestamp": "2026-11-26T00:05:00Z",
    }
    assert reading["status"] == "complete"

    observations = reading["observations"]
    assert [obs["row"] for obs in observations] == list(CATALOG_ORDER)
    for obs in observations:
        assert set(obs) == {
            "row",
            "layer",
            "strength",
            "state",
            "deviation_classes",
            "reason",
            "sources",
        }, "observation %r carries an undeclared field set: %r" % (obs["row"], sorted(obs))

    expected = {
        "run-determination-record": ("host-prompt", "indirect", "Exercised", []),
        "exec-quant-record": ("project-rules", "indirect", "Exercised", []),
        "feedback-entry": ("project-rules", "direct", "Exercised", []),
        "gate-observation-record": ("project-rules", "direct", "Unobserved", []),
        "evidence-finding": ("project-rules", "indirect", "Exercised", ["evidence-missing"]),
        "probe-registry-declaration": ("project-rules", "indirect", "Wired", []),
    }
    for row, (layer, strength, state, classes) in expected.items():
        obs = _observation(reading, row)
        assert (obs["layer"], obs["strength"], obs["state"], obs["deviation_classes"]) == (
            layer,
            strength,
            state,
            classes,
        ), "row %r reads %r" % (row, obs)

    gate = _observation(reading, "gate-observation-record")
    assert gate["reason"]["cause"] == "no-matching-records"
    assert gate["sources"] == []

    for row in CATALOG_ORDER:
        obs = _observation(reading, row)
        if obs["state"] in POSITIVE_STATES:
            assert obs["sources"], "positive observation %r cites no source reference" % row
            for source in obs["sources"]:
                assert (FIXTURES / "seeded" / source["path"]).is_file(), (
                    "row %r cites an unresolvable source path %r" % (row, source["path"])
                )
                assert source["record"] and source["field"] and source["store"]
        else:
            assert obs["reason"] and obs["reason"]["cause"], (
                "absence observation %r carries no reason" % row
            )

    coverage = reading["coverage"]
    assert set(coverage) == {
        "observable",
        "not_observable",
        "blind_spots",
        "records_in_scope",
        "invalid_records",
    }
    assert coverage["observable"] == [
        row for row in CATALOG_ORDER if row != "gate-observation-record"
    ]
    assert coverage["not_observable"] == ["gate-observation-record"]
    assert coverage["blind_spots"] == list(BLIND_SPOTS)
    assert coverage["records_in_scope"] == 4
    assert coverage["invalid_records"] == 0
    assert reading["invalid_sources"] == []
    assert reading["duplicates"] == []
    assert "generated_at" not in reading


def test_human_form_prints_scope_basis_and_one_line_per_row():
    stdout = _human("seeded")
    assert ("scope: run %s" % RUN_ID) in stdout
    assert "scope-resolution: most-recent" in stdout
    assert ("store=evidence path=.specify/evidence/ev-20261126-fixture/findings.json "
            "timestamp=2026-11-26T00:05:00Z") in stdout
    assert "status: complete" in stdout
    row_lines = [line for line in stdout.splitlines() if line.startswith("row ")]
    assert len(row_lines) == 6, "expected one row line per catalog row, got %r" % row_lines
    assert [line.split()[1] for line in row_lines] == list(CATALOG_ORDER)
    assert "coverage-blind-spots: " + ", ".join(BLIND_SPOTS) in stdout
    assert "coverage-records-in-scope: 4" in stdout


def test_two_consecutive_runs_are_field_identical():
    for args in ((), ("--json",)):
        first = _run("--workspace-root", FIXTURES / "seeded", *args)
        second = _run("--workspace-root", FIXTURES / "seeded", *args)
        assert first.returncode == 0 and second.returncode == 0
        assert first.stdout == second.stdout, (
            "two consecutive %r runs differ (determinism, C-023)" % (args,)
        )


def test_deleting_one_rows_records_turns_exactly_that_row_absent(tmp_path):
    workspace = tmp_path / "ws"
    shutil.copytree(FIXTURES / "seeded", workspace)
    baseline = _reading("seeded")
    shutil.rmtree(workspace / ".specify" / "exec-quant")
    proc = _run("--workspace-root", workspace, "--json")
    assert proc.returncode == 0, "deleting one row's records must not abort the reading: %r" % (
        proc.stderr,
    )
    reading = json.loads(proc.stdout)
    obs = _observation(reading, "exec-quant-record")
    assert obs["state"] == "not_evaluated"
    assert obs["reason"]["cause"] == "source-unavailable"
    for row in CATALOG_ORDER:
        if row == "exec-quant-record":
            continue
        assert _observation(reading, row)["state"] == _observation(baseline, row)["state"], (
            "deleting the exec-quant store changed row %r as well" % row
        )
    assert reading["status"] == "partial"


# --------------------------------------------------------------------------- #
# C-021 / C-028 — the two explicit statuses and the absence split
# --------------------------------------------------------------------------- #
def test_recordless_fixture_emits_no_data_with_explicit_absence_lines():
    reading = _reading("recordless")
    assert reading["status"] == "no-data"
    assert reading["scope"]["resolution"] == "none"
    assert reading["scope"]["run"] is None
    assert reading["scope"]["basis"] is None
    assert [obs["row"] for obs in reading["observations"]] == list(CATALOG_ORDER)
    assert _observation(reading, "run-determination-record")["state"] == "Unobserved"
    assert _observation(reading, "exec-quant-record")["state"] == "not_evaluated"
    assert _observation(reading, "exec-quant-record")["reason"]["cause"] == "source-unavailable"
    assert _observation(reading, "probe-registry-declaration")["state"] == "Wired"
    assert reading["coverage"]["records_in_scope"] == 0

    stdout = _human("recordless")
    assert "status: no-data" in stdout
    assert "state=not_evaluated" in stdout
    assert "state=Unobserved" in stdout


def test_unmatched_explicit_run_emits_not_found_and_exits_zero():
    reading = _reading("seeded", "--run", "r20260101T000000Z-no-such-run")
    assert reading["status"] == "not-found"
    assert reading["scope"]["kind"] == "run"
    assert reading["scope"]["resolution"] == "explicit"
    assert reading["scope"]["run"] == "r20260101T000000Z-no-such-run"
    assert reading["coverage"]["records_in_scope"] == 0
    for row in CATALOG_ORDER:
        obs = _observation(reading, row)
        assert obs["state"] in {"not_evaluated", "Unobserved"}
        assert obs["reason"]["cause"]


def test_explicit_run_is_partial_where_default_leaves_unobserved():
    default = _reading("seeded")
    explicit = _reading("seeded", "--run", RUN_ID)
    assert default["status"] == "complete"
    assert explicit["status"] == "partial"
    default_gate = _observation(default, "gate-observation-record")
    explicit_gate = _observation(explicit, "gate-observation-record")
    assert default_gate["state"] == "Unobserved"
    assert explicit_gate["state"] == "not_evaluated"
    assert default_gate["reason"]["cause"] == explicit_gate["reason"]["cause"] == "no-matching-records"


def test_run_with_a_window_is_an_input_error():
    proc = _run("--workspace-root", FIXTURES / "seeded", "--run", RUN_ID, "--since", "2026-11-01")
    assert proc.returncode == 2, "--run combined with a window must exit 2; rc=%d" % proc.returncode
    assert proc.stdout.strip() == ""
    assert proc.stderr.strip()


# --------------------------------------------------------------------------- #
# C-016 / C-024 — the gate family, deviation classes, invalid records, duplicates
# --------------------------------------------------------------------------- #
def test_gate_family_run_marks_the_gate_row_exercised():
    reading = _reading("seeded", "--run", GATE_RUN)
    gate = _observation(reading, "gate-observation-record")
    assert gate["state"] == "Exercised"
    assert gate["sources"], "the gate observation cites no source reference"
    assert gate["sources"][0]["path"].endswith("20261126T000400Z-fixture-gate.md")
    assert _observation(reading, "feedback-entry")["state"] == "not_evaluated"


def test_deviant_run_carries_both_run_determination_deviation_classes():
    reading = _reading("seeded", "--run", DEVIANT_RUN)
    obs = _observation(reading, "run-determination-record")
    assert obs["state"] == "Exercised"
    assert obs["deviation_classes"] == ["axis-regression", "green-unproven"]


def test_invalid_records_are_disclosed_with_causes_and_counts():
    reading = _reading("negative")
    assert reading["status"] == "partial"
    by_path = {entry["path"]: entry["cause"] for entry in reading["invalid_sources"]}
    expected = {
        ".specify/evidence/ev-neg-broken/findings.json": "unparsable",
        ".specify/evidence/ev-neg-nomanifest/findings.json": "invalid-timestamp",
        ".specify/evidence/ev-neg-schema/findings.json": "schema-violation",
        ".specify/exec-quant/records/broken-unparsable.json": "unparsable",
        ".specify/exec-quant/records/unknown-version.json": "unknown-schema-version",
        ".specify/feedback/20261126T000310Z-neg-badtime.md": "invalid-timestamp",
    }
    assert by_path == expected
    paths = [entry["path"] for entry in reading["invalid_sources"]]
    assert paths == sorted(paths), "invalid sources must be sorted by path"
    assert reading["coverage"]["invalid_records"] == len(expected)

    evidence = _observation(reading, "evidence-finding")
    assert evidence["state"] == "not_evaluated"
    assert evidence["reason"]["cause"] == "invalid-source"
    assert _observation(reading, "exec-quant-record")["state"] == "Exercised"
    assert _observation(reading, "feedback-entry")["state"] == "Exercised"
    assert _observation(reading, "run-determination-record")["state"] == "Exercised"


def test_duplicates_are_disclosed_with_paths():
    reading = _reading("negative")
    assert len(reading["duplicates"]) == 1
    duplicate = reading["duplicates"][0]
    assert duplicate["row"] == "feedback-entry"
    assert duplicate["count"] == 1
    assert duplicate["paths"] == [
        ".specify/feedback/20261126T000300Z-neg-a.md",
        ".specify/feedback/20261126T000300Z-neg-b.md",
    ]
    assert NEGATIVE_RUN in duplicate["identity"]


# --------------------------------------------------------------------------- #
# C-027 / C-016 / C-044 — privacy, layer honesty, no verdict
# --------------------------------------------------------------------------- #
def test_no_record_prose_reaches_either_output_form():
    for output in (_human("seeded"), json.dumps(_reading("seeded"))):
        for marker in PROSE_MARKERS:
            assert marker not in output, "record prose marker %r leaked into the output" % marker
    for output in (_human("negative"), json.dumps(_reading("negative"))):
        for marker in ("PROSE-MARKER-NEGATIVE",):
            assert marker not in output, "record prose marker %r leaked into the output" % marker


def test_project_layer_only_fixture_states_no_host_observation_beyond_unobserved():
    reading = _reading("project-only")
    host_rows = [obs for obs in reading["observations"] if obs["layer"] == "host-prompt"]
    assert host_rows, "the project-only reading carries no host-layer row at all"
    for obs in host_rows:
        assert obs["state"] == "Unobserved", (
            "host row %r states %r in a project-layer-only fixture" % (obs["row"], obs["state"])
        )
    assert _observation(reading, "exec-quant-record")["state"] == "Exercised"
    assert _observation(reading, "feedback-entry")["state"] == "Exercised"
    assert reading["scope"]["run"] == PROJECT_ONLY_RUN


def test_indirect_only_fixture_produces_no_layer_level_verdict():
    reading = _reading("indirect-only")
    positive = [obs for obs in reading["observations"] if obs["state"] in POSITIVE_STATES]
    assert positive, "the indirect-only fixture produced no positive observation"
    for obs in positive:
        assert obs["strength"] == "indirect", (
            "a positive observation %r in the indirect-only fixture declares strength %r"
            % (obs["row"], obs["strength"])
        )
    verdict_like_keys = {
        key for key in _keys_deep(reading) if key.lower() in {"verdict", "layer_verdict", "score"}
    }
    assert not verdict_like_keys, "a layer-level verdict-shaped key appeared: %r" % verdict_like_keys
    assert reading["scope"]["run"] == INDIRECT_ONLY_RUN


def test_no_adherence_verdict_token_score_or_ranking():
    for fixture in ("seeded", "negative"):
        outputs = (_human(fixture), json.dumps(_reading(fixture)))
        for output in outputs:
            match = VERDICT_TOKENS.search(output)
            assert not match, "verdict-shaped token %r appears in the %r reading" % (
                match.group(0) if match else None,
                fixture,
            )


# --------------------------------------------------------------------------- #
# C-012 / C-014 — emitted tokens are members of the declared domains
# --------------------------------------------------------------------------- #
def test_emitted_tokens_are_members_of_declared_domains():
    facts = {
        slug: _fact_members(slug)
        for slug in (
            "prompt-adherence-layers",
            "prompt-adherence-strengths",
            "prompt-adherence-signals",
            "prompt-adherence-deviation-classes",
            "prompt-adherence-reading-status",
            "evidence-seven-states",
        )
    }
    composed_states = facts["evidence-seven-states"] | {"not_evaluated"}
    constants = _engine_constants()
    for fixture in ("seeded", "project-only", "indirect-only", "recordless", "negative"):
        reading = _reading(fixture)
        assert reading["status"] in facts["prompt-adherence-reading-status"]
        for obs in reading["observations"]:
            assert obs["row"] in facts["prompt-adherence-signals"]
            assert obs["layer"] in facts["prompt-adherence-layers"]
            assert obs["strength"] in facts["prompt-adherence-strengths"]
            assert obs["state"] in composed_states, obs["state"]
            for token in obs["deviation_classes"]:
                assert token in facts["prompt-adherence-deviation-classes"]
            if obs["reason"]:
                assert obs["reason"]["cause"] in constants["ROW_REASON_CAUSES"]
        for entry in reading["invalid_sources"]:
            assert entry["cause"] in constants["INVALID_SOURCE_CAUSES"]


# --------------------------------------------------------------------------- #
# C-032 / C-034 / C-036 — the read surfaces, the import surface, self-location
# --------------------------------------------------------------------------- #
def test_engine_reads_through_the_owning_engines_surfaces():
    source = _require_engine().read_text(encoding="utf-8")
    for name in (
        "declaration_reader",
        "load_determinations",
        "load_records",
        "scan_entries",
        "load_probe_registry",
        "load_index",
        "SEVEN_STATES",
        "GREEN_UNPROVEN_VERDICT",
        "FINDINGS_PROJECTION_FIELDS",
        "FINDINGS_KIND",
    ):
        assert name in source, "the engine references no %r read point" % name
    for slug in (
        "prompt-adherence-layers",
        "prompt-adherence-strengths",
        "prompt-adherence-signals",
        "prompt-adherence-deviation-classes",
        "prompt-adherence-reading-status",
    ):
        assert slug in source, "the engine references no %s fact slug" % slug
    assert "FINDINGS_PROJECTION_FIELDS" in RUN_DETERMINATION.read_text(encoding="utf-8")
    evidence_source = EVIDENCE_UTILS.read_text(encoding="utf-8")
    assert "FINDINGS_KIND" in evidence_source and "SCHEMA_VERSION" in evidence_source


def test_engine_imports_no_network_module():
    tree = ast.parse(_require_engine().read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])
    forbidden = {
        "socket",
        "ssl",
        "http",
        "urllib",
        "urllib2",
        "ftplib",
        "telnetlib",
        "smtplib",
        "requests",
        "httpx",
        "asyncio",
    }
    assert not (imported & forbidden), (
        "the engine imports network modules: %r" % sorted(imported & forbidden)
    )


# --------------------------------------------------------------------------- #
# C-003 / C-026 — the --check-coverage action (T019/T020)
# --------------------------------------------------------------------------- #
def _scratch_coverage_run(tree):
    engine = tree / "scripts" / "python" / "prompt-adherence.py"
    assert engine.is_file(), "the scratch tree carries no engine copy"
    return subprocess.run(
        [sys.executable, str(engine), "--check-coverage"],
        cwd=str(tree), capture_output=True, text=True,
    )


def _doctor_coverage_row(tree, needle, replacement):
    owner = tree / "shared" / "definitions" / "prompt-adherence-definitions.md"
    assert owner.is_file(), "cannot doctor an absent owner document"
    text = owner.read_text(encoding="utf-8")
    assert text.count(needle) == 1, (
        "the coverage-map shape changed; update the doctor (found %d of %r)"
        % (text.count(needle), needle)
    )
    owner.write_text(text.replace(needle, replacement), encoding="utf-8")


def test_check_coverage_is_clean_on_the_delivered_owner_document():
    proc = _run("--check-coverage")
    assert proc.returncode == 0, (
        "the coverage check must exit 0 on the delivered owner document; rc=%d stdout=%r "
        "stderr=%r" % (proc.returncode, proc.stdout, proc.stderr)
    )
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines == ["coverage-map: ok (0 findings)"], (
        "a clean coverage check prints exactly the zero-findings line; got %r" % lines
    )


DOCTORED_COVERAGE_CASES = (
    (
        "dangling-sensor-target",
        "| `sensor` | `run-determination-record` |",
        "| `sensor` | `zz-ghost-row` |",
        (("unresolved-target", "zz-ghost-row"), ("uncited-catalog-row", "run-determination-record")),
    ),
    (
        "dangling-blind-spot-target",
        "| `blind-spot` | `instruction-drift-between-reconciles` |",
        "| `blind-spot` | `zz-ghost-spot` |",
        (
            ("unresolved-target", "zz-ghost-spot"),
            ("uncited-blind-spot", "instruction-drift-between-reconciles"),
        ),
    ),
    (
        "duplicate-assumed-behavior",
        "| `AB-12` |",
        "| `AB-11` |",
        (("duplicate-assumed-behavior", "AB-11"),),
    ),
    (
        "two-targets-on-one-row",
        "| `sensor` | `run-determination-record` |",
        "| `sensor` | `run-determination-record`, `exec-quant-record` |",
        (("multiple-targets", "AB-01"),),
    ),
)


@pytest.mark.parametrize(
    "name,needle,replacement,expected",
    DOCTORED_COVERAGE_CASES,
    ids=[case[0] for case in DOCTORED_COVERAGE_CASES],
)
def test_check_coverage_reports_sorted_findings_on_doctored_copies(
    tmp_path, name, needle, replacement, expected
):
    tree = _copy_tree(tmp_path / name)
    _doctor_coverage_row(tree, needle, replacement)
    proc = _scratch_coverage_run(tree)
    assert proc.returncode == 1, (
        "the doctored %r copy must exit 1 with findings; rc=%d stdout=%r stderr=%r"
        % (name, proc.returncode, proc.stdout, proc.stderr)
    )
    findings = [line for line in proc.stdout.splitlines() if line.strip()]
    assert findings, "exit 1 emitted no finding list"
    assert findings == sorted(findings), (
        "the finding list must be sorted: %r" % findings
    )
    for marker, subject in expected:
        assert any(marker in line and subject in line for line in findings), (
            "the %r doctored copy does not name (%r, %r) in its findings: %r"
            % (name, marker, subject, findings)
        )
    assert not any(line.startswith("coverage-map: ok") for line in findings), (
        "a doctored copy printed the clean line"
    )


def test_check_coverage_exits_2_when_the_owner_document_is_unusable(tmp_path):
    tree = _copy_tree(tmp_path / "tree")
    (tree / "shared" / "definitions" / "prompt-adherence-definitions.md").unlink()
    proc = _scratch_coverage_run(tree)
    assert proc.returncode == 2, (
        "an unusable owner document must exit 2, never report findings; rc=%d stdout=%r"
        % (proc.returncode, proc.stdout)
    )
    assert proc.stdout.strip() == "", "no coverage verdict may be emitted without the subject"
    assert "owner document" in proc.stderr, (
        "the exit-2 refusal must name the unusable owner document; stderr=%r" % proc.stderr
    )


def test_source_copy_and_installed_copy_each_read_their_own_owner_document(tmp_path):
    tree = _copy_tree(tmp_path / "tree")
    installed_scripts = tree / ".specify" / "scripts" / "python"
    installed_shared = tree / ".specify" / "shared"
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(REPO_ROOT / "scripts" / "python", installed_scripts, ignore=ignore)
    shutil.copytree(REPO_ROOT / "shared", installed_shared, ignore=ignore)
    mirror_doc = installed_shared / "definitions" / "prompt-adherence-definitions.md"
    original = mirror_doc.read_text(encoding="utf-8")
    assert "host-prompt-content" in original
    mirror_doc.write_text(
        original.replace("host-prompt-content", "zz-installed-face-trap"), encoding="utf-8"
    )

    workspace = FIXTURES / "recordless"
    source_proc = subprocess.run(
        [sys.executable, str(tree / "scripts" / "python" / "prompt-adherence.py"),
         "--workspace-root", str(workspace), "--json"],
        cwd=str(tree), capture_output=True, text=True,
    )
    assert source_proc.returncode == 0, source_proc.stderr
    source_reading = json.loads(source_proc.stdout)
    assert source_reading["engine"]["path"] == "scripts/python/prompt-adherence.py"
    assert source_reading["coverage"]["blind_spots"] == list(BLIND_SPOTS), (
        "the source-tree copy read the installed face (self-location fired on a path with no "
        "literal '.specify' component)"
    )

    installed_proc = subprocess.run(
        [sys.executable, str(installed_scripts / "prompt-adherence.py"),
         "--workspace-root", str(workspace), "--json"],
        cwd=str(tree), capture_output=True, text=True,
    )
    assert installed_proc.returncode == 0, installed_proc.stderr
    installed_reading = json.loads(installed_proc.stdout)
    assert installed_reading["engine"]["path"] == "scripts/python/prompt-adherence.py", (
        "the installed copy reports its identity relative to the declaration layer root "
        "(the .specify container), the same logical artifact as the source copy"
    )
    assert installed_reading["coverage"]["blind_spots"][0] == "zz-installed-face-trap", (
        "the installed copy did not read its installed owner document"
    )

# --------------------------------------------------------------------------- #
# T027 — the longitudinal window legs (C-022, FR-015, FR-016)
# --------------------------------------------------------------------------- #
MULTI = "multi-run"
WINDOW_A = ("2026-11-25T00:00:00Z", "2026-11-26T00:00:00Z")
WINDOW_A_COUNTS = {
    "run-determination-record": {"Exercised": 2},
    "exec-quant-record": {"Exercised": 1},
    "feedback-entry": {"Exercised": 1},
    "gate-observation-record": {"Exercised": 1},
    "evidence-finding": {"Exercised": 1},
    "probe-registry-declaration": {},
}
WINDOW_B_COUNTS = {
    "run-determination-record": {"Exercised": 2},
    "exec-quant-record": {"Exercised": 2},
    "feedback-entry": {"Exercised": 2},
    "gate-observation-record": {"Exercised": 1},
    "evidence-finding": {"Exercised": 2},
    "probe-registry-declaration": {},
}
RANKING_TOKENS = re.compile(r"(?i)\b(ranking|ranked|rank|composite|comparison|score)\b")


def _window_args(since=None, until=None):
    args = []
    if since is not None:
        args += ["--since", since]
    if until is not None:
        args += ["--until", until]
    return args


def test_window_reading_reports_per_row_state_counts_in_catalog_order():
    reading = _reading(MULTI, *_window_args(*WINDOW_A))
    scope = reading["scope"]
    assert scope["kind"] == "window"
    assert scope["run"] is None
    assert scope["window"] == {"since": WINDOW_A[0], "until": WINDOW_A[1]}
    assert scope["resolution"] == "explicit"
    assert [obs["row"] for obs in reading["observations"]] == list(CATALOG_ORDER)
    for row, counts in WINDOW_A_COUNTS.items():
        obs = _observation(reading, row)
        assert obs["state_counts"] == counts, "row %r counts %r" % (row, obs.get("state_counts"))
    assert reading["status"] == "complete"
    assert reading["coverage"]["records_in_scope"] == 6
    assert reading["coverage"]["blind_spots"] == list(BLIND_SPOTS)
    assert "generated_at" not in reading

    wider = _reading(MULTI, *_window_args("2026-11-24T00:00:00Z", WINDOW_A[1]))
    for row, counts in WINDOW_B_COUNTS.items():
        obs = _observation(wider, row)
        assert obs["state_counts"] == counts, (
            "the wider window row %r counts %r" % (row, obs.get("state_counts"))
        )
    assert wider["coverage"]["records_in_scope"] == 9


def test_window_boundary_on_exact_record_timestamps_is_half_open():
    reading = _reading(MULTI, *_window_args(*WINDOW_A))
    run_det = _observation(reading, "run-determination-record")
    paths = [source["path"] for source in run_det["sources"]]
    assert any(path.endswith("multi-b.md") for path in paths), (
        "the record whose determined_at equals --since must be included (half-open, since "
        "inclusive): %r" % paths
    )
    assert not any(path.endswith("multi-c.md") for path in paths), (
        "the record whose determined_at equals --until must be excluded (half-open, until "
        "exclusive): %r" % paths
    )
    assert run_det["state_counts"] == {"Exercised": 2}


def test_omitted_window_bound_prints_the_open_literal_and_both_bounds_appear():
    since_only = _reading(MULTI, *_window_args("2026-11-25"))
    assert since_only["scope"]["window"] == {"since": "2026-11-25T00:00:00Z", "until": "open"}
    assert _observation(since_only, "run-determination-record")["state_counts"] == {
        "Exercised": 3
    }, "an open upper bound must include the record at 2026-11-26T00:00:00Z"
    assert since_only["coverage"]["records_in_scope"] == 7

    until_only = _reading(MULTI, *_window_args(None, "2026-11-26T00:00:00Z"))
    assert until_only["scope"]["window"] == {"since": "open", "until": "2026-11-26T00:00:00Z"}
    assert until_only["coverage"]["records_in_scope"] == 10

    stdout = _human(MULTI, *_window_args("2026-11-25"))
    assert "scope: window [2026-11-25T00:00:00Z, open)" in stdout
    assert "window-since: 2026-11-25T00:00:00Z" in stdout
    assert "window-until: open" in stdout


def test_window_accepts_both_declared_bound_forms_and_rejects_invalid_values():
    date_only = _run(
        "--workspace-root", FIXTURES / MULTI, "--json",
        "--since", "2026-11-25", "--until", "2026-11-26",
    )
    full = _run(
        "--workspace-root", FIXTURES / MULTI, "--json",
        "--since", WINDOW_A[0], "--until", WINDOW_A[1],
    )
    assert date_only.returncode == 0 and full.returncode == 0
    assert date_only.stdout == full.stdout, (
        "the date-only form must resolve to the same UTC midnight window as the full form"
    )
    for flag, value in (
        ("--since", "2026/11/25"),
        ("--since", "yesterday"),
        ("--until", "2026-11-25T99:00:00Z"),
    ):
        proc = _run("--workspace-root", FIXTURES / MULTI, flag, value)
        assert proc.returncode == 2, (
            "an invalid %s value must exit 2; rc=%d stdout=%r stderr=%r"
            % (flag, proc.returncode, proc.stdout, proc.stderr)
        )
        assert proc.stdout.strip() == "", "no reading may be emitted for an invalid bound"
        assert flag in proc.stderr, "the refusal must name the offending flag: %r" % proc.stderr


def test_probe_row_evaluates_once_and_is_marked_window_exempt():
    reading = _reading(MULTI, *_window_args(*WINDOW_A))
    notes = reading["scope"].get("notes") or []
    assert any(
        "probe-registry-declaration" in note and "window-exempt" in note for note in notes
    ), "the window-exempt declaration-row note is absent: %r" % notes
    probe = _observation(reading, "probe-registry-declaration")
    assert probe["state"] == "Wired"
    assert probe["state_counts"] == {}, (
        "the declaration row must not be faked into a timestamped series: %r"
        % probe["state_counts"]
    )
    assert probe["sources"], "the declaration row still cites its registry once"
    stdout = _human(MULTI, *_window_args(*WINDOW_A))
    assert "window-exempt" in stdout
    assert "state-counts probe-registry-declaration none" in stdout


def test_window_reading_produces_no_ranking_or_comparison():
    reading = _reading(MULTI, *_window_args(*WINDOW_A))
    ranked_keys = [
        key for key in _keys_deep(reading) if re.search(r"(?i)rank|compar|composite|score", key)
    ]
    assert not ranked_keys, "a ranking-shaped key appeared in the window reading: %r" % ranked_keys
    for output in (_human(MULTI, *_window_args(*WINDOW_A)), json.dumps(reading)):
        match = RANKING_TOKENS.search(output)
        assert not match, "ranking token %r appears in the window reading" % (
            match.group(0) if match else None,
        )


def test_window_with_zero_records_emits_no_data_with_all_rows_present():
    reading = _reading(MULTI, *_window_args("2027-01-01", "2027-02-01"))
    assert reading["status"] == "no-data"
    assert reading["coverage"]["records_in_scope"] == 0
    assert [obs["row"] for obs in reading["observations"]] == list(CATALOG_ORDER)
    for row in CATALOG_ORDER:
        obs = _observation(reading, row)
        assert obs["state_counts"] == {}
        if row == "probe-registry-declaration":
            assert obs["state"] == "Wired"
        else:
            assert obs["state"] == "Unobserved", (
                "a readable source with zero in-window records reads %r on row %r"
                % (obs["state"], row)
            )
            assert obs["reason"]["cause"] == "no-matching-records"


# --------------------------------------------------------------------------- #
# T028 — the output caps (bounds, never thresholds; C-023)
# --------------------------------------------------------------------------- #
def test_output_caps_truncate_sources_with_a_shown_total_disclosure(tmp_path):
    workspace = tmp_path / "ws"
    shutil.copytree(FIXTURES / "seeded", workspace)
    for index in range(25):
        name = "20261126T0006%02dZ-cap-%02d.md" % (index, index)
        (workspace / ".specify" / "feedback" / name).write_text(
            "---\n"
            'id: "%s"\n'
            'unit_id: "/speckit.plan"\n'
            'unit_type: "command"\n'
            'run_id: "%s"\n'
            'created: "2026-11-26T00:06:%02dZ"\n'
            "---\n\n## Review\n\nCap-leg fixture entry; metadata only is read.\n"
            % (name[:-3], RUN_ID, index),
            encoding="utf-8",
        )
    proc = _run("--workspace-root", workspace, "--json")
    assert proc.returncode == 0, proc.stderr
    reading = json.loads(proc.stdout)
    obs = _observation(reading, "feedback-entry")
    assert len(obs["sources"]) == 20, "per-observation sources must cap at 20"
    assert reading["truncations"] == [
        {"list": "sources", "row": "feedback-entry", "shown": 20, "total": 26}
    ], "each truncation must carry its shown/total disclosure: %r" % reading.get("truncations")

    human = _run("--workspace-root", workspace)
    assert human.returncode == 0
    assert "truncated sources row=feedback-entry shown=20 total=26" in human.stdout


# --------------------------------------------------------------------------- #
# T030 — the advisory-only boundary (C-029/C-044, FR-008, FR-025)
# --------------------------------------------------------------------------- #
ADVISORY_FORBIDDEN_KEY_RE = re.compile(
    r"(?i)(disposition|threshold|mutation|remediat|next_action|action_item|verdict)"
)
ADVISORY_FORBIDDEN_TEXT_RE = re.compile(
    r"(?i)\b(disposition|threshold|remediat\w*|mutation|next action|action item)\b"
)


def _advisory_readings():
    return (
        ("seeded", _reading("seeded")),
        ("seeded-deviant", _reading("seeded", "--run", DEVIANT_RUN)),
        ("negative", _reading("negative")),
    )


def test_a_deviation_bearing_reading_carries_no_disposition_threshold_or_mutation():
    saw_deviation = False
    for label, reading in _advisory_readings():
        for observation in reading["observations"]:
            if observation["deviation_classes"]:
                saw_deviation = True
        shaped = [
            key for key in _keys_deep(reading) if ADVISORY_FORBIDDEN_KEY_RE.search(key)
        ]
        assert not shaped, (
            "the %r reading carries an automatic-disposition-shaped key %r; a reading is "
            "advisory-only (FR-008/FR-025)" % (label, shaped)
        )
        for output in (_human(label.split("-")[0], *(["--run", DEVIANT_RUN] if label.endswith("deviant") else [])),
                       json.dumps(reading)):
            match = ADVISORY_FORBIDDEN_TEXT_RE.search(output)
            assert not match, (
                "the %r reading carries the automatic-disposition token %r"
                % (label, match.group(0) if match else None)
            )
    assert saw_deviation, (
        "the advisory fixtures yielded no deviation-class observation; the negative observation "
        "this leg exists for is not present"
    )


def test_negative_vocabulary_is_exactly_the_three_deviation_classes_plus_absence_states():
    facts = _fact_members("prompt-adherence-deviation-classes")
    assert facts == {"axis-regression", "green-unproven", "evidence-missing"}
    emitted_classes = set()
    for _label, reading in _advisory_readings():
        for observation in reading["observations"]:
            emitted_classes.update(observation["deviation_classes"])
            if observation["state"] not in POSITIVE_STATES:
                assert observation["state"] in {"not_evaluated", "Unobserved"}, (
                    "row %r states %r outside the negative vocabulary"
                    % (observation["row"], observation["state"])
                )
                assert observation["reason"] and observation["reason"]["cause"], (
                    "absence reading %r carries no reason" % observation["row"]
                )
    assert emitted_classes == facts, (
        "the exercised negative vocabulary is %r; the declared set is %r"
        % (sorted(emitted_classes), sorted(facts))
    )


# --------------------------------------------------------------------------- #
# T032 — audit replay: every observation resolves from its citations alone
# --------------------------------------------------------------------------- #
FEEDBACK_DIR = REPO_ROOT / ".specify" / "feedback"
BASELINE_MARKER = "prompt-adherence-baseline-v1"


def _frontmatter(text):
    chunks = text.split("---", 2)
    assert len(chunks) >= 3, "the record carries no frontmatter block"
    meta = {}
    for line in chunks[1].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta


def _json_block(text):
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    assert match, "the record carries no fenced JSON block"
    return json.loads(match.group(1))


def _resolve_source_reference(source, workspace):
    """Reconstruct one source reference mechanically from its citations alone (C-024)."""
    store, rel, record, field = (
        source["store"], source["path"], source["record"], source["field"],
    )
    assert store and rel and record and field, "a citation carries an empty part: %r" % source
    target = Path(workspace) / rel
    assert target.is_file(), "citation path %r does not resolve under %r" % (rel, workspace)
    text = target.read_text(encoding="utf-8")
    if store == "registry":
        assert "## Objects" in text, "the registry citation names a file with no Objects table"
        return
    if store == "feedback":
        meta = _frontmatter(text)
        assert meta.get("id") == record, (
            "feedback citation record %r does not name the entry id %r" % (record, meta.get("id"))
        )
        assert field in meta, "feedback citation field %r is absent" % field
        return
    body = _json_block(text) if store == "session" else json.loads(text)
    assert body.get(field) == record, (
        "%s citation (record=%r, field=%r) does not reconstruct (value=%r)"
        % (store, record, field, body.get(field))
    )


def test_every_positive_observation_resolves_from_its_citations_alone():
    for fixture in ("seeded", "multi-run", "project-only", "indirect-only"):
        workspace = FIXTURES / fixture
        reading = _reading(fixture)
        positives = 0
        for observation in reading["observations"]:
            if observation["state"] not in POSITIVE_STATES:
                continue
            positives += 1
            assert observation["sources"], (
                "positive observation %r in %r cites no source" % (observation["row"], fixture)
            )
            for source in observation["sources"]:
                _resolve_source_reference(source, workspace)
        assert positives, "fixture %r produced no positive observation to audit" % fixture


def test_the_seeded_broken_reference_appears_as_an_invalid_source_never_skipped():
    reading = _reading("negative")
    by_path = {entry["path"]: entry["cause"] for entry in reading["invalid_sources"]}
    assert by_path.get(".specify/evidence/ev-neg-broken/findings.json") == "unparsable", (
        "the seeded broken reference must surface in invalid_sources as unparsable: %r" % by_path
    )
    assert reading["coverage"]["invalid_records"] == len(reading["invalid_sources"]), (
        "the invalid-record count must equal the disclosed list: %r"
        % reading["invalid_sources"]
    )


def test_the_dated_baseline_entry_replays_against_its_citations():
    entries = [
        path for path in sorted(FEEDBACK_DIR.glob("*.md"))
        if BASELINE_MARKER in path.read_text(encoding="utf-8")
    ]
    assert len(entries) == 1, (
        "exactly one dated baseline entry must exist under .specify/feedback/; found %r"
        % [path.name for path in entries]
    )
    baseline = _json_block(entries[0].read_text(encoding="utf-8"))
    assert baseline["feature"] == "109-prompt-adherence"
    assert baseline["status"] in {"complete", "partial", "no-data", "not-found"}
    for rel in baseline["sources"]:
        assert (REPO_ROOT / rel).is_file(), "the baseline cites an unresolvable path %r" % rel

    proc = _run("--json", "--run", baseline["scope"]["run"])
    assert proc.returncode == 0, (
        "the replay engine run must exit 0; rc=%d stderr=%r" % (proc.returncode, proc.stderr)
    )
    replay = json.loads(proc.stdout)
    assert replay["declaration_set"]["version"] == baseline["declaration_set_version"], (
        "the declaration-set digest drifted since the baseline was recorded"
    )
    assert replay["coverage"]["invalid_records"] == baseline["coverage"]["invalid_records"]
    assert replay["coverage"]["records_in_scope"] == baseline["coverage"]["records_in_scope"]

    expected_partial = False
    for row, recorded in baseline["observations"].items():
        observation = _observation(replay, row)
        if row == "probe-registry-declaration":
            # The declaration row evaluates once against current state under a default scope
            # (Wired); under the explicit-run replay its documented derivation is
            # not_evaluated / no-matching-records (the edge case FR-028 records).
            assert recorded["state"] == "Wired"
            expected_partial = True
            assert observation["state"] == "not_evaluated"
            assert observation["reason"]["cause"] == "no-matching-records"
            continue
        if recorded["state"] in POSITIVE_STATES:
            assert observation["state"] == recorded["state"], (
                "row %r replayed as %r; the baseline recorded %r"
                % (row, observation["state"], recorded["state"])
            )
            assert observation["deviation_classes"] == recorded["deviation_classes"], (
                "row %r replayed with classes %r; the baseline recorded %r"
                % (row, observation["deviation_classes"], recorded["deviation_classes"])
            )
        else:
            # The baseline was a default-scope reading; the replay pins the same identity with
            # --run, which per the declared four-way derivation shifts an absence from
            # Unobserved to not_evaluated. Both are absence states carrying a reason.
            expected_partial = True
            assert recorded["state"] == "Unobserved", (
                "a default-scope absence records Unobserved; saw %r on row %r"
                % (recorded["state"], row)
            )
            assert observation["state"] == "not_evaluated", (
                "under the explicit-run replay row %r reads %r, never a positive state"
                % (row, observation["state"])
            )
            assert observation["reason"]["cause"] == recorded["reason_cause"]
            assert observation["reason"]["cause"] == "no-matching-records"
    assert replay["status"] == ("partial" if expected_partial else baseline["status"]), (
        "the replay status %r does not match the scope-shifted expectation" % replay["status"]
    )
