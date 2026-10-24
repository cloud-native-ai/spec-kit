# Decomposition Gate Record — Feature 069

**Date**: 2026-10-24
**Gate**: plan 入口（requirements U4 后、plan 派发前）
**Owner rule**: `.specify/skills/sdd-loop-driver/references/efficiency-model.md` §5（框架源：`skills/external/sdd-loop-driver/references/efficiency-model.md`）
**Base commit**: `5183bd8f`（分支 `069-execution-expression-sdd`）

## Measurement

```text
python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py \
  --mode plan \
  --requirements .specify/specs/069-execution-expression-sdd/requirements.md
```

Result: `split-required` (exit 1)

```json
{"mode": "plan", "decision": "split-required", "measured": {"fr_count": 41, "task_count": null, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": ["FR definitions=41 exceeds ceiling 30"], "checked_at": "2026-10-24T12:02:47Z"}
```

Success Criteria measured on the same artifact: 13 条（`^- \*\*SC-\d{3}\*\*:` 定义行；`- **SC-NNN Source**` 度量来源行不计）。

## Measured / Reason / Ceilings

| 项 | 值 | 来源 |
|----|-----|------|
| `measured.fr_count` | 41 | `decomposition-check.py --mode plan`（2026-10-24 实跑） |
| `measured.task_count` | `null`（plan 入口不读 tasks） | 同上 |
| SC 定义行 | 13 | 同 artifact 定义行计数 |
| `ceilings.fr_ceiling` | 30 | 脚本 `FR_CEILING` 常量（owner：`efficiency-model.md` §5.1） |
| `ceilings.task_ceiling` | 40 | 脚本 `TASK_CEILING` 常量（同上） |
| `reasons[]` | `FR definitions=41 exceeds ceiling 30` | 脚本输出原文 |

## Confirmation

- **2026-10-24**：用户确认采用**两片**方案（原文选项：「两片（推荐）」）。拆分是**范围决策**，不是需求删除/合并/重排（§5.3.4）。
- 确认对象是切片定义（名称 + 父 FR 范围）；两片的具体规格由切片各自的 requirements 阶段产出。

## Proposed slices（已确认）

| Slice | 名称 | 父 FR 范围 | 条数 | 题眼 |
|-------|------|-----------|------|------|
| 069a | `069a-flow-classification-docs-gates` | 编号 001–017、023–032 | 27 | 分类本体 + 阶段/门禁关系 + 六面文档型门禁 + 表达类首批成员 |
| 069b | `069b-isomorphism-migration-metrics` | 编号 018–022、033–041 | 14 | 同构映射与边界 + 迁移兼容 + 落地口径与度量仪器 |

两片均落在 §5.3.2 的 8–30 FR 区间内（27 / 14）；`proposed_slices[]` 的 FR 范围即父 requirements 的编号区间，编号间隙属切片结果，不改写父条目。

## Slice numbering rule（切片编号规则）

- **切片内连续编号**：每个切片的 `requirements.md` 使用自己的连续 ID 空间（069a = FR-001–FR-027、SC-001–SC-008），因为 `validate-requirements.py` 的 `id-contiguous` 把任何编号缺口判为「行被删除或从未写」，父编号区间在切片内必然留缺口、无法机器绿。
- **父映射表**：切片目录 `notes/parent-fr-mapping.md` 逐条记录「切片 ID → 父 ID → 主题」；父编号只出现在该表与切片的来源说明中，切片正文的交叉引用一律用切片本地 ID。
- **父仍是权威**：父 `requirements.md` 的 41 条 FR / 13 条 SC 定义不变，仍是唯一规范来源；切片编号只是对父条目的投影，编号变化不构成删除、合并或重排。
- **范围不变**：`proposed_slices` 的父 FR 范围与条数不变——069a = 27 FR（编号 001–017、023–032）、069b = 14 FR（编号 018–022、033–041）。

## Scope consequences（可审计，不是遗漏）

1. **SC 归属**：`069a` 只声明由本片 FR 直接支撑的 8 条 SC（编号 001–006、008、010）；编号 007、009、011、012、013 归 `069b`——它们的规范来源分别是同构映射行标注、旧项目升级回归、台账双注入可区分性、混合 oracle 归属、六面门禁 owner 指针，对应父 FR 编号 018–022、033–035、037、038、040，全部落在 069b 区间。
2. **落地口径 FR 全在 069b**：分类所有者的文件落点（编号 036）、台账形态与反空真下限（037）、混合 oracle 一律取 `execution`（038）、命令↔委托技能的机械核验（039）、六面门禁 owner 指针（040）、三项基线的仪器与 not-evaluated 降级（041）均由 `069b` 承接。069a 因此只以「唯一所有者 / 台账 / 决定论对账」的抽象要求出现，不复制其落地形态。
3. **未采纳的替代切法**：若要求 069a 也覆盖「台账注入 / 混合 oracle / 六面门禁 owner」三项 SC，可把编号 037、038、040 移入 069a——069a 将达 **30 条**（仍在 30 上限内），069b 降为 11 条（仍在 8 下限之上）。该切法会改变已确认的范围，**本次不执行**；需用户裁决后才可重写切片范围。
4. **069b 规格未创建**：本次只落 069a 的 requirements 与本记录，`069b-isomorphism-migration-metrics` 目录不存在、不预建。

## Boundary checks

- 上限只约束单特性规模，不评价内容质量（§5.4）；切片仍受测试预算、plan 约束与全部质量门约束，拆分不降低任何门。
- 父 `requirements.md` 的 41 条 FR / 13 条 SC 定义未被本记录修改；编号间隙不是删除、合并或重排。

## Re-run

切片交付前按片重跑本门：`decomposition-check.py --mode plan --requirements .specify/specs/<slice>/requirements.md` 必须返回 `proceed`；切片规格的 FR 行数实测为 069a = 27、069b = 14。
