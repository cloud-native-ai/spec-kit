# Research: Add Qoder Support

## Context Summary

[CN] Qoder [CN]“[CN]”[CN]“[CN]”[CN] `README.md`[CN]`docs/**`[CN]`.specify/memory/**`[CN]`src/specify_cli/__init__.py`[CN]`scripts/bash/generate-instructions.sh` [CN] `tmp/patches/qoder-main/` [CN]

## Key Findings

### 1. Current assistant architecture is matrix-driven

- CLI assistant definitions are centralized in `AGENT_CONFIG` in `src/specify_cli/__init__.py`.
- The main initialization path distributes command assets for different assistants through `copy_local_templates()` + `generate_commands()`.
- [CN] CLI/IDE [CN] `copilot`[CN]`qwen`[CN]`opencode`[CN]
- `scripts/bash/generate-instructions.sh` [CN] `.qoder/project_rules.md`[CN] Qoder [CN]

### 2. Governance and public docs are currently inconsistent with Qoder support

- `.specify/memory/constitution.md` [CN] GitHub Copilot[CN]Qwen Code[CN]opencode[CN]
- `README.md` [CN] `docs/installation.md` [CN] Qoder[CN]
- `templates/plan-template.md` [CN] `templates/commands/agents.md` [CN]
- [CN] CLI[CN] FR-012/FR-013[CN]

### 3. Upstream patch provides a low-risk implementation reference

[CN] `tmp/patches/qoder-main/non-merge/0001-feat-support-Qoder-CLI.patch` [CN]

- [CN] key[CN]`qoder`
- [CN]`Qoder CLI`
- CLI [CN]`qoder`
- [CN]`https://qoder.com/cli`
- [CN]`.qoder/commands/`
- [CN]Markdown
- [CN]/[CN]`QODER.md` [CN] `.qoder/project_rules.md` [CN]

[CN] Qoder [CN]

### 4. Existing refresh behavior constrains implementation strategy

- [CN]
- [CN] `generate-instructions.sh`[CN]
- [CN]“[CN] Qoder [CN]”[CN]“[CN]”[CN]

## Decisions

### Decision 1: Treat Qoder as a CLI-based first-class assistant

**Decision**: Qoder [CN] `qwen`[CN]`opencode` [CN] CLI [CN]

**Why**:
- [CN] FR-001[CN]FR-004[CN]FR-005[CN]FR-011[CN]
- [CN] `AGENT_CONFIG` [CN]
- [CN]

### Decision 2: Use `.qoder/commands/` as the generated command directory

**Decision**: [CN]Qoder [CN] `.qoder/commands/`[CN]

**Why**:
- [CN]
- [CN] `.qoder/project_rules.md` [CN]
- [CN] FR-002[CN]FR-006[CN]FR-007[CN]

### Decision 3: Make governance alignment part of the feature, not a follow-up

**Decision**: [CN] feature [CN]Feature [CN]README[CN]

**Why**:
- [CN] Qoder [CN]
- [CN] FR-012[CN]FR-013[CN]

### Decision 4: Model support consistency as a releasable contract

**Decision**: [CN] `contracts/qoder-support.openapi.yaml` [CN]CLI [CN]

**Why**:
- [CN] FR-012 [CN]“[CN]”[CN] tasks/test cases[CN]
- [CN]

## Drift and Risks

### Known drift

- README [CN]
- Qoder [CN] README/[CN]/[CN]
- [CN] Qwen/opencode [CN] Qoder[CN]

### Risks to control in implementation

1. **[CN]**[CN] CLI[CN]
2. **[CN]**[CN]`--ai` [CN]`check()` [CN] Qoder[CN]
3. **[CN]**[CN]
4. **[CN]**[CN] wheel/[CN] SC-004 [CN]

## Recommended Implementation Order

1. [CN]
2. [CN] CLI [CN]/[CN]
3. [CN]
4. [CN] README[CN]
5. [CN]

## Research Outcome

[CN]`/speckit.plan` [CN] Phase 1/2[CN] `/speckit.research`[CN]