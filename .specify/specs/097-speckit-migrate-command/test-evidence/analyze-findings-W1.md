# Analyze Findings — W1

**Feature**: 097-speckit-migrate-command
**Stage**: analyze（并发波 W1）
**Date**: 2026-11-10
**Read domain**: `.specify/specs/097-speckit-migrate-command/requirements.md`；`.specify/specs/097-speckit-migrate-command/checklists/requirements-quality-2026-11-10.md`
**Method**: analyze-artifacts 检测通道 A（重复）/ B（歧义）/ C（欠指定）/ D（宪法对齐）/ E（覆盖缺口）/ F（不一致）+ H（checklist 问责）；严格只读，不做修复。
**Same-author**: 两份输入由本轮 SDD 线前序阶段代理撰写；本波次由驱动派发的独立只读上下文执行，未参与撰写，满足 same-author 委派条件。HIGH 项的独立验证由后续验证波次承担，本波次不自我验证。
**Boundary**: G（feature registry/detail 对齐）、I（plan.md Decision Tensions）、clause coverage accountant、FR→task 覆盖与 plan/tasks 交叉检查不在 W1 读域，由其他波次或驱动侧承载。
**Propagation surface**: 下列 finding 的传播面均为「计划 → 任务 / 实现（或验收取证）」，无 `none` 行，故严重度不受 `none` 上限约束。

## Findings

