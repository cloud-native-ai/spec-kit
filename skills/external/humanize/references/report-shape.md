# Report shape — 五节报告（`/speckit.humanize` 运行模式的报告面）

**归属**: 本文件是运行模式报告面的行为细则所有者：元数据块、五个固定小节、逐节义务、语言与保真。入口解析、模式路由、派发、载荷与信封归 `references/run-mode.md`；`SKILL.md` 正文只声明分支边界，不复述这里的形态、字面量或义务。

**外部所有者**: 五个小节标题与契约面固定 literal（载体标记、`verdict` 行、派发记录键名、迁移提示整句）的 owner 是 requirements § Shared Strings；verdict 集合与 `status → verdict` 映射的 owner 是 requirements FR-019；来源三态（`read` / `not-read` / `unavailable`）的语义与判定 owner 是 FR-014；受保护集合的枚举 owner 是 FR-017（承 062 FR-007）；失败措辞的封闭词表 owner 是 requirements § Failure Wording — Closed Banned Vocabulary。本文件只固定形态与义务，不复制这些表。

---

## Metadata Block

五节之前 MUST **恰一条载体标记行**：`mode: subagent` 或 `mode: in-session-degraded`，二选一、恰一个，与该次运行的真实载体一致（判定与写入义务归 `references/run-mode.md` § Dispatch）。MUST NOT 冒充、MUST NOT 双写、MUST NOT 漏写。

- **裸文本调用**：该行之后 MUST 再加一条**迁移提示行**（整句 literal 的 owner 是 requirements FR-005，运行侧的落点与触发归 `references/run-mode.md` § Migration Hint）。提示行是调用级会话通知，只出现一次。
- **该块 MUST NOT 用标题、MUST NOT 构成第六节、MUST NOT 混入其他内容**——它不是五节之一，也不得被编号或加粗成小标题。它承载的是「这份报告从哪条通道出来」这一条事实，不是叙述段落。
- 写入 `--output` 文件时，迁移提示行按 FR-024 省略；载体标记行仍须在五个 H2 之前保留（文件面的义务归 RP-19）。

## Sections

报告 MUST 恰含五个 H2 小节，顺序固定、标题**逐字**、**不加编号**、**不翻译**、不合并（下列清单的序号只是本文档的枚举序号，不进入报告）：

1. `## Conclusion`
2. `## Key Changes`
3. `## Evidence`
4. `## Risks & Limits`
5. `## Next Steps`

**缺任一小节即不合格**；五节之外 MUST NOT 再加第六个 H2 小节（会话回显的 `--output` 摘要同样不是第六节）。标题字面量的 owner 是 requirements § Shared Strings——本清单是消费方，不是所有者；改标题 MUST 改所有者，再回到这里。

- **报告由 humanize 主会话撰写**；执行体 MUST NOT 写最终报告——执行体只回传结果信封（`references/run-mode.md` § Envelope）。撰写者与执行者是两个角色：报告里 MUST NOT 出现**以执行体身份的自述**（「我执行了…」「我跑了…」），执行结果一律以第三人称的证据指针表述。
- **默认零写入**：无 `--output` 时报告只在会话内呈现，MUST NOT 写隐式副本、MUST NOT 写到默认位置、MUST NOT 创建报告文件。只有显式 `--output` 才写入该路径；会话另回显一份摘要，摘要不替代报告。
- 五节内部的义务逐节定义在 `## Conclusion` … `## Next Steps`；本节的职责只是固定「有几节、叫什么、什么顺序」。

## Conclusion

结论 MUST **先于一切细节**给出可直接行动的总判断：它是报告的第一节，也是读者只读一节时得到的全部收获。

- **首行 MUST 是 `verdict: <token>` 形式的机器可判定行**（键名的 literal owner 是 requirements § Shared Strings）。token MUST 恒为**英文原样**，其后的正文 MUST 用**报告语言**写出对应措辞，并给出一句可直接行动的理由（为什么是这个判断、卡在哪、下一步看哪）。
- token 的封闭集、每个 token 的报告语言措辞与 `status → verdict` 的单向映射，唯一 owner 是 requirements FR-019；本文件不复述枚举，也不得在此增删取值。token MUST NOT 被上调或下调。
- `status=not-an-action` 的结论文案 MUST 是「未执行任何动作」，MUST NOT 被写成「执行成功」——它映射到的 verdict 只表示「没有失败」，不表示做成了什么。
- 失败时 MUST NOT 使用成功措辞：verdict 为 `failure` / `aborted` 的报告，其结论正文受 requirements § Failure Wording — Closed Banned Vocabulary 的封闭词表约束（词表与匹配规则 owner 在该节，本文件不复制）；「部分完成」「未执行任何动作」一类如实表述是允许的。
- 需确认而无法取得答复时，结论写明「需要确认，未获答复」与卡点；用户明确拒绝时写明「用户拒绝确认」与未执行范围（措辞义务的 owner 是 `references/run-mode.md` § Confirmation Missing 与 § Envelope）。

