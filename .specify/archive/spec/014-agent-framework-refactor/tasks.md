# Tasks: Agent Framework Refactor

**Requirement ID**: 014 (from branch name)
**Requirement Key**: 014-agent-framework-refactor
**Related Feature**: 019 Agents Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/014-agent-framework-refactor/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/agents-directory.yaml, quickstart.md

**Tests**: Test tasks are included per Constitution Principle IV (Test-First & Contract-Driven Implementation).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- [ ] All code changes trace to a specific FR in requirements.md
- [ ] Existing skills symlinks continue to work after refactor (regression)
- [ ] `pytest -m contract` passes for new symlink contract tests
- [ ] `pytest -m integration` passes for init flow tests
- [ ] All 6 quickstart.md validation scenarios pass manually
- [ ] `pyproject.toml` force-include verified via `hatch build` or equivalent
- [ ] No backward-incompatible changes to existing `.github/agents/` content (migration only)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Packaging and configuration prerequisites

- [x] T001 Add `"agents" = "specify_cli/agents"` to force-include in `pyproject.toml`
- [x] T002 Add `".specify/agents"` to `_CORE_SPECIFY_ASSETS` list in `src/specify_cli/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Extract and generalize the symlink helper so both skills and agents can use it. MUST complete before any user story work.

**Why this blocks**: US2 (symlink bridging) and US3 (init bundling) both depend on the generalized symlink function. US1 (command template) also references symlink behavior. Extracting this first ensures no code duplication and no regression on existing skills behavior.

- [x] T003 Extract nested `ensure_agent_skills_symlink` from `copy_local_templates()` to a module-level function `ensure_specify_symlink(root_path: Path, agent_dir_name: str, specify_subdir: str)` in `src/specify_cli/__init__.py`. The new function must accept a third parameter `specify_subdir` (e.g., `"skills"` or `"agents"`) instead of hardcoding `"skills"`.
- [x] T004 Replace all five existing `ensure_agent_skills_symlink(project_path, "<dir>")` call sites inside `copy_local_templates()` with `ensure_specify_symlink(project_path, "<dir>", "skills")` in `src/specify_cli/__init__.py`. Remove the old nested function definition.
- [x] T005 [P] Write unit test for `ensure_specify_symlink` covering: fresh create, existing correct symlink (no-op), existing stale symlink (re-link), existing regular directory (migrate + replace) in `tests/unit/test_ensure_symlink.py`
- [x] T006 [P] Write contract test verifying that after calling `ensure_specify_symlink(root, ".github", "skills")`, the symlink `.github/skills` resolves to `.specify/skills` — regression guard for existing behavior in `tests/contract/test_skills_symlink_regression.py`
- [x] T007 Run `pytest -m contract -m integration` to confirm no regression on existing skills symlink behavior

**Checkpoint**: Generalized symlink helper ready. Skills behavior verified. User story implementation can begin.

---

## Phase 3: User Story 1 — Create Agent via `/speckit.agents` Command (Priority: P1) MVP

**Goal**: `/speckit.agents` creates agents in `.specify/agents/` with workspace support files and shared `references/` directory.

**Independent Test**: Run `/speckit.agents` with an agent description, verify `.specify/agents/<name>.agent.md` exists with valid frontmatter, workspace files (`AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md`) are created, and reference materials land in `.specify/agents/references/`.

### Tests for User Story 1

- [x] T008 [P] [US1] Write integration test: run `/speckit.agents`-equivalent template logic and verify `.specify/agents/<name>.agent.md` is created with valid YAML frontmatter in `tests/integration/test_agents_creation.py`

### Implementation for User Story 1

- [x] T009 [US1] Update `templates/commands/agents.md` — change all target paths from `.github/agents/<name>.agent.md` to `.specify/agents/<name>.agent.md`. Update step 1 "Agent File Management" target path, step 10 "Create or update .agent.md" path, and step 12 "Generate and register agent_id" canonical path references.
- [x] T010 [US1] Add workspace file generation to `templates/commands/agents.md` — insert a new step (after directory creation, before agent file write) that checks if `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md` exist in `.specify/agents/` and creates them with initial scaffolding content if absent. Define the scaffold content for each file per plan D5.
- [x] T011 [US1] Update `templates/commands/agents.md` — add instructions for placing agent reference materials in `.specify/agents/references/` instead of inline in the agent body. Update step 8 "Define agent shape" to include reference file handling.
- [x] T012 [US1] Update the "Valid File Locations" section in `templates/commands/agents.md` — change workspace scope from `.github/agents/*.agent.md` to `.specify/agents/*.agent.md` and note that tool-specific paths are symlinks.
- [x] T013 [US1] Update `templates/commands/agents.md` — modify agent_id generation (step 12) to use `.specify/agents/<agent-name>.agent.md` as the canonical path and update the Resource Registry reference accordingly.

**Checkpoint**: `/speckit.agents` now writes to `.specify/agents/` with workspace files and references. Independently testable.

---

## Phase 4: User Story 2 — Tool-Specific Symlink Bridging (Priority: P1)

**Goal**: After agent creation, directory-level symlinks make agents discoverable by all supported AI tools.

**Independent Test**: Create an agent in `.specify/agents/`, then verify directory-level symlinks exist at `.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/` (all pointing to `.specify/agents/`).

### Tests for User Story 2

- [x] T014 [P] [US2] Write contract test verifying directory-level symlink creation: `ensure_specify_symlink(root, ".github", "agents")` creates `.github/agents/` → `.specify/agents/` in `tests/contract/test_agents_symlink.py`
- [x] T015 [P] [US2] Write contract test verifying migration: when `.github/agents/` is a regular directory with files, `ensure_specify_symlink` migrates content to `.specify/agents/` and replaces directory with symlink in `tests/contract/test_agents_symlink.py`

### Implementation for User Story 2

- [x] T016 [US2] Add agent symlink creation calls to `copy_local_templates()` in `src/specify_cli/__init__.py` — after the existing skills symlink block for each tool, add a parallel block calling `ensure_specify_symlink(project_path, "<tool_dir>", "agents")` with matching tracker messages. Tools: `.github` (copilot/claude), `.qoder` (qoder), `.qwen` (qwen), `.opencode` (opencode).
- [x] T017 [US2] Update `templates/commands/agents.md` — add a post-write step that instructs the AI to verify directory-level symlinks exist from tool-specific directories to `.specify/agents/` and note that these are created by `specify init`, not by the command itself.

**Checkpoint**: Symlink bridging works for all 5 tool directories. Agents are discoverable via tool-specific paths.

---

## Phase 5: User Story 3 — Pre-built Agents Bundled with `specify init` (Priority: P2)

**Goal**: `specify init` copies bundled agents from the package into `.specify/agents/` and creates symlinks.

**Independent Test**: Run `specify init` on a fresh directory, verify `.specify/agents/` contains bundled agents and `.github/agents` is a symlink.

### Tests for User Story 3

- [x] T018 [P] [US3] Write integration test: `specify init` on a fresh project creates `.specify/agents/` with bundled agent files and `references/` directory in `tests/integration/test_init_agents.py`
- [x] T019 [P] [US3] Write integration test: `specify init` on a project with existing `.specify/agents/my-agent.agent.md` preserves the user agent and merges bundled agents in `tests/integration/test_init_agents.py`

### Implementation for User Story 3

- [x] T020 [US3] Create initial bundled agent: `agents/code-reviewer.agent.md` — a general-purpose code review agent using `templates/agent-common-template.md` as reference. Include valid YAML frontmatter and body sections per data-model.md schema.
- [x] T021 [P] [US3] Create `agents/references/` directory with `agents/references/.gitkeep` to ensure the shared references directory is included in the wheel.
- [x] T022 [US3] Add agents copy block to `copy_local_templates()` in `src/specify_cli/__init__.py` — after the skills copy block (around line 980), add a parallel block that copies `resource_path / "agents"` to `project_path / ".specify" / "agents"` using `shutil.copytree(dirs_exist_ok=True)` with tracker messages. Guard with `if (resource_path / "agents").exists()`.
- [x] T023 [US3] Verify `hatch build` includes the `agents/` directory in the wheel by checking the built wheel contents.

**Checkpoint**: `specify init` installs bundled agents + creates symlinks. Re-init preserves user agents.

---

## Phase 6: User Story 4 — Shared References Directory (Priority: P2)

**Goal**: Multiple agents can share reference materials through `.specify/agents/references/` without file duplication.

**Independent Test**: Create two agents referencing the same file in `references/`, verify only one copy exists and both agent files resolve the reference.

### Implementation for User Story 4

- [x] T024 [US4] Ensure the `templates/commands/agents.md` reference handling (from T011) uses agent-prefixed naming for agent-specific references and generic naming for shared references per data-model.md naming convention. Verify no duplicate file creation logic.
- [x] T025 [US4] Add a note in `templates/commands/agents.md` step 8 that before creating a new reference file, the agent should check if an equivalent file already exists in `.specify/agents/references/` and reuse it.

**Checkpoint**: Shared references work. No duplication.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation, documentation, and cleanup

- [x] T026 Run quickstart.md Scenario 1 (init with bundled agents) — verified via integration tests (test_init_agents.py)
- [x] T027 Run quickstart.md Scenario 5 (migration from existing regular directory) — verified via contract tests (test_agents_symlink.py::TestAgentsSymlinkMigration)
- [x] T028 [P] Run full test suite: `pytest` — 265 passed, 4 pre-existing failures (unrelated), 1 skipped
- [x] T029 [P] Verify `.specify/agents` appears correctly — pyproject.toml force-include confirmed, agents/ directory structure verified
- [x] T030 Update `.specify/memory/features/019.md` with final implementation notes and set status to reflect refactored agent framework

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — command template changes only (no Python code dependencies on T003/T004)
- **US2 (Phase 4)**: Depends on Foundational (T003/T004 — needs `ensure_specify_symlink`)
- **US3 (Phase 5)**: Depends on Foundational (T003/T004) and US2 (T016 — symlink calls in init)
- **US4 (Phase 6)**: Depends on US1 (T011 — reference handling in template)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — independent of US2/US3/US4
- **US2 (P1)**: Can start after Foundational — independent of US1
- **US3 (P2)**: Depends on US2 being complete (symlink calls in init flow are part of US2 T016)
- **US4 (P2)**: Depends on US1 (reference handling logic)

### Within Each User Story

- Tests before implementation (TDD)
- Template changes are independent and parallelizable
- Python code changes must be sequential where they touch the same function

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T005 and T006 can run in parallel (different test files)
- T008, T014, T015, T018, T019 (test tasks) — independent test files, all [P]
- T020 and T021 can run in parallel (different files in `agents/`)
- US1 and US2 can be developed in parallel after Foundational (different files: `templates/commands/agents.md` vs `src/specify_cli/__init__.py`)
- T026, T027, T028, T029 — all independent validation tasks

---

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T007)
3. Complete Phase 3: US1 — `/speckit.agents` writes to `.specify/agents/` (T008–T013)
4. Complete Phase 4: US2 — Symlink bridging (T014–T017)
5. **STOP and VALIDATE**: Create an agent via `/speckit.agents`, verify it appears at both `.specify/agents/` and `.github/agents/`

### Incremental Delivery

1. Setup + Foundational → generalized symlink helper ready
2. US1 → agents created in canonical directory (MVP command)
3. US2 → agents discoverable by tools (MVP complete)
4. US3 → `specify init` bundles agents (out-of-box value)
5. US4 → shared references (ergonomic improvement)
6. Polish → full validation + documentation

---

## Notes

- The command template (`templates/commands/agents.md`) is a prompt file, not executable code — changes are markdown/text edits
- The CLI code (`src/specify_cli/__init__.py`) is the only Python source file modified
- `pyproject.toml` packaging change is a one-line addition
- The existing `ensure_agent_skills_symlink` function name is misleading (it's a generic symlink helper) — the rename to `ensure_specify_symlink` clarifies its purpose
