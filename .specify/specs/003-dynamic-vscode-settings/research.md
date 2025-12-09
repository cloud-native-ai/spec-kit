# Research: Dynamic VS Code Settings Generation

**Status**: Complete
**Date**: 2025-12-10

## Decisions

### 1. Implementation Language
- **Decision**: Python 3 (Standard Library)
- **Rationale**: 
  - The Spec Kit project already uses Python.
  - Python's `json` module handles JSON generation reliably.
  - `argparse` provides a standard CLI interface.
  - Regular expressions (`re`) are sufficient for stripping comments from JSONC (JSON with comments) without needing external libraries like `json5`.
- **Alternatives Considered**:
  - **Bash (`sed`/`awk`/`jq`)**: Too fragile for robust JSON manipulation and logic branching based on file existence. `jq` might not be available in all environments.
  - **Node.js**: Adds a runtime dependency that might not be present in all build environments for this project.

### 2. JSONC Parsing
- **Decision**: Regex-based comment stripping.
- **Rationale**: `templates/vscode-settings.json` contains comments. The standard `json` library does not support comments. A simple regex can remove `//` and `/* */` style comments before parsing.
- **Trade-offs**: Regex parsing of code/JSON can be imperfect (e.g., comments inside strings), but for a controlled template file, it is a safe and simple solution that avoids dependencies.

### 3. Tech Stack Detection
- **Decision**: File existence check.
- **Rationale**: Checking for `pom.xml`, `pyproject.toml`, `package.json` is the standard way to identify project types.
- **Alternatives**: analyzing file extensions (too slow/complex), reading config files (overkill).

## Unknowns & Clarifications

- **None**: The requirements are clear and the scope is well-defined.
