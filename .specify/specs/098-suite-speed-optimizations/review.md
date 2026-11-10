# Specification-Driven Development (SDD) Process Review Report: 098-suite-speed-optimizations

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 098 |
| Requirement Key | `098-suite-speed-optimizations` |
| Requirement Name | 测试套件提速五项优化（xdist 验证 / slow 分档 / 会话缓存 / 去固定 sleep / 进程内直调） |
| Related Feature | 086 Efficient Test Execution (Concurrent by Default) — claimed status `Ready for Review`, not regressed |
| Repository | spec-kit (framework source + its own client runtime) |
| Repository URL | `origin` = `git@github.com:github/spec-kit.git` (UPSTREAM); fork remotes `gitee` / `github` / `gitlab` exist but hold no pushed copy of this branch |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — cite absolute paths plus `git show <sha>:<path>` recovery instead of URLs |
| Branch | `098-suite-speed-optimizations` |
| Commit SHA | `ea5962c8751f124a94d9807f2bf8f8f10ac6ce6b` (short: `ea5962c87`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder · four-segment composition (`/speckit.review`) |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash 4/5, Python 3.11.11, pytest 8.4.2, pytest-xdist 3.8.0, git 2.43.5 |
| spec-kit Source Snapshot | this worktree at `ea5962c87` (framework source `templates/`, `shared/`, `scripts/`, `skills/` and the client runtime `.specify/` in one repository) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 266 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/requirements.md` | 27 FR / 11 SC (9 final, 2 supporting), 17 assumptions, 5 clarification Q/A |
| plan.md | 366 | `…/098-suite-speed-optimizations/plan.md` | 22-row Constitution Check, T-001…T-003, EP-001…EP-004, 9 work packages |
| tasks.md | 407 | `…/098-suite-speed-optimizations/tasks.md` | 61 rows (60 `[X]`, 1 `[~]` T061), 7 phases, DoD and 5 completion gates |
| research.md | 137 | `…/098-suite-speed-optimizations/research.md` | B-1…B-10 measured baselines, R-1…R-10 decisions |
| data-model.md | 121 | `…/098-suite-speed-optimizations/data-model.md` | Entities E-1…E-8 |
| quickstart.md | 193 | `…/098-suite-speed-optimizations/quickstart.md` | Scenarios S-0…S-13 |
| feature-ref.md | 66 | `…/098-suite-speed-optimizations/feature-ref.md` | 26-row delivery surface, disclosures, out-of-scope |
| contracts/ | 424 | `…/098-suite-speed-optimizations/contracts/` | 6 files, 68 clauses (16/9/12/11/10/10) |
| verification.md | **0 (absent)** | `…/098-suite-speed-optimizations/verification.md` | **Missing** — no SC status rows, no smoke record, no `deferred_tasks=` |
| checklists/requirements.md | 52 | `…/098-suite-speed-optimizations/checklists/requirements.md` | Requirements-quality checklist |
| test-evidence/index.md | 46 | `…/098-suite-speed-optimizations/test-evidence/index.md` | SC → evidence mapping (SC-003/SC-005 pending closure) |
| notes/ (three records) | 9252 | `…/098-suite-speed-optimizations/notes/` | pre-change measurements (8640), quickstart run (268), red-first (344) |
| checkpoints/ | 3 files | `…/098-suite-speed-optimizations/checkpoints/` | Only 01-requirements, 02-clarify, 03-plan |

## 1. Process Execution Timeline

Reconstructed from the 26 commits in `b3da3a26d..ea5962c87` (the feature-first-commit base resolved by `git-delta-review.sh base`). No working-tree fallback was needed; all stage products are committed.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements authored; RS-001 Contract cell repaired the next commit | `5d1c8eed0`, `a4b6b178c` | None — inline repair |
| 2 | clarify binds Feature 086 and resolves 5 decision gaps | `4c359241b` | None |
| 3 | plan + Phase-1 design artifacts | `fc4a469dc` | None |
| 4 | tasks (61 rows) and the E3 status row | `1990e4ea0`, `1303399c7` | None |
| 5 | requirements-quality checklist | `361ff7fed` | None |
| 6 | analyze round 1 merge | `808c1eb1b` | Three analyze rounds were needed |
| 7 | analyze repair pass — 1 CRITICAL + 7 HIGH | `eadc0fc12` | Repair pass, disclosed |
| 8 | analyze round 2 merge — gate FAIL (1 CRITICAL open) | `3c0e49042` | Gate correctly failed |
| 9 | analyze repair r3 — re-anchored SC-004 | `bcea9a678` | Repair pass, disclosed |
| 10 | analyze round 3 merge — 0 CRITICAL/HIGH, gate PASS | `89350606c` | None |
| 11 | setup — notes landing point + frozen coverage baseline | `6669fb4e3` | None |
| 12 | constitution amended 1.19.0 → 1.19.1 (Principle VII carrier) | `af73f65f1` | **Out-of-plan**: no 098 task row asks for it; the commit records a 2026-11-10 user ruling (F7) |
| 13 | WP-1 runner tier mechanism; WP-2 slow registry | `0d1f7a1e4`, `1dca066fb` | None |
| 14 | T012 green record + T013 tier/slow mutation drills | `719f78b90` | T012's stated scope "obligations 1–11" outran the file at that moment (F8) |
| 15 | WP-3 … WP-9 (docs, parallel consistency, cache, clock, in-process, measurement) | `ac91ab81a` … `2183d4986` | None |
| 16 | S-4 serial wall restated from file timestamps | `c5b2b32a7` | Measurement proxy, disclosed (F6 note) |
| 17 | T013 close — 13 mutation legs | `ea5962c87` | None |
| 18 | Implement close-out (verification.md, closure checker, status carrier) | **absent** — no commit touches `verification.md`; `git log --all --name-only -- …/verification.md` is empty | **Deviation**: the implement stage's step 9 / Pre-Status-Flip Gate was never run (F1) |
| 19 | Driver state spine and checkpoints | `.specify/state/098-suite-speed-optimizations.md` still reads `stage: requirements` / `state: stalled`; `checkpoints/` stops at 03-plan | **Deviation**: per-stage state writes and checkpoints for tasks…implement are missing (F2, F4) |
| 20 | Review dispatch (this run) | state spine says `stage: requirements` while all 60 implement rows are `[X]` | The review was dispatched on a stale spine with no implement close-out |

## 2. Findings Summary

Severity counts cover the three non-code segments (process § 3, artifact § 2.2, implementation § 2.3). The code segment keeps its own six-level family and is never merged into these counts.

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 5 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

Category counts cover the **process-segment** findings only (Section 3); the artifact and implementation findings are counted by severity in their own slots.

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation | 1 |
| Workflow | 4 |
| Documentation | 3 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base (feature-first-commit: parent of `5d1c8eed0`) |
| Head commit | `ea5962c8751f124a94d9807f2bf8f8f10ac6ce6b` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec …` |
| Renderer mode | `text` | non-interactive review; `receipt` recorded `renderer=text` |
| Changed / judged / skipped / gap files | 250 / 137 / 113 / 0 | copied field by field from `code-review.md`'s coverage receipt |
| Segment verdict | `not-evaluated` | 113 non-code files skipped with the legal reason `non-code-file`; 0 gap, 0 blocking |
| Gate verdict | `allow` (code merge gate) — **transition gate `blocking-unresolved`** | `report --summary --file code-review.md` → `"gate":"allow"`, `blocking_entries=0`; the `Implemented → Ready for Review` transition is refused for the non-code conditions named in § 2.4 and the conclusion |
| Reason, when one applies | `none` for the code merge gate; the transition refusal's named conditions are in § 2.4 | — |
| Uncommitted scope | 35 uncommitted paths were outside the review object (runtime memory records, this report and the code record); the receipt gives no conclusion over them | `code-review.md` § 未提交范围 |
| Record | `.specify/specs/098-suite-speed-optimizations/code-review.md` | written because triage = `run` |
| Archive | `none` | first code record in this spec directory |

**Receipt provenance disclosure**: the unmodified `git-delta-review.sh receipt` exits 2 on this delta because three evidence `.log.gz` files are binary (`git diff --numstat` yields `-`), even though `binary` is a legal skip reason. The block above was produced by an otherwise identical local copy with the skip selectors honored before line measurement; the workspace script is unchanged (finding F6).

**Important item answer (required)**: *Agree.* The single `important` item (`scripts/bash/run-tests.sh:372` — `tier=caller` skips the 086 C-010/C-011 serial two-pass while `tier-selection` C-012 declares the serial model unchanged, and no guard covers the serial-marked + caller-`-m` intersection) is a real contract/implementation mismatch. It remains open; this review does not remediate code.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `test-evidence/` | union of the standard spec set and `plan.md` § Project Structure (lines 131-141) |
| Coverage line | 9 / 10 | present members / expected members |
| Missing members | `verification.md` | absent from disk; also counted as an uncovered member |
| Segment verdict | `blocked` | a required member is missing **and** the latest final-path evidence contradicts SC-002 |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `.specify/specs/098-suite-speed-optimizations/verification.md` | n/a | the artifact does not exist | A1 — the implement-stage evidence carrier is missing: no SC status rows, no smoke record, no `deferred_tasks=`; the closure checker exits 2 on it |
| P0 | `.specify/specs/098-suite-speed-optimizations/notes/quickstart-run.md` | 91 | line present | A2 — SC-002's final-tree bidirectional difference is non-empty (`comm -13` = 2 names) while the criterion requires both directions empty; the record substitutes the weaker "0 new failure names" reading |
| P1 | `.specify/specs/098-suite-speed-optimizations/notes/pre-change-measurements.md` | 12 | line present | A3 — the "implement-start" slot-1 baseline was run at WP-9 on the post-WP-8 tree; SC-005's "≤ 110 % of the baseline" has no pre-change referent |
| P1 | `.specify/specs/098-suite-speed-optimizations/tasks.md` | 221 | line present | A4 — T061 is the only `[~]` row and its reason is inline only; DoD-1 requires `deferred_tasks=` in `verification.md`, which is absent |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `ea5962c8751f124a94d9807f2bf8f8f10ac6ce6b` | run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh --workers 4 tests/contract/test_suite_tier_contract.py tests/contract/test_parallel_consistency_contract.py tests/contract/test_scan_cache_contract.py tests/contract/test_event_wait_contract.py tests/contract/test_inprocess_conversion_contract.py tests/contract/test_run_tests_runner_contract.py -q` | recorded verbatim; run by this review |
| Smoke exit code | 0 | 86 passed in 34.83 s, `mode=parallel workers=4 dist=load passes=1 tier=fast excluded_slow=0` |
| Smoke evidence path | `.specify/specs/098-suite-speed-optimizations/test-evidence/review-smoke-098.txt` | exists and is non-empty |
| Scope and regression verdict | **fail** — the five new guards and the 086 runner suite are green, but SC-002's final-tree comparison is non-empty and SC-005's baseline is post-change; the delta also carries one out-of-plan, user-ruled constitution amendment | see I1–I3 |
| Segment verdict | `blocked` | correctness/acceptance for final-path SC-002 is not met on the final tree |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P0 | `.specify/specs/098-suite-speed-optimizations/verification.md` | n/a | the artifact does not exist | I1 — the feature has no smoke record (`smoke_command` / `smoke_exit_code` / `smoke_evidence_path`); the review-run smoke above is not the feature's record |
| P0 | `.specify/specs/098-suite-speed-optimizations/notes/quickstart-run.md` | 91 | line present | I2 — the final-tree delta does not leave `tests/contract` in the state SC-002 requires: `comm -13` = 2 serial-only names in `test_trigger_engine.py`, a file the delta touched (its c2 conversion); no repair or serial registration is recorded (C-004) |
| P1 | `.specify/specs/098-suite-speed-optimizations/notes/pre-change-measurements.md` | 12 | line present | I3 — FR-020 says the baseline is the implement-start reading; T003 executed at WP-9, so SC-005's wall comparison is post-change against post-change |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features/086-efficient-test-execution.md:6`, copied, not written back |
| `final_path` record, copied verbatim (7/7) | **not produced** — `closure-acceptance-check.py` exited 2 with `input error: required input not found: …/098-suite-speed-optimizations/verification.md` | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/098-suite-speed-optimizations --json` |
| Comparison verdict | `refused` | the checker cannot produce a record; the claim has no `final_path` evidence to survive |
| Failed condition, on refusal | `verification.md` absent → (a) no status row for any criterion (Planned→Implemented condition 2 fails), (b) no smoke record (condition 4 fails), (c) SC-002's latest same-tree measurement contradicts its own criterion, and (d) SC-003/SC-005 are closure-stage readings not yet taken while T061 remains deferred | named conditions, not merely "the transition was refused" |
| Fixed item, on refusal | `none` — `F-ACCEPTANCE` fires only when a `final_path` record exists with `pass` = 0; here no record exists at all | the zero-pass trigger cannot be evaluated |

## 3. Findings (Problems & Improvement Targets)

### F1 — Implement close-out was skipped: no `verification.md`, no closure verdict, no status carrier update

- **Severity**: P0
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/verification.md` (absent); duty: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/skills/internal/implement-feature/SKILL.md:325` and `templates/commands/implement.md:50,58-60`
- **Evidence** (verbatim quote):

  ```
  Populate `REQUIREMENTS_DIR/verification.md` from …   (implement-feature/SKILL.md:325)

  (1) run the checker on the tree to be claimed …, (2) copy its `verdict` and emitted
  reasons into `REQUIREMENTS_DIR/verification.md`, (3) only then write the registry row /
  detail status.   (templates/commands/implement.md:59)
  ```

  Measured: `ls .specify/specs/098-suite-speed-optimizations/` has no `verification.md`;
  `closure-acceptance-check.py --spec-dir … --json` exits 2 with
  `input error: required input not found: …/verification.md`; `git log --all --name-only -- …/verification.md`
  is empty; the 086 feature detail's `Last Updated`/`Latest Review` carry no 098 implement note.

- **Why it's a problem**: the slice closed 60/60 task rows and 13 mutation legs without ever executing its own Pre-Status-Flip Gate. The review is then asked to judge a status transition whose evidence base (SC rows, smoke, deferred record, closure verdict) does not exist. This is silent corruption risk: a future reader sees `[X]` rows and a `Ready for Review` parent and cannot tell that the implement gate never ran.
- **Proposed fix**: run the implement close-out on the current tree — populate `verification.md` (SC-001…SC-011 status rows with values/evidence pointers, the smoke triple, `deferred_tasks=T061 — driver closure stage`), run `closure-acceptance-check.py`, copy its verdict, and only then record any status claim. Make the driver refuse to dispatch review when `verification.md` is absent.

### F2 — The state spine is stale at `requirements`/`stalled` after the implement stage closed

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/098-suite-speed-optimizations.md:5-13,22-23,52-53`
- **Evidence** (verbatim quote):

  ```
  stage: requirements
  …
  last_verdict: U0 entry written; requirements dispatching
  …
  - state: `stalled`（U5；reentry-required）
  - next_stage: `none（停线）`；gates: analyze round-2 FAIL（1C/0H）
  ```

  The worktree HEAD is 26 commits past the base, with WP-1…WP-9 and T013 closed.

- **Why it's a problem**: a re-entrant session reads the spine first (driver discipline: "续环与重入只读状态脊"). It would resume at requirements and could re-dispatch stages or overwrite evidence; the E2 baseline row and E3 stage-status rows the driver's budget block requires are also absent.
- **Proposed fix**: write the spine at every U2/U3/U4 (stage, attempts, breakpoint, gate summary, evidence pointers) and make the review dispatch fail fast when the spine's stage is not the implement close-out. Refresh this line's spine to the actual state before any closure action.

### F3 — The "implement-start baseline" slot executed last because T003 is both a Phase-1 row and a WP-9 item

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/tasks.md:68,298-311`; `/…/notes/pre-change-measurements.md:12-19`
- **Evidence** (verbatim quote):

  ```
  The package map (`tasks.md` § Work Package Mapping) assigns T003 to WP-9, the last
  package, so the slot-1 run below executes on the post-WP-8 tree rather than literally
  before WP-1.   (notes/pre-change-measurements.md:14-16)
  ```

- **Why it's a problem**: the two-slot model's slot 1 is the pre-change reference. A post-change reading cannot serve as the baseline for SC-005's "full tier ≤ 110 % of the baseline", and the contradiction is structural: Phase 1 says T003 "starts immediately" while the WP table places it last.
- **Proposed fix**: make T003 (slot 1) a hard predecessor of WP-1 in the WP mapping (`[blockedBy: T003]` on every WP row, or a dedicated WP-0 executed before any behavior change), and re-take the base-tree full reading as the slot-1 in-slot rerun with the current tree as trigger + evidence.

### F4 — Driver checkpoints stop at the plan stage

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/checkpoints/`
- **Evidence**: the directory contains only `01-requirements.md`, `02-clarify.md`, `03-plan.md`; there is no `04-tasks`, `05-checklist`, `06-analyze` or implement checkpoint, while `checkpoints/` is the driver's per-stage handoff record (085/090 checkpoint protocol).
- **Why it's a problem**: the checkpoints are the re-entry and direction-audit carriers; their absence means the second half of the run is reconstructible only from git history and memory.
- **Proposed fix**: write the missing checkpoints from the stage records and commits before closure, and make the driver's stage-close verification require the checkpoint file it declares.

### F5 — `tasks.md` DoD Status is still `pending` and the deferred row has no `deferred_tasks=` carrier

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/tasks.md:23,221`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: pending

  - [~] T061 … <!-- deferred: driver closure stage after review; slot 2 of 2 — not an implement-stage run -->
  ```

- **Why it's a problem**: the DoD block is the stage's own completion claim; leaving it `pending` after 60 `[X]` rows and all evidence makes the artifact contradict itself. DoD-1 requires T061's reason in `verification.md` under `deferred_tasks=`, which is absent.
- **Proposed fix**: set the DoD status after the close-out and record `deferred_tasks=T061 — driver closure stage after review` in `verification.md` (or change DoD-1's carrier if a `[~]` row's inline comment is deemed sufficient).

### F6 — `code-review` receipt refuses a legal binary skip selector

- **Severity**: P2
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/skills/internal/code-review/scripts/git-delta-review.sh:1035-1042,1178-1187`
- **Evidence** (verbatim quote):

  ```
  SKIP_REASONS_LEGAL=( non-code-file generated binary … )

  if [[ "$stat_a" == "-" || "$stat_d" == "-" ]]; then
      echo "行数无法测量 (binary): ${stat_rest:-?}" >&2
      echo "不可量测的数字字段意味着不写块 (C-41 / V16)" >&2
      exit 2
  fi
  ```

  This review's delta carries three `.log.gz` evidence files; `receipt --skip-with-reason '*.gz' --reason binary`
  still exits 2 before applying the selector.

- **Why it's a problem**: the skill declares `binary` a legal skip reason but measures line counts over all files before honoring skip selectors, so a legal skip cannot be used and the composed path has no receipt block (an input error). The reviewer must either hand-write a block or patch the tool.
- **Proposed fix**: apply the skip selectors before the line-count loop and exclude matched binary paths from the aggregate; add a contract case with a binary file plus a `binary` skip selector.

### F7 — A user-ruled constitution amendment rides inside the 098 delta with no 098 task row

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/constitution.md:1-11`; commit `af73f65f1`
- **Evidence** (verbatim quote):

  ```
  - Modified principles: VII. Workflow Gates — the Pre-Status-Flip Gate's status-line
    carrier is corrected from `verification.log` to `verification.md` … User ruling
    (2026-11-10): amend the constitution to the framework carrier …
  ```

- **Why it's a problem**: the review range contains a framework-governance change that no 098 requirement or task row asks for. It is authorized by the commit's recorded user ruling, but the only trace is that Sync Impact Report — the feature's delta and the register do not attribute it.
- **Proposed fix**: register the ruling as a decision row (D-…) in `.specify/register.md` at the moment it lands, or split such edits out of a feature delta; the implement scope audit should name every out-of-plan commit.

### F8 — T012 claims "obligations 1–11" while obligation 11 did not exist at that row

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/tasks.md:91`; `/…/test-evidence/tier-contract-green.txt:7-14`
- **Evidence** (verbatim quote):

  ```
  Run `tests/contract/test_suite_tier_contract.py` (obligations 1–11) …
  (tasks.md:91)

  Obligation 11 … is authored at T021 (US2, still `[ ]`, blockedBy T020):
  `grep -c "def test_obligation_11" tests/contract/test_suite_tier_contract.py` → `0`.
  (tier-contract-green.txt:8-10)
  ```

- **Why it's a problem**: a task row's scope must be what the run measured. The record is honest, but the row still says "1–11" and would let a reader believe the full file was green at T012.
- **Proposed fix**: change T012 to "obligations 1–10 plus slow-membership guard cases" and let T021/T022 carry obligation 11, as the evidence already states.

## 4. What Worked — Preserve (Brief)

- The tier contract is genuinely behavioral: obligations run on throwaway fixture trees with registered markers, and the 13 mutation legs (TS/SL) are recorded red.
- The evidence records disclose their own deviations instead of hiding them (baseline timing at WP-9, S-4 flake attribution, the two-slot scope reading).
- Mirror discipline is clean: `sync-mirrors.py --check` exits 0, the four pairs are byte-identical (the runner pair is the declared projection), and no mirror was hand-edited.
- The in-process manifest is closed over an AST census (503 rows, 147 convert / 356 keep, 112 convert files) and the guard names an unclassified site or a reverted conversion.
- The injected clock (`--now`) is default-off and the default path is byte-identical; the scan cache is deep-copied and session-keyed.
- The three analyze rounds caught and repaired the clause-id form defect before implement; clause coverage is 27/27 FR, 0 uncovered beyond the frozen baseline.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-098-01 — The baseline row cannot be scheduled last** — Target: `templates/commands/tasks.md` § Work Package Mapping (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/templates/commands/tasks.md`). Change: reject a WP mapping in which a "Phase 1 / starts immediately" baseline row is assigned to the last package; require the baseline row to precede every behavior-changing package (e.g. `[blockedBy: T003]` on all WPs). Source: F3/A3/I3. Expected impact: the two-slot baseline keeps its pre-change referent by construction.

