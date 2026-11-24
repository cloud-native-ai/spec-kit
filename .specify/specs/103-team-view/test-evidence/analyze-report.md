# Analyze Report — 103-team-view (Round 1, 2026-11-24)

**Stage**: analyze · **Round**: 1 (no prior analyze report for this spec — no rerun delta)
**Spec**: `.specify/specs/103-team-view/` · **Bound feature**: 027 Team Management (high confidence)
**Read domain**: the 12 spec files named in the state spine + `.specify/constitution.md` + `.specify/features.md` + `.specify/features/027-team-management.md` (single-unit domain; `requested=24 / effective=1 / effective_reason=single-unit`)
**Same-author gate**: **not fired** — every artifact predates this session and was produced by prior stage executors (independent authors); detection was therefore not delegated, and this stage's brief forbids subagent dispatch.
**Verdict**: **pass with suggestions** — 0 CRITICAL / 0 HIGH / 4 MEDIUM / 2 LOW. No CRITICAL/HIGH means no validation wave was required (§5.5); the zero-C/H coverage floor was executed instead (see Coverage Summary).

## Findings

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| E-01 | Coverage gap (E; scopes b/c) | none | MEDIUM | `coverage-baseline.txt` (absent); `.specify/features.md:36`; `tasks.md:96` (T002 still `[ ]`) | The clause/FR coverage delta cannot be judged: the read-only accountant exits 2 with `status: baseline-missing` (no baseline file exists and none ever existed in git history), while the Feature 027 index row records "coverage baseline frozen". | Freeze the baseline through the tasks-stage owner path (create-tasks runtime-evidence landing point) or record an explicit dated deferral in the tasks evidence; drop/correct the registry note; then re-run analyze for a judged coverage lane. |
| E-02 | Coverage gap (E; scope b) | 实现（FR lane 关闭 / `.specify/features*` 同步） | MEDIUM | `tasks.md:19` (DoD-1); `tasks.md:11-13`; `requirements.md:157` (FR-018); `tasks.md:216` (T040); `tasks.md:220` (T044) | FR-018 is cited on **zero** `- [ ] T<NNN>` task lines, although DoD-1 asserts every FR-001…FR-021 is quoted on one and its named oracle (`pre-analyze-check --stage tasks`, errors=0) counts FRs (`fr=21`) rather than citations, so the check stays green on this defect. The requirement's substance is only partially reached through T040/T044's feature-registry paths, without any owning row. | Cite FR-018 on the rows that sync `.specify/features.md` / `.specify/features/027-team-management.md` (T040/T044) or add a dedicated implement row; make the DoD-1 check citation-sensitive rather than `errors=0`. |
| E-03 | Coverage gap (E; scope b) | `verification.md`（SC-006 证据路径） | MEDIUM | `tasks.md:213` (T037); `tasks.md:124` (T008); `data-model.md:169` (fixture map); `quickstart.md:44-52` | SC-006's only citing row (T037) runs quickstart S-0…S-5, none of which builds the missing-`runs/`+ledger+`Verification` fixture; the row that writes the covering test (T008) does not cite SC-006, even though the fixture map assigns SC-006 to the integration test. The named evidence carrier will not produce the criterion's evidence. | Cite SC-006 on T008 and drop (or re-point) T037's SC-006 citation; keep T037 for SC-001/SC-002. |
| F-01 | Inconsistency (F; scopes a/b) | none | LOW | `plan.md:162` ("18-entry"); `plan.md:43` ("four new test files"); `feature-ref.md:54-56` (19 entries); `data-model.md:161-177` (map names 3 of the 4 test files) | Two retrospective counts in the plan's Phase 1 summary were not refreshed: feature-ref.md now carries 19 delivery-surface entries after the declared tasks-stage minor PLAN-EDIT (N-4), and the FR-021 fixture map names three new test files, not four (the unit-parser file is absent from the map). | Refresh both counts in a minor plan edit, or mark them as dated retrospective readings. |
| F-02 | Inconsistency (F; scope b) | `skills/internal/view-team/SKILL.md` (C-13) + `scripts/python/team-view.py` (C-26 scope handling) | MEDIUM | `templates/commands/team.md:37`; `templates/commands/team.md:73`; owner: `.specify/shared/definitions/anchor-definitions.md:43`; already recorded: `.specify/memory/feedback/20261124T031029Z-speckit-clarify.md:20` | The Scope paragraph and the goal-based-branch paragraph name `goal-definitions.md § Archive Layers` as the owner of the `--scope` value set / archive layers, but that file has no such section; the owner is `anchor-definitions.md § Archive Layers` (which declares itself the `--scope` owner). View inherits the scope semantics through this Scope section (FR-005, C-13), so the dangling pointer sits on the inheritance path. | Correct the pointer while T016/T028 edit the same template (reference-only change; regenerate the four copies), or record a dated deferral. |
| F-03 | Inconsistency (F; scope b) | none | LOW | `quickstart.md:49` (S-1), `:90` (S-5 program test), `:96` (S-6); `tasks.md:122` (T006), `tasks.md:124` (T008); `tasks.md:36` (GATE-5) | quickstart pins three test names that no task row mandates — `test_single_team_renders_six_groups`, `test_undeclared_target_option_rejected`, `test_view_leaves_tree_byte_identical` — while GATE-5 explicitly accepts "实现期最终名"; the pin can silently break if the implementer names tests differently. (The other named tests are mandated by T007/T026/T032.) | Name these tests in T006/T008, or soften the quickstart pins to behavior + file path. |

