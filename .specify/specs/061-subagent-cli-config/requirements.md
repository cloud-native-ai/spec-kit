# Requirements Specification: 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification）

**Requirement Branch**: `061-subagent-cli-config`  
**Created**: 2026-10-18  
**Status**: Draft  
**Input**: User description: "依据 /tmp/061-subagent-cli-config-brief.md 创建 Feature 061「子代理 CLI 配置管理与按派发量化」的 requirements"

## Related Feature *(mandatory)*

**Feature ID**: 061  
**Feature Name**: 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification）

## 现状锚点（2026-10-18 以源码实测为准；dated record，仅作可行性输入，非运行时保证）

- `.specify/agents/execution/configs/` 目录存在但为空；`_defaults.yaml` 与 `templates/execution-config-defaults.yaml` 均不存在。
- [[STR-003]] 当前为 `schema_version = 1`，动作集为 `collect / list-records / score`，`unit_type` 取值为 `command / skill / custom-unit`，provenance 取值为 `measured / carried / user-given`；`collect_llm()` 只在宿主为 qodercli 时读取 `~/.qoder/settings.json`，其余宿主直接返回未采标记。
- [[STR-004]] 的 external 派发引用 [[STR-009]]；后者已支持 `[-- <extra cli args>]` 参数透传形态，本特性只做接线，不新建派发器。
- [[STR-005]] 的 ④ 项当前按宿主 CLI 配置面核验 model/context/effort，尚未校验「已解析配置」。
- [[STR-011]] 当前未记载 `--reasoning-effort` / `--context-window` 等已验证旗标。
- [[STR-006]] 当前字段表仅含 `agent / mode / cli / model / reasoning_effort / context_window / extra_flags / log_dir`，无分层、默认层、量化方法与快照语义。
- Feature 059（exec-quant）与 Feature 060（decompose-subagent-dispatch）在 `.specify/memory/features.md` 均为 Implemented；本特性不改变其状态。

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **Feature 绑定已落定（Clarifications Session 2026-10-18）**：新建 Feature 061「子代理 CLI 配置管理与按派发量化」；060/059 保持 Implemented 不变。
- 解析引擎名称已锁定为 [[STR-002]] `scripts/python/execution-config.py`（stdlib-only，三动作 `resolve / validate / list-configs`）；plan 不得改名，若确需改名须走范围修订并同步 [[STR-002]]。全仓同名冲突实测为零（2026-10-18）。
- [[STR-015]] 在配置快照 `config_id` 与本次解析结果不一致时，按**非阻塞且可见**的失败处理：输出失败原因并以非零退出报告、不写入声称该配置的记录、不阻塞派发结果；存储保持 append-only。
- `quantification.method` 未声明或声明为 `auto` 时走 auto 解析；「显式覆盖」只统计代理层与内联层中显式设置且未被清除哨兵（`""` / `auto`）清空的 `model / reasoning_effort / context_window / extra_flags / log_dir` 任一字段，默认层与 `quantification.method` 键本身不计入。
- 真实 qodercli 端到端派发属**可选验证**，需显式授权；未授权时以生成的 `cli_args` 与确定性引擎测试满足验收。
- 「默认层整体跳过」适用于代理层或内联层选择了非 qodercli 的全部情形；跳过时默认层的全部键（`mode / model / reasoning_effort / context_window / extra_flags / quantification.method / log_dir / cli`）一律不参与合并，`skipped_layers` MUST 记录该层被跳过。
- 本特性不新增 CLI 适配器，也不接线 create-team / run-team。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 配置分层解析与 CLI 能力矩阵 (Priority: P1)

编排者为一个子代理声明 CLI 配置——默认层、代理配置文件与内联派发参数可以同时存在。派发前，确定性解析引擎按固定优先级合并三层配置、按所选 CLI 的能力矩阵校验每一项，并产出可复现的 effective config、`config_id`、逐字段来源链、CLI 参数、是否需要 external 以及配置快照。冲突与未验证组合被拒收并点名到字段，绝不静默丢弃。

**Why this priority**: 这是「配置写了不生效」的直接修复面，也是按派发量化的前提——没有确定的 effective config 与 `config_id`，记录无法说明「这次派发到底用了什么配置」。

**Independent Test**: 仅实现本故事即可用夹具配置直接调用解析引擎，断言合并结果、来源链、`config_id`、`cli_args` 与拒收行为；不依赖任何真实派发。

**Acceptance Scenarios**:

