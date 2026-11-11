# Analyze dispositions — 100-seal-slice-archive — 2026-11-11

Policy: unattended analyze gate — CRITICAL/HIGH are repaired in place and the gate is re-run until 0 open CRITICAL / 0 open HIGH (owner: `shared/guidelines/confirmation-gates.md` § Analyze-gate exception).

## Validation wave

| Finding | Verdict | Proposed severity | Disposition |
|---------|---------|-------------------|-------------|
| D-01 | reject | same | rejected — FR-020/pt. requirements already scope slice archival outside retirement/archive-gate; no edit |
| D-02 | confirm | same | confirmed — fixed: FR ids added to T-001…T-006 decision lines |
| D-03 | confirm | CRITICAL | confirmed — fixed: three tests/unit modules + plan/tasks/DoD/feature-ref wiring |
| F-01 | confirm | same | confirmed — fixed: Edge Cases split + C-102 ⑤/V3 |
| F-02 | confirm | same | confirmed — fixed: FR-006/C-102 ① not-applicable carve-out |
| F-03 | confirm | HIGH | confirmed — fixed: SC-009/T053 scoped to 本特性新增 + baseline named |
| F-04 | downgrade | MEDIUM | downgraded MEDIUM — fixed: FR-018/C-211/T030/data-model E9 pattern predicate + complement |
| F-05 | reject | same | rejected — baseline pinned by implement-feature owner; FR-025 now cites the owner chain (clarification only) |
| F-06 | downgrade | MEDIUM | downgraded MEDIUM — fixed: C-110/V14/S-6/T033 now use pinned_commit tree comparison; index restore added |
| F-07 | confirm | HIGH | confirmed — fixed: C-207 per-field path bases; T016 cites C-207 |
| F-08 | confirm | HIGH | confirmed — fixed: C-116/feature-ref/quickstart/plan source map SC-010 to rollback.py |
| F-09 | confirm | same | confirmed — fixed: T012 arithmetic/delete-row; T026 runtime cases; SC trace T012/T027 and T013/T026 |
| F-10 | confirm | HIGH | confirmed — fixed: FR-005/T016 use C-203 seven fields; T012 asserts seven-field key set + sorts |
| F-11 | confirm | HIGH | confirmed — fixed: FR-028(b) cites C-301 live roster incl. register/features/glossary/instructions |
| F-12 | confirm | HIGH | confirmed — fixed: FR-028(a) covers source→destination move |
| C-01 | downgrade | MEDIUM | downgraded MEDIUM — fixed: FR-006 + C-102 per-condition exit/reason mapping |
| B-01 | confirm | HIGH (same) | confirmed — fixed: comparison base pinned in all consumers |

## Additional MEDIUM/LOW findings fixed in the same pass

