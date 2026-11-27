# Specification-Driven Development (SDD) Process Review Report: Context Management（上下文的声明、组合与只读审计）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 110 |
| Requirement Key | 110-context-management |
| Requirement Name | Context Management（上下文的声明、组合与只读审计） |
| Related Feature | 110 Context Management（上下文的声明、组合与只读审计） |
| Repository | spec-kit (worktree `context-management`; branch `110-context-management`) |
| Repository URL | `git@github.com:cloud-native-ai/spec-kit.git` (GitHub remote; `origin` is the upstream `github/spec-kit` and is not where these commits live) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — no pushed branch contains `8ef781e27`; every citation below is an absolute path plus `git show <sha>:<path>` recovery |
| Branch | `110-context-management` |
| Commit SHA | `8ef781e2719a07eef8cefdc3290466b3b0a4cd38` (short: `8ef781e27`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management` |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (four segments + Acceptance Reality Check, one execution) |
| Environment | Linux 5.10.134-15.2.al8.x86_64 x86_64; bash; Python 3.11.11; pytest 8.4.2 via `SPECKIT_PYTHON=/usr/local/bin/python3` |
| spec-kit Source Snapshot | `github/spec-kit` @ branch base `0419adae5e6e0e208ad6bcb443e45be8d266f04a` (feature-first-commit) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 288 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/requirements.md` | 29 FR / 11 SC (9 final, 2 supporting), runtime-stack rows, shared strings |
| plan.md | 426 | `…/110-context-management/plan.md` | 10 execution premises (all verified), 11 declared dependencies with 14 dispositions, mirror obligations |
| tasks.md | 406 | `…/110-context-management/tasks.md` | 39 tasks (39 `[X]`), 39-clause coverage table, evidence landing points |
| data-model.md | 207 | `…/110-context-management/data-model.md` | Entities, presence states, JSON faces |
| quickstart.md | 159 | `…/110-context-management/quickstart.md` | Six runnable scenarios |
| verification.md | 102 | `…/110-context-management/verification.md` | 11 SC status rows (all `pass`) + smoke record + RS joint-acceptance rows |
| research.md | 197 | `…/110-context-management/research.md` | R-1…R-10 findings, RU-1…RU-3 residual unknowns |
| feature-ref.md | 78 | `…/110-context-management/feature-ref.md` | FR→clause / SC→clause mapping |
| contracts/ | 5 files | `…/110-context-management/contracts/` | C-001…C-046 (39 claimed machine-decidable clauses) |
| checklists/ | 2 files | `…/110-context-management/checklists/` | Requirements-quality checklist (38 items) + initial quality checklist |
| checkpoints/ | 7 files | `…/110-context-management/checkpoints/` | Stage checkpoints 01–07 |
| test-evidence/ | 125 files | `…/110-context-management/test-evidence/` | Red/green logs, mutation drill, full-suite comparison, per-SC evidence |
| notes/ | 4 files | `…/110-context-management/notes/` | Pre-change measurements, red-first slots, quickstart run |
| Registry row | row 118 | `.specify/features.md` | Feature 110 row (`Implemented` before this review) |
| Feature detail | 30 | `.specify/features/110-context-management.md` | Feature 110 detail (`Implemented` before this review) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | U0 entry declaration, preflight, U1 probe | `.specify/state/context-management.md` § U0/§ Dispatch Preflight/§ U1 | No |
| 2 | Requirements stage (29 FR / 11 SC) | `197a91c71`, `ae4247783`; checkpoint `0f580d6ec` | No |
| 3 | Clarify stage; produced paths left uncommitted | `01857c016` subject: "record clarify artifacts and stage records (driver repair)" | **Yes — driver committed the stage's produced paths** |
| 4 | Plan stage (plan / data-model / quickstart / five contracts) | `07d962a57`; checkpoint `ae9922ca8` | No |
| 5 | Tasks stage (406 lines / 39 tasks; validator 0/0) | `ef87d85bf`; checkpoint `114a8ae86` | No |
| 6 | Checklist stage (38-item requirements-quality checklist; 15+ gaps routed to analyze) | `cb79bb43d`, `0a517b2b8`; checkpoint `0de907fe5` | No |
| 7 | Analyze round 1: 2 HIGH (AN-01 seven-trigger composers, AN-04 audited-source read boundary) | `09abf6ab0`, `5fbe83302`; spine § U4 analyze round 1 | No — the gate correctly blocked and repaired |
| 8 | Analyze repair + round 2: open C 0 / H 0 / M 10 / L 15 | `badc0e149`, `c0e913612`; checkpoint `2cbbb3c8a` | No |
| 9 | Implement P1 (T001–T010), P2 (T011–T020), P3 (T021–T030), P4 (T031–T039) | `3822d1c04`, `c4d41dfb4`, `7ca67aa93`, `08fff9870`, `75b3b6457` | No |
| 10 | Implement hand-off omits `verification.md`, Feature 110 registration, and the RS joint-acceptance rows | `checkpoints/07-implement.md:4`: "the stage handed off a crew-side `verification-input.md` without deriving `verification.md` and without registering Feature 110. The driver derived `verification.md` (9 SC rows), added the RS-001/RS-005 joint-acceptance rows … registered row 110 + detail" | **Yes — three driver repairs (`5faa8b9d8`, `221e1f72d`, `8ef781e27`)** |
| 11 | Review stage (this run): four segments + ARC, both records written, status flipped | this commit | No |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 2 |
| Documentation | 8 |

> Severity note: P1/P2 rows need no independent validation pass; the process segment raised zero P0, so the P0 validation gate is vacuously satisfied (see §7).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | the resolved diff base (`git-delta-review.sh base`) |
| Head commit | `8ef781e2719a07eef8cefdc3290466b3b0a4cd38` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker (non-TTY agent invocation) |
| Changed / judged / skipped / gap files | 429 / 29 / 400 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `not-evaluated` | four closed values owned by the `code-review` skill |
| Gate verdict | `allow` | `report --summary --file` exit 0; zero `blocking` entries |
| Reason, when one applies | legal skips (non-code and generated files) earn no coverage credit, so the receipt issues no pass verdict over the full 429-file delta; all 29 code-path files were reviewed and the code findings are recorded | mandatory for `not-evaluated` |
| Uncommitted scope | 2 paths (`.specify/session/20261125T140702Z-…-clarify-artifact-…md`, `.specify/trigger/index.json`) are disclosed, never concluded over; the same sentence lives in `code-review.md` | disclosed |
| Record | `.specify/specs/110-context-management/code-review.md` | written (triage `run`) |
| Archive | `none` | first run |

Two `important` items are open; both are **answered — agree**:
- JSON face key drift (F9): agreed; the fix requires an owner decision between FR-021's `message` and the shipped `detail` shape, so it is not repaired inside this read-only review.
- Decidable-duplication reading not applied to the repository layout (F10): agreed; the repair belongs to the requirement/guard owner, not to this review.

No `blocking` entry exists in the record, so this segment does not refuse the status transition; its non-`pass` verdict is a disclosed coverage limit, not a finding against the feature.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, contracts/, checklists/, checkpoints/, test-evidence/, notes/, registry row, feature detail | union of the standard spec set, `plan.md` § Project Structure, the tasks-declared `notes/` landing point, and the bound-feature carriers |
| Coverage line | 15 / 15 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | expected set complete; no P0; P1/P2 below |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/110-context-management/tasks.md` | 121 | — | 22 of 39 clause-coverage `Pinning test` references name test functions that do not exist (F5) |
| P1 | `.specify/specs/110-context-management/requirements.md` | 174 | — | `empty` is defined/judged two ways across requirements, data-model and the owner document (F6) |
| P1 | `.specify/specs/110-context-management/requirements.md` | 164 | — | FR-010 says the audit reports decidable duplication while FR-021 closes `check` at nine rules with no such rule (F7) |
| P2 | `.specify/features/110-context-management.md` | 10 | — | The template's `## Latest Review` section is absent from the detail (F8); this review's landing adds it |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | the resolved diff base |
| Head commit | `8ef781e2719a07eef8cefdc3290466b3b0a4cd38` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code skill's `git-delta-review.sh` reported |
| Smoke command | `python3 .specify/scripts/python/context-audit.py --action check` | recorded verbatim; re-run by this review |
| Smoke exit code | 0 | the integer the command returned |
| Smoke evidence path | `.specify/specs/110-context-management/test-evidence/audit-fixtures.txt` | exists, 4,352 bytes, non-empty |
| Scope and regression verdict | Scope: the delta implements the declared surfaces (four facts, owner document, engine, ambient section, framework-map rows, guards, fixtures, records); the two root-level evidence files are a landing-point gap (F4), not unrequested code. Regression: the five feature guard modules pass 59/59 on the reviewed tree; mirrors are byte-identical on all six pairs; the full-suite comparison reports 223 failed at baseline and 223 at current with zero new names (SC-008 evidence) | the segment's own reading |
| Segment verdict | `pass` | no P0; the smoke triple is complete and green |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/context-audit.py` | 540 | — | `check` JSON findings carry `row`/`detail` and summary carries a third `findings` count, unlike FR-021's fixed `rule`/`file`/`line`/`message` face (F9) |
| P1 | `tests/contract/test_context_management_engine.py` | 593 | — | The C-027 decidable-duplication reading runs only over fixture copies, never over the repository's own layout or the audit entry (F10) |
| P2 | `scripts/python/context-audit.py` | 441 | — | A directory holding only 0-byte files reads `empty`, while FR-020 judges a directory by entry count (F11) |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | the bound feature detail's claim (and the registry row), copied |
| `final_path` record, copied verbatim (7/7) | pass 9 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 9 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/110-context-management --json`, never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept` against the claim `Implemented` |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition.** `Implemented → Ready for Review` is accepted: the four conjunctive conditions hold — zero deferred (`[~]`) tasks (39/39 `[X]`); review evidence produced (this report plus `code-review.md`); the current code-segment record carries zero `blocking` entries; and no `final`-path criterion sits in `blocked` / `deferred` / `fail` (9/9 `pass`). Both carriers are flipped in this run's artifact commit.

## 3. Findings (Problems & Improvement Targets)

### F1 — Stage hand-offs pass while their closing artifacts are still the driver's work

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/checkpoints/07-implement.md#L4` (also commits `01857c016`, `5faa8b9d8`, `221e1f72d`)
- **Evidence** (verbatim quote):

  ```
  **Driver repair**: the stage handed off a crew-side `verification-input.md` without deriving `verification.md` and without registering Feature 110. The driver derived `verification.md` (9 SC rows), added the RS-001/RS-005 joint-acceptance rows for the in-scope runtime rows, registered row 110 + detail, and the closure checker now returns `accept` (four conditions true, 9/9 final path, no reasons).
  ```

- **Why it's a problem**: Three stages in this line closed with a driver repair on their behalf (clarify's produced paths left uncommitted; implement's `verification.md` + registry + RS joint-acceptance rows). The stage contract reads "PASS" while the artifact closure is performed by the orchestrator, so every unattended line pays the same repair toll and the stage's own gate never proves it produced its closing artifact.
- **Proposed fix**: In `templates/commands/implement.md`, make the hand-off block require the three items explicitly (derived `verification.md`, bound-feature registration on both carriers, one joint-acceptance row per `in-scope` runtime row) and have the stage's own U4 run `closure-acceptance-check.py` before it may emit its sentinel; a red checker is a stage failure, not a driver repair.

### F2 — The plan's declared recovery point for registration was overtaken and never reconciled

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/plan.md#L362-L369`
- **Evidence** (verbatim quote):

  ```
  This stage writes neither, and also writes no `.specify/register.md` row and no decision-archive entry. The registration set — the index row, the `.specify/features/110-context-management.md` detail (from `.specify/templates/feature-details-template.md`), the status advance, and any decision/register rows the three tensions would normally coin — is handed to the line close-out's Feature Integration Protocol as a recovery point
  ```

- **Why it's a problem**: The tree now carries the registry row and the detail (driver repair at implement), while the plan still tells a reader the set is missing until line close-out. Two artifacts state the same fact differently; a later close-out step reading the plan will look for work that is already done and cannot tell which reading is current.
- **Proposed fix**: When a driver repair consumes a plan-declared recovery point, amend the plan's § Feature Integration in the same repair (one line recording the registration landed early and by which commit), so the recovery point is retired rather than left dangling.

### F3 — No program checks that a `Pinning test` reference resolves

- **Severity**: P2
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/scripts/python/validate-tasks.py` (validator output against `tasks.md:121`)
- **Evidence** (verbatim quote):

  ```
  PASS: .specify/specs/110-context-management/tasks.md — 0 error(s), 0 warning(s)
  ```

  while `tasks.md:121` reads `| \`contracts/owner-and-layout.contract.md\` | C-005 | \`test_context_management_owner.py::test_form_legality_matrix_matches_the_owner_document\` | T024 |` and no such function exists (22 such rows).

- **Why it's a problem**: The validator proves the `[green:]` partition is internally consistent but never resolves the clause table's pinning-test names, so a renamed test leaves a broken link that passes every gate. The artifact finding F5 is the concrete instance; this is the tooling gap that lets it happen.
- **Proposed fix**: Extend `scripts/python/validate-tasks.py` with one check: every `*_test.py::test_*` token in a clause-coverage table MUST resolve to a `def test_…` in that file; report unresolved names as errors.

### F4 — The evidence landing set is not closed; a large evidence file landed outside every declared point

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/tasks.md#L68` (and `.specify/specs/110-context-management/baseline-failed.txt`)
- **Evidence** (verbatim quote):

  ```
  - **Evidence landing points (this feature)**: `.specify/specs/110-context-management/notes/{pre-change-measurements.md,red-first-evidence.md,quickstart-run.md}`, `.specify/specs/110-context-management/coverage-baseline.txt`, `.specify/specs/110-context-management/test-evidence/{…}`
  ```

  The spec root also carries `baseline-failed.txt` (21,944 bytes, 223 lines), which appears in no landing-point list and in no `plan.md` § Project Structure row.
- **Why it's a problem**: The tasks file declares a closed landing set, yet the implement run wrote an evidence file beside it. The next reader cannot tell whether an unlisted evidence file is sanctioned or residue, and the artifact segment's expected set has to guess.
- **Proposed fix**: Either add `baseline-failed.txt` to the declared landing points in `templates/commands/implement.md`'s Test runs bullet (its owner per `tasks.md:68`), or require evidence writers to place every capture under `test-evidence/`; then reconcile this spec's root files in the next touch.

### F5 — 22 of 39 clause-coverage pinning tests do not exist under the names written

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/tasks.md#L121`
- **Evidence** (verbatim quote of the C-005 row):

  ```
  | `contracts/owner-and-layout.contract.md` | C-005 | `test_context_management_owner.py::test_form_legality_matrix_matches_the_owner_document` | T024 |
  ```

  Enumerated unresolved references (file :: function), each absent from the named test module:
  `test_context_management_declarations.py` :: `test_domains_are_closed_sets_with_one_owner`, `test_engine_reads_facts_through_the_shared_reader`, `test_four_facts_carry_required_keys_and_registration`, `test_no_numeric_bound_and_cap_reference_form`, `test_presence_vocabulary_is_defined_once`, `test_roster_agreement_is_machine_checked`, `test_unknown_or_missing_declaration_member_is_refused`;
  `test_context_management_engine.py` :: `test_check_reports_the_closed_rule_set_deterministically`;
  `test_context_management_owner.py` :: `test_ambient_section_stays_summary_plus_pointer`, `test_baseline_composes_once_per_session_or_line`, `test_composer_roles_resolve_through_the_existing_relative_model`, `test_concept_pointer_and_protocol_boundary_guard`, `test_concept_pointer_slot_maps_onto_existing_channels_per_structure`, `test_concept_pointer_slot_structures_have_carriers_and_presence_surfaces`, `test_dispatch_mapping_keeps_the_existing_payload`, `test_existing_owners_are_not_redefined`, `test_form_legality_matrix_matches_the_owner_document`, `test_layer_landing_guard`, `test_reentry_recites_refreshes_delta_and_records_statement`, `test_source_drift_is_an_observed_record_change_not_a_poll`, `test_task_composition_selects_under_caps_without_widening`, `test_trigger_set_is_closed_at_seven`.
- **Why it's a problem**: The clause table is the artifact a maintainer uses to answer "which test pins C-0NN?". For 22 of 39 clauses the far end of that link has no target — the tests were authored under different names and the table was never reconciled. The `[green:]` partition passes because it is checked by a different mechanism, so the broken links stay invisible.
- **Proposed fix**: Reconcile every `Pinning test` cell against the landed modules in one pass (22 renames above) and add the F3 validator so the table cannot silently drift again.

### F6 — `empty` means two different things in requirements/data-model and in the owner document

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/requirements.md#L174`
- **Evidence** (verbatim quotes):

  ```
  `empty`（可解析但存储为空——0 字节文件或空目录）… 在场判定按来源的实际类型执行：普通文件看大小、目录看条目数
  ```
  ```
  | `empty` | every standing source resolves but the row's store is empty (0-byte file, empty directory) | same owner document |
  ```
  (data-model.md:156)
  ```
  | `empty` | 可解析但存储为空——0 字节文件、空目录，或只含 0 字节文件的目录存储 |
  ```
  (shared/definitions/context-management-definitions.md:78)

- **Why it's a problem**: The same vocabulary member is stated once with an entry-count rule (requirements, data-model) and once with a content-size rule for directories (owner document, and the shipped engine). A consumer reading FR-020 and one reading the owner document compute different presence tokens for a directory of empty files.
- **Proposed fix**: Pick one reading at the owner document and propagate it: either delete the zero-only branch from the owner document and the engine, or amend FR-020's `empty` definition and its entry-count sentence in the same change, and update data-model.md.

### F7 — FR-010 and FR-021 disagree on whether the audit reports decidable duplication

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/specs/110-context-management/requirements.md#L164`
- **Evidence** (verbatim quotes):

  ```
  **可判定的**内容重复由审计报告，恰为两种形状：任务行以 `read-in-full` 覆盖一个不变层行声明的来源；任务行以 `inline-digest` 覆盖一个被不变层行以 `read-in-full` 物化的来源。
  ```
  (FR-010)
  ```
  `--action check`（完整性：…——恰为九个规则 `roster-mismatch`、`roster-order`、`unknown-layer`、`unknown-form`、`layer-form-illegal`、`duplicate-class`、`empty-layer`、`cap-missing`、`category-column`；…）
  ```
  (FR-021; duplication is not among the nine)
  ```
  The audit reports the duplication where the row shape makes it decidable — exactly two shapes
  ```
  (contracts/matrix-and-triggers.contract.md C-027)

- **Why it's a problem**: Two MUST-level requirements cannot both hold as written: FR-010 assigns the two decidable shapes to "the audit", and FR-021 closes the audit's `check` rule set at nine rules with no duplication rule. The implementation silently resolved the contradiction in favour of FR-021 (recorded only inside a test docstring), so the requirement set still promises a reading no shipped surface delivers.
- **Proposed fix**: Ratify the resolution at the requirement owner: either state in FR-010 that the guard suite (not `--action check`) reports the two shapes and why, or widen FR-021's closed set with a tenth rule — and mirror the choice in C-027.

### F8 — The feature detail omits the template's `## Latest Review` section

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/.specify/features/110-context-management.md#L10`
- **Evidence** (verbatim quote from `.specify/templates/feature-details-template.md:19-21`):

  ```
  ## Latest Review
  ```

  (the template renders the heading followed by its summary placeholder token). The detail's heading sequence is `Overview → Key Changes → Implementation Notes → Status Criteria`; `## Latest Review` does not appear.
- **Why it's a problem**: The detail is the second verifiable carrier for review conclusions; without the section, the first review has nowhere to land its record and the carrier drifts from its template immediately. (This review's landing adds the section and the entry.)
- **Proposed fix**: Keep the heading when instantiating the template (write `No review yet.` when there is none), and have `/speckit.implement`'s registration step assert the heading exists.

