# Feature-Centric Specification-Driven Development (F-SDD)

## The Evolution of SDD

While SDD establishes the core principle that **code serves specifications**, Feature-Centric Specification-Driven Development (F-SDD) builds upon this foundation by introducing a crucial new dimension: the **feature**.

### Requirement vs. Feature: Two Sides of the Same Coin

It's essential to understand the relationship between *requirements* and *features*:
*   **Requirements**: These are the external demands or expectations placed on the system. They originate from users, stakeholders, or business goals and answer the question: "What should the system be able to do?"
*   **Features**: These are the internal, realized capabilities of the system. They are the concrete, implemented answers to the requirements and answer the question: "What can the system actually do?"

In essence, **requirements drive the creation and evolution of features, and features are the tangible embodiment of requirements**. F-SDD formalizes this relationship, making features the primary management unit for delivering value.

### The F-SDD Workflow: SDD + Feature as the Organizing Principle

F-SDD is not a replacement for SDD; it is its natural evolution. The core SDD commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, etc.) remain the engine of development. F-SDD adds a lightweight layer of feature-centric semantics on top of this powerful engine.

The workflow introduces just **one new command** to the SDD process:

#### ## 1. `/speckit.feature` (Generating the Feature Index)
*   **Purpose**: Create or update a project-level feature index based on high-level goals or existing context.
*   **Process**: Execute `/speckit.feature`. The AI generates or updates feature entries (including ID, name, brief description) based on product vision, requirement refinement, and other inputs, but subsequent specifications, plans, and tasks still follow the standard SDD process.
*   **Output**: A `features.md` file that records identified features and their basic information; this is the only new command output in F-SDD compared to pure SDD.

### Integrating Features into the SDD Loop

Once the feature index is established, the standard SDD workflow is executed, but now each step is explicitly tied to a specific feature. This creates a clear, traceable lineage from business intent (feature) to technical execution (specification) to working software (code).

The development phase is an SDD cycle with "feature semantics". That is to say:

*   **The SDD Chain Remains**: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement` → `/speckit.checklist`
*   **The Feature Layer is Added**: Every artifact and action is explicitly linked to a feature ID, and the `features.md` file is updated at key points in the process.

This integration happens seamlessly within the existing commands:

1.  **`/speckit.specify` (Specifying by Feature)**  
    - **Behavior**: Starting from user stories or requirements, generate a standard `spec.md` and place it under `.specify/specs/<feature-id>/`; branch naming can also include `<feature-id>` for tracking.  
    - **Feature Integration**: When specifications are created/updated, write metadata such as specification path, key acceptance criteria, etc., to the corresponding feature entry.

2.  **`/speckit.plan` & `/speckit.tasks` (Planning and Tasking by Feature)**  
    - All generated documents (`plan.md`, `data-model.md`, `tasks.md`, etc.) are stamped with the feature ID.
    - Tasks are prefixed with the feature ID for clear scoping.

3.  **`/speckit.analyze` (Feature-Consistency Review)**  
    - Confirms that the tasks fully cover the feature's acceptance criteria.
    - **Updates the feature's status** in `features.md` (e.g., from `Draft` to `Planned`) and logs key risks or open questions.

4.  **`/speckit.implement` (Implementing by Feature)**  
    - Code, tests, and documentation are generated within a feature-branched context.
    - Commit messages and code comments reference the feature ID for full traceability.

5.  **`/speckit.checklist` (Final Gate + Feature Status Update)**  
    - Performs all standard SDD quality checks (consistency, static analysis, security scans, tests).
    - **Updates the `features.md` entry** to reflect the final state (e.g., `Implemented` or `Ready for Review`) and can link to test reports.

Through this approach, F-SDD provides a powerful framework for managing scope, ensuring traceability, and aligning technical work with business value—all without introducing any new "implementation" commands. The feature is simply a semantic label that threads through the entire, proven SDD process.

*   `/speckit.feature`: Manages the "what" and the current state of features.
*   SDD Commands: Handle the "how" of specifying, planning, and implementing each feature.
*   `/speckit.analyze` & `/speckit.checklist`: Act as the synchronization points, ensuring the `features.md` index always reflects the true state of the system.

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

The F-SDD workflow reuses SDD commands and artifacts as much as possible, adding only one `/speckit.feature` command at the entry level to maintain the feature index; all other feature tracking, status updates, and validation are handled through existing commands.

### # Preparation Phase

This phase establishes the project's foundational rules and creates an initial map of its potential capabilities.

#### ## 1. `/speckit.constitution` (Establishing the Project Constitution)
*   **Purpose**: Define the immutable architectural and quality principles that will govern all future development.
*   **Process**: Execute the `/speckit.constitution` command. An AI agent analyzes the project type and organizational best practices to generate a `constitution.md`.
*   **Output**: A `constitution.md` file containing non-negotiable rules like "Library-First Principle," "Test-First Imperative," and "Simplicity Gates." This acts as the system's DNA, ensuring consistency across all features.

#### ## 2. `/speckit.feature` (Generating the Feature Index)
*   **Purpose**: Create or update a project-level feature index based on high-level goals or existing context.
*   **Process**: Execute `/speckit.feature`. The AI generates or updates feature entries (including ID, name, brief description) based on product vision, requirement refinement, and other inputs, but subsequent specifications, plans, and tasks still follow the standard SDD process.
*   **Output**: A `features.md` file that records identified features and their basic information; this is the only new command output in F-SDD compared to pure SDD.

### # Development Phase

This phase is essentially an SDD cycle with "feature semantics". That is to say:

*   Still use the SDD main chain: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement` → `/speckit.checklist`;
*   The only requirement is to explicitly carry the feature ID at each step and update `features.md` at appropriate stages.

