# Review — segments C (implementation) + D (code) — 093-concurrency-by-default

**Role**: independent reviewer, segments C (implementation verification) and D (code), SDD review wave
**Tree**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-review` — branch `093-review` @ `46bcb8716`
**Feature diff**: `git diff 6a87db2b6f05df4eb688f876688a8cd12b2a0635..HEAD` (merge-base `master..HEAD`)
**Date**: 2026-11-10 (session readings dated 2026-11-09 UTC) · **Mode**: read-only; the only write is this file.

Provenance note used throughout: `6a87db2b` already carries the 094 scope-vocabulary rename, and the two
`master` merges (`95e44f3ac`, `ed8168a0d`) bring later 094/090 content into the range. Per-file `git log`
separates 093's own work (engine, facts, driver edits, new tests) from that inherited content; the review
judges only the former as 093's code delta.

---

## Segment C — implementation verification

### C.1 Acceptance suite re-run (the retained command, run unchanged)

First line of `test-evidence/wp5-acceptance-final.txt`, re-run through the mandated runner:

```
bash scripts/bash/run-tests.sh tests/contract/test_concurrency_declarations.py \
  tests/contract/test_concurrency_class_table.py tests/contract/test_concurrency_serial_reason.py \
  tests/contract/test_concurrency_units.py tests/contract/test_concurrency_high_order.py \
  tests/contract/test_concurrency_dispatch_capability.py tests/contract/test_concurrency_disposal.py \
  tests/contract/test_concurrency_real_run_evidence.py tests/contract/test_concurrency_reproduction_092.py \
  tests/contract/test_test_entry_guard.py tests/unit/test_concurrency_check_engine.py -q
```

Reading: **96 passed in 7.12s, exit 0** (retained artifact: 96 passed / 7.14s). The smoke record's
`smoke_exit_code=0` and "96 passed / 0 skipped" both reproduce. No skips fired.

Supporting gates re-run independently:

| Gate | Command | Reading |
|---|---|---|
| GATE-1 name set | recomputed from `wp5-suite-final.txt` vs `notes/test-baseline.txt` | 207 `FAILED` lines, 161 baseline names, **46 NEW**; the 46-name set is byte-identical to `wp5-gate1-comparison.txt`'s list (`diff` → identical); zero names mention concurrency |
| GATE-2 | `python3 scripts/python/sync-mirrors.py --check` / `python3 scripts/python/regen-command-copies.py --check` | exit 0 ("ok shared/ == .specify/shared/ (110 files, byte-identical)") / "OK: all per-tool command copies match the source templates." |
| compile-embeds | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` (no standalone `compile-embeds` script exists; the probe action is the sanctioned path) | `compile-embeds --check: 79 units, zero drift`, exit 0 |
| GATE-6 | `python3 .specify/scripts/python/validate-tasks.py …/tasks.md` / `validate-requirements.py …/requirements.md` | PASS 0 error / 0 warning (159 rows); 0 error / 0 warning (345 lines / 48 definitions / 11 strings) |

### C.2 GATE-1 attribution method, verified

Method reproduced: failure-**name**-set diff against the frozen serial baseline, then per-name
classification. My independent spot checks of the "44 master-inherited" sample:

- `test_run_checks::test_c1_the_action_exists_and_the_roster_grew_by_exactly_one` — fails on
  `len(actions)` 18 vs 11 (094's `resolve-scope`/`run-checks` roster growth), not on anything 093 added.
- `test_nested_run_report::…goal_field_set…` — fails on 090's `binding_block` Goal field.
- `test_expression_gate_wiring::test_a6_wiring_set_is_closed` — `templates/commands/feedback.md →
  flow-class-check.py`; the token is absent on the branch pre-second-merge (`ed8168a0d^1`) and present at
  HEAD, i.e. reintroduced by the master merge, not by a 093 feat commit.
- `test_goal_scope_engine::test_spec_scope_paths` — `resolve_scope(..., "spec")` is outside the base tree's
  `ARCHIVE_SCOPES = ("goal","teams","auto")`; the test asserts the pre-094 vocabulary.
- `test_coaching_wiring_contract::test_c1…` — `coaching-skills <trainee-name|trainee-path> <work>` call-form
  mismatch exists at the base commit too; 093 only edited the skill's `## Boundaries` section.

Substantive conclusion confirmed: **zero NEW 093-caused failure names**. The 2 trigger-order names are the
recorded serial-vs-parallel caveat.

### C.3 SC-by-SC evidence table

| SC | Claimed | Retained artifact(s) | Independent check | Result |
|---|---|---|---|---|
| SC-001 | pass | `tests/contract/test_concurrency_class_table.py`, `wp5-t034-t040-*`, `wp5-t028-t043-t045-*` | ran `concurrency-check.py classify --repo .`: `decision=pass findings=0`; root counts exactly **agents 17 / anchoring 6 / commands 29 / skills 54 / teams 12**, 118 bodies; mutation file shows both drift mutations red | confirmed |
| SC-002 | pass | named tests in `test_concurrency_serial_reason.py` / `test_concurrency_high_order.py` | both tests exist, pass in the re-run; the second mutates the fact to `coverage: off` and the judge reddens | confirmed |
| SC-003 | pass | `test_concurrency_serial_reason.py` (10 tests), `wp5-t028-t043-t045-*` § D–G | closed vocabulary, per-code evidence forms, both C-030 directions, bijection mutations both ways all read red in the retained output | confirmed |
| SC-004 | pass | `test_concurrency_units.py` (11 tests), `wp5-t062-t085-*` | seven obligations each carry a fixture; the "168 passed" reading is the retained 070 modules `test_sdd_loop_driver_wp_coordination.py` + `test_sdd_loop_driver_wp_model.py` | confirmed (attribution nit C-3) |
| SC-005 | pass | `test_concurrency_reproduction_092.py`, `wp5-t090-*` | module 4 passed; retained reading shows pre-repair copy `decision=pass` exit 0 vs repaired `decision=fail` exit 1 with two `declaration-execution-mismatch` | confirmed |
| SC-006 | blocked | `notes/coordination-report.md`, `notes/serial-baseline.md`, `wp5-t110-t112-*` | report reads `effective: not_evaluated`, reason `mechanism-not-yet-landed`, duration `not_evaluated`, six real units recorded, 091 baseline cited; five `SC-006_*` keys present; `blocked` is a legal vocabulary member | **honest**, no overclaim |
| SC-007 | partial | `wp5-t110-t112-*`, `wp2-t109-t113-t119.txt` | goal partition fixture measured (5 targets → `[3,2]` at ceiling 4; ceiling 2 → serial `budget-reserve`); team/loop only documented — the row says exactly that | honest partial |
| SC-008 | pass | `wp5-t110-t112-*`, `tests/contract/test_concurrency_check_engine.py` | ran `coverage --repo .`: `decision=pass`, 8/8 stages (`analyze` = covered/on, rest covered-by-default), bound 6/4/1 → available 3 | behavior confirmed; **evidence pointer broken** (C-2) |
| SC-009 | pass | `wp5-t017-t019-*`, `test_concurrency_declarations.py` (T017/T019) | live `capability` run → `owner-unavailable`, exit 2, named message; absent/broken/unparsable forms all exercised as engine runs | confirmed |
| SC-010 | partial | `notes/disposal-ledger.md` (12 rows), `wp5-gate1-comparison.txt`, `wp5-suite-final.txt` | ledger domain test passes; 12 rows, four-value domain, pointer/daté rows resolve; GATE-1 recomputation holds | confirmed partial (headline defect C-1) |
| SC-011 | pass | `test_concurrency_high_order.py::test_anti_nesting_chain_is_depth_two_with_its_three_prohibitions` | depth-2 + three prohibitions pinned; the tamper mutation reddens the judge | confirmed |
| SC-012 | pass | `tests/unit/test_concurrency_check_engine.py::test_cost_benefit_fixture…` | fixture-form by design (SC-012 itself says "在夹具上"); identical result set, lower wall clock | confirmed as a fixture claim |

### C findings

- **C-1 (important) — GATE-1 headline contradicts the artifact it cites.** `wp5-gate1-comparison.txt`
  line 6 reads `211 failed, 8252 passed, 2 skipped, 576 warnings in 49.96s`; the retained
  `wp5-suite-final.txt` reads `207 failed, 8256 passed, 2 skipped, 576 warnings in 49.90s` (and
  `verification.md` / `notes/implement-wp5.md` both use 207/8256). The 46-name list and its classification
  are correct (independently recomputed), so only the summary line is stale. Fix the line and name which
  run it came from.
- **C-2 (important) — SC-008's evidence pointer does not resolve.** The row cites
  `tests/contract/test_concurrency_check_engine.py`; no such file exists (the module is
  `tests/unit/test_concurrency_check_engine.py`), and that module only asserts envelope shape while
  accepting exit codes 0/1/2 for the coverage action. The SC-008 behavior itself reproduces (live run
  above), but the row's test citation overstates what a test pins (see D-I3).
- **C-3 (nitpick) — "168 model tests green" attribution.** In the SC-004 row the 168 tests belong to the
  retained 070 model suites, not to the seven 093 obligation fixtures; the row reads as if they are the
  same evidence. Split the pointer.

**Segment C verdict: PASS with two evidence-record repairs (C-1, C-2) and one wording nit (C-3).**
Every `SC-*_status=` value reproduces against a retained, re-runnable artifact; SC-006's `blocked` is the
honest reading (no real run with `effective >= 2`; nothing written as `0` or an estimate); no criterion
overclaims its own status — the two defects are in the records, not in the behavior.

---

## Segment D — code review

### D.1 Delta and method

093's own code delta (new files unless noted):

- `scripts/python/concurrency-check.py` — 1534 lines, new engine; mirror `.specify/scripts/python/concurrency-check.py`
  is byte-identical (`sha256 fa150dfd…`).
- `shared/declarations/facts/` — eight new facts (`concurrency-class`, `serial-reason`, `effective-concurrency`,
  `concurrency-slot-and-reserve`, `decomposition-coverage`, `executor-enumeration-roots`,
  `concurrency-contract`, `coordinator-dispatch-verdict`) + `contract.yaml` registration block; mirrors byte-identical.
- `skills/external/sdd-loop-driver/` — `SKILL.md`, `references/{decomposition-model,dispatch-recipes,stage-prompts,watch-model}.md`,
  `templates/stage-team-preset.md`; `scripts/wp-gate.py` +100 (WG-15 write-domain arms).
- `shared/definitions/subagent-definitions.md` (+71: the Concurrency Obligation owner section, the carrier
  ban, Dispatch Capability), `agent-definitions.md`, `goal-definitions.md` (Target concurrency),
  `shared/workflow/{execution-topology,external-dispatch-recipes}.md`; `scripts/python/validate-tasks.py`
  (+39: `[green:]` marker semantics + `build_parser`).
- Consumer skills: `run-team`, `create-team` (+`conceptual-model`), `implement-feature`, `run-agent`,
  `coaching-skills`, `create-skills`, `merge-skills`, `sdd-house-keeping`, `sdd-project-setup`.
- Templates: 29 command templates + plan/tasks/instructions templates (one authored pointer block each).
- Tests: 9 new concurrency contract modules + 1 unit module + `test_test_entry_guard.py` +
  `test_validate_tasks_green_semantics.py`; 10 existing modules re-pinned.

Not 093's work in the same range: the `.specify/scripts/python/goal-utils.py` mirror catch-up (+238, source
unchanged in `base..HEAD`), and the 094-family test reds — both inherited through the master merges.

