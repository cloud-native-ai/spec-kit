# 095 — Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）

**Feature ID**: 095
**Name**: Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）
**Description**: 把事实上的 super agent 归一为派发边上的相对逻辑角色：定义 owner、判定引擎、super↔sub 协议与身份转变注入、digest 角色视图与 harness 落点。
**Status**: Ready for Review
**Created**: 2026-11-10
**Last Updated**: 2026-11-25（clarify：绑定切片 106 background dispatch settlement；plan：切片 106 plan 集落盘，切片行 `Draft → Planned`；tasks：切片 106 任务清单落盘（37 行 / 5 故事 / 34 条款各被认领一次）；父状态保持 `Ready for Review` 不回退）

## Overview

框架里 super agent 事实上早已存在（交互 session、team 协调会话、SDD 驱动者、派发者），但只以「主 session / 编排者 / supervisor / driver / 派发方」等分散措辞出现：没有归一化定义、没有 super↔sub 协议、没有「身份转变时注入什么」的清单，也没有把并发、状态同步、状态跟踪与可视化接到同一张关系模型上。本特性把 super agent 正式定义为**派发边上的相对逻辑角色**（不是实体类型；同一执行体可在不同边上同时是 subagent 与 superagent），交付「定义 + 协议 + 身份转变注入清单 + 既有载体的投影接线」，并以三个真实形态验收：桌面端 Qoder 经 SSH 驱动远端 qodercli、本地 qodercli 编排一个 team、team 成员并发扇出 10 个 subagent 并自行汇总。本运行同时作为 080–094 机制实际效果的观测（FR-038）。

## Latest Review

- **2026-11-26 — `/speckit.review` slice 106 (run `r20261125T113505Z-106a`)** — Report: `.specify/specs/106-background-silent-failure/review.md`; code record: `.specify/specs/106-background-silent-failure/code-review.md`.
  - **Process segment**: pass with 1 P0 (repaired in-run), 2 P1 and 3 P2 findings — the P0: the slice's `Planned → Implemented` flip landed while `verification.md` was absent; the review materialized it from `test-evidence/verification-input.md` (nine SC rows + smoke triple) plus five `RS-NNN_joint_acceptance=` rows, and re-ran the ARC to `accept`. The two P0 rows carry the documented `(validated: direct re-read, subagent unavailable)` fallback.
  - **Artifact segment**: pass — coverage 10/10 after the repair (9/10 at review start; missing member `verification.md`); A2 P1 (quickstart S-1 command cannot block as written) and A3 P2 (EP-001 verdict-token enumeration under-inclusive) remain disclosed.
  - **Implementation segment**: pass — smoke `57 passed` exit 0 (evidence `.specify/specs/106-background-silent-failure/test-evidence/review-evidence.txt`), scope carries one P2 (stale `sdd-debt-governor` render refreshed by the prescribed render step), regression re-measured green (report byte-identical, engine + owner pins 35 passed, six settlement modules 100 passed).
  - **Code segment**: `not-evaluated` (receipt 331 changed / 49 judged / 282 legally skipped / 0 gap; skips earn no coverage credit) — 0 `blocking`, 2 `important` (each answered), 1 `suggestion`, 1 `nitpick`, 2 `praise`; merge gate `allow`.
  - **Acceptance Reality Check**: `final_path` record copied verbatim — pass 3 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 3; claimed status `Implemented`; ARC verdict `agree`; no fixed item.
  - **Status transition `Implemented → Ready for Review`: allowed** — the four conjunctive conditions hold; the registry row 106 and this entry carry the flip; the parent's own status is unchanged.

