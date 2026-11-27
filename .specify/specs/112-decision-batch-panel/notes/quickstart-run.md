# Quickstart run — 112-decision-batch-panel（T057）

**Date**: 2026-11-27 · **Package**: P4 · **Worktree**: `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`（HEAD at run start `8d5aafb37`）
**Engine**: `python3 scripts/python/decision-batch.py`（framework source; mirror `.specify/scripts/python/decision-batch.py` byte-identical）
**Rule**: every scenario in `.specify/specs/112-decision-batch-panel/quickstart.md` executed as written; commands, decisive output and exit status recorded per scenario. Sanctioned scratch root: `.specify/.tmp/` (git-ignored), torn down at the end.

## Scenario 1 — Inspect the pending sources（executed）

```text
$ awk -F'|' '$2 ~ /^ *(OI-|D-)/ && $5 ~ /^ *open([[:space:],，（(]|$)/ {n++} END{print n+0}' .specify/register.md
17
$ grep -rE '^### PENDING —' .specify/specs .specify/goals .specify/anchoring .specify/teams | wc -l
0
$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:112-decision-batch-panel"
unit_id: spec:112-decision-batch-panel
flow_class: execution
flow_type: -
source: declaration
marker: null
basis: null
neutral: false
rc = 0
```

Matches the plan-time measurement: 17 register-derived candidates, zero authored blocks, flow class `execution`.

## Scenario 2 — One complete presentation（pinned; now executable）

```text
$ python3 scripts/python/decision-batch.py scan --workspace-root . --format text > /tmp/s2.txt   # rc 0
$ grep -c '^==== 事项' /tmp/s2.txt
17
$ grep -c '当前状态：信息不完整' /tmp/s2.txt
17
$ grep -c '建议默认值：本项没有唯一的默认选项。' /tmp/s2.txt
17
```

Expected shape confirmed: 17 item rows in deterministic order, each `incomplete` with named reasons
(`class-missing` / `authority-unresolved`) and no invented slot value; bookkeeping
`candidates = presented rows + merged references + named exclusions` with per-source counts and verdict
`complete`; zero `ai-autonomous` presentations; zero batch records written (`.specify/knowledge/` untouched).

## Scenario 3 — Object only, record the batch（pinned; executed on `.specify/.tmp/decide-demo/`）

Workspace: one complete reversible item (`演示批量静默项`), one complete item named in the reply
(`演示批量异议项`), one `irreversible-default` item (`演示批量不可逆项`), one `ai-autonomous` item
(`演示批量自主项`). Reading note: the scenario's expected result names **both** an `accepted-default` and an
`objected-alternative`, so the workspace carries two settle-able human items plus the irreversible and the
autonomous one.

```text
$ python3 scripts/python/decision-batch.py scan --workspace-root .specify/.tmp/decide-demo --format json > .specify/.tmp/decide-demo/scan.json
scan rc = 0
$ python3 scripts/python/decision-batch.py record \
    --workspace-root .specify/.tmp/decide-demo \
    --presentation .specify/.tmp/decide-demo/scan.json \
    --reply .specify/.tmp/decide-demo/reply.md \
    --authorization interactive
批次记录已写入：.specify/knowledge/decision-batch-b-20261127t105530z-28f0c049.md
批次编号：B-20261127T105530Z-28f0c049
已结案 2 项，暂缓 0 项，保持待定 1 项。
  D-001  演示批量静默项  accepted-default
  D-002  演示批量异议项  objected-alternative
登记册：.specify/register.md，追加 2 行，更新 0 个状态单元格。
来源块更新：.specify/specs/demo/items.md
record rc = 0
```

Item row table in the record:

```text
| 演示批量静默项 | authored-pending-item@.specify/specs/demo/items.md | eligible | no-evidence | 方案甲 | accepted-default | D-001 |
| 演示批量异议项 | authored-pending-item@.specify/specs/demo/items.md | eligible | no-evidence | 方案甲 | objected-alternative | D-002 |
| 演示批量不可逆项 | authored-pending-item@.specify/specs/demo/items.md | irreversible-default(default-irreversible) | no-evidence | 立即切换 | pending | — |
```

The `ai-autonomous` candidate was excluded `not-human-held`
（`{'reason': 'not-human-held', 'subject': '演示批量自主项', 'classes': ['ai-autonomous']}`，partition
`presented_rows=3 / not_human_held=1 / already_resolved=0`，判定 `complete`）。The settled blocks gained
`- **resolution**: B-20261127T105530Z-28f0c049 -> D-001` / `-> D-002`。Same-id second write：

