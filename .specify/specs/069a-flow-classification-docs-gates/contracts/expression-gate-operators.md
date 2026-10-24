# Contract: 文档型门禁算子集（Expression-Class Document-Form Gates）

**Feature**: 069a（父 069） | **File scope**: `shared/workflow/expression-gates.md`（owner）+ 接线点 `templates/commands/docs.md`、`templates/commands/humanize.md`、`skills/external/create-docs/SKILL.md`、`skills/external/humanize/SKILL.md`（只含指针） | **FR served**: FR-012、FR-013、FR-014、FR-018、FR-019、FR-020、FR-021、FR-022、FR-023、FR-024、FR-025、FR-026、FR-027

本契约钉住「六面 + 逐阶段算子 + 调用点 + 阻断级别 + 语法 + 基线协议」的**结构**；每面的判据正文归其单一 owner，本契约与门禁 owner 都 MUST NOT 复制。

- **C-1** 六面齐全且每面单一 owner

门禁集 MUST 覆盖六面：需求清晰度、读者/目的/边界、证据分级与 as-of、结构/链接/构建、事实一致性、评审。
每面 MUST 登记且仅登记一个 `owner_pointer`（路径 + 章节锚），该指针 MUST 在仓库中可解析。六面的 owner 指针为：

| 面 | owner_pointer |
|----|---------------|
| 需求清晰度 | `scripts/python/validate-requirements.py`（五项结构检查）+ `shared/guidelines/requirements-guidelines.md` |
| 读者/目的/边界 | `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 |
| 证据分级与 as-of | 本门禁 owner（本切片新增面） |
| 结构/链接/构建 | `skills/external/create-docs/SKILL.md` § Desired-State Baseline（执行体 `skills/external/create-docs/scripts/docs-utils.py`） |
| 事实一致性 | `shared/guidelines/one-source-of-truth.md` |
| 评审 | `skills/internal/review-sdd-process/SKILL.md` + `templates/review-template.md` |

同一面出现两个 owner_pointer → 失败（第二副本）。新增面之外，门禁 owner MUST NOT 复述这些 owner 的判据句。

- **C-2** 逐阶段算子表

门禁 owner MUST 含一张表，覆盖全部 8 个阶段：requirements → clarify → plan → tasks → checklist → analyze → implement → review。
每行 MUST 给出：阶段、执行算子（可执行入口或点名的既有流程）、对应面、阻断级别。
任一阶段无算子 → 失败；算子行不得为空表头行（反空真：行数 ≥ 8）。

- **C-3** 阻断级别不降

六面中任一面 MUST 至少有一个 `blocking` 算子——该底线的作用对象是**六面全集**（即 `/speckit.docs` 调用点及其文档型特性路径）。
不得因为「属表达类」把既有 P0/P1 判定降为 advisory；不得把本门禁集表达为「更宽松的通道」。
需求清晰度、事实一致性、评审三面 MUST 各至少一个 `blocking` 算子；读者声明缺失 MUST 阻断（FR-019），不是警告。
`/speckit.humanize` 调用点只执行最小算子集（C-14），**不继承**六面的阻断底线，也 MUST NOT 被读作把六面降级——它是另一条调用点行，不是同一集合的子集声明。

- **C-4** 读者声明形态

文档型交付物 MUST 在其前 40 个非空行内声明两行：`**Readers**: ...` 与 `**Reading scenario**: ...`。
两行任一缺失或值为空 → `reader-declaration-missing`（阻断）。
读者判定 MUST 沿用 `user-facing-comprehension.md` § 基准读者与覆盖协议 的基准读者，MUST NOT 新建第二套读者定义；本地覆盖按该 owner 的协议声明。

- **C-5** 证据等级与 as-of 语法

证据等级取封闭三值：`实测` / `推断` / `引用`。`as-of` 取 `YYYY-MM-DD`。
配对规则：一条事实性断言只要出现等级或 `as-of` 任一，另一项 MUST 同时出现。
语法校验 MUST 由 `doc-consistency-check.py` 的 `evidence` 面执行（§ `doc-consistency-checker.md` C-3）。
本面的**对象**是文档断言；`shared/workflow/evidence-step.md` 的七态与 `shared/guidelines/single-run-evidence.md` 的记录留存 MUST NOT 被本面重定义、收窄或并入。

- **C-6** 结构/链接/构建只是必要条件

结构、链接、构建通过 MUST NOT 被援引为内容正确性的证据；门禁 owner MUST 含这一负向条款。
结构面判据 MUST 写成「零**新增**违规」：既有基线（2026-10-24 实测 `violations=3`：`broken-link` 2 + `note-frontmatter` 1）不因本特性被继承为失败，也不因本特性被顺手修复。
站点层不存在时，构建算子记为 `not-applicable`（显式），不得记为通过。

- **C-7** 事实唯一性与修复方向

同一事实 MUST 只有一个所有者并以引用表达；≥2 处手写即缺陷（FR-022）。
修复方向 MUST 是「改为对唯一 owner 的引用」，MUST NOT 是「把多处措辞改到一致」。
派生计数 MUST 由制品导出；手工计数 MUST 由既有计数判定（`pre-analyze-check.py`）报出，本门禁集 MUST NOT 自建第二套计数规则。

- **C-8** 评审按读者基准

表达类的评审 MUST 保留且 MUST 按声明的读者基准判定（C-4），MUST NOT 复用代码评审的判定对象（编译/测试/覆盖率），MUST NOT 由分类免除。
评审面 MUST 至少一条 `blocking` 算子，且在 analyze 与 review 两个阶段都在场。

- **C-9** 三项基线的冻结与对照

表达类特性 MUST 在开工前冻结三项实测基线（门禁调用次数、人工确认次数、requirements→analyze 墙钟），收尾逐项对照；基线缺失 → 不可验收（FR-024）。
记录形态见 `data-model.md` E8；三项值 MUST 来自既有通道，MUST NOT 新增采集器：

| 量 | 既有通道（实测可用） |
|----|---------------------|
| 门禁调用次数 | `exec-quant.py --action list-records --since <ISO> --format json`（按声明的门禁单元集过滤计数） |
| 人工确认次数 | 门控观察记录（`feedback-utils.py --action record --lifecycle-point gate-*` → `--action list`）+ clarify 提问轮次 |
| requirements→analyze 墙钟 | `git log -1 --format=%cs -- <requirements.md>` 的首次提交 author date → `/speckit.analyze` 的运行判定记录时间戳 |

任一量无来源时记 `null` + `reason`，MUST NOT 记 0、MUST NOT 记达成。仪器口径与 `not-evaluated` 降级的规范条款归 069b（父编号 041）。

- **C-10** 算子去重（更少但更准）

同一算子在**同一次产物变更**上 MUST 只跑一次：requirements 未变更时，clarify 后 MUST NOT 重跑需求面全量校验；plan/tasks 的结构检查 MUST 由 `pre-analyze-check.py` 一次承担，MUST NOT 在各阶段手工重做同一比对。
表达类 MUST NOT 继承代码型算子（测试执行、编译、覆盖率）；除非该特性确实产出代码或站点（此时按产出物补回，并在基线记录中说明）。
去重 MUST 不减少面数与阻断级别（C-1/C-3）。

- **C-11** 阶段完整性不读类别

门禁集 MUST 声明：阶段完整性由既有阶段记录判定，类别 MUST NOT 参与该判定；analyze 与 review 的调用率 MUST 为 100%。
任何以「本流程属表达类」为由跳过、缩短或改判阶段的请求 MUST 被拒绝——该拒绝规则 MUST 在门禁 owner 中有一条明文，且 MUST NOT 附带例外。

- **C-12** 首批成员只补强、不削弱

`/speckit.docs` 与 `/speckit.humanize` 的既有门禁 MUST NOT 被本门禁集削弱；只允许按 C-1…C-11 补强，且补强形态**封闭**为
各自入口的最小接线（C-14/C-15）：命令模板与技能只出现 lookup 调用与 owner 指针，不出现算子表副本、不改写既有行为。
本切片 MUST NOT 新增 `/speckit.*` 命令；062 的保真底线、默认零写入与报告契约 MUST 原样保留。

- **C-13** 与其他轴的边界

门禁集 MUST 声明与复杂度轴（决定 wrap-up 面有无，owner：`shared/workflow/feedback-step.md`）正交：本门禁集选择算子，复杂度轴决定是否有 wrap-up 面，两轴 MUST NOT 互相推导。
`shared/workflow/feedback-step.md` 只需一行指针指向分类 owner，MUST NOT 在该文件中复制判据或台账。

- **C-14** 命令/技能调用点表（call-site registry）

门禁 owner MUST 含一张调用点表，回答「哪个入口、在什么阶段、执行哪些算子、阻断与否」。本切片的行集合固定为：

| 调用点 | 时点 | 类别读取 | 执行算子 | 阻断 |
|--------|------|----------|----------|------|
| `/speckit.docs`（W1） | `## Outline` 内、目标声明协调与分派之前 | `flow-class-check.py --action lookup --unit-id "/speckit.docs"` | 六面：需求清晰度（`validate-requirements.py`，规格面存在时）· 读者/目的 + 证据/as-of + 事实一致性（`doc-consistency-check.py --action verify` 的 `reader` / `evidence` / `duplicate` 三面；`count` 面委派 `pre-analyze-check.py`）· 结构/链接/构建（`docs-utils.py --action validate`，零新增）· 评审（既有 `/speckit.review`） | 每面 ≥ 1 blocking（C-3） |
| `skill:create-docs`（W3） | Reconcile Loop 的 R6 verify + Authoring Flow 的 R6 验证（两处） | 沿用调用方已解析结果；无调用方（standalone）时不新读 | 读者/目的 + 证据/as-of + 事实一致性 → `doc-consistency-check.py --action verify`（对受触文档）；结构/链接/构建 → `docs-utils.py --action validate` | blocking：发现即报告并阻止「收敛完成」结论 |
| `/speckit.humanize`（W2） | `## Outline` 内、委派技能之前 | `flow-class-check.py --action lookup --unit-id "/speckit.humanize"` | 最小集（**不按六面登记**，归属 062 域）：`062-stage6-fidelity`（受保护内容与事实逐字不变）· `062-stage6-entailment`（不新增输入未蕴含的断言）· `062-stage5-audience-report`（语气/受众应用与限制报告）· `062-reviewer-report`（调用者复核会话报告：冲突/未处理项/注入提示） | `062-stage6-fidelity` 与 `062-stage6-entailment` blocking；其余为 062 既有报告义务 |
| `skill:humanize`（W4） | Stage 6 保真自检 + Stage 7 报告 | 沿用调用方解析结果（不新读） | 同上一行；执行细则由 `skills/external/humanize/SKILL.md` 承载，owner 只登记调用点、算子名与阻断级别 | 同上 |

