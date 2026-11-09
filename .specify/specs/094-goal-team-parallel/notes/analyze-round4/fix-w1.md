# W1 — fork fix writer report (analyze round 4, 2026-11-09)

**Worker**: W1, fork fix writer (write scope: `contracts/*.md`, `tasks.md`, `coverage-baseline.txt` only).
**Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`, branch `master`, base HEAD `ea799326`. No commits, no push, no subagents.
**Source of truth**: `notes/analyze-round4/vc-anchoring.md` §1 split table + §6 fix targets; `vb-consistency.md` VB-2; `va-closures.md` ANOMALY; `notes/analyze-round3-findings.md` § Decision sheet D4/D5.
**Convention**: all line numbers below are unchanged pre→post (same-line replacements; no line-count delta in any file). Every edit is a path/identity alignment — clause ids, green tags, counts and dated wording were preserved.

## Closed ids

### H-1 — the 9 live normative contract lines (`.specify/goal` → `.specify/anchoring`)

| file:line | clause | before (fragment) | after (fragment) |
|---|---|---|---|
| `contracts/binding-and-lifecycle.md:61` | C-10 | `resolve the goal root to `.specify/goal`` | `resolve the goal root to `.specify/anchoring`` |
| `contracts/binding-and-lifecycle.md:75` | C-13 | `write target outside `.specify/goal/<slug>/`` | `write target outside `.specify/anchoring/<slug>/`` |
| `contracts/binding-and-lifecycle.md:88` | C-15 | `write into `.specify/goal/**`` | `write into `.specify/anchoring/**`` |
| `contracts/unified-archive-and-migration.md:10` | C-31 | `MUST be exactly `.specify/goal/<slug>/`` | `MUST be exactly `.specify/anchoring/<slug>/`` |
| `contracts/unified-archive-and-migration.md:11` | C-31 | `lives at `.specify/goal/<slug>/goal.md`` | `lives at `.specify/anchoring/<slug>/goal.md`` |
| `contracts/handoff-contract.md:36` | C-58 | `MUST resolve to `.specify/goal/<goal_slug>/goal.md`` | `MUST resolve to `.specify/anchoring/<goal_slug>/goal.md`` |
| `contracts/handoff-contract.md:42` | C-59 | `two other sides: `.specify/goal/<goal_slug>/goal.md`` | `two other sides: `.specify/anchoring/<goal_slug>/goal.md`` |
| `contracts/handoff-contract.md:66` | C-63 | `MUST NOT include `.specify/goal/**`` | `MUST NOT include `.specify/anchoring/**`` |
| `contracts/owner-rewrites-and-tests.md:57` | C-100 | `land only in `.specify/goal/`` | `land only in `.specify/anchoring/`` |

Kept per dispatch: the file name `goal.md` and the spec-local store `<spec>/goal/<slug>/goal.md` are untouched; only the global tree moved. Post-edit `grep -rn '\.specify/goal' contracts/` = **0 hits**; `grep -rc '\.specify/anchoring' contracts/*.md` = 3 + 3 + 1 + 3 = **10 lines, matching the split table's 10 line occurrences**.

### H-2 — the 5 normative instruction rows in tasks.md

| file:line | row | before (fragment) | after (fragment) |
|---|---|---|---|
| `tasks.md:176` | US1 Independent Test | `assert both land under `.specify/goal/<slug>/`` | `assert both land under `.specify/anchoring/<slug>/`` |
| `tasks.md:220` | T037 [US2] | `archive layout is `.specify/goal/<slug>/goal.md`` | `archive layout is `.specify/anchoring/<slug>/goal.md`` |
| `tasks.md:321` | T073 (FR-029) | `name only `.specify/goal/`` | `name only `.specify/anchoring/`` |
| `tasks.md:330` | T081 | `every `.specify/goal/*/goal.md`` | `every `.specify/anchoring/*/goal.md`` |
| `tasks.md:400` | 085 disposal row 11 | `goal path moves to `.specify/goal/<slug>/`` | `goal path moves to `.specify/anchoring/<slug>/`` |

Post-edit `grep -n '\.specify/goal' tasks.md` = **0 hits**.

### M-1 — C-112 dated measurement path

- `contracts/unified-archive-and-migration.md:125` (C-112): `Measured 2026-11-09: `.specify/goal/*/goal.md` carries 6` → `Measured 2026-11-09: `.specify/anchoring/*/goal.md` carries 6`.
- **Count 6 kept** (dated live reading, not a historic pre-rename tree): re-measured this run — `.specify/anchoring/` holds 6 slug dirs / 6 `goal.md` files, `.specify/teams/` 12 slug dirs; both counts reproduce.

### M-2 — C-93 dead section title

- `contracts/owner-rewrites-and-tests.md:22` (C-93): `§ Temporary Goal/Team MUST be retitled and rewritten` → `§ Goal/Team（085） MUST be retitled and rewritten`.
- Verified the named heading exists: `skills/external/sdd-loop-driver/SKILL.md:45` reads `**Goal/Team（085）**：…`; no `Temporary Goal/Team` heading exists on the tree.

### M-6 — identity residues in tasks.md

| file:line | before | after |
|---|---|---|
| `tasks.md:3` | `**Requirement ID**: 092` | `**Requirement ID**: 094` |
| `tasks.md:5` | `**Related Feature**: 092 goal/team 与 spec 的平行关系…` | `**Related Feature**: 094 goal/team 与 spec 的平行关系…` |

(The key line `:4` already read `094-goal-team-parallel`; the file no longer contradicts itself.)

### M-7 — N-2 version point

- `tasks.md:472`: `the next minor release after 092` → `the next minor release after 094` (after the renumber, bare `092` denotes the Non-Disposable archive lineage; the ruling is about this line's alias removal point).

### M-8 — premises re-derivation command

- `tasks.md:96`: `` `basename -a .specify/goal/*/ | wc -l` `` → `` `basename -a .specify/anchoring/*/ | wc -l` ``. Measured value **6 goal / 12 team kept**; the aligned command reproduces it (6 / 12, measured this run).

### L-1 — fixture/context 092 tokens

| file:line | before | after |
|---|---|---|
| `tasks.md:143` (T003) | `.specify/.tmp/s092/probe/.specify/specs/900-fixture/` | `.specify/.tmp/s094/probe/.specify/specs/900-fixture/` |
| `tasks.md:490` | `tree under `.specify/.tmp/s092/`` | `tree under `.specify/.tmp/s094/`` |
| `tasks.md:491` | `follows the pre-092 protocol … so 092's spec-local goal and team` | `follows the pre-094 protocol … so 094's spec-local goal and team` |

Fixture root now agrees with `quickstart.md`'s `.specify/.tmp/s094` form.

### L-3 — Phase 4 heading

- `tasks.md:200`: `## Phase 4: User Story 2 - 档案统一落 `.specify/goal/` 与 `.specify/teams/`…` → `## Phase 4: User Story 2 - 档案统一落 `.specify/anchoring/` 与 `.specify/teams/`…` (cosmetic alignment per the split table).

### VA / VB-2 — mispointed pre-analyze evidence

- `tasks.md:483`: ``kept verbatim at `test-evidence/analyze-repair2-gates-requirements.txt` `` → ``kept verbatim at `test-evidence/pre-analyze-tasks-analyze-repair.json` ``.
- Verified before editing: `analyze-repair2-gates-requirements.txt` contains no pre-analyze-check section and its FR lane reads `43 of 43`; `pre-analyze-tasks-analyze-repair.json` exists with `"summary": {"fr": 42, "sc": 11, "tasks": 80}`, `"decision": "pass"`, `checked_at 2026-11-09T08:20:54Z`. The sentence's `42/42` reading now matches the file it cites.

### Baseline header (VA anomaly, second half)

- `coverage-baseline.txt:2`: `# frozen-from: /storage/project/cloud-native-ai/spec-kit/.specify/specs/*/contracts/* …` → `# frozen-from: .specify/specs/*/contracts/* …` — repo-relative corpus-root form, matching the prior freeze (`84d8765f^` header) and the freeze writer's own emission (`account-clause-coverage.py:461` writes `corpus_root.as_posix()`, so a relative `--corpus-root` yields exactly this form).
- **Header only**; `diff` of the `#`-stripped file vs HEAD: **identical** — 599-name set untouched. `base-sha: abfc12d19412 | files: 308 (parsed 193 + named 115)` kept verbatim. No consumer reads `frozen-from` (`grep -rn frozen-from tests/ scripts/ .specify/scripts/` → only the writer line).

## Gate reading (mandated)

`python3 .specify/scripts/python/validate-tasks.py .specify/specs/094-goal-team-parallel/tasks.md` → verbatim:

```
WARN  239: blockedBy: T043 references later task T054 (forward dependency — verify this is intentional)
PASS (with warnings): .specify/specs/094-goal-team-parallel/tasks.md — 0 error(s), 1 warning(s)
EXIT=0
```

Same reading as the round-3/4 baseline: 0 errors, the one disclosed forward edge `T043 → T054`. No cross-file gates were run (per dispatch). Contract edits add/remove no clause marker and touch no citation group, so the clause universe and FR lane are unaffected by construction; `grep -cE '^- \*\*C-[0-9]+\*\*:' contracts/*.md` still reads 30 / 24 / 18 / 20 / 21 = 113.

## Residual risks

1. **`tasks.md:94–95, 474` keep pre-renumber `092` identity inside dated notes** — the premise rows (`8 (085–092)`, "092's own spec-local goal") and N-4 ("092's own spec-local goal and team", "16 definitions") were measured at generation time (2026-11-09) when this line was still 092. VC's split table classified them as dated/explanatory (not live residues) and the dispatch did not name them, so they were kept per D5. An implement-stage reader could confuse `092` with the Non-Disposable lineage; the premise table's own re-measurement mandate (T004) and N-4's `(N-4)` back-reference are the mitigating pointers. Note also N-4's "16 definitions" predates the round-3 re-derivations (probe-visible 17 / all 19 per VC L-2, which W2 is fixing in plan.md/requirements.md) — tasks.md still carries the old arithmetic in this dated ruling.
2. **C-112's count 6 is a live clause with an embedded dated reading** — it reproduces today (6 / 12 measured this run), but any archive change before implement entry invalidates it; C-52's rule already forbids restating the number as a constant elsewhere, and the T083 row requires a re-measured denominator.
3. **`analyze-repair2-gates-requirements.txt` remains cited in dated round-3 notes** (`w2-traceability.md:88,105`, `repair-r1.md:28`) where the citation is accurate as a coverage/validate record; only the tasks.md pre-analyze pointer was wrong and is now re-pointed. Those dated notes were not touched.
4. **Sibling W2 writes share this working tree** — the working-tree diff also shows changes in `data-model.md`, `feature-ref.md`, `plan.md`, `quickstart.md`, `requirements.md`, `research.md` that are W2's, not W1's; none of them was edited or read-in-place by W1 beyond verification greps.
