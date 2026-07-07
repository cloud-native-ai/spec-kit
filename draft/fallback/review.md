# Specification-Driven Development (SDD) Process Review Report: Agent Hook Creation Command

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 002 |
| Requirement Key | 002-agent-hook-creation |
| Requirement Name | Agent Hook Creation Command |
| Related Feature | 002 Agent Hook Management |
| Repository | ai-tracing |
| Repository URL | https://gitlab.alibaba-inc.com/cloud-native-ai/ai-tracing |
| Branch | 002-agent-hook-creation |
| Commit SHA | 34bdb77fe7331f4f4a8f3ffcd57847c80deceb67 (short: 34bdb77) |
| Repo Root (absolute) | /cws_work/ai-tracing |
| Review Date | 2026-07-06 |
| Reviewer (Agent) | Qoder Agent (speckit.review invocation) |
| Environment | Linux 5.10.134-15.2.al8.x86_64 (Ubuntu 22.04); bash; Node.js v25.9.0; npm 11.12.1; Python 3.11.0rc1; Bun not found in PATH |
| spec-kit Source Snapshot | unknown (no version file, no `specify` CLI, not running inside the spec-kit repo itself) |

**Note**: All spec artifacts for requirement 002 are staged in the git index but not yet committed. The commit SHA above (34bdb77) is the latest commit and does NOT contain the spec files. Absolute paths are used throughout this report because no commit contains the spec artifacts.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 126 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/requirements.md | User stories (3), functional requirements (FR-001..008), success criteria, 5 clarification Q&As |
| plan.md | 183 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/plan.md | Technical context, Constitution Check (7 principles), Phase 0 research, 3 plan-level clarifications |
| tasks.md | 222 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/tasks.md | 29 tasks across 6 phases, Tests Mode ON, DoD with 6 criteria, dependency graph |
| data-model.md | 152 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/data-model.md | 4 entities (SupportedTool, HookTemplate, HookArtifact, HookRegistry), validation rules, relationships |
| quickstart.md | 160 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/quickstart.md | 5 scenarios, prerequisites, troubleshooting table, env vars |
| contracts/hook-create.md | 122 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/contracts/hook-create.md | CLI contract: synopsis, behavior paths, output, error responses, side effects |
| contracts/hook-list.md | 109 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/contracts/hook-list.md | Read-only CLI contract: table + JSON output, malformed-registry warning |
| contracts/hook-recreate.md | 94 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/contracts/hook-recreate.md | Thin wrapper over hook-create --force, recreate vs create-fresh output |
| checklists/requirements.md | 39 | /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/checklists/requirements.md | Quality checklist with 3 unchecked items (stale — see F2) |
| feature-detail (002) | 76 | /cws_work/ai-tracing/.specify/memory/features/002-agent-hook-management.md | Feature overview, status tracking, canonical state machine, latest review notes |
| constitution.md | 254 | /cws_work/ai-tracing/.specify/memory/constitution.md | 7 core principles, architecture constraints, governance, version 1.0.0.1 |
| requirements-template.md | 174 | /cws_work/ai-tracing/.specify/templates/requirements-template.md | Template with user stories, FRs, success criteria, shared strings section |
| plan-template.md | 127 | /cws_work/ai-tracing/.specify/templates/plan-template.md | Template with technical context, constitution check, project structure, complexity tracking |
| tasks-template.md | 317 | /cws_work/ai-tracing/.specify/templates/tasks-template.md | Template with DoD, task sigils, phase structure, Python-centric sample tasks |
| feature-details-template.md | 119 | /cws_work/ai-tracing/.specify/templates/feature-details-template.md | Template with overview, key changes, status state machine, duplicate spec entries |
| review-template.md | 187 | /cws_work/ai-tracing/.specify/templates/review-template.md | Template with portable context, findings, recommendations, self-containment check |

