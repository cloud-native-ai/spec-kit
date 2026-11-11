# Research — 100-seal-slice-archive（plan 阶段）

**Feature**: 100-seal-slice-archive（bound Feature 099 Speckit Seal） | **Date**: 2026-11-11 | **Plan**: [plan.md](plan.md)
**Measured at**: worktree `100-seal-slice-archive`，HEAD `9695d78c5`（基线提交 `48e273d73` 的 074 读数沿用 requirements 阶段记录并复核）
**Authority**: `requirements.md`（28 FR / 10 SC / 5 STR / 5 条 Clarifications）是意图 owner；本页只记录**计划阶段实测的既有 owner 位置与读数**，不复述规则。

本页回答一个问题：把「分片归档」放进既有 `/speckit.seal` 之前，磁盘上哪些既有 owner 必须原地修订、哪些读数构成设计前提。全部条目带 file:line 或实测命令输出。

---

## R-01 — 处置词汇 owner：non-disposable（四值封闭集）

| 事实 | 位置 | 读数 |
|---|---|---|
| 处置集封闭四值 `archive` / `supersede` / `correct` / `exempt`，`archive` 现行目的地为 `.specify/archive/` | `.specify/shared/definitions/non-disposable-definitions.md:275-292`（§ Disposition Set） | 表行 281 写明 `archive = 移入 .specify/archive/ 并留下指针`；本文档声明自己是唯一 owner，引擎/契约 MUST 引用 |
| `archive` 的落盘通道 = 一次移动（`git mv` 语义），记录携带 `moved = {from, to}` | 同文件 `:394-414`（§ Disposal Pathways；C-308 在 `:408-414`） | "MUST 是一次移动…`git status --porcelain` MUST 显示一对重命名，MUST NEVER 显示一次删除" |
| 与 sanitize / history 的四向边界 | 同文件 `:661-682` | 两套词表互不合并；唯一裁决规则在 § Disposition Bridge；本特性只补 `archive` 的目的地形，不新增第五值 |
| 镜像副本 | `.specify/shared/definitions/` 是 `shared/definitions/` 的投影 | `sync-mirrors.py` 对 `shared` 对声明逐字节一致（本日实测 ok，113 文件） |

**结论**：分片归档复用 `archive` 处置；唯一需要原地修订的是「目的地」表述（封闭二形：退休 `.specify/archive/**` | 父 spec 的 `slices/`）与「处置记录 = 父 spec 的 `archive-manifest.json`」。

## R-02 — 独立 spec 退休归档 owner：sanitize 归档 lane + `archive-gate`

| 事实 | 位置 | 读数 |
|---|---|---|
| sanitize 的破坏性确认门把 delete/archive 合并为一次清理计划 | `skills/internal/sanitize-materials/SKILL.md:211-217`（Stage 5） | 计划文件 `.specify/memory/sanitize/cleanup-plan.json`（`confirmed: false`） |
| 退休一个 spec 目录前 MUST 查询唯一准入 owner | 同文件 `:219-234`（§ Archive admission gate） | 命令 `python3 .specify/scripts/python/seal-utils.py --action archive-gate --spec-dir <target> --json`；exit 0 放行 / 1 拒绝 / 2 错误；"not queried never means allowed" |
| 归档执行写入 `.specify/archive/` 保序布局 | 同文件 `:238-244`（Stage 6） | `--action apply` 执行 delete/archive 与状态更新 |
| sanitize 引擎的处置集是五值 `delete/archive/repair/delegate/dismiss` | `scripts/python/sanitize-utils.py:35` | 与 non-disposable 四值是两套封闭集（桥在 owner 页） |
| 归档根常量 | `scripts/python/sanitize-utils.py:51,60,317` | `ARCHIVE_REL = .specify/archive`；`("archive-spec", ".specify/archive/spec")`；`SPECS_ARCHIVE_PREFIX = .specify/specs/.archive/` |
| archive 的 apply 分支 | `scripts/python/sanitize-utils.py:1007-1015` | 写入 `.specify/archive/<rel>` |

