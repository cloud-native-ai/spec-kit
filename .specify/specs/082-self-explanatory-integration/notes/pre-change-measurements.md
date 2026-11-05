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

## T012 — 原则块对确认门控扫描器的零命中（executed 2026-11-05, implement part 2）

The principle block written by T011 into `templates/constitution-template.md` was scanned line by
line with the scanner's **compiled** pattern (loaded from the script itself, not re-typed), exactly
as the clause requires:

```console
$ python3 - <<'PY'
import importlib.util, json
from pathlib import Path
spec = importlib.util.spec_from_file_location("s", "scripts/python/scan-confirmation-gates.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lines = Path('templates/constitution-template.md').read_text(encoding='utf-8').splitlines()
start = next(i for i,l in enumerate(lines) if l.startswith('### XVIII.'))
end = next(i for i in range(start+1, len(lines))
           if lines[i].startswith('### ') or lines[i].startswith('## '))
hits = [f"L{i}:{mm.group(0)!r}" for i, line in enumerate(lines[start:end], 1)
        for mm in m.BLOCKING_RE.finditer(line)]
print(json.dumps({"block_lines": end-start, "hits": hits}))
PY
{"block_lines": 22, "hits": []}
```

`hits: []` — the block is 22 lines and trips no blocking pattern. No scanner pattern, no frozen
baseline and no `.json` baseline file was modified.

Whole-scan control, measured in the same session (the clause forbids changing the total, and T049
owns the final comparison):

```console
$ python3 scripts/python/scan-confirmation-gates.py --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'
27
```

`27` equals the value re-measured at T002 above and the value pinned in `tasks.md` — zero new gate
hits attributable to this feature. Note the reading convention recorded at T002: `27` is **not** a
frozen baseline (the frozen value is `23` and one pre-existing test pins that equality, red in this
feature's baseline). The obligation this row discharges is "no NEW hit", not "total unchanged".

## T012 follow-on — mirror of the edited template (executed 2026-11-05)

Editing `templates/constitution-template.md` made its runtime mirror stale. `sync-mirrors.py
--check` reported the drift before the write, and the write was scoped to `templates` only:

```console
$ python3 scripts/python/sync-mirrors.py --check
DIFF  .specify/templates/constitution-template.md        (before the write)

$ python3 scripts/python/sync-mirrors.py --write --only templates
scope --only: templates
DIFF  .specify/templates/constitution-template.md
sync  templates/ -> .specify/templates/ (1 files)

$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
EXIT=0
```

`tasks.md` defers mirror commits to T039, but T007-T012 cannot leave a `DIFF` standing: T010's C-20
assertion reads the owner's **mirror** and asserts byte identity with the source, and the mirror
parity suite is this feature's own guard (C-22/C-24). The mirror write is therefore recorded here as
an in-passing repair and reported in the part-2 anomaly line, not as a scope expansion. The
`.specify/templates/` copy of the constitution template is a **generated** artifact (Two Hats): it
follows the source, and the source is what was authored.

---

# Implement part 3 measurements — T013-T018 (appended 2026-11-05)

**Base commit**: `8daf6b65` | **part_scope**: `T013-T018`

## T013/T014 — generator mandate entry and mirror sync

The `- **MUST include**` block went from 10 to 11 sub-entries. The mirror pair that owns it is
`skills/internal/` → `.specify/skills/internal/` (a separate pair from `skills/external/`), which is
why `--only templates --only skills` reported `ok` for skills and left the SKILL mirror at `DIFF`:

```console
$ python3 scripts/python/sync-mirrors.py --check          # after the T013 edit
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
DIFF  .specify/skills/internal/manage-constitution/SKILL.md
DRIFT detected

$ python3 scripts/python/sync-mirrors.py --write --only skills/internal
scope --only: skills/internal
DIFF  .specify/skills/internal/manage-constitution/SKILL.md
sync  skills/internal/ -> .specify/skills/internal/ (1 files)
EXIT=0

$ cmp skills/internal/manage-constitution/SKILL.md .specify/skills/internal/manage-constitution/SKILL.md
(identical)

$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0
```

## T016/T017 — the counts the carrier and the live roster actually hold

```console
$ grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
templates/constitution-template.md:18
.specify/memory/constitution.md:19

$ grep -cE '^  - \*\*.+?\*\* —' skills/internal/manage-constitution/SKILL.md
11

$ grep -n '^\*\*Version\*\*:' .specify/memory/constitution.md
422:**Version**: 1.16.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-11-05
```

Numeral split, as C-3 of the double-landing contract states it: the template's next free numeral is
XVIII, the live roster's is XIX. That is per-surface numbering, not a divergence.

## T017 — gate budget after the live landing (unchanged total)

```console
$ python3 scripts/python/scan-confirmation-gates.py --json | python3 -c "import json,sys;print(json.load(sys.stdin)['total'])"
27
```

27 is the same total measured at T002 (part 1). The new principle block, the instruction surface it
will gain in T022, and the mandate entry produced **zero** new blocking hits — which is the C-8
obligation, and the reason the frozen-baseline guards did not move on this feature's account.
