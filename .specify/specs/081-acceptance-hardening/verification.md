# Verification Log — 081-acceptance-hardening

baseline_commit=cb841d90
baseline_date=2026-11-02
baseline_branch=081-acceptance-hardening
implementation_date=2026-11-03
post_change_commit=f29b6178

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-004_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the 026 shape is refused at all three call sites — 3/3 refused, 0 passed, measured on the tree the evidence file records (`f29b6178` + the CHANGELOG entry; the later reconciliation/close commits do not touch the call sites): the implement site (`skills/internal/implement-feature/SKILL.md` Step 9's invocation), the review site (`templates/commands/review.md` § The Acceptance Reality Check's own invocation, `--json`) and the driver closure/merge site (`integrate-lines.py build_gate_cmd` output, run the way the gate runs it) each return `block`/exit 1 on `tests/fixtures/acceptance-hardening/negative`, and each refusal's named reason is the closed-set member `zero-final-path-pass` ([[STR-008]]), quoted verbatim from the site's own output — no free text anywhere
SC-001_note=commands, verbatim outputs and exit codes in `test-evidence/081d-call-sites.txt`; the closed-set membership is asserted by the carrier against the checker's own `REASON_CODES`, never re-typed; carrier `tests/contract/test_gate_wiring_081.py` 22 passed

SC-002_status=pass
SC-002_value=all three named readings on record (3/3): (i) the implement site ACCEPTS `tests/fixtures/acceptance-hardening/positive` — `accept`/exit 0, `final_path pass=1 total=1`, `reason: none`; (ii) T004's recorded four-segment composition run over `review-implemented-clean` — its record is `tests/fixtures/acceptance-hardening/review-implemented-clean/review.md`, its transcript (commands/exit codes/segment verdicts) is `test-evidence/081d-review-site-measurement.txt`: process pass; artifact pass with coverage 7/7 derived BEFORE membership; implementation not-applicable WITH the smoke triple measured (command verbatim, exit 0, evidence path non-empty); code not-applicable on the triage's own printed basis; ARC `accept`, claimed `Implemented`, comparison `agree`, the seven-key `final_path` record copied verbatim, the fourth condition judged and passed; (iii) `smoke-mutation` refuses — `block`/exit 1 with `status-claims-implemented-but-blocked` ([[STR-014]])
SC-002_note=(ii) is NOT a bare checker invocation: the payload is one input the artifact segment consumed; T004 owns the reading and this row cites it (C-08 — one run, one evidence file); readings (i) and (iii) are measured in `test-evidence/081d-call-sites.txt`

