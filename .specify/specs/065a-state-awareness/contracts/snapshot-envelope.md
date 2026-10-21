# Contract: Snapshot JSON 信封（`schema_version: 1`）

**Scope**: `loop-state.py --action snapshot` 的唯一输出形状。字段的实体级语义见 `data-model.md` §2–§7；本契约规定规范性约束与一个规范示例。
**Owner note**: derived `loop_state` 映射表与 watcher 优先不变量只在切片 `requirements.md` FR-004（parent #FR-004）定义一次；本契约引用它，不复制其规则。

## 0. 条款编号与别名

本契约的 14 条条款使用项目规范形态 `**C-N**`（语法 owner：`.specify/shared/definitions/contract-clause-definitions.md` §3）。全局编号接续 `loop-state-cli`（C-1…C-18）；历史文字引用使用下列别名。

| 历史别名 | 规范 ID | 历史别名 | 规范 ID |
|----------|---------|----------|---------|
| SN-01 | C-19 | SN-08 | C-26 |
| SN-02 | C-20 | SN-09 | C-27 |
| SN-03 | C-21 | SN-10 | C-28 |
| SN-04 | C-22 | SN-11 | C-29 |
| SN-05 | C-23 | SN-12 | C-30 |
| SN-06 | C-24 | SN-13 | C-31 |
| SN-07 | C-25 | SN-14 | C-32 |

## 1. 版本与兼容

- **C-19**: 每次输出 MUST 含 `"schema_version": 1`。增量字段只允许追加；读取方 MUST 忽略未知字段。MUST NOT 在同一 `schema_version` 内改变既有字段的类型或语义。 (FR-003)

## 2. 必填顶层字段

- **C-20**: 输出 MUST 含：`schema_version`、`line_id`、`run_id`、`stage`、`loop_state`、`verdict_source`、`loop_state_reason`、`watch_verdict`、`recovery_action`、`recovery_reason`、`recovery_decision`、`false_completion`、`spine`、`registry`、`paths`、`thresholds`、`evidence`、`interruptions`、`missing_artifacts`、`uncommitted_artifacts`、`stale_signals`、`evaluated_at`。`recovery_decision` MUST 含 `action`、`reason`、`preconditions[]`、`blocked_by[]`，且 `action`/`reason` MUST 与顶层 `recovery_action`/`recovery_reason` 相等。一致性字段 MUST 为嵌套 `spine.consistent`；MUST NOT 输出顶层 `spine_consistent` 别名。 (FR-003, FR-004)

## 3. 状态与值

- **C-21**: 每个信号 MUST 含 `status ∈ {present, missing, na}` 与 `value_state ∈ {known, unknown, na}`：

  | 情形 | `status` | `value_state` | 值 |
  |------|----------|---------------|-----|
  | 源存在且值可判 | `present` | `known` | 实际值 |
  | 源存在但值不可判（legacy 缺字段/不可解析/阶段未知） | `present` | `unknown` | `null` |
  | 源不存在或不可读 | `missing` | `na` | `null` |
  | 对本阶段/本次尝试不适用（含 never-dispatched 的四件套/watchbeat/artifacts/commits） | `na` | `na` | `null` |

  (FR-003, SC-002)
- **C-22**: 缺失值 MUST 用 `null`；MUST NOT 用 `0`、`""`、`"ok"`、`"none"` 或默认阈值代替。`unknown` 是值级标记（`value_state`），MUST NOT 被塞进 `status` 枚举。 (FR-003, SC-002)

## 4. 状态脊与 Registry

- **C-23**: `spine` MUST 含 `path`、`status`、`schema ∈ {v1, legacy, missing}`、`state`、`state_value_state`、`consistent`、`fields`、`missing_fields`。legacy 脊 MUST 被识别为 `schema=legacy` 并降级求值；缺字段记 `unknown`，MUST NOT 猜测或用默认值补齐（A-11/A-18 的读取侧）。`consistent` 的判据见 `interruption-and-action.md` C-39（summary only；owner 为 C-39，其上游规则在 `requirements.md` FR-004）。 (FR-003, FR-004)
- **C-24**: `registry` MUST 含 `status`、`path`、`state`、`stage`、`run_id`、`spine_path`。Registry 缺失时 `status=missing` 且求值继续（`C-5`）；Registry 字段语义与 ownership 归 Feature 064，本切片只读消费。 (FR-003, FR-039, FR-052)

## 5. 监听判定

