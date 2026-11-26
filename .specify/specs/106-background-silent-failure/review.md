# Specification-Driven Development (SDD) Process Review Report: Background Dispatch Settlement — 后台派发静默退出结算契约

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 106 |
| Requirement Key | 106-background-silent-failure |
| Requirement Name | Background Dispatch Settlement — 后台派发静默退出结算契约（切片） |
| Related Feature | 095 Super Agent Role（本切片绑定的父特性） |
| Repository | spec-kit (`/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | (no remote holds these commits) configured remotes: `git@gitee.com:cloud-native-ai/spec-kit.git` (gitee), `git@github.com:cloud-native-ai/spec-kit.git` (github), `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (gitlab); `origin` is the upstream `github/spec-kit` and is a read-only reference |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — every citation below uses repo-relative or absolute paths plus `git show 0a01f797a:<path>` recovery instructions |
| Branch | `106-background-silent-failure` (temp-branch model; trunk `master`) |
| Commit SHA | 0a01f797a9f52d446c9069b029afda8ab8f65ea9 (short: 0a01f797a) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-11-26 |
| Reviewer (Agent) | SDD Review Executor (Qoder agent), run `r20261125T113505Z-106a`, stage `review`, attempt 1 |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash 4.4.20(1)-release; CPython 3.11.11 at `/usr/local/bin/python3` (repo `.venv` has no pytest); pytest 8.4.2; typer 0.19.2; git 2.43.5; no container runtime, cluster or network needed |
| spec-kit Source Snapshot | this repository @ 0a01f797a (self-hosting framework source = client runtime) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 311 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/requirements.md | 41 FR / 9 SC / 4 STR / A-1…A-18 / closed carrier inventory C1–C6 / settlement evidence matrix |
| plan.md | 217 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/plan.md | 23-row Constitution Check, T-001…T-003 decision tensions, EP-001…EP-005 premises (EP-005 falsified→fallback), mirror obligations |
| tasks.md | 361 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/tasks.md | 37 dependency-ordered rows, 34 clauses each claimed once, DoD-1…DoD-8, GATE-1…GATE-8 |
| verification.md | 65 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/verification.md | SC-001…SC-009 status rows, smoke triple, RS-001…RS-004 joint-acceptance rows (**materialized by this review from `test-evidence/verification-input.md` — see A1**) |
| research.md | 33 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/research.md | B-01…B-14 measurements + R-01…R-08 decisions (table form) |
| data-model.md | 163 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/data-model.md | E1–E9 entities, INV01…INV12 invariants, attempt state transitions |
| contracts/ (3 files) | 156 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/contracts/ | settlement C-01…C-12; carrier C-13…C-24; enforcement/migration C-25…C-34 |
| quickstart.md | 171 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/quickstart.md | S-0…S-7 with run-now / not-implemented-yet markers and pinning tests |
| feature-ref.md | 102 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/feature-ref.md | Feature 095 binding, 35 delivery-surface items, unit-registration verdict = no new unit |
| checklists/ (2 files) | 143 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/checklists/ | requirements checklist (18 `[x]`) + 40-item settlement checklist |
| notes/ (3 files) | 717 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/notes/ | pre-change measurements, red-first evidence ledger, quickstart run record |
| test-evidence/ (179 files) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/106-background-silent-failure/test-evidence/ | stage readings, analyze rounds/repairs, acceptance pack, drills, auth audit, review evidence |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements lands (2026-11-25) | commits `36a538e84`, `1b9ce922e`, `6f66b50fc`; spine U4: validator 0/0, pre-analyze pass 0 advisory | None; one disclosed degradation (`flow_class` payload `error=owner-unavailable` at dispatch because requirements.md did not exist yet) |
| 2 | clarify attempt 1 hits an environment anomaly | spine U3/U5: watcher `ANOMALY` (exit 11) — "`.git/config` is root-owned mode 600 and unreadable by uid 1001"; evidence `test-evidence/git-access-anomaly.txt` | Correct fast-fail behaviour (surfaced, not absorbed); driver repaired ownership, attempt 2 committed the on-disk artifacts |
| 3 | clarify attempt 2 binds Feature 095 + 3 adjudications | commits `c68e91344`, `3c793da7e` | None |
| 4 | plan set lands | commits `ba6585a5f`, `7eb405a28`, `6d1c85e44`; EP-005 falsified with a recorded fallback (gate total 31 ≠ pinned 27, pre-existing red) | None for content; one in-passing repair disclosed — the stage's own `workspace-plan-after.json` was all-null and was regenerated (`test-evidence/workspace-plan-after-driver.json`) |
| 5 | tasks set lands (37 rows) | commits `63adec172`, `1eff18747`, `0762f9a8f` | None; one in-passing fix of a missing FR quote in T013 |
| 6 | checklist stage (40 items) | commits `6dd33b02a`, `31a53d1e1`, `40856bb0d` | None |
| 7 | goal/team activation + agent render | spine § Goal/Team Activation: anchor + team + handoff; `specify render-agents --ai qoder` → 25 rendered | Prescribed; its render step refreshes a stale pre-existing debt-governor render (see I1) |
| 8 | analyze rounds 1–5 | reports `analyze-report-2026-11-25.md`, `analyze-report-r5-2026-11-26.md`; 20 confirmed C/H repaired across r1–r4; R5 0 C/H / 6 MEDIUM residual | One disclosed evidence boundary at R5: the reused W3-domain hash artifact is absent (see F3) |
| 9 | line PARKED (priority redirection) and resumed | spine § PARKED 2026-11-25T13:41Z; analyze PASS 2026-11-26 | None — clean-boundary park with exact reentry steps |
| 10 | implement packages P1–P4 | commits `ef807eead`…`0b59b17ad`; spine: baseline slot 1 (10049 passed / 218 failed names), four package verdicts pass | Two in-passing corrections disclosed (C1 pid-line reader T033; stale P3/P4 dispatch ranges, integrator corrected) |
| 11 | task table closed + integration record | commits `3d6b39c03`, `0eb18700d`; `test-evidence/implement-integration.md` | T037 GATE-8 could not be satisfied by its own seat (see F6); discharged by the integrator |
| 12 | registry row 106 → `Implemented` | commit `daada5c96`; `.specify/features.md` row 106 reads `Implemented`; `verification.md` **absent** on disk at this moment | **Deviation**: the `Planned → Implemented` gate's condition 2 (a `SC-NNN_status=` row per criterion in `verification.md`) had no carrier (see F1/A1) |
| 13 | review run (this report) | four segments + ARC; `verification.md` materialized from `verification-input.md` and RS joint-acceptance rows added; ARC re-run `accept`; code record `code-review.md` with receipt 331/49/282/0 | In-passing correction (A1), disclosed here |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. Both repaired in this run (F1/A1 are two views of one fact). |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 2 (F2, F6) |
| Automation / Scripts | 1 (F4) |
| Workflow | 5 (F1, F3, A1, I1, I2) |
| Documentation | 3 (F5, A2, A3) |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | fbab7a45c4a57b596bc32437181ee9eb799ebe60 | `git-delta-review.sh base --spec …` (feature-first-commit) |
| Head commit | 0a01f797a9f52d446c9069b029afda8ab8f65ea9 | run-start HEAD, fixed for this run |
| Base source | feature-first-commit | `base` step output |
| Renderer mode | text | non-interactive agent run (two-condition rule → text) |
| Changed / judged / skipped / gap files | 331 / 49 / 282 / 0 | copied from the record's coverage-receipt block |
| Segment verdict | not-evaluated | receipt-derived: 282 files legally skipped (`non-code-file` for stage records/evidence; `generated` for mirrors and per-tool copies) earn no coverage credit (C-37), so the segment cannot assert `pass`; 0 gap files |
| Gate verdict | allow | `report --summary --file` → `blocking_entries=0`, `gate=allow`; 2 `important` items, each answered in the record |
| Reason, when one applies | 49/331 files judge the code delta (engine, carrier script, owner/definition texts, skill/command/agent copies' sources, docs, six test modules, fixture tree); the 282 skipped paths are the stage's dated records (the artifact segment's object) and sync-generated mirrors/copies — legal skips, no coverage credit | receipt block in `code-review.md` |
| Uncommitted scope | 2 untracked review-run files at receipt time (`verification.md`, `code-review.md`) disclosed and not concluded over | receipt `**未提交范围（未评审）**` sentence in the record |
| Record | .specify/specs/106-background-silent-failure/code-review.md | written (triage `run`) |
| Archive | none | first run for this slice |

The record carries 0 `blocking`, 2 `important` (each answered), 1 `suggestion`, 1 `nitpick`, 2 `praise` — findings are read in `code-review.md` and are not restated here.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, verification.md, contracts/ (3 files), data-model.md, quickstart.md, research.md, feature-ref.md, test-evidence/ | union of the stage rules and `plan.md` § Project Structure (plan.md:108-119) |
| Coverage line | 10 / 10 | after the in-run repair (A1); 9 / 10 at review start |
| Missing members | none (at review start: `verification.md` — see A1) | disk listing before/after repair |
| Segment verdict | pass | no open P0 after the A1 repair; A2 (P1) and A3 (P2) remain disclosed |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 (repaired) | .specify/specs/106-background-silent-failure/verification.md | n/a — file was absent | file absent from disk; the derivation input `test-evidence/verification-input.md` is the anchor | verification.md missing at review start → ARC input error; materialized from the input + five duty-③ RS rows; ARC re-run `accept` (validated: direct re-read, subagent unavailable) |
| P1 | .specify/specs/106-background-silent-failure/quickstart.md | 28 | — | S-1's dispatch command cannot block as written: `DISPATCH_CLI_FLAGS="-c 'sleep 300'"` is word-split before `dispatch.sh` sees it; T033 had to substitute a fake CLI (see A2) |
| P2 | .specify/specs/106-background-silent-failure/plan.md | 181 | — | EP-001's extracted verdict-token set lists 8 tokens but the watcher block (and the guard's extractor) carry 9 (`USAGE`); equality to baseline still holds, the enumeration is under-inclusive (see A3) |

Also checked: FR count 41 / SC count 9 / STR count 4 (definition lines); 34 contract clauses each claimed exactly once by a monotone row order; Requirement Coverage Map covers 41/41 FR and 9/9 SC; 37/37 task rows closed; every `test-evidence/` pointer named in the acceptance pack resolves (15/15); `validate-tasks` PASS 0/0; `pre-analyze --stage tasks` decision=pass errors=0 advisories=2 (both adjudicated in `final-gate.txt`). `checklists/` is present but outside the derived denominator (optional-stage artifact; noted, not counted).

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | fbab7a45c4a57b596bc32437181ee9eb799ebe60 | code skill `base` resolution (same range) |
| Head commit | 0a01f797a9f52d446c9069b029afda8ab8f65ea9 | run-start HEAD |
| Base source | feature-first-commit | `base` step |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q` | `verification.md` smoke record, re-run at review |
| Smoke exit code | 0 | re-run at review: `57 passed in 6.47s` |
| Smoke evidence path | .specify/specs/106-background-silent-failure/test-evidence/review-evidence.txt | exists, non-empty (64 lines; t033-smoke.txt also present) |
| Scope and regression verdict | Scope: one P2 out-of-scope carry (I1 — a stale pre-existing render refreshed by the prescribed agent-render step); every other changed path maps to a task row or a mirror/generated obligation. Regression: engine `report`/`query` byte-identical to the recorded baseline (preservation test), `test_role_edge_engine.py` 25 passed, owner-page pins 10 passed, six settlement modules 100 passed; no requirement found undelivered except the FR-005 live-log window leg noted in I2/code record | this run's readings (`test-evidence/review-evidence.txt`) |
| Segment verdict | pass | no open P0; two P2 disclosed |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | .qoder/agents/sdd-debt-governor.agent.md | 32-42 | — | out-of-scope but disclosed: the prescribed `render-agents` step refreshed a stale render of a source changed in feature 105 (`6a62a8c3a`); the render manifest still maps it to the nonexistent `templates/sdd-debt-governor.agent.md` (see I1) |
| P2 | shared/definitions/superagent-definitions.md | 74 | — | FR-005's live-log-window liveness leg is declared (owner row + `--live-window`) but not consumed by the judgment face; the other liveness legs still satisfy the one-of rule (see I2; code record `important`) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Implemented | `.specify/features.md` row 106 (claimed_status_source in the checker payload) |
| `final_path` record, copied verbatim (7/7) | pass 3 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 3 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/106-background-silent-failure --repo . --json` → `verdict: accept`, `reasons: []` |
| Comparison verdict | agree | `accept` + claim `Implemented` |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The ARC ran only after the A1 repair (before it, the checker exited with `input error: required input not found: …/verification.md` — never an accept). The `final_path` record counts the three `final`-path criteria (SC-001 / SC-002 / SC-004).

## 3. Findings (Problems & Improvement Targets)

### F1 — `Planned → Implemented` was flipped without its gate product on disk

- **Severity**: P0 (repaired in this run; validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `.specify/features.md` row 106; `.specify/specs/106-background-silent-failure/test-evidence/implement-integration.md` § Residual observations item 5; `.specify/specs/106-background-silent-failure/verification.md` (absent at flip time)
- **Evidence** (verbatim quotes):

  ```
  Registry row 106: "… | Implemented | .specify/features/095-superagent-role.md | .specify/specs/106-background-silent-failure/requirements.md | 2026-11-26 (implemented: 37/37 tasks closed, P1–P4 verifier pass, …)"

  implement-integration.md: "**`verification.md` writeback** — T035 forbids the crew (and this seat) to write it;
  the spec-side `verification.md` remains the driver's post-input duty."

  tasks.md T035: "`verification.md` 由 spec 侧（驱动者）在该输入落盘后派生写回"
  ```
- **Why it's a problem**: the `Planned → Implemented` gate's condition 2 requires a `SC-NNN_status=` row per criterion in `verification.md`; the flip landed while that file did not exist, so a reader could not re-derive the claim — the same "status without its measurement" shape the acceptance-hardening owner calls a P0 by construction. The closure checker refused the tree (`input error: required input not found`) until this review materialized the file.
- **Proposed fix**: make the implement stage's Feature Integration step require a successful `closure-acceptance-check.py` run (or at minimum parse the derived `verification.md`) **before** the registry flip; the spec-side derivation step belongs in the implement prompt's sentinel conditions, not only in a task row.
- **Repair applied (this run)**: `verification.md` materialized from `test-evidence/verification-input.md` (all nine SC rows + the smoke triple, verbatim), plus five `RS-NNN_joint_acceptance=` rows binding the Runtime-Stack duty ③; ARC re-run → `verdict: accept`; artifact coverage 10/10.

### F2 — A "red-first" row was already green because an earlier row over-delivered its clauses

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `.specify/specs/106-background-silent-failure/tasks.md` lines 176 (T007), 261 (T028), 265 (T029); `test-evidence/implement-integration.md` § Residual observations item 1
- **Evidence** (verbatim):

  ```
  implement-integration.md: "the planned red could not reproduce because the T007 commit `eabebe7bf`
  already shipped `version_bearing`/`legacy` in the engine. No source was rolled back to fabricate a red;
  red capability is evidenced by T021/T025/T032."
  ```
- **Why it's a problem**: T007's row claims C-13/C-25…C-28, while the `settlement_version`/legacy split belongs to C-33 → T029. The engine commit shipped both at once, so T028's planned red (and T029's claim) had no live window. The implementer behaved correctly (disclosed, no rollback); the defect is that the task map does not bind a row to *only* its claimed clauses, and the red-first ledger therefore cannot vouch for T028's guard.
- **Proposed fix**: in `templates/commands/tasks.md` (and the `create-tasks` skill's row rules), make a row's `[green:]` claim set a **write-scope fence**: a row may not implement behavior whose clause belongs to a later row; when a design forces co-delivery, the generator must split the row or move the later claim onto the earlier row and record the red-window loss.

### F3 — Analyze round 5 reused a domain without the content-hash artifact its own protocol requires

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/state/background-silent-failure.md` § ANALYZE GATE; `skills/internal/analyze-artifacts` incremental protocol
- **Evidence** (verbatim):

  ```
  "**evidence boundary disclosed**: the reused W3-domain hash artifact is absent; W1 digest-verified;
  W3 reuse rests on the dispatch brief (no fresh R5 pass over W3). Does not affect the 0 C/H reading;
  carried to review."
  ```
- **Why it's a problem**: incremental analysis is legal only when the reused domain's content identity is recorded; here the reuse rests on prose in a dispatch brief, so "the artifacts did not change" is asserted rather than measured. It did not change the gate verdict this time, but the same hole would silently bless a real drift.
- **Proposed fix**: the incremental re-check gate should fail closed when the per-domain hash artifact is missing (emit `not-evaluated` for that domain and shrink the reuse set), instead of accepting a dispatch-brief basis; the hash file should be a named output of every analyze round.

### F4 — The workspace signature writer emitted an all-null "after" snapshot

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `scripts/python/workspace-guard.py`; evidence `.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-after.json` (all-null) and `workspace-plan-after-driver.json`
- **Evidence** (verbatim, spine):

  ```
  "**workspace evidence defect (in-passing repair)**: the stage's `workspace-plan-after.json` was written
  with all null fields (invalid snapshot); the before-signature check is `clean`, and the driver regenerated
  `workspace-plan-after-driver.json` (`clean`)."
  ```
- **Why it's a problem**: an invalid signature that renders as JSON looks like evidence; only a human noticing nulls kept it out of the record. A snapshot writer that cannot read the tree must fail loudly, not serialize emptiness.
- **Proposed fix**: `workspace-guard.py` should refuse to emit a snapshot whose required fields are all/mostly null (exit non-zero with the reason), and its `--check` should reject an all-null baseline as an input error.

### F5 — Stage records retype measured counts and drift

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/state/background-silent-failure.md` § U4 Verification — requirements
- **Evidence** (verbatim vs measurement):

  ```
  spine: "`requirements.md` (41 FR / 17 SC / 306 lines)"
  measured: 41 FR (definition lines), 9 SC (definition lines; validator `sc=9`), 311 lines (wc -l)
  ```
- **Why it's a problem**: the state spine is the reader's first summary; hand-retyped counts there disagree with the artifacts and with the validator's own output, so two "facts" exist for the same question.
- **Proposed fix**: the U4 record step should paste the validator's summary (which already prints `fr`/`sc`) instead of retyping counts, or cite the validator output path and print no numbers.

### F6 — GATE-8 as written cannot be satisfied by the task row that owns it

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `.specify/specs/106-background-silent-failure/tasks.md` line 37 (GATE-8) and line 285 (T037); `test-evidence/final-gate.txt` § GATE-8
- **Evidence** (verbatim):

  ```
  tasks.md GATE-8: "check: `grep -cE '^- \[[ >]\]' …/tasks.md` 返回 0"
  final-gate.txt: "This executor is assigned "do not mark the task table complete";
  the count above is the state at P4 hand-off."
  ```
- **Why it's a problem**: the final-gate row asserts a condition only the integrator can produce, so the row's own reading is necessarily red and every feature must carry a bespoke adjudication note. A gate that cannot pass for its owner trains readers to accept red gates.
- **Proposed fix**: split the task-table closure into an integrator-owned step and make T037's GATE-8 read the post-closure state (or record the ownership transfer in the gate text itself), so "0 open rows" is checkable by the seat that runs it.

### A1 — `verification.md` absent from the expected artifact set

(Recorded in §2.2's finding table; same fact as F1 from the artifact-completeness side. P0 at diagnosis, repaired in-run: materialized from `verification-input.md` + five RS duty-③ rows; ARC `accept`; coverage 10/10. Validated: direct re-read, subagent unavailable.)

### A2 — Quickstart S-1 cannot execute as written

- **Severity**: P1
- **Category**: Documentation
- **Location**: `.specify/specs/106-background-silent-failure/quickstart.md` line 28
- **Evidence** (verbatim):

  ```
  DISPATCH_CLI=/bin/sh DISPATCH_CLI_FLAGS="-c 'sleep 300'" \
  ```
  and T033's own record: "`DISPATCH_CLI_FLAGS="-c 'sleep 300'"` is word-split by the shell before dispatch.sh sees it (the literal quotes reach `sh` as separate words), so the quoted form cannot block"
- **Why it's a problem**: the quickstart is the page a maintainer runs first; its headline scenario (S-1) fails to reproduce the silent death it promises unless the reader invents the workaround the implement run disclosed. A later reader without that record sees only a broken example.
- **Proposed fix**: replace the flags value with a form that survives word splitting — e.g. ship the blocking fake CLI used by the carrier tests and call it by path (`DISPATCH_CLI_FLAGS="$PWD/tests/fixtures/settlement/blocking-cli.py"`), or use `DISPATCH_CLI=/bin/sh DISPATCH_CLI_FLAGS='-c "sleep 300"'` with the quoted form documented — and re-run S-1 verbatim (this review re-ran the scenario with a fixture CLI: SIGKILL → `silent-end`, rc 0).

### A3 — EP-001's verdict-token enumeration is under-inclusive

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/106-background-silent-failure/plan.md` line 181
- **Evidence** (verbatim vs live):

  ```
  plan.md EP-001: "extracted verdict tokens `{DONE,RUNNING,ANOMALY,FAILED,DEAD,TIMEOUT,INCOMPLETE,NO_SIGNAL}`"
  live watcher block (watch-target.sh:86-95) carries 9: the eight above plus `2 USAGE`;
  test_settlement_preservation.py EXPECTED_VERDICTS includes "USAGE".
  ```
- **Why it's a problem**: SC-003's criterion (equality to baseline) is met, but the premise's enumeration is a recorded measurement that disagrees with the guard's set — a reader comparing the two counts gets two answers for the preserved set.
- **Proposed fix**: correct the EP-001 enumeration to the 9-token set (or state that the set is whatever the verdict block carries and cite the guard), and align the quickstart S-2 grep listing.

### I1 — A stale pre-existing agent render refreshed inside this delta

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.qoder/agents/sdd-debt-governor.agent.md` lines 32-42; `.specify/agents/.render-manifest.json`
- **Evidence** (verbatim diff):

  ```
  - **History**: `.specify/history/` (theme KB), `.specify/memory/knowledge/` + `.specify/memory/session/`, …
  + **History**: `.specify/history/` (theme KB), `.specify/knowledge/` + `.specify/session/` (memory tiers), …
  ```
- **Why it's a problem**: the change is correct (the source `agents/sdd-debt-governor.agent.md` was updated in feature 105, commit `6a62a8c3a`, but the render was left stale), yet it belongs to no 106 task row, so the delta carries unattributed work. The manifest entry also names `templates/sdd-debt-governor.agent.md` as the source — a path that does not exist.
- **Proposed fix**: `specify render-agents` should refuse or disclose a refresh whose source has not changed in the current branch (render drift is a change like any other), and the manifest's `source` field should resolve; alternatively a `render --check` should be part of the close-out gates so drift is repaired where it is introduced.

### I2 — FR-005's live-log window leg is declared but not consumed

(Recorded in §2.3's finding table; the code record holds the `important` item with the same anchors: `role-edge-check.py:1672` accepts `--live-window`, the owner page's `running` row names "a live log growing inside the `--live-window` window" (superagent-definitions.md:74), but `_derive_settlement` never receives the value. The pid-liveness and open-return-channel legs keep the one-of liveness rule satisfied, so no gate failure.)

## 4. What Worked — Preserve (Brief)

- The **EP-005 falsification** was recorded as a `falsified` premise with a substituted fallback criterion, and every later stage repeated "never claimed green" — the honest-red pattern worked end-to-end.
- **Fast-fail discipline** in clarify attempt 1: the stage refused to repair a root-owned `.git/config`, wrote all artifacts, surfaced `ANOMALY:` with evidence; the driver repaired the environment and re-ran only the blocked work.
- **Additive-only carrier changes**: `dispatch.sh` kept its `.status` line byte-compatible, added `.attempt`/`.end` atomically, and the preservation test pins the old reader's result — the contract's "empty allowed-delta set" is measured, not asserted.
- **Real-process silent-death fixture**: the C2 test (and this review's S-1 re-run) SIGKILLs the shipped wrapper and proves `silent-end` from a start record plus absence — the defect class the feature exists for is demonstrated on the carrier.
- **Red-first ledger**: 437 lines of `notes/red-first-evidence.md` with commands, real outputs and exit codes; the two regression-guard exceptions are declared up front in the tasks "Tests Mode" line.
- **Mirror discipline**: all mirrors/copies regenerated by the owning scripts (`sync-mirrors.py`, `regen-command-copies.py` rc 0), zero hand edits; the watcher file hashes equal to `fbab7a45c`.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-106-01** — Target: `templates/verification-log-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`). Change: add an explicit "materialized by" marker line and a sentinel instruction that the implement stage MUST derive this file from `test-evidence/verification-input.md` **before** the Feature Integration flip (a stage without it counts as no implement result). Source: F1/A1. Expected impact: the gate product cannot be skipped again.

### 5.2 Command Prompt Improvements

- **REC-106-02** — Target: `templates/commands/tasks.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md`) and the `create-tasks` skill. Change: make a row's `[green:]` clause set a write-scope fence (no row may implement a later row's clause; co-delivery forces a split or an explicit red-window-loss record). Source: F2. Expected impact: red-first claims stay truthfully red.
- **REC-106-03** — Target: `templates/commands/tasks.md` + `skills/internal/create-tasks` completion-gate guidance. Change: generate the final-gate row so its checks are runnable by its owning seat (task-table closure moves to the integrator step; the gate reads the post-closure state). Source: F6. Expected impact: no more per-feature red-gate adjudications.

### 5.3 Automation / Script Improvements

- **REC-106-04** — Target: `scripts/python/workspace-guard.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/scripts/python/workspace-guard.py`). Change: refuse to emit a snapshot whose required fields are all/mostly null; treat an all-null baseline as an input error. Source: F4. Expected impact: invalid workspace evidence fails loudly instead of serializing emptiness.
- **REC-106-05** — Target: `skills/internal/analyze-artifacts` incremental protocol + its references. Change: fail closed when a reused domain's content-hash artifact is missing (emit `not-evaluated` for that domain, shrink the reuse set). Source: F3. Expected impact: incremental analysis reuse is measured, not asserted.
- **REC-106-06** — Target: `src/specify_cli` (`render-agents`). Change: disclose or refuse a render refresh whose source did not change on this branch; resolve the manifest's `source` field (the `templates/sdd-debt-governor.agent.md` key names a nonexistent path). Source: I1. Expected impact: agent-render drift stops riding along unlabelled deltas.

### 5.4 Workflow Improvements

- **REC-106-07** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` (U4 record step). Change: paste the validator's `fr`/`sc` summary instead of retyping counts (or cite its output path and print no numbers). Source: F5. Expected impact: one fact, one source; no stale summary counts.
- **REC-106-08** — Target: `skills/internal/create-team/scripts/dispatch.sh` + the settlement owner § C2. Change: on TERM/INT/HUP, signal the pipeline's process group after writing `.end`/`.status` (or document the orphan explicitly) so the terminal record does not imply the work ended. Source: code record `important` item (dispatch.sh:211). Expected impact: no orphaned CLI behind a terminal record.
- **REC-106-09** — Target: `scripts/python/role-edge-check.py` + the owner page's `running` row. Change: either implement the live-log-growth leg (honoring `--live-window`) or drop the option and the owner sentence; one of the two must stop being inert. Source: I2 / code record `important` item. Expected impact: declared boundary inputs change behavior or disappear.

### 5.5 Documentation Improvements

- **REC-106-10** — Target: `templates/commands/review.md` (or the quickstart authoring guidance in the `create-plan` skill). Change: executable quickstart examples must be validated verbatim by their pinning run — a scenario that needed a workaround is recorded as a failed example and repaired (spec-side) in the same change. Source: A2. Expected impact: the first page a maintainer runs actually runs.
- **REC-106-11** — Target: `.specify/specs/106-background-silent-failure/plan.md` EP-001 (and the same enumeration in `quickstart.md` S-2). Change: correct to the 9-token verdict set carried by the watcher block, or state that the set is whatever the extractor yields and cite the guard. Source: A3. Expected impact: preserved-set readings agree wherever they are printed.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Verification-log derivation is a stage condition before the registry flip | templates/verification-log-template.md + implement prompt | F1 / A1 |
| P1 | Clause write-scope fence for task rows | templates/commands/tasks.md + create-tasks | F2 |
| P1 | Analyze incremental reuse fails closed on a missing hash artifact | skills/internal/analyze-artifacts | F3 |
| P1 | Quickstart examples validated verbatim | templates/commands/review.md + plan authoring | A2 |
| P2 | Workspace snapshots refuse all-null output | scripts/python/workspace-guard.py | F4 |
| P2 | Runnable final gates for the owning seat | templates/commands/tasks.md | F6 |
| P2 | U4 counts pasted from the validator | sdd-loop-driver/references/stage-prompts.md | F5 |
| P2 | Render drift disclosed/resolvable | src/specify_cli (render-agents) | I1 |
| P2 | Live-log window leg implemented or removed | role-edge-check.py + owner § Termination | I2 |
| P2 | Dispatch trap signals the pipeline group | dispatch.sh + owner § C2 | code important |
| P2 | EP-001 verdict-token enumeration corrected | plan.md EP-001 / quickstart S-2 | A3 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: two P0 findings were raised (F1, A1 — one underlying fact from two segments). This executor is forbidden to dispatch a validation subagent, so both rows carry the documented fallback `(validated: direct re-read, subagent unavailable)`; the evidence is a two-state file-existence fact (absent before the repair, present and accepted after), re-read directly at diagnosis and after repair.

**Run-level disclosures (not findings)**: (a) `verification.md` and five `RS-NNN_joint_acceptance=` rows were materialized by this review (F1/A1 repair), from `test-evidence/verification-input.md`, with no invented readings; (b) `--live-window` and the C1 `sentinel=` token are parsed but not consumed (I2 / code `nitpick`); (c) the code segment is `not-evaluated` because legal skips earn no coverage credit — 0 gap files, 0 blocking entries, gate `allow`; (d) this run's own new files (`review.md`, `code-review.md`, `verification.md`, `test-evidence/review-evidence.txt`, `test-evidence/review.jsonl`, register rows, registry/detail status notes) were uncommitted at receipt time and are disclosed as unreviewed scope, not concluded over.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
