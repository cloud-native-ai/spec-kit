# 094 analyze-repair — round 1 findings closure (2026-11-09)

Authority: `notes/analyze-round1-findings.md` (read in full). Ordering followed: C-01 → H-02 → H-03+H-04 →
M-01…M-05 + L-01 → H-05 → H-01 → L-02. No framework source touched; no other line's worktree touched.

## 1. Findings — disposition by ID

| ID | Disposition | What changed | Where |
|---|---|---|---|
| C-01 | closed | FR-006 rewritten around a decidable discriminator measured on the engine itself: `/speckit.feedback` and `/speckit.plan` return `flow_class: execution` with `source: ledger`; `/speckit.nonexistentcommand` returns `flow_class: execution` with `source: default` and `marker: 未声明·按默认` — both exit 0. Membership in the command family is therefore decided by `source`, not by `flow_class`. A9 restated in the same terms. | `requirements.md` FR-006, A9 |
| H-01 | closed (by rewriting the clauses' citation groups, not by weakening the gate) | All 111 contract clauses now end with exactly one trailing citation-group line `(FR-…)` in the grammar owned by `shared/definitions/contract-clause-definitions.md` § 引用组. Coverage moved from 26/42 uncited to **42/42 cited**. Prose is byte-identical apart from the added groups. GATE-6 keeps all three lanes and now names why the FR lane exists. The one-shot repair tool lives in git-ignored scratch: `.specify/.tmp/s092-repair/add_cites.py` (idempotent; two consecutive runs reported `md5sum -c` OK). | `contracts/*.md` (5 pages), `tasks.md` GATE-6 |
| H-02 | closed | One owner: FR-025 states the closed set `goal` / `teams` / `auto` (`spec` 与 `global` 一并出域). FR-008 and A1 now point at FR-025 instead of restating a competing set. Ruling recorded in `## Clarifications` § Session 2026-11-09 (Q13) — the deciding argument is semantic, not majority: `{global, auto}` cannot express the two distinct write targets (`.specify/goal` vs `.specify/teams`), which is exactly what the goal verbatim asks for. | `requirements.md` FR-025, FR-008, A1, Clarifications |
| H-03 | closed | The two `### Assumptions` blocks merged into one contiguous A1–A11 block; every line preserved. Both set differences (`seg1 \ seg2`, `seg2 \ seg1`) are recorded verbatim in § Notes. | `requirements.md` § Assumptions, § Notes |
| H-04 | closed | Four mis-cites fixed in the merged block: A2 → `FR-006、FR-031`; A3 → `FR-018 / FR-031`; A4 → `FR-024`, `RS-003、RS-004`; and seg-2's A1 ("本阶段不裁 scope 取值名") is **not** merged — it is superseded by the H-02 ruling and recorded as a superseded reading. A6 unified to one reading (M-01). | `requirements.md` § Assumptions, § Notes |
| H-05 | closed | T043 now carries `[blockedBy: T015,T054]` and `[owner: wp03-command-family]`; T054 carries `[blockedBy: T015,T053]`. Partition re-cut: `wp03` absorbs T043 (19 rows, write domain gains `tests/integration/test_parallel_lines.py`), `wp05` gives it up (16 rows). Chain now `… = 15 + 14 + 19 + 8 + 16 + 6 + 2 = 80`. A row cannot be served before its blocker: T043 needs `handoff-decision` (T054). The one residual `validate-tasks` warning is that same edge, now disclosed rather than unexplained. | `tasks.md` T043, T054, Package Map, Package Dependencies, Parallel Opportunities, Parallel Example, DO NOT-2 |
| M-01 | closed | A6 states one reading (085–091 各一对, 089 的 goal slug 为 `script-interface-contract`); SC-003 uses the same reading. | `requirements.md` A6 |
| M-02 | closed | FR-005 `见 FR-032` → `见 FR-031`; RS-003 row `FR-032` → `FR-031`. | `requirements.md` FR-005, RS-003 |
| M-03 | closed | A9 rewritten in `source: ledger` vs `source: default` terms (shares the C-01 measurement). | `requirements.md` A9 |
| M-04 | closed | FR-009 carries the no-lineage prohibition; A11 keeps the rationale and points at FR-009. | `requirements.md` FR-009, A11 |
| M-05 | closed (deliberately not "fixed") | FR-041's double citation of A7 is **left intact**: it is the only anchor for the irreversible 085 removal, and L-01's paragraph removes the ambiguity that made the double-A7 look like a defect. Recorded in § Notes instead of silently de-duplicated. | `requirements.md` § Notes |
| L-01 | closed | One paragraph after `#### E. 判定面与取证` states that all 42 FRs are registered contiguously under `A` (group headings are titles only) and supplies a searchable A–F → FR correspondence that explicitly "不构成第二份清单". | `requirements.md` § E |
| L-02 | closed | Stage record refreshed in both the index row and the feature detail. | `.specify/memory/features.md` (092 row), `.specify/memory/features/092.md` |
| L-03 | **residual** | `team/094-goal-team-parallel/team.md` carries `name: SDD Temporary Team 092`, the same generation name as 085–091 (7 files, measured). C-107's scan surface is `shared/` `skills/` `scripts/` `templates/` `src/`, which does **not** include `.specify/specs/**`, so the scan is not triggered today; whether the generation name should also be rewritten is an implement-stage question, not a requirements one. Reported, not patched. | see § 3 residual risks |

## 2. Gate readings (evidence, `test-evidence/`)

| Gate | Command | Reading | Evidence |
|---|---|---|---|
| requirements structure | `validate-requirements.py` | `status: ok`, 0 error / 0 warning | (stdout, this slice) |
| FR lane | `account-clause-coverage.py --spec-dir …` | `fr-uncovered pass (0) — 42 of 42 FRs cited from citation groups`, exit 0 | (stdout) |
| tasks structure | `validate-tasks.py tasks.md` | `PASS (with warnings)`, 0 error / 1 warning (`T043 → T054`, disclosed in H-05) | (stdout) |
| pre-analyze requirements | `pre-analyze-check.py --stage requirements` | `decision pass errors 0 advisories 86 fr 42 sc 11` | `pre-analyze-requirements-analyze-repair.json` |
| pre-analyze plan | `pre-analyze-check.py --stage plan` | same | `pre-analyze-plan-analyze-repair.json` |
| pre-analyze tasks | `pre-analyze-check.py --stage tasks` | same | `pre-analyze-tasks-analyze-repair.json` |
| decision tensions | `validate-decision-tensions.py --spec .specify/specs/094-goal-team-parallel` | `status: ok`, 7 records, 0 error / 0 warning, exit 0 | `validate-decision-tensions-analyze-repair.txt` |
| decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | `proceed`, fr=42 / tasks=80 (ceilings 120 / 160), exit 0 | `decomposition-tasks-analyze-repair.txt` |

## 3. Residual risks handed to analyze round 2

1. **L-03** — the "Temporary Team" generation name still exists on 8 surfaces (085–092); C-107 does not scan them, so no gate sees it.
2. **H-01 grammar dependence** — the 42/42 reading holds only under the citation-group grammar (last parenthetical of a clause block). A future clause edit that appends a trailing parenthetical without FR ids would silently drop that clause from the lane; the gate asserts the count, not the stability of the grammar.
3. **H-05 partition churn** — `wp03` now carries 19 rows against a 16-row per-package ceiling named in the plan's execution model; the ceiling is a target, not a hard gate, but a reviewer should confirm 19 is accepted or split `wp03` at implement time.
4. **`spec` 出域 blast radius** — FR-025's `goal`/`teams`/`auto` set removes `spec` from the declared value domain; `goal-utils.py --scope choices=` and the 085–091 records still contain `spec`-scoped data, whose handling belongs to the migration rows (C-31…C-52), not to this repair.
