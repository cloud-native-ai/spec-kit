# Implementation Plan: Self-Explanatory Framework Integration（不言自明的框架集成）

**Branch**: `082-self-explanatory-integration` | **Date**: 2026-11-05 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `082-self-explanatory-integration` → Feature 082 Self-Explanatory Framework Integration（不言自明的框架集成）
**Input**: Specification from `.specify/specs/082-self-explanatory-integration/requirements.md`

## Summary

The three owner documents written at the close of the interview
(`shared/definitions/self-explanatory-definitions.md`, `shared/guidelines/self-explanatory.md`,
`shared/workflow/best-practice-optimization.md`) already exist but reach neither the governance
surfaces a downstream project receives nor that project's runtime mirror. This plan delivers the
integration and nothing else: one numbered constitution principle in the framework template plus the
generator's mandate list, one ambient instructions section, one minimal budget raise to make room for
it, three source→mirror pairs, one glossary entry, and the contract tests that go red when any of them
disappears.

The technical shape is "author text and regenerate": no new engine, no new generator, no new checker.
Every deliverable lands on a surface that already has a regeneration path
(`scripts/python/sync-mirrors.py` for mirrors, `scripts/bash/generate-instructions.sh` for the live
instructions file, `manage-constitution`'s template-guided path for the live constitution) and an
existing contract suite to extend (double-landing, instructions propagation, mirror parity, glossary
mechanism).

## Technical Context

**Language/Version**: Python `>=3.8` (declared in `pyproject.toml`; verified interpreter here is CPython 3.11.11) — the implementation artifacts are Markdown authority documents plus edits to existing Python contract tests; no new Python module is introduced  
**Primary Dependencies**: no new runtime dependency. The work is executed by existing repository engines: `scripts/python/sync-mirrors.py`, `scripts/bash/generate-instructions.sh`, `scripts/python/regen-command-copies.py`, `scripts/python/scan-confirmation-gates.py`, `scripts/python/glossary-utils.py`. Test runner: `pytest` (verified 8.4.2)  
**Storage**: Markdown files in the repository (framework sources and their runtime mirrors); the glossary store at `.specify/memory/glossary.md`  
**Testing**: `pytest` with the `contract` marker; four existing suites are extended, one existing suite is reused without modification (mirror parity derives its table from `MIRROR_PAIRS`)  
**Target Platform**: the repository itself plus any project initialized with `specify init` — the distribution path is what makes the mirror obligation load-bearing  
**Project Type**: framework / code generator (single Python package `src/specify_cli/` + packaged `templates/`, `skills/`, `scripts/`, `shared/` sources)  
**Performance Goals**: N/A — no runtime path is changed; the only measured quantity is a byte budget (see Constraints)  
**Constraints**: the live instructions file sits 29 B below the current `INSTRUCTIONS_BUDGET_BYTES` ceiling, so the new section cannot land without raising that constant by the smallest sufficient amount; the gate-scanner total is pinned at an exact integer by two contract tests, so every new passage on a scanned surface must carry zero blocking-pattern hits  
<!-- 092 handoff: F1 — "29 B below the current `INSTRUCTIONS_BUDGET_BYTES` ceiling" is a plan-time reading and MUST NOT be updated. That constant's only definition point is `scripts/bash/generate-instructions.sh`; the FR/task decomposition ceilings are owned by `.specify/skills/sdd-loop-driver/scripts/decomposition-check.py` (`FR_CEILING = 120`, `TASK_CEILING = 160`). Re-read the owner; never quote this line's number. See 092 F1, 2026-11-09. -->
**Scale/Scope**: 3 owner documents mirrored (already authored, untracked), 1 constitution template + 1 live constitution + 1 skill mandate list, 1 instructions template + 1 live instructions file + 1 budget constant, 1 glossary entry, 1 docs pointer page, 4 contract suites touched


## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`; the roster below is
the live constitution's own roster, 18 principles, in file order):

<!-- 092 handoff: F3 — 「18 principles」是 plan-time 快照，保留不改。本行原作自己的名册断言，并非引用；名册的唯一值 owner 是 `.specify/memory/constitution.md`（2026-11-09 现值 22 条，版本 1.19.0）。参见 092 F3。 -->

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every deliverable traces to an FR: constitution surfaces → FR-001–FR-003, instructions → FR-004–FR-005, mirrors → FR-006–FR-007, guards → FR-008–FR-012. |
| II | Feature-Centric Development | ✅ Pass | Feature 082 row + detail exist; this plan advances `Draft → Planned` and records the change in `.specify/memory/features/082.md` § Latest Review; no new Feature introduced (Feature-list review below). |
| III | Intent-Driven Development | ✅ Pass | Intent is recorded and adjudicated upstream: `requirements.md` § Assumptions A1–A11 and § Clarifications § Session 2026-11-04. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Every new guard is specified as a failing-test-first row in `contracts/` (C-1…C-34) and `tasks.md` will carry them in Red-Green order; mutation legs (contract § Mutation legs) prove each guard can go red. |
| V | AI Agent Integration Standards | ✅ Pass | The only agent-facing surface touched is `.specify/instructions.md` (and its symlinks), which stays the single source of truth; the symlink model is not changed (contract C-10). |
| VI | Continuous Quality & Observability | ✅ Pass | Observability is the budget report that `generate-instructions.sh` already prints; the plan adds a recorded measured-after value rather than a new meter (SC-009). |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This plan is the plan stage; `tasks.md` is explicitly out of scope here (plan integrity gate: no `tasks.md` claim). |
| VIII | Code as the Single Source of Truth | ✅ Pass | Where plan text states a repository fact (counts, paths, exit codes) the statement was produced by a command run during this phase and recorded in `research.md` § Phase 0. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Zero new engine, zero new generator, zero new link checker: mirrors reuse `sync-mirrors.py`, instructions reuse `generate-instructions.sh`, the docs link guard reuses pytest + mirror parity (FR-012). |
| X | Documentation Naming & Location Conventions | ✅ Pass | New page is `docs/concepts/self-explanatory.md` (lowercase kebab-case, `docs/<area>/<topic>.md`); owner docs follow the existing `shared/{definitions,guidelines,workflow}/<name>.md` layout. |
| XI | Dogfooding (Self-Application) | ✅ Pass | The change is made in the framework sources and reaches this repository's runtime through the same regeneration paths a client project uses (Two Hats: `templates/` + `skills/` + `shared/` edited; `.specify/` regenerated). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Each mechanism this plan leans on is an existing named engine or skill; no throwaway script is introduced (research.md R-4 records the reuse decisions). |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | The principle's own content is an improvement-orientation statement for structure; the integration makes it reachable by every project through the harness surfaces it already loads. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The concept owner stays `shared/definitions/self-explanatory-definitions.md`; every output surface carries a pointer + at most a summary (contract C-20 asserts the owner body is absent from the surfaces that point at it). |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The projected principle and instructions section are written as declarative statements with every non-derivable claim reachable by path; `research.md` R-6 records the wording review. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Known negative facts are recorded rather than parked: the pre-existing gate-total drift is a `falsified` execution premise with a `Decision` (EP-003), and two pre-existing suite outcomes are recorded in `research.md` § Measured baseline instead of being repaired in place. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created; `docs/concepts/`, `shared/definitions/`, `shared/guidelines/`, `shared/workflow/`, `test-evidence/` all pre-exist and are documented. |
| XVIII | Grounded Naming | ✅ Pass | Canonical names come from a higher-priority source: `STR-001` (constitution section title) and `STR-003` (glossary canonical) are the interview's ratified names (A6), carried verbatim to every surface (contract C-12). |

**Gates Status**: ✅ All gates pass — no Fail and no Partial row, so no Complexity Tracking entry is owed.

**Re-check after Phase 1** (2026-11-05, after the Phase 1 artifacts landed): the same table re-read
against `contracts/constitution-double-landing.contract.md`, `contracts/instructions-propagation.contract.md`,
`contracts/mirror-distribution.contract.md`, `contracts/glossary-integration.contract.md`,
`data-model.md` and `quickstart.md` — all 18 rows unchanged. Two rows were re-examined in detail:
IV (Test-First) because the guard suites are the bulk of the deliverable, now backed by contract
§ Mutation legs rows M-1…M-4, each naming the exact assertion that must go red; XIV (One Source of
Truth) because four surfaces will quote `STR-001`, now backed by C-20 (owner body absent) plus C-21
(the summary sentence bounded to ≤ 2 sentences). No row changed verdict.

## Decision Tensions

Two decisions in this plan satisfy the owner's load-bearing threshold (irreversibility and a
constitution MUST respectively); the remaining choices were settled by measurement and are recorded
in `research.md` instead.

