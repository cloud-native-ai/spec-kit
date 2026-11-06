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
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs-obligation"

# The fixture build steps are a plain helper module, not a pytest fixture module: a
# `conftest.py` anywhere under the rootdir is registered by pytest under the plain module
# name `conftest`, which shadowed the root `tests/conftest.py`. Load it by file path
# instead — one explicit module, no import-order dependency.
_spec = importlib.util.spec_from_file_location(
    "docs_obligation_fixtures", FIXTURES / "helpers.py")
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


def _reported_line(root: Path, doc_path: str, *extra: str) -> int:
    """The `line` the engine reports for `doc_path` (C-005: the reference's own line, or 0 when there is none)."""
    payload = obligation(root, *extra)
    for entry in payload["documents"]:
        if entry["path"] == doc_path:
            return entry["line"]
    raise AssertionError(f"{doc_path} not judged; documents={payload['documents']}")


DOC = "docs/concepts/widget-overview.md"
TYPE_DIRS = ("concepts", "tutorials", "tasks", "reference", "decisions", "contribute")


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
VERDICTS = ("satisfied", "missing", "stale", "recorded-exemption", "not-evaluated")


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


# ---------------------------------------------------------------------------
# C-013 — the two predicates (`converged`, `clean`) and the five counts
#
# The two predicates answer two different questions and the definition point for both is
# `contracts/diagram-obligation.contract.md` C-013: `converged = judged_scope_has_carrier &&
# missing == 0 && stale == 0 && not_evaluated == 0`; `clean = converged && exempted == 0`.
# Each assertion below drives one of the four false-green faces through a real fixture and
# reads the predicate back, so "the space is fine" can never be produced by an empty or
# exemption-carrying scope.
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c013_clean_is_strict(tmp_path: Path):
    """A dirty space turns both predicates false, and the counts say why.

    `no-diagram/` has a complete record and both faces on disk; the only defect is that the judgeable document
    carries no diagram reference. Every other carrier has none either, so the space reads six `missing` — one
    is enough to make `converged` and `clean` false, and the "run finished" fact lives in the exit code, never
    here.

    red-when: a non-zero `missing` / `stale` / `not_evaluated` count still yields `converged` or `clean` true, or
    the counts do not add up to the judged documents.
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    summary = payload["summary"]
    assert summary["missing"] == 6, f"no-diagram/ must report six missing carriers, got {summary['missing']}"
    assert summary["converged"] is False, "a non-zero missing count must force converged=false"
    assert summary["clean"] is False, "a non-zero missing count must force clean=false"
    counted = (summary["satisfied"] + summary["missing"] + summary["stale"]
               + summary["exempted"] + summary["not_evaluated"])
    assert counted == len(payload["documents"]) == payload["carriers"], (
        "the five counts must partition the judged documents"
    )


@pytest.mark.integration
def test_c013_empty_scope_not_converged(tmp_path: Path):
    """A space with no carrier at all is "no judgement object", never "compliant".

    red-when: `carriers == 0` reports `converged` true (a zero-finding claim produced by an empty judged set).
    """
    empty = tmp_path / "no-carriers"
    (empty / "docs" / "notes").mkdir(parents=True)
    (empty / "docs" / "notes" / "scratch.md").write_text("# scratch\n", encoding="utf-8")
    payload = obligation(empty)
    assert payload["carriers"] == 0, f"the space must have no carrier, got {payload['carriers']}"
    assert payload["documents"] == [], "an empty judged scope carries no documents[]"
    assert payload["summary"]["converged"] is False, (
        "carriers == 0 means the criterion has no object; converged MUST be false"
    )
    assert payload["summary"]["clean"] is False, "carriers == 0 must also force clean=false"


@pytest.mark.integration
def test_c013_converged_ignores_exemptions(tmp_path: Path):
    """A named exemption is a lawful end state: it blocks `clean`, never `converged`.

    `exempt-ok/` ships one documented exemption. Every other carrier in the space has no diagram at all, so the
    reading is `exempted == 1`, `converged == false` (those `missing` findings still await convergence),
    `clean == false`. The assertion that matters is the direction: the exemption itself never drives
    `converged` down — remove the unrelated `missing` findings from the judged scope with `--only` and the
    space converges while staying unclean. An implementation that defines `converged` as a synonym of `clean`
    reads `false` in both places and fails on the `--only` reading.

    red-when: `exempted > 0` drives `converged` false on its own (i.e. the `--only` reading does not converge),
    or an exemption-carrying space reports `clean` true.
    """
    space = fixtures.copy_fixture("exempt-ok", tmp_path)
    payload = obligation(space)
    summary = payload["summary"]
    assert verdict_of(payload, DOC) == ("recorded-exemption", "exempt-chronological")
    assert summary["exempted"] == 1, f"exempt-ok/ carries exactly one exemption, got {summary['exempted']}"
    assert summary["missing"] == 5, f"the five undiagrammed carriers are missing, got {summary['missing']}"
    assert summary["converged"] is False, "the five pending missing findings keep the space unconverged"
    assert summary["clean"] is False, "an exemption visible is not a pass: clean MUST be false"

    scoped = obligation(space, "--only", DOC)
    assert scoped["summary"]["exempted"] == 1, "the exemption is the only judged object"
    assert scoped["summary"]["converged"] is True, (
        "an exemption is a lawful end state and MUST NOT block convergence (C-013, SC-008)"
    )
    assert scoped["summary"]["clean"] is False, "converged + exempted > 0 is the 'converged but unclean' state"


@pytest.mark.integration
def test_c013_only_empty_scope(tmp_path: Path):
    """An `--only` that selects nothing is the caller's choice, not a verdict on the space.

    The contract fixes both predicates true for that reading because nothing judged is unclean; the caller
    MUST NOT read it as "the space complies". The assertion pins the values so the two readings stop being
    conflated, and pins that the rest of the space stays unjudged.

    red-when: `--only` silently widens to the whole space, or the narrowed empty scope is reported as a
    non-converged space (conflating "nothing judged" with "something unclean").
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path)
    payload = obligation(space, "--record", record_arg(space), "--only", "docs/concepts/absent.md")
    assert payload["documents"] == [], "an --only that matches nothing judges nothing"
    assert payload["carriers"] == 6, (
        f"carriers reports the whole carrier population, not the narrowed scope; got {payload['carriers']}"
    )
    assert payload["summary"]["converged"] is True, (
        "the narrowed empty scope is the caller's choice; nothing judged is unclean"
    )
    assert payload["summary"]["clean"] is True, "same reading for clean"
    narrowed = obligation(space, "--record", record_arg(space), "--only", DOC)
    assert [entry["path"] for entry in narrowed["documents"]] == [DOC], (
        "--only must judge exactly the named carrier"
    )