1. **Given** 项目只有默认层（夹具默认层声明 `mode: external` 与 `cli: qodercli`）且选择 qodercli, **When** 执行 resolve, **Then** `cli_args` 恰为 [[STR-013]]，`config_id` 在重复运行间保持稳定，`source_chain` 对 effective config 的每个非 null 字段与 `quantification.method` 说明取值来自默认层。
2. **Given** 代理配置覆盖 model、内联参数覆盖 reasoning_effort, **When** 执行 resolve, **Then** effective config 同时体现两层取值，`source_chain` 按字段区分来源，且 `config_id` 与仅默认层时不同。
3. **Given** 低层已设置某覆盖字段, **When** 代理层或内联层显式给出空串（`""`）或 `auto`, **Then** 该字段在 effective config 中为 `null`（8 键仍在位），不生成任何 CLI 旗标，也不进入 `source_chain`。
4. **Given** 代理配置声明 `cli: claude` 而内联声明 `cli: qodercli`, **When** 执行 resolve, **Then** 解析期拒收并列出 `cli` 为冲突字段；显式 `mode: native|virtual` 且存在覆盖字段时同样拒收并提示改用 external；显式 `cli` 与生效 `native|virtual` 同时出现、或 `mode: external` 但无生效 `cli` 时同样拒收。
5. **Given** 选择 claude 且显式给出 model/effort/context 任一值, **When** 执行 resolve, **Then** 以 exit 2 拒收并列出「字段 + 支持集」；codex/opencode 的 external 派发与未知 CLI 同样拒收。
6. **Given** 默认层文件缺失, **When** 执行 resolve, **Then** 快速失败，输出缺失路径与 `specify init` 修复方式，不加载任何内置默认值。

---

### User Story 2 - 每次派发一条量化记录 (Priority: P1)

编排者经 run-agent 完成一次 **external 派发**后，系统为本次派发落一条身份为 `agent:<slug>` 的量化记录：`run_id` 即派发 label，记录同时包含本次生效的配置组、量化方法（声明 vs 实测）与质量字段（退出码、耗时、可测的 token）。native/virtual 派发没有派发三元组，不落 agent 记录。同一派发重复采集不产生第二行；记录可按单元类型与 `config_id` 查询并补打分。

**Why this priority**: 这是本特性的核心收益——把量化粒度从「与运行判定同语义的单元」下沉到「每次派发」，并让不同配置可以被区分与比较。

**Independent Test**: 仅实现本故事即可用夹具派发产物（jsonl/status/快照）调用 [[STR-015]] 并查询记录；不依赖真实外部 CLI 执行。

**Acceptance Scenarios**:

1. **Given** 一次 qodercli external 派发且无显式覆盖, **When** 派发返回后执行 [[STR-015]], **Then** 记录 `method_resolved=qoder-settings`，`config` 组恰含 11 个字段 `config_id / source_chain / method_requested / method_resolved / mode / cli / model / reasoning_effort / context_window / extra_flags / snapshot`，`llm` 组取自 qoder settings 并标注 measured。
2. **Given** 代理层显式覆盖 model/effort/context 三项, **When** 执行同一派发, **Then** `method_resolved=declared`，`llm` 组回显配置值并标注 configured。
3. **Given** 解析结果为 `method_resolved=none`, **When** 采集, **Then** `llm` 组全部为显式未采标记，记录仍完整落库。
4. **Given** 同一 `(agent:<slug>, 派发 label)` 已被采集, **When** 再次调用 [[STR-015]], **Then** 不写入第二行，存储保持 append-only。
5. **Given** status 文件记录了退出码, **When** 采集, **Then** `quality.exit_code` 落值：exit 0 时 `errors=[]`，非 0 时恰有一条 `dispatch.exit_code`；无 status 文件时相关叶子为显式未采标记。
6. **Given** 已有多条 agent 记录, **When** 执行 `list-records --unit-type agent --config-id <id>`, **Then** 只返回匹配记录，且 `score` 可对 agent 记录追加用户打分。

---

### User Story 3 - 派发接线、schema 真源扩展与默认值播种 (Priority: P2)

run-agent 在派发前解析并展示配置、external 派发把 `cli_args` 透传给 dispatch.sh、派发后非阻塞地采集记录；preflight ④ 改为校验「已解析配置」；create-agent 的 execution-config reference 扩为 schema 权威；subagent-definitions 增补三层配置与量化指针；`specify init` 首次播种 `_defaults.yaml` 且永不覆盖；CLI 与 agent 文档补录已验证事实。

**Why this priority**: 没有接线，解析与量化只是离线工具；没有真源扩展与播种，下游项目拿不到可用的默认层。它是前两个故事的落地面，故为 P2。

**Independent Test**: 分别在带/不带既有 `_defaults.yaml` 的临时项目上运行 init，并审计 run-agent / preflight 文本与派发命令形态；不执行真实外部派发。

**Acceptance Scenarios**:

1. **Given** 一次 external 派发, **When** run-agent 执行, **Then** 派发前展示解析结果，命令形态经 [[STR-009]] 以 `-- <cli_args>` 传递旗标，派发返回后调用 [[STR-015]] 且采集失败不影响派发结果；AUTO-GENERATED Wrap-up 段零改动。
2. **Given** preflight ④ 运行, **When** resolve 失败或 `config_id` 缺失, **Then** 前置检查失败并列出待补齐字段；060 C-17 要求的 `model / effort / context` 字面量仍在检查描述中。
3. **Given** 一个尚无 `_defaults.yaml` 的项目, **When** 运行 `specify init`, **Then** 从 [[STR-010]] 播种 [[STR-001]]；再次 init 后该文件逐字节不变（永不覆盖）。
4. **Given** 扩展后的 schema 文档, **When** 审计 [[STR-006]] 与 [[STR-008]], **Then** 分层、量化、默认层、CLI 能力与快照语义各有唯一 owner，其它位置只引用、不复制字段表。
5. **Given** 一个已有代理配置的项目, **When** 执行 `validate` 与 `list-configs`, **Then** 非法配置被逐项拒收，合法配置可被发现与列举。

---

### User Story 4 - 既有机制非回归与生成面一致性 (Priority: P2)

本特性会改动 run-agent、preflight 与 exec-quant，而这些面同时被无人值守的驱动循环用于派发后续阶段。改造后，059 的 unit 级记录、060 的派发契约（冲突拒收、前置检查、注入子句、反嵌套）与既有 probe/action-set/preflight 钉定测试必须零新增失败；有意扩展的断言逐条登记；镜像与生成面相对 2026-10-18 基线零 NEW drift；下游阶段派发前重新读取更新后的派发契约，契约不兼容时按快速失败上送。

**Why this priority**: 驱动循环自身依赖被改造的派发面；没有这条非回归与流程约束，特性会把风险带进后续所有阶段的派发。

**Independent Test**: 对冻结基线做名字级失败名单比对，并运行生成/镜像三连；不需要真实外部派发。

**Acceptance Scenarios**:

1. **Given** 既有 unit 级量化记录, **When** 以新版本 `collect` 采集命令/技能单元, **Then** 记录升级为 v2，`config` 组与 `quality.exit_code` 以显式未采标记出现；`agent:` 单元被 `collect` 拒绝。
2. **Given** v1 旧记录, **When** 执行 list-records 或 score, **Then** 记录以只读归一化形式参与，不被改写。
3. **Given** 实现前冻结的失败节点名单, **When** 运行契约与集成测试, **Then** 排序后的失败 nodeid 名单与基线逐名比对零新增；所有有意扩展项逐条登记。
4. **Given** 受影响模板、命令、技能、`scripts` 与 `shared/definitions` 镜像面, **When** 依次运行 `compile-embeds → regen-command-copies → sync-mirrors`, **Then** 相对 2026-10-18 基线零 NEW drift，无手改生成物。
5. **Given** 用户显式授权, **When** 执行一次极短 qodercli 派发, **Then** 带旗标参数被 CLI 接受，且落一条 agent 派发记录；未授权时本场景不执行，不构成阻塞。

### Edge Cases

- 默认层文件存在但语法非法（tab、列表、未知键、更深嵌套）→ 与缺失同级的快速失败，指明文件与违规行/键。
- 代理配置选择非 qodercli 而未显式写 `cli` → 若默认层 `cli=qodercli` 作为默认值生效则沿用 qoder；一旦代理层或内联层显式声明其它 CLI，默认层整层（全部键，含 `mode` 与 `quantification.method`）跳过并在 `skipped_layers` 记录，禁止 qoder 默认值（含量化方法）泄漏。
- `extra_flags` 含换行或托管旗标（`-m` / `--model` / `--reasoning-effort` / `--context-window`）→ 校验期拒收，不得透传到 CLI。
- `mode=external` 但无生效 `cli` → 校验期拒收并列出 `cli` 与支持集。
- `context_window` 为 0、负数、布尔值或非整数 → 校验期拒收。
- `log_dir` 解析后落在 `.specify/agents/execution/logs` 之外 → 校验期拒收。
- 显式 `declared` 但 effective config 缺任一 model/effort/context → exit 2，不降级为其它方法。
- 代理层或内联层仅以 `extra_flags` / `log_dir` 构成显式覆盖（auto 解析落到 `declared`），但 effective config 缺 model/effort/context → 按 FR-010 exit 2，不降级为 `qoder-settings` / `none`。
- 显式 `qoder-settings` 但宿主不是 qodercli → exit 2。
- auto 解析落到 `none` → 记录照常落库并输出 warning，不阻塞派发。
- 同一 `(unit_id, run_id)` 并发重复采集 → 幂等键保证至多一行（实现需避免竞态写入）。
- 配置快照缺失、不可读或 `config_id` 与本次解析不一致 → 非阻塞可见失败：[[STR-015]] 输出原因并以非零退出报告、不写入声称该配置的记录、不阻塞派发结果；存储保持 append-only。
- stream result 缺 `duration_ms`、status 文件缺失、usage 缺输入或输出 token → 对应叶子落显式未采标记，不臆造。
- 记录序列化超过 64 KiB → 按既有策略截断并标注，不丢失身份字段。
- 记录含凭据型值 → 按既有脱敏模式掩码后再落库。

