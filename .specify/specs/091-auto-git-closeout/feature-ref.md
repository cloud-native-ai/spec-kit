# Feature Reference — 091-auto-git-closeout

**Feature ID**: 091 | **Feature Name**: Automatic git Close-out（自动收口）
**Requirement key**: `091-auto-git-closeout` | **Branch**: `091-auto-git-closeout`
**Status at this stage**: `Draft → Clarified → Planned` | **Date**: 2026-11-09

## Binding

| Item | Value |
|------|-------|
| Spec directory | the spec directory of requirement key 091-auto-git-closeout |
| Stage status so far | requirements done (27 FR / 7 SC) → clarify done (28 FR / 8 SC) → plan done (this file refined) |
| Flow class | `execution` (`**Flow Class**` line in the requirements file) |
| Policy owner | the workflow state file's managed block (git-utils scope A) |
| Lifecycle owner | the canonical artifact-commit step |

## Why this file exists (clarify C-1)

`overlap-check.py` compares the **current** feature's delivery surface only when the feature
declares it. Without this file the check falls back to `tasks.md` / `plan.md`; neither exists at
clarify, so the gate returned `clear` with the note *"current feature has no declaration
artifact"* and compared **nothing** (`checked_specs` = the current spec alone, overlaps 0). That
green is vacuous, and the driver's efficiency model names this file as the receipt surface for
an overlap adjudication. It is created here.

**Declaration discipline.** This file lists only paths the feature will *write*; a document it
reads, cites or preserves is not a deliverable. Paths are written as bare backticked tokens
because that is what the checker reads — so a read-only document is named without a path-shaped
token, and does not turn into a phantom collision.

**Plan refinement (2026-11-09).** The inventory below is the plan's version of the same list. Two
rows moved: the git skill's command surface is now a **new sibling reference** rather than an
addition to the existing three-tier reference (`research.md` R4), and the instructions template
row is **contingent** on implement finding the existing line insufficient (`research.md` R10).

## Delivered paths (inventory, refined at plan)

| # | Path | Kind | FR |
|---|------|------|----|
| 1 | `.specify/workflow/git.md` | edit — two declaration rows inside the managed block (this project's own runtime state: it carries an instance, not the shipped template) | FR-001, FR-002 |
| 2 | `skills/external/git-utils/assets/git-workflow-block.md` | edit — the shipped block template gains both rows in placeholder form | FR-004 |
| 3 | `skills/external/git-utils/SKILL.md` | edit — scope A gains the named `closeout` operation and its three-input positioning | FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016 |
| 4 | the new sibling close-out reference under `skills/external/git-utils/references/` | **NEW sibling reference** — the close-out command surface's home (plan decision, `research.md` R4); the existing three-tier reference only gains a one-line pointer | FR-010, FR-011 |
| 5 | `shared/workflow/artifact-commit-step.md` | edit — the close-out step, its records-commit semantics, three forks, and the revised push boundary | FR-005, FR-006, FR-007, FR-008 |
| 6 | `shared/definitions/probe-definitions.md` | edit — one wrap-up handler row (or one handler plus bindings) expressing the close-out step; the faces are then compiled, never hand-written | FR-021 |
| 7 | `shared/workflow/external-dispatch-recipes.md` | edit, **contingent** — measured at plan: the dispatcher copies the *wording* of three discipline defaults (see its stage-prompt skeleton), not a numbered wrap-up sequence, so no edit is expected; implement edits it only if the new step makes the copied default stale | FR-020 |
| 8 | `templates/instructions-template.md` | edit, **contingent — default is no edit** — measured at plan: its Git Workflow section already names close-out and is byte-identical to the live instructions section, so at most one pointer line is added, and only if implement finds a reader cannot reach the step from it | FR-022 |
| 9 | the contract test tree's `test_git_closeout_contract.py` (a new module in the repository's existing contract test suite) | **NEW** guard module: the two declarations and their value domain, the four model sequences, the pointer duties, the absence of a second branch table, and the SC-004 / SC-008 closed-set claims | FR-023, FR-024, FR-027, SC-008 |
| 10 | the `git-closeout` fixture directory (a new sibling under the repository's existing test-fixture tree, mirroring how sibling features keep one fixture directory each) | **NEW** — one fixture repo + one local bare remote per workflow model, built under a sanctioned temp root and torn down per test | FR-024, FR-025 |
| 11 | the compiled wrap-up faces of every artifact-producing command and skill | **generated**, not authored — the probe engine's `compile-embeds` output, reached through row 6 | FR-021 |

Every path above reaches the runtime tree through the framework's own sync entries (mirror and
per-tool command copies), so none of them is written twice by hand.

