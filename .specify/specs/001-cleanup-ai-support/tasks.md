# Implementation Tasks: Cleanup Legacy AI Tools Support

**Feature**: Cleanup Legacy AI Tools Support (`001-cleanup-ai-support`)
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Phase 1: Setup

- [ ] T001 Verify project prerequisite check script still passes [.specify/scripts/bash/check-prerequisites.sh]

## Phase 2: Foundational

- [ ] T002 Update Agent Registry Configuration in [src/specify_cli/__init__.py]
  - Reduce `AGENT_CONFIG` to include only: `copilot`, `qwen`, `opencode`.
  - Remove all other entries (`claude`, `gemini`, `cursor-agent`, `codex`, `windsurf`, etc.).

## Phase 3: User Story 1 - Remove Unsupported AI Tools

**Goal**: Remove all code and templates related to unsupported AI tools.
**Independent Test**: Search for "Claude", "Gemini", etc. in codebase and find no functional logic.

- [ ] T003 [US1] Clean up `generate_commands` function in [src/specify_cli/__init__.py]
  - Remove logic branches for `claude`, `gemini`, `cursor-agent`, `codex`, `windsurf`, `kilocode`, `auggie`, `codebuddy`, `roo`, `q`.
  - Ensure only `copilot`, `qwen`, `opencode` logic remains.

- [ ] T004 [US1] Remove deprecated CLI options in [src/specify_cli/__init__.py]
  - Update `ai_assistant` help text in `init` command to list only supported agents.
  - Remove any legacy imports if they become unused.

- [ ] T005 [P] [US1] Prune removed agent templates if any exist in [templates/commands/]
  - (Note: Most generic templates are kept; only specific overrides if they exist need removal).
  - Verify if `templates/commands/` contains any agent-specific files that are no longer referenced.

## Phase 4: User Story 2 - Verify Supported Tools & Documentation

**Goal**: Ensure the retained tools work and documentation is accurate.
**Independent Test**: Run `specify init --ai <agent>` for all 3 supported agents.

- [ ] T006 [P] [US2] Update primary documentation in [README.md]
  - Update supported tools list.
  - Remove references to removed tools in installation/usage sections.

- [ ] T007 [P] [US2] Update user documentation in [docs/]
  - Scan `docs/` for references to removed tools and update.

- [ ] T008 [US2] Verify `opencode` initialization logic in [src/specify_cli/__init__.py]
  - Ensure `generate_commands` for `opencode` correctly uses `md` extension and `$ARGUMENTS` placeholder.

- [ ] T009 [US2] Verify `qwen` initialization logic in [src/specify_cli/__init__.py]
  - Ensure `generate_commands` for `qwen` correctly uses `toml` extension and `{{args}}` placeholder.

- [ ] T010 [US2] Verify `copilot` initialization logic in [src/specify_cli/__init__.py]
  - Ensure `generate_commands` for `copilot` correctly uses `prompt.md` extension and `$ARGUMENTS` placeholder.

## Final Phase: Polish

- [ ] T011 Run full linting and type checking on [src/specify_cli/]
- [ ] T012 Manual test: Run `specify init --help` and verify output.

## Dependencies

- Phase 2 (Config update) blocks Phase 3 (Logic removal) and Phase 4 (Verification).
- Phase 3 (Logic removal) blocks final verification in Phase 4.

## Implementation Strategy

1.  **Cut the config first**: Updating `AGENT_CONFIG` (T002) is the most impactful change.
2.  **Prune the logic**: Update `generate_commands` (T003) to match the new config.
3.  **Update Docs**: Reflect reality in README and help text.
