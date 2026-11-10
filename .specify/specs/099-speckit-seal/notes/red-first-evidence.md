# Red-First Evidence — Feature 099（implement 阶段）

> 只记录**红先读数**：命令 verbatim、退出码与完整输出。实现转绿后的读数落 `test-evidence/`。
> 本文件是 T003 起各红先行共享的追加槽（tasks.md § Notes：写本文件的行不标 `[P]`）。

## 1. T003 红先漂移守卫 `tests/contract/test_sealed_status_domain.py`

**采集点**：T003 落地、T006–T013 任何 carrier/消费面修改之前（工作树仅新增该测试文件）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_sealed_status_domain.py -q
```

**退出码**：1（10 failed）。

**完整 stdout/stderr（verbatim）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_sealed_status_domain.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFF                                                               [100%]
=================================== FAILURES ===================================
_ test_feature_integration_carries_the_seal_protocol_row_and_closes_completed __
[gw5] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_feature_integration_carries_the_seal_protocol_row_and_closes_completed():
        """C-029 surface 5: § Status State Machine's `/speckit.seal` protocol row."""
        table = _integration_table()
        rows = [l for l in table.splitlines() if l.startswith("| `/speckit.seal`")]
>       assert len(rows) == 1, (
            "shared/workflow/feature-integration.md § Status State Machine MUST carry exactly one "
            "`/speckit.seal` protocol row; found %d (C-029 surface 5, FR-001)" % len(rows)
        )
E       AssertionError: shared/workflow/feature-integration.md § Status State Machine MUST carry exactly one `/speckit.seal` protocol row; found 0 (C-029 surface 5, FR-001)
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_sealed_status_domain.py:227: AssertionError
______ test_template_feature_status_token_and_status_bullet_admit_sealed _______
[gw2] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_template_feature_status_token_and_status_bullet_admit_sealed():
        """C-029 surface 2: the `[FEATURE_STATUS]` glossary row and the `**Status**` bullets."""
        text = _read(DETAILS)
        token = next((l for l in text.splitlines()
                      if l.startswith("|") and "[FEATURE_STATUS]" in l), None)
        assert token, (
            "templates/feature-details-template.md lost its `[FEATURE_STATUS]` glossary row — "
            "the surface this guard names is gone"
        )
>       assert SEALED in token, (
            "the `[FEATURE_STATUS]` glossary row does not admit `Sealed`: %r "
            "(C-029 surface 2, FR-001)" % token
        )
E       AssertionError: the `[FEATURE_STATUS]` glossary row does not admit `Sealed`: '| [FEATURE_STATUS] | Draft | Planned | Implemented | Blocked | Ready for Review | Completed |' (C-029 surface 2, FR-001)
E       assert 'Sealed' in '| [FEATURE_STATUS] | Draft | Planned | Implemented | Blocked | Ready for Review | Completed |'

tests/contract/test_sealed_status_domain.py:175: AssertionError
_________________ test_index_template_vocabulary_admits_sealed _________________
[gw3] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_index_template_vocabulary_admits_sealed():
        """C-029 surface 3: templates/feature-index-template.md's closed status vocabulary."""
        lines = [l for l in _read(INDEX_TEMPLATE).splitlines()
                 if re.search(r"(?i)status vocabulary", l)]
        assert lines, (
            "templates/feature-index-template.md carries no status vocabulary line — the surface "
            "this guard names is gone"
        )
        declared = " ".join(lines)
>       assert re.search(r"`%s`" % SEALED, declared), (
            "templates/feature-index-template.md's status vocabulary does not admit `Sealed`: %r "
            "(C-029 surface 3, FR-001)" % declared
        )
E       AssertionError: templates/feature-index-template.md's status vocabulary does not admit `Sealed`: '**Status vocabulary** (closed — these six values are the entire domain a `Status` cell may carry): `Draft` | `Planned` | `Implemented` | `Blocked` | `Ready for Review` | `Completed`.' (C-029 surface 3, FR-001)
E       assert None
E        +  where None = <function search at 0x7fc9351ee3e0>(('`%s`' % 'Sealed'), '**Status vocabulary** (closed — these six values are the entire domain a `Status` cell may carry): `Draft` | `Planned` | `Implemented` | `Blocked` | `Ready for Review` | `Completed`.')
E        +    where <function search at 0x7fc9351ee3e0> = re.search

tests/contract/test_sealed_status_domain.py:198: AssertionError
___________ test_non_disposable_check_engine_judges_the_sealed_cells ___________
[gw8] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_check_engine_judges_the_sealed_cells():
        """C-029 surface 6c: scripts/python/non-disposable-check.py's status × verdict table."""
        source = _read(NON_DISPOSABLE_ENGINE)
        table = re.search(r"def contradiction\(.*?\n(.*?)\n\s*return table\.get", source, re.S)
        assert table, (
            "scripts/python/non-disposable-check.py no longer carries its `contradiction` table — "
            "the surface this guard names is gone"
        )
        body = table.group(1)
>       assert re.search(r'\("Sealed", "accept"\):\s*False', body), (
            "scripts/python/non-disposable-check.py's status × verdict table has no consistent "
            "`Sealed × accept` cell (C-029 surface 6c, FR-001)"
        )
E       AssertionError: scripts/python/non-disposable-check.py's status × verdict table has no consistent `Sealed × accept` cell (C-029 surface 6c, FR-001)
E       assert None
E        +  where None = <function search at 0x7f766530e3e0>('\\("Sealed", "accept"\\):\\s*False', '    """C-802\'s closed table: `True` clash, `False` agree, `None` unknown spelling."""\n    table = {\n        ("Draf...   ("Blocked", "block"): False,\n        ("Completed", "accept"): False,\n        ("Completed", "block"): True,\n    }')
E        +    where <function search at 0x7f766530e3e0> = re.search

tests/contract/test_sealed_status_domain.py:320: AssertionError
_____________ test_non_disposable_owner_domain_line_admits_sealed ______________
[gw6] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_owner_domain_line_admits_sealed():
        """C-029 surface 6a: the Status Readability registry-status domain line."""
        line = next((l for l in _read(NON_DISPOSABLE_OWNER).splitlines()
                     if "注册表状态值域" in l), None)
        assert line, (
            "shared/definitions/non-disposable-definitions.md carries no 注册表状态值域 row — the "
            "surface this guard names is gone"
        )
>       assert SEALED in line, (
            "the Status Readability domain row does not admit `Sealed`: %r "
            "(C-029 surface 6a, FR-001)" % line
        )
E       AssertionError: the Status Readability domain row does not admit `Sealed`: '| 注册表状态值域（`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed` / `Relocated`） | `shared/workflow/feature-integration.md` § Status State Machine；载体声明在 `templates/feature-details-template.md` § Canonical Status State Machine |' (C-029 surface 6a, FR-001)
E       assert 'Sealed' in '| 注册表状态值域（`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed` / `Relocated`） | `shared...ntegration.md` § Status State Machine；载体声明在 `templates/feature-details-template.md` § Canonical Status State Machine |'

tests/contract/test_sealed_status_domain.py:281: AssertionError
______________ test_closure_completion_claim_family_admits_sealed ______________
[gw9] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_closure_completion_claim_family_admits_sealed():
        """C-029 surface 7: CLAIMED_IMPLEMENTED and the AUDIT_FAMILY that follows it."""
        source = _read(CLOSURE_ENGINE)
        claimed = re.search(r"(?m)^CLAIMED_IMPLEMENTED = \(([^)]*)\)", source)
        assert claimed, (
            "scripts/python/closure-acceptance-check.py no longer defines `CLAIMED_IMPLEMENTED` — "
            "the surface this guard names is gone"
        )
        members = [m.strip().strip('"\'') for m in claimed.group(1).split(",") if m.strip()]
>       assert SEALED in members, (
            "`CLAIMED_IMPLEMENTED` does not admit `Sealed`; a sealed row would not be read as a "
            "completion claim (C-029 surface 7, plan § Disclosed Rulings 3): %r" % members
        )
E       AssertionError: `CLAIMED_IMPLEMENTED` does not admit `Sealed`; a sealed row would not be read as a completion claim (C-029 surface 7, plan § Disclosed Rulings 3): ['Implemented', 'Ready for Review']
E       assert 'Sealed' in ['Implemented', 'Ready for Review']

tests/contract/test_sealed_status_domain.py:343: AssertionError
________________ test_manage_features_vocabulary_admits_sealed _________________
[gw4] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_manage_features_vocabulary_admits_sealed():
        """C-029 surface 4: skills/internal/manage-features/SKILL.md's status vocabulary."""
        row = next((l for l in _read(MANAGE_FEATURES).splitlines()
                    if re.match(r"^\s*-\s*Status vocabulary:", l)), None)
        assert row, (
            "skills/internal/manage-features/SKILL.md carries no `Status vocabulary` line — the "
            "surface this guard names is gone"
        )
        members = [v.strip().strip("`") for v in row.split(":", 1)[1].split("|")]
