# Specification-Driven Development (SDD) Process Review Report: 095-superagent-role

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

Rendered by `/speckit.review`, run `r20261110T055657Z-b095-review-r2` — **review round 2** — four segments in the fixed order process → artifact → implementation → code, plus the Acceptance Reality Check; no order changed and no segment skipped. Round 1's report and code record are archived as `review-r1.md` and `code-review-r1.md`.

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
| Commit SHA | `2cf1e82ca513e3e265f781485e222834af3e9bbb` (short: `2cf1e82ca`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-10 |
| Reviewer (Agent) | Qoder CLI, `/speckit.review` four-segment run, round 2 (reviewer display name: Qiming Liu (John)) |
| Environment | Linux x64, bash, CPython 3.11.11 (`pyproject.toml` requires `>=3.8`), 192 CPUs, pytest runner `scripts/bash/run-tests.sh` (parallel default) |
| spec-kit Source Snapshot | self-hosting framework repo @ `2cf1e82ca` (framework sources + the same repo's `.specify/` runtime) |
| Review object (code segment) | `base..head` = `b3da3a26dfba209057f65c2b17962b9516812c39..2cf1e82ca513e3e265f781485e222834af3e9bbb`, base source `feature-first-commit` (the parent of the first 095 commit) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 287 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/requirements.md` | 38 FR / 10 SC / 6 shared strings; five user stories |
| plan.md | 247 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/plan.md` | D-1…D-14, T-001/T-002, 22-row Constitution Check, P1–P6 packages |
| tasks.md | 341 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/tasks.md` | 54 rows, 8 phases, DoD + GATE-1…GATE-6; T003 resolved |
| data-model.md | 115 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/data-model.md` | role/edge/executor/violation model, nine-item slugs, carrier row shapes |
| contracts/role-edge-engine.contract.md | 82 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/role-edge-engine.contract.md` | engine C-1…C-11 |
| contracts/role-transition-payload.contract.md | 67 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/role-transition-payload.contract.md` | payload/protocol C-1…C-13 |
| contracts/status-digest-role-view.contract.md | 47 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md` | digest role view C-1…C-8 |
| contracts/harness-landing.contract.md | 59 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/contracts/harness-landing.contract.md` | pointer section + zero-second-mechanism C-1…C-6 |
| quickstart.md | 57 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/quickstart.md` | four scenarios with per-example premises |
| verification.md | 135 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/verification.md` | SC status table + machine block + smoke record + cross-line commit register |
| feature-ref.md | 21 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/feature-ref.md` | Feature 095 binding + six-row mapping |
| observation-appendix.md | 30 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/observation-appendix.md` | 14 slice rows (6 exercised / 8 not-observed) |
| checklists/requirements.md | 55 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/checklists/requirements.md` | specification-quality checklist |
| checklists/requirements-quality-2026-11-10.md | 83 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md` | 39-item requirements-quality checklist |
| test-evidence/ | 90 files | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/test-evidence/` | gate/closure/smoke/mutation/repair readings + round-2 review captures |
| review-r1.md | 404 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/review-r1.md` | round-1 report (archived by this run) |
| code-review.md | 1481 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/code-review.md` | round-2 code segment record + coverage receipt |
| code-review-r1.md | 1377 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/code-review-r1.md` | round-1 code segment record (archived) |
| review.md | this file | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/095-superagent-role/review.md` | this report |
| Bound feature detail | 89 | `/storage/project/cloud-native-ai/spec-kit/.specify/features/095-superagent-role.md` | overview, planned changes, status criteria |

## 1. Process Execution Timeline

Reconstructed from `git log b3da3a26d..HEAD` and the append-only stage records in `/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md`. Rows 1–11 are round 1's reconstruction, retained for context; rows 12–14 are this round's new history.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements stage completed | `e2f760159`, `6a82f253c`, `9b3dbbc0d`, `c3507e4e6`; validator `status: ok` | none |
| 2 | clarify stage completed (10 self-rulings) | `4c515c08a`, `99586eb65`, `5aea9e5d4`, `71344d551`, `0b6a040b6`; overlap `decision=clear` | none |
| 3 | plan stage + one repair round | `448c1f3a3`, `99f0589d7`, `f6aea4f5a`, `2c8da54c0`; gate `decision=pass` | first plan gate red on a Source-cell format rule (F9) |
| 4 | tasks stage + one gate repair | `82f046aa1`, `1752a1acd`, `438fe6c97`, `035a572c0`, `4369dc7fe`; `validate-tasks` 0 error | count-claim regex false red (F10) |
| 5 | checklist stage | `841bef68d`, `293e0e063`; 39 items | none |
| 6 | analyze round 1 | `1793add54`, `8ef0a173f`, `c5609242d`; 2 CRITICAL + 12 HIGH | expected analyze findings |
| 7 | analyze repair + round 2 | `1e59f10e2`, `02b654b5c`, `b31f87ba5`, `d5a372d45`; round-2 gate FAIL 0C/4H → U5 stop-line | stop-line resolved only after an out-of-band interview ruling (`6d13938aa`) |
| 8 | analyze rounds 3–4 released | `1959550ab`, `d5b262fc0`, `3cee1381d`, `2da3a4ba2`, `75f2297db`, `c671e168a`; 0 CRITICAL / 0 HIGH open | none |
| 9 | implement P1–P6 | `b7e2a5bc8` (P1), `68f8968bd` (P2), `c7913da22` (P3), `aa548057f` + `23f1cd1fc` (P4), `d8843810f` (P5), `6c48e9c25` (P6) | T001 baseline never captured; T003 deferred; no `Planned → Implemented` flip (F1) |
| 10 | Other-line commits interleaved on this branch | `dddd09773`, `c2f199955`, `48d78d1a5`, `9c39b8e06`, `6d13938aa`, `57d364074`, `343ad1e1e` | 7 commits with no 095 task row (F3) |
| 11 | User-ruled constitution amendment inside the run | `dd7cbbab4` (1.19.0 → 1.19.1, Principle VII carrier `verification.log` → `verification.md`) | user-ruling change, outside the 095 task rows |
| 12 | Review round 1 (run `r20261110T055657Z-b095-review`) | `14652bfd0` (report + code record + register entries), `2c5ecfb80` (four-unit run records), `7a3a10798` (close-out receipt), `d54b1c012` (wording correction); verdict `blocked` | none (four segments + ARC executed; transition refused) |
| 13 | Review-repair r1 | `2cf1e82ca` + nine `review-repair-*` evidence files; disposition table `test-evidence/review-repair-dispositions-r1-2026-11-10.md`: 10 items fixed, F7/F8 deferred by budget | repair round directed by the user; two code `blocking` causes repaired and re-measured |
| 14 | Review round 2 (this run) | start `2026-11-10T15:46Z`; code record `code-review.md` (`2026-11-10T15:56:39Z`), receipt 344/17/327/0, gate `allow`; this report | transition re-judged and allowed (see § Status Transition) |

## 1A. Round-1 Closure Ledger (round 2's first duty)

| Round-1 item | Severity then | Round-1 location | Round-2 reading | Owner of what remains |
|---|---|---|---|---|
| **F1** implement never lands its owned `Planned → Implemented` transition | P0 | `verification.md:42`, `.specify/features.md:102` | **Closed**: the registry row reads `Implemented`, the feature detail carries `**Status**: Implemented`, and `verification.md` § Feature-list review records the flip after the four conditions re-verified. The reviewer's checker run returns `claimed_status=Implemented`, four conditions `true`, `verdict=accept` (`test-evidence/review-r2-closure-acceptance.json`) | REC-095-01 (driver stage prompt + sentinel) still open as a framework remedy |
| **Code blocking-1** 18 guard tests red at HEAD | blocking | `code-review-r1.md` | **Closed as a product defect**: `last_completion` is back in the only reachable renderer, `render_digest` is deleted, and the affected modules re-measure green. The reviewer's re-run reads 40 of 41 green; the single red is a *new* clock-sensitive guard introduced by the repair (see N1) | code record `important` N1 |
| **Code blocking-2** C-68 explicit state dropped, guard weakened | blocking | `code-review-r1.md` | **Closed**: the renderer emits one `store=no measurements` summary line (`scripts/python/status-digest.py:1572`), and the guard asserts exactly one such line with the entry rows unchanged (`tests/contract/test_efficiency_element.py:528`); Drill B goes red when the line is removed | — |
| **Code important C-1** digest reads the registry twice | important | `code-review-r1.md` | **Closed**: `read_carrier_inputs` returns `registry_payloads` (`scripts/python/role-edge-check.py:530`), `read_state` derives the legacy rows from that one read (`scripts/python/status-digest.py:1026`, `:1047`), and the guard is behavioural — an audit hook observes one registry-root scan and one open per entry (`tests/contract/test_status_digest_roles.py:187`); Drill A goes red with `observed 2 reads` | — |
| **F2** reconstructed baseline absorbs in-range breakage | P1 | `notes/baseline-provenance.md:7` | **Closed for this feature**: the provenance note carries per-module guard health with the rule "inherited only when also red at the range base" — 17 inherited, 1 in-range (`c2f199955`), 1 in-range fix; `verification.md` SC-009 states the same reading | REC-095-02 (template side) open |
| **F3** seven other-line commits make the delta non-feature-scoped | P1 | git range, commits listed in round 1 | **Mitigated by registration, not closed**: `verification.md` § 跨线提交 now records every one of the seven commits plus the user-ruling amendment with its provenance class and evidence; the scope review can read the register. The structural mechanism still does not exist | carried as F3 (this report § 3); REC-095-03 |
| **F4** loop-state machine block stale at "stalled / analyze round 2" | P1 | `.specify/state/095-superagent-role.md:3` | **Closed**: the block now reads `spine_state: active`, `stage: review-repair (round 1)`, and a `last_verdict` covering analyze r3/r4, implement P1–P6, review round 1 and the repair round | REC-095-04 (mechanism) open |
| **F5** frozen-baseline re-freeze deferred into the review gate | P2 | `verification.md:38`, `tasks.md:90` | **Closed**: the tasks-frozen baseline was copied to `notes/coverage-baseline-2026-11-10-tasks-frozen.txt` (642 lines, `base-sha 2c8da54c0`) and re-frozen in place (`coverage-baseline.txt`, 642 lines, `base-sha d54b1c012`); T003 is `[X]`; `deferred_tasks=none` | — |
| **F6** code-review script's step census vs its skill body | P2 | `skills/internal/code-review/scripts/git-delta-review.sh:88` | **Closed**: header and `--help` both read the five-step path with `capture` as step 5; the contract guard was aligned to five steps and passes | REC-095-06 marked done in the register |
| **plan D-1** declares `better-harness.md` unmodified | P2 | `plan.md:29` | **Closed**: D-1 carries a pointer to the later user ruling `dd7cbbab4` and names the file's actual change set | — |
| **F7** re-dispatch reads the previous attempt's status as DONE | P2 | state spine § FO-095-05 | **Open, budget-deferred**: recorded as FO-095-05 with the measured plan-round evidence and a proposed fix; this round's disclosure is the source of the carried finding | carried as F7 |
| **F8** `watch-target.sh --window` does not return RUNNING at expiry | P2 | state spine § FO-095-02 | **Open, budget-deferred**: recorded as FO-095-02 with the 200 s/340 s measurements | carried as F8 |
| **F9 / F10 / F11** gate and runner input defects | P2 | state spine § FO-095-06 / FO-095-07 / FO-095-01 | **Open, unchanged**: no disposition was recorded in r1; all three remain reproduce-able from the quoted FO lines | carried as F9–F11 |
| **F12** feature detail lacks the template's Status field and Latest Review | P2 | `.specify/features/095-superagent-role.md:1` | **Closed in instance**: the detail carries the full header field block and `## Latest Review`; the creation flow was not changed | REC-095-09 (creation flow) open |
| **Artifact P2** SC-007 budget readings unreconciled | P2 | `verification.md:18` | **Open**: still 38,301 B / 99 B beside 37,454 B / 946 B with no named source for the +514 B | carried as N2 |
| **Artifact P1** `verification.md` vs `tasks.md` on the implement-stage status obligation | P1 | `verification.md:42` vs `tasks.md:241` | **Half closed**: `verification.md` now records the flip and the tree follows the implement command; `tasks.md:5`/`:241` still instruct "stays `Planned` / no `features.md` edit" | carried as N3 |
| **Code important ×5** (team-root interrupted semantics, no-artifact executor permanently running, `CONST_LIVE` path, owner-page attribution, C-3.6 tautological seed) | important | `code-review-r1.md` | **Open, answered**: each is re-anchored at HEAD in the round-2 record and carries an explicit answer ("agreed — remains open") | code record `important` items |
| **Code suggestion ×5** (payload self-check model, conflict fixture shape, error-name tautology, `.gitignore` state de-indexing, ad-hoc appendix check) | suggestion | `code-review-r1.md` | **Open, carried**: re-recorded at their HEAD anchors in the round-2 record | code record `suggestion` items |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 8 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 6 |
| Workflow | 1 |
| Documentation | 2 |

**New P0/P1 this round: none.** The single P1 (F3) is carried from round 1, and the round-2 code segment raises no `blocking` entry. The eight P2s are six carried round-1 items (F7–F11 and the SC-007 reconciliation) plus two new round-2 observations (N1 verification evidence, N3 stale status literals).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `2cf1e82ca513e3e265f781485e222834af3e9bbb` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 344 / 17 / 327 / 0 | copied field by field from the record's coverage receipt block (never recomputed) |
| Segment verdict | `pass` | the record contains no `blocking` entry |
| Gate verdict | `allow` | `report --summary --file .specify/specs/095-superagent-role/code-review.md` exits 0, `blocking_entries=0` |
| Reason, when one applies | none | — |
| Uncommitted scope | 53 uncommitted paths disclosed at receipt time and never concluded over: the 44 pre-existing dirty paths from round 1 (agent mirrors, session/quant/feedback/todo runtime records, `checkpoints/`, etc.) plus 9 paths this run owns (the rotated `review-r1.md`/`code-review-r1.md`, the `review.md` deletion, and six `review-r2-*` evidence files); the full sentence lives in `code-review.md` § 未提交范围 | `uncommitted_scope=53` |
| Record | `.specify/specs/095-superagent-role/code-review.md` | written because triage is `run` |
| Archive | `.specify/specs/095-superagent-role/code-review-r1.md` | archived by the composition rule `<record>-<slice>.md` (slice `r1`) immediately before `start` created the new record; `start` therefore reported `archive=none` |
| Client capture | `skipped hat=framework basis=root owns framework source directories (templates/skills/shared/scripts/src/specify_cli); owner=.specify/shared/definitions/dogfooding-definitions.md § 2.1; triage=run` | the fifth non-interactive step's disclosure line |

This subsection carries the verdict and the pointers only: no opinion body and no per-severity item count. The findings live in `code-review.md` and are read there. The round-1 `blocking` causes are repaired and re-measured (see § 1A); the round-2 record's `important` items each carry an explicit answer.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/` (4 files), `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `observation-appendix.md`, `checklists/` (2 files), `test-evidence/` (90 files) | union of the standard spec-stage set and `plan.md` § Project Structure (lines 109–120) |
| Coverage line | 11 / 11 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | the two P2 rows below; no P0/P1 artifact finding |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `.specify/specs/095-superagent-role/verification.md` | 18 | none | SC-007 reports 38,301 B / 38,400 B (99 B headroom) while `requirements.md:285` (A13) and `plan.md:175` (EP-005) measured 37,454 B / 946 B; the intervening +514 B instruction insert from another line (`.specify/instructions.md` hunk of `57d364074`) is still not named, so the two readings cannot be reconciled from the artifacts (N2). |
| P2 | `.specify/specs/095-superagent-role/tasks.md` | 241 | none | T054 still instructs "confirm Feature 095 stays `Planned` … no `.specify/features.md` edit" (its own parenthetical says "implement advances"), and `tasks.md:5` plus `checklists/requirements-quality-2026-11-10.md:5` still state the row as `Planned`, while the registry, the feature detail and `verification.md` now read `Implemented`. The implement-stage instruction that produced F1 survives in the artifact (N3). |

One row per finding. `line` is required whenever the artifact is line-addressable; every member above is markdown and line-addressable. Traceability re-measured mechanically this round: 38/38 FR reach at least one task row, 10/10 SC reach a task row and a `verification.md` status row.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `2cf1e82ca513e3e265f781485e222834af3e9bbb` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code skill's `git-delta-review.sh` reported |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_role_edge_engine.py tests/contract/test_role_transition_payload.py tests/contract/test_status_digest_roles.py tests/contract/test_superagent_definitions.py tests/contract/test_instructions_budget_superagent_section.py tests/contract/test_superagent_zero_mechanism.py -q` | recorded verbatim from `verification.md`; re-run by this review |
| Smoke exit code | 0 | the integer the command returned; re-run at review time: 85 passed, exit 0 |
| Smoke evidence path | `.specify/specs/095-superagent-role/test-evidence/review-r2-smoke.txt` | exists and non-empty (this run's own capture) |
| Scope and regression verdict | scope passes with registration (the 7 other-line commits plus the user-ruling amendment are each registered with provenance in `verification.md` § 跨线提交; the structural guard remains F3); regression passes — repaired guard modules re-measured green except the clock-sensitive guard recorded as a code `important`, and the closure full suite reads 216 failed / 8414 passed / 2 skipped against the 303-name baseline, NEW = 3 names all environment/concurrency-owned and named (two in SC-009's ledger; `test_script_interface_contract.py::test_c15` is a parallel-scan race on a vanishing `.specify/.tmp` directory, green when re-run alone) | the segment's own reading |
| Segment verdict | `pass` | no P0/P1 finding in this segment this round |

No findings this round: the delta's scope and regression readings are the verdict above, and the one code-level defect surfacing during the regression re-measurement is recorded under its own vocabulary in `code-review.md` (N1).

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | the bound feature detail's registry claim (`.specify/features.md` row 095), copied |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7 | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/095-superagent-role --json`, never recomputed here (`test-evidence/review-r2-closure-acceptance.json`) |
| Comparison verdict | `agree` | checker verdict `accept`; the `Implemented` claim agrees with the evidence; no ARC refusal condition fires |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition judgement — allowed.** The transition `Implemented → Ready for Review` is judged once, after both artifacts exist; its four conjunctive conditions are owned by `templates/feature-details-template.md` § Canonical Status State Machine and cited, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | the checker's `tasks` block: `closed=54`, `deferred=0`, `open=0`; T003 resolved by archive-then-refreeze | satisfied |
| (b) review evidence produced | this report and `code-review.md` are on disk | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `report --summary --file` exits 0, `blocking_entries=0`, `gate=allow` | satisfied |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 7 `pass`, zero in every non-pass bucket | satisfied |

The flip lands on both carriers: `.specify/features.md` row 095 and `.specify/features/095-superagent-role.md` (`**Status**`), and the feature detail's `## Latest Review` entry records this run's conclusions. No waiver is needed and none is claimed.

## 3. Findings (Problems & Improvement Targets)

### F3 — The feature branch still carries seven other-line commits; registration is not a guard

- **Severity**: P1 (carried from round 1)
- **Category**: Workflow
- **Location**: git range `b3da3a26d..2cf1e82ca`, commits `dddd09773`, `c2f199955`, `48d78d1a5`, `9c39b8e06`, `6d13938aa`, `57d364074`, `343ad1e1e`; the mitigation is `.specify/specs/095-superagent-role/verification.md:44` § 跨线提交
- **Evidence** (verbatim quote):

  ```
  代码段 delta `b3da3a26d..6c48e9c25` 内的 7 个无 095 任务行的提交与 1 个用户裁定修订，逐个登记出处。
  ```

  and, from the range: `c2f199955 feat(status): executor-primary digest — closed lines hidden, one row per live agent execution` / `57d364074 chore(harness): .specify/state is runtime — ignored, untracked, and the ignore set is framework-maintained`
- **Why it's a problem**: the register makes the scope reviewable for this feature, but it is a per-feature workaround: the delta still spans four unrelated subjects, per-feature bisectability is still lost, and the next feature pays the same cost. The 18 red guards that round 1 found were a direct consequence of commits no task row asked for.
- **Proposed fix**: add a line-scoped commit guard to the git workflow — while a feature branch is active, a commit whose subject carries no line id is refused or explicitly recorded as a cross-line commit, and the review's scope dimension reads that record (`skills/git-utils` scope A + the git model template under `.specify/workflow/`; REC-095-03).

### F7 — A re-dispatched stage can still be instantly "DONE" from the previous attempt's status file

- **Severity**: P2 (carried; deferred by the repair round's budget)
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-05 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/state/095-superagent-role.md`)
- **Evidence** (verbatim quote):

  ```
  FO-095-05（假完成，U3 面）：同一阶段**重派发**时，上一轮的 `status-<line>-<stage>` 文件留在原路径；
  `watch-target.sh` 读到旧 status（`exit=0 sentinel=1`）立刻判 `DONE`，而新子进程仍 `pid=alive`
  ```
- **Why it's a problem**: retries and repair rounds are routine; a stale status record can declare a live attempt finished, and only an independent U4 validation caught it in this run. The repair round deferred this by budget with the FO recorded — that disclosure is the mandated handling, and the finding stays open rather than silently dropped.
- **Proposed fix**: on re-dispatch, `stage-runner.sh` archives the previous attempt's `status-<line>-<stage>` before the new pid file lands, and `watch-target.sh` requires the status mtime to be newer than the pid file before judging DONE (REC-095-07).

### F8 — `watch-target.sh --window` does not return RUNNING at window expiry while the pid is alive

- **Severity**: P2 (carried; deferred by the repair round's budget)
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-02
- **Evidence** (verbatim quote):

  ```
  FO-095-02（监听窗口）：`watch-target.sh --window 120/180` 在 pid 存活时不会按窗口到期返回 RUNNING
  （实测 200s/340s 工具超时仍未返回），与 `stage-prompts.md` § U3「窗口到期只返回 RUNNING 并立即重入」的叙述不一致
  ```
- **Why it's a problem**: the driver's bounded-wait protocol is documented but not delivered; hosts must background the command, which degrades the wait into a notification race (REC-095-07 carries the fix).
- **Proposed fix**: implement window-expiry RUNNING in `watch-target.sh` as `stage-prompts.md` U3 describes, or correct the documentation to the measured behaviour.

### F9 — The plan gate rejects a Source locator followed by a note, while the plan template never says the cell must be bare

- **Severity**: P2 (carried; not dispositioned in round 1)
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-06
- **Evidence** (verbatim quote):

  ```
  FO-095-06（门禁与模板表述）：`pre-analyze-check --stage plan` 要求「Source row」单元格为裸
  `<feature>:<row>` 定位符，但计划模板/作者指引未提示「注记不得与定位符同格」，首轮 plan 因此 exit 2
  ```
- **Why it's a problem**: a format rule enforced by the gate but stated nowhere the author reads costs a repair round per plan; the failure is mechanical, not semantic.
- **Proposed fix**: accept a locator followed by a separator and note (parse the first token) or state the bare-cell rule in the plan template's table header (REC-095-08).

### F10 — The count-claim gate reads a per-package bound as a total-count claim

- **Severity**: P2 (carried; not dispositioned in round 1)
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-07
- **Evidence** (verbatim quote):

  ```
  FO-095-07（计数断言门 vs 分包上界表述）：`pre-analyze-check --stage tasks` 的 count-claim 模式
  `(\d+)\s*tasks?` 会把 plan 中「≤16 tasks per package」（每包上界）读成**总量声明**并对照 tasks.md
  实际条数判红（本轮 plan.md:217 vs 54）
  ```
- **Why it's a problem**: the template itself invites the phrasing the gate rejects; the author must discover the trap by a red gate and write around it.
- **Proposed fix**: exempt per-unit bounds (`per package` / `每包`) from the count-claim matcher, or ban the phrasing in the plan/tasks templates (REC-095-08).

### F11 — The stage runner's pid line carries no `run=` field, so run-scoped attribution is unavailable

- **Severity**: P2 (carried; not dispositioned in round 1)
- **Category**: Automation
- **Location**: `.specify/state/095-superagent-role.md` § 框架观察 FO-095-01
- **Evidence** (verbatim quote):

  ```
  FO-095-01（064 归属面）：`stage-runner.sh` 写入的 `pid-<line>-<stage>` 行只有
  `pid= start= at= line= stage= event=`，**缺 `run=` 字段**；`watch-target.sh` 的 `classify_pair`
  要求 line 与 run 同时匹配才判 `own`
  ```
- **Why it's a problem**: every watcher invocation with `--run-id` degrades to `unattributed` / `pid=missing` — the multi-line attribution feature (064) is unusable exactly in the case it was built for.
- **Proposed fix**: `stage-runner.sh` writes `run=<run-id>` into the pid line, or `watch-target.sh` falls back to the registry's recorded pids as the identity source before the pid-file gate (REC-095-07).

### N1 — The repair round's evidence is a single run per suite, so a clock-sensitive guard passed as green

- **Severity**: P2
- **Category**: Automation
- **Location**: `tests/unit/test_status_digest_unit.py:657` (the guard); `test-evidence/review-repair-suite.txt` (the evidence)
- **Evidence** (verbatim quote from the repair's reading):

  ```
  41 passed in 5.98s
  ```

  and the repair's own rewrite of the guard:

  ```
  -    first = _digest(workspace, registry, "--cap", "5")
  -    second = _digest(workspace, registry, "--cap", "5")
  +    first = _json_stdout(_digest(workspace, registry, "--cap", "5", "--format", "json"))
  +    second = _json_stdout(_digest(workspace, registry, "--cap", "5", "--format", "json"))
  ```

  measured by this review: the guard fails on a healthy tree when the two renders straddle a one-second boundary (`age_seconds` 395291 vs 395292; 1 failure in 8 isolated runs, `test-evidence/review-r2-guards.txt`).
- **Why it's a problem**: the single run that recorded the repair's green could not distinguish a stable guard from a lucky one. The concrete guard defect is recorded under the code segment's own vocabulary (`code-review.md`, `important`); this finding is about the evidence discipline that let it pass — a repair that rewrites a determinism claim owes a repeat reading, not one sample.
- **Proposed fix**: in a repair round, re-run the determinism-sensitive selection at least twice (or freeze the clock in the guard) before recording green; state the repeat count beside the reading in `verification.md` (`templates/verification-log-template.md` + `templates/commands/implement.md` § Test runs; REC-095-10).

### N2 — SC-007's 38,301 B reading and the plan's 37,454 B reading still have no reconciliation

- **Severity**: P2 (carried from round 1's artifact segment)
- **Category**: Documentation
- **Location**: `.specify/specs/095-superagent-role/verification.md:18`
- **Evidence** (verbatim quote):

  ```
  generator `BUDGET:` ends `within` — 38,301 B / 38,400 B budget, 99 B headroom
  ```

  against `requirements.md:285` (A13): `本阶段实测 .specify/instructions.md = 37,454 B、templates/instructions-template.md = 32,975 B、… 余量 946 B`, and `plan.md:175` (EP-005): `measured wc -c: .specify/instructions.md = 37,454 B … → 946 B headroom`
- **Why it's a problem**: both readings are real, but no artifact names the +514 B insert that separates them (the `.specify/instructions.md` hunk of `57d364074`, written by another line between the plan measurement and the generator run). A reader cannot tell whether the budget moved, the template moved, or the measurement is wrong.
- **Proposed fix**: state the intervening delta and its source commit beside the fresh reading (or record both readings with their measurement trees/dates) in `verification.md` SC-007.

### N3 — The tasks artifact still instructs the implement stage to keep the feature `Planned`

- **Severity**: P2 (the surviving fragment of round 1's artifact P1)
- **Category**: Documentation
- **Location**: `.specify/specs/095-superagent-role/tasks.md:241` (T054); also `tasks.md:5`; `checklists/requirements-quality-2026-11-10.md:5`
- **Evidence** (verbatim quote):

  ```
  - [X] T054 Record the Feature-list review — confirm Feature 095 stays `Planned` (feature-integration
    table: `/speckit.tasks` maintains `Planned`; implement advances) and that the task breakdown exposed
    no new or invalidated Feature; write the one-line record into `verification.md`; no `.specify/features.md`
    edit [blockedBy: T051] (requirements.md § Related Feature; constitution Principle II)
  ```

  and `tasks.md:5`: `**Related Feature**: … — `.specify/features.md` row `Planned`（tasks 阶段只维护 `Planned`，不改状态）`
- **Why it's a problem**: the row's main clause and its parenthetical contradict each other, and the instruction is exactly the one that produced round 1's P0 — the tree now follows the implement command, but the artifact still tells a future executor to do the opposite. The checklist line states `Planned` as a present fact.
- **Proposed fix**: amend T054 to state the implement stage owns the flip (the row is closed; its instruction should read as the historical tasks-stage record), and update the checklist line to point at the registry instead of restating a status.

## 4. What Worked — Preserve (Brief)

- The disposition table made the repair auditable item by item: 10 of 12 items closed with a named evidence file each, and the two budget deferrals named rather than dropped.
- The C-1 repair replaced an AST call-site proxy with a behavioural audit-hook guard (one registry-root scan, one open per entry) and shipped a mutation drill that turns red on a seeded second read.
- The archive-then-refreeze disposition gave T003 a legal resolution without breaking the analyze reports' citations.
- The per-module guard-health attribution (17 inherited / 1 in-range / 1 fixed) turned "zero NEW failures" from a subtraction into an attribution.
- The five-step census fix carried its contract guard with it: the four-step test was renamed and re-asserted as five steps, and the module stays green.
- The closure checker's explicit-carrier path now reads `claimed_status=Implemented` with all four conditions true — the round-1 P0's repair is machine-visible, not prose.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **REC-095-07 — Close the watcher/runner identity and stale-record gaps** — Target: `skills/external/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/`). Change: write `run=` into the pid line; archive the previous attempt's status file on re-dispatch; require status mtime newer than the pid file before DONE; return RUNNING at window expiry while the pid is alive. Sources: F7, F8, F11. Expected impact: run-scoped attribution works and false completion disappears. Carried; still open.
- **REC-095-08 — Let the gate accept a locator plus note, and exempt per-unit bounds** — Target: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: parse the first token of a Source cell; exempt `per package` / `每包` from the count-claim matcher (or ban the phrasing in templates). Sources: F9, F10. Expected impact: first-pass plan/tasks gates; no author-side workarounds. Carried; still open.
- **REC-095-10 — Make a repair round's determinism evidence a repeat reading** — Target: `templates/verification-log-template.md` + `templates/commands/implement.md` § Test runs (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/`). Change: when a repair rewrites a determinism guard, the recorded green must name the repeat count (or a frozen clock) for the determinism-sensitive selection; a single sample is not evidence of determinism. Source: N1. Expected impact: clock-sensitive guards stop passing as green once.

### 5.4 Workflow Improvements

- **REC-095-03 — Add a line-scoped commit guard** — Target: `skills/git-utils` scope A + the git model template under `.specify/workflow/`. Change: while a feature branch is active, refuse or explicitly record a commit whose subject carries no line id; the review's scope dimension reads that record. Source: F3. Expected impact: feature branches stay bisectable and reviewable; other-line regressions surface before merge. Carried; still open. (REC-095-06, the five-step census, landed in `2cf1e82ca` and is marked done in the register.)

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-095-03 — line-scoped commit guard | `skills/git-utils` scope A + git model | F3 |
| P2 | REC-095-07 — watcher/runner identity and stale-record gaps | `stage-runner.sh` + `watch-target.sh` | F7, F8, F11 |
| P2 | REC-095-08 — gate input parsing (locator + note; per-unit bounds) | `pre-analyze-check.py` | F9, F10 |
| P2 | REC-095-10 — repair-round determinism evidence is a repeat reading | verification-log template + implement template | N1 |

The spec-side P2s (N2 budget reconciliation, N3 stale `Planned` literals) are repaired by editing this feature's own artifacts and become review evidence on the next run; they carry no framework recommendation.

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
