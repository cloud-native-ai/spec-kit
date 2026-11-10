# Feature Reference — 093-concurrency-by-default

**Feature**: default subagent concurrency across every execution body (skills, commands, goal, team, loop)
**Spec directory**: `.specify/specs/093-concurrency-by-default/`
**Binding**: `spec:093-concurrency-by-default`; `flow_class=execution; source=declaration; marker=; error=-`
**Requirement → Feature**: `093-concurrency-by-default` → **Feature 093** (`.specify/features/093-concurrency-by-default.md`)
**Authority**: `requirements.md` (36 FR, 12 SC, 15 clarify rulings + 3 dated user rulings of 2026-11-09) owns intent; `contracts/*` own conformance;
`plan.md` owns design. This page restates no rule — it maps.

---

## Delivery map — FR → contract clause

| FR | Clause | FR | Clause |
|---|---|---|---|
| FR-001 | declaration-facts C-005, C-014 | FR-018 | executor-obligations C-057, C-059 |
| FR-002 | declaration-facts C-010, C-011 | FR-019 | existing-semantics-disposal C-091 |
| FR-003 | declaration-facts C-014, C-015 | FR-020 | declaration-facts C-008; judgement-engine C-034 |
| FR-004 | declaration-facts C-004; judgement-engine C-023, C-024 | FR-021 | judgement-engine C-037, C-039 |
| FR-005 | executor-obligations C-045…C-048 | FR-022 | judgement-engine C-037, C-038 |
| FR-006 | executor-obligations C-049; judgement-engine C-028 | FR-023 | judgement-engine C-040; executor-obligations C-057 |
| FR-007 | judgement-engine C-029, C-030; executor-obligations C-050…C-052 | FR-024 | high-order-executors C-073…C-075; executor-obligations C-059 |
| FR-008 | judgement-engine C-031…C-034; executor-obligations C-058 | FR-025 | high-order-executors C-078 |
| FR-009 | judgement-engine C-027; executor-obligations C-053 | FR-026 | high-order-executors C-063…C-065 |
| FR-010 | declaration-facts C-004 (`unit_form`); judgement-engine C-023 | FR-027 | high-order-executors C-066, C-067 |
| FR-011 | judgement-engine C-029 (`dependency-edge` evidence) | FR-028 | high-order-executors C-069…C-071 |
| FR-012 | executor-obligations C-043; existing-semantics-disposal C-082 | FR-029 | declaration-facts C-009; judgement-engine C-035, C-036 |
| FR-013 | declaration-facts C-008; judgement-engine C-029 (`write-conflict`) | FR-030 | executor-obligations C-060 |
| FR-014 | declaration-facts C-008; judgement-engine C-034 | FR-031 | declaration-facts C-001…C-003, C-010…C-013 |
| FR-015 | declaration-facts C-008; high-order-executors C-065 | FR-032 | existing-semantics-disposal C-079…C-081; plan Fact Owners |
| FR-016 | judgement-engine C-040; declaration-facts C-008 | FR-033 | existing-semantics-disposal C-085…C-092 |
| FR-017 | high-order-executors C-069; declaration-facts C-004 | FR-034 | high-order-executors C-093 |
| FR-035 | high-order-executors C-094 | FR-036 | no contract clause — the enforcement is the guard test `tests/contract/test_test_entry_guard.py` (T159) |

Count: 36 map rows, 36 distinct FR ids. Whether every requirement reaches at least one clause is decided by the
machine reading, not by this table: `account-clause-coverage.py` reports the FR lane as claimed / uncovered names
(from clause citation groups), and this map is the human index over that reading — it asserts no totality of its own.
FR-036 is the one declared exception: the 2026-11-09 user ruling names a guard test, not a clause, as its
enforcement, so the machine FR lane will report it uncovered until an owner revises that ruling; the exception is
recorded here rather than hidden.

## Measurement map — SC → red-first module

