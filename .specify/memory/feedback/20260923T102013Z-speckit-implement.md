---
id: "20260923T102013Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "052-fast-fail-principle-implement-20260923T1"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "052-fast-fail-principle"
disposition: "processed"
partial: true
created: "2026-09-23T10:20:13Z"
summary: "**Partial run** — Phase 1–8 部分完成:63 个任务中 50 个已闭合(Phase 1–7 全部 + Phase 8 的 T044–T049),13 个仍为 `[ ]`(T050–T062),因上下文预算耗尽而停在一个**已提交、树洁净、门禁全绿**的检查点上,不是失败也不是移交。已完成部分逐项有实跑取证:契约套件相对冻结名字级基线 `comm -13` 的 26 条新增"
introspection_ref: "introspection-20260923T120035Z#F-08"
disposition_reason: "introspection:introspection-20260923T120035Z#F-08"
---

## Review
**Partial run** — Phase 1–8 部分完成:63 个任务中 50 个已闭合(Phase 1–7 全部 + Phase 8 的 T044–T049),13 个仍为 `[ ]`(T050–T062),因上下文预算耗尽而停在一个**已提交、树洁净、门禁全绿**的检查点上,不是失败也不是移交。已完成部分逐项有实跑取证:契约套件相对冻结名字级基线 `comm -13` 的 26 条新增失败**全部**落在 red-first 守卫文件内、零外部新增,另治好 7 条既有失败;门控 `total` 全程 23、violations 0、扫描器零改动;四组镜像判据按**集合包含**复核通过。本特性的核心制品已落地且被守卫:真源文档 9 节全部填实(308 行、逐行零命中阻塞模式)、常驻顶级章节、宪章双落点(模板 XIV / 活动 XVI / 命令第 8 条 / 版本 1.13.0 / 四钉同批上调)、子代理派发注入(拥有者子句 + 2 份出厂预设 + 4 棵按工具树共 8 个字节相等副本 + 团队载荷第六字段行 + 两处制作者要求)、生长闭环、五处边界与冲突裁决顺序、类 ⑪ 跨纪律登记。未完成的是 T050 的 22 条断言体(c22/x23/a13–a15/g1–g17)与 Phase 9 的收尾核验,故 DoD 与 Completion Gate **均未达成,MUST NOT 被报为 met**。运行期共查出并处置 9 处缺陷,其中 6 处顺手修复(各附变异演练或实跑取证)、1 处上送用户裁定(FR-014 同一性键,已裁定并级联五处)、3 处上游缺陷如实上报未改写。

## Optimization Points
- `pytest -k` 的 token 按**子串**匹配测试 id,且**同时匹配 slug**:裸 `c1` 会选中 `test_c10_*`…`test_c19_*`,而 slug 里出现 `c6_` 一类片段会跨阶段泄漏。分区式认领一个测试文件时,token MUST 带尾下划线、函数名 MUST 形如 `test_<前缀><N>_<描述>`,且每个核验行 MUST 断言其收集数等于认领条款数(否则空选恒绿)。建议在 implement.md 的"Test runs"要点里补一条。
- 取证命令 MUST NOT 把 pytest 接在管道之后再取退出码(`| tail` 会把非零换成 0),且 node id MUST 由 grep 取真而非凭记忆书写:本轮凭记忆写了两个不存在的 `test_c7_*` / `test_c8_*` node id,pytest 收集 0 个用例、`no tests ran` 被写进取证文件,看起来像一条通过记录。
- 自指哨兵(扫描自身源码的检查)MUST 让探针字符串与被禁字符串不同形:把被禁路径逐字写进断言的失败消息会让哨兵在自己的诊断文本上恒红。修法是片段拼接 needle + 消息改写为不含该字面量的散文 + 一条伴生非空断言。
- 只支持全量再生的引擎(`regen-command-copies.py`)与支持窄前缀的引擎(`sync-mirrors.py --only <path>`)混用时,MUST 对每个被编辑的源文件逐个核对其镜像已同步:本轮窄 `--only` 漏掉两个 skills 文件,而 skills 的 DIFF **条数**改前改后都是 38(一增一减相互抵消),只有**集合**比较才暴露出 `patterns.md` 是新增成员。这直接证明"相对判据 MUST 写成集合包含,不能写成条数相等"。
- 对未知参数**静默返回成功**的渲染入口是高危面:`render_agents_for_tool(root, "github")` 对不存在的 tool 键返回 `rendered: 0` 而不报错,正确键是 `copilot`。调用此类入口后 MUST 断言其返回的渲染数 > 0,而不是只看退出码。
- 阶段边界不总能满足"回归差集为空":新建一个真源文档而其常驻指针要到下一阶段才落地时,既有的可达性守卫会在这中间**合法地**变红。此时 MUST 把两个阶段合成一个提交单元,而不是提交一个已知红的增量。
