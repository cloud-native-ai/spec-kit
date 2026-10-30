# Tasks: Coaching Skills（教练技能） — 078

**Requirement ID**: 078
**Requirement Key**: `078-coaching-skills`
**Branch**: `078-coaching-skills`（本阶段禁止切换或新建分支；不 push）
**Related Feature**: Feature 078 — Coaching Skills（教练技能）, status `Planned`（tasks 阶段不推进状态机；`Planned → Implemented` 归 `/speckit.implement`，活状态只在 `.specify/memory/features.md` 的 078 行）
**Input**: Design documents from `.specify/specs/078-coaching-skills/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required；29 FR / 9 SC / 4 用户故事 / 17 Shared Strings）、`data-model.md`（8 实体 + 4 状态机）、`contracts/`（5 份文件 / 38 条款，全部 `md-heading` 形）、`quickstart.md`（5 场景）、`feature-ref.md`

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」把测试定为先写后实现，本特性的五个新契约测试文件全部红先行；同时按 Principle VII 的 **template-only 门**：技能本体是提示词契约、改名接线是注册表与再生成产物，都没有可跑的运行时，它们的「测试」是**结构契约测试**（正文条款断言、夹具记录集的正/反例判定、坐标与名册计数、镜像与副本零漂移、`cleanup_obsolete_framework_assets` 的真实删除语义），不是 unit/integration 测。两层都发，且不互相替代。

**Tests**: 五组红先行各自先在未改动树上跑出**记录在案的失败**（命令、真实输出、退出码、失败计数四字段，落入 `.specify/specs/078-coaching-skills/notes/red-first-evidence.md`）：`tests/contract/test_coaching_run_contract.py`（T009）、`tests/contract/test_coaching_expectation_contract.py`（T014）、`tests/contract/test_coaching_observation_contract.py` + `tests/contract/test_coaching_dispatch_contract.py`（T017）、`tests/contract/test_coaching_wiring_contract.py`（T020）。四个冻结基线测试的更新（T027）属**实现后守卫**（迁移/回归例外），排在全部接线之后并携带显式 `[blockedBy:]`，不作红先行声称。

**Organization**: 按 `requirements.md` 的四个用户故事分组（US1、US2 为 P1；US3、US4 为 P2）；Setup / Foundational / Polish 行无故事标签。38 条契约条款由 16 行以 `[green:]` 认领，每条款恰好一行、同一契约内条款序随行序递增（§ Clause Partition）。Foundational 承载「改名骨架」——新目录、身份 frontmatter、台账行、probe 行、目录登记与编译面，因为 US1…US3 的正文都必须写在新坐标上；它不是任意故事的内容。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/078-coaching-skills/verification.md` 的 `deferred_tasks=`。
- DoD-2: 38 条契约条款各被恰好一行 `[green:]` 认领；`python3 scripts/python/validate-tasks.py .specify/specs/078-coaching-skills/tasks.md` 退出 0，四项 green 检查（dangling / cross-phase / clause-collision / path-divergence）零 finding。
- DoD-3: 五个新契约测试文件红先行（`notes/red-first-evidence.md` 四字段记录）并全部转绿；四个冻结基线测试显式更新（每处带 2026-10-30 与 Feature 078 的日期理由），更新后的计数与目录实测一致。
- DoD-4: 八身份坐标一致——新目录、frontmatter `name`、`skill_id`、运行时 unit id、台账行、probe 行、路由行、description 触发词；每个坐标各以一条判定通过并按坐标计数（`coaching-skills` 被 `skill:coaching-skills` 包含不重复计，8/8）；`flow-class-check.py --action lookup --unit-id "skill:coaching-skills"` 报 `source: ledger` / `execution` / `behavior-oracle`；`probe-utils.py --action compile-embeds --check` 报 `75 units, zero drift`。
- DoD-5: 闭集内旧名出现次数恰为 1（仅 `_OBSOLETE_SKILLS` 条目），裁决由 guard copy 机械派生（`MIRROR_PAIRS` 六对 + `regen-command-copies.py` 目标 + A10 残余成员），`.qoder/agents`、`.specify/agents/templates`、`.specify/shared/definitions`、`.specify/memory/feedback/probe-map.md` 各独立判定；`.specify/skills/think-skills` 不存在；`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对改动前基线零新增漂移。
- DoD-6: 教练闭环的四产物在 `notes/quickstart-run.md` 记录的一次真实运行中按序存在，夹具主产物真实存在；优化状态以封闭值域单列，且优化不可用不把执行判为失败。
- DoD-7: 零新增阻断式确认门——`git diff <base> -- <scan-confirmation-gates.py 的 SCAN_DIRS + SCAN_ROOT_FILES 扫描面> | grep '^+'` 的**新增行 0 命中** `BLOCKING_PATTERNS`（pattern 集与改动前基线读数入证据；不以新增前后总量相等为判据）；技能保持 `classification: external`。
- DoD-8: `verification.md` 为 SC-001…SC-009 各记一条状态行；历史记录（`.specify/specs/**` 旧特性、`memory/evidence/**`、`features/<ID>.md`、reviews、eval-baseline）未被改写。
- DoD-9: 新技能形态 `skill-shape.py --budget-tokens 5000` 判 `pass`（退出 0），读数与 findings 记入 `notes/skill-shape-after.md`；T001 采的旧技能基线只作对照，不替代本项。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 scripts/python/validate-tasks.py .specify/specs/078-coaching-skills/tasks.md` 退出 0，0 error / 0 warning（含四项 green 判定）。
- GATE-2: 跨制品一致 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/078-coaching-skills --stage tasks --repo .` 报 `decision=pass`、`errors=0`；`missing-path` advisory 只允许命名本特性将新建的路径（`skills/external/coaching-skills/**`、`.specify/memory/coaching/**`、`tests/fixtures/coaching/**`、`notes/**`、`coverage-baseline.txt`、`verification.md`）与 plan 期既有的待建清单；其它路径的 advisory 是缺陷。
- GATE-3: 拆解尺度 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/078-coaching-skills/requirements.md --tasks .specify/specs/078-coaching-skills/tasks.md` 报 `decision=proceed`，`task_count` 不超过该脚本的 `TASK_CEILING`。
- GATE-4: 条款认领 — check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/078-coaching-skills` 报 `claimed clauses (this feature): 38`，且 `UNCOVERED` 名单中不出现任何 `078-coaching-skills/contracts/` 名字。该命令的 FR 车道读数为 0/29：本特性的契约正文不带引用组，FR→条款的映射目前只写在 `plan.md` § Phase 1（指针所有者），属制品缺口而非本阶段可修项，交 `/speckit.analyze` 裁定（见 § Measured Premises）。
- GATE-5: 新组转绿且既有守卫无新增失败 — check（经 profiles venv 的 `python -m pytest -q`）：五个新测试文件全绿、四个冻结基线测试全绿，且既有套件失败名集合相对实现期基线（捕获形式归 `/speckit.implement` 的 `**Test runs**` bullet，此处引用不重述）无新增。
- GATE-6: 接线与派生面 — check: `flow-class-check.py --action check` 报 `matched=79 inventory_units=79`、`probe-utils.py --action probes --validate` 退出 0、`probe-utils.py --action compile-embeds --check` 报 75 units 零漂移、`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 退出 0；旧名残留的**裁决**由 `tests/contract/test_coaching_wiring_contract.py` 给出（候选集机械派生 + 恰一处断言），`.qoder/agents` / `.specify/agents/templates` / `.specify/shared/definitions` / `.specify/memory/feedback/probe-map.md` 各独立判定；`git grep -n` 仅作诊断旁证。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/078-coaching-skills/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器、镜像、集群、注册表或特殊硬件依赖；全部工作为本地文件、本地 git、本地 pytest。

- Python（系统解释器）: **available** — probe: `python3 --version` → `Python 3.9.6` @ 2026-10-30；affected: T002、T004–T031 的全部确定性引擎行（只要求 ≥3.8 与标准库）。
- pytest: **partial** — probe: `.venv/bin/python -m pytest --version` → `No module named pytest`（仓库自带 `.venv` 是 Python 3.14.6 但未装 pytest）；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` → `pytest 9.1.1` @ 2026-10-30。affected: T009、T014、T017、T020、T027、T031。处置：测试一律经 profiles venv 的 `python -m pytest` 运行。
- `specify` CLI: **partial** — probe: `.venv/bin/specify render-agents --help` 可用（渲染入口存在）@ 2026-10-30；PATH 上的 `specify` 是**改动前**的构建，不含本次 `_OBSOLETE_SKILLS` 条目。affected: T023（只用 render 子命令）、T020 / T028（升级语义改由 `cleanup_obsolete_framework_assets` 的真实调用验证，不依赖重新构建 CLI）。
- Git: **available** — probe: `git --version` → `git 2.54.0 (Apple Git-157)` @ 2026-10-30；affected: T004（`git mv`）、T026（残留审计面诊断）、T031（新增行门禁判定）。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 `[P]` 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US4]`；故事相位每行必有且仅有一个，Setup / Foundational / Polish 行禁止出现。
- **[blockedBy: T004,T006]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **[green: <contract>#<clause>]**: 本行是把该条款转绿的那一行；标签面定义归 `.specify/templates/tasks-template.md` § Format，机器校验归 `scripts/python/validate-tasks.py`，契约路径相对本文件目录解析，同一行内多条款按序递增书写。认领分区见 § Clause Partition。
- 任务状态符（`- [ ]` / `- [>]` / `- [X]` / `- [~]`）归 `.specify/templates/tasks-template.md` § Task State Sigil，本文件不复述。
- 每行给出具体文件路径与可执行验收；测试行写明它写入的证据槽，实现行写明它让哪一组断言转绿。

## Measured Premises（2026-10-30 生成时实测，HEAD `bc0ea7fb`，分支 `078-coaching-skills`）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/078-coaching-skills/requirements.md` | `29` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/078-coaching-skills/requirements.md` | `9` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/078-coaching-skills/requirements.md` | `4`（US1/US2 为 P1，US3/US4 为 P2） |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/078-coaching-skills/requirements.md` | `17` |
| 契约文件数 | `ls .specify/specs/078-coaching-skills/contracts/*.md \| wc -l` | `5` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/078-coaching-skills/contracts/*.md \| grep -c '^  C-'` | `38`（coaching-run 14 + dispatch-payload 5 + expectation 5 + identity-and-wiring 8 + observation 6） |
| 条款计数陷阱形 | `grep -oh 'C-[0-9]\{1,2\}' .specify/specs/078-coaching-skills/contracts/*.md \| wc -l` | `54` — 这是条款 id 的**提及**数（条款内互引），单位是条款**定义**时正确答案是 38；两数并记，表明测量是有意取的 |
| 命令模板 / 技能目录 | `ls templates/commands/*.md \| wc -l`；`ls skills/external/*/SKILL.md \| wc -l`；`ls skills/internal/*/SKILL.md \| wc -l` | `27` / `15` / `37`（技能合计 52） |
| probe 编译单元 | `for f in templates/commands/*.md skills/external/*/SKILL.md skills/internal/*/SKILL.md; do grep -q '^## Wrap-up' "$f" && echo x; done \| wc -l`；交叉核对 `python3 scripts/python/probe-utils.py --action compile-embeds --check` | 计数脚本 `75`（23 命令 + 52 技能）；引擎 `75 units, zero drift` |
| probe 单元计数陷阱形 | 同上的计数脚本逐类打印 | 命令侧 23 / 技能侧 52：**4 个命令模板没有 Wrap-up 面**，所以 27 + 52 = 79 ≠ 75；改名是删一个技能单元、增一个技能单元，净变化 0——`plan.md` § Mirror Obligations 与 `quickstart.md` § 1.2 里「75 增至 76」的预期与实测冲突，本文件按 75 记账（PLAN-EDIT 见 § Notes） |
| 台账 | `python3 scripts/python/flow-class-check.py --action check` | `79 unit(s) scanned, 0 finding(s)`；`ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0` |
| 新名当前解析 | `python3 scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"` | `flow_class: execution` / `source: default`（不是 `ledger`），退出码 0——未知单元回落默认值，故断言必须看 `source`，不能只看退出码 |
| probe 注册表 | `python3 scripts/python/probe-utils.py --action probes --validate` | `Probe registry valid: 10 classes, 117 internal + 0 external objects`，退出码 0 |
| 门禁基线 | `python3 scripts/python/scan-confirmation-gates.py --summary` | `blocking confirmation gates: 27`（destructive 20 + governance_kept 7），`violations 0` |
| 旧名受版本管理文件 | `git grep -l "think-skills" \| wc -l` | `85`（含本规格自身与派生镜像；SC-006 不以全仓计数为判据，只认 A10 的封闭集） |
| 旧名闭集命中 | `git grep -c "think-skills" -- skills/external skills/internal templates/commands agents shared/definitions src/specify_cli/__init__.py docs/reference/agents/command-and-skills.md docs/tutorials/quickstart.md tests/contract .specify/skills` | `26` 个文件 = 19 个手改源 + 7 个派生镜像（`.specify/skills/…`）；逐文件次数最高的是两个技能本体（源 8 次、镜像 8 次） |
| 旧名出现次数陷阱形 | `git grep -o "think-skills" \| wc -l` | `198` 次——单位是「文件」时用 `-l`（85），单位是「某个文件内几次」时用 `-c`，单位是「全仓出现几次」时用 `-o`；三个数都真实，混用就会得到互相矛盾却都自称实测的结论 |
| 技能形态基线 | `python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/think-skills/SKILL.md` | `pass`，`≈1981 tokens` / `110 行`，两条 warning（`oversized-section` Workflow 51 行、`flags-outside-contract` Wrap-up 23 flag） |
| 覆盖率基线 | `head -2 .specify/specs/078-coaching-skills/coverage-baseline.txt` | 头部含 `excluding 078-coaching-skills`、`files: 229 (parsed 135 + named 94)`、`base-sha: bc0ea7fbd268`——本阶段已冻结；本特性 38 条只能被任务行认领，不能被自己的基线豁免 |
| FR 车道现状 | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/078-coaching-skills \| tail -8` | `FR claimed: 0` / `FR uncovered: 29`——五份契约正文不带引用组，FR→条款映射目前只写在 `plan.md` § Phase 1；本阶段不改写 plan 属主制品，故在 GATE-4 如实记录为制品缺口 |
| 待建目录 | `ls -d .specify/memory/coaching .specify/specs/078-coaching-skills/notes tests/fixtures/coaching` | 生成时三条都是 `No such file or directory`：`notes/` 由 T001 建并写测量，`tests/fixtures/coaching/` 由 T003 建，`.specify/memory/coaching/` 由 T011 的首次运行建；本阶段只把 `coverage-baseline.txt` 冻结到 spec 目录根（不在 `notes/` 内），未替这三处预置任何内容 |
| 任务行预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/078-coaching-skills/tasks.md` | 本文件 31 行（T001–T031），不超过 `decomposition-check.py` 的 `TASK_CEILING` 上限 |
| 任务行预算陷阱形 | `grep -oE 'T[0-9]{3}' .specify/specs/078-coaching-skills/tasks.md \| wc -l` | 远大于 31——这是任务标识的**提及**数（`[blockedBy:]`、覆盖表、认领表都在引用），不是定义数；单位是任务**行**时用行首锚定 `^- \[ \] T` |

## Clause Partition

38 条条款、5 份契约文件，每条款恰被一行认领，同文件内条款序随行序递增。认领的引擎是 `account-clause-coverage.py`（`claimed clauses` 必须等于 38），本表只是声明。

| Contract file | Clauses | Claimed by |
|---|---|---|
| `contracts/coaching-run.contract.md` | C-1、C-2 | T010 |
| `contracts/coaching-run.contract.md` | C-3、C-4、C-5、C-6 | T011 |
| `contracts/coaching-run.contract.md` | C-7、C-8、C-9、C-10 | T012 |
| `contracts/coaching-run.contract.md` | C-11、C-12、C-13、C-14 | T013 |
| `contracts/expectation.contract.md` | C-1、C-2、C-3 | T015 |
| `contracts/expectation.contract.md` | C-4、C-5 | T016 |
| `contracts/observation.contract.md` | C-1…C-6 | T018 |
| `contracts/dispatch-payload.contract.md` | C-1…C-5 | T019 |
| `contracts/identity-and-wiring.contract.md` | C-1 | T021 |
| `contracts/identity-and-wiring.contract.md` | C-2 | T022 |
| `contracts/identity-and-wiring.contract.md` | C-3 | T023 |
| `contracts/identity-and-wiring.contract.md` | C-4 | T024 |
| `contracts/identity-and-wiring.contract.md` | C-5 | T025 |
| `contracts/identity-and-wiring.contract.md` | C-6 | T026 |
| `contracts/identity-and-wiring.contract.md` | C-7 | T027 |
| `contracts/identity-and-wiring.contract.md` | C-8 | T031 |

**Partition check**: 14 + 5 + 6 + 5 + 8 = 38；16 个认领行，无条款落在两行，无行认领其相位之后才能转绿的条款带。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T010, T020 | FR-016 | T012 |
| FR-002 | T010 | FR-017 | T012 |
| FR-003 | T010 | FR-018 | T004, T005, T006, T021 |
| FR-004 | T010, T015 | FR-019 | T021 |
| FR-005 | T015 | FR-020 | T024 |
| FR-006 | T015 | FR-021 | T023 |
| FR-007 | T016 | FR-022 | T022 |
| FR-008 | T010, T016 | FR-023 | T027 |
| FR-009 | T011, T019 | FR-024 | T026, T027 |
| FR-010 | T011 | FR-025 | T011, T019 |
| FR-011 | T018 | FR-026 | T004, T025 |
| FR-012 | T011, T018 | FR-027 | T013, T031 |
| FR-013 | T013, T018 | FR-028 | T011, T012 |
| FR-014 | T012, T018 | FR-029 | T012, T019 |
| FR-015 | T012, T018 | — | — |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T009, T029 |
| SC-002 | T009, T011 |
| SC-003 | T012, T014 |
| SC-004 | T017, T018 |
| SC-005 | T012, T017, T029 |
| SC-006 | T020, T021, T022, T023, T024, T025, T026, T027, T031 |
| SC-007 | T020, T024, T028 |
| SC-008 | T023, T028 |
| SC-009 | T027 |

**流程行与取证行**: T001、T002、T003、T028、T029、T030 为证据与执行行，不认领条款——T028 / T029 服务 SC-001 / SC-005 / SC-007 / SC-008 的复现，T030 服务技能形态预算，T020 / T026 服务 SC-006 的残留裁决；T031 是终局门禁与 SC 状态行落档行。不构成漏映射。

## Mirror Obligations

镜像对的清单所有者是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对），范围登记见 `plan.md` § Mirror Obligations，本文件不复述其行内容。落地形态：源编辑分散在 T004（技能包）、T005 / T006 / T007（三份 `shared/definitions`）、T021（路由模板）、T022（agents 与角色模板与 docs）；**T023 是唯一的镜像同步与再生成行**（`--write` 后逐对陈述无新增漂移），T026 的残留裁决与 T031 的终局验证只读不写；T024 的 `_OBSOLETE_SKILLS` 与 T027 的冻结测试无镜像义务；`templates/commands/**` 不在 templates 镜像对内，只经 `regen-command-copies.py` 产出 per-tool 副本。派生面 MUST 由再生成入口产出，MUST NOT 手改。

## Test Budget

- **本阶段（tasks）不运行任何测试套件**（docs-only 预算）：`validate-tasks` / `decomposition-check` / `pre-analyze-check` / `account-clause-coverage` 的输出留档 `test-evidence/tasks-*.txt`。
- **实现期基线（恰好一次）**: 实现开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获失败名基线；本文件任何行不得重捕获或刷新。
- **中间阶段**: 定向集 `targeted-set-v1`（`stage_base=bc0ea7fb`），逐故事跑本故事新增/更新的测试文件，不跑全量。
- **闭环节点**: review 之后由驱动者跑一次全量并按名比较；本特性任何行不得预支。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 证据槽与改动前/基线读数——后续每个相位都往这两个落点写，先建好它。

- [ ] T001 建证据槽并采集改动前读数：把六条命令的真实输出（命令、日期、退出码一并）写进 `.specify/specs/078-coaching-skills/notes/pre-change-measurements.md` —— `git grep -l "think-skills" | wc -l`、闭集逐文件 `git grep -c`、`python3 scripts/python/flow-class-check.py --action check`、`python3 scripts/python/probe-utils.py --action compile-embeds --check`、`python3 scripts/python/scan-confirmation-gates.py --summary`、`python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/think-skills/SKILL.md`；该文件是全特性「改动前侧」的唯一落点。
- [ ] T002 在实现起点按 never-cache 规则重采条款覆盖基线：`python3 scripts/python/account-clause-coverage.py .specify/specs/078-coaching-skills --freeze > .specify/specs/078-coaching-skills/coverage-baseline.txt`（脚本只打印、不写文件），核对头部含 `excluding 078-coaching-skills` 且正文不含本特性任何一条条款名；把两车道读数（`claimed clauses`、`UNCOVERED` 中属于本特性的条数、`FR uncovered`）追加进 `.specify/specs/078-coaching-skills/notes/pre-change-measurements.md`，并注明 FR 车道的成因见 § Measured Premises。

**Checkpoint**: 两个证据落点存在且写着真实读数——后续任何行引用「改动前」时只指向 `notes/pre-change-measurements.md` 与 `coverage-baseline.txt`。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 让新坐标先存在——夹具、改名骨架、台账行、probe 行、目录登记与编译面。四个故事都写在新名字、新路径上，没有这一相位它们无处落笔。

- [ ] T003 [P] 建夹具：写 `tests/fixtures/coaching/fixture-trainee/SKILL.md`（最小 Trainee，主产物为一份清单文件，流程内置一处正确性缺陷与一处效率退化，供 US1/US2/US3 的记录契约测试共用）与 `tests/fixtures/coaching/work.md`（夹具工作原文，逐字进入派发载荷断言）。
- [ ] T004 [P] 改名技能包骨架：`git mv skills/external/think-skills skills/external/coaching-skills`，然后把 `skills/external/coaching-skills/SKILL.md` 的 frontmatter 改为 `name: coaching-skills`、`skill_id: "<SKILL:.specify/skills/coaching-skills/SKILL.md>"`、description 触发词改为 教练 / 陪练 / 观察执行 / 预期 vs 实际 / 执行偏差 / 微调建议 / coaching 并写明调用形态 `coaching-skills <trainee-name|trainee-path> <work>`，删掉 thought experiment / 思想实验 / 不要真的执行 这类承诺零副作用的说法；`classification: external` 不动，正文留给 T010–T013 与 T015/T016/T018 重写。
- [ ] T005 [P] 台账行改名：在 `shared/definitions/flow-class-definitions.md` 用 `skill:coaching-skills | execution | behavior-oracle | （空中立标记）| 理由改写为「先给预期、再看真实执行、最后给微调」的教练闭环` 替换旧名行，台账版本 1 → 2（2026-10-30），§ 变更记录 追加一条；同时把文件头过期的 78 行 / 51 技能读数更正为实测的 27 命令 + 52 技能 = 79 行并标注 2026-10-30。
- [ ] T006 [P] probe 行改名：把 `shared/definitions/probe-definitions.md` 的 Object 行 `skill-think-skills-wrapup | skill-wrapup | skill:think-skills | wrap-up` 改成 `skill-coaching-skills-wrapup | skill-wrapup | skill:coaching-skills | wrap-up`；改名只换行不新增行，单元数不变。
- [ ] T007 [P] 登记运行目录：在 `shared/definitions/framework-map.md` 的 Project memory 行补 `.specify/memory/coaching/`（`<run-id>` 运行产物目录，一文一件），同一次变更内完成（宪法 XVII 目录治理）。
- [ ] T008 [blockedBy: T004,T006] 重建编译面：`python3 scripts/python/probe-utils.py --action compile-embeds` 让 `skills/external/coaching-skills/SKILL.md` 的 `## Wrap-up` 由注册表编译（不得手写），再 `--action map` 重建 `.specify/memory/feedback/probe-map.md`；随后 `--action compile-embeds --check` 应报 `75 units, zero drift`。

**Checkpoint**: 新名在目录、frontmatter、unit id、台账、probe 与编译块上各就位；`flow-class-check.py --action lookup --unit-id "skill:coaching-skills"` 报 `source: ledger`。

---

## Phase 3: User Story 1 - 一次教练闭环：先给预期，再看真实执行，最后给微调 (Priority: P1) — MVP 的一半

**Goal**: 让 `coaching-skills` 的技能正文承载完整闭环——解析 Trainee、落盘预期、恰好一次派发、观测、偏差、提升计划、经既有入口优化，并以封闭值域收束运行状态。

**Independent Test**: `tests/contract/test_coaching_run_contract.py` 全绿：合规夹具记录集四产物齐备且顺序正确、主工件在；反例集（缺预期、两次派发、失败被叙述成完成、优化不可用被判成失败）逐条判红。

### Tests for User Story 1 (MANDATORY)

- [ ] T009 [US1] [blockedBy: T003,T008] 红先行写 `tests/contract/test_coaching_run_contract.py`：按 `contracts/coaching-run.contract.md` 的 C-1…C-14 组织断言（两个位置参数与解析阶梯、命中计数与 fail-closed、run-id 与运行目录、四产物与顺序、执行优先、恰好一次派发且失败不重试、退化阶梯与 `evidence: none`、运行状态封闭值、双上下文与载荷禁止项、治理预算），用 `tests/fixtures/coaching/` 与 `tmp_path` 构造合规集与反例集（反例必须被判红，保证判定可复现），并把 `pytest -q tests/contract/test_coaching_run_contract.py` 的真实失败（命令、输出、退出码、失败计数）记入 `.specify/specs/078-coaching-skills/notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T010 [US1] [blockedBy: T009] [green: contracts/coaching-run.contract.md#C-1] [green: contracts/coaching-run.contract.md#C-2] 写 `skills/external/coaching-skills/SKILL.md` 的 § Inputs / § Trainee Resolution / § Preflight：两个位置参数缺一即 fail-closed 并点名缺失项、`<work>` 原样透传且不得与 Trainee 目标互换、解析复用 `run-skills` 的四坐标阶梯（源与镜像同实体算一次命中，仅跨层同名才算两次并点名两个候选，未找到点名坐标）、`SKILL.md` 缺失或 frontmatter 非法或目标是自身时在预期阶段之前拒绝，缺参只问一句普通澄清并停止。
- [ ] T011 [US1] [blockedBy: T010] [green: contracts/coaching-run.contract.md#C-3] [green: contracts/coaching-run.contract.md#C-4] [green: contracts/coaching-run.contract.md#C-5] [green: contracts/coaching-run.contract.md#C-6] 写 § Run Identity / § Artifacts and Order / § Execution First / § Single Dispatch：run-id 形态 `YYYYMMDDTHHMMSSZ-<trainee-slug>` 与目录已存在即 fail-closed 不加后缀、四产物文件名与落盘顺序（`expectation.md` 先于第一次派发动作，`dispatched-at` 是顺序证据）、主成功条件是 Trainee 主工件产生、优化不得前置也不得压缩执行、每次恰好一个子代理且失败不重试、教练不得代跑或注入副作用。
- [ ] T012 [US1] [blockedBy: T011] [green: contracts/coaching-run.contract.md#C-7] [green: contracts/coaching-run.contract.md#C-8] [green: contracts/coaching-run.contract.md#C-9] [green: contracts/coaching-run.contract.md#C-10] 写 § Compare / § Improvement Plan / § Optimization / § Run Status：偏差按两维度对照并逐条引观测记录证据、区分 `result-deviation` 与 `process-deviation`、提升计划条目点名 Trainee 的文件与章节并给一条具体微调、优化经 `improve-skills` 既有入口且先建 `.optimization-claim` 并扫描同一 Trainee 的其它 claim（冲突即点名 run-id 停止，不重试）、`run` 与 `optimization` 两个封闭值域的判定规则写在 `improvement-plan.md` § Run Status。
- [ ] T013 [US1] [blockedBy: T012] [green: contracts/coaching-run.contract.md#C-11] [green: contracts/coaching-run.contract.md#C-12] [green: contracts/coaching-run.contract.md#C-13] [green: contracts/coaching-run.contract.md#C-14] 写 § Degradation Ladder / § Boundaries：`host-event` → `self-report` → `observation-gap` → 完全无观测（计划仍产出、逐条 `evidence: none`、`run: partial`）；技能保持 `external`、新增文案对阻断模式零命中、Trainee 自身的破坏性步骤以转达方式取得用户答复后再派发、教练预期与 Trainee 实际理解的分歧作为可报告发现保留。

**Checkpoint**: US1 可独立验证——闭环的每一步在正文里都有可判定的落地位置，且反例集逐条被判红。

---

## Phase 4: User Story 2 - 预期必须双维度可判定 (Priority: P1)

**Goal**: 执行预期不是一段感想：结果面写清应产出什么、验收判据与允许偏差；过程面写清步骤量级、工具调用轮廓、重试余量与关键路径，且每项可推导或标为校验缺口。

**Independent Test**: `tests/contract/test_coaching_expectation_contract.py` 全绿：合规预期通过、缺 `## Process Efficiency`、出现「大致符合」这类不可判定措辞、把无法推导的数字编出来，三种反例各判红。

### Tests for User Story 2 (MANDATORY)

- [ ] T014 [US2] [blockedBy: T003,T008] 红先行写 `tests/contract/test_coaching_expectation_contract.py`：按 `contracts/expectation.contract.md` 的 C-1…C-5 断言文件骨架与必备章节、OC/PE 行字段与封闭容差形态、不可判定措辞被拒、无法推导项标 `validation-gap` 而非编造数字、预期阶段的四条零副作用；用 `tmp_path` 造合规与反例，并把真实失败记入 `.specify/specs/078-coaching-skills/notes/red-first-evidence.md`。

### Implementation for User Story 2

- [ ] T015 [US2] [blockedBy: T014] [green: contracts/expectation.contract.md#C-1] [green: contracts/expectation.contract.md#C-2] [green: contracts/expectation.contract.md#C-3] 写 `skills/external/coaching-skills/references/prompt-templates.md` 的预期模板：文件骨架（Run header / Trainee / Outcome Correctness / Process Efficiency / Assumptions / Unknowns / Forbidden Side Effects / Trainee Failure Semantics），OC 表五列（`OC-1` 点名主交付物，验收与允许偏差只用 `pass|fail` 或 `tolerance=<number><unit> severity=<low|medium|high>`），PE 表五列（步骤量级、工具调用轮廓、重试余量、关键路径、derivation 或 `validation-gap`）。
- [ ] T016 [US2] [blockedBy: T015] [green: contracts/expectation.contract.md#C-4] [green: contracts/expectation.contract.md#C-5] 写同一文件的推导方法段与零副作用段：沿用原技能的心智模拟流程（仿真契约 + 自然语言逻辑与程序化逻辑的分层审计，脚本契约按给定输出处理），并声明预期阶段不得执行 Trainee 的工具、不得写 Trainee 目录、不得发起网络或外部动作、不得创建 claim；`SKILL.md` 的预期步骤只留一句指针指向该文件，把逐步骤手册留在 references。

**Checkpoint**: US2 可独立验证——单看 `expectation.md` 就能在执行后逐条核对两个维度。

---

## Phase 5: User Story 3 - 子代理真实执行，教练只观测不代跑 (Priority: P2)

**Goal**: 派发载荷只带 Trainee 目标、`<work>` 原文与「按 Trainee 自身 SKILL.md 执行」的指示；观测记录逐步承载动作、工具、状态、产物、耗时与来源，不可见步骤显式标缺口。

**Independent Test**: 两个测试文件全绿：`test_coaching_observation_contract.py` 的含一处不可观测步骤的夹具恰好出现一次缺口标记且 `## Gaps` 不重复标记；`test_coaching_dispatch_contract.py` 的载荷字段集闭合并对四类禁入内容逐条判红。

### Tests for User Story 3 (MANDATORY)

- [ ] T017 [US3] [blockedBy: T003,T008] 红先行写 `tests/contract/test_coaching_observation_contract.py`（`contracts/observation.contract.md` C-1…C-6：节序、九列步表、来源封闭值、缺口只标步骤行且计数、失败/超时/拒绝如实记录、无观测仍产出记录）与 `tests/contract/test_coaching_dispatch_contract.py`（`contracts/dispatch-payload.contract.md` C-1…C-5：必需字段、四类禁止字段、一次一份、返回异常行原样写入、传输方式入 DispatchRecord），两文件共用 `tests/fixtures/coaching/`，真实失败记入 `.specify/specs/078-coaching-skills/notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T018 [P] [US3] [blockedBy: T017] [green: contracts/observation.contract.md#C-1] [green: contracts/observation.contract.md#C-2] [green: contracts/observation.contract.md#C-3] [green: contracts/observation.contract.md#C-4] [green: contracts/observation.contract.md#C-5] [green: contracts/observation.contract.md#C-6] 写 `skills/external/coaching-skills/references/prompt-templates.md` 的 § Observation Record / § Deviations / § Improvement Plan 模板：`## Run header` / `## Dispatch` / `## Steps` / `## Gaps` / `## Result` 的节序，九列步表（step、trigger/instruction、action、tool-call、state-change、artefact、elapsed、source、consistency），consistency 只做观测判定且不得执行 Trainee 的验证逻辑，缺口在步骤行标 `observation-gap` 而 `## Gaps` 用普通文字并报计数与步骤 id。
- [ ] T019 [P] [US3] [blockedBy: T017] [green: contracts/dispatch-payload.contract.md#C-1] [green: contracts/dispatch-payload.contract.md#C-2] [green: contracts/dispatch-payload.contract.md#C-3] [green: contracts/dispatch-payload.contract.md#C-4] [green: contracts/dispatch-payload.contract.md#C-5] 写 `skills/external/coaching-skills/SKILL.md` 的 § Dispatch Payload：必需字段（trainee 解析坐标、`<work>` 逐字、按 Trainee 自身 `SKILL.md` 执行的指示、结构化返回契约、异常行、派发时注入的快速失败条款、破坏性步骤转达），禁止字段（预期文件或 OC/PE 行、教练结论、教练改写的流程、运行目录内路径），一次一份且失败不重发，返回的异常行原样写入 DispatchRecord，传输方式记入 `mode`。

**Checkpoint**: US3 可独立验证——观测记录在缺通道时仍诚实（计数、不编造），载荷在字段层面无法被教练的预期污染。

---

## Phase 6: User Story 4 - 重命名后调用面与分发面一致，旧项目可平滑升级 (Priority: P2)

**Goal**: 八身份坐标、路由、活接线引用、派生面与冻结基线全部一致；旧目录名进入清理名册，升级后删实体目录、留用户自建的同名链接。

**Independent Test**: `tests/contract/test_coaching_wiring_contract.py` 全绿，并单独跑 1.1–1.4 的四条 shell 检查：lookup 来源为台账、台账与 probe 一致、派生面零漂移、闭集旧名恰一处。

### Tests for User Story 4 (MANDATORY)

- [ ] T020 [US4] [blockedBy: T004,T005,T006,T008] 红先行**创建** `tests/contract/test_coaching_wiring_contract.py`：按 `contracts/identity-and-wiring.contract.md` 的 C-1…C-8 为 SC-006 的**八个身份坐标**各写一条独立判定（① 目录存在/旧目录不存在、② frontmatter `name`、③ `skill_id` 与 Canonical ID/Path、④ unit id 的 `flow-class-check.py --action lookup` 解析、⑤ 台账行、⑥ probe 行与编译检查、⑦ 路由行与路径、⑧ description 触发词与两参数调用形态），并按坐标计数至 `8/8`（`coaching-skills` 被 `skill:coaching-skills` 包含时不重复计）；同时把残留审计的候选集实现为**运行时机械派生**——`MIRROR_PAIRS` 六对的源侧与镜像侧、`regen-command-copies.py` 实际扇出的逐工具副本目标、A10 中不经生成器的残余手改成员（`.qoder/agents`、probe 编译面 `## Wrap-up`、`.specify/memory/feedback/probe-map.md` 在测试内点名并各自独立断言），统一要求 `.qoder/agents`、`.specify/agents/templates`、`.specify/shared/definitions`、`.specify/memory/feedback/probe-map.md` 各面 0 命中、`src/specify_cli/__init__.py` 的 `_OBSOLETE_SKILLS` 条目恰 1 处；再断言 probe 编译零漂移、镜像与命令副本零漂移、四个冻结名册含新名，并用 `cleanup_obsolete_framework_assets` 在 `tmp_path` 上断言旧实体目录被删而同名用户符号链接保留（SC-007 的可执行形态）；真实失败记入 `.specify/specs/078-coaching-skills/notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T021 [US4] [blockedBy: T020] [green: contracts/identity-and-wiring.contract.md#C-1] 改 `templates/commands/skills.md` 的 modify 族路由行：目标改为 `skills/external/coaching-skills/SKILL.md`，条件文案改为教练意图（先给预期、再看真实执行、最后给微调），并写明调用形态 `coaching-skills <trainee-name|trainee-path> <work>`；五条路由行数不变，其余四行不动。
- [ ] T022 [US4] [blockedBy: T021] [green: contracts/identity-and-wiring.contract.md#C-2] 更新其余活接线引用：`agents/skill-verifier.agent.md` 与 `agents/structure-adjuster.agent.md` 的 `skills:` 列表；`skills/internal/create-agent/templates/agent-capacity-module-designer-template.md` 及同族另三份（requirements-analyst / system-designer / test-engineer）的 `skills:` 行**与**能力表描述行（把「心智模拟」语义改为教练闭环）；`skills/internal/run-skills/SKILL.md` 的 modify 族指针；`docs/reference/agents/command-and-skills.md` 与 `docs/tutorials/quickstart.md` 的两处——至此 A10 的 19 个手改源文件除四个测试外全部改完。
- [ ] T023 [US4] [blockedBy: T022] [green: contracts/identity-and-wiring.contract.md#C-3] 重生成派生面：`python3 scripts/python/sync-mirrors.py --write --only skills/external`、`--only shared`、`--only agents`；显式删除 `.specify/skills/think-skills`（`sync-mirrors.py` 不删 extras）；`python3 scripts/python/regen-command-copies.py` 扇出命令副本；`.venv/bin/specify render-agents --ai qoder` 重渲在场宿主 agents；再跑 `probe-utils.py --action compile-embeds` 与 `--action map` 重算 probe 派生面——全程不手改派生文件。
- [ ] T024 [US4] [blockedBy: T023] [green: contracts/identity-and-wiring.contract.md#C-4] 接通升级清理：在 `src/specify_cli/__init__.py` 的 `_OBSOLETE_SKILLS` 元组按字典序加入旧目录名条目，并把 OBSOLETE-ASSET-REGISTRY 区内那行历史注释改成不带旧名字面量的表述（保留改名链语义并指向 Feature 078）；`cleanup_obsolete_framework_assets` 删实体目录、跳过符号链接的既有语义不改。
- [ ] T025 [US4] [blockedBy: T024] [green: contracts/identity-and-wiring.contract.md#C-5] 核对路由与发现面一致：`templates/commands/skills.md` 仍为五行且 modify 族指向新路径、技能位于 `skills/external/coaching-skills` 且 `classification: external`、description 写明两参数调用形态；用 `python3 scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"` 确认 `source: ledger` / `execution` / `behavior-oracle`。
- [ ] T026 [US4] [blockedBy: T025] [green: contracts/identity-and-wiring.contract.md#C-6] 残留审计裁决（机械派生，不手写第五份清单）：运行 T020 创建的 `tests/contract/test_coaching_wiring_contract.py`，其候选路径集由三源在运行时合成——`scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 六对（源侧与镜像侧，含 `.specify/agents/templates`、`.specify/shared/definitions`）、`scripts/python/regen-command-copies.py` 实际扇出的逐工具命令副本目标、以及 A10 中不经任一生成器的残余手改成员（`.qoder/agents`、probe 编译面 `## Wrap-up`、`.specify/memory/feedback/probe-map.md`，在测试内以字面量钉住）；逐面读取判定：`.qoder/agents`、`.specify/agents/templates`、`.specify/shared/definitions`、`.specify/memory/feedback/probe-map.md` 各面旧名 0 命中，`src/specify_cli/__init__.py` 的 `_OBSOLETE_SKILLS` 条目恰 1 处；把测试输出与逐面读数记入 `.specify/specs/078-coaching-skills/notes/residual-audit.md` 供 T031 引用；`git grep -n` 只是诊断旁证，不是裁决；历史记录目录（`.specify/specs/**`、`memory/evidence/**`、`features/`、reviews、eval-baseline）不在面内，不改写。
- [ ] T027 [US4] [blockedBy: T026] [green: contracts/identity-and-wiring.contract.md#C-7] 显式更新四个冻结基线测试 `tests/contract/test_expression_compatibility.py`、`tests/contract/test_migration_distribution.py`、`tests/contract/test_skill_layer_visibility_guards.py`、`tests/contract/test_run_skills_wiring.py`：名册换新名并各带 2026-10-30 / Feature 078 的日期与理由注记，计数与目录实测一致（27 命令、52 技能 = 15 external + 37 internal、49 条 manifest 技能）；069a 的哈希清单不改写，改为从清单里找出磁盘上已不存在的唯一路径、映射到新路径并在新文件上重新断言内容标记，从而不重复写出旧名字面量（SC-006 只允许一处）。

**Checkpoint**: US4 可独立验证——四类派生面零漂移、闭集旧名恰一处、升级夹具证明「删实体目录、留用户符号链接」。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 把「真的跑过」留成证据，并把 SC 逐条收口。

- [ ] T028 [blockedBy: T027] 跑 quickstart 场景 1 / 3 / 5 并记录：`python3 scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"`、`--action check`（`matched=79`）、`probe-utils.py --action probes --validate`、`probe-utils.py --action compile-embeds --check`、`sync-mirrors.py --check`、`regen-command-copies.py --check`、`scan-confirmation-gates.py --summary`、`test ! -e .specify/skills/think-skills` 的真实输出，以及在一次性夹具目录里调用 `cleanup_obsolete_framework_assets` 验证「删实体目录、留同名符号链接」；连同场景 5 的清理步骤一并写入 `.specify/specs/078-coaching-skills/notes/quickstart-run.md`。
- [ ] T029 [blockedBy: T028] 跑 quickstart 场景 2 / 4 的教练闭环：以 `tests/fixtures/coaching/fixture-trainee` 为 Trainee 执行一次真实教练运行（优化置 `skipped`，不动 Trainee 文件），核对 `.specify/memory/coaching/<run-id>/` 下四产物齐备、`expectation.md` 早于第一次派发动作、主产物存在、观测记录每行带来源；再在 `.specify/.tmp/coaching-degraded/` 的一次性副本里让 `improve-skills` 两层都不可用，核对 `optimization: unavailable` 且 `run` 不为 `failed`；两次运行的真实输出与清理步骤追加进 `.specify/specs/078-coaching-skills/notes/quickstart-run.md`。
- [ ] T030 [blockedBy: T027] 新技能形态预算：对最终形态的 `skills/external/coaching-skills/SKILL.md` 跑 `python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/coaching-skills/SKILL.md --budget-tokens 5000`，判 `pass`（退出 0，可控正文 ≤ 5000 tokens），把命令、`≈N tokens / 预算 5000`、行数与 findings 逐条写入 `.specify/specs/078-coaching-skills/notes/skill-shape-after.md`；T001 采的是旧技能基线，只作前后对照，不能替代本行判定。
- [ ] T031 [blockedBy: T028,T029,T030] [green: contracts/identity-and-wiring.contract.md#C-8] 终局门禁与留档：依次跑 `validate-tasks.py`、`pre-analyze-check.py --stage tasks`、`decomposition-check.py --mode tasks`、`account-clause-coverage.py`、`contracts/identity-and-wiring.contract.md` C-8 列出的七条验证命令；确认门预算按**新增行**判定：先把 `BASE=<feature baseline commit>`（基线提交 SHA 与取法）记入 `verification.md` 的 SC-008 行，再跑 `git diff "$BASE" -- templates/commands skills shared 'templates/*.md' | grep '^+' | grep -v '^+++'`，逐新增行对照 `scripts/python/scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`（编译形态 `BLOCKING_RE`），要求 `blocking_hits=0` 且退出 0；同命令同 pattern 集的改动前基线读数（`test-evidence/gate-newline-baseline.txt`：`added_lines=0` / `blocking_hits=0`；`--summary`：`blocking=27` = destructive 20 + governance_kept 7，`violations=0`）与本次读数并列入证据，**不以新增前后总量相等为判据**；把全部真实输出贴入 `.specify/specs/078-coaching-skills/verification.md`，并为 SC-001…SC-009 各记一条状态行（无一条留空）。

**Checkpoint**: SC-001…SC-009 每条都有可复现的证据来源，`verification.md` 是它们的唯一索引；新技能形态的 `skill-shape.py` 读数在 `notes/skill-shape-after.md`，与 T001 的旧技能基线成对可对照。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，先做——T001 与 T002 都写 `notes/pre-change-measurements.md`，故串行。
- **Foundational (Phase 2)**: 依赖 Setup 完成；**阻塞全部故事**。T003 / T004 / T005 / T006 / T007 互不共享写目标，可并行；T008 依赖 T004 与 T006。
- **User Stories (Phase 3–6)**: 依赖 Foundational 完成；US1 与 US2 互不共享写目标（`SKILL.md` 与 `references/prompt-templates.md` 可分别推进），US3 与 US4 同理，故事之间按优先级串行即可。
- **Polish (Phase 7)**: 依赖全部故事完成。

### User Story Dependencies

- **US1 (P1)**: Foundational 之后可独立开工；不依赖 US2/US3/US4 的产物。
- **US2 (P1)**: Foundational 之后可独立开工；其正文写 `references/prompt-templates.md`，与 US1 的 `SKILL.md` 不同文件。
- **US3 (P2)**: Foundational 之后可独立开工；`SKILL.md` 的载荷段与 US1 的正文段同文件，故在 US1 之后落笔（同文件串行）。
- **US4 (P2)**: Foundational 之后可独立开工；它的四条 shell 判据与故事内容无关，可在 US1–US3 之前先跑起来。

### Within Each User Story

- 测试先写、先红、先留证；实现行随后让它转绿。
- 同一文件的多行按行序串行（`SKILL.md`、`references/prompt-templates.md` 各有多个写入行）。
- 每个故事在自己的 Checkpoint 处可独立验证，不靠后续故事补齐。

### Parallel Opportunities

- Foundational 的 T003 / T004 / T005 / T006 / T007 写目标互不相交。
- US3 的 T018（references）与 T019（`SKILL.md`）写目标不同，可并行；两者都依赖 T017。
- 本文件其余段落零 `[P]`：`notes/red-first-evidence.md` 是追加落点、`notes/quickstart-run.md` 是 T028 / T029 共用的追加落点、`SKILL.md` 与 `references/prompt-templates.md` 各被多行写入——共享 sink 与同文件即同写目标，按行序串行，不靠删路径消警。

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2（两个 P1 故事）。理由按模板的 MVP 规则：只有 US1 而没有 US2，预期落不成可判定的形状，闭环的「偏差」与「提升计划」无从谈起；两者合起来才是可独立交付的最小增量。

1. 完成 Phase 1 与 Phase 2（证据槽 + 新坐标）。
2. 完成 US1 与 US2，在每个 Checkpoint 独立验证。
3. **STOP and VALIDATE**: 跑定向集 `targeted-set-v1`，确认两个测试文件转绿且反例集判红。
4. 继续 US3、US4，最后 Phase 7 收口。

### Incremental Delivery

1. Foundational → 新名可被解析（`source: ledger`）、四产物目录已登记。
2. US1 + US2 → 闭环与双维度预期成立（MVP）。
3. US3 → 观测与载荷的诚实性成立。
4. US4 → 改名面收口、旧项目可升级。
5. Polish → 真实运行证据与 SC 收口。

---

## Notes

- [P] 只标在写目标不同、无未完依赖的行；共享追加落点（`notes/*.md`）与同文件多写行一律串行。
- `[green:]` 认领的是「把该条款转绿的那一行」；分区由 `account-clause-coverage.py` 计数（必须等于 38），WARN 不靠删标签消音。
- **PLAN-EDIT 声明（本阶段实际发生）**: `plan.md` § Mirror Obligations 与 `quickstart.md` § 1.2 把 probe 编译单元的改名预期写成「75 增至 76」；实测该引擎按目录名生成单元（52 技能 + 23 个带 Wrap-up 的命令 = 75），改名删一增一净变化 0。已在两处就地更正为 75 并保留 2026-10-30 的实测理由；分类=minor（事实订正，不改架构、范围、条款语义或任务拆分）。其余 plan 属主制品未被修改。
- **FR 车道缺口**: 五份契约正文不带 FR 引用组，`account-clause-coverage.py` 的 FR 车道读数为 0/29；FR→条款的映射目前只写在 `plan.md` § Phase 1。补引用组等于改写五份契约的每条条款，属 plan 属主制品的内容变更，本阶段不改写、如实记录，交 `/speckit.analyze` 裁定。
- **历史不改写**: `.specify/specs/**` 的既有特性、`memory/evidence/**`、`features/<ID>.md`、reviews、eval-baseline、按旧 unit id 归档的 run/feedback 记录都是 dated record，本文件任何行不得回填。
- **临时目录**: 只有 T029 需要一次性副本，落点 `.specify/.tmp/coaching-degraded/`（已被 `.specify/.gitignore` 的 `.tmp/` 规则匹配），用完即删。
