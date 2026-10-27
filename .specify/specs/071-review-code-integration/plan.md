# Implementation Plan: 071-review-code-integration

**Branch**: `071-review-code-integration` | **Date**: 2026-10-27 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition）
**Input**: Specification from `.specify/specs/071-review-code-integration/requirements.md`

## Summary

Feature 071 composes an existing, currently unreferenced capability into a command that needs it. `/speckit.review` today delegates only to `review-sdd-process` and explicitly refuses to judge code; the `code-review` skill is a complete code-review loop that no command calls. After this feature, one `/speckit.review` invocation runs two segments in a fixed order — the process segment first and unconditionally, the code segment second and applicability-triaged — writes two artifacts into the feature directory, and reports both conclusions while keeping the two severity vocabularies apart.

The technical approach is deliberately thin. The command template only orchestrates and points. The code segment's determinism (which commits are reviewed, which files were judged, whether the merge gate allows) moves into subcommands of the skill's existing script, so an unattended run can finish without a terminal, without a renderer, and without improvising a diff base from a branch name. The "was the whole diff read" question stops being a matter of trust and becomes a coverage receipt whose file set must equal the changed-file set and whose gap exits `1`. The renderer's absence stops being a stop condition and becomes a labelled text mode, with the anti-pretense rule kept verbatim in the rewritten clause.

One governance convergence rides along because the composition forces it: the `Implemented → Ready for Review` criteria exist twice and disagree, so the state-machine owner keeps them and the integration protocol's summary row becomes a reference. That single edit is why one existing pin changes; the change is authorized as a single non-precedential exception, disclosed, and it gains assertions rather than losing them.

**Remediation round 1 (2026-10-27, after the analyze gate).** `/speckit.analyze` returned `GATE: CRITICAL=0 HIGH=6`; the driver authorized the only permitted upstream repair round, and the requirements layer absorbed all 32 findings. This stage carried the plan-owned half — the worklist in `notes/remediation-round-1.md` — into the six contracts, the data model, research, quickstart, `feature-ref.md` and this file. Six decisions changed the design's shape rather than its wording, and each is recorded where it lives: the closing summary stops being a verifiable carrier (two carriers: the report's code subsection and the feature detail's `## Latest Review` entry); "what counts as a code path" belongs to one deterministic owner in the skill script with a `--code-paths` override; head is fixed at run start while base keeps three tiers plus a closed trunk-identification order; the gate is an existence test over the current record (no "cleared" state exists); the receipt's exit alphabet is closed at `0`/`1`/`2` with a closed skip-reason set; and the per-run unit census is three. Clause ids were preserved and one clause (C-74) appended, so the frozen ids every task row already cites still resolve.

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

**Re-check after Phase 1** (2026-10-27, after the artifacts landed): the same sixteen rows remain ✅ Pass. New evidence: `data-model.md` (13 entities, 35 validation rules), six contract files with 74 clauses, `quickstart.md` with eight scenarios each carrying an execution status, and the executed programme checks in `test-evidence/`. No new violation; no Complexity Tracking row.