### F9 — The `check` JSON face does not match FR-021's fixed key set

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/scripts/python/context-audit.py#L540`
- **Evidence** (verbatim quotes):

  ```
  `check` = `action`、`findings`（每项 `rule`、`file`、`line`、`message`）、`summary`（`total` 与 `by_rule` 计数）
  ```
  (requirements.md:175, FR-021)
  ```
  return {"rule": rule, "file": file_ref, "row": row, "line": line, "detail": detail}
  ```
  (context-audit.py:540; `_check_summary` also adds `"findings": len(findings)`)
  ```
  FINDING_KEYS = ["rule", "file", "row", "line", "detail"]
  ```
  (tests/contract/test_context_management_engine.py:63)

- **Why it's a problem**: A consumer written to the requirement's face reads `finding["message"]` and gets a `KeyError`; the tests were written to the implementation, so the drift is pinned rather than caught. The contract (C-032) names no sub-keys, so nothing but FR-021 decides — and the implementation contradicts it.
- **Proposed fix**: Decide the owner (FR-021 vs the shipped shape), then update the engine and its tests or the requirement in one change; add a key-set assertion that reads the chosen owner rather than a literal.

### F10 — The decidable-duplication reading never runs against the repository's own layout

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/tests/contract/test_context_management_engine.py#L593`
- **Evidence** (verbatim quotes):

  ```
  pristine = copy_case_to(tmp_path / "pristine", "all-present")
  pristine_doc = pristine / "shared" / "definitions" / "context-management-definitions.md"
  pristine_rows = _owner_layout_rows(pristine_doc.read_text(encoding="utf-8"))
  assert _decidable_duplications(pristine_rows) == [], (
      "the clean fixture must carry no decidable duplication")
  ```

  and the test docstring: "the engine's `check` rule set is closed at nine (C-032, PA-7), so the two shapes FR-010 makes decidable are reported by this guard's own reading of the layout table" (same file, lines 9–12).
