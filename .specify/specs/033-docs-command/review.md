# Specification-Driven Development (SDD) Process Review Report: /speckit.docs 文档规范与管理命令

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 033 |
| Requirement Key | 033-docs-command |
| Requirement Name | /speckit.docs 文档规范与管理命令 |
| Related Feature | 037 Docs Command |
| Repository | spec-kit |
| Repository URL | https://github.com/github/spec-kit (origin; local fork diverges) |
| Branch | 033-docs-command |
| Commit SHA | 98040f98ca22a6845ed274926e527e1aa4968fe6 (short: 98040f98) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-07-28 |
| Reviewer (Agent) | Qoder CLI agent (session-driven SDD run) |
| Environment | Linux 5.10.134 (container, uid 1001, restricted sandbox: no /tmp writes, no `git worktree` exec, no `rm -rf`, no passwordless sudo), bash, Python 3.11 venv + pytest 8.4.2 |
| spec-kit Source Snapshot | https://github.com/github/spec-kit @ 98040f98ca22a6845ed274926e527e1aa4968fe6 (self-hosted: framework repo == project repo) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 203 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/requirements.md | 5 user stories, FR-001…011, SC-001…007, 3 clarify sessions + 3 mid-run directives |
| plan.md | 116 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/plan.md | Constitution check (11 principles), mirror obligations table, inlined Phase 0 |
| tasks.md | 226 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/tasks.md | 37 tasks / 8 phases, doc-feature taxonomy, all closed |
| data-model.md | 83 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/data-model.md | 7 entities incl. notes state machine, reserved-name registry |
| contracts/ (3 files) | 49 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/contracts/ | command-template C-1…11, docs-utils CLI C-1…11, docs-step injection C-1…9 |
| quickstart.md | 60 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/quickstart.md | 6 scenarios; CLI examples execution-verified |
| verification.md | 67 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/verification.md | SC-001…007 all pass; failure-delta attribution narrative |
| checklists/requirements.md | 36 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/033-docs-command/checklists/requirements.md | 16/16 pass, one re-validation entry |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | /speckit.requirements → spec drafted, 0 NEEDS-CLARIFICATION | checklist "全部项通过（3 轮内一次通过）" | None |
| 2 | /speckit.clarify (Mode A): 3 Q&A, Feature 037 registered | requirements.md `### Session 2026-07-28` (3 Q rows) | None |
| 3 | /speckit.plan with in-flight user directive #1 (uppercase naming) + directive #2 arriving mid-run (docs-sync step) | requirements.md "用户修订指示（2026-07-28，plan 阶段）" ×2 | Spec-restructure-first applied; but a Clarifications edit transiently REPLACED the prior directive row (restored by hand) — see F2 |
| 4 | /speckit.tasks: 36 tasks, Tests Mode ON banner | tasks.md "**Tests Mode**: ON (Constitution Principle IV…" | None |
| 5 | /speckit.implement phases 1–2: baseline 83F/827P recorded as counts only | verification.md `baseline_pytest=83F/827P/1S`; commit 5dfd868e | Baseline stored without failed-test name list — see F1 |
| 6 | US4 dogfooding stalled: `docs/notes/` root-owned, sandbox denied sudo | session: "sudo: a password is required"; fixed by user-run `! sudo chown` | Environment friction; implement has no writability pre-probe — see F6 |
| 7 | US4 aggressive reconcile: 15 git-mv moves, 134→0 broken links | commit 141dde0e; audit /storage/project/cloud-native-ai/spec-kit/.specify/docs/audit/20260728T082822Z-docs-audit.md | Link rewriting done by ad-hoc one-off script — see F5 |
| 8 | Mid-implement user directive #3 (Reserved Filenames strict blocking) | requirements.md "用户修订指示（2026-07-28，implement 阶段）"; commit ab3e881d | Handled via clarify's Scope Revision Protocol by analogy; /speckit.implement itself prescribes none — see F4 |
| 9 | Regression +4 vs baseline; root-caused to 3 stale test pins + 1 fragile version pin; fixed | verification.md "Failure-delta attribution" block; commit 28b95a00 | Pin fragility recurred despite documented lesson — see F3 |
| 10 | Wrap-up: verification, Feature 037 → Implemented, feedback entries | commits 28b95a00, 98040f98 | None (evidence strength: commits are phase-grouped, not per-task) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 3 |
| Automation / Scripts | 2 |
| Workflow | 1 |
| Documentation | 0 |

## 3. Findings (Problems & Improvement Targets)

### F1 — Test baseline stores counts, not failed-test identities

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/run-tests.sh; consumed by https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/templates/commands/implement.md
- **Evidence** (verbatim quote, verification.md attribution burden this gap caused):

  ```
  # Failure-delta attribution: every failing family's root cause verified present at
  # baseline commit d8d120df (missing templates/agent-role-*-template.md; missing
  # "## Agent-Specific Configuration" headings ...). Zero failures in any file or
  # surface touched by spec 033.
  ```

