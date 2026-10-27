# Quickstart S3–S8 实跑记录（T028）

- 运行时间： 2026-10-27T12:48Z（本记录由实跑日志逐字组装， 命令/输出/退出码均为真实执行结果）。
- 方法： 每个 Scenario 在 `tests/fixtures/client_project.py` 构建的一次性客户夹具（git 仓库 + 最小 `.specify/` 运行时， hat=client）内实跑； 引擎经自定位规则锚定夹具根, 与真实客户拓扑一致。
- PLAN-EDIT: 无。plan 属主 `quickstart.md` 未改写——其 S3–S8"未实现/逐例豁免"措辞是计划期（实现前）时点记录, 本文件以实跑证据承担 closure 留痕; 判定为无需 minor 修订（假设已记录, 若编排者认定必须更新豁免措辞, 可按 `PLAN-EDIT: .specify/specs/072-client-self-improvement/quickstart.md — S3–S8 已实现并实跑， 豁免措辞过时；分类=minor` 另行处理）。
- 输出读法备注：
  - S4-g `report --summary --format json` 退出码 `1` 是退出字母表的正常成员（0 允许 / 1 拒绝=当前记录有 blocking 计数, 此处 blocking=1 → deny）, 非执行失败。
  - S4/S5/S6/S8 输出中的 ANSI 颜色转义为脚本真实 stdout 字节, 未做美化。
  - S6 `package` 在排除唯一外部条目后无剩余可打包内容, 故 `"zip": null`、未写任何打包产物——排除语义由 `"excluded_external": 1` 实证。
  - S8 `/speckit.improve custom:myteam/review-loop` 是聊天指令而非终端命令; 实跑的是其在客户项目内的引擎可观测面（观察源读取 + run-determination 对 custom 主体的 fail-closed 判定, C-34）, SI-0..SI-9 流程面由 `tests/contract/test_client_improve_loop.py` 钉住。

---

## S3 在模拟客户项目里武装客户通道（实跑）

fixture root: `/tmp/client-project-ec43c8p9/repo`（一次性 git 仓库, hat=client）

武装前外部探针对象数: `0`（probes --format json 的 objects[] 按 `ext-` 前缀推导, C-9）

**S3 probe-inject（quickstart 原命令形态, 在夹具根内执行）**

```bash
$ cd /tmp/client-project-ec43c8p9/repo
$ python3 /tmp/client-project-ec43c8p9/repo/.specify/scripts/python/probe-utils.py --action probe-inject --unit custom:myteam/review-loop --workspace-root /tmp/client-project-ec43c8p9/repo
```

exit code: `0`

stdout:

```text
{
  "object_id": "ext-myteam-review-loop",
  "class_id": "external-custom",
  "path": ".specify/memory/feedback/probes/ext-myteam-review-loop.md",
  "note": "external probe feedback stays host-project-local; it is excluded from upstream packages."
}
```

武装后外部探针对象数: `1`；units=['custom:myteam/review-loop']

拆卸: 夹具随上下文退出 `shutil.rmtree(/tmp/client-project-ec43c8p9/repo)`（见文末拆卸汇总）。

## S4 一次评审运行自动采集一条指针条目（实跑）

fixture root: `/tmp/client-project-mje4ob23/repo`；已武装 `custom:myteam/review-loop`

**S4-0 采集前 list --kind external**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ python3 /tmp/client-project-mje4ob23/repo/.specify/scripts/python/feedback-utils.py --action list --kind external --format json --workspace-root /tmp/client-project-mje4ob23/repo
```

exit code: `0`

stdout:

```text
{
  "count": 0,
  "matches": []
}
```

**S4-a 非交互路径第 1-3 步: triage (triage=run 才合格)**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh triage --since HEAD~1 --head HEAD
```

exit code: `0`

stdout:

```text
base=780e1c1749d13708804b296f3d5229982587c0aa
head=ab5089c1a38e9b4e9cb942f30d4d1795c0ef13ab
base_source=explicit
changed_files=1
triage=run
basis=code path in the committed delta: src/app.py
```

