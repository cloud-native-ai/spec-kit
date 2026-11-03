# Analyze — slice 081c (US3: review composition, artifact/implementation segments, ARC)

**Stage**: `/speckit.analyze`, read-only cross-artifact consistency analysis of the 081c artifact set.
**Inputs read**: `requirements.md` (FR-008, FR-013…FR-016, FR-021, FR-022, SC-002, SC-006), `plan.md` (§ D4, D5, T-002, T-004, D10, § Project Structure, § Execution Premises, § Inherited Blockers), `tasks.md` (T001–T014, DoD, gates, Slice Boundary), `data-model.md` (E-2/E-3/E-4/E-10, V-9, V-12, V-29, Fixture set), all five `contracts/`, `checklists/081c-2026-11-03.md`, and the live implementation surfaces the artifacts assert against (`templates/commands/review.md`, `templates/review-template.md`, `docs/reference/commands/review.md`, `shared/workflow/acceptance-hardening.md`, `skills/internal/code-review/SKILL.md`, `tests/contract/{test_review_code_composition,test_review_docs_isomorphism,test_status_gate_owner,test_client_guard_sweep,test_gate_wiring_081}.py`, `tests/fixtures/acceptance-hardening/*`).
**Findings**: `test-evidence/analyze-081c.jsonl` (24 rows).
**Scope discipline**: no artifact was edited. The only files written by this stage are this report and the JSONL.

## Counts

| Severity | Count | Meaning |
|---|---|---|
| C | 1 | contradiction that makes a requirement unsatisfiable as written |
| H | 8 | defect that would let a wrong implementation pass (green check, unreachable criterion, unnamed conflict) |
| M | 11 | ambiguity / underspecification / duplication with real drift risk |
| L | 4 | wording, carrier and traceability hygiene |
| **Total** | **24** | 21 of them correspond to checklist FAILs, 3 are new |

Lane distribution: `inconsistency` 11, `coverage-gap` 6, `ambiguity` 3, `underspecification` 3, `constitution-conflict` 1.

## Gate verdict

**`fail`** — 1 C and 8 H remain after adjudication. The slice is not ready for `/speckit.implement` until the C and H rows are resolved (or explicitly re-scoped by the owner).

## Checklist adjudication (22 FAIL items, independently re-derived)

Severity scale used here: `C` ≈ unsatisfiable contradiction, `H` ≈ P1 that lets a wrong implementation pass, `M` ≈ P2, `L` ≈ P3.

