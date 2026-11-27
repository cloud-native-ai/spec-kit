# Quality Gate — 四轴验收、硬失败与结果 manifest

> Owner：本文件。前门 Step 4 与六个引擎条目只引用本文件，不复写判据。交付形态与面向用户文字规则的 owner 仍是 [delivery-contract.md](delivery-contract.md)；几何语义与 `layout_policy` 的 owner 是 [semantic-model.md](semantic-model.md)。

## 轴①–④：分开验收，互不替代

| 轴 | 至少要证明什么 |
|----|----------------|
| 语义 | 原生源回读的元素/关系/分组/标签/方向与 LDM 一致（`uncertain` 已声明）；声明了交互时逐 form 复现一次「输入 → 可见变化」 |
| 视觉 | 真实导出成功且可解码；实际文字在盘可查；箭头落点与端点可判；标签确实绑在它描述的那条关系上 |
| 交互/编辑 | 声明的 form 或「可继续编辑」有实际输入证据；未实操即写未验证 |
| 工程复现 | 源、导出图与 manifest 同盘；导出命令、引擎与版本、运行时条件可复述 |

任一轴 `pass` 不得写进另一轴。**语义 pass + 导出成功 ≠ 视觉 pass。**

## 最小质量门（每次交付必过）

1. **原生源回读**：从实际产物文件（不是输入副本）读出完整元素、分组/父级、关系方向与标签，与 LDM 对照计数和集合；同名不同 ID 保留。只复制输入 JSON 再宣称通过不算回读。引擎提供 `native-readback.py` 时，其接口须过 `check-readback-contract.py`；适配器不支持或只抽取部分时记 `unsupported/partial`，不得写成 pass 或图损坏。
2. **真实导出**：导出命令实际执行成功（HTTP 2xx 或 CLI 退出 0），图片可完整解码；`healthz`/健康检查不算出图成功。
3. **文本与端点实测**：实际 SVG/PNG 中的标签文本、字号/可读性、端点与箭头落点有测量或局部原像素复核记录；估算文本宽度不得当成视觉验收。
4. **标签归属**：边标签与它所描述的关系绑定一致——标签错归关系、箭头指入错误框是**硬失败**，必须返修或如实报 fail。
5. **交叉/共线可追踪**：量化并单列（数量 + 清单或报告路径 + 测量口径）；不可消除的交叉如实保留，**不得**靠删边、合并不同关系、加中转业务实体或事后手改 PNG 来消除。
6. **限制显式**：无法验证或不可消除的项写入 `unresolved`；引擎条目「已知限制与返修判据」小节给出的限制必须被逐条回应（修复 / 保留并说明 / 标 N/A）。

复用各引擎已有脚本作为回读/几何检查入口（如 drawio 的 `architecture.py validate`、echarts 的 `verify-deliverable.mjs`/`check-layout.mjs`、mermaid/plantuml 的 `measure-svg-layout.py`、d3js 的 `sds-realization.md` 校验三关）；脚本不具备的能力用该引擎条目声明的只读回读方式补足，不另建跨引擎框架。

## 硬失败与返修

- **硬失败**（出现即该轴 fail，不可用其它轴抵消）：标签错归关系；箭头指入错误框；元素/关系/方向缺失或反向；同名不同 ID 被合并；容器级端点被擅自展开；删边或新增中转业务实体；导出失败仍宣称交付图。
- **partial**：视觉仍有可描述缺陷（拥挤、交叉、遮挡、纵长、字体可疑）→ 带 delta 返修**一次**（上限 1 次）；仍 partial → 交付并在 manifest 与回报里写 `visual: partial` + 未解决项，不得默认写「满意」或「通过」。
- **不能默认满意的两件事**：用户评价缺失时写 `user_evaluation: not_available`（见 SKILL.md Evaluation Form「无评价 = 未评价」）；没有实际执行的项写 `not_performed`/`not_checked`，不写 pass。

## 执行记录与验收分离（run record）

一次绘图运行至少留下五条互不替代的记录轴；任何一轴的完成/pass 都不得写成另一轴，`scripts/check-run-record.py` 机械校验这一封闭结构。

| 轴 | 记录什么（字段） | 不得代替 |
|----|------------------|----------|
| `transport` | `status: completed\|failed\|not_started` + evidence：进程/HTTP 是否走完 | 业务结果 |
| `runtime_identity` | executor/model/context_window/reasoning_effort/config_root/session_id（值或 `not_provided`）+ evidence | 任何结论；该轴只记身份，出现 `status`/`verdict` 即违规 |
| `permission_events` | `status: none\|blocked_by_permission\|not_assessed`、逐事件 `scope: read_only\|deliverable_write\|unknown` 与 outcome、`assessment` | 业务失败；`read_only` 拒绝不是语义错误，但任何 denial 必须保留 `blocked_by_permission` |
| `required_steps` | 每步 `completed\|failed\|blocked\|skipped\|not_started` + evidence | 有未完成步骤时不得让全部业务轴 pass |
| `business_result` | `semantic`（含 `extraction`）、`visual`、`interaction`（含 `exercised`）、`reproducibility`、`satisfaction` 各自状态 + evidence | 彼此替代；`satisfaction` 只有 `not_evaluated` 或 `user_provided` |

