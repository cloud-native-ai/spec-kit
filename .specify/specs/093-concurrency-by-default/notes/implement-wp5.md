# Implement — WP5-release (feature 093-concurrency-by-default)

**Package**: `WP5-release` (`tasks.md` § Work Packages) — rows **T017, T019, T028, T034–T036, T038–T040,
T043, T045, T058–T059, T062–T065, T079–T085, T088, T090, T093, T099, T101–T105, T108, T110–T112,
T116–T118, T124, T126–T128, T130–T131, T133–T134, T137** (49 rows).
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-wp5` · **Branch**: `093-wp5` · **Base**: `6001c9ad1`
(WP1–WP4 + enginefix) · **Date**: 2026-11-09 · **Mode**: one detached fork worker, serial, no subagents,
no push, no merge.

**Outcome**: **49 of 49 rows closed.** The release tree is green on every 093-owned surface; the two
WP4 modules that skipped on `not_evaluated` (T110's report, T134's ledger) now run and pass, and the
acceptance suite reads **96 passed / 0 skipped**. The closure checker's verdict is `block` with one
reason — **SC-006** — which is the feature's honest `not_evaluated` state, not missing work.

## Commits (oldest first)

| Commit | Content |
|---|---|
| `b2f9589ab` | release-wave documents (dispatch capability, falsifiability, brief/return/coordinator obligations, slot/ceiling pointers, preset obligation), the re-pinned assertions, and `test_concurrency_reproduction_092.py` + the T017/T019 assertions |
| `51dd8d37c` | the release readings (`test-evidence/wp5-*`), the coordination report, the serial baseline, the disposal ledger, the quickstart run record and `verification.md` |
| _(this commit)_ | this record |

## Per-row closure

| Row(s) | Status | Evidence / reading |
|---|---|---|
| T017 (C-011) | closed | `test_concurrency_declarations.py::test_unregistered_slug_reads_owner_unavailable_with_a_named_message`; reader exit 1 → engine exit 2 `owner-unavailable`, named message (`wp5-t017-t019-owner-unavailable.txt`) |
| T019 (C-013) | closed | `::test_removed_fact_never_falls_back_to_a_default`; broken `fact:` key and unparsable body both refuse, no default |
| T028 (C-015) | closed | drift-guard mutations: add-without-class → `class-unknown` fail; root removed → `uncovered` fail (`wp5-t028-t043-t045-mutations.txt`) |
| T034–T036 | closed | the three class anchors in `subagent-definitions.md` verified against C-045/C-046/C-047; T029's anchor-resolvability tests green (`wp5-t034-t040-class-obligations.txt`) |
| T038 (C-043) | closed | the obligation section and the command pointer blocks carry no tuning number; class anchors' only digits are an FR id |
| T039–T040 | closed | the four-grain pointer table; 29/29 command surfaces carry the authored pointer; live classify pass, 0 `obligation-missing`, 118 bodies measured |
| T043 (C-028) | closed | bijection mutations both directions → `bijection-gap` naming FR-005(e) / FR-005(d) |
| T045 (C-030) | closed | concurrent-with-codes and serial-with-none both `form-reason-inconsistent` |
| T058 | closed | a code whose evidence belongs to another condition is reported naming code + condition + evidence pointer; nothing preferred (`wp5-t058-t059-reserve.txt`) |
| T059 / T079 | closed | the slot fact owns `verifier_reserve` + `reserve_deduction` + `degradation_rule`; the engine recomputes 6/4/1 → available 3; ceiling 1 → available 0 → goal serial with `budget-reserve` |
| T062/T080 · T063/T081 · T064/T082 · T065 | closed | the obligation's per-unit reading, the coordinator's package+shape obligation, the falsifiability sentence (C-057), the partial-settlement rule — all present and pinned (`wp5-t062-t085-unit-obligations.txt`) |
| T083 · T084 · T085 | closed | readiness = recorded verdict + evidence pointer with the partition rule pointed at the class fact; integration order = declared order with replay equality; re-entry from records with the ledger-derived re-dispatch count |
| T088 | closed | absent fact → exit 2 `owner-unavailable`; unadjudicated live fact → same; adjudicated fixture → verdict reported verbatim (`wp5-t088-coordinator-verdict.txt`) |
| T090 | closed | `tests/contract/test_concurrency_reproduction_092.py`: the 092 shape accepted by a pre-repair engine copy (exit 0) and refused by the repaired engine (exit 1, two `declaration-execution-mismatch`) |
| T093 | closed | `STR-012` added without an owner → the closed-set judge red (`string-set-changed` + `owner-missing`) |
| T099 | closed | the `## Dispatch Capability` section (STR-004 literal, four verdict forms, depth-2 pointer); engine reads `capability-tools` only (`wp5-t099-dispatch-capability.txt`) |
| T101–T105 | closed | driver SKILL bullets (partition-first, real shape, per-dispatch pass-down) + the dispatch-governance paragraph (brief carries the obligation, return carries the triple) (`wp5-t101-t105-coordinator.txt`) |
| T108 | closed | fabricated-number judge red on `0` and `"~20"`; `not_evaluated` green; cost-benefit result-set identity test green (`wp5-t108-fabricated-number.txt`) |
| T110 | closed | `notes/coordination-report.md` — `effective: not_evaluated`, `mechanism-not-yet-landed`; the live report test now passes |
| T111 | closed | `notes/serial-baseline.md` — 62 tasks / 1 agent / 116 minutes cited from the recorded 091 run, never re-measured |
| T112 | closed | the coverage action records each goal slice's per-stage coverage (resolved through the fact) and lists only open targets as packages — no hollow coverage claim (`wp5-t110-t112-coordination-coverage.txt`) |
| T116 (C-068) | closed | the preset carries one obligation paragraph and two `projection-of` lines; seat structure unchanged (`wp5-t116-t118-team-loop.txt`) |
| T117 (C-070) | closed | the driver bullet: per-stage coverage, no inheritance, per-unit reading (stage/package, entry, step — never "per round") |
| T118 (C-035) | closed | the explicit per-stage-default sentence in the decomposition model; live coverage resolves all 8 stages |
| T124 (C-082) | closed | the numeric slot cap now appears only in the fact (scan) and the ceiling only in `wp-gate.py`'s default; four prose sites are pointers (`wp5-t124-t134-owners.txt`) |
| T126 (C-084) | closed | fact `spine_relation` says projection; the engine reports `relation: projection` and `slot_cap_matches_fact: true` for the 093 spine; dated-record rows carry date + reason |
| T127 | closed | every fact `kind` ∈ the existing five-member set; kind-assignment tests green |
| T128 | closed | pre-093 key set (16561f2ad) vs current: 9 existing keys untouched, the 8 slug keys appended (plus `registered_facts` from 094's master sync) |
| T130 | closed | `sync-mirrors.py --check` exit 0 against the frozen baseline; `regen-command-copies.py --check` exit 0 (`wp5-t130-t131-release-parity.txt`) |
| T131 | closed | copies regenerated (no template changed in this wave); `.specify/templates/commands/` stays absent |
| T133 | closed | every `pointer` ledger row's evidence path resolves (5/5); the preset's slot sentence is a pointer, the four seats unchanged |
| T134 (C-092) | closed | `notes/disposal-ledger.md` — 12 rows, closed four-value domain; the live ledger test passes; the four-carrier and slot dispositions recorded |
| T137 | closed | `notes/quickstart-run.md` — S-0…S-6 run against the live tree with a teardown note; S-5's record-less command repaired in place |

## Readings

| Reading | Command (canonical entry) | Result | Evidence |
|---|---|---|---|
| Acceptance suite (smoke) | `bash scripts/bash/run-tests.sh <11 concurrency modules> -q` | **96 passed, 0 skipped** | `wp5-acceptance-final.txt` |
| Full suite (GATE-1, final tree) | `bash scripts/bash/run-tests.sh -q` | 207 failed / 8256 passed / 2 skipped; **0 NEW 093-caused** names vs the frozen 161-name baseline (46 NEW = 44 master-inherited + 2 trigger-order) | `wp5-suite-final.txt`, `wp5-gate1-comparison.txt` |
| Pre-WP5 suite | same, on the untouched tree | 230 failed / 8225 passed / 4 skipped; 70 NEW | `wp5-suite-pre.txt` |
| Re-pin set | the 6 affected modules | 323 passed | commits `b2f9589ab`; readings in the row files |
| Mirrors / copies | `sync-mirrors.py --check`; `regen-command-copies.py --check` | exit 0 / exit 0 | `wp5-t130-t131-release-parity.txt` |
| validate-tasks (GATE-6) | `python3 .specify/scripts/python/validate-tasks.py …/tasks.md` | PASS — 0 error / 0 warning, 159 rows | `wp5-validate-tasks.txt` |
| validate-requirements | `python3 .specify/scripts/python/validate-requirements.py …/requirements.md` | 0 error / 0 warning (345 lines / 48 definitions / 11 strings) | `wp5-validate-requirements.txt` |
| Closure judgement | `closure-acceptance-check.py --spec-dir … --repo .` | `block` — one reason: `final-path-not-pass` (SC-006) | `wp5-closure-reading.json` |
| Post-commit re-checks | `test_script_interface_contract::test_c20` + `test_clause_coverage::test_c20` | 2 passed (both were transient: the untracked-module finding cleared at commit; the corpus-md5 race passes alone); the final full-suite run confirms both resolved | this record |

## Disclosures (Fast Fail — correction-class, repaired in passing)

1. **The package's declared write domain was narrower than the rows it owns.** The map lists evidence
   files only, but the rows themselves require document writes (`T034–T036`, `T099`, `T062–T065`,
   `T079–T085`, `T101–T105`, `T116–T118`, `T124`, `T133`), test writes (`T017/T019`, `T090`) and the
   13-assertion re-pin that SC-010's green reading needs (`test_stage_class_wiring`, `test_humanize_command_surface`,
   `test_validation_carrier_contract`, `test_sdd_house_keeping_skill`, `test_sdd_loop_driver_wp_coordination`
   fixtures, `test_sdd_loop_driver_wp_preset`). Each write was executed as the row states, after every
   other package closed, so no write-domain conflict existed; this record is the deviation disclosure.
