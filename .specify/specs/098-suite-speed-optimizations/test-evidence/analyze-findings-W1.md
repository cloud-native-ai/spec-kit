# Analyze Findings — W1（098-suite-speed-optimizations）

- **Stage**: analyze / concurrent wave W1（只读检测波）
- **Round**: 1（`test-evidence/` 下无既有 analyze 报告，无 rerun delta）
- **Date**: 2026-11-10
- **Read domain**: `.specify/specs/098-suite-speed-optimizations/requirements.md`、`.specify/specs/098-suite-speed-optimizations/checklists/suite-speed-2026-11-10.md`
- **Authority read**: `.specify/constitution.md`、`.specify/skills/internal/analyze-artifacts/SKILL.md` 及其 `references/detection-and-severity.md`、`references/validation-and-report.md`
- **Mode**: strictly read-only；未修改任何制品，未执行修复。

## Scope & Limits

- 已应用的 pass：A 重复、B 歧义、C 欠指定、D 宪法对齐、F 不一致、H checklist 问责（全部限定在读域内）。
- 未在 W1 评估：pass E 覆盖缺口、pass G feature registry/linkage、pass I decision tensions——`tasks.md`、`plan.md`、`contracts/` 与 `.specify/features/` 不在 W1 读域，由 analyze 主报告的其它波次承担。
- `scripts/python/account-clause-coverage.py` 未在 W1 运行（同一读域理由），由 analyze 主阶段承担。
- CRITICAL/HIGH 行为 W1 检测结论，尚待独立验证波裁决；MEDIUM/LOW 按契约跳过验证。
- W1 未参与被检制品写作，不构成 self-review。

