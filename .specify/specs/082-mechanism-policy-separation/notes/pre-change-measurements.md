# Pre-change measurements — 082（implement Part 1, T001）

Captured 2026-11-05 (+08), branch `082-mechanism-policy-separation`, HEAD `8778d2bb`
(working tree carries the concurrent skill-reference implementation, folded into 082 by
user ruling `requirements.md` § A11 — it is this feature's delivery surface, not foreign drift).
Every reading below was re-taken in this stage; the plan-stage readings in
`test-evidence/plan2026-11-05-baseline.txt` are cited, never inherited.

## (a) Zero-drift baseline of the two regeneration entries (EP-005)

```
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (413 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (63 files)
rc=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

Delta against EP-005 (plan-time: `skills-external 409` / `shared 62`): `skills/external`
now carries 413 files and `shared/` 63 — the concurrent skill-reference implementation's
four new files, mirrored. Both pairs still report `ok`, so this is not drift; the
post-image counts are the ones this feature must return to (T036).

## (b) SC-003 denominator (closed-set comparison unit)

```
$ git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/ | wc -l
     575
$ git ls-tree -r --name-only 3ffeb26e -- skills/ | wc -l
     548
$ git ls-tree -r --name-only 3ffeb26e -- templates/commands/ | wc -l
      27
```

575 = 548 + 27, matching `tasks.md` § Environment Prerequisites EP-004.

## (c) Two owners' starting states

```
$ ls shared/definitions/mechanism-policy-definitions.md
ls: shared/definitions/mechanism-policy-definitions.md: No such file or directory
$ ls shared/definitions/skill-reference-definitions.md
shared/definitions/skill-reference-definitions.md
```

The mechanism/policy owner is **new** (T003–T006 author it); the skill-reference owner is
a **to-be-finalised draft** in the working tree (T007 verifies and closes gaps, never
re-authors).

## (d) Reference-string population (the SR-05 rewrite population)

```
$ grep -ro "skill-reference-definitions" skills/ | wc -l
       8
$ grep -rc "skill-reference-definitions" skills/ | grep -v ':0$'
skills/internal/run-skills/SKILL.md:2
skills/external/merge-skills/SKILL.md:1
skills/external/improve-skills/SKILL.md:1
skills/external/coaching-skills/SKILL.md:3
skills/external/create-skills/SKILL.md:1
$ grep -rno "\.specify/shared/definitions/skill-reference-definitions\.md" skills/ | wc -l
       8
```

8 reference strings, all eight in the `.specify/` mirror form — the whole population
T035 converts. Per-file split (1 / 1 / 1 / 3 / 2) matches `research.md` § R11 / SR-05.

## (e) Test coverage of the skill-reference and mechanism/policy surface

```
$ ls tests/contract/ | grep -cE "mechanism_policy|skill_reference"
0
```

Eleven contract modules plus one test-only helper are still to be authored (EP-006);
no `scripts/` file is planned.

## (f) `skill-shape.py` readings of the three edited `SKILL.md` files (EP-003)

Script: `skills/external/improve-skills/scripts/skill-shape.py <path/to/SKILL.md>`.
The path argument is a **file**, not a directory: passing the skill directory exits with
`{"error": "[Errno 21] Is a directory"}` and rc 0, which would silently read as a pass.

```
$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/create-skills/SKILL.md --quiet
rc=10
  正文估算     ≈5403 tokens 可控 / 预算 5000（249 行）
    ✗ [l1-token-budget] 可控正文 ≈ 5403 tokens > 预算 5000（L1 在触发时整体载入，超预算会稀释硬约束）

$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/improve-skills/SKILL.md --quiet
rc=10
  正文估算     ≈5722 tokens 可控 / 预算 5000（全文 6188，契约强制块 466）（157 行）

$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/merge-skills/SKILL.md --quiet
rc=10
  正文估算     ≈5134 tokens 可控 / 预算 5000（166 行）
```

All three are **already over budget before this feature** (debt, not an outage — EP-003);
the implement-time measurement is the delta, never exit 0.

Delta against the plan-time readings (≈5354 / ≈5584 / ≈5096): +49 / +138 / +38 tokens,
i.e. the concurrent implementation's wiring already sits inside these three bodies. T040's
"before" column is therefore this reading, not the plan-time one.

## Frozen registration (T002) — the surface T038 writes into

Read from `tests/contract/test_expression_compatibility.py` at `8778d2bb`; **nothing was
written into the module by this reading** (T038 owns the five registration points).

**`ALLOWED_POST_BASELINE_CHANGES` — exact key set, 21 entries**:

```
skills/internal/create-team/SKILL.md          skills/internal/analyze-artifacts/SKILL.md
skills/internal/run-agent/SKILL.md            templates/commands/analyze.md
skills/internal/manage-features/SKILL.md      templates/commands/skills.md
skills/external/sdd-loop-driver/SKILL.md      skills/internal/run-skills/SKILL.md
templates/commands/review.md                  templates/commands/feedback.md
skills/internal/code-review/SKILL.md          templates/commands/improve.md
skills/internal/review-sdd-process/SKILL.md   skills/internal/manage-feedback/SKILL.md
skills/internal/self-improvement/SKILL.md     skills/internal/create-tasks/SKILL.md
skills/internal/implement-feature/SKILL.md    skills/external/sdd-project-setup/SKILL.md
skills/internal/manage-constitution/SKILL.md  skills/internal/sanitize-materials/SKILL.md
templates/commands/sanitize.md
```

- **`skills/internal/run-skills/SKILL.md` is already a key** — reason `2026-10-30 Feature 078
  updates the run-skills routing-family pointer`, markers `('coaching-skills',)`. T038
  **updates** this entry (extends the reason to the skill-reference wiring, folds in the new
  wiring line's unique literal); it MUST NOT add a second key for the same path.
- **Four new keys are needed** — `skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md`.
  None of them is present today, and none collides with an existing 083 or other-feature row.
- `templates/commands/skills.md` is already keyed (a command-surface entry, unrelated to this
  feature's keyed set) — T022 / T037 must prove it byte-identical, not re-key it.

**`RENAMED_SKILL_REL` = `skills/external/coaching-skills/SKILL.md`** (confirmed). Because
`_retired_skill_register` asserts `len(missing) == 1` and that the retired path's grandparent
equals `RENAMED_SKILL_REL`'s grandparent, the directory `skills/external/coaching-skills/`
**must keep existing** for the register to remain decidable — deleting or moving it turns the
freeze into a broken assertion rather than a passing one. T032 edits that `SKILL.md` in place,
which satisfies the constraint.

**`WIRING_SKILLS` = `('skills/external/create-docs/SKILL.md', 'skills/external/humanize/SKILL.md')`**
— exactly `create-docs` / `humanize`, as D7 states. `test_c5` asserts `not any(rel in WIRING_SKILLS
for rel in skills)`; `WIRING_SKILLS` therefore also defines the **complement** of the frozen set
and MUST NOT gain a 082 entry (T038's "the hash list, `WIRING_SKILLS` and every assertion stay
intact").

**Consequence for T038's five points**: four new keys (create-skills / improve-skills /
merge-skills / coaching-skills) + one updated existing key (run-skills), each with a reason
naming its FR group and markers drawn from that skill's own newly added literals. No
`references/` file is registered — the frozen list does not cover them.

## Command surface (T022) — the command templates are untouched

Captured 2026-11-05 during implement Part 3B, at continuation baseline `02bef714`.
The three readings below are taken in the same run; each carries its own command line so
that a third party can recompute it without reading this file's prose.

```
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

Zero changed copies across the four per-tool trees that exist in this repository
(`.claude/commands`, `.github/prompts`, `.qoder/commands`, `.opencode/command` — 27
`speckit.*` copies each). `--check` writes nothing (its `--help` states "report drift,
write nothing"); it reports drift by exit status, and the status is 0.

```
$ git rev-parse 3ffeb26e:templates/commands/skills.md
53159b7bb27faf6e8eace2feee6eb423821e338a
$ git hash-object templates/commands/skills.md
53159b7bb27faf6e8eace2feee6eb423821e338a
```

`templates/commands/skills.md` is byte-identical to its `3ffeb26e` blob — the blob hash,
not a textual diff, is the reading.

```
$ git ls-tree -r --name-only 3ffeb26e -- templates/commands/ | wc -l    # denominator
27
$ <per-path loop> git rev-parse 3ffeb26e:$p vs git hash-object $p       # every path
(no CHANGED lines)
$ git diff --name-status 3ffeb26e..HEAD -- templates/commands/
(no output)
```

All 27 command templates are byte-identical to the baseline, and the history since
`3ffeb26e` contains no change to `templates/commands/` at all. T037 re-takes the same
two readings after the rewrite set, in the same shape, so the two are comparable.

**Consequence recorded for T022's stop clause**: the template did not need to change, so
the task's "stop and report" branch did not fire.

### T037 — the same reading after the full rewrite set

Re-taken 2026-11-05 in implement Part 5 with the same commands and the same shape, so it is
directly comparable with T022's reading above:

```
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0

$ git ls-tree -r --name-only 3ffeb26e -- templates/commands/ | wc -l
27
$ <per-path loop> git rev-parse 3ffeb26e:$p vs git hash-object $p   # every path
(no CHANGED lines; changed=0)
$ git diff --name-status 3ffeb26e..HEAD -- templates/commands/
(no output)
```

Zero changed copies, all 27 command templates byte-identical to the baseline, and still no
history change under `templates/commands/` — identical to T022's reading. Full capture:
`test-evidence/implement-part5-t036-t037.txt`.

## Reference coordinates (T034 audit, recorded before T035 rewrites)

Captured 2026-11-05 during implement Part 5, at HEAD `fa563b0e`, before any file below was
edited. The readable coordinate is **file + reference-string content + landing section**;
line numbers are reported only as the audit-time position and are never the identifying form
(lines drift with editing — `research.md` § R11 says the same for the plan-time reading).

| # | Consumer (framework source) | Reference string (exact) | Current path form | Landing section (audit time) |
|---|---|---|---|---|
| 1 | `skills/external/create-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § 1 Determine the creation source → Case A → `skill name` bullet (line 35) |
| 2 | `skills/external/create-skills/SKILL.md` | `shared/definitions/skill-reference-definitions.md` | **source** (added by T011) | § 2 Determine SKILL_HOME and metadata → `Both layers before any write` bullet (line 58) |
| 3 | `skills/external/improve-skills/SKILL.md` | `shared/definitions/skill-reference-definitions.md` | **source** (added by T014) | § Input Contract → `Target identifier` (line 20) |
| 4 | `skills/external/merge-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § Input Contract → `Source` parameter (line 27) |
| 5 | `skills/external/coaching-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § Inputs → `Trainee` parameter (line 26) |
| 6 | `skills/external/coaching-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § Trainee Resolution → normalize-first bullet (line 49) |
| 7 | `skills/external/coaching-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § Nested (chain) runs → intro line (line 69) |
| 8 | `skills/internal/run-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § Input Contract → `Target` parameter (line 16) |
| 9 | `skills/internal/run-skills/SKILL.md` | `.specify/shared/definitions/skill-reference-definitions.md` | mirror | § 1 解析 → step 0 归一化 (line 24) |

Counts at audit time: **7 mirror-path strings** (rows 1, 4–9) + **2 source-path strings**
(rows 2 and 3, added by T011 / T014 after T001(d) was taken). T001(d) measured the pre-rewrite
population (8 mirror strings, all mirror); the re-measurement here is 9 strings across the
same five files. Of the T001(d) population, the `improve-skills` string was already converted
to the source form by T014, so T035 converts the **7 remaining** mirror strings rather than
re-converting an already-converted one.

The rewrite's target population is those 7 mirror strings (SR-05 / GR-08, clarify ruling ②).
After the rewrite each consumer MUST carry **exactly one** source-path reference
(`test_skill_reference_consumers.py` SR-01…SR-06), so the two consumers that would end with
two (row 2 vs row 1, row 8 vs row 9) and the consumer that starts with three (rows 5–7)
collapse to one cited path each; the other landing points keep a pointer to the owner without
re-spelling its path.

## Why this reading set is stable

Three of the six readings changed between plan and now: (a) `skills-external 409 → 413` and
`shared 62 → 63`, and (f) all three token counts. All three changes trace to one cause —
the concurrent skill-reference implementation, which `requirements.md` § A11 folded into 082.
No reading changed for a reason this stage created.