## Requirements *(mandatory)*

### Functional Requirements

#### 配置分层与解析（US1）

- **FR-001**: 配置覆盖字段集 MUST 恰为 `model / reasoning_effort / context_window / extra_flags / quantification.method / log_dir`；合并优先级 MUST 为默认层 [[STR-001]] < 代理配置 `configs/<slug>.yaml` < 内联派发参数。缺省键 MUST 继承低层值；对五个值字段 `model / reasoning_effort / context_window / extra_flags / log_dir`，显式空串（`""`）或 `auto` MUST 清除低层值，非空值 MUST 覆盖低层值。`quantification.method=auto` 是合法方法值而非清除哨兵。effective config MUST 恒含全部 8 个键；被清除或从未提供的字段值为 `null`，MUST NOT 进入 `source_chain` 或 `cli_args`。
- **FR-002**: `mode` 与 `cli` MUST 作为拓扑身份字段按 060 的声明语义处理，而非普通覆盖字段：内联与代理配置同时声明且不一致时 MUST 在解析期拒收并列出冲突字段；默认层的 `cli` 与 `mode` 只是默认值而非声明——代理或内联选择其它 CLI 时，默认层 MUST 整体跳过，任何 qoder 默认值 MUST NOT 泄漏到 claude/codex 等其它 CLI 的 effective config、`cli_args` 或量化记录。「整体跳过」MUST 覆盖默认层的全部键（`mode / model / reasoning_effort / context_window / extra_flags / quantification.method / log_dir / cli`），并 MUST 在 `skipped_layers` 中记录该层被跳过。显式 `cli` 与生效 `native|virtual` 同时出现 MUST 拒收；`mode=external` 且无生效 `cli` MUST 拒收（消息列出 `cli` 与支持集）。
- **FR-003**: `mode` 枚举 MUST NOT 新增 `auto`；未声明时 MUST 遵循 060 的自动选择（native 优先）。内联层或代理层存在任一覆盖字段（不含默认层）时 `requires_external` MUST 为 true——该覆盖触发的 external MUST 优先于默认层 `mode` 的 `native|virtual`（默认层 `mode` 被覆盖）；显式（代理层或内联层）`mode: native|virtual` 且存在覆盖 MUST 拒收并提示改用 external。
- **FR-004**: 默认层文件 [[STR-001]] 缺失时，解析 MUST 快速失败并指明路径与 `specify init` 修复方式；MUST NOT 内置静默默认值。
- **FR-005**: 配置解析 MUST 由 scripts 层新增的确定性引擎 [[STR-002]] 承担（stdlib-only），提供 `resolve / validate / list-configs` 三个动作；引擎名已锁定，plan 不得改名。YAML 子集 MUST 仅支持注释、`key: value` 与一层 `quantification:` 嵌套，tab、列表、更深嵌套 MUST 被拒绝。
- **FR-006**: `resolve` MUST 输出 effective config、`config_id`（effective 字段 canonical JSON 的 sha256 前 16 位）、`source_chain`、`skipped_layers`、`cli_args`、`requires_external`、配置快照路径，以及 `quantification{requested,resolved}`。
- **FR-007**: `validate` MUST 拒绝未知/重复键、类型不符、枚举外值、非正整数的 `context_window`、不在 `.specify/agents/execution/logs` 内的 `log_dir`、含换行或托管旗标（`-m` / `--model` / `--reasoning-effort` / `--context-window`）的 `extra_flags`。
- **FR-008**: CLI 能力矩阵 MUST 在代码侧拥有唯一 owner（解析引擎内的单一数据表），其它位置只引用：`qodercli` 支持 external 派发与 `--model` / `--reasoning-effort` / `--context-window` 全量旗标，量化方法 `qoder-settings / declared / none`；`claude` 支持 external 派发（受 060 可见性契约约束），model/effort/context 旗标未在仓库验证，显式值 MUST 被拒收，量化 `declared / none`；`codex` / `opencode` 的 external stream-json 未验证，external MUST 被拒收并保留能力扩展点；其它 CLI MUST 被拒收。未验证的参数组合 MUST 以 exit 2 结束并列出「字段 + 支持集」。能力矩阵的方法约束 MUST 只校验 **resolved** 量化方法；`auto` 是请求层选择器，MUST NOT 因不在 `quantification_methods` 列表中被矩阵拒绝。

#### 量化方法（US1 / US2）

