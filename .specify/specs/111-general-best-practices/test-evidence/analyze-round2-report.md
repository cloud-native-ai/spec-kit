# Analyze Round-2 Report — 111-general-best-practices (incremental)

**Stage**: analyze (round 2, incremental) · **Baseline**: `61e3ccfb6` · **Line run id**: `r20261127T071500Z-111a` · **Round accounting run id**: `r20261127T074400Z-111a-analyze-r2` · **Worker**: SDD Analysis Worker (read-only analysis seat) · **Date**: 2026-11-27
**Spec**: `.specify/specs/111-general-best-practices/` · **Quartet**: `flow_class=execution; source=declaration; marker=; error=-`
**Findings file**: [`test-evidence/analyze-round2-findings.jsonl`](./analyze-round2-findings.jsonl) (14 records: 3 closed-fixed · 9 residue · 2 new; JSON-validated)
**Concurrency**: requested=1 · effective=1 · reason=single-unit

## 0. Verdict summary

- **Round-1 blocking set adjudicated on the repaired tree: all FIXED.** AR1-02 (CRITICAL), AR1-01 (HIGH), AR1-03 (HIGH) are resolved by cause; no CRITICAL or HIGH finding remains open.
- **New in round 2: 1 MEDIUM · 1 LOW.** AR2-01: eight summary/checkpoint loci still describe accumulation as pointer-only — the US2 Checkpoint line would fail a correct US2 implementation. AR2-02: the accumulation contract header's owner list omits the `**来源**` shape that A-22/E8 assign to the manifest.
- **Residues**: 8 round-1 MEDIUM/LOW findings carried open (`deferred`); AR1-12 closed as no-defect (`rejected`).
- **Open set: CRITICAL 0 · HIGH 0 · MEDIUM 4 · LOW 6.**
- Validators on the repaired tree: requirements `0 error / 0 warning` (229 lines, 16 definition rows, 7 shared strings); tasks `PASS 0 error / 0 warning`.

## 1. Incremental protocol and read domain

- **Touched-loci set** (from the repair commit diff `4f6905a95..61e3ccfb6`):
  - `requirements.md` — Reading scenario (L9); Binding basis (L19); 本特性交付 / 不做什么 (L36/L38); A-4 (L47); A-17 (L60); A-22/A-23/A-24 (L65–L67); US2 goal/why/test/scenarios (L89–L99); FR-004 (L140); Key Entities Entry/Observation (L150–L152); RS-002 (L162); SC-003 (L171); Clarifications session 2026-11-27 (L223–L229).
  - `contracts/manifest.contract.md` — C-104(c) (L20).
  - `contracts/accumulation.contract.md` — header owner list (L4); C-301 (L6–L8); C-302 (L10–L12); C-304 (L18–L20); C-305 (L22–L24).
  - `data-model.md` — owner statement (L3); E2 accumulation_pointer (L28); E7 rows `review_marker`/`review_stem`/`unit_convention` (L70–L81); E8 generality_basis (L82–L90); INV-08 (L140).
  - `plan.md` — Summary (L9); Constitution Check XIV (L44); Decision Tensions bullet (L69); EP-002 (L123).
  - `quickstart.md` — S-4 (L92–L98).
  - `research.md` — M3 (L19–L22); R-5 (L86).
  - `feature-ref.md` — Binding basis (L9); delivery row 1 (L18); FR-004 row (L35); SC-003 row (L48); Work packages (L60); Re-measure list (L61).
  - `tasks.md` — Requirement Coverage Map FR-006 row (L90); T007A (L178); T008 blockedBy (L179); US2 Goal (L187) / Independent Test (L189); T009 (L193); Dependencies (L237); doc-feature flow (L252); Notes 零新机制 (L301).
- **One-hop neighbors re-read**: US2 Checkpoint (L196), Organization (L13), Incremental Delivery (L288); plan Project Structure (L97) and Inherited Blockers (L130); requirements 本特性交付 (L36) and Key Entities Manifest (L151); accumulation header vs C-303 vs data-model E8; the full green-tag partition (T008 8 / T010 9 / T013 2 / T015 3 / T019 2); T011–T015 dependency chain; the engine's record validation block; `probe-utils.py` action set; Shared Strings; C-103/C-204/C-403/C-404/C-406; GATE-7/T019; A-15/A-20/FR-001/FR-003/FR-005/FR-007.
- **Reused domains (path + SHA-256)**:

