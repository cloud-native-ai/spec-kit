# Tasks: sdd-loop-driver 执行效率加固 —— 框架测试套件瘦身（Loop Efficiency Hardening）

**Requirement ID**: 067 (from branch `067-loop-efficiency-hardening`)
**Requirement Key**: `067-loop-efficiency-hardening`
**Related Feature**: Feature 058 无人值守 SDD 循环驱动机制（演化规格；状态保持 `Implemented`，不回退，不改注册表计数）
**Input**: Design documents from `.specify/specs/067-loop-efficiency-hardening/` — requirements.md（21 FR 定义 / 10 SC 定义，已 clarify）、plan.md（§Design by Workstream W1–W5 + §Implementation Slicing）、research.md（B-1…B-5 / R-1…R-10）、data-model.md（E1…E6）、contracts/ ×4（MP-01…MP-10 / LED-01…LED-08 / RC-01…RC-08 / FB-01…FB-09）、quickstart.md（S1…S7）、test-evidence/ 基线 dated 记录
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests Mode**: ON — 宪法 IV（Test-First & Contract-Driven）。本特性的交付物本身就是测试组织与测量，red→green 的落法由此特化：性能类任务的 red = 基线 dated 记录中的家族墙钟（全套件 750 s 或该家族基线时长，来源 `test-evidence/baseline-full-2026-10-22.md` 与 `test-evidence/baseline-durations-2026-10-22.txt`），green = 改动后同法定向复测落入 plan §W2 预期带并留 dated 证据；行为面沿用既有红测试与钉住（基线失败集权威 = FB-01 的 83 名清单），每次合并/折叠以 FB-08 注入演练 + FB-09 定位演练验证防护有效。任何任务 MUST NOT 把未运行的测试写成通过；预算达标主张只认 MP-08 证据。plan § Complexity Tracking 对 IV 的 ⚠ Partial 判定与辩护在本特性原样适用，此处只引用不复制。

**Tests**: 每个优化任务必须给出目标命令或 node id、预期 red→green（性能类 red = 基线 750 s 或该家族基线时长）、变更文件面与禁改面、证据落点。被删除或被合并的测试逐条入留证台账（FR-015 / LED-01…LED-03）；基线失败处置三选一（修复 / 登记 / 更新钉住，FB-05），禁止删测试消灭失败（FB-07）。全量运行只出现在两个槽位：T007（implement 起点，兼 RC-07 全局验证点）与 T034（closure 槽位，review 后、合并前）——槽位纪律由 GATE-6 机械审计。

**Organization**: 按 plan §Implementation Slicing 的 part 顺序 A→B→C→D→E→F 组织（每 part ≤8 任务），前置 Phase 1 T-Start（基线冻结与证据骨架），收口拆为 Phase 8（review 前置，implement 期收尾）与 Phase 9（closure 槽位验收，review 后、合并前执行）。E 组内部是关键路径：套件先落（T019）→ 同步修复（T023）→ 转绿核对（T024）；W1 据此拆为 Class 1（E 组，机制侧同步修复）与 Class 2（F 组，逐名 triage）两段执行，分组覆盖完整对应派发 brief 的 T-Start / W1 / W2 / W3 / W4 / W5 / 收口 各组（映射与裁决记录见 `notes/tasks-assumptions-2026-10-22.md`）。

**Plan constraint**: plan U4 已于提交 `bca3bc99` 通过。本文件只消费 plan §Implementation Slicing / §Design by Workstream / §W5 与四份契约，按 § 引用、不复制其表格。implement 期如需改动 plan-owned 产物，MUST 带 `PLAN-EDIT:` 声明，或停为 `ANOMALY:` 上报。

## Requirements Coverage（每条 FR/SC 至少一个任务行承载；归属依据 = plan § Requirements Coverage）

- **FR-001…FR-004、FR-006…FR-009**（US1–US4 派发机制面）：机制 owner = 063 已落地面，本特性 implement 以其纪律自应用执行——part brief 与预算（驱动者派发面）、分段写文件、显式豁免、dispatch log、微缺口并流、预授权边界；本阶段的任务级证据载体 = T032 / T038 的 dispatch log 转录与 verification 记录（SC-001…SC-005 证据，不可得记 `not_evaluated`），不新增机制任务。
- **FR-005**（定向集 + 两槽位）→ T007 / T034 两个全量槽位，其余任务全部定向集。**FR-010**（owner 面引用性更新）→ T030。
- **FR-011**（完整运行构成）→ T007 / T034（MP-05 有效性判据）+ Notes 红线。**FR-012**（墙钟与测量）→ T007 / T034（MP-02 / E1 / MP-08）。**FR-013**（运行器契约）→ Notes 红线 + T030（如确需改动走镜像义务）。
- **FR-014**（表驱动合并）→ T005 / T019–T022。**FR-015**（台账留证）→ T002（骨架）/ T004 / T020–T022（逐行）/ T035（审计）。**FR-016**（夹具复用不换语义）→ T004 / T005 / T008 / T010 / T011 / T013 / T015–T017。
- **FR-017**（并行或等价加速）→ Notes（xdist 不采用；等价加速 = W2 各任务合计，R-7）。**FR-018**（钉住不削弱）→ T002（名册）/ T019–T020（LED-07）/ T023（负债登记）/ T025（更新钉住须记理由）/ T036（名册 ⊆ post）。
- **FR-019**（依赖边界）→ T037。**FR-020**（失败定位）→ T019（参数 id）/ T022（复测）/ T028（FB-09 演练）。**FR-021**（交付面）→ Path Conventions 禁改面 + T030。
- **SC-001…SC-005** → T032 / T038（dispatch log 证据）。**SC-006** → T034。**SC-007** → T001 / T033 / T035。**SC-008** → T002 / T023 / T025–T027 / T029 / T036（演练面见 T028）。**SC-009** → T028。**SC-010** → T037。

