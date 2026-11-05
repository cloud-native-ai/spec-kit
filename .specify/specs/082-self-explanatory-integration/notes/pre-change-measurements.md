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

---

# Implement part 5 measurements — T024-T028 (appended 2026-11-05)

**Base commit**: `5f267f22` | **part_scope**: `T024-T028`

The live-reconcile transcript, the idempotence run, the C-21 pairing and the T026 mirror transcript
live in `notes/quickstart-run.md` (that file is T024's designated landing point). Only the
measurements whose landing point is **this** file appear below.

## T025 — compatibility links (four commands + resolution)

```console
$ test -L CLAUDE.md && test -L QODER.md && test -L AGENTS.md
EXIT=0

$ readlink on all eight links the generator maintains
CLAUDE.md: L=yes -> .specify/instructions.md | resolves=yes
QODER.md: L=yes -> .specify/instructions.md | resolves=yes
AGENTS.md: L=yes -> .specify/instructions.md | resolves=yes
HERMES.md: L=yes -> .specify/instructions.md | resolves=yes
.github/copilot-instructions.md: L=yes -> ../.specify/instructions.md | resolves=yes
.qoder/project_rules.md: L=yes -> ../.specify/instructions.md | resolves=yes
.claude/project_rules.md: L=yes -> ../.specify/instructions.md | resolves=yes
.opencode/instructions.md: L=yes -> ../.specify/instructions.md | resolves=yes
```

Four commands were run as the row specifies (three `test -L` plus the `readlink` resolution) and the
four tool-directory links were added because C-16 names them as part of the same obligation. No link
was rewritten as a copy; the row's stop condition did not fire, so nothing was hand-rebuilt.

## T027 — mutation legs M-3 / M-4

Full transcript in `notes/red-first-evidence.md` § "Part 5 — mutation legs M-3 / M-4". Scratch root:
`.specify/.tmp/082-part5/` (verified against `.specify/.gitignore:30 .tmp/` with `git check-ignore`
**before** the first write, per `shared/guidelines/temp-directory-discipline.md` § 3), removed after
the run. The legs' anti-vacuity sentinels report the four repository files unchanged:
`template=44ea5381d660`, `generator=e8c46c498a75` before and after.

## T028 — the C-19 measurement this decision rests on

```console
$ python3 - <<'PY'   # count Documentation Map rows and locate the owner
...
rows: 10
shared/definitions/self-explanatory-definitions.md: in map=False rows=[]
shared/guidelines/self-explanatory.md:              in map=False rows=[]
shared/workflow/best-practice-optimization.md:      in map=False rows=[]
precedent row: **Confirmation Gates**   -> `.specify/shared/guidelines/confirmation-gates.md`
precedent row: **Objective Analysis**   -> `.specify/shared/workflow/objective-analysis-gate.md`
precedent row: **Critique and Self-Critique** -> `docs/concepts/critique-and-self-critique.md` + `.specify/shared/guidelines/critique-and-self-critique.md`
precedent row: **TODO-in-Context**      -> `.specify/shared/guidelines/todo-in-context.md`
PY

$ grep -n 'self-explanatory-definitions.md' templates/instructions-template.md
81:Full discipline — definitions, practice steps and the ceiling/floor rule — lives in `.specify/shared/definitions/self-explanatory-definitions.md` (do NOT copy its rules; reference the file).
```

The map has 10 rows; four of them are the precedent for an ambient discipline owner, and in every one
of those four the cited document's own trigger is **per-turn or per-command**. The owner's own trigger
(`shared/guidelines/self-explanatory.md` § 1 何时应用) is narrower — see the recorded decision in
`test-evidence/tasks-stage-premises.md` § P-5. The template names the owner exactly once, in the section
body, and the map section is 4 lines above it.


## Part 6 (T029-T033) — distribution measurements, 2026-11-05

### T031 — mirror engine, before and after the write

```console
$ python3 scripts/python/sync-mirrors.py --check          # BEFORE --write
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0

$ python3 scripts/python/sync-mirrors.py --write --only shared
scope --only: shared
ok    shared/ == .specify/shared/ (65 files)
EXIT=0

$ python3 scripts/python/sync-mirrors.py --check          # AFTER --write
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0
```

**The `shared` pair reports 65 files, not the 68 T031 predicts.** The figure is re-derived
independently and does not indicate a missing mirror:

| quantity | command | value |
|----------|---------|-------|
| files under `shared/` at HEAD | `git ls-tree -r --name-only HEAD shared \| wc -l` | 62 |
| new source files added by this part | `git diff --cached --name-only -- shared \| wc -l` | 3 |
| files under `shared/` now | `find shared -type f \| wc -l` | **65** |
| files under `.specify/shared/` now | `find .specify/shared -type f \| wc -l` | **65** |

**T029's "10-minute install" caveat did not materialise**: the venv + `pip install -e` completed in
≈6 s against cached wheels. Under the 540 s timeout the fixture allows, that is ample headroom on
this host; a cold host without wheel cache would be slower and is the case the timeout is sized for.

**Root cause of the 65-vs-68 reading — it is not a mirror defect, and no mirror file is wrong.**
The plan stage's own record already contains both numbers: research.md B-7 measured `ok … 65 files`
at the *start* of the plan stage, before this feature had added anything, at which time `shared/`
held **62** tracked files. So 65 was never `62 + 3`; it is a 62-file tree the engine counted as 65.
The three new documents are on disk in both trees (identical size, identical mtime, `cmp` rc 0), so
the pair is in fact complete — but T031's stated before/after (`65 → 68`) cannot both be true of the
same 62-file baseline, and the engine has not been observed counting 68 here.

Two candidate readings, and why this part does not pick one: (a) the plan-stage readings came from a
different tree state than this checkout (the files were created outside the plan run — B-7's own
"created outside this run's reach" note), so 65 was measured when three other files existed that are
now gone or were never tracked; (b) the engine's file enumeration differs from a plain `find` in a
way this run has not isolated. Distinguishing them means either inspecting an artifact this feature
does not own or judging the engine's semantics against a state that no longer exists — a decision,
not a correction. Recorded as an anomaly in the part-6 return and in the state spine.

### T031 — mutation off the dispatcher's checklist, proving the engine really writes these files

A `--write` that reports `ok` while copying nothing would leave the mirrors resting on a prior
state, so the copy path was exercised deliberately. The dispatcher's listed mutation legs (M-5/M-6)
target the parity suite and the docs link guard; this leg targets the *engine* and is not one of
them — it exists because "the three mirrors happen to be identical" is weaker evidence than "the
engine's write path produces them identically".

```console
$ printf 'x' >> .specify/shared/definitions/self-explanatory-definitions.md
$ python3 scripts/python/sync-mirrors.py --check
DIFF  .specify/shared/definitions/self-explanatory-definitions.md
EXIT=2

$ python3 scripts/python/sync-mirrors.py --write --only shared
scope --only: shared
DIFF  .specify/shared/definitions/self-explanatory-definitions.md
sync  shared/ -> .specify/shared/ (1 files)
EXIT=0

$ cmp shared/definitions/self-explanatory-definitions.md \
      .specify/shared/definitions/self-explanatory-definitions.md
EXIT=0        # byte-identical again
$ stat -c '%y %s' .specify/shared/definitions/self-explanatory-definitions.md
2026-11-04 14:40:51.431892221 +0800 4508   # source mtime restored by copy2
```

The engine's write path therefore does copy these files. The repository is left in the state the
three `cmp` calls in T032 assert.

### T033 — the packaged `shared/` tree is the distribution source, and it carries all three

```console
$ python3 -c "import specify_cli, os; print(os.path.dirname(specify_cli.__file__))"
/usr/local/lib/python3.11/site-packages/specify_cli      # the PRE-INSTALLED released CLI

$ python3 -c "import sys; sys.path.insert(0,'src'); import specify_cli; \
              print(specify_cli.MODULE_DIR); print(specify_cli.get_resource_path())"
/storage/project/cloud-native-ai/spec-kit/src/specify_cli
/storage/project/cloud-native-ai/spec-kit               # the WORKING TREE's resource root

$ grep -n '"shared" = ' pyproject.toml
37:"shared" = "specify_cli/shared"
```

**Recomputation for the "the source tree must have it; mirror-only does not count" criterion:**

```console
$ python3 - <<'PY'
import pathlib, sys; sys.path.insert(0, "src"); import specify_cli
shared_src = pathlib.Path(specify_cli.get_resource_path()) / "shared"
for rel in ("definitions/self-explanatory-definitions.md",
            "guidelines/self-explanatory.md",
            "workflow/best-practice-optimization.md"):
    p = shared_src / rel
    print(("YES" if p.is_file() else "NO "), p, p.stat().st_size if p.is_file() else "-")
sent = sorted(p.relative_to(shared_src).as_posix()
              for p in shared_src.rglob("*") if p.is_file())
print("transmitted:", len(sent), "| all three present:", all(t in sent for t in (
    "definitions/self-explanatory-definitions.md",
    "guidelines/self-explanatory.md",
    "workflow/best-practice-optimization.md")))
PY
YES .../shared/definitions/self-explanatory-definitions.md 4508
YES .../shared/guidelines/self-explanatory.md 6271
YES .../shared/workflow/best-practice-optimization.md 4613
transmitted: 65 | all three present: True
```

The copy section itself was not modified — `src/specify_cli/__init__.py` carries, unchanged:

```python
        # Copy shared directory (shared reference documents)
        if (resource_path / "shared").exists():
            ...
            shared_dest = project_path / ".specify" / "shared"
            shared_dest.mkdir(parents=True, exist_ok=True)
            copy_tree_with_rewrite(
                resource_path / "shared",
                shared_dest,
            )
```

`copy_tree_with_rewrite` walks `src.rglob("*")` over that root, so the three new files are reached
by the existing section with no new copy logic — which is what T033 asks this row to confirm. The
end-to-end proof of the same fact is T029's `specify init` run (three files present, 65 files in
`.specify/shared/`).

