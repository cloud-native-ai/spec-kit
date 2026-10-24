# Contract: 三项度量仪器（Measurement Instruments）

**Feature**: 069b（父 069） | **File scope**: `.specify/specs/069b-isomorphism-migration-metrics/notes/expression-baseline.md` | **FR served**: FR-014

- **C-1** 三项量与冻结点

三项基线 MUST 是：`gate_calls`（门禁调用次数）、`confirmations`（人工确认次数）、`wall_clock`（requirements→analyze 墙钟）。
冻结点 MUST 是本切片 `requirements.md` 的**首次提交**（`frozen_commit = f0df3d0b`，author date `2026-10-24`，实测
`git log --diff-filter=A --format='%h %as' -- .specify/specs/069b-isomorphism-migration-metrics/requirements.md`
→ `f0df3d0b 2026-10-24`；MUST NOT 用 `git log -1 --format=%as`——它取最近一次触及，2026-10-25 实测已返回 `2026-10-25`，且不输出提交哈希）。
三项 MUST 共用同一起点，MUST NOT 各取各的起点。

（FR-014）

- **C-2** 仪器封闭：只用既有通道

三项量 MUST 只取自下列四个既有通道，MUST NOT 新增采集器、MUST NOT 插桩、MUST NOT 手工补采：

| 量 | 通道 | 命令（本阶段实跑） |
|----|------|--------------------|
| `gate_calls` | exec-quant 运行记录（068 通道） | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json` |
| `confirmations`（门控观察） | feedback 条目 frontmatter | `python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json`，逐条查其文件是否带 `lifecycle_point: gate-*` |
| `confirmations`（clarify 轮次） | 本切片 `requirements.md` § Clarifications | 仅当存在本切片的 `/speckit.clarify` 运行记录时：`grep -c '^- Q:' <requirements.md>`；无记录或自裁决 Q/A 记 0（C-4） |
| `wall_clock`（终点） | 运行判定记录 | `python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json` |
| `wall_clock`（起点） | git 首次提交的 author date | `git log --diff-filter=A --format='%h %as' -- <requirements.md>` |

068 通道的 owner 是 `.specify/specs/068-exec-quant-feedback-channel/`；本契约只引用，不重定义其记录语义。

（FR-014）

- **C-3** `gate_calls` 的过滤集合事先冻结

`gate_calls` 的过滤集合 MUST 在冻结点写成封闭的单元 id 列表，本切片取
`{/speckit.checklist, /speckit.analyze, /speckit.review, skill:create-checklist, skill:analyze-artifacts, skill:review-sdd-process}`。
计数 MUST 是该集合在记录窗口内、且 `run_id` 含切片键 `069b` 的记录条数（unit 粒度）。收尾复测 MUST 使用同一集合与同一归属规则，MUST NOT 回选单元集。
脚本级检查（`pre-analyze-check.py` / `validate-requirements.py` / `doc-consistency-check.py` / 测试套件）不是 exec-quant 的
`unit_id`，其调用**不可按次计数**——这是已声明的仪器边界，MUST 在基线记录里写明，MUST NOT 当作 0。

（FR-014）

- **C-4** `confirmations` 的口径

`confirmations` MUST = （归属本切片的、带 `lifecycle_point: gate-*` 的 feedback 条目数）+（归属本切片的 clarify 提问轮次）。
两个分项 MUST 分别记录，MUST NOT 只记合计。
「归属本切片」的判据 MUST 是记录 `run_id` 含切片键 `069b`（或该次的 `feature_id = 069` 且 run_id 含 `069b`）；
父 Feature 与 069a 的历史记录 MUST NOT 计入。
clarify 提问轮次 = 该切片是否有 `/speckit.clarify` 运行记录：无则 `0`；有则取其写入 `requirements.md § Clarifications`
的 `- Q:` 行数。requirements 阶段的自裁决 Q/A 对（preamble 明写「未向用户发起访谈」）MUST NOT 计入——
它们不是向用户的提问。实测 0 时照记 0（实测值，不是缺省填充）。

（FR-014）

- **C-5** `wall_clock` 的口径

`wall_clock` MUST = `/speckit.analyze` 的运行判定记录时间戳（`determined_at`）− `requirements.md` 首次提交 author date。
两端 MUST 取同一时钟语义（日期级即可，`YYYY-MM-DD`）；终点记录不存在时 MUST 记 `null` + reason，
MUST NOT 用 `/speckit.review`、`/speckit.tasks` 或人工填的时间替代。

（FR-014）

- **C-6** 无样本记 `not-evaluated`

任一量无来源、或冻结值为 0 使降幅不可定义时，其判据 MUST 记 `not-evaluated`（附 reason），
MUST NOT 记 `0`、MUST NOT 记「达成」、MUST NOT 用绝对量冒充降幅。
「不足」MUST NOT 成为不冻结基线的理由：三项 MUST 在开工前落盘，落盘值可以是 `0` / `null` / 实测绝对值，
但**判据结论**必须如实写 `not-evaluated`。

（FR-014）

- **C-7** 与 `verification.md` 词表的语汇边界

`not-evaluated` 是**判据取值**，不是 SC 状态词。`verification.md` 的 SC 状态 MUST 仍取
`.specify/templates/verification-log-template.md` 拥有的词表（`pass` / `fail` / `partial` / `deferred` / `unknown`）。
两者对象不同：前者描述「这个量有没有样本」，后者描述「这条 SC 被验证到什么程度」。
MUST NOT 互相顶替、MUST NOT 收窄、MUST NOT 新增第六个 SC 状态词。

（FR-014）

- **C-8** 基线记录的形态

基线 MUST 落 `.specify/specs/069b-isomorphism-migration-metrics/notes/expression-baseline.md`，
每条一行，字段固定为：`quantity` / `frozen_value` / `frozen_at` / `frozen_commit` / `instrument` / `source_command` / `verdict`。
`verdict` 取 `not-evaluated` 或 `measured`——**不存在**「达成 / 未达成」这一层：降幅结论归 SC，不归基线记录。
记录 MUST 附一段「不可计部分」（C-3 的仪器边界）与一条可复算命令。

（FR-014）

- **C-9** 收尾对照使用同一仪器与同一集合

收尾对照 MUST 用与 C-2 相同的命令、相同的过滤集合（C-3）与相同的样本窗口；
MUST NOT 在收尾时改口径、改集合、改起点。若收尾时某通道不可用，MUST 记 `not-evaluated` + reason。

（FR-014）

- **C-10** 不得新增统计系统

本切片 MUST NOT 新建统计系统、评分体系、计量台账、dashboard 或第二份基线存储；
基线记录是**每特性一份**的 `notes/` dated 记录，属既有规格面，不构成运行时存储。

（FR-014）
