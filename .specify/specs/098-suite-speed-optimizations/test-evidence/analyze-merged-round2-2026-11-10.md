# Analyze Merged Report — 098-suite-speed-optimizations（analyze Round 2，2026-11-10）

- **Stage**: analyze（串行集成 · Round 2 · 修复后重过门；单轮重跑）
- **输入**: `test-evidence/analyze-findings-round2-W1.md`（requirements + checklists，22 条）、`analyze-findings-round2-W2.md`（plan / data-model / quickstart / contracts，5 条新 finding + 12 条 round-1 residue 再裁）、`analyze-findings-round2-W3.md`（tasks.md，9 条）
- **权威**: 本特性 spec 全目录 + `.specify/constitution.md`（v1.19.0）+ `.specify/skills/internal/analyze-artifacts/`（SKILL.md、`references/detection-and-severity.md`、`references/validation-and-report.md`）；判据 owner `.specify/shared/guidelines/test-execution-efficiency.md`
- **上游记录**: `test-evidence/analyze-merged-2026-11-10.md`（Round 1，58 条：1C/7H/37M/13L）、`test-evidence/analyze-repair-dispositions-2026-11-10.md`（8/8 C/H confirm + 修复落点）、`test-evidence/analyze-repair-gates-2026-11-10.txt`（修复后门禁读数）
- **性质**: 只读集成。未修复任何 finding；本阶段写入仅：本报告、`test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback，按派发纪律不提交）。
- **归属声明**: 三个 Worker 的检测结论原样保留；集成者只做确定性归并、跨制品聚类、C/H 锚点复核与 residue 记账。

## 0. Gate verdict 与 CRITICAL/HIGH 汇总

**Verdict: 未通过（FAIL）** —— 新增 1 条 CRITICAL（W1-01，open），0 条新增 HIGH。按 SKILL §9，CRITICAL MUST 在 `/speckit.implement` 前处置。

**两项声明分开陈述（cleared backlog ≠ clean rerun）**:

- **Round-1 C/H 后备箱已清空**：8/8 修复落点经本轮证据复核为 fixed（§2.2.1 逐条给出证据），W2-09 被 reject，0 条 round-1 C/H 仍 open。
- **本轮不是一次干净的 rerun**：修复后的全量重检在 requirements 域新发现 1 条 CRITICAL，且在 tasks 域发现 9 条修复引入/未收敛的 MEDIUM/LOW（W3-01…W3-09）。因此 headline verdict 不读作「ready to implement」。

| 严重度 | 新增条数 | 构成 | 处置要求 |
|--------|----------|------|----------|
| CRITICAL | 1 | W1-01（宪法冲突，validated） | 实施前必须处置；不可降级 |
| HIGH | 0 | — | — |
| MEDIUM | 17 | W1 ×10 · W2 ×3 · W3 ×4 | 不阻断；随建议 owner 收敛 |
| LOW | 18 | W1 ×11 · W2 ×2 · W3 ×5 | 建议性 |
| **新增合计** | **36** | 主表 36 行（≤50）；overflow 0 | — |
| **Round-1 residue** | **58** | fixed 11 · rejected 1 · deferred 46 | 见 §2.2 |

### 0.1 验证路径声明（显式披露，非静默）

- **路径**: 本轮唯一 CRITICAL（W1-01）的锚点复核由**串行集成者直接重读**完成（SKILL `validation-and-report.md` § 5.5 的 subagent-unavailable 直接重读形态）；未派发 fresh-context 验证波——本次派发 ① 明确把「C/H 先复核锚点再标 validated/proposed」交给串行集成者，且本轮 C/H 恰 1 条。
- **独立性**: 集成者不是 W1/W2/W3 检测结论的作者；但按严格标准，直接重读弱于 fresh-context 子代理。后续阶段若需要更严证据，可按同一 finding ID 重派验证波。
- **W1-01 不可降级**: 宪法冲突按 SKILL Input Contract 自动 CRITICAL 且不是 `downgrade` 候选；本复核只给出证据边界，不重新定级。

### 0.2 C/H 汇总与指针（1 条；validated，无 proposed）

| # | ID | 严重度 | 一句话事实 | 指针（worker 行 → 锚点） | 状态 |
|---|----|--------|------------|---------------------------|------|
| 1 | W1-01 | **CRITICAL** | FR-007 的缺省档以 `slow` 标记排除换取更快的缺省运行，SC-004 又以「缺省档墙钟 ≤ 全量基线 50%」作为 final 验收——正是宪法 XX / owner 禁止的「以标记排除换取数字下降」；修复后的 FR-021「MUST NOT 以该清单中的任何方式兑现任何 SC」与其自相矛盾，Overview「不改变测试覆盖的选择」不能自证 | `analyze-findings-round2-W1.md#W1-01`；`requirements.md` §Overview(L28)、§FR-007(L147)、§FR-021(L170)、§SC-004(L205)、§A3(L252) vs `constitution.md` §XX(L437–439)；`test-execution-efficiency.md` L74（默认排除一类标记即缩小 selection）、L80（同一选择锚点）、L93（标记排除换取数字下降，任何情形不可采纳） | **validated（direct re-read）** · open |

### 0.3 W1-01 证据边界（集成者直接重读，2026-11-10）

