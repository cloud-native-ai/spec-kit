# Specification-Driven Development (SDD) Process Review Report: 095-superagent-role

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

Rendered by `/speckit.review`, run `r20261110T055657Z-b095-review` (four segments in the fixed order process → artifact → implementation → code, plus the Acceptance Reality Check; no order changed and no segment skipped).

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 095 |
| Requirement Key | 095-superagent-role |
| Requirement Name | Super Agent Role（相对逻辑角色：定义、协议与 harness 落点） |
| Related Feature | 095 Super Agent Role（相对逻辑角色：定义、协议与 harness 落点） |
| Repository | spec-kit |
| Repository URL | remotes: `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`; `origin` is the upstream `git@github.com:github/spec-kit.git` and does not hold these commits |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (unpushed) — citations below use absolute paths plus `git show <sha>:<path>` recovery instructions instead of URLs |
| Branch | `095-superagent-role` |
| Commit SHA | `6c48e9c253166a71ab8364dd818c7d4409471fb5` (short: `6c48e9c25`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-10 |
| Reviewer (Agent) | Qoder CLI, `/speckit.review` four-segment run (reviewer display name: Qiming Liu (John)) |
| Environment | Linux x64, bash, CPython 3.11.11 (`pyproject.toml` requires `>=3.8`), 192 CPUs, pytest runner `scripts/bash/run-tests.sh` (parallel default) |
| spec-kit Source Snapshot | self-hosting framework repo @ `6c48e9c25` (framework sources + the same repo's `.specify/` runtime) |
| Review object (code segment) | `base..head` = `b3da3a26dfba209057f65c2b17962b9516812c39..6c48e9c253166a71ab8364dd818c7d4409471fb5`, base source `feature-first-commit` (the parent of the first 095 commit) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 287 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/requirements.md` | 38 FR / 10 SC / 6 shared strings; five user stories |
| plan.md | 247 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/plan.md` | D-1…D-14, T-001/T-002, 22-row Constitution Check, P1–P6 packages |
| tasks.md | 341 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/tasks.md` | 54 rows, 8 phases, DoD + GATE-1…GATE-6 |
| data-model.md | 115 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/data-model.md` | role/edge/executor/violation model, nine-item slugs, carrier row shapes |
| contracts/role-edge-engine.contract.md | 82 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/role-edge-engine.contract.md` | engine C-1…C-11 |
| contracts/role-transition-payload.contract.md | 67 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/role-transition-payload.contract.md` | payload/protocol C-1…C-13 |
| contracts/status-digest-role-view.contract.md | 47 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md` | digest role view C-1…C-8 |
| contracts/harness-landing.contract.md | 59 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/harness-landing.contract.md` | pointer section + zero-second-mechanism C-1…C-6 |
| quickstart.md | 57 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/quickstart.md` | four scenarios with per-example premises |
| verification.md | 118 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/verification.md` | SC status table + machine block + smoke record |
| feature-ref.md | 21 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/feature-ref.md` | Feature 095 binding + six-row mapping |
| observation-appendix.md | 30 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/observation-appendix.md` | 14 slice rows (6 exercised / 8 not-observed) |
| checklists/requirements.md | 55 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/checklists/requirements.md` | specification-quality checklist |
| checklists/requirements-quality-2026-11-10.md | 83 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md` | 39-item requirements-quality checklist |
| test-evidence/ | 59 files | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/test-evidence/` | gate/closure/smoke/mutation readings |
| code-review.md | 1377 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/code-review.md` | code segment record + coverage receipt |
| review.md | this file | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/review.md` | this report |
| Bound feature detail | 71 | `/storage/project/cloud-native-ai/spec-kit/.specify/features/095-superagent-role.md` | overview, planned changes, status criteria |

## 1. Process Execution Timeline

Reconstructed from `git log b3da3a26d..HEAD` (51 commits) and the append-only stage records in `/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md`.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements stage completed | `e2f760159`, `6a82f253c`, `9b3dbbc0d`, `c3507e4e6`; validator `status: ok` | none |
| 2 | clarify stage completed (10 self-rulings) | `4c515c08a`, `99586eb65`, `5aea9e5d4`, `71344d551`, `0b6a040b6`; overlap `decision=clear` | none |
| 3 | plan stage + one repair round | `448c1f3a3`, `99f0589d7`, `f6aea4f5a`, `2c8da54c0`; gate `decision=pass` | first plan gate red on a Source-cell format rule (F9) |
| 4 | tasks stage + one gate repair | `82f046aa1`, `1752a1acd`, `438fe6c97`, `035a572c0`, `4369dc7fe`; `validate-tasks` 0 error | count-claim regex false red (F10) |
| 5 | checklist stage | `841bef68d`, `293e0e063`; 39 items | none |
| 6 | analyze round 1 | `1793add54`, `8ef0a173f`, `c5609242d`; 2 CRITICAL + 12 HIGH | expected analyze findings |
| 7 | analyze repair + round 2 | `1e59f10e2`, `02b654b5c`, `b31f87ba5`, `d5a372d45`; round-2 gate FAIL 0C/4H → U5 stop-line | stop-line reached; resolved only after an out-of-band interview ruling (`6d13938aa`) that lets unattended runs self-repair analyze findings |
| 8 | analyze rounds 3–4 released | `1959550ab`, `d5b262fc0`, `3cee1381d`, `2da3a4ba2`, `75f2297db`, `c671e168a`; 0 CRITICAL / 0 HIGH open | none |
| 9 | implement P1–P6 | `b7e2a5bc8` (P1), `68f8968bd` (P2), `c7913da22` (P3), `aa548057f` + `23f1cd1fc` (P4), `d8843810f` (P5), `6c48e9c25` (P6) | T001 baseline never captured; reconstructed at `c671e168a` (F2); T003 deferred (F5); no status flip (F1) |
| 10 | Other-line commits interleaved on this branch | `dddd09773`, `c2f199955`, `48d78d1a5`, `9c39b8e06` (digest redesign), `6d13938aa` (gates self-repair), `57d364074` (state-is-runtime), `343ad1e1e` (coaching record) | 7 commits with no 095 task row (F3) |
| 11 | User-ruled constitution amendment inside the run | `dd7cbbab4` (1.19.0 → 1.19.1, Principle VII carrier `verification.log` → `verification.md`); guard pin raised but unverifiable (F-C6 in `code-review.md`) | user-ruling change, out of the 095 task rows |
| 12 | review stage (this run) | start `2026-11-10T14:55:56Z` (`pid-095-superagent-role-review`); code record `.specify/specs/095-superagent-role/code-review.md`; receipt 313/13/300/0, gate deny | none (four segments + ARC executed) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 8 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 6 |
| Workflow | 4 |
| Documentation | 1 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `6c48e9c253166a71ab8364dd818c7d4409471fb5` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 313 / 13 / 300 / 0 | copied field by field from the record's coverage receipt block (never recomputed) |
| Segment verdict | `blocked` | the record carries 2 `blocking` entries |
| Gate verdict | `blocking-unresolved` | `report --summary --file .specify/specs/095-superagent-role/code-review.md` exits 1, `blocking_entries=2`, `gate=deny` |
| Reason, when one applies | none (segment verdict is `blocked`, not `not-applicable` / `not-evaluated`) | — |
| Uncommitted scope | 44 uncommitted paths disclosed and not reviewed; the same sentence lives in `code-review.md` § 未提交范围 | `uncommitted_scope=44` |
| Record | `.specify/specs/095-superagent-role/code-review.md` | written because triage is `run` |
| Archive | `none` | first run |
| Client capture | `skipped hat=framework basis=root owns framework source directories (templates/skills/shared/scripts/src/specify_cli); owner=.specify/shared/definitions/dogfooding-definitions.md § 2.1; triage=run` | the fifth non-interactive step's disclosure line |

This subsection carries the verdict and the pointers only: no opinion body and no per-severity item count. The findings live in `code-review.md` and are read there. The two `blocking` entries are: (1) 18 existing guard tests red at HEAD caused by in-range digest-redesign commits, with `last_completion` removed from the only reachable renderer; (2) the C-68 explicit "no measurements" state dropped and its guarding assertion weakened in the same range.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/` (4 files), `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `observation-appendix.md`, `checklists/` (2 files), `test-evidence/` (59 files) | union of the standard spec-stage set and `plan.md` § Project Structure (lines 109–120) |
| Coverage line | 11 / 11 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | the three P1 rows below |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md` | 7 | none | C-1 says the materialization is the digest's "single state-read pass — the legacy line entries and the role view both derive from it, and **no carrier root may be read twice**"; the implementation reads the line registry twice (legacy `read_registry()` + the engine's `_parse_registry`) and the legacy entries do not derive from the materialization. The guarding test (`test_status_digest_roles.py:205`) counts AST call sites only, so the clause has no carrier that can go red. |
| P1 | `.specify/features/095-superagent-role.md` | 1 | none (heading is line 1; the missing field block would sit at lines 3–8) | The bound feature detail carries no `**Status**:` field and no `## Latest Review` section although `templates/feature-details-template.md` requires both; the closure checker exited 2 on the missing field and the run worked around it by dropping the optional `--feature-detail/--feature-registry` arguments (`/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md:292`). |
| P1 | `.specify/specs/095-superagent-role/verification.md` | 42 | none | The close-out states "Feature 095 stays **`Planned`** … this close-out performs no status flip", while `tasks.md:241` (T054) says the feature-integration table has "`/speckit.tasks` maintains `Planned`; **implement advances**" — two artifacts state the implement-stage status obligation differently, and the tree follows neither of the implement command's rules. |
| P2 | `.specify/specs/095-superagent-role/verification.md` | 18 | none | SC-007 reports 38,301 B / 38,400 B (99 B headroom) while `requirements.md:285` (A13) and `plan.md:175` (EP-005) measured 37,454 B / 946 B; the intervening +514 B instruction insert from another line (`.specify/instructions.md` diff hunk of `57d364074`) is not named, so the two readings cannot be reconciled from the artifacts. |
| P2 | `.specify/specs/095-superagent-role/plan.md` | 29 | none | D-1 declares "`better-harness.md` is **not** modified"; the delta modifies it in `dd7cbbab4` (user-ruling constitution amendment, two sensor references `verification.log` → `verification.md`). The plan carries no pointer to the later ruling, so a plan reader is misled about the branch's actual change set. |

One row per finding. `line` is required whenever the artifact is line-addressable; every member above is markdown and line-addressable.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `6c48e9c253166a71ab8364dd818c7d4409471fb5` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code skill's `git-delta-review.sh` reported |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_role_edge_engine.py tests/contract/test_role_transition_payload.py tests/contract/test_status_digest_roles.py tests/contract/test_superagent_definitions.py tests/contract/test_instructions_budget_superagent_section.py tests/contract/test_superagent_zero_mechanism.py -q` | recorded verbatim from `verification.md` |
| Smoke exit code | 0 | the integer the command returned; re-run at review time: 85 passed, exit 0 |
| Smoke evidence path | `.specify/specs/095-superagent-role/test-evidence/smoke-six-modules.txt` | exists and non-empty |
| Scope and regression verdict | scope fails (7 non-095 commits + 1 user-ruling amendment inside the delta); regression fails (18 in-range guards red, attributable to the other-line digest-redesign commits); the 095 packages themselves re-measure green (smoke 85 passed at review; closure checker `accept`, `final_path.pass=7`) | the segment's own reading |
| Segment verdict | `blocked` | the three P1 rows below |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/status-digest.py` | 1054 | none | The delta carries 7 commits with no 095 requirement or task row — `dddd09773`, `c2f199955`, `48d78d1a5`, `9c39b8e06` (digest redesign), `6d13938aa` (gates self-repair), `57d364074` (state-is-runtime), `343ad1e1e` (coaching record) — plus the user-ruling `dd7cbbab4`; no task row asks for the digest column redesign, the gate policy, or the state reclassification. |
| P1 | `.specify/features.md` | 102 | absence: the expected edit never landed | The implement stage's owned transition `Planned → Implemented` was not written although the closure checker returned `accept` and all four conditions hold; the registry row still reads `Planned` (F1). The review's `Implemented → Ready for Review` transition therefore has no legal source state. |
| P1 | `scripts/python/status-digest.py` | 1174 | none | Regression: 18 existing guards in `tests/unit/test_status_digest_unit.py` (10) and `tests/contract/test_efficiency_element.py` (8) are red at HEAD, caused by the in-range redesign commits (measured: `18 failed, 23 passed`); the same range did not update those guards. The reconstructed baseline sits after those commits and absorbs them (F2), so the feature's zero-NEW gate cannot see them. |
| P2 | `.specify/features.md` | 102 | none | The registry's `Last Updated` cell reads `2026-11-10` with no `(deferred: T003)` suffix, although `templates/feature-details-template.md` § Canonical Status State Machine requires the suffix when a task is `[~]` deferred. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Planned` | the bound feature detail's registry claim (`.specify/features.md` row 095), copied |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7 | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/095-superagent-role --json`, never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept`; the `Planned` claim is behind the evidence and contradicts no count; no ARC refusal condition fires |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition judgement — refused (`blocking-unresolved`).** The transition `Implemented → Ready for Review` is refused; the status is left at `Planned`. The failed conditions are named: (1) **condition (c)** — the current code-segment record carries two `blocking` entries (`code-review.md`); (2) **condition (a)** — `deferred_tasks=T003` is neither resolved nor named by an explicit user waiver; (3) **source state** — the claimed status is `Planned`, because `/speckit.implement` never landed its owned `Planned → Implemented` transition after the checker returned `accept` (F1), and no `Planned → Ready for Review` row exists in the state machine. No user ruling exists in this run, so the unattended disposition is halt-and-report.

## 3. Findings (Problems & Improvement Targets)

### F1 — Implement never lands its owned status transition, so the review gate has no source state

- **Severity**: P0
- **Category**: Workflow
- **Location**: `.specify/specs/095-superagent-role/verification.md:42`; `.specify/features.md:102` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/verification.md:42`)
- **Evidence** (verbatim quote):

  ```
  Feature 095 stays **`Planned`** in `.specify/features.md` — the tasks stage maintains
  `Planned` and this close-out performs no status flip; the task breakdown exposed no
  new or invalidated Feature, and no `.specify/features.md` edit was made by this package
  ```

  and the registry row's status cell: `| 095 | Super Agent Role（…） | … | Planned | … | 2026-11-10 |`
- **Why it's a problem**: `templates/feature-details-template.md` § Canonical Status State Machine makes `Planned → Implemented` the implement command's transition, requires all four conjunctive conditions, and states the "Critical contract: `/speckit.implement` MUST advance `Planned → Implemented` only when all four conditions above hold". The closure checker returns `accept`, `final_path.pass=7`, all four conditions true — the flip was owed and not delivered. The close-out's rationale ("the tasks stage maintains Planned") is a stage self-assessment, exactly what `templates/commands/implement.md:59` forbids. Downstream, `/speckit.review` judges exactly `Implemented → Ready for Review` and the state machine has no `Planned → Ready for Review` row, so the feature cannot progress without a re-run of implement's Feature Integration step. Independently confirmed by a fresh-context read-only validator (`confirm`, P0).
- **Proposed fix**: make the driver's implement stage prompt carry the command-level Feature Integration step and make the implement stage sentinel require the registry row / detail status to be written after the checker's `accept`; add a driver-side post-implement check that refuses the sentinel while the registry still reads `Planned` with an `accept` verdict (`templates/commands/implement.md` § Feature Integration + `skills/external/sdd-loop-driver/references/stage-prompts.md` implement block).

### F2 — Reconstructed baseline absorbs in-range breakage, so "zero NEW failures" is scoped to the feature's own packages only

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/095-superagent-role/notes/baseline-provenance.md:7` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/notes/baseline-provenance.md:7`)
- **Evidence** (verbatim quote):

  ```
  Throwaway worktree at the P1 parent commit — the tree as it stood immediately before
  the first implement commit:
  `git worktree add --detach .specify/.tmp/095-base-wt c671e168a`
  ```

  and, from the review's own measurement: `18 failed, 23 passed` for `tests/unit/test_status_digest_unit.py tests/contract/test_efficiency_element.py`, with all 18 names present in `notes/baseline-failed-names.txt`.
- **Why it's a problem**: the reconstruction tree `c671e168a` is *after* the branch's own digest-redesign commits (`dddd09773`, `c2f199955`, `48d78d1a5` are ancestors of it), so 18 guards those commits broke are classified "inherited" and the completion gate (`comm -13`) cannot see them. The verification's "zero NEW failures attributable to this feature" is literally true for the 095 packages but reads as branch health; the provenance note's "known limit" names only untracked scratch, not the in-range guard breakage.
- **Proposed fix**: the reconstructed-baseline path must record the tree's guard health per module and must refuse to classify as "inherited" any failure introduced by a commit inside the review range; carry the range's commit attribution into the provenance note and into `verification.md`'s SC-009 reading (`templates/commands/implement.md` § Baseline pre-flight + `templates/verification-log-template.md`).

### F3 — The feature branch carries seven other-line commits, so the slice delta is not feature-scoped

- **Severity**: P1
- **Category**: Workflow
- **Location**: git range `b3da3a26d..6c48e9c25`, commits `dddd09773`, `c2f199955`, `48d78d1a5`, `9c39b8e06`, `6d13938aa`, `57d364074`, `343ad1e1e`
- **Evidence** (verbatim quote from `git log`):

  ```
  c2f199955 feat(status): executor-primary digest — closed lines hidden, one row per live agent execution
  57d364074 chore(harness): .specify/state is runtime — ignored, untracked, and the ignore set is framework-maintained
  6d13938aa feat(gates): analyze gate self-repairs in unattended SDD runs — interview rulings for the blocked and stalled lines
  ```
- **Why it's a problem**: the code segment's judgment object is the committed `base..head` delta; seven commits with no 095 task row (plus the user-ruling amendment `dd7cbbab4`) make the delta span four unrelated subjects, destroy per-feature bisectability, and hand the review a scope judgement it can only resolve by attribution instead of by requirement trace. The 18 red guards (F2, code segment blocking) are a direct consequence.
- **Proposed fix**: add a line-scoped commit guard to the git workflow — while a feature branch is active, a commit whose subject carries no line id is refused or explicitly recorded as a cross-line commit, and the review's scope dimension reads that record (`skills/git-utils` scope A + `.specify/workflow/` git model template).

### F4 — The machine-readable loop-state block stays at "stalled / analyze round 2" through implement completion

- **Severity**: P1
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md:3` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md:3`)
- **Evidence** (verbatim quote):

  ```
  spine_state: stalled
  stage: analyze (round 2)
  last_verdict: analyze round-2 gate FAIL (0C/4H; repair-round bound reached) — U5 stop-line; handoff written
  ```
- **Why it's a problem**: the append-only stage records below the block show rounds 3–4 released and implement P1–P6 completed, but the block any engine or reader parses first still reports a stalled analyze line. The state machine's own machine surface contradicts its human record; an automated reader (driver, digest, recovery) would treat the line as stopped at analyze round 2.
- **Proposed fix**: every stage-record write must advance the `<!-- loop-state:begin -->` block (state, stage, attempt, last_verdict) in the same operation, and a stage record appended without the block advance should be refused (`skills/external/sdd-loop-driver/scripts/loop-state.py` + `references/stage-prompts.md` U4).

### F5 — The frozen-baseline re-freeze was deferrable into the review gate

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/095-superagent-role/verification.md:38`; `tasks.md:90` (T003)
- **Evidence** (verbatim quote):

  ```
  deferred_tasks=T003 — the implement-start clause-coverage re-freeze was not executed;
  the tasks-frozen baseline (642 lines, `base-sha 2c8da54c0`) remains the artifact cited
  by the analyze reports, and overwriting it at close-out would break those citations;
  lift it by re-freezing at the next implement pre-flight.
  ```
- **Why it's a problem**: the `Implemented → Ready for Review` gate requires every `[~]` task to be resolved or explicitly waived; T003 is neither, so this design-avoidable deferral alone refuses the transition. The task's own premise ("the implement pre-flight re-captures it (never cached)") conflicts with the reason for deferring it — there was no legal disposition that satisfied both without a second carrier for the analyze citations.
- **Proposed fix**: when a frozen baseline must survive re-capture, copy it to a dated archive path first and re-freeze in place; or make the deferral's resolution path (a named waiver) explicit in `create-tasks`/`implement` templates so the review gate is not blocked by a bookkeeping choice (`templates/commands/tasks.md` + `templates/commands/implement.md` § baseline).

### F6 — The code-review script's step census contradicts its own skill body

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/skills/internal/code-review/scripts/git-delta-review.sh:88` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/code-review/scripts/git-delta-review.sh:88`)
- **Evidence** (verbatim quote):

  ```
  NON-INTERACTIVE PATH (four steps, in this order — four, never three):
  ```

  versus `SKILL.md:70`: `### 非交互路径（Agent / CI：五步，不是四步）`
