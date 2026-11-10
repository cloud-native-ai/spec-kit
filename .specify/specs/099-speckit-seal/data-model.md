# Data Model — 099-speckit-seal

**Feature**: 099 Speckit Seal | **Date**: 2026-11-10 | **Plan**: [plan.md](plan.md)
**Authority**: `requirements.md`（FR-001…FR-028）是语义 owner；`contracts/` 是符合性 owner；
本页只是设计侧的实体/字段/校验视图，不复述条款正文。

本特性的「数据」全部是**文件承载的记录**：一个状态值、两份按 spec 的记录文件、一份 stdout 拒绝报告，
以及从既有测量面逐字复制的一小块回执。没有数据库、服务或共享可变聚合。并发安全按「一 spec 一记录文件」
满足（AGENTS.md § Concurrent Development Safety）。

---

## 1. 实体清单

| # | 实体 | 承载 | 生命周期 | 主要 FR |
|---|------|------|----------|---------|
| E1 | Feature Status Value（域成员 `Sealed`） | `shared/workflow/acceptance-hardening.md` § Feature Status（owner）+ 各 carrier | 随框架分发 | FR-001…FR-004 |
| E2 | Seal Record（`seal.md`） | 父 spec 目录固定文件名 | 每 spec 当前回执；审计更正后原子替换 | FR-010 |
| E3 | Merge Manifest（`merge-manifest.json`） | 父 spec 目录固定文件名 | 每次 `merge-apply` 覆盖为当前清单 | FR-018 |
| E4 | Slice / Slice Set | 从 `.specify/specs/` 派生（不落独立文件） | 派生量，写入 E3 | FR-011 |
| E5 | Artifact Merge Record | E3 的 `artifacts[]` 行 | 随 E3 | FR-012 |
| E6 | ID Mapping Record | E3 的 `id_maps{}` | 随 E3 | FR-014, FR-015 |
| E7 | Conflict | E3 的 `conflicts[]` | 开放即阻断；解决留痕 | FR-017 |
| E8 | Disposition Record（拆前行处置） | E3 的 `dispositions[]` | 随 E3；不复写原行 | FR-018, FR-026(e) |
| E9 | Closure Receipt（逐字复制） | E2 的 `closure{}` 块 | 随 E2（每次判定实时复制） | FR-007, FR-010 |
| E10 | Claimed Status Pair | `.specify/features.md` 行 + `.specify/features/<ID>.md` | 既有状态面 | FR-004, FR-005 |
| E11 | Archive Gate Verdict | `archive-gate` 的 stdout（不落盘） | 查询即生即弃 | FR-023 |
| E12 | Refusal Report | `seal` / `merge-*` 的 stdout（不落盘） | 拒绝即生即弃；调用方可捕获 | FR-009 |
| E13 | Round Adjudication Item（074 回合） | E3 `conflicts[]` / `dispositions[]` / E2 `waivers[]` 的并集投影 | 与回合同生 | FR-026, FR-027 |
| E14 | Slice Merge Marker | 分片 `requirements.md` 头部一行 | 一次写入，永久指针 | FR-018 |

---

## 2. E1 — Feature Status Value（`Sealed`）

| 字段 | 值 | 说明 |
|------|----|------|
| `value` | `Sealed`（STR-001） | 值域**恰好**新增这一个成员 |
| `from` | `Ready for Review` | 唯一合法前驱 |
| `owner_command` | `/speckit.seal` | 该转移的唯一 owner |
| `terminal` | `true` | 无前向出口 |
| `audit_correction` | `Sealed → Ready for Review` | 唯一后向转移；必须携带使原封装结论不成立的证据，并同时落在 E10 两载体 |

**状态机（新增部分；其余转移由既有 owner 持有，本页不复制）**

```text
Draft → Planned → Implemented → Ready for Review → Sealed   (terminal; this feature)
             └──→ Blocked ──→ Implemented                  (existing branches, shown for completeness)
Implemented ── audit correction ──→ Blocked                 (existing; evidence required)
Ready for Review ──→ Completed                              (legacy only; closed for new work)
Sealed ── audit correction (evidence required) ──→ Ready for Review
```

**校验规则**

- V1 值域成员恰 +1；不存在第二个终态标签用于新工作（FR-001、FR-003）。
- V2 `Sealed` 行不参与 `Ready for Review → Completed`；后者对新工作关闭（FR-003）。
- V3 状态写入只落 E10 两载体 + E2；不建新注册表/台账/状态脊（FR-004）。
- V4 任一 carrier 移除 `Sealed` 时漂移守卫转红并点名该处（FR-001、SC-008）。