**结论**：分片归档**不得**查询 `archive-gate`、不得写 `.specify/archive/`、不得被任何退休入口复用（FR-020）。`archive-gate` 的六个封闭 reason 已覆盖独立 spec 准入，本特性零改动。

## R-03 — `archive-gate` 的引擎实现与封闭 reason 集

| 事实 | 位置 | 读数 |
|---|---|---|
| 动作实现 | `scripts/python/seal-utils.py:2867-2947`（`action_archive_gate`） | 读状态面对（详情 + 注册表），`Sealed` + 可读回执放行；遗留 `Completed` 需 C-044 双载体用户裁定；其余具名拒绝 |
| reason 封闭集 | 同文件 `:77-84` | `sealed` / `legacy-completed-ruled` / `not-sealed` / `legacy-completed-unruled` / `state-drift` / `seal-receipt-invalid` |
| 动作注册表 | 同文件 `:2950-2955`（`HANDLERS`） | 恰四动作；新增动作必须同时改 `ACTIONS` 与该表 |

**结论**：分片归档不复用 `archive-gate`（分片没有状态载体）；本特性只在同一 `HANDLERS` 表追加两个动作，不动 gate 的 reason 集。

## R-04 — 框架布局 owner：`slices/` 的登记位置

| 事实 | 位置 | 读数 |
|---|---|---|
| Feature specs 行 | `.specify/shared/definitions/framework-map.md:38` | 当前仅登记 `.specify/specs/<ID>-<slug>/`（requirements/plan/tasks/verification…）；无 `slices/` 语义 |
| 目录治理纪律 | `.specify/instructions.md` § Temporary Directory Discipline / Directory Governance | 无文档目录 MUST NOT 创建；新目录语义必须登记到布局 owner |

**结论**：FR-002 要求在 `framework-map.md` 的 Feature specs 行登记 `<parent>/slices/<原分片目录名>/` 的语义；源与 `.specify/` 镜像同批修订。

## R-05 — seal 引擎现状：动作集、写面、分片发现、清单与摘要

| 事实 | 位置 | 读数 |
|---|---|---|
| 动作集恰四值 | `scripts/python/seal-utils.py:43`（`ACTIONS`） | `merge-plan`, `merge-apply`, `seal`, `archive-gate` |
| 只读/写动作划分 | 同文件 `:45-46`（`READ_ONLY_ACTIONS` / `WRITE_ACTIONS`） | 只读 2 / 写 2 |
| 写面白名单（数据形态） | 同文件 `:62-68`（`WRITE_PATH_ALLOWLIST`） | `seal.md`、`merge-manifest.json`、父级合并产物、分片 `requirements.md` 一行、已记录的出厂文档修正；**无移动** |
| 分片发现只扫同级兄弟目录 | 同文件 `:454-477`（`_discover_slices`） | `specs_root.iterdir()` + 名称族 + 父声明双条件；分片移入 `parent/slices/` 后不再被发现 |
| 分片顺序派生 | 同文件 `:480-520`（`_derive_order`） | 先读 `.specify/state/<parent>.md` § 拆分记录 `proposed_slices`，缺席回退字母序并写 `order_basis` / `order_source` |
| 合并清单文档与摘要 | 同文件 `:1751-1788`、`:1831-1836` | `schema_version/spec/merge/slices/artifacts/conflicts/id_maps/checks…`；`digest = "sha256:" + sha256(排序紧凑 JSON 剔除 digest)`（C-034） |
| `merge.status` 二值 | 同文件 `:1764-1770` | `merged` 或 `not-applicable`（分片集为空，带 `basis`） |

**结论**：FR-008/FR-019 要求动作集扩为六、写面白名单追加归档移动与归档清单、`_discover_slices` 改为「先读 `archive-manifest.json` 再回退同级扫描」。全部改动落在同一引擎文件与同一注册表。

## R-06 — 必须在同批原地修订的 099 契约条款

