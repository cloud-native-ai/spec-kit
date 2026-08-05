# Contract: Write-Set and Migration

**Requirement**: 037-goal-registry | **FRs**: FR-007, FR-020, FR-022, FR-023, FR-024
**Supersedes for the goal face**: requirement 036's `contracts/summary-writeset.contract.md` delivery-directory rows — the invariants are unchanged, the paths move.

## Write-set allow-list

During the summary/SUMMARIZE step the writable surface is exactly:

```text
.specify/goal/<goal-slug>/summary/**        # the derived subtree
.specify/memory/feedback/**                 # feedback store (unchanged from 036)
```

Everything else MUST remain byte-identical for the duration of the step, specifically these six groups:

| # | Group | Rule |
|---|-------|------|
| 1 | `.specify/goal/<goal-slug>/goal.md` | authored definition — **new group added by this requirement** |
| 2 | `.specify/teams/**` | team artifacts |
| 3 | the monitored target | whatever the team observes |
| 4 | the `summarize-project` skill's own files | invoked skill must not self-modify |
| 5 | `.specify/agents/**` | agent definitions |
| 6 | `.specify/project/**` | pre-existing `manage-project` era artifacts; after migration this tree holds no goal content at all |

- **WS-1** The allow-list replaces 036's deny-list formulation. A single writable subtree is the reason "zero writes to the definition" is mechanically checkable.
- **WS-2** A write landing outside the allow-list is a violation, not an incidental update — including a write to `goal.md` in the same goal directory.
- **WS-3** Writes are atomic: temporary file plus same-directory replace. A half-written delivery directory is a forbidden state.
- **WS-4** Refresh remains serialized by the directory lock at `summary/data/.refresh.lock` with a 900-second stale threshold. A yielding refresh exits `4` (serialized) and MUST NOT silently no-op.
- **WS-5** Normal team-cycle writes (`STATE.md`, `items.jsonl`, `run-log.jsonl`, `runs/<ts>-report.md`, result manifests) are outside this contract's scope — the invariance constraint binds the summary step only, not the whole run.

## Path migration

Exactly one construction site changes in the generator, and its derived defaults follow:

| Before | After |
|--------|-------|
| `.specify/project/goal/<goal-slug>/` | `.specify/goal/<goal-slug>/summary/` |
| `.specify/project/goal/<goal-slug>/data/project-input.yaml` | `.specify/goal/<goal-slug>/summary/data/project-input.yaml` |
| `.specify/project/goal/<goal-slug>/data/.refresh.lock` | `.specify/goal/<goal-slug>/summary/data/.refresh.lock` |

Verified by execution against the `goal-share-a` / `goal-share-b` fixtures: the generator today reports `delivery_dir = .specify/project/goal/shared-harvest-goal` and writes `data/project-input.yaml` beneath it, confirming a single path root drives every derived location.

- **MG-1** `.specify/project/` MUST hold no goal artifacts after migration. Exactly one goal-indexed directory exists in the project.
- **MG-2** The migration carries **no data**: `.specify/project/goal/` was never materialized in this repository — the generator creates it on demand. This is a code, documentation, and test migration.
- **MG-3** The pre-existing `.specify/project/` contents (`project.md`, wbs/gantt/milestones charts) MUST NOT be moved, overwritten, or deleted.

## Reference surface

The migration is scoped by face. Live surfaces MUST reach zero residual references; historical surfaces MUST NOT be touched.

| Face | Count | Disposition |
|------|-------|-------------|
| canonical source | 4 | rewrite |
| `.specify/` mirrors | 4 | regenerate via `sync-mirrors.py --write` |
| per-tool generated copies | 5 | regenerate; never hand-edit |
| tests | 9 | rewrite path literals only |
| user documentation | 1 | rewrite |
| Tool record | 1 | rewrite |
| **live total** | **24** | residual references MUST be 0 |
| historical (036 spec artifacts, 037 spec, feedback records, feature memory) | 18 | MUST NOT be rewritten — rewriting them falsifies the record |
| `__pycache__/*.pyc` | 9 | build artifacts; ignored |

- **RS-1** A whole-repository zero is unachievable by construction: the 2026-08-04 Clarifications entry quotes the old path verbatim as the user's directive.
- **RS-2** `tests/contract/test_summary_trigger.py` asserts the old path string across the canonical file, its mirror, and all five tool copies. It breaks by design on migration and MUST be updated to the new path in the same change.
- **RS-3** Test updates are path-only. No assertion may be weakened, deleted, or made less specific to accommodate the migration.
- **RS-4** `tests/integration/test_summary_four_patterns.py` guards that the real repository tree stays byte-unchanged; it is the migration's regression net and MUST keep passing.

## Verification

| Check | Command | Expected |
|-------|---------|----------|
| live residual references | `grep -rl 'project/goal'` classified by face | 0 on the live face |
| mirror parity | `python3 scripts/python/sync-mirrors.py --check` | exit 0 |
| no regression | `pytest -q`, diffed against `baseline-failed.txt` | no new failure names |
| definition untouched by refresh | content fingerprint of `goal.md` before/after a refresh | identical |
