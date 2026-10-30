# Data Model: Humanize Run Output（动作输出的人类友好化）

**Feature**: 062 扩展（本规格 `079-humanize-run-output`）
**Input**: `requirements.md` § Key Entities + FR-001…FR-030
**性质**: 设计期数据模型。实体是**提示词契约里的结构化概念**，不是数据库表——除 E4 的临时占位文件与
E8 的显式输出外，没有任何实体落盘。字段名与语义在本文件定义一次；契约测试按此断言，别处只引用。

---

## E1 HumanizeRun — 一次调用

一次 `/speckit.humanize` 调用 = 一个 HumanizeRun。它是其余实体的聚合根。

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `run_id` | `<UTC 时间戳>-<6 位随机>` | 一次运行的稳定标识；同时是 E4 占位文件名 | 本文件 |
| `parse` | E2 | 入口解析结果（决定本运行是不是 run mode） | FR-001…FR-006 |
| `instruction` | E3 \| null | run mode 下待执行指令；content mode 下为 null | FR-001 |
| `carrier` | `native` \| `in-session` | 实际使用的执行载体 | FR-007, FR-011 |
| `reservation` | E4 \| null | run mode 的并发占位；content mode 为 null | FR-030 |
| `envelope` | E5 \| null | 子代理（或降级执行）回传的结果信封 | FR-009 |
| `context` | E6 \| null | 报告前装配的上下文包 | FR-014 |
| `report` | E7 \| null | 主会话撰写的报告 | FR-018 |
| `output` | E8 \| null | 显式输出目标；缺省为 null（零写入） | FR-024 |
| `status` | 见 § 状态机 | 运行状态，不是报告口径 | 本文件 |

### E1 状态机

| 当前 | 事件 | 下一状态 | 守卫（不满足即停在当前并走拒绝/上报） |
|------|------|----------|--------------------------------------|
| `parsed` | 入口判定为 content mode | `handed-to-content-mode` | 无内容源与非空指令同现（FR-002） |
| `parsed` | 入口判定为 run mode | `reserved` | E4 占位成功（FR-030） |
| `parsed` | 入口判定为拒绝 | `rejected` | 拒绝原因已点名（FR-003, FR-006） |
| `reserved` | 派发发出 | `dispatched` | 派发载荷含快速失败子句（EX 契约） |
| `dispatched` | 收到信封 | `returned` | 信封含显式异常行（FR-009） |
| `dispatched` | 派发失败 / 中止 | `aborted` | 失败坐标已记录，不重试（FR-010, FR-012） |
| `returned` | 报告落定（缺省会话内） | `reported` | 五节齐备（FR-018） |
| `reported` | 显式 `--output` 写入成功 | `released` | 原子写入成功或未给 `--output`（FR-024） |
| 任意已占位状态 | 任一出口（含异常） | `released` | E4 已移除（EX 契约） |

`rejected` 与 `aborted` 都不是「成功」；状态名只供实现自检，**报告口径**由 E7 `verdict` 决定（FR-019）。

---

## E2 InvocationParse — 入口解析（确定性）

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `tone` | `professional` \| `humorous` \| `empathetic` \| `colloquial` \| null | 取值域沿用既有契约，本特性不改 | FR-004 |
| `audience` | string \| null | 自由文本，只作用于表达层 | FR-004, FR-022 |
| `file` | path \| null | 显式内容源 | FR-002 |
| `inline` | string \| null | 显式内联内容源 | FR-002 |
| `output` | path \| null | 显式写入目标 | FR-004 |
| `force` | bool | 覆盖既有目标 | FR-004 |
| `instruction_text` | string | 选项之后的剩余文本（逐字，不重写） | FR-001 |
| `mode` | `run` \| `content` \| `reject` | 三分支判定结果 | FR-001…FR-003 |
| `reject_code` | 见下表 \| null | `mode=reject` 时的封闭原因码 | FR-002, FR-003, FR-030 |

### E2 判定表（封闭，按顺序求值）