| CHK | Verdict | Sev | Finding | Reason |
|---|---|---|---|---|
| CHK003 | confirm | **C** | F-01 | Verified on the text: contract:4 names `templates/commands/review.md` § Composition owner of composition/order/boundaries; tasks:92/264 name the owner doc the *only* definition point for six items including segments/order/boundary sentences; T007 (tasks:115) then requires the command to declare the same content, and FR-013 (`requirements.md:153`) requires it too. Two obligations that cannot both hold. § Notes' prohibition covers only the derivation rule, so it does not resolve the other five items. |
| CHK004 | confirm | M | F-13 | Real, but the count is 23 files, not 20 (`grep -rln 'two segments' --include=*.md .`). `.venv/.../specify_cli/templates/commands/review.md` is in the set and no row regenerates it; dated 071/080 records are in it too. The defect is the missing scope definition, not a specific forbidden file. |
| CHK005 | confirm (severity **raised**) | **H** | F-07 | Verified: T004's legs (a)-(i) never name RC-12, the traceability cell points at legs (a)/(b) which judge markers and fields, and C-29 asserts presence only. The plan's own rejected antithesis (T-004) would pass every listed leg, so the carrier decision is not defended by any assertion. Raised from P2 because the unbacked decision is the architecture, not a wording. |
| CHK013 | confirm | **H** | F-06 | Stronger than reported: `data-model.md`'s 13-case corpus contains **no** missing-artifact case for any slice, so the FR-013 false-green clause is never falsified feature-wide, not merely within 081c. |
| CHK014 | confirm | M | F-14 | Verified: plan § Documentation lists ten items and omits `requirements.md`, which is one of the seven. Two readings, neither owned. |
| CHK015 | confirm | **H** | F-05 | Verified verbatim: `requirements.md:153` MUST → `review-composition.contract.md:16` conditional → `plan.md:289` 'optional line' → `data-model.md:175` '`line` (optional)'; no leg asserts the locator. |
| CHK019 | confirm | M | F-15 | Verified: no branch rule anywhere; the same record is a hard condition at the implement gate (V-9) and a quotation-eligible one in the implementation segment. |
| CHK021 | **downgrade** → M | M | F-10 | The contradiction is resolvable inside requirements: `FR-006:140` already says the record is for FR-015's direct reference and MUST NOT be re-counted by a second place. So FR-015's verb 统计 is a wording defect, not an unsatisfiable pair. Confirmed as a defect, lowered from P1. |
| CHK022 | confirm | **H** | F-04 | Verified: FR-015:155 three counts, SC-006:208 3/3, SC-006 Source:220 'three counts', `verification.md:67` 'the three counts' vs RC-14:30's seven keys plus 'MUST NOT narrow it to a three-count summary'. Satisfiable only by a superset — which means SC-006's 3/3 reading passes exactly the form RC-14 forbids. |
| CHK024 | confirm (evidence **corrected**) | **H** | F-03 | The core is right and larger than claimed. I ran the checker on the three relevant fixtures: `negative` → claimed Planned, pass 0; `smoke-mutation` → claimed Implemented, pass 1. So `smoke-mutation` is **not** reachable for RC-15 either — it refuses on `status-claims-implemented-but-blocked`, a different clause. No fixture satisfies 'claimed Implemented/Ready for Review AND pass bucket zero', so F-ACCEPTANCE has no reachable input at all. |
| CHK027 | confirm | **H** | F-02 | Verified by the same run: `positive` claims Planned, so the review site's fourth condition is *inapplicable* rather than passing; the only `Implemented` fixture must be refused. SC-002's `pass` expectation is unreachable; a `positive` re-drive would pass by inapplicability. |
| CHK029 | **downgrade** → M | M | F-11 | The mechanism is verified: `_report_subsection()` uses `(?ms)^### 2\.1.*?(?=^## )`, and `### 2.2` does not satisfy `^## `, so 2.2-2.4 are absorbed. But I read all four legs: the content-list and glossary legs still pass with a broadened subject, and the opinion-body leg reds only if a new slot's text carries one of six code-severity literals. The guaranteed damage is an **undeclared subject change**, not the 'unclaimed red' the checklist asserts. Lowered from P1. |
| CHK030 | confirm | M | F-12 | Verified: `SEGMENTS` (test_review_docs_isomorphism.py:42) has two concepts, the equality test (:193) compares only those, and the page still reads two segments (`docs/reference/commands/review.md:22`). GW-14's docs limb has no assertion that can fail. |
| CHK031 | confirm | **H** | F-09 | Verified and sharpened: the owner doc's § Gates (`shared/workflow/acceptance-hardening.md:111`) itself names `/speckit.checklist` as a consumer that cites `templates/feature-details-template.md` § Canonical Status State Machine. T010 points it at § Gates instead — i.e. the task contradicts a landed owner text and FR-016/SV-05 — while guard C-48 (test_status_gate_owner.py:539-556) stays green under either target. |
| CHK034 | confirm | **H** | F-08 | Verified: `skills/internal/code-review/SKILL.md:111` carries the three-unit census and `tests/contract/test_client_guard_sweep.py:348` pins it verbatim (message 'MUST be preserved verbatim (C-53)'). RC-19 says 'the existing guard' (singular); T009's three modules do not include it; T003 only asks for a segment-position declaration. |
| CHK035 | confirm | L | F-22 | Real but low: the obligation's substance is re-homed in DoD-6 and T009 without saying the carrier was adjudicated. |
| CHK036 | confirm | M | F-16 | Verified: `review-composition.contract.md:48` says 'FR-018 (census)'; FR-018 (`requirements.md:161`) is the `Blocked` vocabulary requirement and the roster gives it to 081d (tasks:241). RC-18/19 have no authorizing FR. |
| CHK039 | confirm | M | F-17 | Verified: ledger cells read `inherited` (plan:235-237) while DoD-7 (tasks:33) and § Deferred Slices (tasks:258) use 'resolved' as a reading; V-29 forbids conflating them. |
| CHK041 | confirm | L | F-23 | Verified: `grep -n 'two segments'` yields 29 and 31; `three units` is at 117/121 and needs its own grep; line 31 (the normative sentence leg (a) targets) is missing from the reading list. |
| CHK042 | confirm | M | F-18 | Verified: T004 and T012 carry no `[blockedBy:]`; § Format (tasks:62) makes the tag the machine-read field. |
| CHK043 | confirm | M | F-19 | Verified: T014 = `[blockedBy: T010,T011,T013]`, closure excludes T003, and T003 edits two framework skill sources whose mirrors T014 regenerates. |
| CHK044 | **reject** | — | — | The checklist's premise fails. The guard `test_c09_every_placeholder_in_the_subsection_is_glossed` reads `_report_subsection()`, which — precisely because of the extractor behaviour CHK029 identifies — runs past `### 2.2`/`### 2.3`/`### 2.4` to the next `## ` heading. Once T006 inserts the slots, the existing guard **does** check their placeholders against `## Placeholder Glossary`, so T006's parenthetical is true and 'a missing glossary entry would not go red' is false. The item is a restatement of CHK029's mechanism read in the opposite direction; CHK029 (F-11) is where the real decision lives — narrowing the extractor would *create* the gap CHK044 complains about. |

