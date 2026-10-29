# Verification Log — 074b-nested-governance

Shape follows `.specify/templates/verification-log-template.md`; every `status` value below is drawn
from that template's closed vocabulary (`pass | fail | partial | deferred | unknown`) and nothing
narrower. Every `pass` carries a complete evidence row (`sample_id` / `evidence_path` /
`evidence_sha256` / `verdict`), hashed over the archived file's bytes with `sha256sum`.

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=241a6082b40e7eb412de8143d0d0fbc52014967f
baseline_date=2026-10-29
baseline_branch=074b-nested-governance

baseline_full_suite_passed=6452
baseline_full_suite_failed=21
baseline_targeted_set_collected=290
baseline_targeted_set_passed=289
baseline_targeted_set_failed=1
baseline_mirror_pairs_clean=6
baseline_instruction_template_bytes=34666
baseline_instruction_live_bytes=41948
baseline_flow_class_units=79

> Owners of those numbers: the full-suite slot is `test-evidence/implement.jsonl` `seq=1`
> (`test-evidence/implement-baseline-run.txt`, 21 pre-existing failures named in
> `baseline-failed.txt`); the targeted set is `test-evidence/targeted-set-v1-baseline.txt` (T002
> re-capture at this commit); the mirror / size / flow-class baselines are
> `notes/pre-change-measurements.md` § 1 / § 3 / § 6.

# -- /speckit.implement results --

implementation_date=2026-10-29
post_change_commit=182f526a5

> `post_change_commit` is the commit at which **every measurement in this file was taken** (T024's
> structure commit, the last one before this file landed). The sections below landed in the commits
> after it — the SC verdicts and DoD close in the commit that carries this file, the gate re-runs in
> the next one — so no commit hash here claims to contain them. § Gates records the recorded tip at
> gate time, and every gate block carries its own `checked_at` / run timestamp. (This is the
> `post_change_commit` trap a sibling slice's review flagged as F5; here the field names the measured
> tree state instead of guessing at a later commit.)

post_change_full_suite_passed=not-evaluated
post_change_full_suite_failed=not-evaluated
post_change_targeted_set_collected=338
post_change_targeted_set_passed=337
post_change_targeted_set_failed=1
post_change_new_failed_nodeids=0
post_change_mirror_pairs_clean=6
post_change_new_test_modules=3
post_change_new_tests=42
post_change_flow_class_units=79

> `post_change_full_suite_*=not-evaluated`: the closure full-suite slot was not spent in this stage.
> The E2 baseline slot was consumed at implement start (`test-evidence/implement.jsonl` seq 1, `6452
> passed / 21 failed`) and the dispatch forbids a second full run; the closure slot belongs to the
> driver after `/speckit.review`. Nothing here claims a full-suite result that was not measured.
> `post_change_new_failed_nodeids=0` is the `comm -13` result over node-id **names**, not a count
> difference (`notes/pre-change-measurements.md` § 11).

# -- Evidence records (bind every `pass` claim to an archived file) --

sample_id=SC-001
evidence_path=.specify/specs/074b-nested-governance/notes/pre-change-measurements.md
evidence_sha256=319f81a9b09ddfd08b349ed8e0a804216b649bdceba9c8eb84b1f9c526dcfb9e
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/074b-nested-governance/notes/quickstart-run.md
evidence_sha256=2854caff96ee4aab6d7d431f5e96231af8a58355e34d9585cb9d99bcf7694092
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=7 named node-id sets / 17 files / 266 pre-change cases: post ⊇ pre with dropped=0 in every set (S1 dropped=0 added=6, S2–S7 dropped=0 added=0), and the same 17 files executed after the change give 272 passed / 0 failed, so every shared id keeps its verdict; the targeted re-run gives 338 collected / 337 passed / 1 failed with `comm -13` empty against the T002 re-capture (and `comm -23` empty too)
SC-001_note=Both halves of the claim are discharged and neither is a count comparison: T018 compares the collected case ids per named set, T023 compares failing node ids by name. The single pre-existing red (`test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`, gate total 27 vs its frozen 23) lies outside the 7 sets, stays red with its integer unmoved, and is claimed by nobody.