## Findings

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|----|----------|------|------------|----------|
| W1-01 | CRITICAL | `requirements.md` §Overview (L28) / §FR-021 (L170) vs `constitution.md` §XX (L438–439)；checklist CHK001 (L13) | FR-021 的规范性禁止清单重述了宪法 XX 拥有的捷径集却漏掉「宣告 flaky」，Overview 与宪法 XX 都禁止它，重述已发生漂移且未按宪法 XX 的指针规则引用 owner。 | requirements §FR-021（对齐宪法 XX 的 owner，仅保留 098 特有增量） |
| W1-02 | HIGH | `requirements.md` §SC-010 (L211) / §Measurement Sources SC-010 (L225) / §FR-021 (L170)；checklist CHK002 (L14) | SC-010 的度量源只统计「新增的 skip / xfail / 重试装饰器」，函数体内 `pytest.skip()`、条件跳过与手写重跑至绿循环不在检测面内，禁止捷径缺席的全称谓断言不覆盖其类别。 | requirements §SC-010 / §FR-021（定义非装饰器形式的检测面） |
| W1-03 | MEDIUM | `requirements.md` §FR-021 (L170)；checklist CHK003 (L15) | FR-021 的「无上限 worker 数」与「随机丢参」没有具名上限或可比口径，出现时无法机械判红。 | requirements §FR-021 |
| W1-04 | MEDIUM | `requirements.md` §FR-021 (L170) / §SC-010 (L211)；checklist CHK004 (L16) | FR-021 / SC-010 的「缩小参数化」只给「参数化条目数不减少」，未定义比较单位（逐文件/逐测试）与范围，减参可能漏检。 | requirements §FR-021 / §SC-010 |
| W1-05 | MEDIUM | `requirements.md` §FR-006 (L146)；checklist CHK007 (L22) | FR-006 的「少数」全语料扫描型 contract 测试没有数量或占比上限，成员增长可在「已披露」下持续缩小缺省档。 | requirements §FR-006 |
| W1-06 | MEDIUM | `requirements.md` §FR-006 (L146)；checklist CHK008 (L23) | FR-006 未定义「integration 类测试」的判定基（目录、marker 还是行为），`tests/contract` 下的进程边界测试是否可入慢档不可判定。 | requirements §FR-006 |
| W1-07 | MEDIUM | `requirements.md` §FR-006 (L146) / §FR-024 (L173)；checklist CHK009 (L24) | FR-006 的两类成员判据未规定同时满足两类时的归类规则，而 FR-024 的登记册每条只记一个「类别」，双属测试的登记值不可判定。 | requirements §FR-006 / §FR-024 |
| W1-08 | HIGH | `requirements.md` §FR-024 (L173) vs §FR-007 (L147) / §FR-009 (L149)；§Clarifications Q2 (L243)；checklist CHK010 (L25) | FR-024 的「披露排除数 = 本次选择内 slow 成员数」未按档位限定：调用方自带 `-m` 时 slow 成员被选中而非排除，排除数应为 0，与 FR-007 / FR-009 的 caller-tier 语义冲突。 | requirements §FR-024 与 §FR-007 / §FR-009（按 tier 限定披露算式） |
| W1-09 | HIGH | `requirements.md` §FR-024 (L173) vs §FR-009 (L149)；§FR-008 (L148) 的「完整选择」；checklist CHK011 (L26) | FR-024 的「`--full` 时收集集合回到全量」与 FR-009「调用方 `-m` 在 `--full` 下仍拥有选择」冲突，`--full` + 调用方 `-m` 时不会回到全局全量。 | requirements §FR-024 与 §FR-009（限定为无调用方 `-m`） |
| W1-10 | MEDIUM | `requirements.md` §Shared Strings (L232–L234) / §FR-024 (L173)；checklist CHK012 (L27) | Shared Strings 只钉了 STR-001…003，登记册类别值、登记册路径与运行形态行新增字段名（`tier=` / `excluded_slow=`）被守门测试逐字消费却没有单一 owner。 | requirements §Shared Strings / §FR-024（补钉或声明 owner） |
| W1-11 | LOW | `requirements.md` §FR-024 (L173)；checklist CHK013 (L28) | FR-024 只规定孤儿行使守门转红，未规定成员失去判据时由谁、按什么步骤更新登记册；移除路径不可追踪。 | requirements §FR-024 或 plan（登记册维护程序） |
| W1-12 | MEDIUM | `requirements.md` §FR-009 (L149)；checklist CHK014 (L29) | FR-009 的「调用方自带 `-m`」未定义检测面：仅命令行拼写，还是也含 pytest 配置（`addopts`）注入的选择；下游用 shipped runner 时「不产生两个 `-m`」不可判定。 | requirements §FR-009 |
| W1-13 | MEDIUM | `requirements.md` §FR-025 (L174)；checklist CHK015 (L33) | FR-025 的缓存键只拥有（会话、worker、受管扫描面），而 checklist 记录设计另加 `root` 与 `variant`；决定条目身份的成分未全部由需求拥有。 | requirements §FR-025 与 plan（缓存键单一 owner） |
| W1-14 | MEDIUM | `requirements.md` §FR-012 (L155) / §FR-025 (L174)；checklist CHK016 (L34) | FR-012 / FR-025 未枚举「受管扫描面」与「框架根文件」的具体集合，「每面每会话一次」无法脱离设计查找判定。 | requirements §FR-012 / §FR-025 |
| W1-15 | MEDIUM | `requirements.md` §FR-013 (L156) / §FR-014 (L157)；checklist CHK017 (L35) | FR-013 禁止改写树者消费共享缓存，但 FR-014 的突变只证明内容篡改会转红，没有发现「改写者消费了共享缓存」的检测面。 | requirements §FR-013 / §FR-014 |
| W1-16 | LOW | `requirements.md` §FR-025 (L174)；checklist CHK018 (L36) | FR-025 的会话内快照语义未写明快照取于会话起点还是首次消费时刻，按现有文字可能隐含消费顺序依赖。 | requirements §FR-025 |
| W1-17 | HIGH | `requirements.md` §SC-008 (L209) / §FR-016 (L162) / §FR-017 (L163)；§Measurement Sources SC-008 (L223)；checklist CHK019 (L40) | SC-008 的零计数声明以「runner 相关测试」为作用域，但 FR-016 未枚举文件集合；该全称否定断言缺少可判定的边界。 | requirements §FR-016 / §FR-017 / §SC-008（枚举作用域） |
| W1-18 | MEDIUM | `requirements.md` §FR-017 (L163)；checklist CHK020 (L41) | FR-017 要求保留的真实时间语义 sleep 列入豁免清单，但未规定清单载体路径与行模式，扫描守门无法消费。 | requirements §FR-017 或 plan（豁免清单 owner） |
| W1-19 | MEDIUM | `requirements.md` §FR-015 (L161) / §A12 (L261)；checklist CHK021 (L42) | A12 的范围外清单对产品代码改动沉默，FR-015 未说明注入时钟可以是 shipped engine 的新选项还是必须留在测试侧。 | requirements §FR-015 / §A12 |
| W1-20 | MEDIUM | `requirements.md` §FR-017 (L163)；checklist CHK022 (L43) | FR-017 的「承担同步或顺序语义的 `time.sleep`」与 TTL 等真实时间语义之间没有可判定的分类规则，只剩逐例豁免判断。 | requirements §FR-017 |
| W1-21 | HIGH | `requirements.md` §FR-026 (L175) / §A16 (L265) / §Clarifications Q4 (L245)；checklist CHK023 (L44) | FR-026 / §A16 声称 30 秒截止「与既有 runner 测试约定一致」，而 checklist 记录 tasks 阶段实测共享等待辅助的当前缺省为 5 秒；共享缺省的行为变更未被声明。 | requirements §FR-026 / §A16 与 tasks/plan 的等待辅助对齐（或声明变更） |
| W1-22 | MEDIUM | `requirements.md` §FR-019 (L168)；checklist CHK024 (L48) | FR-019 的转换清单未定义完整性分母：计数单位（调用点/源码行/helper）与普查人群（`tests/` 是否含 fixtures 与 conftest 的 AST 扫描）。 | requirements §FR-019 |
| W1-23 | MEDIUM | `requirements.md` §FR-027 (L176)；checklist CHK025 (L49) | FR-027 的保留优先规则未写成穷尽式（任一保留类成立即保留，其余才转换），也未规定不属于任何列类且无法转换的调用如何处置。 | requirements §FR-027 |
| W1-24 | MEDIUM | `requirements.md` §FR-019 (L168) / §FR-027 (L176) / §SC-009 (L210)；checklist CHK026 (L50) | FR-019 要求「同等行为断言」、SC-009 要求「同一断言集合全绿」，FR-027 又允许断言改为 CliRunner 等价结果；何为等价没有可判定的比较规则。 | requirements §FR-019 / §FR-027 / §SC-009 |
| W1-25 | MEDIUM | `requirements.md` §FR-019 (L168)；checklist CHK027 (L51) | FR-019 未定义 helper wrapper 的分类单位（每个 wrapper 一行还是每个被包裹调用点一行），清单完整性不可计数。 | requirements §FR-019 |
| W1-26 | MEDIUM | `requirements.md` §FR-027 (L176) / §A11 (L260)；checklist CHK028 (L52) | FR-027 / §A11 的保留边界枚举未包含 checklist 记录的设计所依赖的 `copy-topology` 类。 | requirements §FR-027 / §A11 |
| W1-27 | MEDIUM | `requirements.md` §FR-023 (L172)；checklist CHK029 (L56) | FR-023 的「前缀兼容」没有可判定不变量（既有字段位置与拼写不变、新增字段只在尾部追加、分隔符与既有解析不受影响）。 | requirements §FR-023 与 098 契约面（定义不变量） |
| W1-28 | LOW | `requirements.md` §FR-023 (L172)；checklist CHK030 (L57) | FR-023 的「C-001…C-016 条款文本 MUST NOT 被重开或改写」未给出检查形态（如 086 契约文件在 diff 中不变），仍是意图陈述。 | requirements §FR-023 或 tasks（漂移守门） |
| W1-29 | MEDIUM | `requirements.md` §FR-010 (L150)；checklist CHK031 (L58) | FR-010 的「驱动者文档」没有 owner 路径，两槽位 `--full` 更新无法追踪到具名文件。 | requirements §FR-010 |
| W1-30 | MEDIUM | `requirements.md` §FR-020 (L169)；checklist CHK032 (L62) | FR-020 的「运行期子进程调用数」未定义测量方法（动态调用计数还是静态 AST 普查），同一数字不可复现。 | requirements §FR-020 |
| W1-31 | MEDIUM | `requirements.md` §SC-004 (L205) / §SC-005 (L206)；checklist CHK033 (L63) | SC-004 的 50% 与 SC-005 的 110% 墙钟阈值未定义运行间波动的容忍度（单次运行还是重复测量）。 | requirements §SC-004 / §SC-005 |
| W1-32 | MEDIUM | `requirements.md` §Overview (L30) / §A6 (L255)；checklist CHK034 (L64) | Overview 记录 `time.sleep`「20 处 / 8 文件」，checklist 记录 tasks 阶段重算为「20 处 / 10 文件」；§A6 只说基线读数非常量，未决定验收采用哪一读法。 | requirements §Overview / §A6 与 tasks 证据（统一计数口径） |
| W1-33 | MEDIUM | `requirements.md` §Runtime Stack & Dependency Ownership (L184–L187) | Runtime Stack 表的 Premises 列引用 EP-001…EP-004，但本制品内没有任何 EP 定义或指向其 owner 的路径。 | requirements §Runtime Stack & Dependency Ownership（定义或指向 premises owner） |
| W1-34 | LOW | `requirements.md` §Shared Strings (L232–L234) vs §FR-007 (L147) / §FR-024 (L173) | Shared Strings 的 Consumed by 列遗漏 FR-007 与 FR-024 对 STR-001 / STR-003 的消费，消费枚举已过期。 | requirements §Shared Strings |

