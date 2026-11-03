# Analyze R2 — slice 081d repair verification

**Stage**: `/speckit.analyze` round 2 (read-only verification of the repair, not a fresh analysis).
**Subject**: commit `8b1e6cc8 fix(081d): repair the analyze C/H findings` on branch `081-acceptance-hardening`.
**Inputs read**: the full repair diff (14 files), and every repaired artifact in its post-repair state — `requirements.md` (FR-020, SC-002, SC-009 ④ and both Source rows), `plan.md` (§ § Mirror Obligations, § D1, § D3), `tasks.md` (DoD-5, DoD-7, DoD-9, GATE-6, T002, T003, T004, T005, T008, T011, T013, T014, T016, T017, § Phase Dependencies, § Parallel Opportunities, § Task Traceability, § No Deferred Slice, § Notes, § Status consequence), `data-model.md` (census, V-31/V-32, § Fixture set), `quickstart.md` (§ S6 premises, § S7), `contracts/{artifact-schemas, closure-acceptance-check, gate-wiring}.contract.md`, `verification.md` (SC-002 ladder), `shared/workflow/acceptance-hardening.md` (§ Declared carriers, new § Schema Uniqueness, § Closure Verdict), plus the live surfaces the repair asserts against (`closure-acceptance-check.py`, `line-registry.py`, `integrate-lines.py`, `.specify/memory/features.md`, `templates/plan-template.md`, `templates/requirements-template.md`, `tests/integration/test_acceptance_smoke.py`, the 15 fixtures, the archived `tasks-081b.md` / `tasks-081c.md` lines the repair cites).
**Findings**: `test-evidence/analyze-081d-r2.jsonl` (35 rows).
**Scope discipline**: no artifact edited. Files written: this report and the JSONL only. No test suite run, no commit, no push.

## Gate verdict

**`fail`** — 0 open C, **1 open H**. All 11 round-1 C/H findings are resolved as stated; the H is **new**, introduced by the repair's own new text (R2-F-12).

| | Count |
|---|---|
| Round-1 C/H re-adjudicated | 11 |
| … resolved | **11 / 11** |
| New C | 0 |
| New H | **1** (R2-F-12) |
| New M | 1 (R2-F-13) |
| New L | 4 (R2-F-14…R2-F-17) |
| Carry-over M/L re-verified | 18 (14 open, 1 partially resolved, 3 resolved by the repair) |

## Round-1 C/H — per-finding verdict

"Rule satisfied" names the constraint the new text now meets; "measured" means a program produced the reading, not a reading of prose.