## Definition of Done (DoD)

- DoD-1: 全部任务行闭合（无 `[ ]` / `[>]` 残留），每个优化任务的 dated 证据落在 `.specify/specs/067-loop-efficiency-hardening/test-evidence/`（台账、计时、差集、演练记录各归其位）。
- DoD-2: E4 双清单齐备（`test-evidence/baseline-test-ids.txt` 与同法再生的 post 清单），LED-05 join 审计 unmatched = 0（SC-007）。
- DoD-3: FB-04 名称级差集为空（两侧同 15 条在册红：14 debt + i11）、钉住名册按 W-1 台账 join 执行（每 id 在 post 或映射到绿色套件参数）、83 名 triage 表按 V-E5-1…V-E5-3 闭环（SC-008）。
- DoD-4: FB-08 注入演练 + FB-09 定位演练记录落档且注入已还原（SC-008 / SC-009）。
- DoD-5: closure 槽位 MP-02 测量的 E1 全字段 dated 记录存在；wall ≤600 s，或 RC-04 显式升级记录在案（SC-006）。
- DoD-6: SC-010 三项检索全过（运行时依赖 diff 为空 / 测试侧新增依赖仅在开发组 / 新增网络调用为 0）。
- DoD-7: `verification.md` 记录哪些测试跑了、哪些未跑、waiver 原文（如有）；SC-001…SC-010 逐项有状态与证据指针；不可得指标记 `not_evaluated`。

**DoD Status**: pending（tasks 阶段产物；implement 闭合后按 GATE-1…GATE-7 复核翻转）

## Completion Gate

- GATE-1: 零 NEW 名称级失败 — check: 从 T034 closure 运行日志提取 post FAILED 名（FB-04 等价形态，剥离 `FAILED ` 前缀、排序），`comm -13 test-evidence/baseline-failures-2026-10-22.txt <post-names>` 输出为空。
- GATE-2: 覆盖审计零静默删除 — check: LED-05 inline join（`comm -23` 基线/post id 清单 → 逐 id 对账台账）报告 unmatched = 0，过程与输出落 coverage-audit dated 记录。
- GATE-3: 无未闭合任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/067-loop-efficiency-hardening/tasks.md` 返回 0。
- GATE-4: 达标测量证据存在 — check: closure E1 记录文件 `test -e` 通过，且其 `wall_seconds` ≤600 或同文件含 RC-04 升级段。
- GATE-5: 结构校验器通过 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/067-loop-efficiency-hardening/tasks.md` 退出 0；`python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/067-loop-efficiency-hardening --stage tasks --repo .` decision=pass；`python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/067-loop-efficiency-hardening/requirements.md --tasks .specify/specs/067-loop-efficiency-hardening/tasks.md` decision=proceed。
- GATE-6: 两槽位纪律 — check: `python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine "$STATE_SPINE" --spec-dir .specify/specs/067-loop-efficiency-hardening --stage-check closure` 退出 0 且报告 `baseline:1 closure:1`（`$STATE_SPINE` = 驱动 U0 入口声明的状态脊路径；063 E2 槽位台账唯一来源 = 状态脊 `<!-- test-budget -->` 围栏，同 063 I-05 语义）。
- GATE-7: 镜像义务 — check: 对本特性触碰过的镜像对执行 `python3 scripts/python/sync-mirrors.py --check --only <pair>` 退出 0，且全仓 `--check` 相对实施前读数零 NEW drift；未触碰镜像面则在 `verification.md` 显式记录「未触碰」。

## Environment Prerequisites

- **python + pytest（仅经规范运行器）**: available — probe: `test-evidence/plan-probes-2026-10-22.md` P-1 @ 2026-10-22（运行器解析 PATH python 3.14.6 + pytest 9.1.1；仓库 `.venv/bin/python` 无 pytest，裸 `python3 -m pytest` 本机不可用）；affected: T001/T006/T007/T012/T014/T018/T022/T024/T033/T034（see § Environment Prerequisites）。
- **bash + git**: available — probe: `git rev-parse --abbrev-ref HEAD` @ 2026-10-22 → `067-loop-efficiency-hardening`；affected: 全部 fixture 仓类任务与 RC-07（see § Environment Prerequisites）。
- **宿主全局 `core.hooksPath` 安全扫描钩子**: present — probe: plan-probes P-4 @ 2026-10-22（每次 fixture 提交 ≈0.9 s 钩子税）；affected: T003/T007/T008–T012 的预期节省带；若宿主钩子在实施期已移除，RC-07 仍然正确，回收幅度按实测记录（see § Environment Prerequisites）。
- **网络 / 新依赖**: not required — 本特性零新增运行时或开发依赖（FR-019 / RC-08；xdist 准入不采用，R-7）；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行（不同写目标、无未满足依赖；仅 Phase 1/3/5 内标注的行）。
- **[Story]**: 仅 User Story 阶段内的行携带；本特性 implement 面集中在 User Story 5（框架测试套件瘦身），Phase 8–9 为非 story 收口阶段，不带 story 标签。
- **[blockedBy: T001]**（示例用真实 id）: 显式依赖；所列行未闭合前不得开工；无标签的行按阶段顺序执行。
- 每行一条任务（含路径、命令、验收、证据落点），仓库相对路径；red 记录按 063 惯例落 `notes/`，测量/审计类证据一律落 `test-evidence/`（dated，一文一件）。
- 不使用 `[green:]` 标签：本特性契约条款（MP/LED/RC/FB）由收口审计与既有契约测试承载（plan § Constitution Check IV），条款→任务映射在各任务行内以条款 id 显式引用。
- 证据文件名中的 `〈date〉` 沿用 plan §W5 的 dated 占位写法，实施时以实际 ISO 日期落盘。

