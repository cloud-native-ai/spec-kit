---
id: "20260907T132729Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "050-proactive-flow-trigger-clarify-20260907"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "050-proactive-flow-trigger"
partial: false
created: "2026-09-07T13:27:29Z"
summary: "Mode A 全流程走通:check-prerequisites 解析 → 相位判定(plan.md 不存在 → Mode A)→ **可写性探针先行**(dir/file 写位 + touch-test 全 PASS,未先跑问题循环)→ 摘要优先加载上下文(features.md 49 行索引以 ID/Status/Name 三列投影读取,未整表注入;constitution/README/do"
---

## Review
Mode A 全流程走通:check-prerequisites 解析 → 相位判定(plan.md 不存在 → Mode A)→ **可写性探针先行**(dir/file 写位 + touch-test 全 PASS,未先跑问题循环)→ 摘要优先加载上下文(features.md 49 行索引以 ID/Status/Name 三列投影读取,未整表注入;constitution/README/docs 未做无谓全量读)。生成 5 问一批提出(互不改变对方选项集,符合批处理规则),每题附 Recommended 与理由,用户全选推荐。集成后逐项落地:Related Feature 解析、FR 23→26、SC 12→15、Key Entities 5→7、Acceptance Scenario 30→32、Edge Case 14→17、Assumptions 增 3 改 2。new-Feature 注册义务全部完成:features/050.md(0 残留占位符)、索引行 + 表头 49→50、Feature 032 反向交叉引用;索引一致性经程序校验(50 行/header 50/ID 1–50 连续唯一/详情文件 50 份)。append-only 不变式经计数校验(4→9 严格递增,首轮 4 行逐字保留)。本轮另发现并修复两处**既有文本缺陷**(SC-011/SC-012 无生产它们的 FR;SC-008 只测 violations 未测 total 上限,而实测门控预算整数余量为 0 且 templates/*.md 在扫描范围内),以及一处自造的标号歧义(两套同日 Q 号),均已回溯修补并程序复核。glossary 新增 3 条(情境身份/回合遥测/种子规则)经 detect-conflict 全 clean 后直写,validate 通过。残留 NEEDS CLARIFICATION 0。

## Optimization Points
- **Mode A 集成规则未警示 `update-feature-index.sh` 是破坏性脚本,而 AGENTS.md 恰恰把它写成该表头计数的维护者——这是本次最高风险的一步**:规则原文是「allocate the next ID from `.specify/memory/features.md`, add the index row (Draft) and `features/<ID>.md` detail」。按 AGENTS.md 的 Documentation Map(「the authoritative count is the auto-derived `Total Features` header (maintained by `scripts/bash/update-feature-index.sh`)」),最"守纪律"的做法正是跑该脚本;而 Feature 049 的 Implementation Notes 已实测记录该脚本整体重写 features.md、输出 6 列(缺 Spec Path)、以目录 slug 与桩文本覆盖手写散文、重置全部 Status,且 `test_c3` 仍然通过(**静默损坏**)。本次是因为先读了邻近 Feature 的详情文件才发现并改为手工编辑。建议在 Mode A 的 new-Feature 集成规则里直接补一句「索引行与表头计数**手工编辑**,MUST NOT 运行 `update-feature-index.sh`」,或至少「改动 `features.md` 前先查邻近 Feature 详情文件的 Implementation Notes 是否记录了索引维护陷阱」。当前状态下,一次"正确遵守文档"的操作就足以静默毁掉整份索引,而测试不会报警。
- **Mode A 的 Completion Signals 类目缺一条可产出性检查,导致 requirements 阶段的检查清单会以"通过"放行不可测的 SC**:本次发现 SC-011/SC-012 的 Measurement Source 引用"回合级观察记录",但**没有任何 FR 要求生产该记录**(FR-009 只记录发生了建议的事件,静默回合零痕迹)→ 两条 SC 的分母不存在。而 requirements 阶段的检查清单当时判定为通过,因为它校验的是「每条 SC 都具名了一个 Measurement Source」——这个条件被平凡满足。类目现有的「Acceptance criteria testability / Measurable DoD indicators」不足以捕获它。建议增列一条:**每条 SC 的度量来源必须指向某个 FR 强制生产的记录或产物**;若来源是"人工观察"而该度量又被用作护栏,则视为缺口。护栏型 SC 不可测等于无护栏,这类缺陷比缺 SC 更危险,因为它在纸面上看起来已经覆盖了。
- **同日追加第二个 session 块时缺少标号消歧规则,导致自造的引用歧义与 7 处回溯修补**:requirements 阶段已写入 `### Session 2026-09-07`(Q1–Q3),本轮同日又提 5 问,我沿用了 Q1–Q5 编号——两套 Q 号语义完全不同(首轮 Q3=评估时机 B,本轮 Q3=阈值语义 A),写进 FR-010 后形成字面自相矛盾的观感。发现后不得不回溯 7 处加 `首轮` / `R2-` 前缀。append-only 不变式禁止改写既有行,所以消歧只能在写入时一次做对。建议 Mode A 集成规则补一句:**目标文件已存在同日 session 块时,新块必须使用带轮次前缀的标号(如 `R2-Qn`)并在块首声明该约定**;集成后 grep 一次裸 `Q\d` 引用确认无歧义残留。
