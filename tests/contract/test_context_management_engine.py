"""Contract guard: the context-management audit engine (Feature 110, C-027, C-030…C-034, C-040, C-042).

The engine `scripts/python/context-audit.py` is one read-only stdlib entry with two
actions. This file pins its CLI surface, its `check` rule readings on the seeded
violation fixtures, its `manifest` faces (text and JSON, presence tokens, roster row
set, `source-reading` digest) and its honesty legs (no selection, no ranking, no
audited-source content read, no host values or timestamps).

The two decidable duplication shapes of C-027 are judged here: the engine's `check`
rule set is closed at nine (C-032, PA-7), so the two shapes FR-010 makes decidable are
reported by this guard's own reading of the layout table, with the remaining cases left
to review.

Fixture expectations (the fixture inventory lives in `tests/fixtures/context_management_support.py`;
this table is the guard's expectation map, one seeded case per checked rule):

* `violation-unknown-layer`    → `unknown-layer`;
* `violation-unknown-form`     → `unknown-form`;
* `violation-roster-mismatch`  → `roster-mismatch`;
* `violation-roster-order`     → `roster-order`;
* `violation-layer-form`       → exactly two `layer-form-illegal` findings;
* `violation-duplicate-class`  → `duplicate-class`;
* `violation-empty-layer`      → `empty-layer` naming the layout side and the layer;
* `violation-cap-missing`      → `cap-missing`;
* `violation-category-column`  → `category-column`, judged by the header alone.

Authored red-first (C-040): the engine, the owner document and the four facts do not
exist yet at this point of the run, so the whole module is expected to fail before the
implementation rows land.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.context_management_support import (
    ENGINE,
    LAYOUT_COLUMNS,
    REPO_ROOT,
    copy_case_to,
    declaration_reader,
    run_engine,
    run_engine_json,
    table_rows,
)

pytestmark = pytest.mark.contract

OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "context-management-definitions.md"
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SKILL_LAYERS = (REPO_ROOT / "skills",)

MANIFEST_KEYS = ["action", "layer", "rows", "counts", "source_reading"]
ROW_KEYS = ["class", "layer", "form", "sources", "token", "reason", "cap"]
CHECK_KEYS = ["action", "findings", "summary"]
FINDING_KEYS = ["rule", "file", "row", "line", "detail"]
PRESENCE_TOKENS = ("present", "absent", "unreachable", "empty", "not-evaluated")
ABSENCE_TOKENS = ("absent", "unreachable", "empty", "not-evaluated")
CLOSED_RULES = (
    "roster-mismatch",
    "roster-order",
    "unknown-layer",
    "unknown-form",
    "layer-form-illegal",
    "duplicate-class",
    "empty-layer",
    "cap-missing",
    "category-column",
)
CAP_OWNER_CELL = ".specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First)"
VERSION_LINE = re.compile(r"^context-audit\.py \S+$")
DIGEST_LINE = re.compile(r"^source-reading: ([0-9a-f]{64})$", re.M)
TIMESTAMP_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")
RANKING_KEYS = {"rank", "ranking", "score", "relevance", "select", "selection"}

TASK_LAYER_LABEL = "task"
READ_IN_FULL = "read-in-full"
INLINE_DIGEST = "inline-digest"


def _fixture_layer_root(root: Path) -> Path:
    return root if (root / "shared" / "declarations").is_dir() else root / ".specify"


def _fixture_fact(root: Path, slug: str) -> dict:
    return declaration_reader().load_fact(_fixture_layer_root(root), slug)["body"]


def _fixture_layers(root: Path) -> tuple:
    return tuple(_fixture_fact(root, "context-layers")["statement"])


def _fixture_roster(root: Path, layer: str) -> list:
    roster = _fixture_fact(root, "context-classes")["statement"]
    return list(roster[layer])


def _run_raw(*args: str) -> subprocess.CompletedProcess:
    """Run the engine without the fixture helper's appended --workspace-root."""
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    return subprocess.run([sys.executable, str(ENGINE), *args],
                          capture_output=True, text=True, timeout=120)


