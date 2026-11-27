# Analyze Repair — Round 1: 112-decision-batch-panel

**Line**: `decision-batch-panel` · **Run**: `r20261127T081500Z-112a` · **Stage**: `analyze-repair` · **Baseline**: `087b1c631`
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel` (branch `112-decision-batch-panel`)
**Input findings**: `test-evidence/analyze-round1-findings.jsonl` (0 CRITICAL / 2 HIGH / 6 MEDIUM / 8 LOW) and `test-evidence/analyze-round1-report.md`
**Scope**: resolve exactly the two HIGH findings (I-01, I-02) at their owner surfaces and align every cited locus; no other finding was re-graded, fixed or closed. This record reports the edits and the deterministic gates run here — it is not a new analyze verdict; a re-run of `/speckit.analyze` remains the verification authority.

## Verdict

- **I-01 resolved** — the unqualified "distinct batch ids MUST NOT read or modify each other's records" is now a three-part boundary: writes isolated, in-flight state not depended on, reads of settled records permitted only for four declared read-only purposes (already-resolved join, grounding, prior-decision conflict, replay pointer resolution).
- **I-02 resolved** — option (a) adopted: the `superseded_by` single-field append is the sole sanctioned post-write mutation of a batch record (append-only; every pre-existing byte unchanged), named as the bounded exception in FR-032, FR-037, C-502, C-503 and C-507, and stated as the rule in C-510.
- **No contract weakened**: both repairs add scope precision and one bounded exception; no FR/SC id, closure, or count changed (45 FR / 10 SC / 54 contract clauses / 58 task rows before and after; assumptions 25 → 27).

## Adjudications (recorded in `requirements.md` § Assumptions & Decisions)

| ID | Decision | Why |
|----|----------|-----|
| **A-26** | Cross-batch access boundary — **write isolation + declared read exits**. Writes: distinct knowledge paths; a batch MUST NOT write/modify/delete another batch's records (sole exception = A-27); no dependence on another batch's in-flight state. Reads of a settled prior batch record are permitted only for the declared read-only purposes — already-resolved exclusion (FR-012), grounding (FR-022, whose carrier set includes batch records), prior-decision conflict detection (FR-023) and replay pointer resolution (FR-036) — and MUST be read-only. | The isolation intent (requirements edge case 「两个并发批次」) is concurrent-write safety; the four read paths are the recorded design. The unqualified wording merged audit reads with write isolation. |
| **A-27** | Redecision recording form — **option (a): the declared single-field append**. A batch-produced prior record lives inside its batch record; the redecision appends the conditional field `superseded_by` (with the new record's carrier pointer) at that record, leaving every pre-existing byte unchanged. That append is the batch record's sole sanctioned post-write mutation and the named, bounded exception to FR-032 「永不覆盖」, FR-037 「MUST NOT 修改他批记录」 and the whole-file immutability of C-502/C-503/C-507; it is not a same-batch-id second batch record. Forms (b) reverse pointer in the new record and (c) supersession sidecar were rejected: (b) would fork the 107 supersession rule into a second form, (c) would create a second store (FR-004/A-17). An unreadable/unwritable prior carrier still refuses the redecision (A-7). | Keeps the single 107 supersession rule; the exception is minimal and machine-decidable (one extra conditional field, zero byte changes); not appending would break the supersession chain, which falsifies (b) as a substitute. |

## Finding → resolution → files changed

### I-01 — batch isolation vs prior-batch read (HIGH)

**Resolution**: FR-037 and C-507 were rewritten from an unqualified mutual-read prohibition into the A-26 boundary. FR-012 and C-107 now name the already-resolved join as one of the permitted read-only cross-batch joins. The concurrency edge case was restated with the same boundary. Data-model E-9 states the read side for batch records; research D-7 records it in the record-transaction design. The engine test row T033 now names the read-side assertion alongside the write isolation.

**Files changed**:
- `requirements.md` — A-7 (pointer), A-26 (new), FR-012, FR-037, edge case 「两个并发批次」; header references A-1…A-27 in `plan.md`, `tasks.md`, `feature-ref.md`, `research.md`
- `contracts/source-roster.contract.md` — C-107
- `contracts/record-replay.contract.md` — C-507
- `data-model.md` — E-9 Batch Record
- `research.md` — D-7
- `tasks.md` — T033 (test description)

### I-02 — supersession write-back vs batch immutability (HIGH)

**Resolution**: option (a) recorded as A-27. FR-029 now states the append's effect on a batch-produced old record is the file's sole sanctioned post-write mutation; FR-032 「永不覆盖」 carries the single-field exception; FR-037's prohibition carries the same exception; C-502/C-503/C-507 carry it; C-510 states it as the rule; data-model I-16/I-18 and E-9 plus the `record` operation were aligned; research D-8 records the choice and the rejected alternatives; plan PA4 and the blast-radius rationale now include the append in the write surface; task T050 names the batch-record case in implementation.

**Files changed**:
- `requirements.md` — A-7, A-11 (pointer), A-27 (new), FR-029, FR-032, FR-037
- `contracts/record-replay.contract.md` — C-502, C-503, C-507, C-510
- `data-model.md` — E-9, § 4 `record` operation, I-16, I-18
- `research.md` — D-8
- `plan.md` — PA4, Decision Tensions blast-radius bullet
- `tasks.md` — T050 (implementation description)

## Alignment matrix (post-edit anchors)

| Locus | Anchor (after edit) | What it now says |
|-------|---------------------|------------------|
| Assumptions | `requirements.md:77` A-26, `:78` A-27 | The two adjudications above |
| A-7 / A-11 | `requirements.md:58`, `:62` | Pointer to A-27; 「永不覆盖——唯一例外见 A-27」 |
| FR-012 | `requirements.md:279` | The read-time join is a FR-037/A-26 permitted read |
| FR-029 | `requirements.md:305` | Append leaves bytes unchanged; batch-produced old record covered by A-27 |
| FR-032 | `requirements.md:311` | 「永不覆盖」 with the single-field A-27 exception |
| FR-037 | `requirements.md:316` | A-26 boundary: write isolation, no in-flight dependence, four read purposes, read-only |
| Edge case | `requirements.md:246` | Same boundary restated for two concurrent batches |
| C-107 | `contracts/source-roster.contract.md:17` | Join named as the C-507-permitted read; cites A-26 |
| C-502 / C-503 | `contracts/record-replay.contract.md:12`, `:13` | Create-only with the C-510 single-field append exception |
| C-507 | `contracts/record-replay.contract.md:17` | A-26 boundary with the four read purposes (C-107/C-303/C-306/C-508) |
| C-510 | `contracts/record-replay.contract.md:20` | Append is the batch record's sole sanctioned post-write mutation; cites A-27 |
| Data model | `data-model.md:113` (E-9), `:190` (record op), `:212` (I-16), `:214` (I-18) | Immutability + single exception; read purposes; supersession step in the operation order |
| Research | `research.md:42` (D-7), `:44` (D-8) | Read purposes + in-flight rule; append carve-out + rejected forms |
| Plan | `plan.md:32` (PA4), `:84` (blast radius) | Create-only exception; write surface includes the sanctioned append |
| Tasks | `tasks.md:278` (T033), `:330` (T050) | Read-side test assertion; batch-record append case in implementation |

**Verification of the original contradiction**: FR-012's join is now explicitly within FR-037's permitted reads, so no later batch is simultaneously mandated and forbidden to read a settled identity. FR-029's append is now explicitly FR-032/FR-037's single named exception, so redeciding a batch-produced decision is no longer simultaneously mandated and forbidden. SC-006 and SC-010 assertions are unchanged and remain satisfiable (SC-010 speaks of two concurrent batches, whose mutual non-modification stays absolute; the append is a later batch's action on a settled record).

## Deterministic gates run this stage

| Check | Command | Result | Capture |
|-------|---------|--------|---------|
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/112-decision-batch-panel/requirements.md` | status ok — 439 lines / 55 definition rows / 15 shared strings / 0 error / 0 warning, rc 0 | `test-evidence/analyze-repair-validate-requirements.txt` |
| Pre-analyze gate (tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/112-decision-batch-panel --stage tasks --repo .` | `decision=pass`, errors=0, advisories=77 (all `missing-path` deliverables — the same 77 of the analyze round), fr=45 sc=10 tasks=58 clauses=54 | `test-evidence/analyze-repair-pre-analyze-tasks.json` / `.txt` |
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/112-decision-batch-panel/tasks.md` | PASS — 0 error / 0 warning, rc 0 | `test-evidence/analyze-repair-validate-tasks.txt` |
| Decision tensions (side check after the plan edit) | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/112-decision-batch-panel --json` | status ok, 0 errors / 0 warnings, 0 records, six labels pass, rc 0 | quoted in this record |
| Workspace signature (pre-commit) | `python3 scripts/python/workspace-guard.py --check .specify/specs/112-decision-batch-panel/test-evidence/workspace-analyze.json --repo . --json` | `{"status": "clean", "changed": []}`, rc 0 — branch `112-decision-batch-panel`; no refs/specs drift vs the analyze-stage snapshot | `test-evidence/workspace-analyze-repair-readings.txt` |

Stage-order note: the snapshot/self-check pair for the post-commit state is captured in the wrap-up commit (same pattern as the analyze stage: artifact commit → wrap-up records commit).

## Concurrency record

`requested=1` · `effective=not_evaluated` · `effective_reason=single-unit` — the executor role forbids dispatching, and this repair is one serial work package (one owner surface set, one gate set).

## Anomalies

未发现异常. No in-passing repair was needed; no unexpected state was found. The analyze-stage readings had attributed sibling-line refs drift (line 111 branch removal, `master` advance) that was already clean at the analyze snapshot; this repair's pre-commit check matched that snapshot exactly, so there is no new concurrent drift to attribute.

## Limits

- I-03…F-01 (14 findings) remain open and untouched; G-01 (`coverage-baseline.txt` absent) still prevents the clause-delta lane from judging — this repair does not freeze a baseline.
- The quality checklist `checklists/requirements-quality-2026-11-27.md` was not rewritten (dated instrument): its CHK005/CHK025/CHK036 questions about these two rules now resolve against A-26/A-27 and the aligned clauses; the checklist entries themselves stay as raised.
- No owner-page, engine, test or mirror edit: this stage is spec-design repair; the owner page extension is implementation work (T007/T015…T018/T028/T034/T035/T041/T048).