| ID | Severity | Anchor | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W1-01 | HIGH | requirements.md:116 §FR-006 / :134 §FR-018；checklist:33 CHK014 | FR-006 规定干跑 MUST NOT 写入、移动或删除任何文件与数据，FR-018 又要求干跑 MUST 产出落盘于 `.specify/memory/migrate/receipts/` 的逐运行回执，两条 MUST 直接冲突且无优先关系裁定。 | requirements.md（clarify：裁定干跑回执为仅输出流并改 FR-018，或把回执路径列为零写入的显式例外并补 SC）。 |
| W1-02 | HIGH | requirements.md:134 §FR-018 / :133 §FR-017 / :175 §SC-004 / :177 §SC-006；checklist:53 CHK025、:54 CHK026 | FR-018 的回执字段不含 SC-004 要求的源版本与 FR-017/SC-006 续跑所需的运行状态、续跑标识，且源版本的读取来源与无 source stamp 项目的回退取值未定义。 | requirements.md（扩 FR-018 字段清单，并给 FR-020 补源版本读取来源与回退规则）。 |
| W1-03 | HIGH | requirements.md:145 §FR-023 / :172 §SC-001；checklist:63 CHK032 | FR-023 把纯旧版夹具的构成封闭为退役条目、旧代状态文件、平铺 internal 残留、旧锚点布局四类，未覆盖模板/镜像内容漂移与兼容链接缺失，而 SC-001 要求五维各自在移除收敛处置时转红，两处清单无法自洽。 | requirements.md（统一 FR-023 构成类与 SC-001 逐维变异要求）。 |
| W1-04 | HIGH | requirements.md:135 §FR-019 / :174 §SC-003；checklist:29 CHK010 | FR-019 要求稳定区分四类运行结局，但 clean 与 applied 同为退出 0，且未规定机器可读 outcome token 或输出格式，SC-003 的结局判定因此没有判定基。 | requirements.md（补 outcome token 与输出格式，或改退出码映射）。 |
| W1-05 | HIGH | requirements.md:130 §FR-014 / :135 §FR-019；checklist:30 CHK011 | FR-014 的逐项六值处置到 FR-019 的四类运行结局没有映射规则；部分项已应用而仍有 refuse/blocked 时，applied 与 blocked 两条定义同时成立。 | requirements.md（定义结局聚合规则与优先级）。 |
| W1-06 | HIGH | requirements.md:115 §FR-005 / :211、:219 Clarifications；checklist:17 CHK001、:18 CHK002 | FR-005 未定义「当前已安装版本」的判定方式（wheel、可编辑安装、仓库检出），也未规定 CLI 源路径与工作区 `.specify/scripts/` 副本并存时哪一份为权威。 | requirements.md（clarify 钉名版本解析方式与副本权威）。 |
| W1-07 | MEDIUM | requirements.md:115 §FR-005 / :118 §FR-008 / :99 Edge Cases；checklist:19 CHK003、:46 CHK021 | 某个钉名 owner 缺席或执行报错、或维度不可评估时，需求未定义降级语义（中止、该维 refuse 或可见降级），现有覆盖只有「平台不支持符号链接」一例。 | requirements.md（补降级结局，并禁止把不可评估当作 clean）。 |
| W1-08 | MEDIUM | requirements.md:131 §FR-015 / :93 Edge Cases；checklist:26 CHK007、:27 CHK008 | FR-015 的「一次单批确认提示」未定义覆盖范围与拒绝粒度，也未定义交互终端下 EOF、空回车、取消的结局。 | requirements.md（补确认交互契约与拒绝语义）。 |
| W1-09 | MEDIUM | requirements.md:131 §FR-015；checklist:28 CHK009 | FR-015 声明确认清单的 owner 是 confirmation-gates.md，但未要求命令从该 owner 派生或导入成员并以漂移测试钉住，命令内复制一份清单仍可通过现有验收。 | requirements.md / plan（补派生方式与漂移断言）。 |
| W1-10 | MEDIUM | requirements.md:116 §FR-006 / :172 §SC-001；checklist:32 CHK013、:43 CHK018、:48 CHK023 | 「零写入」「文件树哈希不变」「逐项零差异」未钉名比较单元（内容哈希、模式/可执行位、符号链接目标、空目录创建、权限变更），不同实现会得到不同判定。 | requirements.md § SC-001 / Measurement Sources（补比较单元与允许增量）。 |
| W1-11 | MEDIUM | requirements.md:130 §FR-014 / :133 §FR-017 / :135 §FR-019；checklist:31 CHK012 | 应用期 I/O 失败（归档写失败、目标写失败）未被映射到 FR-014 的六值处置或 FR-019 的四类结局，失败语义只有 FR-017 的前向续跑原则。 | requirements.md（补失败处置与结局映射）。 |
| W1-12 | MEDIUM | requirements.md:117 §FR-007 / :130 §FR-014；checklist:21 CHK005 | 维度①（模板与生成物，含技能/代理镜像）与维度④（镜像一致性）会对同一镜像文件同时命中，需求未定义归属、去重与处置优先级。 | requirements.md（定义维度归属与去重规则）。 |
| W1-13 | MEDIUM | requirements.md:115 §FR-005 / :117 §FR-007；checklist:44 CHK019、:47 CHK022 | FR-005 的封闭 owner 清单不含 init 的模板复制、路径改写、命令生成机制，维度①的模板期望态缺少来源；平台资产变体（sh/ps、工具命令目录交集）的选择规则也未在需求层定义。 | requirements.md（补 owner，或明确由 plan 钉名并回填引用）。 |
| W1-14 | MEDIUM | requirements.md:115 §FR-005 / :229 §A4；checklist:45 CHK020 | FR-005 只定义「当前已安装版本」为期望态来源，未定义框架源仓库以工作区自身声明/脚本为源时的解析规则，与宪法 XI 的自举场景存在未裁定冲突。 | requirements.md / plan（定义两顶帽子的来源切换）。 |
| W1-15 | MEDIUM | requirements.md:133 §FR-017 / :177 §SC-006 / :92 Edge Cases；checklist:55 CHK027、:56 CHK028 | FR-017/SC-006 只覆盖「已归档未写」与「已归档且已写」两个中断点，未枚举写入中、回执未更新等中断点，也未定义中断后工作区被用户改动时按旧回执续做还是重新探测或 refuse。 | requirements.md（补中断点集合与续跑判定）。 |
| W1-16 | MEDIUM | requirements.md:145 §FR-023 / :175 §SC-004；checklist:58 CHK030、:62 CHK031、:65 CHK034 | FR-023 的构成类未映射到具名注册表条目或检查器发现，未规定夹具构建是实时读取来源还是抄写作者时名单，SC-004 的「两类以上历史代残留」也未定义「类」与「代」的计数单位。 | requirements.md（补映射、实时派生要求与计数单位）。 |
| W1-17 | MEDIUM | requirements.md:145 §FR-023 / :174 §SC-003；checklist:64 CHK033 | FR-023/SC-003 未定义「已最新夹具」的构造基（init 现场投影树还是 migrate 收敛后的树），以后者构造会使 clean 断言循环取证。 | requirements.md（钉名构造基与独立 oracle）。 |
| W1-18 | MEDIUM | requirements.md:100 Edge Cases / :231 §A6 / :134 §FR-018；checklist:67 CHK036 | 两写者并发回执测试只出现在 Edge Cases 与假设 A6，没有 FR 承载其义务、也没有 SC 取证，无法进入验收门。 | requirements.md（在 FR-018 或 SC 中补可转红断言）；tasks 承接。 |
| W1-19 | MEDIUM | requirements.md:178 §SC-007 / :126 §FR-013；checklist:39 CHK017、:73 CHK039 | SC-007 的「sanitize 的迁移类检查」未指名具体检查器或动作集合，FR-013 的「静止指针」也没有字段或固定文本形态，零发现与指针存在断言因此不可机判。 | requirements.md（钉名检查器集合与静止指针形态）。 |
| W1-20 | MEDIUM | requirements.md:110 §FR-003 / :135 §FR-019 / :182-192 Measurement Sources | FR-003（缺 `.specify/` 拒绝并指向 init、零写入）与 FR-019 的输入错误退出 2 没有任何 SC 或 Measurement Source 覆盖。 | requirements.md（补 SC 与 measurement source）。 |
| W1-21 | MEDIUM | requirements.md:115 §FR-005 / :175 §SC-004；checklist:20 CHK004 | FR-005 的三条禁令中只有「按源版本号选择路径」经 SC-004 变异转红；「不读 `.specify/version`」与「不按模板指纹猜测」没有可转红的负向断言。 | requirements.md § SC / tasks（补负向测试）。 |
| W1-22 | MEDIUM | requirements.md:123 §FR-010 / :172 §SC-001 | FR-010 的「MUST NOT 读写 sanitize 发现台账」没有对应 SC 或 Measurement Source；零写入哈希只能覆盖夹具树内写入，无法证明未读台账或未以 `--action collect` 触发台账写入。 | requirements.md § SC / tasks（补台账不可变断言）。 |
| W1-23 | MEDIUM | requirements.md:153-158 Runtime Stack & Dependency Ownership（Premises 列） | Runtime Stack 表的 Premises 列引用 EP-001…EP-004，但 requirements.md 内没有 Premises 定义或指向其 owner 的引用，四个前置件不可核验。 | requirements.md（补 Premises 节）或 plan（若 EP 定义在 plan，requirements 改为指针）。 |
| W1-24 | LOW | requirements.md:108 §FR-001 / :200 STR-003；checklist:25 CHK006 | FR-001/STR-003 未定义显式 `--dry-run` 与裸默认是否等价，以及 `--dry-run` 与 `--apply` 同时出现时的结局（输入错误退出 2 还是 apply 优先）。 | requirements.md / plan（补旗标组合契约）。 |

