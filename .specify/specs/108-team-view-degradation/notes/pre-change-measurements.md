# Pre-change measurements — 108-team-view-degradation (T003)

Every row records the command, the real reading and the date it was taken. All readings are
taken **before** any executable surface of this feature is edited (implement entry, HEAD
`005437f72`, worktree `.specify/.tmp/sdd-loop/worktrees/team-view-degradation`, branch
`108-team-view-degradation`). Re-measure; do not trust the numbers without the command.

## Row 1 — Corpus composition (FR-001 grammar + FR-003 order)

- **Date**: 2026-11-26
- **Command**: inline CPython scan over `.specify/teams/*/runs/*` (regular files only) applying the
  five FR-001 stamp forms with strict UTC calendar validation and the FR-003 fixed order
  (no parseable leading stamp → residue; stamp + `(?:-[0-9a-f]{4})?-(?:report|stage)\.md` → report;
  stamp + any other remainder → auxiliary):

```python
import re, datetime, pathlib, collections
STAMP_FORMS = [
    ("compact+hhmmss", re.compile(r'^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z')),
    ("compact+hhmm",   re.compile(r'^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})Z')),
    ("iso+hh:mm:ss",   re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z')),
    ("iso+hh-mm-ss",   re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2})Z')),
    ("iso+hhmmss",     re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2})(\d{2})(\d{2})Z')),
]
REPORT_REMAINDER = re.compile(r'^(?:-[0-9a-f]{4})?-(?:report|stage)\.md$')
def stamp(name):
    for label, rx in STAMP_FORMS:
        m = rx.match(name)
        if not m: continue
        g = [int(x) for x in m.groups()]
        sec = g[5] if len(g) == 6 else 0
        try: datetime.datetime(g[0], g[1], g[2], g[3], g[4], sec)
        except ValueError: return None, None
        return m.end(), label
    return None, None
files = sorted(p for p in pathlib.Path('.specify/teams').glob('*/runs/*') if p.is_file())
counts = collections.Counter(); teams = collections.defaultdict(collections.Counter)
aux, res, reportstyle = [], [], []; compact = 0
for p in files:
    end, form = stamp(p.name)
    if end is None: cls = 'residue'; res.append(str(p))
    elif REPORT_REMAINDER.match(p.name[end:]):
        cls = 'report'
        if form == 'compact+hhmmss' and p.name[end:] == '-report.md': compact += 1
        else: reportstyle.append(str(p))
    else: cls = 'auxiliary'; aux.append(str(p))
    counts[cls] += 1; teams[p.parts[2]][cls] += 1
print(f"files={len(files)} reports={counts['report']} auxiliary={counts['auxiliary']} residue={counts['residue']}")
print(f"compact-conforming={compact} report-style={len(reportstyle)}")
print("auxiliary:", *aux, sep='\n  '); print("residue:", *res, sep='\n  ')
for t, c in sorted(teams.items()):
    print(f"  {t}: reports={c['report']} auxiliary={c['auxiliary']} residue={c['residue']}")
```

- **Reading**: `files=46 reports=41 auxiliary=3 residue=2`; `compact-conforming=28 report-style=13`.
  - auxiliary: `demo-seat-dispatch/runs/20261008T214100Z-seat-result.md`,
    `session-driven-self-improvement/runs/20261008T070532Z-verification.md`,
    `session-driven-self-improvement/runs/20261008T084144Z-verification.md`
  - residue: `session-driven-self-improvement/runs/2026-10-06-S1-judgment-contract.md`,
    `session-driven-self-improvement/runs/2026-10-07-progress-snapshot.md`
  - all-non-conforming teams: `viz-skill-arena` 5 reports, `draw-two-layer-structure` 7,
    `draw-diagram-interactive` 1 (sum 13).
  - full per-team table (reports only, teams with files): command-logic-as-classified-skills 4,
    cws-workspace-cluster 2, demo-seat-dispatch 1, draw-diagram-interactive 1,
    draw-plantuml-optimizer 5, draw-two-layer-structure 7, post-refactor-mechanism-integrity 1,
    requirement-implement-monitor 5, session-driven-self-improvement 5,
    skill-layer-install-separation 3, summarize-project-optimizer 2, viz-skill-arena 5.
- Matches plan-time M1 (research.md § M1) and EP-004 exactly. Trap form: a bare `ls | wc -l`
  reads 46 as "46 reports", counting the 3 auxiliary + 2 residue.

## Row 2 — Baseline object and blob identity (plan baseline `54c6efa8c`)