| R2 | R1 | Sev | Status | The repair, and the rule it satisfies | Measured evidence |
|---|---|---|---|---|---|
| R2-F-01 | F-01 | C | **resolved** | SC-002 now names three readings that must each hold, states that a bare checker invocation *is* the reduced measurement (「把它当 (ii) 即为 reduced measurement 冒充完整测量」), and T004/DoD-9/T017/§ Status consequence/verification ladder all read the same bar. Satisfies: a `final` criterion may not be claimed on evidence its own record calls insufficient. | The three legs are discriminable: `positive` → exit 0 / accept / `Planned`; `smoke-mutation` → exit 1 / [`status-claims-implemented-but-blocked`]; `review-implemented-clean` → exit 0 / accept / `Implemented`, pass 1/1. |
| R2-F-02 | F-02 | C | **resolved** | § Declared carriers now says it "does **not** define the schema-uniqueness guard's allow-list", and a new owner section § Schema Uniqueness is the single authority; AS-13 points at it and forbids re-enumeration. Satisfies: one authority per fact (the round-1 defect was two lists in one sentence). | Grep for `exemption list\|four-member\|豁免清单\|四处` over all live artifacts → 0 guard-list hits. The four archived-slice lines the repair cites (tasks-081b.md:19/:90/:226, tasks-081c.md:273) verified verbatim, and tasks.md:263 discloses them as unmodifiable dated records. |
| R2-F-03 | F-03 | H | **resolved** | The three spec-side paths are no longer *called* exemptions; they are declared outside the scan domain with their own narrowing duties ("够不着的路径不构成边界"), and the one allowed surface is now in-domain. Satisfies: an exemption no scan can reach must not be presented as that scan's boundary. | Column-set scan over `templates/` + `shared/`: Runtime Stack set **0** hits, Execution Premises set **1** (plan-template.md:176), Inherited Blockers set **1** (plan-template.md:184). |
| R2-F-04 | F-04 | H | **resolved** | The subject changed from *derived literals* to the owner's `Column` cell **set**, matched as a whole header row. A column set has no third-party user, so no exclusion list is needed — the second-definition-point risk is removed by construction. | Single names collide (header-cell scan: `Status` in 6 files, `ID` in 4, `Owner` in 3, `Form`/`Evidence`/`Capability`/`Premise`/`Disposition`/`Carrier`/`Source row` in 2 each); column sets do not (0/1/1). The three foreign owners verified verbatim (sdd-routing-definitions.md:78, review-template.md:81, derivation-definitions.md:189). |
| R2-F-05 | F-05 | H | **resolved** | C-02 amended at clause level: `--spec-dir` "required outside audit mode only"; audit root is `--repo`; `--spec-dir` **rejected** in audit mode; mode check and spec-dir requirement are two branches with two messages. FR-020 / C-04 / C-11 / GATE-6 / T013 / quickstart § S7 all carry it; the docstring route is withdrawn (§ No Deferred Slice). | The ordering claim reproduces in code: `run()` raises the mode message at :1294 before `resolve_inputs()` reaches the `--spec-dir` guard at :343. |
| R2-F-06 | F-06 | H | **resolved** | GW-03 states the derivation end to end (branch → leading `\d{3}` → registry row `ID` → `Spec Path` cell → joined to `worktree_path`, because `cwd=wt`), with four named input-error shapes and an explicit "never a silent skip, never an invented path". V-32 restates it; T008 quotes it. | The data source exists: `features.md` row 8 = `\| ID \| Name \| Description \| Status \| Feature Details \| Spec Path \| Last Updated \|`; row 081 → `.specify/specs/081-acceptance-hardening/requirements.md`. Registry entries still carry no `spec_dir` field, so the derivation is the only mechanism — now defined. |
| R2-F-07 | F-07 | H | **resolved** | GW-03 makes record-before-transition a constraint with its reason; T008 and DoD-5 repeat it; **T005 gains the missing leg** — record on a `completed` line, assert `state=completed` + `integration_result.result=failed`, then transition, and assert the reverse order fails. Satisfies: a required ordering must have a red-able carrier, not just narrative order. | Mechanism verified in `line-registry.py`: `--reason` at :2454, `state == "completed"` requirement at :1682, `mutate` writes `integration_result` only and never `state`. |
| R2-F-08 | F-08 | H | **resolved** | § Fixture set now declares two shapes (spec-dir case / audit-root case) with a per-case `Shape` cell, and the audit-root case is self-contained with directories *inside* the case. The `audit-history` row, T011 and quickstart § S6/§ S7 all name it. Satisfies: a fixture's shape must be owned where the corpus shape lives. | "no case references a real feature directory" survives verbatim; "self-contained audit root" now resolves to a definition (data-model.md:188) instead of to zero occurrences. 15 cases on disk, unchanged, none carrying `.specify/`. |
| R2-F-09 | F-09 | H | **resolved** | T016's edge set is `T004,T007,T008,T013,T014,T015`, and § Phase Dependencies justifies each edge against the reading that consumes it. Satisfies: the scheduler's only input is the field, so the field must be complete. | The internally-checked claim is true: `test_acceptance_smoke.py:46` sets `REGEN_REL = 'scripts/python/regen-command-copies.py'` and :146 runs it `--check`, so "over the final tree" before T015 is red by construction. `validate-tasks.py` passes, so the field is well-formed as well as complete. |
| R2-F-10 | F-10 | H | **resolved** | T002 now creates `test_the_four_blocked_literals_stay_four` and says why ("because FR-019's only named carrier was a test id that no row created"); the traceability cell reads "(created by this row)". T002 also lost its `[P]` and T003 gained `blockedBy: T002`, so the two rows that edit one module cannot run concurrently. | Still 0 occurrences under `tests/` (the implementation has not run) — but no longer orphaned: a named row creates it in a module that already exists (14 tests). `contracts/state-vocabulary.contract.md:46` names the same id, unchanged, and is now consistent. |
| R2-F-11 | F-11 | H | **resolved** | The three SC-002 readings are named in the criterion, in its Source row, in DoD-9, in T016 § (a2)(i)(ii)(iii) and in T017 as a conjunction, with the failure branch spelled out (stay `partial`, feature stays `Blocked`). Satisfies: a `final` criterion measured on one of its three readings must say which reading it lacks. | See R2-F-01: all three legs re-measured read-only and each is discriminable. |

