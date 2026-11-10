# Tasks-stage deterministic checks — Feature 074

Recorded 2026-10-28 during `/speckit.tasks` for
`.specify/specs/074-goal-team-sdd-unification`. Every line below is a command that was actually run
in this repository at `stage_base=6297c14f6`, followed by its real output. Nothing here is a
pre-written expectation.

Test budget for this stage: **targeted-set-v1** (stage_base `6297c14f6`); the tasks stage edits no
source and no test, so the targeted set has no new subject — it is run as the recorded baseline the
implementation stage compares against.

## 1. Structural validation of the generated tasks.md

```bash
python3 .specify/scripts/python/validate-tasks.py .specify/specs/074-goal-team-sdd-unification/tasks.md
```

```text
PASS: .specify/specs/074-goal-team-sdd-unification/tasks.md — 0 error(s), 0 warning(s)
rc=0
```

One warning was raised by the first draft and repaired before this record:
`green-cross-phase` on `contracts/report-and-attribution.md` — T028 claimed `#C-53` while T029 (the
next row) claimed `#C-50`, so the clause order ran backwards against row order. The partition was
re-cut (T028 → C-47/C-48/C-49; T029 → C-50…C-54) rather than the warning being silenced.

## 2. Clause partition and task population

```bash
grep -oE '\[green: [^]]+\]' tasks.md      # 68 matches
grep -oE '\[green: <contract>#[^]]+\]' …  # the Format section's own tag definition is the 68th
grep -cE '^- \[ \] T[0-9]{3}' tasks.md
```

```text
task rows: 57   (US1 9, US2 7, US3 5, US4 9, US5 6, non-story 21)
[P] rows: 11
[green:] claims: 67  — C-1…C-67, each exactly once, one claim per clause
```

