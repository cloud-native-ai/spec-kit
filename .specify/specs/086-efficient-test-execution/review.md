# Specification-Driven Development (SDD) Process Review Report: 测试高效执行（默认并发）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 086 |
| Requirement Key | 086-efficient-test-execution |
| Requirement Name | 测试高效执行（默认并发） |
| Related Feature | 086 Efficient Test Execution (Concurrent by Default) |
| Repository | spec-kit |
| Repository URL | `gitlab` remote only: `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH, not HTTPS-web-accessible) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the 31 feature commits are unpushed and live only in this checkout. Every citation below is an absolute path or a repo-relative path resolved against `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`; recover any cited blob with `git show a0426644:<path>` |
| Branch | 086-efficient-test-execution |
| Commit SHA | a0426644f9ad0520cdc75cb9273621de8e66f7f7 (short: a0426644) |
| Repo Root (absolute) | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | spec-kit review stage executor (`/speckit.review`, unattended SDD loop) |
| Environment | macOS 25.6.0 arm64, 18 logical CPUs, bash 5.x; CPython 3.14.6 (`.venv`), pytest 9.2.0, pytest-xdist 3.8.0; every measured command run under `env -u PYTHONPATH` per requirements A20 |
| spec-kit Source Snapshot | this repository at `a0426644` (self-hosting: framework source and client runtime in one tree) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 334 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/requirements.md | 33 FR / 12 SC / 7 STR / 20 assumptions; the review's contract with the delivery |
| plan.md | 339 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/plan.md | 9 work packages, 10 execution premises, 3 decision tensions, inherited-blocker row |
| tasks.md | 338 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/tasks.md | 56 closed rows, DoD-1…DoD-6, nine completion gates, 19 mutation-leg carriers |
| contracts/ (4 files) | 1048 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/contracts/ | C-001…C-052, each claimed by exactly one `[green:]` carrier row |
| data-model.md | 199 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/data-model.md | 10 entities, 22 validation rules, 3 state machines |
| quickstart.md | 196 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/quickstart.md | S-0 executed pre-flight plus S-1…S-8 scenarios |
| verification.md | 90 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/verification.md | Flat `SC-NNN_status=` rows, two full-run slots, the single smoke record |
| feature detail 086 | 139 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/086.md | Claims `Implemented`; carries the disclosed limitations this review adjudicates |
| test-evidence/ (28 files) | — | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/test-evidence/ | Baseline, closure, mutation legs, dogfood, mirror parity, budget ledger |
| checkpoints/ (12 files) | — | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/checkpoints/ | Per-stage 085 checkpoint records 01–12 |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Branch scaffolded, then a `087-` branch was briefly created and discarded | `requirements.md` A19(a): "requirements 阶段的 scaffold 曾短暂创建 `087-` 分支，随后清理并以正确的 `086` 分支重建" | Yes — recorded as a framework observation the feature does not repair |
| 2 | `/speckit.requirements` + U4 verification, checkpoint 01 | `2a88a9e7`, `3afe10df` | None |
| 3 | `/speckit.clarify` Mode A, binds Feature 086 without a new id | `fee3f874`, `554d8333`, checkpoint `02-clarify.md` | None |
| 4 | `/speckit.plan`; registry flipped `Draft → Planned` | `67bbae51`, checkpoint `03-plan.md` | None |
| 5 | Temporary Team created at plan close (085 timing) | `0f4b203e` | None |
| 6 | `/speckit.tasks`, `/speckit.checklist`, `/speckit.analyze` | `f3105c98`, `5cbc757b`, `d9033981` | None |
| 7 | Analyze blocker C-01 repaired by a separate fix pass | `9496090b`; `test-evidence/analyze-findings.md` — FR coverage 30/33 restored to 33/33 | Yes — the repair ran as a driver-owned fix pass, not a re-run of the authoring stage |
| 8 | T050 baseline slot taken; then a **corrective** baseline-provenance commit | `f3279c6e`, `ed9dad97` ("correct the implement wave") | Yes — T050 was placed at the head of Phase 1 by an amendment after the first wave had been recorded |
| 9 | Implement waves A1/A2/A3/A4/B1/B2/B3 | `bd241323`, `3540c7f5`, `01cc8da8`, `58d30bde`, `dfe27809`, `f12b554d`, `1d962bfb` | None |
| 10 | Wave C1: serial marker, nested-run case, then a `--dist` guard repair | `05ae56ca`, `bf455401`, `018b0455` | Yes — the `--dist` caller guard (FR-004/FR-019 boundary) was found mid-wave and fixed as a new commit |
| 11 | Wave C2 first attempt: sandbox `git worktree` **inside the repo root** contaminated the closure run | `test-evidence/closure-diff.txt` § Run ledger row 1: `21 failed, 7533 passed, 7 skipped in 271.72s` | Yes — a process defect by the feature's own executor; disclosed and re-run, no extra slot spent |
| 12 | Wave C2 closure: clean re-run, 085 carve-out, verification log, nine gates, `Implemented` flip | `93e61050`, `d30bfadf`, `a0426644` | None |
| 13 | Feature flipped to `Implemented` on the checker's `accept` verdict, contradicting a pre-written `Blocked` premise | `.specify/memory/features/086.md` § 当前状态裁定: "裁决前本文件与 `features.md` 曾按预期先写成 `Blocked`" | Yes — a prediction was written as a status before the verdict existed |
| 14 | `/speckit.review` (this run): four segments plus the Acceptance Reality Check | `code-review.md` coverage receipt: 113 changed / 113 judged / 0 skipped / 0 gap | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 8 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. F1, F2, F5, F6, F7, F9, F10, F11. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. F3, F4, F8, F12, F13. |

| Category | Count | Finding ids |
|----------|------:|-------------|
| Template | 1 | F10 |
| Command Prompt | 1 | F5 |
| Automation / Scripts | 5 | F3, F7, F8, F11, F13 |
| Workflow | 3 | F1, F2, F6 |
| Documentation | 3 | F4, F9, F12 |
| **Total** | **13** | |

P0 validation status: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 24cb4edcc53db3cfc86f574e5e6d627c78b2ca08 | the resolved diff base |
| Head commit | a0426644f9ad0520cdc75cb9273621de8e66f7f7 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit (`start`); the `receipt` re-resolution reported `trunk-merge-base` and resolved to the same commit | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker (no TTY, non-interactive agent run) |
| Changed / judged / skipped / gap files | 113 / 113 / 0 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | pass | one of the four closed values the `code-review` skill owns |
| Gate verdict | allow | `report --summary --file code-review.md --format json` → `"gate":"allow"`, exit 0; the red path was probed once on a scratch copy and returned `"gate":"deny"`, exit 1 |
| Reason, when one applies | none | mandatory for `not-applicable` / `not-evaluated`; `none` otherwise |
| Uncommitted scope | none — `git status --porcelain` reports 0 entries before and after this run; nothing was left unreviewed | disclosed, never concluded over; the same sentence lives in `.specify/specs/086-efficient-test-execution/code-review.md` |
| Record | `.specify/specs/086-efficient-test-execution/code-review.md` | written because the triage value is `run` |
| Archive | none | first run for this feature |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The findings themselves live in `.specify/specs/086-efficient-test-execution/code-review.md` and are read there. Counts are `blocking 0 · important 2 · suggestion 1 · nitpick 0 · question 1 · praise 0`; both `important` items are answered in § 3 (F10, F11).

Client capture: not run — this repository is judged the **framework hat** by `.specify/shared/definitions/dogfooding-definitions.md` § 2.1 (root owns `templates/`, `skills/`, `shared/`, `scripts/`, `src/specify_cli`), so the capture step printed `capture: skipped hat=framework basis=root owns framework source directories … triage=run` and wrote zero entries. The five-token capture vocabulary does not apply to a framework-hat run; the hat verdict is this line's basis.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, checklists/, test-evidence/, checkpoints/, goal/, team/ | union of the slice's stage rules and `plan.md` § Project Structure's declared tree; each of the four extra members beyond the standard seven is declared at `plan.md` line 126 (`research.md`), 128–133 (`feature-ref.md`, `test-evidence/`, `checkpoints/`, `goal/`) and 128 (`team/` via WP-C0's temporary Team) |
| Coverage line | 13 / 13 | present members / expected members |
| Missing members | none | every declared member resolves on disk and is non-empty |
| Segment verdict | pass | one of `pass`, `blocked`, `not-applicable` or `not-evaluated` |

Per-member verdict rows: one row per expected member, in the row table below, immediately after the findings table. Line references for traceability sampling are inside those rows.

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | .specify/specs/086-efficient-test-execution/requirements.md | 219 | none | SC-003's proposition is read on the shipped template layer, not on the rendered artifact it names — a `final`-path criterion whose acceptance record measures a weaker surface than its own text (F1) |
| P1 | .specify/specs/086-efficient-test-execution/tasks.md | 22 | none | DoD-2's "met" verdict closes a gate over a carrier map whose named evidence files did not exist at the time; the reading was backfilled afterwards and the row does not separate "applied by the carrying row" from "reconstructed later" (F2) |
| P2 | .specify/specs/086-efficient-test-execution/tasks.md | 143 | none | T032's `[green]`-free row delegates SC-003 to the template layer while the criterion names the rendered files — the delegation is stated in `downstream-init.txt` but nowhere in the artifact chain (F3) |
| P2 | .specify/specs/086-efficient-test-execution/test-evidence/downstream-init.txt | 90 | none | The evidence file describes the init outcome in a form that no longer reproduces at this HEAD, and does not say which of the two shipped template copies the init consumed (F12) |
| P2 | .specify/specs/086-efficient-test-execution/verification.md | 36 | none | SC-003's `_value` asserts a delivery on the template layer while the criterion text names `.specify/instructions.md`, which the run records as absent at init (F3, same defect read on the second carrier) |

| Member | Verdict | Evidence anchor |
|--------|---------|-----------------|
| requirements.md | pass | 33 FR / 12 SC / 7 STR; every SC carries a `**Path**` marker (line 217 onward); A20 declares the measurement environment |
| plan.md | pass | § Project Structure declares the full artifact tree (lines 122–134); § Work Packages fixes the write/forbid sets |
| tasks.md | pass (two P1/P2 findings above) | 52 `#C-` ids each claimed exactly once; 19 legs each with one carrier; Completion Gate GATE-086 + GATE-1…8 |
| contracts/ | pass | C-001…C-052 contiguous, no duplicate claim, no orphan `[green:]` |
| data-model.md | pass | E-1…E-10, V-1…V-22, SM-1…SM-3 referenced from `plan.md` and T007 |
| quickstart.md | pass | S-0 records executed commands with output; S-1…S-8 route (b) with named tests |
| verification.md | pass (one P2 finding above) | 12 `SC-NNN_status=` rows; both slots; one smoke record |
| research.md | pass | B-1…B-9 measured baseline; R-1…R-10 decisions |
| feature-ref.md | pass | 21-row delivery surface mapped to FRs |
| checklists/ | pass | 44 items, each with a `Req §` or `Gap` owner |
| test-evidence/ | pass | every pointer target named by `tasks.md` § Mutation Leg Carriers resolves and is non-empty |
| checkpoints/ | pass | 12 records, each naming carrier, concurrency and completion state |
| goal/, team/ | pass | bound pair; `goal.md` and `team.md` cross-reference; requested 24 / effective 18 recorded |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 24cb4edcc53db3cfc86f574e5e6d627c78b2ca08 | the resolved diff base |
| Head commit | a0426644f9ad0520cdc75cb9273621de8e66f7f7 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier `git-delta-review.sh base` reported |
| Smoke command | `env -u PYTHONPATH SPECKIT_PYTHON=/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.venv/bin/python bash scripts/bash/run-tests.sh tests/contract/test_run_tests_runner_contract.py tests/contract/test_test_execution_efficiency.py tests/unit/test_audit_test_budget.py -q` | recorded verbatim from `verification.md` line 18, executed in this run |
| Smoke exit code | 0 | the integer the command returned (`84 passed in 8.63s`); `passes=1`, no serial exception in the selection |
| Smoke evidence path | `.specify/specs/086-efficient-test-execution/test-evidence/smoke-086.txt` | exists and is non-empty (1,662 B, records `exit code: 0` and the verbatim run) |
| Scope and regression verdict | pass with two disclosed readings — the delta is inside the declared work-package write sets (113 files, 0 outside), the closure name diff is empty in both directions (re-measured this run), and the two readings that do **not** fully satisfy their requirement's text are F1 (SC-003) and F10 (pointer form) | the segment's own reading of scope and regression |
| Segment verdict | pass | one of `pass`, `blocked`, `not-applicable` or `not-evaluated` |

