# Feature Reference — 082

**Requirement key**: `082-mechanism-policy-separation`
**Bound Feature**: **Feature 082** — 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance: Mechanism–Policy Separation & Skill Reference Grammar）
**Feature index row**: `.specify/memory/features.md`（行 `| 082 |`；绑定时已在同一趟重算 `Total Features`；scope update clarify 已按裁决把该行改名并追加第二能力段，**绑定不变**）
**Feature detail**: `.specify/memory/features/082.md`
**Binding basis**: `/speckit.clarify` Mode A（2026-11-05）按 `feature-integration.md` § Feature Binding Rules 复核 013／023／032／036／040／047／050／051／052／053／069／077／078／079／081 全部无归属，且无「反复吸收同类工作」的兄弟规格前例 → **新建**。裁决过程见 `requirements.md` § Clarifications § Session 2026-11-05；本文件不重复该论证。

## How this plan maps onto the Feature

| Feature element | This plan's carrier |
|---|---|
| 状态推进 | 本阶段只落 `Draft → Planned`（`plan.md` / `research.md` / `data-model.md` / **4 份 `contracts/`** / `quickstart.md` / 本文件 + 一条无未解释 Fail 的 Constitution Check）；`Implemented` 由 `/speckit.implement` 拥有；本阶段**不改**任何注册表（D9 把 `Last Updated` 更新留给 implement 收口） |
| Key Changes（feature 详情 6 条） | ① 一等原则 + 唯一 owner → `plan.md` § Summary + `contracts/owner-document.contract.md` OD-01…OD-10；② 元技能接线 → `contracts/skill-wiring.contract.md` SW-01…SW-08（SW-05 已按 SU-01 收紧为「机制/策略判定字面零命中」）；③ 消费侧统一提示 → OD-06 + SW-04；④ 可复算的封闭集 → `contracts/guard-and-measurement.contract.md` GM-03…GM-07；⑤ **技能引用唯一 owner**（[[STR-004]] 拥有接受形式 / 归一化顺序 / 消歧 / 失败语义）→ `contracts/skill-reference.contract.md` GR-01…GR-10；⑥ **五消费方只声明参数 + 源路径引用**，归一化结果为命令面／技能标识／失败三值封闭 → GR-01…GR-10 + SR-01…SR-06 + `contracts/guard-and-measurement.contract.md` GM-11…GM-14 |
| Implementation Notes | `plan.md` § Design Decisions **D1–D14**（含被否决的替代方案与 D11–D14 的第二能力落点）与 `data-model.md`（10 实体、34 条校验规则、3 条状态转移） |
| 承重决策 | `plan.md` § Decision Tensions **T-001…T-004**（T-004 = 消费方引用源路径，重开代价是一次跨仓坐标迁移） |
| Related Files | `requirements.md`（FR / SC / STR 的当前计数以 `validate-requirements.py` 实测为准，本文件不手抄）、`checklists/requirements.md`、`test-evidence/`、`research.md` R1–R15 |
| 本特性的自用（dogfooding） | 本特性自己的作者流程就是被它约束的五个元技能之外的流程；其「机制/策略」判定首先落在**自身设计产物**上：`data-model.md` 与 `contracts/` 只写机制（判定形态），策略（路径、落点、样本位置）一律写成参数或运行环境取值 |

## Delivery surface（Feature 行「Last Updated」要报告的内容）

计数口径与 `plan.md` § Phase 1: Design Artifacts Summary 逐项同口径；**单包**（无切片）。

- **新增框架源**（**3**）：① `shared/definitions/mechanism-policy-definitions.md`（机制/策略 owner，[[STR-003]]，镜像到 `.specify/shared/definitions/`）；② `shared/definitions/skill-reference-definitions.md`（技能引用 owner，[[STR-004]]，起点已在工作树、实现期核验定稿后经镜像再生成落地）；③ `skills/external/create-skills/references/mechanism-policy-check.md`（技能自有的判定步骤资源，SW-01，≤ 12 行 + 两类误置的定位方法）。
- **改写框架源**（**9**）：`skills/external/create-skills/SKILL.md`（§ 6 一条 checklist 项 + § 1 引用接线）、`skills/external/improve-skills/SKILL.md`（§ 2 一条调研问题 + § 3 一个候选类别 + Input Contract 引用接线）、`skills/external/improve-skills/references/loop-playbook.md`（批量口径一句）、`skills/external/merge-skills/SKILL.md`（§ 5 后一步 + § 8 一条验证项 + Input Contract 引用接线）、`skills/external/merge-skills/references/provenance-record.md`（层归属写入「how to verify」一栏）、`skills/external/coaching-skills/SKILL.md`（**仅**引用归一化接线，SR-06）、`skills/internal/run-skills/SKILL.md`（**仅**引用归一化接线 + § 1 第 0 步，SR-01；位置阶梯逐字节不变）、`skills/external/coaching-skills/data-model.md`（吸收的 skill-reference 并发改造）、`skills/external/coaching-skills/references/prompt-templates.md`（同上）。
  - **计数口径**（与 `plan.md` § Scale/Scope 同口径，M3 repair 2026-11-05 改正）：本项的 9 = 允许差异集第 1–8 行中**改写类**的 6 条（`create-skills` / `improve-skills` / `merge-skills` 三份 `SKILL.md` + 两份 `references/` + `coaching-skills/SKILL.md`）+ `run-skills/SKILL.md` 1 条 + 2 条吸收的 coaching skill-reference 文件（GM-03 第 19–20 行）；第 2 行（`create-skills/references/mechanism-policy-check.md`）是**新增**、已计入上一项「新增框架源 3」。清单的唯一落点是 `data-model.md` § GM-03 第 1–8 行与 `plan.md` § Source Code 的树；本节只给计数与每项的改动性质，MUST NOT 再手抄一份逐文件清单。
