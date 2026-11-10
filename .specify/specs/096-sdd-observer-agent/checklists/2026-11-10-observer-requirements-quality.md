# Observer Requirements Quality Checklist: sdd-observer agent

**Purpose**: 对 096 的**需求文本**做质量判定——观察者生命周期的可判定性、`journal.md` 客观性是否可机判（禁止评价 / 建议的判定）、内部 subagent 的读域与只读边界、掉线不阻塞的失败语义、以及与既有报告 / 摘要契约的边界。本清单只测试需求写得对不对，不测试实现行为。
**Created**: 2026-11-10
**Feature (Requirement Scope)**: Feature 096 SDD 专用观察者与线级观察记录（`.specify/features/096.md`）
**Requirements (What)**: `.specify/specs/096-sdd-observer-agent/requirements.md`
**Specifications (How, context only)**: `plan.md`、`contracts/`、`data-model.md`、`tasks.md`——仅用于暴露需求缺口，不作为评分对象

**Note**: 深度 Standard / 读者 Reviewer / 焦点五簇（生命周期可判定性、客观性可机判、subagent 读域与只读边界、非阻塞失败语义、报告与摘要契约边界）。同作者条件成立：缺口检测由三路 fresh-context 只读 subagent 分域完成（生命周期与失败语义 / journal 客观性 / 角色与边界），本文件由主会话合并与编号，无独立校验轮（本命令为单轮检测，逐项追溯性即本地替代门）。

## Requirement Completeness

- [ ] CHK001 - `U2 派发` 与 `line 已登记` 是否有可观测谓词（owner 文档 + 判定动作），使 FR-005 的「唯一机械判据」不依赖未定义术语？ [Completeness, Req §FR-005; A3]
- [ ] CHK002 - `spec key` 是否有派生来源与唯一性范围的定义，使 FR-004 的身份函数 `line_id + spec key` 可求值？ [Gap, Req §FR-004]
- [ ] CHK003 - 关闭开关 `observer: on|off` 的入口声明载体、位置与解析格式是否已定义（「入口声明」本身由谁拥有）？ [Gap, Req §FR-023]
- [ ] CHK004 - 「自身执行运行产物」是否被枚举或按引用拥有，且 US4 AS1 的「审计实际写面」有测量规则——锁文件、游标、临时文件可被判为写面内或写面外？ [Gap, Req §FR-016; US4 AS1]
- [ ] CHK005 - 「留存类别」词表与「可解析」的判定（存在 / 类型 / 版本历史可达）是否被定义为受拥有的封闭集合，并覆盖收束与工作树清理后两个时点？ [Gap, Req §FR-014; A9]
- [ ] CHK006 - FR-013 的观测输入清单是否被声明为穷尽，并指名新增载体的 owner（含其他产物引入的 meta 包络）？ [Ambiguity, Req §FR-013]
- [ ] CHK007 - 「规格拥有信息面 / owner 拥有拼写面」的分界是否落成两侧各自可新增内容的封闭清单（含 `min_persistent` 这类语义项的归属）？ [Ambiguity, Req §FR-011; A8]
- [ ] CHK008 - `observer` 角色面是否在特性自身产物之外有单一 owner 定义点，使 FR-001 / FR-002 的边界可被独立核对？ [Gap, Req §FR-001, FR-002]
- [ ] CHK009 - `stage executor` / `reviewer` / `reporter` 三个席位是否都以可核对的角色面谓词按引用定义，使 FR-001 的 MUST NOT 对三者均可判定？ [Gap, Req §FR-001]

## Requirement Clarity & Quantification

- [ ] CHK010 - 「有界执行窗口」是否被量化（具体预算 / deadline 值或具名拥有参数），且「窗口到期」是否被命名为可观测状态？ [Clarity, Req §FR-007; A4]
- [ ] CHK011 - 「已结算」是否覆盖「执行崩溃且没有 `.status` 记录」的分支，且一个永不结算的记录对下一次派发的阻塞是否有界？ [Ambiguity, Req §FR-007]
- [ ] CHK012 - 收束「原因」是否取自声明的封闭词表或具名枚举字段，且满足 FR-020 披露义务的「一条记录」是否被唯一指名？ [Ambiguity, Req §FR-009, FR-020]
- [ ] CHK013 - `命令` 字段的可容许内容是否被约束（来源载体、字符集 / 长度），使评价或建议文本无法借一个被允许的文本字段进入条目？ [Clarity, Req §FR-011, FR-013]
- [ ] CHK014 - 「自由叙述条目」是否有需求层的结构定义（区别于「表格之外的段落」这一位置性判据），使 SC-004(c) 的反例不是循环判据？ [Ambiguity, US2 Independent Test, SC-004]
- [ ] CHK015 - 九类信息对每个事件类的角色是否已定义——哪些字段对哪类事件允许为 `-`（例如线级提交事件的 `阶段`）？ [Clarity, Req §FR-011]
- [ ] CHK016 - `事件时间` 的语义是否跨事件类一致，特别是 `observer-gap` 类由窗口导出而非载体提供的情形？ [Consistency, Req §FR-011, FR-013]
- [ ] CHK017 - 零长度缺口窗口（起止同一秒）是否被显式裁决（写入或抑制）？ [Ambiguity, Req §FR-013]

## Requirement Consistency

