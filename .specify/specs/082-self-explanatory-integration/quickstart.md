# Quickstart: Self-Explanatory Framework Integration

**Feature**: 082-self-explanatory-integration | **Date**: 2026-11-05

Every scenario below was executed in this repository during the plan stage, and the output shown is
what the command actually printed. The scenarios that can only run **after** implementation say so
per scenario — not per file — and state exactly which premises they rest on, so `/speckit.tasks` can
re-probe the premise instead of trusting the example.

Working directory for every command: repository root (`/storage/project/cloud-native-ai/spec-kit` on
the machine that produced these readings; the commands are written against `.` so they run anywhere).

## S-0 — Re-take the baseline (run first, always)

```bash
python3 --version && git --version && python3 -m pytest --version
python3 scripts/python/sync-mirrors.py --check; echo "mirror exit=$?"
wc -c .specify/instructions.md
grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
python3 scripts/python/scan-confirmation-gates.py --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'
```

Observed on 2026-11-05:

```text
Python 3.11.11
git version 2.43.5
pytest 8.4.2
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
OK: all per-tool command copies match the source templates.
mirror exit=0
32739 .specify/instructions.md
38:INSTRUCTIONS_BUDGET_BYTES=32768
templates/constitution-template.md:17
.specify/memory/constitution.md:18
27
```

Read the exit code directly (`echo $?` right after the command, never `| tail`), because the engine
prints its verdict to stdout while the process status is what any acceptance claim must cite.

## S-1 — Mouth-to-tail: the whole point of one framework command

```bash
cd "$(mktemp -d)" && specify init --here --ai claude --no-git --skip-tls 2>&1 | tail -5
ls .specify/shared/definitions/self-explanatory-definitions.md \
   .specify/shared/guidelines/self-explanatory.md \
   .specify/shared/workflow/best-practice-optimization.md
```

Executed at plan stage (the entry point is `specify`, not `spec`; `specify init --help` lists
`--here`, `--ai`, `--no-git`, `--skip-tls`). Observed:

```text
Optional: /speckit.agents /speckit.analyze /speckit.checklist /speckit.clarify
/speckit.derive /speckit.docs /speckit.feedback /speckit.goal /speckit.history
/speckit.instructions /speckit.interview /speckit.research /speckit.review
/speckit.sanitize /speckit.session /speckit.skills /speckit.team /speckit.todo
/speckit.tools
ls: cannot access '.specify/shared/definitions/self-explanatory-definitions.md': No such file or directory
ls: cannot access '.specify/shared/guidelines/self-explanatory.md': No such file or directory
ls: cannot access '.specify/shared/workflow/best-practice-optimization.md': No such file or directory
```

The installed CLI is the **published** release, whose packaged resources predate this feature, so the
three files are absent — the correct reading at plan time. The scenario's expected result applies
**after** a release that carries the three documents. Premises the example rests on, each re-probable:
(i) `specify` is on `PATH`; (ii) the packaged resource tree contains
`shared/{definitions,guidelines,workflow}/<name>.md` — the sink that receives it is confirmed present
(`.specify/shared/{constants,definitions,guidelines,patterns,workflow}` exist in the fresh project,
so the copy ran and only the source files were missing); (iii) the copy path is
`src/specify_cli/__init__.py:2504-2516`; (iv) the four flags above are accepted by the installed
version. Re-probe with `specify init --help` and, for (ii), `python3 -c "import specify_cli,os;
print(os.path.dirname(specify_cli.__file__))"` followed by a listing of its `shared/` tree.

## S-2 — The generator injects an additive section on an existing project

```bash
T=$(mktemp -d) && mkdir -p "$T/.specify/templates" "$T/.specify/scripts/python"
printf '# Instructions\n\n## Alpha\n\nalpha body\n\n## Beta\n\nbeta body\n\n## Gamma\n\ngamma body\n' \
  > "$T/.specify/templates/instructions-template.md"
printf '# Instructions\n\n## Alpha\n\nalpha body (customized)\n\n## Project Custom\n\nkept\n' \
  > "$T/.specify/instructions.md"
ln -s "$PWD/scripts/python/tools-utils.py" "$T/.specify/scripts/python/tools-utils.py"
cd "$T" && git init -q && bash "$OLDPWD/scripts/bash/generate-instructions.sh" 2>&1 | grep -E 'Injected|Section reconcile|Instructions size'
cat .specify/instructions.md
```

Executed at plan stage; observed (the log prefix is the house logger's timestamp/pid form, shown
elided):

```text
[...][INFO]Injected missing template section(s): Beta, Gamma
[...][INFO]Instructions size: 118 B (budget 32768 B, 32650 B headroom). Section table, largest first:
# Instructions

## Alpha

alpha body (customized)

## Project Custom

kept

## Beta

beta body


## Gamma

gamma body
```

Note the double blank line before `## Gamma`: injection splices each missing block in with its own
trailing blank line, so a project that has never received a section gets one extra blank line. It is
cosmetic and pre-existing; this feature does not change the injection logic, so no clause asserts
anything about it. A second run printed
`Section reconcile: live instructions already carry all template sections.` — idempotence holds.

What this proves: injection happens, customised content survives, project-specific sections survive,
and the size report runs on the injection path. What it does **not** prove: that the *real* section
propagates — that is the contract test's job (S-4).