- **Date**: 2026-11-26
- **Command**: `git cat-file -e 54c6efa8c && echo OBJECT-OK`;
  `git show 54c6efa8c:scripts/python/team-view.py | sha256sum`;
  `sha256sum scripts/python/team-view.py`
- **Reading**: object present (`OBJECT-OK`, exit 0);
  baseline blob sha256 = `81fad3f9df019319c75d1a73c1ffa27338ac942db6b22c4b90e6b5b61e7bf06b`;
  working-tree sha256 = `81fad3f9df019319c75d1a73c1ffa27338ac942db6b22c4b90e6b5b61e7bf06b`
  (byte-equal — the baseline referent is exact).

## Row 3 — Mirror and per-tool-copy baseline

- **Date**: 2026-11-26
- **Command**: `python3 scripts/python/sync-mirrors.py --check; echo rc=$?` and
  `python3 scripts/python/regen-command-copies.py --check; echo rc=$?`
- **Reading**: `sync-mirrors.py --check` rc **0** — six mirror pairs `ok` byte-identical
  (templates 23 files, skills/external 394, skills/internal 139, agents 20, scripts 133, shared 117),
  seven projected members `ok` (including `.specify/scripts/python/team-view.py` and
  `.specify/skills/internal/view-team/SKILL.md` pairs via their projection declaration);
  `regen-command-copies.py --check` rc **0**, `OK: all per-tool command copies match the source templates.`

## Row 4 — Fingerprints of the four existing team-view test files

- **Date**: 2026-11-26
- **Command**: `sha256sum tests/unit/test_team_view_parsers.py tests/contract/test_team_view_program_contract.py tests/contract/test_team_view_command.py tests/integration/test_team_view_program.py`
- **Reading**:
  - `tests/unit/test_team_view_parsers.py` = `586d89af7b80d3638d608f4aaf94286f9e13ede8248cbf04075d0d306a27efea`
  - `tests/contract/test_team_view_program_contract.py` = `c90700aa0801bc3e49f83bad868551f8c44650732236a6eb3e3bc17fb326cb90`
  - `tests/contract/test_team_view_command.py` = `93ca0b23673a6b6030e9b8625151bd2f71a19598d31d9834a65241666161da90`
  - `tests/integration/test_team_view_program.py` = `6cfaca939d93c74eaa231ef0bf7e1ad58b1ca4a52177244fedd1f1d3d5509623`
- Matches the tasks.md § Measured Premises row (prefixes `586d89af` / `c90700aa` / `93ca0b23` / `6cfaca93`).

## Row 5 — The two `goal-utils.py binding` messages

- **Date**: 2026-11-26
- **Command** (scratch teams under the sanctioned temp root
  `.specify/.tmp/sdd-loop/tmp/team-view-degradation/binding-probe/`, gitignored via `.specify/.gitignore:30`;
  each team.md is a minimal frontmatter file — one without a `binding:` block, one with a
  partial block carrying only `owner: human`):
  `python3 scripts/python/goal-utils.py binding team no-binding-team --repo-root <probe-abs> --json`
  `python3 scripts/python/goal-utils.py binding team partial-binding-team --repo-root <probe-abs> --json`
- **Reading** (both exit **2**):
  - no-binding: `binding-missing: <path>/team.md carries no binding block; a definition without a complete binding record is uninterpretable (owner / owner_id / origin)`
  - partial-keys: `binding-missing: <path>/team.md is missing the binding key(s) owner_id, origin; exactly owner / owner_id / origin are required`
- Note: all 24 live `.specify/teams/*/team.md` definitions carry complete three-key bindings
  (`binding:` block with `owner` / `owner_id` / `origin`; `viz-skill-arena` sample reads exit 0),
  so both messages are reproduced the way M3 did — a synthesized scratch team — never by
  editing a live team definition.

## Row 6 — Implement-entry dependency requirement sets (DoD-2 baseline capture, see T005)

- **Date**: 2026-11-26
- **Command**: `sed -n '/^\[project\]/,/^\[project.scripts\]/p' pyproject.toml`
- **Reading**:
  - `[project].dependencies` = `typer`, `rich`, `httpx[socks]`, `readchar`,
    `truststore>=0.10.4; python_version >= '3.10'`
  - `[project.optional-dependencies].dev` = `pytest`, `pytest-xdist; python_version >= '3.9'`, `ruff`
- These sets are re-captured at implement entry in
  `test-evidence/implement-entry-readings.txt` as DoD-2's baseline side.