SC-002_status=pass
SC-002_value=`parse_goal` over the fixture Goal returns the same 12 fields before and after the attribution row (`identical: True`; `goal.md` 224 B unchanged); attribution lands only as the existing ledger `target_ref`, and no Goal field or Goal→requirements link is added
SC-002_note=Measured twice on two independent fixtures — quickstart S3 over a goal fixture, and `test_nested_run_report.py::test_attribution_is_observational_so_the_goal_field_set_is_unchanged` over the `074a` fixture — so the property is measured, not asserted once.

# -- Per-SC rows (one line each: status · command · output summary · evidence pointer) --

- **SC-001** — status `pass` · commands `python3 -m pytest --collect-only -q <the 17 files of the 7 named sets>`, `bash scripts/bash/run-tests.sh <the same 17 files>`, and `bash scripts/bash/run-tests.sh --names-out … <19 baseline files + this slice's 3 suites>` · output `S1 pre=49 post=55 lost=0` … `S7 pre=38 post=38 lost=0`, `272 passed`, `1 failed, 337 passed` with `comm -13` empty · evidence `notes/pre-change-measurements.md` § 10 and § 11, `test-evidence/containment-post-change-collect.txt`, `test-evidence/implement-targeted-part4-run.txt`, quickstart `notes/quickstart-run.md` § S6.
- **SC-002** — status `pass` · commands `python3 scripts/python/goal-utils.py … create` + `parse_goal` before/after the ledger row, and `python3 -m pytest -q tests/contract/test_nested_run_report.py -k attribution` · output `field_set: ['boundaries', …, 'updated']` (12 keys), `identical: True`, `goal_md_bytes: 224` · evidence `notes/quickstart-run.md` § S3, `tests/contract/test_nested_run_report.py`.

# -- Requirement faces without an SC --

`requirements.md` declares 2 SC for 8 FR. The six FR rows below carry no success criterion of their
own; each is graded by a named test and a task row instead, and none is waived:

- **FR-001 / FR-002** → measured by SC-002 (attribution face) and SC-001's regression set
  (`test_nested_run_report.py`, 16 cases; task rows T005–T009).
- **FR-003** → `tests/contract/test_sdd_diffusion.py` C-13 / C-14 cases (Stage values unchanged,
  disambiguation present, roster owner named); task row T011.
- **FR-004** → the same suite's C-15…C-17 cases (declaration and the three responsibility statements
  read together; the shipped leaf preset declares nothing); task row T012.
- **FR-005** → the same suite's C-18 / C-19 / C-20 cases (exactly one pointer section, reverse-count
  audit 0, the trigger's `## ` section set unchanged); task rows T013–T015.
- **FR-006 / FR-007 / FR-008** → SC-001 (both containment halves) plus
  `tests/contract/test_sdd_compat_containment.py` (11 cases: four-surface additivity, safety
  negatives, zero new command / skill / store); task rows T017–T020, T024.

# -- plan_constraint declarations (this pass) --

plan_edit_count=0

> No line of a plan-owned surface was edited during this implement stage. Measured, not asserted:
> `git diff --stat 241a6082b..HEAD -- plan.md data-model.md contracts quickstart.md research.md
> feature-ref.md` (paths under this spec directory) prints nothing. There is therefore no
> `PLAN-EDIT:` line to declare and no substantive change to halt on.

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=The classification-honesty audit duty that T023 assigns (`/speckit.review` is that surface)
is left to the review stage: this file records the measured base it will read — the node-id
comparison, the disclosed pre-existing red, the E3 targeted row — and writes no adjudication back.
The single pre-existing red is disclosed in three places (`baseline-failed.txt`,
`targeted-set-v1-baseline.txt`, `notes/pre-change-measurements.md` § 11) and repaired nowhere, per
the slice's own criterion ("this slice's edit does not move the total", measured 27 = 27).

