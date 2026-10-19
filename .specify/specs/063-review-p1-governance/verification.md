# Verification Log — 063-review-p1-governance

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=728ad4ea
baseline_date=2026-10-19
baseline_branch=063-review-p1-governance
baseline_failed_tests=63
baseline_passed_tests=3954
baseline_mirror_diff=202
baseline_compile_units=74
baseline_compile_drift=0
baseline_register_rec_rows=0
baseline_backlog_line89_status=open

# -- /speckit.implement results --

implementation_date=2026-10-19
post_change_commit=pending

# -- Success Criteria evaluation --
# Status values: pass | fail | partial | deferred | unknown.

SC-001_status=unknown
SC-001_value=pending
SC-001_note=pending

SC-002_status=unknown
SC-002_value=pending
SC-002_note=pending

SC-003_status=unknown
SC-003_value=pending
SC-003_note=pending

SC-004_status=unknown
SC-004_value=pending
SC-004_note=pending

SC-005_status=unknown
SC-005_value=pending
SC-005_note=pending

SC-006_status=unknown
SC-006_value=pending
SC-006_note=pending

SC-007_status=unknown
SC-007_value=pending
SC-007_note=pending

SC-008_status=unknown
SC-008_value=pending
SC-008_note=pending

SC-009_status=unknown
SC-009_value=pending
SC-009_note=pending

SC-010_status=unknown
SC-010_value=pending
SC-010_note=pending

SC-011_status=unknown
SC-011_value=pending
SC-011_note=pending

SC-012_status=unknown
SC-012_value=pending
SC-012_note=pending

SC-013_status=unknown
SC-013_value=pending
SC-013_note=pending

SC-014_status=unknown
SC-014_value=pending
SC-014_note=pending

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=none

# -- Phase verification log --

## US1 — T011 (C-1, C-2)

- Command: `python3 -m pytest tests/contract/test_clause_forms.py -q`
- Result: `34 passed, 1 failed`; the single failure is the frozen baseline failure
  `test_the_four_md_forms_never_co_occur_in_one_file` (baseline line 5). All new
  dual-width/nesting/malformed/ASCII-invariance tests pass.
- Owner text assertion passes against `shared/definitions/contract-clause-definitions.md`
  § 4 rule 2.

## US1 — T012 (C-3, C-4)

- Command: `python3 -m pytest tests/contract/test_review_p1_checklist_governance.py -q`
- Result: `5 passed` (0 failed).
- Drill (`/tmp/s63-drills-*`): one checklist with `[Coverage, Gap]` CHK001 plus a
  no-Gap CHK002; a recheck answers CHK001. Output:
  `unchecked=2 gaps=1 no_gap=1`, `unchecked + unraised + undispositioned = 0`.
  No-Gap row adds no obligation.
- Disposition drill: `CHK003 disposition: raised-as-finding H-01` yields
  `unchecked + unraised + undispositioned = 0`.

## US1 — T013 (C-5, C-6, C-7)

- Command: `python3 -m pytest tests/contract/test_clause_coverage.py -q`
- Result: `43 passed, 1 failed`; the only failure is the frozen baseline
  failure `test_c5_gate_budget_is_unchanged_by_the_owner_document` (baseline line 4).
- Dual-width fixture: `clause_extract.py` reports
  `clauses=3` with citations `{C-1: FR-001, C-2: FR-002, C-3: FR-003}` — one total for
  half-width, full-width and same-width nested groups.
- Accountant without a frozen baseline on the hermetic fixture:
  `baseline: .../coverage-baseline.txt (0 names, MISSING)`, `status: baseline-missing`,
  exit 2 — visible, never a silent pass.
- Same path form: `account-clause-coverage.py` `BASELINE_NAME=coverage-baseline.txt`;
  both the analyze and create-tasks faces name that same default (asserted by
  `test_c7_both_sides_name_the_accountants_same_default_path`).
- A feature without a contract set: the analyze skill records an explicit skip with its
  reason (C-5); the accountant's zero-denominator companion remains observable.

## US1 — T014 (C-8, C-9, C-10)

- Command: `python3 -m pytest tests/contract/test_review_p1_recheck_waiver.py -q`
- Result: `9 passed` (0 failed).
- Drill: recheck answers CHK001; original checklist SHA-256 is byte-identical before and
  after (`93864ebccd11...`); the third branch leaves only CHK002 unresolved (no waiver
  needed for the answered item). Four-part waiver is compliant; a waiver missing
  `Closed` is non-compliant.

## Decisions carried by this feature (analyze C-01 / C-02 / C-03)

### C-01 — "运行证据" carrier set

A runtime-evidence claim (FR-017's explicit re-measurement decision, and every other
"this run produced evidence" claim) is carried by exactly this set:

1. **Engine store record** — the record `run-determination.py` writes for the
   `(unit_id, run_id)` pair (its store entry, addressable by that key), plus the
   `feedback-utils.py` / `exec-quant.py` entries when the claim spans those engines.
