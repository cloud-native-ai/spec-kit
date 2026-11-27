# Analyze — Round 2 Report: 112-decision-batch-panel

**Run**: `r20261127T094343Z-112a` · **Stage**: analyze, round 2 (incremental; declared **C/H-only** with residue) · **Baseline**: `8aad9c47d` (analyze-repair close-out) · **Round-1 baseline**: `9d1116f42`
**Spec**: `.specify/specs/112-decision-batch-panel/` · **Feature**: 112 Batch Decision Panel（批量决策面板）
**Inputs**: `test-evidence/analyze-round1-findings.jsonl` (0C / 2H / 6M / 8L), `test-evidence/analyze-round1-report.md`, `test-evidence/analyze-repair-round1.md` (I-01/I-02 repair: A-26/A-27), and the repaired artifacts at `8aad9c47d`.
**Authority**: `.specify/constitution.md` v1.20.0; `.specify/instructions.md`; `.specify/features.md` row 112 + `.specify/features/112-decision-batch-panel.md`; `.specify/register.md`; owner pages by pointer (decision-definitions, decision-tension, confirmation-gates, closed-set-claims, one-source-of-truth, acceptance-hardening); the analyze skill and its references.
**Method**: fresh-context worker (role forbids dispatch and spine writes); detection direct; incremental re-check of the repaired loci and their one-hop neighbors. **Touch-volume gate**: the repair touched 8 of the 15 declared domain files (more than half), so the CRITICAL/HIGH adjudication was run over the **full declared domain** — all 15 files re-read in full, not only the repaired loci — while the MEDIUM/LOW layer is C/H-only with the residue enumeration the Rounds rule requires. Deterministic gates full-ran as the backstop. Product artifacts read-only; only this evidence set was written.

## Verdict

**0 CRITICAL · 0 open HIGH.** The two round-1 HIGH findings are repaired and confirmed fixed at the rule level: I-01 (cross-batch read boundary) and I-02 (supersession append vs batch-record immutability) no longer have mutually exclusive MUSTs. The repaired boundary produced **4 new findings — 0 CRITICAL / 0 HIGH / 2 MEDIUM (I-07, U-05) / 2 LOW (A-03, I-08)** — all on the transaction/target semantics and fan-out of the new A-26/A-27 boundary. The 14 open round-1 MEDIUM/LOW findings are carried as residue rows, all `deferred` with reasons.

**The analyze gate is NOT cleared**: G-01 (`coverage-baseline.txt` absent, accountant exit 2, clause-delta lane unjudgeable) and G-02 (FR-043 uncovered) still hold, I-03's verification-path drift is unchanged, and the new MEDIUM U-05 needs one target-state rule before implementation locks the append semantics. "Two HIGH closed" is a cleared backlog, not a clean rerun — stated separately.

## Round Record (incremental protocol)

| Field | Value |
|-------|-------|
| Touched loci (round-1 repair) | `requirements.md` (A-7, A-11, A-26 §77, A-27 §78, FR-012 §279, FR-029 §305, FR-032 §311, FR-037 §316, edge case §246); `contracts/source-roster.contract.md` (C-107 §17); `contracts/record-replay.contract.md` (C-502 §12, C-503 §13, C-507 §17, C-510 §20); `data-model.md` (E-9 §113, record op §190, I-16 §212, I-18 §214); `research.md` (D-7 §42, D-8 §44, §3); `plan.md` (Input §5, PA4 §32, blast radius §84); `tasks.md` (Prerequisites §7, T033 §278, T050 §330); `feature-ref.md` (§5) |
| One-hop neighbors pulled | FR-022/C-303, FR-023/C-306, FR-036/C-508 (the other three read purposes); FR-034/C-505, FR-035/C-506; FR-030/C-408; SC-006; SC-010; T046/T052 (C-510 test/green), T039 (C-507 green), T028/T048 (owner-page authoring), the Feature 112 detail, the two checklists (dated instruments), quickstart Scenarios 3–5, E-13 (U-04) |
| Reused domains (untouched; round-1 M/L analysis reused, hashes measured this round) | see table below |
| Per-carried disposition | 2 `fixed` (I-01, I-02) · 14 `deferred` (residue table) · 0 `rejected` |
| Full-run trigger | fired on touch volume (8/15 > half) → C/H adjudication full-domain; M/L layer C/H-only + residue, per the Rounds rule |

