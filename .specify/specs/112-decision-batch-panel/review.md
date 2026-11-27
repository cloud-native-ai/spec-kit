# Specification-Driven Development (SDD) Process Review Report: Batch Decision Panel（批量决策面板）— 112-decision-batch-panel — review round 2

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap or a review finding, it does not belong here.
>
> **This is round 2 of the review of Feature 112.** Round 1's report is archived at `review-r1.md` in this
> directory and its code-segment record at `code-review-r1.md` (rotation per
> `shared/workflow/acceptance-hardening.md` § Review Composition § Records and rotation; the slice id here is
> the review round, as in the 084/095 precedent). Round 2's delta is the repair commit `e319f265b`; round 2's
> first duty is to close or retain every round-1 item, and its verdicts below supersede round 1's where they
> differ.

## Segment Verdicts (one composed run, fixed order)

| Order | Segment | Verdict | Findings (own vocabulary) |
|-------|---------|---------|---------------------------|
| 1 | process | **pass** | 0 P0 · 4 P1 · 0 P2 — all carried from round 1, none repaired by this delta (framework targets) |
| 2 | artifact | **pass** | 0 P0 · 2 P1 · 3 P2 open; 1 P2 closed at the flip (F7) |
| 3 | implementation | **pass** | 0 P0 · 0 P1 · 2 P2 (F11/F12 closed by the repair; F13/F14 carried) |
| 4 | code | **not-evaluated** (non-conclusion, 0 coverage gap: receipt 349 changed / 19 judged / 330 declared legal skips / 0 gap; 0 blocking; gate `allow`) | 0 blocking · 1 important · 2 suggestions · 0 questions · 1 praise |
| — | Acceptance Reality Check | **agree** (`final_path` pass 7 / total 7; four completion conditions true; claimed status `Implemented`) | — |
| — | Status transition (the one gate this run judges) | **performed** — Feature 112 `Implemented → Ready for Review` on both carriers | four conjunctive conditions met (§ 2.5) |