## 1. Process Execution Timeline

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|---------|---------------------------------|
| 1 | spec-kit framework added to project | Commit `1f3f00e add speckit framework`; templates, scripts, constitution under `.specify/` | None — initial setup |
| 2 | Feature 002 registered, requirements.md drafted (Draft status) | `/cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/requirements.md` line 5: `**Status**: Draft`; Created: 2026-07-04 | None — standard `/speckit.feature` + `/speckit.requirements` flow |
| 3 | Requirements clarification session (5 Q&As) | requirements.md lines 119-126: `### Session 2026-07-05` with 5 Q&A pairs | None — standard `/speckit.clarify` flow |
| 4 | Checklist generated but left stale | checklists/requirements.md has `[ ] No [NEEDS CLARIFICATION] markers remain` unchecked; Notes claim markers remain | **Yes** — checklist not updated after clarifications resolved the markers (see F2) |
| 5 | plan.md generated (Phase 0 + Phase 1) | plan.md lines 1-183; data-model.md, 3 contracts, quickstart.md created 2026-07-05 | None — standard `/speckit.plan` flow |
| 6 | Plan-level clarification session (3 Q&As) added ad hoc | plan.md lines 18-26: `## Clarifications` / `### Session 2026-07-06` | **Yes** — plan template has no Clarifications section; writer invented it (see F7) |
| 7 | Constitution Check re-verified after Phase 1 | plan.md line 58: `**Re-check after Phase 1**: 2026-07-05` | None — prescribed re-check performed |
| 8 | `feature-ref.md` silently omitted from plan | plan.md documentation tree (lines 64-77) does not list `feature-ref.md`; plan-template.md line 72 lists it as Phase 1 output | **Yes** — template-prescribed artifact not produced, no explanation given (see F3) |
| 9 | tasks.md generated (29 tasks, 6 phases) | tasks.md lines 1-222; all tasks `[ ]` open | None — standard `/speckit.tasks` flow |
| 10 | Feature status advanced to "Planned" | features.md line 10: `Planned`; feature detail line 6: `**Status**: Planned` | None — correct state transition per state machine |
| 11 | Requirements Status NOT updated from "Draft" | requirements.md line 5: `**Status**: Draft` while plan.md line 73 comments `requirements.md # Frozen requirements` | **Yes** — status field contradicts "frozen" label (see F9) |
| 12 | `/speckit.review` invoked before `/speckit.implement` | All 29 tasks in tasks.md are `[ ]` open; no implementation code exists; no `verification.log` | **Yes** — review command spec says "after `/speckit.implement` has completed" (see F12) |
| 13 | Spec files staged but not committed | `git status` shows `A` (staged) for all spec files; no commit contains them | Friction — git log cannot trace spec creation history |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 6 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 4 |
| Documentation | 1 |

## 3. Findings (Problems & Improvement Targets)

### F1 — Cross-artifact endpoint name drift: requirements.md references non-existent `/api/v1/collect`

- **Severity**: P0
- **Category**: Workflow
- **Location**: /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/requirements.md (line 91, line 124); /cws_work/ai-tracing/server.js (line 148)
- **Evidence** (verbatim quote from requirements.md line 91):

  ```
  Hooks send HTTP POST requests to the existing `/api/v1/collect` endpoint on `localhost:<TRACE_PORT>` (default 43200). No new endpoint is required.
  ```

  And from the Clarifications section (requirements.md line 124):

  ```
  A: HTTP POST to the existing `/api/v1/collect` endpoint on `localhost:<TRACE_PORT>` (default 43200)
  ```

  The actual server.js (line 148) registers:

  ```
  } else if (method === 'POST' && url === '/api/v1/report') {
  ```

  The plan.md (line 13) and all three contracts correctly use `/api/v1/report`, but requirements.md was never corrected.

- **Why it's a problem**: The endpoint `/api/v1/collect` does not exist in the actual server. The clarification session perpetuated the error rather than correcting it. The plan writer caught and fixed it downstream, but the "frozen" requirements.md remains wrong. If implementation follows requirements.md literally, hooks will POST to a non-existent endpoint and fail silently. The SDD process has no mechanism to retroactively correct requirements.md when downstream investigation reveals an error in a "frozen" spec.
- **Proposed fix**: Add a post-clarification step to `/speckit.clarify` that scans the requirements body for factual claims contradicted by clarification answers and patches them in place. Alternatively, add a `/speckit.analyze` check that cross-references endpoint paths in requirements.md against `server.js` route definitions.