**Severity tally**: 1 CRITICAL / 5 HIGH / 24 MEDIUM / 4 LOW = 34.

## Checklist Accountability（pass H）

所有 34 个 unchecked 项均已处置；其中 10 个 `[Gap]` 项全部升为 finding，`undispositioned = 0`。

| Item | Tag | Disposition |
|------|-----|-------------|
| CHK001 | Gap | CHK001 disposition: raised-as-finding W1-01 |
| CHK002 | Coverage | CHK002 disposition: raised-as-finding W1-02 |
| CHK003 | Ambiguity | CHK003 disposition: raised-as-finding W1-03 |
| CHK004 | Clarity | CHK004 disposition: raised-as-finding W1-04 |
| CHK005 | Consistency | CHK005 disposition: covered-by requirements.md §SC-002/§SC-003（同树运行的「双向差为空」已蕴含既存失败按名称相等；SC-003 条款为显式澄清，行为约定相同） |
| CHK006 | Measurability | CHK006 disposition: covered-by requirements.md §SC-004（50% 阈值是规范判据；「读数应回退」原文标注为反度量记录，不是 pass/fail 判据） |
| CHK007 | Ambiguity | CHK007 disposition: raised-as-finding W1-05 |
| CHK008 | Ambiguity | CHK008 disposition: raised-as-finding W1-06 |
| CHK009 | Gap | CHK009 disposition: raised-as-finding W1-07 |
| CHK010 | Conflict | CHK010 disposition: raised-as-finding W1-08 |
| CHK011 | Conflict | CHK011 disposition: raised-as-finding W1-09 |
| CHK012 | Gap | CHK012 disposition: raised-as-finding W1-10 |
| CHK013 | Completeness | CHK013 disposition: raised-as-finding W1-11 |
| CHK014 | Ambiguity | CHK014 disposition: raised-as-finding W1-12 |
| CHK015 | Gap | CHK015 disposition: raised-as-finding W1-13 |
| CHK016 | Ambiguity | CHK016 disposition: raised-as-finding W1-14 |
| CHK017 | Gap | CHK017 disposition: raised-as-finding W1-15 |
| CHK018 | Clarity | CHK018 disposition: raised-as-finding W1-16 |
| CHK019 | Ambiguity | CHK019 disposition: raised-as-finding W1-17 |
| CHK020 | Gap | CHK020 disposition: raised-as-finding W1-18 |
| CHK021 | Gap | CHK021 disposition: raised-as-finding W1-19 |
| CHK022 | Clarity | CHK022 disposition: raised-as-finding W1-20 |
| CHK023 | Assumption | CHK023 disposition: raised-as-finding W1-21 |
| CHK024 | Gap | CHK024 disposition: raised-as-finding W1-22 |
| CHK025 | Clarity | CHK025 disposition: raised-as-finding W1-23 |
| CHK026 | Conflict | CHK026 disposition: raised-as-finding W1-24 |
| CHK027 | Gap | CHK027 disposition: raised-as-finding W1-25 |
| CHK028 | Gap | CHK028 disposition: raised-as-finding W1-26 |
| CHK029 | Clarity | CHK029 disposition: raised-as-finding W1-27 |
| CHK030 | Measurability | CHK030 disposition: raised-as-finding W1-28 |
| CHK031 | Traceability | CHK031 disposition: raised-as-finding W1-29 |
| CHK032 | Ambiguity | CHK032 disposition: raised-as-finding W1-30 |
| CHK033 | Measurability | CHK033 disposition: raised-as-finding W1-31 |
| CHK034 | Consistency | CHK034 disposition: raised-as-finding W1-32 |