- **Why it's a problem**: the skill body and the command template require five steps (capture is the fifth), while the script — the only executable entry — prints "four steps" twice (header and `--help`). A caller following the script's help omits the capture step the skill says is mandatory; a caller following the skill expects a path the script does not advertise.
- **Proposed fix**: update the script's header comment and usage text to the five-step census, naming `capture` as step 5 (`skills/internal/code-review/scripts/git-delta-review.sh`; mirror the same file).

### F7 — A re-dispatched stage can be instantly "DONE" from the previous attempt's status file

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-05 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md`)
- **Evidence** (verbatim quote):

  ```
  FO-095-05（假完成，U3 面）：同一阶段**重派发**时，上一轮的 `status-<line>-<stage>` 文件留在原路径；
  `watch-target.sh` 读到旧 status（`exit=0 sentinel=1`）立刻判 `DONE`，而新子进程仍 `pid=alive`
  ```
- **Why it's a problem**: retries and repair rounds are routine in long SDD runs; a stale status record can declare a live attempt finished, and only an independent U4 validation caught it in this run (the old file was archived manually). The false-completion window is silent.
- **Proposed fix**: on re-dispatch, `stage-runner.sh` archives or renames the previous attempt's `status-<line>-<stage>` before the new pid file lands, and `watch-target.sh` requires the status mtime to be newer than the pid file before judging DONE (`skills/external/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh`).

### F8 — `watch-target.sh --window` does not return RUNNING at window expiry while the pid is alive

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-02
- **Evidence** (verbatim quote):

  ```
  FO-095-02（监听窗口）：`watch-target.sh --window 120/180` 在 pid 存活时不会按窗口到期返回 RUNNING
  （实测 200s/340s 工具超时仍未返回），与 `stage-prompts.md` § U3「窗口到期只返回 RUNNING 并立即重入」的叙述不一致
  ```
- **Why it's a problem**: the driver's bounded-wait protocol is documented but not delivered; hosts must background the command, which degrades the wait into a notification race and can lose the re-entry point.
- **Proposed fix**: implement window-expiry RUNNING in `watch-target.sh` as `stage-prompts.md` U3 describes, or correct the documentation to the measured behaviour (`skills/external/sdd-loop-driver/scripts/watch-target.sh` + `references/stage-prompts.md` § U3).

### F9 — The plan gate rejects a Source locator followed by a note, while the plan template never says the cell must be bare

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-06
- **Evidence** (verbatim quote):

  ```
  FO-095-06（门禁与模板表述）：`pre-analyze-check --stage plan` 要求「Source row」单元格为裸
  `<feature>:<row>` 定位符，但计划模板/作者指引未提示「注记不得与定位符同格」，首轮 plan 因此 exit 2
  ```
- **Why it's a problem**: a format rule enforced by the gate but stated nowhere the author reads costs a repair round per plan; the failure is mechanical, not semantic.
- **Proposed fix**: either accept a locator followed by a separator and note (parse the first token), or state the bare-cell rule in the plan template's table header (`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` + `templates/plan-template.md`).

### F10 — The count-claim gate reads a per-package bound as a total-count claim

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-07
- **Evidence** (verbatim quote):

  ```
  FO-095-07（计数断言门 vs 分包上界表述）：`pre-analyze-check --stage tasks` 的 count-claim 模式
  `(\d+)\s*tasks?` 会把 plan 中「≤16 tasks per package」（每包上界）读成**总量声明**并对照 tasks.md
  实际条数判红（本轮 plan.md:217 vs 54）
  ```
- **Why it's a problem**: the template itself invites the phrasing the gate rejects; the author must discover the trap by a red gate and write around it, and a future author will repeat it.
- **Proposed fix**: exempt phrases that declare a per-unit bound (`per package` / `每包`) in the count-claim matcher, or ban the phrasing in the plan/tasks templates and standardize on "work items" (`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` + `templates/tasks-template.md`).

### F11 — The stage runner's pid line carries no `run=` field, so run-scoped attribution is unavailable

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-01
- **Evidence** (verbatim quote):

  ```
  FO-095-01（064 归属面）：`stage-runner.sh` 写入的 `pid-<line>-<stage>` 行只有
  `pid= start= at= line= stage= event=`，**缺 `run=` 字段**；`watch-target.sh` 的 `classify_pair`
  要求 line 与 run 同时匹配才判 `own`
  ```
- **Why it's a problem**: every watcher invocation with `--run-id` degrades to `unattributed` / `pid=missing`, i.e. the multi-line attribution feature (064) is unusable exactly in the multi-line case it was built for; this review's own stage pid file reproduces the same shape (`pid=1062402 start=2325881771 at=1794322556 line=095-superagent-role stage=review event=pid`).
- **Proposed fix**: `stage-runner.sh` writes `run=<run-id>` into the pid line (accepting an optional `--run-id`), or `watch-target.sh` falls back to the registry's recorded pids as the identity source before the pid-file gate (`skills/external/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh`).

### F12 — The feature detail lacks the template's Status field and Latest Review carrier, forcing a checker workaround

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/features/095-superagent-role.md:1` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/features/095-superagent-role.md:1`)
- **Evidence** (verbatim quote):

  ```
  # 095 — Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）

  ## Overview
  ```

  and the run's workaround record: `closure-acceptance 首次调用因 feature detail 缺 **Status**: 行 exit 2 → 去掉可选 --feature-detail/--feature-registry 参数后引擎从注册表读取 claimed_status`
- **Why it's a problem**: `templates/feature-details-template.md` requires the `**Status**:` header field and a `## Latest Review` section; the created detail has neither. The closure checker's explicit-input path therefore fails, and the review's mandated carrier for both segment conclusions has to be created by this run; the registry becomes the only status source, which hides drift between the two carriers.
- **Proposed fix**: the feature-creation flow (`/speckit.feature` / `create-feature`) must instantiate the full header field block and the `## Latest Review` section, and the closure checker's explicit-input error should name the missing field with the path it read (`templates/feature-details-template.md` + the feature-creation skill; `scripts/python/closure-acceptance-check.py`).

