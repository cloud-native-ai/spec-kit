# FV1 — final verification of the D4 anchoring fix wave (analyze round 4 close, 2026-11-09)

**Worker**: FV1, final verification worker (read-only; this file is the only write).
**Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master`, HEAD `aeadddd2`.
**Target**: the D4 anchoring fix wave committed in `aeadddd2` — closure of VC H-1…H-5, the VC M/L items the wave adopted, and the VA/VB items in its scope; gates re-run independently.
**Method**: every reading below was re-measured on this tree with `grep`/`ls`/`git diff`/the gate scripts; nothing is taken on faith from the fix ledgers (`notes/analyze-round4/fix-w1.md` / `fix-w2.md`).

---

## 1. `.specify/goal` sweep — the five live surfaces are clean

Measured `grep -c '\.specify/goal'`:

| surface | hits |
|---|---|
| `contracts/binding-and-lifecycle.md` | 0 |
| `contracts/command-family-and-declarations.md` | 0 |
| `contracts/handoff-contract.md` | 0 |
| `contracts/owner-rewrites-and-tests.md` | 0 |
| `contracts/unified-archive-and-migration.md` | 0 |
| `tasks.md` | 0 |
| `quickstart.md` | 0 |
| `feature-ref.md` | 0 |
| `data-model.md` | 0 |

Whole spec dir re-measured: **118** remaining `.specify/goal` occurrences, all in dated records — **28** exactly matching VC's keep list (requirements 6 — user-brief quote / rename fact / dated clarifications; plan 8 — historical/antithesis/rename facts; research 4 — Phase-0 dated research; `goal/094-goal-team-parallel/goal.md` 2 — goal Objective mirrors the brief; `team/094-goal-team-parallel/team.md` 2 — goal/charter prose at :9/:131; checkpoints 6 — dated stage records) plus **90** quotations inside dated notes ledgers (round-1…round-4 records quote every defect line by construction). **0 live normative hits in the five consumed surfaces; no FAIL.**

## 2. The 9 contract lines, the retained `goal.md` name, the spec-local store, C-112

| # | file:line | clause | now reads | verdict |
|---|---|---|---|---|
| 1 | `contracts/binding-and-lifecycle.md:61` | C-10 | `.specify/anchoring` | PASS |
| 2 | `contracts/binding-and-lifecycle.md:75` | C-13 | `.specify/anchoring/<slug>/` | PASS |
| 3 | `contracts/binding-and-lifecycle.md:88` | C-15 | `.specify/anchoring/**` | PASS |
| 4 | `contracts/unified-archive-and-migration.md:10` | C-31 | `.specify/anchoring/<slug>/` | PASS |
| 5 | `contracts/unified-archive-and-migration.md:11` | C-31 | `.specify/anchoring/<slug>/goal.md` | PASS |
| 6 | `contracts/handoff-contract.md:36` | C-58 | `.specify/anchoring/<goal_slug>/goal.md` | PASS |
| 7 | `contracts/handoff-contract.md:42` | C-59 | `.specify/anchoring/<goal_slug>/goal.md` | PASS |
| 8 | `contracts/handoff-contract.md:66` | C-63 | `.specify/anchoring/**` | PASS |
| 9 | `contracts/owner-rewrites-and-tests.md:57` | C-100 | `.specify/anchoring/` | PASS |

- **Diff is path-only.** `git diff aeadddd2^ aeadddd2 -- contracts/` shows exactly 10 path-line pairs (the 9 above + C-112), no clause id, citation group or other prose change; `grep -c anchoring contracts/*.md` = 3 / 0 / 3 / 1 / 3 = **10 line occurrences**, matching VC's split table.
- **`goal.md` file name kept**: 6 occurrences remain in contracts (handoff 2, owner-rewrites 1, archive 3 — incl. C-112's `.specify/anchoring/*/goal.md`).
- **Spec-local store unchanged**: C-43 probe glob `.specify/specs/*/goal/*/goal.md` intact (`unified-archive-and-migration.md:76`); C-46 `.specify/specs/<spec>/goal/**` intact (`:90`); C-106 twin intact (`owner-rewrites-and-tests.md:93`).
- **C-112 keeps its embedded dated count**: `unified-archive-and-migration.md:124–125` — "Measured 2026-11-09: `.specify/anchoring/*/goal.md` carries 6 … and `.specify/teams/*/team.md` 12". Re-measured live this run: `ls -d .specify/anchoring/*/goal.md` = **6**, `ls -d .specify/teams/*/team.md` = **12**.
- Related M-item: C-93 (`owner-rewrites-and-tests.md:22`) now names the real heading `§ Goal/Team（085）`; no `Temporary Goal/Team` heading exists.

## 3. Quickstart / feature-ref / data-model + membership invariant

| item | measured | verdict |
|---|---|---|
| `quickstart.md:42,64,80,82` | all four now `.specify/anchoring/…` (start `mkdir`/S-3/S-5 hashes) | PASS |
| `feature-ref.md:92` (SC-012) | `.specify/anchoring/*/goal.md` + `.specify/teams/*/team.md` | PASS |
| `data-model.md:21,42` | E-1 path `.specify/anchoring/<slug>/goal.md`; territory rule `.specify/anchoring/**` | PASS |
| feature-ref membership | **43 FR entries / 43 distinct ids**, no duplicates (two-pair table parsed structurally); diff of `feature-ref.md` in aeadddd2 = the SC-012 line only | PASS |

## 4. VB items

| item | measured | verdict |
|---|---|---|
| VB-2 `tasks.md:483` pointer | now `test-evidence/pre-analyze-tasks-analyze-repair.json`; the cited file holds `fr: 42, sc: 11, tasks: 80`, decision pass — matches the sentence's 42/42 reading | PASS |
| baseline header | `coverage-baseline.txt:2` `# frozen-from: .specify/specs/*/contracts/* excluding 094-goal-team-parallel` — repo-relative form; 599-name body untouched (`base-sha: abfc12d19412` kept) | PASS |
| VB-3 `research.md:115` | "(46 ids, measured this session 2026-11-09; corrected at analyze round 4 … the file holds 46 unique ids)"; `plan-baseline-names.txt` = 46 lines / 46 unique | PASS |
| VB-4 identity lines | `requirements.md:14` = `**Feature ID**: 094`; `tasks.md:3,5` = 094; `data-model.md:1` / `research.md:1` titles = 094; team identity below; fixture roots `.specify/.tmp/s094` (tasks.md:143,490; quickstart:35,36,124); `tasks.md:472` version point = 094; `tasks.md:491` pre-094; remaining bare `092`s are dated lineage records (renumber note, run id, execution-lessons quote) per D5 | PASS |
| `features.md:4` header | `**Total Features**: 88`; table = **88 rows / 88 distinct ids** | PASS |
| team.md 094 identity | `team/094-goal-team-parallel/team.md:2` `SDD Temporary Team 094`; `:4` Feature 094; `:17` `.specify/anchoring/**`; `:37` `.specify/memory/features/094.md`; `:9`/`:131` keep the brief-mirror `.specify/goal|teams` per VC keep list | PASS |
| **registry status currency** | `features/094.md:66` and `features.md:101` still say "锚定修复波次（W1/W2）**进行中**，下一阶段 = 修复集成 + 门复跑 → 终验 → implement 门", while the **same commit's** state spine (`.specify/state/094-goal-team-parallel.md:13`) records "Fix wave (W1/W2) = D4 anchoring aligned … **ALL GATES GREEN** … Final verification wave dispatched" and `:24` `next_action = final verification … → analyze READY gate` | **FAIL — one increment stale** |

Note: the VB-1 complaint itself (round 3 "进行中" while reparsed and round 4 running) is fixed — both rows now read round 3 closed + round 4 verified. The FAIL is the recurrence of the same defect class at the next boundary: the wave-completion sentence was authored pre-integration (fix-w2.md § VB-1 "after" column) and was not refreshed when the driver committed the integration in the same commit that wrote the contradicting state spine. One-line mechanical refresh; no anchoring substance involved.

## 5. Gates — all re-run independently, explicit flags

| # | Gate | Command | Reading | Exit |
|---|------|---------|---------|------|
| 1 | validate-requirements | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/094-goal-team-parallel/requirements.md` | `status: ok`; six checks `pass (0)`; `scanned: 326 lines, 55 definition rows, 6 shared strings`; `0 error(s), 0 warning(s)` | 0 |
| 2 | account-clause-coverage | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/094-goal-team-parallel --corpus-root /storage/project/cloud-native-ai/spec-kit/.specify/specs` | `scanned 313 files: parsed 198 + named-unparseable 115 == 313`; `clause universe: 2116 distinct names`; `claimed clauses: 113`; `[clause-uncovered] pass (599) — 0 beyond the frozen baseline`; `[fr-uncovered] pass (0) — 43 of 43`; `[clause-unparsable] fail (115)` (1 parse doubt, by design); `[coverage-baseline-delta] pass (0)`; `0 error(s), 1 warning(s)`; `status: ok` | 0 |
| 3 | validate-tasks | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/094-goal-team-parallel/tasks.md` | `WARN 239: blockedBy: T043 references later task T054` (disclosed forward edge); `0 error(s), 1 warning(s)` | 0 |
| 4 | validate-decision-tensions | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/094-goal-team-parallel` | `status: ok`; six checks `pass (0)`; `scanned: 374 lines, 7 record(s)`; `0 error(s), 0 warning(s)` | 0 |
| 5 | pre-analyze-check ×3 | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --repo /storage/project/cloud-native-ai/spec-kit --spec-dir .specify/specs/094-goal-team-parallel --stage {requirements,plan,tasks}` | each stage `decision=pass errors=0 advisories=98 waived=0`, `fr: 43, sc: 12, tasks: 83`; advisories are `missing-path` findings only | 0 ×3 |
| 6 | decomposition-check | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/094-goal-team-parallel/requirements.md --tasks .specify/specs/094-goal-team-parallel/tasks.md` | `{"mode":"tasks","decision":"proceed","measured":{"fr_count":43,"task_count":83,"fr_ceiling":120,"task_ceiling":160},"reasons":[]}` | 0 |

Advisory delta vs the round-4 record (101 → 98): the three aligned `.specify/anchoring` paths now resolve, so their `missing-path` advisories no longer fire; decision remains `pass`, errors 0.

## 6. Independent structural cross-checks

- Clause markers: `grep -cE '^- \*\*C-[0-9]+\*\*:' contracts/*.md` = 30 / 20 / 18 / 21 / 24 = **113 markers, 113 distinct ids**, `uniq -d` empty; namespace C-1…C-113 intact.
- Contract diff scope: path-only, as listed in §2; no clause-text change.
- `features.md` 88/88; feature-ref 43/43; archive 6/12 — all reproduce.

## Verdict

**FV1: FAIL** — one item: registry status currency (`features/094.md:66` + `features.md:101`) is one increment stale; it says the anchoring fix wave is still in progress with "修复集成 + 门复跑" pending, while the same commit's state spine records the wave complete, all gates green and the final verification wave running.

Every D4 anchoring closure (VC H-1…H-5, M-1/M-2/M-3/M-4/M-5/M-6/M-7/M-8, L-1/L-2/L-3), every VA-item (tasks.md:483 pointer, baseline header) and every other VB item (VB-2/VB-3/VB-4, header 88, team identity) is **verified closed**, and all six gates re-run green.

**ANOMALY**: the registry lag is the VB-1 defect class recurring at the integration boundary — W2 authored "W1/W2 进行中" before integration, and the driver's same-commit state update (`last_verdict` = wave complete, gates green, FV dispatched) did not refresh `features.md:101` / `features/094.md:66`; one-line mechanical refresh, registry lane (FV2) or a micro-repair.
