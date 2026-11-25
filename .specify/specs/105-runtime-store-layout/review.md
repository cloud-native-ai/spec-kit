# Specification-Driven Development (SDD) Process Review Report: Runtime Store Layout — 运行期存储迁出 `.specify/memory/`

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
>
> **Round 2 (re-review after artifact repair).** Round-1 records are archived at `.specify/specs/105-runtime-store-layout/review-105-runtime-store-layout.md` and `.specify/specs/105-runtime-store-layout/code-review-20261125T074505Z.md`. This run re-verified the three round-1 artifact findings (A1 P0, A2 P2, A3 P2) as closed and re-ran all four segments plus the Acceptance Reality Check against head `ed629d558`.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 105 |
| Requirement Key | 105-runtime-store-layout |
| Requirement Name | Runtime Store Layout — 运行期存储迁出 `.specify/memory/` |
| Related Feature | 024 Specification Workspace Versioning |
| Repository | spec-kit |
| Repository URL | (no remote holds these commits) configured remotes: `git@gitee.com:cloud-native-ai/spec-kit.git` (gitee), `git@github.com:cloud-native-ai/spec-kit.git` (github), `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (gitlab); `origin` is the upstream `github/spec-kit` |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — every citation below uses absolute paths plus `git show ed629d558:<path>` recovery instructions |
| Branch | `105-runtime-store-layout` |
| Commit SHA | ed629d5585220fc1363ec6fafbfb3b4b2afdecb0 (short: ed629d558) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-11-25 |
| Reviewer (Agent) | SDD Review Executor (Qoder agent), run `r20261125T022857Z-06dd` — re-review round 2 |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash 4.4.20(1)-release; git 2.43.5; CPython 3.11.11 at `/usr/local/bin/python3` (the profile `python3` has no pytest/typer — all test readings use the pinned interpreter); no container runtime, cluster or network needed |
| spec-kit Source Snapshot | this repository @ ed629d558 (self-hosting framework source = client runtime) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 332 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/requirements.md | 27 FR / 9 SC / 6 STR / 17-row Store Inventory / A-1…A-16 / four clarification sessions |
| plan.md | 339 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/plan.md | 15 WPs, 6 Decision Tensions, BC01…BC18 closed inventory, Test-First Coverage |
| tasks.md | 368 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/tasks.md | 43 dependency-ordered rows across Setup / Foundational / US1–US6 / Polish; DoD status closed |
| verification.md | 111 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/verification.md | smoke triple, hash-bound evidence records, SC-001…SC-009 status rows, RS-001…RS-006, post-P5R `notes=` reading |
| research.md | 271 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/research.md | R-1…R-13 measured premises (baseline, mirrors, live references) |
| data-model.md | 191 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/data-model.md | E-1…E-10 entities, I-1…I-10 invariants |
| quickstart.md | 144 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/quickstart.md | Scenarios S-0…S-8 (one per user journey plus baseline and containment) |
| feature-ref.md | 97 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/feature-ref.md | Feature 024 binding, FR→WP 27/27, SC→evidence 9/9, overlap adjudication |
| contracts/ (4 files) | 356 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/contracts/ | store-layout C-1…C-8; migrate M-1…M-10; memory P-1…P-6; live refs L-1…L-8 |
| checklists/ (2 files) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checklists/ | requirements-stage checklist plus the 40-item runtime-store-layout checklist |
| notes/ (3 files) | 839 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/notes/ | pre-change measurements, red-first evidence (T017 revert drill), quickstart run record |
| test-evidence/ (93 files) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/test-evidence/ | raw run logs, readings, mutation drills, dogfood, acceptance pack, T017 red-base drill |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements stage lands and commits | `15926441a`; `test-evidence/requirements-validator.txt` 0/0 | None (checkpoint 01; one host-owned `.git/config` permission change repaired in passing and disclosed) |
| 2 | clarify binds Feature 024 and records four adjudications | `46276431e`; requirements § Clarifications session 2 | None; the overlap gate was vacuous by design before `feature-ref.md` existed and was adjudicated at plan |
| 3 | plan stage: attempt 1 declared complete without the mandatory Wrap-up; bounded repair re-ran the stage | `647c13cd9`; checkpoint 03: "plan attempt 1 was a false-complete candidate (missing Wrap-up)" | Yes — false-complete candidate (F2) |
| 4 | plan correction: quickstart scenario count 8 → 9 | `fa2de626a` | Repair, disclosed |
| 5 | tasks stage lands; mid-run user addendum (FR-027/SC-009) reconciled upstream-first | `617f9bdce`, `e840ee26b`; checkpoint 04 | Yes — addendum had no named lane (F7) |
| 6 | goal/team/anchor/handoff activation; anchor shipped without the engine binding block | `874ff8dc5`; checkpoint 05 § 1 | Yes — recorded as F-OBS-4 (F3) |
| 7 | checklist stage: 40 items, 40/40 anchored | `169aca624`; `test-evidence/checklist.jsonl` | None |
| 8 | analyze chain converges: three bounded repairs, final 0 CRITICAL / 0 HIGH; one capture briefly used bare `/tmp` | `915bd6f75`, `c333ac007`; checkpoint 07 § 1 | Yes — temp-root slip disclosed (F4) |
| 9 | implement P1 (foundation + declaration) | `5b445e916`; 1150-name failed batch, 0 new | None |
| 10 | implement P2 (migrate dimension) / P3 (memory + tools) | `5bc8ed901`, `45d2ffdd9` | None |
| 11 | implement P4 (dogfood + live references); feedback records swept into the package commit | `6a62a8c3a`; checkpoint 08 § 3 | Yes — broad staging (F5) |
| 12 | implement P5 (US6 + BC guard + final gate); GATE-8 recorded 43 open rows at capture time, deferred to the driver | `6b442ed97`; `test-evidence/t041-final-gate.txt` § 6 | Yes — gate ownership split (F1) |
| 13 | P5R repair: completed receipt supersedes the resumed receipt so a third apply is `clean` | `1e6dc208c`; `test-evidence/p5r-resume-idempotence.txt` | Repair after independent verification found the gap |
| 14 | spec-side closure: verification materialized, task table closed, `Planned → Implemented` landed | `c8e73add7`, `f261f6bac` | None |
| 15 | implement independent verification | `test-evidence/implement-verify-verdict.txt` (all PASS; 217 failed / 10042 passed / 0 new vs the 748-name baseline) | None; serial-only crew noted as an efficiency gap (F6) |
| 16 | review round 1 lands both records and `Implemented → Ready for Review`; one artifact P0 (A1) plus two P2 (A2, A3) are recorded, then repaired under driver adjudication | `ed629d558`; `review-105-runtime-store-layout.md` § 2.2, `code-review-20261125T074505Z.md` | Yes — U4 verdict "pass with one artifact P0 → repair + re-review"; the repair round is the prescribed convergence |
| 17 | artifact repair A1–A3: T017 revert drill recorded, note wording replaced by the drill pattern, T017 writeback addendum, DoD status closed, verification `notes=` now names the post-P5R reading | `test-evidence/t017-red-base-drill.txt`; `notes/red-first-evidence.md:194-198`; `writeback/T017.yaml:6`; `tasks.md:26`; `verification.md:111` | Repair (disclosed); each claim re-testable — the drill's restored sha256 equals the current engine (`6007942…e5309`) |
| 18 | review round 2 (this run): A1–A3 re-verified closed; four segments + ARC re-run against `ed629d558`; code segment carried the 262 judged verdicts over the extended range; smoke re-run 11 passed; one in-passing slip (a `receipt` call without `--spec` resolved the trunk tier, exited 2 on an unmeasurable binary, and was re-run with `--spec`; no artifact was written) | this record; `code-review.md`; `test-evidence/t038-smoke.txt` | Yes — the slip is disclosed here and raised as F8 |

## 2. Findings Summary

> Counts cover the process findings (F1–F8) and current artifact findings. Round-1 artifact findings A1 (P0), A2 (P2) and A3 (P2) are **closed** in `ed629d558` and are not re-counted as present defects; their framework recommendations remain in § 5–6. The code segment keeps its own six-level family in `code-review.md` and is not counted here and never converted.

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 7 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 4 |
| Workflow | 3 |
| Documentation | 0 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 23938f22e2af5ac929d1a38274168964030757fc | the resolved diff base |
| Head commit | ed629d5585220fc1363ec6fafbfb3b4b2afdecb0 | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Renderer mode | `renderer: text` | the record's header marker |
| Changed / judged / skipped / gap files | 4357 / 262 / 4095 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `not-evaluated` | skipped files earn no coverage credit (C-37) |
| Gate verdict | `allow` | `report --summary --file code-review.md` exit 0; `important` = 1, `blocking` = 0 |
| Reason, when one applies | `not-evaluated` — 4095 files are generated or non-code (`.specify/` mirrors and command copies, the migration archive, runtime stores, specs, docs) and were skipped with legal reasons; the code verdict covers the 262 judged code files only | |
| Uncommitted scope | 4 paths — this run's own `review.md`, its archive `review-105-runtime-store-layout.md`, and the two feature-entry files it updates (`.specify/features.md`, `.specify/features/024-specification-workspace-versioning.md`); disclosed in the record's receipt block and never concluded over. No product-code path is uncommitted | |
| Record | .specify/specs/105-runtime-store-layout/code-review.md | written because triage = `run` |
| Archive | .specify/specs/105-runtime-store-layout/code-review-20261125T074505Z.md | round-1 record, archived by `start` |

`Implemented → Ready for Review` was judged and landed in round 1 (all four conjunctive conditions held). Round 2 re-checks the same conditions on the current tree and confirms them: every deferred task is resolved (`deferred_tasks=` empty), both review records are on disk, the current code record holds zero `blocking` entries, and no `final`-path criterion is `blocked`/`deferred`/`fail` (6/6 `pass`); no waiver exists and none was needed. The status stays `Ready for Review` — unchanged, never regressed. The single `important` item is answered in the code record's `## 回应` section (agreement, fix named as a follow-up).

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | stage rules plus `plan.md` § Project Structure |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | round-1 findings closed, no new finding |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| — | — | — | — | No artifact findings. Round-1 A1 (P0) is closed by `test-evidence/t017-red-base-drill.txt` (revert → 5 failed, restored sha256-equal, green 5 passed), `notes/red-first-evidence.md:194-198` (drill pattern, no invented discipline) and `writeback/T017.yaml:6`; A2 (P2) is closed at `tasks.md:26` (`**DoD Status**: done`, 43/43 rows `[X]`, 0 open); A3 (P2) is closed at `verification.md:111` (post-P5R verifier reading 217/10042/531 named, pre-P5R T041 snapshot superseded). Tree-wide search for the invented "front-loading-closure" phrase returns zero hits in the live spec artifacts; the remaining hits are the archived round-1 record and dated feedback/state records. |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 23938f22e2af5ac929d1a38274168964030757fc | the resolved diff base |
| Head commit | ed629d5585220fc1363ec6fafbfb3b4b2afdecb0 | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh` reported |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py tests/integration/test_store_layout_migration_us3_us6.py tests/integration/test_init_new_layout.py -q` | recorded verbatim from verification.md |
| Smoke exit code | 0 | the recorded integer; independently re-executed by this review with the same command (11 passed, exit 0) |
| Smoke evidence path | .specify/specs/105-runtime-store-layout/test-evidence/t038-smoke.txt | exists and is non-empty |
| Scope and regression verdict | The delta implements T001–T043 and nothing beyond its declared paths. Relative to the round-1 head `f261f6bac`, the 21 added/modified files are review records, A1–A3 artifact repairs and run-generated exec-quant/session/feedback records — all non-code (`.md`/`.txt`/`.yaml`/`.json`), so the 262 judged code files are byte-identical to the round-1 tree (`git log -3 -- src/specify_cli/__init__.py tests/contract/test_runtime_store_layout.py` shows no commit after `1e6dc208c`). Re-measured by this review: guard contract modules 23 passed, memory/injection modules 12 passed, smoke 11 passed; the post-P5R full-tier reading (217 failed / 10042 passed, `comm -13` NEW=0) is unchanged because no code path changed since the tree that produced it. | this segment's own reading |
| Segment verdict | `pass` | smoke green, guard modules green, no code-path change since the verified tree, scope clean |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| — | — | — | — | No implementation findings: each FR the slice claims has a hunk, the acceptance evidence is the evidence this delta produced, and the regression set is re-measured rather than assumed. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features.md` row 105, as the checker read it |
| `final_path` record, copied verbatim (7/7) | pass 6 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 6 | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/105-runtime-store-layout --json`, never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept`; claim `Ready for Review`; `pass` bucket is 6, not zero |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — GATE-8 names a check its own executor cannot pass

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/test-evidence/t041-final-gate.txt (repo-relative: `.specify/specs/105-runtime-store-layout/test-evidence/t041-final-gate.txt`, lines 29–34); the task-file prohibition is at `.specify/specs/105-runtime-store-layout/handoff.md:44`
- **Evidence** (verbatim quote):

  ```
  == 6. no open/claimed tasks
  grep -cE '^- \[[ >]\]' .specify/specs/105-runtime-store-layout/tasks.md
  43
  reading: all 43 rows are still in the open form at executor hand-back — tasks.md is on this
  seat's forbidden-write list, so row marking and the GATE-8 evaluation belong to the driver
  after it collects the writebacks.
  ```

  ```
  The following MUST stay forbidden to every seat that carries the expansion (C-62): `requirements.md`, `tasks.md`, `verification.md`, `handoff.md`
  ```

- **Why it's problem**: the gate row requires zero open rows, but the handoff contract forbids the executing seat from touching `tasks.md`; the green reading is only produced later, by another seat, and the gate's own evidence file keeps the red one. A later reader of the "final gate" record sees a failing check the driver nevertheless treated as closed.
- **Proposed fix**: split GATE-8 in `skills/internal/implement-feature/SKILL.md` § Completion Gate into an executor-side hand-back check and a driver-side closure check (re-captured into the same evidence path), or require the closing commit to append the re-captured reading.

### F2 — The plan stage can declare itself done without its mandatory Wrap-up

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/03-plan.md:5
- **Evidence** (verbatim quote):

  ```
  - **sentinel**: `PLAN-DONE`; plan attempt 1 was a false-complete candidate (missing Wrap-up), repair attempt 2 produced `PLAN-DONE` with real records
  ```

- **Why it's problem**: the stage sentinel is printed before the six closing steps are accounted for, so "done" can be announced by a run that never wrote its records; catching it costs a bounded repair and a second checkpoint.
- **Proposed fix**: `templates/commands/plan.md` (and the plan skill) assert the compiled Wrap-up steps ran and produced records *before* printing `PLAN-DONE`.

### F3 — New anchors can be created without the engine-owned binding block

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/05-goal-team-activation.md:13
- **Evidence** (verbatim quote):

  ```
  - **anomaly**: Anchor creation omitted the engine-owned binding block. `validate` accepts it as legacy, run-checks pass; this is recorded as F-OBS-4 and not hand-edited.
  ```

- **Why it's problem**: the legacy acceptance path makes a freshly created anchor indistinguishable from a pre-existing one, so the run cannot repair its own definition and must carry an open observation instead of a valid artifact.
- **Proposed fix**: `skills/internal/manage-anchor/SKILL.md` and its engine must write/require the binding block at creation; legacy tolerance should apply only when the file predates the run.

### F4 — A capture step wrote scratch to bare `/tmp`

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/07-analyze.md:12
- **Evidence** (verbatim quote):

  ```
  - **anomaly**: no stage anomaly. One in-passing correction disclosed: a coverage capture was briefly written to bare `/tmp` and removed; no tracked file changed.
  ```

- **Why it's problem**: the temporary-directory discipline forbids bare system temp, and nothing in the capture step steers authors or agents to the sanctioned root; compliance here depended on a later correction that the rule says must not be relied on.
- **Proposed fix**: `templates/commands/analyze.md` and the analyze skill's capture step should resolve `.specify/.tmp/` explicitly and fail fast when it is unavailable, with one guard test.

### F5 — A package commit mixes task work with run-generated feedback entries

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/08-implement.md:23
- **Evidence** (verbatim quote):

  ```
  - **evidence**: serial crew executed five packages + one repair; writebacks 42/42; one broad-staging attribution defect (feedback entries swept into a package commit) disclosed
  ```

- **Why it's problem**: `git log --follow` on the package diff then carries runtime records that no task row asked for, so attribution and later audits have to separate work from noise by hand.
- **Proposed fix**: `.specify/agents/templates/sdd-stage-integrator.agent.md` (and the implement commit discipline) should stage the package's declared write targets explicitly instead of the working tree.

### F6 — Serial-only crew execution left independent packages sequential

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/08-implement.md:24
- **Evidence** (verbatim quote):

  ```
  - **symptom**: serial-only pattern left two dependency-independent packages sequential (efficiency, not correctness)
  ```

- **Why it's problem**: the concurrency obligation defaults to parallel for independent units; here the disjoint write territories existed but the pattern was chosen serial without a recorded reason code, paying wall-clock time for nothing.
- **Proposed fix**: `.specify/agents/templates/sdd-implement-coordinator.agent.md` should partition by write territory and dispatch disjoint packages concurrently after the isolation preconditions, recording the reason code when it stays serial.

### F7 — The tasks stage has no named lane for a mid-run requirements addendum

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/105-runtime-store-layout/checkpoints/04-tasks.md:10
- **Evidence** (verbatim quote):

  ```
  - **anomaly**: original tasks validation had two warnings; both were corrected by the addendum reconciliation. The mid-run user addendum is recorded verbatim in requirements Clarifications and is now fully integrated upstream-first. It has not been treated as a second run; no extra stage command was opened.
  ```

- **Why it's problem**: the user's addendum ("需要将所有不向前兼容的修改都在speckit.migrate命令中添加迁移逻辑") forced an improvised requirements → plan → contracts → tasks reconciliation with every gate re-run; because no lane or order is prescribed, the handling depends on driver judgment and the first validation pass left two warnings.
- **Proposed fix**: `templates/commands/tasks.md` should define a named "requirements addendum" subsection: record verbatim in Clarifications, reconcile upstream first in the fixed order, then re-run every stage gate before regenerating tasks.

### F8 — `receipt` silently re-resolves the trunk tier when `--spec` is omitted

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh (repo-relative: `skills/internal/code-review/scripts/git-delta-review.sh`, `cmd_receipt`); synopsis at `skills/internal/code-review/SKILL.md` § 非交互路径 step 4
- **Evidence** (verbatim output; first command read-only, second the composed-path slip corrected in passing this run):

  ```
  $ bash skills/internal/code-review/scripts/git-delta-review.sh base
  base=926836e0fc931bfdbd531f45b0b27e3715e84a0c
  head=ed629d5585220fc1363ec6fafbfb3b4b2afdecb0
  base_source=trunk-merge-base
  exit=0
  ```

  ```
  行数无法测量 (binary): .specify/anchoring/command-logic-as-classified-skills/summary/assets/wbs.png
  不可量测的数字字段意味着不写块 (C-41 / V16)
  ```

- **Why it's problem**: the composed code segment resolves the feature range in steps 1–2 (`base --spec`, `start --spec`), but the skill's step‑4 synopsis shows only `receipt --review-file <record>`, and `receipt` re-resolves independently. When `--spec`/`--since` is omitted it falls to the `trunk-merge-base` tier and exits 0 — a wrong-range resolution, not a refusal. This run escaped a wrong-range receipt only because some file in that larger range was binary and unmeasurable (exit 2, no block written); a wrong range without such a file would have written a receipt whose base/head disagree with the record header, and nothing in the path compares the two.
- **Proposed fix**: `receipt` should compare the resolved `base`/`head` with the record header's `**基准**`/`**目标**` values and exit 2 on mismatch (a deterministic guard, no new option); the skill's step‑4 synopsis should carry `--spec <dir>` like steps 1–2.

## 4. What Worked — Preserve (Brief)

- One machine declaration (`shared/declarations/facts/runtime-store-layout.yaml`) with a guard that asserts declaration = requirements table = code consumer set (`tests/contract/test_runtime_store_layout.py:232`).
- Manifest-first relocation: digest per entry, resume rows verified against recorded digests, superseded non-content duplicates recorded before removal, archive-first retained for replacement dimensions.
- Refusal classes that name both paths and delete nothing (`dual-content`, `unknown-residue`, `symlink-*`, `permission-denied`, `path-collision:<relpath>`), with mutation drills proving each guard red.
- Live-reference containment measured = declared in both directions, with a pinned four-file allowlist and four mutation drills (`test-evidence/mutation-drill.md`).
- Red-first evidence log with real command/output/exit for the modules that could go red, plus a red→green drill for P5R and a revert drill for T017 whose restore checksum still matches the shipped engine (`6007942…e5309`).
- Independent implement verification (fresh context) plus a deterministic closure checker (`accept`, `final_path` 6/6) before any status flip.
- Round-1 records archived before round-2 writing, and the code segment's carried-verdict model: 262 judged files carried over an extended head while the receipt re-proved set equality (262 / 4095 / 0).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Name the DoD Status updater** — Target: `templates/tasks-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md`). Change: either add the DoD Status row to the implement close-out (driver-side, since the crew may not edit `tasks.md`) or drop the field and let `verification.md` own the close-out state. Source: A2 (closed locally at `tasks.md:26`; the template gap remains). Expected impact: a closed slice stops carrying a contradicting status literal.

### 5.2 Command Prompt Improvements

- **Split GATE-8 ownership** — Target: `templates/commands/implement.md` and `skills/internal/implement-feature/SKILL.md` § Completion Gate (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`, `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`). Change: give the task-count gate an executor-side hand-back form and a driver-side closure form, and require the closing commit to append the re-captured reading to the gate evidence. Source: F1. Expected impact: no "final gate" record contains a red check its reader must know was resolved elsewhere.
- **Add a named addendum lane** — Target: `templates/commands/tasks.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md`). Change: define the verbatim-record / upstream-first-reconcile / re-gate order for a mid-run requirements addendum. Source: F7. Expected impact: addenda stop depending on driver improvisation and stop leaving validator warnings behind.

