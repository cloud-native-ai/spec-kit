"""Contract guards for Feature 091 — automatic git close-out (自动收口).

Every assertion in this module is a read of a **surface this feature writes** or a
behavioural read of a **fixture repository this module builds**. The clause each test
discharges is named in its docstring as ``<contract page> C-n``; the page lives under
`.specify/specs/091-auto-git-closeout/contracts/`.

Two evidence grades, never mixed (`closeout-verification.contract.md` C-1):
- a **structural** predicate reads files and never shells out;
- a **behavioural** predicate runs git against a throwaway repository under
  `tmp_path` / `tempfile.TemporaryDirectory()` and asserts the resulting state.

Everything here is read-only with respect to the framework tree: no test writes a
tracked file, and the only mutations performed on surfaces are *in-memory* (the
mutation arms apply a string substitution to a copy in memory and re-run the same
predicate over it).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.fixtures.git_closeout.block import parse_block

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

# --- surfaces this feature writes (each one is a named constant, never an inline path) ---
BLOCK_ASSET = REPO_ROOT / "skills" / "external" / "git-utils" / "assets" / "git-workflow-block.md"
STATE_FILE = REPO_ROOT / ".specify" / "workflow" / "git.md"
SKILL_MD = REPO_ROOT / "skills" / "external" / "git-utils" / "SKILL.md"
CLOSEOUT_REF = REPO_ROOT / "skills" / "external" / "git-utils" / "references" / "closeout-commands.md"
COMMIT_STEP = REPO_ROOT / "shared" / "workflow" / "artifact-commit-step.md"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
INSTR_TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
INSTR_LIVE = REPO_ROOT / ".specify" / "instructions.md"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "091-auto-git-closeout"
NOTES = SPEC_DIR / "notes"

START = "<!-- GIT_WORKFLOW_START -->"
END = "<!-- GIT_WORKFLOW_END -->"

CLOSEOUT_VALUES = ("commit+merge+push", "commit+merge", "commit-only", "ask")

# ============================================================================
# shared readers — the only places this module slices a surface
# ============================================================================


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def managed_block(text: str) -> str:
    """The text between the two markers, markers excluded. Fails loudly when unpaired."""
    assert text.count(START) == 1, f"expected exactly one {START} marker"
    assert text.count(END) == 1, f"expected exactly one {END} marker"
    start = text.index(START) + len(START)
    end = text.index(END)
    assert start < end, "managed-block markers out of order"
    return text[start:end]


def block_rows(text: str) -> dict[str, str]:
    """``- **Label**: value`` rows of the managed block, label -> value (last wins)."""
    rows: dict[str, str] = {}
    for line in managed_block(text).splitlines():
        m = re.match(r"^- \*\*(?P<label>[^*]+)\*\*:\s*(?P<value>.*)$", line)
        if m:
            rows[m.group("label").strip()] = m.group("value").strip()
    return rows


def closeout_values_of(value: str) -> tuple[str, ...]:
    """Every member of the closed value set that the cell states *as a value*.

    A value counts as *stated* when it appears inside a code span in the cell: prose may
    name a value while explaining what it is not, and only a code span is a claim about
    the declared domain.
    """
    spans = re.findall(r"`([^`]+)`", value)
    return tuple(v for v in CLOSEOUT_VALUES if v in spans)


def section(text: str, heading: str) -> str:
    """Body of the first ``## <heading>`` section.

    ``heading`` is matched against the H2 text with its own backticks and emphasis stripped, so a
    heading that quotes a marker (``## The `## Close-out` step``) is reachable by its plain name.
    """
    def plain(value: str) -> str:
        return " ".join(value.replace("`", "").replace("*", "").split())

    wanted = plain(heading)
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if body:
                break
            if plain(line[3:]) == wanted:
                body.append("")
            continue
        if body:
            body.append(line)
    assert body, f"section '## {heading}' not found"
    return "\n".join(body[1:])


def code_spans(text: str) -> list[str]:
    return re.findall(r"`([^`\n]+)`", text)


def shipped_tokens(text: str) -> set[str]:
    """Placeholder-render tokens of the block asset (``<UPPER_SNAKE>``)."""
    return set(re.findall(r"<([A-Z][A-Z0-9_]*)>", text))


# ============================================================================
# Phase 2 — the declaration on both surfaces (T011, T013, T014)
# ============================================================================

#: The two surfaces that carry the declaration: the shipped block asset (framework source) and
#: this project's instance (client runtime). One function, two paths — a one-sided guard lets
#: the asset and the instance drift apart without a red test.
DECLARATION_SURFACES = (BLOCK_ASSET, STATE_FILE)


@pytest.mark.parametrize("surface", DECLARATION_SURFACES, ids=lambda p: p.name)
def test_the_two_declaration_rows_exist_with_the_closed_value_set(surface):
    """FR-001 / FR-002 / FR-019 — `closeout-declaration.contract.md` C-1.

    Both rows are present, the strategy's value domain is the four-value closed set with
    ``ask`` as the default, and the remotes row states what an empty list means. The reading
    goes through the same parser the fixtures use, so the guard fails on a deleted row, an
    illegal value and a renamed row alike.
    """
    block = managed_block(read(surface))
    raw_rows = block_rows(read(surface))
    rows = {label.lower(): value for label, value in raw_rows.items()}
    assert "closeout" in rows, f"{surface.name}: the `Closeout` declaration row is missing"
    assert "closeout remotes" in rows, f"{surface.name}: the `Closeout remotes` row is missing"

    strategy = rows["closeout"]
    for value in CLOSEOUT_VALUES:
        assert value in strategy, f"{surface.name}: strategy value {value!r} must be offered"
    assert re.search(r"`?ask`?", strategy) and "default" in strategy.lower(), (
        f"{surface.name}: `ask` must be documented as the default"
    )
    illegal = re.findall(r"`(commit[^`]*)`", strategy)
    assert set(illegal) <= set(CLOSEOUT_VALUES), (
        f"{surface.name}: the value domain is closed; found {sorted(set(illegal) - set(CLOSEOUT_VALUES))}"
    )

    remotes = rows["closeout remotes"]
    assert re.search(r"empty|absent", remotes, re.I), (
        f"{surface.name}: the remotes row must name the empty/absent case; read {remotes!r}"
    )
    assert "no pushable remote" in remotes, (
        f"{surface.name}: the remotes row must state that it means no pushable remote; "
        f"read {remotes!r}"
    )
    parsed = parse_block(read(surface))
    expected_state = "placeholder" if surface is BLOCK_ASSET else "declared"
    assert parsed.state == expected_state, (
        f"{surface.name}: the surface must parse as {expected_state!r}, read {parsed.state!r}"
        " — the shipped asset carries the placeholder form and the instance is filled"
    )
    if surface is STATE_FILE:
        assert parsed.remotes, f"{surface.name}: a live instance must name a pushable remote"
        assert parsed.strategy in CLOSEOUT_VALUES, (
            f"{surface.name}: the declared strategy must be a member of the closed set"
        )


@pytest.mark.parametrize("surface", DECLARATION_SURFACES, ids=lambda p: p.name)
def test_the_block_carries_no_second_branch_table_and_no_restated_model_menu(surface):
    """FR-003 — `closeout-declaration.contract.md` C-2.

    The managed block names its own facts and *points* at the skill that owns the model menu.
    A restated branch table or a copied model menu inside the block would be a second owner:
    the two copies drift, and nothing goes red when they do.
    """
    block = managed_block(read(surface))
    pointer = rows_pointer_line(block)
    assert len(pointer.splitlines()) == 1, (
        f"{surface.name}: exactly one pointer line may carry the model menu; found "
        f"{len(pointer.splitlines())}"
    )
    stripped = "\n".join(line for line in block.splitlines() if line not in pointer.splitlines())
    for model in ("single-branch", "dual-branch", "temp-branch", "three-tier"):
        assert model not in stripped, (
            f"{surface.name}: the block must not name the model {model!r} outside its one "
            "pointer line — the model menu belongs to the git-utils skill"
        )
    table_lines = [line for line in block.splitlines() if line.strip().startswith("|")]
    branch_tables = [line for line in table_lines if re.search(r"branch|merge", line, re.I)]
    assert branch_tables == [], (
        f"{surface.name}: the block must carry no second branch table; found {branch_tables}"
    )
    assert pointer.strip(), (
        f"{surface.name}: the pointer line must be present and name the menu's owner; "
        "a block carrying the menu with no pointer has taken the menu over"
    )


def rows_pointer_line(block: str) -> str:
    """The block's pointer line that carries the model menu.

    One line inside the managed block names the menu and says where it is owned. It is
    identified by shape — a comment line stating the menu — so the guard reads a *form*, not
    a copied phrase, and a second such line is itself a failure.
    """
    return "\n".join(
        line for line in block.splitlines()
        if line.lstrip().startswith("<!--") and re.search(r"menu", line, re.I)
    )


def test_the_block_gained_only_the_two_declaration_rows():
    """FR-003 — `closeout-declaration.contract.md` C-2, measured as a set difference.

    ``notes/pre-change-measurements.md`` recorded the block's row set before this feature. The
    guard compares name **sets** (never counts) so a swap that keeps the count is still caught,
    and asserts that neither the merge form nor the conflict policy was restated into the block.
    """
    measurement = read(NOTES / "pre-change-measurements.md")
    added = []
    for surface in DECLARATION_SURFACES:
        rows = block_rows(read(surface))
        recorded = _recorded_rows(measurement, surface)
        new_rows = sorted({r.lower() for r in rows} - {r.lower() for r in recorded})
        added.append((surface.name, new_rows))
    for name, new_rows in added:
        assert {r.lower() for r in new_rows} <= {"closeout", "closeout remotes"}, (
            f"{name}: the only rows this feature adds are the two declaration rows; found {new_rows}"
        )
    block = managed_block(read(BLOCK_ASSET))
    for forbidden in ("--no-ff", "conflict policy", "conflict-resolution", "no fast-forward"):
        assert forbidden not in block.lower(), (
            f"the block must not restate the merge form or the conflict policy ({forbidden!r})"
        )


def _recorded_rows(measurement: str, surface) -> set[str]:
    """Row names the pre-change snapshot recorded for one surface."""
    section_name = "block-asset" if surface is BLOCK_ASSET else "state-file"
    rows: set[str] = set()
    inside = False
    for line in measurement.splitlines():
        if line.startswith("### "):
            inside = section_name in line.lower()
            continue
        if not inside:
            continue
        match = re.match(r"^- \*\*(.+?)\*\*", line)
        if match:
            rows.add(match.group(1).strip().lower())
    return rows


# ============================================================================
# US1 — the command surface (`closeout-commands.md`)
# ============================================================================


def test_command_reference_carries_no_hardcoded_remote_literal():
    """`closeout-declaration.contract.md` C-4 (command-surface half) + `closeout-executor.contract.md` C-7.

    The close-out path resolves its push target from the declaration, so the reference may
    not name a concrete remote. The substitution token ``<remote>`` MUST be present: a
    surface that *describes* substitution while writing a name still fails.
    """
    text = read(CLOSEOUT_REF)
    assert "<remote>" in text, "the substitution token `<remote>` must appear literally"
    invocation = re.compile(r"git\s+push\s+[^\n`]*", re.M)
    remotes = []
    for match in invocation.finditer(text):
        tokens = [tok for tok in match.group(0).split()[2:] if not tok.startswith("-")]
        if not tokens:
            continue
        # ``git push --force-with-lease <remote> <src>:<dst>`` -> the first non-flag token is
        # the remote; flag arguments (``--force-with-lease=...``) are skipped by the ``-`` test.
        remotes.append(tokens[0])
    literals = [r for r in remotes if not (r.startswith("<") and r.endswith(">"))]
    assert literals == [], (
        "no push command in the close-out reference may name a concrete remote; "
        f"found {literals}"
    )
    for forbidden in ("origin/", "gitlab/", "gitee/", "github/"):
        assert forbidden not in text, (
            f"the reference must not bake a remote-qualified ref ({forbidden!r}) into the "
            "command surface — refs are derived from `Closeout remotes`"
        )


def test_pre_existing_examples_elsewhere_are_reported_not_rewritten():
    """`closeout-executor.contract.md` C-7 — plan finding F-1, carried not repaired.

    The skill's *existing* command reference opens its pre-check with a fetch against the
    default-named remote. This feature does not rewrite another surface's examples; the
    finding is reported in the final report. The assertion records the current reading so a
    silent rewrite would be visible as a change here.
    """
    execute = REPO_ROOT / "skills" / "external" / "git-utils" / "references" / "execute-commands.md"
    text = read(execute)
    default_remote = "origin"
    assert re.search(rf"git\s+fetch\s+{default_remote}\b", text) or re.search(
        rf"git\s+push\s+{default_remote}\b", text
    ), (
        "F-1 recorded that the pre-existing examples name the default remote; if that is no "
        "longer true the finding was silently repaired and its record must move with it"
    )
    assert default_remote not in read(CLOSEOUT_REF) or "<remote>" in read(CLOSEOUT_REF)


def test_three_refusal_outcomes_are_distinct_named_outcomes():
    """`closeout-executor.contract.md` C-2 — undeclared model / missing block / not a repository.

    Three refusals, three names, three reasons. A surface that collapses them into one
    "cannot proceed" line has guessed where it should refuse.
    """
    text = read(CLOSEOUT_REF)
    outcomes = {
        "bad_block_missing": "workflow state surface unavailable",
        "bad_block_placeholder": "workflow not declared",
        "bad_block_not_repo": "not a git repository",
    }
    for name, phrase in outcomes.items():
        assert phrase in text, f"refusal {name!r} must be reported as {phrase!r}"
    for name in outcomes:
        assert re.search(rf"`{name}`", text), f"refusal {name!r} must be a named outcome"
    assert "MUST NOT guess" in text or "never a guessed model" in text, (
        "the refusal section must state that guessing is forbidden"
    )


def test_readonly_role_excludes_a_declared_and_named_remote():
    """`closeout-declaration.contract.md` C-4 (role half) — exclusion by role, not by name.

    Three arms: a read-only remote listed in `Closeout remotes`; a read-only remote named by
    a caller instruction; and the empty/absent list degrading the push step (never falling
    back to the repository's own configured remotes).
    """
    text = read(CLOSEOUT_REF)
    role = section(text, "Read-only role check")
    assert "read-only" in role.lower()
    assert re.search(r"even (?:if|when)[^\n]*`?Closeout remotes`?", role), (
        "role exclusion must hold even when the remote is listed in the declaration"
    )
    assert re.search(r"caller", role, re.I), (
        "role exclusion must hold even when a caller instruction names the remote"
    )
    push_targets = section(text, "Push targets")
    assert "skipped" in push_targets and (
        "empty" in push_targets and "absent" in push_targets
    ), "the empty and absent lists must both degrade to a skipped push with a stated reason"
    assert re.search(r"MUST NOT fall back", push_targets), (
        "the derivation must not fall back to the repository's configured remotes"
    )
    assert re.search(r"by role", push_targets), "the exclusion is by role, read from the block"


def test_unusable_block_outcomes_are_distinct_with_distinct_behaviour():
    """`closeout-declaration.contract.md` C-5 — three states, no collapse; no write, no Bootstrap.

    The model axis alone: a declared model with no pushable remote is NOT row 2 (that is
    C-4's separate axis), and `ask` is a third axis that does not move a project between rows.
    """
    text = read(CLOSEOUT_REF)
    table = section(text, "Unusable block")
    for state in ("missing", "unbalanced", "placeholder", "declared"):
        assert state in table.lower(), f"state {state!r} must be distinguished"
    for forbidden in ("MUST NOT run Bootstrap", "MUST NOT create a branch set", "MUST NOT write the block"):
        assert forbidden in text, f"the unusable-block handling must state {forbidden!r}"
    # the three behaviours must differ, not merely be listed
    assert "skip merge and push" in table, "state 1 skips merge and push, keeping the artifact commit"
    assert "degrade to local commit + merge" in table, "state 2 degrades rather than skips"
    assert "derive" in table, "state 3 derives the sequence"


def test_ask_path_presents_and_never_pushes():
    """`closeout-declaration.contract.md` C-7 + `closeout-verification.contract.md` C-1.

    The `ask` path presents the commands, ends the run and never blocks; it is the only
    value that never pushes on its own. It reaches the value->authority table by pointer
    instead of restating it, and no surface of this feature restates the confirmation-gate
    lists (which are reached by pointer to their owner).
    """
    text = read(CLOSEOUT_REF)
    ask = section(text, "The `ask` path")
    assert "presented" in ask, "the ask path presents the derived sequence"
    assert re.search(r"never blocks?|does not block|without blocking", ask), (
        "the ask path must not block the run"
    )
    assert re.search(r"never pushes|does not push", ask), "the ask path never pushes on its own"
    assert re.search(r"only value", ask), "`ask` must be named as the only never-pushing value"
    # pointer, not restatement: the transition table has its one carrier elsewhere
    assert "closeout-executor.contract.md" in ask, (
        "the ask path must reach the value->authority table by pointer"
    )
    # no surface of this feature restates a confirmation-gate list
    gate_owner = "shared/guidelines/confirmation-gates.md"
    for surface in (CLOSEOUT_REF, COMMIT_STEP):
        surface_text = read(surface)
        assert gate_owner in surface_text, (
            f"{surface.name} must reach the gate lists by pointer ({gate_owner})"
        )
        assert "gate-git-workflow-remote-ops" not in surface_text, (
            f"{surface.name} must not cite a gate from the owner's list by name"
        )


def test_strategy_value_transition_is_per_value_and_behavioural():
    """`closeout-executor.contract.md` C-8 — the terminal state per declared value.

    The reference points at the transition table rather than restating it; the guard drives
    each of the four values and asserts the *terminal state*, not the presence of a sentence.
    """
    text = read(CLOSEOUT_REF)
    transition = section(text, "Strategy value -> authorized actions")
    assert "closeout-executor.contract.md" in transition, (
        "the transition table's only carrier is the contract page; the reference points at it"
    )
    from tests.fixtures.git_closeout import derive_closeout

    expectations = {
        "commit+merge+push": "executed",
        "commit+merge": "executed",
        "commit-only": "executed",
        "ask": "presented",
    }
    for value, terminal in expectations.items():
        plan = derive_closeout(model="temp-branch", strategy=value, remotes=["mirror"], readonly=[])
        assert plan.terminal_state == terminal, f"{value!r} must end {terminal!r}"
    skipped = {
        "commit+merge+push": (),
        "commit+merge": ("push",),
        "commit-only": ("merge", "push"),
        "ask": ("commit", "merge", "push"),
    }
    for value, steps in skipped.items():
        plan = derive_closeout(model="temp-branch", strategy=value, remotes=["mirror"], readonly=[])
        assert plan.skipped == steps, f"{value!r} must skip exactly {steps}"


# ============================================================================
# US2 — the lifecycle owner (`shared/workflow/artifact-commit-step.md`)
# ============================================================================

_LIFECYCLE_HEADINGS = ("The step", "Boundaries", "Close-out step", "Why a shared owner rather than five copies")


def test_closeout_section_exists_after_the_commit_and_after_the_record_steps():
    """`closeout-lifecycle.contract.md` C-1 — a named section, placed after commit and records.

    The section is a part of the same owner, and its position is decidable from the document's own
    H2 order: the artifact-commit step comes first, the close-out section after it, and the
    record-producing steps it commits are named inside it.
    """
    text = read(COMMIT_STEP)
    headings = [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]
    assert headings[0] == "The step", f"the artifact-commit step must stay first, got {headings[0]!r}"
    close = [i for i, h in enumerate(headings) if "Close-out" in h]
    assert len(close) == 1, f"exactly one close-out section expected, got {close}"
    idx = close[0]
    assert idx > 0 and idx < headings.index("Why a shared owner rather than five copies"), (
        "the close-out section must sit between the commit step and the ownership rationale"
    )
    body = section(text, headings[idx])
    for step in ("## Feedback", "documentation"):
        assert step in body, f"the close-out must be placed after the record-producing step {step!r}"
    assert ".specify/memory/retention/closeout/" in body, (
        "the receipt directory must be named in the section that owns the receipt"
    )
    assert re.search(r"one receipt", body, re.I), "one receipt per run"
    assert re.search(r"never an edit", body), "the receipt is a new file, never an edit"
    assert re.search(r"written once", body, re.I), "write-once shape"


def test_commit_boundary_artifacts_first_records_once():
    """`closeout-lifecycle.contract.md` C-2 — artifacts in the artifact commit, records once."""
    body = section(read(COMMIT_STEP), "The `## Close-out` step")
    assert re.search(r"MUST NOT appear again", body), (
        "a record file appearing in the artifact commit must not appear again here"
    )
    assert re.search(r"listed in the report", body), (
        "an un-includable record is listed in the report, never silently dropped"
    )
    assert re.search(r"exactly one", body, re.I), "one commit covers the run's records"
    assert re.search(r"not split into per-class commits", body), (
        "the four record classes are not split into per-class commits"
    )
    assert re.search(r"every\s+\**`commit`\**\s+value inside one receipt is equal", body), (
        "the invariant is C-2's single commit, stated as value equality"
    )


def test_receipt_points_at_the_consuming_engine_and_never_edits_a_record():
    """`closeout-lifecycle.contract.md` C-3 — one receipt per run, pointer not rewrite."""
    body = section(read(COMMIT_STEP), "The `## Close-out` step")
    assert "pointer" in body.lower() and "engine" in body.lower(), (
        "the receipt must carry a pointer to the consuming engine's read rule"
    )
    assert re.search(r"MUST NOT modify, truncate or delete a record file", body), (
        "the close-out never edits a record file"
    )
    ref = read(CLOSEOUT_REF)
    assert re.search(r"closeout-lifecycle\.contract\.md` C-3", ref) or (
        ".specify/memory/retention/closeout/" in ref or "artifact-commit-step.md" in ref
    ), "the receipt contract is mirrored in the command reference"
    assert "artifact-commit-step.md" in ref, (
        "the command reference must reach the lifecycle owner by pointer"
    )


def test_report_field_set_is_enumerated_and_omission_is_a_defect():
    """`closeout-lifecycle.contract.md` C-4 — the mandatory report and its fields."""
    body = section(read(COMMIT_STEP), "The `## Close-out` step")
    for field in ("receipt", "records commit", "merge", "push targets", "deviations", "failure"):
        assert re.search(rf"\|\s*{field}\s*\|", body), f"report field {field!r} must be enumerated"
    assert "omission is a defect" in body, "the report is mandatory; omission must be named a defect"
    assert "nothing to do" in body, "'nothing to do' is itself a reportable outcome"


def test_three_forks_are_three_distinct_behaviours():
    """`closeout-lifecycle.contract.md` C-5 and C-6 — the three forks."""
    body = section(read(COMMIT_STEP), "The `## Close-out` step")
    assert re.search(r"read-only run", body), "fork 1 must be named"
    assert re.search(r"no empty commit", body), "fork 1 creates no empty commit"
    assert re.search(r"one line", body), "fork 1 is stated in one line"
    assert re.search(r"artifacts without records", body), "fork 2 must be named"
    assert re.search(r"still merge and push", body), "fork 2 still merges and pushes"
    assert re.search(r"carried no records commit", body), "fork 2 states the absence explicitly"
    assert re.search(r"other lines?' dirty files", body), "fork 3 must be named"
    assert re.search(r"upstream deviation", body), "fork 3 reports a deviation"
    assert re.search(r"never stage them", body), "fork 3 never stages them"


def test_old_push_boundary_is_gone_and_the_revision_is_present():
    """`closeout-lifecycle.contract.md` C-7 — the boundary sentence is revised in place."""
    text = read(COMMIT_STEP)
    boundaries = section(text, "Boundaries")
    assert "This step commits locally." not in text, (
        "the old wording must be gone: it asserted a local-only step without saying who pushes"
    )
    assert re.search(
        r"The artifact-commit step itself does not push;\s+push(?:ing)? belongs to the close-out step that follows it",
        " ".join(boundaries.split()),
    ), "the revised sentence must state that pushing belongs to the close-out step that follows"
    for other in (CLOSEOUT_REF, SKILL_MD):
        assert "This step commits locally." not in read(other), (
            f"{other.name} must not repeat the retired wording"
        )


def test_lifecycle_is_reached_by_pointer_from_every_unattended_mechanism():
    """`closeout-lifecycle.contract.md` C-8 — the closed set of mechanisms, and no second implementation.

    The pointer set is the SDD driver's close, periodic house-keeping and the feedback digest —
    a closed, named set this test enumerates. A fourth mechanism is a revision of the clause, not a
    silent extension of the search.
    """
    mechanisms = {
        "SDD driver close": REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md",
        "house-keeping": REPO_ROOT / "skills" / "external" / "sdd-house-keeping" / "SKILL.md",
        "feedback digest": REPO_ROOT / "skills" / "external" / "sdd-feedback-digest" / "SKILL.md",
    }
    owner = "artifact-commit-step.md"
    reachable = []
    for name, path in mechanisms.items():
        if not path.exists():
            continue  # mechanisms installed under a different slug are reported, not invented
        assert owner in read(path), f"{name} must reach the close-out owner by pointer ({owner})"
        reachable.append(name)
    assert reachable, "at least one unattended mechanism must reach the owner by pointer"

    # negative search: no second close-out implementation in the framework sources
    second = []
    for base in ("shared", "scripts", "skills", "templates"):
        for path in sorted((REPO_ROOT / base).rglob("*.md")) + sorted((REPO_ROOT / base).rglob("*.py")):
            if path == COMMIT_STEP or path.name.startswith("test_"):
                continue
            text = read(path) if path.suffix == ".md" else ""
            if re.search(r"^## (?:The )?`?##? ?Close-out", text, re.M):
                second.append(path)
    assert second == [], f"a second close-out owner was found: {second}"


def test_closeout_never_writes_the_block_and_never_runs_bootstrap():
    """`closeout-lifecycle.contract.md` C-6 + `closeout-declaration.contract.md` C-5."""
    body = section(read(COMMIT_STEP), "The `## Close-out` step")
    assert re.search(r"never write the workflow state surface", body, re.I) or re.search(
        r"does not fill, repair or create the block", body
    ), "the close-out must not write the state surface"
    assert re.search(r"does not run Bootstrap", body, re.I), "the close-out must not run Bootstrap"
    assert "shared/guidelines/confirmation-gates.md" in body, (
        "the gate list is reached by pointer to its owner"
    )


# ============================================================================
# US3 — the four models' derived sequences, proven on fixture repositories
# ============================================================================
def _seed_record(repo) -> tuple[str, ...]:
    """Write one record file and return its path — the commit the close-out must carry.

    Every US3 arm asserts a *new* commit, so each one seeds exactly what the close-out is for:
    one record the run produced, staged by explicit path (C-2, C-6). Without it the close-out
    correctly takes the artifacts-without-records fork and commits nothing, which is a
    different clause's subject.
    """
    rel = ".specify/memory/session/091-fixture-record.md"
    path = repo.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("run: 091 fixture\n", encoding="utf-8")
    return (rel,)




def test_the_reference_carries_all_four_derived_sequences():
    """FR-023 — `closeout-verification.contract.md` C-3.

    The derivation table names each model exactly once and each row's branches belong to that
    model alone: a projection that names another model's branches has copied a project's
    sequence into a shipped surface. The three-tier row must carry the intermediate branch.
    """
    table = section(read(CLOSEOUT_REF), "Deriving the sequence")
    for model in ("single-branch", "dual-branch", "temp-branch", "three-tier"):
        assert re.search(rf"\| \*\*{model}\*\* \|", table), f"the {model!r} row is missing"
    three_tier = [line for line in table.splitlines() if "three-tier" in line][0]
    assert "PRE" in three_tier and "DEV" in three_tier and "MAIN" in three_tier, (
        "the three-tier row must name DEV, PRE and MAIN — the intermediate branch is part of "
        "the sequence, never an optimization to skip"
    )
    assert re.search(r"MUST NOT skip an intermediate branch", table), (
        "the no-skip rule must be stated, so skipping PRE is decidable rather than a judgement"
    )
    # the per-model rows are the only place a sequence form is listed; the runnable arm is the
    # fixture driver, which must reproduce each row's shape
    from tests.fixtures.git_closeout import derive_closeout

    expected_kinds = {
        "single-branch": ("commit", "push"),
        "dual-branch": ("commit", "merge", "push"),
        "temp-branch": ("branch", "commit", "merge", "delete-branch", "push"),
        "three-tier": ("commit", "merge", "merge", "push"),
    }
    for model, kinds in expected_kinds.items():
        plan = derive_closeout(model=model, strategy="commit+merge+push", remotes=["mirror"], readonly=[])
        assert plan.kinds == kinds, f"{model}: derived {plan.kinds}, the table says {kinds}"


def test_single_and_dual_branch_models_reach_the_expected_end_state():
    """SC-001 — `closeout-verification.contract.md` C-3, asserted on end state.

    Single-branch: the trunk gains exactly one commit and the remote holds that commit.
    Dual-branch: the commit is on the daily branch, the archive branch advanced through the
    declared merge, and the remote holds both.
    """
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    # --- single-branch -----------------------------------------------------
    with build_repo("single-branch") as repo:
        before = repo.head_of(repo.trunk)
        plan = derive_closeout(
            model="single-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo))
        assert outcome.exit_code == 0, outcome.stdout
        assert repo.head_of("master") != before, "the trunk must gain a commit"
        assert repo.remote_branch_sha("mirror", "master") == repo.head_of("master"), (
            "the bare remote must hold the trunk's new head — a login-time push and a reported "
            "push that never happened are different facts"
        )
        assert len(repo.log_subjects("master")) == 2, (
            "exactly one new commit on the trunk (seed + commit); a second commit would mean "
            "the artifact commit was re-opened"
        )

    # --- dual-branch -------------------------------------------------------
    with build_repo("dual-branch") as repo:
        # The declared relation: the archive branch is a different line of history, so it is
        # seeded from an *earlier* commit and the daily branch's commit advances it through the
        # merge. Seeded from the same commit it would be fast-forwardable and the merge would be
        # a no-op — an end-state assertion that could then never distinguish the two outcomes.
        seed = repo.log_subjects("develop")[-1]
        repo.git("commit", "-q", "--allow-empty", "-m", "seed: archive line base")
        repo.git("update-ref", "refs/heads/archive", "HEAD")
        repo.git("reset", "-q", "--hard", seed_target := f"HEAD~1")
        archive_before = repo.head_of("archive")
        assert archive_before != repo.head_of("develop"), f"archive must start behind ({seed})"
        plan = derive_closeout(
            model="dual-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo))
        assert outcome.exit_code == 0, outcome.stdout
        daily_head = repo.head_of("develop")
        assert daily_head is not None and daily_head != archive_before, (
            "the daily branch carries the commit"
        )
        assert repo.head_of("archive") != archive_before, (
            "the archive branch advances through the declared relation"
        )
        assert repo.remote_branch_sha("mirror", "develop") == daily_head, (
            "the remote holds the daily branch at the commit"
        )
        assert repo.remote_branch_sha("mirror", "archive") is not None, (
            "the remote holds the archive branch the pivot pushed"
        )


def test_three_tier_model_advances_through_the_intermediate_branch():
    """SC-001 — the three-tier arm: DEV holds the commit, PRE then MAIN advanced, nothing skipped.

    The assertion is on the graph, not on printed text: PRE's head must be the merge of DEV, so
    a `DEV → MAIN` shortcut leaves PRE behind and fails here.
    """
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    with build_repo("three-tier") as repo:
        pre_before = repo.head_of("pre")
        main_before = repo.head_of("main")
        plan = derive_closeout(
            model="three-tier", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo))
        assert outcome.exit_code == 0, outcome.stdout

        dev, pre, main = repo.head_of("dev"), repo.head_of("pre"), repo.head_of("main")
        assert dev and dev != pre_before, "DEV holds the commit"
        assert pre != pre_before, "PRE advanced — the intermediate branch is never skipped"
        assert main != main_before, "MAIN advanced last"
        assert repo.is_ancestor(dev, pre), "PRE's history contains the commit"
        assert repo.is_ancestor(pre, main), "MAIN's history contains PRE — the order is real"
        for branch in ("dev", "pre", "main"):
            assert repo.remote_branch_sha("mirror", branch) == repo.head_of(branch), (
                f"all three declared branches reached the remote ({branch})"
            )


def test_short_lived_branch_rules_are_stated_and_guarded():
    """`closeout-executor.contract.md` C-4 — never on a remote, deleted only after a landed merge.

    Three duties: the branch never reaches a remote, the local delete waits for the merge
    (`branch -d` refuses an unmerged branch; `-D` is never used), and a collision with another
    line's branch is a reported stop rather than a reuse or a deletion.
    """
    text = read(CLOSEOUT_REF)
    short = section(text, "Short-lived branches")
    assert re.search(r"never created on any remote", short), (
        "the short-lived branch is never pushed"
    )
    assert re.search(r"only after the merge[^\n]*succeeded", short, re.I), (
        "the local delete waits for a landed merge"
    )
    assert "git branch -d" in short, "the merged-only form is the one named"
    assert re.search(r"`-D` is never used", short), (
        "the forced delete is excluded by name, so its absence is stated rather than assumed"
    )
    assert re.search(r"collision[^\n]*reported stop", short, re.I), (
        "a name collision is a reported stop"
    )
    assert re.search(r"never reuses? the branch", short) and re.search(
        r"never\s+deletes it", short
    ), "collision handling neither reuses nor deletes another line's branch"

    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    with build_repo("temp-branch") as repo:
        plan = derive_closeout(
            model="temp-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo))
        assert outcome.exit_code == 0, outcome.stdout
        feature = plan.feature_branch
        assert feature not in {ref.split("/")[-1] for ref in repo.remote_branch_names("mirror")}, (
            "the short-lived branch must never appear on the remote"
        )
        assert feature not in repo.branches(), (
            "the local short-lived branch is deleted after the landed merge"
        )


# ============================================================================
# US4 — a failure stops the line and hands back the exact command
# ============================================================================


def _advance_remote(repo, remote: str = "mirror", branch: str = "master") -> None:
    """Move the bare remote ahead through a second clone, so the next push is rejected."""
    repo.git("push", "-q", remote, f"{branch}:{branch}")
    side = repo.root / "side-clone"
    subprocess.run(
        ["git", "clone", "-q", str(repo.remotes[remote]), str(side)],
        check=True, capture_output=True, text=True,
    )
    env = dict(**__import__("os").environ)
    env.update(
        GIT_AUTHOR_NAME="side", GIT_AUTHOR_EMAIL="side@example.invalid",
        GIT_COMMITTER_NAME="side", GIT_COMMITTER_EMAIL="side@example.invalid",
        GIT_CONFIG_NOSYSTEM="1",
    )
    for args in (
        ["checkout", "-q", branch],
        ["commit", "-q", "--allow-empty", "-m", "side: advance the remote"],
        ["push", "-q", "origin", branch],
    ):
        proc = subprocess.run(["git", *args], cwd=str(side), capture_output=True, text=True, env=env)
        assert proc.returncode == 0, f"side clone failed at {args}: {proc.stderr}"


def test_failure_classes_and_the_no_retry_rule_are_stated():
    """FR-011 / SC-003 — `closeout-executor.contract.md` C-5.

    Three failure classes, an explicit ban on the retry loop, and no force form other than the
    lease variant. The negative arms matter most: a surface that lists the classes but leaves
    retrying allowed has not discharged the clause.
    """
    text = read(CLOSEOUT_REF)
    failure = section(text, "Failure discipline")
    # a phrase may wrap across a line inside the section, so the reading is whitespace-flattened
    flat = " ".join(failure.split())
    for phrase in ("merge conflict", "non-fast-forward rejection", "rejected push"):
        assert phrase in flat, f"failure class {phrase!r} must be named"
    assert re.search(r"no retry|never retry|No retry", failure), (
        "the ban on the retry loop must be explicit, not implied"
    )
    assert re.search(r"stops at that step", flat, re.I), "the line stops at the first failure"

    pushes = [m.group(0) for m in re.finditer(r"git\s+push[^\n`]*", text)]
    assert pushes, "the surface carries at least one push invocation"
    forced = [p for p in pushes if re.search(r"(^|\s)(--force|-f)(\s|$)", p)]
    assert forced == [], f"no bare force form may appear; found {forced}"
    for inv in pushes:
        if "--force" in inv:
            assert "--force-with-lease" in inv, f"forced form must be the lease variant: {inv}"
            assert "confirmation" in text.lower(), (
                "the lease variant runs only behind its own confirmation"
            )
    assert "never force" in failure or "no `--force`" in failure or "No force" in failure, (
        "the failure discipline states that forcing is not a recovery path"
    )


def test_a_rejected_push_stops_before_the_remote_changes():
    """SC-003 — `closeout-verification.contract.md` C-4, on the remote's own end state.

    The remote is advanced by a second clone, so the close-out's push is rejected. The
    assertions are that the run reports the failing stage and the exact command, performs no
    second attempt, and leaves the remote's reference listing exactly as it was — proof that
    nothing was forced over it.
    """
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    with build_repo("single-branch") as repo:
        _advance_remote(repo)
        before = repo.remote_branch_names("mirror")
        head_before = repo.remote_branch_sha("mirror", "master")
        assert head_before is not None

        plan = derive_closeout(
            model="single-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo))

        assert outcome.exit_code != 0, "a rejected push must not be reported as success"
        assert outcome.stage == "push", f"the failing stage is named, read {outcome.stage!r}"
        assert outcome.command.startswith("git push"), (
            f"the exact command is handed back, read {outcome.command!r}"
        )
        assert "mirror" in outcome.command, "the command names the concrete remote it failed on"
        assert repo.remote_branch_names("mirror") == before, (
            "the remote's reference listing is unchanged — the remote was never force-overwritten"
        )
        assert repo.remote_branch_sha("mirror", "master") == head_before, (
            "the remote's branch still points where the other line left it"
        )


def test_a_merge_conflict_stops_before_any_push():
    """`closeout-executor.contract.md` C-5 — the merge class, and no push step runs after it."""
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    with build_repo("dual-branch") as repo:
        repo.git("commit", "-q", "--allow-empty", "-m", "seed: archive line base")
        repo.git("update-ref", "refs/heads/archive", "HEAD")
        repo.git("checkout", "-q", "archive")
        target = repo.repo / "conflict.txt"
        target.write_text("archive line\n", encoding="utf-8")
        repo.git("add", "--", "conflict.txt")
        repo.git("commit", "-q", "-m", "archive: divergent edit")
        repo.git("checkout", "-q", "develop")
        target.write_text("daily line\n", encoding="utf-8")
        repo.git("add", "--", "conflict.txt")
        repo.git("commit", "-q", "-m", "daily: divergent edit")

        before = repo.remote_branch_names("mirror")
        plan = derive_closeout(
            model="dual-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed_record(repo), conflict=True)

        assert outcome.exit_code != 0, "a conflicted merge must not be reported as success"
        assert outcome.stage == "merge", f"the failing stage is the merge, read {outcome.stage!r}"
        assert "conflict.txt" in outcome.stdout, (
            "the conflicting path is reported so the run is reproducible"
        )
        assert outcome.pushed == (), "no push step runs after a failed merge"
        assert repo.remote_branch_names("mirror") == before, "the remote is untouched"


# ============================================================================
# US5 — the destructive boundary and "another line's dirty files" both hold
# ============================================================================

#: Every form that stages the whole working tree. Staging by explicit path is the rule (C-6);
#: a whole-tree form is how another line's work is silently swept in.
WHOLE_TREE_STAGING = (
    "git add -A",
    "git add --all",
    "git add .",
    "git add -u",
    "git commit -a",
    "git commit --all",
    "git stash",
    "git reset --hard",
    "git clean -",
)


def test_no_surface_carries_a_whole_tree_staging_form():
    """FR-014 — `closeout-executor.contract.md` C-6, on all three surfaces this feature writes."""
    for surface in (CLOSEOUT_REF, COMMIT_STEP, SKILL_MD):
        text = read(surface)
        for form in WHOLE_TREE_STAGING:
            # a prohibition may name the form in order to forbid it; a *command* may not use it
            offenders = [
                line for line in text.splitlines()
                if form in line and not re.search(r"MUST NOT|never|not\b|forbidden|禁止|不得", line, re.I)
            ]
            assert offenders == [], (
                f"{surface.name} carries the whole-tree form {form!r} as an instruction: {offenders}"
            )


def test_another_lines_dirty_file_is_a_deviation_and_never_staged():
    """FR-015 — C-6 and C-5 fork 3, asserted on the commit's own contents.

    Two files are in the tree: this run's record and another line's uncommitted file. The
    commit must contain the first and not the second, and the report must name the second as a
    deviation. An end-state assertion matters here: a run that prints the right sentence while
    staging everything would pass a text-only guard.
    """
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    with build_repo("single-branch") as repo:
        repo.git("checkout", "-q", "-b", "other-line")
        foreign = repo.repo / "other-line-work.txt"
        foreign.write_text("another line's uncommitted work\n", encoding="utf-8")
        repo.git("checkout", "-q", "master")

        owned = _seed_record(repo)
        plan = derive_closeout(
            model="single-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=owned)
        assert outcome.exit_code == 0, outcome.stdout

        committed = set(repo.git("show", "--name-only", "--pretty=format:", "HEAD").split())
        assert owned[0] in committed, "the run's own record is in the commit"
        assert "other-line-work.txt" not in committed, (
            "another line's dirty file MUST NOT be staged into this commit"
        )
        assert any("other-line-work.txt" in d for d in outcome.deviations), (
            f"the dirty foreign file is reported as a deviation, read {outcome.deviations}"
        )
        assert "other-line-work.txt" in repo.status_porcelain_as_text(), (
            "the foreign file is left exactly where it was — never stashed, reset or cleaned"
        )


#: The closed-set comparison for the destructive boundary (C-4 / C-6). The baseline object is
#: the pre-change reading in `notes/pre-change-measurements.md`; the comparison unit is the
#: set of **gate ids** the scanner reports; the admissible-difference owner is
#: `shared/guidelines/closed-set-claims.md`. No total-count constant is introduced here — the
#: existing pin in `test_wrap_up_wording_gate_safe.py` owns that number (tasks F-2).
GATE_SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
GATE_OWNER = "shared/guidelines/confirmation-gates.md"
CLOSED_SET_OWNER = "shared/guidelines/closed-set-claims.md"


def live_gate_ids() -> set[str]:
    """The gate ids of a scan taken in this run — the comparison unit, read mechanically."""
    proc = subprocess.run(
        [sys.executable, str(GATE_SCANNER), "--json", "--root", str(REPO_ROOT)],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, f"gate scan failed: {proc.stdout}{proc.stderr}"
    return {gate["id"] for gate in json.loads(proc.stdout)["gates"]}


def test_the_destructive_boundary_did_not_shrink_by_gate_name():
    """SC-004 / FR-026 — `closeout-verification.contract.md` C-4 and C-6.

    Baseline object: the pre-change gate reading recorded in
    `.specify/specs/091-auto-git-closeout/notes/pre-change-measurements.md` § T003.
    Comparison unit: the **ids** of the blocking gates a same-run scan reports.
    Admissible-difference owner: `shared/guidelines/closed-set-claims.md` — this feature adds
    none of its own and removes none of the owner's, so the admissible difference is empty.
    The set may only grow: a shrunken set means a destructive action lost its gate.
    """
    assert "27 blocking gates" in read(NOTES / "pre-change-measurements.md"), (
        "the baseline object must still record the pre-change gate reading"
    )
    assert GATE_OWNER in read(COMMIT_STEP) and GATE_OWNER in read(CLOSEOUT_REF), (
        "the gate lists are reached by pointer to their owner, never restated"
    )
    assert (REPO_ROOT / CLOSED_SET_OWNER).exists(), (
        "the admissible-difference owner named by the claim must exist"
    )
    current = live_gate_ids()
    baseline = {f"gate-{n:03d}" for n in range(1, 28)}
    assert current, "the same-run scan reports no gates — an empty unit proves nothing"
    missing = baseline - current
    assert missing == set(), (
        f"the destructive boundary shrank: {sorted(missing)} no longer gates a blocking action"
    )
    for surface in (CLOSEOUT_REF, COMMIT_STEP, SKILL_MD):
        text = read(surface)
        leaked = [
            gate_id for gate_id in re.findall(r"gate-\d{3}", text)
        ]
        assert leaked == [], f"{surface.name} cites a gate by id instead of by pointer: {leaked}"


def test_the_closeout_hands_a_destructive_step_back_before_running_it():
    """FR-017 / FR-018 — `closeout-executor.contract.md` C-7, stated once per surface.

    The hand-off is by pointer: the list is named by its owner's path, never copied. Both
    surfaces that describe the step carry the sentence, so a reader on either one sees the
    stop.
    """
    for surface in (COMMIT_STEP, CLOSEOUT_REF):
        text = read(surface)
        assert GATE_OWNER in text, f"{surface.name} must reach the gate owner by pointer"
        flat = " ".join(text.split())
        assert re.search(r"stops? and presents|stops? at that step|presented before it runs", flat, re.I), (
            f"{surface.name} must state that a destructive or governance-kept step stops and "
            "presents before it runs"
        )


# ============================================================================
# Polish — the entry point, the compiled face, the pointers, the instruction row
# ============================================================================


def test_the_skill_declares_one_named_closeout_operation():
    """FR-009 / T049 — the operation joins the skill's directed-convergence operations."""
    text = read(SKILL_MD)
    assert re.search(r"`closeout`", text), "the operation is named as a code span"
    assert "closeout-commands.md" in text, "the § Resources list carries the new reference"
    assert re.search(r"directed[- ]convergence|定向收敛", text), (
        "the operation is positioned by the two axes the skill already uses"
    )
    # one skill, one entry table: no second SKILL.md and no second dispatch table
    siblings = sorted(
        p.relative_to(REPO_ROOT / "skills").parts[:2]
        for p in (REPO_ROOT / "skills").rglob("closeout-commands.md")
    )
    assert siblings == [("external", "git-utils")], (
        f"exactly one skill owns the reference, read {siblings}"
    )
    refs = [p for p in (REPO_ROOT / "skills").rglob("*.md") if "closeout" in p.name]
    assert len(refs) == 1, f"no second close-out surface exists, read {[str(p) for p in refs]}"


def test_the_wrap_up_handler_row_exists_at_order_sixty():
    """T051 — one agent-kind handler row, order 60, behaviour-owner column pointing at the owner."""
    text = read(PROBE_DEFS)
    handlers = section(text, "Handler")
    rows = [
        line for line in handlers.splitlines()
        if line.startswith("|") and re.match(r"\| h-closeout \|", line)
    ]
    assert rows, "a close-out handler row must exist in the § Handler table"
    row = rows[0]
    assert re.search(r"\b60\b", row), f"the row takes the next free order, 60; read {row!r}"
    assert "shared/workflow/artifact-commit-step.md" in row, (
        f"the behaviour-owner column points at the commit-step owner; read {row!r}"
    )
    assert re.search(r"\| agent \|", row), "the handler kind is the agent kind"

    # the compiled faces are generated, never hand-edited — the check runs the engine
    compile_check = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "probe-utils.py"),
         "--action", "compile-embeds", "--check"],
        capture_output=True, text=True, check=False,
    )
    assert compile_check.returncode == 0, (
        f"the compiled faces are stale: {compile_check.stdout}{compile_check.stderr}"
    )


