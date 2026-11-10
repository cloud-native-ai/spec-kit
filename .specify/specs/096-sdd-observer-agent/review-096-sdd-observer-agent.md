# Specification-Driven Development (SDD) Process Review Report: SDD 专用观察者与线级观察记录（sdd-observer）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

- **Review run**: `/speckit.review` — 过程 → 产物 → 实现 → 代码四段固定顺序 + Acceptance Reality Check（非第五段）。
- **Judgement**: `Implemented → Ready for Review` = **refused**（不是合法的可执行翻转）。命名拒绝字面：`blocking-unresolved`。claimed status 保持 `Planned`，未降级、未改写。

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 096 |
| Requirement Key | 096-sdd-observer-agent |
| Requirement Name | SDD 专用观察者与线级观察记录（sdd-observer） |
| Related Feature | 096 SDD Observer Agent（sdd-observer 专用观察者与线级 journal） |
| Repository | spec-kit（worktree `096-sdd-observer-agent`） |
| Repository URL | 已配置 `gitee` / `github` / `gitlab`（均 `cloud-native-ai/spec-kit`）；`origin` 指向上游 `github/spec-kit` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` 为空：HEAD 未推送到任何跟踪远端分支。本报告不使用 URL 引用，统一用绝对路径 + `git show ed4dd1e6b:<path>` 取回 |
| Branch | 096-sdd-observer-agent |
| Commit SHA | ed4dd1e6b43336e84a6de41d2c24f13c6a64fb35（short: ed4dd1e6b） |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent` |
| Review Date | 2026-11-10 |
| Reviewer (Agent) | Qoder（SDD review run；git user: Qiming Liu (John)） |
| Environment | Linux x64；CPython 3.11.11；pytest 8.4.2；git 2.43.5 |
| spec-kit Source Snapshot | 本 worktree @ ed4dd1e6b（`journal-utils.py` 自报版本 0.0.22） |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 253 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/requirements.md` | 23 FR / 7 SC；observer 角色、生命周期、journal 客观性与边界 |
| plan.md | 277 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/plan.md` | 22 项宪法检查、5 decision tensions、8 premises、4 工作包 |
| tasks.md | 382 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/tasks.md` | 47 行依赖有序任务，47/47 关闭；DoD-7 延至 closure |
| data-model.md | 164 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/data-model.md` | 10 实体 / 20 校验规则（V-1…V-20） |
| contracts/ | 375（5 文件） | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/contracts/` | 58 条款：role / lifecycle / format / engine / verification |
| quickstart.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/quickstart.md` | S-0…S-7 八场景 |
| research.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/research.md` | R-01…R-14 实测记录 |
| feature-ref.md | 111 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/feature-ref.md` | 19 交付行、FR/SC 映射、重叠裁定 |
| verification.md | **absent** | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/verification.md` | 期望产物缺失：无 SC 状态行、无 smoke 记录（见 §2.2 / §2.4） |
| review.md | 本文件 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/review.md` | 本报告 |
| code-review.md | 696 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/code-review.md` | 代码段记录（含覆盖率回执与逐条意见） |
| test-evidence/review-smoke.txt | 22 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/test-evidence/review-smoke.txt` | 实现段冒烟三元组的证据载体 |

## 1. Process Execution Timeline

