# Requirements Quality Checklist: SDD 临时 Goal / 临时 Team 与多 Agent 并发

**Purpose**: Validate the quality, clarity and completeness of the 085 requirements before implementation.
**Created**: 2026-11-06
**Feature (Requirement Scope)**: `.specify/memory/features/085.md`
**Requirements (What)**: [`../requirements.md`](../requirements.md)
**Specifications (How, context only)**: [`../plan.md`](../plan.md), [`../tasks.md`](../tasks.md)

## Scope and lifecycle

- [ ] CHK001 Temporary Goal and Temporary Team are explicitly distinguished from Global Goal/Team, including storage and lifecycle.
- [ ] CHK002 The creation timing is stated and testable: Temporary Goal after requirements U4, Temporary Team after clarify + plan U4.
- [ ] CHK003 The "authored, not derived" rule for the temporary goal is explicit, including the no-SC-copy constraint.

## Concurrency and agents

- [ ] CHK004 The default concurrency is a single declared value, and requested vs effective is required on every dispatch.
- [ ] CHK005 Downgrade reasons form a closed set and a downgrade is never reported as the requested value.
- [ ] CHK006 The stage-agent roster is expressed as a role grammar, not a fixed per-stage count.
- [ ] CHK007 Every retained framework agent has exactly one turn budget (500), and rendered copies are covered.

## Worktrees and integration

- [ ] CHK008 Child lines are defined with parent, depth-1, worktree, branch, owned paths and forbidden paths.
- [ ] CHK009 Integration order is declared by the work-package plan, never by dispatch timing.
- [ ] CHK010 Failure/conflict behavior retains evidence and never produces a partial stage deliverable.

## Checkpoints and compatibility

- [ ] CHK011 The four checkpoint parts are mandatory, and at most one configuration change is allowed per checkpoint.
- [ ] CHK012 Rollback triggers are named and testable.
- [ ] CHK013 Global stores (`.specify/goal/**`, `.specify/teams/**`) are forbidden paths for temporary-scope writes.
- [ ] CHK014 The 070 shared-tree default and 064 root-line behavior remain the compatibility baseline.
- [ ] CHK015 The generic `sdd-executor` removal is covered by a live-reference cleanup obligation, without rewriting dated records.

## Notes

- Check items off as completed: `[x]`
- The checklist validates requirement quality, not implementation behavior.