| # | 内容源（`file`/`inline`） | 指令文本 | 判定 |
|---|--------------------------|----------|------|
| 1 | 有 | 非空 | `reject` / `both-sources-and-instruction` |
| 2 | 有 | 空 | `content` |
| 3 | 无 | 非空 | `run` |
| 4 | 无 | 空 | `reject` / `no-input` |

内容源自身为空/纯空白时按第 4 行走（`reject` / `empty-input`），不落进第 2 行——空内容不是内容。

### reject_code 封闭集

| 码 | 触发 | 点名要求 |
|----|------|----------|
| `both-sources-and-instruction` | 内容源与非空指令同现 | 点名两者（源名与指令前缀） |
| `no-input` | 既无内容源也无指令 | 用法 + 迁移提示 |
| `empty-input` | 内容源为空/纯空白 | 该源为空 |
| `unknown-tone` | 语气值在封闭集外 | 该值与支持集 |
| `bad-extension` | 内容源或输出目标扩展名不受支持 | 该扩展名与支持集 |
| `unwritable-target` | 输出目标不可写 | 目标路径与原因 |
| `active-run` | 同一仓库已有活动占位 | 冲突 `run_id` 与起始时间 |
| `output-occupied` | 输出目标被另一次运行占位 | 目标路径与冲突 `run_id` |
| `nested-invocation` | 指令含本命令的调用 token | 命中的字面量 |

---

## E3 Instruction — 待执行指令

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `text` | string | 指令原文，逐字进入派发载荷与报告；MUST NOT 被 humanize 改写或简化 | FR-001, FR-013 |
| `language` | `zh` \| `latin` \| `undetermined` | 报告语言的第一顺位判据 | FR-018（语言条） |
| `nesting_hits` | string[] | 指令中出现的本命令调用 token（空 = 无嵌套） | FR-030 |

`language` 的判定复用既有主语言计数口径（占位符、代码与纯数字/符号剔除后按书写系统计数，并列取
首个非空段落）；口径 owner 是 062 的技能 Stage 2 规则，本文件不复述算法，只固定它在报告语言上的用途。

---

## E4 RunReservation — 并发占位（唯一的落盘面）

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `path` | `.specify/.tmp/humanize/<run_id>.run` | 一文一件；文件名即 run_id | FR-030 |
| `created_at` | ISO 时间戳 | 占位建立时刻；过期判定依据 | FR-030 |
| `output_target` | path \| null | 本次运行声明的输出目标（无则 null） | FR-030 |
| `ttl_hours` | int = 24 | 超过即视为遗弃占位（不阻断，但在报告中点名） | FR-030 |

不变量：

- **仓库级恰一**：同一仓库同时至多一个未过期占位；后来者按 `active-run` 拒绝并点名冲突 `run_id`。
- **目标级恰一**：同一输出目标同时至多一个未过期占位；后来者按 `output-occupied` 拒绝。
- **离开即释放**：任何出口（正常、失败、中止、拒绝后的清理）都移除本人占位；不留残骸。
- **零写入不变**：占位落在受制裁的临时根（`.specify/.tmp/`，已被 `.specify/.gitignore` 匹配），
  不是报告也不是副本，运行结束即消失；它 MUST NOT 出现在 `git status` 里。
- **遗弃占位**：过期占位不移除他人文件，只在报告 `## Risks & Limits` 点名「检测到遗弃占位」。

---

## E5 ActionResultEnvelope — 子代理回传信封

子代理只回传信封，不写报告（A6）。信封是**回传消息**，不是文件。

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `status` | `completed` \| `failed` \| `partial` \| `aborted` \| `needs-confirmation` \| `not-an-action` | 执行结果类别 | FR-012, FR-019 |
| `final_output` | string \| null | 子代理的最终输出原文（可为空） | FR-009 |
| `products` | `{path, kind: created\|modified}[]` | 指令造成的写入，逐项 | FR-009, FR-024 |
| `evidence` | `{pointer, kind: command\|path\|reading}[]` | 可定位证据：命令 + 退出码 / 产物路径 / 测试读数 | FR-009, FR-020 |
| `failures` | `{where, what}[]` | 失败坐标与信息 | FR-012 |
| `blocked_at` | string \| null | 需确认却无法询问时停下的位置 | FR-008（clarify 裁决） |
| `anomaly_line` | string | 显式异常行：无异常写 `未发现异常`，有异常写行首 `ANOMALY:` 逐条 | 快速失败纪律（派发注入） |

