# Analyze 第二轮 Findings — W1（并发波）

- **Round**: 2（修复后重过门；rerun after remediation）
- **Worker**: W1
- **Read domain（文件级互斥）**: `.specify/specs/098-suite-speed-optimizations/requirements.md`、`.specify/specs/098-suite-speed-optimizations/checklists/suite-speed-2026-11-10.md`
- **判据来源**: 分析契约 `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md`；宪法 `.specify/constitution.md`；判据 owner `.specify/shared/guidelines/test-execution-efficiency.md`
- **方法**: 对读域执行 pass A（重复）/ B（歧义）/ C（欠指定）/ D（宪法对齐）/ F（一致性）/ H（checklist 问责）；pass E（requirements↔tasks 覆盖）与 G（feature registry 联动）不在本 worker 读域，pass I（Decision Tensions，判据对象为 plan.md）不在读域——由协调者合并其他 worker 结果
- **只读声明**: 未修改任何产物；本文件为分配到 EVIDENCE_DIR 的输出
- **Delta 说明**: 第一轮 W1 findings 文件不在本 worker 读域（文件级互斥），round-1 residue 的枚举与 delta 由协调者按 SKILL §Rounds 合并；本文件为对修复后文本的全集新检测
- **覆盖记账**: §3 coverage accountant 属协调者固定步骤（`analyze-coverage-accounting-2026-11-10.txt` 已在证据目录）

## Findings（22 行；1 CRITICAL / 10 MEDIUM / 11 LOW）

