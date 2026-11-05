# Pre-change measurements — 084 Harness 三重结构

**Task**: `tasks.md` T001 · **Captured at**: implement start, branch `084-harness-triple-structure`,
HEAD `9657885fe2731d216e21e4d5d607fe47d7f36a07` (short `9657885f`) · **Date**: 2026-11-05

**What this file is**: the frozen comparison values every later "it used to read X" and "no **NEW** drift"
claim is measured against. Every block below carries the command that produced it and that command's
real output. These are **readings, not pass marks**: an empty result later is only meaningful against the
value recorded here. Nothing here is inherited from `research.md` or `plan.md` — both were re-measured on
this tree for this file.

**Toolchain readings taken in the same pass** (the EP-001 premise re-read, not inherited):

```
$ python3 --version
Python 3.11.13
$ python3 -m pytest --version
pytest 9.2.0
```

---

## (a) Mirror baseline — `sync-mirrors.py --check`

```
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (62 files)
exit code: 0
```

Frozen values: six pairs `ok`; per-pair counts `templates` 22 · `skills/external` 409 ·
`skills/internal` 138 · `agents` 3 · `scripts` 119 · `shared` 62. This is the drift baseline § Mirror
Obligations of `plan.md` refers to; the criterion at closure is "no **NEW** drift on the pairs this
feature touches", never a bare "all green".

## (b) The nine batch-1 constants, `file:line`

```
$ grep -n "DEFAULT_THRESHOLD\|SEVEN_STATES\|LANE_NAMES\|CLASS_VALUES\|BASIS_VALUES\|FLOW_TYPE_VALUES\|REQUIRED_LEDGER_COLUMNS\|NEUTRAL_CATEGORIES\|PATH_VALUES" scripts/python/*.py
scripts/python/evidence-utils.py:23:SEVEN_STATES = (
scripts/python/evidence-utils.py:27:LANE_NAMES = ("session", "project", "assets", "runs", "feedback")
scripts/python/evidence-utils.py:526:    requested = LANE_NAMES if args.lanes in (None, "", "all") else tuple(
scripts/python/evidence-utils.py:529:        if lane not in LANE_NAMES:
scripts/python/evidence-utils.py:544:    for lane in LANE_NAMES:
scripts/python/feedback-utils.py:93:DEFAULT_THRESHOLD = 10
scripts/python/feedback-utils.py:163:    return DEFAULT_THRESHOLD
scripts/python/feedback-utils.py:440:                      else DEFAULT_THRESHOLD),
scripts/python/flow-class-check.py:96:CLASS_VALUES = (EXECUTION, EXPRESSION)
scripts/python/flow-class-check.py:97:BASIS_VALUES = ("behavior-oracle", "reader-oracle", "mixed-oracle")
scripts/python/flow-class-check.py:99:NEUTRAL_CATEGORIES = ("memory", "feedback", "evidence", "session")
scripts/python/flow-class-check.py:120:REQUIRED_LEDGER_COLUMNS = ("unit_id", CLASS_KEY, "basis", "neutral")
scripts/python/flow-class-check.py:320:        if record.get("category", "") not in NEUTRAL_CATEGORIES:
scripts/python/flow-class-check.py:354:    missing_columns = [c for c in REQUIRED_LEDGER_COLUMNS if c not in names]
scripts/python/flow-class-check.py:421:    if record.get("basis", "").strip() not in BASIS_VALUES:
scripts/python/flow-class-check.py:424:            BASIS_VALUES,
scripts/python/flow-class-check.py:530:        if row[CLASS_KEY] not in CLASS_VALUES:
scripts/python/flow-class-check.py:536:                    % (CLASS_KEY, row[CLASS_KEY], CLASS_VALUES),
scripts/python/flow-class-check.py:559:        values = {row[CLASS_KEY] for row in group if row[CLASS_KEY] in CLASS_VALUES}
scripts/python/flow-class-check.py:826:    value outside ``CLASS_VALUES``, a duplicated row, or two rows that disagree.
scripts/python/flow-class-check.py:882:FLOW_TYPE_VALUES = (
scripts/python/flow-class-check.py:1032:        if match.group(1) not in CLASS_VALUES:
scripts/python/flow-class-check.py:1038:                "reason": "outside the closed set (%s)" % ", ".join(CLASS_VALUES),
scripts/python/flow-class-check.py:1108:        if value not in FLOW_TYPE_VALUES:
scripts/python/flow-class-check.py:1114:                "reason": "outside the closed set (%s)" % ", ".join(FLOW_TYPE_VALUES),
scripts/python/flow-class-check.py:1322:    if row[CLASS_KEY] not in CLASS_VALUES:
scripts/python/flow-class-check.py:1327:            % (unit_id, row[CLASS_KEY], CLASS_VALUES),
scripts/python/flow-class-check.py:2161:        if row[CLASS_KEY] in CLASS_VALUES:
scripts/python/validate-requirements.py:98:PATH_VALUES = ("final", "supporting")
scripts/python/validate-requirements.py:346:        if value not in PATH_VALUES:
exit code: 0
```

