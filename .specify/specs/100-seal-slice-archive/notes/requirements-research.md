# Requirements-stage research — 100-seal-slice-archive

> 本文件是 requirements 阶段的**证据记录**，不是 plan 阶段拥有的 `research.md`。
> 目标：在写 FR 之前，把「既有归档 owner」与「074a/074b 的真实引用面」量到可引用。
> 测量提交：`48e273d7395d949656099c596161ac9210687cfa`（worktree `100-seal-slice-archive`）。
> 原始读数：`../test-evidence/requirements-measurements.txt`。

## 1. 既有归档 owner（按指针抵达，不另造第二套）

| 所有权 | owner | 与本特性的关系 |
|---|---|---|
| 处置词汇（`archive` / `supersede` / `correct` / `exempt`）与落盘通道 | `.specify/shared/definitions/non-disposable-definitions.md` § Disposition Set / § Disposal Pathways | 分片归档 MUST 复用 `archive`（一次移动、映射入记录、可逆、永不删除）；本特性只扩展该 owner 的**归档目的地**表述（`.specify/archive/` 或所属父 spec 的 `slices/`），不新增第五个处置值、不建第二份词表。 |
| 独立 spec 的退休归档与准入 | `skills/internal/sanitize-materials/SKILL.md` 归档 lane + `scripts/python/seal-utils.py --action archive-gate` | 保持不变。分片归档**不是退休**：目标在父 spec 树内，不是 `.specify/archive/`；因此不查询 `archive-gate`，也不得被任何退休入口复用。 |
| 分片合并回写的写面与后续处置义务 | `.specify/specs/099-speckit-seal/contracts/merge-back.contract.md` C-019 / C-023（需求 099 FR 018 / FR 020） | 099 明写「分片承载物的后续保留/退役 MUST 按 non-disposable 纪律复核后决定，MUST NOT 默认沉默保留」。本特性就是这次复核：选择 `archive`（移动），并把执行面放进 `/speckit.seal`。 |
| seal 的引擎动作集与写面 | 同目录 `seal-engine.contract.md` C-001 / C-008 | C-001 当前封闭为四个动作且「不存在第五个」；C-008 当前禁止动作表含移动/归档。本特性 MUST 在同一 owner 上**原地修订**为「四 + 两个归档动作」，并把移动限定为 `archive-apply` 的分片归档；不建第二个引擎。 |
| 四向边界与零重复机制 | 同目录 `records-and-boundaries.contract.md` C-035 / C-036 | C-035 说 sanitize 拥有归档动作；C-036 禁止第二个归档机制。本特性把「分片归档」定为 seal 既有机制内的第五/第六个动作，并明确它不是退休通道；两处需原地补充例外。 |
| 目录语义 | `.specify/shared/definitions/framework-map.md` 第 38 行（Feature specs） | `slices/` 是 split 特性的从属分片归档层；本特性 MUST 在该行登记其语义，避免出现无文档目录（目录治理）。 |

**结论**：分片归档不是一个新机制，而是 099 已明确延后的「分片后续处置」的执行面；它复用 non-disposable 的 `archive` 处置、扩展 seal 引擎的既有动作集，并把「目的地」这一个事实留在 non-disposable owner 内。

## 2. 074 现状（验收对象）

| 事实 | 读数 | 来源 |
|---|---|---|
| 父 spec 状态 | `Ready for Review`；无 `seal.md` | `.specify/features.md` 074 行；`ls .specify/specs/074-goal-team-sdd-unification/seal.md`（不存在） |
| merge-apply | 已完成：`merge-manifest.json` 的 `merge.status=merged`，`conflicts=[]`，78 个 artifact 行；父 `tasks.md` 未勾选行 0 | `merge-manifest.json`；099 契约 C-043 |
| 父级指针视图 | `verification.md`（聚合指针）、`review.md` / `code-review.md`（分片记录汇总指针）已由 merge-apply 生成 | 三个文件头部 |
| seal 回合终态 | 阻断（任务简报：FR 027(d) + B2 具名）；本阶段只复核到「无 seal.md + 状态未推进」，阻断清单原文不在本阶段重算 | 任务简报 + 上两项实测 |
| 分片位置 | `.specify/specs/074a-authorized-routing`、`.specify/specs/074b-nested-governance`（仍为同级兄弟目录） | 目录实测 |
| 分片规模 | 074a：58 文件 / 942,609 B / aggregate sha256 `0dbcefd2…`；074b：54 文件 / 826,558 B / `91e4520c…`；合计 112 文件 | `requirements-measurements.txt` |

