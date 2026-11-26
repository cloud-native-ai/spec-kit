# Contract: 决策文本与选项集（text-and-options）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**FR 覆盖**: FR-006…FR-013
**载体**: `shared/definitions/decision-definitions.md`（owner page）；消费面 = instruction 段、决策项模板、守卫与评审承接面。owner page 的 `.specify/` 镜像随镜像检查落地。

本契约规定「一个决策项必须长什么样」：类别先行，文本按类强调，选项必须封闭可比较。判「文本是否足够完整/定位是否足够区分」是行为类（B-01/B-02），本契约只规定可机械判定的形态与在场性。

## 条款

- **C-101** (class declaration, closed set): every decision item MUST declare exactly one `decision_class` value from the closed set `human-interactive` / `ai-autonomous`; a missing class, a mixed class or a value outside the set is a defect; the class decides which template and which check set applies. (FR-006, FR-011)
- **C-102** (full-name minimum bar): the decision subject and every option label MUST use the full name of the object, MUST NOT use an abbreviation alone; this rule and C-103 are a **minimum bar** and MUST land on four surfaces together — the owner page, the instruction section, the decision-item templates and the guards/review surfaces — not in the instruction template alone. (FR-007, FR-010)
- **C-103** (same-name locator): when a same-name conflict is possible, the decision item MUST declare `same_name_conflict: true` and MUST carry a machine-parseable `resource_locator` whose named dimensions include at least the business resource group + region id pair; a same-name object MUST NOT be presented without a locator; declaring `false` to bypass the locator is a defect, not an exemption (B-02 owns the adequacy judgement). (FR-007)
- **C-104** (human-interactive template): a `human-interactive` item MUST prioritize readability — plain language, context, each option's consequences and reversibility, the default option, full names and locator; wording and context MUST follow `shared/guidelines/user-facing-comprehension.md`; a bare formal predicate without explanation is a defect on B-03's review surface. (FR-008, FR-011)
- **C-105** (ai-autonomous template): an `ai-autonomous` item MUST prioritize rigor — closed option set, an explicit decision predicate/rule, explicit assumptions, machine-checkable evidence pointers, a deterministic conclusion and a reopening condition; prose without a decision rule is a defect on B-04's review surface. (FR-009, FR-011)
- **C-106** (option-set closure): options MUST form a closed, enumerable set with a declared count (0/1 degenerate cases included); every option MUST carry all five elements — `label`, `consequences`, `reversibility`, `default` marker, `evidence`; labels MUST be unique; an option named `other` is legal only with a `path` declaring who/when/how may add options and write the record back; an empty option set is not a decision item; a single viable option MUST declare `forced` with a reason. (FR-012)
- **C-107** (chosen member and replayability): `chosen_option` MUST be one named member of the option set; for an `ai-autonomous` decision, replaying the recorded inputs with the recorded decision predicate MUST deterministically re-derive the chosen option, and a replay mismatch is a defect. (FR-013)
- **C-108** (human choice signal): a `human-interactive` decision MUST record the human's choice signal using the existing vocabulary of the gate-observation protocol owned by `shared/guidelines/confirmation-gates.md`; this contract reaches that vocabulary by pointer and MUST NOT restate it. (FR-013)
- **C-109** (presentation/class mismatch): a class whose presentation lacks its class's elements MUST be reported by the named review surface (B-03 / B-04); a mis-chosen class is B-06; none of the three may be claimed as machine-covered. (FR-011, FR-023)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-101 | FR-006, FR-011 | `test_decision_governance_contracts.py::test_class_declaration_closed` |
| C-102 | FR-007, FR-010 | `test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces` |
| C-103 | FR-007 | `test_decision_governance_guards.py::test_m02_locator_red_then_green` |
| C-104 | FR-008, FR-011 | `test_decision_governance_contracts.py::test_human_template_elements` |
| C-105 | FR-009, FR-011 | `test_decision_governance_contracts.py::test_ai_template_elements` |
| C-106 | FR-012 | `test_validate_decisions.py::test_m03_option_set_reverse_samples` |
| C-107 | FR-013 | `test_validate_decisions.py::test_ai_replay_deterministic` |
| C-108 | FR-013 | `test_decision_governance_contracts.py::test_human_signal_pointer_only` |
| C-109 | FR-011, FR-023 | `test_decision_governance_contracts.py::test_review_surfaces_named` |

## FR 覆盖核对

- FR-006…FR-013 由本文件 C-101…C-109 承接；可转红判据见 `enforcement-boundary.contract.md` 的 M-02 / M-03 / M-08 与 B-01…B-07 行。
- 类别的**选错**（B-06）与名称/定位的**充分性**（B-01/B-02）是行为类，本契约不声称机器覆盖。
