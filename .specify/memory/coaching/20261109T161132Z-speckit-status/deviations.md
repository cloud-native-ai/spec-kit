# Deviations — /speckit.status (no-argument execution)

**Run**: `20261109T161132Z-speckit-status` · every finding cites `observation.md` rows and/or artifact paths.

## Outcome Correctness

| ID | Class | Expectation | Finding | Evidence |
|---|---|---|---|---|
| D-O1 | result-deviation | OC-1: default `digest` executed | **Met** — the digest ran as the default action; neither guard nor report was selected. | observation §Steps 4; return §2–3 |
| D-O2 | result-deviation | OC-2: stdout verbatim + exit status | **Met** — the digest is reproduced in the return and closes with `last_completion=…`; exit `0` stated. | observation §Primary artifact |
| D-O3 | result-deviation | OC-3: exit 3 preserved | **Not applicable** — the run returned exit 0; no `nothing-running` case arose. | return §3 |
| D-O4 | result-deviation | OC-4: thin entry, no second projection | **Met** — the entry rendered nothing of its own; no re-judged propositions. | return §2–5 |
| D-O5 | result-deviation | OC-5: Wrap-up chain executed/evidenced | **Met** — determination, exec-quant, feedback recorded; docs sync eval and token reflection explicitly adjudicated. | return §3–4 |

## Process Efficiency

| ID | Class | Expectation | Finding | Evidence |
|---|---|---|---|---|
| D-P1 | process-deviation | PE-1: one digest invocation | **Met** — one digest reading; wrap-up engines invoked once each. | return §3 |
| D-P2 | process-deviation | PE-2: no extra analysis | **Met** — output copied, not extended; the one analysis remark is a recorded feedback point, not a re-judgement. | return §2/§4 |
| D-P3 | process-deviation | PE-3: no extra file reads | **observation-gap** — the return does not enumerate reads beyond the engines it invoked. Not inferred. | — |
| D-P4 | **process-deviation** | (transport) completion signal | **Coaching-harness deviation**: every fork dispatch reads `sentinel=0` because the closed coaching payload carries no sentinel instruction; completion was correctly judged by exit 0 + the primary artifact. No Trainee impact. | `forks/coach-status/status-coach-status-dispatch` |
| D-P5 | **process-deviation** | (dispatch hygiene) | **Coaching-harness deviation**: the reused fork directory held a previous run's `status` file (mtime 19:47), producing a premature completion event; the monitor was re-armed on PID liveness. No Trainee impact. | fork dir listing; monitor `b6gxul4t7` → re-armed |

## Divergence between the coach's reading and the Trainee's execution

No material divergence. The coach read `<work>` as the no-argument digest; the Trainee executed exactly
that, then followed its own closeout contract to the `ask` branch and surfaced one open input (the
feature-branch name for a record-only run) instead of guessing — consistent with the injected
confirmation-relay. The Trainee went one step beyond the minimum by recording a substantive framework
feedback point (digest header lacks the resolved registry directory; 074 label/derived-state split).
