# Verification Log — 074a-authorized-routing

Shape follows `.specify/templates/verification-log-template.md`; the `status` values below are drawn
from that template's closed vocabulary (`pass | fail | partial | deferred | unknown`) and nothing
narrower. Every `pass` carries a complete evidence row (`sample_id` / `evidence_path` /
`evidence_sha256` / `verdict`), hashed over the archived file's bytes.

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=71954e31a1ff58480342209c1d54329a05c30225
baseline_date=2026-10-29
baseline_branch=074-goal-team-sdd-unification

baseline_full_suite_passed=6361
baseline_full_suite_failed=23
baseline_targeted_set_passed=191
baseline_mirror_pairs_clean=6
baseline_contract_files_targeted=13

# -- /speckit.implement results --

implementation_date=2026-10-29
post_change_commit=f1d65142ad73433a838a096120f837706ba20644

post_change_full_suite_passed=not-evaluated
post_change_full_suite_failed=not-evaluated
post_change_targeted_set_passed=277
post_change_mirror_pairs_clean=6
post_change_new_test_modules=5
post_change_new_tests=86

> `post_change_full_suite_*=not-evaluated`: the closure full-suite slot was not spent in this stage.
> The E2 baseline slot was consumed at implement start (`test-evidence/implement.jsonl` seq 1,
> `6361 passed / 23 failed`) and the dispatch forbids a second full run; the closure slot belongs to the
> driver after `/speckit.review`. Nothing here claims a full-suite result that was not measured.

# -- Evidence records (bind every `pass` claim to an archived file) --

sample_id=SC-001
evidence_path=.specify/specs/074a-authorized-routing/notes/green-t016.txt
evidence_sha256=55ef7a5d717555667b21b38c91efec90cd4d61102ce5c2f78c39d86da3f0ef6d
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/074a-authorized-routing/notes/golden-rows.txt
evidence_sha256=cc05b8724b4c98a0ba69ba23754ca00eb5a1ea0fe18f96307fef651f0deeadea
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/074a-authorized-routing/notes/green-t016-demo.txt
evidence_sha256=97116fab2652ad597d7ee3bb2091f62678885045611b40f32e856f3d3f5a8727
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/074a-authorized-routing/notes/green-t025.txt
evidence_sha256=f81df8d28ff70014adaa5f2bbc57f7030d12bf1b6338897851584ddbb6fbb96e
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/074a-authorized-routing/notes/quickstart-run.md
evidence_sha256=ddc4445c5b3b57b06dcf6cca4f4d808e2f22a4ba5a823dde28c57ba010166c40
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/074a-authorized-routing/notes/green-t021.txt
evidence_sha256=02a2451a06897d8b5f0609b37e588f2f9acc5d7a0a683f4e38b880868090fb31
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=34 passed (tests/contract/test_sdd_authorization.py 11 + tests/contract/test_nested_sdd_invocation.py 23); fixture team with seat-allowed / seat-forbidden / seat-absent
SC-001_note=Authorization resolves both halves by (team, seat); the unauthorized seat is refused before dispatch with `failed_half=seat` plus both source paths and the seat slug, and that record rides the existing create-team report contract (no new carrier). The "starts exactly one nested run" half is exercised on the fixture's content face — no live team run exists in this repository (recorded decisions D-2 / D-3).

SC-002_status=pass
SC-002_value=14/14 golden rows judged (`all_match=True`); two `--action golden --format json` runs byte-identical
SC-002_note=Every row returns its documented verdict and reason code across all seven required change classes; repeated evaluation of identical inputs is byte-identical (determinism measured, not asserted).

SC-003_status=pass
SC-003_value=handoff carries the 7-field closed set; stages stop at review; `git log` / `git status` / branch / HEAD identical before and after (zero merge, zero push)
SC-003_note=Delivered scope per recorded decision D-3 — artifact chain, review stop, zero merge / zero push, and artifact + evidence path references carried by the caller result and the existing report contract. The report's `## Nested SDD Runs` heading literal and section semantics belong to 074b and are **not** claimed here.