**The installed CLI is `partial`, and this part does not read it as evidence.** `/usr/local/bin/
specify` resolves to a released site-packages tree that predates this feature; C-26's own text and
T029's instruction forbid using it as an exemption. T029 therefore builds its own entry point from
this working tree in a temp venv (see `notes/red-first-evidence.md` § R-2).

---

# Part 7 (T034-T038) — the docs page, its links, and the two mutation legs

**Captured**: 2026-11-05 | **Base commit**: `e5d0ae87` | **part_scope**: `T034-T038`
**Scratch root**: `.specify/.tmp/082-part7/` (verified with `git check-ignore -q .specify/.tmp` before
the first write; removed after the run per `shared/guidelines/temp-directory-discipline.md` § 4)

## T035 — read-only review of the docs page's pointer-page form

Command and output (the page was untracked at review time; `git status --short docs/` showed `??`):

```console
$ wc -c docs/concepts/self-explanatory.md
1993 docs/concepts/self-explanatory.md

$ python3 - <<'PY'   # sentence-level copy probe + retired-name census
import re; from pathlib import Path
page  = Path("docs/concepts/self-explanatory.md").read_text(encoding="utf-8")
owner = Path("shared/definitions/self-explanatory-definitions.md").read_text(encoding="utf-8")
def sents(t):
    return [s.strip() for s in re.split(r"(?<=[。.!?])\s+|\n\n", t) if len(s.strip()) > 24]
page_s, owner_s = sents(page), set(sents(owner))
print("page sentences >24ch:", len(page_s),
      "| verdict-identical to owner sentences:", sum(s in owner_s for s in page_s))
print("望文生义 occurrences:", page.count("望文生义"))
print("canonical 不言自明:", page.count("不言自明"))
PY
page sentences >24ch: 13 | verdict-identical to owner sentences: 0
望文生义 occurrences: 1
canonical 不言自明: 2
```