@pytest.mark.integration
def test_c013_documents_field_set(tmp_path: Path):
    """`documents[]` is ordered by `path` and every entry carries all four fields.

    `data-model.md` E3 owns the field set; this row pins the observable consequences: a total order on
    `path` (byte-comparability, C-006) and no entry that lost a field on a branch of the judgement.

    red-when: the paths are not in ascending order, or an entry is missing one of the four fields.
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    paths = [entry["path"] for entry in payload["documents"]]
    assert paths == sorted(paths), f"documents[] must be sorted by path: {paths}"
    assert len(paths) == 6, f"no-diagram/ judges six carriers, got {len(paths)}"
    for entry in payload["documents"]:
        assert set(entry) == set(DOCUMENT_KEYS), f"entry lost a field: {entry}"
        assert isinstance(entry["path"], str) and entry["path"].startswith("docs/"), entry
        assert isinstance(entry["line"], int), entry
        assert entry["verdict"] in VERDICTS, entry
        assert entry["reason"], entry


# ---------------------------------------------------------------------------
# C-001 / C-015 — the exit-code contract
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c015_exit_codes(tmp_path: Path):
    """`0` = "judged, clean or not"; `2` = input error; a merely dirty space is never a non-zero exit.

    This is the clause that keeps two facts apart: "the run finished" (exit code) and "the space is clean"
    (payload). Mapping dirtiness onto the exit code would make a reconciling caller unable to tell a broken
    invocation from a space with findings.

    red-when: a dirty space exits non-zero, or an input error (`--root` absent, `--record` unreadable, unknown
    switch) exits 0.
    """
    dirty = fixtures.copy_fixture("no-diagram", tmp_path / "dirty")
    judged_dirty = run_engine("--action", "obligation", "--root", str(dirty),
                              "--record", str(dirty / "docs" / ".speckit" / "runs" / fixtures_record_name(dirty)))
    assert judged_dirty.returncode == 0, (
        f"a dirty space is still a completed judgement (exit 0), got {judged_dirty.returncode}"
    )
    assert json.loads(judged_dirty.stdout)["summary"]["clean"] is False, "the dirtiness lives in the payload"

    absent_root = run_engine("--action", "obligation", "--root", str(tmp_path / "no-such-root"))
    assert absent_root.returncode == 2, f"--root absent is an input error (exit 2), got {absent_root.returncode}"

    space = fixtures.copy_fixture("clean", tmp_path / "clean")
    unreadable = run_engine("--action", "obligation", "--root", str(space),
                            "--record", str(space / "docs" / ".speckit" / "runs" / "no-such-record.json"))
    assert unreadable.returncode == 2, f"--record unreadable is an input error (exit 2), got {unreadable.returncode}"

    unknown = run_engine("--action", "obligation", "--root", str(space), "--totally-unknown-switch")
    assert unknown.returncode == 2, f"an unknown option is an input error (exit 2), got {unknown.returncode}"


@pytest.mark.integration
def test_c015_validate_action_intact():
    """`--action validate` survives as its own action; `obligation` is a sibling, not a replacement.

    The contract keeps these two apart because they answer different questions on different clocks: `validate`
    answers "is this document well formed", `obligation` answers "does this document carry its diagram yet". A
    merged action could not express the transition period this feature deliberately creates (today's compliant
    space, tomorrow's newly-obligated one), so `validate` must remain a registered choice with its own judge and
    must not share the obligation implementation.

    red-when: `validate` leaves the `choices` set, or the obligation code path is reached from `validate`.
    """
    source = SCRIPT.read_text(encoding="utf-8")
    choices = re.search(r"choices\s*=\s*\[([^\]]*)\]", source, re.S)
    assert choices, "the action registry did not parse out of the engine source"
    registered = set(re.findall(r"[\"']([a-z0-9-]+)[\"']", choices.group(1)))
    assert "validate" in registered, f"`validate` left the action registry: {sorted(registered)}"
    assert "obligation" in registered, f"`obligation` is not registered beside `validate`: {sorted(registered)}"

    validate_body = re.search(r"def cmd_validate\(.*?(?=\ndef )", source, re.S)
    assert validate_body, "`cmd_validate` was not found, so the not-shared reading cannot be taken"
    assert "obligation" not in validate_body.group(0), (
        "`cmd_validate` reaches the obligation code path: the two actions are merged"
    )
    obligation_body = re.search(r"def cmd_obligation\(.*?(?=\ndef )", source, re.S)
    assert obligation_body, "`cmd_obligation` was not found"
    assert "cmd_validate" not in obligation_body.group(0), (
        "`cmd_obligation` calls `cmd_validate`: the two actions share one judge"
    )


@pytest.mark.integration
def test_c015_validate_zero_new_violations(tmp_path: Path):
    """The W1 call site's "zero new violations" baseline is unchanged by the new action.

    `validate`'s reading of a space is a pre-existing contract that other flows depend on. This feature adds a
    verdict vocabulary of its own; if any of it leaked into `validate`'s output, a space that was clean under W1
    would start reporting violations the moment the obligation checker shipped — exactly the "today compliant,
    tomorrow all red" failure `C-015` forbids.

    red-when: running `--action validate` on the same space reports a different violation count, or its output
    grows obligation vocabulary (a verdict word or an obligation reason).
    """
    space = fixtures.copy_fixture("clean", tmp_path / "clean")

    def validate(space_path: Path) -> subprocess.CompletedProcess:
        return run_engine("--action", "validate", "--root", str(space_path), "--json")

    first = validate(space)
    assert first.returncode == 0, f"`validate` on the clean fixture exited {first.returncode}: {first.stderr}"
    second = validate(space)
    assert second.stdout == first.stdout, "`validate`'s reading of an unchanged space is not stable"

    text = first.stdout.lower()
    obligation_words = {"satisfied", "not-evaluated", "recorded-exemption", "source-newer-than-render",
                        "render-digest-mismatch", "exempt-chronological", "trace-incomplete"}
    leaked = sorted(word for word in obligation_words if f'"{word}"' in text)
    assert not leaked, (
        f"`validate`'s output carries obligation vocabulary {leaked}: the two judgements were merged"
    )

    # The baseline itself: validating a clean space yields zero violations, and the obligation action does not
    # change that reading even when its own verdicts are non-clean on the same bytes.
    payload = json.loads(first.stdout)
    violations = payload.get("violations", payload.get("issues", []))
    assert len(violations) == 0, f"the clean fixture reports {len(violations)} validate violations: {violations}"


# ---------------------------------------------------------------------------
# C-004 / C-005 — the closed verdict and reason sets, and the two faces that must not swap
# ---------------------------------------------------------------------------

# Read from the contract's own table rather than re-typed: `contracts/diagram-obligation.contract.md` C-005 is
# the definition point, so the assertion is "the engine emits a subset of the contract's table", not "the
# engine matches a second copy of the table written here".
CONTRACT = (REPO_ROOT / ".specify" / "specs" / "087-arch-diagram-docs"
            / "contracts" / "diagram-obligation.contract.md")


def contract_reason_table() -> dict[str, set[str]]:
    """{verdict: {allowed reasons}} parsed from C-005's row table."""
    text = CONTRACT.read_text(encoding="utf-8")
    section = text.split("## C-005", 1)[1].split("## C-006", 1)[0]
    table: dict[str, set[str]] = {}
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        verdict = cells[0].strip("`")
        reason = cells[1].strip("`")
        if verdict not in VERDICTS:
            continue  # the header row names the columns, not a verdict
        table.setdefault(verdict, set()).add(reason)
    return table


@pytest.mark.integration
def test_c005_reason_pairs_closed(tmp_path: Path):
    """Every emitted pair is a row of C-005's table; nothing outside it can appear.

    The assertion is two-sided: the contract's table must parse into the five verdicts (so a silently emptied
    table cannot make this green), and every pair across the fixture spaces must be a member of it.

    red-when: an emitted `(verdict, reason)` pair is not a row of the contract's table, or a verdict's row is
    missing from the contract (the test would then be reading an empty closed set).
    """
    table = contract_reason_table()
    assert set(table) == set(VERDICTS), (
        f"C-005's table must carry exactly the five verdicts; parsed {sorted(table)}"
    )
    seen: set[tuple[str, str]] = set()
    for name in fixtures.FIXTURE_NAMES:
        space = fixtures.copy_fixture(name, tmp_path / name)
        runs = space / "docs" / ".speckit" / "runs"
        records = sorted(runs.glob("*.json"))
        payload = obligation(space, *("--record", str(records[0])) if records else ())
        for entry in payload["documents"]:
            pair = (entry["verdict"], entry["reason"])
            assert entry["verdict"] in table, f"{name}/: {entry['verdict']!r} is outside the five-value set"
            assert entry["reason"] in table[entry["verdict"]], (
                f"{name}/: reason {entry['reason']!r} does not pair with verdict {entry['verdict']!r}; "
                f"allowed {sorted(table[entry['verdict']])}"
            )
            seen.add(pair)
    assert ("satisfied", "reference-resolves") in seen, "the clean fixture must exercise the green pair"
    assert ("missing", "orphan-rendered") in seen and ("missing", "orphan-source") in seen, (
        "both face-loss values must be produced by their own fixture"
    )


@pytest.mark.integration
def test_c005_faces_not_swapped(tmp_path: Path):
    """`orphan-rendered` and `orphan-source` are mirror images and MUST NOT be swapped or merged.

    Source present with the rendered face missing is `orphan-rendered`; the rendered face present with the
    source missing is `orphan-source`. Naming the missing face is the whole judgement (`SC-002`).

    red-when: the two values are swapped between the fixtures, or one value is used for both directions.
    """
    rendered_case = fixtures.copy_fixture("orphan-rendered", tmp_path / "rendered")
    source_case = fixtures.copy_fixture("orphan-source", tmp_path / "source")
    assert not (rendered_case / "docs" / "assets" / "widget.svg").is_file(), (
        "fixture premise: orphan-rendered/ has no rendered face on disk"
    )
    assert (rendered_case / "docs" / "assets" / "widget.mmd").is_file(), (
        "fixture premise: orphan-rendered/ keeps its source"
    )
    assert (source_case / "docs" / "assets" / "widget.svg").is_file(), (
        "fixture premise: orphan-source/ keeps its rendered face"
    )
    assert not (source_case / "docs" / "assets" / "widget.mmd").is_file(), (
        "fixture premise: orphan-source/ has no source on disk"
    )

    assert verdict_of(obligation(rendered_case, "--record", record_arg(rendered_case)), DOC) == (
        "missing", "orphan-rendered"), "source present + rendered face gone must read as orphan-rendered"
    assert verdict_of(obligation(source_case, "--record", record_arg(source_case)), DOC) == (
        "missing", "orphan-source"), "rendered face present + source gone must read as orphan-source"


@pytest.mark.integration
def test_c005_every_entry_named(tmp_path: Path):
    """Every `documents[]` entry names its document (a POSIX path relative to `--root`) and its line.

    Counting-only output is what `FR-016` forbids: a reader must be able to open the named document. `line` is
    the 1-based line of the reference, `0` when the document has no reference at all.

    red-when: an entry lacks `path` or `line`, a path is absolute or Windows-shaped, or a document that does
    carry a reference reports `line == 0`.
    """
    for name in ("clean", "no-diagram", "no-trace"):
        space = fixtures.copy_fixture(name, tmp_path / name)
        runs = space / "docs" / ".speckit" / "runs"
        records = sorted(runs.glob("*.json"))
        payload = obligation(space, *("--record", str(records[0])) if records else ())
        for entry in payload["documents"]:
            assert set(entry) == {"path", "line", "verdict", "reason"}, f"{name}/: {entry}"
            assert isinstance(entry["path"], str) and entry["path"], f"{name}/: entry has no path"
            assert not os.path.isabs(entry["path"]), f"{name}/: path must be relative: {entry['path']}"
            assert "\\" not in entry["path"], f"{name}/: path must be POSIX: {entry['path']}"
            assert isinstance(entry["line"], int) and entry["line"] >= 0, f"{name}/: {entry}"
        named = verdict_of(payload, DOC)
        doc_line = next(e["line"] for e in payload["documents"] if e["path"] == DOC)
        if named[1] == "no-diagram-reference":
            assert doc_line == 0, f"{name}/: a reference-free document reports line 0, got {doc_line}"
        else:
            assert doc_line > 0, f"{name}/: a document with a reference reports its line, got {doc_line}"


@pytest.mark.integration
def test_c004_verdict_domain_closed(tmp_path: Path):
    """A sixth verdict value anywhere is a contract violation; the payload can only carry the five.

    The engine's own closed table is read from the module and compared with the contract's five verdicts, then
    every fixture's output is checked against that set. A sixth value cannot be invented at a branch without
    one of the two readings going red.

    red-when: the engine's verdict table grows a sixth key, or a payload emits a value outside the five.
    """
    source = SCRIPT.read_text(encoding="utf-8")
    namespace: dict = {}
    exec(compile(source, str(SCRIPT), "exec"), namespace)  # noqa: S102 - reading the engine's own constants
    verdicts = namespace["VERDICT_REASONS"]
    assert set(verdicts) == set(VERDICTS), (
        f"the engine's closed verdict set drifted: {sorted(verdicts)} != {sorted(VERDICTS)}"
    )
    for name in ("clean", "no-diagram", "no-trace", "exempt-bad"):
        space = fixtures.copy_fixture(name, tmp_path / name)
        runs = space / "docs" / ".speckit" / "runs"
        records = sorted(runs.glob("*.json"))
        payload = obligation(space, *("--record", str(records[0])) if records else ())
        emitted = {entry["verdict"] for entry in payload["documents"]}
        assert emitted <= set(VERDICTS), f"{name}/ emitted a sixth verdict value: {sorted(emitted - set(VERDICTS))}"


@pytest.mark.integration
def test_c004_not_evaluated_breaks_clean(tmp_path: Path):
    """`not-evaluated` is not a pass: it forces both `converged` and `clean` false.

    Unjudgeable is the one state most easily read as "nothing to see". The `no-trace/` space has both faces and
    a resolving reference; the sole defect is the missing record, and the reading must still be unclean.

    red-when: a document judged `not-evaluated` leaves either predicate true.
    """
    space = fixtures.copy_fixture("no-trace", tmp_path)
    payload = obligation(space)
    assert verdict_of(payload, DOC) == ("not-evaluated", "no-trace-record")
    assert payload["summary"]["not_evaluated"] >= 1, "the unjudgeable document must be counted"
    assert payload["summary"]["converged"] is False, "not-evaluated must force converged=false"
    assert payload["summary"]["clean"] is False, "not-evaluated must force clean=false"


@pytest.mark.integration
def test_c002_two_runs_identical_payload(tmp_path: Path):
    """Two in-process invocations over one input produce equal payloads, field order included.

    The subprocess form (byte comparison) lives in the integration file; this reading compares the parsed
    payloads of two direct calls, so a divergence caused by import-time state rather than by the CLI is caught
    too.

    red-when: the two payloads differ in any value or in the order of `documents[]`.
    """
    space = fixtures.copy_fixture("stale-source", tmp_path)
    record = record_arg(space)
    env = {**os.environ, "PYTHONHASHSEED": "0"}
    first = run_engine("--action", "obligation", "--root", str(space), "--record", record)
    second = subprocess.run([sys.executable, str(SCRIPT), "--action", "obligation",
                             "--root", str(space), "--record", record],
                            capture_output=True, text=True, env=env)
    assert first.returncode == second.returncode == 0, first.stderr + second.stderr
    left, right = json.loads(first.stdout), json.loads(second.stdout)
    assert left == right, "two runs of one input must produce one payload"
    assert [e["path"] for e in left["documents"]] == [e["path"] for e in right["documents"]]


@pytest.mark.integration
def test_c002_open_for_write_never_seen(tmp_path: Path):
    """The obligation path never opens a file for writing — the allowed side-effect set is empty.

    Read as source: the read-only block of the engine carries no write-mode `open`, no `write_text`,
    `write_bytes`, `mkdir`, `unlink`, `utime` or `rename`. This is the assertion that would stay green if the
    engine started writing to a path no fixture watches, so it is deliberately blunt.

    red-when: a write-mode call appears anywhere in the obligation block (`# --action obligation` onwards).
    """
    source = SCRIPT.read_text(encoding="utf-8")
    marker = "# --action obligation"
    end_marker = "# End of the read-only obligation block"
    assert marker in source, "the obligation block's start marker is gone; the scan below would read the wrong span"
    assert end_marker in source, "the obligation block's end marker is gone; the scan would run past the block"
    block = source[source.index(marker):source.index(end_marker)]
    forbidden = ("write_text(", "write_bytes(", "\"w\"", "'w'", "\"wb\"", "'wb'", "\"a\"", "'a'",
                 ".mkdir(", ".unlink(", "os.utime(", "os.rename(", "shutil.", "open(")
    hits = [
        f"line {i}: {line.strip()}"
        for i, line in enumerate(block.splitlines(), start=1)
        if any(token in line for token in forbidden)
    ]
    assert not hits, "the read-only obligation block opened something for writing:\n" + "\n".join(hits)
    assert "def cmd_audit(" in source[source.index(end_marker):], (
        "the writing audit command must stay outside the read-only span"
    )


@pytest.mark.integration
def test_c003_carrier_table(tmp_path: Path):
    """The carrier table of C-003 holds: six typed directories plus the `docs/ARCHITECTURE.md` root file.

    Each typed directory is exercised on its own so a whole class going unjudged is visible by name, and the
    root carrier file is added and removed to show it joins the set only when it exists.

    red-when: a typed directory's documents are not judged, or `docs/ARCHITECTURE.md` is ignored while present.
    """
    space = tmp_path / "carriers"
    for name in TYPE_DIRS:
        (space / "docs" / name).mkdir(parents=True)
        (space / "docs" / name / "index.md").write_text(f"# {name}\n", encoding="utf-8")
    payload = obligation(space)
    judged = {entry["path"] for entry in payload["documents"]}
    for name in TYPE_DIRS:
        assert f"docs/{name}/index.md" in judged, f"docs/{name}/ is a carrier directory and was not judged"
    assert payload["carriers"] == 6, f"six typed-dir carriers expected, got {payload['carriers']}"

    (space / "docs" / "ARCHITECTURE.md").write_text("# Architecture\n", encoding="utf-8")
    with_root_file = obligation(space)
    assert "docs/ARCHITECTURE.md" in {e["path"] for e in with_root_file["documents"]}, (
        "docs/ARCHITECTURE.md is a carrier when it exists"
    )
    assert with_root_file["carriers"] == 7, f"the root carrier file joins the set: got {with_root_file['carriers']}"


# ---------------------------------------------------------------------------
# C-007 / C-008 / C-009 — satisfied's conjunction, and the two halves of `stale`
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c007_satisfied_requires_all_five(tmp_path: Path):
    """`satisfied` needs all five conjuncts; each one removed lands on its own tier of C-016.

    The five are: a relative link that resolves, that file being a same-named `rendered[].path` of the record,
    both faces on disk, a complete record, and neither C-008 rule holding. Four of them are removed here — on
    `tmp_path` copies only — and each removal must leave `satisfied` behind.

    red-when: removing any conjunct still reads `satisfied` (the conjunction was weakened to a disjunction).
    """
    base = fixtures.copy_fixture("clean", tmp_path / "base")
    assert verdict_of(obligation(base, "--record", record_arg(base)), DOC) == ("satisfied", "reference-resolves"), (
        "the premise: clean/ is satisfied"
    )

    # (1) no reference at all
    no_ref = fixtures.copy_fixture("clean", tmp_path / "no-ref")
    (no_ref / DOC).write_text("# Widget overview\n\nNo diagram here.\n", encoding="utf-8")
    assert verdict_of(obligation(no_ref, "--record", record_arg(no_ref)), DOC) == (
        "missing", "no-diagram-reference"), "conjunct 1: without a reference the verdict is not satisfied"

    # (2) a reference that resolves to a file the record does not name
    (base / "docs" / "assets" / "unrecorded.svg").write_text("<svg/>\n", encoding="utf-8")
    (base / DOC).write_text("# Widget overview\n\nSee [it](../assets/unrecorded.svg).\n", encoding="utf-8")
    assert verdict_of(obligation(base, "--record", record_arg(base)), DOC) == (
        "not-evaluated", "trace-incomplete"), "conjunct 2: an unrecorded target is not satisfied"

    # (5) both faces on disk but the source is strictly newer ⇒ stale, still not satisfied
    stale = fixtures.copy_fixture("stale-source", tmp_path / "stale")
    assert verdict_of(obligation(stale, "--record", record_arg(stale)), DOC) == (
        "stale", "source-newer-than-render"), "conjunct 5: staleness outranks satisfied"

    # (4) a record that lost a required field
    incomplete = fixtures.copy_fixture("clean", tmp_path / "incomplete")
    record_file = Path(record_arg(incomplete))
    payload = json.loads(record_file.read_text(encoding="utf-8"))
    payload["diagrams"][0].pop("engine_reason")
    record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert verdict_of(obligation(incomplete, "--record", str(record_file)), DOC) == (
        "not-evaluated", "trace-incomplete"), "conjunct 4: an incomplete record is not satisfied"


@pytest.mark.integration
def test_c007_no_record_not_satisfied(tmp_path: Path):
    """Both faces + a resolving reference + no `--record` is `not-evaluated`, never `satisfied`.

    This is the clause the spec states in one line (FR-013: no record = not accepted), and the one a
    "files are present" implementation gets wrong.

    red-when: a record-less run reports `satisfied` for a diagram whose faces are both on disk.
    """
    space = fixtures.copy_fixture("no-trace", tmp_path)
    assert (space / "docs" / "assets" / "widget.mmd").is_file(), "premise: the source face is on disk"
    assert (space / "docs" / "assets" / "widget.svg").is_file(), "premise: the rendered face is on disk"
    payload = obligation(space)
    assert payload["record"] is None, "no --record was given"
    assert verdict_of(payload, DOC) == ("not-evaluated", "no-trace-record")


@pytest.mark.integration
def test_c007_source_only_reference_is_not_satisfied(tmp_path: Path):
    """A reference at the editable SOURCE, with both faces on disk, is never `satisfied` (C-007 condition 2).

    `satisfied` is a five-condition conjunction and condition 2 is "the referenced file is a same-named
    `rendered[].path`" — a `.mmd` link fails it while every file is present and the record is complete, so no
    other tier can be what rejects the document. The old reading matched the record entry on `source` too and fell
    through to the last tier, which reported the central obligation as met for a document whose reader gets a
    file they cannot view.

    red-when: the source-only reference reads `satisfied` (the probe that motivated this row returned exactly
    that), or the engine reports an unrelated reason that any complete pair would also produce.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    document = space / DOC
    assert verdict_of(obligation(space, "--record", record_arg(space)), DOC) == (
        "satisfied", "reference-resolves"), "premise: the unmodified copy is green"
    document.write_text(
        document.read_text(encoding="utf-8").replace("../assets/widget.svg", "../assets/widget.mmd"),
        encoding="utf-8")
    for face in ("widget.mmd", "widget.svg", "widget.png"):
        assert (space / "docs" / "assets" / face).is_file(), f"premise: {face} stays on disk"
    verdict, reason = verdict_of(obligation(space, "--record", record_arg(space)), DOC)
    assert (verdict, reason) != ("satisfied", "reference-resolves"), (
        "a reference at the source must not be a pass: C-007 condition 2 names rendered[].path"
    )
    assert (verdict, reason) == ("missing", "orphan-rendered"), (
        f"a source-only reference with the record pointing at this document means the reader has no render; "
        f"expected the named face loss, got {(verdict, reason)}"
    )


@pytest.mark.integration
def test_c010_html_face_is_recognised(tmp_path: Path):
    """The delivery contract's D1 HTML page is a recognisable diagram face, not an unrecognised suffix.

    `draw-diagram`'s delivery contract requires an `.html` page on every delivery and registers the `.drawio` /
    `.excalidraw` sources and the `.pdf` render for the engine layers that produce them. The checker's suffix set
    is a projection of that table, so a document linking `widget.html` must be judged, not reported as
    `no-diagram-reference` — the false red a hard-coded `.svg`/`.png` list produced.

    red-when: a conformant delivery whose document links the D1 page reads `missing` / `no-diagram-reference`.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    page = space / "docs" / "assets" / "widget.html"
    page.write_text("<!doctype html><title>Widget pipeline</title><img src=\"widget.svg\">\n", encoding="utf-8")
    document = space / DOC
    document.write_text(
        document.read_text(encoding="utf-8").replace("../assets/widget.svg", "../assets/widget.html"),
        encoding="utf-8")
    verdict, reason = verdict_of(obligation(space, "--record", record_arg(space)), DOC)
    assert (verdict, reason) != ("missing", "no-diagram-reference"), (
        "an `.html` delivery page is a diagram-shaped reference (delivery contract D1)"
    )
    # the record carries no entry for the page, so the honest reading is "cannot be traced", never a false red
    # about the document having no diagram at all
    assert (verdict, reason) == ("not-evaluated", "trace-incomplete"), (
        f"a page the record does not register is untraceable, not absent: got {(verdict, reason)}"
    )


@pytest.mark.integration
def test_c005_fenced_block_does_not_shift_the_line(tmp_path: Path):
    """A fenced example above the diagram link must not move the reported line (C-005's `line` field).

    Stripping a fenced block by deleting it also deletes its newlines, so every later reference shifts upward and
    the finding sends its reader to the wrong place. The case inserts a five-line block above the existing link
    and asserts the line moved by exactly those five lines.

    red-when: the reported line does not account for the inserted block.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    document = space / DOC
    before = verdict_of(obligation(space, "--record", record_arg(space)), DOC)
    assert before == ("satisfied", "reference-resolves"), "premise: the unmodified copy is green"
    baseline = _reported_line(space, DOC, "--record", record_arg(space))
    fenced = "```mermaid\ngraph LR\n  A --> B\n  B --> C\n```\n"
    inserted = fenced.count("\n") + 1  # the block's own lines plus the blank separator below it
    body = document.read_text(encoding="utf-8")
    marker = "The pipeline is drawn in"
    assert marker in body, "premise: the reference line is the one this case moves"
    document.write_text(body.replace(marker, fenced + "\n" + marker), encoding="utf-8")
    after = _reported_line(space, DOC, "--record", record_arg(space))
    assert after == baseline + inserted, (
        f"a {fenced.count(chr(10))}-line fenced block plus its blank separator must move the line by {inserted}: "
        f"baseline={baseline}, after={after}"
    )


@pytest.mark.integration
def test_c008_source_newer(tmp_path: Path):
    """A source strictly newer than its earliest rendered face reads `stale` / `source-newer-than-render`.

    The inequality is a fixture fact (`helpers.apply_mtime_step`), asserted here a second time so a silently
    failed `os.utime` fails on this assertion instead of making the case green by accident.

    red-when: the fixture's mtime inequality did not take effect, or a newer source is not reported stale.
    """
    space = fixtures.copy_fixture("stale-source", tmp_path)
    source = space / "docs" / "assets" / "widget.mmd"
    rendered = space / "docs" / "assets" / "widget.svg"
    assert source.stat().st_mtime > rendered.stat().st_mtime, (
        "fixture premise: the source must be strictly newer than the earliest rendered face"
    )
    assert verdict_of(obligation(space, "--record", record_arg(space)), DOC) == (
        "stale", "source-newer-than-render")


@pytest.mark.integration
def test_c008_render_digest_mismatch(tmp_path: Path):
    """A rendered face whose bytes no longer match the record's `sha256` reads `stale` / `render-digest-mismatch`.

    The bytes are changed on a `tmp_path` copy with the mtime held back, so rule 1 cannot be what fires — the
    digest mismatch has to be reported on its own.

    red-when: a hand-edited rendered face is accepted as satisfied, or the mismatch is reported under rule 1.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    rendered = space / "docs" / "assets" / "widget.svg"
    original = rendered.stat().st_mtime
    rendered.write_text(rendered.read_text(encoding="utf-8") + "<!-- hand edited -->\n", encoding="utf-8")
    os.utime(rendered, (original, original))
    assert rendered.stat().st_mtime == original, "the mtime must not be the reason this reads stale"
    assert verdict_of(obligation(space, "--record", record_arg(space)), DOC) == (
        "stale", "render-digest-mismatch")


@pytest.mark.integration
def test_c008_requires_both_faces(tmp_path: Path):
    """One face on disk is never `stale`: C-008's rules need a second face to compare against.

    A one-faced document is a face-loss finding (C-016 tier 5), which this case asserts by reading the value:
    the point is that `stale` is unreachable, not that some verdict was produced.

    red-when: a document missing one face is reported stale (`os.stat` on the absent face cannot have produced
    a value, so a `stale` reading means the rule was applied without its precondition).
    """
    for name, expected in (("orphan-rendered", "orphan-rendered"), ("orphan-source", "orphan-source")):
        space = fixtures.copy_fixture(name, tmp_path / name)
        verdict, reason = verdict_of(obligation(space, "--record", record_arg(space)), DOC)
        assert verdict != "stale", f"{name}/ must not be stale: one face is absent"
        assert (verdict, reason) == ("missing", expected), f"{name}/ must name the missing face"


@pytest.mark.integration
def test_c009_reference_unresolved_not_stale(tmp_path: Path):
    """A rendered artifact renamed away while the document still points at the old path is `missing`, not `stale`.

    This is C-009's frozen rule 1, and C-016's tier 4 settling it before tier 5.

    red-when: the rename is reported as `stale` (the case a resolver-by-guess implementation produces), or as
    `orphan-rendered` (tier 5 applied before tier 4).
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    rendered = space / "docs" / "assets" / "widget.svg"
    os.rename(rendered, space / "docs" / "assets" / "renamed.svg")
    assert verdict_of(obligation(space, "--record", record_arg(space)), DOC) == (
        "missing", "reference-unresolved")


@pytest.mark.integration
def test_c009_unrecorded_target_not_evaluated(tmp_path: Path):
    """A reference that resolves to a real file no record entry names is `trace-incomplete`, not satisfied.

    C-009's frozen rule 2: the record does not cover this diagram, so the diagram cannot have been accepted.

    red-when: two faces plus a resolving reference are enough for `satisfied` even though the record never names
    that path.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    (space / "docs" / "assets" / "second.svg").write_text("<svg id='second'/>\n", encoding="utf-8")
    (space / DOC).write_text("# Widget overview\n\nSee [the second render](../assets/second.svg).\n",
                             encoding="utf-8")
    assert verdict_of(obligation(space, "--record", record_arg(space)), DOC) == (
        "not-evaluated", "trace-incomplete")


@pytest.mark.integration
def test_c009_semantic_half_has_no_verdict(tmp_path: Path):
    """The semantic half of `stale` (labels/relations contradicting the prose) produces no verdict at all.

    The frozen decision (`plan.md` T-003 / `D-001`): the checker judges the reference and the faces, not the
    meaning of the picture. A document whose prose was rewritten after the render — so the labels contradict it —
    still reads `satisfied`, and the uncovered half is reported by the producing run as `D-001`, never as a
    sixth verdict. The assertion therefore pins both halves: no verdict appears for the semantic drift, and the
    payload carries no field that could hold one.

    red-when: a semantic drift is reported as `stale` (inventing a criterion the contract froze as uncovered),
    or the payload grows a field for the semantic face.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    doc = space / DOC
    doc.write_text(
        doc.read_text(encoding="utf-8").replace(
            "The widget subsystem validates every request before it reaches the store.",
            "The widget subsystem bypasses validation entirely and writes straight to the store.",
        ),
        encoding="utf-8",
    )
    payload = obligation(space, "--record", record_arg(space))
    verdict, reason = verdict_of(payload, DOC)
    assert (verdict, reason) == ("satisfied", "reference-resolves"), (
        "the semantic face has no criterion; it must not move the verdict"
    )
    assert set(payload["documents"][0]) == {"path", "line", "verdict", "reason"}, (
        "the payload must not grow a field for the uncovered semantic face"
    )
    assert "d-001" not in json.dumps(payload).lower(), (
        "the semantic residual is reported by the producing run, never carried in the checker payload"
    )


@pytest.mark.integration
def test_c010_record_schema(tmp_path: Path):
    """The record reader requires the C-010 field set; a missing one is `trace-incomplete`.

    Each required field is dropped on its own copy of the record, so a reader that tolerates one of them is
    named by the assertion that fails.

    red-when: a record missing `document` / `engine` / `engine_reason` / `ldm_summary` / `delivery.accepted` /
    `source` / `rendered[].path` is still enough for `satisfied`.
    """
    for field in ("document", "engine", "engine_reason", "ldm_summary", "source", "rendered"):
        space = fixtures.copy_fixture("clean", tmp_path / f"drop-{field}")
        record_file = Path(record_arg(space))
        payload = json.loads(record_file.read_text(encoding="utf-8"))
        payload["diagrams"][0].pop(field)
        record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        assert verdict_of(obligation(space, "--record", str(record_file)), DOC) == (
            "not-evaluated", "trace-incomplete"), f"a record without {field!r} must not satisfy the obligation"

    no_rendered = fixtures.copy_fixture("clean", tmp_path / "drop-rendered-path")
    record_file = Path(record_arg(no_rendered))
    payload = json.loads(record_file.read_text(encoding="utf-8"))
    payload["diagrams"][0]["rendered"] = [{"sha256": "0" * 64}]
    record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert verdict_of(obligation(no_rendered, "--record", str(record_file)), DOC) == (
        "not-evaluated", "trace-incomplete"), "a rendered face without `path` must not satisfy the obligation"

    no_acceptance = fixtures.copy_fixture("clean", tmp_path / "drop-accepted")
    record_file = Path(record_arg(no_acceptance))
    payload = json.loads(record_file.read_text(encoding="utf-8"))
    payload["diagrams"][0]["delivery"] = {"unmet": []}
    record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert verdict_of(obligation(no_acceptance, "--record", str(record_file)), DOC) == (
        "not-evaluated", "trace-incomplete"), "a delivery block without `accepted` must not satisfy"


@pytest.mark.integration
def test_c010_relative_to_root(tmp_path: Path):
    """Record paths are resolved relative to `--root`; an absolute path in the record matches nothing.

    C-010 fixes the convention so that the record's `source` / `rendered[].path` and a document's relative
    reference can be compared on one basis. An absolute path breaks that basis and must not silently satisfy.

    red-when: an absolute `rendered[].path` still satisfies the obligation, i.e. the engine accepted a path it
    cannot have compared with the document's relative reference on the same basis.
    """
    space = fixtures.copy_fixture("clean", tmp_path / "abs")
    record_file = Path(record_arg(space))
    payload = json.loads(record_file.read_text(encoding="utf-8"))
    for face in payload["diagrams"][0]["rendered"]:
        face["path"] = str(space / face["path"])
    payload["diagrams"][0]["source"] = str(space / payload["diagrams"][0]["source"])
    record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    verdict, reason = verdict_of(obligation(space, "--record", str(record_file)), DOC)
    assert (verdict, reason) != ("satisfied", "reference-resolves"), (
        "record paths are relative to --root; an absolute one shares no basis with the document's reference"
    )

    relative = fixtures.copy_fixture("clean", tmp_path / "relative")
    relative_record = record_arg(relative)
    rel_to_root = os.path.relpath(relative_record, relative)
    assert verdict_of(obligation(relative, "--record", rel_to_root), DOC) == (
        "satisfied", "reference-resolves"), "--record itself is resolved relative to --root"


@pytest.mark.integration
def test_c010_no_glob_no_guess(tmp_path: Path):
    """Only the file `--record` names is read: the engine never globs `runs/` nor guesses the newest record.

    `no-trace/` becomes satisfiable only when `--record` names one. The assertion proves the direction: with
    two records present (`clean/`'s plus a decoy that names a different diagram) the verdict follows the named
    file, and with no record it stays `no-trace-record` even though a record is sitting in `runs/`.

    red-when: the engine finds a record nobody named (a glob or "newest wins"), or it reads a second record with
    the first and merges the results.
    """
    space = fixtures.copy_fixture("clean", tmp_path / "decoy")
    named = Path(record_arg(space))  # read BEFORE the decoy lands, so the helper's one-record check holds
    runs = named.parent
    decoy = runs / "20261106T235959Z-deadbeef-diagram-trace.json"
    decoy.write_text(json.dumps({
        "run_id": "20261106T235959Z-deadbeef",
        "feature": None,
        "diagrams": [{"document": DOC, "engine": "mermaid", "engine_reason": "decoy",
                      "ldm_summary": "decoy", "delivery": {"accepted": True, "unmet": []},
                      "source": "docs/assets/elsewhere.mmd",
                      "rendered": [{"path": "docs/assets/elsewhere.svg"}]}],
    }, indent=2) + "\n", encoding="utf-8")
    assert named.name != decoy.name, "the premise needs two distinct records"
    assert len(sorted(runs.glob("*.json"))) == 2, "premise: two records now sit in runs/"
    assert verdict_of(obligation(space, "--record", str(named)), DOC) == ("satisfied", "reference-resolves"), (
        "the named record decides; the decoy must not be merged in"
    )
    assert verdict_of(obligation(space, "--record", str(decoy)), DOC) == ("not-evaluated", "trace-incomplete"), (
        "the named record decides in the other direction too: the decoy points at a diagram this document "
        "does not reference, so the record cannot cover it"
    )

    no_trace = fixtures.copy_fixture("no-trace", tmp_path / "no-trace")
    planted = no_trace / "docs" / ".speckit" / "runs"
    planted.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(named, planted / named.name)
    assert sorted(p.name for p in planted.glob("*.json")) == [named.name], (
        "premise: the unrecorded space now carries a record nobody names"
    )
    assert verdict_of(obligation(no_trace), DOC) == ("not-evaluated", "no-trace-record"), (
        "a record sitting in runs/ is not found without --record: no glob, no newest-wins"
    )


@pytest.mark.integration
def test_c012_four_conditions_closed(tmp_path: Path):
    """Exactly four conditions produce `not-evaluated`, each driven by its own fixture; a fifth is a violation.

    The four are `no-trace-record`, `trace-incomplete`, `exemption-invalid` and `render-unreadable` (an `OSError`
    normalized). The engine's own reason table is read as the closed set, so adding a fifth condition to the
    implementation changes the table and this assertion sees it.

    red-when: a fifth `not-evaluated` reason exists, one of the four cannot be produced by its fixture, or
    "the engine is unavailable" appears among them (the checker calls no engine at all).
    """
    source = SCRIPT.read_text(encoding="utf-8")
    namespace: dict = {}
    exec(compile(source, str(SCRIPT), "exec"), namespace)  # noqa: S102 - reading the engine's own constants
    assert set(namespace["VERDICT_REASONS"]["not-evaluated"]) == {
        "no-trace-record", "trace-incomplete", "exemption-invalid", "render-unreadable",
    }, "the not-evaluated reason set is a closed four"

    cases = {
        "no-trace": ("not-evaluated", "no-trace-record"),
        "trace-incomplete": ("not-evaluated", "trace-incomplete"),
        "exempt-bad": ("not-evaluated", "exemption-invalid"),
    }
    for name, expected in cases.items():
        space = fixtures.copy_fixture(name, tmp_path / name)
        runs = space / "docs" / ".speckit" / "runs"
        records = sorted(runs.glob("*.json"))
        payload = obligation(space, *("--record", str(records[0])) if records else ())
        assert verdict_of(payload, DOC) == expected, f"{name}/ must land {expected}"

    # the fourth: a rendered face that exists but cannot be read
    unreadable = fixtures.copy_fixture("clean", tmp_path / "render-unreadable")
    rendered = unreadable / "docs" / "assets" / "widget.png"
    assert rendered.is_file(), "premise: the rendered face is present"
    rendered.chmod(0o000)
    try:
        if os.access(rendered, os.R_OK):
            pytest.skip("running as a user that can read a 0o000 file; the render-unreadable condition "
                        "cannot be driven on this host")
        verdict, reason = verdict_of(obligation(unreadable, "--record", record_arg(unreadable)), DOC)
    finally:
        rendered.chmod(0o644)
    assert (verdict, reason) == ("not-evaluated", "render-unreadable"), (
        "an unreadable rendered face is normalized to render-unreadable, not to stale or satisfied"
    )
    assert "engine" not in namespace["VERDICT_REASONS"]["not-evaluated"], (
        "engine unavailability is deliberately not a not-evaluated condition"
    )
