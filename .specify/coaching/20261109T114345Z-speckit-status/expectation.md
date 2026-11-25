## Run header
- run-id: 20261109T114345Z-speckit-status
- chain: user → /speckit.status   (direct run; no subject)
- trainee: /speckit.status at templates/commands/status.md
- subject: (none — no-argument execution)
- started-at: 2026-11-09T11:43:45Z

## Trainee
- identifier (verbatim): /speckit.status
- resolved-path: templates/commands/status.md
- executor-kind: command
- layer: n/a (command)
- subject-resolution: self (Trainee is the subject)
- failure-semantics: the entry is thin — it must print the script's output verbatim and report the exit
  status; a paraphrase, a re-rendering, or a fabricated verdict is a contract failure. Default action with
  empty input is the digest.

## Outcome Correctness
| id | object | acceptance | allowed-deviation | derivation |
|---|---|---|---|---|
| OC-1 | the digest produced by `python3 .specify/scripts/python/status-digest.py --action digest` and printed verbatim, plus the reported exit status | output non-empty; printed block equals the script stdout; exit ∈ {0,3} (3 = nothing-running is correct) | tolerance=0 | templates/commands/status.md § Delegation / three actions |
| OC-2 | no paraphrase or second rendering by the entry | the printed digest is byte-identical to the script's stdout | tolerance=0 | templates/commands/status.md § Delegation |

## Process Efficiency
| id | steps | tool-calls | retries | critical-path | derivation |
|---|---|---|---|---|---|
| PE-1 | ~3-5 | 1-2 Bash rounds (read template, run script) | 0 | resolve script → run digest → print → report exit | templates/commands/status.md § Delegation |
| PE-2 | validation-gap | validation-gap | validation-gap | validation-gap | validation-gap |

## Assumptions
- The script runs from the repository root; a non-TTY child resolves `--format auto` to the text (kv) render.
- The digest lists registry-backed lines only; our active state-spine lines are not registered (known gap).

## Unknowns
- The child's stdout is not a TTY; the table render is therefore not exercised by this run.

## Forbidden Side Effects
- No Trainee tool, script or command is executed in this phase.
- No write inside the Trainee's directory (templates/commands/).
