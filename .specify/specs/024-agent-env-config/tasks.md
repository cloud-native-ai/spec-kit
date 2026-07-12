---

description: "Task list for 024-agent-env-config"
---

# Tasks: Unified Env-Var Agent Configuration

**Requirement ID**: 024
**Requirement Key**: 024-agent-env-config
**Related Feature**: 022 AI Tools Support
**Input**: Design documents from `.specify/specs/024-agent-env-config/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE implementation; contract + integration + unit tasks emitted per story)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Definition of Done (DoD)

- DoD-1: `config_agent_env_validate` and `config_agent_env_apply` implemented in `skills/agent-setup/scripts/config-agent.sh` per `contracts/unified-env-contract.md`.
- DoD-2: All automated tests pass (`pytest -m contract`, `pytest -m integration`, and unit tests).
- DoD-3: Manual verification completed via `quickstart.md` (validate → apply → inspect files).
- DoD-4: `SKILL.md` and reference docs reflect the unified env-var workflow and 6-tool scope.
- DoD-5: No secret value (API key) appears in any command output, log, or error (FR-014 verified by test).
- DoD-6: Changes validated against Success Criteria SC-001..SC-006 in requirements.md.

**DoD Status**: complete

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies).
- **[Story]**: US1/US2/US3 maps to requirements.md user stories.
- **Note**: Almost all implementation edits the single file `skills/agent-setup/scripts/config-agent.sh`; those tasks are therefore **serialized** (no `[P]`). Test files, docs, and reference files are separate and parallelizable.

## Path Conventions

- Skill source: `skills/agent-setup/` (canonical mirror `.specify/skills/agent-setup/` via install/symlink — edit the `skills/…` source).
- Tests: `tests/contract/`, `tests/integration/`, `tests/unit/` (pytest, per `pyproject.toml`).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Test scaffolding and the input contract reference doc.

- [X] T001 [P] Create an isolated-HOME bash invocation test helper (source `config-agent.sh`, run functions with a temp `$HOME` and controlled `AGENT_*` env, capture stdout/stderr/exit) in tests/integration/agent_env_helpers.py
- [X] T002 [P] Create skills/agent-setup/references/unified-variables.md documenting `AGENT_API_KEY`, `AGENT_MODEL`, `AGENT_BASE_URL`, `AGENT_ANTHROPIC_BASE_URL` and their rules, sourced from `.specify/specs/024-agent-env-config/contracts/unified-env-contract.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Registry, shared helpers, and the offender collector that both stories depend on.

**⚠️ CRITICAL**: No user-story work can begin until this phase is complete.

- [X] T003 [P] Contract test asserting skills/agent-setup/SKILL.md documents the unified variables, the `config_agent_env_validate`/`config_agent_env_apply` commands, and the 6-tool scope (claude, codex, qwen, qoder, iflow, opencode) in tests/contract/test_agent_env_config_contract.py
- [X] T004 Add the 6-tool profile registry (fields: name|protocol|url_source|config_path|format) for claude, codex, qwen, qoder, iflow, opencode in skills/agent-setup/scripts/config-agent.sh
- [X] T005 Add shared helpers (`_ca_ensure_dir`, `_ca_url_has_scheme`, `_ca_json_merge`, `_ca_dotenv_upsert`, `_ca_toml_write_block`) in skills/agent-setup/scripts/config-agent.sh (depends on T004)
- [X] T006 Add target-aware offender collector `_config_agent_env_collect_offenders <targets>` (returns grouped missing/malformed; requires `AGENT_ANTHROPIC_BASE_URL` only when claude is targeted) in skills/agent-setup/scripts/config-agent.sh (depends on T005)
- [X] T007 [P] Reframe skills/agent-setup/SKILL.md around the unified env-var workflow (check → read → write), the 6-tool scope, and the `config_agent_env_validate`/`config_agent_env_apply` commands

**Checkpoint**: Registry + helpers + validation core ready — user stories can begin.

---

## Phase 3: User Story 1 - One-shot configuration of all supported tools (Priority: P1) 🎯 MVP

**Goal**: From valid unified env vars, write each of the six tools' own config file with the mapped key/URL/model, preserving unrelated settings, idempotently, secret-free.

**Independent Test**: Set valid `AGENT_*` vars in a temp HOME, run `config_agent_env_apply --all`, and confirm all six config files exist with correct fields per `contracts/tool-config-targets.md`; re-run yields identical files; pre-seeded unrelated keys survive.

### Tests for User Story 1 (MANDATORY) ⚠️

> Write these FIRST and ensure they FAIL before implementation.

- [X] T008 [P] [US1] US1 integration tests in tests/integration/test_agent_env_apply.py: (a) `apply --all` writes all 6 files with fields per `contracts/tool-config-targets.md`; (b) idempotency — two runs produce identical managed fields; (c) unrelated pre-existing keys preserved; (d) API key never appears in stdout/stderr

### Implementation for User Story 1

- [X] T009 [US1] Update per-tool writers `_config_agent_write_claude` (use `AGENT_ANTHROPIC_BASE_URL`), `_config_agent_write_qoder`, `_config_agent_write_iflow`, `_config_agent_write_opencode` to secondary-assign from unified values and merge-preserve unrelated keys, in skills/agent-setup/scripts/config-agent.sh
- [X] T010 [US1] Add durable file persistence: `_config_agent_write_qwen` → `~/.qwen/.env` (dotenv upsert) and `_config_agent_write_codex` → `~/.codex/config.toml` + `~/.codex/auth.json` (mode 600), in skills/agent-setup/scripts/config-agent.sh (depends on T009)
- [X] T011 [US1] Implement `config_agent_env_apply [--all|<tool>...]` orchestration: read values, iterate targets, ensure dirs, call writers, emit secret-free per-tool report (configured/skipped/failed), exit 0 or 2, in skills/agent-setup/scripts/config-agent.sh (depends on T004–T006, T009, T010)

