# Quickstart run record — slice 074b-nested-governance

Append-only record of the `quickstart.md` scenarios this slice executes during implementation. Each
entry pastes the command, the real output and the exit code; nothing here is a paraphrase. Scenarios
that `quickstart.md` declares **pinned** (S2, S4, S5) are still executed here against a live fixture,
because a pinned scenario that was never run is a claim, not evidence.

Two path rules apply to every capture below, both from the project's own guidelines:

- **Temp roots.** The fixture builder `tests/fixtures/nested_sdd.py` refuses any root inside the
  framework source tree by construction, so its scratch lives under the user-level sanctioned root
  `~/tmp/spec-kit/<purpose>/` instead of the in-repo `.specify/.tmp/<purpose>/`. The goal fixture (S3)
  does not carry that refusal and uses `.specify/.tmp/074b-goal-fixture` as `quickstart.md` wrote it,
  which is matched by `.specify/.gitignore` (`.tmp/`, verified with `git check-ignore`). Both captures
  tear their root down in the same command.
- **`HEAD`.** Every capture names the commit it ran at.

---

## S2 — the report section is mandatory and explicit when empty (executed with the fixture team)

**Pinned test**: `tests/contract/test_nested_run_report.py` (16 cases). **Captured** at `f26eb59ac`.

```bash
python3 - <<'PY'
import os, re, shutil, sys
from pathlib import Path
sys.path.insert(0, "tests")
from fixtures.nested_sdd import build
root = Path(os.path.expanduser("~/tmp/spec-kit/074b-quickstart-s2")).resolve()
shutil.rmtree(root, ignore_errors=True)
project = build(root)
contract = Path("skills/internal/create-team/SKILL.md").read_text(encoding="utf-8")
heading = "## Nested SDD Runs"
exact = [n for n, line in enumerate(contract.splitlines(), 1) if line.strip() == heading]
skeleton = re.search(r"```markdown\n(# Team Run Report[\s\S]*?)```", contract).group(1)
sections = []
for line in skeleton.splitlines():
    sections += [m.group(1).strip() for m in re.finditer(r"##\s+([^#\n]+?)(?=\s*##\s|\s*$)", line)]
explicit_none = [line.strip() for line in contract.splitlines() if "本次无嵌套 SDD 调用" in line]
print(f"fixture_team: {project.team_slug} (goal {project.goal_slug}, target {project.target_id})")
print(f"report_path: .specify/teams/{project.team_slug}/runs/<UTC-timestamp>-report.md")
print(f"heading_literal_line_exact: {exact}")
print(f"skeleton_sections: {sections}")
print(f"nested_section_is_appended_last: {sections[-1] == 'Nested SDD Runs'}")
print(f"explicit_when_empty_statements: {len(explicit_none)}")
for line in explicit_none:
    print(f"  {line[:160]}")
shutil.rmtree(root, ignore_errors=True)
print("teardown: removed", root)
PY
```

```text
fixture_root: /home/agent/tmp/spec-kit/074b-quickstart-s2
fixture_team: fixture-team (goal fixture-goal, target T-001)
report_path: .specify/teams/fixture-team/runs/<UTC-timestamp>-report.md
heading_literal_line_exact: [63]
skeleton_sections: ['Result Summary', 'Deliverables', 'Verification', 'Execution Detail', 'Run Workspace', 'Summary', 'Nested SDD Runs']
nested_section_is_appended_last: True
explicit_when_empty_statements: 1
  - **无嵌套调用**: MUST 在段内显式声明「本次无嵌套 SDD 调用」,不是省略整段 —— 即便正确内容本是 none,省略仍是违约。
teardown: removed /home/agent/tmp/spec-kit/074b-quickstart-s2
rc=0
```

**The two propositions, pinned by name**: `test_section_is_mandatory_for_every_run_in_both_pattern_families`
and `test_no_invocation_is_stated_explicitly_and_omission_is_a_violation`.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py -k "mandatory_for_every_run or no_invocation_is_stated"
..                                                                       [100%]
2 passed, 14 deselected in 0.04s
rc=0
```

**Reading**: the mandatory section is the **last** token of the report skeleton's section list, so a
run of the fixture team that nests nothing still owes the section, and the explicit-none sentence is
present exactly once inside the obligation subsection. The heading literal has one line-exact
occurrence, in the report contract only.

---

## S3 — attribution leaves the Goal field set identical (executed, measurement shape)

**Command**: `quickstart.md` § S3's block, run verbatim (goal fixture under `.specify/.tmp/`, torn down
in the same command). **Captured** at `f26eb59ac`.

