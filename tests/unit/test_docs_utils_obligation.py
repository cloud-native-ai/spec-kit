"""Unit tests: `docs-utils.py --action obligation` (spec 087).

Owner of the assertion names and of each assertion's red-when condition: `plan.md` § Test Plan table A. This
file pins the engine's **judgement surface** — the closed verdict/reason vocabulary, the ordered precedence, the
carrier set, the payload shape, the two predicates and the read-only/deterministic posture. Fixture-driven
end-to-end scenarios live in `tests/integration/test_docs_obligation_scenarios.py`; the carrier-set assertions
have their own file (`test_docs_utils_carriers.py`) because they write a different path.

Every assertion here is RED before `--action obligation` exists. The command-surface block below is therefore
also the front-loaded gate: it names the exact command the contract promises and fails until the engine parses
it.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs-obligation"

# `conftest` is a name pytest itself registers per test directory, so importing it by that
# plain name collides with the root `tests/conftest.py` module. Load the fixture build steps by
# file path instead — one explicit module, no import-order dependency.
_spec = importlib.util.spec_from_file_location(
    "docs_obligation_fixtures", FIXTURES / "conftest.py")
fixtures = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fixtures)


def run_engine(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
    )


def run_json(*args: str) -> dict:
    proc = run_engine(*args)
    assert proc.returncode == 0, f"engine exited {proc.returncode}: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


def obligation(root: Path, *extra: str) -> dict:
    return run_json("--action", "obligation", "--root", str(root), *extra)


def verdict_of(payload: dict, doc_path: str) -> tuple[str, str]:
    for entry in payload["documents"]:
        if entry["path"] == doc_path:
            return entry["verdict"], entry["reason"]
    raise AssertionError(f"{doc_path} not judged; documents={payload['documents']}")


DOC = "docs/concepts/widget-overview.md"


# ---------------------------------------------------------------------------
# C-001 — command surface: the action is registered and its option set is closed
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c001_action_registered():
    """`obligation` is one of the action's accepted choices.

    red-when: the engine's `--action` choices list does not contain `obligation` (exit 2 + `invalid choice`).
    """
    proc = run_engine("--action", "obligation", "--help")
    assert proc.returncode == 0, (
        f"`--action obligation` is not a registered choice: {proc.stderr.strip()}"
    )
    help_text = proc.stdout + proc.stderr
    for option in ("--root", "--record", "--only", "--json"):
        assert option in help_text, f"{option} is missing from the obligation command surface"


@pytest.mark.integration
def test_c001_option_set_closed(tmp_path: Path):
    """The four contract options are accepted; a fifth, contract-external switch is rejected with exit 2.

    red-when: `--record` / `--only` / `--json` is unregistered (exit 2 on a lawful call), or an unknown switch
    is silently accepted (exit 0 where 2 is required).
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = space / "docs" / ".speckit" / "runs" / fixtures_record_name(space)
    ok = run_engine(
        "--action", "obligation", "--root", str(space),
        "--record", str(record), "--only", DOC, "--json",
    )
    assert ok.returncode == 0, f"lawful option set rejected: {ok.stderr.strip()}"
    bad = run_engine("--action", "obligation", "--root", str(space), "--totally-unknown-switch")
    assert bad.returncode == 2, (
        f"a contract-external switch must be an input error (exit 2), got {bad.returncode}"
    )


def fixtures_record_name(space: Path) -> str:
    runs = space / "docs" / ".speckit" / "runs"
    names = sorted(p.name for p in runs.glob("*.json"))
    assert len(names) == 1, f"expected exactly one trace record, got {names}"
    return names[0]


