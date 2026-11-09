"""Disposal contract (contracts/existing-semantics-disposal.contract.md C-079…C-084).

Rows pinned here (WP4): T107, T123, T125.

- **T107** — ``owner-unavailable`` and ``inconsistency`` are distinguishable by exit code
  alone: the engine's non-convention reading is asserted, never assumed — a documented check
  failure exits 1, the absent-owner read exits 2 (C-011, C-019 taxonomy).
- **T123/C-079** — the disposition domain is the closed four-member set
  {``owner-moved``, ``pointer``, ``removed``, ``dated-record``}; every pre-existing
  concurrency statement carries exactly one disposition and it is readable. A ``pointer``
  row leaves a resolving path (C-080); a ``dated-record`` row carries its date and reason
  (C-081).
- **T125/C-008/C-083** — the ceiling owner remains ``wp-gate.py``'s declared default
  (``--slot-cap-ceiling``, ``WG-16``); no second assignable site exists and the slot fact
  carries no numeric slot ceiling of its own.

Engine cases are red-first (``scripts/python/concurrency-check.py`` lands in WP2). The live
disposal ledger landed with T134 (WP5); its live read is a hard assertion, so a missing or
emptied ledger fails instead of skipping.
"""
from __future__ import annotations

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
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
WP_GATE = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "wp-gate.py"
DISPOSAL_CONTRACT = (
    REPO_ROOT / ".specify" / "specs" / "093-concurrency-by-default" / "contracts"
    / "existing-semantics-disposal.contract.md"
)
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "093-concurrency-by-default"

DISPOSITIONS = ("owner-moved", "pointer", "removed", "dated-record")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run_engine(*args):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120,
    )


def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    return tmp_path


def _record(repo: Path, name: str, lines) -> Path:
    path = repo / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# T107 — exit-code disposition
# --------------------------------------------------------------------------- #
def test_owner_unavailable_and_inconsistency_are_distinguishable_by_exit_code(tmp_path):
    repo = _repo(tmp_path)
    fact = repo / "shared" / "declarations" / "facts" / "coordinator-dispatch-verdict.yaml"
    fact.unlink()
    (repo / "agents").mkdir()
    (repo / "agents" / "fixture.agent.md").write_text(
        "---\nname: fixture\ncapability-tools: []\n---\n# Fixture\n", encoding="utf-8")
    run_record = _record(repo, "run.yaml", ["units: []"])
    proc = _run_engine("capability", "--repo", repo, "--record", run_record,
                       "--json-out", tmp_path / "cap.json")
    assert proc.returncode == 2, ("owner-unavailable must be exit 2: %s"
                                  % (proc.stdout + proc.stderr))

    inconsistent = _record(repo, "inconsistent.yaml", [
        "pattern: concurrent",
        "codes:",
        "  - single-unit",
        "evidence:",
        "  single-unit:",
        "    units:",
        "      - only-unit",
    ])
    proc = _run_engine("serial-reason", "--repo", repo, "--record", inconsistent,
                       "--json-out", tmp_path / "serial.json")
    assert proc.returncode == 1, ("an inconsistency must be exit 1: %s"
                                  % (proc.stdout + proc.stderr))


# --------------------------------------------------------------------------- #
# T123 — the closed disposition domain
# --------------------------------------------------------------------------- #
def test_disposition_domain_is_the_closed_four_member_set():
    text = DISPOSAL_CONTRACT.read_text(encoding="utf-8")
    for disposition in DISPOSITIONS:
        assert "`%s`" % disposition in text, "missing disposition %r" % disposition
    assert "no fifth disposition" in text, (
        "the contract must state that there is no fifth disposition")


def _judge_dispositions(rows):
    """C-079…C-081 — exactly one disposition per row; pointer paths resolve; records dated."""
    findings = []
    for row in rows:
        matches = [cell for cell in row["cells"] if cell in DISPOSITIONS]
        if len(matches) != 1:
            findings.append(("disposition-missing", row["statement"]))
            continue
        if matches[0] == "pointer":
            evidence = row.get("evidence", "")
            if not evidence or not (REPO_ROOT / evidence).exists():
                findings.append(("dangling-reference", row["statement"]))
        if matches[0] == "dated-record":
            if not row.get("date") or not row.get("reason"):
                findings.append(("record-undated", row["statement"]))
    return findings


def test_judge_rejects_unassigned_and_fifth_dispositions():
    good = [
        {"statement": "064 write lines", "cells": ["owner-moved"], "evidence": "shared/definitions/subagent-definitions.md"},
        {"statement": "070 wp-gate", "cells": ["pointer"], "evidence": "skills/external/sdd-loop-driver/scripts/wp-gate.py"},
        {"statement": "092 plan parallelism", "cells": ["dated-record"], "evidence": "notes/analyze-repair.md",
         "date": "2026-11-09", "reason": "resolved by the reproduction fixture"},
    ]
    assert _judge_dispositions(good) == []
    assert _judge_dispositions([{"statement": "x", "cells": []}])
    assert _judge_dispositions([{"statement": "x", "cells": ["owner-moved", "pointer"]}])
    assert _judge_dispositions([{"statement": "x", "cells": ["retained"]}]), (
        "a fifth disposition is not in the closed set")
    assert _judge_dispositions([{"statement": "x", "cells": ["pointer"], "evidence": "no/such/path.md"}])
    assert _judge_dispositions([{"statement": "x", "cells": ["dated-record"],
                                 "evidence": "notes/x.md", "reason": "no date"}])


def _live_disposition_rows():
    rows = []
    for path in sorted(SPEC_DIR.rglob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
            if any(cell in DISPOSITIONS for cell in cells):
                rows.append({"statement": "|".join(cells[:1]), "cells": cells})
    return rows


def test_every_pre_existing_statement_has_a_readable_disposition():
    rows = _live_disposition_rows()
    assert rows, ("the live disposal ledger must carry disposition rows; a missing "
                  "ledger is a regression, not a skip")
    for row in rows:
        matches = [cell for cell in row["cells"] if cell in DISPOSITIONS]
        assert len(matches) == 1, ("a row must carry exactly one disposition: %s" % row["cells"])


# --------------------------------------------------------------------------- #
# T125 — the ceiling owner
# --------------------------------------------------------------------------- #
def test_ceiling_owner_is_the_gate_default_and_is_not_duplicated(tmp_path):
    source = WP_GATE.read_text(encoding="utf-8")
    match = re.search(r'"--slot-cap-ceiling"[^)]*default\s*=\s*(\d+)', source)
    assert match, "wp-gate.py must declare --slot-cap-ceiling with a numeric default"
    ceiling = int(match.group(1))

    statement = _reader_module().load_fact(
        str(REPO_ROOT), "concurrency-slot-and-reserve")["body"]["statement"]
    owner = statement["ceiling_owner"]
    assert owner["path"] == "skills/external/sdd-loop-driver/scripts/wp-gate.py"
    assert owner["argument"] == "--slot-cap-ceiling"
    assert owner["check_id"] == "WG-16"

    def slot_ceilings(node):
        found = []
        if isinstance(node, dict):
            for key, value in node.items():
                if "slot" in str(key) and "ceiling" in str(key) and isinstance(value, int):
                    found.append((key, value))
                found.extend(slot_ceilings(value))
        elif isinstance(node, list):
            for item in node:
                found.extend(slot_ceilings(item))
        return found

    assert slot_ceilings(statement) == [], (
        "the slot fact must not carry a numeric slot ceiling of its own (C-008)")
    assert ceiling > 0