def test_every_unattended_mechanism_reaches_the_one_owner():
    """SC-005 — `closeout-lifecycle.contract.md` C-9, plus the negative half.

    Three mechanisms must reach the close-out step by pointer: the driver's close, periodic
    house-keeping and the feedback digest. Each pointer must name the one owner; none may keep
    a close-out of its own.
    """
    mechanisms = {
        "driver": REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md",
        "house-keeping": REPO_ROOT / "skills" / "external" / "sdd-house-keeping" / "SKILL.md",
        "docs": REPO_ROOT / "skills" / "external" / "improve-docs" / "SKILL.md",
    }
    owner = ".specify/shared/workflow/artifact-commit-step.md"
    for name, path in mechanisms.items():
        text = read(path)
        assert owner in text, f"{name} must point at the one close-out owner ({owner})"
        assert re.search(r"Close-out|close-out", text), f"{name} must name the step it points at"

    # negative search: no second engine, no second entry point that performs a close-out
    engines = [
        p for p in list(REPO_ROOT.glob("scripts/python/*.py")) + list(REPO_ROOT.glob("scripts/bash/*"))
        if re.search(r"closeout", p.name, re.I)
    ]
    assert engines == [], f"a second close-out engine exists: {engines}"
    second_owners = [
        p for p in (REPO_ROOT / "shared").rglob("*.md")
        if re.search(r"^## .*[Cc]lose-out", p.read_text(encoding="utf-8"), re.M)
        and p.name != "artifact-commit-step.md"
    ]
    assert second_owners == [], f"a second close-out owner document exists: {second_owners}"


