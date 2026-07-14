# Requirements Specification: Reclassify sdd-workflow as a Shared Reference Directory

**Requirement Branch**: `028-sdd-workflow-refactor`  
**Created**: 2026-07-14  
**Status**: Draft  
**Input**: User description: "参考 docs/summary/03-sdd-workflow-refactor-proposal.md 的提议，将 sdd-workflow 从「技能」重构为「共享参考目录」。"

## Related Feature *(mandatory)*

**Feature ID**: 029  
**Feature Name**: Shared Reference Directory

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE.
-->

### User Story 1 - Stop treating shared protocols as an invocable skill (Priority: P1)

As a Spec Kit maintainer, I want the shared SDD protocol documents to no longer be registered or discovered as a skill, so that AI agents cannot mis-invoke a "skill" that is not actually invocable, the skill namespace and registry stay clean, and maintainers are not confused about whether it is a skill or a document library.

**Why this priority**: This is the core problem the refactor exists to solve. The current `sdd-workflow` entry self-declares "This skill is NOT invoked directly," yet appears in the invocable skill list, pollutes the skills registry, and is symlinked into every tool's skills directory — creating real mis-invocation risk and conceptual ambiguity. Removing it delivers value on its own.

**Independent Test**: After the change, confirm that `sdd-workflow` does not appear in any skill registry table, skill count, or skill-discovery listing, and is absent from `skills/`, `.specify/skills/`, and every compatibility skills path (`.github/skills`, `.<agent>/skills`).

**Acceptance Scenarios**:

1. **Given** the project after the refactor, **When** an agent enumerates available skills, **Then** `sdd-workflow` is not present in the list.
2. **Given** the instructions/registry file, **When** the Skills registry table and skill count are inspected, **Then** `sdd-workflow` is absent and the total skill count reflects one fewer skill.
3. **Given** the source tree and installed workspace, **When** the skills directories and their compatibility symlinks are listed, **Then** no `sdd-workflow` skill directory exists in any of them.

---

### User Story 2 - Relocate shared protocols to a dedicated shared reference location (Priority: P1)

As a command/skill author, I want the shared protocol documents (input protocol, feature integration, agent configuration, clarify taxonomy, DfX catalog, ignore patterns, tool definitions, checklist methodology, requirements guidelines, feedback step) to live in a dedicated shared reference directory that is installed into the project workspace at init, so that commands and skills can reference a single de-duplicated source without borrowing the skills pipeline.

**Why this priority**: The documents themselves are still valuable and actively referenced (~100 references across templates, skills, and the installed mirror). They must remain available at a stable, installed location; otherwise every referring command/skill breaks. This story is the necessary counterpart to removing the pseudo-skill.

**Independent Test**: After a fresh init, confirm the dedicated shared reference directory exists at `.specify/shared/workflow` in the installed workspace and contains all previously-shipped reference documents with unchanged content.

**Acceptance Scenarios**:

1. **Given** the source tree, **When** the shared reference directory `shared/workflow` is inspected, **Then** it contains all ten reference documents previously under `skills/sdd-workflow/references/` with equivalent content.
2. **Given** a fresh project initialization, **When** the workspace is inspected, **Then** `.specify/shared/workflow` is present, copied wholesale like other core assets (templates, scripts).
3. **Given** an already-initialized project, **When** initialization is run again, **Then** `.specify/shared/workflow` is preserved and not overwritten (treated as a retained core asset).

---

### User Story 3 - No dangling references after the move (Priority: P1)

As a Spec Kit maintainer, I want every reference that previously pointed at `skills/sdd-workflow/...` to be updated to the new shared location, so that no command or skill produces a runtime dead link when it tries to load a shared protocol.

**Why this priority**: The refactor's dominant risk is a missed reference causing a runtime dead link. A single unmigrated path silently breaks a command's ability to load its protocol. This is the acceptance gate for the whole feature.