- **evidence_supported**: ① SC-004(L205) 的比较对象是「缺省档墙钟」对「implement 起点基线（同 runner 缺省并行、**全量选择**）」，要求 ≤50%——两侧选择集合不同；② FR-007(L147) 的实现手段就是缺省前置 `not slow` 标记排除；③ owner L93 把「用过滤条件、**标记排除**或去掉一整层测试来换取数字下降」列为**任何情形下**不可采纳；L80 要求效率比较「两次运行 MUST 覆盖同一个测试集合」；L74 明示「若某个选择范围（例如一类标记的测试）被默认排除，这已经是缩小 selection」；④ 宪法 XX L437–439 原文即「a faster run MUST NOT be bought by shrinking the selection…」；⑤ FR-021(L170) 禁止「以该清单中的任何方式兑现任何 SC」，与 FR-007/SC-004 的组合构成文本内自相矛盾；⑥ A3(L252) 把「缺省全量 + 显式 fast 档」记录为**被否决**的替代设计，证明设计侧已知该路径而未采用。
- **evidence_not_supported**: 未主张用户 Input 的「PR 默认 `-m "not slow"`」可以被本技能重解释消化（SKILL 规定宪法修订只能发生在 analyze 之外的显式更新）；未审计规格链外是否存在一次已批准的宪法修订（链内无此记录）；未把 SC-005（全量档 vs 全量基线，同一选择）并入冲突面；未评估「`slow` 成员全量档仍被完整运行」能否改变结论——owner 的「同一选择」锚点使该事实不能自证合规。
- **可退出路径（仅两条，供 owner 裁决）**: (a) 改机制——缺省全量 + 显式快档（A3 已列的被否决替代设计），并把 SC-004 改写为同选择比较；(b) 在 analyze 之外完成**显式宪法修订**（用户裁决）。MEDIUM/LOW 的任何修补不能关闭本条。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 输入读取 | 三份 round-2 worker findings（读域互斥：W1 = requirements + checklist；W2 = plan/data-model/quickstart/contracts（9 文件）；W3 = tasks.md） | 22 + 5 + 9 = 36 条新增 finding；W2 另携 12 条 round-1 residue |
| 确定性归并 | 本报告 §2 | 主表 36 行 + overflow 0；严重度不重评分 |
| C/H 锚点复核 | 集成者直接重读（§0.1、§0.3） | 1/1 validated；0 proposed；0 reject；0 downgrade |
| 覆盖核算（固定步骤，**未** `--freeze`） | `python3 scripts/python/account-clause-coverage.py .specify/specs/098-suite-speed-optimizations` | exit 2，`status: baseline-missing`（预期 pre-T002）；`claimed clauses 68`；`[fr-uncovered] pass — 27 of 27`；`[clause-unparsable] fail (107)`（全语料，含既有面）——完整输出：`test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt` |
| 决策张力（pass I 确定性段） | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/098-suite-speed-optimizations --json` | `status: pass`，errors 0 / warnings 0，3 records；与 W2 波内读数一致 |
| Checklist 问责（pass H） | W1 round-2 全量处置 34 项；本报告复核计数 | 34/34 dispositioned；10 个 `[Gap]` 全部 raised/covered；`unchecked + unraised + undispositioned = 0`（§4） |
| Pass G 补做（有界） | 读 `.specify/features.md` L94（086 行）、`.specify/features/086-efficient-test-execution.md` `Last Updated` | 绑定与状态保持；checklist/analyze 阶段无登记 → G-01 维持（§5） |
| C/H 修复复核 | 重读 requirements（FR-021/SC-010/FR-024/FR-016/FR-017/SC-008/FR-026/A16）、contracts 计数、tasks DoD-7/GATE-1、六契约条款形态 | 8/8 round-1 C/H 修复落点成立（§2.2.1） |

**归并规则（确定性，可复现）**: worker finding 原样保留其 ID、严重度、锚点、事实与建议；主表按「严重度降序 → 波次（W1<W2<W3）→ 同波内 ID 升序」排列；全部 36 行入表（≤50），无 overflow；`propagation_surface` 按 round-1 同口径（W1 = `plan → tasks → 实现`；W2 = `tasks → 实现`（或 `plan/quickstart → 实现`）；W3 = `实现`）。round-1 residue 单列 §2.2，不重复计入主表。

**归并完整性说明**: round-2 W1/W3 的 finding ID 从 01 重新起编，未沿用 SKILL §6 的稳定 ID 规则；§2.2.3 的 round-1→round-2 映射表恢复 rerun-delta 的可追溯性。该项为**流程观察**，不对制品产生 finding。

## 2. 合并 Findings

### 2.1 Round-2 新增主表（36 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W1-01 | D 宪法对齐 | plan → tasks → 实现 | **CRITICAL**（validated: direct re-read） | `requirements.md` §Overview(L28)/§FR-007(L147)/§FR-021(L170)/§SC-004(L205)/§A3(L252) vs `constitution.md` §XX(L437–439)；`test-execution-efficiency.md` L74/L80/L93 | 缺省档以 slow 标记排除换取更快缺省运行，SC-004 以「≤ 全量基线 50%」做 final 验收——owner 明列「任何情形不可采纳」，且与 FR-021「MUST NOT 以该清单任何方式兑现任何 SC」自相矛盾 | 机制裁决（缺省全量 + 显式快档）或在 analyze 之外显式修订宪法；不得重解释 |
| W1-02 | F 不一致 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-003(L140)/§SC-002(L203)/§SC-002 Source(L217) | FR-003/SC-002 的 contract 子树并行/串行验证未钉死档位；缺省档排除 slow（含全语料扫描型 contract），「tests/contract 名称级一致」的覆盖集合不可判定 | requirements 补档位/选择口径或 plan 契约面声明 |
| W1-03 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-019(L168)/§SC-009(L210)/§Overview(L26) | 转换清单完备性没有分母：计数单位与普查总体（AST 扫描范围、是否含 fixtures/conftest、是否排除嵌套树）未定义，「非边界调用点为 0」不可复算 | requirements 定义普查口径 |
| W1-04 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-024(L173)/§SC-006(L207)/§Shared Strings(L230–234) | 守门测试逐字消费的 `tier=fast/full/caller` 与运行形态行字段、登记册「类别」取值均未进入 Shared Strings，无单一定义点 | requirements 扩展 Shared Strings 或声明字段 owner |
| W1-05 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-025(L174)；`checklists/suite-speed-2026-11-10.md` CHK015(L33) | FR-025 缓存键只声明（会话，worker，受管扫描面），checklist 记录设计另加 `root`/`variant`——入口身份成分未由需求拥有 | requirements 把键成分收归 FR-025 或 plan 显式声明并回引 |
| W1-06 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-006(L146)、§Key Entities(L192) | FR-006(b) 用「少数」界定全语料 contract 成员，全篇无成员数/占比上限；slow 成员增长只能被披露、不能被阻止 | requirements 给出上限或可判定边界 |
| W1-07 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-006(L146) | FR-006(a)「integration 类测试」未说明按目录、marker 还是行为界定；契约目录下的进程边界用例是否具 slow 资格不可判定 | requirements 定义判定基 |
| W1-08 | E 覆盖 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-027(L176)/§A11(L260)；CHK028(L52) | FR-027/A11 的保留类封闭清单不含 checklist 记录设计依赖的 `copy-topology` 类，该类调用点在二值归类中无落点 | requirements 与 plan 对齐保留类闭集 |
| W1-09 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-010(L150)、§Clarifications Q2(L242) | FR-010 要求「驱动者文档」两槽位命令显式请求全量档，但未给出该文档 owner 路径，更新目标不可追溯 | requirements 命名 owner 路径 |
| W1-10 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-007(L147)/§FR-009(L149)/§FR-024(L173) | 「调用方自带 `-m`」只按命令行拼写判定；pytest `addopts` 提供的 `-m` 对 runner 不可见，缺省前置 `-m "not slow"` 会压过它且披露为 0 | requirements 定义 caller-`-m` 检测面或 runner 档位契约声明 |
| W1-11 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §SC-004(L205)/§SC-005(L206)/§FR-020(L169)/§A9(L258) | SC-004 的 50% 与 SC-005 的 110% 阈值未规定单次读数还是重复测量、未给方差容忍；A9 禁止第三次全量运行使重复测量空间受限 | requirements 定义测量协议 |
| W1-12 | F 不一致 | plan → tasks → 实现 | LOW | `requirements.md` §SC-002(L203) vs §SC-003(L204) | SC-003 写明「既存失败按名称相等处理」而 SC-002 只有「双向差为空」——同一比较约定在两条成功判据间不对称 | requirements 措辞对齐 |
| W1-13 | B 歧义 | plan → tasks → 实现 | LOW | `requirements.md` §FR-006(L146) | 同时满足两类 slow 判据（进程边界 + 全语料扫描）的测试没有归类规则，登记册「类别」取值不可判定 | requirements 增加一条归类规则 |
| W1-14 | E 覆盖 | plan → tasks → 实现 | LOW | `requirements.md` §FR-013(L156)/§FR-014(L157) | FR-013 的「改写被扫描树的用例 MUST NOT 消费共享缓存」没有守门检测面，只能靠评审发现违规消费 | plan/implement 补检测面或 requirements 声明评审面 |
| W1-15 | C 欠指定 | plan → tasks → 实现 | LOW | `requirements.md` §FR-017(L163)/§SC-008(L209) | FR-017 的豁免清单未规定载体路径与行模式（文件、行、理由、日期），扫描守卫无法机器消费 | requirements 定义豁免清单 schema |
| W1-16 | C 欠指定 | plan → tasks → 实现 | LOW | `requirements.md` §FR-019(L168) | 转换清单分类粒度未定义：wrapper 包裹多处调用时按 wrapper 一行还是按调用点逐行计数不可判定 | requirements 定义计数单位 |
| W1-17 | B 歧义 | plan → tasks → 实现 | LOW | `requirements.md` §FR-023(L172)/§SC-011(L212) | 「`mode=` 行保持前缀兼容」没有可判定不变量（既有字段位置/拼写不变、新字段尾部追加、分隔符与既有解析不受影响） | requirements 或 098 契约面钉死不变量 |
| W1-18 | C 欠指定 | plan → tasks → 实现 | LOW | `requirements.md` §FR-023(L172) | 「C-001…C-016 条款文本 MUST NOT 被重开或改写」没有检查面（如 086 契约文件在变更 diff 中逐字不变），只是意图声明 | requirements 给检查形态或 plan 契约 |
| W1-19 | C 欠指定 | plan → tasks → 实现 | LOW | `requirements.md` §FR-020(L169) | 「运行期子进程调用数」的测量方法未定义（动态调用计数 vs 静态 AST 普查），同一指标不可复现 | requirements 定义测量方法 |
| W1-20 | B 歧义 | plan → tasks → 实现 | LOW | `requirements.md` §FR-021(L170)/§SC-010(L211) | SC-010 的参数化守卫只比较条目数总量且未定义范围（逐文件 vs 全局），也不覆盖「随机丢参」形态——缩小参数化的禁止无法完全机检 | requirements 定义比较范围 + 丢参规则 |
| W1-21 | B 歧义 | plan → tasks → 实现 | LOW | `requirements.md` §FR-012(L155)/§FR-025(L174) | 共享缓存的「受管扫描面」与「框架根文件」未枚举，「每个面每会话至多一次」缺可枚举判定边界（A6 豁免不覆盖此集合） | requirements 或 plan 数据枚举集合 |
| W1-22 | F 不一致 | plan → tasks → 实现 | LOW | `requirements.md` §FR-021(L170) vs §FR-026(L175) | FR-021 把「等待截止被放宽到超过 FR-026 的上限」一律判红，而 FR-026 允许 >30 秒截止逐条记录理由——同一行为两侧判定相反 | requirements 对齐判红条件与豁免 |
| W2-13 | F 不一致 | plan/quickstart → 实现 | MEDIUM | `plan.md:135` vs `plan.md:217`；`quickstart.md` 场景清单 | plan 的 Project Structure 块写 quickstart「S-0…S-11」，同文件 Phase-1 summary 写「14 scenarios S-0…S-13」，quickstart 实为 S-0…S-13（14）——一份副本的计数过期 | `plan.md`（/speckit.plan 收敛） |
| W2-14 | F 不一致 | tasks → 实现 | MEDIUM | `contracts/tier-selection.contract.md` C-001(L13) vs C-003(L18)/C-010(L46–47)；`data-model.md` E-1(L18–20) | C-001 声明「只有两个档（fast/full）」，机器消费的 `tier` 字段却有三值 `fast/full/caller`；无条款说明 `caller` 是档位状态还是档位缺席 | tier-selection 契约 + E-1 收敛三值语义 |
| W2-15 | F 不一致 | tasks → 实现 | MEDIUM | `quickstart.md` S-10(L131–138) | S-10 第二命令只数**新增** `@pytest.mark.parametrize` 行，无法检测删除，因而不能证明其 Proves 文本的「parametrize removals MUST be zero」 | `quickstart.md` S-10 改计数方向或加删除侧检查 |
| W2-16 | F 不一致 | tasks → 实现 | LOW | `plan.md:79`（Constitution Check XXI）vs `contracts/event-wait.contract.md` C-004(L27–29)；`data-model.md` E-4 | XXI 行把 event-wait C-004 当作「help-documented / zero-side-effect flags」证据，而 C-004 只拥有注入时钟的排序用法；`--help` 义务在 E-4 与 requirements，不在 C-004 | `plan.md` Constitution Check XXI 证据单元格改引 owner |
| W2-17 | F 不一致 | tasks → 实现 | LOW | `plan.md:78`（Constitution Check XX）vs `plan.md:36`（§Summary no-restatement 句） | XX 行证据括注「(no selection shrink, skip, or retry)」压缩重述了 owner 的三类禁止手段，与 §Summary 自述「this plan does not restate」相抵——修复后的残余漂移副本 | `plan.md` Constitution Check XX 改为指针 |
| W3-01 | F 不一致 | 实现 | MEDIUM | `tasks.md:395–396` vs `:89`、`:91`、`:108`、`:112–114` | § Clause Attribution 的「Claiming rows」与 14 条 `[green:]` 实际标签矛盾（slow-membership C-005…C-009 表记 T010、实际标在 T012；parallel-consistency C-001…C-006/C-009…C-011 表记 T014/T015/T016、实际九条在 T017）；标签分区本身 68/68 恰一次，过期的是表 | tasks 修复：以行内标签（机器判据）对齐归属表 |
| W3-02 | F 不一致 | 实现 | MEDIUM | `tasks.md:91`（T012）、`:118`（T021）、`:287–289` | T012 声明跑 `test_suite_tier_contract.py`「obligations 1–11」，但 obligation 11 的两用例到 T021（US2）才追加，T012 仅 blockedBy T010/T011——声明的运行范围包含尚不存在的用例 | tasks 收窄 T012 为 obligations 1–10，或把 T021 的编写前移/补依赖 |
| W3-03 | E 覆盖 | 实现 | MEDIUM | `tasks.md:373`（TS carrier）、`:92`（T013）、`:118`（T021） | TS-M1…TS-M8 载体点名 T021 为 guard 行，但唯一 drill 行 T013 在 US1、只依赖 T012，早于 T021；未声明按腿的 guard 映射 | tasks 声明逐腿映射并把 drill 放到 T021 之后或移除 T021 载体 |
| W3-04 | E 覆盖 | 实现 | MEDIUM | `tasks.md:170`（T037）、`:161`（T031）、`:247` | T037 改 `wait_until` 缺省（使 event-wait C-006/C-007 转绿）却无 `[blockedBy: T031]`（red 默认断言作者）；test-first 链（:247）未覆盖该变更，图允许变更先于红例落地 | tasks 补 `[blockedBy: T031]` 并在 §Within Each User Story 列链 |
| W3-05 | B 歧义 | 实现 | LOW | `tasks.md:215–216`（T055/T056）、`:257` | T055 为 `[P]` 且无 blocker，却消费 T003 的槽 1 读数并与 T056 写同一 evidence 文件；`[P]` 前提与输入依赖未声明 | tasks 补 `[blockedBy: T003]`、去 `[P]` 或拆分 evidence 目标 |
| W3-06 | C 欠指定 | 实现 | LOW | `tasks.md:218`（T058）、`:220`（T060）、`:237` | T058（`[P]`，接口证据）与 T060（quickstart S-1…S-13）未声明 `[blockedBy:]`；前置仅由相位叙事约束 | tasks 声明缺失依赖 |
| W3-07 | F 不一致 | 实现 | LOW | `tasks.md:9` vs `:16`（DoD-2）、`:31`（GATE-5） | Tests Mode 层声明「5 个新守卫文件 + the tier contract file」，DoD-2/GATE-5 枚举五文件总计（含 `test_suite_tier_contract.py`）——层声明多计或措辞不实 | tasks 层声明与五文件枚举对齐 |
| W3-08 | F 不一致 | 实现 | LOW | `tasks.md:11` vs `:300–311`（Work Package Mapping） | Organization 行说「WP-9 → Polish and the closure-stage row」，包表却把 T061 放入独立「Setup / closure handoff」包、把 T003/T022 放入 WP-9 | tasks 对齐 Organization 与包表 |
| W3-09 | F 不一致 | 实现 | LOW | `tasks.md:29`（GATE-3 检查） | GATE-3 写成「`grep -cE …` returns 0」；无匹配时 `grep -c` 打印 0 但退出 1，按退出状态读会反转门禁判定 | tasks 改为「打印计数为 0」或 `! grep -qE …` |

### 2.2 Rerun delta 与 round-1 residue

#### 2.2.1 Resolved Since Last Run（11 条，含证据）

| Round-1 ID | 严重度 | 关闭证据（artifact + location） | 复核来源 |
|------------|--------|--------------------------------|----------|
| W1-01 | CRITICAL | `requirements.md` §FR-021(L170) 改为 owner 唯一判据 + 禁止重述；§Overview(L28) 同步为指针；`plan.md:36` §Summary 同步 | W2 round-2 §3；集成者重读 |
| W1-02 | HIGH | `requirements.md` §SC-010(L211) 扩为 AST + 文本双通道四类形态；§SC-010 Source(L225) 加扫描规则清单与反空转打印；`quickstart.md` S-10(L135–138)；`tasks.md` T057 | W2 round-2 §3（quickstart 侧）；集成者重读（requirements 侧） |
| W1-08 | HIGH | `requirements.md` §FR-024(L173) 按档断言（fast/caller/full）；Q2(L243) 同步；§SC-006(L207) 同步；`data-model.md` E-1(L14) 规则按档限定 | W2 round-2 §3（E-1 侧）；集成者重读（requirements 侧） |
| W1-09 | HIGH | 同上；FR-024(L173) 明列「`--full` + 调用方 `-m` 时选择仍归调用方，收集集合 MUST NOT 扩展回全局全量」 | 集成者重读 |
| W1-17 | HIGH | `requirements.md` §FR-016(L162) 枚举三文件；§FR-017(L163) 六文件闭集；§SC-008(L209) 与 Source(L223) 携带完整闭集 | 集成者重读；`event-wait` C-001 六文件枚举与之一致（W2 §3） |
| W1-21 | HIGH | `requirements.md` §FR-026(L175) 与 §A16(L265) 改为「声明内共享缺省行为变更」（实测 5.0 → 30 秒）；`tasks.md` T031(:161) 断言 `timeout == 30` | 集成者重读 |
| W3-01 | HIGH | 六份契约 68 条款全部重编号为 `C-001…`（`md-bold-closed`，16/9/12/11/10/10）；`account-clause-coverage.py` 读数 `claimed clauses 68`、`[fr-uncovered] pass — 27 of 27`；`validate-tasks.py` 0 error | 本轮覆盖核算运行（§1）；`analyze-repair-gates-2026-11-10.txt` §7–§8；W2 round-2 §3–§4 |
| W3-11 | HIGH | `tasks.md` DoD-7(:21)/GATE-1(:27) 改为「两预算槽全量 + closure 同树 `--full --serial` 验证运行（不占槽、不进度量，A14）」；plan 侧措辞经复核一致未改 | 集成者重读；repair dispositions W3-11 |
| W2-10 | LOW | `data-model.md` E-1(L14) `excluded_slow` 规则与不变量一致（caller/full = 0） | W2 round-2 §2（fixed）；集成者抽查 |
| W3-02 | MEDIUM | tasks.md 现携带 68 条 `[green:]` 标签与 `## Clause Attribution`，原「条款恰一次认领」与「本文件不携带标签」的互斥句已消失；修复合规性由 §3 的标签分区承接 | repair dispositions §3（顺带贴合）；W3 round-2 机械核验（68/68 恰一次） |
| W3-04 | MEDIUM | `tasks.md` T031(:161) 由 `timeout <= 30` 改为 `timeout == 30`（对变更前 5.0 必红），red-first 恢复判别力 | repair dispositions W1-21 同步；集成者重读 |