## Checklist Accountability (pass H)

| File | Items | Checked | Unchecked | Unchecked `[Gap]` | Raised | Dispositioned | Residual |
|------|-------|---------|-----------|-------------------|--------|---------------|----------|
| `checklists/requirements.md` | 17 | 17 | 0 | 0 | 0 | 0 | 0 |
| `checklists/team-view.md` | 40 | 0 | 40 | 0 | 0 | 0 | 0 |
| **Total** | **57** | **17** | **40** | **0** | **0** | **0** | **0** |

**Gate equation**: `unchecked[Gap] + unraised + undispositioned = 0 + 0 + 0 = 0` — the analyze gate is not blocked by pass H (zero `[Gap]`-tagged items exist in either checklist; the 40 unchecked non-`[Gap]` items are advisory requirements-quality questions outside the H required set).
Observation only: the checklist author left three `[Ambiguity]` items open (CHK031 report ordering key, CHK032 excerpt depth, CHK033 display-cap value); all three are resolved downstream by C-32, C-33 and C-31, so they are recorded here rather than raised as findings.

## Coverage Summary

**Clause/FR accountant (read-only, no `--freeze`; command run with its supported positional/`--spec-dir` form — see Method Notes)**: exit 2, verbatim lane verdicts:

```text
[clause-uncovered] fail (785) — 785 uncovered, 785 beyond the frozen baseline
[fr-uncovered] fail (12) — 9 of 21 FRs cited from citation groups
[clause-unparsable] fail (108) — 108 files yield no clause id under the owner's forms
[coverage-baseline-delta] fail (785) — baseline holds 0 names; 0 uncovered items are baseline-internal and do not block
status: baseline-missing
```

- `status: baseline-missing` is a **phase-visible problem**, not silently skipped: the run cannot judge this feature's coverage delta because `<spec-dir>/coverage-baseline.txt` does not exist (finding E-01). Remedy: freeze it through the tasks-stage owner path (or record the deferral explicitly), then re-run analyze.
- The corpus-wide lane numbers cannot be read as this feature's gaps: with no baseline, every uncovered name counts as "beyond baseline". The `claimed clauses 0` reading matches the declared tasks-stage decision N-1 (no `[green:]` tags), so the clause-claim lane is intentionally empty.
- Independent of that lane, the FR→task-row coverage was computed mechanically from `tasks.md` (citation-sensitive): **20/21 FRs cited**; bands: ≥3 rows = 12 FRs, exactly 2 rows = 8 FRs, exactly 1 row = 0, zero rows = 1 (**FR-018**, finding E-02). SC map: **7/7 criteria cited**; exactly-one-row criteria = SC-006 (T037) — re-read in full, producing E-03.

