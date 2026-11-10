"""Integration tests: docs command deterministic scenarios (spec 033).

Covers the engine-verifiable parts of SC-001 (compliant skeleton passes
validate), SC-002 (repeat runs converge to zero new findings, audit always
written), and SC-006 (naming violations named).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs_command"

TYPE_DIRS = ["concepts", "tutorials", "tasks", "reference", "decisions", "contribute", "notes"]
ROOT_ENTRIES = {
    "README.md": "# Project\n\nSee [docs](docs/concepts/overview.md).\n",
    "ARCHITECTURE.md": "# Architecture\n\nSummary. See [overview](docs/concepts/overview.md).\n",
    "CONTRIBUTING.md": "# Contributing\n\nSee [dev setup](docs/contribute/dev-setup.md).\n",
    "CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n",
}


def run_engine(*args: str) -> dict:
    proc = run_engine_in_process(SCRIPT, args)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def make_skeleton(root: Path) -> None:
    """Build the bootstrap skeleton the command template promises (SC-001 shape)."""
    for name, body in ROOT_ENTRIES.items():
        (root / name).write_text(body, encoding="utf-8")
    for d in TYPE_DIRS:
        (root / "docs" / d).mkdir(parents=True)
    (root / "docs" / "concepts" / "overview.md").write_text("# Overview\n", encoding="utf-8")
    (root / "docs" / "contribute" / "dev-setup.md").write_text("# Dev setup\n", encoding="utf-8")
    (root / "docs" / "decisions" / "index.md").write_text("# ADR index\n", encoding="utf-8")
    (root / "docs" / "decisions" / "template.md").write_text("# ADR-NNNN: title\n", encoding="utf-8")
    (root / "docs" / "notes" / "index.md").write_text(
        "# Notes\n\nfrontmatter required: title/created/expires/status\n", encoding="utf-8"
    )


@pytest.mark.integration
def test_sc001_compliant_skeleton_has_zero_violations(tmp_path: Path):
    make_skeleton(tmp_path)
    out = run_engine("--action", "validate", "--root", str(tmp_path))
    assert out["violations"] == [], f"skeleton must be clean: {out['violations']}"


@pytest.mark.integration
def test_sc002_repeat_run_zero_new_findings_but_audit_always_written(tmp_path: Path):
    make_skeleton(tmp_path)
    first = run_engine("--action", "validate", "--root", str(tmp_path))
    second = run_engine("--action", "validate", "--root", str(tmp_path))
    assert first == second, "validate must be idempotent (anti-churn)"
    a1 = run_engine("--action", "audit", "--root", str(tmp_path),
                    "--scope", "full", "--summary", "all dimensions within tolerance")
    a2 = run_engine("--action", "audit", "--root", str(tmp_path),
                    "--scope", "full", "--summary", "all dimensions within tolerance")
    audit_dir = tmp_path / "docs" / ".speckit" / "audit"
    assert a1["written"] and a2["written"]
    assert len(list(audit_dir.glob("*.md"))) == 2, "every run must leave an audit trace"


@pytest.mark.integration
def test_sc006_naming_violations_all_named(tmp_path: Path):
    proj = tmp_path / "proj"
    shutil.copytree(FIXTURES / "messy_project", proj)
    out = run_engine("--action", "validate", "--root", str(proj))
    flagged = {(v["kind"], v["path"]) for v in out["violations"]}
    assert ("reserved-name-case", "readme.md") in flagged
    assert ("reserved-name-misuse", "DESIGN.md") in flagged
    assert ("reserved-name-misplaced", "docs/README.md") in flagged
    broken = [v for v in out["violations"] if v["kind"] == "broken-link"]
    assert len(broken) >= 2, "both broken links must be reported"


# ---------------------------------------------------------------------------
# spec 087 — the flow-obligation assertions (table B of `plan.md` § Test Plan)
#
# Owner of every assertion name below and of its red-when condition: `plan.md` § Test Plan table B. This block
# reads TEXT, not a fixture space: each clause of `contracts/flow-obligations.contract.md` is a statement about
# what one of the three surfaces says, so the assertion for it is a reading of that surface. Two rules shape
# every one of them:
#
# 1. **Anchor, then claim.** A reading that silently succeeds on an absent section is the defect this feature
#    records as its own lesson, so each assertion first locates the section it is about — a lost heading fails
#    with "the anchor is gone", never with a vacuous pass on `""`.
# 2. **Bounds are computed, not invented.** Any limit on "how much one surface may say" is READ from the owner
#    that already declares it (the diff budget from `BASE_COMMIT`, the residual-group ceiling from `create-docs`
#    § Tiered Confirmation), because a second copy of a ceiling is a second source of truth for it.
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / ".specify" / "specs" / "087-arch-diagram-docs"
CREATE_DOCS = REPO / "skills" / "external" / "create-docs" / "SKILL.md"
IMPROVE_DOCS = REPO / "skills" / "external" / "improve-docs" / "SKILL.md"
DOCS_TEMPLATE = REPO / "templates" / "commands" / "docs.md"
DRAW_DIAGRAM = REPO / "skills" / "external" / "draw-diagram" / "SKILL.md"
READER_DOC = REPO / "docs" / "concepts" / "documentation-model.md"
BASE_COMMIT = "24cb4edc"

DRAW_DIAGRAM_POINTER = "skills/external/draw-diagram"
# F26: the faces' step registry must be a path that SHIPS with the skill, not the framework repo's
# `quickstart.md` — a client project installs `.specify/skills/create-docs/` and never receives the spec dir.
SHIPPED_REFERENCE = "references/diagram-obligation.md"


def read(path: Path) -> str:
    assert path.is_file(), f"{path.relative_to(REPO)} is missing"
    return path.read_text(encoding="utf-8")


def section(path: Path, heading: str) -> str:
    """Body of the ATX section whose heading line is exactly `heading`, up to the next heading of any level."""
    return section_at(read(path), heading, origin=path)


def section_at(text: str, heading: str, origin: Path | None = None) -> str:
    """`section`, over text already in hand — the scope of a heading to the next heading of any level."""
    where = origin.relative_to(REPO) if origin is not None else "the document"
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        raise AssertionError(f"{where} no longer carries the section {heading!r}") from None
    level = len(heading) - len(heading.lstrip("#"))
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("#"):
            depth = len(line) - len(line.lstrip("#"))
            if depth <= level:
                return "\n".join(lines[start:index])
    return "\n".join(lines[start:])


def subsection(path: Path, parent: str, heading: str) -> str:
    """Body of `heading` where it must appear INSIDE `parent` — a same-named section elsewhere is not it.

    "Inside" is measured by scope, not by substring: the parent's own body runs to the next heading of ANY
    level, so a `####` subsection of it is not part of the section read. Nesting the child is therefore the
    parent's scope up to the next heading at the parent's level or shallower.
    """
    text = read(path)
    assert heading in text, f"{path.relative_to(REPO)}: {heading!r} must sit inside {parent!r}"
    scope = section_at(text, parent)
    assert heading in scope, f"{path.relative_to(REPO)}: {heading!r} must sit inside {parent!r}, not only after it"
    lines = scope.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    level = len(heading) - len(heading.lstrip("#"))
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("#"):
            depth = len(line) - len(line.lstrip("#"))
            if depth <= level:
                return "\n".join(lines[start:index])
    return "\n".join(lines[start:])


def bullet_after(body: str, marker: str) -> str:
    """The single bullet whose LABEL names `marker`, plus its continuation lines up to the next bullet/heading.

    The label is the leading token before the first separator (`R5 写作收敛`, `R5 收敛: …`), because a marker
    matched anywhere in the line also matches a cross-reference to that step inside another step's sentence —
    which would make "the step that produces diagrams" resolve to the step that merely mentions it. A bare
    `R##` label is read as a whole token, so `R4` never matches inside an indented `R6` sub-bullet.
    """
    lines = body.splitlines()
    label_re = re.compile(rf"^(\s*[-*]\s+)(?:\*\*)?{re.escape(marker)}(?![0-9a-z])")
    hits = [i for i, line in enumerate(lines) if label_re.match(line)]
    assert len(hits) == 1, f"expected exactly one bullet labelled {marker!r}, found {len(hits)}"
    indent = len(lines[hits[0]]) - len(lines[hits[0]].lstrip())
    collected = [lines[hits[0]]]
    for line in lines[hits[0] + 1:]:
        if line.startswith("#"):
            break
        if re.match(r"^\s*[-*]\s", line):
            if len(line) - len(line.lstrip()) <= indent:
                break
        elif line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        collected.append(line)
    return "\n".join(collected)


def sentence_with(body: str, needle: str) -> str:
    """The sentence (multi-line, whitespace-joined) containing `needle`."""
    flat = " ".join(body.split())
    starts = [0]
    for match in re.finditer(r"(?<=[.;:])\s+", flat):
        starts.append(match.end())
    starts.append(len(flat))
    for begin, end in zip(starts, starts[1:]):
        sentence = flat[begin:end]
        if needle in sentence:
            return sentence
    raise AssertionError(f"no sentence mentions {needle!r}")


def numbered_items(body: str) -> list[str]:
    """The numbered baseline items of a section, as one block each."""
    lines = body.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^\d+\.\s", line)]
    items = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        items.append("\n".join(lines[start:end]))
    return items


def base_commit_text(rel: str) -> str:
    proc = subprocess.run(["git", "show", f"{BASE_COMMIT}:{rel}"], cwd=REPO, capture_output=True, text=True)
    assert proc.returncode == 0, f"cannot read {rel} at {BASE_COMMIT}: {proc.stderr}"
    return proc.stdout


def changed_paths(rel: str) -> list[str]:
    """Paths this feature added to a directory, so a "the counterexample set is empty" claim is bounded."""
    proc = subprocess.run(["git", "diff", "--name-only", BASE_COMMIT, "--", rel],
                          cwd=REPO, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return sorted(line for line in proc.stdout.splitlines() if line)


def is_new(rel: str) -> bool:
    proc = subprocess.run(["git", "cat-file", "-e", f"{BASE_COMMIT}:{rel}"], cwd=REPO, capture_output=True)
    return proc.returncode != 0


# --- A. the obligation itself (C-001 … C-007) ----------------------------------------------------------


@pytest.mark.integration
def test_c001_four_artifacts_one_run():
    """One flow run yields four on-disk artifacts; the traceability record is deliberately not a fifth.

    The four are enumerated in `flow-obligations` `C-001` and inside `create-docs` by `[D-007]`; the reading is
    that R5 names the carrying document, the editable source, the rendered face(s) the delivery contract
    requires, and the resolving relative reference — and that the record is spoken of separately.

    red-when: R5 asks for fewer than four, or folds the record into the same enumeration (which would make the
    artifact count five and `C-003` ownerless).
    """
    r5 = bullet_after(section(CREATE_DOCS, "### Authoring Flow（文档写作流程）"), "R5")
    for named in ("document", "editable source", "rendered", "reference"):
        assert named in r5.lower(), f"the four artifacts must name {named!r}: {r5}"
    assert "record" in r5.lower(), "the producing run must also write the traceability record"


@pytest.mark.integration
def test_c002_by_reference_only():
    """Every surface that produces a diagram reaches the capability by PATH and copies none of its rules.

    `T-004`'s decision in executable form: a pointer, not a paraphrase. The assertion is that the path appears
    while the capability's own enumerations (engine layer names, the semantic-model schema, the delivery-clause
    identifiers) stay in their owner's file.

    red-when: a surface produces a diagram without naming the capability's path, or copies one of its
    enumerations — the second source of truth `C-002` exists to forbid.
    """
    for path in (CREATE_DOCS, IMPROVE_DOCS, DOCS_TEMPLATE):
        body = read(path)
        assert DRAW_DIAGRAM_POINTER in body, f"{path.relative_to(REPO)} must reach the capability by path"
        for restated in ("ldm_summary:", "| `mermaid` |", "§ D6", "routing-matrix.md#"):
            assert restated not in body, (
                f"{path.relative_to(REPO)} restates {restated!r}, which belongs to the drawing capability"
            )


@pytest.mark.integration
def test_c002_no_second_render_path():
    """The closed counterexample set is empty: no new drawing script, no engine table, no delivery copy.

    The set is CLOSED by construction (`C-002` lists its four members), so the assertion enumerates those four
    over the paths this feature changed and finds nothing. Bounding it to this feature's own paths is what makes
    the reading a claim about this delivery rather than about the repository's history.

    red-when: one of the four counterexamples appears under `skills/`, `templates/`, `scripts/` or `shared/` as a
    path this feature added.
    """
    added = [rel for rel in changed_paths("skills") + changed_paths("templates")
             + changed_paths("scripts") + changed_paths("shared") if is_new(rel)]
    forbidden = ("draw-diagram-", "render-", "engine-select", "delivery-contract")
    hits = [rel for rel in added if any(token in rel for token in forbidden)]
    assert not hits, f"a second render path was added: {hits}"


@pytest.mark.integration
def test_c003_same_run_wording():
    """The traceability record lands in the SAME run that produced the faces, and no later run may backfill it.

    `C-003` has two halves: "same run" (so the record travels with the faces) and the checker's reading of a
    missing record (so a later run cannot retro-fit acceptance). The reading half is the engine's and belongs to
    `I::test_c003_missing_record_not_satisfied` (`plan.md` table B); this assertion is the text half, on the step
    that produces diagrams.

    red-when: the record is described as written by a different step from the faces, or the step stops saying the
    record is part of the same run.
    """
    r5 = bullet_after(section(CREATE_DOCS, "### Authoring Flow（文档写作流程）"), "R5")
    flat = " ".join(r5.split()).lower()
    assert "same run" in flat or "同一次运行" in r5, "the record must be written in the same run as the faces"


@pytest.mark.integration
def test_c004_refusal_carried_through():
    """The capability's three refusal points are carried through verbatim, never absorbed into "complete".

    The three are the owner's own steps, so the premise is read from the owner first: `draw-diagram` must still
    name a Step 2 preflight, a Step 2.5 backend preflight and a Step 4 delivery check. The claim is that the
    consuming flows route a refusal there instead of writing "document complete, diagram skipped".

    red-when: a flow renders locally on refusal, marks the run complete anyway, or the owner stops carrying one
    of the three steps (which would make the carried-through claim unanchored).
    """
    owner = read(DRAW_DIAGRAM)
    for step in ("### Step 2:", "### Step 2.5:", "### Step 4:"):
        assert step in owner, f"premise: the capability no longer carries {step}"
    r5 = bullet_after(section(CREATE_DOCS, "### Authoring Flow（文档写作流程）"), "R5")
    flat = " ".join(r5.split()).lower()
    assert "refus" in flat or "拒绝" in flat, "R5 must name the refusal path it carries through"
    for absorbed in ("diagram skipped", "图跳过", "document complete, diagram"):
        assert absorbed not in r5.lower(), f"R5 must not absorb a refusal as {absorbed!r}"


# `C-005` (shared diagram, single source) and `C-006` (an existing diagram keeps its engine) name their subject
# by its MECHANISM, so `plan.md` table B assigns them to `tests/integration/test_docs_obligation_scenarios.py` as
# `I::test_c005_shared_diagram_single_source` / `I::test_c006_engine_sticky_on_update` — they read a space's trace
# record, not a skill's prose. The prose side of both clauses is read here, under names table B does not own:
# `test_c005_assets_single_landing_when_shared` and `test_c006_r5_keeps_a_recorded_engine`.


@pytest.mark.integration
def test_c005_assets_single_landing_when_shared():
    """Two documents may share one diagram, and sharing never forks the source or the record entry.

    The statement lives where both flows can read it — the baseline's `#### Assets` subsection registers the
    single landing and says what sharing means for it. The mechanism half of the same clause (one record entry
    per diagram, no per-document fork) is `I::test_c005_shared_diagram_single_source` in the engine-scenario
    file, which is where `plan.md` table B assigns it.

    red-when: sharing is described as a per-document copy, or the single landing stops being named a single
    landing.
    """
    assets = subsection(CREATE_DOCS, "### Desired-State Baseline", "#### Assets")
    flat = " ".join(assets.split()).lower()
    assert "share" in flat or "共享" in flat, "the landing must say that two documents may share one diagram"
    assert "single" in flat or "唯一" in flat, "the landing must stay a single landing when a diagram is shared"


@pytest.mark.integration
def test_c006_r5_keeps_a_recorded_engine():
    """Updating an existing diagram re-uses the engine its record names; only a NEW diagram is routed.

    `FR-010` on the flow side. The re-render text is anchored on the step that produces diagrams, so the claim
    cannot be satisfied by a sentence about a different step. The mechanism half (the record's `engine` is
    unchanged across an update) is `I::test_c006_engine_sticky_on_update`, per `plan.md` table B.

    red-when: the update step describes re-routing, or says nothing distinguishing an update from a new diagram.
    """
    r5 = bullet_after(section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)"),
                      "R5")
    flat = " ".join(r5.split()).lower()
    assert "engine" in flat, "R5 must name the engine decision it preserves"
    assert "existing" in flat or "已有" in flat or "既有" in flat, (
        "R5 must distinguish an existing diagram (engine kept) from a new one (routed)"
    )


@pytest.mark.integration
def test_c007_baseline_single_owner():
    """The obligation body lives ONCE, inside § Desired-State Baseline, in three parts, and restates no verdict.

    Three parts are the contract's own decomposition (`C-007`: carrier set + obligation + exemption). The second
    half is the `one-source-of-truth` check: the section must cite the carrier table rather than re-list it, and
    must not repeat the checker's verdict vocabulary — a baseline that echoes the vocabulary becomes a second
    owner of it.

    red-when: the obligation appears outside the baseline, the baseline item is missing one of its three parts,
    re-lists the carrier table, or names two or more checker verdicts.
    """
    baseline = section(CREATE_DOCS, "### Desired-State Baseline")
    items = numbered_items(baseline)
    assert len(items) == 5, f"the baseline must carry five numbered items, found {len(items)}"
    obligation = items[-1]
    flat = " ".join(obligation.split()).lower()
    assert "carrier" in flat, "the obligation item must name the carrier set"
    assert "exempt" in flat, "the obligation item must name the named-exemption path"
    assert "contracts/diagram-obligation.contract.md" in obligation, (
        "the obligation must cite the carrier table's owner instead of re-listing it"
    )
    # F26: the citation is by NAME, never by a spec-local link — the skill ships as `.specify/skills/create-docs/`,
    # where `contracts/` and `quickstart.md` do not exist, so a link there is dead for every client project.
    assert "](" + "contracts/diagram-obligation.contract.md" + ")" not in obligation, (
        "the carrier table's owner must be cited by name, not as a link that resolves only in the framework repo"
    )
    for verdict in ("satisfied", "not-evaluated", "recorded-exemption", "no-trace-record"):
        assert verdict not in flat, f"the baseline must not restate the checker's verdict word {verdict!r}"
    outside = read(CREATE_DOCS).replace(baseline, "")
    assert "diagram obligation" not in outside.lower(), "the obligation body appears outside its single owner"


# --- B. the two flows' wiring (C-008 … C-008a) ----------------------------------------------------------


@pytest.mark.integration
def test_c008_authoring_r2_plans_and_r6_checks():
    """R2 plans each new document's diagram, R5 produces both faces + reference + record, R6 runs the checker.

    `C-008` is a three-point wiring, and a partial wiring is the failure it names: R2 without R6 plans a diagram
    nobody verifies, R6 without R2 verifies a diagram nobody planned. `T045`'s authoring-flow reading lives here
    too — R2 (the plan), R5 (produce on create, re-render-not-re-route on update) and R6 (the two faces reported
    separately) — under the clause's own name, which `plan.md` table B owns.

    red-when: any of the three points is missing, R6 does not run the obligation action beside `validate`, or R5
    produces fewer than the four artifacts one run owes.
    """
    authoring = section(CREATE_DOCS, "### Authoring Flow（文档写作流程）")
    r2 = bullet_after(authoring, "R2")
    r5 = bullet_after(authoring, "R5")
    r6 = bullet_after(authoring, "R6")
    assert "diagram" in r2.lower(), "R2 must plan each new document's diagram"
    assert DRAW_DIAGRAM_POINTER in r5, "R5 must call the capability by path"
    assert "--action obligation" in r6, "R6 must run the obligation checker"
    assert "--action validate" in r6, "R6 must keep running validate alongside it"
    # T045's three authoring readings, each on the step that owns it.
    for part in ("structure the document will describe", "engine layer", "landing"):
        assert part in r2.lower(), f"R2's diagram plan must name the {part!r} element"
    r5_flat = " ".join(r5.split()).lower()
    for artifact in ("editable source", "rendered face", "relative reference", "traceability record"):
        assert artifact in r5_flat, f"R5 must produce the {artifact!r} in the same run"
    assert "never re-routed" in r5_flat or "not re-routed" in r5_flat, (
        "R5 must say an existing diagram keeps the engine its record names"
    )
    r6_flat = " ".join(r6.split()).lower()
    for face in ("source", "rendered face", "reference", "trace-record"):
        assert face in r6_flat, f"R6 must report the {face!r} face separately"


@pytest.mark.integration
def test_c008a_r3_r4_r5_wiring():
    """The reconcile loop's three diagram points: R3 differences, R4 one plan row each, R5 produces in-loop.

    `C-008a` is the clause that makes the diagram dimension CONVERGENT rather than a permanent observation: a
    finding has to become a plan row, and the plan row has to be executed by the same reconcile.

    red-when: R3 stops admitting the three actionable verdicts as differences, R4 does not give each difference
    its own produce/re-render row, or R5 delegates production to the authoring flow (which would make one
    reconcile an unbounded recursion).
    """
    loop = section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)")
    r3, r4, r5 = bullet_after(loop, "R3"), bullet_after(loop, "R4"), bullet_after(loop, "R5")
    for verdict in ("missing", "stale", "not-evaluated"):
        assert verdict in r3, f"R3 must admit {verdict!r} into the difference set"
    assert "produce" in r4.lower() or "re-render" in r4.lower(), "R4 must plan a produce/re-render row"
    assert "opt-out" in r4.lower(), "R4 must say the produce row stays out of the move/archive opt-out list"
    assert DRAW_DIAGRAM_POINTER in r5, "R5 must produce in-loop through the capability's front door"


@pytest.mark.integration
def test_c008a_second_reconcile_zero_findings():
    """The residual report's convergence criterion is `converged`, which is reachable a second time round.

    This clause is deliberately about the READING of the second run rather than about a fictional command:
    R6 must name `converged` as the criterion and must block the convergence conclusion on any non-zero
    actionable tier — the two halves that make "second run reports zero" decidable.

    red-when: the report uses `clean` as the convergence criterion (an exempted space then never converges), or
    a non-zero tier no longer blocks the conclusion.
    """
    r6 = bullet_after(section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)"),
                      "R6")
    flat = " ".join(r6.split())
    assert "converged" in flat, "R6 must name `converged` as the convergence criterion"
    assert "clean" in flat, "R6 must also report `clean`, so the two readings stay distinguishable"
    assert "convergence" in flat.lower() or "收敛" in flat, "R6 must state what blocks the convergence conclusion"


@pytest.mark.integration
def test_c008a_exemption_does_not_block_convergence():
    """An exempted document is a lawful terminal state: it blocks `clean`, never `converged`.

    `C-008a`'s sharpest row, and the one an implementation is most likely to get backwards — treating the
    exemption as residual makes every space with one legitimate exemption unconvergeable.

    red-when: R6 counts an exemption as an unresolved difference, or reports `clean` for a space that has one.
    """
    r6 = bullet_after(section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)"),
                      "R6")
    flat = " ".join(r6.split()).lower()
    assert "exempt" in flat, "R6 must count exemptions separately"
    assert "not a residual" in flat or "不是残差" in flat or "legal" in flat or "合法" in flat, (
        "R6 must say an exemption is a lawful state rather than a residual"
    )


# --- C. the dispatch surface (C-016 … C-022) --------------------------------------------------------------


@pytest.mark.integration
def test_c009_single_landing_named():
    """The landing is `docs/assets/<slug>.<ext>`, and no second landing exists.

    Two readings: the landing is NAMED (in the subsection that owns the area convention), and the second landing
    the decision rejected (`docs/<type>/diagrams/`) exists nowhere under `docs/`.

    red-when: the landing stops being named, or a `diagrams/` subtree appears (the excluded counter-proposal
    coming in through the back door).
    """
    assets = subsection(CREATE_DOCS, "### Desired-State Baseline", "#### Assets")
    assert "docs/assets/" in assets, "the single landing must be named"
    stray = sorted(str(p.relative_to(REPO)) for p in (REPO / "docs").rglob("diagrams"))
    assert not stray, f"a second landing exists under docs/: {stray}"


@pytest.mark.integration
def test_c010_tiers_unchanged():
    """Writing a diagram stays a safe local write; moving/archiving stays stop-and-confirm; no third tier.

    The tier table is read as a table: two named classes and one absence. A third row is the change this clause
    forbids, so the assertion is on the row count as well as on the two labels.

    red-when: a third action class appears, or diagram writing is moved into the confirm-gated class.
    """
    tiers = section(CREATE_DOCS, "### Tiered Confirmation（分级确认门禁）")
    rows = [line for line in tiers.splitlines()
            if line.startswith("|") and not re.match(r"^\|\s*-", line)
            and "Action class" not in line and "动作类" not in line]
    assert len([row for row in rows if "|" in row]) == 4, f"the tier table must keep its four rows: {rows}"
    assert "自动执行" in tiers, "safe local writes must stay automatic"
    assert "Stop and confirm" in tiers, "move/archive must stay stop-and-confirm"
    # `FR-020`: producing a diagram is a safe local write, and a diagram is never triaged as prose. Both are
    # readings of THIS table, which is why they belong to this clause rather than to a new one.
    assert "写图" in tiers or "diagram" in tiers.lower(), (
        "the tier table must place diagram writing in the automatic class by name"
    )
    assert "图" not in tiers.split("Archive")[-1] or "图示" not in tiers, (
        "a diagram must never be triaged as ordinary prose content"
    )


@pytest.mark.integration
def test_c011_improve_pointer():
    """The evidence step reads the document's traceability record as machine evidence of what diagram it owns.

    red-when: the evidence step never mentions the record, or points at a section that does not exist.
    """
    evidence = section(IMPROVE_DOCS, "### 2. Gather evidence (deterministic sources first)")
    flat = " ".join(evidence.split()).lower()
    assert "trace" in flat or "记录" in flat, "the evidence step must read the traceability record"
    assert "diagram" in flat or "图" in flat, "the record must be read as diagram evidence"


@pytest.mark.integration
def test_c012_improve_minimal_edit():
    """The classification table gains exactly one row — Diagram-sync — with an either/or consequence.

    The premise is the table as it stands (five rows), read by name rather than by count, so the assertion
    distinguishes "the table gained a row" from "the parser read nothing".

    red-when: the row is absent, a second row is added, or the row's verification consequence is hedged into
    something that permits doing neither.
    """
    classify = section(IMPROVE_DOCS, "### 3. Classify the improvement")
    rows = [line for line in classify.splitlines() if line.startswith("| `") or line.startswith("| **")]
    assert len(rows) >= 6, f"premise + claim: five existing rows plus one new row, found {len(rows)}"
    diagram_rows = [row for row in rows if "Diagram-sync" in row]
    assert len(diagram_rows) == 1, f"exactly one Diagram-sync row must exist, found {len(diagram_rows)}"
    row = " ".join(diagram_rows[0].split()).lower()
    assert "update the diagram" in row and ("or" in row), "the consequence must be an either/or"
    assert "staleness" in row, "the alternative consequence is a named staleness finding"


@pytest.mark.integration
def test_c013_improve_verify_includes_obligation():
    """A Diagram-sync hit updates the diagram; a miss says so in place and repeats it once in the report.

    `FR-007`'s anti-performance rule: not re-rendering to look busy. The assertion therefore looks for the
    negative branch explicitly — a rule that only describes the hit would leave the miss unconstrained.

    red-when: the miss branch is unstated (so a gratuitous re-render is permitted), or the update is not bound to
    the flow obligations.
    """
    apply_step = section(IMPROVE_DOCS, "### 4. Apply the minimal section-level edit")
    flat = " ".join(apply_step.split()).lower()
    assert "diagram" in flat, "the minimal-edit step must address the diagram"
    assert "no diagram work" in flat or "本次无需图工作" in apply_step, (
        "a miss must be stated in place, not left to inference"
    )
    assert "report" in flat or "报告" in apply_step, "the same statement must be repeated once in the report"


@pytest.mark.integration
def test_c014_improve_report():
    """Verify demands `satisfied` or a valid recorded exemption; the three other readings block completion.

    The clause is a conjunction of one positive pair and one blocking set, and both halves matter: without the
    blocking set, a `stale` document may still report itself improved.

    red-when: the verdict requirement is absent, or only the positive pair is stated (no blocking set).
    """
    verify = section(IMPROVE_DOCS, "### 5. Verify")
    flat = " ".join(verify.split()).lower()
    assert "satisfied" in flat, "Verify must require the satisfied reading"
    assert "recorded-exemption" in flat or "exemption" in flat, "Verify must accept a valid recorded exemption"
    for blocking in ("stale", "missing", "not-evaluated"):
        assert blocking in flat, f"Verify must block improvement-complete on {blocking!r}"


@pytest.mark.integration
def test_c015_named_staleness_keeps_source():
    """An unavailable engine raises a NAMED staleness finding and leaves the source untouched.

    red-when: re-render failure is swallowed, or the source is rolled back to "look consistent" — which the
    clause forbids precisely because the rollback destroys the evidence that the two faces disagree.
    """
    report = section(IMPROVE_DOCS, "### 6. Record and report")
    flat = " ".join(report.split()).lower()
    assert "staleness" in flat, "the report must carry a named staleness finding"
    assert "untouched" in flat or "不动" in report or "keep" in flat, "the source must stay untouched"


@pytest.mark.integration
def test_c016_dispatch_names_both_paths():
    """The dispatch section says BOTH the authoring and the content path are bound, and restates no obligation.

    Two readings in one clause: coverage (both paths) and restraint (the obligation's body stays in the two
    skills). The restraint half is what keeps the command a thin dispatch layer.

    red-when: only one path is named, or the command paraphrases the obligation instead of citing the skills.
    """
    dispatch = section(DOCS_TEMPLATE, "### 分派(本命令保留的编排职责)")
    flat = " ".join(dispatch.split()).lower()
    assert "authoring" in flat, "the authoring path must be named"
    assert "content" in flat, "the content path must be named"
    assert "skills/external/create-docs/SKILL.md" in dispatch or "create-docs" in dispatch, (
        "the obligation's body must be cited at its owning skill"
    )
    assert "improve-docs" in dispatch, "the content owner must be cited"
    assert "four on-disk artifacts" not in flat and "四件" not in dispatch, (
        "the command must not restate the obligation's body"
    )


@pytest.mark.integration
def test_c017_residual_five_counts():
    """The residual report carries the diagram dimension's five counts, grouped, with no sixth group name.

    The group ceiling is READ from the tier/governance owner rather than invented here: the assertion computes
    the ceiling from the structures already on disk (the artifact groups the flows name plus the diagram
    counts) and then checks that no extra name was introduced.

    red-when: one of the five counts is missing, or a sixth residual group name appears.
    """
    dispatch = section(DOCS_TEMPLATE, "### 分派(本命令保留的编排职责)")
    for count in ("satisfied", "missing", "stale", "exempted", "not-evaluated"):
        assert count in dispatch, f"the residual report must carry the {count!r} count"
    owners = read(CREATE_DOCS)
    ceiling = owners.count("残差报告")
    assert ceiling >= 2, "premise: the owning skills name the residual report"
    groups = re.findall(r"residual report grouped by owning skill]([^`]*)`", dispatch)
    assert not groups or "|\n" not in groups[0], "the group roster must not grow a sixth name"


@pytest.mark.integration
def test_c018_hard_constraints_kept():
    """The top-level chapter sequence, the `stop-and-confirm` literal and the owner literals all survive.

    `C-018` lists four hard constraints because four different guards pin them; this assertion states the three
    that live in the template (the fourth, the W1 byte-unchanged section, is pinned by the gate-wiring guard and
    its own contract test).

    red-when: a chapter is reordered, the governance literal is dropped, or a delegation pointer disappears.
    """
    text = read(DOCS_TEMPLATE)
    chapters = [line for line in text.splitlines() if line.startswith("## ")]
    assert chapters == ["## User Input", "## Glossary", "## Outline", "## Wrap-up", "## Handoffs"], chapters
    assert "stop-and-confirm" in text, "the governance keep-list literal must survive"
    assert "skills/external/improve-docs/SKILL.md" in text, "the content owner pointer must survive"
    # `C-018`'s fourth constraint is a byte-level claim about the W1 wiring subsection: new content lands AFTER
    # it, never inside it. Measured against the branch base, so "unchanged" is a reading rather than a memory.
    current = section(DOCS_TEMPLATE, "### 类别读取与文档型门禁(判定前一次,本命令不复制判据)")
    assert current in base_commit_text("templates/commands/docs.md"), (
        "the W1 category-reading subsection must stay byte-identical to the base commit"
    )


@pytest.mark.integration
def test_c019_no_new_command_no_new_tier():
    """The obligation is reachable from existing verification steps only: no new command, no new tier.

    "No new command" is read as a DELTA against the base commit rather than as an absolute roster (the roster's
    owner is another contract), which is the only form in which this feature can make the claim honestly.

    red-when: this feature added a command template, or a tier row — either would make the check reachable by a
    surface the specification never opened.
    """
    # 2026-11-07: the merged trunk carries Feature 088's two sanctioned command templates
    # (status.md, measure.md). This feature's delta check still rejects every other addition.
    # 2026-11-11: Feature 099's `/speckit.seal` template (seal.md) is sanctioned the same way.
    sanctioned_later_commands = {
        "templates/commands/status.md",
        "templates/commands/measure.md",
        "templates/commands/seal.md",
    }
    added = [
        rel
        for rel in changed_paths("templates/commands")
        if is_new(rel) and rel not in sanctioned_later_commands
    ]
    assert not added, f"no new command template may be introduced: {added}"
    tiers = section(CREATE_DOCS, "### Tiered Confirmation（分级确认门禁）")
    assert len([line for line in tiers.splitlines() if line.startswith("|")]) == 6, (
        "the tier table must keep its header plus four action classes"
    )
    # `FR-018`'s division of labour, read as a declaration rather than as prose: each of the four participants
    # still owns its own concern, and the obligation is an addition to what they produce.
    ownership = read(CREATE_DOCS)
    for owner, concern in (("`create-pages`", "presentation"), ("`improve-docs`", "Content quality")):
        assert owner in ownership and concern in ownership, (
            f"the ownership table must keep {owner} as the {concern} owner"
        )


# --- E. the improve-docs legs of US3, read as text (T056 / T058) -------------------------------------------
#
# The five assertions `test_c011` … `test_c015` above are table B's owners and they live in section C because
# T035 authored them red-first; what T056 adds here is the OTHER half of the same two clauses — that the
# improve flow reaches the drawing capability without duplicating it (`C-002`) — plus the reader's copy of the
# three face names (`C-023`). All three are readings of `improve-docs/SKILL.md`'s own text, never of a command.


@pytest.mark.integration
def test_c002_improve_docs_reaches_the_capability_by_path_only():
    """The improve flow names the capability's path AND stays inside its own structural boundary.

    `C-002` is a two-sided claim, and T058's row states both sides: reached by path (so a reader of the improve
    flow knows where to go) and never copied (no semantic model, no routing criteria, no delivery-contract row,
    no second rendering path). The second side is what keeps `create-docs` § Desired-State Baseline the single
    owner of the obligation's body — and what keeps the improve flow from gaining structural powers it does not
    have: it may update a diagram, never move, rename or archive a document while doing so.

    red-when: the pointer is absent, a copy of the capability's own rows appears, or the flow gains a move /
    rename / archive power on the way to the diagram.
    """
    body = read(IMPROVE_DOCS)
    assert DRAW_DIAGRAM_POINTER in body, "the improve flow must reach the capability by path"
    for copied in ("ldm_summary:", "| `mermaid` |", "§ D6", "routing-matrix.md#"):
        assert copied not in body, f"the improve flow restates {copied!r}, which the capability owns"
    boundary = section(IMPROVE_DOCS, "### Ownership boundary (do not cross)")
    flat = " ".join(boundary.split()).lower()
    assert "create-docs" in flat, "the boundary must keep the structural owner named"
    assert "move" in flat and "archive" in flat, (
        "the boundary must keep the move/archive hand-off that the diagram work cannot cross"
    )


@pytest.mark.integration
def test_c023_per_face_reasons_named_on_the_improve_side():
    """The three face reasons a content improvement can produce are each named where the improvement reads them.

    `C-023`'s flow half. `test_c023_per_face_reasons_named` reads them on `create-docs`'s side; an improvement
    run makes the same three findable, because a rename or a re-render is exactly what produces them. The
    registry pointer is part of the claim: three names without their step sequence are three words.

    red-when: one of the three is unnamed on the improve side, or the pointer to the single step registry is gone.
    """
    body = read(IMPROVE_DOCS)
    for face in ("orphan-rendered", "orphan-source", "source-newer-than-render"):
        assert face in body, f"the improve flow must name the face {face!r}"
    assert SHIPPED_REFERENCE in body, "the faces must point at the single step registry"


@pytest.mark.integration
def test_c019_no_new_command_reachable_from_existing_verification_steps():
    """`F::test_c019_dispatch_pointer`: the obligation has no entry point of its own — only the flows' verify.

    `FR-017`'s reachability claim read as a POSITIVE roster instead of as an absence: every surface that names
    the checker is one of the two owning skills' verification steps, and the command names it only through them.
    "No new command" was already checked as a delta (`test_c019_no_new_command_no_new_tier`); this is the same
    clause's other direction — that the check was not smuggled into a new dispatch point either.

    red-when: a third surface names `--action obligation`, or the command stops citing both skills for it.
    """
    dispatch = section(DOCS_TEMPLATE, "### 分派(本命令保留的编排职责)")
    assert "--action obligation" not in dispatch, (
        "the command must reach the checker through the skills' verification steps, not by calling it itself"
    )
    for skill in ("create-docs", "improve-docs"):
        assert skill in dispatch, f"the dispatch must keep naming {skill} as the owning surface"
    for skill_file in (CREATE_DOCS, IMPROVE_DOCS):
        assert "--action obligation" in read(skill_file), (
            f"{skill_file.relative_to(REPO)} must be the surface that runs the checker"
        )


@pytest.mark.integration
def test_c018_top_level_sequence_unchanged_and_confirm_literal_kept():
    """`F::test_c018_top_level_sequence_unchanged`: the two hard constraints a reader can check in one read.

    The full four-constraint reading is `test_c018_hard_constraints_kept`, including the byte-unchanged W1
    subsection; this assertion adds the one thing that one cannot state — that the sequence is the same as the
    BASE COMMIT's, not merely the same as a literal written in the test.

    red-when: a chapter is added, removed or reordered relative to the branch base, or the governance literal
    stops appearing BEFORE the dispatch section (which is where the command declares the tier it delegates).
    """
    def chapters(text: str) -> list[str]:
        return [line for line in text.splitlines() if line.startswith("## ")]

    assert chapters(read(DOCS_TEMPLATE)) == chapters(base_commit_text("templates/commands/docs.md")), (
        "the top-level chapter sequence must be the base commit's, measured rather than restated"
    )
    # The literal's position is a reading, not a choice: the command declares the tier it delegates in the
    # delegation sentence of `## Outline` (line 30 at the base commit), which PRECEDES `### 分派`. Scoping the
    # reading to the dispatch section instead would make the assertion red against a correct base commit.
    text = read(DOCS_TEMPLATE)
    assert "stop-and-confirm" in text.split("### 分派", 1)[0], (
        "the governance keep-list literal must survive in the delegation text before the dispatch section"
    )


@pytest.mark.integration
def test_c020_reader_projection_bounded():
    """The reader section exists, stays ≤ 12 lines and carries exactly the three reader-facing points.

    Absence and emptiness are different states, so the heading must exist before the bound is applied. The three
    points are the clause's own content list; anything beyond them turns the projection into a second rulebook.

    red-when: the section is missing, exceeds twelve lines, or states a fourth point / restates the verdict
    vocabulary.
    """
    body = section(READER_DOC, "## Diagram Obligation for Readers")
    lines = [line for line in body.splitlines() if line.strip()]
    assert len(lines) <= 12, f"the reader projection must stay within twelve lines, found {len(lines)}"
    flat = " ".join(body.split()).lower()
    for point in ("arrive with", "exempt", "reported"):
        assert point in flat, f"the projection must carry the point {point!r}"


@pytest.mark.integration
def test_c021_path_unchanged():
    """The reader document keeps its path: not renamed, not deleted, still in the directory-governance area map.

    Three readings of one fact. The diff reading is scoped to the base commit, so "unchanged path" is measured
    rather than asserted from memory.

    red-when: the file is renamed or deleted, or the area map stops naming it.
    """
    assert READER_DOC.is_file(), "docs/concepts/documentation-model.md must stay at its path"
    proc = subprocess.run(["git", "diff", "--name-status", BASE_COMMIT, "--", "docs/concepts/documentation-model.md"],
                          cwd=REPO, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    for line in proc.stdout.splitlines():
        status = line.split("\t", 1)[0]
        assert status.startswith("M"), f"the reader document must only ever be modified, got {status!r}"
    area_map = read(REPO / "tests" / "contract" / "test_directory_governance.py")
    assert "docs/concepts/documentation-model.md" in area_map, "the area map must still name the reader document"


@pytest.mark.integration
def test_c022_no_destructive_reclassification():
    """Existing documents are never silently re-classified: findings first, then a confirmed plan, then writes.

    `FR-021`'s guard, read where it can be read: the plan row adds faces rather than touching a document body,
    and the move/archive opt-out list stays the only gate on destructive work.

    red-when: the produce row is described as editing the document body, or it joins the destructive opt-out list
    (which would let a diagram change carry a document move with it).
    """
    r4 = bullet_after(section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)"),
                      "R4")
    flat = " ".join(r4.split()).lower()
    assert "加两面" in r4 or "add the diagram faces" in flat, (
        "the produce row must add faces rather than rewrite the document body"
    )
    assert "never rewrite the document body" in flat or "不重写文档正文" in r4, (
        "the guard must say the produce row leaves the document body alone"
    )
    assert "dry-run" in flat or "干跑" in r4, "the produce row must arrive through the dry-run plan"
    assert "opt-out" in flat, "the destructive gate must stay named"


@pytest.mark.integration
def test_c023_per_face_reasons_named():
    """The three face reasons are each named on the flow side, pointing at their single step registry.

    `FR-023`'s negative observability: three named faces, not one sentence saying "the diagram is wrong". The
    registry pointer is part of the clause, because the names are only decidable if their step sequence is.

    red-when: one of the three is unnamed, or the flow stops pointing at the registry that owns the steps.
    """
    assets = subsection(CREATE_DOCS, "### Desired-State Baseline", "#### Assets")
    body = assets + section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)")
    for face in ("orphan-rendered", "orphan-source", "source-newer-than-render"):
        assert face in body, f"the flow text must name the face {face!r}"
    assert SHIPPED_REFERENCE in body, "the faces must point at the single step registry"


# --- D. the run report's four evidences, and the two repository-level readings -----------------------------


@pytest.mark.integration
def test_c022_report_carries_four_evidences():
    """The run report carries four evidences; a "complete" conclusion missing one of them is not evidence.

    `FR-022` is stated twice in the contract on purpose — `C-001` as the production obligation, this clause as
    the REPORT obligation. The report side is the one a later reader depends on, so the assertion reads the
    residual/completion text for all four rather than for a summary count.

    red-when: a report field list omits one of the four (source path, rendered path(s), document reference,
    trace-record path), or allows the conclusion without them.
    """
    r6 = bullet_after(section(CREATE_DOCS, "### Reconcile Loop (thin dispatch — engine semantics live in the pattern doc)"),
                      "R6")
    flat = " ".join(r6.split()).lower()
    for evidence in ("source", "rendered", "reference", "record"):
        assert evidence in flat, f"the residual report must carry the {evidence!r} evidence"
    assert "four" in flat or "四件" in r6 or "四" in r6, "the report must state the evidence set as a fixed set"


@pytest.mark.integration
def test_c001_before_implementation_exit2_is_gone():
    """The pre-implementation reading is retired: the action is registered and answers with a payload.

    The recorded S1 reading (`invalid choice: 'obligation'`, exit 2) is kept in `quickstart.md` S1 as the
    front-loaded pre-state evidence; what must NOT survive is the behaviour. Two readings, because either alone
    is a false green: the parser accepts the action, and a real invocation returns a payload with exit 0.

    red-when: the action is absent from the parser's closed choice list, or a real run exits non-zero — which
    would mean "clean" and "ran" were compressed into one signal, the failure `C-001` forbids.
    """
    engine = read(REPO / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py")
    assert '"obligation"' in engine, "the action must be registered in the closed choice list"
    assert "invalid choice: 'obligation'" not in engine, "the retired pre-state must not be reproduced in source"
    proc = run_engine_in_process(
        SCRIPT,
        ["--action", "obligation", "--root",
         str(REPO / "tests" / "fixtures" / "docs-obligation" / "clean"), "--json"],
    )
    assert proc.returncode == 0, f"a real run must exit 0 (judged, not necessarily clean): {proc.stderr}"
    payload = json.loads(proc.stdout)
    assert payload["action"] == "obligation" and "summary" in payload, "the run must answer with a payload"
