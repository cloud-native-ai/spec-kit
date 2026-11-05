# Line State: 082-self-explanatory-integration

- **line_id**: 082-self-explanatory-integration
- **run_id**: r20261105T032102Z-c139
- **state**: running
- **current_stage**: implement
- **part_scope**: T019-T023 (part 4 of 10)
- **attempts**: 1
- **breakpoint_verdict**: post-analyze — analyze read-only pass complete; findings = CRITICAL 0 / HIGH 0 / MEDIUM 12 / LOW 2 (7 CRITICAL/HIGH candidates validated: 1 confirm already MEDIUM-capped, 4 downgraded, 2 rejected); next stage (implement) dispatched by driver ONLY after the driver adjudicates the U1 upsends (T006 red-first premise, C-26/T029 unsatisfiable entry point)
- **topology**: local-native (host native subagent; no qodercli)
- **target_project**: /storage/project/cloud-native-ai/spec-kit
- **authority**: docs/git-workflow.md; .specify/memory/constitution.md; .specify/instructions.md; .specify/specs/082-self-explanatory-integration/requirements.md; shared/definitions/self-explanatory-definitions.md; shared/guidelines/self-explanatory.md; shared/workflow/best-practice-optimization.md
- **slice**: 082-self-explanatory-integration — plan → tasks → checklist → analyze → implement → review → local merge; no push
- **category_quartet**: flow_class=execution; source=declaration; marker=null; error=-
- **gates**:
  - overlap-check: clear (0 overlaps)
  - decomposition-check plan: proceed (fr_count=12 ≤ 30)
  - decomposition-check tasks: split-required at the old ceiling 40 → user decision raised TASK_CEILING/TASK_MAX to 60; re-run proceeds (task_count=53 ≤ 60)
  - pre-analyze requirements: pass (errors=0, advisories=11 — mirror paths expected to be created by implement)
  - pre-analyze tasks: pass (errors=0, advisories=14)
  - flow-class lookup: execution / - / exit 0
- **decomposition**: plan=single-package; tasks=off; implement=parts (10; ≤8 tasks each): P1 T001-T006, P2 T007-T012, P3 T013-T018, P4 T019-T023, P5 T024-T028, P6 T029-T033, P7 T034-T038, P8 T039-T043, P9 T044-T047, P10 T048-T053
- **plan_constraint**: active since 2026-11-05T03:30:36Z; plan_commit=2f6b8bbb; approved_baseline_commit=2f6b8bbb
- **stage_started_at**: 2026-11-05T04:07:42Z
- **stage_deadline_epoch**: 1793856180
- **pid_status_log_heartbeat**: local native — no pid/status/log; completion is the subagent return + sentinel
- **part_checkpoint** (implement part 3/10): `part_scope=T013-T018` — **done**; commit `2161ac40` (9 files, 409+/26-). T013-T018 all `[X]` in tasks.md, no `[>]` held; 35 unchecked rows remain (T019+), by design. E3 stage-status row in `.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md`. Next part (P4 T019-T023) is driver-dispatched; this run MUST NOT start T019+.

## E2 baseline row (implement, seq=1)