#### 2.2.2 Rejected（1 条）

| Round-1 ID | 严重度 | 裁决 | 依据 |
|------------|--------|------|------|
| W2-09 | LOW | rejected（round-1 主张不成立） | W2 round-2 重读：C-007 自身写明「The validation run consumes no budget slot and its duration is not an SC-004/SC-005 wall-clock reading」；末尾 `C-010` 引用是对缺引擎条款的冗余邻接交叉引用，不构成无主命题 |

#### 2.2.3 Deferred residue（46 条，全部 open；未修复、未重定级）

**W1 域（28 条；requirements / checklists）**

| Round-1 ID | Sev | Round-2 重报 | 处置 |
|------------|-----|--------------|------|
| W1-03 | MEDIUM | W1-20 | deferred：丢参口径/worker 上限仍无判据 |
| W1-04 | MEDIUM | W1-20 | deferred：参数化比较单位与范围仍未定义 |
| W1-05 | MEDIUM | W1-06 | deferred：「少数」仍无上限 |
| W1-06 | MEDIUM | W1-07 | deferred：integration 判定基仍未定义 |
| W1-07 | MEDIUM | W1-13 | deferred：双属归类规则仍缺 |
| W1-10 | MEDIUM | W1-04 | deferred：登记册字段/取值 owner 仍缺 |
| W1-11 | LOW | — | deferred：孤儿行维护程序仍无（未重报） |
| W1-12 | MEDIUM | W1-10 | deferred：caller `-m` 检测面仍不含 `addopts` |
| W1-13 | MEDIUM | W1-05 | deferred：缓存键 `root`/`variant` 仍未归需求 |
| W1-14 | MEDIUM | W1-21 | deferred：受管扫描面/框架根文件仍未枚举 |
| W1-15 | MEDIUM | W1-14 | deferred：FR-013 违规消费仍无检测面 |
| W1-16 | LOW | — | deferred：会话快照时点（未重报；FR-025「首次消费」可读） |
| W1-18 | MEDIUM | W1-15 | deferred：豁免清单 schema 仍未定义 |
| W1-19 | MEDIUM | — | deferred：注入时钟允许面（未重报；round-2 把 CHK021 判 covered-by §Key Entities/§A12） |
| W1-20 | MEDIUM | — | deferred：sleep 语义分类规则（未重报） |
| W1-22 | MEDIUM | W1-03 | deferred：转换清单分母仍未定义 |
| W1-23 | MEDIUM | — | deferred：保留优先规则穷尽性（未重报） |
| W1-24 | MEDIUM | — | deferred：等价比较规则（未重报） |
| W1-25 | MEDIUM | W1-16 | deferred：wrapper 计数单位仍未定义 |
| W1-26 | MEDIUM | W1-08 | deferred：`copy-topology` 保留类仍缺 |
| W1-27 | MEDIUM | W1-17 | deferred：`mode=` 前缀兼容不变量仍缺 |
| W1-28 | LOW | W1-18 | deferred：C-001…C-016 不重开仍无检查面 |
| W1-29 | MEDIUM | W1-09 | deferred：驱动者文档 owner 路径仍缺 |
| W1-30 | MEDIUM | W1-19 | deferred：子进程计数测量方法仍未定义 |
| W1-31 | MEDIUM | W1-11 | deferred：墙钟阈值测量协议仍未定义 |
| W1-32 | MEDIUM | — | deferred：Overview 20 处/8 文件 vs tasks 20 处/10 文件（未重报；CHK034 附注同源） |
| W1-33 | MEDIUM | — | deferred：EP-001…EP-004 premises owner（未重报） |
| W1-34 | LOW | W1-04 | deferred：Shared Strings 消费列仍缺 FR-007/FR-024（同面重报） |

