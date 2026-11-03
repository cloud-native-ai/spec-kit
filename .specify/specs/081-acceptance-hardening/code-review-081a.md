# Code Review — Feature 081, slice 081a

**Range**: `f9f6d4f3..0277b00f` (the code segment first ran on `d0186dc5`; P0/P1 fixes landed in `0277b00f`)
**Scope**: `scripts/python/closure-acceptance-check.py`, `scripts/python/validate-requirements.py`, `src/specify_cli/__init__.py`, the owner doc, the state/verification/tasks templates, `templates/commands/{tasks,implement}.md`, the skills and their mirrors/copies, `tests/**`, fixtures.
**Excluded**: `90de4d7f fix(coaching-skills)` — a concurrent non-081 commit inside the range; its files are not judged as 081 work.

## Findings

### important

1. **`final_path` shape disagreement** — the requirement asked for three keys, the implementation emitted five buckets, and `partial` had no home. **Resolved in `0277b00f`**: the owner doc defines `{pass, blocked, deferred, partial, fail, unknown, total}`, the checker emits it, and the requirement/contracts/plan/data-model/RC-14 reference that single shape.
2. **081 gate lines lived inside the 077 wiring card** — stripping the card removed the closure/GATE-4 obligations and no assertion failed. **Resolved**: lines moved back to their semantic homes; the stage-class baselines were re-measured with a dated reason; a `templates/commands/implement.md` assertion now makes deletion red.
3. **Contradictory flow-class docstring** — `validate-requirements.py` said an undeclared spec is outside the closure system, while the checker defaults to `execution`. **Resolved**: the docstring reason is corrected; the strict default is unchanged.

### suggestion

- `partial` had no `final_path` bucket, so a partial final criterion counted as `unknown`. **Resolved** (`partial` is now a measured bucket).
- Contract C-03 was behind the implemented spec-local claim-carrier resolution. **Resolved** (contract records it).
- Smoke test rewrites its own tracked evidence, so a stale evidence file cannot be detected. **Recorded** as a known item; the 081d audit/closure path is the owner.

### nitpick

- A bullet in `templates/commands/tasks.md` lost its opening `**`. **Resolved** in the source and all four per-tool copies.

### question

- The implement-side gate is prose plus a text/execution test; no mechanism turns red when the registry status contradicts the verdict. **Answered**: `--audit-existing` is 081d; the current state is an explicit intermediate with the closure checker as the single judgement source.

### praise

- `_section()` stops a section body at any heading level; `_table_rows()` distinguishes “section exists but no table” from “section missing”; `parse_waiver()` validates form and defers membership until the set is in hand. Those choices avoid treating prose as rows and input defects as feature findings.
- `evaluate_smoke()` resolves the evidence path against the repo root, so the verdict is independent of the caller's cwd.
- `test_gate_wiring_081.py` extracts the command from the carrier and executes it; the test proves the documented invocation rather than copying it.

## Gate

No `blocking` entry. The `Implemented → Ready for Review` code condition is not the reason the feature is `Blocked`; the acceptance gate (SC-001 1/3, SC-002 partial) is. The feature stays `Blocked` until 081b/081c/081d close the final-path criteria.