SC-003_status=pass
SC-003_value=`Blocked` is first-class in 3/3 vocabulary owners: `templates/feature-details-template.md` (the transition owner — 4/4 rows `Planned→Blocked` / `Blocked→Implemented` / `Blocked→Ready for Review` illegal / `Implemented→Blocked` audit exception, landed 081a), `templates/feature-index-template.md` (its own closed six-value status domain, T010 — the file's only prior status surface was the column header) and `skills/internal/manage-features/SKILL.md` (the six-value `Status vocabulary` line plus the narrow `Implemented → Blocked` audit-correction exception BY POINTER with no criteria copied, T010)
SC-003_note=the window 081c recorded (registry row `Blocked` while `manage-features` admitted five values, deferred as WC-14-frozen T024) is closed by T010; carrier `tests/contract/test_acceptance_state_machine.py` 17 passed at the final tree

SC-004_status=pass
SC-004_value=the six-value vocabulary, five `SC-NNN_` ladder fields, illegal-row trigger and the exactly-one smoke record are asserted by the state-machine contract test
SC-004_note=the ladder-mutation fixture is asserted by the checker contract test

SC-005_status=pass
SC-005_value=ownership and premises are first-class, and the inherited-blockers ledger is re-read at line closure (T012): all three this-slice carriers resolve against the live `tasks.md` — IB-004 → `task:T004+test:tests/contract/test_acceptance_review_composition.py`, IB-006 and IB-007 → `task:T012+test:tests/contract/test_acceptance_premises.py` — a 3-of-3 resolved reading (not 081b's 2-resolved-plus-1-disclosed), with zero `inherited-blocker-undisposed` instances in both payloads (closure checker and pre-analyze), cited from the payloads rather than recomputed (C-17 limb 3)
SC-005_note=T012's reading: `test-evidence/081d-inherited-ledger.txt`; carrier `tests/contract/test_acceptance_premises.py` 28 passed. The four deterministic findings still fire 4/4 through both producers; `RS-004`'s three `in-scope` duties remain 3/3

SC-006_status=pass
SC-006_value=the produced `review.md` from T004's recorded run is on record and its CONTENT carries SC-006's measurements: the artifact segment judges the expected set (denominator derived before membership, size printed 7) at coverage 7/7 with no missing member; the implementation segment carries the smoke triple 3/3 (command verbatim, exit 0, evidence path non-empty — measured, not waived); the ARC copies the seven-key `final_path` record verbatim (7/7: pass 1 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 1) and never recounts; zero findings were raised, so the locating-field requirement is met vacuously with its form pinned by the carrier; the negative-side conclusion (P0 `F-ACCEPTANCE`, transition refused, claim unchanged) is green in `tests/contract/test_acceptance_review_composition.py` (32 passed at the final tree, legs f2/f3/f4 + g2)
SC-006_note=the record is fixture-local by stated scope — its header says so, and it names the absence of template sections 3–7 as a scope of reviewing a declarative fixture, not as an omitted required member; this row's basis is the run's content (the run T004 recorded), not the file's existence; the same recorded run is SC-002's reading (ii), so one run serves both

SC-007_status=pass
SC-007_value=the audit is read-only and judgeable: `--audit-existing --repo tests/fixtures/acceptance-hardening/audit-history` leaves both zero-write subjects intact (recursive content hash over a `tmp_path` copy identical before/after; `git status --porcelain` delta 0 over the repository), exits 0 while reporting a finding (C-10) and 2 only on invalid input, and reports per affected feature the claimed status, verdict and every reason (C-12); over the real repository (`--repo .`) it enumerated 63 rows, judged 0 — every pre-081 spec carries no `**Path**` marker yet, so each is reported `not judged` with that reason, never silently skipped — and wrote nothing
SC-007_note=evidence `test-evidence/081d-audit-zero-write.txt`; carrier `tests/contract/test_closure_acceptance_check.py` 23 passed including the contract-named `test_audit_writes_nothing`; the real-repo reading of FR-020 is "the audit runs, reports, and writes nothing", not "the repository is clean"

SC-008_status=pass
SC-008_value=the smoke record exists and reproduces on the final tree: the one command run twice — exit 0 and exit 0 (identical, 2/2) — with `smoke-081.txt` refreshed by the second run (byte-identical content: the smoke module's output is deterministic, "no network, no wall clock"); the command covers FR-005's three things (3/3): `specify init` builds a `.specify/` tree from the checkout's own templates, the checker accepts `positive` (exit 0) and blocks `negative` (exit 1, `zero-final-path-pass`), and `regen-command-copies.py --check` exits 0
SC-008_note=evidence `test-evidence/081d-final-baseline.txt` § (b); the refresh shows as an mtime change, not a diff

SC-009_status=pass
SC-009_value=the four limbs hold: ① both `--check` exits are 0 (`test-evidence/081d-gates.txt`); ② the id-level baseline comparison is green — head 39 failed / 7134 passed / 7 skipped, `head − baseline` = 0 new, `baseline − head` = 0 fixed (the 19 earlier failures were each reconciled deliberately in `test-evidence/081d-final-baseline-2.txt`, 12 pins updated with their reasons); ③ the `CHANGELOG.md` entry landed; ④ the schema-ownership guard is green (column-set hits 0 outside the owner and its one allowed surface `templates/plan-template.md`). The coverage lane remains a **named remainder** outside this criterion (`[fr-uncovered] fail (23)`, 2 of 25 FRs cited; claimable only from in-block FR citations inside this spec's `contracts/`), recorded in the slice's No Deferred Slice section rather than claimed
SC-009_note=the feature-level baseline is now 0 new / 0 fixed at the recorded pins; the 39 remaining failures are the pre-existing baseline set owned by other slices
SC-009_blocked_at=
SC-009_reduced_measurement=full suite: 39 failed / 7134 passed / 7 skipped; head−baseline=0, baseline−head=0; mirrors/regen 0; schema guard 9 passed
SC-009_reduced_measurement_run=yes
SC-009_why_reduced_insufficient=
SC-009_unblock=

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=Slice 081d has no `[~]` task row. 081a's deferred T024 subject (the `manage-features` vocabulary owner) landed in 081d's T010, so no deferral remains anywhere in the feature.

# -- Acceptance summary (copied from the checker; never recomputed here) --

final_path_pass=2
final_path_blocked=0
final_path_deferred=0
final_path_partial=0
final_path_fail=0
final_path_unknown=0
final_path_total=2
acceptance_verdict=accept
final_path_source=test-evidence/closure-verdict-081d.json (byte-identical copy of `.specify/.tmp/081d-closure-verdict.json`, produced by `closure-acceptance-check.py --json-out`; this block is a copy, not a second count)

# -- Notes --

notes=081d closes the feature (final slice, 18/18 rows): SC-001 measures 3/3 call-site refusals with the closed-set reason `zero-final-path-pass` quoted at each site; SC-002 measures all three named readings (implement accepts `positive` exit 0; T004's recorded four-segment composition run over `review-implemented-clean` with its produced fixture-local `review.md` + ARC; `smoke-mutation` refuses with [[STR-014]]); SC-006 passes on the run's content (7/7 coverage, smoke triple measured, 7/7 ARC record, zero findings, negative leg green in the 32-test carrier) with the fixture-local scope disclosed in the row. SC-009 read `fail` at the part-3 close: limbs ①③④ passed and ④'s guard was green, but limb ② measured 19 new full-suite failure ids vs the plan-stage baseline (16 from 081b/081c's late commits, 3 from 081d's spec-mandated T010 edit). The reconciliation `54ad418d` moved limb ② to 0 new / 0 fixed and the row now reads `pass`; the reading is `test-evidence/081d-final-baseline-2.txt`. This is a dated record of the intermediate state, not the current row. The coverage lane remains the named remainder (23 uncovered, 2/25 cited). SC-009 is `supporting`-path, so the feature's transitions are judged by the final path: SC-001 and SC-002 both `pass`, zero open rows, the smoke record in place — T018 lands the status in `.specify/memory/features.md` and `.specify/memory/features/081.md`; the checker is read before the landing (claim still `Blocked`) and again after it, and both payloads are recorded. T015's final sweep: both `--check` runs exit 0 over the final tree with zero regeneration deltas (`test-evidence/081d-gates.txt`); GW-14's three limbs confirmed with the instructions-file spelling disclosed there. Historical 081a/081b/081c notes are preserved in `notes/red-first-evidence*.md`; this slice's own pre-change readings are `notes/red-first-evidence-081d.md`. The task checkboxes T001–T004 and T010–T014 were ticked at this close — their work landed in parts 1–3 (commits 8ceaeb7a, fc6811c6, f29b6178) with the evidence files on record, and the zero-`[ ]` condition requires the file to say so. The full-suite reading was taken on the tree `f29b6178` + this part's CHANGELOG entry (the only tracked delta at run time), with pins re-read and matching; this part's own evidence files and the checkbox ticks are the only other deltas.
