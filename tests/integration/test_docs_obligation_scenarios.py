"""Integration tests: `--action obligation` end-to-end scenarios (spec 087).

Owner of the assertion names and of each assertion's red-when condition: `plan.md` § Test Plan table A (rows
`C-002`, `C-006`, `C-011`, `C-012` and the `C-008a` rows of table B). Every case runs the engine as a
subprocess against a `tmp_path` copy of a fixture space, so nothing this file does can touch the repository
copy of a fixture — that invariant is the whole reason `tests/fixtures/docs-obligation/conftest.py::copy_fixture`
exists.

Read-only is asserted the way a reader can check it: run the engine, then ask git whether the space moved.
"""
from __future__ import annotations

import importlib.util
import json
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

DOC = "docs/concepts/widget-overview.md"


def run_engine(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
    )


def record_arg(space: Path) -> str:
    """The one trace-record file a fixture ships, as an absolute `--record` value."""
    runs = space / "docs" / ".speckit" / "runs"
    names = sorted(p.name for p in runs.glob("*.json"))
    assert len(names) == 1, f"expected exactly one trace record in {runs}, got {names}"
    return str(runs / names[0])


GIT_ENV = {
    "PATH": "/usr/bin:/bin",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_AUTHOR_NAME": "fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
}


def git_baseline(space: Path) -> None:
    """Turn the space into a throwaway repository whose HEAD is the pre-run state."""
    subprocess.run(["git", "init", "-q"], cwd=space, check=True, capture_output=True, env=GIT_ENV)
    subprocess.run(["git", "add", "-A"], cwd=space, check=True, capture_output=True, env=GIT_ENV)
    subprocess.run(["git", "commit", "-qm", "fixture baseline"], cwd=space, check=True,
                   capture_output=True, env=GIT_ENV)


def git_status(space: Path) -> str:
    """`git status --porcelain` for the space — did the engine's run change any byte?

    The space lives under a `tmp_path`, outside the repository, so it is its own throwaway repository: that
    is exactly the question this assertion asks. `git_baseline` commits once; this helper only reads.
    """
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=space, capture_output=True,
                          text=True, env=GIT_ENV, check=True)
    return proc.stdout