- **2026-11-10 — `/speckit.review` (run `r20261110T055657Z-b095-review`)** — Report: `.specify/specs/095-superagent-role/review.md`; code record: `.specify/specs/095-superagent-role/code-review.md`.
  - **Process segment**: `blocked` at the P0 level — 1 P0 (the implement stage never landed its owned `Planned → Implemented` transition although the closure checker returned `accept`), 3 P1 and 8 P2 findings; the P0 was confirmed by an independent read-only validator.
  - **Artifact segment**: `blocked` — coverage 11/11, no missing member; P1 findings: the digest contract C-1 "no carrier root may be read twice" clause is unimplemented and unguarded, the bound feature detail carries no `**Status**` field or `## Latest Review` section, and `verification.md` vs `tasks.md` disagree on the implement-stage status obligation.
  - **Implementation segment**: `blocked` — the delta carries 7 non-095 commits plus a user-ruling amendment (scope), and 18 existing guards are red from in-range commits (regression); the 095 packages themselves re-measure green (smoke `85 passed`, exit 0). Smoke triple: command from `verification.md`, exit 0, evidence `.specify/specs/095-superagent-role/test-evidence/smoke-six-modules.txt`.
  - **Code segment**: `blocked` — 2 `blocking` entries in the current record (18 red guards from the in-range digest redesign; the C-68 "no measurements" state removed with its guard weakened), 6 `important`, 5 `suggestion`, 1 `praise`; coverage receipt 313 changed / 13 judged / 300 skipped / 0 gap; client capture skipped (framework hat).
  - **Acceptance Reality Check**: `final_path` record copied verbatim — pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7; claimed status `Planned`; ARC verdict `agree`; no fixed item.
  - **Status transition `Implemented → Ready for Review`: refused (`blocking-unresolved`)** — the current code record carries 2 `blocking` entries (condition c); `deferred_tasks=T003` is unresolved and unwaived (condition a); and the claimed status was `Planned` because the implement-owned `Planned → Implemented` flip never landed, so the transition had no legal source state. No user waiver exists; the status was left unchanged at `Planned` at review time.
  - **Review-repair r1 (2026-11-10)**: the missed implement Feature Integration flip is landed — the registry row and this file now read `Implemented` (the four conjunctive conditions hold; `T003` resolved by archive-then-refreeze). The two `blocking` causes (in-range digest-redesign regressions and the dropped C-68 state) are repaired and re-measured green; the record still carrying the entries is superseded only by the next code-segment run, so a re-review is required before the transition is re-judged.

- **2026-11-10 — `/speckit.review` round 2 (run `r20261110T055657Z-b095-review-r2`)** — Report: `.specify/specs/095-superagent-role/review.md`; code record: `.specify/specs/095-superagent-role/code-review.md` (round-1 records archived as `review-r1.md` / `code-review-r1.md`).
  - **Process segment**: `pass` — 0 P0; 1 carried P1 (F3, line-scoped commit guard) and 8 P2; round-1's P0 (missed Feature Integration flip) and the two code `blocking` causes are verified fixed at their anchors; F7/F8 are disclosed as budget-deferred (FO-095-05 / FO-095-02).
  - **Artifact segment**: `pass` — coverage 11/11, no missing member; two P2 (SC-007 budget reconciliation; stale `Planned` literals in `tasks.md` / the checklist).
  - **Implementation segment**: `pass` — scope registered (`verification.md` § 跨线提交); regression re-measured green (smoke `85 passed`, exit 0; closure suite `216 failed / 8414 passed`, NEW = 3 environment/concurrency-owned names). Smoke triple: command from `verification.md`, exit 0, evidence `.specify/specs/095-superagent-role/test-evidence/review-r2-smoke.txt`.
  - **Code segment**: `pass` — 0 `blocking`, 6 `important` (each answered), 5 `suggestion`, 1 `praise`; coverage receipt 344 changed / 17 judged / 327 skipped / 0 gap; client capture skipped (framework hat).
  - **Acceptance Reality Check**: `final_path` record copied verbatim — pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7; claimed status `Implemented`; ARC verdict `agree`.
  - **Status transition `Implemented → Ready for Review`: allowed** — the four conjunctive conditions hold; the status is flipped on this file and `.specify/features.md` row 095.

## Key Changes（planned）

