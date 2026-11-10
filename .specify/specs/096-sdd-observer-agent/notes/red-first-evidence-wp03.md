# Red-first evidence — wp03-driver-lifecycle

One entry per red-first run: command · real output · exit status. Appended by the rows of
`wp03-driver-lifecycle` (T024); never rewritten.

<!-- entries appended below -->

## T024 — lifecycle module before the driver text lands (2026-11-10)

Purpose: the non-blocking and terminal-close assertions MUST fail before the driver text
lands. Both are red below (owner H2 absent); the four already-green cases are the two
failure fixtures and the two baseline guards, whose subjects already exist.

Command: bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_lifecycle.py -q
Exit status: 1 (12 failed, 4 passed)

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_sdd_observer_lifecycle.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFFFF....                                                         [100%]
=================================== FAILURES ===================================
_____________ test_non_blocking_predicate_holds_on_the_driver_text _____________
[gw8] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_blocking_predicate_holds_on_the_driver_text():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:243: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
____________ test_dispatch_brief_reference_carries_its_obligations _____________
[gw11] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_dispatch_brief_reference_carries_its_obligations():
>       assert REFERENCE.is_file(), "missing reference: %s" % REFERENCE
E       AssertionError: missing reference: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/skills/external/sdd-loop-driver/references/observer-lifecycle.md
E       assert False
E        +  where False = is_file()
E        +    where is_file = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/skills/external/sdd-loop-driver/references/observer-lifecycle.md').is_file

tests/contract/test_sdd_observer_lifecycle.py:281: AssertionError
________________ test_stage_prompts_pointer_is_a_single_pointer ________________
[gw12] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_stage_prompts_pointer_is_a_single_pointer():
        section = state_spine_section()
        pointer_lines = [line for line in section.splitlines() if "§ SDD Observer" in line]
>       assert len(pointer_lines) == 1, (
            "§ 状态脊 must carry exactly one pointer line, got %d" % len(pointer_lines)
        )
E       AssertionError: § 状态脊 must carry exactly one pointer line, got 0
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_sdd_observer_lifecycle.py:302: AssertionError
_____________________ test_entry_switch_and_disabled_state _____________________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_entry_switch_and_disabled_state():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:118: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
______________________ test_bounded_execution_and_restart ______________________
[gw6] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_bounded_execution_and_restart():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:211: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
______________ test_record_section_shape_is_owned_by_the_section _______________
[gw2] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_record_section_shape_is_owned_by_the_section():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:149: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
_____________________________ test_terminal_close ______________________________
[gw7] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_terminal_close():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:227: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
_______________ test_startup_point_is_driver_owned_and_decidable _______________
[gw1] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_startup_point_is_driver_owned_and_decidable():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:134: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
___________________ test_execution_carrier_is_external_only ____________________
[gw5] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_execution_carrier_is_external_only():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:194: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
___________________ test_instance_identity_and_creation_duty ___________________
[gw4] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_instance_identity_and_creation_duty():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:176: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
_________________________ test_scope_of_the_mechanism __________________________
[gw10] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_scope_of_the_mechanism():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:268: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
__________________ test_doctored_gate_turns_the_predicate_red __________________
[gw9] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_doctored_gate_turns_the_predicate_red():
>       section = observer_section()
                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_sdd_observer_lifecycle.py:256: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def observer_section() -> str:
        text = SKILL_MD.read_text(encoding="utf-8")
        start = text.find(SECTION_TITLE)
>       assert start != -1, "SKILL.md lacks the owner H2: %s" % SECTION_TITLE
E       AssertionError: SKILL.md lacks the owner H2: ## SDD Observer（观察者：启动、记录节与收束）
E       assert -1 != -1

tests/contract/test_sdd_observer_lifecycle.py:69: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_non_blocking_predicate_holds_on_the_driver_text
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_dispatch_brief_reference_carries_its_obligations
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_stage_prompts_pointer_is_a_single_pointer
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_entry_switch_and_disabled_state
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_bounded_execution_and_restart
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_record_section_shape_is_owned_by_the_section
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_terminal_close - A...
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_startup_point_is_driver_owned_and_decidable
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_execution_carrier_is_external_only
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_instance_identity_and_creation_duty
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_scope_of_the_mechanism
FAILED tests/contract/test_sdd_observer_lifecycle.py::test_doctored_gate_turns_the_predicate_red
12 failed, 4 passed in 6.17s
```
