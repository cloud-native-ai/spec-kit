# Data Model: Coaching Skills（教练技能）

**Feature**: 078 Coaching Skills | **Plan**: [plan.md](./plan.md) | **Requirements**: [requirements.md](./requirements.md)

**Authority**: this file refines the *shape* of the records defined by `requirements.md` § Key Entities. The literal values (17 Shared Strings), the closed status vocabularies and the normative rules stay owned by `requirements.md`; a disagreement resolves there, never here.

## Entity Overview

| Entity | Carrier | Cardinality per run | Purpose |
|--------|---------|---------------------|---------|
| CoachRun | run directory name + `improvement-plan.md` § Run Status | 1 | Identity, status, and the four-artifact binding |
| TraineeTarget | `expectation.md` § Trainee | 1 | Which skill is coached, where it resolved, what `<work>` it received |
| ExpectationCriteria | `expectation.md` § Outcome Correctness / § Process Efficiency | 1 set of two | The pre-dispatch prediction, in two dimensions |
| DispatchRecord | `observation.md` § Dispatch | 1 | How the single subagent was dispatched and what payload it received |
| ObservationStep | `observation.md` step table | 0..N | One observable step of the Trainee flow |
| DeviationFinding | `deviations.md` rows | 0..N | One evidenced gap between expectation and actual |
| ImprovementEntry | `improvement-plan.md` items | 0..N | One concrete tweak aimed at a named Trainee location |
| RunStatus | `improvement-plan.md` § Run Status | 1 | `run:` and `optimization:` closed values |

## CoachRun

| Field | Type | Source / Rule |
|-------|------|---------------|
| `run-id` | `YYYYMMDDTHHMMSSZ-<trainee-slug>` (UTC, slug = resolved trainee name, lowercase kebab) | Derived at run start. If the directory already exists, the run fails closed naming the existing path — never append a suffix (two runs must never share a directory). |
| `run-dir` | `.specify/memory/coaching/<run-id>/` | The literal is owned by `requirements.md` STR-013. |
| `trainee` | TraineeTarget | Resolved once, before the expectation is written. |
| `artifacts` | fixed set of four files | `expectation.md`, `observation.md`, `deviations.md`, `improvement-plan.md` (STR-014…STR-017). No fifth product file; the claim marker is a dotfile (`.optimization-claim`). |
| `started-at` | ISO-8601 UTC | Written into `expectation.md` § Run header. |

**Validation**: all four paths exist under `/memory/coaching/`; `expectation.md` mtime precedes the first dispatch action recorded in `observation.md` § Dispatch; no path escapes the run directory.

## TraineeTarget

| Field | Type | Source / Rule |
|-------|------|---------------|
| `identifier` | string | The first positional parameter, verbatim (name or path). |
| `resolved-path` | repo-relative path | One of the four positions owned by `run-skills` (canonical internal → canonical external → installed internal → installed external); the resolution order is NOT re-specified here. |
| `layer` | `external` \| `internal` | Which layer the hit belongs to. |
| `hit-count` | integer | Source and mirror of the same skill count as **one** hit; external and internal same-name are two hits and fail closed. |
| `work` | string (verbatim) | The second positional parameter, non-empty; carried into the run and the dispatch payload unchanged. |
| `failure-semantics` | text | The Trainee's own failure semantics, extracted during the expectation phase and used to decide continue-vs-stop after a failure. |

**Validation rules**

1. Missing either positional parameter → fail closed naming the missing one; no dispatch (FR-001).
2. `hit-count = 0` → fail closed naming the four searched coordinates (FR-001).
3. `hit-count = 2` across layers → fail closed naming both candidates; never "nearest wins" (FR-001, Edge Cases).
4. `SKILL.md` absent or frontmatter invalid → refuse before the expectation phase (Edge Cases).
5. Target resolves to `coaching-skills` itself → refuse; recursion depth is 1 (Edge Cases).

## ExpectationCriteria

Two dimension sets, both required in a single `expectation.md` (missing one fails the run, FR-004).

### Outcome Correctness rows (STR-008)