# -- DoD close --

- **DoD-1**: 26/26 rows `[X]`; `deferred_tasks=` empty (no `[~]` row exists).
- **DoD-2**: the 9-row delivery surface as `feature-ref.md` § 2 declares — 3 new test suites
  (`test_nested_run_report.py` 16 cases / `test_sdd_diffusion.py` 15 / `test_sdd_compat_containment.py`
  11) and 6 edited files (5 framework sources + `test_sdd_invocation_governance.py` in the superset
  direction), plus the generator-produced `.specify/instructions.md`; zero new command, zero new
  skill, zero new fixture (`tests/fixtures/nested_sdd.py` reused unchanged).
- **DoD-3**: 30/30 clauses claimed once each; `account-clause-coverage.py` reports `claimed clauses
  (this feature): 30`, `FR 8 / 8`, `uncovered beyond baseline: 0`, `status: ok` (§ Gates).
- **DoD-4**: three new suites green (42 cases); the edited governance suite keeps its 17 original
  propositions and adds 6 absent-declaration cases; zero new failed node ids against the T002
  re-capture (§ 11's two `comm` results); the pre-existing red unmoved.
- **DoD-5**: every Mirror Obligations row discharged — five source↔`.specify/` pairs `cmp`-identical,
  `sync-mirrors.py --check` clean on all six pairs, `regen-command-copies.py --check` `OK`, a second
  `generate-instructions.sh` run byte-identical (same sha256), four compatibility symlinks intact,
  zero hand-edited mirror (`notes/quickstart-run.md` § refresh).
- **DoD-6**: `## Nested SDD Runs` lands once, in the report contract's owner section (reverse-count
  audit in `notes/red-first-evidence.md`); Stage values byte-identical; the roster, routing input set /
  value domains / verdict table / reason codes and the neutral key values are reached by path only;
  zero new registry, ledger, state spine, ownership model, integration queue, confirmation gate,
  scheduler, daemon or automatic transfer (`notes/quickstart-run.md` § structure).
- **DoD-7**: the two `- **SC-00N**` rows above carry a closed-vocabulary status, the command, an
  output summary and an evidence pointer; the only `not-evaluated` quantities are the full-suite pair,
  each with its reason and no number substituted.
- **DoD-8**: both containment claims are decided on node-id **name sets** (post ⊇ pre, shared ids
  verdict-unchanged) over the 7 named sets in `test-evidence/compat-baseline-nodeids.txt`; no count
  comparison is used as evidence (§ 10 of `notes/pre-change-measurements.md`).
- **DoD-9**: plan_constraint honoured — `plan_edit_count=0`, measured by an empty `git diff --stat`
  over every plan-owned path for the whole implement stage.

# -- Gates (tasks T026, re-run against the frozen task list) --

