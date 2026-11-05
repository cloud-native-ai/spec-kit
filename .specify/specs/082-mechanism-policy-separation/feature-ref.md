# Feature Reference — 082

**Requirement key**: `082-mechanism-policy-separation`
**Bound Feature**: **Feature 082** — 机制/策略分离（Mechanism–Policy Separation）
**Feature index row**: `.specify/memory/features.md`（行 `| 082 |`；绑定时已在同一趟重算 `Total Features`）
**Feature detail**: `.specify/memory/features/082.md`
**Binding basis**: `/speckit.clarify` Mode A（2026-11-05）按 `feature-integration.md` § Feature Binding Rules 复核 013／023／032／036／040／047／050／051／052／053／069／077／078／079／081 全部无归属，且无「反复吸收同类工作」的兄弟规格前例 → **新建**。裁决过程见 `requirements.md` § Clarifications § Session 2026-11-05；本文件不重复该论证。

## How this plan maps onto the Feature

| Feature element | This plan's carrier |
|---|---|
| 状态推进 | 本阶段只落 `Draft → Planned`（`plan.md` / `research.md` / `data-model.md` / `contracts/` 3 份 / `quickstart.md` / 本文件 + 一条无未解释 Fail 的 Constitution Check）；`Implemented` 由 `/speckit.implement` 拥有 |
| Key Changes（feature 详情 4 条） | ① 一等原则 + 唯一 owner → `plan.md` § Summary + `contracts/owner-document.contract.md` OD-01…OD-10；② 元技能接线 → `contracts/skill-wiring.contract.md` SW-01…SW-06；③ 消费侧统一提示 → OD-06 + SW-04；④ 可复算的封闭集 → `contracts/guard-and-measurement.contract.md` GM-03…GM-09 |
| Implementation Notes | `plan.md` § Design Decisions D1–D10（含被否决的替代方案）与 `data-model.md`（实体、字段域、两条状态转移） |
| Related Files | `requirements.md`（18 FR / 5 SC / 3 STR）、`checklists/requirements.md`、`test-evidence/`、`research.md` R1–R9 |
| 本特性的自用（dogfooding） | 本特性自己的作者流程就是被它约束的三个元技能之外的流程；其「机制/策略」判定首先落在**自身设计产物**上：`data-model.md` 与 `contracts/` 只写机制（判定形态），策略（路径、落点、样本位置）一律写成参数或运行环境取值 |

## Delivery surface（Feature 行「Last Updated」要报告的内容）

- **新增框架源**（1）：`shared/definitions/mechanism-policy-definitions.md`（owner 文档，镜像到 `.specify/shared/definitions/`）。
- **新增技能自有资源**（1）：`skills/external/create-skills/references/mechanism-policy-check.md`（SW-01 的判定步骤，≤ 12 行 + 定位方法）。
- **改写框架源**（5）：`skills/external/create-skills/SKILL.md`（§ 6 一条 checklist 项）、`skills/external/improve-skills/SKILL.md`（§ 2 一条调研问题 + § 3 一个候选类别）、`skills/external/improve-skills/references/loop-playbook.md`（批量口径一句）、`skills/external/merge-skills/SKILL.md`（§ 5 后一步 + § 8 一条验证项）、`skills/external/merge-skills/references/provenance-record.md`（层归属写入「how to verify」一栏）。
- **新增契约测试**（6）：`tests/contract/test_mechanism_policy_{owner_doc,ownership,skill_wiring,guard,missing_policy,decidability}.py`。
- **计划期义务（登记，不属本特性的代码交付面）**：`.specify/memory/glossary.md` 新增词条 `机制/策略分离 (Mechanism–Policy Separation)`（Origin `user` / Status `proposed`，按 `shared/workflow/glossary.md` 协议），`.specify/shared/definitions/framework-map.md` 新增 owner 文档行（既有目录，非新目录树），`CHANGELOG.md` 在 implement 收口时记一条。
- **再生成入口**（2）：`python3 scripts/python/sync-mirrors.py`、`python3 scripts/python/regen-command-copies.py`（各跑一次，再以 `--check` 判零漂移）。本特性**不改命令模板**，故命令副本预期零变化；`--check` 仍跑，用来证明这一点。
- **明确不新增**：`/speckit.*` 命令、门禁脚本、校验器、环境变量、目录根、第二套分类数据文件、配置键。

## 与既有冻结的关系（实现期必须处理的一条）

三个被改的 `SKILL.md` 在 `tests/contract/test_expression_compatibility.py` 的冻结哈希清单里（`.specify/specs/069*/notes/pre-change-file-hashes.txt`）。实现期 MUST 在该模块的 `ALLOWED_POST_BASELINE_CHANGES` 里为每个被改文件追加一行（`reason` + 改动后必须存在的 `markers`），MUST NOT 改哈希清单本身、MUST NOT 删除或跳过断言（`research.md` § R3）。

## Slices

自然任务计数估计 **≈ 21**，低于 40 的上限，因此**单包交付**（`single-package`，理由见 `plan.md` § Design Decisions D10）。主用户故事按「owner 文档 → 接线 → 守护」的自然顺序推进：US1（作者侧拦误置）与 US4（成员裁定）先落 owner 文档与成员表，US2（改进对账）与 US3（消费侧提示）落在同一批技能接线里；无 FR / SC 被切片丢弃。