| field | value |
|-------|-------|
| seq | 1 |
| slot | baseline |
| stage | implement |
| selection_basis | full-suite |
| command | `bash scripts/bash/run-tests.sh --names-out .specify/specs/082-self-explanatory-integration/baseline-failed.txt` |
| rc | 1 |
| passed | 7156 |
| failed | 26 |
| skipped | 1 |
| duration | 387.00s (wall 389s) |
| failed_names_path | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries, sorted) |
| evidence_ptr | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt`; raw full log preserved at `.specify/specs/082-self-explanatory-integration/notes/baseline-full-suite-20261105.log` (untracked — matched by `.gitignore:37 *.log`) |
| merge_source | na |
| merged_at | na |

Consumption note: this is the single full-suite run of the implement stage (TEST BUDGET). A second full suite MUST NOT be run in implement; intermediate verification uses targeted-set-v1. The 26 failures are the inherited baseline, not this feature's regressions — name-level comparison for any later part is `LC_ALL=C comm -13 baseline-failed.txt <current-names>`.

## E3 stage-status row (implement part 1)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T001-T006 |
| status | red-first-captured |
| commands | `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q` → **exit 1**, 1 failed (C-1: template missing the principle; subject absent, assertion sound) |
| control_command | `python3 -m pytest tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q` → **exit 0**, 21 passed 1.68s |
| evidence_ptr | `.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md` (R-1 RED + not-the-red control + pending-pair table) |
| claims_verified | T002 baselines re-measured (32739 B / `38:INSTRUCTIONS_BUDGET_BYTES=32768` / 17,18 / live v1.15.0 / gates total 27) — all match tasks.md; T003 coverage re-freeze delta = provenance header only (513 names unchanged); T004 three owner docs present 4508/6271/4613 B with 7/10/8 headings; T005 `sync-mirrors.py --check` exit 0, six `ok` pairs, `shared` 65 files |
| unproven | R-1's green half (T015), R-2 (T031/T032), R-3 (T043) — recorded as OPEN, not as closed |

## E3 stage-status row (implement part 3)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T013-T018 |
| status | us1-green-and-mutation-legs-proven |
| command | `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k 'not c21'` → **rc 0**, 12 passed 1 deselected; `python3 -m pytest tests/contract/test_constitution_double_landing.py -q` → **rc 0**, 19 passed |
| selection_basis | targeted-set-v1 — the exact pair the dispatch brief names: the US1 guard subset (subject completed this part) and the carrier whose count constants T016 owns |
| selected_paths | `tests/contract/test_self_explanatory_constitution.py`, `tests/contract/test_constitution_double_landing.py` |
| sufficiency | those two are the only guards judging the surfaces this part edits; two further guards (`test_fast_fail_discipline.py`, `test_confirmation_gates_sweep.py`) were run as a companion set because they pin constants referencing the same subjects. Sufficiency claimed for the edit set only; the full-suite verdict belongs to the Completion Gate, not run here |
| rc | 0 (both mandated commands) |
| passed / failed | 12 + 19 passed; 0 failed in the selected set |
| new_failures | none in the selected set; the declared expected-red `test_c21_instructions_summary_is_at_most_two_sentences` stays outside it (`-k 'not c21'`) — its green is T024's |
| companion_set | `test_fast_fail_discipline.py` + `test_confirmation_gates_sweep.py` + the new module → 3 failed / 160 passed; name-level `comm -13` shows exactly one NEW failure (the declared C-21 red); the other two are baseline-inherited (`test_g9_total_equals_frozen_baseline`, `test_residual_total_within_sc002_target`) |
| baseline | `baseline-failed.txt` (26 entries from E2), name-level comparison |
| gate_total | 27 before and after this part — C-8's zero-new-hits obligation held (the 23-vs-27 mismatch is another feature's frozen pin, inherited, not moved here) |
| evidence_ptr | `.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md`; red/green pairing and the M-1/M-2 transcripts in `notes/red-first-evidence.md`; mirror and count measurements in `notes/pre-change-measurements.md` |

- **verdict_analyze** (stage closed 2026-11-05, preserved verbatim): analyze PASS-with-open-upsends — CRITICAL=0 HIGH=0 MEDIUM=12 LOW=2; 36/36 checklist `[Gap]` items raised or dispositioned (unchecked+unraised+undispositioned = 0, gate open); validation wave 7 sent / 1 confirm / 4 downgrade / 2 reject (downgrade+reject rate 6/7, reported as a detection-quality signal); coverage `status: uncovered` (1 clause beyond frozen baseline `constitution-double-landing.contract.md#C-20`, FR-citation lane 1/12 — the accountant does not read task rows); read-only on artifacts, no plan-owned file touched (PLAN-EDIT none), no commit of any artifact; both upsends (U1-a T006 red-first premise, U1-b C-26/T029 entry point) adjudicated and repaired in tasks.md at `94e8c30d`; evidence at `test-evidence/analyze-stage-checks.md`
- **last_verdict**: implement part 3 done (`2161ac40`) — US1 surface complete: template principle (part 2), generator mandate entry (T013), both mirrors byte-identical (T014), live constitution XIX with MINOR bump 1.15.0→1.16.0 and a Sync Impact Report naming this amendment's principle (T017), carrier watchlist + three counts raised together 18/19/11 (T016). US1 subset 12 passed rc 0; carrier 19 passed rc 0; both mutation legs M-1/M-2 PASS with anti-vacuity companions and a sha256 unchanged-repository proof (T018). Five collateral guards pinned values this landing moved and were repaired in passing (x13/x15/x18/x5/x6 of `test_fast_fail_discipline.py`), each disclosed with its reason; none weakened, each keeps its own subject. No plan-owned artifact touched (PLAN-EDIT none, `requirements.md`/`plan.md`/`data-model.md`/`contracts/`/`quickstart.md`/`research.md`/`feature-ref.md` unmodified). No Completion Gate run, no Feature status flip, no implement Feedback/Wrap-up, no push.
- **next_step**: driver adjudicates the part-4 held-open C-18 reading, then dispatches implement part 5 (P5 `T024-T028`: live reconcile, symlink check, mirror sync, M-3/M-4 mutation legs). Part 4 stopped at the part boundary by design; C-15's green (`test_c1_live_instructions_carry_all_template_sections`) and C-21's red/green pairing both close at T024.
- **stage_commits**: 94caea76 (implement part 1) → 171d4bcc (implement part 2) → 8daf6b65 (C-21 ordering correction) → 2161ac40 (implement part 3) → 567834e2 (implement part 4)