- **Why it's a problem**: The implement flow only records `83F/827P` at baseline. When the final count differed by +1, zero-regression could not be proven by name-diff; it required per-family manual root-cause archaeology (checking heading presence at the baseline commit), and the sandbox denied the `git worktree` replay fallback.
- **Proposed fix**: Extend `run-tests.sh` with a `--names-out <file>` flag emitting the sorted `FAILED` test-id list, and make the `/speckit.implement` baseline task archive that file beside `verification.md` so regression checks become a `comm -13 baseline current` one-liner.

### F2 — Clarifications session log has no append-only guard; an Edit-based integration silently replaced a prior entry

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/.specify/shared/constants/clarify-taxonomy.md (Mode A Integration Rules)
- **Evidence** (verbatim quote — the rule says append but nothing forbids/detects replacement):

  ```
  - Ensure `## Clarifications` exists (create after highest-level overview section). Under it, `### Session YYYY-MM-DD`.
  - Append: `- Q: <question> → A: <final answer>`
  ```

- **Why it's a problem**: During this run an exact-string Edit targeting the newest directive row overwrote the previous "plan 阶段" directive row instead of appending after it; the loss was only caught by re-reading the diff. Clarifications are governance history — silent truncation there corrupts the audit trail with no tooling signal.
- **Proposed fix**: Add an integration invariant to clarify-taxonomy.md (and the `/speckit.analyze` checks): "session entries are append-only; after integration, re-count `- Q:`/`用户修订指示` rows and verify count strictly increased". Optionally provide a `glossary-utils`-style helper (`spec-utils.py --action append-clarification`) so entries are appended mechanically instead of via free-form Edit.

### F3 — Fragile pins recur despite a documented lesson: exact version prefix, phantom surface file, hard-coded counts

- **Severity**: P1
- **Category**: Workflow
- **Location**: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/tests/contract/test_dogfooding_practice.py (pre-fix); /storage/project/cloud-native-ai/spec-kit/tests/conftest.py (pre-fix)
- **Evidence** (verbatim quotes, both pre-fix):

  ```
  assert m.group(1).startswith("1.6"), f"expected MINOR bump to 1.6.x, found {m.group(1)}"
  ```

  ```
  repo_root / "docs" / "usage.md",
  ```

- **Why it's a problem**: The constitution's own next MINOR bump (1.7.0, required by this spec) broke a contract test that pinned `1.6` exactly; and `docs/usage.md` never existed at any reviewed commit, so two surface tests failed at FileNotFoundError before ever reaching their real assertion. The instructions file already carries the lesson ("Hard-coded counts/numbers … are fragile signals that break on expansion"), yet nothing enforces it at test-authoring time.
- **Proposed fix**: Add a pin-hygiene rule to the `/speckit.tasks` Task Generation Rules ("version pins MUST be `>=` semantics; every file listed in a test surface fixture MUST be existence-checked or the list generated from the tree") and a one-off sweep task template for existing pins.

### F4 — /speckit.implement prescribes no mid-run scope-revision protocol

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/templates/commands/implement.md (no revision section); protocol exists only in https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/templates/commands/clarify.md
- **Evidence** (verbatim quote — the protocol lives in clarify only):

  ```
  ### Scope Revision Protocol (user re-scopes AFTER plan/tasks exist)
  1. **Amend upstream in place**: update requirements.md first, recording the user directive verbatim under `## Clarifications` ...
  ```

- **Why it's a problem**: Two of this spec's three scope-changing user directives arrived during `/speckit.plan` and `/speckit.implement` runs. The executor had to apply clarify's protocol "by analogy" (spec → constitution → engine → tests → renames → task append), with nothing in implement.md mandating the upstream-first order, the verbatim Clarifications record, or the appended-task (`T037`) discipline.
- **Proposed fix**: Add a short "Mid-run user directive" subsection to implement.md (and plan.md) that points at clarify.md's Scope Revision Protocol and adds the implement-specific steps: append new `T0NN` rows (never renumber), re-run the affected contract batch, note the directive in `verification.md`.

### F5 — Reconcile link rewriting is not an engine capability; dogfooding needed a throwaway script

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/docs-utils.py (validate is read-only; no fix action)
- **Evidence** (verbatim quote from the run's own feedback entry, /storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/20260728T082901Z-speckit-docs.md):

  ```
  dogfooding 全量调谐中，134 处断链的批量修复靠临时脚本完成；建议 /speckit.docs 后续版本将"链接自动重写（搬迁映射 + 锚点保持）"纳入引擎 fix 类动作（安全写入层）
  ```

- **Why it's a problem**: Every future re-taxonomy (any downstream project adopting the six-type layout) will re-pay the cost of writing anchor-aware, move-map-aware link rewriting from scratch; the logic (2 iterations, ~60 lines) existed only in a session-transient heredoc.
- **Proposed fix**: Add `--action fix-links --moves <json>` to `scripts/python/docs-utils.py` (safe-write tier: rewrites relative links per an explicit move map, preserves anchors, dry-run by default) and pin it with contract rows in the docs-utils CLI contract.

### F6 — No writability pre-probe in /speckit.implement; root-owned directory stalled the run mid-phase

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/templates/commands/implement.md (Project Setup Verification step); probe exists only in clarify.md
- **Evidence** (verbatim quote — clarify has the fail-fast probe, implement does not):

  ```
  3. **Writability probe (fail fast)**: before generating any questions, verify the target file is writable (touch-test or write-bit stat on the target and its directory). If unwritable (e.g. root-owned spec dir), STOP immediately ...
  ```

- **Why it's a problem**: `docs/notes/` was root-owned (a known container gotcha already listed in the instructions file); implement discovered it only at the US4 write attempt, mid-dogfooding, requiring a user-run `sudo chown` round-trip. A 1-second probe over the plan's declared write surfaces at step 4 would have surfaced it before any phase started.
- **Proposed fix**: Extend implement.md step 4 ("Project Setup Verification") to walk the plan.md Source Code tree / Mirror Obligations rows and write-bit-probe each target directory, reporting all unwritable paths with the `sudo chown -R $USER <dir>` remedy up front.

## 4. What Worked — Preserve (Brief)

- Spec-restructure-first rule in plan.md: both plan-stage directives landed in requirements.md before design artifacts, so no drift.
- Doc-feature task taxonomy + paired mirror tasks: `regen-command-copies.py --check` stayed at zero drift through 4 rounds of template edits.
- Contract-first TDD on a prompt feature: 3 contract files → 3 red test suites → green, including the 13→14 classification flip caught by design.
- Reconcile pattern's dry-run plan + tiered confirmation: the aggressive 30-item dogfooding converge was user-gated and fully audited (`.specify/docs/plans/`, `.specify/docs/audit/`).
- Quickstart execution-verify gate (contract C-11): all CLI examples ran verbatim before closure — zero doc/code drift shipped.

## 5. spec-kit / SDD Improvement Recommendations

### 5.2 Command Prompt Improvements

- **Append-only Clarifications invariant** — Target: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/.specify/shared/constants/clarify-taxonomy.md (Mode A Integration Rules). Change: add "entries are append-only; after each integration verify entry count strictly increased" + row-count check in `/speckit.analyze`. Source: F2. Expected impact: eliminates silent governance-history loss.
- **Mid-run directive protocol in implement/plan** — Target: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/templates/commands/implement.md. Change: add "Mid-run user directive" subsection pointing to clarify.md's Scope Revision Protocol + append-only task IDs + verification note. Source: F4. Expected impact: deterministic handling of the most common real-session event (3/3 specs recently hit it).
- **Writability pre-probe in implement step 4** — Target: same implement.md, "Project Setup Verification". Change: probe write-bit on every directory named in plan.md's Source Code tree / Mirror Obligations before Phase 1. Source: F6. Expected impact: converts mid-phase stalls into pre-flight fixes.

### 5.3 Automation / Script Improvements

- **Baseline failed-name capture** — Target: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/.specify/scripts/bash/run-tests.sh. Change: add `--names-out <file>` (sorted FAILED ids); implement.md baseline task archives it. Source: F1. Expected impact: zero-regression proof becomes a diff, not archaeology.
- **`fix-links` engine action** — Target: https://github.com/github/spec-kit/blob/98040f98ca22a6845ed274926e527e1aa4968fe6/scripts/python/docs-utils.py (+ `.specify` mirror + CLI contract). Change: `--action fix-links --moves <json>` with anchor preservation and dry-run default. Source: F5. Expected impact: re-taxonomy cost drops from custom scripting to one confirmed command.

### 5.4 Workflow Improvements

- **Pin-hygiene rule at test-authoring time** — Change: add to `/speckit.tasks` Task Generation Rules: version pins use `>=` semantics; surface-file fixtures must be existence-checked or tree-derived; plus a one-off sweep of existing pins. Source: F3. Expected impact: stops the recurring "our own next increment breaks our own contract test" class.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Baseline failed-name capture | .specify/scripts/bash/run-tests.sh + templates/commands/implement.md | F1 |
| P1 | Append-only Clarifications invariant | .specify/shared/constants/clarify-taxonomy.md | F2 |
| P1 | Pin-hygiene rule | templates/commands/tasks.md | F3 |
| P1 | Mid-run directive protocol | templates/commands/implement.md, templates/commands/plan.md | F4 |
| P2 | fix-links engine action | scripts/python/docs-utils.py | F5 |
| P2 | Writability pre-probe | templates/commands/implement.md | F6 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `https://github.com/github/spec-kit/blob/98040f98.../...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
