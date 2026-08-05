# Implementation Plan: Goal 作为项目级一等概念(goal 定义归档 + 团队引用 + 单一撰写入口 + 多团队协调)

**Branch**: `037-goal-registry` | **Date**: 2026-08-05 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `037-goal-registry` → Feature 041 Goal Registry
**Input**: Specification from `.specify/specs/037-goal-registry/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command, which **replaces** every placeholder token in place — it MUST NOT append a second copy of this template below the filled content. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Promote `goal` from a per-team field into a project-level first-class concept, and give the goal level the two things it has never had: a **definition** and a **view of who is working on it**.

Four deliverables:

1. **Authored definition archive** at `.specify/goal/<goal-slug>/goal.md` — exactly three parts (narrative, zero-or-more verifiable criteria, lifecycle `active`/`achieved`/`abandoned`), identity carried by the directory name. Never written by a derived flow.
2. **Consolidated single goal index** — requirement 036's derived delivery directory moves from `.specify/project/goal/<goal-slug>/` into `.specify/goal/<goal-slug>/summary/`, so the definition and its summary are two faces of one object with a **single-subtree write-set allow-list** protecting the definition.
3. **`/speckit.goal`** as the sole authoring entry (create / modify / view / migrate), delivered through the existing mirror fan-out.
4. **Multi-team coordination** — a derived roster of teams sharing the goal, a new **team-level `territory`** declaration, mechanical overlap detection riding 036's existing summary refresh, and a coordination round that only proposes a re-division for human ratification.

**Technical approach**: this is overwhelmingly a *reference-surface* change plus one genuinely new piece of executable logic. Research (E-1…E-3) established that the migration is a one-line path change in the generator (`build-summary-input.py:577`) fanned out across **24 live source files**, with no data to move because `.specify/project/goal/` was never materialized. The one real new capability is overlap detection: territory exists today only as prose for the LLM with **zero executable validation** (E-4), so this requirement writes the first territory validator — and it does so inside `resolve_goal()` (E-6), the existing function that already collects every team sharing a `goal_slug`, which is what makes "zero new trigger machinery" literally true rather than aspirational.

## Technical Context

**Language/Version**: Python `>=3.8` (repo floor, `pyproject.toml`). The extended engine `build-summary-input.py` targets the same floor.
**Primary Dependencies**: **none new**. The engine already uses `pyyaml`; `typer` / `rich` / `httpx` are untouched. Adding a command requires **no `src/specify_cli/` change** — `templates/commands/` is packaged wholesale and `regen-command-copies.py` fans out from it (E-7); `tests/integration/test_ai_tools_command_coverage.py` globs the directory dynamically, so it picks the new command up without edits.
**Storage**: files only. Authored `.specify/goal/<goal-slug>/goal.md` (Markdown + YAML frontmatter, matching the repo's existing artifact idiom); derived `.specify/goal/<goal-slug>/summary/**` (the relocated 036 output: `data/project-input.yaml` plus whatever `summarize-project` emits). No database is introduced by this requirement.
**Testing**: `pytest` with the repo's `contract` / `integration` markers. **Baseline frozen before any change: 40 failed / 1308 passed / 1 skipped**, names in `baseline-failed.txt`. Two baseline notes: (a) the single new failure vs 036's baseline is branch-state-dependent and self-resolves at `/speckit.tasks` (research D-12); (b) `tests/fixtures/teams/goal-share-{a,b}/` already share one `goal_slug` and are the intended overlap test bed (D-11).
**Target Platform**: Linux / macOS developer shells. Generated command copies target the 5 tool directories that exist in this repo (`.claude`, `.github/prompts`, `.qoder`, `.opencode`, `.qwen`); `.hermes` / `.iflow` / `.codex` are skipped because `regen-command-copies.py` only regenerates directories that already exist (E-7).
**Project Type**: single — a template/prompt framework repository (`templates/` + `skills/` + `scripts/` + `shared/` + `src/specify_cli/`), with `.specify/` as the installed runtime mirror.
**Performance Goals**: no latency target is meaningful at this scale, but overlap detection MUST NOT make a refresh perceptibly slower. Detection is O(T²) in the number of teams sharing one goal, pairwise over normalized path sets; T is 4 today and is expected to stay single-digit. Refresh is already serialized by a directory lock with a 900s stale threshold, so detection inherits that mutual exclusion for free.
**Constraints**: zero new runtime dependencies; `.specify/` mirrors byte-identical (`sync-mirrors.py --check` exit 0); the authored `goal.md` receives **zero** writes from any derived flow; 036's existing assertions are preserved with paths updated only (FR-024); historical spec/feedback records that quote the old path MUST NOT be rewritten (FR-022); no new option may collide with the two existing `--goal` meanings (FR-021).
**Scale/Scope**: 42 functional requirements, 18 success criteria, 5 user stories, 8 FR groups. Concretely: 24 live files to migrate, 1 new command (+ 1 mirror + 5 generated copies + 1 reference doc + 2 doc-table rows), 1 new engine capability inside an existing script, 4 test fixtures extended, 9 existing test files updated for the path change.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.9.0 — 13 principles, in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design decision below traces to a numbered FR in `requirements.md`; no artifact is introduced without an FR citation |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 041 (registered during `/speckit.clarify`); `features/027.md` carries the reverse cross-reference; this run advances 041 Draft → Planned only |
| III | Intent-Driven Development | ✅ Pass | Four clarify sessions of multi-step refinement precede any code; `research.md` records why each option was rejected, not just what was chosen |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Executable code exists (goal engine, overlap detection, migration), so the template-only clause of Principle VII does **not** apply. Contracts land in Phase 1 before implementation; `tests/fixtures/teams/goal-share-{a,b}` are the pre-existing overlap bed (research D-11) |
| V | AI Agent Integration Standards | ✅ Pass | No new provider. The new command fans out via the authoritative `_ASSISTANT_COMMAND_DIRS` config to the 5 materialized tool dirs; `.qwen`'s mandated `.toml` form is respected (research E-7) |
| VI | Continuous Quality & Observability | ✅ Pass | Baseline measured and frozen (40F/1308P/1S) before any change; the generator's existing structured exit codes (0/2/3/4) are reused rather than replaced; migration guarded by the existing byte-invariance test |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first was evaluated and a new Feature justified on scope (goal has consumers outside the team domain); no status regression (041 Draft → Planned); this command does not land `Implemented` |
| VIII | Code as the Single Source of Truth | ✅ Pass | Actively exercised: this plan **corrected the spec** from measured code state — the stale "37 files" became a verified 24-live/18-historical split, and SC-011's whole-repo zero was found unachievable by construction and rescoped (research D-1) |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | Adds a new command surface **and** the first executable territory validator. Mitigated: all new logic is deterministic file/text processing, and the coordination round itself stays prompt-interpreted with human ratification (FR-039) — no scheduler, no runtime platform. Justified in Complexity Tracking rows 1–2 |
| X | Documentation Naming & Location Conventions | ✅ Pass | All new names lowercase (`goal.md`, `summary/`); `docs/reference/commands/goal.md` follows the existing 1:1-with-templates convention (no nested `README.md`, no index needed); no ALL-CAPS reserved name introduced |
| XI | Dogfooding (Self-Application) | ✅ Pass | 037 is itself going through the full SDD workflow; the coordination design was derived from measured repo evidence (territory prior art, fixtures) rather than hypothesized |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the Verified Tool `sync-mirrors.py` for all fan-out and **extends** `build-summary-input.py` rather than writing a second engine; that Tool record is itself in the migration surface and gets updated (research E-1) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Names the dimensions strengthened: **Controlled Execution** (team-level territory stops two teams competing for one write set) and **Task Understanding** (one authoritative objective instead of N team copies). Adds no scoring or maturity machinery |

**Gates Status**: ⚠ **12 Pass / 1 Partial** — Principle IX is Partial with justification; both causes are recorded in Complexity Tracking below. No Fail rows, so the Draft → Planned transition is unblocked per the canonical state machine.

**Re-check after Phase 1**: 2026-08-05 — re-run against the landed artifacts (`data-model.md`, 4 contracts, `quickstart.md`, `feature-ref.md`). Result unchanged: 12 Pass / 1 Partial. The Phase 1 design **kept Principle IX's cost where it was scoped** rather than widening it: roster derivation and overlap detection fold into the existing `build-summary-input.py` (reusing `resolve_goal()`, which already enumerates every team sharing a goal), goal authoring stays **prompt-driven** in `templates/commands/goal.md` rather than becoming an execution engine, and the only new script is a focused validator following the repo's established `*-utils.py` convention (`docs-utils.py`, `feedback-utils.py`, `glossary-utils.py`, …) for the deterministic checks — identity grammar, three-part structure, lifecycle enum, archive enumeration. The coordination round remained a proposal document with no write authority.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/037-goal-registry/
├── plan.md                  # This file (/speckit.plan command output)
├── research.md              # Phase 0 output — E-1…E-10 findings, D-1…D-12 decisions
├── data-model.md            # Phase 1 output (/speckit.plan command)
├── quickstart.md            # Phase 1 output (/speckit.plan command)
├── contracts/               # Phase 1 output (/speckit.plan command)
├── feature-ref.md           # Phase 1 output (/speckit.plan command)
├── baseline-failed.txt      # Frozen test baseline (40 failures) for regression attribution
├── checklists/requirements.md  # Spec quality checklist (4 clarify sessions logged)
├── tasks.md                 # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md          # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
.specify/goal/                       # NEW runtime dir — the goal archive (authored goal.md + derived summary/)
templates/commands/                  # + goal.md (new command source of truth); team.md edited for the path change
skills/create-team/                  # SKILL.md (team-level territory key, gate order, status line), references/, scripts/
skills/create-team/scripts/          # build-summary-input.py — delivery path + roster derivation + overlap detection
skills/create-team/references/       # summary-mapping.md (write-set + roster), goal.md (points at concept authority)
skills/improve-team/references/      # goal-editing.md — re-point concept statements at the authority
docs/reference/commands/             # + goal.md (new command reference); team.md layout tables updated
docs/tutorials/                      # quickstart.md + installation.md — one command-table row each
tests/contract/                      # 4 existing files repathed; new goal-command + territory contract tests
tests/integration/                   # 5 existing files repathed; new roster/overlap integration tests
tests/fixtures/teams/                # goal-share-{a,b} gain `territory` (the overlap bed)
.specify/**                          # mirrors of every canonical edit above (regenerated, never hand-edited)
```

**Structure Decision**: this spec extends the existing **code-generator / framework** shape — it adds one new command to `templates/commands/`, extends one existing engine script and one skill in `skills/create-team/`, and introduces exactly one new top-level runtime directory, `.specify/goal/`. No new package, no new engine, no new top-level source tree. The new directory is a *runtime* artifact location (like `.specify/teams/`), not source. **Prerequisite note**: `shared/definitions/goal-definitions.md` and its `.specify/` mirror are the read-only concept authority for this work (FR-019, spec Assumptions) and are currently **untracked** — they must be committed before or with this requirement, but this requirement does not modify them.

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/goal.md` **(new)** | `.specify/templates/commands/goal.md`; `.claude/commands/speckit.goal.md`; `.github/prompts/speckit.goal.prompt.md`; `.qoder/commands/speckit.goal.md`; `.opencode/command/speckit.goal.md`; `.qwen/commands/speckit.goal.toml` | `sync-mirrors.py --check` exit 0; each generated copy carries the `AUTO-GENERATED` header naming the source |
| `templates/commands/team.md` | `.specify/templates/commands/team.md`; the same 5 per-tool copies for `speckit.team` | `diff -q` mirror; generated copies contain the new path and no `project/goal` |
| `skills/create-team/SKILL.md` | `.specify/skills/create-team/SKILL.md` | `diff -q` |
| `skills/create-team/references/summary-mapping.md` | `.specify/skills/create-team/references/summary-mapping.md` | `diff -q` |
| `skills/create-team/references/goal.md` | `.specify/skills/create-team/references/goal.md` | `diff -q` |
| `skills/create-team/references/optimization-goals.md` | `.specify/skills/create-team/references/optimization-goals.md` | `diff -q` |
| `skills/improve-team/references/goal-editing.md` | `.specify/skills/improve-team/references/goal-editing.md` | `diff -q` |
| `skills/create-team/scripts/build-summary-input.py` | `.specify/skills/create-team/scripts/build-summary-input.py` | `diff -q` (verified byte-identical today) |
| `scripts/python/goal-utils.py` **(new)** | `.specify/scripts/python/goal-utils.py` | `diff -q`; `sync-mirrors.py --check` reports `scripts/ == .specify/scripts/` |
| `.specify/memory/tools/build-summary-input.py.md` | *(no mirror — single canonical location)* | Tool record's source contract matches the edited script |

All fan-out is performed by one command — `python3 scripts/python/sync-mirrors.py --write` — and verified with `--check` (exit 2 = drift). Per-tool copies are **never** hand-edited.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **New command surface `/speckit.goal`** (1 template + 1 mirror + 5 generated copies + 1 reference doc + 2 doc-table rows) — Principle IX | goal is a project-level concept with no existing owner; FR-025 requires exactly one authoring entry for create/modify/view/migrate, mirroring how Feature 027 makes `/speckit.team` the team domain's sole entry | **Extending `/speckit.team`** binds a project-level concept back into the team command, directly contradicting this requirement's core claim that goal is not a team attribute. **A bare skill** (create-goal/improve-goal) avoids the command surface but has no discoverable entry point, so the "one authoring entry" criterion could not be verified. **Contract-only, hand-authored files** leaves US1 creation and US4 migration with no automation, which is how the concept would fail to be adopted |
| **First executable territory validator** (path normalization + pairwise intersection + contested-area classification inside `build-summary-input.py`) — Principle IX | FR-036 requires a *determinate* overlap verdict, and FR-042 requires "no overlap" to be distinguishable from "undecidable". Territory is prose-only today with zero executable validation (research E-4), so there is nothing to extend — the logic has to be written | **Delegating the judgement to the LLM per run** is non-reproducible (Principle XII's stated failure mode: the same logical check re-improvised each run) and would silently miss notation differences — this repo has already been bitten by a `{a,b,c}` brace path evading an existence check. **A new standalone script** was rejected in favour of extending `resolve_goal()`, which already enumerates every team sharing the goal, keeping the new surface to a function rather than a file |