### T-001 — Raise the instructions budget constant instead of compressing an existing section

- **decision**: The new ambient section lands by raising `INSTRUCTIONS_BUDGET_BYTES` by the smallest sufficient amount, never by shrinking an existing section.
- **antithesis**: Compress an existing framework section back to its template shape (the R1 route `/speckit.instructions` Action 5 already offers) until the 29 B of headroom suffices; when the live file has drifted above its template for reasons unrelated to this feature and a compression pass is due anyway, it is better — it keeps the ceiling honest and forces the periodic convergence that the two other routes exist to perform.
- **binding_constraints**:
  - pole_a: The governance section added by this feature is value the feature delivers; hiding it behind an unrelated compression review couples two changes with different owners and different risk, and a failed compression silently blocks the feature.
  - pole_b: A budget is only a budget if exceeding it is a decision someone made, and a constant raised casually on every new section stops being a constraint at all.
- **discriminating_evidence**: Run `bash scripts/bash/generate-instructions.sh` twice — once with the section added and the constant at its current value, once with the section added and the constant raised — and read the `BUDGET: <size> <budget> <verdict>` line: `over` in the first run, `within` in the second. The result is binary and reproducible. The measurement was executed during this phase; `research.md` R-1 records both readings.
- **expected_sacrifice**: SC-009 Source ↓ the ceiling moves as a deliberate, recorded raise rather than staying fixed; the cost is that the number in the generator stops being a stable reference point for downstream projects that quoted it.
- **revision_trigger**: If a second feature in one release cycle needs another raise, or if the measured headroom after a raise drops below 1 KiB → reopen and switch the default route to compression-first (R1) with the budget constant left untouched.