### 5.3 Automation / Script Improvements

- **Guard the plan sentinel on the Wrap-up** — Target: `skills/internal/create-plan/SKILL.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-plan/SKILL.md`). Change: assert the six closing steps produced records before the stage sentinel is printed. Source: F2. Expected impact: false-complete plan runs are impossible rather than merely detectable.
- **Write the binding block at anchor creation** — Target: `skills/internal/manage-anchor/SKILL.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/manage-anchor/SKILL.md`). Change: creation writes or requires the engine binding block; legacy tolerance applies only to files predating the run. Source: F3. Expected impact: new anchors stop shipping with an open observation.
- **Resolve the sanctioned temp root in captures** — Target: `templates/commands/analyze.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md`). Change: every capture resolves `.specify/.tmp/` explicitly and fails fast when it cannot. Source: F4. Expected impact: bare `/tmp` usage becomes a mechanical impossibility, not a correction.
- **Pin the receipt range to the record header** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (`cmd_receipt`) and `skills/internal/code-review/SKILL.md` § 非交互路径 step 4 (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`, `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/SKILL.md`). Change: `receipt` exits 2 when the resolved base/head differ from the record header's `**基准**`/`**目标**`, and the step‑4 synopsis names `--spec <dir>`. Source: F8. Expected impact: a wrong-range coverage receipt becomes impossible rather than merely detectable.

### 5.4 Workflow Improvements

- **Red-first under front-loading = drill or correction, never an invented discipline** — Target: `skills/internal/implement-feature/SKILL.md` § Test runs and `skills/internal/create-tasks/SKILL.md` § red-first obligations (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`, `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md`). Change: when a subject lands before its test, require a mutation or revert drill (the US6/T042 pattern) or correct the task's red-first claim; forbid justifying a deviation with a discipline name that no owner document defines. Source: A1 (closed locally by the T017 revert drill; the framework rule gap remains). Expected impact: red-first claims stay evidence-shaped, and invented authorities stop spreading.
- **Stage explicit paths in the integrator** — Target: `.specify/agents/templates/sdd-stage-integrator.agent.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/agents/templates/sdd-stage-integrator.agent.md`). Change: commits stage the package's declared write targets, never the whole working tree. Source: F5. Expected impact: package diffs stop carrying run-generated records.
- **Partition by write territory before choosing serial** — Target: `.specify/agents/templates/sdd-implement-coordinator.agent.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/agents/templates/sdd-implement-coordinator.agent.md`). Change: dispatch disjoint packages concurrently after the isolation preconditions, recording a serial reason code otherwise. Source: F6. Expected impact: independent work stops paying serial wall-clock.

