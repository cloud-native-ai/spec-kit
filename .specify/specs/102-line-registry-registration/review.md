# Specification-Driven Development (SDD) Process Review Report: 长任务 line 登记与 status 可见性（切片）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 102 |
| Requirement Key | 102-line-registry-registration |
| Requirement Name | 长任务 line 登记与 status 可见性（切片） |
| Related Feature | 088 Speckit 框架可视化（Speckit Framework Visualization） |
| Repository | spec-kit |
| Repository URL | `origin git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH remote; no HTTPS web rendering) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch has no upstream and nothing was pushed. Cite absolute paths plus `git show 13c3b10b5:<path>` instead of URLs. |
| Branch | 102-line-registry-registration |
| Commit SHA | `13c3b10b5de140d0b3ecf4d4818088e1cecfadc4` (short: `13c3b10b5`) |
| Repo Root (absolute) | `/cws_data/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-16 |
| Reviewer (Agent) | Qoder SDD review run (main orchestrator + four fresh-context read-only review units + one P0 validator) |
| Environment | Linux x86_64 (5.10.134-007.ali5000.al8), bash, CPython 3.11.0rc1, pytest 9.0.3, pytest-xdist 3.8.0, git 2.34.1, Node 26.3.0 |
| spec-kit Source Snapshot | same repository at `13c3b10b5` (self-hosting; framework hat) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 257 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/requirements.md` | 23 FR / 9 SC / RS-001…006 / 9 shared strings / A-14…A-24 |
| plan.md | 178 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/plan.md` | Constitution Check, T-001/T-002, EP-001…005, Project Structure |
| tasks.md | 300 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/tasks.md` | 57 task rows (T001–T057), Tests Mode ON, dependency order |
| research.md | 110 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/research.md` | R-01…R-13, U-1…U-5, baseline measurements |
| data-model.md | 118 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/data-model.md` | E1–E8, INV-01…INV-12 |
| quickstart.md | 206 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/quickstart.md` | S-1…S-7 (S-7 executed) |
| contracts/line-run.contract.md | 116 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/contracts/line-run.contract.md` | C-01…C-19 wrapper semantics and exit matrix |
| contracts/line-registration-scan.contract.md | 110 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/contracts/line-registration-scan.contract.md` | C-01…C-17 scanner surface, predicate, verdicts |
| contracts/wiring-surfaces.contract.md | 67 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/contracts/wiring-surfaces.contract.md` | C-01…C-13/C-15 wiring and invariant clauses |
| feature-ref.md | 61 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/feature-ref.md` | Feature 088 binding + 24-path delivery surface |
| verification.md | 90 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/verification.md` | 9 SC status rows, smoke record, joint acceptance |
| checklists/ | 121 | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/checklists/` | requirement-quality checklist (81 lines) + requirements checklist (40 lines) |
| test-evidence/ | dir | `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/test-evidence/` | stage E3 rows, red-first readings, gate and polish evidence |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements attempt 1 | `e612b341e`; U4 gate `INPUT_ERROR` — `### Runtime Stack & Dependency Ownership` missing | Yes — gate correctly refused; bounded repair dispatched |
| 2 | requirements attempt 2 | `c2944e720`; RS-001…RS-006; pre-analyze `decision=pass` | No |
| 3 | clarify | `25b242bca`; 12 findings integrated, 0 open markers, Feature 088 bound | No |
| 4 | plan attempt 1 | `ed2a71a15`; EP-001…EP-005 verified; Constitution Check 23/23 | No |
| 5 | tasks attempt 1 | `f30681a04`; 57 rows, Tests Mode ON, zero plan-owned touches | No |
| 6 | checklist | `cc54a0df1`, `d392d6ff3`; 38 items, 23 in-file defects corrected; CHK038 left open | Yes — one item left open by design |
| 7 | analyze round 1 | 3 workers; 5 HIGH; plan attempt 2 `f6ce95b01` (8 PLAN-EDITs, rebaseline) | Yes — analyze gate refused; upstream repair loop |
| 8 | analyze rounds 2–4 | `d18b3e894` tasks repair; `e0ab20bdf` plan repair 3; round 4 blocking = 0 | Yes — four rounds before the gate passed |
| 9 | implement P1–P3 | `3bbe083a9`, `49bcbcfcf`, `bffd59af6`; red-first + teeth readings | No |
| 10 | implement P4 stall (U5) | `.specify/instructions.md` 38,578 B > `INSTRUCTIONS_BUDGET_BYTES=38,400` | Yes — halt-and-report; user decision D-102-01 (`d6b491167`, 38400→38912) |
| 11 | implement P5–P6 | `a14638790`, `2faade346`; wiring, verification, gates; Status → Implemented | No |
| 12 | closure attempt 1 | 2 new failure names vs the 241-name baseline (096 guard window, live-scan write race) | Yes — closure gate refused |
| 13 | closure-repair + closure attempt 2 | `44e3636cd`; two test-isolation fixes; 241/241, `comm` both directions 0 | Yes — a bounded repair inside the implement slot |
| 14 | head refresh | `13c3b10b5`; live-scan reading timestamp only | No |

