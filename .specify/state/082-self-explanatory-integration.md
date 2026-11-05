# Line State: 082-self-explanatory-integration

- **line_id**: 082-self-explanatory-integration
- **run_id**: r20261105T032102Z-c139
- **state**: running
- **current_stage**: checklist
- **attempts**: 1
- **breakpoint_verdict**: post-checklist — requirements.md + checklists/requirements.md + checklists/requirements-quality-20261105.md + plan.md + tasks.md present; next stage (analyze) dispatched by driver
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
- **decomposition**: plan=single-package (one coherent plan artifact; 12 FR); tasks=off
- **plan_constraint**: active since 2026-11-05T03:30:36Z; plan_commit=2f6b8bbb; approved_baseline_commit=2f6b8bbb
- **stage_started_at**: 2026-11-05T03:53:00Z
- **stage_deadline_epoch**: 1793856180
- **pid_status_log_heartbeat**: local native — no pid/status/log; completion is the subagent return + sentinel
- **last_verdict**: checklist pass — 36-item requirements-quality checklist (8 dimensions, 36/36 traceable, soft cap 40 respected, no implementation-behaviour items) at `checklists/requirements-quality-20261105.md`; existing `checklists/requirements.md` untouched; no plan-owned artifact modified (0 PLAN-EDIT owed); inputs re-measured mechanically (12 FR / 9 SC / 4 STR / 11 A; 53 task rows; 34/34 clauses claimed exactly once; 6 mutation legs; mirror `--check` all six pairs `ok`); docs-only, status=not-run-docs-only; commit 9f871e50
- **artifacts**:
  - .specify/specs/082-self-explanatory-integration/checklists/requirements-quality-20261105.md (36 items: Completeness 8 / Clarity 7 / Consistency 3 / Traceability 4 / Scenario-EdgeCase 4 / NonFunctional 4 / Dependencies 3 / Ambiguity 3)
  - .specify/specs/082-self-explanatory-integration/test-evidence/checklist-stage-checks.md (E-1 inputs, E-2 baselines, E-3 invariant parse, E-4 E3 stage-status row)
  - .specify/specs/082-self-explanatory-integration/tasks.md (53 rows: Setup 3 / Foundational 3 / US1 12 / US2 10 / US3 10 / US4 9 / Polish 6)
  - .specify/specs/082-self-explanatory-integration/test-evidence/tasks-stage-premises.md
  - .specify/specs/082-self-explanatory-integration/coverage-baseline.txt (base-sha f712cf58; 513 names)
  - .specify/memory/features/082.md (Latest tasks-stage entry)
  - .specify/memory/glossary.md (term 不言自明 (Self-explanatory))
- **stage_commits**: f712cf58 (tasks.md + premises) → 85cb38a7 (amendments + coverage baseline + features/082.md) → 1dae464d (glossary term) → 9f871e50 (checklist + stage evidence)
- **wrapup**: driver-completed for plan (session/20261105T033022Z-run-determination-speckit-plan-r20261105t033022z-e4a7.md; feedback/20261105T033022Z-speckit-plan.md); tasks stage wrap-up executed by this subagent — session 20261105T033628Z-run-determination-speckit-tasks-r20261105t033022z-082tasks.md, exec-quant 20261105T033630408551Z-b337d0f2.json, feedback 20261105T033635Z-speckit-tasks.md; checklist stage wrap-up by this subagent — run-determination skipped (simple-unit), exec-quant 20261105T035525387720Z-9e2fbd29.json, feedback 20261105T035530Z-speckit-checklist.md (threshold notice: count_since_submission=250 ≥ 10)
- **test_budget**: middle-stage targeted-set-v1 (stage_base=24c27f81); checklist is docs-only → status=not-run-docs-only (six condensed fields recorded in test-evidence/checklist-stage-checks.md E-4)
- **evidence**: .specify/specs/082-self-explanatory-integration/test-evidence; spec dir; this spine
- **stage_history**:
  - 2026-11-05 plan: done — commit 2f6b8bbb; pre-analyze plan pass (0 errors / 8 advisories); subagent hit 120-turn limit after artifacts/commit; driver completed wrap-up; mirror side-effect anomaly recorded below.
  - 2026-11-05 tasks: done — commits f712cf58 / 85cb38a7 / 1dae464d; validate-tasks 0 errors / 32 adjudicated warnings; coverage baseline frozen at f712cf58; glossary term registered; no plan-owned artifact touched (no PLAN-EDIT needed).

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