<!-- The first "gates" key above is a preserved historical section; the canonical list follows. -->

- **gates**: (as listed above)
- **artifacts**:
  - .specify/specs/082-self-explanatory-integration/checklists/requirements-quality-20261105.md (36 items: Completeness 8 / Clarity 7 / Consistency 3 / Traceability 4 / Scenario-EdgeCase 4 / NonFunctional 4 / Dependencies 3 / Ambiguity 3)
  - .specify/specs/082-self-explanatory-integration/test-evidence/checklist-stage-checks.md (E-1 inputs, E-2 baselines, E-3 invariant parse, E-4 E3 stage-status row)
  - .specify/specs/082-self-explanatory-integration/tasks.md (53 rows: Setup 3 / Foundational 3 / US1 12 / US2 10 / US3 10 / US4 9 / Polish 6)
  - .specify/specs/082-self-explanatory-integration/test-evidence/tasks-stage-premises.md
  - .specify/specs/082-self-explanatory-integration/coverage-baseline.txt (base-sha f712cf58; 513 names)
  - .specify/specs/082-self-explanatory-integration/test-evidence/implement-part-2.md
  - .specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md
  - .specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md (R-1 red + R-1-GREEN pair, M-1/M-2 transcripts, open-pair table)
  - .specify/specs/082-self-explanatory-integration/notes/pre-change-measurements.md (T002/T012 baselines + part 3 mirror/count/gate measurements)
  - .specify/memory/constitution.md (v1.16.0; Principle XIX + Sync Impact Report)
  - skills/internal/manage-constitution/SKILL.md + .specify mirror (MUST-include list 11 entries)
  - .specify/memory/features/082.md (Latest tasks-stage entry)
  - .specify/memory/glossary.md (term 不言自明 (Self-explanatory))
- **stage_commits**: f712cf58 (tasks.md + premises) → 85cb38a7 (amendments + coverage baseline + features/082.md) → 1dae464d (glossary term) → 9f871e50 (checklist + stage evidence)
- **wrapup**: driver-completed for plan (session/20261105T033022Z-run-determination-speckit-plan-r20261105t033022z-e4a7.md; feedback/20261105T033022Z-speckit-plan.md); tasks stage wrap-up executed by this subagent — session 20261105T033628Z-run-determination-speckit-tasks-r20261105t033022z-082tasks.md, exec-quant 20261105T033630408551Z-b337d0f2.json, feedback 20261105T033635Z-speckit-tasks.md; checklist stage wrap-up by this subagent — run-determination skipped (simple-unit), exec-quant 20261105T035525387720Z-9e2fbd29.json, feedback 20261105T035530Z-speckit-checklist.md (threshold notice: count_since_submission=250 ≥ 10); analyze stage wrap-up by this subagent — run-determination 20261105T040447Z-run-determination-speckit-analyze-r20261105t032102z-c139-ana.md, exec-quant 20261105T040449355071Z-b07129a1.json, feedback 20261105T040452Z-speckit-analyze.md (threshold notice: count_since_submission=251 ≥ 10)
- **test_budget**: middle-stage targeted-set-v1 (stage_base=2f5ab4bd); analyze is docs-only → status=not-run-docs-only (six condensed fields in test-evidence/analyze-stage-checks.md E-3); one load-bearing exception executed — `pytest test_constitution_double_landing.py test_instructions_section_propagation.py -q` → 21 passed 1.67s, run to test T006's red-first premise, not as a regression gate; parts 2 and 3 each ran their targeted set only (no second full suite)
- **evidence**: .specify/specs/082-self-explanatory-integration/test-evidence; spec dir; this spine
- **stage_history**:
  - 2026-11-05 plan: done — commit 2f6b8bbb; pre-analyze plan pass (0 errors / 8 advisories); subagent hit 120-turn limit after artifacts/commit; driver completed wrap-up; mirror side-effect anomaly recorded below.
  - 2026-11-05 tasks: done — commits f712cf58 / 85cb38a7 / 1dae464d; validate-tasks 0 errors / 32 adjudicated warnings; coverage baseline frozen at f712cf58; glossary term registered; no plan-owned artifact touched (no PLAN-EDIT needed).
  - 2026-11-05 checklist: done — commit 9f871e50; 36 quality items; inputs re-measured; docs-only.
  - 2026-11-05 analyze: done (read-only) — CRITICAL 0 / HIGH 0 / MEDIUM 12 / LOW 2; 7 CRITICAL/HIGH candidates sent to a fresh-context validation wave (1 confirm / 4 downgrade / 2 reject); 36/36 checklist gaps raised or dispositioned; no artifact, checklist, registry or plan-owned file modified; evidence commit holds `test-evidence/analyze-stage-checks.md` + this spine only.
  - 2026-11-05 implement part 1: done — commit 94caea76; T001-T006 closed; baseline full suite captured once (26 failed / 7156 passed / rc=1 / 387s); red-first signal belongs to the NEW module while both pre-existing suites stay green.
  - 2026-11-05 implement part 2: done — commits 171d4bcc + 8daf6b65; T007-T012 closed; template principle XVIII landed; US1 subset 12 passed with C-7 mandate side and C-21 declared expected-red.
  - 2026-11-05 implement part 3: done — commit 2161ac40; T013-T018 closed; US1 surface complete on all three surfaces; mutation legs M-1/M-2 PASS.
  - 2026-11-05 implement part 4: done with one held-open clause — T019-T022 closed (C-10/C-11/C-14/C-17 carriers + template section, C-21 green); T023's budget raise applied and recorded but its C-18 claim awaits the driver's reading choice (34816 vs 33792); one new and attributable failure, the deferred T024 live reconcile.