## 4. What Worked — Preserve (Brief)

- The four-contract design (`role-edge-engine`, `role-transition-payload`, `status-digest-role-view`, `harness-landing`) with per-clause ids and guarding test modules — every 095 behaviour has a named contract clause and a red-first record.
- The read-only engine's executable contract: zero write points, `--help`/`--version`, undeclared-option exit 2, explicit empty-set summary, four violation fixtures each exit 1, conflict and malformed drills per C-2…C-9.
- The evidence discipline of the observation appendix: one row per existing slice, `exercised` only with a resolvable machine record, `not-observed` with a reason (14 slices, 6/8 split).
- The analyze self-repair loop: the four-round convergence (2C/12H → 0C/0H) with per-round merged reports and dispositions is a reusable shape for unattended runs.
- The mirror-parity pin and the honest budget leg: section-count pins raised in the section's own commit, generator budget report captured in full, and the a7 stale-pin repair documented in place.
- The digest role view's both-channel output (table + JSON) with the marker passed through from the model and a table/JSON identity test.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-095-09 — Instantiate the full feature-detail carriers and name the missing field** — Target: `templates/feature-details-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/feature-details-template.md`) and the feature-creation flow. Change: make the creation flow emit the header field block (`**Status**` included) and `## Latest Review`; make `closure-acceptance-check.py`'s explicit-input error name the missing field and the path it read. Source: F12. Expected impact: no checker workaround and no missing carrier for the review conclusions.

