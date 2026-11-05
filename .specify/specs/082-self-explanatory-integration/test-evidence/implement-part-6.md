# Implement part 6 — T029-T033 (US3: the documents reach a client project)

- **stage**: implement
- **part**: 6/10
- **part_scope**: T029-T033
- **stage_base**: `02fd6db5`
- **test_budget**: targeted-set-v1 (E2's single full suite from part 1 stands unchanged: 26 failed /
  7156 passed / 1 skipped; no second full suite is run here)
- **docs-only**: no; this part adds one test module and three framework documents

## E3 stage-status row (implement part 6)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T029-T033 |
| status | us3-distribution-green-and-mutation-legs-proven |
| command | `python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q` then `python3 scripts/python/sync-mirrors.py --check` then three `cmp` calls |
| selection_basis | targeted-set-v1 — exactly the pair the dispatch brief names: the new distribution module (whose subject this part creates) and the mirror engine (whose enumeration T031 owns), plus the three pairwise `cmp` calls T032 names verbatim |
| selected_paths | `tests/contract/test_self_explanatory_distribution.py` (new), `shared/definitions/self-explanatory-definitions.md`, `shared/guidelines/self-explanatory.md`, `shared/workflow/best-practice-optimization.md` (new sources), `scripts/python/sync-mirrors.py` (read-only, invoked) |
| sufficiency | the new module and the mirror engine are the only two guards that judge this part's surfaces. The three documents are plain prose with no other carrier; the parity suite (`test_mirror_parity_suite.py`) derives its parameters from `MIRROR_PAIRS` and therefore picked the three new sources up without an edit — it is the companion set below. Sufficiency is claimed for **the edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run |
| rc | 0 (module), 0 (engine `--check`), 0/0/0 (`cmp` ×3) |
| passed / failed | 4 passed / 0 failed in the new module; 3 `ok` pairs + `OK:` line from the engine |
| new_failures | none in the selected set |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries) — no comparison triggered, since nothing in the selected set is a baseline failure |
| evidence_ptr | `notes/pre-change-measurements.md` § Part 6 (T031/T032/T033 transcripts + the count derivation), `notes/quickstart-run.md` § Part 6 (T029 `init` run, T032 `cmp`), `notes/red-first-evidence.md` § R-2 (red/green pairs) |

### Command output, verbatim

```console
$ python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q
....                                                                     [100%]
4 passed in 6.86s
EXIT=0

$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0

$ cmp shared/definitions/self-explanatory-definitions.md .specify/shared/definitions/self-explanatory-definitions.md ; echo rc=$?
rc=0
$ cmp shared/guidelines/self-explanatory.md .specify/shared/guidelines/self-explanatory.md ; echo rc=$?
rc=0
$ cmp shared/workflow/best-practice-optimization.md .specify/shared/workflow/best-practice-optimization.md ; echo rc=$?
rc=0
```

### Companion set — the parity suite picks the three new sources up on its own

`test_mirror_parity_suite.py` derives one parameter per **source** file from the engine's
`MIRROR_PAIRS`, so C-22's three new parameters exist without editing that suite (the contract's own
requirement: "MUST NOT introduce a second table of pairs"). Running it confirms the derivation
reached the new files rather than silently missing them:

```console
$ python3 -m pytest tests/contract/test_mirror_parity_suite.py -q \
      -k "self_explanatory or self-explanatory or best-practice-optimization"
...                                                                      [100%]
3 passed, 759 deselected in 0.09s
EXIT=0

$ # the three derived node ids, collected:
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[shared/definitions/self-explanatory-definitions.md->.specify/shared/definitions/self-explanatory-definitions.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[shared/guidelines/self-explanatory.md->.specify/shared/guidelines/self-explanatory.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[shared/workflow/best-practice-optimization.md->.specify/shared/workflow/best-practice-optimization.md]
```

