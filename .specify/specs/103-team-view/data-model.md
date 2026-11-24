# Data Model — Team View (103-team-view)

**Owner statement**: this file owns the view's presentation model — entity set, the six-group field sources, the missing-state vocabulary, the rendering line types and the program's input/output shape. It does **not** own any upstream semantics: the team schema belongs to `skills/internal/create-team/references/create-mode.md`, the binding record and lifecycle to `.specify/shared/definitions/anchor-definitions.md`, report segments to `skills/internal/create-team/SKILL.md` § Report contract, ledger fields/states to `skills/internal/create-team/references/summary-mapping.md` § 6, and the archive layers to `.specify/shared/definitions/goal-definitions.md` / `anchor-definitions.md` § Archive Layers.

## Entities

Field types shown in E1–E9 are the **view's own presentation schema**. Where a field mirrors an upstream value, the `Source` / `Rule` cell names the owner; where a type is a view-authored taxonomy (`kind`, `reports_state`, `items_state`, `roster_delta`, `nested_runs`, `state`), the vocabulary is owned by § Rendering Line Types, not by the upstream owner.

### E1 — View Request

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `mode` | `overview` \| `single` | derived | No positional slug → `overview`; one positional slug → `single`; more than one → input error (exit 2) |
| `slug` | string \| null | CLI positional | Exact match only; never prefix/fuzzy (FR-005) |
| `scope` | `teams` \| `auto` \| other declared value | CLI `--scope` | Default `teams`; `auto` is serviced only for `single` whose identity resolves in the team archive; `anchor`/`goals` and no-slug `auto` are refused with a named not-applicable message (exit 2) (FR-005, R-09) |
| `spec_dir` | path \| null | CLI `--spec-dir` | Forwarded to engine reads that accept it; never decides a landing point (FR-005) |
| `json` | bool | CLI `--json` | Internal envelope for tests; not a user-facing format (A-5) |
| `repo_root` | absolute path | CLI `--repo-root` or derived from the program's own resolved path | Framework rule: self-location fires on a literal `.specify` component of its own path (Two Hats, `shared/definitions/dogfooding-definitions.md` § 2.1) |