This run's targeted confirmation of the closure claim (a two-file name diff and line count, not a suite run):

```
$ wc -l test-evidence/baseline-failed.txt test-evidence/final-failed.txt
  19 …/baseline-failed.txt
  19 …/final-failed.txt
$ comm -13 <(sort -u baseline-failed.txt) <(sort -u final-failed.txt)     -> empty
$ comm -23 <(sort -u baseline-failed.txt) <(sort -u final-failed.txt)     -> empty
$ env -u PYTHONPATH SPECKIT_PYTHON=…/.venv/bin/python bash scripts/bash/run-tests.sh \
      tests/contract/test_run_tests_runner_contract.py \
      tests/contract/test_test_execution_efficiency.py \
      tests/unit/test_audit_test_budget.py -q
# test runner: … -m pytest -n auto --dist load … -q
# test runner: mode=parallel workers=auto dist=load passes=1
84 passed in 8.63s        (exit 0)
```

No full suite was run by this review: the T047 closure slot already records the feature's last full run (`19 failed / 7535 passed / 7 skipped in 284.12 s` plus the serial exception pass `1 passed / 7561 deselected in 35.22 s`), and re-running it would spend a third slot to re-measure a reading this run could verify by name diff.

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | scripts/bash/run-tests.sh | 285 | none | The two-pass status composition rule ("combined code is non-zero iff a pass FAILED") is pinned by a contract case only on the `--names-out` path; the plain `-q` path implements the same rule in a separate branch that no case exercises, so a hand run composes its exit code by a rule nothing tests. No recorded reading is affected — every measured run used `--names-out` (F13) |
| P2 | .specify/scripts/bash/run-tests.sh | 285 | none | The mirror carries the identical branch by byte-identity (C-016); naming it here so the repair of F13 is not applied to one carrier only |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Implemented | `.specify/memory/features/086.md`, copied |
| `final_path` record, copied verbatim (7/7) | pass 8 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 8 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/086-efficient-test-execution --repo . --feature-detail .specify/memory/features/086.md --feature-registry .specify/memory/features.md --json`, never recomputed here |
| Comparison verdict | agree | the checker returned `"verdict": "accept"` with `"reasons": []`, `"waived": []`, and all four completion conditions `true`; the claim `Implemented` agrees with that verdict, no `F-ACCEPTANCE` item fires |
| Failed condition, on refusal | none — not a refusal | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — A `final`-path criterion is accepted on a weaker surface than its own text names

- **Severity**: P1
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/requirements.md#L219

- **Evidence** (verbatim quote):

  ```
  - **SC-003**: 在临时目录用 CLI 初始化的新项目里，生成的 constitution 与 instructions 中都能检出该原则、其 owner 指南指针（[[STR-003]]）与文件名（[[STR-001]]），读者不需要读本仓即可理解原则适用范围。**Path**: final
  ```

  against the record that moves it, `test-evidence/downstream-init.txt`:

  ```
  The generated tree at `ds086/.specify/` carries **templates**, not a pre-filled constitution: the
  generated `.specify/memory/constitution.md` is the two-line placeholder … and `.specify/instructions.md`
  is not generated at init time at all.
  ```

- **Why it's a problem**: the criterion says the principle is found in the **generated** `constitution.md` and `instructions.md`; the acceptance reading greps `.specify/templates/*-template.md` instead, because at init the named files are empty. The substitution is honestly disclosed, but the criterion was never re-worded to match it, so a `final` gate passes on a surface its own text does not name — the exact shape "acceptance honesty" exists to catch. A reviewer reading only the artifact chain cannot see that the measured surface differs from the stated one.
- **Proposed fix**: either (a) widen T032 into a full render — run `/speckit.constitution` and `/speckit.instructions` in the initialised project and grep the rendered files, which is what the criterion says; or (b) re-word SC-003 in `requirements.md` to name the shipped template layer explicitly and record the substitution as the criterion rather than as a note. (a) is preferable: it costs one stage in a temp directory and removes the reader-independence question entirely.

### F2 — The mutation-leg carrier map was "met" before its evidence existed, and the backfill was not recorded as a red-first event

- **Severity**: P1
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/tasks.md#L22

- **Evidence** (verbatim quote):

  ```
  **DoD Status**: met (DoD-1…DoD-6). … Disclosed while closing it: the carrier map named `test-evidence/ledger-parallel-flags.txt` before that file existed, and M-2/M-3/M-4/M-10…M-15 had carriers but no recorded reading; both gaps were closed by producing the readings on doctored copies outside the repo root, never by weakening a carrier and never by editing a tracked file. No DoD row is void.
  ```

- **Why it's a problem**: `notes/red-first-evidence.md` and the two evidence files named by the original carrier map were the only recorded proof that a mutation leg discriminated; for 11 of the 19 legs that proof was produced **after** the DoD had been declared satisfied and after implement had already closed its rows. The backfill itself is competent (I re-read `test-evidence/mutation-legs-runner.txt`: each M-leg is paired control/mutant, and § 4 proves in-memory mutation never writes a tracked file). The process defect is different: a carrier map is treated as a plan of record whose existence can be asserted independently of its readings, so "every leg has a carrier" reads as "every leg was exercised". That inference is exactly what DoD-2 forbids, and it took a separate cleanup commit to expose it.
- **Proposed fix**: in `templates/tasks-template.md`, make the mutation-leg DoD require the evidence **path** to exist at the moment the row is checked off, not merely to be named — a `test -s <path>` per leg in the gate row, or a gate row that greps the evidence file for the leg id. And when a reading is produced after the fact, require the DoD row to carry the producing commit — a reading with no commit behind it is indistinguishable from a reading invented from the carrier's name.

### F3 — A delegated verification row can silently narrow a `final` criterion

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/tasks.md#L143

- **Evidence** (verbatim quote):

  ```
  - [x] T032 [P] [US2] [blockedBy: T022] Run the downstream render-verify for `SC-003` … : in a scratch directory under `.specify/.tmp/086/`, initialize a project with the CLI, then grep the generated `.specify/memory/constitution.md` and `.specify/instructions.md` for the principle title …
  ```

  — the row instructs the run to grep the generated files, and the evidence file records that it grepped the templates instead.

- **Why it's a problem**: `verification.md` and `closure-acceptance-check.py` both read a status row, never a row's *scope*. A task row can therefore satisfy its gate by measuring something adjacent to what it names, and no gate goes red. This feature shows the failure mode without any dishonest actor: the row's instruction was unachievable as written (the files are empty at init), the executor made the reasonable substitution, and the substitution lives only in the evidence prose. `tasks.md` has no field for "measured a different surface, here is why", so the narrowing is invisible to every machine that gates on it.
- **Proposed fix**: add an optional `[narrowed: <what changed> — <why>]` tag to `templates/tasks-template.md`'s row vocabulary, and make the completion-gate check grep for it so any narrowed row appears in the gate output. The cheap version: `verification.md`'s `SC-NNN_value` for a `final` criterion must quote the criterion's own object phrase, and a value that does not contain it is an input error.

### F4 — Two binary delivery claims in the process rules name today's runner by hand, before the feature that owns the runner exists

- **Severity**: P2
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/AGENTS.md (`## Test Execution Efficiency (测试执行效率)` section source is `.specify/shared/guidelines/test-execution-efficiency.md`; the section text is in AGENTS.md)

- **Evidence** (verbatim quote):

  ```
  - **Mode follows the discriminating property (方式由判别属性决定)**: process-level parallelism, asynchronous concurrency and neither are decided per execution unit by what it waits on — serial stays a legitimate answer, recorded rather than forced.
  ```

- **Why it's a problem**: this is not a defect in 086 — it is the shape the feature deliberately chose (owner guideline plus a four-line ambient section). It is recorded here because the review's job is to say what a maintainer inherits: the ambient section tells every downstream project that serial is "a legitimate answer, recorded rather than forced", while this repository's own shipped default is now parallel and its one serial exception is a marker, not a recording. A reader who takes the ambient line as a default instruction will not find the runner's actual default anywhere in the inherited text. That is a comprehension gap, not a contradiction — but it is one the next project pays for.
- **Proposed fix**: add one clause to the ambient section in `templates/instructions-template.md`: that a project's own runner default is the runner's business and this rule does not choose it, pointing at the feature's own decision record shape. That is a pointer, not a copy, and it closes the "is the rule telling me to stay serial?" question at first read.

### F5 — The temporary-SDD-run mechanism has no stage for the process defect that recurs across waves

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/checkpoints/12-implement-closure.md#L44

- **Evidence** (verbatim quote):

  ```
  - observations: mutation sandboxes must live outside the repo root (now a standing rule for later
    waves); the DoD-2 backfill is the second time a package reported a complete-looking carrier map
    without readings — review should check the newly produced readings.
  ```

- **Why it's a problem**: the checkpoint itself records that the DoD-2 backfill is the **second** occurrence of the same defect, and the closure record still routes the remedy to "review should check". A recurring process defect that is re-routed to a later stage each time it appears is the compounding toll this severity level names: every subsequent feature will spend one wave discovering it and one cleanup commit disclosing it. The `sdd-loop-driver` skill has a configuration-review section in its checkpoint shape, but no mechanism that promotes a repeated observation into a change to the driving skill.
- **Proposed fix**: in `skills/external/sdd-loop-driver/` (the checkpoint protocol's owner), require a checkpoint's `observations:` field to carry a `recurrence:` counter, and require any observation at count ≥ 2 to be either promoted into a named change to the driver skill or explicitly parked with a reason. "Review should check" is not a disposition.

### F6 — A prediction was written into the status field before the verdict existed

- **Severity**: P1
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/086.md (`### 当前状态裁定`)

- **Evidence** (verbatim quote):

  ```
  **披露**：裁决前本文件与 `features.md` 曾按预期先写成 `Blocked`（当时估计继承缺口会挡住收口），实测裁决为 accept 后已改正
  ```

- **Why it's a problem**: the feature's status field briefly carried `Blocked` as a *prediction* of what the closure checker would say, and the correction is disclosed only in prose. The status field is the machine-readable claim the Acceptance Reality Check compares against, and `Implemented → Blocked` is legal only as an **audit correction citing evidence that makes the claim false** — writing a predicted `Blocked` before any verdict could make it true means the vocabulary was used to express an expectation, not an observation. The final state is correct and the checker agrees; the process lesson is that the flip commit sequence left no way for a reader to see which state preceded which verdict.
- **Proposed fix**: in `templates/feature-details-template.md` § Canonical Status State Machine, state that a status is written **only** from a completed verdict, and that a predicted status MUST NOT be written even transiently. Where a run needs to record an expectation, it belongs in the checkpoint's `observations:`, not in the status field. (The record survives here only because the driver disclosed it — the rule should make the disclosure unnecessary.)

### F7 — The two-slot budget is spent by discipline, not by a machine, so the accounting is only as good as the executor's honesty

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/test-evidence/full-run-budget.md#L18

- **Evidence** (verbatim quote):

  ```
  Rule applied when reading the table below: a full-suite invocation that is neither listed nor
  exempted here is an unaccounted consumption and fails T054.
  ```

- **Why it's a problem**: the account is excellent — eight rows, each with slot label, purpose, command and evidence, plus two "no run" rows. But nothing produces it except a human/agent remembering to write it, and the one row that matters most (row 7, the contaminated first closure attempt) exists only because the executor chose to disclose it. The feature's own cost model therefore rests on the same property that F2 shows is unreliable: an executor who reports a complete-looking artifact. `audit-test-budget.py` reads a *ledger of runs*, so the sensor exists — the gap is that this feature's own two-slot discipline is not wired to it.
- **Proposed fix**: in `skills/external/sdd-loop-driver/references/efficiency-model.md`, make the runner's own invocation write a slot row (or make `run-tests.sh` append to the ledger when `--names-out` points into a spec's `test-evidence/`). Then `audit-test-budget.py` can refuse a closure whose full-run count exceeds the slot ceiling, and the account stops depending on a table someone remembered to fill.

### F8 — "No new machinery" is asserted by an exclusion grep rather than by a positive inventory

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/tasks.md#L225

- **Evidence** (verbatim quote):

  ```
  `git diff --name-only $(git merge-base HEAD master)..HEAD -- templates/commands skills/ | grep -v 'skills/internal/manage-constitution/SKILL.md'` is empty … this row is FR-017's only carrier (DoD-1).
  ```

- **Why it's a problem**: the check proves that no file under two paths changed, with one path allow-listed by hand. It does not prove the boundary FR-017 declares — "no new `/speckit.*` command, skill entry template or runtime service". A new command template added under a *third* path would pass; so would a new runtime service in `src/`. The feature's own diff happens to be clean (I confirmed `templates/commands/` is untouched in the 113-file delta), but the guard proves the paths, not the property.
- **Proposed fix**: invert the check in `scripts/python/` — add a small inventory script that enumerates the command-entry surface and the runtime entrypoints and diffs the *inventory* against the merge base. An allow-list of paths is a proxy; an enumerated inventory is the property.

### F9 — The closure checker's `inherited`-row rule is documented only in the feature that tripped over it

- **Severity**: P1
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/verification.md#L90

- **Evidence** (verbatim quote):

  ```
  Note the interaction with 085: its SC-010 stays partial, and the checker accepts this feature anyway because an `inherited` row is judged by whether its carrier RESOLVES (here `gate:GATE-086` in tasks.md), not by whether the dependency has already flipped that row to pass.
  ```

- **Why it's a problem**: the executor expected the opposite (hence F6's predicted `Blocked`) and only discovered the actual rule by experiment — blanking the carrier or aiming it at `gate:GATE-999` was the probe. The rule is real and defensible, but the place a spec writer would look for it (`shared/workflow/acceptance-hardening.md` § Inherited Blockers, or the checker's own `--help`) does not state it in that form. So every feature with an inherited blocker spends a wave re-deriving it, and the safer error is the one this feature made: assert `Blocked` in advance out of caution.
- **Proposed fix**: state the resolution rule in `shared/workflow/acceptance-hardening.md` § Inherited Blockers in one sentence — "an `inherited` row is judged by whether its carrier resolves, not by the dependency's own status; an unresolvable carrier is `inherited-blocker-undisposed`" — and have `closure-acceptance-check.py --help` name the same sentence.

### F10 — The principle's pointer names the runtime form of the owner path, while the specification fixes the framework-source form

- **Severity**: P1
- **Category**: Template
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/constitution-template.md#L331

- **Evidence** (verbatim quote):

  ```
  - Test execution efficiency MUST be judged by the criterion owned at
    `.specify/shared/guidelines/test-execution-efficiency.md`, which is also the only
  ```

  against `requirements.md` line 313, which fixes the pointer path:

  ```
  | `STR-003` | `"shared/guidelines/test-execution-efficiency.md"` | FR-018, FR-019, FR-020, SC-002, SC-003, 指针形态的唯一路径 |
  ```

- **Why it's a problem**: both forms are legitimate — `.specify/` is the runtime form a project-initialised tree uses, and FR-018/FR-020 use it too. `src/specify_cli/__init__.py`'s `_render_specify_local_paths` rewrites **only** `.specify/`-prefixed strings, so the template's literal passes through unchanged and the shipped clause lands in a downstream project pointing at `.specify/shared/…` while the file beside it opens with the other spelling. Measured this run on a fresh `specify init` at `a0426644`: the generated `shared/guidelines/test-execution-efficiency.md` line 3 reads `文件路径:.specify/shared/guidelines/test-execution-efficiency.md`. The consequence is that `STR-003` — declared as "the only path form" — is not the path that ships, and the guard in `tests/contract/test_test_execution_efficiency.py` asserts the source form only, so it cannot see the drift. **Answer** (this run's disposition): the runtime form is the correct one for a downstream tree — a pointer to a framework-source path inside an initialised project is itself the defect — so the repair belongs in the specification, and re-pinning `STR-003` plus the SC-002/SC-003 readings is a follow-up, not an edit to a closed feature.
- **Proposed fix**: re-pin `STR-003` to the runtime form and make the template's clause and the owner file's own header agree; extend the six-surface guard so each surface is asserted against the form that is correct *for that surface* (source form under `shared/`, runtime form under `.specify/` and downstream). Keep the fix in the specification and the guard — no change to the shipped text is needed once `STR-003` names what ships.

### F11 — The six-surface guard cannot see the pointer drift it is meant to prevent

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_test_execution_efficiency.py

- **Evidence** (verbatim quote, the guard's own scope as described in `test-evidence/smoke-086.txt`):

  ```
  | `tests/contract/test_test_execution_efficiency.py` | the shipped principle: the owner guideline exists and holds the criteria, and the constitution (template + live), the instructions (template + live) and the generator's MUST-include list each carry a **pointer** to it rather than a copy |
  ```

- **Why it's a problem**: F10 shows two spellings of one pointer coexisting in the tree. This guard is green, and it is green because it asserts one spelling. A guard whose red path cannot fire on the actual coexistence is a claim, not evidence — and this one is named in `verification.md` as the carrier for SC-002. A reader who trusts it would conclude the pointer form is unified when it is not. **Answer** (this run's disposition): accept the guard as-is for what it does assert (presence, distinctness, no decision-table copy, in-memory red legs), and treat the cross-form consistency check as the half that is missing — see F10's proposed fix, which adds exactly that half.
- **Proposed fix**: extend `test_c39_*` with a cross-surface consistency case that resolves the pointer on each surface to an existing file, instead of comparing it to a literal — a resolved path proves the pointer works; a literal comparison only proves someone typed it twice. Add the downstream case (run the pointer against a temp `specify init` tree) so the runtime form is measured where it ships.

### F12 — Evidence describes a state that no longer reproduces, without naming the copy that produced it

- **Severity**: P2
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/086-efficient-test-execution/test-evidence/downstream-init.txt#L90

- **Evidence** (verbatim quote):

  ```
  the generated `.specify/memory/constitution.md` is the two-line placeholder … and `.specify/instructions.md`
  is not generated at init time at all. That is the product's designed shape
  ```

- **Why it's a problem**: measured this run, a fresh `specify init` at `a0426644` in a directory **inside** the repo produces a `.specify/memory/constitution.md` that already carries `### XIX. Efficient Test Execution (Concurrent by Default)` — because in that layout the CLI finds local templates and copies the packaged `constitution-template.md` over the placeholder. Both observations are true; they differ by which template copy the init consumed (the packaged source vs the nested `.specify/templates` copy), and the evidence file does not record which. A later reader comparing the record with a fresh init sees a contradiction that is really an unrecorded variable.
- **Proposed fix**: record the template source the init consumed in the evidence file (the CLI prints `ok Using local templates: constitution.md copied` — quote that line), and state explicitly whether the init ran inside or outside a spec-kit checkout. The same discipline should apply to any evidence that depends on which of two shipped copies won.

### F13 — The two-pass status composition rule is pinned only on the `--names-out` path

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/bash/run-tests.sh#L285

- **Evidence** (verbatim quote):

  ```
  set +e
  "$PY" -m pytest -n0 -m serial ${ARGS[@]+"${ARGS[@]}"}
  SERIAL_STATUS=$?
  set -e
  [ "$SERIAL_STATUS" -eq 5 ] && SERIAL_STATUS=0
  if [ "$SERIAL_STATUS" -ne 0 ]; then
      exit "$SERIAL_STATUS"
  fi
  exit "$PARALLEL_STATUS"
  ```

- **Why it's a problem**: this plain branch is *behaviourally* right — a failed parallel pass keeps its non-zero code because `$PARALLEL_STATUS` is what the branch finally returns. The asymmetry is that the composition rule the two-pass mode implements ("the combined code is non-zero iff one of the passes failed") lives in two separate branch bodies: the `--names-out` branch above this one (line 265) normalizes exit 5 and returns the serial status first, and this branch returns `$PARALLEL_STATUS` last. A contract case pins the rule on the `--names-out` path only. So the code shape a reader must reason about differs between the two paths, and a future edit to either branch can change the composed exit code on the plain path without any test going red. Nothing measured is affected — every recorded run in `test-evidence/` used `--names-out` — but `bash scripts/bash/run-tests.sh -q` by hand is a supported surface whose contract is untested.
- **Proposed fix**: make both branches call one `compose_status` function so there is a single body to test, then add one contract case that drives that function against an injected parallel-fail/serial-pass pair and a parallel-pass/serial-fail pair. The first half removes the divergence by construction; the case pins the rule once.

## 4. What Worked — Preserve (Brief)

- `tasks.md` § Mutation Leg Carriers as a single map (leg → carrier → case that must fail → evidence file), with control/mutant pairing in the evidence so a red reading is attributable to the edit.
- The two-slot full-run model with a named `slot-2-in-slot-rerun-attempt` label — a contaminated run kept in the ledger instead of quietly dropped.
- The runner's two-line stderr header (`# test runner: <command>` plus `mode=… reason=… detail=…`), which made all three escape hatches decidable from output alone and pinned by contract cases.
- `closure-acceptance-check.py` as the sole verdict authority — it overruled an agent's prediction (F6) and that is the right direction for that authority to point.
- The 085 carve-out expressed as a two-part mechanical `git diff -U0` check (C-041) rather than as a prose permission; I reproduced it in one command and it held exactly.
- The code segment's coverage receipt as the "did not claim to have read it" evidence form.

## 5. spec-kit / SDD Improvement Recommendations

Nine ids, all registered in `.specify/memory/register.md` in the same commit as this report
(`REC-086-T1`, `REC-086-C1`, `REC-086-C2`, `REC-086-A1`, `REC-086-A2`, `REC-086-A3`,
`REC-086-W1`, `REC-086-W2`, `REC-086-D1`). Each carries its one-line meaning, this report's
section as the authority path, and status `open`; the register owns the row form, this section
owns the content.

### 5.1 Template Improvements

- **REC-086-T1 Escape-hatch and mode-truthfulness clauses in the runner contract template** — Target: `templates/` (the runner-contract shape used by 067 and 086; no single template file owns it yet). Change: name the serial escape hatches (explicit switch, nested invocation, absent engine) plus the mode line and the truthful command header as contract clauses a runner change MUST carry. Source: F13. Expected impact: a runner change cannot add a parallel default without deciding, and testing, what happens on the other two paths.

### 5.2 Command Prompt Improvements

- **REC-086-C1 A recurrence counter on checkpoint observations** — Target: `skills/external/sdd-loop-driver/` (the checkpoint protocol owner) and the checkpoint template it renders. Change: require `observations:` entries to carry a `recurrence:` count and require count ≥ 2 to be promoted into a named driver change or explicitly parked. Source: F5, F2. Expected impact: a defect that repeats across waves stops being re-discovered and re-routed to review each time.
- **REC-086-C2 A `[narrowed: …]` row tag in the tasks vocabulary** — Target: `templates/tasks-template.md`. Change: add the tag plus a completion-gate grep so any row that measured a different surface than it named appears in the gate output. Source: F3, F1. Expected impact: a `final` criterion can no longer be satisfied by an adjacent measurement without a machine-visible trace.

### 5.3 Automation / Script Improvements

- **REC-086-A1 Resolve pointers instead of comparing literals** — Target: `tests/contract/test_test_execution_efficiency.py` (and the six-surface guard shape it originated). Change: assert that each surface's pointer resolves to an existing file, and add a downstream case that runs the pointer against a temp `specify init` tree. Source: F11, F10. Expected impact: the guard would have caught the two coexisting pointer spellings instead of passing over them.
- **REC-086-A2 A positive inventory check for the no-new-machinery boundary** — Target: `scripts/python/` (new inventory script) plus the tasks-template gate idiom. Change: enumerate the command-entry surface and the runtime entrypoints and diff the inventory against the merge base, instead of asserting that two paths are unchanged. Source: F8. Expected impact: the boundary FR-017 declares becomes the measured property rather than a proxy for it.
- **REC-086-A3 One status-composition function in the runner** — Target: `scripts/bash/run-tests.sh` (+ its mirror via `sync-mirrors.py`). Change: extract `compose_status` and call it from both the `--names-out` and the plain branches. Source: F13. Expected impact: one place to pin with a contract case; the two branches cannot drift.

### 5.4 Workflow Improvements

- **REC-086-W1 State the `inherited`-row resolution rule where spec writers look** — Target: `shared/workflow/acceptance-hardening.md` § Inherited Blockers. Change: add the one sentence that an `inherited` row is judged by whether its carrier resolves, and mirror it in `closure-acceptance-check.py --help`. Source: F9, F6. Expected impact: a feature with an inherited blocker stops spending a wave deriving the rule by experiment, and stops pre-emptively claiming `Blocked`.
- **REC-086-W2 Write a status only from a completed verdict** — Target: `templates/feature-details-template.md` § Canonical Status State Machine. Change: forbid a predicted status, even transiently, and route expectations to the checkpoint's `observations:`. Source: F6. Expected impact: the status field stays an observation the checker can compare against, and the "briefly wrong then corrected" disclosure disappears.

### 5.5 Documentation Improvements

- **REC-086-D1 One path form per surface for owner-guideline pointers** — Target: `templates/constitution-template.md` (clause XIX's pointer) and the owner-guideline header the generator writes. Change: pick the runtime form for shipped text, re-pin `STR-003` in the declaring specification, and make the owner file's own header agree. Source: F10, F11. Expected impact: a downstream reader gets one path, which resolves.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-086-C1 recurrence counter on checkpoint observations | `skills/external/sdd-loop-driver/` checkpoint protocol | F5, F2 |
| P1 | REC-086-W1 state the `inherited`-row resolution rule | `shared/workflow/acceptance-hardening.md` § Inherited Blockers | F9, F6 |
| P1 | REC-086-W2 status only from a completed verdict | `templates/feature-details-template.md` | F6 |
| P1 | REC-086-A1 resolve pointers instead of comparing literals | `tests/contract/test_test_execution_efficiency.py` | F11, F10 |
| P2 | REC-086-T1 escape-hatch and mode-truthfulness contract clauses | runner-contract template shape | F13 |
| P2 | REC-086-C2 `[narrowed: …]` row tag | `templates/tasks-template.md` | F3, F1 |
| P2 | REC-086-A2 positive no-new-machinery inventory | `scripts/python/` | F8 |
| P2 | REC-086-A3 one status-composition function | `scripts/bash/run-tests.sh` | F13 |
| P2 | REC-086-D1 one path form per surface | `templates/constitution-template.md` | F10, F11 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: "No P0 findings raised; the P0 independent-validation pass is vacuously satisfied."

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

### 8.1 Wrap-up record (six steps, four units)

The composed run's unit census is four, all sharing run id `r20261106t120000z-086rev` and
differing only in `unit_id`, so none deduped another. Every unit completed its own closing
record; none was written on another's behalf and none was back-filled.

| Step | `/speckit.review` | `skill:review-sdd-process` | `skill:review-feature-quality` | `skill:code-review` |
|------|-------------------|----------------------------|-------------------------------|---------------------|
| 1 Run Determination | record `.specify/memory/session/20261106T075020Z-run-determination-speckit-review-r20261106t120000z-086rev.md`; four axes `not_evaluated` (`source_unavailable` ×2, `no_declared_checks`, `pending_next_turn`) | `…-skill-review-sdd-process-…md`, same axis shape | `…-skill-review-feature-quality-…md`, same axis shape | `…-skill-code-review-…md`, same axis shape |
| 2 Exec Quant | record `exec-quant/records/20261106T075023661339Z-f6aafb52.json` | `…075023857234Z-455cea8c.json` | `…075024032854Z-a6188ca2.json` | `…075024223229Z-35afe9cd.json` |
| 3 Feedback Record | `.specify/memory/feedback/20261106T075030Z-speckit-review.md` | `…075035Z-skill-review-sdd-process.md` | `…075040Z-skill-review-feature-quality.md` | `…075045Z-skill-code-review.md` |
| 4 Threshold Notice | `should_prompt: true` (292 since submission, threshold 10) — one consolidated non-blocking notification raised below | same store, same counter | same store, same counter | same store, same counter |
| 5 Token Reflection | embedded in each unit's own `## Review` / `## Optimization Points` — no unit's entry restates another's | — | — | — |
| 6 Docs Sync Eval | **无需记录** — `docs/contribute/dev-setup.md` already carries the parallel default, the `--serial` / `--workers` / `SPECKIT_TEST_WORKERS` precedence, the three `reason=` fallbacks and the `serial` marker enumeration (landed with WP-A3, commit `58d30bde`), and `CHANGELOG.md` carries the 086 entry; this review produced no new user-facing capability to document | | | |

**Threshold notice (step 4).** The feedback store holds 292 pending entries against a
threshold of 10, so a consolidated notification is raised — non-blocking, no transmission:

> The feedback store has accumulated 292 entries since the last submission. Run
> `/speckit.feedback` and let it judge how to route them, skip this time (silence counts as
> skip, and the notice returns once more accumulate), or stop prompting by raising the
> threshold.

**Token efficiency self-check (step 5).** Two findings, both recorded as `token-efficiency`
entries in the owning units' step-3 records: (i) the artifact segment's 13-member expected set
was derived by hand from two documents because no engine produces it — an LLM doing
deterministic work, and the exact substitution `REC-086-A2` targets; (ii) the closure reading
had to be re-derived from two evidence files with `wc -l` and `comm` because no engine exposes
the recorded slot, which is the repeated-read shape. No fabricated token counts are given —
precise counting is unavailable in this run and the procedure forbids inventing them.