def obligation(space: Path, *extra: str) -> dict:
    proc = run_engine("--action", "obligation", "--root", str(space), *extra)
    assert proc.returncode == 0, f"engine exited {proc.returncode}: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# C-002 (read-only by construction) and C-006 rule 1/2 (determinism, idempotence)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c002_two_runs_identical_json(tmp_path: Path):
    """Two runs over one input produce byte-identical stdout, and neither run moves a byte on disk.

    red-when: the two payloads differ in any byte (ordering, field set, a timestamp leaking into the output),
    or the space is dirty after either run.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = record_arg(space)
    git_baseline(space)
    assert git_status(space) == "", "the fixture baseline commit must leave a clean tree"

    first = run_engine("--action", "obligation", "--root", str(space), "--record", record)
    after_first = git_status(space)
    second = run_engine("--action", "obligation", "--root", str(space), "--record", record)
    after_second = git_status(space)

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout, "two runs of one input must serialise identically"
    assert after_first == "", f"the first run wrote to the space: {after_first!r}"
    assert after_second == "", f"the second run wrote to the space: {after_second!r}"


@pytest.mark.integration
def test_c002_no_writes_on_dirty_fixture(tmp_path: Path):
    """A space that is already dirty is judged without the engine adding to the dirt.

    The dirty state is deliberate: an unjudgeable extra carrier plus an unreadable exemption record. Whatever
    the engine decides, it decides read-only.

    red-when: `git status --porcelain` grows after the run — the engine created, modified or deleted a file.
    """
    space = fixtures.copy_fixture("exempt-bad", tmp_path)
    git_baseline(space)
    (space / "docs" / "concepts" / "extra.md").write_text(
        "# Extra carrier\n\nStill no diagram here.\n", encoding="utf-8")
    before = git_status(space)
    assert before != "", "this case needs a dirty baseline to be meaningful"

    obligation(space)
    after = git_status(space)
    assert after == before, f"the engine wrote to a dirty space: before={before!r} after={after!r}"


# ---------------------------------------------------------------------------
# C-011 — exemptions are visible, and an overturned one is reported (quickstart S5)
# ---------------------------------------------------------------------------


def verdict_of(payload: dict, doc_path: str) -> tuple[str, str]:
    for entry in payload["documents"]:
        if entry["path"] == doc_path:
            return entry["verdict"], entry["reason"]
    raise AssertionError(f"{doc_path} not judged; documents={payload['documents']}")


@pytest.mark.integration
def test_c011_exempt_ok(tmp_path: Path):
    """A valid exemption record reads `recorded-exemption` and shows up as `exempted`, never as a pass.

    `exempt-ok/`'s document has no diagram at all and carries a three-field record. The reading is the lawful
    end state of FR-004: the document is exempted (visible), `clean` is false, and the exemption itself is not
    a finding awaiting convergence. The rest of the space has undiagrammed carriers, so the whole-space
    `converged` is false on those findings — the exemption is not what drives it.

    red-when: an invalid or missing record is accepted as an exemption, `exempted > 0` still yields
    `clean=true`, or the exemption is reported as `missing` (invisible instead of exempt).
    """
    space = fixtures.copy_fixture("exempt-ok", tmp_path)
    payload = obligation(space)
    summary = payload["summary"]
    assert verdict_of(payload, DOC) == ("recorded-exemption", "exempt-chronological")
    assert summary["exempted"] == 1, f"the exemption must be counted once, got {summary['exempted']}"
    assert summary["clean"] is False, "exempted > 0 ⇒ clean=false (FR-004: a recorded exemption is not a pass)"
    assert (space / "docs" / ".speckit" / "exemptions" / "concepts" / "widget-overview.md").is_file(), (
        "premise: the record lives at C-011's landing point"
    )


@pytest.mark.integration
def test_c011_exempt_bad(tmp_path: Path):
    """An exemption record missing `justification` is `not-evaluated` / `exemption-invalid`, not an exemption.

    An invalid record must be visible rather than silently passing: the document becomes unjudgeable, which is
    strictly worse than missing — the reader is told the record, not the diagram, is the problem.

    red-when: a record that fails C-011's validity test is still accepted (`recorded-exemption`), or it is
    degraded into `missing` (which would hide the broken record behind a diagram finding).
    """
    space = fixtures.copy_fixture("exempt-bad", tmp_path)
    record = space / "docs" / ".speckit" / "exemptions" / "concepts" / "widget-overview.md"
    assert "justification" not in record.read_text(encoding="utf-8"), (
        "premise: the invalid record is the one missing its justification"
    )
    payload = obligation(space)
    assert verdict_of(payload, DOC) == ("not-evaluated", "exemption-invalid")
    assert payload["summary"]["exempted"] == 0, "an invalid record is not an exemption"
    assert payload["summary"]["not_evaluated"] >= 1, "it is counted as unjudgeable"
    assert payload["summary"]["converged"] is False, "not-evaluated forces converged=false"


@pytest.mark.integration
def test_c011_superseded(tmp_path: Path):
    """A still-valid exemption whose document now resolves a render is overturned, and the count says so.

    The document carries a resolving reference, so the exemption's own reason no longer holds. That is the one
    mechanical signal FR-004 permits (`summary.exemption_superseded`), and it is reconstructed mechanically by
    removing the reference from a copy and re-judging: the same record then reads as a valid exemption again.
    That permutation is what makes the count attributable to the record-vs-fact contradiction rather than to
    the record's syntax.

    red-when: the contradiction is not reported (verdict stays `recorded-exemption`), or the superseded count
    is reached by any other route.
    """
    space = fixtures.copy_fixture("exempt-superseded", tmp_path)
    record = record_arg(space)
    payload = obligation(space, "--record", record)
    assert verdict_of(payload, DOC) == ("not-evaluated", "exemption-invalid")
    assert payload["summary"]["exemption_superseded"] == 1, (
        f"the overturned exemption must be counted once, got {payload['summary']['exemption_superseded']}"
    )
    assert payload["summary"]["converged"] is False, "an overturned exemption is unjudgeable, not converged"

    control = fixtures.copy_fixture("exempt-superseded", tmp_path / "control")
    (control / DOC).write_text("# Widget overview\n\nNo diagram reference survives here.\n", encoding="utf-8")
    control_payload = obligation(control, "--record", record_arg(control))
    assert control_payload["summary"]["exemption_superseded"] == 0, (
        "without the contradiction the record is a valid exemption, so nothing is superseded"
    )
    assert verdict_of(control_payload, DOC) == ("recorded-exemption", "exempt-chronological"), (
        "control reading: the same record is accepted once the document stops resolving a render"
    )


# ---------------------------------------------------------------------------
# C-012 — "no record" is not "no diagram": the four not-evaluated conditions end to end
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c012_no_record_not_evaluated(tmp_path: Path):
    """A diagram with both faces and a resolving reference, judged without `--record`, reads `no-trace-record`.

    This is the case a "the files are there" implementation gets wrong, and the one the plan names as this
    repository's first real reading (85 carriers, one diagram, no record): `not-evaluated` / `no-trace-record`
    and an unclean space is the correct conclusion, not a defect.

    red-when: an unrecorded diagram is satisfied, or the missing `--record` is reported as `missing`.
    """
    space = fixtures.copy_fixture("no-trace", tmp_path)
    payload = obligation(space)
    assert payload["record"] is None, "no --record was passed, so the payload must say so (null, not omitted)"
    assert verdict_of(payload, DOC) == ("not-evaluated", "no-trace-record")
    assert payload["summary"]["not_evaluated"] == 1, "exactly the diagram-carrying document is unjudgeable"
    assert payload["summary"]["converged"] is False and payload["summary"]["clean"] is False


@pytest.mark.integration
def test_c012_two_faces_resolving_but_unrecorded(tmp_path: Path):
    """The same space turns green on the verdict only when the record is supplied — nothing else changes.

    One variable: `--record`. Everything else (both faces, the reference, the record's own content) is held
    constant, so the reading is attributable to the record rather than to the fixture.

    red-when: supplying an unrelated record flips the verdict (which would mean the record is matched by
    presence rather than by the named diagram), or supplying the right one leaves it unjudgeable.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    rendered = record_arg(space)

    without = obligation(space)
    assert verdict_of(without, DOC) == ("not-evaluated", "no-trace-record"), (
        "without --record the two faces are not enough"
    )

    with_record = obligation(space, "--record", rendered)
    assert verdict_of(with_record, DOC) == ("satisfied", "reference-resolves"), (
        "the same space with the record supplied is satisfied"
    )
    assert with_record["summary"]["clean"] is False, (
        "the space's five other carriers carry no diagram, so it is not clean — the verdict moved, not the space"
    )
    scoped = obligation(space, "--record", rendered, "--only", DOC)
    assert scoped["summary"]["converged"] is True and scoped["summary"]["clean"] is True, (
        "scoped to the recorded diagram, the same reading is the green reference case"
    )


@pytest.mark.integration
def test_c012_trace_incomplete_end_to_end(tmp_path: Path):
    """A record that exists but cannot point at this diagram is `trace-incomplete`, the second of the four.

    The fixture's record names a different rendered path, so the reference resolves and both faces are on disk
    while the record still cannot cover the diagram. The reading must not degrade to `no-trace-record` (a record
    IS present) nor to `satisfied` (the record does not cover it).

    red-when: a present-but-unrelated record is treated as absent or as sufficient.
    """
    space = fixtures.copy_fixture("trace-incomplete", tmp_path)
    payload = obligation(space, "--record", record_arg(space))
    assert verdict_of(payload, DOC) == ("not-evaluated", "trace-incomplete")
    assert payload["record"] is not None, "the record was supplied; the unjudgeability is about coverage"
    assert payload["summary"]["not_evaluated"] == 1


# ---------------------------------------------------------------------------
# C-016 — the ordering, read as an ordering: the sharp case first
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c016_deleted_rendered_first(tmp_path: Path):
    """The render is gone AND the reference points at it: tier 4 wins over tier 5.

    `deleted-rendered/` holds the case the contract calls its sharpest: a decision implemented as a set test
    would report a face loss (`orphan-rendered`, tier 5) because the source is on disk and the render is not,
    while the document's reference — which points at the deleted render — settles the document one tier earlier
    as `reference-unresolved`. The sibling reading (`orphan-rendered/`'s reference pointing at the source) is
    what makes the two distinguishable at all.

    red-when: `deleted-rendered/` lands any `orphan-*` value, or the two cases stop being distinguishable.
    """
    sharp = fixtures.copy_fixture("deleted-rendered", tmp_path / "sharp")
    assert (sharp / "docs" / "assets" / "widget.mmd").is_file(), "premise: the source is on disk"
    assert not (sharp / "docs" / "assets" / "widget.svg").is_file(), "premise: the render is gone"
    assert verdict_of(obligation(sharp, "--record", record_arg(sharp)), DOC) == (
        "missing", "reference-unresolved"), "tier 4 (reference unresolved) precedes tier 5 (face loss)"

    sibling = fixtures.copy_fixture("orphan-rendered", tmp_path / "sibling")
    assert verdict_of(obligation(sibling, "--record", record_arg(sibling)), DOC) == (
        "missing", "orphan-rendered"), "with a resolving reference the same face loss is named at tier 5"
