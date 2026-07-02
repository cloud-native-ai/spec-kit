# Implementation Plan: EEI Agent Triad

**Branch**: `022-eei-agent-triad` | **Date**: 2026-07-02 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/022-eei-agent-triad/requirements.md`

## Summary

Add the Executor-Evaluator-Improver (EEI) triad pattern to the existing Role-Based Agent architecture. The triad adds a second dimension to agent design: within any role, work can be decomposed into three independent sub-agents (Executor, Evaluator, Improver) that operate in a quality-gated iterative loop. Implementation consists of: (1) three new sub-role agent templates, (2) a triad orchestration prompt template, (3) updates to create-agent and improve-agent skills to support triad creation, and (4) a reference guide documenting the pattern.

## Technical Context

**Language/Version**: N/A — this is a template/prompt engineering feature, not runtime code  
**Primary Dependencies**: Existing agent template system (`templates/agent-role-*-template.md`), create-agent skill, improve-agent skill  
**Storage**: Filesystem — `.specify/agents/` directory for generated agents, `templates/` for templates  
**Testing**: Contract tests verifying template rendering; integration test applying the triad to a sample task  
**Target Platform**: All supported AI agents (Claude Code, Copilot, Qwen, opencode, Qoder)  
**Project Type**: Template/prompt system (extends existing `templates/` + `skills/` directories)  
**Performance Goals**: N/A — template rendering is near-instantaneous  
**Constraints**: Templates must follow existing YAML frontmatter + Markdown body format; must compose with all 6 existing role templates  
**Scale/Scope**: 3 new sub-role templates, 1 orchestration template, 2 skill updates, 1 reference guide

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Spec `022-eei-agent-triad/requirements.md` drives all template design; 12 FRs trace to 5 user stories |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 019 (Agents Command); feature index updated |
| III | Intent-Driven Development | ✅ Pass | Pattern derived from real session experience (K8s diagram 49→91); intent documented in Context & Motivation |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract defined for triad orchestration protocol; test scenarios in US1-US5 acceptance criteria |
| V | AI Agent Integration Standards | ✅ Pass | Templates target all Tier 1 agents; sub-role templates follow existing `agent-role-*-template.md` format |
| VI | Continuous Quality & Observability | ✅ Pass | FR-007 requires iteration history tracking; FR-005 requires structured scoring output |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full SDD workflow followed: requirements → clarify → plan → tasks → implement |

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/022-eei-agent-triad/
├── requirements.md          # Feature specification
├── plan.md                  # This file
├── data-model.md            # Triad entity model
├── contracts/               # Orchestration protocol contracts
│   └── triad-protocol.md    # EEI loop protocol specification
├── quickstart.md            # How to create and use an EEI triad
├── checklists/
│   └── requirements.md      # Spec quality checklist
└── tasks.md                 # Task breakdown (via /speckit.tasks)
```

No standalone research.md — findings inlined below (pattern fully understood from session experience).

### Source Code (repository root)

```text
templates/                                    # New sub-role templates
├── agent-subrole-executor-template.md        # Executor sub-role template
├── agent-subrole-evaluator-template.md       # Evaluator sub-role template
├── agent-subrole-improver-template.md        # Improver sub-role template
└── agent-triad-orchestration-template.md     # Orchestration prompt template

skills/create-agent/                          # Updated skill
└── SKILL.md                                  # Add triad creation support

skills/improve-agent/                         # Updated skill
└── SKILL.md                                  # Add triad improvement support

docs/                                         # Reference documentation
└── eei-triad-pattern.md                      # Pattern guide with examples
```

**Structure Decision**: Extends the existing agent template system by adding 3 sub-role templates (`agent-subrole-*`) alongside the 6 existing role templates (`agent-role-*`). The `subrole` prefix distinguishes them from role-level templates. One orchestration template provides the loop scaffold. No new top-level directories.

## Complexity Tracking

N/A — no constitution violations.

## Phase 0: Research Review

### Findings from Session Experience

The K8s diagram optimization session (17 rounds, score 49→91) provided complete empirical evidence:

**What worked:**
- Independent subagent invocation (no shared context) → clean evaluation
- Evaluator receiving ONLY output artifacts (PNG) → unbiased scoring
- Improver modifying skill reference files → environment improvement persists across iterations
- Structured scoring output (per-dimension + weighted total + suggestions) → actionable feedback
- Grouping arrows by semantic category in prompts → better executor output quality

**What didn't work:**
- Re-scoring the same output hoping for a higher score → waste of tokens
- Adding notes/elements to "help" the evaluator → often hurt aesthetics score
- Switching layout direction mid-loop without clear evidence → caused regressions

**Key design decisions:**
- The orchestrator (main agent) manages the loop, NOT the sub-agents themselves
- Each sub-agent is a fresh invocation with no memory of prior rounds
- The improver's changes to files persist on disk, so the executor naturally picks them up
- Scoring variability of ±3 points is inherent to LLM-based evaluation; the loop handles this by tracking the best score

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for full entity definitions.

### Contracts

See [contracts/triad-protocol.md](contracts/triad-protocol.md) for the orchestration protocol.

### Quickstart

See [quickstart.md](quickstart.md) for usage guide.
