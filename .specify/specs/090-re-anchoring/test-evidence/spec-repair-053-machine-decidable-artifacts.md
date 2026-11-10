# Spec Repair — 053-machine-decidable-artifacts

**Date**: 2026-11-10
**Target**: `.specify/specs/053-machine-decidable-artifacts/` (live spec dir; not archived)
**Mode**: read-first, bounded — dead-reference repair only; no commit, no push, no subagents.

## Sources

- Prior audit prose: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-2.md` § `053-machine-decidable-artifacts` (verdict BROKEN; 215 refs / 150 alive / 53 dead; broken list items 1–41).
- Deterministic settled scan: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` → key `.specify/specs/053-machine-decidable-artifacts`: `refs 188 / alive 143 / dead 45`; `dead_list` is a 20-path sample (it omits the anchor-move trio and most `.specify/goal` sites), so the audit prose above is the canonical per-entry source.
- Verdict index: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-summary.md` (row 053 = BROKEN).
- Target-format cross-check: `.specify/features.md` row `053` (Feature Details / Spec Path columns) and the detail file's own H1; `skills/external/create-pages/references/hugo-site.md` + `docs/.gitignore` for the `docs/public` convention.

## Counts

| Class | Unique entries | Occurrences | Disposition |
|-------|---------------:|------------:|-------------|
| **Dead total** | **53** | **239** | — |
| live-fixed | 7 | 37 | path rewritten to the live target |
| dated-kept | 26 | 156 | text left unchanged (dated records) |
| non-reference | 20 | 46 | left unchanged (example / placeholder / generated-output filter) |

Arithmetic: 7 + 26 + 20 = 53 unique entries; 37 + 156 + 46 = 239 occurrences. Unit: one **entry** = one distinct dead token spelling (the same token cited in several files is one entry); one **occurrence** = one citation instance. 114 of the 156 dated occurrences are repeated pytest node-id lines in three dated run logs (see §2.2).

Reconciliation with the two sources: the audit prose's 53 uses another grouping (5 anchor-move + 3 goal-move + 1 docs-build + 23 dated skill-layout + 21 illustrative forms) and omits several live sites; the settled scan's 45 counts a distinct-path sample with a different extractor. Both are subsumed by the disposition tables below.

## 1. Live-fixed (7 unique tokens / 37 occurrences, 13 files, 36 changed lines)

| # | Dead reference (before) | Live target (after) | Occ | Locations (file:line, current numbering) |
|---|-------------------------|---------------------|----:|------------------------------------------|
| 1 | `.specify/memory/constitution.md` | `.specify/constitution.md` | 3 | `plan.md:49`; `contracts/clause-coverage.md:78`; `research.md:188` |
| 2 | `.specify/memory/features.md` | `.specify/features.md` | 3 | `plan.md:54`; `feature-ref.md:14`; `research.md:321` |
| 3 | `.specify/memory/features/053.md` | `.specify/features/053-machine-decidable-artifacts.md` | 7 | `plan.md:54,65`; `feature-ref.md:15,153,157`; `checklists/requirements.md:94,99` |
| 4 | `.specify/memory/features/040.md` | `.specify/features/040-agent-metadata-portability.md` | 1 | `feature-ref.md:13` |
| 5 | `.specify/memory/glossary.md` | `.specify/glossary.md` | 8 | `contracts/checker-form.md:6`; `contracts/criterion-subject.md:35`; `contracts/green-point-claim.md:55`; `requirements.md:86,95,186,305`; `research.md:71` |
| 6 | `.specify/goal/` (goal store) | `.specify/anchoring/` | 14 | `requirements.md:115,123,208,254,266`; `contracts/criterion-subject.md:41`; `contracts/run-checks.md:17,79`; `data-model.md:218,244`; `tasks.md:162`; `quickstart.md:42,280,307` |
| 7 | `.specify/goal/draw-two-layer-structure/goal.md` | `.specify/anchoring/draw-two-layer-structure/goal.md` | 1 | `quickstart.md:339` |

Target-existence evidence (all `-e` true at repair time): `.specify/constitution.md`, `.specify/features.md`, `.specify/features/053-machine-decidable-artifacts.md`, `.specify/features/040-agent-metadata-portability.md`, `.specify/glossary.md`, `.specify/anchoring/draw-two-layer-structure/goal.md` (6173 B). The goal store relocation is corroborated by the live engine: `scripts/python/goal-utils.py:71-72` (`ARCHIVE_DIRNAME = ".specify/anchoring"`) and its help text (`:2584-2592`); `.specify/teams/` is still live and was not changed.

Content checks:
- `.specify/features/040-agent-metadata-portability.md` H1 = `# Feature Detail: Token Efficiency Discipline` — the known slug/content inversion noted by the prior audits (same artefact as row 006/027). It is the registry's Feature Details target for Feature ID 040, so it is the live target; no better-named file exists.
- `research.md:321` cites `.specify/features.md:36`: line 36 is the Feature 027 row and still carries the goal-summary dual-index record (`… while .specify/goal/<goal-slug>/ holds the sole complete summary …`) that the A-2 finding cites — the line suffix remained correct after the anchor move.
- Line suffixes (`:14`, `:36`, `:134`) were left exactly as recorded, per the batch's path-only convention (`spec-repair-052-fast-fail-principle.md` §1). The current anchor positions were verified but deliberately not written: `.specify/glossary.md:137` holds the 条款分区 entry; `.specify/constitution.md:120` holds follow-up TODO (a); `.specify/constitution.md:179` is the Principle IV heading.