### F2 — Stale checklist: claims `[NEEDS CLARIFICATION]` markers remain after they were resolved

- **Severity**: P1
- **Category**: Workflow
- **Location**: /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/checklists/requirements.md (lines 16, 34-38)
- **Evidence** (verbatim quote from line 16):

  ```
  - [ ] No [NEEDS CLARIFICATION] markers remain
  ```

  And from the Notes section (lines 34-37):

  ```
  - Two `[NEEDS CLARIFICATION]` markers remain in the Functional Requirements section:
    - FR-002: supported agent tool list and priority.
    - FR-004: hook artifact form factor.
  ```

  The actual requirements.md FR-002 (line 78) reads:

  ```
  - **FR-002**: System MUST maintain a registry of supported agent tools and their hook integration patterns. Initial supported tools in priority order: (1) Claude Code, (2) Qoder CLI, (3) Cursor, (4) GitHub Copilot.
  ```

  No `[NEEDS CLARIFICATION]` marker is present.

- **Why it's a problem**: The checklist was generated during `/speckit.requirements` when markers existed, but `/speckit.clarify` resolved them without updating the checklist. A reviewer reading the checklist would believe the spec is incomplete when it is not. This creates false signals and wasted investigation time.
- **Proposed fix**: Add a post-clarification hook in `/speckit.clarify` that re-runs the checklist validation and updates checkbox states. Alternatively, add an `/speckit.analyze` pass that detects stale checklist items by comparing checklist claims against actual file content.

### F3 — Missing `feature-ref.md`: template prescribes it, plan silently omits it

- **Severity**: P1
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/plan-template.md (line 72); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/plan.md (lines 64-77)
- **Evidence** (verbatim quote from plan-template.md line 72):

  ```
  ├── feature-ref.md       # Phase 1 output (/speckit.plan command)
  ```

  The actual plan.md documentation tree (lines 64-77) does not list `feature-ref.md` at all:

  ```
  .specify/specs/002-agent-hook-creation/
  ├── plan.md              # This file
  ├── data-model.md        # Phase 1 output
  ├── quickstart.md        # Phase 1 output
  ├── contracts/
  │   ├── hook-create.md   # Phase 1 output
  │   ├── hook-list.md     # Phase 1 output
  │   └── hook-recreate.md # Phase 1 output
  ├── requirements.md      # Frozen requirements
  ├── tasks.md             # Phase 2 output (/speckit.tasks)
  └── checklists/
      └── requirements.md  # Existing checklist
  ```

  No `feature-ref.md` exists in the spec directory, and no template for it exists under `/cws_work/ai-tracing/.specify/templates/`.

- **Why it's a problem**: The plan template lists `feature-ref.md` as a Phase 1 output, implying `/speckit.plan` should produce it. But there is no corresponding template, and the plan writer silently dropped it. This creates ambiguity: is `feature-ref.md` mandatory or optional? If mandatory, why is there no template? If optional, why does the template list it as a Phase 1 output?
- **Proposed fix**: Either (a) remove `feature-ref.md` from the plan-template.md documentation tree if it is no longer part of the workflow, or (b) provide a `feature-ref-template.md` under `.specify/templates/` and add generation logic to `/speckit.plan`. If retained as optional, add a conditional note similar to the `research.md` guidance in plan-template.md lines 78-85.

### F4 — Broken cross-reference: plan-template.md points to non-existent `.specify/templates/commands/` directory

- **Severity**: P1
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/plan-template.md (line 6)
- **Evidence** (verbatim quote):

  ```
  **Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.
  ```

  The directory `/cws_work/ai-tracing/.specify/templates/commands/` does not exist. The actual command instruction files are located at `/cws_work/ai-tracing/.claude/commands/speckit.plan.md`, `/cws_work/ai-tracing/.github/prompts/speckit.plan.prompt.md`, `/cws_work/ai-tracing/.opencode/command/speckit.plan.md`, and `/cws_work/ai-tracing/.qwen/commands/speckit.plan.toml`.