Three findings, each decidable:

| check | verdict | measurement |
|-------|---------|-------------|
| points at `shared/definitions/self-explanatory-definitions.md` | **yes** | in the extractor's output, first entry |
| points at `shared/guidelines/self-explanatory.md` | **yes** | second entry |
| points at `shared/workflow/best-practice-optimization.md` | **yes** | third entry |
| copies the owner's body | **no** | 0 of 13 page sentences longer than 24 characters appear verbatim in the owner; the owner's seven `## ` headings appear 0 times (asserted by `test_c27_docs_page_does_not_restate_the_owner_body`) |
| retired name `望文生义` present only as a variant | **yes, and one line short** | one occurrence, inside `## Naming history`: `Introduced as 望文生义; the canonical term is now 不言自明 (Self-explanatory).` — it names the retirement but never states that the old name survives only as a glossary synonym |

**The one row that needed a write.** T035's instruction names exactly one addition — a one-line
retired-name history note — and the measured page carried the retirement fact without the variant
fact. Added (the sole edit T035 makes to the page; the page is not plan-owned):

```diff
 Introduced as 望文生义; the canonical term is now 不言自明 (Self-explanatory).
+The retired name survives only as a synonym in the glossary entry (`望文生义`), never as a second
+canonical term.
```

1993 B → 2111 B; the added sentence restates no owner rule (the glossary entry it names is the store
row, and the canonical/variant distinction is `STR-003`'s shape), so the page keeps its pointer-page
form. The `## Naming history` section is the only section the two-line note touches.

## T034 — the C-27 guard's own measurements

```console
$ python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q
.........                                                                [100%]
9 passed in 6.94s
EXIT=0
```

What the extractor found on the real page and how each path maps through the engine's `MIRROR_PAIRS`
(the mapping is derived, never restated — `_mirror_of` reads the engine):

```console
$ python3 -c "<load the module; print extraction + _mirror_of>"
extracted: ['shared/definitions/self-explanatory-definitions.md',
            'shared/guidelines/self-explanatory.md',
            'shared/workflow/best-practice-optimization.md']
problems : []
pair: shared/definitions/self-explanatory-definitions.md -> ('shared', '.specify/shared')
pair: shared/guidelines/self-explanatory.md              -> ('shared', '.specify/shared')
pair: shared/workflow/best-practice-optimization.md      -> ('shared', '.specify/shared')
exemptions: {}
```

**The allow-list is empty, and that is a measurement rather than an omission.** C-27 permits a path
that legitimately has no mirror to be judged in the source tree only, with a one-line reason. The
page names no such path today: all three of its pointers live under `shared/`, which is one of the
engine's pairs. `C27_MIRROR_EXEMPTIONS` therefore carries no entry — a one-line contract in the code
(`docs/` has no mirror, so a docs-internal link would be exempt) rather than five speculative entries.
The guard is still decidable for the exempt case: any extracted path outside every engine source dir
is reported as *"belongs to no mirror pair, and it is not in C27_MIRROR_EXEMPTIONS"*, so the next
docs-internal link fails loudly and forces a visible decision.

Four assertions carry C-27 in the module:

| assertion | subject | goes red when |
|-----------|---------|---------------|
| `test_c27_docs_page_names_both_required_owner_paths` | the floor paths named by the clause itself | the page is absent, or stops naming `STR-002` or the workflow owner (an empty extraction cannot pass) |
| `test_c27_docs_page_pointers_resolve_in_source_and_mirror` | every extracted path | a path is missing in the source tree **or** in its mirror tree |
| `test_c27_extraction_is_not_vacuous` | the extractor, over synthetic text | the regexp stops matching whole-span `.md` code spans, or stops reporting a broken pointer |
| `test_c27_docs_page_does_not_restate_the_owner_body` | the page vs the owner's `## ` headings | a heading is transplanted from the definition file |

T034 required no second engine: the guard is plain `re` + `pathlib` + the house `pytest` surface, and
the only table it consults is the mirror engine's own `MIRROR_PAIRS`.

## T037 / T038 — mutation legs M-5 and M-6

Both legs ran from `.specify/.tmp/082-part7/m56.py` against copies only. Verbatim transcript is in
`notes/red-first-evidence.md` § M-5 / M-6 and the E3 row below; the closes:

- **M-5**: one byte flipped at offset 53 of a copied mirror file → engine `compare_pair` returns
  `differing=[PosixPath('definitions/self-explanatory-definitions.md')]` → the parity suite's own
  byte-identity assertion raises, naming
  `.specify/shared/definitions/self-explanatory-definitions.md`. Real pair sha256 unchanged
  (`1b12a9c5e098` both sides).
- **M-6**: `` `shared/definitions/self-explanatory-definitions.md` `` replaced on a copy of the page →
  extraction still yields three paths but no longer that one → `unresolved_docs_page_paths` returns
  `['shared/definitions/removed-by-m6.md: MISSING in the source tree']` → the guard's own
  `assert not problems` goes red and names the mutated path. The real page is byte-identical before
  and after (`sha256 04bb8c345c4e…`), and all 11 files under `docs/concepts/` keep their digests.