## Analyze-stage upsends (need driver adjudication before implement)

Two items were found by this stage that an in-passing repair MUST NOT absorb (each is a decision
between readings, not a single consistent correction):

- **U1-a — T006's red-first premise is false as written.** `tasks.md` T006 expects
  `test_constitution_double_landing.py` + `test_instructions_section_propagation.py` to go red before the
  feature lands ("因 STR-001 尚不存在而失败,或对既有断言为空真"), and T051 closes only when "T006 的红" is
  paired with T015/T031/T043's green. Measured this run: **21 passed** in 1.67 s. Neither suite
  references `STR-001`, so the first branch is impossible and the second is green-vacuous. `tasks.md`
  § Adjudicated validator warnings also states T006 "turns nothing green" while the same paragraph counts
  it among the red captures. The real red-first evidence this feature needs is the *new* module
  (`test_self_explanatory_constitution.py`, T007) run before its artifacts land; no task does that.
- **U1-b — C-26 / T029 cannot pass against the installed entry point as written.** C-26 states an
  unconditional failure on a missing path and T029 forbids encoding the stale-install exemption, while
  `tasks.md` § Environment Prerequisites records the installed `specify` as `partial` and T036 records
  the weaker reading. No task performs the rebuild (`pip install -e .`) that would make T029 satisfiable.
  Repair is a tasks-file edit (add a rebuild step before T029, or scope T029 to the rebuilt entry point).

## 框架观察（implement part 3，2026-11-05）

- **现象**: `sync-mirrors.py --only skills` 匹配不到 `skills/internal/` 的镜像对，SKILL 镜像留在
  `DIFF` 而不报错——`--only` 的前缀 `skills` 先命中了并列的 `skills/external → .specify/skills`
  一对，于是内部层被跳过；退出码仍为 0，`DIFF` 只出现在逐行输出里。
  **框架位置**: `scripts/python/sync-mirrors.py` 的 `--only` 前缀匹配 vs `MIRROR_PAIRS` 中
  `skills/external` 与 `skills/internal` 两个并列对。
  **影响**: 一次「同步 skills」的写入会静默漏掉内部层，而 `sync-mirrors.py --check` 随后会以
  `DIFF` 报出——靠后面的 check 兜住，但 owner 自己的写入通道给出了半完成的“成功”。
  按 T014 的括号替代读法（“或全量 `--write` 后复查”）改跑 `--only skills/internal` 后一致。

- **现象**: `tests/contract/test_fast_fail_discipline.py` 在模块中部把 `PRINCIPLE_TITLE`
  重新绑到 Fast Fail 标题（第 933 行覆盖第 99 行），该文件后半段的守卫因此都在用一个与注释
  所指主题不同的名字；`test_x15` 原先的 `PRINCIPLE_TITLE in entries` 断言在监听清单里找的是
  Fast Fail，而不是本次新增的条目——它无法因自己的主题损坏而转红。
  **框架位置**: `tests/contract/test_fast_fail_discipline.py` 的重复模块级常量。
  **影响**: 本次把 x15 改指“派生自 owner 的最后一条”以恢复可红性；同一文件里其余复用该常量的
  断言仍是旧的绑定方式，建议后续把该常量按段落分区重命名（本阶段未做，避免越界改另一特性的守卫）。