| 契约 | 条款 | 位置 | 现行内容 | 本特性的修订方向 |
|---|---|---|---|---|
| `seal-engine.contract.md` | C-001 | `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md:6-12` | 动作集恰四个，「不存在第五个」 | 原地改为六动作（+ `archive-plan` / `archive-apply`），只读/写划分同步 |
| 同 | C-008 | 同文件 `:63-69` | 动作表 MUST NOT 含移动/删除/归档 | 移动唯一例外 = `archive-apply`，目标限父 spec 的 `slices/`；删除与 push 仍禁止 |
| `merge-back.contract.md` | C-019 | `.specify/specs/099-speckit-seal/contracts/merge-back.contract.md:95-102` | 分片后续保留/退役 MUST 按 non-disposable 复核后决定 | 决定已由本特性作出（`archive`），处置记录 = `archive-manifest.json` |
| 同 | C-023 | 同文件 `:134-141` | `merge-apply` MUST NOT 归档/移动/删除 spec 目录 | 保持；归档动作只归 `archive-apply`，`merge-apply` 语义不变 |
| `records-and-boundaries.contract.md` | C-035 | `.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md:31-38` | 归档/退休动作归 sanitize 归档 lane | 按**退休**语义原地澄清：分片归档是父 spec 内的位置迁移，归 seal |
| 同 | C-036 | 同文件 `:40-46` | 禁止第二个归档机制 | 保持；分片归档是既有机制的动作扩展，不是第二机制 |

**结论**：FR-023 的「原地修订」有精确位置；契约页的条款 id 归属不变（C-001/C-008/C-019/C-023/C-035/C-036）。

## R-07 — 074 当前实测状态（验收对象）

| 事实 | 读数 | 来源 |
|---|---|---|
| 父 spec 注册状态 | `Ready for Review`；无 `seal.md` | `.specify/features.md` 099 行与 074 行；`ls .specify/specs/074-goal-team-sdd-unification/seal.md` 不存在 |
| 合并清单状态 | `merge.status = "merged"`；`conflicts = []`（0）；`slices` 2 行，`retention = "pending-review"` | `.specify/specs/074-goal-team-sdd-unification/merge-manifest.json`（实测解析） |
| 合并清单摘要 | `sha256:a43c954dac989b5768405bf1255a0555aac334869051a382d4a233b81e00ce7b` | 同上 `digest` 字段 |
| 分片规模 | 074a：58 文件 / 942,609 B；074b：54 文件 / 826,558 B | 本日 `os.walk` 实测（运行时探针；requirements 阶段记录同值） |
| 分片位置 | `.specify/specs/074a-authorized-routing/`、`.specify/specs/074b-nested-governance/`（同级兄弟目录） | 目录实测 |
| 父 tasks 拆前行 | 57 行 `> superseded` 拆分账（当前合并账） | requirements Assumptions；父 `tasks.md` 实测 |

**结论**：归档触发条件只能取合并清单状态（`merged` + 零开放冲突），不能取 `Sealed`；074 的 `retention: pending-review` 字段属 099 合并清单的非路径字段，本特性不改写它，处置决定写入 `archive-manifest.json`。

## R-08 — 074 引用面（path-form 实测，按载体）

检测式：`\.specify/specs/<slug>` 或词边界处的 `<slug>/`（slug = 两个分片目录名）。**裸 slug（不作为路径片段）不计为引用**——例如 `merge-manifest` 的 `slices[].slug`、`artifacts[].sources[]`、`id_maps` 键与 `<!-- source: 074a-... -->` 标注（449 处）保持原字节。

