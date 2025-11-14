好的，已收到您的指令。我将严格以您提供的原始文档（`spec-driven.md`）为基础，并参考您给出的 `F-SDD` 流程设计，对生成的 **Feature-Centric Specification-Driven Development (F-SDD)** 文档进行内容校验和补充。

我的目标是：
1.  **保持风格一致**：确保新文档的语言、结构和术语与 `spec-driven.md` 完全一致。
2.  **内容校验**：检查现有 F-SDD 文档中是否有与 `spec-driven.md` 内容相悖或不一致的地方。
3.  **精准补充**：将您设计的详细流程步骤无缝、自然地融入原文，使其看起来像是原作者撰写的扩展内容。

---

# Feature-Centric Specification-Driven Development (F-SDD)

## The Power Inversion, Centered on Features

For decades, code has been king. Specifications served code—they were the scaffolding we built and then discarded once the "real work" of coding began. We wrote PRDs to guide development, created design docs to inform implementation, drew diagrams to visualize architecture. But these were always subordinate to the code itself. Code was truth.

Feature-Centric Specification-Driven Development (F-SDD) inverts this power structure **and places the feature at its heart**. It asserts that:
1.  **Specifications don't serve code—code serves specifications.**
2.  **Features are not just a list; they are the primary management unit for value delivery.**

In F-SDD, the Product Requirements Document (PRD) isn't a guide for implementation; it's the source that generates implementation. More importantly, every specification is intrinsically linked to a well-defined **feature**. This isn't an incremental improvement to how we build software. It's a fundamental rethinking of what drives development: **a clear, traceable lineage from business intent (feature) to technical execution (specification) to working software (code)**.

The gap between business value and technical implementation has plagued software development since its inception. F-SDD eliminates this gap by making features and their specifications executable. When a feature's specification generates code, there is no gap—only transformation.

This transformation is now possible because AI can understand complex user needs, define precise features, implement detailed specifications, and create comprehensive implementation plans. But raw AI generation without structure produces chaos. F-SDD provides that structure through **features as the organizational anchor** and **executable specifications** derived from them. The specification becomes the primary artifact. Code becomes its expression (as an implementation from the implementation plan) in a particular language and framework.

