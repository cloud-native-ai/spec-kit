# Spec repair — 078-coaching-skills

**Date**: 2026-11-10
**Spec**: `.specify/specs/078-coaching-skills/` (live; not archived)
**Sources**
- Prior audit: `spec-audit-live-batch-4.md` § 078-coaching-skills — 122 refs, verdict
  INTACT at audit time (4 moved anchor refs, 0 dead).
- Deterministic settled scan: `spec-audit-settled.json` →
  `.specify/specs/078-coaching-skills`: `refs 160 / alive 133 / moved 133 / dead 27`;
  `dead_list` carries **20 unique paths** (the scan's `dead` count counts repeat
  occurrences). This repair works the `dead_list` set.
- Anchor layout (post-`6fb8093c4`): `.specify/{features,constitution,glossary,register,tools}.md`
  and `.specify/features/<NNN>-<slug>.md` all exist and resolve.

## Counts

| bucket | unique dead paths | notes |
|---|---:|---|
| **dead total** | **20** | settled scan flags 27 references; `dead_list` dedupes to 20 |
| **live-fixed** | **0** | no `dead_list` entry is a live normative pointer; all are dated records or non-references |
| **dated-kept** | **18** | left byte-identical (past-run records, transient tmp paths, absence/removal records) |
| **non-reference** | **2** | glob token over live files; fixture-example symlink |

**Additional (outside `dead_list`)**: 9 **moved-anchor live pointers** repaired across 5 files
(before → after table below). These were counted `moved`, not `dead`, by the settled scan.

## Per-entry disposition (all 20 `dead_list` paths)

Occurrence lists give the exact line sites in the current tree; `→ unchanged` means the text
was intentionally not rewritten.

| # | dead path | occurrences | disposition |
|---:|---|---|---|
| 1 | `skills/external/think-skills/` | `notes/pre-change-measurements.md:37,38,90,91`; `plan.md:107,135`; `tasks.md:79,164`; `test-evidence/implement-part3-targeted.txt:137,138`; `test-evidence/stage-plan-baselines.txt:26,27,129` | **dated-kept** — pre-change measurement readings, the plan's REMOVED change row, and completed T001/T004 baseline rows → unchanged |
| 2 | `skills/external/think-skills/SKILL.md` | `notes/pre-change-measurements.md:37,90,91`; `tasks.md:79,164`; `test-evidence/implement-part3-targeted.txt:137,138`; `test-evidence/stage-plan-baselines.txt:26,129` | **dated-kept** — same measurement/baseline records → unchanged |
| 3 | `skills/external/think-skills/references/prompt-templates.md` | `notes/pre-change-measurements.md:38`; `test-evidence/stage-plan-baselines.txt:27` | **dated-kept** — `git grep -c` baseline output → unchanged |
| 4 | `.specify/.tmp/coaching-078/run1-work/work.md` | `notes/quickstart-run.md:121` | **dated-kept** — transient scratch from the recorded run → unchanged |
| 5 | `.specify/skills/think-skills/references/prompt-templates.md` | `notes/pre-change-measurements.md:30` | **dated-kept** — pre-change grep baseline → unchanged |
| 6 | `.specify/.tmp/coaching-078/run1-work/checklist.md` | `notes/quickstart-run.md:145` | **dated-kept** — transient scratch from the recorded run → unchanged |
| 7 | `skills/internal/improve-skills/SKILL.md` | `notes/quickstart-run.md:191`; `test-evidence/sc005-degraded.txt:6` | **dated-kept** — `absent:` lines of the degraded-fixture run (absence is the finding) → unchanged |
| 8 | `.specify/skills/think-skills-alias` | `quickstart.md:161,164` | **non-reference** — user-authored symlink inside a disposable fixture project (scenario 3 example) → unchanged |
| 9 | `.specify/memory/coaching/20261030T101500Z-memory-recall` | `quickstart.md:205,207` | **dated-kept** — scenario-5 teardown of one dated acceptance run → unchanged |
| 10 | `.specify/skills/think-skills/` | `contracts/identity-and-wiring.contract.md:35`; `notes/pre-change-measurements.md:29,30`; `plan.md:135,154`; `quickstart.md:160`; `test-evidence/implement-part3-status.txt:26`; `test-evidence/implement-part4-gates-raw.txt:7`; `test-evidence/review-repair-pre-analyze-{plan,requirements,tasks}.txt:4`; `verification.md:175` | **dated-kept** (10 sites) + **non-reference** (2 sites: contract:35 is a removal-target row; quickstart:160 is the fixture example) → all unchanged |
| 11 | `.specify/memory/coaching/.optimization-claims/fixture-trainee` | `notes/quickstart-run.md:229` | **dated-kept** — claim path readout of the recorded fixture run → unchanged |
| 12 | `.specify/templates/commands/` | `verification.md:174`; `test-evidence/implement-part4-gates-raw.txt:7`; `test-evidence/pre-analyze-check-plan-fix.txt:5,11`; `test-evidence/pre-analyze-check-plan-fix2.txt:4`; `test-evidence/pre-analyze-check-plan.txt:6,10`; `test-evidence/pre-analyze-check.txt:3`; `test-evidence/review-repair-pre-analyze-{plan,requirements,tasks}.txt:4`; `test-evidence/tasks-pre-analyze-check.txt:3` | **dated-kept** — advisory records that explicitly state the retired tree is absent (not assertions of a live path) → unchanged |
| 13 | `.specify/memory/coaching/20261030T083250Z-fixture-trainee` | `notes/quickstart-run.md:161`; `test-evidence/sc001-run-artifacts.txt:5`; `verification.md:90` | **dated-kept** — dated acceptance-run output → unchanged |
| 14 | `.specify/skills/think-skills/SKILL.md` | `notes/pre-change-measurements.md:29` | **dated-kept** — pre-change grep baseline → unchanged |
| 15 | `.specify/.tmp/coaching-degraded/.specify/memory/coaching/20261030T083352Z-fixture-trainee` | `notes/quickstart-run.md:199`; `test-evidence/sc005-degraded.txt:11` | **dated-kept** — transient degraded-fixture scratch → unchanged |
| 16 | `tests/contract/test_coaching_` | glob token from `checklists/requirements.md:37` (`test_coaching_*`); brace/glob forms at `review.md:377`, `test-evidence/review-repair-status.txt:4`, `test-evidence/review-repair-targeted-raw.txt:2`, `test-evidence/implement-part3-status.txt:39` | **non-reference** — glob/brace expression; all six targets exist (`tests/contract/test_coaching_{run,expectation,observation,dispatch,wiring,reporting_duty}` → live files) → unchanged |
| 17 | `.specify/skills/internal/improve-skills/SKILL.md` | `notes/quickstart-run.md:193`; `test-evidence/sc005-degraded.txt:8` | **dated-kept** — `absent:` lines of the degraded-fixture run → unchanged |
| 18 | `.specify/.tmp/coaching-078/run1-events.jsonl` | `notes/quickstart-run.md:137` | **dated-kept** — transient host-event log of the recorded run → unchanged |
| 19 | `.specify/memory/coaching/20261030T083250Z-fixture-trainee/` | `verification.md:90` | **dated-kept** — same dated run as #13 → unchanged |
| 20 | `.specify/memory/coaching/.optimization-claims/memory-recall` | `quickstart.md:206,208`; `test-evidence/plan-fix2-status.txt:18` | **dated-kept** — scenario-5 teardown / plan-fix status for the dated run → unchanged |

