# Feature Reference — 091-auto-git-closeout

**Feature ID**: 091 | **Feature Name**: Automatic git Close-out（自动收口）
**Requirement key**: `091-auto-git-closeout` | **Branch**: `091-auto-git-closeout`
**Status at this stage**: `Draft → Clarified` | **Date**: 2026-11-09

## Binding

| Item | Value |
|------|-------|
| Spec directory | the spec directory of requirement key 091-auto-git-closeout |
| Stage status so far | requirements done (27 FR / 7 SC) → clarify done (28 FR / 8 SC; this file added) |
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

## Delivered paths (inventory, refined at plan)

| # | Path | Kind | FR |
|---|------|------|----|
| 1 | `.specify/workflow/git.md` | edit — two declaration rows inside the managed block (this project's own runtime state: it carries an instance, not the shipped template) | FR-001, FR-002 |
| 2 | `skills/external/git-utils/assets/git-workflow-block.md` | edit — the shipped block template gains both rows in placeholder form | FR-004 |
| 3 | `skills/external/git-utils/SKILL.md` | edit — scope A gains the named `closeout` operation and its three-input positioning | FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016 |
| 4 | `skills/external/git-utils/references/execute-commands.md` | edit — the close-out command surface's home; whether it extends this reference or adds a sibling is a plan decision | FR-010, FR-011 |
| 5 | `shared/workflow/artifact-commit-step.md` | edit — the close-out step, its records-commit semantics, three forks, and the revised push boundary | FR-005, FR-006, FR-007, FR-008 |
| 6 | `shared/definitions/probe-definitions.md` | edit — one wrap-up handler row (or one handler plus bindings) expressing the close-out step; the faces are then compiled, never hand-written | FR-021 |
| 7 | `shared/workflow/external-dispatch-recipes.md` | edit, **contingent** — only if the dispatcher's wrap-up copy restates a step order the new step makes stale (measured at plan) | FR-020 |
| 8 | `templates/instructions-template.md` | edit — at most one pointer line in the Git Workflow section, and only if plan finds the existing line insufficient | FR-022 |
| 9 | `tests/contract/` | NEW contract tests: the two declarations and their value domain, the four model sequences, the pointer existence, the absence of a second branch table, and the closed-set claim of SC-004 | FR-023, FR-024, FR-027, SC-008 |
| 10 | the git-closeout fixture root (a directory under the tests fixtures tree, named at plan) | NEW — one fixture repo plus a fake remote per workflow model (the fixture root is a plan decision) | FR-024, FR-025 |
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

## Stage status

| Stage | State | Artifact |
|-------|-------|----------|
| requirements | done (27 FR / 7 SC, 12 assumptions) | requirements file |
| clarify | **this stage** — 16 adjudications (C-1…C-16), FR 28 / SC 8, 3 edge cases, 9 assumptions added; the overlap check run before **and** after this file | requirements Clarifications, this file |
| plan / tasks / checklist / analyze / implement / review | not started | — |