**结论**：验收用例必须在「seal 阻断」状态下可执行，因此归档步骤的触发条件只能是「merge-apply 成功」，不能是 `Sealed`。

## 3. 引用面（实测分类）

### 3.1 活引用（当前指针，必须改写为归档路径）

| 载体 | 命中数 | 说明 |
|---|---:|---|
| `.specify/register.md` | 5 | REC-074a-01…05，全部指向 `074a-authorized-routing/review.md` |
| `.specify/features/074-goal-team-sdd-unification.md` § `## Related Specifications/Requirements` | 10 行（约 12 个路径） | 活指针区；同文件其余命中在日期化时间线 |
| `.specify/specs/074-goal-team-sdd-unification/plan.md` | 29 | 活设计文档 |
| 同目录 `research.md` | 12 | 活设计文档 |
| 同目录 `quickstart.md` | 3 | 活文档 |
| 同目录 `tasks.md` | 143 | 合并后的任务行 + `> superseded` 拆分账（57 行 × 2 + 合并行）；均为当前指针账 |
| 同目录 `verification.md` | 24 | merge-apply 生成的聚合指针视图 |
| 同目录 `review.md` / `code-review.md` | 4 / 4 | 汇总指针视图 |
| 同目录 `feature-ref.md` | 1 | 交付面指针 |
| 同目录 `contracts/*.md` | 15（5 文件） | 活契约 |
| 同目录 `merge-manifest.json` | 123 个 path-form 值 | `dispositions[].evidence[]` 114 + `artifacts[].pointer.paths[]` 6 + `slices[].carrier_tasks` 2 + 1；另有 449 个裸 slug 名（不改） |
| `shared/definitions/sdd-routing-definitions.md` + `.specify/` 镜像 | 1 + 1 | 指向 `074a-authorized-routing/data-model.md` E4 的活指针；源与镜像同改 |
| `tests/integration/test_seal_074_round.py` | 2 | `SLICE_A` / `SLICE_B` 常量 |
| `tests/contract/test_sdd_compat_containment.py` | 1 | `SLICE_DIR` 常量 |
| `tests/contract/test_sdd_diffusion.py` | 1 | `SLICE_DIR` 常量 |

### 3.2 日期化记录（不得改写，经 manifest 映射解析）

| 载体 | 命中数 | 处置 |
|---|---:|---|
| 两个分片目录内部 | 074a 327 处 / 38 文件；074b 299 处 / 42 文件 | 纯移动，字节不变；旧路径经 `archive-manifest.json` 的 `from → to` 前缀映射解析 |
| `.specify/features.md` 074 行 Last Updated 历史叙述 | 13 | 日期化叙述，保持原字节；经映射解析 |
| `.specify/features/074-…md` 的 `## Latest Review` / `## Key Changes` / `## Implementation Notes` 时间线 | 约 10 | 同上 |
| `.specify/memory/**`（session / feedback / exec-quant / coaching / evidence / renumber） | 多处 | 日期化/机器记录，保持原字节；经映射解析 |
| `merge-manifest.json` 中 449 个裸 slug 名 | 449 | 目录名保持不变，因此无需改动 |

### 3.3 运行期 line registry（环境级，git-ignored）

- 主仓 `.specify/state/074-goal-team-sdd-unification.md`：21 处；`.specify/state/074b-nested-governance.md`：14 处。
- 本 worktree 无 `.specify/state/`（`git check-ignore` 命中 `.specify/.gitignore:34`）。
- 结论：它们是**运行期活指针**，存在时必须更新并留痕；缺席时 manifest 记 `absent`，不得因此失败（否则同一命令在 worktree 与主仓会得到不同结论）。