### Task State Sigil (REQUIRED)

- `- [ ]` open; `- [>]` claimed/in-progress; `- [X]` closed; `- [~]` deferred with a recorded reason.

## Path Conventions

- 交付面（RC-06 / FR-021）：`tests/`（用例、夹具、conftest）、`scripts/bash/run-tests.sh`（预期零改动）、`pyproject.toml`（仅开发依赖组，预期零新增）、本 spec 目录 `test-evidence/` 与 `verification.md`。
- 禁改面（全部任务通用）：`src/specify_cli/` 运行时行为（FR-021）；`scripts/python/` 引擎语义——镜像修复走引擎调用、测试进程内直调走 importlib 载入，都不改引擎（plan § Assumptions：引擎疑有缺陷按 Fast Fail 上升）；宿主 git 配置；`templates/`；注册表（`.specify/memory/features*`、`register.md`、`glossary.md`）；`requirements.md` / `plan.md`（无 `PLAN-EDIT:` 不改）。
- 镜像对（plan § Mirror Obligations）：`scripts/bash/run-tests.sh` ↔ `.specify/scripts/bash/`、`skills/external/sdd-loop-driver/` ↔ `.specify/skills/sdd-loop-driver/`（引擎 `--write --only` 同步，禁止手改镜像）；`tests/**` 与 `pyproject.toml` 开发组不在镜像对内。

## Notes（红线与既定裁决；各任务行不重复展开，冲突时以本节 + 契约为准）

- 禁止以删除或合并掉失败测试的方式处置基线失败（FB-07）；台账行描述重组、不处置失败（FR-015）。
- 债务记录永不声称 green（FB-06）；本范围不得成为任何钉住测试失败的原因（FR-018）。
- xdist 裁决 = 准入、本 spec 不采用（research R-7 / RC-03 / FR-017 等价加速分支由 W2 手段合计承载）；固定测量命令保持串行；closure 超 600 s 走 RC-04 显式升级，禁止静默改命令、子集运行或降层（FR-011）。
- 运行器契约零改动（RC-01 / RC-02 / FR-013）；如实施确需诊断性标记，标记必须构成中立（RC-05 / MP-10）并触发 T030 镜像同步。
- 全量运行仅 T007（implement 起点）与 T034（closure）两个槽位（FR-005 / FR-012），其余一律定向集。
- 本文件不声称任何测试通过；所有 green 均为 implement 期须实际达成并留证的预期；复测超带时如实记录并归因，不虚报达标。
- 分组与裁决性假设（part 任务数与 plan 预估的偏差、W1 拆两段的依赖依据、closure 取名单形态等）记录在 `notes/tasks-assumptions-2026-10-22.md`。
- 符号消歧（CHK012 纠正，2026-10-22）：本文件中的「data-model §E2」= ConsolidationLedger 台账行；「063-E2 槽位行」= 状态脊 `<!-- test-budget -->` 围栏的 test-budget 槽位台账（063 efficiency-model §E2）。两者不得互换写入位置。
- 测试预算裁定（M-1 处置，2026-10-22）：pre-stage 750 s 全量 = implement 外的诊断基线，不占槽位；T007 = 本线 implement 起点槽位（必须 `--names-out` 捕获 in-stage 基线失败名）；T034 = closure 槽位；implement 内全量恰两次，无第三槽位。closure 名称级差集以 T007 的 in-stage 清单为权威，pre-stage 83 名作范围对照。
- 计数锚点（M-2 处置，2026-10-22）：基线 accounted = 83 + 4467 + 1 = 4551；缓存 nodeids = 4553；T001 以三数对账并在文件头解释差异，不再以任一单数为停机锚点。admission 家族 red 锚点以 durations 合计 87.45 s 为准（早期 82.5 s 为局部口径，已弃用）。

---

## Phase 1: User Story 5 — T-Start 基线冻结与证据骨架

**Purpose**: 在任何合并类任务开工前冻结基线 id 清单（E4），并建立台账、triage、钉住名册三件证据骨架；后续一切折叠/同步/triage 都有落账位置。

- [X] T001 [P] [US5] 生成基线测试 id 清单（E4）：`bash scripts/bash/run-tests.sh --collect-only -q`（经运行器参数透传到 pytest；把解析到的解释器写入文件头，plan-probes P-1 实测解析 PATH python 3.14.6 + pytest 9.1.1），剔除 `# test runner:` 头行与末尾汇总行后一行一条，写入 `test-evidence/baseline-test-ids.txt`（头部记录生成命令、日期、解释器）；验收：文件存在、每行一个合法 node id；文件头记录三数对账——runner 收集数、基线 accounted 4551（83 failed + 4467 passed + 1 skipped）、缓存 nodeids 4553——差异逐条解释（如缓存残留 id）；未解释的实质偏差即停并以 `ANOMALY:` 上报，不带偏差继续。时点 = 本阶段首个任务、先于一切合并类改动（requirements § Measurement Sources 定案时点）。证据落点：该文件本身。禁改面：无（只读收集）。
- [X] T002 [P] [US5] 建立证据骨架三件：(a) `test-evidence/test-consolidation-ledger.md` 台账骨架（data-model §E2 ConsolidationLedger 行字段：original_id / disposition（deleted|case-merge|file-merge|retained）/ retained_equivalent_id / equivalence_rationale / date / commit；头注声明 LED-01…LED-03 的追加式纪律与封闭处置词表）；(b) `test-evidence/failure-triage-2026-10-22.md` triage 表骨架（E5 字段：original node id / class（mirror-sync|stale-pin|regression|pre-existing-debt）/ disposition（synced|pin-updated+rationale|mechanism-fixed|debt-registered）/ evidence 指针 / date / commit，另设 FB-06 负债记录索引节）；(c) `test-evidence/pinned-roster-2026-10-22.txt` 钉住名册：按 FR-018 / FB-03 类目（镜像 byte-identity、节集合钉住、宪法双落地 watchlist、确认门准则 SHA 钉住、fast-fail 契约）从 `tests/contract/` 盘点全部钉住测试 node id，一行一条。验收：三文件存在、字段与 data-model E2/E5 一致。证据落点：三文件本身。

