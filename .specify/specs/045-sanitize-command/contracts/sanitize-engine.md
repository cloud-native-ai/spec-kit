# Contract: sanitize-utils.py 引擎 CLI(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene  
**消费方**: `/speckit.sanitize` 命令模板、tests/contract/test_sanitize_engine_contract.py、tests/unit/test_sanitize_engine.py

## 1. CLI 形态

- 引擎为 `scripts/python/sanitize-utils.py`,stdlib-only,Python ≥ 3.8,镜像至 `.specify/scripts/python/sanitize-utils.py`(sync-mirrors strict 对)。
- 参数风格沿用 feedback-utils.py:`--action <name>`(必填)+ `--workspace-root <path>`(默认 `.`)+ `--format text|json`(引擎输出恒 JSON)。
- `--action` 取值恰为 4 个:`collect` / `record` / `status` / `apply`。未知 action 退出 1(CliError,输出 `{"error": ...}`)。

## 2. 动作语义

### collect
- 输入:`--workspace-root`,可选 `--roots <csv>`(限定资料根子集;缺省=全部根)。
- 行为:运行全部确定性检查(契约 C-4);将确定性发现按合并语义写入台账(契约 C-2);采集语义候选及其证据包(仅内存输出,不写台账)。
- 输出信封:

```json
{
  "ok": true,
  "store": { "pending": 12, "resolved": 3, "byCategory": {...}, "bySeverity": {...} },
  "deterministic": { "detected": 10, "merged": 7, "autoResolved": 2 },
  "semanticCandidates": [ { "material": ".specify/memory/todo/xxx.md", "claims": ["五项未落地"], "evidencePack": { "gitLog": ["1a090c72 ..."], "pathExistence": {...} } } ],
  "notes": ["git unavailable - semantic detection degraded"]
}
```

- 无 git 可用时:`semanticCandidates` 为空且 `notes` 含降级声明;确定性检查照常(FR 边界:非 git 环境语义检测降级)。

### record
- 输入:`--file <path>`(agent 产出的语义判定 JSON)+ `--workspace-root`。
- 文件 schema:`{ "findings": [ { ...Sanitize Finding, detection="semantic"... } ] }`;schema 校验失败 → 退出 2,不落盘任何条目(全有或全无)。
- 行为:按合并语义并入台账;输出更新后 store 摘要。
- 判定为"证据不足"的候选不得出现在 findings 中(不构成发现,仅在运行摘要呈现计数)。

### status
- 零写入;输出台账摘要(按 state/category/severity 计数 + pending 目标列表摘要)。

### apply
- 输入:`--plan <path>` + `--workspace-root`。
- 前置校验(任一失败 → 退出 2,零执行):plan 为合法 JSON;`confirmed === true`;每个 findingId 存在于台账且 state=pending;disposition 与台账建议一致或为 dismiss;target 落在资料根白名单内(见 §4 范围红线)。
- 执行:`delete`(删除文件/目录,仅限空目录或单文件材料)、`archive`(移动至 `.specify/archive/<原相对路径>`,自动创建父目录)、`repair`/`dismiss`(仅状态更新;repair 的内容修改由命令流程中 agent 先行完成)。
- 输出:Execution Report 信封(data-model §5);成功项状态置 resolved,失败项保持 pending 并追加失败备注。
- 全程在单次调用内完成;失败不回滚已成功项,逐项如实报告。

## 3. 退出码

| 码 | 语义 |
|----|------|
| 0 | 成功(含"发现为空""无可执行项") |
| 1 | CliError(参数/文件不可读/JSON 解析失败) |
| 2 | 校验失败(未确认计划、schema 违例、目标越界、台账不一致) |

## 4. 范围红线(引擎强制)

- **写入范围**:`collect`/`record`/`apply` 对文件系统的写入仅限 `.specify/memory/sanitize/`(台账/计划)与 `apply` 的 delete/archive 处置目标;`status` 零写入。
- **被检材料零修改**:collect/record 阶段不得修改任何资料根本体(SC-002 机械验证锚点)。
- **目标白名单**:apply 的 delete/archive 目标必须命中资料根(data-model §4);显式拒绝 `src/`、`tests/`、`node_modules/`、`.git/` 下任何路径(退出 2)。
- **递归豁免**:引擎不得将 `.specify/memory/sanitize/` 自身纳入扫描。

## 5. 复用接线(Tool Reuse,宪法 XII)

- docs 树死引用:导入 `docs_utils`(同目录模块)的链接校验能力,不重复实现;docs lane 的发现 `evidenceRefs.kind="output"`,ref 记 `docs-utils:broken-links`。
- 镜像漂移:子进程调用 `sync-mirrors.py --check`(JSON 输出),解析 MISS/DIFF/ORPHAN 项;孤儿目录比对与 obsolete-registry 交叉核对由本引擎补充实现(sync-mirrors 不覆盖该面)。
- git 证据:子进程 `git log --oneline -n 20 --since <声明日期> -- <相关路径>`,输出截断为摘要行;超时/失败按"证据不足"处理,不得臆造。

## 6. 契约测试锚点

- `test_sanitize_engine_contract.py` 断言:4 action 恰好存在且无多余;退出码表;collect 写入仅台账(夹具快照);apply 无 confirmed 拒绝;越界 target 拒绝;record schema 违例全拒绝。
- 本契约与 quickstart.md 中全部可执行 CLI 示例由该测试钉死(flags/arg 语法不漂移)。