**W2 域（10 条；plan / contracts / quickstart；处置取自 W2 round-2 §2）**

| Round-1 ID | Sev | 处置与证据 |
|------------|-----|------------|
| W2-01 | MEDIUM | deferred：基线槽拼写三种仍并存；S-13 baseline 省略 `--full`；S-12 消费 `/tmp/full-baseline.txt` 但同一场景无产出命令 |
| W2-02 | MEDIUM | deferred：C-008 仍把 `c20` 列入「已转换为消费 payload」的调用者，而 C-006 要求 `test_c20` 字节一致性检查 MUST NOT 消费缓存 |
| W2-03 | MEDIUM | deferred：PC-M2 仍期望「记录树身份检查」对两树名单判红，C-012 证据字段仍无树身份/指纹 |
| W2-04 | MEDIUM | deferred：C-004/CA-M2 仍要求 copy-isolation 突变失败，C-009…C-011 与 S-5 仍无可执行用例 |
| W2-05 | MEDIUM | deferred：C-009 守卫仍断言 `timeout <= 30`，而 C-007/E-5 允许更长截止（逐条理由）——合法站点仍让守卫转红 |
| W2-06 | MEDIUM | deferred：S-1/S-4 仍把未排序、含汇总行的 `--collect-only` 原始输出直接管道给 `comm` |
| W2-07 | MEDIUM | deferred：S-1/S-4/S-12/S-13 仍指向裸 `/tmp/...`；plan XVII 合规证据仍只覆盖 research 探针 |
| W2-08 | LOW | deferred：E-8 仍写「三个 owner/restatement 面」，WP-3 列四行、S-9 检查两侧槽行与两处阶段提示重述 |
| W2-11 | LOW | deferred：C-007 仍只为 `framework-specs-corpus` 定义构建/装载/计数；第二受管面 `framework-root-inputs` 仍无机制，而 C-011 的 `build_count=1` 覆盖全部受管面 |
| W2-12 | LOW | deferred：C-016 仍允许记录反度量（marked set 并回缺省档 = 全量选择）同时禁止「第三次全量运行」，反度量的预算类仍未定义 |

