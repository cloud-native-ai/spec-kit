# Analyze Merged Report — 098-suite-speed-optimizations（analyze Round 3，2026-11-10）

- **Stage**: analyze（串行集成 · Round 3 · r3 修复后重过门；并发 N=2）
- **输入**: `test-evidence/analyze-findings-r3-W2.md`（plan / data-model / quickstart / 6 契约，10 条）、`test-evidence/analyze-findings-r3-W13.md`（requirements / checklists / tasks，11 条）；两波读域互斥且合并覆盖 spec 全目录
- **权威**: 本特性 spec 全目录 + `.specify/constitution.md`（v1.19.0）+ `.specify/skills/internal/analyze-artifacts/`（SKILL.md、`references/detection-and-severity.md`、`references/validation-and-report.md`）；判据 owner `.specify/shared/guidelines/test-execution-efficiency.md`
- **上游记录**: `test-evidence/analyze-merged-round2-2026-11-10.md`（Round 2：36 条新增 1C/0H/17M/18L；round-1 residue 58 = fixed 11 / rejected 1 / deferred 46）、`test-evidence/analyze-repair-dispositions-r3-2026-11-10.md`（W1-01 confirm + 修复落点）、`test-evidence/analyze-repair-gates-r3-2026-11-10.txt`（修复后门禁读数）
- **性质**: 只读集成。未修复任何 finding；本阶段写入仅：本报告、`test-evidence/analyze-coverage-accounting-round3-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback，按派发纪律不提交）。
- **归属声明**: 两个 Worker 的检测结论原样保留（ID、严重度、锚点、事实、建议）；集成者只做确定性归并、跨制品聚类、C/H 锚点复核、一处机械行号更正（§1，显式披露）与 residue 记账。

## 0. Gate verdict 与 CRITICAL/HIGH 汇总

**Verdict: 通过（PASS）** —— 本轮新增 **0 CRITICAL / 0 HIGH**；Round-2 的唯一 CRITICAL（W1-01）已由 r3 修复关闭（§2.2.1，落点逐条复核）；21 条 MEDIUM/LOW 不阻断，随建议 owner 收敛。

**两项声明分开陈述（cleared backlog ≠ clean rerun）**:

- **Round-2 C/H 后备箱已清空**：1 条 CRITICAL（W1-01）fixed、1 条 LOW（W2-17）fixed；0 条 round-2 C/H 仍 open。
- **本轮是一次干净的全覆盖重检（C/H 级）**：W2 波读 plan/data-model/quickstart/契约，W13 波读 requirements/checklists/tasks；检测在 SC-004 重锚面（上一轮 CRITICAL 的落点）做了专项复核（§0.2）后仍给 0 C/H。

| 严重度 | 新增条数 | 构成 | 处置要求 |
|--------|----------|------|----------|
| CRITICAL | 0 | — | — |
| HIGH | 0 | — | — |
| MEDIUM | 10 | W2 ×5 · W13 ×5 | 不阻断；按建议 owner 收敛 |
| LOW | 11 | W2 ×5 · W13 ×6 | 建议性 |
| **新增合计** | **21** | 主表 21 行（≤50）；overflow 0 | — |
| **Round-2 新增 36 条（本轮 prior state）** | **36** | fixed 2 · carried 9 · 未重报 25 | 见 §2.2 |
| **Round-1 deferred residue 46 条** | **46** | re-raised 7（映射 8 行）· still deferred 39 | 见 §2.3 |

### 0.1 验证路径与零 C/H 声明（显式披露）

- 本轮 C/H 为 0，按 SKILL §7 **无验证波可派发**；未产生 proposed / rejected / downgrade 行。C/H 送审 0、validated 0、downgrade rate 不适用。
- **零 C/H 的样本义务（zero-finding floor）**：对「覆盖仅系于单一任务行」的 8 个 FR 全部抽读（FR-005→T008、FR-006→T009、FR-010→T018、FR-011→T022、FR-019→T045、FR-020→T055、FR-021→T057、FR-027→T049），另抽读 5 组其余行上下文（T004–T007、T012–T013、T021–T022、T043–T045、T055–T057）。结果：7/8 单行覆盖成立；FR-020 的单行 T055 不产出运行期子进程调用数——即 W13-02，样本未另立新 finding（§5）。
- **上一轮 CRITICAL 的关闭复核**：集成者直接重读 SC-004 全链（§0.2 指针列出的全部落点），确认「同选择集两臂」判据、范围披露降级与「不得兑现」声明均已落位；W13 波的专项复核结论与本复核一致。

### 0.2 C/H 汇总与指针（本轮 0 条；前轮 C/H 关闭指针）

| # | ID | 严重度 | 状态 | 指针 |
|---|----|--------|------|------|
| — | — | CRITICAL | 本轮无 | 两波显式 0 CRITICAL；样本见 §0.1 |
| — | — | HIGH | 本轮无 | 同理 |
| 关闭 1 | round-2 W1-01 | CRITICAL（前轮） | **fixed**（r3 修复） | `analyze-repair-dispositions-r3-2026-11-10.md` §1；落点：`requirements.md` §SC-004(L205)、§SC-004 Source(L219)、§FR-007(L147)、§FR-021(L170)、§A3(L252)；`plan.md` Constitution Check XX(L78)、T-001；`contracts/tier-selection.contract.md` C-016(L75–84)；`quickstart.md` S-13(L174–189)；`tasks.md` T055–T056(L215–216) |
| 关闭 2 | round-2 W2-17 | LOW（前轮） | **fixed** | `plan.md` L78 的 XX 行现为 SC-004 / SC-006 / C-016 指针，不再重述 owner 清单 |

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 输入读取 | 两份 round-3 worker findings（读域互斥：W2 = plan/data-model/quickstart/6 契约；W13 = requirements/checklists/tasks） | 10 + 11 = 21 条新增 finding |
| 确定性归并 | 本报告 §2 | 主表 21 行 + overflow 0；严重度不重评分（worker 原值保留） |
| `propagation_surface` 分配 | 两波未携带该字段；集成者按锚点域以 round-2 同口径确定分配：requirements 侧 → `plan → tasks → 实现`；tasks 侧 → `实现`；plan/quickstart/contracts 侧 → `tasks → 实现` | 21/21 分配；不触碰严重度 |
| C/H 锚点复核 | 0 C/H；改为复核前轮 CRITICAL 的关闭落点（§0.2）与两波 0 C/H 声明的支撑面 | 0 送审；前轮 CRITICAL 关闭成立 |
| SC-004 专项复核 | 重读 requirements §Overview(L28)/US1(L36–40)/FR-007(L147)/FR-021(L170)/SC-004(L205)/Source(L219)/A3(L252)/A9(L258)/A12(L261) 与 tasks T055–T056 | 全部一致；无「slow 排除兑现提速判据」残留 |
| 机械更正（显式披露） | W13-05 记 FR-015 锚点为 L165；当前文件实测 L161（其余锚点 RS-004 L187、Key Entities L194、A12 L261 均核对一致） | 1 处行号更正（correction，非 decision）；不改 finding 事实与严重度 |
| 覆盖核算（固定步骤，**未** `--freeze`） | `python3 scripts/python/account-clause-coverage.py .specify/specs/098-suite-speed-optimizations` | exit 2，`status: baseline-missing`（预期 pre-T002）；`claimed clauses 68`；`[fr-uncovered] pass — 27 of 27`；`[clause-unparsable] fail (107)` 与 `[clause-uncovered] fail (640)` 均为缺失基线下的全语料读数——完整输出：`test-evidence/analyze-coverage-accounting-round3-2026-11-10.txt` |
| 决策张力（pass I 确定性段） | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/098-suite-speed-optimizations --json` | `status: ok`，errors 0 / warnings 0，3 records |
| 任务校验读数 | 引用 `analyze-repair-gates-r3-2026-11-10.txt` §5 | `validate-tasks.py` PASS（with warnings）：0 error / 3 warning（green-cross-phase：T017/T025/T040，均为已知条款序警告） |
| Checklist 问责（pass H） | 复核 round-2 的 34/34 全量映射 + 本轮 re-raise 对账 | 34/34 dispositioned；10 个 `[Gap]` 全部 raised/covered；`unchecked + unraised + undispositioned = 0`（§4） |
| Pass G 有界复查 | 读 `.specify/features.md` L94（086 行）、`.specify/features/086-efficient-test-execution.md` `Last Updated` 与 § Related Specifications | 索引最新 098 记录 = tasks；详情 Last Updated = 098 plan；checklist/analyze 未登记 → G-01 维持（§5） |
| 零 C/H 样本 | §0.1 的 8 个单行 FR + 5 组上下文抽读 | 7/8 成立；1 条落在既有 W13-02，无新 finding |