### 3.4 未解析定义的边界

「归档后未解析引用 = 0」若按字面要求所有历史文本都改路径，会与非 disposable 的「历史记录不得改写」和 099 C-020 的 dated-record 红线冲突。因此本阶段采用的判据是：

> 一个引用被判定为**已解析**，当且仅当 (a) 目标路径在树上存在，或 (b) 它是日期化记录中的旧分片路径，且该前缀命中 `archive-manifest.json` 的 `from → to` 映射并落到存在的归档路径。

活引用必须直接解析（(a)）；日期化引用只允许经映射解析（(b)）；两者之外即未解析，apply 拒绝（fail closed）。这条判据写入 FR，映射表成为唯一解析通道。

## 4. 现有引擎与消费面的缺口

1. `seal-utils.py::_discover_slices` 只扫描父目录的**同级兄弟目录**（`specs_root.iterdir()`）；分片移入 `parent/slices/` 后不再被发现，`merge-plan` / `merge-apply` / `seal` 会把它读成「无分片」——必须改为**先读归档 manifest**，再把归档分片视为同一分片集。
2. `merge-apply` 的幂等判定依赖 `_merge_state` 与分片 `**Merged into**` 标注；归档后重跑必须仍得到 `idempotent: true` 且零写入，不得把归档当作输入缺失。
3. 三个测试文件硬编码分片路径（见 3.1）；它们是活守卫，必须随归档更新或改为 manifest-aware。
4. 当前动作集封闭为四个（C-001），写面静态审计禁止移动（C-008）；新增归档动作必须在同一契约上原地修订，静态审计改为「移动只允许 `archive-apply` 且只在父 spec 树内」。
5. `archive-gate` 只回答「独立 spec 是否可退休」，分片没有状态载体；分片归档 MUST NOT 走该 gate，也不得被退休 lane 复用。

## 5. 本阶段采用的裁定（供 clarify 复核）

| # | 裁定 | 依据 |
|---|---|---|
| R-1 | 目的地 = `<parent-spec>/slices/<原分片目录名>/`，保留目录名与相对树 | 用户原话「在 074 中建子目录归档 074a 和 074b」 |
| R-2 | 归档清单 = 父 spec 根下的 `archive-manifest.json`，一 spec 一文件 | 与 `merge-manifest.json` 同构；并发安全 |
| R-3 | 引擎动作 = `archive-plan`（只读）+ `archive-apply`（写），沿用 `merge-plan` / `merge-apply` 先例；退出码 0/1/2 封闭 | 用户「dry-run 预览 + apply 两阶段」 |
| R-4 | 归档是纯移动：不改分片内任何字节、不加标记；记录由 manifest 与父级指针承载 | 零丢失 + dated-record 红线 |
| R-5 | 活引用改写、日期化引用经 manifest 映射解析；未解析 = 0 为 apply 的合取前置 | 用户「零丢失 / fail closed」+ non-disposable |
| R-6 | 运行期 state 记录存在则更新并留痕，缺席记 `absent`，不阻断 | 环境级、git-ignored、worktree 不可见 |
| R-7 | 099 契约与非 disposable owner 原地修订；不新建命令、不建第二引擎/词表/台账 | 用户边界 + 099 C-036 |
| R-8 | 父 `tasks.md` 的 `> superseded` 行按活指针账处理（改路径、不改历史事实） | 它是当前合并账，不是日期化测量 |

## 6. 留给 clarify 的问题（不超过三条，均可默认）

1. `archive-manifest.json` 放父 spec 根还是 `slices/` 内？（默认：父 spec 根，与 merge-manifest 并列。）
2. 父 `tasks.md` 的 57 行 `> superseded` 拆分账算活指针还是日期化记录？（默认：活指针，改路径不改事实。）
3. 归档是否需要在交互模式下单独确认？（默认：按既有 confirmation-gates owner；无人值守授权运行直接 apply。）
