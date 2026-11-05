# Contract — 元技能与命令面的接线条款（Meta-skill Wiring）

**Status**: designed（本阶段）；由 `/speckit.implement` 落地
**判据 owner**: `shared/definitions/mechanism-policy-definitions.md`（下称「owner」）。本契约是**接线图**：哪一面在第几步加哪一种判定，以及哪些面 MUST NOT 动。

## 接线形态（所有条款共用）

- 一条判定 = **一行判定语 + 一个 owner 路径引用**（C5 / FR-015）。判定语 MUST 是可执行的问句或命令式动作，MUST NOT 复述 owner 的判据表、症状表或提示骨架。
- 位置 MUST 在元技能**既有**的校验/调研步骤之内；MUST NOT 新增步骤编号、MUST NOT 新增独立门禁、MUST NOT 新增脚本（A5 / A6 / C8）。
- 判定 MUST **可定位**：点名文件 + 位置（行号或章节 + 引文），MUST NOT 只给结论（FR-012）。
- 判定 MUST 有**通过分支**：正确分层时必须给出「通过」且不要求作者补充内容（US1 场景 3）；没有通过分支的判定会退化成永远要改的噪声。

## SW-01 — `create-skills` § 6 Validate the Skill

- 在 § 6 的 `Minimum checks` 清单**末行之后**追加**一条** checklist 项，标识 MUST 含字面 `Mechanism / policy separation`。
- 该项 MUST 包含：① 一句判定（正文/`references/` 是否把运行环境路径或目录名固化为机制；可复用逻辑是否落在运行环境说明里）；② 一个短锚点，指向 `./references/mechanism-policy-check.md`（本技能自有资源）；③ 一个 owner 路径引用。
- 该项 MUST NOT 内联判据表或症状全表；允许的最大内联是**两类误置各一个关键词短语**（如「environment path」「reusable logic」），超出即视为复制（FR-015）。
- `./references/mechanism-policy-check.md` MUST 存在且只含：判定步骤（≤ 12 行）、两类误置的**定位方法**（如何 grep、如何读引文）、改正方向的两条类别、owner 路径。MUST NOT 重写 owner 的症状表。
- 作者态判定 MUST 同时判**两侧**：只判策略侧误置（最常见的绝对路径）而漏机制侧误置，不满足 US1 场景 2。

## SW-02 — `improve-skills` § 2 调研 / § 3 候选清单

- § 2（调研实现）末尾追加一条**调研问题**：把被引用的运行环境文件（输入/输出/配置/目标目录）与技能正文一起读，并回答「策略在哪里取值」。
- § 3（候选清单冻结）在候选类别里 MUST 追加一项 `policy source missing or ambiguous`，并 MUST 明写：冻结前提出、冻结后不得新增（existing freeze discipline 不变）。
- 该候选 MUST 携带 FR-013 的禁止项：**MUST NOT** 把技能里现存的硬编码值当作默认策略继承；改进方向是「让策略在运行时由用户/环境提供」。
- 批量模式（用户点名一组技能）MUST 以**一次**批口径执行该判定，MUST NOT 对每个技能重复。落点：`./references/loop-playbook.md` 的批量小节追加一条说明，正文只留指针。

## SW-03 — `merge-skills` § 5 覆盖证明 / § 8 校验

- § 5（no-loss gate）之后 MUST 追加一步前置判断：合并**是否改变了两层的分布**——源技能的机制内容进入目标技能资产（预期）、源技能携带的策略绑定进入目标正文（须改为策略侧表达）。
- `./references/provenance-record.md` 的能力行 MUST 允许（不强制新增列）在「how to verify」一栏写出该行的层归属判定；MUST NOT 新增第二个记录表。
- § 8（验证清单）追加一条：合并后的目标 MUST 在 `skill-shape.py` 与 `redline-check.py` 之外，仍通过 `create-skills` § 6 的机制/策略项——复用已有判定，MUST NOT 复制一份。

## SW-04 — 消费侧：副作用之前的双输入检查

- 消费侧义务的**唯一形态**在 owner § Consumption Contract；元技能与元命令 MUST 以路径引用它，MUST NOT 各自写提示语（FR-005–FR-008）。
- 接线点 MUST 落在「即将执行副作用」的那一步**之前**：`create-skills` 是 § 2 的 writability pre-flight 与 § 7/§ 8 的写入之前；`improve-skills` 是 § 7 的编辑之前；`merge-skills` 是 § 7 的 decommission 之前（破坏性动作）。
- 检查 MUST 是**读-判-停**三步，检查本身 MUST NOT 写入任何路径（含创建目录、写临时文件）；缺策略时 MUST 停在原地，不留半成品。
- 「策略缺失」与「环境错误」的措辞 MUST 可区分（FR-007），且判定 MUST NOT 把环境错误报成策略缺失。

## SW-05 — `coaching-skills` 与 `run-skills`：机制/策略判定零加载（`excluded` 成员）