### 5.5 Documentation Improvements

- **Close-out notes name the run they quote** — Target: `templates/verification-log-template.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`). Change: a `notes=` line that quotes a regression reading names the command or run identifier that produced it, and names only one reading per quantity. Source: A3 (closed locally at `verification.md:111`; the template gap remains). Expected impact: two final-looking readings can no longer coexist unattributed.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Red-first under front-loading: drill or correction, never an invented discipline (round-1 finding A1, closed locally; framework gap remains) | `skills/internal/implement-feature/SKILL.md` § Test runs; `skills/internal/create-tasks/SKILL.md` | A1 (closed) |
| P1 | Split GATE-8 ownership between executor hand-back and driver closure | `templates/commands/implement.md`; `skills/internal/implement-feature/SKILL.md` | F1 |
| P2 | Pin the receipt range to the record header and name `--spec` in step 4 | `skills/internal/code-review/scripts/git-delta-review.sh`; `skills/internal/code-review/SKILL.md` | F8 |
| P2 | Name the DoD Status updater (or drop the field) | `templates/tasks-template.md` | A2 (closed) |
| P2 | Add a named requirements-addendum lane to the tasks stage | `templates/commands/tasks.md` | F7 |
| P2 | Guard the plan sentinel on the Wrap-up | `skills/internal/create-plan/SKILL.md` | F2 |
| P2 | Write the binding block at anchor creation | `skills/internal/manage-anchor/SKILL.md` | F3 |
| P2 | Resolve the sanctioned temp root in captures | `templates/commands/analyze.md` | F4 |
| P2 | Stage explicit paths in the integrator | `.specify/agents/templates/sdd-stage-integrator.agent.md` | F5 |
| P2 | Partition by write territory before choosing serial | `.specify/agents/templates/sdd-implement-coordinator.agent.md` | F6 |
| P2 | Close-out notes name the run they quote | `templates/verification-log-template.md` | A3 (closed) |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file (A1–A3 quote their closure evidence in the § 2.2 row).
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: no P0 findings were raised in round 2; the P0 independent-validation pass is vacuously satisfied. (Round-1's P0 — A1 — was validated by direct re-read of `tasks.md:205`, `notes/red-first-evidence.md:182-201` and a tree-wide search for the cited discipline, because the review assignment prohibits dispatching another agent; it is closed in round 2 and not re-counted.)

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