- **Why it's a problem**: The guard's observable is a copy of the `all-present` fixture; the repository's own `shared/definitions/context-management-definitions.md` is never fed through `_decidable_duplications`. C-027's red condition — "the audit silently passes a decidable duplication" — therefore holds for the shipped tree: a future edit that turns `task-memory` into a `read-in-full` row over `.specify/constitution.md` would pass every shipped test.
- **Proposed fix**: Add one leg that runs `_decidable_duplications` over `_owner_text()`'s layout rows (and, if the requirement is repaired per F7, over the engine's chosen surface). Until then, record the clause as not guarded.

### F11 — A directory of 0-byte files reads `empty`, contradicting the entry-count rule

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/context-management/scripts/python/context-audit.py#L441`
- **Evidence** (verbatim quote):

  ```
  zero_only = all(
      entry.is_file() and not entry.is_symlink() and entry.stat().st_size == 0
      for entry in entries)
  if zero_only:
      return _reading(EMPTY_TOKEN, "empty: %s holds only 0-byte files" % source,
                      count, stat.st_mtime_ns)
  ```

  against FR-020's "普通文件看大小、目录看条目数" and its `empty` definition "0 字节文件或空目录".
- **Why it's a problem**: The reading is conservative (never reports a false `present`), but it is not the reading the requirement states: a directory with entries is judged by count, and none of those entries is a 0-byte *file* source. A session store full of empty placeholder entries reads `empty` where the requirement says `present`.
- **Proposed fix**: Same repair as F6 — one authoritative definition, engine and tests aligned; if the widened reading is wanted, state it in FR-020 and data-model.md.

