"""Contract tests for the per-team item ledger (`items.jsonl`).

Pins `contracts/items-ledger.contract.md` rules LC-1…LC-10 plus the identifier
grammar. Two layers, per Constitution Principle VII:

* structural — the ledger schema, invariants and grammar are documented in the
  canonical mapping reference (and its mirror);
* behavioural — the identifier grammar is enforced *upstream* by the
  summarize-project DDL, so we assert against the real loader rather than
  restating the regex. See research.md E-2 / E-7.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

MAPPING_CANONICAL = REPO_ROOT / "skills/create-team/references/summary-mapping.md"
MAPPING_MIRROR = REPO_ROOT / ".specify/skills/create-team/references/summary-mapping.md"

SUMMARIZE_SCRIPTS = REPO_ROOT / "skills/summarize-project/scripts"
PROJECT_DB = SUMMARIZE_SCRIPTS / "project-db.py"

# LC-4 grammar
EXPLICIT_ITEM_ID = re.compile(r"^TI-[0-9]{4}$")
INFERRED_ITEM_ID = re.compile(r"^TIX-[0-9a-f]{8}$")
# LC-5 — the upstream DDL identifier constraint
DDL_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")

LEDGER_STATES = {"completed", "in-progress", "delayed", "not-started", "unknown"}
REQUIRED_KEYS = {"item_id", "title", "phase_ref", "state", "provenance", "ts", "identity"}

# LC-3 — provenance that is not tracked in version control
INADMISSIBLE_PREFIXES = (
    ".specify/teams/.work/",
    ".specify/agents/execution/logs/",
)


pytestmark = pytest.mark.contract


# --------------------------------------------------------------------------
# Structural: the ledger contract is documented in the canonical reference
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_ledger_schema_is_documented(path: Path) -> None:
    assert path.is_file(), f"missing concept-mapping reference: {path}"
    text = path.read_text(encoding="utf-8")
    assert "items.jsonl" in text, "ledger file name absent from the mapping reference"
    for key in sorted(REQUIRED_KEYS):
        assert key in text, f"ledger field `{key}` not documented in {path.name}"


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_ledger_invariants_are_documented(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [tag for tag in ("IL-1", "IL-2", "IL-3", "IL-4", "IL-5") if tag not in text]
    assert not missing, f"ledger invariants {missing} not documented in {path.name}"


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_identifier_grammar_is_documented(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for token in ("TI-", "TIX-", "PH-", "MS-"):
        assert token in text, f"identifier form `{token}` not documented in {path.name}"


# --------------------------------------------------------------------------
# Line-level validation of ledger rows (LC-3, LC-4, LC-5, LC-7)
# --------------------------------------------------------------------------


def validate_ledger_line(row: dict) -> list[str]:
    """Return a list of contract violations for one ledger row."""
    problems: list[str] = []

    missing = REQUIRED_KEYS - row.keys()
    if missing:
        problems.append(f"missing required keys: {sorted(missing)}")
        return problems

    identity = row["identity"]
    if identity not in {"explicit", "inferred"}:
        problems.append(f"LC-4: identity must be explicit|inferred, got {identity!r}")
    else:
        pattern = EXPLICIT_ITEM_ID if identity == "explicit" else INFERRED_ITEM_ID
        if not pattern.match(row["item_id"]):
            problems.append(
                f"LC-4: item_id {row['item_id']!r} does not match {pattern.pattern} "
                f"for identity={identity}"
            )

    if not DDL_IDENTIFIER.match(row["item_id"]):
        problems.append(f"LC-5: item_id {row['item_id']!r} violates the DDL grammar")

    if row["state"] not in LEDGER_STATES:
        problems.append(f"LC-7: state {row['state']!r} outside {sorted(LEDGER_STATES)}")

    provenance = row["provenance"]
    if provenance.startswith(INADMISSIBLE_PREFIXES) or provenance.startswith("/"):
        problems.append(f"LC-3: provenance {provenance!r} is not a tracked path")

    return problems


def test_validator_accepts_a_conforming_row() -> None:
    row = {
        "item_id": "TI-0007",
        "title": "P7 sync-mirrors 单入口",
        "phase_ref": "PH-0002",
        "state": "completed",
        "provenance": ".specify/teams/demo/runs/20260730T094500Z-report.md#deliverables",
        "ts": "2026-07-30T09:45:00Z",
        "identity": "explicit",
        "maturity_at_event": "L1",
    }
    assert validate_ledger_line(row) == []


@pytest.mark.parametrize(
    "mutation,expected_tag",
    [
        ({"item_id": "TI-7"}, "LC-4"),
        ({"item_id": "改进点 7", "identity": "explicit"}, "LC-4"),
        ({"identity": "inferred"}, "LC-4"),
        ({"state": "done"}, "LC-7"),
        ({"provenance": ".specify/teams/.work/demo/parallel-result-a.md"}, "LC-3"),
        ({"provenance": ".specify/agents/execution/logs/a.live.log"}, "LC-3"),
        ({"provenance": "/tmp/spec-kit-dispatch/a.status"}, "LC-3"),
    ],
)
def test_validator_rejects_violations(mutation: dict, expected_tag: str) -> None:
    row = {
        "item_id": "TI-0007",
        "title": "demo",
        "phase_ref": "PH-0001",
        "state": "completed",
        "provenance": ".specify/teams/demo/runs/r.md",
        "ts": "2026-07-30T09:45:00Z",
        "identity": "explicit",
    }
    row.update(mutation)
    problems = validate_ledger_line(row)
    assert problems, f"expected a {expected_tag} violation for {mutation}"
    assert any(expected_tag in p for p in problems), problems


def test_inferred_identifier_is_a_truncated_hash_not_a_title() -> None:
    """FR-027 / LC-5: derived identity must be hashed, because a CJK title is
    rejected by the upstream DDL (measured — see the loader test below)."""
    import hashlib

    title, phase = "洞察台账条目", "PH-0001"
    digest = hashlib.sha256(f"{title}\x00{phase}".encode()).hexdigest()[:8]
    item_id = f"TIX-{digest}"
    assert INFERRED_ITEM_ID.match(item_id)
    assert DDL_IDENTIFIER.match(item_id)
    assert not DDL_IDENTIFIER.match(title), "a CJK title must not be usable as an id"


# --------------------------------------------------------------------------
# Behavioural: the grammar is enforced by the upstream loader (LC-5)
# --------------------------------------------------------------------------


def _minimal_form(item_id: str) -> str:
    return f"""schema: project-input/v1