| 载体 | path-form 命中 | 分类 |
|---|---:|---|
| `.specify/specs/074-goal-team-sdd-unification/tasks.md` | 138 | live |
| 同 `merge-manifest.json` 的**路径形态值** | 123（全文 slug 提及 572；其余为 identity 值） | live（只改路径字段，摘要重算） |
| 同 `verification.md` | 16 | live（合并生成的聚合指针视图） |
| 同 `contracts/*.md`（5 文件） | 15（4+3+3+3+2） | live |
| 同 `plan.md` / `research.md` | 6 / 6 | live |
| 同 `quickstart.md` | 3 | live |
| 同 `review.md` / `code-review.md` | 2 / 2 | live（聚合指针视图） |
| 同 `feature-ref.md` | 1 | live |
| 同 `data-model.md` / `requirements.md` | 0 / 0 | — |
| 同 `notes/**`（25 文件） | 118 | dated |
| 同 `test-evidence/**`（29 文件） | 214 | dated |
| 同 `checklists/**`（3 文件） | 25 | dated（日期化验证记录） |
| `.specify/register.md` | 5（`REC-074a-01…05` 行，:105-109） | live |
| `.specify/features/074-goal-team-sdd-unification.md` § `## Related Specifications/Requirements`（:70-89） | 10 | live（混合载体的活区） |
| 同文件其余章节（`## Latest Review` :16-41、`## Key Changes` :42-49 等） | 3 | dated |
| `.specify/features.md` 074 行 Last Updated 叙述 | 5 | dated |
| `shared/definitions/sdd-routing-definitions.md` + `.specify/` 镜像 | 1 + 1（`:184`） | live（源/镜像同批） |
| 分片目录内部 | 074a 295 / 074b 262（path-form） | dated（纯移动，字节不变） |

**结论**：引用面远大于 requirements 阶段的粗计数（该阶段按裸 slug 计数）。计划把载体名册与扫描根写成封闭集（contracts/reference-classification），任何命中落在封闭集之外即 `unclassified-reference` 阻断。

## R-09 — 硬编码分片路径的测试载体

| 测试 | 位置 | 形态 | 处置 |
|---|---|---|---|
| `tests/contract/test_sdd_compat_containment.py` | `:60-63` | `SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "074b-nested-governance"`（构造式） | live：slug 字面量改 `<parent>/slices/<slug>` |
| `tests/contract/test_sdd_diffusion.py` | `:67,84,635` | 同上 | live：同上 |
| `tests/integration/test_seal_074_round.py` | `:39-40` | `SLICE_A/SLICE_B` 裸 slug，仅作 identity 断言键（`:45-49,89`） | 非路径引用；不重写，归档后断言仍成立（slug 不变） |

**结论**：引用检测器必须区分「路径构造行上的 slug 字面量」（live，改写）与「identity 常量」（不改写）；判定谓词 = 同一行同时含 `.specify` 与 `specs`，仅对 `tests/**` 生效。

## R-10 — 运行期 line registry 载体

| 载体 | 声明数 | 本 worktree | 主仓实测 |
|---|---:|---|---|
| `.specify/state/<parent-slug>.md` | 1 | 不存在（`.specify/state/` 整体缺席，git-ignored） | 存在，11 处 slice 引用，`spine_state: running` |
| `.specify/state/<slice-slug>.md` | 每分片 1（074a / 074b） | 不存在 | `074b-nested-governance.md` 存在（8 处引用）；`074a-authorized-routing.md` **不存在** |
| 合计声明 | 3 | 3 × `absent` | 2 × 可更新 + 1 × `absent` |

**结论**：`runtime-updated + absent = 被声明的运行期载体数（3）` 在两种环境下都成立；worktree 与主仓的结论差异只体现在行值，不改变退出码（FR-017）。

## R-11 — 镜像与命令副本基线（编辑前实测）

| 检查 | 命令 | 读数 |
|---|---|---|
| 镜像 | `python3 scripts/python/sync-mirrors.py --check` | exit 2；`skills/external` / `skills/internal` / `agents` / `scripts` / `shared` 全部 `ok`；**唯一既有漂移**：`DIFF .specify/templates/gitignore-specify-template`（与本特性写面无关） |
| 命令副本 | `python3 scripts/python/regen-command-copies.py --check` | exit 0 / `OK: all per-tool command copies match the source templates.` |

**结论**：Mirror Obligations 的判据写成「本 spec 触及的镜像对**无新增漂移**」，不以全局 exit 0 为准（基线已有一条无关漂移）。