- **C-25**: `watch_verdict` MUST 为对象，含 `present`、`status`、`value_state`、`verdict`、`reason`、`exit_code`、`attribution`、`detail`，且 MUST 满足三态：

  | 状态 | `present` | `status` | `value_state` | `verdict` | `reason` | `attribution` |
  |------|-----------|----------|---------------|-----------|----------|---------------|
  | 取得判定 | `true` | `present` | `known` | watcher 字面量 | watcher 的 reason 或 `null` | watcher 输出的 `attribution` 字面量 |
  | watcher 不可用 | `false` | `missing` | `na` | `null` | `unavailable` | `null` |
  | 无活动 target | `false` | `na` | `na` | `null` | `null` | `null` |

  `exit_code` MUST 只为 watcher 的判定码（`0` 或非零判定码，owner：`watch-target.sh --help`）；usage 与调用失败 MUST 记 `exit_code=null` 并走“不可用”。`detail` 的取值域见 `C-15`（`LS-15`）。 (FR-005, SC-002)
- **C-26**: `verdict_source` 与 `watch_verdict.present` 的对应关系、以及 watcher 来源下 `loop_state` 与 `watch_verdict.verdict` 的逐字相等约束，MUST 按 `requirements.md` FR-004 执行；该不变量只在 FR-004 定义一次，本条不重复其规则内容。 (FR-004, FR-005)

## 6. 证据块

- **C-27**: `evidence` MUST 含 `evidence_source ∈ {local, probe}` 以及 `pid`、`status`、`log`、`heartbeat`、`watchbeat`、`hook`、`artifacts`、`commits` 八个键。`evidence_source=probe` 时所有证据来自 `--probe` 文件，MUST NOT 混入本地读取。`watchbeat` 是驱动者写入标记的只读投影（写入义务归 065b），其 `status`/`value_state` 同样遵守 `C-21`。 (FR-002, FR-003, FR-010)
- **C-28**: `artifacts` MUST 含 `stage`、`complete`、`commit_required`、`no_change_allowed`、`items[]`；`commits` MUST 含 `base`、`pathspec[]`、`commits[]`、`touching`。`commit_required=false` 时 `commits.status=na`。`artifacts.complete` 的 completeness 判据与 `提交齐备` 谓词见 `interruption-and-action.md` C-46（`IA-14`）与 `stage-artifact-map.md` C-53/C-54/C-57/C-60。 (FR-006, FR-008)
- **C-29**: `interruptions[]` 条目 MUST 含 `form`、`detail`、`evidence[]`、`detector`；`evidence[]` 至少一项。`stale_signals[]` 条目 MUST 含 `signal`、`path`、`reason`、`run_id`、`at`、`mtime_ns`。`missing_artifacts` 与 `uncommitted_artifacts` MUST 为路径字符串数组。 (FR-009, SC-002)

## 7. 判定与动作

- **C-30**: `loop_state` MUST 取自封闭集 `RUNNING / DONE / INCOMPLETE / ANOMALY / FAILED / DEAD / TIMEOUT / NO_SIGNAL / STALLED / REENTRY_REQUIRED / UNKNOWN`；`recovery_action` MUST 取自 `none / watch / verify / resume / retry / stop`。优先级与门见 `interruption-and-action.md`；`recovery_decision` 与顶层动作字段 MUST 一致。 (FR-004, FR-009)
- **C-31**: `false_completion=true` 当且仅当哨兵存在（按 `requirements.md` FR-004，哨兵 = 日志最后非空行 `== <STAGE>-DONE`）且任一必需产物缺失或为空；此时 `recovery_action` 按 `IA-14`（C-46）求值：`STALLED`/`REENTRY_REQUIRED` 为 `stop`（行 11），其余为 `retry`，除非 `IA-04` 证据缺口短路或 `IA-15` 尝试上限改为 `stop`；MUST NOT 建议 `resume`。`false_completion` 与 `artifacts-without-completion` 是互斥的两侧（见 `IA-10`），MUST NOT 同时为真。 (FR-007, FR-051)
- **C-32**: 相同输入两次运行，除 `evaluated_at` 外所有字段 MUST 逐字相等。输出 MUST NOT 包含 `age_seconds`、剩余时间或其他随调用时刻变化的派生数值；只输出原始 `at`/`mtime_ns` 与布尔判定。`evaluated_at` MUST 为 ISO-8601 UTC。 (FR-001, SC-002)

## 8. 规范示例

下列示例省略 `thresholds` 的数值成员（数值由 `watch-target.sh` 拥有，本契约不复述）；其余字段为实际形状。