def test_the_instruction_surface_reaches_the_step_without_restating_it():
    """FR-022 — `closeout-verification.contract.md` C-7, decided by measurement.

    ``notes/pre-change-measurements.md`` recorded that the `## Git Workflow` section already
    reaches the close-out through the mechanism it names and the pointer chain it carries. The
    guard records that reading (so "no edit" is a measured conclusion) and asserts the section
    gained no restatement of the close-out rules.
    """
    measurement = read(NOTES / "pre-change-measurements.md")
    assert re.search(r"pointer line or a \"no edit\" by measurement", measurement), (
        "the T004 reading that decides this row must still be recorded"
    )
    for path in (INSTR_TEMPLATE, INSTR_LIVE):
        text = read(path)
        section_text = section(text, "Git Workflow") if "\n## Git Workflow" in text else text
        assert "close-out" in section_text, (
            f"{path.name}: the Git Workflow section must reach the close-out by name"
        )
        assert ".specify/workflow/git.md" in section_text, (
            f"{path.name}: the section must point at the git workflow state file"
        )
        # no restatement: the section must not carry the close-out's own rules
        for leak in ("Closeout remotes", "commit+merge+push", "stop at the first failure"):
            assert leak not in section_text, (
                f"{path.name}: the Git Workflow section must not restate {leak!r} — the owner "
                "is the shared workflow document, reached by pointer"
            )