Clause partition by contract file (claims in ascending clause order within each file, which is what
the validator's `green-cross-phase` check measures):

| Contract file | Clauses | Claiming rows |
|---|---|---|
| `route-decision.md` | C-1…C-14 | T017–T021 |
| `authorization-and-probe.md` | C-15…C-30 | T008–T011, T023–T026, T047 |
| `nested-invocation.md` | C-31…C-46 | T013, T014, T030–T035 |
| `report-and-attribution.md` | C-47…C-54 | T028, T029 |
| `diffusion-and-compat.md` | C-55…C-67 | T037–T041, T046–T051 |

## 3. Clause and FR coverage accounting (green)

```bash
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification --freeze > .specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification
```

```text
freeze rc=0 ; coverage-baseline.txt = 497 lines (2 header + 495 names), base-sha 6297c14f68fd
claimed clauses (this feature): 67
baseline: .specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 28 / FR claimed: 28 / FR uncovered: 0
  [clause-uncovered] pass (495) — 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 28 of 28 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files declare no positive clause form (parse doubt, never read as covered)
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
status: ok ; rc=0
```

The clause lane was `status: baseline-missing` at the plan stage by design; it freezes here, once
the `[green:]` claims exist, which is the timing plan.md § Phase 1 named. Freezing before the
claims existed would have made this lane trivially green.

## 4. Targeted-set-v1 baseline at `stage_base=6297c14f6`

```bash
python3 -m pytest -q tests/contract/test_agent_dispatch_mechanism.py \
  tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py \
  tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py \
  tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py \
  tests/contract/test_instructions_section_propagation.py tests/contract/test_flow_class_ledger.py \
  tests/contract/test_flow_class_correctness.py tests/contract/test_shipped_agent_presets.py
```

```text
191 passed in 21.61s
rc=0
```

`stage-status` line (six fields):

```text
status=run ; command="python3 -m pytest -q <13 files>" ; selection_basis="suites that pin every surface this feature edits (anti-nesting, dispatch governance, neutral metadata schema + tool mapping, driver skill, team command routing, goal definition, instructions section propagation, flow-class ledger)" ; selected_paths=13 files as listed above ; sufficiency="each edited source surface has a pinning suite; the set is also the pre-change case set for FR-026/FR-027/SC-005" ; rc=0 ; passed-failed="191 passed / 0 failed" ; new_failures=[] ; baseline=191 passed at 6297c14f6 (test-evidence/targeted-set-v1-baseline.txt)
```

## 5. Plan-owned artifact touch (declared, minor)

```bash
grep -n 'new test files\|test files are new' .specify/specs/074-goal-team-sdd-unification/plan.md
```

Two prose counts said "7 new test files" / "seven test files are new" while every enumerated source
in the plan-owned set says six: `plan.md` § Source Code lists six `NEW` test files,
`feature-ref.md` § 2 rows 13–18 list six, `research.md` R14 says "six new contract/unit test files",
and each contract's "Pinned by" line resolves to that same six. Both phrases were corrected to
`6` / `six` — a line-level consistency repair, no change to scope, architecture, data-model,
contract semantics, FR/SC content, or task breakdown.

<!-- merged from 074a-authorized-routing (source: .specify/specs/074a-authorized-routing/test-evidence/tasks-stage-checks.md) -->

# Tasks-stage deterministic checks — slice 074a-authorized-routing

**Stage**: tasks（`/speckit.tasks`，`decomposition=single-package`，无子代理派发）
**Slice**: `.specify/specs/074a-authorized-routing/`
**Stage base**: `907d21fbe`（074a plan 完成提交）
**Recorded**: 2026-10-29T02:17Z
**Host**: python3（本机 PATH），pytest 8.4.2，git

本文件只贴各确定性检查的**真实输出**与偏离裁定；结论不复述到其他产物。

## 1. 入口前提（command `scripts:` 块）与就地撰写理由

```text
$ bash scripts/bash/check-prerequisites.sh --json
{"REQUIREMENTS_DIR":"/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification","REQUIREMENT_ID":"074","FEATURE_ID":"074","FEATURE_NAME":"Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）","AVAILABLE_DOCS":["research.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md"],"MODE":"C","WRITABLE":true}
rc=0
```

- **实测**：前提脚本按分支前缀解析到**父** spec 目录（`.specify/specs/074-goal-team-sdd-unification`），不是切片目录——分支名为 `074-goal-team-sdd-unification`，前缀匹配命中父目录。故 `REQUIREMENTS_DIR` 由派发简报覆盖为 `.specify/specs/074a-authorized-routing/`；未切换分支、未触碰父 `tasks.md`。
- **派发简报的前提偏差（实测优先于简报）**：简报称可能失败的脚手架脚本是 `create-new-tasks.sh`。实测该脚本在仓库内**不存在**：`find . -name "create-new-tasks*" -not -path "./.git/*"` → 0 命中；`scripts/bash/` 与 `.specify/scripts/bash/` 内只有 `create-new-requirements.sh` / `create-new-plan.sh` / `create-new-skill.sh` / `create-new-tools.sh`。因此切片 `tasks.md` 按 `templates/commands/tasks.md` → `create-tasks` 技能 → `templates/tasks-template.md` **就地撰写**，失败原因类别是「该脚手架不存在」，不是「前缀碰撞」；前缀碰撞的实际受害者是上一条 Prerequisites 解析。

## 2. 生成时实测的分母（Measured Premises 的复算）

```text
$ grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/074a-authorized-routing/requirements.md   → 20
$ grep -cE '^\- \*\*SC-[0-9]+\*\*:' .specify/specs/074a-authorized-routing/requirements.md   → 6
$ grep -cE '^\| `STR-[0-9]+`' .specify/specs/074a-authorized-routing/requirements.md          → 10
$ for f in …/contracts/*.md; do grep -cE '^\*\*C-[0-9]+\*\*' "$f"; done
  bootstrap-and-maintenance.md 4 / hierarchy-and-authorization.md 16 / nested-invocation.md 13 / routing-decision.md 14
$ grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md | wc -l                                       → 47
$ grep -cE '^- \[[ xX>~]\] T[0-9]{3}' .specify/specs/074a-authorized-routing/tasks.md           → 32
```

9 个新文件逐个 `test -e` → 9/9 ABSENT（3 个框架文件 + 5 个测试文件 + 1 个夹具），红先前提成立。
`grep -c 'sdd-invocation' src/specify_cli/__init__.py` → `0`（**陷阱形**：全仓 `grep -rn` 会命中本切片设计文档的说明文字，那是引用不是定义，故计量单位取代码 owner 文件）。

## 3. 结构校验（`validate-tasks.py`）

首稿（32 行、47 claims）报两条 `parallel-safe` WARN：

```text
WARN  194: parallel-safe: [P] tasks T026 (line 194) and T027 (line 195) both WRITE ['shared/definitions/sdd-routing-definitions.md'] in phase `## Phase 6: Polish & Cross-Cutting Concerns`
WARN  195: parallel-safe: [P] tasks T027 (line 195) and T028 (line 196) both WRITE ['notes/quickstart-run.md'] in phase `## Phase 6: Polish & Cross-Cutting Concerns`
PASS (with warnings): …tasks.md — 0 error(s), 2 warning(s)
```

按行内实际写目标逐条裁定：

| WARN | 实际写目标 | 裁定 |
|------|-----------|------|
| T026 × T027 争 `shared/definitions/sdd-routing-definitions.md` | T026 只 `cmp` 只读该源文件（写的是 `.specify/` 投影）；T027 只读它做反向计数（写的是 `notes/quickstart-run.md`） | 误报：两者都不写该源文件。但 `[P]` 保留会让机器判据持续报警，故与下一条同一处置：Polish 段整体去掉 `[P]`，按行序串行 |
| T027 × T028 争 `notes/quickstart-run.md` | 两行都向同一追加落点写入 | **真冲突**：去掉 T028 的 `[P]`（正是该 WARN 给出的补救），未删任何被点名的路径 |

定稿：

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md
PASS: .specify/specs/074a-authorized-routing/tasks.md — 0 error(s), 0 warning(s)
rc=0
$ grep -cE '^- \[[ xX>~]\] T[0-9]{3}' …/tasks.md   → 32
```

## 4. 分解规模（`decomposition-check.py --mode tasks`）

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074a-authorized-routing/requirements.md \
    --tasks .specify/specs/074a-authorized-routing/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 20, "task_count": 32, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T02:17:21Z"}
rc=0
```

32 ≤ 40、20 ≤ 30：本切片自身**不**触发再拆。父规格 57 行的 `split-required` 是拆分来源，切片化后已消解。

## 5. 条款覆盖（`account-clause-coverage.py`）

冻结前（首次全树核算，baseline 尚不存在——按设计为红，不冒充为绿）：

```text
claimed clauses (this feature): 47
baseline: .specify/specs/074a-authorized-routing/coverage-baseline.txt (0 names, MISSING)
ERROR frozen baseline not found … freeze it with --freeze
  [clause-uncovered] fail (495) — 495 uncovered, 495 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
496 error(s), 0 warning(s)
status: baseline-missing
```

claims 已存在，故按冻结时机冻结（`--freeze`，脚本只打印、不写文件）：

```text
$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing --freeze > …/coverage-baseline.txt
rc=0；497 行；头部：
# frozen-from: .specify/specs/*/contracts/* excluding 074a-authorized-routing | … | base-sha: 907d21fbe065 | files: 208 (parsed 114 + named 94)
```

冻结后复算：

```text
companion (must be non-empty on a green run): claimed clauses 47, scanned files 212, clause universe 1285, FR universe 20
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them declare a positive form
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s)
status: ok
```

基线正文不含本切片 47 条 `C-N` 名（`--freeze` 排除被核算 spec 本身）：本切片条款只能被任务行认领，不能被自己的基线豁免。

## 6. 跨产物一致（`pre-analyze-check.py --stage tasks`）

```text
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=65 waived=0
summary: {"errors": 0, "advisories": 65, "waived": 0, "fr": 20, "sc": 6, "tasks": 32, "clauses": 0, "files": 12}
```

65 条 advisory **全部**是 `missing-path`，逐类裁定（无一为 blocking，不加 `--strict`）：

| 类 | 条数（约） | 命名对象 | 裁定 |
|----|-----------|----------|------|
| 本切片**将创建**的框架文件与测试文件 | 55 | `shared/definitions/sdd-routing-definitions.md`、`scripts/python/sdd-route.py`、`skills/external/sdd-loop-driver/references/nested-invocation.md`、5 个 `tests/contract/test_sdd_*.py`、`tests/fixtures/nested_sdd.py` | 任务阶段尚未创建，属预期；T004/T005/T011/T013/T014/T017/T019/T020 各行的交付面 |
| 兄弟切片目录 | 1 | `.specify/specs/074b-nested-governance` | 尚未开始，本切片 MUST NOT 创建 |
| 本切片确认为 074b 承接的测试 | 1 | `tests/contract/test_nested_run_report.py` | `feature-ref.md` § 2 明示归 074b |
| 继承的 requirements 检查清单引用 | 1 | `feedback/20261028T160637Z-speckit-requirements.md` | 既有的未跟踪运行记录（脏文件），不提交不还原 |
| `.specify/` 投影 | 1 | `.specify/scripts/python/sdd-route.py` | 由 T026 的镜像机构生成，非手写 |

## 7. 镜像与命令副本基线（改前，未做任何源编辑）

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
rc=0
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
```

