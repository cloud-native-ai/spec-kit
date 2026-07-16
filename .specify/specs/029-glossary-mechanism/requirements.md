# Requirements Specification: Project Glossary Mechanism (项目词汇表机制)

**Requirement Branch**: `029-glossary-mechanism`  
**Created**: 2026-07-16  
**Status**: Draft  
**Input**: User description: "需要在这个框架中引入词汇表机制：1. 在生成 instruction 时初始化词汇表 2. 随项目开发进程逐步完善词汇表 3. 对词汇表中存在或可能出现的冲突词汇进行提示，由用户确认。核心目的是支持语音输入，校正用户输入中因同音词或易混淆词导致的错误，对项目文档或高频描述进行锚定，词汇表本身也定义了一系列领域知识。原则：1. 常用词汇无需记录 2. 支持用户手动更新，以用户输入为准"

## Related Feature *(mandatory)*

**Feature ID**: 031  
**Feature Name**: Glossary Mechanism

<!-- New feature — not yet in .specify/memory/features.md; register via /speckit.feature before /speckit.plan wrap-up. -->

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initialize the glossary during instruction generation (Priority: P1)

When a project author runs the instruction-generation step, the framework seeds a project glossary with the domain-specific and project-specific terms it can already observe (existing docs, constitution, feature names, high-frequency descriptions). Common everyday words are deliberately excluded. The author ends up with a starter list of canonical terms that anchors how the project's vocabulary is understood from that point on.

**Why this priority**: The glossary must exist before it can correct anything. Seeding it at instruction time is the single change that unlocks every downstream benefit (voice correction, anchoring, domain knowledge), so it is the minimum viable slice.

**Independent Test**: Run instruction generation on a project that has existing docs containing project-specific terms; confirm a glossary artifact is created containing those domain terms (with canonical form + short meaning) and that common words are absent. Delivers value on its own as a reviewable domain-term list.

**Acceptance Scenarios**:

1. **Given** a project with documentation containing project-specific terms, **When** the author generates the project instructions, **Then** a glossary artifact is created and populated with observed domain/project terms, each carrying a canonical form and a brief meaning.
2. **Given** the same generation run, **When** the glossary is populated, **Then** common everyday words (that carry no project-specific meaning) are excluded.
3. **Given** an existing glossary from a prior run, **When** instruction generation runs again, **Then** existing (especially user-edited) entries are preserved rather than discarded.

---

### User Story 2 - Correct and anchor voice/dictated input against the glossary (Priority: P1)

A contributor dictates a request by voice; speech-to-text introduces homophone or easily-confused substitutions (e.g. a domain term rendered as a phonetically similar but wrong word). When any workflow command processes such input, it consults the glossary (loaded as ambient context), recognizes a known variant/homophone of a canonical term, and interprets the input using the canonical term — anchoring the contributor's high-frequency descriptions to the project's agreed vocabulary. Because user input is authoritative, the correction is applied for interpretation without silently discarding what the user literally said.

**Why this priority**: This is the stated core purpose of the feature — reducing errors from voice input. Without it the glossary is only a static dictionary. It is P1 because it delivers the primary user value once a glossary exists.

**Independent Test**: With a populated glossary, provide input containing a known homophone/confusable variant of a canonical term; confirm the framework resolves it to the canonical term and proceeds as if the correct term had been used, while making the correction visible/traceable.

**Acceptance Scenarios**:

1. **Given** a glossary entry whose canonical term has a recorded homophone/confusable variant, **When** input to any workflow command contains that variant, **Then** the input is interpreted using the canonical term.
2. **Given** a correction was applied, **When** the framework acts on the input, **Then** the substitution is surfaced (traceable) so the user can see and, if wrong, override it.
3. **Given** an ambiguous variant that could map to more than one canonical term, **When** the framework cannot choose confidently, **Then** it does not silently pick one and instead defers to the user.

---

### User Story 3 - Progressively enrich the glossary with conflict prompts (Priority: P2)

As the project develops across the spec → plan → tasks → implement workflow, new project-specific terms appear. At natural workflow checkpoints the framework proposes adding these emerging terms to the glossary. When a proposed (or manually added) term conflicts — or could plausibly conflict — with an existing entry (same term with a different meaning, or a homophone/near-duplicate of an existing canonical term), the framework flags the conflict and asks the user to confirm how to resolve it. No conflicting change is written without user confirmation.

**Why this priority**: Keeps the glossary alive and accurate over the project lifetime and prevents corruption from ambiguous additions. It is P2 because it enhances a glossary that Stories 1–2 have already made useful.

