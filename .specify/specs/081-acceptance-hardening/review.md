# Review — Feature 081, slice 081b

**Date**: 2026-11-03
**Branch**: `081-acceptance-hardening`
**Reviewed range**: `97014440..4c07fdc9` (081b implementation). `90de4d7f fix(coaching-skills)` lies inside the broader history and is excluded from judgement, as in 081a. 081a's carriers `review-081a.md` / `code-review-081a.md` are untouched.
**Status**: `Blocked` — unchanged by this slice. SC-001 `blocked` (1/3 call sites), SC-002 `partial`, SC-005 `partial`; closure checker `block` / exit 1 / `zero-final-path-pass`

## Verdict

081b does land what it claims about its own fixtures: the five declarative fixture sets reproduce, the four findings fire from both producers on every mutation fixture and from neither on the two accepting ones, the targeted contract set is green, and both parity engines exit 0. The red-first note is honest — it records 17 red / 6 green with the six named, and §2.2 labels the 89-green run a diagnostic rather than a close record.

What it does not land is producer agreement on the shape a **real** spec has. On Feature 081's own `plan.md` the stage gate resolves none of the four dependency artifacts the plan declares, resolves the spec's own `requirements.md` / `tasks.md` / `research.md` / `verification.md` instead, and emits **nine fabricated** `inherited-blocker-undisposed: 081:*` reasons plus one false positive on the documented legal `inherited-later` reading — while the closure checker on the same tree resolves the declared 071/077 files and emits no inherited reason at all. That is defect 3 of the slice's own `notes/red-first-evidence-081b.md` §2.3, repaired in §2.4 in **one** of the two producers and never re-measured in the other.

Findings: **P0=1, P1=2, P2=4**; all repaired in the review-fix commit, each with a re-measured reading below. The feature stays `Blocked` for the reason the slice states (no closure call site; 081c/081d own the two remaining), not because of these findings — though F1 also means the gate would refuse this feature's own plan stage today, which is a second, independent reason not to read this slice as clean.

## Findings and disposition

| ID | Severity | Location | Finding | Disposition |
|---|---|---|---|---|
| F1 | **P0** | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:621` (`declared_dependency_files`); `notes/red-first-evidence-081b.md` §2.4 repair #3; `tasks.md` § Notes "One closed set, two producers" | The dependency-declaration repair landed in the closure checker only. The gate still joins **every** backticked `.md` token in § Inherited Blockers against the spec dir, so on this feature's own plan it resolves `requirements.md`, `tasks.md`, `research.md`, `verification.md` (measured) and emits nine fabricated `081:SC-00N_status` / `081:deferred_tasks` reasons — the exact defect §2.3 recorded — while discovering **none** of the declared `071` / `077` artifacts. `--stage plan --spec-dir .specify/specs/081-acceptance-hardening` → exit 1, 10 errors. No post-implementation plan-stage reading on a real spec exists in the evidence; the only one (`test-evidence/checklist-081b-probes.txt` P5, `decision=pass errors=0`, commit `43b0e668`) predates the findings' implementation. Contradicts FR-011 ("declared, never implied"), the declared block at `plan.md:240`, and the cross-producer premise of GATE-5 / `test_acceptance_premises.py` leg (d) | **Fixed**: the gate now reads only the `**Dependency artifacts` block (same parser as the closure checker) and resolves the declared 071/077 files; measured plan gate `decision=pass errors=0`, closure `block` / `zero-final-path-pass`; new leg (d2) runs both producers on this spec dir |
| F2 | P1 | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:761` (`later_slice_is_legal`); `plan.md` § Inherited Blockers IB-004 | `inherited-later` is unreachable at the gate: the claimed status is read from `<spec-dir>/feature-detail.md`, a fixture-only filename. A real spec dir has none (measured `False`), so `Carrier slice = 081c` never becomes legal and IB-004 (a `test:`-only carrier, the documented `inherited-later` form) is emitted as `inherited-blocker-undisposed: 071:SC-006_status`. The closure checker reads the claimed status from `.specify/memory/features.md` and treats the same row as legal. Contradicts FR-011's "`inherited-later` … MUST NOT 当作未处置" and owner § `inherited-later` — a fourth *reading*, never a fourth disposition | **Fixed**: `resolve_claimed_status()` reads the same carriers as the closure checker (spec-dir detail/registry, then `.specify/memory/features.md`); the gate accepts IB-004's `test:`-only later-slice carrier |
| F3 | P1 | `scripts/python/closure-acceptance-check.py:983`; `shared/workflow/acceptance-hardening.md:350`; `templates/plan-template.md:180` | The declared-dependency block's marker is an undocumented literal. `declared_dependency_files()` reads only paths after the exact string `**Dependency artifacts`, and returns `[]` — silently — for any other wording; the owner's rule ("The plan states which dependencies it read") and the skeleton future plans inherit (`templates/plan-template.md:182`) never give the marker's shape. Measured probe: rewording the marker in `inherited-mutation` drops `inherited-blocker-undisposed: 901:SC-004_status` (2 reasons → 1, still exit 1) with no input error — a compliant plan can leave the fourth finding permanently unable to fire, which is the false-green class this feature exists to remove | **Fixed**: the marker is published in the owner and the plan skeleton; a dependency set without the block is exit 2 at both producers; legs (d3)/(d5) assert it |
| F4 | P2 | `pre-analyze-check.py:124` and `closure-acceptance-check.py:222` (`ABSENT_LOCATORS`) | `Source row` accepts `(none)` / `none` / `n/a` / `(no dependency)` — a sentinel documented nowhere — while rejecting `—`, the emptiness spelling used in every other cell of the same tables. Measured: `(none)` → accept; `—` → input error (exit 2) at both producers. All ten fixture sets and the three pin-adjusted unit fixtures depend on the undocumented form | **Fixed**: `—` is accepted alongside `(none)` and documented as the absent-row sentinel; leg (d4) measures it |
| F5 | P2 | `verification.md:7`, `verification.md:99` | The slice updated `verification.md` but not its own carrier fields. `post_change_commit=8ce0f006` is an 081a-era commit (this slice closes at `4c07fdc9`), and `deferred_tasks=T024` no longer mirrors anything: `templates/verification-log-template.md:152` defines the field as "mirrors `[~]` rows in tasks.md", `tasks.md` has **0** `[~]` rows and no row `T024` (`grep -c T024` = 0), and the checker's own payload reports `tasks.deferred=0`. A future dependent feature would extract `081:deferred_tasks` as a live locator — the invented-locator defect the join key exists to prevent | **Fixed**: `post_change_commit=4c07fdc9`; `deferred_tasks=` is empty and the note records that 081a's T024 is not a row of this slice |
| F6 | P2 | `tasks.md:18` vs `tasks.md:234` | The same file states two different premise ranges for the parent plan (`EP-001…EP-010` in § Parent Context, `EP-001…EP-009` in § Notes); `plan.md` § Execution Premises defines **10** rows | **Fixed**: `EP-001…EP-010` |
| F7 | P2 | `data-model.md:195` | The `inherited-clean` census is stale: it lists five dispositions (`two resolved, one not-applicable, one inherited, one inherited-later`) while the fixture carries **six** rows — the second `inherited` row and its `gate:GATE-1` carrier form are missing from the description. The fixture's own header comment counts them correctly | **Fixed**: the census now lists all six rows, including the second `inherited` row and its `gate:GATE-1` carrier |