1. 新增定义 owner `shared/definitions/superagent-definitions.md`（[[STR-004]]）：角色定义、边谓词、深度、super↔sub 协议（下行 / 上行 / 分类 / 等待 / 尝试 / 授权 / 终止）、九项身份转变注入、状态同步与恢复映射、可视化映射、零第二机制边界、术语边界。
2. 新增独立只读角色-边判定引擎 `scripts/python/role-edge-check.py`（动作 `report` / `query`）：从既有载体（父侧派发记录、run report 映射表、状态脊 / line registry、artifact triplet）判定边、角色集（含 [[STR-002]]）、深度与四类封闭违例（self-dispatch / dangling-parent / unbacked-role-claim / depth-inconsistent）；零写点，契约测试在注入违例时转红。
3. `status-digest.py` 增加角色-边视图：身份、父边、角色集、深度、状态、age、stale、截断声明与 `nothing-running`；经引擎可导入接口一次物化（`read_carrier_inputs` + `evaluate_role_model`），不新建 parser / renderer / dashboard。
4. 派发面只加字段：`run-agent` 注入清单增加 [[STR-003]] 指针；team 派发与 driver 阶段派发携带父身份、子 label 与角色声明；driver 手册入口自检加一行指针。
5. harness 落点：`templates/instructions-template.md` 新增极小指针段（生成文件预算由 `scripts/bash/generate-instructions.sh` 判据）；`agent-definitions.md`、`subagent-definitions.md`、`framework-map.md` 各加指针行；`better-harness.md` 不改。
6. 收尾产出 080–094 机制观测附录：逐切片 `exercised`（可解析证据路径 + 可复现机器记录）或 `not-observed`，不以配置存在或「运行顺利」推断。

## Implementation Notes

- 实现按 `plan.md` § Work Packages 的 P1–P6 包推进；定义 owner 先行（阻塞全部用户故事），镜像按文件级 `sync-mirrors.py --only` 同步（基线 428 行 DIFF-class，只要求被触及的镜像对无 NEW drift）。
- 身份转变注入是派发载荷内的封闭九项指针清单；既有派发前自检按 `role-transition` 标识 + 九项 item-id 句柄逐项判定，缺任一即阻断（`data-model.md` § 7）。
- 违例集封闭四类；已授予派发职责由独立的 `dispatch_duty` 声明承载，不是 superagent 主张——已授权未派发不得被判违例；`dual-role` 只是角色集输出标记（引擎输出键 `role_set_marker`，`data-model.md` § 4/§ 5）、不作载体声明值。
- instructions 新增段 ≤600 B，超限时只允许缩为纯指针行，不抬预算（A7）；`test_fast_fail_discipline.py` 的 section-count pin 与模板段同提交升降。
- 测试执行唯一入口 `scripts/bash/run-tests.sh`；完成门判据是「相对 implement 起点基线零新增失败」（FR-036）。
- 本节其余实现细节随 `/speckit.implement` 落笔（按阶段落笔惯例）。

## Clarify Notes（2026-11-10，无人值守 clarify）

- **Feature Linkage**：`Related Feature` 绑定为新 Feature 095（同号惯例，索引 Draft + 本详情文件）；无既有 Feature 承载该主题，候选 019 / 027 / 085 / 093 的比较见规格 Clarifications。
- **10 条自行裁决**（详见 `requirements.md` § Clarifications · Session 2026-11-10（clarify 阶段））：判定入口 = 可执行只读引擎；协议分层逐项映射既有 owner（不复制字段表）；九项注入为封闭清单（可见性契约落 (f)、注意力预算落 (g)、驱动手册不进入载荷）；并发/状态同步/跟踪/可视化各归既有 owner，零新增投影面；instructions 新增极小指针段并接受 37,454 / 38,400 B 的实测余量约束；角色深度无上限与许可链深度 2 正交；观测读数必须是机器记录；out-of-scope 显式化；术语形态固定。
- **受影响 FR**：FR-003（父侧派发记录优先 + 冲突报错）、FR-004（两轴一句话落 owner）、FR-005（集合形态 + 引擎为唯一入口）、FR-017（封闭清单 + 红线）、FR-034（driver 手册入口指针）、FR-038（机器读数与反「顺利即有效」）；计数不变（38 FR / 10 SC）。
- **门读数**：flow-class 读取 `execution` / `source: declaration`；需求校验器与 overlap-check 读数见 `test-evidence/` 与状态脊。

## Related Specifications