**W3 域（7 条；tasks.md）**

| Round-1 ID | Sev | Round-2 重报 | 处置 |
|------------|-----|--------------|------|
| W3-03 | MEDIUM | — | deferred：trace 表仍无 T001/T002/T011/T032/T033/T059/T060 行（未重报；T032/T033 → FR-015 仍无映射） |
| W3-05 | MEDIUM | W3-02 + W3-03 | deferred：T012 obligations 1–11 与 T021 时序矛盾仍存 |
| W3-06 | MEDIUM | — | deferred：GATE-5 机械检查面仍窄于其全称谓声明（未重报） |
| W3-07 | LOW | — | deferred：T028 的 before/after 运行叙事未说明 before 侧实为 T003 名单（未重报） |
| W3-08 | LOW | W3-07 | deferred：Tests Mode 层声明与五文件枚举仍不一致 |
| W3-09 | LOW | W3-08 | deferred：Organization 行与 Work Package 表仍不一致 |
| W3-10 | MEDIUM | — | deferred：US2 checkpoint(:122) 仍称「US1 is not required」，而 T015 blockedBy T007/T009（US1 行）（未重报） |

**G 域（1 条；integrator addendum）**

| ID | Sev | 处置与证据 |
|----|-----|------------|
| G-01 | LOW | deferred：`.specify/features.md` L94（086 行）最新 098 阶段记录仍为 tasks；详情文件 `Last Updated` 仍止于 098 plan；checklist 与 analyze 阶段无对应登记——与 round-1 结论一致，未修复 |