- **保留旧状态**：既有记录里因权限拒绝写下的 `blocked_by_permission` 原样保留——即使进程 exit 0、交付物在盘，也不得改写为 success；业务结果在另一轴陈述。
- **适配器边界**：`extraction` 为 `partial/unsupported/not_attempted` 时 `semantic` 不得 `pass`；`fail + reason=graph-corruption` 只允许在 `extraction=complete` 时声明；`unsupported` 是独立状态，既不是 corruption 也不是 pass。
- **禁止合轴**：顶层 `status`/`overall`/`result`/`success`/`verdict` 一律拒绝；没有一条总状态能代替五轴。检查器入口见下方「可执行检查」。

## 原生回读入口契约（native-readback.py）

每个引擎层的原生回读入口固定为：

```bash
python3 references/types/<engine>/scripts/native-readback.py \
  --source <native-file> --semantics <authoritative-json> [--svg <rendered-svg>] \
  --output <new-report>
```

- `--help` / `--version` 退出 0 且无副作用；未声明选项与缺必填参数退出 2；`--output` 已存在必须拒绝，不得覆盖。
- 退出码语义由引擎条目写死并遵守共同下限：`0` 仅当全部已评估项通过；硬差异必须非零；partial/unsupported/not_evaluated 不得记 pass；参数错误用 `2`（`check-readback-contract.py` 按 `2` 校验未知选项与缺参）。
- 报告是单个自足 JSON，至少含 `engine`、`source{path,sha256}`、`actual`（实际抽取的 records）、`semantic{status,diff}`、`visual{checks,issues,limitations}`、`overall`、`unsupported`、`not_evaluated`。`actual` 必须来自原生文件/渲染产物，不得回填期望语义；`source.sha256` 必须等于实际文件哈希。
- 解析器不支持的语法写 `unsupported/partial`，不得伪造成完整覆盖，也不得据此判图损坏；穿框、交叉、标签落点等几何量是该引擎的几何证据，不是输入断言。
- 接口一致性用 `scripts/check-readback-contract.py` 验证（真实夹具由调用方提供）；无真实夹具时运行项记 `not_evaluated`，不算通过。

## 共享渲染访问（render-client.py）

引擎层对共享渲染服务的请求经唯一薄客户端发出，避免手拼 curl/编码/输出链：

```bash
python3 "${SKILL_HOME}/scripts/render-client.py" \
  --service-url <http(s)://host[:port]> \
  --route <引擎条目定义的请求路径> --expect <svg|png|html|javascript|json|text|any> \
  --output <新文件> [--method POST --body <文件> --content-type <mime>] \
  [--preflight-route /healthz] [--receipt <新 JSON>]
```

- **职责只是搬运**：服务 URL 与 route 由调用方提供（endpoint 契约 owner 仍是 [self-deploy-render-service.md](self-deploy-render-service.md)）；客户端不猜端点、不做引擎编码、不做布局或渲染；`--body` 原字节发送，route 原样使用。
- **有界与拒绝**：`--timeout` 1–120 s、`--max-bytes` 1 KiB–512 MiB；不跟随重定向、不支持凭据/cookie、不重试；输出与收据均拒绝覆盖；非 2xx、媒体类型/magic 不符或超限时不落盘。
- **退出码**：`0` 已写入；`2` 参数错误；`3` preflight 不可用（停止渲染、不落盘）；`4` 请求/响应失败；`5` 输出/收据拒绝或不可写。
- `--preflight-only` 供前门 Step 2.5 使用（单条命令替代复合 shell 行）；`--receipt` 只记 `transport`，其余四轴固定 `not_evaluated`——**收据不是验收**。
- 服务不可达时按前门 Step 2.5 中断并提示自部署，不静默改用本地渲染。

## 结果 manifest（每次交付一份，随产物同盘）

**格式：JSON**（`manifest.json`，字段封闭、值与类型由 `scripts/check-manifest.py` 机械校验）。文件名由调用方指定，不与既有产物同名；文件内路径一律相对 manifest 所在目录，**拒绝绝对路径与 `..`**。

