# Specification-Driven Development (SDD) Process Review Report: /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

> **This is review round 2.** The round-1 record is archived at `.specify/specs/097-speckit-migrate-command/review-097-speckit-migrate-command.md`; the round-1 code record is archived at `.specify/specs/097-speckit-migrate-command/code-review-20261110T161419Z.md`. This report stands alone: it re-runs all four segments and the Acceptance Reality Check against the current tree (HEAD `da34a3d44`), and it re-verifies every round-1 P0/P1 repair anchor.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 097 |
| Requirement Key | 097-speckit-migrate-command |
| Requirement Name | /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态） |
| Related Feature | 024 Specification Workspace Versioning |
| Repository | spec-kit (published as `specify-cli` 0.0.22) |
| Repository URL | remotes are SSH-only: `gitee git@gitee.com:cloud-native-ai/spec-kit.git`, `github git@github.com:cloud-native-ai/spec-kit.git`, `gitlab git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`; `origin` is the upstream `git@github.com:github/spec-kit.git` (no HTTPS web remote) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (commit unpushed); cite absolute paths + `git show <sha>:<path>` |
| Branch | 097-speckit-migrate-command |
| Commit SHA | da34a3d44132852a348b61ba0be64ea8efcffef9 (short: da34a3d44) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder review session (four composed units: /speckit.review, skill:review-sdd-process, skill:review-feature-quality, skill:code-review) |
| Environment | Linux 5.10.134 x86_64; bash; CPython 3.11.11; pytest 8.4.2 via `scripts/bash/run-tests.sh` (parallel, `-n auto --dist load`) |
| spec-kit Source Snapshot | the same worktree at commit da34a3d44 (`.specify/` installed from this repo) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 236 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command/.specify/specs/097-speckit-migrate-command/requirements.md | 25 FR / 9 SC / 4 runtime-stack rows / 11 assumptions; SC-001…SC-004 are `final`-path |
| research.md | 101 | …/097-speckit-migrate-command/research.md | Phase-0 readings R-1…R-9, including the mirror-form divergence that decided T-002 |
| plan.md | 202 | …/097-speckit-migrate-command/plan.md | 14 WPs, T-001/T-002 decision tensions, EP-001…EP-006, mirror obligations, Project Structure |
| data-model.md | 144 | …/097-speckit-migrate-command/data-model.md | E-1…E-9 entities + invariants I-1…I-5 (E-8 owns dimension tokens/order; E-3 now carries the receipt `workspace` key) |
| contracts/migrate-cli.md | 87 | …/097-speckit-migrate-command/contracts/migrate-cli.md | Command surface C-1 (`--help` only), preconditions C-2, outcome map C-3, envelope C-4 (incl. receipt `workspace`), gate C-5, interface C-6, invariants C-7 |
| contracts/migrate-engine.md | 90 | …/097-speckit-migrate-command/contracts/migrate-engine.md | Expected-state sources C-2, disposition map C-3, reference-tree rules C-4, reuse boundary C-5, safety C-6, receipt/resume C-7, fixtures C-8 |
| contracts/migrate-template.md | 59 | …/097-speckit-migrate-command/contracts/migrate-template.md | Thin-projection contract T-1…T-6 for `/speckit.migrate` |
| quickstart.md | 84 | …/097-speckit-migrate-command/quickstart.md | Six user journeys; status declaration now states the repository-source implementation and the executed scenarios |
| tasks.md | 380 | …/097-speckit-migrate-command/tasks.md | 48 rows, T001–T048, package map pkg01–pkg07, DoD-1…DoD-10 (`DoD Status: pass`), GATE-1…GATE-6 |
| verification.md | 177 | …/097-speckit-migrate-command/verification.md | SC-001…SC-009 status rows, re-executed smoke record, nine evidence bindings (all sha256 match), DoD/GATE readings, closure verdict block |
| feature-ref.md | 53 | …/097-speckit-migrate-command/feature-ref.md | Feature 024 binding + FR→WP matrix (25/25) |

## 1. Process Execution Timeline

