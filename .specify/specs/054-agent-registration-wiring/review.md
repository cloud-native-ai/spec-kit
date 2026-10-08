# Specification-Driven Development (SDD) Process Review Report: Agent Registration Wiring (054)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. Sections describing the feature instead of identifying a process gap were deleted at write time.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 054 |
| Requirement Key | 054-agent-registration-wiring |
| Requirement Name | Agent 定义到宿主注册面的接线 (Agent Registration Wiring) |
| Related Feature | 044 Agent Metadata Portability |
| Repository | spec-kit (distributed as `specify-cli` 0.0.22) |
| Repository URL | git@github.com:cloud-native-ai/spec-kit.git (also gitee/gitlab mirrors of the same name) — SSH-only remotes; `blob/` URLs cannot be rendered |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty (branch unpushed). Citations below use absolute paths plus `git show <sha>:<path>` recovery: e.g. `git show d58a600e:.specify/specs/054-agent-registration-wiring/verification.md` |
| Branch | 054-agent-registration-wiring |
| Commit SHA | d58a600e0fc1c07c69d2181e6c9524909986d859 (short d58a600e) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-08 |
| Reviewer (Agent) | Qoder CLI (fresh-context detection subagents + disjoint P0 validators, per objective-analysis-gate) |
| Environment | Linux 5.10.134 x86_64, Python ≥3.8, pytest (contract marker) |
| spec-kit Source Snapshot | this repository @ d58a600e (self-hosting) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|---|---|---|---|
| requirements.md | 194 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/054-agent-registration-wiring/requirements.md | 4 stories, 14 FR, 4 SC, ruling (b) recorded |
| plan.md | 142 | …/plan.md | render-agents subcommand design; Constitution 16/16 (delegated scoring) |
| tasks.md | 230 | …/tasks.md | 31 tasks, 7 phases, [green:] partition |
| data-model.md | 60 | …/data-model.md | 4 entities |
| contracts/ (4) | ~150 | …/contracts/*.md | seat-instantiation, render-trigger-cli, modify-backfill, teaching-and-guards |
| quickstart.md | 47 | …/quickstart.md | 3 scenarios, per-example disclaimers |
| verification.md | 28 | …/verification.md | SC-001..004 rows, gate_rejections=0 |
| checklists/requirements.md | 24 | …/checklists/requirements.md | 16/16, 3 validation runs |
| notes/ (3) | ~120 | …/notes/*.md | baseline, red-first evidence, quickstart run |

## 1. Timeline (process history, reconstructed from git)

`git log 5e970dce..d58a600e` — 9 commits: 09bd40a9 clarify (⚠ folded 52 foreign files, see W1) → 8c2ad699 plan → 6f7ea28c tasks → 3e673e16 P1-2 (subcommand + key, red→green 9/9) → 38c19d1e P3 US1 (teaching surfaces, guard 11/11) → b95b5818 P4 US2 (create/improve-team steps, guard 6/6) → fb3432e9 P5 US3 (docs + owner section, guard 5/5) → 77e041cb P6 US4 (aggregate guards 4/4, 3 source-side drills) → d58a600e P7 (verification, DoD green). Every implement-phase commit is path-limited and lands within plan.md's declared tree (validated by the workflow detection pass); regression `comm -13` empty at each boundary. User pre-authorized commits mid-run (「直接提交」/长跑模式); six phase commits followed without re-asking, none known-red. Evidence-strength note: phases were attributed from per-task [X] markers + commit messages (commit granularity is phase-level, not per-task).

## 2. Findings Summary

| Sev | Count | By category |
|---|---|---|
| P0 (validated) | 1 | Workflow 1 |
| P1 | 4 | Workflow 2, Automation 1, Documentation 1 |
| P2 | 8 | Workflow 4, Template 1, Command Prompt 1, Documentation 2 |

P0 validation: two detection-pass P0s went to disjoint validators — F1 **confirmed** (P0 stands), F2 **downgraded to P1** (validated: downgraded). Detection claimed SC-003 spans 4 tools; the validator's literal read corrected this to the criterion's own two-directory form (recorded in F1's caveat, not split into a new row).

## 3. Findings

### F1 — P0 (validated: confirm) — Workflow — SC-002 marked pass on evidence weaker than its own criterion

**Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/054-agent-registration-wiring/verification.md (SC-002 row) vs requirements.md:165,172
**Evidence**: SC-002 Source (requirements.md:172): 「端到端演示项目(或本仓 dogfooding 团队)的宿主 agent 目录清单 **+ 派发记录**(如 run report 的席位派发面)」. verification.md SC-002_status=pass with evidence = "test_agent_chain_guards.py test_c9 (instantiated seat definition → `specify render-agents --ai qoder` → … real file …)"; repo reality at review time: `.specify/agents/instances/` empty, `.qoder/agents/` holds only the 2 factory agents, no dispatch record exists. The note's "Dispatch of a seat by its registered type now carries … system-prompt" has zero record behind it.
**Why**: A `pass` in the programmatically-consumed acceptance record (verification.md) that the SC's own measurement source does not support is silent corruption — /speckit.review and /speckit.analyze read this row as green.
**Proposed fix**: Flip SC-002 to `partial` (render half measured; dispatch demonstration unmet) or run the dogfood demonstration (create a scratch team via the new flow, dispatch a seat, record the run report) before restoring pass. Template-side: the verification template already names this exact case ("an honest `partial` … mechanical half measured, stated measurement condition not met") — the implement command's SC-status guidance should re-quote that clause at the wrap-up step.

### F2 — P1 (validated: downgraded from P0) — Automation — evidence file presents paraphrased command lines under a "real outputs" label

**Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/054-agent-registration-wiring/notes/quickstart-run.md (grep block), cited by verification.md SC-001_note and tasks.md T029
**Evidence**: Displayed command `$ grep -rn "<STR-001 verbatim> + SKILL retired phrases" <shipped surfaces>` — angle-bracket placeholders, and one grep cannot express both classes; yet the output lines (`templates/commands/agents.md:0` …) are exactly `grep -rc` format over precisely the file list pinned in the guard test, and the validator independently re-searched: zero hits confirmed on every listed surface.
**Why**: The recorded values are true and machine-pinned elsewhere, but an evidence file labeled "executed real outputs" carrying a paraphrased command line teaches the next run that command fidelity in evidence records is negotiable.
**Proposed fix**: Re-run the actual `grep -rc` commands (two, one per literal class) and paste verbatim; never paraphrase a command line inside an evidence file.

### F3 — P1 — Workflow — clarify commit folded 52 files from a parallel session

**Location**: commit 09bd40a9 (`git show --stat` = 56 files, 4306 insertions)
**Evidence**: Spec-054 content is ~4 files (requirements.md, checklist, two registry rows); the rest is the parallel self-improvement stream's work (speckit.improve command set ×4, skills/self-improvement, critique-and-self-criticism docs, 6 feedback records, a 706-line test file, and binaries: summary/data/project.db 196KB, wbs.png).
**Why**: Permanently mislabels an entire parallel feature's history under 054; the root cause (git commit takes the whole shared index; ` M`/`??` status doesn't reveal other sessions' staged files) was surfaced by the run itself and recorded in feedback 20261008T093319Z, but the artifact-commit-step owner text still doesn't mandate the path-limited form.
**Proposed fix**: Already partially self-healed (every later commit used `git commit -m "…" -- <paths>` after the index was confirmed empty). Land the mechanism fix: artifact-commit-step.md should mandate `git commit -- <explicit paths>` (or a pre-commit `git diff --cached --name-only` ownership audit) in multi-session repos. History correction for 09bd40a9 itself is the user's call (rewrite vs annotation).

### F4 — P1 — Documentation — tasks.md still cites pre-renumber clause ids

**Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/054-agent-registration-wiring/tasks.md (T015/T016 rows)
**Evidence**: T015: "per contract C-3.1/C-3.2" → seat-instantiation's schema-note clause is **C-9**; T016: "per contract modify-backfill C-3.1 … (contract modify-backfill C-4.2)" → the report/guidance clauses are **C-4/C-8**.
**Why**: The tasks-phase renumber (recorded in tasks.md Notes) rewrote [green:] tags but left prose citations pointing at the pre-renumber scheme — the exact stale-reference class the renumber was supposed to eliminate.
**Proposed fix**: Rewrite the two citations to canonical ids; add "grep for `\w-C-\d` in tasks prose against the renumbered contracts" to the tasks-phase renumber checklist.

### F5 — P1 — Automation — five contract clauses have no [green:] claim and no guard assertion

**Location**: …/tasks.md Notes ("each clause claimed exactly once") vs contracts/modify-backfill.md C-4..C-7, contracts/seat-instantiation.md C-10
**Evidence**: improve-team step 7 DID land the C-4 three-way report distinction (直接引用/本次补实例化/渲染 stats), but test_seat_instantiation_flow.py's improve-team assertions are only `"specify render-agents" in text` + `"回填" in text` — deleting the distinction stays green. Same for C-5..C-7, C-10.
**Why**: The partition claim in the Notes is false, and the landed-but-unguarded clause is a regression window the whole guard discipline exists to close.
**Proposed fix**: Extend the improve-team guard to pin the three-way report markers and assign [green:] claims for the five orphaned clauses (or record them as deliberately unguarded with a reason).

### F6 — P2 — Documentation — teaching-surface repair was scoped to line anchors, leaving a same-class dead letter 10 lines above

**Location**: /storage/project/cloud-native-ai/spec-kit/skills/create-agent/SKILL.md:108; templates/commands/agents.md (create step area)
**Evidence**: :108 still teaches "Frontmatter uses Qoder-compatible fields — `model` … `tools`/`disallowedTools`, `maxTurns`/`timeoutMins`, `skills`/`mcpServers` …" — 8 of the 10 keys `FORBIDDEN_AGENT_METADATA_KEYS` (src/specify_cli/__init__.py:154-167) rejects; FR-002 pinned only :122/:127 and the guard pins only the symlink phrases. The authoring key list is now restated in 4 places that disagree (SKILL.md:108 vs SKILL.md:113 vs agents.md vs the code key set).
**Why**: The spec's line-anchor framing let a validator-rejected dialect survive the "teaching surfaces" sweep — the F-A02 dead-letter class, one layer deeper.
**Proposed fix**: Scope teaching repairs by claim-class (any frontmatter-vocabulary teaching must reference the code key set, not enumerate), and add a guard on the forbidden-dialect class.

### F7 — P2 — Workflow — chain-guard family never had an authoring-time red

**Location**: …/notes/red-first-evidence.md:3 vs :51
**Evidence**: Header: "Every guard: red output … at authoring time"; T025: "front-loaded closure (subjects landed in Phases 2/4; component reds captured at T004/T009/T014)". test_agent_chain_guards.py was authored after its subjects.
**Why**: The deviation is disclosed and drilled, but the file's own header overclaims; Constitution IV's red-first is satisfied at component level, not at this file level.
**Proposed fix**: Amend the header ("every guard except the disclosed T025 front-load") or add a synthetic red record (subject-revert drill).

### F8 — P2 — Workflow — baseline class attribution covers only ~7 of 49 entries

**Location**: …/notes/pre-change-measurements.md (baseline section)
**Evidence**: "The 49 are pre-existing reds (agent-skill-enablement, neutrality-budget, no-nested-skills classes)" — baseline-failed.txt actually holds 36× test_browser_site_memory, 4× test_agent_specific_config_skills, 1× browser_site_exclusions, 1× goal_migration, plus those 7.
**Why**: The "pre-existing, not ours" justification is under-evidenced for 42 entries even though the count is right.
**Proposed fix**: Correct the enumeration to match baseline-failed.txt (a `sort | uniq -c` paste is enough).

### F9 — P2 — Workflow — final full-suite regression summary never landed in verification.md

**Location**: …/verification.md (regression line) vs tasks.md T028 ("paste summary into verification.md")
**Evidence**: verification.md has `regression=comm -13 … empty at every phase boundary (Phases 2,3,4,5,6)` and no terminal `N failed / M passed` line; Phase 7 only touched `.specify/` paths so the omission is defensible, but the T028 paste obligation went unmet. Also `commits=` omits d58a600e itself.
**Proposed fix**: Append the final summary + the landing commit's own sha (post-landing amendment is a new commit, never --amend).

### F10 — P2 — Documentation — stale clause id and a dangling STR id in supporting artifacts

**Location**: …/notes/pre-change-measurements.md:15 ("the C-7 guard pins both"); …/checklists/requirements.md validation-runs header ("STR-001/STR-002 引用形态")
**Evidence**: The retired-literal pin is teaching-and-guards **C-4** after the renumber; STR-002 ("seat_kind") was removed from requirements.md's Shared Strings when ruling (b) landed — the checklist's historical row cites a now-nonexistent id without an annotation.
**Why**: Supporting artifacts citing dead ids re-teach the drift the renumber fixed; the checklist row is a dated record (legitimate duplicate class) but should annotate the removal.
**Proposed fix**: Correct the clause id in notes; annotate the checklist's historical mention ("STR-002 was removed with ruling (c) — see Clarifications").

### F11 — P2 — Template — single-green-point rule forced an awkward claim-less row and an unexplained serial chain

**Location**: …/tasks.md (T005 row; T009 [P] + [blockedBy: T005])
**Evidence**: T005: "green claims for this file live on T004 … a separate row … for review granularity"; T009 carries [P] while being blocked behind an unrelated same-file row.
**Why**: The validator's green-path-divergence check has no form for "appends to a file whose green point is another row" — the tasks template absorbed the friction silently (root cause shared with F4's renumber chain).
**Proposed fix**: Teach validate-tasks.py an append-mode marker (e.g. `[extends: T004]`) that exempts a row from carrying claims while keeping it in the writer chain; or fix the checker to accept disjoint claim sets (the remedy text it prints already names "partition the clauses" — the implementation doesn't recognize it).

### F12 — P2 — Workflow — run's own feedback ledger left uncommitted while the parallel stream's was swept

**Location**: git status — `M .specify/memory/feedback/index.json` + 4 untracked feedback records (clarify/plan/tasks/implement) post-dating the final commit
**Why**: Same-path records from the parallel session were committed (in 09bd40a9) while this run's were left in the tree — inconsistent ledger handling, and the implement record (20261008T132002Z, the one carrying the drill-blindness finding) is unpushed-orphaned.
**Proposed fix**: Commit the four records + index delta (feedback stream's own wrap-up convention owns the batching decision); consider making the implement wrap-up stage its own ledger records explicitly.

## Unvalidated Findings

None — both detection-pass P0s went through disjoint validation; P1/P2 rows skip validation per the gate.

## 4. What Worked (brief)

- **Delegated scoring held up**: fresh-context subagents (plan 16/16, review detection ×2, P0 validation ×2) produced every load-bearing verdict in this lifecycle; zero self-review green lights on scored surfaces.
- **Red-first + mutation drills with source-side plants**: 6 drills all closed (plant→red→byte-equal restore→green), including catching the suffix-append drill blindness and a substring false-positive **before** they shipped as guards.
- **Path-limited commits after the first failure**: six consecutive clean phase commits; no foreign folds after 09bd40a9; deletion-surface audit empty at every boundary.
- **Evidence files**: red-first-evidence.md carries real command outputs for four of five guard families; baseline verified byte-identical before use.

## 5. Recommendations (target files)

1. **verification honesty at wrap-up** (F1/F9): templates/commands/implement.md — at the verification-log step, require each SC row's status to be re-checked against its own Measurement Source wording before flipping DoD; re-quote the template's `partial` clause.
2. **evidence-record command fidelity** (F2/F7): shared/workflow/feedback-step.md or a new evidence-convention line in templates/commands/implement.md — evidence files quote commands verbatim, never paraphrase; a front-load deviation must be visible in the file's own header.
3. **artifact-commit path-limited form** (F3/F12): .specify/shared/workflow/artifact-commit-step.md — mandate `git commit -m "…" -- <explicit paths>` in multi-session repos (this run's own feedback entry 20261008T093319Z documents the root cause).
4. **renumber-aware tasks prose** (F4/F10): templates/commands/tasks.md renumber checklist — after any contract renumber, grep tasks.md prose for `C-\d` citations and stale STR ids against the renumbered owners.
5. **claim coverage completeness** (F5): the tasks-phase [green:] partition step should enumerate every clause and force a claim-or-reason per clause; extend the improve-team guard to pin the landed C-4 distinction.
6. **claim-class scoping for teaching repairs** (F6): requirements/plan guidance — when fixing "teaches a retired model" findings, scope by claim-class (vocabulary teaching must point at the code key set), not by line anchors; add a forbidden-dialect guard.
7. **validator remedy-text/implementation gap** (F11): scripts/python/validate-tasks.py — green-path-divergence's printed remedies (partition / blockedBy) are not recognized by its implementation; fix one side.

## 6. Priority Roadmap

| Priority | Item | Files |
|---|---|---|
| Now (before merge) | F1 SC-002 partial-or-demo; F2 verbatim evidence re-run; F4 stale clause citations | verification.md, notes/, tasks.md |
| Next (framework mechanisms) | R3 path-limited artifact-commit; R1 SC-source recheck at wrap-up; R5 clause-coverage enumeration; R7 validator fix | artifact-commit-step.md, implement.md, validate-tasks.py |
| Later (hardening) | R6 claim-class scoping; F8 baseline enumeration; F6 dialect guard | requirements-guidelines, notes, tests |

---

*Self-containment: COMMIT_SHA unpushed — all citations above use absolute paths; recover any file via `git show <sha>:<path>` from a checkout of d58a600e. Detection and validation were delegated per `.specify/shared/workflow/objective-analysis-gate.md`; propagation-surface cap P1 applied.*