# --------------------------------------------------------------------------- #
# C-030 — one documented entry, two actions, no wrapper
# --------------------------------------------------------------------------- #
def test_single_documented_entry_two_actions_no_wrapper():
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    help_text = run_engine(REPO_ROOT, "--help")
    assert help_text.returncode == 0, f"--help must exit 0:\n{help_text.stdout}\n{help_text.stderr}"
    lowered = help_text.stdout.lower()
    for action in ("check", "manifest"):
        assert action in lowered, f"--help must document the {action!r} action"
    for flag in ("--action", "--layer", "--workspace-root", "--json"):
        assert flag in help_text.stdout, f"--help must document {flag}"
    wrappers = []
    if COMMANDS_DIR.is_dir():
        for path in sorted(COMMANDS_DIR.glob("*.md")):
            if "context-audit.py" in path.read_text(encoding="utf-8", errors="ignore"):
                wrappers.append(str(path.relative_to(REPO_ROOT)))
    for layer in SKILL_LAYERS:
        if layer.is_dir():
            for path in sorted(layer.rglob("SKILL.md")):
                if "context-audit.py" in path.read_text(encoding="utf-8", errors="ignore"):
                    wrappers.append(str(path.relative_to(REPO_ROOT)))
    assert wrappers == [], f"no command or skill wrapper may ship for the audit entry: {wrappers}"


# --------------------------------------------------------------------------- #
# C-031 — script interface contract satisfied
# --------------------------------------------------------------------------- #
def test_script_interface_contract_is_satisfied():
    short_help = run_engine(REPO_ROOT, "-h")
    long_help = run_engine(REPO_ROOT, "--help")
    assert short_help.returncode == 0 and long_help.returncode == 0
    assert short_help.stdout == long_help.stdout, "-h and --help must print identical bodies"
    lowered = short_help.stdout.lower()
    for label in ("usage", "options", "side-effects", "exit-codes"):
        assert label in lowered, f"the help body must carry the {label!r} label"

    version = run_engine(REPO_ROOT, "--version")
    assert version.returncode == 0, "--version must exit 0"
    line = version.stdout.strip().splitlines()[0] if version.stdout.strip() else ""
    assert VERSION_LINE.match(line), f"--version must print one identity line, got {line!r}"

    help_first = run_engine(REPO_ROOT, "--help", "--workspace-root", str(REPO_ROOT / "missing-root"))
    assert help_first.returncode == 0, "--help must be answered before any read"

    usage_errors = [
        ("--bogus",),
        ("--", "--bogus"),
        ("--version", "--bogus"),
        ("--action", "bogus"),
        (),
        ("--action", "manifest"),
        ("--action", "manifest", "--layer", "bogus"),
        ("--action", "check", "--layer", "project"),
    ]
    for args in usage_errors:
        completed = run_engine(REPO_ROOT, *args)
        assert completed.returncode == 2, (
            f"usage error {args} must exit 2, got {completed.returncode}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}")
        assert '"findings"' not in completed.stdout and '"rows"' not in completed.stdout, (
            f"usage error {args} leaked an action output: {completed.stdout}")

    missing = str(REPO_ROOT / "missing-root")
    for args in (("--action", "check", "--workspace-root", missing),
                 ("--action", "manifest", "--layer", "project", "--workspace-root", missing)):
        completed = _run_raw(*args)
        assert completed.returncode == 2, (
            f"an unresolvable workspace root must exit 2 for {args}, got {completed.returncode}")


def test_missing_owner_document_or_declaration_layer_is_an_input_error(tmp_path: Path):
    empty = tmp_path / "empty"
    empty.mkdir()
    for args in (("--action", "manifest", "--layer", "project"), ("--action", "check")):
        completed = run_engine(empty, *args)
        assert completed.returncode == 2, (
            f"an unresolvable declaration layer must exit 2 for {args}, got {completed.returncode}")
        assert completed.stdout.strip() == "", "an input error must emit no partial verdict"


