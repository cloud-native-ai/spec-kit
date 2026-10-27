# Implementation Plan: 072-client-self-improvement

**Branch**: `072-client-self-improvement` | **Date**: 2026-10-27 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement）
**Input**: Specification from `.specify/specs/072-client-self-improvement/requirements.md`

## Summary

Feature 072 spreads the framework's feedback and self-improvement machinery onto the client project itself. Today every mechanism targets Spec Kit's own friction: the code-review segment's findings stop inside `code-review.md` where no loop reads them, the feedback store's routing was built for the framework's units, and the self-improvement loop's observation source contract accepts only command and skill unit forms. After this feature, one qualifying `/speckit.review` run in a client project automatically lands exactly one pointer-shaped client entry in the existing feedback store; the feedback command digests client entries in place and assigns each exactly one of three existing carriers; the improvement command runs the unchanged SI-0…SI-9 loop over a `custom:` subject with an honest "run-determination history not evaluated" disclosure; and four read-built metrics answer whether the loop works.

The technical approach adds exactly two bounded faces to existing engines — a deterministic `capture` subcommand on the code-review script (the non-interactive path's fifth step) and a read-only `client-metrics` action on the feedback engine — plus one opt-in `--format json` flag on the existing summary command. Everything else is prompt-level: the review template grows one optional `--client-unit` parameter, the digest reference gains the carrier-assignment rule, the self-improvement workflow gains one observation-source rule, and the Dogfooding Loop B recipe's one wrong line is rewritten. No new command, engine, store, ledger, score, dependency, scheduler, or transmission path is introduced.

The single amendment to Feature 071's closed surfaces is the step enumeration (four steps → five), with its reason and cost recorded at the amendment site. Client-side behavior is verified in a simulated client project — a fixture without root-level framework source directories — because framework-repository self-testing takes the other hat branch and would leave the whole client path unexecuted.

**Run input classification** (the planning skill's step 2): the dispatch brief arrived as run parameters — background facts, scope boundaries, and the adjudicated Q1–Q10 rulings — not as a new requirement set. No mid-run addendum arrived; `requirements.md` was not restructured.

## Technical Context

**Language/Version**: Bash for the code-review script extension (host bash 5.x); Python 3.8+ for the feedback engine action and contract tests (host 3.11.11, pytest 8.4.2); Markdown for command templates, skills, shared owner docs, and docs pages.
**Primary Dependencies**: none new. Reuses `feedback-utils.py`, `probe-utils.py`, `run-determination.py`, `evidence-utils.py`, `git-delta-review.sh`, `sync-mirrors.py`, `regen-command-copies.py`, and pytest.
**Storage**: files only — client entries land in the existing `.specify/memory/feedback/` store (one file per entry, `kind: external` / `slice: host-custom` / `custom:` unit); external probe files in the existing `.specify/memory/feedback/probes/`; no new directory, aggregate, or index file is created anywhere (metrics are read-built).
**Testing**: pytest contract suites under `tests/contract/`; five new files for the five FR-029 behavior groups, each red-first with a recorded failing run (command line, exit code, failure count); the fixture is a temporary git repository with a minimal installed `.specify/` runtime and no root-level framework source directories, plus a framework-hat twin fixture. Tests Mode = **ON**.
**Target Platform**: the framework repository and every consuming client project; hosts with or without a TTY; un-upgraded `.specify/` runtimes (registry-missing branch is a specified disclosure, not a crash).
**Project Type**: SDD framework (prompt templates, skills, shared workflow docs, deterministic scripts, contract tests) — no application runtime is added.
**Performance Goals**: not a performance feature. Capture adds one probe-registry read, one summary invocation, and one engine record call to a review run; metrics recompute on report with the same order of cost as the existing `status` action.
**Constraints**: no new `/speckit.*` command, no new engine/store/ledger/score/id-family, no dependency, no network call, no resident process; zero automatic transmission; no hand-edited runtime projection; no history rewrite or backfill; the four feedback red lines and Feature 071's closed surfaces stay in force (sole amendment: the step enumeration).
**Scale/Scope**: 29 FRs, 7 SCs, six contract files with 62 clauses, ten data-model entities, 33 validation rules, two engine faces, one command parameter, one workflow rule, one guideline line rewrite, five new test files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Same-author condition (disclosed, per `shared/workflow/objective-analysis-gate.md`)**: these design artifacts were authored in this session and this environment exposes no subagent dispatch capability, so scoring could not be delegated. Every row therefore carries `(direct read, subagent unavailable)`; the program-derivable checks were actually executed instead — `pre-analyze-check.py --stage plan`, `clause_extract.py` (all six contract files parse as `md-bold-closed`, C-1…C-62 in order), `account-clause-coverage.py` (FR lane), `sync-mirrors.py --check` / `regen-command-copies.py --check` (baseline drift recorded), plus the neighbouring guard suites (evidence in `test-evidence/`).

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | All 29 FRs and 7 SCs are cited from contract citation groups (`feature-ref.md` § 3/§ 4); every technical choice traces to a requirements adjudication or a recorded plan-level ruling in `research.md` R1–R12 (direct read, subagent unavailable) |
| II | Feature-Centric Development | ✅ Pass | Feature 072 bound and registered in the requirements stage; this stage advances `Draft → Planned` and records key changes in `features/072.md`; no second row (direct read, subagent unavailable) |
| III | Intent-Driven Development | ✅ Pass | The spec's what/why (six user stories, Q1–Q10 rulings) precede this how; `research.md` records every rejected alternative (skill-text engine call, wrap-up-id run key, icon-text parsing, receipt counts, LLM-derived metrics, new script) (direct read, subagent unavailable) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Five behavior groups, each red-first with recorded failing runs (SC-006); fixture proves the client branch that framework self-testing cannot reach (C-58/C-59); guard suites only grow (C-61) (direct read, subagent unavailable) |
| V | AI Agent Integration Standards | ✅ Pass | No provider, config key, or agent roster change; per-tool command copies stay generator-produced (`regen-command-copies.py --check` clean) (direct read, subagent unavailable) |
| VI | Continuous Quality & Observability | ✅ Pass | Capture keeps the existing closed exit alphabets and adds a deterministic, always-exactly-one disclosure line; the four metrics are observable without being a gate (C-48); no speculative feature (direct read, subagent unavailable) |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify → plan respected; status ceiling `Planned`; the single upstream amendment (step enumeration) is recorded with reason and cost at its owner site (direct read, subagent unavailable) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 re-measured the engines and script before designing: idempotency key at `feedback-utils.py:783–793`, exclusion at `1871–1892`, custom-unit fail-closed at `run-determination.py:1228–1246`, record header at `git-delta-review.sh` `cmd_start`; `research.md` quotes the outputs (direct read, subagent unavailable) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Everything lands on existing artifacts; the two engine faces are subcommands/actions of existing engines; "continuous" is explicitly not a scheduler (C-40); the sequencing rule is prompt-level (direct read, subagent unavailable) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic names under this spec and `tests/contract/`; no reserved ALL-CAPS name; `SKILL.md` mandated names unchanged (direct read, subagent unavailable) |
| XI | Dogfooding (Self-Application) | ✅ Pass | The feature rides its own SDD chain; framework sources are the only edit surface with generators producing projections; Loop B's wrong recipe line is fixed at the mechanism (guideline source), not per client (direct read, subagent unavailable) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the feedback/probe/run-determination/evidence engines and the review script instead of new machinery; no Tool record covers armed-state resolution or pointer capture, so writing them on the existing script is the expected outcome (direct read, subagent unavailable) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Learning Capture (findings reach a loop instead of a dead file) and Change Validation (metrics honest about not-evaluated); no new scoring system; closure evidence follows the configured≠used discipline (direct read, subagent unavailable) |
| XIV | One Source Of Truth (Authority & Reference Discipline) | ✅ Pass | Hat criterion, probe registry, carrier owners, backlog semantics, and the receipt are cited by path, never restated; the five disclosure tokens and ten shared strings are referenced as `[[STR-NNN]]`, not copied; armed state has one resolver in one subcommand (direct read, subagent unavailable) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The disclosure line is a closed literal set plus plain-reason detail; quickstart scenarios carry execution status and per-example premise lists; engine call forms stay out of the reader's conclusion path (direct read, subagent unavailable) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The registry-missing leak path is surfaced as a fail-closed disclosure rule (C-4) rather than patched over; the framework-hat disclosure got its own ruling (R6) instead of overloading a closed token; the subagent-unavailable condition is disclosed (direct read, subagent unavailable) |

**Gates Status**: ✅ All gates pass. No ❌ and no ⚠ row, so Complexity Tracking is N/A.

**Re-check after Phase 1** (2026-10-27, after the artifacts landed): the same sixteen rows remain ✅ Pass. New evidence: `data-model.md` (10 entities, 33 validation rules, 2 state transitions), six contract files with 62 clauses, `quickstart.md` with 8 scenarios (2 executed live, 6 with per-example disclaimers and named pinning tests), and the executed program checks in `test-evidence/`. No new violation; no Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/072-client-self-improvement/
├── plan.md                 # This file
├── requirements.md         # Input (29 FR / 7 SC / 10 Shared Strings; Q1–Q10 + 5 clarify adjudications)
├── research.md             # Phase 0: rulings R1–R12 with measured evidence
├── data-model.md           # Phase 1: entities E1–E10, validation rules V1–V33, 2 state transitions
├── contracts/              # Phase 1: six files, clauses C-1…C-62
│   ├── client-identity-and-armed-state.md   # C-1…C-9
│   ├── capture-step.md                      # C-10…C-24
│   ├── digest-and-carriers.md               # C-25…C-32
│   ├── client-improvement-loop.md           # C-33…C-39
│   ├── cadence-and-metrics.md               # C-40…C-50
│   └── red-lines-and-surfaces.md            # C-51…C-62
├── quickstart.md           # Phase 1: scenarios S1–S8 (S1–S2 executed; S3–S8 per-example disclaimers)
├── feature-ref.md          # Phase 1: binding, delivery surface, FR/SC coverage, disclosed rulings
├── checklists/
│   └── requirements.md     # Requirements-stage quality checklist (unchanged)
├── test-evidence/          # deterministic check records (plan.jsonl + gate outputs)
├── tasks.md                # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md         # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
templates/commands/
├── review.md               # + --client-unit parameter, step-5 pointer, conclusion disclosure
├── feedback.md             # + client digest / carrier / metrics report pointers
└── improve.md              # + custom-subject observation-source pointer

skills/internal/code-review/
├── SKILL.md                # 非交互路径 四步→五步 (sole closed-surface amendment); capture rules
└── scripts/git-delta-review.sh  # + capture subcommand; report --summary --format json (opt-in)

skills/internal/manage-feedback/
├── SKILL.md                # client-side carrier/digest report duties
└── references/path-a-digest.md  # A4 carrier assignment (closed 3), report facts

skills/internal/self-improvement/
└── SKILL.md                # why-segment custom-subject observation source

shared/workflow/self-improvement-workflow.md  # SI-1 observation-source rule + disclosure literal
shared/guidelines/dogfooding.md               # Loop B recipe: skill:<scenario-name> → custom: (one line + reason)

scripts/python/
└── feedback-utils.py       # + read-only client-metrics action (no write point)

docs/reference/commands/
├── review.md / feedback.md / improve.md      # sync surfaces

tests/contract/
├── test_client_capture.py           # NEW
├── test_client_armed_state.py       # NEW
├── test_client_package_exclusion.py # NEW
├── test_client_improve_loop.py      # NEW
└── test_client_metrics.py           # NEW
```

**Structure Decision**: extends the existing SDD-framework layout on all seven existing surfaces; no new top-level directory. The only new files are one spec-doc set, five contract tests, and two bounded engine faces on existing engines.

### Mirror Obligations

The live mirror pairs are defined in `scripts/python/sync-mirrors.py` MIRROR_PAIRS; command templates fan out only to `regen-command-copies.py` per-tool copies (`.specify/templates/commands/` is retired).

**Baseline drift measured before this plan's edits** (2026-10-27): `sync-mirrors.py --check` reports exactly one pre-existing drift, `.specify/skills/improve-skills/references/loop-playbook.md` (legacy divergence recorded in the constitution's Sync Impact Report, unrelated to this feature); `regen-command-copies.py --check` is clean. Pass criterion for every row: **no NEW drift on the pairs this spec touches** — regenerated copies contain the edit.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/{review,feedback,improve}.md` | per-tool copies via `regen-command-copies.py` (`.claude/commands/`, `.github/prompts/`, `.qoder/commands/`, `.opencode/command/`, …); NO `.specify/templates/commands/` mirror (retired) | `python3 scripts/python/regen-command-copies.py --check` after regen — no new drift vs the measured baseline |
| `skills/internal/code-review/`, `skills/internal/manage-feedback/`, `skills/internal/self-improvement/` | `.specify/skills/internal/` mirror via `sync-mirrors.py` | `python3 scripts/python/sync-mirrors.py --check` — no new drift beyond the one recorded pre-existing diff |
| `shared/workflow/self-improvement-workflow.md`, `shared/guidelines/dogfooding.md` | `.specify/shared/...` mirror via `sync-mirrors.py` | same check, same criterion |
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` via `sync-mirrors.py` | same check, same criterion |

## Complexity Tracking

N/A — Constitution Check has no Fail or Partial row.

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 12 rulings (R1–R12), each with measured evidence and rejected alternatives |
| Data model | [`data-model.md`](data-model.md) | 10 entities (E1–E10), 33 validation rules (V1–V33), 2 state-transition diagrams |
| Contracts | [`contracts/`](contracts/) | 6 files, 62 clauses (C-1…C-62), all `md-bold-closed`; 29/29 FR and 7/7 SC cited |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 scenarios: S1–S2 executed live 2026-10-27 (outputs pasted), S3–S8 per-example disclaimers with premise lists and named pinning tests |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, 11-row delivery surface, FR/SC coverage tables, 7 disclosed rulings, non-regression statement |

Executed derivation commands (real outputs in `test-evidence/`): `clause_extract.py contracts/*.md` → 62 clauses across 6 files, all `md-bold-closed`; `probe-utils.py --action probes --format json` → `available: True, external objects: 0, classes: 10`; `feedback-utils.py --action list --kind external --format json` → `count: 0`; `pre-analyze-check.py --stage plan` → `decision=pass, errors=0`; `account-clause-coverage.py` → FR lane 29/29.