## 2. Findings Summary

Each segment keeps its own vocabulary and its own count; the three blocks below are not summed, mapped or scored together.

**Process segment** (`P0`/`P1`/`P2`, owned by `review-sdd-process`):

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 6 |
| Documentation | 1 |

**Artifact segment**: P0 0 · P1 1 · P2 4 (rows in § 2.2).
**Implementation segment**: P0 0 · P1 2 · P2 2 (rows in § 2.3).
**Code segment** (six-level family, owned by `code-review`): `blocking` 0 · `important` 2 · `suggestion` 4 · `nitpick` 1 · `question` 2 · `praise` 1 (§ 2.1 and `code-review.md`).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `cdc79cdb52c892e8ed43145860cea2cd6ffdbfdf` | `git-delta-review.sh base --spec .specify/specs/102-line-registry-registration` |
| Head commit | `13c3b10b5de140d0b3ecf4d4818088e1cecfadc4` | run-start `HEAD`, fixed for this run |
| Base source | `feature-first-commit` | the resolution tier the code skill's `base` step reported |
| Renderer mode | `text` | non-interactive agent invocation; receipt header `renderer=text` |
| Changed / judged / skipped / gap files | 124 / 11 / 113 / 0 | copied field by field from the receipt block in `code-review.md` |
| Segment verdict | `not-evaluated` | the receipt's own derivation: `skipped_files > 0` earns no coverage credit; 0 gap, 0 `blocking` |
| Gate verdict | `allow` | `report --summary --file code-review.md` → `{"blocking":0,"important":2,"suggestion":4,"nitpick":1,"question":2,"praise":1}`, `gate=allow`; the two `important` items are answered in the record |
| Reason, when one applies | not-evaluated: 113 legal skips (`generated` mirrors/copies and run outputs; `non-code-file` docs, evidence and runtime records), 0 gaps; `none` for the merge gate | `code-review.md` |
| Uncommitted scope | 14 uncommitted paths were outside the review object (12 `.specify/memory/**` runtime records and the two pre-existing untracked scripts); the receipt gives no conclusion over them; the verbatim sentence with the full path list lives in `code-review.md` | `code-review.md` |
| Record | `.specify/specs/102-line-registry-registration/code-review.md` | written because triage = `run` |
| Archive | `none` | first code-segment run for this slice |