从 `git log b3da3a26..HEAD` 与状态脊重建；时间线只取有提交/产物锚的事件。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements 阶段完成 | `32c26f3c0`（requirements + checklist + test-evidence + glossary） | none |
| 2 | clarify 完成 | `7d3e34183` | none |
| 3 | plan 完成 | `79a650f45`；plan.md:38 以 v1.19.0 渲染 Constitution Check | none（版本 pin 见 F5） |
| 4 | tasks 完成 | `492353de4`；GATE-4 声明 `verification.md` 载体 | none |
| 5 | checklist 完成 | `38377e3ae` | none |
| 6 | analyze round 1 | `07cf28816`；merge 报告 39 findings = CRITICAL 0 / 4 validated HIGH / 26 MEDIUM / 8 LOW | gate 未过 |
| 7 | analyze round 2 | `60c78e773`；1 CRITICAL + 3 HIGH | gate 未过 |
| 8 | analyze repair r3 + round 3 | `32e83b95e` → `14a7da094` | gate 未过 |
| 9 | analyze repair r4 + round 4 | `05491c0a7` → `4c34b2c1f`；open HIGH W13-17（`verification.log` vs `.gitignore` vs 框架链） | gate 未过 |
| 10 | **宪法修订 v1.19.0 → v1.19.1** | `34ea3eb76`；Sync Impact Report: "Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)" | **deviation**：运行中修订治理文档 |
| 11 | analyze repair r5 + round 5 | `e2b248bfd` → `dee7e2976` / `c9b86e7fa`；C0/H0 门禁通过 | none（5 轮才过） |
| 12 | implement setup | `ac9ca879b`；基线/落点固化 | none |
| 13 | implement wp01–wp04 | `50cdd6cb5` … `ed4dd1e6b`（13 个实现/证据提交）；47/47 行关闭 | **deviation**：`verification.md` 未产出，Feature 停在 `Planned` |
| 14 | state spine 记录 | 最后一条 Stage Record 是 analyze r4；loop-state 仍是 `stage: requirements` / `attempt: 0`；无 r5 / implement 记录 | **deviation**：单一持久状态过期（见 F2） |
| 15 | review（本次） | `check-prerequisites.sh` 成功；`closure-acceptance-check.py --spec-dir ... --json` → exit 2 | ARC 输入错误（见 F1 / §2.4） |

## 2. Findings Summary

> 本节汇总的是**过程段**（`review-sdd-process`）的 findings。产物段与实现段各自在 `### 2.2` / `### 2.3` 给出自己的逐条表，代码段在独立的 `code-review.md`；四段结论不合并、不折算、不评分。

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 3 |
| Documentation | 1 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | `git-delta-review.sh base --spec .specify/specs/096-sdd-observer-agent` |
| Head commit | ed4dd1e6b43336e84a6de41d2c24f13c6a64fb35 | run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier the code segment reported |
| Renderer mode | text | the code record's header marker (`renderer: text`) |
| Changed / judged / skipped / gap files | 162 / 11 / 151 / 0 | copied field by field from the receipt block in `code-review.md` |
| Segment verdict | blocked | the current record carries a `blocking` entry |
| Gate verdict | blocking-unresolved | `report --summary --file code-review.md` → `gate=deny`, exit 1 |
| Reason, when one applies | the current code record carries a `blocking` entry (record-scoped: `scripts/python/journal-utils.py:65` rejects the owner-documented record-section shape); `report --summary --file` returns `gate=deny` | `code-review.md` |
| Uncommitted scope | `.specify/specs/096-sdd-observer-agent/checkpoints/`（未跟踪目录，运行前已存在，非本切片产物）— disclosed, never concluded over | `git status --porcelain` at run start |
| Record | .specify/specs/096-sdd-observer-agent/code-review.md | written (triage = run) |
| Archive | none | first run |

代码段四短语约束：本次以 `renderer: text` 运行，记录与结论均未声称可视化评审已完成。本报告推荐行中的 `CR-1` / `CR-2` / `CR-3` 依次指 `code-review.md` 内的 blocking / important / suggestion 三条（按记录内出现顺序，不折算为 P 级）。

### 2.2 Artifact Review Segment

