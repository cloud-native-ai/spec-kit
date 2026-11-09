# Research — Feature 094 (Phase 0)

Every ruling below was taken from live files or live commands in this session; the file or command that bears on it
is named. Rulings that changed the design carry their consequence.

## Archive and storage

**R-01 — The binding record lives inside the definition file; no second store.** 085 already stores one
definition per slug under a root selected by `resolve_scope` (`scripts/python/goal-utils.py`), and `create_goal`
writes exactly one `goal.md`. Adding a separate binding store would create a second owner for "who owns this" —
the failure FR-002 forbids. Consequence: `binding` is a frontmatter block of the existing file.

**R-02 — One objective carries both owner families.** 085's `resolve_scope` rejects a call when both a global and a
spec candidate exist (`scope-ambiguous`, read in `goal-utils.py`). With one archive, the two-candidate condition
disappears; the remaining question ("who created it") is answered by data, not by location.

**R-03 — `create_goal` already refuses duplicates.** `create_goal` raises `GoalError` when
`definition_path(repo_root, slug).exists()`, and `definition_path` resolves under `archive_root` =
`.specify/goal`. Consequence: FR-021's "same slug in both lines" needs no new detector; the message must additionally
name the existing `owner` / `owner_id` (C-27).

**R-04 — Frontmatter in existing definitions is ordinary YAML-ish key/value.** Reading
`.specify/archive/goal-team/trees/085-sdd-temporary-goal-team/goal/085-sdd-temporary-goal-team/goal.md` and the archive teams' `team.md`
shows flat `key: value` with inline lists. Consequence: a small closed reader inside `goal-utils.py` suffices.

**R-05 — Archive layout must be per-entry files.** Per `## Concurrent Development Safety` (AGENTS.md), append-only
observations land one file per entry. Consequence: receipts at `receipts/<kind>-<slug>.yaml`, moved trees at
`trees/<spec>/<kind>/<slug>/` (C-32).

**R-06 — `declaration_reader.parse_subset` must not be reused for definitions.** Its grammar
(`block-subset/v1`) refuses flow collections and block scalars, and the caller of the definition reader is not the
declaration layer. Consequence: `goal-utils.py` gets its own ~60-line reader; a fact file still goes through
`parse_subset` (C-78).

**R-07 — The archive root already exists and is small.** `.specify/goal/` holds 6 goals and `.specify/teams/` 12
teams; the spec-local set is 7 + 7 (baseline probe). An overlay of the two sets in this session returned no shared
slug, so migration cannot collide by identity (EP-002).

**R-08 — `.specify/archive/spec/` is an existing precedent.** It archives deprecated specs with the original
layout, owned by `/speckit.sanitize`. Consequence: `.specify/archive/goal-team/` follows the same shape, keeps
sanitize out of the write path, and is registered in `framework-map.md` next to the spec-archive row (C-100).

## Vocabulary and declarations

**R-09 — `run_id` is already a state-spine concept.** The spine header carries `run_id: r20261109T064500Z-092a`
(`.specify/state/094-goal-team-parallel.md`). Consequence: `owner_id` cites that field by name; this feature does not
re-declare its grammar (C-3).

**R-10 — Two facts, not one, keep value domains separate.** `flow-class-classes.yaml` shows the house shape
(`fact`, `kind`, `statement`, `consumers`, `former_carriers`). Two facts avoid one file owning both a set and a
threshold, which would need two `kind` values in one statement.

**R-11 — `contract.yaml` has no "registry of facts" today.** `declaration_reader.load_contract` returns the file as a
mapping, and `load_fact` matches on the `fact:` key of each file — there is no registration gate. Consequence: FR-031's
registration requirement must add one (`registered_facts:`, C-83) and the consumer must validate against it.

**R-12 — `flow-class-check.py --action lookup` is the class entry.** It exits 0 with a registered class for
`spec:094-goal-team-parallel` (measured). Consequence: the command-family predicate reuses it and does not modify it
(C-71, C-74).

**R-13 — A command without a registered class is "not in the family".** `templates/commands/` contains entry-layer
carriers whose class is unregistered; guessing a whitelist reintroduces the per-command hardcoding FR-005 forbids.
Consequence: A9 becomes C-72.

## Scope and engine behaviour

**R-14 — `--scope` is read in three places.** `goal-utils.py` (`resolve_scope`), `sdd-route.py` (`authorize`,
`--scope choices=("global","spec","auto")`), and command templates (`templates/commands/goal.md`,
`team.md` argument hints). Consequence: the value-set change is a three-surface edit plus the tests (C-9, C-29).

**R-15 — The engine already has a must-fail shape for a bad value.** argparse's `invalid choice` path exits 2 and is
already the precedent the spec names. Consequence: deleting `spec` needs no new error class (C-9).

**R-16 — `archive-scope` is the right name to keep.** The spec's `[[STR-002]]` literal is `archive-scope`, and the
concept it names (the archive coordinate system) is exactly what replaced the old position-based scope. Consequence:
no rename churn across 41 citations.

