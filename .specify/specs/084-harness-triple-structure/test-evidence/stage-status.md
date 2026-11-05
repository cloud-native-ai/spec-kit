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


## requirements 修复（2026-11-05，analyze 回环 round 1）

```yaml
stage: requirements
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
base_commit: 6ac4c2d3
```

## Why `not-run-docs-only`（requirements 修复）

本轮只改规格文本与证据文件：`requirements.md` 上按 finding 计的十组文本修复（F-01／F-03／F-04／F-06／F-08／C-02…C-06），
外加两份 `test-evidence/` 文件。改动面没有一行落在
`tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`，也没有触碰 `scripts/`、`skills/**/scripts/`、
`src/`、夹具或 `templates/*.yaml`。因此 `targeted-set-v1` 的输入全部落在 `test_roots` 之外、与夹具无关，得空集属
**预期形态**，按判据 owner `.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 记
`not-run-docs-only` 而非 `empty-selection-escalated`。

## 逐条处置（只处置 requirements-owned findings）

| Finding | 原严重度 | 处置 | 落点 |
|---|---|---|---|
| F-01 | CRITICAL | **一次 owner 枚举 + 四处指针**：FR-010 成为「既有门禁脚本」的唯一枚举点，并按两个角色分列——「不得重判侧」六脚本（含 `doc-consistency-check.py`，它在其中是被**复用**的一方）、「零 diff 侧」五脚本（六者去掉 `doc-consistency-check.py`）。FR-019／N5／SC-006／SC-006 Source 四处改为按名字引用 FR-010，各自的计数词随之改正（「四个面」「四个门禁脚本」「五个既有门禁脚本（五名）」全部消失）。**与 plan HC-07 的五处计数在同一行内点名对齐**：六元集是 HC-07 重判清单的超集，第六处 `closure-acceptance-check.py` 由 SC-006／A8(a) 带入、本特性对它承担的是「不得改动」义务（081 验收面，见 FR-018 硬约束），因此不留给 round 2 一个新计数分歧 | FR-010（owner）、FR-019、N5、SC-006、SC-006 Source |
| F-03 | HIGH | **在每条断言内点名参照物，不在判据内重新推导基线**：基线 = T001 采集进 `notes/pre-change-measurements.md` 的该条读数（实现起点由该次采集固定），plan 侧同形态先例 EP-003 的 `171c2ff8`（镜像侧 EP-004）。三条断言与两条 Source 行各自写明 | FR-009、SC-005、SC-006、SC-005 Source、SC-006 Source |
| F-06 | MEDIUM | 形态规则的真实分区：**五条各带一个占位符**（`STR-009`／`STR-010`／`STR-012`／`STR-013`／`STR-014`）、**一条带两个**（`STR-011`）、**无零占位模板**（5 + 1 = 6）。value 表本身未动 | § Shared Strings 收尾段 |
| F-04 | LOW | **钉住 `duplicate` 面的调用形态** `--action verify --faces duplicate --spec-dir <spec 目录>`，并写明该面没有逐事实选择器、读数随 owner 路径而变；**事实级归因**来自 [[STR-011]] 的 `<fact>@<path>` 与 `--action lookup --fact <fact-slug>`。FR-010 的「复用、不另造扫描器」与 SC-002 的逐事实计数由此不冲突 | FR-007 (b)、FR-010、SC-002、SC-002 Source |
| C-02 | MEDIUM | 去掉开放量词「至少」，改成**收口规则**：受影响 owner 文档 = MB-01／MB-03／MB-04 点名的全部 carrier ∪ 每个 in-scope fact 的每个 markdown carrier；五处已点名文档降级为「举例，不是第二份枚举」 | FR-018 |
| C-03 | MEDIUM | 二选一取**「文本自由、只判机械项」**：exit 2 降级标注不登记为 Shared String、不进封闭原因集（plan D7），夹具只判三件事（退出码 2／标注非空且点名缺失目录／不抛异常不打印 traceback）；FR-017 同步声明 exit-2 不是 finding | FR-013、FR-017 |
| C-04 | MEDIUM | `consumers` MUST 至少含一个引擎，只列载体是 **schema 错误**，MUST NOT 被容忍为永久 [[STR-005]] | FR-005 |
| C-05 | MEDIUM | SR-07 的**单一子集解析器守卫腿**进入 FR-019 的枚举（两份祖父解析器由显式 allowlist 豁免，理由 = N4） | FR-019 |
| C-06 | LOW | 确定性范围收口为**三个动作**（`coverage`／`verify`／`lookup`），SC-001 (i) 只作 `coverage` 上的读数实例 | FR-016、SC-001 (i) |
| F-08 | MEDIUM | Exclusion Record 属性表去掉 `reason`，写明**由文件名承载**（`exclusions/<reason>.yaml`） | § Key Entities |

联动修正（同一事实的指针同步，非新裁决）：`STR-003`／`STR-005`／`STR-011` 的 `Consumed by` 列补上本轮新增的引用方。

## 本轮不处置（非 requirements-owned，已在 analyze 报告点名归属）

F-02（contracts 条款 id → plan）、F-05（`tasks.md` 的 `FR-023` → tasks）、F-07（`plan.md` D10 的 `39` → plan）、
E-01（`coverage-baseline.txt` 冻结 → tasks）、F-09（任务行 tag → tasks）、G-01（特性详情文件的阶段记录 → feature）。
`tasks.md`／`checklists/`／plan-owned 产物本轮**零改动**。

## Bases verified（requirements 修复）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 规格自校验 | `python3 scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` | exit 0；六判项全 `pass (0)`；`scanned: 282 lines, 25 definition rows, 14 shared strings`；0 error／0 warning | `test-evidence/validate-requirements.txt` § 1 |
| 前置门（analysis 前） | `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/084-harness-triple-structure --stage requirements --repo <repo>` | `decision=fail`、`errors=5`：五条全是 `dangling-id`（`FR-023` 在 `tasks.md:62`／`tasks.md:208`／`checklists/layer-criteria-2026-11-05.md:71/79/82`）。**非本轮引入、非 requirements-owned**（`FR-023` 在 `HEAD` 版 requirements 内同样不存在；`tasks.md`／`checklists/` 零改动），归属 F-05 | 同文件 § 2；修复前对照读数见 § 判读第 3 条 |
| FR 规模 | `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/084-harness-triple-structure/requirements.md` | `decision=proceed`、`fr_count=19`（上限 30）、`reasons=[]` ⇒ 19 FR／6 SC 编号稳定，未新增未删除 | 同文件 § 3 |
| 编号稳定性（独立复核） | `git show HEAD:.specify/specs/084-harness-triple-structure/requirements.md` 的 FR id 集 vs 工作树 | 两处都是 `FR-001..FR-019`（19 个），`**Flow Class**`／`**Flow Type**`／`**Path**` 标注未改 | 本行即读数 + 校验器 `id-contiguous`／`path-marker` 判项 |
| 只改 requirements-owned | `git status --porcelain -- .specify/specs/084-harness-triple-structure` | 修复轮内只有 `requirements.md` 被修改（证据文件另计），`plan.md`／`data-model.md`／`contracts/`／`quickstart.md`／`research.md`／`feature-ref.md`／`tasks.md`／`checklists/` 全部未动 | 本行即读数 |
| 临时目录已回收 | `rm -rf .specify/.tmp/084-reqfix` | 修复前的对照副本与两份 JSON 读数用完即删；只留证据文本里的读数与命令 | 本行即读数 |

**本轮未修改 plan-owned 产物、未修改 `tasks.md`、未勾选任何任务行、未改 Feature 注册表、未新增 FR/SC 编号；
F-01 的 CRITICAL 修复是文本级「一次枚举 + 指针」，不是新增机制。**


## plan 修复（2026-11-05，analyze 回环 round 1）

```yaml
stage: plan
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/contracts/declaration-schema.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/distribution-and-mirror.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/harness-triple-check.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md
  - .specify/specs/084-harness-triple-structure/contracts/shared-reader.contract.md
  - .specify/specs/084-harness-triple-structure/plan.md
  - .specify/specs/084-harness-triple-structure/research.md
  - .specify/specs/084-harness-triple-structure/feature-ref.md
  - .specify/specs/084-harness-triple-structure/quickstart.md
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/specs/084-harness-triple-structure/checklists/layer-criteria-2026-11-05.md
  - .specify/specs/084-harness-triple-structure/test-evidence/clause-extract-5-contracts.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/f07-test-file-readings.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan-repair.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/decomposition-plan-repair.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-decision-tensions-repair.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements-repair.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/clause-extract-5-contracts.txt
base_commit: fd84ed63
```

## Why `not-run-docs-only`（plan 修复）

本轮是 analyze 门对 F-02 的**显式 substantive reopen**（驱动者授权），改动面只有五份契约、六份 plan 阶段文本与
五份证据文件：没有一行落在 `tests/`、`scripts/`、`skills/**/scripts/`、`src/` 或夹具。因此 `targeted-set-v1` 的输入
全部落在 `test_roots` 之外，按判据 owner `.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06**
记 `not-run-docs-only`。

## 逐条处置（只处置 plan-owned findings）

| Finding | 原严重度 | 处置 | 落点 |
|---|---|---|---|
| F-02 | HIGH | **条款 id 重编号为规范形态 `md-bold-closed`**：59 条按文件与出现顺序确定性映射为 `C-001…C-059`（表见下节），所有规范性引用同步；`distribution-and-mirror` 的 `**DM-01 Asset roster**` 式「标签在粗体内」写法改为 `**C-013** Asset roster`，使每条标记都是 `**C-NNN**`。语义零改动 | 五份 `contracts/*.contract.md`、`plan.md`、`research.md`（引用侧）、`feature-ref.md`、`quickstart.md`、`requirements.md`、`tasks.md`、`checklists/layer-criteria-2026-11-05.md` |
| F-07 | MEDIUM | **读数可复现化**：把「五个冻结门禁脚本」逐字写进 `plan.md` D10 与 § Evidence List，读数取 SC-006 零 diff 侧五个 ⇒ **38** 个测试文件；另两个读数连来源一起记录——35 = 同一条命令在 analyze 时的五名集（`doc-consistency-check` 顶替 `closure-acceptance-check`），39 = 六名并集（正是修复前 `plan.md` 所写的数）。逐字命令、三个名单清单与三者算术落新证据文件；`research.md` § R7 同步订正并注明 `plan-readings.txt` § R10 是日期化读数、不回改 | `plan.md` § D10 + § Evidence List、`research.md` § R7、`test-evidence/f07-test-file-readings.txt` |
| C-01 | MEDIUM | **批 2／批 3 逐行补 engine side**：`C-044`／`C-045` 改为与 `C-042` 同形的两列表格（engine side ｜ carrier side），一行一事实；有引擎侧的写常量名或读取点（`flow-class-check.py` 的 `FACES_EXPECTED`／表头 `required`、`closure-acceptance-check.py` 的 `final_path_counts()`／`verdict`、`loop-state.py` 的 `STAGE_ARTIFACTS`／`sentinel_literal()`、`memory-utils.py` 的 `SCOPES`、`record-retention.py` 的 `DEFAULT_GRACE_DAYS`／`STORES`、`history-utils.py` 的 manifest 读写、`probe-utils.py` 的字段元组、`exec-quant.py`／`trigger-utils.py` 的 schema 常量），确无引擎侧的写 `none` 并给实测理由。批次划分与验收规则未动 | `contracts/migration-batches.contract.md` C-044／C-045 |

### F-02 的确定性映射（按文件与出现顺序）

| 契约文件 | 旧 id | 新 id | 条款数 |
|---|---|---|---|
| `declaration-schema.contract.md` | `DS-01…DS-12` | `C-001…C-012` | 12 |
| `distribution-and-mirror.contract.md` | `DM-01…DM-13` | `C-013…C-025` | 13 |
| `harness-triple-check.contract.md` | `HC-01…HC-16` | `C-026…C-041` | 16 |
| `migration-batches.contract.md` | `MB-01…MB-10` | `C-042…C-051` | 10 |
| `shared-reader.contract.md` | `SR-01…SR-08` | `C-052…C-059` | 8 |
| **合计** | — | `C-001…C-059` | **59** |

`migration-batches.contract.md` 的章节标题 `## MB-01 — Batch 1: …` 改为 `## Batch 1 — …`：标题若带条款 id，同一份
契约内该 id 会出现两次（章节 + 条款行），违反语法 owner § 1 的「id 在同一份契约内 MUST 唯一」。`feature-ref.md` 里
指向该章节的 `§ MB-01` 随之改为指向条款 `C-042`（批 1 名单即该条款）。

## 本轮不处置（非 plan-owned，已在 analyze 报告点名归属）

F-05（`tasks.md`／`checklists/` 的 `FR-023` → tasks）、E-01（`coverage-baseline.txt` 冻结 → tasks）、
F-09（任务行 tag → tasks）、G-01（特性详情文件的阶段记录 → feature）。三处 `tasks.md` 改动仅限条款 id 的机械替换。

## Bases verified（plan 修复）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 条款形态（五份契约各一次） | `python3 scripts/python/clause_extract.py .specify/specs/084-harness-triple-structure/contracts/*.contract.md` | 五份全 `form=md-bold-closed`；条款数 12／13／16／10／8 = **59**，id 连续 `C-001…C-059`，exit 0（修复前同一命令为五份全 `form=md-none` `clauses=0`） | `test-evidence/clause-extract-5-contracts.txt` |
| 旧 id 残留扫描 | `grep -rnE "\b(DS\|HC\|SR\|MB\|DM)-[0-9]+\b" contracts/ plan.md data-model.md quickstart.md research.md feature-ref.md requirements.md tasks.md checklists/layer-criteria-2026-11-05.md` | **零命中**（exit 1）。日期化读数 `analyze-report-2026-11-05.md`／`stage-status.md`／`plan-readings.txt`／`tasks-readings.txt` 按派发要求不回改，它们保留当时的 id | 本行即读数 |
| 前置门（analysis 前） | `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/084-harness-triple-structure --stage plan --repo <repo>` | `decision=fail`、`errors=5`、`advisories=82`。五条 error 全是 `dangling-id`：`FR-023` 在 `tasks.md:62`／`tasks.md:208`／`checklists/layer-criteria-2026-11-05.md:71/79/82`——**与本轮改动无关**：把 `HEAD`（`fd84ed63`）的 spec 目录用 `git archive` 拉到 `.specify/.tmp/084-head-check2/` 后跑同一命令，产出的 **error 集与本轮逐条相同**（同为那 5 条，同路径同行号；对称差里没有任何 `dangling-id` 行），归属 F-05（tasks-owned） | `test-evidence/pre-analyze-plan-repair.txt`；HEAD 对照读数在本行记录，临时目录已回收 |
| 该门两条 advisory 差的成因（逐条比对，不猜） | 同上两条命令的 findings 做 `(check, path, line, message)` 对称差 | 净差 −3，逐条归因：① `tasks.md:249` 的 `external-clause`（`FF-12`）消失——`summary.clauses` 由 `59` 掉到 `0` 后该检查整体跳过；②③ `requirements.md:146`／`tasks.md:62` 那两条 `missing-path`（spec 目录内的 `notes/pre-change-measurements.md`）消失——**是对照跑法的产物，不是修复的产物**：该检查对 `spec_rel` 前缀下的路径按设计跳过，HEAD 对照用的是临时 spec 目录，其 `spec_rel` 不同故未跳过；另有一条 `missing-path`（`contracts/migration-batches.contract.md`）由第 60 行移到第 82 行，即 C-044／C-045 增表带来的行位移 | 本行即读数 |
| 该门对本特性条款的覆盖读数 | 同上 JSON 的 `summary.clauses` | `59`（HEAD）→ **`0`**（本轮后）。原因是门宿主 `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 的 `CLAUSE_DEF = r"^- \*\*([A-Z]{2,4}-\d{2})\b"` 只认 2–4 个字母的前缀，规范形态 `C-001` 的前缀是单字母 `C`，故一条都抽不到。**这是门宿主既有口径对规范形态的覆盖缺口**（081 的 `C-` 形契约同样抽不到），不是本轮引入的失败，也不在本次授权范围内修（门宿主的改动属 T024 的 opt-in 委派行） | 本行即读数（数字取自两个 JSON 的 `summary.clauses`） |
| 拆解门 | `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/084-harness-triple-structure/requirements.md` | `decision=proceed`，`fr_count=19` ≤ 30，`reasons=[]`，exit 0 | `test-evidence/decomposition-plan-repair.txt` |
| 决策张力记录形态 | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/084-harness-triple-structure` | `status: ok`，六判项全 `pass (0)`，`scanned: 434 lines, 4 record(s)`，`channel: value_domain=HIGH-or-0, high=0`，exit 0 | `test-evidence/validate-decision-tensions-repair.txt` |
| 规格自校验 | `python3 scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` | `status: ok`，六判项全 `pass (0)`，`scanned: 282 lines, 25 definition rows, 14 shared strings`，exit 0（`requirements.md` 本轮只做 id 机械替换） | `test-evidence/validate-requirements-repair.txt` |
| 任务清单仍可解析 | `python3 scripts/python/validate-tasks.py .specify/specs/084-harness-triple-structure/tasks.md` | `PASS`，`0 error(s), 0 warning(s)`，exit 0（`tasks.md` 本轮只做 id 机械替换，未改任务内容） | 本行即读数 |
| F-07 读数可复现 | `grep -rlE --include=*.py "<五名>" tests/ \| sort \| wc -l` 与两个对照集 | 38（SC-006 零 diff 侧五名）／35（analyze 时五名）／39（六名并集）；38 的 38 个文件名逐行在证据文件内 | `test-evidence/f07-test-file-readings.txt` |
| 临时目录已回收 | `rm -rf .specify/.tmp/084-head-check2` | 修复前的 HEAD 对照副本与两份 JSON 读数用完即删，`.specify/.tmp/` 下无残留 | 本行即读数 |

**本轮未改 FR/SC 内容、未改阶段序列、未改门禁判据或退出码、未改批次划分与验收规则、未改 Feature 注册表状态、
未勾选任何任务行；F-02 是「形态归一 + 引用同步」，不是设计改写。**

## tasks 修复（2026-11-05，analyze 回环 round 1）

```yaml
stage: tasks
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/specs/084-harness-triple-structure/checklists/layer-criteria-2026-11-05.md
  - .specify/specs/084-harness-triple-structure/coverage-baseline.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/memory/features.md
  - .specify/memory/features/084.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan-tasks-repair.txt
stage_base: 9284c789
```

## Why `not-run-docs-only`（tasks 修复）

改动面是五件 markdown／文本产物加证据：`tasks.md`（四条标签）、`checklists/layer-criteria-2026-11-05.md`（三处
机械替换 + 一条 Note 补记）、`coverage-baseline.txt`（本阶段的冻结交付物，515 行文本）、`features.md` 的 084 行与
`features/084.md`（阶段记录与路径登记）。没有一行落在 `tests/`、`scripts/`、`skills/**/scripts/`、`src/`、
`templates/*.yaml` 或夹具上，因此 `targeted-set-v1`（`stage_base=9284c789`）的输入全部落在 `test_roots` 之外、
与夹具无关，得空集属**预期形态**，按判据 owner `.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md`
**TB-06** 记 `not-run-docs-only`；缩减字段集即本行六项，运行字段（`selected_paths[]`、`sufficiency`、`rc`、
`passed`/`failed`、`new_failures[]`、比较基线）不适用且 MUST NOT 报 `unknown`。本轮确实**执行**了五个只读程序
（`validate-tasks`、`decomposition-check --mode tasks`、`pre-analyze-check` 两阶段、`account-clause-coverage`
加一次 `--freeze`）与一次类别读取，它们都不读 `tests/` 的用例选择面、不产生测试结果。