Frozen values: **30 hits total** — and, as `tasks.md` warns, the number to compare against is the
**definition set (9)**, not the hit count (30 = 9 definition lines + 21 usage sites). The nine
definitions:

| # | constant | `file:line` |
|---|----------|-------------|
| 1 | `DEFAULT_THRESHOLD` | `scripts/python/feedback-utils.py:93` |
| 2 | `SEVEN_STATES` | `scripts/python/evidence-utils.py:23` |
| 3 | `LANE_NAMES` | `scripts/python/evidence-utils.py:27` |
| 4 | `CLASS_VALUES` | `scripts/python/flow-class-check.py:96` |
| 5 | `BASIS_VALUES` | `scripts/python/flow-class-check.py:97` |
| 6 | `FLOW_TYPE_VALUES` | `scripts/python/flow-class-check.py:882` |
| 7 | `REQUIRED_LEDGER_COLUMNS` | `scripts/python/flow-class-check.py:120` |
| 8 | `NEUTRAL_CATEGORIES` | `scripts/python/flow-class-check.py:99` |
| 9 | `PATH_VALUES` | `scripts/python/validate-requirements.py:98` |

**(b′) supplementary reading — the ninth row's second copy.** Not one of the nine named constants, but
part of the same batch-1 row (`contracts/migration-batches.contract.md` C-042 row 9 names **both**
engines), so it is measured here rather than trusted from the plan:

```
$ grep -n 'final", "supporting"' scripts/python/closure-acceptance-check.py
505:        if value not in ("final", "supporting"):
exit code: 0
```

Frozen value: `scripts/python/closure-acceptance-check.py:505` holds an inline tuple, i.e. the value
domain exists twice on the tree today. T013 deletes both inline copies; this line number is where the
second one stands at implement start.

## (c) Candidate-surface counts

```
$ ls templates/commands/*.md | wc -l
27
$ ls skills/external/*/SKILL.md skills/internal/*/SKILL.md | wc -l
53
$ ls shared/workflow/*.md | wc -l
19
$ ls shared/definitions/*.md | wc -l
12
```

Frozen values: command templates **27** · `SKILL.md` carriers **53** · workflow documents **19** ·
definition documents **12**. The first three are the screen's three carrier surfaces
(`contracts/harness-triple-check.contract.md` C-030); `shared/definitions/*.md` is counted so the
"definitions are **not** units" clause can be read as a delta, not as an absence. `27 + 53 + 19 = 99`,
the candidate-surface size `plan.md` § Technical Context quotes.

## (d) 081's accepted surface — zero diff and the two collect counts

```
$ git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py
(empty output)
exit code: 0

$ python3 -m pytest --collect-only -q tests/contract/test_requirements_checker.py
40 tests collected in 0.03s
$ python3 -m pytest --collect-only -q tests/contract/test_checker_form.py
37 tests collected in 0.03s
```

Frozen values: **zero diff** against `4b65517c` on both files (A8(a)'s premise holding at implement
entry), and **40 / 37** collected tests. GATE-5 and `SC-006` compare against these three numbers.

## (e) Dependency list — the SC-006 byte-identical premise

```
$ git diff --name-only 4b65517c -- pyproject.toml
(empty output)
exit code: 0
```

Frozen value: no change to `pyproject.toml` since `4b65517c`, i.e. `dependencies` is byte-identical to
the baseline `SC-006` and `FR-009` compare against. This is the referent those two clauses name.

---

## How a later reading uses this file

| Later claim | Compared against |
|-------------|------------------|
| "no NEW mirror drift" (GATE-3, `SC-005`, T026) | § (a) — pair-by-pair, never an absolute "all ok" |
| "the constant is gone" (T013, T027(c), `DoD-4`) | § (b) definition set and § (b′) line 505 |
| "the command-template count did not move" (GATE-6, `SC-006`) | § (c) — 27 |
| "the 081 surface did not move" (GATE-5, T029) | § (d) — zero diff and 40 / 37 |
| "dependencies are byte-identical" (`SC-006`, `FR-009`) | § (e) — empty `git diff --name-only` |

A count that moved is reported as a moved count. No value in this file is a target: they are the state
of the tree before this feature touched it.
