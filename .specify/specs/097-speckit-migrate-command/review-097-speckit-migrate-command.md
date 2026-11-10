# Specification-Driven Development (SDD) Process Review Report: /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 097 |
| Requirement Key | 097-speckit-migrate-command |
| Requirement Name | /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态） |
| Related Feature | 024 Specification Workspace Versioning |
| Repository | spec-kit (published as `specify-cli` 0.0.22) |
| Repository URL | remotes are SSH-only: `gitee git@gitee.com:cloud-native-ai/spec-kit.git`, `github git@github.com:cloud-native-ai/spec-kit.git` (no HTTPS web remote) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (commit unpushed); cite absolute paths + `git show <sha>:<path>` |
| Branch | 097-speckit-migrate-command |
| Commit SHA | 3195519e28401fbb14def6d25cf17e4133311142 (short: 3195519e2) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command |
| Review Date | 2026-11-10 |
| Reviewer (Agent) | Qoder review session (four composed units: /speckit.review, skill:review-sdd-process, skill:review-feature-quality, skill:code-review) |
| Environment | Linux 5.10.134 x86_64; bash; CPython 3.11.11; pytest 8.4.2 via `scripts/bash/run-tests.sh` (parallel, `-n auto --dist load`) |
| spec-kit Source Snapshot | the same worktree at commit 3195519e2 (`.specify/` installed from this repo) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 236 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command/.specify/specs/097-speckit-migrate-command/requirements.md | 25 FR / 9 SC / 4 runtime-stack rows / 11 assumptions; SC-001…SC-004 are `final`-path |
| research.md | 101 | …/097-speckit-migrate-command/research.md | Phase-0 readings R-1…R-9, including the mirror-form divergence that decided T-002 |
| plan.md | 202 | …/097-speckit-migrate-command/plan.md | 14 WPs, T-001/T-002 decision tensions, EP-001…EP-006, mirror obligations, Project Structure |
| data-model.md | 143 | …/097-speckit-migrate-command/data-model.md | E-1…E-9 entities + invariants I-1…I-5 (E-8 owns dimension tokens/order) |
| contracts/migrate-cli.md | 87 | …/097-speckit-migrate-command/contracts/migrate-cli.md | Command surface C-1, preconditions C-2, outcome map C-3, envelope C-4, gate C-5, interface C-6, invariants C-7 |
| contracts/migrate-engine.md | 90 | …/097-speckit-migrate-command/contracts/migrate-engine.md | Expected-state sources C-2, disposition map C-3, reference-tree rules C-4, reuse boundary C-5, safety C-6, receipt/resume C-7, fixtures C-8 |
| contracts/migrate-template.md | 59 | …/097-speckit-migrate-command/contracts/migrate-template.md | Thin-projection contract T-1…T-6 for `/speckit.migrate` |
| quickstart.md | 84 | …/097-speckit-migrate-command/quickstart.md | Six user journeys; still carries its plan-stage "not implemented" status text |
| tasks.md | 999 | …/097-speckit-migrate-command/tasks.md | 48 rows, T001–T048, package map pkg01–pkg07, DoD-1…DoD-10, GATE-1…GATE-6 |
| verification.md | 165 | …/097-speckit-migrate-command/verification.md | SC-001…SC-009 status rows, smoke record, nine evidence bindings, DoD/GATE readings |
| feature-ref.md | 53 | …/097-speckit-migrate-command/feature-ref.md | Feature 024 binding + FR→WP matrix (25/25) |

## 1. Process Execution Timeline

