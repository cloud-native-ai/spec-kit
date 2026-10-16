# Tasks: Agent+LLM 执行量化记录(Execution Quant Recording)

**Requirement ID**: 059
**Requirement Key**: 059-exec-quant-recording
**Related Feature**: 059 Agent+LLM 执行量化记录(Execution Quant Recording)(`.specify/memory/features.md` 行 67,Planned;详情 `.specify/memory/features/059.md`)
**Input**: Design documents from `.specify/specs/059-exec-quant-recording/`(user input `059-exec-quant-recording` 分类为背景信息:仅特性标识,无任务大纲、无追加条目)
**Prerequisites**: plan.md(✅ 含 D1–D12 裁决)、requirements.md(✅ 3 US / 15 FR / 4 SC,A1–A6 已裁决)、data-model.md(✅ 6 实体 / V1–V8)、contracts/(✅ exec-quant-cli.md + probe-registration.md)、quickstart.md(✅ 5 场景)、feature-ref.md(✅ FR/SC 映射)、checklists/requirements.md(✅ 全绿,0 澄清标记)

**Tests Mode**: ON(Constitution Principle IV "Test-First & Contract-Driven Implementation" 为强制:关键流 MUST 有自动化回归、跨服务/外部接口 MUST 有契约/集成覆盖——`constitution.md` § IV;本特性交付可执行引擎代码,plan Constitution Check IV 行裁定「测试先行全适用,tasks 期 red-first 取证」。层级 = contract 层:引擎契约测试 `tests/contract/test_exec_quant_engine.py` + 既有 `test_probe_engine_action_sets.py` 有意扩展(plan Technical Context 钉定;引擎行为面以 subprocess 契约测试覆盖,与相邻引擎同形态,无独立 unit 层)。US3 的回归网按「迁移/回归例外」置于实现之后(其守护对象在 US1/US2 落地),非 red-first。)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: 引擎三动作(collect / list-records / score)按 `contracts/exec-quant-cli.md` 实现并通过契约测试(动作封闭集、退出码、幂等、打分前置)
- DoD-2: 全部自动化测试通过——新增契约测试绿,既有 contract + integration 套件相对冻结基线零新增失败(name-level,SC-003)
- DoD-3: quickstart.md 五场景实跑留痕(`notes/quickstart-run.md`);red-first 测试取证留痕(`notes/red-first-evidence.md`)
- DoD-4: probe 注册表行落定且 `--action probes --validate` / `handlers --validate` 双绿;编译面按固定顺序再生,行预算与传播顺序测试绿;镜像义务全绿(`sync-mirrors.py --check` / `regen-command-copies.py --check` exit 0)
- DoD-5: 边界隔离零违例(SC-004:打包产物零含量化记录、全部记录凭据形值零出现)且采不到字段 100% 显式未采标记(SC-002)
- DoD-6: 验证对照 `requirements.md` SC-001..004 逐条留痕于 `verification.md`(implement 期产出)

**DoD Status**: pending

## Completion Gate

