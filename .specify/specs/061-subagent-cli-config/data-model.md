# Data Model: 子代理 CLI 配置管理与按派发量化（Feature 061）

**Feature**: 061 | **Plan**: [plan.md](plan.md) | **Spec**: [requirements.md](requirements.md)
**Contract owners**: 解析引擎行为 → [`contracts/execution-config-cli.md`](contracts/execution-config-cli.md)；记录 schema → [`contracts/exec-quant-v2.md`](contracts/exec-quant-v2.md)；接线 → [`contracts/dispatch-wiring.md`](contracts/dispatch-wiring.md)
**Runtime owners**: 能力矩阵唯一 owner = `CAPABILITY_MATRIX`（`scripts/python/execution-config.py`）；记录行为唯一 owner = `scripts/python/exec-quant.py`

本文件定义实体、字段、关系与校验规则；行为细节以两份契约与引擎代码为准。字段名一旦在本文件与契约中固定，实现不得改名（requirements Shared Strings 为身份标识）。

## E1 — Execution Config Layers（分层配置输入）

一次解析最多读取三层，按固定优先级合并：

| Layer | Source | Path / provenance | Tracked |
|-------|--------|-------------------|---------|
| `defaults` | 默认层 | `.specify/agents/execution/configs/_defaults.yaml`（模板 owner `templates/execution-config-defaults.yaml`） | yes |
| `agent-config` | 代理配置 | `.specify/agents/execution/configs/<slug>.yaml` | yes |
| `inline` | 内联派发参数 | `resolve` 命令行参数 | n/a |

**Allowed keys by layer**:

| Key | `defaults` | `agent-config` | `inline` | Kind |
|-----|-----------|----------------|----------|------|
| `agent` | reject | allowed（必须等于 `<slug>`） | n/a | identity |
| `mode` | allowed（默认值） | allowed | `--mode` | topology identity |
| `cli` | allowed（默认值） | allowed（声明） | `--cli` | topology identity |
| `model` | allowed | allowed | `--model` | override |
| `reasoning_effort` | allowed | allowed | `--reasoning-effort` | override |
| `context_window` | allowed | allowed | `--context-window` | override |
| `extra_flags` | allowed | allowed | `--extra-flags` | override |
| `log_dir` | allowed | allowed | `--log-dir` | override |
| `quantification.method` | allowed | allowed | `--quantification-method` | override（方法选择） |

`mode` 在默认层是默认值而非声明：默认层参与时作为 base；默认层整层跳过时随之跳过。跨层冲突规则只比较代理层与内联层的显式声明。

**Relations**: E1 → E2（merge）；E1 的 `agent-config` 引用一个 Agent Template/Instance slug（存在性由 `create-agent` 授权时保证；`resolve` 只解析配置，不要求定义文件在位）。

## E2 — Effective Config & Config Identity

`resolve` 的输出核心。字段集固定：

| Field | Type | Rule |
|-------|------|------|
| `mode` | `native` \| `virtual` \| `external` | 代理/内联显式值 > 默认层默认值（层参与时）> 覆盖推导（external）> native（060） |
| `cli` | string \| null | 已知 CLI 名；显式声明不得与 native/virtual 共存；默认层值可生效但 native/virtual 不生成旗标 |
| `model` | string \| null | 非空覆盖值；清除哨兵后为 null |
| `reasoning_effort` | string \| null | 同上 |
| `context_window` | positive int \| null | 同上；不得为 bool/0/负数/非整数 |
| `extra_flags` | string \| null | 单行；可被 `shlex.split`；不含托管旗标 |
| `log_dir` | string \| null | 解析后必须位于 `.specify/agents/execution/logs` 内 |
| `quantification` | object | `{requested, resolved}`，见 E5 |

**Merge semantics**:

1. 低层值先入；代理层值覆盖或清除；内联值最后覆盖或清除。
2. **清除哨兵**：`""` 与 `auto` 对 `model / reasoning_effort / context_window / extra_flags / log_dir` 表示“清除低层值”。effective config **恒含全部 8 个键**；被清除或从未提供的字段值为 `null`。清除字段不生成 CLI 旗标、不写入 `source_chain`。
3. `quantification.method` 的 `auto` 是合法方法值，不是清除哨兵；空串对它是非法枚举。
4. 所有被加载层的值在合并前先做字段级校验（类型/枚举/log_dir/extra_flags）；任一非法值即使会被高层覆盖也拒收（确定性优先）。
5. 默认层整层跳过时，其全部键（含 `cli` 与 `quantification.method`）不参与合并，并记入 `skipped_layers`。

