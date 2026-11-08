# checklist stage — status record for 089-script-interface-contract

Recorded 2026-11-06 on branch `089-script-interface-contract` (HEAD `408b5555`, base of this stage). This file is
the checklist-stage evidence pointer: it names the artifact produced, the self-checks that were actually run, and
the anomaly lines this stage refuses to repair itself.

## Artifacts produced this stage

| Artifact | Path | State |
|----------|------|-------|
| Requirements-quality checklist (this round) | `.specify/specs/089-script-interface-contract/checklists/contract-integrity-2026-11-06.md` | written, 60 items CHK001…CHK060, dense ids |
| Self-check output | `test-evidence/checklist-selfcheck.txt` | 60 items · traceability 60/60 · 0 prohibited openers · ids dense |
| Flow-class lookup (single read for the stage) | `test-evidence/checklist-flow-class.txt` | `flow_class: execution` · `source: declaration` · exit 0 |
| This status record | `test-evidence/checklist-stage-status.md` | written |
| Prior checklist (untouched) | `checklists/requirements.md` | byte-identical to the pre-stage copy (verified by `diff -q`) |

## Measured counts

- Items: **60** (`grep -c '^- \[ \] CHK'`), ids dense `CHK001`…`CHK060` in document order (asserted by the self-check).
- Traceability: **60 / 60** items carry at least one of `FR-…`, `SC-…`, `C-…`, `F-…`, `A…`, `Q…`, `US…`
  (methodology floor 80 %).
- Category distribution: Measurability 12 · Completeness 8 · Conflict 7 · Edge Case 6 · Traceability 6 ·
  Ambiguity 5 · Coverage 5 · Non-functional 5 · Consistency 4 · Clarity 2.
- Soft cap: 60 > 40. Declared in the file's § Notes with the axis-based justification (second round over the
  same requirement set; the first is `checklists/requirements.md`).
- Requirement structures re-measured this stage: 31 FR · 12 SC · 7 US · 10 edge cases · 10 assumptions · 9 clarify
  rulings — all equal to the stage brief's premise, so no premise correction was needed.

## Baseline re-derived this stage (not carried forward)

- Candidates: 737 = 71 `.sh` + 666 `.py`; work-tree walk also 737. Root split `tests/` 449 · `.specify/` 146 ·
  `skills/` 87 · `scripts/` 51 · `src/` 3 · `install.sh` 1.
- `skills/external/*/` skills declaring `classification: external`: **16 of 16**, carrying **72** `.sh`/`.py`
  files.
- `skills/internal/*/` declaring `internal` and carrying scripts: 5.
- Instruction top-level sections: template **34** · live **34** today; C-28's pins target 34 / 35.
- `manage-constitution` mandate entries: 11 today (`COMMAND_COUNT = 11` in the double-landing test); C-28 targets 12.

## Gates run

1. `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:089-script-interface-contract"` → exit **0**, `flow_class: execution`, `source: declaration`, `marker: null`, `neutral: false`.
   The stage's gate set is therefore the unchanged one (no expression-class operator rows apply).
2. Checklist self-check (`test-evidence/checklist-selfcheck.txt`): item count, dense ids, traceability ratio,
   prohibited-opener scan, category tally, and agreement between the § Notes claims and the measured values.
3. `diff -q checklists/requirements.md <pre-stage copy>` → identical; the existing checklist was not refreshed.

No deterministic requirements validator was run: `validate-requirements.py` judges `requirements.md`, which this
stage neither reads as an edit target nor writes.

## Same-author gate

`.specify/shared/workflow/objective-analysis-gate.md` fires on the requirement set (authored in earlier stages of
this same feature run). Detection was **not** delegated to fresh-context subagents, because this worker's
operating contract forbids dispatching agents. Every item therefore records the weaker evidence path
`(detected: direct read, delegation unavailable)` in § Notes, per that owner's § "Subagent-unavailable fallback".
The downgrade rate is not measurable on this path; the next round that can dispatch detectors SHOULD re-derive
CHK021…CHK032 (requirement ↔ plan/contract agreement), where drift concentrates.

## Open points handed forward

- The requirement text was **not** edited by this stage. Every contradiction the checklist names (CHK021–CHK032)
  is recorded for a recheck round or a requirements revision, not repaired here.
- All anomaly lines below belong to the upstream artifacts; each is a decision for the driver, not a repair this
  worker may perform.

### Anomalies surfaced (not repaired here)

- `ANOMALY` **scope of checklist requirement vs repository convention**: the stage brief forbids overwriting
  `checklists/requirements.md`, and the create-checklist skill says each run creates a NEW file, but the repo's
  own convention is a single `requirements.md` per feature (119 tracked `checklists/` files; `requirements.md` is
  the conventional name). A second, differently-named checklist now coexists with it, and no pointer from
  `requirements.md` to the new file was added (that file is the earlier stage's record). A convention decision is
  the driver's.
- `ANOMALY` **`plan.md` internal citation drift**: `plan.md` § Constitution Check rows III / VIII / XVI cite
  `PLAN-EDIT F-1…F-4`, but the actual follow-up table lives in `feature-ref.md` § 7 and carries **F-1…F-7**; VIII
  also says "three requirements readings" while the row lists four. Recorded, not repaired.
- `ANOMALY` **stale requirement counts**: `requirements.md` A10 / Q8 / A2 record `scripts/python/` as 38 files while
  the tree holds 37, and 207 `__main__`-carrying `.py` while tasks measures 208; both are already disclosed as
  F-1 / F-2 but the requirement text itself still carries the old readings.
  **Correction (2026-11-06, analyze round 1 repair, commit `5c2bb98f`)**: the requirement text now reads 37 files
  (35 `argparse` + 2 self-parsing) and 207 / 459 `__main__`; the per-file re-measurement gives 207 carrying and 459
  not, so "tasks measures 208" was this record's misreading of `plan.md`'s then-stale figure — `plan.md` now reads
  207 / 459 as well. This anomaly is closed.
- `ANOMALY` **constitution and instruction count vectors move independently**: `manage-constitution` carries 11
  mandate entries against a template roster of 18 / live roster of 19 today, and C-28 moves them to 12 / 19 / 20.
  FR-014 and SC-006 say "生成器清单条目数与两侧宪法的原则条目数一致", which is false today and would still be
  false after the landing under any literal reading. Recorded as CHK031; the interpretation is the driver's.
- `ANOMALY` **A6 / Q6 / Edge Case still disagree after the clarify correction**: A6 and the Edge Case
  「上游来源判定」 read `external`; Q6's body still reads "声明 `classification: internal`" with the correction
  only in a trailing note. Measured this stage: all 16 `skills/external/*/` skills declare `external`.
- `ANOMALY` **the stage brief and `plan.md` carry a stale instruction-section count**: both cite template 32
  / live 33 with `TPL_EXPECTED = 33` / `LIVE_EXPECTED = 34`; measured this stage both files read **34** and the pins
  read **34** / **35**. Recorded with the measured values in the checklist's baseline table; the checklist's
  questions are unaffected (CHK031 tests the mandate/roster vectors, not the section pins).
  **Correction (2026-11-06)**: re-measured with the pinned command `grep -c '^## '` →
  `templates/instructions-template.md` = **32**, `.specify/instructions.md` = **33**, and the pins in
  `tests/contract/test_fast_fail_discipline.py` (lines 747–748) read `TPL_EXPECTED = 32` /
  `LIVE_EXPECTED = 33`. The "34 / 34 / 35" figures above are not reproducible with that command on this tree, so
  `plan.md`'s 32/33 → 33/34 is **correct** and this anomaly is withdrawn.
