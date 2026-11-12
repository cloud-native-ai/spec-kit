# Round-2 verification — requirements quality checklist（checklist 第 2 轮）

**Purpose**: 复核第 1 轮 11 条 fail（F-1…F-11）与 CHK025 下游漂移是否在各自 owner 中真正闭合，并检查修复本身是否引入新的两读局面。本文件**只**核对既有文本，不改写 requirements / plan / tasks / contracts / 代码。
**Created**: 2026-11-12
**Round**: 2（post-repair verification）
**Feature**: [../feature-ref.md](../feature-ref.md)（101-anchor-goal-realignment）
**Round-1 checklist**: [2026-11-12-requirements-quality.md](2026-11-12-requirements-quality.md)
**Repair record**: [../notes/checklist-repair.md](../notes/checklist-repair.md)
**Machine-readable PLAN-EDIT index**: [../notes/plan-edits-round1.txt](../notes/plan-edits-round1.txt)
**Authorities read in full**: `../requirements.md`、`../contracts/{anchor-command,goal-command,goal-engine,migration-cleanup}.contract.md`、`../research.md`、`../data-model.md`、`../classification.json`、`../plan.md`（Phase 0 / WP-01…WP-05 / G-5 / G-6 / EP-006）、`../tasks.md`（被引用行）、`../feature-ref.md`、`../quickstart.md`，以及被引用的既有引擎源 `scripts/python/goal-utils.py` 与 `skills/internal/run-team/SKILL.md`。

**Method**: 逐条读**修复后的正文与 owner 行**，不复用修复记录的自述。凡修复记录声称"已在 X 处改正"的，都打开 X 核对；凡引用实测数字的，用只读命令复算（`grep` / `git show` / 行号读取）。round-1 的检测降级情形（本层禁止派发子代理）在 round-2 依旧成立：本轮同样是一次有界直读，判定证据强度弱于独立复核，已在此显式披露。

---

## 1. F-1…F-11 与 CHK025 的闭合核对