## 4. What Worked — Preserve (Brief)

- The analyze gate blocked on two HIGH findings, the repair landed at the owner surfaces, and round 2 re-measured: the loop did what it is for.
- The per-rule mutation drill (`test-evidence/mutation-drill.txt`) makes all nine `check` guards credible — the red condition is the guard's verdict, not the engine's output.
- The owner document is a genuine single home: roster fact → layout table → engine → guards → mirrors all agree, and `sync-mirrors.py --check` reports all six pairs byte-identical.
- Read-only containment is mechanically demonstrated (AST write/socket scan, in-process socket blocking, before/after SHA-256 manifests), not asserted in prose.
- Acceptance evidence is real: red-first logs with failing counts, 223-vs-223 full-suite name comparison, existing non-empty evidence paths for every SC.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC_T1 — Close the implement hand-off at the stage.** Target: `templates/commands/implement.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`). Change: the hand-off block requires derived `verification.md`, both-carrier registration, and one joint-acceptance row per `in-scope` RS row; the stage runs `closure-acceptance-check.py` before emitting its sentinel. Source: F1. Expected impact: driver repairs stop masking stage gaps.
- **REC_T2 — Keep `## Latest Review` when instantiating the detail template.** Target: `templates/feature-details-template.md` + `templates/commands/implement.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/…`). Change: the heading is preserved with `No review yet.`; the registration step asserts it. Source: F8. Expected impact: the review carrier never starts out malformed.

