# Implement — WP4-tests (093-concurrency-by-default)

**Executor**: implement-stage fork worker for package `WP4-tests`
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-wp4` (branch `093-wp4`, base `7ec5cc05`)
**Date**: 2026-11-09
**Rows closed**: 38 / 38 authored (see the closure table for per-row reading status)
**Write domain**: the 15 declared test-module paths plus `test-evidence/wp4-*.txt` and this note; **no framework document was edited**.

---

## 1. Package map and modules

| Module | Rows |
|---|---|
| `tests/contract/test_concurrency_declarations.py` | T016, T018, T020, T092, T094, T129 |
| `tests/unit/test_concurrency_check_engine.py` | T015, T136 |
| `tests/contract/test_concurrency_class_table.py` | T027 |
| `tests/contract/test_concurrency_serial_reason.py` | T042, T044, T046–T050, T057 |
| `tests/contract/test_concurrency_units.py` | T066–T073 |
| `tests/contract/test_concurrency_dispatch_capability.py` | T086, T087, T089 |
| `tests/contract/test_concurrency_high_order.py` | T029, T091, T141, T143 |
| `tests/contract/test_concurrency_disposal.py` | T107, T123, T125 |
| `tests/contract/test_concurrency_real_run_evidence.py` | T106 |
| `tests/contract/test_test_entry_guard.py` | T159 (no clause claimed — the user ruling names the guard) |
| `tests/contract/test_sdd_carrier_contract.py` | T152 |
| `tests/contract/test_sdd_project_setup_skill.py` | T152 |
| `tests/contract/test_sdd_loop_driver_skill.py` | T152 |
| `tests/contract/test_coaching_run_contract.py` | T152 |

**Scope note (one declared path carries no WP4 row)**: the package map's `write_domain`
lists `tests/contract/test_concurrency_reproduction_092.py`, but its authoring row is T090,
which the map assigns to `WP5-release`. No WP4 row names that module, so it was not authored
here; the fourteen modules above are exactly the WP4 row set. This is a package-map/row
inconsistency, recorded rather than resolved by taking another package's write domain.

All readings below were produced with the canonical entry only:
`bash scripts/bash/run-tests.sh <paths> -q` (pytest-xdist). No raw `pytest` /
`python3 -m pytest` was used at any point (FR-036).

---

## 2. Per-row closure table

Legend: **GREEN** = measured pass on this worktree; **RED-FIRST** = the module was authored
red-first and its green reading is deferred to the declared-order fold (the dependency is
named); **DONE** = the row's own deliverable is the reading, not a green assertion.

| Row | Module | What it pins | Reading in this worktree | Evidence |
|---|---|---|---|---|
| T015 | unit | kind ∈ `fact_kinds`, stem == `fact:`, C-003 per-slug kind | **GREEN** (3/3) | `wp4-unit-engine.txt` |
| T016 | declarations | registration is a read behaviour; rename / broken `fact:` mutations (never deletion) | **GREEN** (mutation cases discriminated) | `wp4-green-declarations.txt` |
| T018 | declarations | subset construct reported, never dropped; stem disagreement is `registration-invisible` | **GREEN** | `wp4-green-declarations.txt` |
| T020 | declarations | source ↔ `.specify/shared/` byte identity; mirror-only layer readable | **GREEN** | `wp4-green-declarations.txt` |
| T027 | class_table | classify pass + V-2 double-direction drift guard | **RED-FIRST** — engine absent (WP2) | `wp4-red-first-modules.txt` |
| T029 | high_order | obligation reachable from body or anchor; unresolvable anchor red | **RED-FIRST** — engine (WP2) + class anchors (WP5 T034–T036) | `wp4-red-first-modules.txt` |
| T042 | serial_reason | two-unit overlap reads effective 2; closed ordered code list; condition↔code bijection both directions | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T044 | serial_reason | per-code evidence form; `.` rejected for every code; form/reason inconsistency both directions | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T046 | serial_reason | four condition-bound evidence fixtures (edge+verdict ptr / intersecting paths / probe+landing / before-after readings) | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T047 | serial_reason | budget code rejected without measured remaining budget | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T048 | serial_reason | host code needs a resolving landing point (never reusable) | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T049 | serial_reason | simplicity / controllability / history rejected with the string named | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T050 | serial_reason | two-condition ordered record; list length never reported as concurrency | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T057 | serial_reason | red-first run recorded by name | **DONE** — 43 FAILED names recorded | `wp4-red-first-modules.txt` |
| T066 | units | max interval overlap; triple judged together | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T067 | units | missing interval → literal `not_evaluated`, unit named, no pass | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T068 | units | one/two fields alone → `reading-incomplete`; shortfall needs a reason | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T069 | units | bound recomputed from slot fact + ceiling owner − reserve; operands reported | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T070 | units | V-17 partition replay: identical ids/layers/edges | **GREEN** (retained 070 gate engine) | `wp4-red-first-modules.txt` (pass list) |
| T071 | units | V-19/V-20 write-domain unit form | **GREEN** for empty-domain and read-only; **RED-FIRST** for directory-level (T061 / WP3) | `wp4-red-first-modules.txt` |
| T072 | units | V-21 executor/verifier independence; prose alone red | **GREEN** (module judge; fixtures both directions) | `wp4-red-first-modules.txt` |
| T073 | units | V-22 integration order = layer-flattened declared order incl. tie-break, replay-stable | **GREEN** (retained 070 gate engine) | `wp4-red-first-modules.txt` |
| T086 | capability | existing `capability-tools` is the reading; a new key never upgrades the verdict | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T087 | capability | absent / unadjudicated verdict ⇒ exit 2 `owner-unavailable`; adjudicated value reported verbatim | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T089 | capability | statement-by-statement mismatch reported, never repaired; verdict value carried | static judge **GREEN**; engine half **RED-FIRST** (WP2) | `wp4-red-first-modules.txt` |
| T091 | high_order | anti-nesting depth 2 + three prohibitions; taxonomy keeps its shape | **GREEN** (mutation judge red on a stage-can-carry-driver tamper) | `wp4-red-first-modules.txt` (pass list) |
| T092 | declarations | shared strings closed, singly owned, no cross-role use | **GREEN** | `wp4-green-declarations.txt` |
| T094 | declarations | landing discipline reachable by path; judgment faces resolve | **GREEN** | `wp4-green-declarations.txt` |
| T106 | real_run | report shape judge (real-only, intervals, verdicts, order, duration, 091 baseline, `not_evaluated` instead of 0/estimate) + engine interval evidence | judge **GREEN**; engine half **RED-FIRST** (WP2); live report `not_evaluated` (WP5 T110) | `wp4-red-first-modules.txt` |
| T107 | disposal | `owner-unavailable` (exit 2) vs inconsistency (exit 1) distinguishable by exit code alone | **RED-FIRST** — engine (WP2) | `wp4-red-first-modules.txt` |
| T123 | disposal | closed four-member disposition domain; one disposition per statement; pointer resolves; record dated | domain + judge **GREEN**; live ledger `not_evaluated` (WP5 T134) | `wp4-red-first-modules.txt` |
| T125 | disposal | ceiling owner remains `wp-gate.py --slot-cap-ceiling` (WG-16); no second numeric site | **GREEN** | `wp4-red-first-modules.txt` (pass list) |
| T129 | declarations | each fact carries its registration line; unregistered file red | **GREEN** (mutation: registration line removed) | `wp4-green-declarations.txt` |
| T136 | unit | five actions' argument surface; `--record` required; cost-benefit fixture | cost-benefit **GREEN**; argument surface **RED-FIRST** (WP2) | `wp4-unit-engine.txt` |
| T141 | high_order | analyze defaults to N≥2 Workers; read-domain intersection; deterministic consolidation; triple + ids; `off` mutation red | **RED-FIRST** — driver surfaces (WP3 T139/T140); mutation judge authored | `wp4-red-first-modules.txt` |
| T143 | high_order | runner `--help` shape (stdin prompt, stream-json, sentinel); pool bound is a runtime `nproc` reading; in-process fan-out not a mechanism | runner + mechanism **GREEN**; pool-bound live **RED-FIRST** (WP3 T142) | `wp4-red-first-modules.txt` |
| T152 | 4 framework modules | in-process ban + fork/subprocess carriers; old rule absent | **DONE red-first** — 8 re-pinned tests red until WP3 T144–T151; the other 61 tests in the four modules stay green | `wp4-t152-repin.txt` |
| T159 | test-entry guard | raw `pytest` / `python3 -m pytest` guard over the tracked framework artifacts with the exact allowlist | **DONE red-first** — mutated copy turns it red; prose stays quiet; live tree red with the 9 named offenders until WP3 T156–T158 | `wp4-red-first-modules.txt`, `wp4-t152-repin.txt` note, guard output |

---

## 3. Test readings (commands, exits, counts)

| Reading | Command (entry: `bash scripts/bash/run-tests.sh … -q`) | Result | File |
|---|---|---|---|
| Declaration layer | `tests/contract/test_concurrency_declarations.py` | **13 passed**, exit 0 | `wp4-green-declarations.txt` |
| Engine unit module | `tests/unit/test_concurrency_check_engine.py` | 4 passed, **5 failed** (T136 engine surface, red-first) | `wp4-unit-engine.txt` |
| New contract modules | 8 modules (class table … guard) | **43 failed, 23 passed, 2 skipped** — every failure is a designed red-first (engine absent / WP3 sweep pending / T061 pending / T159 offenders) | `wp4-red-first-modules.txt` |
| T152 re-pin | the four framework modules | **8 failed** (the re-pinned carrier tests), **61 passed**, plus the serial pass 1 passed | `wp4-t152-repin.txt` |
| Full suite | whole tree (parallel runner) | **224 failed, 8171 passed, 4 skipped**; new vs the frozen baseline = **63** names = the **56 designed WP4 reds** + **7** trigger/tuning order-sensitive names WP1's T002 note already records (serial-vs-parallel difference); **0** baseline names disappeared | `wp4-suite-after.txt` |

The two skips are explicit `not_evaluated` readings, never silent skips:

1. `test_every_pre_existing_statement_has_a_readable_disposition` —
   `not_evaluated: the live disposal ledger lands with T134 (WP5)`.
2. `test_this_features_coordination_report_is_decidable_or_not_evaluated` —
   `not_evaluated: this feature's own coordination report lands with T110 (WP5)`.

