# Contract: Execution Expectation

**Scope**: the pre-dispatch prediction file `expectation.md` (STR-014), its two mandatory dimension sections, and the zero-side-effect rule of the expectation phase.

**Literal authority**: section names, file name and run directory are owned by [`../requirements.md`](../requirements.md) § Shared Strings (STR-007…STR-009, STR-013, STR-014).

## C-1 File Shape and Timing

- The file lives at `.specify/memory/coaching/<run-id>/expectation.md`.
- It is written **before** any dispatch action. Its modification time and the DispatchRecord's `dispatched-at` are the ordering evidence.
- It contains both `## Outcome Correctness` and `## Process Efficiency`; a missing section fails the run.
- Mandatory companion sections: `## Run header` (run-id, trainee, started-at), `## Trainee`, `## Assumptions`, `## Unknowns`, `## Forbidden Side Effects`, `## Trainee Failure Semantics`.

## C-2 Outcome Correctness Rows

| Column | Rule |
|--------|------|
| `id` | `OC-1`…`OC-N` |
| `object` | An artifact path, a check item, or an explicit verdict statement |
| `acceptance` | `pass|fail`, or `tolerance=<number><unit> severity=<low|medium|high>` |
| `allowed-deviation` | The same closed form as `acceptance` |
| `derivation` | A Trainee file/section anchor |

- `OC-1` names the primary deliverable.
- A Trainee that produces no artifact MUST still have `OC-1`, naming a checkable conclusion (decision, report, or verdict statement).
- Undecidable wording (“roughly matches”, “reasonable”) is invalid in either the acceptance or the deviation column.

## C-3 Process Efficiency Rows

| Column | Rule |
|--------|------|
| `id` | `PE-1`…`PE-N` |
| `steps` | Expected step count as an order of magnitude |
| `tool-calls` | Which tools, how many rounds |
| `retries` | Allowed retry/redundancy budget |
| `critical-path` | Named sequence of steps that must not be skipped |
| `derivation` | A Trainee anchor, or `validation-gap` |

- Every row derives from the Trainee text; a row that cannot be derived is marked `validation-gap`.
- Numbers MUST NOT be invented to fill a row.

## C-4 Derivation Method

- The expectation is produced by the mental-simulation procedure formerly owned by `think-skills`: build the simulation contract (initial state, rules, constraints, assumptions, unknowns), run the trace, and audit the split between natural-language logic and deterministic script logic.
- The audit result is recorded in the file: which Trainee steps are judgement, which are deterministic calls whose contracts are taken as given, and which side effects are forbidden for this phase.
- The Trainee's own failure semantics are extracted here and reused later to decide continue-vs-stop.

## C-5 Zero Side Effects

The expectation phase MUST NOT:

1. execute any Trainee tool, script, or command;
2. write inside the Trainee's directory;
3. make network or external calls;
4. create the run's claim marker (that belongs to the optimization step).

Reading the Trainee's `SKILL.md` and the reference files it needs is permitted and is the only allowed interaction.
