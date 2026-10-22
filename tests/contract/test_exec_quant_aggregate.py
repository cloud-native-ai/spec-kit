"""Contract tests for the exec-quant aggregate action (Feature 068, US3).

Owns ``.specify/specs/068-exec-quant-feedback-channel/contracts/aggregate-contract.md``
C-18..C-23: the ``--action aggregate`` registration (``ACTIONS`` tuple +
``ARG_MANIFEST`` via the existing args-manifest mechanism — the argparse parser
stays the single source of truth for flags), the consumption face
(``aggregated/**/records/*.json`` envelopes only — local ``records/`` and
``scores/`` MUST NOT enter the view), the E7 view projection
(sources[]/units/quality/coverage/record_files + totals + store_digest), the
D8 field-shape normalization, zero fabrication (every number replayable from
the ``record_files`` roster), the append-only ``aggregated/summaries/``
products isomorphic with stdout, rerun safety, and the C-23 explicit-action
boundary.

Subject = the framework source ``scripts/python/exec-quant.py`` (loaded via
``tests/script_api.py``'s loader; never the ``.specify/`` mirror). CLI behavior
runs through the engine's real command line (subprocess), consistent with
``test_exec_quant_engine.py``.

Red-first evidence: notes/red-first-evidence.md (§ part 4a / T016).

Implement-side pins this file fixes for 4b (each traceable to recorded text):
- ``skipped_unreadable`` surfaces as a top-level int on the view (C-19 requires
  the count observable; E7's table is a required-field floor — same
  subset-not-closed reading as the intake action's flat counters, C-16).
- Coverage is the total of the per-source quality distribution (D8: "quality
  各字段 evaluated/not_evaluated 分布 … coverage 汇总") — replayable without a
  hardcoded field vocabulary (CHK025 residue is resolved shape-based, see
  ``test_quality_shape_normalization``).
- The empty-store 0/0 ratio form is NOT pinned (CHK027 explicitly undefined);
  the numeric zero-fabrication guard in ``test_totals_and_store_digest…``
  still forbids any fabricated percentage for the empty denominator.
- Unknown-field normalization follows the shape rule uniformly (a future
  field carrying a proper ``{"value", "provenance"}`` object counts as
  evaluated; any unforeseen form counts as not_evaluated) — the only reading
  consistent with the record law (two legal shapes only), FR-013 (hiding a
  measured value would distort the coverage rate) and C-20's 零硬编码 (a
  name-allowlist would be hard-coding). The strict alternative (unknown NAME
  always not_evaluated) would need a hardcoded vocabulary and is rejected.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.script_api import _load_module

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "exec-quant.py"

#: Loaded from the framework source via tests/script_api.py's loader — the
#: module-level registry face under test (never the .specify/ mirror).
EQ = _load_module("exec_quant_aggregate_contract", "exec-quant.py")

VIEW_KIND = "speckit.exec-quant-aggregate-view"  # data-model § E7
ENVELOPE_KIND = "speckit.exec-quant-aggregated"  # data-model § E6
NOT_EVALUATED = "not_evaluated"  # [[STR-002]] (requirements § Shared Strings)
SCHEMA_VERSION = 1  # data-model § E7

#: entry_filename() form (timestamp with microseconds + 8-hex uuid suffix).
ENTRY_NAME_FORM = re.compile(r"^\d{8}T\d{6}\d{6}Z-[0-9a-f]{8}\.json$")

E7_TOP_KEYS = {"kind", "schema_version", "generated_at", "sources", "totals",
               "store_digest"}
E7_SOURCE_KEYS = {"project", "identity_status", "record_count", "units",
                  "quality", "coverage", "record_files"}


# --------------------------------------------------------------------------- #
# fixture helpers (self-constructed aggregated stores)
# --------------------------------------------------------------------------- #
def _hex(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def _agg(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant" / "aggregated"


def _summaries(ws: Path) -> Path:
    return _agg(ws) / "summaries"


def _envelope(source_project: str, identity_status: str, unit_id: str,
              run_id: str, quality: dict, *, unit_type: str = "command",
              collected_at: str = "2026-01-01T00:00:00Z",
              identity_key: str | None = None,
              name: str | None = None) -> tuple[str, dict]:
    """One E6 envelope; returns (filename, envelope). The aggregation face is
    built exactly as the intake leg writes it (data-model § E6)."""
    envelope = {
        "aggregation_envelope": {
            "schema_version": 1,
            "kind": ENVELOPE_KIND,
            "source_project": source_project,
            "source_commit": None,
            "identity_status": identity_status,
            "identity_key": identity_key or _hex(f"{source_project}|{unit_id}|{run_id}"),
            "content_hash": _hex(f"content|{unit_id}|{run_id}"),
            "package_file": "feedback-2026.zip",
            "ingested_at": "2026-01-02T00:00:00Z",
        },
        "record": {
            "kind": "speckit.exec-quant",  # [[STR-001]]
            "schema_version": 2,
            "unit_id": unit_id,
            "unit_type": unit_type,
            "run_id": run_id,
            "collected_at": collected_at,
            "quality": quality,
        },
    }
    return (name or f"20260102T000000Z-{_hex(unit_id + run_id)[:8]}.json",
            envelope)


def _write_envelope(ws: Path, group_slug: str, filename: str,
                    envelope: dict) -> Path:
    target = _agg(ws) / group_slug / "records" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(envelope, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    return target


def _alpha_envelopes() -> list[tuple[str, str, dict]]:
    """Three envelopes for one source project with mixed D8 field shapes:
    a measured object, the bare [[STR-002]] literal, a field missing from a
    sibling record, an unknown new field in bare form, and an unforeseen
    value form (never guessed)."""
    out = []
    out.append(_envelope(
        "customer-alpha", "identified", "/speckit.plan", "r1",
        {"elapsed_ms": {"value": 1200, "provenance": "carried"},
         "tokens": NOT_EVALUATED},  # satisfaction missing entirely
        name="20260102T000001Z-aaaa0001.json"))
    out.append(_envelope(
        "customer-alpha", "identified", "/speckit.implement", "r2",
        {"elapsed_ms": NOT_EVALUATED,
         "tokens": {"value": 42, "provenance": "measured"}},
        name="20260102T000002Z-aaaa0002.json"))
    out.append(_envelope(
        "customer-alpha", "identified", "/speckit.plan", "r3",
        {"elapsed_ms": {"value": 900, "provenance": "carried"},
         "brand_new_axis": NOT_EVALUATED,       # unknown field, bare form
         "odd_future_form": "raw-unforeseen"},  # unknown form: never guessed
        name="20260102T000003Z-aaaa0003.json"))
    return out


def _seed_store(ws: Path) -> None:
    """Aggregated layer with two source projects (three + one envelopes)."""
    for filename, envelope in _alpha_envelopes():
        _write_envelope(ws, "customer-alpha-deadbeef", filename, envelope)
    beta_name, beta_env = _envelope(
        "customer-beta", "identified", "/speckit.review", "r9",
        {"elapsed_ms": NOT_EVALUATED, "tokens": NOT_EVALUATED},
        name="20260102T000004Z-beef0004.json")
    _write_envelope(ws, "customer-beta-cafebabe", beta_name, beta_env)


def _run(ws: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), "--action", "aggregate",
         "--workspace-root", str(ws), *flags],
        capture_output=True, text=True, timeout=120)


def _run_json(ws: Path, *flags: str) -> tuple[dict, subprocess.CompletedProcess]:
    proc = _run(ws, *flags)
    assert proc.stdout.strip(), f"no stdout JSON (rc={proc.returncode}): {proc.stderr}"
    return json.loads(proc.stdout), proc


def _products(ws: Path) -> list[Path]:
    summaries = _summaries(ws)
    return sorted(summaries.glob("*.json")) if summaries.is_dir() else []


def _shape_evaluates(value: object) -> bool:
    """D8 shape rule: a ``{"value", "provenance"}`` object measures; the bare
    [[STR-002]] literal, a missing key and any unforeseen form do not —
    nothing is ever guessed."""
    return isinstance(value, dict) and "value" in value


def _replay(envelopes: list[dict]) -> dict:
    """Independent replay oracle (FR-011 / C-20): recompute record_count,
    units, quality and coverage from a list of envelope dicts. The field
    universe is the union of observed keys — zero hard-coding; a key missing
    from one record counts as not_evaluated for that record."""
    per_record: list[dict] = []
    field_names: set[str] = set()
    units: dict[str, int] = {}
    for env in envelopes:
        record = env["record"]
        unit_id = str(record.get("unit_id", ""))
        units[unit_id] = units.get(unit_id, 0) + 1
        quality = record.get("quality")
        quality = quality if isinstance(quality, dict) else {}
        per_record.append(quality)
        field_names.update(quality)
    projected: dict[str, dict[str, int]] = {}
    for field in sorted(field_names):
        evaluated = not_evaluated = 0
        for quality in per_record:
            if _shape_evaluates(quality.get(field)):
                evaluated += 1
            else:  # bare [[STR-002]], missing key, unforeseen form
                not_evaluated += 1
        projected[field] = {"evaluated": evaluated,
                            "not_evaluated": not_evaluated}
    coverage = {
        "not_evaluated_total": sum(c["not_evaluated"] for c in projected.values()),
        "evaluated_total": sum(c["evaluated"] for c in projected.values()),
    }
    return {"record_count": len(envelopes), "units": units,
            "quality": projected, "coverage": coverage}


def _source_of(view: dict, project: str) -> dict:
    matches = [s for s in view["sources"] if s["project"] == project]
    assert len(matches) == 1, f"expected exactly one group for {project!r}"
    return matches[0]


def _envelopes_by_name(ws: Path) -> dict[str, dict]:
    """Read back every aggregated envelope on disk, keyed by bare filename."""
    out: dict[str, dict] = {}
    for path in _agg(ws).glob("*/records/*.json"):
        out[path.name] = json.loads(path.read_text(encoding="utf-8"))
    return out


def _replay_source(ws: Path, source: dict) -> None:
    """Replay one sources[] entry digit-by-digit from the envelope files its
    own record_files roster names (FR-011: 任一数字可由名单重放核对)."""
    envelopes = _envelopes_by_name(ws)
    roster = [envelopes[name] for name in source["record_files"]]
    expected = _replay(roster)
    assert source["record_count"] == expected["record_count"]
    assert source["units"] == expected["units"]
    assert source["quality"] == expected["quality"]
    assert source["coverage"] == expected["coverage"]


def _snapshot(ws: Path) -> dict[str, bytes]:
    return {str(p.relative_to(ws)): p.read_bytes()
            for p in sorted(ws.rglob("*")) if p.is_file()}


# --------------------------------------------------------------------------- #
# C-18: action registration and signature
# --------------------------------------------------------------------------- #
def test_subject_is_framework_source_engine():
    # The subject is the framework source, never the .specify/ mirror: the
    # loaded module must originate under scripts/python/exec-quant.py.
    origin = getattr(EQ, "__file__", "") or ""
    assert Path(origin) == ENGINE


def test_action_registered_in_actions_and_arg_manifest():
    # C-18: aggregate joins the registry; pre-existing actions stay untouched.
    assert "aggregate" in EQ.ACTIONS
    assert "aggregate" in EQ.ARG_MANIFEST
    for legacy in ("collect", "list-records", "score", "collect-dispatch",
                   "args-manifest"):
        assert legacy in EQ.ACTIONS


def test_args_manifest_covers_aggregate_flags():
    # C-18: the existing `--action args-manifest` contract covers the new
    # action automatically — zero new validators; every declared flag must be
    # a live option of the engine's own parser (the parser is the single
    # source of truth).
    view = EQ.build_parser()
    live = {opt for act in view._actions for opt in act.option_strings}
    spec = EQ.ARG_MANIFEST["aggregate"]
    assert spec["required"] == []  # C-18: zero new required parameters
    declared = set(spec["required"]) | set(spec["source"])
    assert declared <= live, f"undeclared flags: {sorted(declared - live)}"


def test_aggregate_accepts_workspace_root_and_format_flags(tmp_path):
    # C-18: `--workspace-root` (existing) + `--format {text,json}` are
    # accepted; the action is registered (never "invalid choice").
    proc = _run(tmp_path, "--format", "json")
    assert "invalid choice" not in proc.stderr
    assert proc.returncode == 0


def test_format_defaults_to_json(tmp_path):
    # C-18: without --format the machine face is JSON (list-records keeps its
    # own text default; aggregate's default is json by contract).
    _seed_store(tmp_path)
    view, proc = _run_json(tmp_path)
    assert proc.returncode == 0
    assert view["kind"] == VIEW_KIND  # a parsed E7 view, not a text listing


def test_format_text_face_runs(tmp_path):
    # C-18: the --format {text,json} flag form exists and the text face runs.
    _seed_store(tmp_path)
    proc = _run(tmp_path, "--format", "text")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip()


# --------------------------------------------------------------------------- #
# C-19: consumption face
# --------------------------------------------------------------------------- #
def test_consumes_aggregated_envelopes_grouped_by_source_project(tmp_path):
    _seed_store(tmp_path)
    view, proc = _run_json(tmp_path)
    assert proc.returncode == 0
    projects = sorted(s["project"] for s in view["sources"])
    assert projects == ["customer-alpha", "customer-beta"]
    alpha = _source_of(view, "customer-alpha")
    assert alpha["identity_status"] == "identified"
    assert alpha["record_count"] == 3
    beta = _source_of(view, "customer-beta")
    assert beta["record_count"] == 1
    # each roster names exactly the envelopes that were written for the group
    on_disk = _envelopes_by_name(tmp_path)
    for source in view["sources"]:
        assert set(source["record_files"]) <= set(on_disk)
        assert len(source["record_files"]) == source["record_count"]


def test_same_source_project_across_slug_dirs_merges(tmp_path):
    # C-19/C-20: the view groups by envelope source_project — two slug
    # directories carrying the same project identity present as ONE source
    # group (zero special-casing on directory names).
    _seed_store(tmp_path)
    name, envelope = _envelope(
        "customer-alpha", "identified", "/speckit.tasks", "r7",
        {"elapsed_ms": {"value": 5, "provenance": "measured"}},
        name="20260102T000005Z-aaaa0005.json")
    _write_envelope(tmp_path, "customer-alpha-12345678", name, envelope)

    view, _ = _run_json(tmp_path)

    alpha = _source_of(view, "customer-alpha")
    assert alpha["record_count"] == 4
    assert alpha["units"] == {"/speckit.plan": 2, "/speckit.implement": 1,
                              "/speckit.tasks": 1}
    assert len(alpha["record_files"]) == 4
    _replay_source(tmp_path, alpha)


def test_local_records_and_scores_never_enter_view(tmp_path):
    # C-19 negative: the consumption face is aggregated/**/records/*.json
    # ONLY — local records/ and scores/ (no source attribution in the US3
    # context) never reach the view.
    ws = tmp_path
    _seed_store(ws)
    store = ws / ".specify" / "memory" / "exec-quant"
    local_unit = "custom:local/private-probe"
    for name, body in (
        ("20260101T000010Z-local001.json", {
            "kind": "speckit.exec-quant", "schema_version": 2,
            "unit_id": local_unit, "unit_type": "custom-unit", "run_id": "l1",
            "collected_at": "2026-01-01T00:00:00Z"}),
        ("20260101T000011Z-local002.json", {
            "kind": "speckit.exec-quant", "schema_version": 2,
            "unit_id": "custom:local/second-probe", "unit_type": "custom-unit",
            "run_id": "l2", "collected_at": "2026-01-01T00:00:00Z"}),
    ):
        target = store / "records" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(body), encoding="utf-8")
    scores = store / "scores" / "20260101T000012Z-score001.json"
    scores.parent.mkdir(parents=True, exist_ok=True)
    scores.write_text(json.dumps({
        "kind": "speckit.exec-quant", "entry_type": "score",
        "unit_id": "custom:local/score-only", "run_id": "s1", "score": 3}),
        encoding="utf-8")

    view, proc = _run_json(ws)

    assert proc.returncode == 0
    assert view["totals"]["record_count"] == 4  # aggregated envelopes only
    dump = json.dumps(view, ensure_ascii=False)
    assert local_unit not in dump
    assert "private-probe" not in dump and "score-only" not in dump
    assert "second-probe" not in dump
    for source in view["sources"]:
        assert all("/records/" not in n and "/scores/" not in n
                   for n in source["record_files"])


def test_unreadable_envelopes_counted_non_blocking(tmp_path):
    # C-19: a non-dict envelope and a dict missing the `record` key count as
    # skipped_unreadable and never block the action.
    ws = tmp_path
    _seed_store(ws)
    group = _agg(ws) / "customer-alpha-deadbeef" / "records"
    (group / "20260102T000006Z-bad00001.json").write_text(
        "[1, 2, 3]", encoding="utf-8")  # valid JSON, not a dict
    (group / "20260102T000007Z-bad00002.json").write_text(
        json.dumps({"aggregation_envelope": {"source_project": "x"}}),
        encoding="utf-8")  # dict, missing `record`

    view, proc = _run_json(ws)

    assert proc.returncode == 0  # degradation is non-blocking
    assert view["skipped_unreadable"] == 2
    assert _source_of(view, "customer-alpha")["record_count"] == 3


def test_own_repo_source_has_same_rights(tmp_path):
    # C-19: this very repository as a source project is presented like any
    # other source — grouping by envelope source_project, zero special-casing.
    ws = tmp_path
    instructions = REPO_ROOT / ".specify" / "instructions.md"
    match = re.search(r"^\s*(?:-\s*)?\*\*Project Name\*\*:\s*(.+?)\s*$",
                      instructions.read_text(encoding="utf-8"), re.M)
    own_name = match.group(1).strip()
    assert own_name  # the repo does declare a project name
    name, envelope = _envelope(
        own_name, "identified", "/speckit.implement", "own-1",
        {"elapsed_ms": {"value": 3, "provenance": "measured"}})
    _write_envelope(ws, "own-repo-slug-00000001", name, envelope)
    _seed_store(ws)

    view, proc = _run_json(ws)

    assert proc.returncode == 0
    own = _source_of(view, own_name)  # first-class group, full projection
    assert own["record_count"] == 1
    assert own["units"] == {"/speckit.implement": 1}
    _replay_source(ws, own)


# --------------------------------------------------------------------------- #
# C-20: view projection (data-model § E7)
# --------------------------------------------------------------------------- #
def test_view_projection_field_set_e7(tmp_path):
    _seed_store(tmp_path)
    view, proc = _run_json(tmp_path)
    assert proc.returncode == 0
    # E7 required field floor (+ skipped_unreadable, see module docstring)
    assert E7_TOP_KEYS <= set(view)
    assert isinstance(view["skipped_unreadable"], int)
    assert view["kind"] == VIEW_KIND
    assert view["schema_version"] == SCHEMA_VERSION
    generated = view["generated_at"]
    assert isinstance(generated, str) and generated.endswith("Z")
    assert EQ._parse_iso(generated) is not None  # ISO-8601 Z
    for source in view["sources"]:
        assert E7_SOURCE_KEYS <= set(source)
        assert isinstance(source["record_count"], int)
        assert isinstance(source["units"], dict)
        assert isinstance(source["quality"], dict)
        assert set(source["coverage"]) == {"not_evaluated_total",
                                           "evaluated_total"}
        assert isinstance(source["record_files"], list)
    assert set(view["store_digest"]) == {"record_files_total",
                                         "identity_keys_total"}


def test_quality_shape_normalization(tmp_path):
    # C-20 / D8: {value, provenance} → evaluated; bare [[STR-002]], a missing
    # key and any unforeseen form → not_evaluated; unknown NEW fields surface
    # data-driven (zero hard-coded vocabulary) and are never guessed.
    ws = tmp_path
    _seed_store(ws)

    view, _ = _run_json(ws)

    alpha = _source_of(view, "customer-alpha")
    _replay_source(ws, alpha)  # full digit-by-digit replay of the projection
    quality = alpha["quality"]
    assert quality["elapsed_ms"] == {"evaluated": 2, "not_evaluated": 1}
    assert quality["tokens"] == {"evaluated": 1, "not_evaluated": 2}
    # a field missing from two sibling records still counts not_evaluated
    assert quality["brand_new_axis"] == {"evaluated": 0, "not_evaluated": 1}
    # an unforeseen value form is never evaluated
    assert quality["odd_future_form"] == {"evaluated": 0, "not_evaluated": 1}


def test_unknown_field_with_measured_shape_is_shape_evaluated(tmp_path):
    # D8 reading disclosed in the module docstring: the shape rule applies
    # uniformly — a future field carrying a proper {"value", "provenance"}
    # object counts as evaluated with zero hard-coding.
    ws = tmp_path
    name, envelope = _envelope(
        "customer-gamma", "identified", "/speckit.review", "r-g",
        {"future_metric": {"value": 7, "provenance": "measured"}})
    _write_envelope(ws, "customer-gamma-11111111", name, envelope)

    view, _ = _run_json(ws)

    gamma = _source_of(view, "customer-gamma")
    assert gamma["quality"]["future_metric"] == {"evaluated": 1,
                                                 "not_evaluated": 0}


def test_coverage_is_quality_distribution_total(tmp_path):
    # D8: coverage 汇总 = the total of the per-source quality distribution —
    # replayable with no field vocabulary of its own.
    ws = tmp_path
    _seed_store(ws)

    view, _ = _run_json(ws)

    for source in view["sources"]:
        _replay_source(ws, source)  # pins coverage == Σ quality counts
        evaluated = sum(f["evaluated"] for f in source["quality"].values())
        not_evaluated = sum(f["not_evaluated"]
                            for f in source["quality"].values())
        assert source["coverage"] == {"not_evaluated_total": not_evaluated,
                                      "evaluated_total": evaluated}


def test_totals_and_store_digest_replayable(tmp_path):
    # C-20/C-21: global counts + a not-evaluated ratio in totals; both digest
    # counters replay from the store; the ratio never fabricates a number
    # outside the replayable value set (CHK027's 0/0 denominator included).
    ws = tmp_path
    _seed_store(ws)
    # one duplicate identity_key across two groups (re-attributed duplicate):
    # identity_keys_total counts DISTINCT keys, not files.
    dup_name, dup_env = _envelope(
        "customer-beta", "identified", "/speckit.plan", "r1",
        {"elapsed_ms": {"value": 1, "provenance": "carried"}},
        identity_key=_hex("customer-alpha|/speckit.plan|r1"),
        name="20260102T000008Z-dup00008.json")
    _write_envelope(ws, "customer-beta-cafebabe", dup_name, dup_env)

    view, _ = _run_json(ws)

    envelopes = _envelopes_by_name(ws)
    total_records = sum(s["record_count"] for s in view["sources"])
    assert view["totals"]["record_count"] == total_records == 5
    assert set(view["totals"]) >= {"record_count"}  # 未测总占比 element present
    assert len(view["totals"]) >= 2
    assert view["store_digest"]["record_files_total"] == len(envelopes) == 5
    distinct_keys = len({e["aggregation_envelope"]["identity_key"]
                         for e in envelopes.values()})
    assert view["store_digest"]["identity_keys_total"] == distinct_keys == 4
    # zero-fabrication numeric guard: every numeric totals value must be one
    # of the replayable aggregates (counts, sums, or a ratio of them).
    slots = sum(s["coverage"]["evaluated_total"]
                + s["coverage"]["not_evaluated_total"] for s in view["sources"])
    evaluated = sum(s["coverage"]["evaluated_total"] for s in view["sources"])
    not_evaluated = sum(s["coverage"]["not_evaluated_total"]
                        for s in view["sources"])
    allowed = {total_records, evaluated, not_evaluated}
    if slots:
        allowed |= {not_evaluated / slots, evaluated / slots,
                    round(100 * not_evaluated / slots, 6),
                    round(100 * evaluated / slots, 6)}
    for key, value in view["totals"].items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            assert value in allowed, (
                f"totals[{key!r}]={value!r} is not replayable from the store")


def test_every_number_replayable_from_record_files(tmp_path):
    # FR-011 / SC-004: the reconciliation duty itself — each sources[] entry
    # is recomputed from exactly the files its record_files roster names.
    ws = tmp_path
    _seed_store(ws)
    name, envelope = _envelope(
        "customer-beta", "identified", "/speckit.review", "r10",
        {"tokens": {"value": 9, "provenance": "measured"}},
        name="20260102T000009Z-beef0009.json")
    _write_envelope(ws, "customer-beta-cafebabe", name, envelope)

    view, proc = _run_json(ws)

    assert proc.returncode == 0
    for source in view["sources"]:
        _replay_source(ws, source)
    assert view["totals"]["record_count"] == 5


# --------------------------------------------------------------------------- #
# C-21: zero fabrication — the machine face stays a counter projection
# --------------------------------------------------------------------------- #
def test_view_keys_are_closed_counter_projection(tmp_path):
    # C-21: 不评估、不打分、不判阈值 — the view carries exactly the E7 field
    # set (+ the C-19 skipped_unreadable counter); any scoring/evaluated-value
    # slot would show up as an extra key.
    _seed_store(tmp_path)
    view, _ = _run_json(tmp_path)
    assert set(view) == E7_TOP_KEYS | {"skipped_unreadable"}
    for source in view["sources"]:
        assert set(source) == E7_SOURCE_KEYS
        for counts in source["quality"].values():
            assert set(counts) == {"evaluated", "not_evaluated"}
            assert all(isinstance(v, int) for v in counts.values())


def test_no_fabricated_values_in_view(tmp_path):
    # C-21: zero filled-in / extrapolated values — every leaf of the view is
    # a count, a projection of envelope fields, or an E7 header field.
    ws = tmp_path
    _seed_store(ws)
    view, _ = _run_json(ws)
    on_disk = _envelopes_by_name(ws)
    ok_strings = (
        {VIEW_KIND, ENVELOPE_KIND}
        | {s["project"] for s in view["sources"]}
        | {e["aggregation_envelope"]["identity_status"]
           for e in on_disk.values()}
    )
    for source in view["sources"]:
        assert source["project"] in ok_strings
        assert source["record_files"]
        for name in source["record_files"]:
            assert name in on_disk  # no invented roster entries


# --------------------------------------------------------------------------- #
# C-22: products land under aggregated/summaries/, append-only, isomorphic
# --------------------------------------------------------------------------- #
def test_product_lands_in_summaries_entry_form(tmp_path):
    ws = tmp_path
    _seed_store(ws)
    assert _products(ws) == []

    _, proc = _run_json(ws)

    assert proc.returncode == 0
    products = _products(ws)
    assert len(products) == 1  # one aggregate run → one new file
    assert ENTRY_NAME_FORM.match(products[0].name)  # entry_filename() 形态
    product = json.loads(products[0].read_text(encoding="utf-8"))
    assert product["kind"] == VIEW_KIND
    assert product["schema_version"] == SCHEMA_VERSION
    assert product["generated_at"].endswith("Z")
    assert set(product["store_digest"]) == {"record_files_total",
                                            "identity_keys_total"}


def test_stdout_and_product_are_isomorphic(tmp_path):
    ws = tmp_path
    _seed_store(ws)

    view, _ = _run_json(ws)

    products = _products(ws)
    assert len(products) == 1
    product = json.loads(products[0].read_text(encoding="utf-8"))
    assert view == product  # same structure AND same content, face for face


def test_rerun_appends_new_file_with_identical_numbers(tmp_path):
    # C-22/C-23: rerunning is safe — a new product file, the old one never
    # rewritten, and every projection number identical (rebuildability).
    ws = tmp_path
    _seed_store(ws)
    first_view, _ = _run_json(ws)
    products_after_first = _products(ws)
    first_bytes = products_after_first[0].read_bytes()

    second_view, proc = _run_json(ws)

    assert proc.returncode == 0
    products = _products(ws)
    assert len(products) == 2
    assert products[0].read_bytes() == first_bytes  # append-only
    assert products[1].name != products[0].name
    stable = {"sources", "totals", "store_digest", "kind", "schema_version",
              "skipped_unreadable"}
    assert {k: second_view[k] for k in stable} == {
        k: first_view[k] for k in stable}
    assert second_view["generated_at"].endswith("Z")


def test_empty_aggregated_layer_zero_sources(tmp_path):
    # C-20 edge (CHK027): an empty (and a missing) aggregated layer is a
    # valid zero-view, not a failure; the 0/0 ratio form is deliberately NOT
    # pinned (undefined at contract level) but no fabricated numbers pass the
    # totals guard.
    for ws in (tmp_path / "absent", tmp_path / "empty"):
        ws.mkdir()
        if ws.name == "empty":
            _agg(ws).mkdir(parents=True)
        view, proc = _run_json(ws)
        assert proc.returncode == 0
        assert view["sources"] == []
        assert view["totals"]["record_count"] == 0
        assert view["store_digest"] == {"record_files_total": 0,
                                        "identity_keys_total": 0}
        assert len(_products(ws)) == 1


# --------------------------------------------------------------------------- #
# C-23: explicit action boundary
# --------------------------------------------------------------------------- #
def test_engine_has_no_coupling_to_the_intake_path():
    # C-23: aggregate is an explicit action only — the exec-quant engine
    # cannot be auto-triggered by the receive leg because it holds no
    # coupling to it at all (zero references to the feedback engine or the
    # ingest action). The behavioral negative (ingest → zero summaries/)
    # lives in tests/contract/test_feedback_intake_exec_quant.py and the 4a
    # integration chain.
    source = ENGINE.read_text(encoding="utf-8")
    assert "feedback_utils" not in source
    assert "ingest-exec-quant" not in source
    assert "feedback-utils" not in source


def test_aggregate_writes_only_under_aggregated(tmp_path):
    # C-23: zero network, zero egress; products land only in this repo's
    # aggregated/ — every byte-level change of a run is inside aggregated/.
    ws = tmp_path
    _seed_store(ws)
    before = _snapshot(ws)

    _, proc = _run_json(ws)

    assert proc.returncode == 0
    after = _snapshot(ws)
    changed = {p for p in set(before) | set(after)
               if before.get(p) != after.get(p)}
    assert changed, "aggregate produced nothing at all"
    assert all(p.startswith("aggregated") for p in changed), sorted(changed)
    landed = [p for p in changed if p.startswith("aggregated/summaries/")]
    assert len(landed) == 1 and landed[0] in after  # the product itself
