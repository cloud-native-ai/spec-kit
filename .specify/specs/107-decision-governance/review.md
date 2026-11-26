# Specification-Driven Development (SDD) Process Review Report: Decision Governance（AI Agent 决策项治理）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.
> **Segment verdicts (console conclusion)**: process `pass` (1 P0 repaired in-run) · artifact `pass` (coverage 10/10 after the in-run repair; A1 repaired) · implementation `pass` (smoke 43 passed, exit 0) · code `not-evaluated` (receipt 684/27/657/0; skips earn no coverage credit) · Acceptance Reality Check `accept` (`agree` with the claim).

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 107 |
| Requirement Key | `107-decision-governance` |
| Requirement Name | Decision Governance（AI Agent 决策项治理） |
| Related Feature | 107 Decision Governance（AI Agent 决策项治理） |
| Repository | spec-kit (self-hosting framework repository) |
| Repository URL | remotes: `gitee` git@gitee.com:cloud-native-ai/spec-kit.git · `github` git@github.com:cloud-native-ai/spec-kit.git · `gitlab` git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git · `origin` git@github.com:github/spec-kit.git (upstream). All are SSH-only; none carries this branch. |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch is unpushed (the line's push policy is forbidden). Every citation below is an absolute path plus `git show <sha>:<path>` recovery. |
| Branch | `107-decision-governance` (checked out in the worktree below) |
| Commit SHA | `3f0200b421bf284c176592afa34549e7a2c07706` (short: `3f0200b42`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance` (git worktree of `/storage/project/cloud-native-ai/spec-kit`) |
| Review Date | 2026-11-26 |
| Reviewer (Agent) | SDD Review Executor (Qoder CLI agent, dispatched by the SDD driver; spec side) |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash 4.4.20(1); git 2.43.5; CPython 3.11.11 (`/usr/local/bin/python3`); pytest 8.4.2 |
| spec-kit Source Snapshot | this repository at `3f0200b42` (self-hosted; framework sources and client-runtime mirrors in one tree) |
| Line / run | line `decision-governance`; run `r20261125T134500Z-107a`; implement baseline commit `0d7519521` (includes the line-106 merge) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 427 | `…/worktrees/decision-governance/.specify/specs/107-decision-governance/requirements.md` | 30 FR / 10 SC / 9 STR / A-1…A-14 / P-01…P-12 / M-01…M-09 / B-01…B-07 |
| plan.md | 217 | `…/107-decision-governance/plan.md` | 23-principle Constitution Check, EP-001…EP-007, BC-01…BC-06, T-001…T-003 |
| tasks.md | 420 | `…/107-decision-governance/tasks.md` | 56 rows, 38 clause green claims, 6 user stories, all closed |
| data-model.md | 134 | `…/107-decision-governance/data-model.md` | 9 entities, 14 invariants, 1 state domain |
| quickstart.md | 81 | `…/107-decision-governance/quickstart.md` | 6 scenarios, executed-part split (A) executed / (B) planned |
| research.md | 73 | `…/107-decision-governance/research.md` | 16 measured baselines + 8 resolved design points |
| feature-ref.md | 73 | `…/107-decision-governance/feature-ref.md` | Feature 107 binding, delivery surfaces, BC rows |
| contracts/ (5 files) | 190 | `…/107-decision-governance/contracts/` | C-101…C-109, C-201…C-208, C-301…C-308, C-401…C-407, C-501…C-506 (38 clauses) |
| verification.md | 105 | `…/107-decision-governance/verification.md` | **Derived in this review** (was absent at review start): 10 SC rows, 6 RS joint-acceptance rows, smoke triple, ARC verdict |
| review.md (this file) | — | `…/107-decision-governance/review.md` | four segments + ARC |
| code-review.md | 1400 | `…/107-decision-governance/code-review.md` | code segment record with coverage receipt block |
| test-evidence/ | 130 files | `…/107-decision-governance/test-evidence/` | baselines, per-phase gates, mutation drill, migration closure, preservation sweep, review evidence |
| notes/ | 12 files | `…/107-decision-governance/notes/` | red-first evidence (26 slots), per-US green records, quickstart run |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements: spec + quality checklist scaffolded by hand | `942b0d5a5`; checkpoint 01 `d86eba994`; Clarifications: "因当前已在 `107-decision-governance` 分支且脚本的编号推导会把当前分支计入而派生 108 … 采用等价的手工脚手架" | Recorded deviation (script would derive 108; manual equivalent used, disclosed) |
| 2 | clarify: Related Feature bound as a new Feature 107 | `75ce843f6`; checkpoint 02 `08b59695c` | None |
| 3 | plan: plan set + 3 tensions registered as `T-019…T-021` | `fc8bbdf54`, `d05c3a350`; overlap gate `decision=overlap overlaps=117` adjudicated in-stage (pointer-only landing) | In-stage adjudication with residual (workspace "after" snapshot all-null; driver fell back to the before-snapshot) |
| 4 | tasks: 56 dependency-ordered rows; handoff decided (56 > 10) | `55a67bbac`, `a954f64a3` (anchor/team/handoff), `95f5a8ca9` (39 checklist items) | Roster validator needed a block-style members fix (driver correction) |
| 5 | analyze: five rounds to a passed gate | R1 5H (`346f54d60`) → R2 3H (`d33319fa7`) → full plan re-review (`7ceb653b1`, `78c7563ba`, `288a8a0c9`) → R3 2H (`576439fef`) → R4 1H (`ff69edd14`) → R5 0 C/H (`9655e484a`); gate PASS | Loop by design; the FR-025 claim alone took four repair rounds (F4) |
| 6 | implement: branch merged with master (line 106) at `0d7519521`, then P1–P5 serial packages | `7c1d882b0`, `75af9f5eb` (section-count pin bump), `e5d374c57` (56/56 + integration), `d25698eff` (close-out), `3f0200b42` (U4) | Merge declared by the line ruling; the implement U4 flipped the registry to `Implemented` **without** the closure checker or `verification.md` (F1/A1) |
| 7 | review (this run): verification.md derived, ARC run, four segments, code record, status flip | `test-evidence/review-evidence.txt`; `verification.md`; `code-review.md`; this file | P0 repaired in-run (F1/A1); P1/P2 disclosed below |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. Both repaired in this run (F1/A1 are two views of one fact). |
| P1 | 7 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 (F4, A4) |
| Command Prompt | 1 (F5) |
| Automation / Scripts | 2 (F2, F3) |
| Workflow | 5 (F1, F6, A1, A2, I1) |
| Documentation | 3 (A3, A5, I2) |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `fbab7a45c4a57b596bc32437181ee9eb799ebe60` | resolved diff base |
| Head commit | `3f0200b421bf284c176592afa34549e7a2c07706` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Renderer mode | `renderer: text` | record header (no TTY; non-interactive agent invocation) |
| Changed / judged / skipped / gap files | 684 / 27 / 657 / 0 | copied from the record's coverage receipt block |
| Segment verdict | `not-evaluated` | skips earn no coverage credit |
| Gate verdict | allow | `report --summary --file` exit 0; 0 `blocking` |
| Reason, when one applies | 657 files legally skipped — generated mirrors/copies, non-code records/spec artifacts, and the line-106 merge scope under `size-guard-focus-not-reviewed`; the feature's own code and test surfaces (27 files) were all judged | — |
| Uncommitted scope | "2 个未提交路径未计入本次评审对象（.specify/specs/107-decision-governance/test-evidence/review-evidence.txt, .specify/specs/107-decision-governance/verification.md）；本回执不对该范围给出任何结论。" (disclosed at receipt time; both files landed in the review commit) | same sentence in `code-review.md` |
| Record | `.specify/specs/107-decision-governance/code-review.md` | written (triage `run`) |
| Archive | `none` | first run for this feature |

The code record carries 0 `blocking`, 1 `important` (answered in the record), 1 `suggestion`, 1 `question`, 1 `praise`. The 27 judged files include the new engine read in full, the owner page read in full, every pointer/template/generator diff, and the five test modules; the 657 skips are named per file in the receipt block. Client capture is `skipped`: this repository wears the framework hat (`shared/definitions/dogfooding-definitions.md` § 2.1), so no client feedback entry is written.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/ (5), data-model.md, quickstart.md, research.md, feature-ref.md, test-evidence/, verification.md | stage rules + `plan.md` § Project Structure |
| Coverage line | 10 / 10 (9 / 10 at review start; `verification.md` was absent and was derived in-run) | present members / expected members |
| Missing members | none after the repair (at review start: `verification.md`) | — |
| Segment verdict | `pass` (after the A1 repair; re-judged on the repaired set) | — |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `.specify/specs/107-decision-governance/verification.md` | — | the file was absent on disk at review start, so no line exists to cite | A1: the expected-set member and the ARC input were missing while the registry already claimed `Implemented`; repaired in-run by deriving the carrier spec-side from `test-evidence/verification-input.md` (statuses/values copied; SC-001 note corrected per A3; six `RS-NNN_joint_acceptance` rows added) and copying the ARC verdict into it |
| P1 | `.specify/features/107-decision-governance.md` | 6 | — | A2: `**Status**: Planned` contradicted the registry row `Implemented` (one fact, two carriers); both carriers now read `Ready for Review` after the gate, and `## Latest Review` carries this run's entry |
| P1 | `.specify/specs/107-decision-governance/test-evidence/verification-input.md` | 18 | — | A3: the SC-001 note claims "the documented code-face scan … equals the owner page's declared producer set minus the two declared exemptions"; the measured scan maps only P-04/P-05/P-06/P-09 (plus 3 declared non-producer faces and the checker), and `observed=10` comes from the checker's declaration-side existence augmentation. The note is corrected in the derived `verification.md`; the semantic question stays open as I1 |
| P2 | `.specify/specs/107-decision-governance/requirements.md` | 348 | — | A4: SC-008's literal "blocking 计数不变" does not hold (31 → 30), while "zero NEW hits" does; `test-evidence/gate-neutrality.txt` adjudicates the one removed member as a line-106 merge change with an empty added set — a recorded re-baseline, not a 107 change |
| P2 | `shared/definitions/decision-definitions.md` | 271 | — | A5: M-01's red condition names conditional-family absence generically, but only the transmission family has a machine-detectable trigger; the supersession family has neither a detection rule nor a reverse sample (`m01/red-conditional-missing.md` drills the transmission family only) |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `fbab7a45c` | resolved diff base |
| Head commit | `3f0200b42` | run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py tests/contract/test_decision_governance_guards.py tests/contract/test_decision_governance_migration_map.py tests/unit/test_validate_decisions.py tests/integration/test_decision_governance_migrate_dryrun.py -q` | recorded verbatim; re-run by this review |
| Smoke exit code | 0 | 43 passed in 13.40s |
| Smoke evidence path | `.specify/specs/107-decision-governance/test-evidence/review-evidence.txt` | exists, non-empty; carries the clean run plus the disclosed self-collision incident |
| Scope and regression verdict | scope confined to the plan's declared landing surface plus the declared line-106 merge; regression re-measured — preservation sweep 5 failed / 241 passed, all five names inside `baseline-failed.txt`, zero new names; FR-025 three-path diff rc 0 with zero `--numstat` rows | — |
| Segment verdict | `pass` | — |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/validate-decisions.py` | 1064 | — | I1: the inventory action's `observed` set is not the documented scan (the scan maps 4 producers); declared rows are added to `observed` whenever their owner path exists, so `observed == declared ± exempt` is reached by declaration-side existence and a declared face that stops referencing the owner page while its file remains is still counted observed (code record `important`) |
| P2 | `scripts/bash/generate-instructions.sh` | 112 | — | I2: the budget-raise record states the new ambient section is "1,274 B"; the extracted section measures 1,276 B in template and live alike (no threshold is affected) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` (at check time) | registry row 107, read by the checker |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/107-decision-governance --json`, verdict `accept`, exit 0; never recomputed here |
| Comparison verdict | `agree` | — |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — `Planned → Implemented` was flipped without its gate product on disk

- **Severity**: P0
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance/.specify/features.md` (row 107) and the absent `verification.md`
- **Evidence** (verbatim quotes):

  ```
  The implement command template prescribes: "Closure verdict before the flip: run
  `python3 scripts/python/closure-acceptance-check.py --spec-dir <REQUIREMENTS_DIR>` from the
  repository root before landing the status." and "(2) copy its `verdict` and emitted reasons
  into `REQUIREMENTS_DIR/verification.md`, (3) only then write the registry row / detail
  status."
  ```

  ```
  State spine U4 — implement: "registry 107 → Implemented; checkpoint 08 committed."
  (no closure-checker invocation or record anywhere in the spine, the checkpoints, or
  test-evidence). `test -e .specify/specs/107-decision-governance/verification.md` → ABSENT
  at review start; the closure checker itself exits 2: "input error: required input not
  found: …/verification.md".
  ```

  ```
  Recurrence, one feature earlier (line 106's own review, quoted from
  .specify/features/095-superagent-role.md § Latest Review): "the P0: the slice's
  `Planned → Implemented` flip landed while `verification.md` was absent".
  ```

- **Why it's a problem**: The status carrier claimed `Implemented` with no gate product behind it — exactly the silent-corruption shape the implement template's ordering rule removes, and it is now a two-feature recurrence. The registry row is the surface downstream drivers and closure audits read; an unbacked claim there travels.
- **P0 validation status**: this assignment prohibits dispatching a validation subagent ("Do not dispatch another agent"), so the skill's subagent-unavailable fallback applies: **direct re-read by the reviewing agent** (registry row, absent file, absent checker record, and the checker's own exit-2 message). Marked `(validated: direct re-read, subagent unavailable)`.
- **Repaired in this run**: `verification.md` derived spec-side from the crew's recorded input block; the closure checker run on the tree and its verdict copied into the carrier (`accept`, `final_path` 7/7 pass); the `Implemented → Ready for Review` move lands only after the gate. The implement stage's structural cause (no stage-table artifact for `verification.md`; the spec-side derivation has no named executor) is REC-W1.

### F2 — Stage dispatch failed on a prompt path the runner resolves after `chdir`

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (line 334 at the failure time)
- **Evidence** (verbatim quote):

  ```
  watcher: `FAILED` (rc=1), startup in 7s; runner log: "stage-runner.sh: line 334:
  .specify/state/prompt-decision-governance-requirements.md: No such file or directory"
  root cause: the runner chdirs to `--project-dir` (the worktree) before reading
  `--prompt-file`; the relative prompt path resolved inside the worktree.
  ```

- **Why it's a problem**: A worktree project-dir plus the documented relative prompt path is a guaranteed first-dispatch failure; the workaround (absolute paths) is undocumented, so every line pays this toll once.
- **Proposed fix**: Resolve `--prompt-file` / `--state-dir` against the invocation directory before the `chdir`, or document the absolute-path requirement in the dispatch recipe.

### F3 — The line registry refuses the driver's own sanctioned worktree root

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `skills/external/sdd-loop-driver/scripts/line-registry.py`
- **Evidence** (verbatim quote):

  ```
  "`line-registry.py register --write-line --worktree-path <repo>/.specify/.tmp/sdd-loop/worktrees/<line>`
  exits 2 (`worktree_path must be outside repo_root`), while the driver's sanctioned worktree
  root is exactly that path. The line was registered without write-line fields and the
  worktree recorded only in the spine."
  ```

- **Why it's a problem**: The two owners disagree about the same path: the driver's worktree convention is rejected by the engine that is supposed to register it, so the registry cannot see worktree lines and the spine becomes the only record.
- **Proposed fix**: Exempt the sanctioned `.specify/.tmp/sdd-loop/worktrees/` prefix from the outside-repo rule (or move the sanctioned root and update the recipes in the same change).

### F4 — Containment claims were authored undecidable; the analyze loop paid for it five times

- **Severity**: P1
- **Category**: Template
- **Location**: `templates/requirements-template.md` / the FR-025 clause lineage in `…/107-decision-governance/requirements.md:241`
- **Evidence** (verbatim quotes):

  ```
  "chain: R1 5H → repair1; R2 3H → repair2; R3 2H → repair3; R4 1H → repair4
  (allowed-delta reading); R5 incremental 0 C/H."
  ```

  ```
  "R4-01: the FR-025/SC-008 containment claim's ruling authorization still has an undecidable
  element after the repair (two admissible ruling forms / unruled-change defect not in a
  closed enforcement row — see R4-02/03 as related)."
  ```

- **Why it's a problem**: The containment-claim discipline exists (`shared/guidelines/closed-set-claims.md`), but nothing at requirements-authoring time forces its five elements, so undecidability surfaced only in analyze round 3–4 — at the cost of a five-round gate plus a full mid-analyze plan re-review. Every spec that asserts "unchanged" pays the same toll.
- **Proposed fix**: Add a decidability lint (baseline reference, comparison unit, allowed-delta set, complement assertion, ruling location) to the requirements authoring/validation path so the five rounds shrink to one.

### F5 — Analyze workers hit the output-token ceiling three times in one package

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: analyze worker dispatch template (`skills/internal/analyze-artifacts/`, worker briefs in `.specify/state/prompt-decision-governance-analyze-*`)
- **Evidence** (verbatim quote):

  ```
  "a 9-file analyze domain without strict output discipline hit the model's 48k output-token
  ceiling three times (incomplete unit, no findings file). Mitigation applied: split domains to
  2–3 files and enforce 'findings file + counts only, no narration'."
  ```

- **Why it's a problem**: The dispatch template lacks an output-budget clause; a worker can silently produce nothing (an incomplete unit), which reads as a clean domain to a careless integrator.
- **Proposed fix**: Add the output-budget clause (bounded domain size + "findings file + counts only") to the analyze worker dispatch template.

### F6 — Pre-merge measured premises went stale inside the same run

- **Severity**: P2
- **Category**: Workflow
- **Location**: `…/107-decision-governance/test-evidence/implement-integration.md` § Residuals
- **Evidence** (verbatim quotes):

  ```
  "T053's literal expectation — `git diff d05c3a350..HEAD -- .specify/glossary.md` empty —
  does not hold on the merged tree: 106's own `silent-end` proposed row arrived with the merge."
  ```

  ```
  "The added `## Decision Items（决策项）` section required the section-count pin in
  `tests/contract/test_fast_fail_discipline.py` to move 38/39 → 39/40; repaired in `75af9f5eb`
  with the dated stale-pin note."
  ```

- **Why it's a problem**: Two accepted premises changed meaning when the line merged master; both were caught and disclosed, but only after the task that depended on them ran. Specs written on long-lived branches will keep paying this.
- **Proposed fix**: When a line merges trunk, re-base every literal diff-range premise in its evidence set and record the re-base as part of the merge step.

## 4. What Worked — Preserve (Brief)

- The closed producer inventory + pointer-only adjacent edits kept one owner page without a second definition point.
- Reverse-sample discipline: 9/9 machine rules go red with rule-carrying verdict lines, run through the single test entry.
- The recorded gate re-baseline (31 → 30) with a membership diff against a read-only extraction of the baseline tree is an auditable way to absorb merge drift.
- Per-package verifier verdicts made the 56-task closure program-checkable (contiguous ranges, zero missing/duplicate rows).
- The strict no-write snapshot inside `test_cli_surface` proved its worth immediately — it caught a concurrent write during this review (disclosed in `review-evidence.txt`).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-T1 Decidability lint for containment claims** — Target: `templates/requirements-template.md` (absolute: `<repo>/templates/requirements-template.md`). Change: make the five containment elements a required authoring shape and validate them in the requirements validators. Source: F4. Expected impact: the five-round analyze loop becomes one; undecidability is caught where the sentence is written.

### 5.2 Command Prompt Improvements

- **REC-C1 Analyze worker output-budget clause** — Target: `skills/internal/analyze-artifacts/` worker dispatch (absolute: `<repo>/skills/internal/analyze-artifacts/`). Change: cap domain size and mandate "findings file + counts only, no narration". Source: F5. Expected impact: no silent incomplete units; the integrator cannot mistake emptiness for a clean domain.

### 5.3 Automation / Script Improvements

- **REC-A1 Resolve dispatch paths before `chdir`** — Target: `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (absolute: `<repo>/skills/external/sdd-loop-driver/scripts/stage-runner.sh`). Change: resolve `--prompt-file`/`--state-dir` against the invocation directory before switching to `--project-dir`, or document the absolute-path requirement. Source: F2. Expected impact: first dispatch succeeds from a worktree.
- **REC-A2 Exempt the sanctioned worktree root in the registry** — Target: `skills/external/sdd-loop-driver/scripts/line-registry.py` (absolute: `<repo>/skills/external/sdd-loop-driver/scripts/line-registry.py`). Change: accept `<repo>/.specify/.tmp/sdd-loop/worktrees/<line>` as a worktree path. Source: F3. Expected impact: the registry and the driver agree on one convention.

### 5.4 Workflow Improvements

- **REC-W1 Make `verification.md` derivation a named stage step with an executor** — Target: `shared/declarations/facts/driver-stage-artifacts.yaml` + `templates/commands/implement.md` (absolute: `<repo>/shared/declarations/facts/driver-stage-artifacts.yaml`, `<repo>/templates/commands/implement.md`). Change: list `verification.md` as an implement-stage artifact and name who derives it (the spec side) and when (before the status flip); optionally make the closure checker's input error block the flip mechanically. Source: F1/A1. Expected impact: the third occurrence of the same P0 (106, 107, and the next handoff line) stops.
- **REC-W2 Re-base premises on merge** — Target: `skills/external/sdd-loop-driver/references/dispatch-recipes.md` (absolute: `<repo>/skills/external/sdd-loop-driver/references/dispatch-recipes.md`). Change: a merge step re-bases literal diff-range premises and pins updated counts in the same commit. Source: F6. Expected impact: no stale premise survives a merge.

### 5.5 Documentation Improvements

- **REC-D1 Make acceptance notes state the measurement actually made** — Target: `templates/verification-log-template.md` (absolute: `<repo>/templates/verification-log-template.md`) and the SC-001/SC-008 criteria lineage. Change: require an acceptance note to name the observed set and the measurement source verbatim; align the inventory observation definition (strict scan vs augmented) across owner page, checker docstring and SC-001. Source: A3/I1. Expected impact: a `pass` note cannot overstate its own scan.
- **REC-D2 Correct the generator's recorded section size** — Target: `scripts/bash/generate-instructions.sh` (absolute: `<repo>/scripts/bash/generate-instructions.sh` line 112). Change: "1,274 B" → the measured 1,276 B. Source: I2. Expected impact: the raise record is exact.
- **REC-D3 Scope the M-01 supersession leg** — Target: `shared/definitions/decision-definitions.md` (absolute: `<repo>/shared/definitions/decision-definitions.md` line 271). Change: either name a machine-detectable supersession trigger or scope the M-01 red condition to the transmission family and route supersession detection to review. Source: A5. Expected impact: the table's claim matches the guard and the drill.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Make verification.md derivation + the closure checker a named stage step | driver-stage-artifacts.yaml + templates/commands/implement.md | F1, A1 |
| P1 | Decidability lint for containment claims | templates/requirements-template.md + validators | F4 |
| P1 | Analyze worker output-budget clause | skills/internal/analyze-artifacts/ | F5 |
| P1 | Resolve dispatch paths before chdir | stage-runner.sh | F2 |
| P1 | Exempt the sanctioned worktree root | line-registry.py | F3 |
| P1 | Inventory observation definition aligned (strict vs augmented) | owner page + checker + SC-001 | A3, I1 |
| P1 | Status carriers: one fact, both carriers | features.md + features/107 detail | A2 |
| P2 | Re-base premises on merge | dispatch-recipes.md | F6 |
| P2 | SC-008 count literal vs recorded re-baseline | requirements.md criterion lineage | A4 |
| P2 | M-01 supersession leg scoped or detected | decision-definitions.md | A5 |
| P2 | Generator section-size figure corrected | generate-instructions.sh | I2 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path as a parenthetical supplement.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file. (A/I findings quote their evidence in the §2 tables and are cross-referenced here.)
- [x] No bullet says "see attached" or references context outside this document; unreachable-commit citations name absolute paths and `git show` recovery.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file and at least one source finding ID.
- [x] P0 validation status is stated explicitly: two P0 findings (F1 + A1, two views of one fact), both **repaired in this run**, validated by direct evidence re-read because this assignment prohibits dispatching validation subagents (`(validated: direct re-read, subagent unavailable)`).

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
