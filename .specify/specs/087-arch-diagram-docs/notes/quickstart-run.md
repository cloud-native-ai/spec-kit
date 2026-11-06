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

## T067 — US5 (`SC-009`) scenario set, end to end (Part 5, 2026-11-06)

```text
$ /usr/bin/python3 -m pytest tests/integration/test_docs_obligation_scenarios.py -q --no-header -p no:cacheprovider -k "sc003 or sc006 or sc009 or sc010"
4 passed, 17 deselected, 1 warning in 0.37s
exit status = 0

$ /usr/bin/python3 -m pytest tests/integration/test_docs_command_scenarios.py -q --no-header -p no:cacheprovider -k "c018 or c019"
4 passed, 32 deselected, 1 warning in 0.05s
exit status = 0
```

Readings: `test_sc006_two_runs_identical_and_keyed_by_path` (byte-identical runs, path-keyed ordering, every
reason inside the closed table read from the engine, `not-evaluated` never a pass), `test_sc003_reconcile_reports_then_converges`,
`test_sc009_confirm_tiers_and_zones_unchanged` (no `assets/` or `.speckit` artefact triaged as a carrier; the
produce step's writes converge once and stay converged), `test_sc010_unrefreshed_runtime_degrades_visibly`; on the
command side `test_c018_top_level_sequence_unchanged_and_confirm_literal_kept`,
`test_c019_no_new_command_reachable_from_existing_verification_steps` and their two siblings.
**US5 is satisfied independently** — the check is a verdict a machine refuses, a clean space says so explicitly,
an exemption is visible and distinct from a pass, and an unreadable case is never clean.

## T073 — quickstart S1–S9 walked against the landed implementation (Part 5, 2026-11-06)

Every block below is a command this run actually executed in this worktree plus the output it produced.
`$PY` = `/usr/bin/python3` (CPython 3.11.13 / pytest 9.2.0 / typer 0.27.3). Records are named
`docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json` — the file the fixtures **actually carry**
(the planning example `20261106T000000Z-aaaaaaaa-diagram-trace.json` is a shape illustration and is absent on
disk; see § T073.4).

### T073.1 — S1: the checker runs on an existing documentation space

```text
$ $PY skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
exit status = 0
{
  "action": "obligation", "root": "<worktree>", "record": null, "carriers": 85,
  "documents": [ … 85 entries … ],
  "summary": {"satisfied": 0, "missing": 84, "stale": 0, "exempted": 0, "not_evaluated": 1,
              "converged": false, "clean": false, "exemption_superseded": 0}
}
```

S1's expectation was **exit 0 with a `C-013` payload**, and that is what it printed: the action the planning
phase measured as `invalid choice` (exit 2) now judges 85 carriers and maps "not clean" into the payload rather
than the exit code (`C-001`). The single `not-evaluated` row is `docs/tutorials/quickstart.md` (`line` 214,
`no-trace-record`) — the one carrier that references a diagram and has no record, exactly the known-red the
plan's baseline table registers. The other 84 are `missing` / `no-diagram-reference`.

The `validate` baseline is unchanged (3 pre-existing violations, exit 0 — `C-015`):

```text
$ $PY skills/external/create-docs/scripts/docs-utils.py --action validate --root .
exit status = 0
{"violations": [{"kind": "root-entry-oversize", "path": "CHANGELOG.md", …},
                {"kind": "note-frontmatter", "path": "docs/notes/081-acceptance-hardening-final.md", …},
                {"kind": "note-frontmatter", "path": "docs/notes/type-follows-stage-misclassification.md", …}]}
```

### T073.2 — S2: the carrier population

```text
$ $PY - <<'EOF'   (quickstart S2's own census script, unchanged)
concepts/ 12
tutorials/ 2
tasks/ 1
reference/ 64
decisions/ 5
contribute/ 1
ARCHITECTURE.md False
carriers 85
exit status = 0
EOF
```

The recorded population (85, `ARCHITECTURE.md` absent) is reproduced byte for byte, and it equals the
`carriers` field S1 printed. The three readings S2 says must be handled explicitly all hold: `docs/.speckit/`
is absent (`ls -d docs/.speckit` → `No such file or directory`), `docs/assets/` carries
`quickstart-workflow.{png,puml,svg}` and no HTML face, and the repository `docs/` gained no content (T073.7).

### T073.3 — S3: the four negative fixture verdicts

`--record` is resolved **relative to `--root`** (`C-010`'s own convention, `_record_path`), so the argument is
`docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json`, not the repository-relative path S3's block
shows. The two are the same file under a different base; S3's form joins `--root` twice and the engine correctly
refuses it with `exit 2` (`--record` is not readable) — recorded in T073.4 as a quickstart correction.

```text
$ $PY skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/<space> \
      --record docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json --json

clean/           exit 0  satisfied=1 missing=5 stale=0 exempted=0 not_evaluated=0 converged=false clean=false
                 doc: satisfied / reference-resolves (line 5)
orphan-rendered/ exit 0  satisfied=0 missing=6 …              doc: missing / orphan-rendered (line 5)
orphan-source/   exit 0  satisfied=0 missing=6 …              doc: missing / orphan-source (line 5)
stale-source/    exit 0  satisfied=0 missing=5 stale=1 …      doc: stale / source-newer-than-render (line 5)
```

⇒ **The four verdicts match S3's table one for one**, and each names the face it lost (`orphan-rendered` vs
`orphan-source` are not swapped, `C-005`). `stale-source/` was **not** read off the repository copy: its mtime
inequality is a copy-time fact (`conftest.apply_mtime_step`, `T007`), so the reading was taken on a `tmp_path`
copy after that step ran. Repository mtimes for all three faces of `stale-source/` are identical
(`2026-11-06 16:47:21.093121107`) — the inequality exists only where the build step put it, which is why the
repository copy must not be the one judged.

**About the five `no-diagram-reference` rows**: each fixture carries six carriers (one formal document plus the
five typed `index.md` placeholders), so `converged`/`clean` are false in the fixture spaces for the same reason
they are false in this repository — five carriers genuinely carry no diagram. The **per-document** verdict, which
is what S3's table registers, is the one tabulated above. The `_exemptions` family reproduces the same shape
(S5), and the fully-produced space converges (S9).

Exit codes are 0 in all four: red and green live in the payload, never in the exit code (`C-001`, `FR-023`).

### T073.4 — S3 correction disclosed: the fixture record's filename

`quickstart.md` S3 prints `docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json` as a **shape**
example. The fixtures on disk carry `20261106T090000Z-0870a1b2-diagram-trace.json` (`build_fixtures.py`, the
committed builder), and against the printed name S3's commands exit 2 with `--record is not readable`. This is a
**correction**, not a decision: `data-model.md` E6 is the fixture-composition owner and says "本夹具记录", and
`C-010` owns the filename **shape** (`<UTC basic>-<8 hex>-diagram-trace.json`) — value and base both settle one
way. The form used above is that one. The other two corrections are mechanical and are given inline: `--record`
is root-relative, and `stale-source/` must be judged on a copy.

### T073.5 — S4: determinism, idempotence, zero write

```text
$ $PY skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --json > "${TMPDIR}/087-a.json"   → exit 0
$ $PY skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --json > "${TMPDIR}/087-b.json"   → exit 0
$ cmp "${TMPDIR}/087-a.json" "${TMPDIR}/087-b.json" && echo IDENTICAL
IDENTICAL
$ git status --porcelain tests/fixtures/docs-obligation/clean
(empty)                                       ⇒ zero writes
```

Both redirects went outside the worktree, so the empty `git status` measures the checker and not the
redirection (`C-002`, `C-006`).

### T073.6 — S5: exemption visibility and invalidation

```text
$ $PY … --action obligation --root tests/fixtures/docs-obligation/exempt-ok --json
exit 0   doc: recorded-exemption / exempt-chronological   exempted=1 converged=false clean=false

$ $PY … --action obligation --root tests/fixtures/docs-obligation/exempt-bad --json
exit 0   doc: not-evaluated / exemption-invalid           not_evaluated=1 exempted=0 converged=false

$ $PY … --action obligation --root tests/fixtures/docs-obligation/exempt-superseded \
       --record docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json --json
exit 0   doc: not-evaluated / exemption-invalid           exemption_superseded=1 converged=false
```

⇒ The three readings S5 registers on the exemption side all match: a lawful exemption is **visible**
(`exempted=1`, `clean=false` — exemption is not a pass), an invalid one is `not-evaluated`, and an overturned one
is reported through `exemption_superseded` instead of being deleted.

**On `exempt-ok`'s `converged`**: S5's block reads `converged=true` on the repository copy, and the measured
value there is `false` — because the five typed `index.md` carriers of that space genuinely carry no diagram, so
`missing=5` and the `C-013` conjunction is false on its own terms. S5's own expectations are not in conflict
once the produce step is applied: on a copy where those five carriers carry the diagram, the reading is
`exempted=1 converged=true clean=false` (S9's exemption row, T073.9) — the "converged but not clean" state the
quickstart describes. Recorded here rather than silently reconciled, so a later reader can tell which reading
belongs to which state.

### T073.7 — S6: the flow-side guard readings

```text
$ $PY -m pytest "tests/contract/test_confirmation_gates_sweep.py::test_protected_gate_preserved[templates/commands/docs.md-stop-and-confirm]" -q
1 passed, 1 warning in 0.09s                                     exit 0   ← the exact node id, one instance

$ $PY -m pytest tests/contract/test_expression_gate_wiring.py -q -k "a1 or a3 or a5"
5 passed, 11 deselected, 1 warning in 0.09s                      exit 0

$ $PY -m pytest tests/contract/test_docs_command_template.py -q -k "c3 or c4a"
2 passed, 20 deselected, 1 warning in 0.06s                      exit 0

$ $PY -m pytest tests/contract/test_directory_governance.py -q
21 passed, 1 warning in 0.07s                                    exit 0   ← baseline 21, unchanged

$ $PY -m pytest tests/contract/test_expression_compatibility.py -q
16 passed, 1 warning in 0.35s                                    exit 0   ← baseline 16, unchanged

$ $PY -m pytest tests/contract/test_confirmation_gates_sweep.py tests/contract/test_expression_gate_wiring.py \
      tests/contract/test_docs_command_template.py -q --tb=no -rf
FAILED tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
1 failed, 83 passed, 1 warning in 1.86s
```

**No new failures**: the failure name set is exactly the recorded baseline's single name
(`test_residual_total_within_sc002_target`, pre-existing from 085), and every other guard file reproduces its
recorded count. `C5`'s allowlist entry resolves — measured directly against the manifest, not just by the green
suite: `skills/external/improve-docs/SKILL.md` **is** a 74-entry manifest key, its current sha256 differs from
the frozen one (so the entry is load-bearing, not vacuous), and all four markers (`Diagram-sync`,
`skills/external/draw-diagram`, `--action obligation`, `staleness finding`) are literally present in the file.
The guard's own `for rel, allowance in ALLOWED_POST_BASELINE_CHANGES.items()` block asserts exactly those three
conditions, and all 35 allowlist keys resolve to manifest entries.

### T073.8 — S7: the two `--check` commands

```text
$ $PY scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (415 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (16 files)
ok    scripts/ == .specify/scripts/ (121 files)
ok    shared/ == .specify/shared/ (94 files)
exit 0

$ $PY scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
exit 0
```

Six pairs `ok`, both checks exit 0 — **no new drift** relative to the T003 baseline, which is the criterion
(not an absolute exit 0). The `--write` pass this part ran (T068/T069) changed **nothing**: `git status` over
the sources, the `.specify/` mirrors and the four per-tool copies is empty, i.e. Parts 1–4 had already left the
tree at parity and the two generators reproduce it exactly.

### T073.9 — S8: the repository's own `docs/` tree

```text
$ git diff --name-only 24cb4edc...HEAD -- docs/
docs/concepts/documentation-model.md
$ git diff --name-only 24cb4edc...HEAD -- docs/ | wc -l
1
$ git status --porcelain docs/
(empty)
```

**Exactly one line**, the reader projection `FR-001` requires (`T064`); no second path, no uncommitted change.
Cross-checks: `skills/external/draw-diagram/` has **0** changed files (`T-004`) and `templates/commands/` has
exactly one changed file, `docs.md` `(C-019)`.

### T073.10 — S9: the reconcile convergence loop

Run on copies in `${TMPDIR}` (the repository fixtures stay at their registered composition). S9's **criterion is
`converged`**, not `clean` — the two predicates answer different questions (`C-013`).

| Step | Reading |
|------|---------|
| first R6 on a `no-diagram` copy (6 carriers, all without diagrams) | `missing=6`, `converged=false`, `clean=false` — a finding, not a pass |
| R5 produce the diagram for the one formal carrier (two faces + reference + record) | that document → `satisfied` / `reference-resolves`; the five typed `index.md` carriers still `missing` / `no-diagram-reference` ⇒ `converged=false` |
| R5 produce every remaining carrier | `satisfied=6 missing=0 stale=0 not_evaluated=0` ⇒ **`converged=true`, `clean=true`** — second pass zero graph findings |
| anti-churn (tree digest before/after the third R6) | `ZERO-WRITE: tree digest unchanged across the run` |
| exemption row: the same produce step on an `exempt-ok` copy | `exempted=1 converged=true clean=false` — a lawful terminal state, and **not** an unconverged space |

⇒ **`converged=true` on the second pass holds**, exactly as S9 states, and the exempted space converges while
staying unclean — which is the whole reason `converged` and `clean` are two predicates rather than one. The
executable form of the same claim is `I::test_c008a_second_reconcile_zero_findings`,
`I::test_c008a_exemption_does_not_block_convergence` and `I::test_c008a_r3_r4_r5_wiring` — all green (T073.11).

### T073.11 — the `C-008a` wiring readings behind S9

```text
$ $PY -m pytest tests/integration/test_docs_obligation_scenarios.py -q -k "c008a"
2 passed, 19 deselected, 1 warning in 0.17s        exit 0
$ $PY -m pytest tests/unit/test_docs_utils_obligation.py -q -k "c008"
3 passed, 34 deselected, 1 warning in 0.16s        exit 0
```

### T073.12 — the clause's four evidences (`C-022`)

No "complete" conclusion in this file rests on a report missing any of the four. On the fixture spaces they are:

| Evidence | Value |
|----------|-------|
| source path | `docs/assets/widget.mmd` |
| rendered artifact path(s) | `docs/assets/widget.svg`, `docs/assets/widget.png` |
| the document reference | `docs/concepts/widget-overview.md` line 5 → `../assets/widget.svg` |
| the trace-record path | `docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json` |

On **this repository** the four are: `docs/assets/quickstart-workflow.puml`; `docs/assets/quickstart-workflow.png`
and `.svg`; `docs/tutorials/quickstart.md` line 214; and **none** — no trace record exists, which is why S1
reads that document `not-evaluated` / `no-trace-record` and why the conclusion drawn here is "the obligation is
enforced", never "this repository's documentation space is diagram-complete".