| ID | Severity | Anchors | 一句话事实 | 建议归属 |
|----|----------|---------|-----------|----------|
| W1-01 | **CRITICAL** | requirements.md:28（Overview 合规断言）、:147（FR-007 缺省排除）、:170（FR-021）、:205（SC-004）、:252（A3）；constitution.md §XX（:439「a faster run MUST NOT be bought by shrinking the selection」）；test-execution-efficiency.md:93（不可采纳：「标记排除…换取数字下降」「在任何情形下」）、:80（测量锚点「同一选择」）、:74（默认排除一类标记即缩小 selection） | FR-007 的缺省档以 `slow` 标记排除换取更快的缺省运行，SC-004 又以「缺省档墙钟 ≤ 全量基线 50%」作为 final 验收——这正是宪法 XX 明文禁止的「以缩小选择换取更快的运行」，其判据 owner 更把「标记排除换取数字下降」列为任何情形下不可采纳，并规定效率比较必须「两次运行覆盖同一测试集合」；FR-021「MUST NOT 以该清单中的任何方式兑现任何 SC」因此与 FR-007/SC-004 自相矛盾，需求文本的「不改变测试覆盖选择」不能自证合规。 | `/speckit.clarify` 或 `/speckit.requirements` 做机制裁决：保留缺省排除必须先完成 **analyze 之外的显式宪法修订**（用户裁决，技能禁止以重解释消化 MUST）；否则应改为缺省全量 + 显式快档开关（A3 已列的被否决替代设计），并重写 SC-004 为同选择比较。若第一轮已就本条给过 disposition，请复核其是否属于技能禁止的 reinterpreting。 |
| W1-02 | MEDIUM | requirements.md:140（FR-003）、:203（SC-002）、:217（SC-002 Source） | FR-003/SC-002 的 contract 子树「并行 vs 串行」验证未钉死档位：缺省档会排除 `slow` 标记的 contract 测试（恰含全语料扫描型），使「tests/contract 名称级一致」的覆盖集合不可判定，并与 FR-003 自身「MUST NOT 只验证子集」的边界不清。 | `/speckit.requirements`（补档位/选择口径）或 plan 契约面显式声明 |
| W1-03 | MEDIUM | requirements.md:168（FR-019）、:210（SC-009）、:26（Overview 499 引用基线） | FR-019/SC-009 的转换清单完备性没有分母：计数单位（调用点/源码行/wrapper）与普查总体（AST 扫描范围、是否含 fixtures/conftest、是否排除嵌套树）未定义，「非边界调用点为 0」不可复算，改回突变的清单断言只能证明已列入者的判别力、不能证明无漏转。 | `/speckit.requirements`（定义普查口径）或 plan 的转换清单契约 |
| W1-04 | MEDIUM | requirements.md:173（FR-024）、:207（SC-006）、:228-234（Shared Strings） | 守门测试逐字消费的 `tier=fast/full/caller` 与运行形态行披露字段、以及登记册「类别」取值，均未进入 Shared Strings、未被任何单一定义点拥有（现表只有 STR-001…003）。 | `/speckit.requirements`（扩展 Shared Strings 或声明字段 owner） |
| W1-05 | MEDIUM | requirements.md:174（FR-025）；checklist:33（CHK015 记录设计增补 `root`/`variant`） | FR-025 的缓存键只声明（会话，worker，受管扫描面），而 checklist 记录设计在键中加入 `root` 与 `variant`——需求未拥有这两个身份成分，入口身份不可在需求层判定。 | `/speckit.requirements`（键成分归需求）或 plan 显式声明并回引 FR-025 |
| W1-06 | MEDIUM | requirements.md:146（FR-006）、:192（Key Entities 慢档标记） | FR-006(b) 用「少数」界定全语料 contract 成员，全篇无成员数上限或占比上限——slow 成员增长只能被披露、不能被阻止，缺省档可被逐步蚕食而仍「合规」。 | `/speckit.requirements`（给出上限或可判定边界） |
| W1-07 | MEDIUM | requirements.md:146（FR-006） | FR-006(a)「integration 类测试」未说明按目录、marker 还是行为界定：行为上拉起/等待进程却位于 `tests/contract` 的用例（如 FR-016 所列 `test_line_envelope_contract.py`）是否具 slow 资格不可判定。 | `/speckit.requirements` |
| W1-08 | MEDIUM | requirements.md:176（FR-027）、:260（A11）；checklist:52（CHK028 记录设计依赖 `copy-topology`） | FR-027/A11 的保留类枚举是封闭清单且不含 checklist 记录设计所依赖的 `copy-topology` 类——该类调用点在二值归类中没有落点（保留侧缺口）。 | `/speckit.requirements` 与 plan 对齐保留类闭集 |
| W1-09 | MEDIUM | requirements.md:150（FR-010）、:243（Clarifications Q2） | FR-010 要求「驱动者文档」两槽位命令显式请求全量档，但未给出该文档的 owner 路径，更新目标不可追溯。 | `/speckit.requirements`（命名 owner 路径） |
| W1-10 | MEDIUM | requirements.md:147（FR-007）、:149（FR-009）、:173（FR-024） | 「调用方自带 `-m`」只按命令行拼写判定：pytest 配置 `addopts` 提供的 `-m` 对 runner 不可见，缺省前置的 `-m "not slow"` 会压过它且披露为 0，下游项目经同一 runner 的选择可被静默收窄。 | `/speckit.requirements`（定义 caller-`-m` 检测面）或 runner 档位契约 |
| W1-11 | MEDIUM | requirements.md:205-206（SC-004/SC-005）、:169（FR-020）、:258（A9） | SC-004 的 50% 与 SC-005 的 110% 墙钟阈值未规定单次读数还是重复测量、也未给方差容忍，验收读数不可复现（A9 禁止为度量新增第三次全量运行，使重复测量空间受限）。 | `/speckit.requirements`（测量协议）或 plan 的度量契约 |
| W1-12 | LOW | requirements.md:203（SC-002）vs :204（SC-003） | SC-003 写明「既存失败按名称相等处理」而 SC-002 只有「双向差为空」——同一比较约定在两条成功判据间不对称。 | `/speckit.requirements`（措辞对齐） |
| W1-13 | LOW | requirements.md:146（FR-006） | 同时满足两类 slow 判据（进程边界 + 全语料扫描）的测试没有归类规则，登记册「类别」列取值不可判定。 | `/speckit.requirements`（一条二义归类规则） |
| W1-14 | LOW | requirements.md:156（FR-013）、:157（FR-014） | FR-013 的「改写被扫描树的用例 MUST NOT 消费共享缓存」没有守门检测面（如何发现违规消费），只能靠评审。 | plan/implement（补检测面）或 requirements 声明评审面 |
| W1-15 | LOW | requirements.md:163（FR-017）、:209（SC-008） | FR-017 要求真实时间语义等待「逐条记录理由并列入豁免清单」，但未规定清单的载体路径与行模式（文件、行、理由、日期），扫描守卫无法机器消费。 | `/speckit.requirements`（豁免清单 schema） |
| W1-16 | LOW | requirements.md:168（FR-019） | 转换清单的分类粒度未定义：一个 wrapper 辅助函数包裹多处调用时，按 wrapper 一行还是按调用点逐行计数不可判定。 | `/speckit.requirements`（计数单位） |
| W1-17 | LOW | requirements.md:172（FR-023）、:212（SC-011） | 「`mode=` 行保持前缀兼容」没有可判定不变量（既有字段位置/拼写不变、新字段尾部追加、分隔符与既有解析不受影响），仍是隐喻。 | `/speckit.requirements` 或 098 契约面 |
| W1-18 | LOW | requirements.md:172（FR-023） | 「C-001…C-016 条款文本 MUST NOT 被重开或改写」没有检查面（如 086 契约文件在变更 diff 中逐字不变），只是意图声明。 | `/speckit.requirements`（给检查形态）或 plan 契约 |
| W1-19 | LOW | requirements.md:169（FR-020） | 「运行期子进程调用数」的测量方法未定义（动态调用计数 vs 静态 AST 普查），同一指标不可复现。 | `/speckit.requirements`（测量方法） |
| W1-20 | LOW | requirements.md:170（FR-021）、:211（SC-010） | SC-010 的参数化守卫只比较「条目数」总量且未定义范围（逐文件 vs 全局），也不覆盖「随机丢参」形态——缩小参数化的禁止无法完全机检。 | `/speckit.requirements`（比较范围 + 丢参规则） |
| W1-21 | LOW | requirements.md:155（FR-012）、:174（FR-025） | 共享缓存的「受管扫描面」与「框架根文件」未被枚举，「每个面每会话至多一次」缺少可枚举的判定边界（A6 的数据清单豁免只覆盖 slow 成员与直调清单，不覆盖此集合）。 | `/speckit.requirements` 或 plan 数据 |
| W1-22 | LOW | requirements.md:170（FR-021）vs :175（FR-026） | FR-021 把「等待截止被放宽到超过 FR-026 的上限」一律判红，而 FR-026 允许 >30 秒截止逐条记录理由——同一行为两侧判定相反。 | `/speckit.requirements`（对齐判红条件与豁免） |

