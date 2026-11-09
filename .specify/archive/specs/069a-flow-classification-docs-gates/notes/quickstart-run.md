# Quickstart 重跑记录 — T034 ③

**Run**: 2026-10-24 · branch `069-execution-expression-sdd` · run-start HEAD `c3a8f325`
**Repo**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
**Interpreter**: `python3`（引擎）/ `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（测试，本仓 `.venv` 无 pytest）
**判据**: 本文件贴的是**真实输出摘录**（未改字，长 JSON 只截断不重写）；每条给命令、输出与退出码。场景 0/5 属基线/脚手架记录，不在 T034 的重跑集内。

---

## 场景 1 — 查表与缺口

```bash
$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs" --format json
{
  "action": "lookup",
  "checked_at": "2026-10-24T14:52:57Z",
  "unit_id": "/speckit.docs",
  "flow_class": "expression",
  "source": "ledger",
  "marker": null,
  "basis": "reader-oracle",
  "neutral": false,
  "error": null
}
# exit 0

$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.nonexistent" --format json
{
  "action": "lookup",
  "checked_at": "2026-10-24T14:52:57Z",
  "unit_id": "/speckit.nonexistent",
  "flow_class": "execution",
  "source": "default",
  "marker": "未声明·按默认",
  "basis": null,
  "neutral": false,
  "error": null
}
# exit 0（未登记单元：默认类 + 固定标记，不呈现为已判定）

$ python3 scripts/python/flow-class-check.py --action check --format json
{
  "action": "check",
  "checked_at": "2026-10-24T14:52:56Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "units": 78,
  "inventory": { "commands": 27, "skills": 51, "floors": { "commands": 27, "skills": 51 } },
  "findings": [],
  "error": null
}
# exit 0（零缺口）
```

**缺口演练（不改本仓台账：`--repo` 指向临时夹具）**——临时树含 27 个命令模板 + 51 个 `SKILL.md` + 台账副本（删去 `skill:humanize` 行）：

```bash
$ python3 scripts/python/flow-class-check.py --action check --repo ~/tmp/069a/drill.7PdvJ4 --format json
{
  "action": "check",
  "checked_at": "2026-10-24T14:57:02Z",
  "repo": "/Users/liuqiming.lqm/tmp/069a/drill.7PdvJ4",
  "units": 78,
  "inventory": { "commands": 27, "skills": 51, "floors": { "commands": 27, "skills": 51 } },
  "findings": [
    { "kind": "missing", "unit_id": "skill:humanize", "message": "inventory unit has no ledger row" }
  ],
  "error": null
}
# exit 1（缺口被报出；演练后本仓 lookup skill:humanize 仍 source=ledger / flow_class=expression）
```

**分类正确性（场景 1 的 route b）**

```bash
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_flow_class_correctness.py -p no:cacheprovider --tb=no -v
tests/contract/test_flow_class_correctness.py::test_fixture_matrix_is_not_vacuous PASSED      [ 25%]
tests/contract/test_flow_class_correctness.py::test_lookup_matches_independent_oracle PASSED  [ 50%]
tests/contract/test_flow_class_correctness.py::test_mutating_one_class_turns_the_same_comparison_red PASSED [ 75%]
tests/contract/test_flow_class_correctness.py::test_source_and_marker_invariants_hold_for_every_unit PASSED [100%]
============================== 4 passed in 5.95s ==============================
```

fixture 覆盖 10 个单元（`expression` 4 / `execution` 4 / 混合 1 / 类中立 1 / 未声明 1），oracle 表独立书写于测试内（`ORACLE`，第 76–86 行），变异断言 = `test_mutating_one_class_turns_the_same_comparison_red`。

---

## 场景 2 — 文档型门禁三面

route b（`test_doc_consistency_checker.py`）已在场景 6 的全量运行中全绿；下面贴 route a 的真实引擎输出。夹具 `~/tmp/069a/docfix.qLYL6T/docs/`：

```bash
$ python3 scripts/python/doc-consistency-check.py --action verify --path <fixture>/docs/clean.md --faces reader,evidence --format json
{"action": "verify", "checked_at": "2026-10-24T14:54:06Z",
 "scope": {"spec_dir": null, "paths": ["<fixture>/docs/clean.md"], "files_scanned": 1},
 "faces": {"reader": "pass", "evidence": "not-evaluated"},
 "findings": [],
 "count_check": {"status": "not-run", "reason": "count face not requested"},
 "degradations": [{"face": "evidence", "status": "not-evaluated", "path": "<fixture>/docs/clean.md", "line": 6,
   "reason": "not a git working tree or unreadable history: fatal: not a git repository (or any of the parent directories): .git"}]}