不变量：

- `status=needs-confirmation` ⇒ `blocked_at` 非空，且 `products` 只含该步之前已完成的写入。
- `status=completed` 且 `final_output=null` 且 `products=[]` ⇒ 报告写「无可报告输出」，`## Evidence` 写 `none`（SC-009）。
- 缺 `anomaly_line` ⇒ 信封不完整：结论 MUST NOT 被消费（EX 契约）；报告按失败/不完整处理。
- `not-an-action`：指令不是可执行动作（散文/聊天式提问），报告 `## Conclusion` 写「未执行任何动作」（Edge Cases）。

---

## E6 ContextBundle — 上下文包

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `action_result` | E5 | 动作输出/证据来源 | FR-014 |
| `governance.instructions` | `read` \| `unavailable` \| `not-read` | `.specify/instructions.md` | FR-014, FR-015 |
| `governance.constitution` | 同上 | `.specify/memory/constitution.md` | FR-014, FR-015 |
| `governance.glossary` | 同上 | `.specify/memory/glossary.md` | FR-014, FR-015 |
| `governance.feature_registry` | 同上 | `.specify/memory/features.md`（索引行投影，非整文件注入） | FR-014, FR-015 |
| `session` | `read` \| `unavailable` | 本次会话上下文 | FR-014, FR-015 |

不变量：来源清单只列 `read` 的来源；`unavailable` / `not-read` 必须在 `## Risks & Limits` 声明缺失
（FR-015）。读取按摘要优先——注册表取行投影，治理文档取相关段落，不整文件注入。

---

## E7 HumanReport — 五节报告

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `carrier_marker` | `mode: subagent` \| `mode: in-session-degraded` | 五节之前的一行元数据；恰一个 | FR-011, FR-018 |
| `migration_hint` | literal \| null | 裸文本调用时为固定整句；非裸文本为 null | FR-005（A4） |
| `sections` | 有序五节 | 标题逐字：`## Conclusion` / `## Key Changes` / `## Evidence` / `## Risks & Limits` / `## Next Steps` | FR-018, STR 表 |
| `verdict` | `success` \| `partial` \| `failure` \| `aborted` \| `needs-confirmation` | 报告口径的总结论；由 E5 `status` 映射 | FR-019 |
| `dispatch_count` | int | `## Evidence` 的派发记录行：只计 humanize 发起的顶层派发 | FR-007 |
| `language` | `zh` \| `latin` | 正文语言：指令优先，治理回退 | FR-018（语言条） |
| `sources` | string[] | `## Risks & Limits` 内的实际读取来源清单 | FR-015 |

### E5 → E7 的 verdict 映射（封闭）

| E5.status | verdict |
|-----------|---------|
| `completed` | `success` |
| `partial` | `partial` |
| `failed` | `failure` |
| `aborted` | `aborted` |
| `needs-confirmation` | `needs-confirmation` |
| `not-an-action` | `success`（结论文案为「未执行任何动作」，不称执行成功） |

映射是单向的：`verdict` MUST NOT 被上调（`partial` 不得写成 `success`），也不得因表达层需要被下调
（FR-019, FR-012）。

---

## E8 ReportOutput — 显式输出目标

| 字段 | 类型 | 语义 | 来源 |
|------|------|------|------|
| `target` | path \| null | `--output` 目标；null = 不写 | FR-024 |
| `content` | `full-report` \| `rewritten-text` | run mode 写完整五节报告；content mode 只写改写文本 | FR-024 |
| `extension` | `.md` \| `.markdown` \| `.txt` | run mode 的封闭扩展名集 | FR-024 |
| `force` | bool | 目标已存在时必需 | FR-024 |
| `write` | `atomic` \| `rejected` | 临时文件 + 原子重命名；失败即拒绝且不留部分文件 | FR-024 |

