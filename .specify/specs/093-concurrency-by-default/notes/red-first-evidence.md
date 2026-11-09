# Red-first evidence — 093-concurrency-by-default

Landing point for every red-first row of this feature (`tasks.md` § Tests). Each entry records, in this
order: the exact command, its **real** output (pasted, never paraphrased), and its exit status. A row
whose subject never went red before its implementation has no entry here and is not red-first.

Entry format:

```text
## <row id> — <short subject>
- command: `<exact command>`
- output:
  <real output, verbatim>
- exit status: <code>
```

Full command/output records: `test-evidence/wp1-t004-t014-t098-t026-red.txt` (WP1 reds),
`test-evidence/wp1-t005-t014-green.txt` (WP1 greens). Entries below are verbatim excerpts.

## T004 — the eight fact files do not exist (red before T004 lands)
- command: `python3 .specify/scripts/python/declaration_reader.py --action get --fact <slug> --repo .` (each of the eight slugs)
- output: `no declaration for fact '<slug>'` for every slug; e.g. `no declaration for fact 'concurrency-class'`
- exit status: 1 (each)

## T014 — the facts are unregistered through the read entry (red before the files land)
- command: same eight `--action get` invocations as T004
- output: `no declaration for fact '<slug>'` × 8
- exit status: 1 (each)

## T098 — the coordinator verdict surface is absent (red before T098 lands)
- command: `python3 .specify/scripts/python/declaration_reader.py --action get --fact coordinator-dispatch-verdict --repo .`
- output: `no declaration for fact 'coordinator-dispatch-verdict'`
- exit status: 1

## T026 — Phase-2 subjects at WP1 close (subject-absent reds; assertion-level reds land with WP4/WP2)
- command: `python3 -m pytest tests/unit/test_concurrency_check_engine.py -q` (T015)
- output: `ERROR: file or directory not found: tests/unit/test_concurrency_check_engine.py` / `no tests ran in 0.00s`
- exit status: 4
- command: `python3 -m pytest tests/contract/test_concurrency_declarations.py -q` (T016–T020)
- output: `ERROR: file or directory not found: tests/contract/test_concurrency_declarations.py` / `no tests ran in 0.00s`
- exit status: 4
- command: `python3 .specify/scripts/python/script-interface-check.py --files scripts/python/concurrency-check.py` (T025)
- output: `candidate-not-collected: requested candidate scripts/python/concurrency-check.py is not in the candidate set` / `candidates=0 applicable=0 exempt=0 violations=0`
- exit status: 1
- note: the T025/GATE-5 row quotes `script-interface-check.py scripts/python/concurrency-check.py` (positional); the tool's
  declared CLI selects candidates with `--files PATH[,PATH]` and the positional form exits 2 with
  `unrecognized arguments`. Recorded here, not repaired in this package (the row belongs to WP2's surface).

## T057 and later red-first rows
Entries are appended by the row that runs the red reading; this file is the single landing point.
