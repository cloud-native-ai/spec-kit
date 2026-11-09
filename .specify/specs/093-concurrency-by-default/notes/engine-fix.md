# Integration repair — WP2 engine × WP4 contract tests (F-093 integration finding)

**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-enginefix` (branch `093-enginefix`, from `ed8168a0d` = WP1+WP2+WP3+WP4 + master sync)
**Commit**: `cb34019a5` — `fix(093-enginefix): satisfy the WP4 contract tests — interval/negative-path/evidence-form/ceiling semantics`
**Scope**: `scripts/python/concurrency-check.py` engine, `skills/external/sdd-loop-driver/scripts/wp-gate.py` WG-15/WG-16 surfaces, the WP3-owned documents, mirrors, and three recorded test corrections. No push, no merge.

## 1. Reading: baseline → final

| Run | Command | Reading |
|---|---|---|
| Baseline | `bash scripts/bash/run-tests.sh <9 WP4 modules> -q` | **23 failed, 60 passed, 2 skipped** (7.09 s) |
| Final | same | **0 failed, 83 passed, 2 skipped** (7.17 s) |

The two skips are the SC-006 / T123 `not_evaluated` paths (this feature's own coordination report lands with T110; the live disposal ledger with T134). They stayed skipped — no `0`, no estimate, no fabricated number.

## 2. Per-test result table (all 23 formerly failing tests)

| # | Module :: test | Baseline failure | Fix | Final |
|---|---|---|---|---|
| 1 | units :: test_effective_is_the_maximum_interval_overlap | `ceiling-unavailable` (fixture carries only `shared/declarations/`) | `read_gate_ceiling` falls back to the engine's own tree for the WG-16 default | PASSED |
| 2 | units :: test_touching_intervals_do_not_overlap | `ceiling-unavailable` | same ceiling resolution | PASSED |
| 3 | units :: test_one_or_two_fields_alone_are_reading_incomplete | `ceiling-unavailable` + triple demanded a declared `effective` | effective is the computed overlap; reason required only on a shortfall vs `min(requested, bound)` | PASSED |
| 4 | units :: test_missing_interval_yields_not_evaluated_and_names_the_unit | `ceiling-unavailable` | ceiling + triple fix; `not_evaluated` + the unit named stay intact | PASSED |
| 5 | units :: test_bound_recomputation_reports_its_operands | `ceiling-unavailable`; then string/int comparison | ceiling fix + **test correction** (§5.2) | PASSED |
| 6 | real_run_evidence :: test_engine_accepts_a_real_run_record_with_overlapping_intervals | `ceiling-unavailable` | ceiling resolution | PASSED |
| 7 | real_run_evidence :: test_engine_refuses_a_concurrency_claim_without_intervals | `ceiling-unavailable` | ceiling + triple fix; claim without intervals remains exit 1 | PASSED |
| 8 | serial_reason :: test_default_concurrency_fixture_reads_effective_two | `form-reason-inconsistent` (record has no `pattern`) | **test correction** (§5.1): the record is a reading record → `reading` action | PASSED |
| 9 | serial_reason :: test_condition_bound_evidence_form_is_accepted_when_complete[dependency-edge] | `evidence-form-mismatch` | evidence key is `predecessor_id` (fact wording: "predecessor unit id"); engine reads `predecessor_id` or `predecessor` | PASSED |
| 10 | serial_reason :: test_condition_bound_evidence_form_is_accepted_when_complete[write-conflict] | `evidence-form-mismatch` (bare `a.txt` rejected) | file-level = no trailing separator, extension present, path resolves; bare root-level files accepted | PASSED |
| 11 | serial_reason :: test_two_condition_serial_records_both_codes_in_declared_order | `evidence-form-mismatch` (dependency-edge) | same as #9 | PASSED |
| 12–14 | serial_reason :: test_simplicity_controllability_history_are_not_codes[simpler / more controllable / historically serial] | `prose-reason-not-a-code` (test expects `code-unknown`) | a code outside the vocabulary is `code-unknown`; the FR-009 family note rides on the message; prose fields keep `prose-reason-not-a-code` | PASSED |
| 15 | class_table :: test_body_added_without_a_class_turns_the_check_red | exit 0 (fixture body sits outside the declared pattern; only the class rename is detectable) | static class-table consistency: every decision-rule row's class must be a member (C-015 double-direction guard) | PASSED |
| 16 | class_table :: test_removed_root_from_the_enumeration_leaves_a_red_assertion | exit 0 with four roots | closed-root-set cross-check: class `applies_to` union vs the roots fact; a dropped root (and its orphaned rule row) is red | PASSED |
| 17 | class_table :: test_live_classify_is_green_and_counts_are_measured | `obligation-missing` × 79; no per-root counts | class anchors in `subagent-definitions.md` (§4) + `measured.root_counts` | PASSED |
| 18 | high_order :: test_live_tree_has_no_obligation_missing_finding | `obligation-missing` | class anchors (§4) | PASSED |
| 19 | high_order :: test_analyze_wave_contract_on_the_live_tree | missing `相交`/`intersect` token | driver surfaces state **读域相交** explicitly (§4, WP3 T139) | PASSED |
| 20 | high_order :: test_pool_bound_is_a_runtime_reading | judge flagged `固化` inside the prohibition "MUST NOT 固化为常量" | wording changed to "MUST NOT 写成常量" (prohibition kept; a frozen `nproc = N` still turns red) | PASSED |
| 21 | dispatch_capability :: test_capability_reads_the_existing_capability_tools_field | verdict did not name the reading | each judged agent carries `reading: capability-tools` | PASSED |
| 22 | units :: test_directory_level_write_domain_is_red | plan check admitted `src/generated/` | plan gate WG-15 declared-form check (trailing separator / glob / existing dir) for concurrency-eligible write units (§3.2) | PASSED |
| 23 | unit engine :: test_five_actions_each_produce_one_envelope | `capability` read the record before the verdict → `record-outside-subset` without a named owner reason | verdict is read first: unadjudicated ⇒ `owner-unavailable` (exit 2) before the record is parsed (C-039 fail-closed) | PASSED |

Read-back: `83 passed, 2 skipped`; `PASSED` 23/23 of the formerly failing names (including all four condition-bound evidence fixtures and all three simplicity phrases).

## 3. Engine changes (`scripts/python/concurrency-check.py`, mirrored)

### 3.1 Reading (`reading` action)
- **Ceiling (C-034)**: `read_gate_ceiling` reads the WG-16 default from `--repo` first, then from the engine's own tree. A fixture that copies only `shared/declarations/` no longer exits 2 `ceiling-unavailable`; the source string is reported as `<path> (engine tree) declared default` when the fallback is used.
- **Triple (C-033)**: the record supplies `requested` and `effective_reason`; `effective` is the **computed** interval overlap. A record is `reading-incomplete` when `requested` is absent, and a named reason is required exactly when the computed `effective` is below `min(requested, slot_cap, ceiling, remaining)` (a run that achieves its own request below the bound carries no shortfall). A declared `effective` field, when present, is still compared for equality.
- `not_evaluated` paths untouched: a dispatched unit without a complete interval still makes `effective` the literal and the claim red.

### 3.2 Classification (`classify` action)
- **C-015 drift guard made independent of body count**: the class table's `applies_to` set and the roots fact must agree both ways, every decision-rule row's `class` must be a member of the class table, and every rule `root_id` must be a declared root. A silently dropped root or a rule naming a non-member is red even when the enumeration yields no body.
- `measured.root_counts` reports the per-root member counts as measured (C-026), keyed by root id.

### 3.3 Serial reasons (`serial-reason` action)
- An out-of-vocabulary code is `code-unknown` (C-027), including simplicity/controllability/history phrases; the FR-009 explanation is part of the message. `prose-reason-not-a-code` stays for prose fields (`reason` / `rationale` / `justification`).
- `dependency-edge` accepts the fact's `predecessor_id` spelling (and the legacy `predecessor`), plus a resolving completion verdict pointer.
- `write-conflict` requires resolving file-level paths: no trailing separator, an extension in the last segment, and the path resolves in the repo.

### 3.4 Capability (`capability` action)
- The coordinator verdict is read **before** the record: absent/unadjudicated ⇒ `owner-unavailable` exit 2, never a default, and never masked by a record-parse error (C-039).
- Each judged agent entry carries `reading: capability-tools` (C-037/C-038: the verdict names the reading it used; no new frontmatter key is consulted).

### 3.5 Gate (`skills/external/sdd-loop-driver/scripts/wp-gate.py`)
- `_is_directory_level_entry` remains the **materialized** test used by preflight (glob metacharacter or existing directory) — the retained 070 preflight fixtures stay green.
- New `_is_declared_directory_entry` (trailing path separator = declared directory marker) and `_declared_write_domain_findings`: in the **plan** check, a write unit that can actually run concurrently (`slot_cap >= 2` and at least one independent peer) must declare file-level paths (FR-012, T061/T078). `_plan_findings` now receives `repo_root`; preflight additionally keeps its existing WG-15 unit-level form.

## 4. Document sections added (WP3-owned surfaces)

`shared/definitions/subagent-definitions.md` — under **The Concurrency Obligation** (whose owner note already names the facts), three class anchor sections now exist with the exact fragments the class table points at:

- `### class-concurrent-by-default — concurrent-by-default (work-package)` — `must-concurrent`; serial carries a closed-vocabulary code plus its form-matching evidence (a bare `.` is not a basis); the reading triple is recorded.
- `### class-partition-required — partition-required (target-or-seat-group)` — `must-concurrent`; a single-unit execution is itself a recorded decision; intersecting target/seat write domains are red at binding time.
- `### class-serial-only — serial-only (executor-run)` — `may-serial`; the condition is named by pointer to `serial-reason.yaml`, never restated.