Reconstructed from `git log` scoped to the spec directory (every stage artifact is committed under its producing command's commit on this branch), plus the working-tree state for the uncommitted residue.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` authors the spec (16:30) | 79bfaf180 `docs(097…): requirements — author the one-shot migrate wrap-up spec`; run records 5b0bdc539 / 92873ad87 | None. `checkpoints/01-requirements.md` produced but left untracked (row 16) |
| 2 | `/speckit.clarify` binds Feature 024 and pins sources/safety (16:38) | 7ca4dfa63 `clarify — bind 024, pin sources and safety semantics` | None; `checkpoints/02-clarify.md` left untracked |
| 3 | `/speckit.plan` produces Phase 0/1 artifacts (17:04–17:07) | 76603af9d → 979697118 (12/12 audit findings closed) → 96df5d2f5 | None; registry advanced Draft → Planned as designed |
| 4 | `/speckit.tasks` cuts 48 rows, freezes coverage baseline (17:19) | ca866399d; `DoD Status: pending` written (tasks.md:44) | None at this stage |
| 5 | `/speckit.checklist` produces 39 CHK items (17:29) | 70bfe20cd | None |
| 6 | `/speckit.analyze` round 1 — 51 findings (2C/9H/27M/13L) (17:44) | 8c6a727f6 | None |
| 7 | Analyze repair round 1 — 11 C/H fixed (17:54) | aef2a7ecf | Repair loop by design |
| 8 | Analyze round 2 — 3 HIGH pending independent validation, 55 open (18:13) | b73cf63a2 | None |
| 9 | Analyze repair r3 — W3-09/15/16/18 fixed; **carriers forced to `verification.log` + `.gitignore` negation added** (20:18) | b94eea72f; `analyze-repair-dispositions-r3-2026-11-10.md` W3-16/W3-18 | Deviation: the repair bound the feature to a constitution literal that was about to be corrected |
| 10 | Analyze round 3 — 0 open C/H, 51 open M/L (20:41) | 4194e0ebb | The 51 open M/L enter implement with no disposition record (F3) |
| 11 | `/speckit.implement` pkg01 — baselines frozen, env probed | 5a92d5196 | None |
| 12 | Constitution amended 1.19.0 → 1.19.1: Principle VII carrier `verification.log` → `verification.md` | 27ccbab93; `.specify/constitution.md` Sync Impact Report | Deviation: mid-implement owner change; Sync Impact inventory misses two live docs (F5) |
| 13 | Implement pkg02–pkg06 — engine, safety, cross-version, template | a561fac83, 30a2d456e, f3b3a7a2d, 552c723b8, 5ca92c533 | None; serial on `src/specify_cli/__init__.py` by declared `write-conflict` |
| 14 | Carrier fix — feature artifacts reverted to `verification.md` | 1b2d998c6 `fix: align the verification carrier with constitution VII (verification.md)` | Repair of the row-9/row-12 collision; `.gitignore` negation removed, its comment left (nitpick in the code record) |
| 15 | Implement pkg07 — polish, final gate, verification.md (48/48 rows closed) | 3195519e2 | Deviation: no commit touches `.specify/features.md` or the 024 detail — the `Planned → Implemented` flip is never landed (A1) |
| 16 | `/speckit.review` (this run) | `git status --short` at run start: `M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`; untracked `checkpoints/01-requirements.md`, `checkpoints/02-clarify.md`, `test-evidence/analyze-validation-round2-2026-11-10.md` | Deviation: four upstream uncommitted paths — disclosed, not reviewed (see §2.1) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 8 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 7 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 10 |
| Documentation | 5 |

Count convention: the P-family roll-up covers the process findings of §3 (F1–F6), the artifact-segment findings of §2.2 (A1–A9) and the implementation-segment finding of §2.3 (I1). The code segment's six-level record is separate and is never merged into this table (§2.1).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base (`git-delta-review.sh base --spec …`) |
| Head commit | 3195519e28401fbb14def6d25cf17e4133311142 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier the code segment reported |
| Renderer mode | text | the code record's header marker (`renderer: text`; no delta binary / non-TTY) |
| Changed / judged / skipped / gap files | 123 / 97 / 26 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | blocked | one `blocking` entry (`[BLOCKING]` heading) in the current record |
| Gate verdict | blocking-unresolved | `report --summary --file code-review.md` exited 1 (`gate=deny`) |
| Reason, when one applies | none | — |
| Uncommitted scope | 4 uncommitted paths were disclosed and are not part of the review object: `M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`; untracked `.specify/specs/097-speckit-migrate-command/checkpoints/01-requirements.md`, `.specify/specs/097-speckit-migrate-command/checkpoints/02-clarify.md`, `.specify/specs/097-speckit-migrate-command/test-evidence/analyze-validation-round2-2026-11-10.md`; no conclusion is issued over this scope | the same sentence lives in `.specify/specs/097-speckit-migrate-command/code-review.md` |
| Record | .specify/specs/097-speckit-migrate-command/code-review.md | written because the triage value is `run` |
| Archive | none | first run |

Code findings (six-level family, read in the record): 1 `blocking` — `tests/integration/test_migrate_us2_safety.py:273` `test_symlink_support_probe_is_zero_write` cannot fail (the probe takes no workspace and runs in the system temp dir, so both assertions are unfailable), i.e. the FR-006/C-7 zero-write claim has no functioning guard; 2 `important` — the `--help` zero-side-effect limb is unfailable (`tests/contract/test_migrate_cli_surface.py:81`), and `contracts/migrate-cli.md:19` + `docs/reference/commands/migrate.md:25` promise a `-h` option the CLI rejects (verified: `specify migrate -h` exits 2); 8 `suggestion`, 1 `nitpick`, 1 `praise`.

**Status-transition judgment (`Implemented → Ready for Review`): refused — status left at `Planned`.** Named conditions: (1) the transition's From-state does not match — the bound feature claims `Planned` (`.specify/features.md:33`, `.specify/features/024-specification-workspace-versioning.md:6`), so `Implemented → Ready for Review` is not a legal transition for it; (2) the current code-segment record contains one `blocking` entry. The Acceptance Reality Check raises no refusal of its own (§2.4). Repair path: land `Planned → Implemented` through the implement status step (all four `Planned → Implemented` conditions already pass per `closure-acceptance-check.py`), fix the blocking test defect, then re-run `/speckit.review` (which rotates `code-review.md`); no waiver was presented and none is inferred.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, research.md, plan.md, data-model.md, contracts/ (3 files), quickstart.md, feature-ref.md, tasks.md, verification.md | derived from the stage rules plus `plan.md` § Project Structure (the plan declares research.md and feature-ref.md beyond the standard seven) |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | blocked | one `P0` finding (A1) below |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | .specify/features/024-specification-workspace-versioning.md | 6 | none | A1 — the feature claims `Planned` while all four `Planned → Implemented` conditions pass (checker `accept`, `final_path` 4/4 pass, zero open rows, smoke pass); the `Implemented → Ready for Review` transition is unavailable from `Planned`. The registry row agrees with the detail (`.specify/features.md:33`), so both carriers are stale together. (validated: confirm, independent read-only subagent) |
| P1 | .specify/specs/097-speckit-migrate-command/verification.md | 27 | none | A2 — `smoke_command` is not the command that produced `final-suite.txt`: the recorded literal omits `--names-out .specify/.tmp/pkg07/final-failed.txt`, which the evidence file's §Command block shows was executed. A re-run of the recorded literal passes (103 passed, exit 0), so the substance holds but the "verbatim" record is inaccurate. |
| P1 | .specify/specs/097-speckit-migrate-command/verification.md | 107 | none | A3 — the SC-007 evidence pointer attributes the sanitize-lane reading to `us1-converge.txt`, which contains no sanitize reading at all; the support lives in `skills/internal/sanitize-materials/SKILL.md:164-178` and the mirror pair in `mirror-verify.txt`. |
| P1 | .specify/specs/097-speckit-migrate-command/contracts/migrate-cli.md | 19 | none | A4 — C-1's option table declares `--help` / `-h` accepted; the CLI registers only `--help` and `specify migrate -h` exits 2 (verified 2026-11-10). `docs/reference/commands/migrate.md:25` repeats the claim; `templates/commands/migrate.md:24` points at `--help` for envelope keys that `--help` does not list. |
| P1 | .specify/specs/097-speckit-migrate-command/contracts/migrate-cli.md | 62 | none | A5 — C-4 lists `workspace` among the receipt's volatile fields, and `docs/reference/commands/migrate.md:44` lists "workspace path" as a receipt field, but `_migrate_receipt_payload` has no `workspace` key and E-3 omits it. This is analyze finding W2-02, carried open, now materialized. |
| P2 | .specify/specs/097-speckit-migrate-command/verification.md | 87 | none | A6 — the SC-002 note says four in-suite mutations each turn the corresponding assertion red; the fourth (`us2-safety.txt:39` `MUT-existence-only exists=True byte-identical=3/4 => existence-only-would-pass=yes`) shows the weakened reading stays green while the byte assertion reds — a check-power drill, not a product mutation. |
| P2 | .specify/specs/097-speckit-migrate-command/quickstart.md | 5 | none | A7 — the page still declares the command unimplemented and every `specify migrate` example unexecuted ("本命令尚未实现… 凡以 `specify migrate` 开始的示例都**未被执行**"), contradicted by `notes/quickstart-run.md` (scenarios 1–5 executed, driver `all_pass=True`) and commit 3195519e2 (T045). |
| P2 | .specify/features/024-specification-workspace-versioning.md | 55 | none | A8 — the `Planned` DoD line still reads "Version schema and migration registry designed", contradicting the supersession recorded at line 18 (no `.specify/version` marker, no version→migration registry). |
| P2 | .specify/specs/097-speckit-migrate-command/tasks.md | 44 | none | A9 — `**DoD Status**: pending` was never updated although `verification.md` records DoD-1…DoD-10 all pass and all 48 rows are closed. |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | 3195519e28401fbb14def6d25cf17e4133311142 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier `git-delta-review.sh` reported |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_migrate_cli_surface.py tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/contract/test_migration_distribution.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/integration/test_migrate_us1_converge.py tests/integration/test_migrate_us2_safety.py tests/integration/test_migrate_us3_crossversion.py tests/integration/test_migrate_us4_equivalence.py -q` | recorded verbatim from verification.md:27 |
| Smoke exit code | 0 | re-run of the recorded literal this session: `103 passed in 23.88s`, exit 0 |
| Smoke evidence path | .specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt | exists and non-empty (4,929 B; `103 passed`; `# exit=0`); this session's re-run transcript: `.specify/.tmp/review-097/smoke-rerun.txt` |
| Scope and regression verdict | pass — every hunk traces to a declared FR/task row (engine pkg02–pkg05, template+assembly pkg06, polish pkg07, registry/027-contract side effects of FR-021, constitution amendment 1.19.1); the touched-contract pins moved coherently 29→30; the feature subset shows zero NEW failures against the recorded 278-name baseline (final-suite.txt §Failure-name comparison, `new_count=0`) | this segment's own reading |
| Segment verdict | pass | one `P1` finding below; no P0 |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | .specify/specs/097-speckit-migrate-command/verification.md | 27 | none | I1 — the smoke record's command literal is not the executed command (the executed run carried `--names-out .specify/.tmp/pkg07/final-failed.txt`); the smoke triple holds only after a re-run of the recorded literal. Record the executed command verbatim (see also A2). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Planned | the bound feature detail, copied |
| `final_path` record, copied verbatim (7/7) | pass [4] · blocked [0] · deferred [0] · partial [0] · fail [0] · unknown [0] · total [4] | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/097-speckit-migrate-command --feature-detail .specify/features/024-specification-workspace-versioning.md --json`, never recomputed here |
| Comparison verdict | agree | neither refusal condition fires (verdict `accept`; the claim is not `Implemented`/`Ready for Review` with a zero `pass` bucket) |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The checker's own completion conditions all read true: `every_final_path_pass=true`, `no_open_rows=true`, `smoke_record_pass=true`, `status_row_per_criterion=true`. The missing action is the status flip, not the work.

## 3. Findings (Problems & Improvement Targets)

### F1 — The line state spine still says "stalled at analyze round 2" while round 3 and the whole implement stage landed

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/state/097-speckit-migrate-command.md
- **Evidence** (verbatim quote):

  ```
  spine_state: stalled
  stage: analyze (round 2)
  last_verdict: analyze round-2 gate FAIL (3 validated HIGH remain; repair-round bound reached) — U5 stop-line
  ```

  The branch meanwhile carries 4194e0ebb ("analyze round 3 — r3 repairs validated, 0 open C/H") and six implement commits through 3195519e2.

- **Why it's a problem**: the state carrier is what any reentry reads first; it now contradicts the branch it describes, so a resumed run would re-run analyze round 2 or treat a completed implement stage as never started. The spine is written outside the worktree, so nothing in the branch's own history corrects it.
- **Proposed fix**: reconcile the spine to the actual stage (or add a stage-close assertion that compares `stage`/`stage_base_commit` against `git log` HEAD before a line may be re-entered); owner: the SDD loop-driver's state spine step.

### F2 — An owner-level conflict was first forced onto feature artifacts, then the owner was amended, forcing a second repair

- **Severity**: P1
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md (W3-16/W3-18) × .specify/constitution.md (1.19.1 Sync Impact Report) × commit 1b2d998c6
- **Evidence** (verbatim quote):

  ```
  | W3-16 | HIGH | confirm | fixed | `tasks.md:113`（pkg07 写域） | `verification.md` 全文件仅存于 pkg07 写域一处，与 T048/DoD-7/GATE-4/宪法 VII 的 `verification.log` 冲突；pkg07 写域改为 `verification.log` 后 …
  ```

  Two commits later: `-  **Pre-Status-Flip Gate** (Planned→Implemented): … in `verification.log`` → `+  … in `verification.md`` (27ccbab93), then 1b2d998c6 reverted the feature artifacts; the `.gitignore` negation added for W3-18 was removed but its comment stayed (`.gitignore:38`).

- **Why it's a problem**: the analyze repair round paid to bind the feature to a literal that the next upstream decision removed. The root cause was an owner-level fork (constitution vs mechanism), yet the repair was applied one level down, at the artifacts, and had to be re-applied. Two commits and one repair row were spent on a round trip.
- **Proposed fix**: extend the analyze repair disposition rules — when a finding's root is a conflict between two owners (here: constitution § VII vs the framework chain), the disposition is "route to the owner", not "coerce the artifact", and the artifact-side change waits for the owner's ruling.

### F3 — Fifty-plus open analyze MEDIUM/LOW findings entered implement with no disposition record, and two of them recurred as live defects

- **Severity**: P1
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-r3-2026-11-10.md
- **Evidence** (verbatim quote):

  ```
  | W2-02 | carried-over | data-model.md:41 E-2 / :55–71 E-3 / migrate-cli.md:62–65 C-4 | 回执 `workspace` 字段三处不一致：E-2 称记录、C-4 列为易变字段、E-3 schema 无该字段。 | data-model E-3 / migrate-cli C-4 |
  ```

  and §S-6: `断点：W2-02、W2-16、W2-20、W2-03、W3-10（carried）。` The round-3 gate (4194e0ebb) records "0 open C/H, 51 open M/L"; no implement-stage record dispositions them, and W2-02 materialized as A5 while W1-25/W3-05 (SC-007 has no line-level acceptance surface) materialized as A3.

- **Why it's a problem**: an analysis backlog without a consumption lane is a promise nobody keeps. The M/L findings that predicted the exact review defects were carried silently; the implement stage could not distinguish "accepted risk" from "not yet read".
- **Proposed fix**: add an implement-entry disposition step for open analyze findings — fix / waiver with owner / carry with a named owner — recorded on one list; or make the analyze gate emit a machine-readable backlog that `/speckit.implement` must consume.

### F4 — Prior-stage checkpoints were never committed; the committed timeline cannot cover the requirements and clarify stages

- **Severity**: P2
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/checkpoints/
- **Evidence** (verbatim quote):

  ```
  ?? .specify/specs/097-speckit-migrate-command/checkpoints/01-requirements.md
  ?? .specify/specs/097-speckit-migrate-command/checkpoints/02-clarify.md
  ```

  (from `git status --short` at review start; `checkpoints/03-plan.md` is committed)

- **Why it's a problem**: the artifact-commit step exists to keep each stage's product on the branch (see `shared/workflow/artifact-commit-step.md` § Why); two of three checkpoints fall outside it, so the review's timeline rows 1–2 rest on run-record timestamps rather than the stage products.
- **Proposed fix**: either commit a stage's checkpoint with the stage, or declare `checkpoints/` as intentionally untracked scratch in the loop-driver contract so the deviation is not repeated as a finding each run.

### F5 — The constitution amendment's Sync Impact inventory misses two live documents that still name `verification.log`

- **Severity**: P2
- **Category**: Documentation
- **Location**: .specify/constitution.md (Sync Impact Report) × docs/concepts/better-harness.md × docs/reference/history/00-cross-cutting-lessons.md
- **Evidence** (verbatim quote):

  ```
  - Templates requiring updates:
    ✅ shared/guidelines/better-harness.md (+ .specify mirror) — the two sensor references now name verification.md
    ✅ tests/contract/test_fast_fail_discipline.py — live version pin 1.19.0 → 1.19.1
  ```

  but `docs/concepts/better-harness.md:32` still reads `Test-First, checklist, analyze, verification.log`, and `docs/reference/history/00-cross-cutting-lessons.md:67` still reads `每个成功标准(SC)在 verification.log 有状态行`.

- **Why it's a problem**: the amendment declares its carrier sweep complete; two live guidance docs keep the old name, so a reader following either lands on a file the framework chain never reads. The report is a completeness claim, and it is false.
- **Proposed fix**: add both docs to the Sync Impact inventory and correct them (or explicitly rank the lessons file as a dated record); the amendment checklist should enumerate live docs by grep, not by memory.

### F6 — Evidence bookkeeping has no machine check; three pointer defects survived the implement gate

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: .specify/specs/097-speckit-migrate-command/verification.md
- **Evidence** (verbatim quote):

  ```
  smoke_command=bash scripts/bash/run-tests.sh tests/contract/… -q
  ```

  versus the evidence file's own header: `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/pkg07/final-failed.txt \`; and `SC-007_value=us1-converge.txt: …` where that file contains no sanitize reading.

- **Why it's a problem**: all three defects (A2, A3, A6) are mechanically detectable — resolve each evidence path, compare the smoke literal with the run header, and require one reading per claimed value. None is checked today, so each implement run re-earns the right to drift.
- **Proposed fix**: add a verification-pointer check to the closure checker (or the implement gate): every `evidence_path`/`SC-*_value` pointer resolves to an existing file, and the recorded smoke command matches the header of the file it cites.

## 4. What Worked — Preserve (Brief)

- The single-engine posture held: `specify migrate` is the only executor; `copy_local_templates`, `sanitize-utils` checkers, `anchor-layout-migrate` and the sync/regen checkers are consumed, not copied; the T-002 split (framework-source vs client) is backed by a measured fact (mirror ≠ `rewrite_paths(source)`).
- Domain constants have one owner and the contract tests extract them from the owner files (dimension tokens from data-model E-8, disposition domain from requirements FR-014) — owner drift cannot pass silently.
- Deterministic plan payload: volatile fields (run id, timestamps, absolute workspace) excluded; repeated dry-runs are byte-identical, which is what makes "zero write" measurable.
- Receipt discipline: one file per run, exclusive create, per-item flush, archive-before-write, resume judged from the old receipt's own `archiveTo` paths — the interruption drill proves no second move.
- The declarative fixture builders re-check every constructed name against its owner at build time, so a stale fixture fails loudly instead of passing quietly.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **Pointer-resolution check in the closure chain** — Target: `scripts/python/closure-acceptance-check.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command/scripts/python/closure-acceptance-check.py). Change: add a read-only check that every `evidence_path`/`SC-*_value` pointer in `verification.md` resolves and that `smoke_command` matches the header of the file it cites. Source: F6 (A2/A3). Expected impact: the three pointer defects of this feature become gate failures instead of review findings.
- **Spine-vs-history reconciliation** — Target: the SDD loop-driver's state spine step (owner: `.specify/skills/external/sdd-loop-driver/`). Change: before a line is re-entered, assert that the spine's `stage` and `stage_base_commit` agree with the branch history; mismatch surfaces as an anomaly. Source: F1. Expected impact: a stalled spine can no longer describe a running line.