**Independent Test**: Search the entire repository for the token `sdd-workflow`; the result set contains zero live references outside of historical/archival content (e.g., this spec, the proposal document, and `docs/history/`).

**Acceptance Scenarios**:

1. **Given** the refactored source tree, **When** a repository-wide search for `sdd-workflow` is run, **Then** it returns zero matches in active source, templates, skills, and the installed mirror.
2. **Given** any command that previously loaded a shared protocol, **When** that reference path is resolved, **Then** it points to an existing file under `shared/workflow` / `.specify/shared/workflow`.
3. **Given** a skill that previously hard-coded a `.specify/skills/sdd-workflow/...` path, **When** the path is inspected, **Then** it uses `.specify/shared/workflow/...` and resolves to an existing file.

---

### User Story 4 - Consistent reference form and documentation (Priority: P2)

As a maintainer, I want references to the shared directory to follow one consistent convention and the documentation map to reflect the new structure, so that future authors are not confused by mixed reference styles or stale docs.

**Why this priority**: Prevents regression into the same ambiguity the refactor removes; important for maintainability but not required for the runtime to work.

**Independent Test**: Inspect referring artefacts and confirm command templates use the root-relative form (`shared/workflow/...`, rewritten with the `.specify/` prefix during install) while skills use the installed absolute form (`.specify/shared/workflow/...`), with no mixing; confirm docs no longer describe `sdd-workflow` as a skill.

**Acceptance Scenarios**:

1. **Given** command templates, **When** their shared-reference links are inspected, **Then** they use the root-relative form `shared/workflow/...` consistent with existing template conventions.
2. **Given** skills that reference shared protocols, **When** their links are inspected, **Then** they use the installed absolute form `.specify/shared/workflow/...`, and no artefact mixes the two forms.
3. **Given** the documentation, **When** the sections mentioning `sdd-workflow` are inspected, **Then** they describe the shared reference directory instead of a skill.

---

### Edge Cases

