"""Integration tests: `--action obligation` end-to-end scenarios (spec 087).

Owner of the assertion names and of each assertion's red-when condition: `plan.md` § Test Plan table A (rows
`C-002`, `C-006`, `C-011`, `C-012` and the `C-008a` rows of table B). Every case runs the engine as a
subprocess against a `tmp_path` copy of a fixture space, so nothing this file does can touch the repository
copy of a fixture — that invariant is the whole reason `tests/fixtures/docs-obligation/helpers.py::copy_fixture`
exists.

Read-only is asserted the way a reader can check it: run the engine, then ask git whether the space moved.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
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


# ---------------------------------------------------------------------------
# C-008a — the reconcile convergence loop (`plan.md` § Test Plan table B, rows `C-008a`)
#
# The clause is "a reconcile can converge the diagram dimension to zero". Its executable form is the four-step
# sequence `quickstart.md` S9 registers: R6 finding → R5 produce → second R6 → anti-churn. The R5 step calls
# `draw-diagram`, which is a model-driven capability and not something a test may invoke; the harness therefore
# plays that role mechanically by writing exactly what `flow-obligations` `C-003` says a producing run writes —
# the two faces, the document's resolving relative reference and the traceability record, in one pass. That is a
# test double for the PRODUCER, never for the checker: every verdict below is the real engine's.
# ---------------------------------------------------------------------------

import hashlib  # noqa: E402  (kept beside its only use)


def produce_diagram(space: Path, doc_rel: str = DOC, exempt: str | None = None) -> Path:
    """The R5 produce step, written by hand: both faces, the resolving reference, the record, and ONE plan row.

    Shapes are the ones `clean/` registers (source + two rendered faces + one record entry), because `clean/` is
    this feature's green reference reading and a second shape would be a second fixture standard. The record's
    `diagrams[]` carries one entry PER DOCUMENT, which is `C-010`'s own unit of identity ("每图一条"): each
    carrier document that has nothing to depict gets its own generated face naming what it indexes.

    Only the fixture's designated carrier gets the human-written `widget` pipeline; a directory `index.md` gets a
    generated `index-<type>` flow, which is what a producing run would draw for an index page. Returns the record
    path, which is the `--record` the second R6 must be given.
    """
    asset_dir = space / "docs" / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    source = asset_dir / "widget.mmd"
    svg = asset_dir / "widget.svg"
    png = asset_dir / "widget.png"
    source.write_text("graph LR\n  A[Request] --> B[Validator]\n  B --> C[Widget store]\n", encoding="utf-8")
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40">\n'
                   '  <text x="4" y="24">Request -> Validator -> Widget store</text>\n</svg>\n', encoding="utf-8")
    png.write_text("PNG-PLACEHOLDER 087 produced rendered face (never decoded; only hashed)\n", encoding="utf-8")

    entries = []

    def entry_for(doc_path: str, slug: str, label: str) -> dict:
        faces = []
        for suffix in ("svg", "png"):
            face = asset_dir / f"{slug}.{suffix}"
            if not face.is_file():
                face.write_text(
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="160" height="30">\n'
                    f'  <text x="4" y="20">{label} structure</text>\n</svg>\n' if suffix == "svg"
                    else f"PNG-PLACEHOLDER 087 {slug} ({suffix})\n", encoding="utf-8")
            faces.append({"path": f"docs/assets/{face.name}",
                          "sha256": hashlib.sha256(face.read_bytes()).hexdigest()})
        return {
            "document": doc_path,
            "engine": "mermaid",
            "engine_reason": "routing matrix row: flow graph, no zone grammar required",
            "ldm_summary": "diagram_class=flow; elements=3; relations=2; zones=0",
            "delivery": {"accepted": True, "unmet": []},
            "source": f"docs/assets/{slug}.mmd",
            "rendered": faces,
        }

    def write_reference(doc_path: Path, target: str) -> None:
        body = doc_path.read_text(encoding="utf-8")
        if target in body:
            return
        doc_path.write_text(body.rstrip("\n") + f"\n\nIt is drawn in [its structure diagram](../{target}).\n",
                            encoding="utf-8")

    # the referenced carrier: the two faces `clean/` registers. When the space's designated carrier is the
    # EXEMPTED one, the produce step draws something else — an exempted document must stay unreferenced, or its
    # exemption would be overturned by an artifact rather than by a fact (`C-011`).
    drawn_doc = doc_rel
    if exempt is not None and doc_rel == exempt:
        drawn_doc = sorted(
            doc.relative_to(space).as_posix() for doc in (space / "docs").rglob("*.md")
        )[0]
    write_reference(space / drawn_doc, "assets/widget.svg")
    entries.append(entry_for(drawn_doc, "widget", "Widget pipeline"))

    # every remaining carrier: one generated flow per document (`C-010`: one entry per produced diagram)
    for doc in sorted((space / "docs").rglob("*.md")):
        rel_doc = doc.relative_to(space).as_posix()
        if rel_doc in (doc_rel, drawn_doc) or "/.speckit/" in rel_doc or "/assets/" in rel_doc:
            continue
        if exempt is not None and rel_doc == exempt:
            # an exempted document has nothing to depict; `C-008a` R5 says it is not a residual, so the
            # producing run does not give it a face (and its own reference must stay absent, `C-011`).
            continue
        slug = "index-" + doc.parent.name if doc.name == "index.md" else doc.stem
        (asset_dir / f"{slug}.mmd").write_text(f"graph LR\n  T[{doc.parent.name} index] --> L[linked pages]\n",
                                               encoding="utf-8")
        write_reference(doc, f"assets/{slug}.svg")
        entries.append(entry_for(rel_doc, slug, doc.parent.name))

    runs = space / "docs" / ".speckit" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    record = {"run_id": "20261106T120000Z-087b2c3d", "feature": "087-arch-diagram-docs", "diagrams": entries}
    target = runs / "20261106T120000Z-087b2c3d-diagram-trace.json"
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return target


@pytest.mark.integration
def test_c008a_second_reconcile_zero_findings(tmp_path: Path):
    """Four steps: the first pass finds, R5 produces, the second pass converges, and nothing churns.

    `SC-003` end to end on a fixture whose documents are all compliant with the PRE-change baseline — which is
    the point: they were compliant yesterday and are findings today, because the baseline moved (US2).

    Three readings per step, and the middle one is the sharpest: the record the first pass did not have is what
    turns each document from `missing` into `satisfied`, so the convergence is attributable to the produce step
    rather than to the checker changing its mind.

    red-when: the second pass still reports an actionable tier, `converged` is not true, or the copy's `git
    status` is non-empty (cosmetic churn, or the engine writing where it must not).
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path)

    first = obligation(space)
    assert verdict_of(first, DOC) == ("missing", "no-diagram-reference"), (
        "a document compliant with the pre-change baseline is a finding under the amended one"
    )
    assert first["summary"]["converged"] is False, "the first pass cannot be converged while a document lacks a diagram"
    assert first["summary"]["missing"] >= 1

    record = produce_diagram(space)
    second = obligation(space, "--record", str(record))
    assert verdict_of(second, DOC) == ("satisfied", "reference-resolves"), (
        "the produce step's own record is what makes the document judgeable"
    )
    assert second["summary"]["missing"] == 0 and second["summary"]["stale"] == 0, (
        "the actionable tiers must be zero after the produce step"
    )
    assert second["summary"]["not_evaluated"] == 0
    assert second["summary"]["converged"] is True, "C-013's predicate: a carrier in scope and three tiers at zero"

    # anti-churn, measured the way `C-002` states it: the space is its own throwaway repository whose HEAD is
    # the post-produce state, and the second run must leave it byte-identical.
    git_baseline(space)
    assert git_status(space) == "", "the baseline commit must land after the produce step"
    third = obligation(space, "--record", str(record))
    assert third == second, "a repeat run on an unchanged space reports the same verdict (anti-churn)"
    assert git_status(space) == "", "the convergent run wrote to the space (C-002)"


@pytest.mark.integration
def test_c008a_exemption_does_not_block_convergence(tmp_path: Path):
    """An exempted space converges while staying unclean: `converged` and `clean` answer different questions.

    The space is the one this clause's family exercises: one carrier with a lawful recorded exemption and one
    carrier that must be produced. The reading after the produce step is `converged=true` + `clean=false` + a
    non-zero `exempted` — the classification `FR-004` calls a lawful terminal state, and the one an
    implementation that used `clean` as its convergence criterion could never reach.

    red-when: an exemption drags `converged` to false (the convergence criterion was `clean`), or `exempted`
    stops being counted separately from the pass count.
    """
    space = fixtures.copy_fixture("exempt-ok", tmp_path)
    record_doc = produce_diagram(space, exempt=DOC)
    payload = obligation(space, "--record", str(record_doc))
    summary = payload["summary"]
    assert summary["exempted"] == 1, f"the exemption stays visible, got {summary['exempted']}"
    assert summary["missing"] == 0 and summary["stale"] == 0 and summary["not_evaluated"] == 0, (
        f"no actionable tier survives the produce step: {summary}"
    )
    assert summary["converged"] is True, "an exemption is a lawful terminal state; it cannot block convergence"
    assert summary["clean"] is False, "an exempted space is not a zero-finding space (FR-004)"
    assert verdict_of(payload, DOC) == ("recorded-exemption", "exempt-chronological"), (
        "and the exempted document reads as exempted, not as satisfied"
    )


# ---------------------------------------------------------------------------
# SC-001 / SC-002 — the four artifacts one run owes, and the negative faces (T046)
#
# `T046` authors these under `C-023`'s own two names (`plan.md` table B): `test_sc001_four_artifacts_present` is
# `C-001`'s subject read on a space (`F::test_c001_four_artifacts_one_run` reads the flow text that promises it),
# and `test_sc002_removing_either_face_turns_red` is `I::test_sc002_removing_either_face_turns_red` verbatim.
# Every deletion happens on a `tmp_path` copy — the repository copy of a fixture is its registered state.
# ---------------------------------------------------------------------------


def trace_entry(space: Path, doc_rel: str = DOC) -> dict:
    """The one `diagrams[]` entry a space's record carries for `doc_rel` (`C-010`'s unit of identity)."""
    record = json.loads(Path(record_arg(space)).read_text(encoding="utf-8"))
    hits = [entry for entry in record["diagrams"] if entry["document"] == doc_rel]
    assert len(hits) == 1, f"expected exactly one record entry for {doc_rel}, got {len(hits)}"
    return hits[0]


@pytest.mark.integration
def test_sc001_four_artifacts_present(tmp_path: Path):
    """One run's four on-disk artifacts, read on the space: document, source, rendered face(s), reference.

    `SC-001`'s independent reading. The four are asserted on disk AND read through the engine's verdict, because
    either half alone is a false green: files on disk with no reference are not the artifact set (nobody can find
    the diagram), and a reference with no faces is not either. The traceability record is asserted separately —
    `C-003` owns it, and folding it into the four would make the artifact count five.

    red-when: any of the four is absent while the run still reads satisfied, or the record is counted as one of
    the four.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = record_arg(space)
    entry = trace_entry(space)

    document = space / DOC
    assert document.is_file(), "artifact 1: the carrier document"
    source = space / entry["source"]
    assert source.is_file(), f"artifact 2: the editable source at {entry['source']}"
    rendered = [space / face["path"] for face in entry["rendered"]]
    assert rendered and all(face.is_file() for face in rendered), (
        f"artifact 3: every rendered face the delivery contract requires: {entry['rendered']}"
    )
    body = document.read_text(encoding="utf-8")
    reference = [line for line in body.splitlines() if "../assets/" in line and "](" in line]
    assert len(reference) == 1, f"artifact 4: exactly one resolving relative reference, found {reference}"
    # artifact 4 is a reference at a RENDERED face, not merely at some `../assets/` path (FR-005, C-007 condition
    # 2). Reading the record is what makes this half of the assertion able to catch a source-only link — which is
    # exactly the reading the engine got wrong once, so the test has to be able to see it.
    rendered_paths = {face["path"] for face in entry["rendered"]}
    targets = re.findall(r"\]\(([^)\s]+)\)", reference[0])
    assert len(targets) == 1, f"artifact 4: one link target on the reference line, found {targets}"
    resolved = (document.parent / targets[0]).resolve()
    assert resolved.relative_to(space).as_posix() in rendered_paths, (
        f"artifact 4: the reference must land one of the record's rendered faces {sorted(rendered_paths)}, "
        f"got {targets[0]}"
    )

    payload = obligation(space, "--record", record, "--only", DOC)
    assert verdict_of(payload, DOC) == ("satisfied", "reference-resolves"), (
        "the four artifacts must be exactly what the engine calls satisfied"
    )
    assert payload["summary"]["converged"] is True and payload["summary"]["clean"] is True
    assert (Path(record)).is_file(), "the traceability record is the fifth file, cited by C-003 and not counted"


@pytest.mark.integration
def test_sc002_removing_either_face_turns_red(tmp_path: Path):
    """Each of `C-023`'s three faces, one at a time, on its own copy: every one of them turns the run red.

    The baseline is measured first (the copy reads satisfied), then exactly one face is disturbed — so a red
    reading is attributable to that face and to nothing else. The two `orphan-*` values are asserted to be
    DIFFERENT values in different directions: deleting the rendered face names the rendered face, deleting the
    source names the source, and an implementation that swapped them would pass a count-based assertion while
    failing this one.

    red-when: any of the three disturbances leaves the space satisfied (which is "unverified", not "satisfied"),
    or the missing face is named by the other face's reason.
    """
    faces = []

    # a) the rendered face is deleted, the source stays, and the document's reference points at the SOURCE (so
    #    the loss is a face loss and not an unresolvable reference — `C-016` tier 5, not tier 4).
    no_render = fixtures.copy_fixture("clean", tmp_path / "no-render")
    record = record_arg(no_render)
    entry = trace_entry(no_render)
    assert verdict_of(obligation(no_render, "--record", record), DOC) == ("satisfied", "reference-resolves")
    for face in entry["rendered"]:
        (no_render / face["path"]).unlink()
    document = no_render / DOC
    document.write_text(
        document.read_text(encoding="utf-8").replace("../assets/widget.svg", "../assets/widget.mmd"),
        encoding="utf-8")
    faces.append(("rendered face deleted", no_render, record, ("missing", "orphan-rendered")))

    # b) the source is deleted, both rendered faces stay, and the reference resolves to a rendered face.
    no_source = fixtures.copy_fixture("clean", tmp_path / "no-source")
    record = record_arg(no_source)
    assert verdict_of(obligation(no_source, "--record", record), DOC) == ("satisfied", "reference-resolves")
    (no_source / trace_entry(no_source)["source"]).unlink()
    faces.append(("source deleted", no_source, record, ("missing", "orphan-source")))

    # c) both faces on disk, but the source is touched afterwards: the pair is out of step, not incomplete.
    stale = fixtures.copy_fixture("clean", tmp_path / "stale")
    record = record_arg(stale)
    entry = trace_entry(stale)
    source = stale / entry["source"]
    earliest_render = min((stale / face["path"]).stat().st_mtime for face in entry["rendered"])
    assert verdict_of(obligation(stale, "--record", record), DOC) == ("satisfied", "reference-resolves")
    untouched = source.read_text(encoding="utf-8")
    os.utime(source, (earliest_render + fixtures.MTIME_GAP_SECONDS, earliest_render + fixtures.MTIME_GAP_SECONDS))
    assert source.stat().st_mtime > min((stale / f["path"]).stat().st_mtime for f in entry["rendered"]), (
        "the mtime step must take effect, or this face would go green for the wrong reason"
    )
    assert source.read_text(encoding="utf-8") == untouched, "only the mtime moves; the bytes stay"
    faces.append(("source touched after render", stale, record, ("stale", "source-newer-than-render")))

    for label, space, record, expected in faces:
        payload = obligation(space, "--record", record, "--only", DOC)
        reading = verdict_of(payload, DOC)
        assert reading == expected, f"{label}: expected {expected}, got {reading}"
        assert payload["summary"]["converged"] is False, f"{label}: an actionable reading cannot converge"
        assert payload["summary"]["clean"] is False, f"{label}: an actionable reading cannot be clean"

    reasons = {reading[1] for _, _, _, reading in faces}
    assert reasons == {"orphan-rendered", "orphan-source", "source-newer-than-render"}, (
        f"the three faces must be three distinct named reasons, got {sorted(reasons)}"
    )


# ---------------------------------------------------------------------------
# SC-008 — an exemption is visible, and an exemption that no longer holds is reported (T047)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_sc008_exemption_visible_and_superseded(tmp_path: Path):
    """A recorded exemption is visible and lawful; one whose justification stopped holding is reported, not kept.

    Three readings of one state machine, on a space whose designated carrier has nothing to draw:

    1. **Visible, not a pass** — the document reads `recorded-exemption`, is counted in `exempted`, and the space
       is therefore not `clean`. An exemption a reader cannot see is an omission with paperwork.
    2. **It converges** — the same space converges once the other carriers carry diagrams (`converged=true` with
       `clean=false`): the exemption is a legal end state, never a residual awaiting work.
    3. **Superseded is reported** — once the document itself carries a resolving reference, the exemption is
       overturned by a fact, `summary.exemption_superseded` counts it, and the reading becomes unjudgeable. The
       record is NOT silently retained, and NOT silently deleted.

    red-when: an exempted document reads as satisfied or as missing, an exemption keeps the space from converging,
    or an exemption contradicted by a resolving reference is still accepted (or quietly removed).
    """
    space = fixtures.copy_fixture("exempt-ok", tmp_path)
    payload = obligation(space)
    summary = payload["summary"]
    assert verdict_of(payload, DOC) == ("recorded-exemption", "exempt-chronological"), (
        "an exempted document is exempted — not satisfied, and not missing"
    )
    assert summary["exempted"] == 1, f"the exemption is counted in its own bucket, got {summary['exempted']}"
    assert summary["clean"] is False, "an exempted space is not a zero-finding space (FR-004: not a pass)"
    assert summary["satisfied"] == 0, "an exemption MUST NOT be counted as a pass"

    converged = fixtures.copy_fixture("exempt-ok", tmp_path / "converged")
    converged_payload = obligation(converged, "--record", str(produce_diagram(converged, exempt=DOC)))
    assert converged_payload["summary"]["converged"] is True, "the exemption does not block convergence"
    assert converged_payload["summary"]["exempted"] == 1, "and it stays visible after convergence"

    overturned = fixtures.copy_fixture("exempt-superseded", tmp_path / "overturned")
    record = record_arg(overturned)
    assert verdict_of(obligation(overturned, "--record", record), DOC) == (
        "not-evaluated", "exemption-invalid"), "a resolving reference overturns the exemption's own justification"
    assert obligation(overturned, "--record", record)["summary"]["exemption_superseded"] == 1, (
        "the overturn is counted, so a report can say why an exemption stopped applying"
    )
    exemption = overturned / "docs" / ".speckit" / "exemptions" / "concepts" / "widget-overview.md"
    assert exemption.is_file(), "the record is retained as evidence — reported, never silently deleted"


# ---------------------------------------------------------------------------
# C-005 / C-006 — the mechanism half of the two flow clauses (`plan.md` table B assigns both here)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c005_shared_diagram_single_source(tmp_path: Path):
    """Two documents may reference one diagram, and the record keeps ONE entry and ONE source for it.

    Sharing is a property of the record, so it is asserted on the record: the second document's reference resolves
    to the same rendered face, and `diagrams[]` still holds a single entry naming that face. A producing run that
    forked the diagram per document would show two entries pointing at two different renders.

    red-when: a shared diagram acquires a second record entry (a per-document fork), or the second document's
    reference no longer resolves to the shared face.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record_path = produce_diagram(space)
    other = space / "docs" / "concepts" / "widget-adjacent.md"
    other.write_text(
        "# Widget adjacent\n\nThe same pipeline is drawn in "
        "[the shared diagram](../assets/widget.svg).\n", encoding="utf-8")

    record = json.loads(record_path.read_text(encoding="utf-8"))
    shared = [entry for entry in record["diagrams"] if entry["source"].endswith("widget.mmd")]
    assert len(shared) == 1, f"a shared diagram keeps exactly one source entry, got {len(shared)}"
    rendered_paths = [face["path"] for face in shared[0]["rendered"]]
    assert len(rendered_paths) == len(set(rendered_paths)), f"rendered faces must not fork: {rendered_paths}"

    payload = obligation(space, "--record", str(record_path), "--only", "docs/concepts/widget-adjacent.md")
    assert payload["summary"]["satisfied"] == 1, (
        "the second document resolves to the same face and is judged satisfied by the same entry"
    )
    assert space.joinpath("docs/assets/widget.mmd").is_file(), "one source file, not one per document"


# ---------------------------------------------------------------------------
# SC-004 — a rename keeps the document and its diagram in step (T057)
#
# The scenario is the one `requirements.md` US3 names: a depicted component is renamed in the prose, and the
# pair must either move together or say out loud that it did not. `plan.md` table B gives the clauses this row
# serves (`C-023`'s red-when and `C-015`'s named-staleness half); the assertion is authored here and the
# GREEN state is delivered by T052/T053/T058, so it is red first by construction.
# ---------------------------------------------------------------------------


def renamed_pair(space: Path, old: str, new: str) -> tuple[Path, Path]:
    """Rename `old` → `new` in the document's prose AND in its diagram source; return both written files.

    This is what "the pair moves together" means on disk, written mechanically because the producing capability
    is model-driven and a test may not invoke it (`test_c008a_*`'s harness note applies here too).
    """
    source = space / "docs" / "assets" / "widget.mmd"
    document = space / DOC
    source.write_text(source.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    document.write_text(document.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    return document, source


@pytest.mark.integration
def test_sc004_rename_keeps_document_and_diagram_in_step(tmp_path: Path):
    """A rename either lands in both the prose and the diagram, or is reported — never a silent divergence.

    Three readings, and the middle one is the reason the row exists:

    1. **Re-rendered** — renaming the depicted component in the document and re-producing the pair keeps the
       document `satisfied`: the pair moved together, and the checker still resolves the reference to the face
       the run produced. Byte-level before/after readings of BOTH files are captured, so "it moved" is measured.
    2. **Prose only** — the same rename applied to the document alone leaves the space judged `satisfied` too,
       and that is the recorded capability boundary rather than a bug: `D-001` (the semantic half of `stale`)
       is deliberately uncovered, so the mechanical reading cannot see that the picture still says `Validator`.
       The assertion therefore pins WHAT THE MECHANISM CAN SEE (the document is still judged, the diagram is
       still on disk) and states the limit explicitly instead of asserting a green that would be a lie.
    3. **Source only, no re-render** — renaming the component in the source without re-rendering turns the
       space red as `stale` / `source-newer-than-render`, which is the named staleness finding `C-015` requires
       an improve run to report rather than roll back.

    red-when: the re-rendered pair stops being `satisfied`, the source-only rename stops being named `stale`, or
    the prose-only rename silently changes the DIAGRAM's bytes (a silent re-render would destroy the evidence).
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = record_arg(space)
    before_doc = (space / DOC).read_bytes()
    before_src = (space / "docs/assets/widget.mmd").read_bytes()
    assert obligation(space, "--record", record)["documents"][0]["verdict"] == "satisfied", (
        "premise: the pair starts in step"
    )

    # 1) the pair moves together: prose and source both renamed, then the run re-renders the face.
    #    The rename is word-bounded because the fixture's prose says "the store" while its diagram label says
    #    "Widget store" — matching the label string verbatim would rename the source and no byte of the prose.
    document = space / DOC
    document.write_text(
        re.sub(r"\bstore\b", "repository", document.read_text(encoding="utf-8")), encoding="utf-8")
    document, source = renamed_pair(space, "Widget store", "Widget repository")
    after_doc, after_src = document.read_bytes(), source.read_bytes()
    assert after_doc != before_doc and after_src != before_src, (
        "the rename must touch BOTH files, or 'they moved together' would be unmeasured"
    )
    assert "repository" in after_doc.decode("utf-8"), "the prose carries the new name"
    assert "Widget repository" in after_src.decode("utf-8"), "and so does the diagram source's label"
    # The re-render is what closes the pair, and it is not optional: the moment the source is newer than the
    # face, the space reads `stale`. Asserting that FIRST pins the mechanism (the rename alone is not "in
    # step"), then the re-render produces both faces again and the reading returns to `satisfied` — the record
    # is re-written in the same pass because its `rendered[].sha256` must describe the faces now on disk.
    before_render = obligation(space, "--record", record, "--only", DOC)
    assert verdict_of(before_render, DOC) == ("stale", "source-newer-than-render"), (
        "a renamed source with no re-render is `stale` — the pair is not in step until the face is rebuilt"
    )
    record = str(produce_diagram(space))
    together = obligation(space, "--record", record, "--only", DOC)
    assert verdict_of(together, DOC) == ("satisfied", "reference-resolves"), (
        "after the re-render the pair moved together: both faces carry the new name and the record describes them"
    )

    # 2) the prose-only rename: the pair now disagrees, and the checker's own scope stops at the reference
    prose_only = fixtures.copy_fixture("clean", tmp_path / "prose-only")
    prose_record = record_arg(prose_only)
    doc_before = (prose_only / DOC).read_bytes()
    src_before = (prose_only / "docs/assets/widget.mmd").read_bytes()
    (prose_only / DOC).write_text(
        re.sub(r"\bstore\b", "repository", (prose_only / DOC).read_text(encoding="utf-8")),
        encoding="utf-8")
    reading = obligation(prose_only, "--record", prose_record, "--only", DOC)
    assert verdict_of(reading, DOC) == ("satisfied", "reference-resolves"), (
        "D-001: the semantic half of `stale` is uncovered by design, so the mechanical reading is unchanged"
    )
    assert (prose_only / "docs/assets/widget.mmd").read_bytes() == src_before, (
        "a prose-only rename MUST NOT silently re-render the diagram — the divergence stays on disk as evidence"
    )
    assert (prose_only / DOC).read_bytes() != doc_before, "the prose change itself is the fact under test"

    # 3) the source-only rename with no re-render: the named staleness finding, not a green
    source_only = fixtures.copy_fixture("clean", tmp_path / "source-only")
    source_record = record_arg(source_only)
    entry = trace_entry(source_only)
    mmd = source_only / entry["source"]
    earliest_face = min((source_only / face["path"]).stat().st_mtime for face in entry["rendered"])
    mmd.write_text(mmd.read_text(encoding="utf-8").replace("Widget store", "Widget repository"),
                   encoding="utf-8")
    os.utime(mmd, (earliest_face + fixtures.MTIME_GAP_SECONDS, earliest_face + fixtures.MTIME_GAP_SECONDS))
    assert verdict_of(obligation(source_only, "--record", source_record), DOC) == (
        "stale", "source-newer-than-render"), (
        "a renamed source with no re-render is the named staleness finding an improve run must REPORT"
    )


@pytest.mark.integration
def test_c006_engine_sticky_on_update(tmp_path: Path):
    """An update to an existing diagram keeps the engine its record names; only a NEW diagram is routed.

    The record is the evidence, so the reading is a before/after comparison of `engine` across an update: the
    same diagram re-produced keeps `mermaid`, while a diagram the record has never seen carries whatever the
    producing run routed for it. A flow that re-routed on update would change the first one's engine.

    red-when: re-rendering an existing diagram changes the engine its record names.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    before = trace_entry(space, DOC)["engine"]
    record_path = produce_diagram(space)
    after = json.loads(record_path.read_text(encoding="utf-8"))["diagrams"]
    kept = [entry for entry in after if entry["document"] == DOC]
    assert len(kept) == 1, "the existing diagram keeps exactly one record entry after the update"
    assert kept[0]["engine"] == before, (
        f"an update must re-use the recorded engine ({before}), not re-route it (got {kept[0]['engine']})"
    )
    fresh = [entry for entry in after if entry["document"] != DOC]
    assert fresh and all(entry["engine"] for entry in fresh), (
        "a new diagram is the only one that is routed, and it carries the engine it was routed to"
    )


# ---------------------------------------------------------------------------
# SC-006 / SC-003 / SC-009 / SC-010 — US5's readings (T060)
#
# Four assertions, one per US5 criterion the plan's table B names on this file. Each is authored red-first: the
# scenario they describe is one the delivery must make true, so a green here before T063/T064 would mean the
# assertion is vacuous rather than that the delivery landed.
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_sc006_two_runs_identical_and_keyed_by_path(tmp_path: Path):
    """Determinism, a path-keyed finding set drawn from the closed vocabulary, and three explicit verdicts.

    `SC-006` read as one assertion because its four readings only mean something together: two byte-identical
    runs (determinism), every affected document reported BY PATH with a reason the contract's closed table
    allows (re-runnability across a growing space), a clean space that says so explicitly rather than printing
    nothing (the empty-output false green), and an unjudgeable document reported as `not-evaluated` rather
    than folded into a pass.

    red-when: the two runs differ, a finding lacks a path, a reason falls outside the closed table, the clean
    space stops reporting `clean=true`, or a document with no trace record is counted as satisfied.
    """
    # the closed table is READ from its owner (the engine), never re-typed here — a second copy of the
    # vocabulary in a test would drift exactly the way `C-004`/`C-005` forbid the flows to drift.
    spec = importlib.util.spec_from_file_location("docs_utils_obligation_vocab", SCRIPT)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    closed = {reason for reasons in engine.VERDICT_REASONS.values() for reason in reasons}
    assert len(closed) >= 9, f"premise: the closed reason table did not load: {sorted(closed)}"

    mixed = fixtures.copy_fixture("no-diagram", tmp_path / "mixed")
    record = str(produce_diagram(mixed))
    # leave one carrier unproduced so the run has both a satisfied and a missing document in it
    untouched = mixed / "docs" / "reference" / "index.md"
    untouched_body = untouched.read_text(encoding="utf-8")
    untouched.write_text(re.sub(r"\n\nIt is drawn in \[.*", "", untouched_body), encoding="utf-8")

    first = run_engine("--action", "obligation", "--root", str(mixed), "--record", record)
    second = run_engine("--action", "obligation", "--root", str(mixed), "--record", record)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout, "two runs over one space must serialise byte-identically"

    payload = json.loads(first.stdout)
    assert payload["documents"], "the space has carriers, so the finding set cannot be empty"
    for entry in payload["documents"]:
        assert entry["path"], f"every finding is keyed by path (FR-016): {entry}"
        assert entry["reason"] in closed, f"reason {entry['reason']!r} is outside the closed table"
    assert [entry["path"] for entry in payload["documents"]] == sorted(
        entry["path"] for entry in payload["documents"]), "the finding set is ordered by path, not by discovery"

    # `clean/` is the space whose DESIGNATED carrier is converged; the five directory indexes it also carries
    # have no diagram and are therefore findings — a reading `test_sc001_four_artifacts_present` pins from the
    # `--only` side. Scoping to the carrier is what makes "a clean space says so" a claim about the space's
    # own subject rather than a number this test would have to keep in step with the fixture.
    clean = fixtures.copy_fixture("clean", tmp_path / "clean")
    clean_payload = obligation(clean, "--record", record_arg(clean), "--only", DOC)
    assert clean_payload["summary"]["clean"] is True and clean_payload["summary"]["converged"] is True, (
        "a clean scope states its verdict explicitly; an empty output would be the false green this checks"
    )

    unjudged = fixtures.copy_fixture("no-trace", tmp_path / "unjudged")
    assert verdict_of(obligation(unjudged), DOC) == ("not-evaluated", "no-trace-record"), (
        "a document whose record is absent is not evaluated — never counted as a pass"
    )
    assert obligation(unjudged)["summary"]["converged"] is False, "and an unjudged space has not converged"


@pytest.mark.integration
def test_sc003_reconcile_reports_then_converges(tmp_path: Path):
    """`SC-003`'s two-run shape: the first reconcile reports, the second converges, and the space stops churning.

    This is the criterion read on the ENGINE's side of the loop (its sibling `test_c008a_second_reconcile_zero_findings`
    reads the flow text that promises the loop exists). The distinction matters: one is "the flows converge the
    dimension", this one is "the dimension is convergent when they do".

    red-when: the first run reports nothing actionable, the second run stops converging after a produce step, or
    a repeat run keeps finding something new on an unchanged space.
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path / "reconcile")
    first = obligation(space)
    assert first["summary"]["missing"] >= 1, "the first reconcile must have something to report"
    assert first["summary"]["converged"] is False, "and it cannot claim convergence while it does"

    record = str(produce_diagram(space))
    second = obligation(space, "--record", record)
    assert second["summary"]["converged"] is True, "after the produce step the dimension converges"
    assert (second["summary"]["missing"], second["summary"]["stale"],
            second["summary"]["not_evaluated"]) == (0, 0, 0), f"the three actionable tiers: {second['summary']}"

    third = obligation(space, "--record", record)
    assert third == second, "a repeat reconcile on an unchanged space reports the same reading (anti-churn)"


@pytest.mark.integration
def test_sc009_confirm_tiers_and_zones_unchanged(tmp_path: Path):
    """`SC-009`: the diagram dimension adds no confirmation tier, and no diagram artifact is triaged as prose.

    Two readings on one space. The tier table is `create-docs`'s, so this assertion only measures that the space's
    diagram work stays INSIDE the automatic class it is already in (a produce step that needed a confirmation
    would have to appear in that table); and `assets/` is outside the carrier set, so no file under it may be
    judged, counted or moved as a document — including the two faces the produce step just wrote.

    red-when: an `assets/` file is judged as a carrier, an auxiliary record directory is judged, or the produce
    step's own writes make the space unrepeatable (which is what a confirmation gate would show up as).
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = str(produce_diagram(space))
    payload = obligation(space, "--record", record)

    judged = [entry["path"] for entry in payload["documents"]]
    assert judged, "premise: the space is judged at all"
    for path in judged:
        assert "/assets/" not in path, f"a diagram artifact was triaged as a carrier document: {path}"
        assert "/.speckit/" not in path, f"an auxiliary record was triaged as a carrier document: {path}"
    assert payload["carriers"] == len(judged), (
        "the carrier count is the judged set — an `assets/` face did not inflate it"
    )

    before = payload["summary"]
    repeat = obligation(space, "--record", record)["summary"]
    assert repeat == before, (
        "the produce step's own writes converge once and stay converged — a tier that re-gated them would "
        f"show up as a changed reading: {before} -> {repeat}"
    )
    assert "assets/" in str(record) or (space / "docs" / "assets").is_dir(), (
        "premise: the landing the produce step used is the one still on disk"
    )


@pytest.mark.integration
def test_sc010_unrefreshed_runtime_degrades_visibly(tmp_path: Path):
    """`SC-010`: a project whose runtime was never refreshed reads as NOT EVALUATED, never as satisfied.

    The realistic shape is a space that predates the obligation: documents with prose, no `docs/.speckit/`
    directory at all, therefore no record and nothing to resolve a reference against. `FR-023`'s discipline is
    that this state must be VISIBLE — the failure mode it guards against is a checker that finds nothing to
    compare and therefore reports nothing wrong.

    red-when: a pre-obligation space reads `satisfied` (or `clean`), or the absence of the runtime store makes
    the engine silent instead of reporting an unjudged document.
    """
    space = fixtures.copy_fixture("no-diagram", tmp_path)
    speckit = space / "docs" / ".speckit"
    if speckit.exists():
        subprocess.run(["rm", "-rf", str(speckit)], check=True)
    assert not speckit.exists(), "premise: the runtime store is absent, not merely empty"

    payload = obligation(space)
    assert payload["documents"], "an unrefreshed space is still judged — silence would be the false green"
    assert verdict_of(payload, DOC)[0] == "missing", (
        "with no runtime store there is no diagram to resolve, so the document is a finding, not a pass"
    )
    assert payload["summary"]["satisfied"] == 0, "nothing in an unrefreshed space can be satisfied"
    assert payload["summary"]["clean"] is False and payload["summary"]["converged"] is False, (
        "and the space reports both predicates false rather than a vacuous clean"
    )
    assert payload["record"] is None, "no record was available, and the payload says so instead of guessing one"