**归并规则（确定性，可复现）**: worker finding 原样保留其 ID、严重度、锚点、事实与建议；主表按「严重度降序 → 波次（W2 < W13，与文件时序一致）→ 同波内 ID 升序」排列；全部 21 行入表（≤50），无 overflow。

## 2. 合并 Findings

### 2.1 Round-3 新增主表（21 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation | Delta |
|----|----------|---------------------|----------|-------------|---------|----------------|-------|
| W2-01 | F 不一致 | tasks → 实现 | MEDIUM | `quickstart.md` S-13(L177, 190–193)；`plan.md` WP-9.1(L327)、WP-3.1–2(L254–257)；`contracts/tier-selection.contract.md` C-015/C-016(L71–84) | S-13 的基线槽命令省略 `--full`，而其自身前提与 WP-9 第 1 项都说基线槽带 `--full`；C-015/C-016 把基线放在 implement 起点（那时 `--full` 尚不存在）——命令、前提与时点不能同时成立 | `quickstart.md` S-13（命令+前提）；`plan.md` WP-9 第 1 项对齐契约的基线定义 | carried（round-1 W2-01） |
| W2-02 | E 覆盖 | tasks → 实现 | MEDIUM | `quickstart.md` S-12(L158–172)；C-015(L71–74)；`plan.md` WP-9.4(L330) | S-12 读 `/tmp/full-baseline.txt` 作为 implement 起点全量 id 集，但无任何制品指派产出该文件的命令（S-13 基线槽把 `--names-out` 失败名单写到 `/tmp/base-full.txt`）——C-015 的基线输入无生产者 | `quickstart.md` S-12 命名产出命令；C-015 钉死基线 id 集记录方式 | carried（round-1 W2-01 后半，拆分） |
| W2-03 | F 不一致 | tasks → 实现 | MEDIUM | `quickstart.md` S-10(L131–138) | S-10 的 skip/xfail 臂对每个改动文件的**全内容** grep 而非 diff 新增行，parametrize 臂数**新增**标记行（`^\+`）而判据是删除为零——两条命令都不度量其 Proves 声称的「diff 内零新增命中」 | `quickstart.md` S-10 | carried（round-2 W2-15） |
| W2-04 | F 不一致 | tasks → 实现 | MEDIUM | `contracts/scan-cache.contract.md` C-006(L27–29)、C-008(L37–40)；`data-model.md` E-3(L59) | C-008 把 `c20` 列入「已转换为消费 payload」的实语料调用者，而 C-006/E-3 要求 `test_c20` 的字节一致性检查保留为独立子进程测试且 MUST NOT 消费缓存；无文件限定的 node id 或 test-vs-call-site 粒度区分两种处置 | `scan-cache.contract.md` C-006/C-008 限定 node id | carried（round-1 W2-02） |
| W2-05 | B 歧义 | tasks → 实现 | MEDIUM | `tier-selection.contract.md` C-009(L43–46)、C-004(L22–23)；`data-model.md` E-1(L14)；`quickstart.md` S-2(L40–47) | C-009 说排除数「over the caller's selection」但给出的是不带调用方 path/`-k` 的 `pytest --collect-only -q -m slow`；E-1 把 `excluded_slow` 定义在调用方选择上、C-004 又允许 path/`-k` 在档内收窄——被收窄的缺省运行其披露数在「全树」与「收窄」之间不可判定 | `tier-selection.contract.md` C-009 | **new** |
| W13-01 | E 覆盖 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-021(L170)、§SC-010(L211)、§SC-010 Source(L225)；`tasks.md` T057(L217) | FR-021 要求 SC-010 的程序化 diff 扫描对三类 098 增量判据「任一命中即 MUST 判红」，但 SC-010 的扫描规则、Measurement Source 与 T057 都只含「参数化条目数不减少」，缺「等待截止被放宽超过 FR-026 上限」与「worker 数解析超出 runner 契约既有规则」两类——MUST 级判据缺承载面 | requirements FR-021 ↔ SC-010 补齐；T057 同步 | carried（round-2 W1-20；LOW→MEDIUM） |
| W13-02 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-020(L169)、§Measurement Sources；`tasks.md` T003(L68)、T055–T060(L215–220) | FR-020 的 MUST「记录运行期子进程调用数」既无测量方法定义（动态计数 vs 静态 AST 普查，CHK032），也无任何任务行产出该读数——T003 只做静态 subprocess 普查（P-4），T045 的清单仅覆盖转换面 | requirements FR-020 定义方法并落测量源；tasks 新增读数行或改写为静态口径 | carried（round-2 W1-19；LOW→MEDIUM） |
| W13-03 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-025(L174)、§Key Entities(L193)、CHK015(L33)；`tasks.md` T025(L140) | FR-025/Key Entities 把缓存键定义为（会话，worker，受管扫描面）三元组，而 T025 实现键为 `(worker, surface, root, variant)`——`root`/`variant` 两个身份组件在需求侧无定义，键身份以哪一侧为准不可判定 | requirements FR-025 吸收 root/variant 或将其声明为扫描面身份 | carried（round-2 W1-05） |
| W13-04 | E 覆盖 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-027(L176)、§A11(L260)、§A17(L266)、CHK028(L52)；`tasks.md` T049(L200) | FR-027 的保留类封闭枚举（含 A11/A17 扩展）不含 `copy-topology`，而 T049 依赖该保留类登记 keep 行；按 FR-027「其余只验证纯 Python 引擎或 CLI 的调用 MUST 改进程内直调」的字面判据，该保留属违约 | requirements FR-027/A11/A17 补入该类或归并到既有保留类 | carried（round-2 W1-08） |
| W13-05 | C 欠指定 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-015(L161；worker 记 L165)、§RS-004(L187)、§Key Entities(L194)、§A12(L261)、CHK021(L42)；`tasks.md` T032–T033(L165–166) | 需求把注入时钟描述为「测试夹具输入」、RS-004 的 in-scope 面不含 `scripts/python/feedback-utils.py`，而 T032 新增该 shipped engine 的 `--now` CLI 选项（含 `--help` 与具名错误面）并触发镜像义务——需求侧未授权也未约束任何产品代码接口变更 | requirements（FR-015/RS-004/A12/Key Entities 明示载体与边界）；plan/contracts 对齐 | carried（round-1 W1-19 重报） |
| W2-06 | F 不一致 | tasks → 实现 | LOW | `quickstart.md` S-1(L27–30) | S-1 把原始 `pytest --collect-only -q` 输出（定义序，非字典序）喂给要求排序输入的 `comm`——集合比较按原文不可靠可判 | `quickstart.md` S-1 先排序两侧 id 文件 | carried（round-1 W2-06） |
| W2-07 | F 不一致 | tasks → 实现 | LOW | `plan.md` Phase 1 Summary(L217)；`quickstart.md` S-0.7(L18) | plan 的 Phase 1 摘要写 quickstart「S-0.1…S-0.6 executed with real output」，而 S-0 表还带一条已执行的 S-0.7 hazard 行 | `plan.md` § Phase 1 summary | **new** |
| W2-08 | F 不一致 | tasks → 实现 | LOW | `data-model.md` E-8(L119)；`plan.md` WP-3(L252–260)；`quickstart.md` S-9(L116–126) | E-8 说 `--full` 拼写改动落在「三个 owner/restatement 面」，而 WP-3 列四条编辑（两槽行 + 两处阶段提示重述）、S-9 断言「两侧槽行与两处阶段提示重述」 | `data-model.md` E-8 枚举表面或去掉计数 | carried（round-1 W2-08） |
| W2-09 | E 覆盖 | tasks → 实现 | LOW | `plan.md` WP-3.6(L259)；`quickstart.md` S-9(L116–126) | WP-3 第 6 项要求「doc assertion (guard case)」证明两条 owner 行都带 `--full`，但不命名测试文件，也无 098 契约条款拥有该断言（T021 把它附会到 tier-selection §E obligation 11，而 obligation 11 只拥有 full-collection equality） | `plan.md` WP-3 命名守卫文件或补 owning clause | **new** |
| W2-10 | F 不一致 | tasks → 实现 | LOW | `tier-selection.contract.md` C-001(L13–15)、C-003(L19–21)；`data-model.md` E-1(L9–25)、E-7(L108–110) | C-001 声明「两档且只有两档」，而 mode-line `tier` 字段在 C-003/E-1/E-7 允许三值 `fast|full|caller`——「tier」同时命名两成员选择枚举与三值披露字段，无定义区分 | `tier-selection.contract.md` C-001 加一行区分 | carried（round-2 W2-14；MEDIUM→LOW） |
| W13-06 | F 不一致 | plan → tasks → 实现 | LOW | `requirements.md` §Overview(L25, L30)；`tasks.md` P-3(L53)；CHK034(L64) | 同一 `time.sleep` 普查的文件数两处不一致：requirements 记「20 处 / 8 文件」，tasks P-3 记「20 occurrences in 10 files」，A6 未指定验收以哪一读数为准 | requirements §Overview 对账，或标注一律以 implement 起点重测为准 | carried（round-1 W1-32 重报） |
| W13-07 | F 不一致 | 实现 | LOW | `tasks.md` T012(L91)、T021(L118)、GATE-5(L31) | T012 声明运行 tier 契约「obligations 1–11」全绿，但 obligation 11 由更晚的 T021 追加、T012 的 blockedBy 不含 T021——按行序该绿记录不可能覆盖 obligation 11，之后也无重跑行（仅 GATE-5 兜底） | tasks T012 改为 obligations 1–10，或增加 T021 后的重跑行/依赖 | carried（round-2 W3-02；MEDIUM→LOW） |
| W13-08 | F 不一致 | 实现 | LOW | `tasks.md` § Clause Attribution(L392–397) vs 行内标签 T010/T012(L89–91)、T014–T017(L108–114)、T061(L221) | Clause Attribution 表与实际 `[green:]` 标签错位：slow-membership C-005…C-009 表记 T010 而标签在 T012；parallel-consistency 的 C-001…C-006/C-009…C-012 表分散记于 T014–T017 而标签集中于 T017（+T061）；标签自身构成合法 68/68 单次分区 | tasks § Clause Attribution 按实际标签重写表 | carried（round-2 W3-01；MEDIUM→LOW） |
| W13-09 | C 欠指定 | plan → tasks → 实现 | LOW | `requirements.md` §Shared Strings(L228–236)、US1 AS4(L47)、Edge(L126)、§FR-024(L173)、§A3/A4(L252–253)、CHK012(L27)；`tasks.md` T007(L86)、T009(L88) | Shared Strings 的 Consumed by 列不完整（[[STR-001]] 漏 FR-007/FR-024；[[STR-003]] 漏 US1 AS4/Edge/FR-024/A3/A4；[[STR-002]] 漏 US1 AS4/Edge），且本特性新增、被守门测试逐字消费的 `tier=` / `excluded_slow=` / 登记册类别值未按该约定挂接单一所有者 | requirements §Shared Strings 补 Consumed by；新字面量入表或显式指向契约 owner | carried（round-2 W1-04；MEDIUM→LOW） |
| W13-10 | B 歧义 | plan → tasks → 实现 | LOW | `requirements.md` §FR-019(L168)、§FR-027(L176)、§SC-009(L210)、CHK026(L50) | SC-009 的「转换前后同一断言集合全绿」与 FR-027 允许把退出码断言改为 CliRunner 等价结果之间存在形式冲突，「等价性」未定义可判定的比较口径 | requirements SC-009/FR-027 给出等价性判据措辞 | carried（round-1 W1-24 重报） |
| W13-11 | E 覆盖 | 实现 | LOW | `tasks.md` GATE-1(L27)、T003(L68)、T061(L221) | GATE-1 与 T061 均以 `baseline-failed.txt` 为比较基线，但没有任何行声明该文件为产出物（T003 只记「the --names-out reading」未落路径）——gate 的比较对象无产出归属 | tasks T003 显式以 `--names-out` 写 `baseline-failed.txt`，或 GATE-1 注明该路径由槽位 1 产出 | **new** |

