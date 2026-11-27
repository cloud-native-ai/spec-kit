# Analyze — Round 1 Report: 112-decision-batch-panel

**Run**: `r20261127T081500Z-112a` · **Stage**: analyze · **Baseline**: `9d1116f42` (checkpoint 05, checklist U4 pass)
**Spec**: `.specify/specs/112-decision-batch-panel/` · **Feature**: 112 Batch Decision Panel（批量决策面板）
**Authority**: `.specify/constitution.md` v1.20.0; `.specify/instructions.md`; `.specify/features.md` row 112 + `.specify/features/112-decision-batch-panel.md`; `.specify/register.md`; owner pages reached by pointer (`shared/definitions/decision-definitions.md`, `shared/guidelines/decision-tension.md`, `shared/guidelines/confirmation-gates.md`, `shared/guidelines/closed-set-claims.md`, `shared/guidelines/one-source-of-truth.md`, `shared/workflow/acceptance-hardening.md`), and the analyze skill + its references.
**Read domain (15 files, analyzed in full)**: `requirements.md`, `checklists/requirements.md`, `checklists/requirements-quality-2026-11-27.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `tasks.md`, and the six `contracts/*.contract.md` files. Precedence-only reads: constitution, instructions, the 107 owner page, decision-tension / confirmation-gates / acceptance-hardening owners, register, feature index and detail, probe and validator sources.
**Method**: read-only round-1 `/speckit.analyze` — full severity set; detection direct. Same-author condition is **not established**: every artifact was authored by a different stage executor of this line, none by this worker. The worker role forbids dispatching agents, so detection and the CRITICAL/HIGH validation fallback were direct evidence re-reads, recorded as such. No product artifact was modified. Worktree clean at baseline; concurrent lines 110/111 share history only (no artifact overlap in this worktree).

## Verdict

**0 CRITICAL · 2 HIGH · 6 MEDIUM · 8 LOW — 16 findings.** The structural chain is coherent: 45/45 FRs reach a task row, 10/10 SCs reach tasks, 54/54 contract clauses carry exactly one `[green:]` claim, every `[[STR-NNN]]` resolves, and the constitution check holds on all 23 principles (no conflict). The headline is nevertheless **not "ready to implement" as-is**: two HIGH cross-clause contradictions sit on the batch-record lifecycle (isolation vs the read-time join; supersession append vs other-batch immutability), both landing on FR-012/FR-037/FR-029 and their contracts and guards. The analyze-side coverage lane also cannot judge the clause delta (`baseline-missing`), one FR (FR-043) has no contract carrier, and the SC-010 path classification drifts across live artifacts.

## Findings

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **I-01** | inconsistency | engine scan/record read-time join + M-15/M-16 guard tests → implement | **HIGH** | `requirements.md:277` (FR-012), `:314` (FR-037), `:244` (edge case); `contracts/source-roster.contract.md:17` (C-107); `contracts/record-replay.contract.md:17` (C-507) | FR-012/C-107 mandate reading prior batch records (already-resolved join); FR-037/C-507 mandate distinct batch ids never read each other's records. Same object, mutually exclusive MUSTs; the concurrency intent appears only in one edge case, and neither FR-037/C-507 nor C-107 carries a qualifier or exception. | Scope the isolation rule to concurrent batches / in-flight state and carve the settled-record read explicitly — e.g. "MUST NOT depend on another batch's in-flight record; the already-resolved read-time join is the only permitted cross-batch read". |
| **I-02** | inconsistency | redecision path in `record` → US5/SC-006 final-path evidence + C-507/C-510 guard tests → implement | **HIGH** | `requirements.md:303` (FR-029), `:309` (FR-032), `:314` (FR-037); `contracts/record-replay.contract.md:20` (C-510), `:17` (C-507), `:12` (C-502), `:13` (C-503); `data-model.md:212` (I-16), `:214` (I-18); `research.md:44` (D-8) | Supersession requires appending `superseded_by` to the prior record; a batch-produced prior record lives inside a prior batch record, while FR-037/C-507 forbid modifying other batches' records and FR-032/C-503 declare the batch record never overwritten. No clause carves the append as the sanctioned mutation, so the normal redecision of a batch decision is simultaneously mandated and forbidden (the skill's own cross-clause contradiction example). | Add the carve-out: "the `superseded_by` append is the sole sanctioned post-write mutation of a batch record — append-only, no other byte changes"; align FR-032/FR-037, C-502/C-503/C-507 and I-18, and pin it in C-510's test. |
| **G-01** | coverage-gap | analyze coverage gate → implement clause-coverage accounting (T004) → review | **MEDIUM** | `coverage-baseline.txt` (absent); `tasks.md:191` (T004); analyze skill § 3 | `account-clause-coverage.py` exits 2 with `status: baseline-missing` (787 errors): the clause-delta lane cannot judge the feature. The freeze exists only as implement-phase T004, while the analyze skill assigns it to `/speckit.tasks` and requires the state to surface with its remedy. | Re-run `/speckit.tasks` (or a tasks remediation) to freeze `coverage-baseline.txt` before the gate closes; never pass `--freeze` from analyze; if T004's implement placement is kept, record an explicit analyze-side waiver. |
| **G-02** | coverage-gap | analyze coverage gate → contract traceability → review | **MEDIUM** | `requirements.md:323` (FR-043); `feature-ref.md:84`; `tasks.md:342` (T053); all six contracts | FR-043 (command reference doc) is cited by no contract clause; the accountant's FR lane fails 44/45 (`UNCOVERED-FR: FR-043`). The carrier exists only in plan § Source Code and task T053. | Name FR-043's contract carrier (extend C-511's coverage or add a distribution/doc clause), or record the plan-only carrier as a declared disposition in the coverage summary. |
| **I-03** | inconsistency | implement verification gate GATE-4 → `verification.md` smoke record → review | **MEDIUM** | `requirements.md:364` (SC-010 Path supporting); `tasks.md:23` (DoD-7), `:32` (GATE-4); `checklists/requirements-quality-2026-11-27.md:81` (CHK038) | SC-010 is declared `supporting` by its owner (requirements) while tasks and the quality checklist treat SC-001…SC-007 + SC-010 as the final-path set; GATE-4 would demand a smoke record for a supporting criterion, and CHK038 contradicts the requirements it cites. | Align all three on the requirements classification (SC-010 supporting), or deliberately flip the Path marker in requirements first; fix DoD-7 / GATE-4 / CHK038 to match. |
| **I-04** | inconsistency | scan bookkeeping partition + the C-108 named-exclusion test (T013) → implement | **MEDIUM** | `requirements.md:272` (FR-007), `:86-91` (roster + 排除族), `:123` (exclusion states); `contracts/source-roster.contract.md:11` (C-101), `:18` (C-108); `data-model.md:153-157` (E-13) | FR-007/C-108 require five exclusion families to be "named and counted", but four cannot be produced by the closed predicates (REC- rows fail the OI-/D- prefix; clarification markers and parked ideas are not PENDING blocks; parked ideas sit outside the four roots; triggered gates are not carrier artifacts) and none has a slot in the closed states or the E-13 partition. The planned test has no defined expected set. | Decide the semantics: (a) roster-rationale-only — reword FR-007/C-108 to "named with reasons at the roster, not counted candidates"; or (b) add zero-count family rows to the bookkeeping; align E-13 and the C-108 fixture. |
| **A-01** | ambiguity | engine scan predicate + SC-001 final-path fixtures → implement | **MEDIUM** | `requirements.md:86-87` (roster), `:73` (A-22); `contracts/source-roster.contract.md:11` (C-101), `:14-15` (C-104/C-105); `data-model.md:33-34` (E-1) | The candidate predicate is not fully deterministic: "去 markdown 强调" does not enumerate the marks stripped; the register authority path is "该行单元格中的显式仓库相对路径" with no column named and no multi-cell/multi-path rule; "tracked Markdown 载体" does not define tracked (git index vs working-tree presence). | Enumerate the de-emphasis mark set; name the authority-path cell and its conflict rule; define "tracked" (recommend: tracked by the git index) in the roster and owner clauses. |
| **U-01** | underspecification | scan payload + reply membership (C-403) + source-conflict fixture → implement | **MEDIUM** | `requirements.md:55` (A-4), `:274` (FR-009), `:235` (edge case), `:290` (FR-019); `contracts/source-roster.contract.md:14` (C-104); `contracts/objection-reply.contract.md:13` (C-403); `data-model.md:71-86` (E-5) | For a `source-conflict` row no artifact states which option set and which default the merged row presents, nor against which set the reply is validated; FR-019 (one closed option set, one default) and C-403 (membership against "the presented option set") have no single subject when two divergent sets are merged. | Declare the source-conflict presentation contract: show each source's set with provenance, no single recommended default, and require the objection label to be a member of a named presented set (or of the reply-named source). |
| **U-02** | underspecification | record path (register status-cell writes) + register guards → implement | **LOW** | `requirements.md:311` (FR-034); `contracts/record-replay.contract.md:15` (C-505); `checklists/requirements-quality-2026-11-27.md:50` (CHK022) | Settled register rows' status cells must "name the batch and decision id" but no value grammar is declared; the scan predicate only tests the leading word `open`, so neither future batches nor guards can compare the updated form beyond its presence. | Declare the settled status-cell shape (e.g. `resolved (<B-id>, <D-NNN>)`) in the owner page and C-505. |
| **U-03** | underspecification | engine `nothing-pending` output + the empty-project / absent-root fixtures | **LOW** | `requirements.md:285` (FR-017), `:286` (FR-018); `contracts/completeness-refusal.contract.md:14-15` (C-604/C-605); `quickstart.md:90-98` | FR-017 requires the completeness verdict to disclose absences and "not read as clean"; FR-018/C-605 define `nothing-pending` as an explicit success with no record but do not say whether it must carry the per-source presence/absence bookkeeping (sharp edge: all roots absent → zero candidates). | State that `nothing-pending` carries the per-source presence readings (recommended) or explicitly declare it disclosure-free. |
| **U-04** | underspecification | scan bookkeeping assertions (SC-001 final) + guard tests | **LOW** | `requirements.md:283` (FR-015); `data-model.md:154-156` (E-13); `contracts/completeness-refusal.contract.md:12` (C-602) | The identity's counting units mix vocabularies: FR-015 says "扫描候选 = 呈现行来源 + 合并引用 + 具名排除" while E-13 uses `presented_rows` and then `reference_total = presented candidates + duplicate_merged candidates`; for a row with several references the term "presented candidates" admits two readings (rows vs candidates-represented-on-rows) with different sums. | Fix the E-13 wording ("sum of per-row reference counts = candidates represented on presented rows + duplicate-merged candidates") and align C-602/FR-015 vocabulary. |
| **A-02** | ambiguity | none (vocabulary vs emission surface) | **LOW** | `requirements.md:304` (FR-030); `contracts/objection-reply.contract.md:18` (C-408); `shared/guidelines/confirmation-gates.md:75-86`; `data-model.md:135-137` (E-11) | The disposition→gate-observation mapping is owned, but no artifact pins where the mapped signal is materialized (batch record disposition vs a gate-observation entry at a probe); the decide flow declares no probe obligation. | Name the signal surface (or declare the mapping documentary). If a gate-observation entry is expected, add the probe obligation. |
| **G-03** | coverage-gap | none (process-row coverage note) | **LOW** | `tasks.md:189` (T002), `:191` (T004), `:238` (T022), `:263` (T031), `:286` (T038), `:308` (T044), `:331` (T051), `:346` (T057), `:65` (map declaration) | Eight task rows carry no FR/SC anchor: they appear in no Requirement Coverage Map row and cite no FR-/SC- id on their own lines. Six are evidence/mirror/gate/quickstart process rows that plausibly serve FR-042/FR-044 but do not say so. | Add the intended anchors (FR-042 for mirror-verify rows, FR-044 for gate/evidence rows, SC-005 for the quickstart run) or list them as declared process rows in the coverage note. |
| **I-05** | inconsistency | none (descriptive count in live headers) | **LOW** | `plan.md:5`; `tasks.md:7`; `feature-ref.md:5`; `requirements.md:401-425`; `checklists/requirements-quality-2026-11-27.md:6` | Three live headers say "13 clarification rows" while requirements contains 16 `- Q:` rows (11 + 5). The quality checklist measured and disclosed the stale count; the headers were not corrected. No rule gates on the count. | Correct the three headers to 16 (or drop the count from live headers). |
| **I-06** | inconsistency | none (record-shape claim; no downstream rule reads it) | **LOW** | `requirements.md:61` (A-10); `shared/guidelines/decision-tension.md:3-35`; `plan.md:72-87`; `.specify/register.md` (no T- row for 112) | A-10 claims the decision-tension owner's form, but the owner's closed form is six fields **plus** a `tension_id` (`T-NNN`) carried as a `### T-NNN —` section; A-10 is an inline cell with the six labeled fields and no identifier/registration. The plan's pass-I verdict (ok, 0 records) is valid for `plan.md`, the only pass-I judged object; this is the requirements-side form claim, so the load-bearing decision has no `T-NNN` in any carrier. | Mint an owner-compliant `T-NNN` record (and register it), or reword A-10's form claim to "six-field content inline; identifier minted at plan/review". |
| **F-01** | feature-relevance | none (feature detail text; T011 countermands the pin edit) | **LOW** | `.specify/features/112-decision-batch-panel.md:44`; `tasks.md:174` (Measured Premises), `:209` (T011); `research.md:21` (M-11) | The detail still carries the plan-stage simplification "census pin 122 → 123", while the measured registry is 130 objects and T011 explicitly forbids the 122 + 1 shortcut. Metadata drift on a live carrier, mitigated by T011. | Refresh the detail's line to "130 (re-measured at edit time; see T011)". |

## Coverage Summary

| Lane | Result | Source |
|------|--------|--------|
| FR → task row | **45/45** (map rows; every FR named) | `tasks.md` § Requirement Coverage Map; machine-checked |
| SC → task row | **10/10** | same |
| FR → contract clause | **44/45** — FR-043 uncovered (G-02) | `account-clause-coverage.py` FR lane; six contracts |
| Contract clause → `[green:]` claim | **54/54 exactly once** (10/8/7/9/12/8; no duplicate, no miss) | `tasks.md` green claims; machine-checked |
| Clause-coverage accountant | `[fr-uncovered]` fail (1); clause-delta lane **unjudgeable** (`status: baseline-missing`, exit 2 — G-01); claimed clauses 54; `[clause-unparsable]` fail (111, 1 file declares a positive form) | run this stage |
| Single-task coverage floor sample | FRs on a single task row: FR-002→T007, FR-038→T047, FR-043→T053; each row's text carries the mapped obligation (vocabulary + P-13; transmission chain test; command doc) | `tasks.md`; verified by reading the three rows |
| Deliverable paths | all new deliverables absent (mechanism is new; expected pre-implementation); 77 pre-analyze advisories, every one a `missing-path` for a deliverable this feature creates | `pre-analyze-check --stage tasks` |
| Unmapped tasks | T002, T004, T022, T031, T038, T044, T051, T057 (G-03) | machine extraction |

## Feature Linkage Summary

| Check | Result |
|-------|--------|
| Feature bound | **Feature 112 — Batch Decision Panel（批量决策面板）** (new standalone feature; additive extension of Feature 107's owner page, never a slice) |
| Index row | `.specify/features.md:119` — `Planned`; Details/Spec paths present; Last Updated `2026-11-27` |
| Detail file | `.specify/features/112-decision-batch-panel.md` — `Status: Planned`; Overview / Latest Review / Key Changes / Implementation Notes / Future Evolution / Related Files / Status Tracking / Related Specifications present; the corrected 17-row baseline is recorded and the 8-row slip is disclosed (PA6 applied) |
| Stage record | Checklist stage (checkpoint 05) does not advance the lifecycle; Planned is the current lawful status; the detail's `(current — 2026-11-27)` marker sits on Planned, so no stale-marker defect |
| Parent / reverse reference | 112 → 107 parent pointer present (detail § Related Specifications); 107 → 112 reverse citation absent — no duty found for it (feature-details template has no reverse-reference requirement), recorded as a one-way link observation |
| Stale metadata | One: the probe census pin in the detail (F-01) |
| Registry edits this stage | None (read-only; `.specify/register.md`, `features.md` and the detail untouched) |

## Constitution Alignment

**No constitution conflicts — 0 CRITICAL.** All 23 principles (v1.20.0) were re-read against the artifacts: Principle IV holds (Tests Mode ON, red-first obligations named per contract, the T042 regression-exception declared and ordered); Principle XIV holds at spec/design level (owner-page extension, pointer duties; delivery surfaces are required to be pointer-only); XVII/XXI hold (no new runtime directory; engine interface contract declared); XX holds (single test entry). I-01/I-02 are design-contract contradictions between clauses of the same requirements/contract set, not principle conflicts, so they stay HIGH and are not CRITICAL. No finding is a constitution `downgrade` candidate.

## Decision-Tension Records (pass I)

`python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/112-decision-batch-panel --json` → **status: ok**, 0 errors, 0 warnings, **0 records**; all six labels pass (`dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form`, `expected-sacrifice-unmapped`). The judged object is `plan.md` only: its `## Decision Tensions` section sits between Constitution Check and Project Structure and carries a compliant `N/A` with one reasoned line per load-bearing trigger. No pass-I defect exists. I-06 is recorded separately (the requirements-side inline A-10 form), explicitly **not** a pass-I verdict.

## Checklist Accountability (pass H)

`checklists/requirements.md` — all items checked (`[x]`); no unchecked `[Gap]` item.
`checklists/requirements-quality-2026-11-27.md` — 40 items, all unchecked; `[Gap]`-tagged items are CHK002, CHK006, CHK013, CHK023, CHK037:

```
CHK002 disposition: raised-as-finding A-01
CHK006 disposition: covered-by data-model.md § E-8 + contracts/objection-reply.contract.md § C-406 + research.md § D-1
CHK013 disposition: covered-by requirements.md § FR-023 + FR-029 + contracts/default-derivation.contract.md § C-306
CHK023 disposition: covered-by data-model.md § E-9 (closing carries source-update outcomes and disclosures) + requirements.md § FR-035
CHK037 disposition: covered-by requirements.md § FR-034 + contracts/record-replay.contract.md § C-505
```

Count: unchecked `[Gap]` 5 − raised-as-finding 1 − covered-by 4 − undispositioned 0 = **0**.

Adjudication of the 16 candidate confirmation points named in the checklist's closing note:

| CHK | Disposition | Where |
|-----|-------------|-------|
| CHK001 | raised-as-finding **A-01** | de-emphasis mark set; "tracked" definition |
| CHK002 | raised-as-finding **A-01** | register authority-path cell |
| CHK003 | covered-by `A-22` + `FR-009` + `C-104` | byte-equal identity, locator pairing, merge lists all sources |
| CHK004 | covered-by `requirements.md` § Batch States + `quickstart.md` Scenario 2 | the state section allows plural named reasons ("资格原因 MUST 具名"), FR-010/FR-011 do not claim exclusivity, and the first real batch co-names `class-missing` + `authority-unresolved` |
| CHK006 | covered-by `E-8` + `C-406` + `D-1` | closed authorization enum, caller declares, missing = unattended |
| CHK011 | covered-by `D-5` + `C-304` | pointer resolution = path exists + anchor findable |
| CHK012 | covered-by `C-305` + `E-5`/`E-7` | grounding (domain 5) is orthogonal to qualification (domain 3); `incomplete` and `no-evidence` may co-exist; C-305 forces `no-evidence` |
| CHK013 | covered-by `FR-023`/`FR-029`/`C-306` + `FR-016` | multiple prior records: any differing record triggers the conflict; unreadable carrier refuses |
| CHK014 | covered-by `A-25` + `C-401` + `FR-045` | reply definition is behaviour-class; verbatim preserved; structure-only machine judgement |
| CHK022 | raised-as-finding **U-02** | settled status-cell grammar |
| CHK023 | covered-by `E-9` + `FR-035` | disclosure lands in the batch record closing section |
| CHK027 | raised-as-finding **U-04** | accounting unit vocabulary |
| CHK032 | raised-as-finding **A-02** | signal emission surface |
| CHK034 | covered-by `C-202` + `C-204` | structured payload vs user-facing body split |
| CHK036 | raised-as-finding **I-02** | supersession append vs batch-record immutability |
| CHK037 | covered-by `FR-034` + `C-505` | redecision re-settles through the same register status-cell update; supersession chain lives in the records |

## Systemic Observations

1. **Cross-batch lifecycle vs immutability is the weakest surface.** I-01 and I-02 hang on the same unscoped sentence ("different batch ids MUST NOT read or modify each other's records"): the concurrency intent is visible only in one requirements edge case, while the read-time join and the supersession append both cross that boundary by design. One scope clarification closes both.
2. **The exclusion/qualification vocabulary is closed at the state level but not at the bookkeeping level.** I-04, U-01 and U-04 each concern a rule that names content the closed states/partition cannot slot (exclusion families, a second option set, reference counting units). The state machine is strong; the accounting around it needs its own explicit units.
3. **The analyze-side coverage lane has an unowned freeze and one plan-only carrier.** G-01 (baseline missing, freeze scheduled at implement) and G-02 (FR-043 has no contract clause) are process/traceability gaps, not design gaps; both are fixable by one tasks remediation.
4. **Verification-path classification is the only gate-level disagreement.** I-03: requirements, tasks and the checklist split 1 vs 2 on SC-010's Path. Requirements owns the marker; the other two should follow it.
5. **Stale derivative counts persist in live carriers after being disclosed.** I-05 (13 vs 16 clarification rows) and F-01 (122 → 123 vs measured 130) were both measured and disclosed by later stages, yet the live texts were not corrected; a disclosure is not a repair for a live artifact.
6. **Predicate determinability is the top implementation risk.** A-01 does not change any rule, but every candidate-universe decision (and SC-001's completeness assertion) depends on the de-emphasis mark set, the authority-path cell and "tracked".

## Metrics

| Metric | Value |
|--------|-------|
| Total FRs / SCs / contract clauses / tasks | 45 / 10 / 54 / 58 |
| FR → task coverage | 100% (45/45) |
| SC → task coverage | 100% (10/10) |
| FR → contract clause coverage | 97.8% (44/45; FR-043, G-02) |
| Clause → green claim | 100% (54/54, exactly once) |
| Feature linkage | bound and consistent (one stale metadata pin, F-01) |
| Findings | 16 total — CRITICAL 0 · HIGH 2 · MEDIUM 6 · LOW 8 |
| By category | inconsistency 6 · underspecification 4 · coverage-gap 3 · ambiguity 2 · feature-relevance 1 · duplication 0 · constitution 0 |
| Ambiguity / Duplication / Inconsistency / Critical | 2 / 0 / 6 / 0 |

## Validation Wave

Two HIGH findings exist. The worker role forbids dispatching agents, so the independent validation wave could not be run by this execution; per the skill's subagent-unavailable fallback both rows were substituted with a **direct evidence re-read** (each clause read in full and re-checked against the other), and each carries the marker `(validated: direct re-read, subagent unavailable)`.

- **I-01 boundaries** — `evidence_supported`: the quoted clauses are literally mutually exclusive on reading prior batch records; the edge case scopes the sentence to concurrent batches. `evidence_not_supported`: that the intended design actually forbids all cross-batch reads in every case (the intent is inferred from FR-012's join, not from a clause that scopes FR-037).
- **I-02 boundaries** — `evidence_supported`: FR-029/C-510 require the append, FR-037/C-507 forbid modifying other batches' records, FR-032/C-503 declare the batch record never overwritten, and I-16/I-18 repeat both sides; no carve-out exists. `evidence_not_supported`: that "永不覆盖" must be read narrowly as upsert-of-the-entry (a narrower reading is possible but unwritten); no batch-produced decision record exists on this tree yet.

Downgrade rate: not applicable (no independent wave). An independent validation wave remains owed by a dispatching orchestrator if the process requires it.

## Residue and Rerun Delta

- **Residue list (round 1)**: none — all 16 findings are open and carried into the JSONL.
- **Rerun delta**: not applicable — first analyze report for 112; no prior report exists.

## Deterministic Checks Run This Stage (read-only)

| Check | Command | Verdict |
|-------|---------|---------|
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/112-decision-batch-panel/tasks.md` | exit 0 — PASS, 0 error / 0 warning |
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/112-decision-batch-panel/requirements.md` | exit 0 — status ok, 437 lines / 55 definition rows / 15 shared strings / 0 error / 0 warning |
| Pre-analyze gate (tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/112-decision-batch-panel --stage tasks --repo .` | `decision=pass`, errors=0, advisories=77 (all `missing-path` deliverables), fr=45 sc=10 tasks=58 clauses=54 |
| Clause/FR coverage accountant | `python3 scripts/python/account-clause-coverage.py .specify/specs/112-decision-batch-panel` | exit 2 — `status: baseline-missing` (G-01); FR lane 44/45 (G-02); claimed clauses 54 |
| Decision tensions | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/112-decision-batch-panel --json` | exit 0 — status ok, 0 errors, 0 records, six labels pass |
| Scan predicate (register) | inline awk predicate over `.specify/register.md` | **17** open OI-/D- rows, ids exactly the spec's corrected list; 0 `### PENDING —` blocks in the four roots |
| Owner page inventory | greps over `shared/definitions/decision-definitions.md` | 9 sections / 9 vocabulary rows / P-01…P-12 (no batch row yet) / M-01…M-09 / B-01…B-07; `CONDITIONAL_FIELDS` = 6, admitted field lines = 15 |
| Frozen inventories | `ls templates/commands/*.md`; `find skills -name SKILL.md`; `ls docs/reference/commands` | 32 commands / 60 skills / 30 docs; `decide` absent (expected) |
| Probe registry | `python3 scripts/python/probe-utils.py --action probes --validate` | 11 classes, 130 internal + 0 external, 0 errors; the test literal 122 is pre-existing drift, disclosed and owned by T011 (noise-floor: not re-filed) |
| Mirror / copy toolchain | `sync-mirrors.py --check`; `regen-command-copies.py --check` | rc 0 (123 files byte-identical); rc 0 (all per-tool copies match) |
| Instruction budget | section extraction on `.specify/instructions.md` | `## Decision Items` = **1,276 B** of the 1,500 B cap (unchanged) |
| Gate neutrality | `python3 .specify/scripts/python/scan-confirmation-gates.py --summary` | 30 blocking (22 destructive / 7 governance-kept / 1 reversible), 0 violations — matches the frozen baseline |
| Knowledge batches | `memory-utils.py --action list --scope knowledge` | 0 `decision-batch-` entries (matches quickstart Scenario 6) |
| Flow class | `flow-class-check.py --action lookup --unit-id spec:112-decision-batch-panel` | `flow_class: execution` / `flow_type: -` / `source: declaration`, rc 0 |
| Machine coverage extraction | in-line program over the 15 domain files | 45 FR / 10 SC / 15 STR / 25 A / 5 US / 24 edge cases / 8 RS / 58 task rows / 11 `[P]` / 54 green claims / 54 clauses; 8 unanchored process rows (G-03) |

## Limits

Read-only artifact analysis. The batch engine, tests and fixtures do not exist yet, so every behavioural claim was judged against the artifacts and the measured owners, not against an execution. Behaviour-class propositions (name completeness, recommendation reasonableness, consequence truthfulness) were not judged — they belong to the named review surfaces (B-08/B-09) and no machine coverage is claimed. The 130-object probe reading is a measured fact of the current registry; its pre-existing test-literal drift is disclosed by the tasks file and excluded here by the noise floor. No network, no push, no register/spine edit.

## Evidence Pointers

- Findings JSONL: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round1-findings.jsonl` (16 records; `propagation_surface` is the first key of every record)
- This report: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round1-report.md`