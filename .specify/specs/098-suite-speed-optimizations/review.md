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
| Commit SHA | `f129eb8019ac11bef74c3931271a0aec4d6d145b` (short: `f129eb801`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder · four-segment composition (`/speckit.review`), round 2 |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash 4/5, Python 3.11.11, pytest 8.4.2, pytest-xdist 3.8.0, git 2.43.5 |
| spec-kit Source Snapshot | this worktree at `f129eb801` (framework source `templates/`, `shared/`, `scripts/`, `skills/` and the client runtime `.specify/` in one repository) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 266 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/requirements.md` | 27 FR / 11 SC (9 final, 2 supporting), 17 assumptions, 5 clarification Q/A |
| plan.md | 366 | `…/098-suite-speed-optimizations/plan.md` | 22-row Constitution Check, T-001…T-003, EP-001…EP-004, 9 work packages |
| tasks.md | 407 | `…/098-suite-speed-optimizations/tasks.md` | 61 rows (60 `[X]`, 1 `[~]` T061), 7 phases, DoD-1…DoD-7, GATE-1…GATE-5 |
| research.md | 137 | `…/098-suite-speed-optimizations/research.md` | B-1…B-10 measured baselines, R-1…R-10 decisions |
| data-model.md | 121 | `…/098-suite-speed-optimizations/data-model.md` | Entities E-1…E-8 |
| quickstart.md | 193 | `…/098-suite-speed-optimizations/quickstart.md` | Scenarios S-0…S-13 |
| feature-ref.md | 66 | `…/098-suite-speed-optimizations/feature-ref.md` | 26-row delivery surface, disclosures, out-of-scope |
| contracts/ | 424 (6 files) | `…/098-suite-speed-optimizations/contracts/` | 68 clauses (16/9/12/11/10/10) |
| verification.md | 188 | `…/098-suite-speed-optimizations/verification.md` | **Now present** — SC-001…SC-011 status rows, one smoke triple, `deferred_tasks=T061`, RS-004, copied closure verdict |
| review-098.md (round-1 archive) | 379 | `…/098-suite-speed-optimizations/review-098.md` | Round-1 report, archived by this run's rotation |
| code-review.md | 1030 | `…/098-suite-speed-optimizations/code-review.md` | Round-2 code record: receipt block (277/139/138/0), one `important`, one `suggestion`, one `praise` |
| code-review-20261110T185547Z.md (round-1 archive) | 925 | `…/098-suite-speed-optimizations/code-review-20261110T185547Z.md` | Round-1 code record, archived by `start` |
| checklists/ | 2 files | `…/098-suite-speed-optimizations/checklists/` | requirements-quality checklist + dated suite-speed checklist |
| checkpoints/ | 8 files | `…/098-suite-speed-optimizations/checkpoints/` | 01-requirements … 08-review (02 is a duplicate — finding F2) |
| notes/ (three records) | 8688 / 297 / 344 | `…/098-suite-speed-optimizations/notes/` | pre-change measurements (§1 superseded slot-1 + §7 rebuilt baseline), quickstart run, red-first |
| test-evidence/ | index + records | `…/098-suite-speed-optimizations/test-evidence/` | SC → evidence mapping; round-2 smoke and affected-test transcripts added |

## 1. Process Execution Timeline

Reconstructed from the 26 commits in `b3da3a26d..f129eb801` (feature-first-commit base resolved by `git-delta-review.sh base`) plus this round's working-tree evidence. Round-2 additions are rows 20–23.

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
| 12 | constitution amended 1.19.0 → 1.19.1 (Principle VII carrier) | `af73f65f1` | **Out-of-plan**: no 098 task row asks for it; now attributed by `D-098-01` (round 1 F7, repaired) |
| 13 | WP-1 runner tier mechanism; WP-2 slow registry | `0d1f7a1e4`, `1dca066fb` | None |
| 14 | T012 green record + T013 tier/slow mutation drills | `719f78b90` | T012's scope wording outran the file at that moment (round 1 F8, repaired) |
| 15 | WP-3 … WP-9 (docs, parallel consistency, cache, clock, in-process, measurement) | `ac91ab81a` … `2183d4986` | None |
| 16 | S-4 serial wall restated from file timestamps | `c5b2b32a7` | Measurement proxy, disclosed |
| 17 | T013 close — 13 mutation legs | `ea5962c87` | None |
| 18 | Implement stage close — **without** its Step 9 close-out (no `verification.md`, no closure record) | Round-1 evidence: `git log --all --name-only -- …/verification.md` was empty at `ea5962c87` | **Deviation**: the Pre-Status-Flip Gate was skipped (round 1 F1/A1/I1) |
| 19 | Review round 1 — four segments + ARC; transition refused | `b9e5a35a2`; archived report `review-098.md` | Refusal was correct for the evidence state at that tree; P0 5 / P1 6 / P2 4 |
| 20 | Review-repair r1 — close-out, SC-002 root fix, rebuilt baseline, spine/checkpoints, P2 quick wins | `f129eb801` | Remediation of round-1 findings; disclosed per finding in §1.1 |
| 21 | Round-2 close-out verification — evidence sha256 recomputed (9/9 bound records match), SC-002 `comm` recomputed (0/0), closure checker reproduced (`block`, pass 7 / partial 2 / total 9), spine snapshot parsed (`schema v1`, `state running`) | this run; `test-evidence/review-r2-arc-payload.json`, `test-evidence/review-repair-r1-sc002-comm.txt` | None |
| 22 | Round-2 code segment — `start` rotated the round-1 record; receipt written by the **workspace** script with legal skip selectors (`*.md`/`*.txt`/`*.yaml`/`*.jsonl`/`*.json` → `non-code-file`, `*.gz` → `binary`); gate `allow` | `code-review.md`, `code-review-20261110T185547Z.md`; `report --summary --format json` → `{"blocking":0,"important":1,"suggestion":1,"nitpick":0,"question":0,"praise":1}` | None — the round-1 receipt-provenance workaround is no longer needed (F6 repaired) |
| 23 | Round-2 implementation segment — smoke re-run and the two affected suites | `test-evidence/review-smoke-098-r2.txt` (86 passed, exit 0, 37.34 s wall), `review-r2-affected-trigger-engine.txt` (145 passed), `review-r2-affected-receipt-contracts.txt` (59 passed) | None |

### 1.1 Round-1 finding verification (5 P0 / 6 P1)

Every round-1 finding was re-measured on the round-2 tree; nothing below is accepted on the repair's self-report alone.

| r1 ID | Sev | Round-1 claim | Round-2 verification (evidence) | Status |
|-------|-----|---------------|---------------------------------|--------|
| F1 / A1 / I1 | P0 | Implement close-out skipped; no `verification.md` | `verification.md` exists (188 lines) with SC-001…SC-011 rows, one smoke triple, `deferred_tasks=T061` (line 150), RS-004 row and the copied closure verdict; all nine `evidence_sha256=` values recomputed equal; the checker reproduces the same `block` payload | **repaired** |
| A2 / I2 | P0 | SC-002 final-tree bidirectional difference non-empty (`comm -13` = 2) | `review-repair-s4-parallel-names.txt` / `-serial-names.txt` each 137 names; recomputed `comm -13` = 0 and `comm -23` = 0; `test_trigger_engine.py` runs 145/145 green; root cause (engine C-7 self-location inside the nested worktree) recorded in `review-repair-r1-trigger-fix.txt` | **repaired at the root** |
| A3 / I3 | P1 | slot-1 baseline taken on the post-WP-8 tree | rebuilt baseline at `af73f65f1` (implement-entry), 76.52 s / 279 names vs final tree 70.73 s / 254 names = 92.4 % ≤ 110 %; `git diff --stat b3da3a26d af73f65f1 -- tests/ scripts/ pyproject.toml` is the constitution-pin test only; both full logs archived (`.log.gz`) | **repaired (slice)** |
| F2 | P1 | state spine stale at requirements/stalled | spine machine block and human section now read `stage: review`, `stage_base_commit: ea5962c87`, `attempt: 1`, and the repair verdict; `loop-state.py snapshot` parses `schema v1`, `state running` (derived stage remains `implement` until a `REVIEW-DONE` sentinel exists — the expected mid-stage reading) | **repaired** |
| F3 | P1 | baseline row scheduled last (T003 in WP-9) | runtime consequence repaired by the rebuilt baseline; the WP mapping is unchanged (`tasks.md:310` still assigns T003 to WP-9); REC-098-01 remains open at the framework level | **carried** → this round's F1 |
| F4 | P1 | driver checkpoints stop at plan | `checkpoints/04-tasks.md` … `08-review.md` exist; while verifying, `02-clarify.md` was found byte-identical to `01-requirements.md` (`cmp` exit 0) | **repaired, residual** → this round's F2 |
| A4 | P1 | T061 had no `deferred_tasks=` carrier | `verification.md:150` `deferred_tasks=T061 — driver closure stage after review; slot 2 of 2, not an implement-stage run` plus a reason summary | **repaired** |
| F5 | P2 | DoD status `pending` contradicted 60 `[X]` rows | `tasks.md:23` now names the remaining condition (T061; SC-003/SC-005 `partial`) and the close-out record; DoD is honestly not met | **repaired** |
| F6 | P2 | `receipt` refused a legal binary skip selector | script fixed (skip selectors precede line measurement); source and `.specify` mirror byte-identical; `sync-mirrors.py --check` exit 0; this round's receipt with `*.gz` → `binary` exits 0 and writes a real block; positive/negative drill archived | **repaired** |
| F7 | P2 | user-ruled constitution amendment unattributed | `.specify/register.md:221` `D-098-01 … ratified (user ruling 2026-11-10; review F7 补登记)` | **repaired** |
| F8 | P2 | T012 claimed "obligations 1–11" before obligation 11 existed | `tasks.md:91` now reads "obligations 1–10 plus the slow-membership guard cases as they exist at this row; obligation 11 lands with T021/T022" | **repaired** |

## 2. Findings Summary

Severity counts cover the three non-code segments (process § 3, artifact § 2.2, implementation § 2.3). The code segment keeps its own six-level family and is never merged into these counts.

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

Category counts cover the **process-segment** findings only (Section 3); the artifact and implementation findings are counted by severity in their own slots.

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation | 0 |
| Workflow | 2 |
| Documentation | 0 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base (feature-first-commit: parent of `5d1c8eed0`) |
| Head commit | `f129eb8019ac11bef74c3931271a0aec4d6d145b` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec …` |
| Renderer mode | `text` | non-interactive review; receipt records `renderer=text` |
| Changed / judged / skipped / gap files | 277 / 139 / 138 / 0 | copied field by field from `code-review.md`'s receipt block; judged = 134 `.py` + 4 `.sh` + 1 `.toml`, skipped = 54 `.md` + 74 `.txt` + 7 `.gz` + 1 `.yaml` + 1 `.jsonl` + 1 `.json` with legal reasons `non-code-file` / `binary` |
| Segment verdict | `not-evaluated` | the receipt's own reading (`skipped_files > 0` ⇒ no coverage credit, C-37); 0 gap, 0 blocking |
| Gate verdict | `allow` (code merge gate) — **transition gate `blocking-unresolved`** | `report --summary --file code-review.md` → `"gate":"allow"`, `blocking_entries=0`; the `Implemented → Ready for Review` transition is refused for the non-code conditions named in § 2.4 and the conclusion |
| Reason, when one applies | `none` for the code merge gate; the transition refusal's named conditions are in § 2.4 | — |
| Uncommitted scope | 48 uncommitted paths were outside the review object (runtime memory records, feedback records, the spine's runtime residue and the pre-existing checkpoints); the receipt gives no conclusion over them; the verbatim sentence with the full path list lives in `code-review.md` § 未提交范围 | `code-review.md` |
| Record | `.specify/specs/098-suite-speed-optimizations/code-review.md` | written because triage = `run` |
| Archive | `.specify/specs/098-suite-speed-optimizations/code-review-20261110T185547Z.md` | `start` rotated the round-1 record |

**Important item answer (required)**: *Agree.* The single `important` item (`scripts/bash/run-tests.sh:372` — `tier=caller` skips the 086 C-010/C-011 serial two-pass while tier-selection C-012 declares the serial model unchanged, and no guard covers the serial-marked + caller-`-m` intersection) is a real contract/implementation mismatch. It remains open by design of this review: the fix is a contract-wording narrowing plus a guard, not a code change a reviewer may make. Not blocking.

**Round-1 code record**: archived at `code-review-20261110T185547Z.md`; its `important` item is the same one, re-recorded and re-answered here.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `test-evidence/` | union of the standard spec set and `plan.md` § Project Structure (lines 130-141) |
| Coverage line | 10 / 10 | present members / expected members |
| Missing members | `none` | — |
| Segment verdict | `pass` | every expected member exists and is internally traceable; the two findings below are P2 record-accuracy defects |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `.specify/specs/098-suite-speed-optimizations/verification.md` | 12, 16, 23 | line present | A1 — the baseline/post-change commit fields do not name the trees actually measured (baseline wall/names were taken at `af73f65f1`, post-change on a working tree committed as `f129eb801`); a later reader diffing the named commits cannot reproduce the readings |
| P2 | `.specify/specs/098-suite-speed-optimizations/test-evidence/index.md` | 15 | line present | A2 — the SC-005 row still opens with the superseded slot-1 wall (`70.99 s`) while the authoritative rebuilt wall is `76.52 s`; the supersession is stated only in `notes/pre-change-measurements.md:21`, not at the index row |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `b3da3a26dfba209057f65c2b17962b9516812c39` | the resolved diff base |
| Head commit | `f129eb8019ac11bef74c3931271a0aec4d6d145b` | run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh --workers 4 tests/contract/test_suite_tier_contract.py tests/contract/test_parallel_consistency_contract.py tests/contract/test_scan_cache_contract.py tests/contract/test_event_wait_contract.py tests/contract/test_inprocess_conversion_contract.py tests/contract/test_run_tests_runner_contract.py -q` | recorded verbatim; run by this review |
| Smoke exit code | 0 | 86 passed in 35.36 s, `mode=parallel workers=4 dist=load passes=1 tier=fast excluded_slow=0`; outer wall 37.34 s |
| Smoke evidence path | `.specify/specs/098-suite-speed-optimizations/test-evidence/review-smoke-098-r2.txt` | exists and is non-empty (9 lines) |
| Scope and regression verdict | **pass** — the five new guards plus the 086 runner suite are green; the repair commit is remediation of round-1 findings (fixture isolation for SC-002, receipt skip ordering, close-out records, register/task wording) and carries no unasked feature work; the two affected code surfaces re-run green (145 + 59 passed); SC-002's name sets are equal in both directions | see the three transcripts above |
| Segment verdict | `pass` | scope and regression hold; the closure-stage criteria are quoted, not judged, by this segment |

No findings in this segment.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features/086-efficient-test-execution.md:6`, copied, not written back |
| `final_path` record, copied verbatim (7/7) | pass 7 · blocked 0 · deferred 0 · partial 2 · fail 0 · unknown 0 · total 9 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/098-suite-speed-optimizations --feature-detail .specify/features/086-efficient-test-execution.md --json` (exit 1; payload archived at `test-evidence/review-r2-arc-payload.json`) |
| Comparison verdict | `refused` | the checker's verdict is `block` and the claim is `Ready for Review` |
| Failed condition, on refusal | the checker's named reasons: `final-path-not-pass: SC-003`, `final-path-not-pass: SC-005`, `status-claims-implemented-but-blocked`; the two criteria are `partial` because their readings are the T061 closure-stage legs by `tasks.md` GATE-4 / DoD-7; independently, the gate's first condition fails because T061 remains `[~]` with no user waiver | named conditions, not merely "the transition was refused" |
| Fixed item, on refusal | `none` — `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here `pass = 7` | the zero-pass trigger cannot be evaluated |

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

- **Why it's a problem**: Phase 1 says the baseline "starts immediately" while the package map places it in the last package; a future run of this same tasks file repeats the defect, and the slice only recovered because review-repair rebuilt the baseline at the implement-entry tree. The evidence base is now correct (`76.52 s` vs `70.73 s`), but the structural rule that should have prevented the mis-timing is still unowned by the tasks template (REC-098-01, open).
- **Proposed fix**: make the baseline row a hard predecessor of every behavior-changing package (e.g. `[blockedBy: T003]` on all WP rows or a dedicated WP-0), as REC-098-01 states; this slice keeps its rebuilt evidence and needs no re-run.

### F2 — `checkpoints/02-clarify.md` is a byte-identical copy of `01-requirements.md`

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/.specify/specs/098-suite-speed-optimizations/checkpoints/02-clarify.md:1`
- **Evidence** (verbatim quote):

  ```
  # Checkpoint 01 — requirements（098-suite-speed-optimizations）

  - 哨兵 REQUIREMENTS-DONE（修复轮）；U4 PASS（首轮门禁 exit 2：RS-001 Contract 单元格混排 → 修复后 pass）
  ```

  Measured: `cmp checkpoints/01-requirements.md checkpoints/02-clarify.md` exits 0 (byte-identical); the file contains the requirements sentinel and none of the clarify stage's content (the 5 Q/A, commit `4c359241b`, gate readings).

- **Why it's a problem**: a checkpoint is the stage's handoff and re-entry record; a duplicated file tells a re-entrant session that clarify produced the requirements record and gives no clarify handoff at all. The stage-close check that should catch this only tests file existence, not that the record is about its own stage.
- **Proposed fix**: write the real clarify checkpoint from `4c359241b` (sentinel `CLARIFY-DONE`, the 5 Q/A, the 086 binding, gate readings) and add one consistency assertion to the driver's stage close: the checkpoint's declared stage/sentinel must match its filename.

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

- **Why it's a problem**: 098's SC-003/SC-005 readings are T061's, and the driver's order runs closure after review, so both review rounds are forced to refuse on the same verdict — correctly, but the review stage's sentinel then carries no machine-readable distinction between "refused for defects" and "refused pending the closure leg". The driver must interpret prose to decide whether to repair or proceed to closure. This round's refusal is the second consecutive one with zero open P0 and one carried framework P1, which is exactly the shape the ambiguity hides.
- **Proposed fix**: when every blocking reason is a `final-path-not-pass` whose `SC-NNN` row is declared a closure-stage leg (`verification.md` ladder + `deferred_tasks=` naming the row), let the review conclusion record a named `pending-closure` residual beside the refusal (the ARC record itself stays unchanged), or move the closure budget leg before review; either way the driver gets a mechanical route to the closure stage.

## 4. What Worked — Preserve (Brief)

- The review-repair round repaired at the root, not the symptom: SC-002's serial-only names disappeared because the engine's C-7 self-location trap was fixed in the test helper, and the file then ran 145/145.
- The rebuilt baseline is a genuine pre-change referent (`af73f65f1`, diff vs the base is the constitution-pin test only), with complete logs and a name-level disclosure.
- `verification.md` is an honest record: ten bound evidence hashes all match, the two `partial` rows carry the five ladder fields, and the checker's `block` verdict is copied verbatim.
- The receipt defect (F6) was fixed in the framework source, mirrored byte-identically, and drilled positive/negative; this round's receipt no longer needs the workaround.
- Round-1 findings were closed with verifiable artifacts, and the repair disclosed its own deviations (bare checker exit 2, validator warnings, diagnostic side effects).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-098-09 — Verification records must name the tree they measured** — Target: `templates/verification-log-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations/templates/verification-log-template.md`). Change: require a measured-tree field (e.g. `baseline_tree=` / `post_change_tree=`) distinct from any base/claim commit, or state that the wall/name readings are bound to that hash. Source: A1. Expected impact: a later reader can reproduce a wall or name list from the record without reading prose notes.

### 5.2 Command Prompt Improvements

- **REC-098-01 (carried, open) — The baseline row cannot be scheduled last** — Target: `templates/commands/tasks.md` § Work Package Mapping (absolute supplement: `…/templates/commands/tasks.md`). Change: reject a WP mapping in which a "Phase 1 / starts immediately" baseline row is assigned to the last package; require it to precede every behavior-changing package. Source: F1. Expected impact: the two-slot baseline keeps its pre-change referent by construction.
- **REC-098-08 — Distinguish "pending closure" from "defect" at the review gate** — Target: `templates/commands/review.md` § The Acceptance Reality Check (absolute supplement: `…/templates/commands/review.md`). Change: when the checker's only blocking reasons are closure-stage `final-path-not-pass` criteria, record the refusal with a named `pending-closure` residual (ARC record unchanged) so the driver can route to the closure stage instead of another repair round; alternatively reorder the closure budget leg before review. Source: F3. Expected impact: the review stage's sentinel becomes actionable for slices whose final readings are closure-stage rows.

### 5.4 Workflow Improvements

- **REC-098-07 — A checkpoint must be about its own stage** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` § stage close (absolute supplement: `…/skills/external/sdd-loop-driver/references/stage-prompts.md`). Change: the stage-close verification asserts that the checkpoint named for the stage carries that stage's sentinel/title and its own artifacts; a byte-identical copy of another stage's checkpoint fails the close. Source: F2. Expected impact: a duplicated checkpoint cannot pass as a handoff record.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Make the baseline row precede all behavior-changing packages (carried, open) | `templates/commands/tasks.md` § Work Package Mapping | F1 (r1 F3) |
| P2 | Distinguish pending-closure from defect at the review gate | `templates/commands/review.md` § The Acceptance Reality Check | F3 |
| P2 | Check the checkpoint's stage against its filename | driver `stage-prompts.md` § stage close | F2 |
| P2 | Bind verification readings to the measured tree | `templates/verification-log-template.md` | A1 |
| P2 | Mark the superseded slot-1 wall in this feature's evidence index | `.specify/specs/098-suite-speed-optimizations/test-evidence/index.md:15` | A2 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings were raised in this round; the P0 independent-validation pass is vacuously satisfied.** The five P0 findings of round 1 were re-measured and are recorded as repaired in § 1.1; they are not re-raised. This review session authored none of the artifacts under review (round 1 and the repair were separate sessions), so the same-author delegation gate did not fire.

## 8. Feedback

This document is the round-2 process/artifact/implementation-side review of the 098 slice. The code-side record is the separate `code-review.md` (`blocking_entries=0`, `important=1`, `suggestion=1`, `praise=1`, gate `allow`). The round-1 report is archived as `review-098.md`.

## Conclusion — status transition judgement

**`Implemented → Ready for Review` is REFUSED.** The bound feature 086's claim stays `Ready for Review` (a refusal is not a downgrade), and this run does not present itself as a completed review. Named conditions:

1. **The closure checker returns `block`** with `final-path-not-pass: SC-003`, `final-path-not-pass: SC-005` and `status-claims-implemented-but-blocked`; the comparison verdict is `refused` (verdict `block` against a `Ready for Review` claim). SC-003/SC-005 are `partial` because their readings are the T061 closure-stage legs by the tasks file's own design (`tasks.md` GATE-4, DoD-7); the record is pass 7 · partial 2 · total 9.
2. **The gate's first condition is not met**: T061 is still `[~]` and no user waiver names it.

Cleared since round 1: the missing `verification.md` / closure record (F1/A1/I1), SC-002's non-empty bidirectional difference (A2/I2), the post-change slot-1 baseline (A3/I3), the deferred carrier (A4), the stale spine and missing checkpoints (F2/F4), and the P2 items F5–F8. All five P0 and six P1 findings from round 1 are verified repaired with evidence; no new P0 was raised. No slice-repairable P1 remains: this round's P1 is the carried framework-level baseline-placement finding (REC-098-01), and the P2s are record-accuracy fixes (checkpoint duplicate, measured-tree fields, index supersession) plus the carried review-gate timing ambiguity.

**Next action**: the driver's closure stage executes T061 (slot-2 full run with `--names-out`, the same-tree `--full --serial` comparison, and the closure wall ratio), then re-runs `closure-acceptance-check.py`. If that verdict becomes `accept`, the transition can be judged again; this review neither forces the flip nor treats the refusal as a defect.
