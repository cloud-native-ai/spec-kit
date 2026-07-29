# Data Model: 034-evidence-infra(Feature 038 Evidence Infrastructure)

> 来源:requirements.md Key Entities + FR-003~FR-007、FR-011;字面量以 Shared Strings([[STR-NNN]])为准。

## E1. 证据运行(Evidence Run)

一次采集的产物单元。

| 字段 | 类型 | 约束 |
|------|------|------|
| runId | string | 格式 `ev-<YYYYMMDD>-<HHMMSS>-<target-slug>`;目录名即 runId |
| 目录 | path | `.specify/memory/evidence/<run-id>/` |
| 内容 | files | `findings.json`(必)+ `manifest.json`(必)+ `lanes/<lane>.json`(每条实际执行的泳道一份) |

生命周期:创建后只读(不可变);无删除动作(治理走 feedback package 排除 + 未来清理策略,本 spec 不建清理)。

## E2. 证据合同(findings.json)

公共层与消费层的边界契约。顶层字段:

| 字段 | 类型 | 约束 |
|------|------|------|
| schemaVersion | int | 本版固定 1 |
| kind | string | 固定 [[STR-011]] `"speckit.evidence-findings"` |
| target | string | 目标单元 id,沿用 feedback unit_id 词汇(`skill:<name>` 或 `/speckit.<cmd>`)或 `project`(整仓) |
| runId | string | = E1.runId |
| window | object | `{since, until}` ISO 8601;可空(全量) |
| platforms | string[] | 本次实际采集到数据的平台(qoder/codex/claude/cursor…) |
| lanes | object | 五键(session/project/assets/runs/feedback)→ E4 泳道状态 |
| evidence | E3[] | 证据条目数组(可为空数组——空证据源合法,不编造) |
| findingsDigest | string | `sha256:<hex>`,对 evidence 数组的规范化 JSON 计算 |

禁止字段(合同红线,FR-004):严重度/评分/修复建议/支持轨道等一切裁决字段。

## E3. 证据条目(Evidence Item)

| 字段 | 类型 | 约束 |
|------|------|------|
| id | string | `ev-NNN` 运行内唯一、连续 |
| lane | enum | session/project/assets/runs/feedback |
| evidenceState | enum | 七态之一(E5) |
| summary | string | 脱敏后的语义摘要;禁含原文 prompt/命令/私有绝对路径/密钥 |
| evidenceRefs | string[] | 不可逆哈希 或 仓库相对路径(runs/feedback 泳道) |
| signals | object | 数值信号(计数只路由不产生发现);键自由、值为 number |
| privacyNote | string? | 可选,标注脱敏方式(如 `redacted-semantic-facet`) |

## E4. 泳道(Lane)与泳道状态

| 泳道 | 实现 | 数据源 |
|------|------|--------|
| session | Node:`session-analysis.mjs facts` | 各平台本地会话落盘 |
| project | Node:`core-change-watch/*.mjs`(project-profile、git-history-profile、evidence-pack;可选 dependency-governance) | 仓库结构与 git 历史 |
| assets | Node:`coding-agent-practices/asset-baseline.mjs`(lint/inventory/integrity 三信封) | 已配置资产 |
| runs | Python 原生 | `.specify/teams/<slug>/{runs/*.md, STATE.md, run-log.jsonl}` |
| feedback | Python 原生 | `.specify/memory/feedback/{index.json, *.md}` |

泳道状态(manifest 与 findings.lanes 共用):[[STR-008]] `available` / [[STR-009]] `partial` / [[STR-010]] `unavailable`。附加字段按泳道:runs → `teamsScanned`;feedback → `entries`。降级规则:单泳道失败标注后继续(FR-005),禁止整束失败。

## E5. evidenceState 七态

[[STR-001]] `Present` / [[STR-002]] `Wired` / [[STR-003]] `Exercised` / [[STR-004]] `Outcome-supported` / [[STR-005]] `Missing` / [[STR-006]] `Unobserved` / [[STR-007]] `Not applicable`。

语义全量移植上游 `models/agent-work-loop.md:97-103`,定义文本落 `skills/collect-evidence/references/evidence-discipline.md`;消费方不得裁剪/重定义(FR-005)。

## E6. manifest.json

| 字段 | 类型 | 约束 |
|------|------|------|
| runId / target / created | string | 同 E1/E2 |
| lanes | object | 每泳道:status + 失败原因(unavailable 时必填 reason)+ 引擎调用摘要(argv 首元素、退出码) |
| engine | object | `{nodeVersion?, engineSubsetPath, upstreamCommit}` |
| findingsDigest | string | 与 findings.json 一致(交叉校验) |

## E7. 存储索引(index.json)

`.specify/memory/evidence/index.json`,仿 feedback index:`{store:"evidence", updated, entries:[{runId, target, created, lanesSummary, file}]}`。由 collect 追加、list/latest 消费;reindex 语义暂不提供(目录即真相,索引损坏可重建——实现为 collect 时全量重扫兜底)。

## E8. 干预台账(intervention.json)

improve 消费层产物,落 `.specify/memory/evidence/<baseline-run-id>/intervention.json`(附着于基线运行):

| 字段 | 类型 | 约束 |
|------|------|------|
| targetFinding | string | 基线 findings 中的证据条目 id(必须可解析) |
| change | string | 定向修改描述(脱敏) |
| baselineRunId | string | = 所在目录 runId |
| expectedSignal | object | `{signalKey, direction}` direction ∈ improve/reduce |
| verdict | enum? | compare 后写回:[[STR-004]] `Outcome-supported` 或 [[STR-006]] `Unobserved`;缺省=未验证 |

## E9. UPSTREAM 溯源台账(UPSTREAM.md)

`scripts/js/better-harness/UPSTREAM.md`,人读 Markdown,必填节:源仓库、基线 commit(`b2e621d`)、复制日期、子集清单(目录级 + agent-lint 说明)、排除清单、本地修改日志(表格:日期/文件/动机/是否可回馈上游)。每次本地修改追加一行(FR-002)。

## 关系图(文字)

- E1 包含 E2(1:1)、E6(1:1)、lanes/*.json(1:N)、E8(0:1)。
- E2 包含 E3(1:N);E3 归属 E4 某泳道、携带 E5 状态。
- E7 索引全部 E1。
- E9 治理引擎子集,E6.engine.upstreamCommit 引用其基线 commit。
- E8.targetFinding → E3.id(跨文件引用,compare 时校验存在性)。