Residue 合计：46 deferred = 28（W1）+ 10（W2）+ 7（W3）+ 1（G）。与 fixed 11 + rejected 1 相加 = round-1 全部 58 条，无遗漏、无重复。

## 3. 跨制品一致性（Cross-Artifact Consistency）

以下簇把跨 requirements → plan/contracts → tasks 的同一缺陷面合并观察；**不改写任何单行严重度**，归属只指向单一决策 owner。

| 簇 | 成员（round-2 ID） | 共同缺陷 | 单一决策 owner |
|----|--------------------|----------|----------------|
| **X-1 宪法 XX 与档位机制的根本冲突** | W1-01（CRITICAL）；关联 W2-16/W2-17 的证据单元格残余 | 需求层把「缺省档 = 全量 − slow」与 SC-004 的 50% 胜利绑成一条验收链；判据 owner 把「标记排除换取数字下降」列为任何情形不可采纳、并要求同一选择比较。修复轮完成的「owner 指针化」没有消除冲突，反而使 FR-021 的「不得以该清单任何方式兑现任何 SC」与 SC-004 的文本矛盾可直接判定 | requirements §FR-007/§SC-004/§A3（机制裁决）；宪法修订只能发生在 analyze 之外（用户裁决） |
| **X-2 守卫面分母、单位与载体未钉死** | W1-03、W1-04、W1-15、W1-16、W1-19、W1-20、W2-15 | 守卫测试已在 SC/契约中命名，但其分母（普查总体）、计数单位（wrapper/调用点）、载体 schema（豁免清单、登记册字段）、比较范围（逐文件/全局、新增/删除）无单一 owner——「命中为零」不可复算，quickstart 的证明命令甚至数错了方向 | requirements（守卫面一次收敛）；plan 契约只回引 |
| **X-3 需求内部语义与检测面空缺** | W1-02、W1-05、W1-06、W1-07、W1-09、W1-10、W1-11、W1-13、W1-14、W1-21、W1-22 | 档位选择口径（FR-003/SC-002）、slow 成员判据（「少数」/integration 判定基/双属规则）、缓存键入口身份、caller-`-m` 检测面、墙钟测量协议、判红与豁免边界——需求内部条款彼此可读但对外不可判定 | requirements §FR-003…§FR-027 |
| **X-4 修复引入的 tasks 依赖与归属漂移** | W3-01…W3-09 | 68 条 `[green:]` 的刚性分区与 § Clause Attribution 表脱节（W3-01）；T012 声明范围超前于 T021（W3-02）；TS drill 早于其 guard 载体（W3-03）；T037 缺 red-first 依赖（W3-04）；`[P]`/blockedBy 前提未声明（W3-05/06）；层声明与包表措辞漂移（W3-07/08）；GATE-3 退出码读法反转（W3-09）——修复轮的重编号与标签发布引入了自己的分析债 | tasks（一轮重对齐；行内 `[green:]` 标签是机器判据，表随标签） |
| **X-5 修复后副本计数与术语漂移** | W2-13、W2-14；carried round-1 W2-08 | 同一事实在 plan/quickstart/contracts/data-model 各留副本：quickstart 场景数 11 vs 14；档位「二值」vs `tier` 三值；E-8 表面计数 3 vs 4。符合 one-source-of-truth 的预测：副本必然漂移 | plan 阶段单点拥有（计数与术语） |