零漂移，故本切片每条镜像义务的判据是「相对该基线零**新增**差异」。

## 8. 任务分布与条款分区

```text
Setup 3（T001–T003；一对 [P]）· Foundational 2（T004–T005）· US1 11（T006–T016）
US2 5（T017–T021）· US3 4（T022–T025）· Polish 7（T026–T032）  合计 32
```

47 条款分区（每条恰一行认领一次；每文件内序号随行序单调）：

| 契约文件 | 分区 |
|----------|------|
| `hierarchy-and-authorization.md`（16） | C-1…C-2→T004、C-3→T008、C-4→T009、C-5→T010、C-6…C-8→T011、C-9…C-10→T023、C-11…C-14→T024、C-15…C-16→T025 |
| `routing-decision.md`（14） | C-17→T004、C-18…C-27→T017、C-28→T019、C-29→T020、C-30→T027 |
| `nested-invocation.md`（13） | C-31…C-33→T013、C-34…C-37→T014、C-38…C-40→T015、C-41…C-42→T016、C-43→T028 |
| `bootstrap-and-maintenance.md`（4） | C-44…C-46→T004、C-47→T028 |

## 9. Feature 表复审（tasks 阶段的强制项）

`pre-analyze` 与本阶段的分解结果均未暴露新增 / 合并 / 失效 Feature：切片继续复用 Feature 074 的注册行（`.specify/memory/features.md` 074 行），MUST NOT 新增注册行。已同步更新 `.specify/memory/features/074.md`（§ Latest Review 加 tasks 段、§ Implementation Notes 加「074a 切片 tasks 期裁定」、`Last Updated`）与 `.specify/memory/features.md` 074 行的 Last Updated 单元格；状态列保持 `Planned`（`Implemented` 属 `/speckit.implement`）。

