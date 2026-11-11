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



## T007/T035 红先 — manifest-aware 分片发现（`archive-manifest.json`，C-112）

- **采集点**: 2026-11-11 · worktree `100-seal-slice-archive` · 引擎未改动（`scripts/python/seal-utils.py` sha256 `f6355d5b0eb9b27c36d1343b098f98a2dbe974278ab52376c572966a4b008178`）· 夹具 `tests/fixtures/seal-archive/archived-pair/` 与两份测试文件已就位
- **命令（verbatim）**: `bash scripts/bash/run-tests.sh tests/contract/test_seal_merge_plan.py tests/integration/test_seal_074_round.py -q`
- **退出码**: `1`
- **完整 stdout/stderr（verbatim）**:

```text
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_seal_merge_plan.py tests/integration/test_seal_074_round.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

.................F.FFFF....F..FFF                                        [100%]
=================================== FAILURES ===================================
_______ test_c112_manifest_disagreeing_with_the_merge_manifest_is_drift ________
[gw22] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw22/test_c112_manifest_disagreeing0')

    def test_c112_manifest_disagreeing_with_the_merge_manifest_is_drift(tmp_path):
        repo = _copy_archive_fixture(tmp_path)
        merge_path = repo / ".specify" / "specs" / ARCHIVE_PARENT / "merge-manifest.json"
        document = json.loads(merge_path.read_text(encoding="utf-8"))
        document["slices"][1]["order"] = 3
        merge_path.write_text(
            json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        proc, payload = _run_plan(repo, ARCHIVE_PARENT)
>       assert proc.returncode == 2
E       assert 0 == 2
E        +  where 0 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor.../test_c112_manifest_disagreeing0/archived-pair/.specify/specs/100-fixture-parent",\n  "verdict": "ok"\n}\n', stderr='').returncode

tests/contract/test_seal_merge_plan.py:563: AssertionError
____________ test_c112_manifest_disagreeing_with_the_tree_is_drift _____________
[gw23] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw23/test_c112_manifest_disagreeing0')

    def test_c112_manifest_disagreeing_with_the_tree_is_drift(tmp_path):
        repo = _copy_archive_fixture(tmp_path)
        parent = repo / ".specify" / "specs" / ARCHIVE_PARENT
        shutil.move(str(parent / "slices" / ARCHIVE_BETA),
                    str(repo / ".specify" / "specs" / ARCHIVE_BETA))
        proc, payload = _run_plan(repo, ARCHIVE_PARENT)
>       assert proc.returncode == 2
E       assert 0 == 2
E        +  where 0 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor.../test_c112_manifest_disagreeing0/archived-pair/.specify/specs/100-fixture-parent",\n  "verdict": "ok"\n}\n', stderr='').returncode

tests/contract/test_seal_merge_plan.py:576: AssertionError
____________ test_c112_archived_pair_keeps_the_slice_set_and_order _____________
[gw18] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw18/test_c112_archived_pair_keeps_0')

    def test_c112_archived_pair_keeps_the_slice_set_and_order(tmp_path):
        repo = _copy_archive_fixture(tmp_path)
        proc, payload = _run_plan(repo, ARCHIVE_PARENT)
        assert proc.returncode == 0, (
            "C-112: an archived pair is the same slice set, not an empty one; "
            "exit=%d conditions=%r" % (proc.returncode, payload.get("conditions"))
        )
        plan = payload["plan"]
>       assert [entry["slug"] for entry in plan["slices"]] == [ARCHIVE_ALPHA, ARCHIVE_BETA]
E       AssertionError: assert [] == ['100a-fixtur...fixture-beta']
E         
E         Right contains 2 more items, first extra item: '100a-fixture-alpha'
E         Use -v to get more diff

tests/contract/test_seal_merge_plan.py:508: AssertionError
_________ test_c112_archived_slices_are_read_from_their_archived_paths _________
[gw19] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw19/test_c112_archived_slices_are_0')

    def test_c112_archived_slices_are_read_from_their_archived_paths(tmp_path):
        repo = _copy_archive_fixture(tmp_path)
        plan = _plan(repo, ARCHIVE_PARENT)
        for entry in plan["slices"]:
            assert entry["carrier_tasks"] == (
                ".specify/specs/%s/slices/%s/tasks.md" % (ARCHIVE_PARENT, entry["slug"])
            ), "C-112: the archived slice record is read at its `to` path"
>       mapped = _entry(_entries(plan, "FR"), ARCHIVE_ALPHA, "FR-001")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/contract/test_seal_merge_plan.py:527: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

entries = [], slice_slug = '100a-fixture-alpha', slice_id = 'FR-001'

    def _entry(entries: list, slice_slug: str, slice_id: str) -> dict:
        found = [e for e in entries
                 if e["slice"] == slice_slug and e["slice_id"] == slice_id]
>       assert len(found) == 1, (
            f"expected exactly one id_map entry for {slice_slug} {slice_id}; "
            f"got {found!r}"
        )
E       AssertionError: expected exactly one id_map entry for 100a-fixture-alpha FR-001; got []
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_seal_merge_plan.py:116: AssertionError
___________ test_c112_unparsable_archive_manifest_is_an_input_error ____________
[gw21] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw21/test_c112_unparsable_archive_m0')

    def test_c112_unparsable_archive_manifest_is_an_input_error(tmp_path):
        repo = _copy_archive_fixture(tmp_path)
        manifest = repo / ".specify" / "specs" / ARCHIVE_PARENT / "archive-manifest.json"
        manifest.write_text("{ not json\n", encoding="utf-8")
        proc, payload = _run_plan(repo, ARCHIVE_PARENT)
>       assert proc.returncode == 2
E       assert 0 == 2
E        +  where 0 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor.../test_c112_unparsable_archive_m0/archived-pair/.specify/specs/100-fixture-parent",\n  "verdict": "ok"\n}\n', stderr='').returncode

tests/contract/test_seal_merge_plan.py:547: AssertionError
_________ test_live_plan_identifies_both_slices_from_the_split_record __________
[gw24] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_live_plan_identifies_both_slices_from_the_split_record():
        proc, payload = _run_plan()
        plan = payload["plan"]
        assert proc.returncode == 0, (
            "the settled round must leave a conflict-free plan; exit=%d payload=%r"
            % (proc.returncode, payload.get("conditions"))
        )
        slices = plan["slices"]
        assert [item["slug"] for item in slices] == [SLICE_A, SLICE_B], (
            "C-012: the split record's declared order (074a → 074b) decides the order"
        )
        assert [item["order"] for item in slices] == [1, 2]
>       assert {item["order_basis"] for item in slices} == {"split-record"}, (
            "C-012: the order MUST be taken from `.specify/state/074-*.md` § 拆分记录"
        )
E       AssertionError: C-012: the order MUST be taken from `.specify/state/074-*.md` § 拆分记录
E       assert {'letter-order'} == {'split-record'}
E         
E         Extra items in the left set:
E         'letter-order'
E         Extra items in the right set:
E         'split-record'
E         Use -v to get more diff

tests/integration/test_seal_074_round.py:99: AssertionError
________ test_c112_merge_plan_after_archive_reports_the_same_slice_set _________
[gw29] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw29/test_c112_merge_plan_after_arc0')

    def test_c112_merge_plan_after_archive_reports_the_same_slice_set(tmp_path):
        repo = _replay_tree(tmp_path)
        before_proc, before = _run_action(repo, "merge-plan")
        assert before_proc.returncode == 0, (
            "the replay's pre-archive plan must be conflict-free: %r"
            % before.get("conditions"))
        before_plan = before["plan"]
        assert [entry["slug"] for entry in before_plan["slices"]] == [SLICE_A, SLICE_B]
    
        _archive_replay(repo, before_plan)
    
        after_proc, after = _run_action(repo, "merge-plan")
        assert after_proc.returncode == 0, (
            "C-112: an archived tree is not an input error: %r"
            % after.get("conditions"))
        after_plan = after["plan"]
>       assert _slice_identity(after_plan) == _slice_identity(before_plan), (
            "C-112: the archived slice set and its order are the same slice set"
        )
E       AssertionError: C-112: the archived slice set and its order are the same slice set
E       assert [] == [('074a-autho...etter-order')]
E         
E         Right contains 2 more items, first extra item: ('074a-authorized-routing', 1, 'letter-order')
E         Use -v to get more diff

tests/integration/test_seal_074_round.py:385: AssertionError
____ test_c112_merge_apply_after_archive_is_an_idempotent_zero_write_rerun _____
[gw30] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw30/test_c112_merge_apply_after_ar0')

    def test_c112_merge_apply_after_archive_is_an_idempotent_zero_write_rerun(tmp_path):
        repo = _replay_tree(tmp_path)
        plan = _run_action(repo, "merge-plan")[1]["plan"]
        before_proc, before = _run_action(repo, "merge-apply")
        assert before_proc.returncode == 0
        assert before["apply"]["idempotent"] is True
    
        _archive_replay(repo, plan)
    
        after_proc, after = _run_action(repo, "merge-apply")
        assert after_proc.returncode == 0, (
            "C-112: merge-apply after the archive is an idempotent success: %r"
            % after.get("conditions"))
        assert after["apply"]["idempotent"] is True
        assert after["apply"]["writes"] == [], (
            "C-112: the archived rerun performs zero writes"
        )
>       assert after["apply"]["slices"] == [SLICE_A, SLICE_B]
E       AssertionError: assert [] == ['074a-author...d-governance']
E         
E         Right contains 2 more items, first extra item: '074a-authorized-routing'
E         Use -v to get more diff

tests/integration/test_seal_074_round.py:412: AssertionError
_________________ test_c112_seal_judgment_survives_the_archive _________________
[gw31] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-9497/popen-gw31/test_c112_seal_judgment_surviv0')

    def test_c112_seal_judgment_survives_the_archive(tmp_path):
        repo = _replay_tree(tmp_path)
        plan = _run_action(repo, "merge-plan")[1]["plan"]
        before_proc, before = _run_action(repo, "seal")
        assert [condition for condition in before["conditions"]
                if condition["code"] == "p0-unresolved"], (
            "the 074 round's P0 reading is the face this test compares")
    
        _archive_replay(repo, plan)
    
        after_proc, after = _run_action(repo, "seal")
        assert after_proc.returncode == before_proc.returncode, (
            "C-112: the seal verdict (P0 / blocking / closure) is unchanged by the archive"
        )
        assert after["verdict"] == before["verdict"]
>       assert _seal_facets(after) == _seal_facets(before), (
            "C-112: seal keeps reading the original slice records, now at `to` paths; "
            "the condition list MUST stay byte-identical"
        )
E       AssertionError: C-112: seal keeps reading the original slice records, now at `to` paths; the condition list MUST stay byte-identical
E       assert [('closure-in...y slice set')] == [('p0-unresol...y Ownership')]
E         
E         At index 0 diff: ('closure-input-defect', 'the closure engine exited 2: closure-acceptance-check: input error: /tmp/pytest-of-agent/pytest-9497/popen-gw31/test_c112_seal_judgment_surviv0/replay/.specify/specs/074-goal-team-sdd-unification/requirements.md carries no § Runtime Stack & Dependency Ownership') != ('p0-unresolved', '074b-nested-governance:F1 (line 115 of .specify/specs/074b-nested-governance/review.md) has neither a resolvable `- **Fix**:` pointer nor a user waiver on both carriers')
E         Use -v to get more diff

tests/integration/test_seal_074_round.py:430: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_seal_merge_plan.py::test_c112_manifest_disagreeing_with_the_merge_manifest_is_drift
FAILED tests/contract/test_seal_merge_plan.py::test_c112_manifest_disagreeing_with_the_tree_is_drift
FAILED tests/contract/test_seal_merge_plan.py::test_c112_archived_pair_keeps_the_slice_set_and_order
FAILED tests/contract/test_seal_merge_plan.py::test_c112_archived_slices_are_read_from_their_archived_paths
FAILED tests/contract/test_seal_merge_plan.py::test_c112_unparsable_archive_manifest_is_an_input_error
FAILED tests/integration/test_seal_074_round.py::test_live_plan_identifies_both_slices_from_the_split_record
FAILED tests/integration/test_seal_074_round.py::test_c112_merge_plan_after_archive_reports_the_same_slice_set
FAILED tests/integration/test_seal_074_round.py::test_c112_merge_apply_after_archive_is_an_idempotent_zero_write_rerun
FAILED tests/integration/test_seal_074_round.py::test_c112_seal_judgment_survives_the_archive
9 failed, 24 passed in 6.52s
```