## 逐条处置（tasks-owned findings + G-01）

| Finding | 原严重度 | 处置 | 落点 |
|---|---|---|---|
| F-05 | MEDIUM | **按裁决把越界引用改指 `FR-011, FR-018`**：T001 行标签与 § Traceability 的 T001 单元格各一处；任务内容、任务数（31）、FR 数（19）与「19 条 FR 全被点名」的覆盖声明都不变 | `tasks.md` T001 行 + § Traceability T001 行 |
| F-05 的清单侧残留 | MEDIUM（同一缺陷） | **同一越界引用的三处机械残留一并收口**：CHK037 去掉悬空 id 但保留「编号空间能否被机械复核」的质量问题语义；两条 Note 如实记下裁决与原 id 的去向（原 id 的逐字读数指向日期化证据 `analyze-report-2026-11-05.md` § F-05，注文本身不带该字面量，以守住「规范性与清单文件零命中」） | `checklists/layer-criteria-2026-11-05.md` CHK037 + 两条 Note |
| E-01 | MEDIUM | **本阶段行使自己的冻结职责**：`--freeze` 产出 `coverage-baseline.txt`（2 行 header + 513 个码点排序名，`base-sha: 9284c789e154`，`files: 248 (parsed 145 + named 103)`）；随后不带 `--freeze` 复跑，`status: baseline-missing`／exit 2 消失，读数变为 `status: uncovered`／exit 1（覆盖判决，不是输入错误）。同一命令跑两次输出逐字节相同，故 implement 阶段 T002 的重跑是幂等的 | `coverage-baseline.txt`、`test-evidence/coverage-baseline-freeze.txt`、`test-evidence/account-clause-coverage-tasks.txt` |
| F-09 | LOW | **两行标签补齐 `FR-008`**（T005、T006），与 § Traceability 一致；任务内容一字未动，覆盖声明里「FR-008 有意由两行各承一次」的写法因此与行标签自洽 | `tasks.md` T005、T006 |
| G-01 | LOW | **阶段记录补齐**：`features/084.md` § Latest Review 追加 tasks（`5dc5919a` + `8ed70a87`）、checklist（`9abb10fb`）、analyze 回环修复三提交三条带日期记录；§ Related Files 登记 `checklists/layer-criteria-2026-11-05.md`；`§ MB-01` 悬空指针改指 `C-042`。`features.md` 的 084 行两处机械订正（`59 条款 DS·HC·SR·MB·DM` → `59 条款 C-001…C-059`；`§ MB-01` → `C-042`），行结构、`Total Features` 与其它 76 行未动 | `features/084.md`、`features.md` |

### 一处口径判断（就地纠正，已在回传披露）

派发简报要求 Note 里如实说明「原 FR-023 已按 F-05 裁决改为 FR-011, FR-018」，同时又要求清单文件对该 id
零命中。两条在字面上冲突，按「日期化证据保留历史」这条既有口径收口：Note 写「原引用已按裁决改为
`FR-011, FR-018`」并指向 `analyze-report-2026-11-05.md` § F-05（该文件保留原 id 的逐字读数），
清单正文不出现该字面量。

## 本轮不处置（已在 analyze 报告点名，或超出本次授权）

- **`uncovered beyond baseline: 59` 与 `FR claimed: 0`**：那 59 条正是本特性自己的 `C-001…C-059`，未被认领的原因
  是 `tasks.md` 全文没有任何 `[green:]` 声明。analyze 报告已在 F-02 行裁定「[green:] 未使用本身不是缺陷（模板里
  该标签可选），它是症状」，故本轮不动任务行、不新增声明面。
- **T002 的内容**：它仍写着 implement 阶段重跑 `--freeze`；基线已在 tasks 阶段冻结，故该行在实现期退化为一次
  幂等复核，任务语义无需改动（改它属任务内容改写，不在本次授权内）。
- **plan-owned 与 requirements**：零改动（`git diff --stat 9284c789 -- requirements.md plan.md data-model.md
  contracts/ quickstart.md research.md feature-ref.md` 空输出）。
- **未勾选任何任务行**：31 行仍全为 `[ ]`；`Implemented` 归 `/speckit.implement`。

## Bases verified（tasks 修复）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 任务清单可解析 | `python3 scripts/python/validate-tasks.py .specify/specs/084-harness-triple-structure/tasks.md` | `PASS`，`0 error(s), 0 warning(s)`，exit 0 | `test-evidence/validate-tasks-repair.txt` |
| 拆解门 | `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements ... --tasks ...` | `decision=proceed`，`fr_count=19` ≤ 30、`task_count=31` ≤ 40，`reasons=[]`，exit 0 | `test-evidence/decomposition-tasks-repair.txt` |
| 前置门（analysis 前，requirements） | `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir ... --stage requirements --repo <repo>` | **`decision=pass`、`errors=0`**、`advisories=82`、`waived=0`，exit 0（修复前同一命令为 `fail`／5 条 `dangling-id`） | `test-evidence/pre-analyze-requirements-repair.txt` |
| 前置门（analysis 前，plan） | 同上，`--stage plan` | **`decision=pass`、`errors=0`**、`advisories=82`、`waived=0`，exit 0（修复前同 `test-evidence/pre-analyze-plan-repair.txt` 所记 `fail`／5） | `test-evidence/pre-analyze-plan-tasks-repair.txt` |
| 覆盖核算（冻结后） | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/084-harness-triple-structure` | `baseline: … (513 names)`（不再是 `0 names, MISSING`）；`baseline-internal existing uncovered: 513`；`uncovered beyond baseline: 59`；`status: uncovered`、`78 error(s)`、exit 1（判决态，非输入错误） | `test-evidence/account-clause-coverage-tasks.txt` |
| 基线冻结 | `python3 scripts/python/account-clause-coverage.py --spec-dir ... --freeze > .../coverage-baseline.txt` | exit 0；515 行 = 2 header + **513 names**；`base-sha: 9284c789e154`；`files: 248 (parsed 145 + named 103)`；重跑 + `diff` 逐字节相同 | `test-evidence/coverage-baseline-freeze.txt` |
| 越界 id 残留扫描（规范性与清单文件） | `grep -rn "FR-023" .specify/specs/084-harness-triple-structure/ \| grep -v "/test-evidence/"` | **零命中**（exit 1）。剩余命中只在 `test-evidence/` 的日期化证据（`analyze-report-2026-11-05.md`、`checklist-self-check.txt`、`validate-requirements.txt`、`pre-analyze-plan-repair.txt` 及本文件）。`.specify/memory/features.md` 的那一处 `FR-023` 属 **081** 自己的需求编号，与 084 无关，按「不改任何其它 Feature 行」保留 | 本行即读数 |
| 类别（本阶段唯一一次读取） | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null`，exit 0 ⇒ 非表达类，门禁集逐字不变、零新增阻断项 | 本行即读数 |
| Feature 索引一致性 | `grep -c "^| 0" .specify/memory/features.md` 与 `grep -n "Total Features"` | 77 行 = `Total Features: 77`，均未变；084 行只做两处机械订正 | 本行即读数 |
| 越界改动检查 | `git status --porcelain -- .specify/specs/084-harness-triple-structure .specify/memory/features.md .specify/memory/features/084.md` | 4 件改动（`tasks.md`、清单、`features.md`、`features/084.md`）+ 1 件新增（`coverage-baseline.txt`）+ 6 件证据；plan-owned、`requirements.md`、其它 Feature 行、`.specify/state/` 与运行时记录均未纳入 | 本行即读数 |

**本轮未改任务内容与任务数、未改 FR/SC 语义、未改阶段序列、未改门禁判据或退出码、未勾选任何任务行、未 push；
`coverage-baseline.txt` 是「记录」而非聚合处理状态，一条事实一个文件，双写者只会产生不同路径或零路径。**


## analyze（round 2, 2026-11-05）

```yaml
stage: analyze
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1@stage_base=2b18485e — (a) 改动路径覆盖 0 命中；(b) 交付物契约测试 16 命中；(c) 夹具变更 0 命中"
selected_paths:
  - tests/contract/test_acceptance_premises.py
  - tests/contract/test_acceptance_state_machine.py
  - tests/contract/test_client_guard_sweep.py
  - tests/contract/test_directory_governance.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_line_state_blocked.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_non_regression_064.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_sdd_diffusion.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/contract/test_sdd_loop_driver_wrapup_accounting.py
  - tests/contract/test_validation_carrier_contract.py
  - tests/integration/test_expression_line_pilot.py
  - tests/integration/test_sdd_loop_efficiency_runner.py
sufficiency: "TB-05 的 (b) 子句对每个阶段无条件生效（交付面 = 本特性短名 `harness-triple-structure` + `skills/external/sdd-loop-driver` + docs 指针页），故本只读阶段也得到 16 个文件；(a) 与 (c) 为空是因为改动集不含可执行面、不含夹具"
command: "python3 -m pytest -q <上列 16 个文件>"
rc: 1
passed: 295
failed: 3
new_failures: "not_computable —— implement 起点的 baseline 槽位尚未捕获，无比较基线；改为逐条归因：1 条由本特性制品引起（R2-01：features/084.md:31 的 `flow_class: execution` 命中 test_c2_no_project_side_classification_store），2 条属环境（test_e_a_stale_pin…：git 2.54.0 钉 vs 实测 2.43.7；test_c22_watch_target_hook_selftest：/home/agent/tmp 建目录被拒）"
baseline_compare: "none available at this stage（baseline 槽位归 implement 起点；本阶段按 TB-06 只做定向集）"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/analyze-round2-targeted-run.txt
```

## Why `ran`（analyze round 2）

派发简报预期本阶段记 `not-run-docs-only`（六项缩减字段），但 TB-05 的 **(b) 子句无条件生效**：它按「本特性短名 +
交付面路径」选契约/集成测试，与本阶段是否改动可执行面无关。实测选择集非空（16 个文件），因此本阶段**运行**了定向集。
先运行再记 `not-run-docs-only` 会与事实不符，故本行按 `status=ran` 记全字段（TB-06 的完整体例）。

对照：round 1 的 E3 行记 `not-run-docs-only`，理由写作「targeted-set-v1 得空集」。按 (b) 子句，空集不是该阶段的
真实选择结果；正确的表述应是「选中 16 个文件、因仅文档改动而未运行（TB-06）」。两行的**结论**（不消耗测试槽位、
不产生基线比较）不变，此处只把**依据**订正为可复现的形式——本条是簿记精度问题，不是规格 finding。

## Bases verified（analyze round 2）

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 五份契约可解析 | `python3 scripts/python/clause_extract.py .specify/specs/084-harness-triple-structure/contracts/*.contract.md` | 五份全 `form=md-bold-closed`；12 + 13 + 16 + 10 + 8 = **59** 条款；旧 `DS/HC/SR/MB/DM-<dd>` 在规范性与清单文件零命中 | `analyze-report-round2-2026-11-05.md` § Rerun delta |
| 条款/FR 覆盖（固定只读步，MUST NOT `--freeze`） | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/084-harness-triple-structure` | `claimed clauses 0`；`0 of 19` FRs cited；`59 beyond the frozen baseline`（513 names）；`status: uncovered`、78 error(s)、**exit 1**（判决态，不再是 `baseline-missing` 的 exit 2） | 报告 § Adjudication 1 |
| 前置门 ×3 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir … --stage {requirements,plan,tasks} --repo .` | 三门全 `decision=pass`、`errors=0`、`advisories=82`、`waived=0`，exit 0；三门 `summary.clauses=0`（`CLAUSE_DEF` 只认 2–4 字母 + 两位数字，`C-001` 抽不到 —— 框架侧缺口，077/079 同样命中） | 报告 § Adjudication 3 |
| 需求/任务校验 | `validate-requirements.py` · `validate-tasks.py` | `0 error(s), 0 warning(s)`（282 行、25 定义行、14 STR）；tasks `PASS 0/0` | 本行即读数 |
| 决策张力 | `validate-decision-tensions.py --spec … --json` | `status: ok`，六个 label 全 `pass`/count 0 | 本行即读数 |
| 拆解门 | `decomposition-check.py --mode plan` / `--mode tasks` | `proceed`（fr_count 19 ≤ 30；task_count 31 ≤ 40，`reasons=[]`） | 本行即读数 |
| 宪法对齐 | `plan.md` § Constitution Check vs `constitution.md` v1.15.0 | 18 行 / 18 条，名称逐条一致，0 缺失、0 不符 | 本行即读数 |
| Feature 注册表 | `grep -c "^| 0" .specify/memory/features.md`；`grep "Total Features"` | 77 行 = `Total Features: 77`；084 行 `Planned`、条款短语 `C-001…C-059`；详情文件状态一致 | 本行即读数 |
| 081 冻结面 | `git diff --stat 3ffeb26e -- shared/workflow/acceptance-hardening.md .specify/shared/workflow/acceptance-hardening.md tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py` | 空输出 ⇒ 零 diff | 本行即读数 |
| PLAN CONSTRAINT | `git diff --stat 9284c789..HEAD -- plan.md data-model.md contracts/ quickstart.md research.md feature-ref.md` | 空输出（tasks 修复未再碰 plan-owned）；`4b65517c..HEAD` 的差异恰为已授权的 plan 修复（9 文件 / +153 −115） | 本行即读数 |
| 只读性 | `git status --porcelain` 验证波前后各一次 | 两次均 22 行，唯一 `M` 是 clarify 遗留的 `.specify/memory/session/…-081a.md` ⇒ 波次零写入 | 报告 § Validation wave |

**本阶段未修改任何制品、未勾选任何任务行、未提交、未 push；R2-01／R2-02 两条 HIGH 的修复归属已点名
（feature 详情文件 / plan-or-requirements 的裁定），修平动作留给对应命令。**

## plan reopen（2026-11-05，路径 A：8 条 `engine side = none` 的事实移出名册）

```yaml
stage: plan
row_type: stage-status
status: not-run-docs-only
selection_basis: "docs-only（TB-06）＋ 一处定向守卫：本阶段写入 .specify/memory/，按 analyze round 2 § Systemic observations 2 的结论追加 tests/contract/test_expression_compatibility.py（`.specify/memory/` 的守卫集不属本特性自身测试面，任何写该目录的阶段都该跑）"
changed_paths:
  - .specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/memory/features/084.md
  - .specify/specs/084-harness-triple-structure/test-evidence/plan-reopen-pathA-gates-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/plan-reopen-pathA-targeted-run.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
command: python3 -m pytest -q tests/contract/test_expression_compatibility.py
rc: 0
passed: 16
failed: 0
new_failures: "0 —— 该文件在本轮改动后 16 passed；守卫腿 test_c2_no_project_side_classification_store 未命中本轮新增文本（新增段落不含 `flow_class: <value>` 赋值形态）"
baseline_compare: "none available at this stage（baseline 槽位归 implement 起点）"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/plan-reopen-pathA-targeted-run.txt
base_commit: d23490c3
```

## Why `not-run-docs-only`（plan reopen）