## 3. E2 — Seal Record（`seal.md`）

固定文件名、父 spec 目录。机器可读核心（**封闭字段集**，行内 `key: value` 或围栏 JSON 等价）：

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `judged_at` | ISO-8601 UTC | 引擎时钟（唯一允许的时间源；仅入档，不参与任何排序） | 判定时刻 |
| `pinned_commit` | git SHA | `git rev-parse HEAD`（判定时刻） | 钉住的提交 |
| `from_status` / `to_status` | 状态字面量 | E10 | 判定时的 from/to |
| `review.paths[]` | 路径列表 | 当前 `review.md` / `code-review.md`（归档记录不计） | 所引 review 记录 |
| `review.counts` | `{p0_unresolved, p1, p2, blocking}` | review 摘要行 | 计数 |
| `closure.exit_code` | `0|1|2` | 闭包引擎子进程 | 回执退出码 |
| `closure.final_path` | 七键 `{pass,blocked,deferred,partial,fail,unknown,total}` | 闭包引擎 JSON **逐字复制** | 不重算 |
| `closure.command` | 命令行 | 调用方 | 可复现 |
| `merge.manifest` | 路径 | 父 spec 目录 | 合并清单指针 |
| `merge.slices[]` | slug 列表（声明顺序） | E3 | 分片列表 |
| `merge.status` | `merged` / `not-applicable` | E3（`not-applicable` 必须带 `basis`） | 合并完成度 |
| `merge.basis` | 文本（仅 `not-applicable`） | 判定依据（分片集合为空的两条件判空结果） | 空合并的显式依据 |
| `waivers[]` | `{finding, form, source}` | 用户裁定载体 | 命中的豁免引用 |
| `engine` | `{identity, version, command}` | 引擎自述 | 引擎身份 |
| `supersedes` | 前回执 `pinned_commit`（可选） | 审计更正后重封装 | 仅重封装时出现 |

**校验规则**

- V5 字段集封闭（封闭性由 C-032 声明；FR-010 给出「至少含」下限）；未知字段不写入。
- V6 只引用测量来源（review 文件、闭包回执、manifest、豁免载体），不复述第二份测量（FR-010、FR-019）。
- V7 当前回执唯一：审计更正后再次封装**原子替换**本文件并写 `supersedes`；历史由 git 承载（FR-010）。
- V8 与 E10 的状态面**同批落盘**；任一写入失败按原字节恢复已写文件并以 exit 2 结束（FR-009）。

## 4. E3 — Merge Manifest（`merge-manifest.json`）

固定文件名、父 spec 目录、机器可读、**键序稳定**（`json.dumps(indent=2, sort_keys=True, ensure_ascii=False)`）。

```
{
  "schema_version": 1,
  "spec": "<parent spec dir name>",
  "generated_by": {"engine": "seal-utils.py", "version": "<x.y.z>", "command": "<argv>"},
  "slices": [ {"slug": "...", "order": 1, "order_basis": "split-record|letter-order", "order_source": "<path#anchor>", "carrier_tasks": "<slice tasks.md path>", "retention": "pending-review"} ],
  "artifacts": [ {"name": "<artifact>", "action": "merge|create|keep|not-applicable", "basis": "<仅 not-applicable>", "sources": ["<slice>", ...], "per_slice": [ {"slice": "...", "present": true} ], "checks": {"...": "..."}} ],
  "factory_doc_resolutions": [ {"path": "...", "line": 0, "before": "...", "after": "...", "kind": "repoint|literal|user-waiver", "ref": "..."} ],
  "id_maps": { "<family>": [ {"slice": "...", "slice_id": "...", "parent_id": "...", "kind": "mapped|appended|localization"} ] },
  "conflicts": [ {"id": "CF-001", "artifact": "...", "unit": "...", "side_a": {"path": "...", "line": 0, "excerpt": "..."}, "side_b": {"...": "..."}, "candidates": ["..."], "status": "open|resolved", "resolution": {"kind": "user-ruling|canonical-map|literal|repoint", "ref": "..."}} ],
  "dispositions": [ {"disposition": "supersede", "superseded": {"path": "...", "line": 0}, "superseded_by": {"path": "...", "line": 0}, "evidence": ["..."], "guard_status": "retired|replaced|unchanged-with-reason"} ],
  "checks": {"id_continuity": "pass|fail", "duplicate_ids": 0, "dangling_refs": 0, "open_rows": 0, "dated_record_hashes_stable": true},
  "digest": "sha256:<...>"
}
```