- **FR-009**: 量化方法注册集 MUST 恰为 `auto / declared / qoder-settings / none`；未声明或声明 `auto` 时 MUST 按以下顺序解析：external 且存在显式覆盖（代理层或内联层，不含默认层）→ `declared`；external 且无显式覆盖、CLI=qodercli → `qoder-settings`；native/virtual 且宿主为 qodercli → `qoder-settings`；其余 → `none` 并输出 warning。「显式覆盖」MUST 指代理层或内联层显式设置且未被清除哨兵（`""` / `auto`）清空的 `model / reasoning_effort / context_window / extra_flags / log_dir` 任一字段；默认层与 `quantification.method` 键本身 MUST NOT 计入。请求层 `auto` MUST 先按上述顺序解析为 resolved 方法，再接受能力矩阵校验；`auto` 本身不参与矩阵拒绝。
- **FR-010**: `declared`——无论显式请求还是由 auto 解析产生——MUST 要求 effective config 的 model / reasoning_effort / context_window 三项齐全；显式 `qoder-settings` MUST 要求 qoder 宿主；不兼容组合 MUST 以 exit 2 结束，MUST NOT 降级到其它方法。

#### 按派发量化记录（US2）

- **FR-011**: [[STR-003]] MUST 升级到 `schema_version = 2`：provenance 取值集新增 `configured`；`unit_type` 新增 `agent`；`unit_id` MUST 接受 [[STR-014]] 形式的 `agent:<slug>`。
- **FR-012**: [[STR-003]] MUST 新增动作 [[STR-015]]：入参 `unit_id=agent:<slug>`、`run_id=派发 label`（execution_id），使用显式解析；幂等键 MUST 为 `(unit_id, run_id)`，重复调用不得写入第二行；采集前 MUST 从 `snapshot.effective` 重算 canonical `config_id`，并同时与 `snapshot.config_id` 及 `--config-id` 双方一致；同一 `config_id` 的新 resolve MUST 在 collect 完成之后再发起（避免刷新 `resolved_at` 影响 elapsed 回退）。不一致时 MUST 非阻塞失败：输出原因并以非零退出报告、不写入声称该配置的记录、不改变派发结果。本动作 MUST 只覆盖 external 派发；native/virtual 无派发三元组，不落 agent 记录。
- **FR-013**: [[STR-003]] 的记录 MUST 新增 `config` 组，字段恰为 `config_id / source_chain / method_requested / method_resolved / mode / cli / model / reasoning_effort / context_window / extra_flags / snapshot`。
- **FR-014**: `llm` 组 MUST 按 `method_resolved` 取值，叶子集合沿用 059（`model / reasoning_effort / context_window / config_source / endpoint_candidates / connection_evidence`）：`declared` → `model / reasoning_effort / context_window` 回显配置值并以 `configured` 标注，`config_source` 为 `execution-config:<config_id>`（`configured`），`endpoint_candidates / connection_evidence` 为显式未采；`qoder-settings` → 复用既有 qoder settings 适配器并以 `measured` 标注（`config_source` 为 settings 路径 `measured`，`endpoint_candidates / connection_evidence` 为显式未采）；`none` → 六个叶子全部为显式未采标记。
- **FR-015**: `quality` MUST 新增 `exit_code`；`elapsed_ms` MUST 优先取 stream result 的 `duration_ms`，否则取 status 文件 mtime 与快照 `resolved_at` 之差（差值必须非负，否则落显式未采标记），两者皆无时落显式未采标记；`tokens` MUST 仅在 usage 的输入与输出 token 均为整数时取值；exit 0 → `errors=[]`，非 0 → 一条 `dispatch.exit_code`；无 status 文件或 status 行不可解析 → 相关字段落显式未采标记。`quality.satisfaction` 与顶层 `qualification` 对 agent 记录 MUST 为显式未采标记。不确定的 stream 字段形态 MUST 落显式未采，不得臆造。
- **FR-016**: [[STR-003]] 的既有 `collect` 动作 MUST 写 v2 记录：新增 `config` 组与 `quality.exit_code`（单元记录对应叶子为显式未采标记），并 MUST 拒绝 `agent:` 单元。
- **FR-017**: `list-records` MUST 支持 `--unit-type agent` 与 `--config-id` 过滤；v1 旧记录 MUST 以只读归一化方式参与列出与打分；`score` MUST 对 agent 记录可用。
- **FR-018**: 非阻塞语义、append-only 存储、凭据脱敏与 64 KiB 单记录封顶 MUST 保持不变。

#### 派发接线与真源扩展（US3）

