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
