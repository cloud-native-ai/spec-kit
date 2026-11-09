# Fix W2 — analyze round 4 (fork fix writer, 2026-11-09)

**Worker**: W2 (fork fix writer). **Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master`,
HEAD `ea799326`. No commits, no push, no subagents; no cross-file gates run. Territory: `quickstart.md`,
`feature-ref.md`, `data-model.md`, `plan.md`, `requirements.md`, `research.md`, `.specify/memory/features.md`
(header + `| 094 |` row), `.specify/memory/features/094.md`, `team/094-goal-team-parallel/team.md`.
Sibling W1 owns `contracts/*`, `tasks.md`, `coverage-baseline.txt` — none of those was touched.

Inputs read: `notes/analyze-round4/vc-anchoring.md`, `notes/analyze-round4/vb-consistency.md`,
`notes/analyze-round4/va-closures.md`, `notes/analyze-round3-findings.md` § D4, and the W3 body
(`notes/analyze-round3/w3-trunk-reconciliation.md`). Every count re-measured on the tree this session.

---

## 1. Per-id record (file:line before → after)

### VC H-3 (HIGH) — quickstart executable lines → `.specify/anchoring`

| file:line | before | after |
|---|---|---|
| `quickstart.md:42` | ``the definition lands at `.specify/goal/demo-command-goal/goal.md` `` | ``the definition lands at `.specify/anchoring/demo-command-goal/goal.md` `` |
| `quickstart.md:64` | ``each definition exists at `.specify/goal/<slug>/goal.md` / `.specify/teams/<slug>/team.md` `` | ``each definition exists at `.specify/anchoring/<slug>/goal.md` / `.specify/teams/<slug>/team.md` `` |
| `quickstart.md:80` | `sha256sum .specify/goal/demo-command-goal/goal.md` | `sha256sum .specify/anchoring/demo-command-goal/goal.md` |
| `quickstart.md:82` | `sha256sum .specify/goal/demo-command-goal/goal.md` | `sha256sum .specify/anchoring/demo-command-goal/goal.md` |

Spec-local paths kept: S-1 fixture root `.specify/.tmp/s094/s1/.specify/specs/900-fixture`, the
“`.specify/specs/` gains **no** goal/team path” assertion, and `.specify/teams/**` occurrences are untouched.

### VC H-4 (HIGH) — feature-ref SC-012 row

| file:line | before | after |
|---|---|---|
| `feature-ref.md:92` | ``every `.specify/goal/*/goal.md` and `.specify/teams/*/team.md` resident …`` | ``every `.specify/anchoring/*/goal.md` and `.specify/teams/*/team.md` resident …`` |

Mapping membership unchanged: the row still maps SC-012 → `tests/contract/test_resident_backfill.py`; no other
cell, anchor or count on the page moved.

### VC H-5 (HIGH) — data-model design rules

| file:line | before | after |
|---|---|---|
| `data-model.md:21` | ``Path `.specify/goal/<slug>/goal.md` (C-31)`` | ``Path `.specify/anchoring/<slug>/goal.md` (C-31)`` |
| `data-model.md:42` | must not include `` `.specify/goal/**` `` or `` `.specify/teams/**` `` (C-15) | must not include `` `.specify/anchoring/**` `` or `` `.specify/teams/**` `` (C-15) |

### VC M-5 — EP-002 / A6 denominator reading (one canonical value, dated history)

Re-measured on this tree (2026-11-09, HEAD `ea799326`), two readings because the tree has two shapes:

- **Probe form (C-43 globs `*/goal/*/goal.md`, `*/team/*/team.md`)**: goal **9** + team **8** = **17** — canonical.
- **Full census (all spec-local definition files)**: goal **9** + team **10** = **19**; the two extra files are
  one-level non-conforming `team/team.md` under `088-speckit-visualization/` and `092-non-disposable/` (both
  tracked, both `lifecycle_state: active`; `.specify/specs/088-speckit-visualization/fixtures/…/team.md` is a
  fixture, excluded).
- **Historical readings, kept with dates**: plan entry 7 goal / 7 team = 14 (`test-evidence/requirements-baseline-probe.txt`,
  2026-11-09); tasks stage 8 / 8 = 16 (tasks.md N-4, 2026-11-09). The prior `18 = goal 9 / team 9, one
  non-conforming` record matched neither shape and is superseded.

| file:line | before | after |
|---|---|---|
| `plan.md:53` | “18 spec-local definition files measured 2026-11-09 (goal 9 / team 9; the team side includes one non-conforming `092-non-disposable/team/team.md` at a one-level path — plan-entry baseline … 7 / 7 … tasks-stage reading was 8 / 8 …, and the residual probe remains the authority over all three numbers)” | “spec-local definitions measured 2026-11-09 at analyze-repair round 4: the residual probe's own form (`*/goal/*/goal.md`, `*/team/*/team.md`, C-43) reads goal 9 / team 8 = 17, and the full census adds two one-level non-conforming team files (`088-speckit-visualization/team/team.md`, `092-non-disposable/team/team.md`), goal 9 / team 10 = 19 definition files; the earlier readings keep their dates — plan entry 7 goal / 7 team = 14 (…, 2026-11-09) and tasks stage 8 / 8 = 16 (tasks.md N-4, 2026-11-09) — and the residual probe remains the authority over every number” |
| `plan.md:258` (EP-002) | “plan-entry 7 goal / 7 team, tasks-stage 8 / 8 (tasks.md N-4), repair-stage 2026-11-09 goal 9 / team 9 definition files (the team side includes one non-conforming `092-non-disposable/team/team.md`)” + evidence “analyze-repair round 3 (goal 9 / team 9 files, one at a one-level …)” | “plan-entry 7 goal / 7 team = 14, tasks-stage 8 / 8 (tasks.md N-4), analyze-repair round 4 (2026-11-09) probe-form reading goal 9 / team 8 = 17, with the full census at goal 9 / team 10 = 19 definition files (two one-level non-conforming team files: `088-speckit-visualization/team/team.md`, `092-non-disposable/team/team.md`)” + evidence “analyze-repair round 4 (probe form goal 9 / team 8 = 17; full census goal 9 / team 10 = 19, two files at one-level non-conforming paths)” |
| `requirements.md:320` (A6) | “2026-11-09 analyze-repair round 3 复测（本阶段）：`<kind>/<slug>/` 形态 goal 9 / team 8，另加 `092-non-disposable/team/team.md` 一条一级非规范层级，合计 goal 9 / team 9” | “2026-11-09 analyze-repair round 4 复测（本阶段）：`<kind>/<slug>/` 形态（探针口径，C-43）goal 9 / team 8 = 17，另有一级非规范层级两条（`088-speckit-visualization/team/team.md`、`092-non-disposable/team/team.md`），全量定义文件计 goal 9 / team 10 = 19；历史读数按日期保留：plan 入口 7 / 7 = 14（…，2026-11-09），tasks 阶段 8 / 8 = 16（tasks.md N-4，2026-11-09）” |

The A6 comparative-baseline sentence (“该复测不替换本条的比较基线——SC-003 的基线仍取本特性第一个实现提交之前的探测读数”)
is kept verbatim; the 6 goal / 12 team archive counts in EP-002 re-verified this session (`ls -d` = 6 / 12) and kept.

### VC M-6 — requirements identity line

| file:line | before | after |
|---|---|---|
| `requirements.md:14` | `**Feature ID**: 092` | `**Feature ID**: 094` |

### VB-3 — research R-25 baseline count 44 → 46 (dated)

| file:line | before | after |
|---|---|---|
| `research.md:115` | “`test-evidence/plan-baseline-names.txt` (44 ids, measured this session)” | “(46 ids, measured this session 2026-11-09; corrected at analyze round 4, 2026-11-09, from an earlier 44 reading — the file holds 46 unique ids)” |

Evidence re-measured: `wc -l` = 46, `sort -u | wc -l` = 46.

### VC L-2 — 092 titles

| file:line | before | after |
|---|---|---|
| `data-model.md:1` | `# Data Model — Feature 092` | `# Data Model — Feature 094` |
| `research.md:1` | `# Research — Feature 092 (Phase 0)` | `# Research — Feature 094 (Phase 0)` |

### VC M-3 — features.md header count

| file:line | before | after |
|---|---|---|
| `features.md:4` | `**Total Features**: 87` | `**Total Features**: 88` |

Independently verified this session: `grep -cE '^\| [0-9]{3}'` = **88** rows; `grep -oE '^\| [0-9]{3}' | sort -u | wc -l`
= **88** distinct ids.

### VB-1 — registry status is the current truth

| file:line | before | after |
|---|---|---|
| `features.md:101` (`\| 094 \|` row) | “…+ 4 MEDIUM + 5 LOW，**repair round 3 进行中**（…）；2026-11-09 renumber：…；下一阶段 = repair round 3 收口 → analyze 第 4 轮” | “…+ 4 MEDIUM + 5 LOW（…）；repair round 3 已收口（commit `84d8765f`，H-1/H-2 闭合、六门全绿；注册行刷新 `2c704003`）；analyze 第 4 轮验证完成：VA PASS / VB 4 LOW / VC split（…`notes/analyze-round4/`）；锚定修复波次（W1/W2）进行中，下一阶段 = 修复集成 + 门复跑 → 终验 → implement 门；2026-11-09 renumber：…” |
| `features/094.md:56-68` | “…见 `notes/analyze-round3-findings.md`；**repair round 3 进行中**。修复账：…” | round-3 bullet keeps its finding text and repair ledgers, closes with “**repair round 3 已收口（2026-11-09，commit `84d8765f`，H-1/H-2 闭合、六门全绿；注册行刷新 `2c704003`）**”; new round-4 bullet records VA PASS / VB 4 LOW / VC split and the fix-wave next step |

Facts kept verbatim in both files: FR 43 / SC 12, 113 clauses (C-1…C-113), 83 tasks (T001–T083) / 7 packages
(15+17+19+8+16+6+2), 46-id baseline, round-1/2 analyze history.

### VC M-4 — team.md identity and live territory grants

Naming convention checked against siblings before editing: `089`/`090`/`091` all read `name: SDD Temporary Team <NNN>`
with NNN = the team's own spec id, so the generation-name pattern is kept and only the digits move.

| file:line | before | after |
|---|---|---|
| `team.md:2` | `name: SDD Temporary Team 092` | `name: SDD Temporary Team 094` |
| `team.md:4` | `description: Run-scoped SDD team for Feature 092 — …` | `description: Run-scoped SDD team for Feature 094 — …` |
| `team.md:17` | `territory.write` entry `.specify/goal/**` | entry `.specify/anchoring/**` |
| `team.md:37` | `territory.write` entry `.specify/memory/features/092.md` | entry `.specify/memory/features/094.md` |

`:9` / `:131` goal/charter prose mirroring the user brief stays per the VC keep-list. Because the fix closes
residual L-03, the L-03 bullet in `features/094.md:69-72` now records the closure instead of “留待后续判定”
(in-scope consequence of the team.md fix, disclosed here).

---

## 2. Validator reading (mandated)

Command after all edits:
`python3 .specify/scripts/python/validate-requirements.py .specify/specs/094-goal-team-parallel/requirements.md`

```
file: .specify/specs/094-goal-team-parallel/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 326 lines, 55 definition rows, 6 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

No other gate was run (cross-file gates are the driver’s after-W1+W2 integration step).

## 3. Post-fix sweep

- `.specify/goal` in territory now survives only at `team.md:9` and `team.md:131` (goal/charter prose, VC
  keep-list). Zero live hits remain in quickstart / feature-ref / data-model.
- `Feature 092` / `features/092.md` identity hits left in territory: only `requirements.md:262` (dated
  round-2 Clarification quote, D5 keep, not in my CLOSE set) and the L-03 closure note in `features/094.md`
  that quotes the old target. `tasks.md:3,5` (VB-4) are W1 territory.
- `research.md:1` / `data-model.md:1` titles now read 094; no stale 092 title remains in the spec dir.

## 4. Residual risks

1. **M-5 premise vs tree (see ANOMALY)**: W3’s “9 goal + 9 team” counts spec directories carrying a
   `team/` root, not definition files; the definition-level tree reads probe form 9/8 = 17 and census 9/10 = 19.
   The artifacts now state the tree reading; any later reader who quotes “9/9” will reintroduce the
   falsified denominator.
2. **One-level team files are disclosed, not dispositioned**: EP-002’s migration subject is what the C-43
   probe enumerates (17). Whether `088-speckit-visualization/team/team.md` and
   `092-non-disposable/team/team.md` are migrated (or their one-level form is refused) is a design decision
   for the implement stage, not settled by this fix; they may fail the probe silently if left as-is.
3. **`team.md` is live operational state**: `run-team` consumes it; only the four assigned lines changed and
   the YAML shape is unchanged, but no runtime check of the team file was run (no cross-file gates per brief).
4. **VB-2/VB-4 remain elsewhere**: `tasks.md:483` evidence pointer and `tasks.md:3,5` identity lines are W1
   territory; `requirements.md:262` keeps its dated 092 quote by D5. Round-4 closure of VB requires both
   writers’ output.
5. **features.md header is hand-maintained**: 88 is verified today by rows and distinct ids; the next
   renumber/merge must update it in the same commit or the drift recurs.

**ANOMALY**: the dispatch premise “spec-local definitions: 9 goal + 9 team per W3” is a directory-root count
(`ls -d .specify/specs/*/team` = 9), not a definition-file count — the measured tree reads probe form
goal 9 / team 8 = 17, full census goal 9 / team 10 = 19 (two one-level team files), so the three M-5 sites
record the tree reading per VC L-2 rather than the literal 9/9.