### 2.2 Rerun delta（round-2 → round-3）

#### 2.2.1 Resolved Since Last Run（2 条，含证据）

| Round-2 ID | 严重度 | 关闭证据（artifact + location） | 复核来源 |
|------------|--------|--------------------------------|----------|
| W1-01 | CRITICAL | `requirements.md` §SC-004(L205) 重锚为「缺省档并行 vs 同选择集 `--serial`」并明文「提速 MUST NOT 由慢档排除兑现」；§SC-004 Source(L219) 要求两组 `--collect-only` 证明两臂选择相等；§FR-007(L147)/§FR-021(L170)/§A3(L252) 补「选择差异不得兑现任何 SC」；§A9(L258) 把两臂定为定向运行；§A12(L261) 限定全量档选择判据不变；`plan.md` L78 XX 行改为 SC-004/SC-006/C-016 指针、Performance Goals(L47) 同选择集 50%、T-001 同步；`contracts/tier-selection.contract.md` C-016(L75–84) 重写；`quickstart.md` S-13(L174–189)；`tasks.md` T055–T056(L215–216) | 集成者直接重读九处落点；W13 波专项复核（r3 W13 报告首段）；repair dispositions §1 |
| W2-17 | LOW | `plan.md` L78 XX 行现为「SC-004 same-selection measurement and SC-006 coverage-preservation guard; C-016」指针，原先压缩重述 owner 清单的括注已消失 | 集成者重读 |

