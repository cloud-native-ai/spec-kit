# Pre-change measurements — slice 074b-nested-governance (implement, T001)

**Captured**: 2026-10-29T05:45:14Z, before any edit of this slice's delivery surface.
**HEAD at capture**: `241a6082b40e7eb412de8143d0d0fbc52014967f` (`241a6082b`)
**Host**: linux / Python 3.11.11 / pytest 8.4.2

Every block below is pasted from the real run of the command above it; no value is transcribed by hand.
Later tasks append their own sections (`containment`, `regression`) — this file is the single evidence
sink for "no new X" comparisons, so a reader compares against the block captured here, never against a
number quoted in another document.

## 1. Mirror and command-copy baselines

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
rc=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

Six pairs, zero pre-existing drift: the criterion for every mirror row of this slice is "no NEW drift",
and it is measurable as "still clean".

## 2. Repository state at capture

```text
$ git rev-parse HEAD
241a6082b40e7eb412de8143d0d0fbc52014967f

$ git status --short | wc -l
33
# 8 modified tracked files (all under .specify/memory/session/, pre-existing dirty — not touched,
#   not restored by this slice) + 25 untracked entries:
#   .specify/memory/{exec-quant/records,feedback,session}/… (8 each, per-entry stage-accounting records)
#   .specify/state/074b-nested-governance.md (1)
```

The eight modified tracked session files and the twenty-five untracked entries above are **pre-existing**
and are neither committed nor reverted by this slice.

## 3. Instruction-surface sizes (the ceiling judgement for FR-005 / C-18)

```text
$ wc -c templates/instructions-template.md .specify/instructions.md
34666 templates/instructions-template.md
41948 .specify/instructions.md
76614 total
```

Both files already exceed the generator's 32,768 B budget **before** this slice, so the diffusion section's
criterion is a declared ceiling plus a measured delta, never "fits the budget" (research RB6).

## 4. The leaf preset carries no hosting declaration (V-9's negative subject)

```text
$ grep -c 'sdd-invocation' agents/sdd-executor.agent.md
0
rc=1
```

Measurement unit: the shipped preset file, not a repo-wide grep (design prose mentioning the key is a
citation, not a declaration).

## 5. Ledger attribution field (reused, never invented)

```text
$ grep -n 'target_ref' skills/internal/create-team/references/summary-mapping.md
100:| `target_ref` | string | 否 | 归属的 Target 身份(038)。**局部形** `T-\d{3}`,goal 由团队绑定隐含;缺省 = 归属 goal 整体。见 §6.5 |
143:### 6.5 `target_ref` 归属折叠(038)
149:- **缺省**:无 `target_ref` → 归属 goal 整体(`targets.unattributed_to_target` 计数);存量行语义不变。
150:- **正交性**:团队命名空间前缀(`<team-slug>.TI-nnnn`,§6.2)照常加;`target_ref` 仍为局部形,二者互不影响。
```

Field, grammar and default are owned there; this slice cites them and adds no field.

## 6. Flow-class baseline (no-new-unit negative)

```text
$ python3 .specify/scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
rc=0
```

## 7. Existence census of the 9-row delivery surface

```text
$ for f in <the nine rows + the leaf preset and the reused fixture>; do test -e "$f" && echo OK || echo ABSENT; done
OK      skills/internal/create-team/SKILL.md
OK      skills/internal/create-team/references/conceptual-model.md
OK      skills/internal/run-agent/SKILL.md
OK      templates/instructions-template.md
OK      shared/guidelines/proactive-trigger.md
OK      tests/contract/test_sdd_invocation_governance.py
OK      tests/fixtures/nested_sdd.py
OK      agents/sdd-executor.agent.md
ABSENT  tests/contract/test_nested_run_report.py
ABSENT  tests/contract/test_sdd_diffusion.py
ABSENT  tests/contract/test_sdd_compat_containment.py
```

8/8 subjects in place, 3/3 new suites absent — the precondition of the red-first step.

## 8. Storage-surface file-name sets (GATE-7 comparator)

```text
$ find .specify/state -maxdepth 1 -type f | LC_ALL=C sort | wc -l
3
$ find .specify/memory -type f | LC_ALL=C sort | wc -l
681
# .specify/memory/ composition by top-level entry: feedback 194, session 180, evidence 130,
#   exec-quant 78, features 71, tools 10, knowledge 9, trigger 2, sanitize 2,
#   + tools.md / register.md / glossary.md / constitution.md (single files)
```

The two sorted lists (688 lines with headers) live verbatim in
[`pre-change-file-sets.txt`](pre-change-file-sets.txt) — captured with the command recorded in that
file's header, because the comparator for GATE-7 / T024 is `LC_ALL=C comm -13 <that file> <re-captured>`
and a comparison needs the pre-list on disk, not a count in prose. The lists are kept out of this
document so a reader is not handed 681 machine-generated paths to skip.

Reading note for the later comparison: `feedback/`, `session/`, `evidence/` and `exec-quant/records/`
are per-entry record families written by stage accounting (one file per entry, timestamped names); a new
name there is a stage record, not a registry, ledger, state spine, ownership model or integration queue.
`state/` is the line-registry / state-spine family and its name set is the strict one.

## 9. Not measured here

- Full-suite baseline: recorded as the implement slot-`baseline` row in
  [`../test-evidence/implement.jsonl`](../test-evidence/implement.jsonl) (`seq=1`), not in this file.
- Name-level targeted baseline: owned by
  [`../test-evidence/targeted-set-v1-baseline.txt`](../test-evidence/targeted-set-v1-baseline.txt) (T002
  re-captures it in place).
- Clause-coverage baseline: owned by [`../coverage-baseline.txt`](../coverage-baseline.txt) (T003 freezes
  it).
