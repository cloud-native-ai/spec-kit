<!-- merged from 074a-authorized-routing (source: .specify/specs/074a-authorized-routing/test-evidence/analyze-fix-checks.md) -->

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
| `contracts/routing-decision.md` | 契约 C-002、C-004、C-005、C-006、C-008、C-009、C-010、C-012 | HIGH-1、HIGH-3、C-03、B-03 |
| `contracts/hierarchy-and-authorization.md` | 契约 C-008、C-009、C-013、C-014 | HIGH-3、HIGH-2、B-01、B-04 |
| `data-model.md` | E4（inputs / override）、E7（cap、SDD 指派定义指针） | HIGH-1、HIGH-2、B-03、B-04 |
| `quickstart.md` | S4 退出码字母表；S1/S3 的 `--nature` 字面量与封闭域对齐 | HIGH-3、HIGH-1 |
| `tasks.md` | T007（退出码断言）、T017 / T023 / T024 同步、T029 审计职责、Requirement Coverage Map 两处、FR-025 waiver、DoD-2 计数 | HIGH-1、HIGH-2、B-02、B-04、E-01、F-02 |
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

条款总数与编号区间未变（C-001…C-004，四个文件 16/14/13/4），因此 `tasks.md` 的 47 条 `[green:]`
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

<!-- merged from 074b-nested-governance (source: .specify/specs/074b-nested-governance/test-evidence/analyze-fix-checks.md) -->

# Analyze-fix deterministic checks — slice 074b-nested-governance

**Stage**: analyze remediation round 1 of 1（修复 2 HIGH + 7 MEDIUM + 部分 LOW；`decomposition=single-package`，无子代理派发）
**Slice**: `.specify/specs/074b-nested-governance/`
**Stage base**: `7d9308519`（074b checklist 完成提交）
**Recorded**: 2026-10-29
**Host**: python3（本机 PATH），git

本文件只贴各确定性检查的**真实输出**；结论不复述到其他产物。修复决策与本轮 PLAN-EDIT 声明见
`plan.md` § Plan Revision 与回传信息，不在此重复。

## 0. 本轮改动面（只改切片产物 + Feature 登记）

| 文件 | 性质 | 对应 finding |
|------|------|--------------|
| `checklists/readiness-2026-10-29.md` | CHK006 一处：`074a` 的裸 id `FR-017` → `074a`'s local FR 017（含跨切片限定语） | F-02（HIGH） |
| `contracts/compat-and-safety.md` | C-006 与 C-007 之间新增 C-003 / C-006 共享集合 `S2` 的判据消歧段；C-011 标注散文级锚点 | F-01（HIGH）、E-03 |
| `contracts/report-and-attribution.md` | C-059 基数统一（at most one / exactly one / none）；FR-020「summary」绑定既有 goal summary 通道；C-063 增补集成身份与不完整交接规则 | A-02、A-01、E-01 |
| `contracts/diffusion.md` | `Measures` 由 `—` 改为 DoD-2 / DoD-4 / DoD-6 + T042/T048/T051/T056 指针；C-001 双向约束 + 席位 operating object 判定；C-008 标注设计级判据 | E-02、E-04、E-03 |
| `data-model.md` | E2 写者 / 何时写两行与 V-5 基数改写（至多一条；有 Target 恰一条；无 Target 零条） | A-02 |
| `plan.md` | 新增 `## Plan Revision`（F-01 决策 + 同轮文本级对齐清单） | F-01、PLAN-EDIT 记录 |
| `.specify/memory/features.md` / `features/074.md` | 补记 074b tasks（`61496b869`）与 checklist（`7d9308519`）两阶段；Last Updated 同步 | G-01 |

零删除面。未重跑 requirements / plan / tasks 生成命令；父 spec（`.specify/specs/074-goal-team-sdd-unification/**`）
与 074a（`.specify/specs/074a-authorized-routing/**`）零改动；`templates/commands/**` 零改动。

## 1. 需求条目检查 — `validate-requirements.py`

```text
$ python3 scripts/python/validate-requirements.py .specify/specs/074b-nested-governance/requirements.md
file: .specify/specs/074b-nested-governance/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 308 lines, 10 definition rows, 7 shared strings
0 error(s), 0 warning(s)
exit=0
```

## 2. 跨产物门 — `pre-analyze-check.py`（修复前 / 修复后）

**修复前**（同一命令，抓取 HIGH-2 的现象）：

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage requirements
pre-analyze-check: stage=requirements decision=fail errors=1 advisories=0 waived=0
{"check": "dangling-id", "severity": "error", "path": "checklists/readiness-2026-10-29.md",
 "line": 22, "message": "references FR-017 which is not defined"}
```

`--stage plan` 与 `--stage tasks` 同一条 finding，三种 stage 一致（`errors=1`）。

**修复后**（三档 stage，带 `--repo .` 的严格读法）：

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage requirements --repo .
pre-analyze-check: stage=requirements decision=pass errors=0 advisories=21 waived=0

$ ... --stage plan --repo .
pre-analyze-check: stage=plan decision=pass errors=0 advisories=21 waived=0

$ ... --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=21 waived=0
{"summary": {"errors": 0, "advisories": 21, "waived": 0, "fr": 8, "sc": 2, "tasks": 26, "files": 12}}
exit=0
```

