# Expectation — /study-code (core-concepts study of dsh-superagent-prototype)

**Run**: `20261109T161336Z-study-code` · **Coach date**: 2026-11-09 · **Zero side effect**: this file writes
nothing to the Trainee's flow; the coach runs no Trainee step.

## Target

- Raw identifier: `/study-code` · Normalized: `study-code` · **Decision class: `skill`** (external;
  canonical `skills/external/study-code/SKILL.md`, installed mirror `.specify/skills/study-code/SKILL.md` —
  the same skill in two layers, one hit; no command template named `study-code` exists).
- `<work>` (verbatim): `分析 /storage/project/cloud-native-ai/dsh-superagent-prototype 中的核心概念`

## The coach's reading of the work

The user asks for the target repository's **core concepts**. The Trainee's own SKILL.md defines a five-step
flow (strip-repo → outline-code → outline-docs → deep-study → report) and an indexable-report contract. A
correct execution answers the request through that flow, with the core-concepts analysis as the deep-study
deliverable and the report as the primary artifact — not by ad-hoc reading of the in-place repo.

## Execution expectation (outcome correctness)

| ID | Expectation |
|---|---|
| OC-1 | The Trainee follows its own SKILL.md flow (or a justified subset that still reaches deep-study and the report); no coach-style ad-hoc substitution of the flow. |
| OC-2 | The primary artifact is an **indexable report** (index table + stable anchors + evidence paths + lookup guide) at the skill-declared location, with the **core concepts** section directly answering the user's ask. |
| OC-3 | The target repository is never modified. The study workspace is writable and outside the target repo (or a justified, disclosed exception). |
| OC-4 | No invented facts: every core-concept claim is traceable to a path in the studied copy; the strip manifest records what was deleted and why. |
| OC-5 | The return states the study workspace path and the artifact paths. |

## Process expectation (efficiency)

| ID | Expectation |
|---|---|
| PE-1 | Shallow clone + strip rather than reading the in-place repo at full depth. |
| PE-2 | No build / test / full-suite execution against the target; no writes into the target. |
| PE-3 | Bounded reading — the five steps each land once; no repeated full re-reads to produce the report. |

## Dispatch declaration

One dispatch, no retries inside this run. The dispatched executor's own reported steps are the observation
surface; anything it does not cover is an `observation-gap`, never invented.