**校验规则**

- V9 `artifacts[]` 的 `per_slice` 必须覆盖每个分片 × 每个候选输出件（`present` 真假都记录）；`not-applicable` 必须带 `basis`（FR-012、FR-018）。
- V10 `id_maps` 覆盖每个分片条目；家族至少 FR / SC / STR / 契约条款 / 任务行 / 实体 / 阶段检查点标识（FR-014）。
- V11 `conflicts[]` 每条含两侧摘录与候选处置；`status=open` 的条数 >0 时 `seal` MUST 阻断（FR-017、FR-009）。
- V12 `digest` 为剔除 `digest` 与时间键后的排序紧凑 JSON 的 sha256（复用 R-16 形态）。
- V13 `dispositions[]` 的 `superseded_by` 必须可解析；不可解析即冲突（R-15、FR-018）。
- V14 `checks.open_rows` 在父 `tasks.md` 上为 0；`dated_record_hashes_stable` 对分片 review/code-review/verification/test-evidence 运行前后哈希一致（FR-019、SC-009）。
- V15 `factory_doc_resolutions[]` 每行的 `path:line` 与 `after` 必须可核实（重跑不再复现该引用缺陷），`kind` 三值封闭（`repoint | literal | user-waiver`）（FR-016）。
- V16 `slices[].retention` 必须显式取值（默认 `pending-review`，或经非一次性复核后的处置值）；缺席即缺陷——MUST NOT 沉默保留（FR-018）。

## 5. E4 — Slice / Slice Set（派生）

| 字段 | 规则 |
|------|------|
| `slug` | 目录名形如 `<父编号><一个或多个字母>-<slug>`，且位于同一 `.specify/specs/`（FR-011(a)） |
| `declared_parent` | 分片 `requirements.md` 含 `## Parent Mapping` 节 **或** `**Parent spec**:` 头部字段（二形封闭；FR-011(b)） |
| `order_basis` | `split-record`（默认）：`.specify/state/<parent>.md` § 拆分记录 `proposed_slices` 的有序列表；缺席时 `letter-order`（字母后缀字典序）并记录所用依据（FR-011） |
| `excluded` | 只命中一个条件的目录 → 进入 E7 冲突（`slice-candidate-unconfirmed`），不进集合 |

## 6. E5/E6/E7/E8 — 合并明细、映射、冲突与处置

- **E5 Artifact Merge Record**：`name` 取自 15 项封闭候选（FR-012）；`action` 四值；`sources` 为分片 slug 列表；`checks` 记录该件自身的后置校验（如 `id_continuity`）。
- **E6 ID Mapping Record**：`kind` 三值——`mapped`（用父 ID）、`appended`（分片独有，按合并顺序追加）、`localization`（映射已声明、两侧文本不同，属合法本地化，非冲突；见 plan § Disclosed Rulings 1）。
- **E7 Conflict**：开放即阻断；解决必须具名（`canonical-map` 声明映射 / `recheck-clean` 输入修复后重跑 / `user-waiver` 用户裁定）；无「较新/较全/较大/较后胜出」（FR-017、C-018）。
- **E8 Disposition Record**：57 行拆前记录按 `supersede` 处置；`superseded` 指向父 `tasks.md` 的原行；`superseded_by` 指向**合并清单本身**（`{path: merge-manifest.json, line: 0}`，line 0 = 整文件事实），其 `slices[].carrier_tasks` 列出真正接手的分片 `tasks.md`——不发明逐行映射（C-016）；`evidence[]` 列分片任务文件路径，`guard_status` 取值 `retired|replaced|unchanged-with-reason`。原行以 `> ` 引用前缀保留在「Superseded pre-split record」块内（`TASK_ROW_RE` 为 `^\s*- \[(.)\]`，`> ` 前缀使其不再被计为任务行，见 R-09）。

## 7. E9 — Closure Receipt

只读复制自 `scripts/python/closure-acceptance-check.py --spec-dir <parent> --json`：
`exit_code` + `final_path` 七键**逐字**。`exit 2` 一律按输入缺陷阻断（E12 具名 `closure-input-defect`，附带引擎 stderr 首行），绝不写入回执、绝不读作 accept（FR-007）。

## 8. E10 — Claimed Status Pair

