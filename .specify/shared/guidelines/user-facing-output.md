# 面向用户输出维护(User-Facing Output Channel)

> **Single Source of Truth**: 本文档是框架「面向用户输出」**呈现机制**的唯一定义处，拥有四件事：① 通道归属（谁写用户面输出）；② 回显命令类（判据与机器可读标记）；③ 呈现边界（何时发出）；④ 稳定包封（以什么形状发出）与「工具结果不是用户面输出」的重发规则。其余全部按指针抵达：措辞与上下文归 `.specify/shared/guidelines/user-facing-comprehension.md`，内容与节奏归 `.specify/shared/guidelines/reporting-obligations.md`，各命令的内容与上限归其自身的契约与引擎。任何命令、技能或代理引用本机制时 MUST 以路径引用本文档，MUST NOT 复制其条件集、标记语法或包封字面量。

**本机制防的失效是「命令输出了，但用户没看到」**：在 superagent 会话里，子代理活动、长工具结果与推理流占满可见面；回显命令（输出即产品的只读命令）的产物要么落在被宿主折叠的工具结果里，要么被一句摘要替代。读者看到的不是命令的答案，而是执行者的叙事。本机制只治理**呈现**：它不改变命令内容，不新增第二渲染器，也不接管任何既有 owner 的规则。

**与其他纪律的边界**：面向用户的**措辞与上下文**由 `.specify/shared/guidelines/user-facing-comprehension.md` 统一定义；周期汇报、摘要内容与上限由 `.specify/shared/guidelines/reporting-obligations.md` 拥有；命令的退出码与内容由各命令契约拥有。本文档**不是**一个新的消息类，也**不是**一个新的措辞类——它只回答「谁在什么时刻、以什么形状，把命令的既有产物呈现给用户」。

## 通道归属 (Channel ownership)

- **唯一写者**：只有**持有用户会话的根执行体**（root）写用户面输出。子代理的 stdout、progress、return 是**输入**，不是输出；父边组合后才成为用户面内容。角色的判定只由派发边决定，owner 为 `.specify/shared/definitions/superagent-definitions.md`。
- **既有载体**：用户面输出的载体是既有的 **live console**（`reporting-obligations.md` § 八 已声明的两种载体之一）。本机制**不新增控制台通道**、不新增第二载体、不新增通知服务。
- **无新存储**：包封在消息内组合，不落盘、不排队、不建缓存、不建索引。呈现边界由执行体自己的步骤边界产生，不引入定时器、守护进程或调度器。
- **子代理静默**：子代理的流产物留在其既有产物路径（artifact triplet / 运行报告 / 宿主原生渲染）；根执行体 MUST NOT 把子日志逐字镜像进用户面。既有的周期汇报行与最终报告不受本机制削减。

## 回显命令类 (Echo command class)

**判据（三条同时成立，缺一不是）**：

1. **产物是既有状态的有界投影**——只读，不改变状态；
2. **渲染由确定性引擎或声明程序拥有**——命令自身不携带渲染逻辑；
3. **输出回答用户的问题**（「是什么 / 做了什么」），而不是报告自身执行的动作、征求同意或发起提问。

**机器可读标记（成员资格的唯一声明）**：满足判据的命令或模式 MUST 在其模板/技能正文携带规范标记：

- 整条命令：`**Output class**: echo`
- 某一模式：`**Output class (<mode>[, <mode>…])**: echo`

标记行 MUST 与 owner 指针同处（同一文件内出现 `user-facing-output.md`）。成员集合就是携带标记的集合；初始集合由契约测试 `tests/contract/test_user_facing_output.py` 钉死，新增回显命令在同一变更中补标记并更新该测试。典型成员：现状摘要（digest/guard）、测量摘要（summary）、team/goal/anchor 的 view、tools 的 view/list、todo 的 list、agents 的无参列表。**机器通道**（如 `--format json`）不是回显输出，不套包封；单行状态汇报（如 status 的 `report` 动作）归 `reporting-obligations.md`，不套包封。

## 呈现边界 (Presentation boundary)

- **不在子代理爆发中发出**：当子代理活动正在发出、或当前步骤内有未结算的子返回时，回显命令 MUST NOT 中途呈现；在下一次**步骤边界**发出。边界是执行体自己的步骤边界，**不是**时钟、不是定时器、不是队列。
- **块即窗口末块**：包封块是本次呈现窗口的**最后一个用户面块**；块之后最多再有一条说明（见「子代理静默与工具结果重发」），MUST NOT 再用大段叙述覆盖它。
- **提前执行只算内部结果**：若命令因内部原因提前执行，其原始输出不是用户面答案；执行体在边界以包封重发同一 stdout。**不引入缓冲、队列或存储**——重发所需的文本来自本次会话上下文。
- **多命令**：同一窗口内多个回显请求按请求顺序各发一个包封；最后一个包封仍是窗口末块。