- **Why it's a problem**: A reader following the cross-reference encounters a "No such file or directory" error. The plan template was likely written when command instruction files lived under `.specify/templates/commands/`, but the directory structure was reorganized without updating this reference. This is a classic drift risk: the path is hardcoded in a template comment that no automated check validates.
- **Proposed fix**: Update plan-template.md line 6 to reference the actual command instruction location. Since the command files exist in multiple tool-specific directories (`.claude/commands/`, `.github/prompts/`, etc.), either reference all of them or point to a canonical source. Alternatively, remove the cross-reference and rely on the `/speckit.plan` command itself to provide workflow context.

### F5 — Python-centric sample paths in tasks template create friction for non-Python projects

- **Severity**: P1
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/tasks-template.md (lines 137-150, 165-167, 174-176, 200-202)
- **Evidence** (verbatim quotes from lines 137-138):

  ```
  - [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
  - [ ] T011 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py
  ```

  And from lines 146-147:

  ```
  - [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py
  - [ ] T013 [P] [US1] Create [Entity2] model in src/models/[entity2].py
  ```

  The actual project uses JavaScript (Bun/Node.js), as confirmed by the plan.md Technical Context (line 30): `**Language/Version**: JavaScript (Bun 1.0+, ES Modules)`. The tasks-template.md also references Python in its Path Conventions (line 74): `**Single project**: `src/`, `tests/` at repository root` — but then the sample tasks hardcode `.py` extensions and Python-specific directory structures (`tests/contract/`, `src/models/`).

- **Why it's a problem**: Every non-Python project using spec-kit must mentally translate every sample path. The template comment says "The /speckit.tasks command MUST replace these with actual tasks" (line 83-84), but the Python-specific patterns leak into the structural guidance (path conventions, test file naming, source directory layout). This is cargo-cult boilerplate from a Python-first template that was never generalized.
- **Proposed fix**: Replace language-specific paths in the tasks-template.md with language-agnostic placeholders. Use `<test-dir>/test_<name>.<ext>` instead of `tests/contract/test_[name].py`. Add a note directing the writer to derive the actual paths from `plan.md § Technical Context` rather than from the template samples. Consider providing per-language path convention examples (Python, JavaScript, Go, Rust) in a lookup table.

### F6 — Requirements template `Shared Strings` section unused despite verbatim string duplication across contracts

- **Severity**: P1
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/requirements-template.md (lines 143-166); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/contracts/hook-create.md (line 90); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/contracts/hook-recreate.md (line 72)
- **Evidence** (verbatim quote from requirements-template.md lines 143-150):

  ```
  ## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

  <!--
    ACTION REQUIRED:
    Use this section as the SINGLE SOURCE OF TRUTH for string literals that must match
    exactly across multiple artefacts (FRs, contracts, snippet bodies, test assertions,
    task descriptions). Downstream artefacts MUST cite by `<string-id>` rather than
    re-typing the text, so a rotation only edits this section.
  ```

  The actual requirements.md does NOT include this section at all. Meanwhile, the error message is duplicated verbatim in two contracts. From hook-create.md line 90:

  ```
  | `--tool` value not in registry | 1 | `Error: unsupported tool "xyz". Supported tools: claude-code, qoder, cursor, github-copilot` |
  ```

  From hook-recreate.md line 72:

  ```
  | `--tool` value not in registry | 1 | `Error: unsupported tool "xyz". Supported tools: claude-code, qoder, cursor, github-copilot` |
  ```

  The same string also appears in tasks.md (line 92): `validate tool in registry (FR-003)` and in quickstart.md (line 139): `Error: unsupported tool "vim". Supported tools: claude-code, qoder, cursor, github-copilot`.