| 载体 | 读取面 | 规则 |
|------|--------|------|
| 注册表行 | `.specify/features.md` Status 列 | 与详情状态**同时存在且相等** |
| 特性详情 | `.specify/features/<ID>.md` `**Status**` 行 | 同上 |
| 注册表 `Last Updated` | 同行时间列 | 与状态同批更新 |
| 详情 `## Latest Review` | 记录节 | 与状态同批**追加**一条封装记录（只追加，不改历史条目） |
| 矛盾/缺失 | 任一不等或缺失 → `state-drift`，exit 2，不择一采信（FR-005、SC-002） |

## 9. E11 — Archive Gate Verdict

```
{"target": "<spec dir>", "status": "<claimed>", "allowed": true|false,
 "reason": "<code>", "pointer": "seal.md|/speckit.seal", "exit": 0|1|2}
```

- `Sealed` → `allowed: true`，`exit 0`。
- 非 `Sealed`（含遗留 `Completed` 且无用户裁定）→ `allowed: false`，`reason` 具名，`pointer` 指向 `/speckit.seal`，`exit 1`。
- 输入/环境错误 → `exit 2`。
- 判据只有一处实现；消费 lane 复制判定时守卫测试转红（FR-023、SC-007）。

## 10. E12 — Refusal Report（stdout-only）

字段：`verdict`、`exit_code`、`conditions[]`（每条 `{code, evidence, fix_path, rerun}`）。MUST NOT 含时间戳——阻断态两次运行的清单须逐字节一致（C-038）。

**封闭拒绝码**（覆盖 SC-002 的八类失败，另含 FR-006 的缺 review、FR-005 的 slice-not-sealable，以及成功语义 already-sealed；`state-drift` 不在本表，见下）：

| 码 | 触发 | 来源 |
|----|------|------|
| `from-status-invalid` | from 状态非 `Ready for Review`（且非已封装） | FR-005 |
| `slice-not-sealable` | 目标目录本身是分片 | FR-005 |
| `review-missing` | 当前 review 记录缺失 | FR-006 |
| `p0-unresolved` | 当前 review 有未处置 P0（驱动者豁免不算） | FR-006 |
| `code-review-blocking` | `code-review.md` 含 `blocking` 条目 | FR-006 |
| `closure-refused` | 闭包裁决 `block` | FR-007 |
| `closure-input-defect` | 闭包引擎 exit 2 | FR-007 |
| `merge-incomplete` | 分片非空但 manifest 缺失/覆盖不全/`not-applicable` 依据缺失 | FR-008 |
| `conflict-open` | manifest 有开放冲突 | FR-008、FR-017 |
| `dirty-spec-tree` | 父 spec 树有本流程之外的未提交改动 | FR-010 |
| `already-sealed` | 已封装（**成功语义**，exit 0，非拒绝） | FR-005 |

`state-drift` 不在此表：它按 FR-005 以 **exit 2** 结束，不是退出 1 的拒绝。

## 11. E13 — Round Adjudication Item（074）

| 字段 | 规则 |
|------|------|
| `item` | FR-027(a)…(e) 五项之一（缺 `Path` 标记 / STR 同号不同义 / 出厂文档引用 / P0 驱动者豁免 / 57 行拆前记录） |
| `state` | `resolved`（证据指针）或 `blocked`（理由） |
| `carrier` | E3 `conflicts[]` / E3 `dispositions[]` / E2 `waivers[]` / 被阻断时 stdout 拒绝清单的捕获文件（`test-evidence/074-round-*.txt`）之一（不新建第三份台账） |

## 12. E14 — Slice Merge Marker

分片 `requirements.md` 头部（`**Status**` 行之后，若缺失则首节之前）追加**恰好一行**：

```
**Merged into**: .specify/specs/<parent-slug>（merge-manifest.json）
```

只新增这一行；分片正文不改写、不删除（FR-018）。

## 13. 关系图

```text
E10 (registry row) ─┐
E10 (detail)      ──┴─→ state-drift 判定 ──→ E2.seal.md ──→ E11 gate 查询
E1 (Sealed) ──转移──→ E10 / E2            │
E4 slices ─→ E5 artifacts ─→ merge-apply ─→ 父 spec 产物 ─→ E3 manifest
              E6 id_maps ─→ 引用改写        │              │
              E7 conflicts ────────────────┘              │
              E8 dispositions ────────────────────────────┘
E9 closure receipt ─→ E2.closure（逐字）      E13 round items ─→ E3/E2 投影
```