### T-002 — Two separate section titles carry `STR-001`, instead of one shared string

- **decision**: The constitution principle's title and the instructions ambient section's title are the same literal `STR-001`, written on both surfaces, rather than one surface pointing at the other's heading.
- **antithesis**: Let only the constitution carry `STR-001` and give the instructions section a different heading (for example `Self-Explanatory Structures`) that points at the principle by numeral; when the two surfaces are maintained by different commands on different cadences, it is better — the instructions reconcile is a mechanical per-section diff, and a title shared with a document it never diffs against is a second copy that can drift silently.
- **binding_constraints**:
  - pole_a: Constitution IV and II make the constitution the governance anchor; an ambient section with a different name forces every reader to translate between two vocabularies for one concept, which is the failure Constitution XV names.
  - pole_b: Two surfaces holding one literal is exactly the pattern Constitution XIV restricts, and the only legitimate duplicates it permits are a machine-regenerated copy, a pinned test literal, and a dated record.
- **discriminating_evidence**: Run `grep -cF 'Self-Explanatory Structure (不言自明)' templates/constitution-template.md templates/instructions-template.md` and read the two counts: 1 and 1 means both surfaces carry the literal, 0 means one surface lost it. The result is binary. The measurement was executed during this phase; `research.md` R-3 records the reading and C-12 pins it as a contract assertion.
- **expected_sacrifice**: SC-001 Source ↓ the literal lives on two surfaces, so a future rename must edit both in one change; Constitution XIV's drift risk is accepted and paid for by the C-12 set-membership assertion on both surfaces rather than by removing the duplication.
- **revision_trigger**: If a future rename finds `STR-001` on three or more independent surfaces, or if a drift between the two titles is ever observed in a completed run → reopen and convert the instructions heading into a pointer at the constitution's numeral.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/082-self-explanatory-integration/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — measured baseline, reuse decisions, 7 resolved unknowns
├── data-model.md        # Phase 1 output — E-1…E-8 entities, V-1…V-19 validation rules
├── quickstart.md        # Phase 1 output — S-0…S-7, every command executed with output pasted
├── contracts/           # Phase 1 output — 4 files, C-1…C-34
├── feature-ref.md       # Phase 1 output — delivery surface, mirror rows, rulings
├── requirements.md      # upstream (/speckit.requirements + /speckit.clarify)
├── checklists/
│   └── requirements.md  # upstream checklist
├── test-evidence/       # stage evidence (E-3 stage-status row, measured baselines)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
templates/                          # framework sources (constitution + instructions templates)
skills/internal/manage-constitution/ # generator skill: the MUST-include mandate list
shared/definitions/                 # concept owner (source) — mirrored
shared/guidelines/                  # practice owner (source) — mirrored
shared/workflow/                    # optimization-workflow owner (source) — mirrored
scripts/bash/                       # generate-instructions.sh: budget constant + additive reconcile
scripts/python/                     # sync-mirrors.py MIRROR_PAIRS (read, not edited)
docs/concepts/                      # the pointer page
tests/contract/                     # four guard suites
.specify/shared/                    # runtime mirrors (generated by sync-mirrors.py)
.specify/memory/                    # live constitution, live instructions, glossary
.specify/templates/                 # template mirror (generated)
.specify/specs/082-self-explanatory-integration/   # this spec's design + evidence artifacts
```

**Structure Decision**: this is the "code generator / framework" shape already used by the repository
(`templates/`, `skills/`, `scripts/`, `src/`): the feature edits framework sources under
`templates/`, `skills/`, `shared/` and `scripts/`, regenerates the runtime tree under `.specify/`,
and extends the existing `tests/contract/` suites. No new top-level directory is created. The one
directory whose contents are new is `.specify/specs/082-self-explanatory-integration/test-evidence/`,
which the plan stage populates with a single stage-status evidence row.

### Mirror Obligations *(mandatory — this spec touches mirrored surfaces)*

Baseline measured on this branch (`stage_base=506adf88`), twice and both readings kept:
`python3 scripts/python/sync-mirrors.py --check` reported exit 2 with exactly three `MISS` lines (this
feature's three owner documents) at the start of the stage, and exit 0 — `shared/ == .specify/shared/`
`ok`, 65 files — when re-measured later in the same stage, the three pairs `cmp`-identical. Every other
pair was `ok` throughout (templates 22, skills/external 409, skills/internal 138, agents 3, scripts 119)
with `OK: all per-tool command copies match the source templates`. Both readings and the timing note
are recorded in `research.md` § Measured baseline (B-1, B-7) and in
`test-evidence/plan-stage-checks.md`. Each `Verify` cell below is therefore stated as **keep the
measured baseline — no new `MISS` or `DIFF` line on the pairs this spec touches**.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/self-explanatory-definitions.md` (extended in the interview, untracked at plan time) | `.specify/shared/definitions/self-explanatory-definitions.md` via `sync-mirrors.py` pair `shared → .specify/shared` | `python3 scripts/python/sync-mirrors.py --check` exits 0 and `cmp` reports the pair identical; judged against the measured baseline, i.e. this row's `MISS` line disappears and no other line changes |
| `shared/guidelines/self-explanatory.md` (same) | `.specify/shared/guidelines/self-explanatory.md` | same command; this row's `MISS` line disappears |
| `shared/workflow/best-practice-optimization.md` (same) | `.specify/shared/workflow/best-practice-optimization.md` | same command; this row's `MISS` line disappears |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` via pair `templates → .specify/templates` | `sync-mirrors.py --check` exits 0 with the templates line `ok`; `cmp` on the pair identical |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` via the same pair | `sync-mirrors.py --check` exits 0; `cmp` identical |
| `scripts/bash/generate-instructions.sh` | `.specify/scripts/bash/generate-instructions.sh` via strict pair `scripts → .specify/scripts` | `sync-mirrors.py --check` exits 0 (strict pair also fails on mirror-only orphans); `cmp` identical |
| `shared/workflow/best-practice-optimization.md` (distribution companion) | no per-tool command copy — `shared/` has one mirror pair and no regen fan-out | none beyond the `shared` pair row above |
| `templates/commands/` (NOT edited by this feature) | zero per-tool copies regenerated: `regen-command-copies.py` delegates only from `templates/commands/` | `python3 scripts/python/regen-command-copies.py --check` prints `OK: all per-tool command copies match the source templates.` — an unchanged-surface assertion, recorded as evidence, not as a change |
| `docs/concepts/self-explanatory.md` | none — `docs/` is not distributed and has no mirror pair | not applicable; the page is guarded by a link assertion instead (contract C-27) |
| `tests/contract/*.py` | none — tests are not mirrored | not applicable |