#### 2.2.2 New Since Last Run（4 条）

`W2-05`（tier-selection C-009 的 caller-selection 口径）、`W2-07`（plan Phase 1 摘要 S-0.1…S-0.6 vs S-0.7）、`W2-09`（WP-3 doc-assertion 无 owner）、`W13-11`（`baseline-failed.txt` 无产出归属）。

#### 2.2.3 Carried over（17 条，映射与严重度变化）

| Round-3 ID | 前身 | 严重度变化（前 → 本） |
|------------|------|------------------------|
| W2-01 | round-1 W2-01（round-2 deferred） | MEDIUM → MEDIUM |
| W2-02 | round-1 W2-01（同面拆分） | —（拆分新增行） |
| W2-03 | round-2 W2-15 | MEDIUM → MEDIUM |
| W2-04 | round-1 W2-02（round-2 deferred） | MEDIUM → MEDIUM |
| W2-06 | round-1 W2-06（round-2 deferred） | MEDIUM → LOW |
| W2-08 | round-1 W2-08（round-2 deferred） | LOW → LOW |
| W2-10 | round-2 W2-14 | MEDIUM → LOW |
| W13-01 | round-2 W1-20 | LOW → MEDIUM |
| W13-02 | round-2 W1-19（亦 round-1 W1-30 同面） | LOW → MEDIUM |
| W13-03 | round-2 W1-05 | MEDIUM → MEDIUM |
| W13-04 | round-2 W1-08 | MEDIUM → MEDIUM |
| W13-05 | round-1 W1-19（round-2 deferred） | MEDIUM → MEDIUM |
| W13-06 | round-1 W1-32（round-2 deferred） | MEDIUM → LOW |
| W13-07 | round-2 W3-02 | MEDIUM → LOW |
| W13-08 | round-2 W3-01 | MEDIUM → LOW |
| W13-09 | round-2 W1-04（亦 round-1 W1-34 同面） | MEDIUM → LOW |
| W13-10 | round-1 W1-24（round-2 deferred） | MEDIUM → LOW |