## Systemic Observations（不改变任何单行 severity）

- **机器可消费面缺少单一 owner**：W1-10、W1-13、W1-18、W1-22、W1-25、W1-34 指向同一模式——登记册、缓存键、豁免清单、转换清单与 Shared Strings 都声称机器可读，但字段名、载体路径或计数单位未由单一 owner 钉死。合并处置应在 plan 阶段一次性收敛，而不是逐条补字。
- **全称否定型 SC 的度量面偏窄**：W1-02 与 W1-17 都让一个「为零」的成功判据依赖未闭合的检测面；这是 gate 级风险簇，建议主报告在裁决 CRITICAL/HIGH 时合并观察。
- **086 接口稳定性承诺缺少可检查的不变量**：W1-27、W1-28、W1-29 指向同一类问题——`前缀兼容`、`条款文本不重开`、`驱动者文档` 都还停留在意图层；098 自己的契约面应在 plan 阶段定义漂移守门。
- **跨阶段事实漂移**：W1-21（30 秒 vs 实测 5 秒）与 W1-32（8 文件 vs 10 文件）说明 requirements 继承的阶段外读数需要在 implement 前统一口径；§A6 只声明「基线不是常量」，没有决定验收读法。

## Artifacts Untouched

- `requirements.md` 未改动；`checklists/suite-speed-2026-11-10.md` 未改动（保持全部 `- [ ]`）。
- 唯一写入：本文件 `test-evidence/analyze-findings-W1.md`。
