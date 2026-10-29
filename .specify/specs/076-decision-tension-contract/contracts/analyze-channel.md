# Contract: 分析结构通道（analyze-channel）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-011…FR-014
**载体**: `skills/internal/analyze-artifacts/references/detection-and-severity.md`、`skills/internal/analyze-artifacts/SKILL.md`（各含 `.specify/` 镜像）

本契约把一个**结构**通道加到既有检测面：它判「记录是否成立」，不判「决策是否正确」。
这一区分是严重度的来源——结构缺陷必然被下游继承（计划 → 任务 / 实现），语义分歧则不会。

## 条款

- **C-1** (single judged object, fixed scope): the channel MUST judge exactly one artifact — the `plan.md` under the `REQUIREMENTS_DIR` resolved by the prerequisite script — and MUST NOT open any other feature directory's `plan.md`; `requirements.md` in the same directory is a mapping reference, never a second judged object; in-scope historical plans written before this contract MUST NOT be exempted, while out-of-scope plans produce no finding at all. (FR-011)
- **C-2** (three defect classes, fail-closed, no advisory tier): the channel MUST judge three classes and assign each HIGH — a missing `## Decision Tensions` section or a bare `N/A` without one justification line per trigger (both read as 「no record」), any record with a missing or empty field including a single-pole `binding_constraints`, and an `expected_sacrifice` that does not resolve to a declared measurement source; the detector MUST NOT be asked to decide whether the plan contains a load-bearing decision, the value domain MUST be HIGH or 0 with no advisory or downgrade tier, and when `requirements.md` has no measurement-source section the outcome MUST branch mechanically on the record count — one or more records fail mapping one by one, a compliant `N/A` with zero records produces zero findings. (FR-011)
- **C-3** (severity from the propagation surface): the channel's severity MUST use the existing propagation-surface criterion owned by `.specify/shared/workflow/objective-analysis-gate.md` — no new severity level, score or maturity verdict — and every finding MUST name its propagation surface as the first field, namely the plan flowing into tasks and implementation. (FR-012)
- **C-4** (deterministic verdicts): every mechanically decidable part of the judgement — field presence, enumerated values, reference resolution — MUST be executed by a program under `scripts/python/` that prints the verdict, and the model MUST consume that verdict rather than score the record semantically. (FR-013)
- **C-5** (placement and declared allowed delta): the channel MUST live inside `detection-and-severity.md` beside the existing channels, added under an only-add containment claim whose baseline referent is commit `ac63fe8c` and whose comparison unit is 「existing paragraph / new paragraph」; for that file the allowed delta set is exactly the new channel section plus the one count line the new channel forces to change (its `## The seven passes` heading), and everything outside that set MUST be byte-identical to the baseline with zero deleted or rewritten lines. `SKILL.md` is edited separately: its pass-enumeration sentence gains the new channel so the two enumerations cannot drift, and that edit is declared here as a pointer update outside the containment claim — the closed surfaces are the two files FR-026 names, and `SKILL.md` carries no closed set. The contract test MUST enumerate the actual diff lines of both files and compare each against its own declared set. (FR-014)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-011 | test_channel_scope_is_one_plan_artifact |
| C-2 | FR-011 | test_three_defect_classes_fail_closed_no_advisory |
| C-3 | FR-012 | test_severity_follows_propagation_surface |
| C-4 | FR-013 | test_verdicts_come_from_the_program |
| C-5 | FR-014 | test_channel_only_add_allowed_delta_enumeration |

## FR 覆盖核对

- FR-011…FR-014 由本文件 C-1…C-5 承接；通道的封闭标签面与退出码见 `validator.md`。
- 既有通道（A–G）与 checklist 通道（H）的判据不被本契约改动；C-5 的零删除条款即该不变量的机器表达。
