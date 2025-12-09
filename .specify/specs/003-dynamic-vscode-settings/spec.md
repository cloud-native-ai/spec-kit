# Feature Specification: Dynamic VS Code Settings Generation

**Feature Branch**: `003-dynamic-vscode-settings`  
**Created**: 2025-12-09  
**Status**: Draft  
**Input**: User description: "Add dynamic and customized templates/vscode-settings.json to .vscode/settings.json conversion, currently just simple copy, I want to combine project's constitution.md and feature-index.md etc documents, generate different .vscode/settings.json based on different projects, e.g. if project uses java tech stack settings.json should contain java config, if project has coding or formatting requirements settings should have relevant config, use a python script to dynamic load and dump current project directory .vscode/settings.json content, note that .vscode/settings.json is not strict json, might contain comments."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Settings for Java Project (Priority: P1)

As a developer building the Spec Kit in a Java environment, I want the VS Code settings to be pre-configured for Java so that I don't have to manually set them up.

**Why this priority**: Ensures the kit is immediately useful for Java developers.

**Independent Test**: Run the generation script in a directory with `pom.xml` and verify `java.configuration.updateBuildConfiguration` is present in output.

**Acceptance Scenarios**:

1. **Given** a project root with `pom.xml`, **When** `create-release-packages.sh` is run, **Then** the generated `.vscode/settings.json` contains Java-specific settings.

---

### User Story 2 - Generate Settings for Python Project (Priority: P1)

As a developer building the Spec Kit in a Python environment, I want the VS Code settings to be pre-configured for Python.

**Why this priority**: Ensures the kit is immediately useful for Python developers (and Spec Kit itself is Python).

**Independent Test**: Run the generation script in a directory with `pyproject.toml` and verify `python.analysis.typeCheckingMode` is present.

**Acceptance Scenarios**:

1. **Given** a project root with `pyproject.toml`, **When** `create-release-packages.sh` is run, **Then** the generated `.vscode/settings.json` contains Python-specific settings.

---

### User Story 3 - Handle JSONC Templates (Priority: P2)

As a maintainer, I want to be able to use comments in `templates/vscode-settings.json` without breaking the build.

**Why this priority**: VS Code settings often use comments for documentation.

**Independent Test**: Add a comment to the template and run the script.

**Acceptance Scenarios**:

1. **Given** `templates/vscode-settings.json` contains comments (// or /* */), **When** the script runs, **Then** it successfully parses the template and generates valid JSON output.

### Edge Cases

- What happens when no tech stack is detected? -> Should output base template settings.
- What happens when template file is missing? -> Build script handles this (falls back or skips).
- What happens when output directory doesn't exist? -> Script should create it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The build process MUST use a Python script (`scripts/generate_vscode_settings.py`) to generate `.vscode/settings.json`.
- **FR-002**: The script MUST detect the technology stack of the root project by checking for key files (`pom.xml`, `build.gradle`, `pyproject.toml`, `package.json`).
- **FR-003**: The script MUST inject appropriate VS Code settings for the detected stack (Java, Python, JS/TS).
- **FR-004**: The script MUST support reading JSONC (JSON with comments) from the input template.
- **FR-005**: The script MUST output valid JSON.
- **FR-006**: The script MUST check for the presence of `memory/constitution.md` and `memory/feature-index.md` and allow for future logic integration.

### Success Criteria

- Generated `.vscode/settings.json` is valid JSON.
- When run in the Spec Kit repo (Python), the output includes Python settings.
- The build process (`create-release-packages.sh`) completes successfully.
- No external dependencies (like `json5`) are required for the script to run.

### Key Entities

- **Settings Generator**: Python script responsible for logic.
- **Template**: Source JSONC file.
- **Project Context**: The set of files in the root determining the stack.
