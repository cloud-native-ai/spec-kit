# Contract — Archive Manifest（`archive-manifest.json` 的固定名、封闭字段集与校验）

**Feature**: 100-seal-slice-archive（bound Feature 099） | **Date**: 2026-11-11 | **Plan**: [plan.md](../plan.md)
**Owns**: 归档清单的固定名与位置、顶层与嵌套字段的**封闭集**、序列化与摘要约定、确定性与校验纪律、合并清单摘要对照。动作语义归 `archive-actions.contract.md`；载体名册与解析定义归 `reference-classification.contract.md`。

**C-201** — 固定名与位置：每个父 spec 一份，与合并清单并列。

归档清单 MUST 落父 spec 根目录的固定文件名 `archive-manifest.json`（[[STR-002]]），与 `merge-manifest.json` 并列。每个父 spec MUST 只有一份；MUST NOT 引入按运行、按分片或共享聚合的第二份清单。回滚移除该文件即恢复归档前的存在性（归档前它不存在；回滚配方与完成判据 owner = C-110）。

(FR-005)

**C-202** — 序列化与顶层键集是封闭集。

清单 MUST 以 `json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"` 序列化。顶层键集恰为：

```json
{
  "schema_version": 1,
  "spec": "<父 spec 目录名>",
  "spec_path": ".specify/specs/<父 spec 目录名>",
  "generated_by": {"engine": "seal-utils.py", "version": "<framework version>", "command": "seal-utils.py --action archive-apply --spec-dir .specify/specs/<父 spec 目录名>"},
  "pinned_commit": "<40 hex>",
  "order_basis": "<split-record | letter-order>",
  "order_source": "<声明来源字符串>",
  "slices": [],
  "references": {"rows": [], "runtime": []},
  "merge_manifest": {"path": "merge-manifest.json", "digest_before": "sha256:<hex>", "digest_after": "sha256:<hex>"},
  "checks": {},
  "digest": "sha256:<hex>"
}
```

未知顶层字段 MUST NOT 写入。读取侧对**每一层**封闭集（C-202…C-206）生效：任何层级的缺失或未知字段 MUST 以 exit `2`（`archive-manifest-invalid`）拒绝，MUST NOT 静默补默认值。`generated_by.command` 描述**落盘**清单的动作（`archive-apply`）；`archive-plan` 只在 stdout 报告同一候选，不落盘、不写清单。

(FR-005)

**C-203** — 逐片条目的字段集是封闭集。

`slices[]` 的每个元素恰含：`slug`、`from`、`to`、`order`、`file_count`、`files`、`merged_into_pointer`。`from = .specify/specs/<slug>`；`to = <spec_path>/slices/<slug>`；`files` 为 `[{path, sha256}]`，`path` 是该分片目录内相对 POSIX 路径，按 `path` 升序；`merged_into_pointer = {path: "<to>/requirements.md", line: <int>}` 指向归档后分片 `requirements.md` 的 `**Merged into**:` 标注行；该行由 099 的合并回写保证在归档前已存在（C-019 / data-model E14），归档动作 MUST NOT 创建它。`slices` 按 `order` 升序；`order` 为 1 起连续唯一整数；`file_count` MUST 等于该片 `files` 行数。`order_basis` 的取值谓词：父 `.specify/state/<parent>.md` 的拆分记录可读出 `proposed_slices` 时取 `split-record`，否则取 `letter-order`；`order_source` 记录声明来源（`split-record` 时为该状态文件的仓库根相对路径 + 字段名，`letter-order` 时为 `directory-name-order`）。未知字段 MUST NOT 写入。

(FR-004, FR-005)

**C-204** — 引用台账行的字段集与二值分类。

`references.rows[]` 的每个元素恰含：`carrier`（仓库根相对 POSIX 路径）、`line`（1 起行号）、`before`（命中整行原文）、`after`（改写后整行；`dated-preserved` 时与 `before` 相等）、`kind`（封闭二值 `live-rewrite` / `dated-preserved`）。每条扫描命中 MUST 恰有一行；二值互斥。`runtime-updated` / `absent` MUST NOT 出现在 `rows[]` 中（它们只属于 `references.runtime[]`）。

(FR-012, FR-016)

**C-205** — 运行期行的字段集与缺席语义。

`references.runtime[]` 的每个元素恰含：`carrier`（声明状态载体路径）、`status`（封闭二值 `runtime-updated` / `absent`）、`reason`（`absent` 时必填：状态根不可解析或记录缺席；`runtime-updated` 时为 `null`）、`updates`（`[{line, before, after}]`；`absent` 时为空数组；记录存在但零命中时 `status = runtime-updated` 且 `updates = []`，表示已核对）。行数 MUST 等于声明的运行期载体数；`absent` MUST NOT 改变退出码或阻断。

(FR-017)

**C-206** — `checks` 的字段集与闭环算术。

