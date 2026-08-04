# Contract: Summary Trigger & Gating

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Covers**: FR-012…FR-016, FR-028
**Pinned by**: `tests/contract/test_summary_trigger.py`
**Edited surfaces**: `skills/create-team/SKILL.md`, `templates/commands/team.md` (+ 6 mirrors/copies)

## Trigger points

| Pattern | Boundary | Insertion point in the existing flow |
|---------|----------|--------------------------------------|
| `continuous` | end of every Nth cycle | new phase **9. SUMMARIZE**, after existing phase 8 REPORT |
| `iteration` | after each generation's DECIDE phase | after DECIDE, before the next generation's COORDINATE |
| `serial` | after each stage handoff verification passes | after per-handoff verification, before the next stage dispatch |
| `parallel` | after cross-verification and aggregation complete | after Result Aggregation |
| all | goal met, convergence, halt, or manual stop | terminal summary at run wrap-up |

**Scope of a refresh (goal, not team)**: a boundary reached by one team refreshes **its goal's** summary, which aggregates every team declaring the same `goal_slug` ([[STR-006]]). A team never produces a team-scoped summary of its own — the team directory holds run info only.

## Gate order (normative)

Gates MUST be evaluated in this order. The first gate that blocks determines the recorded status.

1. **Budget** — at `report-only` tier or kill-switch, skip and record `skipped(budget)` ([[STR-003]]).
2. **Cadence** — not at an Nth boundary, skip and record `skipped(cadence)`.
3. **Material** — no ledger entries and no run reports, decline and record `declined(no-material)`.
4. Otherwise produce the summary and record `produced`.

- **TG-1**: Budget MUST outrank cadence. Reaching a cadence point MUST NOT force chart generation when the budget ladder has tripped.
- **TG-2**: The summary step's own consumption MUST NOT push the run over budget. A run MUST complete normally when the summary is skipped.
- **TG-3**: The summary step MUST be the first step dropped under budget pressure, and MUST NOT be retried within the same run after being skipped.
- **TG-4**: Two boundaries reached in rapid succession MUST coalesce into a single refresh, not one summary per boundary.

## Status line (FR-015)

Every run report MUST carry exactly one summary status line, using the vocabulary of [[STR-005]]:

```
Summary: produced | skipped(cadence) | skipped(budget) | declined(no-material)
```

- **TG-5**: Exactly one of the four states MUST be recorded per run. Absence of the line is a violation — it is what makes "not observed" distinguishable from "observed, no progress".
- **TG-6**: `produced` MUST be accompanied by the delivery directory path.
- **TG-7**: `skipped(budget)` MUST name the tier that caused it.
- **TG-8**: `declined(no-material)` MUST NOT be emitted alongside any chart or partial summary artifact.

## Enablement (FR-013)

- **TG-9**: A team that does not declare `config.summary` is treated as **enabled** (opt-out semantics), running at its pattern's documented default cadence.
- **TG-10**: The `continuous` default cadence MUST NOT be every cycle. Default is every 5th cycle; bounded patterns default to every boundary.
- **TG-11**: Configuration keys MUST nest under `config.summary` ([[STR-002]]). A top-level `summary:` key MUST NOT be introduced, since team preset files already use that name for a one-line preset digest.

## First-run disclosure (FR-028)

- **TG-12**: The first time a summary is produced for a team that has never had one, the run report MUST carry a one-time declaration that the mechanism has activated, naming the cadence now in force. This makes the opt-out default visible rather than silent for pre-existing teams.

## Confirmation-gate disclosure (FR-016)

The run mode's preview→confirm→execute sequence is unchanged in shape. Step 5's presentation MUST additionally disclose the summary decision for this run.

- **TG-13**: Before confirmation, the gate MUST state whether this run will produce a summary, and when it will not, which gate suppresses it.
- **TG-14**: Disclosure MUST appear in the preview, before execution, so cost is known at decision time.
- **TG-15**: The existing assertion that the team directory holds only `team.md` and `runs/` MUST be corrected wherever it appears. It is already inaccurate for continuous teams, which additionally hold `constraints.md`, `STATE.md`, and `run-log.jsonl`; this mechanism adds `items.jsonl`. Affected locations: the output-discipline line in `templates/commands/team.md`, the Rules bullet and the Hard Constraints bullet in `skills/create-team/SKILL.md`, and every mirrored copy.

## Goal-scope rules

- **TG-16**: When two teams under one goal reach boundaries close in time, the goal refresh MUST be serialized into a single successful refresh. The suppressed one MUST record a status line in its own run report; it MUST NOT silently no-op, and it MUST NOT produce a second parallel summary.
- **TG-17**: Budget gating for a goal-level refresh is evaluated against the **triggering team's** budget, since that team's run bears the cost. A team at the report-only tier MUST NOT trigger a refresh even when sibling teams have budget remaining; the refresh simply waits for whichever team next reaches a boundary with budget available.
- **TG-18**: The confirmation gate MUST disclose the resolved goal identity, whether it is explicit or inferred ([[STR-006]] absent), and the target delivery directory — so the user knows which goal's summary this run will refresh and where it lands, before confirming.

## Ordering relative to REPORT

The summary reads the run report as a provenance source, so it MUST run after the report is written. Producing a summary before the report would leave the current run's outcome unattributable.