**Re-check after remediation round 1** (2026-10-27, substantive revision at the driver's explicit authorization): all sixteen rows remain ✅ Pass, with three rows re-examined rather than re-asserted because the remediation moved what they rest on. XIV (One Source of Truth) is stronger than before — the counts now have one declared source with an equality assertion (C-74), the code-path predicate has one owner instead of a silent gap, and the two severity vocabularies are cited rather than restated. XVI (Fast Fail) is exercised rather than claimed: each amended clause names its finding id in the contract file's amendment log, and the one new clause is appended instead of inserted so no existing citation breaks. IX (Framework Scope Discipline) is unchanged in outcome — the round edited specification documents only; no engine, dependency, command, skill, template, test or task row was added. The two program checks re-ran after the edits: `pre-analyze-check.py --stage plan` → `decision=pass`, `errors=0`; `account-clause-coverage.py` → FR lane 28/28, with the one appended clause (C-74) reported beyond the frozen baseline because no `tasks.md` row claims it yet (pending-claim list in `notes/plan-remediation-round-1.md`).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/071-review-code-integration/
├── plan.md                 # This file
├── research.md             # Phase 0 decisions R1–R14 (standalone: >50 lines, external-source evaluation)
├── data-model.md           # Phase 1: entities E1–E13 + validation rules V1–V35
├── contracts/              # Phase 1: six contract files, clauses C-1…C-74 (C-74 appended in remediation round 1)
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

**Remediation round 1 leaves this table unchanged**: the round edited only artifacts under `.specify/specs/071-review-code-integration/` plus the feature registry, so no source file above was touched and the measured baselines (22 / 136 / 55 / per-tool copies) still describe the pre-edit tree. The table and its criterion are therefore carried forward, not re-measured — re-measuring a tree that has not changed would be a run whose only product is a restated number.

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

Before the code segment starts, the command resolves `run` / `not-applicable` / `not-evaluated` (as `[[STR-005]]` / `[[STR-001]]` / `[[STR-002]]`). `not-applicable` must carry a basis (no code deliverable, or no committed code delta); `not-evaluated` must carry a reason (unresolvable base, unusable repository). Whether a changed path is a *code* path is not decided here: the `code-review` skill's script owns one closed default path set and accepts `--code-paths`, because a second list in the command template would drift and a drift flips the triage value for one repository state. An empty delta (base and head at the same commit) is triaged before the receipt runs, so a 0/0/0 receipt can never report a clean review of nothing. Both non-`run` values are disclosed on the two carriers — the report's code subsection and the feature detail's `## Latest Review` entry — and only `run` writes a record file. For an expression-class feature this is what keeps the code segment additive rather than substitutive (C-6, C-7, C-11, C-52, C-62).

### 3. The code segment's deterministic core

All of it lands on `skills/internal/code-review/scripts/git-delta-review.sh`:

- `base` — base resolution in three tiers plus the closed trunk order (`--trunk`), and head (`--head`, else run-start `HEAD` fixed for the run); prints `base=`, `head=`, `base_source=`; exits `2` when nothing resolves.
- `start` — creates the record header, rotates a previous record to its `YYYYMMDDTHHMMSSZ` archive name, refuses to overwrite an existing archive (wait a second or exit `2`).
- `note` — unchanged behavior, now always called with an explicit `--review-file` by the composed path.
- `receipt` — computes the changed-file set from the resolved range, compares it with the judged set, honours the closed skip-reason set, writes the delimited block, exits `0`/`1`/`2` with one meaning each, and derives the segment verdict from the three signals.
- `report --summary --file` — the single gate verdict source; `0` allow, `1` deny (a `blocking` entry is present), `2` input error; an omitted `--file` stays as a labelled legacy mode.

`review` (the interactive per-file walk) keeps its tests-first ordering, its focus option, and its six-level validation; its rendered default follows FR-013's single mode rule — renderer **and** TTY — so an agent call takes text mode even on a host where `delta` is installed. The rewrite of the renderer clause reaches the skill body's `Strict Requirements`, its Phase 0 step, and the `references/` wording in one pass (C-17…C-30).

### 4. The receipt: what makes "read the whole diff" checkable

The block's name set is closed and its counting identity is asserted (`judged + skipped + gap = changed`). Exit `1` means at least one changed file has no verdict, the sets differ, or a skip carries a reason outside the closed set; exit `0` with a non-zero skip count is still legal but forbids a `pass` verdict, because a skip is disclosure, not coverage. The four counts have exactly one source — this block — and the two disclosures copy it, with a contract test asserting the three agree. One write produces both the header marker and the block's `renderer` field, and a test asserts their equality — the disclosed projection that keeps one owner for one fact (C-31…C-42, C-74, `research.md` § R4).

### 5. The gate: one owner, two initiators, no mapping

`templates/feature-details-template.md` § Canonical Status State Machine keeps the criterion and gains the third condition — the current code-segment record contains no `blocking` entry, judged by reading the six-level vocabulary directly. That condition is an existence test: there is no clearing action and no cleared state, so a later run that writes a record with zero `blocking` entries is the whole mechanism. `shared/workflow/feature-integration.md`'s `/speckit.review` row becomes a reference to that section and its `/speckit.checklist` row becomes a conditional reference (the checklist initiates the transition only when it runs after implement). A waiver is only a user ruling — a driver's confirmation is not — recorded on both carriers; without one the unattended disposition is halt-and-report with `blocking-unresolved` as the named refusal literal. The transition is judged once, after both artifacts exist (C-45…C-54).

### 6. Feedback: three units, framework friction only, zero transmission

The command unit and both delegated skill units (`skill:review-sdd-process`, `skill:code-review`) each close themselves; the key is `(unit_id, run_id)`, so none suppresses another. The classification duty is written into the command template and the skill text: framework friction in, code defects out. The predecessor invariants — same-commit recommendation registration, introspection as the legal global entry, `scope: local`, zero automatic transmission, no new intake — stay in force (C-55…C-61).

### 7. Documentation and tests

The docs page, both skills' boundary wording, and the state-machine owner move in one change. Six contract groups land red-first — each with a recorded failing run (command, exit code, failing count) — and the one intentional pin change keeps its subject, adds the owner path, and adds a negative assertion. The neighbouring suites and the mirror checks are re-run against the measured baselines and judged by "no NEW failure, no NEW drift" (C-64…C-73).

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

**Remediation round 1 does not move this budget.** The round's added obligations — `--code-paths`, `--trunk` / `--head`, the TTY condition, the closed skip-reason check, the count-equality assertion — are absorbed into rows that already exist (the script subcommands row, the three test-and-fixture rows, the template/skill body rows). No new phase, no new test file and no new delivery file was introduced, so the estimate stays at 30 steps and the six-group test plan of FR-028 stays six.

## Risks and Assumptions

| # | Risk / assumption | Impact | Mitigation | Evidence / owner |
|---|-------------------|--------|------------|------------------|
| R-01 | The composed path inherits the "newest file in the directory" selection from the skill's `note`/`report` defaults. | A false allow: the process report is read as the code record and has no `blocking` heading. | The composed path always passes `--review-file` / `--file`; the legacy mode labels itself; a test asserts the explicit path is used. | C-27; `research.md` § R7 |
| R-02 | A branch-name default silently reviews the wrong slice. | The whole code judgement is about the wrong commits. | Three ordered tiers; measured proof that `origin/HEAD` is absent and `main`'s merge base is far behind; no branch literal anywhere. | C-18…C-20; `research.md` § R2 |
| R-03 | The one pin change is read as a weakening — or as a permission. | A silent loss of an existing guarantee; or a second pin edit justified by the first. | Authorized as a **single non-precedential exception** by FR-027 (C-64, C-67): the rationale must be declared in the feature detail's review-record entry, the replacement adds the owner path and a negative assertion, net assertions increase, and the authorization may not be cited as precedent. Disclosed in `research.md` § R5 and `feature-ref.md` § 5. | C-64, C-67; FR-027 |
| R-04 | Skipped files are treated as judged, so a focused pass reports `pass`. | A review that read 2 of 50 files goes green. | Skip is not coverage credit; a non-zero skip count forbids `pass`; the count is a receipt field surfaced on both carriers. | C-36…C-38, C-43 |
| R-05 | The receipt's two renderer literals drift apart. | A record claims a mode the block contradicts. | One write produces both; a test asserts equality. | C-40; DR1 |
| R-06 | Two feedback units collide or one suppresses the other. | A missing or duplicated entry per run. | Three units, keyed `(unit_id, run_id)`; all three are probe-registered so no closing-face edit is needed. | C-58, C-59; `research.md` § R9 |
| R-07 | A code defect is posted as framework feedback. | The feedback store fills with feature defects and loses its meaning. | The classification duty is written in two surfaces; the contract test builds both samples. | C-56, C-57 |
| R-08 | Mirrors are missed while editing skills and templates. | Client-runtime drift, the highest-frequency rework source in this repo. | Measured baselines (22 / 136 / 55 files, per-tool copies) and the "no NEW drift" criterion per pair. | C-69, C-70 |
| R-09 | The report template's new subsection renumbers top-level sections. | An unrelated pin (`§ 5` / `§ 6`) goes red for the wrong reason. | The content lands as `### 2.1`, keeping every existing number. | C-9; `research.md` § R8 |
| R-10 | The text-mode path cannot be exercised on this host (`delta` is installed at `/home/agent/.cargo/bin/delta`). | The mode's behaviour stays unproven. | Two deterministic substitutions: `DELTA_BIN` pointed at a non-existent binary, and a non-TTY run with the renderer present (the shape an agent actually gets). | C-22; `quickstart.md` scenario D |
| R-11 | Same-author detection could not be delegated in this environment. | The Constitution Check is weaker evidence than the gate intends. | Row-level markers, a named disclosure, and program-derivable checks actually executed — including a re-run after the remediation. | `research.md` § R12 |
| R-12 | The requirements' 28-FR budget leaves no room for scope growth. | A mid-flight requirement forces a split or a dropped obligation. | No new requirement is introduced; the plan maps every requirement to a clause; the 30-step estimate sits under the ceiling and the remediation added no step. | `feature-ref.md` § 3; Task Budget |
| R-13 | Two code-path lists appear (command template and script) and drift. | One repository state triaged `run` by one reader and `not-applicable` by another; SC-005 becomes untestable. | The predicate has exactly one owner — the skill script with `--code-paths`; C-7 and the command template cite it and carry no list. | C-7, C-30; FR-003 |
| R-14 | An empty delta reaches the receipt and the 0/0/0 conjunction returns `pass`. | A review of nothing reported as clean. | Triage runs before the receipt; C-38's conjunction is scoped to `run` with a non-empty changed set; V30 keeps the two apart. | C-7, C-38; V20, V30 |
| R-15 | Two runs inside one second collide on the archive path. | A record overwritten, or the run unable to write at all. | The rotation waits for the next second or exits `2` with a reason; an existing archive is never overwritten. | C-12; V12, V24 |
| R-16 | The four receipt counts drift across the block and its two disclosures. | The number a reader trusts is not the number the receipt produced. | One declared source plus an equality assertion in the receipt test (the same guard C-40 uses for the renderer literal). | C-74; V33 |

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
| Data model | [`data-model.md`] | 13 entities (E1–E13), 35 validation rules (V1–V35); the seven rules added in remediation round 1 are V29–V35, appended so no existing rule number moves |
| Contracts | [`contracts/`] | 6 files, 74 clauses: `command-orchestration.md` (C-1…C-16), `code-review-skill.md` (C-17…C-30), `coverage-receipt.md` (C-31…C-44 plus the appended C-74), `status-gate-ownership.md` (C-45…C-54), `feedback-and-boundaries.md` (C-55…C-64), `tests-and-docs-sync.md` (C-65…C-73) |
| Quickstart | [`quickstart.md`] | 8 scenarios (A–H): in A the two git-instrument blocks are `EXECUTED` against the real repository and its scripted `base` example is `PINNED`; B–H are `PINNED` with premises listed per example, D now carrying the no-TTY case alongside the missing-renderer one; the regression block is `EXECUTED` with its measured counts |
| Feature reference | [`feature-ref.md`] | Binding, delivery surface (16 files), requirement coverage, one disclosed pin change (authorized by FR-027), mirror-obligation pointer (owner: this file § Mirror Obligations) |

**Drift from the Phase 0 expectation**: none in scope. The clause count (73 at Phase 1, 74 after remediation round 1) is above the pre-filling estimate of roughly 60 because the receipt grammar and the pin disclosure each needed their own clauses, and the round appended exactly one more (C-74: the counts' single source with its equality assertion); no requirement was added to accommodate them, and every clause cites an existing requirement. The contract-clause form is the canonical `md-bold-closed` form declared by `shared/definitions/contract-clause-definitions.md` § 3, so the clause extraction lane reads them without a legacy fallback.

## Plan Change Log

### Remediation round 1 — 2026-10-27 (substantive revision, driver-authorized)

**Trigger**: `.specify/specs/071-review-code-integration/test-evidence/analyze-report.md` → `GATE: CRITICAL=0 HIGH=6` (32 findings: HIGH 6 / MEDIUM 22 / LOW 4). The requirements layer absorbed all of them in commit `14a1c6ec`; the plan-owned half was handed over as `notes/remediation-round-1.md`. This round is the only permitted upstream repair round, and the driver authorized substantive edits to plan-owned artifacts (a plain `PLAN-EDIT` declaration per file follows, and the same list is returned in the stage's report).

| Artifact | What changed | Findings |
|----------|--------------|----------|
| `contracts/command-orchestration.md` | C-5 (minimal report on abort), C-6 ([[STR-005]]), C-7 (code-path owner + empty delta), C-9 (disclosure + counts copied), C-11 (record existence follows triage), C-12 (timestamp/collision/first-run), C-13 (`## Latest Review` carrier), C-14 (two carriers) | A-01, A-02, A-04, A-07, A-08, A-09, A-11, A-21, A-22, A-29, A-33 |
| `contracts/code-review-skill.md` | C-17 (four steps), C-18 (head + trunk order), C-21 (head in header), C-22 (renderer ∧ TTY, [[STR-008]]), C-23 (SC-003 owns the phrase list), C-28 (cites FR-013), C-30 (`--code-paths` on the script entity) | A-02, A-03, A-10, A-15, A-16, A-26, A-32 |
| `contracts/coverage-receipt.md` | C-34/C-35 (closed `0/1/2` alphabet), C-36 (skip reasons owned by FR-014), C-37/C-38 (presence; scoped conjunction), C-39 ([[STR-006]]/[[STR-007]]), C-43 (two carriers), C-44 (dual-carrier disclosure), **C-74 appended** (counts' single source + equality assertion) | A-01, A-04, A-05, A-11, A-12, A-13, A-14, A-29 |
| `contracts/status-gate-ownership.md` | C-46 (existence), C-48 (conditional checklist initiator), C-51 (halt-and-report, [[STR-010]]), C-52/C-53 (two carriers, named failing condition) | A-01, A-05, A-18, A-19 |
| `contracts/feedback-and-boundaries.md` | C-58/C-59 (three units), C-63 (coverage disambiguation both ways), C-64 (single non-precedential authorization + declaration duty) | A-06, A-17, A-20 |
| `contracts/tests-and-docs-sync.md` | C-66 (red-first per group), C-67 (pin tied to C-64), C-70 (criterion vs. table owner) | A-06, A-23, A-25 |
| `data-model.md` | E1/E3/E4/E5/E6/E7/E8/E9/E10/E11/E12/E13 aligned; V6/V9/V12/V20/V22/V24/V25 amended; V29–V35 appended | A-03, A-04, A-05, A-08, A-11, A-12, A-13, A-14, A-16, A-20, A-21, A-22, A-29 |
| `research.md` | R2 (head rule + trunk order, measured), R3 (renderer ∧ TTY), R4 (exit meanings, skip grounds), R5 (authorized pin), R6 (`YYYYMMDDTHHMMSSZ` vs. the script's legacy form), R7 (four steps), R8 (content list), R9 (three units), R11 (per-group red-first) | A-03, A-10, A-13, A-16, A-20, A-22, A-26 |
| `quickstart.md` | A (head/trunk premises), B (two carriers, counts copied), C (predicate basis, no record for non-`run`), D (no-TTY case), E (exit alphabet + unrecognised reason), F (legal skip reason literal), G (existence gate, [[STR-010]]), H (three units) | A-01, A-02, A-03, A-05, A-12, A-13, A-16, A-19, A-20, A-21 |
| `feature-ref.md` | delivery-surface rows, FR/SC clause map (incl. C-74), § 5 pin authorization + this round disclosed, artifact counts | A-06, A-29 |
| `plan.md` | Summary, Design Overview §2–§7, Task Budget, Risks (R-03 rewritten, R-13…R-16 added), Constitution re-check, Mirror note, Phase 1 counts, this change log | all |

**Clause-ID discipline**: C-1…C-73 keep their ids and their meaning; every wording change is listed per file in that contract's `## Amendment log — remediation round 1` with the finding id that forced it; the single new obligation was **appended** as C-74 rather than inserted, so no existing citation in `tasks.md` breaks and no clause id is reused. Each amended and appended clause still ends with its FR/SC citation group, which is what keeps `clause_extract.py` and `account-clause-coverage.py` able to read the set.

**Pending claim**: C-74 is unclaimed by any `tasks.md` row (this stage does not edit `tasks.md`), so it reports as one item beyond the frozen clause baseline. The tasks stage claims it; the exact command output and the pending list are in `notes/plan-remediation-round-1.md`.