# ============================================================================
# Polish — the mutation arms (T041 / T046 / T048 / T053)
#
# Each arm applies a *string substitution to an in-memory copy* and re-runs the same
# predicate the landed guard runs. No tracked file is written: the substitution never
# reaches disk, and the closure below is the landed guard's own body. An arm that
# reds proves the guard could red; an arm that stays green proves the guard is a
# presence check in disguise and must be rewritten (`closeout-verification.contract.md`
# C-6: "a green check is a claim, not evidence").
# ============================================================================


def _as_mutated(text: str, *substitutions: tuple[str, str]) -> str:
    """Apply plain string substitutions to a copy; every one must hit exactly once."""
    out = text
    for old, new in substitutions:
        assert out.count(old) == 1, f"mutation anchor {old!r} hits {out.count(old)} times"
        out = out.replace(old, new, 1)
    return out


def _is_red(assertion) -> bool:
    """Run one guard body; ``True`` when it raises, ``False`` when it stays green."""
    try:
        assertion()
    except Exception:  # noqa: BLE001 — any raise is the red we are looking for
        return True
    return False


def _failure_discipline_is_intact(text: str) -> None:
    """The landed body of ``test_failure_classes_and_the_no_retry_rule_are_stated``, over ``text``."""
    failure = section(text, "Failure discipline")
    flat = " ".join(failure.split())
    for phrase in ("merge conflict", "non-fast-forward rejection", "rejected push"):
        assert phrase in flat, f"failure class {phrase!r} must be named"
    assert re.search(r"no retry|never retry|No retry", failure), "the retry ban must be explicit"
    assert re.search(r"stops at that step", flat, re.I), "the line stops at the first failure"
    pushes = [m.group(0) for m in re.finditer(r"git\s+push[^\n`]*", text)]
    assert pushes, "the surface carries at least one push invocation"
    forced = [p for p in pushes if re.search(r"(^|\s)(--force|-f)(\s|$)", p)]
    assert forced == [], f"no bare force form may appear; found {forced}"
    for inv in pushes:
        if "--force" in inv:
            assert "--force-with-lease" in inv, f"forced form must be the lease variant: {inv}"
            assert "confirmation" in text.lower(), "the lease variant runs behind its confirmation"
    assert (
        "never force" in failure or "no `--force`" in failure or "No force" in failure
    ), "the failure discipline states that forcing is not a recovery path"