project:
  project_name: "ledger grammar probe"
  baseline_date: "2026-07-30"

work_items:
  - item_id: {item_id}
    item_name: "probe"
    status: "已完成"
    source: ".specify/teams/demo/runs/r.md"

sources:
  - source_id: S-0001
    source_kind: user-form
    source_ref: ".specify/teams/demo/runs/r.md"
    covers: [work_items]
"""


def _load(tmp_path: Path, item_id: str) -> subprocess.CompletedProcess:
    form = tmp_path / "project-input.yaml"
    form.write_text(_minimal_form(item_id), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(PROJECT_DB),
            "--db",
            str(tmp_path / "project.db"),
            "--load",
            str(form),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


@pytest.mark.skipif(not PROJECT_DB.is_file(), reason="summarize-project loader absent")
def test_loader_accepts_a_conforming_identifier(tmp_path: Path) -> None:
    result = _load(tmp_path, "TI-0001")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(not PROJECT_DB.is_file(), reason="summarize-project loader absent")
@pytest.mark.parametrize("bad_id", ['"TI-0001 x"', '"改进点-1"', '"-TI-0001"'])
def test_loader_rejects_identifiers_outside_the_ddl_grammar(
    tmp_path: Path, bad_id: str
) -> None:
    """LC-5 is enforced upstream: exit code 3, not a silent coercion."""
    result = _load(tmp_path, bad_id)
    assert result.returncode == 3, (
        f"expected exit 3 for id {bad_id}, got {result.returncode}\n"
        + result.stdout
        + result.stderr
    )


@pytest.mark.skipif(not PROJECT_DB.is_file(), reason="summarize-project loader absent")
def test_per_team_identifiers_collide_without_a_team_namespace(tmp_path: Path) -> None:
    """FG-15 / research.md E-7 — the reason aggregation must prefix identifiers.

    `entity_ids` is a global namespace enforced by primary key, so two teams that
    each issue `TI-0001` cannot both load. Prefixing resolves it.
    """
    colliding = """schema: project-input/v1

project:
  project_name: "collision probe"
  baseline_date: "2026-07-30"

work_items:
  - item_id: TI-0001
    item_name: "team A item"
    source: ".specify/teams/a/runs/r.md"
  - item_id: TI-0001
    item_name: "team B item"
    source: ".specify/teams/b/runs/r.md"

sources:
  - source_id: S-0001
    source_kind: user-form
    source_ref: ".specify/teams/a/runs/r.md"
    covers: [work_items]
"""
    form = tmp_path / "collide.yaml"
    form.write_text(colliding, encoding="utf-8")
    clash = subprocess.run(
        [sys.executable, str(PROJECT_DB), "--db", str(tmp_path / "c.db"), "--load", str(form)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert clash.returncode == 3, "unprefixed duplicate ids must be rejected"

    prefixed = colliding.replace("item_id: TI-0001\n    item_name: \"team A item\"",
                                 "item_id: team-a.TI-0001\n    item_name: \"team A item\"")
    prefixed = prefixed.replace("item_id: TI-0001\n    item_name: \"team B item\"",
                                "item_id: team-b.TI-0001\n    item_name: \"team B item\"")
    form2 = tmp_path / "prefixed.yaml"
    form2.write_text(prefixed, encoding="utf-8")
    ok = subprocess.run(
        [sys.executable, str(PROJECT_DB), "--db", str(tmp_path / "p.db"), "--load", str(form2)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert ok.returncode == 0, (
        "team-namespaced ids must load cleanly\n" + ok.stdout + ok.stderr
    )


def test_ledger_fold_takes_the_last_event_per_item(tmp_path: Path) -> None:
    """LC-2: current state is the last event for an item_id, ordered by ts."""
    lines = [
        {"item_id": "TI-0001", "title": "a", "phase_ref": "PH-0001", "state": "not-started",
         "provenance": ".specify/teams/d/runs/r1.md", "ts": "2026-07-01T00:00:00Z",
         "identity": "explicit"},
        {"item_id": "TI-0001", "title": "a", "phase_ref": "PH-0001", "state": "in-progress",
         "provenance": ".specify/teams/d/runs/r2.md", "ts": "2026-07-02T00:00:00Z",
         "identity": "explicit"},
        {"item_id": "TI-0001", "title": "a", "phase_ref": "PH-0001", "state": "completed",
         "provenance": ".specify/teams/d/runs/r3.md", "ts": "2026-07-03T00:00:00Z",
         "identity": "explicit"},
    ]
    ledger = tmp_path / "items.jsonl"
    ledger.write_text("\n".join(json.dumps(r) for r in lines) + "\n", encoding="utf-8")

    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    folded: dict[str, dict] = {}
    for row in sorted(rows, key=lambda r: r["ts"]):
        folded[row["item_id"]] = row

    assert len(folded) == 1
    assert folded["TI-0001"]["state"] == "completed"
    assert all(validate_ledger_line(r) == [] for r in rows)