本轮是 **用户裁定的 substantive reopen（路径 A）**：改的是契约名册、范围表、任务行与 feature 记录，没有一行落在
`tests/`、`scripts/`、`skills/**/scripts/`、`src/` 或夹具，`targeted-set-v1` 的输入仍全部落在 `test_roots` 之外，故按
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md` **TB-06** 记 `not-run-docs-only`。唯一的例外是那一处
定向守卫：本轮第一次把内容写进 `.specify/memory/`（`features/084.md`），而 analyze round 2 已经证明该目录的守卫测试
不属任何阶段的门禁集（R2-01 就是这样漏过去的），所以主动补跑一次并留读数。

## 逐条处置（8 条事实的移出与排除理由）

| # | fact | 批次 | 单元（失去该事实的候选载体） | 处置 |
|---|------|------|------------------------------|------|
| 1 | `analyze-severity-values` | 2 | `templates/commands/analyze.md`；`skills/internal/analyze-artifacts/SKILL.md` | 移出 in-scope；两条事实落 2 个排除单元 |
| 2 | analysis finding-channel set | 2 | 同上 | 同上 |
| 3 | `review-segment-sequence` | 2 | `templates/commands/review.md`；`skills/internal/review-sdd-process/SKILL.md` | 移出 in-scope，**不写排除行**：该单元组仍持有 in-scope 的 `ARC verdict mapping`（`closure-acceptance-check.py`） |
| 4 | `self-improvement-stage-sequence` | 2 | `skills/internal/self-improvement/SKILL.md`（`self-improvement-workflow.md` 实测 0 条引擎路径引用 ⇒ 不入候选屏幕） | 移出 in-scope；两条事实落 1 个排除单元 |
| 5 | track-to-executor mapping | 2 | 同上 | 同上 |
| 6 | `improvement-track-values` | 2 | `improve-agent/`、`improve-team/`、`improve-tools/`、`skills/external/improve-docs/`、`improve-skills/` 五个 SKILL.md | 移出 in-scope；两条事实落 5 个排除单元 |
| 7 | changed-asset-category mapping | 2 | 同上 | 同上 |
| 8 | `history-categories` | 3 | `skills/internal/manage-history/SKILL.md` | 移出 in-scope，**不写排除行**：该单元仍持有 in-scope 的 `history-manifest-schema`（`history-utils.py`） |

**排除文件行数 = 8**（2 analyze + 1 self-improvement + 5 improve），与「8 条事实」是两个不同的量：排除行按**单元**
写（FR-002 + FR-005 + `data-model.md` E-2），一个单元 MUST NOT 既被声明覆盖又被排除行点名（E-2 **R-4**；E-5 把该矛盾
判为 finding）。第 3、8 条事实因此零行，其「未迁移」由 `contracts/migration-batches.contract.md`
§ Facts outside the roster 与 `features/084.md` § Latest Review 记录，而不是沉默删除。

**为什么不选路径 B**：把 FR-006 (i) 改成「迁移后可成立」会让判据自我证成——迁移自己制造自己的理由——而 clarify A2
的收窄正是为消灭这个机制。故本条按 FR-006 的 disposition 子句（「任一不成立即留在原处」）走排除侧。

## C-044／C-045 删除后剩余行

- **批 2（C-044）余 7 行，全部有今日引擎侧**：`expression-gate-faces`、`expression-stage-operator-table`、
  `ARC verdict mapping`、`driver-stage-sequence`、`driver-gate-roster`、`driver-completion-sentinels`、
  `driver-stage-artifacts`。
- **批 3（C-045）余 7 行，全部有今日引擎侧**：`memory-types`、`memory-retention-thresholds`、
  `history-manifest-schema`、`probe-class-values`、`probe-object-binding-map`、`quant-record-schema`、
  `trigger-state-schema`。
- **条款编号未动**：删除的是表行，不是条款；`C-044`／`C-045` 两条仍在，C-044／C-045 的 `none` 语义段改成「本表每行今天都有引擎侧，无读取点的事实归 § Facts outside the roster」。五份契约仍 12+13+16+10+8 = **59** 条，全部 `md-bold-closed`。

## 旧 in-scope 引用扫描（本轮改动的自检）

| 扫描 | 命令 | 读数 |
|------|------|------|
| 8 个 fact slug 在移出小节之外的出现 | `grep -n` 八个 slug × `*.md contracts/*.md` | 仅 `requirements.md:203` 的日期化复核段点名（属记录，不是名册行）；契约内只在 § Facts outside the roster 出现 |
| 残留的 `in-scope（批 2／批 3）` 行 | `grep -n "in-scope（批 2\|in-scope（批 3" requirements.md` | 6 行：expression-gates、review（标注「仅 ARC 判定」）、memory、manage-history（标注「仅 `history-manifest-schema`」）、sdd-loop-driver、probe；无一行仍把移出的 8 条事实算作 in-scope |
| tasks 的旧措辞 | `grep -n "mapping-shaped sets\|record schemas:" tasks.md` | 只剩 T016 的 `Migrate batch 3's record schemas:` 标题行；`mapping-shaped sets`（旧 T015 的措辞）0 命中 |
| 契约内 `none` 语义的旧读法 | `grep -n "read point is created at migration\|is a reading, not a gap\|none\` again" contracts/migration-batches.contract.md` | 0 命中（路径 B 的自我证成措辞已消失，改为「今天没有读取点即不 in-scope」） |
| plan-owned 四份对这 8 条事实的引用 | `grep -n` 八个 slug × `plan.md data-model.md feature-ref.md quickstart.md research.md` | 0 命中于五份中的前四份 ⇒ 没有「in-scope 主张」或「批次条数」需要订正，四份 plan-owned 文本**本轮零改动**；`research.md` 与本轮的 `none` 实测无关（它只在 § R1 用 `none` 一词描述依赖表），其日期化读数按简报保留 |

## Bases verified（plan reopen）

| 判项 | 命令 | 结果 |
|---|---|---|
| requirements 校验 | `python3 scripts/python/validate-requirements.py …/requirements.md` | `status: ok`、`0 error(s), 0 warning(s)`、exit 0 |
| tasks 校验 | `python3 scripts/python/validate-tasks.py …/tasks.md` | `PASS`、`0 error(s), 0 warning(s)`、exit 0 |
| 决策张力 | `python3 scripts/python/validate-decision-tensions.py --spec …` | `status: ok`、六个 label 全 pass、exit 0 |
| 拆解门（plan） | `decomposition-check.py --mode plan --requirements …` | `proceed`，`fr_count 19` ≤ 30，`reasons=[]` |
| 拆解门（tasks） | `decomposition-check.py --mode tasks --requirements … --tasks …` | `proceed`，`task_count 31` ≤ 40（任务总数未变） |
| 前置门（plan） | `pre-analyze-check.py --spec-dir … --stage plan --repo …` | `decision=pass`、`errors=0`、`advisories=84`、`waived=0`、exit 0 |
| 条款解析 | `clause_extract.py` × 五契约 | 12 + 13 + 16 + 10 + 8 = **59**，五份全 `md-bold-closed` |
| 覆盖会计 | `account-clause-coverage.py --spec-dir …`（不加 `--freeze`） | `claimed clauses 0`、`0 of 19` FRs、`59 beyond the frozen baseline`、`status: uncovered`、**exit 1**（与本轮改动前同读数） |
| `.specify/memory/` 守卫 | `python3 -m pytest -q tests/contract/test_expression_compatibility.py` | `16 passed`、exit 0 |
| 081 冻结面 | `git diff --stat d23490c3 -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py shared/workflow/acceptance-hardening.md` | 空输出 ⇒ 零 diff |

**advisories 由 82 → 84 的原因（两条，均为计划路径）**：新增段落点到两个尚不存在的路径
`shared/declarations/exclusions/no-machine-fact.yaml`（`requirements.md:203`、`contracts/migration-batches.contract.md:123`），
`missing-path` 按既有口径记 advisory，不是 error。

## 本轮不处置

- **R2-03（MEDIUM，tasks banner 的旧前提）**：不在本次授权范围（用户裁定只走路径 A）；`tasks.md:11` 与 `tasks.md:204`
  仍以「五份契约用 `DS/HC/SR/MB/DM` 编号」为由解释 `[green:]` 未启用，而实测已是 `C-001…C-059`。留给 analyze round 3
  或一次独立的 tasks 修复。
- **R2-04（LOW，历史提交信息 `DN`）**：历史不可改，不处置。
- **框架观察（`pre-analyze-check.py` 的 `CLAUSE_DEF` 认不出 `C-<digits>`）**：不属本特性。


## analyze（round 3, 2026-11-05）

```yaml
stage: analyze
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1@stage_base=b1b19e93 — (a) 改动路径覆盖 0 命中；(b) 交付物契约测试 16 命中；(c) 夹具变更 0 命中（改动集 = 27 条既有运行时记录，全部位于 .specify/memory/{session,exec-quant,feedback}/ 与 .specify/state/，没有一条落在 tests/、scripts/、skills/**/scripts/、src/ 或 tests/fixtures/）"
changed_paths[]:
  - .specify/memory/session/20261102T231648Z-run-determination-speckit-clarify-r20261102t225758z-081a.md
  - .specify/memory/exec-quant/records/20261105T075132768628Z-cf37e921.json
  - .specify/memory/exec-quant/records/20261105T080159336037Z-7f8a3419.json
  - .specify/memory/exec-quant/records/20261105T082009374970Z-a1347a99.json
  - .specify/memory/exec-quant/records/20261105T083525969720Z-0c4b8437.json
  - .specify/memory/exec-quant/records/20261105T084309278446Z-6ee2f63f.json
  - .specify/memory/exec-quant/records/20261105T085419852858Z-eb6daa1e.json
  - .specify/memory/exec-quant/records/20261105T094511658251Z-1d71de8a.json
  - .specify/memory/exec-quant/records/20261105T094750637884Z-90e0cae3.json
  - .specify/memory/feedback/20261105T075137Z-speckit-requirements.md
  - .specify/memory/feedback/20261105T080203Z-speckit-clarify.md
  - .specify/memory/feedback/20261105T082017Z-speckit-plan.md
  - .specify/memory/feedback/20261105T083530Z-speckit-tasks.md
  - .specify/memory/feedback/20261105T084312Z-speckit-checklist.md
  - .specify/memory/feedback/20261105T085423Z-speckit-analyze.md
  - .specify/memory/feedback/20261105T094516Z-speckit-analyze.md
  - .specify/memory/feedback/20261105T094753Z-skill-sdd-loop-driver.md
  - .specify/memory/session/20261105T075127Z-run-determination-speckit-requirements-r20261105t074027z-084.md
  - .specify/memory/session/20261105T080146Z-run-determination-speckit-clarify-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T082004Z-run-determination-speckit-plan-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T083523Z-run-determination-speckit-tasks-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T084306Z-run-determination-speckit-checklist-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T085413Z-run-determination-speckit-analyze-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T094508Z-run-determination-speckit-analyze-r20261105t074027z-084a-r2.md
  - .specify/memory/session/20261105T094745Z-run-determination-skill-sdd-loop-driver-r20261105t074027z-08.md
  - .specify/state/084-harness-triple-structure.md
selected_paths:
  - tests/contract/test_acceptance_premises.py
  - tests/contract/test_acceptance_state_machine.py
  - tests/contract/test_client_guard_sweep.py
  - tests/contract/test_directory_governance.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_line_state_blocked.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_non_regression_064.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_sdd_diffusion.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/contract/test_sdd_loop_driver_wrapup_accounting.py
  - tests/contract/test_validation_carrier_contract.py
  - tests/integration/test_expression_line_pilot.py
  - tests/integration/test_sdd_loop_efficiency_runner.py
sufficiency: "TB-05 的 (b) 子句对每个阶段无条件生效（交付面 = 本特性短名 `harness-triple-structure` + `skills/external/sdd-loop-driver` + docs 指针页），故本只读阶段也得到同一 16 个文件；(a) 与 (c) 为空是因为改动集不含可执行面、不含夹具。选择集与 round 2 逐文件相同，说明 stage_base 的差异没有进入选择输入"
command: "python3 -m pytest -q <上列 16 个文件>"
rc: 1
passed: 296
failed: 2
new_failures: "not_computable —— implement 起点的 baseline 槽位仍未捕获，无比较基线；改为逐条归因：0 条由本特性制品引起，2 条属环境（test_e_a_stale_pin…：git 2.54.0 钉 vs 实测 2.43.7；test_c22_watch_target_hook_selftest：mkdir /home/agent/tmp/spec-kit 权限被拒）。round 2 的第三条失败（R2-01 引起的 test_c2_no_project_side_classification_store）已随 43dcf30e 消失 —— 3 failed / 295 passed → 2 failed / 296 passed"
baseline_compare: "none available at this stage（baseline 槽位归 implement 起点；本阶段按 TB-06 只做定向集）"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/analyze-round3-targeted-run.txt
```

## Why `ran`（analyze round 3）

本阶段是**只读**阶段，改动集 27 条全部是运行时记录（session / exec-quant / feedback / 状态脊），没有一条落在可执行面或夹具。
按 TB-06 本可记 `not-run-docs-only`（六项缩减字段即可判完整）；本轮仍然**选择并实跑**同一条 16 文件定向集，理由是紧前一阶段
（plan reopen）证明了这条路线上有两个真信号：① `.specify/memory/` 的守卫测试 R2-01 曾在这里被漏过；② 无 CRITICAL/HIGH 的
一轮仍需要一条实测来把「本轮没有新失败」写成读数而不是印象。故 E3 行按更严口径记 `status: ran` 并附 `changed_paths[]`，
使缩减字段集与运行字段同时可读。

## R2 闭环读数（round 3 复测，不继承 round 2）

| 判项 | 命令 | 读数 |
|---|---|---|
| R2-01 守卫 | `python3 -m pytest -q tests/contract/test_expression_compatibility.py -k c2_no_project_side_classification_store` | `1 passed, 15 deselected`，exit 0（round 2 修复前为 failed） |
| R2-01 残留扫描 | `grep -rn "flow_class" .specify/memory/` | 12 命中 / 5 文件，**不含** `features/084.md`；该文件第 31 行为「类别读取结果：`execution`（由 `requirements.md` 的声明行解析）」，不匹配 C-2 的 `flow_class\s*[:=]` 正则 |
| R2-02 名册行数 | `C-044` / `C-045` 表行机械解析 | 批 2 余 **7** 行、批 3 余 **7** 行（原 14 / 8），14 行全部有今日引擎侧；表内唯一 `none` 是解释句里的英文词 |
| R2-02 排除记录算术 | § Facts outside the roster 的 `unit` 列去重 | 8 条事实 → **8 个排除单元**（2 analyze + 1 self-improvement + 5 improve）；`review-segment-sequence` 与 `history-categories` 零行，其单元仍 in-scope |
| R2-02 双向冲突扫描 | 八个排除单元 × `C-042`/`C-044`/`C-045` 的 carrier side | 无交集 ⇒ 不存在「既被声明覆盖又被排除行点名」（E-2 R-4） |
| R2-02 判据未反转 | `grep -rniE "read point is created\|created during migration\|post-migration criterion"` | 仅 `contracts/migration-batches.contract.md:104` 一处，且是**明确否决**该读法的句子 ⇒ 路径 B 未发生，FR-006 (i) 仍是今日树判据 |
| R2-03 banner | `tasks.md:11` / `:44` 逐字读 | 前提已为「`C-001…C-059` + `md-bold-closed` + `[green:]` 可选」，旧的 `DS/HC/SR/MB/DM` + `md-none` 前提 0 命中 |
| 条款解析 | `clause_extract.py` × 五契约 | 12 + 13 + 16 + 10 + 8 = **59**，五份全 `md-bold-closed` |
| 081 冻结面 | `git diff --stat 3ffeb26e -- …`（六路径） | 空输出 ⇒ 零 diff |

## Bases verified（analyze round 3）

| 判项 | 命令 | 结果 |
|---|---|---|
| requirements 校验 | `validate-requirements.py …/requirements.md` | `status: ok`、六判项全 pass、0 error / 0 warning、286 行 / 25 定义行 / 14 字符串、exit 0 |
| tasks 校验 | `validate-tasks.py …/tasks.md` | `PASS`、0 error / 0 warning、exit 0 |
| 决策张力 | `validate-decision-tensions.py --spec …` | `status: ok`、六 label 全 pass、4 records、`channel high=0`、exit 0 |
| 拆解门（plan） | `decomposition-check.py --mode plan …` | `proceed`，`fr_count 19` ≤ 30，`reasons=[]` |
| 拆解门（tasks） | `decomposition-check.py --mode tasks …` | `proceed`，`task_count 31` ≤ 40，`reasons=[]` |
| 前置门（三阶段） | `pre-analyze-check.py --stage {requirements,plan,tasks}` | 三次 `decision=pass`、`errors=0`、`advisories=84`、`waived=0`、exit 0 |
| 覆盖会计 | `account-clause-coverage.py --spec …`（不加 `--freeze`） | `claimed clauses 0`、`0 of 19` FRs、`59 beyond the frozen baseline`、`status: uncovered`、**exit 1**（与 round 2 同读数；范围收缩不改变车道输入） |
| 宪法对照 | `constitution.md` v1.15.0 × `plan.md` § Constitution Check | 18/18 名称逐字一致，0 缺失、0 错配、0 重排 |
| Feature 注册表 | `features.md` 头行与行数 | `Total Features: 77` = 77 行；084 行为 `Planned`、路径指 `requirements.md`、条款短语 `C-001…C-059`（旧 id 族 0 命中） |
| 定向集 | `targeted-set-v1@stage_base=b1b19e93` | (a) 0 / (b) 16 / (c) 0，与 round 2 逐文件相同 |

## gate 结论（analyze round 3）

**GATE GREEN：CRITICAL 0 / HIGH 0 / MEDIUM 3 / LOW 2。** 无 CRITICAL/HIGH ⇒ 独立校验波次按规则派发 0 个校验器
（MEDIUM/LOW 跳过校验），零发现下限由「四条单行覆盖的 FR 逐条重读 + 三行抽样」履行；三条 MEDIUM 与两条 LOW 均为
一句话级措辞/计数精度修复，落在非判据面，不阻断 `/speckit.implement`。完整判定、闭环读数与证据指针见
`analyze-report-round3-2026-11-05.md`。

## implement（Part 1, T007 收口，2026-11-05）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1@stage_base=fa7ce0f1 —— (a) 两条新增源码路径（`scripts/python/declaration_reader.py`、`scripts/python/harness-triple-check.py`）直接命中，且被触碰文档的模块 stem 把 92 个候选带入（其中一个带来真读数：`test_c57`）；(b) 交付面 16 个文件（特性短名 / `skills/external/sdd-loop-driver` / docs 指针页）；(c) 本段修改的 `tests/contract/test_harness_triple_structure.py` 自身。选择程序及其输出逐字记录在 `test-evidence/implement-part1-targeted-set.txt`"
changed_paths[]:
  - .specify/memory/exec-quant/records/20261105T075132768628Z-cf37e921.json
  - .specify/memory/exec-quant/records/20261105T080159336037Z-7f8a3419.json
  - .specify/memory/exec-quant/records/20261105T082009374970Z-a1347a99.json
  - .specify/memory/exec-quant/records/20261105T083525969720Z-0c4b8437.json
  - .specify/memory/exec-quant/records/20261105T084309278446Z-6ee2f63f.json
  - .specify/memory/exec-quant/records/20261105T085419852858Z-eb6daa1e.json
  - .specify/memory/exec-quant/records/20261105T094511658251Z-1d71de8a.json
  - .specify/memory/exec-quant/records/20261105T094750637884Z-90e0cae3.json
  - .specify/memory/exec-quant/records/20261105T111724911488Z-17c66632.json
  - .specify/memory/feedback/20261105T075137Z-speckit-requirements.md
  - .specify/memory/feedback/20261105T080203Z-speckit-clarify.md
  - .specify/memory/feedback/20261105T082017Z-speckit-plan.md
  - .specify/memory/feedback/20261105T083530Z-speckit-tasks.md
  - .specify/memory/feedback/20261105T084312Z-speckit-checklist.md
  - .specify/memory/feedback/20261105T085423Z-speckit-analyze.md
  - .specify/memory/feedback/20261105T094516Z-speckit-analyze.md
  - .specify/memory/feedback/20261105T094753Z-skill-sdd-loop-driver.md
  - .specify/memory/feedback/20261105T111730Z-speckit-analyze.md
  - .specify/memory/session/20261102T231648Z-run-determination-speckit-clarify-r20261102t225758z-081a.md
  - .specify/memory/session/20261105T075127Z-run-determination-speckit-requirements-r20261105t074027z-084.md
  - .specify/memory/session/20261105T080146Z-run-determination-speckit-clarify-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T082004Z-run-determination-speckit-plan-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T083523Z-run-determination-speckit-tasks-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T084306Z-run-determination-speckit-checklist-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T085413Z-run-determination-speckit-analyze-r20261105t074027z-084a.md
  - .specify/memory/session/20261105T094508Z-run-determination-speckit-analyze-r20261105t074027z-084a-r2.md
  - .specify/memory/session/20261105T094745Z-run-determination-skill-sdd-loop-driver-r20261105t074027z-08.md
  - .specify/memory/session/20261105T111722Z-run-determination-speckit-analyze-r20261105t074027z-084a-r3.md
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part1-attempt1-targeted-failed-names.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part1-t007-closeout-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part1-targeted-run-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part1-targeted-set.txt
  - .specify/state/084-harness-triple-structure.md
  - scripts/python/declaration_reader.py
  - scripts/python/harness-triple-check.py
  - tests/contract/test_harness_triple_structure.py
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
selected_paths:
  - tests/contract/test_acceptance_premises.py
  - tests/contract/test_acceptance_review_composition.py
  - tests/contract/test_acceptance_state_machine.py
  - tests/contract/test_checker_form.py
  - tests/contract/test_clarify_semantic_completeness.py
  - tests/contract/test_clause_coverage.py
  - tests/contract/test_cleanup_obsolete_assets.py
  - tests/contract/test_client_guard_sweep.py
  - tests/contract/test_closure_acceptance_check.py
  - tests/contract/test_coaching_run_contract.py
  - tests/contract/test_decision_tension_contract.py
  - tests/contract/test_delegation_classes.py
  - tests/contract/test_directory_governance.py
  - tests/contract/test_doc_consistency_checker.py
  - tests/contract/test_docs_command_template.py
  - tests/contract/test_docs_gate_driver.py
  - tests/contract/test_docs_step_injection.py
  - tests/contract/test_evidence_binding_contract.py
  - tests/contract/test_exec_quant_aggregate.py
  - tests/contract/test_exec_quant_channel_boundary.py
  - tests/contract/test_exec_quant_channel_compat.py
  - tests/contract/test_exec_quant_engine.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_expression_faces.py
  - tests/contract/test_expression_gate_wiring.py
  - tests/contract/test_expression_gates_doc.py
  - tests/contract/test_fast_fail_discipline.py
  - tests/contract/test_feedback_entry_schema.py
  - tests/contract/test_feedback_utils_cli.py
  - tests/contract/test_flow_class_ledger.py
  - tests/contract/test_gate_wiring_081.py
  - tests/contract/test_glossary_mechanism.py
  - tests/contract/test_green_point_claim.py
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_humanize_command_surface.py
  - tests/contract/test_isomorphism_map.py
  - tests/contract/test_ledger_reconciliation.py
  - tests/contract/test_line_state_blocked.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_measurement_instruments.py
  - tests/contract/test_migration_distribution.py
  - tests/contract/test_nested_sdd_invocation.py
  - tests/contract/test_neutrality_budget.py
  - tests/contract/test_non_regression_064.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_objective_analysis_gate.py
  - tests/contract/test_premise_carrier_contract.py
  - tests/contract/test_probe_nonentity_catalog.py
  - tests/contract/test_review_code_composition.py
  - tests/contract/test_run_skills_wiring.py
  - tests/contract/test_sdd_diffusion.py
  - tests/contract/test_sdd_invocation_governance.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_gates.py
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/contract/test_sdd_loop_driver_wp_coordination.py
  - tests/contract/test_sdd_loop_driver_wrapup_accounting.py
  - tests/contract/test_self_improvement_conformance.py
  - tests/contract/test_skill_layer_visibility_guards.py
  - tests/contract/test_specify_script_paths.py
  - tests/contract/test_stage_class_wiring.py
  - tests/contract/test_status_gate_owner.py
  - tests/contract/test_summarize_project_prompt_assets.py
  - tests/contract/test_token_efficiency_feedback.py
  - tests/contract/test_trigger_engine.py
  - tests/contract/test_trigger_seed_derivation.py
  - tests/contract/test_validate_tasks_parallel_safety.py
  - tests/contract/test_validation_carrier_contract.py
  - tests/integration/test_docs_command_scenarios.py
  - tests/integration/test_expression_line_pilot.py
  - tests/integration/test_feedback_exec_quant_channel.py
  - tests/integration/test_hugo_scaffold_scenarios.py
  - tests/integration/test_sdd_loop_efficiency_runner.py
  - tests/integration/test_trigger_promotion.py
  - tests/integration/test_trigger_telemetry.py
  - tests/integration/test_trigger_tuning.py
  - tests/integration/test_wp_coordination_dry_runs.py
  - tests/unit/test_admission_check.py
  - tests/unit/test_audit_plan_changes.py
  - tests/unit/test_audit_test_budget.py
  - tests/unit/test_decomposition_check.py
  - tests/unit/test_derive_live_log.py
  - tests/unit/test_feedback_exec_quant_payload.py
  - tests/unit/test_feedback_package.py
  - tests/unit/test_flow_class_check.py
  - tests/unit/test_isomorphism_checker.py
  - tests/unit/test_loop_state_engine.py
  - tests/unit/test_memory_utils.py
  - tests/unit/test_pre_analyze_check.py
  - tests/unit/test_renumber_engine.py
  - tests/unit/test_trigger_utils_units.py
  - tests/unit/test_wp_gate.py
sufficiency: "92 个文件、2349 收集 → 2330 passed / 16 failed / 3 skipped。三个子句各自有贡献：(a) 由两条新增源码路径直接命中，并经 `tasks` 这类通用 stem 过度选择（这正是 `test_isomorphism_map.py` 与 `test_client_guard_sweep.py` 进集合的原因，后者带来一条真读数）；(b) 复现前序阶段的同一交付面；(c) 选中本段唯一被改的 `test_roots` 文件。**集合到不了的地方如实写明**：(a) 是按文本搜索，只能找到*点名*了改动路径的测试，故镜像对测试（`test_mirror_parity_suite.py`、`test_scripts_distribution_parity.py`）落在集合外；本轮以**披露式补充运行**取得该读数并单独记录，MUST NOT 合并进 `selected_paths[]`（看到结果再扩集合会让记录本身不可读）"
command: "python3 -m pytest -q <上列 92 个文件>"
rc: 1
passed: 2330
failed: 16
skipped: 3
new_failures: "相对 E2 的 23 名比较集，集合内 3 条不在基线里，逐条归因，0 条可被读作静默吸收：① `test_client_guard_sweep.py::test_c57_shipped_text_adds_no_fresh_neutrality_violation` —— `shared/declarations/contract.yaml` 头部注释写了 `Feature 084`，触犯既有 072 中性化守卫；该文件是 T003 产物、不在本段声明的写域内，按 FF-11 上送而不就地改（见回传 ANOMALY 行与 closeout § 6a）；② `test_ng_08_mirror_no_new_drift` 与 ③ `test_trigger_engine.py::test_c2_sync_mirrors_check_clean` —— 镜像未投影，T026 的所有物，`baseline-reading-2026-11-05.md` 已写明「T026 之前该两条按构造为红」"
baseline: "E2 `slot=baseline` 行（状态脊 `<!-- test-budget:begin -->` 的 `seq:1`，25F / 7151P / 4S，比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名，另 2 条镜像为在途）。本行按该 23 名做 `comm -23` 差额"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part1-targeted-run-2026-11-05.txt（两次运行完整 stdout：run 1 = 发现轮，run 2 = 清理陈旧 scratch 后的终树读数）
```

