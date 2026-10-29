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

## S4 — the Stage vocabulary is disambiguated and nothing is renamed (pinned, executed below)

<!-- S4 block appended by T016 -->

## S5 — the instructions pointer is one additive section, regenerated (pinned, executed below)

<!-- S5 block appended by T016 -->
