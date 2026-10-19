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

## US4 — T033 (C-26, C-27, C-28)

- Suite: `python3 -m pytest tests/contract/test_evidence_binding_contract.py -q`
  → **19 passed** (red run recorded first: 17 failed / 2 passed, exit 1 — the 2 green
  legs are the must-remain pins `test_c26_existing_sections_preserved_additive_only`
  and `test_c27_reuses_the_existing_handler_no_new_subsystem`; verbatim tails in
  `notes/red-first-evidence.md`).
- C-26 landed (T031): `templates/verification-log-template.md` gains
  `# -- Evidence records ... --` between the implement-results and SC-evaluation
  markers — four declared fields (`sample_id` / `evidence_path` repo-relative /
  `evidence_sha256` SHA-256 over the archived file's bytes, sha256sum-compatible /
  `verdict`), the pass-requires-complete-evidence-row rule, the `unverified` class,
  and the no-downgrade rule; pre-existing section set and order preserved (additive).
- C-27 landed (T032): registry Object row
  `| gate-implement-evidence-binding | command-gate | /speckit.implement | ... |`
  directly beside `gate-implement-checklist-waiver`; HandlerBinding row
  `| h-gate-evidence | @point:confirm-gate | gate-implement-evidence-binding | 063
  证据绑定门:pass 声明绑定归档证据([[STR-001]]) |` — REUSING the existing
  h-gate-evidence handler id (no new subsystem, pinned by
  `test_c27_reuses_the_existing_handler_no_new_subsystem`); `implement-feature`
  Step 9 references the gate with the full check semantics + 门控观察协议 +
  `--lifecycle-point` firing-evidence path.
- C-28 drills (T033, quickstart S8 shape, in the suite): the S8 fixture (four `pass`
  samples — matching/missing/empty/mismatch + one `fail` sample) yields green only
  for the matching sample; each red names the sample id and reason
  (`SC-002 missing` / `SC-003 empty` / `SC-004 mismatch`); the `fail` sample carries
  no binding duty; the no-evidence-section form marks every SC `pass` unverified
  (green stays empty); an incomplete evidence row (`pass` missing `evidence_sha256`)
  is unverified, never green, never mismatch-red. The checker derives its parser
  from the template's declared section — a template without the section fails the
  drills, so the red run was genuine and a declaration drift breaks its own gate
  semantics.
- Intermediate projection (D-T8 pattern, registry + template + skill edits):
  `sync-mirrors --only shared` → `compile-embeds` (74 unchanged — the gate binding
  sits at `@point:confirm-gate`, outside the wrap-up render, so faces and banner
  fingerprint stayed identical) → `regen-command-copies` →
  `sync --only skills/internal/implement-feature --only templates`. Post-state:
  `compile-embeds --check` 74 units zero drift; regen OK; sync 3 DIFF (the
  pre-existing `.specify/agents` baseline drift only, untouched prefix).
- Registry consumers re-run green: `test_probe_engine_action_sets.py +
  test_phase2_bindings.py + test_compile_embeds.py + test_run_skills_wiring.py +
  test_evidence_binding_contract.py + test_review_p1_recheck_waiver.py` →
  **55 passed**.