## Checklist 问责（pass H）

清单共 34 项全部未勾选。以下为全部 34 项的处置映射；`[Gap]` 标记 10 项全部满足「raised or dispositioned」，`unchecked + unraised + undispositioned = 0`。

### `[Gap]` 项（10/10）

- CHK001 disposition: covered-by requirements.md § SC-010（`xfail`/`skip`/重试装饰器扫描）+ § FR-021（owner 清单为唯一判据；A12 禁新增第三方依赖，flaky 插件形态不可出现）
- CHK009 disposition: raised-as-finding W1-13
- CHK012 disposition: raised-as-finding W1-04
- CHK015 disposition: raised-as-finding W1-05
- CHK017 disposition: raised-as-finding W1-14
- CHK020 disposition: raised-as-finding W1-15
- CHK021 disposition: covered-by requirements.md § Key Entities（注入时钟 = 测试夹具输入，只影响测试内时间戳来源）+ § A12
- CHK024 disposition: raised-as-finding W1-03
- CHK027 disposition: raised-as-finding W1-16
- CHK028 disposition: raised-as-finding W1-08

### 其余 24 项

- CHK002 covered-by § SC-010（AST + 文本双通道覆盖函数体内 `pytest.skip(`/`pytest.xfail(`、条件跳过、重试至绿循环）
- CHK003 raised-as-finding W1-20
- CHK004 raised-as-finding W1-20
- CHK005 raised-as-finding W1-12
- CHK006 covered-by § SC-004（「作为反度量记录」= 观察记录而非判据）
- CHK007 raised-as-finding W1-06
- CHK008 raised-as-finding W1-07
- CHK010 covered-by § FR-024（`tier=caller` 排除数 MUST 为 0）
- CHK011 covered-by § FR-024（`--full` 条款已按「无调用方 `-m`」条件化，并与 FR-009 一致）
- CHK013 covered-by § FR-024（孤儿行守卫强制登记册随解标记更新）
- CHK014 raised-as-finding W1-10
- CHK016 raised-as-finding W1-21
- CHK018 covered-by § FR-025（首次消费构建一次、按会话重建）+ § FR-013（共享输入只读，无顺序依赖）
- CHK019 covered-by § FR-016（三文件闭集）、§ FR-017（六文件闭集）、§ SC-008
- CHK022 covered-by § FR-017（作用域内计数为零 + 保留逐条豁免即机械规则）
- CHK023 covered-by § FR-026 + § A16（5.0 秒共享缺省调为 30 秒已明示为规格内行为变更）
- CHK025 covered-by § FR-027（保留类枚举 + 其余直调）+ § Edge Cases（不可恢复全局状态归保留）
- CHK026 covered-by § FR-019 + § FR-027 + § SC-009（同一断言集前后全绿；退出码断言有 CliRunner 等价物明文）
- CHK029 raised-as-finding W1-17
- CHK030 raised-as-finding W1-18
- CHK031 raised-as-finding W1-09
- CHK032 raised-as-finding W1-19
- CHK033 raised-as-finding W1-11
- CHK034 covered-by § A6（探针读数是基线读数、非验收常量）+ § FR-017/SC-008（验收范围为六文件闭集的零计数）；附注：清单所述「tasks 阶段 20 处/10 文件」与 § Overview「20 处/8 文件」的跨产物差异在本 worker 读域外，交协调者与 tasks 域核对