- GATE-1: Full test suite has zero NEW failures vs recorded baseline — check: `scripts/bash/run-tests.sh`(采集形态与逐名比对真源:`.specify/skills/internal/implement-feature/SKILL.md` § Test runs)+ `comm -13 .specify/specs/059-exec-quant-recording/baseline-failed.txt <current-names-file>` 为空
- GATE-2: Every mirror obligation from plan.md verified — check: `python3 scripts/python/sync-mirrors.py --check` exit 0 且 `python3 scripts/python/regen-command-copies.py --check` exit 0
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/059-exec-quant-recording/tasks.md` returns 0
- GATE-4: verification.md lists every SC-NNN with a status — check: `grep -c "SC-00[1-4]" .specify/specs/059-exec-quant-recording/verification.md` ≥ 4 且逐条有判定
- GATE-5: Registry validates — check: `python3 scripts/python/probe-utils.py --action probes --validate` 与 `--action handlers --validate` 均 exit 0
- GATE-6: Compiled-face budget and propagation order hold — check: `python3 -m pytest tests/contract/test_wrap_up_line_budget.py tests/contract/test_compile_propagation_order.py -q` 全绿

## Environment Prerequisites

- Linux 宿主采集工具(ps / /proc / ss):available — probe: `ps --version`(procps-ng 3.3.15)、`ss --version`(iproute2-5.18.0)、`/proc/self` 存在 @ 2026-10-16(生成时实探);affected: T005(collect 采集,T007–T009 间接)。任一工具缺失或非 Linux 宿主 → 对应字段按 data-model.md §1.1 缺省行为降级 `not_evaluated`,不阻塞落库;实现开工时按 never-cache 规则重探,结论变化则更新本节而非沿用此行。
- jq:available(jq-1.6 @ 2026-10-16)— 仅 quickstart 手动审计辅助(场景 1–4 命令行);引擎与测试代码仅用 Python 标准库,jq 缺失时以 `python3 -c` JSON 等价审查替代,不影响交付。
- 无容器运行时 / 镜像仓库 / 活动集群依赖 — 无任务需要 `[~]` 预标注。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **[blockedBy: T001,T002]** (optional): explicit dependency tag — this task MUST NOT start until every listed task is `[X]`. Tasks without the tag follow phase order only.
- **[green: \<contract\>#\<clause\>]** (optional): green-point attribution tag — 本特性**未使用**(2026-10-16 实测:两份契约经 `clause_extract.py` 均为 `form=md-none, clauses=0`,非机器可判定条款形态,声明即 dangling ERROR);测试文件的跨相位分区改由各行行内文字命名所负责的契约节替代(见 T003/T010/T013)。
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Task has not been completed. A run is NOT complete while any `[ ]` remains.
- `- [>]` — **Claimed / in progress**. Multi-agent claim state; single-agent runs may skip.
- `- [X]` — **Closed**. Task has been fully executed and verified.
- `- [~]` — **Deferred**. Intentional handoff with recorded reason in `verification.md` `deferred_tasks=`.

A `/speckit.implement` run is considered complete when **zero `[ ]` or `[>]` rows remain**.

## Path Conventions

- 引擎(框架源):`scripts/python/exec-quant.py`(新建);运行时镜像 `.specify/scripts/python/exec-quant.py` 由 `sync-mirrors.py` 自动投影(scripts 对 rglob 吸收,缺失 = ORPHAN error)
- 注册表(框架源):`shared/definitions/probe-definitions.md`;镜像 `.specify/shared/definitions/` 同上
- 测试:`tests/contract/test_exec_quant_engine.py`(新建)、`tests/contract/test_probe_engine_action_sets.py`(扩展)
- 编译面:`templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md`(+ per-tool 副本,经 `regen-command-copies.py`)
- 量化存储(数据目录,非代码):`.specify/memory/exec-quant/`(records.jsonl + scores.jsonl,引擎自建)
- 规格工作区:`.specify/specs/059-exec-quant-recording/`(`notes/`、`baseline-failed.txt`、`verification.md`、本文件)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 取证落地目录与 pre-change 实测基线;无代码变更。

- [ ] T001 [P] Create the evidence landing directory `.specify/specs/059-exec-quant-recording/notes/` and record the pre-change measurements into `.specify/specs/059-exec-quant-recording/notes/pre-change-measurements.md` — each entry with its real command output and capture date: wrap-up non-empty lines total (re-derived 2026-10-16: 431 = 137 `templates/commands` + 222 `skills/internal` + 72 `skills/external`, counting rule = per-file H2 Feedback/Documentation/Wrap-up non-blank lines, same rule as `tests/contract/test_wrap_up_line_budget.py`; naive whole-grep line count is the documented trap form and yields a different number), compiled-face count (72 = 23 command templates + 49 skills), `python3 scripts/python/sync-mirrors.py --check` exit 0, `python3 scripts/python/regen-command-copies.py --check` exit 0, `pytest tests/contract/test_wrap_up_line_budget.py` green
- [ ] T002 [P] Freeze the failing-test baseline name list to `.specify/specs/059-exec-quant-recording/baseline-failed.txt` — capture form, flag, and name-level comparison form are owned by `.specify/skills/internal/implement-feature/SKILL.md` § Test runs (canonical runner `scripts/bash/run-tests.sh` + `--names-out` + `comm -13`; not restated here); never-cache: re-capture at implement start whenever the tree has advanced, per the same owner

**Checkpoint**: 取证面就绪——T003 起的 red-first 测试有处落证据,编译面再生有 pre-change 对照值。

---

## Phase 2: User Story 1 - 每次执行自动落一条量化记录 (Priority: P1) 🎯 MVP

**Goal**: 任何受测单元完成一次执行后,一条量化记录自动落入 `.specify/memory/exec-quant/`:agent 程序 / LLM 详细 / 质量三字段组齐备,每字段或为带来源标注的值、或为显式 `not_evaluated`——零空缺、零臆造;采集失败非阻塞(FR-001/002/003/004/005–010/012)。

**Independent Test**: 完整执行一次任一受测单元,直读 `records.jsonl` 可找到该次 `(unit_id, run_id)` 的记录并逐字段审计(列出动作在 US2 落地,US1 期以直读存储为独立审计面);不依赖 US2/US3。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation** — red-first 取证落 `notes/red-first-evidence.md`(命令、真实输出、退出状态)。

- [ ] T003 [P] [US1] Author contract tests (red-first) in `tests/contract/test_exec_quant_engine.py` (subprocess CLI invocation form, same shape as adjacent engine contract tests; new file owns `contracts/exec-quant-cli.md` 通用参数 + 动作一 and data-model.md V1/V2/V3): argparse choices closed set == ["collect", "list-records", "score"]; storage paths `.specify/memory/exec-quant/records.jsonl` + `scores.jsonl`; kind literal "speckit.exec-quant" ([[STR-001]]) and `schema_version == 1` (V3); V1 identity closed forms (`unit_id` = /speckit.\<cmd\> | skill:\<name\> | custom:\<owner\>/\<name\>, `unit_type` ∈ command|skill|custom-unit); V2 field binary law (every measurable field is a {"value","provenance"} object or the literal `not_evaluated` [[STR-002]]; zero null / zero empty string / zero missing key; `provenance` ∈ measured|carried|user-given); exit codes 0 success (incl. degraded collection) / 1 failure with visible stderr / 2 usage error; collect idempotence (duplicate (unit_id, run_id) → hint, no second row); record the failing run as the first section of `.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md`
- [ ] T004 [US1] [blockedBy: T003] Extend `tests/contract/test_probe_engine_action_sets.py` (red-first; this file owns `contracts/probe-registration.md` §2/§3 union wiring): add `_execquant_actions()` into the union construction and new `test_exec_quant_action_set_exact` pinning choices == {collect, list-records, score}; premise-verified narrowing of plan D11 — existing `test_engine_action_sets_disjoint` (L71) and `test_registered_engine_actions_hit_real_engine_union` (L105) already assert cross-engine zero-intersection and union-hit, so no new disjoint assertion is authored (measured 2026-10-16); append the failing-run section to `.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md`

### Implementation for User Story 1

- [ ] T005 [US1] [blockedBy: T003,T004] Implement `scripts/python/exec-quant.py` — spine + collect per `contracts/exec-quant-cli.md` 动作一 and data-model.md §1.1 (stdlib only, Python ≥ 3.8, adjacent-engine form): module constants kind="speckit.exec-quant" ([[STR-001]]) / marker `not_evaluated` ([[STR-002]]) / schema_version=1; storage bootstrap `.specify/memory/exec-quant/` (records.jsonl + scores.jsonl, append-only); `--workspace-root` resolution same as adjacent engines; argparse `choices=["collect","list-records","score"]` with flags `--unit-id/--unit-type/--run-id/--workspace-root`; exit codes 0/1/2; D2 run-id resolution (explicit / adopted from the most recent run-determination record for the unit within `RECENT_WINDOW_MINUTES = 90` per plan D2 as the single adjudication / synthesized timestamp run_id with all carried fields `not_evaluated`); agent collection per D8 (self parent-chain ascent + known host-CLI process-name patterns; version via `<binary> --version` subprocess timeout 10s; `resolution` ∈ resolved|ambiguous|unresolved; MUST NOT guess a unique process); LLM collection per D6+D7 (endpoint whitelist variable names, values origin-only scheme://host stripped of path/query/credentials; connection evidence from `ss -tnp` remote ip:port, no DNS, ss absent → `not_evaluated`, never labeled "effective"; qoder adapter reading `~/.qoder/settings.json` for model/contextWindow/per-model reasoning.effort, unset effort → `not_evaluated`, MUST NOT infer the CLI default; other hosts degrade whole-group); quality carried fields from the same-run run-determination record (elapsed/tokens/satisfaction/qualification, provenance=carried, A6 no re-measure) + D5 error sources (failed_set_diff count + red-axis counts, each labeled with its source; determination record missing → whole group `not_evaluated`); per-field provenance encoding per data-model.md §1.1 field-binary rule; 64 KiB per-record cap with `truncated` path list (D9); credential-shape defense scan over the serialized record before write (D9, hit values masked and annotated); non-blocking throughout — any failure path exits 1 with a stderr message, never raising into the caller (V8)
- [ ] T006 [US1] [blockedBy: T005] Engine registration code side (the single probe-utils change): append `"exec-quant.py"` to the `_ENGINE_SIBLINGS` tuple in `scripts/python/probe-utils.py` (measured at L619, 2026-10-16 grep; plan cited L620–621) and add the exec-quant partition section to `.specify/specs/056-probe-handler-system/contracts/engine-action-sets.md` verbatim per `contracts/probe-registration.md` §3 — the existing two partition sections stay byte-identical
- [ ] T007 [US1] [blockedBy: T005,T006] Land the registry rows in `shared/definitions/probe-definitions.md` verbatim per `contracts/probe-registration.md` §1: ## Classes +1 (exec-quant, scripts slice, internal, wrap-up, code anchor `scripts/python/exec-quant.py`:`ACTIONS`,`build_record`,`resolve_run_identity`), ## Objects +4 (eq-collect-execution / eq-probe-host-process / eq-probe-host-config / eq-probe-determination-link, unit = `scripts/python/exec-quant.py`), ## Handler +1 (h-exec-quant | engine | collect | non-blocking | 15 | scripts/python/exec-quant.py — order 15 free: 10 = h-run-determination and 20 = h-feedback-record, measured L184–185), ## HandlerBinding +1 (h-exec-quant | @point:wrap-up | all); derived views rebuilt through the registry's own rebuild path, never hand-copied (FR-004); verify `python3 scripts/python/probe-utils.py --action probes --validate` and `--action handlers --validate` both exit 0 (handler action=collect must hit the real engine union via T006)
- [ ] T008 [US1] [blockedBy: T007] Regenerate compiled faces in the fixed propagation order (pinned by `tests/contract/test_compile_propagation_order.py`, order not reversible): `python3 scripts/python/probe-utils.py --action compile-embeds` (72 faces = 23 command templates + 49 skills, each `## Wrap-up` +1 line with the machine-derived label "Exec Quant", renderer untouched, fingerprints update) → `python3 scripts/python/regen-command-copies.py` (per-tool copies) → `python3 scripts/python/sync-mirrors.py --write` (runtime mirrors absorb `exec-quant.py` + `probe-definitions.md`); then verify: `python3 -m pytest tests/contract/test_wrap_up_line_budget.py tests/contract/test_compile_propagation_order.py -q` green, wrap-up total ≈ 503 ≤ 853 (pre-change 431 from T001), `sync-mirrors.py --check` and `regen-command-copies.py --check` both exit 0, and `.specify/scripts/python/exec-quant.py` exists