**Domain hashes (sha256, this round)** — the eight repaired files:

| Domain file | sha256 | Round-2 handling |
|-------------|--------|------------------|
| `requirements.md` | `d9feb48d6195d077e82f1bc25be82905232f1fb0a1d81e59c5703919ea1b6bcb` | repaired; re-read in full |
| `plan.md` | `b04912e2b082f8b506205324d602e7160e87837cea202fb636fb25cb6f6ed7f2` | repaired; re-read in full |
| `research.md` | `bcae5dcecc87a5b26545017f4d0075445b29dffcdcc50ead407568a87b3c457b` | repaired; re-read in full |
| `data-model.md` | `e7436b6a8cc84726d185cb7166d252938a7a900ed06a6fffee077e19e576c493` | repaired; re-read in full |
| `feature-ref.md` | `018b88593a443fb46768dde24081209bee28e4e81ef9ead34f63baccf44eb7fa` | repaired (header); re-read in full |
| `tasks.md` | `9668c584f2c16cd25d065a6929ea500ee67a5ec92b4c72c34e7a1ee4bb682a2a` | repaired; re-read in full |
| `contracts/record-replay.contract.md` | `fd2509e95ef3618b19ba6e81788c2a1de81e413369b72cfd2de93b7376bc3140` | repaired; re-read in full |
| `contracts/source-roster.contract.md` | `135166cf5c1a5e6be859848975b6bc5ff21c3d6bf6beb161d4c1dd865e55be8e` | repaired; re-read in full |

**Reused domains** (untouched by the repair; their round-1 M/L analysis is the reused layer; each was re-read in full for the C/H adjudication and spot-checked at the one-hop clauses named above):

| Domain file | sha256 | Reused content |
|-------------|--------|----------------|
| `quickstart.md` | `43b72ff5cd23f8e82f292ae5fcc612c96f6c8522f566bbc3fc8f2934c191aee7` | Scenario 3/4/5 behaviour (append not exercised); no round-1 finding |
| `checklists/requirements.md` | `1eca1048d77f9474966190f032874ca071dc11cbd37cd02e6d92dd47531d0b51` | dated gate checklist; all checked |
| `checklists/requirements-quality-2026-11-27.md` | `e28dc16615b0656f68a968d99bf69ad9a8650784991c5015cbb48a19a4f27910` | dated instrument; CHK036 raises I-02 (now fixed), CHK025/CHK022/CHK027/CHK032 carry the open M/L questions |
| `contracts/completeness-refusal.contract.md` | `897f579e670bc1440953daee1a071514cfba036e1f116f6abe2b7ccbf021a73e` | G-01/G-02/U-03/U-04 carriers unchanged |
| `contracts/default-derivation.contract.md` | `5393c49caee7b28efd5221fb03f74c5ee11f0b864a5293022b8705d266372fd6` | C-303/C-306 are read-purpose anchors (verified) |
| `contracts/objection-reply.contract.md` | `9265d37281c99e1d04cf557b523ecea4e0ba657c6b1ea28128e193b017157d8e` | A-02/U-01 carriers unchanged |
| `contracts/presentation.contract.md` | `2b9a50ba74cd4e8810d3cfbcc850a7fd79ad34439cbcf3ba37c6f526cc534d4e` | C-201/C-206/C-207 unchanged (SC-010 lane) |

## Resolved Since Round 1