### 5.3 Automation / Script Improvements

- **REC_A1 — Resolve clause-table test names.** Target: `scripts/python/validate-tasks.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/scripts/python/validate-tasks.py`). Change: error on a `*_test.py::test_*` token that does not resolve to a `def test_…` in that file. Source: F5, F3. Expected impact: renamed tests cannot orphan a clause.
- **REC_A2 — Declare the full-suite baseline path as a landing point.** Target: `templates/commands/implement.md` (Test runs bullet; absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`). Change: name `<spec>/baseline-failed.txt` (or `test-evidence/…`) as the declared landing point and have the evidence-landing list include it. Source: F4. Expected impact: no undeclared evidence at the spec root.

### 5.4 Workflow Improvements

- **REC_W1 — Retire a consumed recovery point.** Target: the repair procedure in `skills/external/sdd-loop-driver/` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/`). Change: when a driver repair consumes a plan-declared handoff, amend the plan in the same repair and cite the commit. Source: F2. Expected impact: plan and tree stop disagreeing about what is missing.
- **REC_W2 — Run the duplication reading over the repository layout.** Target: `tests/contract/test_context_management_engine.py` (or its owner surface). Change: one leg applies `_decidable_duplications` to the repository's own owner document and, if F7 is repaired toward the engine, to the audit output. Source: F10. Expected impact: C-027's red condition becomes reachable.