# --------------------------------------------------------------------------- #
# C-032 / C-040 — one seeded violation per checked rule, exact findings
# --------------------------------------------------------------------------- #
def _findings(root: Path) -> tuple:
    completed, payload = run_engine_json(root, "--action", "check")
    assert completed.returncode == 1, (
        f"a seeded violation must exit 1, got {completed.returncode}\n"
        f"stdout={completed.stdout}\nstderr={completed.stderr}")
    assert payload is not None, f"check --json must print a JSON object:\n{completed.stdout}"
    assert list(payload) == CHECK_KEYS, f"check JSON keys must be {CHECK_KEYS}, got {list(payload)}"
    assert payload["action"] == "check"
    findings = payload["findings"]
    assert isinstance(findings, list) and findings, "a violation fixture must produce a finding"
    for finding in findings:
        assert list(finding) == FINDING_KEYS, (
            f"a finding must carry exactly {FINDING_KEYS}, got {list(finding)}")
        assert finding["rule"] in CLOSED_RULES, f"rule outside the closed set: {finding['rule']}"
        assert finding["file"], "a finding must name its file"
        assert isinstance(finding["row"], int), "a finding must name its row ordinal"
        assert finding["detail"], "a finding must carry a detail"
    summary = payload["summary"]
    assert isinstance(summary, dict) and summary.get("findings") == len(findings), (
        "the summary must count the findings")
    return payload, findings


def _assert_single_rule(case: str, rule: str, tmp_path: Path) -> dict:
    root = copy_case_to(tmp_path, case)
    payload, findings = _findings(root)
    rules = [finding["rule"] for finding in findings]
    assert rules == [rule], f"{case}: expected exactly [{rule!r}], got {rules}"
    first = run_engine(root, "--action", "check")
    rerun = run_engine(root, "--action", "check")
    assert first.stdout == rerun.stdout, f"{case}: two runs on an unchanged tree must be byte-identical"
    assert first.returncode == rerun.returncode == 1
    return payload


def test_rule_unknown_layer_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-unknown-layer", "unknown-layer", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "runtime" in detail, f"the finding must name the unknown token, got {detail!r}"


def test_rule_unknown_form_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-unknown-form", "unknown-form", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "cache" in detail, f"the finding must name the unknown token, got {detail!r}"


def test_rule_roster_mismatch_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-roster-mismatch", "roster-mismatch", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "task-memory" in detail, f"the finding must name the missing class, got {detail!r}"


def test_rule_roster_order_fixture_is_exact(tmp_path: Path):
    _assert_single_rule("violation-roster-order", "roster-order", tmp_path)


def test_rule_layer_form_fixture_yields_exactly_two_findings(tmp_path: Path):
    root = copy_case_to(tmp_path, "violation-layer-form")
    payload, findings = _findings(root)
    rules = [finding["rule"] for finding in findings]
    assert rules == ["layer-form-illegal", "layer-form-illegal"], (
        f"the merged layer-form fixture must yield exactly two layer-form findings, got {rules}")
    rows = sorted(finding["row"] for finding in findings)
    assert len(set(rows)) == 2, f"the two findings must name two different rows, got {rows}"
    assert isinstance(payload["summary"], dict)


def test_rule_duplicate_class_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-duplicate-class", "duplicate-class", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "reality-constraints" in detail, f"the finding must name the class, got {detail!r}"


def test_rule_empty_layer_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-empty-layer", "empty-layer", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "layout" in detail and "task" in detail, (
        f"the empty-layer finding must name the side and the layer, got {detail!r}")


def test_rule_cap_missing_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-cap-missing", "cap-missing", tmp_path)
    detail = payload["findings"][0]["detail"].lower()
    assert "task-memory" in detail, f"the finding must name the row's class, got {detail!r}"


def test_rule_category_column_fixture_is_exact(tmp_path: Path):
    payload = _assert_single_rule("violation-category-column", "category-column", tmp_path)
    finding = payload["findings"][0]
    assert finding["row"] == 0, "the category-column finding is judged by the header alone"


