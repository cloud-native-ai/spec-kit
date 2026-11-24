# Research — /speckit.team view（103-team-view）

**Stage**: plan / Phase 0
**Measured**: 2026-11-24 (all counts and command outputs below were taken in this session)

Every fact below was read from the repository or produced by executing the named command. Nothing in this file restates an owner's rule table; the owner path is cited instead.

## Baseline measurements

| # | Measurement | Command / path | Reading |
|---|-------------|----------------|---------|
| B-01 | Team archive size | `ls .specify/teams \| wc -l` | 20 team directories |
| B-02 | Legacy `goal_slug` spelling in the live archive | `grep -rl '^goal_slug:' .specify/teams/*/team.md \| wc -l` | 0 files — the legacy branch is fixture-only |
| B-03 | Teams with no declared `anchor_slug` (inferred identity path) | loop over `.specify/teams/*/team.md` | 10 of 20 — the inferred-identity disclosure is a live path, not an edge case |
| B-04 | Item ledgers present | `ls .specify/teams/*/items.jsonl` | 5 teams; one of them (`viz-skill-arena`) is a zero-line file → the "empty" state exists live |
| B-05 | Run directories / reports | `ls -d .specify/teams/*/runs`; `ls .specify/teams/*/runs/*.md` | 12 directories, 46 reports |
| B-06 | Reports carrying the mandatory `## Verification` segment | `grep -l '^## Verification' .specify/teams/*/runs/*.md \| wc -l` | 9 of 46 — most live reports predate the current report contract |
| B-07 | Reports carrying `## Nested SDD Runs` | `grep -l '^## Nested SDD Runs' .specify/teams/*/runs/*.md \| wc -l` | 0 of 46 — the "未记录" branch is the normal case in this repository |
| B-08 | Continuous operating spines | loop for `constraints.md` | 3 teams |
| B-09 | Frontmatter keys actually present | regex scan of `.specify/teams/*/team.md` | `binding`/`created`/`description`/`pattern`/`slug`/`updated` 20/20; `members` 19; `config` 19; `lifecycle_state` 11; `anchor_slug` 10; `territory` 15; `seats` 8; `stage_seats` 7; `preset` 4; plus legacy top-level `summary` (2), `scope`/`spec_dir` (8) — the view must tolerate keys outside the current schema |
| B-10 | Declared `config` top-level keys | regex scan | 59 distinct keys — the key space is open; the view cannot enumerate a closed config catalogue |
| B-11 | `goal-utils.py` version and read actions | `python3 scripts/python/goal-utils.py --version`; `--help` | `0.0.22`; read actions `binding`, `list`, `targets --list`, `validate` exist with zero-write descriptions |
| B-12 | `binding` output shape | `python3 scripts/python/goal-utils.py binding team 085-sdd-temporary-goal-team --json` | keys `kind` / `slug` / `owner` / `owner_id` / `origin` / `path` / `archive_layer` / `lifecycle` |
| B-13 | Anchor enumeration shape | `python3 scripts/python/goal-utils.py list --json` | `{"goals": [{slug, status, criteria_count, updated}, …]}` |
| B-14 | Target enumeration shape | `python3 scripts/python/goal-utils.py targets 094-goal-team-parallel --list --json` | `{"targets": []}` for an anchor with no Targets |
| B-15 | Mirror baseline (before any edit) | `python3 scripts/python/sync-mirrors.py --check` | rc 0: all five mirror pairs `ok`, all six projected rows `ok`, per-tool command copies `OK` |
| B-16 | Per-tool copy baseline | `python3 scripts/python/regen-command-copies.py --check` | rc 0 — regenerate, then `--check` again after editing `templates/commands/team.md` |
| B-17 | Command template currently carries no `argument-hint` | `grep -n 'argument-hint' templates/commands/team.md` | no match — FR-001 adds the key; `templates/commands/anchor.md` and `goal.md` are the sibling precedents |
| B-18 | Stale literal locations | `grep -rn 'exactly three modes'` | `templates/commands/team.md`, `docs/reference/commands/team.md`, and four per-tool copies (regenerated) — the archived spec under `.specify/archive/` is dated history and is not edited |
| B-19 | `command-mode` scope | `python3 scripts/python/goal-utils.py command-mode --help` | `--command` choices are `anchor\|goal` only; adding `view` to the team argument-hint has no engine consumer |
| B-20 | PyYAML is not a declared dependency | `grep -n 'dependencies' -A 10 pyproject.toml`; `grep -n 'requires-python' pyproject.toml` | runtime set `typer`, `rich`, `httpx[socks]`, `readchar`, `truststore`; dev group `pytest`, `pytest-xdist`, `ruff`; `requires-python = ">=3.8"` — no YAML library, so RS-001's stdlib-only obligation holds |

## Decisions