---

## T010/T012/T023/T024/T027/T029/T030 红先 — archive-plan 前置、分类与清单（P3，15 行包）

- **采集点**: 2026-11-11 · worktree `100-seal-slice-archive` · 引擎已回退到 P2 提交 `efe5f4d3f` 的版本（sha256 `e7d45cc52e68b031e0f8d0ff038a55b839d9f8de90983e68c40773eb64c69b76`）· 六套夹具（T011/T022）与最终测试文件已落盘
- **命令（verbatim）**: `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/unit/test_seal_archive_classify.py tests/unit/test_seal_archive_manifest_math.py tests/unit/test_seal_archive_schema.py tests/contract/test_seal_merge_apply.py -q`
- **退出码**: `1` — `63 failed, 18 passed`（63 条红 = 新增契约/单元断言 + C-211 扩写；18 条绿 = merge-apply 既有回归与不依赖新符号的用例）
- **完整 stdout/stderr（verbatim）**: 全量 96 KB 读数存 `test-evidence/p3-red-first.txt`（sha256 `a13b14233c16098c77e933104385ba3dc283e4be7903cd639f0dc455968c6bec`），此处不复写；头部与结尾 verbatim：

```text
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/unit/test_seal_archive_classify.py tests/unit/test_seal_archive_manifest_math.py tests/unit/test_seal_archive_schema.py tests/contract/test_seal_merge_apply.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF..F...........FF.FFFFFFFF.FFFFFFFFF. [ 88%]
FFFFFFF..                                                                [100%]
=================================== FAILURES ===================================
...
FAILED tests/contract/test_seal_archive_manifest.py::test_c207_digest_is_the_c034_algorithm
FAILED tests/contract/test_seal_archive_manifest.py::test_sc007_delete_a_ledger_row_turns_the_arithmetic_red
FAILED tests/contract/test_seal_archive_manifest.py::test_c209_unknown_or_missing_fields_refuse_at_every_level
FAILED tests/contract/test_seal_archive_manifest.py::test_c212_schema_version_is_one_and_higher_versions_refuse
FAILED tests/contract/test_seal_archive_manifest.py::test_same_input_twice_is_byte_identical
63 failed, 18 passed, 576 warnings in 6.41s
```

