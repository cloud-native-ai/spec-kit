---
name: coaching-skills
description: |
  Coach another Skill (the Trainee) through one real work item: state the expected outcome and process efficiency first, dispatch exactly one subagent to execute the Trainee's own SKILL.md, observe what actually happens, then report the deviations and a micro-adjustment plan. Use this when the user mentions ["教练", "陪练", "观察执行", "预期 vs 实际", "执行偏差", "微调建议", "coaching"], or invokes it as `coaching-skills <trainee-name|trainee-path> <work>`.
skill_id: "<SKILL:.specify/skills/coaching-skills/SKILL.md>"
classification: external
---

# coaching-skills

## Goal

Coach one Trainee skill through one real work item: state the execution expectation
first (outcome correctness and process efficiency), dispatch exactly one subagent to
execute the Trainee's own `SKILL.md`, observe what actually happens, compare the two,
and hand a micro-adjustment plan to the existing `improve-skills` entry. The Trainee's
real work is the primary result; optimizing the Trainee is secondary.

## Inputs

Invocation: `coaching-skills <trainee-name|trainee-path> <work>`.

- Exactly two positional parameters: `<trainee-name|trainee-path>` and `<work>`.
- `<work>` MUST be non-empty and enters the run and the dispatch payload verbatim;
  never rewrite, summarize, or re-scope it.
- A missing or empty parameter fails closed and names the missing parameter; never
  substitute one parameter for the other and never pick a topic on the user's behalf.
- Missing-argument handling is a plain one-sentence clarification, then stop. It is
  not a confirmation step.

## Trainee Resolution

Reuse the `run-skills` position ladder, with no second resolution rule: canonical
internal → canonical external → installed internal → installed external.

- A source hit and its installed mirror hit are one hit for the same skill; only two
  distinct layers carrying the same name are two hits.
- Two hits: fail closed naming both candidate paths; never pick the nearest.
- Zero hits: fail closed naming the resolved identifier and the searched coordinates.
- Reject before the expectation phase when the directory has no readable `SKILL.md`
  or its frontmatter is invalid.
- Reject a target that resolves to `coaching-skills` itself: recursion depth is 1 and
  no dispatch happens.
- When the host can only load by explicit path, use the `run-skills` explicit-path
  mode and record it in the DispatchRecord `mode`.
- Read the Trainee's `SKILL.md` and the reference files it needs; change nothing and
  trigger no Trainee side effect in this phase.

## Preflight

Run these checks in order before writing any artifact:

1. both positional parameters are present and `<work>` is non-empty;
2. exactly one Trainee hit resolves from the ladder, with valid frontmatter and a
   target other than this skill;
3. the run directory does not already exist (see § Run Identity).

Any failure stops the run before the expectation phase and names what failed and
where it was searched. A run that passes preflight proceeds to write the expectation;
nothing else is a precondition.

## Run Identity

- `run-id`: `YYYYMMDDTHHMMSSZ-<trainee-slug>` — a UTC timestamp plus the lowercase
  kebab slug of the resolved Trainee name.
- Run directory: `.specify/memory/coaching/<run-id>/`, created before the expectation
  is written.
- If the directory already exists the run fails closed naming the existing path;
  MUST NOT append a suffix and MUST NOT reuse the directory.
- All four artifacts live inside the run directory; no artifact path escapes it.

## Artifacts and Order

Exactly four files, in this order:

1. `expectation.md`
2. `observation.md`
3. `deviations.md`
4. `improvement-plan.md`

- `expectation.md` MUST land on disk before the first action of the dispatched
  subagent. The DispatchRecord field `dispatched-at` is the ordering evidence.
- Observation, deviations and improvement plan follow in that order; a missing file
  fails the run regardless of how good the others are.
- The two closed status values are recorded once, in `improvement-plan.md` § Run
  Status.

## Execution First

- The primary success condition is: the Trainee's real work completed and its primary
  artifact exists.
- Optimization MUST NOT be a precondition of execution and MUST NOT shorten, redirect,
  or simplify the execution to collect optimization material.
- The coach MUST NOT run any Trainee step in parallel with the subagent.

## Single Dispatch

- Dispatch exactly one subagent per run. A failed, timed-out, or refused dispatch is
  recorded as such and never retried inside the same run.
- After a failed dispatch, continue into `deviations.md` and `improvement-plan.md` —
  continue means exactly that and nothing more.
