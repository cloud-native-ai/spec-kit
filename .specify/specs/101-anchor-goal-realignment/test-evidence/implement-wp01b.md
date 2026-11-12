# Implementation evidence — WP-01b (T016–T025)

Run `r20261112T064607Z-b101`, feature `101-anchor-goal-realignment`, package WP-01b,
executor `/speckit.implement` (SDD Implement Executor). Constitution v1.20.0; stage
`implement`; previous package commit `1b417678a`. State spine
`.specify/state/101-anchor-goal-realignment.md` read, never written.

E2 baseline (not re-run): `test-evidence/suite-baseline-entry.txt` — rc=1, 8900 passed,
192 pre-existing failure ids, 3 skipped. Every test command below went through
`bash scripts/bash/run-tests.sh`; no bare test CLI and no `-m` module entry was used.

## T016 — cleanup phase machine remainder

`scripts/python/goal-utils.py` only. The classification-driven `cleanup` action now carries
the whole phase machine (`read → project → write-target → write-receipt → remove-source`),
team structural rename (one line per file, receipt per line), team-body term normalization,
R1/R2/R3 dispositions, the derived `summary/**` move at action time, and the closing
self-checks. Drills were run against clones under `.specify/.tmp/cleanup-drill*`
(removed at wrap-up); the live tree was never written.

- `cleanup --check` on a clone: rc 0, zero writes.
- `cleanup --apply --classification <clone>/classification.json`: rc 0, receipt per changed
  definition, `--check` afterwards reads clean.
- A second `--apply` is a noop and writes no byte.

## T017 — existing actions adapted to the new layer and `anchor_slug`

`scripts/python/goal-utils.py`:
- `list` dispatches by layer (`--scope goals` → action-level store; `--scope teams` →
  `scope-not-applicable`).
- `validate` / `binding` / `targets` / `run-checks` / `handoff-decision` / `handoff-ref` /
  `probe-residual` keep their semantics and resolve `anchor.md` (FR-029).
- `run-checks` emits `anchor_slug`; `goal_slug` is no longer a top-level payload key.
- Eight engine hints now point `/speckit.goal` → `/speckit.anchor` for
  `targets` / `migrate` / `migrate-archive` / `coordinate`.
- Team-side binding reads accept `anchor_slug` and the legacy `goal_slug` (dual key,
  FR-029 transitional fallback).

Reading: `bash scripts/bash/run-tests.sh tests/contract/test_run_checks.py -q` — the
fixture-driven cases pass after T025; see the red-first record for the remaining three.

## T018 — command-family per layer, plus `command-mode`

`command-family` answers per layer (`layers` object: anchor / goals / teams), not one
boolean. New read-only `command-mode --command <anchor|goal> --mode <mode>`:
- mode sets derived only from the canonical `templates/commands/{anchor,goal}.md`
  `argument-hint` (no second list); template absent → `template-missing`;
- `--command goal` on the four Goal modes → exit 0; the four Anchor-only modes → exit 2
  with stderr containing the literal `anchor-only-mode` and `/speckit.anchor`;
- `--command anchor` on the seven Anchor modes → exit 0; unknown mode → exit 2
  `unknown-mode`; zero writes throughout.

Readings (post-split fixture, checked at the cutoff): Goal modes `create` / `view` /
`modify` / `status` → 0; `targets` / `migrate` / `migrate-archive` / `coordinate` → 2 with
both stderr literals; Anchor modes `create` / `view` / `modify` / `targets` / `migrate` /
`migrate-archive` / `coordinate` → 0.

**Adjudication recorded here**: the `command-mode` mode sets are read from the templates,
so until WP-02 authors `templates/commands/anchor.md` (T026) the anchor side answers
`template-missing`. That is the declared behavior, not a defect; the four Goal-side
rejections against `templates/commands/goal.md` were verified live.

**Adjudication recorded here**: the "migrate one existing consumer to the new `layers`
shape" clause of T018 lands in T043's territory (`skills/internal/create-team/**`). No
consumer inside this package's write set reads `command-family`, so this package only
emits the new shape; the consumer migration stays with T043 and is not left half-done in
the engine.

