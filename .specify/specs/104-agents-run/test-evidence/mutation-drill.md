# Mutation Drill — 4/4 (SC-006, C-35)

Feature: 104-agents-run · Date: 2026-11-24 · Repo: `/storage/project/cloud-native-ai/spec-kit`
Branch: `104-agents-run` · Tree state at drill: commit `8c39cdec0` (product slice), no unstaged
product changes.

Method (owner: `.specify/skills/internal/implement-feature/SKILL.md` § Step 6, mutation-drill
restore): each mutation is applied against the committed subject, the named module is run through
the only test entry `bash scripts/bash/run-tests.sh`, the red set is recorded, the subject is
restored by exact reverse substitution, the restored literal is asserted at count 1, the case is
re-run to green, and the file's `git diff` is confirmed empty — a `cp` exit code is never read as
proof of restore.

## M1 — delete `argument-hint` → C-01 red

Mutation: delete the single frontmatter line
`argument-hint: "[create|refine|run] [agent-name] [task]"` from `templates/commands/agents.md`
(precondition: count = 1; after = 0).

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q --names-out /tmp/m1-red.txt; rc=$?
rc=1
FAILED tests/contract/test_agents_run_command_contract.py::test_c01_template_declares_the_argument_grammar
FAILED tests/contract/test_agents_run_command_contract.py::test_c06_the_three_syntax_faces_agree_verbatim
2 failed, 8 passed in 6.61s
```

Red as designed: C-01 is the pinned check (C-06 also red — the template face carries [[STR-001]]).
Restore reading: restored literal count = 1; `git diff --quiet -- templates/commands/agents.md` →
empty; re-run `10 passed` (rc 0).

Disclosed in-passing repair: the first restore used bare `cp` and the interactive alias answered
"overwrite?" — the file stayed mutated and the restore assertion fired. Reverted with the
alias-proof `\cp -f`, then the literal assertion and the empty-diff check both passed before the
re-run. This is the exact trap the skill's shell-hygiene rule names; no drill reading was taken
from the aliased copy.

## M2 — delete the template run intent row → C-02 red

Mutation: delete the Delegation table row beginning `| **run** an agent, or empty arguments |`
from `templates/commands/agents.md` (precondition: exactly one such row; after: two data rows).

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q --names-out /tmp/m2-red.txt; rc=$?
rc=1
FAILED tests/contract/test_agents_run_command_contract.py::test_c02_three_skill_rows_and_run_row_carries_the_explicit_form
FAILED tests/contract/test_agents_run_command_contract.py::test_c08_routing_sample_set_proxies
FAILED tests/contract/test_agents_run_command_contract.py::test_c09_per_tool_copies_are_generated_and_carry_the_run_form
3 failed, 7 passed in 6.56s
```

Red as designed: C-02 is the pinned check; C-08 reads the same table and C-09 sees the copies
diverge from the mutated template. Restore reading: run row count = 1; `git diff` empty; re-run
`10 passed` (rc 0).

## M3 — delete the seven-field downlink pointer → C-12 red

Mutation: delete the five-line paragraph beginning
`**Role-edge downlink (seven fields, by pointer)**` from `skills/internal/run-agent/SKILL.md`
(precondition: paragraph present once, `parent_identity` present once; after: absent).

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_skill_wiring.py -q --names-out /tmp/m3-red.txt; rc=$?
rc=1
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c12_downlink_names_the_seven_role_fields
1 failed, 16 passed in 6.23s
```

Red as designed: C-12 alone. Restore reading: paragraph count = 1; `git diff` empty; re-run
`17 passed` (rc 0). (A secondary probe in the restore script asserted `parent_identity` appears
twice and reported 1 — the probe was wrong, the restored literal assertion of 1 and the empty
diff are the operative readings; no restore defect.)

## M4 — duplicate the command reference body → C-23 red

Mutation: append a second `# /speckit.agents` heading plus a one-line body to
`docs/reference/commands/agents.md` (precondition: zero second headings; after: heading count = 2
— the shape of the retired three-copy concatenation).

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py -q --names-out /tmp/m4-red.txt; rc=$?
rc=1
FAILED tests/contract/test_agents_run_docs_contract.py::test_c23_one_command_reference_body
1 failed, 11 passed in 6.23s
```

Red as designed: C-23 alone. Restore reading: heading count = 1; `git diff` empty; re-run
`12 passed` (rc 0).

## Verdict

4/4 mutations turned exactly their pinned check red and the exact reverse substitution turned each
green again with an empty file diff. SC-006 source: this file. Behavior-class clauses cite this
drill under "evidence route", never as contract-test coverage.