### E2 — Team Definition Facts

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `name` / `slug` / `description` | string \| `未记录` | `team.md` frontmatter | Absent → `未记录`; never fabricated (FR-008) |
| `lifecycle` | `active` \| `archived` + `declared` flag | frontmatter `lifecycle_state` | Absent → `active` read from the owner's default (`create-mode.md` § Schema notes), rendered as `未声明 → active` (FR-008, FR-020) |
| `binding` | `{owner, owner_id, origin}` \| `不可读` | engine `binding team <slug> --json` | Never parsed from the file (FR-008, RS-004); a non-zero engine exit → the group marks `不可读` with the engine's message and the run is degraded (exit 5) |
| `anchor_identity` | `{value, kind}` where `kind ∈ declared(anchor_slug) \| legacy(goal_slug) \| inferred(own slug)` | frontmatter + identity-resolution rule (owner: `create-mode.md` § Schema notes / `summary-mapping.md` § 10.1) | The **resolution order and inferred value** are owner-owned; the three `kind` words are view-authored presentation labels (the owner types the ledger's identity `explicit`/`inferred`, a different domain). Legacy/inferred MUST be disclosed, never normalized (FR-008, FR-020). |
| `handoff_ref` | path \| `未声明` | frontmatter | Rendered in group 6 (archive references) (FR-013) |
| `legacy_or_unknown_keys` | list of key names | frontmatter keys outside the schema | Disclosed as declared facts, never interpreted (B-09; A-8) |

### E3 — Static Structure View

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `matrix_rows` | list of `{role, stage, type, agent, lifecycle, responsibility}` | body `## Static Structure` table | Every data row is rendered; missing/duplicate required columns → section `不可读` (FR-009) |
| `members` | list of `{agent, role, lifecycle, territory?, blockedBy?}` | frontmatter `members` | Complete coverage; absent list → `未声明` (one live team has no `members`, B-09) |
| `seats` | map \| `未声明` \| `形态异常` | frontmatter `seats` | Declared entries rendered; a non-block-map shape is `形态异常`, never repaired (A-8) |
| `stage_seats` | map \| `未声明` \| `形态异常` | frontmatter `stage_seats` | Each entry renders `seats[]` and `max_parallel` as declared (FR-009) |
| `roster_delta` | `{only_in_matrix: [agent], only_in_members: [agent]}` | derived | Both sides presented; no adjudication (A-18) |
| `type_source` | literal `body-matrix` | derived | Type is read from the body matrix only; frontmatter carries no type (A-18) |

### E4 — Dynamic Structure View

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `pattern` | `parallel` \| `serial` \| `iteration` \| `continuous` \| `未记录` | frontmatter `pattern` | The four value members are owned by `skills/internal/create-team/references/conceptual-model.md`; `未记录` is the view's missing-state label. Absent is recorded, not guessed (FR-010). |
| `config_declared` | ordered list of `{key, value_text}` | frontmatter `config` top-level keys | Every declared key/value is rendered verbatim (normalized, not interpreted); the key space is open (B-10) |
| `config_absent` | bool | derived | No `config` block → the whole block renders `未声明（默认值见 create-mode.md § Schema notes）` |
| optional-key flags | per key: `已声明` \| `未声明（默认值见 create-mode.md § Schema notes）` | frontmatter | Closed set limited to schema-named optional keys: `lifecycle_state`, `anchor_slug`, `focus_target`, `territory`, `preset`, `seats`, `stage_seats`, `config.summary`, `config.reporting-reason` (R-10) |
| `focus_target` | `T-<nnn>` \| `未声明` | frontmatter | Rendered as declared; view does not validate or resolve it against the anchor (that is run's duty) (FR-010, A-7). |

### E5 — Persistence Inventory

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `team_dir` | path | derived | Always rendered (the directory exists by construction of the single-team path) |
| `reports` | `{total, shown: [filename], omitted, unrecognized: [filename]}` | `runs/*-report.md` | Reverse chronological by filename timestamp; newest 20 shown; omitted count reported; non-conforming filenames listed as `未识别` and never silently dropped (FR-011, R-06) |
| `reports_state` | `缺失` \| `为空` \| `已列出` \| `不可读` | derived | No `runs/` → `缺失`; directory with 0 reports → `为空`; unreadable report is counted and does not interrupt (FR-011, FR-015) |
| `items` | `{state, total_lines, bad_lines, by_state, non_terminal: [{item_id, state}]}` | `items.jsonl` | Existence, line count, folded current-state counts (owner rule IL-2, `summary-mapping.md` § 6.1) and non-terminal items; unparseable lines counted as `bad_lines` and disclosed (FR-011, FR-015) |
| `items_state` | `缺失` \| `为空` \| `已聚合` \| `不可读` | derived | Zero-line file is `为空`, never `缺失` (B-04) |
| `spine` | per file `{name, state}` for `constraints.md` / `STATE.md` / `run-log.jsonl` | team directory | Presence check only; content not summarized (FR-011) |
| `summary_delivery` | `{declared_dir, source}` \| `未声明` | `config.summary.delivery_dir` else identity-derived path | Render the declared value; when absent render `未声明` plus the owner pointer — the default is never invented (FR-011) |

`reports_state` and `items_state` are **view-owned presentation states** (members in § Rendering Line Types); the ledger's state members and last-event rule remain owner-owned (`summary-mapping.md` § 6.1, IL-2), and the report segment names remain owned by `create-team/SKILL.md` § Report contract.

### E6 — Latest Run Summary

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `latest_report` | filename \| `未记录` | newest recognized report | Selected by filename timestamp, not mtime (FR-012) |
| `outcome` | string \| `未记录` | header verdict segment | Missing → `未记录` (FR-012) |
| `target_assignment` | line \| `未记录` | `**Target 指派**` | Missing → `未记录` (FR-012) |
| `result_summary` | excerpt \| `未记录` | `## Result Summary` | First 10 non-empty lines / 800 chars, whichever hits first; truncation marker `…（截断）`. The 10/800 bound is this view's display cap (A-4 permits a cap with omission notice), not a report-owner rule (FR-012, R-05). |
| `verification` | `{present, excerpt}` | `## Verification` | Missing → `未记录`; present → same bounded excerpt rule (FR-012) |
| `nested_runs` | list of `{anomalies}` \| `未记录` \| `本次无嵌套 SDD 调用` | `## Nested SDD Runs` | Missing section → `未记录`; declared-none → the section's own none declaration; an unrecorded anomaly is never rendered as "无异常" (FR-012) |
| `ledger_signal` | `{non_terminal_count, bad_lines}` | E5 | Rendered alongside the report summary as the remaining-abnormality signal (FR-012) |

### E7 — Archive References

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `handoff_ref` | path \| `未声明` | frontmatter | Identity reference only (FR-013) |
| `anchor` | `{identity, lifecycle, criteria_count, targets: [{id, statement, status}], dangling_reason}` \| `不可读` | engine `list --json` + `targets <anchor> --list --json` | Identity/lifecycle/criteria count/targets only; no objective or criteria body copied; unresolvable → `悬空（dangling）` + reason (FR-013) |
| `anchor_pointer` | literal `/speckit.anchor view` | constant | Content lives behind the pointer (FR-013) |

### E8 — Overview Row

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `slug` | directory name | `.specify/teams/*/` | Sort key, ascending (FR-007) |
| `name` | frontmatter \| `未记录` | `team.md` | — |
| `pattern` | frontmatter \| `未记录` | `team.md` | — |
| `lifecycle` | `active` \| `archived` (declared flag) | `team.md` | Absent → `active` per owner (FR-007) |
| `anchor_identity` | declared/legacy/inferred + value | `team.md` | Disclosed (FR-007) |
| `updated` | date \| `未记录` | `team.md` | — |
| `latest_run` | timestamp \| `未记录` | newest report filename | Missing → `未记录` (FR-007) |
| `state` | `ok` \| `定义损坏` | filesystem | No readable `team.md` → the row stays in the list, labelled `定义损坏` with its path; never skipped (FR-006, Edge Cases) |

Overview rows never change the process exit code: a corrupt row is rendered under exit `0`, while exit `4` applies only to the single-slug path (C-28). The quickstart's second corrupt variant (unparseable frontmatter) follows the same split and is pinned by the same test pair (`::test_corrupt_definition_is_not_not_found` + `::test_overview_lists_every_team_sorted`).

### E9 — View Envelope (program output)

```json
{
  "tool": "team-view",
  "version": "<framework version>",
  "mode": "overview | single",
  "repo_root": "<absolute path>",
  "scope": {"requested": "teams|auto", "effective": "teams|not-applicable", "note": "string|null"},
  "as_of": {"max_file_mtime_utc": "<ISO-8601 or null>", "latest_report_timestamp": "<token or null>"},
  "overview": {"rows": [E8], "total": 0, "corrupt_total": 0},
  "team": {"definition": E2, "static": E3, "dynamic": E4, "persistence": E5, "latest": E6, "archive": E7},
  "errors": [{"code": "team-not-found|definition-corrupt|input-error|engine-degraded", "message": "…", "path": "…"}],
  "degraded": false
}
```

The envelope is an internal test surface (A-5): it is not a second user-facing format and no other program may consume it as a contract. The default (non-`--json`) output is the human-facing rendering; the envelope and the rendering are derived from the same extraction so they cannot disagree.

## Rendering Line Types (closed set)

**Label vocabulary (owned here)**: every state or declaration label the rendering emits MUST be a member of this table; no other label may stand for the same distinction.

| Label class | Members | Meaning |
|-------------|---------|---------|
| Missing-state | `缺失` / `为空` / `不可读` / `未记录` | file/dir absent · present but zero entries · present but parse failed · upstream segment not recorded. Never collapsed into each other; never rendered as `0`. |
| Declaration | `已声明` / `未声明` | an optional key is present / absent. The `未声明` form always carries the owner pointer for the default. |
| Derived state | `定义损坏` / `形态异常` / `悬空（dangling）` / `未识别` / `已列出` / `已聚合` / `本次无嵌套 SDD 调用` / `未声明 → active` | view-owned presentation states: corrupt definition (single mode exit 4, overview row) · malformed declared shape (e.g. non-block `seats`) · binding anchor unresolvable · non-conforming report filename · reports listed · ledger folded · the nested-runs section's own none declaration · lifecycle absent with the owner default applied. |

| Line type | Form | Used in |
|-----------|------|---------|
| Group heading | `## <n>. <中文组名>（<English group name>）` | groups 1–6 |
| Field line | `- <label>: <value>` | every group |
| Declared/undeclared | `<label>: 已声明 (<value>)` / `<label>: 未声明（默认值见 <owner path> § <anchor>）` — the concrete instance this view emits is `未声明（默认值见 create-mode.md § Schema notes）` | optional keys |
| Three-state fact | `<label>: 缺失 (<path>)` / `<label>: 为空 (<path>)` / `<label>: 不可读 (<path>；<reason>)` / `<label>: 未记录` | all groups |
| Table | GFM table with the group's declared columns | overview, static matrix, targets, ledger counts |
| As-of | `as-of: <max_file_mtime_utc>（文件时间；非实时探测）` | single view and overview |
| Error | `team not found: <slug>` (STR-001) / `定义损坏: <path>` / `No teams found` (STR-002) | error paths |

The missing-state subset is closed at four values and closed against substitution; a zero value is never rendered for a missing fact (FR-015, A-8). The derived labels are view-authored presentation vocabulary — none of them is an upstream enum: `定义损坏`/`悬空` are view states over owner facts, and `未声明 → active` records that the owner's default was applied.

## Invariants

| ID | Invariant | Checked by |
|----|-----------|------------|
| INV-01 | One view run writes no file, creates no directory, dispatches no seat and registers no run line. | path+sha256 snapshot before/after (FR-004, SC-002) |
| INV-02 | Binding and anchor facts come only from `goal-utils.py binding` / `list` / `targets --list`; no second parse of the binding record or Target semantics. | contract + source scan for the three actions |
| INV-03 | Missing / empty / unreadable / unrecorded are never collapsed; no fabricated zero. | fixture assertions (FR-015, SC-006) |
| INV-04 | Deterministic ordering: overview slugs ascending; reports reverse chronological by filename timestamp; ledger last-event by `ts` then file order. | fixture assertions |
| INV-05 | Slug resolution is exact; no prefix/fuzzy match. | fixture with a near-miss slug |
| INV-06 | Corrupt definition (dir exists, `team.md` missing/unreadable) is exit 4 and a named path; not-found is exit 3. | fixture pair |
| INV-07 | Latest-report summary is bounded; old reports are names only; omissions are counted. | fixture with >20 reports and long segments |
| INV-08 | As-of is declared from file timestamps; no real-time claim. | rendering assertion |
| INV-09 | An unrecorded anomalies field never renders as "无异常". | fixture with a report lacking `## Nested SDD Runs` |
| INV-10 | Body matrix vs frontmatter roster mismatch is presented on both sides, never adjudicated. | fixture with a deliberate mismatch |
| INV-11 | No user-facing machine-readable format; `--json` is internal. | contract assertion on the default output + docs |
| INV-12 | Legacy `goal_slug` and inferred identity are disclosed, never normalized or migrated. | fixture with `goal_slug` only |
| INV-13 | Archived teams render normally with an `archived` label; view never refuses them. | fixture |
| INV-14 | The program never invokes `run-checks` and never renders a `blocked` verdict. | source scan + contract |

## FR-021 Fixture Map

| Fixture | Covers | Test file |
|---------|--------|-----------|
| Complete team (definition + 2 reports + ledger) | six groups, full member/report coverage (SC-001) | `tests/integration/test_team_view_program.py` |
| Minimal team (definition only) | `缺失` states for runs/ledger/spine, no fabricated zeros | same |
| Unknown slug + empty archive | STR-001 / STR-002 paths (SC-004) | same |
| Corrupt definition (dir without `team.md`) | exit 4, named path, overview row (SC-004) | same |
| Missing optional artifacts + latest report without `Verification` / `Nested SDD Runs` | three-state + `未记录` (SC-006) | same |
| Legacy `goal_slug` | legacy identity disclosure (FR-020) | same |
| Archived lifecycle | archived label, not refused (FR-020) | same |
| Ledger bad line | bad-line count, non-interrupting (FR-015) | same |
| Roster mismatch / >20 reports | INV-07 / INV-10 | same |
| Read-only snapshot | SC-002 | same |
| Routing samples + docs stale literal | SC-003 / SC-005 | `tests/contract/test_team_view_command.py` |
| CLI surface / exit codes / no run-checks | FR-014 / A-7 | `tests/contract/test_team_view_program_contract.py` |