```json
{
  "schema_version": 1,
  "line_id": "demo-line",
  "run_id": "run-0001",
  "stage": "plan",
  "loop_state": "RUNNING",
  "verdict_source": "derived",
  "loop_state_reason": "running",
  "watch_verdict": {
    "present": false,
    "status": "missing",
    "value_state": "na",
    "verdict": null,
    "reason": "unavailable",
    "exit_code": null,
    "attribution": null,
    "detail": "script-missing"
  },
  "recovery_action": "watch",
  "recovery_reason": "unwatched",
  "recovery_decision": {
    "action": "watch",
    "reason": "unwatched",
    "preconditions": ["stage running", "no terminal evidence"],
    "blocked_by": []
  },
  "false_completion": false,
  "spine": {
    "path": "/state/demo-line/spine.md",
    "status": "present",
    "schema": "v1",
    "state": "running",
    "state_value_state": "known",
    "consistent": null,
    "fields": {
      "stage_started_at": 1790000000,
      "stage_deadline_epoch": 1790005400,
      "stage_base_commit": "abc1234",
      "attempt": 1,
      "last_verdict": null,
      "salvage": null,
      "salvage_evidence": null,
      "salvage_at": null,
      "pid_path": "/state/demo-line/pid-demo-line-plan",
      "status_path": "/state/demo-line/status-demo-line-plan",
      "log_path": "/state/demo-line/log-demo-line-plan.log",
      "heartbeat_path": "/state/demo-line/heartbeat-demo-line-plan.log"
    },
    "missing_fields": []
  },
  "registry": {
    "status": "present",
    "path": "/registry/demo-line.json",
    "state": "active",
    "stage": "plan",
    "run_id": "run-0001",
    "spine_path": "/state/demo-line/spine.md"
  },
  "paths": {
    "state_dir": "/state/demo-line",
    "spec_dir": "/repo/.specify/specs/demo",
    "repo": "/repo",
    "spine": "/state/demo-line/spine.md",
    "probe": null
  },
  "thresholds": {
    "source": "watch-target-help",
    "value_state": "known"
  },
  "evidence": {
    "evidence_source": "local",
    "pid": {
      "status": "present",
      "value_state": "known",
      "path": "/state/demo-line/pid-demo-line-plan",
      "pid": 4242,
      "start": "123456",
      "at": 1790000001,
      "alive": true,
      "identity": "ok",
      "attribution": "legacy"
    },
    "status": {
      "status": "missing",
      "value_state": "na",
      "path": "/state/demo-line/status-demo-line-plan",
      "exit_code": null,
      "at": null,
      "sentinel": null,
      "run_id": null,
      "stage": null,
      "event": null,
      "legacy": null,
      "attribution": null
    },
    "log": {
      "status": "present",
      "value_state": "known",
      "path": "/state/demo-line/log-demo-line-plan.log",
      "last_line": "working",
      "sentinel_present": false,
      "sentinel": "PLAN-DONE",
      "anomaly": false
    },
    "heartbeat": {
      "status": "present",
      "value_state": "known",
      "path": "/state/demo-line/heartbeat-demo-line-plan.log",
      "at": 1790000100,
      "mtime_ns": 1790000100000000000,
      "fresh": true,
      "attribution": "legacy"
    },
    "watchbeat": {
      "status": "missing",
      "value_state": "na",
      "path": "/state/demo-line/watchbeat-demo-line-plan",
      "run_id": null,
      "stage": null,
      "window": null,
      "at": null,
      "event": null,
      "fresh": null
    },
    "hook": {
      "status": "na",
      "value_state": "na",
      "path": null,
      "observed_at": null
    },
    "artifacts": {
      "status": "present",
      "value_state": "known",
      "stage": "plan",
      "complete": false,
      "commit_required": true,
      "no_change_allowed": false,
      "items": [
        {"path": "plan.md", "required": true, "status": "present", "size": 2048},
        {"path": "data-model.md", "required": true, "status": "missing", "size": 0},
        {"path": "contracts/", "required": true, "status": "missing", "size": 0},
        {"path": "quickstart.md", "required": true, "status": "present", "size": 1024},
        {"path": "feature-ref.md", "required": true, "status": "present", "size": 512}
      ]
    },
    "commits": {
      "status": "present",
      "value_state": "known",
      "base": "abc1234",
      "pathspec": [
        ".specify/specs/demo/plan.md",
        ".specify/specs/demo/data-model.md",
        ".specify/specs/demo/contracts/",
        ".specify/specs/demo/quickstart.md",
        ".specify/specs/demo/feature-ref.md",
        ".specify/specs/demo/research.md"
      ],
      "commits": [],
      "touching": false
    }
  },
  "interruptions": [
    {
      "form": "unwatched",
      "detail": "stage is running and no fresh watchbeat marker exists",
      "evidence": [
        {"signal": "watchbeat", "path": "/state/demo-line/watchbeat-demo-line-plan"},
        {"signal": "heartbeat", "path": "/state/demo-line/heartbeat-demo-line-plan.log"}
      ],
      "detector": "065a"
    }
  ],
  "missing_artifacts": ["data-model.md", "contracts/"],
  "uncommitted_artifacts": ["plan.md", "quickstart.md", "feature-ref.md"],
  "stale_signals": [],
  "evaluated_at": "2026-10-21T10:00:00Z"
}
```

示例中的 `consistent=null` 表示状态脊没有 `last_verdict`，一致性不可判；`plan.md` 已存在但基线之后没有触及它的提交，因此进入 `uncommitted_artifacts`。