def test_seeded_rule_fixtures_are_exact(tmp_path: Path):
    cases = (
        "violation-unknown-layer",
        "violation-unknown-form",
        "violation-roster-mismatch",
        "violation-roster-order",
        "violation-layer-form",
        "violation-duplicate-class",
        "violation-empty-layer",
        "violation-cap-missing",
        "violation-category-column",
    )
    observed = []
    for case in cases:
        root = copy_case_to(tmp_path / case, case)
        completed, payload = run_engine_json(root, "--action", "check")
        assert completed.returncode == 1, f"{case}: expected exit 1, got {completed.returncode}"
        observed.append(sorted(finding["rule"] for finding in payload["findings"]))
    assert observed == [
        ["unknown-layer"], ["unknown-form"], ["roster-mismatch"], ["roster-order"],
        ["layer-form-illegal", "layer-form-illegal"], ["duplicate-class"], ["empty-layer"],
        ["cap-missing"], ["category-column"],
    ], f"the fixture family must stay exact: {observed}"


def test_check_is_clean_on_this_repository():
    completed, payload = run_engine_json(REPO_ROOT, "--action", "check")
    assert completed.returncode == 0, (
        f"check must be clean on this repository:\n{completed.stdout}\n{completed.stderr}")
    assert payload is not None and payload["findings"] == [], "a clean tree must carry zero findings"
    assert payload["summary"].get("findings") == 0


def test_declaration_error_fixtures_exit_two_without_partial_verdict(tmp_path: Path):
    for case in ("declaration-unknown-member", "declaration-missing"):
        root = copy_case_to(tmp_path / case, case)
        for args in (("--action", "check"), ("--action", "manifest", "--layer", "project")):
            completed = run_engine(root, *args)
            assert completed.returncode == 2, (
                f"{case} {args}: a declaration member error must exit 2, got {completed.returncode}")
            assert '"findings"' not in completed.stdout and '"rows"' not in completed.stdout, (
                f"{case} {args}: a partial verdict leaked: {completed.stdout}")


def test_unparsable_owner_document_is_an_input_error(tmp_path: Path):
    pristine = copy_case_to(tmp_path / "pristine", "all-present")
    mutations = {
        "missing-layout": lambda text: text.replace("## Layout", "## Layout-Moved"),
        "missing-forms": lambda text: text.replace("## Forms", "## Forms-Moved"),
        "short-row": lambda text: text.replace(
            "| `reality-constraints` | system | `pointer` | docs/constraints.md | fixture owner | — |",
            "| `reality-constraints` | system | `pointer` |"),
    }
    for case, mutation in mutations.items():
        root = tmp_path / case
        root.mkdir()
        target = shutil.copytree(pristine, root / "case", symlinks=True)
        doc = target / "shared" / "definitions" / "context-management-definitions.md"
        before = doc.read_text(encoding="utf-8")
        after = mutation(before)
        assert after != before, f"{case}: mutation did not apply"
        doc.write_text(after, encoding="utf-8")
        for args in (("--action", "check"), ("--action", "manifest", "--layer", "project")):
            completed = run_engine(target, *args)
            assert completed.returncode == 2, (
                f"{case} {args}: an unparsable owner document must exit 2, "
                f"got {completed.returncode}\n{completed.stdout}\n{completed.stderr}")


# --------------------------------------------------------------------------- #
# C-033 — manifest: roster rows, presence tokens, faces, digest
# --------------------------------------------------------------------------- #
def _manifest_rows(root: Path, layer: str) -> tuple:
    completed, payload = run_engine_json(root, "--action", "manifest", "--layer", layer)
    assert completed.returncode == 0, (
        f"manifest --layer {layer} must exit 0, got {completed.returncode}\n"
        f"stdout={completed.stdout}\nstderr={completed.stderr}")
    assert payload is not None, f"manifest --json must print a JSON object:\n{completed.stdout}"
    assert list(payload) == MANIFEST_KEYS, f"manifest keys must be {MANIFEST_KEYS}, got {list(payload)}"
    assert payload["action"] == "manifest" and payload["layer"] == layer
    rows = payload["rows"]
    for row in rows:
        assert list(row) == ROW_KEYS, f"a manifest row must carry exactly {ROW_KEYS}, got {list(row)}"
        assert row["token"] in PRESENCE_TOKENS, f"token outside the vocabulary: {row['token']}"
        if row["token"] in ABSENCE_TOKENS:
            assert row["reason"], f"an absence row must carry a reason: {row}"
        else:
            assert row["reason"] in (None, ""), f"a present row carries no reason: {row}"
    counts = payload["counts"]
    assert isinstance(counts, dict)
    assert sum(counts.values()) == len(rows), f"counts must tally the rows: {counts} vs {len(rows)}"
    for token, count in counts.items():
        assert token in PRESENCE_TOKENS, f"a count uses a token outside the vocabulary: {token}"
        assert count == sum(1 for row in rows if row["token"] == token), (
            f"count for {token!r} disagrees with the row tokens")
    assert re.match(r"^[0-9a-f]{64}$", payload["source_reading"] or ""), (
        "the JSON source_reading must be one SHA-256 hex digest")
    return payload, rows


