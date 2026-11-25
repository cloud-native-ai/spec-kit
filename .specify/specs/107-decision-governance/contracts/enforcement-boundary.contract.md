# Contract: 强制边界（enforcement-boundary）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**FR 覆盖**: FR-022…FR-025
**载体**: `shared/definitions/decision-definitions.md` § Enforcement Boundary（M/B 两表的 owner）；`scripts/python/validate-decisions.py`（新只读引擎）；`scripts/python/scan-confirmation-gates.py`（不改动，零新增命中）。

本契约规定「哪些规则由程序判、哪些只能由评审承接」，并保证程序的绿不是假绿：每条机器规则有能转红的守卫与逆向样本，每条行为规则有具名承接面。

## 条款

- **C-401** (machine rules, one judge each): the nine machine rules MUST each name exactly one deterministic judge action and one red condition:

  | Rule | Judge (`validate-decisions.py`) | Red condition | Reverse sample |
  |------|----------------------------------|---------------|----------------|
  | M-01 | `--action records` | a missing base-layer field, a conditional-layer field missing while its trigger holds, a class outside the closed set, a `transmission_status` outside its closed domain, a malformed timepoint, or a timepoint contradicting the `transmission_status` phase | `fixtures/m01/*` |
  | M-02 | `--action records` | `same_name_conflict: true` with an empty `resource_locator` or fewer than two named dimensions (the same-name conditional family) | `fixtures/m02/*` |
  | M-03 | `--action records` | empty set, duplicate label, `other` without `path`, a missing option element | `fixtures/m03/*` |
  | M-04 | `--action records` | new-form record (`^### D-\d{3}` heading carrying the record field grammar): `D-NNN` form error, non-dense per carrier, id unresolvable in the register; legacy headings and register rows are never judged | `fixtures/m04/*` |
  | M-05 | `--action chain` | receipt missing, `decision_id` missing or unresolvable | `fixtures/m05/*` |
  | M-06 | `--action payload` | decision-backed dispatch missing the block or a block field | `fixtures/m06/*` |
  | M-07 | `--action chain` | any of the three chain segments missing or ids inconsistent | `fixtures/m07/*` |
  | M-08 | `--action records` | the structured decision subject matches a registered glossary variant whose canonical exists | `fixtures/m08/*` |
  | M-09 | `--action records` | any evidence pointer unresolvable (the referenced carrier path/anchor does not exist or is unreadable) | `fixtures/m09/*` |

  (FR-022)
- **C-402** (behavior rules, named surfaces, never machine-claimed): the six behavior rules MUST each name a review surface — B-01/B-02/B-03/B-06 → `/speckit.review` artifact segment + human decision review; B-04/B-05 → `/speckit.analyze` + `/speckit.review`; documentation and tests MUST NOT claim machine coverage for any of them. (FR-023)
- **C-403** (reverse sample per guard): every machine guard MUST carry a reverse/mutation sample that turns it red; a guard without a reverse sample is a defect; all guards MUST run through the single test entry `scripts/bash/run-tests.sh`. (FR-024)
- **C-404** (checker interface, read-only): the new checker MUST answer `--help` and `--version`, reject undeclared options with a non-zero exit, declare its read-only surface, and use exit `0` = pass / `1` = a documented check failed / `2` = input or argument error. (FR-024, `shared/definitions/script-interface-definitions.md`)
- **C-405** (gate neutrality): the feature MUST NOT add a blocking confirmation gate; `scan-confirmation-gates.py` MUST report zero new hits against the measured baseline (31 blocking gates / 0 violations at `test-evidence/scan-confirmation-gates-baseline.txt`); existing sentinel literals, watcher verdicts/exit codes and the two-slot test budget MUST remain unchanged. (FR-025)
- **C-406** (producer-inventory closure): the checker's `--action inventory` MUST compare the declared producer set (owner page) against the observation set produced by the documented code-face scan command; the verdict MUST be `observed == declared ± exempt`; a producer outside the declaration that yields a decision item MUST turn the guard red. (FR-003, SC-001)
- **C-407** (table–guard parity): the guard roster in the tests and the owner page's two tables MUST be row-identical; a missing row on either side is a defect. (FR-022, FR-023)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-401 | FR-022 | `test_decision_governance_guards.py`（逐 M 行） |
| C-402 | FR-023 | `test_decision_governance_contracts.py::test_behavior_surfaces_named` |
| C-403 | FR-024 | `test_decision_governance_guards.py::test_every_guard_has_reverse_sample` |
| C-404 | FR-024 | `test_script_interface_contract.py` 覆盖新脚本 + `test_validate_decisions.py::test_cli_surface` |
| C-405 | FR-025 | `test_decision_governance_contracts.py::test_gate_neutrality`（含 `scan-confirmation-gates.py` 复扫） |
| C-406 | FR-003, SC-001 | `test_decision_governance_guards.py::test_inventory_closure` |
| C-407 | FR-022, FR-023 | `test_decision_governance_guards.py::test_table_guard_parity` |

## FR 覆盖核对

- FR-022…FR-025 由本文件 C-401…C-407 承接；M/B 的转红条件与承接面与 requirements § Enforcement Boundary 逐行一致。
- 守卫不新增阻塞式确认门控；门禁扫描器的模式集不被扩宽。