def test_mutation_an_injected_retry_reds_the_no_retry_guard():
    """T041 — FR-011 / SC-003: an automatic retry appended to the operation reds it.

    The retry is added as a *numbered step*, which is the shape a retry loop actually takes
    in this reference. It reds through the "stops at that step" read: once the run retries,
    the line no longer stops at the first failure — the exact property C-5 forbids. Removing
    the ban sentence alone does not red, and that limit is asserted instead of papered over:
    the predicate's retry arm reads the *positive* ban wording, so a deletion is caught by the
    sentence-disappearance, not by the run's shape.
    """
    text = read(CLOSEOUT_REF)
    assert not _is_red(lambda: _failure_discipline_is_intact(text)), (
        "the landed surface already reds the predicate — the arm would prove nothing"
    )
    mutated = _as_mutated(
        text,
        (
            "1. stops at that step",
            "1. retries the same step once",
        ),
    )
    assert _is_red(lambda: _failure_discipline_is_intact(mutated)), (
        "an injected retry stayed green — the guard reads the retry vocabulary but not the "
        "run's shape, so it cannot fail for the reason FR-011 names"
    )


def test_mutation_a_behavioural_retry_loop_reds_the_no_retry_assertions():
    """T041 — FR-011 / SC-003, the *behavioural* retry arm, on a real fixture repository.

    The structural mutation above reads the reference's wording. This arm mutates the driver's
    behaviour instead: the fixture exposes ``attempt_retry``, so retry = 0 is the landed driver
    and retry = 2 is a driver that re-issues the failing step. The SAME predicate the two
    failure tests assert must hold under retry = 0 and break under retry = 2 — otherwise the
    two behavioural arms prove "the run failed" but not "the run did not retry".

    Measured 2026-11-09: the driver's retry loop sits on the **push** step only, so the
    rejected-push arm reds (a bare remote refuses every attempt, and the retry count comes back
    on the outcome) while the merge-conflict arm stays green (a conflicted merge is never
    retried by any variant). Both readings are asserted here so the limit is recorded by a
    test rather than by prose.
    """
    from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout

    # --- arm A: rejected push — the retry loop is observable and the arm reds --------------
    def rejected_push(attempt_retry: int):
        with build_repo("single-branch") as repo:
            _advance_remote(repo)
            before = repo.remote_branch_sha("mirror", "master")
            plan = derive_closeout(
                model="single-branch", strategy="commit+merge+push",
                remotes=["mirror"], readonly=[],
            )
            outcome = run_closeout(
                repo, plan, paths=_seed_record(repo), attempt_retry=attempt_retry
            )
            return outcome, before, repo.remote_branch_sha("mirror", "master")

    landed, before, after = rejected_push(0)
    assert landed.exit_code != 0 and landed.stage == "push", "the landed driver fails at the push"
    assert after == before, "and the remote is not force-overwritten"
    assert landed.retries == 0, f"the landed driver performs no retry, read {landed.retries}"

    mutated, before_m, after_m = rejected_push(2)
    assert mutated.exit_code != 0 and mutated.stage == "push", (
        "the mutated driver still fails — a bare remote refuses every attempt"
    )
    assert after_m == before_m, "and still never forces over the remote"
    assert mutated.retries > 0, (
        "the injected retry did not fire, so this arm proves nothing about FR-011"
    )

    # --- arm B: merge conflict — recorded limit, not papered over --------------------------
    def merge_conflict(attempt_retry: int):
        with build_repo("dual-branch") as repo:
            repo.git("commit", "-q", "--allow-empty", "-m", "seed: archive line base")
            repo.git("update-ref", "refs/heads/archive", "HEAD")
            repo.git("checkout", "-q", "archive")
            target = repo.repo / "conflict.txt"
            target.write_text("archive line\n", encoding="utf-8")
            repo.git("add", "--", "conflict.txt")
            repo.git("commit", "-q", "-m", "archive: divergent edit")
            repo.git("checkout", "-q", "develop")
            target.write_text("daily line\n", encoding="utf-8")
            repo.git("add", "--", "conflict.txt")
            repo.git("commit", "-q", "-m", "daily: divergent edit")
            plan = derive_closeout(
                model="dual-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
            )
            return run_closeout(
                repo, plan, paths=_seed_record(repo), conflict=True, attempt_retry=attempt_retry
            )

    landed_m = merge_conflict(0)
    mutated_m = merge_conflict(2)
    assert landed_m.stage == "merge" and landed_m.pushed == (), "the landed run stops at the merge"
    assert mutated_m.stage == "merge" and mutated_m.pushed == (), (
        "the merge arm is unchanged by the retry hook — its guarantee is 'no push after a "
        "failed merge', which the hook does not touch"
    )
    assert mutated_m.retries == 0, (
        "recorded limit (mutations.txt § R-21b): the retry hook is a push-step hook, so the "
        "merge arm proves 'stops at the merge' but not 'the retry would have been caught here'"
    )