### Manual Verification for User Story 1

- [ ] T009 [US1] [blockedBy: T008] Real-execution smoke (quickstart.md scenario 1): execute one covered unit (a /speckit.* command) through its wrap-up including the new Exec Quant collect line, then audit `.specify/memory/exec-quant/records.jsonl` directly (list-records lands in US2): exactly one record for that (unit_id, run_id), the three field groups present, every field a provenance-carrying value or the literal `not_evaluated`, zero null/empty (SC-001); the host's known-uncollectable fields (effective-endpoint authoritative value, unset effort — brief §3 dated list as the availability baseline) fall back to `not_evaluated` (SC-002); append the scenario-1 section with real output to `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md`

**Checkpoint**: User Story 1 independently functional — a real unit execution leaves exactly one fully-auditable quant record; storage boundary and non-blocking behavior observable. US2/US3 both chain from T005/T008.

---

## Phase 3: User Story 2 - 记录可列出、可追溯、可补打分 (Priority: P1)

**Goal**: 积累的记录可经引擎动作列出(按单元/类型/时间过滤、机器可读输出),每条可追溯到 `(unit_id, unit_type, run_id)`;用户可对既有记录补录手动打分,与运行判定推导的满意度按来源区分(FR-013/FR-014)。

**Independent Test**: 落库若干记录后执行 `list-records` 验证过滤与追溯;对一条记录执行 `score` 验证来源标注;不依赖 US3。

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation** — list/score 行为在 T005 后尚不存在,红先取证同 `notes/red-first-evidence.md`。