Artifacts: 6 / 7   missing: verification.md

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md | union of the stage rules (Canonical Status State Machine: every SC has a `verification.md` status row) and plan.md § Project Structure |
| Coverage line | 6 / 7 | present members / expected members |
| Missing members | verification.md | absent from disk |
| Segment verdict | blocked | the finding rows below are this segment's record |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | .specify/specs/096-sdd-observer-agent/verification.md | — | artifact absent from disk; no line is addressable | **AF-1** — 期望成员缺失：无 `SC-NNN_status=` 行、无 smoke 三元组；ARC 因此 exit 2，实现段也无法引用 feature smoke record。补写六类 `SC-001…SC-007_status=` 行 + `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=` 后重跑 `closure-acceptance-check.py`。 |
| P1 | .specify/specs/096-sdd-observer-agent/tasks.md | 20 | none | **AF-2** — DoD-4 写「zero NEW failed ids against the implement-entry baseline」，而 `test-evidence/full-suite.txt:121` 实测 GATE-1 字面 delta = 11 ids；结论改用「attributable to this line」的解释性口径，同一事实两个判据。把 GATE-1 改成「先落 implement-entry baseline，再要求逐名 delta 为空」，或把 11 条归因写成带 owner 的 DEFERRED。 |
| P2 | .specify/specs/096-sdd-observer-agent/requirements.md | 181 | none | **AF-3** — Key Entities「记录条目」仍写「承载八类信息」，与 FR-011:142 的九类矛盾（W13-02 历轮 carried over）；改为九类并引用 FR-011。 |
| P2 | .specify/specs/096-sdd-observer-agent/plan.md | 38 | none | **AF-4** — Constitution Check 渲染注记仍写 `(v1.19.0)`，实际宪法为 v1.19.1（W13-20）；更新版本 pin。 |
| P2 | .specify/specs/096-sdd-observer-agent/tasks.md | 33 | none | **AF-5** — GATE-4 披露句仍称 `verification.log` 字面「由框架级统一裁定」，该裁定已于 v1.19.1 完成（W13-19；同句在 :379）；把「待裁定」改为「已裁定为 verification.md」。 |
| P2 | .specify/specs/096-sdd-observer-agent/plan.md | 135-149 | none | **AF-6** — § Project Structure 的 Documentation 树没有列出 `verification.md`，为后来 DoD-7 的延后留下缺口；把该成员加入树并声明其产出阶段。 |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | ed4dd1e6b43336e84a6de41d2c24f13c6a64fb35 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_agent.py tests/contract/test_sdd_observer_lifecycle.py tests/contract/test_sdd_loop_driver_skill.py -q` | recorded verbatim |
| Smoke exit code | 0 | the integer the command returned |
| Smoke evidence path | .specify/specs/096-sdd-observer-agent/test-evidence/review-smoke.txt | exists, 22 lines |
| Scope and regression verdict | scope: pass with one render-refresh disclosure; regression: pass — 096 modules green, full-suite 11 NEW ids all attributed to the pre-existing trigger suite (no 096 id in the failed list) | segment's own reading |
| Segment verdict | blocked | the finding rows below are this segment's record |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P0 | scripts/python/journal-utils.py | 622 | none | **IM-1** — `anomaly` 事件只在日志最后一个非空行以 `ANOMALY:` 开头时被投影。夹具 `write_quartet(anomaly=..., sentinel_present=True)` 把 ANOMALY 写在完成哨兵之前，实测该线上一次 append 产出 47 行、0 条 anomaly 行——绿阶段报告的异常被静默遗漏（FR-012 / US1 AS2）。扫描日志中最后一个 `ANOMALY:` 行，并补 anomaly+sentinel 契约用例。 |
| P1 | scripts/python/journal-utils.py（owner 面：skills/external/sdd-loop-driver/SKILL.md:239） | 65 | none | **IM-2** — 记录节形状 owner 在代码块中把 `## Observer Record — …` 与八个键写成两空格缩进，而唯一解析器 `OBSERVER_HEADING_RE = re.compile(r"^##\s+Observer Record…")` 只接受行首 `##`。按 owner 文本逐字写出的状态脊使 `append` 以 exit 2 失败（`identity-mismatch: no observer record section`，已实证）。解析前 strip 行首空白（或把 owner 块去缩进），并让测试直接喂入 owner 块。 |
| P2 | .claude/agents/reporter.md; .github/agents/reporter.agent.md; .opencode/agents/reporter.md; .qoder/agents/reporter.agent.md | 44 | none | **IM-3** — T041 的 `specify render-agents --ai <tool>` 会重生成全部 agent 副本，导致四个与本特性无关的 reporter 副本各增 1 行 092 handoff 注释；这是生成面副作用而非需求工作，plan 的 Mirror Obligations 未声明。给 render 命令加 per-agent 过滤，或在 plan 的镜像表中声明这些副本会被刷新。 |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Planned | `.specify/features/096.md` `**Status**`（与 `.specify/features.md` 096 行一致） |
| `final_path` record, copied verbatim (7/7) | **not produced** — `closure-acceptance-check.py --spec-dir .specify/specs/096-sdd-observer-agent --json` exits 2: `input error: required input not found: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/verification.md` | `scripts/python/closure-acceptance-check.py`, never recomputed here |
| Comparison verdict | refused | the transition cannot be granted |
| Failed condition, on refusal | (i) from-state is not `Implemented` — the claim reads `Planned`, and `Planned → Ready for Review` is not a transition; (ii) the ARC input `verification.md` is absent (checker exit 2), so no `final_path` record exists and the fourth condition cannot be evaluated; (iii) the current code record carries a `blocking` entry (condition (c) fails); (iv) no user waiver names any condition | named, not merely "the transition was refused" |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the claim is `Implemented` / `Ready for Review` while `pass=0`; here the claim is `Planned` and no record was produced |

