# Specification-Driven Development (SDD) Process Review Report: Batch Decision Panel（批量决策面板）— 112-decision-batch-panel

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap or a review finding, it does not belong here.

## Segment Verdicts (one composed run, fixed order)

| Order | Segment | Verdict | Findings (own vocabulary) |
|-------|---------|---------|---------------------------|
| 1 | process | **pass** | 0 P0 · 4 P1 · 0 P2 |
| 2 | artifact | **pass** | 0 P0 · 2 P1 · 4 P2 |
| 3 | implementation | **pass** | 0 P0 · 2 P1 · 2 P2 |
| 4 | code | **blocked** (receipt 339 changed / 19 judged / 320 legally skipped / 0 gap; 2 blocking; gate `blocking-unresolved`) | 2 blocking · 2 important · 1 suggestion · 1 question · 1 praise |
| — | Acceptance Reality Check | **agree** (`final_path` pass 7 / total 7; four completion conditions true) | — |
| — | **Consolidated review verdict** | **blocked** | **blocking findings: 2 (code segment)** |

Status transition: **not performed.** The code segment's merge gate refuses (`blocking-unresolved`, 2 blocking entries), so Feature 112 stays `Implemented` on both carriers (`.specify/features.md` row 112 and `.specify/features/112-decision-batch-panel.md`). ARC itself agrees; the refusal is the code gate's, not ARC's.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 112 |
| Requirement Key | 112-decision-batch-panel |
| Requirement Name | Batch Decision Panel（批量决策面板） |
| Related Feature | 112 Batch Decision Panel（批量决策面板） |
| Repository | spec-kit (`specify-cli`, framework version answered by the engine's `--version`) |
| Repository URL | `(no single resolvable URL for this commit)` — four remotes exist: `gitee` git@gitee.com:cloud-native-ai/spec-kit.git, `github` git@github.com:cloud-native-ai/spec-kit.git, `gitlab` git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git, and `origin` **which is the UPSTREAM** git@github.com:github/spec-kit.git |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the commit is unpushed. Every citation below is repo-relative plus this worktree's absolute path; recover any file with `git show 838e7acb4650512bceefd689fec8e0da07c78f6d:<repo-relative-path>` |
| Branch | 112-decision-batch-panel (git worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`; the main tree stays on master) |
| Commit SHA | 838e7acb4650512bceefd689fec8e0da07c78f6d (short: 838e7acb4) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (fresh-context subagent; the four segments and ARC executed in one consolidation pass — no segment was produced by the implement executor) |
| Environment | Linux x86_64; bash 4.4.20; Python 3.11.11; git 2.43.5; tests through `scripts/bash/run-tests.sh`; the pytest-capable interpreter on this host is `/usr/local/bin/python3` (the bare `python3` on PATH is a profile venv without pytest) |
| spec-kit Source Snapshot | this repository itself @ 838e7acb4 (dogfooding: framework sources and the client runtime live in one tree) |

**Baseline note (transparent):** the dispatch brief names `0419adae5` as the code-review baseline, while the code skill's own `base` route resolves `c3489e52c` (`base_source=feature-first-commit`) for this spec. `0419adae5` is an ancestor of the branch base and `0419adae5..c3489e52c` belongs to prior lines (109 and earlier), so the judged delta is `c3489e52c..838e7acb4` (339 files). Both facts are recorded; the code record carries the resolved pair.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 438 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel/.specify/specs/112-decision-batch-panel/requirements.md | 45 FR / 10 SC, A-1…A-27, RS-001…RS-008, 16 clarification Q rows |
| plan.md | 178 | …/112-decision-batch-panel/plan.md | 23-row Constitution Check, 7 execution premises EP-001…EP-007, PA1–PA6, project structure and mirror obligations |
| tasks.md | 432 | …/112-decision-batch-panel/tasks.md | 58 rows T001–T058, tests mode ON, 54 clause green claims, 8 gates |
| data-model.md | 265 | …/112-decision-batch-panel/data-model.md | 13 entities E-1…E-13, 22 invariants I-1…I-22, 5 state domains |
| research.md | 61 | …/112-decision-batch-panel/research.md | 14 measured baselines M-1…M-14 and 12 resolved design points D-1…D-12 |
| quickstart.md | 123 | …/112-decision-batch-panel/quickstart.md | 7 scenarios pinned by named tests and premises |
| feature-ref.md | 110 | …/112-decision-batch-panel/feature-ref.md | FR-001…FR-045 delivery map and integration authority |
| contracts/ (6 files) | 222 | …/112-decision-batch-panel/contracts/ | 54 clauses C-101…C-110, C-201…C-208, C-301…C-307, C-401…C-409, C-501…C-512, C-601…C-608 |
| checklists/ (2 files) | 150 | …/112-decision-batch-panel/checklists/ | requirements validation + 40-item requirements-quality instrument |
| verification.md | 97 | …/112-decision-batch-panel/verification.md | 10 SC rows (all pass) + 3 in-scope RS joint-acceptance rows; smoke record and baseline |
| checkpoints/ (7 files) | — | …/112-decision-batch-panel/checkpoints/ | Checkpoint 01 requirements … 07 implement |
| feature registry row + detail | — | .specify/features.md row 112; .specify/features/112-decision-batch-panel.md | Registry status `Implemented`; detail status `Implemented` with stale Status Tracking (F7) |
| test-evidence/ (~100 files) | — | …/112-decision-batch-panel/test-evidence/ | Gate captures, red-first/green readings, closure JSON, stage inputs and records |
| review.md / code-review.md | — | …/112-decision-batch-panel/ | This report and the code-segment record |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Line entry, U0/U1 probe: worktree on `112-decision-batch-panel`, base `c3489e52c`, breakpoint requirements; runs concurrently with lines 110/111 | spine `/storage/project/cloud-native-ai/spec-kit/.specify/state/decision-batch-panel.md` § U0/U1 | no |
| 2 | requirements attempt 1 pass: 45 FR / 10 SC + quality checklist; the spec was scaffolded **by hand** because the creator self-counts the current branch | commits `4a6cfa0ec`, `fbdc3819c`; `requirements.md:70` A-19 | **yes — manual scaffold** (F4) |
| 3 | clarify pass: 16 `- Q:` rows adjudicated; the downstream count of 13 starts here | commits `8b7591f63`, `d53bd81cb`; `grep -c '^- Q:' requirements.md` = 16 | minor — stale count propagates (F9) |
| 4 | plan pass: plan/research/data-model/6 contracts/quickstart/feature-ref; test entry **not run** — the runner found no pytest interpreter in this worktree | commits `ab6a297dd`, `4c36be59a`, `3ff8efd2a`; `tasks.md:41` Environment Prerequisites | **yes — environment probe could not reach the host interpreter** (F1) |
| 5 | tasks pass: 58 rows, tests mode ON, 54 clauses partitioned, 8 gates | commits `db5001af3`, `908fbe4c3` | no |
| 6 | checklist pass: 40-item instrument, 45/45 FR / 10/10 SC / 54/54 clauses covered | commits `f045db102`, `91ff6a97b` | no |
| 7 | analyze round 1: 0 CRITICAL / 2 HIGH (I-01 batch isolation vs prior-batch read; I-02 supersession write-back vs batch immutability) / 6 MEDIUM / 8 LOW | commits `d45e61426`, `087b1c631` | no — the gate worked |
| 8 | analyze-repair: I-01/I-02 resolved at the owner surfaces as A-26 (cross-batch read boundary) and A-27 (single-field `superseded_by` append); derived carriers aligned | commits `ec9ca5686`, `8aad9c47d`; `test-evidence/analyze-repair-round1.md` | no |
| 9 | analyze round 2: 0 open CRITICAL/HIGH, 4 new M/L, 14 residues; the report says **the gate is not cleared** (G-01 baseline absent, G-02 FR-043 uncovered) while the driver records PASS (C/H = 0) | commit `f1410a4c3`, `78a60309b`; `analyze-round2-report.md:13`; spine U4 | **yes — two gate criteria disagree** (F2) |
| 10 | implement P1–P4: fixtures, engine, entry surfaces, US1–US5, guards; 58/58 closed; GATE-1…GATE-8 green; per-package commits and wrap-ups | `fc674b4f5`, `6581129aa`, `ebcdabf26`, `b8203c09b`, `8d5aafb37`, `9b1719c58`, `8fec0315f` | no |
| 11 | Implement closure (driver repair): `verification.md` derived spec-side from `verification-input.md`, RS-005/006/008 rows added, Feature 112 flipped to `Implemented`; closure checker `accept` (7/7) | commit `838e7acb4`; checkpoint 07 | **yes — the stage's required output was handed off and derived post-hoc** (F3/F6) |
| 12 | Review dispatch (this run): four segments + ARC; code `base` resolves `c3489e52c`, head fixed at `838e7acb4`; live feature smoke re-run `108 passed in 8.46s`, exit 0; the **recorded** smoke command (without the interpreter switch) exits 1; code gate denies with 2 blocking | this report; `code-review.md`; `test-evidence/implement-p4-full-suite.txt:55` | **yes — recorded command is not the executed command** (F5) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 8 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 6 |
| Workflow | 3 |
| Documentation | 3 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c3489e52c` | the resolved diff base |
| Head commit | `838e7acb4` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the code segment's `base` route |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 339 / 19 / 320 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `blocked` | the code skill's four closed values |
| Gate verdict | `blocking-unresolved` | the merge gate; `report --summary --file` exits 1 with 2 blocking entries |
| Reason, when one applies | none | no reason is needed; the refusal is the blocking set |
| Uncommitted scope | none beyond this run's own records (`review.md`, `code-review.md`) and the ignored scratch `.specify/.tmp/review-smoke-112.txt`; no product file is uncommitted | disclosed, never concluded over; the same sentence lives in `.specify/specs/112-decision-batch-panel/code-review.md` |
| Record | `.specify/specs/112-decision-batch-panel/code-review.md` | written (triage `run`) |
| Archive | `none` | first run |

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, data-model.md, research.md, quickstart.md, feature-ref.md, contracts/ (6 files), checklists/ (2 files), verification.md, checkpoints/ (7 files), .specify/features.md row 112 + .specify/features/112-decision-batch-panel.md | derived from the stage rules and `plan.md` § Project Structure |
| Coverage line | 12 / 12 | all expected members present |
| Missing members | none | — |
| Segment verdict | `pass` | no P0 |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | .specify/specs/112-decision-batch-panel/verification.md | 19 | none | The recorded smoke command omits the interpreter switch and exits 1 verbatim; the recorded exit 0 came from a different command (F5) |
| P1 | .specify/specs/112-decision-batch-panel/verification.md | 7 | none | `baseline_commit` is the P4 package base, not the implement-run start; `post_change_commit`, the checker verdict/reasons and the evidence-binding rows are absent (F6) |
| P2 | .specify/features/112-decision-batch-panel.md | 72 | none | Status Tracking still marks `Planned` as current while the header says `Implemented`; Latest Review stops at the plan stage (F7) |
| P2 | .specify/specs/112-decision-batch-panel/verification.md | 93 | none | RS joint-acceptance rows carry prose instead of the template's closed verdict token (F8) |
| P2 | .specify/specs/112-decision-batch-panel/plan.md | 5 | none | The clarification-row count says 13 while the requirements carry 16; tasks.md and feature-ref.md copy the stale number (F9) |
| P2 | .specify/specs/112-decision-batch-panel/tasks.md | 23 | none | DoD-7 names SC-010 in the final set while requirements.md marks it `supporting`; the closure checker counts 7 (F10) |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c3489e52c` | the resolved diff base |
| Head commit | `838e7acb4` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the code skill's `base` route |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py tests/contract/test_decision_governance_guards.py tests/contract/test_migration_distribution.py tests/contract/test_probe_nonentity_catalog.py tests/unit/test_validate_decisions.py -q` | recorded verbatim; this review's own re-run |
| Smoke exit code | 0 — `108 passed in 8.46s` | this review's re-run; the implement run recorded the same 108/8.43 s |
| Smoke evidence path | .specify/specs/112-decision-batch-panel/test-evidence/implement-p4-full-suite.txt (exists, non-empty; line 55 carries the 108-passed reading) | verification.md |
| Scope and regression verdict | Scope clean: the 339-file delta's code surface is the 19 judged files; no unreferenced hunk; the frozen rosters moved only their pins; mirrors and generated copies are byte-identical. Regression: full suite `229 failed / 10412 passed` vs the `8d5aafb37` base `229 failed / 10404 passed`, zero NEW failed names; the review's live smoke is green. | this segment's reading; `implement-p4-full-suite.txt` |
| Segment verdict | `pass` | no P0 |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | scripts/python/decision-batch.py | 806 | none | The user-facing completeness disclosure prints the roster source ids and the presence token; C-204/FR-020 forbid internal identifiers in the body (F11) |
| P1 | tests/contract/test_decision_batch_contract.py | 216 | none | The C-204 guard's token set and single fixture let the two leak loci pass green (F12) |
| P2 | scripts/python/decision-batch.py | 690 | none | Option-level missing elements are reduced to a generic reason; C-202's "named missing elements" is met only for block fields (F13) |
| P2 | scripts/python/decision-batch.py | 540 | none | `explicit_repo_path`/`resolve_pointer` accept `..`, so a register authority cell can resolve outside the workspace and the block-update path can write there (F14) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/features/112-decision-batch-panel.md` and `.specify/features.md` row 112 |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/112-decision-batch-panel --repo . --feature-detail .specify/features/112-decision-batch-panel.md --feature-registry .specify/features.md --json` |
| Comparison verdict | `agree` | checker `verdict: accept`; four completion conditions true; claimed status `Implemented` |
| Failed condition, on refusal | none | no refusal |
| Fixed item, on refusal | none | no refusal |

## 3. Findings (Problems & Improvement Targets)

### F1 — The test-entry interpreter ladder misses the host's pytest interpreter

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `scripts/bash/run-tests.sh` § interpreter ladder (lines 64–74); `.specify/specs/112-decision-batch-panel/tasks.md:41`; `.specify/specs/112-decision-batch-panel/verification.md:19`
- **Evidence** (verbatim quote):

  ```
  for candidate in "${SPECKIT_PYTHON:-}" "$repo_venv" ".venv/bin/python" "python3" "python"; do
  ...
  error: no interpreter with pytest found (tried SPECKIT_PYTHON, .venv/bin/python, python3, python)
  ```

- **Why it's a problem**: the host's pytest-capable interpreter is `/usr/local/bin/python3`; the bare `python3` on PATH is a profile venv without pytest. The plan stage therefore could not run a single test, and every later stage had to pass `SPECKIT_PYTHON` by hand. The switch then vanished from the recorded smoke command (F5), turning the acceptance record into a non-reproducible claim.
- **Proposed fix**: probe the host's absolute interpreters (e.g. `command -v -a python3` plus `/usr/local/bin/python3`) for `import pytest`, print the resolved interpreter in the runner's output, and name the resolved form in the verification template's smoke record.

### F2 — The analyze gate verdict contradicts itself

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-report.md:13`; `.specify/specs/112-decision-batch-panel/checkpoints/06-analyze.md`; state spine § U4 analyze round 2
- **Evidence** (verbatim quote):

  ```
  **The analyze gate is NOT cleared**: G-01 (`baseline-missing`, clause-delta lane unjudgeable), G-02 (FR-043 uncovered) and I-03 (SC-010 Path drift) remain.
  ```

- **Why it's a problem**: the driver recorded `U4 — analyze round 2: PASS … Gate pass` using the C/H = 0 criterion, while the stage's own report says the gate is not cleared. A reader cannot tell whether analyze passed, and the implementation proceeded on a narrower reading than the report's.
- **Proposed fix**: single-source the analyze gate criterion in the analyze skill/command, have the report emit one machine-readable `gate=pass|fail` value per that criterion, and make the driver consume that emitted value instead of re-deriving C/H.

### F3 — The implement stage's verification output is redefined and derived post-hoc

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/112-decision-batch-panel/tasks.md:14` (DoD-1); `.specify/specs/112-decision-batch-panel/test-evidence/verification-input.md:3-6`; `templates/commands/implement.md:58-60`; `.specify/specs/112-decision-batch-panel/verification.md:3`
- **Evidence** (verbatim quote):

  ```
  the P4 task rows author this `verification-input.md` instead of `verification.md`.
  `verification.md` is derived **spec-side** from this input and MUST NOT be written by the implement executor.
  ```

- **Why it's a problem**: the implement command makes `verification.md` the stage's own gate product, populated before the status flip; the task authoring moved that output to a hand-off file and the driver wrote it after the stage. The derivation then dropped template obligations (F6) and the checker's verdict/reasons are nowhere in the record.
- **Proposed fix**: have the implement executor populate `verification.md` per step 9; if a derivation step is kept, declare it in the command/skill, make it template-conformant (all baseline/result/evidence fields), and record the checker's verdict and reasons in the file.

### F4 — The manual requirements scaffold recurs a third time

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/112-decision-batch-panel/requirements.md:70` (A-19); 109 review F1 and recommendation REC-A1
- **Evidence** (verbatim quote):

  ```
  `create-new-requirements.sh` 会把该分支计入编号空间并派生 113 且新建分支，与本线「停留在既有分支、编号 112」冲突。按 107/109/110 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到本目录
  ```

- **Why it's a problem**: the 109 review already diagnosed the same self-counting branch and recommended an explicit in-place mode; it was not implemented, so 112 pays the manual scaffold and template-fidelity hand-check again. This is the third recorded occurrence (108 A-16, 109 F1, 112 A-19).
- **Proposed fix**: implement the in-place mode (`--feature-id <NNN>` / `--branch <name>`) in `scripts/bash/create-new-requirements.sh`, expose it in `-h`, and name it in the requirements stage brief.

### F5 — The recorded smoke command is not the command that produced the reading

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `.specify/specs/112-decision-batch-panel/verification.md:19-21`
- **Evidence** (verbatim quote):

  ```
  smoke_command=bash scripts/bash/run-tests.sh tests/unit/test_decision_batch_engine.py ... tests/unit/test_validate_decisions.py -q
  smoke_exit_code=0
  ```

  Executed verbatim on this host: `error: no interpreter with pytest found (tried SPECKIT_PYTHON, .venv/bin/python, python3, python)` — exit 1. The reading was produced by `env SPECKIT_PYTHON=/usr/local/bin/python3 bash …` (this review's re-run: `108 passed in 8.46s`, exit 0).

- **Why it's a problem**: the smoke triple's command/exit pair is false as written; a downstream verifier following the record gets exit 1. The template explicitly allows the `env SPECKIT_PYTHON=…` form and warns against a leading bare assignment, and 109's record used that form.
- **Proposed fix**: re-record the command as `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh … -q`, re-run it, and keep the exit code and evidence path in the record.

### F6 — verification.md omits template-required fields and uses the wrong baseline

- **Severity**: P1
- **Category**: Template
- **Location**: `.specify/specs/112-decision-batch-panel/verification.md:7`; `templates/verification-log-template.md` § Baseline / Implementation results / Evidence records; `templates/commands/implement.md:58-60`
- **Evidence** (verbatim quote):

  ```
  baseline_commit=8d5aafb37
  ```

  The template requires `baseline_commit` to be the run-start commit, "recorded once, BEFORE any /speckit.implement work changes the tree", and `post_change_commit` to be the run-end commit. The implement stage began at `e4692034e` (checkpoint 06); `8d5aafb37` is the P4 package base. No `post_change_commit=` line exists, no checker verdict/reasons line exists (the command requires copying them), and the 10 `pass` rows carry no `sample_id` / `evidence_sha256` binding rows ("a `pass` without a complete evidence row is `unverified`" per the template).

- **Why it's a problem**: the recorded baseline window hides P1–P3 from any baseline comparison; the end tree is unnamed; the status claim's gate product is not recorded; and the hash-bound evidence rule is skipped. The record looks complete but cannot support the audit it claims.
- **Proposed fix**: regenerate the file from the template with `baseline_commit=e4692034e`, `post_change_commit=838e7acb4`, the checker's `verdict` and reasons, and one `sample_id` / `evidence_path` / `evidence_sha256` / `verdict=pass` row per SC.

### F7 — The feature detail's status tracking and Latest Review are stale

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/features/112-decision-batch-panel.md:72`; the Latest Review block at lines 18–21
- **Evidence** (verbatim quote):

  ```
  - **Planned**: plan/design artifacts exist for the bound spec and the Constitution Check has no unjustified Fail rows. (current — 2026-11-27)
  ```

  while line 6 says `**Status**: Implemented` and the Latest Review ends at the plan stage.

- **Why it's a problem**: the bound feature detail contradicts its own header and the registry on which rung the feature occupies; the stage log omits tasks, checklist, analyze and implement. A reader acting on the detail cannot tell that the feature is implemented (or what evidence backs it).
- **Proposed fix**: mark `Planned` historical, mark `Implemented` current with the checker's 7/7 reading and the stage entry, and add the missing Latest Review entries (the 109 detail is the recent convention).

### F8 — The RS joint-acceptance rows lose the closed verdict token

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/specs/112-decision-batch-panel/verification.md:93, 95, 97`
- **Evidence** (verbatim quote):

  ```
  RS-005_joint_acceptance=verified by behaviour on the delivered tree: batch records pass the decision-record grammar ...
  ```

  The template's row takes exactly one of the closed verdicts pass / fail / partial / blocked / deferred / unknown; the input (`verification-input.md:25-31`) carried `pass`.

- **Why it's a problem**: prose is not a verdict from the closed domain; the closure checker only tests row presence, so the loss is silent. The same drift exists in 109's record, so it is recurring.
- **Proposed fix**: restore the verdict token (`pass`) and move the evidence sentence to an `RS-NNN_note=` line; add a template/checker check on the value domain.

### F9 — The clarification-row count is stale in three artifacts

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/112-decision-batch-panel/plan.md:5`, `.specify/specs/112-decision-batch-panel/tasks.md:7`, `.specify/specs/112-decision-batch-panel/feature-ref.md:5`
- **Evidence** (verbatim quote):

  ```
  **Input**: Specification from `.specify/specs/112-decision-batch-panel/requirements.md` (45 FR / 10 SC; Assumptions A-1…A-27; 13 clarification rows), ...
  ```

  Measured: `grep -c '^- Q:' requirements.md` = **16** (the checklist's own reading recorded 11 + 5 = 16; residue I-05).

- **Why it's a problem**: the same fact has two spellings; every downstream reader who trusts the plan/tasks headers under-counts the adjudications. The checklist disclosed the disagreement but the carriers were not corrected.
- **Proposed fix**: correct the three headers to 16 (or point at the requirements § Clarifications) and add a count check to the plan/tasks validators.

### F10 — The final-path set is stated three ways

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/112-decision-batch-panel/tasks.md:23` (DoD-7), `tasks.md:32` (GATE-4), `.specify/specs/112-decision-batch-panel/requirements.md:366`
- **Evidence** (verbatim quote):

  ```
  - DoD-7: ... `final` 路径判据（SC-001…SC-007、SC-010）记 `pass` ...
  ```

  while `requirements.md:366` says `- **SC-010**: ... **Path**: supporting`. The closure checker counts 7 final criteria; `verification-input.md:31-34` reconciles the wording.

- **Why it's a problem**: a reader (or a future validator) can read the final set as 8 and disagree with the checker's 7. The reconciliation lives in an evidence file, not in the artifact that made the claim.
- **Proposed fix**: align DoD-7/GATE-4 to the requirements Path markers, and keep the reconciliation in the tasks' own wording.

### F11 — The user-facing presentation carries machine identifiers

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `scripts/python/decision-batch.py:801-809` (source ids/presence), `:926-931` (field names)
- **Evidence** (verbatim quotes from live scans):

  ```
  本次扫描读取了封闭来源清单中的全部来源（register-open-decision-row 在场状态为 read，候选 2 项；authored-pending-item 在场状态为 read，候选 6 项）
  ```

  ```
  当前状态：信息不完整，本次不会结案（缺少必填内容：decision_class）。
  ```

- **Why it's a problem**: FR-020 and contract C-204 say the user-facing body MUST NOT carry field names, status tokens or other internal identifiers; the completeness disclosure prints two roster ids and the `read` presence token on every scan, and incomplete items print raw field names. The presentation is the feature's primary product surface. The code segment records this as 2 blocking entries; the implementation consequence is that SC-002/C-204 is not delivered for the affected rows.
- **Proposed fix**: render plain-language source names and presence ("登记册中的待定决策行：已读取；项目文档中的待决策条目：已读取") and a field-label map (`decision_class` → 决策类别, `context` → 上下文, …) mirroring `REASON_TEXT`; keep the JSON payload unchanged.

### F12 — The C-204 guard misses both leak loci

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `tests/contract/test_decision_batch_contract.py:216-238`
- **Evidence** (verbatim quote):

  ```
  INTERNAL_TOKENS = (
      "decision_class", "recommended_default", ... "malformed-field",
  )
  ...
  root = tmp_path / "two-source"
  ```

  The token set omits `register-open-decision-row`, `authored-pending-item` and `read`; the test scans only `two-source`, which never enters the missing-field rendering path.

- **Why it's a problem**: the green C-204 test is cited as the machine evidence for the identifier boundary, but it cannot detect either leak; F11 ships under a passing guard. A green check that would not go red when its subject breaks proves nothing.
- **Proposed fix**: add the roster ids and presence words to `INTERNAL_TOKENS`, scan the `incomplete-block` and `autonomous` fixtures, and assert the field-label rendering specifically.

### F13 — Option-level missing elements are not individually named

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `scripts/python/decision-batch.py:690-696`, `:926-931`; contract C-202 / FR-019
- **Evidence** (verbatim quote):

  ```
  for defect in primary_block["defects"]:
      reasons.append(defect[0])
  ...
  "option-element-missing": "存在要素不全的选项",
  ```

  The defect tuple's `(line, name)` detail is dropped, and the reason text names no option or element.

- **Why it's a problem**: C-202 requires an incomplete item to show all content and "逐项点名缺失要素"; block-level fields are named (`缺少必填内容：context`), but an option missing `evidence`/`consequences` only yields the generic sentence and an empty value in the options list. A reader cannot tell which element to author.
- **Proposed fix**: carry the option label and element name into the qualification (with a plain-language label map) and render them in the state sentence; add a fixture with one option element missing.

### F14 — Path containment is not enforced for register-linked carriers

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `scripts/python/decision-batch.py:538-541` (`explicit_repo_path`), `:426-444` (`resolve_pointer`), `:1673-1674` (`apply_text_update`); the code record's important entry at `scripts/python/decision-batch.py:540`
- **Evidence** (verbatim quote):

  ```
  match = re.match(r"^(?:\./)?(\.specify/[A-Za-z0-9._/-]+\.md)$", cleaned)
  ```

  Probe: `explicit_repo_path('.specify/../../outside/doc.md')` returns the string; `(root / rel).resolve()` lands at `/outside/doc.md`. The same acceptance exists on the read side in `resolve_pointer`.

- **Why it's a problem**: a register authority cell can point a `### PENDING —` block outside the workspace, and `record`'s block-update path would append a `resolution` line there — outside the declared write surface. The owner requires an explicit repository-relative path; `..` is not containment-safe.
- **Proposed fix**: reject `..` segments and assert the resolved path stays under the workspace root in both `explicit_repo_path` and `resolve_pointer`; add a reverse-sample test.

## 4. What Worked — Preserve (Brief)

- The deterministic engine with closed actions/exit codes, a real `--help`/`--version` face and standard-library-only dependencies; scan/replay write nothing and `record` is the only writer.
- Create-only discipline: the candidate batch id is derived as a pure string, the duplicate check runs before the write surface, and the batch id is adopted only after every precondition; the suite backs this with zero-write snapshots across drift, unattended, membership, duplicate and unwritable-prior refusals.
- Red-first evidence per test slot with command, real output and exit code — including the honest "green at authoring, not claimed red-first" disclosure for R-C307.
- Mirror and generated-copy parity exact (`cmp` byte-identical for engine, owner page and skill; `sync-mirrors.py --check` rc 0; `regen-command-copies.py --check` rc 0), and the frozen rosters moved 32→33 / 60→61 with same-change comments in each guard.
- Analyze round 1 caught two HIGH contradictions and the repair resolved them at the owner surfaces with A-26/A-27 and one-hop carrier alignment; round 2 re-read the full declared domain.
- Objection-only/silence semantics tested across four reply forms; register status-cell updates, `resolution` appends and the single-line `superseded_by` append are all byte-level tested.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-T1 — Make the verification log's smoke and evidence fields executable** — Target: `templates/verification-log-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel/templates/verification-log-template.md`). Change: state the `env SPECKIT_PYTHON=…` command form as the example, require the recorded command to be the executed one, and make the evidence-binding rows (`sample_id` / `evidence_path` / `evidence_sha256` / `verdict`) mandatory for each `pass`. Source: F5, F6. Expected impact: the smoke triple becomes reproducible and every `pass` is hash-bound.
- **REC-T2 — Separate the RS verdict from its evidence sentence** — Target: `templates/verification-log-template.md` § Joint acceptance. Change: pin `RS-NNN_joint_acceptance` to the closed token domain and give the evidence sentence its own `RS-NNN_note=` row; add the domain to the closure checker. Source: F8. Expected impact: the machine reader keeps a verdict instead of prose.

### 5.2 Command Prompt Improvements

- **REC-C1 — Put the verification hand-off in the command, not in task authoring** — Target: `templates/commands/implement.md` § Step 9 and `templates/tasks-template.md` (absolute supplements: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel/templates/…`). Change: make `verification.md` the implement executor's own output (or declare a derivation sub-step with all template fields and the checker verdict/reasons), and forbid a task row from redefining the stage's output. Source: F3, F6. Expected impact: the status-flip ordering (checker → copy verdict → write status) stays observable and the record is complete.

### 5.3 Automation / Script Improvements

- **REC-A1 — Resolve the pytest interpreter on the host** — Target: `scripts/bash/run-tests.sh` (absolute supplement: `…/scripts/bash/run-tests.sh`). Change: try `command -v -a python3` and `/usr/local/bin/python3` for `import pytest`, print the resolved interpreter, and name the resolved form in the runner's smoke/template guidance. Source: F1, F5. Expected impact: the plan stage can run its test entry and the recorded smoke command stops losing the switch.
- **REC-A2 — Render plain-language source/presence/field labels** — Target: `scripts/python/decision-batch.py` (absolute supplement: `…/scripts/python/decision-batch.py`). Change: add label maps for the roster source ids, the presence readings and the block field names, and use them in `batch_context`/`state_sentence`; keep the JSON payload as the machine channel. Source: F11. Expected impact: C-204/FR-020 holds on the primary user surface.
- **REC-A3 — Extend the C-204 guard** — Target: `tests/contract/test_decision_batch_contract.py` (absolute supplement: `…/tests/contract/test_decision_batch_contract.py`). Change: add the roster ids and `read` to `INTERNAL_TOKENS`, scan the incomplete-block and autonomous fixtures, and assert the field-label rendering. Source: F12. Expected impact: the guard goes red when the leak returns.
- **REC-A4 — Enforce carrier containment** — Target: `scripts/python/decision-batch.py` (absolute supplement: `…/scripts/python/decision-batch.py`). Change: reject `..` in `explicit_repo_path` and `resolve_pointer`, and assert the resolved path stays under the workspace root before any read or write; add the reverse sample. Source: F14. Expected impact: the declared write surface is closed.
- **REC-A5 — Name option-level missing elements** — Target: `scripts/python/decision-batch.py` (absolute supplement: `…/scripts/python/decision-batch.py`). Change: carry the option label and element into the qualification and render them; add a fixture with one missing option element. Source: F13. Expected impact: C-202's "named missing elements" holds for options too.

### 5.4 Workflow Improvements

- **REC-W1 — Single-source the analyze gate criterion** — Target: `.specify/skills/internal/analyze-artifacts/SKILL.md` and the analyze report template (absolute supplements under `…/.specify/`). Change: emit one `gate=pass|fail` value per the same criterion the driver consumes; stop carrying a second G-01/G-02 checklist verdict. Source: F2. Expected impact: the stage verdict is unambiguous.
- **REC-W2 — Re-issue the in-place requirements scaffold** — Target: `scripts/bash/create-new-requirements.sh` (absolute supplement: `…/scripts/bash/create-new-requirements.sh`). Change: implement 109's REC-A1 `--feature-id/--branch` mode, expose it in `-h`, and name it in the requirements stage brief. Source: F4. Expected impact: removes the third-occurrence manual scaffold.
- **REC-W3 — Keep stage records self-describing** — Target: the implement/close-out stage brief (the driver's stage prompt). Change: require the baseline to be the stage-start commit and the end commit to be written before the flip. Source: F3, F6. Expected impact: the record's window matches the stage it describes.

### 5.5 Documentation Improvements

- **REC-D1 — Update the bound feature detail at every status change** — Target: `.specify/features/112-decision-batch-panel.md` (absolute supplement: `…/.specify/features/112-decision-batch-panel.md`). Change: move the `(current)` marker with the status and add the stage entries to Latest Review. Source: F7. Expected impact: the detail stops contradicting its own header.
- **REC-D2 — Correct the count and the final-set wording in place** — Target: `plan.md`, `tasks.md`, `feature-ref.md` (absolute supplements under `…/.specify/specs/112-decision-batch-panel/`). Change: state 16 clarification rows and align DoD-7/GATE-4 with the requirements Path markers. Source: F9, F10. Expected impact: one spelling per fact.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-A2 + REC-A3 — plain-language rendering and the widened C-204 guard | `scripts/python/decision-batch.py`; `tests/contract/test_decision_batch_contract.py` | F11, F12 |
| P1 | REC-T1 + REC-C1 + REC-W3 — reproducible smoke, evidence binding, verification hand-off | `templates/verification-log-template.md`; `templates/commands/implement.md` | F3, F5, F6 |
| P1 | REC-A1 — host pytest interpreter resolution | `scripts/bash/run-tests.sh` | F1, F5 |
| P1 | REC-W1 — single analyze gate verdict | analyze skill/command | F2 |
| P1 | REC-W2 — in-place requirements scaffold | `scripts/bash/create-new-requirements.sh` | F4 |
| P2 | REC-A4 — carrier containment | `scripts/python/decision-batch.py` | F14 |
| P2 | REC-A5 — option-level missing-element naming | `scripts/python/decision-batch.py` | F13 |
| P2 | REC-T2 — RS verdict token | `templates/verification-log-template.md` | F8 |
| P2 | REC-D1 + REC-D2 — detail and count/final-set corrections | feature detail; plan/tasks/feature-ref | F7, F9, F10 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. No P0 findings raised; the P0 independent-validation pass is vacuously satisfied. (The two code-segment blocking entries were found by this fresh-context review, not by the implement executor; they are recorded in `code-review.md` and were not subject to the P0 validator, which applies only to the process family's P0.)

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.