- [ ] CHK018 - 条目的信息类数量是否在 FR-011（九类）与 Key Entities（八类）之间一致？ [Conflict, Req §FR-011, §Key Entities]
- [ ] CHK019 - 缺口窗口的起止锚点在连续多个缺口与 `state=disabled`（无启动时间）两种情形下是否被一致定义？ [Consistency, Req §FR-013]
- [ ] CHK020 - 「不同线 MUST NOT 共享 journal」（FR-003）与按 spec 目录落一份 journal 的路径（FR-010）在「两条不同线指向同一 spec」时是否相容，该状态是否被排除？ [Conflict, Req §FR-003, FR-010]
- [ ] CHK021 - 当内层嵌套运行与外层运行解析到同一 spec 目录时，内外 observer 的边界以及「不承载 SDD 线的 team 运行」是否被定义？ [Conflict, Req §FR-021]
- [ ] CHK022 - 当多次执行写入不同状态（如 `failed` 后 `disabled` / `closed`）时，观察者记录的取值优先级是否已定义，使线终态的 `disabled` 与 `failed` 仍可区分？ [Consistency, Req §FR-023; A13]
- [ ] CHK023 - SC-005 的「被拒绝或串行化」是否与 FR-007（driver 侧不派发 + 引擎侧拒绝）相容，并收敛为恰一个可观测结果？ [Conflict, SC-005, FR-007]

## Measurability & Acceptance Criteria

- [ ] CHK024 - 对已写入条目的就地改写是否可由需求点名的判据检出（如逐行摘要或提交连续性），而非仅靠序号单调？ [Measurability, Req §FR-010]
- [ ] CHK025 - 「MUST NOT 以 driver 会话上下文 / 阶段提示词作为观测输入」是否有任何证据面，且「没有载体证据的事件 MUST NOT 被记录」是否按事件类绑定具名载体而可证伪？ [Measurability, Req §FR-013, FR-014]
- [ ] CHK026 - SC-003 的红腿是否以可观测、可复现的判据表述，而不是把「转红」寄托在对 driver 文本的结构扫描上？ [Measurability, SC-003]
- [ ] CHK027 - SC-006 的基线是否由具名、可复现的契约拥有（而非一次性本地采集），且「既有已派发 agent 语义」是否映射到可判定的具体界面？ [Measurability, SC-006, FR-017]
- [ ] CHK028 - SC-007 的触发是否以需求术语定义（哪些状态脊状态、哪几次执行构成被跳过的窗口），无需实现内部知识即可复现？ [Measurability, SC-007]
- [ ] CHK029 - FR-019 的「MUST NOT 复制其内容」是否被表述为可检出的谓词（逐字节相同子串 / 同一路径复现等）？ [Measurability, Req §FR-019]

## Edge Cases & Failure Semantics

- [ ] CHK030 - 重启为 MAY 时，若 driver 不重启或最终执行在终态失败，缺口记录的写入者与窗口终点是否被指名？ [Coverage, Req §FR-008, FR-013]
- [ ] CHK031 - 禁止成为门的集合是否以已定义术语枚举，且「observer 异常」是否被定义（启动失败 / 中途终止 / journal 缺失 / 关闭）？ [Coverage, Req §FR-020]
- [ ] CHK032 - 启动失败、中途终止、journal 写入失败、observer 启动前线即失败、driver 崩溃五种失败是否被分配到互不矛盾的记录载体？ [Consistency, Req §FR-009, FR-010, FR-013; Edge Cases]

## Boundary & Dependency Coverage

- [ ] CHK033 - 内部 subagent 的读域是否可枚举，并与 observer 继承同一封闭清单？ [Coverage, Req §FR-022, FR-013]
- [ ] CHK034 - FR-022 的三条禁令（in-process 并发承载、非串行执行、引用 / 加载 driver 技能）是否各自在具名能力面上有可检出属性？ [Measurability, Req §FR-022]
- [ ] CHK035 - 对 095 的非依赖是否被表述为具名检测词表的可判定断言，且未来「引用绑定」路径是否带有义务而非愿望？ [Measurability, Req §FR-002; A2]
- [ ] CHK036 - 「journal 不进阶段产物表」（A12）是否以带具名指涉与红腿的 FR 表述，而非只存在于假设？ [Gap, Req §A12]
- [ ] CHK037 - 「用户可见的汇报 / 提问 / 审批请求」是否是一个封闭且被指名的通道集合？ [Coverage, Req §FR-018]
- [ ] CHK038 - 「两个不同实例身份」是否由具名身份函数派生，且并行线场景是否覆盖同一仓库内的两条线（而非两个仓库）？ [Clarity, SC-005, FR-003, FR-004]

## Notes

- 勾选方式：`[x]` 表示该问题已在需求文本中得到满足；未勾选项应在 `/speckit.analyze`、`/speckit.clarify` 或 `/speckit.plan` 迭代中处置。
- 同作者条件成立（本线 requirements → clarify → plan → tasks 由同一无人值守代理链生成）；检测由三路 fresh-context 只读 subagent 按不相交 FR 区间分域完成，无独立校验轮，因此不报告降级率。
- 并发读数：requested=24（U0 声明）；effective=3（三路检测并行重叠）；effective_reason=representable unit set size 3（低于 slot cap 6 − verifier reserve 1 = 5）。
- 本清单只测试需求质量；`plan.md` / `tasks.md` / `contracts/` 仅用于暴露缺口。检测阶段两路独立报告出同一处八 / 九类矛盾（CHK018），已在需求原文核实。