- **红因分类**: `archive-plan` 仍指向 `_pending`（无 `outcome`/`archive` 负载）；分类/摘要/校验/修订符号不存在（`AttributeError`）；C-211 修订函数未实现。夹具与测试文件本身无导入错误——红来自行为缺失，不是拼写。
- **测试文件哈希（红时定稿字节）**: plan `304df745…`；manifest `f48cfc5d…`；merge_apply `394ff922…`；classify `725f5bc7…`；manifest_math `cdc7911b…`；schema `1adc8f07…`。
- **转绿读数**: `test-evidence/p3-green.txt`（`81 passed`，exit 0）与 `test-evidence/p3-regression.txt`（`119 passed / 3 failed`，3 条均为 P2 § 4 已记录的既有基线行）。

---

## T013/T014 红先 — archive-apply 两阶段、纯移动与幂等（P4，6 行包）

- **采集点**: 2026-11-11 · worktree `100-seal-slice-archive` · 引擎停在 P3 提交 `4b62d1677` 的版本（sha256 `f3cce2c42fe6a86814fc0c06c766896d88f23c63695e8943a86cc76df6238e48`）· `HANDLERS["archive-apply"]` 仍指向 `_pending`
- **命令（verbatim）**: `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py -q`
- **退出码**: `1` — `14 failed, 3 passed`（14 红 = apply 行为缺失；3 绿 = 已实现的 plan 确定性用例）
- **完整 stdout/stderr（verbatim）**: 全量读数存 `test-evidence/p4-red-first.txt`（sha256 `45f40e97c3a9053c07f71e66cb9e9f47e306758c2b0ca9339e7fa934fe6b241a`；以最终测试字节对 P3 引擎 `f3cce2c4…` 重采，随后恢复实现版引擎）；头部与结尾 verbatim：

```text
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

FFF.FFFFFFF.FF.FF                                                        [100%]
...
14 failed, 3 passed
```

- **红因分类**: `archive-apply` 载荷为 `not-implemented`（`_pending`）；`_archive_move` / `_archive_write_text` 注入缝尚不存在（`AttributeError`）；`already-archived`、写批次与恢复路径均无实现。夹具与测试文件无导入错误——红来自行为缺失，不是拼写。
- **测试文件哈希（红时定稿字节）**: apply `a6ab246fd7eb…`；idempotency `bd5dacc569da…`。
