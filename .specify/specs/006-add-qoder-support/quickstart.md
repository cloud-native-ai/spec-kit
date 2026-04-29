# Quickstart: Validate Qoder Support

## Prerequisites

- The workspace is at the repository root.
- The implementation tasks for this feature have been completed.
- To verify the normal CLI check path, `qoder` is installed on this machine; to verify the failure path, ensure `qoder` is not in `PATH`.

## Scenario 1: New project initialization with Qoder

1. [CN] `specify init demo-qoder --ai qoder`[CN]
2. [CN]
   - `.qoder/commands/`
   - `.qoder/project_rules.md`[CN]
   - `.specify/` [CN]
3. [CN] Qoder [CN]

**Expected Result**:
- [CN]
- [CN] Qoder [CN]
- [CN]

## Scenario 2: Existing-directory initialization with Qoder

1. [CN] `specify init . --ai qoder --ignore-agent-tools`[CN]
2. [CN]
3. [CN] Qoder [CN] Qoder [CN]

**Expected Result**:
- Qoder [CN]
- [CN]

## Scenario 3: Missing Qoder CLI failure path

1. [CN] `qoder` CLI [CN]
2. [CN] `specify init demo-qoder --ai qoder`[CN]

**Expected Result**:
- [CN] `qoder`[CN]
- [CN]
- [CN] `--ignore-agent-tools`[CN]

## Scenario 4: Skip validation with existing ignore behavior

1. [CN] `qoder` CLI [CN] `specify init demo-qoder --ai qoder --ignore-agent-tools`[CN]
2. [CN]

**Expected Result**:
- CLI [CN]
- [CN] Qoder [CN]

## Scenario 5: Refresh instructions and support surfaces

1. [CN] `generate-instructions.sh` [CN]
2. [CN]
   - `README.md`
   - `docs/installation.md`
   - `.ai/instructions.md`
   - `templates/plan-template.md`
   - `templates/commands/agents.md`
3. [CN] Qoder [CN]

**Expected Result**:
- [CN] Qoder[CN]
- [CN]“[CN] `.qoder/`[CN]/[CN]”[CN]

## Scenario 6: Release/package audit

1. [CN]
2. [CN] Qoder [CN]
3. [CN]

**Expected Result**:
- [CN] CLI [CN] Qoder[CN]
- [CN] SC-004 [CN] FR-007[CN]