不变量：run mode 下 `--output` 写的是与 `target` 内容一致的完整报告，并在会话回显一份摘要；
摘要不是报告的第六节，也不得替代报告。

---

## 校验规则（V-01…V-26）

| ID | 规则 | 依据 |
|----|------|------|
| V-01 | 同一 argv 序列 MUST 得到同一 E2 判定（不依赖模型对内容的猜测） | FR-006 |
| V-02 | 内容源与非空指令同现 MUST 拒绝并点名两者，优先于任何「内容优先」猜测 | FR-002 |
| V-03 | 既无内容源也无非空指令 MUST 拒绝并给用法与迁移提示 | FR-003 |
| V-04 | 语气取值域与拒收语义 MUST 与既有契约逐字一致 | FR-004 |
| V-05 | 裸文本调用 MUST 输出迁移提示整句，且只输出一次 | FR-005 |
| V-06 | run mode 每次调用 MUST 恰好一次顶层派发 | FR-007 |
| V-07 | 派发 MUST 经既有 run-agent 载体；MUST NOT 引入第二套派发机制 | FR-007（A5） |
| V-08 | 载体标记 MUST 恰一个，且与真实载体一致；降级不得冒充子代理 | FR-011 |
| V-09 | humanize MUST NOT 代答、跳过或自动完成指令自身的确认 | FR-008 |
| V-10 | 需确认却无法询问时 MUST 停在该步，记录卡点，其余已完成部分照常报告 | FR-008（clarify） |
| V-11 | 失败 MUST NOT 自动重试；每次运行至多一次执行尝试 | FR-010 |
| V-12 | humanize 自身 MUST NOT 联网或引入外部服务/模型 API | FR-010 |
| V-13 | 指令自身产生的联网与写入 MUST 在报告中披露 | FR-010, FR-024 |
| V-14 | 失败/中止 MUST 记录坐标与已完成部分，MUST NOT 叙述为成功 | FR-012 |
| V-15 | 指令 MUST 按原文与其所属契约执行，MUST NOT 被替换为简化流程 | FR-013 |
| V-16 | 报告前 MUST 装配三类上下文，且按摘要优先读取 | FR-014 |
| V-17 | 来源清单 MUST 只列实际读取的来源；缺失项 MUST 在 `## Risks & Limits` 声明 | FR-015 |
| V-18 | 上下文补全 MUST NOT 引入新事实、新数字、新来源或新因果 | FR-016 |
| V-19 | 保真底线 MUST 在报告与旧内容模式同时生效 | FR-017 |
| V-20 | 五节 MUST 按序齐备，标题逐字；正文语言按「指令优先、治理回退」 | FR-018 |
| V-21 | `## Evidence` 的每条关键结论 MUST 带可定位指针；无可报告输出写 `none` | FR-020 |
| V-22 | 无已知风险时 MUST 显式写「无已知风险」/`no known risks`，该节不得省略 | FR-021 |
| V-23 | 旧内容模式 MUST NOT 派发、MUST NOT 生成五节、`--output` 只写改写文本 | FR-023, FR-024 |
| V-24 | 注入防护 MUST 在两种模式下同时生效 | FR-025（FR-029 溯源） |
| V-25 | 并发与嵌套 MUST fail-closed，并点名冲突运行/路径/字面量 | FR-030 |
| V-26 | Feature 062 状态 MUST 保持 `Implemented`，扩展只追加记录 | FR-029 |

---

## 与既有模型的关系

- 062 的 `data-model.md`（8 实体 / 30 校验规则，内容模式）继续拥有内容模式的行为细则；本文件的 E2
  只拥有**模式路由**，不重述内容模式的输入核验、分段与四维改写。
- 本文件新增的落盘面只有 E4（临时占位，运行后消失）与 E8（显式输出，既有语义扩展）；没有数据库、
  没有新持久存储、没有新索引。
