# Research — 108-team-view-degradation

**Purpose**: record the measurements this plan stands on and the design points it resolved, so later stages re-measure instead of inheriting claims. Every number below was taken at plan time (2026-11-26, worktree `108-team-view-degradation`, HEAD `4e5b8a11d`, baseline commit `54c6efa8c`) with the command named in its row.

## M1 — In-repo corpus composition (measured)

Command: a Python pass over `.specify/teams/*/runs/*` applying the FR-001 closed grammar (five timestamp forms with strict calendar validation + suffix `(?:-[0-9a-f]{4})?-(?:report|stage)\.md`) and the FR-003 order.

- 46 files total: **41 run reports** (28 compact-conforming `^\d{8}T\d{6}Z-report\.md$`, 13 parseable-non-conforming report-style), **3 auxiliary artifacts**, **2 residue**.
- Auxiliary: `20261008T214100Z-seat-result.md`, `20261008T070532Z-verification.md`, `20261008T084144Z-verification.md`.
- Residue: `2026-10-06-S1-judgment-contract.md`, `2026-10-07-progress-snapshot.md` (date prefix only, no time → no parseable leading timestamp).
- Per-team report styles:
  | team | reports | conforming | non-conforming style |
  |------|---------|-----------|----------------------|
  | `viz-skill-arena` | 5 | 0 | `YYYY-MM-DDThh-mm-ssZ-report.md` |
  | `draw-two-layer-structure` | 7 | 0 | `YYYY-MM-DDThhmmssZ-report.md` |
  | `draw-diagram-interactive` | 1 | 0 | `YYYYMMDDThhmmZ-report.md` |
  | `session-driven-self-improvement` | 5 | 5 | plus 2 auxiliary + 2 residue |
- The three all-non-conforming teams contribute exactly the 13 report-style files SC-002 names.
- **Zero** `-<4hex>-report.md` / `-<4hex>-stage.md` names exist in this repo (EP-005); those fixtures are synthesized from the production evidence (A-12).

## M2 — Current reader behavior on the corpus (measured)

- `python3 scripts/python/team-view.py viz-skill-arena --repo-root .` → exit 0; `运行报告: 为空（…/runs）`; `未识别（unrecognized）: <5 names, unbounded>`; `最近报告（latest_report）: 未记录`.
- Same shape for `draw-two-layer-structure` (7 names) and `draw-diagram-interactive` (1 name).
- Overview `最近运行` column for these teams = `未记录`; `session-driven-self-improvement` = `20261008T090000Z`.
- Root cause in source: `REPORT_NAME_RE = ^(\d{8}T\d{6}Z)-report\.md$` (line 143); selection sorts only the narrow matches (lines 925–941); `_latest_report_token` in overview takes `max()` over narrow matches (lines 1122–1131); the `未识别` line joins every name with no bound (line 1473).

## M3 — Current reader behavior on degraded definitions (measured)

Scratch fixture (`no binding` block, inline `goal`, matrix without `agent`, empty `runs/`, no `items.jsonl`, no spine, `pattern: iteration`):

- `goal-utils.py binding team no-binding-team --json` → exit 2, `{"error": "binding-missing: … carries no binding block; a definition without a complete binding record is uninterpretable (owner / owner_id / origin)"}`; the partial-keys variant names the missing keys (`owner_id, origin`).
- View exit 5 (engine read failure); `绑定（binding）: 不可读（<engine message>）`; `其它声明键: goal`; `名册差异（roster_delta）: 未记录（正文矩阵无 agent 列，两侧名册不可比对）`; `台账: 缺失（<path>）`; spine rendered as plain `缺失`; `goal` never rendered as a named normalization state; no repair pointer anywhere.

## M4 — Healthy fixture and baseline program (measured)

- Fixture built with `tests/fixtures/team_view_fixtures.py` (`default_frontmatter` + default body + two compact-named reports): complete canonical binding, `agent` column present, no `goal` key, no residue, readable reports.
- Current program: exit 0, zero writes (`snapshot()` before == after, 3 files).
- Baseline program materialized with `git show 54c6efa8c:scripts/python/team-view.py` beside copies of `script_interface_cli.py` and `goal-utils.py`: exit 0, **stdout diff lines = 0** against the current program.
- `git cat-file -e 54c6efa8c` succeeds in this checkout; the baseline blob's sha256 equals the current `scripts/python/team-view.py` (`81fad3f9…`), i.e. the referent is exact.

## M5 — Owner readings (cited, never copied)