## 2. Dated-kept (26 unique entries / 156 occurrences)

### 2.1 Dated pre-change mirror snapshot — 22 paths, `notes/pre-change-measurements.md:91–120`

Measured before the two-layer skills layout landed. The fence lists 30 paths; 22 are absent today (8 are alive and were not referenced by the audit). The record is a frozen measurement, not a live pointer, so it is preserved verbatim.

| Line | Path (kept as written) | Today |
|-----:|-----------------------|-------|
| 91 | `.specify/skills/archive-session/SKILL.md` | absent (now `skills/internal/archive-session/`) |
| 92 | `.specify/skills/code-review/SKILL.md` | absent (now `skills/internal/code-review/`) |
| 93 | `.specify/skills/collect-evidence/SKILL.md` | absent (now `skills/internal/collect-evidence/`) |
| 96 | `.specify/skills/create-team/references/operating-loops.md` | absent (now `skills/internal/create-team/references/`) |
| 97 | `.specify/skills/create-team/references/summary-mapping.md` | absent (now `skills/internal/create-team/references/`) |
| 98 | `.specify/skills/create-tools/SKILL.md` | absent (now `skills/internal/create-tools/`) |
| 101 | `.specify/skills/draw-drawio/SKILL.md` | absent (merged into `skills/external/draw-diagram/`) |
| 102 | `.specify/skills/draw-excalidraw/SKILL.md` | absent (merged into `draw-diagram`) |
| 103 | `.specify/skills/draw-mermaid/SKILL.md` | absent (merged into `draw-diagram`) |
| 104 | `.specify/skills/draw-plantuml/SKILL.md` | absent (merged into `draw-diagram`) |
| 105 | `.specify/skills/git-fleet/SKILL.md` | absent (merged into `skills/external/git-utils/`) |
| 106 | `.specify/skills/git-server-init/SKILL.md` | absent (merged into `git-utils`) |
| 107 | `.specify/skills/git-submodule-edit/SKILL.md` | absent (merged into `git-utils`) |
| 108 | `.specify/skills/git-workflow/SKILL.md` | absent (merged into `git-utils`) |
| 109 | `.specify/skills/improve-agent/SKILL.md` | absent (now `skills/internal/improve-agent/`) |
| 113 | `.specify/skills/improve-tools/SKILL.md` | absent (now `skills/internal/improve-tools/`) |
| 114 | `.specify/skills/manage-agents/SKILL.md` | absent (now `skills/internal/manage-agents/`) |
| 115 | `.specify/skills/memory-recall/SKILL.md` | absent (now `skills/internal/memory-recall/`) |
| 116 | `.specify/skills/memory-record/SKILL.md` | absent (now `skills/internal/memory-record/`) |
| 118 | `.specify/skills/study-project/SKILL.md` | absent (renamed `skills/external/study-code/`) |
| 119 | `.specify/skills/summarize-project/SKILL.md` | absent (now `skills/internal/summarize-project/`) |
| 120 | `.specify/skills/think-skills/SKILL.md` | absent (skill removed; no replacement) — same token also at `plan.md:180`, a dated DIFF measurement record |

### 2.2 Other dated records — 4 unique entries / 123 occurrences

