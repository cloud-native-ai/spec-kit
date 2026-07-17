# 🌱 Spec Kit Feature Index

**Last Updated**: 2026-07-16
**Total Features**: 31

## Features

| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |
|----|------|-------------|--------|-----------------|-----------|--------------|
| 001 | Unify Command Handoffs | Make command prerequisites and next steps explicit. | Planned | .specify/memory/features/001.md | - | 2026-02-10 |
| 002 | Analyze Command | Analyze project context and code structure. | Completed | .specify/memory/features/002.md | - | 2026-02-10 |
| 003 | Checklist Command | Verify project alignment with constitution. | Completed | .specify/memory/features/003.md | - | 2026-02-10 |
| 004 | Clarify Command | Resolve ambiguities in specifications. | Completed | .specify/memory/features/004.md | - | 2026-02-10 |
| 005 | Constitution Command | Manage project governance and principles. | Completed | .specify/memory/features/005.md | - | 2026-02-10 |
| 006 | Feature Command | Manage feature lifecycle and metadata. | Completed | .specify/memory/features/006.md | - | 2026-02-10 |
| 007 | Implement Command | Generate code from tasks and plans. | Completed | .specify/memory/features/007.md | - | 2026-02-10 |
| 008 | Instructions Command | Generate prompts for AI agents. | Completed | .specify/memory/features/008.md | - | 2026-02-10 |
| 009 | Plan Command | Create implementation plans from specs. | Completed | .specify/memory/features/009.md | - | 2026-02-10 |
| 010 | Requirements Command | Define requirements and specifications. | Completed | .specify/memory/features/010.md | - | 2026-02-10 |
| 011 | Research Command | Gather context and dependencies. | Completed | .specify/memory/features/011.md | - | 2026-02-10 |
| 012 | Review Command | Review implementation against rules. | Completed | .specify/memory/features/012.md | - | 2026-02-10 |
| 013 | Skills Command | Manage extensible skills/tools. | Implemented | .specify/memory/features/013.md | .specify/specs/017-consolidate-draft-skills/requirements.md | 2026-06-18 |
| 014 | Tasks Command | Break down plans into atomic tasks. | Completed | .specify/memory/features/014.md | - | 2026-02-10 |
| 015 | CLI Interface | Rich terminal interface using Typer. | Completed | .specify/memory/features/015.md | - | 2026-02-10 |
| 016 | Tools Command | Definition-first tool management: create, modify, and invoke tools with explicit behavioral rules, replacing discovery-driven approach. | Implemented | .specify/memory/features/016.md | .specify/specs/016-refactor-tools-command/requirements.md | 2026-06-17 (deferred: T022,T042,T043,T046) |
| 017 | Template Engine | Markdown-based template system. | Completed | .specify/memory/features/017.md | - | 2026-02-10 |
| 018 | Configuration Management | Project configuration via pyproject.toml. | Completed | .specify/memory/features/018.md | - | 2026-02-10 |
| 019 | Agents Command | Create or refine custom AI agents (.agent.md) for workspace-specific workflows. Includes EEI (Executor-Evaluator-Optimizer) triad pattern for iterative quality optimization. | Implemented | .specify/memory/features/019.md | .specify/specs/.archive/023-agent-framework-redesign/requirements.md | 2026-07-10 (spec 023 agent-framework-redesign implemented: Role/Stage/Type + Team/Loop model, terminology unification, supervisor merge, template canonicalization) |
| 020 | Qoder Support | Add Qoder as a supported CLI assistant across initialization, validation, documentation, and release distribution. | Implemented | .specify/memory/features/020.md | .specify/specs/006-add-qoder-support/requirements.md | 2026-03-30 |
| 021 | Claude Code Support | Add Claude Code as a first-class assistant with custom commands and Claude Code-specific configuration assets. | Implemented | .specify/memory/features/021.md | .specify/specs/009-claude-code-support/requirements.md | 2026-05-14 |
| 022 | AI Tools Support | Ensure all officially supported AI tools receive complete initialization coverage and can coexist without overwriting shared Spec Kit core files. | Implemented | .specify/memory/features/022.md | .specify/specs/021-agent-specific-config/requirements.md | 2026-07-12 (spec 024 agent-env-config implemented: unified env-var one-time config persisted to 6 CLI tools' own config files) |
| 023 | Prompt Template Quality | Structural validation and consistency enforcement across all command and skill templates. | Draft | .specify/memory/features/023.md | - | 2026-06-05 |
| 024 | Specification Workspace Versioning | Version management and migration support for .specify/ workspace structure across CLI releases. | Draft | .specify/memory/features/024.md | - | 2026-06-05 |
| 025 | Todo Command | Discover marked TODO blocks in text files and turn them into reviewable execution plans. | Implemented | .specify/memory/features/025.md | .specify/specs/020-speckit-todo-command/requirements.md | 2026-06-23 |
| 026 | Agent Skill Enablement | Empower the 7 built-in role agents to prefer installed framework skills for role-relevant operations, since skills and agent definitions install together. | Implemented | .specify/memory/features/026.md | .specify/specs/025-agent-skill-enablement/requirements.md | 2026-07-13 (spec 025 implemented: skills: frontmatter + ## Skill Enablement section on all 7 role agents + create-agent templates; contract test_agent_skill_enablement.py green) |
| 027 | Team Management | Dedicated team domain for multi-agent configuration: `/speckit.team` (create/modify/run) as the sole entry point, `create-team` (renamed from organize-agents) + `improve-team` skills, Conceptual Model extracted from create-agent, and single-agent vs team separation. | Implemented | .specify/memory/features/027.md | .specify/specs/.archive/026-agent-team-management/requirements.md | 2026-07-13 |
| 028 | Feedback Mechanism | Distributed, local-scope feedback layer: agent self-reflection optimization points generated at flow wrap-up for every skill and for complex (process-interaction) commands, persisted to `.specify/memory/feedback/` with a threshold-triggered consolidated submission prompt; complements the global `/speckit.review`. | Implemented | .specify/memory/features/028.md | .specify/specs/027-feedback-mechanism/requirements.md | 2026-07-14 (implemented: feedback-utils.py engine + `## Feedback` on all 21 skills & 13 complex commands; 64/64 feature tests pass, 0 regressions) |
| 029 | Shared Reference Directory | Reclassify `sdd-workflow` from a (non-invocable) skill into a dedicated shared reference directory (`shared/workflow` → `.specify/shared/workflow`) copied wholesale at init like templates/scripts, retained across re-init, with a `.specify/` path-rewrite rule; remove it from the skills registry/count/symlinks and rewrite ~100 references, with a zero-`sdd-workflow`-reference acceptance gate. | Implemented | .specify/memory/features/029.md | .specify/specs/028-sdd-workflow-refactor/requirements.md | 2026-07-14 (implemented: 10 docs relocated to shared/workflow/; skills 20→19; ~38 source refs + 70 generated command files rewritten; .specify/shared installed & retained; SC-001..006 pass; pytest 104F/643P = 0 new failures vs baseline) |
| 030 | History Command | `/speckit.history` distills the current AI tool's past conversations for the current project into a theme-aggregated knowledge base under `.specify/history/` (decisions, reusable lessons, TODOs, interaction flows, user↔model conflicts — not verbatim). Incremental via a manifest; Claude Code supported today with a pluggable `STORE_RESOLVERS` adapter for other tools. | Implemented | .specify/memory/features/030.md | - | 2026-07-14 (implemented: history-utils.py engine + collect-history.sh + templates/commands/history.md + 4 runtime command mirrors + docs/commands/history.md) |
| 031 | Glossary Mechanism | Single project-wide glossary (`.specify/memory/glossary.md`) anchoring project vocabulary and correcting voice/dictated input (homophones,易混淆词); initialized at instruction generation, ambient to all commands via the Documentation Map, progressively enriched at checkpoints with user-confirmed conflict handling and user-authoritative manual edits. | Implemented | .specify/memory/features/031.md | .specify/specs/029-glossary-mechanism/requirements.md | 2026-07-16 (implemented: glossary-utils.py engine + glossary-template + shared/workflow/glossary.md protocol + generate-instructions init hook + Documentation Map wiring + `## Glossary` step on 4 commands & instructions seeding; 23 tests pass, 0 regressions; SC-006 deferred as post-adoption metric) |

## Feature Entry Format

Each feature entry should follow this format in the table:

| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |
|----|------|-------------|--------|----------------|-----------|--------------|
| NNN | Feature Name | Brief description of the feature | Draft | .specify/memory/features/NNN.md | .specify/specs/NNN-feature-name/requirements.md | 2025-11-21 |

### Column Definitions

| Column | Description |
|--------|-------------|
| ID | Sequential three-digit feature identifier (001, 002, etc.) |
| Name | Short feature name (2-4 words) describing the feature |
| Description | Brief summary of the feature's purpose and scope |
| Status | Current implementation status (Draft, Planned, Implemented, Ready for Review, Completed) |
| Feature Details | Path to feature detail file in .specify/memory/features/[FEATURE_ID].md |
| Spec Path | Path to the latest requirements specification for the feature |
| Last Updated | When the feature entry was last modified (YYYY-MM-DD format) |
