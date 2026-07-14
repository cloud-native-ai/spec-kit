<!--
Sync Impact Report
- Version change: 1.3.0.1 → 1.4.0.1 (MINOR; added Principle IX "Framework Scope Discipline"; expanded Principle VI with root-cause rule and Principle VII with explicit SDD Workflow Gates)
- Modified principles: VI. Continuous Quality & Observability (added root-cause rule); VII. Specification-Plan-Task-Implementation Workflow (added NON-NEGOTIABLE Workflow Gates)
- Added sections: Principle IX — Framework Scope Discipline (No Over-Engineering)
- Removed sections: None
- Templates requiring updates:
  ✅ templates/plan-template.md - No change needed (Constitution Check renders principles dynamically from constitution.md; auto-includes new/expanded principles)
  ✅ templates/tasks-template.md - No change needed (no hard-coded principle numbers)
  ✅ templates/requirements-template.md - No change needed (no principle-number references)
  ⚠ .specify/instructions.md - Documentation Map principle count updated separately (7 → 9)
- Follow-up TODOs: None
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
- Only support officially approved AI agents: Claude Code, Codex CLI, GitHub Copilot, Qwen Code, Hermes Agent, iFlow, opencode, and Qoder
- Tiered support classification: Tier 1 (priority support with deepest integration) — Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode; Tier 2 (standard support) — Qwen Code, Hermes Agent, iFlow
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

**Version**: 1.4.0.1 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-07-14