**Identity fields（`mode` / `cli`）**:

- 代理层与内联层同时声明且不一致 → exit 2，消息列出字段名（`mode` / `cli`）。
- 默认层 `cli` 不是声明：代理/内联显式选择不同 CLI → 默认层整层跳过；相同 → 正常参与。
- `mode` 缺省时按 060 native 优先：存在代理/内联非清除覆盖 → `external`；否则 `native`。**显式 `cli` 不单独触发 external**。默认层可提供 `mode` 作为默认值（层参与时生效，层跳过时一并跳过）。
- 显式 `cli` 与生效的 `native`/`virtual` 同时出现 → exit 2（`cli` 仅用于 external，属身份矛盾）。
- 显式 `mode: native|virtual` + 代理/内联任一非清除覆盖 → exit 2，提示改用 external。

**`source_chain`**: `{<field>: {"layer": "defaults"|"agent-config"|"inline"|"derived"}}`，文件层额外带 `"path": <workspace-relative path>`；覆盖 effective config 中每个非 null 字段以及 `quantification.method`。inline/derived 来源**省略 `path` 键**（不写 null），以满足 059 记录律。`skipped_layers`: `["defaults"]`（字符串数组）。

**`config_id`**: `sha256(canonical_json(effective))[:16]`，其中 canonical JSON = `json.dumps(effective, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`；`effective` 恒含 `mode / cli / model / reasoning_effort / context_window / extra_flags / log_dir / quantification` 八个键（缺省值为 `null`），不含 `agent`、路径、时间戳、warnings、cli_args。重复解析同一输入必须得到同一 `config_id`。

## E3 — Config Snapshot（配置快照）

`resolve` 每次成功解析写一份快照，供 `collect-dispatch` 校验：

- **Path**: `.specify/agents/execution/logs/config-snapshots/<config_id>.json`（相对 workspace root 的 POSIX 路径；gitignored 运行证据；目录自动创建；原子写：临时文件 + `os.replace`）。
- **Fields**: `kind="speckit.execution-config-snapshot"`、`schema_version=1`、`config_id`、`resolved_at`、`agent`、`effective`、`source_chain`、`skipped_layers`、`requires_external`、`cli_args`、`log_dir`（effective `log_dir` 或默认 `.specify/agents/execution/logs`）。
- **Integrity**: 消费方 MUST 重算 `sha256(canonical_json(snapshot.effective))[:16]` 并与 `snapshot.config_id` 比较；不一致 → 非阻塞可见失败（exit 1，不写记录）。
- **Overwrite**: 同一 `config_id` 的重复解析覆盖同一路径（最新 `resolved_at` 生效）；不同 `config_id` 各占一文件。并发同 id resolve 可能刷新 `resolved_at`，实现须在 collect 后再发起同 id 的新 resolve（plan 风险 7）。

**Relations**: E2 → E3（1:1 per resolution）；E3 → E6（`config` 组引用 `config_id` 与 `snapshot` 路径）。

## E4 — CLI Capability Matrix（代码侧单一 owner）

