# Specification-Driven Development (SDD) Process Review Report: 069b — Isomorphism Map, Migration Compatibility & Measurement Instruments

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 069b (Feature 069, second and final slice) |
| Requirement Key | `069b-isomorphism-migration-metrics` |
| Requirement Name | 同构映射、迁移兼容与度量仪器（Isomorphism Map, Migration Compatibility & Measurement Instruments） |
| Related Feature | 069 执行/表达二元分类与文档型 SDD 同构 |
| Repository | spec-kit (self-hosting framework repository + its own client runtime) |
| Repository URL | `gitlab` → `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH only; no HTTPS web remote) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty (the branch is unpushed). No `blob/` URL can resolve. Every citation below is a repo-relative path with an absolute-path supplement; historical states are recoverable with `git show <sha>:<path>` from the local checkout. |
| Branch | `069b-isomorphism-migration-metrics` |
| Commit SHA | `414538125ef85c5d02771a04d0a4d2a1f531869b` (short: `41453812`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-25 |
| Reviewer (Agent) | Qoder SDD review agent (`/speckit.review` → `review-sdd-process`) |
| Environment | macOS darwin/arm64; system `python3` 3.9.6; pytest 9.1.1 only in `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest` (repo `.venv` has no pytest); git 2.54.0 (Apple Git-157); `go1.27.2` |
| spec-kit Source Snapshot | this repository @ `41453812` (the feature edits framework sources `shared/`, `scripts/`, `tests/` and their `.specify/` mirrors) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 283 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069b-isomorphism-migration-metrics/requirements.md` | 14 FR / 5 SC / 3 STR slice requirements; explicit out-of-slice allocation |
| plan.md | 311 | `…/069b-isomorphism-migration-metrics/plan.md` | Carrier, table shape, migration/distribution, three baselines, test strategy, mirror obligations |
| tasks.md | 298 | `…/069b-isomorphism-migration-metrics/tasks.md` | 29 task rows (3/6/4/10/6), 51 `[green:]` claims, 9 completion gates |
| data-model.md | 179 | `…/069b-isomorphism-migration-metrics/data-model.md` | E1–E10 file-structure entities (no runtime store) |
| research.md | 216 | `…/069b-isomorphism-migration-metrics/research.md` | R1–R15 decisions with rejected alternatives |
| quickstart.md | 176 | `…/069b-isomorphism-migration-metrics/quickstart.md` | 7 verification scenarios, route a/b per scenario |
| feature-ref.md | 88 | `…/069b-isomorphism-migration-metrics/feature-ref.md` | FR→design→contract→test map; SC→measurement source |
| verification.md | 352 | `…/069b-isomorphism-migration-metrics/verification.md` | Per-SC status, gates, DoD rows, assumptions, residual |
| contracts/isomorphism-map.md | 132 | `…/contracts/isomorphism-map.md` | 14 clauses: carrier, table shape, cell grammar, enforcement truth, boundaries |
| contracts/ledger-reconciler.md | 177 | `…/contracts/ledger-reconciler.md` | 16 clauses: floor, coverage, `red_kind`, delegation, faces, scope |
| contracts/migration-distribution.md | 110 | `…/contracts/migration-distribution.md` | 11 clauses: unrefreshed behaviour, refresh atomicity, snapshots, mirrors |
| contracts/measurement-instruments.md | 100 | `…/contracts/measurement-instruments.md` | 10 clauses: three quantities, channels, `not-evaluated`, vocabulary boundary |
| checklists/isomorphism-migration-metrics.md | 151 | `…/checklists/isomorphism-migration-metrics.md` | 36 requirement-quality items (35 `[x]` / 1 `[ ]`) |
| notes/pre-change-measurements.md | 317 | `…/notes/pre-change-measurements.md` | T001 pre-change baselines (mirrors, structure face, HEAD, dirty tree) |
| notes/red-first-evidence.md | 457 | `…/notes/red-first-evidence.md` | R1–R9 red runs and G1–G6 green runs with commands/outputs |
| notes/quickstart-run.md | 386 | `…/notes/quickstart-run.md` | Scenario 1–7 + docs-sync transcripts |
| notes/expression-baseline.md | 71 | `…/notes/expression-baseline.md` | Three-quantity freeze row + recheck commands |
| notes/migration-samples.md | 85 | `…/notes/migration-samples.md` | 3 pre-frozen customer snapshots + two post-freeze mechanism corrections |
| notes/parent-fr-mapping.md | 113 | `…/notes/parent-fr-mapping.md` | Slice ID → parent ID → handling value for 14 FR / 5 SC |
| notes/test-baseline-contract.txt | 40 | `…/notes/test-baseline-contract.txt` | Frozen 33 failing node ids (frame-repo contract+unit suite) |
| coverage-baseline.txt | 497 | `…/coverage-baseline.txt` | Frozen 495 uncovered clause names (excluding 069b's own clauses) |

## 1. Process Execution Timeline

Reconstructed from `git log` scoped to `.specify/specs/069b-isomorphism-migration-metrics/` (16 commits) plus working-tree evidence. All commits are local-only (branch unpushed).

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Requirements landed; no `/speckit.clarify` run; 13 self-adjudicated Q/A recorded | `f0df3d0b`; `requirements.md:267` “**未向用户发起访谈**…其余缺口…自行裁决” | Yes — clarify skipped, disclosed. Also `wall_clock` freeze point is this commit, so the slice's own clock starts here |
| 2 | Plan + research + data-model + 4 contracts + quickstart + feature-ref | `410e7c67` | None |
| 3 | Plan-gate output pasted into plan, then its advisory count corrected (9 → 10) | `afb7e8b4`, `385a05b1` | Minor: an unfilled/miscounted gate transcript needed a second commit |
| 4 | FR-009 traced to a map-carrier clause after plan | `02abd56c` | Post-plan traceability repair |
| 5 | Tasks landed (29 rows, 51 `[green:]`) | `84dd63e5` | None |
| 6 | Quality checklist run; 11 groups of facts/feasibility defects corrected in the same round | `9bfe53de`; checklist § 实测前提 | Yes — requirements/plan/tasks were materially corrected after tasks were frozen |
| 7 | “Analyze round”: parse floor 78 → 39, `wall_clock` start instrument `git log -1` → `--diff-filter=A`, coverage baseline frozen | `47106762`; `tasks.md:97` | Yes — three criteria repairs during a self-run “analyze round”; **no `/speckit.analyze` run-determination record exists** (see F6) |
| 8 | Pre-change baselines frozen (mirrors, structure face, test names) | `c38b44cc`; `notes/pre-change-measurements.md` | None |
| 9 | US1: owner map + 4 boundaries + `--action isomorphism` | `efe63551` | None |
| 10 | US2: pointer convergence + 3 snapshot evidence | `d4aaac6e` | None |
| 11 | Snapshot outcome re-recorded after the xuanji-function harness corrections | `7be06a08` | Yes — measurement harness changed after the first snapshot run |
| 12 | US3 red-first tests (5 files) | `ed713ede` | None — red-first ordering respected |
| 13 | US3 implementation: ledger version, `coverage`/`red_kind`, `delegation`, `faces` | `5d5331b9`; commit message claims “the only edit to a 069a test is the A-1 one-line version declaration” | Yes — see F2: a second 069a test is edited in the next commit |
| 14 | Polish T024–T029: mirrors, docs sync, regression, SC evidence, registry; **edits `shared/workflow/expression-gates.md` and `tests/contract/test_expression_gates_doc.py`** | `33c47fd5`; `git diff --stat f0df3d0b^..HEAD` → 3 files incl. the gate owner | Yes — declared off-limits surface edited; not registered as a task row (F2) |
| 15 | Post-closure docs-sync evidence | `41453812` | Minor: T025 evidence landed after the “close” commit |
| 16 | Feature 069 index row left at `Planned` although both slices are Implemented | `features.md:77`; `features/069.md:106` | Yes — see F3 |

**Independent re-execution performed by this review** (2026-10-25, tree at `41453812`): `--action isomorphism` / `check` / `delegation` / `faces` all exit 0 on the real tree (`stages=8`, `units=78`, `faces=6`, `findings=[]`); the eight new test files re-run `128 passed`; the retained regression log shows `33 failed / 5219 passed` with a byte-identical 33-name set against the frozen baseline (`diff -q` → identical, NEW file 0 lines); the three snapshot evidence logs in `~/tmp/069b-p3-evidence/` reproduce identical before/after node-id sets (`agent` 250 passed both, `cli` 2=2, `function` 12=12, `comm -13` empty).

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 4 (F7, F9, F10, F11) |
| Command Prompt | 2 (F1, F4) |
| Automation / Scripts | 1 (F6) |
| Workflow | 5 (F2, F3, F5, F8, F12) |
| Documentation | 0 |

**P0 validation status**: both P0 findings were validated by direct re-read **and** re-execution in this review session (mutation probe for F1; `git diff` + task-file text for F2). The independent read-only validation subagent step could not be dispatched — no subagent/Agent tool is exposed in this environment — so each P0 row carries `(validated: direct re-read, subagent unavailable)` per the skill's documented fallback.

## 3. Findings (Problems & Improvement Targets)

### F1 — The mapping's “enforcement” is a stage-level proxy: 8/8 passes by construction, and the 24 cells carry no machine-checked meaning

- **Severity**: P0
- **Category**: Command Prompt
- **Location**: `shared/definitions/flow-class-definitions.md:90` (owner legend); `scripts/python/flow-class-check.py:1146,1200-1206` (`check_map`); `shared/workflow/expression-gates.md:32-47` (stage operator table); `verification.md:197`
- **Evidence** (verbatim):

  ```
  # flow-class-definitions.md:90
  `已强制` 表示该行点名的每个 `(阶段, face)` 在该阶段确有 blocking 算子；`已声明未强制` 表示该阶段此刻没有任何 blocking 算子

  # flow-class-check.py:1200-1206
  for face in named:
      if (stage, face) not in blocking_pairs:
          findings.append(iso_finding("annotation-false-enforced", stage, …))

  # expression-gates.md § 阶段算子表 — blocking row counts per stage
  requirements 2 / clarify 2 / plan 2 / tasks 2 / checklist 2 / analyze 2 / implement 1 (+1 advisory) / review 2

  # verification.md:197
  SC-001_value=stages=8 gates=6 findings=0 exit=0; 8/8 rows enforced-and-truthful; …
  ```

  Mutation probe run by this review (copy of the owner + gate owner + roster in `~/tmp/069b-review-probe`, one structure cell replaced with meaningless text — `代码型：随便写点什么凑够八个字 ↔ 文档型：随便写点什么凑够八个字` — grammar preserved):

  ```
  $ python3 scripts/python/flow-class-check.py --action isomorphism --repo ~/tmp/069b-review-probe --format json
  {"action": "isomorphism", …, "stages": 8, "gates": 6, "findings": [], "error": null}
  EXIT=0
  ```

- **Why it's a problem**: FR-002 asks whether a gate **actually executes** the row; the engine only asks whether the named `(stage, face)` has *any* blocking operator. Every one of the eight stages has one, so no row can ever be “not enforced”, `已声明未强制` is unreachable in practice (delivered table: 8 `已强制` / 0 `已声明未强制`), and any row can claim enforcement with any blocking face at its stage. The 24 cells and the four boundary “handling” prose cells are only checked for shape (`↔` present, both sides ≥8 chars; a face id plus ≥4 residual chars). A check that cannot go red when its subject is nonsense proves nothing; `verification.md`’s phrase “enforced-and-truthful” is stronger than what was measured. C-10 does say semantic judgement belongs to the review face — but the requirement (FR-002) was never amended, so requirement and instrument disagree, and SC-001’s “annotation-distortion rows = 0” is a tautology.
- **Proposed fix**: either (a) make the link verifiable — the gate owner must declare, per face, which map rows/artifacts it consumes (e.g. a `consumes` column), and `--action isomorphism` checks that a row’s claimed faces actually list it; or (b) amend FR-002 / C-5 to “structural annotation consistency” and add a review-face criterion with a named judge and a recorded verdict. In both cases, replace the per-stage proxy with per-row enforcement so `已声明未强制` is reachable.
- **(validated: direct re-read, subagent unavailable)** — mutation probe executed against a copy; engine code and gate table re-read.

### F2 — 069b edits the gate owner and a 069a test that its own task file declares off-limits, while the record still claims the only touch was A-1

- **Severity**: P0
- **Category**: Workflow
- **Location**: `tasks.md:69,295,297`; `shared/workflow/expression-gates.md:103,105`; `tests/contract/test_expression_gates_doc.py:487-489`; commits `33c47fd5`, `5d5331b9`
- **Evidence** (verbatim):

  ```
  # tasks.md:69
  - **禁改面**: `templates/commands/`、`skills/`、`shared/workflow/expression-gates.md`（六面与算子表 owner，069a 已交付）、…

  # tasks.md:295
  判据正文只在两个 owner 内（… 与 `shared/workflow/expression-gates.md`）：… `shared/workflow/expression-gates.md` 本切片零改动。

  # tasks.md:297
  069a 的规格与判据正文零改动（唯一触碰是 A-1 允许的 069a 单元测试夹具补一行输入）。

  # commit 5d5331b9 message
  the only edit to a 069a test is the A-1 one-line version declaration in its fixture builder (input only, no assertion changed)

  # git diff --stat f0df3d0b^..HEAD
   shared/workflow/expression-gates.md         | 4 ++--
   tests/contract/test_expression_gates_doc.py | 5 +++--
   tests/unit/test_flow_class_check.py         | 5 +++++
  ```

- **Why it's a problem**: a shared gate owner and a second 069a contract test were changed by a slice whose frozen task file names that file a no-touch surface and asserts the only 069a touch is A-1. The cross-slice change is disclosed only in `verification.md` §跨切片一致性修正 and in commit messages; the tasks/plan record was never amended. A reviewer or a later reconcile that trusts “zero change” will skip re-verification, and a shared owner can be repurposed by any slice as long as the rationale is written afterwards. The test assertion was also changed in the direction of the implementation (`git log -1 --format=%cs` → `--diff-filter=A`), which is exactly the “test follows implementation” pattern Test-First forbids unless explicitly recorded and authorized.
- **Proposed fix**: the implement commit gate should compute the set of paths named in `tasks.md` §禁改面 / `plan.md` §Constraints and fail when such a path is modified without a task row that names it (or without a plan amendment in the same commit). When a cross-slice consistency fix is genuinely in scope (069a C-9 delegates the instrument wording to 069b), add a task row with the owner’s authority and a `[green:]`/evidence pointer instead of a verification-only note.
- **(validated: direct re-read, subagent unavailable)** — `git diff --stat`, the three task-file lines and the test diff were re-read at `41453812`.

### F3 — Feature 069 stays `Planned` although the Pre-Status-Flip Gate's four checks pass and its owner says implement MUST advance

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/memory/features.md:77`; `.specify/memory/features/069.md:96,100,106`; `shared/workflow/feature-integration.md:40-48`; `verification.md:243`
- **Evidence** (verbatim):

  ```
  # features.md:77 (status column)
  | 069 | 执行/表达二元分类与文档型 SDD 同构 | … | Planned | …

  # features/069.md:96 (Canonical Status State Machine)
  | Planned | Implemented | `/speckit.implement` | `tasks.md` has zero `[ ]` rows … AND `verification.md` records a `SC-NNN_status=` row for every Success Criterion …

  # features/069.md:100
  **Critical contract**: … `/speckit.implement` MUST advance `Planned → Implemented` only when the DoD above is satisfied

  # shared/workflow/feature-integration.md:40-48 (owner)
  5. Only if ALL checks pass: advance status

  # verification.md:243 (A-P1)
  状态列保持 `Planned` …… `Implemented` 转移属 `/speckit.implement`／评审 owner，本 run 按派发不进入 review，故按可逆优先停放
  ```

- **Why it's a problem**: the four gate checks all pass (29/29 `[X]`, `deferred_tasks=` empty, five SC rows, zero open tasks), so the owner protocol says advance. A-P1 cites T028’s sentence — but T028 itself says the flip “属 `/speckit.implement`”, and this run **is** the implement closure; the sentence is self-contradictory. The result is an index that understates a fully implemented feature and contradicts its own detail file (“069a Implemented / 069b Implemented”). This is the mirror image of 069a review F10: the missing slice-aware state (REC-069a-09) is still the root cause, and the framework now carries two conflicting statements in one detail file.
- **Proposed fix**: follow the owner gate and flip the row to `Implemented` (2/2), **and** land the slice-aware state (`Implemented k/n` or `Partially Implemented`) so a future two-slice feature has a legal resting state. Remove the “status flip belongs to the review owner” wording from tasks-template-style text; add a contract test that the index status equals the state derived from the detail file’s slice statuses.

### F4 — SC-005’s “criterion text appears zero times outside the owner” is measured over 13 files, not the exclusion-set scope the requirements name

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `requirements.md:240,248`; `contracts/ledger-reconciler.md:143-147`; `verification.md:193,213`
- **Evidence** (verbatim):

  ```
  # requirements.md:248 (SC-005 Source)
  SC-005 Source: 六面门禁 owner 指针表（6 行）+ 对判据正文的 grep 计数，排除集 = 门禁 owner 已声明的 S3 比较集（9 条 owner 路径…）

  # contracts/ledger-reconciler.md:143-147 (C-13)
  SC-005 的「判据正文在 owner 之外出现 0 次」MUST 由既有 … duplicate 面测量 … 主体集 MUST 封闭为 `shared/definitions/flow-class-definitions.md` 与本 spec 的 formal artifacts。

  # verification.md:193
  … 在封闭主体集（13 个文件）上 `faces.duplicate = pass`、`findings = []` …
  ```

- **Why it's a problem**: the requirement reads as near-global (“everything outside the 9 owner paths”), but the contract replaces it with 13 files (owner + spec artifacts). The places where criterion copies are most likely — `templates/commands/**`, `skills/**`, `docs/**` — are neither subject nor comparison side, so the duplicate face cannot see them (`check_duplicates` only compares `subject` records against `subject + owners`). SC-005 is `pass` while a copy in a command template would not be detected. This is 069a F12’s owner↔owner blind spot narrowed one step further, and it is exactly the “measurement scope silently narrowed to what the instrument can pass” failure mode.
- **Proposed fix**: make SC text and contract scope agree — either state the closed subject set in SC-005 itself, or widen the subject set to the same scope `scope_markdown_files()` already defines (`shared/` + `templates/commands/` + `skills/` + the spec) and re-baseline the existing duplicates. Add an analyze check that any SC whose Source says “exclusion set = X” and whose contract says “subject set = Y” is flagged when X ≠ complement(Y).

### F5 — The three migration snapshots prove “adding files does not break product tests”, not that the refreshed payload works

- **Severity**: P1
- **Category**: Workflow
- **Location**: `notes/migration-samples.md:8-12`; `notes/quickstart-run.md:288-292`
- **Evidence** (verbatim):

  ```
  # migration-samples.md:10-12 (suite commands)
  | 1 | xuanji-agent | … | 3f68b62 | master | 195 | 无 | `.venv/bin/python -m pytest tests/ -q` | … |
  | 2 | xuanji-cli | … | a0c476d | xuanji/develop | 548 | 无 | `go test ./...` | … |
  | 3 | xuanji-function | … | a2fad18 | main | 28 | 无 | `.venv/bin/python -m pytest -q` | … |
  ```

- **Why it's a problem**: none of the three commands loads `specify` or anything under `.specify/`; they are product suites. Zero NEW is therefore guaranteed unless merely adding files breaks import collection. The refreshed payload (owner, gates, engine, command copies) is delivered but never executed in the client snapshots, so the migration promise (“升级后既有项目行为不变，且分类数据随既有分发路径到达”) is tested at file-presence level only. The raw logs are retained and symmetric (this review reproduced `250/250`, `2=2`, `12=12`), so the claim is true — it is just not the claim the criterion needs.
- **Proposed fix**: for every migration SC, require at least one post-refresh payload smoke per sample — execute a shipped `.specify` entry point (e.g. `flow-class-check.py --action lookup`, `sync-mirrors.py --check`, or `specify check`) and assert the exit code/label — and record it in the same before/after table. Also state sample representativeness (F12).

### F6 — Two of the three baselines are blind by design: `gate_calls` counts command units while the gates are scripts, and `wall_clock`’s endpoint record was never produced although an analyze round ran

- **Severity**: P1
- **Category**: Automation
- **Location**: `contracts/measurement-instruments.md:33-37`; `notes/expression-baseline.md:29-33,40,55-57`; `tasks.md:97`
- **Evidence** (verbatim):

  ```
  # contracts/measurement-instruments.md:36-37
  脚本级检查（`pre-analyze-check.py` / `validate-requirements.py` / `doc-consistency-check.py` / 测试套件）不是 exec-quant 的 `unit_id`，其调用**不可按次计数**——这是已声明的仪器边界，MUST 在基线记录里写明，MUST NOT 当作 0。

  # expression-baseline.md:40
  → counts.total = 5，全部属其他特性/切片（无 run_id 含 `069b`）→ wall_clock 终点不存在，记 `null` + reason。

  # tasks.md:97
  **2026-10-25 analyze 轮修正（三处…）** …
  ```

- **Why it's a problem**: the quantity named “gate calls” is defined over exec-quant `unit_id`s, but the actual gates are scripts; the contract admits they cannot be counted per invocation. The metric is therefore 0 for every slice regardless of how many gates ran, and the slice freezes it as `not-evaluated` because the denominator is zero — a number that can never become measurable. For `wall_clock`, the endpoint is a `/speckit.analyze` run-determination record; `tasks.md` says an analyze round did run on 2026-10-25, yet `run-determination.py --action history --target /speckit.analyze` has no 069b record. The baseline’s stated reason (“5 records all belong to other features”) is true but omits that the slice’s own analyze activity produced no record. Net: FR-014 is satisfied on paper while the slice’s “measurement instruments” deliverable measures nothing. (069a F8 already reported the same instrument-object mismatch; 069b owned the instrument clause and did not fix it.)
- **Proposed fix**: instrument gate invocations where they happen (one record per script invocation, or have each gate write an exec-quant-shaped record), or redefine the quantity to something the existing channel can observe; make `/speckit.analyze`’s wrap-up always write a run-determination record (or choose an endpoint that exists); add a plan-time “instrument can observe the object” check that must pass before a quantity enters the baseline table.

### F7 — The verification log ships a prose placeholder where the template requires a commit SHA

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/specs/069b-isomorphism-migration-metrics/verification.md:15`; `templates/verification-log-template.md:47`
- **Evidence** (verbatim):

  ```
  # verification.md:15
  post_change_commit=<本文件的引入提交：git log -1 --format=%H -- .specify/specs/069b-isomorphism-migration-metrics/verification.md>

  # templates/verification-log-template.md:47
  post_change_commit=[GIT_SHA_AT_RUN_END]
  ```

- **Why it's a problem**: machine consumers of `post_change_commit` (review/analyze/CI scripts) receive a shell command in a value slot, not a SHA; a schema check would either reject the record or silently skip it. The record otherwise claims to be machine-parseable (`key=value` + per-SC rows).
- **Proposed fix**: fill the SHA at commit time (the commit that lands `verification.md` is knowable after the fact — a follow-up amend or a second write), and add a contract check that every `*_commit=` value matches `^[0-9a-f]{7,40}$` (or `null` with a reason).

### F8 — The frozen snapshot table’s “run prerequisites” were false, and the fixes were appended as post-freeze corrections

- **Severity**: P2
- **Category**: Workflow
- **Location**: `notes/migration-samples.md:10-12,40-68`
- **Evidence** (verbatim):

  ```
  # migration-samples.md:10 (frozen prerequisite)
  `.venv/bin/python` 存在（实测）；套件不依赖未跟踪文件

  # migration-samples.md:40 (post-freeze correction)
  1. **快照不含 `.venv`**：`xuanji-agent` 与 `xuanji-function` 的 `.gitignore` 都把 `.venv/` 排除，`git archive` 不携带它 …
  # migration-samples.md:44
  2. **editable 安装会把源码指向原项目** … 不设 `PYTHONPATH` 时，快照里的测试实际导入**原工作树（含 195 个脏改动）**的源码，快照隔离失效。
  ```

- **Why it's a problem**: a “pre-frozen” sample is meant to fix the measurement before results are seen. Here the sample set (project/HEAD/branch) stayed frozen — good — but three of the four run prerequisites had to be redefined after the first runs (interpreter path, `PYTHONPATH`, `CWS_LIB_PYTHON_HOME`, and folding `ERROR` node ids into the failure set). Before/after are symmetric, so the zero-NEW result still stands (this review verified it from the retained logs), but the freeze covered the sample, not the harness. A reader of the frozen table would run a command that cannot start.
- **Proposed fix**: freeze the runnable command **and** its environment contract (interpreter sourcing, `PYTHONPATH`, node-set extraction including errors), with a smoke run at freeze time; a later correction must be a new dated record that re-baselines both sides before comparison. The template for migration samples should carry an `environment_contract` block, not a one-line “prerequisite”.

### F9 — An open checklist item survives the slice closure with no closing evidence

- **Severity**: P2
- **Category**: Template
- **Location**: `checklists/isomorphism-migration-metrics.md:122`; `.specify/memory/features/069.md:16`
- **Evidence** (verbatim):

  ```
  # checklists/isomorphism-migration-metrics.md:122
  - [ ] CHK025 客户项目那份分类副本的「漂移检查」是否被指定了 owner 与仪器，还是只有框架源 ↔ 镜像的检查？[Gap, Req §FR-008] → disposition: verify-in-implementation: …

  # features/069.md:16
  （36 项 = 35 `[x]` / 1 `[ ]`；唯一 open item = 客户副本漂移检查的 owner，disposition `verify-in-implementation`）
  ```

- **Why it's a problem**: the disposition says “verify in implementation”, but `verification.md` never mentions CHK025; the checklist remains 35/1 while the slice declares itself complete. The open item is a requirements gap (client-copy drift check owner), not an implementation gap — so it should have been escalated or transferred, not left dangling. Nothing in the implement wrap-up reconciles checklist state.
- **Proposed fix**: implement wrap-up must reconcile every checklist `[ ]` whose disposition is `verify-in-implementation` into either closed (with evidence pointer) or transferred (new owner + a register id), and record the reconciliation in `verification.md`; the checklist template should define the two legal terminal forms.

### F10 — SC-004 needs two independent judges; the plan never scheduled them, so the only possible outcome was `unknown`

- **Severity**: P2
- **Category**: Template
- **Location**: `requirements.md:239,247`; `verification.md:191,350`
- **Evidence** (verbatim):

  ```
  # verification.md:191
  SC-004 — 状态 **unknown**。… 两名判定者（不同的人 / 不同的会话 / 判定时互不可见、结论分别落盘后比对）的独立归类演练**本次未执行** …

  # verification.md:350
  - **MEDIUM-1**：SC-004 的人工半（两名互相隔离判定者的独立归类）未执行——单代理收口无第二判定者。解除条件：由第二名判定者在隔离结论后逐条比对 …
  ```

- **Why it's a problem**: the report is honest (`unknown`, not `pass`) — this is a process-strength, not a misreport. But a SC whose execution requires a second human/agent has no execution carrier in `tasks.md` or `quickstart.md`, so a single-agent implement run can never produce it; it will be `unknown` for every slice until someone schedules it. The same shape recurs in `not-evaluated` baselines: criteria are written, obligations are created, and no step owns them.
- **Proposed fix**: at plan time, mark every human-judge or multi-party SC with an explicit execution carrier — a task row that dispatches a second, mutually blind session (the framework already has subagent/agent-team capability), or a `deferred` entry with a named owner and unblock condition. Implement must not close a slice with an `unknown` that has no carrier.

### F11 — The feature index row has become a 3,389-character append-only narrative

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/memory/features.md:77`
- **Evidence** (verbatim, abridged):

  ```
  # features.md:77 — the Last Updated cell (3,389 chars; measured)
  2026-10-24 (slice-aware reconcile: **069a Implemented / 069b unplanned** …); 2026-10-24 (later): slice 069a **implemented** …; 2026-10-25 (later): slice 069b **plan landed** …; 2026-10-25 (later): slice 069b **tasks landed** …; 2026-10-25 (later): slice 069b **checklist landed** …; 2026-10-25 (later): slice 069b **implemented** …
  ```

- **Why it's a problem**: the index is the registry every command and human scans; its `Last Updated` cell now restates what `features/069.md` § Status Tracking already owns, and it grows by one paragraph per command (six appends for this feature). This is a One-Source-Of-Truth violation at the index level and makes the table unreadable for adjacent rows.
- **Proposed fix**: cap the index cell to `YYYY-MM-DD (slice: <id> <state>)` plus a pointer to the detail file; move narrative to the detail file’s Status Tracking (it already exists). Add a length guard / normalization step to `manage-features` that rewrites an over-long cell instead of appending.

### F12 — The migration sample is a convenience sample: three projects, one code group, one author

- **Severity**: P2
- **Category**: Workflow
- **Location**: `notes/migration-samples.md:10-12`
- **Evidence** (verbatim):

  ```
  | 1 | xuanji-agent | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent` | …
  | 2 | xuanji-cli   | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-cli`   | …
  | 3 | xuanji-function | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-function` | …
  ```

- **Why it's a problem**: SC-002 speaks about “既有客户项目” generally; the frozen set is three repositories from a single code group, all maintained by the same owner, with two language families (Python/Go). The result is valid for those three and says nothing about a Java/Maven client, a Windows checkout, or a project with a different `.specify` history. Sample selection is a criterion the slice owns, and no representativeness dimension is recorded.
- **Proposed fix**: record the dimensions that matter (org, language/toolchain, `.specify` age, OS) in the freeze table and require at least one sample outside the author’s group for any migration/compatibility SC. Better: derive the sample from the framework’s own installed-project inventory rather than from the author’s working set.

## 4. What Worked — Preserve (Brief)

- **Red-first evidence with full transcripts**: R1–R9 red runs and G1–G6 green runs carry command, real output and exit code; the eight new test files re-run `128 passed` here. Red forms are “action/section missing”, not collection errors.
- **Name-level baselines, independently reproduced**: the retained logs show `33 failed / 5219 passed`, and the 33-name set is byte-identical to `notes/test-baseline-contract.txt` (`diff -q` identical; NEW list 0 lines). Counts are never used as the criterion.
- **Anti-vacuous reconciliation**: `coverage` prints `matched`/`inventory_units` beside the empty set; the floor is derived (`⌊(27+51)/2⌋ = 39`) and the 77-row injection stays `gap` while the 0-row injection becomes `parse-failure` — the two reds are genuinely distinguishable and were re-verified by the test suite.
- **Honest degradation states**: payload roots get `framework-source-required` at exit 2 (re-verified for all four actions) instead of a false green; `not-evaluated` is kept out of the SC status column; SC-004 is `unknown` rather than claimed.
- **Constrained edit surface**: 27 command templates untouched (`regen-command-copies.py --check` OK), mirrors byte-identical, 51 clauses claimed by 29 task rows, `FR universe 14 / claimed 14`.
- **Scope discipline at the boundary**: no new command, no new gate face, no project-side store, no new collector — all four independently observable.
- **The 069a→069b handoff closed its main pointer**: `grep -c '069b 承接' shared/definitions/flow-class-definitions.md` → 0; the map and boundary now live in the unique owner.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-069b-01 — Success Criteria need a falsifier, not only a measurement source** — Target: `templates/requirements-template.md` § Success Criteria & Measurement Sources. Change: require each SC row to name at least one *mutation* that must turn it red (e.g. “replace a map cell with nonsense → check must fail”), and have `/speckit.analyze` reject an SC whose falsifier is absent. Source: F1. Expected impact: an SC whose instrument is a stage-level proxy cannot be written without the author noticing that the mutation would not fire.
- **REC-069b-02 — Verification log values must be machine-shaped** — Target: `templates/verification-log-template.md`. Change: define the `*_commit=` value domain (`^[0-9a-f]{7,40}$` or `null` + reason) and add the check to the implement completion gate. Source: F7. Expected impact: downstream consumers stop parsing prose in a SHA slot.
- **REC-069b-03 — Feature index `Last Updated` is a pointer, not a log** — Target: `templates/feature-index-template.md` + `skills/internal/manage-features/SKILL.md`. Change: cap the cell to `date (slice: id state)` + detail-file pointer; have `manage-features` rewrite over-long cells during reconcile. Source: F11. Expected impact: the index stays scannable and stops duplicating the detail file.
- **REC-069b-04 — Human-judge / multi-party SCs need an execution carrier** — Target: `templates/requirements-template.md` + `templates/tasks-template.md`. Change: a SC whose measurement requires a second isolated judge MUST carry a task row that dispatches it (subagent/team), or a `deferred` entry with owner and unblock condition; implement may not close with an unowned `unknown`. Source: F10. Expected impact: independent-replication criteria become deliverable instead of permanently `unknown`.

### 5.2 Command Prompt Improvements

- **REC-069b-05 — “Off-limits” surfaces must be diff-checked at the commit gate** — Target: `templates/commands/implement.md` + `skills/internal/implement-feature/SKILL.md` (commit gate and Pre-Status-Flip Gate). Change: parse the plan/tasks no-touch list and fail the commit when one of those paths changed without a task row naming it in the same commit; a legitimate cross-slice fix must add a task row (or amend the plan) rather than live only in a verification section. Source: F2. Expected impact: the process record and the tree cannot disagree.
- **REC-069b-06 — Measurement scope must not be narrowed between SC and contract** — Target: `templates/commands/plan.md` + `templates/commands/analyze.md`. Change: when a plan/contract defines an SC’s instrument, require the SC’s own Source text to be updated to the same closed subject set; `/speckit.analyze` flags any SC whose “exclusion set” and its contract’s “subject set” are not complements. Source: F4. Expected impact: a criterion cannot be silently shrunk to what the instrument already passes.
- **REC-069b-07 — Status flip follows the owner protocol, not task prose** — Target: `templates/commands/implement.md` + `templates/commands/tasks.md` (avoid writing “status flip belongs to another owner” into a task row). Change: the flip is performed by implement when the Pre-Status-Flip Gate passes; task rows must not contradict `shared/workflow/feature-integration.md`. Source: F3. Expected impact: the index cannot stay `Planned` after a DoD-satisfying implement run.

### 5.3 Automation / Script Improvements

- **REC-069b-08 — Instrument-object fit is a plan-time gate** — Target: `shared/workflow/expression-gates.md` § 三项基线 + `templates/commands/plan.md`. Change: before a quantity enters a baseline table, prove one real observation from the chosen channel (not `0`, not `null`); if the object is a script invocation the channel cannot see, either instrument the call site or drop the quantity. Also make `/speckit.analyze`’s wrap-up emit a run-determination record so `wall_clock` has an endpoint. Source: F6. Expected impact: efficiency baselines become measurable rather than structurally zero.

### 5.4 Workflow Improvements

- **REC-069b-09 — Migration samples must exercise the refreshed payload** — Target: the migration-sample section of `templates/commands/implement.md` / `templates/verification-log-template.md`. Change: every compatibility SC requires at least one post-refresh smoke that executes a shipped `.specify` entry point in the snapshot, recorded beside the before/after node-id sets; also record sample representativeness dimensions and require one sample outside the author’s group. Source: F5, F12. Expected impact: “refresh did not change behaviour” is tested, not inferred from file presence.
- **REC-069b-10 — Freeze the harness, not only the sample** — Target: migration/sample record shape (same owner as REC-069b-09). Change: freeze interpreter sourcing, `PYTHONPATH`, environment variables and the node-set extraction (including whether `ERROR` counts) together with the sample; require a smoke run at freeze time; a later correction re-baselines both sides as a new dated record. Source: F8. Expected impact: a “pre-frozen” sample can actually be executed by the next reader.
- **REC-069b-11 — Checklist closure reconciles dispositions** — Target: `templates/checklist-template.md` + `skills/internal/implement-feature/SKILL.md` (wrap-up). Change: every `[ ]` with `verify-in-implementation` must be closed with evidence or transferred to a named owner + register id at wrap-up; the closure summary is derived from the markers. Source: F9. Expected impact: a slice cannot declare completion while an owned-but-unclosed requirement gap remains invisible.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-069b-01 Success Criteria need a falsifier | `templates/requirements-template.md`, `templates/commands/analyze.md` | F1 |
| P0 | REC-069b-05 Off-limits surfaces diff-checked at commit | `templates/commands/implement.md`, `skills/internal/implement-feature/SKILL.md` | F2 |
| P1 | REC-069b-07 Status flip follows the owner protocol | `templates/commands/implement.md`, `templates/commands/tasks.md`, `shared/workflow/feature-integration.md` | F3 |
| P1 | REC-069b-06 Measurement scope coherence | `templates/commands/plan.md`, `templates/commands/analyze.md` | F4 |
| P1 | REC-069b-09 Migration samples exercise the payload | migration-sample section of implement / verification template | F5, F12 |
| P1 | REC-069b-08 Instrument-object fit gate | `shared/workflow/expression-gates.md` § 三项基线, `templates/commands/plan.md` | F6 |
| P2 | REC-069b-02 Verification log value domain | `templates/verification-log-template.md` | F7 |
| P2 | REC-069b-10 Freeze the harness, not only the sample | migration/sample record shape | F8 |
| P2 | REC-069b-11 Checklist closure reconciliation | `templates/checklist-template.md`, implement-feature wrap-up | F9 |
| P2 | REC-069b-04 Human-judge SC execution carrier | `templates/requirements-template.md`, `templates/tasks-template.md` | F10 |
| P2 | REC-069b-03 Feature index cell is a pointer | `templates/feature-index-template.md`, `skills/internal/manage-features/SKILL.md` | F11 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (All targets resolve inside this repository; no external target is proposed.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says “see attached”, “as discussed earlier”, or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report. (The only bracketed upper-case token is `[GIT_SHA_AT_RUN_END]` inside the verbatim template quote in F7 — it is the quoted defect, not an unfilled report placeholder.)
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: two P0 findings, both `(validated: direct re-read, subagent unavailable)` — the independent read-only subagent step could not be dispatched (no subagent/Agent tool in this environment); each was re-verified by re-reading the exact lines and, for F1, by executing a mutation probe against a copy of the owner/gate/roster tree.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
