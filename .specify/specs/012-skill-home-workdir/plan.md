# Implementation Plan: SKILL_HOME and SKILL_WORKDIR Path Conventions

**Branch**: `012-skill-home-workdir` | **Date**: 2026-05-30 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/012-skill-home-workdir/requirements.md`

## Summary

Introduce two named, agent-engine-agnostic path variables — `${SKILL_HOME}` (the Skill's real on-disk directory after symlink resolution) and `${SKILL_WORKDIR}` (the runtime working directory of a Skill-invoked process) — into the `/speckit.skills` orchestration template (`templates/commands/skills.md`) and propagate the convention into `skills/create-skills/SKILL.md` and `skills/improve-skills/SKILL.md` (plus their `.specify/skills/` mirrors).

The change is documentation-only: no new CLI code, no new scripts, no new runtime dependencies. The deliverable is a normative writing/computation convention covering (a) how authors reference Skill-owned resources, (b) how authors reference user-facing runtime paths, (c) how shell scripts self-compute both variables with a portable fallback, (d) how `SKILL_HOME` supersedes the legacy `SKILL_ROOT`, and (e) a legacy-→-new migration mapping so pre-existing Skills can be converted opportunistically without a flag-day change.

Technical approach: pick a portable shell idiom (`cd … && pwd -P` instead of `readlink -f`) that works on stock macOS BSD shells, anchor it in `templates/commands/skills.md`, then rewrite the two authoring Skills to use the new convention. Add a contract test that asserts the structural requirements (variable definitions, paired example, migration table, FR-016 script idiom, zero remaining `SKILL_ROOT` references) so the convention is verifiable in CI rather than only by reading.

## Technical Context

**Language/Version**: Markdown/YAML for templates and Skills (primary edit target); Bash 3.2+ for the normative script idiom (lowest common denominator: stock macOS `/bin/bash`); Python 3.8+ for the existing pytest harness  
**Primary Dependencies**: No new runtime or build dependencies. Tests reuse existing `pytest` markers (`contract`); template/Skill content is plain Markdown, no new template engine  
**Storage**: File-based repository artifacts only — `templates/commands/skills.md`, `skills/create-skills/SKILL.md`, `skills/improve-skills/SKILL.md`, mirrored `.specify/skills/<name>/SKILL.md` files, and optionally `.specify/instructions.md` / `CLAUDE.md` consistency check (per FR-015)  
**Testing**: `pytest -m contract` for a new structural assertion suite on the updated template and Skills; manual regression check (per SC-004) by invoking each pre-existing Skill once post-change  
**Target Platform**: All officially supported AI agents (Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder); host OSes: macOS (BSD shell), Linux (GNU shell), WSL. The portable shell idiom must run on stock macOS `/bin/bash` (3.2) without GNU coreutils  
**Project Type**: Single (Python CLI + Markdown templates + reusable Skill directories). No frontend/backend split  
**Performance Goals**: N/A — documentation-only change; no runtime performance characteristic. Reader-comprehension target inherited from SC-002 ("identify the correct variable on first read")  
**Constraints**: (1) Bash 3.2 + POSIX `pwd -P` only — no `readlink -f`, no GNU coreutils, no Python 3 dependency in the normative idiom; (2) preserve FR-012 backward-compatibility (legacy Skills keep working); (3) keep `templates/commands/skills.md` concise and progressive-disclosure-friendly; (4) `${VAR:-fallback}` pattern must preserve agent-runtime exports when present (per Q3 clarification)  
**Scale/Scope**: 4 in-scope edit targets (1 template + 2 SKILL.md pairs); 1 new contract test file; 1 migration mapping table with ≥3 legacy idiom rows; 6 pre-existing Skills covered by the regression-only verification (per SC-004)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **I. Specification-Driven Development**: ✅ Every change traces to a numbered FR/SC in `requirements.md`; the plan adds no behavior beyond what the spec mandates.
- **II. Feature-Centric Development**: ✅ Bound to Feature `013` / `Skills Command` (per Clarifications Q1). `features.md` and `features/013.md` will be updated by the `/speckit.plan` integration step.
- **III. Intent-Driven Development**: ✅ The "what" (two named variables with single canonical meaning) and the "why" (agent-engine independence, separation of Skill-owned vs. user-facing paths) are the spec's focus; "how" (which shell incantation) is settled in Phase 0 research below.
- **IV. Test-First & Contract-Driven**: ✅ Phase 1 generates a structural contract (`contracts/skill-home-workdir-template.openapi.yaml`) and the task plan will create a contract test asserting the contract *before* the template/SKILL.md edits land.
- **V. AI Agent Integration**: ✅ Convention is explicitly agent-engine-agnostic (FR-007, FR-013); no new providers introduced.
- **VI. Continuous Quality & Observability**: ✅ No new code → no new logging surface. Semver: this is a non-breaking documentation MINOR-style change for `templates/commands/skills.md`. CI quality gates exercised by the new contract test.
- **VII. SDD Workflow Compliance**: ✅ Following requirements → clarify → plan; tasks/implement handoffs identified at end of file.

**Gates Status**: ✅ All gates pass.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/012-skill-home-workdir/
├── plan.md              # This file
├── research.md          # Phase 0 output — readlink-f portability + script self-locate primitive decisions
├── data-model.md        # Phase 1 output — SKILL_HOME, SKILL_WORKDIR, MigrationMappingEntry, TemplateSection entities
├── quickstart.md        # Phase 1 output — author walkthrough for using the new convention
├── contracts/
│   └── skill-home-workdir-template.openapi.yaml  # Phase 1 output — structural contract for templates/commands/skills.md
├── feature-ref.md       # Phase 1 output — links back to Feature 013 with this iteration's deltas
├── checklists/
│   └── requirements.md  # Pre-existing /speckit.checklist output
└── requirements.md      # Spec (input)
```

