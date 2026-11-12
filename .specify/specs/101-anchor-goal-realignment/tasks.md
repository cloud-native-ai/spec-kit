# Tasks: Anchor / Goal 语义反转与命令面清理（Anchor / Goal Realignment）

**Requirement ID**: 101
**Requirement Key**: 101-anchor-goal-realignment
**Related Feature**: 101 Anchor / Goal Realignment（`.specify/features/101-anchor-goal-realignment.md`）
**Input**: Design documents from `.specify/specs/101-anchor-goal-realignment/`
**Prerequisites**: `requirements.md`（71 FR / 10 SC / 8 STR / Clarifications D-1…D-5 / Assumptions A-1…A-12 / 14 条暂定分类清单）, `plan.md`（49 条款 C-1…C-49 / decision tensions T-001…T-004 / EP-001…EP-006 / Mirror Obligations / 六个工作包 / fence 六条）, `research.md`（R-01…R-14、§3 分类记录、§4 团队处置、§5 活根声明）, `data-model.md`（E-1…E-11）, `contracts/`（anchor-command / goal-command / goal-engine / migration-cleanup）, `classification.json`（9 anchor / 3 action-goal / 2 obsolete，7 条团队处置）, `quickstart.md`（S-0…S-8）, `feature-ref.md`

**Tests Mode**: ON — Constitution Principle IV（Test-First & Contract-Driven Implementation）为 test-mandating 原则，`plan.md` § Constitution Check 该行亦记录了本特性承担的义务；`plan.md` § Testing Strategy 以 G-1…G-10 指名每个守卫的真实测试文件，并声明"subject 完好时才为绿"不算证据。

**Tests**: MANDATORY。红先证据落在 `.specify/specs/101-anchor-goal-realignment/notes/red-first-evidence.md`，执行读数落在 `.specify/specs/101-anchor-goal-realignment/test-evidence/`。plan 把守卫集中在 WP-05（实现之后），所以每一行的红先义务由下列之一满足：(a) 其守卫模块先建、先观察红、再实现；(b) 其主体先实现、再由守卫覆盖时，做**注入检查**——改写主体让守卫必须转红、观察红、还原，读数记入证据文件。这两条都是可复核的红，而不是"跑一遍是绿的"。

**Organization**: Setup 之后按 `plan.md` § Decomposition 的六个工作包（WP-01…WP-06）分为七个**非故事**阶段。工作包是分解脊：每行以 `[WP-0N]` 标注所属包，write territory 逐行点名，FR 段与 fence 由 plan 拥有、本文件不复述。用户故事（US1…US6）到行的对应见 § SC → 行 trace 与各阶段的覆盖行；行内不贴 `[US]` 标签，因为阶段是按工作包而不是按故事切分的。

## Phase Map

| Phase | 工作包 | 目的 | 行 |
|-------|--------|------|----|
| 1 Setup | — | 三类基线（受保护路径、套件失败集、子句覆盖）与读数落点 | T001–T005 |
| 2 WP-01 | 概念 owner + 引擎 | 两份 owner 换主与重写；引擎按层解析、四成员 `--scope`、两个动作组、五个消费者 | T006–T025 |
| 3 WP-02 | 命令面 | 七模式 `/speckit.anchor`、四模式 `/speckit.goal`、两技能、四套副本、两参考页 | T026–T034 |
| 4 WP-03 | 活面收敛 | 六份共享定义、glossary、pattern、setup / house-keeping、四团队域技能、教程、处置回顾面 | T035–T047 |
| 5 WP-04 | 清理与处置 | 分类证据、`--check`、9 改名 / 3 迁移 / 2 归档、summary、16 行改名、R2、6×R3、幂等复跑 | T048–T060 |
| 6 WP-05 | 守卫与读数 | 夹具 + G-1…G-10 + not-evaluated 读数 + 守卫读数索引 | T061–T077 |
| 7 WP-06 | 注册与收尾 | 041 继任说明、注册表、全量复核、`verification.md` | T078–T081 |

**Row count and ID shape**: 81 rows, `T001`…`T081`, one ID per row, no gaps, contiguous in execution order; each row names its package tag, its write territory and its evidence obligation.

## Definition of Done (DoD)

