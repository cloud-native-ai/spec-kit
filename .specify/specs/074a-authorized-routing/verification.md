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

# -- Gates (tasks T032, re-run against the frozen task list) --

Four gate commands, run in order, real output verbatim. No task was renumbered; the frozen list is the
one T032 was written against.

### GATE-1 — task-file structure

```console
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md
PASS: .specify/specs/074a-authorized-routing/tasks.md — 0 error(s), 0 warning(s)
RC=0
```

### GATE-2 — cross-artifact consistency

```console
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074a-authorized-routing --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=3 waived=0
{"stage": "tasks", "decision": "pass", "findings": [
  {"check": "missing-path", "severity": "advisory", "path": "tasks.md", "line": 66,
   "message": "path does not exist under the repo: .specify/specs/074b-nested-governance"},
  {"check": "missing-path", "severity": "advisory", "path": "feature-ref.md", "line": 60,
   "message": "path does not exist under the repo: tests/contract/test_nested_run_report.py"},
  {"check": "missing-path", "severity": "advisory", "path": "checklists/requirements.md", "line": 62,
   "message": "path does not exist under the repo: feedback/20261028T160637Z-speckit-requirements.md"}],
 "summary": {"errors": 0, "advisories": 3, "waived": 0, "fr": 20, "sc": 6, "tasks": 32,
             "clauses": 0, "files": 14}, "checked_at": "2026-10-29T03:55:15Z"}
RC=0
```

**Adjudication of the 3 advisories — each `expected absent`, none waived silently:**

1. `tasks.md:66` → `.specify/specs/074b-nested-governance`. The sibling slice has **not** started; its
   absence is exactly what the slice's path conventions require (`tasks.md` § Path Conventions marks it
   `MUST NOT implement`). The citation is a boundary statement, not a promise of an existing file.
2. `feature-ref.md:60` → `tests/contract/test_nested_run_report.py`. That test belongs to 074b together
   with the report section it pins (recorded decision D-3). Absent by design.
3. `checklists/requirements.md:62` → `feedback/20261028T160637Z-speckit-requirements.md`. The bundle
   **does** exist, at `.specify/memory/feedback/20261028T160637Z-speckit-requirements.md`; the checklist
   cites `.specify/memory/`-relative paths throughout (the same line cites `session/…` and
   `exec-quant/records/…` the same way), so this is a resolution-convention artefact rather than a
   missing artifact. The checklist is a dated record from an earlier stage; its citations are left
   byte-identical rather than rewritten in this stage.

### GATE-3 — decomposition size

```console
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074a-authorized-routing/requirements.md \
    --tasks .specify/specs/074a-authorized-routing/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 20, "task_count": 32,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T03:55:13Z"}
RC=0
```

### GATE-4 — clause coverage

```console
$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing
== clause coverage (universe: contract files per the owner's forms; claimed: tasks.md [green:] declarations) ==
claimed clauses (this feature): 47
== FR coverage (universe: requirements.md definition rows outside code spans; claimed: clause citation groups, never task rows) ==
FR universe: 20
FR claimed: 20
FR uncovered: 0

companion (must be non-empty on a green run): claimed clauses 47, scanned files 212, clause universe 1285, FR universe 20
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] pass (0) — baseline holds 495 names; 495 uncovered items are baseline-internal and do not block
uncovered beyond baseline: 0
0 error(s), 0 warning(s)
status: ok
RC=0
```

All 47 clauses are claimed exactly once, the FR lane is 20/20, and the uncovered count is 0 beyond the
frozen baseline — the `[clause-unparsable]` warn is the baseline's own parse-doubt class (0 of those
files declare a positive form), unchanged by this slice.

### GATE-8 / GATE-9 — no open rows, SC rows complete

Both are measured **after** T032 itself was closed, which is the only moment GATE-8 can be 0 — while the
last row is still open it reports 1, and that is what it returned on the first look. Stated explicitly so
the number is not read as a pre-close measurement:

```console
$ grep -cE '^- \[[ >]\]' .specify/specs/074a-authorized-routing/tasks.md   # before closing T032
1
$ grep -cE '^- \[[ >]\]' .specify/specs/074a-authorized-routing/tasks.md   # after closing T032
0
$ grep -cE '^- \*\*SC-00[1-6]\*\*' .specify/specs/074a-authorized-routing/verification.md
6
```

**Structural drift check**: no drift was found between the frozen task list and the delivered slice, so
no rerun row was appended and nothing was renumbered.

---

# -- DoD close --

- **DoD-1**: 32/32 rows `[X]`; `deferred_tasks=` empty (no `[~]` row exists).
- **DoD-2**: 15-row delivery surface as `feature-ref.md` § 2 declares — 9 new (3 framework sources + 5 test
  modules + 1 fixture) and 6 changed; zero new command, zero new skill.
- **DoD-3**: 47/47 clauses claimed once each; GATE-4 above.
- **DoD-4**: 5 new modules green (86 cases); zero new failed nodeids against the implement-start re-capture.
- **DoD-5**: 7 source/mirror pairs `cmp`-identical; `sync-mirrors.py --check` clean; `.specify/` mirrors
  were never hand-edited.
- **DoD-6**: the four routing facts land once (reverse count in `notes/quickstart-run.md` § Single-owner);
  zero new registry, ledger, state spine, ownership model, integration queue, confirmation gate,
  scheduler, daemon or automatic transfer (§ Structure).
- **DoD-7**: the six `- **SC-00N**` rows above carry status, command, output summary and evidence pointer.
- **DoD-8**: plan_constraint honoured — `plan_edit_count=0`, measured by an empty `git diff --stat` over
  every plan-owned path for the whole implement stage.
