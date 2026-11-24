# Contract — `team-view.py` Program Interface

**Path**: `scripts/python/team-view.py` (source), `.specify/scripts/python/team-view.py` (mirror)
**Pinning test**: `tests/contract/test_team_view_program_contract.py` (CLI surface, exits, JSON keys, no-`run-checks`, read-only) and `tests/integration/test_team_view_program.py` (fixture behaviour, rendering, snapshot).
**Rule owner cited, never restated**: `shared/definitions/script-interface-definitions.md` (Script Interface Contract); `shared/definitions/anchor-definitions.md` § Archive Layers (scope value set); `skills/internal/create-team/SKILL.md` § Report contract; `skills/internal/create-team/references/summary-mapping.md` § 6 (ledger); `skills/internal/create-team/references/create-mode.md` (team schema).

**C-24** Read-only program.

`team-view.py` MUST NOT write any file, create any directory, register any run line, dispatch any seat, reach the network, or invoke any `goal-utils.py` action other than the three declared reads in C-25. A view must leave the working tree byte-identical (FR-004).

**C-25** Engine composition.

The only engine calls are:
```bash
python3 <sibling>/goal-utils.py binding team <slug> --json
python3 <sibling>/goal-utils.py list --json
python3 <sibling>/goal-utils.py targets <anchor-slug> --list --json
```
`<sibling>` is the directory of `team-view.py` itself, so the source tree and the `.specify/` mirror resolve identically. The action set, flags and exit codes are owned by the engine's `--help` and are not restated here. The program MUST NOT invoke `run-checks` and MUST NOT call any write action (FR-008 / FR-013 / A-7).

Measured 2026-11-24 (exit 0): `binding` → `{kind, slug, owner, owner_id, origin, path, archive_layer, lifecycle}`; `list` → `{"goals":[{slug,status,criteria_count,updated}, …]}`; `targets --list` → `{"targets":[…]}`.

**C-26** CLI surface (closed).

```
team-view.py [options] [<team-slug>]

  <team-slug>        exact slug under .specify/teams/; omitted = overview
  --repo-root PATH   repository root (default: derived from this file's resolved path)
  --scope VALUE      archive layer selector; closed set owned by anchor-definitions § Archive Layers
  --spec-dir PATH    forwarded to engine reads that accept it; never decides a landing point
  --json             emit the internal envelope instead of the human rendering
  -h, --help         usage; exit 0, zero side effects
  --version          one identity line; exit 0, zero side effects
```

No other option is declared. In particular `--target` is not declared (run-only; refused as an undeclared option with exit 2).

**C-27** Script Interface Contract.

`team-view.py` belongs to the required set of the rule owned by `shared/definitions/script-interface-definitions.md`; the rule's label set and classification steps are not restated here. The executable obligations this contract adds are only: (a) the implementation consumes `scripts/python/script_interface_cli.py` (`configure_parser`, `VersionAction`, `version_text`) so the version line and flag precedence come from the one helper; (b) the pinning test executes `-h`, `--help`, `--version` and an undeclared option, asserting zero writes for the first three and exit 2 for the last.

**C-28** Exit codes (closed).

| Exit | Meaning |
|------|---------|
| `0` | rendering produced: single team, overview, empty archive, dangling binding, overview with corrupt rows |
| `2` | input error: undeclared option, invalid `--scope`, extra positional, no-slug `--scope auto` |
| `3` | team not found: no `.specify/teams/<slug>/` directory (single mode) |
| `4` | definition corrupt: directory exists but `team.md` is missing, unreadable or has unparseable frontmatter (single mode) |
| `5` | rendered, but one required fact group is `不可读` because an engine read failed (degraded) |

No other exit code is produced. `3` and `4` are never interchanged (FR-006).

**C-29** Output modes.

- Default: the human-facing rendering (Chinese explanations, canonical identifiers), beginning with a title line (single) or an overview line, an `as-of` line, then the applicable groups/rows.
- `--json`: the E9 envelope of `data-model.md`; keys are part of this contract only for tests, never a user API.

The default rendering MUST contain the six group headings in the order of FR-008…FR-013 for a single team, and a table with one row per team (sorted by slug ascending) for the overview.

