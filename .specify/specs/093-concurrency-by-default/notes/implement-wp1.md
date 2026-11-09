# Implement — WP1-facts (feature 093-concurrency-by-default)

**Package**: `WP1-facts` (`tasks.md` § Work Packages) — rows **T001–T014, T026, T098**.
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-clarify`, branch `093-concurrency-by-default`.
**Date**: 2026-11-09. **Mode**: one detached fork executor, serial, no subagents, no push.

**Outcome**: 15 of 16 rows closed; **T098 left open** — the coordinator-dispatch verdict value has no
owner ruling (F-093-003), and C-016 forbids writing one that was not supplied. The surface is
registered and fail-closed; the row cannot close without inventing intent.

## Commits (oldest first)

| Commit | Rows | Subject |
|---|---|---|
| `41900079` | T004, T008–T013, T098 | the eight facts, the append-only registration, and the regenerated `.specify/shared/` mirror |
| `cbdf8fe2` | T001–T003, T005–T007, T014, T026 | setup baselines, red-first readings, fact-schema evidence |
| `cc05e4b6` | T004, T014 | the shared-string closed set registered in [[STR-006]]; subset-clean interval wording; coherence evidence |
| `354145e2` | T009 | the GitHub projection trees added to `excluded_layers` |
| _(this commit)_ | T002, wrap-up | the frozen failure-name baseline and this page |

## Per-row closure

| Row | Status | Evidence |
|---|---|---|
| T001 | closed | `notes/red-first-evidence.md` created with the header/entry format; entries appended by T004 / T014 / T026 / T098 (the file is the row's deliverable) |
| T002 | closed | `test-evidence/suite-baseline-093.txt` (serial canonical runner, stable tree: **161 failed, 8147 passed, 2 skipped**) + `notes/test-baseline.txt` (161 sorted failed ids) + `test-evidence/wp1-t002-baseline.txt` (run provenance and the overlap/ordering comparisons) |
| T003 | closed | `notes/pre-change-measurements.md`; `test-evidence/wp1-t003-enumeration-probes.txt` (38 / 16 / 29 / 17 / 12 / 6 = 118 bodies; trap form 17) |
| T004 | closed | the eight files under `shared/declarations/facts/` (slug = stem); red `test-evidence/wp1-t004-t014-t098-t026-red.txt`; green `test-evidence/wp1-t014-schema.txt` (8/8 PASS) and `wp1-facts-coherence.txt` |
| T005 | closed | `shared/declarations/contract.yaml` +8 append-only keys; `test-evidence/wp1-t005-t014-green.txt` — `--action list` reads contract 17 / facts 32 with all eight slugs in the `facts` array |
| T006 | closed | `coverage-baseline.txt` frozen (601 lines); `test-evidence/wp1-t006-coverage-baseline.txt`; clause count re-measured **94** in the same pass |
| T007 | closed | `test-evidence/mirror-baseline-tasks.txt` — pre-sync drift (8 MISS + 1 DIFF), regeneration, post-sync `--check` exit 0 with every pair byte-identical |
| T008 | closed | `shared/declarations/facts/concurrency-class.yaml` — closed class table, semantic name, per-class fields, FR-004 `(root_id, produced_shape)` rule |
| T009 | closed | `shared/declarations/facts/executor-enumeration-roots.yaml` — exactly five roots as patterns, class per root, 10 excluded projection layers |
| T010 | closed | `shared/declarations/facts/serial-reason.yaml` — six codes in declaration order, two groups, condition index (b)–(e) with a zero-gap bijection, evidence forms |
| T011 | closed | `shared/declarations/facts/effective-concurrency.yaml` — the three fields, `integer \| not_evaluated`, interval-overlap computation with the half-open/tie-break rule |
| T012 | closed | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` — slot cap 6, reserve 1, `max_turns` 1..500, round ceiling 2, the `min` formula, the ceiling by pointer (`wp-gate.py --slot-cap-ceiling`, WG-16) |
| T013 | closed | `shared/declarations/facts/decomposition-coverage.yaml` — 8 stage rows, analyze `on` with its spine-sourced N, the spine-keys-as-projections relation |
| T014 | closed | `test-evidence/wp1-t014-schema.txt` — required keys / kind / slug==stem all PASS for the eight; all eight `--action get` exits 0; `harness-triple-check.py --action coverage` exits 0 with 0 findings over the layer |
| T026 | closed | `notes/red-first-evidence.md` § T026; `test-evidence/wp1-t004-t014-t098-t026-red.txt` — the named commands' real failing output and exits (T015 ↔ exit 4, T016–T020 ↔ exit 4, T025 ↔ exit 1 via `--files`) |
| **T098** | **open** | the fact exists and `--action get` exits 0 (surface registered, fail-closed), but `statement.decision_state: unadjudicated`: C-016's "carry a value from `{allow, forbid}`" and "never write a verdict the owner did not supply" are jointly unsatisfiable until the owner rules (register `F-093-003`, plan T-004) |

## Test readings (red-first where a `[green:]` row declares it)