Two mirror facts that the implementation MUST NOT re-discover the hard way:

1. **The mirror criterion is `keep`, not `reach`.** The stage measured both states (exit 2 before,
   exit 0 after) and the applying baseline is exit 0. A task row that writes "run `--write` to make
   `--check` pass" is describing work already done; the real obligation is that no later edit to the
   three owner documents or to `shared/` leaves the mirror stale. If a future edit does reintroduce a
   `MISS`/`DIFF` line, the order is `--write` (or `--only shared`) then `--check`.
2. **`templates/commands/` is a retired mirror.** Editing a command template fans out only to the
   per-tool copies produced by `regen-command-copies.py`; there is no `templates/commands/`
   copy to update. This feature does not edit command templates at all, which is why the only regen
   assertion here is the unchanged-surface `--check`.

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The three deterministic checkers this feature's guards depend on run on the repository's declared interpreter floor (`>=3.8`): `pytest`, `sync-mirrors.py`, `scan-confirmation-gates.py` all execute successfully here. | `python3 --version` → `Python 3.11.11`; `git --version` → `git version 2.43.5`; `python3 -m pytest --version` → `pytest 8.4.2`; `sync-mirrors.py --check` and `scan-confirmation-gates.py --json` both execute and exit with a parseable verdict (research.md § Measured baseline). Static import list for the touched modules is empty (no new module). | verified | — |
| EP-002 | `specify init` distributes what the mirror step produced: `src/specify_cli/__init__.py` copies the resource `shared/` tree into `<project>/.specify/shared/`, and `.specify/shared` is part of the shared core. A file present only in the mirror and absent from the source is never distributed. | `src/specify_cli/__init__.py:2504-2516` (copy `shared/` → `.specify/shared`), `:1148` (`.specify/shared` in the shared-core list), `:1563` (segment roster `memory, scripts, templates, shared`); `sync-mirrors.py --check` prints the three `MISS` lines that `--write` will clear (research.md R-5). | verified | — |
| EP-003 | The gate-scanner total is *not* at the value two contract tests pin: the live scan reports 27 while `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` freezes 23, and `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` therefore fails today — independently of this feature. | `python3 scripts/python/scan-confirmation-gates.py --json` → `total: 27` (`governance_kept` 7, `destructive` 20, `violations: []`); frozen baseline file → `confirmationGates.total: 23`; the pin is an equality assertion at `tests/contract/test_proactive_trigger_section.py:361`. | falsified | fallback |
| EP-004 | The four guard suites named in the spec are the only regression surfaces this feature needs, and each can be made to go red by deleting or drifting its subject. | `tests/contract/test_constitution_double_landing.py` (watchlist + per-side mutation probe), `tests/contract/test_instructions_section_propagation.py` C-1/C-2, `tests/contract/test_mirror_parity_suite.py` (param table derived from `MIRROR_PAIRS`), `tests/contract/test_glossary_mechanism.py`. Each mutation leg is specified in `contracts/` § Mutation legs and executed in Phase 1 (quickstart S-5). | verified | — |