| Entry | Locations | Why kept |
|-------|-----------|----------|
| `skills/create-tools/SKILL.md` (bare form) | `notes/clarify-current-failed.txt:60` (2); `baseline-failed.txt:60` (2) | dated clarify-failure log and frozen failure baseline; the `.specify/`-prefixed spelling is the §2.1 snapshot entry |
| `tests/contract/test_browser_site_exclusions.py` | `notes/clarify-current-failed.txt:10–11`; `baseline-failed.txt:10–11`; `current-failed.txt:10–11` (2 per file, 6 total) | dated pytest node ids from runs before the browser-site consolidation; no such file exists anywhere today (`find` → empty) |
| `tests/contract/test_browser_site_memory.py` | `notes/clarify-current-failed.txt:12–47`; `baseline-failed.txt:12–47`; `current-failed.txt:12–47` (36 per file, 108 total) | same; the two tokens together account for the 114 dated log lines |
| `017-consolidate-draft-skills/contracts/skill-format.md#C-001…C-007` | `coverage-baseline.txt:21–27` (7) | frozen coverage-baseline keys, not pointers; the spec is archived (`.specify/archive/specs/017-consolidate-draft-skills/contracts/skill-format.md` exists) |

### 2.3 Kept occurrences inside otherwise-fixed tokens — 10 occurrences

| Token | Kept at | Reason |
|-------|---------|--------|
| `.specify/goal` | `quickstart.md:52,312`; `verification.md:101`; `tasks.md:47,175`; `research.md:260`; `notes/quickstart-run.md:97,144,217` | 9 recorded outputs / probes / verification prose ("本轮真实输出", "实测", `probe:`). Consequence: the recorded checksum `751e5df220adef18c79b1aa3…` in `quickstart.md:52` was taken over the old path strings and is not reproducible after the store move; it stays a dated reading. |
| `.specify/memory/glossary.md` | `notes/red-first-evidence.md:212` | verbatim checker output from the red-first run; the live checker now emits `.specify/glossary.md` (`validate-tasks.py:504`), so this occurrence is history, not a pointer |

## 3. Non-reference (20 unique entries / 46 occurrences)

| # | Token | Occ | Locations | Why not a reference |
|---|-------|----:|-----------|---------------------|
| 1 | `docs/public` | 2 | `quickstart.md:222`; `research.md:23` | generated-output filter (`grep -v`); `skills/external/create-pages/references/hugo-site.md:22` and `docs/.gitignore` still define `docs/public/` as Hugo build output, never committed; absent because unbuilt |
| 2 | `docs/a.md` | 15 | `quickstart.md:147,148,154,165,174`; `research.md:128,129,130,133,138`; `contracts/green-point-claim.md:66,71`; `notes/quickstart-run.md:352`; `notes/red-first-evidence.md:225,232` | synthetic task-row fixture path |
| 3 | `docs/b.md` | 7 | `quickstart.md:155,174`; `research.md:134,138`; `contracts/green-point-claim.md:67,71`; `notes/red-first-evidence.md:232` | same fixture family |
| 4 | `skills/draw-d3js` | 3 | `notes/quickstart-run.md:198,203`; `verification.md:109` | example / negative-test name |
| 5 | `skills/draw-xyz` | 3 | `notes/quickstart-run.md:208,241`; `verification.md:109` | example / negative-test name |
| 6 | `skills/draw-diagram` | 1 | `notes/quickstart-run.md:240` | example name (live skill is `skills/external/draw-diagram/`) |
| 7 | `skills/draw-drawio` | 1 | `notes/quickstart-run.md:240` | example name |
| 8 | `skills/draw-echarts` | 1 | `notes/quickstart-run.md:240` | example name |
| 9 | `skills/draw-excalidraw` | 1 | `notes/quickstart-run.md:241` | example name |
| 10 | `skills/draw-mermaid` | 1 | `notes/quickstart-run.md:241` | example name |
| 11 | `skills/draw-plantuml` | 1 | `notes/quickstart-run.md:241` | example name |
| 12 | `skills/zzz-` | 1 | `notes/quickstart-run.md:226` | negative-test name |
| 13 | `skills/draw-` (prefix) | 2 | `notes/quickstart-run.md:227`; `research.md:248` | prefix / glob form, not a path |
| 14 | `tests/contract/test_x.py` | 1 | `notes/red-first-evidence.md:213` | example path |
| 15 | `.specify/specs/053-` | 1 | `contracts/neutrality-budget.md:16` | ellipsis form (`053-…`), not a path |
| 16 | `scripts/python/scan-confirmation-gat` | 1 | `feature-ref.md:98` | regex-truncated fragment of `scripts/python/scan-confirmation-gates.py` (alive) |
| 17 | `shared/guidelines/requirements-guidelines.m` | 1 | `feature-ref.md:66` | regex-truncated fragment of an alive `.md` path |
| 18 | `shared/constants/clarify-taxonomy.m` | 1 | `feature-ref.md:67` | same |
| 19 | `scripts/python/test` | 1 | `tasks.md:105` | literal phrase ("test… none"), not a path |
| 20 | `templates/contracts-template.md` | 1 | `research.md:33` | rejected alternative ("被拒方案"), never created |