| ID | Round-1 severity | Status | Evidence that closed it |
|----|------------------|--------|--------------------------|
| **I-01** | HIGH | **fixed** | FR-037 (`:316`) now states write isolation + no in-flight dependence + the four declared read-only purposes; FR-012 (`:279`) names the join as a permitted read; C-107 (`source-roster:17`) cites A-26; C-507 (`record-replay:17`) lists C-107/C-303/C-306/C-508 and requires read-only; edge case (`:246`), E-9 (`:113`), D-7 (`:42`), T033 (`:278`) aligned. Purpose mapping verified pair-by-pair (C-107=FR-012, C-303=FR-022, C-306=FR-023, C-508=FR-036). *(validated: direct re-read, subagent unavailable)* |
| **I-02** | HIGH | **fixed** | A-27 (`:78`) adopts the single-field append; FR-029 (`:305`), FR-032 (`:311`), FR-037 (`:316`), A-11 (`:62`) name it the sole sanctioned post-write mutation; C-502/C-503/C-507/C-510 (`record-replay:12/:13/:17/:20`), I-16/I-18 (`:212/:214`), E-9/record op (`:113/:190`), D-8 (`research:44`), PA4/blast radius (`plan:32/:84`), T050 (`:330`) aligned. No clause pair remains mutually exclusive. *(validated: direct re-read, subagent unavailable)* |

