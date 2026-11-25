# Expectation — /speckit.status (no-argument execution)

**Run**: `20261109T161132Z-speckit-status` · **Coach date**: 2026-11-09 · **Zero side effect**: this file
writes nothing to the Trainee's flow; the coach runs no Trainee step.

## Target

- Raw identifier: `/speckit.status` · Normalized: `speckit.status` → command name `status` ·
  **Decision class: `command`** (scanning both lists: `templates/commands/status.md` is the only hit; no
  skill named `status` or `speckit.status` exists in either layer).
- Resolved executor: `templates/commands/status.md` (its generated per-tool copies are aliases).
- `<work>`: empty — the **no-argument** form of the command (default action = digest).

## Execution expectation (outcome correctness)

| ID | Expectation |
|---|---|
| OC-1 | The default `digest` action is executed: `python3 .specify/scripts/python/status-digest.py --action digest` from the repository root. Neither `guard` nor `report` is selected. |
| OC-2 | The script's stdout is the primary artifact: it is reproduced **verbatim**, and its exit status is reported. No paraphrase, no re-render, no label rewrite. |
| OC-3 | Exit `3` (nothing active) is preserved as the explicit `nothing-running` rendering if returned — never softened into an empty result. |
| OC-4 | The thin entry renders nothing of its own: no second projection of state, no re-judging of propositions. |
| OC-5 | The command's declared Wrap-up chain is executed (or its deferral is explicitly stated per the template). |

## Process expectation (efficiency)

| ID | Expectation |
|---|---|
| PE-1 | Exactly one digest invocation (no redundant re-runs for the same reading). |
| PE-2 | No extra analysis pass: the output is copied, not interpreted or extended. |
| PE-3 | No file reads beyond what the Trainee's own contract requires. |

## Dispatch declaration

One dispatch, no retries inside this run. The dispatched executor's own reported steps are the observation
surface; anything it does not cover is an `observation-gap`, never invented.
