# Pre-change measurements — Feature 053

**Purpose**: the frozen, re-measurable facts every gate and DoD row compares against. Captured once at implement start by RUNNING each command; a later run whose re-capture differs MUST carry the new value here (re-freeze rule, tasks.md § Environment Prerequisites).

**Capture date**: 2026-10-03 · **Captured by**: `/speckit.implement` T002

## 1. BASE SHA (GATE-6's window anchor)

```
$ git rev-parse HEAD
ad190d46de960efd70e61a4719a16561a89b7e9d
```

## 2. Confirmation-gate budget (DoD-5, GATE-6, FR-045)

```
$ python3 scripts/python/scan-confirmation-gates.py --summary
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
exit=0
```

Expected 23/13/10/0 — matches. Cap arithmetic: 93 × 0.25 = 23.25, so integer headroom is **0**.

## 3. `goal-utils.py` action roster (T031/T035 premises)

```
$ grep -c 'sub.add_parser' scripts/python/goal-utils.py
9
```

## 4. `validate-tasks.py` check-label set (T002/T019/T020 premises)

Authoritative derivation (the same one `tests/contract/test_validate_tasks_parallel_safety.py:312` uses):

```
$ python3 -c "…re.findall(r'^  ([A-Za-z][A-Za-z-]*)\s{2,}', module.__doc__, re.M)…"
['blockedBy', 'dod-format', 'id-unique', 'parallel-safe', 'row-format', 'story-labels']
count 6
```

**Trap form** (do NOT use as the label count):

```
$ grep -c 'parallel-safe' scripts/python/validate-tasks.py
3
```

The raw mention count is 3 for one label; the label set is 6. US2 grows the set 6 → 10.

## 5. Clause-form census baseline (FR-027 § 基线面, GATE-8)

Run FROM REPO ROOT — the glob is repo-root relative and a wrong cwd returns `(0, 0)` silently:

```
$ python3 - <<'CENSUS_EOF'   # command body owned by notes/clause-form-census.md
excl-053 (baseline): (110, 508)
CENSUS_EOF
```

**Premise falsified during Phase 2 (written back per implement step 5)**: the `508` above comes from the census file's *coarse whole-text* classifier, which counts an id anywhere in a file. The clause-syntax owner doc (`shared/definitions/contract-clause-definitions.md`, FR-022) declares a stricter rule — only a line-start marker or a **table first cell** declares a clause; an id elsewhere is a cross-reference. Re-derived with `scripts/python/clause_extract.py` under the owner rule:

```
excl-053 (110, 507)   ·   053 own (7, 182)   ·   all (117, 689)
```

The whole delta is **1 id**: `051-user-facing-comprehension/contracts/gate-neutrality.md` carries a `**C-13**` in a non-first table cell that cites *another* contract's clause. File counts and the six-form distribution are unchanged, so the census's form table still holds; its id literal does not. **507 supersedes 508** as the citable pre-change baseline, and the census owner file carries the same correction. GATE-8 and every downstream id count MUST use `clause_extract.py`, never the coarse command.

`(110, 507)` is the only figure safe to cite as a literal (it is the pre-change baseline and does not move with this feature's edits). The `053 own` and `all` totals are volatile and are deliberately NOT frozen here — re-derive them when needed.

## 6. Mirror pre-change DIFF name lists (GATE-2's relativity criteria)

Per-pair, exit code taken by assignment (never through a pipe):

| pair / scope | EXIT | DIFF | MISS | names |
|---|---|---|---|---|
| `scripts/python` | 2 | 1 | 0 | `.specify/scripts/python/trigger-utils.py` |
| `shared/definitions` | 0 | 0 | 0 | — |
| `shared/guidelines` | 0 | 0 | 0 | — |
| `shared/constants` | 0 | 0 | 0 | — |
| `templates/tasks-template.md` | 0 | 0 | 0 | — |
| `templates/commands` | 0 | 0 | 0 | — |
| `templates` (pair) | 2 | 2 | 0 | `.specify/templates/proactive-trigger-seed.json`, `.specify/templates/skills-template.md` |
| `skills` (pair) | 2 | 30 | 0 | the 30 names listed below |

`skills` pair, all 30 (this feature writes three files under `skills/create-team/`; **none of the three appears here**, so each is currently byte-identical to its mirror and carries an absolute criterion):

```
.specify/skills/archive-session/SKILL.md
.specify/skills/code-review/SKILL.md
.specify/skills/collect-evidence/SKILL.md
.specify/skills/create-docs/SKILL.md
.specify/skills/create-pages/SKILL.md
.specify/skills/create-team/references/operating-loops.md
.specify/skills/create-team/references/summary-mapping.md
.specify/skills/create-tools/SKILL.md
.specify/skills/database-utils/SKILL.md
.specify/skills/document-utils/SKILL.md
.specify/skills/draw-drawio/SKILL.md
.specify/skills/draw-excalidraw/SKILL.md
.specify/skills/draw-mermaid/SKILL.md
.specify/skills/draw-plantuml/SKILL.md
.specify/skills/git-fleet/SKILL.md
.specify/skills/git-server-init/SKILL.md
.specify/skills/git-submodule-edit/SKILL.md
.specify/skills/git-workflow/SKILL.md
.specify/skills/improve-agent/SKILL.md
.specify/skills/improve-docs/SKILL.md
.specify/skills/improve-skills/SKILL.md
.specify/skills/improve-skills/references/loop-playbook.md
.specify/skills/improve-tools/SKILL.md
.specify/skills/manage-agents/SKILL.md
.specify/skills/memory-recall/SKILL.md
.specify/skills/memory-record/SKILL.md
.specify/skills/merge-skills/SKILL.md
.specify/skills/study-project/SKILL.md
.specify/skills/summarize-project/SKILL.md
.specify/skills/think-skills/SKILL.md
```

Reconciliation to the whole-tree check: 30 (`skills`) + 2 (`templates`) + 1 (`scripts/python`) = **33**, matching `sync-mirrors.py --check` without `--only`.

## 7. Implement-owned test baseline (DoD-6, GATE-1)

Captured by `run-tests.sh --names-out .specify/specs/053-machine-decidable-artifacts/baseline-failed.txt -q tests/` at this same instant; the name list lives in that file (names, not counts — the comparison form is `comm -13`).

```
65 failed, 2927 passed, 2 skipped, 3 warnings in 101.36s
# failed-name list written: .specify/specs/053-machine-decidable-artifacts/baseline-failed.txt (65 entries)
md5  02177c0e6e5961c880f73d932007df92   (65 lines)
```

The md5 matches `.specify/specs/052-fast-fail-principle/current-failed.txt` and this spec's `notes/clarify-current-failed.txt`, i.e. the 2026-10-03 artifact-only remediation moved no test outcome. GATE-1 compares against **this** file, never against 052's frozen baseline (which holds 76 names — a different, weaker denominator; see `research.md` F-10).