Exactly three parameters matched, and each node id names its own `source->mirror` pair — C-24's
re-runnability requirement, satisfied by construction rather than by an assertion this part wrote.

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion lives | State after this part |
|-----|--------|---------------------------|-----------------------|
| T029 | C-26 | `tests/contract/test_self_explanatory_distribution.py`: a module-scoped fixture builds a temp venv + `pip install -e <repo>`, runs `specify init --here --ai claude --no-git --skip-tls --ignore-agent-tools` in a temp project, and asserts each of the three `.specify/shared/…` paths present and non-empty; a second test asserts the entry point's resource root carries all three; a third is the anti-vacuity companion | green, 4 passed; red proven by removal (2 failed naming the removed document) |
| T030 | C-28 | `git add` of the three sources; `git status --short -- shared/` shows exactly three `A` and no mirror entry | green — three `A`, mirrors still `??` until T031 |
| T031 | C-23 | `sync-mirrors.py --write --only shared` then `--check` → exit 0; the engine also proven to actually copy these files (DIFF → `sync … (1 files)` → byte-identical) | green at 65 files |
| T032 | C-22 | three `cmp` calls, all `rc=0`; plus a `filecmp.cmp(shallow=False)` sweep of the whole pair: `missing=[] extra=[] differing=[]` | green |
| T033 | C-28 | resource root resolved from the working tree, the three files present under its `shared/`, and the copy section read verbatim to confirm it walks that root with no new logic | green — recomputation commands recorded in `notes/pre-change-measurements.md` |

## The 65-vs-68 reading (open, raised rather than repaired)

T031's task text says "实测基线 65 文件,本阶段后应为 68". Measured: 65 before and 65 after.

The three documents **are** mirrored and byte-identical, so no mirror file is missing. The figure is
explained by the stage's own records: research.md B-7 measured `ok … (65 files)` at the *start* of the
plan stage, when `shared/` held 62 tracked files — so 65 was never the pre-feature baseline the
subtraction `65 + 3 = 68` assumes. Re-derived independently:

| quantity | command | value |
|----------|---------|-------|
| `shared/` at HEAD | `git ls-tree -r --name-only HEAD shared \| wc -l` | 62 |
| new sources staged by this part | `git diff --cached --name-only -- shared \| wc -l` | 3 |
| `shared/` now | `find shared -type f \| wc -l` | 65 |
| `.specify/shared/` now | `find .specify/shared -type f \| wc -l` | 65 |

Why this is not repaired in passing: two readings remain open — (a) the plan-stage readings describe a
tree state this checkout no longer has (B-7 itself records the three files were created outside that
run's reach), or (b) the engine enumerates files differently from `find` in a way this run has not
isolated. Choosing between them needs either an artifact this feature does not own or a judgement
about engine semantics — a **decision**, not a correction — so it is raised in the part return and the
state spine instead of being written down as settled.

What is *not* in doubt, and is asserted above: the pair is complete, the three files are byte-identical
on both sides, `--check` exits 0, and the same 65 files reach a client project through `specify init`.

## In-passing repairs (corrections, disclosed)

1. **Layer 3 skipped instead of judging.** The first version of
   `test_c26_entry_point_resource_root_carries_the_three_documents` reported
   `ANOMALY: … ships no templates/` whenever the resource root was not `MODULE_DIR`. The measured
   editable-install layout is `MODULE_DIR.parent.parent` (the repo root) because the build's
   force-include materialises `src/specify_cli/{templates,shared,…}` as a **sibling** of the module
   dir. One reading is consistent with `get_resource_path`'s own docstring, so this is a correction:
   both layouts are now named and accepted, a third value still fails, and the strongest layer is
   judged on this host instead of being silently skipped.
2. **By-path `importlib` loading does not work for `specify_cli`.** `src/specify_cli/__init__.py`
   imports `from . import _provenance`, so `spec_from_file_location` raises `ModuleNotFoundError`
   (observed: the module failed at collection). Switched to the `sys.path` + plain-import idiom
   already used by `test_capability_matrix_contract.py` / `test_upgrade_end_state.py`, with an
   assertion that the imported package really came from this working tree.
3. **`--ignore-agent-tools` added to T029's `init` invocation.** The three brief-mandated flags are
   all present; this fourth is required because the host has no `claude` agent CLI and `init` aborts
   on that check before reaching the copy step. Recorded in `notes/quickstart-run.md`.

No guard was weakened to make a step green: the removal leg and the anti-vacuity companion both show
that the module goes red on its own subject, and the mirror engine's write path was exercised rather
than assumed.

## Out of scope, verified not done

- T034+ not started: no docs link guard, no `docs/concepts/self-explanatory.md` work (T035/T036), no
  M-5/M-6 legs, no US4 rows.
- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` unmodified (`PLAN-EDIT: none`).
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
