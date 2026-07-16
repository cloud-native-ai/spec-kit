# Implementation Plan: Project Glossary Mechanism (项目词汇表机制)

**Branch**: `029-glossary-mechanism` | **Date**: 2026-07-16 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `029-glossary-mechanism` → Feature 031 Glossary Mechanism
**Input**: Specification from `.specify/specs/029-glossary-mechanism/requirements.md`

## Summary

Introduce a single project-wide glossary (词汇表) — a human-readable, user-editable Markdown artifact at `.specify/memory/glossary.md` — that anchors project vocabulary and corrects voice/dictated input errors (homophones, easily-confused words). The glossary is **initialized at instruction generation**, **referenced ambiently** by every `/speckit.*` command (via the Documentation Map in the generated `.specify/instructions.md`, exactly like the constitution), **progressively enriched** at workflow checkpoints, and **conflict-checked** with mandatory user confirmation before any conflicting write. Manual user edits are always authoritative.

Consistent with Principle IX (Framework Scope Discipline), this is a **documentation/prompt-framework** capability, not a runtime service: the term-correction and conflict-*judgment* are prompt instructions interpreted by the AI agent; a small, dependency-free `glossary-utils.py` engine (mirroring `feedback-utils.py` / `history-utils.py` / `memory-utils.py`) provides deterministic file operations (init-from-template, list, append, structural validation) so programmatic and manual edits coexist safely.

## Technical Context

**Language/Version**: Python `>=3.8` (engine `glossary-utils.py`, matching project baseline); Markdown for the glossary artifact, templates, and shared-workflow protocol; Bash for the instruction-generation hook.  
**Primary Dependencies**: Python standard library only — **no new runtime dependencies** (same discipline as the existing `*-utils.py` engines).  
**Storage**: Files. One project-wide artifact `.specify/memory/glossary.md` (canonical), seeded from `templates/glossary-template.md` ↔ `.specify/templates/glossary-template.md`.  
**Testing**: `pytest` with existing `contract` / `unit` markers; contract test verifies template presence, glossary structure, Documentation-Map wiring, and non-destructive re-init (pattern: `tests/contract/test_agent_skill_enablement.py`); unit tests cover `glossary-utils.py` file ops.  
**Target Platform**: Repo-local CLI tooling (cross-platform: Bash + Python), consumed by all supported AI agents.  
**Project Type**: single — code generator / framework (templates/, scripts/, src/specify_cli/).  
**Performance Goals**: N/A (document framework). Glossary parse/append is trivial for expected sizes.  
**Constraints**: No new dependencies; non-destructive to user-authored glossary content on re-init (FR-011/FR-013); offline-capable; MUST NOT regress the existing test baseline (long-standing pre-existing failures excluded); mirror-sync discipline for `templates/` ↔ `.specify/templates/`, `shared/workflow/` ↔ `.specify/shared/workflow/`, and per-tool command copies.  
**Scale/Scope**: Exactly one glossary per project; tens-to-hundreds of entries typical; touches instruction-generation, a shared-workflow protocol doc, and a lightweight `## Glossary` reference on the workflow command templates.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Design traces to FR-001…FR-015 in `requirements.md`; every artifact below maps to a requirement. |
| II | Feature-Centric Development | ✅ Pass | Binds to new **Feature 031 Glossary Mechanism** (no existing feature fit — clarified 2026-07-16); registered in `features.md` + `features/031.md`, status → Planned. |
| III | Intent-Driven Development | ✅ Pass | Spec captures WHAT/WHY (anchoring, voice correction, domain knowledge); plan maps intent to prompt/template artifacts before HOW. |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Majority is template/prompt content (Principle VII "template-only" clause); executable `glossary-utils.py` receives unit + contract tests written before implementation. |
| V | AI Agent Integration Standards | ✅ Pass | Glossary is loaded ambiently across ALL supported tools through the existing `.specify/instructions.md` symlinks (CLAUDE.md/QWEN.md/…); no new/unsupported agent introduced. |
| VI | Continuous Quality & Observability | ✅ Pass | YAGNI honored (minimal file-mgmt engine, no runtime infra); corrections are traceable/visible (FR-006); changes reflected in specs/plan/tasks/docs. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following spec→plan→(tasks)→implement; Feature Index re-evaluated this phase; status advanced Draft→Planned (not Implemented). |
| VIII | Code as the Single Source of Truth | ✅ Pass | `glossary-utils.py` is authoritative for file operations; `glossary.md` is a data artifact; no doc-vs-code drift introduced. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Glossary = editable Markdown + prompt protocol + small file-mgmt helper. Correction & conflict-judgment are PROMPT INSTRUCTIONS, not a runtime NLP/homophone service. Directly upholds the No-DFX standard. |
| X | Documentation Naming & Location Conventions | ✅ Pass | `glossary.md` (lowercase kebab) placed semantically: `.specify/memory/glossary.md` (project memory) and `shared/workflow/glossary.md` (the glossary protocol of the workflow); template `glossary-template.md`. |

**Gates Status**: ✅ All gates pass — Principle IV is a justified Partial (template-heavy feature per Principle VII), recorded in Complexity Tracking; no unjustified violations.