> **按 SU-01 收紧（2026-11-05，scope update）**。原文「正文零改动 + 以基线逐字节比较」在第二个能力并入后自相矛盾：FR-026 点名五个消费方含这两者，而引用归一化接线必然改这两份文件。**谓词未被翻转**——C1 判的是「要不要加载机制/策略判定」，从不判「文件能否被另一条 FR 改」。收窄后的可判形态如下。

- 两者的**机制/策略侧** MUST 零加载：`SKILL.md` 与 `references/` 中 MUST NOT 出现判据句、误置症状、失败表行或 owner 引用（字面零命中：`mechanism-policy-definitions`、`Mechanism / policy separation`、`mechanism-in-policy`、`policy-in-mechanism`）。
- 两者**允许**的改动只有两种：① 引用坐标改写（`SR-01` / `SR-06`，把镜像路径改为源路径）；② 一行「按 owner 归一化并披露」的接线句（MUST NOT 自述归一化顺序，见 FR-019 唯一 owner）。
- 排除理由 MUST 只写在 owner 成员表行里（FR-014 / A7），MUST NOT 在技能正文里复述。
- 守卫形态：不再用逐字节相等（该断言对第 7、8 号允许路径失效），改为 **① 机制/策略字面零命中（grep 级，可复算）+ ② 与基线的差异行必须全部落在上述两种允许改动内**（`test_mechanism_policy_guard.py` 断言 ①，`test_skill_reference_consumers.py` 断言 ② 的一半——接线条数与源路径口径，见 `contracts/skill-reference.contract.md` SR-01 / SR-06 与 GM-11 / GM-12）。

## SW-06 — `/speckit.skills` 命令面

- `templates/commands/skills.md` MUST **不改**（A7 / FR-011 的「不新增命令」；该模板的 Routing 表已经转发给三个纳入的元技能，接线位在 owner 成员表声明）。
- 若实现期发现该模板必须改（例如转发目标消失），MUST 停下并在计划中记录，MUST NOT 静默改（本特性对命令面零改动是 SC-003 的一部分）。

## SW-07 — 不新增机器

- 本特性 MUST NOT 新增：`/speckit.*` 命令、独立门禁脚本、第二套清单、第二个分类数据文件、环境变量、目录根（A5 / A6 / C8 / FR-016）。
- 任何「为判定新增一个 checker」的冲动 MUST 先回答：判定是否需要模型判断？需要 → 落在元技能步骤里（本契约）；不需要且已在别处有确定性载体 → 接线到既有载体。本特性两条都不是，故零新脚本（D2）。

## SW-08 — 镜像义务

- **两份 owner 文档**（`shared/definitions/mechanism-policy-definitions.md` 与 `shared/definitions/skill-reference-definitions.md`）与**五个消费方**的 `SKILL.md`（`create-skills`、`improve-skills`、`merge-skills`、`coaching-skills`、`run-skills`）以及 `create-skills` 的 `references/mechanism-policy-check.md` MUST 先改框架源（`skills/…`、`shared/…`），再经 `python3 scripts/python/sync-mirrors.py` 落到 `.specify/…`；MUST NOT 手改镜像（FR-028）。
- 同一提交内 MUST 跑 `--check` 并记录输出（判据是「无新增漂移」，基线已在 `test-evidence/plan2026-11-05-baseline.txt` 实测；本阶段复跑为 `shared/ == .specify/shared/ (63 files)`、全项 ok）。
- **覆盖面自 3 份扩到 5 份 + 2 份 owner**：`coaching-skills` 与 `run-skills` 的引用坐标改写（SR-01 / SR-06）同样 MUST 走再生成，MUST NOT 只改源而让镜像落后——这正是 EP-007(b) 的判别点。
- 引用坐标口径：消费方引用**框架源路径**（`shared/definitions/skill-reference-definitions.md`），MUST NOT 引用镜像路径（T-004 / SU-02）；镜像继续由脚本生成，`--check` 只证明一致，不把镜像变成被引用坐标。

## 可追溯性

| FR / SC | 条款 | 测试载体 |
|---|---|---|
| FR-008 | SW-04 | `tests/contract/test_mechanism_policy_skill_wiring.py` |
| FR-009 | SW-01, SW-02 | 同上 |
| FR-011 | SW-05, SW-06, SW-07 | 同上 + `tests/contract/test_mechanism_policy_guard.py` |
| FR-012 | SW-01 | `tests/contract/test_mechanism_policy_skill_wiring.py` |
| FR-013 | SW-02 | 同上 |
| FR-014 | SW-03, SW-05 | 同上 |
| FR-016 | SW-07 | `tests/contract/test_mechanism_policy_guard.py` |
| SC-002 | SW-01, SW-02 | `test-evidence/sc-002-*.txt`（宿主实录） |
| SC-004 | SW-04 | `tests/contract/test_mechanism_policy_missing_policy.py` |

**跨能力行**：FR-026（五个消费方接线）与 SC-007 的接线断言落在 `contracts/skill-reference.contract.md` 的 SR-01…SR-06；本文件的 SW-05 只陈述**机制/策略侧的收紧形态**，两者 MUST NOT 互相替代（C9）。
