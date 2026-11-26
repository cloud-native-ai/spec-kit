# Data Model — Team View Degradation Hardening (108-team-view-degradation)

**Owner statement**: this file owns the view's **classification and presentation model** added by 108 — the run-file classification result, the runs inventory, the latest-selection record, the residue summary, the degradation-reason record, the binding/goal/spine/roster presentation records, and the program's output shape. It does **not** own: the rendering label vocabulary (visual forms live in `contracts/view-labels.contract.md`), the degradation reason closed set and exit map (live owner `contracts/team-view-program.contract.md`), the report naming rule (`skills/internal/create-team/SKILL.md` § Report contract), the continuous spine layout (`skills/internal/create-team/references/operating-loops.md` § 8), the binding record (`shared/definitions/anchor-definitions.md` § The Binding Record), the team schema (`skills/internal/create-team/references/create-mode.md`), or the ledger fold rule (`skills/internal/create-team/references/summary-mapping.md` § 6.1, IL-2). Upstream semantics are cited, never restated.

## Entities

### C1 — Run File Classification

The result of applying the closed grammar to one regular file name under `runs/`.

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `name` | string | directory entry | Base name only; no path elsewhere in the record |
| `kind` | `report` \| `auxiliary` \| `residue` | derived | Fixed order: no valid leading stamp → `residue`; valid stamp + report suffix → `report`; valid stamp + other remainder → `auxiliary` (C-202) |
| `timestamp` | UTC datetime \| null | parsed from the name | `null` exactly when `kind = residue` |
| `token` | string \| null | derived | Normalized `YYYYMMDDThhmmssZ`, `null` for residue (C-204) |

### C2 — Report Timestamp Grammar

The closed set of accepted leading forms and their suffix grammar. Whatever regex spelling the program uses MUST accept exactly these five forms — `YYYYMMDDThhmmssZ`, `YYYYMMDDThhmmZ`, `YYYY-MM-DDThh:mm:ssZ`, `YYYY-MM-DDThh-mm-ssZ`, `YYYY-MM-DDThhmmssZ` — each followed by `T` + `Z` as written, and MUST reject anything that is not a valid UTC calendar instant (month 13, day 30 of February, hour 24). The suffix after the stamp is `(?:-[0-9a-f]{4})?-(?:report|stage)\.md`; the four hex digits are lowercase and the role word is exactly `report` or `stage`. The grammar is owned here and restated normatively in C-201 of `contracts/report-recognition.contract.md`; the program contains one compiled form.

### C3 — Runs Inventory

One pass over a team's `runs/` directory; the only input to both output modes.

| Field | Type | Source | Rule |
|-------|------|--------|------|
| `state` | `缺失` \| `不可读` \| `已列出` \| `为空` \| `未识别（unrecognized）` | derived | `缺失` = no `runs/`; `不可读` = directory unreadable; `已列出` = ≥1 report; `未识别（unrecognized）` = zero reports and ≥1 residue; `为空` = readable, zero reports, zero residue |
| `reports` | list of C1 | derived | Sorted by parsed timestamp descending, ties by name ascending; the first element is latest |
| `shown` / `omitted` | list / int | derived | First 20 report names + omitted count (carried cap) |
| `auxiliaries` | list of C1 | derived | Sorted by name ascending |
| `residue` | C4 | derived | Present whenever `state` is `已列出` or `未识别（unrecognized）` with residue ≥ 1 |
| `latest_path` | path \| null | derived | First element of `reports`, else `null` |
| `latest_token` | string \| null | derived | C1.token of the latest, else `null` |
| `uncertain` | bool | derived | `residue.count >= 1` (C-206) |
| `unreadable` | bool | derived | The latest report path exists but cannot be read (FR-009 path) |

### C4 — Residue Summary

| Field | Type | Rule |
|-------|------|------|
| `count` | int | Total residue files |
| `examples` | list of names | At most 3, name-ascending |
| `omitted` | int | `max(0, count - len(examples))` |
| `auxiliary_count` / `auxiliary_examples` / `auxiliary_omitted` | int / list / int | Same bounded form for auxiliary artifacts |