## Why `ran`

本段改的是可执行面（两个新引擎 + 一条契约测试腿），落 `not-run-docs-only` 就是假绿。按 TB-05 的固定程序选
92 个文件并实跑两次：**run 1** 在接手时的树上跑（18 failed），**run 2** 在清掉上一位执行者遗留的 scratch 后
跑（16 failed）。两次都在本文件里，前者是发现轮、后者是终树读数，谁都不替代谁。

## T006 / T007 收口读数

| 判项 | 命令 | 读数 | 证据 |
|---|---|---|---|
| 契约测试模块 | `python3 -m pytest tests/contract/test_harness_triple_structure.py -q` | **22 passed**（T005 交付时 20 failed / 1 passed，两个主体都不存在） | 本行即读数 |
| reader 双形态（C-053） | 从 `scripts/python/` 执行 `python3 -c "import declaration_reader"`；`declaration_reader.py --action {list,get}` | import 成功、两个 CLI 动作各自 exit 0，`normalize_path` 只剥一层 `.specify/` | closeout § 1 |
| 子集语法（C-008） | 对 `parse_subset` 逐构造驱动 11 个禁用构造 + 5 个允许构造 | 11 个禁用构造全部 `template=STR-010` 拒绝、无一被"尽力解析"；5 个允许构造正常读出 | closeout § 2 |
| 完整性三条件（E-6） | 同一 `negative-duplicated-fact-literal/` 树上跑修前 / 修后引擎 | 修前 `state: complete`（假绿），修后 `state: pending` + `reason: duplicated-fact-literal`；exit 均为 1 | closeout § 3 |
| verify 不误报理由 | 同一树上修前 / 修后 `--action verify` | 两版输出逐字节相同：只发 `STR-011` 一条，未追加一条理由错位的 `STR-009` | closeout § 3 |
| 只读（C-039） | 模块腿 `test_a_run_leaves_the_judged_tree_byte_identical`（`git status --porcelain` 前后比对） | 绿；在本仓真树上跑 `coverage` 得 `candidates: 83 / unclassified: 83`、exit 1（批次 1 未迁，属读数） | 本行即读数 |
| 单一解析器守卫（C-058） | 模块腿 `test_the_shared_read_entry_is_the_only_subset_parser` | 绿：检出集合 = `{declaration_reader.py}` ∪ 两个 N4 祖父（`execution-config.py`、`gate-check.py`） | 本行即读数 |

## 三件补充读数（都在本轮实跑，不与选择集混记）

1. **陈旧 scratch 是两个失败的因，清掉即消**：`test_isomorphism_map.py` 扫全仓 `.md`，上一位执行者留在
   `.specify/.tmp/084-impl-p1/pristine/` 的 80 MB `git archive` 树被当成"第二份映射载体"。该树的用途（把 E2 的
   25 条拆成 23 + 2）已记在 `baseline-reading-2026-11-05.md`，按 Temporary Directory Discipline 清除后
   `tests/contract/test_isomorphism_map.py` 两个腿转绿，`test_client_guard_sweep.py` 51 passed 只剩 c57 一条。
   这不是"把红的弄绿"，是删掉本不该存在的目录。
2. **镜像补充运行**（披露式，不进 `selected_paths[]`）：
   `python3 -m pytest -q tests/contract/test_mirror_parity_suite.py tests/contract/test_scripts_distribution_parity.py`
   → `6 failed, 761 passed`，六条全是未投影的镜像对（本段两个新引擎 + 之前四件），T026 的所有物；
   手工补镜像＝FF-12 的错误帽子，MUST NOT。
3. **上送项**：`test_c57` 命中的是 T003 的 `shared/declarations/contract.yaml`（注释里的 `Feature 084`），
   一行注释即可修，但越出本段声明的写域（FF-11），故停在本层、连同上送件形态回抛驱动者。