Premise notes:

- **EP-003 is a known negative conclusion and is decided, not parked.** `Decision: fallback` — this
  feature (a) MUST NOT repair the pin (it belongs to Feature 050's frozen baseline and repairing it
  here would fold an unrelated measurement into this change), (b) MUST extend the double-landing
  suite's own zero-hit assertion (`test_c13_new_principle_blocks_have_zero_blocking_hits`) to the new
  surfaces instead of relying on the drifted total as its guard, and (c) MUST report the pre-existing
  failed node in every stage's targeted-run evidence by name, never as "clean". See `research.md` R-2.
- **EP-002 is the premise behind the `in-scope` runtime-stack row RS-004**: the capability is not
  external, it is the repository's own distribution path, and its three `in-scope` duties are paid by
  FR-007 (requirements), a `tasks.md` row quoting FR-007 (tasks stage), and a joint-acceptance row in
  `verification.md` (closure stage).

## Inherited Blockers

Dependency set: none — this feature integrates three documents authored in the same interview and
depends on no earlier feature's deferred records. The two pre-existing facts the plan carries are
not inherited records but this plan's own measurement: the gate-total drift (EP-003, decided as
`fallback`) and the mirror baseline (three `MISS` lines that `--write` clears), both recorded above
and in `research.md`.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | — | not-applicable | — | — | Dependency set: none — no dependency feature was read, so the extraction set is empty and no row can be undisposed. |