**Adjudication note**: no round-1 C/H was rejected or partially accepted. The repair chose the *decidable* repair for all three decision groups round 1 escalated — the D6 group (F-02/F-03/F-04) by changing the guard's **subject** rather than picking a list, the audit group (F-05/F-08) at contract level rather than in a docstring, and the SC-002 group (F-01/F-11) by naming three readings with an honest failure branch. That is the opposite of the failure mode the previous round recorded.

## New findings (introduced by the repair)

### R2-F-12 (H, open) — the derivation's four input-error shapes have no defined consumer, and the default-on gate turns them into a mislabelled failure

This is the one finding that keeps the gate at `fail`. It is not speculation: it is the repair's own new sentence colliding with the only live consumer.

- **What the repair added**: GW-03 (and V-32, and T008) now say a branch with no `\d{3}` prefix, a missing registry row, an empty or `-` `Spec Path`, or a non-existent resolved directory are "**input errors (exit 2) naming the offending subject** — never a silent skip and never a fallback that invents `.specify/specs/<branch>`".
- **What the consumer does**: `integrate-lines.py` has exactly one gate path — `if gate_cmd: gate = run(["bash","-c",gate_cmd], cwd=wt); if gate.returncode != 0: _record_failed(reg, line_id, "quality-gate")`. Exit 2 is indistinguishable from exit 1, and it lands the line failed with `quality-gate` — a driver-vocabulary reason, not the checker's closed set, not `closure-blocked`.
- **Why it cannot be resolved by reading**: "never a silent skip" forbids the only other disposition, so the two readings are *(a)* wedge the line with a mislabelled reason, or *(b)* skip the judgement in violation of GW-03. No artifact chooses — not requirements, not the owner doc, not GW-03, not V-32, not T007, T008, DoD-5 or GATE-5.
- **Why it is not an edge case**: `--gate-cmd` is opt-in today (`add_argument("--gate-cmd")`, default `None`), so T008's default-on gate is what converts the shape into a failure. Measured over the live registry (63 lines): **21** have `branch: null`; **27** have a branch with no `\d{3}` prefix (`main`, `master`, `xuanji/develop`, `line/...`); **7** have a `\d{3}` branch whose feature row's `Spec Path` is empty (003, 005 ×2, 006 ×2, 007, 010). **55 of 63 lines are unresolvable, 8 are resolvable**; among the **18 currently `active`** lines exactly one (081) resolves.
- **Why no gate catches it**: GATE-5 exercises fixture paths; T007's legs assert the command the script builds; nothing asserts anything about a line whose feature has no spec. There is no red-able carrier for the majority path — that is the H criterion.
- **Recommendation**: decide, do not delegate. Either a fifth non-silent outcome (exit 0 + an explicit `not-applicable` record, asserted by T007 — a recorded state, not the skip GW-03 forbids), or keep exit 2 and require `integrate-lines.py` to distinguish 1 from 2 with its own reason and a stated operator next step. Either way add the `tmp_path`-registry leg (one line per shape, asserting resulting `state` and `integration_result`) and disclose the 55/63 exposure in § Environment Prerequisites.

### R2-F-13 (M) — the scan domain acquired a second home

Owner doc § Schema Uniqueness opens "…on what subject, **over which paths** — stated here once"; the new plan paragraph is headed "**Why this section is the home of one guard's scan domain**" and closes "this section fixes only which paths are scanned". Both clauses are ownership claims for one fact. The values agree today, so nothing is unsatisfiable — which is exactly why this is M and not the C that F-02 was. But it is the same defect class the repair had just removed, and no gate compares the two texts.

### R2-F-14, R2-F-15, R2-F-16, R2-F-17 (L) — accuracy and hygiene, all in new text

