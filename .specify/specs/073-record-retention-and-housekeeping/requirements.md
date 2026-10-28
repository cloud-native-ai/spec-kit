# Feature 073 — Record Retention & SDD House-Keeping

**Feature ID**: 073
**Name**: 记录消费回收与 SDD 项目管家
**Status**: Implemented
**Created**: 2026-10-27

## Overview

Three per-run record stores accumulate without a consumption lifecycle:
`.specify/memory/exec-quant/records/`, `.specify/memory/feedback/`, and
`.specify/memory/session/`. Existing engines stop at marking or packaging. This feature adds
a consume → receipt → retire lifecycle surfaced through `/speckit.sanitize --lane retention`,
and an external periodic-maintenance skill `sdd-house-keeping` that extracts the repeatable
maintenance steps from `sdd-project-setup` and invokes the target project's sanitize
retention lane.

## User Stories

### US1 — Consume-then-retire records

As a framework maintainer, I want raw per-run records to be distilled into durable
summaries/receipts and then retired, so the repository does not grow forever and every
deletion is auditable.

**Acceptance**
- A raw record is deleted only when a retention receipt covers it.
- Open feedback, unsettled run-determination records, unreadable exec-quant records, and
  session notes without a promotion/ephemeral decision are never retired.
- The default grace period is 30 days; apply re-checks it.
- Apply refuses dirty target paths (git history is the backup) and writes one retirement
  ledger per batch with a count-conservation assertion.
- `--lane materials` keeps the existing sanitize behavior unchanged.

### US2 — Periodic SDD house-keeping

As a framework user, I want a reusable house-keeping skill that inventories, reconciles,
strengthens, verifies, and reports on a target project, including record-retention cleanup.

**Acceptance**
- `sdd-house-keeping` is an external skill at `skills/external/sdd-house-keeping/`.
- One-time bootstrap (init/refresh/constitution/first goal/agents/team) stays in
  `sdd-project-setup`; the new skill owns H1–H5 and handoffs both ways.
- The skill calls the target project's `/speckit.sanitize --lane retention`; it never calls
  `apply` directly and adds no second confirmation gate.
- `check` is the default mode; `cleanup` is explicit.
- The skill does not reimplement sanitize/docs/history/feature/instructions and does not
  advance SDD stages.

## Functional Requirements

- **FR-001**: Add `scripts/python/record-retention.py` with actions `scan`, `distill`,
  `plan`, `apply`, `status`, `args-manifest`.
- **FR-002**: Receipts, monthly summaries, plans, and ledgers live under
  `.specify/memory/retention/`; receipts are per-entry, summaries/ledgers are per-run.
- **FR-003**: Feedback entries require `disposition ∈ {processed, ignored}` plus a durable
  carrier (`disposition_reason`, `introspection_ref`, or a consume-log row).
- **FR-004**: Run-determination records require `settled_at`; exec-quant records must be
  readable; session notes require a promotion or `ephemeral` receipt.
- **FR-005**: `apply` requires `confirmed: true`, a clean git state (or explicit
  `--allow-unversioned`), and asserts `remaining + retired = original`.
- **FR-006**: `/speckit.sanitize` accepts `--lane materials|retention|all`; the materials
  lane's seven stages and confirmation gate are unchanged.
- **FR-007**: Create `skills/external/sdd-house-keeping/` with H0–H5, self-contained
  inventory scripts, and a handoff contract with `sdd-project-setup`.
- **FR-008**: Register the new skill in the probe registry, flow-class ledger, documentation
  map, external roster, and frozen inventory; sync mirrors after compile/regen.
- **FR-009**: No new scheduler, daemon, automatic transmission, or second confirmation gate.

## Success Criteria

- **SC-001**: A temp workspace with consumed records is scanned, distilled, planned,
  applied, and leaves exactly the blocked backlog; a second scan is idempotent.
- **SC-002**: No raw record is deleted without a receipt; open/unsettled/unclassified
  records survive an apply.
- **SC-003**: `sdd-house-keeping` structure/contract tests pass; compile-embeds,
  regen-command-copies, sync-mirrors, and flow-class checks are clean.
- **SC-004**: Existing sanitize and setup contract tests remain green (modulo documented
  pre-existing debt).

## Out of Scope

- Automatic scheduling/daemon.
- Automatic feedback transmission.
- Rewriting the internal flows of sanitize/docs/history/feature/instructions.
- SDD stage advancement.
- Deleting `exec-quant/scores/` (kept; small and joinable).