#### 2.2.4 Round-2 findings 未重报（25 条，prior evidence stands）

- **requirements 侧（16）**：W1-02、W1-03、W1-06、W1-07、W1-09、W1-10、W1-11、W1-12、W1-13、W1-14、W1-15、W1-16、W1-17、W1-18、W1-21、W1-22 —— 本轮未重报，未修复，按 round-2 证据保持 open。
- **plan/quickstart/契约侧（2）**：W2-13、W2-16 —— 未重报；**集成者抽验两条仍存在**：`plan.md` L135 仍写「scenarios S-0…S-11」而 L217 写 14 个场景（W2-13）；`plan.md` L79 XXI 行仍把 `event-wait C-004` 括注为「help-documented, zero-side-effect flags」（W2-16）。prior evidence stands。
- **tasks 侧（7）**：W3-03、W3-04、W3-05、W3-06、W3-07、W3-08、W3-09 —— 未重报，未修复，按 round-2 证据保持 open。

### 2.3 Round-1 residue delta（相对 round-2 的 deferred 46 条）

| 处置 | 条数 | 明细 |
|------|------|------|
| re-raised（本轮重报） | 7 | W1-19→W13-05、W1-24→W13-10、W1-32→W13-06、W2-01→W2-01+W2-02、W2-02→W2-04、W2-06→W2-06、W2-08→W2-08 |
| still deferred（未重报） | 39 | 其余 round-1 deferred 项；状态与 round-2 相同 |
| rejected / fixed（status quo） | 1 / 11 | round-2 的 W2-09 reject 与 11 条 fixed 结论不变 |