- The coach never executes Trainee steps itself and never injects side effects into
  the subagent's work.

## Compare

Write `deviations.md` by comparing the expectation with the observation on both
dimensions: `## Outcome Correctness` and `## Process Efficiency`.

- Every finding cites concrete evidence from `observation.md`: a step id and/or an
  artifact path.
- Classify every finding `result-deviation` or `process-deviation`; a partially
  completed Trainee flow separates the two classes.
- State where the coach's reading of `<work>` and the Trainee's actual
  reading/execution materially diverged beyond normal execution noise.

## Improvement Plan

Write `improvement-plan.md` with entries ordered by priority.

- Each entry names a concrete Trainee file and section plus one concrete tweak;
  generic advice ("improve clarity", "be more careful") is invalid.
- Each entry cites `D-*` findings, or is marked `evidence: none` when no execution
  evidence exists.
- When observation is empty the plan is still produced; it is never dropped for lack
  of evidence.

## Optimization

- Apply the plan through the existing `improve-skills` entry, passing the Trainee
  target and the deviation evidence. Do not rewrite Trainee files directly and do not
  change that entry's contract.
- Claim protocol: the sole owner is `data-model.md` § Optimization claim. Apply that
  section's single timing (after the execution loop and the plan are written, before
  `improve-skills` is invoked), its atomic creation, its conflict rule and its
  release/leftover semantics exactly as written there. This skill states no second
  version and never decides a claim by scanning run directories or by any
  read-then-write sequence.
- A claim conflict fails the step closed: record `optimization: failed` and name the
  conflicting run-id, as the owner's conflict rule prescribes.
- A rejection by `improve-skills` is recorded as `optimization: failed` (or
  `unavailable` when the entry cannot be resolved); never retry in a loop.

## Run Status

Record both values once, in `improvement-plan.md` § Run Status:

- `run:` one of `success`, `partial`, `failed`.
- `optimization:` one of `applied`, `skipped`, `unavailable`, `failed`.

Report optimization beside the execution verdict, never inside it: an unavailable,
skipped, or failed optimization never turns a completed Trainee execution into `failed`.
The verdict ladder itself is owned by `data-model.md` § RunStatus — consult
it instead of restating it here. The run report restates both values and names the
four artifact paths.

## Degradation Ladder

- Host events available: steps carry `host-event`.
- Host events unavailable but the subagent's structured return is available: steps
  carry `self-report`.
- Neither: the step is a row marked `observation-gap`, counted in the gap list, never
  invented.
- No observation at all: the plan still exists, every entry is `evidence: none`, and
  the run closes `run: partial` per `data-model.md` § RunStatus.

## Boundaries

- Dispatch mechanism: host-native subagent capability first; `run-agent` is the
  fallback; `run-skills` only resolves and executes the Trainee and carries no
  dispatch duty. No second mechanism is introduced; the mode used is recorded in the
  DispatchRecord.
- Governance: this skill stays `classification: external`. Relaying a destructive
  step that belongs to the Trainee's own flow is a governance-kept relay: state the
  step to the user, obtain the answer, then dispatch; the subagent never
  self-approves.
- Dual independent context: the coach forms the expectation from its own reading of
  `<work>`. The dispatch payload carries `<work>` verbatim, the Trainee target, and
  the instruction to execute per the Trainee's own `SKILL.md`; it never carries the
  expectation, deviation guesses, or the coach's conclusions. The coach never
  pre-digests `<work>`; divergence is a reportable finding, not something to
  eliminate.

## Resources

- Expectation skeleton, derivation method and the zero-side-effect declaration:
  [`./references/prompt-templates.md`](./references/prompt-templates.md).
- Observation, deviation and improvement-plan templates: the same file.

## Resource ID
- Canonical ID: `<SKILL:.specify/skills/coaching-skills/SKILL.md>`
- Canonical Path: `.specify/skills/coaching-skills/SKILL.md`

## Available Tools & Resources

### Scripts (`./scripts/`)
- No scripts required.

### References (`./references/`)
- `./references/prompt-templates.md` — execution-expectation skeleton, derivation
  method, zero-side-effect declaration, and the later run-record templates.

### Assets (`./assets/`)
- No assets required.

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 7877db82c58c — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:coaching-skills" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:coaching-skills" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:coaching-skills" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