- DoD-1: **FR lane** — FR-001…FR-071 每条都被至少一个任务行按 `pre-analyze-check.py` 认可的形态引用（`- [ ] T<NNN>` 行内出现该 FR id；表格单元或散文提及不算），§ FR → 行 trace 记录全部出现位置。Check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage tasks --spec-dir .specify/specs/101-anchor-goal-realignment --json-out .specify/.tmp/pre-analyze-tasks-101.json` 的 FR 覆盖项无残留，且 runtime `in-scope` 行（FR-047 / FR-048 / FR-049 / FR-054 / FR-057 / FR-070）逐条在行内被引用。
- DoD-2: **SC lane** — SC-001…SC-010 每条都有具名传感器行与证据路径，`**Path**` 为 `final` 的判据必须拿到 pass 读数；SC-008 的文档站构建腿按 EP-006 报 `not-evaluated` 并附复证，绝不写成通过。Check: § SC → 行 trace 与 T077 的读数索引交叉核对。
- DoD-3: **单写者** — 两层定义文件的写入面静态审计只有一个引擎写者（派生 `summary/**` 在定义写者之外），注入引擎外写入后审计转红；不存在第二套引擎、schema 或迁移工具。Check: GATE-3 与 T065。
- DoD-4: **零丢失** — 每条被迁移 / 归档条目有逐条 JSON 回执，概念摘要前后相等，删除数为 0，Target 语句原样保留。Check: T051 / T052 / T059 的读数与 T070。
- DoD-5: **幂等与可续做** — 第二次 apply 零新增 diff、零重复回执；两处中断注入都能从报告阶段续做，I5 半状态 exit 4 且不被静默修复。Check: T060 / T068 / T069。
- DoD-6: **受保护历史不动** — FR-061 集合以 `d7c9da7a3` 为基线逐文件相等，无一被删除；本特性新增的 `.specify/archive/anchoring/**` 按"新增"单列。Check: T002 / T070 / GATE-4。
- DoD-7: **镜像与副本是生成的** — `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 无**新增**漂移；两个命令模板到达四套既有副本，未新建工具目录、未手写副本。Check: GATE-2。
- DoD-8: **本阶段裁决全部披露** — 四条 `PLAN-EDIT:` 更正、`[green:]` 标签的省略、非故事阶段划分、守卫后置下的红先满足方式，全部写在 § Notes，绝不折进绿里。

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件零**新增**失败——按失败用例 id 名与 T003 入口基线做集合差（不是计数比较，也不是并行模式读数）。Check: `bash scripts/bash/run-tests.sh` 后 `comm -13 <入口基线失败集> <收尾失败集>` 为空；读数在 T080。
- GATE-2: 每条镜像义务成立——`python3 scripts/python/sync-mirrors.py --check` 只报基线已有 DIFF（`shared` / `skills` / `scripts` / `templates` 四对），`python3 scripts/python/regen-command-copies.py --check` exit 0。
- GATE-3: 定义写者唯一且两层存储纯净——`tests/contract/test_goal_store_write_boundary.py` 绿，且其注入用例在临时改写后转红；锚点档内 `action-goal` 条目数为 0。
- GATE-4: 受保护路径与基线相等——`tests/integration/test_101_protected_paths.py` 绿，且新增归档子树被单列而未计入失败。
- GATE-5: 每条 `final` 路径 SC 为 pass 且冒烟记录在案——`verification.md` 中每个 `**Path**: final` 判据有 `SC-NNN_status=pass` 以及 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`；`supporting` 判据按 T077 索引取值。
- GATE-6: 结构与 FR lane 静默——`python3 .specify/scripts/python/validate-tasks.py .specify/specs/101-anchor-goal-realignment/tasks.md` exit 0，且 `pre-analyze-check.py --stage tasks` 判定通过。
- GATE-7: 命令面契约成立——`python3 scripts/python/goal-utils.py --help` 与 `--version` exit 0 且零副作用；`--scope goal` 以非法取值失败；`/speckit.goal targets` 的子进程调用 exit 2 且 stderr 含字面 `anchor-only-mode` 并点名 `/speckit.anchor`。

## Environment Prerequisites

Probed 2026-11-12 in `/storage/project/cloud-native-ai/spec-kit` on `master`（stage base `8f91310f7`）。引用本节的每一行都以此为判决，不逐行复述；实现入口必须复测，读数不得跨轮缓存。

- CPython 解释器（引擎、守卫、夹具）：**available** — `python3 --version` → `Python 3.11.11`（`pyproject.toml` 声明 `>=3.8`）。affects：每个引擎行与守卫行。
- `pytest` 运行器：**available** — `python3 -m pytest --version` → `pytest 8.4.2`；所有测试经 `bash scripts/bash/run-tests.sh` 执行（默认并行，`-m contract` / `-m integration` 选择标记），不得用裸测试 CLI 或 `-m` 模块入口。affects：T003、T062–T072、T080。
- `git`：**available** — `git --version` → `2.43.5`；`d7c9da7a3^{commit}` 可解析。affects：T002、T006、T070。
- `hugo`：**available 但构建失败** — `hugo version` → `v0.141.0+extended`；`hugo --renderToMemory` 在本仓 exit 1，报 `.Site.Language.Locale: can't evaluate field Locale in type *langs.Language`（EP-006，特性前既有）。affects：T073 只记录 `not-evaluated`，任何收敛任务都不得用该构建评分。
- 外部服务 / 容器 / 网络：**不需要**。

## Format

每行一条、单行不折行，形如：任务状态框 + 任务 id + 工作包标签 + 动作 + write territory + 证据义务 + 依赖键。依赖键的取值是行号列表，模板语法见 `templates/tasks-template.md` § Format（本文件不复述其占位符形态）。

- `[P]` 只标在 write territory 与本阶段其他 `[P]` 行互不相交的行上（同一文件、同一镜像对都算冲突）。
- 依赖以 `blockedBy` 键声明，取值是任务行号、逗号分隔；顺序即执行顺序，前向依赖不入表。
- 本文件**不使用** `[green: <contract>#<clause>]` 形式的条款归属标签，原因见 § Notes N-4；条款级归属由 plan 的 49 条款与守卫行按段对应，FR 级可追溯性由 DoD-1 的逐行引用承担。
- 任务状态记号沿用模板块：`- [ ]` 待办、`- [x]` 完成、`- [>]` 阻塞、`- [~]` 取消。

## Path Conventions

源与镜像的方向是既定的：`shared/`、`skills/`、`scripts/`、`templates/`、`src/`、`docs/` 是源，`.specify/` 下的是镜像与运行期产物。镜像行只做 `sync-mirrors.py --write` 后再 `--check`，从不手写；命令副本只经 `regen-command-copies.py` 生成。本规格自身的产物（`tasks.md`、`test-evidence/`、`notes/`、`verification.md`、`classification.json`）不是镜像对象。

### Premises measured at generation time (2026-11-12)

| 量 | 实测 | 复现 | 朴素形态的陷阱 |
|----|------|------|----------------|
| 锚点档条目 | 14 个目录，各持定义文件；5 棵 `summary/` | `ls -d .specify/anchoring/*/` | 用引擎 `list` 数团队——它今天只读锚点档 |
| 团队定义 | 20 个；16 条 `goal_slug`；4 个无绑定；2 处悬空绑定 | `grep -l '^goal_slug:' .specify/teams/*/team.md \| wc -l` | 把 `list --scope teams` 当团队清单（新增后仍 `scope-not-applicable`） |
| Goal 存档 | `.specify/goals/` 不存在 | `test -e .specify/goals` | 把单数历史路径当既有目录 |
| 归档目的地 | `.specify/archive/anchoring/` 不存在 | `test -e .specify/archive/anchoring` | 把"已存在子树"当基线 |
| 引擎身份 | `goal-utils.py 0.0.22`，`--help` exit 0 | `python3 scripts/python/goal-utils.py --version` | 用 `.specify/scripts/python/` 的镜像判定版本 |
| 镜像基线 | `sync-mirrors.py --check` exit 0（`shared/` 113 文件逐字节一致） | 同名 | 把基线已有 DIFF 记成本特性漂移 |
| 副本基线 | `regen-command-copies.py --check` exit 0 | 同名 | 为 `hermes` / `codex` 新建副本目录 |
| 残留基线 | C1 4 · C2 0 · C3 7 · C4 15（26 行） | `test-evidence/live-semantic-scan-baseline-2026-11-12.txt` | 用 80 字符窗口的宽 pattern，会多出 16 行无关命中 |
| flow-class 台账 | 89 单元 / 0 findings / floor 39 / `check` exit 0 | `python3 scripts/python/flow-class-check.py --action check` | 加行不改计数声明 |
| 文档站 | hugo v0.141.0 渲染 exit 1 | `hugo --renderToMemory` | 用管道取到 `tail` 的退出码，误判为 0 |
| 基线提交 | `d7c9da7a3` 可解析 | `git cat-file -e d7c9da7a3^{commit}` | — |

---

## Phase 1: Setup — 读数与证据落点

- [ ] T001 [SETUP] 建立本规格的两处证据落点（`notes/`、`test-evidence/`），并把实现入口的实测读数连同取数命令与日期逐条写入测量文件：14 个锚点条目目录、20 个团队定义、16 条绑定、5 棵派生 summary、残留基线（C1 4 · C2 0 · C3 7 · C4 15）、flow-class 台账 89 单元——作为后续所有读数行的对照面，无读数的结论一律 `not-evaluated`（FR-071）。write: `.specify/specs/101-anchor-goal-realignment/notes/pre-change-measurements.md`（证据目录只创建、不预填）。
- [ ] T002 [P] [SETUP] 采集受保护路径的实现入口基线：对 FR-061 集合在特性前提交 `d7c9da7a3` 上逐文件 `git hash-object`，输出分两组——"基线已存在"（参与等值断言）与"本特性将新增的归档子树"（只登记目录前缀，不预填内容）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/protected-paths-entry.txt`；证据: G-8 的对照输入（FR-069, FR-061）。[blockedBy: T001]
- [ ] T003 [P] [SETUP] 经 `bash scripts/bash/run-tests.sh` 跑一次全量套件，按**失败用例 id 名**（不是计数、不是并行模式读数）记录入口失败集，连同退出码与耗时写入证据目录；此后 GATE-1 只做集合差（FR-062, FR-071）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/suite-baseline-entry.txt`。[blockedBy: T001]
- [ ] T004 [P] [SETUP] 冻结本规格的子句与覆盖基线：以 `account-clause-coverage.py --freeze`（`--spec-dir` 指本规格、`--corpus-root` 指仓根）生成覆盖基线，供收尾判定"条款覆盖面无退化"。write: `.specify/specs/101-anchor-goal-realignment/coverage-baseline.txt`；证据: T080 的收尾对照（FR-071）。[blockedBy: T001]
- [ ] T005 [SETUP] 实测既有套件的受影响面：对 plan § Testing Strategy 与 § Mirror Obligations 点名的既存模块（命令模板解析、引擎、绑定、参考矩阵、镜像与副本守卫）逐个确认其断言了哪条将被改名的事实，把"模块 → 断言 → 改法"三列追加到 T001 的测量文件；本行不根据文件名猜内容，只登记实测结果（FR-071）。write: 追加 `.specify/specs/101-anchor-goal-realignment/notes/pre-change-measurements.md`；证据: T025 / T034 / T047 的行集合取自本行。[blockedBy: T001]

## Phase 2: WP-01 — 概念 owner 与引擎

- [ ] T006 [WP-01] 以 `git mv` 把 `shared/definitions/goal-definitions.md` 改名为 `shared/definitions/anchor-definitions.md`，并在同一包内从移动前的 blob 重建 Goal owner 原文件，使"内容换主"这一步留在 git 历史里而不是一次覆盖式改写；本行与 T007 之间必须有一次提交边界（R-08）（FR-006）。write: `shared/definitions/anchor-definitions.md`, `shared/definitions/goal-definitions.md`；证据: 两文件的 `git log --follow` 读数写入红先证据文件。
- [ ] T007 [P] [WP-01] 重写 Anchor 的唯一 owner：仓载 Anchor 定义（项目级、长周期、跨交付物持续追求的 authored end state）、构成为"目标叙述 + 至少一条可验证成功判据 + 生命周期"、档案层与定义文件 [[STR-001]]、共享三键绑定记录（`owner` / `owner_id` / `origin`）与生命周期取值的**唯一 owner**、Target 分解与 Anchor–Team 绑定，并以 § Archive Layers 承担 `--scope` 封闭四成员的唯一所有权；其他面（含 Goal owner 与引擎 `--help`）只按路径引用（FR-001, FR-002, FR-007, FR-008, FR-009, FR-030）。write: `shared/definitions/anchor-definitions.md`；证据: G-3 的标题断言 + T074 的 SC-010 复述。[blockedBy: T006]
- [ ] T008 [P] [WP-01] 重写 Goal owner 为**行动级、短周期、可执行的实际指导**：指导叙述（MAY 为步骤形）、至少一条可验证完成条件、生命周期、存档 [[STR-002]] 与身份文法；按路径引用 FR-002 的绑定与生命周期 owner，且不得定义 Targets、团队绑定、coordinate 或任何控制层级位置；同一次重写删净本文件内"Goal = 项目级"的全部残留（FR-003, FR-004, FR-005, FR-024）。write: `shared/definitions/goal-definitions.md`；证据: 残留 C1 在本文件的命中从基线归零（T075 读数）。[blockedBy: T006]
- [ ] T009 [WP-01] 在引擎内把单一全局文件名常量替换为按层解析（`anchor` → 锚点定义文件、`goals` → Goal 定义文件、`teams` → 团队定义文件），并让 `summary_dir()` 走同一解析；引擎与全部消费者不得再假定单一文件名，且定义文件层面仍只有本引擎一个写者（FR-028, FR-029）。write: `scripts/python/goal-utils.py`；证据: `--help` / `--version` 与既有动作的回归读数。[blockedBy: T007, T008]
- [ ] T010 [WP-01] 把 `--scope` 收敛为封闭四成员（`anchor` / `teams` / `goals` / `auto`），退役成员 `goal` 与单数 `team` 以非法取值失败（exit 2）且不静默回退；取值集只在 Anchor owner § Archive Layers 定义，引擎 `--help` 按路径引用（FR-030）。write: `scripts/python/goal-utils.py`。[blockedBy: T009]
- [ ] T011 [WP-01] 实现 `--scope auto` 的三层解析：slug 不存在于任何层、或多于一层命中时 exit 2 并指名候选，不得猜测；写入类动作在 `auto` 下以只读拒绝（FR-031）。write: `scripts/python/goal-utils.py`。[blockedBy: T010]
- [ ] T012 [WP-01] 新增行动级 Goal 动作组（`goal-create` / `goal-list` / `goal-view` / `goal-modify` / `goal-status`）：只写 `.specify/goals/<goal-slug>/goal.md`（[[STR-002]]），拒绝跨层写入与同名 slug 双存；`goal-create` 至少要求一条 `--done`，撰写接受步骤形文本（不施加 Anchor 的 outcome-not-steps 校验），`goal-status` 无 `--set` 只报告，终态 Goal 保留在存档不被删除（FR-021, FR-024, FR-025, FR-032）。write: `scripts/python/goal-utils.py`；证据: 跨层写入拒绝的注入用例（T065 的 subject）。[blockedBy: T010]
- [ ] T013 [WP-01] 新增清理动作组的外壳：`cleanup --check|--apply --classification <path>`，先做输入裁决（schema、class/rule 配对、条目完整性、`mapping_version`、`baseline_commit` 可解析），非法输入 exit 2 且零写入；`cleanup` 不接受 `--scope`（`scope-not-applicable`，exit 2）（FR-032, FR-035）。write: `scripts/python/goal-utils.py`。[blockedBy: T012]
- [ ] T014 [WP-01] 实现清理的字段映射、概念摘要与回执：映射限于五项（文件位置、`## Objective` → `## Guidance`、`## Success Criteria` → `## Completion Conditions`、标题与身份、Targets 容器），摘要为映射后归一化投影的 `sha256` 并在动作前后各算一次，回执逐条落在动作目标内且带 `delete_policy: archive-not-delete`（FR-039, FR-040, FR-042, FR-043）。write: `scripts/python/goal-utils.py`；证据: T068 的摘要与 Target 丢失去例。[blockedBy: T013]
- [ ] T015 [WP-01] 实现幂等、可续做与冲突：第二次 apply 对每条报 `already-*` 且零新增写；在"移除源"前中断后重入报所处阶段并从该阶段续做；目标 slug 已存在且载荷不等价时停下、指名两个候选、不覆盖也不择一（FR-043, FR-044, FR-045）。write: `scripts/python/goal-utils.py`；证据: T068 / T069 两个模块的 subject。[blockedBy: T014]
- [ ] T016 [WP-01] 实现清理阶段机的余项：团队结构改名（每文件只改一行）、团队正文术语归一化（逐行记入回执）、R1 / R2 / R3 处置、派生 summary 随定义移动或归档、以及收尾自检（锚点档纯度、绑定可解析、回执齐备、无孤立 summary）（FR-046, FR-047, FR-048, FR-049）。write: `scripts/python/goal-utils.py`；证据: T071 的夹具收敛断言。[blockedBy: T015]
- [ ] T017 [WP-01] 把既有动作适配到新层与 `anchor_slug`：`list` 支持 `--scope goals`、对 `--scope teams` 返回 `scope-not-applicable`；`validate` / `binding` / `targets` / `run-checks` / `handoff-decision` / `handoff-ref` / `probe-residual` 保持原语义只换文件名与字段；`targets` 与 `coordinate` 作用于 Anchor 及其绑定团队，`migrate-archive` 仍是 spec-local 遗留定义树的唯一显式迁移入口（FR-033, FR-015, FR-023, FR-017）。write: `scripts/python/goal-utils.py`。[blockedBy: T016]
- [ ] T018 [WP-01] 让 `command-family` 按定义层分别作答（每层一个判定，而不是单一布尔），并迁移一个既有消费者读新形状（FR-027）。write: `scripts/python/goal-utils.py`；证据: T072 的按层断言。[blockedBy: T017]
- [ ] T019 [WP-01] 让 `migrate` 从团队内联目标派生 **Anchor**（产出锚点定义文件，而不是 Goal），目标层已存在时停下并指名候选（FR-015, FR-045）。write: `scripts/python/goal-utils.py`。[blockedBy: T017]
- [ ] T020 [WP-01] 保持脚本接口契约：`-h` / `--help` / `--version` 零副作用，未声明选项被拒绝；新增动作的声明选项（`--classification`、`--guidance`、`--done`、`--clear-done`）进入签名守卫（FR-034）。write: `scripts/python/goal-utils.py`；证据: GATE-7 的三条读数。[blockedBy: T018, T019]
- [ ] T021 [WP-01] 同包适配两个工作流脚本消费者：`scripts/python/sdd-route.py` 的 scope 投影改为四成员并区分锚点侧与行动级 Goal 的路由，`scripts/python/concurrency-check.py` 的布局探针改读锚点定义文件（FR-029, FR-031）。write: `scripts/python/sdd-route.py`, `scripts/python/concurrency-check.py`。[blockedBy: T010]
- [ ] T022 [WP-01] 同包适配三个技能内脚本消费者：两份 `logical-framework.py`（`skills/external/sdd-project-setup/scripts/` 与 `skills/external/sdd-house-keeping/scripts/`）改读锚点存档与 `anchor_slug`，`skills/internal/create-team/scripts/build-summary-input.py` 的 summary 输入路径改指 `.specify/anchoring/<slug>/summary/`（FR-029, FR-058）。write: `skills/external/sdd-project-setup/scripts/logical-framework.py`, `skills/external/sdd-house-keeping/scripts/logical-framework.py`, `skills/internal/create-team/scripts/build-summary-input.py`。[blockedBy: T009]
- [ ] T023 [WP-01] 同包适配 CLI 静态指针：`MIGRATE_STATIC_POINTERS` 的 owner 命令改为 `/speckit.anchor`，行动级 Goal 的提示与可选命令列表按四模式更新（FR-016, FR-015）。write: `src/specify_cli/__init__.py`。[blockedBy: T017]
- [ ] T024 [WP-01] 同步本包镜像并复核"无新增漂移"：先 `python3 scripts/python/sync-mirrors.py --write`，再 `--check`，只允许基线已有 DIFF；`shared/definitions` 与 `scripts/python` 两对必须逐字节一致（FR-029）。write: `.specify/shared/definitions/anchor-definitions.md`, `.specify/shared/definitions/goal-definitions.md`, `.specify/scripts/python/goal-utils.py`, `.specify/scripts/python/sdd-route.py`, `.specify/scripts/python/concurrency-check.py`；证据: `--check` 输出追加到测量文件。[blockedBy: T021, T022, T023]
- [ ] T025 [WP-01] 更新本包改名所触红的既有测试模块（集合由 T005 实测给出，覆盖引擎 / 定义 / 写入面 / 布局迁移类模块），记录"先红后绿"的 diff 与用例名；本包内收口，不留跨包残红（FR-029, FR-033）。write: T005 点名的本包既有测试模块；证据: `notes/red-first-evidence.md`。[blockedBy: T024]

## Phase 3: WP-02 — 命令面

- [ ] T026 [WP-02] 编写 canonical 模板 `templates/commands/anchor.md`：`argument-hint` 恰为七模式（`create` / `view` / `modify` / `targets` / `migrate` / `migrate-archive` / `coordinate`），定位为锚点档案的唯一撰写入口（引擎是唯一写者，派生 `summary/**` 由既有总结流刷新），`--scope` 取值只按路径引用 Anchor owner 而不复述集合，模式语义委派七模式技能（模板不复述技能的模式表），`## Wrap-up` 块留给 T040 编译填充（FR-010, FR-011, FR-012, FR-013, FR-015, FR-016）。write: `templates/commands/anchor.md`；证据: G-1 的 subject。[blockedBy: T016]
- [ ] T027 [P] [WP-02] 重写 canonical 模板 `templates/commands/goal.md`：恰四模式（`create` / `view` / `modify` / `status`），`view` 无 slug 时只读列出 Goal 存档，`status` 报告并可转换共享三值生命周期；四个 Anchor-only 模式（`targets` / `migrate` / `migrate-archive` / `coordinate`）以字面 `anchor-only-mode` 具名拒绝、点名 `/speckit.anchor`、exit 2、零写入、不静默回退 `view`；定位只写行动级 Goal 存档（FR-019, FR-020, FR-021, FR-026）。write: `templates/commands/goal.md`；证据: G-2 的 subject。[blockedBy: T012]
- [ ] T028 [WP-02] 编写七模式技能（`skills/internal/manage-anchor/SKILL.md`）：模式表只在此处一份，命令模板按路径引用它；`targets` / `coordinate` 作用于 Anchor 的 Targets 与绑定该 Anchor 的团队，`migrate` 从团队内联目标派生 Anchor，`migrate-archive` 仍是 spec-local 遗留树的唯一显式迁移入口（archive-not-delete）（FR-011, FR-012, FR-015）。write: `skills/internal/manage-anchor/SKILL.md`。[blockedBy: T026]
- [ ] T029 [WP-02] 把四模式技能（`skills/internal/manage-goal/SKILL.md`）重写为四模式并删除七模式表，不得再暴露 Targets、迁移、coordinate 或团队操作，与新 Goal owner 的构成一致（FR-022）。write: `skills/internal/manage-goal/SKILL.md`。[blockedBy: T027]
- [ ] T030 [WP-02] 经 `regen-command-copies.py` 只对**已存在**的四套副本目录重新生成两个命令的副本并 `--check` 复核：不新建工具目录、不手写任何副本，副本携带七模式 / 四模式 hint（FR-013, FR-010, FR-019）。write: `.claude/commands/speckit.anchor.md`, `.github/prompts/speckit.anchor.prompt.md`, `.qoder/commands/speckit.anchor.md`, `.opencode/command/speckit.anchor.md` 及 `/speckit.goal` 的同名四份。[blockedBy: T026, T027, T028, T029]
- [ ] T031 [WP-02] 编写参考页 `docs/reference/commands/anchor.md`：七模式的执行流程、唯一撰写入口定位、`--scope` 按 owner 引用、与四模式命令的分工（FR-013, FR-057）。write: `docs/reference/commands/anchor.md`。[blockedBy: T026]
- [ ] T032 [P] [WP-02] 重写参考页 `docs/reference/commands/goal.md`：新概念与四模式；任何活段落不得再把该命令写成项目级目标的撰写入口或锚点档案入口（FR-026, FR-057）。write: `docs/reference/commands/goal.md`。[blockedBy: T027]
- [ ] T033 [WP-02] 同步本包镜像并复核：两个技能树落到 `.specify/skills/internal/` 对应位置，`sync-mirrors.py --check` 无新增漂移；同时断言 `templates/commands/` 不产生 `.specify/templates/commands/` 镜像（该镜像面已退役）（FR-013）。write: `.specify/skills/internal/manage-anchor/SKILL.md`, `.specify/skills/internal/manage-goal/SKILL.md`。[blockedBy: T028, T029]
- [ ] T034 [WP-02] 更新本包改名所触红的既有测试模块（集合由 T005 给出，覆盖模板解析、hint 模式数、参考页矩阵与副本一致性），红先 diff 记入证据文件（FR-010, FR-019）。write: T005 点名的本包既有测试模块；证据: `notes/red-first-evidence.md`。[blockedBy: T030, T033]

## Phase 4: WP-03 — 活面收敛

- [ ] T035 [WP-03] 在 framework-map 中分别列出锚点存档、Goal 存档、锚点归档目的地与团队存档四行，每行点名其 owner，其余行不动（FR-050）。write: `shared/definitions/framework-map.md`。[blockedBy: T007]
- [ ] T036 [P] [WP-03] 重写 glossary 的相关行：删掉把项目级档案写成历史单数路径的过期描述，定义 Anchor、Anchor Archive、Anchor–Team Binding、行动级 Goal 与 Goal 存档，并把 Re-Anchoring / direction anchor 与 anchoring archive 明确消歧；所有活行中引用旧路径或旧绑定字段名的一并改新，裸词 "anchoring" 不得指代行动级 Goal（FR-051, FR-009, FR-017）。write: `.specify/glossary.md`。[blockedBy: T007, T008]
- [ ] T037 [P] [WP-03] 改写路由定义：Anchor 位于控制层级最高层、Goal 移出该层级；锚点侧共享定义的改写路由到 `/speckit.anchor`，团队侧仍走 `/speckit.team`，行动级 Goal 由四模式命令管理且不进入该层级（FR-052）。write: `shared/definitions/sdd-routing-definitions.md`；证据: T067 的 C2 回归网。[blockedBy: T007]
- [ ] T038 [P] [WP-03] 改写 re-anchoring 定义的 § Anchoring archive：实体定义改为按路径引用 Anchor owner，保留它自己拥有的三条边，不重定义实体（FR-053）。write: `shared/definitions/re-anchoring-definitions.md`。[blockedBy: T007]
- [ ] T039 [WP-03] 更新 flow-class 台账：新增七模式命令行、更新四模式命令行、技能行反映两个技能的模式数；在同一变更内用 `flow-class-check.py --action check` 重测台账自身的计数声明与漂移守卫期望（FR-054, FR-027）。write: `shared/definitions/flow-class-definitions.md`；证据: 重测后的台账读数写入证据目录。[blockedBy: T026, T028, T029]
- [ ] T040 [WP-03] 在探针登记处新增七模式命令的 wrap-up 探针对象、绑定与 docs 面，保留四模式命令的探针；随后用 `probe-utils.py --action compile-embeds` 重生成两个命令模板的 `## Wrap-up` 嵌入（不手改，指纹随登记处变化），并重跑 T030 的副本再生成让副本同步（FR-014, FR-055）。write: `shared/definitions/probe-definitions.md`, `templates/commands/anchor.md`, `templates/commands/goal.md`；证据: 编译前后 diff 与副本 `--check` 读数。[blockedBy: T026, T039]
- [ ] T041 [WP-03] 修正项目 setup 与 house-keeping 两个技能：检查锚点存档而不是历史路径，并在 bootstrap / 维护指引里点名七模式命令；其脚本已在 WP-01 适配，本行只改技能正文与引用页（FR-056）。write: `skills/external/sdd-project-setup/SKILL.md`, `skills/external/sdd-house-keeping/SKILL.md`。[blockedBy: T022]
- [ ] T042 [WP-03] 更新教程与前置表：`docs/tutorials/quickstart.md`、`docs/tutorials/installation.md` 及任何命令索引类页面按新语义列出两个命令，删除旧入口描述（FR-057）。write: `docs/tutorials/quickstart.md`, `docs/tutorials/installation.md`。[blockedBy: T031, T032]
- [ ] T043 [WP-03] 更新四个团队域技能（`create-team` / `improve-team` / `run-team` / `summarize-project`）：改用 Anchor 术语与 `anchor_slug`，交付目录写成 `.specify/anchoring/<slug>/summary/`，活页面不得再把历史单数路径当交付路径（FR-058, FR-017）。write: `skills/internal/create-team/SKILL.md`, `skills/internal/improve-team/SKILL.md`, `skills/internal/run-team/SKILL.md`, `skills/internal/summarize-project/SKILL.md`。[blockedBy: T022]
- [ ] T044 [P] [WP-03] 更新 interview pattern 及点名的其他活 pattern / 定义页：锚点撰写指向七模式命令，只有行动级指导指向四模式命令（FR-059, FR-016）。write: `shared/patterns/interview-pattern.md`。[blockedBy: T007]
- [ ] T045 [P] [WP-03] 更新非一次性处置回顾面的成员声明：`.specify/anchoring` 与 `.specify/goals` 成为成员，退役成员 `.specify/goal` 在 owner 声明中记录退役理由（镜像副本由 T046 同步）（FR-060）。write: `shared/declarations/facts/non-disposable-review-surface.yaml`。[blockedBy: T007]
- [ ] T046 [WP-03] 同步本包镜像并复核：本包改写的共享定义、pattern、成员声明与六个技能树（两个外部、四个内部）落到 `.specify/` 下同名位置，`sync-mirrors.py --check` 只允许基线已有 DIFF（FR-054, FR-060）。write: 上述源文件在 `.specify/` 下的同名镜像；证据: `--check` 输出追加到测量文件。[blockedBy: T035, T036, T037, T038, T039, T040, T041, T043, T044, T045]
- [ ] T047 [WP-03] 更新本包改名所触红的既有测试与检查（doc-consistency、glossary 协议、declaration 读取器、参考矩阵；集合取自 T005），红先 diff 记入证据文件（FR-051, FR-058）。write: T005 点名的本包既有测试与检查脚本；证据: `notes/red-first-evidence.md`。[blockedBy: T046]

## Phase 5: WP-04 — 清理、迁移与团队处置

- [ ] T048 [WP-04] 把分类记录落成实现期证据：逐条读出 `classification.json` 的 slug、status、Targets 数、class、rule id 与实测依据（目标数、summary 存在性），与 requirements § Assumptions 的暂定清单逐条比对；无偏差记明，有偏差记规则 id + 证据，不得静默改判（FR-035, FR-036, FR-037）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/classification-<date>.md`；证据: SC-003。[blockedBy: T016]
- [ ] T049 [WP-04] 跑 `cleanup --check`：渲染 9 anchor / 3 action-goal / 2 obsolete 与 7 条团队处置，断言零写入（调用前后工作树状态相同），输出全量保存；与目录枚举读数交叉核对（FR-035）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/cleanup-check-<date>.json`。[blockedBy: T048]
- [ ] T050 [WP-04] 执行 P1：9 个判为 anchor 的条目保持原位并持有锚点定义文件（由引擎改名完成），派生 summary 标记为待重生成而不是手改（FR-038）。write: `.specify/anchoring/<slug>/anchor.md`（9 条）；证据: 每条的状态行。[blockedBy: T049]
- [ ] T051 [WP-04] 执行 P2 迁移：`088-speckit-visualization`、`091-auto-git-closeout`、`draw-diagram-interactive` 迁入 `.specify/goals/<slug>/goal.md`，按声明映射改写字段、保留叙述 / 成功判据 / 生命周期 / 时间戳 / History，`088` 的 2 条 Target 语句原样保留在迁移后正文的固定标题下并在回执记身份（FR-039, FR-040, FR-042, FR-043）。write: `.specify/goals/`（3 条）+ 各条 `migration-receipt.json`。[blockedBy: T050]
- [ ] T052 [WP-04] 执行 P2 归档：`085-sdd-temporary-goal-team`、`post-refactor-mechanism-integrity` 经引擎归档动作连同回执进入 `.specify/archive/anchoring/<slug>/`，不得删除、不得以手工 `git mv` 替代引擎动作（FR-041, FR-042, FR-043）。write: `.specify/archive/anchoring/`（2 条）+ 各条 `archive-receipt.json`。[blockedBy: T051]
- [ ] T053 [WP-04] 执行 R2：为 `viz-skill-arena` 的悬空绑定经引擎 `migrate` 落成 Anchor `visualization-skill-selection`（不得手写锚点定义文件），并把该团队的绑定指向它（FR-046, FR-048）。write: `.specify/anchoring/visualization-skill-selection/anchor.md`, `.specify/teams/viz-skill-arena/team.md`。[blockedBy: T052]
- [ ] T054 [WP-04] 执行 P4：派生 summary 随定义处置——迁移 / 归档条目的 summary 移入对应目标并在回执记 `summary: moved`，锚点类条目的 summary 留给重生成；锚点存档内不得留下定义已不存在的孤立 summary（FR-049）。write: 对应目标目录内的 summary 子树。[blockedBy: T053]
- [ ] T055 [WP-04] 执行 P5 团队结构改名：16 个绑定团队的 frontmatter 绑定键由旧名改为 `anchor_slug`，每文件只改这一行、其余字节保持不变；4 个无绑定团队保持逐字节相同，作为 FR-047 验收场景的断言（FR-047）。write: `.specify/teams/<slug>/team.md`（16 个）。[blockedBy: T054]
- [ ] T056 [WP-04] 执行 P6 正文归一化：按声明的改写表（N-1…N-6）逐处更新团队定义正文中对绑定字段与交付路径的引用，逐行记入回执（FR-047, FR-058）。write: `.specify/teams/<slug>/team.md`（受影响的 16 个）。[blockedBy: T055]
- [ ] T057 [WP-04] 执行 P7 处置：5 个团队按 R3 归档（其中 `091-auto-git-closeout` 已满足，只记录并引用既有的 `lifecycle_state: archived` 行）、`demo-seat-dispatch` 按 R3 归档，同时删除其绑定行；每个受影响团队在自己的目录落一条处置回执（FR-046, FR-048）。write: `.specify/teams/<slug>/team.md`, `.specify/teams/<slug>/disposition-receipt.json`。[blockedBy: T056]
- [ ] T058 [WP-04] 重生成锚点类条目的派生 summary（经既有总结流，不手改），只作用于已有 summary 的目录，不为没有 summary 的条目凭空造一棵（FR-038, FR-049）。write: `.specify/anchoring/<slug>/summary/`（留下的 3 棵）。[blockedBy: T057]
- [ ] T059 [WP-04] 执行 P8 自检并把读数落盘：锚点档内无行动级条目、每个 `anchor_slug` 可解析、每条被迁移 / 归档条目有回执、无孤立 summary；与 SC-003 / SC-005 的来源交叉核对（FR-048, FR-049）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/cleanup-apply-<date>.json`。[blockedBy: T058]
- [ ] T060 [WP-04] 第二次执行 `cleanup --apply` 验证幂等：每条报 `already-*`、exit 0、零新增回执、工作树无新增条目，读数落盘作为 SC-007 的 supporting 证据（FR-043）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/cleanup-apply-2-<date>.json`。[blockedBy: T059]

## Phase 6: WP-05 — 守卫与读数

- [ ] T061 [WP-05] 建夹具 `tests/fixtures/anchor-goal-realignment/`：14 条目的分类夹具、20 个团队的绑定夹具（16 绑定 / 4 无绑定 / 2 悬空）、受保护路径夹具，以及一棵"行动级条目尚未迁出"的收敛前树；夹具只提供输入，读数由被测代码产出，不预填期望值（FR-062, FR-068）。write: `tests/fixtures/anchor-goal-realignment/`。[blockedBy: T059]
- [ ] T062 [WP-05] G-1 `tests/contract/test_anchor_command_surface.py`：模板缺失、模式数不等于 7、或模板复述 `--scope` 取值集而非按路径引用 owner 时转红；注入两种缺陷各观察一次红（FR-062；SC-002）。write: `tests/contract/test_anchor_command_surface.py`；证据: 红先读数入 `notes/red-first-evidence.md`。[blockedBy: T026, T030, T061]
- [ ] T063 [WP-05] G-2 `tests/contract/test_goal_command_surface.py`：四模式断言；对四个 Anchor-only 模式做子进程调用，采集 exit 2、stderr 含字面 `anchor-only-mode` 与指向七模式命令的文案、以及调用前后存储摘要不变；模板把 Anchor-only 模式当可接受模式时转红（FR-063, FR-020；SC-002）。write: `tests/contract/test_goal_command_surface.py`。[blockedBy: T027, T030, T061]
- [ ] T064 [WP-05] G-3 `tests/contract/test_anchor_definitions.py`：任一锚点条目缺锚点定义文件、或分类为 action-goal 的条目仍留在锚点档时转红（FR-064；SC-003）。write: `tests/contract/test_anchor_definitions.py`。[blockedBy: T050, T059, T061]
- [ ] T065 [WP-05] G-4 `tests/contract/test_goal_store_write_boundary.py`：静态写入面审计覆盖 `scripts/`、两层 `skills/`、`src/`、`templates/` 并对引擎开白名单；两写者模拟证明不同 slug 落到不同路径；注入一次引擎外的定义写入后必须转红（FR-065, FR-028；SC-006）。write: `tests/contract/test_goal_store_write_boundary.py`。[blockedBy: T012, T016, T061]
- [ ] T066 [WP-05] G-5 `tests/contract/test_binding_rename.py`：任一活团队定义（frontmatter 或正文，含已归档的团队定义，`runs/**` 除外）仍含旧绑定键、任一 `anchor_slug` 无法解析、受影响团队缺处置记录、或两处悬空绑定未解决时转红（FR-066；SC-005）。write: `tests/contract/test_binding_rename.py`。[blockedBy: T055, T056, T057, T061]
- [ ] T067 [WP-05] G-6 `tests/contract/test_live_semantic_residue.py`：活根从 `research.md` §5 的声明读取（测试不硬编码第二份根表），C1 / C3 / C4 与 C2 回归网在活根上计数为 0，且注入一句旧语义后必须转红（FR-067, FR-005；SC-001）。write: `tests/contract/test_live_semantic_residue.py`。[blockedBy: T046, T061]
- [ ] T068 [WP-05] G-7a `tests/contract/test_cleanup_idempotency.py`：第二次 apply 不新增 diff、不新增回执；注入重复回执、摘要不等或丢弃一个 Target 必须转红（FR-068, FR-043；SC-007）。write: `tests/contract/test_cleanup_idempotency.py`。[blockedBy: T060, T061]
- [ ] T069 [WP-05] G-7b `tests/contract/test_cleanup_resume.py`：在"移除源"之前与"写回执"之后各注入一次中断，断言重入报所处阶段并从该阶段续做；I5 半状态必须 exit 4 且不得被静默修复；不得存在无回执的删除（FR-068, FR-044）。write: `tests/contract/test_cleanup_resume.py`。[blockedBy: T060, T061]
- [ ] T070 [WP-05] G-8 `tests/integration/test_101_protected_paths.py`：以入口基线为对照，断言基线已存在的受保护路径逐字节不变且无一被删除；本特性新增的归档子树按"新增"单列、不计失败（FR-069, FR-061；SC-004, SC-009）。write: `tests/integration/test_101_protected_paths.py`。[blockedBy: T002, T059, T061]
- [ ] T071 [WP-05] G-9 `tests/integration/test_101_convergence.py`：在夹具树上断言锚点档无行动级条目、无旧绑定键幸存、无悬空 `anchor_slug`（FR-064, FR-066）。write: `tests/integration/test_101_convergence.py`。[blockedBy: T061, T064]
- [ ] T072 [WP-05] G-10 `tests/contract/test_command_family_101.py`：台账缺七模式命令行、参考页缺失、或命令族只答单一布尔时转红（FR-070, FR-027；SC-008）。write: `tests/contract/test_command_family_101.py`。[blockedBy: T018, T031, T039]
- [ ] T073 [WP-05] 记录文档站读数为 `not-evaluated`：在 `docs/` 跑一次内存渲染，保存退出码与 `.Site.Language.Locale` 报错原文作为 EP-006 的复证；该判据的构建腿据此报 `not-evaluated`，其余腿（参考页存在、台账行、探针面）照常测（FR-071）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/docs-build-<date>.txt`。[blockedBy: T042]
- [ ] T074 [WP-05] 生成读者复述记录：以 glossary 与两份 owner 为依据，逐词条复述 Anchor、anchoring archive、Re-Anchoring、行动级 Goal 的对象与所在目录；任一词条复述失败即该判定不通过，记录事实而不改写词条求通过（FR-009；SC-010）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/reader-restatement-<date>.md`。[blockedBy: T036]
- [ ] T075 [WP-05] 在活树跑 G-6 并把四类计数与基线（C1 4 · C2 0 · C3 7 · C4 15，合计 26）并列记录，作为最终读数；任何非零项必须定位到具体路径并回对应包修复，不得靠调整扫描根或排除项消音（FR-067）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/residue-scan-<date>.txt`。[blockedBy: T067]
- [ ] T076 [WP-05] 在实现后的树上逐条走 `quickstart.md` 的 S-0…S-8，记录真实输出（真实存储读数与夹具演练分开标注），失败或不适用逐条写明（FR-071）。write: `.specify/specs/101-anchor-goal-realignment/notes/quickstart-run.md`。[blockedBy: T060, T075]
- [ ] T077 [WP-05] 汇总守卫读数索引：FR-062…FR-071 每条判据一行，指向其证据路径与结果；无读数的判据一律写 `not-evaluated`，不得写通过（FR-071）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/guard-readings-<date>.md`。[blockedBy: T062, T063, T064, T065, T066, T067, T068, T069, T070, T071, T072, T073, T074, T075, T076]

## Phase 7: WP-06 — 注册与收尾

- [ ] T078 [WP-06] 在 041 的特性详情里追加一条指向本特性的继任说明（单向反向引用：其项目级 Goal 语义由本特性接手），不改 041 的状态、不改写任何日期化记录（FR-018）。write: `.specify/features/041-goal-registry.md`。[blockedBy: T077]
- [ ] T079 [WP-06] 更新本特性的详情与注册表：概览、关键变更、实现注记、状态判据写入特性详情，注册表 101 行的状态按 registry 协议取值并挂证据路径（FR-071）。write: `.specify/features/101-anchor-goal-realignment.md`, `.specify/features.md`。[blockedBy: T078]
- [ ] T080 [WP-06] 收尾全量复核：经 `bash scripts/bash/run-tests.sh` 跑一次全量，按**失败用例 id 名**与 T003 的入口基线做集合差（零新增失败），并复核 `sync-mirrors.py --check` 与 `regen-command-copies.py --check`，连同子句覆盖基线一并落盘（FR-071, FR-070）。write: `.specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-<date>.txt`。[blockedBy: T079]
- [ ] T081 [WP-06] 写 `verification.md` 的判据表：每条 SC 一行状态（`final` 路径必须 pass），`smoke_command` / `smoke_exit_code` / `smoke_evidence_path` 指向真实读数，`not-evaluated` 项保留原因（FR-071）。write: `.specify/specs/101-anchor-goal-realignment/verification.md`。[blockedBy: T080]

---

## Dependencies & Execution Order

阶段间是硬顺序：Setup → WP-01 → WP-02 → WP-03 → WP-04 → WP-05 → WP-06。`plan.md` § Decomposition 的依赖列是唯一所有者（WP-02 依赖 WP-01 的模式语义、WP-03 依赖 WP-01 与 WP-02、WP-04 依赖 WP-01 的引擎动作、WP-05 依赖 WP-01…WP-04、WP-06 依赖 WP-05）。

阶段内有三个不可并行的链，其余行按行号顺序执行即可：

- **引擎链** T009 → T010 → T011 → T012 → T013 → T014 → T015 → T016 → T017 → T018 / T019 → T020：同一文件（引擎），只能串行。
- **命令面链** T026 → T028 → T030 → T033 → T034：模板 → 技能 → 副本 → 镜像 → 既有测试。
- **清理链** T048 → T049 → T050 → T051 → T052 → T053 → T054 → T055 → T056 → T057 → T058 → T059 → T060：同一次 apply 的阶段顺序即此顺序，回退成本高于等待。

## Parallel Opportunities

- T002 / T003 / T004：三个基线各自写一个独立文件，互不读对方。
- T007 / T008：两份 owner 重写，各写各的文件；T006 的改名提交必须先落地。
- T027 / T032：模板与参考页分属两个目录。
- T036 / T037 / T038 / T044 / T045：五份互不相交的共享定义 / pattern / 成员声明。
- 其余行**不标 `[P]`**：它们要么共用文件、要么共用同一个镜像对、要么其证据文件是共享的追加型记录（追加竞争不是数据损坏，但会让两行的读数互相污染）。

## FR → 行 trace

每行列出引用该 FR 的全部任务行（DoD-1 的机械判据是行内出现该 id；本表是对应的可读索引）。

| FR | 行 |
|----|----|
| FR-001, FR-002, FR-007, FR-008 | T007 |
| FR-003, FR-004 | T008 |
| FR-005 | T008, T067 |
| FR-006 | T006 |
| FR-009 | T007, T036, T074 |
| FR-010 | T026, T030, T034 |
| FR-011, FR-012 | T026, T028 |
| FR-013 | T026, T030, T031, T033 |
| FR-014 | T040 |
| FR-015 | T017, T019, T023, T026, T028 |
| FR-016 | T023, T026, T044 |
| FR-017 | T017, T036, T043 |
| FR-018 | T078 |
| FR-019 | T027, T029, T030, T032, T034 |
| FR-020 | T027, T063 |
| FR-021 | T012, T027 |
| FR-022 | T029 |
| FR-023 | T017 |
| FR-024 | T008, T012 |
| FR-025 | T012 |
| FR-026 | T027, T032 |
| FR-027 | T018, T039, T072 |
| FR-028 | T009, T065 |
| FR-029 | T009, T021, T022, T024 |
| FR-030 | T007, T010 |
| FR-031 | T011, T021 |
| FR-032 | T012, T013 |
| FR-033 | T017, T021, T025 |
| FR-034 | T020 |
| FR-035 | T013, T048, T049 |
| FR-036, FR-037 | T048 |
| FR-038 | T050, T058 |
| FR-039, FR-040 | T014, T051 |
| FR-041 | T052 |
| FR-042 | T014, T051, T052 |
| FR-043 | T014, T015, T051, T052, T060, T068 |
| FR-044 | T015, T069 |
| FR-045 | T015, T019 |
| FR-046 | T016, T053, T057 |
| FR-047 | T016, T055, T056 |
| FR-048 | T016, T053, T057, T059 |
| FR-049 | T016, T054, T058, T059 |
| FR-050 | T035 |
| FR-051 | T036, T047 |
| FR-052 | T037 |
| FR-053 | T038 |
| FR-054 | T039, T046 |
| FR-055 | T040 |
| FR-056 | T041 |
| FR-057 | T031, T032, T042 |
| FR-058 | T022, T043, T047, T056 |
| FR-059 | T044 |
| FR-060 | T045, T046 |
| FR-061 | T002, T070 |
| FR-062 | T003, T061, T062 |
| FR-063 | T063 |
| FR-064 | T064, T071 |
| FR-065 | T061, T065 |
| FR-066 | T066, T071 |
| FR-067 | T067, T075 |
| FR-068 | T061, T068, T069 |
| FR-069 | T002, T070 |
| FR-070 | T072, T080 |
| FR-071 | T001, T003, T004, T005, T073, T076, T077, T079, T080, T081 |

## SC → 行 trace

| SC | Path | 传感器行 | 判据来源 |
|----|------|----------|----------|
| SC-001 | final | T067（模块）、T075（最终读数） | 活根计数为 0 + 注入转红；日期化根不计入 |
| SC-002 | final | T062、T063、T030 | 七模式 / 四模式 / 四个具名拒绝 / 删除模板即转红 |
| SC-003 | final | T048、T049、T059 | 逐条分类记录 + 锚点档行动级条目为 0 + 目标层各恰一份 |
| SC-004 | final | T051、T052、T070 | 逐条回执 + 摘要相等 + 删除为 0 + 受保护路径相等 |
| SC-005 | final | T059、T066 | 旧绑定键为 0 + 每个绑定可解析 + 每条处置记录 + 两处悬空已处置 |
| SC-006 | final | T065 | 定义写者唯一 + 两写者模拟 + 注入转红 |
| SC-007 | supporting | T060、T068、T069 | 第二次 apply 零 diff + 两处中断续做 |
| SC-008 | supporting | T031、T039、T040、T073 | 参考页 / 台账 / 探针面照常测；构建腿 `not-evaluated`（EP-006） |
| SC-009 | final | T070 | 受保护路径哈希集合与 `d7c9da7a3` 相等 |
| SC-010 | supporting | T074 | 基准读者复述记录，失败即不通过 |

## Guard ↔ 条款

`plan.md` § Testing Strategy 拥有 G-1…G-10 与测试路径的对应（本文件不复述其"转红条件"列）。行级对应：G-1 → T062、G-2 → T063、G-3 → T064、G-4 → T065、G-5 → T066、G-6 → T067 与 T075、G-7 → T068 与 T069、G-8 → T070、G-9 → T071、G-10 → T072。契约条款（C-1…C-49）与行的段级对应由各阶段的目的说明承担，不做逐条标签化（理由见 N-4）。

## Notes

- **N-1 `PLAN-EDIT: 101-005`（分类计数的转录偏差，已更正）**。`classification.json` 与 `research.md` §3 的记录是 **9 anchor / 3 action-goal / 2 obsolete**（action-goal 三条为 `088-speckit-visualization`、`091-auto-git-closeout`、`draw-diagram-interactive`），但五处文字写成"2 action-goal"：`plan.md` § Technical Context 的 `(9 / 2 / 2)`、`contracts/migration-cleanup.contract.md` C-44 的 P2 行 `action-goal migrations (2)`、`quickstart.md` S-5 的 Expected、`feature-ref.md` 的 SC-003 测量行、`.specify/features.md` 101 行。判为**更正**而非决定：录制意图只有一种读法（plan 阶段的 checkpoint 03 已声明"plan prose 被更正为 3/3"，但改动只落到了其中两处，其余是同一转录错误的副本），改动局部且可逆；五处已改，本行是声明。权威仍是 `classification.json` 与 `research.md` §3。
- **N-2 `PLAN-EDIT: 101-006`（消费者脚本路径不存在，已更正）**。`plan.md` § Source Code 树与 § Decomposition 的 WP-01 territory 把 `logical-framework.py` 与 `build-summary-input.py` 写成 `scripts/python/` 下的文件——该路径不存在。实测位置是 `skills/external/sdd-project-setup/scripts/logical-framework.py`、`skills/external/sdd-house-keeping/scripts/logical-framework.py`、`skills/internal/create-team/scripts/build-summary-input.py`，与 `contracts/goal-engine.contract.md` C-32 的消费者表一致。两处已按实测改正；任务行使用实测路径。
- **N-3 `PLAN-EDIT: 101-007`（团队域技能所在层，已更正）**。`plan.md` 的树与 WP-03 territory 把 `create-team` / `improve-team` / `run-team` / `summarize-project` 归到 `skills/external/`；实测四者均在 `skills/internal/`。两处已改正。与 WP-01 的 `skills/internal/create-team/scripts/build-summary-input.py` 由**文件级** territory 互斥（WP-01 只写该脚本，WP-03 只写四份 SKILL.md）。
- **N-4 不使用 `[green:]` 标签**。`templates/tasks-template.md` 允许零个标签订阅；本特性 49 条款若逐条标签化，会迫使行序按条款序号排列，与 plan 的工作包脊和依赖链冲突，并必然产生 `green-cross-phase` 警告。代价是失去"条款 → 行"的机械归属，故以 DoD-1 的 FR 级逐行引用 + § Guard ↔ 条款 的段级对应补偿；这是本阶段的一项取舍，不是遗漏。
- **N-5 非故事阶段划分**。`requirements.md` 的 US1…US6 是价值切分，`plan.md` 的 WP-01…WP-06 是施工切分；本文件按后者分阶段，因此行内不带 `[US]` 标签（校验器对非故事阶段的硬要求）。故事到判据的映射由 § SC → 行 trace 承担：US1（概念 / 语义）→ SC-001 / SC-010，US2（命令面）→ SC-002 / SC-008，US3（档案迁移与零丢失）→ SC-003 / SC-004 / SC-007，US4（绑定与团队处置）→ SC-005，US5（单写者与守卫）→ SC-006 / SC-009。
- **N-6 守卫后置下的红先**。plan 把守卫集中在 WP-05。对每个守卫，红先的实现形态是**注入检查**：临时制造它点名的缺陷、观察转红、还原、把读数写入 `notes/red-first-evidence.md`；"在无缺陷的树上跑绿"不作为红先证据。
- **N-7 文档站构建腿是 `not-evaluated`，不是通过**。EP-006 在特性前即为假（hugo 0.141.0 渲染 exit 1，`.Site.Language.Locale`），T073 只做复证与记录；把不可得读数写成通过，是 FR-071 明令禁止的行为。
- **N-8 工作树里已有的改动不入本特性**。实现入口存在一个与本特性无关的既存修改（`.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`），本阶段既不提交也不回退它；G-8 与 GATE-1 的对照面都按此口径读取。
