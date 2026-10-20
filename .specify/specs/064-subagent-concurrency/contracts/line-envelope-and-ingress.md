# Contract: Line Envelope & Message Ingress（归属信封与消息入口）

**Feature**: 064
**Owning FR**: FR-008…FR-017
**实体**: `data-model.md` § E2；决策 `research.md` § R2–R3
**Implementation surface**: `skills/external/sdd-loop-driver/scripts/line-registry.py`（`resolve-message`/`verify-identity`/`classify-remote`）+ `skills/external/sdd-loop-driver/scripts/watch-target.sh`（归属过滤）+ `references/stage-prompts.md`（入口程序）+ `references/watch-model.md`（归属层引用）

## A. Envelope

- **EN-01（信封字段）**: 每个阶段 prompt、status、log、heartbeat、哨兵承载记录、watcher 输出与 monitor 事件 MUST 携带 `line_id`、`run_id`、`stage`、`event`、`at`（`at` 为 epoch seconds；Registry 中其他时间字段仍为 ISO-8601 UTC）；终止事件另带 `sentinel_seen`/`exit`（FR-008, V-EN）。
- **EN-02（载体与命名）**: 信封 MUST 采用 JSON 旁路：status/pid/heartbeat 在既有 key=value 行尾追加字段；日志旁路 `log-<line>-<stage>.log.meta.jsonl`（append-only，单写者）；提示词旁路 `prompt-<line>-<stage>.md.meta.json`；watcher 输出追加 `line=`/`run=`/`attribution=`。MUST NOT 写入日志正文（FR-008）。
- **EN-03（哨兵保全）**: 通用哨兵字面量（大写阶段名 + `-DONE`）与「日志最后非空行」判定 MUST 保持不变；归属 MUST NOT 通过改写哨兵、位移最后一行或在其后追加信封实现（FR-009）。
- **EN-04（分类）**: 归属键 `(line_id, run_id)`；`line_id` 不同 → `foreign`；`line_id` 相同 `run_id` 不同 → `stale-run`；缺失/不可解析 → `unattributed`；watcher 未提供归属参数 → `legacy`（058 兼容）（FR-014, FR-015, V-EN-2）。
- **EN-05（消费规则）**: 只有 `own` 事件可参与判定、进度与 Registry 状态。`foreign`/`stale-run`/`unattributed` MAY 出现在 watcher 摘要或线日志，MUST NOT 被消费、转发、计入进度或改变状态（FR-014, FR-015, SC-003）。
- **EN-06（Watcher 接口）**: `watch-target.sh` 新增可选 `--line-id`、`--run-id`、`--meta`。提供两者时执行归属过滤；输出行追加 `line=`/`run=`/`stage=`/`event=watcher-verdict`/`at=`/`attribution=`；判定状态机、退出码、窗口/deadline 语义 MUST 零改动（FR-013, FR-063）。
- **EN-07（PID 身份）**: watcher/monitor MUST 只消费 Registry 中登记且身份校验通过的 PID（start token；cwd/branch 在可用时）。归属判定 MUST NOT 使用宽泛 `ps`/`pgrep`、进程名匹配或当前 shell 状态；对单个登记 PID 的定向探询（`ps -p <registered-pid>`）不属宽泛扫描（FR-013, V-LR-7）。

## B. Message Ingress

- **EN-08（活动线定义）**: 活动线 = `state ∈ {active, waiting}`；入口判定只读取 Registry 摘要（FR-010）。
- **EN-09（可识别标识）**: 可识别标识为显式 `line_id` token，或唯一匹配的 `project_dir`/`repo_root`/分支名；`line_id` 匹配按单词边界，路径按归一化后的相等/包含匹配（FR-010）。
- **EN-10（恰好一次澄清）**: 活动线 >1 且消息无可识别标识（或匹配不唯一）时，驱动 MUST 对每条此类消息提出**恰好一个**澄清问题并列出候选活动线（`line_id`、项目、分支、阶段、状态）。MUST NOT 基于 `ps`/`pgrep`/进程名/cwd/环境态推断（FR-010, SC-002）。
- **EN-11（回答后停止规则）**: 用户回答仍无法唯一匹配时，MUST 显式报告候选并停止路由；MUST NOT 追加第二个问题，也不得猜测（`resolve-message --clarified` → `ambiguous-stop`）（FR-010）。
- **EN-12（单线/零线）**: 恰好 1 条活动线且无标识 → 直接路由；0 条 → 明确报告无活动线路并请求目标；匹配到非活动/不存在线路 → 报告候选并停止，不回落到猜测（FR-011）。
- **EN-13（不阻塞他线）**: 一次入口澄清 MUST NOT 停止/暂停/改变其他 line 的子代理与监听；等待回答只阻塞该条消息的路由（FR-012）。
- **EN-14（零进程扫描）**: `resolve-message` 及其调用链 MUST NOT 执行 `ps`/`pgrep`/`pidof`/进程名枚举；契约测试以 PATH 桩计数与源码扫描双重验证（FR-010, SC-002）。
- **EN-15（双线验收）**: 同环境双线、相同通用哨兵、相同 CLI 命令名下：跨线归属错误 0；每条无标识消息澄清数 1；foreign monitor 事件改变当前状态 0 次；PID 复用/死亡不产生假完成（FR-016, SC-001/SC-003, SC-008）。
- **EN-16（单线信封与兼容）**: 单线运行 MUST 同样注册并携带信封；watcher 提供归属参数时即使只有一条线也执行归属过滤。`legacy` 仅用于单活动线 / 058 兼容调用（未提供归属参数）；多活动线 MUST NOT 以 legacy 调用绕过归属过滤。单线的 U0–U6、阶段链、哨兵校验、watcher 判定与退出码 MUST 与 058 基线一致（FR-017, FR-068）。

## Watcher 输出示例（own / foreign）

```text
WATCH label=L1 verdict=RUNNING pid=alive heartbeat=ok anomaly=no sentinel=no rc=na elapsed=12 reason=alive line=<line_id> run=<run_id> attribution=own
WATCH label=L1 verdict=RUNNING pid=alive heartbeat=ok anomaly=no sentinel=no rc=na elapsed=12 reason=alive line=<other_line_id> run=<other_run_id> attribution=foreign
```

第一行可参与判定；第二行只作摘要，不改变 verdict 或状态。

## Engine Actions

接口清单的唯一 owner 是 `contracts/line-registry.md` § Engine Actions；本契约使用其中 `resolve-message`、`verify-identity`、`classify-remote` 三个动作。`clarify` 输出的 `question` 是**唯一**问题文本（含候选清单），驱动不得自增第二个问题。

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| EN-01…EN-04 | FR-008, FR-009, FR-014 | `test_line_envelope_contract.py::test_en_01_fields`, `test_en_02_carriers`, `test_en_03_sentinel_untouched`, `test_en_04_classification` |
| EN-05/EN-06/EN-07 | FR-013…FR-015, FR-063, SC-003 | `test_en_05_foreign_not_consumed`, `test_en_06_watcher_flags_and_exit_codes`, `test_en_07_targeted_pid_only` |
| EN-08…EN-14 | FR-010…FR-012, SC-002 | `test_en_10_exactly_one_clarification`, `test_en_11_ambiguous_stop`, `test_en_12_single_zero_active`, `test_en_13_clarification_non_blocking`, `test_en_14_no_process_scan` |
| EN-15 | FR-016, SC-001/SC-003/SC-008 | `tests/integration/test_two_line_isolation.py` |
| EN-16 | FR-017, FR-068 | `test_en_16_single_line_envelope_compat` |