## Checklist Accountability（H 通道）

`unchecked=39; dispositioned=39; undispositioned=0; [Gap] subset: unchecked=15, raised=12, covered-by=3, undispositioned=0`

```
CHK001 disposition: raised-as-finding W1-06
CHK002 disposition: raised-as-finding W1-06
CHK003 disposition: raised-as-finding W1-07
CHK004 disposition: raised-as-finding W1-21
CHK005 disposition: raised-as-finding W1-12
CHK006 disposition: raised-as-finding W1-24
CHK007 disposition: raised-as-finding W1-08
CHK008 disposition: raised-as-finding W1-08
CHK009 disposition: raised-as-finding W1-09
CHK010 disposition: raised-as-finding W1-04
CHK011 disposition: raised-as-finding W1-05
CHK012 disposition: raised-as-finding W1-11
CHK013 disposition: raised-as-finding W1-10
CHK014 disposition: raised-as-finding W1-01
CHK015 disposition: covered-by requirements.md § FR-012
CHK016 disposition: covered-by requirements.md § SC-007
CHK017 disposition: raised-as-finding W1-19
CHK018 disposition: raised-as-finding W1-10
CHK019 disposition: raised-as-finding W1-13
CHK020 disposition: raised-as-finding W1-14
CHK021 disposition: raised-as-finding W1-07
CHK022 disposition: raised-as-finding W1-13
CHK023 disposition: raised-as-finding W1-10
CHK024 disposition: covered-by requirements.md § SC-001
CHK025 disposition: raised-as-finding W1-02
CHK026 disposition: raised-as-finding W1-02
CHK027 disposition: raised-as-finding W1-15
CHK028 disposition: raised-as-finding W1-15
CHK029 disposition: covered-by requirements.md § FR-017
CHK030 disposition: raised-as-finding W1-16
CHK031 disposition: raised-as-finding W1-16
CHK032 disposition: raised-as-finding W1-03
CHK033 disposition: raised-as-finding W1-17
CHK034 disposition: raised-as-finding W1-16
CHK035 disposition: covered-by requirements.md § Measurement Sources & Collection Methods
CHK036 disposition: raised-as-finding W1-18
CHK037 disposition: covered-by requirements.md § FR-002
CHK038 disposition: covered-by requirements.md § SC-009
CHK039 disposition: raised-as-finding W1-19
```

