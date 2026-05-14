# Feature References: Claude Code Support

## Primary Feature

### Feature 021 — Claude Code Support

- **Role in this plan**: The sole primary feature for this requirement.
- **Why primary**: The specification explicitly requests Claude Code support, including custom commands and `.claudeignore`-style configuration.
- **Plan impact**: Must cover assistant selection, validation, command generation, ignore policy, instruction refresh, documentation, governance, coexistence, and release audit.

## Related Existing Features

### Feature 008 — Instructions Command

- **Relationship**: Claude Code compatibility files must remain derived from canonical Spec Kit instructions.
- **Shared assets**:
  - `.specify/instructions.md`
  - `templates/instructions-template.md`
  - `scripts/bash/generate-instructions.sh`

### Feature 015 — CLI Interface

- **Relationship**: Claude Code support affects `specify init --ai ...`, assistant validation, missing-tool messages, and CLI help output.
- **Shared assets**:
  - `src/specify_cli/__init__.py`

### Feature 017 — Template Engine

- **Relationship**: Claude Code custom commands should be generated from canonical command templates.
- **Shared assets**:
  - `templates/commands/*.md`
  - command generation logic in `src/specify_cli/__init__.py`

### Feature 019 — Agents Command

- **Relationship**: Assistant/agent guidance must remain consistent with supported assistant governance and command conventions.
- **Shared assets**:
  - agent-related command templates
  - instruction and compatibility surfaces

### Feature 020 — Qoder Support

- **Relationship**: Closest precedent for adding a first-class assistant across initialization, validation, documentation, distribution, and tests.
- **Reusable patterns**:
  - assistant support matrix updates
  - command generation into assistant-specific directories
  - support-surface audits
  - contract/integration/unit test layering

## Feature Review Outcome

- **New feature required?** No; Feature 021 was already created during requirements and is the correct target.
- **Feature merge/split required?** No.
- **Feature deprecation required?** No.
- **Feature classification change required?** No.
- **Non-functional feature impact?** Configuration Management, Template Engine, and CLI Interface are touched as implementation surfaces, but no separate non-functional feature is required.

## Notes for `/speckit.tasks`

1. Treat governance update as an early blocking task because Claude Code is not currently listed in the constitution-approved assistant set.
2. Derive command coverage tasks from the canonical `templates/commands/*.md` inventory.
3. Include tests that verify `.claudeignore` excludes sensitive/noisy paths without excluding required `.specify/` workflow artifacts.
4. Include coexistence tests for Copilot, Qwen Code, opencode, and Qoder assets.
5. Include release/package audit tasks so generated project resources match documentation and CLI help.