- **Why it's a problem**: The template provides a mechanism to avoid string duplication, but the writer did not use it. The error message `Error: unsupported tool "xyz". Supported tools: claude-code, qoder, cursor, github-copilot` now lives in at least 3 files with no single source of truth. If the supported tool list changes, all copies must be found and updated manually. The template's `[[STR-NNN]]` citation convention exists but has no enforcement — nothing in the SDD workflow requires or even prompts the writer to populate the Shared Strings section.
- **Proposed fix**: Add a step to `/speckit.plan` that scans the contracts directory for repeated error messages and auto-generates a draft Shared Strings table in requirements.md. Alternatively, add a `/speckit.analyze` check that flags verbatim string duplication across contracts and recommends consolidation via `[[STR-NNN]]` references.

### F7 — Plan template missing `Clarifications` section; writer had to add it ad hoc

- **Severity**: P1
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/plan-template.md (entire file, no Clarifications heading); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/plan.md (lines 18-26)
- **Evidence**: The plan-template.md has headings for: Summary, Technical Context, Constitution Check, Project Structure, Complexity Tracking. There is no `## Clarifications` heading anywhere in the 127-line template.

  The actual plan.md (lines 18-26) adds a Clarifications section:

  ```
  ## Clarifications

  ### Session 2026-07-06

  - Q: How should `{project}` be resolved and tracked for the VS Code-task tools (Cursor, GitHub Copilot)? → A: Resolve `{project}` to the current working directory at command run time; ...
  - Q: How should the file-watcher dependency for Cursor/GitHub Copilot hooks be handled? → A: Add `fswatch` (macOS) / `inotifywait` from `inotify-tools` (Linux) to the documented required system tools. ...
  - Q: How should tool version compatibility be handled in this feature? → A: Out of scope for the initial release (YAGNI, Principle VII). ...
  ```

- **Why it's a problem**: Plan-level clarifications (design decisions that emerge during planning) have no designated home in the template. The writer improvised by adding the section between Summary and Technical Context. Without a template-prescribed location, the position and format of clarifications will vary across specs, making them harder to find and compare. This is a missing-structure issue: information that should be templated lives in unstructured prose.
- **Proposed fix**: Add a `## Clarifications` section to plan-template.md between `## Summary` and `## Technical Context`, with the same Q&A format used in requirements-template.md (lines 168-173). Include a comment noting that plan-level clarifications address design decisions, while requirement-level clarifications address scope ambiguities.

### F8 — Duplicate "Related Specifications" entries in feature-details-template.md

- **Severity**: P2
- **Category**: Template
- **Location**: /cws_work/ai-tracing/.specify/templates/feature-details-template.md (lines 111-116)
- **Evidence** (verbatim quote):

  ```
  ## Related Specifications/Requirements

  - Specification: .specify/specs/[REQUIREMENTS_KEY]/requirements.md
    Quality Checklist: .specify/specs/[REQUIREMENTS_KEY]/checklists/requirements.md
  - Specification: .specify/specs/[REQUIREMENTS_KEY]/requirements.md
    Quality Checklist: .specify/specs/[REQUIREMENTS_KEY]/checklists/requirements.md
  ```

  The same entry is listed twice. The actual feature detail file (002-agent-hook-management.md, lines 74-76) correctly has only one entry:

  ```
  - Specification: `.specify/specs/002-agent-hook-creation/requirements.md`
    Quality Checklist: `.specify/specs/002-agent-hook-creation/checklists/requirements.md`
  ```

- **Why it's a problem**: The duplicate is a copy-paste error in the template. While the writer caught and fixed it during instantiation, the template remains broken for future specs. A writer who does not notice will produce a feature detail file with redundant entries.
- **Proposed fix**: Remove the duplicate entry in feature-details-template.md lines 115-116. Keep a single entry with a comment noting that multiple specifications can be listed if a feature spans multiple requirements.

### F9 — Requirements Status stuck at "Draft" after plan completion and feature advancement to "Planned"

- **Severity**: P2
- **Category**: Workflow
- **Location**: /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/requirements.md (line 5); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/plan.md (line 73)
- **Evidence** (verbatim quote from requirements.md line 5):

  ```
  **Status**: Draft
  ```

  And from plan.md line 73 (documentation tree comment):

  ```
  ├── requirements.md      # Frozen requirements
  ```

  The feature is at status "Planned" (features.md line 10), which per the canonical state machine requires `plan.md`, `data-model.md`, `contracts/`, and `quickstart.md` to exist — all of which are present.