## 10. 红线复核

- 父 spec 与父设计（`.specify/specs/074-goal-team-sdd-unification/**`，含父 `tasks.md`）零改动。
- 本阶段零 plan-owned 面改动 → 无 `PLAN-EDIT:`。
- 未派发子代理（`decomposition=single-package`）；未切换分支；未 push。
- 只提交本阶段产物（`tasks.md`、`coverage-baseline.txt`、本文件、特性登记两处）；运行记录与状态脊不入提交。

<!-- merged from 074b-nested-governance (source: .specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md) -->

# Tasks-stage deterministic checks — 074b-nested-governance

**Stage**: `/speckit.tasks` · **Slice**: `074b-nested-governance` · **Feature**: 074
**Stage base**: `ce9de5983` (plan DONE) · **Captured**: 2026-10-29
**Single-run evidence discipline**: every command below was executed once in this stage. Command
lines and their decisive output are pasted here; the one expensive run (the 19-suite targeted set)
keeps its **complete** stdout in the sanctioned ignored temp root —
`.specify/.tmp/074b-tasks-targeted.log`, with its failed-name list at
`.specify/.tmp/074b-tasks-failed.txt` — both retained rather than discarded, so no follow-up
question needs a re-run. The temp root is the one `.specify/.gitignore:30` already matches.

---

## 1. Structural validator — `validate-tasks.py`

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md
PASS: .specify/specs/074b-nested-governance/tasks.md — 0 error(s), 0 warning(s)
exit=0
```

Adjudicated WARN: none emitted. The four green-attribution checks (`green-dangling`,
`green-cross-phase`, `green-clause-collision`, `green-path-divergence`) all report clean, so the
30 clauses are each claimed exactly once, in ascending order per contract, with no test path
carrying two different green points.

## 2. Decomposition gate — `decomposition-check.py --mode tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074b-nested-governance/requirements.md \
    --tasks .specify/specs/074b-nested-governance/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 8, "task_count": 26,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T04:51:28Z"}
exit=0
```

Row count re-derived independently:
`grep -cE '^- \[[ xX>~]\] T[0-9]+' tasks.md` → **26** (ceiling 40; 14 rows of headroom).

## 3. Clause coverage — freeze, then account

### 3a. Freeze (after the 30 `[green:]` claims landed in `tasks.md`)

```text
$ python3 .specify/scripts/python/account-clause-coverage.py \
    --spec-dir .specify/specs/074b-nested-governance --freeze \
    > .specify/specs/074b-nested-governance/coverage-baseline.txt