- `.specify/specs/095-superagent-role/requirements.md`（本特性的需求规格；三个真实场景为定义输入）
- `.specify/specs/106-background-silent-failure/requirements.md`（**切片行 106**，`Draft`；2026-11-25 `/speckit.clarify` 绑定）：后台派发静默退出结算契约——修订本 Feature 拥有的 `superagent-definitions.md` § Termination（封闭结算值集合、每值正证据、`silent-end` / `unknown` 语义），并加性扩展 `role-edge-check.py` 为其唯一确定性结算判定面；父行状态保持 `Ready for Review`，不回退。
- `.specify/studies/dsh-superagent-prototype-study/docs/overview.md`（研读归档；授权链、能力分离、WorkerSlots、注意力预算、三层恢复、提示词不可越权）
- `.specify/shared/definitions/subagent-definitions.md`（子端 owner：三模态、并发义务、可见性契约、派发治理）
- `.specify/shared/definitions/agent-definitions.md`（Agent 三层分类法）
- `.specify/shared/guidelines/reporting-obligations.md`（汇报义务与 digest 契约）
- `.specify/shared/guidelines/fast-fail.md`（派发注入子句与异常行）
- `.specify/skills/sdd-loop-driver/references/watch-model.md`（等待 / 监听 / 归属层）
- **Related Features（邻域交叉引用；只在本文记录，不修改对方产物）**:
  - Feature 027 Team Management — team 席位编排；super agent 角色模型作用在其派发边上
  - Feature 085 SDD Temporary Goal/Team — SDD 临时 goal/team 与多 agent 并发；本特性引用其并发与席位事实
  - Feature 093 Concurrency by Default — 并发默认形态与派发能力；本特性的并发一问完全归其 owner

## Plan Notes（2026-11-10，plan 阶段）

- **判定面落点已固定**：新增独立只读引擎 `scripts/python/role-edge-check.py`（动作 `report` / `query`，零写点，`--help/--version` + 未声明选项拒绝），不并入 `line-registry.py` / `loop-state.py` / `status-digest.py`（两轴分离；决策张力 T-001）。
- **边记录形态**：`role-edge` 投影三载体 —— team 运行报告 `## Execution Detail` 的 `label | role | dispatch_duty | workspace | parent` 映射表、driver stage envelope sidecar 的 `role_edge` 七字段、`run-agent` 派发记录 + 三元组；违例四类封闭（self-dispatch / dangling-parent / unbacked-role-claim / depth-inconsistent）。
- **注入形态**：`role-transition` 九项为封闭指针清单，物理存在、由既有派发前自检按子串判定（决策张力 T-002）。
- **harness 落点**：instructions 模板新增 `## Super Agent (相对逻辑角色)` 段，目标 ≤600 B（实测余量 946 B），超限只允许缩为一纯指针行；`better-harness.md` 不改（clarify 裁定；brief 该行与之冲突，以需求为准）。
- **任务边界**：P1 定义 owner + 指针行 / P2 判定引擎 / P3 协议与注入接线 / P4 digest 角色视图 / P5 harness 落点 / P6 收尾（080–094 观测附录 + 既有测试处置），均 ≤16 任务。
- **镜象基线**：实测 428 条既有 drift、`.specify/shared/` 100 个既有脏文件（路径前缀改写，与本特性无关）；实现只按文件级 `--only` 同步被触及的对，其余脏文件不提交、不还原。

## Related Files

- Feature Index: `.specify/features.md`（095 行）
- Feature Detail: `.specify/features/095-superagent-role.md`（本文件）
- Specification: `.specify/specs/095-superagent-role/requirements.md`
- Plan / data-model / contracts / quickstart / feature-ref / tasks / checklists / observation-appendix: `.specify/specs/095-superagent-role/` 同名产物
- Owner page（implement 产物）: `shared/definitions/superagent-definitions.md`（运行时镜像 `.specify/shared/definitions/superagent-definitions.md`）
- Engine（implement 产物）: `scripts/python/role-edge-check.py`；digest: `scripts/python/status-digest.py`

## Status Criteria

- **Draft**: 规格已创建并完成 clarify。
- **Planned**（当前）: `plan.md`、`data-model.md`、`contracts/`、`quickstart.md` 存在，Constitution Check 无未论证 Fail。
- **Implemented**: 任务清零、每条 SC 有状态行、所有 `final` 路径 SC 为 pass、smoke 记录 pass。
- **Blocked**: 任务已关但至少一条 `final` 路径 SC 非 pass；或闭包判定 `block`。
- **Ready for Review**: review 证据齐、`code-review.md` 无 blocking、无未豁免的 `final` 路径非 pass。
- **Completed**: 人工 / 治理最终验收。

