# E3 stage-status — 084-harness-triple-structure

## requirements（2026-11-05）

```yaml
stage: requirements
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/checklists/requirements.md
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
```

## Why `not-run-docs-only`

本阶段只生产规格、清单与证据文件，未触及任何可执行面（`scripts/`、`skills/**/scripts/`、
`src/`、`tests/`、`templates/*.yaml` 均未改动）。因此 `targeted-set-v1` 的输入
`changed_paths` 全部落在 `test_roots`（`tests/unit`、`tests/contract`、
`tests/integration`、`tests/scenarios`）之外、且不涉及夹具，选择程序得空集属预期形态，
按 `.specify/skills/external/sdd-loop-driver/references/efficiency-model.md` § 2.3 末条
记 `not-run-docs-only` 而非 `empty-selection-escalated`。运行字段（`selected_paths[]`、
`sufficiency`、`rc`、`passed`/`failed`、`new_failures[]`、比较基线）不适用，MUST NOT
报 `unknown`（同 owner § 2.4 六项缩减字段集）。

## Bases verified (not "green by assumption")

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 规格结构 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` | `status: ok`，六判项全 pass，`0 error(s), 0 warning(s)`，exit 0 | `test-evidence/validate-requirements.txt` |
| 类别解析 | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration` / exit 0 | `test-evidence/flow-class-lookup.txt` |

**驱动者 U4 复跑（2026-11-05 07:53 UTC；独立于阶段执行者）**：

- `decomposition-check.py --mode plan --requirements .specify/specs/084-harness-triple-structure/requirements.md`
  → `decision=proceed`（`fr_count=19`，上限 30），exit 0。
- `pre-analyze-check.py --spec-dir .specify/specs/084-harness-triple-structure --stage requirements --repo <repo>`
  → 首次运行 exit 2（`requirements.md carries no § Runtime Stack & Dependency Ownership`）；
  驱动者补写该强制节（`execution` 类特性必填，三行：RS-001 CPython / RS-002 pytest / RS-003 `specify init`）后复跑
  → `decision=pass`，`errors=0`，`advisories=12`（全部为 requirements 阶段尚未创建的计划交付路径，属预期），exit 0。
- 修复提交：`fix(084): add the mandatory runtime stack section and refresh the evidence`（独立于阶段提交 `a94c3945`）。

## clarify（2026-11-05）

```yaml
stage: clarify
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/checklists/requirements.md
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup-clarify.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/clarify-adjudication.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-clarify.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/memory/features.md
  - .specify/memory/features/084.md
  - .specify/memory/features/081.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/clarify-adjudication.txt
```

## Why `not-run-docs-only`（clarify）

