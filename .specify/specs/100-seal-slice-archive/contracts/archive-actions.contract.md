# Contract — Archive Actions（分片归档的引擎动作、流程位置与写面）

**Feature**: 100-seal-slice-archive（bound Feature 099） | **Date**: 2026-11-11 | **Plan**: [plan.md](../plan.md)
**Owns**: `seal-utils.py` 的归档动作契约——动作集增量、触发与前置条件、两阶段执行、幂等与拒绝语义、写面白名单、回滚配方、流程位置与命令面。清单字段归 `archive-manifest.contract.md`；载体分类与解析归 `reference-classification.contract.md`；合并与封装语义仍归 099 的三份契约。

**C-101** — 动作集由四扩为六，只读/写划分同步；动作集 owner 仍是 099 C-001（原地修订）。

引擎 `--action` 取值封闭为 `merge-plan`、`merge-apply`、`seal`、`archive-gate`、`archive-plan`、`archive-apply`。`archive-plan` 是只读动作（零写盘）；`archive-apply` 是写动作。未声明的动作以退出码 `2` 拒绝并回显动作名。除这六个之外 MUST NOT 存在第七个动作。099 `seal-engine.contract.md` C-001 MUST 在同一次变更内原地修订为六值，MUST NOT 新建第二个引擎或第二条命令入口。

(FR-008, FR-021)

**C-102** — 触发谓词取合并清单状态，前置条件是合取，逐条点名全部未满足项。

归档的触发谓词 MUST 从 `merge-manifest.json` 与工作树读取，MUST NOT 依赖「命令刚刚写过盘」：① 合并清单存在且可解析，`merge.status` 为 `"merged"`；② `conflicts` 中开放冲突数为 0；③ 每个分片按 099 既有闭合判据已闭合；④ 父 spec 与分片范围内无本流程之外的未提交改动（`git status --porcelain -- <parent> <slices>`）；⑤ 每个分片在源与目标中恰好存在一侧。任一不成立 MUST 拒绝（`1`）或按输入缺陷退出（`2`），并逐条点名**全部**未满足条件；MUST NOT 只报第一条，MUST NOT 有部分归档。`merge-apply` 以 `0` 退出（新合并或幂等重跑）即满足①；`merge-apply` 被拒绝或报错时归档 MUST NOT 启动，并点名上游阻断。

(FR-001, FR-006)

**C-103** — 结果词汇与退出码封闭；拒绝零持久化。

成功语义（exit `0`）：`would-archive`（仅 `archive-plan`，表示可执行且无阻断）、`archived`（apply 成功）、`already-archived`（幂等）、`not-applicable`（分片集为空）。拒绝语义（exit `1`）：`destination-exists`、`dirty-spec-tree`、`conflict-open`、`slice-unclosed`、`unresolved-references`、`unclassified-reference`。输入或环境错误（exit `2`）：`merge-manifest-missing`、`merge-manifest-invalid`、`slice-missing`、`partial-archive`、`archive-drift`、`archive-manifest-invalid`、`not-a-git-tree`、`mirror-copy`、`write-failed`。三个退出码之外 MUST NOT 出现，词汇之外 MUST NOT 新增 reason。拒绝 MUST 零持久化：无拒绝记录、无空清单、无第二份台账；报告只经 stdout，每条带修复路径与重跑命令。

(FR-007, FR-009)

**C-104** — `not-applicable` 是具名成功，不是静默跳过。

分片集为空时（合并清单 `merge.status == "not-applicable"`），两个动作 MUST 以 `0` 退出并具名报告 `not-applicable`，判定依据 MUST 来自合并清单的 `basis` 或分片发现结果，MUST NOT 只写「无分片」；MUST NOT 创建空清单、MUST NOT 静默跳过。

(FR-007)

**C-105** — 已归档是幂等成功，不是拒绝。

当归档清单存在、每个分片位于 `to` 且 `from` 不存在时，`archive-apply` MUST 以 `0` 退出并具名报告 `already-archived`：不产生第二份清单、不重复移动、不重复改写引用、零 diff。`archive-plan` 重跑 MUST 报告零待移动、零未解析。并发场景下后到者读到先到者清单即走此路径；引擎 MUST NOT 依赖锁文件。

(FR-010, FR-027)

**C-106** — 纯移动：每个文件一条重命名对，零纯删除。

