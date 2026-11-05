# Specification-Driven Development (SDD) Process Review Report: Harness 三重结构（markdown + yaml + script）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 084 |
| Requirement Key | 084-harness-triple-structure |
| Requirement Name | Harness 三重结构（markdown + yaml + script） |
| Related Feature | 084 Harness 三重结构（markdown + yaml + script） |
| Repository | spec-kit (`git rev-parse --show-toplevel` → `/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | `(no publishable HTTPS remote)` — remotes are `gitee`/`github`/`gitlab` (SSH) plus `origin` = `git@github.com:github/spec-kit.git` (upstream; it does not contain these commits) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch was never pushed. Every citation in this report is an absolute path plus `git show 03a19487:<path>` recovery |
| Branch | `084-harness-triple-structure` |
| Commit SHA | `03a19487e4ceb668e27ef1a4554aff82e4dc8a4c` (short: `03a19487`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-05 |
| Reviewer (Agent) | SDD Executor (fresh dispatch; same-author detection delegated per `shared/workflow/objective-analysis-gate.md`) |
| Environment | Linux, bash, CPython 3.11.13, `pytest 9.2.0` pin (EP-001), no subagent-dispatch capability in this topology |
| spec-kit Source Snapshot | this repository at `03a19487` (self-hosting: `.specify/` is the same flow every client project runs) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|------------------|
| requirements.md | 285 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/requirements.md` | 19 FR / 6 SC / 14 STR, A1–A10 adjudications, scope criteria D1∧D2 |
| plan.md | 434 | `…/084-harness-triple-structure/plan.md` | 18/18 Constitution Check, 4 decision tensions, EP-001…EP-007, D1–D13, Project Structure |
| tasks.md | 261 | `…/084-harness-triple-structure/tasks.md` | 32 rows (all `[X]`), 7 phases, GATE-1…7, § Traceability 32 rows |
| verification.md | 133 | `…/084-harness-triple-structure/verification.md` | baseline block, one smoke record, six SC status rows, joint-acceptance rows |
| contracts/ (5 files) | 426 | `…/084-harness-triple-structure/contracts/` | C-001…C-059, `md-bold-closed` (verified: 12+13+16+10+8 = 59) |
| data-model.md | 169 | `…/084-harness-triple-structure/data-model.md` | E-1…E-10 + six fixture families |
| quickstart.md | 152 | `…/084-harness-triple-structure/quickstart.md` | S1…S8 (4 measured, 4 route-(b)) |
| research.md | 157 | `…/084-harness-triple-structure/research.md` | R1–R10 measured readings |
| feature-ref.md | 42 | `…/084-harness-triple-structure/feature-ref.md` | bound Feature 084 + status movement |
| code-review.md | 370 | `…/084-harness-triple-structure/code-review.md` | this run's code segment record (2 blocking, 2 important, 2 suggestion, 1 nitpick, 1 praise) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements attempt 1 exhausted its 40-turn budget with a scaffold only | state spine § U5 重试记录; branch created, template unfilled | **Yes** — retried as attempt 2 under a 120-turn executor |
| 2 | requirements / clarify / plan / tasks / checklist | `a94c3945` → `cd446a6e` → `171c2ff8` → `4b65517c` → `5dc5919a`/`8ed70a87` → `9abb10fb` | No |
| 3 | analyze round 1: 1 CRITICAL + 2 HIGH | `test-evidence/analyze-report-2026-11-05.md`; fixes `fd84ed63`/`9284c789`/`2b18485e` | No — one bounded loop as prescribed |
| 4 | analyze round 2: still HIGH (R2-02) → **U5 halt** | `test-evidence/analyze-report-round2-2026-11-05.md`; spine § U5 停线上送 | No — the halt is the prescribed disposition |
| 5 | user ruling **path A** → plan reopen (substantive) + analyze round 3 green | `ba141671`, `b1b19e93`; `analyze-report-round3-2026-11-05.md` | Deviation **authorized by explicit user ruling** |
| 6 | implement Part 1–2d (5 dispatches, one partial at 120 turns) | `e3e0af68`…`3f4d9b1b`, `1da7a88d` | **Yes** — attempt 1 stopped at T012, re-split into 2a/2b |
| 7 | user test waiver 2026-11-05: no pytest, no smoke, no scratch proofs | spine § 最终状态; `tasks.md` § Notes 202-205 | Deviation **authorized by explicit user ruling** |
| 8 | Part 4/5 closed T020–T031 under the waiver; Feature → `Blocked` | `1e4ca01e`; `verification.md` header (pre-`03a19487`) | No — `Blocked` was the honest landing |
| 9 | classification slice T032: 58 unclassified → 0 | `94d9db33`, `e185da6c`; `t032-classification-readings-2026-11-05.txt` | No — follows user path A |
| 10 | user-authorized final test budget: contract module 68 passed, residual face pass, smoke twice | `03a19487`; `final-contract-module.txt`, `final-duplicate-face.txt`, `smoke-run1/2-2026-11-05.txt` | No |
| 11 | Feature flipped `Blocked → Implemented` in the **same** commit | `03a19487` diff: `features.md` `\| Blocked \|` → `\| Implemented \|` | **Yes** — condition ④ was asserted from prose; the owner checker reports it unsatisfied (F1) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 3 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 7 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 4 |
| Command Prompt | 1 |
| Automation / Scripts | 1 |
| Workflow | 6 |
| Documentation | 4 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `03a19487e4ceb668e27ef1a4554aff82e4dc8a4c` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 276 / 39 / 237 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `blocked` | the record carries 2 `blocking` entries |
| Gate verdict | `blocking-unresolved` | `report --summary --file …` exits 1 with 2 `[blocking]` |
| Reason, when one applies | none | a `blocked` verdict needs no basis line |
| Uncommitted scope | disclosed, never concluded over: this run adds only `code-review.md` and `test-evidence/review-smoke-2026-11-05.txt`; a pre-existing modified run record `session/20261102T231648Z-…-081a.md` and pre-existing untracked `memory/` records are outside the slice and were left untouched | same sentence in [`.specify/specs/084-harness-triple-structure/code-review.md`](/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md) |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` | written (triage `run`) |
| Archive | `none` | first run for this slice |

Six-level counts in the record: `blocking` 2 · `important` 2 · `suggestion` 2 · `nitpick` 1 · `question` 0 · `praise` 1. The two `blocking` entries are: (1) the declared closed set `flow-class-classes` still has an inline copy in three engines the declaration does not name as consumers, and (2) `success-criterion-path-values` is read for the membership verdict while three comparison sites re-spell its member `final`. The two `important` entries are the FR-012 fallback-vs-delete split and `verify`'s non-reading `residual_literals` field. The findings themselves are read there; this subsection carries the verdict and the pointers only.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | derived: the standard spec-stage set ∪ `plan.md` § Project Structure § Documentation (which declares `research.md` and `feature-ref.md` in addition) — **9 members** |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | two `P0` acceptance-honesty findings |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `.specify/specs/084-harness-triple-structure/verification.md` | 55 | none | Smoke record is not machine-parseable, so the feature's `Implemented` claim does not survive its own checker (F8) |
| P0 | `.specify/memory/features.md` | 90 | none | One row carries two statuses for one feature: `Implemented` in the column, `Blocked` at the end of its own narrative (F9) |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 91 | none | `SC-004_status=pass` rests on a stale 12-row reading while the same file's SC-002 says 70 rows (F10) |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 132 | none | `notes_feature_status=Blocked` contradicts the file's own header (`Implemented`) (F11) |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 21 | none | The datum labelled "recorded at implement start" is a Part-3 commit, so the comparison anchors SC-005/SC-006 rest on cannot be trusted (F12) |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 26 | none | `DoD Status: pending` with all 32 rows `[X]` and the feature `Implemented`; no surface reconciles the two (F13) |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `03a19487e4ceb668e27ef1a4554aff82e4dc8a4c` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | as the code skill's `git-delta-review.sh` reported it |
| Smoke command | `python3 scripts/python/harness-triple-check.py --action coverage` (run twice, byte-compared) | recorded verbatim |
| Smoke exit code | `0` | the integer the command returned, both runs |
| Smoke evidence path | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/test-evidence/review-smoke-2026-11-05.txt` | exists, non-empty; holds both runs, the `cmp` exit and the two sha256 values |
| Scope and regression verdict | scope clean (no work without a row); regression clean on the surfaces that were read — `sync-mirrors.py --check` exit 0 with six pairs `ok` (templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 121 / shared 89), `git diff 4b65517c -- pyproject.toml` empty, `git diff -​-stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` empty | the segment's own reading |
| Segment verdict | `blocked` | the delta does not deliver the property its requirements state (F14) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/closure-acceptance-check.py` | 223 | none | The delta does not deliver "one machine-read copy" for two declared closed sets; the detail and the two extra files are in `code-review.md` (F14) |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 56 | none | The two-run byte-identity claim SC-001 (i) requires has no legal carrier in the log format, so the implementer overloaded the evidence path (F15) |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 165 | none | The distribution limb (T030) and the legacy-degradation limb (T022) were never read, so client-project behaviour is unverified (F16) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `features.md` row 084 and `features/084.md` `**Status**` |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 1), never recomputed here |
| Comparison verdict | `refused` | the checker's verdict is `block` while the claim is `Implemented` |
| Failed condition, on refusal | completion condition ④ `smoke_record_pass = false` — the checker reports `evidence_exists: false` and `exit_code: "0 (both runs)"`; its reason record is `status-claims-implemented-but-blocked` | `completion_conditions.smoke_record_pass` and `reasons[0].code` in the same JSON |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 2 |

**The transition is refused and the status stays `Implemented`.** A refusal is not a downgrade: no surface is written back, and the feature is not presented as having completed review. The user's test waiver for the *test* budget does not lift this refusal — it is recorded here as residual risk and the item still fires.

## 3. Findings (Problems & Improvement Targets)

### F1 — The implement gate asserted completion condition ④ from prose, not from the checker that owns it

- **Severity**: P0 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md` lines 55–56; owner check `scripts/python/closure-acceptance-check.py`
- **Evidence** (verbatim quote):

  ```
  smoke_exit_code=0 (both runs)
  smoke_evidence_path=.specify/specs/084-harness-triple-structure/test-evidence/smoke-run1-2026-11-05.txt; .specify/specs/084-harness-triple-structure/test-evidence/smoke-run2-2026-11-05.txt (byte-identical, cmp exit 0)
  ```

  against the checker's own reading of the same file:

  ```
  "completion_conditions": { "smoke_record_pass": false, ... }
  "reasons": [ { "code": "status-claims-implemented-but-blocked", "target": "" } ]
  "verdict": "block"
  ```

- **Why it's a problem**: the four conditions of `Planned → Implemented` are machine facts with a single program that answers them. The run wrote them into prose, believed the prose, and flipped the status. The smoke *did* run and did pass (this review reproduced it: two runs, exit 0, `sha256 f9cd934a…3473` on both) — which makes the failure worse, not better: a true fact recorded in an unreadable shape produced a false status, and nothing in the flow went red.
- **Proposed fix**: `templates/commands/implement.md` § status flip MUST route through `python3 scripts/python/closure-acceptance-check.py --spec-dir <spec> --json` and copy its `verdict`; a prose self-assessment MUST NOT be the input. The copy slot is the verification log's smoke block.

### F2 — Two closed task rows name evidence carriers that do not exist

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md` lines 31 and 166
- **Evidence** (verbatim quote):

  ```
  - GATE-2: … check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt -q`, then `comm -13 <implement-start baseline> head-failed.txt` prints nothing
  ```

  ```
  - [X] T031 … Run `quickstart.md`'s S5–S8 on the final tree and record the real output in `notes/quickstart-run.md`
  ```

  `ls .specify/specs/084-harness-triple-structure/notes/` returns only `pre-change-measurements.md` and `red-first-evidence.md`; `test-evidence/head-failed.txt` does not exist.
- **Why it's a problem**: a `[X]` row whose named carrier is absent is indistinguishable from a row closed by assertion. The waiver is recorded honestly in § Notes, but the row state itself does not carry it, so the *only* machine-readable signal (the `[X]`) says "done".
- **Proposed fix**: give `validate-tasks.py` (or the implement gate) a carrier-existence leg: a row that names a repo-relative output path MUST have that path present when it is `[X]`, or carry an explicit `waived-by-user` token in the row.

### F3 — One count drifted across four surfaces inside the feature that removes drift

- **Severity**: P1
- **Category**: Workflow
- **Location**: `verification.md` line 91, `.specify/memory/features/084.md` § Latest Review (implement entry), `.specify/memory/features.md` line 90, `tasks.md` line 203
- **Evidence** (verbatim quote):

  ```
  SC-004_value=12 exclusion rows in 2 reason files (`no-machine-fact` 10 rows, `no-harness-asset` 2 rows); `by-owner-decree` 0 rows …
  ```

  against the same file's SC-002 row and the tree:

  ```
  SC-002_value=… 70 exclusion rows (13 in-scope / 70 excluded / 0 unclassified) …
  ```

  ```
  $ grep -c "^- unit:" shared/declarations/exclusions/*.yaml
  shared/declarations/exclusions/no-harness-asset.yaml:32
  shared/declarations/exclusions/no-machine-fact.yaml:38
  ```

- **Why it's a problem**: T032 appended 58 rows after those three surfaces were written, and only `verification.md`'s SC-002 was updated. The feature's own thesis is that a value restated in several places drifts and nobody notices — and its own records demonstrate it. SC-004 is still `pass` on the stale number.
- **Proposed fix**: derive the count in the report (`harness-triple-check.py --action coverage` already prints `excluded`) and let every prose surface point at that reading instead of restating a number.

### F4 — The new delegation cannot be default-on because an existing closed assertion forbids a new finding name

- **Severity**: P2
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (module docstring, `--triple-structure`)
- **Evidence** (verbatim quote):

  ```
  * **One subprocess call — the judging engine** (``scripts/python/harness-triple-check.py``). It runs
    only when ``--triple-structure`` is passed, once per run, and each finding line it prints is
    forwarded verbatim under the single check name ``triple-structure``. The flag defaults **off** by
    measurement rather than taste: an existing 081 assertion closes the set of finding *names* a stage
    run may produce, so a default-on delegation would turn it red (plan D8 / `T-003`).
  ```

- **Why it's a problem**: a gate that should catch the feature's regressions cannot be reached without an opt-in flag nobody passes, because a *closed set* in an older test forbids growth. Closing a set is the right move; closing it so that later stages cannot add a name is a treadmill that every future gate improvement will hit.
- **Proposed fix**: let the closed set name its growth procedure (a declared roster, which this very feature now provides as `driver-gate-roster`) instead of a literal tuple in `tests/contract/test_acceptance_premises.py`, then default the delegation on.

### F5 — A contract clause asks `verify` for a reading another clause forbids it to perform

- **Severity**: P2
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/contracts/harness-triple-check.contract.md` C-032 and C-038
- **Evidence** (verbatim quote):

  ```
  - **C-032** **`--action verify`** judges declaration completeness only: … and residual literals via the reused `duplicate-fact` reading.
  ```

  ```
  - **C-038** No model judgement, no network, no subprocess, no environment-dependent branch …
  ```

  and the implementation's answer, `scripts/python/harness-triple-check.py:440`:

  ```
  "residual_literals": "delegated: doc-consistency-check.py --faces duplicate "
                       "(this engine opens no subprocess and never re-scans)",
  ```

- **Why it's a problem**: the two clauses cannot both hold in one runtime. The implementer chose the clause that yields a green and documented the choice — honest, but `verify` now exits 0 having printed a constant where a reading was promised, which is the "green that would not go red" shape.
- **Proposed fix**: drop the residual-literal conjunct from C-032 and name the separate `doc-consistency-check.py` run as that fact's carrier, or add an explicit `residual-literals: not-evaluated` state so a green cannot be over-read. Whichever is chosen, pin it in the contract so the next implementer does not choose again.

### F6 — Same-author detection could not be delegated in this topology

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md` (rule 7 fallback) vs the local dispatch topology
- **Evidence** (verbatim quote):

  ```
  * **Subagent-unavailable fallback**: if the validation subagent dispatch fails twice in a
    row (upstream error), a direct evidence re-read by the reviewing agent MAY substitute;
  ```
  (`.specify/skills/internal/review-sdd-process/SKILL.md` § 5 — the applicable fallback shape)
- **Why it's a problem**: the artifacts under review were produced by the same agent lineage that reviews them, and the topology has no dispatch. The gate's own escape hatch was used, and every P0 in this report therefore carries "(validated: direct re-read, subagent unavailable)". That is weaker evidence than the gate intends, and it is invisible unless this line is read.
- **Proposed fix**: make the fallback visible on the report itself (a required field in `templates/review-template.md` § Findings Summary: `P0 validation path: subagent | direct re-read`), so a reader can weight the P0s without reading the skill.

### F7 — The code-review skill states a five-step path; its own script help states four

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/code-review/scripts/git-delta-review.sh` (help text) vs `SKILL.md` § 非交互路径
- **Evidence** (verbatim quote):

  ```
    NON-INTERACTIVE PATH (four steps, in this order — four, never three):
      1. base      resolve the range: base= head= base_source=
      2. start     record creation and rotation (required from the second run on)
      3. note      append opinions (repeatable, one call per opinion)
  ```

  while `SKILL.md` says「**非交互路径（Agent / CI：五步，不是四步）**」 and step 5 is `capture`. `capture` exists in the same script (`cmd_capture`, line 1277).
- **Why it's a problem**: the help text is the surface an agent or a maintainer reads first when a step fails, and it contradicts the owner. This is pre-existing (the slice does not touch this script) but it is the exact defect class the slice removes: one fact, two surfaces, no reader notices.
- **Proposed fix**: regenerate the help's step list from the same closed enumeration the skill uses, or delete the numbered list from the help and point at the skill section.

### F8 — The smoke record has no machine-parseable shape, so condition ④ cannot be read

- **Severity**: P0 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md` lines 54–57
- **Evidence** (verbatim quote):

  ```
  smoke_command=python3 scripts/python/harness-triple-check.py --action coverage (run twice)
  smoke_exit_code=0 (both runs)
  smoke_evidence_path=.specify/specs/…/smoke-run1-2026-11-05.txt; .specify/specs/…/smoke-run2-2026-11-05.txt (byte-identical, cmp exit 0)
  ```

- **Why it's a problem**: the owner says `smoke_exit_code` is `0` and `smoke_evidence_path` is *a repo-relative path to a file that exists and is non-empty*. Both values here are annotated prose. `evaluate_smoke()` compares `exits[0].strip() != "0"` and resolves the path with `Path(rel).is_file()`; both fail, so `smoke_record_pass=false` and the whole feature is `block`. The template gives no slot for "two runs compared byte for byte", which is what SC-001 (i) actually requires — so the implementer improvised inside a field whose grammar is fixed.
- **Proposed fix**: add a `smoke_comparison=` field (or let `smoke_evidence_path` name one comparison transcript) to `templates/verification-log-template.md`, and state in the template that the three smoke values may contain no annotation.

### F9 — One features.md row carries two statuses for one feature

- **Severity**: P0 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/features.md` line 90
- **Evidence** (verbatim quote, from the same physical line):

  ```
  | 084 | Harness 三重结构（markdown + yaml + script） | … | Implemented | .specify/memory/features/084.md | …
  ```

  ```
  … ⇒ 状态机条件 (3)(4) 不成立，故落 `Blocked`，不写 `Implemented`|
  ```

- **Why it's a problem**: `03a19487` changed the `Status` column and left the `Last Updated` narrative untouched, so the row asserts both. A reader — or a program that greps the narrative — gets whichever value it looks at first. This is the state the feature's own thesis calls impossible to drift.
- **Proposed fix**: the flip commit must rewrite the narrative in the same edit; `validate-features`-style check (or a contract test) should assert that a row's narrative ends with the same status the column carries.

### F10 — A `pass` row rests on a stale reading

- **Severity**: P1
- **Category**: Documentation
- **Location**: `verification.md` line 91
- **Evidence** (verbatim quote):

  ```
  SC-004_status=pass
  SC-004_value=12 exclusion rows in 2 reason files (`no-machine-fact` 10 rows, `no-harness-asset` 2 rows); `by-owner-decree` 0 rows …
  ```

- **Why it's a problem**: the reading was true when T020 closed and false after T032 wrote 58 more rows. Nothing re-read the row, and `pass` is the value an acceptance reader trusts. The criterion's own mechanical limbs still hold on the final tree (70 rows, all reasons in the closed set, all 70 anchors resolving, 0 `exclusion-anchor-unresolvable` per this run's coverage), so the *verdict* is right and the *value* is wrong — the most misleading of the two failures.
- **Proposed fix**: a `pass` row whose value names a count MUST carry the command that produced it and the commit it was read at, and the implement gate should re-read any row whose `SC-*_verified_at` predates `HEAD`.

### F11 — verification.md contradicts itself about the feature's status

- **Severity**: P1
- **Category**: Documentation
- **Location**: `verification.md` line 132 vs lines 10–16
- **Evidence** (verbatim quote):

  ```
  notes_feature_status=Blocked — reason `test-waiver: final-path evidence waived-by-user`. Conditions (3) and (4) of `Planned → Implemented` fail: SC-001 and SC-002 are `final`-path rows that are not `pass`, and the smoke record was not run.
  ```

  against the same file's header, rewritten in `03a19487`:

  ```
  Consequence: the feature is **`Implemented`**. … The smoke record is complete (two byte-identical coverage runs, exit 0).
  ```

- **Why it's a problem**: `03a19487` updated the header and the smoke block but left the notes line at the pre-flip reading, so the file states both. This is precisely where a later auditor looks for "what did the run think at the end".
- **Proposed fix**: same as F9 — a status flip is one edit across every surface that states it, and the surfaces should be enumerable (the feature detail, the index row, the log's notes line).

### F12 — The baseline datum is labelled "implement start" but is a Part-3 commit

- **Severity**: P1
- **Category**: Documentation
- **Location**: `verification.md` lines 21 and 39
- **Evidence** (verbatim quote):

  ```
  # -- Baseline (recorded at implement start, before any work changed the tree) --
  baseline_commit=98288d45
  ```

  ```
  post_change_commit=98288d45 (this segment's commit is the one carrying these files; recorded here as the parent-inclusive working tree)
  ```

  `git log --oneline` shows `98288d45 feat(084): migrate the ARC and record-schema facts (T015-T019)` — Part 3, not implement start.
- **Why it's a problem**: SC-005 and SC-006 both say "relative to the baseline captured in `notes/pre-change-measurements.md`" and this block is the log's copy of that anchor. A baseline that is silently a mid-implement commit makes every "no NEW drift" claim vacuous, and no reader can tell without cross-checking git.
- **Proposed fix**: the baseline block's commit should be copied mechanically from the state spine's `E2` slot (T001's tree), and a mismatch between the label and the commit's position in the branch should fail a check.

### F13 — `DoD Status: pending` survives a fully closed, `Implemented` feature

- **Severity**: P2
- **Category**: Template
- **Location**: `tasks.md` line 26
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: pending
  ```

  with `grep -cE '^- \[[ OX]\]'`-style reading of the same file: 32 rows, all `[X]`, and `features.md` = `Implemented`.
- **Why it's a problem**: under the test waiver the DoD rows genuinely are not satisfied (DoD-4's "zero new failures", DoD-7's distribution reading), so `pending` is honest — but nothing links that value to the status machine, so a feature can be `Implemented` while its own DoD block says it is not. One of the two values must be wrong, and the reader has no rule to decide which.
- **Proposed fix**: state in `templates/tasks-template.md` whether `DoD Status` is an input to the status machine; if it is not, say so where the status rows are defined, so the divergence is a documented one instead of a contradiction.

### F14 — The delta does not deliver one machine-read copy for two declared closed sets

- **Severity**: P1
- **Category**: Template
- **Location**: `scripts/python/closure-acceptance-check.py:223`, `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:332`, `scripts/python/validate-requirements.py:99`, `scripts/python/closure-acceptance-check.py:916/939/1347`, `scripts/python/validate-requirements.py:395`
- **Evidence** (verbatim quote):

  ```
  FLOW_CLASSES = ("execution", "expression")
  ```
  (two engines, neither named in `shared/declarations/facts/flow-class-classes.yaml`, whose `consumers:` list is exactly `scripts/python/flow-class-check.py`)

  ```
  if path != "final":
  ```
  ```
  if criteria[sc_id] == "final" and _first_status(statuses, sc_id) != FINAL_PATH_PASS_BUCKET
  ```
  (three sites in an engine that the `success-criterion-path-values.yaml` `consumers:` list *does* name)

- **Why it's a problem**: migration contract C-042/C-044 enumerate a fact's carrier and *one* engine side, and T012's row literally instructs "delete `CLASS_VALUES` … from `scripts/python/flow-class-check.py`". Enumerating by carrier makes the roster complete-looking while three engines keep the same value; reading the declaration for the membership verdict while re-spelling the member at the branch sites makes the read cosmetic. Add one legal member to `flow-class-classes.yaml` and `flow-class-check.py` accepts it while two gates still refuse it — falsifying US2 acceptance scenario 2 and SC-002's property, and nothing in the tree measures it (the contract module asserts membership rejection, not the absence of surviving literals; the tests that would have noticed were waived).
- **Proposed fix**: derive the migration roster by `grep` over each fact's *values* across `scripts/` + `skills/` (the roster row then lists every hit, not the one the plan author remembered), and add a leg to `harness-triple-check.py --action verify` that fails when a declared fact's member literal appears in an engine that is not in `consumers`.

### F15 — The two-run claim SC-001 (i) requires has no legal carrier

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `tasks.md` line 129 (T018) and `verification.md` line 56
- **Evidence** (verbatim quote):

  ```
  - [X] T018 … capturing the full stdout/stderr, exit code and duration of **both** runs (single-run evidence discipline: the record is the evidence, a re-run is not): the two runs are byte-identical
  ```

  while the log format offers exactly one `smoke_command` / `smoke_exit_code` / `smoke_evidence_path` triple.

- **Why it's a problem**: the requirement (determinism, proven by comparing two runs) and the carrier (one three-field record) are one field short, so every implementer of this requirement will improvise in the same place and break the same parse. The report's own P0 (F8) is what that looks like downstream.
- **Proposed fix**: name a second evidence path per comparison in the plan/tasks row *and* give the log a field for it (F8's fix), so the requirement has one legal encoding.

### F16 — The client-project limbs of SC-005 never ran

- **Severity**: P2
- **Category**: Workflow
- **Location**: `verification.md` lines 95–102 (SC-005) and `tasks.md` line 165 (T030)
- **Evidence** (verbatim quote):

  ```
  SC-005_why_reduced_insufficient=mirrors prove the framework source and this repo's `.specify/` copy agree; they say nothing about what a *client project* receives from `specify init`, which is the limb the criterion names
  ```

- **Why it's a problem**: the feature's whole point is that a *client project* receives the layer and degrades honestly without it. Both readings are scratch-tree proofs and both were waived, so the only thing this feature changed for clients (`specify init` distribution and the degraded path) has zero measured evidence — and the row that says so is buried under a `partial`. This review confirmed the six mirror pairs are identical (`sync-mirrors.py --check` exit 0) and that the degraded path is *absent* from the source readings, which does not substitute.
- **Proposed fix**: treat the distribution limb as its own criterion with its own `Path: final` if it matters (it does — it is the product's only client-facing change), instead of folding it into a `supporting` row that can be `partial` forever.

## 4. What Worked — Preserve (Brief)

- The `Blocked` landing at `1e4ca01e`: the run wrote `Blocked` and said "no test evidence", instead of rounding a waived suite up to a pass.
- `test-evidence/` as the run's own archive: 32 transcripts with commands, exit codes and durations, so this review could re-read rather than re-run.
- The U5 halt at analyze round 2 and the escalation with two named paths — the loop stopped at the quality gate rather than choosing a reading for the user.
- `analyze`'s enumerated findings with per-round reports retained (three rounds, all on disk) — the loop's history is reconstructible.
- The declaration layer's own error discipline: `DeclarationError` carrying a finding id, `absent_label()` as the one rendering of `STR-014`, and `flow-class-check.py`'s refusal to judge against an absent closed set (exit 2 with the labels) instead of running on an empty tuple.
- `harness-triple-check.py`'s determinism is real: two consecutive `coverage` runs are byte-identical (`sha256 f9cd934a…3473`, reproduced by this review), and `--action coverage` exits 0 with `candidates 83 / unclassified 0 / findings 0`.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-084-01** — Target: `templates/verification-log-template.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md`). Change: add a `smoke_comparison=` field (or let `smoke_evidence_path` name one comparison transcript) and state that `smoke_command` / `smoke_exit_code` / `smoke_evidence_path` values carry no annotation. Source: F8, F15. Expected impact: completion condition ④ becomes readable for any feature whose smoke is a determinism comparison, and the improvised-in-a-fixed-grammar failure cannot recur.
- **REC-084-02** — Target: `templates/tasks-template.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/tasks-template.md`). Change: state whether `DoD Status` feeds the status machine; if not, say so at the status-row definition, and require a `[X]` row that names an output path to carry that path's existence check. Source: F13, F2. Expected impact: `pending` and `Implemented` stop coexisting silently, and a closed row with a missing carrier becomes a failing assertion.
- **REC-084-03** — Target: `templates/plan.md` § contract guidance (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/plan.md`). Change: a migration contract may not conjoin a "must judge X" clause with a "must not call the thing that judges X" clause; require the roster to be derived by `grep` over each fact's values across `scripts/` and `skills/`, listing every hit. Source: F5, F14. Expected impact: unsatisfiable contract conjuncts and carrier-only rosters stop being written.
- **REC-084-04** — Target: `templates/review-template.md` § Findings Summary (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/review-template.md`). Change: add a required `P0 validation path:` field with the closed values `subagent` / `direct re-read`, so the same-author fallback is visible on the report instead of only in the skill. Source: F6. Expected impact: a reader can weight P0 findings without knowing the review skill's fallback rules.

### 5.2 Command Prompt Improvements

- **REC-084-05** — Target: `templates/commands/implement.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/implement.md`). Change: before any status flip, run `closure-acceptance-check.py --spec-dir <spec> --json` and copy its `verdict`; a prose reading MUST NOT be the input, and the flip commit MUST rewrite every surface that states the status in the same edit. Source: F1, F9, F11. Expected impact: the status machine becomes a machine reading end to end, and one fact stops having two values in one row.

### 5.3 Automation / Script Improvements

- **REC-084-06** — Target: `scripts/python/validate-tasks.py` (absolute: `/storage/project/cloud-native-ai/spec-kit/scripts/python/validate-tasks.py`) and the implement gate's reading of it. Change: add a carrier-existence leg — a `[X]` row naming a repo-relative output path fails when the path is absent, unless the row carries an explicit `waived-by-user` token — and have the review/verification reports derive counts (`excluded`, `pending`) from the checker's JSON instead of restating numbers. Source: F2, F3, F10, F12. Expected impact: closed-by-assertion rows and stale counts become red checks rather than reader vigilance.

### 5.4 Workflow Improvements

- **REC-084-07** — Target: `.specify/skills/internal/review-sdd-process/SKILL.md` § 5 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/review-sdd-process/SKILL.md`). Change: name the "gate that cannot grow" pattern explicitly (closed set in an older test blocking a new finding name) and require the closed set to point at its growth procedure — which this feature now provides as `shared/declarations/facts/driver-gate-roster.yaml`. Source: F4. Expected impact: future gate improvements are not forced behind off-by-default flags.

### 5.5 Documentation Improvements

- **REC-084-08** — Target: `.specify/skills/internal/code-review/scripts/git-delta-review.sh` help text (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/code-review/scripts/git-delta-review.sh`). Change: delete the hand-maintained numbered step list from the help and point at the skill's closed enumeration (now five steps). Source: F7. Expected impact: one owner for the step count.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-084-05 — Machine-read status flip | `templates/commands/implement.md` | F1, F9, F11 |
| P0 | REC-084-01 — A legal carrier for a comparison smoke | `templates/verification-log-template.md` | F8, F15 |
| P1 | REC-084-02 — `DoD Status` ownership + carrier existence on a `[X]` row | `templates/tasks-template.md` | F13, F2 |
| P1 | REC-084-03 — Derived migration rosters, no unsatisfiable contract conjuncts | `templates/plan.md` | F5, F14 |
| P1 | REC-084-06 — Carrier-existence leg + derived counts in the checker | `scripts/python/validate-tasks.py` | F2, F3, F10, F12 |
| P2 | REC-084-04 — Visible P0 validation path | `templates/review-template.md` | F6 |
| P2 | REC-084-07 — Growth procedure instead of a frozen finding-name set | `skills/internal/review-sdd-process/SKILL.md` | F4 |
| P2 | REC-084-08 — One owner for the non-interactive step count | `skills/internal/code-review/scripts/git-delta-review.sh` | F7 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No target was `external` this run.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status**: three P0 findings were raised (F1, F8, F9). None was validated by an independent read-only subagent — this topology has no dispatch capability, and the declared fallback was used. Each P0 was validated by a direct mechanical re-read at diagnosis time: F1 and F8 from one `closure-acceptance-check.py --json` run (`smoke_record_pass=false`, `verdict=block`, `reasons[0].code=status-claims-implemented-but-blocked`); F9 from the single `features.md` line 90 that reads both values. Each row therefore carries `(validated: direct re-read, subagent unavailable)` and the weaker evidence path is disclosed rather than hidden.

---

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
