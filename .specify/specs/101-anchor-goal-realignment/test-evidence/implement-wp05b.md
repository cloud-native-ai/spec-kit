# Implement — WP-05b (live-residue correction: C1 / C4)

- **Unit**: `/speckit.implement` (`skill:implement-feature`) · **run-id**: `r20261112T064607Z-b101`
- **Feature**: `101-anchor-goal-realignment` · **Stage/package**: implement / WP-05b
- **Base commit**: `8677a32b4` (checkpoint 18)
- **Category quartet**: `flow_class=execution; source=declaration; marker=; error=-`
- **Verdict**: both live-surface corrections applied; live-residue guard green on every class; no guard or
  out-of-territory file touched.

## 1. Corrections

| Class | File | Before | After |
|---|---|---|---|
| C1 | `shared/definitions/derivation-definitions.md:414` | `| **Goal** | Project-level authored end state, measured by degree — a different plane entirely | goal-definitions.md |` | `| **Anchor** | Project-level authored end state, measured by degree — a different plane entirely | anchor-definitions.md |` |
| C4 | `.specify/memory/tools/build-summary-input.py.md:35` | default `--out` = `.specify/goal/<goal-slug>/summary/data/project-input.yaml` | default `--out` = `.specify/anchoring/<slug>/summary/data/project-input.yaml` |

C4 basis: the engine's declared default is `repo_root / ".specify/anchoring" / goal_slug / "summary"`
(`skills/internal/create-team/scripts/build-summary-input.py` — `ARCHIVE_DIRNAME = ".specify/anchoring"`,
`delivery_dir = repo_root / ARCHIVE_DIRNAME / goal_slug / "summary"`, `--out` help text
`<delivery_dir>/data/project-input.yaml`). The tool record is a live behavior authority, so it was aligned
to the engine rather than the engine to the record.

C1 mirror: `shared/` is the source; the `.specify/shared/` copy was refreshed only through
`python3 scripts/python/sync-mirrors.py --write` and then verified with `--check`.

## 2. Guard readings

| Reading | Command | Result |
|---|---|---|
| Live-semantic residue module | `bash scripts/bash/run-tests.sh tests/contract/test_live_semantic_residue.py -q` | **rc 0, 7 passed** (`implement-wp05b-live-residue.txt`) |
| Live class counts (G-6 `scan_tree`) | in-process reading of the guard module | `C1 0, C2 0, C3 0, C4 0, C5 0, C6 0, C7 0` — **total 0** |
| Guard set + writeset base reds | same 13-module command as WP-05 | **rc 0, 111 passed** (`implement-wp05b-targeted-tests.txt`) — the prior 110 passed + the closed live-residue test |
| Mirror identity | `python3 scripts/python/sync-mirrors.py --check`; `cmp shared/... .specify/shared/...` | **rc 0**, `shared/ == .specify/shared/ (114 files, byte-identical)`, `MIRROR-IDENTICAL` |

Module set for the 111-pass reading (identical to WP-05's): G-1 `test_anchor_command_surface`, G-2
`test_goal_command_surface`, G-3 `test_anchor_definitions`, G-4 `test_goal_store_write_boundary`, G-5
`test_binding_rename`, G-6 `test_live_semantic_residue`, G-7a `test_cleanup_idempotency`, G-7b
`test_cleanup_resume`, G-10 `test_command_family_101`, G-8 `test_101_protected_paths`, G-9
`test_101_convergence`, plus base reds `test_goal_writeset` and `test_summary_writeset`. No second full
suite was run.

## 3. Wrap-up engines

All three ran on `(skill:implement-feature, r20261112T064607Z-b101)` and each reported **duplicate** for
this (unit, run), so no second row was written (duplicates count as satisfied):

| Engine | Reading | Evidence |
|---|---|---|
| `run-determination.py --action determine --complexity complex --json` | rc 0, `duplicate: true` — "this (unit_id, run_id) was already determined" (a `--complexity simple` probe returns `skipped: simple-unit` and writes nothing) | `test-evidence/wrap-up-determine-wp05b-2026-11-12.json` |
| `exec-quant.py --action collect --unit-type skill` | rc 0, `duplicate record for (skill:implement-feature, r20261112T064607Z-b101); no second row written` | `test-evidence/wrap-up-execquant-wp05b-2026-11-12.json` |
| `feedback-utils.py --action record --unit-type skill` | rc 0, `id 20261112T121643Z-skill-implement-feature`, `duplicate: true`, `count_since_submission` 483, `should_prompt` true | `test-evidence/wrap-up-feedback-wp05b-2026-11-12.json` |

## 4. Disclosed observations (not corrections, no edit)

- Pre-existing dirty files were left untouched and are not part of this commit:
  `M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` (the WP-05-disclosed
  pre-existing change) and untracked `.specify/.specify/`.
- The same tool record's `Source Identifier` still reads `skills/create-team/scripts/build-summary-input.py`;
  the real path is `skills/internal/create-team/scripts/build-summary-input.py` (no `skills/create-team`
  directory exists). No residue class covers this field and the WP-05b authority names only the default
  path, so this was recorded rather than edited — owner: the Tool-record surface.
- The 12 live `team.md` files carrying `.specify/goal/**` in `forbidden_paths` remain the classified
  prohibition-field residual; unchanged, as ruled at checkpoint 18.

## 5. Fast-fail line

Both changes are **corrections**: each has exactly one reading consistent with the recorded intent
(the new Anchor = project-level model; the engine's actual anchoring default), each is local and
reversible, and neither contradicts a downstream premise. No guard, guard root, exclusion, dated record,
team definition, source engine, or out-of-territory file was modified.
