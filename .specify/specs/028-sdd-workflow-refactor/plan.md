# Implementation Plan: Reclassify sdd-workflow as a Shared Reference Directory

**Branch**: `028-sdd-workflow-refactor` | **Date**: 2026-07-14 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `028-sdd-workflow-refactor` → Feature 029 Shared Reference Directory
**Input**: Specification from `.specify/specs/028-sdd-workflow-refactor/requirements.md`

## Summary

Move the ten shared SDD protocol documents out of the `sdd-workflow` "skill" (which self-declares it is not invocable) into a first-class shared reference directory: source `shared/workflow/`, installed `.specify/shared/workflow/`. The directory is bundled into the wheel and copied wholesale at `init` — exactly like `templates/`/`scripts/` — added to the retained core-asset list, and reached through a `shared/ → .specify/shared/` path-rewrite rule. `sdd-workflow` is deleted from `skills/`, removed from the skills registry/count and all skills symlink surfaces, and its ~38 source references (18 template files + 20 skill files, plus 4 docs) are rewritten to the new location in a single consistent form per artefact type. Acceptance gate: a repository-wide search for `sdd-workflow` returns zero live matches and no reference resolves to a dead link.

## Technical Context

**Language/Version**: Python `>=3.8` (CLI `src/specify_cli/__init__.py`); Bash (workflow scripts); Markdown (templates, skills, docs, shared references)  
**Primary Dependencies**: `hatchling` (PEP 517 wheel packaging, `force-include`), `typer`, `rich`, `httpx`; `pytest` for tests  
**Storage**: Filesystem only — source tree + the installed `.specify/` workspace mirror  
**Testing**: `pytest` with `contract` and `integration` markers (`tests/contract/`, `tests/integration/`, `tests/unit/`)  
**Target Platform**: Local developer CLI (Linux/macOS/Windows) invoked via `specify init`  
**Project Type**: Code generator / framework — `templates/`, `scripts/`, `skills/`, `agents/`, `src/specify_cli/`, packaged into the `specify-cli` wheel  
**Performance Goals**: N/A — one-time init-time directory copy; negligible cost  
**Constraints**: Zero runtime dead links (hard gate); content parity for all ten docs; installed `.specify/` mirror byte-consistent with source; no regression to the existing test suite; single reference form per artefact type (no mixing)  
**Scale/Scope**: 10 reference documents; ~38 referring source files; 5 CLI/packaging touchpoints; 4 docs files; the regenerated `.specify/` mirror

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every FR-001…FR-012 traces to a design artefact; refactor driven by requirements.md, not code-first |
| II | Feature-Centric Development | ✅ Pass | Feature 029 created in `features.md` + `features/029.md`; plan advances Draft→Planned |
| III | Intent-Driven Development | ✅ Pass | WHAT/WHY captured in spec; two decisions resolved via `/speckit.clarify`; multi-step refinement |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` define behavioral contracts; contract/integration tests authored before edits; zero-reference gate is the regression guard |
| V | AI Agent Integration Standards | ✅ Pass | Supported agent list unchanged; skills-symlink model for all tiers preserved; shared dir reached only via `.specify/` paths (no new symlink surface) |
| VI | Continuous Quality & Observability | ✅ Pass | Docs updated (map, skills docs); YAGNI-simple (reuse existing copy/rewrite patterns); CI test suite must stay green |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following requirements → plan → tasks → implement; Feature Index re-validated this phase |

**Gates Status**: ✅ All gates pass

**Re-check after Phase 1**: 2026-07-14 — Re-evaluated against `data-model.md` + `contracts/` + `quickstart.md`. No principle regresses; all rows remain ✅ Pass. Test-First strengthened by five concrete contracts. Complexity Tracking remains N/A.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/028-sdd-workflow-refactor/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output — asset/reference entities
├── quickstart.md        # Phase 1 output — verification walkthrough
├── contracts/           # Phase 1 output — 5 behavioral contracts
├── checklists/
│   └── requirements.md  # From /speckit.requirements + /speckit.clarify
├── requirements.md      # Feature specification (input)
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement)
```

No standalone `research.md` — Phase 0 findings are internal (code inspection) and inlined below under **Phase 0**.

### Source Code (repository root)

```text
shared/workflow/                    # NEW source dir — 10 relocated reference docs (was skills/sdd-workflow/references/)
skills/sdd-workflow/                # DELETED — pseudo-skill removed (SKILL.md + references/)
src/specify_cli/__init__.py         # init copy block, _CORE_SPECIFY_ASSETS, rewrite_paths()
pyproject.toml                      # wheel force-include: add "shared" = "specify_cli/shared"
templates/commands/*.md             # 17 command templates — rewrite refs to shared/workflow/...
templates/skills-template.md        # skills template — rewrite ref to .specify/shared/workflow/...
skills/*/SKILL.md                   # 20 sibling skills — rewrite hard-coded refs to .specify/shared/workflow/...
docs/agents/, docs/commands/, docs/skills/  # 4 docs — describe shared dir, not a skill; fix skill count
```