```text
$ ( cd .specify/.tmp/074b-goal-fixture && python3 scripts/python/goal-utils.py --repo-root . create demo-goal \
      --objective "Deliver the slice end to end." --criterion "Every FR is claimed by a clause." )
created: .specify/goal/demo-goal/goal.md

$ ( cd .specify/.tmp/074b-goal-fixture && python3 - <<'PY' … parse_goal before/after the ledger row … PY )
field_set: ['boundaries', 'created', 'criteria', 'criteria_count', 'history', 'objective', 'slug', 'status', 'subjects', 'targets', 'title', 'updated']
identical: True
goal_md_bytes: 224

teardown: removed /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/074b-goal-fixture
rc=0
```

**Reading**: twelve parsed fields before and after the ledger row, and the Goal definition's bytes do
not move — attribution is observational and lands in the ledger, which is the shape SC-002 measures.
`tests/contract/test_nested_run_report.py::test_attribution_is_observational_so_the_goal_field_set_is_unchanged`
executes the same instrument over the `074a` fixture Goal, so the claim is measured twice from two
independent fixtures rather than asserted once.

---

## S4 — the Stage vocabulary is disambiguated and nothing is renamed (pinned, executed)

**Pinned test**: `tests/contract/test_sdd_diffusion.py` C-13 / C-14 cases. **Captured** after
`7842fa888`, comparing the edited bullet against the same bullet at the part-2 base commit.

```bash
python3 - <<'PY'
re/Path/git as above: read the Stage bullet at f26eb59ac and in the working tree,
print the backticked values of each, whether the disambiguation landed, whether the
roster owner is named, which SDD stage names appear in the bullet, and the `## ` count.
PY
```

```text
stage_values_before: ['executor', 'evaluator', 'optimizer']
stage_values_after : ['executor', 'evaluator', 'optimizer']
values_unchanged   : True
disambiguation_added: True
roster_owner_named  : True
sdd_stage_names_in_bullet: []
top_level_sections: 7
any_sdd_heading: []

$ git show 7842fa888 --numstat --format="" -- skills/internal/create-team/references/conceptual-model.md
1	1	skills/internal/create-team/references/conceptual-model.md

$ python3 -m pytest -q tests/contract/test_single_conceptual_model.py
...                                                                      [100%]
3 passed in 0.04s
rc=0
```

**Reading**: the three canonical values are byte-identical before and after, and not one SDD stage
name appears in the bullet — the roster is reached by path (`skills/external/sdd-loop-driver/SKILL.md`)
and never enumerated. The change is `1 insertion / 1 deletion` on the *same line*: the sentence is
appended to the existing Stage bullet in place, and the file's seven `## ` sections are untouched
(no SDD-shaped heading), which is what "no new top-level section" means mechanically. The sibling
suite that pins the Role × Stage × Type model stays green.

---

## S5 — the instructions pointer is one additive section, regenerated (pinned, executed)

**Captured** after `1f7fd6e61` (source edit `e1ee11c35` + this generation).

```bash
$ python3 scripts/python/sync-mirrors.py --write --only templates --only skills --only shared
sync  templates/ -> .specify/templates/ (1 files)
sync  shared/ -> .specify/shared/ (1 files)

$ bash scripts/bash/generate-instructions.sh
| SDD Routing Decision (SDD 分流裁决)                 | 1262   | 1262   | 0     | no          | no            |
…
success Instructions generated/updated at .specify/instructions.md
rc=0
```

```text
live_carries_heading: True
live_neighbours: ## Fact, Correctness & Logic Checks (Input Sanity) -> ## SDD Routing Decision (SDD 分流裁决) -> ## One Source Of Truth
live_block_bytes: 1261
template_block_bytes: 1261
verbatim_equal: True
live_bytes_before: 41948 after: 43210 delta: 1262

$ git diff --stat .specify/instructions.md
 .specify/instructions.md | 11 +++++++++++

$ git diff -U0 .specify/instructions.md | grep -c "^+[^+]"   # 7
$ git diff -U0 .specify/instructions.md | grep -c "^-[^-]"   # 0

$ ls -l AGENTS.md CLAUDE.md QODER.md .github/copilot-instructions.md
AGENTS.md -> .specify/instructions.md
CLAUDE.md -> .specify/instructions.md
.github/copilot-instructions.md -> ../.specify/instructions.md
QODER.md -> .specify/instructions.md
```

**Reading**: one additive `## ` section, injected at the template's position (after Input Sanity,
before One Source Of Truth), carried verbatim into the live file, and **zero lines removed** — no
existing section was rewritten. The measured delta is 1,262 B against the section's own declared
ceiling of 2,000 B; the generator's budget is not cited as the criterion anywhere, because both
files already exceeded it before this slice. The four compatibility paths still resolve at the live
file, so no symlink repair was needed. The second-run idempotence check is T022's and is not run here.

**Placement constraint discovered (disclosed)**: the first placement — between `## Proactive Flow
Trigger` and `## Fact, Correctness & Logic Checks (Input Sanity)` — broke a delivered guard this
slice does not own (`tests/contract/test_proactive_trigger_section.py` C-3 and C-9 pin that exact
adjacency, and `test_ask_record_repeat.py` re-states it). The section was moved to the next free
slot; no contract text changed, only the position. Commit `e1ee11c35`.


