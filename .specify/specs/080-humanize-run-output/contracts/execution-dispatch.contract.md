# Contract: 指令执行与派发（execution-dispatch）

**Feature**: 062 扩展 | **规格**: `.specify/specs/080-humanize-run-output/requirements.md`
**性质**: 行为契约。判定派发载体、载荷、回传、失败与降级。
**覆盖**: 见文末可追溯性表。
**外部所有者**: `run-agent` 技能的 Run Mode 是本契约的**载体所有者**（载体的步骤、拓扑声明与
快速失败注入子句都在它那里）；本文件只固定 humanize 侧必须满足的部分，MUST NOT 复制 carrier 的
步骤表。快速失败子句的拥有者字面量在 `shared/guidelines/fast-fail.md` § 子代理派发注入。

---

## 派发

- **EX-01**: 运行模式每次调用 MUST 派发**恰好一个**顶层执行体；一次调用两次派发、或「先试一个再补一个」都判违反（FR-007）。
- **EX-02**: 派发 MUST 经既有 `run-agent` 载体（Run Mode），MUST NOT 引入第二套派发机制、MUST NOT 新建派发脚本、MUST NOT 直接调用某宿主的私有会话 API（FR-007, A5）。
- **EX-03**: 派发的执行体是**会话级临时执行体**：不写入 `.specify/agents/`，不产生 `.agent.md`，不占用既有 Agent 席位。它的任务简报就是指令原文，因此 run-agent 的「按名解析已存 Agent」分支不适用于本次派发；MUST NOT 因此在磁盘上创建一个只为本次运行存在的 Agent 定义（FR-007, 宪法 IX）。本次派发**不声明 SDD 执行席位**：run-agent 的席位授权探针服务于 SDD 阶段派发，对不声明席位的传输型派发不适用；若指令本身要启动一次 SDD 运行，那次运行的授权仍由指令所属单元自己的入口判定——humanize MUST NOT 代替它判定，也 MUST NOT 以「只是一次传输」为由跳过它（FR-007, FR-008）。
- **EX-04**: 载体 MUST 按宿主能力选择模式：具备原生派发通道 → `native`；不具备 → `in-session`。`run-agent` 的第三种模式（独立 CLI 进程）MUST NOT 被本命令使用——它会带来进程、凭据与网络面，超出「不新增运行时」（FR-011, 宪法 IX）。
- **EX-05**: 载体标记 MUST 与真实载体一致：`native` → `mode: subagent`（`[[STR-006]]`）；`in-session` → `mode: in-session-degraded`（`[[STR-007]]`）。MUST NOT 冒充、MUST NOT 两个都写、MUST NOT 都不写（FR-011）。

## 派发载荷（必须携带的六项）

- **EX-06**: 派发载荷 MUST 按顺序携带：①快速失败注入子句（拥有者字面量，逐字节相等，置于载荷开头独立段落）；②指令原文（逐字）；③回传信封的字段与封闭取值（`data-model.md` § E5）；④「不得撰写最终报告」；⑤「不得重试、不得代替用户答复确认」；⑥「指令自身再调用本命令即拒绝并回传」（FR-007, FR-009, FR-010, FR-030）。
- **EX-07**: 载荷 MUST NOT 把指令改写成步骤清单、MUST NOT 预先替指令挑选实现路径、MUST NOT 把 humanize 的报告要求当作指令的执行目标（FR-013）。
- **EX-08**: 载荷 MUST 声明指令自身的确认步骤与权限边界优先：执行体遇需确认且无法取得答复时停在该步（FR-008, FR-013）。

## 回传与判定

- **EX-09**: 回传 MUST 是 `data-model.md` § E5 的信封；MUST NOT 以「写了报告文件」代替回传（零写入，A9）。
- **EX-10**: 信封缺显式异常行时 MUST 判为不完整：其结论 MUST NOT 被消费，报告 `## Conclusion` 记失败/不完整并点名缺失项（快速失败纪律；FR-012）。这是硬判定，不是风格建议。
- **EX-11**: 载荷发出后才发现缺快速失败子句 → MUST 停止消费该次结果并按失败报告；MUST NOT 以「补发一次」修复（重试禁令，FR-010）。
- **EX-12**: 派发失败、超时或执行体中止时 MUST 记录失败坐标（载体、阶段、错误信息）与已完成部分；MUST NOT 自动重试、MUST NOT 改写为成功（FR-010, FR-012）。
- **EX-13**: 指令被用户中止时 MUST 记录中止点与已完成部分，报告口径为「已中止」（Edge Cases；FR-012）。
- **EX-14**: 执行体回传的 `products` 与 `evidence` MUST 逐项核对可定位性（路径存在、命令与退出码自洽、读数可复核）；核对不上的项 MUST NOT 作为证据写进报告，MUST 在 `## Risks & Limits` 记为「未能核实」（FR-009, FR-020）。