本阶段的 `changed_paths` 全部是 markdown（规格、清单、注册表行、Feature 详情、证据文件）：没有一行落在
`tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`，也没有触碰 `scripts/`、
`skills/**/scripts/`、`src/`、`tests/` 的夹具。因此 `targeted-set-v1` 在 `stage_base=cd446a6e` 上
**不适用**——判据 owner `.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 明文
规定「仅文档改动时 MUST 记录 `not-run-docs-only` 与 `changed_paths[]` 改动路径证据」，缩减字段集即本行
六项（`stage`、`row_type=stage-status`、`status`、`selection_basis`、`changed_paths[]`、`evidence_ptr`）；
运行字段不适用且 MUST NOT 报 `unknown`。载体面同义表述（§ 2.3 末条 / § 2.4）与本条一致，二者不一致时以
TB-06 为准。

一次**不记账**的旁证：若把 TB-05 (a) 的「模块 stem」子句字面套用在 markdown 上，`requirements.md` 的
stem `requirements` 一个词就命中 **118** 个测试文件（读数与命令见证据文件附节）——这是把「改 .py 模块要
选中提到该模块的测试」这条规则误用到文档上的退化结果，不是定向集。故本轮不记 `selected_paths[]`，也不
执行该集合；若把它当定向集运行，属于 TB-08 意义上的预算浪费而非合规。

## Bases verified (clarify)

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 规格结构（写回后） | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` | `status: ok`，六判项全 pass，`scanned: 282 lines, 25 definition rows, 14 shared strings`，`0 error(s), 0 warning(s)`，exit 0 | `test-evidence/validate-requirements.txt` |
| 类别声明仍成立 | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration`，exit 0（`marker: null` = 0 个活动澄清标记） | `test-evidence/flow-class-lookup-clarify.txt` |
| 需求阶段门禁未被写回破坏 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/084-harness-triple-structure --stage requirements --repo .` | `decision=pass`，`errors=0`，`advisories=15`（全部为尚未创建的计划交付路径），exit 0 | `test-evidence/pre-analyze-clarify.txt` |
| 裁定依据的机械读数 | 见证据文件内逐条「命令 + 原始输出」 | 台账 80 行（原写 79，已订正）；`Path` 取值域三处实体；标签集被 081 验收测试钉住；`shared/declarations` 树内零命中 | `test-evidence/clarify-adjudication.txt` |
| 注册表自洽 | `grep -cE '^\| [0-9]{3} \|' .specify/memory/features.md` / `sed -n '4p'` | 行数 77 = `**Total Features**: 77`（同趟重算，原 76） | `test-evidence/clarify-adjudication.txt` |

**本阶段未新增门禁、未创建 plan 产物、未改变阶段序列**；`pre-analyze-check` 的 `--stage` 取值域不含
`clarify`，故上表第三行用 `requirements` 复跑作为「写回没有破坏已通过的阶段门」的读数，不是新增门禁。

## plan（2026-11-05）

```yaml
stage: plan
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/plan.md
  - .specify/specs/084-harness-triple-structure/research.md
  - .specify/specs/084-harness-triple-structure/data-model.md
  - .specify/specs/084-harness-triple-structure/quickstart.md
  - .specify/specs/084-harness-triple-structure/feature-ref.md
  - .specify/specs/084-harness-triple-structure/contracts/declaration-schema.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/harness-triple-check.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/shared-reader.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/distribution-and-mirror.contract.md
  - .specify/specs/084-harness-triple-structure/test-evidence/plan-readings.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/decomposition-plan.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/specify-init-source-route.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/memory/features.md
  - .specify/memory/features/084.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan.txt
```

**attempt-2 收口复跑（2026-11-05T08:18Z，驱动者收口轮次）**：第 1 次 plan 执行在回合预算处停止、
未返回 `PLAN-DONE`，产物已落盘。本轮不重跑设计，只把三道门各复跑一次并刷新逐字输出：
`pre-analyze --stage plan` exit 0 `decision=pass` `errors=0` `advisories=51`、
`decomposition-check --mode plan` exit 0 `decision=proceed` `fr_count=19`、
`validate-decision-tensions` exit 0 `status: ok` 六判项全 pass `4 record(s)`。
两次读数的判决逐项一致，`changed_paths[]` 与上表相同（无新增路径）。

## Why `not-run-docs-only`（plan）

本阶段的产品全部是文档：`plan.md`、`research.md`、`data-model.md`、五份 `contracts/*.md`、`quickstart.md`、
`feature-ref.md`、证据文件，以及 Feature 注册表与详情的状态位。没有一行落在 `tests/unit`、`tests/contract`、
`tests/integration`、`tests/scenarios`，也没有触碰 `scripts/`、`skills/**/scripts/`、`src/`、`tests/` 夹具。
故 `targeted-set-v1`（`stage_base=171c2ff8`）在本阶段不适用：判据 owner
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 规定「仅文档改动时 MUST 记录
`not-run-docs-only` 与 `changed_paths[]`」，缩减字段集即本行六项（`stage`、`row_type=stage-status`、`status`、
`selection_basis`、`changed_paths[]`、`evidence_ptr`）；运行字段（`selected_paths[]`、`sufficiency`、`rc`、
`passed`/`failed`、`new_failures[]`、比较基线）不适用且 MUST NOT 报 `unknown`。

