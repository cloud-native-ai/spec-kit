# Data Model — 100-seal-slice-archive

**Feature**: 100-seal-slice-archive（bound Feature 099） | **Date**: 2026-11-11 | **Plan**: [plan.md](plan.md)
**Authority**: `requirements.md`（FR-001…FR-028）是语义 owner；`contracts/` 是符合性 owner；本页只是设计侧的实体/字段/校验视图，不复述条款正文。

本特性的「数据」全部是**文件承载的记录**：一份按父 spec 的归档清单、一份既有合并清单的路径字段修正、移动后的分片目录、以及 stdout 上的计划/拒绝报告。没有数据库、服务或共享可变聚合。并发安全按「一 spec 一清单」满足（AGENTS.md § Concurrent Development Safety）。

---

## 1. 实体清单

| # | 实体 | 承载 | 生命周期 | 主要 FR |
|---|------|------|----------|---------|
| E1 | Slice Set（分片集） | 从 `merge-manifest.json` + 归档清单 + 目录树派生（不落独立文件） | 每次 action 重新派生 | FR-006, FR-019 |
| E2 | Archive Plan（只读计划） | `archive-plan` 的 stdout（`--json` 负载）；不落盘 | 查询即生即弃 | FR-008, FR-009 |
| E3 | Archive Manifest（`archive-manifest.json`） | 父 spec 目录固定文件名 | 每父 spec 一份；apply 新建，回滚移除 | FR-005, FR-016, FR-018 |
| E4 | Archived Slice Entry | E3 的 `slices[]` 行 | 随 E3 | FR-004, FR-005 |
| E5 | Reference Update Row | E3 的 `references.rows[]` 行 | 随 E3 | FR-012…FR-016 |
| E6 | Runtime State Record | E3 的 `references.runtime[]` 行；对应 `.specify/state/**` 的可选更新 | 随 E3；运行期文件不进版本库 | FR-017 |
| E7 | Carrier Roster（载体封闭集） | `contracts/reference-classification.contract.md`（owner）；扫描时只读 | 随框架分发 | FR-012, FR-013, FR-014 |
| E8 | Archive Action Verdict | `archive-plan` / `archive-apply` 的 stdout；拒绝零持久化 | 即生即弃 | FR-007…FR-011 |
| E9 | Merge Manifest Path-Field Amendment | `merge-manifest.json` 的路径形态值 + 重算 `digest` | 每次 apply 覆盖为当前清单 | FR-018 |
| E10 | Rollback Recipe（回滚配方） | `contracts/archive-actions.contract.md` + `quickstart.md` 的文档化步骤（不落新文件） | 文档面；由 E3 的事实驱动 | FR-011 |

---

## 2. E1 — Slice Set（派生规则）

| 字段 | 类型 | 说明 |
|------|------|------|
| `slug` | string | 分片目录名原样（如 `074a-authorized-routing`） |
| `source` | path | `.specify/specs/<slug>`（归档前） |
| `destination` | path | `.specify/specs/<parent>/slices/<slug>`（归档后） |
| `order` / `order_basis` / `order_source` | int / string / string | 与合并清单同源（`.specify/state/<parent>.md` § 拆分记录，缺席回退字母序） |
| `closed` | bool | 按 099 既有闭合判据（任务行闭合 + `**Merged into**` 标注） |

**派生顺序**：① 先读父 `merge-manifest.json` 的 `slices[]`（slug 与顺序）；② 若父根存在 `archive-manifest.json`，校验其 `slices[]` 与 ① 的 slug 集一致，并用 `to` 作为实际路径；③ 目录状态按「源存在 / 目标存在」二值矩阵判定（V3）。MUST NOT 把 `slices/` 目录读成新的分片候选。

## 3. E3 — Archive Manifest（`archive-manifest.json`）