### 5.5 Documentation Improvements

- **REC_D1 — One `empty` definition across four surfaces.** Target: `shared/definitions/context-management-definitions.md` + this spec's `requirements.md` FR-020 + `data-model.md`. Change: choose the entry-count reading or the zero-only reading and state it once; align the engine and tests. Source: F6, F11. Expected impact: one presence reading for an empty-store directory.
- **REC_D2 — Ratify the duplication-reporting surface.** Target: this spec's `requirements.md` FR-010/FR-021 + `contracts/matrix-and-triggers.contract.md` C-027. Change: state that the guard suite reports the two shapes (with the reason the engine's nine rules do not), or add the tenth rule. Source: F7. Expected impact: requirement and delivery agree.
- **REC_D3 — Align the `check` JSON face with its owner.** Target: this spec's `requirements.md` FR-021 + `scripts/python/context-audit.py` + its tests. Change: decide `message` vs `detail`/`row` and update the other side; assert the key set from the owner. Source: F9. Expected impact: consumers can write against one face.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC_T1 — close the implement hand-off at the stage | `templates/commands/implement.md` | F1 |
| P1 | REC_A1 — resolve clause-table test names | `scripts/python/validate-tasks.py` | F5, F3 |
| P1 | REC_D1 — one `empty` definition | owner doc + FR-020 + data-model | F6, F11 |
| P1 | REC_D2 — ratify the duplication-reporting surface | FR-010/FR-021 + C-027 | F7 |
| P1 | REC_D3 — align the `check` JSON face | FR-021 + engine + tests | F9 |
| P1 | REC_W2 — run the duplication reading on the repo layout | engine guard | F10 |
| P2 | REC_T2 — keep `## Latest Review` | feature-details template | F8 |
| P2 | REC_A2 — declare the baseline landing point | implement command | F4 |
| P2 | REC_W1 — retire a consumed recovery point | sdd-loop-driver | F2 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `external` targets in this report.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.