| Field | Type | Rule |
|-------|------|------|
| `id` | `OC-1`…`OC-N` | `OC-1` MUST name the primary deliverable (artifact path, or a checkable conclusion for a Trainee that produces no artifact) (FR-005). |
| `object` | artifact path \| check item \| verdict statement | The thing a reader can compare against the observation record. |
| `acceptance` | binary or numeric tolerance | Closed form: `pass|fail`, or `tolerance=<number><unit> severity=<low|medium|high>` (FR-005). |
| `allowed-deviation` | same closed form as `acceptance` | "Roughly matches" and similar undecidable wording is invalid (FR-005). |
| `derivation` | Trainee section anchor | Where in the Trainee text this criterion comes from. |

### Process Efficiency rows (STR-009)

| Field | Type | Rule |
|-------|------|------|
| `id` | `PE-1`…`PE-N` | |
| `steps` | order of magnitude (e.g. `~5-8`) | MUST be derived from the Trainee text, or marked `validation-gap` (FR-006). |
| `tool-calls` | profile (which tools, how many rounds) | Same derivation rule. |
| `retries` | allowed count / redundancy budget | Same derivation rule. |
| `critical-path` | named step sequence | Same derivation rule. |
| `derivation` | Trainee section anchor **or** `validation-gap` | `validation-gap` is the expectation-side unknown marker; it is NOT `observation-gap` (which belongs to the observation record only) and the two MUST NOT be swapped. |

### Sections that travel with the criteria (FR-007 / FR-008)

`## Assumptions`, `## Unknowns`, `## Forbidden Side Effects` (explicit zero-side-effect declarations for the expectation phase), `## Trainee Failure Semantics`.

## DispatchRecord

| Field | Type | Rule |
|-------|------|------|
| `mode` | `native` \| `run-agent-fallback` \| `run-skills-explicit-path` | Which carrier performed the dispatch — recorded, never assumed (A5 / FR-025). |
| `dispatched-at` | ISO-8601 UTC | MUST be later than `expectation.md` mtime (SC-002). |
| `payload-ref` | `dispatch-payload.contract.md` | The payload's field set is owned there; this record points at it and stores only the rendered payload path/hash. |
| `returned` | `completed` \| `partial` \| `failed` \| `timeout` \| `refused` | The subagent's terminal state as observed. |
| `anomaly-line` | text \| `none reported` | The explicit anomaly line the payload requires on return; silence is not read as clean. |

**Validation**: exactly one DispatchRecord per run; a second entry is a contract violation even when the first failed (FR-009 / FR-013).

## ObservationStep

Step table columns (all required per row, FR-011):