### Source Code (repository root)

```text
templates/
└── commands/
    └── skills.md                              # PRIMARY EDIT: add SKILL_HOME/SKILL_WORKDIR section, paired example,
                                               #   migration mapping, FR-016 script idiom

skills/
├── create-skills/
│   └── SKILL.md                               # EDIT: rename SKILL_ROOT → SKILL_HOME (lines 37, 39, 42, 91)
└── improve-skills/
    └── SKILL.md                               # EDIT: add legacy idiom detection for FR-010

.specify/
├── skills/
│   ├── create-skills/
│   │   └── SKILL.md                           # MIRROR EDIT (canonical install location)
│   └── improve-skills/
│       └── SKILL.md                           # MIRROR EDIT
└── instructions.md                            # CONSISTENCY CHECK ONLY — verify Skills registry rows
                                               #   don't drift; no edit expected unless they reference SKILL_ROOT

CLAUDE.md                                       # SYMLINK to .specify/instructions.md — covered by the check above

tests/
└── contract/
    └── test_skill_home_workdir_template.py    # NEW: structural assertions on the four edited files
```

**Structure Decision**: Single-project layout (Python CLI + Markdown templates + reusable Skills). No new directory levels; this iteration is a localized edit + test-add. The mirrored pair `skills/<name>/SKILL.md` ↔ `.specify/skills/<name>/SKILL.md` is the established Spec Kit pattern (per `008-create-skills-skill` precedent); both copies must stay in sync within this change.

## Phase 0: Research & Decisions

The clarify phase deferred one item to planning ("the exact portable recipe for `readlink -f`"). Two additional implementation-level decisions need to be settled before the template wording is finalized. These are captured below; if they grow further they will be promoted into `research.md`.

### Decision 1: Portable `readlink -f` replacement for the script self-locate idiom

**Decision**: Use POSIX `cd … && pwd -P` to resolve a script's real directory; do NOT rely on `readlink -f`.

- Normative script idiom (FR-016): 
  ```bash
  SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}"
  SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"
  ```
- `pwd -P` resolves the *physical* (symlink-followed) absolute path on every POSIX shell, including stock macOS `/bin/bash` 3.2 and Alpine `ash`. No GNU coreutils dependency, no Python fallback needed.
- `${BASH_SOURCE[0]:-$0}` lets the same idiom work whether the script is `bash script.sh` (BASH_SOURCE set) or `sh script.sh` (falls back to `$0`).
- The `/..` segment assumes the conventional placement `${SKILL_HOME}/scripts/<name>.sh`. The template will state that script depth explicitly; deeper-nested scripts adjust the `..` count.

**Rationale**: The original `readlink -f SKILL.md` example in the user's input is a *conceptual* recipe (compute SKILL_HOME from a known SKILL.md path) and remains valid in prose. But the *normative script-side* recipe must be portable, and `cd + pwd -P` is the simplest portable substitute. Adding a Python fallback would introduce a Python 3 hard dependency for every Skill shell script, which is heavier than the problem warrants.

**Alternatives considered**:
- `readlink -f` directly: rejected — fails on stock macOS shells before 10.13 and on any system where `readlink` is BSD-only.
- A POSIX shell loop that manually walks symlinks: rejected — too verbose for an idiom that every Skill script must inline.
- Python 3 fallback (`python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))"`): rejected — adds a Python 3 dependency where none exists today and would surprise shell-only Skill authors.

### Decision 2: Variable canonical written form vs. computation idioms

**Decision**: `${SKILL_HOME}` and `${SKILL_WORKDIR}` are the canonical *written* form in all contexts (SKILL.md prose, code blocks, template guidance) regardless of execution environment. The shell-form computation idioms (FR-003, FR-016) are normative *examples* — agents without a shell resolve the variables semantically but the written form is unchanged.

**Rationale**: Matches FR-007 and FR-013 unambiguously. Authors learn one syntax; non-shell agents (e.g., LLM-only resolution) treat the same syntax as a semantic placeholder.

### Decision 3: Scope of CLAUDE.md / `.specify/instructions.md` edits

