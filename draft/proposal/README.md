# spec-kit Improvement Proposals — toward a universal agent-coding framework

> **Status: draft.** These proposals live in `draft/` and describe *possible* evolutions of
> spec-kit. None is implemented or wired into the main `/speckit.*` flow yet. Each proposal is
> self-contained and independently adoptable; adopt in the phased order below or cherry-pick.

## Vision

Evolve spec-kit from a **Spec-Driven Development CLI** into a **universal agent-coding
assistant framework** that unifies four pillars:

| Pillar | Today | Target |
|--------|-------|--------|
| **Skills** | `skills/<name>/SKILL.md` + Registry | Auto-discovered, progressively-disclosed, self-authoring skill library |
| **Commands** | `/speckit.*` static markdown flow | Broad composable command catalog with handoffs |
| **Workflow / Process** | Linear spec→plan→tasks→implement | Task graphs, parallel worktrees, autonomous loops, event hooks, quality gates |
| **Scripts** | `scripts/bash` + `scripts/python` helpers | A tool/registry + MCP layer and optional runnable runtime |

**Guiding principle — enhance, don't replace.** spec-kit is *scaffolding that steers an agent
harness*, not a competing runtime. Every proposal is expressed, wherever possible, as
templates / skills / commands / scripts / settings that layer on top of the existing flow.
Nothing here should disturb the current `/speckit.*` pipeline until deliberately promoted.

## How these proposals were produced

Ten analysis subagents mined **seven external open-source projects** through a single lens:
*what concretely would move spec-kit toward the universal-framework goal?* Raw per-project
mining reports (with file-path evidence) are preserved under [`_research/`](_research/).

| Source project | Lens | What it contributed |
|----------------|------|---------------------|
| **OpenSpec** | tooling beyond delta-spec | validation, status graph, per-artifact instruction injection, multi-harness adapters |
| **superpowers** | skills beyond SDD/TDD | brainstorming, systematic-debugging, writing-plans, verification gate, SessionStart auto-injection |
| **claw-code-agent** | runnable Python reimpl | zero-dep runtime loop, stdlib OpenAI-compatible client, declarative tool registry, parity + benchmark harness |
| **intellegix-code-agent-toolkit** | config/orchestration | autonomous loop driver, completion gate, worktree multi-agent, multi-model council, portfolio governance, command catalog, MCP template |
| **claude-code-ts** | full TS harness | tool-search/deferred tools, MCP client, workflow engine, goal-continuation loop, coordinator/worker, lifecycle hooks, compaction, skill-learning |
| **claude-code-py** | distribution/config | event hooks system, guardrail rules, plugin marketplace, layered/managed settings |
| **learn-claude-code** | harness patterns | file-based task DAG, worktree-per-task, context compaction ladder, task-claiming loop, request/response FSM |

## Proposal index

| # | Proposal | Pillar | Value | Effort | Phase |
|---|----------|--------|-------|--------|-------|
| P001 | [Hooks & Event Automation](P001-hooks-and-event-automation.md) | Process | H | M | 1 |
| P002 | [Skill System Evolution](P002-skill-system-evolution.md) | Skills | H | M | 1 |
| P003 | [Skill Library Expansion](P003-skill-library-expansion.md) | Skills | H | L–M | 1 |
| P004 | [Task Graph & Parallel Worktree Orchestration](P004-task-graph-and-worktree-orchestration.md) | Process | H | M–H | 2 |
| P005 | [Autonomous Loop Driver](P005-autonomous-loop-driver.md) | Process | H | H | 2 |
| P006 | [Verification & Quality Gates](P006-verification-and-quality-gates.md) | Process | H | M | 1 |
| P007 | [Context & Memory Management](P007-context-and-memory-management.md) | Process | H | M | 2 |
| P008 | [Tool Registry & MCP Integration](P008-tool-registry-and-mcp.md) | Scripts | H | M–H | 2 |
| P009 | [Workflow Engine & Deterministic Orchestration](P009-workflow-engine.md) | Workflow | H | H | 3 |
| P010 | [Command Catalog Expansion](P010-command-catalog-expansion.md) | Commands | M–H | L–M | 1 |
| P011 | [Optional Runtime, Local Models & Benchmarking](P011-runtime-local-models-benchmarking.md) | Scripts | M–H | H | 3 |
| P012 | [Plugin Packaging, Settings & Portfolio Governance](P012-plugin-settings-governance.md) | Infra | M–H | M–H | 2 |
| P013 | [Spec Validation, Status Graph & Multi-Harness Tooling](P013-validation-status-multiharness.md) | Infra | H | M–H | 1 |

## Phased roadmap

**Phase 1 — Low-risk, high-leverage layers that don't touch the runtime**
P001 hooks, P002/P003 skills, P006 quality gates, P010 commands, P013 validation & multi-harness
tooling. These are mostly markdown, settings, and small scripts — the fastest wins.

**Phase 2 — Process & platform depth**
P004 task graph + worktrees, P005 autonomous loop, P007 context/memory, P008 tools + MCP,
P012 plugins/settings/governance. Introduces real orchestration state and extensibility.

**Phase 3 — Framework maturity**
P009 workflow engine, P011 optional runnable runtime + local models + benchmarks. These are the
largest bets and turn spec-kit from scaffolding into a full harness for teams that want it.

## Conventions

- Each proposal file is `PNNN-<slug>.md` and follows a shared template (Problem → Proposal →
  Design sketch → Source evidence → Adoption plan → Risks → Value/Effort).
- Cross-references use `[[PNNN]]`-style links between proposals.
- Anything that becomes real lands in `draft/` first (skills in `draft/skills/`, commands as
  drafts, scripts in a draft scripts area), then graduates via the promotion process in
  [`../README.md`](../README.md).
- `_research/` holds the source mining reports; treat them as evidence, not proposals.
