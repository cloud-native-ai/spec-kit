# quickstart-run.md — the executed scenario record

Owner of the *procedure* each block replays: `quickstart.md` (S1–S9). This file holds only what a run actually
printed: the command line, the exit status and the output. A block is appended by the task row that runs it; a
row that only reads text records the reading, not a command it never ran.

Interpreter for every block: `/usr/bin/python3` — CPython 3.11.13 / pytest 9.2.0 / typer 0.27.3 (the one that can
`import typer`, per `plan.md` § Mirror Obligations; the bare-`python3` false red is recorded in
`notes/pre-change-measurements.md`).

## T055 — US1 (`SC-001`) authoring flow, end to end (Part 4, 2026-11-06)

```text
$ /usr/bin/python3 -m pytest tests/integration/test_docs_obligation_scenarios.py -q --no-header -p no:cacheprovider -k "sc001 or sc002 or sc008"
3 passed, 18 deselected, 1 warning in 0.37s
exit status = 0

$ /usr/bin/python3 -m pytest tests/integration/test_docs_command_scenarios.py -q --no-header -p no:cacheprovider -k "c010 or c015 or c016 or c017"
4 passed, 32 deselected, 1 warning in 0.04s
exit status = 0
```

Readings: `test_sc001_four_artifacts_present` (the four on-disk artifacts, with the trace record asserted
separately rather than counted as a fifth), `test_sc002_removing_either_face_turns_red` (each of the three faces
disturbed on its own copy, each turning red under its own name), `test_sc008_exemption_visible_and_superseded`
(visible, converges while staying unclean, and an overturned exemption reported rather than deleted); on the
command side the four authoring readings (`c010` the tier table, `c015` R2's plan, `c016` R5's four artifacts,
`c017` R6's separate faces). **US1 is satisfied independently** — one commission yields all four artifacts plus
the record, and deleting either diagram face turns the flow's own verdict red naming that face.

## T059 — US3 (`SC-004`) rename scenario, end to end (Part 4, 2026-11-06)

```text
$ /usr/bin/python3 -m pytest tests/integration/test_docs_obligation_scenarios.py -q --no-header -p no:cacheprovider -k "sc004"
1 passed, 20 deselected, 1 warning in 0.21s
exit status = 0

$ /usr/bin/python3 -m pytest tests/integration/test_docs_command_scenarios.py -q --no-header -p no:cacheprovider -k "c011 or c012 or c013 or c014 or c023"
6 passed, 30 deselected, 1 warning in 0.04s
exit status = 0
```

**The rename fixture's before/after readings** (`test_sc004_rename_keeps_document_and_diagram_in_step`, all on
`tmp_path` copies of `clean/` — the repository copies stay at their registered pre-state):

| Step | Document bytes | Diagram-source bytes | Verdict / reason |
|------|----------------|----------------------|------------------|
| before | `…reaches the store.` (unchanged) | `… B --> C[Widget store]` (unchanged) | `satisfied` / `reference-resolves` |
| prose + source renamed, no re-render | `…reaches the repository.` | `… B --> C[Widget repository]` | `stale` / `source-newer-than-render` |
| after the re-render | unchanged since step 2 | unchanged since step 2 (mtimes refreshed, digest re-recorded) | `satisfied` / `reference-resolves` |
| prose only | `…reaches the repository.` | **byte-identical to before** | `satisfied` / `reference-resolves` — the recorded `D-001` boundary |
| source only, no re-render | unchanged | `… C[Widget repository]`, mtime pushed past every face | `stale` / `source-newer-than-render` |

⇒ The pair moves together or the run says so. The prose-only row is the honest one: the semantic half of
`stale` is uncovered by design (`D-001`), so a rename applied to the prose alone is NOT mechanically visible —
and the assertion pins the other thing that row must never do, silently re-rendering the diagram, because that
would destroy the only on-disk evidence that the two disagree. The source-only row is what an improve run must
turn into a named staleness finding instead of a rollback.

On the command side the six readings are the five `improve-docs` legs (`c011` evidence step, `c012` the
Diagram-sync row, `c013` minimal edit, `c014` verify, plus their sibling `c023` face names) and
`test_c002_improve_docs_reaches_the_capability_by_path_only`. **US3 is satisfied independently.**