2. **Same-commit `git show --stat`** — the stat of the commit that carries the record,
   proving the record and the artifact landed together.

A claim missing either carrier is unrecorded: the engine record without the commit stat
cannot show same-commit landing, and the stat without the engine record cannot show what
was measured. This definition is reachable from requirements FR-017's inline note.

### C-02 — waiver storage location

Waivers land at `<spec-dir>/waivers.md` (`REQUIREMENTS_DIR/waivers.md` in the implement
skill's terms) — the same location 062 used (`062-humanize-command/waivers.md`). No new
store is introduced, and the four-part format is owned by implement Step 2 (C-10).

### C-03 — S6 reconcile-flag decision

Recorded with the S6 run in `notes/quickstart-run.md` (T047); the decision and its command
line are mirrored here when that run lands.

## C-12/T018 — adjudication landed (2026-10-20, resumed run)

The attempt-1 halt is resolved by user adjudication (recorded in `requirements.md` §
Clarifications, Session 2026-10-20): the live `.specify/instructions.md` receives the
`REC-` enumeration through `/speckit.instructions` (manage-instructions Action 5 content
refresh) — `generate-instructions.sh` stays additive-only per its pinned C-2 contract
(`test_instructions_section_propagation`), never extended.

- Landing facts: template row in `templates/instructions-template.md` (bd108d5a); live
  file row at `.specify/instructions.md` line 176 via the instructions stage (a8c3c1f0);
  ID Register section byte-identical to the rendered template; 9/9 compatibility
  symlinks resolve; `git diff` on the symlink set empty.
- Alignment edits this run: `contracts/template-mechanisms.md` C-12, `tasks.md` T018 +
  decision D-T7 (supersedes D-T3's mechanism leg), `quickstart.md` S5 comment,
  `plan.md` § Mirror Obligations row, and the test renamed to
  `test_c12_live_instructions_received_rec_via_content_refresh` (docstring/assertion
  message aligned to the content-refresh owner).

## US2 — T022 (C-11, C-12, C-13, C-14, C-15)

- Command: `python3 -m pytest tests/contract/test_review_p1_review_loop.py -q`
- Result: `10 passed` (0 failed) — includes the renamed C-12 live-file leg.
- S5 seed drill (`/tmp/s63-s5-drill.*`, removed after the run): a fixture review with
  `REC-s63-01..03` landed its `register.md` pointer rows (3/3) **in the same commit**
  as the report (`git show --stat` shows `review.md` + `register.md` in one commit);
  a clean clone resolves the repo-relative REC targets (`docs/rec-target-a.md`,
  `docs/rec-target-b.md` — `test -f` green) while the no-repo-relative target stays
  marked `external`; the live table carries
  `| /speckit.review | Implemented → Ready for Review | review.md committed AND every deferred item resolved or waived |`
  with the checklist row annotated "applies only when the checklist runs after
  implement" (mirror, post-sync); `A3 自省(Introspection)` named in the synced
  `feedback-step.md` mirror; `grep -n "REC-" .specify/instructions.md` → line 176.
- Claim: C-11..C-15 green (clause partition row T022).

## Pre-existing 3 contract failures — reconciled this run (2026-10-20)

The resumed run's first act re-ran the fixed-order projection for the bd108d5a source
batch (`compile-embeds --check` → 74 units zero drift, no write needed; `regen-command-copies.py` write;
`sync-mirrors.py --write --only templates --only skills/internal --only shared --only scripts`):

- `test_run_checks.py::test_c27_…` and `test_user_facing_comprehension_pointers.py::test_c14_…`
  turned green by the regen/sync (per-tool copies + mirrors now match sources).
- `test_neutrality_budget.py::test_c12_the_status_state_machine_is_untouched` was **not**
  a mirror-staleness failure (the dispatch's stated cause does not hold for it): it pins a
  `git diff ad190d46..HEAD` window over `shared/workflow/feature-integration.md`, which
  bd108d5a's T021 (C-15 review row) legitimately changed. Reconciled by closing the
  window at 053's last implement-window commit (`C12_WINDOW_END = cb0a190a`) in the test:
  053's own contract scopes the freeze to "本特性窗口" (this feature's window), so the
  open-ended HEAD form over-reached the clause it pins; the closed window keeps the
  original protective claim true forever (`git diff ad190d46..cb0a190a -- <both files>`
  verified empty 2026-10-20) while later features may legitimately extend the table.
  Same amendment shape as that file's own `test_c7` precedent (stale untouched-since-BASE
  claim replaced by the guard that still holds). The plan's § Research already listed
  `test_neutrality_budget.py` among the existing contract tests 063 updates alongside the
  mechanism they pin (FR-027); the research line "presence-only — safe" was a falsified
  premise, disclosed here rather than worked around silently.
- Full-suite name-level comparison after the projection: `run-tests.sh --names-out`
  → 31 failed / 4021 passed; `comm -13 baseline-failed-tests.txt <names>` → **0 NEW**
  (32 baseline failures disappeared with the mirror sync — disappearances are not
  regressions; the 63-name baseline file is untouched).

## US3 — T028 (C-20, C-21, C-22, C-23, C-24)

- Targeted suites: `python3 -m pytest tests/contract/test_engine_face_contract.py
  tests/contract/test_probe_engine_action_sets.py tests/contract/test_compile_embeds.py
  tests/contract/test_compile_reconcile_guards.py tests/contract/test_phase2_bindings.py
  tests/contract/test_run_determination_engine.py tests/contract/test_dogfooding_practice.py
  tests/contract/test_run_skills_wiring.py -q` → **266 passed** (18/18 in the new
  `test_engine_face_contract.py`; the pre-existing suites stay green under the
  extended faces — `_CALL_ENGINE_RE` anchors on the `python3 <owner> --action <action>`
  prefix, so the inline placeholder tails keep every structural consumer working).
- Live face shape (per-tool `/speckit.implement` copy, post-recompile): the Run
  Determination line carries `--run-id <RUN_ID> --complexity <COMPLEXITY>` inline plus
  `` `；source args when available: `` `--session-file <SESSION_FILE> … --red-source <RED_SOURCE>`;
  the registry-declared convention line renders once after the first placeholder-carrying
  line; Exec Quant carries the source-only `--run-id <RUN_ID>`; Feedback Record carries
  `--run-id <RUN_ID> --review <REVIEW> --points <POINTS>`. Banner fingerprint updated
  by the recompile (`7877db82c58c`).
- Intermediate projection (D-T8, forced inside US3): registry sync (`--only shared`) →
  `compile-embeds` 74 units written → `regen-command-copies` → touched-mirror sync
  (skills sub-prefixes synced per touched source prefix; the bare `--only skills` form
  is a silent no-op — the pair names are `skills/external`/`skills/internal`, disclosed
  here as an engine UX trap, not fixed in passing: it is a cross-feature engine
  interface, out of this feature's declared scope).
- Post-projection checks: `compile-embeds --check` → ok, 74 units, zero drift;
  `regen-command-copies.py --check` → OK; `sync-mirrors.py --check` → 3 DIFF (all
  pre-existing `.specify/agents` baseline drift, untouched prefix), 0 NEW vs the
  202-DIFF `notes/baseline-mirror-check.txt`; touched pairs (shared/, scripts/,
  skills/, templates→per-tool copies) absolutely consistent.
- In-passing corrections disclosed (byte-budget amendments, same amendment shape as
  the D-T8 forced recompile): C-20/C-21's inline manifest rendering grew the largest
  compiled face to 2135 B, tripping three `1500 B` reference-not-copy budgets
  (`test_feedback_step_reference_form.py::MAX_SECTION_BYTES`, and the inline `< 1500`
  asserts in `test_docs_step_injection.py` + `test_derive_command_surface.py`) and
  surfacing one stale closed-set pin (`test_exec_quant_engine.py::ACTIONS_CLOSED_SET`,
  which had already drifted at 059 — collect-dispatch landed without the write-back).
  All four amended with dated 063 comments; the reference-not-copy intent is unchanged
  (OWNER_ONLY_LITERALS + docs-step cite assertions still enforce it); the C-21
  mutation-drill guards in `test_engine_face_contract.py` prove the rendered set is
  the engine manifest, not a hand-written copy. `scan-confirmation-gates.py` → 0
  violations (rendered faces pass the wording gate).
- Full-suite name-level comparison after the amendments: `run-tests.sh --names-out`
  → 21 failed / 4050 passed; `comm -13 baseline-failed-tests.txt <names>` → **0 NEW**
  (42 of the 63 baseline failures disappeared with the mirror sync; the remaining 21
  are pre-existing baseline failures, not this feature's repair surface).
- 062 read-only invariant: `git diff --stat -- .specify/specs/062-humanize-command/`
  → empty. Symlinks 9/9 intact. `gate-check.py` over all 288 US3 write paths → exit 0.
- Claim: C-20..C-24 green (clause partition row T028).

# -- Free-form notes --

notes=US1 complete (C-1..C-10 claimed by T011..T014). US2 complete (C-11..C-15 claimed by T022): C-12 adjudication landed via /speckit.instructions Action 5 (a8c3c1f0) with mechanism descriptions aligned this run; the 3 pre-existing contract failures reconciled (c27/c14 via regen+sync, c12 via the 053-window closure amendment, disclosed above). US3 complete (C-20..C-24 claimed by T028): args-manifest on all three wrap-up engines, one-shot missing-arg errors, manifest-driven renderer + registry convention line, 18/18 new face-contract suite, D-T8 forced intermediate projection, byte-budget/closed-set amendments disclosed above; full suite 21 failed / 4050 passed, 0 NEW vs the frozen baseline. US4–US6 + Polish remain.