- **C-02** corrupted manifest behavior: FR-010 + C-105: unparseable/schema-invalid → exit 2 `archive-manifest-invalid`; never already-archived
- **C-03** unattended decision-record carrier: FR-022: decision recorded in test-evidence/ round record (command/exit/outcome/readings)
- **C-04** RS premises undefined: requirements RS table now uses RS-P1…RS-P4 with a local premise definition line
- **B-02** identity constant predicate: C-311 cites C-302 F3 as the mechanical predicate
- **B-03** batch undefined: C-108: batch = one archive-apply run (all moves/rewrites/manifest/merge fields)
- **B-04** dirty-tree vs already-archived precedence: FR-010 + C-105 + C-102 ④: already-archived is evaluated before the clean-tree precondition; in-flow carriers are exempt
- **B-05** runtime refs in scan-hit arithmetic: FR-016: runtime carriers are outside the scan-hit universe
- **B-06** F1/F2 overlap: C-302: longest-match F1 precedence; F2 only on uncovered spans
- **B-07** dated-preserved plan-time target: C-306/C-307: plan uses the projected archive tree; apply re-verifies the real tree
- **C-05** rejection reason owner: FR-008 cites C-103 as the reason-set owner
- **C-06** SC-004 comparison unit: SC-004: canonical plan JSON sha256 equality
- **C-08** order/preconditions types: C-202 order_basis/source predicate; C-206 typed preconditions + files_match
- **C-09** unnamed test carriers: T043 + plan P7 name test_sdd_compat_containment.py and test_sdd_diffusion.py
- **C-10** plan outcome on archived tree: C-105/data-model/S-4/T044: archive-plan reports already-archived with zero pending/unresolved
- **C-11** T027 C-207 constraints: T027 now states no wall-clock/host/random/absolute-path fields
- **C-12** generated_by.command: C-202: command describes the writing action (archive-apply); plan does not persist a manifest
- **F-19** package/phase dependency edges: tasks note + plan edge-scope note
- **F-20** C-113 vs § Disposal Pathways: C-113 now authorizes the § Disposal Pathways edit; Bridge unchanged
- **F-21** undefined 计数: C-211/data-model E9/T030 name merge/checks/conflicts/id_maps/order/retention
- **F-22** state machine error reasons in outcome slot: data-model §9 uses error (reason: …) lines
- **F-23** scenario labels: plan Phase-1 table matches actual S-1…S-6 headings
- **F-24** blocked-pair fixture inventory: plan fixture inventory adds blocked pair and runtime/concurrent/rollback sets
- **F-25** rollback index restore: C-110/S-6 use --staged --worktree + git rm --cached for the new manifest
- **F-26** S-2 payload keys: S-2 names checks.unresolved_before/after and unclassified
- **F-27** “状态写” undefined: V13 defines it as registry/detail/seal-receipt status writes; .specify/state updates are separately allowed
- **F-28** plan seal.md referent: plan constraints line distinguishes the parent seal.md receipt from templates/commands/seal.md
- **F-29** Overview 143 count: Overview labels the 143 as parent tasks.md path-or-name count and cites the narrower R-08 detector
- **F-30** Shared-String consumers: column renamed Primary consumers (non-exhaustive)
- **F-31** typo 封装修阻断: all occurrences corrected to 封装阻断
- **F-32** pre-manifest concurrent apply: FR-027 + C-105: archive-drift/partial-archive exit 2, no second manifest
- **F-33** concurrency fixture unnamed: T034 names tests/fixtures/seal-archive/concurrent/
- **F-34** command-reference recovery walkthrough: T040 requires an executable recovery walkthrough in docs/reference/commands/seal.md
- **E-01** trace omissions: trace note records T001/T002/T051 as process rows; T003 added to FR-024
- **G-01** checklist stage record: 099 row + detail Last Updated carry the dated checklist note
- **F-15** features.md status vocabulary: Status column now points to acceptance-hardening.md § Feature Status
- **F-16** checklist SC Path composition: header corrected to 4 final + 6 supporting
- **F-17** checklist candidate arithmetic: Detection path clarifies 37−9=28; 28+8=36
- **W5-F-02** requirements-stage checker evidence: restated as Path value in {final,supporting} with 4/6 reading
- **W5-F-03** requirements-stage checklist verdicts: dated analyze annotation added; [x] verdicts retained as the stage record
- **I-01** T-001 discriminating evidence: rewritten as one binary experiment over archive-plan + archive-gate
- **I-02** T-004 pole_b: rewritten as the real sacrifice (two files to open) with a shared measured quantity
- **A-02** edge-case restatement of FR-019: edge case now points to FR-019 and adds seal P0-list equality

## Residue (open, non-blocking)

- **A-01** (MEDIUM, deferred): contract-level determinism duplication (C-109 vs C-208; C-201 vs C-111; C-105 vs C-111). One owner per property remains the desired cleanup; no execution behaviour depends on it. Disposition: deferred to a focused one-source-of-truth cleanup, recorded in the analyze report.
- **Dated-record note** (not a finding): `test-evidence/tasks-stage-checks.txt` says “675 lines (6 header + 669 names)”; measured 675 lines = 2 header + 673 names. The dated record is preserved; the accountant’s measured reading is authoritative.

