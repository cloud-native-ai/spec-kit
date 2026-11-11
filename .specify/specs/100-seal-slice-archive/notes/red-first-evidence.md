# Red-First Evidence — Feature 100（implement 阶段）

> 只记录**红先读数**：命令 verbatim、退出码与完整输出。实现转绿后的读数落 `test-evidence/`。
> 本文件是 Foundational（T004）起各红先行共享的追加槽；写入本文件的行按其 `[blockedBy:]` 串行追加。

## 记录模板（每行一节）

每节依次含：`T0xx 红先 <测试文件 / 主题>` 标题、**采集点**、**命令（verbatim）**、**退出码**、**完整 stdout/stderr（verbatim）**（四要素均为真实读数，不摘写）。

---

## T004 红先 — 六动作集 pin（`tests/contract/test_seal_engine_contract.py`）

- **采集点**: 2026-11-11 · worktree `100-seal-slice-archive` · 引擎未改动（`scripts/python/seal-utils.py` sha256 `dcc816e162c7e3a1963ef6870163402f5398bbb20b6fa31884e95feccdd73f35`）· 测试文件已扩写到六值
- **命令（verbatim）**: `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q`
- **退出码**: `1`
- **完整 stdout/stderr（verbatim）**:

```text
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_seal_engine_contract.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

....FFF..............FF....FFFF.                                         [100%]
=================================== FAILURES ===================================
_______________ test_c001_dispatch_table_covers_exactly_the_six ________________
[gw1] linux -- Python 3.11.11 /usr/local/bin/python3

eng = <module 'seal_utils_under_test' from '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py'>

    def test_c001_dispatch_table_covers_exactly_the_six(eng):
>       assert set(eng.HANDLERS) == set(ACTIONS), (
            "C-001/C-101: every declared action has exactly one dispatch entry and no other"
        )
E       AssertionError: C-001/C-101: every declared action has exactly one dispatch entry and no other
E       assert {'archive-gat...plan', 'seal'} == {'archive-app...plan', 'seal'}
E         
E         Extra items in the right set:
E         'archive-apply'
E         'archive-plan'
E         Use -v to get more diff

tests/contract/test_seal_engine_contract.py:216: AssertionError
________ test_c005_read_only_and_write_actions_partition_the_closed_set ________
[gw14] linux -- Python 3.11.11 /usr/local/bin/python3

eng = <module 'seal_utils_under_test' from '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py'>

    def test_c005_read_only_and_write_actions_partition_the_closed_set(eng):
>       assert tuple(eng.READ_ONLY_ACTIONS) == READ_ONLY_ACTIONS
E       AssertionError: assert ('merge-plan', 'archive-gate') == ('merge-plan'...archive-plan')
E         
E         Right contains one more item: 'archive-plan'
E         Use -v to get more diff

tests/contract/test_seal_engine_contract.py:356: AssertionError
___________________ test_c001_action_set_is_exactly_the_six ____________________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

eng = <module 'seal_utils_under_test' from '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py'>

    def test_c001_action_set_is_exactly_the_six(eng):
>       assert tuple(eng.ACTIONS) == ACTIONS, (
            "C-001/C-101: the engine's action set MUST be exactly the six closed actions"
        )
E       AssertionError: C-001/C-101: the engine's action set MUST be exactly the six closed actions
E       assert ('merge-plan'...archive-gate') == ('merge-plan'...rchive-apply')
E         
E         Right contains 2 more items, first extra item: 'archive-plan'
E         Use -v to get more diff

tests/contract/test_seal_engine_contract.py:206: AssertionError
_____________________ test_c115_six_action_cli_consistency _____________________
[gw31] linux -- Python 3.11.11 /usr/local/bin/python3

eng = <module 'seal_utils_under_test' from '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py'>
engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw31/test_c115_six_action_cli_consi0')

    def test_c115_six_action_cli_consistency(eng, engine, tmp_path):
        spec_dir = _make_spec(tmp_path)
        before = _snapshot(tmp_path)
    
        help_proc = _run(engine, ["--help"], tmp_path)
        assert help_proc.returncode == 0, (
            f"C-115: --help MUST exit 0; got {help_proc.returncode}"
        )
        for action in ACTIONS:
>           assert action in help_proc.stdout, (
                f"C-115: --help MUST list the six closed actions; {action!r} is missing"
            )
E           AssertionError: C-115: --help MUST list the six closed actions; 'archive-plan' is missing
E           assert 'archive-plan' in 'usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_D...ation writes nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n'
E            +  where 'usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_D...ation writes nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n' = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor... nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n', stderr='').stdout

tests/contract/test_seal_engine_contract.py:617: AssertionError
______ test_c003_help_answers_zero_side_effect_and_carries_the_cli_labels ______
[gw5] linux -- Python 3.11.11 /usr/local/bin/python3

engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw5/test_c003_help_answers_zero_si0')

    def test_c003_help_answers_zero_side_effect_and_carries_the_cli_labels(engine, tmp_path):
        before = _snapshot(tmp_path)
        proc = _run(engine, ["--help"], tmp_path)
        assert proc.returncode == 0, f"C-003: --help MUST exit 0; got {proc.returncode}"
        assert _snapshot(tmp_path) == before, "C-003: --help MUST NOT touch the workspace"
        for label in ("usage", "options", "side-effects:", "exit-codes:"):
            assert label in proc.stdout.lower(), (
                f"C-003: the help body MUST carry the {label!r} label"
            )
        for action in ACTIONS:
>           assert action in proc.stdout, (
                f"C-101: the help body MUST list the {action!r} action label"
            )
E           AssertionError: C-101: the help body MUST list the 'archive-plan' action label
E           assert 'archive-plan' in 'usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_D...ation writes nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n'
E            +  where 'usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_D...ation writes nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n' = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor... nothing\nexit-codes: 0 success or idempotent; 1 a precondition refused; 2 an input or environment error\n', stderr='').stdout

tests/contract/test_seal_engine_contract.py:287: AssertionError
________________ test_c006_read_only_reports_go_to_stdout_only _________________
[gw16] linux -- Python 3.11.11 /usr/local/bin/python3

engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw16/test_c006_read_only_reports_go0')

    def test_c006_read_only_reports_go_to_stdout_only(engine, tmp_path):
        spec_dir = _make_spec(tmp_path)
        for action in READ_ONLY_ACTIONS:
            proc = _run(engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], tmp_path)
>           assert proc.stderr == "", (
                f"C-006: {action} MUST report on stdout only; stderr={proc.stderr[-500:]!r}"
            )
E           AssertionError: C-006: archive-plan MUST report on stdout only; stderr="usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_DIR [--repo REPO]\n                     [--feature-detail FEATURE_DETAIL]\n                     [--feature-registry FEATURE_REGISTRY] [--json]\n                     [--version]\nseal-utils.py: error: argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n"
E           assert "usage: seal-...hive-gate')\n" == ''
E             
E             + usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}
E             +                      --spec-dir SPEC_DIR [--repo REPO]
E             +                      [--feature-detail FEATURE_DETAIL]
E             +                      [--feature-registry FEATURE_REGISTRY] [--json]
E             +                      [--version]
E             + seal-utils.py: error: argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')

tests/contract/test_seal_engine_contract.py:399: AssertionError
_________________ test_c009_mirror_copy_refuses_write_actions __________________
[gw23] linux -- Python 3.11.11 /usr/local/bin/python3

engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw23/test_c009_mirror_copy_refuses_0')

    def test_c009_mirror_copy_refuses_write_actions(engine, tmp_path):
        repo = tmp_path / "repo"
        mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
        spec_dir = _make_spec(repo)
        for action in WRITE_ACTIONS:
            proc = _run(mirror_engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], repo)
            assert proc.returncode == 2, (
                f"C-009: a mirror-copy write action exits 2; got {proc.returncode} for {action}"
            )
>           payload = _payload(proc)
                      ^^^^^^^^^^^^^^

tests/contract/test_seal_engine_contract.py:505: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

proc = CompletedProcess(args=['/usr/local/bin/python3', '/tmp/pytest-of-agent/pytest-9487/popen-gw23/test_c009_mirror_copy_re...rgument --action: invalid choice: 'archive-apply' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n")

    def _payload(proc) -> dict:
>       assert proc.stdout.strip(), (
            f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
        )
E       AssertionError: expected a stdout payload; exit=2 stderr="usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_DIR [--repo REPO]\n                     [--feature-detail FEATURE_DETAIL]\n                     [--feature-registry FEATURE_REGISTRY] [--json]\n                     [--version]\nseal-utils.py: error: argument --action: invalid choice: 'archive-apply' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n"
E       assert ''
E        +  where '' = <built-in method strip of str object at 0x7fee29da7a60>()
E        +    where <built-in method strip of str object at 0x7fee29da7a60> = ''.strip
E        +      where '' = CompletedProcess(args=['/usr/local/bin/python3', '/tmp/pytest-of-agent/pytest-9487/popen-gw23/test_c009_mirror_copy_re...rgument --action: invalid choice: 'archive-apply' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n").stdout

tests/contract/test_seal_engine_contract.py:139: AssertionError
__________ test_c009_read_actions_are_not_refused_by_the_mirror_guard __________
[gw24] linux -- Python 3.11.11 /usr/local/bin/python3

engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw24/test_c009_read_actions_are_not0')

    def test_c009_read_actions_are_not_refused_by_the_mirror_guard(engine, tmp_path):
        repo = tmp_path / "repo"
        mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
        spec_dir = _make_spec(repo)
        for action in READ_ONLY_ACTIONS:
            proc = _run(mirror_engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], repo)
>           payload = _payload(proc)
                      ^^^^^^^^^^^^^^

tests/contract/test_seal_engine_contract.py:517: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

proc = CompletedProcess(args=['/usr/local/bin/python3', '/tmp/pytest-of-agent/pytest-9487/popen-gw24/test_c009_read_actions_a...argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n")

    def _payload(proc) -> dict:
>       assert proc.stdout.strip(), (
            f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
        )
E       AssertionError: expected a stdout payload; exit=2 stderr="usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_DIR [--repo REPO]\n                     [--feature-detail FEATURE_DETAIL]\n                     [--feature-registry FEATURE_REGISTRY] [--json]\n                     [--version]\nseal-utils.py: error: argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n"
E       assert ''
E        +  where '' = <built-in method strip of str object at 0x7fe0dc5c0a60>()
E        +    where <built-in method strip of str object at 0x7fe0dc5c0a60> = ''.strip
E        +      where '' = CompletedProcess(args=['/usr/local/bin/python3', '/tmp/pytest-of-agent/pytest-9487/popen-gw24/test_c009_read_actions_a...argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n").stdout

tests/contract/test_seal_engine_contract.py:139: AssertionError
________ test_c010_json_payload_is_canonical_and_matches_the_exit_code _________
[gw28] linux -- Python 3.11.11 /usr/local/bin/python3

engine = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/scripts/python/seal-utils.py')
tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9487/popen-gw28/test_c010_json_payload_is_cano0')

    def test_c010_json_payload_is_canonical_and_matches_the_exit_code(engine, tmp_path):
        spec_dir = _make_spec(tmp_path)
        for action in ACTIONS:
            proc = _run(engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], tmp_path)
>           payload = _payload(proc)
                      ^^^^^^^^^^^^^^

tests/contract/test_seal_engine_contract.py:568: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

proc = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n")

    def _payload(proc) -> dict:
>       assert proc.stdout.strip(), (
            f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
        )
E       AssertionError: expected a stdout payload; exit=2 stderr="usage: seal-utils.py [-h] --action {merge-plan,merge-apply,seal,archive-gate}\n                     --spec-dir SPEC_DIR [--repo REPO]\n                     [--feature-detail FEATURE_DETAIL]\n                     [--feature-registry FEATURE_REGISTRY] [--json]\n                     [--version]\nseal-utils.py: error: argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n"
E       assert ''
E        +  where '' = <built-in method strip of str object at 0x7f31a1873a60>()
E        +    where <built-in method strip of str object at 0x7f31a1873a60> = ''.strip
E        +      where '' = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...argument --action: invalid choice: 'archive-plan' (choose from 'merge-plan', 'merge-apply', 'seal', 'archive-gate')\n").stdout

tests/contract/test_seal_engine_contract.py:139: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_seal_engine_contract.py::test_c001_dispatch_table_covers_exactly_the_six
FAILED tests/contract/test_seal_engine_contract.py::test_c005_read_only_and_write_actions_partition_the_closed_set
FAILED tests/contract/test_seal_engine_contract.py::test_c001_action_set_is_exactly_the_six
FAILED tests/contract/test_seal_engine_contract.py::test_c115_six_action_cli_consistency
FAILED tests/contract/test_seal_engine_contract.py::test_c003_help_answers_zero_side_effect_and_carries_the_cli_labels
FAILED tests/contract/test_seal_engine_contract.py::test_c006_read_only_reports_go_to_stdout_only
FAILED tests/contract/test_seal_engine_contract.py::test_c009_mirror_copy_refuses_write_actions
FAILED tests/contract/test_seal_engine_contract.py::test_c009_read_actions_are_not_refused_by_the_mirror_guard
FAILED tests/contract/test_seal_engine_contract.py::test_c010_json_payload_is_canonical_and_matches_the_exit_code
9 failed, 23 passed in 6.73s
```