## Key Changes

关键变化 MUST **按影响降序**排列：读者先看到对自己影响最大的那条。

- 排序依据是 requirements FR-019 的**封闭影响尺**（owner 是该 FR；本文件不复述档位）；同一档并列时 MUST 按文件路径**字典序**——MUST NOT 引入其他排序依据（「我最先做的」「改动行数最多」「执行顺序」都不合格）。
- **无变化时也必须占位**：没有关键变化时 MUST 明写「无变化」，MUST NOT 留空、MUST NOT 省略该节。
- **指令造成的写入在此可见**：回传信封的 `products` 逐项落进本节（humanize 自身除显式 `--output` 外不写文件）；写入归入哪一档按影响尺判定，不按文件数量或行数判定。
- 每条变化 = 一句结论 + 一个指针（指针形态与义务见 `## Evidence`）；MUST NOT 只写形容词、「若干文件已更新」或「多处调整」。

## Evidence

证据节把每条关键结论接到可定位的坐标上：读者应当能照着指针自己复核，而不必相信报告的措辞。

- **每条关键结论配可定位指针**：`产物路径`（存在且可打开）、`命令与退出码`（命令原文 + 实际退出码）、`测试读数`（通过/失败计数及其来源）、或可定位引用（文件 + 小节或行号）。MUST NOT 只写形容词，也 MUST NOT 用「已验证」「测试通过」「一切正常」这类没有坐标的断言充数。
- **指令造成的写入逐项列出**：回传信封 `products` 的每一项都在本节出现一次，标明 created / modified；它与 `## Key Changes` 的条目对应，但比那里更细（路径逐条，不合并成「若干文件」）。
- **无可报告输出时写 `none`**：执行体 `status=completed` 且无输出无产物时，本节正文写成 `none`（literal owner 是 requirements § Shared Strings）；`none` 只替代证据指针与产物清单，MUST NOT 替代派发记录行——该行仍须出现。
- **一行派发记录**：本节 MUST 含一行 `dispatches:` 元数据（键名 owner 是 requirements § Shared Strings），值是 humanize 发起的**顶层派发**次数。计数口径的唯一 owner 是 `contracts/execution-dispatch.contract.md` EX-21：原生通道**成功路径恒为 1**，降级为 `0`；指令自身再发起的派发归属该指令单元，MUST NOT 重复计数。该行是派发与重试计数的唯一来源，散文叙述不作数。
- **核对不上的证据不进本节**：证据逐项核对可定位性（`references/run-mode.md` § Failure & No Retry 的对应条款）；核对不上的项 MUST NOT 作为证据出现，改记「未能核实」到 `## Risks & Limits`。

## Risks & Limits

风险节 MUST 列出四类内容：**风险**、**限制**、**未验证项**、**缺失上下文**。该节 MUST NOT 省略，也 MUST NOT 留空——「没有风险」本身也是必须写出的判断，而不是可以省掉的一段。

- **无已知风险时显式写出**：用报告语言明写该判断（英文报告为 `no known risks`，中文报告为「无已知风险」）；MUST NOT 删掉整节，也 MUST NOT 只留一个破折号或一个「无」字。
- **未验证项**：证据核对不上的项按「未能核实」列出；载体不提供的信号（如超时信号）在此声明为不可判——MUST NOT 用推断把空白填成结论。
- **缺失上下文**：本轮 `not-read` / `unavailable` 的治理来源与会话上下文在此逐项声明缺失，并说明它对哪些结论有影响（读者要能判断「这份报告少看了什么」）。
- **来源清单**：本节 MUST 含来源清单，**只列**本轮**实际读取**的来源（`read` 状态）；读取失败或未读取的来源 MUST 作为缺失项同节声明，MUST NOT 列进来源清单，也 MUST NOT 列出未载入却「看起来相关」的来源。`read` / `not-read` / `unavailable` 三态的语义与判定 owner 是 requirements FR-014；四件治理来源与会话上下文各自按上述三态登记，多源时逐条一行。