- Report naming owner: `skills/internal/create-team/SKILL.md` § Report contract — `runs/<UTC-timestamp>-report.md`; the contract is unchanged (A-3: tolerance is read-side).
- Continuous spine layout: `skills/internal/create-team/references/operating-loops.md` § 8 — `iteration` / `parallel` / `serial` teams hold `team.md` + `runs/` only; `continuous` adds `constraints.md` / `STATE.md` / `run-log.jsonl`.
- Pattern value set: `skills/internal/create-team/references/create-mode.md` § Schema notes — `pattern: parallel | serial | iteration | continuous`, **no default declared**; absent pattern therefore has no owner-sanctioned default to apply (FR-008).
- Binding record: `.specify/shared/definitions/anchor-definitions.md` § The Binding Record; reading is engine-only (`goal-utils.py binding`), keys exactly `owner / owner_id / origin`.
- Identity resolution: `anchor_slug` > `goal_slug` > inferred own slug (existing, unchanged; FR-014).
- Ledger: `skills/internal/create-team/references/summary-mapping.md` § 6 (IL-2), untouched.
- Missing-state vocabulary: four members `缺失` / `为空` / `不可读` / `未记录` (103 FR-015 discipline, carried; the live table moves to this feature's `view-labels` contract).

## M6 — Existing test surface to preserve or extend (measured)

- `tests/unit/test_team_view_parsers.py` (328 lines): frontmatter subset, matrix, report segments, ledger, bounded excerpt.
- `tests/contract/test_team_view_program_contract.py` (220 lines): CLI surface, exit set, envelope keys (exact ten-key set), read-only source scan.
- `tests/integration/test_team_view_program.py` (360 lines): six groups, missing states, legacy goal_slug, archived, ledger, roster mismatch, report cap, overview, not-found, corrupt, snapshot.
- `tests/contract/test_team_view_command.py` (354 lines): template/docs four-mode tables, routing samples, per-tool copies.
- No existing test pins the `未识别` line content, the `roster_delta: 未记录` text, or a residue-bearing exit code — the 108 amendments therefore extend rather than contradict the 103 test surface (the envelope key set and CLI surface stay untouched).

## M7 — Toolchain baseline (measured)

- `python3 scripts/python/sync-mirrors.py --check` → rc 0, all six mirror families byte-identical (templates 23 / skills 394 + 139 / agents 20 / scripts 133 / shared 117 files).
- `python3 scripts/python/regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.`
- `pytest` availability: `/usr/local/bin/python3` → pytest 8.4.2; the profile `python3` on PATH imports no pytest. The implement stage MUST pass `SPECKIT_PYTHON=/usr/local/bin/python3` to `scripts/bash/run-tests.sh`.

## M8 — Gate baselines (measured)

- `flow-class-check.py --action lookup --unit-id "spec:108-team-view-degradation"` → `flow_class: execution` (no expression-class gates).
- `pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage requirements --repo .` → `decision=pass errors=0 advisories=0`, `fr=25 sc=8`.
- `validate-decision-tensions.py --spec .specify/specs/108-team-view-degradation` → N/A form accepted (the 103 precedent validates the same shape).

## Resolved design points

### R-1 — Closed timestamp grammar, leading position only

One compiled token grammar with five alternatives, longest-first (ISO colon form, ISO dashed form, ISO compact form, compact six-digit, compact four-digit), followed by strict `datetime.strptime` validation per form; an unparseable or calendar-invalid candidate is **not** a timestamp. Only a stamp at the **start** of the file name counts (A-17 rejects fuzzy matching). Suffix grammar: `^(?:-[0-9a-f]{4})?-(?:report|stage)\.md$` (lowercase hex exactly four, role word exactly `report` or `stage`).

### R-2 — Classification order (fixed and decidable)

(1) no valid leading stamp → residue; (2) valid stamp + report suffix → run report; (3) valid stamp + any other remainder → auxiliary artifact. `.md` is not a condition for residue; auxiliary artifacts never compete for latest and are never counted as residue. One function produces `(kind, timestamp)` per name; nothing else classifies.

### R-3 — Latest and normalization

Latest = maximum parsed UTC timestamp. Ties = file name lexicographic ascending first (matches the current stable order for compact names). The normalized value is `strftime("%Y%m%dT%H%M%SZ")` from the parsed datetime and is the single value used by `as_of.latest_report_timestamp` and the overview column (SC-006). No mtime or content inference; no fallback to an older conforming report when a newer parseable one exists.

### R-4 — Residue presentation bound

The residue line carries the total, up to **3** example names and the omitted count (`EXAMPLE_CAP = 3`); auxiliary artifacts get the same bounded form. No unbounded transcription (the current unbounded join is the anti-pattern this replaces).

### R-5 — Uncertainty predicate and its degradation

`runs/` exists (readable) and residue count ≥ 1 → latest is **unprovable** → `report-recognition-uncertain` active, exit 5. `runs/` missing/empty, or files that all carry parseable stamps (auxiliary only) → no uncertainty. When reports exist, the report list still renders and the residue line discloses the uncertainty; when only residue exists, the run-report state renders `未识别（unrecognized）—— 仅残留，最新不可确定` (never `为空` / `缺失`).

### R-6 — Overview uncertainty is inline, never a reason

The overview shares the classifier and the normalized value; a residue-bearing row appends `（report-recognition-uncertain：残留 N）` to its latest cell. The overview issues no degradation reason and keeps the existing `0/2` exit domain.

### R-7 — Degradation carriers reuse existing fields

Top-level envelope keys stay the measured ten (EP-007). Reasons ride the existing `errors[]` array with `code` values from the closed set; `degraded` is true iff ≥1 reason; `as_of.latest_report_timestamp` carries the normalized token or null. The human rendering appends a non-group degradation block naming every active reason; the six-group body is untouched (C-105/C-308).

### R-8 — Binding and goal states present, never infer

Binding readability is engine-only; an unreadable binding keeps the engine's verbatim reason and adds two repair pointers (`/speckit.team modify`, `goal-utils.py bind`; owner: `anchor-definitions.md` § The Binding Record). Any declared `goal` key renders a named normalization state (`goal 需归一为 anchor_slug`) with repair pointers (`/speckit.team modify`; derive via `goal-utils.py migrate`); identity resolution stays `anchor_slug` > `goal_slug` > inferred and is never changed by the suggestion.

### R-9 — Matrix anomaly and roster not-comparable

A missing or duplicated `agent` column makes the matrix group carry `形态异常` and name the defect; parsed rows still render in full. `roster_delta` renders `不可比对（not comparable）` with the reason (never `未记录`); frontmatter members stay fully listed; `seats` / `stage_seats` keep their declared/undeclared disclosure with the owner pointer.

### R-10 — Ledger consequence and spine applicability

`items.jsonl` missing keeps the `缺失` state and appends its consequences (no aggregate counts, no non-terminal signal); zero-line files stay `为空`. Spine absence is judged by the declared pattern: `continuous` → real gap; declared non-`continuous` → `按声明 pattern 不适用` with the `operating-loops.md` § 8 pointer; pattern undeclared → applicability undeterminable with the `create-mode.md` § Schema notes pointer (no invented default, because the owner declares none).

### R-11 — Label vocabulary: one live owner

`contracts/view-labels.contract.md` becomes the single live owner of the rendering label table (carried members + new members: `未识别（unrecognized）` residue form, `辅助产物（auxiliary）`, `不可比对（not comparable）`, `按声明 pattern 不适用`, `适用性不可判定`, the `goal 需归一为 anchor_slug` state form). `103-team-view/data-model.md` § Rendering Line Types stays untouched as a dated record; nothing cites it as a live owner any more. The reason ids' closed set and exit map live in the program contract and are referenced, not re-tabled, here.

### R-12 — One engine, one recognition entry

A single `classify_runs()` produces the runs inventory for both the single view and the overview; the old narrow regex and the overview's own `max()` helper are removed. A source scan asserts exactly one classifier definition and one timestamp grammar; a behavioral assertion checks overview and single values agree (SC-006).

### R-13 — Healthy fidelity is measured, not promised

The test materializes the baseline program (`git show 54c6efa8c:…`) beside the current `script_interface_cli.py` and `goal-utils.py` (the latter zero-modified by RS-004), runs both on the same healthy fixture and compares stdout bytes and exit codes. The git object's presence is asserted explicitly (EP-003), not skipped silently.

### R-14 — Three-surface consistency is pointer-shaped

`docs/reference/commands/team.md` (View Mode), `skills/internal/view-team/SKILL.md` (error navigation row 5) and the program's declared exit codes each name both reason ids and the owner contract path; a contract test asserts those tokens on all three surfaces. The closed set and mapping themselves are defined only in the program contract (FR-020 permits this pointer form).

### R-15 — Shape-change boundary

This feature changes no report-naming rule and no `team.md` schema, so there is nothing to migrate: every compact name that conformed before still conforms, and all 28 + 13 report-style corpus names classify as reports (SC-002 coverage). A contract clause (C-108) states the migration/refusal obligation for any future proposal that does change shape: it MUST ship migration or deterministic refusal before merge.

## Re-measure list for `/speckit.tasks` / `/speckit.implement`

1. Corpus composition (M1) — the counts anchor SC-002 fidelity; re-run before writing the corpus-replica fixture.
2. `git cat-file -e 54c6efa8c` and the baseline blob sha256 (M4) — the fidelity test depends on the object being present in the implement checkout.
3. `sync-mirrors.py --check` and `regen-command-copies.py --check` (M7) — re-take the "no NEW drift" baseline immediately before editing.
4. `SPECKIT_PYTHON=/usr/local/bin/python3` pytest availability (M7) — required by the runner on this host.
5. The 103 test surface (M6) — confirm none of the four files changed since plan time before claiming the regression comparison.
6. The engine's `binding` messages (M3) — assert their exact text in the degraded fixture is still produced by `goal-utils.py`.