对账：46 = 7 + 39；round-1 全部 58 条 = fixed 11 + rejected 1 + deferred 46，无遗漏、无重复。

## 3. 跨制品一致性（Cross-Artifact Consistency）

以下簇把跨 requirements → plan/contracts → tasks 的同一缺陷面合并观察；**不改写任何单行严重度**，归属只指向单一决策 owner。

| 簇 | 成员（round-3 ID） | 共同缺陷 | 单一决策 owner |
|----|--------------------|----------|----------------|
| **X-1 基线/读数的生产者链断裂** | W2-01、W2-02、W13-02、W13-11 | 四个 MUST 级读数（基线槽命令、全量 id 集文件、运行期子进程调用数、失败名单基线文件）都被下游消费，但没有一个制品声明「谁、在哪一步、以哪条命令产出它」——S-12/S-13、T003、GATE-1 与 C-015 的输入在制品间互相指空 | quickstart S-12/S-13 + tasks T003（产出归属）；plan WP-9 对齐 |
| **X-2 守卫与扫描不判其所声称的性质** | W13-01、W2-03、W2-06、W2-09 | SC-010 声明三类判红形态但其规则与 Measurement Source 只承载一类；S-10 两条命令分别扫全文件与数新增行；S-1 把未排序输出喂 `comm`；WP-3 的 doc assertion 无测试文件与 owning clause——「零命中」在这些面上不可复算或可能假绿 | requirements（FR-021↔SC-010 与 FR-020）；quickstart S-1/S-10；plan WP-3 |
| **X-3 身份、枚举与口径未收敛到单一 owner** | W2-04、W2-05、W2-10、W13-03、W13-04、W13-05、W13-09、W13-10 | 缓存键成分（root/variant）、`c20` 的双重处置、`tier` 二值/三值、保留类闭集（copy-topology）、注入时钟的产品面（`--now`）、Shared Strings 消费列与新字面量、断言等价口径——需求与契约各留半份定义，读者无法判定以哪侧为准 | requirements 一次收敛（FR-015/FR-021/FR-025/FR-027/Shared Strings）；契约只回引 |
| **X-4 副本计数、标签与归属漂移** | W2-07、W2-08、W13-06、W13-07、W13-08 | 同一事实的副本各自计数：S-0 行数（6 vs 7）、`--full` 表面数（3 vs 4）、sleep 文件数（8 vs 10）；tasks 的归属表落后于行内 `[green:]` 标签、T012 的声明范围超前于 T021 的追加时点——与 one-source-of-truth 的预测一致 | plan/quickstart 副本单点拥有；tasks（行内标签是机器判据，表随标签） |

