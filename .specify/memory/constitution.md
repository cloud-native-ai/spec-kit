<!--
Sync Impact Report
- Version change: 1.9.1 → 1.10.0 (MINOR; Principle XI materially extended — term definition anchored + two normative rules added from user-directed concept work under Dogfooding, 2026-08-14)
- Modified principles: XI. Dogfooding (Self-Application) — (a) intro now anchors the TERM's canonical definition at shared/definitions/dogfooding-definitions.md § 0 (using the tool/framework to develop itself; compiler self-hosting analogy; every mention of "Dogfooding" carries that definition by reference); (b) added "Fix the mechanism, not just the instance (修复落机制侧)" (repairs of mechanism-produced artifacts MUST land mechanism-side; instance patches only as logged temporary stabilization); (c) added "Two hats: framework sources vs client runtime (两顶帽子)" (fixes intended for all consuming projects MUST land in framework sources and ride publish→install→init; direct `.specify/` runtime edits are client-side instance fixes)
- Added sections: None (new concept authority lives outside the constitution at shared/definitions/dogfooding-definitions.md, mirrored to .specify/shared/definitions/)
- Removed sections: None
- Templates requiring updates:
  ✅ shared/definitions/dogfooding-definitions.md — NEW concept authority (§0 Dogfooding 本体定义 with self-hosting analogy + 语义束表; §1 problem/mechanism + fix classification; §2 client/framework + three-copy topology + two-hats rule; §3 glossary anchors)
  ✅ .specify/memory/glossary.md — five entries registered (Dogfooding / 问题修复 / 机制修复 / 框架项目 / 客户项目, origin=user, status=confirmed)
  ✅ scripts/bash/generate-instructions.sh (+mirror) — the MECHANISM fix executed 2026-08-15 under the new rule: additive section reconcile (template sections missing from the live file are injected verbatim, in template order; existing sections never touched; idempotent). Running it healed the live file — ## Dogfooding Practice AND ## Spec Kit Framework Map (a second, previously undetected casualty of the same gap) now present; AGENTS.md inherits via symlink
  ✅ tests/contract/test_instructions_section_propagation.py — guarding contract: C-1 live managed-section set ⊇ template section set (real-tree); C-2 generator injects additively + idempotently (fixture)
- Follow-up TODOs: test_c4_no_new_memory_layout remains a pre-existing baseline failure (stale pin over evidence/todo/tools dirs, unrelated to XI). Environment note: live .specify/instructions.md was root-owned (container leftover) blocking the mechanism; ownership restored via same-content rename (parent dir writable), then reconcile ran
- Preserved by design: historical specs/feedback keep their original wording as dated records.

Previous change (1.9.0 → 1.9.1, PATCH): non-semantic reconciliation of Principle V's approved-agent roster with shipped code — Qwen Code and iFlow removed from AGENT_CONFIG in 0c300bc8. Follow-ups resolved: update-agent-context.sh / setup-plan.sh deleted as orphan upstream leftovers (now gated by sync-mirrors --check ORPHAN detection via test_scripts_distribution_parity.py). Remaining unrelated observation: .specify/skills/draw-echarts/yuque-workspace/ nested-skill placement issue.
-->

# Spec Kit Constitution

## Core Principles

### I. Specification-Driven Development (SDD) as Foundation
Specifications are the primary source of truth and MUST drive all implementation:
- Code serves specifications, not the other way around
- Specifications MUST be executable and generate working systems
- Every technical decision MUST trace back to specific requirements in the specification
- Specifications MUST evolve continuously based on feedback, operational reality, and changing requirements

Rationale: Eliminates the gap between specification and implementation, ensuring systematic alignment and maintainable software.

### II. Feature-Centric Development
Features are the long-term backbone of the project:
- The Feature Index MUST serve as the single source of truth for all project capabilities
- Every spec → plan → tasks → implement step MUST re-evaluate Feature additions, removals, merges, or splits
- Feature changes MUST be traceable to corresponding spec/plan evidence and recorded in Feature details
- Features MUST be versioned and their evolution tracked systematically

