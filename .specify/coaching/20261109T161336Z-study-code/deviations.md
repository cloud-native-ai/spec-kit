# Deviations — /study-code (core-concepts study)

**Run**: `20261109T161336Z-study-code` · findings cite `observation.md` rows and artifact paths.

## Outcome Correctness

| ID | Expectation | Finding | Evidence |
|---|---|---|---|
| D-O1 | OC-1: follow the SKILL.md flow | **Met** — all five steps executed in order; the report is the step-5 deliverable. | observation §Steps |
| D-O2 | OC-2: indexable report with the core-concepts answer | **Met** — `docs/overview.md` carries the index table + anchors + lookup guide; the core-concepts answer is in the return §核心概念要点 1–6. | `docs/overview.md`, return tail |
| D-O3 | OC-3: target unmodified; workspace writable outside the target | **Met with a disclosed fallback** — the skill's default `$WORK_DIR/../study-code/` was unwritable; the run used `~/tmp/study-code/…` (a sanctioned temp root) instead. | return §执行轨迹 step 1; observation §Primary artifact |
| D-O4 | OC-4: evidence-traceable claims, strip manifest | **Met** — 42 evidence paths, 29/29 anchors, 21 index rows self-checked; strip manifest records 301→120. | `self-check-evidence.txt`, `strip-manifest.md` |
| D-O5 | OC-5: return names workspace + artifacts | **Met** — the return names both. | return §产出 |

## Process Efficiency

| ID | Expectation | Finding | Evidence |
|---|---|---|---|
| D-P1 | PE-1: shallow clone + strip | **Met with correction** — the shallow clone returned empty because the target `.git` is corrupted; the run verified the object store and materialized the working tree, which is the honest alternative. | return anomaly ① |
| D-P2 | PE-2: no build/test against the target | **Met** — none executed. | return §执行轨迹 |
| D-P3 | PE-3: bounded reading | **observation-gap** — the return does not enumerate reads; not inferred. | — |

## Skill-level deviations (feed the improvement plan)

| ID | Class | Finding |
|---|---|---|
| D-S1 | process-deviation | **The skill's workspace default is not probed for writability before cloning.** A root-owned target parent made the declared default fail; the fallback ladder existed only in the executor's judgment. |
| D-S2 | process-deviation | **No source-integrity preflight.** A corrupted `.git` (refs zeroed, index unreadable) produced an empty shallow clone; the working-tree materialization path is improvisation, not skill text. |
| D-S3 | process-deviation | **The diagram-backend degradation is not codified.** The run degraded to Mermaid sketches + retained `.puml` + a visible note — correct behavior, but no skill step owns it. |
| D-S4 | **harness-deviation** | **Fork evidence was deleted mid-run** (the whole `forks/` scratch). The return survived only in the qoder session store. Coach-side, not Trainee-side. User confirmed the temp cleanup was planned; the lesson is to write fork evidence to durable spec paths, not only scratch. |

## Divergence between the coach's reading and the Trainee's execution

The coach expected the skill's default workspace and a routine shallow clone; the actual target is root-owned and
its `.git` is damaged, so the Trainee legitimately took two corrections. The core request (core concepts) was
answered beyond the minimum with a full indexable report.
