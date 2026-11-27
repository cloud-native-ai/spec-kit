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
window, advisory and audit-replay legs are later slices' rows (T027, T030, T032) and extend
this file there; they are not claimed here.
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