| Path | SHA-256 | Reused for |
|---|---|---|
| `test-evidence/analyze-round1-findings.jsonl` | `c2c30914fae3ba7d3c377e99f00c02b6d70e1d92c5b59bb0a3efd539d862d485` | round-1 finding set and severity/anchors (residue source) |
| `test-evidence/analyze-round1-report.md` | `10f9c6478f59185580cc04cd5ca107b77041a026b994eb7439a5c5f82fc3cb59` | round-1 method, readings and constitution verification |
| `test-evidence/analyze-repair-round1.md` | `5a1db1b15289b8b011998807e527a629181df5f4cb2a1561b171c28fa586873c` | repair resolutions and the engine measurements behind A-22/A-23 |
| `test-evidence/analyze-repair-pre-analyze.json` | `b5a8867c19190552a4e6ab2d2a89c739df4b204a0599041691ff97050355b83a` | tasks-stage pre-analyze verdict at `61e3ccfb6` (`decision=pass`, tasks 20, clauses 24, advisories 150, errors 0) |
| `test-evidence/analyze-repair-pre-analyze.txt` | `3b0514b0a55a4410749ddb461f6393a236a8b021878bf5b53f87ce00b9000da2` | same reading, human view |

- **Product artifacts re-read on the repaired tree (SHA-256 prefix 16)**: `requirements.md` `592062091bd343a9` · `plan.md` `4426c256e91ae5f7` · `data-model.md` `cb7cffe577b8505c` · `research.md` `552e1f835363e416` · `quickstart.md` `804f8200fcb8495d` · `feature-ref.md` `d8c525c66fea178f` · `tasks.md` `751897203f22104f` · `contracts/accumulation.contract.md` `c5185cfd97dc252d` · `contracts/distribution-guard.contract.md` `b9ca11672c475e2d` · `contracts/entry-shape.contract.md` `3fcab4e37bfdb435` · `contracts/manifest.contract.md` `ab6fe27a122e04f9`.
- **Fresh engine probes (2026-11-27)**: `feedback-utils.py --action args-manifest` → `record` required `[--unit-id, --run-id, --review, --points]`, source `[]` (no `notes`); `feedback-utils.py:857-873` enforces `custom:` + `custom-unit` and `/speckit.<command>` / `skill:<name>` + `command`/`skill`; `probe-utils.py --help` → actions `{probes, map, probe-inject, handlers, compile-embeds}`, `probe-inject` takes `--unit custom:<owner>/<name>`.

## 2. Re-adjudication of the round-1 CRITICAL/HIGH set

| Finding | Was | Verdict | Basis (one line) |
|---|---|---|---|
| AR1-02 | CRITICAL | **FIXED** | Promotion procedure + generality criterion + `**来源**` shape are owned by the manifest's 逐步积累机制 section (A-22) across all nine artifact families; `knowledge-promotion.md` is cited only for the knowledge-recording obligation it defines; C-305 no longer forbids what C-104(c)/C-302/T009 require; Constitution Check XIV pass is supported. |
| AR1-01 | HIGH | **FIXED** | The carrier is the engine's real `--review` text; the identity convention matches the engine's validation exactly; the probe prerequisite names a real action; zero `notes` carrier references remain. |
| AR1-03 | HIGH | **FIXED** | T007A (write-mode mirror regeneration) is ordered after T005/T006/T007 and before T008; T008's blockedBy includes it; C-404's prelude is unchanged; no green checkpoint is impossible as ordered. |

**AR1-02 — ownership chain check.** A-22 (L65) splits ownership three ways: the manifest owns procedure/criterion/来源 shape; `feedback-utils.py` owns the record shape, store and disposal; `knowledge-promotion.md` owns the knowledge-recording obligation and emphasis escalation. The split is restated consistently in FR-004 (L140), C-301/C-302/C-305, C-104(c), data-model (owner statement, E2, E7, E8, INV-08), plan Summary/XIV/EP-002, research M3/R-5, tasks US2/T009/Notes, quickstart S-4 and feature-ref. All remaining `knowledge-promotion` mentions were enumerated (requirements L19/L47/L93/L171; tasks L76/L189/L301; plan L123; research L22; quickstart L22/L94) and every one frames it as the knowledge-recording owner. The one-hop asymmetry it leaves is AR2-02.

**AR1-01 — engine-form check.** A-23 records the measured basis: `record` requires `--unit-id/--run-id/--review/--points`; `--notes` is parser-declared but silently dropped (no `notes` field exists). The declared convention matches `action_record`'s validation branch byte-for-byte in semantics: `custom:best-practices/observation` requires `--unit-type custom-unit`; `/speckit.<command>` and `skill:<name>` units require `command`/`skill`. The probe prerequisite is real (`probe-inject`, `--unit custom:<owner>/<name>`). A grep over the artifact set finds no residual `notes` carrier reference.