exit=0
```

Baseline header (verbatim):

```text
# frozen-from: .specify/specs/*/contracts/* excluding 074b-nested-governance | owner-forms: md-bold-closed,md-bold-paren,md-heading,yaml-openapi,yaml-assertions,md-none (md-none named, never silently covered) | clause-rules: shared/definitions/contract-clause-definitions.md | per-form counts: notes/clause-form-census.md | base-sha: ce9de598356a | files: 212 (parsed 118 + named 94)
```

Self-exemption audit (the baseline must not hold this slice's own clause names):

```text
$ grep -c '^074b-nested-governance/' .specify/specs/074b-nested-governance/coverage-baseline.txt
0
$ grep -c '074b-nested-governance/contracts' .specify/specs/074b-nested-governance/coverage-baseline.txt
0
```

Baseline holds 495 pre-existing uncovered names from other specs (`wc -l` = 497 with two header
lines). This slice's 30 clauses can therefore only be covered by a task row, never by its own
frozen baseline.

### 3b. Account (post-freeze)

```text
$ python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance
claimed clauses (this feature): 30
baseline: .specify/specs/074b-nested-governance/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 8
FR claimed: 8
FR uncovered: 0
companion (must be non-empty on a green run): claimed clauses 30, scanned files 215, clause universe 1315, FR universe 8
status: ok
exit=0
```

Pre-freeze state, recorded for the delta (plan stage left it `baseline-missing`, as designed):
`claimed clauses (this feature): 0`; `baseline: …/coverage-baseline.txt (0 names, MISSING)`;
`FR claimed: 8 / uncovered: 0`; `status: baseline-missing`; exit 2.

Clause census re-derived from disk (not from the plan's prose):

```text
$ grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/074b-nested-governance/contracts/*.md
contracts/compat-and-safety.md:12
contracts/diffusion.md:8
contracts/report-and-attribution.md:10
$ grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md | wc -l
30     # ids contiguous C-1…C-30
```

## 4. Cross-artifact gate — `pre-analyze-check.py --stage tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=21 waived=0
exit=0
```

**Adjudication of all 21 advisories**: every one is `missing-path` and every one names one of the
three contract-test files this slice's *implementation* stage authors —
`tests/contract/test_nested_run_report.py` (7 hits: `plan.md:301`, `tasks.md:19`, `tasks.md:134`,
`quickstart.md:48`, `quickstart.md:110`, `research.md:251`, `feature-ref.md:44`,
`contracts/report-and-attribution.md:10`), `tests/contract/test_sdd_diffusion.py` (`tasks.md:19`,
`tasks.md:149`, `tasks.md:151`, `quickstart.md:120`, `research.md:252`, `feature-ref.md:45`,
`contracts/diffusion.md:10`) and `tests/contract/test_sdd_compat_containment.py` (`tasks.md:19`,
`tasks.md:171`, `tasks.md:210`, `research.md:253`, `feature-ref.md:46`,
`contracts/compat-and-safety.md:11`). Each is a *planned* path whose authoring row exists (T036,
T042, T051), so none is a phantom reference; the advisory is the expected shape at this stage and
will clear when those rows run. Zero waived — the count is adjudicated, not silenced.

Note on the JSON summary's `"clauses": 0`: pre-analyze counts clause *citations in the analysed
docs' citation groups*, not `[green:]` claims; the claim count is the accountant's number in § 3b
(30), and the two are different metrics, not a disagreement.

## 5. Test budget — targeted-set-v1 (`stage_base=tasks`), one run, no second full suite

**E3 stage-status row (six run fields)** —

| Field | Value |
|-------|-------|
| `command` | `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/074b-tasks-failed.txt <the 19 suites recorded in test-evidence/targeted-set-v1-baseline.txt>` |
| `exit_status` | `1` (one pre-existing failure; see below) |
| `counts` | `collected 290 items` → **1 failed, 289 passed** |
| `duration` | pytest `34.15s`; wall-clock `34,965 ms` |
| `failed_name_set` | `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` (1 entry) |
| `baseline_ptr` | `.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt` (`stage_base=33269994a`) |

Name-level comparison against the frozen baseline (identity, not counts):

```text
$ diff <(grep -E '^tests/[^ ]*::' test-evidence/targeted-set-v1-baseline.txt | sort) \
       <(sort .specify/.tmp/074b-tasks-failed.txt)
IDENTICAL name set
new failures (comm -13):        <empty>
disappeared (comm -23):         <empty>
```

The single red is the pre-existing `test_c11_gate_scan_total_unchanged` (gate total `27` vs the
frozen `23`, four gates predating this slice). It is recorded, not repaired, and no green claim is
made over it. This stage changed no executable surface (markdown and evidence files only), so the
identical result is the expected outcome; no second suite was run.

**Full-suite row**: `status=not-run-docs-only` — this stage added `tasks.md`, `coverage-baseline.txt`
and this evidence file, and touched no owner, engine, or test file. The full suite has no new
subject; its two slots belong to the implement and review stages.

## 6. Baseline surfaces re-measured at generation time (no drift)

```text
$ python3 scripts/python/sync-mirrors.py --check
exit=0 · ok templates/ 22 · skills/external/ 406 · skills/internal/ 136 · agents/ 3 · scripts/ 114 · shared/ 59

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.   exit=0

$ python3 .specify/scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
```

## 7. Premises measured before any row cites them

| Premise | Command | Measured |
|---------|---------|----------|
| FR / SC / STR in `requirements.md` | `grep -cE '^\- \*\*FR-[0-9]+\*\*:'` / `SC-` / `^\| \`STR-[0-9]+\`'` | 8 / 2 / 7 |
| Contract clauses | `grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` | 12 / 8 / 10 = **30** |
| Three new test files | `test -e` each | 3/3 absent (red-first precondition) |
| Edit targets + reused fixture + leaf preset | `test -e` each | 8/8 present |
| Leaf preset declaration count | `grep -c 'sdd-invocation' agents/sdd-executor.agent.md` | `0` (trap: a repo-wide grep hits design-doc prose; the unit is the shipped preset) |
| Report-contract owner site | `grep -n '### Report contract' skills/internal/create-team/SKILL.md` | `:53` (skeleton block `:57-63`) |
| `run-team` delegation | `grep -n 'target_ref' skills/internal/run-team/SKILL.md` | `:66` — keeps delegating, already carries `"target_ref": "T-<nnn>"` |
| Stage bullet site | `grep -n 'executor.*evaluator.*optimizer' …/conceptual-model.md` | `:10` |
| Authoring-baseline site | `grep -n '^## Authoring Baseline' skills/internal/run-agent/SKILL.md` | `:171` |
| Trigger discipline section set | `grep -c '^## ' shared/guidelines/proactive-trigger.md` | 10 `## ` sections; `## Promotion & Safety Boundary` at `:68` |
| Instructions pointer face | `grep -c 'sdd-routing\|sdd-invocation\|Nested SDD' templates/instructions-template.md` | `0` (new, not a rewrite) |
| Instructions byte sizes | `wc -c templates/instructions-template.md .specify/instructions.md` | 34,666 / 41,948 (both already over the 32,768 B budget → ceiling + measured delta is the criterion) |
| Ledger attribution field | `grep -n 'target_ref' …/summary-mapping.md` | `:100` (`target_ref`, `T-\d{3}`, absent = goal-wide form) |
| Containment carrier | `awk` per `## S<n>` over `^tests/` lines | 266 cases / 17 files / 7 sets (49/25/24/40/36/54/38) @ `33269994a` |
| Task rows | `grep -cE '^- \[[ xX>~]\] T[0-9]+' tasks.md` | 26 |

## 8. Clause → row partition (the claims this stage froze)

| Contract | Clauses | Rows |
|----------|---------|------|
| `contracts/report-and-attribution.md` | C-21…C-23 / C-24…C-26 / C-27…C-29 / C-30 | T037 / T038 / T039 / T040 |
| `contracts/diffusion.md` | C-13…C-14 / C-15…C-17 / C-18 / C-19 / C-20 | T043 / T044 / T045 / T046 / T047 |
| `contracts/compat-and-safety.md` | C-1…C-2 / C-3…C-6 / C-7…C-12 | T049 / T050 / T051 |

Each clause is claimed exactly once and each file's ordinals ascend with row order — the validator's
four green checks agree (§ 1), and the accountant's `claimed clauses = 30` (§ 3b) is the same fact
measured from the other side.

## 9. PLAN-EDIT declarations

None. This stage wrote `tasks.md`, `coverage-baseline.txt` and this evidence file only; no
plan-owned artifact (`plan.md`, `data-model.md`, `contracts/**`, `quickstart.md`, `research.md`,
`feature-ref.md`) was edited, so `plan_constraint` (active since 2026-10-29T04:47Z at
`plan_commit=ce9de5983`) was never engaged.

## 10. Deletion-surface audit

`git status --short` over this stage's write set shows three added paths and zero deletions:

```text
A  .specify/specs/074b-nested-governance/tasks.md
A  .specify/specs/074b-nested-governance/coverage-baseline.txt
A  .specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md
```

No file was removed, renamed, or emptied; the parent spec and the `074a` slice show zero diff.