### 5.4 Workflow Improvements

- **Enforce the registry flip in the implement stage** — Target: `templates/commands/implement.md` (absolute supplement: …/templates/commands/implement.md) and the stage-closing checklist it points at. Change: make the `Planned → Implemented` flip an explicit closing step whose absence fails the stage (the four conditions are already machine-checked by `closure-acceptance-check.py`). Source: A1. Expected impact: the review gate stops receiving features whose status carrier lags their work.
- **Owner-conflict routing in analyze repair** — Target: `skills/internal/analyze-artifacts/SKILL.md`. Change: when a finding's root is a conflict between two owners, dispose as "route to the owner" and defer the artifact change until the owner rules. Source: F2. Expected impact: no more double repairs like W3-16/W3-18 → 27ccbab93 → 1b2d998c6.
- **A consumption lane for open analyze findings** — Target: `templates/commands/implement.md` + `templates/tasks-template.md`. Change: at implement entry, require a disposition row per open analyze finding (fix / waiver owner / carry owner). Source: F3. Expected impact: carried M/L findings stop materializing as review defects without attribution.
- **Checkpoint commit discipline** — Target: the SDD loop-driver contract. Change: commit each stage's checkpoint with its stage, or declare `checkpoints/` untracked scratch. Source: F4. Expected impact: the review timeline can cite stage products, not run-record timestamps.