## Deliberate non-deliverables

Recorded so a reader does not go looking for them in the delivery commit. Each is named by role,
not by a path token, so the checker sees no claim:

- **No new skill directory, no engine script, no `/speckit.*` command** (FR-027).
- **The confirmation-gates owner** — not edited. It stays the sole owner of the destructive list;
  this feature references it (FR-018).
- **The closed-set-claims owner** — consumed, not amended.
- **The fast-fail owner** — referenced only.
- **The SDD loop driver skill and its whole references tree** — no path delivered. Clarify C-14:
  the driver's U6 close becomes an instance of this feature's owner statement, so the driver and
  its decomposition model (whose "does not push" sentence stays true) are read, never rewritten.
  This is the largest read-only adjacency and was the reason an earlier draft of this file
  reported 64 phantom collisions against one completed feature line.
- **The record-retention engine and the cross-cutting-lessons page** — consumed facts (the
  record-consumption lifecycle in C-10a; the blind-check lesson behind C-11c), not deliverables.
- **The mirror-sync and command-copy generators** — run, never edited.

## Consuming / Consumed Owners

| Relation | Owner (by role) | Note |
|----------|-----------------|------|
| edits | the workflow state file's managed block | the two close-out declarations; the block already owns model, branch roles and remote roles |
| edits | the canonical artifact-commit step | the close-out lifecycle step and its records-commit semantics |
| edits | the git skill's scope A | the `closeout` operation |
| consumes | the confirmation-gates owner | destructive class kept, never restated (FR-018) |
| consumes | the closed-set-claims owner | the admissible-elements rule SC-004 / SC-008 are judged by |
| consumes | the probe registry's handler and binding tables | one row added, no rule restated |
| consumes | the record-retention engine reached through the sanitize skill | the record-consumption lifecycle the close-out receipt feeds (C-10a) |
| preserves | the fast-fail owner (dispatch-time injection clause) | referenced only |

## Plan refinement — FR → contract map

Every functional requirement is discharged by a named clause; a clause column empty for an FR would mean an
unplanned requirement.

**Re-verified at the analyze-repair round (2026-11-09).** C-01 measured that FR-020 / FR-021 / FR-022 / FR-027 were
cited by zero clause — the four map rows below pointed at clauses whose *subject* was something else (a lifecycle
position, a delivery row). M-08 found six more rows of the same shape. The map is now checked mechanically rather than
by reading: `account-clause-coverage.py --spec-dir` reports **FR claimed 28 / FR uncovered 0** by reading each clause's
citation group, so a row that stops being true turns the account red. The check reads a clause's **last
FR-containing parenthetical**, which is why each clause ends with its citation group rather than mentioning ids earlier
in the body.