# exit 0（fixture 不在 git 树内 → evidence 面显式 not-evaluated，不静默绿）

$ python3 scripts/python/doc-consistency-check.py --action verify --path <fixture>/docs/dup-b.md --path <fixture>/docs/dup-a.md --faces duplicate --format json
{"action": "verify", "checked_at": "2026-10-24T14:54:06Z",
 "scope": {"spec_dir": null, "paths": ["<fixture>/docs/dup-b.md", "<fixture>/docs/dup-a.md"], "files_scanned": 2},
 "faces": {"duplicate": "fail"},
 "findings": [{"face": "duplicate", "rule": "duplicate-fact",
   "path": "<fixture>/docs/dup-a.md", "line": 3,
   "snippet": "框架把分类判据集中在一处定义，其余位置一律引用路径而不复述判据句，避免第二份清单随所有者改动而漂移。",
   "counterpart": "<fixture>/docs/dup-b.md:3",
   "fix_direction": "改为对唯一 owner 的引用"}],
 "count_check": {"status": "not-run", "reason": "count face not requested"}, "degradations": []}
# exit 1（注入 1：owner 原文副本 → duplicate-fact，两侧定位齐备）
```

三类注入（SC-007）的机械化钉住在同一测试文件的三个用例，本次逐条实跑：

```bash
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_doc_consistency_checker.py::test_c05_copied_owner_text_is_reported_as_duplicate_fact \
    tests/contract/test_doc_consistency_checker.py::test_c04_evidence_asof_stale_against_last_commit \
    tests/contract/test_doc_consistency_checker.py::test_c06_injected_count_mismatch_is_reported -v --tb=short