- **FR-019**: [[STR-004]] MUST 在派发前 resolve 配置并向用户展示——「披露而非阻断」只指展示环节，`resolve` 非零时 MUST 停止、不得派发；external 派发 MUST 通过 [[STR-009]] 以 `-- <cli_args>` 原样传递旗标，MUST NOT 重排、重引或过滤；`log_dir` MUST 绝对化后再调用派发器（`dispatch.sh` 在 `cd` 前 mkdir）；远端拓扑 MUST 在目标项目侧执行 resolve 与 [[STR-015]]；派发返回后 MUST 调用 [[STR-015]] 落一条记录且采集失败不得影响派发结果；本节只覆盖 external 派发；MUST NOT 改动 AUTO-GENERATED Wrap-up 段。
- **FR-020**: [[STR-005]] 的 ④ 项 MUST 改为校验「已解析配置」（resolve exit 0 且 `config_id` 存在），失败时列出待补齐字段；为兼容 060 C-17，`model / effort / context` 三个字面量 MUST 保留在检查描述中。
- **FR-021**: [[STR-006]] MUST 作为 schema 权威扩格：承载分层与优先级、quantification、默认层与快照语义，并引用 CLI 能力矩阵的代码侧唯一 owner（`CAPABILITY_MATRIX`）而不复制其表格；[[STR-007]] MUST 增加「写后跑 validate」义务；两处 MUST 只引用 owner，不复制矩阵。
- **FR-022**: [[STR-008]] MUST 在拓扑声明中增补三层配置、覆盖与冲突的区分、配置快照与量化方法，并 MUST 引用 schema owner，不得复制字段表。
- **FR-023**: `ensure_agent_layer_dirs` MUST 在 init 时从 [[STR-010]] 播种 [[STR-001]]：文件不存在才复制，MUST NEVER 覆盖既有文件；重复 init MUST 幂等。未显式传入来源时 MUST 使用打包资源 `get_resource_path()/templates/execution-config-defaults.yaml`；显式传入的来源缺失 MUST raise（打包缺陷可见），MUST NOT 静默跳过。
- **FR-024**: [[STR-011]] MUST 补录已验证的 qodercli 旗标；[[STR-012]] MUST 增加配置分层与量化方法的指针。

#### 非回归与流程约束（US4）

- **FR-025**: 059 的既有 unit 级记录行为、060 的派发契约（含冲突拒收、前置检查、注入子句与反嵌套）与 probe/action-set/preflight 钉定测试 MUST 零新增失败；有意扩展的断言 MUST 在 `verification.md` 中逐条登记，MUST NOT 以放宽断言方式通过。
- **FR-026**: 受影响的模板、命令、技能、`scripts` 与 `shared/definitions` 镜像面 MUST 经 `compile-embeds → regen-command-copies → sync-mirrors`，相对 2026-10-18 基线零 NEW drift，MUST NOT 手改生成物。
- **FR-027**: 实现完成后、派发后续阶段之前，MUST 重新读取更新后的派发契约，并记录四个可判定字段：重读面、契约差异、驱动者实际派发路径（本线为直接 runner 还是经 run-agent）、是否影响驱动形态 + 结论；运行时默认层 [[STR-001]] 的存在性 MUST 作为前置证据。若契约变化影响驱动技能的派发形态，MUST 按快速失败上送，MUST NOT 静默适配。

### 显式排除项（Out of Scope）

- create-team / run-team 的配置与量化接线。
- 新增 CLI 适配（qodercli / claude 之外），以及 codex / opencode 的 stream-json 验证与适配。
- 跨 run 聚合、报表、自动打分与任何自动上送。
- native 派发的模型覆盖（本特性只覆盖 external 旗标与量化）。
- 修改 059 / 060 的已实现行为与生命周期状态（两者保持 Implemented）。
- 重定义 Agent 三层分类法或另建平行定义文档；配置语义只在既有真源与 schema owner 内扩展。

### Key Entities *(include if requirement involves data)*