| FR | Discharging clause(s) |
|----|-----------------------|
| FR-001 | `closeout-declaration.contract.md` C-1, C-3 |
| FR-002 | C-1, C-4; `closeout-executor.contract.md` C-7 |
| FR-003 | `closeout-declaration.contract.md` C-2, C-6 |
| FR-004 | C-1 (both surfaces: the shipped asset and this project's instance) |
| FR-005 | `closeout-lifecycle.contract.md` C-1 |
| FR-006 | C-2 (one records commit, per-class coverage) |
| FR-007 | C-4, C-5 |
| FR-008 | C-7 (the old sentence named, and absent from every surface) |
| FR-009 | `closeout-executor.contract.md` C-1, C-2 |
| FR-010 | C-3 |
| FR-011 | C-5 |
| FR-012 | C-5; `closeout-lifecycle.contract.md` C-6 |
| FR-013 | `closeout-declaration.contract.md` C-4; `closeout-executor.contract.md` C-7 |
| FR-014 | `closeout-lifecycle.contract.md` C-5; `closeout-executor.contract.md` C-6 |
| FR-015 | `closeout-executor.contract.md` C-4 |
| FR-016 | C-2; `closeout-declaration.contract.md` C-5 |
| FR-017 | `closeout-declaration.contract.md` C-7; `closeout-executor.contract.md` C-8; `closeout-lifecycle.contract.md` C-6 |
| FR-018 | `closeout-declaration.contract.md` C-7; `closeout-lifecycle.contract.md` C-6 (both reference the owner, neither restates it) |
| FR-019 | `closeout-declaration.contract.md` C-3; `closeout-executor.contract.md` C-8 |
| FR-020 | `closeout-lifecycle.contract.md` C-8 (the one step, reached by pointer; no second implementation) |
| FR-021 | `closeout-lifecycle.contract.md` C-9 (faces rendered by the registry, never authored) |
| FR-022 | `closeout-lifecycle.contract.md` C-10; `closeout-verification.contract.md` C-7 (the measured pointer duty) |
| FR-023 | `closeout-verification.contract.md` C-1 |
| FR-024 | C-2, C-3 |
| FR-025 | C-5 |
| FR-026 | C-4, C-6 (the closed-set claim with its three named elements) |
| FR-027 | `closeout-executor.contract.md` C-1 (the five non-goals as an owned negative assertion) |
| FR-028 | `closeout-lifecycle.contract.md` C-3 (receipt, never a rewrite) |

**Clause count after the repair: 32** — declaration C-1…C-7 (7), lifecycle C-1…C-10 (10), executor C-1…C-8 (8),
verification C-1…C-7 (7). The 26-clause reading in `plan.md` and `tasks.md` is the pre-repair state; the green partition
is re-cut in `tasks.md` § Green Partition so each of the 32 clauses is claimed exactly once.

## Plan refinement — SC → measurement map

| SC | Measurement | Carrier |
|----|-------------|---------|
| SC-001 | four fixture repositories, end-state assertions (branches, HEAD, remote contents); the roster itself is `data-model.md` E-6's, never repeated here | `closeout-verification.contract.md` C-2 |
| SC-002 | declaration rows + value domain read from both surfaces; illegal value / deleted row mutations | `closeout-declaration.contract.md` C-1, C-3; verification C-1 |
| SC-003 | two failure fixtures (push rejected, merge conflict) + an injected-retry mutation | verification C-3 |
| SC-004 | confirmation-gate scan compared against a same-run baseline **by name**, plus "no surface copies the list" | verification C-4, C-6 |
| SC-005 | pointer existence from each unattended mechanism, plus a negative search for a second close-out implementation | `closeout-lifecycle.contract.md` C-8; verification C-7 |
| SC-006 | the dry-run record on this repository (no push, no remote change) | verification C-5; `quickstart.md` S-7 |
| SC-007 | the two wrap-up forks asserted separately (skip-with-one-line; records-free merge+push tells the truth) | `closeout-lifecycle.contract.md` C-4, C-5 |
| SC-008 | the three named elements inside the SC-004 test, plus two mutation arms | verification C-4, C-6 |

## Plan refinement — disclosed rulings

Three rulings were made while planning and are recorded so a later stage does not re-derive them.

- **Ruling P-1 — the command surface gets a sibling reference, not a taller one.** The close-out sequences do not
  belong to the page about three-tier operations. `research.md` R4 records the measurement that makes the split the
  mechanism fix rather than a stylistic choice. Delivery row 4 changed shape accordingly.
- **Ruling P-2 — the instructions template defaults to no edit.** The `## Git Workflow` section already names
  close-out and is byte-identical between the shipped template and this project's live instructions (`research.md`
  R10). Row 8 stays contingent.
