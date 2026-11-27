# Specification-Driven Development (SDD) Review Report: General Best Practices（通用最佳实践模块）

> **Audience**: spec-kit framework maintainers and the SDD driver owning this line.
> **Purpose**: the composed `/speckit.review` record — process, artifact, implementation and code segments in their fixed order, followed by the Acceptance Reality Check.
> **Intentionally problem-first**: artifact contents are described only where a finding needs the context.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 111 |
| Requirement Key | `111-general-best-practices` |
| Requirement Name | General Best Practices（通用最佳实践模块） |
| Related Feature | 111 — General Best Practices（通用最佳实践），new standalone feature (no parent slice) |
| Repository | spec-kit (git worktree `general-best-practices`) |
| Repository URL | `origin` = `git@github.com:github/spec-kit.git` (UPSTREAM; does not carry this branch). Fork remotes present: `gitee`, `github`, `gitlab`. |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty (the branch is unpushed). Citations below use absolute paths plus `git show <sha>:<path>` recovery instead of URLs. |
| Branch | `111-general-best-practices` |
| Commit SHA | `aca4fb076e9e9ea28ef6516f9d0a935949545fa9` (short `aca4fb076`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/general-best-practices` |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (Qoder CLI) |
| Environment | Linux x64 · bash 4.4.20 · CPython 3.11.11 · pytest 8.4.2 · line run id `r20261127T071500Z-111a` |
| spec-kit Source Snapshot | This worktree at `aca4fb076` (self-hosted project; feature base `0419adae5`) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 228 | `<repo>/.specify/specs/111-general-best-practices/requirements.md` | 9 FR / 7 SC / 7 STR / 24 adjudicated assumptions; closed four-category content module + accumulation by pointer |
| plan.md | 151 | `<repo>/.specify/specs/111-general-best-practices/plan.md` | 23-row Constitution Check (all pass), EP-001…EP-005, mirror obligations, declares `verification.md` as implement output |
| tasks.md | 305 | `<repo>/.specify/specs/111-general-best-practices/tasks.md` | 20 task rows (T001–T019 + T007A), 24 clause green tags, 8 gate items, DoD-1…DoD-7 |
| data-model.md | 157 | `<repo>/.specify/specs/111-general-best-practices/data-model.md` | E1–E11 entities, INV-01…INV-12, 3 transitions |
| quickstart.md | 153 | `<repo>/.specify/specs/111-general-best-practices/quickstart.md` | S-0…S-8 scenarios with measured readings |
| research.md | 114 | `<repo>/.specify/specs/111-general-best-practices/research.md` | M1–M11 measurements + R-1…R-10 design points |
| feature-ref.md | 64 | `<repo>/.specify/specs/111-general-best-practices/feature-ref.md` | Feature 111 binding, delivery surface, FR→surface and SC→evidence maps |
| contracts/ (4 files) | 116 | `<repo>/.specify/specs/111-general-best-practices/contracts/` | C-101…C-106 / C-201…C-205 / C-301…C-306 / C-401…C-407 = 24 clauses |
| checklists/ (2 files) | 140 | `<repo>/.specify/specs/111-general-best-practices/checklists/` | 40-item requirements-quality checklist + spec-quality checklist |
| test-evidence/ (110 files) | — | `<repo>/.specify/specs/111-general-best-practices/test-evidence/` | gate captures, validator outputs, full-suite and containment readings |
| notes/ (6 files) | — | `<repo>/.specify/specs/111-general-best-practices/notes/` | red-first capture, pre-change measurements, quickstart run, US1/US2/US3 green records |
| checkpoints/ (7 files) | 83 | `<repo>/.specify/specs/111-general-best-practices/checkpoints/` | driver checkpoints 01–07 |
| Module documents (5) | 68 | `<repo>/shared/best-practices/` | manifest + four category owner files (closed set, one seed, three placeholders) |
| Contract guard | 288 | `<repo>/tests/contract/test_general_best_practices.py` | six legs (a)–(f) + module-read prelude, `pytest.mark.contract` |
| Framework map row | 1 row | `<repo>/shared/definitions/framework-map.md` (+ mirror) | registration row for `.specify/shared/best-practices/` with `Feature 111` |
| Feature registry + detail | 1 row / 33 | `<repo>/.specify/features.md` (line 118) · `<repo>/.specify/features/111-general-best-practices.md` | claimed status `Implemented` on both carriers |

## 1. Process Execution Timeline

Reconstructed from `git log` scoped to the spec directory plus the stage records and driver checkpoints. All commits are local; head fixed for this run at `aca4fb076`. The review brief named baseline `39be9495a` while the spine's `stage_base_commit` and the run-start HEAD are `aca4fb076` (the intervening `39be9495a..aca4fb076` commit is checkpoint 07 itself); the run uses the run-start HEAD and discloses the brief/spine delta as an in-passing correction.

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | Requirements scaffolded by hand from the template (the script would derive number 112) | `requirements.md` A-9; `test-evidence/requirements-stage-2026-11-27.md` | Recorded deviation (branch pinned to 111) |
| 2 | Requirements stage left artifacts uncommitted; driver committed them | checkpoint 01 (`d53d3c228` "driver repair") | Yes — commit discipline gap, repaired by driver |
| 3 | Clarify stage: same uncommitted-artifact repair | checkpoint 02 (`652f2c09e`) | Yes — second occurrence |
| 4 | Plan stage: plan set + four contracts, clean commit | `87ad3d068`, checkpoint 03 `1638077e4` | No |
| 5 | Tasks stage: 20 rows, 24 clause tags, 8 gates | `6c5fd4654`, checkpoint 04 `1f5b9284e` | No |
| 6 | Checklist stage: 40-item dated checklist | `7cb097c81`, checkpoint 05 `5af1c1290` | No |
| 7 | Analyze round 1: 1 CRITICAL / 2 HIGH → repaired by cause | `4f6905a95` → `61e3ccfb6` (A-22/A-23/A-24) | No — gate worked as designed |
| 8 | Analyze round 2 (incremental): round-1 C/H fixed; open set C0/H0/M4/L6 deferred | `93326d8bc`, checkpoint 06 `7db9d8dec` | Recorded deferrals (review-visible) |
| 9 | Implement P1/P2: module + guard, map + mirror + init proof, closure runs | `570ef1a6a`, `63fdca3f7`, `f985cca92`, `16c40ee7d`, `0cbec5aa4`, `65b495b86` | No |
| 10 | Feature registration missing at stage closure; driver wrote row 111 + detail | `39be9495a`; checkpoint 07 line 4 | Yes — no stage in the driver sequence owns registration |
| 11 | Checkpoint 07 (implement U4) closes the stage | `aca4fb076` | No |
| 12 | Review: four segments + ARC; `verification.md` absent → closure checker exit 2 | this record; `closure-acceptance-check.py` stderr | **Blocking finding F-ACCEPTANCE** |

**Same-author gate**: not fired — the reviewed artifacts were produced by other stage executors dispatched by the driver, not by this review run; detection stayed with this read and is disclosed as such.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 5 |
| Documentation | 2 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | resolved diff base |
| Head commit | `aca4fb076e9e9ea28ef6516f9d0a935949545fa9` | run-start `HEAD`, fixed for the run |
| Base source | `explicit` (`--since 0419adae5`) | the feature's declared containment baseline; the `trunk-merge-base` default read `926836e0` (13,389 unrelated files) and was rejected — see F6 |
| Renderer mode | `renderer: text` | code record header |
| Changed / judged / skipped / gap files | 138 / 15 / 123 / 0 | copied field by field from the coverage receipt in the record |
| Segment verdict | `blocked` | one `blocking` entry (status claim without its acceptance carrier) |
| Gate verdict | `blocking-unresolved` | `report --summary --file` exits 1 |
| Reason, when one applies | `none` | — |
| Uncommitted scope | No uncommitted change outside this run's own records at receipt time; the two review records are produced by this run | disclosed, never concluded over |
| Record | `.specify/specs/111-general-best-practices/code-review.md` | written (triage `run`) |
| Archive | `none` | first run in this directory |

The code findings (1 blocking / 1 important / 2 suggestions / 2 nitpicks / 1 praise) live in the record and are read there; the six-level family is not restated here.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `checklists/`, `test-evidence/` | union of the stage rules (implement Step 9 requires `verification.md`) and `plan.md` § Project Structure (lines 79–91) |
| Coverage line | 10 / 11 | present members / expected members |
| Missing members | `verification.md` | absent from disk (`test -e` rc 1); also a finding |
| Segment verdict | `blocked` | one P0 |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `.specify/specs/111-general-best-practices/verification.md` | — | artifact absent from disk; no line to address | F-ACCEPTANCE: the acceptance carrier is missing, so the `Implemented` claim has no SC status rows and the closure checker exits 2 |
| P2 | `.specify/specs/111-general-best-practices/checklists/general-best-practices-2026-11-27.md` | 7 | — | F3: the checklist states `tasks.md` carries 19 task rows while the file carries 20 (T001–T019 + T007A) |

Readings behind the verdict: FR→task coverage 9/9 and SC→task coverage 7/7 (§ Requirement Coverage Map); 24 contract clause definition lines each claimed once by a `[green:]` tag (partition re-read against the tasks table); every SC has a `SC-NNN_status` row with a command and an evidence pointer in `test-evidence/verification-input.md`; the red-first claim carries a recorded red run (6 errors on the absent module, exit 1) and a subsequent 6-passed green; feature detail and registry row agree on `Implemented`. Open analyze residues are carried, not re-raised: AR2-01 (M), AR2-02 (L), AR1-04…AR1-06 (M), AR1-07…AR1-11 (L) — all recorded with reasons in `test-evidence/analyze-round2-report.md` and checkpoint 07.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | resolved diff base (explicit) |
| Head commit | `aca4fb076e9e9ea28ef6516f9d0a935949545fa9` | run-start `HEAD` |
| Base source | `explicit` | `git-delta-review.sh base --since 0419adae5` |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py` | recorded verbatim; re-run by this review |
| Smoke exit code | 0 | `6 passed in 6.26s` |
| Smoke evidence path | `.specify/.tmp/review-111/smoke.log` | exists, non-empty |
| Scope and regression verdict | scope clean — 138 paths = 113 declared + 2 registry exception + 23 per-entry accounting residuals, 0 violations (re-derived at HEAD); regression none — mirror parity 888 passed (re-run), targeted set 895 passed, full suite 223 failed names byte-identical to the implement-entry baseline (`cmp` exit 0) | — |
| Segment verdict | `pass` | one P2 |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | `.specify/specs/111-general-best-practices/test-evidence/containment.txt` | 81 | — | F4: the "final-tree re-read" (135 paths at `0cbec5aa4`) predates the registry-repair and checkpoint commits; the HEAD reading is 138 paths (invariant still 0 violations) |

Correctness readings: the five module documents match the settled source in substance (only the A-4 adaptations and the A-22/A-23 accumulation expansion differ); the guard's six legs are executable and red-first-backed; the map row exists once in source and mirror; `sync-mirrors.py --check` reports `shared/ == .specify/shared/ (122 files, byte-identical)`; the init proof carries all three evidences; `git diff --numstat 0419adae5..HEAD -- src/` is empty. Carried-open (not re-raised): AR1-04, the manifest's spec-local contract pointer that `specify init` never distributes.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` (registry row 118 and feature detail line 6 agree) | copied |
| `final_path` record, copied verbatim (7/7) | **not produced** — the checker exits 2 on an input defect (`required input not found: …/verification.md`); no seven-key record exists to copy, and none is fabricated | `closure-acceptance-check.py --spec-dir … --json`, run 2026-11-27 |
| Comparison verdict | `refused` | the claim is `Implemented` and no acceptance record can be read |
| Failed condition, on refusal | the acceptance carrier `verification.md` is absent, so no SC status row and no smoke record exist for the checker to read; exit 2 is an input defect, never an `accept` | named condition |
| Fixed item, on refusal | `F-ACCEPTANCE` at `P0` | exact spelling |

## 3. Findings (Problems & Improvement Targets)

### F-ACCEPTANCE — The acceptance carrier `verification.md` never landed; `Implemented` has no readable status rows

- **Severity**: P0
- **Category**: Workflow
- **Location**: `<repo>/.specify/specs/111-general-best-practices/verification.md` (absent). Context anchors: `<repo>/.specify/specs/111-general-best-practices/plan.md` L91; `<repo>/.specify/specs/111-general-best-practices/tasks.md` L23; `<repo>/.specify/skills/internal/implement-feature/SKILL.md` L325. *(Reachability: commit unpushed — use `git show aca4fb076:<path>`.)*
- **Evidence** (verbatim quotes):

  ```
  plan.md:91   └── verification.md      # Implementation output (/speckit.implement — NOT created by /speckit.plan)
  tasks.md:23  `verification.md` 由 spec 侧从该输入派生（crew MUST NOT 直接写）。
  implement-feature/SKILL.md:325  Populate `REQUIREMENTS_DIR/verification.md` from
                                  `.specify/templates/verification-log-template.md` — that template OWNS the
  checker stderr  closure-acceptance-check: input error: required input not found: …/.specify/specs/111-general-best-practices/verification.md
  ```

- **Why it's a problem**: `Planned → Implemented` is four conjunctive conditions, and condition 2 requires a status row per success criterion **in `verification.md`** (owner: `shared/workflow/acceptance-hardening.md` § Feature Status). The claim landed with the rows existing only in `test-evidence/verification-input.md`, a crew-side input the protocol never reads. The closure checker therefore exits 2, ARC cannot read any `final_path` record, and the transition to `Ready for Review` is refused. *(validated: direct re-read; validator-subagent dispatch prohibited by the coordinator role — "Never dispatch another agent")*
- **Proposed fix**: derive `verification.md` from `test-evidence/verification-input.md` using `.specify/templates/verification-log-template.md` (the shape used by the 107 and 108 reviews), re-run `closure-acceptance-check.py` to `accept`, then re-dispatch this review so the ARC copies a real record.

### F1 — The `verification.md` derivation has no named owner between implement and review

- **Severity**: P1
- **Category**: Workflow
- **Location**: `<repo>/.specify/specs/111-general-best-practices/tasks.md` L23 versus `<repo>/.specify/skills/internal/implement-feature/SKILL.md` L322–L329
- **Evidence** (verbatim quote):

  ```
  tasks.md:23        `verification.md` 由 spec 侧从该输入派生（crew MUST NOT 直接写）。
  SKILL.md:322-325   ### Step 9 — Pre-Status-Flip Gate and Verification Log
                     … Populate `REQUIREMENTS_DIR/verification.md` from
                     `.specify/templates/verification-log-template.md`
  ```

- **Why it's a problem**: the tasks file forbids the executing crew to write the file and delegates it to an unnamed "spec side", while the implement skill assigns the same file to the implement run. No stage in the driver's sequence owns the derivation, so the file vanished between the two statements. This is the third occurrence: the 107 review repaired the skipped derivation as its P0, and the 108 review recorded "verification.md is declared spec-side-derived (tasks DoD-8) but no stage owns producing it before review, so this review materialized it".
- **Proposed fix**: in `skills/internal/create-tasks/SKILL.md`, forbid a DoD row from reassigning an implement-stage deliverable without naming the deriving stage; in `skills/internal/implement-feature/SKILL.md` § Step 9, state that the run itself owns the population (with the review entry as the named fallback when a stage skipped it).

### F2 — The driver's stage sequence has no feature-registration stage, so every line pays a post-closure repair

- **Severity**: P1
- **Category**: Workflow
- **Location**: `<repo>/.specify/specs/111-general-best-practices/checkpoints/07-implement.md` L4; `<repo>/.specify/specs/111-general-best-practices/feature-ref.md` L10
- **Evidence** (verbatim quotes):

  ```
  checkpoints/07-implement.md:4  **Driver repair**: the stage closed without registering the feature; the driver added the registry row 111,
                                 updated the header (105) and wrote `.specify/features/111-general-best-practices.md` (commit `39be9495a`).
  feature-ref.md:10              The `Draft → Planned` advance therefore lands with that later stage, not here.
  ```

- **Why it's a problem**: plan/tasks deliberately deferred registry edits to a "feature-registration stage" named in FR-009, but the driver's `stage_plan` (spine: requirements → clarify → plan → tasks → checklist → analyze → implement → review → checkpoints → U6) contains no such stage. The registration therefore always lands as an ad-hoc driver repair, and the branch — based pre-109 — now carries a registry that lacks rows 109/110, creating a reconciliation debt for U6.
- **Proposed fix**: add the registration step (row + detail + `Draft → Planned`/status advance) to the driver's declared stage sequence, or make the implement stage own same-change registration; either way, record the owning seat in the stage brief.

### F3 — Task-row count stated as 19 while the file carries 20 rows

- **Severity**: P2
- **Category**: Documentation
- **Location**: `<repo>/.specify/specs/111-general-best-practices/checklists/general-best-practices-2026-11-27.md` L7 (same phrasing in `test-evidence/closure-gates.txt` L24 and `.specify/features/111-general-best-practices.md` L24)
- **Evidence** (verbatim quote):

  ```
  checklists/…:7   [../tasks.md](../tasks.md)（19 任务行；§ Requirement Coverage Map 9/9 与 7/7；24 条款逐条恰认领一次）
  closure-gates:42 The tasks validator additionally reports `tasks=20` (19 T-rows + T007A)
  ```

- **Why it's a problem**: a reader reconciling closure counts meets "19", "19/19" and "tasks=20" for the same file without a stated counting unit, which is exactly the kind of fact two artifacts should state one way.
- **Proposed fix**: state the row count (20, including T007A) or define the unit ("19 numbered task ids plus the T007A insertion") in the checklist and the closure records.

### F4 — The containment "final-tree re-read" predates the last three commits

- **Severity**: P2
- **Category**: Documentation
- **Location**: `<repo>/.specify/specs/111-general-best-practices/test-evidence/containment.txt` L81
- **Evidence** (verbatim quote):

  ```
  ## Reading 2 — final-tree re-read at `0cbec5aa4` (after the wrap-up accounting commit)
  | Committed paths in range | **135** |
  ```

- **Why it's a problem**: two commits after this reading add three paths — the registry exception pair from `39be9495a` and `checkpoints/07-implement.md` from `aca4fb076`. The SC-006 invariant still holds (re-derived at HEAD: 138 paths = 113 declared + 2 registry exception + 23 residuals, 0 violations), but a reader who takes "final" at its word inherits a stale count.
- **Proposed fix**: append a post-checkpoint re-read, or relabel Reading 2 as interim and cite the HEAD reading in `verification-input.md`.

### F5 — Full-suite run 1 executed while the executor was still writing the tree

- **Severity**: P2
- **Category**: Workflow
- **Location**: `<repo>/.specify/specs/111-general-best-practices/test-evidence/full-suite.txt` L4–L7
- **Evidence** (verbatim quote):

  ```
  Two runs are on record: run 1
  was taken while the executor itself was writing `tasks.md` (an invalid measurement
  window), run 2 is the authoritative frozen-tree reading.
  ```

- **Why it's a problem**: the most expensive execution in the feature bought an unusable reading because task-state writes landed mid-run (and one suite test compares `git status` before/after, so the executor's own write turned it red). The re-run was handled honestly; the precondition was avoidable.
- **Proposed fix**: in `skills/internal/implement-feature/SKILL.md` § Step 8, require the last task-state write to land before any full-suite invocation (freeze the tree for the measurement), the same discipline `shared/guidelines/test-execution-efficiency.md` already asks for isolation.

### F6 — Code-review `base` resolution picks the fork merge base in a worktree topology

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `<repo>/.specify/skills/internal/code-review/scripts/git-delta-review.sh` (`base` tiers)
- **Evidence** (verbatim output of this review's first resolution):

  ```
  base=926836e0fc931bfdbd531f45b0b27e3715e84a0c
  head=aca4fb076e9e9ea28ef6516f9d0a935949545fa9
  base_source=trunk-merge-base
  $ git diff --stat 926836e0..0419adae5 | tail -1
   13389 files changed, 2670221 insertions(+), 7185 deletions(-)
  ```

- **Why it's a problem**: the default resolution returned the upstream fork point, so the code segment's denominator would cover 13,389 unrelated files instead of the feature's 138; only the caller knowing to pass `--since 0419adae5` produced a usable interval. The same denominator pressure was recorded in the 108 review ("the delta was 264 files for a six-file code surface").
- **Proposed fix**: add a resolution tier that reads the spec's declared baseline (this spec declares `0419adae5` in FR-009/plan EP-005) before the trunk merge base, or have the driver pass the declared baseline explicitly; keep `explicit` highest.

### F7 — Stage artifacts repeatedly left uncommitted, repaired by the driver

- **Severity**: P2
- **Category**: Workflow
- **Location**: `<repo>/.specify/specs/111-general-best-practices/checkpoints/01-requirements.md` L6; `<repo>/.specify/specs/111-general-best-practices/checkpoints/02-clarify.md` L4
- **Evidence** (verbatim quotes):

  ```
  checkpoints/01:6  **Repair**: the stage left its artifacts uncommitted; the driver staged exactly the produced paths
                    and committed `d53d3c228` (records commit). No content was changed by the repair.
  checkpoints/02:4  **Repair**: stage left artifacts uncommitted; driver committed exactly the six produced paths (commit `652f2c09e`).
  ```

- **Why it's a problem**: two of the six stages before implement ended with their products uncommitted, so the driver had to reconstruct the produced path set twice. The repair worked, but the burden lands on the orchestrator every time a stage executor skips its commit.
- **Proposed fix**: make a clean worktree (or a stage-owned explicit-path commit) part of the U4 acceptance criterion for stage sentinels; keep the driver's explicit-path commit as the fallback only.

## 4. What Worked — Preserve (Brief)

- Red-first guard: 6 errors on the absent module (exit 1) → 6 passed after landing; the capture carries command, output and exit code.
- Analyze round 2 re-adjudicated the round-1 CRITICAL/HIGH by cause with engine measurements (A-22/A-23/A-24) instead of asserting repair.
- Containment is decidable and was re-derived at every reading (0 violations; per-entry accounting predicate works).
- Mirror byte identity has one adjudicator (parity suite, 888 passed) and the guard deliberately keeps its hands off it.
- Full-suite discipline: both runs preserved, the invalid window attributed, `cmp` byte-identical against the 223-name entry baseline.
- The guard pins structure without freezing the delivery count of 3 or claiming semantic-truth judgement (C-203/C-205).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Automation / Script Improvements

- **REC-111-01 — Resolve the code-segment base from the spec's declared baseline** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (`base` tiers). Change: insert a "declared-baseline" tier (read FR-009/plan baseline) before `trunk-merge-base`, and print the rejected default reading when an explicit base wins. Source: F6. Expected impact: fork worktrees stop producing five-figure denominators and skip-heavy receipts.

### 5.2 Workflow Improvements

- **REC-111-02 — Name the seat that derives `verification.md`** — Target: `skills/internal/implement-feature/SKILL.md` § Step 9 and `skills/internal/create-tasks/SKILL.md` (DoD generation). Change: implement run owns the population; a tasks-authored DoD may not reassign it without naming the deriving stage. Source: F-ACCEPTANCE, F1. Expected impact: ends a three-feature recurrence (107/108/111) of the review discovering the missing carrier.
- **REC-111-03 — Add a registration step to the driver's stage sequence** — Target: `skills/external/sdd-loop-driver/SKILL.md` (stage sequence) with its stage-brief templates. Change: declare the registration seat (row + detail + status advance) as a stage, or fold it into implement's closure; record the owning seat in the briefing. Source: F2. Expected impact: no more post-closure driver repairs and no U6 reconciliation debt for sibling rows.
- **REC-111-04 — Freeze the tree before a full-suite measurement** — Target: `skills/internal/implement-feature/SKILL.md` § Step 8 (commit gate). Change: the last task-state write lands before any `run-tests.sh --full`, and the run records the tree state it measured. Source: F5. Expected impact: the one expensive suite execution per feature stops being wasted on an invalid window.
- **REC-111-05 — Stage-completion criterion includes a clean worktree** — Target: `skills/external/sdd-loop-driver/SKILL.md` (U4 criteria). Change: the sentinel may not be accepted while produced stage artifacts are uncommitted; the driver's explicit-path commit stays as the fallback, not the norm. Source: F7 (below). Expected impact: removes the two repairs this line needed at requirements/clarify.

### 5.3 Documentation Improvements

- **REC-111-06 — One way to state the task-row count** — Target: the feature's checklists and closure records (and the tasks-template guidance). Change: state `20 rows (T001–T019 + T007A)` or define the counting unit once. Source: F3. Expected impact: closure counts reconcile without recounting.
- **REC-111-07 — Keep "final" readings actually final** — Target: the review/implement evidence conventions (`shared/workflow/acceptance-hardening.md` evidence guidance or the feature's own evidence records). Change: a reading labeled final must be taken after the last commit in the range, or is labeled interim with its commit. Source: F4. Expected impact: the acceptance evidence's newest reading is also its final one.

*(F7 — uncommitted stage artifacts — is folded into REC-111-05 for brevity; it is the same workflow seat.)*

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Derive `verification.md` and re-run the closure gate | feature's implement close-out / `.specify/templates/verification-log-template.md` | F-ACCEPTANCE |
| P1 | Name the deriving seat for `verification.md` | `skills/internal/implement-feature/SKILL.md` § Step 9; `skills/internal/create-tasks/SKILL.md` | F1 |
| P1 | Declare the feature-registration stage | `skills/external/sdd-loop-driver/SKILL.md` | F2 |
| P2 | Declared-baseline tier in `base` | `skills/internal/code-review/scripts/git-delta-review.sh` | F6 |
| P2 | Freeze the tree before full-suite runs | `skills/internal/implement-feature/SKILL.md` § Step 8 | F5 |
| P2 | Clean-worktree stage completion | `skills/external/sdd-loop-driver/SKILL.md` (U4) | F7 |
| P2 | One task-count phrasing; truly-final readings | feature checklists/evidence conventions | F3, F4 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: the single P0 (`F-ACCEPTANCE`) was confirmed by a direct re-read of the missing path, the plan's declared structure, the checker's exit-2 stderr and the implement skill's Step 9; the independent validator subagent wave was not dispatched because the coordinator role forbids dispatching agents ("Never dispatch another agent"), and the substitution is disclosed in the finding itself.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

---

**Composed-run verdict**: the four segments conclude independently — process: P1 ×2 (F1, F2) / P2 ×3 (F5, F6, F7); artifact: `blocked` — P0 ×1 (F-ACCEPTANCE) / P2 ×1 (F3); implementation: `pass` — P2 ×1 (F4); code: `blocked`, gate `blocking-unresolved` (findings in `code-review.md`). The Acceptance Reality Check refuses the comparison (checker exit 2 on the absent `verification.md`). **The feature status stays `Implemented`; no flip to `Ready for Review`.**