### Manual Verification for User Story 1

- [X] T012 [US1] Manual QA: follow quickstart.md (export vars → `config_agent_env_apply --all`) and inspect the six config files; confirm no secret printed

**Checkpoint**: US1 fully functional — the MVP (configure-all persistence) is testable independently.

---

## Phase 4: User Story 2 - Pre-flight validation of environment variables (Priority: P2)

**Goal**: A standalone validation step reports every offending variable (grouped missing/malformed) and guarantees no config files are written on failure.

**Independent Test**: Unset/corrupt one or more `AGENT_*` vars, run `config_agent_env_validate --all`, and confirm exit code 1, all offenders listed, and zero files written; confirm `apply` aborts identically.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T013 [P] [US2] US2 validation tests in tests/integration/test_agent_env_validate.py: (a) missing + malformed vars are all reported grouped, exit 1, zero files written; (b) `config_agent_env_apply` aborts on invalid input with no partial writes; (c) claude target requires `AGENT_ANTHROPIC_BASE_URL`

### Implementation for User Story 2

- [X] T014 [US2] Implement `config_agent_env_validate [--all|<tool>...]` using the offender collector: print grouped `Missing`/`Malformed` variables, return exit 1 on any offender, write nothing, in skills/agent-setup/scripts/config-agent.sh
- [X] T015 [US2] Wire the validation gate into `config_agent_env_apply` so it aborts (exit 1, no writes) before any file operation when offenders exist, in skills/agent-setup/scripts/config-agent.sh (depends on T011, T014)

**Checkpoint**: US1 and US2 both work independently.

---

## Phase 5: User Story 3 - Configure a single named tool (Priority: P3)

**Goal**: Target one tool (write only its config file) and reject unknown tool names with a helpful message.

**Independent Test**: Run `config_agent_env_apply qwen` and confirm only `~/.qwen/.env` changes; run with an unknown name and confirm exit 3 plus a list of the six supported tools.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T016 [P] [US3] US3 targeting tests in tests/integration/test_agent_env_targeting.py: (a) single-tool apply writes only that tool's file, others untouched; (b) unknown tool → exit 3 and lists the six supported tools

### Implementation for User Story 3

- [X] T017 [US3] Add target parsing (`--all` | one-or-more tool names) and unknown-tool rejection (exit 3, list the six supported tools) shared by `config_agent_env_validate`/`config_agent_env_apply`, in skills/agent-setup/scripts/config-agent.sh (depends on T011, T014)

**Checkpoint**: All three stories independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T018 [P] Unit tests for pure helpers (`_ca_url_has_scheme`, `_ca_dotenv_upsert`) invoked via bash, in tests/unit/test_agent_env_helpers.py
- [X] T019 [P] Update skills/agent-setup/references/supported-tuples.md and skills/agent-setup/references/available-tuples.md to note the unified `AGENT_*` input model supersedes provider-specific input variables (frame prior four-tuple provider vars as legacy)
- [X] T020 Run quickstart.md end-to-end and confirm secret-free output; record result for SC-001..SC-006 in verification.md (created by /speckit.implement)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup; BLOCKS all user stories.
- **User Stories (Phase 3–5)**: All depend on Foundational.
- **Polish (Phase 6)**: Depends on the desired stories being complete.

### User Story Dependencies

- **US1 (P1)**: After Foundational. Independent MVP.
- **US2 (P2)**: After Foundational. The offender collector (T006) is foundational, so US2 is independently testable; `apply` already aborts once T015 lands.
- **US3 (P3)**: After Foundational. Targeting/rejection layered on the shared parser.

### Within Each Story

- Tests written and failing before implementation (Principle IV).
- Registry/helpers/collector (Phase 2) → writers → orchestration → validation gate → targeting.

### Parallel Opportunities

- Setup: T001, T002 in parallel.
- Foundational: T003 (contract test) and T007 (SKILL.md) parallel with each other; T004→T005→T006 are serialized (same file `config-agent.sh`).
- Story test-authoring tasks (T008, T013, T016) are in separate files and may be written in parallel.
- **Implementation caveat**: T009, T010, T011, T014, T015, T017 all edit `config-agent.sh` and MUST be serialized (no `[P]`).

---

## Parallel Example: kickoff

```bash
# Setup + foundational tests/docs in parallel:
Task: "T001 isolated-HOME test helper in tests/integration/agent_env_helpers.py"
Task: "T002 reference doc skills/agent-setup/references/unified-variables.md"
Task: "T003 SKILL.md contract test in tests/contract/test_agent_env_config_contract.py"
Task: "T007 reframe skills/agent-setup/SKILL.md"

# Story test authoring in parallel (separate files):
Task: "T008 US1 integration tests in tests/integration/test_agent_env_apply.py"
Task: "T013 US2 validation tests in tests/integration/test_agent_env_validate.py"
Task: "T016 US3 targeting tests in tests/integration/test_agent_env_targeting.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 Setup → 2. Phase 2 Foundational → 3. Phase 3 US1 → 4. STOP & VALIDATE (`config_agent_env_apply --all` in a temp HOME) → 5. Demo.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 → configure-all persistence (MVP).
3. US2 → pre-flight validation & fail-fast.
4. US3 → single-tool targeting & unknown rejection.
5. Polish → unit tests, reference docs, quickstart validation.

---

## Notes

- [P] = different files, no dependencies. The core script `config-agent.sh` is a single file → most implementation tasks are serial.
- Verify tests FAIL before implementing.
- Never print the API key value (FR-014) — assert this in tests.
- Prefer `[~]` (deferred, with reason in verification.md) over leaving a task `[ ]`.
