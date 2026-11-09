# Analyze-lite verification — FR-036 amendment (independent)

**Date**: 2026-11-09 · **Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-clarify` · **Branch**: `093-concurrency-by-default`
**HEAD**: `7ec5cc05` · **Objects under verification**: `b337e94d` (amendment) + `b9edf99f` (spine)
**Mode**: read-only except this note; no edits, no commits, no push, no subagents.

## 1. Verification table

| # | Check | Reading | Verdict |
|---|---|---|---|
| 1 | FR-036 is a definition row, contiguous after FR-035 | `requirements.md:196` immediately follows FR-035 (`:194`); no FR-037; validate-requirements `[id-contiguous] pass (0)`, `[doc-order] pass (0)`, `[dup-id] pass (0)`; 48 definition rows (47 before the amendment → +1 = FR-036 counted) | PASS |
| 2 | Closed rule stated | `requirements.md:196`: 唯一入口 = `scripts/bash/run-tests.sh`（缺省 `-n <effective> --dist load`）; raw `pytest` / `python3 -m pytest` forbidden; path/arg pass-through (single-test debugging included); exemptions exactly two classes — runner internals and dated records; guard `tests/contract/test_test_entry_guard.py` with EXACT four-entry allowlist and red-first mutated-copy evidence. Runner default corroborated by `scripts/bash/run-tests.sh` (`:9` comment, `:99–100` default `--dist load` guard, `:174–175` `-n` append) | PASS |
| 3 | Clarifications quote directive + routing verdict | `requirements.md:331` session `Session 2026-11-09（amend · 用户裁定：测试入口唯一化）`; `:335` quotes the English directive verbatim and the verdict `sdd-capability-or-contract-change` @ `2026-11-09T11:14:16Z` with the owner path | PASS |
| 4 | T156–T159 exist with correct targets/obligations | `tasks.md:329–332`; T156 → `templates/instructions-template.md` + mirror + live `.specify/instructions.md` via instructions flow; T157 → `stage-prompts.md` + `dispatch-recipes.md` (only those sentences; 094 wp05 serialized); T158 → `skills/internal/implement-feature/SKILL.md` + agent definitions + measured sweep (create-skills, merge-skills `decommission-and-wiring.md`, `non-disposable-definitions.md`, `cross-cutting-lessons.md`); T159 → `tests/contract/test_test_entry_guard.py`, tracked framework artifacts, EXACT allowlist, red-first | PASS |
| 5 | Row count and Package Map | `grep -c '^- \[ \] T[0-9]'` = **159**; `first=T001 last=T159 count=159` with no gaps; partition 16+26+30+38+49 = **159 ≤ 160**; WP3-owners carries T153–T158 (30 rows, +3), WP4-tests carries T159 (38 rows, +1); write domains gained `test_test_entry_guard.py`, `instructions-template.md`, the five sweep files and `.specify/instructions.md` | PASS |
| 6 | DoD / premise counts updated in the same commit | `b337e94d` diff: DoD-1 `FR-001…FR-035`→`FR-036`; DoD-3 `nine`→`ten new contract modules plus one unit module`; Organization `ten`→`eleven test modules`; package size `155`→`159`; plan Input `35`→`36` FR, Scale/Scope `35`→`36` and `10`→`11`, Constitution row I `35/35`→`36/36`, feature-ref inventory `35`→`36` map rows, gates row `35`→`36`; feature-ref authority `36 FR / 3 dated user rulings` and 36/36 count | PASS |
| 7 | Register row | `.specify/memory/register.md:203` — `FR-036@093` grouped row, pointer shape (meaning → authority paths → `open (pending implement)`); +1 line in `b337e94d` | PASS |
| 8 | Spine records amendment and routes next turn | `.specify/state/093-concurrency-by-default.md`: `last_verdict` records the amendment + all gate readings; `next_action` = "dispatch analyze-lite verification of the amendment, then resume implement waves"; new `amendments:` block and dated `gates:` line; `b9edf99f` touches only this file | PASS |
| 9 | Fresh gate reruns (explicit flags) | See § 2 — validate-requirements 0/0; validate-tasks PASS 0/0 over 159; pre-analyze requirements/plan/tasks all decision=pass, 0 errors, fr=36 sc=12 tasks=159; decomposition proceed 36 FR / 159 tasks (ceilings 120/160); decision-tensions ok 0/0 (5 records) | PASS |
| 10 | Commit scope | `git show --name-only b337e94d`: 13 files — 12 under `.specify/specs/093-concurrency-by-default/` (requirements, plan, tasks, feature-ref, notes/amend-fr036.md, 7 test-evidence files) + `.specify/memory/register.md`; `b9edf99f`: only the spine. No file outside spec dir + register + spine. Both are ancestors of HEAD `7ec5cc05`; working tree clean | PASS |

## 2. Fresh readings (verbatim)

```
CMD: python3 .specify/scripts/python/validate-requirements.py .specify/specs/093-concurrency-by-default/requirements.md
file: .specify/specs/093-concurrency-by-default/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 345 lines, 48 definition rows, 11 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

```
CMD: python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md
PASS: .specify/specs/093-concurrency-by-default/tasks.md — 0 error(s), 0 warning(s)
EXIT=0
```
Independent row count: `first=T001 last=T159 count=159`, no gap.

```
CMD: python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --repo <worktree> --spec-dir .specify/specs/093-concurrency-by-default --stage <requirements|plan|tasks>
{"stage": "<stage>", "decision": "pass", ..., "summary": {"errors": 0, "advisories": 83, "waived": 0, "fr": 36, "sc": 12, "tasks": 159, "clauses": 0, "files": 15}}
pre-analyze-check: stage=<stage> decision=pass errors=0 advisories=83 waived=0
EXIT=0   (all three stages; advisories are creation-target / .specify/goal / dated-history paths, no errors)
```

```
CMD: python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/093-concurrency-by-default/requirements.md --tasks .specify/specs/093-concurrency-by-default/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 36, "task_count": 159, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": [], "checked_at": "2026-11-09T11:28:19Z"}
EXIT=0
```

```
CMD: python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/093-concurrency-by-default
spec: .specify/specs/093-concurrency-by-default
status: ok
  [dtr-anchor] pass (0)  [dtr-section-missing] pass (0)  [dtr-record-incomplete] pass (0)
  [dtr-tension-id] pass (0)  [dtr-rejected-form] pass (0)  [expected-sacrifice-unmapped] pass (0)
scanned: 491 lines, 5 record(s)
0 error(s), 0 warning(s)
EXIT=0
```

## 3. Observations (non-blocking)

- `plan.md` § Summary still says "eleven new contract test modules"; the precise split (DoD-3, tasks.md) is ten new contract modules plus one unit module = eleven modules. The loose "contract" label predates the amendment and was incremented consistently; it does not affect any gate or DoD statement.
- The pre-analyze advisory total is 83 on this tree; the round-3 historical reading (112) belongs to an earlier tree and is a dated record. The amendment's evidence and this fresh rerun agree at 83.

## Verdict

AL: PASS