每个分片目录 MUST 以 `git mv` 语义整体移动。`git diff --name-status -M` MUST 对每个被移动文件给出重命名对，MUST NEVER 给出纯删除。MUST NOT 复制后删除、MUST NOT 改写分片内任何文件的字节、MUST NOT 在分片内添加标记行。非 git 工作树 MUST 退出 `2`（`not-a-git-tree`），MUST NOT 退化为普通 `mv`。

(FR-003, FR-028)

**C-107** — 流程位置：合并批次提交之后、seal 判定之前；封装阻断不阻断归档。

一次 `/speckit.seal` 运行的固定位置为：`merge-plan → merge-apply → 按既有「Commit before sealing」提交 merge 批次 → archive-plan → archive-apply → 按显式路径提交 archive 批次 → seal 判定`。归档 MUST 在最终封装判定为 `Sealed` 或任一具名阻断时都可用，MUST NOT 以 `Sealed` 为前置，也 MUST NOT 查询 seal 终态。归档的干净树前置要求 merge 产物先收口；archive 产物再收口后，seal 的 `dirty-spec-tree`（099 C-039）在已落定的树上判定。确认门：`archive-apply` 是一次可逆移动 + 清单映射，按 confirmation-gates owner 属自动执行层；交互运行先展示 `archive-plan` 预览再 apply，无人值守授权运行直接 apply 并记录决策。

(FR-001, FR-022)

**C-108** — `archive-apply` 两阶段执行，写入按批次原子，失败按原字节恢复。

`archive-apply` MUST 先在只读阶段重算与 `archive-plan` 相同的完整计划；只有阻断数为 0 才进入写入。写入 MUST 按批次执行（移动、活引用改写、清单落盘、合并清单路径字段与摘要），任一步失败 MUST 按原字节恢复本批已移动目录与已改写文件，以 `2`（`write-failed`）结束，MUST NOT 留下可被读作半归档的状态。同输入重跑 MUST 复现同一计划（顺序稳定）。

(FR-009)

**C-109** — 确定性是归档的硬约束。

同一输入 MUST 产生逐字节一致的归档清单与引用台账；两次 `archive-plan` MUST 一致；成功 apply 后重跑 MUST 零 diff。任何决策 MUST NOT 依赖返回时刻、目录枚举顺序、随机源或「最后写入者胜出」。无法确定性归类的命中 MUST 成为 `unclassified-reference` 阻断，MUST NOT 由启发式择一。

(FR-005, FR-012)

**C-110** — 回滚是文档化的 git 级配方；引擎零新增回滚动作。

动作集 MUST NOT 增加回滚/undo 动作或第二引擎。版本化面按文档步骤逐字执行：① 按清单 `slices[]` 顺序逐片 `git mv <spec_path>/slices/<slug> .specify/specs/<slug>` 逆移动；② 对每条 `live-rewrite` 的载体与父 `merge-manifest.json` 执行 `git restore --source=<pinned_commit> -- <path>`；③ 移除 apply 新建的 `archive-manifest.json`；④ 运行期面按清单逐条把 `after` 逆写回 `before`。完成判据：父 spec、分片与全部 live 载体的 sha256 等于清单记录的 `before` 值。若归档批次已提交，等效形态是一条 `git revert <archive-commit>`；两种形态都不得触碰批次之外的改动。

(FR-011)

**C-111** — 并发写路径互异，无锁文件。

归档清单 MUST 每个父 spec 一份单文件，MUST NOT 引入共享可变聚合。两条并行线归档不同 spec 时 MUST 写入不同父 spec 目录下的不同清单路径；同一 spec 的并发 apply MUST 由「后到者读清单 → 后到者复核树后走 `already-archived` 或 `archive-drift`」收敛，MUST NOT 依赖锁文件、租约或共享协调文件。

(FR-027)

**C-112** — 归档后的分片发现先读清单，语义不变。

`merge-plan`、`merge-apply`、`seal` 的分片发现与载体解析 MUST 先读 `archive-manifest.json`，把归档分片视为**同一分片集**：MUST NOT 把归档读成「无分片」，MUST NOT 把 `slices/` 目录读成新的分片候选，MUST NOT 改变分片顺序依据。归档后重跑 `merge-apply` MUST 幂等成功且零写入；seal 的 P0 / `blocking` / 闭合判定 MUST 继续读取归档后的分片原始记录。该条只扩展解析路径，MUST NOT 改变合并回写与封装判定语义。清单缺失或不可解析时回退既有同级目录扫描。

(FR-019)

**C-113** — 既有 owner 原地修订，不建第二套。