**Checkpoint**: 基线 id 清单与三件证据骨架就位；后续合并 / 同步 / triage 均有落账位置与名册基线。

---

## Phase 2: User Story 5 — Part A · RC-07 钩子中和与 admission_check 提速（plan §Implementation Slicing A；W2 行 1）

**Purpose**: 落地收益最大、风险最低的一组：单点中和宿主 git 钩子税（全局受益），admission_check 家族进程内直调与夹具共享，随后用 implement 起点全量槽位验证全局宽尾回收。

- [X] T003 [US5] [blockedBy: T001] RC-07 钩子中和 autouse fixture：在 `tests/conftest.py` 增加单点 autouse fixture，把 `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` 指向空临时文件（仅测试进程树生效；不改任何断言；不动宿主 git 配置；可回退 = 删除该 fixture 即恢复原行为）。目标命令：`bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q --durations=0`。预期 red→green：red = 该家族基线 ≈87.45 s（18 条 durations 合计，`test-evidence/baseline-durations-2026-10-22.txt`）；green = 家族合计显著下降（本任务只收钩子税份额，不单独设达标带）。风险处置：个别用例依赖全局 git config → 按 RC-07 收窄覆盖范围（逐用例 env 豁免清单），不得整体放弃中和。证据落点：`test-evidence/rc07-neutralization-〈date〉.md`（前后 targeted 计时与差异）。禁改面：`scripts/`、`src/`、宿主 git 配置。
- [X] T004 [US5] [blockedBy: T002,T003] admission_check 引擎进程内直调 + CLI 钉住保留（research R-2）：改 `tests/unit/test_admission_check.py` — importlib 载入 `skills/external/sdd-loop-driver/scripts/admission-check.py` 直调其入口（套件既有模式），消除逐用例子进程冷启动；保留 ≥1 条真 CLI 子进程用例钉住 exit code / argv 契约面（`test_exit_codes_0_1_2` 的 0/1/2 退出码语义不得丢失）；用例间显式重置引擎模块全局态（FR-016 隔离语义不变）。目标 node id：该文件 18 条慢用例（基线 3.08–8.32 s/条，durations dated 记录）。预期 red→green：red = 家族基线 ≈87.45 s；green = 家族 ≤25 s（plan §W2 带 15–25 s；实测落带即记，超带如实归因记录，不虚报）。台账：被合并/改写用例逐条 case-merge 或 retained 行（入 T002 骨架）。禁改面：admission-check.py 引擎本身。证据落点：T006 timing 记录 + 台账行。
- [X] T005 [US5] [blockedBy: T004] admission_check 同形夹具共享 + 矩阵表驱动扩展（research R-3 / R-4）：仍改 `tests/unit/test_admission_check.py` — 模块级 base 仓 fixture（完成基线提交后冻结），每用例从 base 克隆（写时复制语义），替代逐用例建仓 + 2–3 次 git commit；`test_task_count_boundary_edges` 的参数化模式扩展到同形 sibling 行（每行断言保留、行编码 parametrize id 保留，FR-014 / FR-020）。目标面：18 条慢用例的夹具准备相（setup）。预期 red→green：随 T006 复测合并评估（家族带 15–25 s）。台账：矩阵扩展若有用例合并 → 逐条 case-merge 行。禁改面：同 T004。证据落点：T006 timing 记录 + 台账行。
- [X] T006 [US5] [blockedBy: T005] admission 家族定向复测与留证：运行 `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q --durations=0`，记录家族合计与逐条 call 时长；对照基线 ≈87.45 s 与预期带 15–25 s；核对 ≥1 条 CLI 子进程钉住用例仍在且断言语义不变；核对台账行（原 18 条 id 与新形态一一对应或注明 retained）。证据落点：`test-evidence/w2-admission-timing-〈date〉.md`（命令、输出节选、前后对照表）。超带处置：家族仍 >25 s 时按 plan §W2 假设表逐项归因并记录，不虚报达标、不追加全量运行。
- [X] T007 [US5] [blockedBy: T006] implement 起点全量槽位（RC-07 全局宽尾验证点）：按 `contracts/measurement.md` MP-02 逐字组合执行（冷缓存清 `.pytest_cache` 与 `tests/`、`src/` 下 `__pycache__` 后单次完整运行；epoch 包装墙钟（MP-04）；tee 日志；至多一次 warm-up 且先于清理（MP-03））；按 MP-06 记 E1 全字段（data-model.md E1）到 `test-evidence/full-run-〈date〉-implement-start.md`，`baseline_pointer` = `test-evidence/baseline-full-2026-10-22.md`。有效性判据（MP-05）：单次调用、三层全执行、无过滤器、deselected=0。对照：基线 750 s vs 本次墙钟，记录宽尾回收量（plan §W2 预期 ≈40–70 s 量级，仅作过程记录，不构成 SC-006 达标主张——MP-08）。两槽位纪律：此为 implement 起点槽位；运行必须带 `--names-out test-evidence/baseline-failures-<date>-implement-start.txt`（063 TB-03 基线捕获）；该清单是 closure 名称级差集的权威基线，pre-stage 83 名清单只作范围对照。同时把槽位写为状态脊 `<!-- test-budget -->` 围栏 063-E2 槽位行（slot=baseline，`$STATE_SPINE` 同 U0 入口声明，SPINE_WRITE_MODE=direct，063 纪律）。本轮是本线 implement 起点槽位；pre-stage 750 s 全量是 implement 外的诊断基线，不占槽位。

