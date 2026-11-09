# Analyze round 4 — VB fork: cross-artifact consistency, counts, gates

Writer: VB (fork verification worker). Date 2026-11-09. Tree: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master`, HEAD `2c704003`. Read-only: no commits, no push, no subagents; writes only this file and `test-evidence/vb-*`. No in-passing repairs were made.

S94 = `/storage/project/cloud-native-ai/spec-kit/.specify/specs/094-goal-team-parallel`.

## 1. Gate readings (all rerun this round, verbatim)

Verbatim captures, each ending with its `EXIT=` line: `test-evidence/vb-gate-requirements.txt`, `vb-gate-coverage.txt`, `vb-gate-tasks.txt`, `vb-gate-tensions.txt`, `vb-gate-decomposition.txt`, `vb-gate-precheck-{requirements,plan,tasks}.txt`.

| # | Gate | Command (explicit flags) | Reading (verbatim excerpts) | Exit |
|---|------|--------------------------|------------------------------|------|
| 1 | validate-requirements | `python3 .specify/scripts/python/validate-requirements.py $S94/requirements.md` | `status: ok`; `[id-contiguous] pass (0)` `[doc-order] pass (0)` `[ref-resolvable] pass (0)` `[marker-count] pass (0)` `[dup-id] pass (0)` `[path-marker] pass (0)`; `scanned: 326 lines, 55 definition rows, 6 shared strings`; `0 error(s), 0 warning(s)` | 0 |
| 2 | account-clause-coverage | `python3 .specify/scripts/python/account-clause-coverage.py $S94 --corpus-root /storage/project/cloud-native-ai/spec-kit/.specify/specs` | `scanned 313 files: parsed 198 + named-unparseable 115 == 313  [relational sentinel OK]`; `clause universe: 2116 distinct names over 198 parsed files (2140 ids extracted)`; `claimed clauses (this feature): 113`; `[clause-uncovered] pass (599) — 599 uncovered, 0 beyond the frozen baseline`; `[fr-uncovered] pass (0) — 43 of 43 FRs cited from citation groups`; `[clause-unparsable] fail (115) — … 1 of them declare a positive form, which is parse doubt and is never read as zero-and-covered`; `[coverage-baseline-delta] pass (0) — baseline holds 599 names …`; `0 error(s), 1 warning(s)`; `status: ok` | 0 |
| 3 | validate-tasks | `python3 .specify/scripts/python/validate-tasks.py $S94/tasks.md` | `WARN  239: blockedBy: T043 references later task T054 (forward dependency — verify this is intentional)`; `PASS (with warnings): … 0 error(s), 1 warning(s)` | 0 |
| 4 | validate-decision-tensions | `python3 .specify/scripts/python/validate-decision-tensions.py --spec $S94` | `status: ok`; six checks `pass (0)`; `scanned: 374 lines, 7 record(s)`; `channel: value_domain=HIGH-or-0, high=0`; `0 error(s), 0 warning(s)` | 0 |
| 5 | pre-analyze-check ×3 | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --repo /storage/project/cloud-native-ai/spec-kit --spec-dir $S94 --stage {requirements,plan,tasks}` | each stage: `decision=pass errors=0 advisories=101 waived=0 fr=43 sc=12 tasks=83`; all 101 findings are `missing-path` advisories | 0 ×3 |
| 6 | decomposition-check | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements $S94/requirements.md --tasks $S94/tasks.md` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 43, "task_count": 83, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}` | 0 |

