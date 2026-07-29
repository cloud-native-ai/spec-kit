# Contract: evidence-utils.py CLI 表面

> 合同 ID 前缀 C-E。pytest 合同测试:`tests/contract/test_evidence_utils_cli.py`。风格基线:feedback-utils.py / docs-utils.py(--action + 纯函数派发 + JSON stdout)。

## C-E1 调用形态

`python3 .specify/scripts/python/evidence-utils.py --action <doctor|collect|list|latest|compare> [options]`。`--action` 必填且枚举封闭;未知 action 退出码 2(argparse 默认)。所有 action 输出为 UTF-8 JSON(`ensure_ascii=False, indent=2`)到 stdout,以换行收尾。

## C-E2 stdlib-only 与零网络

脚本 MUST 仅 import Python 标准库;MUST NOT 发起任何网络请求。对 Node 的调用 MUST 为 `subprocess.run(argv_list, shell=False)`(argv-array;合同测试静态断言源码无 `shell=True` 且无 `requests/urllib.request.urlopen` 等网络调用)。

## C-E3 doctor

无必选参数。输出 MUST 含:`node`(`{available: bool, version?: string, satisfies: bool}`,satisfies 按引擎 engines 要求 ≥22.20.0 <25 判定)、`engineSubset`(`{present: bool, path, upstreamCommit?}`)、`platforms`(八工具各 `{sessionStore: detected|not-detected}`,按各工具本地落盘探测)、`lanes`(五泳道各 available/unavailable 及原因)。doctor MUST 只读、零副作用、退出码 0(探测到缺失不是错误)。

## C-E4 collect

参数:`--target <unit-id>`(必填,词汇同 C-F2)、`--lanes <csv|all>`(默认 all)、`--since/--until`(可选 ISO 8601)、`--depth <quick|normal>`(默认 normal)、`--platform <csv>`(默认 qoder,session/assets 泳道用)。行为:

1. 逐泳道采集;单泳道失败 MUST 标注(manifest reason)后继续,MUST NOT 使整次 collect 失败(FR-005)。
2. 产出 E1 运行目录(findings/manifest/lanes)并更新 index(C-F12)。
3. 全部五泳道均 unavailable 时仍产出合法 findings(evidence 空、lanes 全 unavailable),退出码 0;仅当无法写入存储目录时非零退出。
4. 落盘前 MUST 施加字段白名单 + 脱敏过滤(C-F7);Node 泳道原始 envelope 中的白名单外字段 MUST 剥离后才进 findings(lanes/*.json 保留 envelope 但同样过脱敏)。
5. 输出:`{runId, path, lanes: {…status…}, evidenceCount, findingsDigest}`。

## C-E5 list

参数:`--target`(可选过滤)、`--limit`(默认 20)。输出 `{entries: [...]}`(按 created 降序)。只读。

## C-E6 latest

参数:`--target`(必填)、`--max-age-days`(默认 7)。输出 `{runId, path, created, ageDays, stale: bool}`;`stale=true` 时 MUST 附 `warning` 字段(超龄警告,FR-003);无任何历史运行时输出 `{found: false}` 且退出码 0(消费方据此决定采集)。

## C-E7 compare

参数:`--target`(必填)、`--baseline <runId>`(可选,默认取次新)、`--current <runId>`(可选,默认取最新)。输出:`{baseline, current, signalDeltas: [{lane, signalKey, before, after}], newEvidence: [...], resolvedEvidence: [...], intervention?: {targetFinding, expectedSignal, verdict}}`。当 baseline 目录含 intervention.json 时 MUST 依 expectedSignal 判定 verdict:预期方向改善 → `Outcome-supported`;无可比信号 → `Unobserved`;并把 verdict 写回 intervention.json(compare 是唯一允许写 E8.verdict 的动作)。两个 runId 任一不存在 → 退出码 1 + `error` JSON。

## C-E8 引擎调用映射(collect 内部)

| 泳道 | argv(相对 engineSubsetPath) |
|------|------------------------------|
| session | `node session-analysis.mjs facts --platform <p> --workspace <root> [--since/--until] --format json` |
| project | `node core-change-watch/project-profile.mjs --json` + `git-history-profile.mjs --json`(depth=normal 时加 `evidence-pack.mjs`;dependency-governance 仅 normal) |
| assets | `node coding-agent-practices/asset-baseline.mjs <platform> --workspace <root> --json` |

引擎子进程超时 MUST 有上限(单调用 120s);超时按泳道失败处理(标注后继续)。

## C-E9 runs 泳道(纯 Python)

扫描 `.specify/teams/*/`:读 `runs/*-report.md`(存在性与计数)、`STATE.md` 的 `## Post-Run Critique` 追加行、`run-log.jsonl`(七字段行:cycle/maturity/items_found/actions_taken/escalations/tokens_estimate/outcome)。文件缺失的团队 MUST 按 partial 处理(如仅有 runs/ 无 STATE.md),MUST NOT 跳过整个泳道;无 teams 目录 → 泳道 unavailable(reason 注明)。

## C-E10 feedback 泳道(纯 Python)

读 `.specify/memory/feedback/index.json` 与条目 frontmatter/正文要点;条目数动态计数;对 `## Optimization Points` 做跨条目重复主题聚合,重复出现的优化点 MUST 以 `signals.recurrence`(次数)呈现,evidenceRefs 指向条目相对路径。index 缺失时回退全量扫描 md 文件(泳道 partial)。

## C-E11 退出码总表

0 = 成功(含合法降级与 found:false);1 = 运行错误(存储不可写、runId 不存在等,stderr/stdout 附 error JSON);2 = 参数错误(argparse)。