### C5 — Latest Selection Record

| Field | Type | Rule |
|-------|------|------|
| `report` | name \| null | Latest report's base name (`null` when none) |
| `token` | normalized `YYYYMMDDThhmmssZ` \| null | Same value in the envelope and the overview cell |
| `tie_break` | literal `name-ascending` | Declared so the rule is visible in the record |
| `uncertain` | bool | Mirrors C3.uncertain; a residue-bearing directory can still name a latest report, but the selection is disclosed as unprovable |

### C6 — Degradation Reason

| Field | Type | Rule |
|-------|------|------|
| `code` | `engine-degraded` \| `report-recognition-uncertain` | Closed set; owner `contracts/team-view-program.contract.md` C-104 |
| `message` | string | Names the fact (which engine read failed; or residue count) |
| `path` | path \| null | The team directory or the runs directory |
| `exit` | `5` | Both reasons map to 5; the exit-code set itself is `0/2/3/4/5` (C-104) |
| `active_reasons` | list of `code` | Every active reason, in stable order (engine reasons first, then recognition uncertainty) |

The record never carries a reason that is not in the set; file-level states (`缺失` / `为空` / `不可读` / `未记录`) never become reasons by themselves (C-104 / C-306).

### C7 — Binding Readability Record

| Field | Type | Rule |
|-------|------|------|
| `state` | `readable` \| `不可读` | Readability is decided by the engine read only |
| `reason` | string \| null | Verbatim engine message (e.g. `binding-missing: … carries no binding block …` or `… is missing the binding key(s) …`) |
| `keys` | map (`owner` / `owner_id` / `origin`) \| null | Present only when readable |
| `repair` | list of pointers | `["/speckit.team modify", "goal-utils.py bind"]`; the record meaning owner is `anchor-definitions.md` § The Binding Record |

### C8 — Goal Declaration State

| Field | Type | Rule |
|-------|------|------|
| `declared` | bool | True iff the frontmatter carries a `goal` key (any value form) |
| `form` | `slug` \| `inline` \| `absent` | Derived: `slug` = the value passes the shared identity grammar (`shared/definitions/goal-definitions.md` § Identity grammar); `inline` = declared with any other value; `absent` = key not declared |
| `state` | literal `goal 需归一为 anchor_slug` \| null | The literal exactly when `form = inline`, or when `declared` and C7's binding state is `不可读`; `null` otherwise (goal absent, or slug-form with a readable binding — healthy, FR-022) |
| `repair` | list of pointers | `["/speckit.team modify", "goal-utils.py migrate"]`; carried only alongside a non-null `state` |
| `identity_unchanged` | bool | Always true; identity resolution is `anchor_slug` > `goal_slug` > inferred (FR-014) and the suggestion never alters it |

### C9 — Roster Comparability Record

| Field | Type | Rule |
|-------|------|------|
| `matrix_state` | `null` \| `形态异常` \| `不可读` \| `缺失` \| `为空` | `形态异常` = missing/duplicated `agent` column while required columns parse; `不可读` = required column problem |
| `matrix_note` | string \| null | Names the defect (`缺列: agent` / `重复列: agent`) |
| `comparable` | bool | True only when matrix parses with an `agent` column and `members` is a list of maps |
| `reason` | string \| null | Present when not comparable; rendered as `不可比对（not comparable）（原因：…）` |
| `only_in_matrix` / `only_in_members` | list of names | Present only when comparable |

### C10 — Spine Applicability Record

| Field | Type | Rule |
|-------|------|------|
| `name` | `constraints.md` \| `STATE.md` \| `run-log.jsonl` | Fixed member of the continuous spine |
| `present` | bool | Existence check only |
| `applicability` | `applicable` \| `not-applicable-by-pattern` \| `undeterminable` | `applicable` for `continuous`; `not-applicable-by-pattern` for declared non-`continuous`; `undeterminable` for an undeclared pattern (the schema declares no default) |
| `pointer` | path + section | `references/operating-loops.md` § 8 for the first two; `references/create-mode.md` § Schema notes for the third |

## Output shape (program)