- **Execution Config（分层配置）**: 一个子代理的可派发配置，由默认层、代理配置与内联参数合并而成；关联 Agent Template / Instance、CLI 与拓扑身份（`mode` / `cli`）。
- **Effective Config 与 Config Snapshot**: 解析后的生效配置及其身份（`config_id`、`source_chain`、`skipped_layers`、`resolved_at`）；快照是派发量化记录引用配置的凭据。
- **Defaults Layer（默认层）**: [[STR-001]]，由 [[STR-010]] 播种；提供 model / reasoning_effort / context_window 等默认值，其 `cli` 仅为默认值。
- **CLI Capability Matrix**: 每个受支持 CLI 的派发形态、可接受旗标与可用量化方法；代码侧单一 owner。
- **Quantification Method**: `auto / declared / qoder-settings / none` 及其解析规则；决定记录中 LLM 字段是配置回显还是实测值。
- **Agent Dispatch Record（派发量化记录）**: 一条 `agent:<slug>` 记录，`run_id` 为派发 label；包含配置组、LLM 组、质量组与可选用户打分，身份三元组为 `(unit_id, unit_type, run_id)`。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 仅默认层（夹具默认层声明 `mode: external` 与 `cli: qodercli`）且选择 qodercli 时，`resolve` 输出的 `cli_args` 与 [[STR-013]] 逐字相等；同一输入重复运行得到相同 `config_id`，`source_chain` 覆盖 effective config 的每个非 null 字段与 `quantification.method`——三项均可由引擎输出机械判定。
- **SC-002**: 覆盖的非法/冲突组合（跨层冲突、非 qoder CLI 的显式旗标、codex/opencode external、未知 CLI、external 缺生效 `cli`、非法 YAML、非法 `context_window` / `log_dir` / `extra_flags`、不兼容量化方法）100% 以非零退出并被列出「字段 + 支持集/冲突清单」，零静默丢弃。
- **SC-003**: 一次 external 派发后，专属存储中恰有一条该 `(agent:<slug>, 派发 label)` 记录，`config` 组与 `method_resolved` 齐备，可测的质量字段有值、不可测字段为显式未采标记；同一 label 重复调用 [[STR-015]] 不新增行；`list-records --unit-type agent --config-id` 能查回该记录。
- **SC-004**: 契约与集成测试的排序后失败 nodeid 名单与实现前基线逐名比对零新增；所有有意扩展项 MUST 在 `verification.md` 中逐条登记（`red-first-evidence.md` 只作过程证据，不承担登记）。
- **SC-005**: `compile-embeds → regen-command-copies → sync-mirrors` 在受影响面（模板、命令、技能、`scripts`、`shared/definitions`）上相对 2026-10-18 基线零 NEW drift；`specify init` 在缺失时播种 [[STR-001]]、在已存在时逐字节不变（幂等）。
- **SC-006**: 非 qoder CLI 的双路径零泄漏，按「qoder 默认值」字面集 {`DeepSeek-Flash`, `max`, `1000000`, `qodercli`} 机械计数（`auto` MUST NOT 计入——它是合法请求层值，可出现在 `method_requested`）：(a) `claude + none` 正向解析——effective config、`cli_args` 与该派发记录的 `config` 组中该字面集出现次数均为 0（记录的 `agent` 组是宿主证据，不属于默认层泄漏面）；(b) `claude + declared` 拒收路径——exit 2 的错误面（declared 缺项错误）中该字面集出现次数为 0。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 解析引擎以夹具配置（默认层声明 `mode: external` 与 `cli: qodercli`）运行 `resolve`，对 `cli_args` 做逐字比较、对 `config_id` 做重复运行比较、对每个非 null 字段与 `quantification.method` 逐项核对 `source_chain`；实现后一次性采集。
- **SC-002 Source**: 负向夹具矩阵逐条执行 `resolve / validate`，记录退出码与消息中的字段清单；实现后一次性采集。
- **SC-003 Source**: 一次 external 派发（未授权时以夹具派发产物替代）后以 `list-records --format json` 查询专属存储；重复调用 [[STR-015]] 后核对行数；实现后一次性采集。
- **SC-004 Source**: 开工前冻结基线失败 nodeid 名单，收尾时全量运行契约与集成测试并以 `comm` 比较；有意扩展项登记在 `verification.md`。
- **SC-005 Source**: 依次执行生成/镜像三连并与 2026-10-18 基线比较零 NEW drift；在临时项目上连续两次 init，对默认层文件做字节比较。
- **SC-006 Source**: 以 `claude + none` 夹具解析并由 `collect-dispatch` 消费其快照产出夹具记录、以 `claude + declared` 夹具执行解析，对 effective config、`cli_args`、记录的 `config` 组与错误面按「qoder 默认值」字面集检索并计数；`auto` 不计入；`agent` 组不参与计数；实现后一次性采集。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `.specify/agents/execution/configs/_defaults.yaml` | FR-001, FR-004, FR-023, SC-005 |
| `STR-002` | `scripts/python/execution-config.py` | FR-005 |
| `STR-003` | `scripts/python/exec-quant.py` | FR-011, FR-012, FR-013, FR-016 |
| `STR-004` | `.specify/skills/internal/run-agent/SKILL.md` | FR-019 |
| `STR-005` | `.specify/skills/internal/run-agent/references/dispatch-preflight.md` | FR-020 |
| `STR-006` | `.specify/skills/internal/create-agent/references/execution-config.md` | FR-021 |
| `STR-007` | `.specify/skills/internal/create-agent/SKILL.md` | FR-021 |
| `STR-008` | `.specify/shared/definitions/subagent-definitions.md` | FR-022 |
| `STR-009` | `.specify/skills/internal/create-team/scripts/dispatch.sh` | FR-019 |
| `STR-010` | `templates/execution-config-defaults.yaml` | FR-023 |
| `STR-011` | `docs/reference/cli/qoder-cli.md` | FR-024 |
| `STR-012` | `docs/reference/agents/templates-and-agents.md` | FR-024 |
| `STR-013` | `--model DeepSeek-Flash --reasoning-effort max --context-window 1000000` | SC-001 |
| `STR-014` | `agent:<slug>` | FR-011 |
| `STR-015` | `collect-dispatch` | FR-012, FR-019, SC-003 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-10-18

无人值守裁决：以下每问均采纳 Recommended 选项。

