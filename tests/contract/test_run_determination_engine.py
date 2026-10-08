"""Contract tests for the Run Determination engine (运行判定).

Engine: ``scripts/python/run-determination.py``
Design truth: ``.specify/teams/.work/session-driven-self-improvement/outputs/judgment-contract.md``
(dated S1 record; after S3/S4 land, ownership migrates per its header block).

The classes below are named after the contract's § 15 verification hooks so S5
can check each hook without re-deriving it. Two house disciplines shape the file:

* **Red-First 取证 / 变异演练** (owner: ``.specify/memory/glossary.md``). Every
  guard here was run red before the engine existed, and three of them were
  mutation-drilled; the evidence lives at
  ``.specify/teams/.work/session-driven-self-improvement/outputs/red-first-evidence.md``.
* **反空真哨兵** — an "empty is good" reading is always paired with a companion
  reading that something was actually measured, so "empty because correct" and
  "empty because blind" stay distinguishable.

``TestOwnerSurfaces`` deliberately does not touch the engine: it pins the
pre-existing framework facts the engine wires rather than invents. Those tests
pass in the red-first run, which is what makes the engine tests' red
discriminating — the module imports, the fixtures resolve and the syntax is
sound, so only the subject is absent.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
#: The tree the engine under test lives in. Canonically the repository root;
#: during S2 it is the run-workspace overlay that also carries the engine.
ENGINE_ROOT = _HERE.parents[2]
ENGINE = ENGINE_ROOT / "scripts" / "python" / "run-determination.py"


def _framework_root() -> Path:
    """Nearest ancestor that is the framework source tree (Two Hats: the root,
    never the ``.specify/`` mirror)."""
    for candidate in (ENGINE_ROOT, *ENGINE_ROOT.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".specify").is_dir():
            return candidate
    return ENGINE_ROOT


FRAMEWORK_ROOT = _framework_root()


def load_engine():
    assert ENGINE.is_file(), f"engine missing: {ENGINE}"
    spec = importlib.util.spec_from_file_location("run_determination_under_test", ENGINE)
    assert spec is not None and spec.loader is not None, f"cannot load spec for {ENGINE}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return load_engine()


@pytest.fixture(scope="module")
def engine_source() -> str:
    assert ENGINE.is_file(), f"engine missing: {ENGINE}"
    return ENGINE.read_text(encoding="utf-8")


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    """A bare project workspace with the memory session store present."""
    (tmp_path / ".specify" / "memory" / "session").mkdir(parents=True)
    return tmp_path


@pytest.fixture(autouse=True)
def framework_store_untouched():
    """Two-hats guard: the documented path-resolution trap surfaces as workspace
    state written into the framework repository rather than as a failing test, so
    make it a failing test. Every test must pass an explicit --workspace-root."""
    store = FRAMEWORK_ROOT / ".specify" / "memory" / "session"
    before = sorted(p.name for p in store.glob("*")) if store.is_dir() else []
    yield
    after = sorted(p.name for p in store.glob("*")) if store.is_dir() else []
    assert after == before, (
        f"a test wrote into the framework repository's session store: "
        f"added={sorted(set(after) - set(before))}"
    )


def run_cli(eng, args, capsys, as_json=True):
    """Invoke the engine in-process; return (exit_code, json_payload_or_None, captured)."""
    argv = (["--json"] if as_json else []) + [str(a) for a in args]
    rc = eng.main(argv)
    captured = capsys.readouterr()
    payload = None
    if captured.out.strip():
        try:
            payload = json.loads(captured.out)
        except json.JSONDecodeError:
            payload = None
    return rc, payload, captured


def determine_args(ws, unit_id="/speckit.plan", run_id="run-001", **over):
    args = [
        "--action", "determine",
        "--workspace-root", str(ws),
        "--unit-id", unit_id,
        "--run-id", run_id,
        "--complexity", "complex",
    ]
    for key, value in over.items():
        if value is None:
            continue
        flag = "--" + key.replace("_", "-")
        if isinstance(value, (list, tuple)):
            for item in value:
                args += [flag, str(item)]
        elif isinstance(value, bool):
            if value:
                args.append(flag)
        else:
            args += [flag, str(value)]
    return args


def settle_args(ws, unit_id="/speckit.plan", run_id=None, turn_class="topic_change"):
    args = ["--action", "settle", "--workspace-root", str(ws),
            "--unit-id", unit_id, "--user-turn-class", turn_class]
    if run_id:
        args += ["--run-id", run_id]
    return args


def history_args(ws, *extra, target="/speckit.plan"):
    return ["--action", "history", "--workspace-root", str(ws),
            "--target", target, *extra]


_FENCE = re.compile(r"```json\n(.*?)\n```", re.S)


def record_of(ws: Path, run_id: str) -> dict:
    """Read back one persisted determination record (program-side read)."""
    session = ws / ".specify" / "memory" / "session"
    for path in sorted(session.glob("*.md")):
        match = _FENCE.search(path.read_text(encoding="utf-8"))
        if not match:
            continue
        record = json.loads(match.group(1))
        if record.get("run_id") == run_id:
            return record
    raise AssertionError(f"no persisted record for run_id={run_id}")


def only_record(ws: Path) -> dict:
    session = ws / ".specify" / "memory" / "session"
    bodies = [p for p in sorted(session.glob("*.md")) if _FENCE.search(p.read_text(encoding="utf-8"))]
    assert len(bodies) == 1, f"expected exactly one record, got {[p.name for p in bodies]}"
    return json.loads(_FENCE.search(bodies[0].read_text(encoding="utf-8")).group(1))


def write_names(path: Path, names) -> Path:
    path.write_text("".join(f"{n}\n" for n in names), encoding="utf-8")
    return path


def write_session(path: Path, rows) -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def usage_row(ts="2026-10-06T10:00:00.000Z", multiplier=1):
    return {
        "type": "assistant",
        "timestamp": ts,
        "message": {"role": "assistant", "usage": {
            "input_tokens": 100 * multiplier, "output_tokens": 50 * multiplier,
            "cache_read_input_tokens": 10 * multiplier,
            "cache_creation_input_tokens": 5 * multiplier}},
    }


def write_proxy(path: Path, size: int) -> Path:
    path.write_text("x" * size, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Owner surfaces — pre-existing framework facts the engine wires, not invents.
# These pass in the red-first run; they are the discriminator proving that a red
# engine test failed because the engine is absent, not because this file is broken.
# ---------------------------------------------------------------------------

class TestOwnerSurfaces:
    def test_engine_home_is_the_framework_root_not_the_mirror(self):
        assert (FRAMEWORK_ROOT / "scripts" / "python").is_dir()
        assert (FRAMEWORK_ROOT / "shared" / "workflow" / "feedback-step.md").is_file()

    def test_sibling_engines_the_engine_reuses_exist(self):
        for name in ("memory-utils.py", "evidence-utils.py", "history-utils.py"):
            assert (ENGINE.parent / name).is_file(), f"missing sibling engine: {name}"

    def test_names_out_flag_is_owned_by_run_tests_sh(self):
        text = (FRAMEWORK_ROOT / "scripts" / "bash" / "run-tests.sh").read_text(encoding="utf-8")
        assert "--names-out" in text

    def test_exit_code_table_is_owned_by_sibling_engine_constants(self):
        text = (FRAMEWORK_ROOT / "scripts" / "python" / "goal-utils.py").read_text(encoding="utf-8")
        for const in ("EXIT_OK = 0", "EXIT_INPUT_ERROR = 2",
                      "EXIT_NOT_FOUND = 3", "EXIT_INVALID = 4"):
            assert const in text

    def test_memory_engine_owns_record_and_reindex(self):
        text = (FRAMEWORK_ROOT / "scripts" / "python" / "memory-utils.py").read_text(encoding="utf-8")
        assert "def action_record" in text
        assert "def action_reindex" in text

    def test_evidence_engine_owns_latest_and_load_run(self):
        text = (FRAMEWORK_ROOT / "scripts" / "python" / "evidence-utils.py").read_text(encoding="utf-8")
        assert "def action_latest" in text
        assert "def load_run" in text
        assert "findingsDigest" in text

    def test_history_engine_owns_store_resolvers(self):
        text = (FRAMEWORK_ROOT / "scripts" / "python" / "history-utils.py").read_text(encoding="utf-8")
        assert "STORE_RESOLVERS" in text
        assert "UNSUPPORTED_TOOL_HINTS" in text

    def test_glossary_owns_the_machinery_terms(self):
        text = (FRAMEWORK_ROOT / ".specify" / "memory" / "glossary.md").read_text(encoding="utf-8")
        for term in ("名字级基线", "Red-First 取证", "变异演练", "反空真哨兵", "改点", "运行判定"):
            assert term in text, f"glossary entry missing: {term}"

    def test_no_op_line_is_owned_by_the_feedback_engine(self):
        text = (FRAMEWORK_ROOT / "scripts" / "python" / "feedback-utils.py").read_text(encoding="utf-8")
        assert "NO_OP_POINT" in text


# ---------------------------------------------------------------------------
# § 2 — engine identity, actions, exit codes, shared --json
# ---------------------------------------------------------------------------

class TestEngineSurface:
    def test_engine_file_exists(self):
        assert ENGINE.is_file(), f"engine missing: {ENGINE}"

    def test_engine_source_compiles(self):
        compile(ENGINE.read_text(encoding="utf-8"), str(ENGINE), "exec")

    def test_exit_constants_match_the_house_table(self, eng):
        assert (eng.EXIT_OK, eng.EXIT_INPUT_ERROR,
                eng.EXIT_NOT_FOUND, eng.EXIT_INVALID) == (0, 2, 3, 4)

    def test_action_set_is_closed(self, eng):
        assert tuple(eng.ACTIONS) == ("determine", "settle", "history")

    def test_unknown_action_exits_2(self, eng, ws):
        with pytest.raises(SystemExit) as exc:
            eng.main(["--action", "nonsense", "--workspace-root", str(ws)])
        assert exc.value.code == 2

    def test_missing_action_exits_2(self, eng, ws):
        with pytest.raises(SystemExit):
            eng.main(["--workspace-root", str(ws)])

    def test_json_flag_is_position_independent_c11(self, eng, ws, capsys):
        """C-11 guard: one shared flag definition, so position cannot change the
        shape the caller receives."""
        tail = ["--action", "history", "--workspace-root", str(ws), "--target", "/speckit.plan"]
        rc_a, out_a, _ = run_cli(eng, tail, capsys)                              # --json first
        rc_b, out_b, _ = run_cli(eng, tail + ["--json"], capsys, as_json=False)  # --json last
        assert rc_a == rc_b == 0
        assert out_a is not None and out_b is not None
        assert out_a == out_b

    def test_determine_requires_unit_id_run_id_complexity(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, ["--action", "determine", "--workspace-root", str(ws),
                                 "--unit-id", "/speckit.plan", "--run-id", "r1"], capsys)
        assert rc == 2
        rc, _, _ = run_cli(eng, ["--action", "determine", "--workspace-root", str(ws),
                                 "--unit-id", "/speckit.plan", "--complexity", "complex"], capsys)
        assert rc == 2
        rc, _, _ = run_cli(eng, ["--action", "determine", "--workspace-root", str(ws),
                                 "--run-id", "r1", "--complexity", "complex"], capsys)
        assert rc == 2

    def test_invalid_unit_id_exits_2(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, unit_id="not-a-unit"), capsys)
        assert rc == 2

    def test_unit_type_contradiction_exits_2(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, unit_type="skill"), capsys)
        assert rc == 2

    @pytest.mark.parametrize("unit_id,expected", [
        ("/speckit.plan", "command"),
        ("skill:study-project", "skill"),
        ("custom:team/reviewer", "custom-unit"),
    ])
    def test_unit_type_derived_from_unit_id(self, eng, unit_id, expected):
        assert eng.unit_type_of(unit_id) == expected

    def test_simple_unit_is_skipped_and_writes_nothing(self, eng, ws, capsys):
        rc, payload, _ = run_cli(eng, determine_args(ws, complexity="simple"), capsys)
        assert rc == 0
        assert payload == {"skipped": "simple-unit"}
        assert [p.name for p in (ws / ".specify" / "memory" / "session").glob("*.md")] == []

    def test_duplicate_key_no_ops(self, eng, ws, capsys):
        rc1, _, _ = run_cli(eng, determine_args(ws), capsys)
        rc2, payload2, _ = run_cli(eng, determine_args(ws), capsys)
        assert rc1 == 0 and rc2 == 0
        assert payload2.get("duplicate") is True
        assert len(list((ws / ".specify" / "memory" / "session").glob("*.md"))) == 1


# ---------------------------------------------------------------------------
# § 15 hook 1 — value-domain closure
# ---------------------------------------------------------------------------

class TestValueDomainClosure:
    def test_every_axis_present_in_every_record(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws), capsys)
        assert rc == 0
        record = only_record(ws)
        assert set(record["axes"]) == set(eng.AXES)
        for axis in eng.AXES:
            body = record["axes"][axis]
            assert isinstance(body, dict), f"axis {axis} must be an object, never null"
            assert body["verdict"] in eng.domain_of(axis)
            assert body["signal"] == {"key": axis, "direction": eng.SIGNAL_DIRECTIONS[axis]}

    def test_reason_non_null_iff_not_evaluated(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        record = only_record(ws)
        assert eng.validate_record(record) == []
        for axis, body in record["axes"].items():
            assert (body["reason"] is not None) == (body["verdict"] == "not_evaluated"), axis

    def test_reason_values_come_from_the_closed_set(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        for body in only_record(ws)["axes"].values():
            assert body["reason"] is None or body["reason"] in eng.REASONS

    def test_unqualified_run_forces_every_axis_to_unqualified(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, qualification="aborted"), capsys)
        for axis, body in only_record(ws)["axes"].items():
            assert body["verdict"] == "not_evaluated", axis
            assert body["reason"] == "unqualified_run", axis

    def test_no_aggregate_score_anywhere(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        flat = json.dumps(only_record(ws))
        for banned in ("score", "severity", "weighted", "total_quality", "aggregate"):
            assert banned not in flat, f"aggregate roll-up leaked: {banned}"
        assert not hasattr(eng, "aggregate_score")

    def test_ok_and_comparison_words_never_cross_domains(self, eng):
        """`ok` never appears on a comparison axis (`unchanged` already means it)
        and the trend words never appear on artifact_correctness — with the one
        exception the § 5.0 domain table itself lists: `regressed`, which is what
        a non-empty failed-set difference maps to in § 5.3."""
        assert "ok" not in eng.COMPARISON_VERDICTS
        for word in ("improved", "unchanged"):
            assert word not in eng.CORRECTNESS_VERDICTS
        assert eng.CORRECTNESS_VERDICTS == ("ok", "regressed", "not_evaluated")
        assert eng.SATISFACTION_VERDICTS == ("accepted", "rejected", "not_evaluated")

    def test_the_biconditional_has_exactly_one_declared_exception(self, eng):
        """§ 7 rule 2 (reason non-null iff not_evaluated) and § 5.4's
        `accepted / red_state_undeclared` row conflict as written. The conflict is
        resolved at ONE site and this test pins how narrow that site is: widening
        it must be a visible edit, and it is reported as an anomaly rather than
        settled silently."""
        assert eng.REASON_WITH_SUBSTANTIVE_VERDICT == (
            ("satisfaction", "accepted", "red_state_undeclared"),)

    def test_an_undeclared_accept_keeps_its_reason(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", unresolved_red="unknown"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a", turn_class="topic_change"), capsys)
        axis = record_of(ws, "run-a")["axes"]["satisfaction"]
        assert axis["verdict"] == "accepted"
        assert axis["reason"] == "red_state_undeclared"
        assert eng.validate_record(record_of(ws, "run-a")) == []

    def test_record_is_bounded(self, eng, ws, tmp_path, capsys):
        session = write_session(tmp_path / "s.jsonl", [usage_row() for _ in range(50)])
        refs = tmp_path / "refs.md"
        refs.write_text("check-a red-first evidence line\n" * 200, encoding="utf-8")
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        run_cli(eng, determine_args(ws, session_file=session, session_rows="0:49",
                                    names_current=current, names_baseline=baseline,
                                    collected=3, declared_check=["check-a"],
                                    green_check=["check-a"],
                                    red_first_refs=[str(refs)]), capsys)
        blob = json.dumps(only_record(ws))
        assert len(blob) < 20000
        assert "red-first evidence line" not in blob
        assert '"type": "assistant"' not in blob, "raw session rows must never be embedded"
        assert blob.count("tests/a.py::test_old") <= 1


# ---------------------------------------------------------------------------
# § 15 hook 2 — unavailable-source honesty (never ok, never 0, never an estimate)
# ---------------------------------------------------------------------------

class TestUnavailableSourceHonesty:
    def test_all_four_axes_report_not_evaluated_with_no_source(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws), capsys)
        assert rc == 0
        axes = only_record(ws)["axes"]
        assert axes["token_consumption"]["verdict"] == "not_evaluated"
        assert axes["token_consumption"]["reason"] == "source_unavailable"
        assert axes["elapsed"]["verdict"] == "not_evaluated"
        assert axes["elapsed"]["reason"] == "source_unavailable"
        assert axes["artifact_correctness"]["verdict"] == "not_evaluated"
        assert axes["artifact_correctness"]["reason"] == "no_declared_checks"
        assert axes["satisfaction"]["verdict"] == "not_evaluated"
        assert axes["satisfaction"]["reason"] == "pending_next_turn"

    def test_no_axis_reports_ok_or_accepted_without_a_source(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        for axis, body in only_record(ws)["axes"].items():
            assert body["verdict"] not in ("ok", "accepted"), axis

    def test_unavailable_measurements_carry_null_never_zero(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        record = only_record(ws)
        token = record["axes"]["token_consumption"]["measurement"]
        assert token["source"] == "unavailable"
        for field in ("input_tokens", "output_tokens", "cache_read_input_tokens",
                      "cache_creation_input_tokens", "total_tokens",
                      "proxy_lines", "proxy_bytes"):
            assert token[field] is None, f"{field} must be null, never a fabricated 0"
        elapsed = record["axes"]["elapsed"]["measurement"]
        assert elapsed["source"] == "unavailable"
        assert elapsed["ms"] is None
        correctness = record["axes"]["artifact_correctness"]
        assert correctness["declared_checks"] is None
        assert correctness["collected"] is None

    def test_unsupported_tool_reports_source_unavailable_not_a_guess(self, eng, ws, capsys):
        """``UNSUPPORTED_TOOL_HINTS`` owns which agents are not resolvable; the
        engine echoes that state and never a number."""
        rc, _, _ = run_cli(eng, determine_args(ws, tool="codex"), capsys)
        assert rc == 0
        record = only_record(ws)
        assert record["axes"]["token_consumption"]["verdict"] == "not_evaluated"
        assert record["axes"]["token_consumption"]["reason"] == "source_unavailable"
        assert record["provenance"]["session_store"]["supported"] is False

    def test_note_is_echoed_and_never_influences_the_verdict(self, eng, ws, capsys):
        note = "regressed badly, improved nothing, ok fine"
        run_cli(eng, determine_args(ws, token_note=note), capsys)
        record = only_record(ws)
        assert record["axes"]["token_consumption"]["measurement"]["note"] == note
        assert record["axes"]["token_consumption"]["verdict"] == "not_evaluated"
        assert record["axes"]["token_consumption"]["reason"] == "source_unavailable"


# ---------------------------------------------------------------------------
# § 5.1 / § 5.2 — three-tier source hierarchy, baselines, the not_comparable case
# ---------------------------------------------------------------------------

class TestSourceHierarchy:
    def test_source_1_sums_usage_over_the_declared_row_span(self, eng, ws, tmp_path, capsys):
        session = write_session(tmp_path / "s.jsonl", [usage_row() for _ in range(3)])
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session,
                                               session_rows="0:2"), capsys)
        assert rc == 0
        m = only_record(ws)["axes"]["token_consumption"]["measurement"]
        assert m["source"] == "tool_session_usage"
        assert m["input_tokens"] == 300
        assert m["output_tokens"] == 150
        assert m["cache_read_input_tokens"] == 30
        assert m["cache_creation_input_tokens"] == 15
        assert m["total_tokens"] == 495

    def test_source_1_requires_a_declared_row_span(self, eng, ws, tmp_path, capsys):
        """No span => the tokens cannot be attributed to this run; summing a whole
        session would carry another run's consumption into this record."""
        session = write_session(tmp_path / "s.jsonl", [usage_row() for _ in range(3)])
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session), capsys)
        assert rc == 0
        m = only_record(ws)["axes"]["token_consumption"]["measurement"]
        assert m["source"] == "unavailable"
        assert m["total_tokens"] is None

    def test_row_span_out_of_range_exits_2(self, eng, ws, tmp_path, capsys):
        session = write_session(tmp_path / "s.jsonl", [usage_row()])
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session,
                                               session_rows="0:9"), capsys)
        assert rc == 2

    def test_malformed_row_span_exits_2(self, eng, ws, tmp_path, capsys):
        session = write_session(tmp_path / "s.jsonl", [usage_row()])
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session,
                                               session_rows="zero:one"), capsys)
        assert rc == 2

    def test_source_2_line_byte_proxy(self, eng, ws, tmp_path, capsys):
        target = write_proxy(tmp_path / "read-set.txt", 4096)
        rc, _, _ = run_cli(eng, determine_args(ws, proxy_paths=[str(target)]), capsys)
        assert rc == 0
        m = only_record(ws)["axes"]["token_consumption"]["measurement"]
        assert m["source"] == "line_byte_proxy"
        assert m["proxy_bytes"] == 4096
        assert m["proxy_lines"] == 1
        assert m["total_tokens"] is None

    def test_missing_proxy_path_exits_2(self, eng, ws, tmp_path, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, proxy_paths=[str(tmp_path / "nope.txt")]), capsys)
        assert rc == 2

    def test_elapsed_source_1_is_last_row_minus_first_row_in_ms(self, eng, ws, tmp_path, capsys):
        rows = [usage_row("2026-10-06T10:00:00.000Z"),
                usage_row("2026-10-06T10:00:01.500Z"),
                usage_row("2026-10-06T10:00:04.000Z")]
        session = write_session(tmp_path / "s.jsonl", rows)
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session,
                                               session_rows="0:2"), capsys)
        assert rc == 0
        m = only_record(ws)["axes"]["elapsed"]["measurement"]
        assert m["source"] == "tool_session_timestamps"
        assert m["ms"] == 4000

    def test_elapsed_source_2_is_caller_declared_and_labelled(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, elapsed_ms=1234), capsys)
        assert rc == 0
        record = only_record(ws)
        m = record["axes"]["elapsed"]["measurement"]
        assert m["source"] == "caller_declared_ms"
        assert m["ms"] == 1234
        assert "elapsed_ms" in record["provenance"]["declared_by_caller"]

    def test_unparseable_timestamps_degrade_to_unavailable(self, eng, ws, tmp_path, capsys):
        rows = [usage_row("not-a-timestamp"), usage_row()]
        session = write_session(tmp_path / "s.jsonl", rows)
        rc, _, _ = run_cli(eng, determine_args(ws, session_file=session,
                                               session_rows="0:1"), capsys)
        assert rc == 0
        m = only_record(ws)["axes"]["elapsed"]["measurement"]
        assert m["source"] == "unavailable"
        assert m["ms"] is None

    def test_elapsed_source_1_outranks_a_declared_span(self, eng, ws, tmp_path, capsys):
        rows = [usage_row("2026-10-06T10:00:00.000Z"), usage_row("2026-10-06T10:00:02.000Z")]
        session = write_session(tmp_path / "s.jsonl", rows)
        run_cli(eng, determine_args(ws, session_file=session, session_rows="0:1",
                                    elapsed_ms=999), capsys)
        m = only_record(ws)["axes"]["elapsed"]["measurement"]
        assert m["source"] == "tool_session_timestamps"
        assert m["ms"] == 2000

    def test_mixing_an_exact_count_with_a_proxy_is_not_comparable(self, eng):
        assert eng.sources_comparable("tool_session_usage", "line_byte_proxy") is False
        assert eng.sources_comparable("line_byte_proxy", "tool_session_usage") is False
        assert eng.sources_comparable("line_byte_proxy", "line_byte_proxy") is True
        assert eng.sources_comparable("tool_session_usage", "tool_session_usage") is True
        assert eng.sources_comparable("unavailable", "tool_session_usage") is False
        assert eng.sources_comparable("caller_declared_ms", "tool_session_timestamps") is False

    def test_improved_verdict_against_a_settled_baseline(self, eng, ws, tmp_path, capsys):
        big = write_session(tmp_path / "big.jsonl", [usage_row() for _ in range(4)])
        run_cli(eng, determine_args(ws, run_id="run-a", session_file=big,
                                    session_rows="0:3"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        small = write_session(tmp_path / "small.jsonl", [usage_row() for _ in range(2)])
        run_cli(eng, determine_args(ws, run_id="run-b", session_file=small,
                                    session_rows="0:1"), capsys)
        axis = record_of(ws, "run-b")["axes"]["token_consumption"]
        assert axis["verdict"] == "improved"
        assert axis["reason"] is None
        assert axis["baseline"]["run_id"] == "run-a"
        assert axis["baseline"]["source"] == "tool_session_usage"
        assert axis["baseline"]["value"] == 660

    def test_regressed_verdict_against_a_settled_baseline(self, eng, ws, tmp_path, capsys):
        small = write_session(tmp_path / "small.jsonl", [usage_row() for _ in range(2)])
        run_cli(eng, determine_args(ws, run_id="run-a", session_file=small,
                                    session_rows="0:1"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        big = write_session(tmp_path / "big.jsonl", [usage_row() for _ in range(5)])
        run_cli(eng, determine_args(ws, run_id="run-b", session_file=big,
                                    session_rows="0:4"), capsys)
        assert record_of(ws, "run-b")["axes"]["token_consumption"]["verdict"] == "regressed"

    def test_unchanged_verdict_on_exact_equality_no_tolerance_band(self, eng, ws, tmp_path, capsys):
        """OI-8: exact comparison; a one-unit move is a real move, never banded."""
        a = write_session(tmp_path / "a.jsonl", [usage_row() for _ in range(2)])
        run_cli(eng, determine_args(ws, run_id="run-a", session_file=a,
                                    session_rows="0:1"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        b = write_session(tmp_path / "b.jsonl", [usage_row() for _ in range(2)])
        run_cli(eng, determine_args(ws, run_id="run-b", session_file=b,
                                    session_rows="0:1"), capsys)
        assert record_of(ws, "run-b")["axes"]["token_consumption"]["verdict"] == "unchanged"

    def test_unsettled_record_is_not_a_baseline(self, eng, ws, tmp_path, capsys):
        big = write_session(tmp_path / "big.jsonl", [usage_row() for _ in range(4)])
        run_cli(eng, determine_args(ws, run_id="run-a", session_file=big,
                                    session_rows="0:3"), capsys)
        small = write_session(tmp_path / "small.jsonl", [usage_row() for _ in range(2)])
        run_cli(eng, determine_args(ws, run_id="run-b", session_file=small,
                                    session_rows="0:1"), capsys)
        axis = record_of(ws, "run-b")["axes"]["token_consumption"]
        assert axis["baseline"] is None
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "no_baseline"

    def test_mixed_source_baseline_is_not_comparable(self, eng, ws, tmp_path, capsys):
        proxy = write_proxy(tmp_path / "read-set.txt", 4096)
        run_cli(eng, determine_args(ws, run_id="run-a", proxy_paths=[str(proxy)]), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        big = write_session(tmp_path / "big.jsonl", [usage_row() for _ in range(4)])
        run_cli(eng, determine_args(ws, run_id="run-b", session_file=big,
                                    session_rows="0:3"), capsys)
        axis = record_of(ws, "run-b")["axes"]["token_consumption"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "not_comparable"
        assert axis["baseline"]["source"] == "line_byte_proxy"
        assert axis["baseline"]["value"] == 4096

    def test_elapsed_baseline_uses_its_own_source(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", elapsed_ms=1000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b", elapsed_ms=2500), capsys)
        axis = record_of(ws, "run-b")["axes"]["elapsed"]
        assert axis["verdict"] == "regressed"
        assert axis["baseline"] == {"run_id": "run-a", "source": "caller_declared_ms",
                                    "value": 1000}

    def test_baseline_is_the_most_recent_settled_record_not_the_most_recent(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", elapsed_ms=1000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b", elapsed_ms=5000), capsys)  # stays unsettled
        run_cli(eng, determine_args(ws, run_id="run-c", elapsed_ms=2000), capsys)
        axis = record_of(ws, "run-c")["axes"]["elapsed"]
        assert axis["baseline"]["run_id"] == "run-a"
        assert axis["verdict"] == "regressed"


# ---------------------------------------------------------------------------
# § 15 hook 3 — anti-vacuity sentinel on the failed-set difference
# ---------------------------------------------------------------------------

class TestAntiVacuitySentinelOnDiff:
    def test_empty_diff_with_nothing_collected_is_not_evaluated(self, eng, ws, tmp_path, capsys):
        """'pytest collected nothing' and 'pytest passed everything' must not
        produce the same verdict — the blind-check class."""
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", [])
        refs = tmp_path / "refs.md"
        refs.write_text("check-a red-first\n", encoding="utf-8")
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=0,
            declared_check=["check-a"], green_check=["check-a"],
            red_first_refs=[str(refs)]), capsys)
        assert rc == 0
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["failed_set_diff"]["status"] == "empty"
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "no_declared_checks"

    def test_empty_diff_with_collected_and_full_green_evidence_is_ok(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/old.py::test_already_failing"])
        refs = tmp_path / "red-first-evidence.md"
        refs.write_text("red-first evidence for check-a: FAILED then green\n", encoding="utf-8")
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=12,
            declared_check=["check-a"], green_check=["check-a"],
            red_first_refs=[str(refs)]), capsys)
        assert rc == 0
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "ok"
        assert axis["reason"] is None
        assert axis["green_evidence"]["status"] == "complete"
        assert axis["green_evidence"]["uncovered"] == []
        assert axis["declared_checks"] == 1
        assert axis["collected"] == 12

    def test_non_empty_diff_is_regressed(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt",
                              ["tests/a.py::test_one", "tests/b.py::test_two"])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_one"])
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=9,
            declared_check=["check-a"], green_check=["check-a"]), capsys)
        assert rc == 0
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "regressed"
        assert axis["reason"] is None
        assert axis["failed_set_diff"]["status"] == "non_empty"
        assert axis["failed_set_diff"]["added"] == ["tests/b.py::test_two"]
        assert axis["failed_set_diff"]["added_count"] == 1
        assert axis["failed_set_diff"]["truncated"] is False

    def test_diff_is_name_level_never_a_count(self, eng, ws, tmp_path, capsys):
        """名字级基线: equal counts with a swapped failure set is still a regression."""
        current = write_names(tmp_path / "current.txt", ["tests/a.py::test_new"])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        run_cli(eng, determine_args(ws, names_current=current, names_baseline=baseline,
                                    collected=5, declared_check=["c"], green_check=["c"]), capsys)
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["failed_set_diff"]["status"] == "non_empty"
        assert axis["failed_set_diff"]["added"] == ["tests/a.py::test_new"]
        assert axis["failed_set_diff"]["added_count"] == 1
        assert axis["verdict"] == "regressed"

    def test_missing_baseline_names_file_is_no_baseline(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", ["tests/a.py::test_one"])
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=str(tmp_path / "absent.txt"),
            collected=5, declared_check=["c"], green_check=["c"]), capsys)
        assert rc == 0
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "no_baseline"
        assert axis["failed_set_diff"]["status"] == "not_evaluated"

    def test_zero_declared_checks_is_no_declared_checks(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        run_cli(eng, determine_args(ws, names_current=current, names_baseline=baseline,
                                    collected=7), capsys)
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "no_declared_checks"
        assert axis["declared_checks"] == 0

    def test_no_names_files_at_all_is_no_declared_checks(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "no_declared_checks"
        assert axis["declared_checks"] is None
        assert axis["failed_set_diff"]["status"] == "not_evaluated"

    def test_added_list_is_bounded_and_flags_truncation(self, eng, ws, tmp_path, capsys):
        many = [f"tests/x.py::test_{i:04d}" for i in range(eng.MAX_ADDED_NAMES + 30)]
        current = write_names(tmp_path / "current.txt", many)
        baseline = write_names(tmp_path / "baseline.txt", [])
        run_cli(eng, determine_args(ws, names_current=current, names_baseline=baseline,
                                    collected=len(many), declared_check=["c"],
                                    green_check=["c"]), capsys)
        diff = only_record(ws)["axes"]["artifact_correctness"]["failed_set_diff"]
        assert diff["added_count"] == len(many)
        assert len(diff["added"]) == eng.MAX_ADDED_NAMES
        assert diff["truncated"] is True

    def test_green_check_must_be_a_declared_check(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["x"])
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=3,
            declared_check=["check-a"], green_check=["check-ghost"]), capsys)
        assert rc == 2

    def test_missing_red_first_ref_path_exits_2(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["x"])
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=3,
            declared_check=["check-a"], green_check=["check-a"],
            red_first_refs=[str(tmp_path / "absent.md")]), capsys)
        assert rc == 2