- **Why it's a problem**: The requirements.md status field was set to "Draft" during `/speckit.requirements` and never updated. The plan.md labels it "Frozen requirements," implying it should no longer be Draft. No `/speckit.*` command updates the requirements status field after the plan is generated. This creates a contradiction: the file says Draft, the plan says Frozen, and the feature says Planned.
- **Proposed fix**: Add a status-update step to `/speckit.plan` that changes requirements.md `Status` from `Draft` to `Specified` (or `Frozen`) once the plan is generated. Define the valid status values in the requirements-template.md and document the transition in the feature-details state machine.

### F10 — No spec-kit version tracking: impossible to identify which spec-kit version generated `.specify/`

- **Severity**: P2
- **Category**: Automation
- **Location**: /cws_work/ai-tracing/.specify/ (no version file exists); /cws_work/ai-tracing/.specify/scripts/bash/check-prerequisites.sh (does not report version)
- **Evidence**: No version file exists at any of these paths:
  - `/cws_work/ai-tracing/.specify/.specify-version` — does not exist
  - `/cws_work/ai-tracing/.specify/version` — does not exist
  - `specify --version` — command not found
  - No `version` metadata in `/cws_work/ai-tracing/.specify/instructions.md`

  The `/speckit.review` command instructions state: "If none of these are deducible, record `unknown` explicitly."

- **Why it's a problem**: Without version tracking, it is impossible to determine which spec-kit template/script versions were used to generate the current `.specify/` directory. When templates are updated, there is no way to know whether a consumer project's `.specify/` is up to date. Bug reports from consumer projects cannot be traced to a specific spec-kit version. This is especially problematic for the review report, which aims to provide actionable feedback to spec-kit maintainers — without knowing the version, maintainers cannot determine whether a finding has already been fixed.
- **Proposed fix**: Add a `.specify/VERSION` file during spec-kit initialization that records the spec-kit version (or commit SHA) and the initialization date. Add a `--version` flag to `check-prerequisites.sh` that reads and prints this file. Optionally, add a `/speckit.check-version` command that compares the local VERSION file against the latest spec-kit release and reports drift.

### F11 — Stale instructions.md references: placeholder feature index, missing README, archived DESIGN.md

- **Severity**: P2
- **Category**: Documentation
- **Location**: /cws_work/ai-tracing/.specify/instructions.md (lines 23-25)
- **Evidence** (verbatim quote):

  ```
  | **Feature Index** | `.specify/memory/features.md` | Feature roadmap status | Currently placeholder — run `/speckit.feature` to populate |
  | **Design Spec** | `DESIGN.md` | Technical design document | Architecture, module design, API protocol spec, data flow, env vars |
  | **Readme** | `README.md` | Project readme | Not yet created — create during first `/speckit.plan` run |
  ```

  The actual state:
  - `features.md` now has 2 features (not a placeholder)
  - `DESIGN.md` was split into `docs/architecture.md`, `docs/modules.md`, etc. per commit `34bdb77` ("feat: split DESIGN.md into docs")
  - `README.md` exists (created during the first `/speckit.plan` run for feature 001)

- **Why it's a problem**: The instructions.md is the canonical AI agent instruction file (symlinked to CLAUDE.md, QODER.md, etc.). Stale references mislead agents: an agent reading "Currently placeholder" may attempt to re-populate features.md, and an agent reading "Not yet created" may attempt to create README.md. The DESIGN.md reference points to a file that has been archived. No `/speckit.*` command regenerates instructions.md after major project changes (feature additions, document restructuring).
- **Proposed fix**: Add a post-`/speckit.plan` and post-`/speckit.feature` hook that regenerates instructions.md via `/speckit.instructions`. Alternatively, add a `/speckit.analyze` check that compares instructions.md's Documentation Map against the actual filesystem state and flags stale entries.

### F12 — No enforcement of prescribed command ordering: `/speckit.review` runs before `/speckit.implement`

