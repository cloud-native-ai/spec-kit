# Pre-change measurements — 082-self-explanatory-integration (implement part 1)

**Captured**: 2026-11-05 | **Stage**: implement, `part_scope=T001-T006` | **Base commit**: `94e8c30d`
**Working dir**: repository root (`/storage/project/cloud-native-ai/spec-kit`)

This file is the fixed landing point named by `tasks.md` Phase 1–2. Each section states the exact
command, its real output and the date. Nothing below is transcribed from an earlier stage's record:
every figure here was re-executed at implement start, and where a figure differs from the one
pinned in `tasks.md`, the difference is stated in place.

## T002 — 改动前基线重取 (executed 2026-11-05)

```console
$ wc -c .specify/instructions.md
32739 .specify/instructions.md

$ grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
38:INSTRUCTIONS_BUDGET_BYTES=32768

$ grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
templates/constitution-template.md:17
.specify/memory/constitution.md:18

$ grep -n '^\*\*Version\*\*:' .specify/memory/constitution.md
383:**Version**: 1.15.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-10-27

$ python3 scripts/python/scan-confirmation-gates.py --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'
27
```

All five figures agree with the values pinned in `tasks.md` T002 (32739 / `38:INSTRUCTIONS_BUDGET_BYTES=32768` / 17 / 18 / 27).
The live constitution version line is recorded here because T017 (US1) advances it by MINOR and
T049 (Polish) re-reads the gate total — both later rows compare against these numbers.

**Naive-reading traps recorded with the measured value** (same forms as
`test-evidence/tasks-stage-premises.md` § E-1, re-affirmed here because this run re-executed them):

- The heading counts 17 / 18 are **`### N.` title lines**, not clause counts and not a
  "template is behind" signal. The live constitution carries one extra section that the template
  does not, so a template-behind inference from the totals is the wrong reading.
- The gate-scanner total `27` is **not** a frozen baseline. The frozen value (Feature 050's
  `baseline-gates.json`) is `23`, and one pre-existing test pins that equality — it is red in this
  feature's baseline (see the E2 row in the state spine). The claim this feature makes is **zero new
  hits inside the new blocks** (T012), not "total unchanged".

## T003 — 条款覆盖基线冻结 (executed 2026-11-05)

```console
$ python3 scripts/python/account-clause-coverage.py .specify/specs/082-self-explanatory-integration --freeze \
    > .specify/specs/082-self-explanatory-integration/coverage-baseline.txt
RC=0
```

Before/after comparison against the baseline frozen by the tasks stage at `f712cf58`:

```console
$ diff /tmp/cov-before.txt .specify/specs/082-self-explanatory-integration/coverage-baseline.txt
2c2
< # frozen-from: ... | base-sha: f712cf588985 | files: 248 (parsed 145 + named 103)
> # frozen-from: ... | base-sha: 94e8c30d5a20 | files: 248 (parsed 145 + named 103)
```

**The only delta is the provenance header line** (`base-sha` advances to this stage's base
`94e8c30d`); the frozen UNCOVERED clause-name set is unchanged. `wc -l` = 515 (2 header lines + 513
names), matching the tasks-stage baseline's 513 names. The freeze is therefore a re-stamp, not a
content change — the tasks-repair commit `94e8c30d` touched only `tasks.md` and added no contract,
so no clause entered or left the universe.

## T004 — 三份 owner 文档在框架源中的在场与形态 (executed 2026-11-05, read-only)

```console
$ ls -l shared/definitions/self-explanatory-definitions.md shared/guidelines/self-explanatory.md shared/workflow/best-practice-optimization.md
-rw------- 1 agent agent 4508 Nov  4 14:40 shared/definitions/self-explanatory-definitions.md
-rw------- 1 agent agent 6271 Nov  4 14:40 shared/guidelines/self-explanatory.md
-rw------- 1 agent agent 4613 Nov  4 14:40 shared/workflow/best-practice-optimization.md
```

`## ` heading counts (the `tasks.md` T004 premise asks for these):

```console
$ for f in shared/definitions/self-explanatory-definitions.md shared/guidelines/self-explanatory.md shared/workflow/best-practice-optimization.md; do printf '%s: %s\n' "$f" "$(grep -cE '^## ' "$f")"; done
shared/definitions/self-explanatory-definitions.md: 7
shared/guidelines/self-explanatory.md: 10
shared/workflow/best-practice-optimization.md: 8
```

All three present, non-empty, and the heading counts match the values pinned in T004
(4508 B / 7 ; 6271 B / 10 ; 4613 B / 8). This row is an **existence/shape** check only — the
documents' content is out of this feature's scope, and a missing document would be an upsends,
not a new file. Neither condition fired.

## T005 — 镜像引擎枚举形态 (executed 2026-11-05, read-only)

```console
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0
```

Six pairs enumerated, all `ok`, exit 0 — matching the T005 premise (65 files for the `shared`
pair; T031 expects 68 after the three mirrors are written). The `shared` pair is a **non-strict** pair: a file present only in the mirror
is reported as a note, not a failure (plan § Mirror Obligations fact 1). Consequence for this
feature: `ls .specify/shared/...` is NOT evidence of distribution, and the mirror judgement is
**keep**, not **reach** — the three mirrors already existed and were byte-identical at task start;
the obligation is that later edits must not reintroduce `MISS`/`DIFF`.