## 确认缺失（fail-closed）

- **EX-15**: 指令执行到需要用户确认的步骤而执行体无法询问用户时，MUST 不执行该步：`blocked_at` 记卡点，`## Conclusion` 写「需要确认，未获答复」，其余已完成部分照常报告（FR-008，clarify 裁决）。
- **EX-16**: humanize 主会话 MUST NOT 代替用户回答该确认、MUST NOT 以「用户可能同意」继续、MUST NOT 换个等价动作绕开该步（FR-008, A8）。

## 降级

- **EX-17**: 降级为会话内执行时 MUST 声明降级并只把**可观察的结果**当事实；MUST NOT 把推断描述为子代理的观测，MUST NOT 声称有独立上下文或独立工具集（FR-011）。
- **EX-18**: 降级 MUST NOT 改变报告五节、证据义务或保真底线；降级只改载体标记与该载体带来的限制描述（FR-011, FR-018）。

## 边界

- **EX-19**: humanize 自身 MUST NOT 发起网络请求、MUST NOT 调用外部服务或模型 API；指令自身按其契约产生的联网行为 MUST 在 `## Evidence` / `## Key Changes` 披露，MUST NOT 记作 humanize 的外发（FR-010, SC-007）。
- **EX-20**: 退出路径（成功、失败、中止、异常）MUST 全部释放占位（`data-model.md` § E4）；占位残留即判违反（FR-030, 零写入）。
- **EX-21**: 派发记录 MUST 是 `[[STR-003]]` 内一行元数据，键名 `[[STR-011]]`（字面量 owner = requirements § Shared Strings）；本条款是**计数口径的唯一 owner**：只计 humanize 发起的顶层派发（原生 `1` / 降级 `0`），指令自身再发起的派发归该指令单元，MUST NOT 重复计数（FR-007）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| EX-01 | FR-007 | `test_ex01_exactly_one_dispatch` |
| EX-02 | FR-007 | `test_ex02_run_agent_carrier_only` |
| EX-03 | FR-007 | `test_ex03_temporary_executor_no_agent_file` |
| EX-04 | FR-011 | `test_ex04_carrier_modes` |
| EX-05 | FR-011 | `test_ex05_marker_matches_carrier` |
| EX-06 | FR-007, FR-009, FR-010, FR-030 | `test_ex06_payload_six_items` |
| EX-07 | FR-013 | `test_ex07_payload_keeps_instruction_verbatim` |
| EX-08 | FR-008, FR-013 | `test_ex08_payload_defers_to_instruction_gates` |
| EX-09 | FR-009 | `test_ex09_envelope_is_message` |
| EX-10 | FR-012 | `test_ex10_missing_anomaly_line_blocks_consumption` |
| EX-11 | FR-010 | `test_ex11_no_compensating_redispatch` |
| EX-12 | FR-010, FR-012 | `test_ex12_failure_coordinates_no_retry` |
| EX-13 | FR-012 | `test_ex13_aborted_reported_as_aborted` |
| EX-14 | FR-009, FR-020 | `test_ex14_evidence_locatability_check` |
| EX-15 | FR-008 | `test_ex15_confirmation_missing_fail_closed` |
| EX-16 | FR-008 | `test_ex16_no_proxy_answer` |
| EX-17 | FR-011 | `test_ex17_degraded_honesty` |
| EX-18 | FR-011, FR-018 | `test_ex18_degraded_keeps_report_contract` |
| EX-19 | FR-010, SC-007 | `test_ex19_no_network_from_humanize` |
| EX-20 | FR-030 | `test_ex20_reservation_released_all_paths` |
| EX-21 | FR-007 | `test_ex21_dispatch_record_line` |
