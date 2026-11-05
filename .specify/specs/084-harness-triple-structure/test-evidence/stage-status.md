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