@pytest.mark.integration
def test_c001_before_implementation_exit2(tmp_path: Path):
    """The pre-state reading: before the action existed, the same call exited 2 with `invalid choice`.

    Kept as the front-loaded gate's recorded reading (`notes/pre-change-measurements.md` § T002 (a)). After the
    implementation it asserts the *shape* of the difference instead: the action now parses, so the only way to
    reproduce exit 2 is a genuine input error (an unresolvable `--root`), never a missing choice.

    red-when: a lawful call exits 2 (regression to the pre-state), or an input error exits 0.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    lawful = run_engine("--action", "obligation", "--root", str(space))
    assert lawful.returncode == 0, f"lawful call must exit 0 after implementation: {lawful.stderr.strip()}"
    missing_root = run_engine("--action", "obligation", "--root", str(tmp_path / "no-such-project"))
    assert missing_root.returncode == 2, (
        f"an absent --root is an input error (exit 2), got {missing_root.returncode}"
    )


# ---------------------------------------------------------------------------
# C-016 — the ordered precedence: one pass, earliest tier wins, no backtracking
# ---------------------------------------------------------------------------


def record_arg(space: Path) -> str:
    return str(space / "docs" / ".speckit" / "runs" / fixtures_record_name(space))


@pytest.mark.integration
def test_c016_precedence_order(tmp_path: Path):
    """When several tiers hold at once, the earliest one in the table decides.

    `deleted-rendered/` is the sharp case the contract names (`plan.md` § Test Plan table A `C-016`): the render
    is gone (tier 5, `orphan-*` would claim it) **and** the document's reference points at that missing render
    (tier 4, `reference-unresolved`). Tier 4 is earlier, so `reference-unresolved` must win.

    Plus the surrounding tiers on their own fixtures, so the ordering is read as an order and not as one value.

    red-when: `deleted-rendered/` lands any `orphan-*` value (ordering implemented as an unordered set test), or
    one of the neighbouring tiers resolves to a value its own fixture contradicts.
    """
    cases = {
        "deleted-rendered": ("missing", "reference-unresolved"),
        "orphan-rendered": ("missing", "orphan-rendered"),
        "orphan-source": ("missing", "orphan-source"),
        "no-diagram": ("missing", "no-diagram-reference"),
        "stale-source": ("stale", "source-newer-than-render"),
        "clean": ("satisfied", "reference-resolves"),
        "exempt-ok": ("recorded-exemption", "exempt-chronological"),
    }
    for name, expected in cases.items():
        space = fixtures.copy_fixture(name, tmp_path / name)
        runs = space / "docs" / ".speckit" / "runs"
        records = sorted(runs.glob("*.json"))
        extra = ("--record", str(records[0])) if records else ()
        payload = obligation(space, *extra)
        assert verdict_of(payload, DOC) == expected, (
            f"{name}/ expected {expected}, got {verdict_of(payload, DOC)}"
        )


@pytest.mark.integration
def test_c016_no_backtracking(tmp_path: Path):
    """A hit is final: a later tier never overwrites an earlier tier's decision.

    Observable form of "no backtracking": the sum of the per-verdict counts equals the number of judged
    documents, and no document is judged twice. A decision tree that kept looking after a hit, or re-derived a
    verdict, would show up as a count surplus or a duplicated path.

    red-when: a path appears twice in `documents[]`, or the summary counts do not add up to the judged set.
    """
    space = fixtures.copy_fixture("deleted-rendered", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    paths = [entry["path"] for entry in payload["documents"]]
    assert len(paths) == len(set(paths)), f"a document was judged twice: {paths}"

    summary = payload["summary"]
    counted = (summary["satisfied"] + summary["missing"] + summary["stale"]
               + summary["exempted"] + summary["not_evaluated"])
    assert counted == len(paths), (
        f"summary counts {counted} != judged documents {len(paths)}; a hit was re-decided somewhere"
    )


@pytest.mark.integration
def test_c016_no_second_precedence_owner():
    """There is exactly one code path in the engine that assigns a verdict.

    Two independent decision trees would drift apart the first time one is edited. The check counts the
    assignments to a verdict-shaped name in the engine source and requires a single implementation site.

    red-when: a second independent decision tree appears (a second function that assigns `verdict` outside the
    one ordered pass).
    """
    source = SCRIPT.read_text(encoding="utf-8")
    assign_sites = [
        line for line in source.splitlines()
        if "verdict =" in line and "def " not in line
    ]
    assert len(assign_sites) <= 1, (
        "expected at most one site that assigns a verdict (the ordered pass); found:\n"
        + "\n".join(assign_sites)
    )
    assert source.count("def _judge_document") == 1, (
        "the ordered single-pass judgement must exist exactly once as `_judge_document`"
    )


# ---------------------------------------------------------------------------
# C-013 / C-006 — payload shape: fixed top-level keys, four document fields, stable order
# ---------------------------------------------------------------------------

TOP_LEVEL_KEYS = ["action", "root", "record", "carriers", "documents", "summary"]
DOCUMENT_KEYS = ["path", "line", "verdict", "reason"]
SUMMARY_KEYS = ["satisfied", "missing", "stale", "exempted", "not_evaluated",
                "converged", "clean", "exemption_superseded"]


@pytest.mark.integration
def test_c006_payload_schema(tmp_path: Path):
    """The payload carries exactly the contract's top-level keys and four document fields.

    red-when: a top-level key is missing or an unregistered one appears, or a `documents[]` entry is not
    exactly `path` / `line` / `verdict` / `reason`.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    assert sorted(payload) == sorted(TOP_LEVEL_KEYS), f"top-level keys drifted: {sorted(payload)}"
    assert payload["action"] == "obligation"
    assert Path(payload["root"]).is_absolute(), "root is reported as an absolute path"
    assert Path(payload["root"]).resolve() == space.resolve()
    assert sorted(payload["summary"]) == sorted(SUMMARY_KEYS), (
        f"summary keys drifted: {sorted(payload['summary'])}"
    )
    assert payload["documents"], "the clean fixture has carriers, so documents[] cannot be empty"
    for entry in payload["documents"]:
        assert sorted(entry) == sorted(DOCUMENT_KEYS), f"document entry fields drifted: {sorted(entry)}"
        assert isinstance(entry["line"], int), "line is an int (0 when there is no reference)"
        assert not os.path.isabs(entry["path"]), f"path must be relative: {entry['path']}"


@pytest.mark.integration
def test_c006_field_order_stable(tmp_path: Path):
    """Key order is stable across two runs of one input, at every level of the payload.

    Byte-comparability (C-006 rule 1) depends on this: identical key order means two runs can be compared as
    bytes instead of as parsed trees.

    red-when: the serialised key order differs between the two runs.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    first = run_engine("--action", "obligation", "--root", str(space), "--record", record_arg(space))
    second = run_engine("--action", "obligation", "--root", str(space), "--record", record_arg(space))
    assert first.returncode == second.returncode == 0, first.stderr + second.stderr
    assert json.loads(first.stdout) == json.loads(second.stdout)
    keys = [list(json.loads(first.stdout)), list(json.loads(second.stdout))]
    assert keys[0] == keys[1], f"top-level key order differs between two runs: {keys}"
    assert first.stdout == second.stdout, "key order must be identical, so stdout must be byte-identical"


@pytest.mark.integration
def test_c006_field_set_and_order(tmp_path: Path):
    """`documents[]` carries exactly four fields, never a fifth, and they are in contract order.

    red-when: a fifth field is appended (e.g. a convenience `source`), or the four are emitted in a different
    order run to run.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    for entry in payload["documents"]:
        assert list(entry.keys()) == DOCUMENT_KEYS, (
            f"documents[] field set/order drifted: {list(entry.keys())}"
        )
        assert len(entry) == 4, f"exactly four fields, got {len(entry)}"