Method: full read of the engine and all eight facts; every new/re-pinned test module read; the engine's five
actions exercised against the live tree and against negative fixtures; `git log`/`git show` provenance for
each contested surface; cross-check against the already-landed 094 binding model (`goal-definitions.md`
§ Goal–Team binding is static; `run-team`/`create-team` now carry pointer obligations only — no second model,
no rebinding, no contradiction).

### D.2 Six-level findings

#### Blocking

- **D-B1 — The user-facing driver/setup docs still state the disposed rule, and the guards that pinned
  them were dropped instead of re-pinned.** `docs/reference/skills/sdd-loop-driver.md` (line 3 "本地用宿主
  原生子代理"; line 16 "宿主原生子代理（不启动 qodercli）"; line 20 "MUST NOT 启动 qodercli") and
  `docs/reference/skills/sdd-project-setup.md` (lines 16, 61) still document the pre-093 local topology.
  FR-035 orders the conflicting rule sets to converge by explicit revision and says they "MUST NOT 让两套
  规则静默并存"; the disposal ledger has no row for these two pages. At the same time
  `tests/contract/test_sdd_loop_driver_skill.py` (C-23) and `tests/contract/test_sdd_project_setup_skill.py`
  removed their `docs`-page assertions instead of re-pinning them. Net effect: the shipped owner documents
  (correct) and this repository's user-facing docs (stale) contradict each other, and the regression guard
  that would have caught it was silently removed — a guard weakening, not a re-pin.
  *Fix*: update the two pages to the fork/subprocess carriers + in-process ban (or add a dated-record
  disposal row **and** keep the page accurate), then re-pin the docs assertions in both modules.

#### Important

- **D-I1 — `mechanism-not-yet-landed` evidence is governed by an undeclared key and a hardcoded code
  literal.** `scripts/python/concurrency-check.py:671-674` requires `evidence.missing_mechanism` for that
  code, but `shared/declarations/facts/serial-reason.yaml` only says "the enumerated unit set plus the named
  missing mechanism" and never names the field; the engine also hardcodes the code literal
  `"mechanism-not-yet-landed"`, contradicting its own docstring (line 22: "no … code vocabulary … carried in
  this file as a second definition") and the fact header's "MUST NOT carry a code literal of its own".
  Verified end-to-end: the suite's own `_valid_record` fixture for this code
  (`test_concurrency_serial_reason.py:122-128`, key `mechanism:`) is **refused** (`evidence-form-mismatch`,
  exit 1) and no test exercises the accepted spelling. A record that follows the suite's fixture is red for
  a reason the owner never declared.
  *Fix*: put the extra required field in the fact (e.g. `evidence_extra_field: missing_mechanism`) and read
  it, or accept both spellings; add a positive fixture for the factual code.
- **D-I2 — A malformed `units` field is silently accepted as "no units".**
  `concurrency-check.py:904` (`unit_list = units if isinstance(units, list) else []`) lets a record with
  `units: "not-a-list"`, `requested: 2`, `pattern: concurrent` and any `effective_reason` return
  `decision=pass`, exit 0, `effective=0` (probed). No `record-malformed` finding is emitted, so C-032's
  "a claim that asserts concurrency MUST NOT pass" is bypassed by hiding the units.
  *Fix*: emit `record-malformed` when `units` is present and not a list.
- **D-I3 — The coverage action's red arms have no committed test (FR-030).** `coverage-undeclared`
  (unknown stage / `off` without decision), `fourth-source`, and the goal-partition arithmetic are exercised
  only by manual readings (`wp2-t109-t113-t119.txt`) and one envelope-shape unit case that accepts exit 0/1/2
  (`tests/unit/test_concurrency_check_engine.py:140-187`). C-035/C-036 are decidable assertions; FR-030
  requires a contract- or unit-level test that goes red when the implementation regresses. This is the same
  gap C-2 shows from the evidence side.
  *Fix*: add the three red fixtures (mutated fact / competing authored rule / partition under `--ceiling`) to
  the contract module and point SC-008 at them.

#### Suggestions

- **D-S1 — Conditional skips survive after the artifacts landed.** `test_concurrency_disposal.py:168-175`
  and `test_concurrency_real_run_evidence.py:242-254` still `pytest.skip` when the ledger/report is absent;
  now that both exist the skip can never fire, so a future deletion would silently skip instead of failing.
  Replace with hard assertions (`rows` / `candidates` non-empty).
- **D-S2 — `write-conflict` evidence rejects extension-less file paths.** `concurrency-check.py:637-644`
  requires a `.` in the last path segment and a resolvable file, so a legitimate `Makefile`/`LICENSE`
  intersection cannot be recorded. Use "not ending with `/` and resolves to a file" instead.
- **D-S3 — No interval-order validation.** `maximum_overlap` (lines 843-859) treats `settled_at < dispatched_at`
  as an ordinary interval; probed record → `effective=0`, `decision=pass`, no finding. Add an
  `interval-inverted` finding (conservative today, but it can hide real overlap).
- **D-S4 — Declaration-owned literals duplicated in the engine.** `NOT_EVALUATED = "not_evaluated"`
  (line 822) duplicates `effective-concurrency.yaml`'s `not_evaluated_literal`; the `budget-reserve` fallback
  in `action_coverage` (line 1267) duplicates a vocabulary member. Read them from the facts like the rest.
- **D-S5 — The positive acceptance assertion is weakened.** `test_five_actions_each_produce_one_envelope`
  accepts `returncode in (0, 1, 2)` for a valid `single-unit` serial record; it should assert `0` for that
  case and reserve 1/2 for the explicitly named negative fixtures.
- **D-S6 — Two write-domain arms with different scopes.** Plan-time `_declared_write_domain_findings`
  (`wp-gate.py:1085`) reddens a directory-level domain only when `slot_cap >= 2` and an independent peer
  exists, while preflight `_write_domain_findings` (line 1116) reddens unconditionally — but FR-012 is
  unconditional. The new `write-domain-empty` code is never asserted by any test (the empty-domain case is
  caught by the retained `kind-mismatch` first). State the intended asymmetry and pin both codes.
- **D-S7 — `--goal <unknown>` is silently empty.** `action_coverage` filters goals by slug and returns an
  empty report with no finding, asymmetric with `--stage`'s `coverage-undeclared`. Add a named finding or
  document the filter semantics.
- **D-S8 — Handoff detection has no negation handling.** `HANDOFF_MARKERS` (line 85) are substring-matched in
  the body, so "no handoff is used" classifies as `handoff-declared`; C-037 permits the marker test, but
  FR-021(b)'s "capable superior + declared form" is thereby reduced to a word hit. Consider requiring the
  handoff sentence to name its recipient and form.
- **D-S9 — The C-094 in-process ban is not machine-decidable at record level.** The only executable judge is
  a test-local helper (`test_concurrency_high_order.py:274-287`); a run record cannot even state its
  mechanism, so an in-process fan-out recorded with overlapping intervals would read as concurrency.
  Consider adding `mechanism` to the reading record schema (data-model E-3) and judging it against the two
  carriers.

#### Nitpicks

- **D-N1 — `excluded_layers` are structurally inert.** Every root's pattern already restricts enumeration to
  a non-projection base (`skills/{internal,external}/`, `templates/commands/`, `agents/`, `.specify/teams/`,
  `.specify/anchoring/`), so `.specify/skills/`, `.claude/commands/`, `.specify/agents/templates/` etc. can
  never be members; the `<id>` placeholders can never match a literal path. Harmless defence, but untested
  and misleading as written.
- **D-N2 — `SIMPLICITY_FAMILY` is broader than FR-009.** The regex (line 579) also rejects prose containing
  speed/faster/clean/cleanliness/更快/速度, which FR-009 does not name.
- **D-N3 — `read_gate_ceiling` parses wp-gate.py source text.** The regex is brittle to formatting changes;
  the failure mode is loud (exit 2 `ceiling-unavailable`), so this is a maintainability note only.
- **D-N4 — `test_entry_guard`'s scanner is prose-tolerant by construction.** The "raw invocation" regex does
  not catch a bare `pytest` followed by a plain path word without a slash/dot (e.g. `` `pytest tests` `` is
  caught, but a bare command with only a directory word and no flag is not); acceptable given FR-036's
  enumerated forms, worth a comment.

#### Questions

- **D-Q1 — Authority of the `validate-tasks.py` relaxation.** The `green-clause-collision` rule moved from a
  totality reading to a marker/strict-subset reading under F-093-004, a feature-local analyze ruling, applied
  to a framework-wide validator. It is warning-level, recorded, and tested (C-5), so this is a question of
  whether a framework semantics change belongs to this feature rather than a defect.
- **D-Q2 — Should C-094 become a record field?** See D-S9: making the mechanism explicit would turn the ban
  from documented policy into a decidable judgement without a second rule set.

### D.3 Test-intent table (rewritten modules)

| Module | Change | Intent preserved? | Note |
|---|---|---|---|
| `test_sdd_loop_driver_skill.py` | C-23 re-pinned to fork/subprocess + ban; old-rule phrases asserted absent | yes (stronger on the new rule) | **docs-page assertions dropped rather than re-pinned → D-B1** |
| `test_sdd_loop_driver_wp_coordination.py` | SD-07: `"qodercli" not in model` → carriers + ban; 070 simulator retained | yes | replacement pin, not a weakening |
| `test_sdd_loop_driver_wp_preset.py` | ST-02/ST-12: `== 6` → `projection-of` + fact read | yes (asserts no second numeric site) | genuine re-pin |
| `test_stage_class_wiring.py` | 9 SHA-256 re-pins with dated justification | yes | strip-restores-pin subject unchanged; passes |
| `test_coaching_run_contract.py` | C-12 carrier re-pin; old fallback framing absent | yes | — |
| `test_sdd_carrier_contract.py` | whole module re-pinned to the two carriers + ban + old-rule absence | yes | adds negative guards |
| `test_sdd_house_keeping_skill.py` | old qodercli prohibition → carriers + ban | yes | — |
| `test_sdd_project_setup_skill.py` | local-default test re-pinned; docs assertion dropped | mostly | **docs assertion dropped → D-B1** |
| `test_validation_carrier_contract.py` | driver carve-out re-pinned | yes | — |
| `test_wp_gate.py` / `wp_fixtures` | directory-level → file-level write domains | yes | matches FR-012 |

No `xfail`, no unconditional `skip`, no weakened assertion found beyond D-B1 and the residual D-S1 guards.

### D.4 Cross-line consistency with the landed 094 binding model

- `goal-definitions.md`'s new § Target concurrency advances independent Targets concurrently without touching
  the static team↔Goal binding, run-level single-Target selection, or identity resolution — the 094 binding
  model is unchanged. `run-team`/`create-team` add pointer obligations and a binding-time territory judgement,
  not a second roster or registry model.
- The 44 inherited reds are 094 vocabulary drift inside the branch line, not a conflict with 093's rules. The
  one real conflict with 094-era content is the stale-docs issue in D-B1, where 093 changed the rule but two
  user-facing pages still assert the old one.

**Segment D verdict: PASS WITH REPAIRS.** No blocking defect in the engine: it is declaration-driven, fails
closed (`owner-unavailable` exit 2), carries no numeric ceiling, and its CLI surface reproduces C-019/C-021/C-022
exactly. The blocking items are documentation/guard (D-B1); the important items are one undeclared
evidence key + hardcoded code literal (D-I1), one false-green path (D-I2), and one FR-030 test gap on the
coverage action (D-I3). Suggestions and nitpicks are non-blocking.

---

**Anomaly line**: one blocking anomaly (D-B1 — the two user-facing docs still state the disposed local-native
rule while their guard assertions were removed rather than re-pinned) and three important anomalies (D-I1
undeclared `missing_mechanism` key + hardcoded code literal, D-I2 malformed `units` false-green, D-I3 coverage
red arms untested) are surfaced, not repaired — this review is read-only; no fast-fail decision is requested,
and the two evidence-record defects in Segment C (C-1, C-2) are likewise surfaced for the release record.

RV093-2-DONE