| Finding | Closed? | Evidence (path:line) | 复核说明 |
|---------|---------|----------------------|----------|
| **F-1** / CHK003 — 保留锚点正文仍说退役词汇，FR-038/C-38 又要求"只改名" | **yes** | `requirements.md:187`（FR-005 把保留条目自身的定义正文列为活面，并把它交给 FR-038 归一化）；`requirements.md:232`（FR-038 第二步：A-N 规则逐行改写 + 逐行 `anchor-body-receipt.json` + 同一映射重算摘要）；`contracts/migration-cleanup.contract.md:45-64`（C-38 两子步 + A-N-1…A-N-4 规则表）；`research.md:171,184-195`（C5 类，基线 16 / 保留 11）；`tasks.md:156,176,184`（T050 / T067 / T075）；实测面 `094-goal-team-parallel/goal.md:11,15,19`（1 标题 + 2 条退役路径行） | 两个子步在需求、契约、数据模型三处给出同一读法：改名步逐字节断言，归一化步逐行回执；C5 目标 0 与实测 11 行对得上。**但 C-38 的命中数是错的**（见 R2-02） |
| **F-2** / CHK004 — `features.md` 被排除、`.specify/features/` 从未列入 | **yes** | `research.md:123`（`.specify/features/` 成为活根）；`research.md:139`（`.specify/features.md` 成为活文件根）；`research.md:150-158`（`.specify/features/**/*.md` 为**封闭且有记录**的排除，并给出判据"不是定义页"）；`research.md:173`（C7 类）；`requirements.md:300`（SC-001 明确含索引行残留）；`tasks.md:145,190,192`（T042 改 027/041/094 三行、T078 追加继任说明、T080 注册表写入后重跑） | SC-001 的测量集合现在是被声明闭集（根 − 封闭排除），全称断言与测量面同源可判。排除理由的引用有一处失准（见 O-1），不影响可判性 |
| **F-3** / CHK024 — 幂等判据 2 项 vs 3 项，摘要不等时结局相反 | **yes** | `requirements.md:237`（FR-043 三条件 + 目标在而回执缺 → exit 4 `half-state`；摘要不等 → exit 4 `conflict` 且指名两侧路径）；`requirements.md:306`（SC-007 同三条件）；`requirements.md:348`（D-4 同三条件）；`contracts/migration-cleanup.contract.md:96-108`（C-41 状态表）；`tasks.md:112,177`（T015 / T068） | 需求、SC、澄清、契约四处一致；`already-*` 只在三条件同时成立时给出，冲突分支不再有第二种结局 |
| **F-4** / CHK026 — R3"归档该团队"未操作化 | **partially** | 已闭合部分：`requirements.md:240`（FR-046 R3 终态 = 目录留在 `.specify/teams/<slug>/` + `lifecycle_state: archived` + 删除绑定行 + 目录内 `disposition-receipt.json` 记 `bound_slug`/`reason`/`acted`；归档后 `team.md` 仍是活定义）；`contracts/migration-cleanup.contract.md:166-180`（C-47）；`data-model.md:157-170`（E-10）；`tasks.md:163`（T057 六队同一条终态，含 091） | R3 终态在需求与契约中唯一。**但**修复记录声称同步改正的 `091` 记录仍有一处自相矛盾：`research.md:86` 写 `**R3, already satisfied** — record only`，而同文件 §4 开头（`research.md:80`）又说"每个处置各带一条回执"。这与 `classification.json:26`（`apply`）、`contracts/migration-cleanup.contract.md:176-179`、`plan.md:303-306`、`feature-ref.md:94`、`tasks.md:163` 全部相反 → 见 **R2-01** |
| **F-5** / CHK033 — SC-005 要求 R3 团队"五查通过"不可满足 | **yes** | `requirements.md:304`（SC-005 改为逐团队 `run-checks` 读数：仍有绑定者 `ok/false`，R3 六队 `no-goal-definition/false`/exit 0，且明写 "MUST NOT 被记作五查通过"）；`requirements.md:317`（Source 把五查枚举委托给 owner）；owner 实测 `skills/internal/run-team/SKILL.md:28,38`（§ 2 Preview 确实逐条列出五项）；`tasks.md:165`（T059 逐团队采集并交叉核对） | 需求不再重复枚举五查，判据可由引擎读数求值。结构旁证：引擎五条检查名 `scripts/python/goal-utils.py:318-320`，且无 `--target` 时检查①为信息项 `:1563-1565`，故绑定团队 ②–④ `not-evaluated` 的写法成立 |
| **F-6** / CHK031 — FR-061/SC-009 把 101 自己的新证据也圈进不变集 | **yes** | `requirements.md:258`（FR-061 对日期化 spec 目录与 test-evidence 都加"基线 `d7c9da7a3` 时已存在"限定，并明写 101 自身新增制品不在等值集）；`requirements.md:308`（SC-009 同限定 + 新增子树单列）；`tasks.md:179`（T070 只断言基线已存在文件）；`research.md:253-257`（R-12 逐文件、按集合比较） | 全称断言与其测量面同集合，FR-071 的新证据写入不再与受保护集冲突 |
| **F-7** / CHK034 — SC-008 无条件要求 docs build 通过（EP-006 已证伪） | **yes** | `requirements.md:307`（SC-008 的构建肢报 `not-evaluated` 并附 EP-006 读数，MUST NOT 记成通过，也不得连带把其余肢记未评估）；`requirements.md:320`（Source 按实际读数写 pass/not-evaluated）；`plan.md:261`（EP-006 = falsified，fallback 已记录）；`tasks.md:182`（T073 只记录读数） | 需求、plan 前提、任务三方一致，不会出现"前提已证伪而需求仍要求通过"的调和负担 |
| **F-8** / CHK017 — FR-065 单写者断言过宽，与既有 summary 写者冲突 | **yes** | `requirements.md:265`（FR-065 收敛为**定义文件** `anchor.md`/`goal.md`，`summary/**` 明列为允许的派生写者）；`contracts/goal-engine.contract.md:97-107`（C-31 白名单 + 注入用例）；`contracts/migration-cleanup.contract.md:191-207`（C-49 守卫措辞）；`tasks.md:33,174`（DoD-3 / T065） | 断言范围与白名单同址，合法写入不再触发假红 |
| **F-9** / CHK002 — Goal↔Anchor 关系只有否定式，`anchor_ref` 既未允许也未禁止 | **yes** | `requirements.md:186`（FR-004：schema MUST NOT 声明 `anchor_ref` 或任何以 Anchor 命名的键；唯一交叉引用是绑定 `origin`；Goal 与 SDD 并列而非从属）；`requirements.md:211`（FR-023 补 Goal 与 SDD/Team 关系）；`contracts/goal-command.contract.md:60-70`（C-20）；`data-model.md:64`（E-2 Forbidden 行）；`tasks.md:105`（T008） | 读者可判定"Goal 不能携带 Anchor 指针"。执行机制的一处精度问题见 O-2 |
| **F-10** / CHK009 — 引擎 8 处用户提示仍指向 `/speckit.goal`，`run-checks` 键仍 `goal_slug` | **yes** | `requirements.md:201`（FR-016 覆盖引擎面向用户输出 + `run-checks` 键 MUST 为 `anchor_slug`）；`contracts/goal-engine.contract.md:49-54`（C-26 横切消息规则 + 8 个站点）；`contracts/goal-engine.contract.md:131-134`（C-33 键改名）；`research.md:172,192-193`（C6 类，基线 40）；`tasks.md:114,120,145,184`（T017 / T023 / T042 / T075）；实测 `scripts/python/goal-utils.py:1274,1294,1304,1310,1360,1363,1377,1393` | 契约列出的 8 个站点与源码逐一对上；第 9 处字面量是模块 docstring `scripts/python/goal-utils.py:2`，非用户可见；`run-checks` 输出键实测在 `:1571`，与 C-33 的改名义务同一处 |
| **F-11** / CHK013 — `--scope auto` 只定义解析，未规定写动作 | **yes** | `requirements.md:222`（FR-031 第三句：`auto` 只读，任何写动作 exit 2 `scope-read-only`、零写入）；`contracts/goal-engine.contract.md:30-34`（C-25 已有该语义）；`data-model.md:209-210`（校验规则 4）；`tasks.md:108`（T011 点名该字面量） | 需求与契约同一读法，写动作在 `auto` 下没有第二种合法行为 |
| **CHK025** — T052 用 `archive-receipt.json`，与 FR-042/C-40 的 `migration-receipt.json` 不一致 | **yes** | `tasks.md:158`（T052 已改为 `migration-receipt.json`）；对侧 `requirements.md:236`（FR-042 两个方向同名）、`contracts/migration-cleanup.contract.md:89-94`（C-40） | 下游漂移已消除，三处同名 |