# ---------------------------------------------------------------------------
# § 5.3 green-evidence conjunction, and the OI-1 provisional ruling
# ---------------------------------------------------------------------------

class TestGreenEvidenceConjunction:
    def _run(self, eng, ws, tmp_path, capsys, refs_text, green, declared):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        refs = tmp_path / "red-first-evidence.md"
        refs.write_text(refs_text, encoding="utf-8")
        rc, _, _ = run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=10,
            declared_check=list(declared), green_check=list(green),
            red_first_refs=[str(refs)]), capsys)
        assert rc == 0
        return only_record(ws)["axes"]["artifact_correctness"]

    def test_partial_coverage_is_green_unproven(self, eng, ws, tmp_path, capsys):
        axis = self._run(eng, ws, tmp_path, capsys,
                         "red-first: check-a went FAILED before green\n",
                         green=["check-a", "check-b"], declared=["check-a", "check-b"])
        assert axis["green_evidence"]["status"] == "partial"
        assert axis["green_evidence"]["uncovered"] == ["check-b"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "green_unproven"

    def test_absent_coverage_is_green_unproven(self, eng, ws, tmp_path, capsys):
        axis = self._run(eng, ws, tmp_path, capsys, "no literal check names here\n",
                         green=["check-a"], declared=["check-a"])
        assert axis["green_evidence"]["status"] == "absent"
        assert axis["green_evidence"]["uncovered"] == ["check-a"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "green_unproven"

    def test_mutation_drill_record_counts_as_evidence(self, eng, ws, tmp_path, capsys):
        """变异演练 is accepted as an alternative to red-first: the search is one
        literal-substring search over the declared refs, whichever file kind."""
        axis = self._run(eng, ws, tmp_path, capsys,
                         "mutation drill log: check-a broke, went red, restored\n",
                         green=["check-a"], declared=["check-a"])
        assert axis["green_evidence"]["status"] == "complete"
        assert axis["verdict"] == "ok"

    def test_zero_green_checks_is_absent_never_vacuously_complete(self, eng, ws, tmp_path, capsys):
        """反空真哨兵 on the conjunction: 'every green check carries evidence' is
        vacuously true with zero green checks, so vacuity must not read as ok."""
        axis = self._run(eng, ws, tmp_path, capsys, "check-a is covered\n",
                         green=[], declared=["check-a"])
        assert axis["green_evidence"]["status"] == "absent"
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "green_unproven"

    def test_semantic_correctness_has_no_axis(self, eng, ws, capsys):
        """OI-4 / B2: 语义正确性 is out of scope and gets no placeholder axis."""
        run_cli(eng, determine_args(ws), capsys)
        record = only_record(ws)
        assert set(record["axes"]) == {"token_consumption", "elapsed",
                                       "artifact_correctness", "satisfaction"}
        assert "semantic" not in json.dumps(record)


class TestOI1ProvisionalRuling:
    """OI-1 was provisionally ruled **(a) not_evaluated / green_unproven**, NOT
    (b) regressed. The rationale, recorded here so the choice stays visible: an
    unproven green is an *unverified claim*, not a *measured regression* —
    reporting `regressed` would state a fact nobody measured, and would make "new
    failure" indistinguishable from "old green never proven" in the record. Both
    sub-signals stay visible, so overriding to (b) is a mapping change, not a
    schema change."""

    def test_the_ruling_is_isolated_at_a_single_site(self, engine_source):
        assert engine_source.count("GREEN_UNPROVEN_VERDICT") == 2, (
            "OI-1 must stay a single-site edit: one definition and one use")
        assert 'GREEN_UNPROVEN_VERDICT = ("not_evaluated", "green_unproven")' in engine_source

    def test_the_ruling_carries_its_rationale_next_to_the_site(self, engine_source):
        idx = engine_source.index("GREEN_UNPROVEN_VERDICT =")
        window = engine_source[max(0, idx - 1200):idx]
        assert "OI-1" in window
        assert "unverified claim" in window

    def test_unproven_green_is_not_regressed(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        run_cli(eng, determine_args(
            ws, names_current=current, names_baseline=baseline, collected=10,
            declared_check=["check-a"], green_check=["check-a"],
            red_first_refs=[]), capsys)
        axis = only_record(ws)["axes"]["artifact_correctness"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "green_unproven"
        assert axis["verdict"] != "regressed"
        assert axis["failed_set_diff"]["status"] == "empty"

    def test_the_mapping_is_reachable_from_one_constant(self, eng):
        assert eng.GREEN_UNPROVEN_VERDICT == ("not_evaluated", "green_unproven")
        assert eng.green_unproven_verdict() == eng.GREEN_UNPROVEN_VERDICT


# ---------------------------------------------------------------------------
# § 15 hook 5 — satisfaction table totality
# ---------------------------------------------------------------------------

class TestSatisfactionTableTotality:
    EXPECTED = {
        ("continuation_negative", "true"): ("rejected", None),
        ("continuation_negative", "false"): ("rejected", None),
        ("continuation_negative", "unknown"): ("rejected", None),
        ("continuation_non_negative", "true"): ("accepted", None),
        ("continuation_non_negative", "false"): ("accepted", None),
        ("continuation_non_negative", "unknown"): ("accepted", None),
        ("no_user_input", "true"): ("not_evaluated", "no_user_input"),
        ("no_user_input", "false"): ("not_evaluated", "no_user_input"),
        ("no_user_input", "unknown"): ("not_evaluated", "no_user_input"),
        ("topic_change", "false"): ("accepted", None),
        ("topic_change", "true"): ("not_evaluated", "red_adjacent"),
        ("topic_change", "unknown"): ("accepted", "red_state_undeclared"),
        ("session_end", "false"): ("accepted", None),
        ("session_end", "true"): ("not_evaluated", "red_adjacent"),
        ("session_end", "unknown"): ("accepted", "red_state_undeclared"),
    }

    def test_cross_product_is_exhausted_with_no_fallthrough(self, eng):
        product = {(c, r) for c in eng.USER_TURN_CLASSES for r in eng.UNRESOLVED_RED_VALUES}
        assert len(product) == 15
        assert set(eng.SATISFACTION_TABLE) == product
        for key in product:
            verdict, reason = eng.SATISFACTION_TABLE[key]
            assert verdict in eng.SATISFACTION_VERDICTS, key
            if verdict == "not_evaluated":
                assert reason is not None, key
            else:
                # The single declared exception to the § 7 rule-2 biconditional.
                assert (reason is None
                        or ("satisfaction", verdict, reason)
                        in eng.REASON_WITH_SUBSTANTIVE_VERDICT), key

    @pytest.mark.parametrize("key,expected", sorted(EXPECTED.items()))
    def test_each_row_matches_the_contract_table(self, eng, key, expected):
        assert eng.SATISFACTION_TABLE[key] == expected

    @pytest.mark.parametrize("key,expected", sorted(EXPECTED.items()))
    def test_resolver_agrees_with_the_table(self, eng, key, expected):
        turn_class, red = key
        resolved = eng.resolve_satisfaction(turn_class, red, "undeclared", "qualified")
        assert (resolved["verdict"], resolved["reason"]) == expected

    def test_adjacency_is_a_closed_predicate_not_a_time_window(self, eng):
        for turn_class in ("topic_change", "session_end"):
            assert eng.resolve_satisfaction(turn_class, "true", "engine_nonzero_exit",
                                            "qualified")["adjacent"] is True
        for turn_class in ("continuation_negative", "continuation_non_negative",
                           "no_user_input"):
            assert eng.resolve_satisfaction(turn_class, "true", "engine_nonzero_exit",
                                            "qualified")["adjacent"] is False

    def test_unqualified_run_beats_the_table(self, eng):
        resolved = eng.resolve_satisfaction("topic_change", "false", "none", "aborted")
        assert resolved["verdict"] == "not_evaluated"
        assert resolved["reason"] == "unqualified_run"

    def test_no_raw_user_text_is_stored(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws), capsys)
        blob = json.dumps(only_record(ws))
        for banned in ("user_text", "raw_input", "transcript", "prompt_text"):
            assert banned not in blob


# ---------------------------------------------------------------------------
# § 4 — two-invocation model, settlement, the honesty boundary
# ---------------------------------------------------------------------------

class TestSettlement:
    def test_determine_leaves_satisfaction_pending(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        axis = record["axes"]["satisfaction"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "pending_next_turn"
        assert axis["user_turn_class"] == "no_user_input"
        assert axis["adjacent"] is False
        assert record["settled_at"] is None

    def test_prev_user_turn_class_settles_the_previous_record(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        rc, payload, _ = run_cli(eng, determine_args(
            ws, run_id="run-b", prev_user_turn_class="topic_change"), capsys)
        assert rc == 0
        assert payload["settled_previous"]["run_id"] == "run-a"
        settled = record_of(ws, "run-a")
        assert settled["settled_at"] is not None
        assert settled["axes"]["satisfaction"]["verdict"] == "accepted"
        assert settled["axes"]["satisfaction"]["user_turn_class"] == "topic_change"

    def test_prev_user_turn_class_without_a_previous_record_is_reported(self, eng, ws, capsys):
        rc, payload, _ = run_cli(eng, determine_args(
            ws, run_id="run-a", prev_user_turn_class="topic_change"), capsys)
        assert rc == 0
        assert payload["settled_previous"] is None

    def test_settle_action_amends_one_record(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        rc, payload, _ = run_cli(eng, settle_args(ws, run_id="run-a",
                                                  turn_class="continuation_negative"), capsys)
        assert rc == 0
        assert payload["settled"] is True
        record = record_of(ws, "run-a")
        assert record["axes"]["satisfaction"]["verdict"] == "rejected"
        assert record["settled_at"] is not None

    def test_settle_without_run_id_picks_the_latest_unsettled(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, unit_id="/speckit.plan", run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, unit_id="skill:study-project", run_id="run-b"), capsys)
        rc, _, _ = run_cli(eng, settle_args(ws, turn_class="session_end"), capsys)
        assert rc == 0
        assert record_of(ws, "run-a")["settled_at"] is not None
        assert record_of(ws, "run-b")["settled_at"] is None

    def test_settle_with_no_unsettled_record_exits_3(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, settle_args(ws), capsys)
        assert rc == 3

    def test_settle_requires_a_unit_id(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, ["--action", "settle", "--workspace-root", str(ws),
                                 "--user-turn-class", "topic_change"], capsys)
        assert rc == 2

    def test_settle_is_idempotent(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        rc, payload, _ = run_cli(eng, settle_args(ws, run_id="run-a",
                                                  turn_class="continuation_negative"), capsys)
        assert rc == 0
        assert payload.get("already_settled") is True
        assert record_of(ws, "run-a")["axes"]["satisfaction"]["verdict"] == "accepted"
        assert len(list((ws / ".specify" / "memory" / "session").glob("*.md"))) == 1

    def test_settle_cannot_retrofit_the_red_state(self, eng, ws, capsys):
        """The red belongs to the run being determined (§ 5.4 adjacency), so it is
        read from that record and never re-declared at settle time."""
        run_cli(eng, determine_args(ws, run_id="run-a", unresolved_red="true",
                                    red_source="engine_nonzero_exit"), capsys)
        rc, _, _ = run_cli(eng, settle_args(ws, run_id="run-a") + ["--unresolved-red", "false"],
                           capsys)
        assert rc == 2

    def test_determine_rejects_its_own_user_turn_class(self, eng, ws, capsys):
        """Run N's satisfaction is by definition settled by a later turn, so
        --user-turn-class has no defined meaning on `determine`."""
        rc, _, captured = run_cli(eng, determine_args(ws, user_turn_class="topic_change"),
                                  capsys, as_json=False)
        assert rc == 2
        assert "--prev-user-turn-class" in captured.err

    def test_red_adjacent_session_end_is_not_an_accept(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", unresolved_red="true",
                                    red_source="surfaced_anomaly_unanswered"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a", turn_class="session_end"), capsys)
        axis = record_of(ws, "run-a")["axes"]["satisfaction"]
        assert axis["verdict"] == "not_evaluated"
        assert axis["reason"] == "red_adjacent"
        assert axis["unresolved_red"] == {"present": "true",
                                          "source": "surfaced_anomaly_unanswered"}
        assert axis["adjacent"] is True

    def test_true_red_requires_a_named_producer(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, unresolved_red="true"), capsys)
        assert rc == 2

    def test_false_red_defaults_to_source_none(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", unresolved_red="false"), capsys)
        axis = only_record(ws)["axes"]["satisfaction"]
        assert axis["unresolved_red"] == {"present": "false", "source": "none"}

    def test_unknown_red_defaults_to_undeclared(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        axis = only_record(ws)["axes"]["satisfaction"]
        assert axis["unresolved_red"] == {"present": "unknown", "source": "undeclared"}

    def test_contradictory_red_declaration_exits_2(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, determine_args(ws, unresolved_red="false",
                                               red_source="engine_nonzero_exit"), capsys)
        assert rc == 2

    def test_abandoned_run_stays_pending_never_a_fabricated_accept(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = record_of(ws, "run-a")
        assert record["axes"]["satisfaction"]["verdict"] == "not_evaluated"
        assert record["axes"]["satisfaction"]["reason"] == "pending_next_turn"
        assert record["settled_at"] is None

    def test_settling_an_unqualified_run_reports_unqualified(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", qualification="partial"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a", turn_class="topic_change"), capsys)
        record = record_of(ws, "run-a")
        assert record["settled_at"] is not None
        assert record["axes"]["satisfaction"]["reason"] == "unqualified_run"


# ---------------------------------------------------------------------------
# § 15 hook 4 — anti-vacuity sentinel on the record
# ---------------------------------------------------------------------------

def _two_runs_second_is_good(eng, ws, tmp_path, capsys):
    """run-a establishes the baseline; run-b is measured on every axis and good."""
    proxy = write_proxy(tmp_path / "read-set.txt", 4096)
    current = write_names(tmp_path / "current.txt", [])
    baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
    refs = tmp_path / "refs.md"
    refs.write_text("red-first evidence: check-a FAILED first, then green\n", encoding="utf-8")
    common = dict(names_current=current, names_baseline=baseline, collected=10,
                  declared_check=["check-a"], green_check=["check-a"],
                  red_first_refs=[str(refs)], proxy_paths=[str(proxy)], elapsed_ms=1000)
    run_cli(eng, determine_args(ws, run_id="run-a", **common), capsys)
    run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
    run_cli(eng, determine_args(ws, run_id="run-b", **common), capsys)
    run_cli(eng, settle_args(ws, run_id="run-b"), capsys)
    return record_of(ws, "run-b")


class TestAntiVacuitySentinelOnRecord:
    def test_clean_is_true_iff_findings_empty(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        assert record["change_point"]["clean"] is (record["change_point"]["findings"] == [])
        assert record["change_point"]["findings"] != [], (
            "anti-vacuity: an unmeasured run must not read as clean")

    def test_fully_measured_good_run_is_clean(self, eng, ws, tmp_path, capsys):
        record = _two_runs_second_is_good(eng, ws, tmp_path, capsys)
        assert record["change_point"]["clean"] is True
        assert record["change_point"]["findings"] == []
        assert record["passive_trigger"]["trigger_feedback"] is False
        assert record["passive_trigger"]["out_of_scope"] == []

    def test_a_clean_record_still_exists(self, eng, ws, tmp_path, capsys):
        record = _two_runs_second_is_good(eng, ws, tmp_path, capsys)
        assert record["kind"] == "speckit.run-determination"
        assert record["run_id"] == "run-b"
        assert record["settled_at"] is not None

    def test_change_point_id_derives_from_run_id(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-xyz"), capsys)
        assert only_record(ws)["change_point"]["id"] == "cp-run-xyz"

    def test_a_clean_run_is_never_padded_with_a_hollow_finding(self, eng, ws, tmp_path, capsys):
        record = _two_runs_second_is_good(eng, ws, tmp_path, capsys)
        assert record["change_point"]["findings"] == []
        assert "No significant" not in json.dumps(record)

    def test_settlement_recomputes_the_change_point(self, eng, ws, tmp_path, capsys):
        proxy = write_proxy(tmp_path / "read-set.txt", 4096)
        run_cli(eng, determine_args(ws, run_id="run-a", proxy_paths=[str(proxy)],
                                    elapsed_ms=1000), capsys)
        before = record_of(ws, "run-a")["change_point"]["findings"]
        assert any(f["axis"] == "satisfaction" for f in before)
        run_cli(eng, settle_args(ws, run_id="run-a", turn_class="session_end"), capsys)
        after = record_of(ws, "run-a")["change_point"]["findings"]
        assert not any(f["axis"] == "satisfaction" for f in after)


# ---------------------------------------------------------------------------
# § 15 hook 6 — 改点 / intervention.json separation
# ---------------------------------------------------------------------------

class TestChangePointLedgerSeparation:
    BANNLED = {"change", "targetFinding", "baselineRunId", "expectedSignal",
               "outcome", "disposition", "threshold", "packagePath"}

    def test_no_ledger_field_anywhere_in_the_record(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)

        def walk(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    assert key not in self.BANNLED, f"ledger field leaked: {key}"
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(only_record(ws))

    def test_finding_status_is_the_constant_observed(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        findings = only_record(ws)["change_point"]["findings"]
        assert findings, "anti-vacuity: this record must carry at least one finding"
        for finding in findings:
            assert finding["status"] == "observed"

    def test_finding_shape(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        finding = only_record(ws)["change_point"]["findings"][0]
        assert set(finding) == {"axis", "verdict", "reason", "observation",
                                "signal", "evidence_refs", "status"}
        assert set(finding["signal"]) == {"key", "direction"}

    def test_record_is_not_a_feedback_entry(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        feedback = ws / ".specify" / "memory" / "feedback"
        assert not feedback.exists() or list(feedback.glob("*.md")) == []

    def test_observations_describe_measurements_never_fixes(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        for finding in only_record(ws)["change_point"]["findings"]:
            text = finding["observation"].lower()
            assert 0 < len(finding["observation"]) <= 240
            for banned in ("should ", "must fix", "consider ", "建议", "应该", "refactor"):
                assert banned not in text, f"prescriptive finding: {banned}"


# ---------------------------------------------------------------------------
# § 10 — trigger derivation, passive non-exhaustiveness, the four red lines
# ---------------------------------------------------------------------------

class TestPassiveTrigger:
    def test_composition_flag_is_constant(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert only_record(ws)["passive_trigger"]["composes_with_should_prompt"] is True

    def test_trigger_formula_is_the_conjunction(self, eng):
        def axes(token, elapsed, correctness, satisfaction):
            return {"token_consumption": {"verdict": token},
                    "elapsed": {"verdict": elapsed},
                    "artifact_correctness": {"verdict": correctness},
                    "satisfaction": {"verdict": satisfaction}}

        assert eng.derive_trigger_feedback(
            "qualified", axes("regressed", "regressed", "ok", "accepted")) is True
        assert eng.derive_trigger_feedback(
            "qualified", axes("regressed", "unchanged", "ok", "accepted")) is False
        assert eng.derive_trigger_feedback(
            "qualified", axes("unchanged", "regressed", "ok", "accepted")) is False
        assert eng.derive_trigger_feedback(
            "qualified", axes("unchanged", "unchanged", "regressed", "accepted")) is True
        assert eng.derive_trigger_feedback(
            "qualified", axes("unchanged", "unchanged", "ok", "rejected")) is True
        assert eng.derive_trigger_feedback(
            "qualified", axes("regressed", "unchanged", "ok", "not_evaluated")) is False
        assert eng.derive_trigger_feedback(
            "qualified", axes("not_evaluated", "not_evaluated", "not_evaluated",
                              "not_evaluated")) is False
        assert eng.derive_trigger_feedback(
            "aborted", axes("regressed", "regressed", "regressed", "rejected")) is False

    def test_single_regressed_comparison_axis_does_not_trigger(self, eng, ws, tmp_path, capsys):
        """The deliberate asymmetry that replaces a tolerance band."""
        small = write_proxy(tmp_path / "small.txt", 1024)
        big = write_proxy(tmp_path / "big.txt", 8192)
        run_cli(eng, determine_args(ws, run_id="run-a", proxy_paths=[str(small)],
                                    elapsed_ms=1000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b", proxy_paths=[str(big)],
                                    elapsed_ms=1000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-b"), capsys)
        record = record_of(ws, "run-b")
        assert record["axes"]["token_consumption"]["verdict"] == "regressed"
        assert record["axes"]["elapsed"]["verdict"] == "unchanged"
        assert record["passive_trigger"]["trigger_feedback"] is False

    def test_both_comparison_axes_regressed_do_trigger(self, eng, ws, tmp_path, capsys):
        small = write_proxy(tmp_path / "small.txt", 1024)
        big = write_proxy(tmp_path / "big.txt", 8192)
        run_cli(eng, determine_args(ws, run_id="run-a", proxy_paths=[str(small)],
                                    elapsed_ms=1000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b", proxy_paths=[str(big)],
                                    elapsed_ms=9000), capsys)
        run_cli(eng, settle_args(ws, run_id="run-b"), capsys)
        assert record_of(ws, "run-b")["passive_trigger"]["trigger_feedback"] is True

    def test_out_of_scope_rows_are_recorded_not_acted_on(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        rows = only_record(ws)["passive_trigger"]["out_of_scope"]
        assert rows, "anti-vacuity: an unmeasured run must park its unevaluated axes"
        for row in rows:
            assert set(row) == {"observation", "parked_via", "ref"}
            assert row["parked_via"] in eng.PARKED_VIA
            assert row["parked_via"] == "none"
            assert row["ref"] is None

    def test_in_scope_is_only_an_evaluated_axis_of_this_unit(self, eng):
        assert eng.in_passive_scope({"axis": "token_consumption", "verdict": "regressed"},
                                    "/speckit.plan", "/speckit.plan") is True
        assert eng.in_passive_scope({"axis": "token_consumption", "verdict": "not_evaluated"},
                                    "/speckit.plan", "/speckit.plan") is False
        assert eng.in_passive_scope({"axis": "token_consumption", "verdict": "regressed"},
                                    "/speckit.plan", "skill:other") is False

    def test_validate_record_rejects_an_out_of_domain_carrier(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        assert eng.validate_record(record) == []
        record["passive_trigger"]["out_of_scope"][0]["parked_via"] = "email"
        problems = eng.validate_record(record)
        assert problems and any("parked_via" in p for p in problems)

    def test_validate_record_rejects_an_extra_out_of_scope_key(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["passive_trigger"]["out_of_scope"][0]["change"] = "edit the template"
        problems = eng.validate_record(record)
        assert problems and any("unexpected key set" in p for p in problems)

    def test_red_line_1_no_finding_targets_the_model_agent_or_user_code(self, eng, ws, tmp_path, capsys):
        session = write_session(tmp_path / "s.jsonl", [usage_row() for _ in range(3)])
        run_cli(eng, determine_args(ws, run_id="run-a", session_file=session,
                                    session_rows="0:2", tool="claude"), capsys)
        blob = json.dumps(only_record(ws)["change_point"]).lower()
        for banned in ("the llm", "agent cli", "user's project code", "claude is slow"):
            assert banned not in blob

    def test_red_line_3_engine_has_no_network_or_shell_path(self, engine_source):
        for marker in ("urllib", "http.client", "requests.", "socket.", "httpx", "ftplib"):
            assert marker not in engine_source, f"network marker found: {marker}"
        assert "shell=True" not in engine_source

    def test_never_solicit_no_interactive_surface(self, engine_source):
        for marker in ("readchar", "click.confirm", "typer.confirm", "sys.stdin.read"):
            assert marker not in engine_source


# ---------------------------------------------------------------------------
# § 15 hook 7 — no new store
# ---------------------------------------------------------------------------

class TestNoNewStore:
    def test_no_new_directory_appears_under_memory(self, eng, ws, capsys):
        before = {p.name for p in (ws / ".specify" / "memory").iterdir()}
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        after = {p.name for p in (ws / ".specify" / "memory").iterdir()}
        assert before == {"session"}
        assert after == before

    def test_the_engine_writes_through_the_memory_engine(self, engine_source):
        assert "memory-utils.py" in engine_source
        assert "action_record" in engine_source
        assert "action_reindex" in engine_source

    def test_record_lands_in_the_session_scope_with_the_declared_tags(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-tag"), capsys)
        entries = eng.sibling_engine("memory-utils.py").load_index(
            ws, "session")["entries"]
        assert len(entries) == 1
        entry = entries[0]
        assert entry["source"] == "/speckit.plan"
        assert "run-determination" in entry["tags"]
        assert "run-tag" in entry["tags"]

    def test_summary_frontmatter_carries_one_line(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        entries = eng.sibling_engine("memory-utils.py").load_index(
            ws, "session")["entries"]
        summary = entries[0]["summary"]
        assert "\n" not in summary
        assert "/speckit.plan" in summary
        for word in ("token", "elapsed", "artifact", "satisfaction"):
            assert word in summary, f"summary omits {word}: {summary!r}"

    def test_settle_creates_no_second_entry(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        entries = eng.sibling_engine("memory-utils.py").load_index(
            ws, "session")["entries"]
        assert len(entries) == 1
        assert entries[0]["summary"].count("not_evaluated") == 3


# ---------------------------------------------------------------------------
# § 15 hook 8/9 — OI-2 / OI-9 isolation, and the gate budget on engine source
# ---------------------------------------------------------------------------

class TestOI2PersistenceIsolation:
    """OI-2 (the record's durable landing point) is open and blocks S3, not S2.
    Option (a) — through ``memory-utils.py`` into ``.specify/memory/session/`` —
    sits behind one adapter seam so S3 can resolve it without touching the axes."""

    def test_the_adapter_seam_is_a_single_site(self, engine_source):
        assert "OI2_PERSISTENCE_ADAPTER" in engine_source
        assert "PERSISTENCE_ADAPTERS" in engine_source
        assert '"memory-utils-session"' in engine_source

    def test_swapping_the_adapter_does_not_touch_the_axes(self, eng, ws, capsys):
        calls = []
        original_name = eng.OI2_PERSISTENCE_ADAPTER
        original = eng.PERSISTENCE_ADAPTERS[original_name]

        def probe(root, record):
            calls.append(record["run_id"])
            return {"persisted": False, "reason": "probe-adapter"}

        eng.PERSISTENCE_ADAPTERS["probe"] = probe
        eng.OI2_PERSISTENCE_ADAPTER = "probe"
        try:
            rc, payload, _ = run_cli(eng, determine_args(ws, run_id="run-probe"), capsys)
        finally:
            eng.OI2_PERSISTENCE_ADAPTER = original_name
            eng.PERSISTENCE_ADAPTERS.pop("probe", None)

        assert rc == 0
        assert calls == ["run-probe"]
        assert payload["persistence"] == {"persisted": False, "reason": "probe-adapter"}
        assert set(payload["record"]["axes"]) == set(eng.AXES)
        assert original is not None
        assert [p.name for p in (ws / ".specify" / "memory" / "session").glob("*.md")] == []

    def test_custom_unit_reports_honestly_instead_of_dropping(self, eng, ws, capsys):
        """§ 3 admits ``custom:<owner>/<name>``, but the memory engine's enforced
        ``--source`` contract does not. The engine reports the gap rather than
        losing the record or silently widening a contract it does not own."""
        rc, payload, _ = run_cli(eng, determine_args(
            ws, unit_id="custom:team/reviewer", run_id="run-c"), capsys)
        assert rc == 0
        assert payload["persistence"]["persisted"] is False
        assert payload["persistence"]["reason"]
        assert payload["record"]["unit_type"] == "custom-unit"
        assert payload["record"]["unit_id"] == "custom:team/reviewer"


class TestOI9RedStateIsolation:
    """OI-9 (how ``unresolved_red`` is produced) is open and blocks S3's wiring
    text, not S2's code. Option (a) — caller declaration, the same shape as the
    existing ``--compliance-done`` precedent — sits behind one producer seam."""

    def test_the_producer_seam_is_a_single_site(self, engine_source):
        assert "OI9_RED_STATE_INPUT" in engine_source
        assert '"caller-declaration"' in engine_source

    def test_red_state_is_declared_never_inferred(self, engine_source):
        assert "telemetry" not in engine_source
        assert "trigger-utils" not in engine_source

    def test_undeclared_accepts_are_separately_countable(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", unresolved_red="unknown"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b", unresolved_red="false"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-b"), capsys)
        rc, payload, _ = run_cli(eng, history_args(ws), capsys)
        assert rc == 0
        assert payload["counts"]["red_state_undeclared_accepts"] == 1
        assert payload["counts"]["derived_accepts"] == 1


class TestGateBudgetOnEngineSource:
    """``scripts/python/`` is outside the scanner's SCAN_DIRS, but S3/S4 quote this
    engine from scanned surfaces and the budget has zero margin."""

    def test_engine_source_adds_no_blocking_pattern(self, engine_source):
        scanner = FRAMEWORK_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
        spec = importlib.util.spec_from_file_location("_gate_scanner_probe", scanner)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        assert module.BLOCKING_RE.findall(engine_source) == []

    def test_retired_naming_forms_do_not_appear(self, engine_source):
        """Drift guard for the retired forms named by
        ``.specify/memory/glossary.md`` → `运行判定` (naming-history owner).

        The two literals below appear in this file ONLY as guard copies in the
        sense ``shared/guidelines/one-source-of-truth.md`` § Legitimate duplicates
        allows: they exist in order to fail when the retired forms re-enter the
        engine. Note that one of them is ordinary vocabulary elsewhere in this
        repository (contract-test contexts, Feature 053's subject matter), so the
        guard is scoped to this engine's source and deliberately not repo-wide.
        """
        for retired in ("断言", "判断逻辑"):
            assert retired not in engine_source

    def test_the_mechanism_name_is_the_ratified_one(self, engine_source):
        assert "运行判定" in engine_source
        assert "Run Determination" in engine_source


# ---------------------------------------------------------------------------
# § 6 — the three lanes and their Summary-First projections
# ---------------------------------------------------------------------------

class TestLaneProjections:
    def test_lane_3_projection_is_an_allowlist(self, eng):
        findings = {
            "schemaVersion": 1, "kind": "speckit.evidence-findings",
            "target": "/speckit.plan", "runId": "ev-1",
            "lanes": {"session": {"status": "available"}},
            "evidence": [{"id": "ev-001", "lane": "session", "evidenceState": "Present",
                          "summary": "one line", "signals": {"token_consumption": "reduce"},
                          "evidenceRefs": ["/some/body.md"], "privacyNote": "redacted"}],
            "findingsDigest": "sha256:abc",
        }
        projected = eng.project_findings(findings)
        assert projected["findingsDigest"] == "sha256:abc"
        assert projected["evidence"] == [{"id": "ev-001", "lane": "session",
                                          "evidenceState": "Present", "summary": "one line",
                                          "signals": {"token_consumption": "reduce"}}]
        blob = json.dumps(projected)
        for excluded in ("evidenceRefs", "privacyNote", "lanes", "manifest", "schemaVersion"):
            assert excluded not in blob

    def test_projection_allowlist_is_declared_in_source(self, engine_source):
        assert "FINDINGS_PROJECTION_FIELDS" in engine_source
        for field in ("id", "lane", "evidenceState", "summary", "signals"):
            assert f'"{field}"' in engine_source

    def _evidence_ws(self, ws, days_ago=0, digest="sha256:deadbeef"):
        run_id = "ev-20261006-000000-plan"
        run_dir = ws / ".specify" / "memory" / "evidence" / run_id
        run_dir.mkdir(parents=True)
        created = (datetime.now(timezone.utc)
                   - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
        findings = {"schemaVersion": 1, "kind": "speckit.evidence-findings",
                    "target": "/speckit.plan", "runId": run_id,
                    "lanes": {}, "evidence": [], "findingsDigest": digest}
        (run_dir / "findings.json").write_text(json.dumps(findings), encoding="utf-8")
        index = {"entries": [{"runId": run_id, "target": "/speckit.plan",
                              "created": created, "lanesSummary": {},
                              "file": f"{run_id}/findings.json"}]}
        (ws / ".specify" / "memory" / "evidence" / "index.json").write_text(
            json.dumps(index), encoding="utf-8")
        return run_id, digest

    def test_fresh_evidence_run_is_consumed_and_its_digest_recorded(self, eng, ws, capsys):
        _, digest = self._evidence_ws(ws)
        rc, _, _ = run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert rc == 0
        provenance = only_record(ws)["provenance"]
        assert provenance["lanes_read"]["evidence"] == "available"
        assert provenance["evidence_digests"] == [digest]

    def test_stale_evidence_run_is_not_consumed_silently(self, eng, ws, capsys):
        _, digest = self._evidence_ws(ws, days_ago=365)
        rc, _, _ = run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert rc == 0
        provenance = only_record(ws)["provenance"]
        assert provenance["lanes_read"]["evidence"] == "stale"
        assert provenance["evidence_digests"] == []
        assert digest not in json.dumps(provenance)

    def test_absent_evidence_lane_is_unavailable(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert only_record(ws)["provenance"]["lanes_read"]["evidence"] == "unavailable"

    def test_lane_2_is_in_context_with_zero_additional_reads(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert only_record(ws)["provenance"]["lanes_read"]["user_input"] == "in_context"

    def test_lane_1_availability_is_probed(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        assert only_record(ws)["provenance"]["lanes_read"]["session"] == "available"

    def test_history_returns_a_projection_never_record_bodies(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", token_note="a secret note"), capsys)
        rc, payload, _ = run_cli(eng, history_args(ws), capsys)
        assert rc == 0
        assert len(payload["records"]) == 1
        row = payload["records"][0]
        assert set(row) <= {"unit_id", "run_id", "determined_at", "settled_at",
                            "complexity", "qualification", "axes", "change_point",
                            "passive_trigger", "provenance"}
        for axis, body in row["axes"].items():
            assert set(body) == {"verdict", "reason", "signal"}, axis
        assert set(row["provenance"]) == {"declared_by_caller"}
        blob = json.dumps(row)
        assert "measurement" not in blob
        assert "a secret note" not in blob

    def test_history_unsettled_filter(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, run_id="run-b"), capsys)
        run_cli(eng, settle_args(ws, run_id="run-a"), capsys)
        rc, payload, _ = run_cli(eng, history_args(ws, "--unsettled"), capsys)
        assert rc == 0
        assert [r["run_id"] for r in payload["records"]] == ["run-b"]
        assert payload["counts"]["unsettled"] == 1
        assert payload["counts"]["total"] == 1

    def test_history_requires_a_target(self, eng, ws, capsys):
        rc, _, _ = run_cli(eng, ["--action", "history", "--workspace-root", str(ws)], capsys)
        assert rc == 2

    def test_history_ignores_other_units(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, unit_id="/speckit.plan", run_id="run-a"), capsys)
        run_cli(eng, determine_args(ws, unit_id="skill:study-project", run_id="run-b"), capsys)
        rc, payload, _ = run_cli(eng, history_args(ws), capsys)
        assert rc == 0
        assert [r["run_id"] for r in payload["records"]] == ["run-a"]

    def test_history_skips_entries_that_are_not_determinations(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        session = ws / ".specify" / "memory" / "session"
        # req 055: the scan picks this junk entry up by itself — no index to
        # patch; history must skip it via body parsing.
        (session / "junk.md").write_text(
            "---\nid: junk\nsource: \"/speckit.plan\"\ntags: [\"run-determination\"]\n"
            "---\n\nnot a determination record\n", encoding="utf-8")
        rc, payload, _ = run_cli(eng, history_args(ws), capsys)
        assert rc == 0
        assert [r["run_id"] for r in payload["records"]] == ["run-a"]


# ---------------------------------------------------------------------------
# § 7 — record schema rules and provenance
# ---------------------------------------------------------------------------

class TestRecordSchema:
    def test_top_level_key_set(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        assert set(record) == {
            "kind", "schema_version", "unit_id", "unit_type", "run_id", "feature",
            "feature_id", "determined_at", "settled_at", "complexity", "qualification",
            "axes", "change_point", "passive_trigger", "provenance"}
        assert record["kind"] == "speckit.run-determination"
        assert record["schema_version"] == 1
        assert record["complexity"] == "complex"
        assert record["qualification"] == "qualified"

    def test_feature_and_feature_id_are_distinct_number_spaces(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a", feature="038-goal-target",
                                    feature_id="041"), capsys)
        record = only_record(ws)
        assert record["feature"] == "038-goal-target"
        assert record["feature_id"] == "041"

    def test_determined_at_is_utc_iso8601(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        value = only_record(ws)["determined_at"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value)

    def test_provenance_shape(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        provenance = only_record(ws)["provenance"]
        assert set(provenance) >= {"engine", "declared_by_caller", "lanes_read",
                                   "evidence_digests", "honesty_boundary"}
        assert provenance["engine"] == "scripts/python/run-determination.py"
        for declared in ("complexity", "qualification", "user_turn_class", "unresolved_red"):
            assert declared in provenance["declared_by_caller"]
        assert set(provenance["lanes_read"]) == {"session", "user_input", "evidence"}
        assert len(provenance["honesty_boundary"]) == 2

    def test_validate_record_rejects_a_dropped_axis(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        assert eng.validate_record(record) == []
        del record["axes"]["elapsed"]
        problems = eng.validate_record(record)
        assert problems and any("elapsed" in p for p in problems)

    def test_validate_record_rejects_a_null_axis(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["axes"]["elapsed"] = None
        assert eng.validate_record(record) != []

    def test_validate_record_rejects_reason_verdict_mismatch(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["axes"]["token_consumption"]["reason"] = "no_baseline"
        record["axes"]["token_consumption"]["verdict"] = "unchanged"
        assert eng.validate_record(record) != []

    def test_validate_record_rejects_an_out_of_domain_verdict(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["axes"]["token_consumption"]["verdict"] = "ok"
        assert eng.validate_record(record) != []

    def test_validate_record_rejects_clean_findings_mismatch(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["change_point"]["clean"] = True
        assert eng.validate_record(record) != []

    def test_validate_record_rejects_a_non_constant_status(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["change_point"]["findings"][0]["status"] = "planned"
        assert eng.validate_record(record) != []

    def test_closed_source_hierarchies_are_pinned(self, eng):
        assert eng.TOKEN_SOURCES == ("tool_session_usage", "line_byte_proxy", "unavailable")
        assert eng.ELAPSED_SOURCES == ("tool_session_timestamps", "caller_declared_ms",
                                       "unavailable")
        assert eng.DIRECTIONS == ("improve", "reduce")
        assert eng.FAILED_DIFF_STATUSES == ("empty", "non_empty", "not_evaluated")
        assert eng.GREEN_EVIDENCE_STATUSES == ("complete", "partial", "absent",
                                               "not_evaluated")

    def test_validate_record_rejects_an_out_of_hierarchy_source(self, eng, ws, capsys):
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        record["axes"]["token_consumption"]["measurement"]["source"] = "model_estimate"
        assert eng.validate_record(record) != []

    def test_validate_record_rejects_a_value_under_an_unavailable_source(self, eng, ws, capsys):
        """The engine polices its own honesty rule: an unavailable source carries
        no measured value at all, so a fabricated zero cannot be persisted."""
        run_cli(eng, determine_args(ws, run_id="run-a"), capsys)
        record = only_record(ws)
        assert eng.validate_record(record) == []
        record["axes"]["elapsed"]["measurement"]["ms"] = 0
        problems = eng.validate_record(record)
        assert problems and any("fabricated zero" in p for p in problems)

    def test_validate_record_rejects_ok_without_complete_green_evidence(self, eng, ws, tmp_path, capsys):
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        refs = tmp_path / "refs.md"
        refs.write_text("check-a red-first\n", encoding="utf-8")
        run_cli(eng, determine_args(ws, run_id="run-a", names_current=current,
                                    names_baseline=baseline, collected=4,
                                    declared_check=["check-a"], green_check=["check-a"],
                                    red_first_refs=[str(refs)]), capsys)
        record = only_record(ws)
        assert record["axes"]["artifact_correctness"]["verdict"] == "ok"
        record["axes"]["artifact_correctness"]["green_evidence"]["status"] = "partial"
        assert eng.validate_record(record) != []

    def test_evidence_refs_are_paths_only(self, eng, ws, tmp_path, capsys):
        refs = tmp_path / "refs.md"
        refs.write_text("check-a red-first\n", encoding="utf-8")
        current = write_names(tmp_path / "current.txt", [])
        baseline = write_names(tmp_path / "baseline.txt", ["tests/a.py::test_old"])
        run_cli(eng, determine_args(ws, run_id="run-a", names_current=current,
                                    names_baseline=baseline, collected=3,
                                    declared_check=["check-a"], green_check=["check-a"],
                                    red_first_refs=[str(refs)]), capsys)
        record = only_record(ws)
        refs_list = record["axes"]["artifact_correctness"]["evidence_refs"]
        assert refs_list and all(isinstance(r, str) for r in refs_list)
        assert all("\n" not in r and len(r) < 400 for r in refs_list)
        assert record["change_point"]["findings"]


# ---------------------------------------------------------------------------
# § 1 — hard separation from 情境评估 (proactive-trigger)
# ---------------------------------------------------------------------------

class TestSeparationFromSituationalAssessment:
    def test_engine_never_writes_a_per_turn_row_or_calls_assess(self, engine_source):
        assert "trigger-utils" not in engine_source
        assert '"assess"' not in engine_source
        assert "turnId" not in engine_source

    def test_engine_adds_no_situation_vocabulary(self, engine_source):
        assert "situations" not in engine_source
        assert "promotion" not in engine_source

    def test_engine_does_not_redefine_a_sibling_action(self, engine_source):
        assert "def action_record" not in engine_source
        assert "def action_reindex" not in engine_source
        assert "def action_latest" not in engine_source
        assert "def load_run" not in engine_source

    def test_engine_does_not_write_the_mirror_by_hand(self, engine_source):
        assert "sync-mirrors" not in engine_source
        assert ".specify/scripts" not in engine_source