Rationale: Ensures project evolution remains focused on delivering value through well-defined, trackable features.

### III. Intent-Driven Development
Development intent MUST be expressed clearly in natural language and design artifacts:
- Focus on the "what" and "why" before the "how"
- Use rich specifications with guardrails and organizational principles
- Multi-step refinement is preferred over one-shot code generation
- Critical thinking and creativity are amplified through structured processes

Rationale: Enables higher-level collaboration and ensures implementations align with business and user needs.

### IV. Test-First & Contract-Driven Implementation
Implementation MUST follow rigorous quality standards:
- Write or update tests BEFORE implementing new behavior (Red-Green-Refactor)
- Pure functions/utilities MUST have unit tests
- Critical flows MUST have automated regression coverage
- Integration/contract tests MUST cover cross-service communication and external APIs
- Acceptance scenarios from specifications become automated tests

Rationale: Reduces regressions, clarifies intent, and validates real-world behavior beyond unit tests.

### V. AI Agent Integration Standards
AI agent integration MUST follow strict guidelines:
- Only support officially approved AI agents: Claude Code, Codex CLI, GitHub Copilot, Hermes Agent, opencode, and Qoder
- Tiered support classification: Tier 1 (priority support with deepest integration) — Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode; Tier 2 (standard support) — Hermes Agent
- Configuration parsing MUST reject unsupported providers
- Agent capabilities MUST be leveraged for specification interpretation and implementation generation
- Heavy reliance on advanced AI model capabilities for specification understanding is expected

Rationale: Ensures consistent, secure, and maintainable AI integration while focusing on target tools.

### VI. Continuous Quality & Observability
All components MUST be observable, versioned, and maintainable:
- Use structured logs for important events and errors
- Prefer semantic versioning (MAJOR.MINOR.PATCH) for all components
- Document breaking changes and migration notes
- Keep designs as simple as possible; avoid speculative features (YAGNI)
- Linting, formatting, and basic tests MUST pass in CI
- New behavior MUST be reflected in specs/plan/tasks/docs where applicable
- Root-cause over "good enough": when results fall short of the stated bar, locate and fix the root cause rather than settling near the threshold

Rationale: Makes systems debuggable, upgradable, maintainable, and ensures consistent quality.

### VII. Specification-Plan-Task-Implementation Workflow
The SDD workflow MUST be followed rigorously:
- **Specification Phase**: Define comprehensive requirements, acceptance criteria, and constraints
- **Planning Phase**: Map requirements to technical decisions with documented rationale
- **Task Breakdown Phase**: Create actionable, atomic tasks from implementation plans
- **Implementation Phase**: Execute tasks according to plans, generating code from specifications
- Each phase MUST validate against the Feature Index and update it as needed
- **Workflow Gates (NON-NEGOTIABLE)**:
  - **Feature reuse-first**: bind evolution/refactor specs to an existing Feature (many-specs-to-one-feature); create a new Feature only when none fits
  - **No status regression**: appending an evolution spec to an `Implemented` Feature keeps it Implemented; never revert to Planned
  - **Pre-Status-Flip Gate** (Planned→Implemented): requires zero open `[ ]` tasks AND a status line for every Success Criterion in `verification.log`
  - **Deferred tasks are first-class**: work that cannot run this session is marked `[~]` with `<!-- deferred: reason -->`, never left as `[ ]`
  - **Template-only features**: features with no executable runtime code judge Test-First as Partial (justified) — "tests" verify template content, canonical paths, and structure instead

Rationale: Provides systematic structure for transforming specifications into working systems while maintaining traceability.

### VIII. Code as the Single Source of Truth
Source code is the authoritative record of the system's ACTUAL state:
- Source code MUST be treated as the single source of truth for how the system currently behaves; documentation, specifications, and plans express INTENDED or TARGET behavior that may not yet be realized
- When establishing or citing facts about current behavior, code MUST take precedence over documentation, UNLESS a document is explicitly designated as authoritative for that fact
- When code and documentation disagree, the divergence MUST be treated as a signal to update the documentation (or to flag the code as not yet implementing the intended goal) — never as license to trust the document as current reality
- Fact-checking, analysis, and troubleshooting MUST verify claims against the code first, then reconcile documentation

