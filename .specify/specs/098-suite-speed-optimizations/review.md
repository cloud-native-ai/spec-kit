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
| Repository URL | `git remote -v` lists `gitee` / `github` / `gitlab` forks plus the upstream lineage; none holds a pushed copy of this branch (see next row) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — cite absolute paths plus `git show <sha>:<path>` recovery instead of URLs |
| Branch | `098-suite-speed-optimizations` |
| Commit SHA | `5ec91b8c7be0464db6b4ec7c7d6f0a15f3ff5a20` (short: `5ec91b8c7`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder · four-segment composition (`/speckit.review`), round 3 |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash 4/5, Python 3.11.11, pytest 8.4.2, pytest-xdist 3.8.0, git 2.43.5, nproc 192 |
| spec-kit Source Snapshot | this worktree at `5ec91b8c7` (framework source `templates/`, `shared/`, `scripts/`, `skills/` and the client runtime `.specify/` in one repository) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 266 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/requirements.md` | 27 FR / 11 SC (9 final, 2 supporting), 17 assumptions, 5 clarification Q/A |
| plan.md | 366 | `…/098-suite-speed-optimizations/plan.md` | 22-row Constitution Check, T-001…T-003, EP-001…EP-004, 9 work packages |
| tasks.md | 407 | `…/098-suite-speed-optimizations/tasks.md` | 61 rows all `[X]`, DoD-1…DoD-7 met, GATE-1…GATE-5, `deferred_tasks=` empty |
| research.md | 137 | `…/098-suite-speed-optimizations/research.md` | B-1…B-10 measured baselines, R-1…R-10 decisions |
| data-model.md | 121 | `…/098-suite-speed-optimizations/data-model.md` | Entities E-1…E-8 |
| quickstart.md | 193 | `…/098-suite-speed-optimizations/quickstart.md` | Scenarios S-0…S-13 |
| feature-ref.md | 66 | `…/098-suite-speed-optimizations/feature-ref.md` | 26-row delivery surface, disclosures, out-of-scope |
| contracts/ | 424 (6 files) | `…/098-suite-speed-optimizations/contracts/` | 68 clauses (16/9/12/11/10/10) |
| verification.md | 199 | `…/098-suite-speed-optimizations/verification.md` | SC-001…SC-011 all `pass`, one smoke triple, measured-tree fields, `deferred_tasks=` empty, copied closure verdict `accept` |
| review-098.md (round-1 archive) | 379 | `…/098-suite-speed-optimizations/review-098.md` | Round-1 report |
| review-20261110T195934Z.md (round-2 archive) | 294 | `…/098-suite-speed-optimizations/review-20261110T195934Z.md` | Round-2 report, archived by this run's rotation |
| code-review.md | 1110 | `…/098-suite-speed-optimizations/code-review.md` | Round-3 code record: receipt block (298/141/157/0), one `important`, one `suggestion`, one `praise` |
| code-review-20261110T185547Z.md (round-1 archive) | 925 | `…/098-suite-speed-optimizations/code-review-20261110T185547Z.md` | Round-1 code record |
| code-review-20261110T195724Z.md (round-2 archive) | 1030 | `…/098-suite-speed-optimizations/code-review-20261110T195724Z.md` | Round-2 code record, archived by `start` |
| checklists/ | 2 files | `…/098-suite-speed-optimizations/checklists/` | requirements-quality checklist + dated suite-speed checklist |
| checkpoints/ | 8 files | `…/098-suite-speed-optimizations/checkpoints/` | 01-requirements … 08-review (02 is still a duplicate — finding F2) |
| notes/ (three records) | 8688 / 297 / 344 | `…/098-suite-speed-optimizations/notes/` | pre-change measurements (§1 superseded slot-1 + §7 rebuilt baseline), quickstart run, red-first |
| test-evidence/ | index + records | `…/098-suite-speed-optimizations/test-evidence/` | SC → evidence mapping; round-3 smoke, ARC payload and closure records |

## 1. Process Execution Timeline

Reconstructed from the 30 commits in `b3da3a26d..5ec91b8c7` (feature-first-commit base resolved by `git-delta-review.sh base`) plus this round's working-tree evidence. Rows 1–19 are the round-2 reconstruction, re-verified; round-3 additions are rows 21–22.

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
| 12 | constitution amended 1.19.0 → 1.19.1 (Principle VII carrier) | `af73f65f1` | **Out-of-plan** in round 1; attributed by `D-098-01` (register) |
| 13 | WP-1 runner tier mechanism; WP-2 slow registry | `0d1f7a1e4`, `1dca066fb` | None |
| 14 | T012 green record + T013 tier/slow mutation drills | `719f78b90` | None (T012 wording repaired by review-repair r1) |
| 15 | WP-3 … WP-9 (docs, parallel consistency, cache, clock, in-process, measurement) | `ac91ab81a` … `2183d4986` | None |
| 16 | S-4 serial wall restated from file timestamps | `c5b2b32a7` | Measurement proxy, disclosed |
| 17 | T013 close — 13 mutation legs | `ea5962c87` | None |
| 18 | Implement stage close — **without** its Step 9 close-out (no `verification.md`, no closure record) | Round-1 evidence: `git log --all --name-only -- …/verification.md` was empty at `ea5962c87` | **Deviation**, repaired by review-repair r1 |
| 19 | Review round 1 — four segments + ARC; transition refused | `b9e5a35a2`; archived report `review-098.md` | Refusal correct for that tree; P0 5 / P1 6 / P2 4 |
| 20 | Review round 2 — four segments + ARC; transition still refused; remediation r1 verified | `c4f7c8bd1`; archived report `review-20261110T195934Z.md` | None — refusal named SC-003/SC-005 (T061 closure legs) |
| 21 | Review-repair r2 — closure slot executed; attempt 1 exposed a five-name parallel-only difference in `tests/integration/test_trigger_tuning.py`, repaired at the root with an explicit `--workspace` (the r1 SC-002 precedent), slot re-taken | `5ec91b8c7`; `test-evidence/closure.txt` §§1–5, `closure-isolation-fix.txt`, `review-repair-dispositions-r2-2026-11-11.md` | Repair disclosed with attempt-1 readings retained as diagnostics, not as any SC wall (anti-metric stated) |
| 22 | Round-3 review — evidence recomputation (10/10 `evidence_sha256` equal; `comm` 0/0, 0/64, 3/59), smoke re-run (86 passed, exit 0, 36.90 s), code receipt (298/141/157/0, 0 gap), ARC `accept` (9/9) | this run; `test-evidence/review-smoke-098-r3.txt`, `test-evidence/review-r3-arc-payload.json`, `code-review.md` | None |

### 1.1 Round-2 finding verification (1 P1 / 4 P2)

Every round-2 finding was re-measured on this round's tree; nothing below is accepted on the repair's self-report alone.

| r2 ID | Sev | Round-2 claim | Round-3 verification (evidence) | Status |
|-------|-----|---------------|---------------------------------|--------|
| F1 | P1 | baseline row scheduled last (T003 in WP-9) | `tasks.md:310` still assigns `T003` to WP-9; REC-098-01 remains `open` in the register | **carried** → this round's F1 |
| F2 | P2 | `checkpoints/02-clarify.md` byte-identical to `01-requirements.md` | `cmp` exits 0; line 1 still reads `# Checkpoint 01 — requirements（098-suite-speed-optimizations）` | **carried** → this round's F2 |
| F3 | P2 | review gate refuses on a verdict its owner defines at feature-line closure | `templates/commands/review.md:99` unchanged; the string `pending-closure` appears in neither the command template nor `acceptance-hardening.md` | **carried** → this round's F3 |
| A1 | P2 | verification readings not bound to the measured tree | `verification.md:20,29,32` now carry `baseline_measured_tree=` / `post_change_measured_tree=` / `closure_measured_tree=` | **repaired** |
| A2 | P2 | index row still opens with the superseded slot-1 wall | `test-evidence/index.md:16` marks `70.99 s` superseded and names the rebuilt pre-change referent | **repaired** |

## 2. Findings Summary

Severity counts cover the three non-code segments (process § 3, artifact § 2.2, implementation § 2.3). The code segment keeps its own six-level family and is never merged into these counts.

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

Category counts cover the **process-segment** findings only (Section 3); the artifact and implementation findings are counted by severity in their own slots.

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 0 |
| Workflow | 3 |
| Documentation | 0 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base (feature-first-commit: parent of `5d1c8eed0`) |
| Head commit | `5ec91b8c7be0464db6b4ec7c7d6f0a15f3ff5a20` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec …` |
| Renderer mode | `text` | non-interactive review; receipt records `renderer=text` |
| Changed / judged / skipped / gap files | 298 / 141 / 157 / 0 | copied field by field from `code-review.md`'s receipt block; judged = 136 `.py` + 4 `.sh` + 1 `.toml`, skipped = 57 `.md` + 84 `.txt` + 11 `.gz` + 3 `.json` + 1 `.yaml` + 1 `.jsonl` with legal reasons `non-code-file` / `binary` |
| Segment verdict | `not-evaluated` | the receipt's own reading (`skipped_files > 0` ⇒ no coverage credit, C-37); 0 gap, 0 blocking |
| Gate verdict | `allow` (code merge gate) — **transition gate granted** | `report --summary --file code-review.md` → `{"blocking":0,"important":1,"suggestion":1,"nitpick":0,"question":0,"praise":1}`, `"gate":"allow"`; the four transition conditions all hold (§ 2.4 and the Conclusion) |
| Reason, when one applies | not-evaluated: 157 legal skips (non-code/binary evidence files), 0 gaps; `none` for the code merge gate | `code-review.md` |
| Uncommitted scope | 49 uncommitted paths were outside the review object (runtime memory/feedback/exec-quant records, three pre-existing checkpoints, this run's uncommitted review products); the receipt gives no conclusion over them; the verbatim sentence with the full path list lives in `code-review.md` § 未提交范围 | `code-review.md` |
| Record | `.specify/specs/098-suite-speed-optimizations/code-review.md` | written because triage = `run` |
| Archive | `.specify/specs/098-suite-speed-optimizations/code-review-20261110T195724Z.md` | `start` rotated the round-2 record |

**Important item answer (required)**: *Agree.* The single `important` item (`scripts/bash/run-tests.sh:372` — `tier=caller` skips the 086 C-010/C-011 serial two-pass while tier-selection C-012 declares the serial model unchanged, and no guard covers the serial-marked + caller-`-m` intersection) is a real contract/implementation mismatch. It remains open by design of this review: the fix is a contract-wording narrowing plus a guard, not a code change a reviewer may make. Not blocking.

**Round-1/2 code records**: archived at `code-review-20261110T185547Z.md` and `code-review-20261110T195724Z.md`; their `important` item is the same one, re-recorded and re-answered here. The `suggestion` (`collect_slow_count` never surfaces pytest status 2/4) and the `praise` (root-cause isolation repair) recur unchanged.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `test-evidence/` | union of the standard spec set and `plan.md` § Project Structure (lines 130-141) |
| Coverage line | 10 / 10 | present members / expected members |
| Missing members | `none` | — |
| Segment verdict | `pass` | every expected member exists and is internally traceable; round-2 A1/A2 re-measured as repaired; no new finding |

No findings in this segment. Verified on this round's tree: 61 task rows, zero `[ ]`/`[>]` rows (GATE-3 reading 0); `deferred_tasks=` empty; all ten `evidence_sha256=` values recompute equal; every `evidence_path=` names an existing non-empty record; SC-001…SC-009 `final` and SC-010/SC-011 `supporting` path markers unchanged; the feature detail's claim (`Ready for Review`) and this feature's records do not contradict.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `5ec91b8c7be0464db6b4ec7c7d6f0a15f3ff5a20` | run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh --workers 4 tests/contract/test_suite_tier_contract.py tests/contract/test_parallel_consistency_contract.py tests/contract/test_scan_cache_contract.py tests/contract/test_event_wait_contract.py tests/contract/test_inprocess_conversion_contract.py tests/contract/test_run_tests_runner_contract.py -q` | recorded verbatim; run by this review |
| Smoke exit code | 0 | 86 passed in 34.93 s, `mode=parallel workers=4 dist=load passes=1 tier=fast excluded_slow=0`; outer wall 36.90 s |
| Smoke evidence path | `.specify/specs/098-suite-speed-optimizations/test-evidence/review-smoke-098-r3.txt` | exists and is non-empty (10 lines) |
| Scope and regression verdict | **pass** — the repair r2 delta (`c4f7c8bd1..5ec91b8c7`) is the closure-leg execution plus its root-cause test-isolation fix, tasks/verification/index updates and evidence records; no unasked feature work; regression re-measured on one tree (full-tier parallel 223 names / serial 223 names byte-identical, both `comm` directions 0; isolated files 38/38 green parallel and serial; smoke 86/86) | `test-evidence/closure.txt`, `closure-isolation-fix.txt`, `review-smoke-098-r3.txt` |
| Segment verdict | `pass` | scope and regression hold; the closure-stage criteria are quoted, not judged, by this segment |

No findings in this segment. The `final_path` record is quoted in § 2.4 and is not re-counted here.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features/086-efficient-test-execution.md:6`, copied, not written back |
| `final_path` record, copied verbatim (7/7) | pass 9 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 9 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/098-suite-speed-optimizations --feature-detail .specify/features/086-efficient-test-execution.md --json --json-out .specify/specs/098-suite-speed-optimizations/test-evidence/review-r3-arc-payload.json` (exit 0; payload archived; invocation and output at `test-evidence/review-r3-arc-verdict.txt`) |
| Comparison verdict | `agree` | checker verdict `accept` against the claim `Ready for Review` |
| Failed condition, on refusal | `none` — no refusal; the checker's `reasons` list is empty and all four completion conditions read `true` | payload `completion_conditions` |
| Fixed item, on refusal | `none` — `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here `pass = 9` | the zero-pass trigger cannot be evaluated |

## 3. Findings (Problems & Improvement Targets)

### F1 — The baseline row is still scheduled last; only its runtime consequence was repaired

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/tasks.md:68,310`; `/…/notes/pre-change-measurements.md:14-16,21,26`
- **Evidence** (verbatim quote):

  ```
  - [X] T003 [blockedBy: T001] Record two-slot budget slot 1 of 2 (implement-start baseline, …)
  (tasks.md:68)

  | WP-9 Measurement, forbidden shortcuts, interface evidence | T003, T022, T055–T060 | 8 |
  (tasks.md:310)

  The package map (`tasks.md` § Work Package Mapping) assigns T003 to WP-9, the last
  package, so the slot-1 run below executes on the post-WP-8 tree rather than literally
  before WP-1.   (notes/pre-change-measurements.md:14-16)
  ```

- **Why it's a problem**: Phase 1 says the baseline "starts immediately" while the package map places it in the last package; a future run of this same tasks file repeats the defect, and this slice only recovered because review-repair rebuilt the baseline at the implement-entry tree. The evidence base is correct (`76.52 s` vs `70.62 s`), but the structural rule that should have prevented the mis-timing is still unowned by the tasks template (REC-098-01, open).
- **Proposed fix**: make the baseline row a hard predecessor of every behavior-changing package (e.g. `[blockedBy: T003]` on all WP rows or a dedicated WP-0), as REC-098-01 states; this slice keeps its rebuilt evidence and needs no re-run.

### F2 — `checkpoints/02-clarify.md` is still a byte-identical copy of `01-requirements.md`

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/checkpoints/02-clarify.md:1`
- **Evidence** (verbatim quote):

  ```
  # Checkpoint 01 — requirements（098-suite-speed-optimizations）

  - 哨兵 REQUIREMENTS-DONE（修复轮）；U4 PASS（首轮门禁 exit 2：RS-001 Contract 单元格混排 → 修复后 pass）
  ```

  Measured this round: `cmp checkpoints/01-requirements.md checkpoints/02-clarify.md` exits 0 (byte-identical); the file contains the requirements sentinel and none of the clarify stage's content (the 5 Q/A, commit `4c359241b`, gate readings).

- **Why it's a problem**: a checkpoint is the stage's handoff and re-entry record; a duplicated file tells a re-entrant session that clarify produced the requirements record and gives no clarify handoff at all. The stage-close check that should catch this only tests file existence, not that the record is about its own stage.
- **Proposed fix**: write the real clarify checkpoint from `4c359241b` (sentinel `CLARIFY-DONE`, the 5 Q/A, the 086 binding, gate readings) and add one consistency assertion to the driver's stage close: the checkpoint's declared stage/sentinel must match its filename (REC-098-07).

### F3 — The review gate refuses on a verdict its owner defines at feature-line closure

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/templates/commands/review.md:99`; `/…/shared/workflow/acceptance-hardening.md:263-267`
- **Evidence** (verbatim quote):

  ```
  The checker's verdict is a closed two-value set — `accept` and `block` — and `block` is a
  **non-pass**: it refuses the transition on its own, whatever the claim reads …
  (templates/commands/review.md:99)

  At the **feature line's closure**. One line carries a feature's whole slice set, so the
  verdict runs once, when that line closes — a `final`-path criterion is legitimately not
  `pass` in an early slice, and reading the judgement as "every slice merge must pass it"
  would block the first merge by construction. Slice merges are judged by the review gate.
  (shared/workflow/acceptance-hardening.md:263-267)
  ```

- **Why it's a problem**: 098's SC-003/SC-005 readings were T061's, and the driver's order ran closure after review, so rounds 1–2 were forced to refuse on the same verdict — correctly, but the review stage's sentinel carried no machine-readable distinction between "refused for defects" and "refused pending the closure leg". This round happens to pass (ARC `accept`), so the ambiguity did not bite; it remains in the template for the next slice whose final readings are closure-stage rows.
- **Proposed fix**: when every blocking reason is a `final-path-not-pass` whose `SC-NNN` row is declared a closure-stage leg (`verification.md` ladder + `deferred_tasks=` naming the row), let the review conclusion record a named `pending-closure` residual beside the refusal (the ARC record itself stays unchanged), or move the closure budget leg before review; either way the driver gets a mechanical route to the closure stage (REC-098-08).

### F4 — The state spine remains one review round behind

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/098-suite-speed-optimizations.md:12-13,51-52`
- **Evidence** (verbatim quote):

  ```
  attempt: 1
  retry_limit: 3
  last_verdict: review r1 refused Implemented→RfR (5 P0 + 6 P1); review-repair r1 delivered — … next: review re-run
  (lines 12-13)

  - dispatch: 待 review 重跑（round 2）；本行交付物为修复轮证据
  - gates: `closure-acceptance-check.py` verdict=`block` — reasons `final-path-not-pass: SC-003` / `final-path-not-pass: SC-005` / `status-claims-implemented-but-blocked`
  (lines 51-52)
  ```

- **Why it's a problem**: round 2 completed, refused, and review-repair r2 landed `accept` — none of it is visible in the spine, which still describes round 1 as the last verdict, names round 2 as the pending dispatch, and records the superseded `block` gate. A re-entrant driver or a human reading only the spine acts on a one-round-old picture; this round the `next: review re-run` line happened to be the right action, but the `gates` line contradicts the current tree (ARC `accept`, 9/9). This is the same discipline gap REC-098-03 already owns; the spine is updated at stage open, not at each review-round return.
- **Proposed fix**: extend REC-098-03's spine discipline to review-round boundaries — every review dispatch return (refused, granted, or repair-then-granted) updates the loop-state `last_verdict` / attempt and the human `dispatch` / `gates` lines before the next dispatch.

## 4. What Worked — Preserve (Brief)

- The closure stage ran the deferred T061 honestly: attempt 1 exposed a real five-name parallel-only isolation defect, it was diagnosed at the root (engine C-7 self-location in a nested worktree), repaired with the r1 precedent (`--workspace`), and the slot was re-taken — with attempt-1 readings retained as diagnostics and an explicit anti-metric disclosure.
- The closure evidence is name-level and reproducible: parallel 223 / serial 223 lists byte-identical (both `comm` directions 0), zero new names versus the slot-1 baseline (64 removals), and the three names newer than the rebuilt pre-change list are enumerated with their worktree-state causes.
- `verification.md` is now a fully bound record: ten evidence hashes recompute equal, the measured tree is named for baseline / post-change / closure, and the closure verdict is copied verbatim (`accept`, 9/9) rather than re-derived.
- Round-2's A1/A2 were repaired at the artifact level without disturbing the record: measured-tree fields were added, and the evidence index marks the superseded slot-1 wall.
- The code-segment receipt worked with no workaround: legal skip selectors (`non-code-file` / `binary`) produced a real 298/141/157/0 block, 0 gap, and the merge gate reads `allow`.

## 5. spec-kit / SDD Improvement Recommendations

No new `REC-…` identifier is coined this round; the recommendations below are the carried register entries (`open`), reached by their existing pointers.

### 5.1 Template Improvements

- **REC-098-09 (open at the framework level; slice instance repaired) — Verification records must name the tree they measured** — Target: `templates/verification-log-template.md`. Change: require a measured-tree field (`baseline_tree=` / `post_change_tree=`) distinct from any base/claim commit. Source: round-2 A1 (repaired in this slice's `verification.md`, template still open).

### 5.2 Command Prompt Improvements

- **REC-098-01 (carried, open) — The baseline row cannot be scheduled last** — Target: `templates/commands/tasks.md` § Work Package Mapping. Change: reject a WP mapping in which a "Phase 1 / starts immediately" baseline row is assigned to the last package; require it to precede every behavior-changing package. Source: F1.
- **REC-098-08 (carried, open) — Distinguish "pending closure" from "defect" at the review gate** — Target: `templates/commands/review.md` § The Acceptance Reality Check. Change: when the checker's only blocking reasons are closure-stage `final-path-not-pass` criteria, record the refusal with a named `pending-closure` residual (ARC record unchanged) so the driver can route to the closure stage instead of another repair round; alternatively reorder the closure budget leg before review. Source: F3.

### 5.4 Workflow Improvements

- **REC-098-07 (carried, open) — A checkpoint must be about its own stage** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` § stage close. Change: the stage-close verification asserts that the checkpoint named for the stage carries that stage's sentinel/title and its own artifacts; a byte-identical copy of another stage's checkpoint fails the close. Source: F2.
- **REC-098-03 (carried, open; scope extended) — The spine must land at every stage boundary** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` § drive state writes. Change: in addition to the stage-boundary snapshots, update the loop-state `last_verdict`/attempt and the human `dispatch`/`gates` lines at every review-round return (refused, granted, or repair-then-granted) before the next dispatch. Source: F4.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Make the baseline row precede all behavior-changing packages (carried, open) | `templates/commands/tasks.md` § Work Package Mapping | F1 (r2 F1) |
| P2 | Distinguish pending-closure from defect at the review gate | `templates/commands/review.md` § The Acceptance Reality Check | F3 (r2 F3) |
| P2 | Check the checkpoint's stage against its filename | driver `stage-prompts.md` § stage close | F2 (r2 F2) |
| P2 | Land the spine at every review-round return | driver `stage-prompts.md` § drive state writes | F4 |
| P2 | Bind verification readings to the measured tree (template) | `templates/verification-log-template.md` | round-2 A1 (instance repaired) |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings were raised in this round; the P0 independent-validation pass is vacuously satisfied.** This review session authored none of the artifacts under review (round 1, round 2 and the two repair rounds were separate sessions), so the same-author detection gate did not fire.

## 8. Feedback

This document is the round-3 process/artifact/implementation-side review of the 098 slice. The code-side record is the separate `code-review.md` (`blocking_entries=0`, `important=1` answered, `suggestion=1`, `praise=1`, gate `allow`). The round-2 report is archived as `review-20261110T195934Z.md`; the round-1 report remains at `review-098.md`.

**Concurrency reading**: requested 4 segment units; effective 1; effective_reason `write-conflict` — all four segments write one `review.md` carrier and share the worktree, and the composition owner (`shared/workflow/acceptance-hardening.md` § Review Composition) fixes a serial order ("no parallel mode"), so the run is serial by composition and by the intersecting write domains.

## Conclusion — status transition judgement

**`Implemented → Ready for Review` is GRANTED — the transition is legal.** All four conjunctive conditions hold on this run's evidence, and the Acceptance Reality Check agrees with the claim:

1. **No deferred task remains**: T061 is `[X]` (61/61 rows closed), `deferred_tasks=` is empty in `verification.md`, and no user waiver is involved.
2. **Review evidence has been produced**: this `review.md` (four segments + ARC) and the current `code-review.md` (receipt 298/141/157/0) are on disk at the head commit.
3. **The current code-segment record contains no `blocking` entry**: `report --summary --file code-review.md` reads `blocking_entries=0`, gate `allow`; the one `important` item is answered above.
4. **No `final`-path criterion sits in `blocked` / `deferred` / `fail`**: all nine final-path criteria are `pass` (`final_path`: pass 9 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 9), and the checker's verdict is `accept` with an empty `reasons` list.

The bound feature 086's claimed status stays `Ready for Review` (this run confirms the claim rather than flipping a status that was already recorded; a refusal would have left it unchanged too). This run presents itself as a completed review. The process-side P1/P2 findings above are framework-level improvement targets and do not gate the transition.

**Client capture**: not run — framework hat. This repository is the spec-kit framework source itself (`dogfooding-definitions.md` § 2.1), so the capture trigger's first condition (a client-project hat) does not hold; zero entries were posted, and the conclusion names the hat verdict as its basis.

**Next action**: none required by this gate. The driver may close the review stage and proceed on its own plan; the open framework RECs ride the normal feedback/improvement flow, not another review round.