**计数**：closed 10 / partially 1（F-4）/ open 0。F-4 的未闭合部分不是需求正文的缺陷，而是修复波次引入的一处计划内两读（R2-01）。

---

## 2. 修复记录 §1 "Observations touched for coherence" 的逐项核对

| 一致性改动 | Landed? | Evidence (path:line) |
|------------|---------|----------------------|
| FR-010 `modify` 清空需显式批准 | **yes**（有一处精度问题，见 O-3） | `requirements.md:195`；契约侧 `contracts/anchor-command.contract.md:56-63`（C-7） |
| FR-019 清空完成条件集需显式批准 | **yes** | `requirements.md:207`；`contracts/goal-command.contract.md:39`（C-16） |
| FR-020 "非零退出" → exit 2 | **yes** | `requirements.md:208`；`contracts/goal-command.contract.md:25-26`（C-15 写明 exit 2） |
| FR-033 既有动作清单声明为示例而非封闭集 | **yes** | `requirements.md:224`（"该清单是示例而非封闭集：未列出的既有动作 MUST 同样保持其所服务层的原语义"）；契约动作表 `contracts/goal-engine.contract.md:36-47`（C-26）未把清单当封闭集 |
| SC-001 Source 不再指向需求内不存在的章节 | **yes** | `requirements.md:313`（只指向 `research.md` §5，无"§ Live-surface roots"式自指） |
| `classification.json` 的 `091-auto-git-closeout.state` → `apply` | **yes（但研究文件的处置表未同步）** | `classification.json:26`；反例 `research.md:86` → R2-01 |
| `research.md` §3 row 7 证据措辞更新 | **yes** | `research.md:55`（"Defines the durable binding model behind goal/Team (now Anchor/Team)"） |