Rationale: Specifications and docs describe where the project is going; code describes where it actually is. Trusting docs as current reality propagates drift and errors. This principle complements Principle I (specs drive what SHOULD be built) by fixing code as the record of what IS.

### IX. Framework Scope Discipline (No Over-Engineering)
Spec Kit is a documentation/prompt framework, NOT a runtime platform or agent execution engine:
- Every "adopt / sync / add" decision MUST be measured against this scope; features that assume a multi-agent runtime, workflow execution engine, or remote-download platform are OUT of scope unless explicitly justified
- Supervisor / orchestration constructs are PROMPT INSTRUCTIONS interpreted by an AI agent, never runtime schedulers
- Upstream changes, security fixes, and dependencies are adopted only when they fit this scope — a fix for functionality this project does not use (e.g. remote catalog download) is NOT applicable
- Prefer the simplest artifact (template / prompt / doc) that satisfies the need; reject speculative infrastructure (YAGNI applied at the architectural level)

Rationale: The single most-reused decision standard across the project's history. Assuming an upstream "runtime platform" trajectory or over-building infrastructure repeatedly wasted effort; anchoring to "framework, not runtime" keeps scope honest.

### X. Documentation Naming & Location Conventions
Markdown documents MUST follow naming and location conventions so that names and paths carry meaning:
- **Reserved Filenames (保留文件名) — strict blocking**: analogous to reserved keywords in a programming language, ALL-CAPS document names are **reserved identifiers**. Each reserved name is defined in a registry entry carrying its **fixed semantics AND registered location**, and may appear ONLY at that location with that meaning. Currently registered (location: project root): `README.md` (root entry indexing all of `docs/`), `ARCHITECTURE.md` (one-page summary of concepts + decisions), `CONTRIBUTING.md` (contribution entry), `CHANGELOG.md` (self-contained timeline). User documents MUST NOT use a reserved name; a document with similar semantics elsewhere MUST use a lowercase alternative — directory indexes use `index.md`, never a nested `README.md`. The registry is extensible: registering a new reserved name requires recording both its semantics and its location. Scope: the managed documentation space (project root + `docs/`); enforcement is a deterministic check of `/speckit.docs`
- **Path is semantic**: a document's meaning derives from its full path, not its filename alone — `docs/team/overview.md` is the overview of the *team* concept. Place documents so `<area>/<topic>.md` reads as "the `<topic>` of `<area>`", and reuse generic lowercase filenames (`overview.md`, `design.md`, `index.md`) scoped by their directory rather than inventing globally-unique names
- **Tool/framework-mandated names are non-negotiable**: files whose names are dictated by an external tool or framework are exempt from the reserved-name blocking and MUST match that exact pattern and location — e.g. GitHub Copilot commands MUST be `.github/prompts/<name>.prompt.md`; tool instruction aliases (`CLAUDE.md`, `QODER.md`, `AGENTS.md`, …), `LICENSE`, and `skills/*/SKILL.md` keep their mandated names and MUST NOT be renamed or "normalized" to project conventions

Rationale: Consistent, path-aware naming keeps documents discoverable and preserves the meaning encoded in a document's location. Treating ALL-CAPS names as strictly reserved identifiers (name = semantics contract) prevents silent semantic collisions — a `README.md` buried in a subdirectory would falsely claim root-entry semantics; `index.md` says exactly what it is.