Reconstructed from `git log` scoped to the spec directory (every stage artifact is committed under its producing command's commit on this branch), plus the working-tree state for the uncommitted residue. Rows 1–15 are the round-1 reconstruction (still accurate); rows 16–20 are the review repair cycle this report re-judges.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` authors the spec | 79bfaf180; `checkpoints/01-requirements.md` produced but left untracked (row 17) | None |
| 2 | `/speckit.clarify` binds Feature 024 and pins sources/safety (16:38) | 7ca4dfa63 | None; `checkpoints/02-clarify.md` left untracked |
| 3 | `/speckit.plan` produces Phase 0/1 artifacts | 76603af9d → 979697118 (12/12 audit findings closed) → 96df5d2f5 | None; registry advanced Draft → Planned |
| 4 | `/speckit.tasks` cuts 48 rows, freezes coverage baseline | ca866399d | None at this stage |
| 5 | `/speckit.checklist` produces 39 CHK items | 70bfe20cd | None |
| 6 | `/speckit.analyze` round 1 — 51 findings (2C/9H/27M/13L) | 8c6a727f6 | None |
| 7 | Analyze repair round 1 — 11 C/H fixed | aef2a7ecf | Repair loop by design |
| 8 | Analyze round 2 — 3 HIGH pending independent validation, 55 open | b73cf63a2 | None |
| 9 | Analyze repair r3 — W3-09/15/16/18 fixed; carriers forced to `verification.log` + `.gitignore` negation added | b94eea72f; `analyze-repair-dispositions-r3-2026-11-10.md` W3-16/W3-18 | Deviation: the repair bound the feature to a constitution literal that was about to be corrected (F1 below) |
| 10 | Analyze round 3 — 0 open C/H, 51 open M/L | 4194e0ebb | The 51 open M/L enter implement with no disposition record (F2 below) |
| 11 | `/speckit.implement` pkg01 — baselines frozen, env probed | 5a92d5196 | None |
| 12 | Constitution amended 1.19.0 → 1.19.1: Principle VII carrier `verification.log` → `verification.md` | 27ccbab93; Sync Impact Report | Deviation: mid-implement owner change; the Sync Impact inventory misses two live docs (F4 below) |
| 13 | Implement pkg02–pkg06 — engine, safety, cross-version, template | a561fac83, 30a2d456e, f3b3a7a2d, 552c723b8, 5ca92c533 | None; serial on `src/specify_cli/__init__.py` by declared `write-conflict` |
| 14 | Carrier fix — feature artifacts reverted to `verification.md` | 1b2d998c6 | Repair of the row-9/row-12 collision; `.gitignore` negation removed, its comment left (nitpick in the code record) |
| 15 | Implement pkg07 — polish, final gate, verification.md (48/48 rows closed) | 3195519e2 | Deviation: no commit touches `.specify/features.md` or the 024 detail — the `Planned → Implemented` flip was never landed (round-1 A1) |
| 16 | `/speckit.review` round 1 — four segments + ARC; `Implemented → Ready for Review` refused `blocking-unresolved` | 432a3d640; archived `review-097-speckit-migrate-command.md` + `code-review-20261110T161419Z.md` | None; review gate blocked on the code record's single `blocking` entry plus the missing From-state |
| 17 | Review round-1 run records and close-out | 21d25a4f4 (run determination ×4, exec-quant ×4, feedback ×4), 9807076e3 (close-out receipt) | None |
| 18 | Review-repair r1 — status flip, zero-write guard rebuild, evidence pointers, C-1 `--help` convergence, receipt `workspace` key | da34a3d44; `review-repair-dispositions-r1-2026-11-10.md` | Repair round by design; all 1 P0 / 8 P1 / 1 `blocking` / P2 quick wins addressed |
| 19 | `/speckit.review` round 2 (this run) — four segments + ARC, transition allowed | this report; `code-review.md` (`not-evaluated`, 147/107/40/0, gate `allow`); ARC `accept`, `final_path` pass 4/4 | None; status flipped to `Ready for Review` after both records landed |
| 20 | Working-tree residue at review start | `git status --short`: `M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`; untracked `checkpoints/01-requirements.md`, `checkpoints/02-clarify.md`, `test-evidence/analyze-validation-round2-2026-11-10.md` | Disclosed, not reviewed (see §2.1 `Uncommitted scope`); F3 below |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 3 |
| Workflow | 3 |
| Documentation | 1 |

Count convention: the P-family roll-up covers the process findings of §3 (F1–F7), the artifact-segment findings of §2.2 (none) and the implementation-segment findings of §2.3 (none). The code segment's six-level record is separate and is never merged into this table (§2.1).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | `git-delta-review.sh base --spec …` |
| Head commit | da34a3d44132852a348b61ba0be64ea8efcffef9 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier the code segment reported |
| Renderer mode | text | the code record's header marker (`renderer: text`; no delta binary / non-TTY) |
| Changed / judged / skipped / gap files | 147 / 107 / 40 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | not-evaluated | no `blocking` entry, but 40 legal `generated` skips — C-37 withholds `pass` from any run carrying skips |
| Gate verdict | allow | `report --summary --file code-review.md` exited 0 (0 `blocking`, 0 `important`) |
| Reason, when one applies | `skipped_files=40` — legal `generated` skips: run records (`exec-quant/records/*.json`, `retention/closeout/*.json`, `session/*.md`) and raw suite dumps (`baseline-failed.txt`, `coverage-baseline.txt`, analyze gate transcripts, `implement-entry-*.txt`, `pkg0*-full-*.txt`); the remaining 107 changed files were read and judged | the receipt's skip rows |
| Uncommitted scope | 6 uncommitted paths were disclosed and are not part of the review object: `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`; the deleted `review.md` and the two records this run rotates; `checkpoints/01-requirements.md`, `checkpoints/02-clarify.md`, `test-evidence/analyze-validation-round2-2026-11-10.md`; no conclusion is issued over this scope | the same sentence lives in `.specify/specs/097-speckit-migrate-command/code-review.md` |
| Record | .specify/specs/097-speckit-migrate-command/code-review.md | written because the triage value is `run` |
| Archive | .specify/specs/097-speckit-migrate-command/code-review-20261110T161419Z.md | this run's rotation (F6 below records that the script uses the timestamped fallback even where the composition owner prefers the slice-id form) |

Code findings (six-level family, read in the record): **0 `blocking`**, 0 `important`, 6 `suggestion`, 1 `nitpick`, 1 `praise`. The round-1 `blocking` entry (unfailable zero-write probe, `tests/integration/test_migrate_us2_safety.py`) is **fixed and re-verified**: the probe now hands `tempfile.TemporaryDirectory` a sentinel path under a monkeypatched stand-in, chdirs into the workspace, and asserts both limbs; mutation 5 injects a workspace-writing probe and turns the digest assertion red; `test-evidence/red-base-probe-guard-2026-11-10.txt` records two engine-mutation variants (sentinel limb red; digest limb red) and the reverted green run (12 passed). The two round-1 `important` items are also fixed and re-verified: the `--help` zero-side-effect limb now chdirs into and snapshots the workspace it inspects, and C-1 / `docs/reference/commands/migrate.md` / `templates/commands/migrate.md` converged to `--help` only, with `-h` pinned as an undeclared option (exit 2). The six standing `suggestion`s are test-strength items carried from the round-1 record (trivially-true pointer assertion, broad `pytest.raises` wrappers, missing module-level contract marker, sampled option set, two-substring generic-coverage check, silently degrading commit assertion); the `nitpick` is the orphaned `.gitignore` comment. None blocks and none is a transition condition.

**Status-transition judgment (`Implemented → Ready for Review`): allowed — landed.** The four conjunctive conditions of `templates/feature-details-template.md` § Canonical Status State Machine all hold: (a) zero deferred (`[~]`) tasks — `tasks.md` closes 48/48, closure checker `deferred: 0`; (b) review evidence produced — this report plus `code-review.md`; (c) the current code-segment record contains **zero** `blocking` entries — `blocking_entries=0`, merge gate `allow`; (d) no `final`-path criterion sits in `blocked` / `deferred` / `fail` — `final_path` reads pass 4 / blocked 0 / deferred 0 / partial 0 / fail 0 / unknown 0 / total 4, and no waiver was presented or inferred. The Acceptance Reality Check raises no refusal of its own (§2.4). The code segment's `not-evaluated` verdict does not block the transition and is disclosed here and in the feature detail's `## Latest Review` entry (state machine item 8). Status was flipped after both records landed, and `.specify/features.md` row 024 and `.specify/features/024-specification-workspace-versioning.md` now agree on `Ready for Review`.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, research.md, plan.md, data-model.md, contracts/ (3 files), quickstart.md, feature-ref.md, tasks.md, verification.md | derived from the stage rules plus `plan.md` § Project Structure (the plan declares research.md and feature-ref.md beyond the standard seven) |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | pass | no finding survives the round-1 repair; A1–A9 are verified closed below |

Round-1 artifact findings, re-verified one by one in this run:

| Round-1 ID | Re-verification reading (this run) |
|------------|-------------------------------------|
| A1 (P0) | `.specify/features.md:33` reads `Implemented` and `.specify/features/024-specification-workspace-versioning.md:6` reads `**Status**: Implemented`; `closure-verdict-pre-flip` (claim `Planned`, verdict `accept`, `final_path` 4/4) and `closure-verdict-implemented` (claim `Implemented`, same counts) are both on disk; the status flip is landed by an explicit commit (`da34a3d44`), not by prose. |
| A2 / I1 (P1) | `verification.md:27` `smoke_command` equals the `## Command` literal in `final-suite.txt` byte for byte, including `--names-out .specify/.tmp/review-repair-r1/final-failed.txt` (machine-compared this run: equal); the file records `105 passed`, `# exit=0`. |
| A3 (P1) | `verification.md:119` now attributes the pointer readings to `us1-converge.txt` and the sanitize-lane support to `skills/internal/sanitize-materials/SKILL.md:167-178` plus the byte-identical mirror pair (`mirror-verify.txt` Pair 1); `us1-converge.txt` does carry `POINTER` / `POINTER-RECEIPT` rows and `SECOND-RUN outcome=clean items=0`, and contains no sanitize-lane claim. |
| A4 (P1) | `contracts/migrate-cli.md:19` declares `--help` only; `docs/reference/commands/migrate.md:25` matches; `templates/commands/migrate.md:24` no longer claims `--help` lists the envelope keys; `test_migrate_cli_surface.py` parametrizes `-h` among the undeclared options and asserts exit 2 with `No such option` (run green this session). |
| A5 (P1) | `src/specify_cli/__init__.py:3047` (running receipt) and `:4381` (completed payload) both carry `workspace`; `data-model.md` E-3 has the row; `tests/unit/test_migrate_receipts.py:51` and `tests/contract/test_migrate_cli_surface.py:125` pin the key in the running receipt and the dry-run envelope; `docs/reference/commands/migrate.md:44` lists the volatile field. |
| A6 (P2) | `verification.md` SC-002 now separates three product mutations + the workspace-writing probe variant from the existence-only check-power drill, which is explicitly labelled; `tasks.md` DoD-4 says "five red-ability drills". |
| A7 (P2) | `quickstart.md:5` states the command is implemented in the repository source, that installed 0.0.22 does not carry it, and that scenarios 1–5 were executed in repository-source form (`notes/quickstart-run.md`, driver `all_pass=True`); scenario headings read "已实测：仓库源码形态". |
| A8 (P2) | The 024 detail's `Planned` criterion no longer claims the superseded version schema / migration registry; `Implemented` describes `specify migrate`; the `Blocked` template row is present. |
| A9 (P2) | `tasks.md:44` reads `**DoD Status**: pass` with the verification pointer and re-validation date; `validate-tasks.py` returns PASS 0 error / 0 warning (re-run this session). |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| — | — | — | — | No open artifact finding: every round-1 finding is verified closed; all nine evidence sha256 values in `verification.md` match the files on disk. |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | da34a3d44132852a348b61ba0be64ea8efcffef9 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier `git-delta-review.sh` reported |
| Smoke command | `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/review-repair-r1/final-failed.txt tests/contract/test_migrate_cli_surface.py tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/contract/test_migration_distribution.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/integration/test_migrate_us1_converge.py tests/integration/test_migrate_us2_safety.py tests/integration/test_migrate_us3_crossversion.py tests/integration/test_migrate_us4_equivalence.py -q` | recorded verbatim from verification.md:27 |
| Smoke exit code | 0 | re-run of the recorded literal this session: `105 passed in 22.79s`, `# exit=0` (`elapsed=25s`) |
| Smoke evidence path | .specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt | exists and non-empty (`105 passed`; `# exit=0`); this session's re-run transcript: `.specify/.tmp/review-097-r2/smoke-rerun.txt` |
| Scope and regression verdict | pass — the delta's 147 files map to declared FR/task rows and the repair round's dispositions (engine pkg02–pkg05, template+assembly pkg06, polish pkg07, registry/pin side effects of FR-021, constitution amendment 1.19.1, review-repair r1's 23 files); the feature subset shows zero NEW failures against the recorded 278-name baseline (final-suite.txt § Failure-name comparison, `new_count=0`) | this segment's own reading |
| Segment verdict | pass | no finding below; round-1 I1 is verified fixed |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| — | — | — | — | No open implementation finding: the recorded smoke literal is the executed command, its exit code is 0, the evidence path exists and is non-empty, and the repair commit stays inside the declared scopes. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Implemented | the bound feature detail, copied before the flip |
| `final_path` record, copied verbatim (7/7) | pass [4] · blocked [0] · deferred [0] · partial [0] · fail [0] · unknown [0] · total [4] | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/097-speckit-migrate-command --feature-detail .specify/features/024-specification-workspace-versioning.md --json`, never recomputed here |
| Comparison verdict | agree | neither refusal condition fires: verdict `accept`, and the claim is `Implemented` with a non-zero `pass` bucket |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The checker's completion conditions all read true: `every_final_path_pass=true`, `no_open_rows=true`, `smoke_record_pass=true`, `status_row_per_criterion=true`; `reasons=[]`, `waived=[]`. The full record: `verdict=accept` · pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4.

## 3. Findings (Problems & Improvement Targets)

### F1 — An owner-level conflict was forced onto feature artifacts, then the owner was amended, forcing a second repair

- **Severity**: P1
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md (W3-16/W3-18) × .specify/constitution.md (1.19.1 Sync Impact Report) × commit 1b2d998c6
- **Evidence** (verbatim quote):

  ```
  | W3-16 | HIGH | confirm | fixed | `tasks.md:113`（pkg07 写域） | `verification.md` 全文件仅存于 pkg07 写域一处，与 T048/DoD-7/GATE-4/宪法 VII 的 `verification.log` 冲突；pkg07 写域改为 `verification.log` 后 …
  ```

  Two commits later: `-  **Pre-Status-Flip Gate** (Planned→Implemented): … in `verification.log`` → `+  … in `verification.md`` (27ccbab93), then 1b2d998c6 reverted the feature artifacts; the `.gitignore` negation added for W3-18 was removed but its comment stayed.

- **Why it's a problem**: the analyze repair round paid to bind the feature to a literal that the next upstream decision removed. The root cause was an owner-level fork (constitution vs mechanism), yet the repair was applied one level down, at the artifacts, and had to be re-applied. Two commits and one repair row were spent on a round trip. The round-1 disposition recorded this as framework observation FO-1; it is still unaddressed, so every future analyze round pays the same toll.
- **Proposed fix**: extend the analyze repair disposition rules — when a finding's root is a conflict between two owners (here: constitution § VII vs the framework chain), the disposition is "route to the owner", not "coerce the artifact", and the artifact-side change waits for the owner's ruling.

### F2 — Fifty-plus open analyze MEDIUM/LOW findings entered implement with no disposition record, and two of them recurred as live defects

- **Severity**: P1
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-r3-2026-11-10.md
- **Evidence** (verbatim quote):

  ```
  | W2-02 | carried-over | data-model.md:41 E-2 / :55–71 E-3 / migrate-cli.md:62–65 C-4 | 回执 `workspace` 字段三处不一致：E-2 称记录、C-4 列为易变字段、E-3 schema 无该字段。 | data-model E-3 / migrate-cli C-4 |
  ```

  and §S-6: `断点：W2-02、W2-16、W2-20、W2-03、W3-10（carried）。` The round-3 gate (4194e0ebb) records "0 open C/H, 51 open M/L"; no implement-stage record dispositions them, and W2-02 materialized as the round-1 A5 while W1-25/W3-05 materialized as A3.

- **Why it's a problem**: an analysis backlog without a consumption lane is a promise nobody keeps. The M/L findings that predicted the exact review defects were carried silently; the implement stage could not distinguish "accepted risk" from "not yet read". The round-1 disposition recorded this as FO-2; no mechanism has changed.
- **Proposed fix**: add an implement-entry disposition step for open analyze findings — fix / waiver with owner / carry with a named owner — recorded on one list; or make the analyze gate emit a machine-readable backlog that `/speckit.implement` must consume.

### F3 — Prior-stage checkpoints were never committed; the committed timeline cannot cover the requirements and clarify stages

- **Severity**: P2
- **Category**: Workflow
- **Location**: .specify/specs/097-speckit-migrate-command/checkpoints/
- **Evidence** (verbatim quote):

  ```
  ?? .specify/specs/097-speckit-migrate-command/checkpoints/01-requirements.md
  ?? .specify/specs/097-speckit-migrate-command/checkpoints/02-clarify.md
  ```

  (from `git status --short` at this review's start; `checkpoints/03-plan.md` is committed)

- **Why it's a problem**: the artifact-commit step exists to keep each stage's product on the branch; two of three checkpoints fall outside it, so the review's timeline rows 1–2 rest on run-record timestamps rather than the stage products. This also contributes two of the six uncommitted paths that every review round must disclose.
- **Proposed fix**: either commit a stage's checkpoint with the stage, or declare `checkpoints/` as intentionally untracked scratch in the loop-driver contract so the deviation is not repeated as a finding each run.

### F4 — The constitution amendment's Sync Impact inventory misses two live documents that still name `verification.log`

- **Severity**: P2
- **Category**: Documentation
- **Location**: .specify/constitution.md (Sync Impact Report) × docs/concepts/better-harness.md × docs/reference/history/00-cross-cutting-lessons.md
- **Evidence** (verbatim quote):

  ```
  - Templates requiring updates:
    ✅ shared/guidelines/better-harness.md (+ .specify mirror) — the two sensor references now name verification.md
    ✅ tests/contract/test_fast_fail_discipline.py — live version pin 1.19.0 → 1.19.1
  ```

  but `docs/concepts/better-harness.md:32` still reads `Test-First, checklist, analyze, verification.log`, and `docs/reference/history/00-cross-cutting-lessons.md:67` still reads `每个成功标准(SC)在 verification.log 有状态行`. The review-repair round did not touch either file.

- **Why it's a problem**: the amendment declares its carrier sweep complete; two live guidance docs keep the old name, so a reader following either lands on a file the framework chain never reads. The report is a completeness claim, and it is false.
- **Proposed fix**: add both docs to the Sync Impact inventory and correct them (or explicitly rank the lessons file as a dated record); the amendment checklist should enumerate live docs by grep, not by memory.

### F5 — Evidence bookkeeping has no machine check; the round-1 pointer defects were found by review, not by a gate

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: .specify/specs/097-speckit-migrate-command/verification.md × scripts/python/closure-acceptance-check.py
- **Evidence** (verbatim quote):

  ```
  # The closure judgement
  # (scripts/python/closure-acceptance-check.py) parses `SC-NNN_status=` lines and nothing else.
  ```

  The round-1 defects A2/A3/A6 (smoke literal not the executed command; SC-007 pointer targeting a file with no such reading; a check-power drill presented as a product mutation) were all mechanically detectable — resolve each `evidence_path` / `SC-*_value` pointer, compare the smoke literal with the run header — but none is checked today; the checker's `SMOKE_FIELDS` path only tests presence, exit code and evidence-file existence.
- **Why it's a problem**: each implement run re-earns the right to drift, and the repair depends on a review round noticing. A pointer check would have turned all three into gate failures.
- **Proposed fix**: add a read-only check to the closure checker: every `evidence_path` / `SC-*_value` pointer resolves to an existing file, and the recorded smoke command matches the header of the file it cites.

### F6 — One composed review run archived its two records under two different naming rules

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: .specify/shared/workflow/acceptance-hardening.md § Records and rotation × .specify/skills/internal/code-review/scripts/git-delta-review.sh (`start`)
- **Evidence** (verbatim quote):

  ```
  When a record already exists, the run archives it **inside the same directory** as
  `<record>-<slice>.md` — the slice id of the run, e.g. `review-081c.md` — and then writes the new record. The
  timestamped `<record>-<YYYYMMDDTHHMMSSZ>.md` (UTC, second resolution) form is the fallback when no slice id
  exists;
  ```

  versus the script's `start` step: `archive_target="${SPEC_DIR%/}/code-review-${stamp}.md"` (and its help text: `归档名 code-review-<YYYYMMDDTHHMMSSZ>.md`). This run followed both: `review.md` → `review-097-speckit-migrate-command.md` (slice-id form) while `code-review.md` → `code-review-20261110T161419Z.md` (timestamp form), even though the slice id was known and passed via `--spec`.
- **Why it's a problem**: the composition owner says the timestamped form is the *fallback*, and the skill's mandated non-interactive path (`start`, "省掉它就是把记录交给 agent 手写") can only produce that fallback. A later reader cannot predict the archive name from the rule, and two runs inside one second can collide into exit 2. The two skills' texts disagree with the owner, and the tool is the one that loses.
- **Proposed fix**: let `start` derive the slice id from `--spec` (or accept `--slice <id>`) and archive as `code-review-<slice>.md`, keeping the timestamp only as the no-slice fallback; align the skill's help text and step description.

### F7 — `receipt` resolves its own range and silently diverges from the record header when `--spec` is omitted

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: .specify/skills/internal/code-review/scripts/git-delta-review.sh (`receipt`) × .specify/skills/internal/code-review/SKILL.md § 非交互路径（Agent / CI：五步）
- **Evidence** (verbatim quote from this run's terminal):

  ```
  行数无法测量 (binary): .specify/anchoring/command-logic-as-classified-skills/summary/assets/wbs.png
  不可量测的数字字段意味着不写块 (C-41 / V16)
  EXIT=2
  ```

  The skill's step 4 is written `receipt --review-file <record>` — no `--spec`; the same document's step 1 resolves `base` / `head` for the run and step 2 (`start`) records them in the record header, but `receipt` does not read that header. Without `--spec` it resolves the default trunk range instead: this run's first receipt attempt walked `.specify/anchoring/…` objects that are not in `b3da3a26d..da34a3d44` and exited 2 on a binary file; adding `--spec` produced the intended 147/107/40/0 receipt. On a tree without binary files the same omission would silently write a receipt over the wrong delta.
- **Why it's a problem**: the receipt is the single evidence form for "the whole diff was read" (C-32/C-38). A step whose documented form can compute counts over a different range — or fail on objects outside the review object — undermines the one mechanism the review composition relies on, and the failure message names a file the operator cannot connect to their omission.
- **Proposed fix**: default `receipt`'s range to the record header's `base` / `head` (with `--spec` / `--since` as overrides), or make `--spec` mandatory in the step text and in `--help`, and name the resolved range in the exit-2 message.

## 4. What Worked — Preserve (Brief)

- The review-repair round converged in one pass: all 1 P0, 8 P1, 1 `blocking` and the P2 quick wins landed in `da34a3d44`, with no assertion weakened (the zero-write guard was strengthened and a fifth mutation added).
- The red-base drill discipline: two distinct engine mutations, each failing a *different* limb of the rebuilt guard (sentinel missing; workspace digest moved), then a reverted green run — the guard's power is demonstrated, not asserted.
- The evidence chain survived the repair: all nine `verification.md` sha256 values match the current evidence files, and the smoke literal equals the executed command's literal byte for byte.
- The single-engine posture held: `specify migrate` is the only executor; `copy_local_templates`, `sanitize-utils` checkers, `anchor-layout-migrate` and the sync/regen checkers are consumed, not copied; the T-002 split (framework-source vs client) is backed by a measured fact (mirror ≠ `rewrite_paths(source)`).
- Domain constants have one owner and the contract tests extract them from the owner files (dimension tokens from data-model E-8, disposition domain from requirements FR-014) — owner drift cannot pass silently.
- The review composition itself worked as designed: both records rotated, the code segment's receipt carried all 147 changed files with 0 gaps, and the merge gate discriminated on `blocking` alone.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **Pointer-resolution check in the closure chain** — Target: `scripts/python/closure-acceptance-check.py`. Change: add a read-only check that every `evidence_path`/`SC-*_value` pointer in `verification.md` resolves and that `smoke_command` matches the header of the file it cites. Source: F5. Expected impact: pointer defects become gate failures instead of review findings.
- **Slice-id rotation in `start`** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` + `skills/internal/code-review/SKILL.md`. Change: derive/accept the slice id and archive as `code-review-<slice>.md`; keep the timestamp form only when no slice id exists. Source: F6. Expected impact: one naming rule across both records; no collision exit on a same-second rerun.
- **Header-anchored receipt range** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (`receipt` / `--help`) and the skill's non-interactive step 4. Change: default to the record header's `base`/`head` or require `--spec`, and name the resolved range when refusing. Source: F7. Expected impact: the receipt's counts cannot silently cover a different delta than the record it annotates.

### 5.4 Workflow Improvements

- **Enforce the registry flip in the implement stage** — Target: `templates/commands/implement.md` and the stage-closing checklist it points at. Change: make the `Planned → Implemented` flip an explicit closing step whose absence fails the stage (the four conditions are already machine-checked by `closure-acceptance-check.py`). Source: the round-1 A1 repair (now closed; the mechanism gap that allowed it remains). Expected impact: the review gate stops receiving features whose status carrier lags their work.
- **Owner-conflict routing in analyze repair** — Target: `skills/internal/analyze-artifacts/SKILL.md`. Change: when a finding's root is a conflict between two owners, dispose as "route to the owner" and defer the artifact change until the owner rules. Source: F1. Expected impact: no more double repairs like W3-16/W3-18 → 27ccbab93 → 1b2d998c6.
- **A consumption lane for open analyze findings** — Target: `templates/commands/implement.md` + `templates/tasks-template.md`. Change: at implement entry, require a disposition row per open analyze finding (fix / waiver owner / carry owner). Source: F2. Expected impact: carried M/L findings stop materializing as review defects without attribution.
- **Checkpoint commit discipline** — Target: the SDD loop-driver contract. Change: commit each stage's checkpoint with its stage, or declare `checkpoints/` untracked scratch. Source: F3. Expected impact: the review timeline can cite stage products, not run-record timestamps.

### 5.5 Documentation Improvements

- **Carrier sweep completeness** — Target: `.specify/constitution.md` Sync Impact Report procedure + the two stale docs (`docs/concepts/better-harness.md:32`, `docs/reference/history/00-cross-cutting-lessons.md:67`). Change: enumerate live carrier references by grep and list them in the report; correct both docs. Source: F4. Expected impact: an amendment's completeness claim becomes checkable.

(No Template or Command Prompt recommendations survived triage; dropped rather than padded.)

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Header-anchor the receipt range (or require `--spec`) | `skills/internal/code-review/scripts/git-delta-review.sh` (`receipt`) | F7 |
| P1 | Route owner-level conflicts to the owner before coercing artifacts | `skills/internal/analyze-artifacts/SKILL.md` | F1 |
| P1 | Consume open analyze findings at implement entry | `templates/commands/implement.md` | F2 |
| P2 | Complete the constitution carrier sweep and correct the two stale docs | `.specify/constitution.md`, `docs/concepts/better-harness.md`, `docs/reference/history/00-cross-cutting-lessons.md` | F4 |
| P2 | Add the evidence-pointer check to the closure chain | `scripts/python/closure-acceptance-check.py` | F5 |
| P2 | Unify record rotation on the slice-id form | `skills/internal/code-review/scripts/git-delta-review.sh`, `skills/internal/code-review/SKILL.md` | F6 |
| P2 | Commit stage checkpoints or declare them scratch | SDD loop-driver contract | F3 |
| P2 | Enforce the registry flip in the implement stage | `templates/commands/implement.md` | round-1 A1 (closed; mechanism gap) |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `REC-…` ids were coined in this report, so no identifier was registered.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. **No P0 was raised this round** (the round-1 P0, A1, is repaired; its repair was re-verified here by two closure-checker runs — pre-flip claim `Planned` and post-flip claim `Implemented`, both `accept` with `final_path` 4/4 — and by an independent re-read of both status carriers). No finding required downgrade or rejection; every P1/P2 cites its own evidence.
- [x] The six uncommitted paths are disclosed, not reviewed; no conclusion is issued over them.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
