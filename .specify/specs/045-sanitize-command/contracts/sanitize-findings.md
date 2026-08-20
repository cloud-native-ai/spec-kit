# Contract: 发现 Schema 与台账合并语义(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene  
**消费方**: sanitize-utils.py 引擎、/speckit.sanitize 命令模板、tests/unit/test_sanitize_engine.py

## 1. 发现 Schema(验证规则)

字段与类型见 data-model.md §1。引擎在 record/collect 写入前强制校验,违例 → 退出 2:

- C-1 `id` 必须等于 `sha1(category + "|" + target)[:12]`(hex);引擎重算比对,不接受调用方自造 ID。
- C-2 `category` ∈ 六枚举;`detection` ∈ {programmatic, semantic};`severity` ∈ {high, medium, low};`disposition` ∈ {delete, archive, repair, delegate, dismiss};`reversibility` ∈ {irreversible, reversible};`state` ∈ {pending, resolved, dismissed}。
- C-3 `stale-residue` / `redundant` 发现的 `evidenceRefs` 必须非空且至少一项 `kind ∈ {commit, path}`(FR-003)。
- C-4 `reversibility` 与 `disposition` 绑定:delete/archive → irreversible;repair/delegate/dismiss → reversible。
- C-5 新写入发现的 `state` 必须为 `pending`(FR-012 初始态)。
- C-6 `disposition=delegate` 时 `summary` 必须包含被移交命令名(`/speckit.docs`、`/speckit.instructions`、sync-mirrors 等)。
- C-7 `target` 必须以资料根前缀开头(data-model §4 白名单)。

## 2. 台账物理契约

- 位置:`.specify/memory/sanitize/findings.json`;结构 `{version, updated, findings[]}`,`version=1`。
- 原子写:先写 `<path>.part` 再 `os.replace`;损坏(非法 JSON)时引擎重建为空台账并在输出 `notes` 声明(对齐 evidence-utils rebuild_index 先例)。
- `updated` 为最近一次成功写入的 UTC ISO-8601。

## 3. 合并语义(跨运行状态机)

以 `id` 匹配,规则表(data-model §2):

- C-8 新 ID → 追加,state=pending,firstSeenRun=lastSeenRun=本次运行。
- C-9 pending + 再检出 → 刷新 lastSeenRun 与 evidenceRefs/summary;state 不变。
- C-10 pending + 未检出 → 自动置 resolved,resolvedAt=本次运行,notes 追加 "not re-detected this run"(外部修复自然收敛的唯一通道)。
- C-11 resolved + 再检出 → 重开 pending,notes 追加重开备注(回归信号)。
- C-12 dismissed + 再检出 → 仅刷新 lastSeenRun;state 不变(用户否决权威)。
- C-13 resolved/dismissed + 未检出 → 原样保留;台账永不删除条目(审计)。

## 4. 自动收敛的运行完整性前提

- C-14 自动收敛(C-10)仅在"该发现所属类别的检查器于本次运行实际执行"时生效;`--roots` 限定子集运行时,未覆盖根上的 pending 发现保持原状(防部分扫描误销账)。

## 5. 语义候选与证据包

- C-15 `collect` 输出的 semanticCandidates 仅含时间性声明材料(memory-todo/memory-draft 根);每候选携带 `claims`(引擎机械抽取的声明短语)、`evidencePack`(gitLog 摘要行 + pathExistence 映射)。
- C-16 agent 判定结果经 `record` 写入;判定为"证据不足"的候选不写入台账(运行摘要呈现计数即可)。
- C-17 语义发现的 evidenceRefs 必须引用其判定所依据的具体证据(commit 哈希/路径),不得只写"经分析"类空引用(SC-005 抽检锚点)。

## 6. 摘要优先输出

- C-18 一切对外输出(status/collect/record 信封)为计数摘要与目标路径列表;不整读、不复述材料原文段落(040 纪律)。

## 7. 契约测试锚点

- 合并规则 C-8..C-13 逐条夹具断言(构造双运行序列);schema 规则 C-1..C-7 逐条违例拒绝断言;C-14 部分扫描不误销账断言;C-17 空引用拒绝断言。
