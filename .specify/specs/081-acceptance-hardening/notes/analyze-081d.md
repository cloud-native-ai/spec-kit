# Analyze — slice 081d (US4 + final wiring: vocabulary owners, `--audit-existing`, driver line state, mirrors, feature-level close)

**Stage**: `/speckit.analyze`, read-only cross-artifact consistency analysis of the 081d artifact set.
**Inputs read**: `requirements.md` (FR-001…FR-025, SC-001/002/003/005/007/008/009, Assumptions A5/A6, `## Shared Strings`), `plan.md` (§ D1/D3/D4/D6/D8/D10, § Execution Premises, § Inherited Blockers, § Mirror Obligations), `tasks.md` (T001–T018, DoD-1…DoD-10, GATE-1…GATE-9, § Environment Prerequisites, § Slice Boundary, § No Deferred Slice), `data-model.md` (§ Fixture set, E-8/E-9, V-13/V-23), all five `contracts/`, `shared/workflow/acceptance-hardening.md` (§ Declared carriers, § Verification Vocabulary, § Extension Points), `checklists/081d-2026-11-03.md`, `verification.md`, `tasks-081b.md` / `tasks-081c.md` (archived precedent), and the live surfaces the artifacts assert against: `skills/external/sdd-loop-driver/scripts/{line-registry,integrate-lines}.py`, `scripts/python/closure-acceptance-check.py`, `tests/contract/{test_acceptance_state_machine,test_gate_wiring_081}.py`, `tests/integration/test_acceptance_smoke.py`, `tests/fixtures/acceptance-hardening/*`, `templates/{feature-index-template,plan-template}.md`, `templates/commands/review.md`, `skills/internal/manage-features/SKILL.md`, `.specify/memory/features.md`, `.specify/memory/features/081.md`.
**Findings**: `test-evidence/analyze-081d.jsonl` (29 rows).
**Scope discipline**: no artifact was edited. The only files this stage writes are this report and the JSONL. `git status --porcelain` shows exactly one new path at the moment of writing (`?? …/test-evidence/analyze-081d.jsonl`); no test module, no framework source and no upstream spec file was touched. No full suite was run.

## Counts

| Severity | Count | Meaning (scale used here, continuous with `notes/analyze-081c.md`) |
|---|---|---|
| C | 2 | contradiction that makes a criterion unsatisfiable or lets a `final` criterion be claimed on evidence its own record calls insufficient |
| H | 9 | defect that would let a wrong implementation pass, or that leaves a required wiring with no defined input / no red-able carrier |
| M | 12 | ambiguity, underspecification or duplication with real drift risk |
| L | 6 | wording, arithmetic, carrier and traceability hygiene |
| **Total** | **29** | 25 rows cover the 25 checklist FAILs one-to-one (3 of them at a downgraded severity); 4 rows are new (F-01, F-10, F-24, F-29) |

Lane distribution: `coverage-gap` 9, `inconsistency` 8, `ambiguity` 8, `constitution-conflict` 1, `underspecification` 1, `measurability` 1, `feature-line-consistency` 1.

## Gate verdict

**`fail`** — 2 C and 9 H remain after independent adjudication. The slice is not ready for `/speckit.implement`:

- **F-01 (C)** must be decided before T004/T017: SC-002's `pass` is currently reachable with a measurement that `verification.md` itself records as insufficient, and that measurement was already taken by 081c.
- **F-02 + F-03 + F-04 (C/H/H)** must be decided as one group before T014: the schema-uniqueness guard's `expected` list has two mutually exclusive authorities, three of the four named exemptions cannot be hit by the scan, and the "mechanically derived literal set" cannot exclude unrelated closed sets (measured: 11–29 files depending on the set chosen).
- **F-05 + F-06 (H/H)** must be decided before T008/T013: the audit root contradicts a MUST-level contract clause, and "the feature line's spec directory" has no data source.

The other H rows (F-07, F-08, F-09, F-10, F-11) are single-sentence specification repairs but each one currently allows a green reading that is not evidence.

## Checklist adjudication (25 FAIL items, independently re-derived)

Verdicts: **confirm** = the checklist's gap holds as written; **confirm (refined)** = the gap holds, the stated support is partly wrong; **downgrade** = a real defect, but the stated severity or the stated consequence is overstated.