整轮 pytest 基线**故意未跑**：它是 implement 阶段的预算项（状态脊 `test-budget` 记 `baseline@implement-start`），
本阶段只做**收集级**读数（`plan-readings.txt` § R11：081 两个验收文件分别收集 40 / 37 个用例），用于把「零新增失败」
写成可测量而不是口号。

## Bases verified (plan)

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 类别（本阶段唯一一次读取） | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration`，exit 0 | `test-evidence/plan-readings.txt` § R12 |
| 跨产物门禁（plan 阶段） | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan --spec-dir .specify/specs/084-harness-triple-structure --repo .` | `decision=pass`，`errors=0`，`advisories=51`（全部为尚未创建的计划交付路径：`shared/declarations/`、owner 文档、测试模块与夹具），exit 0；首轮曾以 11 条 `dangling-id` 失败（`MB-01` 只作为标题定义、`DM-13` 落在被 `SKIP_HEADING` 命中的 `changelog` 小节内），改为条款行定义后复跑转绿 | `test-evidence/pre-analyze-plan.txt` |
| 拆解门 | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/084-harness-triple-structure/requirements.md` | `decision=proceed`（`fr_count=19` ≤ 30），exit 0 ⇒ 决策 `single-package` | `test-evidence/decomposition-plan.txt` |
| 决策张力记录形态 | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/084-harness-triple-structure` | `status: ok`，六个标签全 pass，`scanned: 427 lines, 4 record(s)`，`0 error(s), 0 warning(s)`，exit 0（attempt-2 复跑读数一致；输出 11 行） | `plan.md` § Decision Tensions（T-001…T-004） |
| 结构面 | `python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/084-harness-triple-structure` | `status: not-applicable`（执行类；结构门禁只适用于表达类），`two-way: not-run`；章节树按派发要求仍产出，供 implement 时对照交付文档 | 本行即读数（无独立文件：输出 5 行） |
| 镜像基线（动手前） | `python3 scripts/python/sync-mirrors.py --check` | exit 0，六对全 `ok`（`shared/` 62 文件 / `scripts/` 119 文件） | `test-evidence/plan-readings.txt` § R4 |
| 分发读数（两条路由） | `specify init …`（PATH 控制台）与 `PYTHONPATH=<repo>/src … init …`（源检出） | 前者 55 个 md（安装态快照）、后者 62 个 md + 五个子目录 ⇒ 前者的断言记为 `EP-002` `falsified`，分发读数取后者 | `test-evidence/plan-readings.txt` § R5/R6、`specify-init-source-route.txt` |
| plan 完整性 | `grep -c '^# Implementation Plan:' plan.md` / 占位符扫描 / 印章 | H1 恰 1 个；无 `[UPPER_SNAKE]` 残留占位符；`**Requirement → Feature**` 印章在场 | 本行即读数 |

**本阶段未新增门禁、未新增阶段、未改变任何既有门禁的判据与退出码**；`pre-analyze-check` 的 `--stage` 取值域与
`plan` 行既有算子逐字不变（派发要求里的「门禁调用点」是交付设计，不是本阶段已生效的调用）。

## tasks（2026-11-05）

```yaml
stage: tasks
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-tasks.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/decomposition-tasks.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/tasks-readings.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/decomposition-tasks.txt
```

## Why `not-run-docs-only`（tasks）

