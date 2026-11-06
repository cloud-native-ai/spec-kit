# SDD Review — Feature 088, Second Slice (Efficiency Dimension + `/speckit.measure`)

> **Scope**: delta review of the second slice only. The first slice's verdicts stand as recorded in
> `review.md` and are not re-adjudicated here.
> **Reviewer**: SDD Review Coordinator (`/speckit.review`, run r20261106T040353Z-087a-rev) · 2026-11-06.
> **Review is read-only over artifacts**: this file, the coverage receipt appended to `code-review.md`, and the
> captures under `test-evidence/review-second-slice/` are the only files this run wrote.

## 0. Baseline and Delta

| Field | Value |
|-------|-------|
| Requirements baseline | `ae5401a4` — FR-023…FR-029 / SC-011…SC-014; unit = the step `(unit_id, unit_type)` |
| Plan / data-model baseline | `6be09c3a` — contracts C-53…C-72 |
| Tasks baseline | `e922daec` + `a3d4be1a` — 73 rows; T055–T078 implemented by the second slice |
| Implementation commits | `97d3e8ab` (Part 7: element + measure engine + tests) · `70df8130` (Part 8: command + copies + mirrors + evidence) |
| Evidence commit | `50487649` (verification SC-011…SC-014 blocks) |
| Reviewed delta | `git diff a3d4be1a..50487649` — 46 paths (see the receipt in `code-review.md`) |
| Owner authority | `shared/guidelines/reporting-obligations.md` § 9.1 (the two render literals, step identity, latest-record rule) |
| Test budget | targeted suites + smoke only; the full suite was not run |

## 1. Process Segment — verdict: pass (with disclosed adjudications)

Commit-traced timeline for the slice (`bf22b7e2` → `50487649`): plan revision (`6be09c3a`, unit corrected to
the step per user adjudication `ae5401a4`) → tasks reset (`a3d4be1a`) → checklist/analyze round 5 → Part 7 →
Part 8 → evidence. Deviations found: none unrecorded.

The two Part 7 halts were resolved by **driver adjudications**, both recorded in
`test-evidence/second-slice-part7.txt` § 2 with a clause-by-clause conversion table. Checked for green-washing:

- Every old assertion is mapped to a new one **serving the same contract clause** (C-63/C-64/C-67/C-71 cases);
  nothing was deleted, only converted to the step-identity rule the requirements baseline owns. Verified
  against the commit: the four test files carry **2085 insertions, 0 deletions** — no clause coverage was
  removed in passing.
- The C-67 digest-side proposition moved to `test_status_digest.py::test_c55_a_listed_unit_with_no_record_…`,
  so the clause keeps a judge on both surfaces.
- § 4 of the same file discloses three in-passing corrections (tie direction, digest step-set fallback,
  field-slot literal composition) — see finding P2-2 for the third one.

**One process finding (P1-1) belongs to this segment**: the feature index row's Status cell was not moved by
the second-slice implement, see § 5.

## 2. Artifact Segment — verdict: pass (expected set 8/8 present; findings below)

Expected set: requirements.md, plan.md, data-model.md, contracts/ (8 files, C-01…C-72), quickstart.md, tasks.md,
verification.md, feature-ref.md — all present and read.

| Severity | Location | Finding |
|----------|----------|---------|
| P1 | `verification.md` § Joint acceptance (line ~172) | The note claims "Only RS-005 carries Form: in-scope", which the second slice's own requirements revision made false — RS-007 (`in-scope`) now also owes a `RS-007_joint_acceptance=` row. Its absence is exactly why the closure checker emits `runtime-dependency-not-owned: RS-007` (the `tasks.md` row match for FR-026 passes; the verification row is the missing conjunct). **The backfill belongs in `verification.md` only** — requirements and plan declare RS-007 correctly (owner column, SC-013/SC-014, FR-026…FR-029, EP-002) and need no edit. |
| P2 | `contracts/measure-report.contract.md` C-57 vs `scripts/python/measure.py::classify` | C-57 declares truncation "by the record's own identity (the record file's name stem) in ascending order"; the implementation sorts by `(str(collected_at), position-in-returned-list)` — the stamp first, and the position of a legacy-stream record is stream order, not an identity. Same retained count, potentially a different retained record when a unit exceeds the cap across mixed sources. The clause's judge (`test_c57_*`) asserts determinism and counts, never **which** record is retained — a green check that cannot go red on the deviation it claims to judge. |

## 3. Implementation Segment — verdict: pass (targeted suites green; two P-level code findings)

