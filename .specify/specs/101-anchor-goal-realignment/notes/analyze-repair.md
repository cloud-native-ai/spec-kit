# Analyze round-1 repair — 2026-11-12 (`/speckit.plan` seat, feature 101)

Scope: close HIGH-1, HIGH-2, MEDIUM-1…4, LOW-1…4 from `test-evidence/analyze-2026-11-12.md`
in their owners, plus re-check of the analyze's closure claims and observations O-1…O-4. No code
implemented; no dated record rewritten; no user question raised (every finding had exactly one
reading consistent with the recorded intent).

## Findings

| Finding | Owner(s) and change | Gate / evidence |
|---------|---------------------|-----------------|
| HIGH-1 | `plan.md` § Inherited Blockers re-derived from the six declared dependency artifacts: extraction yields exactly **five** records (`037:SC-016_status` partial, `038:deferred_tasks` = `none`, `042:deferred_tasks` = `none`, `094:SC-001_status` partial, `094:SC-010_status` partial); `074` / `085` contribute none (every status row `pass`, `deferred_tasks=` empty) and no detail page carries a `## Deferred` list item. Each row disposed with evidence: 2 `resolved`, 3 `not-applicable`, none `inherited`. `research.md` R-13, `feature-ref.md` R-13, `.specify/features.md` row 101 and `.specify/features/101-anchor-goal-realignment.md` now state the same 5 (2/3) counts. Dated verification files untouched. | `pre-analyze-check.py` plan/tasks pass; counts read in all five surfaces (see Rebaselines R-3) |
| HIGH-2 | Refusal made measurable by a real dispatcher **defined, not implemented**: engine read action `command-mode --command <anchor\|goal> --mode <mode>` (mode sets derived from the canonical templates' `argument-hint`; zero writes; `--command goal` exit 0 on the four Goal modes, exit 2 with stderr literals `anchor-only-mode` + `/speckit.anchor` on the four Anchor-only modes; `--command anchor` exit 0 on seven; unknown mode exit 2 `unknown-mode`). Defined in `requirements.md` FR-020 + SC-002 Source, `contracts/goal-command.contract.md` C-15, `contracts/goal-engine.contract.md` C-26/C-34, `plan.md` G-2, `quickstart.md` S-4, and carried by `tasks.md` T018 (implementation), T020 (option surface), T063 (contract test subprocess), GATE-7 (gate row). | `validate-requirements.py` 0/0; `validate-tasks.py` 0/0; quickstart S-4 commands unchanged by the repair (T063/GATE-7 read the engine at implement) |
| MEDIUM-1 | Re-measured C1–C4 on the declared roots (21 dirs + 9 files, `.specify/features.md` included; 2650 files scanned): **C1 4 · C2 0 · C3 8 · C4 16 = 28**. `test-evidence/live-semantic-scan-baseline-2026-11-12.txt` rewritten with the new reading; `research.md` § baseline, `tasks.md` T001/T075 premises, `quickstart.md` S-8, `feature-ref.md` SC-001 and `plan.md` summary now read 28. | evidence file header + listings (the readings above); see Rebaseline R-1 |
| MEDIUM-2 | `contracts/migration-cleanup.contract.md` C-46 gains rule **N-7** (`/speckit.goal` + `targets\|migrate\|migrate-archive\|coordinate` → `/speckit.anchor`), covering the live team-definition line and making residue class C6's target 0 reachable; `research.md` C6 paragraph states the measured 1 and its rewrite owner; `tasks.md` T056 sweeps `N-1…N-7` and names the Anchor-only mode pointers; T042/T043 own the docs/skill-tree C6 sites. | `research.md` § C6; C-46 table; pre-analyze pass |
| MEDIUM-3 | `tasks.md` T014 aligned to FR-039's closed three changes (file location, `## Objective`→`## Guidance`, `## Success Criteria`→`## Completion Conditions`) with `## Targets` moved out as FR-040's receipt extraction; the undefined "title and identity" item removed. | `validate-tasks.py` 0/0; FR→row trace re-checked |
| MEDIUM-4 | `plan.md` WP territories realigned to `tasks.md` write sets: `.specify/features/041-goal-registry.md` and `.specify/features/094-goal-team-parallel.md` moved to WP-06 (which owns the cross-reference notes), the 094 successor note moved out of WP-03 in `research.md`, and WP-04's "no other file" now admits `test-evidence/**` of this spec (its own dated readings). | plan WP table read against T048/T049/T078/T080 write rows |
| LOW-1 | `tasks.md` FR→row trace rows corrected: FR-019→`T027, T030, T034`; FR-033→`T017, T025`; FR-065→`T065`; `FR-002` split into its own row; FR-001 / FR-005 / FR-007 / FR-008 / FR-016 / FR-020 / FR-029 / FR-062 rows aligned to the rows that actually cite them. Mechanically verified: zero drift and every FR-001…FR-071 has ≥1 task. | scripted cross-check (no drift, full coverage) |
| LOW-2 | `quickstart.md` S-6 no longer greps the non-existent `.specify/teams.md`; the scenario reads the live surfaces only. | quickstart file read |
| LOW-3 | `contracts/anchor-command.contract.md` C-6 `modify` row no longer claims boundary edits (the engine has no boundaries action); it edits objective / criteria only, prior value kept in `## History`. | contract file read |
| LOW-4 | `tasks.md` T048 reads `slug` / `class` / `rule` / `targets` / `summary` from `classification.json` (its actual fields) and takes lifecycle `status` from the live definition. | `classification.json` schema `101-classification/v1` read |

## Rebaselines (old → new, reason, downstream)

- **R-1 — residue baseline C1–C4: 26 → 28.** Old: C1 4 · C2 0 · C3 7 · C4 15 = 26, measured on
  20 dirs + 8 files with `.specify/features.md` excluded. New: C1 4 · C2 0 · C3 8 · C4 16 = 28,
  measured on the declared set (21 dirs + 9 files). Reason: the declaration in `research.md`
  § Live-surface roots makes `.specify/features.md` a root, so its 041 index row counts once in C3
  and once in C4. Downstream: `test-evidence/live-semantic-scan-baseline-2026-11-12.txt` (rewritten),
  `research.md` § baseline, `tasks.md` T001/T075, `quickstart.md` S-8, `feature-ref.md` SC-001,
  `plan.md` summary line, `.specify/features.md` row 101. The projection line in
  `test-evidence/checklist-repair-residue-baseline-2026-11-12.txt:86` (T075 final projection 26) is
  superseded by this re-measurement; that dated record is **not** rewritten, and the supersession is
  recorded here instead.
- **R-2 — C1 pattern: prefix class → article-tolerant prefix.** Old: `(^\|\|>#-*]\s*)…`, which
  cannot match a prose line. New: `(?i)^[\s>#*+-]*(a\|an\|the)?\s*\**goal\**\s+(is\|means\|refers to)\s+(a\|an\|the)?\s*(project-level\|long-horizon\|long-term objective)`.
  Reason: the old pattern missed `docs/reference/commands/goal.md:12` ("A goal is a project-level
  …"), a line every earlier reading counted; the class meaning is unchanged. Disclosed as a
  correction (one reading, local, reversible). Downstream: `research.md` class table C1 row,
  the evidence-file header, and the compiled patterns the implement-stage test must carry.
- **R-3 — inherited blockers: "four records / 037 contributes none" → "five records, 2 resolved /
  3 not-applicable".** Reason: 037's verification carries a `partial` status row that the closed
  extraction rule includes; 074/085 carry none. Downstream: `plan.md` table + prose, `research.md`
  R-13, `feature-ref.md`, `.specify/features.md`, the 101 detail page.
- **R-4 — C6 rewrite table: N-1…N-6 → N-1…N-7.** Reason: one live team-definition line names
  `/speckit.goal targets`, matching no rule, so C6 could not reach 0. Downstream: C-46,
  `research.md` § C6, `tasks.md` T056 (and T042/T043 for the docs/skill-tree sites).
- **R-5 — SC-002 sensor: template parse only → template parse + engine `command-mode` subprocess.**
  Reason: the refusal branch had no deterministic subject. Downstream: FR-020, SC-002 Source,
  C-15 / C-26 / C-34, plan G-2, tasks T018 / T020 / T063 / GATE-7, quickstart S-4.

## Closure re-check and observations

- F-1…F-11 remain closed against their owners; no repair reopened them.
- **O-1** (exclusion justification): `research.md` no longer attributes the `.specify/features/**/*.md`
  exclusion to FR-061; the note now says the detail tree is outside FR-061's protected set and the
  exclusion is the plan's own closed choice. Exclusion stays decidable (listed in `excluded_files`
  with a reason).
- **O-2** (frontmatter tolerance vs FR-034 `_sig_guard`): unchanged; the requirement's prohibition
  stands on its own and the engine's frontmatter read face stays tolerant by design. No contradictory
  live reading; no edit.
- **O-3** (FR-010 empty-objective path): unchanged; the MUST governs the criteria-emptying write that
  exists. No edit.
- **O-4** (FR-043 wording for anchor entries): unchanged; C-39's before/after reading disambiguates.
  No edit.

## Observation (no repair, out of scope)

`closure-acceptance-check.py`'s `_verification_locators` recognises only flat `SC-\d{3}_status=`
lines, so 037's markdown `| SC-016 | partial |` row is invisible to it even though the owner text
(`shared/workflow/acceptance-hardening.md`) includes verification `partial` rows in the extraction
sources. The plan's five-row set is derived from the owner's rule, not from the checker; the gap is
disclosed here rather than repaired (an engine change, forbidden in this seat).

## Gate readings (this repair)

- `validate-requirements.py` → `0 error(s), 0 warning(s)`; 377 lines / 81 definition rows / 8 shared strings.
- `validate-tasks.py` → `PASS — 0 error(s), 0 warning(s)`.
- `pre-analyze-check.py --stage requirements|plan|tasks` → `decision=pass errors=0 advisories=0 waived=0`
  (`fr 71 / sc 10 / tasks 81 / files 13`).
- `audit-plan-changes.py --repo . --base e8775df5b --head HEAD --plan-owned … --declarations notes/plan-edits-analyze-round1.txt`
  → `classification=declared`, `undeclared=false`, 8 touched plan-owned paths, 8 declaration lines,
  cumulative diff 85 added / 53 deleted (uncommitted at reading time: the same 8 paths).
- C1–C4 re-measured: `2650` files scanned over 21 dirs + 9 files → C1 4 · C2 0 · C3 8 · C4 16 = 28.

## Corrections applied in passing (disclosed)

- **C1 pattern** (R-2) — the declared pattern could not match the prose line that every earlier
  reading counted; corrected and re-measured to 4.
- **Dangling-SC guard** — the new plan prose named 037's criterion with the bare token `SC-016`,
  which `pre-analyze-check.py` reads as a reference to an undefined local criterion; rephrased to
  "that criterion" / "row 1 below" while the locator `037:SC-016_status` (no word boundary after the
  digits, so not a local reference) carries the identity. This is a reading fix, not a change of fact.

No anomaly: every finding had one reading consistent with the recorded intent; no intent was invented.
