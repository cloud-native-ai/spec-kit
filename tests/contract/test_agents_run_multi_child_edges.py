"""Contract tests for multi-child identity — same superagent, several children (104-agents-run, US2).

Clause source: .specify/specs/104-agents-run/contracts/agents-run-dispatch.contract.md
(C-16 / C-17, FR-011 / FR-012) and SC-002.

This module guards **pre-existing engine behaviour** (migration/regression exception, no
red-first step): it builds the same-parent / two-label fixture over the carriers the
``run-agent`` label convention already uses — dispatch records written in the shape
``exec-quant.py --action collect-dispatch`` declares (``unit_type=agent`` /
``unit_id=agent:<parent>`` / ``run_id=<label>``) plus the external artifact triplet
``<label>.live.log`` / ``<label>.jsonl`` / ``<label>.status`` — and runs the read-only
``role-edge-check.py``. The mutation leg (two labels collapsed into one) is the red form:
the report then no longer presents two independent edges.

Clause-class honesty (FR-023): label uniqueness at runtime is behavior-class; this module
pins the fixture-visible projection (two recorded attempts -> two edges) and the owner text
for stale-return attribution. It does not claim contract coverage of live dispatch behaviour.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
WATCH_MODEL = REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver" / "references" / "watch-model.md"

TRIPLET_SUFFIXES = (".live.log", ".jsonl", ".status")
PARENT_ID = "root"  # the owner's root literal — no second root identity is invented


def _build_fixture(tmp_path: Path, attempts: list[tuple[str, str]]) -> dict:
    """Materialize (record_name, label) dispatch attempts plus their artifact triplets."""
    state = tmp_path / "state"
    teams = tmp_path / "teams"
    logs = tmp_path / "logs"
    registry = tmp_path / "registry"
    for path in (state, teams, logs, registry):
        path.mkdir()
    store = tmp_path / "exec-quant" / "records"
    store.mkdir(parents=True)
    for index, (record_name, label) in enumerate(attempts):
        record = {
            "unit_type": "agent",
            "unit_id": f"agent:{PARENT_ID}",
            "run_id": label,
        }
        (store / f"{index:02d}-{record_name}.json").write_text(
            json.dumps(record), encoding="utf-8"
        )
        for suffix in TRIPLET_SUFFIXES:
            (logs / f"{label}{suffix}").write_text(
                f"attempt={label}\n", encoding="utf-8"
            )
    return {
        "state": state,
        "teams": teams,
        "logs": logs,
        "registry": registry,
    }


def _report(fixture: dict) -> tuple[int, dict]:
    result = subprocess.run(
        [
            sys.executable,
            str(ENGINE),
            "--action",
            "report",
            "--state-dir",
            str(fixture["state"]),
            "--teams-dir",
            str(fixture["teams"]),
            "--logs-dir",
            str(fixture["logs"]),
            "--registry-dir",
            str(fixture["registry"]),
            "--format",
            "json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode in (0, 1), (
        "role-edge-check.py failed to judge the fixture:\n" + result.stdout + result.stderr
    )
    return result.returncode, json.loads(result.stdout)


def test_sc002_two_children_under_one_parent_report_two_edges(tmp_path):
    """SC-002: two child labels under one parent -> two edges, depth 1, zero violations."""
    fixture = _build_fixture(tmp_path, [("attempt-alpha", "alpha"), ("attempt-beta", "beta")])
    rc, payload = _report(fixture)

    assert rc == 0, "a clean fixture must exit 0"
    assert payload["summary"] == {
        "edges": 2,
        "executors": 3,
        "violations": 0,
        "conflicts": 0,
    }
    children = {edge["child"] for edge in payload["edges"]}
    assert children == {"alpha", "beta"}, "the two runs did not land as two independent children"
    for edge in payload["edges"]:
        assert edge["parent"] == PARENT_ID, "the child edge lost its parent identity"
        assert edge["depth"] == 1, "a child of a root must sit at depth 1"
        assert edge["role_declaration"] == "subagent"
    root = next(item for item in payload["executors"] if item["id"] == PARENT_ID)
    assert root["roles"] == ["superagent"] and root["depth"] == 0
    assert payload["violations"] == [], "the clean multi-child fixture reported a violation"


def test_sc002_label_collapse_stops_presenting_two_edges(tmp_path):
    """Red form: collapsing both attempts onto one label yields one edge, not two."""
    fixture = _build_fixture(
        tmp_path, [("attempt-one", "alpha"), ("attempt-retry", "alpha")]
    )
    _rc, payload = _report(fixture)

    assert payload["summary"]["edges"] == 1, (
        "two records sharing one label must collapse to a single edge identity"
    )
    assert not (
        len(payload["edges"]) == 2
        and {edge["child"] for edge in payload["edges"]} == {"alpha", "beta"}
    ), "the report still presents two independent edges after the labels were collapsed"


def test_sc002_retry_uses_a_new_label_and_keeps_the_old_triplet(tmp_path):
    """A retry is a new attempt: new label, both triplets kept, old content untouched."""
    fixture = _build_fixture(tmp_path, [("attempt-alpha", "alpha"), ("attempt-beta", "beta")])
    _rc, payload = _report(fixture)

    assert len(payload["edges"]) == 2
    labels = sorted(edge["child"] for edge in payload["edges"])
    assert labels == ["alpha", "beta"], "the retry reused the old label instead of a new one"
    for label in labels:
        for suffix in TRIPLET_SUFFIXES:
            path = fixture["logs"] / f"{label}{suffix}"
            assert path.is_file(), f"the old attempt's artifact was dropped: {path.name}"
            assert path.read_text(encoding="utf-8") == f"attempt={label}\n", (
                f"the old attempt's artifact was overwritten: {path.name}"
            )


def test_stale_return_attribution_is_owned_by_watch_model_section_11():
    """C-16 pointer target: stale attempts are attributed, never consumed as current."""
    text = WATCH_MODEL.read_text(encoding="utf-8")
    assert "## 11." in text, "the watch model lost its section 11"
    section = text.split("## 11.", 1)[1].split("\n## ", 1)[0]
    assert "stale-run" in section, "the stale-run attribution class is not declared"
    assert "只有 `own` 事件参与判定" in section, (
        "the consumption rule (only own events count) is missing"
    )
    assert "不改变 verdict" in section and "不转发为当前线路进度" in section, (
        "a stale attempt's late return may be forwarded as the current result"
    )