- In-passing test-harness fixes disclosed (my new file, correction-class): the
  field regexes were digit-blind (`[a-z_]` missed `evidence_sha256`'s digits),
  blank lines failed to close a record block (records merged onto the last one),
  and the no-section findall captured a 2-tuple where 1 group sufficed. All three
  fixed before the green run; no fixture or assertion weakened.
- Claim: C-26..C-28 green (clause partition row T033).

## US5 — T038 (C-29, C-30)

- Suite: `python3 -m pytest tests/contract/test_baseline_preflight_contract.py -q`
  → **9 passed** (red run recorded first: 9 failed / 0 passed, exit 1 — verbatim tails
  in `notes/red-first-evidence.md`; every leg failed on the absent pre-flight step /
  absent command-face duty).
- C-29 landed (T036): `implement-feature` SKILL.md gains `### Step 0 — Baseline
  pre-flight (re-capture frozen values)` before Step 1 — the set is derived by glob
  (`<spec-dir>/baseline-*`, `<spec-dir>/notes/baseline-*`) plus the coverage baseline
  ([[STR-002]]), declared directory-derived never a hand-written count; differences
  write back into the citing row; the four-way classification (`upstream repair` /
  `inherited` / `attributable to this feature` / `undecidable`) via `git log`
  provenance happens BEFORE any drift verdict; `undecidable` is reported explicitly
  with no guessing; a missing baseline file is a first capture with provenance,
  never zero drift.
- C-30 landed (T037): `templates/commands/implement.md` Skill Delegation inputs gain
  a **Baseline pre-flight** bullet BEFORE the "follow its steps 1–9" bullet, carrying
  the same obligation shape (both glob roots, all four classes, the
  undecidable-report and first-capture rules) — a reader of the command face alone
  meets the duty.
- S9 drill (T038, fixture git repo `/tmp/sdd-review-p1/s9-drill`, removed after
  recording): frozen `notes/baseline-widget-count.txt` (value 5) no longer matched
  the tree (2 widgets); `notes/baseline-probe-latency.txt` cited by a task row but
  never captured. Pre-flight walk: (1) set derived by glob — notes glob found the
  widget baseline, root glob found none, coverage baseline included per [[STR-002]],
  citation discovery surfaced the missing probe-latency file; (2) re-capture: widget
  5→2 DIFFERS, coverage 0=0 matches, probe-latency MISSING; (3) classification
  BEFORE any verdict via `git log`: widget-count diff = `inherited` (post-freeze
  upstream commit 3ab9c77, outside the 999-drill window — provenance-backed, no
  guessing); probe-latency = first capture with provenance (citing row T001 in
  freeze commit c659adb), NOT zero drift; (4) write-back: both citing rows in the
  fixture `tasks.md` now carry the re-captured value 2 with the classification
  (`git diff --stat`: 2 insertions, 2 deletions).
- Projection for the T036/T037 source edits: `regen-command-copies` (per-tool
  `speckit.implement.md` copies regenerated) + `sync --only
  skills/internal/implement-feature`; post-state `compile-embeds --check` 74 units
  zero drift, `regen-command-copies.py --check` OK.
- In-passing disclosures: (a) two regex legs in the new suite needed
  whitespace-flexible matching (the clause's own wording wraps mid-phrase —
  "row that / cites it"); fixed in the test, not by re-flowing the owner text.
  (b) The US4-boundary regression (24 failed) showed 2 transient NEW names
  (`test_run_checks c27`, `test_user_facing_comprehension_pointers c14`) caused by
  the US5 T037 edit landing while that regression was in flight — the per-tool
  copies had not yet been regenerated for it. The US5 projection above closes the
  gap; the final US4+US5-boundary regression below re-verifies 0 NEW.
- Claim: C-29/C-30 green (clause partition row T038).

## US6 — T043 (C-16, C-17, C-18, C-19)

- Suite: `python3 -m pytest tests/contract/test_premise_carrier_contract.py -q`
  → **11 passed** (red run recorded first: 9 failed / 2 passed, exit 1 — the 2 green
  legs are the must-remain pins: the reference-not-restate duty survives the carrier
  opening, and the producer-side re-capture obligation exists before the re-pointing;
  verbatim tails in `notes/red-first-evidence.md`).
- C-16 landed (T041): create-tasks SKILL § Environment probe rules item 2 now declares
  the carrier duty OPEN — per-phase prerequisites, `[~]` task notes, assumption rows,
  decision rows, and ANY free-prose row stating or implying an environment verdict;
  "no carrier is exempt by being unlisted; the list cannot be closed".
- C-17 landed (T042): `templates/tasks-template.md` § Environment Prerequisites ACTION
  REQUIRED now requires ANY restating row (any carrier) to carry an ISO date stamp
  TOGETHER WITH a `(see § Environment Prerequisites)` pointer — both together, neither
  alone, either alone non-compliant.
- C-18 landed (T041): the red-first note shape rule (create-tasks SKILL §
  Runtime-evidence landing points — the content-prescription owner) now requires a
  note binding a claim to a gate to quote the gate row verbatim (id + name + check
  command); a bare gate id alone MUST NOT be used; declared forward-applicable only
  with 062's note instance out of scope (never retro-edited).
- C-19 landed (T041): § Re-freeze timing retains the producer-side obligation
  (re-capture on every generation and every rerun) and points the implement-side
  re-capture at its owner — `/speckit.implement`'s baseline pre-flight (Step 0 in
  implement-feature SKILL, the C-29 consumer step).
