# Implement — WP-05 (T061–T077)

- **Unit**: `/speckit.implement` · **run-id**: `r20261112T064607Z-b101`
- **Feature**: `101-anchor-goal-realignment` · **Stage/package**: implement / WP-05 (T061–T077)
- **Base commit**: `570622221` (checkpoint 17, WP-04 complete)
- **Verdict**: **tasks executed and evidenced; FR-067 / SC-001 unmet** — the live residue scan still reads
  C1 = 2 and C4 = 1, both outside this package's write territory. Reported as anomalies, guards not weakened.

## 1. Guard modules delivered

| Guard | Task | Module | Tests |
|---|---|---|---|
| G-1 | T062 | `tests/contract/test_anchor_command_surface.py` | 9 (3 injections) |
| G-2 | T063 | `tests/contract/test_goal_command_surface.py` | 8 (2 injections, real-subprocess refusals) |
| G-3 | T064 | `tests/contract/test_anchor_definitions.py` | 5 (1 injection + fixture-defect proof) |
| G-4 | T065 | `tests/contract/test_goal_store_write_boundary.py` | 9 (2 injections, 2 two-writer simulations) |
| G-5 | T066 | `tests/contract/test_binding_rename.py` | 6 (1 injection + fixture-defect proof) |
| G-6 | T067 | `tests/contract/test_live_semantic_residue.py` | 7 (corpus, determinism, injection) |
| G-7a | T068 | `tests/contract/test_cleanup_idempotency.py` | 5 (3 injections) |
| G-7b | T069 | `tests/contract/test_cleanup_resume.py` | 3 (phase faults + I5 half-state) |
| G-8 | T070 | `tests/integration/test_101_protected_paths.py` | 3 (entry baseline + fixture injection) |
| G-9 | T071 | `tests/integration/test_101_convergence.py` | 1 (scratch fixture, real apply) |
| G-10 | T072 | `tests/contract/test_command_family_101.py` | 7 (3 injections, live command-family reads) |

Fixtures: `tests/fixtures/anchor-goal-realignment/` (`pre-convergence/` 20 teams, `classification/`,
`residue-corpus/`, `protected-paths/`). Guard files were built red-first: each guard was run against a
broken scratch subject (`SPECKIT_GUARD_ROOT` + isolated `git init` for G-8) and observed failing before the
tree satisfied it — table in `notes/red-first-evidence.md` § WP-05, raw runs in
`test-evidence/wp05-redfirst-g{1,2,3,5,6,8,9,10}.txt`.

## 2. Commands executed (rc + artifact)

| # | Command | rc | Artifact |
|---|---------|----|----------|
| G-1…G-10, base reds | `bash scripts/bash/run-tests.sh <11 guard modules + test_goal_writeset.py + test_summary_writeset.py> -q` | 1 | `implement-wp05-targeted-tests.txt` — **110 passed, 1 failed** (the residue test), no other failure |
| earlier subset | same six new modules before base-red alignment | 1 | `implement-wp05-targeted-tests-run1.txt` — 25 passed, 1 failed |
| T073 | `hugo --source docs --renderToMemory` (hugo v0.141.0 extended) | 1 | `docs-build-2026-11-12.txt` — `.Site.Language.Locale` error; limb `not-evaluated` (EP-006) |
| T075 | live G-6 `scan_tree` reading | 1 | `residue-scan-2026-11-12.txt` — C1 2, C4 1, rest 0 |
| T075/S-5 | `goal-utils.py cleanup --check --classification … --json` | 0 | `cleanup-check-wp05-2026-11-12.json` (14 ≥ decisions, all `noop`) |
| T076 | S-0…S-8 walk, engine + git readings | mixed | `notes/quickstart-run.md` |
| T077 | this index | — | `guard-readings-2026-11-12.md` |

## 3. Executed tasks and readings

- **T061** fixtures: pre-convergence tree with 20 teams (bound/unbound/archived classes), classification,
  retired corpus (each C1–C7 class matchable), protected-paths tree — all consumed by the guards above.
- **T062–T066** G-1…G-5: anchor surface, goal refusal, store purity, single-writer audit, binding rename —
  each green on the live tree and red on a broken subject.
- **T067** G-6: module shipped with the declared-class compile check and injection; live reading **fails**
  (§4).
- **T068–T069** G-7a/b: idempotency (second apply byte-identical, no new receipt), resume phases
  (`write-receipt` → `remove-source`), receipt-less target is rc 4 `half-state` and never silently repaired.
- **T070** G-8: entry baseline (4550 rows; 0 deleted, 1 pre-existing `smoke-081.txt` change disclosed in the
  artifact, not waived); close-out reading 0 changed / 0 deleted; additions bucketed, `.specify/archive/
  anchoring/` listed separately.