## 稳定包封 (Stable envelope)

回显命令的用户面产物 MUST 包在下列稳定包封中（字面量只在本节定义一次，其他位置只引用本节）：

```
[user-output:begin] command=<command> action=<action> exit=<code> attribution=<attribution> generated=<UTC ISO-8601>
````text
<engine stdout, verbatim>
````
[user-output:end] command=<command>
```

字段：

| 字段 | 含义 |
|------|------|
| `command` | 用户命令名（如 `/speckit.status`） |
| `action` | 动作或模式（如 `digest` / `view` / `list`）；无则 `-` |
| `exit` | 引擎退出码，取值域归命令自身契约（`0` 成功、`3` 无人在跑等语义不变） |
| `attribution` | 有运行身份时 `structure=<slug> run=<stamp>`；否则 `workspace=<path>` |
| `generated` | 优先取引擎报告的生成时间（如 status 摘要首行）；否则取本次调用的 UTC 时间 |

**正文规则**：围栏内是命令的 **stdout**，MUST 逐字保留——不增删行、不重排、不改写；围栏只是呈现（让 Markdown 宿主保持等宽对齐），不改变正文。**stderr 与错误导航在正文之外**：命令的降级说明、错误提示、下一步建议写在包封之后，MUST NOT 混入正文。退出码非零不是失败的同义词（如 `3` = 显式「无人在跑」），包封照常发出并如实写 `exit`。

## 子代理静默与工具结果重发 (Child silence and re-emission)

**工具结果不是用户面输出**。宿主可能折叠长工具结果（真实案例：`… +157 lines (Ctrl+O to expand)`），执行体 MUST NOT 把「工具结果里已经有」当作已呈现。规则：

1. 执行体 MUST 把引擎的 **stdout 作为自己的消息**在包封内逐字重发；工具调用结果、子代理返回、日志片段都不构成呈现。
2. MUST NOT 用「已在上方」「见工具输出」「已逐字呈现」一类句子代替正文；这类句子不满足呈现义务。
3. 先发**完整包封块**（含全部组/条目），再发降级说明或摘要；说明与摘要 MUST NOT 替代、删减或重排正文。真实案例中六组信息被摘要替代，即为违规。
4. 子代理日志与流留在其产物路径；用户面最多保留既有的周期汇报行（归 `reporting-obligations.md`）与对产物路径的指针。
5. 虚拟模态下子代理的工作发生在会话内，其叙述同样不是用户面输出；根执行体只呈现组合后的包封与说明。

## 有界呈现 (Bounded presentation)

- **正文逐字，不重排/不截断**：执行体 MUST NOT 为了「好看」改写命令输出；宽度与条目上限由命令引擎的既有边界拥有（如 `--cap`、`--element-bound` 的声明默认值）。
- **不新增第二格式**：本机制不引入 compact/full 之类的第二人读格式。status 摘要的「单一人读格式」裁定（2026-11-10）与 view-team 的「不加第二格式」约束保持有效；包封是呈现外壳，不是第二渲染器。
- **不新增第二渲染器**：包封由执行体在消息内组合；命令引擎仍是其内容的唯一渲染者。第二个 parser / renderer 是缺陷。

## 范围限制 (Scope limits)

本机制 MUST NOT 引入下列任何一项——这是**禁令**，由变更文件集与契约测试判定：

- **不新增控制台通道**：只治理既有 live console；不新增第二载体、通知服务或输出端点。
- **不新增存储**：不新增持久化根、缓存、队列、索引或台账；包封只在消息内组合。
- **不新增第二渲染器**：命令引擎仍是唯一渲染者；包封不是第二个 parser/renderer。
- 不引入调度器、守护进程、定时器服务、第二注册表或第二状态脊。
- **不是消息类、不是措辞类**：本文件拥有呈现；包封头与说明文字的措辞与上下文仍按 `.specify/shared/guidelines/user-facing-comprehension.md` 判定，内容与节奏仍归 `reporting-obligations.md` 与各命令契约。
- **不是审批请求**：包封是单向陈述，不等待回应，也不授权任何动作。
- 子代理静默不削减既有的汇报义务；周期汇报、摘要上限、停滞判定与退出码语义全部保持原 owner。

## 观察约定

收尾反馈自省 MAY 记录本机制的违规观察。观察条目 MUST 内嵌稳定字面标记 `user-facing-output`，供既有反馈引擎按标记检索聚合。三条红线与 `token-efficiency` 先例相同：干净运行 MUST NOT 追加空洞观察；MUST NOT 编造计数；此为纯观察，MUST NOT 阻塞宿主流程或追加提问。
