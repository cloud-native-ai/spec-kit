# Implementation Plan: 071-review-code-integration

**Branch**: `071-review-code-integration` | **Date**: 2026-10-27 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition）
**Input**: Specification from `.specify/specs/071-review-code-integration/requirements.md`

## Summary

Feature 071 composes an existing, currently unreferenced capability into a command that needs it. `/speckit.review` today delegates only to `review-sdd-process` and explicitly refuses to judge code; the `code-review` skill is a complete code-review loop that no command calls. After this feature, one `/speckit.review` invocation runs two segments in a fixed order — the process segment first and unconditionally, the code segment second and applicability-triaged — writes two artifacts into the feature directory, and reports both conclusions while keeping the two severity vocabularies apart.

The technical approach is deliberately thin. The command template only orchestrates and points. The code segment's determinism (which commits are reviewed, which files were judged, whether the merge gate allows) moves into subcommands of the skill's existing script, so an unattended run can finish without a terminal, without a renderer, and without improvising a diff base from a branch name. The "was the whole diff read" question stops being a matter of trust and becomes a coverage receipt whose file set must equal the changed-file set and whose gap exits non-zero. The renderer's absence stops being a stop condition and becomes a labelled text mode, with the anti-pretense rule kept verbatim in the rewritten clause.

One governance convergence rides along because the composition forces it: the `Implemented → Ready for Review` criteria exist twice and disagree, so the state-machine owner keeps them and the integration protocol's summary row becomes a reference. That single edit is why one existing pin changes; the change is disclosed, and it gains assertions rather than losing them.