**Status transition judgement**: `Implemented → Ready for Review` is **refused**; the claimed status stays `Planned`. The unattended disposition is halt-and-report; the named refusal literal recorded in `### 2.1` and in this run's conclusion is `blocking-unresolved`.

## 3. Findings (Problems & Improvement Targets)

### F1 — Review gate requires an artifact that this line defers to a later stage

- **Severity**: P0
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/tasks.md:26` and `:33`; `templates/commands/review.md:85-99`; `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md:31` (stage plan `… implement → review → closure → 合并 master`)
- **Evidence** (verbatim quote):

  ```
  DoD-7 (GATE-4: every final-path SC has a `pass` reading and the smoke record is present in `verification.md`) is deferred to the closure stage's Pre-Status-Flip Gate — measured at wp04 close: `verification.md` absent and no task row creates it
  ```

  ```
  closure-acceptance-check: input error: required input not found: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/verification.md
  ```

- **Why it's a problem**: the review's Acceptance Reality Check reads `verification.md` before any status transition may be judged, while this line's stage plan runs review before closure — the stage that the feature says will write that file. The review therefore cannot copy a `final_path` record, and the gate becomes structurally undecidable. The implement template's own output contract says `/speckit.implement` populates `verification.md`; the deferral contradicts the framework chain, not just the review.
- **Proposed fix**: add an implement-stage task row (after T047) that writes the six-key `SC-NNN_status=` block plus the smoke triple into `.specify/specs/096-sdd-observer-agent/verification.md` and runs `python3 scripts/python/closure-acceptance-check.py --spec-dir <spec>` before review; change DoD-7 from "deferred" to that row. If the line insists on review-before-closure, move review after closure in the driver stage sequence instead — the two orders cannot both hold.

### F2 — The state spine contradicts the line it is supposed to record

- **Severity**: P0
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md:7` (`stage: requirements`), `:11` (`attempt: 0`), `:13` (`last_verdict: U0 entry written; requirements dispatching`), `:23` (`state: stalled (U5; reentry-required)`), and the file tail (last `## Stage Record —` is analyze round 4)
- **Evidence** (verbatim quote):

  ```
  stage: requirements
  attempt: 0
  last_verdict: U0 entry written; requirements dispatching
  ```

  ```
  state: `stalled`（U5；reentry-required）
  ```

  ```
  next stage: implement（analyze 门 round-4 未过：W13-17 为决策项，须先处置）
  ```

- **Why it's a problem**: the spine is the driver's only persistent state and the journal's primary carrier. It currently reports "stalled at requirements, attempt 0", while 43 commits and 47/47 closed rows prove analyze round 5 and the whole implement stage ran. A reentry that reads the spine would restart at requirements; an observer projecting from the spine would record a false state. The missing round-5 and implement Stage Records are not cosmetic.
- **Proposed fix**: append the two missing Stage Records (`analyze` round 5 with its gate reading, `implement` with 47/47 and the DoD-7 deferral), refresh the loop-state block at every stage close, and add a driver-side guard that compares the loop-state `stage` with the last Stage Record heading and fails the close when they disagree.