## Verification after remediation

- `pre-analyze-check --stage plan/tasks`: pass, errors=0, advisories=2 (the intentional `[blockedBy: Txxx,Tyyy]` format example).
- `validate-requirements.py`: 0 error / 0 warning (231 lines, 38 definition rows, 5 shared strings).
- `validate-tasks.py`: PASS 0 error / 0 warning.
- `decomposition-check --mode plan/tasks`: proceed (28 FR / 53 tasks; ceilings 120/160).
- `validate-decision-tensions.py`: 6 records, 0 error, `high=0`.
- `account-clause-coverage.py`: claimed 40, FR 28/28, 0 beyond baseline.
- Evidence: `test-evidence/analyze-gates-round2.txt`, `test-evidence/analyze-coverage-round2.json`.

## Round-2 rerun (post-remediation)

Round-2 wave: 5 fresh workers (R1 requirements, R2 contracts [failed on output limit; retried as R2a archive-actions + R2b archive-manifest], R3 ref-classification+tasks, R4 plan/data-model/quickstart, R5 feature-ref/checklists/registry/constitution). Every worker READ-DOMAIN-CHECK matched its declaration.

### Round-2 new C/H findings — detected and repaired in the same pass
| ID | Severity | Defect | Fix |
|----|----------|--------|-----|
| R1/N-01 | HIGH | RS-002 "全绿且零新增红" conflicts with FR-025 pinned-baseline set difference | RS-002 joint acceptance now uses the set-difference criterion; pre-existing red is not repaired/masked |
| R1/F-01 reopened | HIGH | FR-006 ⑤ per-slice "exactly one side" admits cross-slice mixing | ⑤ requires all slices on the same side; cross-slice / destination-without-manifest → exit 2 (FR-006, C-102) |
| R1/F-04 | HIGH | FR-018 complement includes the recomputed `digest` | complement exempts `digest`; C-211/T030 aligned |
| R1/N-04 | HIGH | SC-005 "no push" has no oracle under a write-path audit | T034 audits the external-command allowlist and adds a `git push` mutation |
| R3/B-02 | HIGH | C-311 identity constants vs F3 unsatisfiable | C-302 F3 requires a path-construction expression; identity comparisons excluded; F1 beats F3 |
| R3/RC-N01 | HIGH | F1/F2 token boundaries and cross-line forms undecidable | explicit boundaries + slug-roster binding + carrier-level unclassified rule (C-302) |
| R3/RC-N02 | HIGH | whole-batch "all rename pairs" false | rename assertion scoped to moved-slice path set; declared A/M set separately; global zero D |
| R3/RC-N03 | HIGH | one reference-matrix fixture both clean and blocking | split into reference-matrix and reference-matrix-unclassified |
| R3/F-11-F-12 | HIGH | no row asserts parent `seal.md` non-rewrite | `seal.md`-bearing fixture + byte-identity assertion; DoD-8/T037/FR-028 trace |
| R4/N-02 | HIGH | four decision-tension records let the chosen design satisfy both poles | all six pole_b constraints rewritten to the value actually sacrificed; expected sacrifices aligned |
| R4/N-03 | HIGH | round/rollback test files and rollback fixture had no file-level write-domain owner | plan P4/P7/P8 ownership updated |
| R5/N-01 | HIGH | checklist annotation claimed repairs without an analyze receipt | annotation cites the analyze report + dispositions; registry row/detail carry the dated analyze note |

