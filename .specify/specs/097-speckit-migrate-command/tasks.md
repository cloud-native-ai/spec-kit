# Tasks: /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态）

**Requirement ID**: 097
**Requirement Key**: 097-speckit-migrate-command
**Related Feature**: 024 Specification Workspace Versioning
**Input**: Design documents from `.specify/specs/097-speckit-migrate-command/`
**Prerequisites**: requirements.md (25 FR / 9 SC / 4 STR / 2 clarification sessions / A1–A11), plan.md (14 WPs, decision tensions T-001/T-002, execution premises EP-001…EP-006, mirror obligations), research.md (R-1…R-9), data-model.md (E-1…E-9, invariants I-1…I-5), contracts/ (3 files: migrate-cli C-1…C-7, migrate-engine C-1…C-8, migrate-template T-1…T-6), quickstart.md (scenarios 0–5), feature-ref.md (FR→WP matrix 25/25)

**Tests Mode**: ON — 宪法 Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则（纯函数 MUST 有单元测试、关键流程 MUST 有自动回归、集成/契约面 MUST 有契约测试），requirements FR-023…FR-025 亦要求可转红取证。类别读取（本阶段一次）：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:097-speckit-migrate-command"` → `flow_class: execution`，本阶段门禁集按该类别保持不变。

**Tests**: MANDATORY。每条红先测试在被测行为实现前先跑红，红先读数（命令、真实输出、退出码）逐条落入 `.specify/specs/097-speckit-migrate-command/notes/red-first-evidence.md`；实现后的读数落入 `test-evidence/`。**模板切片补充口径（template-only gate）**：`templates/commands/migrate.md` 与其四个副本是非运行期资产，其断言是**结构契约测试**（字面量、frontmatter、装配面、镜像一致性），不是对服务的单元测试；运行期段（CLI 子命令、规划器、执行器、回执）仍是逐行为红先测试，两者叠加而非互替。迁移/回归例外：本特性无「移植既有行为」的测试行，全部测试行为新，故无 `[blockedBy:]` 后置的迁移型测试。

**Concurrency reading**: requested=1, effective=1, effective_reason=`single-unit` — 本阶段可表示工作单元只有「写出 tasks.md 一份」，无可并发单元（事实码 `single-unit`，owner: `.specify/shared/declarations/facts/serial-reason.yaml`；读数三元组 owner: `.specify/shared/declarations/facts/effective-concurrency.yaml`）。

**Organization**: 按 requirements.md 的四个用户故事分组（US1 P1 / US2 P1 / US3 P2 / US4 P2），前置 Setup 与 Foundational，收尾 Polish。两个 P1 故事共同构成 MVP（见 § Implementation Strategy）。

## Phase Map

| Phase | Purpose | Rows | Stories / criteria |
|-------|---------|------|--------------------|
| 1 Setup | 固化基线、建立取证落点、探测环境 | T001–T004 | all |
| 2 Foundational | 差异模型、回执存储、工作区形态与参照树、init 决策函数、引擎契约守卫 | T005–T013 | blocks US1–US4 |
| 3 US1 | 安装后一次性收尾：干跑计划 → 应用收敛 → 再跑 clean | T014–T022 | US1, SC-001 / SC-003 |
| 4 US2 | 安全收尾：双键确认、归档可找回、冲突拒绝、用户内容保护 | T023–T028 | US2, SC-002 / SC-005 / SC-008 |
| 5 US3 | 跨版本一次直达、中断续跑 | T029–T032 | US3, SC-004 / SC-006 |
| 6 US4 | `/speckit.migrate` 模板、四副本、命令文档、分发基线、等价性 | T033–T040 | US4, SC-009 |
| 7 Polish | sanitize lane 定位、目录登记、quickstart 实测、终检 | T041–T048 | cross-cutting |

**Row count**: 48 rows, `T001`…`T048`, one ID per row, no gaps, contiguous in execution order.

## Definition of Done (DoD)

- DoD-1: **FR lane** — FR-001…FR-025 每一条都在至少一条任务行的文本中被点名（`grep -E '^- \[[ xX>~]\] T[0-9]{3} ' .specify/specs/097-speckit-migrate-command/tasks.md | grep -oE 'FR-0[0-9]{2}' | sort -u | wc -l` 返回 25），且 § FR/SC → row traceability 给出映射。Check: 该命令输出 `25`，任务行 48；红判据按 FR 判定——删除任一 FR 在任务行中的全部行内引用后，该 FR 必须从去重集合消失、计数降为 24（2026-11-10 实测单点样例：仅删 T016 行内 FR-004 或仅删 T015 行内 FR-008，两者各为唯一引用，删除后计数均为 24；多点 FR 如 FR-001 由 T014、T016 两行点名，须删除两处才降为 24，单删一处计数不变属预期、不判红）。追溯表与 DoD 行文本不参与计数。
- DoD-2: **clause lane** — 采用**严格子集**分区：`contracts/migrate-cli.md` C-1…C-5 与 `contracts/migrate-engine.md` C-1…C-4/C-6/C-7 各由唯一一行以 `[green: <contract>#<clause>]` 声明（分区见 § Green Partition）；未声明条款仍由点名它们的测试行文本钉住，机器上可缺席（owner: `.specify/skills/internal/create-tasks/SKILL.md` § Green）；`contracts/migrate-template.md` 的 T-1…T-6 **不是机器可判条款形态**（clause extractor 只读 `C-*`，该文件被判 `md-none` 具名），改由 T033/T034/T039 的断言钉住。Check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/097-speckit-migrate-command/tasks.md` 退出 0 且 `green-dangling` / `green-clause-collision` / `green-cross-phase` / `green-path-divergence` 全为 0。
- DoD-3: **no second engine** — migrate 段内不存在第二份路径改写正则、第二份命令渲染、第二份链接名单、第二份镜像对名单、第二份退役清单。判别力由 `tests/contract/test_migrate_engine_contract.py` 的测试内注入变异证明：五类源码守卫先钉住非空的 migrate 段、对真实源判 clean；每类守卫另对一份合成第二实现（测试内构造的源文本）判违例——某类注入未被抓出（守卫失效）或真实源含第二实现（实现漂移）均使套件转红。Check: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_engine_contract.py -q` 退出 0（clean 断言与五类注入变异断言在同一次套件运行中执行，读数随 T046 的 `test-evidence/final-suite.txt` 留档）。
- DoD-4: **archive-not-delete 靠测量而非声明** — US2 读数中每个被替换/移除对象的归档位置逐条存在，回执 `archives[]` 与 `recover` 可枚举。Check: T028 的 `test-evidence/us2-safety.txt` 含逐条存在性读数与四个变异结果。
- DoD-5: **分发完整** — 源模板、四个副本、命令文档与 `COMMAND_BASELINE` 30 全部落地，`regen-command-copies.py --check` 退出 0。Check: GATE-2 与 T040 读数。
- DoD-6: **镜像无 NEW drift** — 本特性触及的两个镜像对相对 R-8 基线无 NEW drift。Check: GATE-3。
- DoD-7: **final 路径判据全部通过且有 smoke 记录** — SC-001 / SC-002 / SC-003 / SC-004（`requirements.md` 的 `**Path**: final` 标记为唯一 roster）在 `verification.md` 中均为 `pass`，且 smoke 记录齐全。Check: GATE-4。
- DoD-8: **零写入与确定性靠测量** — 干跑前后树哈希不变、重复干跑逐字节相同、apply 后重跑 clean 且零写入。Check: T022 的 `test-evidence/us1-converge.txt`。
- DoD-9: **quickstart 真实执行** — 场景 1–5 以仓库源码调用形态真实执行并粘贴输出与退出码到 `notes/quickstart-run.md`。Check: T045 记录非空且逐场景含退出码。
- DoD-10: **零未完成行** — 无 `[ ]` / `[>]` 行残留。Check: GATE-5。