规则：
- 本表是「入口 → 阶段 → 算子」的**唯一登记处**；命令模板与技能 MUST NOT 复制本表，只可出现 lookup 调用与本文件（门禁 owner）指针。
- `docs` 行 MUST 含 `doc-consistency-check.py --action verify`；`humanize` 行 MUST NOT 出现六面全集（尤其 MUST NOT 出现 `structure-links-build` 与 `requirements-clarity`——一次改写没有这两个面的对象），且 MUST NOT 被表述为「六面的子集/精简版」。
- 面名（`reader-purpose` / `evidence-asof` / `structure-links-build` / `fact-consistency` / `review` / 需求清晰度）沿用 C-1 的六个 face id；`062-*` 是 humanize 域的算子名，不是第七面，MUST NOT 被六面表吸收。
- 新增调用点属契约变更（须同步 `flow-class-ledger.md` C-15 的接线封闭集），MUST NOT 由模板或技能自行扩面。

- **C-15** 调用点执行时机与降级

1. lookup MUST 先于该入口的任何门禁判定执行，且同一次运行只执行一次（同一产物变更不重复读取）。
2. 降级一律可见：`source: default` → 原样显示固定标记（未声明·按默认）；owner 不可解析或引擎缺席（文件不存在 / 退出码 2）→ 显示 `owner-unavailable`，
   并**保持既有门禁不变**；MUST NOT 中断流程、MUST NOT 静默切换门禁集、MUST NOT 把降级当作通过。
3. 无调用方的技能运行（独立调用）不新读类别；按默认处理并在输出中带同一标记。
4. 接线 MUST NOT 造成算子重复执行：命令与技能在同一个产物变更上重叠时（如 `/speckit.docs` → `create-docs` R6 都跑 checker），以一次执行为准并复用其输出（C-10 去重纪律）。
5. 接线 MUST NOT 改变判定阈值、阶段集合或 P0/P1 定义——它只决定「用哪套算子证明同一不变量」。