## 4. Additional tokens inspected beyond the audit dead set (0 changed)

| Token | Why not repaired |
|-------|------------------|
| `.specify/memory/tools/goal-utils.py.md` | alive (cited `plan.md:64`; `tasks.md:22,174`; `feature-ref.md:149`; `notes/quickstart-run.md:184`) |
| `.specify/memory/feedback/introspection/introspection-20260923T120035Z.md`, `.specify/memory/feedback/backlog.md` | alive (`research.md:203`; `contracts/run-checks.md:29,75`) |
| `templates/commands/team.md:127` | file alive, line beyond EOF (109 lines) inside the dated A-2 finding; the original record is not unambiguously identifiable, so it is not re-pointed |
| `constitution.md:73`, `constitution.md:14` (bare) | scope-relative shorthand with line suffixes recorded at task/research time; the live file is `.specify/constitution.md` (current anchors drift: Principle IV heading `:179`, TODO (a) `:120`), left as recorded under the path-only convention |
| `scripts/build-summary-input.py` | contextual basename; full target `skills/internal/create-team/scripts/build-summary-input.py` and its mirror exist |
| `feedback/introspection`, `feedback/backlog.md` | substrings of the alive `.specify/memory/feedback/...` paths |
| `skills/contracts/skill-format.md` | substring of the §2.2 coverage-baseline keys, not a repo path |

## 5. Registry row

`.specify/features.md` row `053` (line 62): Status `Implemented`; Feature Details `.specify/features/053-machine-decidable-artifacts.md` (exists); Spec Path `.specify/specs/053-machine-decidable-artifacts/requirements.md` (exists). **Resolves — no registry edit needed**, consistent with the prior audit's "Registry: PASS".

## 6. Validator readings

Both named validators exist and were run against the repaired files.

### `validate-requirements.py`

```
$ python3 scripts/python/validate-requirements.py .specify/specs/053-machine-decidable-artifacts/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 324 lines, 60 definition rows, 10 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

### `validate-tasks.py`

```
$ python3 scripts/python/validate-tasks.py .specify/specs/053-machine-decidable-artifacts/tasks.md
PASS: .specify/specs/053-machine-decidable-artifacts/tasks.md — 0 error(s), 0 warning(s)
EXIT=0
```

### Contract-surface accounting (informational)

```
$ python3 scripts/python/account-clause-coverage.py .specify/specs/053-machine-decidable-artifacts
scanned 286 files: parsed 179 + named-unparseable 107 == 286  [relational sentinel OK]
FR universe: 48; FR claimed: 48; FR uncovered: 0
companion: claimed clauses 182, scanned files 286, clause universe 1999, FR universe 48
[clause-uncovered] fail (640) — 640 uncovered, 168 beyond the frozen baseline
[fr-uncovered] pass (0) — 48 of 48 FRs cited from citation groups
[clause-unparsable] fail (107) — 107 files yield no clause id under the owner's forms
[coverage-baseline-delta] fail (168) — baseline holds 483 names; 472 uncovered items are baseline-internal and do not block
168 error(s), 1 warning(s)
status: uncovered
EXIT=1
```

The exit-1 is corpus-level baseline drift, not a 053 regression: `coverage-baseline.txt` was frozen over 110 files (`files: 110 (parsed 57 + named 53)`), while the corpus now scans 286 files (contracts added by later specs). This repair performed 36 in-line path substitutions and changed no clause id or requirement definition row — `FR universe 48`, `FR claimed 48`, and `claimed clauses 182` are unchanged, and every one of the spec's own clauses is claimed. Refreshing the baseline would be a substantive re-freeze, not a dead-reference repair.

## 7. Post-repair sweep

A normalized scan over the spec directory finds **no remaining live dead path tokens**. The only surviving hits are exactly the dated/non-reference classes tabulated above: 9 dated `.specify/goal` occurrences (§2.3), 1 dated `.specify/memory/glossary.md` occurrence (§2.3), the §2.1 snapshot, the §2.2 logs/baseline keys, and the §3 examples.

## 8. Change footprint

`git diff --stat -- .specify/specs/053-machine-decidable-artifacts/`: 13 files changed, 36 insertions(+), 36 deletions(-). Every change is an in-line path substitution; no line added or removed, no number, status or reading altered, no file outside the spec directory touched, no registry edit. No commit and no push were made.

## 9. Anomaly

The audit prose labels `docs/public` "retired", but the live tree contradicts that — `skills/external/create-pages/references/hugo-site.md:22` and `docs/.gitignore` still define `docs/public/` as generated Hugo build output, so the two citations were treated as non-reference filters rather than dead pointers.
