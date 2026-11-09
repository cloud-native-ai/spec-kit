# Checkpoint 01 — requirements

## 1. Artifact verification

- sentinel: `REQUIREMENTS-DONE`
- U4: pass — `test-evidence/requirements-gates.txt`；驱动者独立复跑 `validate-requirements.py`（ok，303 行，0 error / 0 warning）、`pre-analyze-check --stage requirements`（pass，0 advisories）、`decomposition-check --mode plan`（proceed，23/60）
- artifacts: `.specify/specs/089-script-interface-contract/requirements.md`、`checklists/requirements.md`、`test-evidence/requirements-gates.txt`、`.specify/memory/features/086.md`、`.specify/memory/features.md`（086 行）
- commits: `27b8080d`、`5b470835`、`19f53dd2`
- wrap-up: 执行者未产出记账，驱动者已补跑 run-determination / exec-quant / feedback（unit-id `/speckit.requirements`，run-id `r20261106T090000Z-086a`，feature `089-script-interface-contract`）
- anomaly: `ANOMALY: refresh-tools.sh 实测已有 --help（简报基线错误，已在 Assumptions A2 更正）`；`ANOMALY: 事故的 +70/-0 diff 在 git 历史中不可复核（SC-002 已改写为自包含哈希实验）`

## 2. Temporary Goal progress

- goal: `.specify/specs/089-script-interface-contract/goal/script-interface-contract/goal.md`（spec-local，引擎写入）

| criterion | degree | evidence_ptr |
|---|---|---|
| 适用脚本的 -h/--help/--version 全部成功退出、输出非空，执行前后工作树零差异 | not_evaluated | `.specify/specs/089-script-interface-contract/test-evidence/requirements-gates.txt`（基线实测：14 bash 中 6 无 help；38 python 中 36 无 version） |
| 契约检查对全部候选给出判定，违规计数为 0，豁免成员逐条带机械判据证据 | not_evaluated | 契约检查尚未交付（implement 阶段） |
| 干净下游项目经初始化后，宪法含该原则、instructions.md 含对应常驻段落 | not_evaluated | 尚未落地模板（implement 阶段） |

## 3. Team configuration review

- evidence: n/a — Temporary Team 在 clarify + plan U4 通过后创建（085 规则），本 checkpoint 时尚不存在
- symptom: n/a
- proposal: none
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- requested: 24; effective: 1; reason: clarify 是单分析器阶段，无可并行 package
- stage max_parallel: 1; verifier reserve: 2
- roster: SDD Clarify Analyzer ×1