**Run input classification** (the planning skill's step 2): the dispatch brief arrived as run parameters — background facts, scope boundaries, and the non-negotiables already adjudicated in the requirements — not as a new requirement set. No mid-run addendum arrived, so `requirements.md` was not restructured and no upstream gate needed re-running.

## Technical Context

**Language/Version**: Bash 3.2+/4 for the extended skill script (this host runs bash 5.x, `git 2.43.5`); Markdown for the command template, the two skill bodies, the report template, the state-machine owner, and the docs page; Python 3.8+ for the contract tests (this host runs 3.11.11, pytest 8.4.2).
**Primary Dependencies**: none new. Reuses `git`, the existing `git-delta-review.sh` entity, the existing pytest suites, `sync-mirrors.py`, and `regen-command-copies.py`. `delta` stays an optional external binary — its absence is a labelled mode, never a dependency.
**Storage**: files only — `review.md` and `code-review.md` in the feature directory, plus per-run archive files. No database, no sidecar receipt file, no new store, no daemon.
**Testing**: pytest contract suites (`tests/contract/`), one file per FR-028 behavior; the receipt and base-resolution tests drive the real script inside a temporary git repository; the docs/template isomorphism test compares declared surfaces. Tests Mode = **ON** (red-first for every new group).
**Target Platform**: the framework's own repository plus every consuming project; macOS/Linux shells; hosts with or without `delta`; hosts with or without a TTY.
**Project Type**: SDD framework (prompt templates, skills, shared workflow docs, contract tests) — no application runtime is added.
**Performance Goals**: not a performance feature. The only measurable cost claim is that the code segment adds no full-suite run and no new engine invocation beyond the existing script's subcommands; a review run's added work is `git diff --numstat` plus one pass over the changed-file list.
**Constraints**: no new command, skill, agent, dependency, network call, service, or resident process; no second registry, ledger, aggregate, or intake store; no hand-edited runtime projection; no edit to the probe registry (both wrap-up faces already registered); no push.
**Scale/Scope**: two segments, two artifacts, one receipt block with a closed twelve-name field set plus per-file rows, four segment-verdict values, three applicability values, three base-resolution tiers, six contract files, one intentional pin update.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Same-author condition (disclosed, per `shared/workflow/objective-analysis-gate.md` rule 7)**: these design artifacts were authored in this session, and this execution environment exposes no subagent dispatch capability, so the detection pass could not be delegated. Every row below therefore carries `(direct read, subagent unavailable)`; the program-derivable checks were actually executed instead — `pre-analyze-check.py --stage plan`, `clause_extract.py`, `sync-mirrors.py --check` on three pairs, `regen-command-copies.py --check`, and the neighbouring contract suites (evidence in `test-evidence/`).

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design section cites FR groups; each of the 28 requirements is cited from a contract clause's citation group (`feature-ref.md` § 3); no untraced technical choice (direct read, subagent unavailable) |
| II | Feature-Centric Development | ✅ Pass | Feature 071 already bound and registered; this stage advances `Draft → Planned` and records key changes in `features/071.md`; no second row (direct read, subagent unavailable) |
| III | Intent-Driven Development | ✅ Pass | The requirements' what/why precede this how; `research.md` records every alternative rejected (parallel segments, merged report, mode parameter, `HEAD~N`, newest-file verdict) (direct read, subagent unavailable) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Six new contract groups, red-first per `contracts/tests-and-docs-sync.md` C-65/C-66; the receipt and base tiers are proven against a temporary git repository, not against prose (direct read, subagent unavailable) |
| V | AI Agent Integration Standards | ✅ Pass | No provider, config key, or agent roster change; per-tool command copies are regenerated, not hand-written (`regen-command-copies.py --check` measured clean) (direct read, subagent unavailable) |
| VI | Continuous Quality & Observability | ✅ Pass | Deterministic exit codes (0/1/2) reused from the repo's existing gate convention; record header fields fixed; no speculative feature added (direct read, subagent unavailable) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan respected; status ceiling `Planned`; no gate exception; deferred-task and verification rules untouched (direct read, subagent unavailable) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 re-measured the script, the tests, the two status tables, and this repository's own git topology before deciding; `research.md` quotes the outputs (direct read, subagent unavailable) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Everything lands on existing artifacts; the receipt is a block in an existing file; no engine, service, scheduler, or new storage; the sequencing rule is prompt-level (direct read, subagent unavailable) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic names under this spec (`contracts/`, `quickstart.md`); no reserved ALL-CAPS name added; `skills/*/SKILL.md` keeps its mandated name (direct read, subagent unavailable) |
| XI | Dogfooding (Self-Application) | ✅ Pass | The feature rides its own SDD chain; framework sources are the only edit surface with generators producing the projections; the pin change is logged rather than silently absorbed (direct read, subagent unavailable) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Extends the existing script entity instead of generating a new one; no Tool record covers base resolution or a coverage receipt, so writing them there is the expected outcome (direct read, subagent unavailable) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Change Validation (a receipt that cannot be faked) and Controlled Execution (a non-interactive path); no new scoring system, and no improvement claim beyond configured ≠ used (direct read, subagent unavailable) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The gate criterion keeps one declared owner and the copy becomes a reference; the renderer's two literal forms are one write with a test asserting equality; shared strings are referenced, not copied (direct read, subagent unavailable) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Every value the command reports is a closed literal set; the quickstart carries execution status and premises per example; internal engine call forms stay out of the reader's path (direct read, subagent unavailable) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The two collisions found in Phase 0 — the C-15 pin versus the copy-convergence, and the newest-file verdict defect — are surfaced as a disclosed pin change and a clause, not silently patched; the subagent-unavailable condition is disclosed (direct read, subagent unavailable) |

**Gates Status**: ✅ All gates pass. No ❌ and no ⚠ row, so Complexity Tracking is N/A. The one intentional pin change is a design decision recorded in `research.md` § R5, not a gate violation.

**Re-check after Phase 1** (2026-10-27, after the artifacts landed): the same sixteen rows remain ✅ Pass. New evidence: `data-model.md` (13 entities, 28 validation rules), six contract files with 73 clauses, `quickstart.md` with eight scenarios each carrying an execution status, and the executed programme checks in `test-evidence/`. No new violation; no Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/071-review-code-integration/
├── plan.md                 # This file
├── research.md             # Phase 0 decisions R1–R14 (standalone: >50 lines, external-source evaluation)
├── data-model.md           # Phase 1: entities E1–E13 + validation rules V1–V28
├── contracts/              # Phase 1: six contract files, clauses C-1…C-73
│   ├── command-orchestration.md
│   ├── code-review-skill.md
│   ├── coverage-receipt.md
│   ├── status-gate-ownership.md
│   ├── feedback-and-boundaries.md
│   └── tests-and-docs-sync.md
├── quickstart.md           # Phase 1: scenarios A–H with execution status and premises
├── feature-ref.md          # Phase 1: binding, delivery surface, FR/SC coverage, disclosed deviations
├── checklists/
│   └── requirements.md     # Requirements-stage quality checklist (unchanged)
├── test-evidence/          # deterministic check records
├── tasks.md                # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md         # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
templates/
├── commands/review.md              # two-segment orchestration, triage, failure propagation, pointers
├── review-template.md              # + § 2.1 code-segment subsection (verdict + pointers)
└── feature-details-template.md     # Implemented → Ready for Review row becomes the full criterion (owner)

shared/workflow/
└── feature-integration.md          # status rows converge to references to that owner

skills/internal/code-review/
├── SKILL.md                        # non-interactive path, base tiers, header/rotation, rewritten renderer clause, boundary
├── scripts/git-delta-review.sh     # + base / start / receipt subcommands; report gains --file and exit codes
└── references/delta-setup.md       # renderer-absence wording aligned with the rewritten clause

skills/internal/review-sdd-process/
└── SKILL.md                        # description + Boundaries: distinct objects, composed by the command

docs/reference/commands/
└── review.md                       # the composed command surface

tests/contract/
├── test_review_code_composition.py     # NEW
├── test_code_review_skill_contract.py  # NEW
├── test_coverage_receipt.py            # NEW
├── test_status_gate_owner.py           # NEW
├── test_review_feedback_boundary.py    # NEW
├── test_review_docs_isomorphism.py     # NEW
└── test_review_p1_review_loop.py       # ONE pin updated (disclosed)
```

**Structure Decision**: this feature extends three existing template files, one shared workflow document, two existing skills (one body, one script, one reference), one documentation page, and the contract suite — no new top-level directory, no new command template, no new skill package, no runtime source change. The shape is "one command template grows a second delegation; one existing skill grows deterministic subcommands; two governance documents converge on one owner". The Feature Index and Feature detail updates are governance bookkeeping required by the pipeline, not part of the delivery surface.

### Mirror Obligations

**Owner declaration**: this section is the sole owner of the mirror source/projection/verify obligations for this feature. `feature-ref.md` § 6 points here and does not restate the table.

**Baseline drift measured before any edit** (all clean, so the criterion is relative): `templates/` 22 files `ok`; `skills/internal/` 136 files `ok`; `shared/` 55 files `ok`; `regen-command-copies.py --check` → all per-tool copies match. A Verify cell below is therefore stated as "no NEW drift", never as a bare pass — an absolute criterion would be unpassable the moment unrelated drift appears.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/review.md` | `.claude/commands/speckit.review.md`; `.github/prompts/speckit.review.prompt.md`; `.qoder/commands/speckit.review.md`; `.opencode/command/speckit.review.md` — all produced by the command-copy regenerator; the retired runtime command-template mirror is not a target | `python3 scripts/python/regen-command-copies.py --check` reports no drift beyond the measured clean baseline |
| `templates/review-template.md` | `.specify/templates/review-template.md` | `python3 scripts/python/sync-mirrors.py --check --only templates` → no NEW drift vs 22 files |
| `templates/feature-details-template.md` | `.specify/templates/feature-details-template.md` | same |
| `shared/workflow/feature-integration.md` | `.specify/shared/workflow/feature-integration.md` | `python3 scripts/python/sync-mirrors.py --check --only shared` → no NEW drift vs 55 files |
| `skills/internal/code-review/SKILL.md` | `.specify/skills/internal/code-review/SKILL.md` | `python3 scripts/python/sync-mirrors.py --check --only skills/internal` → no NEW drift vs 136 files |
| `skills/internal/code-review/scripts/git-delta-review.sh` | `.specify/skills/internal/code-review/scripts/git-delta-review.sh` | same |
| `skills/internal/code-review/references/delta-setup.md` | `.specify/skills/internal/code-review/references/delta-setup.md` | same |
| `skills/internal/review-sdd-process/SKILL.md` | `.specify/skills/internal/review-sdd-process/SKILL.md` | same |

`docs/` and `tests/` have no mirror. The probe registry is not edited, so no compiled closing face is regenerated. Write direction is source → projection through the generator, always; a hand-edited projection is a violation (C-69).

## Complexity Tracking

N/A — no Constitution Check violation requires justification.

## Phase 0: Research Review

Full decisions, rejected alternatives, and the measured outputs are in `research.md` (R1–R14). The load-bearing conclusions:

1. **Sequential, process-first, no merged severity** — the composition shape follows the requirements' Q1 adjudication; parallel and merged-report alternatives were rejected on both semantics and the existing 100%-call-rate property of the review face (R1).
2. **Base tiers are ordered by what the repository can actually resolve** — measured here: `refs/remotes/origin/HEAD` is absent, `origin` is the upstream project, and the local `main` merge-base is `926836e0`, months behind. A branch-name default would silently review the wrong slice (R2).
3. **Renderer absence becomes a labelled mode** — the old "stop when missing" clause is rewritten with its replacement evidence and reason in the same statement, across all three surfaces that carried it (R3).
4. **Receipt carrier and exit codes** — one delimited block inside the record; `0` / `1` / `2` reusing the repository's existing gate convention; gap ≠ skip, and skip ≠ coverage credit (R4).
5. **Gate ownership convergence, and the pin it breaks** — the two existing status rows disagree; the owner by declaration keeps the criteria and the copy becomes a reference; the one pin that quotes the removed wording is updated with a net assertion gain (R5).
6. **Stable record name plus rotation** — a timestamped-only name would break the pinned literal, a plain overwrite would lose history (R6).
7. **Non-interactive path is narrow** — `note` and `report` already run without `delta`; what is missing is record creation and a receipt, plus the explicit-input verdict that removes the newest-file defect inherited from the clarify run (R7).
8. **The report subsection is a subsection** — adding a numbered top-level section would renumber § 5/§ 6 and red an unrelated pin (R8).
9. **Two feedback units, one key** — both units are already probe-registered; the `(unit_id, run_id)` key lets them coexist (R9).
10. **Mirrors and baselines are measured, not assumed** — three mirror pairs and the per-tool copies re-measured clean before the plan was written (R10).

**Evidence path degradation (disclosed)**: the codebase-exploration pass and the same-author detection pass were performed as bounded direct reads and greps because this environment exposes no subagent dispatch. Every mechanically derivable premise was nevertheless produced by running a program, so the degraded path affects the prose-level compliance judgement only (R12). The conditions it could not supply — an independent reader hunting the self-authored defect class — are named in `research.md` § R12 rather than claimed.

## Design Overview

### 1. The command: two segments, one order, no shared vocabulary

`templates/commands/review.md` gains a composition section that: fixes the order (process first, unconditional; code second, triaged); forbids exempting the process segment by class, arguments, or absent code delta; states the failure-propagation rule (a process-segment abort records `not-evaluated` with its reason and does not suppress the code segment, and the run is not presented as a completed review); names both skills by runtime path; forbids inlining either methodology; states that the two severity vocabularies are never merged; and points at the state-machine owner instead of restating the gate. The frontmatter prerequisite block, the compiled closing face, and the handoff registration duty are untouched (C-16).

Which sources feed each section: the composition rules come from `contracts/command-orchestration.md` C-1…C-8, the output rules from C-9…C-15, the closing face from C-55.

### 2. Applicability triage: three values, no silent fourth

Before the code segment starts, the command resolves `run` / `not-applicable` / `not-evaluated`. `not-applicable` must carry a basis (no code deliverable, or no committed code delta); `not-evaluated` must carry a reason (unresolvable base, unusable repository). Both non-`run` values are disclosed in three places: the report's code subsection, the closing summary, and the feature detail's review-record row. For an expression-class feature this is what keeps the code segment additive rather than substitutive (C-6, C-7, C-52, C-62).

### 3. The code segment's deterministic core

All of it lands on `skills/internal/code-review/scripts/git-delta-review.sh`:

- `base` — three tiers, `--spec` / `--since`, prints `base=`, `head=`, `base_source=`; exits `2` when nothing resolves.
- `start` — creates the record header, rotates a previous record to its archive name, refuses to overwrite an existing archive.
- `note` — unchanged behavior, now always called with an explicit `--review-file` by the composed path.
- `receipt` — computes the changed-file set from the resolved range, compares it with the judged set, writes the delimited block, exits `0`/`1`/`2`, and derives the segment verdict from the three signals.
- `report --summary --file` — the single gate verdict source; `0` allow, `1` deny, `2` input error; an omitted `--file` stays as a labelled legacy mode.

`review` (the interactive per-file walk) keeps its rendered default, its tests-first ordering, its focus option, and its six-level validation. The rewrite of the renderer clause reaches the skill body's `Strict Requirements`, its Phase 0 step, and the `references/` wording in one pass (C-17…C-30, C-31…C-41).

### 4. The receipt: what makes "read the whole diff" checkable

The block's name set is closed and its counting identity is asserted (`judged + skipped + gap = changed`). Exit `1` means at least one changed file has no verdict or the sets differ; exit `0` with a non-zero skip count is still legal but forbids a `pass` verdict, because a skip is disclosure, not coverage. One write produces both the header marker and the block's `renderer` field, and a test asserts their equality — the disclosed projection that keeps one owner for one fact (C-31…C-42, `research.md` § R4).

### 5. The gate: one owner, two initiators, no mapping

`templates/feature-details-template.md` § Canonical Status State Machine keeps the criterion and gains the third condition (no unresolved `blocking` in the code segment), judged by reading the six-level vocabulary directly. `shared/workflow/feature-integration.md`'s `/speckit.review` row and `/speckit.checklist` row become references to that section. A waiver is only a user ruling, recorded in the report and the feature detail; the agent never downgrades a `blocking` item. The transition is judged once, after both artifacts exist (C-45…C-54).

### 6. Feedback: two units, framework friction only, zero transmission

The command unit and the skill unit each close themselves; the key is `(unit_id, run_id)`, so neither suppresses the other. The classification duty is written into the command template and the skill text: framework friction in, code defects out. The predecessor invariants — same-commit recommendation registration, introspection as the legal global entry, `scope: local`, zero automatic transmission, no new intake — stay in force (C-55…C-61).

### 7. Documentation and tests

The docs page, both skills' boundary wording, and the state-machine owner move in one change. Six contract groups land red-first; the one intentional pin change keeps its subject and gains a negative assertion. The neighbouring suites and the mirror checks are re-run against the measured baselines and judged by "no NEW failure, no NEW drift" (C-64…C-73).

### 8. What is deliberately not built

No second verdict source, no receipt sidecar, no id family for code findings, no mapped severity table, no new engine or dependency, no wrap-up step, no probe registry edit, no `/speckit.*` command, and no change to `shared/workflow/expression-gates.md` — the expression review face stays exactly as its contract test pins it (C-62, C-72, C-73, `research.md` § R14).

## Task Budget

The work fits one slice. Estimate: 30 steps against the 40-step ceiling.

| Phase | Steps | Contents |
|-------|-------|----------|
| Red-first tests and fixtures | 7 | Temporary-repository fixture; six contract files written against the unchanged tree; red evidence recorded |
| Script subcommands | 6 | `base`, `start`, `receipt`, `report --file`; the skip selector; green runs against the fixture |
| Template and skill bodies | 6 | Command composition section; skill body rewrite (non-interactive, header, renderer clause, boundary); report `§ 2.1`; state-machine owner row; integration-row convergence |
| Docs and feedback wording | 3 | Command reference page; both skills' boundary text; classification-duty wording in two surfaces |
| Regression, pin update, mirrors | 5 | Neighbouring suites, the one pin update, the three mirror pairs, per-tool copies, no-new-drift verification |
| Feature tracking and closure | 3 | Feature detail key changes, index status, final evidence record |
| **Total** | **30** | |

If the tasks stage needs more steps it may split a row, but the total must stay at or below the ceiling; no requirement may be dropped to fit.

## Risks and Assumptions

| # | Risk / assumption | Impact | Mitigation | Evidence / owner |
|---|-------------------|--------|------------|------------------|
| R-01 | The composed path inherits the "newest file in the directory" selection from the skill's `note`/`report` defaults. | A false allow: the process report is read as the code record and has no `blocking` heading. | The composed path always passes `--review-file` / `--file`; the legacy mode labels itself; a test asserts the explicit path is used. | C-27; `research.md` § R7 |
| R-02 | A branch-name default silently reviews the wrong slice. | The whole code judgement is about the wrong commits. | Three ordered tiers; measured proof that `origin/HEAD` is absent and `main`'s merge base is far behind; no branch literal anywhere. | C-18…C-20; `research.md` § R2 |
| R-03 | The one pin change is read as a weakening. | A silent loss of an existing guarantee. | Disclosed in `research.md` § R5 and `feature-ref.md` § 5; the replacement pin adds the owner path and a negative assertion; net assertions increase. | C-64, C-67 |
| R-04 | Skipped files are treated as judged, so a focused pass reports `pass`. | A review that read 2 of 50 files goes green. | Skip is not coverage credit; a non-zero skip count forbids `pass`; the count is a receipt field and is surfaced outside the block. | C-36…C-38, C-43 |
| R-05 | The receipt's two renderer literals drift apart. | A record claims a mode the block contradicts. | One write produces both; a test asserts equality. | C-40; DR1 |
| R-06 | Two feedback units collide or one suppresses the other. | A missing or duplicated entry per run. | The `(unit_id, run_id)` key already distinguishes them; both are probe-registered so no closing-face edit is needed. | C-58, C-59; `research.md` § R9 |
| R-07 | A code defect is posted as framework feedback. | The feedback store fills with feature defects and loses its meaning. | The classification duty is written in two surfaces; the contract test builds both samples. | C-56, C-57 |
| R-08 | Mirrors are missed while editing skills and templates. | Client-runtime drift, the highest-frequency rework source in this repo. | Measured baselines (22 / 136 / 55 files, per-tool copies) and the "no NEW drift" criterion per pair. | C-69, C-70 |
| R-09 | The report template's new subsection renumbers top-level sections. | An unrelated pin (`§ 5` / `§ 6`) goes red for the wrong reason. | The content lands as `### 2.1`, keeping every existing number. | C-9; `research.md` § R8 |
| R-10 | The text-mode path cannot be exercised on this host (`delta` is installed at `/home/agent/.cargo/bin/delta`). | The mode's behaviour stays unproven. | Drive the script with `DELTA_BIN` pointed at a non-existent binary — a substitution the script already supports. | C-22; `quickstart.md` scenario D |
| R-11 | Same-author detection could not be delegated in this environment. | The Constitution Check is weaker evidence than the gate intends. | Row-level markers, a named disclosure, and program-derivable checks actually executed. | `research.md` § R12 |
| R-12 | The requirements' 28-FR budget leaves no room for scope growth. | A mid-flight requirement forces a split or a dropped obligation. | No new requirement is introduced; the plan maps every requirement to a clause; the 30-step estimate sits under the ceiling. | `feature-ref.md` § 3; Task Budget |

## Dependencies and Sequencing

1. **Red before green**: the six contract groups and the temporary-repository fixture land first, and the red run is recorded with command, exit code, and failure count.
2. **Script before skill body**: the skill body describes behaviour the script already has, so the subcommands land before the prose that promises them.
3. **Skill body before command template**: the command may only point at what the skill states, so the skill's boundary and non-interactive path are written first.
4. **Owner row before integration convergence**: the state-machine owner gains the third condition before the integration row stops quoting criteria, otherwise a reader has a reference without a target.
5. **Docs after templates**: the page describes the surface the templates now carry; the isomorphism test compares the two.
6. **Pin update with the convergence**: the pin change rides in the same commit as the edit that removes the wording it quotes, so the suite is never intentionally red across a commit.
7. **Mirrors last**: source edits finish, then `sync-mirrors.py --write` and the command-copy regenerator, then the no-new-drift check.
8. **Feature tracking at the end**: status `Draft → Planned` and the detail's key changes after the artifacts are on disk.

## Out of Scope Preserved

A third review segment; parallel segments; a merged single report or a unified score; a mode parameter that can skip the process segment; `P0`/`P1`/`P2` relabelling of the code vocabulary; a receipt sidecar file; a `REC-…` id family for code findings; any edit to `shared/workflow/expression-gates.md` or to the flow-classification ledger; the probe registry and its compiled closing faces; a second intake store, aggregation, or upload path; a new command, skill, agent, dependency, service, daemon, or network call; hand-edited runtime projections; rewriting historical review reports or backfilling earlier features' code records; push, force merge, or a confirmation-gate bypass.

## Phase 1: Design Artifacts Summary

Backfilled after the Phase 1 artifacts landed on disk; every count below was taken from the files, not pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research decisions | [`research.md`] | 14 sections (R1–R14) plus one disclosed design refinement (DR1: the renderer literal projection) |
| Data model | [`data-model.md`] | 13 entities (E1–E13), 28 validation rules (V1–V28) |
| Contracts | [`contracts/`] | 6 files, 73 clauses: `command-orchestration.md` (C-1…C-16), `code-review-skill.md` (C-17…C-30), `coverage-receipt.md` (C-31…C-44), `status-gate-ownership.md` (C-45…C-54), `feedback-and-boundaries.md` (C-55…C-64), `tests-and-docs-sync.md` (C-65…C-73) |
| Quickstart | [`quickstart.md`] | 8 scenarios (A–H): in A the two git-instrument blocks are `EXECUTED` against the real repository and its scripted `base` example is `PINNED`; B–H are `PINNED` with premises listed per example; the regression block is `EXECUTED` with its measured counts |
| Feature reference | [`feature-ref.md`] | Binding, delivery surface (16 files), requirement coverage, one disclosed pin change, mirror-obligation pointer (owner: this file § Mirror Obligations) |

**Drift from the Phase 0 expectation**: none in scope. The clause count (73) is above the pre-filling estimate of roughly 60 because the receipt grammar and the pin disclosure each needed their own clauses; no requirement was added to accommodate them, and every clause cites an existing requirement. The contract-clause form is the canonical `md-bold-closed` form declared by `shared/definitions/contract-clause-definitions.md` § 3, so the clause extraction lane reads them without a legacy fallback.