**Independent Test**: With an existing glossary, introduce a new term that is a homophone/near-duplicate of an existing canonical term; confirm the framework flags the potential conflict and requires user confirmation before recording anything.

**Acceptance Scenarios**:

1. **Given** ongoing development produces a new project-specific term, **When** the framework reaches a workflow checkpoint and detects it, **Then** it proposes adding the term to the glossary.
2. **Given** a proposed or manually entered term conflicts (or may conflict) with an existing entry, **When** the framework evaluates it, **Then** it presents the conflict and asks the user to confirm the resolution before writing.
3. **Given** the user resolves a conflict, **When** the resolution is recorded, **Then** the user's decision is honored as authoritative.

---

### User Story 4 - Manually edit the glossary with user precedence (Priority: P2)

A user directly edits the glossary — adding, changing, or removing an entry, or correcting a canonical form. The framework treats these manual edits as authoritative: they are preserved across regenerations and take precedence over automatically proposed entries. Automatic proposals never silently overwrite a user-authored entry.

**Why this priority**: The "以用户输入为准" (user input is authoritative) principle is a hard requirement. It is P2 because it constrains the behavior of Stories 1–3 rather than adding a standalone journey.

**Independent Test**: Manually edit an entry, then trigger a step that would auto-propose a different value for the same term; confirm the manual value is retained and the automatic proposal does not overwrite it without confirmation.

**Acceptance Scenarios**:

1. **Given** a user manually edits or adds a glossary entry, **When** any automatic process later runs, **Then** the manual entry is preserved.
2. **Given** an automatic proposal disagrees with a user-authored entry, **When** the framework processes it, **Then** the user-authored value wins unless the user explicitly confirms a change.
3. **Given** the glossary artifact, **When** a user opens it, **Then** it is human-readable and directly editable.

---

### Edge Cases

- **Common-word over-capture**: An automatic proposal suggests a common everyday word with no project-specific meaning → it should be filtered out and not recorded.
- **Same spelling, different meaning**: A new term matches an existing canonical term's spelling but carries a different domain meaning → treated as a conflict requiring user confirmation.
- **Homophone with distinct canonical spelling**: Input contains a word that sounds like a canonical term but is spelled differently → resolved to the canonical term only if recorded as a known variant; otherwise left to the user.
- **Ambiguous variant**: A variant could map to two or more canonical terms → framework must not auto-resolve; defers to user.
- **Empty / brand-new project**: No source material to seed from → an empty but valid glossary is created and grows over time.
- **Conflicting manual entries**: A user manually introduces two entries that conflict with each other → surfaced for the user to reconcile.
- **Removed term still referenced**: A term is removed from the glossary but still appears in project docs → the framework should not fail; anchoring simply no longer applies to that term.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The framework MUST initialize a project glossary as part of the instruction-generation step, seeding it with domain-specific and project-specific terms observable from existing project material.
- **FR-002**: The glossary MUST record only project-specific / domain-specific terms; common everyday words that carry no project-specific meaning MUST be excluded.
- **FR-003**: Each glossary entry MUST capture a canonical term, its known confusable/homophone variants (if any), and a brief domain meaning.
- **FR-004**: The framework MUST propose new glossary terms as they emerge during the project development workflow (progressive enrichment), at natural workflow checkpoints (e.g. requirements, plan, tasks, implement) in addition to manual updates.
- **FR-005**: The framework MUST use the glossary to correct and anchor user input — mapping recorded homophone/confusable variants to their canonical term — with the primary goal of correcting errors introduced by voice/dictated input.
- **FR-006**: When a correction is applied to user input, the framework MUST make the substitution traceable/visible so the user can review and override it.
- **FR-007**: When a variant is ambiguous (could map to more than one canonical term) or unrecognized, the framework MUST NOT silently choose a canonical term and MUST defer to the user.
- **FR-008**: The framework MUST detect existing or potential conflicts (same term with a differing meaning, or homophone/near-duplicate of an existing canonical term) for both automatically proposed and manually entered terms.
- **FR-009**: The framework MUST prompt the user to confirm the resolution of any detected conflict, and MUST NOT write a conflicting change without user confirmation.
- **FR-010**: Users MUST be able to manually add, edit, and remove glossary entries directly.
- **FR-011**: Manual (user-authored) glossary entries MUST be treated as authoritative — preserved across regenerations and never silently overwritten by automatic proposals.
- **FR-012**: The glossary MUST be stored as a durable, human-readable project artifact that is directly viewable and editable.
- **FR-013**: Re-running instruction generation MUST preserve the existing glossary's user-authored content rather than discarding it.
- **FR-014**: There MUST be a single project-wide glossary (one per project), shared across all features and workflow steps; the framework MUST NOT fragment the vocabulary into per-feature glossaries.
- **FR-015**: The glossary MUST be available as ambient context to all `/speckit.*` workflow commands so any of them can anchor and correct user input against it (analogous to how the constitution is ambiently available), rather than being consulted only by a single dedicated command.