**Suite comparison discipline.** The frozen baseline (`notes/test-baseline.txt`, 161 names) is
a *serial* reading; GATE-1 requires like-for-like normalization (`sed 's/^FAILED //;s/ - .*//'`)
and WP1's T002 note owns the order-sensitivity caveat for the trigger/tuning suites. This
worktree's full run is the canonical parallel runner on a stable tree (no edit during the
run). A first attempt was discarded: it overlapped this package's commit and note-writing
(the same overlap failure WP1 recorded for its first baseline attempt), and its evidence is
superseded by the stable-tree run recorded above.

---

## 4. Red-first proofs specific to the guard (T159)

- **Mutated copy, raw invocation** — a copy of `script-interface-definitions.md` with
  `python3 -m pytest tests/unit -q` appended is reported (test red by design, proven green
  capability in the same run): `test_mutated_copy_with_a_raw_invocation_turns_the_guard_red`
  passes, i.e. the scanner discriminates.
- **Prose-only mutation** — "a pytest module", "pytest only collects", "the pytest
  interpreter" stay quiet.
- **Runner name alone** — naming `scripts/bash/run-tests.sh` is not an invocation.
- **Live tree** — the guard reports exactly the T158-measured offenders plus the live
  instructions line:
  `.specify/instructions.md:256`; `docs/reference/history/00-cross-cutting-lessons.md:57,95`;
  `shared/definitions/non-disposable-definitions.md:704`;
  `skills/external/create-skills/SKILL.md:167,168`;
  `skills/external/merge-skills/references/decommission-and-wiring.md:73`;
  `skills/internal/implement-feature/SKILL.md:180,193`.
  The green reading arrives when WP3's T156–T158 land (declared-order fold).