## Coverage Summary（W1 读域内）

| Item | Reading |
|---|---|
| FR | 25（FR-001…FR-025） |
| SC | 9（SC-001…SC-009） |
| STR | 4（STR-001…STR-004，全部 `[[STR-NNN]]` 引用可解析） |
| User Stories / Edge Cases / Assumptions | 4 / 10 / 11 |
| Clarifications | 2 场，6 + 4 问 |
| SC→FR 映射 | 9 条 SC 均可回指 FR，无孤立 SC |
| 无专属 SC 的 FR | FR-003 与 FR-019 的 input-error 分支（W1-20）；FR-010 台账不可变（W1-22）；FR-002 由 FR-025 元要求钉测试；FR-022 由 SC-009 伞形覆盖 |
| FR→task 覆盖 | 未评估（tasks.md 不在 W1 读域） |

## Feature Linkage Summary（W1 读域内）

- 绑定：Feature 024（Specification Workspace Versioning，Draft），见 requirements.md:14-17 与 checklist 头部。
- requirements 明示本规格是 024 的首个子规格；024 原设想的 `.specify/version`、版本→迁移注册表与 `specify upgrade` 由本规格的「声明驱动期望态 + 一次直达」取代（FR-005、FR-020）。
- registry 集成（024 详情 related-specifications、索引行 Last Updated）在 requirements.md:17、:218 被记录为「本阶段只改 requirements.md」下的待办恢复点；索引/详情实际对齐状态未在 W1 读域核验，G 通道归其他波次。

## Constitution Alignment

- 在 W1 读域内未发现 CRITICAL 级宪法冲突。
- FR-001 / FR-022 显式绑定宪法 XXI（脚本/CLI 接口契约）；FR-005 / FR-007 / FR-015 的 owner 声明与 XIV（一事实一 owner）方向一致；FR-018 要求新目录按 XVII（目录治理）在同一变更登记。
- W1-14 记录宪法 XI（Dogfooding）场景下的来源切换未被需求裁定；该条是对缺失场景的 finding，不构成既有原则冲突。

## Metrics

- Total findings: 24（CRITICAL 0 / HIGH 6 / MEDIUM 17 / LOW 1）。
- Detection pass mapping: A=0; B=W1-06、W1-08、W1-10、W1-17、W1-19、W1-24; C=W1-07、W1-09、W1-11、W1-13、W1-15、W1-16、W1-23; D=0 conflicts; E=W1-18、W1-20、W1-21、W1-22; F=W1-01、W1-02、W1-03、W1-04、W1-05、W1-12、W1-14; H=39/39; G/I=out of domain。
- HIGH validation: 6 条待独立只读验证波次；本波次不自我验证。
- Rerun delta: 无前序 W1 报告，首轮，不适用；同目录的 W2 报告属其他波次，按读域互斥未读取。

## Wrap-up 记账

- 单元：analyze wave W1（unit: skill:analyze-artifacts@097）。
- 输入：requirements.md 236 行 / 35,235 B；checklist 80 行 / 14,779 B（`wc -lc` 与 checklist 自报读数一致）。
- 检测通道：A、B、C、D、E、F、H；G、I、clause coverage accountant、FR→task 覆盖不在 W1 读域。
- 产物：本文件（唯一写面）；未修改 requirements.md、checklist 或其他文件。
- 结果：24 findings（6 HIGH / 17 MEDIUM / 1 LOW / 0 CRITICAL）。
- Checklist H：39 unchecked；39 dispositioned（32 raised / 7 covered-by）；0 undispositioned；[Gap] 15/15。
- 验证：6 条 HIGH 待独立只读验证波次。
- 异常：无异常；无即修（nothing to report is something to say）。
- 运行判定 / exec-quant / feedback：运行环境未提供 RUN_ID 与复杂度参数，由驱动侧统一记账；本波次未生成独立引擎记录。