### F3 — The implement-entry full-suite baseline was not captured; GATE-1's literal delta is not empty

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:20`; `.specify/specs/096-sdd-observer-agent/test-evidence/full-suite.txt:24` and `:121`
- **Evidence** (verbatim quote):

  ```
  DoD-4: **tests** — the new guard modules pass through the one runner (`bash scripts/bash/run-tests.sh`); the full-suite reading has zero NEW failed ids against the implement-entry baseline (owner of the baseline capture: `/speckit.implement` Step 0).
  ```

  ```
  No full-suite failed-names file was captured by `/speckit.implement` Step 0 in this line
  the GATE-1 literal delta is 11 ids, every one proven pre-existing
  ```

- **Why it's a problem**: the gate's criterion is a closed-set claim ("zero NEW failed ids"), but the measurement that exists yields 11 NEW ids against a reconstructed baseline. The line substitutes an attribution ("attributable to this line") for the gate's literal condition. The reconstruction is honest, but the label "DoD-4 pass" no longer means what the gate says, and every later reader must re-derive the distinction.
- **Proposed fix**: make `/speckit.implement` Step 0 capture the full-suite name list before the first edit (one Setup row: `bash scripts/bash/run-tests.sh --names-out <baseline>`), make GATE-1 compare against that file, and require an empty delta; if a shared trigger store makes the baseline unstable, isolate the store or mark GATE-1 DEFERRED with a named owner instead of re-interpreting it.

### F4 — A machine-read path literal in the constitution conflicted with `.gitignore` and the implementation chain, surfacing only at analyze round 4

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/constitution.md:1-10` (Sync Impact Report) and `:235`; `.specify/specs/096-sdd-observer-agent/plan.md:38`; `.specify/specs/096-sdd-observer-agent/test-evidence/analyze-merged-r4-2026-11-10.md`
- **Evidence** (verbatim quote):

  ```
  - Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)
  - Modified principles: VII. Workflow Gates — the Pre-Status-Flip Gate's status-line carrier is corrected from `verification.log` to `verification.md`
  ```

  ```
  round-4 未过 —— 1 条 open HIGH（W13-17）
  ```

- **Why it's a problem**: the plan-stage Constitution Check rendered 22 Pass rows against a constitution whose record carrier (`verification.log`) is excluded by `.gitignore` and unread by every machine consumer. The conflict survived requirements, plan, tasks and three analyze rounds, then forced an in-line constitutional amendment and a fifth analyze round. A plan-stage check that verifies only principle prose cannot catch a machine-read path that no chain reads.
- **Proposed fix**: add a plan-stage gate row — "every record carrier this plan names is (a) committable under the repository's ignore rules and (b) read by a named machine consumer" — and render the Constitution Check against the live version (the v1.19.0 pin is a symptom).

### F5 — Stale version and adjudication text after v1.19.1

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/096-sdd-observer-agent/plan.md:38`; `.specify/specs/096-sdd-observer-agent/tasks.md:33` and `:379`
- **Evidence** (verbatim quote):

  ```
  Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/constitution.md` (v1.19.0) in file order
  ```

  ```
  宪法 VII 的 `verification.log` 字面由框架级统一裁定（反馈已登记：…）
  ```

- **Why it's a problem**: the amendment already happened; the plan still pins v1.19.0 and the tasks still describe the carrier question as awaiting a ruling. The carrier instruction in the same sentences is still correct, so this is drift, not a behavior defect — but it is exactly the kind of stale fact that makes later readers distrust the artifacts.
- **Proposed fix**: update the plan's version pin to v1.19.1 and rewrite the two disclosures as "v1.19.1 已裁定为 `verification.md`（commit `34ea3eb76`）".

