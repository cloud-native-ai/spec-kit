# T041 — stale live-target repair batch (disclosed)

- Date: 2026-11-25
- Run: `r20261125T022857Z-06dd`, implement package P5
- Authority: T041 ("every new failure must be attributed or fixed"; GATE-5 requires
  `comm -13 <implement entry baseline> <current>` empty). The repair is an assertion-side
  correction of a class T029 was scheduled to own; it adds no product behaviour and changes no
  engine.

## Measured before

- Implement entry baseline: `test-evidence/implement-baseline-failed.txt` — **748** failed names.
- P4 close-out: `test-evidence/p4-final-failed.txt` — **570** failed names, of which
  **351 were absent from the entry baseline** (`comm -13`), plus **9** setup errors.
- All 351 names already existed in the P1 delta, i.e. they were one continuous class left open
  across P1–P4, not a P5 regression.

## Root cause (one class, three shapes)

T029 classified live targets by `grep -rl '\.specify/memory' tests/` — a **literal** search. Paths
built from fragments never match it, and three fragment shapes stayed stale:

1. `ws / ".specify" / "memory" / "<store>"` — workspace fixtures and assertions pointed at the
   retired container while the engines wrote `.specify/<store>` (feedback / exec-quant / trigger /
   session / sanitize / todo / retention across the affected modules).
2. `resource_root / "memory"` — minimal init resource fixtures still built the pre-105 packaged
   seed namespace; init reads `seed/` now, so `.specify/session` and `.specify/knowledge` were
   never seeded (this also produced the 9 setup errors and the ai_tools/codex/skills-copy failures).
3. Fixture trees on disk — `seal-archive/reference-matrix/.specify/memory/session/entry.md` and
   `superagent-role/remote-topology/memory/exec-quant/records/*` were classified by their declared
   carrier paths, which already moved in the contract tables.

## Repairs (assertion/fixture side only)

- **Group A — init/resource fixtures**: `tests/conftest.py` (three minimal resource roots,
  `feedback_store`, the claude support-surface list), `tests/fixtures/ai_tools_support.py`
  (`memory/` → `seed/` + `session/`/`knowledge/` placeholders), `tests/unit/test_two_layer_skills_copy.py`
  (packaged sources carry the runtime-form `.specify/session/` path; the generic `memory` rewrite is
  deliberately gone), `tests/integration/test_ai_tools_multi_assistant_coexistence.py` (core set),
  `tests/integration/test_ai_tools_partial_core_repair.py` (message text).
- **Group B — workspace fixtures/assertions** (`.specify/memory/<store>` → `.specify/<store>`;
  container mkdirs become `.specify` or the store root): `test_efficiency_element.py`,
  `test_engine_face_contract.py`, `test_exec_quant_aggregate.py`, `test_exec_quant_channel_boundary.py`,
  `test_exec_quant_channel_compat.py`, `test_exec_quant_dispatch.py`, `test_exec_quant_engine.py`,
  `test_feedback_exec_quant_payload.py`, `test_feedback_intake_exec_quant.py`,
  `test_feedback_probe_cli.py`, `test_feedback_probe_entry_schema.py`,
  `test_feedback_probe_registry.py`, `test_measure.py`, `test_review_feedback_boundary.py`,
  `test_run_determination_engine.py`, `test_status_digest.py`, `test_store_state_protocol.py`,
  `test_trigger_engine.py`, `test_feedback_exec_quant_channel.py`, `test_trigger_promotion.py`,
  `test_trigger_telemetry.py`, `test_trigger_tuning.py`, `test_bounded_read_stdin.py`,
  `test_feedback_exec_quant_payload.py` (unit), `test_measure_unit.py`, `test_sanitize_checks_refs.py`,
  `test_sanitize_semantic.py`, `test_sanitize_store.py`, `test_sanitize_engine_contract.py`,
  `test_sanitize_us1.py`, `test_sanitize_us2.py`, `test_sanitize_us3.py`,
  `test_sdd_house_keeping_flow.py`, `test_agents_run_multi_child_edges.py`.
- **Group C — fixture trees**: `git mv` of the seal reference-matrix session carrier to
  `.specify/session/entry.md`; `git mv` of the superagent-role exec-quant record store to
  `<fixture>/exec-quant/records` (the engine's carrier root); the sanitize `archive` case's material
  and expectation moved from the retired `draft` path to the live `.specify/todo/old.md`.
- **Group D — semantic re-points** (not path-only): the trigger ignore-entry assertions now expect
  `trigger/telemetry.jsonl` (the engine's maintained entry); the run-determination "no new store"
  guard now measures `.specify/` children (`test_no_new_directory_appears_under_the_specify_root`).
- **Kept as legacy fixtures (by design)**: `test_sanitize_checks_migration.py`, the sanitize
  `memory/draft` residue cases, `tests/fixtures/migrate-097/`, anchor-layout and store-layout
  migration tests — these are the L-3-declared legacy carriers and continue to name the retired
  form. The live-refs guard (`test_tests_literal_confined_to_declared_set`) is green after the batch.

## Measured after

- Full fast tier: **218 failed, 10040 passed, 3 skipped, 0 setup errors** in 64.05 s
  (`test-evidence/p5-full-run.txt`; names `test-evidence/p5-full-failed.txt`).
- `comm -13` vs the implement entry baseline: **0 new failure names**
  (`test-evidence/p5-new-vs-baseline.txt` is empty).
- `comm -23` (baseline reds the batch also repaired): **530**.
- The remaining 218 are pre-existing baseline reds, each present in
  `implement-baseline-failed.txt`; they are untouched by this feature and are named by the file.
- Guard modules green: `test_store_layout_live_refs.py` + `test_runtime_store_layout.py` → 11 passed.
- Mirrors: `sync-mirrors.py --check` exit 0, **0** DIFF members (baseline 444; member-set delta
  `new=0`, `cured=all`); `regen-command-copies.py --check` exit 0.

## Scope statement

No engine, template, or other product file changed in this batch — its diff is confined to
`tests/**`. The only non-test files this package adds are spec-side evidence/notes and the S-7
re-check receipt under `.specify/migrate/receipts/`; the engine source carries no P5 modification
(the T036/T042 drills were restored to checksum equality). The repair is reversible and confined
to the assertion/fixture side of the class T029 classified.