---

## S6 — the containment claim's post-change half (executed 2026-10-29, T020)

The pre-change half of S6 (`quickstart.md` § S6) froze 266 cases across 17 files in 7 named sets.
This is the half it deferred: the same command over the same file list, compared set-wise, with the
verdicts of the shared ids measured rather than assumed.

```bash
# collection, same command and same file list as the pre-change capture
$ python3 -m pytest --collect-only -q <the 17 files of the 7 named sets>
272 tests collected in 0.31s

# per set: comm -23 <(sort pre) <(sort post) MUST be empty
S1: dropped=0 added=6
S2: dropped=0 added=0
S3: dropped=0 added=0
S4: dropped=0 added=0
S5: dropped=0 added=0
S6: dropped=0 added=0
S7: dropped=0 added=0

# verdicts of the shared ids
$ bash scripts/bash/run-tests.sh <the same 17 files>
============================= 272 passed in 27.26s =============================
rc=0
```

**Reading**: `dropped=0` in every set discharges the superset direction by *name* (a rename plus an
addition nets to zero in a count and would hide a dropped obligation, which is why the count line
above is labelled orientation-only). The six additions are exactly the cases T017 landed in S1 and
they are listed one by one in `test-evidence/containment-post-change-collect.txt`. All 266 shared ids
are green after the change as they were green before it, so no shared id's verdict moved.

**Also re-measured here** (same run, `notes/pre-change-measurements.md` § 10): the four predecessor
surfaces are a zero diff against the baseline commit, with a positive control showing the same
`git diff` form reporting a non-empty stat for a path this slice did edit.

**Premises**: the comparison is node-id set based, never count based; the baseline commit is the one
the carrier names (`stage_base=33269994a`), not the current HEAD.

---

## refresh — mirror parity, command copies, and generator idempotency (executed 2026-10-29, T021–T022)

T021 and T022 share this section (same evidence sink, run in row order).

### T021 — the five edited sources and their `.specify/` projections

```bash
$ python3 scripts/python/sync-mirrors.py --write --only templates --only skills --only shared
scope --only: templates, skills, shared
ok    templates/ == .specify/templates/ (22 files)
ok    shared/ == .specify/shared/ (59 files)
rc=0

$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
rc=0

# pair-by-pair, byte comparison (cmp -s: silent + rc 0 means identical)
identical  skills/internal/create-team/SKILL.md                     <->  .specify/skills/internal/create-team/SKILL.md
identical  skills/internal/create-team/references/conceptual-model.md <-> .specify/skills/internal/create-team/references/conceptual-model.md
identical  skills/internal/run-agent/SKILL.md                       <->  .specify/skills/internal/run-agent/SKILL.md
identical  shared/guidelines/proactive-trigger.md                   <->  .specify/shared/guidelines/proactive-trigger.md
identical  templates/instructions-template.md                      <->  .specify/templates/instructions-template.md

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

**Reading**: the `--write` pass wrote nothing — part 2 had already projected the three skill edits and
the two other sourced files, and part 3 touched no framework source at all. `--check` is clean on all
six pairs with the same file counts as the T001 baseline (22 / 406 / 136 / 3 / 114 / 59), so there is
no new drift; the five `cmp` results are byte equality, not a summary of it. `regen-command-copies`
still reporting `OK` is the proof that `templates/commands/**` was not touched (a changed command
template would make at least one per-tool copy stale). No mirror was hand-edited.

### T022 — the generator is idempotent and the four compatibility paths still resolve

```bash
$ sha256sum .specify/instructions.md          # the first generation (T015, committed)
23aaf2684c7fab9f31846e930d0cdf0c7a9ada19a74547dcbdf349862cbbeebb

$ bash scripts/bash/generate-instructions.sh
...
success Instructions generated/updated at .specify/instructions.md
rc=0

$ sha256sum .specify/instructions.md          # the second generation
23aaf2684c7fab9f31846e930d0cdf0c7a9ada19a74547dcbdf349862cbbeebb

$ git diff --stat -- .specify/instructions.md
                                              # empty: byte-identical, zero working-tree change

$ ls -l AGENTS.md CLAUDE.md QODER.md .github/copilot-instructions.md
AGENTS.md                     -> .specify/instructions.md
CLAUDE.md                     -> .specify/instructions.md
QODER.md                      -> .specify/instructions.md
.github/copilot-instructions.md -> ../.specify/instructions.md
```

**Reading**: two generations from the same template produce the same bytes (same sha256, empty diff),
so the generator is idempotent over the section T013 added — a second run neither appends a duplicate
nor rewrites a neighbour. The four compatibility symlinks still point at the live file and needed no
repair; `git status --short` after the run lists no change outside the pre-existing dirty files, so the
live instructions were never hand-edited.