### XI. Dogfooding (Self-Application)
The framework's developers and users are tightly linked — often the same team — which enables smooth use→feedback→iterate loops. Spec Kit MUST practice Dogfooding through its existing loop mechanisms, never through new parallel machinery. **Term definition**: "Dogfooding" is defined canonically in `shared/definitions/dogfooding-definitions.md` § 0 (using the tool/framework to develop the tool/framework itself — the compiler self-hosting analogy); every mention of the word in project documents carries that definition by reference:
- **Self-application (bootstrap discipline)**: Spec Kit's own feature evolution MUST go through its own SDD workflow (spec → plan → tasks → implement). Like a compiler achieving self-hosting or an operating system bootstrapping itself, a project that provides development-assistance capabilities proves them by developing itself with them first — only a tool that performs well in its own engineering has earned the credibility to assist other projects
- **Deviation logging**: when a change legitimately bypasses the self-application workflow (e.g. an emergency fix), the deviation and its reason MUST be logged in the affected spec directory (`.specify/specs/<key>/`) or in `.specify/memory/` governance documents — never silently
- **Fix the mechanism, not just the instance (修复落机制侧)**: a defect observed in an artifact that a mechanism (template, generation/refresh command, reconcile flow, guarding contract) repeatedly produces is an *instance*; hand-patching the artifact is a Problem Fix that never propagates. Before repairing any non-one-off artifact, the agent MUST identify the producing mechanism and land the fix there (Mechanism Fix), so the next execution of the corresponding command carries it into this repo's live files and every downstream project naturally. An instance-side patch is permitted ONLY as temporary stabilization while the mechanism fix is pending, and MUST be logged with the pending mechanism-side follow-up. Concept authority: `shared/definitions/dogfooding-definitions.md` § 1
- **Two hats: framework sources vs client runtime (两顶帽子)**: this repository is simultaneously the framework's source (`skills/`, `templates/`, `scripts/`, `shared/`, `src/specify_cli/`) and one of its own client projects (`.specify/`, installed via the same init/refresh flow every downstream project uses). Direct edits to this repo's `.specify/` runtime copies are client-side instance fixes — they never reach other client projects. A fix intended for ALL consuming projects MUST land in the framework sources and ride the publish → install → `specify init` flow; before any edit the agent MUST name which hat it is wearing. Concept authority: `shared/definitions/dogfooding-definitions.md` § 2
- **Loop A (framework-level, existing)**: every project using Spec Kit helps improve Spec Kit via the existing feedback chain (record → threshold prompt → package → manual submission to the install-source repo); this path is identified and surfaced, not rebuilt
- **Loop B (project-level, existing capabilities)**: downstream projects reuse the framework's shipped capabilities (feedback engine, memory, history, review, task records) to build the same use→feedback→iterate loop for their own product
- **Advisory only**: toward downstream projects Dogfooding is an advisory principle delivered as guidance; adoption MUST NOT be enforced through blocking gates, and this principle MUST NOT justify adding new recording, statistics, or reminder systems (see Principle IX)

Rationale: Dogfooding's essence is replacing hypothetical design with real working scenarios. The loops already exist in the framework; naming them in governance keeps the framework honest (it must eat its own dog food to ship) while keeping scope disciplined (identification over invention).

### XII. Tool Reuse Over Ad-Hoc Generation
A **Tool** is a named, pre-verified, reusable definition of one concrete capability (`.specify/memory/tools/<name>.md`) — an abstraction layer between an agent's intent and the environment's reality, defined canonically in `.specify/shared/definitions/tool-definitions.md`. Tools exist because the unmediated alternative fails in two ways: the same logical capability differs by command name, version, version-specific flags, CPU architecture, and OS; and for anything non-trivial an LLM otherwise writes throwaway script code that varies in quality and correctness **between runs**.
- **Reuse before generating**: before generating script code to perform a complex or repeatable action, an agent MUST look for an existing Tool and reuse it when one covers the capability. Where no Tool exists, writing the code is the expected outcome — and a capability worth repeating SHOULD be offered for promotion to a Tool
- **Records outrank model knowledge**: when a Tool record exists, its `## Behavioral Rules` are authoritative; where the record and the model's training knowledge disagree, the record wins
- **Verified, not assumed**: a record MUST NOT claim a version, platform, or CPU architecture it was not verified against. Environment applicability states what was observed and leaves the rest unstated; a `Draft` record is incomplete by definition and MUST NOT be invoked
- **Cheap by construction**: the gate is a lookup plus a decision — it MUST NOT block work, MUST NOT apply to ordinary one-off reads/greps/single obvious commands, and MUST NOT justify new tracking or enforcement machinery (see Principle IX). Its operational form is the existing convention `.specify/shared/workflow/tool-reuse-gate.md`