**Structure Decision**: Extends the existing code-generator/framework layout by introducing one new top-level source directory (`shared/`, with a `workflow/` family subdir) that follows the identical *source → `.specify/`* install model already used by `memory/`, `scripts/`, `templates/`, `skills/`, and `agents/`. No new architectural pattern is introduced; the change reuses the wheel `force-include` mechanism, the init `shutil.copytree` copy pattern, the `_CORE_SPECIFY_ASSETS` retention list, and the `rewrite_paths()` regex family. The only deletion is the `skills/sdd-workflow/` directory.

## Phase 0: Research Review

Findings from direct inspection of the current code (no external research needed):

**Install model (5 parallel precedents).** `pyproject.toml` `[tool.hatch.build.targets.wheel.force-include]` maps `memory`, `scripts`, `templates`, `skills`, `agents` → `specify_cli/<name>`. At init, `src/specify_cli/__init__.py` copies each into `.specify/` via `shutil.copytree(..., dirs_exist_ok=True)` (scripts ~L1119, skills ~L1267, agents ~L1283; templates item-by-item ~L1133). The new `shared/` follows the `skills`/`agents` shape exactly (whole-directory copytree into `.specify/shared`).

**Retention.** `_CORE_SPECIFY_ASSETS` (L308) lists the `.specify/` paths preserved across re-init; `detect_initialized_core_assets` drives refresh protection. Adding `".specify/shared"` makes the new dir a retained core asset.

**Path rewrite.** `rewrite_paths()` (L674) applies negative-lookbehind regex for `memory/`, `scripts/`, `templates/` → `.specify/<x>/`. It runs on command bodies during `generate_commands` (L844). Adding a `shared/ → .specify/shared/` rule lets command templates use root-relative `shared/workflow/...`.

**Reference inventory.** `sdd-workflow` appears in: 17 `templates/commands/*.md` + `templates/skills-template.md` (18 template files, root-relative form); 20 sibling `skills/*/SKILL.md` (hard-coded `.specify/skills/sdd-workflow/...` form); 4 docs (`docs/agents/command-and-skills.md`, `docs/agents/design.md`, `docs/commands/skills.md`, `docs/skills/feedback.md`); and the generated `.specify/` mirror (regenerated, not hand-edited). `docs/summary/03-sdd-workflow-refactor-proposal.md` and this spec are excluded as archival.

**Skill registry & count.** The skill list/count ("20 total … sdd-workflow …") lives in the generated instructions file (`.specify/instructions.md` L54 and its symlinks), produced by `/speckit.instructions`; `skills-utils.py` enumerates `*/SKILL.md` under `.specify/skills` and `.github/skills` (L262-267). Deleting `skills/sdd-workflow/` plus regenerating instructions removes it from the registry, count, and skill-discovery automatically.

**Symlink surface.** `_check_skills_symlink` / `ensure_specify_symlink` symlink `.specify/skills` into `<tool>/skills`. Because `shared/` is referenced only through `.specify/shared/...` paths (never discovered as a skill), it needs **no** new symlink surface; removing `sdd-workflow` from `.specify/skills` removes it from every tool's skills view.

**Feedback-step reference.** `skills/sdd-workflow/references/feedback-step.md` is the canonical `## Feedback` step consumed by skills/commands (Feature 028). It moves to `shared/workflow/feedback-step.md` with the other nine docs and its references are rewritten alongside.

## Phase 1: Design & Contracts

Artifacts generated (see files in this directory):

- **`data-model.md`** — Entities: Shared Reference Directory, Reference Document (×10), Reference Link (two forms), Core Asset Retention entry, Path-Rewrite Rule, Skill Registry Entry (removed). Includes the exhaustive relocation map and the referring-file inventory.
- **`contracts/`** — Five behavioral contracts:
  - `install-copy.contract.md` — `shared/` bundled in wheel and copied to `.specify/shared` at init; retained across re-init.
  - `path-rewrite.contract.md` — `rewrite_paths()` maps root-relative `shared/` → `.specify/shared/` with the same negative-lookbehind guard.
  - `reference-rewrite.contract.md` — exact old→new mapping and the per-artefact form rule (templates root-relative; skills absolute).
  - `skill-removal.contract.md` — `sdd-workflow` absent from `skills/`, `.specify/skills`, tool symlinks, registry table, and count.
  - `zero-reference-gate.contract.md` — the final `grep` gate with its exclusion set and no-dead-link assertion.
- **`quickstart.md`** — Step-by-step verification: fresh init, re-init retention, reference resolution, and the zero-reference grep gate.

**Post-design Constitution re-check**: table above refreshed — all ✅ Pass; Test-First satisfied by the five contracts and their mapped tests.

## Complexity Tracking

N/A — no Constitution violations; the design reuses existing install/rewrite/retention patterns without introducing new abstractions.