**Owner**: `CAPABILITY_MATRIX` in `scripts/python/execution-config.py`。本文件只定义矩阵形状与引用；具体值以 [contract C-EC-08](contracts/execution-config-cli.md#c-ec-08-cli-capability-matrix-single-owner-in-code) 的 dated 设计规格与代码 owner 为准。

Shape per CLI:

```text
{
  "<cli>": {
    "external": true|false,
    "flags": {"model": bool, "reasoning_effort": bool, "context_window": bool},
    "quantification_methods": ["declared", "qoder-settings", "none"],
    "reason": "<why external is unavailable / what is unverified>"
  }
}
```

Current behavior is specified in [contract C-EC-08](contracts/execution-config-cli.md#c-ec-08-cli-capability-matrix-single-owner-in-code) as a dated design specification; the runtime values live only in `CAPABILITY_MATRIX`. Consult C-EC-08 for the exact per-CLI list; this file does not restate it.

**`cli_args` generation**: 仅 `mode=external` 生成；顺序固定 `--model <v> --reasoning-effort <v> --context-window <v>`，随后 `extra_flags` 的 `shlex.split` token。native/virtual 恒为 `[]`。

## E5 — Quantification Method Resolution

**Method domain**: `auto / declared / qoder-settings / none`。

**Requested**: 最高层显式方法值；若默认层被跳过或无任何层声明 → `auto`。

**Auto resolution order**（固定）：

1. `mode=external` 且代理/内联层存在任一**非清除**覆盖（`model / reasoning_effort / context_window / extra_flags / log_dir`）→ `declared`。
2. `mode=external` 且无显式覆盖、`cli=qodercli` → `qoder-settings`。
3. `mode=native|virtual` 且宿主 CLI 为 `qodercli` → `qoder-settings`。
4. 其余 → `none` + warning（写入 resolve 的 `warnings` 数组与 stderr）。

**Host detection order**（仅规则 3 需要）：`--host-cli` → `SPECKIT_HOST_CLI` → 复用 `exec-quant.collect_agent()`（`/proc` 可用时）→ `unknown`。`unknown` 视为非 qoder，解析为 `none` + warning，不猜测。

**Explicit method constraints**:

- `declared`: effective config 必须同时具备 `model / reasoning_effort / context_window`；缺一 → exit 2，不降级。
- `qoder-settings`: 必须由 qodercli 支持（external qodercli，或 native/virtual 且宿主为 qodercli）；否则 exit 2。
- `none`: 合法，不要求任何字段。
- 方法同时受 E4 的 `quantification_methods` 约束。

**Explicit override definition**（规则 1 与 FR-003 共用）：代理层或内联层显式设置且未被清除哨兵清空的五个覆盖字段任一；默认层与 `quantification.method` 本身不计入。

## E6 — Agent Dispatch Record v2（派发量化记录）

`exec-quant.py` 的 v2 记录形状（`collect` 与 `collect-dispatch` 共用外层）：

| Field | Type | `collect`（command/skill/custom） | `collect-dispatch`（agent） |
|-------|------|-----------------------------------|------------------------------|
| `kind` | literal | `speckit.exec-quant` | same |
| `schema_version` | int | `2` | `2` |
| `unit_id` | string | `/speckit.*`, `skill:*`, `custom:*` | `agent:<slug>` |
| `unit_type` | string | `command`/`skill`/`custom-unit` | `agent` |
| `run_id` | string | determination run_id / synthesized | 派发 label（explicit） |
| `run_id_resolution` | enum | `explicit`/`adopted`/`synthesized` | `explicit` |
| `collected_at` | ISO Z | yes | yes |
| `agent` | object | 宿主进程组（059 语义不变） | 同左 |
| `config` | object | 11 个叶子全 `not_evaluated` | 见下 |
| `llm` | object | 059 语义 | 按 `method_resolved` |
| `quality` | object | 059 语义 + `exit_code=not_evaluated` | 见下 |
| `qualification` | object/literal | 059 语义 | `not_evaluated` |
| `truncated` | list | yes | yes |

**`config` 组字段（恰为 11 个）**: `config_id / source_chain / method_requested / method_resolved / mode / cli / model / reasoning_effort / context_window / extra_flags / snapshot`。取值为快照对应值；快照中 null 的 effective 字段落 `not_evaluated`；`source_chain` 原样复制且其条目不含 null（inline/derived 无 `path` 键）。

**`llm` by method**:

| Field | `declared` | `qoder-settings` | `none` |
|-------|-----------|------------------|--------|
| `model` | `{"value", "provenance":"configured"}` | measured | `not_evaluated` |
| `reasoning_effort` | configured | measured | `not_evaluated` |
| `context_window` | configured | measured | `not_evaluated` |
| `config_source` | `{"value":"execution-config:<config_id>","provenance":"configured"}` | settings path measured | `not_evaluated` |
| `endpoint_candidates` | `not_evaluated` | `not_evaluated` | `not_evaluated` |
| `connection_evidence` | `not_evaluated` | `not_evaluated` | `not_evaluated` |

`qoder-settings` 复用从 059 `collect_llm()` 抽出的 qoder settings 读取器（`~/.qoder/settings.json`：`model.name`、`model.preferences[<name>].contextWindow`、`...reasoning.effort`）；文件缺失/不可读 → 三字段 `not_evaluated`，记录照常落库。

**`quality` fields**:

- `exit_code`: `{"value": <int>, "provenance":"measured"}` 或 `not_evaluated`；来源 `.status` 的 `<label> exit=<code>`。
- `elapsed_ms`: 优先最后一条含整数 `duration_ms` 的 stream-json 对象；否则 `.status` mtime − 快照 `resolved_at`（毫秒，非负）；都无 → `not_evaluated`。
- `tokens`: 同一 stream-json 对象内同时存在整数 `input_tokens` 与 `output_tokens` 时取二者之和；否则 `not_evaluated`。
- `errors`: exit 0 → `[]`；非 0 → 恰一条 `{"source":"dispatch.exit_code","count":1}`（保持 059 精确键形状；退出码值只在 `quality.exit_code`）；无 `.status` → `not_evaluated`。
- `satisfaction`: `not_evaluated`（派发记录不消费运行判定）。

**Idempotency**: 幂等键 `(unit_id, run_id)`；在存储锁内完成查重 + append，重复调用不写第二行。存储保持 append-only。

**v1 read-only normalization**: `list-records` / `score` 读取 v1 记录时，仅对输出视图补 `config` 组（全 `not_evaluated`）与 `quality.exit_code=not_evaluated`；不重写 `records.jsonl`、不改 `schema_version`。

**Relations**: E3 → E6（config 快照引用）；E6 → scores.jsonl（可选用户打分，`provenance=user-given`）。

## E7 — Defaults Layer & Seeding（默认层与播种）

- **Template owner**: `templates/execution-config-defaults.yaml`（框架源；随 wheel 打包）。
- **Seeded copy**: `.specify/agents/execution/configs/_defaults.yaml`。
- **Content（初始，dated record 2026-10-18）**: `cli: qodercli`；`model: DeepSeek-Flash`；`reasoning_effort: max`；`context_window: 1000000`；`quantification.method: auto`。内容 owner 是模板文件本身；本节不复述为运行时真源。
- **Seeding rule**: `ensure_agent_layer_dirs(root_path, defaults_source=None)` 在 `execution/configs/_defaults.yaml` 不存在时，从 `defaults_source`（init 传入 `resource_path/templates/execution-config-defaults.yaml`）复制；`defaults_source` 未传时尝试 `get_resource_path()/templates/...`；显式来源缺失 → `RuntimeError`（打包缺陷可见）；目标已存在 → 逐字节不变。
- **Idempotency**: 重复 init 不覆盖；用户可自由编辑该文件。

## Validation Rules

| ID | Rule | Failure |
|----|------|---------|
| V1 | YAML 子集：仅注释、`key: value`、一层 `quantification:` 嵌套 | exit 2，指明文件与行/键 |
| V2 | 拒绝 tab、列表（`- ` / `[...]`）、更深嵌套、重复键、无冒号行 | exit 2 |
| V3 | 未知键或层内不允许的键（如默认层 `agent`） | exit 2，列出键 |
| V4 | `mode ∈ {native,virtual,external}`；`cli` 为字符串 | exit 2 |
| V5 | `context_window` 为正整数；拒绝 bool、0、负数、非整数 | exit 2 |
| V6 | `log_dir` 解析后位于 `.specify/agents/execution/logs` 内（含 `..` 穿越防护） | exit 2 |
| V7 | `extra_flags` 单行；`shlex.split` 失败或含 `-m` / `--model` / `--reasoning-effort` / `--context-window`（含 `=` 形式） | exit 2 |
| V8 | `quantification.method ∈ {auto,declared,qoder-settings,none}`；`quantification` 只允许 `method` | exit 2 |
| V9 | `agent`（若声明）必须等于请求 slug | exit 2 |
| V10 | `mode`/`cli` 跨层冲突、native/virtual + 显式 cli、native/virtual + 覆盖、external + 未验证 CLI/旗标 | exit 2，列字段 + 支持集 |
| V11 | 显式 `declared` 缺任一 model/effort/context；显式 `qoder-settings` 非 qoder 支持 | exit 2，不降级 |
| V12 | 默认层缺失或非法 | exit 2，指明路径与 `specify init` 修复方式 |
| V13 | 快照缺失/不可读/kind 或 schema 不符/config_id 重算不一致 | collect-dispatch exit 1，不写记录 |
| V14 | collect 收到 `agent:` 单元；collect-dispatch 收到非 agent 单元 | exit 2 |
| V15 | 记录序列化 > 64 KiB | 按 059 策略截断并标注，身份字段保留 |