def test_mutation_a_bare_force_form_reds_the_no_retry_guard():
    """T041 — the second half: a bare force push is not a recovery path."""
    text = read(CLOSEOUT_REF)
    mutated = _as_mutated(text, ("It performs **no `--force`**.", "It performs `--force` when needed."))
    assert _is_red(lambda: _failure_discipline_is_intact(mutated)), (
        "a bare --force form stayed green under the failure-discipline read"
    )


#: The gate owner's subjects, one subject per row of its table. Every row the owner publishes
#: is a *subject* the close-out must reach by pointer and never name
#: (`closeout-lifecycle.contract.md` C-6: "cites no gate by name"). The reading is
#: structural — the second table column of the owner file — so it moves with the owner.
GATE_OWNER_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|", re.M)


OWNED_LIST_HEADING = "## 治理保留清单"
#: The destructive list's rows are the bullet items under it (its owner enumerates them there).
DESTRUCTIVE_ROW_RE = re.compile(r"^- ([^\n]+)$", re.M)


def gate_owner_subjects(owner_text: str) -> list[str]:
    """The rows the owner publishes — governance-kept table rows and destructive bullets alike.

    Read structurally (table first column, top-level bullets of the destructive list), so the
    reading moves with the owner instead of pinning a copy of its wording.
    """
    _before, _sep, after = owner_text.partition(OWNED_LIST_HEADING)
    assert _sep, "the owner lost its governance-kept list — the reading would be empty by accident"
    body = after.split("\n## ", 1)[0]
    rows = [
        m.group(1) for m in GATE_OWNER_ROW_RE.finditer(body)
        if not set(m.group(1)) <= {"-", " "}
    ]
    bullets = DESTRUCTIVE_ROW_RE.findall(owner_text)
    subjects = [re.sub(r"^\*\*(.+?)\*\*.*$", r"\1", s) for s in rows + bullets]
    return [s for s in subjects if len(s) > 6]