**Checkpoint**: RC-07 中和生效且全局可见；admission 家族落带；implement 起点槽位已消耗并有 E1 记录与状态脊 063-E2 槽位行。

---

## Phase 3: User Story 5 — Part B · 次慢家族夹具复用（plan §Implementation Slicing B；W2 行 2、5）

**Purpose**: 对 worktree queue、workspace isolation、store-state、audit_plan_changes、loop_state 五个次慢面做夹具复用与 fsck 收敛；断言与隔离语义一概不变，收益依赖 T003 的 RC-07 基建。

- [X] T008 [P] [US5] [blockedBy: T007] worktree queue 家族：改 `tests/integration/test_worktree_integration_queue.py`（基线 6 条 ≈53.8 s，单条 merge+replay 27.13 s）— 模块级 base 仓 + 每用例廉价克隆；fsck 从逐次收敛到终局一次（断言不变）；replay-identical 断言逐字节保持（FR-016 / FR-014）；核对 RC-07 env 经引擎子进程继承生效。目标 node id：`test_integration_executor_merges_queue_and_replay_is_identical`（基线 27.13 s）等 6 条。预期 red→green：red = 家族基线 ≈53.8 s；green = 12–18 s 带（plan §W2）。台账行（若有合并）随 T012 回填核对。禁改面：integration executor 脚本语义。
- [X] T009 [P] [US5] [blockedBy: T007] workspace isolation 家族：改 `tests/contract/test_workspace_isolation_contract.py`（基线 3 条 ≈13.5 s）— 先核对 RC-07（T003）已覆盖钩子税份额；如仍有逐用例仓重建成本 → 模块级仓 + 克隆；隔离断言不弱化（FR-016）。目标 node id：`test_p0_merged_requires_real_head_containment`（基线 6.19 s）等 3 条。预期 red→green：red = ≈13.5 s；green = 5–6 s 带。证据随 T012。
- [X] T010 [P] [US5] [blockedBy: T007] store-state 两分支合并夹具复用：改 `tests/contract/test_store_state_protocol.py` 的 TestTwoBranchMerge（基线单条 8.92 s）— 两分支 fixture 改模块级 base 仓 + 克隆；`test_branch_merge_yields_zero_conflicts_and_both_entries` 的零冲突与双条目断言逐字保持。预期 red→green：red = 8.92 s；green = ≤4 s。证据随 T012。
- [X] T011 [P] [US5] [blockedBy: T007] audit_plan_changes 与 loop_state 夹具复用：改 `tests/unit/test_audit_plan_changes.py`（基线 5.22 s + 4.41 s 两条）与 `tests/unit/test_loop_state_engine.py`（慢条 4.72 s / 3.53 s）— 多提交序列抽共享 fixture、提交次数收敛；loop-state 3 条基线失败用例本任务只动夹具不碰断言（其失败处置归 T027 triage，夹具改动不得成为失败原因）。预期 red→green：red = 两文件家族基线合计 ≈13 s；green = ≤5 s。证据随 T012。
- [X] T012 [US5] [blockedBy: T008,T009,T010,T011] Part B 定向复测与台账回填：逐家族 `bash scripts/bash/run-tests.sh <家族文件> -q --durations=0`，对照基线与 plan §W2 预期带；台账行核对（case-merge / retained 齐备、原 id 可追踪）；五家族前后时长对照表落 `test-evidence/w2-partb-timing-〈date〉.md`。超带处置同 T006（归因记录，不虚报、不追加全量）。

**Checkpoint**: 次慢家族落带；夹具复用未改变任何断言对象与隔离语义；台账行齐备。

---

## Phase 4: User Story 5 — Part C · trigger telemetry 进程内动作化（plan §Implementation Slicing C；W2 行 3）

**Purpose**: 把 60+ 次引擎子进程冷启动的 telemetry 循环改为进程内直调，同时钉住 CLI 契约面，保证子进程与进程内语义一致。

- [x] T013 [US5] [blockedBy: T007] trigger telemetry 进程内动作化 + CLI 冒烟钉住（research R-2）：改 `tests/integration/test_trigger_telemetry.py`（基线 3 条 ≈19.9 s；sixty-turns 用例循环 60+ 次引擎子进程，每次解释器冷启动 ≈55 ms 起，plan-probes P-3）— importlib 载入 `scripts/python/trigger-utils.py` 直调 action（套件既有模式），动作间显式状态重置（模块级全局态以重置 helper 隔离，FR-016）；保留 ≥1 条 CLI 子进程冒烟用例钉住 payload / 退出码语义（子进程↔进程内一致性由此钉住，FR-020）。目标 node id：`test_sixty_turns_then_rotate_keeps_at_most_the_window`（基线 6.31 s）、`test_row_count_never_exceeds_the_window`（6.22 s）、`test_rotation_loses_no_rule_state`（7.39 s）。预期 red→green：red = ≈19.9 s；green = 4–6 s 带。禁改面：trigger-utils.py 引擎。证据随 T014。
- [x] T014 [US5] [blockedBy: T013] Part C 定向复测与台账回填：`bash scripts/bash/run-tests.sh tests/integration/test_trigger_telemetry.py -q --durations=0` 记录逐条时长；CLI 冒烟钉住核对（子进程用例仍真实起进程）；台账行核对；落 `test-evidence/w2-telemetry-timing-〈date〉.md`。超带处置同 T006。

**Checkpoint**: telemetry 家族落带；CLI 契约面钉住保留；进程内全局态无跨用例泄漏证据。

---