...::test_c05_copied_owner_text_is_reported_as_duplicate_fact PASSED [ 33%]
...::test_c04_evidence_asof_stale_against_last_commit PASSED           [ 66%]
...::test_c06_injected_count_mismatch_is_reported PASSED               [100%]
============================== 3 passed in 2.50s ==============================
```

---

## 场景 3 — 三项基线的冻结

```bash
$ python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json | head -c 400
[
  {
    "kind": "speckit.exec-quant",
    "schema_version": 2,
    "unit_id": "skill:git-utils",
    "unit_type": "skill",
    "run_id": "git-utils-merge-gitlab-20261020",
    "collected_at": "2026-10-20T02:39:20Z",
    ...
# exit 0（通道在位；按声明的门禁单元集 {/speckit.docs, skill:create-docs, /speckit.humanize, skill:humanize}
#         过滤：26 条记录中 0 条命中，见 notes/expression-baseline.md）

$ python3 scripts/python/run-determination.py --action history --target /speckit.plan --limit 3 --json | head -12
{
  "target": "/speckit.plan",
  "counts": { "total": 5, "settled": 0, "unsettled": 5, ... },
  "records": [
    { "unit_id": "/speckit.plan", "run_id": "064-subagent-concurrency-analyze-rerun-20261020",
      "determined_at": "2026-10-20T05:04:11Z", ...
# exit 0

$ git log -1 --format=%cs -- .specify/specs/069a-flow-classification-docs-gates/requirements.md
2026-10-24
# 冻结点＝开工前＝requirements 首次提交

$ python3 scripts/python/run-determination.py --action history --target /speckit.analyze --limit 3 --json
{ "counts": { "total": 5, ... }, "records": [ ... 064/055 等其他特性的记录 ... ] }
# 本切片无 /speckit.analyze 运行记录 → requirements→analyze 墙钟无可取的终点时间戳
```

冻结值见 `notes/expression-baseline.md`。

---

## 场景 4 — 兼容与分发

```bash
$ shasum -a 256 .specify/specs/062-humanize-command/requirements.md \
                .specify/specs/067-loop-efficiency-hardening/requirements.md \
                .specify/specs/068-exec-quant-feedback-channel/requirements.md
987b24ea1f98abb2a01d14779814eab28416f4ad1cbd81a36d51efb72d5f9da0  .specify/specs/062-humanize-command/requirements.md
29e26b701ebef9d80782b9a215ef97759290a384d898cb3320cfedde161fa0cd  .specify/specs/067-loop-efficiency-hardening/requirements.md
ec20d5e28bd0eb5e2afdbd851cb753ef6e1c37a1c24e66b196f9305f18b45af7  .specify/specs/068-exec-quant-feedback-channel/requirements.md

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
# exit 0

$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (396 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (112 files)
ok    shared/ == .specify/shared/ (55 files)
# exit 0

$ grep -n "flow-class-check.py\|expression-gates.md\|flow-class-definitions.md" templates/commands/docs.md
34:- **先读数、后判定**：在任何门禁判定之前执行一次 `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs"` …
35:- **按门禁 owner 的调用点行执行算子**：… 唯一所有者是 `shared/workflow/expression-gates.md` …

$ grep -n "flow-class-definitions.md\|expression-gates.md" templates/commands/humanize.md
26:- 类别（判据、两个取值与逐流程台账）的唯一所有者：`shared/definitions/flow-class-definitions.md`；本命令不读取类别，也不调用任何脚本。
27:- 文档型门禁算子集的唯一所有者：`shared/workflow/expression-gates.md`；本命令不执行算子。

$ grep -n "flow-class-check.py\|--action lookup\|doc-consistency-check.py" templates/commands/humanize.md
# （空）——humanize 命令保持 Simple

$ grep -n "doc-consistency-check.py" templates/commands/docs.md
35:… 三面由 `python3 .specify/scripts/python/doc-consistency-check.py --action verify` 承担 …

$ grep -c "SKILL.md" templates/commands/humanize.md
1

$ grep -rn "flow-class-check.py\|expression-gates.md\|doc-consistency-check.py" templates/commands/*.md skills/*/*/SKILL.md \
    | grep -v -e "commands/docs.md" -e "commands/humanize.md" -e "create-docs/SKILL.md" -e "humanize/SKILL.md"
# （空）——接线封闭集之外零调用点

$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_humanize_command_surface.py -q -p no:cacheprovider
..........                                                               [100%]
10 passed in 0.05s
```

---

## 场景 6 — 全量回归

```bash
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider
...
33 failed, 4267 passed, 5 skipped, 1 warning in 252.83s (0:04:12)
# exit 1（pytest 原生；判据是名字级差值，不是绝对绿）

$ grep -E '^FAILED ' <run log> | sed -E 's/^FAILED //; s/ - .*$//' | sort -u > current-failures.txt
$ grep -vE '^#' notes/test-baseline-contract.txt | sort -u > baseline-failures.txt
$ comm -13 baseline-failures.txt current-failures.txt
# （空）= 零 NEW
$ comm -23 baseline-failures.txt current-failures.txt
# （空）= 基线内 33 条失败原样保留，无一条转绿（名单逐名相同）
```

**差值**：基线 `33 failed / 4177 passed / 5 skipped`（HEAD `01d1feaa`）→ 本次 `33 failed / 4267 passed / 5 skipped`，失败名单 33 = 33 且逐名相同（零 NEW、零 GONE）。pass 数 +90 的构成已核到名字级：6 支新增契约测试 **86** 用例 + 既有 `tests/contract/test_mirror_parity_suite.py` 中按文件参数化的 **4** 条新 id（`scripts/python/{doc-consistency-check,flow-class-check}.py`、`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md` 的镜像同字节用例，因载荷文件新增而自然增长）。另外 2 支新增**单元**测试（38 用例）不在 `tests/contract` 收集面，单独运行时 `38 passed`。