## 4. Checklist 问责（pass H）

- 对象: `checklists/suite-speed-2026-11-10.md`（34 项，全部 `- [ ]`；`[Gap]` 10 项）。
- 处置（W1 round-2 全量映射，本报告复核计数）: **34/34 dispositioned** —— `raised-as-finding` 20 项 + `covered-by` 14 项；10 个 `[Gap]` 项中 8 项 raised（CHK009/012/015/017/020/024/027/028）、2 项 covered-by（CHK001 → §SC-010/§FR-021；CHK021 → §Key Entities/§A12）。
- 可观察计数: `unchecked(0) + unraised(0) + undispositioned(0) = 0` → 不阻断。
- 附注: CHK034 提到的「tasks 阶段 20 处/10 文件 vs Overview 20 处/8 文件」差异与其读域外声明一致，映射到 round-1 `W1-32`（deferred），不另立新 finding。

## 5. Coverage Summary 与 Feature Linkage

| 指标 | 读数 | 证据 |
|------|------|------|
| FR 总数 / 已引用 | 27 / **27（pass）** | 覆盖核算 round-2 运行；`[fr-uncovered] pass (0) — 27 of 27` |
| SC 总数 | 11（final 9 + supporting 2） | `requirements.md` §Measurable Outcomes |
| 任务行 | 61（T001–T061；60 `[ ]` + 1 `[~]`） | `tasks.md`；W3 round-2 机械核验 |
| 契约条款宇宙 | 6 文件 / 68 条款（16/9/12/11/10/10） | `analyze-repair-gates-2026-11-10.txt` §8；W2 round-2 §4 |
| 条款机器可判覆盖 | **68/68 claimed**（`[green:]` 每条款恰一次） | 覆盖核算 round-2 运行；W3 round-2；`validate-tasks.py` 0 error / 3 warnings（已记入 tasks § Clause Attribution） |
| 覆盖核算状态 | **`baseline-missing`（exit 2，阶段可见问题）**；冻结（T002）是 implement 起点义务，先冻结会钉住坏基线——本阶段按 SKILL §3 未 `--freeze` | `test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt` |
| 决策张力 | 3 records，errors 0 / warnings 0 | 本轮 `validate-decision-tensions.py` 运行（同一证据文件） |
| Feature 绑定 | `FEATURE_ID=086` / `086 Efficient Test Execution (Concurrent by Default)`；状态保持 `Ready for Review`，不回退 | `.specify/features.md` L94；`.specify/features/086-efficient-test-execution.md` |
| Stage 记录 | 索引行最新 098 记录 = tasks；详情 `Last Updated` = 098 plan；checklist/analyze 未登记 → **G-01 维持（LOW, deferred）** | pass G 有界复查（§1） |