| 字段 | 类型 / 取值 | 含义 |
|------|-------------|------|
| `engine` | `d3js\|drawio\|echarts\|excalidraw\|mermaid\|plantuml` | 引擎 |
| `engine_version` | 字符串或 `not_exposed` | 引擎自报版本 |
| `layout_policy` | `preserve\|optimize` | 本次几何归属 |
| `ldm_sha256` | 64 位小写 hex | 本次冻结 LDM/SDS 哈希；**等于 `source.sha256` 即输入回显，检查器拒绝** |
| `runtime_conditions` | `{executor, model, context_window, reasoning_effort, config_root}` | 只记调用方显式提供者；未提供写 `not_provided`，不读凭据 |
| `source` | `{path, format, sha256}`；format ∈ `mmd\|puml\|drawio\|xml\|excalidraw\|json\|html` | 原生源；文件必须实际存在且哈希一致 |
| `exports` | 至少 1 项 `{path, format, width, height, produced_by}`；format ∈ `svg\|png\|pdf\|html`；宽高为整数或 `null` | 真实导出；文件必须存在、非空、魔数匹配 |
| `readback` | `{method, elements, zones, relations, labels, parents, directions}`；计数为实际回读整数；`parents`/`directions` ∈ `verified\|partial\|not_checked` | 原生源/渲染回读证据 |
| `axes` | `semantic ∈ pass\|partial\|fail\|not_checked`；`visual ∈ pass\|partial\|fail\|not_performed`；`interaction ∈ pass\|partial\|fail\|not_applicable`；`engineering ∈ pass\|partial\|fail` | 四轴分列 |
| `crossings` | `{measured: bool, count: int\|null, collinear_length: number\|null, report_ref: 相对路径\|null}` | 交叉/共线量化；口径随引擎，禁止跨引擎排名 |
| `hard_failures` | 字符串数组 | 硬失败清单（出现即不可被其它轴抵消） |
| `unresolved` | 字符串数组 | 未解决项 |
| `user_evaluation` | `not_available` 或 `provided:<摘要>` | 无评价=未评价；裸写「满意/通过」被拒绝 |

**检查器强制的语义不变量**（不是风格建议）：

1. `axes.semantic=pass` 必须带真实回读——`readback.method` 不得为空或 `input-copy\|ldm`，`directions` 不得 `not_checked`，`zones>0` 时 `parents` 不得 `not_checked`；**语义 pass 必须来自原生源/渲染回读，输入回显（`ldm_sha256 == source.sha256`）直接拒绝。**
2. `axes.visual=pass` 必须 `crossings.measured=true` 且至少一份可解码的 svg/png/pdf 导出。
3. `hard_failures` 非空时 `semantic`/`visual` 不得为 `pass`。
4. drawio 原生源由检查器**独立重数**元素/分区/边（mxCell `vertex`/`edge`），与 `readback` 计数不符即 fail；其他引擎的原生格式本检查器不解析（输出 `native_recount: not_supported`），其回读由引擎条目所列脚本负责。

## 可执行检查（脚本入口）

```bash
# 冷启动/比较模式交接：语义冻结 + 几何剥离，逐引擎生成无几何 SDS 与派发索引
python3 "${SKILL_HOME}/scripts/handoff.py" --semantics <shared-semantics.json> --out <已有目录> [--engines d3js,drawio,...] [--policy optimize|preserve]

# 交付前 manifest 检查：退出 0 通过 / 1 违规（列出 code）/ 2 参数或 I/O 错误
python3 "${SKILL_HOME}/scripts/check-manifest.py" --manifest <交付目录>/manifest.json

# 渲染请求的安全传输入口：服务 URL 与 route 由调用方提供；不做引擎编码、布局或端点猜测
python3 "${SKILL_HOME}/scripts/render-client.py" --service-url <url> --route <path> --expect <kind> --output <新文件> [--preflight-route /healthz --preflight-only]

# 运行记录轴分离检查：退出 0 一致 / 1 违规（列出 code）/ 2 参数或 I/O 错误
python3 "${SKILL_HOME}/scripts/check-run-record.py" --record <run-record.json> [--json]

# 引擎回读入口接口契约：真实夹具由调用方提供；无夹具时运行项记 not_evaluated（退出 3）
python3 "${SKILL_HOME}/scripts/check-readback-contract.py" --script <references/types/<engine>/scripts/native-readback.py> --workdir <已有目录> [--source <native> --semantics <json> [--svg <svg>]]
```

- `handoff.py` 拒绝语义损坏（重复 ID、关系端点缺失、counts 不符），把元素 box、关系 via/anchor/端口等几何字段**剥除并记录**在 `handoff.json` 的 `dropped_geometry` 里——新绘图不继承任何一版的几何，由引擎按 `layout_policy` 自主规划。
- `check-manifest.py` 的输出是确定性的 verdict（含 `native_recount`）；manifest 不合格不得声称交付完成，返修回生成源后重跑。
- `render-client.py` 只搬运调用方给定的一个请求；它的 receipt 是 transport 证据，不是语义/视觉/交互/满意度验收，也不构成对任何引擎协议的二次实现。
- `check-run-record.py` 只校验五轴记录的结构与相互矛盾；它不判断图本身，也不把 `blocked_by_permission`、exit 0 或 `unsupported` 改写成另一种状态。
- `check-readback-contract.py` 不判断语义，只验证 CLI 契约与最小报告形状；`unsupported/partial` 与未运行项都不算 pass。

## 边界

- 本文件不持有任何具体业务节点、用户绝对路径、模型名或固定画布；manifest 的路径在交付目录内相对书写。
- 交叉数、线宽、字号等测量口径由各引擎条目声明，**不同引擎的数字不构成统一评分或排名**。
- 引擎的语法、渲染命令、端口与请求 shape 归各引擎条目与 [self-deploy-render-service.md](self-deploy-render-service.md)，本文件不复写。