---

## 5. Commits

| Commit | Content |
|---|---|
| `5d92723f` | the 14 test modules (10 new, 4 re-pinned) |
| `d2524e945` | the five evidence files `wp4-*.txt` |
| the commit carrying this note | `notes/implement-wp4.md` (this page) |
---

## 6. Residual risks

1. **Engine-absent reds and fixture schema co-design.** `scripts/python/concurrency-check.py`
   is WP2's write domain and is not in this worktree. Every engine case is red by
   construction. The record schemas the tests feed the engine are pinned in the module
   docstrings from C-027, C-031 and data-model E-3/E-5 (block-subset/v1, top-level
   `requested` / `effective_reason` / `units[]` with `unit_id`, `dispatched_at`,
   `settled_at`, `executor_id`, `verifier_id`; serial-reason records carry `pattern`,
   `codes`, `evidence.<code>` with per-code forms). WP2 must implement to this shape; the
   fold's verifier reconciles any residue.
2. **Deferred greens and their owners.** T027 / T042–T050 / T066–T069 / T086–T089 / T106 /
   T107 / T136 green with WP2. T029 and T071's directory-level case green with WP3 T061 +
   WP5 T034–T036 (class obligation anchors). T141 / T143's pool-bound and T152 / T159 green
   with WP3 (T139–T142, T144–T151, T156–T158). T123's live ledger and T106's live report
   green with WP5 (T134, T110). These are recorded `not_evaluated` with reasons where the
   test itself requires the artifact.
3. **Package-order note (structural).** T029 (`obligation-missing` empty on the live tree)
   requires the class obligation anchors that WP5's T034–T036 author; as the fold order is
   WP2 → WP3 → WP4 → WP5, this one row's green necessarily lands after WP5. The same holds
   for T123's live ledger and T106's live report. No row was weakened to hide this.
4. **DoD-8 vs C-079 (anomaly).** DoD-8 lists dispositions
   `owner-moved` / `pointer` / `dated-record` / `retained` / `explicitly-removed` (five),
   while the contract owner (C-079, `existing-semantics-disposal.contract.md`) closes the
   set at four and states "There is no fifth disposition". The test pins the contract owner
   (four values); the DoD wording should be corrected to the owner's closed set.
5. **Guard detector corpus.** The detector is invocation-shaped (interpreter `-m` form, or
   `pytest` followed by a flag/path operand). One corpus line is intentionally not
   matched: `templates/verification-log-template.md` ("`VAR=x pytest …`", prose about the
   key=value parser) — it is outside T158's measured offender list and is not an execution
   instruction. If it should be swept, T158's list needs the row revised first.
6. **Class-table `measured` shape.** The double-direction guard reads per-root counts from
   `measured` in either `{root_id: count}` or `[{root_id|root, count|members}]` form. A third
   shape would fail the green reading by design (a named assertion, not a silent pass).
