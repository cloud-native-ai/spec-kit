# Contract: 特性级类别解析（Class Resolution）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：类别语义与取值归 `shared/definitions/flow-class-definitions.md`；降级标签与门禁保持归
`shared/workflow/expression-gates.md` § 调用时机与降级；本契约只登记**键族、记录形态与退出码**。

## 键族

- **C-001** 解析 MUST 复用既有唯一读取引擎 `scripts/python/flow-class-check.py --action lookup`。
  MUST NOT 新增第二份分类数据文件、MUST NOT 新增第二条读取路径、MUST NOT 新建第二个解析函数或第二个脚本入口。(FR-003)

- **C-002** 特性线键 MUST 取 `spec:<spec 目录名>`，其中 `<spec 目录名>` 是该 spec 目录的 basename
  （如 `spec:077-doc-sdd-integration`）。键文法为 `^spec:[a-z0-9][a-z0-9-]*$`。MUST NOT 接受裸目录名，
  MUST NOT 接受含 `/` 的路径形，MUST NOT 以 `feature:<ID>` 为键。(FR-003, FR-007)

- **C-003** 解析位置 MUST 是 `<repo>/.specify/specs/<name>/requirements.md`；`--repo` 指向 `.specify` 自身时
  退化为 `<repo>/specs/<name>`。spec 目录不存在时 MUST 退出码 2，且 MUST NOT 返回任何类别值。(FR-003)

## 记录形态

- **C-004** 键族为 `spec:` 时返回的记录 MUST 与单元键**逐字段同形**：字段集为**九项**——
  `action` / `checked_at` / `unit_id` / `flow_class` / `source` / `marker` / `basis` / `neutral` / `error`，
  MUST NOT 新增第十个字段（`error` 本就是单元键记录的字段，本特性只是让它对 `spec:` 键也有取值：
  `{label, detail}` 或 `null`）。`unit_id` 取键原文、`source` 取 `declaration` 或 `default`、`basis` 为 `null`、
  `neutral` 为 `false`。(FR-003)

- **C-005** 记录的互斥约束 MUST 成立：`source: declaration` 与 `marker: <默认标记>` MUST NOT 同时出现；
  `flow_class: null` 与 `source: default` MUST NOT 同时出现。任一组合出现即第三态缺陷。(FR-003, FR-004)

## 退出码

- **C-006** 退出码 MUST 分三段：**0** = 已解析（含未声明按默认，此时 `marker` 为 069 登记的默认标记；
  `declaration-absent` 亦落此段，作 advisory）；**1** = 已声明但取值不在封闭集内，或声明行形态错误
  （`invalid-class` / `declaration-malformed` / `declaration-duplicate` / `declaration-misplaced`）；
  **2** = 键或输入非法、spec 目录不存在、owner 不可解析（`owner-unavailable`）。1 与 2 MUST NOT 合并。(FR-003, FR-005, FR-009)

- **C-007** 退出码 1 时 `flow_class` MUST 写 `null`，`source` MUST 写 `declaration`。MUST NOT 写
  `flow_class: execution` + `source: default`——那会让只看记录不看退出码的消费方把作者笔误读成一个判定。(FR-005)

- **C-008** 退出码 1 的诊断 MUST 走 stderr，形态为 `<code>: <repo 相对路径>:<行号> carries '<值或形态摘要>', <判据一句话>`，
  使门禁侧可直接转述文件、行号与越界取值，而记录字段集保持不变。(FR-005)

- **C-009** owner 解析 MUST 先于键族匹配：owner 不可解析时，任何键（含 `spec:`）都 MUST 走退出码 2，
  MUST NOT 因键是新族而给出不同的降级标签。**该顺序相对既有引擎是登记变更**：既有 `action_lookup` 先判
  `UNIT_ID_RE` 再 `parse_owner`，因此「键非法 **且** owner 不可解析」这一输入过去报 `invalid-unit-id`、此后报
  `owner-unavailable`；两者同为退出码 2、门禁集不变，差异已登记为 requirements FR-011 的豁免①，MUST NOT 被当成回归，
  也 MUST NOT 被悄悄改回旧顺序。(FR-003, FR-009)

## 与台账、缓存的关系

- **C-010** 特性线声明 MUST NOT 写入 § 逐流程台账。台账行集 MUST 继续等于框架单元清单
  （`templates/commands/*.md` 与 `skills/{external,internal}/*/SKILL.md`）；写入即产生 `unknown` 发现，
  且 `--action check` 的覆盖块 MUST 保持零缺口。(FR-003)

- **C-011** 同一次阶段运行 MUST 只解析一次，结果复用于本阶段全部算子调用；跨阶段 MUST NOT 缓存，
  跨线 MUST NOT 复用。并发场景下类别 MUST 按线解析，MUST NOT 使用进程级、环境级或会话级全局值。(FR-006, FR-007, FR-008)

- **C-012** 解析失败 MUST 打印 `owner-unavailable` 并保持既有执行类门禁集不变；MUST NOT 中断流程、
  MUST NOT 静默切换门禁集、MUST NOT 把降级结果读作通过。该路径 MUST 只覆盖三类输入，每类都有**调用方可观察**的触发：
  ① owner 不可解析；② **调用方无法执行引擎**——触发是「引擎文件不存在」或「操作系统拒绝执行 / 进程未产出记录」，
  此时降级标签与记录 MUST 由**调用方**写下（MUST NOT 用「引擎自己返回退出码 2」描述这一情形）；③ 键或输入非法（退出码 2）。
  降级 MUST 在记录（`error.label`）与派发载荷（`error=<label>`）里可表示，使「降级」与「作者未声明」可区分。(FR-009)
