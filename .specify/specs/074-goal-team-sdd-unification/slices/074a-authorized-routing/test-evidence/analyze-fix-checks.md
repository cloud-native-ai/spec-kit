# Analyze-fix deterministic checks — slice 074a-authorized-routing

**Stage**: analyze remediation round 1 of 1（修复 3 HIGH + 8 MEDIUM；`decomposition=single-package`，无子代理派发）
**Slice**: `.specify/specs/074a-authorized-routing/`
**Stage base**: `b8363f89f`（074a checklist 完成提交）
**Recorded**: 2026-10-29
**Host**: python3（本机 PATH），git

本文件只贴各确定性检查的**真实输出**；结论不复述到其他产物。修复决策与本轮 PLAN-EDIT 声明见
`plan.md` § Plan Revision 与回传信息，不在此重复。

## 0. 本轮改动面（只改切片产物 + Feature 登记）

| 文件 | 性质 | 对应 finding |
|------|------|--------------|
| `requirements.md` | 需求条文（FR-005/006/007/008/010/012、SC-001、A4、A9、Edge Cases 一处） | HIGH-1、HIGH-2、C-03、B-01、B-02、B-03、B-04 |
| `contracts/routing-decision.md` | 契约 C-18、C-20、C-21、C-22、C-24、C-25、C-26、C-28 | HIGH-1、HIGH-3、C-03、B-03 |
| `contracts/hierarchy-and-authorization.md` | 契约 C-8、C-9、C-13、C-14 | HIGH-3、HIGH-2、B-01、B-04 |
| `data-model.md` | E4（inputs / override）、E7（cap、SDD 指派定义指针） | HIGH-1、HIGH-2、B-03、B-04 |
| `quickstart.md` | S4 退出码字母表；S1/S3 的 `--nature` 字面量与封闭域对齐 | HIGH-3、HIGH-1 |
| `tasks.md` | T007（退出码断言）、T017 / T023 / T024 同步、T029 审计职责、Requirement Coverage Map 两处、FR-020 waiver、DoD-2 计数 | HIGH-1、HIGH-2、B-02、B-04、E-01、F-02 |
| `plan.md` | § Scale/Scope 与 § Structure Decision 交付面计数、新增 `## Plan Revision` | F-02、HIGH-3（plan 重审记录） |
| `feature-ref.md` | § 3 FR-008 行措辞（closure + default） | HIGH-1 |
| `checklists/requirements.md` | 计数刷新（511 行）＋ § Analyze-fix Round 记录 | 计数纪律 |
| `.specify/memory/features.md` / `features/074.md` | 补记 2026-10-29 checklist 阶段 | G-01 |

零删除面；父 spec（`.specify/specs/074-goal-team-sdd-unification/**`）与 `074b` 零改动；`templates/commands/**` 零改动。

## 1. 需求条目检查

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/074a-authorized-routing/requirements.md
file: .specify/specs/074a-authorized-routing/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 511 lines, 26 definition rows, 10 shared strings
0 error(s), 0 warning(s)
rc=0
```

计数结论：FR 20 / SC 6 / STR 10 未变（本轮零新增条目，零重编号）。

## 2. 跨产物一致性（三个 stage）

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074a-authorized-routing --stage <requirements|plan|tasks> --repo .
requirements: decision=pass  rc=0  findings=67  severity={advisory:67}  kinds={missing-path:67}
plan:         decision=pass  rc=0  findings=67  severity={advisory:67}  kinds={missing-path:67}
tasks:        decision=pass  rc=0  findings=67  severity={advisory:67}  kinds={missing-path:67}
```

- 改前基线同为 `pass` / 66 advisory。本轮为 67：唯一新增 advisory 是 `plan.md:329` 对
  `tests/contract/test_sdd_authorization.py` 的引用（`## Plan Revision` 新行），该文件属本切片将创建面，
  与其余 66 条同性质（「本切片将创建的文件此刻尚不存在」）。其余差异全部为行号位移。
- 新增的 definition-class 路径根（`.specify/memory/constitution.md`、`.specify/instructions.md`、
  `.specify/agents/{templates,instances}/`、`agents/`、`.specify/skills/`、`skills/`、`.specify/teams/`、
  `templates/`）逐个实测存在，未产生任何 missing-path。

## 3. 任务结构与分解规模

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md
PASS: .specify/specs/074a-authorized-routing/tasks.md — 0 error(s), 0 warning(s)
rc=0

$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074a-authorized-routing/requirements.md \
    --tasks .specify/specs/074a-authorized-routing/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 20, "task_count": 32,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T02:42:36Z"}
rc=0
```

32 行 ≤ 40，任务行数未变（本轮无新增任务行）。

## 4. 契约条款与覆盖

```text
$ python3 .specify/scripts/python/clause_extract.py .specify/specs/074a-authorized-routing/contracts/*.md
bootstrap-and-maintenance.md	form=md-bold-closed	clauses=4
hierarchy-and-authorization.md	form=md-bold-closed	clauses=16
nested-invocation.md	form=md-bold-closed	clauses=13
routing-decision.md	form=md-bold-closed	clauses=14
合计 clause id = 47

$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing
claimed clauses (this feature): 47
FR universe: 20 / FR claimed: 20 / FR uncovered: 0
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s)
status: ok
rc=0
```

条款总数与编号区间未变（C-1…C-47，四个文件 16/14/13/4），因此 `tasks.md` 的 47 条 `[green:]`
认领仍一一成立、`validate-tasks.py` 的 green 四项检查零告警。

## 5. 定向回归（targeted-set-v1，stage_base=plan）

```text
$ python3 -m pytest -q tests/contract/test_agent_dispatch_mechanism.py \
  tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py \
  tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py \
  tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py \
  tests/contract/test_shipped_agent_presets.py
........................................................................ [ 37%]
........................................................................ [ 75%]
...............................................                          [100%]
191 passed in 22.62s
rc=0
```

与本切片 plan 阶段记录的 `191 passed` 名字级一致；本轮只改 Markdown 产物，未触碰任何被测源文件。

## 6. 镜像与命令副本（零漂移）

```text
$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
rc=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

六对逐对 `ok`、命令副本 `OK`，与 plan 阶段实测基线（22/405/136/3/113/58）逐项相同：本轮没有新增
镜像面（未编辑任何 `shared/`、`skills/`、`scripts/`、`templates/` 源文件）。

## 7. 删除面与越界面审计

```text
$ git status --porcelain | grep -c '^ D'          → 0
$ git diff --name-only -- .specify/specs/074-goal-team-sdd-unification \
    .specify/specs/074b-nested-governance templates/commands | wc -l   → 0
```

零删除、父 spec 与兄弟切片零改动、`templates/commands/**` 零改动。