Client capture: `capture: skipped hat=framework basis=root owns framework source directories …; triage=run` — the repository is judged framework-hat, so capture does not run and no five-value token is emitted.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/ (3), data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, test-evidence/, checklists/ — 11 members | stage rules ∪ `plan.md` § Project Structure (lines 99–108) |
| Coverage line | 11 / 11 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | one P1 acceptance-honesty finding (stale SC-009 measurement) plus four P2 rows |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/102-line-registry-registration/verification.md` | 71 | none | SC-009 records `92 / 90 / 86 / 4` and “0 unexplained”; at HEAD the same T050 pathspec reads 104 / 102 / 97 / **5**, and the fifth outside path (`tests/contract/test_sdd_observer_lifecycle.py`) is not attributable to D-102-01 (A1). |
| P2 | `.specify/specs/102-line-registry-registration/checklists/requirement-quality-2026-11-16.md` | 72 | none | CHK038 is still `open` (“建议实现前由 plan 以 minor 补一句解析基准”), while FR-013/A-21 (`requirements.md:164`) now define the repo-root shape and `--root` base (A2). |
| P2 | `.specify/specs/102-line-registry-registration/plan.md` | 99–108 | none | § Project Structure lists neither `notes/` nor `checklists/`, although T001/T008/T016/T047/T055 write into `notes/` and the checklist stage owns `checklists/` (A3). |
| P2 | `.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt` | 57–59 | none | The file asserts `final-failed.txt` is empty; at HEAD that tracked file holds the 241-name closure list, so the cited artifact and the record now disagree (A4). |
| P2 | `.specify/specs/102-line-registry-registration/verification.md` | 31–33 | none | The smoke triple was read on the pre-closure-repair tree; the scan_live test and the 096 guard were rewritten in `44e3636cd`, and the record is not annotated as superseded by `closure-repair.txt` (A5). |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `cdc79cdb52c892e8ed43145860cea2cd6ffdbfdf` | the resolved diff base (also the master tip) |
| Head commit | `13c3b10b5de140d0b3ecf4d4818088e1cecfadc4` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py tests/contract/test_line_registration_scan.py tests/contract/test_line_registration_wiring.py tests/integration/test_line_run_behavior.py tests/integration/test_line_registration_scan_live.py tests/contract/test_status_digest.py tests/contract/test_status_digest_roles.py tests/unit/test_status_digest_unit.py -q --names-out .specify/specs/102-line-registry-registration/final-failed.txt` | recorded verbatim from `verification.md:31` |
| Smoke exit code | `0` | recorded `smoke_exit_code=0`; independently re-run in this review **without** `--names-out` (to avoid rewriting the tracked names file): `153 passed in 5.45s`, rc 0 |
| Smoke evidence path | `.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt` | exists, non-empty; holds the same 153-passed reading |
| Scope and regression verdict | **scope: two P1 breaches** (FR-016 evidence mechanism withdrawn; 21 runtime records committed) and **regression: clean** — `final-failed.txt` and `baseline-failed.txt` are both 241 names, `comm -13` and `comm -23` both 0, `test_loop_state_engine.py`'s 9 failures stay inside the baseline; plan-owned files are untouched (`classification=none`, `touched_paths=[]`) | this segment's own readings plus `audit-plan-changes.py` and `closure-repair.txt` |
| Segment verdict | `blocked` | two P1 findings below |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `tests/integration/test_line_registration_scan_live.py` | 74–96 | none | The live reading is now written only under pytest `tmp_path`, with a comment saying the committed evidence is produced by the implementation stage; FR-016 (`requirements.md:167`) still requires the reading to be recorded to `test-evidence/` by the test through the unique entry, so the committed reading can no longer be reproduced by the smoke (I1). |
| P1 | `.specify/memory/exec-quant/records/`, `.specify/memory/feedback/`, `.specify/memory/session/` | n/a (file set) | the defect is a set of added files, not one diff hunk | 21 `.specify/memory/**` runtime records were committed by `2ebb46308`, `074bf5cc1`, `23da7469d`, `2b4fc2467`, `1175d066a` and `96c2768e9`, and `20261112T074632Z-…-b101.md` (a 101 record) was mutated; the run's own checkpoints repeatedly claim “未提交 `.specify/memory/**`”. The directive for this run forbids committing them (I2). |
| P2 | `.specify/specs/102-line-registry-registration/test-evidence/polish-scope.txt` | 24–27 | none | The T050 counts `92 / 90 / 86 / 4` no longer reproduce: the same pathspec at HEAD reads 104 / 102 / 97 / 5, and the full committed delta (no pathspec) reads 124 changed files with 27 outside the 24 declared paths (I3). |
| P2 | `.specify/specs/102-line-registry-registration/verification.md` | 33 | none | The smoke's `--names-out` target (`final-failed.txt`) has since been overwritten by the closure full run (0 → 241 names); re-running the recorded command verbatim would rewrite a tracked evidence file (I4). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/features.md` row 102 |
| `final_path` record, copied verbatim (7/7) | pass 3 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 3 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/102-line-registry-registration --json` (exit 0), never recomputed here |
| Comparison verdict | `agree` | the checker's verdict is `accept`; the claim is `Implemented`; the `pass` bucket is 3, not 0 |
| Failed condition, on refusal | none — no refusal fires on this record | `completion_conditions`: `every_final_path_pass: true`, `no_open_rows: true`, `smoke_record_pass: true`, `status_row_per_criterion: true`; `reasons: []` |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 3 |

## Status Transition — judged once, granted

The transition judged here is `Implemented → Ready for Review`; its four conjunctive conditions are owned by `templates/feature-details-template.md` § Canonical Status State Machine and are cited, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | `tasks.md`: 57 closed / 0 open; `deferred_tasks=` empty in `verification.md` | satisfied |
| (b) review evidence produced | this report and `code-review.md` are on disk; `test-evidence/review.jsonl` records the run | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `code-review.md` carries 0 `blocking`; `report --summary --file` exits 0 with `gate=allow`; both `important` items are answered in the record | satisfied |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 3 `pass`, 0 in every non-pass bucket (SC-001/002/003) | satisfied |

**The four conditions hold, so the transition is granted.** The artifact and implementation segments are `blocked` on P1 findings, but none of those P1s is one of the four conditions, so they are carried to a bounded repair rather than holding the flip. **Named limitation L-1**: this run does not write the registry row; its directive limits the commit to `review.md` and review evidence, so the one-line `.specify/features.md` flip (`Implemented → Ready for Review`) is left to the driver's close-out and must be executed there before `/speckit.seal`.

## 3. Findings (Problems & Improvement Targets)

### F01 — The dispatch carrier's evidence envelope omits `run=`, so the watcher classifies it `unattributed`

- **Severity**: P1 (`validated: downgraded` — the independent validator confirmed the evidence and refused P0 because the failure is loud, named and has a documented bypass)
- **Category**: Automation / Scripts
- **Location**: `/cws_data/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/stage-runner.sh:230,231,392`; contract `/cws_data/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/stage-prompts.md:323`; consumer `/cws_data/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/watch-target.sh:401`
- **Evidence** (verbatim quote):

  ```text
  atomic_write "$pidf" "pid=$runner_pid start=$start_token at=$(now_epoch) line=$LINE stage=$STAGE event=pid"
  status / pid / heartbeat 行尾携带 `line=<id> run=<id> stage=<stage> event=<type>`；
  CC="unattributed"; return 0
  ```

- **Why it's a problem**: the producer writes three envelope lines without `run=`, the consumer treats a missing carrier run as `unattributed` and discards the live PID. Every dispatch's first watch window falsely reads `NO_SIGNAL`, and the driver has to hand-patch evidence files. The validator's live stub also showed that a successful stage (`exit=0 sentinel=1`) still collapses to `NO_SIGNAL`, so the impact is broader than the first window.
- **Proposed fix**: add `run=$RUN` to all three writes (pid/heartbeat/status) and add one producer→consumer test that runs the watcher against a real runner-written envelope; `run-stage.sh` already writes the field and is the model.

### F02 — The requirements/plan authoring templates carry no pointer to the Runtime Stack / Execution Premises owners

- **Severity**: P1
- **Category**: Template
- **Location**: `/cws_data/cloud-native-ai/spec-kit/templates/commands/requirements.md` (whole file) and `/cws_data/cloud-native-ai/spec-kit/templates/commands/plan.md` (whole file); owners at `/cws_data/cloud-native-ai/spec-kit/.specify/shared/workflow/acceptance-hardening.md:315,392`; gate at `/cws_data/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:316,317`
- **Evidence** (verbatim quote):

  ```text
  RUNTIME_SECTION = re.compile(r"^#{2,4}\s+Runtime Stack & Dependency Ownership")
  PREMISES_SECTION = re.compile(r"^#{2,4}\s+Execution Premises\s*$")
  ```

  A `grep` for “Runtime Stack” and “Execution Premises” over `templates/commands/` returns zero hits.
- **Why it's a problem**: for an `execution` line the pre-analyze gate hard-requires both sections, but the command templates the author reads never mention them; the requirements stage failed its first U4 with `INPUT_ERROR` for exactly this reason and needed a bounded repair.
- **Proposed fix**: add one pointer line to each template naming `acceptance-hardening.md` § Runtime Stack & Dependency Ownership and § Execution Premises, with no restatement of the row shape.

### F03 — `[green:]` is optional in the tasks template but mandatory for shared test files in the create-tasks skill

- **Severity**: P1
- **Category**: Template
- **Location**: `/cws_data/cloud-native-ai/spec-kit/templates/tasks-template.md:110`; conflicting rule `/cws_data/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md:339`
- **Evidence** (verbatim quote):

  ```text
  - **[green: <contract>#<clause>]** (optional, repeatable): green-point attribution tag
  Declare the partition with the `[green: <contract>#<clause>]` attribution tag … (shared test files)
  ```

- **Why it's a problem**: this line's wiring test is shared by US3 and US4, so the skill required the tag; the template says a row may declare none. The run omitted the tag and validated clean, so the validator could not judge the cross-phase divergence the skill wanted it to catch.
- **Proposed fix**: make the tag mandatory when two verification rows share a test path, and make `validate-tasks.py` report an ERROR (not a silent pass) for that shape.

### F04 — The test runner's serial branch still passes `-n0` to pytest

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/cws_data/cloud-native-ai/spec-kit/scripts/bash/run-tests.sh:205`
- **Evidence** (verbatim quote):

  ```text
  else
      MODE_ARGS=(-n0)
      MODE_NOTE="reason=$SERIAL_REASON"
  fi
  ```

- **Why it's a problem**: without pytest-xdist the runner reports `mode=serial reason=no-xdist` but still passes `-n0`, which bare pytest rejects with a usage error (rc 4). This line hit it at tasks stage and “fixed” it by installing xdist into the environment, so the framework defect remains for any checkout without the dev extras.
- **Proposed fix**: in the serial branch use an empty `MODE_ARGS`, and add a no-xdist unit test that asserts a serial invocation succeeds.

### F05 — The process record repeatedly claims `.specify/memory/**` was not committed; the git history shows it was

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/state/102-line-registry-registration.md:340` (same sentence repeats at 349, 367, 378, 388); commits `2ebb46308`, `074bf5cc1`, `23da7469d`, `2b4fc2467`, `1175d066a`, `96c2768e9`
- **Evidence** (verbatim quote):

  ```text
  - 纪律：未改 plan-owned 工件（`git diff --stat` 仅 tasks.md 13 行勾选）；未提交 `.specify/memory/**`；既有未跟踪 `.specify/scripts/{line-registry.py,stage-runner.sh}` 未提交未还原。
  ```

  `git diff --name-status cdc79cdb5..HEAD -- .specify/memory` shows 21 `A` rows plus one `M` row.
- **Why it's a problem**: every stage close-out asserted a discipline the commits did not keep, so a reader of the spine has a false picture of what the branch contains. The same fact is judged as scope in I2; here the defect is the record's truthfulness.
- **Proposed fix**: make the stage close-out derive the “uncommitted” sentence from `git status`/`git diff` instead of typing it, and add a close-out check that fails when the claim and the tree disagree.

### F06 — The closure full-suite slot was consumed twice in the implement stage, and the refusing run is not in the E2 ledger

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/state/102-line-registry-registration.md:381–390`; `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/test-evidence/closure-repair.txt`; test-budget block in the same spine file (2 rows: `baseline`, `closure`)
- **Evidence** (verbatim quote):

  ```text
  - 断点：closure 全量相对基线新增 2 条失败；仅修两处测试隔离/守卫窗口…
  - closure in-slot 重跑：`bash scripts/bash/run-tests.sh --full …` → rc 1 … 241 failed / 8974 passed / 6 skipped
  ```

  `audit-test-budget.py` reads `slots=baseline:1 closure:1 reruns=0`.
- **Why it's a problem**: the first closure run is the one that found the two regressions, but only the post-repair run is recorded; the audit cannot see a rerun (`reruns=0`), so the budget/evidence ledger looks cleaner than the run was. A later closure consumer cannot tell which reading justified the repair.
- **Proposed fix**: record every full-suite invocation as its own E2 row with a `slot=closure attempt=<n>` field, and make the audit compare the count of full runs against the recorded rows.

### F07 — The analyze stage left no stage-status/E3 evidence, and the driver's own completeness audit fails at HEAD

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/test-evidence/` (no `analyze*.jsonl`); audit command below
- **Evidence** (verbatim quote):

  ```text
  $ python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine .specify/state/102-line-registry-registration.md --spec-dir .specify/specs/102-line-registry-registration
  slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=3 environment_failures=0
  stages=6 complete=3
  status=fail
  reason=checklist: stage-status evidence is incomplete (unknown)
  reason=analyze: stage evidence file missing; counted in the completeness denominator (unknown)
  reason=review: stage evidence file missing; counted in the completeness denominator (unknown)
  ```

- **Why it's a problem**: four analyze rounds (ten worker executions) produced merged reports and runtime memory records but no stage-status evidence row; the checklist row is also incomplete. The review row is expectedly missing mid-review, but the other two are not.
- **Proposed fix**: emit one E3 stage-status row per stage boundary (including read-only analyze), and run the audit at each stage close instead of only at closure.

### F08 — The state spine has two writers: a U4 block appears twice and one is filed under the wrong stage

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/state/102-line-registry-registration.md:173–183` vs `:93–101`; `:164` vs `:235`
- **Evidence** (verbatim quote):

  ```text
  ## U2 派发记录 — analyze 第 2 轮（修复后全量复检，2026-11-16T10:00Z）
  …
  - U4 门禁（attempt 2，2026-11-16T08:43Z）：validate-requirements.py status=ok（0 error / 0 warning；228 lines / 32 definition rows / 8 shared strings）
  ```

- **Why it's a problem**: an 08:43Z requirements gate reading sits under the 10:00Z analyze section, and the same plan/tasks U4 verdicts appear both as their own block and as a later “attempt 2” duplicate. Stage history is no longer linear or machine-trustworthy.
- **Proposed fix**: single writer for the spine (the driver), append-only sections keyed by stage+attempt, and a duplicate-heading check at write time.

### F09 — The plan stage does not pre-run the instructions size budget, so the conflict surfaced only after three packages had landed

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/state/102-line-registry-registration.md:351–357`; budget owner `/cws_data/cloud-native-ai/spec-kit/scripts/bash/generate-instructions.sh:107`
- **Evidence** (verbatim quote):

  ```text
  - 现象: C-07 要求的逐字 bullet 277 B，使 .specify/instructions.md = 38,578 B，超 INSTRUCTIONS_BUDGET_BYTES=38,400（最后可接受 38,399）179 B；…
  ```

- **Why it's a problem**: the plan declared a verbatim bullet that pushes the live instructions file over budget, but no plan-stage gate measured the projected size; the stall appeared in P4 after P1–P3 were committed and required a user decision to raise the constant.
- **Proposed fix**: add a plan-stage preflight that renders the instruction template with the planned ambient bullet and compares against `INSTRUCTIONS_BUDGET_BYTES` before the plan is approved.

### F10 — The closing targeted set cannot see full-tree or HEAD-window guards, so the closure stage discovered two new failures

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt:70–76`; closure reading `/cws_data/cloud-native-ai/spec-kit/.specify/specs/102-line-registry-registration/test-evidence/closure-repair.txt`
- **Evidence** (verbatim quote):

  ```text
  `final-failed.txt` is empty, so the difference set is 0 by construction: this run added no failure name.
  ```

- **Why it's a problem**: both closing failures came from guards that read the whole tree or a `base..HEAD` window (the 096 carrier window and a corpus-stability race), which an eight-file targeted set can never exercise. The implement stage was green while the closure slot was red, and the gap was discovered only by spending the closure budget.
- **Proposed fix**: add a “full-tree guard” lane to the targeted-set recipe — at least the HEAD-window and corpus-stability guards — or record explicitly that targeted readings cannot speak for them.

### F11 — The spine's last disclosure describes a working-tree state that a later commit already changed

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/cws_data/cloud-native-ai/spec-kit/.specify/state/102-line-registry-registration.md:389`
- **Evidence** (verbatim quote):

  ```text
  - 披露：`test-evidence/line-registration-scan-live.txt` 工作区有仅时间戳差异的未提交改动（attempt 1 closure 全量运行于隔离修复前写出的 11:39:04Z 读数）；按「保留不动」未提交、未还原。
  ```

  `git status --porcelain` at review time lists no such modification; `13c3b10b5` is titled “refresh the live scan reading timestamp after the closure repair”.
- **Why it's a problem**: the spine's final state tells the next reader to preserve an uncommitted change that has since been committed, so its working-tree picture is one commit stale.
- **Proposed fix**: re-read `git status` at each stage return and rewrite the disclosure line; never carry a working-tree claim across a commit.

## 4. What Worked — Preserve (Brief)

- **Decision tension with a named counter-metric**: D-102-01 recorded the antithesis (shorten the bullet), the discriminating evidence, the anti-metric and the reopening condition in `.specify/register.md`.
- **Red-first with real teeth**: `notes/red-first-evidence.md` plus `us2-teeth.txt` and `us4-injections-full.txt` carry red runs, injections, exit codes and sha256 restores.
- **Name-level regression comparison**: `baseline-failed.txt` / `final-failed.txt` compared with `comm` in both directions, never by count alone.
- **Zero-machinery audit**: T051's `polish-zero-machinery.txt` shows no scheduler, timer, daemon, second registry or second spine.
- **Fresh-context recitation for SC-008**: a reader outside the feature answered both knowledge questions correctly (`sc008-recitation-2026-11-16.txt`).
- **Mirror parity by generator**: four touched pairs read `ok`; mirrors were projected, never hand-edited.

## 5. spec-kit / SDD Improvement Recommendations

No new `REC-…` identifier is coined this round; each recommendation is named by its source finding, so no register row is owed. Targets are repo-relative, with an absolute supplement where useful.

### 5.1 Template Improvements

- **Add owner pointers for the runtime-stack and premises sections** — Target: `templates/commands/requirements.md` and `templates/commands/plan.md` (absolute: `/cws_data/cloud-native-ai/spec-kit/templates/commands/`). Change: one pointer line each to `shared/workflow/acceptance-hardening.md` § Runtime Stack & Dependency Ownership and § Execution Premises. Source: F02. Expected impact: first-pass execution-class requirements stop failing U4 with `INPUT_ERROR`.
- **Make `[green:]` mandatory for shared test files** — Target: `templates/tasks-template.md:110` and `scripts/python/validate-tasks.py`. Change: require the tag when two rows share a test path; report an ERROR for the untagged shape. Source: F03. Expected impact: the validator can actually judge the divergence the skill describes.

### 5.2 Command Prompt Improvements

- **Teach the implement close-out to derive its discipline sentence** — Target: `templates/commands/implement.md` § close-out. Change: print the “uncommitted” line from `git status` and fail when a claimed-uncommitted path is in the commit. Source: F05. Expected impact: the spine stops asserting disciplines the branch did not keep.
- **Register the full-suite slot discipline** — Target: `templates/commands/implement.md` § test budget. Change: one E2 row per full-suite invocation with `attempt=<n>`. Source: F06. Expected impact: the audit can see reruns.

### 5.3 Automation / Script Improvements

- **Complete the dispatch envelope** — Target: `skills/external/sdd-loop-driver/scripts/stage-runner.sh`. Change: add `run=$RUN` to the pid/heartbeat/status writes; add a producer→consumer contract test. Source: F01. Expected impact: no more false `NO_SIGNAL` first windows.
- **Fix the serial runner branch** — Target: `scripts/bash/run-tests.sh:205`. Change: empty `MODE_ARGS` when serial; add a no-xdist unit test. Source: F04. Expected impact: the unique test entry works on a bare checkout.
- **Complete the instructions raise record** — Target: `scripts/bash/generate-instructions.sh:106`. Change: record the 38912 raise (old/new/measured/reason/rule) beside the existing 36864 and 37888 records. Source: code-review `suggestion` item 5. Expected impact: the constant is self-explanatory in its own file.
- **Fail closed on unreadable judged files** — Target: `scripts/python/line-registration-scan.py:127`. Change: treat an unreadable judged file as an input error (exit 2) or a named skip, never as clean. Source: code-review `suggestion` item 8. Expected impact: the scanner's clean reading means what it says.

### 5.4 Workflow Improvements

- **Run one stage-status audit per stage boundary** — Target: `shared/workflow/` stage close-out procedure. Change: emit the E3 row and run `audit-test-budget.py --stage-check` at every stage, analyze included. Source: F07. Expected impact: completeness is known before closure, not after.
- **Add a full-tree guard lane to the targeted recipe** — Target: `shared/guidelines/test-execution-efficiency.md` (or the implement close-out recipe). Change: name the HEAD-window and corpus-stability guards as mandatory in a closing targeted set. Source: F10. Expected impact: closure stops discovering guard-only regressions.
- **Preflight the instructions budget at plan time** — Target: `templates/commands/plan.md` § pre-plan gate. Change: render the planned ambient bullet and compare with the budget. Source: F09. Expected impact: the U5 stall class is decided in planning, not after three packages.
- **Single-writer state spine** — Target: `shared/workflow/` state-spine procedure. Change: driver-only writer, stage+attempt keyed append, duplicate-heading check, working-tree disclosure refreshed at every return. Source: F08, F11. Expected impact: the spine remains a linear, trustworthy history.

### 5.5 Documentation Improvements

- **Say what the review's smoke command writes** — Target: `templates/commands/review.md` § smoke record. Change: require the smoke command to write names to a review-scoped path, not the feature's tracked closure file. Source: I4. Expected impact: re-running the smoke cannot rewrite committed evidence.
- **State the memory-record boundary in the implement close-out** — Target: `docs/reference/skills/memory.md` (or the implement close-out doc). Change: name `.specify/memory/**` as never-committed runtime storage and point at the guard. Source: I2, F05. Expected impact: the rule is reachable where the executor reads it.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Remove/revert the committed `.specify/memory/**` records and restore the mutated 101 record; add a commit-scope guard | `.specify/memory/**`, implement close-out | I2, F05 |
| P1 | Re-run the T050 scope audit at final HEAD and update SC-009 (104/102/97/5; full delta 27 outside) | `verification.md`, `polish-scope.txt` | A1, I3 |
| P1 | Reconcile FR-016 with the tmp_path isolation (env-gated `test-evidence` write or requirement amendment) | `requirements.md`, live test | I1 |
| P1 | Complete the dispatch envelope (`run=`) and add a producer→consumer test | `stage-runner.sh` | F01 |
| P1 | Fix the serial runner and add a no-xdist test | `run-tests.sh` | F04 |
| P1 | Add runtime-stack/premises pointers to the requirements/plan templates | `templates/commands/` | F02 |
| P1 | Make `[green:]` mandatory for shared test files | `tasks-template.md`, validator | F03 |
| P2 | One E2 row per full-suite run; per-stage status audit | `implement.md`, driver audit | F06, F07 |
| P2 | Annotate superseded smoke/scope evidence; refresh spine disclosures | `verification.md`, state spine | A3–A5, F08, F11 |
| P2 | Plan-stage instructions-budget preflight | `plan.md` | F09 |
| P2 | Add a full-tree guard lane to the closing targeted set | test-execution guidance | F10 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says “see attached”, “as discussed earlier”, or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file or subsystem and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.** The one P0 candidate (F01) was dispatched to an independent read-only validator, which confirmed the evidence and downgraded it to P1 because the failure is loud, named and has a documented bypass.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