## What reproduces (read-only re-runs, this review)

| Claim in the slice's artifacts | Command run here | Result |
|---|---|---|
| closure verdict / acceptance summary | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening --json-out .specify/.tmp/review-081b-verdict.json` | `verdict: block`, `claimed_status: Blocked`, `final_path: pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2`, `reason: zero-final-path-pass`, exit 1 |
| `test-evidence/closure-verdict-081b.json` is a copy, not a recount | `diff .specify/.tmp/review-081b-verdict.json .specify/specs/081-acceptance-hardening/test-evidence/closure-verdict-081b.json` | no output — byte-identical |
| T012 close record `89 passed` | `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py tests/contract/test_closure_acceptance_check.py tests/contract/test_expression_gates_doc.py tests/contract/test_expression_gate_wiring.py tests/contract/test_premise_carrier_contract.py -q` | `89 passed in 4.90s`, exit 0 |
| GATE-3 parity | `python3 scripts/python/sync-mirrors.py --check`; `python3 scripts/python/regen-command-copies.py --check` | exit 0 / exit 0 (22 / 409 / 136 / 3 / 119 / 62 files) |
| GATE-5 both producers, both directions | fixture loop over `premise-mutation`, `runtime-gap-mutation`, `runtime-zero-row`, `inherited-mutation`, `inherited-clean`, `positive`, `negative` | each mutation blocks with the instances `MUTATIONS` names (`RS-905` + `RS-001`; `runtime-stack`; `901:SC-003_status` + `901:SC-004_status`); `inherited-clean` and `positive` accept (exit 0) from both producers |
| GATE-6 status unmoved | `awk` on `.specify/memory/features.md`; `.specify/memory/features/081.md` | `Blocked` / `**Status**: Blocked` |
| § Environment Prerequisites probes | `python3 --version`; `.venv/bin/python -m pytest --version`; `git --version` | `Python 3.9.6`; `pytest 9.2.0`; `git version 2.54.0 (Apple Git-157)` — all three match the recorded text |
| T011 preserved 081a's smoke record | `diff <(git show da5e4480:…/smoke-081.txt) …/smoke-081a.txt` | identical |
| "the red is a measurement, not a restatement" | read `notes/red-first-evidence-081b.md` §1.1 / §3 | 17 failed / 6 passed with the six named; the pre-authoring run is `exit 4` (`ERROR: file or directory not found`) and is labelled absence, not green — honest |

## Acceptance Reality Check

```
$ python3 scripts/python/closure-acceptance-check.py \
      --spec-dir .specify/specs/081-acceptance-hardening \
      --json-out .specify/.tmp/review-081b-verdict.json