- **Severity**: P2
- **Category**: Workflow
- **Location**: /cws_work/ai-tracing/.specify/memory/features/002-agent-hook-management.md (lines 62-71, canonical state machine); /cws_work/ai-tracing/.specify/specs/002-agent-hook-creation/tasks.md (all 29 tasks are `[ ]` open)
- **Evidence** (verbatim quote from the feature detail canonical state machine, lines 68-69):

  ```
  | Planned | Implemented | `/speckit.implement` | `tasks.md` has zero `[ ]` rows (all tasks are `[X]` closed or `[~]` deferred) AND `verification.log` records a `SC-NNN_status=pass|deferred` row for every Success Criterion in `requirements.md`. |
  | Implemented | Ready for Review | `/speckit.review` (or human) | All deferred (`[~]`) tasks are resolved or explicitly waived, and review evidence has been produced. |
  ```

  The `/speckit.review` command instructions state: "This command is intended to be used **after** `/speckit.implement` has completed for a feature."

  However, the feature is at status "Planned" (not "Implemented"), all 29 tasks in tasks.md are `[ ]` (open), and no `verification.log` exists. The review was invoked anyway.

- **Why it's a problem**: The review is evaluating an incomplete artifact chain. Without implementation output (`verification.log`, actual code), the review cannot assess implementation-quality findings such as test coverage, code-contract alignment, or deferred-task handling. The canonical state machine defines the transition `Implemented → Ready for Review` as requiring `/speckit.review`, but nothing prevents `/speckit.review` from running at any earlier stage. This undermines the state machine's purpose as a quality gate.
- **Proposed fix**: Add a pre-flight check to `/speckit.review` that reads the feature status from `features.md` and blocks execution (with a clear message) if the status is not "Implemented" or "Ready for Review". Alternatively, downgrade the review to a "pre-implementation review" mode that explicitly notes the missing artifacts and scopes findings to spec/plan/tasks quality only.

## 4. What Worked — Preserve (Brief)

- The Constitution Check table in plan.md (lines 46-56) correctly dynamically renders all 7 principles from `constitution.md` with specific evidence per row — this is a template feature that works well and should be preserved.
- The plan.md "Cross-artifact note" (line 26) explicitly verifies consistency between `data-model.md` and `contracts/hook-list.md` after a clarification — this cross-checking discipline should be encouraged.
- The tasks.md adapts the Python-centric template to JavaScript correctly: test paths use `tests/hook-*.test.js`, source paths use `scripts/` and `lib/`, and the DoD references `bun test` and `node:test` — the adaptation is clean despite template friction.
- The feature-details-template.md canonical state machine (lines 62-74) provides a clear, citable transition table that the feature detail file correctly instantiates — this is a strong template design.
- The tasks.md task sigil system (`[ ]`, `[X]`, `[~]`) with parallelism markers (`[P]`) and user-story labels (`[US1]`, `[US2]`, `[US3]`) provides excellent traceability — the template structure is sound.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Add Clarifications section to plan template** — Target: `/cws_work/ai-tracing/.specify/templates/plan-template.md`. Add a `## Clarifications` section between `## Summary` and `## Technical Context` with the same Q&A format as requirements-template.md lines 168-173. Source: F7. Expected impact: plan-level design decisions get a structured home instead of ad hoc placement.

- **Remove or template-ize `feature-ref.md`** — Target: `/cws_work/ai-tracing/.specify/templates/plan-template.md` line 72. Either remove `feature-ref.md` from the documentation tree if it is no longer part of the workflow, or provide a `feature-ref-template.md` under `.specify/templates/` and add generation logic to `/speckit.plan`. Source: F3. Expected impact: eliminates ambiguity about whether `feature-ref.md` is a required artifact.

- **Fix broken `.specify/templates/commands/` cross-reference** — Target: `/cws_work/ai-tracing/.specify/templates/plan-template.md` line 6. Update the reference to point to the actual command instruction file location(s), or remove it. Source: F4. Expected impact: eliminates a dead link that confuses readers.