| SC | Measurement surface | Primary test module (red first) |
|---|---|---|
| SC-001 | every enumerated body maps to exactly one class; removing a body still turns it red | `tests/contract/test_concurrency_class_table.py` |
| SC-002 | a ready, dependency-free, disjoint-write fixture runs concurrently with `effective >= 2` | `tests/contract/test_concurrency_units.py` |
| SC-003 | every serial result carries a closed-set code with form-matching evidence | `tests/contract/test_concurrency_serial_reason.py` |
| SC-004 | the seven unit obligations each have a fixture and each turns red when its implementation is missing | `tests/contract/test_concurrency_units.py` |
| SC-005 | 092 shape (6 packages, incapable executor) red before repair, green after | `tests/contract/test_concurrency_reproduction_092.py` |
| SC-006 | at least one real run reports `effective >= 2`; missing quantities write `not_evaluated` | `tests/contract/test_concurrency_real_run_evidence.py` |
| SC-007 | goal targets, team seat territories and loop per-unit readings each have a fixture | `tests/contract/test_concurrency_high_order.py` |
| SC-008 | a stage with concurrent units decomposes by default and records a named decision otherwise | `tests/contract/test_concurrency_high_order.py` |
| SC-009 | removing a registered fact makes the reader report `unregistered` (exit 2), never a default | `tests/contract/test_concurrency_declarations.py` |
| SC-010 | every affected 064/070/086/092 assertion has a disposition record; suite green on `>=3.8` | `tests/contract/test_concurrency_disposal.py` |
| SC-011 | dispatch depth stays 2; a stage body that would carry the driver turns red | `tests/contract/test_concurrency_dispatch_capability.py` |
| SC-012 | same task set runs faster concurrently with an identical result set | `tests/unit/test_concurrency_check_engine.py` |

Count: 12 map rows, 12 distinct SC ids. Modules are added by `/speckit.implement` in red-first order; the
allocation is pinned once, by executor-obligations **C-060** — this page does not restate it a second time.

---

## Delivery surface (file level)

The surface is stated per **file path**, not per directory: two features writing different files in one directory
do not collide, and a directory-level claim would hide that. `declared` = this feature's intent; `delivered` is
recorded at implement/review.

| Surface | Path | Change |
|---|---|---|
| Declaration facts (new) | `shared/declarations/facts/concurrency-class.yaml` | new |
| | `shared/declarations/facts/serial-reason.yaml` | new |
| | `shared/declarations/facts/effective-concurrency.yaml` | new |
| | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` | new |
| | `shared/declarations/facts/decomposition-coverage.yaml` | new |
| | `shared/declarations/facts/executor-enumeration-roots.yaml` | new |
| | `shared/declarations/facts/concurrency-contract.yaml` | new |
| | `shared/declarations/facts/coordinator-dispatch-verdict.yaml` | new |
| Declaration registry | `shared/declarations/contract.yaml` | edit — register the eight slugs |
| Engine (new) | `scripts/python/concurrency-check.py` | new |
| Concept owners | `shared/definitions/subagent-definitions.md` | edit — [[STR-004]] dispatch-capability section |
| | `shared/definitions/goal-definitions.md` | edit — goal/target concurrency |
| | `skills/internal/create-team/references/conceptual-model.md` | edit — seat territory judgement |
| | `skills/external/sdd-loop-driver/references/decomposition-model.md` | edit — slot owner projection, coverage, integration order |
| Driver surface | `skills/external/sdd-loop-driver/SKILL.md` | edit — loop concurrency obligation |
| | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | edit — analyze-wave default and the fork dispatch mechanism (FR-034 / FR-035) |
| | `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | edit — slot cap projection |
| | `skills/external/sdd-loop-driver/scripts/wp-gate.py` | edit only if the ceiling moves — it stays the ceiling owner (C-083) |
| Skill bodies | `skills/internal/create-plan/SKILL.md` | edit — plan stage default-concurrent |
| | `skills/internal/create-team/SKILL.md` | edit — binding-time feasibility |
| | `skills/internal/run-agent/SKILL.md` | edit — dispatch preflight + routing |
| | `skills/internal/run-team/SKILL.md` | edit — default-concurrent executor |
| Agent definitions | `agents/*.agent.md` (17 files) | edit where the capability verdict requires it |
| Templates | `templates/plan-template.md` | edit — stage concurrency plan |
| | `templates/commands/*.md` (29 stems) | edit — concurrency obligation |
| Tests (new) | `tests/contract/test_concurrency_*.py` (9 modules) + `tests/unit/test_concurrency_check_engine.py` | new |
| Evidence | `.specify/specs/093-concurrency-by-default/test-evidence/` | new records, one file per entry |

