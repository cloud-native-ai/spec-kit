# Feature Reference — Feature 090

## 1. Binding

| Field | Value |
|-------|-------|
| Feature ID | 090 |
| Feature name | Re-Anchoring（不忘初心 · 温故而知新） |
| Requirement branch | `090-re-anchoring` |
| Requirements | [`requirements.md`](requirements.md) |
| Plan | [`plan.md`](plan.md) |
| Feature detail | `.specify/memory/features/090.md` |
| Feature index row | `.specify/memory/features.md` (Draft → Planned at this stage) |
| Flow class | execution |
| FR / SC | 10 / 4 |
| Structure | single page under `shared/definitions/` + edits to five existing rule surfaces + four contract guards |

## 2. Delivery Surface

Every path below is a **source** path. Its `.specify/` counterpart is produced by `sync-mirrors.py` and is never
hand-edited; the two live governance files are single copies.

| # | Surface | Change | Mirror |
|---|---------|--------|--------|
| 1 | `shared/definitions/re-anchoring-definitions.md` | NEW — owner page: two concepts, T0/T1/T2, agent obligation, boundaries | `.specify/shared/` pair, byte-equal |
| 2 | `shared/definitions/agent-definitions.md` | EDIT — `## Re-Anchoring Obligation` section | `.specify/shared/` pair |
| 3 | `templates/constitution-template.md` | EDIT — `### XXI. Re-Anchoring (不忘初心 · 温故而知新)` | `.specify/templates/` pair |
| 4 | `.specify/memory/constitution.md` | EDIT — `### XXII. …`, Sync Impact Report, v1.19.0, `Last Amended` | none (live governance file) |
| 5 | `templates/instructions-template.md` | EDIT — ambient `## Re-Anchoring …` section | `.specify/templates/` pair |
| 6 | `.specify/instructions.md` | Regenerated from #5 by `scripts/bash/generate-instructions.sh` | none (generated live copy) |
| 7 | `scripts/bash/generate-instructions.sh` | EDIT — `INSTRUCTIONS_BUDGET_BYTES` raised so the section fits | `.specify/scripts/bash/` pair |
| 8 | `skills/internal/manage-constitution/SKILL.md` | EDIT — one `- **MUST include**` sub-entry (13 → 14) | `skills/internal` pair |
| 9 | `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` | EDIT — part 5 rewritten rule-first; minimal shape carries it; rules list gains the mandatory-audit rule | `.specify/skills/sdd-loop-driver/` pair |
| 10 | `skills/external/sdd-loop-driver/SKILL.md` | EDIT — Hard Requirement 14 names the audit and the owner | same pair |
| 11 | `tests/contract/test_reanchoring_contract.py` | NEW — five-face guard | none (test file) |
| 12 | `tests/contract/test_sdd_loop_driver_reanchor.py` | NEW — protocol part 5 / tiers / verdict / minimal shape | none |
| 13 | `tests/contract/test_constitution_double_landing.py` | EDIT — 21 / 22 / 14; watchlist 8 → 9 | none |
| 14 | `tests/contract/test_fast_fail_discipline.py` | EDIT — watchlist-length pin and section-count pins | none |

## 3. FR → Contract / Slice Map

| FR group | FRs | Contract / task work |
|----------|-----|----------------------|
| Owner page (concepts, tiers, obligation, no machinery) | FR-001 | `re-anchoring-faces.contract.md` C-1, C-2, C-8 |
| Constitution on both surfaces | FR-002 | C-3; `governance-landing.contract.md` C-1, C-2 |
| Ambient section on both instruction surfaces | FR-003 | C-4 |
| Anchor carries task anchor **and** rule anchor | FR-004 | `direction-audit.contract.md` C-4; `data-model.md` V-1, V-2 |
| Five questions, rules first | FR-005 | C-3, C-4; **ordering assertion** = `guard-tests.contract.md` C-7 (OPEN) |
| Tiered reload, no per-tool-call full reload | FR-006 | C-8; `data-model.md` V-4, V-5 |
| Audit is a statement, never an approval request | FR-007 | C-7 |
| Agent-side obligation + brief carries the anchor summary | FR-008 | `re-anchoring-faces.contract.md` C-5 |
| Generator mandate entry | FR-009 | C-6; `governance-landing.contract.md` C-3 |
| Counting pins move in the same batch, guarded | FR-010 | C-4, C-5; `guard-tests.contract.md` C-1…C-4, C-8 |

