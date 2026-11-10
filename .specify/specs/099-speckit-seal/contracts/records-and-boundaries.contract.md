# Contract — Records, Preconditions & Boundaries

**Feature**: 099-speckit-seal | **Date**: 2026-11-10 | **Plan**: [plan.md](../plan.md)
**Owns**: 两份记录文件的 schema 与替换语义、seal 前置条件与拒绝码封闭集、P0 豁免的机器可判形式、
四向边界指针、零重复机制的可核验判据、074 回合记录与测试映射。

**C-032** — `seal.md` 的固定名与封闭字段集。

封装回执 MUST 落父 spec 目录固定文件名 `seal.md`（STR-002），机器可读核心字段集以
`data-model.md` § 3 的字段表为准（15 个字段行，含 `merge.status`、`merge.basis` 与 `closure.command`；
重封装时加 `supersedes`）。未知字段 MUST NOT 写入；
记录 MUST 引用来源而不复述第二份测量。每 spec 的 `seal.md` MUST 只承载**当前**回执。

(FR-010)

**C-033** — 回执替换与 `supersedes`。

审计更正（`Sealed → Ready for Review`）后再次封装时，`seal` MUST 原子替换 `seal.md`，并在机器可读核心写入
`supersedes: <前回执 pinned_commit>`；前回执由 git 历史承载，MUST NOT 另建第二份回执文件或历史聚合。

(FR-002, FR-010)

**C-034** — `merge-manifest.json` 的固定名、稳定键序与自摘要。

合并清单 MUST 落父 spec 目录固定文件名 `merge-manifest.json`，机器可读、键序稳定
（`indent=2, sort_keys=True, ensure_ascii=False`）。`digest` MUST 为剔除 `digest` 自身与时间键后的排序紧凑
JSON 的 sha256。`seal.md` MUST 只引用该文件，不复述其内容。

(FR-018)

**C-035** — 四向边界只按指针抵达。

`/speckit.feature`（`manage-features`）继续拥有注册表 reconcile 与声明语义；`/speckit.review` 继续拥有
review 记录与裁决（seal 只读）；`/speckit.sanitize` 的归档 lane 与 `/speckit.docs` 的 docs lane 继续拥有
归档/退休动作（seal 只提供 C-030 的准入查询）；`/speckit.goal` 的 `migrate-archive` 继续拥有 spec-local
goal/team 树迁移（seal 不迁移、不删除）。seal MUST NOT 实现上述任一动作的第二份。

(FR-022)

**C-036** — 零新增重复机制可静态核验。

仓库 MUST NOT 因本特性新增：第二套状态机或值域、第二份特性注册表或台账、第二个归档机制、调度器/守护进程、
并行 spec 树。封装记录与合并清单 MUST 按 spec 落单文件，MUST NOT 引入共享可变聚合。核验以三重证据：
状态 owner 的单一性（C-025 的静态检索）、引擎动作表（C-008）、目录/注册表清单的差异审计。

(FR-024, SC-008)

**C-037** — 并发写路径互异，无锁文件。

两条并行线封装不同 spec 时 MUST 写入各自 spec 目录下的不同文件；同 spec 的并发 `seal` MUST 由「后到者读回执
→ `already-sealed`」收敛。引擎 MUST NOT 依赖锁文件、租约或任何共享可变协调文件。

(FR-020, SC-009)

**C-038** — 三面一致与阻断态可复现。

合并清单、封装记录或拒绝清单、状态面三者 MUST 一致；阻断状态下重跑 MUST 得到同一阻断清单（顺序、码与
证据指针稳定），MUST NOT 因重跑顺序改变结论；MUST NOT 出现部分封装。回执不可写而状态可写、或反之，
MUST 以 exit 2 与原子恢复收场（C-005）。

(FR-009, FR-028)

**C-039** — `dirty-spec-tree`：对移动中的状态不盖章。

父 spec 树存在本流程之外的未提交改动时 `seal` MUST 拒绝（`dirty-spec-tree`）并指名路径；本流程自身产生的
改动 MUST 在提交后再判定。检测 MUST 以 `git status --porcelain -- <parent-spec-dir>` 为单一依据，MUST NOT
纳入 spec 目录以外的路径（其他线的工作不阻断本 spec）。

(FR-010)

**C-040** — review 与测量记录只读。

`seal` 对当前 `review.md`、`code-review.md` 与 manifest 登记的全部分片测量文件 MUST 只读：运行前后哈希一致。
MUST NOT 改写 finding、重新裁决或降级。

(FR-006, FR-019, SC-009)

**C-041** — 命令面三件套与副本生成。

