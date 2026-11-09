# Repair round 3 — R2 closure ledger (2026-11-09)

**Writer**: R2 (fork repair writer, requirements / plan / feature-ref / quickstart / registry / register).
**Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master` at `abfc12d1`. No commits, no push, no subagents.
**Binding inputs**: `notes/analyze-round3-findings.md` (verdict + D1–D5), `notes/analyze-round3/w3-trunk-reconciliation.md` §2–3, `notes/analyze-round3/w2-traceability.md` §1–2.
**R1 dependency observed mid-wave**: the C-112/C-113 rename landed while this writer worked — re-measured after the edit window: 113 marker lines, **113 distinct ids**, namespace statement `C-1…C-113` (`contracts/binding-and-lifecycle.md:10`). `feature-ref.md` therefore records the post-rename ids and needed no "dependency pending" fallback.

## Closed ids

### D4 — anchoring vocabulary reconciliation

Trunk facts adopted (measured on this tree, read-only):

- `scripts/python/goal-utils.py:59` `ARCHIVE_DIRNAME = ".specify/anchoring"`; `:63` `DEFINITION_FILENAME = "goal.md"`; `:1339` `--scope choices=("global", "spec", "auto")`.
- `.specify/anchoring/` holds 6 slug dirs; `.specify/goal/` is absent.
- `skills/external/sdd-loop-driver/SKILL.md:45` is the real section (`Goal/Team（085）`), mirrored at `.specify/skills/sdd-loop-driver/SKILL.md`; it explicitly requires readers to accept both `goal_slug`/`team_slug` and the historical `temp_*` keys — the alias obligation in FR-028 is live, not moot.

Changes:

- `requirements.md:19` — Overview: global archive now `.specify/anchoring/**` with the rename fact and the stale routing literal noted.
- `requirements.md:22,35,39,45,47,55` — US1 / US2 path vocabulary moved to `.specify/anchoring/...`; US2's duplicated "7 + 7" count replaced by pointers to A6 / plan EP-002 (one-source-of-truth; the count itself is disclosed there).
- `requirements.md:132` (FR-007) — single write home re-scoped to `.specify/anchoring/<slug>/goal.md` and `.specify/teams/<slug>/team.md`; spec-local paths named as migration source only, so the FR remains delta (W3 §1.4: spec-local write path still live upstream).
- `requirements.md:150` (FR-025) — member set stays `goal` / `teams` / `auto`; members name **archive rows / definition kinds, not directories** (`goal` row dir = `.specify/anchoring/`, filename still `goal.md`); engine's current `global|spec|auto` stated as fact. This is a decision: the falsified clause "档案行改名为 goal / teams" is replaced, and the rejected alternative (renaming the member to `anchoring`) is recorded.
- `requirements.md:153` (FR-028) — pointer corrected to `skills/external/sdd-loop-driver/SKILL.md` § `Goal/Team（085）` (+ mirror) and its `references/checkpoint-protocol.md`; alias obligation kept with the driver's own "读方须两者都认" as evidence; dead pointer `.specify/skills/sdd-loop-driver/SKILL.md § Temporary Goal/Team` removed.
- `requirements.md:168` (FR-043), `:186` (Key Entities), `:198` (SC-001), `:203` (SC-006), `:209` (SC-012) — path vocabulary `.specify/anchoring/...`.
- `requirements.md:315` (A1), `:320` (A6) — A1 gains the member-naming fact; A6 keeps the dated 7/7 probe as SC-003's baseline and records the round-3 re-measurement (goal 9 / team 8 conforming + one non-conforming `092-non-disposable/team/team.md` = 9 / 9; see EP-002).
- `requirements.md:297-306` — new `### Analyze-repair round 3（2026-11-09，D4 anchoring 词汇重述）` Notes subsection: the three FR re-scopes, the path sweep, the D5 exclusions (user `Input` quote and dated Clarifications untouched), and the rejected antithesis.
- `plan.md:4,11,16-18,47,53,64,73,84,98-104,110,134,141,163,191,258,354,372` — summary layer paths, Storage, Scale, T-001 (decision/antithesis/poles/evidence/sacrifice), T-002 decision, **T-004** (decision extended with the rename fact + member-naming ruling; `revision_trigger` gains the member-name/directory literal-mapping reopening condition), T-006 search path, contract ranges, EP-002, S2/Phase 1 ranges.
- `features/094.md` — Overview + Key Changes adopt `.specify/anchoring/` and the member-naming ruling.

**D4 decision record pointer**: `plan.md` § Decision Tensions **T-004** (decision at `plan.md:134`, reopening condition at `plan.md:141`) + `requirements.md` § Notes → `Analyze-repair round 3` (`requirements.md:297-306`). Shape: decision / antithesis (rename member to `anchoring`) / binding constraints / discriminating evidence (three-surface value-set consistency: FR-025 ↔ T-004 ↔ contract C-9) / expected sacrifice / revision trigger. The engine's current `global|spec|auto` is recorded as a fact, not redefined.

### D1 — clause-id collision (feature-ref side)

- `feature-ref.md:28` (FR-035) and `:31` (FR-016) — `handoff-contract#C-53` / `handoff-contract#C-54`.
- `feature-ref.md:36` (FR-043) — `unified-archive-and-migration#C-112` / `#C-113` (post-rename ids; R1's rename verified landed: 113 distinct ids).
- Membership kept identical to `w2-traceability.md` §1. Verified programmatically: regenerated map vs. table = **43 FRs / 43 FRs, 0 mismatches** (membership and numeric order).
- In-passing defect found and fixed: the FR-022 table row had 5 cells in a 4-column table (extra trailing pipe); corrected at `feature-ref.md:37` (disclosed, not silent).

### L-3 — "43 map rows" wording + order-only rows

- `feature-ref.md:39-42` — count now reads "43 FR entries across 22 physical table rows (two FR cells per row), 43 distinct FR ids", plus the `page#id` qualification rule.
- `feature-ref.md:44-71` — embedded regeneration snippet now sorts each FR's clauses by clause number and emits the `ANCHOR` set (`handoff-contract#C-53/#C-54`, `unified-archive-and-migration#C-112/#C-113`); prose states the earlier contract-file order differed on five rows (FR-013, FR-029, FR-030, FR-037, FR-039) in order only, and that membership is the invariant. Verified by executing the snippet verbatim: 43/43, 0 mismatches.

### M-4 — registry refresh

- `.specify/memory/features/094.md` — full refresh to current truth: FR 43 / SC 12 / 113 clauses (C-1…C-113, incl. C-112/C-113) / tasks 83 (T001–T083) / 7 packages (15+17+19+8+16+6+2) / plan-stage gates `fr=43` / round-1+2 closures / **round 3 NOT-READY (2 HIGH) → repair round 3 running** with links to `notes/analyze-round3-findings.md` and the two repair ledgers / renumber from 092 recorded (commit `29c3aa08`) / L-03 residual kept.
- `.specify/memory/features.md:101` — `| 094 |` row rewritten: description drops the dead `.specify/goal` path and adopts `.specify/anchoring/`; counts 113 / 43-43 / 12-12 / 83 rows / 7 packages; stage record ends at "analyze round 3 NOT-READY (2 HIGH) → repair round 3 running"; renumber note added; **Feature Details pointer corrected** from the dead `.specify/memory/features/094-goal-team-parallel.md` to the existing `.specify/memory/features/094.md` (only `092.md` and `094.md` exist in that directory).

### L-1 — live SC range + dated 42/111 caveats

- `requirements.md:9` — `SC-001…SC-011` → `SC-001…SC-012`.
- `requirements.md:263` — the H-01 record's `26/42`, `42/42`, `111` keep their values and gain `（pre-FR-043 record；现…）` caveats.
- `requirements.md:295` — the L-01 quote "全部 42 条 FR" gains `（引文为 pre-FR-043 record；现 43 条）`.

### L-2 — spec-local denominator

- `plan.md:53` — "14 real spec-local definitions (goal 7 / team 7)" replaced by the current reading: **18 definition files measured 2026-11-09 (goal 9 / team 9)**, with the plan-entry 7/7 and tasks-stage 8/8 readings named and the residual probe declared the authority.
- `plan.md:258` (EP-002) — premise rewritten to "the count is the probe's reading, not a frozen constant", carrying all three readings (7/7 plan entry; 8/8 tasks N-4; 9/9 repair stage, incl. one non-conforming `092-non-disposable/team/team.md`); slug-collision claim unchanged.
- Deviation from the dispatch brief recorded as a residual risk: the brief said "measured 16 (8+8)"; the tree re-measured at repair time, and D2 itself, say **9 goal + 9 team = 18** (`find .specify/specs -path '*/goal/*/goal.md'` = 9; `*/team/*/team.md` = 8 plus the one-level ND `team/team.md` = 9). The tasks-stage 16 is retained as a dated reading, not as the current denominator.

### L-4 — baseline ids

- `plan.md:262` (EP-006) — "44 baseline failures" → "46 baseline failing ids" (matches `test-evidence/plan-baseline-names.txt`: 46 unique ids).

### quickstart.md — stale-count sweep

- `quickstart.md:1` — title `Feature 092` → `Feature 094` (renumber residue; in-passing correction, disclosed).
- `quickstart.md:35,36,124` — fixture root `.specify/.tmp/s092` → `s094`.
- `quickstart.md:129` — "the 092 execution-lessons record" → `notes/execution-lessons-2026-11-09.md` (no feature-id token).
- Sweep result: **no** stale `80 rows` / `42 FR` / `111 clauses` / `43 map rows` occurrences existed in this file; the only numeric claim (`46 ids`, `quickstart.md:27`) is D2-correct and was left unchanged.

### Register

- `.specify/memory/register.md:193` — new row `R3-H-1…L-5@094`: round-3 finding set meaning, authority `notes/analyze-round3-findings.md` + the two repair ledgers, status `open（repair round 3 running）`. The existing `C-01…L-03@094` row (line 192) is untouched.

## Gate reading

`python3 .specify/scripts/python/validate-requirements.py .specify/specs/094-goal-team-parallel/requirements.md`

```
status: ok
  [id-contiguous] pass (0)   [doc-order] pass (0)   [ref-resolvable] pass (0)
  [marker-count] pass (0)    [dup-id] pass (0)      [path-marker] pass (0)
scanned: 326 lines, 55 definition rows, 6 shared strings
0 error(s), 0 warning(s)     EXIT=0
```

Transient during the edit (self-caught, recorded not hidden): the first post-edit run exited 1 with 3 `dup-id` errors because the new Notes bullets used the `- **FR-007**` profile, which the validator counts as a second definition row; the bullets were converted to plain `FR-007 — …` text and the final reading above is clean. FR/SC counts measured independently: 43 FR definitions, 12 SC definitions.

Cross-file gates were **not** run (driver's full set runs after both writers finish), per dispatch.

## Residual risks

1. **D4 path vocabulary is now split across artifacts.** `requirements.md` / `plan.md` / `feature-ref.md` say `.specify/anchoring/`, but the contract pages still carry `.specify/goal/` in live normative clauses: `contracts/binding-and-lifecycle.md` C-10 (`:61`), C-13 (`:75`), C-15 (`:88`); `contracts/unified-archive-and-migration.md` C-31 (`:10-11`), C-112 (`:125`); `contracts/handoff-contract.md` C-58 (`:36`), C-59 (`:42`), C-66 (`:66`); `contracts/owner-rewrites-and-tests.md:57`. This repair wave assigned D4 to R2 (requirements/plan/registry side) and contracts to R1 (D1/H-2/M/L), so the contracts path sweep is **unowned** — it needs an explicit follow-up before the cross-file gates can be green on this axis.
2. `features.md:4` still declares `Total Features: 87` while the table has 88 rows / 88 distinct ids after the 092→094 renumber. The registry header is outside the `| 094 |`-row-only territory; flagged for the driver.
3. L-2 count reconciliation (dispatch's 16 vs D2/tree's 18) is recorded in EP-002 with all readings; if the driver prefers a different canonical denominator, EP-002 is the single edit point.
4. L-03 residual survives: `team/094-goal-team-parallel/team.md` still carries `name: SDD Temporary Team 092` (create-team generation naming; out of round-3 scope, unchanged).
5. Dated records were not rewritten (D5): the Clarifications Q2/Q13/Q14 semantics and the round-1/round-2 session records keep their original values; the D4 ruling is recorded additively in plan T-004 and the new Notes subsection rather than as a new renumbered Q row.
6. R1's concurrent edits (contracts, tasks.md, coverage-baseline) were not touched by this writer; the diff's non-territory entries belong to that writer/driver activity.