Notes:
- The `[clause-unparsable] fail (115)` lane with overall `status: ok` / exit 0 is the script's own design (1 parse-doubt file: `067-loop-efficiency-hardening/contracts/runner-contract.md`, named owner-grammar finding). It matches `tasks.md` GATE-6's recorded post-freeze reading word-for-word.
- Independent re-derivation this round: **43 FR / 12 SC** definitions, both contiguous (`^- \*\*FR-NNN\*\*:` / `^- \*\*SC-NNN\*\*:`); **113** `**C-NNN**` markers = **113** distinct ids, `C-1…C-113` no gap, per page **30 / 24 / 18 / 20 / 21**; **83** task rows, ids T001–T083 each exactly once (file order places T082 before T081 — correct, T081 carries `[blockedBy: T082]`; `validate-tasks.py` silent); **7** packages 15+17+19+8+16+6+2 = 83; `coverage-baseline.txt` header `base-sha: abfc12d19412 | files: 308 (parsed 193 + named 115)`; `plan-baseline-names.txt` = 46 lines / 46 unique.

## 2. M/L closure verification (targets from `notes/analyze-round3-findings.md`)

| Id | Round-3 target | Verified this round (independent measurement) | Status |
|----|----------------|-----------------------------------------------|--------|
| M-1 | premises FR 42→43 / SC 11→12 | `tasks.md:87` reads **43**, `tasks.md:88` reads **12**; independent count 43 / 12 contiguous | **closed** |
| M-2 | breakdown 30+24+18+20+21=113; archive 24 | `tasks.md:7` states exactly `C-1…C-113 = 113 marker lines / 113 distinct ids: binding 30 + archive 24 + handoff 18 + command-family 20 + owner-rewrites 21`; per-page markers measured 30 / 24 / 18 / 20 / 21 | **closed** |
| M-3 | FR→row trace: 43 rows, drift 0 both directions; malformed FR-043 row fixed | trace table = 43 FR entries over 22 physical rows, every physical row 4 cells (none malformed); script over the 83 task-row bodies vs the table: FRs only-in-table ∅, only-in-rows ∅, per-FR membership drift **0**; FR-043 row reads `T081, T082, T083` and those three rows quote FR-043 | **closed** |
| L-1 | requirements SC range `SC-001…SC-012`; historical 42/111 mentions caveated | `requirements.md:9` reads `FR-001…FR-043 与 SC-001…SC-012`; `:263` carries `（pre-FR-043 record；现 FR 数为 43）` and `（pre-FR-043 record；现条款标记为 113）`; `:295` carries `（引文为 pre-FR-043 record；现 43 条）`; no `SC-001…SC-011` survives in requirements/plan/tasks/quickstart/feature-ref; plan.md and feature-ref.md carry no live 42/111 | **closed** |
| L-4 | 46 baseline ids everywhere | plan.md:48/70/262/282, tasks.md:38/61/99/142/144, quickstart.md:27, `features/094.md` all read 46; `plan-baseline-names.txt` holds 46; `plan-baseline-stability.txt` records the empty 3-run diff | **closed at named sites — one new contradiction**: `research.md:115` (R-25) still says "**44 ids**" while naming the same file → VB-3 (LOW) |
| L-5 | date caveats on pre-repair evidence pointers | `tasks.md:478` bullet marked `round-2 recorded reading (2026-11-09, pre-round-3; historical, not the current reading)`; `:485` correctly states `coverage-tasks.txt` holds `fr-uncovered fail (26) — 16 of 42` / `status: uncovered` (verified against the file); `:488` carries `(pre-repair reading, 2026-11-09: fr 42 / sc 11 / tasks 80)` (verified against `decomposition-tasks.json` 42/80, `pre-analyze-tasks.json` + `.txt` fr=42/sc=11/tasks=80) and points to `notes/analyze-round3/w2-traceability.md` § 3 | **closed with one new mispointer** — `tasks.md:483` says pre-analyze "42/42 … kept verbatim at `test-evidence/analyze-repair2-gates-requirements.txt`", but that file holds validate-requirements + account-clause-coverage readings and its FR lane reads `43 of 43`; the pre-analyze evidence is `analyze-repair2-gates-precheck.txt` (3× pass, 88 advisories, no FR ratio) → VB-2 (LOW) |
| T014 | anchors → `:1447` / `:185` / `:1449` | `tasks.md:165` carries exactly `goal-utils.py:1447`, `:185`, `:1449`; source `scripts/python/goal-utils.py` and mirror `.specify/scripts/python/goal-utils.py` agree line-for-line (185 = `--scope global or --scope spec` guidance; 1447 = `requested_scope = "auto" if …`; 1449 = scope-auto write refusal message) | **closed** |
| quickstart | stale-count sweep | title `Feature 094`; fixtures `.specify/.tmp/s094` in S-1 and Teardown; no stale `42 FR` / `80 rows` / `111 clauses` / `43 map rows`; the only count claim (`46 ids`) is D2-correct | **closed** |