- **R-01 — The program owns the deterministic text rendering; the skill owns invocation and error navigation.** `team-view.py` emits the human-facing six-group rendering by default and a structured envelope under `--json` (internal only). `view-team` resolves inputs, invokes the program, presents its output verbatim, and translates non-zero exits into navigation. Rationale: SC-001/SC-006 become executable assertions over real output instead of LLM behaviour; Program-First discipline (`shared/guidelines/token-efficiency.md`).
- **R-02 — Frontmatter is read through a closed-subset parser owned by the program.** The parser supports scalars, inline lists, nested maps (depth-limited) and block sequences of maps (for `members`). Precedent: `goal-utils.py`'s `read_frontmatter_subset` covers scalars/inline lists/one nested map only and does not read `members`; the program therefore carries its own reader for the schema owned by `create-mode.md`. No third-party import (B-20).
- **R-03 — Binding and anchor facts are engine calls only.** `binding team <slug>`, `list`, `targets <anchor> --list` are invoked as declared read actions; the program never re-implements the binding record's meaning, the lifecycle value set or Target semantics (RS-004 unchanged, FR-008/FR-013). The engine is resolved as a sibling of the program (`Path(__file__).parent / "goal-utils.py"`), which resolves in both the source tree and the `.specify/` mirror.
- **R-04 — Overview performs no engine calls.** FR-007's overview row needs the declared/inferred anchor *identity*, which the identity-resolution rule (owner: `skills/internal/create-team/references/summary-mapping.md` § 10.1 and `create-mode.md` § Schema notes) derives from the definition text. The ownership binding record is shown only in the single-team view, via the engine.
- **R-05 — Report summary is read from the report contract's own segment names.** Owner: `skills/internal/create-team/SKILL.md` § Report contract. Because 0 of 46 live reports carry `## Nested SDD Runs` and only 9 carry `## Verification` (B-06/B-07), every missing segment renders `未记录`; an unrecorded anomalies field is never rendered as "无异常".
- **R-06 — Two display caps, both deterministic and both announcing omissions.** Report names: newest 20 (reverse chronological), with omitted count. Available-slug list on the not-found path: 20, with omitted count. No other cap.
- **R-07 — Ledger aggregation uses the ledger owner's last-event rule.** Input: `items.jsonl`; state value set and last-line-wins are owned by `skills/internal/create-team/references/summary-mapping.md` § 6 / § 6.1 (IL-2). The view reports total lines, per-state current counts, non-terminal current items, and unparseable-line count; it does not write or fold the ledger.
- **R-08 — Exit codes are a closed set.** `0` rendered (including empty archive, overview with corrupt rows, dangling binding) · `2` input error (undeclared option, invalid `--scope`, extra positional; `--target` is not declared) · `3` team not found · `4` definition corrupt · `5` rendered with a degraded engine read. Rationale: each verdict is needed by a distinct test and by the skill's navigation.
- **R-09 — `--scope` handling.** Closed set owner: `shared/definitions/anchor-definitions.md` § Archive Layers. `teams` is serviced; `auto` is serviced only for a single slug whose identity resolves in the team archive (no-slug `auto` is not decidable → exit 2 naming the value); `anchor`/`goals` are refused with an explicit not-applicable message (exit 2). Never silently ignored (FR-005).
- **R-10 — Optional-key labels are limited to schema-named optional keys.** `lifecycle_state`, `anchor_slug`, `focus_target`, `territory`, `preset`, `seats`, `stage_seats`, `config.summary`, `config.reporting-reason` each render `已声明` or `未声明（默认值见 create-mode.md § Schema notes）`. The config block itself renders every declared top-level key; the open key space (B-10) is never forced into a closed catalogue.
- **R-11 — Corrupt versus missing is decided by the filesystem, not the engine.** A slug directory without a readable `team.md`, or with unparseable frontmatter, is exit 4 and a named path; a slug with no directory is exit 3. The overview lists corrupt entries as rows labelled `定义损坏` and never skips them.
- **R-12 — Read-only proof is a content-hash snapshot.** Tests snapshot the fixture tree (paths + sha256) before and after an invocation and assert equality; the contract also asserts the program opens no file for writing (source scan for write-mode opens is not relied on; the behavioural hash is the oracle).
- **R-13 — Fixtures are built per test under `tmp_path`.** A builder module (`tests/fixtures/team_view_fixtures.py`) exposes two helpers the tests share: `build_team(root, slug, *, frontmatter=<dict|raw text>, body=<str|None>, reports=(<name>,<text>)…, items_lines=(<json line|raw>), spine=(<filename>…), corrupt=None)` → the created team directory, and `snapshot(root)` → `{relative_path: sha256}` for the read-only oracle. Every fixture tree is created inside pytest `tmp_path`; no fixture is committed under `.specify/teams/`. Precedent: `tests/fixtures/line_fixtures.py`.
- **R-14 — The `--target` conflict is decided before the program runs.** The skill/command treats `view … --target …` as a mode/parameter conflict and asks for clarification; the program declares no `--target` option, so an undeclared option is refused with exit 2 if it ever reaches it.

## Resolved unknowns

- **U-01 — Does adding `view` to `argument-hint` change an engine contract?** No: `command-mode` accepts `anchor|goal` only (B-19). Resolved.
- **U-02 — Can the program use PyYAML?** No: not a declared dependency; RS-001 requires stdlib only. Resolved by R-02.
- **U-03 — Does a live team exercise the legacy `goal_slug` spelling?** No (B-02); the branch is required by FR-020 and is covered by a fixture. Resolved.
- **U-04 — Do live reports carry the current contract's segments?** Mostly not (B-06/B-07); `未记录` is the normal rendering. Resolved.

## Remaining unknowns

None. No `NEEDS CLARIFICATION` marker remains in `requirements.md`.