本特性 MUST 在同一变更内原地修订：099 `seal-engine.contract.md` C-001（四 → 六动作）与 C-008（唯一新增移动 = `archive-apply`，目标限父 spec 的 `slices/`）；`merge-back.contract.md` C-019（分片的后续处置已由本特性以 `archive` 决定，记录 = 归档清单）与 C-023（保持：`merge-apply` 仍是纯合并）；`records-and-boundaries.contract.md` C-035（按退休语义澄清分片归档归 seal）与 C-036（保持：不构成第二归档机制）。`non-disposable-definitions.md` § Disposition Set 的 `archive` 目的地 MUST 原地扩为封闭二形（`.specify/archive/` 退休 | 所属父 spec 的 `slices/` 分片归档），四值集合与 § Disposition Bridge MUST NOT 变化；`framework-map.md` 的 Feature specs 行 MUST 登记 `slices/` 语义。MUST NOT 新增第五个处置值、第二份词表或第二套契约家族。

(FR-002, FR-020, FR-023)

**C-114** — 命令面仍是三件套；不新建 `/speckit.*` 命令。

归档流程 MUST 固化在既有三件产物内：`templates/commands/seal.md`（及经 `regen-command-copies.py` 产生的逐工具副本）、`skills/internal/seal-artifact/SKILL.md`、`scripts/python/seal-utils.py`。`COMMAND_BASELINE` MUST 保持不变（31 个命令），命令名集合 MUST 与改动前逐一相同。技能 MUST NOT 在引擎判定之外自行给出归档或 `Sealed` 结论；模板 MUST 说明归档发生在 merge-apply 成功之后、先预览后 apply、封装修阻断不阻断归档与拒绝语义。命令参考文档与 quickstart MUST 各给出可执行的归档走查与恢复走查。

(FR-021, FR-022)

**C-115** — 脚本接口契约沿用既有守卫。

两个新动作 MUST 满足既有脚本接口契约：`-h`/`--help` 零副作用、`--version` 打印一行身份并以 `0` 退出、任何未声明选项以 `2` 拒绝且不达任何动作。调用面 MUST NOT 新增选项（沿用 `--action`、`--spec-dir`、`--repo`、`--feature-detail`、`--feature-registry`、`--json`），MUST NOT 增加 `--force`、`--no-verify`、`--waive` 一类旁路。

(FR-008)

**C-116** — 每条可判定断言有契约级或单元级测试（Tests Mode ON）。

测试执行 MUST 走唯一入口 `scripts/bash/run-tests.sh`；只有措辞变化的检查 MUST NOT 计为取证。SC → 首红模块映射：

| SC | 首红模块 | 取证形态 |
|----|----------|----------|
| SC-001 | `tests/integration/test_seal_archive_round.py` | 074 回合前后文件数/逐文件 sha256/相对路径集合 + `git diff --name-status -M` + 清单复核 |
| SC-002 | 同模块（幂等）+ `tests/contract/test_seal_archive_apply.py` | 重跑 apply `already-archived` 零 diff；plan 零待移动；内容变异哈希转红 |
| SC-003 | `tests/contract/test_seal_archive_plan.py` | 活/日期化/未分类三类夹具；注入悬空引用与移除映射两类变异转红 |
| SC-004 | `tests/integration/test_seal_archive_round.py`（阻断态）+ `tests/contract/test_seal_engine_contract.py` | 阻断态夹具照常归档；merge-apply 拒绝夹具不启动；`COMMAND_BASELINE` 对照 |
| SC-005 | `tests/contract/test_seal_boundaries.py`（扩展） | 写面静态审计；注入删除/状态写入转红 |
| SC-006 | `tests/integration/test_seal_archive_idempotency.py` | 两次 plan sha256 对照；重跑零 diff；排序变异转红 |
| SC-007 | `tests/contract/test_seal_archive_manifest.py` | 三组闭环算术复算；删行变异转红 |
| SC-008 | `tests/contract/test_seal_archive_apply.py`（runtime 夹具） | 存在/缺席两类；缺席转阻断变异转红 |
| SC-009 | `tests/contract/test_seal_boundaries.py` + 并发夹具 | 单一机制静态审计；双写路径互异；聚合变异转红 |
| SC-010 | `tests/integration/test_seal_archive_round.py`（rollback） | 回滚前后树哈希对照；跳过步骤转红 |

(FR-024, FR-025, FR-026, SC-001…SC-010)