- **R2-F-14**: the owner doc's justification cites "`templates/plan-template.md`'s Constitution Check table" as an unrelated table carrying a `Status` column. plan-template's Constitution Check section (line 31) has no table; the only `Status` header cell in that file is :176 — the guard's own allowed surface. The argument survives on other files (feature-index-template.md:20, glossary-template.md:23, patterns/interview-pattern.md:190, workflow/interview-walkthrough.md:115), so this is a bad example, not a bad argument.
- **R2-F-15**: the subject is read from code-span-wrapped `Column` cells (`` `ID` ``) and matched against bare skeleton headers (`| ID |`); no carrier says the comparison strips backticks. Raw comparison → 0 hits for all three sets; stripped → 0/1/1. The equality assertion makes the wrong reading fail loudly rather than pass vacuously, so the defect converges once a test is written.
- **R2-F-16**: T004's "carrying" list enumerates the artifact, implementation and code segments plus ARC — three of the four segments the same sentence requires. The process segment has a stable slot (`### 2.1`, kept by RC-17).
- **R2-F-17**: T018 alone still requires "T004's review-site measurement", the phrase T004 was rewritten away from. It names the row, not the form, so it cannot license the withdrawn reading.

## Carry-over (round-1 M/L, re-verified, non-gating)

Fourteen remain open, one is partially resolved, three were resolved by this repair incidentally. Full text in the JSONL; the ones worth naming here:

- **R2-F-28 (`resolved` dual sense, M) is now a third-time recurrence** (081c CHK039 → 081d CHK040 → here). The repair did not touch it; plan.md:236-238 still read `inherited` while T012 writes "3 of 3 resolved". A wording fix in FR-011 will not stick unless it lands where the copied sentence lives.
- **R2-F-20**: T015 still omits T006 from its `blockedBy`, even though T006 edits a file inside the pair T015 regenerates and T009 is in the set for exactly that reason.
- **R2-F-24 / R2-F-25**: the checker still says "not implemented in this slice" in two places with a wrong section reference (`plan.md § Slice Boundary`, 0 hits), and `closure-blocked` is still an unregistered literal (`grep -rl` outside the 081 spec → 0 files) now used in a MUST.
- **R2-F-22 / R2-F-23**: the audited population ("the `Implemented` family") and C-03's missing audit branch both survived; C-04 got closer but neither settles the claim layer.
- **R2-F-29**: `.specify/memory/features.md:89` still describes the checker's output as "final 三计数", the shape FR-015 and SC-006 forbid — a durable-description defect, not a tasks-stage one.
- Resolved by this repair incidentally: **R2-F-35** (F-16 — C-11 now assigns the `git status` half to the tree it observes and adds the content hash, which was round 1's option (c)); **R2-F-36** (F-21 — the guard no longer consumes a literal list, so there is nothing for FR-019's ledger to be confused with); **R2-F-37** (F-27 — the four-member list is gone, so the per-member reason arithmetic is moot).

## Validator readings (all re-run this pass, not copied)

```
=== validate-requirements ===
file: .specify/specs/081-acceptance-hardening/requirements.md
status: ok
  [id-contiguous] pass (0)   [doc-order] pass (0)   [ref-resolvable] pass (0)
  [marker-count] pass (0)    [dup-id] pass (0)      [path-marker] pass (0)
scanned: 272 lines, 34 definition rows, 17 shared strings
0 error(s), 0 warning(s)                                                   EXIT=0

=== validate-tasks ===
PASS: .specify/specs/081-acceptance-hardening/tasks.md — 0 error(s), 0 warning(s)   EXIT=0

=== pre-analyze-check --stage tasks --repo . ===
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=38 waived=0   EXIT=0
  (38 = 1 external-clause advisory on the 081d checklist + 37 missing-path advisories for the
   carriers this slice has not written yet — T005/T011/T014 and the audit fixture. Omitting
   `--repo .` reports advisories=1; the fix-commit transcript's figure of 38 reproduces only
   with `--repo .`, which that file does not record.)

=== decomposition-check --mode tasks ===
{"mode":"tasks","decision":"proceed",
 "measured":{"fr_count":25,"task_count":18,"fr_ceiling":30,"task_ceiling":40},
 "reasons":[]}                                                              EXIT=0
```

Validator status is unchanged from the fix commit's own transcript (`analyze-fix-081d-validators.txt`), i.e. the repair introduced no new error and no new waiver. `advisories=38` is expected-and-disclosed (tasks.md:271) because the carriers land during implementation.

## Measurements this pass produced (so the next reader need not re-derive them)

