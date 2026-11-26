# Contract — Per-Group Presentation Obligations

**Path**: implemented in `scripts/python/team-view.py`; pinning `tests/integration/test_team_view_degradation.py` (behavioural) and `tests/contract/test_team_view_degradation_contract.py` (text/pointer scans).
**Rule owners cited, never restated**: binding record `shared/definitions/anchor-definitions.md` § The Binding Record; team schema and pattern value set `skills/internal/create-team/references/create-mode.md`; continuous spine `skills/internal/create-team/references/operating-loops.md` § 8; ledger fold `skills/internal/create-team/references/summary-mapping.md` § 6.1 (IL-2); label vocabulary `contracts/view-labels.contract.md`.

**C-301** Binding readability and repair pointers.

Binding facts are readable only when the engine read succeeds and all three keys (`owner` / `owner_id` / `origin`) are present. When unreadable, the identity group MUST present `不可读` with the engine's verbatim reason (distinguishing "no binding block" from "missing key(s) <names>"), MUST NOT fill a default or infer from other fields, and MUST append the sanctioned repair pointers: `/speckit.team modify` (definition repair entry) and the engine write face `goal-utils.py bind`, with the record-meaning owner `anchor-definitions.md` § The Binding Record. The view itself MUST NOT execute any repair. (FR-011, FR-012)

**C-302** Goal declaration state (present, never guess).

The named state appears only in the identity group's degraded cases, decided by two conditions: (a) the declared `goal` value does **not** pass the shared identity grammar (`shared/definitions/goal-definitions.md` § Identity grammar — inline long text and any other non-slug value), or (b) the binding is unreadable (C-301's `不可读`; normalization then rides the same `/speckit.team modify` repair). When (a) or (b) holds, the identity group MUST present `goal 需归一为 anchor_slug` with the repair pointers (`/speckit.team modify`; derive an anchor definition via `goal-utils.py migrate`). A slug-form value under a readable binding is healthy (FR-022): the key stays visible in the declared-keys line exactly as the baseline renders it and MUST NOT add a state line. In every case identity resolution keeps the existing order (`anchor_slug` > `goal_slug` > inferred own slug); the suggestion MUST NOT change the presented identity type and MUST NOT trigger any migration; the key is never silently skipped because `anchor_slug` is declared; `goal` → slug inference stays forbidden (C-309). The binding state (C-301) is independent: neither state substitutes for the other, and both appear side by side when both conditions hold. (FR-013, FR-014, FR-022)

**C-303** Matrix anomaly and roster comparability.

When the `## Static Structure` matrix lacks the `agent` column (or declares it twice), the static group MUST carry `形态异常` and name the defect, while every parsed matrix row is still presented in full. `roster_delta` MUST render `不可比对（not comparable）` with the reason — never `未记录` — and the frontmatter members MUST be listed in full; `seats` / `stage_seats` keep their declared/undeclared disclosure with the default pointer. A matrix that cannot parse at all (`不可读` / `缺失` / `为空`) yields `不可比对` with that reason. No group may become a silent empty section. (FR-015, FR-016)

**C-304** Ledger missing state carries consequences.

A missing `items.jsonl` MUST render `缺失` with the path and the consequences (no aggregate counts, no non-terminal signal); MUST NOT be replaced by zero values or an empty aggregate. The `为空` (present but zero lines) and `不可读` distinctions are preserved. (FR-007)

**C-305** Spine applicability follows the declared pattern.

For the three continuous-spine files (`constraints.md`, `STATE.md`, `run-log.jsonl`): a `continuous` team's absence is a real gap rendered `缺失`; a declared non-`continuous` team's absence MUST be rendered as `按声明 pattern 不适用` with the owner pointer `operating-loops.md` § 8; an undeclared pattern makes applicability `适用性不可判定`, and the output MUST disclose that the schema owner declares no pattern default (`create-mode.md` § Schema notes). Present files are listed as today; a partially present spine mixes the two forms per file. (FR-008)

**C-306** Latest-group unreadable state.

An unreadable latest report renders the report name with `不可读` and its path at the top of the latest group; the group's field lines MUST render `不可读` rather than silently falling back to `未记录`. This is a file-level state, not a degradation reason. (FR-009, FR-018)

**C-307** Four-state discipline on every new surface.

`缺失` / `为空` / `不可读` / `未记录` keep their existing meanings and apply to the new surfaces: residue, auxiliary artifacts, an unreadable latest report and pattern-inapplicable spine files are expressed with vocabulary from `view-labels.contract.md`, never collapsed into each other and never rendered as `0`. (FR-010)

**C-308** Additive output only.

The six group headings and every existing line remain; 108's states are additions or state-expression changes required by C-301…C-307. The view-team skill's re-emission rule (program stdout re-sent verbatim as the session's own message, degradation explanation outside the group body) MUST keep holding; the degradation explanation MUST NOT replace, trim or rewrite the six-group body. (FR-025)

**C-309** No inference.

Binding values, `goal` → slug, latest report and roster differences MUST all be read facts or named states with reasons; no guessed value and no filled default may appear anywhere in the output. (FR-019)