## 4. SC → Measurement

| SC | Path | Measurement source | Slot |
|----|------|--------------------|------|
| SC-001 | final | `test_reanchoring_contract.py` (four assertions) + the six-pair `diff -q` loop in `quickstart.md` S-1/S-2 | every stage (cheap) |
| SC-002 | final | **Not yet satisfiable.** `contracts/guard-tests.contract.md` C-7's ordering assertion does not exist; the quickstart S-4 scenario demonstrates today's indifference to a goal-first rewrite | after tasks (T-090-… C-7 task) |
| SC-003 | final | `test_constitution_double_landing.py` + `test_fast_fail_discipline.py::test_x15`/`test_x13`; pins 21 / 22 / 14, watchlist 9 | every stage (cheap) |
| SC-004 | final | `test_sdd_loop_driver_reanchor.py::test_reload_tiers_are_bounded` + the protocol's own tier text read against the owner page § 2 | every stage (cheap) |

## 5. Feature-List Review

| Check | Result |
|-------|--------|
| Row exists in `.specify/memory/features.md` | yes — 090, status `Draft` before this stage |
| Detail file `.specify/memory/features/090.md` | yes — Overview / Key Changes / Implementation Notes / Related Files |
| Status transition this stage | `Draft → Planned` (per the state machine owned by `.specify/templates/feature-details-template.md`) |
| New feature created or merged | no — 090 is an existing row renumbered from 087 |
| Classification unchanged | yes — framework-level, functional |
| Creates a new top-level concept | no — the rule lives under the existing `shared/definitions/` topic directory |

## 6. Disclosed Rulings

1. **The plan describes a tree that already exists.** Thirty of the fourteen delivery rows landed before the spec
   chain ran (`5a1041e4`, `55776937`, replayed as `137adb7f`). This plan therefore measures the tree and hands the
   *remaining* work (one guard assertion, the closure evidence) to tasks, rather than designing a re-implementation.
   Writing a plan for work already done is not a plan defect; writing one that pretends it was not done is.
2. **The one compliance gap is escalated, not repaired** (`plan.md` T-001 background; `guard-tests.contract.md` C-7).
   `SC-002`'s ordering clause is a documentation proposition with no guard. It is recorded as OPEN in three places —
   `plan.md` Complexity Tracking, the contract, and this page — because a single silent note is exactly the failure
   mode the feature exists to prevent.
3. **The contract suite is red before this stage** (`49 failed, 6368 passed, 2 skipped`). Any acceptance criterion
   written as "the suite is green" would be unpassable; the criterion is "no NEW failure" against the name-level
   baseline in `test-evidence/plan-contract-baseline-raw.txt`.
4. **Same-author delegation was unavailable.** The objective-analysis gate expects fresh-context subagents for
   self-scoring; this stage worker cannot dispatch, so the degraded evidence path is disclosed in `plan.md` § Phase 0
   item 6 instead of being papered over with a Pass row.
5. **The requirements file has two defects this stage found but must not repair** (see § 7). Requirements-side fixes
   belong to a requirements revision, not to a plan write into another stage's artifact.

## 7. Follow-ups Not Owned

| # | Item | Why it is not this feature's plan output |
|---|------|------------------------------------------|
| F-1 | `validate-requirements.py` reports `path-marker: SC-001…SC-004 carry no **Path** marker` (4 errors) | The fix edits `requirements.md`, which is the requirements stage's artifact; this stage's write territory is the plan artifact set |
| F-2 | `requirements.md` has no `### Measurement Sources & Collection Methods` section, which `validate-decision-tensions.py` reads to resolve `expected_sacrifice` (label `expected-sacrifice-unmapped`) | Same territory boundary as F-1; the plan's two tension records therefore cite `SC-002 Source` / `SC-004 Source` in the owner's `<SC-NNN> Source ↓` grammar, which resolves the moment that section lands |
| F-3 | `test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` fails (`gate total 23 → 27`) | A pre-existing red outside this feature's clauses; recorded in `research.md` R6, not repaired here |
| F-4 | `test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies` fails on `.qoder/agents/sdd-analysis-worker.agent.md` (clause is not the `rewrite_paths` rendering) | A pre-existing rendered-copy projection defect; recorded in `research.md` R6 |
| F-5 | The `PATH` `python3` has no pytest | An environment fact, recorded in EP-001 and pinned in every `quickstart.md` command |