- S7 drills (T043, fixture `/tmp/sdd-review-p1/s7-drill`, removed after recording):
  - Carrier rule: a seed `tasks.md` carried four restating rows. Mechanical probe of
    the double requirement: D-T1 (no date, no pointer) → FLAG; D-T2 (date-only) →
    FLAG; D-T3 (pointer-only) → FLAG; D-T4 (both) → PASS. Both required, neither
    alone — exactly the Edge-Cases semantics.
  - Renumbering leg (C-18): under a renumbering fixture (GATE-3 → registry-pull,
    docker-build → GATE-4), the bare-id note still resolves but now names
    `registry-pull` — a different gate: the binding silently points at the wrong
    gate, an INVISIBLE mismatch. The verbatim-quote note (`GATE-3 | docker-build |
    docker build -t t .`) resolves before renumbering and FAILS after — a VISIBLE
    mismatch, the exact effect C-18 requires.
- Projection for the T041/T042 source edits: `sync --only skills/internal/create-tasks
  --only templates`; post-state compile-check 74 units zero drift, regen --check OK;
  the three new suites re-run together → 39 passed.
- Claim: C-16..C-19 green (clause partition row T043).

## Polish — T044 (C-25)

- Full-unit recompile (C-25, after T027 renderer/registry + T032 gate row landed):
  `python3 .specify/scripts/python/probe-utils.py --action compile-embeds` →
  `written: [], unchanged: 74, zero_section: []` — the US3 intermediate recompile
  (D-T8) already carries the manifest-driven faces, and the US4/US6 registry edits
  (gate row, sdd-project-setup row) sit outside the wrap-up render, so the recompile
  confirms rather than rewrites.
- Zero drift: `compile-embeds --check` → `{"ok": true, "units": 74, "structural": [],
  "drift": []}`.
- Reconcile closure: `probes --validate --reconcile` → `{"ok": true, "reconciled":
  true, "classes": 10, "objects": 116, "external_objects": 0, "embeds": 74}` —
  rows↔embeds bidirectional consistency holds.
- **In-passing correction disclosed**: the first `--reconcile` run reported
  `embed without probe object: skill:sdd-project-setup` — a registration gap that
  predates this feature (commit 0a1dbf2f added the skill WITH a compiled wrap-up
  face at fingerprint 466ed9a but no registry row; every subsequent recompile kept
  compiling it as part of the 74 units). Registration row
  `| skill-sdd-project-setup-wrapup | skill-wrapup | skill:sdd-project-setup | wrap-up |`
  added (alphabetical, beside the other skill-wrapup rows) — the same
  add-the-missing-row remedy 062's commit 92037f07 applied for `skill:humanize`;
  one consistent reading, local and reversible, disclosed here. No other
  `--reconcile` surface was touched.
- Backlog flip (same commit as the recompile evidence): `.specify/memory/feedback/
  backlog.md` line 89 (2026-10-15 introspection F-01, route direct-fix) flipped
  `open(...)` → `closed(063 C-20..C-25 落位: ... --check 零漂移 ok:true units:74
  structural:0 drift:0, --reconcile ok:true 116 objects/74 embeds; 证据 ... § US3/T028
  与 § Polish/T044)`.
- Claim: C-25 green (clause partition row T044).

# -- Free-form notes --

notes=US1 complete (C-1..C-10 claimed by T011..T014). US2 complete (C-11..C-15 claimed by T022): C-12 adjudication landed via /speckit.instructions Action 5 (a8c3c1f0) with mechanism descriptions aligned this run; the 3 pre-existing contract failures reconciled (c27/c14 via regen+sync, c12 via the 053-window closure amendment, disclosed above). US3 complete (C-20..C-24 claimed by T028): args-manifest on all three wrap-up engines, one-shot missing-arg errors, manifest-driven renderer + registry convention line, 18/18 new face-contract suite, D-T8 forced intermediate projection, byte-budget/closed-set amendments disclosed above; full suite 21 failed / 4050 passed, 0 NEW vs the frozen baseline. US4 complete (C-26..C-28 claimed by T033): template evidence-record section, gate row + HandlerBinding (reusing h-gate-evidence) + Step 9 reference, 19/19 suite with S8-shape red-semantics drills; three test-harness fixes disclosed above. US5–US6 + Polish remain.