- [ ] T010 [US2] [blockedBy: T005] Append the list/score clauses (red-first) to `tests/contract/test_exec_quant_engine.py` (this file's US2 partition = `contracts/exec-quant-cli.md` 动作二 + 动作三; T003's US1 partition untouched): list-records filters `--unit-id/--unit-type/--since/--run-id`, `--format text|json` (json = per-record full schema with per-field provenance and `not_evaluated` markers; text default), zero hits exit 0 (a result, not an error), scores joined with latest `scored_at` winning, user-given vs carried satisfaction distinguishable by provenance (FR-013/FR-014); score appends only to `scores.jsonl` with `entry_type=score` + `provenance=user-given` + optional `--note` preserved, `records.jsonl` untouched, precondition (unit_id, run_id) must exist in records.jsonl else exit 2, `--score` bounds 1–5 else exit 2 (D12 channel convention, not a scoring model); append the failing-run section to `.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md`

### Implementation for User Story 2

- [ ] T011 [US2] [blockedBy: T010] Implement list-records + score in `scripts/python/exec-quant.py` per `contracts/exec-quant-cli.md` 动作二/动作三: list-records reads records.jsonl + scores.jsonl, applies the filters, joins scores (latest `scored_at` wins), renders text (default) or json; score appends a score line to `scores.jsonl` (append-only; re-scoring appends a new row, later wins) with provenance=user-given; exit codes 0 success / 1 write failure / 2 usage (record missing, score out of 1–5, missing params); list exits 0 including zero hits