## Phase 5: User Story 5 — Part D · 模板快照 + 写时克隆夹具（plan §Implementation Slicing D；W2 行 4）

**Purpose**: 用 session 级只读模板快照 + 每用例写时克隆替代逐用例 copytree；平台回退必须实现且行为中性；生成器契约面保持子进程。

- [x] T015 [US5] [blockedBy: T007] session 级模板只读快照 + 每用例写时克隆 fixture：在 `tests/conftest.py`（与 RC-07 同一处，plan § Scale/Scope「conftest 一处」）增 session 级只读模板快照 fixture 与每用例克隆 helper — macOS APFS `clonefile` 优先、普通 copy 回退（平台相关回退必须实现且行为中性，plan §W2 行 4）；每用例独立克隆保持 c9 幂等断言的裸起点语义（FR-016，跨用例零污染）。目标面：`tests/contract/test_proactive_trigger_section.py` 与 `tests/contract/test_instructions_size_budget.py` 的逐用例模板树安装。验收：fixture 自证（克隆树与快照 byte 一致、两次连续克隆互不影响）。证据随 T018。
- [x] T016 [P] [US5] [blockedBy: T015] proactive trigger 家族接入快照克隆：改 `tests/contract/test_proactive_trigger_section.py`（基线 4 条 ≈17.6 s）接入 T015 夹具（模板树安装从逐用例 copytree 改为克隆）；生成器保持子进程执行（契约面不进程内化，plan §W2 行 4）。目标 node id：`test_c9_section_propagates_and_is_idempotent`（基线 7.30 s，幂等断言跑两次生成）等 4 条。预期 red→green：red = ≈17.6 s；green = 与 T017 合计 10–12 s 带。台账行随 T018。
- [x] T017 [P] [US5] [blockedBy: T015] instructions size budget 幂等用例接入：改 `tests/contract/test_instructions_size_budget.py` 的 `test_report_is_idempotent`（基线单条 6.98 s）接入 T015 夹具；两次生成器运行的幂等断言保持。预期 red→green：与 T016 合并评估（合计带 10–12 s）。台账行随 T018。
- [x] T018 [US5] [blockedBy: T016,T017] Part D 定向复测与台账回填：`bash scripts/bash/run-tests.sh tests/contract/test_proactive_trigger_section.py tests/contract/test_instructions_size_budget.py -q --durations=0`；对照基线合计 ≈24.6 s 与 10–12 s 带；核对跨用例无污染（c9 裸起点语义）；台账行核对；落 `test-evidence/w2-partd-timing-〈date〉.md`（含平台回退路径的实测记录）。

**Checkpoint**: 快照克隆夹具落地；proactive / instructions 家族落带；平台回退路径有证据。

---

## Phase 6: User Story 5 — Part E · W3 镜像一致性套件 + W1 Class 1 同步修复（plan §Implementation Slicing E；关键路径 套件→同步→转绿）

**Purpose**: 以同步引擎 pair 清单为表源建共享参数化套件（表源唯一 owner = 引擎），折叠纯 byte-identity 函数并逐条入台账；随后机制侧修复镜像漂移，让套件与既有镜像测试由基线红转绿。

- [X] T019 [US5] [blockedBy: T007] 共享参数化镜像一致性套件（W3 主件，FR-014 / FR-018）：新建 `tests/contract/test_mirror_parity_suite.py` — 参数表源 = importlib 载入 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 与文件枚举 helper（不复制 pair 清单，One Source of Truth / Tool Reuse，引擎新增对自动入列）；断言语义 = 引擎 `--check` 的同一比对（`compare_pair` 等价的逐对字节一致断言，drift 即失败）；parametrize id 携带 源路径→镜像路径（FR-020 可定位）；覆盖引擎清单全部文件对——相对现状散落的 44 个纯 byte-identity 候选只可能更严；引擎非 strict 例外对保持引擎语义、不额外放宽。预期 red→green：对当前漂移对套件行 red（真实漂移，50 条镜像类基线失败为证）——此 red 是 SC-008 相对语义的输入，由 T023 同步后转绿，禁止在本任务内消灭。禁改面：sync-mirrors.py 引擎语义。证据落点：套件文件本身；折叠台账自 T020 起逐行引用套件参数 id。
- [X] T020 [US5] [blockedBy: T002,T019] 纯 byte-identity 函数折叠 · 批 1（P-5 盘点 44 个候选按文件路径字典序前 1/3，逐函数核对）：仅折叠「纯字节比对」函数；带额外断言（节集合 / 计数 / wiring / 归一化等价）的用例保留其额外断言所在用例，只折叠冗余字节比对部分（plan §W3 折叠纪律）；每被移除函数一行台账（case-merge，retained_equivalent_id = 套件对应参数 id，等价依据 = 字节断言由引擎驱动套件等价承载，LED-04）；钉住强度核对（LED-07：钉住字面量与强度不降，FR-018）。目标面：`tests/contract/` 批 1 文件集（按 P-5 清单机械切分，逐函数核对于台账注记）。验收：批 1 文件 targeted 运行仅剩预期形态（额外断言用例 + 套件）。
- [X] T021 [US5] [blockedBy: T020] 折叠 · 批 2（P-5 清单字典序次 1/3）：同 T020 全部纪律（逐函数核对、额外断言保留、逐行台账、LED-07 核对）。验收同 T020。
- [X] T022 [US5] [blockedBy: T021] 折叠 · 批 3（P-5 清单余量）+ 折叠面定向复测：余量函数同纪律折叠（44 为候选上限，据实入台账；决定少折叠某函数须在台账注记原因）；随后 `bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py <批 1–3 触碰文件> -q` 定向复测——失败形态全部可定位到参数行（FR-020）；台账行总数与被移除函数数一致。证据落点：台账 + 复测输出贴入 `test-evidence/w3-fold-recheck-〈date〉.md`。
- [X] T023 [US5] [blockedBy: T019] W1 Class 1 镜像漂移同步修复（FB-05 第 1 类，机制侧，测试零改动）：先 `python3 scripts/python/sync-mirrors.py --check` 盘点漂移对；对可同步对执行 `python3 scripts/python/sync-mirrors.py --write --only <pair>` 修复；canonical 源正被其他在途特性改动的对不盲同步 → FB-06 dated 负债登记（注明非本范围引入）；同步同时把 50 条镜像类基线失败逐名写入 triage 表（class=mirror-sync；disposition=synced 或 debt-registered；V-E5-3 要求行内记 sync 命令与 pair 范围）。验收：可同步对本对 `--check` 归零；负债对有 dated 记录。证据落点：`test-evidence/w1-class1-sync-〈date〉.md`（盘点输出、逐 pair 命令与结果、负债索引）+ triage 表行。
- [X] T024 [US5] [blockedBy: T023] 转绿核对：定向运行 `bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py <受修复影响的镜像测试文件> -q` — 已同步对由 red 转绿（red = 基线失败集内的镜像名；green = 修复后 targeted 实测通过，非声称）；负债对保持 FB-06 登记状态、不声称 green；把转绿对照（基线失败名 → 修复后状态）落 `test-evidence/w1-class1-sync-〈date〉.md` 核对节。