- Targeted re-run this session: `test_measure.py` + `test_measure_unit.py` + `test_efficiency_element.py` +
  `test_status_digest.py` → **91 passed** (Part 7's recorded reading reproduced exactly). Full suite not run (budget).
- Smoke: live `measure.py --action summary` exit 0 with the expected window/selection/cap header; `--action json`
  carries exactly the six C-60 keys. Captured verbatim in `test-evidence/review-second-slice/smoke-run.txt`.
- Windows/median/cap/exclusions/exit codes: exercised by the 24 contract tests; hand-checked against C-54…C-62.
  Read-only and single-read confirmed by `test_c62_*` and the AST audit (no spawn/network/write imports).
- Determinism: two runs byte-identical (`test_c57_two_runs…`, re-verified in evidence SC-014's run1/run2 diff).

| Severity | Location | Finding |
|----------|----------|---------|
| P1 | `scripts/python/measure.py` lines 430, 436 | The owner document § 9.1 declares **itself** the single definition point of the `no measurements` render literal; `status-digest.py` honours this by reading the owner at run time (`efficiency_vocabulary()`), but `measure.py` prints the literal **hard-coded**, twice, and reads no owner — a second copy of the one fact § 9.1 owns (constitution XIV). Fix: reach the literal through the same owner-reading path (or through the shared engine constant), never a second spelling. |
| P2 | `scripts/python/status-digest.py` lines 418–419 (and `measure.py` 56–57) | The Part 7 in-passing correction (c) satisfies the C-70/C-71 AST scans by **composing** the owned field slots part-wise — `"_".join(("elapsed","ms"))`, `"".join(("mo","de"))`. The scan goes green while the file still spells the field name, just split; the mechanical check therefore proves the letter of "no literal", not the substance of "reached through the owner". The genuinely owner-reached forms already exist alongside (`record.get("tokens")` rides the engine's records); the composed slots should read the node name from the engine/declaration instead. |

Positive checks (the brief's focus items, each verified):

- **Step identity and the two visible faces**: the line renders exactly the emitting step (1 element), the digest
  renders this run's or the most recent steps inside its existing cap, and neither face lets the store widen its
  step set (`project_efficiency` iterates only the host surface's steps). `select_latest_by_step` implements the
  one rule — greatest `collected_at`, tie by record identity ascending — and was corrected in passing to the
  ascending-first semantics C-66 declares (disclosed, reversible, matches the recorded intent).
- **Degradation is render-wide** (`resolve_depth` decides once over the widest element; `withheld_summary` names
  the withdrawn quantities in the existing omitted summary).
- **Owner literals referenced, not copied**: `not-evaluated` / `no measurements` in `status-digest.py` are read
  from `shared/guidelines/reporting-obligations.md` § 9.1 at run time (except the P1 above on `measure.py`).

## 4. Code Segment — verdict: pass

| Field | Value |
|-------|-------|
| Delta | `a3d4be1a..50487649`, 46 paths |
| Changed / judged / skipped / gap | 46 / 46 / 0 / 0 — receipt appended to `code-review.md` (dated second-slice section) |
| New suites | `test_measure.py` (24), `test_measure_unit.py` (7), `test_efficiency_element.py` (12), `test_status_digest.py` +8 → 91 green |
| Regression | none new: the four targeted suites are green at HEAD; the first slice's inherited reds (`baseline-failed.txt`) are out of this delta's files |
| Undeclared scope | none — every path in the delta maps to a T055–T078 row, a mirror/copies pair, or dated evidence |

## 5. Acceptance Reality Check (ARC)

| Field | Value |
|-------|-------|
| Checker | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/088-speckit-visualization --json` |
| `final_path` (verbatim) | pass **8** · blocked 0 · deferred 0 · partial **2** · fail 0 · unknown 0 · total **10** |
| Reasons | `final-path-not-pass: SC-001` · `final-path-not-pass: SC-002` · **`runtime-dependency-not-owned: RS-007`** |
| Completion conditions | `no_open_rows` ✓ (73/73) · `status_row_per_criterion` ✓ · `smoke_record_pass` ✓ · `every_final_path_pass` ✗ |
| Verdict | **block** (rc=1) |

**Status consistency — disagreement recorded, not repaired.** The checker reads
`claimed_status=Planned` from the `.specify/memory/features.md` row 087, while the honest state after the
second slice is **Blocked** (two final-path criteria remain `partial`; the feature's own detail page and the
first-slice review both carry Blocked). The second-slice implement (Parts 7–8) and the closure record never
moved the index row's Status cell back from the plan-stage `Planned`, so the checker's claimed-status
comparison currently runs against a stale value. The review stage does not own that cell; the finding is
handed to the driver:

| Severity | Finding |
|----------|---------|
| P1 | `.specify/memory/features.md` row 087 Status cell = `Planned` is stale against the delivered tree (final_path 8 pass / 2 partial ⇒ honest claim is `Blocked` with `final-path-not-pass: SC-001, SC-002`). Every closure re-run until the row is corrected will compare against `Planned`. |

**SC-011…SC-014 evidence reality** — all four `pass` rows bind to files whose sha256 re-computed this session
matches `verification.md` byte-for byte: `us5-efficiency-element.txt`, `us5-readonly-store.txt`,
`us5-measure.txt`, `success-criteria.txt`. The captures carry the real renders they claim (measured /
not-evaluated / absent-store faces, before/after store digests, the hand-computed expectation table with the
C-58 accounting identity, and the run1/run2 determinism diff). **Real, not asserted.**

**RS-007 answer (the brief's question)**: the `runtime-dependency-not-owned: RS-007` closure reason does **not**
require backfill in requirements.md or plan.md — both declare the row correctly. It requires one
`RS-007_joint_acceptance=` block in `verification.md` (the checker's third conjunct), plus correcting the
stale "Only RS-005 carries Form: in-scope" note above it.

## 6. Findings Summary

| Severity | Count | IDs |
|----------|------:|-----|
| P0 | 0 | — |
| P1 | 3 | stale features.md Status cell (§ 5); missing `RS-007_joint_acceptance` in verification.md (§ 2); `measure.py` hard-codes the owner § 9.1 literal (§ 3) |
| P2 | 2 | C-57 truncation order not implemented as declared and not judged (§ 2); part-wise composed field-slot literals game the C-70/C-71 scans (§ 3) |

## 7. Self-Containment Check

- [x] Every finding carries a location and enough quoted substance to judge without opening the file.
- [x] No verdict rests on a run this session did not record into `test-evidence/review-second-slice/`.
- [x] First-slice verdicts were cited, never re-adjudicated.
- [x] No P0 raised; the P0 independent-validation pass is vacuously satisfied.