- Q: 本规格应绑定既有 Feature（059/060）还是新建 Feature？ → A: 新建 Feature 061「子代理 CLI 配置管理与按派发量化」；059/060 保持 Implemented 不变。依据：简报 §2.1 的已裁定范围，配置管理/按派发量化是可独立注册的新能力面。
- Q: 配置解析引擎名是否锁定为 `scripts/python/execution-config.py`？ → A: 锁定 [[STR-002]]（stdlib-only，动作 `resolve / validate / list-configs`）；plan 不得改名，确需改名须走范围修订并同步 [[STR-002]]。全仓同名冲突实测为零（2026-10-18）。
- Q: `auto` 方法解析中的「显式覆盖」统计哪些字段？ → A: 代理层或内联层显式设置且未被清除哨兵（`""` / `auto`）清空的 `model / reasoning_effort / context_window / extra_flags / log_dir` 任一字段；默认层与 `quantification.method` 键本身不计入。仅 `extra_flags` / `log_dir` 覆盖也会使 external 的 auto 落到 `declared`；若 effective config 缺 `model / reasoning_effort / context_window`，则 exit 2，不降级。
- Q: 默认层「整体跳过」时跳过哪些键？ → A: 整层全部键（`mode / model / reasoning_effort / context_window / extra_flags / quantification.method / log_dir / cli`）均不参与合并，并记录到 `skipped_layers`；禁止任何 qoder 默认值（含量化方法）泄漏到非 qoder CLI。
- Q: 配置快照 `config_id` 与本次解析不一致时如何处置？ → A: 非阻塞可见失败：[[STR-015]] 输出原因并以非零退出报告、不写入声称该配置的记录、不阻塞派发结果；存储保持 append-only。

### Session 2026-10-18 (analyze remediation)

本轮为 analyze 第一轮 HIGH=4 的有界上游修复；以下四项为已裁定项（无人值守，不自创用户裁定）。

- **F-01（auto vs 能力矩阵）** → A: 能力矩阵的 `quantification_methods` 约束 MUST 只校验 **resolved** 方法；`auto` 是请求层选择器，先按 FR-009 顺序解析，再接受矩阵校验，MUST NOT 因不在列表中直接被拒。落点：FR-008、FR-009；plan 侧 C-EC-08/C-EC-09、data-model E4/E5；测试义务 T004/T007 补 qodercli/claude 的 `auto` 正向用例。
- **F-02（SC-006 不可达）** → A: 采纳 plan decision 3 的双路径：`claude + none` 正向解析（effective config / `cli_args` / 派发记录中 qoder 默认值计数 0）与 `claude + declared` 拒收错误面（错误消息中 qoder 默认值计数 0）。「qoder 默认值」字面集 MUST 恰为 {`DeepSeek-Flash`, `max`, `1000000`, `qodercli`}；`auto` MUST NOT 计入（它是合法请求层值，可出现在 `method_requested`）。落点：SC-006、SC-006 Source；feature-ref SC-006 映射；C-EC-09；T011 的 `claude + none` 零泄漏记录证据。
- **F-03（默认层 mode 与覆盖优先级）** → A: 代理/内联覆盖触发的 external MUST 优先于低层默认 `mode: native|virtual`——默认层 `mode` 被覆盖，`requires_external=true`；显式（代理/内联）`mode: native|virtual` + 任一覆盖仍 MUST 拒收。落点：FR-002、FR-003；plan Phase 0 decision 1；C-EC-06/C-EC-07；data-model E2；T004/T007 测试义务。
- **C-01（运行时默认层无人播种）** → A: tasks 新增 T033，在本仓通过 `ensure_agent_layer_dirs` / `specify init` 播种 `.specify/agents/execution/configs/_defaults.yaml` 并断言存在；T030 记录驱动者实际派发路径（本线为直接 runner）与运行时默认层存在性，作为 FR-027 的前置证据。落点：tasks T030/T033、依赖、DoD-7、GATE-7；FR-027 判定字段。

同步修复的耦合项：F-04（跳过键补 `mode`）、F-05（`declared` 覆盖显式与 auto 解析两条来源）、F-06（打包资源回退/显式来源缺失即失败）、F-07（快照重算与 collect-before-re-resolve）、C-02（SC-001/US1-1 夹具默认层 `mode: external`）、C-03（external + `cli=null` 拒收）、C-04（`llm`/`quality`/`qualification` 叶子清单）、C-05（external-only 派发范围）、C-06（FR-027 判定字段）、B-01（零 NEW drift + `scripts`/`shared`）、B-02（`auto` 清除哨兵作用域）、F-09（`source_chain` 非 null 字段）、F-10（登记落点统一到 `verification.md`）、F-11（FR-019 证据链）、C-07（T019 stop/远端侧）、E-01（GATE-1 空输出）、E-02（GATE-5 逐 SC 状态）、F-08（能力矩阵只引用 owner）、F-12（US2-1 补齐 11 字段）、F-13（effective 恒 8 键/null 语义）、F-14（显式 `cli` + native/virtual 拒收）。
