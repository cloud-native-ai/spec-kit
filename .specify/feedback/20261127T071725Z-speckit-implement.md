---
id: "20261127T071725Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "r20261127T053750Z-109a-p2"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "109-prompt-adherence"
feature_id: "109"
disposition: "ignored"
partial: false
created: "2026-11-27T07:17:25Z"
summary: "Implement P2 (T009–T016) for 109-prompt-adherence. Landed the five-variant fixture family under tests/fixtures/prompt-adherence/ (seeded, project-only, indirect-only, recordless, negative; every seed "
disposition_reason: "introspection:introspection-20261127T162331Z:excluded"
---

## Review
Implement P2 (T009–T016) for 109-prompt-adherence. Landed the five-variant fixture family under tests/fixtures/prompt-adherence/ (seeded, project-only, indirect-only, recordless, negative; every seed verified readable through its owning engine's read surface at authoring time), the engine guard red-first (red run 23 failed / 1 passed, every failure the named engine-absent assertion, no import errors), and the read-only engine scripts/python/prompt-adherence.py: the interface (identical -h/--help with the four labels, run-time --version from the nearest pyproject.toml, undeclared options exit 2 before any action, the six declared flags), the five declaration facts through declaration_reader with the SHA-256 declaration-set stamp, store roots derived from runtime-store-layout.yaml (no second root table; an undeclared store exits 2), the six in-process sensor reads through the owning engines, the four-way absence derivation with the three reason causes and four invalid-source causes, and the per-run reading assembly (text + --json from one computed structure, no clock field, no verdict token). Part A gate green: 33 passed (engine 24 + declarations 9), closing the declarations guard's five engine-absent legs.

## Optimization Points
- Red-first evidence: notes/red-first-evidence.md now holds the T010 red run (23 failed / 1 passed, every failure the named engine-absent assertion, zero import errors), the T016 green capture (33 passed), the seeded fixture reading and the byte-identical rerun digests for both output forms (json c4e6c565…, human c57f9fc9…).
- Fixture authoring-time check (T009): all five variants were read through the owning engines' surfaces in process before the engine existed — seeded 2 determinations / 1 exec-quant / 2 feedback (one gate-family) / 1 evidence run / probe 1 class 1 object 0 errors; negative exposes its broken, unknown-version and bad-timestamp seeds as dropped or out-of-domain records.
- Staged state declared honestly: --check-coverage and --since/--until exit 2 with a "not delivered" message until their rows land (owner coverage map US2 / T020; window US4 / T028); output caps ride T028, audit replay T032. The engine docstring states this so no caller reads the refusal as a defect.
- Known baseline, not a regression: sync-mirrors --check reports MISS prompt-adherence-definitions.md + DIFF framework-map.md — the single projection is T033's row (same state P1 recorded; GATE-2 compares after that projection). script-interface-check exits 1 pre-commit only because the new engine and test paths are not yet git-tracked candidates; re-run at T035/T038.
- In-passing corrections disclosed: a leftover dead expression in the probe-registry reader and an unused local variable were removed before the green run; no behavior change.
- Anomalies: none.