**C-30** State and declaration vocabulary.

Every state or declaration label in the output MUST be a member of the closed vocabulary owned by `data-model.md` § Rendering Line Types: the missing-state subset is `缺失` / `为空` / `不可读` / `未记录`, the declaration subset is `已声明` / `未声明`, and the derived labels are the members that table names (`定义损坏`, `形态异常`, `悬空（dangling）`, `未识别`, `已列出`, `已聚合`, `本次无嵌套 SDD 调用`, `未声明 → active`). Labels inside the missing-state subset MUST NOT be substituted for one another, and a missing fact never renders as `0` or as a fabricated value (FR-015).

**C-31** Shared strings and caps.

- Unknown slug output contains `[[STR-001]]` verbatim.
- Empty archive output contains `[[STR-002]]` verbatim.
- The available-slug list on the not-found path is bounded to 20 with an explicit omitted count.
- Report names are bounded to the newest 20 with an explicit omitted count.

**C-32** Deterministic ordering.

- Overview rows: slug ascending (directory name).
- Reports: newest first by the filename timestamp token; ties broken by filename ascending.
- Ledger current state follows the owner's last-event rule (`skills/internal/create-team/references/summary-mapping.md` § 6.1, IL-2); this contract only states that the program implements it, never a second ordering rule.
- Targets: the engine's `--list` order preserved.
- Members and matrix rows: file order preserved.

**C-33** Bounded latest-report summary.

`## Result Summary` and `## Verification` excerpts are bounded to the first 10 non-empty lines or 800 characters, whichever is reached first, with the truncation marker `…（截断）`. Old reports are names only, never opened for content. Missing segments render `未记录`; an unrecorded anomalies field never renders `无异常` (FR-012, A-4).

**C-34** As-of.

The rendering declares `as-of: <max_file_mtime_utc>（文件时间；非实时探测）`, computed from the newest mtime among consumed files, plus the latest report's filename timestamp (or `未记录`). The program MUST NOT claim live probing (FR-016).

**C-35** Frontmatter parsing (closed subset).

The program reads `team.md` frontmatter with a closed-subset parser: `key: value` scalars, inline lists, nested maps (bounded depth) and block sequences of maps (for `members`). Anything outside the subset in a position the view must read is `不可读` / `形态异常` for that fact, never a guessed value. The team schema's owner is cited; the parser is the view's own deliverable (research R-02).

**C-36** Legacy and archive tolerance.

- `anchor_slug` absent → identity is the team's own slug, disclosed as `inferred`; legacy `goal_slug` is disclosed as `legacy`; neither is normalized or migrated (FR-008, FR-020).
- `archived` lifecycle renders normally with the label; view never refuses an archived team (FR-020).
- Keys outside the current schema render as `其它声明键`, not as errors (B-09).

**C-37** No user-facing machine format, no new store.

`--json` is internal. The program creates no cache, snapshot, index or second store. Every run reads the archive live (A-5, A-12, FR-019).

**C-38** Example invocations (premises declared per example).

```bash
# E1 — resolved, executed surface: the three engine reads in C-25 (measured 2026-11-24, exit 0).
# E2 — program surfaces. NOT executable until implementation lands; each line is pinned by
#      tests/contract/test_team_view_program_contract.py once it exists.
python3 scripts/python/team-view.py --help
python3 scripts/python/team-view.py --version
python3 scripts/python/team-view.py
python3 scripts/python/team-view.py cws-workspace-cluster
python3 scripts/python/team-view.py cws-workspace-cluster --json
```

Per-example premises for E2 (re-measure, do not inherit):
- `scripts/python/team-view.py` exists and is executable by `python3`;
- `.specify/teams/cws-workspace-cluster/team.md` exists (measured 2026-11-24);
- the sibling `goal-utils.py` resolves at `scripts/python/goal-utils.py` (measured);
- `--help` and `--version` exit 0 with zero writes; the no-argument form exits 0 with an overview;
- the single-slug form exits 0 for an existing team and the rendering contains the six group headings;
- `--json` emits the E9 envelope keys.

A file-level disclaimer is not used: E1 is executed, E2 carries its own premises and its own named pinning test.
