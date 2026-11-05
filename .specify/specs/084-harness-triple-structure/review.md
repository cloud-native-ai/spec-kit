# Specification-Driven Development (SDD) Process Review Report: Harness 三重结构（markdown + yaml + script）— review round 2

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
>
> **This is round 2 of the review of Feature 084.** Round 1's report is archived at
> `review-r1.md` in this directory (rotation per `shared/workflow/acceptance-hardening.md` § Review
> Composition § Records and rotation; the slice id here is the review round, so the archive keeps the
> content's own round marker instead of a feature-slice letter that this feature does not have). Round
> 2's delta is the fix commit `e0453f9e`; round 2's first duty is to close or retain every round-1 item.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 084 |
| Requirement Key | 084-harness-triple-structure |
| Requirement Name | Harness 三重结构（markdown + yaml + script） |
| Repository | spec-kit (`git rev-parse --show-toplevel` → `/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | `(no publishable HTTPS remote)` — remotes are `gitee`/`github`/`gitlab` (SSH) plus `origin` = `git@github.com:github/spec-kit.git` (upstream; it does not contain these commits) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch was never pushed. Every citation is an absolute path plus `git show e0453f9e:<path>` recovery |
| Branch | `084-harness-triple-structure` |
| Commit SHA | `e0453f9e634702d78f20e418af8242cdb1b84a49` (short: `e0453f9e`) — the review round-2 `HEAD`, fixed for the run |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | SDD Executor (fresh dispatch; same-author detection delegated per `shared/workflow/objective-analysis-gate.md`) |
| Environment | Linux, bash, CPython 3.11.13, `pytest 9.2.0` pin (EP-001), no subagent-dispatch capability in this topology |
| spec-kit Source Snapshot | this repository at `e0453f9e` (self-hosting: `.specify/` is the same flow every client project runs) |
| Round-1 record | `review.md` at `03a19487` → archived as `review-r1.md` (43294 B); its code segment → `code-review-20261105T160943Z.md` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|------------------|
| requirements.md | 285 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/requirements.md` | 19 FR / 6 SC / 14 STR, A1–A10 adjudications, scope criteria D1∧D2 |
| plan.md | 434 | `…/084-harness-triple-structure/plan.md` | 18/18 Constitution Check, 4 decision tensions, EP-001…EP-007, D1–D13 |
| tasks.md | 262 | `…/084-harness-triple-structure/tasks.md` | 32 rows (all `[X]`), 7 phases, GATE-1…7, `**DoD Status**: green-with-void` |
| verification.md | 134 | `…/084-harness-triple-structure/verification.md` | baseline block, one machine-readable smoke record, six SC status rows, joint-acceptance rows |
| contracts/ (5 files) | 426 | `…/084-harness-triple-structure/contracts/` | C-001…C-059, `md-bold-closed` (verified: 12+13+16+10+8 = 59) |
| data-model.md | 169 | `…/084-harness-triple-structure/data-model.md` | E-1…E-10 + six fixture families |
| quickstart.md | 152 | `…/084-harness-triple-structure/quickstart.md` | S1…S8 (4 measured, 4 route-(b)) |
| research.md | 157 | `…/084-harness-triple-structure/research.md` | R1–R10 measured readings |
| feature-ref.md | 42 | `…/084-harness-triple-structure/feature-ref.md` | bound Feature 084 + status movement |
| code-review.md | this run | `…/084-harness-triple-structure/code-review.md` | round-2 code segment record (1 blocking, 4 important, 2 suggestion, 2 praise) |
| review-r1.md | 43294 B | `…/084-harness-triple-structure/review-r1.md` | round-1 report, archived by this run |
| code-review-20261105T160943Z.md | 64141 B | `…/084-harness-triple-structure/code-review-20261105T160943Z.md` | round-1 code record, archived by `git-delta-review.sh start` |

## 1. Process Execution Timeline (round-1 close → round-2 open)

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | round 1 judged 3 P0 / 7 P1 / 6 P2 and refused the flip | `review-r1.md` § 2.4: `final_path` pass 2 / blocked 0; `completion_conditions.smoke_record_pass: false`; `verdict: block`; segment verdicts `blocked` ×3 | No — the refusal is the prescribed disposition |
| 2 | round-1 code segment carried 2 `blocking` | `code-review-20261105T160943Z.md` § Review 意见: `closure-acceptance-check.py:223` and `:916` | No |
| 3 | fix commit `e0453f9e` "resolve the review blocking and P0 findings" — 15 paths, +233 −21 | `git show --stat e0453f9e` | **Yes** — see N1: two of the three sites the blocking item named were fixed, the third was not, and the message claims the item resolved |
| 4 | targeted test set after the fix: 219 passed / 2 failed | `test-evidence/review-fix-targeted-tests-2026-11-05.txt` (tail: `2 failed, 219 passed`), both failures in the 23-name implement-start baseline set (`test_e_a_stale_pin…` = stale pin, `test_c22_watch_target_hook_selftest` = `cannot create temp dir` permission) | No — no new failure |
| 5 | ARC re-read: `verdict: accept`, all four completion conditions true | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), copied into § 2.4 | No — this is the machine's answer, not the run's prose |
| 6 | round 2 dispatched against `e0453f9e` | state spine `stage_base_commit: e0453f9e`, `attempt: 2` | No |

## 2A. Round-1 Closure Ledger (round 2's first duty)

| Round-1 item | Severity then | Round-1 location | Round-2 reading | Owner stage of what remains |
|---|---|---|---|---|
| **F1** implement gate asserted completion condition ④ from prose | P0 | `verification.md:55-56` | **Closed on the artifact side, and the mechanism closed with it**: the smoke block is now three literal values (`smoke_exit_code=0`, one `smoke_evidence_path`, `smoke_comparison`), `evaluate_smoke()` reads the same file, and `smoke_record_pass` is `true`. `templates/commands/implement.md:56` already required the closure verdict since `da5e4480` (081a) and is not in this delta, so the remaining gap was never a missing instruction — it was a log the checker could not parse, which is exactly what F8 repaired | — |
| **F8** smoke record not machine-parseable | P0 | `verification.md:54-57` | **Closed**: three fields carry no annotation; `smoke.evidence_exists: true`, `smoke.exit_code: "0"`, `records: 1` | — |
| **F9** one `features.md` row carried two statuses | P0 | `features.md:90` | **Closed**: the narrative now ends `final 测试预算后已翻到 \`Implemented\``, matching the column | — |
| **F2** two closed rows name evidence carriers that do not exist | P1 | `tasks.md:31`, `tasks.md:166` | **Open, unchanged** — `ls test-evidence/head-failed.txt notes/quickstart-run.md` still returns two `No such file`; the fix commit edited `tasks.md` (the DoD line) without touching either row | implement (`tasks.md` rows) → see N4 |
| **F3** one count drifted across four surfaces | P1 | `verification.md:91` | **Closed where round 1 named it** (SC-004 now reads 70 = 38 + 32) and **re-opened one file over**: SC-001 still records `28/28` while the fix's own consumers edit moved the live reading to `30/30` | implement (`verification.md`) → see N5 |
| **F10** a `pass` row rested on a stale reading | P1 | `verification.md:91` | Closed with F3's rewrite; **the same class recurred in SC-001** (N5) | implement |
| **F11** `verification.md` contradicted itself about status | P1 | `verification.md:132` | **Closed**: `notes_feature_status=Implemented` matches the header | — |
| **F12** the baseline datum was labelled "implement start" but was a Part-3 commit | P1 | `verification.md:21` | **Closed**: `baseline_commit=9657885f`, whose successor `e3e0af68` is literally `chore(084): freeze the implement-start readings and the coverage baseline`; the sibling field `post_change_commit` was not re-read (N6) | — / N6 |
| **F14** the delta does not deliver one machine-read copy for two declared closed sets | P1 | `closure-acceptance-check.py:223`, `pre-analyze-check.py:332`, `validate-requirements.py:99`, `:916/939/1347` | **Half closed**: `success-criterion-path-values` is fully migrated (`PASS_PATH` derived in both engines, three branch literals gone); `flow-class-classes` moved two engines onto the declaration and left the third (round-1's own first-named site) as an inline tuple | implement → see N1 / code segment |
| **F15** the two-run claim had no legal carrier | P1 | `tasks.md:129`, `verification.md:56` | **Closed in form, not in force**: the template gained `smoke_comparison`, no program reads it | plan/template → see N3 |
| **F4** the new delegation could not be default-on | P2 | `pre-analyze-check.py` docstring | **Open by decision** — the flag is still off by default and the docstring still names the 081 closed assertion as the reason | framework recommendation REC-084-07 |
| **F5** a contract clause asks `verify` for a reading another clause forbids | P2 | `contracts/harness-triple-check.contract.md` C-032 / C-038 | **Open** — `verify` still prints `residual_literals: "delegated: …"` (`harness-triple-check.py:441`); the contract was not touched by the fix | plan (C-032) → REC-084-03 |
| **F6** same-author detection could not be delegated | P2 | objective-analysis-gate fallback | **Open** — same topology, same weaker evidence path, disclosed here again | framework recommendation REC-084-04 |
| **F7** the code-review help states four steps, its skill states five | P2 | `git-delta-review.sh` help | **Open** — the help still reads `NON-INTERACTIVE PATH (four steps, … — four, never three)` while `SKILL.md` § 非交互路径 says 五步 | framework recommendation REC-084-08 |
| **F13** `DoD Status: pending` beside an `Implemented` feature | P2 | `tasks.md:26` | **Closed in form, mis-resolved in vocabulary**: `green-with-void` is defined for a row whose premise measured false, and the annotation itself says these rows are *user-waived*, not falsified | template → see N7 |
| **F16** the client-project limbs of SC-005 never ran | P2 | `verification.md:95-102` | **Open, under the user's test waiver** — no scratch-tree `specify init` reading exists; the mirror limb is green | user waiver (residual risk, not a defect) |

**Round 1 dispositions that need no action**: F6's weaker P0 evidence path is disclosed again in § 7; F16 stays residual risk under the explicit user waiver, which is the user's ruling and not an agent's.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 5 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 0 |
| Workflow | 3 |
| Documentation | 2 |

Round 1's P0 count (3) is zero this round: the three acceptance-honesty states it named are now machine-readable and read `accept` by the owner program. The five P1s are therefore *not* a regression — four of them are round-1 items that survived, plus one instance of the same drift class created by the fix itself.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `e0453f9e634702d78f20e418af8242cdb1b84a49` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base --spec …` reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 284 / 5 / 279 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `blocked` | the record carries 1 `blocking` entry |
| Gate verdict | `blocking-unresolved` | `report --summary --file …` exits 1 with `blocking_entries=1`, `gate=deny` |
| Reason, when one applies | none | a `blocked` verdict needs no basis line |
| Uncommitted scope | disclosed, never concluded over: this run adds `review.md`, `review-r1.md`, `code-review.md` (rewritten after rotation), `test-evidence/review-round2-smoke-2026-11-06.txt`, the `stage-status.md` round-2 row and the register rows; a pre-existing modified run record `session/20261102T231648Z-…-081a.md` and pre-existing untracked `memory/` records are outside the slice and were left untouched | the same sentence in [`code-review.md`](/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md) |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` | written (triage `run`) |
| Archive | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review-20261105T160943Z.md` | round 1's record, rotated by `start` |

Six-level counts in the record: `blocking` 1 · `important` 4 · `suggestion` 2 · `nitpick` 0 · `question` 0 · `praise` 2. The `blocking` entry is the surviving inline copy of the declared closed set `flow-class-classes` in `scripts/python/closure-acceptance-check.py:227` — round 1's blocking #1, two of whose three sites the fix migrated. The four `important` entries are the two retained round-1 items (the FR-012 fallback-vs-delete split, and `verify`'s non-reading `residual_literals`), the new `smoke_comparison` slot with no reader, and the unlabelled class-axis degradation the fix introduced. The findings themselves are read there; this subsection carries the verdict and the pointers only.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | derived: the standard spec-stage set ∪ `plan.md` § Project Structure § Documentation (which declares `research.md` and `feature-ref.md` in addition) — **9 members** |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | two P1 acceptance-honesty findings plus one P2 status-vocabulary misuse |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/084-harness-triple-structure/tasks.md` | 166 | none | Two `[X]` rows still name carriers that do not exist (round-1 F2, untouched) — N4 |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 70 | none | `SC-001_status=pass` records `28/28` while the live reading after this very fix is `30/30`, and limb (iii)'s "引用它的一方确实被点名" is falsified by an engine that is not named — N5 |
| P2 | `.specify/specs/084-harness-triple-structure/verification.md` | 39 | none | `post_change_commit=98288d45` names a Part-3 commit that never touched this file — N6 |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 26 | none | `green-with-void` used for a user waiver rather than a falsified premise — N7 |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `e0453f9e634702d78f20e418af8242cdb1b84a49` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Smoke command | `python3 scripts/python/harness-triple-check.py --action coverage` (run twice, byte-compared) | recorded verbatim |
| Smoke exit code | `0` | the integer the command returned, both runs |
| Smoke evidence path | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/test-evidence/review-round2-smoke-2026-11-06.txt` | exists, non-empty; holds both runs' full stdout, both exit codes, the `cmp` exit and both sha256 values (`f9cd934a…3473`, identical) |
| Scope and regression verdict | scope clean (the fix touches 15 paths, all inside the feature's own surfaces); regression clean on the surfaces that were read — `sync-mirrors.py --check` exit 0 with six pairs `ok` (templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 121 / shared 89), `git diff 4b65517c -- pyproject.toml` empty, targeted set 219 passed / 2 failed with both failures in the 23-name baseline | the segment's own reading |
| Segment verdict | `blocked` | the delta still does not deliver SC-002's one-machine-read-copy property for one of its two declared closed sets |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/closure-acceptance-check.py` | 227 | none | The delta migrates two engines for `flow-class-classes` and leaves the third holding the pair; the detail is in `code-review.md` — N1 |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `features.md` row 084 and `features/084.md` `**Status**` |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), never recomputed here |
| Comparison verdict | `agree` | the checker's verdict is `accept` and the claim is `Implemented` |
| Failed condition, on refusal | none — no refusal fires on this record | `completion_conditions` reads `every_final_path_pass: true`, `no_open_rows: true`, `smoke_record_pass: true`, `status_row_per_criterion: true`; `reasons: []` |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 2 |

**ARC does not refuse this round.** The run's refusal comes from the status machine's third condition instead (§ Status Transition) — a different gate reading a different artifact, and collapsing the two into one sentence would hide which one fired.

## Status Transition — refused, and the condition is named

The transition judged here is `Implemented → Ready for Review`, whose four conjunctive conditions are owned by `templates/feature-details-template.md` § Canonical Status State Machine and are cited here, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | `tasks.md`: `closed 32 / deferred 0 / open 0` (the checker's own `tasks` block) | satisfied |
| (b) review evidence produced | this report + `code-review.md`, both on disk | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `code-review.md` carries **1** `blocking` entry (`closure-acceptance-check.py:227`); `report --summary --file` exits 1 with `gate=deny` | **FAILS** |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 2 `pass`, 0 in every non-pass bucket | satisfied |

**The refusal literal is `blocking-unresolved`, the failed condition is (c), and the status stays `Implemented`.** No surface is written back: `features.md` and `features/084.md` are untouched by this run, because a refusal is not a downgrade and this feature admits no `Implemented → Ready for Review` shortcut through one. Round 2's own artifacts land on the two verifiable carriers — this report's § 2.1 and the `## Latest Review` entry this run adds to `features/084.md` — and neither of them states a new status.

## 3. Findings (Problems & Improvement Targets)

### N1 — A fix round's closure is asserted from the commit message, not read from the finding's own site list

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/scripts/python/closure-acceptance-check.py:227`; the claiming artifact is `git log -1 e0453f9e` — `fix(084): resolve the review blocking and P0 findings`
- **Evidence** (verbatim quote, from the module):

  ```
  FLOW_CLASSES = ("execution", "expression")
  ```

  against the declaration that owns that set:

  ```
  consumers:
    - scripts/python/flow-class-check.py
    - scripts/python/validate-requirements.py
    - skills/external/sdd-loop-driver/scripts/pre-analyze-check.py
  ```

  and against round 1's own sentence, which named this site **first**:

  ```
  FLOW_CLASSES = ("execution", "expression") here (223) and at skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:332, plus EXECUTION_CLASS = "execution" at scripts/python/validate-requirements.py:99
  ```

- **Why it's a problem**: the second and third sites were changed and their engines added to `consumers:`; the first was left byte-identical. Nothing in the flow reads a fix round against the finding's own enumeration, so a commit message is the only place the claim lives — and the claim is false. The consequence is not stylistic: `grep -n 'flow-class-classes' scripts/python/closure-acceptance-check.py` returns no hit, so add one member to the declaration alone and `flow-class-check.py`, `validate-requirements.py` and `pre-analyze-check.py` accept a `**Flow Class**` value this engine still refuses with `InputError` at 581 — US2 acceptance scenario 2 (`只改声明文件 -> 门禁立刻接受新取值`) falsified for one engine, and `harness-triple-check.py --action verify` reports `findings: 0` on the tree because C-033's bidirectional reading only walks the parties the declaration already names.
- **Proposed fix**: a review-fix commit carries one reading per site the finding enumerated (a site → commit → reading table), and the review's round-2 check reads that table instead of the commit message. Framework shape: `skills/internal/review-sdd-process/SKILL.md` § 5 gains the obligation; `templates/commit-template.md` gains the slot. This is REC-084-10.

### N2 — Round 1's second legal carrier was never written

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/features/084.md` `## Latest Review` (the section that should hold the review-record entry)
- **Evidence** (verbatim quote — the section's entries, in order):

  ```
  - **2026-11-05 clarify（`/speckit.clarify` Mode A，无人值守、零提问）** …
  - **2026-11-05 tasks（`/speckit.tasks`，`5dc5919a` + `8ed70a87`）** …
  - **2026-11-05 checklist（`/speckit.checklist`，`9abb10fb`）** …
  - **2026-11-05 analyze round 1 回环修复（驱动者授权，三提交）** …
  - **2026-11-05 plan reopen（路径 A，用户裁定；…）** …
  - **2026-11-05 implement（`/speckit.implement` 最后一段 T020–T031，用户测试豁免）：** …
  ```

  `grep -n 'speckit.review' .specify/memory/features/084.md` → no hit.
- **Why it's a problem**: `templates/commands/review.md` § Output and placement names two verifiable carriers for the two segment conclusions — the report's code subsection *and* the bound feature detail's `## Latest Review` review-record entry. Round 1 wrote one. The feature side therefore shows a chain that ends at `implement`, and a reader who starts from the feature (the entry point the index points at) sees no review at all — including no refusal. A carrier obligation with no check is how a run can be complete and invisible at once.
- **Proposed fix**: the review's closing steps assert both carriers exist and carry the run's identity (a deterministic check: the feature detail has a `## Latest Review` entry whose date/run id matches this run); a missing entry is a red step, not silence. This is REC-084-11.

### N3 — The new smoke slot ships without a reader

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md:65` (and its mirror `.specify/templates/verification-log-template.md:65`)
- **Evidence** (verbatim quote):

  ```
  smoke_comparison     optional: a repo-relative comparison transcript (e.g. the second run's evidence)
                       when the smoke is a determinism comparison; the three fields above MUST carry
                       no annotation — a value the checker parses is a literal
  ```

  against the checker's own field tuple:

  ```
  SMOKE_FIELDS = ("smoke_command", "smoke_exit_code", "smoke_evidence_path")
  ```

  and `grep -rn smoke_comparison --include=*.py .` → zero hits.
- **Why it's a problem**: round 1's F15 said the two-run claim had no legal carrier; the fix produced one that no program consults, so a fabricated or stale comparison path passes condition ④ exactly as a true one does. This is the same "a slot that would not go red" shape as F8 one level down: F8 made the three parsed fields literal; the fourth field carries the very claim (byte identity) that the run cannot otherwise prove, and it is the one nobody parses. A template that adds a slot without naming its reader teaches the next implementer to improvise in a fixed grammar again.
- **Proposed fix**: a template slot MUST name its reader in the slot's own line, and where the field exists the checker resolves it as an existence test (or the slot becomes mandatory for a feature whose smoke is a comparison). This is REC-084-09.

### N4 — A closed row whose named carrier is absent is still indistinguishable from a closed row

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:31` (GATE-2) and `:166` (T031)
- **Evidence** (verbatim quote):

  ```
  - GATE-2: Zero new failures on the five frozen gate scripts' existing tests, read at id level — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt -q`, then `comm -13 <implement-start baseline> head-failed.txt` prints nothing …
  ```

  ```
  - [X] T031 [blockedBy: T027,T028,T030] (SC-001…SC-006, quickstart S5–S8) Run `quickstart.md`'s S5–S8 on the final tree and record the real output in `notes/quickstart-run.md` …
  ```

  `ls .specify/specs/084-harness-triple-structure/notes/` → `pre-change-measurements.md`, `red-first-evidence.md`; `ls …/test-evidence/head-failed.txt` → `No such file or directory`.
- **Why it's a problem**: unchanged since round 1, and the fix commit touched this very file — it edited the DoD line and left both rows. The only machine-readable signal on a row is its `[X]`; a row that promises an output path which does not exist reads "done" to every program and to every reader who does not `ls`. Under the user's test waiver the honest row state is a waiver token, not a tick.
- **Proposed fix**: REC-084-06 as written (a carrier-existence leg in `validate-tasks.py`, or an explicit `waived-by-user` token on the row). Round 2 adds the datum that the fix round passed over it while editing the same file.

### N5 — A `pass` row records a count the tree no longer reads, and one of its limbs is falsified

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:70`
- **Evidence** (verbatim quote):

  ```
  SC-001_value=… consumer consistency declarations→carriers 28/28 and carriers→declarations 16/16
  ```

  against the live reading on the same tree, after the fix:

  ```
  consistency-declarations-to-carriers: 30/30
  consistency-carriers-to-declarations: 16/16
  ```

  and against the criterion's own limb (iii):

  ```
  (iii) 每条事实声明的 `consumers` 与载体侧引用**双向一致**——声明点名的一方确实引用它、引用它的一方确实被点名（N/N…）
  ```

- **Why it's a problem**: two defects in one row. The count is stale — the fix added two consumers and only the declaration was updated, so the row records a number that moved *because of the fix itself*. And limb (iii)'s second half ("引用它的一方确实被点名") is false on the tree: `closure-acceptance-check.py` references the `flow-class-classes` value and is not named. The program that awards this row cannot see either defect — it compares the parties the declaration lists (`harness-triple-check.py:345-368` iterates `consumers`), so an unnamed reader is invisible by construction. This is round 1's F3/F10 class recurring inside the commit that was repairing it, which is the strongest available evidence that a restated count in prose is not a reading.
- **Proposed fix**: the row's value is a pointer to the run's output (`harness-triple-check.py --action verify`) instead of a restated pair, and limb (iii) is measured by the derived roster REC-084-03 proposes (grep each fact's values across `scripts/` + `skills/`, fail on a hit outside `consumers`).

### N6 — `post_change_commit` names a commit that never touched the file

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:39`
- **Evidence** (verbatim quote):

  ```
  post_change_commit=98288d45 (this segment's commit is the one carrying these files; recorded here as the parent-inclusive working tree)
  ```

  `git show --stat 98288d45 -- .specify/specs/084-harness-triple-structure/verification.md` → empty; `git log --oneline -- verification.md` → `e0453f9e`, `03a19487`, `e185da6c`, `1e4ca01e`.
- **Why it's a problem**: round 1 repaired the sibling `baseline_commit` and left this one. The field's parenthetical asserts that `98288d45` carries these files, which the file's own history contradicts, and `98288d45` is a Part-3 commit. An anchor field that points at the wrong commit is the same defect class as F12 — a datum a later reader would cross-check git to discover is wrong.
- **Proposed fix**: derive the field from `git log -1 --format=%h -- <file>` at write time, or drop the field in favour of the baseline pair the checker actually reads.

### N7 — `green-with-void` is used for a user waiver, which is not what the token means

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:26` and `:202`; the token's owner is `.specify/templates/tasks-template.md:52`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: green-with-void
  ```

  ```
  - **DoD Status `green-with-void`**: the void rows are the user-waived scratch-tree limbs (T022/T030) and the closure full-suite leg, not a premise that measured false. …
  ```

- **Why it's a problem**: the token's own definition — cited in this repo's earlier uses (`076`, `050`'s proposal) — is a row **whose premise is measurably false**, i.e. `void`. The annotation here states in the same sentence that these rows are *not* a false premise; they are unmet readings under an explicit user waiver. So the DoD block now uses the vocabulary's escape hatch for a case the vocabulary does not cover, which launders a waiver into a green. The honest resolution is either a third token (`green-with-waiver`, owned by the template) or `pending` plus a waiver annotation — and round 1's F13 asked exactly which of the two values is wrong; the answer supplied is a third reading of the escape token.
- **Proposed fix**: the template's `DoD Status` domain gains the waiver case explicitly (or states that a waived row is `pending` + annotation and does not feed the status machine), so a feature cannot be `Implemented` while its DoD block reports a status the domain never defined.

## 4. What Worked — Preserve (Brief)

- The fix commit's ARC re-read is machine-derived, not narrated: `verdict: accept` with all four completion conditions true, and the round-2 review reproduced it independently (`test-evidence/review-fix-closure-2026-11-05.txt` is the same JSON).
- The `success-criterion-path-values` migration is now the shape the other axis needs: one derived value (`PASS_PATH = PATH_VALUES[0] if PATH_VALUES else "final"`) and four branch sites comparing against it, with `grep '"final"'` reduced to the labelled fallback.
- `pre-analyze-check.py`'s new `declared_sequence()` degrades **loudly** on the read failure path (`label_absent` before the fallback) — FR-012's second half done right, which makes the silent sibling in `validate-requirements.py` a defect rather than a style choice.
- The smoke record became parseable in one edit without touching the checker's criteria: the three fields went literal, the checker's existing `evaluate_smoke()` read them, and the fourth claim got its own slot instead of being crammed into a parsed field.
- Round 1's own record was complete enough to be *replayed*: every closure decision in § 2A was made by re-running a named command from the round-1 text, never by recalling it.
- Determinism is reproducible across rounds: two consecutive `coverage` runs today produce `sha256 f9cd934a…3473`, the same value as the round-1 smoke — the pass is about the tree, not about the run.

## 5. spec-kit / SDD Improvement Recommendations

**New this round.** Each is registered in `.specify/memory/register.md` in the same commit as this report.

- **REC-084-09** — Target: `templates/verification-log-template.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`). Change: a slot line MUST name the program that reads it; a slot with no reader is either deleted or wired into the checker that awards the record. Source: N3. Expected impact: "the slot exists" stops being mistaken for "the claim is checked", which is the feature's own false-green red line applied to its own template.
- **REC-084-10** — Target: `.specify/skills/internal/review-sdd-process/SKILL.md` § 5 + `templates/commit-template.md` (absolute paths under the same root). Change: a fix round that answers review findings carries a per-site closure table (finding → its enumerated sites → the commit that touched each → the reading), and the next round reads that table instead of the commit subject. Source: N1. Expected impact: "resolve the review findings" becomes a falsifiable claim; the round-1 shape (two of three sites, message says resolved) cannot recur silently.
- **REC-084-11** — Target: `templates/commands/review.md` § Output and placement (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md`). Change: the closing steps assert both verifiable carriers exist and carry this run's identity — the report's § 2.1 and the feature detail's `## Latest Review` entry — and a missing carrier is a red step. Source: N2. Expected impact: a run cannot be complete and invisible from the feature side, and the refusal verdict reaches the reader who starts at the index.

**Round-1 recommendations, unchanged status** (registered, still `open`, none withdrawn): REC-084-01 (partially delivered by the `smoke_comparison` slot — delivered in form only, see N3), REC-084-02 (F13/F2 — still the right fix, N4/N7 show the need), REC-084-03 (F5/F14 — still the right fix, N1 shows the need), REC-084-04 (F6), REC-084-05 (F1/F9/F11 — the artifact side is closed; the "copy the verdict" wording is still absent from `templates/commands/implement.md:56`, which says run it and does not say paste it), REC-084-06 (F2/F3/F10/F12), REC-084-07 (F4), REC-084-08 (F7).

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Fix the surviving `flow-class-classes` copy (`closure-acceptance-check.py`) or record why the engine is out of the roster | `scripts/python/closure-acceptance-check.py` | N1 (code blocking) |
| P1 | Per-site closure table for review-fix rounds | `skills/internal/review-sdd-process/SKILL.md` § 5; `templates/commit-template.md` | N1 (REC-084-10) |
| P1 | Both review carriers asserted at closing | `templates/commands/review.md` | N2 (REC-084-11) |
| P1 | Slot-with-a-reader rule for the verification log | `templates/verification-log-template.md` | N3 (REC-084-09) |
| P1 | Carrier existence on a `[X]` row | `scripts/python/validate-tasks.py` | N4 (REC-084-06) |
| P1 | Derive SC rows / the consumer roster instead of restating counts | `scripts/python/harness-triple-check.py`, `verification.md` | N5 (REC-084-03, REC-084-06) |
| P2 | `post_change_commit` derived or dropped | `templates/verification-log-template.md` | N6 |
| P2 | `DoD Status` domain names the waiver case | `templates/tasks-template.md` | N7 (REC-084-02) |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target is `external`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document (round 1's report is reached by the repo-relative path `review-r1.md` in the same directory).
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status**: **no P0 was raised this round** (round 1 raised three; all three are closed by machine-readable state, see § 2A). The five P1 findings were validated by direct mechanical re-read — each cites a command whose output is quoted — and none was validated by an independent read-only subagent: this topology has no dispatch capability and the declared fallback (`skills/internal/review-sdd-process/SKILL.md` § 5) was used. The weaker evidence path is disclosed rather than hidden; REC-084-04 would put it on the report's own face.
- [x] **Round-level honesty**: this run refuses the status transition on condition (c) and states that ARC, by contrast, reads `accept`. The two gates are reported separately because they read different artifacts.

## 8. Feedback

Framework friction worth posting as feedback (one entry per unit, four units — `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review`): the round-2 run had no way to tell which of round 1's archived records the merge gate reads, and the rotation rule's slice id has no defined value for a same-slice re-review (`review-r1.md` was chosen by this run and the choice is stated in the header). No code defect from `code-review.md` is posted here — per `templates/commands/review.md` § Feedback boundary those stay in that record with their severity, file and line.