| Column | Content |
|--------|---------|
| `step` | `S1`, `S2`, … (or the Trainee's own step ids when it numbers them) |
| `trigger/instruction` | Which instruction of the Trainee caused this step |
| `action` | What the subagent did |
| `tool-call` | Tool name + key argument (or `—`) |
| `state-change` | What changed in the environment/artifacts |
| `artefact` | Path produced or touched (or `—`) |
| `elapsed` | Duration of the step |
| `source` | `host-event` \| `self-report`; `observation-gap` marks the whole row when the step is not observable |
| `consistency` | Observation-only judgement: `on-critical-path: yes|no`, `vs-expected-steps: within|beyond`. It MUST NOT execute the Trainee's verification logic (FR-011). |

**Rules**

1. A not-observable step is a row with `source: observation-gap`; the row is counted as a gap and is never omitted or invented (FR-011, SC-004).
2. `## Gaps` summarizes gaps in plain prose without repeating the marker — the marker is counted only on step rows (FR-011).
3. Field-level conflict between `host-event` and `self-report` resolves to `host-event` (A6).
4. A failed/timed-out/refused run records the failure coordinates and the completed part; gaps never mask a failure (FR-013).

## DeviationFinding

| Field | Type | Rule |
|-------|------|------|
| `id` | `D-1`…`D-N` | |
| `dimension` | `correctness` \| `efficiency` | Exactly the two dimensions of the expectation (FR-014, SC-003). |
| `expected` | id of an `OC-*` / `PE-*` row | Traceability back to the expectation. |
| `actual` | observed value | |
| `evidence` | step id(s) and/or artifact path | Every finding cites concrete evidence from the observation record (FR-014). |
| `severity` | `low` \| `medium` \| `high` | |
| `class` | `result-deviation` \| `process-deviation` | A partially completed run MUST separate these two classes (Edge Cases). |
| `coach-vs-trainee` | `aligned` \| `diverged` (+ one line) | Where the coach's reading of `<work>` and the Trainee's actual reading/execution materially differ beyond execution noise (FR-029). |

**Validation**: with zero observation evidence the file still exists, every finding carries no execution evidence, and the run closes `run: partial` (Edge Cases).

## ImprovementEntry

| Field | Type | Rule |
|-------|------|------|
| `priority` | integer | Ordered application order. |
| `target-location` | `path#section` inside the Trainee | MUST name a concrete file and section, not "the skill in general" (FR-015). |
| `tweak` | one concrete adjustment | A tweak/adjustment, not a restatement of the symptom. |
| `evidence` | `D-*` ids, or `evidence: none` | `evidence: none` marks an assumption with no execution evidence (Edge Cases). |
| `optimization` | closed value (STR-010) | Recorded for the entry set as a whole in § Run Status. |

## RunStatus

The single definition point for the run's two closed values (written as the last section of `improvement-plan.md`):

| Field | Domain | Rule |
|-------|--------|------|
| `run` | `success` \| `partial` \| `failed` | `success` requires the primary artifact to exist and meet its `OC-1` criterion; `failed` covers a failed Trainee flow with no usable result; everything else is `partial` (FR-017). |
| `optimization` | `applied` \| `skipped` \| `unavailable` \| `failed` | Independent of `run`; an unavailable/rejected optimization never turns the execution into a failure (FR-017, SC-005). |

## State Transitions

### Run lifecycle

```text
preflight → expectation-written → dispatched → observed
          → deviations-written → plan-written → optimization-applied
                                             → optimization-skipped
                                             → optimization-unavailable
                                             → optimization-failed
```

| From | To | Guard |
|------|----|-------|
| preflight | expectation-written | Trainee resolved uniquely, `<work>` non-empty, run directory created |
| expectation-written | dispatched | `expectation.md` exists with both dimension sections; claim created only if an optimization will be attempted |
| dispatched | observed | exactly one DispatchRecord exists |
| observed | deviations-written | observation record written (gaps counted) |
| deviations-written | plan-written | every finding cites evidence or is marked `evidence: none` |
| plan-written | optimization-* | `improve-skills` entry resolved, rejected, or unavailable |

### Failure branch

```text
dispatched → observed(failed) → deviations-written → plan-written → optimization-*
```

No transition returns from the failure branch to `dispatched` — the single-dispatch rule forbids a retry (FR-013).

### Optimization claim

```text
no-claim → claimed(this run-id, trainee) → released
                                       → left-behind (crash; blocks the same trainee on later runs)
```

Claim file: `<run-dir>/.optimization-claim` containing `trainee: <resolved-path>` and `run-id: <run-id>`. Before claiming, the skill scans `.specify/memory/coaching/*/.optimization-claim`; a claim naming the same Trainee under a different run-id fails the optimization step closed and names that run-id (FR-028). Distinct Trainees never collide because the file is per run directory.

### Degradation ladder

```text
host events available → source: host-event
host events unavailable, self-report available → source: self-report
neither → source: observation-gap  (counted, never invented)
no observation at all → plan written with evidence: none, run: partial
```

## Cross-Entity Invariants

1. **Order**: `expectation.md` before the first dispatch action (SC-002).
2. **One dispatch**: exactly one DispatchRecord and exactly one subagent execution per run (FR-009).
3. **No re-run**: the coach never executes Trainee steps itself and never injects extra side effects (FR-012).
4. **Isolation**: each run writes only inside its own run directory, so two concurrent runs write different paths (FR-028).
5. **Honesty**: gaps are counted, never filled; failures are recorded as failures (SC-004 / FR-013).
6. **Primary result**: the Trainee's real output is the primary result; optimization status is reported separately (FR-010 / FR-017).
