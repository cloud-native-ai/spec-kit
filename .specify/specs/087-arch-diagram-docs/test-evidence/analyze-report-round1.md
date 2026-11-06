# Analyze Report — Round 1 (087-arch-diagram-docs)

- Object: `.specify/specs/087-arch-diagram-docs/` @ `47a59449`
- Mode: read-only cross-artifact analysis
- Verdict: **fail — 0 CRITICAL / 2 HIGH / 7 MEDIUM / 7 LOW**; no artifact was modified.

## HIGH (blocking)

### F-01 — Contract clause → test/`green` binding is misaligned (plan → tasks → implement)

- `plan.md:406,438-459` § Test Plan table B has 23 rows while `contracts/flow-obligations.contract.md` has 24 clause IDs (C-008 missing); several rows (C-003 onward) carry a subject different from the same-numbered clause.
- `tasks.md` `green` labels inherit the same shift (e.g. T037 claims `flow#C-001` but implements C-007; T054 claims C-016 but implements Authoring R5; T043 claims C-008 but implements C-008a R5).
- `tasks.md:71` "each clause is claimed exactly once" is false: 40 clause IDs are claimed 33 times; 7 are unclaimed (diagram C-014; flow C-007, C-008a, C-009, C-021, C-022, C-023).
- Fix: rebuild table B to cover C-001…C-023 **and** C-008a by actual clause subject; add named assertions for the missing/mismatched clauses; re-bind the tasks `green` labels; re-check "exactly once"; do the same 2–3 row repair for table A (diagram C-001…C-016).

### F-02 — "docs/ zero change" contradicts the delivery of `docs/concepts/documentation-model.md`

- `plan.md:46` says `git diff --name-only <BASE> -- docs/` is empty; `tasks.md:39` GATE-6 and `tasks.md:231` T073/S8 repeat it; `quickstart.md:295-307` expects the same.
- Opposite: `requirements.md:153` FR-001 requires `docs/concepts/documentation-model.md` to be brought into agreement in the same change; `plan.md:244` lists it as a delivery surface; `tasks.md:213` T064 adds the reader projection; `tasks.md:25` DoD-7 requires it.
- Fix: narrow the zero-change constraint to "except `docs/concepts/documentation-model.md`" and update GATE-6 / T073-S8 / quickstart S8 / plan wording consistently.

## MEDIUM (recorded; fix opportunistically in the same repair round)

- E-01: FR-012 (refusal surfacing) and FR-021 (no silent content-destroying reclassification) have zero task rows; flow C-004 has no assertion. Add task rows + assertion.
- E-02: `coverage-baseline.txt` missing; `account-clause-coverage.py` exit 2 (`baseline-missing`); T004 defers it. Freeze the baseline or record an explicit deferral.
- F-03: `diagram-obligation.contract.md:89-91` C-004's five-value order conflicts with C-016's nine-row order; delete the C-004 precedence sentence, keep C-016 as the single owner.
- C-01: `data-model.md:87-91,97-99` fixture invariant "repo copy is always the pre-deletion green state" conflicts with E6's `deleted-rendered/` / `orphan-*` "deleted" states; choose one reading and align fixtures/quickstart.
- F-04: `tasks.md:234` T076 writes `tasks-stage-status.jsonl` (already owned by the tasks stage); rename to `implement-stage-status.jsonl`.
- F-05: `feature-ref.md:30` cites non-existent mirror paths `.specify/skills/external/...` and `.specify/templates/commands`; use the real `.specify/skills/<name>` + four per-tool copies.
- G-01: `register.md:101` OI-087-01 still `open` although `checklists/requirements.md` N6 records it resolved; close it with the N6 evidence and update the plan's stale residual prose.

## LOW (record; no blocking)

- G-02: Feature detail `Last Updated` / `Latest Review` still at plan attempt 2; add the checklist-stage record (owner `/speckit.checklist`).
- F-06: `plan.md:33` "6 处文本落点" vs `data-model.md:125` "5 处落点、4 个文件"; keep one count.
- C-02: `tasks.md:38-39,118,145,231` `<BASE>` placeholder and `--name-only<BASE>` spacing; substitute `24cb4edc` and fix spacing.
- F-07: `plan.md:467` table C merges guards from three files under `test_expression_compatibility.py`; split by file and correct the count.
- F-08: `data-model.md:74` says trace record written by R5/R6; C-008a says R5 writes, R6 reads; change to "R5 写、R6 读".
- F-09: trace-record filename shape `<UTC>-diagram-trace.json` vs `<UTC>-<8hex>-diagram-trace.json`; pin one in C-010.
- A-01: "49 技能冻结清单" vs "74 条冻结清单" — different denominators; state the relationship.

## Checks that passed

- `converged`/`clean` dual predicate and `judged_scope_has_carrier` are consistent across C-013, plan (20/428/444), data-model E3, quickstart S9, feature-ref SC-003, tasks T025/T036; `U::test_c013_empty_scope_not_converged` present.
- C-008a R3/R4/R5/R6 makes SC-001/SC-003 reachable; `not-evaluated` not skipped; `D-001`/`exempt` boundaries correct.
- SC 10/10 have a named measurement + task anchor; runtime in-scope FRs are quoted at task-row level.
- The two P2 fixes (notation alias; S9 formula pointer) are in place.
- OI-087-01 copy deletion is consistent with 1SOT (registry status still needs G-01).
- A7/T-001 allowlist + four guard constraints match the plan/tasks; tasks-stage plan-owned touches are declared (`audit undeclared=false`).
- No new `/speckit.*` command, second engine, second delivery contract, or docs full backfill; the only docs edit is FR-001's explicit requirement.

## Evidence

- E3: `test-evidence/analyze-stage-status.jsonl` (six fields, `not-run-docs-only`)
- Wrap-up: run-determination `simple-unit`; exec-quant `20261106T075307371543Z-8a090e14.json`; feedback `20261106T075313Z-speckit-analyze.md` (feature=087-arch-diagram-docs / feature_id=087)
- No product/spec artifact was modified; HEAD did not advance.