**Not on this surface**: the SDD stage chain and its sentinels, `.specify/templates/commands/` (retired by an
earlier feature — this feature must not revive it, C-090), and every per-agent command copy under
`.claude/commands/` / `.qoder/commands/` (regenerated, never hand-edited, C-089).

---

## Overlap adjudication (F-093-001) — 064 / 070 / 086 / 092

F-093-001 recorded that Feature 093's delivery surface touches directories several earlier features also write.
The adjudication below is **file-level**, measured against each feature's own `feature-ref.md` and the git history
of the touched paths; it resolves the collision per path and records what each side keeps.

| Path | Earlier owner | Their use | 093's use | Adjudication |
|---|---|---|---|---|
| `shared/declarations/facts/` | 092 (`facts/*.yaml` substrate) | 092 registers its own facts there | 093 adds eight **new** files, none reusing 092's slugs | **No collision.** Different filenames in a shared directory; the substrate is reused, not edited. |
| `shared/declarations/contract.yaml` | 092 (registered its slugs) | one-line key per fact | 093 adds eight keys | **Real collision, resolved as append.** Both sides append distinct keys; neither rewrites the other's lines. A merge conflict here is expected and is resolved by taking both sides, not by reordering. |
| `scripts/python/` | 092 (`goal-utils.py`), 070 (`wp-gate.py` helpers) | their engines | 093 adds **one new** file `concurrency-check.py` | **No collision.** No existing engine is edited. |
| `skills/external/sdd-loop-driver/references/decomposition-model.md` | 070 (Work Package model, `wp-gate.py` contract) | WP definition, slot rules | 093 rewrites the slot and coverage statements into pointers | **Real collision on the file.** Resolution: 070 keeps the WP model and the gate; 093 owns only the *slot-value pointer* and the *per-stage coverage* paragraphs, and states that the number stays owned by `wp-gate.py` (C-083). The `decomposition` value domain and the three single-package verdicts stay 070's (FR-029). |
| `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | 070 (seat preset), 092 (team preset) | seat list, slot line | 093 replaces the slot line with a projection | **Real collision on one line.** Resolution: 093 edits the slot sentence only; the seat structure stays 070's/092's. |
| `skills/external/sdd-loop-driver/scripts/wp-gate.py` | 070 (owns `--slot-cap-ceiling`, `WG-16`) | ceiling default + validation | 093 reads the ceiling; it edits the script only if `WG-15` must become file-level (T-003) | **Real same-path overlap, dispositioned.** Default: read-only, C-083 forbids copying the number. If T-003's file-level write-domain judgement lands, 093 changes `WG-15` and nothing else in that file; 070 keeps ownership of the WP gate and every other check. |
| `skills/external/sdd-loop-driver/SKILL.md` | 064 and 070 (both edited it) | the driver loop's execution modes | 093 adds the loop concurrency obligation | **Real collision on the file, resolved by section.** The stage chain, sentinels and WP gate calls stay as they are; 093 adds one obligation paragraph and changes no step order (FR-028 (c)). |
| `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | earlier driver lines (081d / 085 / 091 authored the recipe bodies) | stage prompt, runner, watch, worktree and integration recipes | 093 rewrites § 本地原生拓扑's dispatch default and adds the analyze wave + fork mechanism to § Recipe 2's usage note (FR-034 / FR-035) | **Real collision, resolved by section.** Every other recipe (watch, worktree, integration, line registry) stays as it is; 093 owns only the local-topology default and the analyze-wave paragraph it adds. |
| `shared/definitions/subagent-definitions.md` | 064 (execution modes, write lines) | mode taxonomy | 093 adds the dispatch-capability section | **Adjacent, not overlapping.** 064's execute-section modes are referenced, not redefined; 093 adds a new section. |
| `shared/definitions/goal-definitions.md` | 092 (goal/target binding) | binding, target model | 093 adds the target-concurrency rule | **Adjacent.** 093 edits the concurrency paragraph inside the existing target section; the binding model stays 092's. |
| `skills/internal/create-team/references/conceptual-model.md` | 092 (seat model) | team/seat/target decomposition | 093 adds the binding-time territory-intersection judgement | **Adjacent.** The territory owner stays the same file; 093 adds the judgement, it does not move ownership. |
| `templates/instructions-template.md` | 086 (edited there) | instruction template body | 093 does not touch it | **No collision.** Cited by requirements.md FR-012 only as the *example* of directory-level ambiguity, which is why FR-012 demands file-level write domains. |
| `scripts/python/sync-mirrors.py` | 089 (last edit, `25d5fe13`); used by 070 | mirror engine | 093 does not touch it | **No collision.** Cited by requirements.md FR-012 as the other example; plan.md and research.md cite it as the mirror engine 093 *consumes*, and the plan records a zero-drift baseline. |
| `tests/contract/` | 064, 070, 086, 092 all add modules | their modules | 093 adds ten **new** modules | **No collision** if and only if no existing module is edited. Where an existing module asserts on `capability-tools` (R-5: eight modules), 093 *reads* it — C-038 pins that they stay green and forbids a new frontmatter key. |