- **T071** G-9: fixture converges (10 anchors, 0 `goal.md`, 0 `goal_slug`, every binding resolves).
- **T072** G-10: both ledger rows, seven-mode reference page, layer-shaped `command-family` answer.
- **T073** docs build: `not-evaluated` on the build limb with the verbatim hugo error; other limbs measured
  by G-10/T040.
- **T074** reader restatement: four entries (Anchor / anchoring archive / Re-Anchoring / action-level Goal)
  restated from glossary + owners; all agree.
- **T075** residue: see §4.
- **T076** quickstart: S-0 deviates (stale plan-time text), S-1…S-6 pass or bounded, S-7 pass, S-8 fails
  (§4). Live readings and fixture drills kept apart.
- **T077** guard index: one row per FR-062…FR-071 with evidence path and result.

## 4. Unmet criterion (fast-fail: out-of-territory source defects)

FR-067 / SC-001 require every declared residue class to read 0 on the live tree. Live reading:

| Class | Baseline | Now | Offenders |
|---|---|---|---|
| C1 | 4 | **2** | `shared/definitions/derivation-definitions.md:414` + `.specify/shared/` mirror — `| **Goal** | Project-level authored end state…` |
| C4 | 16 | **1** | `.specify/memory/tools/build-summary-input.py.md:35` — stale `--out` default `.specify/goal/<goal-slug>/summary/…` |
| C2 / C3 / C5 / C6 / C7 | 0 / 8 / 16 / 40 / 3 | 0 / 0 / 0 / 0 / 0 | — |

Both offenders sit outside WP-05's write territory (`tests/**`, fixtures, this spec's evidence,
`notes/quickstart-run.md`); one is a framework-source definition table that the installed mirror copies, so
a mirror-only edit would break the mirror rule. No guard was weakened, no root/exclusion widened
(`research.md` and the guard module are unchanged since `570622221`). Routed: C1 → owner of
`derivation-definitions.md`; C4 → the Tool-record owner (`/speckit.tools`). This is a decision for the
stage owner, hence the `ANOMALY:` report rather than an in-passing repair.

## 5. Base-red alignment (test-side only)

`tests/contract/test_goal_writeset.py` pinned the 037-era definition filename `goal.md`; the rewritten
`skills/internal/create-team/references/summary-mapping.md` now names `anchor.md` with the same prohibition
("MUST 保持字节不变 … 写入面违规"). The source is correct under the new contract, so only the test
expectation moved (`REQUIRED_GROUPS`, the regex, docstrings). Before: 2 failed / 46 passed; after:
48 passed. WP-03 source untouched.

## 6. Disclosed observations (not criteria)

- `--scope goal list` (quickstart S-0) exits 2 — the scope set is the closed four members; the quickstart
  text is plan-time and stale (owner: `quickstart.md`).
- Wrapper wording: `anchor --mode status` reports "Anchor-only mode" while refusing `goal-only-mode`;
  `targets --check` on a terminal anchor prints "终态 goal 只读" (says *goal*). Wording only; behaviour is
  the intended one.
- `goal_slug` raw-grep hits on live roots are confined to dated `runs/**`, receipt `before` fields, generated
  `project-input.yaml`, the create-team scripts' declared legacy tolerance, and the `handoff/v1` contract key
  (owner: `create-team` skill). No residue class covers them; recorded, not edited.
- 12 live `team.md` files carry `.specify/goal/**` inside `forbidden_paths` — a write prohibition, not a
  binding or definition ref. C1–C7 do not cover prohibition fields (C5 is scoped to anchor definitions, C6
  to command-mode pointers), so it is classified as a stale address in a prohibition field, owner = the
  team-definition surface; recorded in `notes/quickstart-run.md` § S-6, not edited (team definitions are
  outside this package's territory).

## 7. Wrap-up engines

All three ran on `(skill:implement-feature, r20261112T064607Z-b101)` — the spine's run id — and each
reported **duplicate** for this (unit, run), so no second row was written (duplicates count as satisfied):

| Engine | Reading | Evidence |
|---|---|---|
| `run-determination.py --action determine` | rc 0, `duplicate: true` — "this (unit_id, run_id) was already determined" | `test-evidence/wrap-up-determine-2026-11-12.json` |
| `exec-quant.py --action collect` | rc 0, `duplicate record … no second row written` | `test-evidence/wrap-up-execquant-2026-11-12.json` |
| `feedback-utils.py --action record` | rc 0, `id 20261112T121643Z-skill-implement-feature`, `duplicate: true`, `count_since_submission` 483, `should_prompt` true | `test-evidence/wrap-up-feedback-2026-11-12.json` |

One correction disclosed: the first `exec-quant collect` used a mistyped run id (`r20261212…`) and wrote a
record; the record was removed immediately (`20261112T130334648828Z-1047c95e.json`, unlinked) and the engine
re-run with the spine id, which returned the duplicate above.