**Decision**: No automatic edits to `CLAUDE.md` or `.specify/instructions.md`. Verify they contain no `SKILL_ROOT` references (grep check in the contract test); if a future audit finds drift, raise a follow-up.

**Rationale**: FR-015 requires consistency, not unconditional edits. Current grep (Phase 0 evidence) shows `SKILL_ROOT` only in `skills/create-skills/SKILL.md` and its mirror — already in the edit scope. The Skills registry rows in `.specify/instructions.md` reference canonical paths, not the deprecated variable name.

**Output**: `research.md` will record these three decisions as locked-in design choices.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

Three first-class entities and one supporting structure:

1. **SKILL_HOME** (variable):
   - `name`: `SKILL_HOME`
   - `meaning`: Real on-disk directory containing the Skill's `SKILL.md`, after symlink resolution
   - `canonical_written_form`: `${SKILL_HOME}`
   - `script_resolution_recipe`: `${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}`
   - `conceptual_resolution_recipe`: `dirname $(readlink -f SKILL.md)` (prose only)
   - `invariants`: post-symlink, absolute, agent-independent, identical across compatibility entrypoints
   - `usage_rule`: every Skill-owned resource reference (scripts/references/assets) goes through `${SKILL_HOME}/...`

2. **SKILL_WORKDIR** (variable):
   - `name`: `SKILL_WORKDIR`
   - `meaning`: Working directory of the Skill-invoked process at run time — typically the user's project root
   - `canonical_written_form`: `${SKILL_WORKDIR}`
   - `script_resolution_recipe`: `${SKILL_WORKDIR:-$(pwd -P)}`
   - `invariants`: runtime-bound, equal to the directory the agent invoked the Skill from, distinct from `SKILL_HOME`, anchored across nested invocations
   - `usage_rule`: every user-facing path (inputs/outputs in the user's project) goes through `${SKILL_WORKDIR}/...`

3. **MigrationMappingEntry** (table row):
   - `legacy_pattern`: e.g., `./X`, `${SKILL_ROOT}/X`, `~/.copilot/skills/<name>/X`
   - `new_pattern`: corresponding `${SKILL_HOME}/X` form
   - `example_before` / `example_after`: concrete one-line examples
   - At least 3 rows present (covers FR-011 / SC-005)

4. **TemplateSection** (structural):
   - Enumerates the named sections the updated `templates/commands/skills.md` MUST contain:
     - `Path Conventions` (defines both variables)
     - `Computation Idioms` (script-side + conceptual)
     - `Paired Example` (one script doing a Skill-owned read + a user-facing write)
     - `Migration Mapping` (the table above)
     - `Non-shell Agents` (semantic-resolution clause)

### Contract (`contracts/skill-home-workdir-template.openapi.yaml`)

Following the precedent set by `008-create-skills-skill/contracts/create-skills-workflow.openapi.yaml`, the structural contract for documentation deliverables is encoded as an OpenAPI schema describing a single "validate template assets" operation. The contract defines:

- A `validateTemplateAssets` operation whose response payload lists, for each of the four edited files, the structural assertions that must hold (sections present, paired example present, migration mapping rows ≥ 3, zero `SKILL_ROOT` references in scoped files, normative script idiom verbatim).
- Error schema for any failed assertion (file path + section name + reason).

This contract is what the new `tests/contract/test_skill_home_workdir_template.py` asserts in CI.

### Quickstart (`quickstart.md`)

A walkthrough for a Skill author writing their first script under the new convention: copy the FR-016 idiom into a new script, write one `${SKILL_HOME}` read and one `${SKILL_WORKDIR}` write, run it from a user project, verify the paths resolve as expected. Mirrors the User Story 2 acceptance scenario.

### Feature Reference (`feature-ref.md`)

Captures the link back to Feature 013 with this iteration's deltas — primarily Key Change #15 from `features/013.md`, with a forward pointer to `plan.md` and the eventual `tasks.md`.

## Re-evaluation Post-Design

**Constitution Check (post-Phase 1)**: ✅ All gates still pass. Design adds one test file and four documentation edits; no new modules, no new dependencies, no architectural changes. The contract-test-first ordering preserves Principle IV.

**Complexity Tracking**: N/A — no constitution violations to justify.

## Phase 2 Handoff

This command stops here. Next step: `/speckit.tasks` to decompose into atomic tasks. The expected task shape:
- Phase 1 (Setup): create the new contract test file with failing assertions.
- Phase 2 (Foundational): finalize the portable shell idiom and the migration mapping table content.
- Phase 3 (US1 / US2 — P1): edit `templates/commands/skills.md` with the new section, paired example, and table; verify contract test now passes for the template.
- Phase 4 (US3 — P2): edit `skills/create-skills/SKILL.md` (rename `SKILL_ROOT`, adopt `${SKILL_HOME}`) and its mirror; edit `skills/improve-skills/SKILL.md` to flag legacy idioms; sync mirrors; final contract test pass.
- Phase 5 (Verification): SC-003 (two-layout regression) + SC-004 (six pre-existing Skill smoke check).