The default rendering keeps the six group headings and every existing line; 108 adds lines and changes state expressions only where this feature's obligations require it. The trailing degradation block (non-group) lists each active reason. The `--json` envelope keeps its measured ten top-level keys; the additions are nested fields (`persistence.reports.*`, `persistence.ledger.*`, `definition.*`, `static.*`, `latest.*`) and `errors[]` entries — never a new top-level key (C-105).

```json
{
  "tool": "team-view",
  "version": "<framework version>",
  "mode": "overview | single",
  "repo_root": "<absolute path>",
  "scope": {"requested": "teams|auto", "effective": "teams|not-applicable", "note": "string|null"},
  "as_of": {"max_file_mtime_utc": "<ISO-8601 or null>", "latest_report_timestamp": "<normalized token or null>"},
  "overview": {"rows": [/* C3-derived latest + residue marker */], "total": 0, "corrupt_total": 0},
  "team": {"definition": C7/C8 fields, "static": C9 fields, "dynamic": {}, "persistence": C3/C4 fields, "latest": C5 fields, "archive": {}},
  "errors": [{"code": "engine-degraded|report-recognition-uncertain", "message": "…", "path": "…"}],
  "degraded": false
}
```

The envelope remains an internal test surface; the human rendering and the envelope derive from the same extraction so they cannot disagree.

## Invariants

| ID | Invariant | Checked by |
|----|-----------|------------|
| INV-01 | One recognition entry: exactly one `classify_runs()` definition and one timestamp grammar in `scripts/python/team-view.py`; the overview calls the same function | contract source scan + behavioral equality |
| INV-02 | One engine: no second reader, cache, snapshot, index, registry; `goal-utils.py` zero modification | existing + new contract scans |
| INV-03 | Read-only: no file/directory write, no seat dispatch, no run-line registration | existing snapshot test + new three-scenario snapshot |
| INV-04 | Latest = max parsed timestamp; ties by name ascending; normalized token identical in envelope and overview | unit + integration |
| INV-05 | Residue ≥ 1 (readable `runs/`) ⇒ `report-recognition-uncertain`, exit 5; no mtime or content inference | unit predicate + integration exit assertions |
| INV-06 | Healthy predicate fixture ⇒ baseline program and amended program byte-identical stdout, equal exit | integration machine diff |
| INV-07 | Four-state discipline: `缺失` / `为空` / `不可读` / `未记录` never collapsed; a missing fact never renders as `0` | integration assertions |
| INV-08 | Binding / goal / latest / roster facts are never inferred or filled | source scan + degraded fixture |
| INV-09 | Existing lines are preserved; new states append; no reorder or merge of the six groups | healthy byte-fidelity + degraded six-group assertion |
| INV-10 | No shape change: report-naming owner and `team.md` schema untouched; compact names keep conforming | corpus-replica coverage 28 + 13 |

## FR → entity / invariant map

| FR | Entities | Invariants |
|----|----------|-----------|
| FR-001 | C1, C2 | INV-01 |
| FR-002 | C3, C5 | INV-04 |
| FR-003 | C1, C3, C4 | INV-01, INV-07 |
| FR-004 | C4 | INV-07 |
| FR-005 | C3, C4, C6 | INV-05 |
| FR-006 | C3, C5 | INV-01, INV-04 |
| FR-007 | C6 (file-level state; not a reason) | INV-07 |
| FR-008 | C10 | INV-07 |
| FR-009 | C3 (`unreadable`) | INV-07 |
| FR-010 | C4, C6, C10 | INV-07 |
| FR-011, FR-012 | C7 | INV-08 |
| FR-013, FR-014 | C8 | INV-08 |
| FR-015, FR-016 | C9 | INV-07, INV-09 |
| FR-017, FR-018 | C6 | INV-05 |
| FR-019 | C6, C7, C8, C9 | INV-08 |
| FR-020 | C6, C10 | INV-01 |
| FR-021 | — | INV-01, INV-02 |
| FR-022 | — | INV-06, INV-09 |
| FR-023 | C2, C3 | INV-10 |
| FR-024 | — (label owner is the contract) | INV-09 |
| FR-025 | — | INV-09 |