### 5.2 Command Prompt Improvements

- **REC-098-02 — Review must refuse a slice without its implement close-out** — Target: `templates/commands/review.md` § Failure propagation (absolute supplement: `…/templates/commands/review.md`). Change: before the four segments, require `verification.md` and a `closure-acceptance-check.py` record for the slice; an absent carrier is a named halt, not a review that produces findings over a missing evidence base. Source: F1/A1/I1. Expected impact: no review is asked to judge a transition that was never prepared.
- **REC-098-03 — The state spine is a dispatch precondition** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` § Stall Handling & State Spine (absolute supplement: `…/skills/external/sdd-loop-driver/references/stage-prompts.md`). Change: every stage's U2/U3/U4 writes the spine, and dispatching review when the spine's stage is not the implement close-out is a fast fail with the stale field named. Source: F2/F4. Expected impact: re-entry never resumes at a stale stage.

### 5.3 Automation / Script Improvements

- **REC-098-04 — Skip selectors precede binary line measurement** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (absolute supplement: `…/.specify/skills/internal/code-review/scripts/git-delta-review.sh`). Change: apply `--skip-with-reason` selectors before the `--numstat` binary refusal, exclude matched paths from `lines_added/lines_deleted`, and add a binary-file contract case. Source: F6. Expected impact: a legal `binary` skip yields a real receipt block instead of exit 2.

### 5.4 Workflow Improvements

- **REC-098-05 — A final-path criterion's latest measurement outranks its label** — Target: `shared/workflow/acceptance-hardening.md` § Review Composition / § Gates (absolute supplement: `…/shared/workflow/acceptance-hardening.md`). Change: when a same-tree re-measurement of a `final`-path criterion is non-empty (or otherwise contradicts the criterion), the review must refuse the transition and name the criterion; an evidence record may not substitute a weaker reading ("0 new names") for the declared one ("both comm directions empty"). Source: A2/I2. Expected impact: acceptance honesty is mechanical, not interpretive.

### 5.5 Documentation Improvements

- **REC-098-06 — Out-of-plan commits are named by the implement scope audit** — Target: `templates/commands/implement.md` § scope/deletion-surface audit (absolute supplement: `…/templates/commands/implement.md`). Change: the audit must enumerate every commit in `base..head` that no task row asks for and require a recorded user ruling (register D-row or split commit). Source: F7. Expected impact: a feature delta stays attributable to its own requirements.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Re-run the implement close-out (verification.md + checker) before any status judgement | `.specify/specs/098-suite-speed-optimizations/verification.md` + `closure-acceptance-check.py` | F1/A1/I1 |
| P0 | Re-measure SC-002 on the final tree; repair or register the two serial-only names | `notes/quickstart-run.md` § S-4 / `parallel-consistency.contract.md` C-002/C-004 | A2/I2 |
| P1 | Make the baseline row precede all behavior-changing packages | `templates/commands/tasks.md` § Work Package Mapping | F3/A3/I3 |
| P1 | Refresh the state spine and write the missing checkpoints | driver state spine + `checkpoints/` | F2/F4 |
| P2 | Fix the receipt binary/skip ordering | `skills/internal/code-review/scripts/git-delta-review.sh` | F6 |
| P2 | Register the user-ruled constitution amendment; correct T012's scope | `.specify/register.md` / `tasks.md` T012 | F7/F8 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: five P0 findings (F1, A1, A2, I1, I2) were independently validated by fresh-context read-only subagents; all returned `confirm (P0)`, none was downgraded or rejected.

## 8. Feedback

This document is the process/artifact/implementation-side review of the 098 slice. The code-side record is the separate `code-review.md` (`blocking_entries=0`, `important=1`, `suggestion=1`, gate `allow`).

## Conclusion — status transition judgement

**`Implemented → Ready for Review` is REFUSED.** The bound feature 086 claims `Ready for Review`; this review leaves that claim unchanged (a refusal is not a downgrade) and does not present itself as a completed review. Named conditions:

1. **No implement close-out**: `verification.md` is absent, so there is no status row for any criterion, no smoke record and no `deferred_tasks=` carrier. The `Planned → Implemented` four conditions are not evidenced, let alone the review gate's four.
2. **SC-002's latest same-tree measurement contradicts the criterion**: `comm -13` = 2 serial-only names on the final tree; the record substitutes "0 new failure names", which is not SC-002 and not C-004.
3. **SC-003/SC-005 cannot be judged at review time**: both are `final`-path criteria whose readings are defined to come from the closure stage (T061), which by the driver's order runs after review; T061 is still `[~]`.
4. **No waiver exists**: the driver's or an agent's confirmation is not a user ruling; no user waiver names any criterion.

The next action is to repair the evidence base (close-out + final-tree SC-002 re-measurement) and re-run this review; the code segment itself has no `blocking` entry.

---

## Placeholder Glossary (report tokens)

| Token | Meaning / Source |
|-------|------------------|
| F1…F8 | Stable process-segment finding IDs used to cross-reference Section 5 |
| A1…A4 | Artifact-segment findings (`### 2.2`) |
| I1…I3 | Implementation-segment findings (`### 2.3`) |
| REC-098-01…06 | Framework recommendations registered in `.specify/register.md` with this report |
| `blocking-unresolved` | The named refusal literal for an unattended transition refusal (owned by `templates/feature-details-template.md` § Canonical Status State Machine) |