## Moved-anchor live pointers repaired (before → after)

These were classified `moved` by the settled scan and are live normative pointers in the
spec's current artifacts (requirements / plan / tasks / feature-ref / checklist), so they
were repaired to the anchor layout.

| file:line | before | after |
|---|---|---|
| `plan.md:17` | `.specify/memory/features.md` | `.specify/features.md` |
| `plan.md:29` | `.specify/memory/constitution.md` | `.specify/constitution.md` |
| `plan.md:34` | `.specify/memory/features/078.md` | `.specify/features/078-coaching-skills.md` |
| `tasks.md:6` | `.specify/memory/features.md` | `.specify/features.md` |
| `requirements.md:46` (A9) | `.specify/memory/features/078.md` | `.specify/features/078-coaching-skills.md` |
| `requirements.md:167` (FR-024) | `.specify/memory/features/078.md` | `.specify/features/078-coaching-skills.md` |
| `feature-ref.md:11` | `.specify/memory/features.md` | `.specify/features.md` |
| `feature-ref.md:12` | `.specify/memory/features/078.md` | `.specify/features/078-coaching-skills.md` |
| `checklists/coaching-loop-2026-10-30.md:5` | `.specify/memory/features/078.md` | `.specify/features/078-coaching-skills.md` |

**Dated anchor citations left unchanged** (recorded readings, not repaired):
`requirements.md:240` (2026-10-30 Clarifications Q/A); `review.md` (13 sites, dated review
record); `notes/residual-audit.md:135`; `test-evidence/{clarify,plan,tasks}.jsonl`,
`review-stage-status.txt`, `requirements-fix-status.txt`.

**Registry row**: not touched — `.specify/features.md` row 078 resolves
(`Implemented`, detail `.specify/features/078-coaching-skills.md`); no stale or missing row.

## Validator readings

### validate-requirements.py

```
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/078-coaching-skills/requirements.md
file: .specify/specs/078-coaching-skills/requirements.md
status: error
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] fail (9)
scanned: 251 lines, 38 definition rows, 17 shared strings
190-198: path-marker: SC-001…SC-009 carry no `**Path**` marker
9 error(s), 0 warning(s)   ; exit 1
```

**Pre-existing, not caused by this repair**: the same 9 `path-marker` errors reproduce on
the HEAD copy (`git show HEAD:.specify/specs/078-coaching-skills/requirements.md` →
`.specify/.tmp/repair-078/requirements-head.md`, same 9 errors, exit 1). The failure is
success-criterion structure (final vs supporting), not a stale reference; assigning the
split would be an invented decision, so it is reported, not fixed.

### validate-tasks.py

```
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/078-coaching-skills/tasks.md
PASS: .specify/specs/078-coaching-skills/tasks.md — 0 error(s), 0 warning(s)   ; exit 0
```

## Anomaly

ANOMALY: `validate-requirements.py` reports 9 pre-existing `path-marker` errors (SC-001…SC-009
lack `**Path**` markers), present at HEAD and unrelated to reference repair; not fixed because
the final/supporting classification is not recorded anywhere in the spec and would have to be
invented.