## Plan Notes — Slice 106（2026-11-25，plan 阶段）

- **设计落点**：结算契约的唯一 owner 仍是本 Feature 拥有的 `shared/definitions/superagent-definitions.md` § Termination（修订：封闭七值集合、每值正证据、反应义务、`settlement_version`/legacy、载体证据表、结算违例三 kind）；判定面复用 `scripts/python/role-edge-check.py` 的加性 `--action settle`，不新建第二引擎（A-6 保持成立）。
- **产物**：`.specify/specs/106-background-silent-failure/` 下 plan / research（14 B + 8 R）/ data-model（9 实体、12 不变量）/ 3 份契约（34 条款：C-01…C-12 结算、C-13…C-24 载体一致性、C-25…C-34 执行与迁移）/ quickstart（8 场景，逐例 premises + 钉住测试）/ feature-ref；门读数 pre-analyze `pass errors=0 advisories=20`、decision-tensions `0 error 0 warning`。
- **载体证据**：C1 四件套与 watcher 判定不变（sha 与 `fbab7a45c` 相等、self-test 39/0）；C2 加性 `.attempt`/`.end` + pid + TERM/INT/HUP trap，`.status` 行格式不变；C3 报告映射表加性 `end_state` + `evidence` 列与 `## Verification` 结算覆盖；C4 父侧尝试记录 + 期限/无返回规则；C5 显式排除并保留「未完成不得报成功」；C6 只允许合规 runner 后台形态或前台终结，含混 stall 表述按结算值逐项拆清。
- **披露的基线事实**：`scan-confirmation-gates.py` 冻结 `total == 27` 的相等判定测试在阶段基线即为红（实测 total 31），plan 以 EP-005 `falsified` + `fallback` 记录，本特性改判为「被触及文件的阻断命中数零新增」，不声称已冻结基线绿。
- **上游标识符纠正**：requirements 的载体编号由连字符形态改为 `C1`…`C6`，与框架契约条款语法（`C-NN`）分离；语义与 FR/SC 不变，requirements 校验器重跑 0 error / 0 warning，并已 append-only 记录在 `## Clarifications`。
- **注册裁决**：不新增 Feature、不新增 skill/command 单元、不新增 flow-class/probe 行；仅切片行 106 状态推进与本详情 plan note。

## Tasks Note — Slice 106（2026-11-25，tasks 阶段）

- **产物**：`.specify/specs/106-background-silent-failure/tasks.md` — 37 行依赖有序任务，按 5 个用户故事组织（US1/US2 P1 = MVP，US3/US4 P2，US5 P3），Foundational 承载 owner 章节修订；34 条款逐条被一行 `[green:]` 认领一次，认领行序与条款序号单调一致；Requirement Coverage Map 41/41。
- **门读数**：`validate-tasks.py` PASS（0 error / 0 warning / 34 green claims）；`pre-analyze-check.py --stage tasks` decision=pass errors=0 advisories=55（全部为 missing-path：50 条指向本阶段规划的新测试/夹具文件、1 条指向 quickstart teardown 临时目录、4 条为 plan 集既有引用）；`account-clause-coverage.py` claimed clauses 34、clause-uncovered beyond-baseline 0，`fr-uncovered` 37/41（FR-036 / FR-037 / FR-039 / FR-040 不被任何契约条款引用——如实报告，不作通过判据；FR 覆盖权威判据是本文件的 Requirement Coverage Map + runtime-stack-row errors=0）。
- **测试模式**：ON（Constitution Principle IV）；两处回归守卫按 migration/regression 例外置于实现之后（T023 保留面、T028 version/legacy），红能力由 T021 / T025 / T032 的演练读数证明。
- **冻结基线**：`coverage-baseline.txt` 已在生成时冻结（787 行，base-sha `1f06dceaf`）。
- **注册裁决**：切片行 106 维持 `Planned`（tasks 阶段无状态迁移权）；本 Feature 状态保持 `Ready for Review`，不回退。