### Manual Verification for User Story 2

- [ ] T012 [US2] [blockedBy: T011] Manual QA via quickstart.md scenarios 1–3: re-audit the SC-001 record through `list-records --format json` (record count == 1, kind == speckit.exec-quant), scenario 2 marker audit on this host (not_evaluated count > 0; null/empty count == 0), scenario 3 score + join + provenance distinction (the joined score carries provenance == user-given while `quality.satisfaction` stays carried); append the scenario sections with real output to `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md`

**Checkpoint**: User Stories 1 AND 2 both work independently — records are a queryable, traceable, scoreable dataset; SC-001/SC-002 audit paths now run through the machine-readable list form.

---

## Phase 4: User Story 3 - 既有机制零回归与边界隔离 (Priority: P2)

**Goal**: 既有 feedback / probe / 运行判定引擎行为零回归(FR-015/SC-003);量化存储结构性排除于反馈打包与一切上送;任何凭据型环境值零进入记录(SC-004/FR-010/FR-011)。

**Independent Test**: 跑既有契约/集成套件与冻结基线逐名比对;产出反馈打包产物核对零含量化记录;对全部记录做凭据扫描——不依赖 US1/US2 的新增行为。

### Tests for User Story 3 (MANDATORY) ⚠️

> **Regression-net note**: these clauses guard behavior already implemented in US1/US2 (cap, credential scan, carried consistency, non-blocking were built with T005; append-only is structural). Per the migration/regression exception they are authored AFTER their subjects, pinned by `[blockedBy: T011]` — not red-first; no red evidence is owed.