| CHK | Checklist | Verdict | Sev | Finding | Reason |
|---|---|---|---|---|---|
| CHK001 | FAIL P2 | confirm | L | F-23 | Verified: tasks.md:233 heading asserts "exactly one owning slice" (restated tasks.md:210, plan.md:335) while the roster assigns FR-011 and FR-022 to three slices and six others to two. Real, but nothing is dropped and no gate reads it — lowered to L. |
| CHK007 | FAIL P1 | confirm | M | F-13 | Verified verbatim at all four locations: three vocabulary owners (requirements:161), four `blocked` literal owners (SV-01), four declared carriers (owner doc 12-19), four exemption members (requirements:211). The owner doc does claim identity between the last two. Real; lowered to M because F-02 carries the load-bearing half. |
| CHK009 | FAIL P2 | **downgrade** | L | F-25 | The bullet does carry two obligations and T002 deletes it whole — verified. But the second obligation is not left unpromised: T010 (tasks.md:137) restates it **with the same measured note** and carries `[blockedBy: T003]`, and SV-06 keeps the note. "既无正文也无承诺" is false. Bookkeeping wart, not a dropped obligation. |
| CHK010 | FAIL P2 | confirm | M | F-14 | Verified: FR-020 "现有 `Implemented` 特性" (requirements:163), SC-007 defines no population (:209), T013 coins "the `Implemented` family" (tasks:140) and no artifact defines it. Four contract clauses say only "per affected feature". |
| CHK011 | FAIL P1 | confirm (refined) | H | F-05 | Verified and sharpened by running the script: the mode check at `:1296` fires **before** the `--spec-dir` requirement at `:344`, so `--audit-existing` with no `--spec-dir` exits 2 with the mode message — `--spec-dir` is *already* unenforced in audit mode, silently. GATE-6 (tasks:49) still invokes the single-feature shape. |
| CHK012 | FAIL P1 | confirm (refined) | H | F-08 | The **case** is assigned to 081d (data-model:206); the **shape** is not — data-model:182 states the opposite rule ("a minimal file set … no case references a real feature directory") and "self-contained audit root" is 0 hits. |
| CHK013 | FAIL P2 | confirm | M | F-15 | Verified: C-03 (:14) puts the spec-local layer first; audit enumerates from registry rows. No audit branch, and all 15 existing cases exercise only the spec-local layer, so the corpus cannot answer it. |
| CHK014 | FAIL P2 | confirm (refined) | M | F-16 | The half is worse than vacuous in the direction the checklist gives (it is sensitive to in-repo writes) and better in none: because the audited tree is the `tmp_path` copy, `git status --porcelain` on the repository observes a **different tree** than the one under test. Confirmed with the refinement, not as "恒为空". |
| CHK016 | FAIL P2 | confirm | M | F-17 | Verified: `:41-42` docstring and `:1295-1296` both say "not implemented in this slice"; T013 removes the gate and the raise but not the docstring. Added: the docstring's `plan.md § Slice Boundary` reference is wrong (`grep -c 'Slice Boundary' plan.md` → 0; the section is tasks.md:208). |
| CHK019 | FAIL P1 | confirm | H | F-07 | Verified: `integration-record` requires `state=completed` (:1682) while A6 item 5 requires it unreachable from `blocked` — the record-then-transition order is forced, appears only as narrative sentence order in T008, and T005 has no leg for it. |
| CHK020 | FAIL P1 | confirm | H | F-06 | Verified: 0 occurrences of `spec_dir|spec-dir|feature_key|feature_id` in line-registry.py; `register` writes no feature field; the gate runs `cwd=wt`. No data source, and no rule for resolving relative to the worktree. |
| CHK021 | FAIL P2 | **downgrade** | L | F-26 | Both halves are pinned in substance: item 7's second half turns the T005 recovery leg red if `:764` is not widened (the checklist concedes this), and item 2's three sub-behaviours all read `state == "active"` in code this slice does not touch. What is missing is the literal correspondence, not the assertion. |
| CHK022 | FAIL P2 | confirm (refined) | M | F-18 | Verified, plus one fact the checklist did not have: `closure-blocked` occurs **nowhere outside the 081 spec** (grep), is in no `*_REASONS` constant (`WAITING_REASONS` only, :54), and `--reason` is free text — so it is an unowned literal with an unpinnable spelling. |
| CHK026 | FAIL P2 | confirm | M | F-19 | Verified: the merge unit is the line (`integrate_line()` per entry), so no per-slice merge event exists; T007's own wording ("so the doc surface says so") concedes that the assertion is a documentation check, against GW-08. |
| CHK027 | FAIL P2 | confirm | M | F-20 | Verified against `integrate-lines.py:79-119`: the second half of GATE-5 (`closure-blocked` recorded, line `blocked`) requires a registered line + worktree + rebase, which a fixture path cannot supply. |
| CHK028 | FAIL **P0** | confirm | **C** | F-02 | Verified verbatim on both sides. (A) owner doc 12-19 = feature-details / verification-log / tasks-template / plan-template and says they "are also the exemption list"; (B) requirements:211 = data-model+contracts / requirements FR-003 / plan-template. Intersection = 1. (A)'s own claim that "each carries its own narrowing assertion" is false for (A)'s members — (a)…(d) all take (B)'s. T014 cannot write `expected`. |
| CHK029 | FAIL P1 | confirm | H | F-03 | Verified analytically and by measurement: the scan domain is `templates/` + `shared/`; three of four exempted members live under `.specify/specs/…`; the one in-domain member (plan-template) must carry 0 domain literals and does (measured 0). The list exempts nothing the scan can reach while the two in-domain files that *do* carry literals are not on it. |
| CHK030 | FAIL P1 | confirm (refined) | H | F-04 | Confirmed by real greps, with a correction: the hit count is 11 files under a narrow set and 29 under a broader one (the checklist's 8 is a third set) — which is itself the proof that the derivation is not mechanical. Named unrelated vocabularies verified: `not-required` = traceability binary (sdd-routing-definitions:78), `not-applicable` = code-review segment verdict (review-template:81/103/129, commands/review:110/117/131/151), `in-scope` = English (derivation-definitions:189). |
| CHK031 | FAIL P2 | confirm | L | F-27 | Verified: three reason clauses for four paths; `expected` is either 4 path tuples or 3 (path-set, reason) pairs. Real but subordinate to F-02 — once the list is settled the arithmetic follows. |
| CHK033 | FAIL P2 | confirm (refined) | M | F-21 | The verdicts do differ (FR-019 admits classified existence; SC-009 ④ admits only absence-or-exemption). Correction to the premise: the two **literal sets** are not identical (FR-019 = `blocked`/`not-required`; SC-009 ④ = the owner's whole domain set), so they overlap only partially. What is missing stands: nothing links T002's ledger to T014's `expected`. |
| CHK037 | FAIL P1 | confirm (widened) | H | F-09 | Verified, and worse than reported: besides T015 / T014 / T005, T016's own text consumes **T004** ("the review site by the T004 extraction") and **T007** ("the implement site by running test_gate_wiring_081.py's implement legs"), neither of which is in its closure. |
| CHK038 | FAIL P1 | confirm | M | F-12 | Verified: T015 `[blockedBy: T002,T009,T010,T013,T014]` omits T006, which edits a file inside the `skills/external/sdd-loop-driver/**` pair T015 regenerates — while T009 is in the list for exactly that reason. Lowered from P1 to M: GATE-3 catches the resulting drift at close, so the harm is a re-run, not a green. |
| CHK040 | FAIL P2 | confirm | M | F-22 | Verified: `plan.md:236-238` cells still read `inherited` while T012 and § No Deferred Slice say "3 of 3 resolved"; `verification.md` SC-005 has already recorded the reading sense. Recurrence of 081c CHK039, still unclosed. |
| CHK042 | FAIL P1 | confirm | H | F-11 | Verified: SC-002 has three readings (2/2 + 1/1); T004 covers only the R4R leg and T017 makes `pass` conditional on it alone. Measured: `review-implemented-clean` → claimed `Implemented`, pass 1/1, four conditions true — structurally unable to exercise `Planned → Implemented`. |
| CHK043 | FAIL P2 | confirm | L | F-28 | Verified: only T001/T002 carry `[P]`; both declared parallel pairs meet the stated criterion and carry none. Hygiene. |

**Adjudication summary**: 19 confirm · 3 confirm-with-refinement · 3 downgrade (CHK009, CHK021, CHK038) · **0 reject**. No checklist FAIL was found to be a misread this round — the difference from 081c's adjudication is that three of them are over-severitied rather than wrong.

## Checklist PASS items — re-derivation honesty

10 of the 18 PASS items were independently re-derived and hold: CHK005 (21 lines, `Blocked` 0 hits, `:20` header), CHK006 (`:121` five values), CHK017/CHK018 (all seven landing line numbers re-measured: 46/47/48, 707, 764, 1447/1949/2139/2249/2266, 806), CHK023 (`stale_from_state` write at `:806` stores the previous value), CHK024 (`:72` constant, `:411` test, 14 tests), CHK025 (`closure-acceptance-check` 0 hits in integrate-lines.py), CHK032 (plan-template domain literals = 0), CHK039 (T004 is row 4 and T012 is row 12, each naming the module its inherited carrier names), CHK041 (T018's two-transition path and its failure branch).

The remaining 8 (CHK002, CHK003, CHK004, CHK008, CHK015, CHK034, CHK035, CHK036) were **accepted on the checklist's evidence** without independent re-derivation. They are readings of probe output I did not re-run; treat them as single-reader. In particular CHK034's six environment readings and CHK003's coverage figures were not re-measured this pass — CHK003's figure is however corroborated by `tasks.md:64` and by the fixture-free reading path, and nothing in this analysis depends on its exact value.

## Findings not raised by the checklist

- **F-10 (H)** — `tests/contract/test_acceptance_state_machine.py::test_the_four_blocked_literals_stay_four` is named as FR-019's sole carrier in both `tasks.md:188` and `contracts/state-vocabulary.contract.md:46` and **does not exist**; no row creates it. The checklist's own probe P42 recorded the zero hit but no item adjudicated it.
- **F-24 (M)** — `.specify/memory/features.md:89` describes the checker's output as "final 三计数" (three counts), the exact shape FR-006/FR-015/SC-006 forbid. A feature-line consistency defect in the durable feature description.
- **F-29 (L)** — SC-009 ② announces "五要件齐备" and names four.
- **F-01 (C)** — the SC-002 sufficiency bar (see above). CHK042 is adjacent but different: CHK042 is "which legs are measured", F-01 is "whether the measured leg counts".

## Notes

- **Every load-bearing claim above was produced by a program, not by reading**: the state-set and guard line numbers by `grep -n`, the phantom carrier by `grep -rn … tests/`, the fixture corpus by `ls`/`find`, the plan-template and domain-literal hit sets by `grep -rlE`, and the two SC-002-relevant verdicts by running `closure-acceptance-check.py --json` on `review-implemented-clean` and on `--audit-existing` (both read-only; the tree is clean afterwards).
- **The three D6 items are one decision, not three.** F-02 (two authorities) / F-03 (exemptions outside the domain) / F-04 (the derivation cannot exclude unrelated sets) cannot be fixed separately: fixing the list without fixing the derivation reverses F-03's reading, and fixing the derivation without the list leaves `expected` undefined. Decide in this order: (1) what the scan's subject is (which paths, which literals), (2) what the allowed set is under that subject, (3) which narrowing assertions describe surfaces the scan cannot reach. Then AS-14, SC-009 ④, § Declared carriers and T014 all follow from one sentence.
- **The two scheduling rows are the same recurrence as 081c CHK042/CHK043** (F-09, F-12): the true dependency exists only in prose. That has now been found in two consecutive slices, which suggests it belongs in the tasks template as a fixed check, not in per-slice discovery.
- **F-22 is a third-time recurrence** (`resolved` dual meaning: 081c CHK039 → 081d CHK040 → F-22). It survives because the wording is copied forward between slices. A wording fix in FR-011 will not stick unless it is fixed where the copied sentence lives.
- This report is **not** a substitute for `/speckit.checklist`: the checklist asks whether the requirement is written clearly; this stage decides whether the defects must be repaired before implementation. The verdict `fail` is about readiness, not about the checklist's accuracy — this round the checklist was accurate on 25 of 25 FAILs.
