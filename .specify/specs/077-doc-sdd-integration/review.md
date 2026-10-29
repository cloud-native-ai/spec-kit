# Specification-Driven Development (SDD) Process Review Report: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 077 |
| Requirement Key | `077-doc-sdd-integration` |
| Requirement Name | 项目文档的 SDD 接入（特性级类别与文档型阶段门禁） |
| Related Feature | 077 项目文档的 SDD 接入（特性级类别与文档型阶段门禁） |
| Repository | `spec-kit` (repo root `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`) |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (remote name `gitlab`; SSH-only, so `blob/` URLs cannot be rendered for this remote) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the whole feature line is unpushed. Every citation below uses absolute paths plus `git show <sha>:<path>` recovery. |
| Branch | `077-doc-sdd-integration` |
| Commit SHA | `794a7f2b285289e125da514f84b18f40835fb52f` (short: `794a7f2b`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-30 |
| Reviewer (Agent) | Qoder agent — `review-sdd-process` segment then `code-review` segment (`/speckit.review` composition) |
| Environment | macOS 26.6.2 (arm64); system `Python 3.14.6`; pytest `9.1.1` via `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` (the repo's own `.venv` has no pytest); `git 2.54.0`; `git-delta` **not installed** → code segment ran in `renderer: text` mode |
| spec-kit Source Snapshot | local framework repo @ `794a7f2b` (`.specify/source.json` records commit `c7082866…`, `stamped_at 20261021T172020Z`) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| `requirements.md` | 263 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/requirements.md` | 25 FR / 8 SC / 4 US / 6 STR / 9 排除项 / 11 假设；含 clarify 八条裁定与 analyze 修复轮裁决小节 |
| `plan.md` | 255 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/plan.md` | 18 行宪法检查 + 3 条 DTR + 三轮 Plan Edits 登记 |
| `tasks.md` | 344 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/tasks.md` | 28 任务（T001–T028）、77 条款由 19 行 `[green:]` 认领、7 条 Completion Gate |
| `research.md` | 246 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/research.md` | R-1…R-13；R-9 是接线子节标题字面量与剥离算法的登记处 |
| `data-model.md` | 248 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/data-model.md` | E1–E9 + 9 行校验规则汇总 |
| `contracts/` (6 files) | 422 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/contracts/` | 77 条款，全部 `md-bold-closed` |
| `quickstart.md` | 171 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/quickstart.md` | S1–S7 场景，每条带实施前实测与实施后期望 |
| `verification.md` | 112 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/verification.md` | 8 条 SC 状态行 + 6 份证据路径与 sha256 |
| `feature-ref.md` | 65 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/feature-ref.md` | 25 FR → 设计落点、8 SC → 证据来源 |
| `checklists/readiness-2026-10-30.md` | 269 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md` | 40 项（21 pass / 19 fail）+ 修复轮处置表 29 行 |
| `checklists/requirements.md` | 45 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/checklists/requirements.md` | requirements 阶段质量清单（17 项） |
| `notes/red-first-evidence.md` | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/notes/red-first-evidence.md` | 五个红先行文件的重放命令 / 真实输出 / 退出码 / 失败计数 |
| `test-evidence/` (78 files) | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/test-evidence/` | 每阶段确定性门与定向测试的逐字转录 |
| State spine | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/state/077-doc-sdd-integration.md` | 阶段记录、analyze 三轮、两槽位预算（只读，本 run 未写） |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | U0/U1 入口声明与断点探测 | `.specify/state/077-doc-sdd-integration.md` § U0/§ U1（深链见上表；断点 = requirements） | none |
| 2 | `/speckit.requirements` | `63848d3b`（spec + 清单 + 证据 + 注册）、`481242b5`（STR id 引用、登记前行数） | none; 派发文本「六个模板」与枚举七个不一致，以枚举为准并登记为偏差 A3 |
| 3 | `/speckit.clarify` | `5f88e3b5`；八条裁定，其中接线面「七个」被二次复核后不改判 | none |
| 4 | `/speckit.plan` | `159aa940`；plan + research + data-model + 6 契约 + quickstart + feature-ref + 13 份证据 | none; 规划期发现「七模板接线必然打破 069a 闭合集守卫」并登记连带义务 |
| 5 | `/speckit.tasks` | `ab288aab`（tasks + 77 条款分区 + `coverage-baseline.txt` 冻结）、`45b6b732`（wrap-up） | none |
| 6 | `/speckit.checklist` | `d05d3bef`；40 项 21 pass / 19 fail | none |
| 7 | `/speckit.analyze` #1 → 修复 | `6217a86f`；14 HIGH / 9 MEDIUM / 6 LOW → 29/29 处置 | none |
| 8 | `/speckit.analyze` #2 → 修复 | `0c8f95d3`；1 HIGH / 6 MEDIUM / 5 LOW → 12/12 处置 | none |
| 9 | `/speckit.analyze` #3 → 修复 | analyze #3 报告 0 CRITICAL / 0 HIGH，`f7ec22c5` 处理 13 项（F-01…F-10 / C-02 / E-02 / B-01） | **部分偏离**：第 3 轮只在 commit message 与 `plan.md` § 修复轮 3（plan 属主子集）留处置，未进清单的处置表（见 F3） |
| 10 | `/speckit.implement` 分段 P1–P4 | `29b515b4` / `a401db98` / `0fb8a2bf`+`f5835e0e` / `0abf94c3`，每段后一个 `chore(...): record … checkpoint` | none; 分段与 U0 声明的四段一致 |
| 11 | implement 期发现 quickstart S2 前提不成立 | `quickstart.md:68` 写「`--repo` 接受任意目录作为仓库根」，`test-evidence/tasks-quickstart-s1-s7.txt:4-7` 自述「S2 snippet as written … degrades to owner-unavailable for all three fixtures」，改用 S2b 补夹具 | **偏离**：DoD-9 的 `PLAN-EDIT … 分类=minor` 通道可用但未用（见 F2） |
| 12 | implement 收尾 | `794a7f2b`（wrap-up）；28/28 任务闭合，0 `[~]` | none |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 1 |
| Documentation | 3 |

No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c1cd46002db62a1565c4ab0a23178e9fe7f149ef` | the resolved diff base (`base` step, `base_source=feature-first-commit`) |
| Head commit | `794a7f2b285289e125da514f84b18f40835fb52f` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | `git-delta` is not installed in this environment (`which delta` → not found); the two-condition rule puts the run in text mode |
| Changed / judged / skipped / gap files | 177 / 23 / 154 / 0 | copied field by field from the coverage receipt block |
| Segment verdict | `not-evaluated` | the receipt's own derivation: `skipped_files > 0` ⇒ skip counts no coverage credit, so the four-value set lands on `not-evaluated`, not `pass` |
| Gate verdict | `allow` (script: `gate=allow`, `blocking_entries=0`) | `report --summary --file …/code-review.md`, exit 0 |
| Reason, when one applies | triage was `run` and all 23 source files of the delivery surface were read; the 154 skipped carry legal reasons — 28 per-tool command copies + 9 `.specify/` mirrors with reason `generated` (their equivalence is machine-proved: `regen-command-copies.py --check` → `OK`, `sync-mirrors.py --check` → six pairs `ok`), and 117 spec artifacts / evidence transcripts with reason `non-code-file` (judged by this report's process segment, not by the code segment). No judgement was issued over the skipped files. | the receipt block in the record |
| Uncommitted scope | none at receipt time — the working tree was clean when the range was resolved; this run's own two records are outputs, not review object | `git status --short` before the run |
| Record | `.specify/specs/077-doc-sdd-integration/code-review.md` | written this run |
| Archive | `none` | first run for this feature |

The findings themselves live in `.specify/specs/077-doc-sdd-integration/code-review.md` and are read there: 6-level counts `blocking 0 / important 3 / suggestion 4 / nitpick 2 / question 1 / praise 2`.

## 3. Findings (Problems & Improvement Targets)

### F1 — 四条 SC 的 `partial` 全部指向同一条不存在的证据线：仓库里没有任何表达类特性线，特性自己又声明为执行类

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/077-doc-sdd-integration/verification.md`（absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/verification.md`）§ Success Criteria evaluation，行 77–103；`.specify/specs/077-doc-sdd-integration/requirements.md:51`（A6）；`.specify/specs/077-doc-sdd-integration/requirements.md:110`（US4）
- **Evidence** (verbatim quote):

  ```
  SC-003_status=partial
  SC-003_value=… "Seven stages each emit ≥1 blocking operator row on one expression fixture line": **not produced by a live line**

  SC-008_value=… the "expression pilot line ran all eight stages, analyze and review once each (2/2), 0 skipped or shortened stages" measurement: **not run** (this repository has no expression-class line to pilot)
  ```

  ```
  - **A6（本特性自身按判据属 execution）**：本特性交付命令模板、驱动技能、owner 文档与确定性检查器，缺陷最先以「阶段命令不读类别」「驱动放行了缺证据的阶段」这类行为差异暴露，按 069 判据为 `execution`；本特性不替自己主张表达类，也不因此获得任何门禁豁免。
  ```

- **Why it's a problem**: the four `partial` rows are honest — each says exactly what was and was not measured — but they are all the *same* missing artifact: an expression-class line. SC-003 (per-stage blocking operator coverage) and SC-008 (eight-stage pilot with analyze/review at 100%) are the two Success Criteria that would prove the feature's central promise (US4: `sdd-loop-driver` can drive a document-class line unattended), and neither has ever been observed. The self-declaration `execution` compounds it: the new document gates never run on the only line that exists in this repo, so the shipping state is "mechanism implemented, never executed end to end". Verdict `partial` is legal, so this is not a DoD violation — it is a delivery-risk finding: the first real document-class line becomes the first test.
- **Proposed fix**: before declaring the feature complete, add one throwaway expression-class spec line (class `expression`, a `## Document Structure` plan, one delivered document) and run the seven stages once with U4 checking them; record the eight stage rows and the analyze/review pair in `verification.md`. If that is out of scope for this run, record an explicit carry-over with an owner and a date in `features/077.md` § Future Evolution Suggestions, and keep SC-003/SC-008 at `partial` — never at `pass`.

### F2 — `quickstart.md` S2 交付了一条已知跑不通的命令，而 DoD-9 的 `PLAN-EDIT` 通道原地未用

- **Severity**: P1
- **Category**: Documentation
- **Location**: `.specify/specs/077-doc-sdd-integration/quickstart.md:68`（absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/quickstart.md`）与 `:59-62` 的「实施后期望」；`.specify/specs/077-doc-sdd-integration/test-evidence/tasks-quickstart-s1-s7.txt:4-7`
- **Evidence** (verbatim quote):

  ```
  **Premises**：`--repo` 接受任意目录作为仓库根；三份夹具的 `requirements.md` 只需头部区即可解析；
  ```

  ```
  # S2b exists because the S2 snippet as written points --repo at a bare temp tree; the engine
  # resolves its class owner under that root, so the bare form degrades to owner-unavailable for
  # all three fixtures (recorded below unchanged). S2b completes the fixture the way the pinned
  # unit test does (owner doc present) — that is the form "三例各答不同" is about.
  ```

- **Why it's a problem**: the quickstart is the artifact a future implementer follows to reproduce the feature. Its S2 snippet sets `--repo "$TMP"` over a bare temp tree, and the engine resolves the class owner (`shared/definitions/flow-class-definitions.md`) under that root — so all three fixtures answer `owner-unavailable` / exit 2, i.e. exactly the "three identical answers" the scenario exists to disprove. The implement run diagnosed this correctly and ran S2b instead, but left `quickstart.md` unchanged and cited "plan-owned" as the reason. DoD-9 in `tasks.md` provides the exit (`PLAN-EDIT: <path> — <reason>；分类=minor|substantive`) and a quickstart command fix is squarely `minor`; the protocol was available and not used, so the shipped document now teaches a command it knows fails.
- **Proposed fix**: apply a `PLAN-EDIT … 分类=minor` to `quickstart.md` S2 — either copy the owner document into `$TMP/shared/definitions/` before the loop (the S2b form) or drop `--repo "$TMP"` and place the fixtures under the repo's `.specify/specs/` with cleanup — then update the `Premises` line to match. Re-run S2 and replace the transcript in `test-evidence/`.

### F3 — analyze #3 的 13 项在仓内没有处置记录；处置表自称的「29 行 / 未关闭项：无」只覆盖前两轮

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md:230-232`、`:268`（absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md`）；`.specify/specs/077-doc-sdd-integration/plan.md:244-246`；commit `f7ec22c5` message
- **Evidence** (verbatim quote):

  ```
  > 全部由 `/speckit.analyze` 修复轮关闭；`/speckit.analyze` 的 29 条发现（14 HIGH / 9 MEDIUM / 6 LOW）逐条对应下表。
  > **第二轮 analyze（HEAD `6217a86f`，判 BLOCKED）**：1 HIGH（R-01）+ 6 MEDIUM（R-02…R-07）+ 5 LOW（首轮 14 HIGH 已全关闭）。
  ```

  ```
  **未在任何行关闭的项**：无。**清单判定的保留**：上文的 21/19 判定仍是那个时点的实测结论，不回填为 pass——
  ```

  ```
  ### 修复轮 3（minor，analyze #3，2026-10-30）
  *第三轮 `/speckit.analyze`（0 CRITICAL / 0 HIGH）留下的 3 MEDIUM + 10 LOW 中，凡落在 plan 属主制品的条目在此登记。*
  ```

- **Why it's a problem**: the table's closing line "未在任何行关闭的项：无" is scoped to two rounds (rows 1–29 = 19 checklist items + 10 analyze-#2 rows), but it reads as covering the whole analyze history, and the header still says "29 条发现". Round 3's thirteen items exist only in a commit message and in the plan-owned subset of `plan.md`; the non-plan ones (requirements SC-003/FR-020/FR-024, tasks T013/T016/T019, quickstart S2) are named in `plan.md` prose but have no row of their own. A reader cannot answer "was analyze #3 closed?" from the checklist, which is the artifact that exists to answer exactly that.
- **Proposed fix**: extend the disposition table with a `第 30–42 行` block (13 rows, one per round-3 item, each naming its landing file), and change the closing sentence to state its scope explicitly ("本节覆盖 analyze #1–#3；第 1–29 行 = 前两轮，第 30–42 行 = 第三轮").

### F4 — 同一事实三处记录两个数：analyze #3 的 MEDIUM 计数 5 与 3 不一致

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/state/077-doc-sdd-integration.md:118`（absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/state/077-doc-sdd-integration.md`）；`.specify/specs/077-doc-sdd-integration/plan.md:246`；commit `f7ec22c5` message
- **Evidence** (verbatim quote):

  ```
  - analyze #3（`0c8f95d3`）：**0 CRITICAL / 0 HIGH** / 5 MEDIUM / 10 LOW → 放行 implement；实现前提醒 F-01/F-02/F-03 由 `f7ec22c5` 微修（13/13，记录形态，计数不变）
  ```

  ```
  *第三轮 `/speckit.analyze`（0 CRITICAL / 0 HIGH）留下的 3 MEDIUM + 10 LOW 中，凡落在 plan 属主制品的条目在此登记。*
  ```

  ```
  analyze #3 cleared the line (0 CRITICAL / 0 HIGH) but left three MEDIUMs that
  implement would have read two ways, plus ten LOWs. All thirteen are spec-only
  ```

- **Why it's a problem**: 3 MEDIUM + 10 LOW = 13 matches the fix commit's item count (F-01…F-10 = 10 LOW, F-01/F-02/F-03 = 3 MEDIUM); the spine's "5 MEDIUM" is the outlier. The spine is the artifact a re-entering driver reads first, so the wrong number is the one most likely to be cited later. This is the same drift class analyze #2 closed as R-07.2 ("派生计数不落登记面") — it recurred in round 3.
- **Proposed fix**: correct the spine line to `3 MEDIUM / 10 LOW`, or, if 5 was right, say which two of the five were non-spec; then apply the R-07.2 rule to round 3: record the count once (in the disposition table) and let every other surface point at it.

### F5 — 特征登记面记「analyze 两轮」，第三轮从登记面消失

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/memory/features.md:86`（absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features.md`）
- **Evidence** (verbatim quote):

  ```
  **analyze 两轮**（第一轮 14 HIGH 修复于 `6217a86f`；第二轮 1 HIGH + 6 MEDIUM + 5 LOW 已按 spec-only 修复并入本行与详情，状态保持 `Planned`）
  ```

- **Why it's a problem**: the spine records three analyze runs and the fix commit `f7ec22c5` exists and is cited nowhere on the registration surface. The index row is the single place another feature or a house-keeping pass reads this feature's history; a round that is absent there is a round that, one compaction later, never happened.
- **Proposed fix**: change the clause to `analyze 三轮（14 HIGH → 6217a86f；1 HIGH + 6 MEDIUM + 5 LOW → 0c8f95d3；0 HIGH / 3 MEDIUM + 10 LOW → f7ec22c5）` and mirror the same sentence into `features/077.md` § Latest Review.

### F6 — 框架级字面量的「唯一登记处」落在特性私有的规格里

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/specs/077-doc-sdd-integration/research.md:150-153`（R-9）；`.specify/specs/077-doc-sdd-integration/requirements.md:228-236`（§ Shared Strings）；消费方 `templates/commands/{requirements,clarify,plan,tasks,checklist,analyze,implement}.md` 与 `templates/plan-template.md:179`
- **Evidence** (verbatim quote):

  ```
  ## R-9 execution 零变化的反向守卫：剥离子节后与基线提交逐字相同（标题字面量与剥离算法的唯一登记处）

  - **子节标题字面量（唯一登记处 = 本节）**：`### 类别读取与文档型门禁`——逐字、无后缀、无变体。
    …
    登记处选在本节而不是 requirements § Shared Strings，
    是为了不改变该表的行数（6 行）：本字面量的消费者只有 stage-wiring 契约与两个测试文件，不是跨规格共享词汇。
  ```

  ```
  **编号范围说明**：本表编号**只在本规格内解析**，新登记的四行接续编为 `STR-003`…`STR-006`。069 已在其 § Shared Strings 占用 `STR-003`（`flow_class`）与 `STR-004`（默认标记字面量）…
  ```

- **Why it's a problem**: both literals are now consumed by *framework-distributed* files (`templates/commands/*.md` ships with `specify init`; `templates/plan-template.md` likewise), yet their owner is a dated artifact of one feature. A maintainer changing the card heading must edit `077/research.md`; the test `wiring_heading()` reads the literal *from that spec file*, so the guard itself breaks the day the spec is archived or compacted. The requirements-side choice shows the cost already: 077 had to spend five lines explaining that its own `[[STR-003]]` collides with 069's `[[STR-003]]`.
- **Proposed fix**: promote the five literals (`### 类别读取与文档型门禁` + `[[STR-002]]`…`[[STR-006]]`) to a framework owner — the simplest is to declare `scripts/python/doc-consistency-check.py`'s constants the code-first owner for all five (it already owns the three column sets) and have `templates/plan-template.md` and the seven command templates cite them; the spec keeps only its as-of measurement.

## 4. What Worked — Preserve (Brief)

- **Per-stage commit + wrap-up chain**: every stage ends with its own `chore(...): record … wrap-up` commit (`038f614f`, `937c06bf`, `06c31b1d`, `45b6b732`, `378d7702`, `794a7f2b`), so the timeline in §1 is reconstructable from git without inference and no commit mixes two stages.
- **Red-first records with four fields and an explicit "which greens are only regression guards" line** (`notes/red-first-evidence.md` § T002: "16 项已绿的是格式拒绝与降级形态的回归守卫…不是本特性已实现的证明") — this is what keeps a red-first claim from being read as a green claim.
- **Evidence hashes are real**: all six `evidence_sha256` values in `verification.md` were recomputed for this report and matched byte for byte (`shasum -a 256` on `tasks-quickstart-s1-s7.txt` → `336a2f2d…`, `tasks-distribution-two-state.txt` → `a477bce1…`, `tasks-closing-suites.txt` → `525131a6…`, `tasks-plan-template-skeleton.txt` → `57e04e21…`, `tasks-scope-set-difference.txt` → `61dee41b…`, `tasks-stage-integrity.txt` → `2ab40493…`).
- **The checklist kept its own verdict**: the 21/19 result stays as the dated reading and the fix rounds append dispositions instead of back-filling `pass` (`checklists/readiness-2026-10-30.md:268`).
- **A negative control on the analyze channel**: analyze #2's R-01 was caught because the record carries an arithmetic self-check (`test-evidence/r01-na-arithmetic-fix2.txt`) rather than a prose claim.
- **Disclosure discipline on a pre-existing red**: `verification.md:112` names `tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` as one of the 39 baseline failures and refuses to mask it.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC_T1 — 让框架级字面量的 owner 落在框架文件里** — Target: `templates/plan-template.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/plan-template.md`）与 `templates/commands/*.md`. Change: 把 `### 类别读取与文档型门禁` 等五个字面量的 owner 从特性规格移到 `scripts/python/doc-consistency-check.py` 的常量，模板只引用常量名；`research.md` R-9 与 requirements § Shared Strings 降级为带日期的测量记录。Source: F6. Expected impact: 下游项目改一次字面量只改一处；特性规格归档后守卫不再断链。

### 5.3 Automation / Script Improvements

- **REC_A1 — analyze 处置表覆盖全部轮次，且轮次边界写在标题里** — Target: `skills/internal/create-checklist/SKILL.md`（或该技能引用的 checklist 模板）与 `.specify/specs/*/checklists/` 的处置表形态. Change: 处置表的分节标题带轮次区间（"第 1–29 行 = analyze #1–#2；第 30–42 行 = analyze #3"），并要求每轮 analyze 的每条发现恰好一行；收尾句显式声明覆盖范围。Source: F3. Expected impact: "这一轮关了没有" 可从一个文件回答，不必回到 commit message。

### 5.4 Workflow Improvements

- **REC_W1 — 交付前必须有一条真实表达类线跑过一次，或写明带日期的交接** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` § Independent Verification 与 `skills/internal/implement-feature/SKILL.md` 的 closure 段. Change: 当特性交付"类别感知"这类**改变门禁集**的能力时，closure 增加一条前置：至少一条真实（或一次性夹具）目标类的线跑过全部阶段，并在 `verification.md` 留八行阶段记录；做不到时在 `features/<ID>.md` § Future Evolution Suggestions 记 owner + 日期，且相关 SC 保持 `partial`。Source: F1. Expected impact: 首个真实用户不再是首次执行者。
- **REC_W2 — 已知跑不通的文档片段必须就地修，不能只写进 evidence** — Target: `skills/internal/create-tasks/SKILL.md` 的 DoD-9（PLAN-EDIT 协议）与 `templates/commands/implement.md` 的偏差条款. Change: 把"运行期发现某 plan-owned 文档有一条**读者会照抄的无效果命令**"列为 `分类=minor` 的**必须** PLAN-EDIT（而非可选），因为读者成本落在下游。Source: F2. Expected impact: quickstart / 指南类 artifact 不会带着已知失效指令出库。

### 5.5 Documentation Improvements

- **REC_D1 — 派生计数只在一处落值** — Target: `.specify/specs/*/checklists/readiness-*.md` 的处置表 + 状态脊阶段记录. Change: analyze 每轮的严重度计数只在处置表出现；状态脊与 `features.md` 只写指针（"见处置表第 N 行"）。Source: F4, F5. Expected impact: 同一个数字不会三处两个值。
- **REC_D2 — 登记面必须与本特性的全部阶段轮次对齐** — Target: `.specify/memory/features.md` 的 feature 行与 `features/<ID>.md` § Latest Review. Change: `/speckit.implement` 收尾时用一条脚本从状态脊的 `### analyze` 段生成该行文字，而不是手写。Source: F5. Expected impact: 第三轮 analyze 这类"发生在 implement 之前、却要在 implement 收尾才登记"的事件不再漏记。

（`### 5.2 Command Prompt Improvements` 无推荐项，按模板要求不保留空标题。）

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC_W1 — 交付前一条真实表达类线跑过一次，或带日期交接 | `skills/external/sdd-loop-driver/references/stage-prompts.md`、`skills/internal/implement-feature/SKILL.md` | F1 |
| P1 | REC_W2 — 已知无效的文档指令必须就地 PLAN-EDIT | `skills/internal/create-tasks/SKILL.md`（DoD-9）、`templates/commands/implement.md` | F2 |
| P2 | REC_T1 — 框架字面量的 owner 归框架文件 | `templates/plan-template.md`、`scripts/python/doc-consistency-check.py` | F6 |
| P2 | REC_A1 — analyze 处置表覆盖全部轮次并标轮次区间 | checklist 技能与 `checklists/` 形态 | F3 |
| P2 | REC_D1 — 派生计数只在一处落值 | 状态脊 / `features.md` / 处置表 | F4, F5 |
| P2 | REC_D2 — 登记面与全部阶段轮次对齐 | `features.md`、`features/<ID>.md` | F5 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Post-review Fix

The two P1s and the three `important` entries were closed by the driver after this review
run, in one review-fix commit:

- **P1-a** — a real expression-class pilot line now exists:
  `tests/integration/test_expression_line_pilot.py` + `tests/fixtures/expression_line/`
  (12 passed). It runs the eight stage operators for real against a synthetic fixture
  (gate-level execution, labelled as such, never presented as a customer line).
  `verification.md` was updated from its results: **SC-003 → `pass`**; SC-002 / SC-005 /
  SC-008 stay `partial` with narrowed, named gaps (no real expression-class stage chain
  in this repo).
- **P1-b** — `quickstart.md` S2 was rewritten to the runnable form (owner documents in the
  fixture), recorded as `PLAN-EDIT: quickstart.md — minor`.
- **important-1/2** — a missing `spec:` input now returns exit 2 with the
  `owner-unavailable` label and `flow_class: null` (no class value), aligning the engine
  with C-003/C-007 and the payload `error` domain; `test_flow_class_spec_key.py` carries
  the assertion.
- **important-3** — the `## Document Structure` skeleton in `templates/plan-template.md`
  now carries downstream-parsable literal headings plus an owner pointer, not per-spec
  `[[STR-NNN]]` tokens.
- **Author responses** for all three `important` entries are appended to `code-review.md`.

Re-measured after the fix: seven gates exit 0; 218 touched/neighbour tests passed; the
status-gate conditions are unchanged (0 open tasks, review evidence present, **0
`blocking`**), so the Feature stays at `Ready for Review`.

## 9. Feedback

Please share the contents of this document with the spec-kit framework developers.
