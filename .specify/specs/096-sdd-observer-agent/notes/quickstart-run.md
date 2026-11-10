# Quickstart run — 096-sdd-observer-agent

Executed end to end against the implemented tree (T045). Worktree `096-sdd-observer-agent`,
HEAD `3fd3c41f6`, 2026-11-10. Fixture scenarios ran under the sanctioned scratch root
`.specify/.tmp/096/quickstart/` and were torn down afterwards.

| Scenario | Command | Exit | Reading |
|---|---|---|---|
| S-0 | `ls agents/sdd-observer.agent.md .specify/agents/templates/sdd-observer.agent.md`; `ls skills/external/sdd-loop-driver/references/observer-lifecycle.md`; `ls shared/declarations/facts/journal-format.yaml scripts/python/journal-utils.py` | 0 | all six surfaces exist; template 5426 B, mirror 5426 B |
| S-1 | `bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_lifecycle.py -q -k "entry_switch_and_disabled_state or startup_point_is_driver_owned_and_decidable or record_section_shape_is_owned_by_the_section"` | 0 | 3 passed — switch `observer: on|off` (default `on`, `off` → `state: disabled`), startup point (line registered + spine created + before first U2), record-section shape owned by SKILL.md § SDD Observer |
| S-2 | engine `--action append` against the line fixture | 0 | `{"action": "append", ..., "appended": 47, "seq_last": 47}`; title `# SDD Journal — 096-sdd-observer-agent`; single nine-column table; 47 rows, `seq` 1..47 |
| S-3 | engine `--action check` on the same fixture | 0 | `journal.md: 0 findings` |
| S-4 | five tamper drills on journal copies | 1/1/1/1/1 | (a) tenth column → V-11; (b) unknown event → V-5; (c) free narrative → V-12; (d) forged pointer → V-10; (e) seq 1,2,4 → V-3 |
| S-5 | failure fixtures + restart gap | 0 | start failure: 1 record `state: failed` + reason, terminal stage `exit=0 sentinel=1`; mid-run kill: states `started → failed → started`, terminal stage `exit=0 sentinel=1`; restart after a 60 s window appends exactly 1 `observer-gap` row |
| S-6 | dual-line fixture | 0 | two journals, identities `sdd-observer-line-a` / `sdd-observer-line-b`, zero shared paths; held-lock second writer exits 3 `concurrent-writer-refused` |
| S-7 | `validate-requirements.py`; `overlap-check.py`; three-module runner selection | 0 | requirements `status: ok` 0 error/0 warning (254 lines); overlap `decision=overlap` (adjudicated additive coexistence); 50 passed |

## S-1 — driver behavior (template-pinned)

```text
...                                                                      [100%]
3 passed in 6.32s
```

## S-0 — shipped surfaces

```text
-rw------- 1 agent agent 5426 Nov 10 22:08 agents/sdd-observer.agent.md
-rw------- 1 agent agent 5426 Nov 10 22:08 .specify/agents/templates/sdd-observer.agent.md
-rw------- 1 agent agent 5438 Nov 10 23:00 skills/external/sdd-loop-driver/references/observer-lifecycle.md
-rw------- 1 agent agent 37164 Nov 10 22:02 scripts/python/journal-utils.py
-rw------- 1 agent agent  3072 Nov 10 21:53 shared/declarations/facts/journal-format.yaml
```

## S-2 — append

```text
exit: 0
stdout: {"action": "append", "journal": ".specify/specs/096-sdd-observer-agent/journal.md", "appended": 47, "seq_last": 47}
title: # SDD Journal — 096-sdd-observer-agent
header: | seq | observed_at | event_at | stage | event | command | artifact | exit | evidence |
entry rows: 47
first row: | 1 | 2026-11-10T15:26:39Z | - | - | line-start | - | - | - | persistent:spine:.specify/state/line-demo.md |
```

## S-3 — check

```text
exit: 0
stdout: .specify/specs/096-sdd-observer-agent/journal.md: 0 findings
```

## S-4 — tamper drills (all must turn red)

```text
(a) ten-column -> exit 1 | V-11: <fixture>/journal.md:57
(b) unknown-event -> exit 1 | V-5: <fixture>/journal.md:57
(c) free-narrative -> exit 1 | V-12: <fixture>/journal.md:59
(d) forged-pointer -> exit 1 | V-10: <fixture>/journal.md:57
(e) seq-renumber-1-2-4 -> exit 1 | V-3: <fixture>/journal.md:13
```

## S-5 — observer failure never gates the line

```text
start-failure records: [{'state': 'failed', ..., 'execution_label': '-', 'reason': 'observer start failed (fixture: dispatch refused)'}]
terminal stage settled: True
mid-run-kill states: ['started', 'failed', 'started']
terminal stage settled: True
observer-gap rows: 1
| 48 | 2026-11-10T15:26:40Z | 2026-11-10T15:26:40Z | - | observer-gap | - | - | - | persistent:spine:.specify/state/line-demo.md#Observer Record — ...; persistent:commit:<sha> |
```

## S-6 — two parallel lines

```text
append line-a exit=0
append line-b exit=0
identity L1: sdd-observer-line-a | identity L2: sdd-observer-line-b
shared paths: 0
second writer exit: 3 | concurrent-writer-refused
```

## S-7 — boundary confirmations

```text
validate-requirements: status ok — scanned 254 lines, 30 definition rows, 3 shared strings; 0 error(s), 0 warning(s)
overlap-check: decision=overlap — checked=77 overlaps=305 (adjudicated: additive coexistence; see plan/analyze)
three modules: 50 passed in 7.40s
```

## Teardown

```text
teardown: scratch removed = True
```