SC-004_status=pass
SC-004_value=17 governance cases green; targeted non-regression set 191 passed with a 0-entry failed-name list
SC-004_note=Four dispatch forms decided (authorized / blocked-before-dispatch / stage-executor refusal / SDD-within-SDD refusal) plus the virtual-mode refusal; the three pre-existing anti-nesting assertions keep their verdict on every non-authorized path.

SC-005_status=pass
SC-005_value=command and skill name sets identical to the T001 commit; `.specify/state/` and `.specify/memory/` `comm -13` both empty; 34 added paths, none a registry / ledger / queue / ownership manifest / state spine
SC-005_note=Line-registry reuse proven by mtime ordering (no entry written by this stage) and by two green contract cases; nested-run records resolve to the existing line entry and this loop's existing state spine.

SC-006_status=pass
SC-006_value=ambiguous rows (G5, G14) and conflicting row (G6) all adjudicate; `test_ambiguous_and_conflicting_rows_never_return_direct` green
SC-006_note=No ambiguous or conflicting input set reaches the direct verdict anywhere in the golden table, and the precedence rule is re-proved live by quickstart S3.

# -- Per-SC rows (one line each: status · command · output summary · evidence pointer) --

- **SC-001** — status `pass` · command `python3 -m pytest -q tests/contract/test_sdd_authorization.py tests/contract/test_nested_sdd_invocation.py` · output `34 passed` · evidence `notes/green-t016.txt`, full demo `notes/green-t016-demo.txt`, quickstart `notes/quickstart-run.md` § S4 / § S5.
- **SC-002** — status `pass` · command `python3 scripts/python/sdd-route.py --action golden --format json` (twice) · output `14 cases, all_match=True` both runs, byte-identical · evidence `notes/golden-rows.txt`, `notes/golden-run1.json`, `notes/golden-run2.json`, quickstart `notes/quickstart-run.md` § S1 / S2 / S3.
- **SC-003** — status `pass` · command `python3 -m pytest -q tests/contract/test_nested_sdd_invocation.py::test_nested_run_reaches_review_zero_merge_zero_push` · output handoff field-complete, `review` terminal, git state identical · evidence `notes/green-t016-demo.txt`, quickstart `notes/quickstart-run.md` § S5.
- **SC-004** — status `pass` · command `python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py` plus the 13-file targeted set · output `17 passed` and `191 passed` · evidence `notes/green-t025.txt`, `notes/green-t025-targeted.txt`, quickstart `notes/quickstart-run.md` § Governance.
- **SC-005** — status `pass` · commands in `notes/quickstart-run.md` § Structure (`diff` over name sets, two `comm -13`, line-registry listing, `comm -13` added-path inventory, two registry-reuse cases) · output all empty / `IDENTICAL-SET` / `2 passed` · evidence `notes/quickstart-run.md` § Structure.
- **SC-006** — status `pass` · command `python3 -m pytest -q tests/contract/test_sdd_routing_definitions.py tests/contract/test_sdd_routing_engine.py` · output `14 + 21 passed`, ambiguous / conflicting rows adjudicate · evidence `notes/green-t021.txt`, `notes/golden-rows.txt`, quickstart `notes/quickstart-run.md` § S3.

# -- Requirement faces without an SC --

- **FR-020 → waived (no SC)**. `## Success Criteria` carries only SC-001…SC-006, all defined before
  FR-020 was added; the implement waiver is taken (no new SC, no renumbering). Its decidable face is
  given by its carrying task rows: T004 (`## Invocation kinds`, four-class classification, C-44 / C-45 /
  C-46) and T028 (zero new commands and skills, C-47), with C-46's "setup / house-keeping subagent
  dispatch uses the same effective-authorization predicate" executed by T023's pre-dispatch probe.

# -- plan_constraint declarations (this pass) --

plan_edit_count=0

> No line of a plan-owned surface was edited in this implement stage. Measured, not asserted:
> `git diff --stat 71954e31a..HEAD -- plan.md data-model.md contracts/ quickstart.md research.md
> feature-ref.md` prints nothing. There is therefore no `PLAN-EDIT:` line to declare, and no
> substantive change to halt on.

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=Gate re-runs (tasks T032) are recorded in the `# -- Gates --` section appended below by that task;
all four gates ran against the frozen task list without renumbering. The closure full-suite run is the
driver's, after review (see the `post_change_full_suite_*` note above).
