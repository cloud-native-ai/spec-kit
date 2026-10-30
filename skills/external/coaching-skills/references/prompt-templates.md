# Coaching Prompt Templates

Fill-in shapes for one coaching run. The skill body owns the rules; this file owns the
skeletons, the derivation method and the phase boundaries.

## Execution Expectation Template

Path: `.specify/memory/coaching/<run-id>/expectation.md`. Write it **before any
dispatch action**; the `dispatched-at` field of `observation.md` § Dispatch is the
ordering evidence.

```markdown
## Run header
- run-id: <YYYYMMDDTHHMMSSZ-trainee-slug>
- trainee: <resolved Trainee name and path>
- started-at: <ISO-8601 UTC>

## Trainee
- identifier (verbatim):
- resolved-path:
- layer: external | internal
- failure-semantics: <extracted from the Trainee's own text>

## Outcome Correctness
<!-- `OC-1` MUST name the primary deliverable: an artifact path, or a checkable
conclusion (decision, report, verdict statement) for a Trainee that produces no
artifact. The acceptance and allowed-deviation columns accept only `pass|fail` or
`tolerance=<number><unit> severity=<low|medium|high>`; undecidable wording such as
"roughly matches" or "reasonable" is invalid in either column. -->
| id | object | acceptance | allowed-deviation | derivation |
|---|---|---|---|---|
| OC-1 | <primary deliverable> | <closed form> | <closed form> | <Trainee file#section> |
| OC-2 | <check item or verdict statement> | <closed form> | <closed form> | <Trainee file#section> |

## Process Efficiency
<!-- Every row derives from the Trainee text. `steps` is an order of magnitude
(`~5-8`), `tool-calls` is a profile (which tools, how many rounds), `retries` is the
allowed redundancy budget, and `critical-path` names the step sequence that must not
be skipped. `derivation` is a Trainee anchor or `validation-gap`; a validation-gap
row carries no invented numbers. `validation-gap` is the expectation-side unknown
marker and must not be swapped with `observation-gap`, which belongs to the
observation record only. -->
| id | steps | tool-calls | retries | critical-path | derivation |
|---|---|---|---|---|---|
| PE-1 | ~<order of magnitude> | <tools and rounds> | <allowed retries> | <named step sequence> | <Trainee file#section> |
| PE-2 | validation-gap | validation-gap | validation-gap | validation-gap | validation-gap |

## Assumptions
- <what this expectation takes for granted>

## Unknowns
- <what cannot be derived from the Trainee text and will be checked after execution>

## Forbidden Side Effects
- No Trainee tool, script or command is executed in this phase.
- No write inside the Trainee directory.
- No network or external call.
- No claim marker is created; the claim protocol belongs to `data-model.md` §
  Optimization claim and to the optimization step only.

## Trainee Failure Semantics
- <which failure stops the run, which continues, and what the Trainee promises to
  report; extracted from the Trainee's own text>
```

## Derivation Method

Produce the expectation by the mental-simulation procedure carried over from the
pre-rename skill:

1. Build the simulation contract: **Initial State**, **Rules**, **Known Constraints**,
   **Assumptions**, **Unknowns**, plus the side effects forbidden for this phase.
2. Run the mental trace step by step. For each Trainee step record the expected
   action, the state delta and a consistency check against the critical path.
3. Run the **Logic Implementation Audit**. Separate **Natural Language Logic**
   (judgement steps executed by reasoning: trade-offs, quality review, intent) from
   **Programmatic Logic** (deterministic script calls). Take each script's contract
   as given (input → output) and audit its invocation timing, preconditions and
   downstream consumption instead of simulating its internals.
4. Record the audit result in `expectation.md`: which Trainee steps are judgement,
   which are deterministic calls, and which side effects are forbidden for this
   phase.
5. Extract the Trainee's own failure semantics here; the compare phase reuses them to
   decide continue-vs-stop.

## Zero Side Effects of the Expectation Phase

The expectation phase MUST NOT:

1. execute any Trainee tool, script, or command;
2. write inside the Trainee's directory;
3. make network or external calls;
4. create the run's claim marker — that belongs to the optimization step.

Reading the Trainee's `SKILL.md` and the reference files it needs is permitted and is
the only allowed interaction.