本阶段只产出一份任务清单（`tasks.md`）与三份证据文件：没有一行改动落在 `tests/unit`、`tests/contract`、
`tests/integration`、`tests/scenarios`，也没有触碰 `scripts/`、`skills/**/scripts/`、`src/`、`tests/` 夹具、`templates/*.yaml`。
因此 `targeted-set-v1`（`stage_base=4b65517c`）输入全部落在 `test_roots` 之外、且不涉及夹具，得空集属预期形态，按 TB-06
记 `not-run-docs-only` 而非 `empty-selection-escalated`；运行字段（`selected_paths[]`、`sufficiency`、`rc`、
`passed`/`failed`、`new_failures[]`、比较基线）不适用且 MUST NOT 报 `unknown`。判据 owner 与六项缩减字段集同 requirements/clarify/plan 三行的引用。

## Bases verified (tasks)

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 任务清单结构 | `python3 scripts/python/validate-tasks.py .specify/specs/084-harness-triple-structure/tasks.md` | `PASS`，`0 error(s), 0 warning(s)`，exit 0；31 行任务、ID 唯一、`blockedBy` 全部指向更早行、8 个 `[P]` 分属四对路径不相交的行、四个故事相各自恰一个 `[USn]`、非故事相零 `[US`、DoD 段零 checkbox | `test-evidence/validate-tasks.txt` |
| 拆解门（tasks 模式） | `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements <req> --tasks <tasks>` | `decision=proceed`，`fr_count=19 ≤ 30`，`task_count=31 ≤ 40`，exit 0 | `test-evidence/decomposition-tasks.txt` |
| 前提复测（生成期实测，非继承） | 见证据文件 A–G 节：镜像基线、081 零差异与 40/37 收集数、`pyproject.toml` 零差异、候选面 27/53/19/12、九个批 1 常量的 `file:line`、`Path` 域的第二处内联元组 | 全部与 `plan.md` / `research.md` 的读数一致；本轮另得两条**新**读数（见下） | `test-evidence/tasks-readings.txt` |
| 契约条款形态 | `clause_extract.form_of` 对五份契约 | 五份全 `md-none`、各 id 族 `resolvable=False` ⇒ `[green:]` 标签在本特性必为 `green-dangling` 错误，故整份 tasks 不启用该标签，条款分区由 § Traceability 承载（逐字输出见证据 F 节） | `test-evidence/tasks-readings.txt` § F |
| 覆盖率账本起点 | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/084-harness-triple-structure` | `status: baseline-missing`；`[fr-uncovered] fail (19) — 0 of 19 FRs cited from citation groups`；`[clause-unparsable] warn (108)`。起点如实记录，不由本阶段冻结基线（冻结是 T002 的 implement 动作） | `test-evidence/tasks-readings.txt` § G |

**本阶段未新增门禁、未新增阶段、未创建任何 plan-owned 产物、未勾选任何任务行**；`tasks.md` 交付 31 行全 `[ ]`，
`plan_constraint=active`（`plan_commit=4b65517c`）下未改动 plan.md / data-model.md / contracts/ / quickstart.md /
research.md / feature-ref.md，故无 `PLAN-EDIT` 声明。

**两处自纠（纠正而非裁定，已披露）**：

1. **T001 的复算命令形态**：初稿写 `grep -n "…" scripts/python/`（对目录 grep 会报 `Is a directory` 并返回 0 行），
   实跑即失败；改为 `scripts/python/*.py` 后同一条命令返回 30 行（9 条定义 + 21 处使用点），并把「比较对象是 9 条定义
   而非 30 条命中」写进该行。这正是「打印了复算命令却从未执行」那个陷阱，本轮由实跑发现并当场修正。
2. **`[green:]` 标签的可用性**：不是风格选择，而是实测约束（五份契约 `md-none`）。若照模板惯例挂标签，`validate-tasks.py`
   会以 `green-dangling` 报错；本阶段按可选面不启用，并在 `tasks.md` 横幅与 § Traceability 各陈述一次理由与替代载体。
   契约 id 方案是 plan-owned 产物，改它属 substantive，故只登记不修改。

## checklist（2026-11-05）

```yaml
stage: checklist
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/checklists/layer-criteria-2026-11-05.md
  - .specify/specs/084-harness-triple-structure/test-evidence/checklist-self-check.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup-checklist.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/checklist-self-check.txt
```

## Why `not-run-docs-only`（checklist）

本阶段新增一件**需求质量清单**（`checklists/layer-criteria-2026-11-05.md`）与三件证据文件：改动面全是 markdown，
没有一行落在 `tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`，也没有触碰 `scripts/`、
`skills/**/scripts/`、`src/`、`tests/` 的夹具或 `templates/*.yaml`。因此 `targeted-set-v1`（`stage_base=8ed70a87`）
的输入全部落在 `test_roots` 之外、与夹具无关，得空集属**预期形态**，按判据 owner
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 记 `not-run-docs-only` 而非
`empty-selection-escalated`；缩减字段集即本行六项（`stage`、`row_type=stage-status`、`status`、`selection_basis`、
`changed_paths[]`、`evidence_ptr`）。运行字段（`selected_paths[]`、`sufficiency`、`rc`、`passed`/`failed`、
`new_failures[]`、比较基线）不适用且 MUST NOT 报 `unknown`。

本阶段确实**执行**了一个程序——清单自检程序（条目数／编号连续／可追溯比例／禁用开头／重复编号／未覆盖既有清单，
外加它将清单引用的每一条前提重新推导一遍）。它不读 `tests/`、不选测试、不消耗测试槽位，故不触发定向集，
也不是一次测试运行；逐字输出与程序全文见 `checklist-self-check.txt`。

## Bases verified（checklist）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 清单形态 | `python3 <清单自检程序>`（程序全文随证据归档） | `status: ok`；38 条；`CHK001..CHK038` 连续、无重复；可追溯 38/38 = 100%（下限 80%）；38/38 为「问句 + 质量维度括号」形态；禁用开头 0；既有 `checklists/requirements.md` 未被覆盖（`git status --porcelain` 为空，7417 bytes） | `test-evidence/checklist-self-check.txt` § 1–3、§ 6 |
| 清单引用的每条前提（重新推导，不继承） | 同上 § 4(a)–(f) | 六条原因模板各带 1 个占位符（`STR-011` 带 2 个）而形态规则称「一条无占位符」；(b) `tasks.md` 引用的 20 个 FR id 中 `FR-023` 不在 `requirements.md` 的 `FR-001..FR-019` 内（2 处命中）；(c) 既有门禁脚本集合在 FR-010／FR-019／N5／SC-006 四处给出口径不一（5／4／4／5，且成员不同）；(d) `templates/review-template.md:148` 引用 `scripts/python/closure-acceptance-check.py` 而该载体不在 FR-004 的三面之内；(e) `better-harness.md` § 消费者清单 存在于第 73 行；(f) 同一棵树上 `duplicate` 面两种调用面读数不同（14 文件/0 finding vs 15 文件/2 finding） | `test-evidence/checklist-self-check.txt` § 4 |
| 类别（本阶段唯一一次读取） | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null` / exit 0 ⇒ 非表达类，本阶段门禁集逐字不变、零新增阻断项、零新增必填章节 | `test-evidence/flow-class-lookup-checklist.txt` |
| PLAN CONSTRAINT（零改动） | `git diff --stat 8ed70a87 -- requirements.md tasks.md plan.md data-model.md contracts/ quickstart.md research.md feature-ref.md` | 空输出、exit 0 ⇒ 无 `PLAN-EDIT`，也没有回改需求或任务 | 本行即读数（命令与基线写明，输出为空） |
| 非规格产物面 | `git status --porcelain -- .specify/specs/084-harness-triple-structure` | 本阶段只新增 3 个未跟踪文件（清单 + 两份证据），`requirements.md`、`tasks.md` 与 plan-owned 全部未动 | 本行即读数 |

**本阶段未新增门禁、未新增阶段、未创建或修改任何 plan-owned 产物、未勾选任何任务行、未改写既有清单**。
清单里的跨产物分歧（`FR-023` 引用缺失、既有门禁集合口径不一）**只登记不修平**：修平要在「改 `tasks.md`」与
「改 `requirements.md`」之间做选择，属 `/speckit.analyze` 的裁决面，不在本阶段范围内。



## analyze（2026-11-05）

```yaml
stage: analyze
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/test-evidence/analyze-report-2026-11-05.md
  - .specify/specs/084-harness-triple-structure/test-evidence/account-clause-coverage.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/analyze-report-2026-11-05.md
```

## Why `not-run-docs-only`（analyze）

`/speckit.analyze` 是**只读质量门**：它不修改任何制品，本阶段的写面只有证据文件与 Wrap-up 记账。改动面全部
落在 `test-evidence/` 之下，没有一行落在 `tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`，
也没有触碰 `scripts/`、`skills/**/scripts/`、`src/`、夹具或 `templates/*.yaml`。因此 `targeted-set-v1`
（`stage_base=9abb10fb`）的输入全部落在 `test_roots` 之外、与夹具无关，得空集属**预期形态**，按判据 owner
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 记 `not-run-docs-only` 而非
`empty-selection-escalated`；缩减字段集即本行六项（`stage`、`row_type=stage-status`、`status`、`selection_basis`、
`changed_paths[]`、`evidence_ptr`）。运行字段（`selected_paths[]`、`sufficiency`、`rc`、`passed`/`failed`、
`new_failures[]`、比较基线）不适用且 MUST NOT 报 `unknown`。

本阶段确实**执行**了若干只读程序（前置脚本、类别读取、条款/FR 覆盖核算、决策张力校验、`duplicate` 面两种
调用形态、门禁脚本测试面并集重算、081 冻结面 `git diff`），另派发了四个只读验证子代理。它们都不读 `tests/` 的
用例选择面、不消耗测试槽位、不产生测试结果，故不触发定向集，也不是一次测试运行；读数与命令见报告
§ Evidence pointers。

## Bases verified（analyze）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 前置与产物齐备 | `bash scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | `REQUIREMENTS_DIR` 解析到本 spec；`AVAILABLE_DOCS` 含 contracts/、checklists/、tasks.md | 本行即读数 |
| 类别（本阶段唯一一次读取） | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration` / exit 0 ⇒ 非表达类，门禁集逐字不变 | 本行即读数 |
| 条款/FR 覆盖（固定只读步，MUST NOT `--freeze`） | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/084-harness-triple-structure` | `claimed clauses 0`；`0 of 19` FRs cited；`status: baseline-missing`（533 errors）⇒ 阶段可见问题 + 修复归属 `/speckit.tasks` | `test-evidence/account-clause-coverage.txt` |
| 决策张力记录 | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/084-harness-triple-structure --json` | `status: ok`，六个 label 全 `pass`/count 0 | 本行即读数 |
| 只读性（无制品改动） | `git status --porcelain` 前后各一次 | 两次逐行相同（18 行）⇒ 验证波零写入 | 本行即读数；报告 § Validation wave |
| 081 冻结面 | `git diff --stat 3ffeb26e -- shared/workflow/acceptance-hardening.md .specify/shared/workflow/acceptance-hardening.md tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py` | 空输出 ⇒ 本分支零改动 | 本行即读数 |
| PLAN CONSTRAINT（零改动） | `git diff --stat 9abb10fb -- requirements.md tasks.md plan.md data-model.md contracts/ quickstart.md research.md feature-ref.md` | 空输出 ⇒ 无 `PLAN-EDIT` | 本行即读数 |

**本阶段未修改任何制品、未勾选任何任务行、未提交、未 push；F-01／F-02／F-03 三条 CRITICAL/HIGH 的修复归属已点名
（requirements / plan / requirements），修平动作留给对应命令。**