In this new world, maintaining software means evolving specifications, which are managed within the context of their parent features. The entire development workflow reorganizes around **features and their specifications** as the central source of truth, with implementation plans and code as the continuously regenerated output. This process is therefore a 0 -> 1, (1', ..), 2, 3, N, where each iteration is tied to a specific feature.

## The F-SDD Workflow in Practice

The F-SDD workflow begins with a high-level idea or a collection of user stories. It immediately structures this chaos into a manageable form by focusing on features first, then detailing them with specifications.

### # Preparation Phase

This phase establishes the project's foundational rules and creates an initial map of its potential capabilities.

#### ## 1. `/constitution` (Establishing the Project Constitution)
*   **Purpose**: Define the immutable architectural and quality principles that will govern all future development.
*   **Process**: Execute the `/constitution` command. An AI agent analyzes the project type and organizational best practices to generate a `constitution.md`.
*   **Output**: A `constitution.md` file containing non-negotiable rules like "Library-First Principle," "Test-First Imperative," and "Simplicity Gates." This acts as the system's DNA, ensuring consistency across all features.

#### ## 2. `/features` (Generating the Initial Feature List)
*   **Purpose**: Create a structured inventory of the project's core capabilities based on high-level goals or existing context.
*   **Process**: Execute the `/features` command. An AI agent scans any available input (e.g., product vision, initial requirements) and proposes a preliminary set of features.
*   **Output**: A `features.md` file listing all identified features with IDs, names, and brief descriptions. This document serves as the master index for all development work.

### # Development Phase

This phase is a repeatable cycle for delivering individual features. Each feature progresses through a series of AI-assisted commands.

#### ## 3. `/specify` (Creating the Feature Specification)
*   **Purpose**: Transform a user story or requirement into a complete, structured specification for a single feature.
*   **Process**: Execute the `/new_feature` command with a feature description. The AI creates a dedicated branch and populates it with a `feature-spec.md` template.
*   **Output**: A `feature-spec.md` file in a feature-specific directory (e.g., `specs/001-user-login/feature-spec.md`) containing user stories, acceptance criteria, and `[NEEDS CLARIFICATION]` markers for ambiguities.

#### ## 4. `/clarify` (Refining the Spec and Linking to Feature)
*   **Purpose**: Resolve ambiguities in the specification and formally link it to the master feature list.
*   **Process**: The team reviews the `feature-spec.md`, answers clarification questions, and removes `[NEEDS CLARIFICATION]` markers. Upon approval, the corresponding entry in `features.md` is updated to reference this `feature-spec.md` and its status is changed (e.g., from "Proposed" to "Specified").
*   **Output**: A finalized `feature-spec.md` and an updated `features.md` with bidirectional links, establishing full traceability.

#### ## 5. `/plan` (Generating the Implementation Plan)
*   **Purpose**: Translate the approved specification into a concrete, actionable technical blueprint.
*   **Process**: Execute the `/generate_plan` command. The AI reads the `feature-spec.md`, consults the `constitution.md`, and generates an `implementation-plan.md`.
*   **Output**: An `implementation-plan.md` file containing technology choices with rationale, data models, API contracts (`contracts/`), research findings (`research.md`), and a quickstart validation guide. This plan enforces constitutional gates (e.g., Simplicity Gate).

#### ## 6. `/tasks` (Deriving Executable Tasks)
*   **Purpose**: Break down the implementation plan into a granular, executable task list.
*   **Process**: The AI analyzes the `implementation-plan.md`, `data-model.md`, and `contracts/` to derive specific actions. *(Note: As per the original document, this step is implied in the `/generate_plan` command's output of detailed documents, but not a separate command. We treat the creation of `tasks.md` as part of the plan's derivation.)*
*   **Output**: A `tasks.md` file (or equivalent task list within the plan) listing atomic tasks, marking independent ones `[P]` for parallelization, ready for a Task Agent to execute.

#### ## 7. `/analyze` (Task Confirmation)
*   **Purpose**: Ensure the generated task list is correct, complete, and aligned with the specification before execution.
*   **Process**: A human developer reviews the `tasks.md` and `implementation-plan.md`, verifies its alignment with the `feature-spec.md`, and approves it for execution.
*   **Output**: A confirmed task list, signaling the start of automated implementation.

#### ## 8. `/implement` (AI-Assisted Development)
*   **Purpose**: Generate code, tests, and other artifacts by executing the approved tasks.
*   **Process**: A Task Agent processes the `tasks.md`, generating code one task at a time. All changes are made in the feature branch.
*   **Output**: Code commits that implement the feature according to the spec and plan.

#### ## 9. `/checklist` (Final Verification and Feature Update)
*   **Purpose**: Perform a final quality check and update the feature's status in the master list.
*   **Process**: Run the `/checklist` command. An AI agent performs consistency checks, SAST scanning, and ensures all tests pass. The human team performs final validation. Once passed, the `features.md` is updated to mark the feature as "Implemented" or "Ready for Review."
*   **Output**: Verified code, test reports, and an updated `features.md` reflecting the latest state of the project.

## Why F-SDD Matters Now

F-SDD combines the necessity of SDD with the practicality of feature-based project management.

1.  **AI Amplifies Human Intent**: AI automates the mechanical translation from natural language requirements to executable specifications and tasks, freeing developers for critical thinking and creativity.
2.  **Complexity Demands Structure**: Modern systems are too complex for ad-hoc development. F-SDD provides a systematic, feature-by-feature approach to maintain alignment.
3.  **Velocity Requires Traceability**: Rapid iteration is impossible if you lose track of what each piece of code is supposed to do. F-SDD's feature-spec-code lineage enables safe, fast pivots. Change a requirement in a `spec.md`, regenerate the plan and tasks, and the implementation follows.

When specifications and features drive implementation, pivots become systematic regenerations rather than manual rewrites. This isn't just about initial development—it's about maintaining engineering velocity through inevitable changes.

## Core Principles of F-SDD

Our methodology is built on seven foundational principles:

**1. Features as the Management Unit**: Features are the primary vehicle for planning, tracking, and delivering value. All work is organized around them.

**2. Specifications as the Lingua Franca**: The specification is the primary artifact. Code is merely its expression in a specific language. Maintaining software means evolving specifications within their feature context.

**3. Executable Specifications & Plans**: Specifications and implementation plans must be precise, complete, and unambiguous enough to generate working systems. This eliminates the gap between intent and implementation.

**4. Continuous Refinement**: Consistency validation happens continuously. AI analyzes specifications for ambiguity, contradictions, and gaps as an ongoing process.

**5. Research-Driven Context**: Research agents gather critical context throughout the specification process, investigating technical options, performance implications, and organizational constraints.

**6. Bidirectional Feedback**: Production reality informs specification evolution. Metrics, incidents, and operational learnings become inputs for specification refinement.

**7. Feature Branching for Exploration**: Use branching to generate multiple implementation approaches for the same feature specification to explore different optimization targets—performance, maintainability, user experience, cost.

## The Constitutional Foundation

At the heart of F-SDD lies the `constitution.md`, a set of immutable principles that ensure architectural integrity across all features.

### Key Articles
*   **Article I: Library-First Principle**: Every feature starts as a standalone library, enforcing modularity.
*   **Article II: CLI Interface Mandate**: Ensures observability and testability.
*   **Article III: Test-First Imperative**: No code before failing tests are written and approved.
*   **Articles VII & VIII: Simplicity and Anti-Abstraction**: Combat over-engineering with explicit gates in the `plan.md`.
*   **Article IX: Integration-First Testing**: Prioritize real environments over mocks.

These articles are enforced automatically by the `/generate_plan` command, transforming AI from a code generator into an architectural partner.

## The Transformation

F-SDD is not about replacing developers. It's about amplifying human capability by automating the mechanical translation from feature intent to implementation. By centering the SDD workflow on **features**, we provide a powerful framework for managing scope, ensuring traceability, and aligning technical work with business value. This creates a tight feedback loop where features, specifications, research, and code evolve together, bringing deeper understanding and better alignment between intent and implementation.