**Zero-C/H floor (executed)**: detection passes A/B/C/D/E/F/G/H/I all ran. Coverage-mapping sample re-read: all 44 task rows read in full; the distinct-row map above was machine-derived; the single single-row criterion (SC-006) was re-read against T037, T008 and the fixture map → E-03; the remaining spot re-reads (T008, T013, T037, T040, T042, T044 against their cited FR/SC ids) confirmed the cited obligations match the rows' written actions. Outcome: 20/21 FR citation coverage, 7/7 SC citation coverage, 1 mis-wired SC, 1 uncited FR.

## Feature Linkage Summary

| Check | Reading | Evidence |
|-------|---------|----------|
| Candidate feature | 027 Team Management — confidence **high** | `requirements.md:16-18` (Related Feature + binding basis); `## Clarifications` 2026-11-24 |
| Index row | 027 present; `Implemented`; spec path points at `.specify/specs/103-team-view/requirements.md`; Last Updated 2026-11-24 | `.specify/features.md:36` |
| Detail file | exists; latest-review notes for clarify/plan/tasks; status-tracking line names this spec; status `Implemented` | `.specify/features/027-team-management.md:16-20,98` |
| Status duty | **lawful hold** — no-status-regression keeps `Implemented`; no stage transition owned by analyze | `feature-integration.md` § Core Protocol / § Status State Machine |
| Stage-record duty | date is current (2026-11-24); the checklist stage initiates no transition pre-implement; the row's note however carries one inaccurate claim ("coverage baseline frozen") | `.specify/features.md:36` → finding E-01 |
| Requirement↔feature intent | additive fourth mode on the same command surface and archive layer — matches 027's description; terminology (`/speckit.team`, team archive, mode names) matches | `feature-ref.md:9-17` |

## Constitution Alignment Issues

**None.** `.specify/constitution.md` (v1.20.0) carries 23 principles; the plan's Constitution Check table lists the same 23 headings in order with no `Fail`/`Partial` row, and the chain's own MUST obligations were spot-checked against the live owners:

- Read-only discipline: this stage wrote no artifact; the chain's view design is a closed read-only claim with a baseline + empty allowed delta (FR-004 / SC-002 / INV-01).
- One Source of Truth: every cited owner path in requirements/plan/data-model/contracts resolves (verified: `create-mode.md` § Schema notes, `summary-mapping.md` § 6 / § 6.1 / § 10.1, `anchor-definitions.md` § The Binding Record / § Archive Layers, `create-team/SKILL.md` § Report contract, `acceptance-hardening.md` § Feature Status / § Gates / § Execution Premises). The one broken pointer is pre-existing in `templates/commands/team.md` and is reported as F-02 (an F-class inconsistency — the spec chain itself cites the true owner).
- Test-first / test-execution / script-interface: Tests Mode ON with red-first rows; the new program's `-h`/`--version`/undeclared-option obligations are pinned by C-27; no reduced selection or retry-until-green is designed.
- No new machinery: C-19 / C-37 forbid a second store, cache or user-facing machine format; `--json` is declared internal (A-5).

## Unmapped Tasks

**0** — every one of the 44 task rows cites at least one FR/SC id (or an explicit gate id whose FR/SC anchor is on the same row). The inverse direction is not clean: FR-018 has no owning row (E-02).

## Decision Tension Channel

`python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/103-team-view --json` → `status: ok`, `records: 0`, `errors: 0`, all six labels `pass` (`dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form`, `expected-sacrifice-unmapped`). The `## Decision Tensions` section is the direct successor of `## Constitution Check` and precedes `## Project Structure`; its `N/A` carries a per-trigger justification for all four trigger classes.

## Systemic Observations