**Disposition**: no earlier feature is redefined (C-091). Two paths carry genuine same-file edits
(`contract.yaml`, `decomposition-model.md`, plus one line of `stage-team-preset.md`); each is resolved by naming
which paragraphs 093 owns. Any collision not listed above must be recorded here with both paths before implement,
never resolved by silent overwrite (C-092).

## Overlap engine reading, and why it is not the adjudication (F-093-002)

`overlap-check.py` was run from **this worktree** (`.specify/.tmp/sdd-loop/worktrees/093-clarify`) on 2026-11-09:
`checked=84 specs, overlaps=195, decision=overlap` (`test-evidence/overlap-plan.json`). The reading is reported
in full, and it is **not** taken as the verdict, for two measured reasons:

1. **113 of the 195 hits are `nested-path`** — the engine pairs a directory against a file inside it (`scripts/python`
   against `scripts/python/goal-utils.py`). Two features writing *different* files under one directory is exactly the
   case FR-012 says a directory-level claim must *not* call a collision.
2. **The current-spec path set the engine reads is coarser than this feature's delivery surface** — it lists
   `scripts/python`, `shared/declarations/facts` and `templates/instructions-template.md`, none of which 093
   writes as a directory, and it omits the eight fact filenames, the eleven test modules and the 17 agent files. That
   is F-093-002's family: the engine's declared-surface extraction, not the surface itself.

The adjudication above is therefore **file-level and by reading**, against each earlier feature's own
`feature-ref.md` and `git log`. Every `same-path` hit against 064 / 070 / 086 / 092 (6 of them) appears in the table;
so does every path this feature edits that an earlier feature also edited. The engine's output is retained as
evidence of what was *measured*, and this paragraph is the record of why the measurement is not the decision.

## Open residue carried from clarify

- **F-093-002** (overlap-check goes vacuously clear from a nested worktree): the plan works around it by running
  the engine from the main repository root and by adjudicating declared surface by reading, and records the trap in
  `research.md` R-9. It is **not** fixed by this feature; the measured workaround is the disposition.
- **F-093-003** (who adjudicates coordinator dispatchability): registered as [[STR-011]] and read by
  judgement-engine C-039, but **not self-adjudicated** — it is carried into plan Decision Tension T-004 as a
  question with a recorded owner and an entry condition, not swalled silently.

## Disclosed rulings made in this stage

Each was adjudicated in place rather than escalated, per the unattended-run instruction; each is recorded where it
binds, not only here.

1. The slot cap value moves to a fact; the ceiling stays with `wp-gate.py`; the three prose sites become pointers —
   plan.md T-001 and C-082/C-083.
2. `effective` is defined as maximum interval overlap, and auxiliary aggregates are refused — plan.md T-002 and
   C-031.
3. `capability-tools` is judged, not extended with a new key — plan.md T-003 and C-038.
4. The coordinator's dispatch verdict is registered but not decided here — plan.md T-004 and C-039.
5. The eight fact entries are one per judgement surface, with `concurrency-contract` carrying the landing
   discipline — plan.md T-005 and C-001.