No blocking finding remains on the current code-segment record. The code segment's `not-evaluated` is a
**non-conclusion with full coverage** — 330 files carry declared legal skips, and skips earn no coverage
credit by design (C-37); it is not a coverage gap and it does not block the transition.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 112 |
| Requirement Key | 112-decision-batch-panel |
| Requirement Name | Batch Decision Panel（批量决策面板） |
| Related Feature | 112 Batch Decision Panel（批量决策面板） |
| Repository | spec-kit (`specify-cli`, framework version answered by the engine's `--version`) |
| Repository URL | `(no single resolvable URL for this commit)` — four remotes exist: `gitee` git@gitee.com:cloud-native-ai/spec-kit.git, `github` git@github.com:cloud-native-ai/spec-kit.git, `gitlab` git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git, and `origin` **which is the UPSTREAM** git@github.com:github/spec-kit.git |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the commit is unpushed. Every citation below is repo-relative plus this worktree's absolute path; recover any file with `git show e319f265b:<repo-relative-path>` |
| Branch | 112-decision-batch-panel (git worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`; the main tree stays on master) |
| Commit SHA | e319f265bd61ad8c97c6fd2d6a4059b6a310946f (short: `e319f265b`) — round-2 `HEAD`, fixed for the run |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (fresh-context subagent; the four segments and ARC executed in one consolidation pass — no segment was produced by the implement executor or by the repair author) |
| Round-1 records | `review-r1.md` (this directory) and `code-review-r1.md` — written at head `838e7acb4`, gate `blocking-unresolved`, 2 blocking |
| Concurrency reading | requested=1 · effective=not_evaluated · effective_reason=single-unit (one consolidation pass by one reviewer; no independent units to partition) |
| Environment | Linux x86_64; bash 4.4.20; Python 3.11.11; git 2.43.5; tests through `scripts/bash/run-tests.sh`; the pytest-capable interpreter is `/usr/local/bin/python3` (the bare `python3` on PATH is a profile venv without pytest) |
| spec-kit Source Snapshot | this repository itself @ `e319f265b` (dogfooding: framework sources and the client runtime live in one tree) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 438 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-batch-panel/.specify/specs/112-decision-batch-panel/requirements.md | 45 FR / 10 SC, A-1…A-27, RS-001…RS-008, 16 clarification Q rows |
| plan.md | 178 | …/112-decision-batch-panel/plan.md | 23-row Constitution Check, 7 execution premises, PA1–PA6 |
| tasks.md | 432 | …/112-decision-batch-panel/tasks.md | 58 rows T001–T058, tests mode ON, 54 clause green claims, 8 gates |
| data-model.md | 265 | …/112-decision-batch-panel/data-model.md | 13 entities, 22 invariants, 5 state domains |
| research.md | 61 | …/112-decision-batch-panel/research.md | 14 measured baselines, 12 resolved design points |
| quickstart.md | 123 | …/112-decision-batch-panel/quickstart.md | 7 pinned scenarios |
| feature-ref.md | 110 | …/112-decision-batch-panel/feature-ref.md | FR-001…FR-045 delivery map |
| contracts/ (6 files) | 222 | …/112-decision-batch-panel/contracts/ | 54 clauses C-101…C-608 |
| checklists/ (2 files) | 150 | …/112-decision-batch-panel/checklists/ | validation record + 40-item instrument |
| verification.md | 97 | …/112-decision-batch-panel/verification.md | 10 SC rows (all pass) + 3 in-scope RS joint-acceptance rows (round-1 F5/F6/F8 still apply) |
| checkpoints/ (7 files) | — | …/112-decision-batch-panel/checkpoints/ | Checkpoint 01 requirements … 07 implement |
| feature registry row + detail | — | `.specify/features.md` row 112; `.specify/features/112-decision-batch-panel.md` | Status `Ready for Review` after this round's flip (was `Implemented` at intake) |
| review-r1.md / code-review-r1.md | — | …/112-decision-batch-panel/ | Round-1 records (archived by this run) |
| review.md / code-review.md | — | …/112-decision-batch-panel/ | This report and the round-2 code record |
| test-evidence/ (round-1 repair + round-2) | — | …/112-decision-batch-panel/test-evidence/ | Round-2 evidence: `review-round2-{rendering,c204-red,contract-green,smoke,mirror-parity,probes}.txt`; repair evidence: `review-repair-*` |

## 1. Process Execution Timeline

Round-1's timeline (requirements → plan → tasks → checklist → analyze ×2 + repair → implement P1–P4 →
close-out) is recorded at `review-r1.md` § 1 and is not repeated here. Round-2's events:

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| R2-1 | Review round 1: four segments + ARC; code gate refused (`blocking-unresolved`, 2 blocking — the C-204 identifier leaks at `decision-batch.py:806` and `:928` plus the blind guard) | `review-r1.md`; `code-review-r1.md`; commits `9536c0718`, `fbc998496` | no — the gate worked as designed |
| R2-2 | Review-repair: display maps `SOURCE_TEXT` / `PRESENCE_TEXT` / `FIELD_TEXT` in the engine (payload unchanged); the C-204 guard widened with reverse samples and four fixture bodies; mirror re-synced; two in-passing corrections disclosed (pointer-span masking in the guard; evidence capture moved outside the snapshotted spec tree) | commit `e319f265b`; `test-evidence/review-repair-2026-11-27.md` | pre-verdict repair by the implementing side — the normal round-1→round-2 iteration; both corrections disclosed, both re-verified by this review |
| R2-3 | Review round 2 (this run): records archived (`review-r1.md`, `code-review-r1.md`); fresh code record over the repaired range; independent red/green/smoke re-runs; ARC re-read; four transition conditions judged; flip performed | this report; `code-review.md`; `test-evidence/review-round2-*` | no |
| R2-4 | One process-level carry was found and disclosed, not repaired (registry frozen by the round's brief): round-1's `REC-…` ids remain unregistered in `.specify/register.md` | § 5 below | **yes — ownership obligation suspended by constraint** (disclosed) |

## 2. Findings Summary

| Status | P0 | P1 | P2 |
|--------|----|----|----|
| Open (carried from round 1) | 0 | 6 | 5 |
| Closed by this round | 0 | 2 | 1 |
| New in this round | 0 | 0 | 0 |

| Category (open items) | Count |
|------------------------|------:|
| Workflow / Automation (process F1–F4) | 4 P1 |
| Template / Documentation (artifact F5, F6, F8, F9, F10) | 2 P1 + 3 P2 |
| Scripts (implementation F13, F14) | 2 P2 |

The code segment's own six-level items (1 important, 2 suggestions, 1 praise) are recorded only in
`code-review.md` and are not converted into this table (the two vocabularies are never merged).

| Round-1 ID | Severity | Subject | Round-2 disposition |
|------------|----------|---------|---------------------|
| F1 | P1 process | test-entry interpreter ladder misses the host interpreter | open — carried (REC-A1); runner unchanged |
| F2 | P1 process | analyze gate verdict contradicts its report | open — carried (REC-W1) |
| F3 | P1 process | implement verification output redefined and derived post-hoc | open — carried (REC-C1, REC-W3) |
| F4 | P1 process | manual requirements scaffold (third occurrence) | open — carried (REC-W2) |
| F5 | P1 artifact | recorded smoke command is not the executed one | open — carried (REC-T1); `verification.md:19` still lacks the `env SPECKIT_PYTHON=…` form (probe § P4) |
| F6 | P1 artifact | `verification.md` wrong baseline, missing end-commit/checker/evidence-binding rows | open — carried (REC-T1); `baseline_commit=8d5aafb37`, no `post_change_commit`, 0 binding rows (probe § P4) |
| F7 | P2 artifact | feature detail's Status Tracking / Latest Review stale | **closed** — updated with this round's flip (Status Tracking moved to `Ready for Review`; Latest Review gains tasks/checklist/analyze/implement/review r1/review r2 entries) |
| F8 | P2 artifact | RS joint-acceptance rows carry prose, not the closed verdict token | open — carried (REC-T2) |
| F9 | P2 artifact | clarification-row count 13 vs 16 | open — carried (REC-D2); probe § P1: 16 rows, three headers still say 13 |
| F10 | P2 artifact | final-path set stated three ways (SC-010 `supporting` vs `final`) | open — carried (REC-D2); probe § P2 |
| F11 | P1 implementation | user-facing body prints roster source ids, presence token and field names | **closed** — plain-language display maps; probe § P5 = 0 hits; renderings on four fixtures plain (`review-round2-rendering.txt`) |
| F12 | P1 implementation | C-204 guard blind to both leak loci | **closed** — widened token set + reverse samples + four-fixture scan; red `1 failed` on the baseline engine, green `10 passed` on the repaired tree (`review-round2-c204-red.txt`, `review-round2-contract-green.txt`) |
| F13 | P2 implementation | option-level missing elements not named | open — carried (REC-A5); engine unchanged at the option-defect path |
| F14 | P2 implementation | path containment (`..`) not enforced | open — carried (REC-A4); probe § P3 reproduces; this is the same defect as the code record's current important entry |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c3489e52c` | the resolved diff base (`git-delta-review.sh base`) |
| Head commit | `e319f265b` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the code segment's `base` route |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 349 / 19 / 330 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `not-evaluated` | a non-conclusion with 0 coverage gap: declared legal skips earn no coverage credit (C-37); the code-path set is fully judged |
| Gate verdict | `allow` | `report --summary --file` exits 0; 0 blocking entries |
| Findings | 0 blocking · 1 important (answered in its note) · 2 suggestions · 0 questions · 1 praise | `code-review.md` § Review 意见 |
| Uncommitted scope | this run's own records only (the two archives and six round-2 evidence files at reading time); no product file uncommitted | disclosed in the record's blockquote above the receipt |
| Record | `.specify/specs/112-decision-batch-panel/code-review.md` | written (triage `run`) |
| Archive | `.specify/specs/112-decision-batch-panel/code-review-r1.md` | this run's rotation |
| Capture | skipped — `hat=framework` (root owns framework source directories) | `capture` step output |

**Round-2 code findings (full text in the record):** the open important is the path-containment defect
(`explicit_repo_path` / `resolve_pointer` accept `..`; a register authority cell can point a block outside
the workspace and `record` can append a resolution line there) — answered: agreed, not in the repair scope,
follow-up fix with a reverse sample; it does not block. The two suggestions are the register
read-modify-write without locking (carried from round 1, answered) and a new precision note on the widened
guard (bare ASCII tokens `read` / `absent` / `unreadable` matched by substring would false-red on an English
word embedding one; no current fixture trips it; anchor with word boundaries).

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, data-model.md, research.md, quickstart.md, feature-ref.md, contracts/ (6), checklists/ (2), verification.md, checkpoints/ (7), `.specify/features.md` row 112 + `.specify/features/112-decision-batch-panel.md` | derived from the stage rules and `plan.md` § Project Structure |
| Coverage line | 12 / 12 | all expected members present |
| Missing members | none | — |
| Segment verdict | `pass` | no P0 |

The repair delta touched no artifact content (only code, a contract test, evidence and records), so the
round-1 artifact findings persist unchanged; F7 closed because this round's flip updated the feature detail
(F7's proposed fix). F5/F6/F8/F9/F10 have their own quoted evidence in `review-r1.md` § 2.2 and are
re-verified live in `review-round2-probes.txt` (§ P1, § P2, § P4).

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c3489e52c` | the resolved diff base |
| Head commit | `e319f265b` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the code skill's `base` route |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py tests/contract/test_decision_governance_guards.py tests/contract/test_migration_distribution.py tests/contract/test_probe_nonentity_catalog.py tests/unit/test_validate_decisions.py -q` | recorded verbatim; this review's own re-run |
| Smoke exit code | 0 — `108 passed in 8.51s` | this review's re-run |
| Smoke evidence path | `.specify/specs/112-decision-batch-panel/test-evidence/review-round2-smoke.txt` (exists, non-empty) | written after the run (outside the snapshotted tree, then copied) |
| Scope verdict | Clean: the repair delta `838e7acb4..e319f265b` touches the engine source + mirror, the C-204 contract test and records/evidence; no unreferenced hunk; mirror byte-identical to the source (`review-round2-mirror-parity.txt`, sha256 `1025f5f1…`, `sync-mirrors --check` rc 0) | this segment's reading |
| Regression verdict | The six-file review smoke set — a superset of every touched code surface — re-ran green; the full-suite comparison (229 failed / 10412 passed vs 229 / 10404 at the pre-repair base, zero NEW failed names) is carried from round 1 and the implement record, since the repair touched only surfaces inside this smoke set | `review-round2-smoke.txt`; `implement-p4-full-suite.txt` |
| Segment verdict | `pass` | no P0, no P1 |

Round-1 P1 findings F11 and F12 are closed on this tree — see the disposition table above and the
red/green evidence.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written before the flip) | `Implemented` | `.specify/features/112-decision-batch-panel.md` and `.specify/features.md` row 112 |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/112-decision-batch-panel --repo . --feature-detail .specify/features/112-decision-batch-panel.md --feature-registry .specify/features.md --json` |
| Checker verdict and completion conditions | `accept`; `every_final_path_pass=true`, `no_open_rows=true`, `smoke_record_pass=true`, `status_row_per_criterion=true`; tasks closed 58 / deferred 0 / open 0 | same run |
| Comparison verdict | `agree` | checker `accept`; claimed status `Implemented` |
| Failed condition, on refusal | none | no refusal |

### 2.5 Status Transition Record (the one gate this run judges)

| # | Condition (owner: `templates/feature-details-template.md` § Canonical Status State Machine; cited, not restated) | Reading | Met |
|---|---------------------------------------------------------------------------------------------------------------|---------|-----|
| 1 | every deferred task resolved or explicitly waived | ARC tasks: closed 58 / in_progress 0 / deferred 0 / open 0; no waiver | yes |
| 2 | review evidence produced | `review.md` (this file) + `code-review.md` (round 2) on disk | yes |
| 3 | the current code-segment record has no `blocking` entry | `blocking_entries=0`; gate `allow` | yes |
| 4 | no `final`-path criterion in `blocked` / `deferred` / `fail` without a naming user waiver | `final_path`: pass 7 / total 7; all other buckets 0; no waiver involved | yes |

**Transition performed** at 2026-11-27 on both carriers: `.specify/features.md` row 112 and
`.specify/features/112-decision-batch-panel.md` (header `**Status**`, Status Tracking, Latest Review).
Recorded here; no push.

## 3. Carried Findings (with quoted evidence)

Full finding forms (location, quote, proposed fix) live in `review-r1.md` § 3 for F1–F14; the excerpts below
keep this report self-contained for the open set.

**F1 — the runner's interpreter ladder misses the host's pytest interpreter (P1, open).** Ladder:
`for candidate in "${SPECKIT_PYTHON:-}" "$repo_venv" ".venv/bin/python" "python3" "python"; do` — the bare
`python3` has no pytest here, and the plan stage could not run tests at all. This review still passes
`SPECKIT_PYTHON` explicitly. Fix (REC-A1): probe `command -v -a python3` and absolute interpreters.

**F2 — the analyze gate verdict contradicts its own report (P1, open).** Report:
`**The analyze gate is NOT cleared**: G-01 (baseline-missing …), G-02 (FR-043 uncovered) and I-03 … remain.`
while the driver recorded PASS on C/H = 0. Fix (REC-W1): one machine-readable `gate=` value consumed by the
driver.

**F3 — the implement stage's verification output is redefined and derived post-hoc (P1, open).** Task input:
`the P4 task rows author this verification-input.md instead of verification.md.` Fix (REC-C1/REC-W3):
make the executor populate the template file or declare a conformant derivation.

**F4 — the manual requirements scaffold recurs a third time (P1, open).** Requirement A-19:
`本阶段**手工**从 .specify/templates/requirements-template.md 脚手架到本目录`. Fix (REC-W2): the
`--feature-id/--branch` in-place mode.

**F5 — the recorded smoke command is not the executed command (P1, open).** `verification.md:19`:
`smoke_command=bash scripts/bash/run-tests.sh …` (no `env SPECKIT_PYTHON=…`); executed verbatim it exits 1
with `error: no interpreter with pytest found`. Re-verified live (probe § P4).

**F6 — `verification.md` omits template-required fields and uses the wrong baseline (P1, open).**
`baseline_commit=8d5aafb37` (the P4 package base, not the implement-run start); no `post_change_commit=`,
no checker verdict/reasons, and 0 `sample_id`/`evidence_sha256` binding rows (probe § P4). Fix (REC-T1).

**F8 — the RS joint-acceptance rows lose the closed verdict token (P2, open).** e.g.
`RS-005_joint_acceptance=verified by behaviour on the delivered tree: …` — prose instead of
`pass|fail|partial|blocked|deferred|unknown`. Fix (REC-T2).

**F9 — the clarification-row count is stale in three artifacts (P2, open).** Three headers say
`13 clarification rows`; measured `grep -c '^- Q:' requirements.md` = 16 (probe § P1). Fix (REC-D2).

**F10 — the final-path set is stated three ways (P2, open).** `tasks.md` DoD-7/GATE-4 list SC-010 as
`final` while `requirements.md:366` marks `**Path**: supporting`; the checker counts 7 (probe § P2).
Fix (REC-D2).

**F13 — option-level missing elements are not individually named (P2, open).**
`for defect in primary_block["defects"]: reasons.append(defect[0])` drops the `(line, name)` detail and
`"option-element-missing": "存在要素不全的选项"` names no option or element, while C-202 requires the named
missing elements. Fix (REC-A5).

**F14 — path containment is not enforced for register-linked carriers (P2, open; the code record's
important).** Probe: `explicit_repo_path('.specify/../../outside/doc.md') => '.specify/../../outside/doc.md'`
and `(root/rel).resolve()` lands outside the workspace; `resolve_pointer` accepts `..` too (probe § P3).
Fix (REC-A4).

## 4. What Worked — Preserve (Brief)

- The repair closed both leak loci **without touching the structured payload**, and it proved the widened
  guard can fail: red on the baseline engine (`1 failed`, exact tokens), green on the repaired tree
  (`10 passed`), plus in-test reverse samples for every leak form — the "a green check is a claim" discipline.
- The two in-passing corrections were disclosed with their rationale (pointer-span masking; evidence capture
  moved outside the snapshotted tree) instead of silently patched — this review re-verified both readings
  independently and they hold.
- Mirror projection discipline survived the repair: source and mirror are byte-identical (sha256 and
  `sync-mirrors --check`).
- Round-1's blocking findings were re-adjudicated one by one (closed / open-answered / answered), and the
  open important carries a real fix direction with a reproducing probe.
- Round 1's process gains still stand: deterministic engine with a closed action/exit-code face, create-only
  discipline with zero-write refusals, red-first evidence per test slot, mirror parity, and analyze round 1
  catching two HIGH contradictions that were repaired at the owner surface.

## 5. Round-2 Process Observations (uncounted — no new identifiers coined)

The round's brief forbids registry edits beyond the status flip, so the two observations below are disclosed
as prose rather than coined as new finding IDs.

1. **The code segment's headline reads `not-evaluated` even for a fully reviewed delta.** With
   `0` coverage gaps and `0` blocking entries, the receipt still prints `verdict=not-evaluated` whenever any
   file carries a declared legal skip (C-37: skips earn no coverage credit). Feature 109's record has the same
   shape. The two-vocabulary design is deliberate, but a downstream reader can mistake the non-conclusion for
   "not reviewed". Suggested improvement: have `receipt` also print a coverage-complete marker (e.g.
   `coverage=complete`) beside the verdict so carriers can quote both without prose.
2. **Round-1's recommendations remain unregistered.** The review Handoff requires every coined `REC-…` id to
   be registered in `.specify/register.md` in the same commit (REC-T1/T2, REC-C1, REC-A1…A5, REC-W1…W3,
   REC-D1…D2). Round 1 did not register them; this round's brief freezes the registry, so the obligation is
   carried forward, disclosed here rather than silently dropped.

## 6. spec-kit / SDD Improvement Recommendations (carried — IDs coined in round 1)

| ID | Target | Source | Round-2 status |
|----|--------|--------|----------------|
| REC-T1 | `templates/verification-log-template.md` — executable smoke/evidence fields | F5, F6 | open |
| REC-T2 | same — RS verdict token separated from its evidence sentence | F8 | open |
| REC-C1 | `templates/commands/implement.md` § Step 9 — verification hand-off in the command | F3, F6 | open |
| REC-A1 | `scripts/bash/run-tests.sh` — host pytest interpreter resolution | F1, F5 | open |
| REC-A2 | `scripts/python/decision-batch.py` — plain-language source/presence/field labels | F11 | **implemented** (`e319f265b`) |
| REC-A3 | `tests/contract/test_decision_batch_contract.py` — extend the C-204 guard | F12 | **implemented** (`e319f265b`) |
| REC-A4 | `scripts/python/decision-batch.py` — carrier containment (`..` rejection + workspace assertion) | F14 | open |
| REC-A5 | `scripts/python/decision-batch.py` — name option-level missing elements | F13 | open |
| REC-W1 | analyze skill/command — single machine-readable gate verdict | F2 | open |
| REC-W2 | `scripts/bash/create-new-requirements.sh` — in-place requirements scaffold | F4 | open |
| REC-W3 | implement/close-out stage brief — self-describing stage records | F3, F6 | open |
| REC-D1 | `.specify/features/112-decision-batch-panel.md` — update the detail at every status change | F7 | **done this round** |
| REC-D2 | plan.md / tasks.md / feature-ref.md — fix the count and final-set wording | F9, F10 | open |

## 7. Priority Roadmap (carried, next first)

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-T1 + REC-C1 + REC-W3 — reproducible smoke, evidence binding, verification hand-off | `templates/verification-log-template.md`; `templates/commands/implement.md` | F3, F5, F6 |
| P1 | REC-A1 — host pytest interpreter resolution | `scripts/bash/run-tests.sh` | F1, F5 |
| P1 | REC-W1 — single analyze gate verdict | analyze skill/command | F2 |
| P1 | REC-W2 — in-place requirements scaffold | `scripts/bash/create-new-requirements.sh` | F4 |
| P2 | REC-A4 — carrier containment | `scripts/python/decision-batch.py` | F14 |
| P2 | REC-A5 — option-level missing-element naming | `scripts/python/decision-batch.py` | F13 |
| P2 | REC-T2 — RS verdict token | `templates/verification-log-template.md` | F8 |
| P2 | REC-D2 — count and final-set corrections | plan/tasks/feature-ref | F9, F10 |

## 8. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary); no new recommendation ids were coined this round.
- [x] Every open finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file; the full forms live in `review-r1.md` § 3.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] P0 validation status is stated explicitly: no P0 findings in this round; the P0 independent-validation pass is vacuously satisfied. (The round-1 code blocking entries were found by that round's fresh-context review and are closed on this tree.)
- [x] The status transition is recorded with its four condition readings (§ 2.5) and no condition was waived.

## 9. Feedback

Please share the contents of this document with the spec-kit framework developers.