### Key Entities *(include if requirement involves data)*

- **Glossary (词汇表)**: The single project-wide collection of domain/project terms. Serves as both an input-anchoring aid and a lightweight domain-knowledge dictionary. Exactly one per project; shared across all features and workflow steps.
- **Glossary Entry (词条)**: A single term record. Attributes: canonical term; known confusable/homophone variants; brief domain meaning/definition; origin (auto-proposed vs. user-authored) and confirmation status. User-authored entries carry precedence over auto-proposed ones.
- **Conflict**: A detected relationship between a candidate term (proposed or manual) and one or more existing entries — either identical spelling with divergent meaning, or phonetic/near-duplicate similarity. Requires user confirmation to resolve. Records the candidate, the conflicting existing entry/entries, and the user's resolution.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After the instruction-generation step runs on a project containing project-specific terminology, a glossary artifact exists on 100% of runs (empty-but-valid when no source terms are available, populated otherwise).
- **SC-002**: For input containing a recorded homophone/confusable variant of a canonical term, the framework resolves it to the canonical term in at least 95% of cases, with the correction visible to the user.
- **SC-003**: 100% of detected term conflicts are surfaced for user confirmation; zero conflicting changes are written without confirmation.
- **SC-004**: 100% of user-authored glossary entries survive a subsequent instruction-generation run unchanged (unless the user explicitly confirmed a change).
- **SC-005**: Common everyday words with no project-specific meaning make up no more than a negligible fraction of auto-proposed entries (auto-proposals are dominated by genuine domain terms).
- **SC-006**: Contributors report a reduction in misinterpreted voice-dictated domain terms compared to a no-glossary baseline.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Presence/validity check of the glossary artifact after instruction generation, verified during acceptance testing across sample projects.
- **SC-002 Source**: Test corpus of input containing known variants mapped to canonical terms; measure resolution rate and confirm the correction is surfaced. Baseline = no glossary (0% auto-resolution).
- **SC-003 Source**: Conflict-handling test scenarios (proposed and manual conflicting terms); audit that every conflict triggered a confirmation prompt and that no write occurred without it.
- **SC-004 Source**: Round-trip test — edit entries, regenerate, diff the glossary; count preserved user-authored entries.
- **SC-005 Source**: Review of auto-proposed entries against a common-word baseline list during acceptance testing.
- **SC-006 Source**: Contributor feedback / observed correction incidents over a usage period, compared against a pre-feature baseline.

## Assumptions

- The glossary is a **document/prompt-framework artifact** (a human-readable, editable project file), consistent with Spec Kit's nature as a document- and prompt-driven framework — not a runtime service, database, or background process.
- "Instruction generation" refers to the framework's existing project-instruction generation step; the glossary is initialized there and lives alongside the project's other canonical memory artifacts (the concrete file location/format is a design decision for `/speckit.plan`).
- "Correction/anchoring" is applied by the AI agent when interpreting user input during the workflow; it is an interpretation aid, not a destructive rewrite of what the user typed/said.
- The primary driver is voice/dictated input, but the same anchoring benefits any user input that references project vocabulary.
- Conflict detection targets project-specific terms only; the deliberate exclusion of common words keeps the glossary small and the conflict surface focused.
- "以用户输入为准" (user input is authoritative) governs precedence throughout: manual edits and explicit user confirmations always win over automatic proposals.

## Clarifications

### Session 2026-07-16

- Q: How should this glossary spec bind to a feature (no existing feature covers vocabulary/glossary)? → A: Create a new feature "Glossary Mechanism" (Feature ID 031); register it in `.specify/memory/features.md` via `/speckit.feature`.
- Q: Which parts of the workflow should actively use the glossary (input correction + progressive enrichment)? → A: Ambient context for all commands — the glossary is loaded as ambient context (like the constitution) so every `/speckit.*` command anchors/corrects input; new terms are proposed at natural checkpoints (requirements/plan/tasks/implement) plus manual edits.
- Q: What is the scope/granularity of the glossary? → A: One project-wide glossary (a single shared vocabulary for the whole project; no per-feature glossaries).
