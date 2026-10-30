# Specification-Driven Development (SDD) Process Review Report: Coaching Skills（教练技能）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 078 |
| Requirement Key | `078-coaching-skills` |
| Requirement Name | Coaching Skills（教练技能） |
| Related Feature | 078 Coaching Skills（教练技能） |
| Repository | `spec-kit` |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (the only remote; SSH-only, no HTTPS web form) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the branch was never pushed. Cite absolute paths plus `git show 347a1458:<path>`; no URL citation in this report resolves |
| Branch | `078-coaching-skills` |
| Commit SHA | `347a145820c9cbfe56e9301799c3d01b5be9792e` (short: `347a1458`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-30 |
| Reviewer (Agent) | SDD executor subagent (unattended loop, stage `review`, run `r20261030T054502Z-078a`) — a different agent and a different session from the stage runs that wrote the artifacts under review |
| Environment | Darwin 25.6.0 arm64; git 2.54.0 (Apple Git-157); python 3.9.6 (system) and a Python venv carrying pytest 9.1.1 |
| spec-kit Source Snapshot | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` @ `347a1458` (self-hosting: framework sources and the `.specify/` runtime share one tree), `specify-cli` 0.0.22 (declared in `pyproject.toml`) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 250 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/requirements.md` | 29 FR / 9 SC / 4 user stories / 17 shared strings, plus assumptions A1–A11 and the clarify record |
| plan.md | 223 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/plan.md` | 18-principle Constitution Check, two decision tensions, mirror obligations, FR→clause mapping and the FR-lane exemption |
| data-model.md | 226 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/data-model.md` | 8 entities, 4 state machines, the RunStatus and optimization-claim owners |
| contracts/ (5 files) | 361 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/contracts/` | 38 clauses across run, expectation, observation, dispatch-payload and identity-and-wiring |
| quickstart.md | 216 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/quickstart.md` | 5 executable scenarios and the verification boundary |
| tasks.md | 340 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/tasks.md` | 31 dependency-ordered rows, 16 green-claim rows, 9 DoD items and 7 completion gates |
| verification.md | 209 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/verification.md` | Baseline readings, 9 SC status rows, evidence hashes and the gate digest |
| feature-ref.md | 41 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/feature-ref.md` | Feature 078 binding and the delivery-surface map |
| checklists/coaching-loop-2026-10-30.md | 72 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/checklists/coaching-loop-2026-10-30.md` | 36-item requirements-quality instrument (all items left unanswered) |
| checklists/requirements.md | 44 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/checklists/requirements.md` | The pre-plan specification-quality checklist, fully ticked |
| notes/pre-change-measurements.md | 147 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/pre-change-measurements.md` | Six pre-change commands with real output and exit codes |
| notes/red-first-evidence.md | 117 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/red-first-evidence.md` | Four red-first suites with command, output slice, exit code and failure count |
| notes/quickstart-run.md | 255 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/quickstart-run.md` | Scenarios 1–5 run record, including the transport-substitution note and teardown |
| notes/residual-audit.md | 136 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/residual-audit.md` | Guard-derived residual verdict, 22 faces / 1608 files, one permitted occurrence |
| notes/skill-shape-after.md | 62 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/skill-shape-after.md` | Skill-shape reading, 3278 of 5000 tokens, one wrap-up warning |
| test-evidence/ (43 files) | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/test-evidence/` | Per-stage deterministic readings, four part-status records, nine SC evidence files, plus this review's targeted run |
| State spine (read-only) | 121 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/state/078-coaching-skills.md` | Stage ledger, rebaseline events, test budget, U5 escalation and human ruling |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements + clarify written before the driver took over | `77557e56`, `c6bd986a`; `requirements.md` § Clarifications records two fresh-context subagents and 24 findings | No |
| 2 | Plan, tasks, checklist stages land in order | `375805f2` (plan), `c11d1aae` (30 tasks rows), `41e1b0fa` (checklist) | No; tasks-fix later grows the file to 31 rows |
| 3 | Analyze round 1 raises 1 CRITICAL / 3 HIGH; requirements-, plan- and tasks-fix land | `d06a85f6`, `d0f50759`, `21e15d53`, `f61d8a23`; `test-evidence/analyze-stage-status.txt` | No |
| 4 | Analyze round 2 finds a new HIGH (H-04, claim creation point) and the line halts | `e43f4c1a`; state spine § U5 | No — the halt-and-escalate rule was followed |
| 5 | Human-authorized design repair (H-04 + M-11) and analyze round 3 passes | `66edf74f`, `5e82668e`; analyze-r3 gate `CRITICAL 0 / HIGH 0` | No — explicitly recorded as an authorized exception, not an automatic loop |
| 6 | Implement part 1 (T001–T008) and part 2 (T009–T016) | `e7203cd1`, `c3cbee21`, `56bed08a`, `fa023d8c`; part-status files | No |
| 7 | Implement part 3 (T017–T024) edits a 20th source that no task owns: `scripts/python/sanitize-utils.py` | `7ce6fd57`, `ea3c16ac`; `test-evidence/implement-part3-status.txt` `changed_paths` lists the file | **Yes** — out-of-plan, out-of-task live-source edit (F1) |
| 8 | Implement part 4 (T025–T031): frozen rosters, real + degraded coaching runs, 9 SC rows | `c7357205`, `eb01db0b`, `435a0397`; `verification.md` | No; the "real" run is a scripted one-shot runner (F4) |
| 9 | Implement wrap-up records run determination, exec quant and feedback | `347a1458` | No |
| 10 | Feature status flip and the detail's `## Latest Review` entry are edited but never committed | working tree vs `git show HEAD:.specify/memory/features.md`; last commit touching the file is `f61d8a23` | **Yes** — the terminal transition is not durable (F2) |
| 11 | Review stage starts on a dirty tree: six modified paths plus one untracked evidence file | `git status --porcelain`: `M .specify/memory/features.md`, `M .specify/memory/features/078.md`, `M` three other features' run-determination records, `M .specify/state/078-coaching-skills.md`, `?? .specify/specs/078-coaching-skills/baseline-failed.txt` | Yes — no clean stage boundary (F2, F5) |
| 12 | Review stage (this run): process segment only, targeted set at `stage_base=347a1458` | `test-evidence/review-stage-status.txt`, `test-evidence/review-targeted.txt` (162 passed, rc 0, 9.21 s) | Scoped deviation, disclosed in § 2.1 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 5 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 2 |
| Workflow | 4 |
| Documentation | 1 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `d0f50759` | the feature baseline recorded in `verification.md` (not a code-segment resolution; the segment did not run) |
| Head commit | `347a145820c9cbfe56e9301799c3d01b5be9792e` (`347a1458`) | the run-start `HEAD`, fixed for the run |
| Base source | `none` | the code segment was not dispatched by this process-scoped stage |
| Renderer mode | `none` | no code record was produced |
| Changed / judged / skipped / gap files | `not produced` / `not produced` / `not produced` / `not produced` | no coverage receipt exists for this run |
| Segment verdict | `not-evaluated` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `blocking-unresolved` | the named refusal literal: the `Implemented → Ready for Review` transition's third condition is an existence test over `code-review.md`, and no such record exists for this run |
| Reason, when one applies | the calling workflow scoped this run to the process segment, so segment 2 was deliberately not dispatched; that scope has no triage value in the command's three-value closed set | mandatory for `not-evaluated` |
| Uncommitted scope | six pre-existing modifications (`features.md`, `features/078.md`, three run-determination session records of other features, the state spine) and one untracked evidence file (`baseline-failed.txt`) were present at run start; none is part of the review object and no conclusion is issued over them | disclosed, never concluded over |
| Record | `not written` | written only when the triage value is `run` |
| Archive | `none` | first review run for this feature |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The process conclusions live in § 3–§ 6 of this report. The code segment's absence is a **scope fact of this run**, not a defect of the feature; closure must dispatch segment 2 or record its own triage before the status transition can be granted.

## 3. Findings (Problems & Improvement Targets)

### F1 — The "19-file closed wiring surface" was falsified during implementation by a 20th live source, and the acceptance criterion still passes by construction

- **Severity**: P1
- **Category**: Documentation
- **Location**: `.specify/specs/078-coaching-skills/requirements.md` § A10 (line 47) and § SC-006; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/sanitize-utils.py` line 637
- **Evidence** (verbatim quotes):

  ```
  本特性开始前实测的 19 个需手改源文件（技能本体 2、路由模板 1、agents 2、create-agent 角色模板 4、run-skills 1、shared/definitions 2、src `_OBSOLETE_SKILLS` 1、docs 2、contract tests 4）……
  **允许差异集恰为一项**：`_OBSOLETE_SKILLS` 中保留旧名的那一行（FR-020 要求它必须存在）；除此之外空集。
  ```

  ```
  -    "theme-creator", "thought-experiment-verifier", "visualize-project",
  +    "theme-creator", "think-skills", "thought-experiment-verifier", "visualize-project",
  ```

  ```
      missing = set(specify_cli._OBSOLETE_SKILLS) - set(su.LEGACY_SKILL_NAMES)
      assert not missing, f"LEGACY_SKILL_NAMES lags the CLI registry: {sorted(missing)}"
  ```

- **Why it's a problem**: the closed set was derived by grepping the retired literal, but `sanitize-utils.py` is a **consumer of the cleanup registry**, not a place that mentioned the old name before this feature. Adding the name to `_OBSOLETE_SKILLS` forces the matching `LEGACY_SKILL_NAMES` entry (the drift guard above), so a 20th hand-edited source was required and now holds the retired literal outside the declared one-line allowance. SC-006 still reads "exactly 1" because it counts inside the 19-file surface only; the guard's own candidate set is also derived from that surface. The containment claim is therefore false in the delivered tree, and its green reading is vacuous for the new face. The edit is also absent from every task row (no `sanitize` occurrence in `tasks.md`, `plan.md` or `requirements.md`), so task→change traceability breaks at part 3.
- **Proposed fix**: derive closed sets from **registry consumers as well as literal occurrences** (owner: `shared/guidelines/closed-set-claims.md`), and amend Feature 078's A10 / SC-006 to name `scripts/python/sanitize-utils.py` (`LEGACY_SKILL_NAMES`) as a registry-consumer face with its own allowed occurrence, or record it as an explicit second exemption. Add the face to the wiring guard's derived candidate set.

### F2 — The implement stage's terminal status flip and review record are uncommitted; `HEAD` still reports `Planned`

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features.md` line 87; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/078.md` § Latest Review
- **Evidence** (verbatim quotes):

  ```
  git show HEAD:.specify/memory/features.md | grep '^| 078 '
  | 078 | Coaching Skills（教练技能） | ... | Planned | .specify/memory/features/078.md | ... |
  ```

  ```
  working tree, same command:
  | 078 | Coaching Skills（教练技能） | ... | Implemented | .specify/memory/features/078.md | ... |
  ```

  ```
  git log --oneline -1 -- .specify/memory/features.md
  f61d8a23 docs(078-coaching-skills): repair tasks against analyze findings H-03, H-02, M-06, L-01, M-02, L-02
  ```

- **Why it's a problem**: the implement stage's last verdict claims `Feature 078 -> Implemented`, but the two carriers of that claim exist only in the working tree; a fresh checkout, the closure run and the merge all read `Planned`. The part-4 commit (`347a1458`) staged run records and evidence but not the registry row or the `## Latest Review` entry. This is the same defect Feature 071's review raised as REC-071-03 — a stage closing with its own two carriers stale — and it recurred here one feature later.
- **Proposed fix**: apply REC-071-03 (status-consistency check at stage closure) and extend the `/speckit.implement` commit gate to include the feature registry row and detail file whenever a status transition is claimed, failing closed on `git status` for feature-owned paths.

### F3 — Analyze's residual 9 MEDIUM / 9 LOW findings have no disposition record and vanish between analyze and implement

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/test-evidence/analyze-stage-status.txt` line 28; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/verification.md` lines 116–117
- **Evidence** (verbatim quotes):

  ```
  gate=CRITICAL 0 / HIGH 0 → implement RELEASED (residual M 9 / L 9 are non-blocking)
  ```

  ```
  deferred_tasks=
  deferred_reason_summary=none — T025-T031 all executed in this segment
  ```

  State spine § 阶段记录: `H-04/M-11 闭合；M-15/M-16 等 9M/9L 留待实现时顺带处理`.

- **Why it's a problem**: "留待实现时顺带处理" is an instruction with no carrier. A search for `M-15` / `M-16` across the spec directory hits only `analyze-stage-status.txt`; no implement artifact lists, fixes, defers or waives any of the 18 residuals. `verification.md` reports `deferred_tasks=` empty, which is true of **tasks** but reads as "nothing deferred" for the process as a whole. The review cannot tell whether the residuals were handled or silently dropped — exactly the failure mode the ID Register exists to prevent, since these are durable finding identifiers cited by a tracked artifact and absent from `.specify/memory/register.md`.
- **Proposed fix**: require `/speckit.analyze` to register every surviving MEDIUM/LOW finding as an open item in `.specify/memory/register.md` at coin time, and require `/speckit.implement` to carry a per-finding disposition row (fixed / carried as an open item / waived with reason) into `verification.md` before the completion gate can pass.

### F4 — The "real" coaching run is a scripted one-shot runner emitting only `self-report`; the host-native dispatch channel the feature is built around was never exercised

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/notes/quickstart-run.md` lines 8–14; `verification.md` § SC-001
- **Evidence** (verbatim quotes):

  ```
  **Transport note (read first).** Scenario 2's single dispatch was executed by a one-shot
  runner that loads `tests/fixtures/coaching/fixture-trainee/SKILL.md` by explicit path and
  follows its Workflow literally, emitting one event per step. No host-native subagent was
  offered to this stage, so the run records `mode: run-skills-explicit-path`,
  `self-report` rows from the runner's event log, and the substitution is stated verbatim in
  the DispatchRecord `anomaly-line` instead of being presented as host telemetry.
  ```

  ```
  SC-001_value=4/4 artifacts + 1/1 primary artifact
  ```

- **Why it's a problem**: the disclosure is exemplary, but the acceptance verdict is not capped accordingly. SC-001 ("一次夹具教练运行") and SC-005 ("执行优先") are marked `pass` on a run whose Trainee was driven by a purpose-written script inside the same working tree, with seven of seven rows `source: self-report`. FR-009's "恰好一个子代理", A5's host-native-first ladder and FR-029's two independent contexts are the load-bearing mechanisms of the feature, and none of them is evidenced by this run. The four artifacts are honest; the inference "the skill works when dispatched by a host" is not. REC-069a-01 already requires a runtime observation for runtime-event SCs; this run shows the next gap: the observation must also identify **which transport** produced it.
- **Proposed fix**: extend the evidence vocabulary (owner: `shared/guidelines/better-harness.md` § 证据纪律) with a transport-identity field (`host-event` / `self-report` / `scripted-substitute`) that a `pass` verdict must carry, and allow at most `partial` when the declared transport differs from the design's primary channel. Record the run's transport in the SC row itself, not only in a free-form note.

### F5 — The implement-start full-suite failure-name baseline is untracked, and the "no new failures" comparison is split across three artifacts with different scopes

- **Severity**: P1
- **Category**: Automation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/baseline-failed.txt` (untracked); `verification.md` line 11; `test-evidence/part4-baseline-failed.txt`; `test-evidence/part4-current-failed.txt`
- **Evidence** (verbatim quotes):

  ```
  ?? .specify/specs/078-coaching-skills/baseline-failed.txt
  ```

  ```
  baseline_full_suite_note=the single implement-start full-suite slot (E2); the 16 names are frozen in `baseline-failed.txt` and are pre-existing reds unrelated to this feature
  ```

  The committed `part4-baseline-failed.txt` holds only the seven feature-owned reds, and the committed `part4-current-failed.txt` is a 0-byte file.

- **Why it's a problem**: the state spine's test-budget row and `verification.md` both point at a path that no checkout contains. The closure gate's name-level comparison ("no new failures") needs those 16 full-suite names; after a clone or a worktree switch, the comparison degrades to "compare against an empty file" and passes trivially. The three artifacts also mix scopes (full-suite baseline, targeted-feature baseline, targeted current) without a scope field, so a reader must reconstruct which set each name belongs to.
- **Proposed fix**: make "every path written into the state spine or `verification.md` is tracked" a checked condition of the stage-status emission (`shared/guidelines/single-run-evidence.md`), and give the failure-name artifacts a header carrying command, scope (full / targeted), base commit and counts, so an empty file can never stand in for "not run".

### F6 — The coverage engine cannot consume a declared lane exemption, so every stage carries a red exit code the completion gate has to argue around

- **Severity**: P2
- **Category**: Automation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/account-clause-coverage.py`; `verification.md` lines 142–160; `plan.md` § FR-Lane Exemption (line 212)
- **Evidence** (verbatim quotes):

  ```
    [fr-uncovered] fail (29) — 0 of 29 FRs cited from citation groups
    ...
  29 error(s), 0 warning(s)
  status: uncovered
  rc=1
  ```

  ```
  `account-clause-coverage.py` 的 **FR 车道对本特性不适用**：该车道的 claimed 子集取自每个条款块最后一个含 FR/SC 的括号组（CITATION GROUP），而本特性的契约刻意采用条件形态条款、不带 citation group，运行该车道只会按构造报「零覆盖」，不是映射缺失。
  ```

- **Why it's a problem**: the exemption is reasoned, recorded and owned by `plan.md`, yet the engine still exits 1 and the completion gate text has to explain why a red checker is acceptable (`tasks.md` GATE-4 calls it "制品缺口而非本阶段可修项"). Every stage then re-litigates the same exemption in prose, and a future run that genuinely loses FR coverage looks identical to this declared non-applicability.
- **Proposed fix**: add a machine-readable lane waiver (`--waive-lane fr --reason-file <path>`) that the engine prints in its summary and reflects in the exit code, so "not applicable by construction" is distinct from "uncovered" and the waiver is auditable instead of narrative.

### F7 — `requirements.md` still declares `Status: Draft` while the registry says `Implemented`

- **Severity**: P2
- **Category**: Template
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/078-coaching-skills/requirements.md` line 5
- **Evidence** (verbatim quotes):

  ```
  **Status**: Draft
  ```

  Registry row: `| 078 | ... | Implemented | .specify/memory/features/078.md | ... |`

- **Why it's a problem**: the two status carriers disagree, and the reader who opens the specification first is told the feature is a draft. This is a known, still-open defect — registered as REC-072-04 ("避免 plan-owned 冻结把 `requirements.md` 头状态滞留在 `Draft`") — and this feature is its second observed recurrence.
- **Proposed fix**: as REC-072-04 — either reconcile the header at each stage transition or retire the field and point at `.specify/memory/features.md` as the single status owner.

### F8 — The same-author gate's only fallback is "dispatch failed twice"; an operating constraint that forbids dispatch has no vocabulary, so stages record the weaker path as free prose

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/078-coaching-skills/plan.md` line 148; `checklists/coaching-loop-2026-10-30.md` line 69; `shared/workflow/objective-analysis-gate.md` rule 7
- **Evidence** (verbatim quotes):

  ```
  未派发 Explore 子代理（本次运行受单上下文约束）。同一约束也适用于 Constitution Check 与质量门的同作者自评分：两份评分均由本上下文完成，未做 fresh-context 委派——这是本阶段的方法局限
  ```

  ```
  This run is under a driver constraint that forbids dispatching subagents, so the gap-finding pass was single-context.
  ```

  Later in the same line, analyze reports: `validation_wave=5 read-only external validators (qodercli -p, write tools disabled, no session persistence)`.

- **Why it's a problem**: the gate's sanctioned degradation requires two consecutive dispatch failures and a visible marker; a run-level prohibition on dispatch is neither, so plan and checklist invent their own prose. The same run later demonstrates that a compliant path (external read-only validators) existed, which makes the earlier non-delegation look like an unexamined default rather than a forced constraint. No reader can compare the two weakenings because they are worded differently.
- **Proposed fix**: add a named fallback reason to the gate (for example `operating-constraint`) with a required marker form and a "what would have been delegated" field, and make the plan/checklist emitters print that marker instead of ad-hoc sentences.

### F9 — `/speckit.review` has no representation for a deliberately process-only invocation; the three-value triage leaves a stage-scoped run reading as a code refusal

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.review.md` § Composition and § Applicability triage; source template `templates/commands/review.md`
- **Evidence** (verbatim quotes):

  ```
  The process segment runs on every invocation. No execution class or expression class exempts it, no `$ARGUMENTS` value exempts it, an absent code delta does not exempt it, and no earlier segment's outcome exempts it.
  ```

  ```
  There is no fourth state: an unspecified value, an empty value, or a silently dropped segment is a violation.
  ```

  ```
  Without an explicit user ruling the command stops before the transition, reports the block, and records `blocking-unresolved`
  ```

- **Why it's a problem**: an unattended workflow that wants only the process review cannot express that intent: `$ARGUMENTS` explicitly cannot select a segment, the triage's closed set has no "deliberately deferred" value, and the refusal literal for a missing code segment (`blocking-unresolved`) is indistinguishable from a real blocking code finding. This run had to record `not-evaluated` / `blocking-unresolved` for a feature whose process chain is sound, which would read to a closure driver as a review failure.
- **Proposed fix**: add a fourth triage value (for example `deferred-by-caller`, with a mandatory reason and owning stage) or a `--segments process` parameter that records the omission as a non-blocking scope fact; keep `blocking-unresolved` reserved for an actual unresolved `blocking` code finding.

## 4. What Worked — Preserve (Brief)

- Red-first evidence with the four required fields per suite, a re-confirmation run, and every red explicitly attributed to a later task.
- The analyze loop's halt-and-escalate: a second-round HIGH stopped the line, a human ruling was recorded in the state spine, and the authorized repair was re-verified read-only before release.
- The residual verdict is a guard copy that mechanically derives 22 faces / 1608 files, with `git grep` demoted to diagnostic side evidence.
- Part segmentation stayed bounded (four parts, at most eight tasks each) and each part-status file records command, rc, counts, new-failure names and the budget slot it did or did not consume.
- Pre-change measurements exist for every judged surface (79 ledger rows, 75 compiled units, 27 blocking gates) and the one factual plan error (probe units 75 vs 76) was corrected in place with a dated PLAN-EDIT rather than silently.
- Substitutions and limitations are disclosed rather than hidden: the transport note, the plan's same-context scoring limitation and the sanctioned temp-dir scratch are all written down.
- The contract partition is machine-checked (38 clauses, 16 claim rows, `validate-tasks.py` zero findings).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-072-04 (existing, open) — reconcile or retire the requirements header status** — Target: `templates/requirements-template.md` header block. Change: as already registered, either reconcile `**Status**` at every transition or remove the field and point at `.specify/memory/features.md`. Source: F7. Expected impact: one status owner; no more "Draft" specifications behind an `Implemented` registry row.

### 5.2 Command Prompt Improvements

- **REC-078-07 — give `/speckit.review` a non-blocking scope-only triage** — Target: `templates/commands/review.md` § Applicability triage and § Status Transition (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/review.md`). Change: add `deferred-by-caller` (with reason and owning stage) or a `--segments process` parameter; reserve `blocking-unresolved` for a real blocking code finding. Source: F9. Expected impact: a process-scoped unattended stage stops reading as a refused code review, and the status transition stays judgeable by the stage that owns it.

### 5.3 Automation / Script Improvements

- **REC-078-04 — make evidence paths tracked and give failure-name artifacts a scope header** — Target: `shared/guidelines/single-run-evidence.md` plus the stage-status emitters under `scripts/python/` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/guidelines/single-run-evidence.md`). Change: a path written into the state spine or `verification.md` must be tracked; failure-name files carry command, scope, base commit and counts. Source: F5. Expected impact: the closure name-level comparison cannot degrade to comparing against an empty file after a clone.
- **REC-078-05 — let the coverage engine consume a documented lane waiver** — Target: `scripts/python/account-clause-coverage.py` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/account-clause-coverage.py`). Change: accept a `--waive-lane fr --reason-file <path>` declaration, print it in the summary, and reflect it in the exit code. Source: F6. Expected impact: "not applicable by construction" and "uncovered" stop looking identical, and stages stop hand-arguing a red checker.

### 5.4 Workflow Improvements

- **REC-078-01 — derive closed sets from registry consumers, not only literal occurrences** — Target: `shared/guidelines/closed-set-claims.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/guidelines/closed-set-claims.md`). Change: require the derivation to enumerate (a) literal occurrences and (b) code paths that must gain the literal when a registry grows; a closed-set claim that names only (a) is incomplete. Source: F1. Expected impact: rename features stop reporting a green containment claim that a forced consumer edit has already falsified.
- **REC-078-02 — register analyze residuals and dispose them at implement** — Target: `skills/internal/analyze-artifacts/SKILL.md` and `templates/commands/implement.md` (absolute supplements under `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/`). Change: every surviving M/L finding gets a register row at coin time and a disposition row in `verification.md` before the completion gate. Source: F3. Expected impact: the 18 non-blocking findings of a run can no longer disappear between stages without any artifact lying.
- **REC-078-03 — make transport identity part of the verdict, not a note** — Target: `shared/guidelines/better-harness.md` § 证据纪律 and `skills/internal/implement-feature/SKILL.md` (absolute supplements under `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/`). Change: a runtime-event SC's verdict carries `host-event` / `self-report` / `scripted-substitute`, and a substitute transport caps the verdict at `partial`. Source: F4. Expected impact: a fixture run driven by a purpose-written script can no longer certify the host-dispatch mechanism it never exercised.
- **REC-078-06 — give the same-author gate an operating-constraint fallback** — Target: `shared/workflow/objective-analysis-gate.md` rule 7 (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/workflow/objective-analysis-gate.md`). Change: add a named `operating-constraint` fallback with a required marker and a "what would have been delegated" field. Source: F8. Expected impact: forced non-delegation becomes comparable across stages instead of being recorded in ad-hoc prose.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Derive closed sets from registry consumers | `shared/guidelines/closed-set-claims.md` | F1 |
| P1 | Apply the stage-closure status-consistency check (existing REC-071-03) | `templates/commands/implement.md` + `scripts/python/` | F2 |
| P1 | Register analyze residuals and dispose them at implement | `skills/internal/analyze-artifacts/SKILL.md` + `templates/commands/implement.md` | F3 |
| P1 | Make transport identity part of the SC verdict | `shared/guidelines/better-harness.md` + `skills/internal/implement-feature/SKILL.md` | F4 |
| P1 | Track evidence paths; add scope headers to failure-name artifacts | `shared/guidelines/single-run-evidence.md` + stage-status emitters | F5 |
| P2 | Let the coverage engine consume a documented lane waiver | `scripts/python/account-clause-coverage.py` | F6 |
| P2 | Reconcile or retire the requirements header status (existing REC-072-04) | `templates/requirements-template.md` | F7 |
| P2 | Add an operating-constraint fallback to the same-author gate | `shared/workflow/objective-analysis-gate.md` | F8 |
| P2 | Give `/speckit.review` a non-blocking scope-only triage | `templates/commands/review.md` | F9 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target needed an `external` marking.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

