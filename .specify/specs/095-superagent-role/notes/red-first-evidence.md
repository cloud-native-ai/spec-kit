# Red-first evidence — 095-superagent-role

Landing point for every row that must go red before its subject exists. Each instance records: the
command, its real output, and its exit status. When an instance binds a claim to a gate, it quotes the
gate row verbatim (id + name + check command) — a bare gate id is never used.

Every test command runs through the single runner `bash scripts/bash/run-tests.sh` (default
`-n <effective> --dist load`; test paths and arguments are forwarded verbatim). Interpreter-level test
commands are never the entry.

## Instances

(none yet — the tasks stage writes this header only; the implement rows append below)