verdict: block
flow_class: execution
claimed_status: Blocked
final_path: pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2
reason: zero-final-path-pass
EXIT=1

completion_conditions  every_final_path_pass=false  no_open_rows=true  smoke_record_pass=true  status_row_per_criterion=true
tasks                  closed=12  deferred=0  in_progress=0  open=0     (slice 081b's tasks.md)
smoke                  present=true exit_code=0 records=1 evidence_exists=true
payload                .specify/.tmp/review-081b-verdict.json == test-evidence/closure-verdict-081b.json (byte-identical)
```

`Blocked` is the honest state and this review does not move it: no final-path criterion passes, the two `final` criteria read `blocked` (SC-001, 1/3 call sites) and `partial` (SC-002, the review-site fourth condition is 081c), and `Blocked → Ready for Review` is illegal by design. `Implemented` is not reachable and no artifact of this slice reads as if it were.

The second producer does not agree with this payload on the same tree: `pre-analyze-check.py --stage plan --repo . --spec-dir .specify/specs/081-acceptance-hardening` exits 1 with 10 `inherited-blocker` errors (9 fabricated, 1 a legal `inherited-later` row). That disagreement is F1 + F2; it is recorded here rather than scored into the ARC, whose contract is the closure verdict only.

## Scope of the remaining work

- **081b review-fix**: F1 (make the gate honour the same declared block the closure checker honours, or make both read one declaration), F2 (resolve the claimed status the way the closure checker does, not from a fixture-only filename), F3 (publish the declaration marker in the owner and the plan skeleton, and make an absent or misshapen declaration an input error instead of an empty extraction set), F4–F7 (artifact corrections).
- Re-run after the fix: the plan-stage gate **and** the closure checker on `.specify/specs/081-acceptance-hardening` itself, and add that pair to `test_acceptance_premises.py` — leg (d) currently proves agreement only on fixtures, whose shapes differ from a real plan in exactly the two ways that fail (fixture-local dependency filenames; a `feature-detail.md` in the spec dir).
- **081c**: `review-feature-quality`, the four-segment composition, the review call site, IB-004's carrier completed to `task:<T-ID>+test:<path>`.
- **081d**: `manage-features` / feature-index vocabularies, `--audit-existing`, driver line-state `blocked` and the driver closure/merge site, the schema-ownership guard, the feature-level baseline re-run, final smoke.
- T024 (081a) remains 081d's; the registry still reads `Blocked` while `manage-features` does not yet admit it — the documented window, not a pass.

## Review-fix outcome (post-review)

All seven findings were repaired in the review-fix commit. The two producers now agree on the
**real spec shape**, not only on the fixture shape:

| Reading | Command | Result |
|---|---|---|
| plan-stage gate on this spec dir | `pre-analyze-check.py --stage plan --repo . --spec-dir .specify/specs/081-acceptance-hardening --json-out …` | `decision=pass`, `errors=0`, `advisories=45` (planned-path advisories for 081c/081d deliverables), exit 0 |
| closure checker on this spec dir | `closure-acceptance-check.py --spec-dir … --json-out …` | `verdict=block`, `zero-final-path-pass`, `final_path 0/1/0/1/0/0/2`, exit 1 |
| both producers on the real dir | `test_acceptance_premises.py::test_d2_the_real_spec_dir_emits_no_phantom_inherited_row` | green — no `081:*` row, no `inherited-blocker-undisposed` reason |
| declaration absence | `test_d3_a_dependency_set_without_the_declaration_block_is_an_input_error` | green — exit 2 at both producers |
| absent-row sentinel | `test_d4_a_dash_source_row_is_the_absent_sentinel` | green — `—` accepted |
| marker publication | `test_d5_the_declaration_marker_is_published_once_in_the_owner_and_the_skeleton` | green |
| targeted set | `run-tests.sh … -q` (8 modules) | `145 passed`, exit 0 |

Evidence: `test-evidence/review-fix-081b-gates.txt`, `test-evidence/review-fix-081b-plan-gate.json`,
`test-evidence/closure-verdict-081b.json`, `test-evidence/tasks-081b-review-fix-tests.txt`.
The feature **still reads `Blocked`**: 081b adds no closure call site, and SC-001 / SC-002 are
081c / 081d's to complete.