**Re-check after Phase 1**: 2026-07-16 — Re-ran the table against generated `data-model.md`, `contracts/`, and `quickstart.md`. No principle regressed; IV remains a justified Partial (engine tests specified in contracts before implementation). Gates still pass.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/029-glossary-mechanism/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # /speckit.requirements + /speckit.clarify output
├── data-model.md        # Phase 1 output (this command)
├── quickstart.md        # Phase 1 output (this command)
├── contracts/           # Phase 1 output (this command)
│   ├── glossary-file-format.md      # Structure/columns of .specify/memory/glossary.md
│   ├── glossary-utils-cli.md        # glossary-utils.py action contract
│   ├── instruction-init.md          # Init-at-instruction-generation contract
│   └── glossary-protocol.md         # Ambient correction/enrichment/conflict protocol
├── checklists/
│   └── requirements.md  # /speckit.requirements quality checklist (passing)
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

No standalone extended research needed — Phase 0 findings are internal and inlined below (< 50 lines).

### Source Code (repository root)

```text
templates/                          # + glossary-template.md (canonical glossary skeleton + authoring rules)
.specify/templates/                 # + glossary-template.md (mirror — dual-write per mirror-sync map)
shared/workflow/                    # + glossary.md (ambient correction/enrichment/conflict protocol)
.specify/shared/workflow/           # + glossary.md (mirror)
scripts/python/                     # + glossary-utils.py (dependency-free file-mgmt engine)
scripts/bash/                       # generate-instructions.sh — hook: seed .specify/memory/glossary.md if absent (non-destructive)
templates/instructions-template.md  # + Documentation Map row → .specify/memory/glossary.md (makes glossary ambient)
templates/commands/                 # + `## Glossary` reference step on requirements/plan/tasks/implement (cite shared protocol)
tests/contract/                     # + test_glossary_mechanism.py (template/structure/wiring/non-destructive re-init)
tests/unit/                         # + glossary-utils.py file-op unit tests
.specify/memory/glossary.md         # RUNTIME ARTIFACT — created at instruction generation, not committed as source
```

**Structure Decision**: This spec extends the existing **code-generator / framework** layout. It adds one new template (`glossary-template.md`, dual-written to `.specify/templates/`), one new shared-workflow protocol doc (`shared/workflow/glossary.md`, mirrored), one new Python engine (`scripts/python/glossary-utils.py`), and weaves references into `generate-instructions.sh`, `instructions-template.md` (Documentation Map), and the four workflow command templates (a `## Glossary` step, modeled on the existing `## Feedback` step). No new top-level directory is introduced. The glossary itself (`.specify/memory/glossary.md`) is a generated per-project runtime artifact that lives beside `constitution.md` and `features.md`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV (Test-First) marked **Partial** | The feature is predominantly template + prompt-protocol content, which has no executable behavior to unit-test in the classical sense; per Principle VII's "template-only features" clause, tests instead verify template content, canonical paths, structure, and non-destructive re-init. The one executable component (`glossary-utils.py`) DOES follow Test-First with unit + contract tests authored before implementation. | Forcing full runtime test coverage on static template/prompt text would fabricate meaningless assertions and contradict Principle IX (no over-engineering); a hybrid (contract tests for structure + TDD for the engine) is the faithful minimum. |

## Phase 0: Research Review (inlined)

**Decision 1 — Artifact location & form.** Single Markdown file `.specify/memory/glossary.md`, beside `constitution.md`/`features.md`. Rationale: matches the canonical project-memory pattern (human-readable, git-diffable, directly editable → satisfies FR-010/FR-012); one-per-project satisfies FR-014 (clarified). Rejected: YAML/JSON (worse for manual editing, Principle X/IX) and per-feature glossaries (rejected in clarify).

**Decision 2 — Ambient availability.** Add a Documentation Map row to `instructions-template.md` pointing at `.specify/memory/glossary.md`. Because `generate-instructions.sh` renders `.specify/instructions.md` and symlinks it to CLAUDE.md/QWEN.md/QODER.md/AGENTS.md/copilot-instructions.md, every supported agent then loads the glossary as ambient context (same mechanism that makes the constitution ambient) → satisfies FR-015 without touching each command's runtime.

**Decision 3 — Initialization hook.** Extend `generate-instructions.sh` to create `.specify/memory/glossary.md` from `templates/glossary-template.md` **only if absent**, preserving any existing file (non-destructive, mirroring its existing `## Project Overview` preservation) → satisfies FR-001/FR-013. Seeding of observed domain terms is a prompt step in the instructions command (AI reads docs/constitution/feature names).

**Decision 4 — Correction / enrichment / conflict protocol.** A shared doc `shared/workflow/glossary.md` (mirrored to `.specify/shared/workflow/`) defines: variant→canonical anchoring for voice input (FR-005), visible/traceable corrections (FR-006), defer-on-ambiguity (FR-007), checkpoint-based term proposals (FR-004), conflict detection + mandatory user confirmation (FR-008/FR-009), and user-precedence (FR-011). Workflow command templates gain a lightweight `## Glossary` reference (pattern: existing `## Feedback` step) citing this doc — no logic duplicated per command.

**Decision 5 — Engine vs. pure prompt.** Deterministic file ops (init, list, append, validate structure) go in `scripts/python/glossary-utils.py` (stdlib-only, consistent with the five existing `*-utils.py` engines) so manual + programmatic edits stay structurally valid. Fuzzy work (homophone/confusable judgment, meaning-conflict detection) stays PROMPT-side — no runtime NLP dependency (Principle IX).

**Unknowns**: none blocking — all Technical Context fields resolved from project docs + constitution; no `/speckit.research` needed.