21 条 advisory 全是 `missing-path`，逐条指向本切片 implement 阶段才创建的三个契约测试文件
（`tests/contract/test_nested_run_report.py` / `test_sdd_diffusion.py` / `test_sdd_compat_containment.py`），
与 tasks 阶段记录的 21 条同集；未 waive 一条。不带 `--repo` 的读法 `advisories=0`，两种读法本轮都跑过，
不择一冒充。

## 3. 任务条目检查 — `validate-tasks.py`

```text
$ python3 scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md
PASS: .specify/specs/074b-nested-governance/tasks.md — 0 error(s), 0 warning(s)
exit=0
```

## 4. 拆解门 — `decomposition-check.py --mode tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074b-nested-governance/requirements.md \
    --tasks .specify/specs/074b-nested-governance/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 8, "task_count": 26,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T05:17:32Z"}
exit=0
```

## 5. 条款抽取 — `clause_extract.py`

```text
$ python3 scripts/python/clause_extract.py .specify/specs/074b-nested-governance/contracts/*.md
compat-and-safety.md      form=md-bold-closed  clauses=12
diffusion.md              form=md-bold-closed  clauses=8
report-and-attribution.md form=md-bold-closed  clauses=10
$ ... | grep -cE '^\s+C-[0-9]+$'
30
```

30 条款不变、三文件形态不变（本轮新增的两段消歧读法为斜体散文段，不产生新 id，也不改变 form 判定）。

## 6. 条款/需求覆盖记账 — `account-clause-coverage.py`

```text
$ python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance
claimed clauses (this feature): 30
uncovered beyond baseline: 0
FR universe: 8
FR claimed: 8
FR uncovered: 0
companion: claimed clauses 30, scanned files 215, clause universe 1315, FR universe 8
  [clause-uncovered]  pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered]      pass (0)   — 8 of 8 FRs cited from citation groups
  [clause-unparsable] warn (94)  — 94 files yield no clause id under the owner's forms
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s)
status: ok
exit=0
```

## 7. 定向集 v1（`stage_base=analyze`）—— 一次运行

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/.tmp/074b-analyze-fix-failed.txt <the 19 suites
  recorded in test-evidence/targeted-set-v1-baseline.txt>
collected 290 items
1 failed, 289 passed in 33.14s
# failed-name list written: .specify/.tmp/074b-analyze-fix-failed.txt (1 entries)
exit_status=1
```

同一命令在本轮跑了两次（第一次在条款修复落盘后、第二次在最后一处措辞回修后），两次结果同形：
`1 failed, 289 passed`（32.11s / 33.14s），失败名单同为 1 条，未因第二次运行而改变——本条以第二次运行为准，
第一次运行不丢弃而是并列记录。

唯一红行是**既有**红：`tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`
（`gate total moved from the frozen 23 to 27`，四个 gate 早于本切片）。名字级与 plan / tasks 两阶段抓取一致，
未修、未掩、未据此做任何绿声明。289 passed / 1 failed 与基线同形，本轮无需第二次全量。

## 8. 镜像与命令副本（零漂移）

```text
$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
exit=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.   exit=0
```

## 9. 语料形态抽检（contract 文本改动后的一次定向补充读法）

改动只碰本切片三份 contract 的散文，但语料级检查会读全部 `.specify/specs/*/contracts/*`，故补跑三支：

```text
$ python3 -m pytest -q tests/contract/test_clause_forms.py tests/contract/test_clause_coverage.py \
    tests/contract/test_green_point_claim.py
1 failed, 110 passed in 18.91s
FAILED tests/contract/test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file
  AssertionError: Left contains 2 more items:
    .specify/specs/060-decompose-subagent-dispatch/contracts/delegation-parity.md
    (and …/skill-enhancements.md)
```

逐文件复核（同一模块直读）：

```text
$ python3 -c "... for p in .specify/specs/*/contracts/*.md: print(p, ce.md_forms_hit(p))"
.specify/specs/060-decompose-subagent-dispatch/contracts/delegation-parity.md   ['md-bold-closed', 'md-heading']
.specify/specs/060-decompose-subagent-dispatch/contracts/skill-enhancements.md ['md-bold-closed', 'md-heading']
```

两条都属 **060**、均为本切片未触碰的既有文件（`git status` 对本切片之外的 spec 为空），本切片三份
contract 的 `form_of` 全部仍为 `md-bold-closed`。故这是**既有红**、在定向集 19 文件之外，本轮记录不修、
不掩，也不据此做任何绿声明。

## 10. 删除面与提交面审计


```text
$ git status --short | grep -E '^ ?D'
<empty>                      # 零删除面
```

本轮只 stage 切片产物（`checklists/` / `contracts/` / `data-model.md` / `plan.md` / 本文件）与
`.specify/memory/features.md`、`.specify/memory/features/074.md`；不 stage 状态脊（`.specify/state/**`）、
运行记录（`.specify/memory/session/**`、`exec-quant/**`、`feedback/**`）、父 spec 与 074a。
既有的脏文件（8 个 `session/*run-determination*`）未提交、未还原。