### 5.5 Documentation Improvements

- **Align the `-h` claim and the envelope pointer** — Target: `templates/commands/migrate.md` and the command-docs baseline (`docs/reference/commands/migrate.md`); the contract is a feature artifact and is fixed in the feature's own repair. Change: point at contract C-4 or the docs page instead of `--help` for envelope keys; the docs page's option table must match the registered Typer options. Source: A4. Expected impact: no user-facing promise the CLI rejects.
- **Carrier sweep completeness** — Target: `.specify/constitution.md` Sync Impact Report procedure + the two stale docs (`docs/concepts/better-harness.md:32`, `docs/reference/history/00-cross-cutting-lessons.md:67`). Change: enumerate live carrier references by grep and list them in the report. Source: F5. Expected impact: an amendment's completeness claim becomes checkable.
- **Quickstart status honesty** — Target: the feature's `quickstart.md`; the mechanism-side lesson belongs to `templates/commands/plan.md`'s guidance on "not implemented" status text. Change: a quickstart that later runs its scenarios must flip its own status declaration in the same change that records the runs. Source: A7. Expected impact: readers stop being told a shipped command does not exist.

(No Template or Command Prompt recommendations survived triage; dropped rather than padded.)

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Land `Planned → Implemented` for Feature 024, then re-run the review gate | `.specify/features.md` + `.specify/features/024-specification-workspace-versioning.md` (via the implement status step) | A1 |
| P1 | Fix the unfailable zero-write test and re-run the code segment | `tests/integration/test_migrate_us2_safety.py:273` | code record `[BLOCKING]` |
| P1 | Reconcile the stale state spine | `.specify/state/097-speckit-migrate-command.md` | F1 |
| P1 | Route owner-level conflicts to the owner before coercing artifacts | `skills/internal/analyze-artifacts/SKILL.md` | F2 |
| P1 | Consume open analyze findings at implement entry | `templates/commands/implement.md` | F3 |
| P1 | Repair the three evidence-pointer defects (smoke literal, SC-007 pointer, SC-002 note) | `verification.md:27/87/107` | A2, A3, A6, I1 |
| P1 | Align the `-h`/envelope claims with the CLI | `contracts/migrate-cli.md` (feature repair) + docs baseline | A4 |
| P1 | Remove the phantom `workspace` receipt field from C-4 and the docs | `contracts/migrate-cli.md:62` (feature repair) + docs baseline | A5 |
| P2 | Fix quickstart status text, 024 Planned criteria line, tasks DoD status | feature artifacts + `plan.md` guidance | A7, A8, A9 |
| P2 | Complete the constitution carrier sweep; add pointer checks; checkpoint discipline | `.specify/constitution.md`, `closure-acceptance-check.py`, driver contract | F4, F5, F6 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `REC-…` ids were coined in this report, so no identifier was registered.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. One P0 was raised (A1) and confirmed by an independent fresh-context read-only validation subagent (verdict: `confirm`), which re-read both carriers, re-ran the closure checker and verified the state machine's transition table. The code record's single `blocking` entry was likewise confirmed by a fresh-context read-only test-review pass.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
