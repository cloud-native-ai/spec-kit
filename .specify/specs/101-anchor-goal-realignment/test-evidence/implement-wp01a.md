# Implement evidence — WP-01a (T006–T015)

Run `r20261112T064607Z-b101`; feature `101-anchor-goal-realignment`; package WP-01a
(tasks T006–T015); stage base commit `7920dc7b5`.

**Comparison baseline (E2, not re-run):** `test-evidence/suite-baseline-entry.txt` — rc=1,
8900 passed, 192 pre-existing failure ids, 3 skipped. Every reading below is targeted; a
pre-existing failure id counts as "not regressed" when it is absent from the selected paths of
these runs.

## T006 — owner file move (commit `9d9043502`)

| Field | Value |
|-------|-------|
| Command | `git mv shared/definitions/goal-definitions.md shared/definitions/anchor-definitions.md`; then `git diff --cached --stat -M`; `git show --stat -M --oneline HEAD` |
| rc | 0 |
| Selected paths | `shared/definitions/anchor-definitions.md` |
| Result | rename detected at 100% similarity (`{goal-definitions.md => anchor-definitions.md} | 0`); no content byte changed at this commit |
| Follow readings | recorded in `notes/red-first-evidence.md` (both files' `git log --follow`) |

Correction disclosed: the first attempt staged the move **and** a reconstructed `goal-definitions.md`
in one commit; git then recorded a plain file creation instead of a rename (the old path still
existed with identical content). The commit was re-made (it was local, unpushed, seconds old) as a
pure rename so the T006 evidence obligation is measurable. T008 recreates the Goal owner from blob
`3e1c0a4f0`, which is what keeps "content changed owner" readable in history.

## T007 — Anchor owner rewrite (FR-001, FR-002, FR-007, FR-008, FR-009, FR-030)

| Field | Value |
|-------|-------|
| Command | heading + terminology assertion over `shared/definitions/anchor-definitions.md` (inline `python3 -`) |
| rc | 0 |
| Selected paths | `shared/definitions/anchor-definitions.md` |
| Result | required headings all present — `# Anchor Definitions Reference`, `## What an Anchor Is`, `### Archive Layers`, `### The Binding Record`, `### Lifecycle`, `## Target Decomposition (目标切片)`, `## Anchor–Team Binding`, `## Terminology Boundaries` → `headings: PASS` |
| G-3 heading assertion | `PASS` — the headings the later `tests/contract/test_anchor_definitions.py` (T064) keys on exist in the owner itself; the store-side half of G-3 is out of this package |
| SC-010 restatement material | each of the four confusable terms has exactly one dedicated table row: `**Anchor** (锚点)` → 1, `**anchoring archive** (锚点档案)` → 1, `**Re-Anchoring** (重新锚定)` → 1, `**action-level Goal** (行动级目标)` → 1; each row states both the referent and what it is NOT |
| Scope ownership | § Archive Layers carries the four-member closed set `anchor` / `teams` / `goals` / `auto`, states the retired member `goal` fails as an invalid value with no alias, and says the engine `--help` cites this section by path |
| Sole-owner split | binding record (three keys) and lifecycle (three values + transition discipline) are declared owned here; the Goal owner is cited by path and MUST NOT restate them |