## R-12 — 钉住当前表面的既有守卫测试（必须同批更新）

| 守卫 | 位置 | 钉住的表面 |
|---|---|---|
| `tests/contract/test_seal_engine_contract.py` | `:36-38`（四动作元组）、`:196-210`（C-001）、`:346-349`（只读/写划分） | 动作集恰四、HANDLERS 与 choices 一致 |
| `tests/contract/test_seal_boundaries.py` | `:211-230`（动作表封闭且无破坏性动作）、`:362-410`（写面白名单） | 写面无移动、无删除；审计报告完整性 |
| `tests/contract/test_seal_merge_apply.py` | `:445-464`（清单 schema + 自摘要 C-034） | 合并清单键集与 digest 算法 |
| `tests/contract/test_migration_distribution.py` | `:104,134,275-278` | `COMMAND_BASELINE` 恰 31 个命令 |
| `tests/integration/test_seal_merge_determinism.py` | 既有 | 合并不确定性与重跑零 diff 的确定性判据形态可复用 |

**结论**：这些守卫是本特性「不回归」的现成红先载体；新增归档测试与它们同批修订，而不是另建第二套判据。

## R-13 — 计划阶段采用的裁定（与 clarify 裁决一致）

| # | 裁定 | 依据 |
|---|---|---|
| RP-1 | 目的地 = `<parent>/slices/<原分片目录名>/`，`slices/` 语义登记进 `framework-map.md:38` 行 | FR-002；R-04 |
| RP-2 | 清单 = 父 spec 根 `archive-manifest.json`，一 spec 一份；与 `merge-manifest.json` 并列 | FR-005；clarify Q3；R-07 |
| RP-3 | 引擎动作 = `archive-plan`（只读）+ `archive-apply`（写）；`ACTIONS` 四 → 六，退出码仍 0/1/2 | FR-008；R-05、R-06 |
| RP-4 | 引用分类 = 载体封闭集 → 章节/行谓词 → 解析测试；日期化豁免四条件机械可判 | FR-012…FR-016；R-08 |
| RP-5 | 运行期载体声明数 = 1 + 分片数（074 为 3）；缺席记 `absent`，不阻断 | FR-017；R-10 |
| RP-6 | 合并清单只改路径形态值并重算摘要；`retention` 等非路径字段不动，处置记录在归档清单 | FR-018；R-07 |
| RP-7 | 归档后分片发现先读归档清单（manifest-aware），不改合并与封装语义 | FR-019；R-05 |
| RP-8 | 回滚 = 文档化 git 级步骤（逆移动 + `git restore --source=<pinned_commit>` + 移除清单 + 运行期逆写）；引擎零新增回滚动作 | FR-011；clarify Q4 |
| RP-9 | 测试载体按「路径构造行上的 slug 字面量」判定；identity 常量不重写 | FR-013；R-09 |

## R-14 — 留给 tasks / implement 的已知实现锚点

1. `_discover_slices` 的 manifest-aware 改造会同时影响 `merge-plan` / `merge-apply` / `seal` 三个动作；判据是「归档后重跑 `merge-apply` 幂等且零写入、`seal` 的 P0 列表不变」（FR-019）。
2. 归档写面包含镜面对（`shared/**` ↔ `.specify/shared/**`），必须走 `sync-mirrors.py` 语义；测试载体是源树文件。
3. 动作集与白名单是静态审计面（`test_seal_boundaries.py`），新增移动必须由**数据表**（`WRITE_PATH_ALLOWLIST` 的归档目标形态）表达，不得散落在函数体内。
4. 归档清单的 `digest` 复用 C-034 算法；`pinned_commit` 取 `git rev-parse HEAD`（apply 前），回滚文档以它为 `git restore --source`。
5. `COMMAND_BASELINE` 保持 31；命令模板只改 `seal.md` 内容，不新增命令名。

---

**No second research artifact**: 本页替代 requirements 阶段的 `notes/requirements-research.md` 作为 plan 阶段的设计证据；后者保留为日期化记录（dated），不再回改。