## 4. Checklist 问责（pass H）

- 对象: `checklists/suite-speed-2026-11-10.md`（34 项，全部 `- [ ]`；`[Gap]` 10 项）。
- 处置: **34/34 dispositioned**（round-2 全量映射维持）；本轮 re-raise 6 项 —— CHK012→W13-09、CHK015→W13-03、CHK021→W13-05（由 round-2 的 covered-by 改为 raised-as-finding，属本轮再裁决）、CHK026→W13-10、CHK028→W13-04、CHK034→W13-06。
- 10 个 `[Gap]` 项：9 项 raised（CHK009/012/015/017/020/021/024/027/028）、1 项 covered-by（CHK001 → §SC-010/§FR-021）。
- 可观察计数: `unchecked(0) + unraised(0) + undispositioned(0) = 0` → 不阻断。

## 5. Coverage Summary、Feature Linkage 与 Unmapped Tasks

| 指标 | 读数 | 证据 |
|------|------|------|
| FR 总数 / 已引用 | 27 / **27（pass）** | round-3 覆盖核算运行；`[fr-uncovered] pass (0) — 27 of 27` |
| FR 单行覆盖样本 | 8 个单行 FR 全抽读；7/8 成立，1 条归入 W13-02 | §0.1；`tasks.md` 逐行计数 |
| SC 总数 | 11（final 9 + supporting 2） | `requirements.md` §Measurable Outcomes |
| 任务行 | 61（T001–T061；60 `[ ]` + 1 `[~]`） | `tasks.md` 机械核验 |
| 契约条款宇宙 | 6 文件 / 68 条款（16/9/12/11/10/10） | `analyze-repair-gates-r3-2026-11-10.txt`；plan Phase 1 summary |
| 条款机器可判覆盖 | **68/68 claimed**（`[green:]` 每条款恰一次） | 覆盖核算运行；W13 机械核验；`validate-tasks.py` 0 error / 3 warning |
| 覆盖核算状态 | **`baseline-missing`（exit 2，阶段可见问题）**；冻结（T002）是 implement 起点义务，本阶段按 SKILL §3 未 `--freeze` | `test-evidence/analyze-coverage-accounting-round3-2026-11-10.txt` |
| 决策张力 | `status: ok`，errors 0 / warnings 0，3 records | 本轮 `validate-decision-tensions.py` 运行 |
| 未映射任务 | **0 条**；61 行全部落在相位/故事内，FR 27/27 经契约引用组被引用 | `validate-tasks.py` / 覆盖核算 |
| 宪法对齐问题 | **0 条（D 类）**；round-1/2 的唯一宪法冲突 W1-01 已关闭（§0.2） | 两波显式 0 C/H |
| Feature 绑定 | `FEATURE_ID=086` / `086 Efficient Test Execution (Concurrent by Default)`；状态保持 `Ready for Review`，不回退 | `.specify/features.md` L94；`.specify/features/086-efficient-test-execution.md` |
| Stage 记录 | 索引行最新 098 记录 = tasks；详情 `Last Updated` = 098 plan；checklist/analyze 未登记 → **G-01 维持（LOW, deferred）** | pass G 有界复查（§1） |

