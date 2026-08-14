---
id: "20260814T062944Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "040-agent-metadata-portability-analyze-2026-08-14"
scope: "local"
feature: "040-agent-metadata-portability"
feature_id: "044"
partial: false
created: "2026-08-14T06:29:44Z"
summary: "只读跨产物一致性分析完成:程序化预检(占位符/FR=28/SC 引用闭包 8/8/blockedBy 悬空/feature 行)后做语义层检测,产出 4 条 finding(0 CRITICAL、1 HIGH→经独立验证子代理降级 MEDIUM、1 MEDIUM、2 LOW)。核心 finding:I-1 claude 行去待核实条件与零待核实交付闸的条件性张力(已验证降级,有 D4/D3 逃生通"
---

## Review
只读跨产物一致性分析完成:程序化预检(占位符/FR=28/SC 引用闭包 8/8/blockedBy 悬空/feature 行)后做语义层检测,产出 4 条 finding(0 CRITICAL、1 HIGH→经独立验证子代理降级 MEDIUM、1 MEDIUM、2 LOW)。核心 finding:I-1 claude 行去待核实条件与零待核实交付闸的条件性张力(已验证降级,有 D4/D3 逃生通道);U-1 model-tier 值域缺 lite 且 none 未定义;U-2 正文缺章节渲染行为未显式;I-2 T009/T027 顺序需注明。覆盖率 100%(28 FR/8 SC 全映射),feature 链接高置信无漂移,constitution 零违规。结论:可进入 /speckit.implement,建议先顺手修订 3 处 MEDIUM/LOW。

## Optimization Points
- **检测取证与产物内事实的边界要分清**:F1(claude provenance 风险)初判 HIGH 的依据之一("官方文档不可达")其实只存在于会话期的探索记录里,并未写进任何被分析产物 —— 独立验证子代理据此降级为 MEDIUM。这是 finding-validation 机制的正确拦截,但也暴露检测侧的教训:把"会话上下文事实"当"产物内事实"引用会系统性抬高严重度。建议 analyze 的检测步骤在提交 finding 前先做一次"该前提能否在被引产物中 grep 到"的自检,不能则自动降一档或改述为条件风险。
- **程序化预检大幅压缩了分析开销**:占位符扫描、FR 计数、SC 引用闭包、blockedBy 悬空检测、feature 行存在性全部用 grep/python 片段完成,LLM 只处理语义层(覆盖映射、术语漂移、constitution 对齐)。其中 blockedBy 检查抓到一个 `Txxx` 悬空引用,人工确认是格式说明里的示例文本而非缺陷 —— 程序报警 + 一次人工判读的组合比纯 LLM 通读 43 任务可靠且省。
- **token-efficiency**:三个产物均为本会话所写、语义模型已在上下文,分析未做整文重读,仅针对性 grep;验证子代理只携带单条 finding 与证据位置(新鲜上下文),符合 §5.5 隔离要求。无显著可避免开销。