1. **Column-set uniqueness** (the repaired guard's subject), table-header scan over `templates/` + `shared/`, cells stripped of pipes/whitespace/backticks: Runtime Stack `ID|Capability|Form|Owner|Pin|Contract|Joint acceptance|FR|Premises` → **0** hits; Execution Premises `ID|Premise|Evidence|Status|Decision` → **1** (plan-template.md:176); Inherited Blockers `#|Source row|Disposition|Carrier|Carrier slice|Evidence / note` → **1** (plan-template.md:184).
2. **Single-name collision breadth** (the reason the subject had to change): `Status` 6 files, `ID` 4, `Owner` 3, `Form`/`Evidence`/`Capability`/`Premise`/`Disposition`/`Carrier`/`Source row` 2 each, `Pin`/`Contract`/`Premises` 1 each.
3. **Narrowing assertions (a) and (c)**: `From | To | Allowed | Condition` header rows in `data-model.md`, `requirements.md` and `plan.md` → **0** each. **(d)**: owner-exported domain literals in `templates/plan-template.md` → **0**.
4. **SC-002's three readings**: `positive` exit 0/accept/`Planned`; `smoke-mutation` exit 1/block/[`status-claims-implemented-but-blocked`]/pass 1/1; `review-implemented-clean` exit 0/accept/`Implemented`/pass 1/1; `review-implemented-blocked` exit 1/block/[`zero-final-path-pass`, `status-claims-implemented-but-blocked`].
5. **GW-03 resolvability over the live registry** (63 lines): branch-null 21, no-3-digit 27, empty `Spec Path` 7, resolvable 8; active lines 18, resolvable 1.
6. **`features.md` `Spec Path`**: column exists (row 8), row 081 populated; 23 of 76 rows empty or `-`, which GW-03 now handles as a named input error rather than a silent skip.
7. **Transition-order mechanism**: `--reason` at line-registry.py:2454; `state == "completed"` requirement at :1682; `mutate` writes `integration_result` only.
8. **Repo facts the repair asserts**: `grep -c 'Slice Boundary' plan.md` → 0; `closure-blocked` outside the 081 spec → 0 files; tasks-081b.md:19/:90/:226 and tasks-081c.md:273 carry the retired wording verbatim; plan.md:236-238 still `inherited`.

## Observations (deliberately not raised as findings)

- **SC-009 ④'s literal wording is self-referentially loose in four places**: "the three column sets appear zero times outside this file, **with** exactly one allowed surface" reads as a contradiction if the clause boundary is ignored. It is the same idiom in requirements, owner doc, AS-14 and T014, and the equality-with-{plan-template} clause makes the intent unambiguous — flagging it would be noise at four sites. If it is ever touched, the fix is one word ("zero times outside this file **and** the allowed surface").
- **Assertion (b)** ("every domain literal used by a projection surface belongs to the owner's exported domain") is pre-existing, unchanged by the repair, and read narrowly it would be false for `data-model.md`'s line-state literals, which belong to `line-registry.py`, not to the owner doc. Round 1 did not raise it and this round does not either, because the natural reading is "a domain the projection states may narrow, never widen" and limb (b) is not what the repair touched. Recorded so a future round does not rediscover it as new.
- **`templates/requirements-template.md` carries no Runtime Stack skeleton**, so the one column set that now has zero hits anywhere must be re-invented by every future `execution`-class feature. That is a design consequence of the repaired formulation rather than a defect in it (the guard's assertion is true and measured), and it is out of this slice's declared scope, but it is the one place where the new subject's rigour exposes a gap the old, broken formulation hid.

## Verdict

The repair resolves all 11 round-1 C/H findings, and it resolves the three escalations the way round 1 asked: by making each fact decidable rather than by picking a side. It also introduces one H of its own — the driver's response to the derivation's four input-error shapes — which is not repairable by reading and must be adjudicated before `T008` runs, because T008 is what makes the gate default-on and 55 of 63 registered lines would land on that undefined path.

## R2-F-12 resolution (owner ruling, 2026-11-03)

The driver's exit-2 disposition is decided: **exit 2 is an input error, not a quality failure.** The
driver records `integration-record --result failed --reason closure-input-error` while the line is still
`completed`, leaves the line's state unchanged (not `blocked`), and refuses the merge; only exit 1
(`block`) records `closure-blocked` and marks the line `blocked`. This is stated in
`contracts/gate-wiring.contract.md` GW-03 and `tasks.md` T008, and T008's tests cover both exits. The
r2 gate's open H is therefore closed by the owner decision; no new H remains.