- **Regenerated mirror**: The installed `.specify/` mirror is regenerated from source; source changes must fully propagate so the mirror contains no `sdd-workflow` remnants after regeneration.
- **Release/packaging enumeration**: If any packaging or release logic enumerates skills to bundle assets, the new `shared/` directory must be bundled equally; otherwise the installed workspace would be missing the shared references.
- **Fresh install vs. upgrade**: Both a brand-new init and re-init over an existing workspace must yield a workspace containing `.specify/shared/workflow`, without clobbering user-retained core assets.
- **Historical content**: Archival material (e.g., `docs/history/`, this spec, the proposal itself) legitimately still contains the string `sdd-workflow` and must be excluded from the zero-reference gate.
- **Content parity**: Relocation must preserve document content; a move must not silently drop or alter a reference document.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST remove `sdd-workflow` as a skill — deleting its skill directory from the source `skills/` tree and ensuring it is absent from the installed skills directory and all compatibility skills symlinks.
- **FR-002**: The system MUST remove `sdd-workflow` from the skills registry table, from the skill count, and from any skill-discovery listing so that agents no longer treat it as an invocable skill.
- **FR-003**: The system MUST relocate all shared protocol documents currently under `skills/sdd-workflow/references/` into a dedicated shared reference directory in the source tree (`shared/workflow`), installed at `.specify/shared/workflow`, preserving each document's content. The `workflow/` subdirectory leaves room for future shared reference families under `shared/`.
- **FR-004**: The system MUST copy the `shared/` directory into the installed `.specify` workspace during initialization, using the same wholesale copy model as existing core assets (templates, scripts).
- **FR-005**: The system MUST treat the installed `.specify/shared` directory as a retained core asset so that re-running initialization does not overwrite it.
- **FR-006**: The system MUST apply a path-rewrite rule so that root-relative references to `shared/` receive the `.specify/` prefix at install time, consistent with the existing rewrite behavior for other core asset directories.
- **FR-007**: The system MUST update every reference that previously targeted `skills/sdd-workflow/...` to the new shared location — command templates to `shared/workflow/...` (root-relative form) and skills to `.specify/shared/workflow/...` (installed absolute form).
- **FR-008**: References MUST follow a single consistent convention per artefact type (command templates use `shared/workflow/...`; skills use `.specify/shared/workflow/...`) with no mixing of the two forms.
- **FR-009**: The system MUST update user-facing documentation (documentation map, skills docs, and any other mentions) to describe the shared reference directory rather than a skill.
- **FR-010**: After the refactor, a repository-wide search for the token `sdd-workflow` MUST return zero matches in active source, templates, skills, and the installed mirror (historical/archival content and this feature's own spec/proposal excluded).
- **FR-011**: Every migrated reference MUST resolve to an existing file at the new shared location, producing no runtime dead links when a command or skill loads a shared protocol.
- **FR-012**: If any packaging/release logic enumerates skills to bundle assets, the system MUST ensure the `shared/` directory is bundled into distributed packages so the installed workspace contains it.

### Key Entities *(include if requirement involves data)*

- **Shared Reference Directory**: The dedicated, install-time-copied location holding the common SDD protocol documents; source `shared/workflow`, installed `.specify/shared/workflow`; replaces the former skill.
- **Reference Document**: One of the ten shared protocol/guideline files (input protocol, feature integration, agent configuration, checklist methodology, requirements guidelines, DfX catalog, clarify taxonomy, ignore patterns, tool definitions, feedback step) consumed by commands/skills.
- **Skill Registry Entry**: The row and count in the instructions/registry describing `sdd-workflow`, to be removed.
- **Reference Link**: A path in a command template or skill pointing at a shared protocol document; must be rewritten to the new location in the correct form.
- **Core Asset Retention List**: The set of installed assets preserved across re-init; must include the `.specify/shared` directory.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A repository-wide search for `sdd-workflow` returns zero live matches (excluding historical/archival content and this feature's spec/proposal).
- **SC-002**: The skill registry lists exactly one fewer skill than before, and `sdd-workflow` appears in no skill listing, registry table, or skills directory (source, installed, or symlinked).
- **SC-003**: All ten previously-shipped reference documents exist at `.specify/shared/workflow` with content equivalent to their originals (100% preserved, 0 lost).
- **SC-004**: After a fresh initialization, `.specify/shared/workflow` is present and 100% of migrated references resolve to existing files (0 dead links).
- **SC-005**: Re-running initialization over an existing workspace leaves `.specify/shared/workflow` intact (0 unintended overwrites).
- **SC-006**: The existing test suite passes with no regressions introduced by the refactor.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Repository-wide text search for the token `sdd-workflow`, run as the final acceptance gate; baseline is the current count of matches across active source.
- **SC-002 Source**: Inspection of the instructions/registry Skills table and skill count, plus directory listings of `skills/`, `.specify/skills/`, and compatibility symlink paths.
- **SC-003 Source**: File-by-file comparison of the ten reference documents between their original and new locations.
- **SC-004 Source**: Fresh `specify init` into a scratch workspace, followed by resolution of each migrated reference path.
- **SC-005 Source**: Re-init over an initialized workspace, followed by inspection of the `.specify/shared/workflow` contents/timestamps.
- **SC-006 Source**: Full `pytest` run (contract + integration + unit) compared against the pre-refactor baseline.

## Clarifications

### Session 2026-07-14

- Q: Which Feature should spec 028 bind to? → A: Create new Feature 029 "Shared Reference Directory" — introduces a distinct new asset class (install-time-copied shared references) plus retention/path-rewrite pipeline not captured by any existing feature.
- Q: What is the exact shared reference directory name (FR-003)? → A: `.specify/shared/workflow` (source: `shared/workflow`). Clearest English; the `workflow/` subdir leaves room for future shared families under `shared/`.