2. **T112's "goal-slice decomposition recording"** is closed on the existing implementation: the coverage
   action reports each goal's per-stage coverage resolved through the fact and lists only open targets as
   packages (so no coverage is claimed over an unfinished slice). The fact gained no second goal-slice block
   — the stages remain the fact's own rows.
3. **The 091 figure chain.** The 116-minute value is not present as a duration field in 091's spine; it is
   carried by the spec's own recorded citation (`requirements.md` line 19/179/SC-006 and `features/093.md`
   line 5). `notes/serial-baseline.md` states the chain explicitly rather than inventing a measurement.
4. **The quickstart S-5 command** omitted `--record`; the capability action is a record-judging action
   (C-021) and rejects that invocation. The page is corrected in place (one argument added) and the
   correction is recorded in `notes/quickstart-run.md`.
5. **The closure verdict is `block`** with SC-006 as its only reason, plus 159 task rows still open in
   `tasks.md` (state sigils are flipped by the integration owner, not by this package — the file is not in
   WP5's write domain). SC-006 needs an explicit user waiver or the next dispatching run.

## Residual risks

- **SC-006** stays `blocked`; the mechanism is delivered, the exercised concurrent run is not.
- **SC-007 / SC-010** stay `partial` with their ladders: no team/loop fixture exists yet, and the tree's
  literal all-green claim is blocked on inherited reds outside this feature's domain.
- **The trigger-family order sensitivity** and the **corpus-md5 race** are pre-existing parallel-run
  behaviors; both pass in isolation and are recorded, not retried into green.
- **`registered_facts`** in `contract.yaml` came from 094's master sync; T128's comparison names it so the
  key set is never read as all-093.

ANOMALY: the WP5 package map's declared write domain (evidence files only) contradicts the rows it owns — 12 document/test surfaces had to be written and 13 pre-093 assertions re-pinned to satisfy SC-010; all writes were executed in the serial release wave after WP1–WP4 closed, each is disclosed above, and the suite carries zero NEW 093-caused failures, but SC-006 remains blocked (no real concurrent run) and the closure verdict therefore reads `block`.
