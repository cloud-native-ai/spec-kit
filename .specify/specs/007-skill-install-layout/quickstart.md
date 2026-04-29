# Quickstart: Skill Install Layout

## Purpose

[CN]“[CN] skills [CN] `.specify/skills/`[CN]”[CN]

## Prerequisites

- [CN]`007-skill-install-layout`
- [CN] skill[CN] `/speckit.skills` [CN]
- [CN]
- [CN]

## Validation Scenarios

### Scenario 1: [CN]P1[CN]

1. [CN] skill [CN]
2. [CN] `.specify/skills/<skill-name>/`[CN]
3. [CN] skill [CN]

**Expected Result**: [CN] `.specify/skills/`[CN] `.github/skills/` [CN]

### Scenario 2: GitHub [CN]P2[CN]

1. [CN] GitHub [CN] skill[CN]
2. [CN] `.github/skills/<skill-name>` [CN]
3. [CN] `.specify/skills/<skill-name>/`[CN]

**Expected Result**: `.github/skills/<skill-name>` [CN]

### Scenario 3: [CN]P2[CN]

1. [CN]
2. [CN]
3. [CN]“[CN]”[CN]

**Expected Result**: [CN] `partial-success`[CN]

### Scenario 4: [CN] + [CN]P3[CN]

1. [CN] `.github/skills/<skill-name>/`[CN]
2. [CN]
3. [CN]

**Expected Result**: [CN] `.specify/skills/<skill-name>/` [CN]

### Scenario 5: [CN]P3[CN]

1. [CN]
2. [CN]
3. [CN]

**Expected Result**: [CN]“[CN]”[CN]

### Scenario 6: [CN]Edge[CN]

1. [CN]
2. [CN]
3. [CN]

**Expected Result**: [CN] `conflict-entry-path` [CN]

### Scenario 7: [CN]Edge[CN]

1. [CN] skill [CN]/[CN]
2. [CN]

**Expected Result**: [CN] `reused` [CN]

## Regression Expectations

## Automated Coverage Mapping

- Scenario 1, Scenario 7 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- Scenario 2, Scenario 3 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- Scenario 4, Scenario 5, Scenario 6 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- [CN] → `tests/unit/test_skills_utils_layout.py`

- [CN] `/speckit.skills` [CN]
- [CN] skill [CN]
- [CN]
- [CN]
