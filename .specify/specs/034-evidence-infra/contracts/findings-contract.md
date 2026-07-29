# Contract: findings.json / manifest.json / lanes / index(证据存储合同)

> 合同 ID 前缀 C-F。字面量以 requirements.md Shared Strings 为准。pytest 合同测试:`tests/contract/test_evidence_findings_schema.py`。

## C-F1 findings.json 顶层结构

MUST 含且仅含字段:`schemaVersion`(int, =1)、`kind`(= "speckit.evidence-findings")、`target`、`runId`、`window`、`platforms`、`lanes`、`evidence`、`findingsDigest`。未知顶层字段 MUST NOT 出现(白名单校验)。

## C-F2 target 词汇

`target` MUST 匹配 `^(skill:[a-z0-9._-]+|/speckit\.[a-z0-9._-]+|project)$`(与 feedback-utils.py 的 unit_id 正则同源,另加 `project` 整仓目标)。

## C-F3 runId 格式

MUST 匹配 `^ev-\d{8}-\d{6}-[a-z0-9-]+$`;与所在目录名一致;与 manifest.runId 一致。

## C-F4 evidenceState 枚举封闭

每条 evidence 的 `evidenceState` MUST ∈ {"Present","Wired","Exercised","Outcome-supported","Missing","Unobserved","Not applicable"}(七态,大小写与连字符逐字符匹配)。合同测试 MUST 断言枚举封闭(出现第八值即失败)。

## C-F5 泳道状态枚举封闭

`lanes` MUST 恰含五键 session/project/assets/runs/feedback;每键的 `status` MUST ∈ {"available","partial","unavailable"}。runs 键 MAY 含 `teamsScanned`(int ≥0);feedback 键 MAY 含 `entries`(int ≥0)。

## C-F6 裁决字段禁令

findings.json 全文档(递归)MUST NOT 出现键名:`severity`、`score`、`scores`、`aiFixPrompt`、`recommendation`、`supportTrack`、`priority`。合同测试以键名黑名单递归断言。

## C-F7 隐私红线

`summary`、`evidenceRefs`、`signals` 的序列化文本 MUST NOT 含:(a) 以 `/home/`、`/Users/`、`C:\` 开头的绝对路径(仓库相对路径豁免);(b) 常见密钥模式(`AKIA[0-9A-Z]{16}`、`ghp_[A-Za-z0-9]{36}`、`-----BEGIN .* PRIVATE KEY-----`、`sk-[A-Za-z0-9]{20,}`);(c) `privacyNote` 缺失时 session 泳道条目视为违规(session 泳道 MUST 标注脱敏方式)。

## C-F8 findingsDigest

MUST 为 `sha256:` + 64 位十六进制;对 `evidence` 数组的紧凑 JSON(`separators=(",",":")`, `sort_keys=True`, UTF-8)计算;findings.json 与 manifest.json 中的值 MUST 相等。

## C-F9 evidence 条目字段

每条 MUST 含 `id`(`ev-\d{3}`,运行内唯一且从 001 连续)、`lane`(∈ 五泳道)、`evidenceState`、`summary`(非空 string)、`evidenceRefs`(string[],可空数组)、`signals`(object,值全为 number)。`privacyNote` 可选。空 `evidence: []` 合法(空证据源不编造)。

## C-F10 manifest.json

MUST 含 `runId`、`target`、`created`(ISO 8601 UTC)、`lanes`(每泳道 status;`unavailable` 的泳道 MUST 附非空 `reason`)、`engine`(`engineSubsetPath`、`upstreamCommit`;Node 可用时含 `nodeVersion`)、`findingsDigest`。

## C-F11 lanes/*.json

每条实际执行(status ≠ unavailable)的泳道 MUST 落 `lanes/<lane>.json`,内容为该泳道的原始引擎 envelope(session/project/assets)或 Python 采集中间结构(runs/feedback),经同一脱敏过滤;`unavailable` 泳道 MUST NOT 产生 lanes 文件。

## C-F12 index.json

`.specify/memory/evidence/index.json` MUST 含 `store`(= "evidence")、`updated`、`entries[]`(每项 `runId/target/created/lanesSummary/file`);collect 成功后 MUST 追加对应条目;索引缺失/损坏时 collect MUST 全量重扫目录重建(不报错终止)。

## C-F13 feedback 打包排除

`.specify/memory/evidence/` MUST 不进入 feedback `--action package` 的 zip(实现侧:package 只收集 feedback 目录内 md,天然排除;合同测试断言 package 产物 zip 中无 evidence 路径)。

## C-F14 intervention.json

存在时 MUST 含 `targetFinding`(匹配基线 findings 中某 evidence.id)、`change`、`baselineRunId`(= 所在目录)、`expectedSignal{signalKey, direction∈{improve,reduce}}`;`verdict` 若存在 MUST ∈ {"Outcome-supported","Unobserved"}。
