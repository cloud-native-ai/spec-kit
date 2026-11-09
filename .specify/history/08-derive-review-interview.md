# 主题：Derive + Review + Interview（T4）

范围：分析门与修复环、独立验证器与严重度裁决、评审分段（process/artifact/implementation/code）、同作者检测、访谈式收敛、需求质量 checklist、测试套件审计。
覆盖 **39 个** Qoder 会话（2026-10-05 → 2026-11-10）；sid 在文内逐条引用，完整清单见文末。
关联主题：[[06-anchoring-goal-team]]（验证波）· [[07-archive-history-session]]（记录证据）· [[09-memory-state]]（状态与基线）· [[02-sdd-feature-lifecycle]] · [[00-cross-cutting-lessons]]

## 1. 关键决策与理由

- **独立验证器模式**：只读、fresh-context、单一 finding；verdict 取值 `confirm` / `downgrade` / `reject`；必须同时返回 `evidence_supported` 与 `evidence_not_supported`（强制指出工件**没有**说的话）；静态验证（Bash 被拒）必须声明其弱路径。严重度 rubric：有界、已披露、有下游缓解的需求文本缺口不是 HIGH；"缺 magnitude 测试"是反对 reject 的理由，不是支持 HIGH 的理由。（`12f9e0ad`、`293b26ba`、`fa711d34`、`57f56b33`、`670d17a3`、`aae40c3f`、`94c3fd85`、`6799e41f`、`f3930139`）
- **Analyze 门**：CRITICAL/HIGH 门槛；一次运行只开**一个有界修复环**；第二轮 C/H 未清 → 停止并交四要素 handoff（发现/影响/产物/封闭选项），不无限自修；HIGH 无条件触发 validation wave；零写入零提交是只读阶段的默认。（`dde7a9d4`、`cfa3d399`、`9857e730`、`6b6a829d`）
- **同作者门**：委派 fresh-context 只读评分者做检测；自编辑后的混合集必委派；工件早于会话（不同作者）时不触发，直接检测 + 无条件验证波。（`7362873e`、`aaf1fee4`、`cfa3d399`）
- **评审架构**：固定顺序 process segment（`review-sdd-process`）→ code segment（`code-review`），双报告 `review.md`/`code-review.md`，严重度不合并；生命周期门 `Implemented → Ready for Review` 单 owner（feature-details 模板）；artifact segment 判断"验收诚实"而不只看文件齐备；ARC（acceptance reality check）独立复核 closure 声明。代码基线解析顺序：显式 > requirements 首提交的父 > trunk merge-base，head 固定。（`c218f73c`、`70806e65`、`b3bf67dc`、`2a7e498f`、`644a1597`）
- **访谈（Interview）**：六轮访谈产出 24 个决策；核心概念改名 望文生义 → 不言自明（Self-explanatory）；用户视角原则，ceiling "直接看到"、floor "一个简单命令"，floor 已足够；SHOULD 作为最佳实践入口；维度顺序 = 用户显式 > 框架规则 > 逐条；真源留在 `goal.md` frontmatter，路径是投影（由 `/speckit.sanitize` 最终一致）；不做预防性优化。（`0f63f87a`）
- **需求质量 checklist**：40 项 CHK001–CHK040、8 组、100% 可追溯；"unit tests for requirements writing"——检查需求文本质量而非实现行为；已有的 `checklists/requirements.md` 不动，新建 `requirements-quality.md`。（`3e8cf04f`、`be645516`）
- **测试套件审计**：三判据 correctness（不可伪证断言、已移除表面、不可重复依赖）/ necessity（重复须点名）/ slow-by-construction；产出 keep / rework / delete-candidate，每个删除候选带一行理由；审计只读，删除与改写归 owner 执行。（`fe7dafff`、`a8412de2`、`3db3e58c`、`bd6dcf6f`、`dc1d9296`）
- **决策张力（decision tension）**：owner 阈值四触发（不可逆/跨团队/高爆炸半径/触及宪法 MUST）；计划没有义务逐一证明"每个决策都低于阈值"；structural validator 绿 ≠ 语义普查。（`fa711d34`）

## 2. 可复用经验 / 踩坑