The entire development phase can be understood as the following lightweight "overlay":

1. **`/speckit.specify` (Creating specifications by feature)**  
    - **Behavior**: Starting from user stories or requirements, generate a standard `spec.md` and place it under `.specify/specs/<feature-id>/`; branch naming can also include `<feature-id>` for tracking.  
    - **Feature Integration**: When specifications are created/updated, write metadata such as specification path, key acceptance criteria, etc., to the corresponding feature entry, but no new commands are needed.

2. **`/speckit.plan` (Generating implementation plans by feature)**  
    - **Behavior**: Generate documents such as `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, etc., based on `spec.md` and `constitution.md`, which completely follows the existing SDD behavior.  
    - **Feature Integration**: All generated documents note the feature ID in the title or metadata, making it convenient to reference and navigate in `features.md` later.

3. **`/speckit.tasks` (Deriving tasks by feature)**  
    - **Behavior**: Derive `tasks.md` from `plan.md` and related documents, still following SDD's conventions for task granularity and parallel markers (`[P]`).  
    - **Feature Integration**: Include the feature ID in task titles or tags, so that task execution and traceability naturally align with a specific feature.

4. **`/speckit.analyze` (Consistency review of tasks and features)**  
    - **Behavior**: Humans and AI together check whether `tasks.md` and `plan.md` cover all acceptance criteria of `spec.md`, this is the existing "task confirmation" step in SDD.  
    - **Feature Integration**: In this step, the feature's status can be updated from something like "Draft/Proposed" to "Planned/Ready", and key risks, open questions can be written back to `features.md`, without needing additional feature commands.

5. **`/speckit.implement` (Executing tasks by feature)**  
    - **Behavior**: Task Agent or developers execute according to `tasks.md`, implementing code, tests, and documentation updates.  
    - **Feature Integration**: As long as branch naming, directory structure, and commit messages continuously carry the feature ID, you can directly reach the specific implementation from `features.md`.

6. **`/speckit.checklist` (Final quality gate + feature status update)**  
    - **Behavior**: Execute existing checklist logic: consistency checks, static analysis, security scans, test runs, etc.  
    - **Feature Integration**: In the same command, update the status of the corresponding feature in `features.md` based on check results (e.g., `Planned` → `Implemented` or `Ready for Review`), and can append links to test reports, known limitations, etc.

Through this approach, F-SDD does not introduce new "implementation class" commands, but treats features as a semantic label that runs through the entire SDD process:

*   `/speckit.feature`: Responsible for "what features exist" and their current approximate status;
*   SDD commands: Responsible for "how this feature is being specified, planned, decomposed, and implemented";
*   `/speckit.analyze` and `/speckit.checklist`: On top of their original responsibilities, they also maintain feature status and metadata, making `features.md` the true single entry point for feature views.

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

These articles are enforced automatically by the `/speckit.generate_plan` command, transforming AI from a code generator into an architectural partner.

## The Transformation

F-SDD is not about replacing developers. It's about amplifying human capability by automating the mechanical translation from feature intent to implementation. By centering the SDD workflow on **features**, we provide a powerful framework for managing scope, ensuring traceability, and aligning technical work with business value. This creates a tight feedback loop where features, specifications, research, and code evolve together, bringing deeper understanding and better alignment between intent and implementation.