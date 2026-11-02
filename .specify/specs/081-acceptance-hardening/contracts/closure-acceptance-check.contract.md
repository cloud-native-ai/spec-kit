# Contract — Closure Acceptance Check (`scripts/python/closure-acceptance-check.py`)

**Status**: designed (this stage); implemented by `/speckit.implement`
**Owner of the schema consumed here**: `shared/workflow/acceptance-hardening.md` § Closure Verdict. This contract fixes the **calling surface**; it never redefines the reason set's meaning.

## Purpose

One deterministic source of truth for "may this feature be called `Implemented`?" — called by `/speckit.implement` (before `Planned → Implemented`), `/speckit.review` (before `Implemented → Ready for Review`) and the `sdd-loop-driver`'s closure/merge step. A caller MUST NOT decide the question another way.

## Calling surface

- **C-01**: The entry point MUST be `scripts/python/closure-acceptance-check.py`, runnable as `python3 scripts/python/closure-acceptance-check.py …` from the repository root, importable-free (no `sys.path` assumptions about `src/`), stdlib-only, and read-only.
- **C-02**: It MUST accept `--spec-dir <dir>` (required) and MUST exit `2` with a message naming the path when the directory does not exist or a required input (`requirements.md`, `plan.md`, `tasks.md`, `verification.md`) is missing or unparsable. A missing file MUST NOT be reported as `block`.
- **C-03**: It MUST accept `--feature-detail <path>` or `--feature-registry <path>` to locate the claimed feature status; when neither is given it MUST resolve the status from `.specify/memory/features.md` by the spec directory's key, and it MUST exit `2` if the claimed status cannot be determined.
- **C-04**: It MUST accept `--audit-existing`, which switches to the read-only audit mode of C-10.
- **C-05**: It MUST accept `--json` (machine-readable on stdout) and `--json-out <path>` (identical payload written to a file); the default human output MUST include the verdict, every reason, and the three `final`-path counts.
- **C-06**: It MUST accept repeatable `--waive <CODE>:<TARGET>` entries using the same `<check>:<path>:<line>`-style waiver grammar as `pre-analyze-check.py`, and a waived reason MUST be absent from the blocking set while still being counted as waived in the summary.

## Verdict and counts

- **C-07**: The verdict MUST be exactly one of `accept` / `block`. There is no third value, no severity scale, and no advisory tier.
- **C-08**: The payload MUST carry `final_path = {pass, blocked, deferred, fail, unknown, total}` computed by this script. No caller, template or report MAY recompute those counts; the report copies them.
- **C-09**: Every `block` MUST carry at least one reason whose `code` is verbatim one of the seven closed values: `zero-final-path-pass`, `final-path-not-pass`, `blocked-without-measurement-ladder`, `runtime-dependency-not-owned`, `falsified-premise-undecided`, `inherited-blocker-undisposed`, `status-claims-implemented-but-blocked`. A reason outside the set is a defect of the checker, not a finding about the feature.

## Exit codes and modes

- **C-10**: Exit codes MUST be `0` = `accept`, `1` = `block`, `2` = input missing or unparsable. In `--audit-existing` mode the exit code MUST reflect input validity only: `0` whenever the inputs parse, regardless of how many features the audit reports.
- **C-11**: `--audit-existing` MUST perform zero writes — no file created or modified anywhere, verified by `git status --porcelain` being unchanged across the run — and MUST NOT alter any historical feature status or verification record.
- **C-12**: The audit output MUST list, per affected feature, the claimed status, the computed verdict and every reason, so the list can be read without re-running the checker.

## Inputs and their readers

- **C-13**: From `requirements.md` it MUST read the SC definition lines and their `**Path**` markers, and the rows of `§ Runtime Stack & Dependency Ownership`. It MUST treat an unparsable `Path` marker as an input error (C-02), never as a `block` reason.
- **C-14**: From `plan.md` it MUST read `§ Execution Premises` rows and `§ Inherited Blockers` rows; both sections MUST be present for an `execution`-class feature, and their absence is an input error (the plan artifact is incomplete, not the feature failing).
- **C-15**: From `tasks.md` it MUST count `[ ]`, `[>]` and `[~]` rows.
- **C-16**: From `verification.md` it MUST read each `SC-NNN_status`, the five measurement-ladder fields and the three smoke fields; it MUST evaluate V-5/V-6 of `data-model.md` (missing ladder field, or a ladder available but not run).
- **C-17**: From the dependency features' details it MUST extract `## Deferred` rows, `verification.md` status rows in `blocked`/`deferred`, and `deferred_tasks=` lists, and it MUST require each extracted row to appear with a disposition in `plan.md` § Inherited Blockers.

## Traceability

| FR | Clauses | Test |
|---|---|---|
| FR-006 | C-01…C-09, C-13…C-17 | `tests/contract/test_closure_acceptance_check.py` |
| FR-007 | C-02, C-10 (exit-code tri-state), C-09 (closed set), `data-model.md` fixture set | `tests/contract/test_closure_acceptance_check.py` (positive + negative fixtures) |
| FR-008 | C-07, C-08 | three call-site assertions in `tests/contract/test_gate_wiring_081.py` |
| FR-020 | C-04, C-10, C-11, C-12 | `tests/contract/test_closure_acceptance_check.py::test_audit_writes_nothing` |