---

## 3. 本轮新发现的缺陷

| ID | Propagation surface (first field) | Finding | Severity | Evidence |
|----|-----------------------------------|---------|----------|----------|
| **R2-01** | `research.md` §4 团队处置表 → T057/P7 执行 + SC-005 传感器 + `feature-ref.md` SC-005 行 | 修复把 `091-auto-git-closeout` 从 `already-satisfied` 改为 `apply`，但 self-declared 拥有"team disposition basis"的 `research.md` §4 仍记 `**R3, already satisfied** — record only`，并写"处置回执引用该行而不是再写一次"。同一状态在四处得到 `apply`、在一处得到 `already-satisfied`；照 §4 执行会留下归档 `team.md` 的 `goal_slug`（FR-047/FR-066 转红）且不写 `disposition-receipt.json`（SC-005/G-5 转红）。该矛盾是**本轮修复新增**的（修复前 `classification.json` 也是 `already-satisfied`，两处一致） | **medium** | `research.md:86` vs `classification.json:26`、`contracts/migration-cleanup.contract.md:176-179`、`plan.md:303-306`、`feature-ref.md:94`、`tasks.md:163`；§4 内部亦不自洽：`research.md:80`（"Every disposition carries its own receipt"）vs `:86`（"cites that line instead of writing it again"） |
| **R2-02** | C-38 的"measured surface"行 → T050 的逐行回执证据 | C-38 写"**9** A-N-1 lines … and **4** A-N-2/A-N-3 hits, all four inside `094-goal-team-parallel`"；实测该文件只有 **2** 处字面量 `.specify/goal\|teams`，位于 2 行（L15 / L19），A-N-3 形态零命中。修复记录与 C-38 的 4 是同一个错数；同一次修复产出的 `research.md:184-195` 与基线证据文件都写 2 行。目标（归零）与逐行回执机制不受影响，但逐站点核对者会看到"少了两处"的假缺口 | **low** | `contracts/migration-cleanup.contract.md:62-64` vs 实测 `094-goal-team-parallel/goal.md:15,19`；`research.md:187-188`（"9 headings 加 2 条退役路径行"）；`test-evidence/checklist-repair-residue-baseline-2026-11-12.txt:17,30-31` |

### Observations（登记为记录点，不阻断本轮判定）