>       assert SEALED in members, (
            "skills/internal/manage-features/SKILL.md's `Status vocabulary` line does not admit "
            "`Sealed`: %r (C-029 surface 4, FR-001)" % members
        )
E       AssertionError: skills/internal/manage-features/SKILL.md's `Status vocabulary` line does not admit `Sealed`: ['Draft', 'Planned', 'Implemented', 'Blocked', 'Ready for Review', 'Completed'] (C-029 surface 4, FR-001)
E       assert 'Sealed' in ['Draft', 'Planned', 'Implemented', 'Blocked', 'Ready for Review', 'Completed']

tests/contract/test_sealed_status_domain.py:213: AssertionError
____ test_non_disposable_owner_status_verdict_table_carries_the_sealed_row _____
[gw7] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_owner_status_verdict_table_carries_the_sealed_row():
        """C-029 surface 6b: the closed status × verdict table's `Sealed` row."""
        rows = _non_disposable_status_rows()
>       assert SEALED in rows, (
            "the status × verdict table carries no `Sealed` row — the value falls outside the "
            "judged range instead of being judged (C-029 surface 6b, FR-001)"
        )
E       AssertionError: the status × verdict table carries no `Sealed` row — the value falls outside the judged range instead of being judged (C-029 surface 6b, FR-001)
E       assert 'Sealed' in {'---': ['---', '---'], 'Blocked': ['**✗ 矛盾**——注册表记了一个检查器看不见的阻断', '一致，且为绿'], 'Completed': ['一致', '**✗ 矛盾**——闭环为 `block` 的已完成特性'], 'Draft': ['**✗ 矛盾**——还在草案的特性不算闭环', '一致'], ...}