### 5.2 Command Prompt Improvements

- **REC-095-01 — Make the implement Feature Integration step survive driver dispatch** — Target: `templates/commands/implement.md` § Feature Integration (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`) + `skills/external/sdd-loop-driver/references/stage-prompts.md` implement block. Change: the driver's implement prompt names the command-level status flip, and the stage sentinel requires the registry/detail status to be written after the checker's `accept`. Source: F1. Expected impact: `/speckit.review`'s transition always has a legal source state.
- **REC-095-05 — Give a frozen baseline a legal secondary carrier instead of a gate-blocking deferral** — Target: `templates/commands/tasks.md` + `templates/commands/implement.md` § baseline (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/commands/`). Change: document the dated-archive-then-refreeze disposition for a baseline that must survive re-capture, so the task is not deferred into the review gate. Source: F5. Expected impact: `Implemented → Ready for Review` is not blocked by a bookkeeping choice.

### 5.3 Automation / Script Improvements

- **REC-095-02 — Baseline reconstruction captures in-range guard health** — Target: `templates/commands/implement.md` § Baseline pre-flight + `templates/verification-log-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/`). Change: record per-module guard health at the reconstruction tree and refuse "inherited" for failures introduced inside the review range; name the in-range commit attribution in the provenance note. Source: F2. Expected impact: zero-NEW readings stop hiding in-range regressions.
- **REC-095-04 — Advance the loop-state block with every stage record** — Target: `skills/external/sdd-loop-driver/scripts/loop-state.py` + `references/stage-prompts.md` (U4) (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/`). Change: write the block (state, stage, attempt, last_verdict) as part of every stage record, and refuse a record appended without it. Source: F4. Expected impact: machine readers stop seeing a stale stalled state after implement.
- **REC-095-07 — Close the watcher/runner identity and stale-record gaps** — Target: `skills/external/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/`). Change: write `run=` into the pid line; archive the previous attempt's status file on re-dispatch; require status mtime newer than the pid file before DONE; return RUNNING at window expiry while the pid is alive. Sources: F7, F8, F11. Expected impact: run-scoped attribution works and false completion disappears.
- **REC-095-08 — Let the gate accept a locator plus note, and exempt per-unit bounds** — Target: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: parse the first token of a Source cell; exempt `per package` / `每包` from the count-claim matcher (or ban the phrasing in templates). Sources: F9, F10. Expected impact: first-pass plan/tasks gates; no author-side workarounds.

### 5.4 Workflow Improvements

- **REC-095-03 — Add a line-scoped commit guard** — Target: `skills/git-utils` scope A + the git model template under `.specify/workflow/`. Change: while a feature branch is active, refuse or explicitly record a commit whose subject carries no line id; the review's scope dimension reads that record. Source: F3. Expected impact: feature branches stay bisectable and reviewable; other-line regressions surface before merge.

### 5.5 Documentation Improvements

- **REC-095-06 — Align the code-review script's step census with the skill** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (header comment + usage) (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`). Change: five steps, `capture` named as step 5. Source: F6. Expected impact: one census across skill, command and script.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-095-01 — implement Feature Integration survives driver dispatch | `templates/commands/implement.md` + driver stage prompts | F1 |
| P1 | REC-095-02 — baseline reconstruction captures in-range guard health | implement template + verification-log template | F2 |
| P1 | REC-095-03 — line-scoped commit guard | `skills/git-utils` scope A + git model | F3 |
| P1 | REC-095-04 — loop-state block advances with stage records | `loop-state.py` + stage prompts | F4 |
| P1 | REC-095-09 — instantiate feature-detail carriers | `templates/feature-details-template.md` + feature-creation flow | F12 |
| P2 | REC-095-05 — frozen-baseline secondary carrier | `templates/commands/tasks.md` + implement template | F5 |
| P2 | REC-095-06 — five-step census in the code-review script | `git-delta-review.sh` | F6 |
| P2 | REC-095-07 — watcher/runner identity and stale-record gaps | `stage-runner.sh` + `watch-target.sh` | F7, F8, F11 |
| P2 | REC-095-08 — gate input parsing (locator + note; per-unit bounds) | `pre-analyze-check.py` | F9, F10 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: one P0 finding (F1) was raised and confirmed by an independent read-only validation subagent (`confirm`, P0) before entering this report; the validator received only the finding, its anchors and its quoted evidence.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