Also fixed for T016/T018 coverage: the engine docstring action table lacked rows for the
`goal-create` / `goal-modify` / `goal-status` / `cleanup` write actions the parser already
declares. The rows were added (mode taken from each action's own argparse help) and the
write-surface module's pinned set grew to match; `tests/contract/test_no_spec_local_writes.py`
is green.

## T019 — `migrate` derives an Anchor

`migrate <team-slug>` derives an **Anchor** definition (`.specify/anchoring/<slug>/anchor.md`)
from the team's inline goal, rewrites the team's `goal_slug:` to `anchor_slug:`, and stops
when the target exists with a non-equivalent concept payload:

- happy path: rc 0, `anchoring/alpha-team/anchor.md` created, team carries `anchor_slug:`.
- equivalent target: rc 0, `definition-untouched: yes`, legacy `goal_slug:` renamed.
- non-equivalent target: rc 4, error names candidate A (existing target with its objective
  / criteria count / status) and candidate B (the team's derived objective / criteria
  count); `zero-writes: yes`; neither is chosen (FR-045 / C-43).

## T020 — script interface contract

`-h` / `--help` / `--version` → rc 0, `help/version zero-side-effect: yes`; an undeclared
option → rc 2; `--scope goal` → rc 2; every new declared option (`--classification`,
`--guidance`, `--done`, `--clear-done`, `--command`, `--mode`) is in the signature guard.

Reading: `bash scripts/bash/run-tests.sh tests/contract/test_script_interface_contract.py -q`
— the three mirror-projection cases are green after T024; the one remaining red
(`test_c26_generator_skill_carries_the_mandate_entry`) is an E2-baseline failure.

## T021 — workflow consumers

- `scripts/python/sdd-route.py`: `--scope` choices `("anchor", "goals", "teams", "auto")`,
  help distinguishes the anchor side from the action-level Goal side.
- `scripts/python/concurrency-check.py`: layout probe reads `anchor.md` with `goal.md`
  fallback (FR-029).

Reading: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_routing_engine.py
tests/contract/test_sdd_routing_definitions.py tests/contract/test_concurrency_high_order.py
-q` → 44 passed. Retired `--scope goal` is refused by the parser (rc 2); the golden call
is rc 0.

## T022 — skill-script consumers

- Both `logical-framework.py` copies (project-setup and house-keeping): `check_goals`
  inspects `.specify/anchoring/`, resolves `anchor.md` with the `goal.md` fallback, and the
  report key is `anchors`; the two copies stay byte-identical apart from the three
  provenance lines and `_SIG_SCRIPT`.
- `skills/internal/create-team/scripts/build-summary-input.py`: summary input path
  `.specify/anchoring/<anchor-slug>/summary/`; binding key `anchor_slug` (with the
  `goal_slug` fallback); dangling check names `anchor_slug` and `anchor.md`.

Readings: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_house_keeping_skill.py
tests/contract/test_sdd_project_setup_skill.py -q` → 31 passed (the two copies stay in
parity). Live `logical-framework.py --project .` → `[recommended] anchors ok 14 anchors:
085-…` (the `required gaps: features` verdict is a pre-existing registry reading,
unrelated to this package).

## T023 — CLI static pointers

`src/specify_cli/__init__.py`: `MIGRATE_STATIC_POINTERS` `ownerCommand` is
`/speckit.anchor`; the note states `/speckit.goal` carries action-level guidance only and
no `migrate-archive` mode; pointer text and the optional command list updated.

Reading: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_us1_converge.py -q`
→ 6 passed.

## T024 — mirror sync and drift check

`python3 scripts/python/sync-mirrors.py --write` then `--check`: **rc 0**, every row
`ok` / byte-identical (shared 114 files, skills 137, agents 20, scripts 129). The five
pairs named by the task are byte-identical:
`shared/definitions/anchor-definitions.md`, `shared/definitions/goal-definitions.md`,
`scripts/python/goal-utils.py`, `scripts/python/sdd-route.py`,
`scripts/python/concurrency-check.py`.

The `--write` / `--check` output was appended to this file after the last engine edit
(the docstring action-table repair); `--check` ends at rc 0.

## T025 — existing tests updated, no cross-package red

Full record, per module and per failure id: `notes/red-first-evidence.md` § WP-01b.
Red-before capture: `test-evidence/wp01b-red-before.txt` (rc=1, 56 failed, 293 passed,
1 skipped). Final targeted reading over 22 modules:

```text
bash scripts/bash/run-tests.sh <22 modules> -q
429 passed, 6 failed, 2 skipped, rc=1
```

The 6 remaining: three E2-baseline pre-existing failures (unchanged) and three live-tree
cases that turn green only after the real definitions migrate in T049–T054. No
rename-caused red remains in this package's reach.

Two test-side repairs worth naming:
- `test_binding_model.py`'s owner tests moved from the Goal owner to the Anchor owner
  (`### Archive Layers` / `### The Binding Record` / `### Lifecycle`), and the cross-citation
  assertion accepts either owner path for the team model's binding-record citation, which
  is stale until T043 re-points it.
- `test_no_spec_local_writes.py` pinned write set grew by the four write actions the parser
  already declared (see T018 above).

## Disclosed deviations / absences

- T005's measurement file `notes/pre-change-measurements.md` **does not exist** in the
  tree. The red-before set was therefore taken from the WP-01a evidence's own 14-module
  command (`test-evidence/wp01b-red-before.txt`), and three further rename-hit modules
  were found by search and closed in-package (`test_goal_targets_check.py`,
  `test_handoff_contract.py`, `test_no_spec_local_writes.py`).
- T018's consumer migration to the `layers` shape is deferred to T043 (territory bound).
- The live `.specify/` definitions were not migrated by this package; that is T049–T054.

## Wrap-up engine readings

All three engines ran; each answered with the same fact: the `(/speckit.implement,
r20261112T064607Z-b101)` pair was already recorded by WP-01a's wrap-up, so none wrote a second row.

1. `run-determination.py --action determine` (rc 0) →
   `{"duplicate": true, "unit_id": "/speckit.implement", "run_id": "r20261112T064607Z-b101",
   "note": "this (unit_id, run_id) was already determined"}`. The record WP-01a wrote:
   `.specify/memory/session/20261112T093540Z-run-determination-speckit-implement-r20261112t064607z-b101.md`.
2. `exec-quant.py --action collect` (rc 0) → `duplicate record for (/speckit.implement,
   r20261112T064607z-b101); no second row written` → store
   `.specify/memory/exec-quant/records/`; the existing row is
   `20261112T093544257617Z-004fee08.json`.
3. `feedback-utils.py --action record` (rc 0) → `{"id": "20261112T093549Z-speckit-implement",
   "path": ".specify/memory/feedback/20261112T093549Z-speckit-implement.md", "duplicate": true,
   "count_since_submission": 482, "threshold": 10, "should_prompt": true}`. The store dedupes on
   `(unit_id, run_id)` and offers no append/force flag, so this package's review text has no store
   landing point; it is preserved here instead (verbatim, so the observation is not lost):

   > WP-01b (T016-T025) completed the Anchor/Goal concept split's implementation lane: T018
   > command-mode adjudications (template-missing until T026; consumer migration deferred to T043)
   > were recorded rather than invented, T019 migrate_team refuses non-equivalent targets with exit 4
   > and zero writes, T020 preserved the --help/--version interface contract, T024 re-synced mirrors
   > to byte-identical (--check rc 0), and T025 closed every rename-caused red across 13 test modules.
   > Final targeted reading: 429 passed, 6 failed, 2 skipped (rc=1); the 6 remaining reds are 3
   > E2-baseline pre-existing ids and 3 live-tree cases owned by T049-T054. One in-passing repair
   > (engine docstring action table missing the goal-*/cleanup write rows) was disclosed.

Recorded observation: the wrap-up contract binds `(unit_id, run_id)`, not the package, so a run
that executes several implementation packages in one run id can carry review text for the first
package only. That gap is a store-schema fact, not a package defect; it is reported here rather
than worked around with a fabricated run id.