**DoD Status**: pending

## Completion Gate

- GATE-1: 本特性契约/集成/单元子集全绿且相对记录基线零 NEW failure — check: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_cli_surface.py tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/contract/test_migration_distribution.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/integration/test_migrate_us1_converge.py tests/integration/test_migrate_us2_safety.py tests/integration/test_migrate_us3_crossversion.py tests/integration/test_migrate_us4_equivalence.py -q` 退出 0，且 T046 记录中的失败名集合相对实现入口基线无新增。
- GATE-2: 分发基线同步 — check: `bash scripts/bash/run-tests.sh tests/contract/test_migration_distribution.py -q` 退出 0（`COMMAND_BASELINE` 含 `migrate` 且长度 30），`python3 scripts/python/regen-command-copies.py --check` 退出 0。
- GATE-3: 镜像义务成立 — check: `python3 scripts/python/sync-mirrors.py --check` 相对 R-8 基线无 NEW drift，`python3 scripts/python/regen-command-copies.py --check` 退出 0。
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/097-speckit-migrate-command/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present. A `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema; carrier name per constitution VII (`verification.md`).
- GATE-5: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\] T[0-9]{3} ' .specify/specs/097-speckit-migrate-command/tasks.md` returns 0.
- GATE-6: 结构校验通过 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/097-speckit-migrate-command/tasks.md` 退出 0，0 error(s)，且每个 WARN 均在 § Notes 中被裁定。

## Environment Prerequisites

Probed 2026-11-10 in this worktree (branch `097-speckit-migrate-command`, base `96df5d2f5`). Every row that depends on one of these verdicts references THIS section instead of restating it; re-probe at implement entry, never cached across runs.

- CPython interpreter: **available** — probe: `python3 --version` @ 2026-11-10 → `Python 3.11.11`; `pyproject.toml` declares `requires-python >=3.8`; affected rows: every engine row T008–T032.
- `pytest` runner: **available** — probe: `python3 -m pytest --version` @ 2026-11-10 → `pytest 8.4.2`; affected rows: every test row and GATE-1.
- Test entry `scripts/bash/run-tests.sh`: **available** — probe: file present and executable (`-rwx------ 12889 bytes`) @ 2026-11-10, and the plan's one-test smoke `bash scripts/bash/run-tests.sh tests/contract/test_anchor_layout_migrate.py -q` → 3 passed; affected rows: T022, T028, T032, T040, T046, GATE-1.
- Symlink creation: **available** — probe: `ln -s target /tmp/migrate-probe-link-$$ && rm -f /tmp/migrate-probe-link-$$` @ 2026-11-10 → `symlink-ok`; affected rows: T020 (link creation), T026 (the platform-degrade refusal is exercised here by simulation, not by an unsupported host).
- Installed `specify` CLI: **partial** — probe: `python3 -c "import specify_cli; print(specify_cli.__file__)"` @ 2026-11-10 → `/usr/local/lib/python3.11/site-packages/specify_cli/__init__.py` (released 0.0.22, not the repository source); affected row: T045, which therefore invokes the repository source with `PYTHONPATH=src python3 -c "import sys; sys.argv=['specify', ...]; from specify_cli import main; main()"` (probe verified exit 0 @ 2026-11-10) and records the substitution.
- Network / container runtime / daemon: **not required** — probe: plan Technical Context states zero network and every fixture builds under a temp dir @ 2026-11-10; affected rows: none.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其他 `[P]` 行并行 —— 写目标不同、不依赖未完成行。
- **[Story]**: `US1`…`US4`，只出现在用户故事阶段；Setup / Foundational / Polish 行**零** `[US` 标记。
- **[blockedBy: Txxx,Tyyy]**: 真实依赖；无标签的行只受阶段顺序约束。
- **[green: <contract>#<clause>]**: 本行是让该条款转绿的行；同一子句只由一行声明（§ Green Partition）。
- 一行一任务：整行（复选框、ID、标签、描述、路径）必须保持同一行，禁止续行。
- **Verification rows**: T022 / T028 / T032 / T040 / T045 / T046 / T048 是显式验证行，各自写独立证据文件。

### Task State Sigil

`- [ ]` open · `- [>]` claimed（多代理）· `- [X]` closed · `- [~]` deferred（行内 `<!-- deferred: reason -->` 承载原因，宪法 VII；`deferred_tasks=` 汇总索引可另记但不替代行内标记）。

## Path Conventions

两顶帽子（plan.md § Structure Decision、§ Mirror Obligations）：`scripts/`、`shared/`、`skills/`、`templates/`、`tests/`、`src/` 是**框架源**；`.specify/scripts/`、`.specify/shared/`、`.specify/skills/` 是它们的运行期投影，只由 `scripts/python/sync-mirrors.py` 生成，永不手改。`.specify/templates/commands/` 已退役，命令模板只经 `scripts/python/regen-command-copies.py` 投影到四个工具副本树。全部路径为仓库相对路径。

运行时证据落点（固定，不逐轮重造）：`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`notes/pre-change-measurements.md`、`test-evidence/`、`coverage-baseline.txt`。失败测试名基线列表的路径、抓取旗标与名称级比较形态由 `/speckit.implement` step 6 的 `**Test runs**` bullet 单一拥有；本文件只按路径指向，不复述。

### Premises measured at generation time (2026-11-10)

| Quantity | Measured | Re-derivation (actually run) | Naive form that disagrees |
|---|---|---|---|
| Command templates | **29** | `ls templates/commands/*.md \| wc -l` → `29` | `ls templates/commands \| wc -l` counts any non-`.md` entry that later lands; the glob is the unit |
| Per-tool copies | **29 each** (4 trees) | `.github/prompts/*.prompt.md` → 29; `.claude/commands/speckit.*.md` → 29; `.qoder/commands/speckit.*.md` → 29; `.opencode/command/speckit.*.md` → 29 | a bare `ls <dir> \| wc -l` also counts non-specify files |
| Command docs | **27** | `ls docs/reference/commands/*.md \| wc -l` → `27` | — |
| `COMMAND_BASELINE` | **29** | `grep -n "assert len(COMMAND_BASELINE)" tests/contract/test_migration_distribution.py` → line 127 `== 29` | — |
| Obsolete registry | **34 / 16 / 4 / 27** | AST `literal_eval` of `_OBSOLETE_SKILLS` / `_OBSOLETE_SKILL_FILES` / `_OBSOLETE_COMMANDS` / `_OBSOLETE_TEMPLATES` in `src/specify_cli/__init__.py` → 34 / 16 / 4 / 27 | `grep -c` on the block also counts comment lines and continuation commas |
| FR definitions | **25** | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/097-speckit-migrate-command/requirements.md` → `25` | counting every `FR-0` mention also counts cross-references inside other FRs |
| SC definitions | **9** | `grep -cE '^- \*\*SC-[0-9]{3}\*\*' .specify/specs/097-speckit-migrate-command/requirements.md` → `9` | a prose SC mention is not a definition |
| Contract clauses | **cli 7 / engine 8 / template 6** | `grep -cE '^## C-[0-9]+' contracts/migrate-cli.md` → 7; same on `contracts/migrate-engine.md` → 8; `grep -cE '^## T-[0-9]+' contracts/migrate-template.md` → 6 | counting all `C-` mentions includes cross-references; and `T-*` is **not** a machine-decidable clause form — the clause extractor reads `C-*` only, so `migrate-template.md` is `md-none` |
| Work packages | **14** | plan.md § Work Packages table WP01–WP14 | — |
| Coverage baseline frozen | **640 names** (642 lines = 2 header + 640 names); `base-sha 96df5d2f56b8` | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command --freeze > .specify/specs/097-speckit-migrate-command/coverage-baseline.txt` @ 2026-11-10 | the pre-freeze run read `baseline holds 0 names` — an absent baseline is not an empty exemption list; and the freeze excludes this spec's own contracts by design, so its 15 `C-*` clause names are the live delta contributors until their `[green:]` claims land |
| Live accountant reading at freeze time | claimed clauses **0** (tasks.md absent), uncovered **655**, own `C-*` clauses **15** (7 + 8) | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command` @ 2026-11-10 → `655 uncovered, 640 baseline names, 15 beyond` | reading the 15 as "other features' drift": they are exactly this spec's 7+8 clauses |

## Package Map (implement-stage dispatch boundary)

**Concurrency rules** (owner: `skills/external/sdd-loop-driver/references/decomposition-model.md`; this section states the partition, not the scheduler's rules): per-package ceiling **16 rows**; packages with intersecting write domains run serially with a declared reason code; read-only/evidence packages may overlap write packages. Row-level `[blockedBy:]` remains the ordering authority inside a package; the edges below order packages.

| Package | Rows | Count | Write domain (owned paths) | Edge (blockedBy) |
|---------|------|-------|----------------------------|------------------|
| `pkg01-setup` | T001–T004 | 4 | `.specify/specs/097-speckit-migrate-command/notes/`, `.specify/specs/097-speckit-migrate-command/test-evidence/`, `coverage-baseline.txt` | none (entry) |
| `pkg02-foundation` | T005–T013 | 9 | `src/specify_cli/__init__.py` (data model / receipt / workspace-kind / reference-tree / decision-function sections), `tests/unit/test_migrate_planner.py`, `tests/unit/test_migrate_receipts.py`, `tests/fixtures/migrate-097/builders.py`, `tests/contract/test_migrate_engine_contract.py` | `pkg01-setup` |
| `pkg03-us1-engine` | T014–T022 | 9 | `src/specify_cli/__init__.py` (subcommand / planner / executor / wiring sections), `tests/contract/test_migrate_cli_surface.py`, `tests/integration/test_migrate_us1_converge.py`, `test-evidence/us1-converge.txt` | `pkg02-foundation` |
| `pkg04-us2-safety` | T023–T028 | 6 | `src/specify_cli/__init__.py` (safety / archive / refusal sections), `tests/integration/test_migrate_us2_safety.py`, `test-evidence/us2-safety.txt` | `pkg03-us1-engine` |
| `pkg05-us3-crossversion` | T029–T032 | 4 | `src/specify_cli/__init__.py` (receipt version / resume sections), `tests/integration/test_migrate_us3_crossversion.py`, `test-evidence/us3-crossversion.txt` | `pkg04-us2-safety` |
| `pkg06-us4-template` | T033–T040 | 8 | `templates/commands/migrate.md`, `.github/prompts/speckit.migrate.prompt.md`, `.claude/commands/speckit.migrate.md`, `.qoder/commands/speckit.migrate.md`, `.opencode/command/speckit.migrate.md`, `docs/reference/commands/migrate.md`, `tests/contract/test_migrate_template.py`, `tests/contract/test_migrate_distribution_assembly.py`, `tests/contract/test_migration_distribution.py`, `tests/integration/test_migrate_us4_equivalence.py`, `test-evidence/us4-equivalence.txt` | `pkg03-us1-engine` (equivalence needs the CLI); disjoint files, authoring may overlap |
| `pkg07-polish` | T041–T048 | 8 | `skills/internal/sanitize-materials/SKILL.md`, `shared/definitions/framework-map.md`, `.specify/skills/internal/sanitize-materials/SKILL.md`, `.specify/shared/definitions/framework-map.md`, `notes/quickstart-run.md`, `test-evidence/final-suite.txt`, `test-evidence/mirror-verify.txt`, `verification.md` | `pkg05-us3-crossversion`, `pkg06-us4-template` |

**Partition check**: 4 + 9 + 9 + 6 + 4 + 8 + 8 = **48** rows, one row per ID, no ID in two packages; largest package 9 ≤ 16.

**Serialization disclosure**: `pkg02`–`pkg05` all write `src/specify_cli/__init__.py`; their write domains intersect, so dispatch runs them **serially** in integration order with reason code `write-conflict` (no isolation form declared — owner vocabulary: `.specify/shared/declarations/facts/serial-reason.yaml`). `pkg06` and `pkg07` own disjoint surfaces and may overlap the engine chain only after their declared edges. `[P]` markers inside a phase describe **test-authoring** parallelism only.

**Declared integration order**: `pkg01-setup → pkg02-foundation → pkg03-us1-engine → pkg04-us2-safety → pkg05-us3-crossversion → pkg06-us4-template → pkg07-polish`.

## Feature Integration Review

Reviewed at tasks generation (2026-11-10): `.specify/features.md` row 024 reads `Planned` with Spec Path `.specify/specs/097-speckit-migrate-command/requirements.md`, and `.specify/features/024-specification-workspace-versioning.md` is `Planned` with the plan-stage Key Changes already recorded. The task breakdown exposes **no new feature and invalidates none**: `specify migrate` stays inside 024's capability domain (cross-CLI-version `.specify/` workspace upgrade), and goal/team archive migration remains owned by `/speckit.goal` (`migrate-archive`). No registry edit is made in this stage; `Planned → Implemented` belongs to `/speckit.implement`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 固化后续所有比较所依赖的基线、建立证据落点、在实现入口预探环境。

- [X] T001 Create the runtime-evidence landing points for this feature: `.specify/specs/097-speckit-migrate-command/notes/red-first-evidence.md` with its per-entry skeleton (command, real output, exit status) and `.specify/specs/097-speckit-migrate-command/notes/pre-change-measurements.md` with its header, so every later row appends instead of inventing a path.
- [X] T002 Re-capture the command-surface baseline into `.specify/specs/097-speckit-migrate-command/notes/pre-change-measurements.md`: `ls templates/commands/*.md | wc -l` (29), the four copy trees (29 each), `ls docs/reference/commands/*.md | wc -l` (27) and the pinned `assert len(COMMAND_BASELINE) == 29` in `tests/contract/test_migration_distribution.py`; paste each real output with its capture date. [blockedBy: T001]
- [X] T003 Probe the environment at implement entry and write `.specify/specs/097-speckit-migrate-command/test-evidence/implement-env-probe.txt`: `python3 --version`, `python3 -m pytest --version`, the one-test smoke `bash scripts/bash/run-tests.sh tests/contract/test_anchor_layout_migrate.py -q`, a symlink creation under a temp root, and the installed-CLI origin reading (see § Environment Prerequisites @ 2026-11-10); record command lines, full output and exit codes. [blockedBy: T001]
- [X] T004 Freeze the contract-coverage baseline at this spec's first full-tree accounting into `.specify/specs/097-speckit-migrate-command/coverage-baseline.txt` with `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command --freeze > .specify/specs/097-speckit-migrate-command/coverage-baseline.txt` and record the readings in `notes/pre-change-measurements.md`; the implement-entry failing-test name list is captured in the form and at the path owned by `/speckit.implement` step 6's `**Test runs**` bullet (pointer, never restated). [blockedBy: T001]

**Checkpoint**: every later row names the baseline it is compared against, the evidence landing points exist, and the environment verdicts are recorded once in § Environment Prerequisites.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 差异模型、回执存储、工作区形态、参照树与 init 决策函数 —— 四个故事共同读取的核心。

**⚠️ CRITICAL**: 本阶段完成前，任何用户故事行不得开始。

- [X] T005 [P] Author `tests/unit/test_migrate_planner.py` red-first: the five dimension tokens and their fixed order come from data-model.md E-8, `(dimension, target)` dedup keeps exactly one item, a repeated dry-run on one tree is byte-identical, and `refuse` / `blocked` items always carry a non-empty reason naming both candidates or the missing second key respectively (FR-006, FR-014).
- [X] T006 [P] Author `tests/unit/test_migrate_receipts.py` red-first: run-id shape `YYYYMMDDTHHMMSSZ-<8 hex>`, one receipt file per run, two simulated concurrent writers land on distinct paths, `running` → `completed` transition, and a dry-run writes no receipt file (FR-017, FR-018).
- [X] T007 [P] Author `tests/fixtures/migrate-097/builders.py` with `build_latest_project` (init copy mechanism into a tmp dir), `build_legacy_project` (legacy anchor layout, `_OBSOLETE_SKILLS` flat dirs, `_OBSOLETE_COMMANDS` old copies, a flat internal duplicate, a missing compat symlink, one edited template file and one deleted script file) and `build_mixed_project`; every constructed name MUST be asserted present in its owner declaration or checker output (FR-023).
- [X] T008 Implement the DiffItem/Plan model in `src/specify_cli/__init__.py`: id = `sha1(dimension + "|" + target)[:12]`, the E-8 dimension tokens in their fixed order, stable `(dimension, target)` sort, dedup, and serialization for both text and json envelopes (FR-006, FR-007). [blockedBy: T005]
- [X] T009 Implement the receipt store in `src/specify_cli/__init__.py`: run-id generation, `.specify/memory/migrate/receipts/<run-id>.json` per run, `running` / `completed` transitions and per-item status updates, never touching another run's file (FR-017, FR-018). [blockedBy: T006]
- [X] T010 Implement workspace-kind detection and engine loading points in `src/specify_cli/__init__.py`: `framework-source` iff `skills/external/` is a directory (same guard as `check_legacy_install_residue`), client engines loaded from `get_resource_path()/scripts/python/`, framework-source engines from the workspace's own `.specify/scripts/python/`; no `.specify/version` marker and no source-version branch (FR-005, FR-020).
- [X] T011 Implement the client reference-tree builder in `src/specify_cli/__init__.py`: run `copy_local_templates` + `rewrite_paths` + `generate_commands` into `tempfile.TemporaryDirectory(prefix="specify-migrate-")`, probe tool command dirs from `_ASSISTANT_COMMAND_DIRS` and the script variant from existing copies, and clean up in `finally` (FR-005, FR-006, FR-007). [blockedBy: T010]
- [X] T012 Extract pure decision functions from `cleanup_obsolete_framework_assets` and `migrate_flat_internal_skills` in `src/specify_cli/__init__.py`, rewire the init call sites onto the same functions, and keep `tracker=None` supported (FR-009). [blockedBy: T008]
- [X] T013 Author `tests/contract/test_migrate_engine_contract.py` red-first: the five-dimension tokens and order read from E-8, the six-value disposition domain extracted byte-for-byte from requirements.md FR-014, the five source guards (no second path-rewrite regex, no second command renderer, no second link roster, no second mirror-pair roster, no second obsolete roster) implemented as callables over source text, pinned to a non-empty migrate segment, and each exercised by an in-test injection mutation (a synthetic second implementation per guard class MUST be reported as a violation; silence fails the suite), and init↔migrate decision equivalence on one fixture (FR-009, FR-010, FR-014). [blockedBy: T012] [green: contracts/migrate-engine.md#C-1] [green: contracts/migrate-engine.md#C-2] [green: contracts/migrate-engine.md#C-3]

**Checkpoint**: the shared model, receipt store, workspace-kind resolution and decision functions exist; every story can now build on them.

---

## Phase 3: User Story 1 — 安装后的一次性收尾 (Priority: P1) 🎯 MVP

**Goal**: 用户运行 `specify migrate` 得到逐项差异计划（零写入），以 `--apply` 收敛到当前安装版本的期望态，再次运行得到 clean 计划。

**Independent Test**: 用携带旧布局与历史残留的合成夹具，先干跑、后应用，断言收敛后逐项零差异、应用前干跑零写入、应用后第二次运行零写入。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试，确认它们在被测实现出现前失败，红先读数落入 `notes/red-first-evidence.md`。**

- [X] T014 [P] [US1] Author `tests/contract/test_migrate_cli_surface.py` red-first: the closed option set (`--dry-run` default, `--apply`, `--workspace PATH`, `--format text|json`), `--apply --dry-run` together exits 2, undeclared options exit 2, `--help` answers with zero side effects and declares the four outcomes with their exit codes, a missing `.specify/` exits 2 naming `specify init`, the outcome→exit mapping matches C-3, the json envelope carries the C-4 keys, and `--yes` / `--force` / `--non-interactive` each exit 2 (FR-001, FR-003, FR-019, FR-022). [green: contracts/migrate-cli.md#C-1] [green: contracts/migrate-cli.md#C-2] [green: contracts/migrate-cli.md#C-3]
- [X] T015 [P] [US1] Author `tests/integration/test_migrate_us1_converge.py` red-first: the latest fixture dry-run reports `clean` exit 0 with an unchanged tree hash, the legacy fixture dry-run reports `planned` exit 1 with an unchanged tree hash and at least one item in every dimension, apply under a simulated interactive confirmation converges every item, a second run reports `clean` exit 0 with zero writes, every plan and receipt carries the E-9 goal/team static pointer and zero goal/team items, and removing one dimension's disposition mutation makes the suite red (FR-006, FR-008, FR-013, FR-023, FR-025). [blockedBy: T007] [green: contracts/migrate-cli.md#C-4] [green: contracts/migrate-engine.md#C-4]

### Implementation for User Story 1

- [X] T016 [US1] Implement the `specify migrate` subcommand surface in `src/specify_cli/__init__.py`: module-level `@app.command()` function, the four options with `--dry-run` as the default, the `.specify/` precondition naming `specify init` as the repair entry, the outcome→exit-code table, the text and json envelopes, and boundary text stating this command performs neither install nor init (FR-001, FR-003, FR-004, FR-019, FR-022). [blockedBy: T014]
- [X] T017 [US1] Implement the planner's `migration-residue` and `compat-links` dimensions in `src/specify_cli/__init__.py`: import the sanitize-utils checkers in-process (`check_legacy_install_residue`, `check_flat_internal_duplicates`, `check_broken_symlinks`; never `--action collect`), take the link roster only from `COMPAT_SYMLINKS` / `COMPAT_SYMLINK_EXPECTATIONS`, and map findings to `archive` / `relocate` / `write` / `replace` / `refuse` (FR-007, FR-010, FR-014). [blockedBy: T008,T011]
- [X] T018 [US1] Implement the planner's `templates-generated` and `mirror-consistency` dimensions in `src/specify_cli/__init__.py`: client mode compares the reference tree against `.specify/templates` (minus commands), `.specify/skills`, `.specify/agents/templates`, `.specify/scripts`, `.specify/shared` and each detected tool command dir; framework-source mode delegates to `sync-mirrors.py --check` and `regen-command-copies.py --check` and parses `MISS` / `DIFF` / `ORPHAN` (FR-005, FR-007, FR-021). [blockedBy: T017]
- [X] T019 [US1] Implement the planner's `anchor-layout` dimension and the E-9 static pointer in `src/specify_cli/__init__.py`: delegate the check to `anchor-layout-migrate.py --action check`, map `move` to archive/relocate and `refuse-existing-target` to `refuse`, and emit the goal/team `migrate-archive` pointer on every plan and receipt (FR-007, FR-011, FR-013). [blockedBy: T018]
- [X] T020 [US1] Implement the executor write paths in `src/specify_cli/__init__.py`: `write` / `replace` / `archive` / `relocate` mechanisms, archive layout `.specify/archive/migrate/<run-id>/<rel>`, anchor-engine `--action apply` delegation, flat-internal relocation, compat-link creation and framework-source mirror writes via `sync-mirrors.py --write --only <pair>` (FR-009, FR-011, FR-014, FR-016). [blockedBy: T019,T012]
- [X] T021 [US1] Implement mode wiring, outcome computation and receipt emission in `src/specify_cli/__init__.py`: connect the subcommand to planner and executor, compute `clean` / `planned` / `applied` with their exit codes, write the receipt `.specify/memory/migrate/receipts/<run-id>.json` on apply (`running` then `completed`), and keep dry-run output-only with zero writes (FR-006, FR-017, FR-018, FR-019). [blockedBy: T020,T016,T009]
- [X] T022 [US1] Run the US1 suites via `bash scripts/bash/run-tests.sh tests/contract/test_migrate_cli_surface.py tests/integration/test_migrate_us1_converge.py -q` and record the readings into `.specify/specs/097-speckit-migrate-command/test-evidence/us1-converge.txt`: verdicts, zero-write tree hashes, per-dimension item counts, and the remove-one-disposition mutation result (SC-001, SC-003). [blockedBy: T021,T015]

**Checkpoint**: US1 works on its own — a legacy fixture converges in one dry-run → apply → re-run cycle with zero writes in both dry-runs.

---

## Phase 4: User Story 2 — 安全收尾：不可逆动作有确认门、数据可找回 (Priority: P1)

**Goal**: 凡删除、移动、覆盖，先归档、留回执、可找回；破坏性动作必须显式确认，无交互环境下宁可 blocked 也不自动批准；目标冲突时命令停住并指名双方。

**Independent Test**: 构造含用户手改文件与目标冲突的夹具，断言未确认时破坏性处置零执行、确认后被替换与归档对象均可找回、冲突时拒绝覆盖并指名双方。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T023 [US2] Author `tests/integration/test_migrate_us2_safety.py` red-first: a non-interactive apply marks every destructive item `blocked` and executes none (exit 3), the interactive single-batch confirmation executes them, every replaced/archived object exists at its receipt-named archive path, the conflict fixture refuses and names both candidates, user skills and hand-edited files stay byte-identical, and four mutations turn the file red (remove the confirmation gate; remove the archive step; inject full-delete; weaken the assertion to existence-only) (FR-015, FR-016, FR-024). [blockedBy: T007] [green: contracts/migrate-cli.md#C-5] [green: contracts/migrate-engine.md#C-6]

### Implementation for User Story 2

- [X] T024 [US2] Implement the disposition classifier and destructive-bucket gate in `src/specify_cli/__init__.py`: classify each item against the destructive criteria by pointer to `.specify/shared/guidelines/confirmation-gates.md`, implement the dual key (`--apply` enters write mode; one single-batch interactive confirmation), and make non-interactive destructive items `blocked` with no prompt and no non-interactive flag (FR-014, FR-015). [blockedBy: T021]
- [X] T025 [US2] Implement archive-not-delete enforcement and recovery enumeration in `src/specify_cli/__init__.py`: every replace/remove first moves the object under `.specify/archive/migrate/<run-id>/<rel>`, each receipt records `archives[]` with `change` and `digest`, and `recover` names one recovery path per entry (FR-016, FR-017, FR-018). [blockedBy: T024]
- [X] T026 [US2] Implement conflict refusal and platform degradation in `src/specify_cli/__init__.py`: a non-equivalent existing target yields `refuse` naming both candidate paths and never picks a winner, and a host without symlink support yields a `refuse` item with reason `platform-no-symlink` instead of a crash (FR-014, FR-016). [blockedBy: T024]
- [X] T027 [US2] Implement user-content protection in `src/specify_cli/__init__.py`: user-built skills, project-specific extensions, `site/` data, `.specify/memory/**` and hand-edited framework files are never residue candidates, and any replacement archives the old content first (FR-016). [blockedBy: T025]
- [X] T028 [US2] Run the US2 suite via `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us2_safety.py -q` and record the readings into `.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt`: blocked-run exit codes, per-archive existence checks, conflict readings, byte hashes and all four mutation results (SC-002, SC-005, SC-008). [blockedBy: T027,T026,T023]

**Checkpoint**: US1 and US2 work independently — convergence is trustworthy because every destructive action is gated and recoverable.

---

## Phase 5: User Story 3 — 跨版本一次直达，中断可续跑 (Priority: P2)

**Goal**: 落后多个版本的项目一次 migrate 收敛到当前期望态；应用中断后第二次运行从回执续做，不重复搬移已归档对象。

**Independent Test**: 用模拟 N→N+k 的多代残留夹具一次收敛；在「已归档、未写目标」处中断，第二次运行完成收尾且不二次搬移。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T029 [US3] Author `tests/integration/test_migrate_us3_crossversion.py` red-first: a multi-generation fixture (two or more legacy generations built by the same declaration-driven builders) converges in one run, the receipt records source and target versions, no intermediate-version step exists, and an interruption fixture (object archived, target missing, `status=running` receipt left) makes the second run report the interrupted stage, complete the write, and leave the archived object un-moved (counting + existence assertions); a re-move mutation turns it red (FR-017, FR-020, FR-025). [blockedBy: T007] [green: contracts/migrate-engine.md#C-7]

### Implementation for User Story 3

- [X] T030 [US3] Implement receipt source/target version recording in `src/specify_cli/__init__.py`: read `.specify/source.json` with the `unavailable` + reason fallback, record the CLI version and framework commit, and keep all of it record-only so no disposition reads it (FR-020). [blockedBy: T021]
- [X] T031 [US3] Implement the resume path in `src/specify_cli/__init__.py`: scan this workspace's receipts for the nearest `status=running` record, report the interrupted stage in `notes` and `resumedFrom`, judge each item from that old receipt's own `items[].status` and `archives[]` `archiveTo`, never re-move an archived object, and open new archives only for items the old receipt did not cover (FR-017). [blockedBy: T030]
- [X] T032 [US3] Run the US3 suite via `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us3_crossversion.py -q` and record the readings into `.specify/specs/097-speckit-migrate-command/test-evidence/us3-crossversion.txt`: one-run convergence, source/target fields, interruption reproduction, archive counts and the re-move mutation result (SC-004, SC-006). [blockedBy: T031,T029]

**Checkpoint**: US3 works independently — a far-behind project converges in one run, and an interrupted apply resumes without double-moving.

---

## Phase 6: User Story 4 — 代理会话与 CLI 走同一引擎 (Priority: P2)

**Goal**: 用户在代理会话中用 `/speckit.migrate` 完成同样的收尾：模板驱动同一确定性引擎，计划与结果和 CLI 一致；模板不复制任何检查或处置逻辑。

**Independent Test**: 同一夹具上比较两个入口的干跑计划，断言逐项一致；结构测试断言模板只委派、不复制实现。

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T033 [P] [US4] Author `tests/contract/test_migrate_template.py`: `templates/commands/migrate.md` carries the two-key frontmatter, contains the literals `specify migrate` and `specify migrate --apply`, contains none of `check_`, `sanitize-utils`, `anchor-layout-migrate`, `sync-mirrors`, `regen-command-copies`, `_OBSOLETE_`, and no inspection code fence; the Qoder copy's frontmatter stays covered by the generic contract test see `tests/contract/test_qoder_command_frontmatter.py` (FR-002, FR-022).
- [X] T034 [P] [US4] Author `tests/integration/test_migrate_us4_equivalence.py`: extract the declared commands from the template, run both entries on one fixture, assert the deterministic `items` + `summary` parts are identical, assert apply produces the same `outcome` and per-item `disposition` / `status`, and assert neither entry leaves extra files; a template that inlines a check mutation turns it red (FR-002, FR-025). [blockedBy: T021]

### Implementation for User Story 4

- [X] T035 [US4] Author `templates/commands/migrate.md` as a thin projection: `## User Input`, `## Glossary` pointer, `## Delegation` (dry-run first via `specify migrate [--format json]`, apply only via `specify migrate --apply` after presenting the plan and obtaining consent), `## Handoffs`, and verbatim restatement of the four outcomes and their exit codes with receipt/archive pointers (FR-002, FR-021, FR-022). [blockedBy: T033]
- [X] T036 [US4] Regenerate the four per-tool copies from the source template with `python3 scripts/python/regen-command-copies.py`: `.github/prompts/speckit.migrate.prompt.md`, `.claude/commands/speckit.migrate.md`, `.qoder/commands/speckit.migrate.md`, `.opencode/command/speckit.migrate.md`; no copy may be hand-written (FR-021). [blockedBy: T035]
- [X] T037 [US4] Author `docs/reference/commands/migrate.md`: execution flow, the four options, the outcome/exit-code table, the receipt `.specify/memory/migrate/receipts/<run-id>.json` and archive `.specify/archive/migrate/<run-id>/` landing points, and the boundary against `specify init` and `/speckit.sanitize` (FR-021). [blockedBy: T035]
- [X] T038 [US4] Update `tests/contract/test_migration_distribution.py`: add `migrate` to `COMMAND_BASELINE` and change the pinned `assert len(COMMAND_BASELINE) == 29` to `== 30` (FR-021). [blockedBy: T036]
- [X] T039 [US4] Author `tests/contract/test_migrate_distribution_assembly.py`: source template present with its frontmatter, all four copies carry the `AUTO-GENERATED` marker naming the source template, the Qoder copy's `description` comes from `short-description`, `docs/reference/commands/migrate.md` exists, `COMMAND_BASELINE` contains `migrate`, `.specify/templates/commands/migrate.md` is absent (retired face), and `regen-command-copies.py --check` exits 0 (FR-021, SC-009). [blockedBy: T036,T037,T038]
- [X] T040 [US4] Run the US4 suites via `bash scripts/bash/run-tests.sh tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/integration/test_migrate_us4_equivalence.py -q` and record the readings into `.specify/specs/097-speckit-migrate-command/test-evidence/us4-equivalence.txt` (SC-009). [blockedBy: T039,T034]

**Checkpoint**: both entries produce the same plan and the same apply result on one fixture; the template contains delegation only.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 职责边界声明、目录登记、两个镜像对的写-验配对、quickstart 实测与终检。

- [ ] T041 [P] Update `skills/internal/sanitize-materials/SKILL.md` § Migration wrap-up lane: state that the one-shot closeout main entry is `/speckit.migrate` and that this lane stays as the periodic recheck fallback, keeping the checkers and dispositions unchanged (FR-012); its mirror pair see `.specify/skills/internal/sanitize-materials/SKILL.md` is synced in T042.
- [ ] T042 Sync the sanitize-lane mirror with `python3 scripts/python/sync-mirrors.py --write --only skills/internal/sanitize-materials`, writing `.specify/skills/internal/sanitize-materials/SKILL.md`, then verify `python3 scripts/python/sync-mirrors.py --check` reports no NEW drift versus the R-8 baseline and `diff -q` shows the pair identical (FR-012). [blockedBy: T041]
- [ ] T043 [P] Register the two runtime directories in `shared/definitions/framework-map.md`: a `Project memory` sub-row for `.specify/memory/migrate/receipts/` and an archive-family row for `.specify/archive/migrate/`, each with owner and per-run file shape (FR-018); its mirror pair see `.specify/shared/definitions/framework-map.md` is synced in T044.
- [ ] T044 Sync the framework-map mirror with `python3 scripts/python/sync-mirrors.py --write --only shared/definitions/framework-map.md`, writing `.specify/shared/definitions/framework-map.md`, then verify `--check` shows no NEW drift and `diff -q` shows the pair byte-identical (FR-018). [blockedBy: T043]
- [ ] T045 Run quickstart scenarios 1–5 end to end and record the real outputs into `.specify/specs/097-speckit-migrate-command/notes/quickstart-run.md`: invoke the repository source with `PYTHONPATH=src python3 -c "import sys; sys.argv=['specify', ...]; from specify_cli import main; main()"` because the installed CLI is the released package (see § Environment Prerequisites @ 2026-11-10); record command, output, exit code and teardown per scenario (FR-023). [blockedBy: T022,T028,T032,T040]
- [ ] T046 Run the feature's full subset via `bash scripts/bash/run-tests.sh tests/contract/test_migrate_cli_surface.py tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/contract/test_migration_distribution.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/integration/test_migrate_us1_converge.py tests/integration/test_migrate_us2_safety.py tests/integration/test_migrate_us3_crossversion.py tests/integration/test_migrate_us4_equivalence.py -q` and record the full output plus any NEW failure names versus the recorded baseline into `.specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt` (SC-001…SC-009). [blockedBy: T045]
- [ ] T047 Verify the mirror and copy obligations into `.specify/specs/097-speckit-migrate-command/test-evidence/mirror-verify.txt`: `python3 scripts/python/regen-command-copies.py --check` exits 0 and `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift against the R-8 baseline (FR-021). [blockedBy: T035,T042,T044]
- [ ] T048 Write `.specify/specs/097-speckit-migrate-command/verification.md` with one `SC-NNN_status=` line per criterion SC-001…SC-009, the smoke record (`smoke_command=`, `smoke_exit_code=0`, `smoke_evidence_path=`), the DoD readings and `deferred_tasks=` (FR-024, FR-025, GATE-4); the carrier name follows constitution VII (`verification.md`) and the framework chain that reads it (closure-acceptance-check.py REQUIRED_INPUTS); the carrier MUST be version-controlled — `git check-ignore -q <path>` MUST exit 1 (not ignored) before staging [blockedBy: T046,T047]

**Checkpoint**: the sanitize boundary is stated in its owner file, both runtime directories are registered, mirrors carry no NEW drift, quickstart is measured, and the closure record exists.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — can start immediately.
- **Foundational (Phase 2)**: depends on Setup — blocks US1–US4.
- **User Stories (Phase 3–6)**: US2, US3 and US4 all depend on US1's engine (the same `src/specify_cli/__init__.py` surface); within that constraint each story keeps its own independent checkpoint.
- **Polish (Phase 7)**: depends on every engine story and on US4's copies.

### User Story Dependencies

- **US1 (P1)**: starts after Foundational — the planner/executor core.
- **US2 (P1)**: starts after US1's wiring (T021) — adds the safety layer over the same executor.
- **US3 (P2)**: starts after US1's wiring (T021) — adds version recording and resume over the same receipt store.
- **US4 (P2)**: starts after US1's CLI (T021) — the template drives that CLI; its copy/doc rows write files disjoint from the engine.

### Within Each User Story

- Tests are authored first and MUST be red before the implementation rows that turn them green.
- Models before services before wiring; anchors engine and mirror engine are delegated, never re-implemented.
- A story's checkpoint is validated before the next story's implementation rows begin.

### Parallel Opportunities

- Phase 2: T005 ‖ T006 ‖ T007 (three distinct test/fixture files).
- Phase 3: T014 ‖ T015 (two distinct test files).
- Phase 6: T033 ‖ T034 (two distinct test files; T034 keeps its `[blockedBy:]`).
- Phase 7: T041 ‖ T043 (two distinct owner files; each mirror sync stays sequential behind its write row).
- Packages `pkg06` and `pkg07` write disjoint surfaces and may overlap the engine chain after their declared edges; `pkg02`–`pkg05` serialize on `src/specify_cli/__init__.py` (`write-conflict`).

## Parallel Example: User Story 1

```bash
# Two red-first test files, independent write targets:
Task: "Author tests/contract/test_migrate_cli_surface.py red-first"
Task: "Author tests/integration/test_migrate_us1_converge.py red-first"
```

## Implementation Strategy

### MVP First

US1 and US2 are both P1 and together form the smallest independently valuable increment: US1 alone converges a workspace, but requirements.md states that without recoverability and confirmation the command must not be released — convergence without the safety layer is not a deliverable. **MVP scope = US1 + US2 (Phases 1–4, T001–T028).** US3 and US4 are the P2 increments on top.

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (blocks all stories).
3. Complete US1 → validate its checkpoint.
4. Complete US2 → validate its checkpoint; the MVP set is now releasable.
5. Complete US3 and US4 → validate each checkpoint.
6. Complete Polish → run the Completion Gate.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 → a workspace converges (dry-run, apply, clean).
3. US2 → the same convergence is gated, archivable and conflict-safe (MVP released).
4. US3 → far-behind projects and interrupted runs are covered.
5. US4 → the agent-session entry reaches the same engine.
6. Polish → boundaries, directory registration, mirrors, quickstart evidence, closure.

## FR/SC → row traceability

| FR | Rows | SC | Rows |
|----|------|----|------|
| FR-001 | T014, T016 | SC-001 | T022 |
| FR-002 | T033, T034, T039 | SC-002 | T028 |
| FR-003 | T014, T016 | SC-003 | T022 |
| FR-004 | T016 | SC-004 | T032 |
| FR-005 | T010, T011, T018 | SC-005 | T028 |
| FR-006 | T005, T011, T015, T021 | SC-006 | T032 |
| FR-007 | T005, T008, T011, T017, T018, T019 | SC-007 | T015 |
| FR-008 | T015 | SC-008 | T028 |
| FR-009 | T012, T013, T020 | SC-009 | T038, T040 |
| FR-010 | T013, T017 | — | — |
| FR-011 | T019, T020 | — | — |
| FR-012 | T041, T042 | — | — |
| FR-013 | T015, T019 | — | — |
| FR-014 | T005, T013, T017, T020, T024, T026 | — | — |
| FR-015 | T023, T024 | — | — |
| FR-016 | T020, T023, T025, T026, T027 | — | — |
| FR-017 | T006, T021, T025, T029, T031 | — | — |
| FR-018 | T006, T009, T021, T025, T043, T044 | — | — |
| FR-019 | T014, T016, T021 | — | — |
| FR-020 | T010, T029, T030 | — | — |
| FR-021 | T018, T034, T035, T036, T037, T038, T047 | — | — |
| FR-022 | T014, T033, T034 | — | — |
| FR-023 | T007, T015, T045, T048 | — | — |
| FR-024 | T023, T048 | — | — |
| FR-025 | T015, T029, T039, T048 | — | — |

### Green Partition

| Contract | Claimed clauses | Row | Unclaimed (pinned by text, not machine-decidable this stage) |
|---|---|---|---|
| `contracts/migrate-cli.md` | C-1, C-2, C-3 | T014 | C-6, C-7 |
| `contracts/migrate-cli.md` | C-4 | T015 | — |
| `contracts/migrate-cli.md` | C-5 | T023 | — |
| `contracts/migrate-engine.md` | C-1, C-2, C-3 | T013 | — |
| `contracts/migrate-engine.md` | C-4 | T015 | C-5, C-8 |
| `contracts/migrate-engine.md` | C-6 | T023 | — |
| `contracts/migrate-engine.md` | C-7 | T029 | — |
| `contracts/migrate-template.md` | none | — | T-1…T-6 (the file is `md-none`: `T-*` is not a machine-decidable clause form; pinned by T033 / T034 / T039) |

## Notes

- **Disclosure — accountant FR-citation lane reads 4/25 at generation**: the three contracts cite FRs in prose headers rather than per-clause citation groups (owner form: `shared/definitions/contract-clause-definitions.md` § 引用组), so `account-clause-coverage.py` cannot read 21 of 25 FRs from citation groups. This is a contracts-side finding for `/speckit.analyze`; it is deliberately **not** turned into a gate here, and the contracts are not edited in this stage.
- **Disclosure — strict-subset green partition**: 11 of this spec's 15 machine-decidable `C-*` clauses are claimed; the four unclaimed (`migrate-cli` C-6/C-7, `migrate-engine` C-5/C-8) stay pinned by the test rows that assert them in prose. The contractor's live delta therefore reads 4 own clauses beyond the frozen baseline until a later stage claims or re-freezes; the freeze itself (`coverage-baseline.txt`, 640 names) is this stage's artifact.
- **Disclosure — `migrate-template.md` is `md-none`**: `T-1`…`T-6` are not extracted by the clause extractor, so no `[green:]` claim is made there; the template's obligations are asserted by T033 (structure), T039 (assembly) and T034 (equivalence).
- **Disclosure — installed CLI substitution**: T045 runs the repository source rather than `/usr/local/bin/specify` (released 0.0.22); the substitution and its probe are recorded in § Environment Prerequisites and must be restated in `notes/quickstart-run.md`.
- **Disclosure — engine packages serialize on one file**: `src/specify_cli/__init__.py` is the single-module CLI; `pkg02`–`pkg05` declare reason code `write-conflict` and run serially, while `[P]` marks test-authoring parallelism only.
- **Premise re-measurement**: every quantity in § Premises measured at generation time is re-measured at implement entry and before each rerun of this command; a differing re-capture replaces the cited value rather than keeping the stale one.