1. **Machine-adjacent record claims** (cluster: E-01, E-02): two green-check claims rest on oracles that do not measure the claimed property — the registry's "coverage baseline frozen" (no such file; T002 still open) and DoD-1's "every FR is cited" (the named check counts FRs, not citations). Individual severities stay as reported; the pattern is that hand-written completion notes sit beside machine-shaped records without a machine reading behind them.
2. **Honest carrier vs drifted note** (E-01): the tasks-stage evidence file itself does not claim the freeze — only the feature-index note does. The drift is in the registry projection, not in the evidence base; repairing the note (or freezing the baseline) closes it.
3. **Measurement base is unusually solid**: all re-measured premises reproduced exactly in this run — 20 teams / 20 `team.md`, 12 run directories, 46 `runs/*.md` vs 41 `*-report.md`, 5 ledgers (1 zero-line), 3 continuous spines, 0 legacy `goal_slug` / 10 missing `anchor_slug`, 9 `## Verification` / 0 `## Nested SDD Runs`, 6 files carrying the stale literal, `goal-utils.py 0.0.22` with the three read actions reproducing S-0's captured output, `sync-mirrors --check` / `regen-command-copies --check` / `compile-embeds --check` all rc 0.

## Metrics

| Metric | Value |
|--------|-------|
| Requirements | 21 FR / 7 SC / 5 RS / 4 STR / 19 A-decisions |
| Tasks | 44 (T001…T044, contiguous; 6 `[P]` rows) |
| FR citation coverage | 20/21 = 95.2 % (FR-018 uncited) |
| SC citation coverage | 7/7 = 100 % (SC-006 mis-wired) |
| Clause extraction | 38/38 (`C-01…C-38`; 12 + 11 + 15) |
| Feature linkage | 027, high confidence |
| Ambiguity / Duplication findings | 0 / 0 |
| Inconsistency findings | 3 (F-01…F-03) |
| Coverage findings | 3 (E-01…E-03) |
| Severity split | CRITICAL 0 · HIGH 0 · MEDIUM 4 · LOW 2 |
| Validation wave | not dispatched — zero CRITICAL/HIGH; downgrade rate n/a |
| Same-author gate | not fired (independent authorship) |
| Tests | not run — docs-only (E3 row `status=not-run-docs-only`) |

## Method Notes & Disclosed Corrections

- **Correction in passing (disclosed)**: the analyze skill's §3 shows `account-clause-coverage.py --spec <dir>`; the program rejects `--spec` (rc 2). Ran the supported form (`<spec-dir>` positional / `--spec-dir`). The drift is in the skill text, not in this feature's artifacts; recorded in the wrap-up feedback points.
- **Read-only proof**: `git status --porcelain` was captured before analysis and diffed after the wrap-up. The only additions are this stage's three evidence files (this report, `analyze.jsonl`, `analyze-findings.jsonl`) plus the sanctioned wrap-up records (one run-determination session record, one exec-quant record, one feedback record). One pre-existing session record was modified by the run-determination engine's declared settlement side effect (a machine record, not an artifact). No spec/plan/tasks/checklist/contract file and no framework source was touched.
- **Plan constraint**: `plan_constraint=active` — zero plan-owned touches by this stage; every plan-owned finding (F-01) is reported, not edited.
- **Remediation is not applied**: the recommendations above are offers; any follow-up edit belongs to `/speckit.tasks`, `/speckit.plan` or the driver's routing.

## Next Actions

1. **E-01** — freeze `coverage-baseline.txt` (tasks-stage owner path) or record the deferral; correct the 027 registry note; re-run analyze for a judged coverage lane.
2. **E-02** — cite FR-018 on T040/T044 (or add a dedicated registry-sync row); make DoD-1's check citation-sensitive.
3. **E-03** — cite SC-006 on T008 and drop/re-point T037's SC-006 citation.
4. **F-02** — correct the `goal-definitions.md § Archive Layers` pointer in `templates/commands/team.md` during T016/T028 (reference-only; regenerate copies), or defer with a dated record.
5. **F-01 / F-03** (LOW) — refresh the plan's two retrospective counts and/or name the three quickstart-pinned tests in T006/T008.

**Gate reading**: no CRITICAL/HIGH remains open, so `/speckit.implement` is not blocked by this report; the four MEDIUM items are routing decisions for the driver (tasks-stage repair vs implement-stage absorption). Would you like concrete remediation edits for the top N issues? (Not applied automatically.)