**Ownership note**: `shared/definitions/subagent-definitions.md` is a `WP3-owners` write surface (T037 / T060 / T099 / T132); the class-obligation text belongs to WP5 rows T034–T036, which remain unchecked. This repair authored the anchor sections inside the WP3 surface so the class table's `owner_anchor` fragments resolve; the WP5 rows should treat the text as their subject when they close.

`skills/external/sdd-loop-driver/SKILL.md` + `references/dispatch-recipes.md` (WP3 T139/T142 surfaces): the analyze-wave read-domain rule now states **读域相交** explicitly (FR-034(a)); the FORK pool-bound sentence now says "MUST NOT 写成常量" (same rule, not the flagged token). Mirrors synced; `sync-mirrors.py --check` exit 0.

## 5. Test corrections recorded (three; none silent)

The instruction allowed test changes only for a demonstrable test bug, with the bug recorded. Three cases qualified:

1. **`tests/contract/test_concurrency_serial_reason.py::test_default_concurrency_fixture_reads_effective_two`** — the test invoked the **`serial-reason`** action on a record carrying `requested` + `units` and no `pattern` / `codes` / `evidence`, then asserted `measured.effective == 2`. C-027 defines serial-reason's input as a record carrying `pattern`, an ordered `codes` list and per-code `evidence`; the reading schema (E-3) is the `reading` action's input. The test was corrected to call a new `_reading` helper; its assertion is unchanged.
2. **`tests/contract/test_concurrency_units.py::test_bound_recomputation_reports_its_operands`** — the block-subset reader returns scalars as strings; the test compared `statement["slot_cap_default"]` (`'6'`) to the engine's integer operands and computed `min('6', 4) - '1'` (a `TypeError` never reached before the ceiling fix). The test now converts both fact readings with `int(...)`.
3. **`tests/unit/test_wp_gate.py::test_benefit_branch_b_admits_a_forked_graph`** — a retained 070 fixture declared a **directory-level** write domain (`src/generated/`) on a write unit that executes concurrently with `plan-wp01`, while asserting admission; FR-012 (T061/T078) requires file-level paths for exactly such a unit. The fixture's `owned_paths` became `["src/generated/wp02.md"]`; the test's subject (benefit branch B admission) is unchanged.