**AR1-03 — ordering check.** Chain is now `T005 → T006/T007 [P] → T007A → T008 → T009 → T010 → T011 → T012 → T013/T014 → T015`; no cycle; T007A carries no `[green:]` tag; the guard prelude's minimum path set is present at T008 time (repo files plus T004's guard and T007A's mirror). Caveat: the mirror is still absent today, so this is a design-level adjudication; red-first remains a plan premise.

## 3. New findings

**AR2-01 (MEDIUM, consistency) — stale pointer-only characterizations survive the A-22 repair.**
Eight summary/checkpoint loci still describe accumulation as pointer-only: `requirements.md` L36 (`积累机制指针`) and L151 (`Key Entities Manifest: … 积累机制指针`); `plan.md` L9 (`progressive accumulation declared by pointer`, inside the same sentence that declares module-owned promotion rules), L97 (`accumulation by pointer`), L130 (`the accumulation owners are consumed read-only by pointer (FR-004)`); `tasks.md` L13 (`观察 / 晋升 / 来源追溯的指针声明`), L196 (`积累路径只以指针复用既有 feedback + memory 引擎`), L288 (`积累机制以指针声明`). The severity-bearing locus is the US2 Checkpoint (L196): a checkpoint is a verdict surface, and applied literally it fails a correct US2 implementation, because T009 must declare the manifest's own promotion procedure and generality criterion. Each locus contradicts A-22 (L65) and FR-004 (L140); the normative clauses are correct, so this is a summary-layer sweep omission of the round-1 repair.

**AR2-02 (LOW, consistency) — contract header owner list drops one of three owned elements.**
`contracts/accumulation.contract.md` L4 declares the manifest owns "the promotion procedure and generality criterion" but omits the `**来源**` traceability shape that A-22, FR-004 and data-model's owner statement/E8 assign to the same owner. C-303 states the shape but names no owner in that file, so the contract face makes the shape appear ownerless while three sibling artifacts list all three elements.

## 4. Residue table (round-1 MEDIUM/LOW carried to round 2)

| ID | Sev | Status | Disposition | One-line claim |
|---|---|---|---|---|
| AR1-04 | MEDIUM | open | deferred | Manifest must point at a spec-local contract path `specify init` never distributes — downstream dangling pointer (C-104(b)/T005 unchanged). |
| AR1-05 | MEDIUM | open | deferred | Second-mechanism detection still has five phrasings; C-304 (exact names) vs C-404(d) (wildcard) and T004/T010 (wildcard) still disagree. |
| AR1-06 | MEDIUM | open | deferred | Containment residual predicate (A-20 sentence / GATE-7 / T019) still omits the per-entry qualifier C-406 carries. |
| AR1-07 | LOW | open | deferred | Map-row adjacency and two Notes elements remain unverified while leg (e) asserts only the two-token pair. |
| AR1-08 | LOW | open | deferred | Seed `**来源**` still splits three ways (exempt / must be absent / no fabricated line). |
| AR1-09 | LOW | open | deferred | A-15 module-wide sole table vs FR-001/C-103/INV-03 manifest-only check. |
| AR1-10 | LOW | open | deferred | Six guard-pinned literals remain outside Shared Strings (7 rows); no drift today. |
| AR1-11 | LOW | open | deferred | `同一变更` still has no referent definition (11 occurrences). |
| AR1-12 | LOW | closed | rejected | Init-drill CLI form is resolved downstream in tasks § Environment Prerequisites; no defect remains. |

None of these was touched by the round-1 repair; each was re-verified against the current tree before being carried (`deferred` = open, driver owns routing). AR1-12 is closed as no-defect because the tasks stage fixes source-run and forbids the installed CLI without contradicting SC-004/A-18.

## 5. Mechanical readings (repaired tree)