- **现象**: 本阶段起点发现 `.specify/` 目录权限为 `drw-r--r--`（缺执行位），`scripts/python/`
  下全部文件对当前用户不可读，`git status` 因此无法读取部分路径。
  **框架位置**: 工作树权限，非框架代码。
  **影响**: 这类状态会让执行者把“读不到”误报为“文件不存在”。本阶段以一次 `chmod -R u+rwX`
  修复 `.specify/ scripts/ templates/` 后继续，`git diff --summary` 确认没有模式位变更被记录。

## Split Record（2026-11-05T03:38:51Z）

- **verdict**: split-required
- **measured**: fr_count=12; task_count=53
- **ceilings**: fr_ceiling=30; task_ceiling=40
- **reasons**: `task rows=53 exceeds ceiling 40`
- **base_commit**: f712cf58 (tasks.md landed); stage base dc83514e
- **proposed_slices**:
  1. **Task re-cut to ≤40（gate-compliant, no feature split）** — keep Feature 082 and all 12 FR; consolidate tightly coupled test/verification and setup/polish rows to ≤40 without dropping FR/SC/contract coverage; re-run tasks U4.
  2. **User waiver — keep 53 tasks** — record an explicit waiver of the 40-task ceiling; proceed to checklist/analyze; the implement stage is split into ≤8-task parts regardless.
  3. **Feature split 082a/082b** — only as a scope decision with a documented exception to the 8–30 FR floor: 082a (8 FR: FR-001…FR-008) + 082b (4 FR: FR-009…FR-012); each gets its own spec directory and registry binding; both must re-run the full chain. This violates the 8-FR floor for 082b and needs explicit user authorization.
- **status**: resolved — user decision 2026-11-05 raised the framework task ceiling to 60; gate re-run proceeds; line resumes at checklist.

## U5 Upsend（四要素）

- **发现了什么**: tasks U4 `decomposition-check --mode tasks` returns `split-required`: task rows=53 exceeds ceiling 40. The feature has 12 FR, below the 8-FR floor for a two-slice split (8+4), so no valid feature-slice split exists without an exception.
- **为何吃重**: the tasks breakdown is highly granular (53 rows) for a 12-FR integration; the gate ceiling is 40; the split floor is 8 FR per slice; the feature is too small to split into valid slices but too large in task count.
- **已产生的中间产物逐项可定位**: tasks.md at f712cf58; coverage baseline at 85cb38a7; glossary at 1dae464d; tasks premise/evidence at test-evidence/tasks-stage-premises.md; plan artifacts at 2f6b8bbb; Feature 082 = Planned; this spine.
- **可选处置**: (1) task re-cut to ≤40; (2) user waiver for 53 tasks; (3) feature split 082a/082b with an explicit 8-FR-floor exception. Driver MUST NOT dispatch checklist/analyze before the choice.

## Split Resolution（2026-11-05T03:53:00Z）

- **decision**: user chose to raise the framework `split-required` threshold to 60 instead of splitting Feature 082.
- **change**: `TASK_CEILING` (decomposition-check.py) and `TASK_MAX` (admission-check.py) 40 → 60; owner doc `references/efficiency-model.md`, `SKILL.md`, `docs/reference/skills/sdd-loop-driver.md`, and the two tests aligned.
- **commits**: edd18472 (framework change) + 24c27f81 (docs/test alignment).
- **verification**: 16 + 66 targeted tests passed; `decomposition-check --mode tasks` now `proceed` (fr=12, tasks=53, task_ceiling=60).
- **consequence**: the fast-lane medium-band endpoint moves to 60 by the existing invariant test; a future feature with 41–60 tasks no longer triggers a split.

- 2026-11-05 tasks (continued): U4 pass after threshold change — edd18472 + 24c27f81; gate proceed; checklist dispatched.
- 2026-11-05 checklist: done — commit 9f871e50; 36 quality items in a new dated file, existing checklists/requirements.md untouched; all items traceable and in question form (re-parsed, not by eye); inputs re-measured mechanically; docs-only status=not-run-docs-only; no plan-owned artifact touched (no PLAN-EDIT owed); no anomaly, no in-passing repair beyond one self-corrected evidence figure.

## 框架观察（checklist 阶段，2026-11-05）