- **Ruling P-3 — an existing equality pin on the confirmation-gate total is not re-asserted.** Measured:
  `tests/contract/test_wrap_up_wording_gate_safe.py` asserts the total equals a literal and calls it the owner fact.
  This feature's guards compare **sets by name** against a same-run baseline and introduce no second constant; if a
  later change moves the total, that pin's owner re-rules first (`research.md` R7 / plan finding F-2).

  This is a `tasks`-visible constraint, not a licence: the guard module MUST NOT be written as `assert total == 27`.

## Adjacency

- **Within the framework's hot trees**: rows 2–4 land in the git skill; 089 touched that skill
  only through the script version bridge shared by every script, not through its prose. Rows 5–9
  are the shared workflow, definition and template trees every feature reads; these edits are
  additive and pointer-shaped.
- **Measured, not asserted**: the pre-declaration run compared nothing (`checked=1`,
  `overlaps=0`, note *no declaration artifact*); the post-declaration run compares 82 sibling
  specs and reports **36 overlaps over 5 paths, all `same-path` except 2 `nested-path`**, all
  against **completed** feature lines, and **none against an active line** — the line registry's
  active set is empty at this moment (`line-registry.py --action list --active` → `[]`), so no
  other line can be writing these paths concurrently. The adjudication is recorded in the
  spec's Clarifications (C-16) and the state spine rather than dropped silently.
- **The 5 colliding paths and their ownership rule**: the four shared documents
  (`probe-definitions`, the artifact-commit step, the dispatch recipes, the instructions
  template) are *shared registries by design* — many completed lines have edited them in the
  past and none owns them; this feature's edits are additive and it inherits the existing
  convention, so the owner stays the document itself. The git skill is the only feature-specific
  collider, and C-16 records why the last three touches there (059/062/063) are sequential. The
  two `nested-path` rows pair this feature's `shared/definitions/probe-definitions.md` with 089's
  / 090's `shared/definitions` claim: a file inside a directory another line declared — nesting
  only, no ownership conflict.
- **Re-measure before the first write**: implement must re-run the overlap check rather than
  inherit this reading, because four declared trees are the framework's hot spots.
- **Plan-stage re-measure (2026-11-09)**: the check was re-run after this file's refinement and returned the same
  reading (`checked=82`, `overlaps=36`, all against completed lines, zero active); evidence
  `test-evidence/overlap-check-plan.json` and `test-evidence/plan-gates.txt` § 3.

## Stage status

| Stage | State | Artifact |
|-------|-------|----------|
| requirements | done | requirements file |
| clarify | done — 16 adjudications (C-1…C-16), FR 28 / SC 8, 3 edge cases, 9 assumptions added; the overlap check run before **and** after this file | requirements Clarifications, this file |
| plan | done — research (R1…R12), data model (6 entities / 17 rules), 4 contract pages (**32 clauses after the analyze-repair round; 26 at the plan baseline**), 8 quickstart scenarios, 5 decision-tension records, 7 execution premises; delivery surface refined (rows 4, 8, 9, 10) | plan.md, research.md, data-model.md, contracts/, quickstart.md, this file |
| tasks / checklist / analyze / implement / review | analyze round 1 done (1C + 4H blocking) → **analyze-repair done 2026-11-09** (C/H resolved, 32 clauses, FR 28/28) → analyze round 2 pending | `test-evidence/analyze-round1-findings.md`, `test-evidence/analyze-repair-round1.md` |