- **O-1（F-2 排除理由的引用失准）**：`research.md:152-158` 用"改写它正是 FR-061 禁止的日期化记录损伤"为 `.specify/features/**/*.md` 的排除辩护，但 FR-061 的受保护集合（`requirements.md:258`）不含 `.specify/features/`，且 T078 正是要往这两页**追加**继任说明。该排除是 plan 阶段的封闭选择，不是 FR-061 的推论；排除本身仍可判（列在 `excluded_files` 且给出理由），故不升级。
- **O-2（F-9 执行机制的精度）**：`requirements.md:186` 把"未声明键以 exit 2 拒绝"挂到 FR-034 的接口契约，而 FR-034/C-34 的 `_sig_guard` 只拒绝未声明的**命令行选项**（`scripts/python/goal-utils.py:2570`）；引擎的 frontmatter 读取面是宽容的（`:408-430`），手改出的 `anchor_ref:` 不会被 `validate`/`goal-view` 拒绝。规范禁令清楚、可判；被引用的执行机制看不清楚这一点。
- **O-3（FR-010 的清空对象）**：FR-010 要求"清空目标叙述**或**成功判据"都需批准，而引擎的 `objective` 动作 `--set` 为必填（`scripts/python/goal-utils.py:2631-2635`），不存在清空目标的写入路径；C-7 也只把"criteria emptying"列为唯一破坏性写入。该 MUST 目前是空转而非冲突。
- **O-4（FR-043 对 anchor 条目的措辞）**：`requirements.md:237` 说"迁移前按同一映射计算的源摘要与归一化后的目标摘要相等"。anchor 条目并不迁移（原地改名 + 归一化），句中的"迁移前/目标"是借用迁移条目的话术；C-39 的"归一化前后两次读数相等"给出了可执行读法，两处不冲突，仅措辞漂移。

---

## 4. 门禁与结构自检读数

| Gate | Command | Reading |
|------|---------|---------|
| Checklist validator（存在性） | `find scripts .specify/scripts src -iname '*checklist*'` | **无结果** —— 项目不存在 checklist 校验器（与 round-1 同读数） |
| Pre-analyze（checklist 阶段） | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage checklist` | **rc=2** —— `invalid choice: 'checklist' (choose from 'requirements', 'plan', 'tasks')`；该预检拒绝本阶段 |
| Requirements baseline | `python3 scripts/python/validate-requirements.py .specify/specs/101-anchor-goal-realignment/requirements.md` | **ok** —— 375 lines, 81 definition rows, 8 shared strings; **0 error / 0 warning**（`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` / `path-marker` 全 pass） |
| Tasks baseline | `python3 scripts/python/validate-tasks.py .specify/specs/101-anchor-goal-realignment/tasks.md` | **PASS** —— 0 error(s), 0 warning(s) |
| Round-2 结构自检（本文件） | 见下方命令 | 见下方读数 |

**Round-2 结构自检**（确定性，作用对象是本文件而非需求）：每个 `Finding | Closed? | Evidence` 行的 finding id 覆盖 F-1…F-11 + CHK025 各恰一次；每个 `path:line` 引用的文件存在且行号不越界；`Closed?` 取值落在 `yes` / `partially` / `no` 内。

```
$ grep -oE '\*\*(F-[0-9]+|CHK0[0-9]+)\*\*' …round2.md | sort -u | wc -l   → 12  (F-1…F-11 + CHK025)
$ 逐条 path:line 解析（95 条引用）                                          → 0 missing, 0 out-of-range
$ §1 表行 Closed? 取值                                                     → 12 行，{yes:11, partially:1, no:0}
```

---

## 5. 本轮判定

**Verdict: fail**

- F-1…F-3、F-5…F-11 与 CHK025 = **closed**（10/11 + 下游漂移）。
- F-4 = **partially closed**：需求与契约侧（FR-046 / C-47 / E-10 / T057）已唯一，但修复记录自述已改正的 `091` 记录在 `research.md:86` 仍是旧值。
- 新发现：**R2-01 medium**（本轮修复引入的两读）、**R2-02 low**（计数与实测不符）。
- 按 round-2 判定规则（任一 F 未闭合，或引入 high/medium 新发现 → fail），本轮判定 **fail**，证据即上表；本层**不修复**，交回编排者。

**未修改**：requirements / plan / tasks / contracts / data-model / research / classification / 代码；本轮唯一写入是本文件。

**状态说明**：本文件不触发 Feature 状态转移（101 在 `.specify/features.md` 的状态不变）。