## Bases verified（implement Part 1 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| 任务清单可解析 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/084-harness-triple-structure/tasks.md` | `PASS`，`0 error(s), 0 warning(s)`，exit 0；T001–T007 已勾，31 行结构与任务数未动 |
| plan 权威零触碰 | `git diff --stat fa7ce0f1 -- .specify/specs/084-harness-triple-structure/{plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出（本段无 PLAN-EDIT） |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集只含 reader / checker / `tasks.md` / 本行 / 四件证据；`.specify/memory/**`、`.specify/state/**` 不提交 |
| 不 push | `git log --oneline -1` 本地提交 | 未执行任何 push |


## implement（Part 2a，T008–T012 收口，2026-11-05）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1@stage_base=3ad6a85c —— 三个子句：(a) 本段改动面 11 个 token（`scripts/python/{feedback-utils,evidence-utils,flow-class-check,declaration_reader}.py`、`shared/declarations/`、`shared/workflow/{feedback-step,evidence-step}.md`、`shared/definitions/flow-class-definitions.md`、`shared/guidelines/better-harness.md`、`skills/internal/collect-evidence/`、`docs/reference/skills/feedback.md`）在 `tests/{contract,integration,unit,scenarios}/test_*.py` 上做文本命中，得 87 个文件；(b) 补 5 个直接 import 迁移引擎而不点名路径的模块（`test_feedback_utils.py`、`test_feedback_threshold.py`、`test_feedback_dedup.py`、`test_feedback_probe_entry_schema.py`、`test_docs_utils_cli.py`），得 92 文件的独立选择集，作为 discovery 轮全量捕获（`implement-part2a-closure-targeted-run-2026-11-05.txt`，27F/2095P）；(c) 终树读数改用 attempt 1 的 235 文件集（`implement-part2a-targeted-set.txt`），使轮间可比，并已机械核对 92 集是其真子集（`small - big = ∅`）"
changed_paths[]:
  - shared/declarations/facts/evidence-lanes.yaml
  - shared/declarations/facts/evidence-seven-states.yaml
  - shared/declarations/facts/feedback-prompt-threshold.yaml
  - shared/declarations/facts/flow-class-basis.yaml
  - shared/declarations/facts/flow-class-classes.yaml
  - shared/declarations/facts/flow-class-document-types.yaml
  - shared/declarations/facts/flow-class-ledger-columns.yaml
  - shared/declarations/facts/flow-class-neutral-categories.yaml
  - scripts/python/declaration_reader.py
  - scripts/python/evidence-utils.py
  - scripts/python/feedback-utils.py
  - scripts/python/flow-class-check.py
  - shared/definitions/flow-class-definitions.md
  - shared/guidelines/better-harness.md
  - shared/workflow/evidence-step.md
  - shared/workflow/feedback-step.md
  - skills/internal/collect-evidence/SKILL.md
  - skills/internal/collect-evidence/references/evidence-discipline.md
  - docs/reference/skills/feedback.md
  - tests/contract/test_compile_embeds.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_store_state_protocol.py
  - .specify/specs/084-harness-triple-structure/tasks.md
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/specs/084-harness-triple-structure/test-evidence/us1-single-definition-point.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-set.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-run-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-run-r2-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-closure-targeted-run-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-closure-targeted-run-r2-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-mirror-parity-supplemental-2026-11-05.txt
selected_paths[]:
  - tests/contract/test_acceptance_review_composition.py
  - tests/contract/test_acceptance_schema_ownership.py
  - tests/contract/test_acceptance_state_machine.py
  - tests/contract/test_agent_chain_guards.py
  - tests/contract/test_agent_dispatch_mechanism.py
  - tests/contract/test_agent_env_config_contract.py
  - tests/contract/test_agent_skill_enablement.py
  - tests/contract/test_agent_specific_config_skills.py
  - tests/contract/test_baseline_preflight_contract.py
  - tests/contract/test_clarify_semantic_completeness.py
  - tests/contract/test_clause_coverage.py
  - tests/contract/test_cleanup_obsolete_assets.py
  - tests/contract/test_client_armed_state.py
  - tests/contract/test_client_capture.py
  - tests/contract/test_client_guard_sweep.py
  - tests/contract/test_client_improve_loop.py
  - tests/contract/test_client_metrics.py
  - tests/contract/test_client_package_exclusion.py
  - tests/contract/test_coaching_dispatch_contract.py
  - tests/contract/test_coaching_expectation_contract.py
  - tests/contract/test_coaching_observation_contract.py
  - tests/contract/test_coaching_run_contract.py
  - tests/contract/test_coaching_wiring_contract.py
  - tests/contract/test_code_review_skill_contract.py
  - tests/contract/test_compile_embeds.py
  - tests/contract/test_compile_propagation_order.py
  - tests/contract/test_compile_reconcile_guards.py
  - tests/contract/test_confirmation_gates_sweep.py
  - tests/contract/test_constitution_double_landing.py
  - tests/contract/test_criterion_subject.py
  - tests/contract/test_decision_tension_contract.py
  - tests/contract/test_delegation_classes.py
  - tests/contract/test_derive_command_surface.py
  - tests/contract/test_directory_governance.py
  - tests/contract/test_doc_consistency_checker.py
  - tests/contract/test_docs_command_template.py
  - tests/contract/test_docs_gate_driver.py
  - tests/contract/test_docs_step_injection.py
  - tests/contract/test_docs_target_structure_declaration.py
  - tests/contract/test_docs_utils_cli.py
  - tests/contract/test_document_structure_gate.py
  - tests/contract/test_dogfooding_practice.py
  - tests/contract/test_engine_face_contract.py
  - tests/contract/test_evidence_binding_contract.py
  - tests/contract/test_evidence_findings_schema.py
  - tests/contract/test_evidence_step_conformance.py
  - tests/contract/test_evidence_utils_cli.py
  - tests/contract/test_exec_quant_aggregate.py
  - tests/contract/test_exec_quant_channel_boundary.py
  - tests/contract/test_exec_quant_channel_compat.py
  - tests/contract/test_exec_quant_engine.py
  - tests/contract/test_export_skill_rework.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_expression_faces.py
  - tests/contract/test_expression_gate_wiring.py
  - tests/contract/test_expression_gates_doc.py
  - tests/contract/test_fast_fail_discipline.py
  - tests/contract/test_feedback_command_classification.py
  - tests/contract/test_feedback_command_template.py
  - tests/contract/test_feedback_entry_schema.py
  - tests/contract/test_feedback_exec_quant_payload.py
  - tests/contract/test_feedback_intake_exec_quant.py
  - tests/contract/test_feedback_introspection_engine.py
  - tests/contract/test_feedback_introspection_report.py
  - tests/contract/test_feedback_mechanism_boundary.py
  - tests/contract/test_feedback_probe_cli.py
  - tests/contract/test_feedback_probe_entry_schema.py
  - tests/contract/test_feedback_probe_registry.py
  - tests/contract/test_feedback_skill_conformance.py
  - tests/contract/test_feedback_step_reference_form.py
  - tests/contract/test_feedback_two_path_routing.py
  - tests/contract/test_feedback_utils_cli.py
  - tests/contract/test_flat_internal_skill_migration.py
  - tests/contract/test_flow_class_correctness.py
  - tests/contract/test_flow_class_ledger.py
  - tests/contract/test_flow_class_spec_declaration.py
  - tests/contract/test_focus_target_resolution.py
  - tests/contract/test_gate_wiring_081.py
  - tests/contract/test_git_workflow_instructions_block.py
  - tests/contract/test_glossary_mechanism.py
  - tests/contract/test_goal_migration.py
  - tests/contract/test_goal_targets_engine.py
  - tests/contract/test_green_point_claim.py
  - tests/contract/test_handler_registry.py
  - tests/contract/test_handoff_chain.py
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_hermes_init_contract.py
  - tests/contract/test_hidden_edge_two_cycle.py
  - tests/contract/test_hugo_scaffold_contract.py
  - tests/contract/test_humanize_command_surface.py
  - tests/contract/test_improve_team_presence.py
  - tests/contract/test_instructions_size_budget.py
  - tests/contract/test_isomorphism_map.py
  - tests/contract/test_knowledge_promotion.py
  - tests/contract/test_ledger_reconciliation.py
  - tests/contract/test_lifecycle_detach_reattach.py
  - tests/contract/test_line_envelope_contract.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_measurement_instruments.py
  - tests/contract/test_merge_provenance_gate.py
  - tests/contract/test_migration_distribution.py
  - tests/contract/test_nested_run_report.py
  - tests/contract/test_nested_sdd_invocation.py
  - tests/contract/test_neutrality_budget.py
  - tests/contract/test_no_nested_skills.py
  - tests/contract/test_no_organize_agents_refs.py
  - tests/contract/test_no_retired_draw_skill_refs.py
  - tests/contract/test_non_regression_064.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_objective_analysis_gate.py
  - tests/contract/test_phase2_bindings.py
  - tests/contract/test_portable_skill_creation.py
  - tests/contract/test_premise_carrier_contract.py
  - tests/contract/test_probe_engine_action_sets.py
  - tests/contract/test_probe_registry_umbrella.py
  - tests/contract/test_problem_solving_naming.py
  - tests/contract/test_project_custom_template.py
  - tests/contract/test_record_retention_engine.py
  - tests/contract/test_registry_completeness.py
  - tests/contract/test_render_evidence_geometry.py
  - tests/contract/test_reproduction_fidelity_readback.py
  - tests/contract/test_requirements_checker.py
  - tests/contract/test_requirements_convention_entry_points.py
  - tests/contract/test_resource_id_generation.py
  - tests/contract/test_resource_id_resolution.py
  - tests/contract/test_review_code_composition.py
  - tests/contract/test_review_docs_isomorphism.py
  - tests/contract/test_review_feedback_boundary.py
  - tests/contract/test_review_p1_checklist_governance.py
  - tests/contract/test_review_p1_recheck_waiver.py
  - tests/contract/test_review_p1_review_loop.py
  - tests/contract/test_run_checks.py
  - tests/contract/test_run_determination_engine.py
  - tests/contract/test_run_determination_passive_wiring.py
  - tests/contract/test_run_skills_wiring.py
  - tests/contract/test_runtime_mode_gate.py
  - tests/contract/test_sanitize_renumber_lane.py
  - tests/contract/test_sanitize_retention_lane.py
  - tests/contract/test_sanitize_template.py
  - tests/contract/test_scan_confirmation_gates.py
  - tests/contract/test_sdd_carrier_contract.py
  - tests/contract/test_sdd_compat_containment.py
  - tests/contract/test_sdd_diffusion.py
  - tests/contract/test_sdd_house_keeping_skill.py
  - tests/contract/test_sdd_invocation_governance.py
  - tests/contract/test_sdd_loop_driver_cli_profiles.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_gates.py
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/contract/test_sdd_loop_driver_watch_iteration.py
  - tests/contract/test_sdd_loop_driver_wp_coordination.py
  - tests/contract/test_sdd_loop_driver_wp_preset.py
  - tests/contract/test_sdd_loop_driver_wrapup_accounting.py
  - tests/contract/test_sdd_project_setup_skill.py
  - tests/contract/test_sdd_routing_definitions.py
  - tests/contract/test_sdd_three_skill_contract.py
  - tests/contract/test_seat_instantiation_flow.py
  - tests/contract/test_self_improvement_conformance.py
  - tests/contract/test_shared_reference_directory.py
  - tests/contract/test_shared_reference_rewrite.py
  - tests/contract/test_shipped_surface_client_neutrality.py
  - tests/contract/test_single_agent_purity.py
  - tests/contract/test_single_conceptual_model.py
  - tests/contract/test_skill_install_layout_contract.py
  - tests/contract/test_skill_layer_visibility_guards.py
  - tests/contract/test_skill_verification_discriminability.py
  - tests/contract/test_skills_symlink_regression.py
  - tests/contract/test_stage_class_wiring.py
  - tests/contract/test_status_gate_owner.py
  - tests/contract/test_store_state_protocol.py
  - tests/contract/test_summarize_project_prompt_assets.py
  - tests/contract/test_summary_trigger.py
  - tests/contract/test_summary_writeset.py
  - tests/contract/test_sync_mirrors_only.py
  - tests/contract/test_teaching_surfaces.py
  - tests/contract/test_team_command_routing.py
  - tests/contract/test_token_efficiency_discipline.py
  - tests/contract/test_token_efficiency_feedback.py
  - tests/contract/test_token_efficiency_gates.py
  - tests/contract/test_tools_command_routing.py
  - tests/contract/test_tools_inventory_ownership.py
  - tests/contract/test_trigger_engine.py
  - tests/contract/test_trigger_seed_derivation.py
  - tests/contract/test_upgrade_end_state.py
  - tests/contract/test_user_facing_comprehension_pointers.py
  - tests/contract/test_validate_tasks_parallel_safety.py
  - tests/contract/test_validation_carrier_contract.py
  - tests/contract/test_workspace_isolation_contract.py
  - tests/contract/test_wrap_up_line_budget.py
  - tests/contract/test_wrap_up_wording_gate_safe.py
  - tests/integration/test_agents_creation.py
  - tests/integration/test_evidence_compare_verdict.py
  - tests/integration/test_evidence_python_lanes.py
  - tests/integration/test_expression_line_pilot.py
  - tests/integration/test_feedback_command_record.py
  - tests/integration/test_feedback_dedup.py
  - tests/integration/test_feedback_exec_quant_channel.py
  - tests/integration/test_feedback_partial.py
  - tests/integration/test_feedback_selective_triggering.py
  - tests/integration/test_feedback_skill_record.py
  - tests/integration/test_feedback_threshold.py
  - tests/integration/test_goal_reference.py
  - tests/integration/test_persistent_agent_lifecycle.py
  - tests/integration/test_resource_id_resolution.py
  - tests/integration/test_sanitize_us1.py
  - tests/integration/test_sanitize_us2.py
  - tests/integration/test_sanitize_us3.py
  - tests/integration/test_sdd_house_keeping_flow.py
  - tests/integration/test_session_kill_reattach.py
  - tests/integration/test_shared_dir_install.py
  - tests/integration/test_skill_install_layout_integration.py
  - tests/integration/test_skills_resource_ids.py
  - tests/integration/test_worktree_integration_queue.py
  - tests/integration/test_zero_sdd_workflow_references.py
  - tests/unit/test_feedback_exec_quant_payload.py
  - tests/unit/test_feedback_intake_exec_quant.py
  - tests/unit/test_feedback_package.py
  - tests/unit/test_feedback_utils.py
  - tests/unit/test_flow_class_check.py
  - tests/unit/test_flow_class_spec_key.py
  - tests/unit/test_isomorphism_checker.py
  - tests/unit/test_reconciler_extensions.py
  - tests/unit/test_record_retention_helpers.py
  - tests/unit/test_renumber_engine.py
  - tests/unit/test_resource_id_helpers.py
  - tests/unit/test_rewrite_paths_skill_layers.py
  - tests/unit/test_sanitize_checks_index.py
  - tests/unit/test_sanitize_checks_migration.py
  - tests/unit/test_sanitize_checks_mirror.py
  - tests/unit/test_sanitize_checks_refs.py
  - tests/unit/test_sanitize_semantic.py
  - tests/unit/test_skills_utils_layout.py
  - tests/unit/test_tier_classification.py
  - tests/unit/test_two_layer_skills_copy.py
  - tests/unit/test_workspace_root_resolution.py
sufficiency: "235 个文件、4368 收集 → 4346 passed / 21 failed / 1 skipped（196 s）；attempt 1 同一集合的终树读数为 4333 passed / 34 failed（`implement-part2a-targeted-run-r2-2026-11-05.txt`），差集的 13 个 id 全部是本段修好的「引擎已改、夹具未带 `declaration_reader.py`」一类，逐条见下方 § 13 条夹具修复。集合的三个子句各有贡献：(a) 直接命中三个迁移引擎与其载体，并经 `evidence-utils`、`feedback` 这类通用 stem 过度选择（`test_coaching_wiring_contract.py`、`test_compile_*` 就是这样进来的，而它们恰好带出 13 条真读数）；(b) 引擎以 import 形式被使用的模块，文本命中抓不到，只能手工补；(c) 与 attempt 1 同集，保证轮间可比。**集合到不了的地方如实写明**：镜像对测试（`test_mirror_parity_suite.py`、`test_scripts_distribution_parity.py`）不在 `selected_paths[]` 内，本轮以披露式补充运行取得读数（`implement-part2a-mirror-parity-supplemental-2026-11-05.txt`，23F/752P），MUST NOT 并入本行计数"
command: "python3 -m pytest -q <上列 235 个文件>"
rc: 1
passed: 4346
failed: 21
skipped: 1
new_failures:
  - "tests/contract/test_coaching_wiring_contract.py::test_c3_mirrors_and_command_copies_are_zero_drift —— `sync-mirrors.py --check` exit 2 —— 本段改的 5 个镜像对未投影（T026 所有物）"
  - "tests/contract/test_coaching_wiring_contract.py::test_c8_the_verification_surface_runs_green —— 同一原因：验证面里 `mirrors` 一项红（同一条 drift 读数）"
  - "tests/contract/test_compile_propagation_order.py::test_propagation_chain_is_green_in_canonical_order —— 同一原因：canonical 链第 3 步 `sync --check` 红"
  - "tests/contract/test_dogfooding_practice.py::test_c4_engine_mirror_untouched —— `scripts/python/feedback-utils.py` 与其镜像字节不同 —— 同一原因"
  - "tests/contract/test_evidence_step_conformance.py::TestEvidenceStepConvention::test_mirrored_to_source_side —— `shared/workflow/evidence-step.md` 与其镜像不同 —— 同一原因"
  - "tests/contract/test_expression_compatibility.py::test_c7_mirrors_are_byte_identical —— 三个镜像对（`flow-class-check.py`、`flow-class-definitions.md`、`feedback-step.md`）—— 同一原因"
  - "tests/contract/test_non_regression_064.py::test_ng_08_mirror_no_new_drift —— `shared/definitions` 的 drift 集新增两个文件名 —— 同一原因"
  - "tests/contract/test_sdd_loop_driver_wrapup_accounting.py::test_runtime_mirrors_match_sources[src2-dst2] —— `shared/workflow/feedback-step.md` 镜像陈旧 —— 同一原因"
  - "tests/contract/test_self_improvement_conformance.py::test_c10_runtime_skill_mirrors_are_current —— `internal/collect-evidence` 技能镜像陈旧 —— 同一原因"
  - "tests/contract/test_sync_mirrors_only.py::TestOnlyScoping::test_only_file_scopes_check_to_its_pair —— `--only scripts/python/feedback-utils.py` 读到 DIFF —— 同一原因"
  - "tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean —— `sync-mirrors --check` exit 2 —— 同一原因（`baseline-reading-2026-11-05.md` 已把该 id 归为「T026 之前按构造为红」）"
baseline: "E2 `slot=baseline` 行（状态脊 `<!-- test-budget:begin -->` 的 `seq:1`：25F / 7151P / 4S，比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名，另 2 条镜像为在途）。本行按该 23 名做 `comm -23` 差额，得 11 条，无一落在迁移本身"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-closure-targeted-run-r2-2026-11-05.txt（终树读数，完整 stdout + rc；discovery 轮见 implement-part2a-closure-targeted-run-2026-11-05.txt，attempt 1 的两轮见 implement-part2a-targeted-run-2026-11-05.txt 与 ...-r2-...）
```

## Why `ran`

本段改的是可执行面：三个引擎的读取路径换成共享入口、8 个新声明、4 个载体从复述改指针、3 个测试模块的
夹具补齐读取入口。这些都不是文档整理，落 `not-run-docs-only` 就是假绿。两轮读数都在本文件对应行的
`evidence_ptr` 里：**discovery 轮**（92 文件独立选择集，27F/2095P）先把失败面暴露出来，**终树轮**
（235 文件集，21F/4346P）是修完夹具后的读数，谁都不替代谁。

## 13 条夹具修复（本段唯一的代码侧修复，且是纠正而非裁定）

**症状**：`test_compile_embeds` 3 条、`test_compile_reconcile_guards` 7 条、`test_engine_face_contract`
3 条，共 13 个 id，症状一律是 `json.decoder.JSONDecodeError: Expecting value: line 1 column 1`
（被测引擎的 stdout 为空）。**根因一行**：`tests/contract/test_compile_embeds.py` 的 `_ENGINE_COPIES`
把 `feedback-utils.py` 拷进沙盒 workspace 却没带 `declaration_reader.py`，于是：

```text
error: handler 'h-feedback-record': engine scripts/python/feedback-utils.py --action args-manifest failed
(rc=1): ModuleNotFoundError: No module named 'declaration_reader'
```

**修法**：把读取入口加进该夹具的引擎拷贝清单，并注明它属于 payload 的一部分。**为什么是纠正**：同一个
读法已被工作树里两处同形修复确立（`test_store_state_protocol.py` 的 fixture repo、
`test_expression_compatibility.py` 的 `_client_shape`，都是「夹具要带兄弟模块」），改动局部、可逆、未
证伪任何下游前提；断言一句没改、没有 `skip`、也没有放宽比较。**为什么不是改引擎**：
`declaration_reader.py` 与引擎同目录分发（C-052 / FR-013），一棵「有引擎没读取入口」的树不是更小的
payload，而是不存在的 payload；让引擎对缺失的兄弟模块静默降级，会把 `[[STR-014]]` 的语义与「模块缺失」
混成一件事。

## T010 的三条读数（逐字见 `test-evidence/us1-single-definition-point.txt`）

| 判项 | 命令 | 读数 |
|---|---|---|
| lookup 点出 slug | `harness-triple-check.py --action lookup --unit-id shared/workflow/feedback-step.md` | `disposition: in-scope`、`state: complete`、`fact: feedback-prompt-threshold kind=threshold`；exit **1**（引擎聚合码，80 条 `unclassified-candidate` 全属批次 2/3） |
| verify | `harness-triple-check.py --action verify` | 8 declarations / 83 candidates、前向 `9/9`、后向 `4/4`、0 条 finding 点名该 unit、0 条 `no-read-point`；exit **1** |
| duplicate face | `doc-consistency-check.py --action verify --faces duplicate --owner-path shared/workflow/feedback-step.md --spec-dir ...` | `duplicate=pass`、`files_scanned: 14`、`findings: 0`；exit **0** |

verify 的 exit=1 要明写而不是含混过去：T010 所属的 US1 Independent Test 原文写「`--action verify` exits 0
for it」。按 **unit** 读，这句今天成立——该 unit 没有任何 finding，`state: complete`，两个方向的计分都
满；按 **树** 读，它要等到批次 2/3 与排除层落地之后，C-043 正是把这两者分开：exit-0 的判据是
`[[STR-013]]` 的条数，今天有 80 条，全部属于本段不迁的单元。本行记的是实测的 `1`，不是希望中的 `0`。

## 未做的两件事（边界明写）

1. **镜像不手改**：`sync-mirrors.py --check` 报出的 DIFF/MISS 全部留给 T026 的
   `sync-mirrors.py --write`。本行 `new_failures` 的 11 条全部落在这一类；披露式补充运行（镜像对
   23F/752P）只是把该类读数钉死，不构成修它的授权（FF-12：手工投影＝戴错帽子）。
2. **不跑全量**：本段沿用 E2 那一次全量基线，只有定向集。

## Bases verified（implement Part 2a 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| 任务清单可解析 | `python3 scripts/python/validate-tasks.py .specify/specs/084-harness-triple-structure/tasks.md` | `PASS`，`0 error(s), 0 warning(s)`，exit 0；T008–T012 已勾，仍开放 19 行（T013 起） |
| plan-owned 零触碰 | `git diff --stat 3ad6a85c -- {plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出（本段无 PLAN-EDIT，故无 PLAN-EDIT 声明） |
| 依赖面未动 | `git diff --stat 4b65517c -- pyproject.toml` | 空输出 |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/**` 与 `.specify/state/**` |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## implement（Part 2b，T013–T014 有界收口，2026-11-05）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1@stage_base=16dcbdf2 —— 29 个文件，四个来源：(a) 本段改动面直接命中（`scripts/python/{flow-class-check,validate-requirements,closure-acceptance-check}.py`、`shared/declarations/facts/`、`shared/workflow/{expression-gates,acceptance-hardening}.md`、`templates/commands/requirements.md`）；(b) 081 的两个验收文件与 closure 面（T013 行自带硬约束）；(c) flow-class / driver / gate-owner 相关契约与单元测试（`test_isomorphism_map`、`test_loop_state_contract`、`test_sdd_loop_driver_skill`、`test_acceptance_premises`、`test_non_regression_070` 等）；(d) 载体模板改动后的四处生成副本同步守卫（`test_run_checks`、`test_user_facing_comprehension_pointers`、`test_fast_fail_discipline`、`test_humanize_command_surface`）——第一轮 25 文件读数里 `regen-command-copies.py --check` 的 drift 就是被这一组抓出来的。集合逐行见 `test-evidence/implement-part2b-targeted-set.txt`"
selected_paths:
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_requirements_checker.py
  - tests/contract/test_checker_form.py
  - tests/contract/test_closure_acceptance_check.py
  - tests/contract/test_gate_wiring_081.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_expression_faces.py
  - tests/contract/test_expression_gates_doc.py
  - tests/contract/test_expression_gate_wiring.py
  - tests/contract/test_isomorphism_map.py
  - tests/contract/test_flow_class_correctness.py
  - tests/contract/test_flow_class_ledger.py
  - tests/contract/test_flow_class_spec_declaration.py
  - tests/contract/test_stage_class_wiring.py
  - tests/contract/test_ledger_reconciliation.py
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_acceptance_premises.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_gates.py
  - tests/unit/test_flow_class_check.py
  - tests/unit/test_isomorphism_checker.py
  - tests/unit/test_pre_analyze_check.py
  - tests/unit/test_loop_state_engine.py
  - tests/contract/test_run_checks.py
  - tests/contract/test_user_facing_comprehension_pointers.py
  - tests/contract/test_fast_fail_discipline.py
  - tests/contract/test_humanize_command_surface.py
sufficiency: "29 个文件、923 收集 → 909 passed / 14 failed / 0 skipped（37 s，终树读数；同一集合的首轮为 659 passed / 13 failed，差异全部来自第 (d) 组补入的 4 个文件与随后的一次生成副本同步）。四个来源各有贡献：(a) 直接覆盖本段改动的四个可执行面与四个载体；(b) 081 的两个验收文件同时承担 T013 的「零改动 + 零新增失败」硬约束；(c) driver / gate-owner 面把「驱动事实未迁移」写成读数而不是印象；(d) 补入后立刻抓出一次真实回归——载体模板改动后四处 per-tool 副本未重新生成，`regen-command-copies.py --check` exit 1。**集合到不了的地方如实写明**：镜像对测试（`test_mirror_parity_suite.py`、`test_scripts_distribution_parity.py`）与本段无关（镜像投影属 T026），未纳入；全量套件按预算不跑，E2 的 25F/7151P 仍是唯一全量读数"
command: "python3 -m pytest -q <上列 29 个文件>"
rc: 1
passed: 909
failed: 14
skipped: 0
new_failures:
  - "tests/contract/test_flow_class_ledger.py::test_no_second_classification_data_file —— `shared/declarations/facts/flow-class-ledger-columns.yaml: data file mentions the class key 'flow_class'`。**不是本段引入**：该声明由 T012（Part 2a）产出、随 `16dcbdf2` 入库，而该测试的扫描面是 `git ls-files`（被跟踪文件）——文件在 Part 2a 自己的读数轮里还是未跟踪状态，故当时不可见，入库后才被判到。两类修法都被封：改声明会抹掉台账列名（引擎按名列比对），改守卫要动 `tests/contract/test_flow_class_ledger.py`（SC-006 的零 diff 侧）。按 FF-11 上送，不就地修平"
  - "tests/contract/test_expression_compatibility.py::test_c7_mirrors_are_byte_identical —— `flow-class-check.py` / `flow-class-definitions.md` / `expression-gates.md` / `feedback-step.md` 四个镜像对未投影，T026 的所有物（Part 2a 的 E3 行已按「镜像类」整类归因）"
baseline: "E2 `slot=baseline` 行（状态脊 `<!-- test-budget:begin -->` 的 `seq:1`：25F / 7151P / 4S；比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名，另 2 条镜像为在途）。本行 14 条失败里 12 条在该 23 名集内（`test_c22_watch_target_hook_selftest`、`test_e_a_stale_pin…`、`test_g9_total_equals_frozen_baseline`、9 条 `unit/test_loop_state_engine.py`），1 条属 T026 的镜像类，1 条是上面归因给 T012 的新增读数 ⇒ **本段引入的新失败 0 条**"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part2b-targeted-run-2026-11-05.txt
```

## Why `ran`

本段改的是可执行面与载体：两个引擎的内联取值被删除并改经共享读取入口、两件批 2 声明落盘、一个载体加指针、
084 自己的契约模块收窄一条腿。落 `not-run-docs-only` 就是假绿，故实跑定向集并按 E2 做名字级比较。

## T013 收口读数（逐条，命令 + 实测）

| 判项 | 命令 | 读数 |
|---|---|---|
| 081 冻结面零 diff | `git diff --stat HEAD -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | **空输出**、exit 0（`HEAD = 16dcbdf2`） |
| 081 验收可收集且零新增失败 | `python3 -m pytest tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py --collect-only -q`；`… -q` | 收集 **77**（40 + 37，与 `research.md` § R7 的读数逐字一致）；运行 **77 passed** |
| 引擎侧内联副本已删除（两处） | `grep -n "PATH_VALUES" scripts/python/*.py` | `validate-requirements.py` 只剩读取后的绑定与注释，`closure-acceptance-check.py` 只剩读取后的绑定；**无任何 `PATH_VALUES = ("final", "supporting")` 形态** |
| 成员集仍是两个 | `harness-triple-check.py --action lookup --unit-id skills/internal/create-requirements/SKILL.md` | `fact: success-criterion-path-values kind=closed-set`；声明 `statement` 两条，未增未减 |
| 载体指针（两件） | `grep` 声明路径 + `#/` | `shared/workflow/acceptance-hardening.md` 与 `templates/commands/requirements.md` 各一处指针 |
| 判据散文 byte-identical | `git diff HEAD -- shared/workflow/acceptance-hardening.md` | 只有**新增**的一段指针；§ Closure Verdict 的判定散文、拒绝模板、退出码语义零改动（`test_closure_acceptance_check.py` 100 passed 中已覆盖） |
| 标签集不迁 | `git diff HEAD -- scripts/python/validate-requirements.py` | docstring 的六项枚举未动（081 的 `test_c01_c02_docstring_enumerates_exactly_the_pinned_labels` 绿） |

## T014 收口读数

| 判项 | 命令 | 读数 |
|---|---|---|
| `expression-stage-operator-table` 引擎侧位置式解析 | `grep -n 'required = (' scripts/python/flow-class-check.py` | 只剩 `required = (STEP_COLUMN, GATE_ID_COLUMN, OPERATOR_COLUMN, FACE_COLUMN, LEVEL_COLUMN)`；五个列名只在声明里各出现一次 |
| 表头检查语义不变 | `python3 scripts/python/flow-class-check.py --action isomorphism` | `stages: 8`、`gates: 6`、`findings: []`、exit 0（与改动前同读数）；拒绝消息模板与 `GateOwnerError` → exit 2 的映射未动 |
| `expression-gate-faces` 引擎侧副本已删除 | `grep -n 'FACES_SECTION_KEYWORD = \|FACES_EXPECTED = ' scripts/python/flow-class-check.py`；`grep -rn '"六面"' scripts/python/*.py` | 前者只剩从声明派生的绑定；后者**零命中**（模块级重复赋值 `FACES_SECTION_KEYWORD = "六面"` / `FACES_EXPECTED = 6` 已删除——它与文件顶部的声明读取同值，留着就会把读取变成死代码） |
| 缺层不判 | 声明缺席时的降级 | `FACES_DECLARED_LABEL` / `OPERATOR_COLUMNS_LABEL` 进入 `main` 的拒绝清单：读不到即 exit 2 + `[[STR-014]]` 实例，绝不在空值上「判成绿」 |
| 载体指针 | `grep` 声明路径 + `#/` | `shared/workflow/expression-gates.md` 新增一段指针（两件声明各一处键路径） |
| **未完成**：`面数 = 6` 仍在本载体 | `grep -n "面数 = 6" shared/workflow/expression-gates.md` | 命中。`tests/contract/test_expression_gates_doc.py:239` 逐字断言该串，而它属 SC-006 的零 diff 侧 ⇒ 删字面量与零新增失败互斥。本段保留字面量、加指针并把两者的从属关系写进文档 |
| **未完成**：四条 `driver-*` 事实 | 见下节 | 未写声明、未改载体、未改引擎 |

## 四条 `driver-*` 事实为何未迁移（读数，不是印象）

| 事实 | 阻断它的已记录断言 | 读数 |
|---|---|---|
| `driver-stage-sequence` | `tests/contract/test_isomorphism_map.py::test_stage_set_equals_the_roster_owner` 用 `^STAGE_ARTIFACTS\s*=\s*\{` **静态解析** `loop-state.py` | 该文件在 SC-006 的 38 文件零失败集内；把 `STAGE_ARTIFACTS` 改成声明派生即得 `roster == []` → 该腿必红 |
| `driver-stage-artifacts` | 同上，另加 `tests/contract/test_loop_state_contract.py::test_stage_artifacts_match_reference_five_dimensions`（引擎表 ↔ `state-awareness.md` §Stage Artifact Map 五维逐项） | 载体面是 `references/state-awareness.md` 的镜像表，删表即该腿必红 |
| `driver-completion-sentinels` | `loop-state.py` 的 `sentinel_literal()` 体 + `tests/contract/test_sdd_loop_driver_skill.py::test_c5_stage_chain_and_sentinel_literals`（`"-DONE"` / `"PLAN-DONE"` 必须**内联**在 `dispatch-recipes.md`） | 载体复述被逐字钉住，改指针即该腿必红 |
| `driver-gate-roster` | 判据面：六个 `check` 名只是消息前缀，改名不改变任何判决 | 按 clarify A2 收窄后的 FR-006 (i)（「判决结果随取值改变」）该行不成立，与路径 A 移出的八行同类；`STAGES` 一面成立而 `check` 名一面不成立，行需重新裁决 |

三者共同点：要迁移就必须改动「既有测试」，而这些测试恰在 SC-006 的零 diff / 零新增失败侧；`C-051` 对同形情形的
处置是「该行停下、回规格，不取本地例外」。故本段**不写**这四条声明——写了而没有读取点，正是 FR-007 的
`[[STR-009]]` 假绿形态，且会让 `harness-triple-check --action verify` 报出四条不存在的读取点。

## 未勾选的任务行与理由

- **T013 未勾**：八条腿里七条实测成立（见上表），第八条「point `skills/internal/create-requirements/SKILL.md`」
  无法与既有门共存——069a 的日期化记录 `.specify/specs/069a-*/notes/pre-change-file-hashes.txt` 冻结该文件字节
  （其自有教条为「dated record and is not rewritten」），`test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes`
  读它，而该测试在零 diff 侧。本轮把上一轮该文件的指针改动**回退**（恢复冻结字节），并把 084 自己的契约模块里
  这条事实的 `carriers` 收窄到两个真正带指针的载体（收窄的注释逐字写明原因与上送形态）。该单元今天的读数是
  `in-scope / pending / third-layer-missing`——缺读取点被封闭原因集点名，不是静默通过。
- **T014 未勾**：六条事实里两条的引擎侧已删副本（上表），四条 `driver-*` 按上节停在规格裁决点。
- 勾选属 `/speckit.implement` 的任务行状态，两行都缺腿，故**不勾**；缺口与可选处置见回传 ANOMALY 行。

## Bases verified（implement Part 2b 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| plan-owned 零触碰 | `git diff --stat 16dcbdf2 -- {plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出 ⇒ 无 PLAN-EDIT |
| 依赖面未动 | `git diff --stat 4b65517c -- pyproject.toml` | 空输出 |
| 镜像不手改 | `git status --porcelain -- .specify/` | 本段未写任何 `.specify/` 镜像；(`.specify/` 下的 spec 证据与运行时记录不属镜像) |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/**` 与 `.specify/state/**` |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## 本段修掉的三处上一轮遗留（都是纠正，逐条披露）

| # | 症状（首次读到的红） | 根因一行 | 修法 | 为何是纠正而非裁定 |
|---|---|---|---|---|
| 1 | `test_stage_class_wiring.py` 的 7 条 `[requirements]` 腿全红：`the block must be followed by a section heading, got '### 成功标准取值指针'` | 上一轮把指针写成**新的三级标题**插在 077 的类别卡与 `## Glossary` 之间，既破坏了卡的边界形态，又让「剥卡恢复基线字节」这条腿拿到不在卡内的内容 | 把指针收进卡内，改成该卡最后一条 `- **…**` 子弹；同时恢复被顺手删掉的 `## Glossary` 后空行 | 同一读法在仓内两处先例已确立（081/081c 对 `tasks`、`checklist` 的处理都是「把新行放进它的语义归属处、并保住卡的边界」），改动局部、可逆、断言一句未改 |
| 2 | `test_run_checks.py::test_c27…` 与 `test_user_facing_comprehension_pointers.py::test_c14…`：`regen-command-copies.py --check` exit 1，四处 per-tool 副本 drift | 上一条的载体改动落在 `templates/commands/requirements.md`，而四处生成副本没有跟着重新生成 | `python3 scripts/python/regen-command-copies.py`（生成器自身，非手改） | 镜像/副本的教条是「生成而非手写」（FF-12 的反面），生成器是唯一合法写者 |
| 3 | `test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes`：`drifted: ['skills/internal/create-requirements/SKILL.md']` | 上一轮为 T013 的载体指针改了该文件，而 069a 的日期化记录冻结它 | 回退该文件到 `HEAD`；把 084 契约模块里这条事实的 `carriers` 收窄到两个真带指针的载体（注释写明原因与上送形态） | 回退**不是**裁定本身：两种读法（「069a 记录可重测」vs「记录不可改写」）未由本层选边，故该单元今天如实读作 `in-scope / pending / third-layer-missing`，并把选择权交回 |

第 3 条同时改写了 `success-criterion-path-values.yaml` 的 `note`：原文称该单元「gain the pointer without losing a literal」，
那是上一轮的预期而非实测——该文件在迁移前对 `final|supporting|Path` 零命中，且现在也没有指针。note 改为实测读数 +
冻结事实 + 「该单元的处置仍然开放」。

## implement（Part 2c，T014 前两条 driver facts，2026-11-05）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1 —— 12 个文件，三个来源：(a) 本段改动面直接命中（`skills/external/sdd-loop-driver/scripts/loop-state.py`、`skills/external/sdd-loop-driver/SKILL.md`、`shared/declarations/facts/driver-*.yaml`）；(b) 驱动与回环的契约面（`test_sdd_loop_driver_skill`、`test_loop_state_contract`、`test_isomorphism_map`、`test_non_regression_070`、`test_sdd_loop_driver_{gates,efficiency,wp_model,wp_coordination}`、`test_pre_analyze_check`）；(c) 084 自己的契约模块（`test_harness_triple_structure`，本段把两条 slug 追加进 `MIGRATED_SO_FAR`，逐条断言 C-047 步骤 2/3/4）。集合到不了的地方如实写明：镜像对测试（`test_mirror_parity_suite`）与初装夹具（`specify init` 面）不在本段范围，全量套件按预算不跑"
selected_paths:
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/unit/test_loop_state_engine.py
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_isomorphism_map.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_sdd_loop_driver_gates.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_wp_model.py
  - tests/contract/test_sdd_loop_driver_wp_coordination.py
  - tests/unit/test_pre_analyze_check.py
sufficiency: "12 个文件、462 收集 → 449 passed / 13 failed / 0 skipped（12.95 s，单次运行；命令、退出码、完整 stdout/stderr 与耗时同次落盘为 `test-evidence/implement-part2c-targeted-run-2026-11-05.txt`，本行读数自该记录派生而非重跑）。13 条红里 10 条在 E2 的 23 名基线集内（`test_c22_watch_target_hook_selftest` + 9 条 `unit/test_loop_state_engine.py`），1 条（`test_c7_mirrors_are_byte_identical`）是 Part 2b 已记录在途的镜像类，2 条为本段改动的镜像后果（见 `new_failures`）。**可判定的充分性缺口**：本集合不含镜像对测试与全量套件，故它证明的是「本段改动的四个面与其载体在其自身断言下正确」，不是「树上无回归」"
command: "python3 -m pytest tests/contract/test_sdd_loop_driver_skill.py tests/unit/test_loop_state_engine.py tests/contract/test_harness_triple_structure.py tests/contract/test_isomorphism_map.py tests/contract/test_loop_state_contract.py tests/contract/test_expression_compatibility.py tests/contract/test_non_regression_070.py tests/contract/test_sdd_loop_driver_gates.py tests/contract/test_sdd_loop_driver_efficiency.py tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_coordination.py tests/unit/test_pre_analyze_check.py -q"
rc: 1
passed: 449
failed: 13
skipped: 0
new_failures:
  - "tests/contract/test_sdd_loop_driver_skill.py::test_c18_mirror_pair_no_drift —— `mirror drift on SKILL.md`（首条即 SKILL.md，`scripts/loop-state.py` 同批）。**不是缺陷而是投影未执行**：本段改的两个文件都在 `MIRROR_FILES` 的镜像对内，而派发约束明写「不改 `.specify/` 镜像」，镜像投影归 T026（`sync-mirrors.py --write` 后 `--check`，并复跑一次确认可重复）。改镜像即越界，不改镜像即本腿必红——两者互斥，处置已由 T026 拥有，故按读数登记不就地修平"
  - "tests/contract/test_sdd_loop_driver_efficiency.py::test_di_05_delivery_and_mirror —— `DIFF .specify/skills/sdd-loop-driver/SKILL.md` + `DIFF .specify/skills/sdd-loop-driver/scripts/loop-state.py`，`exit 2 / DRIFT detected`。同一类、同一原因、同一所有者（T026）"
baseline: "E2 `slot=baseline` 行（`seq:1`：25F / 7151P / 4S；比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名）。本行 13 条失败：10 条在该 23 名集内、1 条为 Part 2b 已登记的镜像在途、2 条为本段的镜像类新增 ⇒ **除镜像类外，本段引入的新失败 0 条**"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part2c-targeted-run-2026-11-05.txt
```

## Why `ran`

本段改的是可执行面（`loop-state.py` 的两处读取点）与一个载体（`SKILL.md` 的 frontmatter 与 § References）。落
`not-run-docs-only` 就是假绿；`empty-selection-escalated` 更不成立——两处都直接落在 `test_roots` 内。

## 两条 fact 的逐条读数（命令 + 实测）

| 判项 | 命令 | 读数 |
|---|---|---|
| 声明落盘且过 schema | `declaration_reader.py --action get --fact driver-stage-sequence`；`… driver-completion-sentinels` | 两条均 exit 0；`kind: ordered-operator-table`（八项有序）/ `kind: mapping`（`pattern` / `transform` / 三个字段名）；`verify` 报 `declarations: 13`（11 + 2） |
| 引擎侧经共享读取入口 | `grep -n 'declaration_reader' skills/external/sdd-loop-driver/scripts/loop-state.py` | 5 处：模块定位、`import`、`return`，以及两处注释；`DECLARATIONS` 在模块加载时解析一次 |
| 阶段顺序由声明驱动 | 模块加载后 `list(STAGE_ARTIFACTS)` | `['requirements','clarify','plan','tasks','checklist','analyze','implement','review']`——与声明 `statement` 同序、与改动前同序（两张脸 2026-11-05 未漂移） |
| 表体仍是本文件的字面量 | `grep -n '^STAGE_ARTIFACTS = {' …/loop-state.py`；`test_isomorphism_map.py` | 命中 `207:STAGE_ARTIFACTS = {`；同表静态解析腿绿（112 passed 的三文件批里含该文件）——顺序改由声明拥有，行的内容仍在此处，`^STAGE_ARTIFACTS\s*=\s*\{` 的位置契约不受影响 |
| 哨兵由声明渲染 | 模块加载后 `sentinel_literal('plan')` | `PLAN-DONE`；`sentinel_literal(None)` / `('')` 仍为 `None` |
| C-044 行的 inline 形态已消失 | `grep -n 'return "%s-DONE"' …/loop-state.py`；`test_harness_triple_structure.py` 的 `inline` 正则 | 只剩 `762:    return "%s-DONE" % name.upper()`（兼容路径，见下条）；契约测试钉的 `^    return "%s-DONE" % str\(stage\)\.upper\(\)` 零命中 |
| 声明缺席时不中断且显式标注 | 把本段引擎复制到 `/tmp` 后 `--self-test`（该副本 `declaration_entry()` 走不到层） | `loop-state: declaration layer unreachable: driver-stage-sequence` / `… driver-completion-sentinels` 各一行 stderr；`SELF-TEST: 31 passed, 5 failed` **与 HEAD 同读数**；`sentinel_literal('plan')` = `PLAN-DONE`。**行为不变、标注非空、无 traceback**（FR-012 / FR-013 的机械三项） |
| 载体指针（两件） | `grep -n 'driver-…yaml#/' SKILL.md` | frontmatter `description` 与 § References 各一处，四处键路径；单元处置 `pending → complete`（`third-layer-missing` 消失） |
| 双向一致 | `harness-triple-check.py --action verify` | `consistency-declarations-to-carriers: 15/15`、`consistency-carriers-to-declarations: 10/10` |

## 本段的两处判断（逐条披露；都是纠正而非裁定）

| # | 判断 | 为何是纠正而非裁定 |
|---|---|---|
| 1 | **哨兵保留一条被标注的兼容渲染**（`return "%s-DONE" % name.upper()`，仅在声明读不到时可达） | FR-012 原文「声明缺席 ⇒ **允许沿用内联值**，但 MUST 显式标注」；同一句在派发简报里对另一条 fact 写作「保持既有降级语义」——对阶段顺序，该语义只能是「照本文件既有的顺序继续」，故两面对称读法唯一。反路径（读不到即 `None`）会让未重装层的项目静默失去完成判定，那是行为变化而非降级。替代读法未被采纳的理由记此：`None` 亦不违反 FR-012，但它与本简报「行为不变」的强约束冲突 |
| 2 | **阶段表的行留在字面量里，只有顺序取自声明** | 派发简报写「用声明顺序校验/驱动 `STAGE_ARTIFACTS` 的键序（行为不变）」；`test_isomorphism_map.py` 用 `^STAGE_ARTIFACTS\s*=\s*\{` 静态解析该表，把整表改成声明派生会使该腿拿到空集（Part 2b 已留读数）。故「键序由声明、行由引擎」是唯一同时满足两条约束的读法，且 `driver-stage-artifacts`（行内容）本就不在本段范围 |

## 未完成与仍然开着的读数（不是本段的失败）

- **`T014` 仍未勾**：六条事实里本段只落两条；`driver-gate-roster` 与 `driver-stage-artifacts` 属 Part 2d，其载体
  （`references/dispatch-recipes.md`）与引擎侧（`pre-analyze-check.py` / `STAGE_ARTIFACTS` 行内容）本段未触。
- **`references/dispatch-recipes.md:154` 仍逐字重述两条取值**（阶段链与「大写阶段名 + `-DONE`」）；它不在本段
  `former_carriers` 范围内（`C-044` 该两行的载体面是 `SKILL.md`，`references/*.md` 也不是候选单元），留给 T014 的
  剩余部分。这不是静默：`test_c5_stage_chain_and_sentinel_literals` 与 `test_058_…` 正把该处字面量逐字钉住，
  故它与「零 diff 侧」互斥，属需要裁定的一步。
- **`verify` 仍报 `third-layer-missing: skills/internal/create-requirements/SKILL.md`**（T013 的第三条载体腿，Part 2b
  已记录为开放处置）。本段按简报勾了 T013 `[X]`，**这条读数是该勾选的反空真伴生量**：勾选表达「T013 的迁移已落地」，
  而该单元的挂起由 069a 冻结记录与 `in-scope/pending/third-layer-missing` 的封闭原因点名，不因勾选而消失。
- **两条镜像红腿**（见 `new_failures`）属 T026；本段按约束不触碰 `.specify/` 镜像。

## Bases verified（implement Part 2c 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| plan-owned 零触碰 | `git diff --stat HEAD -- .specify/specs/084-harness-triple-structure/{plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出 ⇒ 无 PLAN-EDIT |
| 依赖面未动 | `git diff --stat 4b65517c -- pyproject.toml` | 空输出 |
| 镜像不手改 | `git status --porcelain -- .specify/skills .specify/shared .specify/scripts` | 空输出（本段未写任何 `.specify/` 镜像；`.specify/` 下的 084 证据与任务行不属镜像） |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/**` 与 `.specify/state/**` |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## implement（Part 2d，T014 收口：`driver-gate-roster` + `driver-stage-artifacts`，2026-11-05）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "targeted-set-v1 —— 与 Part 2c 同一 12 个文件（可比性优先于重新挑选），另在派发简报点名的 5 个文件上单跑一次作为最小值。三个来源：(a) 本段改动面直接命中（`skills/external/sdd-loop-driver/scripts/{loop-state.py,pre-analyze-check.py}`、`skills/external/sdd-loop-driver/references/{efficiency-model.md,state-awareness.md}`、`shared/declarations/facts/driver-{gate-roster,stage-artifacts}.yaml`）；(b) 驱动与回环的契约面（`test_sdd_loop_driver_skill`、`test_loop_state_contract`、`test_isomorphism_map`、`test_non_regression_070`、`test_sdd_loop_driver_{gates,efficiency,wp_model,wp_coordination}`、`test_pre_analyze_check`）；(c) 084 自己的契约模块（`test_harness_triple_structure`，本段把 T014 余下四条 slug 一并追加进 `MIGRATED_SO_FAR`）。集合到不了的地方如实写明：镜像对测试（`test_mirror_parity_suite`、`test_di_05_delivery_and_mirror`）证据是红的且归 T026，初装夹具（`specify init` 面）不在本段范围，全量套件按预算不跑"
selected_paths:
  - tests/contract/test_sdd_loop_driver_skill.py
  - tests/unit/test_loop_state_engine.py
  - tests/contract/test_harness_triple_structure.py
  - tests/contract/test_isomorphism_map.py
  - tests/contract/test_loop_state_contract.py
  - tests/contract/test_expression_compatibility.py
  - tests/contract/test_non_regression_070.py
  - tests/contract/test_sdd_loop_driver_gates.py
  - tests/contract/test_sdd_loop_driver_efficiency.py
  - tests/contract/test_sdd_loop_driver_wp_model.py
  - tests/contract/test_sdd_loop_driver_wp_coordination.py
  - tests/unit/test_pre_analyze_check.py
sufficiency: "12 个文件、474 收集 → 461 passed / 13 failed / 0 skipped（13.43 s，单次运行；命令、退出码、完整 stdout/stderr 与耗时同次落盘为 `test-evidence/implement-part2d-targeted-set-2026-11-05.txt`，本行读数自该记录派生而非重跑）。13 条红与本段之前**同一批 13 个 id**：10 条在 E2 的 23 名基线集内、`test_c7_mirrors_are_byte_identical`（batch 1 遗留的镜像类）、`test_c18_mirror_pair_no_drift` 与 `test_di_05_delivery_and_mirror`（镜像类，Part 2c 已登记，本段新增的四个文件落在同一清单里）。相对 Part 2c 的 449 passed，461 − 449 = 12 是 `test_harness_triple_structure` 新增的 12 条断言腿（T014 六条 slug × 三条腿）。**可判定的充分性缺口**：集合不含镜像投影与全量套件，故它证明的是「本段改动的四个面与其载体在其自身断言下正确、且未把既有任何一条腿变红」，不是「树上无回归」。**收口复跑**（与上方同一 12 文件集，跑在本次提交的同一棵树上）：复现 rc=1 / 13 failed / 461 passed / 13 720 ms（`implement-part2d-closure-targeted-set-2026-11-05.txt`）；派发简报到点的最小集（4 文件）复现其引用的 11 failed / 167 passed（rc=1 / 7 558 ms，`implement-part2d-closure-brief-set-2026-11-05.txt`）。三组计数（11/167、12/182、13/461）的差异只是集合大小——178 例 / 194 例 / 474 例——不是判定差异，逐集对账见 `implement-part2d-closure-readings-2026-11-05.txt` §1–§2"
command: "python3 -m pytest tests/contract/test_sdd_loop_driver_skill.py tests/unit/test_loop_state_engine.py tests/contract/test_harness_triple_structure.py tests/contract/test_isomorphism_map.py tests/contract/test_loop_state_contract.py tests/contract/test_expression_compatibility.py tests/contract/test_non_regression_070.py tests/contract/test_sdd_loop_driver_gates.py tests/contract/test_sdd_loop_driver_efficiency.py tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_coordination.py tests/unit/test_pre_analyze_check.py -q"
rc: 1
passed: 461
failed: 13
skipped: 0
new_failures:
  - "**0 条**，程序判定而非目视。四份记录的 `FAILED <id>` 行逐条比对 E2 的 23 名比较集与已登记的镜像类 id（`test_c7` / `test_c18` / `test_di_05`）：本行 12 文件集 13 条 = 10 基线 + 3 镜像 + **0 新**；派发简报 4 文件集 11 条 = 10 + 1 + **0**；attempt 1 的 5 文件集 12 条与 12 文件集 13 条同分解。分类程序与四份记录的对账表：`implement-part2d-closure-readings-2026-11-05.txt` §2"
  - "**十名基线**（在 `baseline-pre-existing-failed.txt` 内，逐条名单见 readings §2）：9 条 `unit/test_loop_state_engine.py`（同一处 DEAD/ANOMALY-vs-RUNNING 分支，E2 冻结） + `test_c22_watch_target_hook_selftest`（本机 temp 根不可写：`mkdir: cannot create directory '/home/agent/tmp/spec-kit': Permission denied`，同为环境基线）。按约束不修"
  - "**三名镜像类**：`test_c18_mirror_pair_no_drift`、`test_c7_mirrors_are_byte_identical`、`test_di_05_delivery_and_mirror`。**不是缺陷而是投影未执行**：本段改的四个面（两条 references + 两个引擎）都在镜像对内，而派发约束明写「不改 `.specify/` 镜像」，投影归 T026（`sync-mirrors.py --write` 后 `--check`，并复跑确认可重复）。`test_di_05` 的 DIFF 清单由 Part 2c 的 2 个文件扩展为 5 个（本段四件 + Part 2c 的 `SKILL.md` 与 `loop-state.py`）：同族、同因、同所有者。改镜像即越界、不改即本腿必红——互斥，处置由 T026 拥有，按读数登记不就地修平"
baseline: "E2 `slot=baseline` 行（`seq:1`：25F / 7151P / 4S；比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名）。本行 13 条失败：10 条在该 23 名集内、3 条为镜像在途（`test_c7` / `test_c18` / `test_di_05`，皆在 Part 2b–2c 登记）⇒ **本段引入的新失败 0 条**（程序判定，见 `new_failures` 首条与 readings §2）"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-closure-targeted-set-2026-11-05.txt
```

## Why `ran`

本段改的是可执行面（`pre-analyze-check.py` 的 `GATE_ROSTER`／`STAGE_ARTIFACTS` 的**行内容**）与两个载体
（`references/efficiency-model.md` § 6.2、`references/state-awareness.md` § Stage Artifact Map）。落
`not-run-docs-only` 就是假绿；`empty-selection-escalated` 不成立——两处引擎都直接落在 `test_roots` 内。

## 两条 fact 的读数（命令 + 实测；全文 `implement-part2d-declaration-readings-2026-11-05.txt`）

| 判项 | 命令 / 探针 | 读数 |
|---|---|---|
| 声明落盘且过 schema | `harness-triple-check.py --action verify` | `declarations: 15`（13 + 2）；`consistency-declarations-to-carriers: 17/17`、`consistency-carriers-to-declarations: 10/10`；零 `third-layer-missing` / `duplicated-fact-literal` / `declaration-outside-subset`（76 条 finding 全为 `unclassified-candidate`） |
| 引擎侧经共享读取入口 | `grep -n "READ_ENTRY_REL\|GATE_ROSTER_FACT" …/pre-analyze-check.py`；`…STAGE_ARTIFACTS_FACT…/loop-state.py` | 各两处常量 + 模块加载时的一次 `declared_mapping(...)`；无第二条读取路径（readings §4） |
| roster 由声明渲染 | 加载模块后 `GATE_ROSTER`、`declared_check(...)` | 六名 `dangling-id … duplicate-id`；`stages` 三阶段；未登记键走**标注降级**（`driver-gate-roster: check name 'ghost-check' is not in the declared roster`）而非静默 |
| 行的内容由声明、顺序由 `driver-stage-sequence` | 加载模块后 `STAGE_ARTIFACTS` / `IMPLEMENT_CODE_PATHSPEC` / `STAGE_SEQUENCE` | 八行同序；`plan` 行拿到 `owned_paths: ['research.md']`（引擎字面量不携带该条件项）；两个布尔已 coercion 成 `True/False`；pathspec 六项取自声明 |
| 声明不可用时不中断、显式标注 | 九阶段声明／半行／不可读三种探针（readings §5） | 三次均「拒绝 + 一行 stderr 标注 + 字面量表照旧」；无 traceback、无静默、无行为变化 |
| 闸门输出不变 | 同一 spec-dir 上 HEAD 副本与新引擎对照（readings §6） | requirements / plan / tasks 三阶段 `rc`、stdout、stderr 均相同；findings 用声明渲染的名字 |
| 载体指针（两件） | `grep -n 'driver-…yaml#/' …/references/{efficiency-model,state-awareness}.md` | 各一处；单元处置 `in-scope/complete`，`third-layer-missing` 零（Part 2c 那条已在 `f64cde10` 清掉、仍未复活） |

## 本段的两处披露（都是纠正，已落在 `note` 与测试元组里）

1. **载体面纠正（C-050，两条 fact 各一处）**：C-044 的载体列写「same carrier」（`SKILL.md`），2026-11-05 实测两张
   表分别住在 `references/efficiency-model.md` § 6.2 与 `references/state-awareness.md` § Stage Artifact Map，
   而 `SKILL.md` § References 只索引小节、从不重述表——故声明取实测载体面并把纠正写进 `note`，测试的 `MIGRATED`
   行同步改名。附带的第二处：`efficiency-model.md` § 6.2 只列五个检查名（缺 `external-clause`，而引擎会出该
   advisory），按 authority order（code > authored）六名成立、载体面记为被纠正方；它的判据文本保留（那是闸门的
   文档，重置判据不属本批）。
2. **测试面的自我纠正（披露，不静默）**：`tests/contract/test_harness_triple_structure.py` 的 `MIGRATED_SO_FAR`
   是决定 C-047 三条腿跑哪些声明的元组；其自身注释写「each later task appends its slugs as it closes them」。
   T014 的六条里，两条 expression slug 早已迁移但从未进过该元组——即两条已迁移的行没有任何腿在跑。本段把余下四
   条一并追加，追加前逐条机械复验三条腿（声明齐全／引擎侧有读取入口且 inline 已消失／载体有 `<path>#/` 指针），
   读数 `62 → 68 passed`。读作纠正而非裁定：一个读法（元组自己的指令）、局部、可逆、未证伪任何下游前提。

## 开着的判定 —— `references/dispatch-recipes.md:154`（T014 因此**未**勾选）

- **事实**：该行逐字重述 T014 六条 fact 里的两条——`driver-stage-sequence` 的八阶段有序链、`driver-completion-sentinels`
  的「大写阶段名 + `-DONE`」。两条声明的 `former_carriers` 都不含该文件（`driver-stage-sequence` 只含 `SKILL.md`）。
- **为什么本段不能就地消掉**：`tests/contract/test_sdd_loop_driver_skill.py:185` 读的正是该文件，断言
  `STAGE_CHAIN in text`（"stage chain literal must be inlined"）。改成指针会让一条冻结测试转红，而
  `contracts/migration-batches.contract.md` C-051 明写：需要改冻结闸门判据或退出码的行「stops and returns to the
  spec — it does not get a local exception」。
- **为什么 `verify` 的绿不能替代该判断**：它的 `duplicated-fact-literal` 读数按 `migration-batches.contract.md`
  第 151 行交给 `doc-consistency-check.py --faces duplicate`，作用域是 spec 的正式文件，读不到整仓载体（readings §3 末段）。
- **两种读法（本段不裁定）**：
  - (a) 该行属 one-source-of-truth 允许的三类重复之一（被测试钉住的字面量），声明即权威、文本是操作配方 ⇒ T014 可勾，
    readings §5 作披露；
  - (b) 该行是那两条 fact 未迁移的载体面（C-047 步骤 4/5 未满足）⇒ T014 不能勾，行回规格（C-051）。
- **现状**：`tasks.md` 的 T014 保持 `[ ]`（attempt 1 曾把它改成 `[X]`，收口时按本节回退并在回传披露），本行
  `status` 仍为 `ran`——本段确实跑了、读数确实在，差距由本节拥有，不计入「本段失败」。Part 2c 的同一条读数已把它
  登记为「需要裁定的一步」，至今无人裁定。

## Bases verified（implement Part 2d 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| plan-owned 零触碰 | `git diff --stat HEAD -- .specify/specs/084-harness-triple-structure/{plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出 ⇒ 无 PLAN-EDIT |
| 依赖面未动 | `git diff --stat 4b65517c -- pyproject.toml` | 空输出 |
| 镜像不手改 | `git status --porcelain -- .specify/skills .specify/shared .specify/scripts` | 空输出（本段未写任何 `.specify/` 镜像；`.specify/` 下的 084 证据与任务行不属镜像） |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/**` 与 `.specify/state/**` |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## implement（Part 3，T015–T019，2026-11-05，用户测试豁免）

```yaml
stage: implement
row_type: stage-status
status: waived-by-user
selection_basis: user-test-waiver
changed_paths:
  - scripts/python/closure-acceptance-check.py
  - scripts/python/memory-utils.py
  - scripts/python/record-retention.py
  - scripts/python/history-utils.py
  - scripts/python/probe-utils.py
  - scripts/python/exec-quant.py
  - scripts/python/trigger-utils.py
  - shared/declarations/facts/arc-verdict-mapping.yaml
  - shared/declarations/facts/memory-types.yaml
  - shared/declarations/facts/memory-retention-thresholds.yaml
  - shared/declarations/facts/history-manifest-schema.yaml
  - shared/declarations/facts/probe-class-values.yaml
  - shared/declarations/facts/probe-object-binding-map.yaml
  - shared/declarations/facts/quant-record-schema.yaml
  - shared/declarations/facts/trigger-state-schema.yaml
  - shared/declarations/exclusions/no-machine-fact.yaml
baseline: E2 seq=1
passed: 0
failed: 0
new_failures: waived-by-user
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/t018-coverage-run1-2026-11-05.txt
```

**Why `waived-by-user`**：用户于 2026-11-05 明确指示「后续步骤跳过所有测试」。T017 的三条 US2 读数、T018 的确定性对比、T019 的 scratch-tree 证明均属测试型读数，未在指示后执行；T018 在指示前已产出的两次 coverage 捕获保留为历史证据，但不作为任何 SC 的 `pass`。本段交付的是事实/引擎/carrier/排除记录的代码面；测试与测试型读数整体记 `waived-by-user`，绝不记 `pass`。

## implement（Part 5，T020–T031，2026-11-05，用户测试豁免）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "user-test-waiver (2026-11-05) —— 不跑 pytest／全量／定向／smoke／scratch-tree 证明；只执行派发简报明确允许的**秒级确定性**命令：`sync-mirrors.py`（写 + `--check`，两次）、`harness-triple-check.py` 的 `coverage`／`verify`、`validate-tasks.py`、`pre-analyze-check.py`（带与不带 `--triple-structure`）、`git diff`／`git status`／`grep`／`ls|wc`。测试型读数（T021–T023、T027(e)／T028(e)、T029 的两条 collect 计数与 `comm -13`、T030、T031）一律未执行"
changed_paths:
  - shared/declarations/exclusions/no-harness-asset.yaml            # NEW — T020，2 行
  - shared/declarations/exclusions/no-machine-fact.yaml             # T020，追加 2 行（8 → 10）
  - skills/external/sdd-loop-driver/scripts/pre-analyze-check.py    # T024 — `--triple-structure` + docstring 订正
  - docs/concepts/harness-triple-structure.md                       # NEW — T025
  - CHANGELOG.md                                                    # T025 — 084 条目
  - ".specify/shared/**（36 文件同步 + declarations 子树 + owner 文档）, .specify/scripts/python/**（10 改 + 2 新）, .specify/skills/**（11 改）, .specify/templates/review-template.md, 8 个 per-tool 命令副本（.claude/.github/.opencode/.qoder × history|review）—— 全部由 T026 的 `sync-mirrors.py --write` 生成，无一手改"
  - .specify/specs/084-harness-triple-structure/{tasks.md, verification.md, test-evidence/implement-part5-readings-2026-11-05.txt, test-evidence/t026-mirror-projection-run{1,2}-2026-11-05.txt}
passed: 0
failed: 0
new_failures: waived-by-user
baseline: "E2 `slot=baseline`（seq 1：25F／7151P／4S；比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名）。本段未跑任何测试，`new_failures` 因此是 `waived-by-user`，不是 0"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/implement-part5-readings-2026-11-05.txt
```

**Why `ran` and not `not-run-docs-only`**：本段改的是可执行面（门宿主新增一个参数与一次委托）、声明层数据（两条排除文件）与文档面，并且所有被点名的秒级读数都真实执行、逐字落盘。落 `not-run-docs-only` 会把「没有测试」误写成「没有执行」。

## 本段五条读数（命令 + 实测；全文 `implement-part5-readings-2026-11-05.txt`）

| 判项 | 命令 | 读数 |
|---|---|---|
| T020 落盘且可判 | `harness-triple-check.py --action coverage --repo .` | `candidates: 83`；in-scope 13 ／ excluded **12** ／ unclassified 58；`exclusion-anchor-unresolvable` **0**；单元重名 0（引擎对重名是 exit 2 输入错误，本次 exit 1） |
| SC-001(i) 确定性 | 同一棵树连跑两次 coverage，`cmp` + `sha256sum` | 两次逐字节一致（`70f6dbf5…b483`），44 ms ／ 42 ms，`stdout_bytes 10685` |
| SC-002 声明侧／状态侧 | `--action verify --repo .` | `declarations: 23`；`consistency-declarations-to-carriers: 28/28`；`consistency-carriers-to-declarations: 16/16`；`third-layer-missing` 0 ／ `duplicated-fact-literal` 0 ／ `declaration-outside-subset` 0；`pending: 0` |
| T024 默认关闭 | `pre-analyze-check.py --stage tasks --repo .` | exit 0；finding 名集合 `['missing-path']`（3 条 advisory、0 error）——`triple-structure` 名不出现 |
| T024 开启一次委托 | 同命令 + `--triple-structure` | exit 1；**58** 条逐字转发的 `triple-structure` finding（`unclassified-candidate: …` 原文），宿主自身那 3 条逐条不变；`git status` 前后无差异（C-039 零写） |
| T026 镜像投影 | `sync-mirrors.py --write` → `--check` → 再 `--write` | 首次写：36 个 `shared/` 文件 + scripts/skills 镜像同步；`--check` exit 0，六对全 `ok`（templates 22／skills-external 409／skills-internal 138／agents 3／scripts 121／shared 89）；二次写只打印 `Regenerated command copies for 4 tools`，工作树零变化 |
| T027(c) 内联常量 | `grep -rn "<九个常量名>" --include=*.py scripts/ skills/` | 命中的全是 `*_FACT`／`*_LABEL` 绑定与 `declared_sequence()` 赋值，无第二份字面量表；第九行第二副本 `grep -n '"final", "supporting"' scripts/python/closure-acceptance-check.py` → exit 1（无内联元组） |
| T029 秒级腿 | `git diff 4b65517c -- pyproject.toml`；`git diff --stat 4b65517c -- tests/contract/test_{requirements_checker,checker_form}.py` | 两条均空输出 |

## 本段的四处披露（都是纠正或如实上报，不是就地修平）

1. **per-tool 命令副本由本段再生，plan 的镜像表该行已过时（订正，非裁定）**：`plan.md` § Mirror Obligations 写「no command template is edited by this feature」，但 Part 3 的 `98288d45` 实际改了 `templates/commands/review.md`（§ 2.4 ARC 指针）与 `templates/commands/history.md`（manifest 指针）；两者的 per-tool 副本因此陈旧。同一行末尾已写下处置：「if a later slice edits a command template it MUST regenerate the per-tool copies」。T026 的 `sync-mirrors.py --write` 正是该处置，生成的 8 个副本改动就是那 4 行指针 —— 按既有条文执行，未改 plan、无 PLAN-EDIT。
2. **`shared/definitions/*.md` 计数由 12 变 13（移动的计数如实上报）**：新增的是 owner 文档 `harness-triple-definitions.md`。该目录**不在**候选屏幕的三面内（`C-030` 排除 `shared/definitions/*.md`），候选面仍 27 + 53 + 19 = **99**，与 T001(c) 基线逐项相同。
3. **T029 的「特性状态取值数」没有基线（不可测，而非「未变」）**：T001(c) 只冻结了四个候选面计数，该腿的基线从未采集；T029 整体在豁免下未执行，此处只作如实记录，不构造一个事后基线。
4. **门宿主的转发名不进 roster（判断，已在代码注释里写明理由）**：`triple-structure` 是本地常量，不经 `declared_check()`。理由是 `driver-gate-roster#/statement/checks` 是这个门**自己**的六名封闭集（`C-044`），委托来的 finding 是另一台引擎的判决转发，不是第七个判断；若经 `declared_check()`，每次带 flag 运行都会打印「不在声明名册里」的降级标注，那条 `FR-012` 标注就失去意义。与该文件既有的四个 `GW-07` 名字同一形态。

## Bases verified（implement Part 5 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| plan-owned 零触碰 | `git diff --stat HEAD -- .specify/specs/084-harness-triple-structure/{plan.md,data-model.md,contracts,quickstart.md,research.md,feature-ref.md}` | 空输出 ⇒ 无 PLAN-EDIT |
| 依赖面未动 | `git diff 4b65517c -- pyproject.toml` | 空输出 |
| 081 验收面未动 | `git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | 空输出 |
| 镜像不手改 | 唯一写入 `.specify/` 镜像的命令是 T026 的 `sync-mirrors.py --write`；`grep`／`edit` 未落任何 `.specify/{shared,scripts,skills,templates}/` 文件 | 见 §T026 行 |
| 运行时记录未纳入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/session/**`、`.specify/memory/exec-quant/**`、`.specify/memory/feedback/**`、`.specify/state/**` |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## implement（Part 6，T032，2026-11-05，用户测试豁免）

```yaml
stage: implement
row_type: stage-status
status: ran
selection_basis: "user-test-waiver (2026-11-05) —— 未跑任何 pytest／全量／定向／smoke 腿；只执行派发简报允许的秒级确定性读数：`harness-triple-check.py --action coverage`（两次，含 `--format json`）、`--action verify`、`validate-tasks.py`、`git`／`grep`／`ls`。测试型读数一律未执行，不记 pass"
changed_paths:
  - shared/declarations/exclusions/no-harness-asset.yaml            # 2 → 32 行（追加 30，T032）
  - shared/declarations/exclusions/no-machine-fact.yaml             # 10 → 38 行（追加 28，T032）
  - .specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md   # PLAN-EDIT：§ Facts outside the roster 追加一段判决句
  - .specify/specs/084-harness-triple-structure/tasks.md            # 新增 T032（32 ≤ 40）+ Traceability 一行
  - .specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt   # NEW — 五条读数的全量捕获
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
passed: 0
failed: 0
new_failures: waived-by-user
baseline: "E2 `slot=baseline`（seq 1：25F／7151P／4S；比较集 = `test-evidence/baseline-pre-existing-failed.txt` 的 23 名）。本段未跑任何测试，`new_failures` 因此是 `waived-by-user`，不是 0"
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt
```

**PLAN-EDIT 声明（本段唯一触碰 plan-owned 产物）**：`PLAN-EDIT: .specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md — § Facts outside the roster 追加「候选屏幕的其余单元由 exclusions/ 的逐行记录处置；覆盖动作的零未分类即判决」一段（不抄 58 行清单）；分类=substantive(user-authorized)`。授权来自派发简报：本次 § Facts outside the roster 的扩展是用户授权的 substantive reopen（`plan_constraint=active since 2026-11-05T08:22:55Z`，`plan_commit=4b65517c`）。其余 plan-owned 产物（`plan.md`、`data-model.md`、`research.md`、`quickstart.md`、`feature-ref.md`、其余四份契约）零触碰。

## 本段三条读数（命令 + 实测；全文 `t032-classification-readings-2026-11-05.txt`）

| 判项 | 命令 | 读数 |
|---|---|---|
| T032 归零（SC-001(ii)） | `harness-triple-check.py --action coverage` | `candidates: 83`／`unclassified: **0**`／`pending: 0`／`findings: 0`，exit 0；处置分布 in-scope 13 ／ excluded 70（`no-harness-asset` **32** + `no-machine-fact` **38**）——70 = 12（T020 起的既有行）+ 58（本段） |
| SC-001(i) 确定性 | 同树连跑两次 `coverage`，`sha256sum` 比对 | 两次逐字节一致（`f9cd934a…3473`），47 ms／44 ms，`stdout_bytes 7845` |
| SC-004 锚点可判 | `--action verify` | `declarations: 23`；`consistency-declarations-to-carriers: 28/28`；`consistency-carriers-to-declarations: 16/16`；`findings: 0` ⇒ `exclusion-anchor-unresolvable` **0**、单元重名 0（重名与重复 unit 都是 exit 2 输入错误，本次 exit 0） |

58 个单元的处置分布（按面）：`shared/workflow/*.md` 3（全 `no-harness-asset`）；`skills/external/*/SKILL.md` 9（`no-harness-asset` 2 ／ `no-machine-fact` 7）；`skills/internal/*/SKILL.md` 27（`no-harness-asset` 15 ／ `no-machine-fact` 12）；`templates/commands/*.md` 19（`no-harness-asset` 10 ／ `no-machine-fact` 9）。每行三键齐备，`anchor` 一律 `path#Section` 且段落文本在该文件内逐字出现（`verify` 逐行解析的读数，不是人工比对）。

## 本段的四处披露

1. **D1 的读法（本切片自裁的假设，须评审复核）**：D1 判的是**单元的验收交付物（产品）**，不是「运行顺带写下的记录」。依据是已落地的 `no-harness-asset` 行本身——`draw-diagram` 行明写该单元仍会经 `feedback-utils.py` 写下自己的 feedback 记录，理由却仍是「交付物是图包」。若改取「附带记录」读法，D1 对每个候选恒真（每个技能的 § Wrap-up 都写 session／feedback／exec-quant），判据自我作废、只余 D2 单条件——这正是 A2 clarify 裁定否掉的那条读法。
2. **两条理由没有按面平均分配，也没有被凑成同一个理由**：`no-harness-asset` 落在「产品是 spec 产物／账本／注册表／导出包／文档」的单元，`no-machine-fact` 落在「产品确实改动了消费者清单点名的六棵树，或产出记录与 verdict」的单元。以 `templates/commands/todo.md`（产出工作面 TODO 标记）与 `templates/commands/tools.md`（产出 `tools/` 记录）为例，两者相邻而处置不同。
3. **`carrier` 的两种来源都写进行注释**：43 行取 `grep` 到的 `scripts/python/<name>.py`；15 行取 `skills/<layer>/<name>/scripts/<file>` 形态的引擎——其中 10 行是该单元自己声明的 `${SKILL_HOME}/scripts/<file>` 资产（以相对路径调用），5 行是它文本里点名的兄弟技能引擎（`create-team/scripts/dispatch.sh`、`create-team/scripts/match-team-preset.py`、`archive-session/scripts/export.py`、`code-review/scripts/git-delta-review.sh`），行注释写明该形态；8 行 `no-harness-asset` 单元无自有主体引擎，carrier 取它自己的 § Wrap-up 所调记录引擎（`feedback-utils.py`，全表 17 行用它），逐条注明。
4. **`.specify/` 镜像本段未重投（按派发简报执行）**：两份 exclusions 在 `.specify/shared/declarations/exclusions/` 有镜像副本，本段只改框架源。派发简报明令「不改 `.specify/` 镜像」，故 `sync-mirrors.py --check` 在下次获授权的同步前会把这一对判为 drift；这是授权的范围边界，不是未记录的偏差，`diff -r shared/declarations .specify/shared/declarations` 在本段结束后会显示两份 exclusions 文件不同（其余相同）。

## Bases verified（implement Part 6 收口）

| 判项 | 命令 | 结果 |
|---|---|---|
| plan-owned 仅声明的那一处 | `git status --porcelain .specify/specs/084-harness-triple-structure` | 只有 `contracts/migration-batches.contract.md`（已按 PLAN-EDIT 声明）；`plan.md`／`data-model.md`／`research.md`／`quickstart.md`／`feature-ref.md` 与其余四份契约无改动 |
| 依赖面未动 | `git diff 4b65517c -- pyproject.toml` | 空输出 |
| 运行时不入提交 | `git status --porcelain` 逐条比对 | 提交集不含 `.specify/memory/**`、`.specify/state/**` |
| 既有脏文件未动 | `git status --short` 前后一致 | `M .specify/memory/session/20261102T231648Z-…-081a.md` 与既有未跟踪记录保持原样，未提交未还原 |
| 不 push | `git log --oneline -1` | 本地提交，未执行任何 push |

## review（四段 + Acceptance Reality Check，2026-11-05）

```yaml
stage: review
row_type: stage-status
status: not-run-docs-only
selection_basis: "review 面无 pytest 槽位：本阶段只落两份评审记录与秒级确定性读数（closure checker、harness-triple-check coverage ×2、sync-mirrors --check、三处 git diff）；按派发简报的测试预算，全量 closure 槽位在 review 之后由驱动执行，本阶段不消费也不预支它"
changed_paths:
  - .specify/specs/084-harness-triple-structure/review.md
  - .specify/specs/084-harness-triple-structure/code-review.md
  - .specify/specs/084-harness-triple-structure/test-evidence/review-smoke-2026-11-05.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/memory/register.md
evidence_ptr: .specify/specs/084-harness-triple-structure/review.md
```

## review 的六条读数（命令 + 实测）

| 判项 | 命令 | 读数 |
|---|---|---|
| ARC（判定条件的主人） | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` | `verdict: block`（exit 1）；`claimed_status: Implemented`；`final_path` = pass 2／blocked 0／deferred 0／partial 0／fail 0／unknown 0／total 2；`completion_conditions.smoke_record_pass: false`；`reasons[0].code: status-claims-implemented-but-blocked` |
| smoke 三件（复跑，定向） | `python3 scripts/python/harness-triple-check.py --action coverage` ×2 + `cmp` + `sha256sum` | 两次 exit 0、逐字节一致、`sha256 f9cd934a…3473`；`candidates 83 / pending 0 / unclassified 0 / findings 0`；证据 `test-evidence/review-smoke-2026-11-05.txt` |
| 镜像 | `python3 scripts/python/sync-mirrors.py --check` | exit 0，六对全 `ok`（templates 22／skills-external 409／skills-internal 138／agents 3／scripts 121／shared 89） |
| 非目标 | `git diff --stat 4b65517c -- pyproject.toml`；`git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | 两条均空输出 |
| 代码段回执 | `git-delta-review.sh receipt --review-file …/code-review.md --spec …` | `changed 276 / judged 39 / skipped 237 / gap 0`；`renderer: text`；`segment: blocked`（2 条 `[blocking]`）；`report --summary` exit 1 = 门禁拒绝 |
| 排除记录面 | `grep -c "^- unit:" shared/declarations/exclusions/*.yaml` | `no-harness-asset` 32 + `no-machine-fact` 38 = **70** 行（与 `verification.md` SC-002 的 70 一致；SC-004 的 12 是 T032 之前的陈旧读数，见 `review.md` F10） |

## review 的三处披露

1. **Feature 状态未翻转，这是结论而不是省略**：ARC 的 verdict 是 `block`（条件④ smoke 记录的机器可读形态不成立），且当前 `code-review.md` 含 2 条 `blocking`。两条路径各自独立拒绝 `Implemented → Ready for Review`，故 `features.md` 与 `features/084.md` 保持 `Implemented`，本阶段不写回任何状态值，也不降级（refusal 不是 downgrade）。
2. **P0 的验证路径较弱且已披露**：本拓扑无子代理派发能力，三条 P0 按 `review-sdd-process` § 5 的 subagent-unavailable 回退走「直接重读」，每条在报告里带 `(validated: direct re-read, subagent unavailable)`。
3. **代码段回执的跳过不是遗漏**：`judged 39 / skipped 237` 是按类声明的（`.specify/*` 与四个工具命令副本 = `generated`（已由 `sync-mirrors --check` 证明逐字节同源）；`tests/*`、四个未逐行读完的引擎、以及 `*.md` = 各自法定理由）。首轮 `receipt` 默认把 276 件全记 `reviewed`，那是工具默认值而非本轮的读数，故按实际读过的面重写一次；改写动作本身记在此处，不隐藏。

## review round 2（四段 + Acceptance Reality Check，2026-11-06）

```yaml
stage: review
row_type: stage-status
attempt: 2
status: not-run-docs-only
selection_basis: "review 面无 pytest 槽位：本阶段只落两份评审记录（`review.md` 重写 + `review-r1.md` 归档、`code-review.md` 轮转后重写）、秒级确定性读数（closure checker、harness-triple-check coverage ×2 + cmp、sync-mirrors --check、三处 git diff）与一次定向集复核；按派发简报的测试预算，closure 全量槽位在 review 之后由驱动执行，本阶段不消费也不预支它"
changed_paths:
  - .specify/specs/084-harness-triple-structure/review.md
  - .specify/specs/084-harness-triple-structure/review-r1.md
  - .specify/specs/084-harness-triple-structure/code-review.md
  - .specify/specs/084-harness-triple-structure/code-review-20261105T160943Z.md
  - .specify/specs/084-harness-triple-structure/test-evidence/review-round2-smoke-2026-11-06.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
  - .specify/memory/features/084.md
  - .specify/memory/register.md
evidence_ptr: .specify/specs/084-harness-triple-structure/review.md
```

## review round 2 的七条读数（命令 + 实测）

| 判项 | 命令 | 读数 |
|---|---|---|
| ARC（判定条件的主人） | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` | `verdict: accept`（exit 0）；`claimed_status: Implemented`；`final_path` = pass 2／blocked 0／deferred 0／partial 0／fail 0／unknown 0／total 2；四条 `completion_conditions` 全 true；`reasons: []`；`smoke.evidence_exists: true` / `exit_code: "0"` / `records: 1`；`tasks` = closed 32／deferred 0／open 0 |
| smoke 三件（复跑，定向） | `python3 scripts/python/harness-triple-check.py --action coverage` ×2 + `cmp` + `sha256sum` | 两次 exit 0、逐字节一致、`sha256 f9cd934a…3473`（与 round 1 同值）；`candidates 83 / pending 0 / unclassified 0 / findings 0`；证据 `test-evidence/review-round2-smoke-2026-11-06.txt`（两次完整 stdout） |
| verify（双向一致） | `python3 scripts/python/harness-triple-check.py --action verify` | exit 0；`declarations 23`；`consistency-declarations-to-carriers: 30/30`（round 1 为 28/28，因修复提交给 `flow-class-classes` 补了两个 consumers）；`consistency-carriers-to-declarations: 16/16`；`findings: 0` |
| 镜像 | `python3 scripts/python/sync-mirrors.py --check` | exit 0，六对全 `ok`（templates 22／skills-external 409／skills-internal 138／agents 3／scripts 121／shared 89） |
| 非目标 | `git diff --stat 4b65517c -- pyproject.toml`；`git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | 两条均空输出 |
| 代码段回执 | `git-delta-review.sh receipt --review-file …/code-review.md --spec …` | `changed 284 / judged 5 / skipped 279 / gap 0`；`renderer: text`；`segment: blocked`（1 条 `[blocking]`）；`report --summary --file` exit 1、`blocking_entries=1`、`gate=deny` |
| 修复提交的定向集（复核，不重跑全量） | 读 `test-evidence/review-fix-targeted-tests-2026-11-05.txt` 尾部 | `2 failed, 219 passed`，两条失败均在 23-name implement-start 基线集内（`test_e_a_stale_pin…` 陈旧 pin；`test_c22_watch_target_hook_selftest` 为 `cannot create temp dir` 权限），无新增失败 |

## review round 2 的三处披露

1. **Feature 状态仍未翻转，且拒绝依据与 round 1 不同**：本轮 ARC 是 `accept`，拒绝来自状态机条件 (c)——当前 `code-review.md` 含 1 条 `blocking`（`closure-acceptance-check.py:227` 的 `flow-class-classes` 内联副本）；`features.md` 与 `features/084.md` 的状态列保持 `Implemented`，未写回、未降级，拒绝字面量 `blocking-unresolved` 记在 `review.md` § 2.1 与 § Status Transition。两个门读的是不同工件，故分开报告而不是折算成一句。
2. **本轮判读面是修复提交，不是整个 delta**：`0bd4c622..e0453f9e` 只触碰 15 条路径，回执的 5 条 `reviewed` 就是其去重后的源码面；其余 279 条按 `size-guard-focus-not-reviewed` 跳过（相对 round 1 逐字节未变），跳过不计覆盖信用。round 1 的 39 条 judged 读数在其归档 `code-review-20261105T160943Z.md` 内，本行不对它们给新结论。
3. **两处由修复轮自身引入的状态已如实记为本轮 P1**：`verification.md` SC-001 记录的 `28/28` 被修复提交自己的 `consumers` 修改推到 `30/30`（同一行 limb (iii) 的「引用它的一方确实被点名」被 `closure-acceptance-check.py` 证伪）；round 1 的第二个法定载体——`features/084.md` 的 `## Latest Review` 评审条目——当时没有写，本轮补写（本轮结论落在报告 § 2.1 与本条目两处）。这两条都不是「顺手修平」：SC-001 那一行归 implement，本阶段只记录读数与归属。