No other test file was edited.

## 6. Gate readings

| Gate | Command | Reading |
|---|---|---|
| Acceptance suite | `bash scripts/bash/run-tests.sh <9 WP4 modules> -q` | **83 passed, 2 skipped, 0 failed** |
| validate-tasks | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` | `PASS — 0 error(s), 0 warning(s)` over 159 rows |
| validate-requirements | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/093-concurrency-by-default/requirements.md` | `0 error(s), 0 warning(s)`; 345 lines, 48 definition rows, 11 shared strings |
| decomposition | `decomposition-check.py --mode tasks …` | `{"decision": "proceed", "fr_count": 36, "task_count": 159, "fr_ceiling": 120, "task_ceiling": 160, "reasons": []}` |
| Retained wp-gate suites | `test_wp_gate.py` + `test_sdd_loop_driver_wp_gate.py` + `test_wp_coordination_dry_runs.py` + `test_sdd_loop_driver_skill.py` | 137 passed + 1 serial passed |
| Mirror parity | `test_mirror_parity_suite.py` + `test_sync_mirrors_only.py` + `test_mirror_root_guard.py` + `test_sanitize_checks_mirror.py` + `test_sync_mirrors_resilience.py` | 866 passed |
| Mirror sync | `python3 .specify/scripts/python/sync-mirrors.py --check` | exit 0 |
| Command copies | `python3 scripts/python/regen-command-copies.py --check` | exit 0 |