def test_manifest_prints_roster_rows_with_presence_and_cap(tmp_path: Path):
    root = copy_case_to(tmp_path, "all-present")
    forms = tuple(_fixture_fact(root, "context-forms")["statement"])
    for layer in _fixture_layers(root):
        _payload, rows = _manifest_rows(root, layer)
        assert [row["class"] for row in rows] == _fixture_roster(root, layer), (
            f"layer {layer!r}: rows must be the roster in roster order")
        for row in rows:
            assert row["layer"] == layer
            assert row["form"] in forms, f"row form outside the declared forms: {row}"
            assert row["sources"], f"a present row must name its source(s): {row}"
            assert row["token"] == "present", f"all-present must read present: {row}"
            if row["form"] in ("bounded-index", "read-in-full", "inline-digest"):
                assert row["cap"] == CAP_OWNER_CELL, (
                    f"a capped or content-bearing row must cite the cap owner: {row}")

    text = run_engine(root, "--action", "manifest", "--layer", "project")
    assert text.returncode == 0
    assert DIGEST_LINE.search(text.stdout), "the text face must end with one source-reading digest line"
    for row in _manifest_rows(root, "project")[1]:
        assert row["class"] in text.stdout and row["token"] in text.stdout, (
            f"the text face must carry the JSON row content: {row['class']}")


def test_manifest_reads_genuine_absences_with_reasons(tmp_path: Path):
    root = copy_case_to(tmp_path, "absence-mixed")
    _payload, system_rows = _manifest_rows(root, "system")
    system_by_class = {row["class"]: row for row in system_rows}
    assert system_by_class["reality-constraints"]["token"] == "absent", (
        "the missing source must read absent")
    assert "docs/constraints.md" in system_by_class["reality-constraints"]["reason"]

    _payload, project_rows = _manifest_rows(root, "project")
    project_by_class = {row["class"]: row for row in project_rows}
    assert project_by_class["concept-definitions"]["token"] == "present"

    _payload, task_rows = _manifest_rows(root, "task")
    task_by_class = {row["class"]: row for row in task_rows}
    assert task_by_class["task-artifacts"]["token"] == "unreachable", (
        "the dangling symlink must read unreachable")
    assert ".specify/specs" in task_by_class["task-artifacts"]["reason"]
    assert task_by_class["task-memory"]["token"] == "empty", (
        "the memory root holding only an empty entry must read empty")
    assert ".specify/session" in task_by_class["task-memory"]["reason"]


def _structure_consistency(rows: list) -> str:
    """The derived consistency reading: one non-present carrier → Unobserved (FR-028).

    All carriers present yields no agreement claim either — the manifest reads pointer
    presence only, so the derivation stays silent (`not-claimed`) rather than `present`.
    """
    if any(row["token"] != "present" for row in rows):
        return "Unobserved"
    return "not-claimed"


