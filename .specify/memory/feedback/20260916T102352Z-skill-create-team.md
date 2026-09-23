---
id: "20260916T102352Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "20260916T102026Z-speckit-team-run-draw-two-layer-structure-2"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-two-layer-structure"
disposition: "processed"
partial: false
created: "2026-09-16T10:23:52Z"
summary: "serial 链第 2 次 run:S1a 与 S1c 并发派发双双 PASS(产物 150 行/21618 字节、179 行/25547 字节,0 UNCLEAR),证明上轮改的目录级粒度有效;S1b 撞 15 轮上限只落 10 行桩、gate 五条全不过 → escalate,S1d/S1e/S2/S3 保持 locked,canonical 零改动。诊断:S1b 的技能比 S1a 更轻(52"
introspection_ref: "introspection-20260923T120035Z#F-16"
disposition_reason: "introspection:introspection-20260923T120035Z#F-16"
---

## Review
serial 链第 2 次 run:S1a 与 S1c 并发派发双双 PASS(产物 150 行/21618 字节、179 行/25547 字节,0 UNCLEAR),证明上轮改的目录级粒度有效;S1b 撞 15 轮上限只落 10 行桩、gate 五条全不过 → escalate,S1d/S1e/S2/S3 保持 locked,canonical 零改动。诊断:S1b 的技能比 S1a 更轻(52 文件/6 目录 vs 60 文件/8 目录)却失败,差异在我往同一 stage 里混了两种任务类型——attribution 与 reconciliation(6 对漂移 guide/ 的章节级合并裁定)+ 消化 21.6KB 上游产物。修法是把合并裁定移入 S1d(其定义本就写着「落地 S1b 的 guide/ 合并裁定」),不是再拆细目录。另两条:增量落盘作为 brief 指令不可靠(S1b 自述已完成的 document/ 分类从未落盘、全损;S1a/S1c 遵守了),应升格为可程序判定的 gate 条件;覆盖型 gate 只检得出「没判定」检不出「判定错」,需强制整批判定附实读证据(本次靠这条纪律才发现 echarts 并不干净、mermaid document/ 有 5 个引擎无关文件)。S1b 尚余 1 次 retry,Meta 判定盲目重试预测仍败且修好需移动球门,故不擅自消耗,改为 escalate。

## Optimization Points
- # /speckit.team run 优化点（draw-two-layer-structure 第 2 次 run，2026-09-16T102026Z）
- **[stage 设计] 一个 stage 里混了两种任务类型：attribution 与 reconciliation，而两者预算量级不同。**
- 本次对照数据（确定性，非估算）：S1a 覆盖 60 文件的技能、S1c 覆盖 47 文件 / 3 技能，
- **都在 15 轮预算内正常完成**（产物 150 行 / 21618 字节、179 行 / 25547 字节，0 个 UNCLEAR）——
- 证明上一轮改的「目录级归属 + 例外清单」粒度是有效的。但 S1b 的技能只有 52 文件 / 6 目录，
- **比 S1a 更轻却撞顶失败**（产物 10 行 / 1476 字节，只有标题与图例）。
- 差异不在归属工作量，而在我往 S1b 里额外压了两件事：① 对 6 对已漂移的 `guide/` 文件
- （共 12 个文件）做**章节级**合并裁定并识别每份的 engine-carrier 章节 —— 这是 reconciliation，
- 不是 attribution；② 消化 21.6KB 的上游产物作对照基线（file-path-only handoff 的必然成本）。
- 建议：`create-mode.md` 步骤 5 与 `patterns.md` 的 Serial Chain 段增一条 stage 设计纪律 ——
- **一个 stage 只承载一种任务类型**；attribution（给现状贴归属）与 reconciliation（对多份冲突副本做裁定）
- 预算量级不同，MUST NOT 同 stage。本例的正确修法是把合并裁定移入 S1d（其定义里本就写着
- "落地 S1b 的 guide/ 合并裁定"，合并裁定与迁入目的地设计本是同一件事），而不是把 plantuml 目录再拆细。
- **[协议缺口] "增量落盘"作为 brief 里的一句指令不可靠，撞顶即全损；应升格为 gate 条件。**
- S1b 的 brief 明写「header first, then append and save per directory, so partial progress survives
- budget exhaustion」，但实际产物只有 10 行标题+图例，而子代理自述进度是
- "document/ classified. Now the howto/ exception files" —— **它自述已完成的工作从未落盘，全损**。
- 同一轮里 S1a 与 S1c 都遵守了增量落盘（产物完整）。说明这条纪律的执行率不稳定，
- 而 `patterns.md` 的 Stage Execution Protocol 只在 VALIDATE 步检查「outputs exist」，
- 一个 1476 字节的桩文件也能让「exist」为真。
- 建议：gate 增一条**可程序判定的最小实质性检查**（如产物字节数下限、或「每个已声明判定的目录名
- 在产物中可检索」），使桩文件无法通过 VALIDATE。这与本仓已有的教训同形 ——
- AGENTS.md 里那条「files exist / headings present 这类检查会漏掉只在运行时暴露的潜在缺陷」。
- **[gate 设计] 覆盖型 gate 检不出「判定错了」，只检得出「没判定」。**
- S1a 的 gate「每个目录都有层级判定」通过了，而它对我 brief 里断言为整批引擎语法的
- `references/document/` 给出了 MIXED —— 5 个文件（`01-uml-overview`、`08-modeling-methodology`、
- `09-grasp-principles`、`10-architecture-diagram`、`11-wbs-diagram`）实为引擎无关的建模知识。
- **是子代理越过 brief 的预设去读了那五个文件才发现的**；若它照 brief 字面整批判 SYNTAX，
- gate 照样通过，错误会一路带到 S1d 的目的地设计。本次靠我在 brief 里加的
- 「整批判定须点名 ≥2 个实读文件」这条纪律兜住（S1c 据此发现 echarts 并不干净）。
- 建议：把这条纪律写进 stage gate 模板 —— **任何整批（wholesale）判定必须附实读证据**，
- 否则覆盖型 gate 会把"没读就下结论"判为通过。
- ## 本次 run 做对的部分（非问题）
- **不采信子代理自述计数**：上一轮我把「产物条目数」当成「覆盖文件数」算错过（5–6 vs 12–14 次派发），
- 本次全部用确定性复核（`wc -lc` 产物、`grep -c` 判定词、`find` 实际文件清单、`git status` 越界检查），
- 并抽查了子代理三处反驳 brief 的关键断言（echarts L103-107 原文、mermaid document/ 五文件存在性、
- `cycle4-improvements.md` 的 4 处分布）—— 三处全部成立，其中一处（echarts 行号）我进一步修正了
- 子代理的表述：L103 本身是**正确的**两层形态，越界的是其后三条。
- **不擅自消耗 retry 额度**：S1b 尚余 1 次重试，但诊断指向 stage 定义问题，盲目重试预测仍败，
- 而修好它需要重定义 stage 交付物 = 移动球门。选择 escalate 而非静默重试或静默改 gate。
- **canonical 零改动**：三次派发（含一次并发）后 `git status --short skills/ shared/ templates/ .specify/shared/`
- 全空，Worker/Meta 写权限分离在并发场景下同样成立。