## 3. Registry (must state the current truth)

- `.specify/memory/features.md:101` (`| 094 |` row): description on `.specify/anchoring/`; counts `113 条款，C-1…C-113`, `FR 43/43、SC 12/12`, `83 行 T001–T083 / 7 包`; links `notes/analyze-round3-findings.md`. **No stale counts.** Feature Details pointer resolves to the existing `.specify/memory/features/094.md`.
- `.specify/memory/features/094.md`: same counts; package breakdown 15+17+19+8+16+6+2; 46-id baseline; links the round-3 findings and both repair ledgers. **No stale counts.**
- **VB-1 (LOW, open)**: both still say **"repair round 3 进行中"** (`features.md:101`; `features/094.md:59`) and the row ends `下一阶段 = repair round 3 收口 → analyze 第 4 轮`. The repair landed in `84d8765f` (with `2c704003` refreshing these very rows) and the state spine's own `last_verdict` records `Repair round 3 = H-1/H-2 closed … ALL GATES GREEN`. Per this round's criterion the status should read round 3 **repaired** → round 4 running.
- Known-open, declared in the state spine, outside the `| 094 |` row: `features.md:4` `Total Features: 87` vs **88** table rows / **88** distinct ids (re-measured this round).

## 4. Evidence consistency (artifact claim vs cited file)

Every `test-evidence/*` citation in requirements / plan / tasks / quickstart / feature-ref / data-model / research / contracts / checklists was checked. Current-reading citations all match their files:

- `plan-baseline-names.txt` (46 lines) + `plan-baseline-stability.txt` (empty 3-run diff, 46 each) — plan.md:262 true.
- `requirements-baseline-probe.txt` — 7 goal / 7 team, including the 089 goal-slug and 088/089 team-slug deviations exactly as A6 states.
- `coverage-tasks.txt` — holds `fr-uncovered fail (26) — 16 of 42` and `status: uncovered` (tasks.md:485 true).
- `decomposition-tasks.json` (fr 42 / tasks 80); `pre-analyze-tasks.json` + `.txt` (fr=42 sc=11 tasks=80) — tasks.md:488 caveat true.
- `validate-tasks.txt` — `0 error(s), 1 warning(s)`, warning is T043→T054 (dated record, recorded against the pre-renumber 092 path; claim matches).
- `analyze-repair2-engine-measurements.txt` §1–2 (three grammar facts) and `analyze-repair2-resident-measurement.txt` (6 goal + 12 team = 18 residents, all unbound) match their citing artifacts.
- `checklist-readings-2026-11-09.txt` / `checklist-gates-2026-11-09.txt` — both checklist gates pass with the recorded red-first mutation probe (`reader=fail`, exit 1).
- All currently-absent cited paths (`migration-dryrun.json`, `migration-applied.json`, `residual-before.json`, `residual-after.txt`, `resident-backfill.json`, `implementation-baseline-names.txt`, `closure-failed.txt`, `T003-fixture-probe.txt`, `migration-dryrun.txt`) are prospective implement-stage outputs, not existence claims.