**Checkpoint**: 套件承载全部引擎 pair；44 候选折叠完并逐行留证；Class 1 失败「同步修复或负债登记」闭环。

---

## Phase 7: User Story 5 — Part F · W1 Class 2 逐名 triage + 注入/定位演练（plan §Implementation Slicing F）

**Purpose**: 对 33 条非镜像基线失败逐名三选一处置（陈旧钉住更新 / 机制修复 / 负债登记），并以注入 + 定位演练证明合并后套件的防护与可定位性。

- [X] T025 [US5] [blockedBy: T024] gate-total 钉住类失败逐名 triage：对基线失败清单（FB-01 权威 83 名）中 gate-total 钉住条目逐名对照 owner 事实三选一 — 陈旧钉住（owner 值已合法移动）→ 按当前 owner 值更新钉住并记录理由（FR-018 允许、理由入行）；真回归 → 修机制；收口前无法归因/修复 → FB-06 负债登记。禁止删测试（FB-07）；每名一行入 triage 表（debt 行受 V-E5-2 约束）。证据落点：triage 表行 + 行内 evidence 指针（diff / owner 事实 / 负债记录路径）。
- [X] T026 [US5] [blockedBy: T024] exec-quant 类失败逐名 triage：对基线失败清单中 exec-quant 条目逐名执行同 T025 三选一纪律。证据落点：triage 表行。
- [X] T027 [US5] [blockedBy: T011,T024] loop-state 3 条逐名 triage：对 `tests/unit/test_loop_state_engine.py` 的 3 条基线失败（`test_terminal_states_with_unknown_commit_baseline_never_verify`、`test_unwatched_detector_positive_expired_and_negative`、`test_watchbeat_marker_projection_and_freshness`）执行同三选一纪律；与 T011 夹具改动衔接核对（夹具复用不得是该 3 条失败的原因，若夹具改动影响判定先归因再处置）。证据落点：triage 表行。
- [X] T028 [US5] [blockedBy: T022,T025,T026,T027] FB-08 注入演练 + FB-09 定位演练（SC-008 / SC-009）：选一个 T019–T022 产生的合并后参数化用例，临时注入单行断言失败 → 运行该用例并提取名称级清单（FB-04：`--names-out` 或等价提取）→ `comm -13` 差集 100% 命中且仅命中注入名；失败输出唯一 node id（含参数行标识）→ 按该 node id 定向重跑复现失败（FB-09）；随即还原注入并复跑确认还原。演练记录（命令、差集输出、重跑命令与结果、还原确认、日期）落 `test-evidence/injection-drill-〈date〉.md`。验收：命中、定位、复现三项全中；任一不中即停并按 Fast Fail 上报。
- [X] T029 [US5] [blockedBy: T024,T028] triage 表闭环核对：V-E5-1（83 名每名恰一行）、V-E5-2（debt-registered 行指向 dated 负债记录且注明非本范围引入）、V-E5-3（mirror-sync 行含 sync 命令与 pair 范围）；核对无任何基线失败以删测试方式处置（FB-07）；核对钉住名册（T002）与 triage 表的钉住交集全部有处置。证据落点：`test-evidence/failure-triage-2026-10-22.md` 的核对节（勾稽结果与残留负债清单）。

**Checkpoint**: 83 名全部有处置且留痕；演练三中；无删测试；残留负债显式登记。

---

## Phase 8: 收口与 review 前置（implement wrap-up；非 story 阶段）

**Purpose**: implement 期收尾：镜像义务核销、review 前置核对、verification 建档；review 派发由驱动者执行，closure 槽位（Phase 9）在 review 后、合并前执行。