`/speckit.seal` MUST 由三件构成且只有三件：`templates/commands/seal.md`（薄入口：User Input、Delegation、
Glossary、Wrap-up、Handoffs）、`skills/internal/seal-artifact/SKILL.md`（编排与报告，MUST NOT 复算判定）、
`scripts/python/seal-utils.py`（判定引擎）。per-tool 副本 MUST 由 `scripts/python/regen-command-copies.py`
生成，MUST NOT 手抄；技能镜像由 `sync-mirrors.py` 投影。技能 MUST NOT 在引擎输出之外自行给出
`Sealed`/准入结论。

(FR-021)

**C-042** — 前置条件是合取，拒绝码封闭。

`seal` 的判定 MUST 是对下列条件的合取：from 状态、review/P0、code-review blocking、闭包裁决、合并完成度、
开放冲突、dirty-spec-tree、状态一致性。任一不成立即拒绝并点名**全部**未满足条件。拒绝码封闭集：
`from-status-invalid`、`slice-not-sealable`、`review-missing`、`p0-unresolved`、`code-review-blocking`、
`closure-refused`、`closure-input-defect`、`merge-incomplete`、`conflict-open`、`dirty-spec-tree`；
`already-sealed` 是成功语义（exit 0）；`state-drift` 走 exit 2。**闭包引擎 exit 2 MUST 按输入缺陷处置**
（`closure-input-defect`，附 stderr 首行），MUST NOT 读作 accept，MUST NOT 吞成通过；闭包裁决 MUST 来自
`closure-acceptance-check.py` 的单一来源，MUST NOT 由模型或第二个脚本重算。

(FR-005…FR-009, FR-027)

**C-043** — 074 回合记录与五项处置。

回合记录 MUST 由 `merge-manifest.json`（冲突与处置行）、被阻断时 stdout 拒绝清单的捕获文件
（`test-evidence/074-round-*.txt`）、以及（仅 `Sealed` 终态时）`seal.md` 构成；MUST NOT 新建第三份台账。FR-027 的五项实测
输入（缺 `Path` 标记、STR 同号不同义、出厂文档引用分片本地 ID、P0 驱动者豁免、57 行拆前记录）MUST 各自
以「已解决（证据指针）」或「阻断（理由）」出现在回合记录中，一一对应、无静默默认。回合终态 MUST 是二值：
`Sealed` 或具名阻断清单；阻断态重跑 MUST 清单一致。

(FR-026, FR-027, FR-028)

**C-044** — P0 处置的机器可判形式。

一个 P0 被计为「已处置」仅当下列之一成立：(a) 其 finding 段落含修复指向（可解析的路径或提交引用）；
(b) 用户裁定已按既有 waiver 纪律落在**两处**可核验载体上——当前 `review.md` 的 code 小节与特性详情
`## Latest Review` 各存在一条以字面 `- **User waiver**:` 起头、点名该 finding 的行（会话裁定须由代理把用户
原话记入两处后方可计数；单一载体不计数）。
驱动者/协调者/代理的确认、`显式豁免（P0 waiver）` 一类叙述、以及「无人反对」MUST NOT 计为用户豁免。

(FR-006, FR-027)

**C-045** — SC → 红先测试映射（Tests Mode ON）。

| SC | 首红模块 | 取证形态 |
|----|----------|----------|
| SC-001 | `tests/contract/test_seal_seal.py`（主路径 + 幂等）；`tests/contract/test_sealed_status_domain.py`（漂移变异） | 夹具运行记录 + `seal.md`/注册表/详情报文对照；移除 `Sealed` 守卫转红 |
| SC-002 | `tests/contract/test_seal_seal.py`（八类拒绝夹具 + 三缺一变异） | 引擎输出与退出码逐条比对；状态未变读数 |
| SC-003 | `tests/integration/test_seal_merge_determinism.py` | 两次运行 sha256 对照；`git diff --stat` 零输出；返回时刻排序变异转红 |
| SC-004 | `tests/contract/test_seal_merge_apply.py` | 合并后程序化扫描（ID 序列/悬空引用/映射覆盖/未勾选行）+ 两个既有验证器 exit 0 |
| SC-005 | `tests/contract/test_seal_merge_plan.py` | 同号不同义与出厂引用两类夹具；静默重编号变异转红 |
| SC-006 | `tests/integration/test_seal_074_round.py`（只读 plan 面 + 阻断态重跑）+ 回合实测记录 | `test-evidence/074-round-*.txt`；五项裁决逐条对照；重跑清单一致 |
| SC-007 | `tests/contract/test_seal_archive_gate.py` | 拒绝/通过夹具 + 第二实现注入转红 |
| SC-008 | `tests/contract/test_sealed_status_domain.py`、`tests/contract/test_seal_boundaries.py` | 三处旧 pin 七值化 + 动作表静态审计 |
| SC-009 | `tests/contract/test_seal_concurrency_and_readonly.py` | 双写路径互异；运行前后哈希一致；脏树拒绝 |

测试执行 MUST 走 `scripts/bash/run-tests.sh`（唯一入口）；只有措辞变化的检查 MUST NOT 计为取证。

(FR-025, SC-001…SC-009)