- **现象**: `shared/workflow/objective-analysis-gate.md` § "Binding set is owned by the test" 给出的发现命令是 `grep -rl 'objective-analysis-gate.md' templates/commands/`，但 S3 命令瘦身后命令模板已不再携带该指针（指针落在 `skills/internal/<skill>/SKILL.md`），因此该命令返回空集，而 `tests/contract/test_objective_analysis_gate.py` 的 `BINDING` 名册明确把 `checklist` 列为绑定命令。
  **框架位置**: `shared/workflow/objective-analysis-gate.md` § Binding set / § Reach of the ambient pointer。
  **影响**: 按发现命令自检的执行者会得出“本命令不绑定”的错误结论。建议把该命令改为同时搜索 `templates/commands/` 与 `skills/internal/`（本阶段未改 shared 制品，避免越界）。

- **现象**: 同一 owner 的 "When the gate fires" 只描述“同一会话、同一作者”，未说明派发简报中的 `DECLARED_CHECK` 是否能把触发条件扩展到跨运行的同线阶段。
  **框架位置**: `shared/workflow/objective-analysis-gate.md` § When the gate fires；`agents/sdd-executor.agent.md` 的派发注入子句。
  **影响**: 无人值守 SDD 循环里每个阶段都是新运行，作者身份本就不同，但派发方可能已做同作者检测。判据缺一条时本阶段按“可疑从严”走直接读取并在产物内披露，通道选择由编排者裁定。

- **现象**: `create-checklist` SKILL 与 `templates/commands/checklist.md` 都只写“读 `requirements.md` + `plan.md`/`tasks.md` 做缺口发现”，未要求核对 `requirements.md` 与 `contracts/` 之间的条款级对应；本阶段发现 `requirements.md` 对 C-20 摘要上限、C-21 句数上限、C-12 小节位置三处义务完全沉默。
  **框架位置**: `.specify/skills/internal/create-checklist/SKILL.md` § 4 Load feature context 的表。
  **影响**: 缺口发现若只读 plan/tasks，会漏掉“契约比需求更细”这一最常见缺口形态；建议在输入表中加一行 `contracts/`（仅用于发现需求遗漏）。

## 框架观察

- **现象**: plan 子代理在产物与提交完成后、自身 wrap-up 前触及 120 回合上限。
  **框架位置**: `agents/sdd-executor.agent.md` 的 `run-turn-budget: 120`；plan 阶段产出 7 类设计产物。
  **影响**: 驱动者需补跑 run-determination / exec-quant / feedback，增加一次恢复成本。
- **现象**: plan 的 `test-evidence/plan-stage-checks.md` 用 mtime 相同证明“未写镜像”，但 `.specify/shared/` 下三份镜像实际存在且未跟踪。
  **框架位置**: `sync-mirrors.py` 的 copy2 语义；plan 的 mirror obligation 证据写法。
  **影响**: implement 必须接管并提交镜像；mtime 不能作为“未写”证据。
- **现象**: `shared/workflow/expression-gates.md` 中的 `pre-analyze-check.py` 写作 `.specify/scripts/python/` 下，实际入口在 `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`。
  **框架位置**: `.specify/shared/workflow/expression-gates.md` 的 G-tasks-fact 描述与脚本真实落点不一致。
  **影响**: 执行者需自行搜索入口；建议后续把路径改成相对 skills 目录的写法（本阶段未改，避免越界修改 shared 制品）。
- **现象**: C-20 在 `mirror-distribution.contract.md` 与 `constitution-double-landing.contract.md` 双重定义（指针 + 定义），覆盖会计把条款归属到实际定义文件，与执行者按 repo-root 解析读到的文件不同。
  **框架位置**: `account-clause-coverage.py` 的 clause→file 归属规则 vs `[green:]` 的 co-located→repo-root→cwd 解析次序。
  **影响**: tasks 阶段出现 1 条“baseline 外未覆盖”孪生条目；本阶段以 T010 同时声明 C-20 与 C-21 的方式显式披露而非改写会计口径。

## Implement Part Plan（2026-11-05T04:07:42Z）

- P1 T001-T006 — setup + foundational + red-first; **baseline full suite here**.
- P2 T007-T012 — US1 tests/first implementation.
- P3 T013-T018 — US1 remaining.
- P4 T019-T023 — US2 tests/first implementation.
- P5 T024-T028 — US2 remaining.
- P6 T029-T033 — US3 tests/first implementation (venv + editable install for distribution).
- P7 T034-T038 — US3 remaining.
- P8 T039-T043 — US4 tests/first implementation.
- P9 T044-T047 — US4 remaining.
- P10 T048-T053 — polish + Completion Gate + implement wrap-up + `IMPLEMENT-DONE`.

## Analyze Adjudication（2026-11-05T04:07:42Z）