Rationale: reproducibility and cost both degrade when every run re-improvises how to do the same thing. Pinning a verified invocation once buys stability (identical behavior across runs, sessions, and agents) and efficiency (no re-deriving or re-validating the invocation, so less inference overhead) — while keeping the mechanism to a lookup rather than a new subsystem.

### XIII. Better-Harness Orientation (Improvement North Star)
All of Spec Kit's improvement mechanisms serve one explicit, shared goal: making every project a **better harness** for agent work — an environment in which an AI agent can understand the task, execute on supported and repeatable paths, validate its changes, deliver safely, and carry lessons forward:
- The goal model — the feedforward/feedback loop and the five Agent Work Loop dimensions (Task Understanding, Controlled Execution, Change Validation, Reliable Delivery, Learning Capture) with their mapping to Spec Kit mechanisms — is defined once in `.specify/shared/guidelines/better-harness.md`; improvement units MUST reference that anchor, never fork or restate it
- The feedback mechanism (Loop A/B carrier), the evidence layer, and the create-*/improve-* skill families are instruments of this goal; when motivating or prioritizing an improvement, units SHOULD name the dimension it strengthens instead of inventing ad-hoc categories
- Evidence discipline governs every improvement claim: a configured asset proves at most that a mechanism exists (configured ≠ used); `Unobserved` evidence MUST NOT be treated as a defect or a conclusion; "improved" MUST only be claimed from comparable before/after evidence
- This principle adds orientation, not machinery: it MUST NOT be used to justify new scoring systems, maturity reports, recording engines, or runtime evaluation platforms (Principle IX), and it does not alter the feedback red lines (framework-only target, user-data optionality, zero automated transmission)

Rationale: The feedback mechanism and the improve-* skills each carried their own discipline but no named common goal. Naming the goal — adapted from the open-source Better Harness model, whose evidence-state vocabulary the evidence layer already uses — lets every flow answer "which part of the harness does this strengthen?" and keeps improvement work evidence-honest.

## Spec-Driven Development Workflow

### Research & Context Gathering
- Research agents MUST gather critical context during specification creation
- Investigate library compatibility, performance benchmarks, and security implications
- Organizational constraints MUST be discovered and applied automatically
- Company standards (database, authentication, deployment policies) integrate seamlessly into specifications

### Specification Evolution
- Specifications evolve continuously through iterative dialogue with AI
- AI asks clarifying questions, identifies edge cases, and defines precise acceptance criteria
- Domain concepts become data models, user stories become API endpoints
- Production metrics and incidents update specifications for next regeneration

### Implementation Plan Generation
- Implementation plans map requirements to technical decisions
- Every technology choice has documented rationale
- Every architectural decision traces back to specific requirements
- Consistency validation continuously improves quality throughout the process

## Feature Governance

### Feature Lifecycle Management
- **Draft**: Feature defined, spec in progress
- **Planned**: Spec approved, implementation scheduled  
- **Implemented**: Code changes merged to feature branch
- **Ready for Review**: PR open, tests passing
- **Completed**: Merged to main, deployed

### Feature Documentation Requirements
- Each Feature MUST have a detailed Feature Detail document
- Feature Detail MUST include Overview, Key Changes, Implementation Notes, and Related Files
- Feature Index MUST be updated with status changes and last updated timestamps
- Total Features count MUST be maintained accurately

## Governance

This Constitution supersedes all other guidelines and documentation. All development activities MUST comply with these principles.

**Amendment Procedure**: 
- Amendments require formal proposal, team review, and version bump
- Major changes (backwards incompatible) require MAJOR version increment
- New principles or materially expanded guidance require MINOR version increment  
- Clarifications, wording fixes, and non-semantic refinements require PATCH version increment

**Compliance Review**: 
- All pull requests MUST check compliance with core principles
- Feature changes MUST be validated against the Feature Index
- Specification quality MUST be verified before implementation begins

**Version**: 1.9.1 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-08-08