Both resolutions also carry boundary residues — recorded as new findings, not as re-opened HIGHs: I-07 (the ordered record transaction cannot honour "refused and no new record"), U-05 (no settled-target / same-target concurrency rule), A-03 (the append's constitutive read is outside the four read-only purposes).

## New Findings (round 2)

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **I-07** | inconsistency | `record` op → T050 implementation + T046 unwritable-old-record fixture + SC-006 final-path evidence → implement | **MEDIUM** | `data-model.md:190`; `requirements.md:305` (FR-029), `:362` (SC-006); `contracts/record-replay.contract.md:20` (C-510); `research.md:44` (D-8); `tasks.md:323` (T046), `:330` (T050) | The `record` operation writes the batch record **before** appending `superseded_by`; FR-029/C-510 require an unreadable/unwritable prior carrier to refuse that item's redecision and SC-006 requires that refusal to produce **no new record**. Once the batch record (carrying the decision records) is written, the append-step refusal cannot retract the new record — the ordered design cannot satisfy SC-006's failure case. No clause/task places a prior-carrier readability/writability check before the write. | Add the prior-carrier check to the preconditions that run before `write batch record` (A-24/C-501 scope or the operation order), and state the ordering in T050; keep the post-write failure disclosure for register/source updates only. |
| **U-05** | underspecification | `record` implementation + T033 concurrency test / `concurrency/` fixture + SC-010 guard → implement | **MEDIUM** | `requirements.md:78` (A-27), `:246` (edge case), `:305` (FR-029), `:316` (FR-037), `:366` (SC-010); `contracts/record-replay.contract.md:17` (C-507), `:20` (C-510); `research.md:42` (D-7), `:44` (D-8); `tasks.md:278` (T033) | The A-27 append has no target-state qualifier and no conflict rule for two batches appending to one prior record: FR-037 permits the append for **any** batch (no "settled record"/"non-overlapping batch" condition), SC-010 asserts two concurrent batches' records are mutually non-modifying with no carve-out, and nothing serializes or detects concurrent appends to the same prior record — although every append must leave all pre-existing bytes unchanged (a last-writer-wins interleave breaks that). The repair record's settled-record reading is not stated in any clause. | State the append target as a **settled** prior record; add a conflict rule for same-target appends (first-writer-wins with a re-read and named refusal, or a documented re-append form); align SC-010 and T033's test description with the carve-out. |
| **A-03** | ambiguity | C-507 / T033 read-side guard test → implement | **LOW** | `requirements.md:77` (A-26), `:78` (A-27), `:305` (FR-029), `:316` (FR-037); `contracts/record-replay.contract.md:17` (C-507), `:20` (C-510); `data-model.md:190`; `tasks.md:278` (T033) | The four permitted cross-batch reads are all read-only, while the sanctioned append is a read-modify-append whose own read (locate the record, preserve bytes) is neither one of the four purposes nor read-only. Two readings compete (constitutive read included in the write vs outside the permitted read set), and a literal read-side guard could forbid the append. | Name the append's constitutive read inside the A-27 exception (one clause in FR-037/C-507), or scope the read-purpose sentence to informational reads. |
| **I-08** | inconsistency | owner page § Batch Record Contract / § Redecision & Supersession (T028/T048) → M-15 guard → implement | **LOW** | `.specify/features/112-decision-batch-panel.md:34`; `tasks.md:260` (T028), `:328` (T048), `:278` (T033); `requirements.md:311` (FR-032), `:316` (FR-037); `contracts/record-replay.contract.md:13` (C-503), `:20` (C-510) | The A-27 carve-out is missing from the live derived carriers that cite its clauses: the Feature detail says "never overwritten (A-11, FR-032, FR-037)"; T028 lists "create-only/never-overwrite" for the owner page's § Batch Record Contract; T048 authors § Redecision & Supersession without A-27; T033 says "mutual write isolation" without the append. Executing these rows alone would re-land the pre-repair contradiction at the owner page. | Add the A-27 single-field exception to the four derived carriers in the same change that authors the owner page. |

**Why I-07/U-05 are MEDIUM and not HIGH**: the requirement/contract rule set is consistent and both criteria are testable — the mandated red-first fixtures (T046, T033 `concurrency/`) are the detection surfaces, and each fix is an ordering/target-state sentence, not a rule change. No new CRITICAL or HIGH exists on the repaired tree.

## Residue — Open Round-1 MEDIUM/LOW (all deferred)

| ID | Severity | Status | Disposition | Reason (round-2 disposition) |
|----|----------|--------|-------------|------------------------------|
| G-01 | MEDIUM | open | deferred | Freeze is `/speckit.tasks`'s duty, scheduled as implement T004; analyze MUST NOT `--freeze`; no tasks remediation ran between rounds. Re-verified: baseline absent, accountant exit 2, 787 errors, FR lane 44/45. |
| G-02 | MEDIUM | open | deferred | No contract clause or declared plan-only disposition was added. Re-verified: `grep FR-043 contracts/` → zero matches; carrier remains plan § Source Code + T053. |
| I-03 | MEDIUM | open | deferred | No Path marker or copy changed. Re-verified: requirements SC-010 supporting (`:366`) vs tasks DoD-7 (`:23`) / GATE-4 (`:32`) final set vs CHK038 (`:81`). |
| I-04 | MEDIUM | open | deferred | FR-007/C-108/E-13 untouched; the named-exclusion semantics decision belongs to requirements/plan. |
| A-01 | MEDIUM | open | deferred | Roster predicate wording untouched (de-emphasis marks, authority-path cell, "tracked" all still undefined). |
| U-01 | MEDIUM | open | deferred | Source-conflict presentation contract untouched; E-5 still has one option-set slot; C-403 still validates against "the presented option set". |
| A-02 | LOW | open | deferred | FR-030/C-408/E-11 untouched; the signal emission surface is still unnamed. |
| G-03 | LOW | open | deferred | Re-verified mechanically: T002, T004, T022, T031, T038, T044, T051, T057 — in_map=0, own-line FR/SC=0 for every row. |
| I-05 | LOW | open | deferred | Re-verified: 16 `- Q:` rows; `plan.md:5`, `tasks.md:7`, `feature-ref.md:5` still say 13. |
| I-06 | LOW | open | deferred | Re-verified: zero `### T-` sections in requirements; no T- row for 112 in the register; A-10 remains the inline six-field cell. |
| U-02 | LOW | open | deferred | FR-034/C-505 value grammar untouched. |
| U-03 | LOW | open | deferred | FR-017/FR-018/C-604/C-605 untouched; the nothing-pending disclosure duty is still unstated. |
| U-04 | LOW | open | deferred | E-13 (`data-model.md:155-156`) counting-unit wording untouched. |
| F-01 | LOW | open | deferred | Re-verified: detail line 44 still "census pin 122 → 123"; measured registry 11 classes / 130 objects. |

Residue count: **14 = 6 MEDIUM + 8 LOW**, all open, all deferred, no rejected rows. None is silently dropped: each carries `status` + `disposition` + `disposition_reason` in `analyze-round2-findings.jsonl`.

## Coverage Summary

| Lane | Result | Source |
|------|--------|--------|
| FR → task row | **45/45** (map rows; every FR named) | `tasks.md` § Requirement Coverage Map |
| SC → task row | **10/10** | same |
| FR → contract clause | **44/45** — FR-043 still uncovered (G-02) | `account-clause-coverage.py` FR lane; `grep` over `contracts/` |
| Contract clause → `[green:]` claim | **54/54 exactly once** (10/8/7/9/12/8; no duplicate, no miss) | `tasks.md` green claims |
| Clause-coverage accountant | `[fr-uncovered]` fail (1); clause-delta lane **unjudgeable** (`status: baseline-missing`, exit 2 — G-01); claimed clauses 54; scanned 350 files; clause universe 2618 | run this stage |
| Zero-finding-floor sample (no open C/H exists) | **Single-task-row FRs** — FR-002→T007, FR-038→T047, FR-043→T053: each row's text carries the mapped obligation. **Repaired-FR sample** — FR-012→T013/T019/T034, FR-029→T046/T048/T050, FR-032→T024/T028/T030, FR-037→T024/T028/T030/T033/T036: all present; the read purposes appear in T033; the A-27 engine case in T050; the owner-page/derivative omissions are I-08. **Multi-row sample** — FR-044 (8 rows) present. Sample size 3 + 5 + 1 FRs, outcome clean for C/H purposes | `tasks.md`; direct row reads |
| Deliverable paths | all new deliverables absent (mechanism is new; expected pre-implementation); 77 pre-analyze advisories, every one `missing-path` | `pre-analyze-check --stage tasks` |
| Unmapped tasks | T002, T004, T022, T031, T038, T044, T051, T057 (G-03) | machine extraction |

## Feature Linkage Summary

| Check | Result |
|-------|--------|
| Feature bound | **Feature 112 — Batch Decision Panel（批量决策面板）** (standalone; additive extension of Feature 107's owner page) |
| Index row | `.specify/features.md:119` — `Planned`; Details/Spec paths present; Last Updated `2026-11-27` |
| Detail file | `.specify/features/112-decision-batch-panel.md` — `Status: Planned`; required sections present; `(current — 2026-11-27)` marker on Planned (lawful) |
| Stage record | Analyze stages do not advance the lifecycle; `Planned` remains the lawful status; the analyze-repair did not edit the registry |
| Stale metadata | Two: the probe census pin (F-01) and the missing A-27 carve-out in the record summary (I-08) |
| Registry edits this stage | **None** (read-only; `.specify/register.md`, `features.md` and the detail untouched) |

## Constitution Alignment

**No constitution conflicts — 0 CRITICAL.** All 23 principles (v1.20.0) were re-checked against the repaired clauses: Principle XIV holds (the owner page remains the single owner; the carve-out is a named exception, not a second rule surface); Principle VI/XVI hold (the append is append-only and every failure is disclosed or refused — I-07/U-05 tighten this, they do not weaken it); IV/XXI/XX hold (Tests Mode ON, red-first obligations named per contract, single test entry, engine interface declared). The repaired plan edits (PA4, blast radius) do not touch any Constitution Check row. No principle is a `downgrade` candidate; method is a disclosed direct re-read (the PA1/objective-analysis-gate fallback pattern).

## Decision-Tension Records (pass I)

`python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/112-decision-batch-panel --json` → **status: ok**, 0 errors, 0 warnings, **0 records**, all six labels pass; scanned 179 lines. The judged object (`plan.md`) still carries `## Decision Tensions` as the direct successor of `## Constitution Check` and predecessor of `## Project Structure`; the repaired blast-radius bullet now includes A-27 and leaves the four-trigger N/A justification intact. I-06 (the requirements-side inline A-10 form) remains a residue row, explicitly **not** a pass-I verdict.

## Checklist Accountability (pass H)

`checklists/requirements.md` — all items checked; no unchecked `[Gap]` item.
`checklists/requirements-quality-2026-11-27.md` — 40 items, 0 checked; item-level `[Gap]` tags: CHK002, CHK006, CHK013, CHK023, CHK037.

```
CHK002 disposition: raised-as-finding A-01
CHK006 disposition: covered-by data-model.md § E-8 + contracts/objection-reply.contract.md § C-406 + research.md § D-1
CHK013 disposition: covered-by requirements.md § FR-023 + FR-029 + contracts/default-derivation.contract.md § C-306
CHK023 disposition: covered-by data-model.md § E-9 + requirements.md § FR-035
CHK037 disposition: covered-by requirements.md § FR-034 + contracts/record-replay.contract.md § C-505
```

Count: unchecked `[Gap]` 5 − raised-as-finding 1 − covered-by 4 − undispositioned 0 = **0**. The checklist's closing-note candidates keep their round-1 adjudications; CHK036's raise (**I-02**) is now `fixed` (A-27/C-510) and the entry remains satisfied as raised. The checklist is a dated instrument and was not rewritten; CHK025's "互不读写" wording is the pre-repair question phrasing, answered by A-26/A-27.

## Validation Wave

No open CRITICAL/HIGH exists in this round, so no validator wave is owed; the zero-finding-floor sample above substitutes for the empty wave. The two resolution verdicts (I-01, I-02) are marked `(validated: direct re-read, subagent unavailable)` because the worker role forbids dispatching agents — an independent wave remains available to the orchestrator if the process requires it. Downgrade rate: not applicable; no severity was downgraded or rejected.

## Systemic Observations

1. **The repaired rule surface is coherent; the defect has moved one layer down — into transaction sequencing and fan-out.** I-01/I-02 (rule contradictions) are gone; I-07 (operation order vs refusal), U-05 (target-state/concurrency), A-03 (read/write boundary) and I-08 (derived-carrier omissions) are all *downstream* of the same carve-out. One clause amendment plus one precondition sentence closes I-07/U-05/A-03; four carrier edits close I-08.
2. **The append is now the only cross-batch write and the only write to a foreign file.** It is also a read-modify-write on a shared file — the framework's per-entry-isolation model no longer covers that path. This is the single highest-value sentence still missing from the spec chain.
3. **The gate's remaining weight is the MEDIUM backlog, not C/H.** G-01 (unowned freeze), G-02 (plan-only FR), I-03 (copied Path classification) and I-04 (named-exclusion accounting) are all one remediation away; none is a rule contradiction.
4. **Live derivative counts still drift after disclosure.** I-05 (13 vs 16) and F-01 (122 → 123 vs 130) persist; a disclosure is not a repair for a live carrier.
5. **The analyze/worker topology still files its validation as a direct re-read.** Round 2 produced no C/H to validate; the topology gap already recorded in the round-1 feedback entry remains for the framework owner.

## Metrics

| Metric | Value |
|--------|-------|
| Total FRs / SCs / contract clauses / tasks / assumptions | 45 / 10 / 54 / 58 / 27 |
| FR → task coverage | 100% (45/45) |
| SC → task coverage | 100% (10/10) |
| FR → contract clause coverage | 97.8% (44/45; FR-043, G-02) |
| Clause → green claim | 100% (54/54 exactly once) |
| Findings this round (rows) | 20 = 2 resolved HIGH + 4 new (0C/0H/2M/2L) + 14 residue (6M/8L) |
| Open by severity | **0 CRITICAL · 0 HIGH · 8 MEDIUM · 10 LOW** |
| Ambiguity / Duplication / Inconsistency / Critical (open set) | 3 / 0 / 6 / 0 |
| Residue compliance | 14/14 carried, 0 dropped, 0 rejected |
| Downgrade rate | not applicable (no independent wave; no downgrades) |

## Rerun Delta

- **Resolved Since Last Run** — **I-01** (evidence: FR-037 `:316`, FR-012 `:279`, C-107 `:17`, C-507 `:17`, edge case `:246`) and **I-02** (evidence: A-27 `:78`, FR-029 `:305`, FR-032 `:311`, C-502/C-503/C-507/C-510, I-16/I-18, D-8, PA4, T050). Both closed by the round-1 repair; verified by direct re-read.
- **New Since Last Run** — **I-07, U-05** (MEDIUM) and **A-03, I-08** (LOW). I-07/U-05/A-03 are introduced by the repair's new boundary; I-08 is the repair's fan-out gap. None is CRITICAL/HIGH.
- **Carried over** — the 14 residue rows above, each with its disposition.
- The headline is deliberately split: **cleared backlog** (both HIGHs fixed) and **clean rerun** (achieved for C/H; not achieved overall because G-01/G-02/I-03 and the new MEDIUMs remain).

## Deterministic Checks Run This Stage (read-only except the evidence writes)

| Check | Command | Verdict |
|-------|---------|---------|
| Requirements structure | `validate-requirements.py …/requirements.md` | exit 0 — status ok, 439 lines / 55 definition rows / 15 shared strings / 0 error / 0 warning |
| Tasks structure | `validate-tasks.py …/tasks.md` | exit 0 — PASS, 0 error / 0 warning |
| Pre-analyze gate (tasks) | `pre-analyze-check.py --spec-dir … --stage tasks --repo .` | `decision=pass`, errors=0, advisories=77 (all missing-path), fr=45 sc=10 tasks=58 clauses=54 |
| Clause/FR coverage accountant | `account-clause-coverage.py .specify/specs/112-decision-batch-panel` | exit 2 — `status: baseline-missing` (G-01); FR lane 44/45 (G-02); claimed clauses 54 |
| Decision tensions | `validate-decision-tensions.py --spec … --json` | exit 0 — status ok, 0 records, six labels pass |
| Flow class | `flow-class-check.py --action lookup --unit-id "spec:112-decision-batch-panel"` | `flow_class: execution` / `flow_type: -` / `source: declaration`, rc 0 |
| Mirror / copy toolchain | `sync-mirrors.py --check`; `regen-command-copies.py --check` | rc 0 (shared 123 files, templates 23, skills 439/139, agents 20, scripts 134 byte-identical); rc 0 |
| Gate neutrality | `scan-confirmation-gates.py --summary` | 30 blocking (22 destructive / 7 governance-kept / 1 reversible), 0 violations — matches baseline |
| Probe registry | `probe-utils.py --action probes --validate` | 11 classes, 130 internal + 0 external, 0 errors (literal 122 drift owned by T011) |
| Knowledge batches | `memory-utils.py --action list --scope knowledge --format json` | 0 entries; 0 `decision-batch-` entries (matches quickstart Scenario 6) |
| Recheck greps | FR-043 in contracts; `- Q:` count; SC-010 final-set copies; 8 unanchored rows; census pin; `### T-` count; baseline presence | all round-1 M/L findings reproduce unchanged (see residue table) |
| Workspace signature | `workspace-guard.py --check …/workspace-analyze-repair.json --repo . --json` | `{"status": "clean", "changed": []}`, rc 0 — no refs/specs drift since the repair snapshot |
| Capture | full output | `test-evidence/analyze-round2-gates.txt` |

## Limits

Read-only artifact analysis; the batch engine, tests and fixtures do not exist yet, so every behavioural claim was judged against the artifacts and the measured owners. Behaviour-class propositions (name completeness, recommendation reasonableness, consequence truthfulness) were not judged — they belong to B-08/B-09 and no machine coverage is claimed. The quality checklist is a dated instrument and was not rewritten. The 130-object probe reading is a current measured fact. The append's same-target concurrency hazard (U-05) is flagged as an underspecified edge, not demonstrated by execution. No network, no push, no spine/registry edit; G-01 keeps the clause-delta lane unjudgeable and that is stated, not waived.

## Evidence Pointers

- Findings JSONL: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-findings.jsonl` (20 records; `propagation_surface` is the first key of every record)
- Gate capture: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-gates.txt`
- This report: `.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-report.md`
- Round-1 inputs: `analyze-round1-findings.jsonl`, `analyze-round1-report.md`, `analyze-repair-round1.md`