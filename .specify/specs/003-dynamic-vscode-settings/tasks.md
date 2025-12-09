# Tasks: Dynamic VS Code Settings Generation

**Feature**: Dynamic VS Code Settings
**Status**: In Progress

## Phase 1: Setup
*Goal: Initialize the generation script structure.*

- [x] T001 Create `scripts/generate_vscode_settings.py` skeleton with argument parsing
- [x] T002 Implement `strip_comments` function in `scripts/generate_vscode_settings.py` for JSONC support

## Phase 2: Foundational
*Goal: Implement core detection logic.*

- [x] T003 Implement `detect_tech_stack` function in `scripts/generate_vscode_settings.py` (Java, Python, JS/TS detection)

## Phase 3: User Story 1 (Java Support)
*Goal: Generate settings for Java projects.*

- [x] T004 [US1] Add Java detection logic (pom.xml, build.gradle) in `scripts/generate_vscode_settings.py`
- [x] T005 [US1] Add Java-specific settings injection (e.g. `java.configuration.updateBuildConfiguration`) in `scripts/generate_vscode_settings.py`

## Phase 4: User Story 2 (Python Support)
*Goal: Generate settings for Python projects.*

- [x] T006 [US2] Add Python detection logic (pyproject.toml, etc.) in `scripts/generate_vscode_settings.py`
- [x] T007 [US2] Add Python-specific settings injection (e.g. `python.analysis.typeCheckingMode`) in `scripts/generate_vscode_settings.py`

## Phase 5: User Story 3 (JSONC Support)
*Goal: Ensure template comments are handled.*

- [x] T008 [US3] Verify JSONC parsing with comments in `templates/vscode-settings.json` (Implicitly tested via usage)

## Phase 6: Polish & Integration
*Goal: Finalize integration and update templates.*

- [x] T009 Update `create-release-packages.sh` to invoke `generate_vscode_settings.py`
- [x] T010 Update `templates/vscode-settings.json` to include all `speckit.*.prompt.md` files in `chat.promptFilesRecommendations`

## Dependencies

- Phase 1 & 2 must be completed before Phase 3 & 4.
- Phase 3 & 4 can be executed in parallel.
- Phase 6 depends on all previous phases.

## Implementation Strategy

- **MVP**: Script that reads template and outputs it (Phase 1).
- **Increment 1**: Tech stack detection (Phase 2).
- **Increment 2**: Specific stack support (Phase 3 & 4).
- **Final**: Integration into build pipeline (Phase 6).
