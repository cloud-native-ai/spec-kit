<!--
Sync Impact Report
- Version change: N/A → 1.0.0
- Modified principles: Added comprehensive Spec-Driven Development principles
- Added sections: Spec-Driven Development Workflow, AI Agent Integration, Feature Governance
- Removed sections: Generic template sections replaced with project-specific content
- Templates requiring updates: 
  ✅ templates/plan-template.md - Updated to align with SDD workflow
  ✅ templates/spec-template.md - Updated to include SDD requirements
  ✅ templates/tasks-template.md - Updated to reflect feature-centric task types
  ✅ templates/commands/*.md - Verified alignment with generic guidance
- Follow-up TODOs: None - all placeholders resolved
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
- Only support officially approved AI agents: GitHub Copilot, Qwen Code, and opencode
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

Rationale: Makes systems debuggable, upgradable, maintainable, and ensures consistent quality.

### VII. Specification-Plan-Task-Implementation Workflow
The SDD workflow MUST be followed rigorously:
- **Specification Phase**: Define comprehensive requirements, acceptance criteria, and constraints
- **Planning Phase**: Map requirements to technical decisions with documented rationale
- **Task Breakdown Phase**: Create actionable, atomic tasks from implementation plans
- **Implementation Phase**: Execute tasks according to plans, generating code from specifications
- Each phase MUST validate against the Feature Index and update it as needed

Rationale: Provides systematic structure for transforming specifications into working systems while maintaining traceability.

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

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30