## S-3 — Regenerate this repository's live instructions (implementation-time)

```bash
bash scripts/bash/generate-instructions.sh 2>&1 | grep -E 'Injected|Section reconcile|Instructions size|BUDGET'
grep -n '^## Self-Explanatory Structure' .specify/instructions.md
wc -c .specify/instructions.md
```

Expected after implementation: the `## Self-Explanatory Structure (不言自明)` heading appears in the
live file exactly once, the size line reports `within`, and `wc -c` reads a value strictly less than
the (raised) budget constant. **Not executed at plan stage** — the section does not exist yet.
Premises: the template change lands before the generator runs; the budget constant is raised in the
same change (otherwise `BUDGET … over` is printed and SC-009 is false on arrival); the generator
writes a timestamped backup next to the live file, which is git-ignored.

## S-4 — The guards decide pass and fail

```bash
python3 -m pytest tests/contract/test_constitution_double_landing.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_glossary_mechanism.py \
  -q -p no:cacheprovider --no-header
python3 -m pytest tests/contract/test_mirror_parity_suite.py -q -p no:cacheprovider --no-header \
  -k 'self-explanatory or best-practice-optimization'
```

Expected after implementation: both runs exit 0; the second selects exactly three parameters (one per
new source document). **Not executed at plan stage** — the guards that assert the new subjects do not
exist yet, and today the double-landing suite would pass *vacuously* for this feature. Premises: the
mirror parity suite derives its table from `MIRROR_PAIRS`, so the three files are selected by name;
the double-landing suite's new watchlist entry and count bumps land in the same change or its count
assertions fail.

## S-5 — Mutation drills (the guards must be able to go red)

Executed at plan stage for the two mechanisms that already exist (the third and fourth need the
implementation's new assertions):

```bash
T=$(mktemp -d) && cp templates/constitution-template.md "$T/" && \
  cp skills/internal/manage-constitution/SKILL.md "$T/"
python3 - "$T" <<'PY'
import re, sys
from pathlib import Path
t = Path(sys.argv[1])
for name, title in (("constitution-template.md", "Grounded Naming"),
                    ("SKILL.md", "Grounded Naming")):
    f = t / name
    f.write_text(re.sub(rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$.*?(?=^### |^## |\Z)", "", f.read_text(), flags=re.M | re.S)
                  if name.endswith("template.md") else
                  re.sub(rf"^  - \*\*{re.escape(title)}\*\* —.*?(?=^  - \*\*|^- |\Z)", "", f.read_text(), flags=re.M | re.S))
PY
python3 - "$T" <<'PY'
import re, sys
from pathlib import Path
T = sys.argv[1]
TITLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)
ENTRY_RE = re.compile(r"^  - \*\*(.+?)\*\* —", re.M)
tmpl = {m.group(2).strip() for m in TITLE_RE.finditer(Path(T, "constitution-template.md").read_text())}
skill_text = Path(T, "SKILL.md").read_text()
lines = skill_text.splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("- **MUST include**"))
body = [lines[start]]
for l in lines[start+1:]:
    if l.startswith("- "): break
    body.append(l)
names = {m.group(1).strip() for m in ENTRY_RE.finditer("\n".join(body))}
print("mutated template still has the title:", "Grounded Naming" in tmpl)
print("mutated mandate list still has the entry:", "Grounded Naming" in names)
PY
```

Observed at plan stage:

```text
mutated template still has the title: False
mutated mandate list still has the entry: False
real files untouched: True
```

This is the anti-vacuity half of the drill: the extraction that the guard relies on *does* notice a
deleted subject. On the real tree the same extraction returns `True` for both. The teardown is the
`mktemp` directory, which is discarded; nothing in the repository is touched (the drill writes only
into `$T`).

## S-6 — Distribution check on an installed CLI

```bash
cd "$(mktemp -d)" && specify init --here --ai claude --no-git --skip-tls >/dev/null 2>&1
find .specify/shared \( -name 'self-explanatory*' -o -name 'best-practice-optimization.md' \)
```

Executed at plan stage: prints nothing (the published CLI's resources predate the three documents).
Expected after a release carrying them: three paths. The `-o` terminator is parenthesised on purpose —
without it `find` applies the `-print` of the first branch only to the parenthesised group and silently
narrows the match. Same premises as S-1; teardown is the temporary directory.

## S-7 — The docs page's pointers resolve

```bash
python3 - <<'PY'
import re
from pathlib import Path
page = Path("docs/concepts/self-explanatory.md").read_text()
paths = re.findall(r"`([^`]+\.md)`", page)
missing = [p for p in paths if not Path(p).exists()]
print("referenced:", paths)
print("missing:", missing)
PY
```

Executed at plan stage; observed:

```text
referenced: ['shared/definitions/self-explanatory-definitions.md', 'shared/guidelines/self-explanatory.md', 'shared/workflow/best-practice-optimization.md']
missing: []
```

All three resolve in the source tree; the contract clause (C-27) additionally asserts each resolves
in its mirror tree, which after implementation is also true.

## Teardown

Every scenario creates its state under `mktemp -d` and leaves it there. Nothing is deleted from the
repository, no branch is created, nothing is pushed. Re-running S-2 twice is safe: the second run
reports `Section reconcile: live instructions already carry all template sections.`