- **Generalize tasks template paths from Python-specific to language-agnostic** — Target: `/cws_work/ai-tracing/.specify/templates/tasks-template.md` lines 74, 137-150, 165-167, 174-176, 200-202. Replace `.py` extensions and Python-specific directory structures with language-agnostic placeholders. Add a note directing writers to derive paths from `plan.md § Technical Context`. Source: F5. Expected impact: reduces friction for all non-Python projects using spec-kit.

- **Remove duplicate Related Specifications entries in feature-details template** — Target: `/cws_work/ai-tracing/.specify/templates/feature-details-template.md` lines 115-116. Delete the duplicate entry. Source: F8. Expected impact: eliminates a copy-paste template bug.

- **Enforce or prompt for Shared Strings usage** — Target: `/cws_work/ai-tracing/.specify/templates/requirements-template.md` lines 143-166. Add a stronger comment or make the section non-optional when contracts contain repeated error messages. Source: F6. Expected impact: reduces string duplication drift across contracts.

### 5.2 Command Prompt Improvements

(No command-prompt-specific findings in this review. All command prompt issues are covered under Template or Workflow recommendations.)

### 5.3 Automation / Script Improvements

- **Add spec-kit version tracking** — Target: `/cws_work/ai-tracing/.specify/scripts/bash/check-prerequisites.sh`. Add a `.specify/VERSION` file during spec-kit initialization and a `--version` flag to `check-prerequisites.sh` that reads it. Source: F10. Expected impact: enables version-aware bug reporting and drift detection.

### 5.4 Workflow Improvements

- **Add post-clarification checklist update** — Target: `/speckit.clarify` command workflow. After resolving clarifications, re-validate the requirements checklist and update checkbox states. Source: F2. Expected impact: eliminates stale checklist items that create false incompleteness signals.

- **Add requirements status update on plan completion** — Target: `/speckit.plan` command workflow. After generating `plan.md`, update requirements.md `Status` from `Draft` to `Specified` or `Frozen`. Source: F9. Expected impact: eliminates the Draft/Frozen/Planned status contradiction.

- **Add pre-flight status gate to `/speckit.review`** — Target: `/speckit.review` command workflow. Before generating the review, read the feature status from `features.md` and block execution if the status is not "Implemented" or "Ready for Review". Source: F12. Expected impact: prevents reviewing an incomplete artifact chain.

- **Add cross-artifact endpoint validation** — Target: `/speckit.analyze` command workflow. Add a check that cross-references endpoint paths mentioned in `requirements.md` against actual route definitions in the project's server entry point. Source: F1. Expected impact: catches endpoint name drift before it propagates to implementation.

### 5.5 Documentation Improvements

- **Add instructions.md regeneration trigger** — Target: `/speckit.instructions` command and the `/speckit.plan` + `/speckit.feature` post-completion hooks. Regenerate `instructions.md` after feature additions or document restructuring to keep the Documentation Map current. Source: F11. Expected impact: eliminates stale references in the canonical AI agent instruction file.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Add cross-artifact endpoint validation to catch requirements/server drift | `/speckit.analyze` workflow | F1 |
| P1 | Add post-clarification checklist update | `/speckit.clarify` workflow | F2 |
| P1 | Remove or template-ize `feature-ref.md` | plan-template.md | F3 |
| P1 | Fix broken `.specify/templates/commands/` cross-reference | plan-template.md | F4 |
| P1 | Generalize tasks template from Python-specific to language-agnostic | tasks-template.md | F5 |
| P1 | Enforce Shared Strings usage when contracts contain repeated strings | requirements-template.md | F6 |
| P1 | Add Clarifications section to plan template | plan-template.md | F7 |
| P2 | Remove duplicate Related Specifications entries | feature-details-template.md | F8 |
| P2 | Add requirements status update on plan completion | `/speckit.plan` workflow | F9 |
| P2 | Add spec-kit version tracking file and check | check-prerequisites.sh | F10 |
| P2 | Add instructions.md regeneration trigger | `/speckit.instructions` workflow | F11 |
| P2 | Add pre-flight status gate to `/speckit.review` | `/speckit.review` workflow | F12 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