def test_manifest_row_set_is_the_roster_on_concept_missing(tmp_path: Path):
    root = copy_case_to(tmp_path, "concept-missing")
    payload, rows = _manifest_rows(root, "project")
    by_class = {row["class"]: row for row in rows}
    assert [row["class"] for row in rows] == _fixture_roster(root, "project")
    missing = by_class["concept-definitions"]
    assert missing["token"] == "not-evaluated", (
        "a roster class whose layout row is missing must read not-evaluated")
    assert "layout row" in missing["reason"], (
        f"the reason must name the missing layout row, got {missing['reason']!r}")
    assert missing["form"] == "—" and missing["sources"] == [] and missing["cap"] == "—", (
        f"a missing-layout row prints the undeclared placeholders: {missing}")
    assert by_class["project-vocabulary"]["token"] == "unreachable", (
        "the unreadable concept source must read unreachable")
    assert by_class["concept-explanations"]["token"] == "present"

    concept_rows = [by_class[name] for name in
                    ("project-vocabulary", "concept-definitions", "concept-explanations")]
    derived = _structure_consistency(concept_rows)
    assert derived == "Unobserved", (
        f"the affected structure's consistency reading must be Unobserved, got {derived!r}")

    text = run_engine(root, "--action", "manifest", "--layer", "project")
    assert text.returncode == 0
    lowered = text.stdout.lower()
    for word in ("agreement", "consistent", "agrees"):
        assert word not in lowered, (
            f"no manifest output may claim agreement: {word!r} in {text.stdout!r}")
    assert by_class["concept-definitions"]["token"] != "present"


def test_manifest_json_and_text_faces_carry_the_same_content(tmp_path: Path):
    root = copy_case_to(tmp_path, "all-present")
    for layer in _fixture_layers(root):
        completed, payload = run_engine_json(root, "--action", "manifest", "--layer", layer)
        assert completed.returncode == 0
        text = run_engine(root, "--action", "manifest", "--layer", layer)
        assert text.returncode == 0
        for row in payload["rows"]:
            assert row["class"] in text.stdout, f"text face misses class {row['class']}"
            assert f"token={row['token']}" in text.stdout, (
                f"text face misses the {row['token']!r} token of {row['class']}")
            assert f"form={row['form']}" in text.stdout
        match = DIGEST_LINE.search(text.stdout)
        assert match, "the text face must end with one source-reading digest line"
        assert match.group(1) == payload["source_reading"], (
            "the two faces must carry the same digest")