- [X] T030 [blockedBy: T029] mirror 同步（如涉及）：对本特性触碰过的镜像对 — `scripts/bash/run-tests.sh`（预期零改动）与 `skills/external/sdd-loop-driver/`（仅引用性更新，FR-021 / RC-06）— 执行 `python3 scripts/python/sync-mirrors.py --write --only <pair>` 后 `--check --only <pair>` 本对零 drift，且全仓 `--check` 相对实施前读数零 NEW drift（plan § Mirror Obligations 判据）；未触碰任何镜像面则在 `verification.md` 显式记录「未触碰」。证据落点：核对输出贴入 `verification.md` 对应节。
- [X] T031 [blockedBy: T030] review 前置核对：任务行全闭合（GATE-3 grep 为 0）；两槽位核对（implement 内全量仅 T007 已跑，closure 槽位待 review 后）；`python3 .specify/scripts/python/validate-tasks.py .specify/specs/067-loop-efficiency-hardening/tasks.md` 0 error；证据齐备清单（E1 记录、w2 timing ×4、w1 sync 记录、w3 复测记录、drill 记录、triage 表、台账、钉住名册）逐项 `test -e`；把清单与核对输出写入 `verification.md` 的 review 前置节。
- [X] T032 [blockedBy: T031] verification.md 建档：记录 implement 期间哪些测试跑了（命令 + 计数 + 证据指针）、哪些未跑、waiver 原文（无则记 none）；SC-001…SC-005 自应用证据 = 本特性 dispatch log 如实转录（turn / token 不可得记 `not_evaluated`，FR-007，不编造数字）；SC-006…SC-010 标 `pending-closure`（待 T033–T038 closure 槽位回填）。验收：文件存在、SC 逐项有状态。

**Checkpoint**: implement 期收尾完成、review 可派发；closure 槽位任务待 review 后、合并前执行。

---

## Phase 9: closure 槽位验收（plan §W5；执行时点 = review 后、合并前）

**Purpose**: 全部达标判据的最终验证轮：E4 双清单、MP-02 冷缓存达标测量、SC-007/SC-008/SC-010 三项审计与 verification 定稿。

- [ ] T033 [blockedBy: T032] post id 清单再生（E4 post 侧）：与 T001 同法（V-E4-1 同一收集方法）`bash scripts/bash/run-tests.sh --collect-only -q`，剔除头/汇总行后一行一条写入 `test-evidence/post-test-ids-〈date〉.txt`（transient 证据，头部记录生成命令 + 日期 + 解释器）。验收：与基线清单同格式；行数偏差（预期 = 基线 − 折叠数 + 新增数）在 T035 审计中解释。
- [ ] T034 [blockedBy: T033] SC-006 达标测量（closure 槽位）：MP-02 逐字组合冷缓存完整运行（MP-03 清理后至运行结束无其他运行）；E1 全字段记录 `test-evidence/full-run-〈date〉-closure.md`（`baseline_pointer` = 基线 dated 记录；墙钟 = 包装 epoch 差，pytest 自报仅交叉核对，MP-04）；达标主张只认本记录（MP-08：wall ≤600 s、三层全执行、deselected=0、MP-07 达标主机）；若 >600 s → RC-04：dated 证据 + 显式范围修订 / clarify 升级，禁止静默改命令、子集运行、降层；xdist 不采用维持串行（R-7 / RC-03）。同时把 closure 槽位写为状态脊 `<!-- test-budget -->` 围栏 063-E2 槽位行（slot=closure，含名称级差集字段，GATE-6 审计 `baseline:1 closure:1`）。
- [ ] T035 [blockedBy: T033,T034] SC-007 覆盖审计（LED-05）：`comm -23 test-evidence/baseline-test-ids.txt test-evidence/post-test-ids-〈date〉.txt` 得缺失集 → 按合同 LED-05 的 inline 过程逐 id 对账台账（case 行按全 id、file 行按声明前缀机械展开），unmatched = 0 为过线（LED-06）；E1 layer_counts 与基线三层计数（**以 E4 头注为准：contract 3426 / unit 734 / integration 391，collect 4551**；4553/3428 为缓存 union 旧锚点，已废弃，见 review P2-1）交叉核对；post-only 新增 id 报告性列出（LED-08）。inline 过程文本与完整输出落 `test-evidence/coverage-audit-〈date〉.md`。
- [ ] T036 [blockedBy: T034] SC-008 漂移防护审计：从 T034 closure 运行日志提取 FAILED 名称清单（剥离 `FAILED ` 前缀与装饰、排序、一行一条，与基线清单同格式；FB-04 认可的等价形态，避免为取名单再做一次全量）→ 以 T007 的 `--names-out` in-stage 基线为权威对照：`comm -13 test-evidence/baseline-failures-<date>-implement-start.txt <post-names>` 为空（零 NEW 名）；pre-stage 83 名清单只作范围对照差集。钉住名册按 **W-1 裁定**执行台账 join（review.md §4 P1-1）：每个名册 id 要么在 post 清单，要么其 case-merge 行指向 post 清单内且绿色的套件参数；映射依据 = `test-consolidation-ledger.md` + `pinned-roster-addendum-2026-10-22.md`。closure 名称级差集两侧各含同 **15** 条在册红（14 pre-existing-debt + i11 stale-pin）即 0 NEW；不得在 closure 期顺手修 debt 名。triage 闭环（T029）复核；本范围零新增钉住失败。差集输出落 `test-evidence/name-diff-〈date〉.txt`，审计段落落同目录 dated 记录。
- [ ] T037 [blockedBy: T034] SC-010 依赖边界检索（RC-08 / quickstart S7）：`git diff <实施基点>..HEAD -- pyproject.toml` 核对运行时依赖段 diff 为空；测试侧新增依赖（预期零）全在开发依赖组；`grep -rnE "urllib|requests|httpx|socket" tests/` 仅既有匹配、新增面为 0。检索命令与输出落 `test-evidence/dependency-boundary-〈date〉.md`。
- [ ] T038 [blockedBy: T035,T036,T037] verification 定稿：SC-006…SC-010 逐项回填状态与证据指针；closure 运行结果并入运行记录（哪些跑了 / 未跑 / waiver 原文如有）；SC-001…SC-005 证据核对；不可得项 `not_evaluated`；RC-04 是否触发与残余风险如实记录。验收：DoD-7 满足；GATE-1…GATE-7 全过或带显式豁免记录。

**Checkpoint**: SC-006…SC-010 全部有 dated 证据或显式升级记录；特性进入 review 后合并路径。