**R-17 — `auto` must lose its ambiguity branch.** With one archive the two-candidate ambiguity cannot arise; what can
arise is "slug in neither layer". Consequence: `auto` keeps read-only semantics and changes its failure reason set
(C-11).

**R-18 — `sdd-route.py` records scope today.** Its `authorize` payload carries `scope` and `spec_dir`. Consequence:
record `archive_layer` instead and resolve through the engine (C-29), keeping the payload additive.

## Writability and parallelism

**R-19 — The old defence was a forbidden-path sentence.** `shared/definitions/sdd-routing-definitions.md`
§ Hierarchy states `.specify/goal/**` and `.specify/teams/**` are forbidden to runs; no code enforces it. Consequence:
replacing a sentence with a function is a genuine strengthening (T-002), and the clause must live where an engine can
run it (C-14).

**R-20 — `goal-utils.py` already has a must-refuse precedent.** `scope-ambiguous` exits 2 with a message naming both
paths. Consequence: every new refusal reuses that idiom, giving the contract tests one shape to assert.

**R-21 — Complexity must answer a two-valued question with a noun.** Returning `direct | handoff` lets one computation
serve both "is it complex" and "does this run create a goal/team" — the requirement pair FR-018 / FR-039 shares one
input by design (Clarifications Q5). Consequence: C-79/C-81.

**R-22 — The comparison surface for a handoff threshold is task-row count.** `tasks.md` rows match
`^- \[[ xX>~]\] T[0-9]{3}` (`skills/external/sdd-loop-driver/scripts/decomposition-check.py`). Consequence: the fact
declares `metric: task-count` against that measured shape, and `implement`'s package sizing uses the same count.

## Concurrency and execution model

**R-23 — Single-agent implement is a measured bottleneck.** The 092 execution-lessons record § 1: one package of 60+ rows in one
500-turn agent took 116 min and hit the turn limit; 091's 3-package fix loop finished with zero integration
conflicts. Consequence: the plan declares a per-package ceiling of 16 rows and up to 6 concurrent executors (§ Execution Model).

**R-24 — Worktrees contaminate tree-scanning tests.** The same record § 2: fix worktrees under `.specify/.tmp` were
read as duplicate repo copies by migration/isomorphism/script-interface tests. Consequence: rule 1 of the package
brief set (clean before closure).

**R-25 — The serial failure list is the comparison face.** The record § 3: parallel mode writes bare ids while the
frozen baseline is the `FAILED`-prefixed list. Consequence: GATE-1 uses `test-evidence/plan-baseline-names.txt`
(46 ids, measured this session 2026-11-09; corrected at analyze round 4, 2026-11-09, from an earlier 44 reading —
the file holds 46 unique ids), and the runner records `passes=2`.

**R-26 — The existing integration queue is the only queue.** `skills/external/sdd-loop-driver/references/decomposition-model.md`
§ 13/§ 16 owns scheduling, independent verification and deterministic integration. Consequence: this feature adds no
queue, no registry and no ledger.

## Test surface and disposal

**R-27 — The goal/team suites are green on this tree.** Measured: `tests/contract/test_scope_resolution.py` 8 passed;
`test_temp_goal_contract.py` + `test_temp_team_schema.py` + `test_goal_scope_engine.py` + `test_goal_utils.py` +
`test_goal_targets_engine.py` + `test_goal_targets_check.py` + `test_checkpoint_protocol.py` 171 passed. Consequence:
the disposal work is a deliberate rewrite, not a repair of a broken suite.

**R-28 — The disposal list is 11 modules, and one A7 name does not belong.** A per-file scan for
`scope spec` / `spec-local` / `temp_*` / `Temporary` / `goal/goal.md` / `team/team.md` returned the 11 modules listed
in C-102; `tests/contract/test_goal_writeset.py` returned zero hits (it guards the summary write-set of
`.specify/goal`, which is the *new* location). Consequence: FR-041's list is measured, and A7's file list is a
starting point only (C-102).

**R-29 — Structural guards exist as a pattern.** `tests/contract/test_expression_compatibility.py` already freezes
file hashes for a non-regression face. Consequence: C-106 / C-107 follow that pattern (scan + synthetic mutation)
rather than adding a new check style.

**R-30 — The 14 real definitions are the acceptance data.** `test-evidence/requirements-baseline-probe.txt` records
the 7 + 7 paths, including slug/dir mismatches (`088` team `087-reporting-dogfood`, `089` goal
`script-interface-contract`). Consequence: migration is keyed by `<spec>/<slug>` pair, not by assuming slug == dir
name, and the probe output is the comparison baseline for SC-003.

**R-31 — Evidence forms are already fixed by the driver gates.** `pre-analyze-check.py --stage plan` requires
`EP-NNN` rows in § Execution Premises with a closed `Status` domain, and `decomposition-check.py --mode plan` reads
FR definitions by the `^- **FR-NNN**:` shape. Consequence: the plan's premise table and the "43 FR" claim are shaped
for those readers, and their readings are recorded in `test-evidence/`.