Summary: **19 confirm · 2 downgrade · 1 reject**. Of the 22 FAILs, one is a misread (CHK044), two are real but over-severitied (CHK021, CHK029).

## Findings not raised by the checklist

- **F-20** (M) — FR-016/SV-07 promise a user waiver of the fourth condition, while FR-015/RC-15/GW-02 refuse unconditionally when the pass bucket is zero. No artifact says whether a waiver can reach ARC; as written, a granted waiver still gets refused.
- **F-21** (L) — `tasks.md:19` cites GW-14 as the docs-page limb only, while the clause also carries the CHANGELOG entry (081d) and the `.specify/instructions.md` registration (already landed at `:237`). The clause-level citation overstates 081c's coverage.
- **F-24** (L) — RC-15's 'leave the status at `Implemented`' is undefined when the claimed status is already recorded as `Ready for Review`; writing `Implemented` would be the backward move FR-018 permits only in the audit-correction form.

Not raised, deliberately: the composition's *report* slot order (2.1 code segment, 2.2-2.4 after it) contradicts the *execution* order, but RC-17 explicitly declares slot numbers stable slots rather than execution order — the contradiction is disclosed and closed. Likewise the `this-slice` carrier invalidation on archive is disclosed in `plan.md` § Inherited Blockers (081c update) and assigned to 081d, so it is a carried known item rather than a defect of this slice.

## Evidence boundary (honesty notes)

- Machine-verified in this analysis: the three fixture verdicts and `final_path` buckets (read-only `closure-acceptance-check.py --json` runs on `positive`, `negative`, `smoke-mutation`); the `two segments` hit set and count (23); the `_report_subsection`/`_section` regexes and the four affected legs; the C-48, C-53 and C-29 guard bodies; `SEGMENTS` and the equality test; the fixture claimed statuses; every `path:line` cited in the JSONL.
- Not re-run: the full test suite, `validate-requirements.py` / `validate-tasks.py` / `pre-analyze-check.py`, and the mirror/roster engines. The checklist's P1-P26 engine readings were therefore **not** independently reproduced; where a finding depends on one of them (e.g. the 136→138 mirror count), the finding does not rest on the number.
- P1-family review: the five P1 families the dispatch named are all real, but two are mis-scoped in the checklist (F-ACCEPTANCE reachability is worse, not better; the denominator gap is feature-wide, not slice-local), and one P1 is a wording defect rather than an unsatisfiable pair (CHK021).