- **新增契约测试**（**11**）：机制/策略 6（`tests/contract/test_mechanism_policy_{owner_doc,ownership,skill_wiring,guard,missing_policy,decidability}.py`）+ 技能引用 5（`tests/contract/test_skill_reference_{grammar,matrix,consumers,command_surface,failures}.py`）。另有 **1 个 test-only 辅助** `tests/contract/skill_reference_matrix.py`（归一化的单一可执行实现，不是 pytest 模块、不是门禁，D11）。
- **矩阵 fixture**（**1**）：`tests/fixtures/skill-reference/normalization-matrix.json`（`tests/fixtures/` 下**第 13 个**按特性命名的夹具目录——新增前实测 12 个，`ls -d tests/fixtures/*/`；既有根下的新子目录、不是新目录根，D13）。
- **计划期义务（登记，不属本特性的代码交付面）**（**3**）：按 glossary 协议在词汇表追加 `机制/策略分离 (Mechanism–Policy Separation)` 一行（Origin `user` / Status `proposed`；**作为共享注册表的登记行，不作为本特性的交付面**）；在框架地图的既有 `definitions/` 行补两份 owner 的文件名（不新增行、不新增目录）；`CHANGELOG.md` 在 implement 收口时记一条。
- **再生成入口**（**2**）：`python3 scripts/python/sync-mirrors.py`、`python3 scripts/python/regen-command-copies.py`（各跑一次，再以 `--check` 判零漂移）。本特性**不改命令模板**，故命令副本预期零变化；`--check` 仍跑，用来证明这一点（SW-06 / SC-008 的命令面标杆）。
- **明确不新增**（**7 类**）：`/speckit.*` 命令、门禁脚本、校验器、环境变量、目录根、第二套分类数据文件、配置键。

**合计 24** = 新增 3 + 改写 9 + 新增测试 11 + 矩阵 fixture 1（test-only 辅助 `tests/contract/skill_reference_matrix.py` 已含在「新增测试 11」的口径内，不另计；M3 repair 2026-11-05 重算，frozen 的 24 字面量已随漂移一并改正）。

## 与既有冻结的关系（实现期必须处理的一条）

五个被改的 `SKILL.md` 在 `tests/contract/test_expression_compatibility.py` 的冻结哈希清单里（清单来源 `.specify/specs/069*/notes/pre-change-file-hashes.txt`）。实现期 MUST 在该模块的 `ALLOWED_POST_BASELINE_CHANGES` 里为 `create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` 各**新增**一行、并把 `run-skills` 的**既有键更新**（不是追加第二行），每行带 `reason` + 改动后必须存在的 `markers`；MUST NOT 改哈希清单本身、MUST NOT 删除或跳过断言（`research.md` § R3 + `plan.md` § D7 的 5 行封闭清单）。

## Slices

**单包交付**（`single-package`）。自然任务计数估计 **≈ 36**，低于 80 的任务上限；FR 侧实测 `fr_count=30` / `fr_ceiling=60`（`decomposition-check.py --mode plan` → `decision=proceed`，逐字见 `plan.md` § Decomposition & Ceiling 与 `test-evidence/plan-scope-update-gates.txt`）。因此**不声明切片、不丢弃任何 FR / SC**；`tasks.md` 是一张约 36 行的清单，按 US1 → US2 → US3 → US4 → US5 的用户故事自然顺序推进（`create-skills` / `improve-skills` / `merge-skills` 三份 `SKILL.md` 同时承载机制/策略判定与引用接线，**一次改写两处落点**，不排两遍）。

**切片结论已撤销**：早先的 `082a` / `082b` 两切片写于 FR 上限仍为 30、`30 == 30` 零余量时；预算校准把上限提到 60 后该唯一前提消失（clarify 裁决 ③），`plan.md` 与本节同趟改为单包（见 `plan.md` § Scope Update Record 的 SU-04）。**回退条件**：若 `/speckit.tasks` 的分解检查给出 `split-required`，按用户故事自然顺序切片，且两次切片的 FR 集必须**互斥且并集为全集**——而不是压缩任务粒度。

## Overlap 注记（与 059 / 062 / 063 的历史交付面）

- `.specify/memory/glossary.md` 的**协议源** `shared/workflow/glossary.md` **不是**本特性的交付面：082 只按 glossary 协议新增一行词条，把它当共享只读注册表，交付声明不把它列入「改写框架源」清单。`overlap-check.py` 因此仍会报 029 / 044 / 051 对它各一条同路径重叠——**这是如实残留，不是本条被撤销**：记录该裁决本身必须点名此文件，而 `overlap-check.py` 的声明扫描按 token 识别路径，故它仍会出现在 `current_paths` 中。本行因此**不**声称「已从交付声明移除该 token」；裁决按状态脊 § Overlap adjudication 原样保留、复跑结果如实登记于 `test-evidence/plan-scope-update-gates.txt` § G4-adjudication。
- `skills/external/{create-skills,improve-skills,merge-skills}/SKILL.md` **是**本特性的真实交付面（`data-model.md` § GM-03 第 1 / 3 / 5 行）。059 / 062 / 063 对这三个路径的历史重叠均属**已完成**特性，按状态脊 § Overlap adjudication 原样记录：082 是当前活动写线，无并发写线，MUST NOT 为追求 `clear` 删掉真实交付路径、MUST NOT 改历史 spec、MUST NOT 伪造「无重叠」声明。
- 不变量：无第二条活动写线写这些路径；若出现并发写线，按状态脊的裁决流程重判，而不是就地删路径。