**S4-b 非交互路径第 4 步: start (创建 code-review.md 记录)**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh start --spec .specify/specs/072-demo --since HEAD~1 --head HEAD --triage run
```

exit code: `0`

stdout:

```text
[0;32m✓ 代码段记录已创建: .specify/specs/072-demo/code-review.md[0m
record=.specify/specs/072-demo/code-review.md
archive=none
base=780e1c1749d13708804b296f3d5229982587c0aa
head=ab5089c1a38e9b4e9cb942f30d4d1795c0ef13ab
base_source=explicit
renderer=text
```

**S4-c note -s blocking**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh note -s blocking -f src/app.py -c real defect found in app.py --review-file .specify/specs/072-demo/code-review.md
```

exit code: `0`

stdout:

```text
[0;32m✓ 已追加: [blocking] src/app.py[0m
```

**S4-c note -s praise**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh note -s praise -f src/app.py -c clean change otherwise --review-file .specify/specs/072-demo/code-review.md
```

exit code: `0`

stdout:

```text
[0;32m✓ 已追加: [praise] src/app.py[0m
```

**S4-d receipt (覆盖率回执, 第 4 步收尾)**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh receipt --review-file .specify/specs/072-demo/code-review.md --since HEAD~1 --head HEAD
```

exit code: `0`

stdout:

```text
[0;32m✓ 覆盖率回执已写入: .specify/specs/072-demo/code-review.md[0m
base=780e1c1749d13708804b296f3d5229982587c0aa
head=ab5089c1a38e9b4e9cb942f30d4d1795c0ef13ab
base_source=explicit
renderer=text
changed_files=1
judged_files=1
skipped_files=0
gap_files=0
lines_added=1
lines_deleted=1
blocking_entries=1
verdict=blocked
uncommitted_scope=1
record=.specify/specs/072-demo/code-review.md

<!-- coverage-receipt:begin -->
receipt_version=1
base=780e1c1749d13708804b296f3d5229982587c0aa
head=ab5089c1a38e9b4e9cb942f30d4d1795c0ef13ab
base_source=explicit
renderer=text
changed_files=1
judged_files=1
skipped_files=0
gap_files=0
lines_added=1
lines_deleted=1
file.01.path=src/app.py
file.01.verdict=reviewed
<!-- coverage-receipt:end -->
```

**S4-e 非交互路径第 5 步: capture（自动采集一条指针条目）**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh capture --review-file .specify/specs/072-demo/code-review.md --triage run
```

exit code: `0`

stdout:

```text
capture: client-channel-armed triage=run unit=custom:myteam/review-loop run=2026-10-27T12:48:45Z entry=20261027T124845Z-custom-myteam-review-loop unit_source=auto:unique-external-probe
```

**S4-f 同 (unit, run) 再采一次（幂等: 零新增）**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh capture --review-file .specify/specs/072-demo/code-review.md --triage run
```

exit code: `0`

stdout:

```text
capture: client-channel-armed triage=run unit=custom:myteam/review-loop run=2026-10-27T12:48:45Z entry=20261027T124845Z-custom-myteam-review-loop unit_source=auto:unique-external-probe
```

**S4-g report --summary --format json（六项计数复算面）**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh report --summary --format json --file .specify/specs/072-demo/code-review.md
```

exit code: `1`

stdout:

```text
{"record":".specify/specs/072-demo/code-review.md","counts":{"blocking":1,"important":0,"suggestion":0,"nitpick":0,"question":0,"praise":1},"blocking_entries":1,"gate":"deny"}
```

**S4-h 采集后 list --kind external（count 0 → 1）**

```bash
$ cd /tmp/client-project-mje4ob23/repo
$ python3 /tmp/client-project-mje4ob23/repo/.specify/scripts/python/feedback-utils.py --action list --kind external --format json --workspace-root /tmp/client-project-mje4ob23/repo
```

exit code: `0`

stdout:

```text
{
  "count": 1,
  "matches": [
    {
      "id": "20261027T124845Z-custom-myteam-review-loop",
      "file": "20261027T124845Z-custom-myteam-review-loop.md",
      "unit_id": "custom:myteam/review-loop",
      "unit_type": "custom-unit",
      "run_id": "2026-10-27T12:48:45Z",
      "probe": "ext-myteam-review-loop",
      "kind": "external",
      "slice": "host-custom",
      "feature": "",
      "feature_id": "",
      "disposition": "",
      "introspection_ref": "",
      "disposition_reason": "",
      "partial": false,
      "created": "2026-10-27T12:48:45Z",
      "summary": "record=.specify/specs/072-demo/code-review.md",
      "path": ".specify/memory/feedback/20261027T124845Z-custom-myteam-review-loop.md"
    }
  ]
}
```

指针条目全文（note 型, 闭集字段, 无意见正文 — C-15）:

```text
---
id: "20261027T124845Z-custom-myteam-review-loop"
unit_id: "custom:myteam/review-loop"
unit_type: "custom-unit"
run_id: "2026-10-27T12:48:45Z"
scope: "local"
probe: "ext-myteam-review-loop"
kind: "external"
slice: "host-custom"
partial: false
created: "2026-10-27T12:48:45Z"
summary: "record=.specify/specs/072-demo/code-review.md"
---

## Review
record=.specify/specs/072-demo/code-review.md
triage=run
blocking=1
important=0
suggestion=0
nitpick=0
question=0
praise=1
run=2026-10-27T12:48:45Z
unit=custom:myteam/review-loop

## Optimization Points
- pointer payload assembled from 'report --summary --format json'; no review bodies, per-file verdict lists, or file counts (C-15)
```

拆卸: 夹具随上下文退出 `shutil.rmtree(/tmp/client-project-mje4ob23/repo)`。

## S5 三种"没采集"的具名披露（实跑）

### S5-1 client-channel-unarmed（零外部探针对象, 不带 --unit）

**S5-1 capture（未武装夹具）**

```bash
$ cd /tmp/client-project-kvbc5n7i/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh capture --review-file .specify/specs/072-demo/code-review.md --triage run
```

exit code: `0`

stdout:

```text
capture: client-channel-unarmed triage=run reason=no external probe object in this client project; guidance=arm the channel via 'probe-utils.py --action probe-inject --unit custom:<owner>/<name>'; zero entries
```

拆卸: `shutil.rmtree(/tmp/client-project-kvbc5n7i/repo)`。

### S5-2 client-unit-ambiguous（两个外部探针对象, 无 --client-unit）

fixture root: `/tmp/client-project-182fplvb/repo`；武装 `custom:myteam/review-loop` 与 `custom:myteam/other-loop` 两个外部对象

**S5-2 capture（两对象未指明单元）**

```bash
$ cd /tmp/client-project-182fplvb/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh capture --review-file .specify/specs/072-demo/code-review.md --triage run
```

exit code: `0`

stdout:

```text
capture: client-unit-ambiguous triage=run reason=2 external probe objects and no explicit --unit — no guessing, no rotation, no most-recently-used (C-5); zero entries
```

拆卸: `shutil.rmtree(/tmp/client-project-182fplvb/repo)`。

### S5-3 no-capture-object（适用性非 run）

triage 输出末行: `basis=code path in the committed delta: src/app.py`
**S5-3 capture --triage not-applicable**

```bash
$ cd /tmp/client-project-gttysnty/repo
$ bash /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh capture --review-file .specify/specs/072-demo/code-review.md --triage not-applicable
```

exit code: `0`

stdout:

```text
capture: no-capture-object triage=not-applicable reason=no record exists for applicability 'not-applicable' — nothing to point at (C-14); zero entries
```

拆卸: `shutil.rmtree(/tmp/client-project-gttysnty/repo)`。

## S6 消化: 载体指派与打包排除（实跑打包排除面）

fixture root: `/tmp/client-project-nxqq0yti/repo`；已武装 `custom:myteam/review-loop`

采集后外部条目数: `1`

**S6 package --format json（外部条目无条件排除, 只报计数）**

```bash
$ cd /tmp/client-project-nxqq0yti/repo
$ python3 /tmp/client-project-nxqq0yti/repo/.specify/scripts/python/feedback-utils.py --action package --format json --workspace-root /tmp/client-project-nxqq0yti/repo
```

exit code: `0`

stdout:

```text
{
  "packaged": 0,
  "zip": null,
  "missing": [],
  "upstream": {
    "url": "https://gitlab.alibaba-inc.com/cloud-native-ai/spec-kit.git",
    "source": "install-metadata",
    "commit": "4f73c21d257fe7e263bbbf2e1797e4c38adc4b3d"
  },
  "note": "No feedback entries or exec-quant payload records to package.",
  "exec_quant_payload": {
    "record_count": 0,
    "source_form_counts": {
      "records-dir": 0,
      "legacy-jsonl": 0
    },
    "skipped_unreadable": 0,
    "truncated_count": 0,
    "cap_records": 1000,
    "cap_bytes": 16777216,
    "collected_at_range": null,
    "identity_status": "identified",
    "project_name": "repo",
    "source_commit": "303c19460b86b2a59e16717c43f1213a01ee54ae"
  },
  "excluded_external": 1
}
```

载体指派（Park / 新规格 / 改进循环, 恰好一个）由改进循环面履行, 见 S8；其契约钉住为 `tests/contract/test_client_package_exclusion.py`。

拆卸: 打包产物随夹具一并 `shutil.rmtree(/tmp/client-project-nxqq0yti/repo)`（打包写盘仅限一次性夹具内, 框架仓零写入）。

## S7 四条循环度量（实跑）

**S7 client-metrics --unit custom:myteam/review-loop --format json**

```bash
$ cd /tmp/client-project-8xypvej7/repo
$ python3 /tmp/client-project-8xypvej7/repo/.specify/scripts/python/feedback-utils.py --action client-metrics --unit custom:myteam/review-loop --format json --workspace-root /tmp/client-project-8xypvej7/repo
```

exit code: `0`

stdout:

```text
{
  "unit": "custom:myteam/review-loop",
  "boundary": "2026-10-27T12:48:46Z",
  "metrics": {
    "capture_coverage": {
      "status": "evaluated",
      "numerator": 1,
      "denominator": 1,
      "value": 1.0,
      "excluded_before_arming": 0,
      "boundary": "2026-10-27T12:48:46Z"
    },
    "into_loop_ratio": {
      "status": "evaluated",
      "numerator": 0,
      "denominator": 1,
      "value": 0.0
    },
    "closure_ratio": {
      "status": "evaluated",
      "numerator": 0,
      "denominator": 1,
      "value": 0.0
    },
    "repeat_finding_rate": {
      "status": "evaluated",
      "numerator": 0,
      "denominator": 1,
      "value": 0.0,
      "proxy": true,
      "proxy_label": "coarse proxy - (file, severity) pair reappearance across records of the same unit; not a defect recurrence rate",
      "excluded_unreadable_records": 0
    }
  }
}
```

度量键: boundary, metrics, unit

拆卸: `shutil.rmtree(/tmp/client-project-8xypvej7/repo)`。

## S8 客户主体的改进循环（实跑引擎可观测面）

`/speckit.improve custom:myteam/review-loop` 是聊天指令而非终端命令; 其在客户项目内的可实跑引擎面 = 观察源读取 + run-determination 对 custom 主体的 fail-closed 判定（C-34, 引擎理由逐字引用进 why 段）。以下在夹具内如实执行:

**S8-a 观察源: 客户通道条目清单（why 段的客户观察源）**

```bash
$ cd /tmp/client-project-plc4qzk8/repo
$ python3 /tmp/client-project-plc4qzk8/repo/.specify/scripts/python/feedback-utils.py --action list --kind external --format json --workspace-root /tmp/client-project-plc4qzk8/repo
```

exit code: `0`

stdout:

```text
{
  "count": 1,
  "matches": [
    {
      "id": "20261027T124847Z-custom-myteam-review-loop",
      "file": "20261027T124847Z-custom-myteam-review-loop.md",
      "unit_id": "custom:myteam/review-loop",
      "unit_type": "custom-unit",
      "run_id": "2026-10-27T12:48:47Z",
      "probe": "ext-myteam-review-loop",
      "kind": "external",
      "slice": "host-custom",
      "feature": "",
      "feature_id": "",
      "disposition": "",
      "introspection_ref": "",
      "disposition_reason": "",
      "partial": false,
      "created": "2026-10-27T12:48:47Z",
      "summary": "record=.specify/specs/072-demo/code-review.md",
      "path": ".specify/memory/feedback/20261027T124847Z-custom-myteam-review-loop.md"
    }
  ]
}
```

**S8-b run-determination determine（custom 主体 fail-closed, C-34）**

```bash
$ cd /tmp/client-project-plc4qzk8/repo
$ python3 /tmp/client-project-plc4qzk8/repo/.specify/scripts/python/run-determination.py --action determine --unit-id custom:myteam/review-loop --unit-type custom-unit --run-id run-quickstart-s8 --complexity complex --workspace-root /tmp/client-project-plc4qzk8/repo --json
```

exit code: `0`

stdout:

```text
{
  "unit_id": "custom:myteam/review-loop",
  "run_id": "run-quickstart-s8",
  "trigger_feedback": false,
  "verdicts": {
    "token_consumption": "not_evaluated",
    "elapsed": "not_evaluated",
    "artifact_correctness": "not_evaluated",
    "satisfaction": "not_evaluated"
  },
  "settled_previous": null,
  "persistence": {
    "persisted": false,
    "adapter": "memory-utils-session",
    "reason": "the memory engine's --source contract does not accept 'custom:myteam/review-loop'; the record is emitted but not landed"
  },
  "record": {
    "kind": "speckit.run-determination",
    "schema_version": 1,
    "unit_id": "custom:myteam/review-loop",
    "unit_type": "custom-unit",
    "run_id": "run-quickstart-s8",
    "feature": null,
    "feature_id": null,
    "determined_at": "2026-10-27T12:48:47Z",
    "settled_at": null,
    "complexity": "complex",
    "qualification": "qualified",
    "axes": {
      "token_consumption": {
        "verdict": "not_evaluated",
        "reason": "source_unavailable",
        "signal": {
          "key": "token_consumption",
          "direction": "reduce"
        },
        "measurement": {
          "source": "unavailable",
          "input_tokens": null,
          "output_tokens": null,
          "cache_read_input_tokens": null,
          "cache_creation_input_tokens": null,
          "total_tokens": null,
          "proxy_lines": null,
          "proxy_bytes": null,
          "note": null
        },
        "baseline": null,
        "evidence_refs": []
      },
      "elapsed": {
        "verdict": "not_evaluated",
        "reason": "source_unavailable",
        "signal": {
          "key": "elapsed",
          "direction": "reduce"
        },
        "measurement": {
          "source": "unavailable",
          "ms": null,
          "note": null
        },
        "baseline": null,
        "evidence_refs": []
      },
      "artifact_correctness": {
        "verdict": "not_evaluated",
        "reason": "no_declared_checks",
        "signal": {
          "key": "artifact_correctness",
          "direction": "improve"
        },
        "declared_checks": null,
        "collected": null,
        "failed_set_diff": {
          "status": "not_evaluated",
          "added": [],
          "added_count": null,
          "truncated": false
        },
        "green_evidence": {
          "status": "not_evaluated",
          "uncovered": []
        },
        "evidence_refs": []
      },
      "satisfaction": {
        "verdict": "not_evaluated",
        "reason": "pending_next_turn",
        "user_turn_class": "no_user_input",
        "unresolved_red": {
          "present": "unknown",
          "source": "undeclared"
        },
        "adjacent": false,
        "signal": {
          "key": "satisfaction",
          "direction": "improve"
        }
      }
    },
    "provenance": {
      "engine": "scripts/python/run-determination.py",
      "declared_by_caller": [
        "complexity",
        "user_turn_class",
        "unresolved_red",
        "qualification"
      ],
      "lanes_read": {
        "session": "unavailable",
        "user_input": "in_context",
        "evidence": "unavailable"
      },
      "evidence_digests": [],
      "honesty_boundary": [
        "the unresolved-red state is declared by the caller, never derived (§ 5.4)",
        "a wrap-up that never called determine leaves no trace: absence of a record is not evidence of a clean run (§ 4)"
      ],
      "red_state_input": "caller-declaration"
    },
    "change_point": {
      "id": "cp-run-quickstart-s8",
      "clean": false,
      "findings": [
        {
          "axis": "token_consumption",
          "verdict": "not_evaluated",
          "reason": "source_unavailable",
          "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
          "signal": {
            "key": "token_consumption",
            "direction": "reduce"
          },
          "evidence_refs": [],
          "status": "observed"
        },
        {
          "axis": "elapsed",
          "verdict": "not_evaluated",
          "reason": "source_unavailable",
          "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
          "signal": {
            "key": "elapsed",
            "direction": "reduce"
          },
          "evidence_refs": [],
          "status": "observed"
        },
        {
          "axis": "artifact_correctness",
          "verdict": "not_evaluated",
          "reason": "no_declared_checks",
          "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=None collected=None reason=no_declared_checks",
          "signal": {
            "key": "artifact_correctness",
            "direction": "improve"
          },
          "evidence_refs": [],
          "status": "observed"
        },
        {
          "axis": "satisfaction",
          "verdict": "not_evaluated",
          "reason": "pending_next_turn",
          "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
          "signal": {
            "key": "satisfaction",
            "direction": "improve"
          },
          "evidence_refs": [],
          "status": "observed"
        }
      ]
    },
    "passive_trigger": {
      "trigger_feedback": false,
      "composes_with_should_prompt": true,
      "out_of_scope": [
        {
          "observation": "token_consumption not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
          "parked_via": "none",
          "ref": null
        },
        {
          "observation": "elapsed not_evaluated via source=unavailable: current=None baseline=None reason=source_unavailable",
          "parked_via": "none",
          "ref": null
        },
        {
          "observation": "artifact_correctness not_evaluated: failed-set diff not_evaluated added=None, green evidence not_evaluated uncovered=0 declared_checks=None collected=None reason=no_declared_checks",
          "parked_via": "none",
          "ref": null
        },
        {
          "observation": "satisfaction not_evaluated: user_turn_class=no_user_input unresolved_red=unknown adjacent=False reason=pending_next_turn",
          "parked_via": "none",
          "ref": null
        }
      ]
    }
  }
}
```

persistence: `{"persisted": false, "adapter": "memory-utils-session", "reason": "the memory engine's --source contract does not accept 'custom:myteam/review-loop'; the record is emitted but not landed"}`

判定前后 `git status --short`: before=['?? .specify/'] after=['?? .specify/']（工作树零变更, fail-closed 不落地）

拆卸: `shutil.rmtree(/tmp/client-project-plc4qzk8/repo)`。

## 拆卸汇总

- 每个 Scenario 使用独立的一次性夹具, 由 `tests/fixtures/client_project.py` 的库管理 `tempfile.mkdtemp(prefix="client-project-")` 创建（临时目录纪律的枚举例外,fixture 模块自述为准）; 退出上下文即 `shutil.rmtree` 整个临时根, 含打包产物与全部引擎写盘。
- 框架仓零写入: 全程 `cwd` 在夹具内, 引擎经自定位规则锚定夹具根; 驱动脚本本身位于 `/tmp/t028-quickstart-run/driver.py`（系统临时区, 与仓库无关, 运行后可删）。
- 运行后复核: `git -C /storage/project/cloud-native-ai/spec-kit status --short` 只显示本特性预期产物（test-evidence / notes / 镜像同步）, 无夹具泄漏。