Contradictions:
- **VB-2 (LOW)**: `tasks.md:483` mispointed pre-analyze evidence (see L-5 row). The correct holders are `analyze-repair2-gates-precheck.txt` (pre-analyze pass ×3) and `pre-analyze-tasks*.{txt,json}` / `pre-analyze-*-analyze-repair.json` (fr=42).
- **VB-3 (LOW)**: `research.md:115` (R-25) — "`test-evidence/plan-baseline-names.txt` (44 ids, measured this session)" vs the file's 46.
- **VB-4 (LOW)**: the 092→094 renumber sweep is incomplete on identity lines (W3's own renumber plan listed in-spec identity lines as mechanical rewrites): `requirements.md:14` `**Feature ID**: 092`; `tasks.md:3` `**Requirement ID**: 092` and `:5` `**Related Feature**: 092 …`; `data-model.md:1` `# Data Model — Feature 092`; `research.md:1` `# Research — Feature 092`; `team/094-goal-team-parallel/team.md:4` description "Feature 092" (adjacent to the declared L-03 name residue); fixture roots `.specify/.tmp/s092/` at `tasks.md:143` and `:490` while quickstart was fixed to `.specify/.tmp/s094` — the two artifacts disagree on the sanctioned fixture root. The dated checklist record (`checklists/2026-11-09-requirements-quality.md:3,5`) keeps its 092/42-FR text per D5.
- Known-open (disclosed by repair-r1 residual 3, unchanged): `tasks.md:166` (T015) carries the stray duplicated `— evidence: test-evidence/validate-tasks.txt — evidence: scripts/python/goal-utils.py …` fragment.

## 5. Cross-artifact observations outside the assigned M/L set (VC/driver lane)

- **D4 write-home vocabulary is split wider than the declared residual.** Declared (repair-r2 residual 1; state-spine residual — still open): contracts pages carry `.specify/goal/` in live normative clauses — C-10 (`contracts/binding-and-lifecycle.md:61`), C-13 (`:75`), C-15 (`:88`), C-31 (`contracts/unified-archive-and-migration.md:10-11`), C-58/C-59/C-66 (`contracts/handoff-contract.md:36,42,66`), C-112 (`:125`), `owner-rewrites-and-tests.md:57`. C-31 states normatively that the unified archive "MUST be exactly `.specify/goal/<slug>/`" while re-scoped FR-007 (`requirements.md:132`) and plan Storage (`plan.md:47`) say `.specify/anchoring/<slug>/goal.md` — a direct normative contradiction between requirement owner and contract. **Undeclared additional surface**: `tasks.md:96` (premise re-derivation `basename -a .specify/goal/*/` is a dead path; the value 6 still reproduces against `.specify/anchoring/`), `:176`, `:200`, `:220` (T037), `:321` (T073 instructs writing the old path into `framework-map.md`), `:330` (T081), `:400`; `quickstart.md:42,64,80,82`; `data-model.md:21,42`. Until swept, task rows would implement and assert the retired path.
- Note (not a finding): the premises table (`tasks.md:84`) is explicitly dated "measured at generation time (2026-11-09)" with a mandatory implement-entry re-measurement (T004). `Declaration facts on disk` reads **23**; the tree now holds **24** (`non-disposable-review-surface.yaml` landed 2026-11-09 17:00 through the merged 092 work). `Unified-archive entries today` reads 6 goal / 12 team — still reproduces (`.specify/anchoring/` = 6, `.specify/teams/` = 12), though only through the renamed directory.
- Note: `tasks.md:3-5`'s 092 identifiers are counted once under VB-4 above; requirements.md:, plan.md headers are otherwise clean.

## Verdict

All six gates green. All eight M/L closures verified **closed** at their named sites (L-4 and L-5 closed, each with one adjacent new LOW contradiction). Four LOW findings remain — one registry-status staleness, two evidence-citation contradictions, one incomplete renumber sweep — each a mechanical one-line repair. The D4 split breadth above is handed to VC and is the only item that must be resolved before the implement gate.

**VB: FAIL — VB-1 registry status "repair round 3 进行中" is not the current truth (LOW) · VB-2 tasks.md:483 evidence pointer contradicts its cited file (LOW) · VB-3 research.md:115 "44 ids" vs the file's 46 (LOW) · VB-4 092 renumber residue on identity lines + s092 fixture roots (LOW)**