## 6. Systemic Observations

1. **R3 重锚是成立的**：上一轮 CRITICAL 的九处落点在当前文本中可逐条观测，round-3 检测未再发现任何「以慢档排除兑现提速判据」的残留表述——宪法 XX 冲突关闭，本轮不再有决策级冲突。
2. **剩余 21 条全是簿记/可判定性缺陷**：其中 X-1（生产者链）风险最高——S-12/S-13、T003、GATE-1 与 C-015 在 implement 第一步（T003 基线槽）就会互相指空；若按现状执行，基线读数与失败名单文件可能既无出处也无落点。
3. **修复轮引入的 tasks 分析债仍在**：W13-07/W13-08 是 round-2 W3-01/W3-02 的原面重报（本轮以 LOW 重报，未修复）——`[green:]` 行内标签是机器判据，§ Clause Attribution 表仍是过期副本；implement 不应把表当真值来源。
4. **扫描命令的假绿风险集中在 quickstart**：S-10 的两条命令与 S-1 的 `comm` 都不度量其 Proves 文本声称的性质（W2-03/W2-06）——照抄执行会得到「绿」但证明力为零，属比缺失更隐蔽的缺陷。
5. **两波读域互斥且合并全覆盖**：W13 覆盖 requirements/checklists/tasks，W2 覆盖 plan/data-model/quickstart/contracts；0 C/H 的结论因此是一次干净的全覆盖重检，而非仅后备箱结清。

## 7. Metrics

- **新增**: 21 条 = CRITICAL 0 / HIGH 0 / MEDIUM 10 / LOW 11；主表 21 行（≤50）；overflow 0。
- **Rerun delta**: round-2 新增 36 条 → fixed 2 / carried 9 / 未重报 25；round-1 deferred 46 → re-raised 7 / still deferred 39；rejected 1 与 fixed 11 维持。
- **验证**: C/H 送审 0、validated 0、proposed 0、reject 0、downgrade 0（本轮无 C/H）；零 C/H 样本 8 个单行 FR + 5 组上下文。
- **类别分布（新增行）**: A 0 · B 2（W2-05、W13-10）· C 4（W13-02/03/05/09）· D 0 · E 5（W2-02、W2-09、W13-01、W13-04、W13-11）· F 10 · G 0。
- **Checklist**: 34/34 disposed；10 `[Gap]` 全部 raised/covered；undispositioned 0；本轮 re-raise 6。
- **覆盖核算**: exit 2；`baseline-missing`（预期 pre-T002）；claimed clauses 68；FR 27/27 pass；scanned files 292；clause universe 2067。
- **并发**: 检测波并发 N=2（W13 文件自记；W2 + W13 两波读域互斥）；本阶段为串行集成（职责定义），不另记并发读数。
- **同源检测**: 不适用——被检制品由更早 SDD 阶段作者产出，非本轮任一检测波；集成者不产生检测行。

## 8. Artifacts Untouched 与只读证明

- `requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`quickstart.md`、`contracts/*`（6）、`checklists/*`、`feature-ref.md`、`research.md`、`.specify/features.md`、`.specify/features/086-efficient-test-execution.md` **零修改**（本阶段无 Edit/Write 作用于这些路径）。
- 本阶段唯一写入：本报告、`test-evidence/analyze-coverage-accounting-round3-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback；按派发纪律不提交）。
- 两份 worker findings 文件为本阶段输入，原样保留；单一 closing commit 只包含其与上述两份证据。

## 9. Next Actions（不自动修复）

- **CRITICAL/HIGH：无** → 门禁为 PASS；`/speckit.implement` 不被阻断。
- **MEDIUM（10 条）** → 建议在 implement 触碰对应面之前收敛，优先序：X-1（S-12/S-13 + T003 + GATE-1 的产出归属，最先到期）→ X-3（requirements 一次收敛）→ X-2（守卫/扫描判据）。
- **LOW（11 条）** → 建议随各 owner 批量收敛；X-4（tasks 归属表 + 副本计数）成本最低。
- 修复后若需新一轮 gate 读数，重跑 `/speckit.analyze`（Round 4）产生新的 rerun delta；未修复的 MEDIUM/LOW 不会阻断实现。