- [ ] T013 [US3] [blockedBy: T011] Append the boundary regression clauses to `tests/contract/test_exec_quant_engine.py` (this file's US3 partition = `contracts/exec-quant-cli.md` 交叉约束 + data-model.md V4–V8; T003/T010 partitions untouched): V4 append-only (no action rewrites or reorders existing records.jsonl / scores.jsonl lines), V5 64 KiB cap (an oversized serialized record is truncated per-field and `truncated` is non-empty iff truncation happened), V6 credential-shape defense scan (zero credential-shaped values — api key / token / secret / authorization shapes — in any record, SC-004), V7 carried consistency (`run_id_resolution` explicit/adopted → carried values match the determination record exactly; `synthesized` → all carried fields are `not_evaluated`), V8 non-blocking (collection/write failure → exit 1 + visible stderr, no exception propagates into the caller), plus the packaging structural-exclusion premise re-check per quickstart scenario 4 ⑪ (feedback `package` reads only the feedback store — behavior asserted via the existing `tests/integration/test_feedback_*.py` suite, not re-derived here)

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T013] Boundary isolation verification (quickstart.md scenario 4): run `python3 .specify/scripts/python/feedback-utils.py --action package` (precondition ⑪ re-checked at run time against `--help` and the existing integration tests; the verification zip is removed afterward per ⑫ and never mixed with real packaged artifacts), confirm zero exec-quant entries in the package listing, and run the human credential grep as a re-check of the engine's value-level scan (⑬); append the scenario-4 section with real output to `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md`
- [ ] T015 [US3] [blockedBy: T008,T011,T013] Non-regression baseline comparison (quickstart.md scenario 5): re-run the full contract + integration suite in the owner's capture form (`scripts/bash/run-tests.sh --names-out`, form owned by `.specify/skills/internal/implement-feature/SKILL.md` § Test runs; baseline re-frozen at implement start per the same owner's never-cache rule) and compare name-level against `.specify/specs/059-exec-quant-recording/baseline-failed.txt` — `comm -13` must be empty (zero NEW failing names); comparison scope = data-model.md §4 non-regression base (20 contract + 5 integration files); the intentionally extended `test_probe_engine_action_sets.py` is already green at this point (T004 → T005 → T008 chain); record the comparison verdict in the scenario-5 section of `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md`

**Checkpoint**: All user stories independently functional — recording, consumption/scoring, and the non-regression + boundary guarantees all hold.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 跨故事的收尾义务;不改行为。

- [ ] T016 Docs adjudication (docs-step discipline — adjudicate, never blind-edit): review `docs/reference/skills/probe.md` against the new registry rows (scripts-slice Class exec-quant, Handler h-exec-quant + Binding @point:wrap-up/all) and decide whether its pointer/index content needs an update; record the decision and its rationale during implement wrap-up in `.specify/specs/059-exec-quant-recording/verification.md`; update the doc only if its own governance requires the change (plan Source-Structure note: 「实现期 docs-step 裁定,不盲改」)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 / T002 互不依赖,可并行;无代码变更
- **User Story 1 (Phase 2)**: red-first T003 → T004 → 实现 T005 → T006 → T007 → T008 → 冒烟 T009;US1 的 T005 阻塞 US2/US3 的全部实现面
- **User Story 2 (Phase 3)**: T010 → T011 → T012;起点 T010 只依赖 T005(引擎骨架存在,红先取证才成立)
- **User Story 3 (Phase 4)**: T013 → T014;T015 另需 T008(action-sets 扩展已绿)与 T011(全部引擎代码落地)
- **Polish (Phase 5)**: T016 逻辑上只依赖 T007(注册行存在),排最后以贴合 docs-step 收尾节奏

### User Story Dependencies

- **User Story 1 (P1)**: 无跨故事依赖——可独立实现、独立测试(MVP)
- **User Story 2 (P1)**: 与 US1 共享引擎文件与存储布局(US1 期建成);测试文件跨相位分区见 T003/T010 各自命名的契约节
- **User Story 3 (P2)**: 回归网与边界验证,守护对象是 US1/US2 建成的行为;无新增行为面

### Within Each User Story

- Tests MUST be written and FAIL before implementation(US1/US2 red-first;US3 按迁移/回归例外置于实现后,见 T013 节注)
- 骨架与常量先于动作实现(T005 一体承载 spine + collect)
- 注册代码侧(T006)先于注册表行(T007,validate 依赖 union)
- 编译面再生(T008)必须最后且按固定顺序