def _copied_gate_list(surface_text: str) -> list[str]:
    """Gate subjects the surface names verbatim instead of reaching them by pointer (`[]` = clean)."""
    subjects = gate_owner_subjects(read(REPO_ROOT / GATE_OWNER))
    assert len(subjects) >= 5, f"the gate owner publishes {len(subjects)} subjects — nothing to copy"
    return [s for s in subjects if s in surface_text]


def _hand_off_is_intact(surface_text: str) -> None:
    """The hand-off read: the pointer is present AND no gate subject is copied into the surface."""
    assert GATE_OWNER in surface_text, "the surface must reach the gate owner by pointer"
    flat = " ".join(surface_text.split())
    assert re.search(
        r"stops? and presents|stops? at that step|presented before it runs", flat, re.I
    ), "the surface must state that a destructive or governance-kept step stops and presents"
    copied = _copied_gate_list(surface_text)
    assert copied == [], f"the surface copies gate subjects instead of pointing at them: {copied}"


def test_the_hand_off_points_at_the_gate_owner_instead_of_restating_it():
    """R-20 — `closeout-lifecycle.contract.md` C-6, on both surfaces that describe the step.

    The stop is stated once per surface and the list stays with its owner: a surface may name
    the owner's path, and may name a *class* of action in its own words (the contract's "a
    destructive or governance-kept step"), but must not carry the owner's own rows.
    """
    for surface in (COMMIT_STEP, CLOSEOUT_REF):
        _hand_off_is_intact(read(surface))