`checks` 恰含：`preconditions`（`merge_status`：string，取 `merged`/`not-applicable`；`open_conflicts`：int；`slices_closed`：bool；`dirty_spec_tree`：bool；`side_presence`：object，逐 slug → `source`/`destination`/`both`/`missing`）、`moved_files`、`live_rewrite`、`dated_preserved`、`unclassified`、`unresolved_before`、`unresolved_after`、`runtime_carriers`、`files_match`（bool：归档前后文件数、逐文件 sha256、相对路径集合三者相等）。三组算术 MUST 成立：`live_rewrite + dated_preserved = len(references.rows)`；`runtime-updated 行数 + absent 行数 = runtime_carriers`；`sum(slices[].file_count) = moved_files`。计数与布尔字段（`moved_files`、`live_rewrite`、`dated_preserved`、`unclassified`、`unresolved_before`、`unresolved_after`、`runtime_carriers`）类型 MUST 为 int，`files_match` MUST 为 bool。任一字段缺失或算术不成立 MUST 以 exit `2`（`archive-manifest-invalid`）阻断，MUST NOT 写出自相矛盾的清单。

(FR-016, SC-007)

**C-207** — 摘要、钉住提交与路径约定。

`digest` MUST 复用 099 C-034 的算法：剔除 `digest` 自身的排序紧凑 JSON 的 sha256，带 `sha256:` 前缀。`pinned_commit` MUST 是 apply 开始前 `git rev-parse HEAD` 的 40 位小写十六进制值；apply 本身 MUST NOT 提交。路径基准是**逐字段**的：仓库根相对 POSIX 字段 = `spec_path`、`slices[].from`、`slices[].to`、`slices[].merged_into_pointer.path`、`references.rows[].carrier`、`references.runtime[].carrier`；分片目录内相对字段 = `slices[].files[].path`；父 spec 目录内相对字段 = `merge_manifest.path`（固定 `"merge-manifest.json"`）。MUST NOT 出现绝对路径、`..` 段或反斜杠。清单 MUST NOT 含墙钟时间、运行主机、随机 id 或任何依赖运行时刻的字段。

(FR-005)

**C-208** — 确定性：同输入逐字节一致。

同一输入树上的两次 `archive-plan` MUST 产出逐字节一致的完整计划（含清单候选与台账顺序）；`archive-apply` 的只读阶段重算 MUST 与 `archive-plan` 一致；成功 apply 后重跑 MUST 零 diff。排序键 MUST 只取声明字段（路径、行号、`order`、`slug`），MUST NOT 取文件系统时间、目录枚举顺序或返回时刻。

(FR-005, SC-006)

**C-209** — 校验器只有一个：引擎读写共用同一路径。

清单的 schema 校验 MUST 只由 `seal-utils.py` 实现；`archive-plan`、`archive-apply` 与归档后的发现路径 MUST 共用同一校验函数，MUST NOT 新增独立校验器或引入 JSON Schema 依赖。契约测试 MUST 断言写出的键集等于 C-202…C-206 的各级封闭集，并断言在每一层注入未知字段或移除必填字段时读取 exit `2`。

(FR-005)

**C-210** — 清单是「旧路径 → 归档路径」的唯一解析通道。

日期化记录中的旧分片路径 MUST 只经本清单的 `from → to` 前缀映射解析：`from` MUST 按路径段边界匹配（`from` 后为 `/` 或字符串结束），多个 `from` 可匹配时取最长；映射 MUST 唯一（同一命中只有一个 `from` 可匹配），歧义 MUST 以 exit `2`（`archive-manifest-invalid`）拒绝；替换后的目标 MUST 在树上存在。MUST NOT 为实现解析而改写日期化记录，MUST NOT 建立第二份映射表或派生索引。活引用 MUST 已由 apply 改写为直接存在的归档路径，不依赖映射。

(FR-014, FR-015)

**C-211** — 合并清单只改路径形态值，摘要前后对照入清单。

`archive-apply` 对父 `merge-manifest.json` 的更新 MUST 限定为**匹配 `.specify/specs/<任一分片 slug>[/…]` 形态的整个字符串值**（不按子串部分替换、按路径段边界匹配、同一值仅替换一次）：引擎 MUST 对该清单全文做模式扫描枚举（不依赖手写字段清单，`slices[].carrier_tasks`、`dispositions[].evidence[]`、`artifacts[].pointer.paths[]` 只是该集合的已知实例）；匹配集合 = 允许差异集，匹配集合之外的每个值 MUST 与归档前逐字节一致。合并结论（`merge` 键下全部字段）、`checks` 计数字段、`conflicts`、`id_maps`、分片顺序与 `retention` MUST 保持不变；摘要 MUST 按 099 C-034 的既有算法重算。本清单的 `merge_manifest.digest_before/after` MUST 记录更新前后的摘要值。

(FR-018)

**C-212** — 版本与演进纪律。

`schema_version` MUST 从 `1` 起；本特性只写 `1`。字段集合的增删改 MUST 走本契约页修订，MUST NOT 在读写代码中就地扩展。读取侧遇到更高版本 MUST 以 exit `2`（`archive-manifest-invalid`）拒绝，MUST NOT 猜测兼容。

(FR-005)