| Reading | Command | Result |
|---|---|---|
| Requirements validator | `validate-requirements.py requirements.md` | `status ok`, **0 error / 0 warning**, 229 lines, 16 definition rows, 7 shared strings ([`analyze-round2-requirements-validator.txt`](./analyze-round2-requirements-validator.txt)) |
| Tasks validator | `validate-tasks.py tasks.md` | **PASS**, 0 error / 0 warning ([`analyze-round2-tasks-validator.txt`](./analyze-round2-tasks-validator.txt)) |
| Definition counts | greps | **9 FR / 7 SC (+7 Source rows) / 24 A / 3 US / 3 RS / 7 STR / 9 scenarios** |
| Contract clauses | `grep -cE '^\*\*C-[0-9]{3}\*\*'` | **24** (manifest 6 / entry-shape 5 / accumulation 6 / distribution-guard 7) |
| Tasks | `grep -cE '^- \[ \] T[0-9]+'` | **20** (T001…T019 + T007A) |
| Green partition | `[green: …]` | **24 real tags, 24 unique**, each clause claimed once (T008 8 / T010 9 / T013 2 / T015 3 / T019 2) |
| Clause coverage / pre-analyze | reused `analyze-repair-pre-analyze.json` (`b5a8867c…`) | `decision=pass`, errors 0, tasks 20, clauses 24, advisories 150 (expected pre-implementation missing-path / external-clause class) |
| Workspace | `git for-each-ref \| wc -l`; `git status --porcelain` | refs **215** (unchanged since the repair-stage reading); working tree carries only this round's produced files |

## 6. Constitution check (delta only)

- **Principle XIV (One Source of Truth): the plan's pass is now supported** — the accumulated-rules ownership chain is single-owned (A-22) and every other site is a pointer or a design face. AR2-02's header omission is a completeness nit in one design face, not a second owner.
- No other constitution row's basis changed; the round-1 verification (23 rows match constitution v1.20.0) is reused, with row XIV re-derived above.

## 7. Containment reading (this round)

- Produced by this round: [`analyze-round2-findings.jsonl`](./analyze-round2-findings.jsonl), this report, [`analyze-round2-requirements-validator.txt`](./analyze-round2-requirements-validator.txt), [`analyze-round2-tasks-validator.txt`](./analyze-round2-tasks-validator.txt) — all under `.specify/specs/111-general-best-practices/**` — plus two per-entry accounting records: `.specify/feedback/20261127T082900Z-speckit-analyze.md` and `.specify/session/20261127T082842Z-run-determination-speckit-analyze-r20261127t074400z-111a-ana.md`. Both carry the feature key `111-general-best-practices` in frontmatter.
- **In-passing correction (disclosed)**: the first exec-quant collect wrote a record whose body carries only the round-specific run id — the exec-quant schema has no feature field — so it could not satisfy FR-009/A-20's residual predicate (feature key or line run id). The engine dedupes on `(unit_id, run_id)` and reported the line-run record as a duplicate, so no predicate-passing round-2 entry can exist. The non-conforming self-created record was removed; the line's exec-quant entry remains round 1's `20261127T081331351003Z-14a31158.json` on the line run id. No other store was touched; no aggregate/index file was rewritten.
- **External refs drift**: refs count is 215, identical to the repair-stage reading; no new drift appeared this round. The previously attributed parallel-line drift (refs/heads/109 removed, refs/heads/112 added) is pre-existing and not caused by this line.
- No product write, no spine/registry edit, no push, no main-tree touch.

## 8. Limits of this round

- No implementation exists (module, mirror, guard all absent), so every guard-leg adjudication is design-level; red-first remains a plan premise.
- Residues were re-verified by text against the current tree, not re-derived; their disposition stays with the driver.
- AR2-01's severity is set by the US2 Checkpoint locus (a verdict surface); the five other loci are descriptive.
- The exec-quant correction is disclosed above; the round-specific accounting remains in the feedback and session stores.

## 9. Disposition routing (recommendation only — the driver owns the verdict)

1. **Repair-in-stage before implement**: AR2-01 (sweep the eight summary/checkpoint lines; the US2 Checkpoint first), AR2-02 (add the 来源 shape to the contract header).
2. **Decision-class**: AR1-04 (inline shape vs spec pointer), AR1-07 (add checks vs producer guidance), AR1-08 (seed source-line reading).
3. **Wording alignment**: AR1-05, AR1-06, AR1-09, AR1-10, AR1-11.
4. **No action**: AR1-12 (closed downstream); the round-1 fixed set needs no reopen.

## 10. Wrap-up pointers

- Findings: [`test-evidence/analyze-round2-findings.jsonl`](./analyze-round2-findings.jsonl) (14 records).
- This report: `test-evidence/analyze-round2-report.md`.
- Validator evidence: [`analyze-round2-requirements-validator.txt`](./analyze-round2-requirements-validator.txt), [`analyze-round2-tasks-validator.txt`](./analyze-round2-tasks-validator.txt).
- Accounting (per-entry): `feedback-utils --action record` for `/speckit.analyze` run `r20261127T074400Z-111a-analyze-r2`; `run-determination --action determine` (session); exec-quant line entry unchanged (see §7).

**Anomaly line**: `未发现异常` (the one in-passing correction is disclosed in §7).