- **`[x]` 不是证据（false closure）**：T016–T019 被 commit `19003b613` 扫过，但命名的 guard `tests/contract/test_command_run_goal_team.py` 不存在、T019 的 create-binding 写入缺失；P1 = 在已被接受的 8/8 closure 之下藏着假绿任务账本；P2 = 悬空证据指针。（`70806e65`、`644a1597`、`b3bf67dc`）
- **计数以机械派生为准**：叙述"10 Gap"实际 11（objective-analysis-gate rule 8）；citation group = 块内**最后一个**带 FR-/SC- id 的括号组；backticked 形式是提及不是声明；`account-clause-coverage.py` 只匹配 ASCII 括号（全角括号契约只识别 13/29）；clause id 唯一性按文件；legacy `md-heading` 让 pointer stanza 变成幻影 clause。（`f556a5f4`、`a6a25181`、`aaf1fee4`、`94c3fd85`、`7362873e`）
- **真空绿谱系**：`or True`、`f(x)==f(x)`、断言自己引入字面量的 self-grep、"空真"当红基线、`--baseline` 读错键层、空 fixture 的排除测试、`test_module_exists` 型形状测试；`test_feedback_skill_conformance.py` 的 source glob 在两层布局下匹配 0/54——靠 mirror 侧工作而绿。（`5fea4a1e`、`bd6dcf6f`、`a6a25181`、`670d17a3`、`fe7dafff`）
- **Subagent 声明须一手复核**：Explore 把 manage-feedback Path A 的 "A3 自省" 说成 "Mode 5"；"GATE-8" 不存在（gate id 是 tasks.md 局部，implement 锚点是 Step 9 verification-log）；plan.md 在委派结果回填前预断言 "verdicts unchanged"——被评分者抓到。（`7362873e`）
- **管道会吃掉退出码**：`| tail` 反映 tail 而非 pytest；`run-tests.sh` 尾部捕获的是串行 mini-pass——捕获完整日志再 grep 并行摘要。（`7362873e`、`48099f17`）
- **可达性**：未 push 的 HEAD 使 §0 可达性 UNRESOLVABLE；用绝对路径 + `git show <sha>:<path>` 恢复引用，不编 URL。（`f556a5f4`、`d22e136f`、`df0a6be3`）
- **行号/引用须重解析**：feature-ref "row 3" 实为 `constitution.md`（guard 行 12–13）；`tasks.md:111` 是分隔线；plan pin `:361` 邻近而非命中 `:365` 的等值断言；finding 的转述可能比工件原文更宽。（`670d17a3`、`6799e41f`、`aae40c3f`）
- **SC 过声称**：SC-010 声称 `pass`，但其 post-disposal 契约读法 exit 1、86 个失败 id（51 个高于 46-id 基线）——诚实状态应为 `partial`；无 ratified narrowing 不得改写。（`2a7e498f`）
- **审计产物不可全信**：`junit-full.xml` 记录 `tests="0"`、`full-run.log` 中途中止，任何通过/失败计数不得取自它；`--durations` 数据未留存。（`a8412de2`、`3db3e58c`）
- **只读阶段的边界**：no commits；wrap-up 记录留给 orchestrator 归档；registry 状态冲突作为 ANOMALY 抛回而非自行平滑。（`6b6a829d`、`d22e136f`）

## 3. 未完成 / 待办

- **063 F4 谱系**：编译 Wrap-up 缺引擎参数的生成源未修；063 的 F1 机制修复成为后续特性工作。
- **082 遗留**：SC-005 需要 build qualifier + 一条执行重装的 task；T006 措辞需收紧；`OI-082-01` improve 接线。
- **SC-010 partial**：094 的验收现实检查维持 `partial`（ARC 读法），`final_path` 8/8 不变；P2/P3 残余（悬空 `wp07-closure-suite.log`、§5.1/§5.3 指向列表项）。
- **审计的 rework/delete 执行**：chunk 0–5 的候选由 owner 排期，审计本身不动（慢测试 opt-in 标记是 48099f17 的用户选择）。
- **REC 登记**：REC-063-01..10 已入 register；061 引用的 REC 从未登记（forward-only seam）。

## 4. 关键交互流程

- **SDD 阶段链**：requirements → clarify → plan → tasks → analyze → implement → review → closure；每阶段写 E-3/E-7 证据；analyze 的修复环与 review 的修复波都遵循"发现 → 验证 → 修复 → 重测"。（`cfa3d399`、`9857e730`、`f2f7adbe`）
- **Analyze**：工件装载 → passes A–G → 3 个 fresh-context validator → 严重度表 → 门结论（BLOCKED/PASS）；HIGH 必开 validation wave（confirm/downgrade）。（`cfa3d399`、`dde7a9d4`、`6b6a829d`）
- **Review**：Segment A（process）→ B（artifact）→ C（implementation）→ D（code）+ ARC；verdict 与 severity 分开写；P0/P1/P2 计数进入报告与 register。（`70806e65`、`644a1597`、`b3bf67dc`、`2a7e498f`）
- **Interview**：多轮收敛 → 每轮回显改动 → 目标文件内直接编辑；访谈结果必须落成所有者文档/环境段落/守卫三表面。（`0f63f87a`）
- **测试审计**：chunk 清单 → 机械断言扫描 → 抽样声明 → 逐模块表（模块/函数/keep/rework/delete + 理由）→ 总计与 top 候选。（`fe7dafff`、`a8412de2`、`dc1d9296`、`bd6dcf6f`）

## 5. 用户 ↔ 模型分歧点

- 用户推翻"critique 单独建 spec"，要求与当前 goal 高度契合 → 作为 goal 组件落地。（`9c57a1ed`）
- 用户授权框架阈值变更（082 任务上限 40→60）替代机械拆分；模型披露"用户方案 vs 框架规则"的张力后执行。（`0f63f87a`）
- 模型拒绝给 add-only generator 打补丁（其契约测试会被证伪）——在 T018/C-12 处 fast-fail 停止并给四个封闭处置选项；用户选择"经 `/speckit.instructions` 刷新内容"。（`825aa3a5`、`2633f12c`、`d01a3852`）
- 用户推动更深语义/更严验证的稳定模式延续：从"看门狗只认正证据"到"SC 过声称必须降级"。（`34080ca9`、`2a7e498f`）
- 模型自纠被记录：Complex→Simple 分类自纠（`544f490f`）、verdict 预断言自捉（`7362873e`）、s11 未执行即 PASS 自捉并补正（`da741035`）。

## 覆盖 sid（39）

`0f63f87a` `12f9e0ad` `2633f12c` `26ca6503` `293b26ba` `2a7e498f` `3db3e58c` `48099f17` `5059aff0` `5205ab17` `57f56b33` `61298504` `63f60627` `644a1597` `670d17a3` `6799e41f` `6b6a829d` `70806e65` `7362873e` `825aa3a5` `94c3fd85` `a6a25181` `a8412de2` `aae40c3f` `aaf1fee4` `b3bf67dc` `bd6dcf6f` `be645516` `c218f73c` `c6516cb7` `cfa3d399` `d22e136f` `dc1d9296` `dde7a9d4` `df0a6be3` `f3930139` `f556a5f4` `fa711d34` `fe7dafff`