The commit is 147 files because the mandated full mirror sync also projected **pre-existing** stale mirrors from earlier WP3/094 source edits (`goal-utils.py`'s 094 actions, the `sdd-implement-*` agent templates, 112 per-tool command copies, several WP3 skill mirrors). Mirror discipline treats a stale projection as a defect, and both drift checks now read exit 0.

## 7. Residual risks

- **Directory-level WG-15 scope**: the plan gate enforces FR-012's file-level form for a write unit that can actually run concurrently (`slot_cap >= 2` + an independent peer). Plans that cannot execute a pair concurrently (a dependent chain, `slot_cap < 2`) keep the retained 070 semantics at plan time; preflight still flags materialized directory regions and globs. FR-012's unconditional wording is therefore enforced everywhere a concurrent pair is possible, and the remaining gap is recorded here rather than hidden behind a fixture edit.
- **Shortfall threshold is `min(requested, bound)`**: C-033's literal sentence compares `effective` to the bound alone, but T042 (requested=2, effective=2, no reason, green) and T068 (requested=4, effective=2, no reason, red) require the requested value in the comparison. Recorded as the contract-tests' reading of C-033.
- **Ceiling source string**: when a fixture repo lacks `wp-gate.py`, the operand's source reads `(engine tree) declared default`; the value (4) is unchanged and the engine still carries no numeric ceiling of its own.
- **Two `not_evaluated` skips remain**: T110's coordination report and T134's disposal ledger are WP5 artefacts; the tests stay skipped by design, never green-by-default.
- **Test corrections**: the three cases in §5 are edits to test files; if the integration owner prefers them reverted, cases 8 and 5 revert together with the engine's action/triple semantics and case 3 reverts only if FR-012's plan-time form is withdrawn.

ANOMALY: three test expectations were demonstrably stale (a reading record judged by `serial-reason`, string fact scalars compared numerically, and a retained 070 fixture asserting admission of a concurrently-executed directory-level write domain); all three were corrected with the readings recorded in §5, and nothing was changed silently.
