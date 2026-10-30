# Contract: Observation Record

**Scope**: `observation.md` (STR-015) — the dispatch record, the step table, source tagging, gap marking, and failure recording.

**Literal authority**: `observation-gap` (STR-006), `host-event` (STR-011), `self-report` (STR-012) and the file/run-directory names are owned by [`../requirements.md`](../requirements.md) § Shared Strings.

## C-1 File Shape

`observation.md` contains, in order:

1. `## Run header` — run-id, trainee, observation window.
2. `## Dispatch` — exactly one DispatchRecord block (fields: `mode`, `dispatched-at`, `payload-ref`, `returned`, `anomaly-line`).
3. `## Steps` — the step table (C-2).
4. `## Gaps` — prose list of unobservable steps and what information is missing.
5. `## Result` — the Trainee's real state: `completed` / `partial` / `failed`, with failure coordinates when not completed.

## C-2 Step Table Columns

Every row carries all of: `step`, `trigger/instruction`, `action`, `tool-call`, `state-change`, `artefact`, `elapsed`, `source`, `consistency`.

`consistency` is an observation-only judgement with two closed sub-fields:

- `on-critical-path: yes|no`
- `vs-expected-steps: within|beyond`

It MUST NOT execute the Trainee's verification logic; verifying the Trainee's output is the Trainee's job, not an observation side effect.

## C-3 Source Tagging

- `source: host-event` when the coach observed the step through host events.
- `source: self-report` when the step is known only from the subagent's structured return.
- `source: observation-gap` when neither channel carried the step.
- When both channels describe one step and disagree at field level, the `host-event` value wins.

## C-4 Gap Marking and Counting

- An unobservable step is a row with `source: observation-gap`; the step is never omitted and never reconstructed from expectation.
- `observation-gap` appears only on step rows. `## Gaps` describes gaps in plain prose and does not repeat the marker.
- The gap count is the number of step rows carrying the marker; it is reported in `## Gaps` as a count and by step id.

## C-5 Failure, Timeout, Refusal

- A failed, timed-out, or refused dispatch records its coordinates (which step, which error, which part completed) and the completed portion.
- Gaps MUST NOT mask a failure; the `## Result` section states the true state.
- The record never narrates an incomplete run as completed.

## C-6 Evidence Sufficiency

- If no observation could be collected at all, `observation.md` still exists, `## Gaps` states the total absence, and `## Result` says so plainly. Downstream, `deviations.md` and `improvement-plan.md` carry the `evidence: none` marking (see `coaching-run.contract.md` C-11).