tests/contract/test_sealed_status_domain.py:290: AssertionError
_ test_template_transition_table_carries_the_sealed_edges_and_seven_state_set __
[gw1] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_template_transition_table_carries_the_sealed_edges_and_seven_state_set():
        """C-029 surface 1: § Canonical Status State Machine's transition table."""
        transitions = _transitions(_template_state_machine())
        assert transitions, (
            "templates/feature-details-template.md § Canonical Status State Machine carries no "
            "parseable transition rows — the surface this guard names is gone"
        )
        states = {s for frm, to, _ in transitions for s in (frm, to) if s and s != "(n/a)"}
>       assert states == SEVEN_STATUSES, (
            "templates/feature-details-template.md § Canonical Status State Machine transition table "
            "MUST carry the seven-status set; measured %r (C-029 surface 1, FR-001)"
            % sorted(states)
        )
E       AssertionError: templates/feature-details-template.md § Canonical Status State Machine transition table MUST carry the seven-status set; measured ['Blocked', 'Completed', 'Draft', 'Implemented', 'Planned', 'Ready for Review'] (C-029 surface 1, FR-001)
E       assert {'Blocked', '...y for Review'} == {'Blocked', '... Review', ...}
E         
E         Extra items in the right set:
E         'Sealed'
E         Use -v to get more diff

tests/contract/test_sealed_status_domain.py:151: AssertionError
__________ test_schema_owner_defines_sealed_and_its_single_transition __________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_schema_owner_defines_sealed_and_its_single_transition():
        """C-025: the value and the transition are decided in § Feature Status, not in a carrier."""
        body = _owner_feature_status()
>       assert SEALED in body, (
            "shared/workflow/acceptance-hardening.md § Feature Status does not define `Sealed`; "
            "the schema owner MUST decide the value before any carrier projects it (C-025)"
        )
E       AssertionError: shared/workflow/acceptance-hardening.md § Feature Status does not define `Sealed`; the schema owner MUST decide the value before any carrier projects it (C-025)
E       assert 'Sealed' in '\n\n`Blocked` is a **first-class feature status**, not "`Implemented` with a note attached". It says: the work that\n... user did not object", an agent\'s own confirmation, or a later\ndiscovery that nobody wrote down is not evidence.\n\n'

tests/contract/test_sealed_status_domain.py:112: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_sealed_status_domain.py::test_feature_integration_carries_the_seal_protocol_row_and_closes_completed
FAILED tests/contract/test_sealed_status_domain.py::test_template_feature_status_token_and_status_bullet_admit_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_index_template_vocabulary_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_check_engine_judges_the_sealed_cells
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_owner_domain_line_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_closure_completion_claim_family_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_manage_features_vocabulary_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_owner_status_verdict_table_carries_the_sealed_row
FAILED tests/contract/test_sealed_status_domain.py::test_template_transition_table_carries_the_sealed_edges_and_seven_state_set
FAILED tests/contract/test_sealed_status_domain.py::test_schema_owner_defines_sealed_and_its_single_transition
10 failed in 6.17s
```

**读数**：10/10 红，逐腿点名 7 个 C-029 surface + schema owner + non-disposable 引擎表 + closure completion-claim 家族；红由「面尚未携带 `Sealed`」引起（消息逐条给出实测成员表），不是解析崩溃。