def test_source_reading_digest_is_stable_and_tracks_metadata(tmp_path: Path):
    root = copy_case_to(tmp_path, "all-present")
    first = run_engine(root, "--action", "manifest", "--layer", "project")
    second = run_engine(root, "--action", "manifest", "--layer", "project")
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout, "two runs on an unchanged tree must be byte-identical"
    digest_one = DIGEST_LINE.search(first.stdout).group(1)

    source = root / ".specify" / "glossary.md"
    stat = source.stat()
    os.utime(source, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    third = run_engine(root, "--action", "manifest", "--layer", "project")
    digest_two = DIGEST_LINE.search(third.stdout).group(1)
    assert digest_two != digest_one, (
        "a declared source's metadata change must move the source-reading digest")


# --------------------------------------------------------------------------- #
# C-034 — the audit is honest: no selection, ranking, content read or host value
# --------------------------------------------------------------------------- #
def test_audit_does_not_select_rank_or_read_content(tmp_path: Path):
    root = copy_case_to(tmp_path, "all-present")
    baseline = run_engine(root, "--action", "manifest", "--layer", "project")
    assert baseline.returncode == 0

    source = root / ".specify" / "glossary.md"
    stat = source.stat()
    original = source.read_bytes()
    replacement = (b"#" * len(original))[: len(original)]
    assert len(replacement) == len(original)
    source.write_bytes(replacement)
    os.utime(source, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    after = run_engine(root, "--action", "manifest", "--layer", "project")
    assert after.stdout == baseline.stdout, (
        "a content-only change with metadata restored must leave the output untouched")

    combined = baseline.stdout
    assert str(REPO_ROOT) not in combined
    assert str(tmp_path) not in combined
    assert not TIMESTAMP_RE.search(combined), "no timestamp may enter the manifest"

    completed, payload = run_engine_json(root, "--action", "manifest", "--layer", "task")
    assert completed.returncode == 0
    keys = set(payload)
    for row in payload["rows"]:
        keys |= set(row)
    assert keys & RANKING_KEYS == set(), (
        f"ranking/selection keys leaked: {sorted(keys & RANKING_KEYS)}")


# --------------------------------------------------------------------------- #
# C-027 — the two decidable duplication shapes FR-010 makes decidable
# --------------------------------------------------------------------------- #
def _owner_text() -> str:
    assert OWNER_DOC.is_file(), f"owner document missing: {OWNER_DOC}"
    return OWNER_DOC.read_text(encoding="utf-8")


def _owner_layout_rows(text: str) -> list:
    header, rows = table_rows(text, "Layout")
    assert tuple(header) == LAYOUT_COLUMNS, f"layout header must be {LAYOUT_COLUMNS}, got {header}"
    return rows


def _split_sources(cell: str) -> list:
    return [part.strip() for part in cell.split(",") if part.strip()]


def _decidable_duplications(rows: list) -> list:
    """The two decidable shapes of C-027 over a layout table (guard-side reading).

    Shape 1: a task row using `read-in-full` over a source an invariant row declares.
    Shape 2: a task row using `inline-digest` over a source an invariant row
    materializes as `read-in-full`.
    """
    invariant_sources = set()
    read_in_full_sources = set()
    for row in rows:
        layer, form = row[1], row[2]
        if layer == TASK_LAYER_LABEL:
            continue
        for source in _split_sources(row[3]):
            invariant_sources.add(source)
            if form == READ_IN_FULL:
                read_in_full_sources.add(source)
    found = []
    for row in rows:
        class_id, layer, form = row[0], row[1], row[2]
        if layer != TASK_LAYER_LABEL:
            continue
        sources = _split_sources(row[3])
        if form == READ_IN_FULL and any(source in invariant_sources for source in sources):
            found.append((class_id, "read-in-full-over-invariant-source"))
        if form == INLINE_DIGEST and any(source in read_in_full_sources for source in sources):
            found.append((class_id, "inline-digest-of-read-in-full-source"))
    return sorted(found)


def test_decidable_duplication_shapes_are_reported(tmp_path: Path):
    lowered = _owner_text().lower()
    assert "duplication" in lowered, "the owner document must declare the decidable duplication shapes"
    assert READ_IN_FULL in lowered and INLINE_DIGEST in lowered
    assert "review" in lowered, "the remaining duplication cases must be left to review"

    pristine = copy_case_to(tmp_path / "pristine", "all-present")
    pristine_doc = pristine / "shared" / "definitions" / "context-management-definitions.md"
    pristine_rows = _owner_layout_rows(pristine_doc.read_text(encoding="utf-8"))
    assert _decidable_duplications(pristine_rows) == [], (
        "the clean fixture must carry no decidable duplication")

    shape_one = tmp_path / "shape-one"
    shape_one.mkdir()
    root = shutil.copytree(pristine, shape_one / "case", symlinks=True)
    doc = root / "shared" / "definitions" / "context-management-definitions.md"
    before = doc.read_text(encoding="utf-8")
    mutated = before.replace(
        "| `task-memory` | task | `bounded-index` | .specify/session/, .specify/knowledge/ | fixture owner |"
        " .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |",
        "| `task-memory` | task | `read-in-full` | .specify/constitution.md | fixture owner |"
        " .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |")
    assert mutated != before, "shape-one mutation did not apply"
    doc.write_text(mutated, encoding="utf-8")
    assert _decidable_duplications(_owner_layout_rows(mutated)) == [
        ("task-memory", "read-in-full-over-invariant-source")]

    shape_two = tmp_path / "shape-two"
    shape_two.mkdir()
    root = shutil.copytree(pristine, shape_two / "case", symlinks=True)
    doc = root / "shared" / "definitions" / "context-management-definitions.md"
    before = doc.read_text(encoding="utf-8")
    mutated = before.replace(
        "| `task-statement` | task | `inline-digest` | .specify/shared/workflow/user-input-protocol.md |",
        "| `task-statement` | task | `inline-digest` | .specify/constitution.md |")
    assert mutated != before, "shape-two mutation did not apply"
    doc.write_text(mutated, encoding="utf-8")
    assert _decidable_duplications(_owner_layout_rows(mutated)) == [
        ("task-statement", "inline-digest-of-read-in-full-source")]