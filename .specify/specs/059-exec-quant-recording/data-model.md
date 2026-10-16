# Data Model: Agent+LLM 执行量化记录(Feature 059)

**Spec**: `.specify/specs/059-exec-quant-recording/requirements.md` | **Plan**: `plan.md`(D1–D12 为本文件的裁决引用) | **Date**: 2026-10-16

设计产物:执行量化记录的实体、存储布局、校验规则与非回归基面。行为真源在引擎代码(`scripts/python/exec-quant.py`);本文描述目标 schema 与约束,实现期以契约为准。

## 1. 实体

### 1.1 执行量化记录(Execution Quant Record)

一次受测单元执行的量化快照;记录类型字面量 `[[STR-001]]` = `speckit.exec-quant`,落 `records.jsonl`,一行一记录,**写入后永不改写**。

```json
{
  "kind": "speckit.exec-quant",
  "schema_version": 1,
  "unit_id": "/speckit.plan",
  "unit_type": "command",
  "run_id": "059-exec-quant-recording-20261016T031500Z",
  "run_id_resolution": "explicit | adopted | synthesized",
  "collected_at": "2026-10-16T03:15:02Z",
  "agent": {
    "resolution": "resolved | ambiguous | unresolved",
    "name":          {"value": "qodercli", "provenance": "measured"} | "not_evaluated",
    "version":       {"value": "1.1.72", "provenance": "measured"} | "not_evaluated",
    "binary":        {"value": "/home/x/.qoder/bin/qodercli/qodercli-1.1.72", "provenance": "measured"} | "not_evaluated",
    "argv":          {"value": ["--dangerously-skip-permissions"], "provenance": "measured"} | "not_evaluated",
    "cwd":           {"value": "/path/to/workspace", "provenance": "measured"} | "not_evaluated"
  },
  "llm": {
    "model":            {"value": "gfmodel", "provenance": "measured"} | "not_evaluated",
    "context_window":   {"value": 1000000, "provenance": "measured"} | "not_evaluated",
    "reasoning_effort": "not_evaluated",
    "config_source":    {"value": "~/.qoder/settings.json", "provenance": "measured"} | "not_evaluated",
    "endpoint_candidates": {"ANTHROPIC_BASE_URL": "https://api.example.com", "...": "..."} | "not_evaluated",
    "connection_evidence": {"value": ["203.0.113.7:443"], "provenance": "measured"} | "not_evaluated"
  },
  "quality": {
    "elapsed_ms":  {"value": 81234, "provenance": "carried"} | "not_evaluated",
    "tokens":      {"value": 154321, "provenance": "carried"} | "not_evaluated",
    "errors":      [{"source": "run-determination.failed_set_diff", "count": 2}] | "not_evaluated",
    "satisfaction": {"value": "pass", "provenance": "carried"} | "not_evaluated"
  },
  "qualification": {"value": "complete", "provenance": "carried"} | "not_evaluated",
  "truncated": []
}
```

**字段编码统一规则**:每个可测字段**要么**是 `{"value": X, "provenance": P}` 对象,**要么**逐字为字面量 `not_evaluated`([[STR-002]])——零 `null`、零空串、零缺键。`provenance` 词域封闭(FR-008):`measured`(引擎本机实测)/ `carried`(自同 run 运行判定记录携带)/ `user-given`(用户经 score 动作给出)。`run_id_resolution` ∈ `explicit`(调用方传 `--run-id`)/ `adopted`(采纳同单元最近判定记录的 run_id,D2)/ `synthesized`(无判定记录可采纳,引擎合成时间戳 run_id——此时全部 carried 字段必为 `not_evaluated`)。

**来源约束**(FR-005/006/007 落点):