**固定名与位置**：父 spec 根（与 `merge-manifest.json` 并列）。**序列化**：`json.dumps(indent=2, sort_keys=True, ensure_ascii=False) + "\n"`。**字段是封闭集**（owner：`contracts/archive-manifest.contract.md` C-202…C-207）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema_version` | int | ✓ | 从 `1` 起；本特性只写 `1` |
| `spec` | string | ✓ | 父 spec 目录名 |
| `spec_path` | string | ✓ | 仓库根相对 POSIX 路径（`.specify/specs/<parent>`） |
| `generated_by` | object | ✓ | `{engine, version, command}`；`command` 为可复跑的单行调用 |
| `pinned_commit` | string | ✓ | apply 前的 `git rev-parse HEAD`（40 hex）；回滚的 `git restore --source` 目标 |
| `order_basis` / `order_source` | string | ✓ | E1 的顺序依据与来源 |
| `slices` | array | ✓ | E4 行，按 `order` 升序 |
| `references` | object | ✓ | `{rows: [E5], runtime: [E6]}` |
| `merge_manifest` | object | ✓ | `{path, digest_before, digest_after}`（E9 的摘要对照） |
| `checks` | object | ✓ | 前置与算术读数（见 § 6） |
| `digest` | string | ✓ | C-034 算法：剔除 `digest` 的排序紧凑 JSON 的 `sha256`，带 `sha256:` 前缀 |

**禁止字段**：任何墙钟时间、运行主机、随机 id、绝对路径。同一输入两次 `archive-plan`（及 apply 前的重算）MUST 逐字节一致（FR-005、SC-006）。

## 4. E4 — Archived Slice Entry

| 字段 | 类型 | 说明 |
|------|------|------|
| `slug` | string | 原分片目录名 |
| `from` / `to` | string | 仓库根相对 POSIX 路径；`to = <spec_path>/slices/<slug>` |
| `order` | int | 与 E1 一致 |
| `file_count` | int | 移动文件数（运行期探针） |
| `files` | array | `[{path, sha256}]`，`path` 为**分片目录内**相对路径（移动后仍同义），按 `path` 升序 |
| `merged_into_pointer` | object | `{path, line}`：归档后分片 `requirements.md` 中 `**Merged into**:` 标注的位置；`path` 为 `to/requirements.md` |

## 5. E5 / E6 — Reference Ledger

**E5 Reference Update Row（文本命中行）**

| 字段 | 类型 | 说明 |
|------|------|------|
| `carrier` | string | 载体文件的仓库根相对路径 |
| `line` | int | 命中所在行号（1 起） |
| `before` / `after` | string | 命中前后**整行**文本；`dated-preserved` 行两者相等 |
| `kind` | string | 封闭二值：`live-rewrite` \| `dated-preserved` |

**E6 Runtime State Record（运行期载体行）**

| 字段 | 类型 | 说明 |
|------|------|------|
| `carrier` | string | 声明的运行期载体路径：`.specify/state/<parent>.md` 或 `.specify/state/<slug>.md`（合计 1 + 分片数 个载体） |
| `status` | string | 封闭二值：`runtime-updated` \| `absent` |
| `reason` | string | `absent` 时必填：状态根不可解析 / 记录缺席；`runtime-updated` 时为 `null` |
| `updates` | array | `runtime-updated` 时的 `[{line, before, after}]`；`absent` 时为空数组 |

## 6. E3.checks（前置与算术读数，封闭字段）

| 字段 | 类型 | 含义 |
|------|------|------|
| `preconditions` | object | FR-006 五条件的具名读数：`merge_status`（string：`merged`/`not-applicable`）、`open_conflicts`（int）、`slices_closed`（bool）、`dirty_spec_tree`（bool）、`side_presence`（object：逐 slug → `source`/`destination`/`both`/`missing`） |
| `moved_files` | int | 移动文件行数；MUST 等于全部 `files` 行数之和 |
| `live_rewrite` / `dated_preserved` / `unclassified` | int | 引用台账的三类计数；`unclassified` MUST 为 0 |
| `unresolved_before` / `unresolved_after` | int | plan 时与 apply 后复验的未解析数；两者 MUST 为 0 |
| `runtime_carriers` | int | 声明的运行期载体数（1 + 分片数） |
| `files_match` | bool | 归档前后文件数、逐文件 sha256、相对路径集合三者相等 |

**闭环算术（V9）**：`live_rewrite + dated_preserved = references.rows` 行数；`runtime-updated + absent = runtime_carriers`；`sum(file_count) = moved_files`。

## 7. E8 — Archive Action Verdict（stdout）

`--json` 负载沿用 099 引擎的 `_payload` 形态：`{action, spec_dir, verdict, outcome, exit, conditions[], …}`。本特性的 `verdict` 封闭为 `ok` / `refused` / `error`；成功语义的**具名结论**由独立字段 `outcome` 承载，封闭四值 `would-archive`（仅 `archive-plan`，表示可执行且无阻断）/ `archived` / `already-archived`（apply 幂等；`archive-plan` 在已归档树上也 MUST 报告该结论，零待移动、零未解析、零写入）/ `not-applicable`；`refused` 与 `error` 的 `outcome` 为 `null`，其具名 reason 集见 `contracts/archive-actions.contract.md` C-103。**拒绝（exit 1）与错误（exit 2）零持久化**：无拒绝记录、无空清单、无第二份台账。

## 8. E9 — Merge Manifest Path-Field Amendment

- **只改**匹配 `.specify/specs/<任一分片 slug>[/…]` 形态的字符串值（引擎对清单全文做模式扫描枚举；匹配集合 = 允许差异集；`slices[].carrier_tasks`、`dispositions[].evidence[]`、`artifacts[].pointer.paths[]` 只是已知实例）。
- **不改**匹配集合之外的每个值（含裸 slug：`slices[].slug`、`artifacts[].sources[]`、`artifacts[].per_slice[].slice`、`id_maps` 键）、合并结论（`merge`）、`checks` 计数字段、冲突、ID 映射、分片顺序与 `retention`。
- `digest` 按 C-034 原算法重算；E3 的 `merge_manifest.digest_before/after` 记录前后值。

## 9. 状态机（归档生命周期）

```text
(no manifest, all slices at source)      --archive-plan--> would-archive（只读）
would-archive --archive-apply--> archived（写批次成功；manifest 落盘）
archived      --archive-apply--> already-archived（exit 0；零写入）
archived      --archive-plan--> already-archived（exit 0；只读；零待移动零未解析）
any state     --refusal (exit 1)--> unchanged（零持久化）
any state     --input error (exit 2)--> unchanged（写批次内失败则按原字节恢复）
(no manifest, same slice both sides)     --任何动作--> destination-exists (exit 1)
(no manifest, slice absent both sides)   --任何动作--> error (reason: slice-missing; exit 2)
(no manifest, slices split across sides) --任何动作--> error (reason: partial-archive; exit 2)
(manifest, tree disagrees with manifest) --任何动作--> error (reason: archive-drift; exit 2)
empty slice set                          --任何动作--> not-applicable (exit 0；零写入零清单；先于上述 no-manifest 行求值)
```

## 10. 校验规则

- **V1** 目的地恰为 `<spec_path>/slices/<slug>`；目录名与内部相对树不变（FR-002）。
- **V2** 纯移动：在被移动分片路径集上，每个被移动文件在 `git diff --name-status -M <pinned_commit>` 中是一条重命名对，零纯删除（比较基 = apply 前提交；`git mv` 的索引写入不改变该读数）；批次内清单 A 与活引用载体 M 按声明集合断言，全局零 D（FR-003）。
- **V3** 每个分片在源与目标中恰在一侧；同一分片双侧 → `destination-exists`（exit 1）；同一分片双侧皆无 → `slice-missing`（exit 2）；跨分片混合（一片在源、一片在目标）→ `partial-archive`（exit 2）（FR-006；Edge Cases）。
- **V4** 零丢失：`file_count`、逐文件 `sha256`、相对路径集合归档前后相等；不等即失败并回滚（FR-004）。
- **V5** 清单字段是封闭集；未知字段 MUST NOT 写入；读取侧遇未知或缺失字段 exit 2（FR-005）。
- **V6** 清单无墙钟字段；同输入两次 plan 逐字节一致（FR-005、SC-006）。
- **V7** 每条扫描命中恰有台账一行，`kind` 二值互斥；封闭集外命中 → `unclassified-reference` 阻断（FR-012、FR-016）。
- **V8** 活引用直接解析到存在的归档路径；日期化引用保持原字节且经 `from → to` 映射解析；两者之外即未解析，apply 拒绝（FR-014、FR-015）。
- **V9** 三组闭环算术成立；任一行缺失或算术不成立即阻断（FR-016）。
- **V10** 运行期载体各一行 `runtime-updated` / `absent`；缺席不改退出码（FR-017）。
- **V11** 合并清单只改路径形态值；摘要按 C-034 重算并记录前后值（FR-018）。
- **V12** 归档后 `merge-plan` / `merge-apply` / `seal` 的分片集、顺序与 P0 读取面不变（FR-019）。
- **V13** 写面白名单封闭：移动仅 `archive-apply` 且目标限父 spec 的 `slices/`；无删除 / push / **注册表状态写**（「状态写」= 对 `.specify/features.md`、特性详情状态、父 spec 的 `seal.md` 回执的状态字段写入；`.specify/register.md` 的推荐行文本改写属活引用改写，不属本项；`.specify/state/**` 的运行期载体更新按 FR-017 单独允许且不属本项）（FR-028）。
- **V14** 回滚按文档步骤后，父 spec、分片与全部 live 载体相对 `pinned_commit` 的树零差异（`git diff --exit-code <pinned_commit> -- <parent> <slices> <live carriers>` 为空），且清单 `references.rows[]` 的 `before` / `after` 逐行核对成立（FR-011、SC-010）。

## 11. 实体 → 条款映射

| 实体 | Owner 条款 |
|------|-----------|
| E1 Slice Set | C-102, C-112 |
| E2 Archive Plan | C-103, C-104 |
| E3 Archive Manifest | C-201…C-207 |
| E4 Archived Slice Entry | C-203 |
| E5 / E6 Reference Ledger | C-204, C-205, C-307…C-309 |
| E7 Carrier Roster | C-301…C-307 |
| E8 Verdict | C-103, C-107 |
| E9 Merge Manifest Amendment | C-211 |
| E10 Rollback Recipe | C-106, C-110 |