## 系统性观察

1. **CRITICAL 的根因是决策级冲突，不是措辞**：用户 Input 明示要「PR 默认 `-m "not slow"`」，而宪法 XX 的判据 owner 明文把「标记排除换取数字下降」列为任何情形不可采纳、并要求效率比较同选择。两者不能靠需求文本自证并存；解决路径只有「改机制（缺省全量 + 显式快档）」或「用户裁决后走 analyze 之外的显式宪法修订」。
2. **M/L 残留集中在守卫面的可判定性**：登记册字段、豁免清单 schema、转换清单分母、参数化比较范围、档位字段字面量——守卫测试的面已命名，但分母/owner 未钉死（W1-03/04/15/19/20 同族）。
3. **本 worker 未发现的类别**：pass E（requirements→tasks 覆盖）与 pass G（feature registry/086 联动）不在读域，不能宣称无发现；`Status: Draft` 与 Related Feature 绑定的注册表事实亦未核（读域外）。

## Scope Limits

- 本文件不是最终 gate 报告：findings 的独立验证（CRITICAL/HIGH 波）、round-1 residue 枚举、coverage 摘要与 delta 由协调者合并产出。
- W1-01 需要在协调者的验证波中由独立 fresh-context 验证者判定 `confirm`（宪法冲突不可 downgrade）。