```text
$ python3 scripts/python/decision-batch.py record … --authorization interactive
拒绝：来源 record-request 不可用（duplicate-batch）：B-20261127T105530Z-28f0c049: … already exists; a second
record for the same batch id is refused before the write surface runs
dup rc = 1
```

## Scenario 4 — Replay the batch from the record alone（pinned; executed）

```text
$ python3 scripts/python/decision-batch.py replay \
    --workspace-root .specify/.tmp/decide-demo \
    --batch .specify/.tmp/decide-demo/.specify/knowledge/decision-batch-b-20261127t105530z-28f0c049.md
批次重放 B-20261127T105530Z-28f0c049
完备性：候选 4 = 呈现行 3 + 合并引用 0 + 具名排除 1；判定 complete
> 只对「演示批量异议项」改为「方案乙」，其余没意见。
- 演示批量静默项：eligible；建议默认 方案甲；接地 no-evidence；处置 accepted-default；决策 D-001
- 演示批量异议项：eligible；建议默认 方案甲；接地 no-evidence；处置 objected-alternative；决策 D-002
- 演示批量不可逆项：irreversible-default(default-irreversible)；建议默认 立即切换；接地 no-evidence；处置 pending
- D-001 演示批量静默项：方案甲（accepted-default）
- D-002 演示批量异议项：方案乙（objected-alternative）
指针解析：8/8 可解析。
replay rc = 0
```

Broken-pointer copy（one option-evidence pointer）.:

```text
$ sed 's#\.specify/specs/demo/ref\.md#.specify/specs/demo/missing-ref.md#' <record> > .specify/.tmp/decide-demo/broken-record.md
$ python3 scripts/python/decision-batch.py replay … --batch .specify/.tmp/decide-demo/broken-record.md
拒绝：来源 replay-pointers 不可用（unresolvable-pointer）：.specify/specs/demo/missing-ref.md: path does not exist
broken rc = 1
```

## Scenario 5 — Refusal and honest emptiness（pinned; executed）

```text
$ python3 scripts/python/decision-batch.py scan --workspace-root .specify/.tmp/qs-unparseable
拒绝：来源 register-open-decision-row 不可用（unparseable）：.specify/register.md: the table cannot be parsed into its columns
本次没有呈现任何事项，也没有写入任何内容。
rc = 1

$ python3 scripts/python/decision-batch.py scan --workspace-root .specify/.tmp/qs-absent --format json
result: presentation
absent_roots: ['.specify/goals', '.specify/anchoring', '.specify/teams']
claim absent_sources: ['.specify/goals', '.specify/anchoring', '.specify/teams']
verdict: complete                       # absent roots are named, never read as clean

$ python3 scripts/python/decision-batch.py scan --workspace-root .specify/.tmp/qs-empty
批量决策面板 · 本次呈现
当前没有待决策项。
…（完备性声明含缺席来源：.specify/register.md、.specify/specs、.specify/goals、.specify/anchoring、.specify/teams）
rc = 0                                  # .specify/knowledge/ was not created
```

## Scenario 6 — Inspect recorded batches（executed）

```text
$ ls .specify/knowledge/ | grep '^decision-batch-' | wc -l
0
```

The repository tree's own knowledge store stayed empty — every demo record lived inside a `.specify/.tmp/`
workspace. After Scenario 3 the demo workspace itself lists one record per batch.

## Scenario 7 — Maintainer verification（executed）

The checker resolves evidence pointers repository-relative or carrier-relative; the recorded demo record was
copied to the workspace root (the P3-precedented reading) so its workspace-relative pointers resolve:

```text
$ cp .specify/.tmp/decide-demo/.specify/knowledge/decision-batch-b-20261127t105530z-28f0c049.md \
     .specify/.tmp/decide-demo/record-carrier.md
$ python3 scripts/python/validate-decisions.py --action records \
    --carrier .specify/.tmp/decide-demo/record-carrier.md \
    --register .specify/.tmp/decide-demo/.specify/register.md
PASS: 0 violation(s) (rules: M-01, M-02, M-03, M-04, M-08, M-09)
validator rc = 0
```

```text
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q
59 passed in 7.54s
rc = 0
```

## Teardown

```text
$ rm -rf .specify/.tmp/decide-demo .specify/.tmp/qs-unparseable .specify/.tmp/qs-absent .specify/.tmp/qs-empty .specify/.tmp/p4-supersede-demo
$ ls .specify/.tmp/
（empty）
```

No state was left outside the sanctioned temp root; the repository's runtime stores were never written.