Four gate commands in the order `tasks.md` § Completion Gate names them, plus the two
measured-after-close items and the evidence-binding check. Real output verbatim; the frozen list was
not renumbered and no rerun row was appended. Recorded tip at gate time: `820f65062` (the four
commands ran while T026's own row was still open — GATE-8 is measured after closing it, below).

### GATE-1 — task-file structure

```console
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md
PASS: .specify/specs/074b-nested-governance/tasks.md — 0 error(s), 0 warning(s)
rc=0
```

### GATE-2 — cross-artifact consistency

```console
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=0 waived=0
{"stage": "tasks", "decision": "pass", "findings": [], "summary": {"errors": 0, "advisories": 0,
 "waived": 0, "fr": 8, "sc": 2, "tasks": 26, "clauses": 0, "files": 12},
 "checked_at": "2026-10-29T06:38:46Z"}
rc=0
```

**Advisories**: there are none to adjudicate. The tasks-stage run reported 21 `missing-path`
advisories naming the three contract-test files T004 / T010 / T019 would create; those files now
exist, so the same command returns a clean report. The count moving is the expected consequence of
the slice landing, not a waived finding.

### GATE-3 — decomposition size

```console
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074b-nested-governance/requirements.md \
    --tasks .specify/specs/074b-nested-governance/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 8, "task_count": 26,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T06:38:53Z"}
rc=0
```

### GATE-4 — clause coverage

```console
$ python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance
claimed clauses (this feature): 30
baseline: .specify/specs/074b-nested-governance/coverage-baseline.txt (495 names)
baseline-internal existing uncovered: 495
uncovered beyond baseline: 0

FR universe: 8
FR claimed: 8
FR uncovered: 0

companion (must be non-empty on a green run): claimed clauses 30, scanned files 215,
clause universe 1315, FR universe 8
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 8 of 8 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them
    declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] pass (0) — baseline holds 495 names; 495 uncovered items are
    baseline-internal and do not block
0 error(s), 0 warning(s)
status: ok
rc=0
```

All 30 clauses are claimed exactly once, the FR lane is 8/8, and nothing is uncovered beyond the
frozen baseline. The `[clause-unparsable]` warn is the baseline's own parse-doubt class (0 of those
94 files declare a positive form) and is unchanged by this slice.

### GATE-5 / GATE-6 / GATE-7 — measured by the tasks that own them

These three are not re-run here because each already has a single owner and a single measurement, and
a second run would only produce a second copy of the same comparison:

- **GATE-5** (zero new failing node ids) → T023, `notes/pre-change-measurements.md` § 11:
  `comm -13` empty **and** `comm -23` empty against the T002 re-capture; 338 collected, 337 passed,
  1 failed.
- **GATE-6** (mirror and command-copy drift) → T021/T022, `notes/quickstart-run.md` § refresh:
  `sync-mirrors.py --check` clean on all six pairs with the T001 file counts (22 / 406 / 136 / 3 /
  114 / 59), `regen-command-copies.py --check` `OK`, five `cmp`-identical pairs, second generator run
  byte-identical (sha256 `23aaf2684c7fab9f31846e930d0cdf0c7a9ada19a74547dcbdf349862cbbeebb`).
- **GATE-7** (zero new storage surface) → T024, `notes/quickstart-run.md` § structure:
  `.specify/state/` (3 names) and `.specify/memory/` (681 names) both `comm -13` and `comm -23`
  empty.

### GATE-8 / GATE-9 — no open rows, SC rows complete

Measured **after** closing T026's own row, which is the only moment GATE-8 can be 0:

```console
# before closing T026 — read from the commit that still carried the open row
$ git show 820f65062:.specify/specs/074b-nested-governance/tasks.md | grep -cE '^- \[[ >]\]'
1
# after closing T026 — the working tree
$ grep -cE '^- \[[ >]\]' .specify/specs/074b-nested-governance/tasks.md
0
$ grep -cE '^- \[[xX]\] T[0-9]+' .specify/specs/074b-nested-governance/tasks.md
26
$ grep -cE '^- \[~\]' .specify/specs/074b-nested-governance/tasks.md
0
$ grep -cE '^- \*\*SC-00[12]\*\*' .specify/specs/074b-nested-governance/verification.md
2
```

### Evidence binding — every `pass` row re-hashed at gate time

```console
$ python3 - <<'PY'   # parse the evidence rows, recompute SHA-256 over each archived file
  SC-001: exists=True bytes=15028 sha_match=True verdict=pass -> BOUND
  SC-002: exists=True bytes=18811 sha_match=True verdict=pass -> BOUND
BINDING: green
rc=0
```

Both `pass` rows are complete and bound: the archived artifacts exist, are non-empty, and their
computed digests equal the recorded ones. No `pass` in this file is `unverified`.

**Structural drift check**: none was found between the frozen 26-row list and the delivered slice, so
no rerun row was appended and nothing was renumbered. The four gate commands above therefore ran
against the same list T026 was written against.