### R2 retry (two smaller workers) — new C/H
| ID | Severity | Defect | Fix |
|----|----------|--------|-----|
| R2a/N-01 | HIGH | exit-code selection undecidable across condition classes | C-102 evaluation order + tie-break + not-evaluated reporting |
| R2a/N-02 | HIGH | rollback deleted the manifest before using it; untracked manifest invisible to diff | load rollback plan first; manifest removal last; `git status --porcelain` criterion |
| R2a/N-03 | HIGH | dirty check missed live carriers; whole-file restore could clobber out-of-flow edits | C-102 ④ covers C-301 live roster; restore scoped to in-flow carriers |
| R2b/R2-01 | HIGH | `from` mapping lacked segment boundary/longest/uniqueness | C-210 boundary + longest-from + uniqueness (ambiguity exit 2) |
| R2a/N-04/N-05, R2b/R2-02…R2-06 | MEDIUM | digest exemption, manifest-absent fallback, C-206 exit, C-209 referent, per-level rejection, order/counter types, C-211 granularity | all fixed in the two contracts |
Note: R2b marked C-02/C-10/F-06 OPEN because those clauses live in `archive-actions.contract.md` (C-105/C-110), outside R2b's declared domain; the fixes there were verified by R2a.

### Round-2 medium/low fixes
- R1/N-02 `relative_path` → `path`; N-05 SC-001 reading window; N-06 SC-002 zero-new-diff; N-07 runtime zero-hit binary; N-08 archived-spec identity; N-09 command-baseline phrasing.
- R3/RC-N04 package counts/write targets; RC-N05 T003 `[P]` vs blockedBy; RC-N06 scan-root overlap; RC-N07 merge-manifest hit domain; RC-N08 DoD-8 registration-status wording; RC-N09 F1 slug roster; C-11 T027 path basis; F-08/F-09 trace header and SC citations; F-19 T045 exception.
- R4/N-01 removal of the six `tension_id` body lines (heading is the sole identifier); N-04 S-6 full pathspec; F-22 missing `destination-exists`/`slice-missing` state rows; N-06/N-07 low notes.
- R5/N-02 checklist status owner pointer; N-03 arithmetic wording; N-04 feature-ref owner-page count.

### Round-3 verification (targeted sample)
- V1-requirements: all round-1/R1 findings RESOLVED; one new HIGH (FR-006 inline exit-2 reason list incomplete vs C-103 owner) — fixed by replacing the enumeration with a C-102/C-103 pointer.
- V2-actions: all R2a findings RESOLVED; no new findings.
- V2b-refclass: all R3 ref-class findings RESOLVED; one new HIGH (carrier-level catch-all over-reach, breaking post-apply idempotence) — fixed by narrowing to source-path occurrences and exempting archived paths/identity bare-slugs.
- V3-plan-tasks: all prior findings RESOLVED; four new HIGHs (S-6 criterion used `to` paths after inverse move; `seal.md` ban unqualified vs template/docs edits; plan package anchors vs green ownership; plan write targets without task rows) — all fixed.
- Round-3 new C/H total: 6, all repaired. Final: 0 open CRITICAL / 0 open HIGH.

### Round-2 residue (open, non-blocking)
- A-01 (MEDIUM, deferred): contract determinism duplication (C-109 vs C-208; C-201 vs C-111; C-105 vs C-111).
- R1/N-03 (MEDIUM, deferred): requirements-level field/reason enumerations coexist with the contract owners; copies are aligned and machine-checked; collapse in a future one-source cleanup.
- Dated-record note: tasks-stage baseline line/header transcription; record preserved, measured reading authoritative.

### Round-2 final gate readings
- pre-analyze plan/tasks: pass (errors=0, advisories=2 intentional placeholders).
- validate-requirements: 0/0; validate-tasks: 0/0.
- decomposition plan/tasks: proceed (28 FR / 53 tasks).
- validate-decision-tensions: 6 records / 0 error / high=0.
- account-clause-coverage: claimed 40, FR 28/28, 0 beyond baseline; corpus unparsable lane unchanged (108 / 1 parse doubt).

**Final**: 0 open CRITICAL / 0 open HIGH.