- CRITICAL=0 / HIGH=0 → analyze gate open; checklist accountability 36/36.
- U1-a (T006 red-first premise) and U1-b (T029 distribution entry point) repaired in tasks.md commit 94e8c30d; re-validated: validate-tasks 0 errors / 31 adjudicated warnings, pre-analyze tasks pass, decomposition proceed.
- Plan-owned MEDIUM findings (C-20/C-21 placement, count drift, FR-004 budget-rule gap, etc.) are carried to review; implement MUST NOT edit plan-owned artifacts or requirements.md.

## Implement part 2 checkpoint（2026-11-05T04:23:23Z）

- **part_scope**: T007-T012 — done; T007-T012 all `[X]` in tasks.md.
- **artifacts**: `templates/constitution-template.md` + `.specify/templates/constitution-template.md` (principle XVIII), `tests/contract/test_self_explanatory_constitution.py` (457 lines), `notes/pre-change-measurements.md` (T012 `hits: []`).
- **targeted set**: `test_self_explanatory_constitution.py` → 12 passed / 1 expected-red (`test_c21_instructions_summary_is_at_most_two_sentences`; C-21 green is T022). C-7 mandate-side is expected-red until T013.
- **evidence**: `test-evidence/implement-part-2.md`; baseline 26 inherited failures, no new regression outside the two declared expected-reds.
- **no plan-owned edits**; no Completion Gate, no status flip, no implement wrap-up.
- **next**: P3 T013-T018 (generator skill entry, mirrors, US1 green, live constitution, mutation legs).

- 2026-11-05 implement part 2 correction: 2026-11-05T04:23:52Z — 8daf6b65; C-21 green deferred to T024; no plan-owned edits.

## Implement part 3 checkpoint

- **part_scope**: T013-T018 — done; T013-T018 all `[X]` in tasks.md; no `[>]` held; 35 unchecked rows remain (T019-T053), untouched by this part.
- **commit**: `567834e2` (8 files, 475+/10-).
- **artifacts**:
  - `skills/internal/manage-constitution/SKILL.md` + `.specify/skills/internal/manage-constitution/SKILL.md` — MUST-include list 10 → 11 (T013/T014)
  - `.specify/memory/constitution.md` — Principle XIX, `**Version**:` 1.15.0 → 1.16.0, Sync Impact Report prepended (T017)
  - `tests/contract/test_constitution_double_landing.py` — watchlist + `TEMPLATE_COUNT` 18 / `LIVE_COUNT` 19 / `COMMAND_COUNT` 11 (T016)
  - `tests/contract/test_fast_fail_discipline.py` — five collateral pins raised / repointed (disclosed repairs)
  - `notes/red-first-evidence.md` — R-1 pair closed + M-1/M-2 transcripts (T015/T018)
  - `notes/pre-change-measurements.md` — part 3 mirror/count/gate measurements
  - `test-evidence/implement-part-3.md` — E3 stage-status row
- **targeted set**: US1 subset 12 passed (rc 0, `-k 'not c21'`) + carrier 19 passed (rc 0). Companion set 160 passed / 3 failed, of which exactly one is new (the declared C-21 red) and two are baseline-inherited.
- **in-passing repairs**: `test_x13`/`test_x15`/`test_x18`/`test_x5`/`test_x6` in `test_fast_fail_discipline.py`. `test_x6` was a genuine defect repair (it asserted a fixed older title in a 40-line window that every newer amendment pushes out), not a window widening.
- **gate budget**: `scan-confirmation-gates.py --json` total = 27, unchanged from T002 — C-8 held.
- **no plan-owned edits** (PLAN-EDIT none); no Completion Gate, no Feature status flip, no implement Feedback/Wrap-up, no push.
- **next**: P4 T019-T023 (US2 tests + instructions template section). C-21's green is T024's and is NOT closed here.

- 2026-11-05 implement part 3: 2161ac40; part 4 T019-T023 starts.

## Implement part 4 checkpoint（2026-11-05）

- **part_scope**: T019-T023 — T019/T020/T021/T022 `[X]`; **T023 `[X]` with a held-open clause
  marker** (C-18 not proven, see the anomaly below). 30 task rows remain unchecked (`[ ]` or
  `[>]`): T024-T053, untouched by this part. Grep check at part end: `grep -cE '^- \[[ >]\]'` = 30.