### Parallel Opportunities

- T001 / T002(Setup,[P],不同写目标)
- T003 单任务先行(创建契约测试文件;T004 因共享 red-first 证据文件而显式串行于 T003 之后)
- 其余并行机会受共享文件约束(引擎文件、测试文件、证据文件各只有一行写入责任)——为避免半写观察,刻意串行;单一执行代理下无墙钟损失

---

## Parallel Example: Setup

```bash
# Launch both Setup tasks together (different write targets):
Task: "T001 notes/ + pre-change-measurements.md"
Task: "T002 freeze baseline-failed.txt per owner form"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 单独成 MVP——P1 故事集中 US1 的 checkpoint(真实执行落一条可审计记录)独立可测且独立有价值(数据开始积累);US2(同为 P1)在其上把记录变成可消费数据集,按增量交付。

1. Complete Phase 1: Setup
2. Complete Phase 2 (US1) — red-first 取证 → 引擎 → 注册 → 编译再生 → 冒烟
3. **STOP and VALIDATE**: 按 T009 审计面独立验证 US1
4. 增量交付 US2(T010–T012)→ US3(T013–T015)→ Polish(T016)

### Incremental Delivery

1. Setup + US1 → 采集面可用(MVP!)
2. + US2 → 数据集可列出、可追溯、可打分
3. + US3 → 零回归与边界隔离证明成立
4. Polish → 文档裁定留痕;implement 收尾承担 verification.md 与 Tool 晋升评估(feature-ref.md 已记义务,不设任务行)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Verify tests fail before implementing(US3 回归网例外已在相位节注记)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Deferral discipline**: prefer `[~]` over leaving a task `[ ]` "for now"

### Assumptions & Adjudications(本相位裁决记录,随提交说明同披露)

- **A-tasks-1 Foundational 相位整体省略**:无先于全部故事的阻塞前置——引擎骨架/常量/存储布局按 data-model.md 实体映射规则归最早故事(US1)承载,US2/US3 经 `[blockedBy]` 链到 T005/T008;符合模板「无阻塞前置时整相省略并重编号」条款。
- **A-tasks-2 `[green:]` 归因标签未使用**:2026-10-16 实测两份契约经 `clause_extract.py` 为 `form=md-none, clauses=0`(非 C-N 机器可判定条款形态),声明标签即 green-dangling ERROR;按技能规则的 fallback 改为「每条测试行行内命名其负责的契约节」完成同一文件跨相位分区(见 Format 节与 T003/T010/T013)。
- **A-tasks-3 plan D11 范围收窄(premise-verified)**:plan/契约所述「新增跨引擎动作名零交集断言」经实测已存在——`test_engine_action_sets_disjoint`(L71)与 `test_registered_engine_actions_hit_real_engine_union`(L105),扩展收敛为 union helper `_execquant_actions()` + exact-pin 一项;既有断言在新引擎入 union 后自动覆盖之。
- **A-tasks-4 `_ENGINE_SIBLINGS` 行号勘正**:plan 记 L620–621,2026-10-16 grep 实测赋值行起于 `scripts/python/probe-utils.py` L619;以实测为准。
- **A-tasks-5 quickstart 场景 1 步骤 2(list-records 审计)顺延至 US2**:US1 期列出动作未落地,独立审计面改为直读 `records.jsonl`;US2 的 T012 以机器可读列出形态复审计(与 SC-001 Measurement Sources「列出动作 + 存储记录审计」双轨一致)。
- **A-tasks-6 US3 测试行不设红先义务**:其守护对象(cap/凭据扫描/携带一致性/非阻塞)在 T005 已建成,append-only 为存储结构性质——按「迁移/回归例外」置于实现后并以 `[blockedBy: T011]` 钉序,不虚构红色证据。
- **A-tasks-7 特性清单复核结论**:tasks 相位任务分解未暴露新特性、未使既有特性失效;059 保持 Planned(feature-integration:`/speckit.tasks` → Maintain `Planned`,Status unchanged);features.md 表头计数 58 与实数行 58 一致(2026-10-16 实测),无需编辑。
