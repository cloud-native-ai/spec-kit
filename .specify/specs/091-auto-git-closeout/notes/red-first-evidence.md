# Red-first evidence — feature 091

Each entry records: the guard row, the command run, the **real** output, and the exit status —
captured before the implementation row that turns it green. An entry is appended, never
rewritten; the landed (green) readings live in `test-evidence/`.

Format per entry:

```
## T0NN — <what the guard asserts>
Command: <verbatim>
Exit: <status>
Output: <real output, verbatim or a faithful excerpt with the failing assertion quoted>
```

---
## T016 — the command-surface guard reds before the reference exists
```
Command: /usr/bin/python3 -m pytest tests/contract/test_git_closeout_contract.py -q --tb=line -k "command_reference or pre_existing_examples or refusal_outcomes or readonly_role or unusable_block or ask_path or strategy_value_transition"
Exit: 1
FFFFFFF                                                                  [100%]
=================================== FAILURES ===================================
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
/usr/lib64/python3.11/pathlib.py:1044: FileNotFoundError: [Errno 2] No such file or directory: '/storage/project/cloud-native-ai/spec-kit/skills/external/git-utils/references/closeout-commands.md'
=========================== short test summary info ============================
FAILED tests/contract/test_git_closeout_contract.py::test_command_reference_carries_no_hardcoded_remote_literal
FAILED tests/contract/test_git_closeout_contract.py::test_pre_existing_examples_elsewhere_are_reported_not_rewritten
FAILED tests/contract/test_git_closeout_contract.py::test_three_refusal_outcomes_are_distinct_named_outcomes
FAILED tests/contract/test_git_closeout_contract.py::test_readonly_role_excludes_a_declared_and_named_remote
FAILED tests/contract/test_git_closeout_contract.py::test_unusable_block_outcomes_are_distinct_with_distinct_behaviour
FAILED tests/contract/test_git_closeout_contract.py::test_ask_path_presents_and_never_pushes
FAILED tests/contract/test_git_closeout_contract.py::test_strategy_value_transition_is_per_value_and_behavioural
7 failed in 0.06s
```

## T012 — the declaration guard reds on the pre-change block (both surfaces)
```
Command: git stash push -- skills/external/git-utils/assets/git-workflow-block.md .specify/workflow/git.md
         /usr/bin/python3 -m pytest tests/contract/test_git_closeout_contract.py -q --tb=line \
             -k "closed_value_set or second_branch_table or gained_only"
Exit: 1
FF...                                                                    [100%]
=================================== FAILURES ===================================
.../test_git_closeout_contract.py:146: AssertionError: git-workflow-block.md: the `Closeout` declaration row is missing
.../test_git_closeout_contract.py:146: AssertionError: git.md: the `Closeout` declaration row is missing
=========================== short test summary info ============================
FAILED tests/contract/test_git_closeout_contract.py::test_the_two_declaration_rows_exist_with_the_closed_value_set[git-workflow-block.md]
FAILED tests/contract/test_git_closeout_contract.py::test_the_two_declaration_rows_exist_with_the_closed_value_set[git.md]
2 failed, 3 passed, 15 deselected in 0.05s
```
Two of the three declaration guards red on the pre-change tree — the row is absent on both
surfaces, which is the failure T011 exists to catch. The third (`gained_only`) passes on the
pre-change tree **by construction**: it measures a set *difference*, and before the feature
there is nothing to differ. That is recorded here rather than repaired, because the guard's
discriminating power is a **mutation** (deleting or adding a row on the current tree), and
that mutation is captured below rather than asserted by the pre-change reading.

## T012b — mutation: the same guard reds when the declaration row is swapped for another
```
Command: cp .specify/workflow/git.md /tmp/git.md.keep
         sed -i 's/^- \*\*Closeout\*\*: `ask`/- **Closeout strategy**: `ask`/' .specify/workflow/git.md
         /usr/bin/python3 -m pytest tests/contract/test_git_closeout_contract.py -q --tb=line \
             -k "closed_value_set or gained_only"
         cp /tmp/git.md.keep .specify/workflow/git.md
Exit: 1
.FF                                                                      [100%]
=================================== FAILURES ===================================
.../test_git_closeout_contract.py:146: AssertionError: git.md: the `Closeout` declaration row is missing
.../test_git_closeout_contract.py:240: AssertionError: git.md: the only rows this feature adds are the two declaration rows; found ['closeout remotes', 'closeout strategy']
=========================== short test summary info ============================
FAILED tests/contract/test_git_closeout_contract.py::test_the_two_declaration_rows_exist_with_the_closed_value_set[git.md]
FAILED tests/contract/test_git_closeout_contract.py::test_the_block_gained_only_the_two_declaration_rows
2 failed, 1 passed, 17 deselected in 0.05s
(restored: git.md back to the declared row; `grep -c "^- \*\*Closeout\*\*: \`ask\`"` -> 1)
```
The mutation proves the set-difference guard is not vacuous: renaming the row makes both the
presence guard and the "only two rows were added" guard go red, and the file is restored.