- **artifacts**:
  - `tests/contract/test_instructions_section_propagation.py` — new C-10 / C-11 / C-14 tests plus the
    `_generator_substitutions()` / `_render()` anti-drift companion; module docstring records the
    clause mapping and the isolation note (the guard renders the framework-source template rather
    than calling the generator, which renders from `.specify/templates/`).
  - `tests/contract/test_instructions_size_budget.py` — new `test_c17_real_tree_live_size_is_within_the_raised_budget`,
    budget derived via the existing `_budget_bytes()`, no literal.
  - `templates/instructions-template.md` — `## Self-Explanatory Structure (不言自明)` inserted between
    `## Grounded Naming` and `## Bilingual Expression (双语表述)`; no existing section moved.
    Body = 1 summary sentence + 1 pointer line to `.specify/shared/definitions/self-explanatory-definitions.md`; 618 B.
  - `scripts/bash/generate-instructions.sh` — `INSTRUCTIONS_BUDGET_BYTES` 32768 → 34816, with the
    old/new value, measured size (33357 B), reason and magnitude rule in the comment above it.
  - `notes/red-first-evidence.md` — § R-4 (red capture + ordering note) and the C-21 shape finding.
  - `test-evidence/implement-part-4.md` — E3 stage-status row, red/green capture, measurements table.
- **targeted set** (the three commands the brief names): `test_self_explanatory_constitution.py`
  rc 0 / 13 passed; `test_instructions_section_propagation.py` **rc 1** / 5 passed 1 failed;
  `test_instructions_size_budget.py` rc 0 / 13 passed.
- **the single failure is the deferred obligation, not a regression**:
  `test_c1_live_instructions_carry_all_template_sections` reports the missing section in
  `.specify/instructions.md`. It passed at `2161ac40` (checked with `git show HEAD:…`), and it closes
  at T024, which owns the live reconcile. Confirmation run with only that case deselected:
  4 carriers, **50 passed / 1 deselected**, so no other guard moved.
- **C-21 turned green after T022**, as the brief predicted, and it did so only after an in-passing
  repair: the C-21 carrier strips every line containing the pointer path before counting sentences,
  so a section whose summary and pointer share a line counts as **zero** sentences. The first draft
  did exactly that and went red on a real defect (not an expected-red). Repaired to one summary
  sentence + pointer on its own line; the dropped second sentence also restated owner rules, so the
  short body is the correct shape rather than a budget concession. Transcript in `notes/red-first-evidence.md`.
- **in-passing repairs**: (1) the C-21 section shape above; (2) the R-4 open-pairs table duplicated
  the one already in the file, so the older copy was removed and a single table kept.
- **no plan-owned edits** (`PLAN-EDIT: none`); `requirements.md` / `plan.md` / `data-model.md` /
  `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` unmodified.
- **no** Completion Gate, **no** Feature status flip, **no** implement Feedback/Wrap-up, **no** push,
  **no** mirror sync and **no** live reconcile (both are part 5).

### Part 4 held-open item（需编排者裁定）

- **C-18 / T023 — the raise magnitude has two compliant readings.** The applied constant is 34816.
  Under the T-001 rule as written — the smallest multiple of 1024 leaving at least 1024 B of
  headroom under the `over` verdict (`size >= budget`) — the candidates compute, against the
  measured 33357 B post-injection size, as: **32768** over by 590; **33792** within with 434 B
  headroom (i.e. the rule's literal arithmetic would pick 33792, not 34816); **34816** within with
  1458 B headroom.
  The second reading depends on the section body's own size, which is not yet frozen that tightly:
  with the body re-cut to one shorter sentence the injection lands at 33233 B and **33792 then
  leaves 558 B**, still compliant under either reading.
  Reading A = keep 34816 (headroom measured against the section as it stands, at the cost of one
  extra 1024 B over the literal minimum). Reading B = set 33792 (the literal minimum against the
  measured size, with 434 B headroom).
  This is a choice between readings, not a correction, so it is surfaced rather than settled:
  **T023's `[green:] C-18` claim is NOT proven** until the orchestrator picks one. Both readings
  satisfy the hard constraint (a multiple of 1024, at least 1024 B of headroom under one of the two
  sizes named here), and the value has exactly one owner, so switching is a one-line change plus this
  comment.
- **last_verdict**: implement part 4 done with one held-open clause — T019/T020/T021/T022 closed with
  red-first capture and green after landing; T023's raise applied and recorded but its C-18 claim
  awaits the reading above. One new failure in the targeted set, named and attributable to the
  deferred T024 reconcile.

- 2026-11-05 implement part 4: see the checkpoint above; next is P5 T024-T028 (live reconcile,
  symlink check, mirror sync, M-3/M-4). The C-18 reading must be adjudicated before part 5 lands the
  mirrors, because T026 mirrors `generate-instructions.sh` and re-syncing after a second edit would
  touch the same file twice.