## 6. Systemic Observations

1. **CRITICAL 是决策级冲突，不是措辞缺陷**：修复轮把 FR-021/Overview/plan Summary 改成 owner 指针（round-1 W1-01 的合规修复，且已验证），但这恰好让「缺省档标记排除兑现 SC-004」与 owner 的「任何情形不可采纳」正面相遇。需求文本无法自证共存；可退出路径只有机制变更或 analyze 之外的显式宪法修订。任何 MEDIUM/LOW 修补都不能关闭它。
2. **修复轮引入自己的分析债**：36 条新 finding 中 9 条落在 tasks（W3-01…W3-09），其中 W3-01（归属表 vs 行内标签）与 W3-02/W3-03（T012 声明范围超过已存在用例）直接来自重编号与 68 标签发布。这符合「一次修复 = 一次新的可分析面」的规律；round-2 不能读作「clean rerun」。
3. **守卫面可判定性仍是最大 MEDIUM 家族**（X-2）：守卫被命名、被分配 SC，但分母、计数单位、载体 schema 与比较范围没有 owner——「零命中」在多数面上不可复算。
4. **计数与术语副本漂移**（X-5）：quickstart 场景数、档位二值/三值、E-8 表面计数三处独立漂移，与 one-source-of-truth 的预测一致；修复计数类制品时应同时收敛其副本。
5. **Round-1 C/H 修复质量成立**：8/8 落点在当前文本中可观测（§2.2.1），W2-09 的 reject 也说明 round-1 存在一条过度定级。验证侧观察：本轮唯一的 C/H 由直接重读确认，若后续需要与 fresh-context 波同级的证据，建议按 1 finding : 1 validator 预算派发。

## 7. Metrics

- **新增**: 36 条 = CRITICAL 1 / HIGH 0 / MEDIUM 17 / LOW 18；主表 36 行（≤50）；overflow 0。
- **Round-1 residue**: 58 条 = fixed 11 / rejected 1 / deferred 46；residue 表逐条可对账，无遗漏。
- **验证**: C/H 送审 1、validated 1（direct re-read）、proposed 0、reject 0、downgrade 0（宪法 carve-out：无降级候选）。
- **类别分布（新增行）**: A 0 · B 10 · C 9 · D 1 · E 3 · F 13 · G 0。
- **Checklist**: 34/34 disposed；10 `[Gap]` 全部 raised/covered；undispositioned 0。
- **覆盖核算**: exit 2；`baseline-missing`（预期 pre-T002）；claimed clauses 68；FR 27/27 pass。
- **同源检测**: 不适用——制品由更早 SDD 阶段作者产出，非本轮任一检测波。

## 8. Artifacts Untouched 与只读证明

- `requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`quickstart.md`、`contracts/*`（6）、`checklists/*`、`feature-ref.md`、`research.md`、`.specify/features.md`、`.specify/features/086-efficient-test-execution.md` **零修改**（本阶段无 Edit/Write 作用于这些路径）。
- 本阶段唯一写入：本报告、`test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback；按派发纪律不提交）。
- 三份 worker findings 文件为本阶段输入，原样保留；单一 closing commit 只包含其与上述两份证据。

## 9. Next Actions（不自动修复）

- **CRITICAL（W1-01）** → `/speckit.implement` 前必须处置：由 owner（requirements）做机制裁决，或先完成 analyze 之外的显式宪法修订（用户裁决）。不得以降级、重解释或局部措辞修补关闭。
- **MEDIUM/LOW（35 条新增 + 46 条 residue）** → 不阻断；建议按 §3 簇的单一 owner 分批收敛：X-4（tasks 一轮重对齐）与 X-5（plan 副本收敛）成本最低；X-2/X-3 建议在 requirements 一次收敛。
- 修复后重跑 `/speckit.analyze`（Round 3）以产生新的 rerun delta；在 W1-01 未裁决前，round-3 仍将判 FAIL。
