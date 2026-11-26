# Specification-Driven Development (SDD) Process Review Report: Team View Degradation Hardening（真实团队定义下的诚实呈现与降级语义）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.
> **Segment verdicts (console conclusion)**: process `pass` (0 P0; 3 P1 / 5 P2) · artifact `pass` (coverage 10/10 after the in-run materialization of `verification.md`; 0 P0/P1, 4 P2) · implementation `pass` (smoke 37 passed exit 0; targeted set 149 passed with 0 new failure names; 1 P2) · code `not-evaluated` (receipt 264 changed / 6 judged / 258 legally skipped / 0 gap; 0 blocking, gate allow) · Acceptance Reality Check `accept` (`agree` with the claim).

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 108 |
| Requirement Key | `108-team-view-degradation` |
| Requirement Name | Team View Degradation Hardening — 真实团队定义下的诚实呈现与降级语义 |
| Related Feature | 027 Team Management（slice row 108 in `.specify/features.md`） |
| Repository | spec-kit (self-hosting framework repository) |
| Repository URL | remotes: `gitee` git@gitee.com:cloud-native-ai/spec-kit.git · `github` git@github.com:cloud-native-ai/spec-kit.git · `gitlab` git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git · `origin` git@github.com:github/spec-kit.git (upstream). All are SSH-only; none carries this branch. |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch is unpushed (push is forbidden for this line until close-out). Every citation below is an absolute path plus `git show <sha>:<path>` recovery. |
| Branch | `108-team-view-degradation` (checked out in the worktree below) |
| Commit SHA | `4262522f4e3eaeb4b0a8caac25f0e1c1211c5708` (short: `4262522f4`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/team-view-degradation` (git worktree of `/storage/project/cloud-native-ai/spec-kit`) |
| Review Date | 2026-11-26 |
| Reviewer (Agent) | SDD Review Executor (Qoder CLI agent, dispatched by the SDD driver; spec side) |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash 4.4.20(1); git 2.43.5; CPython 3.11.11 (`/usr/local/bin/python3`); pytest 8.4.2 |
| spec-kit Source Snapshot | this repository at `4262522f4` (self-hosted; framework sources and client-runtime mirrors in one tree) |
| Line / run | line `team-view-degradation`; run `r20261126T071500Z-108a`; implement baseline commit `005437f72`; program fidelity baseline `54c6efa8c` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 238 | `…/worktrees/team-view-degradation/.specify/specs/108-team-view-degradation/requirements.md` | 25 FR / 8 SC / 3 STR / A-1…A-17 / US1–US3 / 5 RS rows / 2 Clarifications sessions |
| plan.md | 155 | `…/108-team-view-degradation/plan.md` | 23-principle Constitution Check, 9 Execution Premises, Inherited Blockers (027, empty extraction set), mirror obligations, Decision Tensions N/A |
| tasks.md | 331 | `…/108-team-view-degradation/tasks.md` | 29 rows, 35 clause green claims (T012/T018/T025), 8 DoD / 8 GATE, all closed |
| data-model.md | 166 | `…/108-team-view-degradation/data-model.md` | 10 entities C1–C10, 10 invariants INV-01…INV-10, envelope shape, FR→entity map |
| contracts/ (4 files) | 169 | `…/108-team-view-degradation/contracts/` | C-101…C-109, C-201…C-208, C-301…C-309, C-401…C-409 (35 clauses) |
| quickstart.md | 153 | `…/108-team-view-degradation/quickstart.md` | 8 scenarios S-0…S-7 with per-example premises |
| research.md | 143 | `…/108-team-view-degradation/research.md` | 8 measurements M1–M8 + 15 resolved design points R-1…R-15 |
| feature-ref.md | 77 | `…/108-team-view-degradation/feature-ref.md` | Feature 027 binding, delivery surface, FR→surface / SC→evidence maps, supersession, overlap adjudication |
| checklists/ (2 files) | 40 items | `…/108-team-view-degradation/checklists/` | requirements-quality checklist (CHK001…CHK040) plus the clarify checklist |
| verification.md | 87 | `…/108-team-view-degradation/verification.md` | **Derived in this review** (absent on disk at review start by design — tasks DoD-8/GATE-4 declare it spec-side): 8 SC rows, 5 RS joint-acceptance rows, smoke triple |
| review.md (this file) | — | `…/108-team-view-degradation/review.md` | four segments + ARC |
| code-review.md | 1130 | `…/108-team-view-degradation/code-review.md` | code segment record with the coverage-receipt block |
| test-evidence/ | 162 files | `…/108-team-view-degradation/test-evidence/` | baselines, red captures, targeted set, shape guard, analyze rounds, implement integration, review re-runs |
| notes/ | 6 files | `…/108-team-view-degradation/notes/` | pre-change measurements, red-first evidence, per-US green records, quickstart run |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements: spec scaffolded by hand | `ac6723037`; requirements.md A-16: "`create-new-requirements.sh` 会把当前本地分支 `108-team-view-degradation` 计入编号空间而派生 109 并新建分支；与本线「不建第二分支、规格编号 108」冲突。按 107 先例，本阶段**手工**从 … 脚手架" | Recorded deviation (script derives 109 from the current branch; manual equivalent used, disclosed) |
| 2 | requirements attempt 1: sentinel present, artifacts uncommitted | state spine `U4 — requirements attempt 1: INCOMPLETE (false-completion candidate)` — "sentinel `REQUIREMENTS-DONE` present, but: spec dir uncommitted; no `test-evidence/workspace-requirements.json`; no stage Wrap-up records for 108" | Yes — completion sentinel was decoupled from artifact state; repaired by attempt 2 (`990eeaf8f`) |
| 3 | clarify: Feature 027 binding; brief candidate corrected | `1f18814da`, `fb4ac4e07`; requirements.md: "Brief 的 leading candidate `103-team-view` 经查找为已定稿的 spec 编号而非 Feature ID" | Brief premise corrected in-stage (recorded) |
| 4 | plan: design set landed; workspace signature invalid | `eba1aa7ad`, `d16559ff5`; `e0f30bf88`; `679301b65` (driver post-stage snapshot); spine correction: "the plan stage's `workspace-plan.json` and `workspace-plan-postcommit.json` are both invalid (all-null; `--check` reports before=None)" | In-stage adjudication with residual (workspace signature; overlap=72 historical/non-concurrent in feature-ref.md) |
| 5 | tasks + checklist stages | `c8f153a2a`, `c491676f8`, `c4e40178c`, `eca0f9d88`, `842ee7714` (anchor/team/handoff; the same commit also refreshed the generated `.specify/agents/.render-manifest.json` timestamp — a generated side effect, no requirement asks for it) | Checklist brief premise "plan + 3 contracts" was stale (4 contracts existed) — recorded in feedback |
| 6 | analyze: four rounds; three repairs | R1 2 HIGH (`01e0f9f29`) → R2 2 HIGH (`16e014194`) → R3 1 HIGH (`c247f6325`) → R4 0 C/H (`58482e133`); `005437f72` merged master into the branch | Loop by design; the classes it caught were machine-detectable at generation (F2/F3) |
| 7 | implement: P1–P4 serial packages; P1 retried | P1 `c55521f3c..74ae2e076` (a1 verdict fail — E2 row missing `trigger`; a2 pass), P2 `83bb3bdea..33303ba94`, P3 `2db7c8ca9..3477f63f1`, P4 `0588a2114..31994cc90`, integration `9cdbafd00`, wrap-up `347dd694f`, U4 `f93467922`, registry `4262522f4` | P1 retry was a record-schema defect, disclosed; writeback gap for T019–T029 surfaced (F6) |
| 8 | review (this run): verification derived, four segments, ARC, code record | `verification.md` (derived); test-evidence/review-{smoke,targeted,targeted-failed,quickstart}.txt; `code-review.md`; this file; `test-evidence/review.jsonl` | No P0 found; `Implemented → Ready for Review` gate passes (ARC `accept`, code gate allow) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 10 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 (A2) |
| Command Prompt | 2 (F7, A1) |
| Automation / Scripts | 2 (F4, F5) |
| Workflow | 6 (F1, F2, F3, F6, I1) |
| Documentation | 3 (F8, A3, A4) |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `54c6efa8c9a93a107400a0256504a5f3169f5c04` | resolved diff base |
| Head commit | `4262522f4e3eaeb4b0a8caac25f0e1c1211c5708` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Renderer mode | `renderer: text` | record header (no TTY; non-interactive agent invocation) |
| Changed / judged / skipped / gap files | 264 / 6 / 258 / 0 | copied field by field from the record's coverage-receipt block |
| Segment verdict | `not-evaluated` | skips earn no coverage credit (code-review skill C-37) |
| Gate verdict | allow | `report --summary --file .specify/specs/108-team-view-degradation/code-review.md` exit 0; 0 `blocking`, 0 `important` |
| Reason, when one applies | 258 files legally skipped — the feature's spec artifacts, session/feedback/retention/exec-quant records and the team archive (`non-code-file`), plus the two generated mirrors and the generated agent manifest (`generated`); the 6 code/product files (`scripts/python/team-view.py`, the three new test modules, `docs/reference/commands/team.md`, `skills/internal/view-team/SKILL.md`) were all judged | — |
| Uncommitted scope | "未提交范围（未评审）: 5 个未提交路径未计入本次评审对象（…/verification.md, …/test-evidence/review-quickstart.txt, …/test-evidence/review-smoke.txt, …/test-evidence/review-targeted-failed.txt, …/test-evidence/review-targeted.txt）；本回执不对该范围给出任何结论。" (disclosed at receipt time; all five land in the review commit) | same sentence in `code-review.md` |
| Record | `.specify/specs/108-team-view-degradation/code-review.md` | written (triage `run`) |
| Archive | `none` | first run for this feature |

The code record carries 0 `blocking`, 0 `important`, 3 `suggestion`, 1 `nitpick`, 0 `question`, 2 `praise`. Client capture is `skipped`: this repository wears the framework hat (`shared/definitions/dogfooding-definitions.md` § 2.1: "root owns framework source directories"), so no client feedback entry is written.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, data-model.md, contracts/ (4), quickstart.md, research.md, feature-ref.md, checklists/ (2), test-evidence/, verification.md | stage rules + `plan.md` § Project Structure (the union is 11 members: the plan's structure list, with contracts/ and checklists/ counted as directories) |
| Coverage line | 11 / 11 (10 / 11 at review start; `verification.md` was absent by design — DoD-8 declares it spec-side — and was derived in-run) | present members / expected members |
| Missing members | none after derivation (at review start: `verification.md`) | — |
| Segment verdict | `pass` (P0/P1 = 0; four P2 findings below) | — |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `.specify/specs/108-team-view-degradation/quickstart.md` | 137 | — | A1: S-7's pinning-test list names `test_label_constants_match_the_owner_table`; that node exists nowhere (zero occurrences in `tests/contract/test_team_view_degradation_contract.py`) — the executed and tasks-pinned node is `test_label_closure_both_directions`. The quickstart-run record maps the name by hand ("Name correspondence (disclosed, not silent)"), so the traceability link has no target in the artifact itself |
| P2 | `.specify/specs/108-team-view-degradation/tasks.md` | 18 | — | A2: DoD-2's declared change surface enumerates "上述 8 个交付文件 + `{notes,test-evidence,writeback}/**` + `checkpoints/**` 与 `coverage-baseline.txt` + handoff 记录类存储组" but omits `tasks.md` itself and `baseline-failed.txt` — both are mandated writes (DoD-1 flips the whole table; the baseline slot writes `baseline-failed.txt` per the spine's E2 row), so the containment claim "变更路径差集 = ∅" is false by construction over its own window |
| P2 | `.specify/specs/108-team-view-degradation/data-model.md` | 53 | — | A3: C5 declares a `tie_break` field "Declared so the rule is visible in the record" and C6 declares `exit` / `active_reasons` (lines 53, 64); the program envelope carries none of them (measured live: `team.latest` keys = nested_runs/outcome/path/readable/report/result_summary/target_assignment/verification; `errors[]` entries carry code/message/path only) — the facts live at `persistence.reports.latest_token` / `.uncertain` and in the process exit code, and no pinning test covers C5/C6 field completeness |
| P2 | `.specify/specs/108-team-view-degradation/test-evidence/targeted-set.txt` | 29 | — | A4: the note says "149 passed …（72 new/US2+US1 unit nodes included: 6 unit …" — its own enumeration (6 unit + 18 contract + 19 integration) sums to 43 new nodes, not 72; the sibling slip is `notes/us2-green.txt:22` ("the 7 US1 integration nodes … plus the 10 US2 nodes" against its own 17-node total = 6 + 11). Both are reconciled only in `test-evidence/implement-integration.md` residual 5; the measured totals are consistent everywhere |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `54c6efa8c` | resolved diff base (feature-first-commit) |
| Head commit | `4262522f4` | run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py tests/integration/test_team_view_degradation.py -q` | recorded verbatim in `verification.md`; **re-executed by this review** (`test-evidence/review-smoke.txt`) |
| Smoke exit code | 0 | 37 passed in 6.88s (review re-run) |
| Smoke evidence path | `.specify/specs/108-team-view-degradation/test-evidence/review-smoke.txt` (record-time path `notes/us3-green.txt` exists, non-empty) | exists, non-empty |
| Scope and regression verdict | scope: the implement window `005437f72..HEAD` touches the 8 declared delivery files, the spec-dir evidence subtrees and the declared record stores; beyond the declared surface it adds `tasks.md` (task-table closure) and `baseline-failed.txt` (baseline slot) — both disclosed below; `pyproject.toml`, `goal-utils.py`, the report-naming owner and `team.md` schema are unchanged (0 diff rows). Regression: one targeted run at review — 149 passed, 0 failed, rc 0; `comm -13` against the 221-name implement-entry baseline → **0 new failure names**; smoke pair 37 passed. The 221 baseline failures carry all five known worktree-environment deltas enumerated for line 107 plus pre-existing repository debt; none is attributable to this feature | — |
| Segment verdict | `pass` | — |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | `.specify/specs/108-team-view-degradation/test-evidence/implement-integration.md` | 135 | — | I1: the integration record states "the closing commit therefore adds exactly one path outside the literal surface: `.specify/specs/108-team-view-degradation/tasks.md`", but the implement window also adds `.specify/specs/108-team-view-degradation/baseline-failed.txt`, which DoD-2's surface does not name — the count "exactly one" is inaccurate (the third path, `.specify/features.md`, is covered by DoD-2's explicit driver carve-out) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` (at check time) | registry row 108, read by the checker via `--feature-registry .specify/features.md` |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/108-team-view-degradation --repo . --feature-registry .specify/features.md --json`, verdict `accept`, exit 0; never recomputed here |
| Comparison verdict | `agree` | — |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — The stage-completion sentinel is decoupled from artifact state

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/team-view-degradation.md` (line-run state spine, runtime store outside the version face)
- **Evidence** (verbatim quote):

  ```
  ## U4 — requirements attempt 1: INCOMPLETE (false-completion candidate)
  - sentinel `REQUIREMENTS-DONE` present, but: spec dir uncommitted; no `test-evidence/workspace-requirements.json`; no stage Wrap-up records for 108.
  ```

- **Why it's a problem**: the requirements stage reported completion while none of its durable evidence existed; only the driver's U4 cross-check caught it, at the cost of a full repair attempt. The same class recurred in line 107's implement stage (registry flipped without the closure carrier).
- **Proposed fix**: make completion a predicate over three machine facts — stage artifacts tracked in git, a workspace signature whose before-side is non-null, and the stage's wrap-up records present — evaluated by the stage runner before the sentinel is emitted; a failing predicate returns a named incomplete status instead of a sentinel.

### F2 — The analyze gate needed three repair rounds for classes the generation gates can machine-check

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-2026-11-26.md:3` (also `analyze-repair2-…md`, `analyze-repair3-…md`)
- **Evidence** (verbatim quote):

  ```
  - **Trigger**: analyze gate, round 1 — **2 validator-confirmed HIGH findings** (W1-01, W2-01)
  ```

- **Why it's a problem**: five HIGH findings across R1–R3 were all generation-time classes: (a) the healthy predicate copied three times with no declared owner (W1-01); (b) the predicate omitted dimensions the feature changes, so the empty-delta claim was unscoped (W2-01); (c) a closed five-form enumeration contradicted its own prose decomposition (R2-W1-01); (d) a void containment claim with no baseline/comparison unit (R3-W3-06). Each cost a repair seat plus a `PLAN-EDIT` bookkeeping pass, while `pre-analyze-check.py` reported `errors=0` (`advisories=48` for plan).
- **Proposed fix**: add three checks to the generation gates — (1) requirements validation that greps condition tokens of any "healthy/golden" predicate and requires exactly one owner plus pointer sites; (2) a containment-claim decidability check (baseline referent + comparison unit + allowed-delta set + complement assertion) over DoD/SC sentences carrying containment verbs; (3) a cross-product expansion check for "A or B × C" prose next to an enumerated set.

### F3 — The territory-vs-task-list contradiction recurred for the third consecutive feature

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-2026-11-26.md` § R2-108-W3-01
- **Evidence** (verbatim quote):

  ```
  R2-108-W3-01 — tasks required producing `verification.md` while both territory contracts forbid it to every crew seat
  ```

  and the recorded recurrence (`.specify/feedback/20261126T092426Z-skill-analyze-artifacts.md`):

  ```
  had already been repaired once in 106 and 107; 108's tasks were generated after those repairs yet reintroduced the crew-writable verification.md sink
  ```

- **Why it's a problem**: the data needed to reject the contradiction (handoff.md / team.md forbidden-path sets) exists at task-generation time, yet the same defect survived 106 → 107 → 108 repairs and cost an analyze repair round again.
- **Proposed fix**: have `validate-tasks.py` load the team's forbidden-path set from `handoff.md`/`team.md` and reject any task row whose write target or deliverable names a forbidden path; add a red fixture proving the rejection.

### F4 — A workspace signature with a null "before" side yields a vacuous clean reading

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/workspace-plan.json` (and `workspace-plan-postcommit.json`)
- **Evidence** (verbatim quote, produced by this review):

  ```
  DRIFT: branch, refs, specs
    branch before=None now='108-team-view-degradation'
  ```

- **Why it's a problem**: `workspace-guard.py --check` on the plan-stage signature reports `before=None` for every field and exits 1 — the before side was never stored — yet the stage recorded a clean workspace reading. The driver had to replace the reading with a post-stage snapshot, so the before/after comparison is unavailable for that stage.
- **Proposed fix**: `workspace-guard.py --snapshot` should refuse to write a signature whose `stored` side is empty, and `--check` should reject a self-referential comparison (a file compared against itself) as an input error; the stage dispatch should take the before-snapshot as a precondition before the first model call.

### F5 — The line registry refuses a worktree path inside the repository root

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/team-view-degradation.md` § U0 (runtime store)
- **Evidence** (verbatim quote):

  ```
  registry note: registered active without `--write-line` fields because the registry refuses a worktree path inside `repo_root` (the known limitation; same as line 107)
  ```

- **Why it's a problem**: every worktree-based line loses its write-line fields and must re-discover the limitation; the sanctioned worktree root is a first-class execution topology, not an arbitrary in-repo path.
- **Proposed fix**: exempt the sanctioned `.specify/.tmp/sdd-loop/worktrees/` prefix from `line-registry.py`'s outside-repo rule (or move the sanctioned root outside the repository and update dispatch recipes in the same change), with a contract test asserting the sanctioned path accepted and a random in-repo path rejected.

### F6 — The handoff writeback obligation is unverified at package close

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/implement-integration.md:141`
- **Evidence** (verbatim quote):

  ```
  3. **Writeback ledger gap (T019–T029).** `writeback/` holds T001–T018 (18 files) but no
     T019–T029 records, while handoff.md § Writeback prescribes one record per completed task.
  ```

- **Why it's a problem**: 11 of 29 required writeback records were missing and surfaced only at integration; the integrator correctly refused to backfill (it would invent run ids), so the handoff contract's ledger is permanently short for this stage.
- **Proposed fix**: add a per-task-id presence check to the package close (or stage U4) that compares `tasks.md`'s closed ids against `writeback/<T>.yaml` and fails the package that owed the records.

### F7 — Analyze dispatch construction drifted from the worker contract twice

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/analyze-final-report-r4-2026-11-26.md:4`
- **Evidence** (verbatim quote):

  ```
  - Dispatch disclosures: round-1 worker sentinels were `WP-Wn-DONE` while the runner expected `WP-108-Wn-DONE` (driver literal mismatch; findings complete, recorded); the R3-108-W3-06 validator payload had mismatched locations (driver construction defect; validator confirmed against tasks.md:18).
  ```

- **Why it's a problem**: both defects sit in the driver's prompt construction — a sentinel literal that does not match the worker's produced token, and a validator payload whose quoted locations drift from the analyzer's record — so the gate's evidence chain needed a manual re-read to stay trustworthy.
- **Proposed fix**: derive the sentinel literal from the same declaration the worker template reads, and copy the findings' evidence arrays verbatim from the analyzer's JSONL instead of retyping paths and line numbers.

### F8 — A stage brief carried a stale artifact-count premise

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/feedback/20261126T085303Z-speckit-checklist.md:22`
- **Evidence** (verbatim quote):

  ```
  - process: the checklist-stage brief's inventory premise said "plan + 3 contracts" while the artifact set carries 4 contracts (view-labels.contract.md landed during the plan stage).
  ```

- **Why it's a problem**: brief premises are supposed to be machine-derived from the artifacts at dispatch time; a hand-typed count silently contradicts the artifact set and forces the stage to adjudicate a non-issue.
- **Proposed fix**: generate the brief's inventory counts (contracts / FR / SC / task rows) by a script at dispatch time and embed the script's output, never a literal.

### A1 — Quickstart S-7 names a pinning test that does not exist

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `.specify/specs/108-team-view-degradation/quickstart.md:137`
- **Evidence** (verbatim quote):

  ```
  Pinned by `tests/contract/test_team_view_degradation_contract.py` (tests `test_single_recognition_entry_source_scan`, `test_reason_set_is_closed`, `test_exit_mapping_two_of_two`, `test_label_constants_match_the_owner_table`, `test_three_surfaces_cite_the_owner`) — SC-005, SC-006.
  ```

- **Why it's a problem**: `test_label_constants_match_the_owner_table` occurs zero times in that file (and anywhere in `tests/`); the executed node is `test_label_closure_both_directions`. A traceability link whose far end has no target is exactly the Segment A link finding the method names.
- **Proposed fix**: have the tasks stage reconcile plan-owned route-b test names against the pinned node ids (or make create-plan emit route-b placeholders the tasks stage replaces with a dated pointer), so a plan-time name can never survive as a dead link.

### A2 — DoD-2's declared change surface omits the paths the same task file mandates writing

- **Severity**: P2
- **Category**: Template
- **Location**: `.specify/specs/108-team-view-degradation/tasks.md:18`
- **Evidence** (verbatim quote):

  ```
  声明变更面 = 上述 8 个交付文件 + `.specify/specs/108-team-view-degradation/{notes,test-evidence,writeback}/**`（handoff 写区）+ 同目录 `checkpoints/**` 与 `coverage-baseline.txt`（阶段机与证据的日期化记录）+ `handoff.md` § Territory 授予的记录类存储组
  ```

- **Why it's a problem**: `tasks.md` itself (DoD-1 / GATE-8 flip the whole table) and `baseline-failed.txt` (written by the baseline slot at the spec-dir root) are not in the enumerated surface, so the containment claim "变更路径差集 = ∅" cannot hold over the implement window. The integration record had to adjudicate the breach by disclosure (residual 2) and undercounted it by one.
- **Proposed fix**: in the tasks DoD generator, derive the declared change surface from the stage contract's own obligated writes (task table, baseline names file, evidence sink, checkpoints) rather than enumerating it by hand, and add a self-check that every path the DoD/GATE text mandates writing is inside the declared surface.

### A3 — data-model C5/C6 declare record fields the program envelope does not materialize

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/108-team-view-degradation/data-model.md:53`
- **Evidence** (verbatim quote):

  ```
  | `tie_break` | literal `name-ascending` | Declared so the rule is visible in the record |
  ```

- **Why it is a problem**: the Latest Selection Record (C5) declares `token` / `tie_break` / `uncertain` and the Degradation Reason record (C6) declares `exit` / `active_reasons`; a live `--json` run shows `team.latest` carries none of them, and `errors[]` entries carry only `code` / `message` / `path`. The facts exist elsewhere (`persistence.reports.latest_token` / `.uncertain`, the process exit code), so no behaviour is missing — but no test pins C5/C6's field set, and a reader of the data model is told a record shape that does not exist.
- **Proposed fix**: either materialize the declared fields (nested additions are allowed by C-105) or demote the unemitted fields to prose with a pointer to their emitting site, and add a contract assertion that the C5/C6 field sets match the envelope.

### A4 — Dated evidence notes assert node counts that contradict their own enumerations

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/targeted-set.txt:29`
- **Evidence** (verbatim quote):

  ```
  - counts: **149 passed, 0 failed, 0 skipped** (72 new/US2+US1 unit nodes included: 6 unit
  ```

  and `notes/us2-green.txt:22`:

  ```
  The 17 nodes are the 7 US1 integration nodes (unchanged, still green) plus the 10 US2 nodes
  ```

- **Why it's a problem**: the first note's own enumeration (6 + 18 + 19) is 43 new nodes, not 72; the second's 17-node total is 6 + 11, not 7 + 10. The measured totals are right everywhere; only the narrative counts drifted, and they were reconciled by hand in the integration record (residual 5). Narrative counts are exactly the class a program can copy.
- **Proposed fix**: have the evidence-note template carry a machine-filled counts block (node count from `--collect-only`, task-id coverage from the task table) and forbid hand-typed totals in favor of pointing at that block.

### I1 — The integration record's containment statement undercounts the paths outside the declared surface

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/108-team-view-degradation/test-evidence/implement-integration.md:135`
- **Evidence** (verbatim quote):

  ```
     closing commit therefore adds exactly one path outside the literal surface:
  ```

- **Why it's a problem**: over the implement window `005437f72..HEAD`, `baseline-failed.txt` is a second path outside DoD-2's literal surface (written by the baseline slot, not by the closing commit). The record's "exactly one" is inaccurate, and a reader trusting it would conclude the containment claim holds after the single disclosed exception.
- **Proposed fix**: compute the changed-path complement mechanically at integration time (the DoD-2 command already exists) and paste the computed list into the record instead of a hand-typed count.

## 4. What Worked — Preserve (Brief)

- The implement stage's containment claim (after the R3 repair) has a baseline referent, per-class comparison units, an empty allowed-delta set and a complement assertion — the shape the closed-set-claims guideline asks for, and every reading was actually taken.
- Healthy byte-fidelity is proven by running the materialized baseline program (`git show 54c6efa8c:…`) beside the amended one on both goal variants, instead of trusting a hash or a claim — the strongest evidence form this repository has for "unchanged output".
- The red-first record is real: per-slot commands, discriminating failure output (AttributeError / named missing state) and exit status, captured before the subject landed; the two regression guards carry their migration/regression exception declaration in the task row.
- One classifier, one compiled grammar, one normalized token; the contract test pins the call-site set (`build_persistence`, `build_overview_row`) rather than only counting definitions.
- The review's smoke and targeted re-runs reproduced the record-time readings exactly (37 and 149 passed, 0 new failures), so the committed evidence is independently re-checkable.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC_T1 — Derive the declared change surface instead of enumerating it** — Target: `skills/internal/create-tasks/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/team-view-degradation/skills/internal/create-tasks/SKILL.md`). Change: generate DoD-2's declared change surface from the stage contract's obligated writes (task table, baseline names file, evidence sinks, checkpoints) and add a self-check that every path mandated elsewhere in the file is inside the surface. Source: A2, I1. Expected impact: containment claims stop being falsified by their own artifact; no adjudication round per feature.

### 5.2 Command Prompt Improvements

- **REC_C1 — Reconcile plan-owned route-b test names at the tasks stage** — Target: `skills/internal/create-plan/SKILL.md` (absolute supplement: `…/skills/internal/create-plan/SKILL.md`). Change: emit route-b entries with placeholder node ids that the tasks stage replaces by a dated pointer to the pinned Clause Coverage table, or have the tasks stage rewrite the quickstart's test-name list. Source: A1. Expected impact: no dead traceability links from plan to executed nodes.
- **REC_C2 — Copy dispatch payloads verbatim and derive sentinel literals** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` (absolute supplement: `…/skills/external/sdd-loop-driver/references/stage-prompts.md`). Change: build the analyze dispatch's evidence arrays by copying the analyzer's JSONL fields, and read the sentinel literal from the same declaration the worker template reads. Source: F7. Expected impact: the analyze gate's evidence chain stops needing a manual re-read to be trustworthy.

### 5.3 Automation / Script Improvements

- **REC_A1 — Completion predicate before the sentinel** — Target: `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (absolute supplement: `…/skills/external/sdd-loop-driver/scripts/stage-runner.sh`). Change: gate the sentinel on artifacts tracked, a non-null before-side signature and wrap-up records present; emit a named incomplete status otherwise. Source: F1. Expected impact: false-completion candidates are caught at the emitting seat, not at U4.
- **REC_A2 — Refuse an empty or self-referential workspace signature** — Target: `scripts/python/workspace-guard.py` (absolute supplement: `…/scripts/python/workspace-guard.py`). Change: `--snapshot` refuses to write an empty `stored` side; `--check` rejects a signature compared against itself as an input error. Source: F4. Expected impact: a vacuous "clean" reading becomes mechanically impossible.
- **REC_A3 — Per-task writeback presence at package close** — Target: `skills/internal/implement-feature/SKILL.md` (absolute supplement: `…/skills/internal/implement-feature/SKILL.md`). Change: compare closed task ids against `writeback/<T>.yaml` at package close and fail the owning package on a gap. Source: F6. Expected impact: the handoff ledger stays complete without inventing records later.
- **REC_A4 — Accept the sanctioned worktree prefix in the line registry** — Target: `skills/external/sdd-loop-driver/scripts/line-registry.py` (absolute supplement: `…/skills/external/sdd-loop-driver/scripts/line-registry.py`). Change: exempt `.specify/.tmp/sdd-loop/worktrees/` from the outside-repo rule, with an acceptance test for the sanctioned path and a rejection test for a random in-repo path. Source: F5. Expected impact: worktree lines keep their write-line fields.

### 5.4 Workflow Improvements

- **REC_W1 — Generation-time checks for duplicate owners, containment decidability and territory contradictions** — Target: `scripts/python/pre-analyze-check.py` plus the requirements/tasks validators (absolute supplement: `…/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: add the three checks named in F2/F3 — predicate-owner dedup, containment-claim decidability (closed-set five elements), and forbidden-path rejection against the handoff/team sets. Source: F2, F3. Expected impact: the analyze repair loop shrinks to genuinely semantic findings.
- **REC_W2 — Mechanical counts in integration and evidence records** — Target: `skills/internal/implement-feature/SKILL.md` § integration record (absolute supplement: `…/skills/internal/implement-feature/SKILL.md`). Change: paste computed counts (changed-path complement, node counts, task-id coverage) into the records from the programs that already produce them; forbid hand-typed totals. Source: A4, I1, F8. Expected impact: narrative-count drift disappears as a class.

### 5.5 Documentation Improvements

- **REC_D1 — Declare only materialized record fields** — Target: `skills/internal/create-plan/SKILL.md` § Phase 1 data-model (absolute supplement: `…/skills/internal/create-plan/SKILL.md`). Change: require every data-model record field to name its emitting site (or be marked as internal), and add an assertion tying the field set to the envelope where one exists. Source: A3. Expected impact: design models stop describing record shapes the program never emits.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Completion predicate before the sentinel | `skills/external/sdd-loop-driver/scripts/stage-runner.sh` | F1 |
| P1 | Generation-time duplicate-owner / containment / territory checks | `scripts/python/pre-analyze-check.py` + validators | F2, F3 |
| P1 | Derive the declared change surface and integration counts | `skills/internal/create-tasks/SKILL.md`, `skills/internal/implement-feature/SKILL.md` | A2, I1, A4 |
| P1 | Verbatim dispatch payloads and derived sentinel literals | `skills/external/sdd-loop-driver/references/stage-prompts.md` | F7 |
| P2 | Non-vacuous workspace signatures | `scripts/python/workspace-guard.py` | F4 |
| P2 | Worktree-prefix acceptance in the line registry | `skills/external/sdd-loop-driver/scripts/line-registry.py` | F5 |
| P2 | Writeback presence at package close | `skills/internal/implement-feature/SKILL.md` | F6 |
| P2 | Route-b test-name reconciliation; materialized-only data-model fields; machine-counted brief premises | `skills/internal/create-plan/SKILL.md`, `skills/internal/create-tasks/SKILL.md` | A1, A3, F8 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason (none in this report — the only external citation is the runtime state spine, cited as evidence, not as a recommendation target).
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.