| 字段组 | 来源 | 缺省行为 |
|--------|------|----------|
| `agent.*` | 自身进程父链上溯 + 宿主 CLI 进程名模式(D8);版本经 `<binary> --version` 子进程(超时 10s) | 任一字段不可解析 → 该字段 `not_evaluated`;归属含糊 → `resolution: "ambiguous"`,可确定部分照录,不猜测唯一进程 |
| `llm.model/context_window/reasoning_effort/config_source` | 宿主配置面适配器(D7,qoder:`~/.qoder/settings.json`) | 适配器缺失或键未设置 → `not_evaluated`;**MUST NOT** 对未设 effort 推断 CLI 默认 |
| `llm.endpoint_candidates` | 白名单端点变量名,值仅取 origin(scheme://host,剥 path/query;D6) | 白名单变量全缺席 → `not_evaluated` |
| `llm.connection_evidence` | `ss -tnp` 解析宿主进程已建立连接的远端 `ip:port`(无 DNS 依赖;D6) | ss 不可用/无连接 → `not_evaluated`;**MUST NOT** 据此判定「生效端点」——只录证据 |
| `quality.elapsed_ms/tokens/satisfaction/qualification` | 同 run 运行判定记录携带(精确 `(unit_id, run_id)` 或 adopted 记录;A6 不重复测量) | 判定记录缺失 → `not_evaluated` |
| `quality.errors` | 自己枚举的声明来源:判定记录 `failed_set_diff` 计数、红轴计数(逐项 `source` 标注;D5) | 判定记录缺失 → 整组 `not_evaluated` |

**非功能约束**:`truncated` 列出被截断字段的 JSON 路径;序列化记录 > 64 KiB 时按字段截断直至达标(D9);写盘前凭据形值防御扫描,命中值脱敏并标注(D9)。

### 1.2 用户打分行(Score Entry)

落 `scores.jsonl`,append-only,重打分追加新行、按 `scored_at` 后者胜(list-records 时 join 最新一条)。

```json
{
  "kind": "speckit.exec-quant",
  "entry_type": "score",
  "unit_id": "/speckit.plan",
  "unit_type": "command",
  "run_id": "059-exec-quant-recording-20261016T031500Z",
  "score": 4,
  "note": "可选说明",
  "scored_at": "2026-10-16T04:00:00Z",
  "provenance": "user-given"
}
```

`score` 为 1–5 数值(通道约定,非打分模型——模型/阈值 Out of Scope,D12)。与运行判定推导的 satisfaction 凭 `provenance` 区分(A4):打分来源 = `user-given`(本文件),推导满意度 = `carried`(记录内 `quality.satisfaction`)。

### 1.3 执行量化存储(Execution Quant Store)

```text
.specify/memory/exec-quant/
├── records.jsonl   # 执行量化记录,append-only,永不改写
└── scores.jsonl    # 用户打分行,append-only,按时间后者胜
```

- 位置:项目 memory 层(FR-009),引擎自有;与 `feedback/`、`evidence/`、`knowledge/` 同层互不渗透。
- append-only:两文件都只追加;`list`/`score` 动作不改写既有行(D3)。
- 结构性排除(FR-011):`feedback-utils.py --action package` 只读 feedback store(实测 L1151–1262),本存储对打包结构性不可见——零代码达成隔离;无任何上送路径。
- 会话内容零采集:MUST NOT 记录 prompt/response 文本(requirements Out of Scope);本 schema 无任何对话文本字段。

### 1.4 量化引擎(Recording Engine)

`scripts/python/exec-quant.py`(框架源)→ `.specify/scripts/python/exec-quant.py`(镜像,scripts 对自动吸收)。

- **动作封闭集**(D1):argparse `choices = ["collect", "list-records", "score"]`——与既有四引擎动作名**零交集**(feedback-utils 既有 `record`/`list`,两者皆避,消除 union 归属歧义);union 对账经 choices 路径实读(`contracts/probe-registration.md` §2)。`collect` 采集+落库一步;`list-records` 过滤枚举(`--unit-id` / `--unit-type` / `--since`,text|json 双形态,join 打分);`score` 补录打分(需 `--unit-id --run-id --score`)。
- **退出码**:`0` 成功(含优雅跳过,如 simple-unit 或判定记录缺失的降级采集);`1` 采集/写盘失败(stderr 可见,wrap-up 非阻塞继续,FR-012);`2` 用法错误。
- **run_id 解析**(D2):`--run-id` 可选;缺省 → 按 `(unit_id)` 查最近判定记录,采纳其 run_id(有界 recent 窗口,常量值与语义以 plan D2 为唯一裁决点);无命中 → 合成时间戳 run_id + carried 字段全 `not_evaluated`。
- **非阻塞**:引擎自身不抛未捕获异常中断调用方——失败以退出码 1 + stderr 消息呈现。
- **Probe 注册行**(声明性元数据,行为真源在引擎代码):1 Class + 4 Objects + 1 Handler + 1 Binding,详见 `contracts/probe-registration.md`。

### 1.5 同 run 判定记录(Run-Determination Record,只读引用)

既有实体,本特性**只读不写**(FR-015):引擎经 `(unit_id, run_id)` 或 adopted 语义读取其四轴(`token_consumption/elapsed/artifact_correctness/satisfaction`)、`qualification`、`failed_set_diff`、红轴信号。其 schema 与改进流程契约不变;量化记录中的携带值是标注来源的机器副本(dated execution artifact,A6),不作为现行事实被引用。

### 1.6 Probe 注册行(Probe Registry Rows)

伞形注册表 `shared/definitions/probe-definitions.md` scripts 切片新增:Class `exec-quant`、Objects `eq-collect-execution` / `eq-probe-host-process` / `eq-probe-host-config` / `eq-probe-determination-link`、Handler `h-exec-quant`(engine/collect/non-blocking/order 15)、Binding(`@point:wrap-up`, `all`)。逐行字面与登记契约见 `contracts/probe-registration.md`。

## 2. 校验规则(Validation Rules)

- **V1 身份完备**:每条记录 `unit_id` 非空且匹配封闭形 `/speckit.<cmd>` | `skill:<name>` | `custom:<owner>/<name>`;`unit_type` ∈ `command|skill|custom-unit`;`run_id` 非空(与运行判定同键语义)。
- **V2 字段二值律**:每个可测字段为 value 对象或逐字 `not_evaluated`;value 对象的 `provenance` ∈ 封闭词域;全记录零 `null`、零空串、零缺键(SC-001 的「零空缺」机械判据)。
- **V3 类型与版本**:`kind == "speckit.exec-quant"`([[STR-001]],records.jsonl)/ `entry_type: "score"` 行同 kind;`schema_version == 1`。
- **V4 纯追加**:records.jsonl 与 scores.jsonl 均只增不改;任何动作不得改写既有行(D3/FR-009)。
- **V5 封顶截断**:序列化记录 ≤ 64 KiB;超限时截断且 `truncated` 非空;`truncated` 为空当且仅当未截断。
- **V6 凭据零出现**:采集侧白名单(仅枚举端点变量名、仅 origin)+ 出口防御扫描(D9);全记录扫描凭据形值命中数 = 0(SC-004)。
- **V7 携带一致性**:`run_id_resolution ∈ {explicit, adopted}` 时,carried 字段值 MUST 与被携带判定记录逐值一致;`synthesized` 时 carried 字段 MUST 全为 `not_evaluated`(A6 不臆造)。
- **V8 非阻塞**:collect 的任何失败路径(宿主探测异常、判定记录缺失、写盘失败)以退出码 1 + stderr 呈现,MUST NOT 使单元运行失败或劣化(FR-012)。

## 3. 状态机

记录无状态迁移(append-only)。仅两条派生生命周期:

```text
记录:appended ──(score 动作)──> scored(scores.jsonl 存在匹配行;list join 呈现,可重打分追加)
采集:probe ──(全部可得)──> measured fields ──(任一不可得)──> not_evaluated per-field ──(写盘失败)──> 退出码 1,零落库
```

## 4. 非回归基面(FR-015 / SC-003)

既有测试套件中本特性 MUST NOT 使其出现**新增**失败(失败名单与冻结基线逐名比对,name-level):

- contract(20):`test_probe_registry_umbrella.py`、`test_handler_registry.py`、`test_probe_engine_action_sets.py`(本特性**有意扩展**,扩展后自身须绿)、`test_probe_nonentity_catalog.py`、`test_phase2_bindings.py`、`test_compile_embeds.py`、`test_compile_propagation_order.py`、`test_compile_reconcile_guards.py`、`test_wrap_up_line_budget.py`、`test_wrap_up_wording_gate_safe.py`、`test_runtime_mode_gate.py`、`test_feedback_probe_cli.py`、`test_feedback_probe_registry.py`、`test_feedback_probe_entry_schema.py`、`test_feedback_introspection_engine.py`、`test_feedback_utils_cli.py`、`test_feedback_entry_schema.py`、`test_feedback_two_path_routing.py`、`test_run_determination_engine.py`、`test_run_determination_passive_wiring.py`
- integration(5):`test_feedback_command_record.py`、`test_feedback_skill_record.py`、`test_feedback_dedup.py`、`test_feedback_partial.py`、`test_feedback_selective_triggering.py`

行为面不变式:feedback record/list/package 动作、probe 注册表校验、运行判定 determine/settle/history 与四轴记录 schema、反馈路由推导——零改动(`engine-action-sets.md` 对账面的 exec-quant 分区为**新增节**,不触碰既有两分区)。
