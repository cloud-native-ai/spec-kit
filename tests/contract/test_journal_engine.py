"""Contract tests for the journal engine (Feature 096).

Contracts: `contracts/journal-engine.contract.md` C-01…C-13 and
`contracts/journal-format.contract.md` C-01…C-12. Every spelling the test needs is read from
`shared/declarations/facts/journal-format.yaml` through the declaration reader — the module pins
no second copy. The line fixture is built by `tests/fixtures/sdd-observer/line_builder.py` under
`tmp_path`; every engine call is a real subprocess invocation of `scripts/python/journal-utils.py`.
"""
from __future__ import annotations

import calendar
import importlib.util
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "journal-utils.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "sdd-observer"

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

#: T013's mutation drills: the coverage test itself must go red under each.
MUTATION = os.environ.get("SDD_OBSERVER_MUTATION", "")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def line_builder():
    return _load_module("sdd_observer_line_builder", FIXTURES / "line_builder.py")


def tamper_builder():
    return _load_module("sdd_observer_tamper_builder", FIXTURES / "tamper_builder.py")


def journal_format(repo: Path = REPO_ROOT) -> dict:
    reader = _load_module("sdd_observer_declaration_reader", READER)
    fact = reader.load_fact(str(repo), "journal-format")
    return fact["body"]["statement"]


def declared_stages(repo: Path = REPO_ROOT):
    return line_builder().declared_stages(repo)


def _plus_seconds(iso_text, seconds):
    epoch = calendar.timegm(time.strptime(iso_text, "%Y-%m-%dT%H:%M:%SZ"))
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch + seconds))


def run_engine(args, cwd=None, env=None):
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=cwd, env=env, timeout=120,
    )


def append(fixture, *extra, engine=None, env=None):
    command = [
        "--action", "append",
        "--spec-dir", fixture["spec_dir"],
        "--spine", fixture["spine"],
        "--state-dir", fixture["state_dir"],
        "--repo", fixture["root"],
        "--line-id", fixture["line_id"],
        "--run-id", fixture["run_id"],
        "--execution-label", fixture["execution_label"],
    ]
    if engine is None:
        return run_engine(command + list(extra), env=env)
    return subprocess.run(
        [sys.executable, str(engine), *[str(arg) for arg in command + list(extra)]],
        capture_output=True, text=True, env=env, timeout=120,
    )


def check(fixture):
    return run_engine(["--action", "check", "--spec-dir", fixture["spec_dir"], "--repo", fixture["root"]])