- **T004 (C-001) red → green**: the eight `--action get` invocations exit **1** (`no declaration for fact '<slug>'`) before the files; after them, exits **0** for all eight, and the schema check reports 8/8 PASS.
- **T014 (C-002) red → green**: same red reading; green = the 8/8 schema PASS plus `harness-triple-check.py --action coverage` exit **0**, findings **0**, pending **0**, unclassified **0**.
- **T098 (C-016)**: red = absent fact (exit 1). Partial green = surface registered (exit 0). The value half cannot be turned green without the owner — recorded, not faked.
- **T026 readings**: `pytest tests/unit/test_concurrency_check_engine.py` → exit 4 (file not found); `pytest tests/contract/test_concurrency_declarations.py` → exit 4; `script-interface-check.py --files scripts/python/concurrency-check.py` → exit 1 (`candidate-not-collected`). These are the subject-absent reds at WP1 close; the owning packages (WP4/WP2) extend this entry with assertion-level reds and greens.
- **T002 baseline**: see `test-evidence/wp1-t002-baseline.txt`. Headline: the serial canonical run on the stable tree froze **161** failed ids into `notes/test-baseline.txt` (`suite-baseline-093.txt`, 706.93s). The first attempt (the row's literal `python3 -m pytest -q`, 163 names) overlapped the fact landing — four live-tree checks failed only there — and the parallel attempt (167 names) differs in 3–6 order-sensitive trigger/tuning tests from both serial runs; both comparison sets are recorded there, and GATE-1's normalization command is stated.
- **Regression-locality checks**: `tests/contract/test_harness_triple_structure.py` + `test_non_disposable_contract.py` + `test_non_disposable_check.py` → **207 passed** (run after the facts landed); `validate-tasks.py` → PASS 0 error / 0 warning.

## Design decisions taken under implement-time latitude

No earlier artifact fixed these; each is recorded here once and owned by the fact entry named.

1. **Class-to-root assignment** (`concurrency-class.yaml`). `concurrent-by-default` ← skills, commands; `partition-required` ← teams, anchoring (targets/seats are the units; a one-unit run is a recorded decision); `serial-only` ← agents (a definition's own advance is one executor run; no definition carries a dispatch tool, 14 forbid dispatching in prose). The decision rule keys on `(root_id, produced_shape)` using the E-1 unit vocabulary. The assignment is re-openable only by revising the fact — in particular, a T-004 `allow` ruling that grants coordinator dispatch tools would require an explicit revision, not an engine change.
2. **Shared-string registration** (C-055) lands inside `concurrency-contract.yaml`: `STR-001…STR-011` as id → owner pointers plus the closed-set rule. No literal is restated; the value stays with the named owner.
3. **`owner_anchor` sections** are declared as `shared/definitions/subagent-definitions.md#class-concurrent-by-default`, `#class-partition-required`, `#class-serial-only`; the implement rows that write the class obligations (T034–T036) must author exactly these sections. Until then T029's anchor-resolvability check is correctly red.
4. **`decomposition-coverage.yaml` stage defaults** re-judge FR-029: every stage becomes `auto` (decompose when the gate admits and the benefit test holds, else a recorded single-package decision) and `analyze` becomes `on` with N read from the stage configuration / `agent_concurrency_requested`. `decomposition-model.md` § 20.1 converges by revision (T140), not by a second owner.
5. **The serial-reason bijection scope** is condition-bound codes ↔ FR-005(b)–(e); FR-005(a)'s shortfall is the factual `single-unit` code, which FR-006 exempts from the bijection. The exemption is stated in the fact's `note`, not as a condition field (factual codes carry no condition).

## Corrections disclosed (Fast Fail, correction-class — repaired in passing)

1. **Stale frozen counts**: `tasks.md` T003/T005 and `research.md` R-1 record `facts` **23** and the `.specify/skills/` trap reading **16**; the tree measures **24** facts and **17** entries (16 flat external + `internal/`). Corrected by measuring, never inherited; no assertion depends on either number.
2. **T025 / GATE-5 command shape**: both quote `script-interface-check.py scripts/python/concurrency-check.py` (positional), while the tool selects candidates with `--files PATH[,PATH]` (the positional form exits 2 `unrecognized arguments`). Recorded in the red-first entry; the owning rows must use `--files`.
3. **Baseline-run overlap**: the first baseline run started before the facts were written and overlapped their landing; four live-tree checks (`test_coaching_wiring_contract` c3/c8, `test_compile_propagation_order::test_propagation_chain_is_green_in_canonical_order`, `test_non_disposable_contract::test_t089_a_full_run_is_byte_identical_on_git_status`) failed only in that window and pass on the stable tree. The authoritative baseline is the serial run on the stable tree.
4. **GATE-1 comparison shape**: the frozen baseline is the serial failed-id set (086 runner owner, 092 execution lesson 3). GATE-1's later run must normalize its `FAILED …` lines the same way (`sed 's/^FAILED //;s/ - .*//' | sort -u`) before `comm -13`; comparing raw prefixed lines against bare ids would report every failure as new.

## Residual risks

- **Anchor convergence**: three class-obligation anchors are declared but not yet authored; T034–T036 must create those sections, or T029 stays red for the right reason and then for the wrong one.
- **contract.yaml key set grew to 17**: no consumer asserted the nine-key set (checked `declaration_reader` consumers and the test tree), but a later contract that freezes the key count must account for the registration block.
- **Trigger/tuning suites are order-sensitive** in this tree (parallel vs serial runs differ by ~4–9 names). GATE-1 should compare like with like (serial vs the serial baseline).
- **`serial-only` over the whole `agents` root** is the largest single design bet; it is a fact value, so a T-004 `allow` ruling or a coordinator capability change is a one-file revision, and WP4's tests judge internal consistency rather than the literal class name.
- **C-016 remains unsatisfied** until the owner supplies `allow` or `forbid`; the engine's `owner-unavailable` path (C-039) is the intended fail-closed reading in the meantime.

## Register / write-domain note

`.specify/memory/register.md` was inside this package's write domain but no new durable identifier was
coined by WP1: the one residue (the unadjudicated verdict) is already carried by `F-093-003`, whose row
records that the value belongs to the [[STR-011]] owner. No register row was added, and nothing outside
the declared domain was written (the `.specify/shared/declarations/**` files are the engine-regenerated
mirror of the authored `shared/declarations/**` sources).