def test_mutation_a_gate_list_copied_into_a_surface_reds_the_pointer_guard():
    """T046 — SC-004: gate subjects copied as plan text replace the pointer and red the guard."""
    subjects = gate_owner_subjects(read(REPO_ROOT / GATE_OWNER))
    assert len(subjects) >= 5, f"the gate owner publishes {len(subjects)} subjects — nothing to copy"
    for surface in (COMMIT_STEP, CLOSEOUT_REF):
        text = read(surface)
        assert not _is_red(lambda: _hand_off_is_intact(text)), (
            f"{surface.name} already reds the reading — the arm would prove nothing"
        )
        # Append the copied rows to the surface's *last* mention of the owner: a restatement
        # rides beside its pointer, which is exactly the shape the clause forbids.
        at = text.rindex(GATE_OWNER) + len(GATE_OWNER)
        copied = (
            text[: at - len(GATE_OWNER)]
            + "%s（本步保存的清单：%s、%s、%s）" % (GATE_OWNER, subjects[0], subjects[1], subjects[2])
            + text[at:]
        )
        assert copied.count(GATE_OWNER) == text.count(GATE_OWNER)
        assert _is_red(lambda: _hand_off_is_intact(copied)), (
            f"{surface.name}: three of the owner's subjects copied into the surface stayed green "
            "— the hand-off read is a pointer-presence check, not a no-restatement check"
        )


def _gate_comparison_is_intact(current: set[str], surfaces: tuple[Path, ...]) -> None:
    """The landed body of ``test_the_destructive_boundary_did_not_shrink_by_gate_name``."""
    baseline = {f"gate-{n:03d}" for n in range(1, 28)}
    assert current, "the same-run scan reports no gates"
    assert baseline - current == set(), f"the destructive boundary shrank: {baseline - current}"
    for surface in surfaces:
        leaked = re.findall(r"gate-\d{3}", read(surface))
        assert leaked == [], f"{surface.name} cites a gate by id: {leaked}"


def test_mutation_a_dropped_gate_id_reds_the_closed_set_comparison():
    """T048 — SC-004: one gate removed from an in-memory copy of the same-run scan reds it."""
    surfaces = (CLOSEOUT_REF, COMMIT_STEP, SKILL_MD)
    current = live_gate_ids()
    assert not _is_red(lambda: _gate_comparison_is_intact(current, surfaces)), (
        "the live scan already reds the comparison — the arm would prove nothing"
    )
    shrunken = set(sorted(current)[1:])
    assert len(shrunken) == len(current) - 1, "the in-memory copy must drop exactly one gate"
    assert _is_red(lambda: _gate_comparison_is_intact(shrunken, surfaces)), (
        "dropping one gate id stayed green — the comparison is not discriminating"
    )


def test_mutation_a_second_closeout_owner_reds_the_single_owner_search():
    """T053 — SC-005: a second entry point carrying its own close-out reds the negative search."""
    text = read(REPO_ROOT / "shared" / "workflow" / "artifact-commit-step.md")
    others = [
        p for p in (REPO_ROOT / "shared").rglob("*.md")
        if p.name != "artifact-commit-step.md"
    ]
    assert not _is_red(lambda: _second_owner_list(others)), (
        "the tree already carries a second close-out owner"
    )
    synthetic = "## Close-out\n\nThis file performs its own close-out.\n"
    assert _is_red(lambda: _second_owner_list(others, extra=synthetic)), (
        "a second owner document carrying `## Close-out` stayed green"
    )


def _second_owner_list(paths, extra: str | None = None) -> None:
    """The landed negative search over ``paths``, plus one synthetic in-memory document."""
    found = [
        p for p in paths
        if re.search(r"^## .*[Cc]lose-out", p.read_text(encoding="utf-8"), re.M)
    ]
    if extra is not None and re.search(r"^## .*[Cc]lose-out", extra, re.M):
        found.append("synthetic")
    assert found == [], f"a second close-out owner document exists: {found}"