The same-author detection gate at the skill's step 4 **did not fire**: the artifacts under review were written by earlier stage runs in other sessions, and this reviewer authored none of them. No detection therefore had to be delegated. This stage also ran under an explicit no-subagent constraint, so any P0 would have required the documented direct re-read fallback with its marker.

### Conclusion — may this feature enter closure and merge?

**Process chain: yes, with record repairs.** The spec → plan → tasks → analyze loop → implement → verification chain is intact: the contracts are partitioned and machine-claimed, red-first evidence exists, the analyze gate halted and escalated rather than proceeding on a HIGH, the human ruling is recorded, the test budget was respected (one full-suite slot at implement start, targeted sets only in the parts, closure reserved), and every stage wrote deterministic readings. P0 = 0; nothing found here blocks closure or merge on implementation grounds.

**Before the feature is marked `Ready for Review` / `Completed`, three P1 record defects should be closed:** F1 (the 19-file closed set is falsified by the sanitize edit, so SC-006's green reading is vacuous for one face), F2 (the status flip is uncommitted, so a fresh checkout still says `Planned`), and F3 (18 analyze residuals have no disposition). F4 and F5 should be repaired in the same closure window because they decide what the closure's "no new failures" and "9/9 SC" claims are actually worth. None of the five requires a code change; all are record/evidence repairs.

**The code segment of `/speckit.review` was not dispatched in this run** (the calling workflow scoped it to the process). Per the command's own rule, the `Implemented → Ready for Review` transition is therefore not granted by this run and § 2.1 records `not-evaluated` / `blocking-unresolved`. The closure owner must run segment 2 (or record its own triage) before the status can flip.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