### F6 — `specify render-agents` refreshes unrelated agent copies as a side effect

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:248` (T041); `.claude/agents/reporter.md:44`; `.github/agents/reporter.agent.md`; `.opencode/agents/reporter.md`; `.qoder/agents/reporter.agent.md`
- **Evidence** (verbatim quote):

  ```
  +<!-- 092 handoff: D4 — 周期数值的唯一 owner 是 `.specify/shared/guidelines/reporting-obligations.md` § 二（长跑档 30 s）；上一行只抵达 `progress-reporting.md` 的交互档缺省与内容下限，该行保留不改、仅作历史记录。参见 092 D4，2026-11-09。 -->
  ```

- **Why it's a problem**: a feature-scoped render obligation silently changes four files owned by other features. The delta stays small here, but the pattern means every feature that renders agents can carry another feature's pending render drift, making the slice's scope claim unverifiable from the diff.
- **Proposed fix**: add a per-agent filter to `specify render-agents` (e.g. `--agent sdd-observer`) or declare the refreshed copies in the plan's Mirror Obligations table and verify them by name; do not let an unlisted copy change inside a feature delta.

## 4. What Worked — Preserve (Brief)

- The journal engine's closed-structure + single declaration owner design is real: `journal-format.yaml` holds every spelling, the engine reads it through `declaration_reader`, and the tamper/gap/dual-line/single-writer drills are genuine red/green tests rather than prose assertions.
- The driver lifecycle section is prose-only and non-blocking; the doctored-gate red leg gives the non-blocking property teeth instead of leaving it as a claim.
- Evidence discipline in `test-evidence/` is strong: every gate reading names its command, exit status and file, and the GATE-1 baseline reconstruction is disclosed as a deviation rather than hidden.
- The analyze repair loop produced traceable dispositions (r3/r4/r5) and recorded the constitutional carrier correction with a user ruling, so the amendment is auditable.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Implement-stage verification carrier** — Target: `templates/commands/implement.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/templates/commands/implement.md`) § Feature Integration, and `templates/tasks-template.md`. Change: make `verification.md` a required implement-stage output row and state that a DoD row may not defer it to a later stage; the review's ARC reads it before any status flip. Source: F1, AF-1. Expected impact: review and implement stop disagreeing about when the acceptance record exists.

### 5.2 Command Prompt Improvements

- None beyond F1's implement-template row; the review prompt already states the ARC clause correctly.

### 5.3 Automation / Script Improvements

- **State-spine close guard** — Target: `skills/external/sdd-loop-driver/SKILL.md` § 状态脊 + the driver's stage-close script. Change: at every stage close, append the Stage Record and refresh the loop-state block in the same step; fail the close when `stage` and the last Stage Record heading disagree. Source: F2. Expected impact: a stale spine becomes detectable at the moment it occurs, not at review.
- **Implement Step 0 baseline capture** — Target: `skills/internal/implement-feature/SKILL.md` Step 0. Change: capture the full-suite name list before the first edit and make `tasks.md` GATE-1 compare against that file. Source: F3, AF-2. Expected impact: the closed-set gate becomes decidable without post-hoc reconstruction.
- **Anomaly projection and owner-shape parsing** — Target: `scripts/python/journal-utils.py` lines 65 and 622, plus `tests/contract/test_journal_engine.py`. Change: strip leading whitespace before matching the observer record heading (or dedent the owner block), and scan the log for the last `ANOMALY:` line rather than only the last line; add the anomaly+sentinel case. Source: IM-1, IM-2, CR-1, CR-2. Expected impact: the mechanism writes under its own documented shape and stops silently dropping the anomaly event class.
- **Per-agent render filter** — Target: the `specify render-agents` CLI entry in `src/specify_cli/__init__.py`. Change: add a per-agent selector so a feature renders only the templates it owns; or record every refreshed copy in the plan's Mirror Obligations. Source: F6. Expected impact: feature deltas stop carrying other features' render drift.

### 5.4 Workflow Improvements

- **Plan-stage carrier committability check** — Target: `templates/plan-template.md` / `skills/internal/create-plan/SKILL.md`. Change: add the record-carrier check from F4 as a plan gate row and render the Constitution Check against the live version. Source: F4, F5. Expected impact: path literals that no machine reads, or that `.gitignore` excludes, are caught before analyze.

### 5.5 Documentation Improvements

- **Refresh the v1.19.1 residue** — Target: `plan.md:38` and `tasks.md:33/379` inside this spec. Change: update the version pin and rewrite the two carrier disclosures as completed rulings. Source: F5. Expected impact: the spec no longer contradicts the constitution it cites.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Produce `verification.md` at implement close and judge the review gate after it exists | `templates/commands/implement.md`, `templates/tasks-template.md` | F1, AF-1 |
| P0 | Make the state spine self-consistent at every stage close | `skills/external/sdd-loop-driver/SKILL.md` § 状态脊 | F2 |
| P0 | Fix the anomaly projection and the record-shape parser | `scripts/python/journal-utils.py:65`, `:622` | IM-1, IM-2, CR-1, CR-2 |
| P1 | Capture the implement-entry suite baseline in Step 0 | `skills/internal/implement-feature/SKILL.md` Step 0 | F3, AF-2 |
| P1 | Add the plan-stage carrier committability gate | `templates/plan-template.md`, `skills/internal/create-plan/SKILL.md` | F4 |
| P2 | Refresh v1.19.1 residue and the plan tree | this spec's `plan.md`, `tasks.md` | F5, AF-6 |
| P2 | Scope `render-agents` per agent | `src/specify_cli/__init__.py` | F6, IM-3 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status is stated explicitly.** F1 and F2 were each confirmed by a fresh-context, read-only independent validator that received only the finding, its anchors and the quoted evidence; both returned `confirm` (no reject, no downgrade). The artifact P0 (`AF-1`) is an existence fact (file absent; checker exit 2) and the implementation P0 (`IM-1`) is a reproduced measurement (47 appended rows, 0 `anomaly` rows), so neither relies on model judgement.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