## Complexity Tracking

N/A — the Constitution Check has no Fail and no Partial row, so no violation needs justification.

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](./research.md) | 7 resolved unknowns (R-1…R-7) + 7 measured baseline facts (B-1…B-7) + a 7-row re-measure list |
| Data model | [`data-model.md`](./data-model.md) | 8 entities (E-1…E-8), 19 validation rules (V-1…V-19), 2 state transitions |
| Contracts | [`contracts/`](./contracts/) | 4 files, 34 clause ids (C-1…C-34): `constitution-double-landing.contract.md` 9 + 1 pointer (C-1…C-9, C-20 note), `instructions-propagation.contract.md` 10 (C-10…C-19), `mirror-distribution.contract.md` 9 (C-20…C-28, C-20/C-21 defined here and referenced by the other two files), `glossary-integration.contract.md` 6 (C-29…C-34); plus 6 mutation legs (M-1…M-6) across the three landing/distribution files |
| Quickstart | [`quickstart.md`](./quickstart.md) | 8 scenarios (S-0…S-7); every command executed during Phase 1 with its output pasted, teardown included |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | 14-row delivery surface, 3 reused-without-modification suites, 7 disclosed rulings, 3 follow-ups |
| Stage evidence | [`test-evidence/plan-stage-checks.md`](./test-evidence/plan-stage-checks.md) | baseline measurements + the E-3 `stage-status` row (`status=not-run-docs-only`) |

Version and command facts quoted anywhere in this artifact set (sizes, counts, exit codes, `--help`
surfaces) were measured during Phase 1 and pasted with their output; where a figure could change
between this run and implementation time, the figure is stated together with the command that
re-measures it, so `/speckit.tasks` can re-take it instead of inheriting it.

## Execution Notes for the Next Stages

- **Ordering constraint**: mirror `--write` precedes any `--check`-based acceptance claim; the live
  instructions regeneration precedes the instructions-propagation assertions; the live constitution
  amendment precedes the double-landing live-side assertions.
- **Budget raise is a same-change obligation**: the section and the constant move together. A task
  row that adds the section without the constant is not implementable — the generator would report
  `over` and the acceptance claim for SC-009 would be false on the same commit.
- **Live constitution numbering**: the live roster is 18 principles and the template roster is 17 at
  plan time; the live constitution's new principle takes the next free numeral *on that surface*

  <!-- 092 handoff: F3 — 「18 / 17 at plan time」是 plan-time 快照，保留不改。名册的唯一值 owner 是 `.specify/memory/constitution.md`（2026-11-09 现值 22 条，版本 1.19.0）；模板侧自按模板文件重新计数。参见 092 F3。 -->
  (XIX), while the template lands the same title at its own next free numeral (XVIII). No test and no
  plan row may pin a numeral.
- **`/speckit.improve` wiring stays out** (`OI-082-01`): the optimization workflow document is
  mirrored and distributed; nothing in this plan connects `templates/commands/improve.md` to it, and
  no acceptance row may read "document mirrored" as "command wired".