def split_cells(line: str):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells, current, index = [], [], 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body) and body[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def parse_journal(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    result = {"title": lines[0] if lines else "", "header": {}, "header_cells": [],
              "separator": "", "rows": [], "body_lines": []}
    index = 1
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("|"):
            break
        if stripped.startswith("- ") and ":" in stripped:
            key, _, value = stripped[2:].partition(":")
            result["header"][key.strip()] = value.strip()
        index += 1
    if index < len(lines):
        result["header_cells"] = split_cells(lines[index])
        index += 1
    if index < len(lines):
        result["separator"] = lines[index].strip()
        index += 1
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or not stripped.startswith("|"):
            break
        result["rows"].append({"line_no": index + 1, "cells": split_cells(lines[index]),
                               "text": lines[index]})
        index += 1
    result["body_lines"] = lines[index:]
    return result


def row_values(parsed):
    columns = journal_format()["entry_columns"]
    return [dict(zip(columns, row["cells"])) for row in parsed["rows"]]


def _fresh_line(tmp_path, **overrides):
    return line_builder().build_line(tmp_path, **overrides)


# --------------------------------------------------------------------------- #
# US1 — the trajectory: coverage, header, table, seq, placeholders, idempotency
# --------------------------------------------------------------------------- #

def test_header_carries_five_declared_keys(tmp_path):
    statement = journal_format()
    fixture = _fresh_line(tmp_path)
    result = append(fixture)
    assert result.returncode == 0, result.stderr
    parsed = parse_journal(fixture["journal"])
    assert parsed["title"] == statement["title_template"].replace("<spec-key>", fixture["spec_key"])
    assert list(parsed["header"]) == statement["header_keys"]
    assert parsed["header"]["line_id"] == fixture["line_id"]
    assert parsed["header"]["run_id"] == fixture["run_id"]
    assert parsed["header"]["spec"] == fixture["spec_key"]
    assert parsed["header"]["observer_instance"] == "sdd-observer-" + fixture["line_id"]
    assert ISO_RE.match(parsed["header"]["created_at"])


def test_body_has_exactly_one_nine_column_table(tmp_path):
    statement = journal_format()
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    parsed = parse_journal(fixture["journal"])
    assert parsed["header_cells"] == statement["entry_columns"]
    assert re.match(r"^\|(\s*:?-{3,}:?\s*\|)+$", parsed["separator"])
    assert parsed["rows"], "the fixture line must produce at least one row"
    for row in parsed["rows"]:
        assert len(row["cells"]) == len(statement["entry_columns"]), row["line_no"]


def test_seq_continues_in_file_order(tmp_path):
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    rows = row_values(parse_journal(fixture["journal"]))
    assert [int(row["seq"]) for row in rows] == list(range(1, len(rows) + 1))


def test_missing_values_use_declared_placeholder(tmp_path):
    placeholder = journal_format()["missing_placeholder"]
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    rows = row_values(parse_journal(fixture["journal"]))
    line_level = [row for row in rows if row["event"] in ("line-start", "observer-start", "commit")]
    assert line_level, "line-level events must be projected"
    for row in line_level:
        assert row["stage"] == placeholder
    starts = [row for row in rows if row["event"] == "stage-start"]
    assert starts, "every declared stage must carry a stage-start row"
    for row in starts:
        assert row["command"] == placeholder
        assert row["artifact"] == placeholder
        assert row["exit"] == placeholder


def test_stage_coverage_over_declared_sequence(tmp_path):
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    stages = declared_stages()
    if MUTATION == "delete-journal":
        fixture["journal"].unlink()
    elif MUTATION.startswith("drop-stage-end:"):
        dropped = MUTATION.split(":", 1)[1]
        kept = []
        for line in fixture["journal"].read_text(encoding="utf-8").splitlines(keepends=True):
            cells = split_cells(line) if line.strip().startswith("|") else []
            if len(cells) == 9 and cells[3] == dropped and cells[4] == "stage-end":
                continue
            kept.append(line)
        fixture["journal"].write_text("".join(kept), encoding="utf-8")
    if not fixture["journal"].is_file():
        pytest.fail("journal is absent: the coverage assertion has no subject")
    rows = row_values(parse_journal(fixture["journal"]))
    for stage in stages:
        assert any(row["stage"] == stage and row["event"] == "stage-start" for row in rows), \
            "stage %s has no stage-start row" % stage
        assert any(row["stage"] == stage and row["event"] == "stage-end" for row in rows), \
            "zero-failure fixture: stage %s has no stage-end row" % stage


def test_append_idempotent_on_unchanged_carriers(tmp_path):
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    first = fixture["journal"].read_bytes()
    second = append(fixture)
    assert second.returncode == 0, second.stderr
    assert fixture["journal"].read_bytes() == first


def test_cli_answers_help_version_and_rejects_unknown(tmp_path):
    help_result = run_engine(["--help"])
    assert help_result.returncode == 0
    assert "side-effects:" in help_result.stdout and "exit-codes:" in help_result.stdout
    version_result = run_engine(["--version"])
    assert version_result.returncode == 0
    assert version_result.stdout.strip().startswith("journal-utils.py ")
    bogus = run_engine(["--bogus-option"])
    assert bogus.returncode != 0


# --------------------------------------------------------------------------- #
# US2 — five tamper drills, the gap drill and persistent-pointer resolution
# --------------------------------------------------------------------------- #

def _clean_journal(tmp_path):
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    return fixture


def _row_line_of_last_data_row(fixture):
    rows = parse_journal(fixture["journal"])["rows"]
    assert rows
    return rows[-1]["line_no"]


@pytest.mark.parametrize("variant,code", [
    ("ten-column", "V-11"),
    ("unknown-event", "V-5"),
    ("free-narrative", "V-12"),
    ("forged-pointer", "V-10"),
    ("unresolvable-commit", "V-10"),
])
def test_tamper_drills_turn_check_red(tmp_path, variant, code):
    fixture = _clean_journal(tmp_path)
    last_line = _row_line_of_last_data_row(fixture)
    original = fixture["journal"].read_text(encoding="utf-8")
    fixture["journal"].write_text(tamper_builder().tamper(original, variant), encoding="utf-8")
    result = check(fixture)
    assert result.returncode == 1, (variant, result.stdout, result.stderr)
    assert code in result.stdout, (variant, result.stdout)
    if variant == "free-narrative":
        narrative_line = len(fixture["journal"].read_text(encoding="utf-8").splitlines())
        assert ":%d" % narrative_line in result.stdout
    else:
        assert ":%d" % last_line in result.stdout, (variant, result.stdout)


def test_gap_drill_emits_exactly_one_window_row(tmp_path):
    fixture = _clean_journal(tmp_path)
    rows = row_values(parse_journal(fixture["journal"]))
    first_observed = rows[-1]["observed_at"]

    restarted_at = _plus_seconds(first_observed, 60)
    restart_label = fixture["execution_label"] + "-restart"
    line_builder().append_observer_record(
        fixture["spine"], fixture["line_id"], fixture["run_id"], fixture["spec_key"],
        restart_label, restarted_at)
    fixture["execution_label"] = restart_label
    second = append(fixture)
    assert second.returncode == 0, second.stderr

    rows = row_values(parse_journal(fixture["journal"]))
    gaps = [row for row in rows if row["event"] == "observer-gap"]
    assert len(gaps) == 1, [row["event"] for row in rows]
    assert gaps[0]["event_at"] == first_observed
    newest = max(row["observed_at"] for row in rows)
    assert gaps[0]["observed_at"] == newest
    clean = check(fixture)
    assert clean.returncode == 0, clean.stdout

    # The drill has teeth: removing the gap-writing path from a copied engine yields no gap row.
    source = ENGINE.read_text(encoding="utf-8")
    marker = "        candidates.extend(_gap_candidates(journal, record, args, repo, fmt))\n"
    assert marker in source, "the gap-writing path marker moved; update the drill"
    mutated_engine = tmp_path / "journal-utils-mutated.py"
    mutated_engine.write_text(source.replace(marker, "", 1), encoding="utf-8")
    mutated_fixture = _fresh_line(tmp_path / "mutated")
    assert append(mutated_fixture).returncode == 0
    mutated_last = row_values(parse_journal(mutated_fixture["journal"]))[-1]["observed_at"]
    mutated_restart = _plus_seconds(mutated_last, 60)
    mutated_label = mutated_fixture["execution_label"] + "-restart"
    line_builder().append_observer_record(
        mutated_fixture["spine"], mutated_fixture["line_id"], mutated_fixture["run_id"],
        mutated_fixture["spec_key"], mutated_label, mutated_restart)
    mutated_fixture["execution_label"] = mutated_label
    mutated_env = dict(os.environ)
    mutated_env["PYTHONPATH"] = str((REPO_ROOT / "scripts" / "python")) + os.pathsep + \
        mutated_env.get("PYTHONPATH", "")
    assert append(mutated_fixture, engine=mutated_engine, env=mutated_env).returncode == 0
    mutated_events = [row["event"] for row in row_values(parse_journal(mutated_fixture["journal"]))]
    assert "observer-gap" not in mutated_events
    mutated_check = check(mutated_fixture)
    assert mutated_check.returncode == 1, mutated_check.stdout
    assert "V-17" in mutated_check.stdout


def test_final_writes_line_terminal_and_observer_settle(tmp_path):
    fixture = _fresh_line(tmp_path)
    assert append(fixture).returncode == 0
    before = [row["event"] for row in row_values(parse_journal(fixture["journal"]))]
    assert "line-terminal" not in before and "observer-settle" not in before
    assert append(fixture, "--final").returncode == 0
    events = [row["event"] for row in row_values(parse_journal(fixture["journal"]))]
    assert events.count("line-terminal") == 1
    assert events.count("observer-settle") == 1
    assert append(fixture, "--final").returncode == 0
    again = [row["event"] for row in row_values(parse_journal(fixture["journal"]))]
    assert again.count("line-terminal") == 1 and again.count("observer-settle") == 1


def test_persistent_pointers_resolve(tmp_path):
    fixture = _clean_journal(tmp_path)
    before = fixture["journal"].read_bytes()
    result = check(fixture)
    assert result.returncode == 0, result.stdout
    assert fixture["journal"].read_bytes() == before, "check must be strictly read-only"
    pointers = []
    for line in fixture["journal"].read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_cells(line)
        if len(cells) != len(journal_format()["entry_columns"]):
            continue
        for chunk in cells[-1].split("; "):
            if chunk.startswith("persistent:"):
                pointers.append(chunk)
    assert pointers
    for chunk in pointers:
        _, kind, target = chunk.split(":", 2)
        target = target.split("#", 1)[0]
        if kind == "commit":
            resolved = subprocess.run(
                ["git", "-C", str(fixture["root"]), "cat-file", "-e", target + "^{commit}"],
                capture_output=True, text=True)
            assert resolved.returncode == 0, chunk
        else:
            assert (fixture["root"] / target).exists(), chunk

