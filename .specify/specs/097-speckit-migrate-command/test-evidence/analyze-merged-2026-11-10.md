# Analyze — Merged Findings Report（097-speckit-migrate-command）

**Stage**: analyze（串行集成波，Round 1）· **Date**: 2026-11-10
**Inputs（只读）**: `test-evidence/analyze-findings-W1.md`（24 行）、`analyze-findings-W2.md`（13 行）、`analyze-findings-W3.md`（14 行）——三路互斥读域：W1 = requirements.md + checklists；W2 = plan.md / data-model.md / quickstart.md / 3 份契约；W3 = tasks.md（+ 宪法 D 通道比对）。
**Authority**: 本特性 spec 全目录（requirements / plan / research / data-model / contracts / quickstart / feature-ref / tasks / checklists）+ `.specify/constitution.md` + `analyze-artifacts` 契约（`.specify/skills/internal/analyze-artifacts/`）。
**确定性归并规则**: ①分节 = 按严重度 CRITICAL → HIGH → MEDIUM → LOW 分节；②节内字典序 = 按 finding ID 的字典序（`W1-* < W2-* < W3-*`，同波内数字序）；③重复 id = 先声明先得（声明序 W1 → W2 → W3）+ 指针替代。机械核对（脚本解析三份输入的表格行）：**51 行 · 重复 id 0 · 指针替代 0 · 丢弃 0**。逐行内容照抄 worker 原文（摘要/建议不重写），Category 与 propagation_surface 两列由契约的报告格式要求补齐，W2/W3 未逐行声明检测通道者以 `†` 标注由集成者归属。
**Read-only**: 本波未修改任何 spec 制品、未修复任何 finding；产物仅本文件。集成者未撰写上游制品、三个 worker 均为 fresh-context——same-author 委派条件成立。
**Validation status（未做，不可省）**: 11 条 C/H（CRITICAL 2 + HIGH 9）**尚待驱动侧独立只读验证波**（契约 §5.5）；验证完成前本文件不构成 analyze gate 的通过证据。宪法类 CRITICAL 不适用 downgrade（契约 § Constitution Authority）。
**H 问责（§5 H 通道）**: `unchecked=39; dispositioned=39; undispositioned=0`；`[Gap] 子集: unchecked=15, raised=12, covered-by=3, undispositioned=0` → `0 + 0 + 0 = 0`，门可观测。逐条 ledger 见附录 A（源 W1，逐字保留）。
**Cap accounting**: 契约的「≤50 findings」是**单次检测通道**的产物上限；本文件是三路互斥读域的确定性归并（24 / 13 / 14，各自低于上限），按阶段指令不截断。相对单通道 50 行上限的溢出量为 1 行（字典序末位 LOW `W3-14`），在 § 11 Metrics 显式记账，正文保留。

---

## 0. C/H 汇总与指针（不修复）

> 只做汇总与指针：不验证、不降级、不修改任何制品。验证波完成后，本表须按验证裁决重写（confirm / downgrade / reject）。

| ID | Severity | 制品位置 | 一句话事实 | 指针 / 验证状态 |
|----|----------|----------|------------|-----------------|
| W3-01 | CRITICAL | tasks.md L77 × 宪法 L224 | `[~]` 延迟原因唯一载体被定为 `verification.md` `deferred_tasks=`，宪法 VII 要求行内 `<!-- deferred: reason -->` | 本文 § 1；源 W3。待独立验证（宪法项，不适用 downgrade） |
| W3-02 | CRITICAL | tasks.md GATE-4 L51 / DoD-7 L39 / T048 L264 × 宪法 L223 | 成功标准状态行载体被定为 `verification.md`，宪法 Pre-Status-Flip Gate 要求 `verification.log` | 本文 § 1；源 W3。待独立验证（宪法项，不适用 downgrade） |
| W1-01 | HIGH | requirements.md §FR-006 / §FR-018；CHK014 | 干跑「零写入」MUST 与干跑「落盘回执」MUST 直接冲突且无优先关系裁定 | 本文 § 2；源 W1。待独立验证 |
| W1-02 | HIGH | requirements.md §FR-018 / §FR-017 / §SC-004 / §SC-006；CHK025/026 | 回执字段缺 SC-004 源版本与 FR-017 续跑状态/续跑标识；源版本读取来源与回退未定义 | 本文 § 2；源 W1。待独立验证 |
| W1-03 | HIGH | requirements.md §FR-023 / §SC-001；CHK032 | FR-023 夹具构成四类 ≠ SC-001 五维各自可转红；两清单不自洽 | 本文 § 2；源 W1。待独立验证 |
| W1-04 | HIGH | requirements.md §FR-019 / §SC-003；CHK010 | 四类结局中 clean 与 applied 同为退出 0，且无机器可读 outcome token / 输出格式 → SC-003 判定无基 | 本文 § 2；源 W1。待独立验证 |
| W1-05 | HIGH | requirements.md §FR-014 / §FR-019；CHK011 | 六值处置到四类结局无聚合规则；部分应用后 applied 与 blocked 双成立 | 本文 § 2；源 W1。待独立验证 |
| W1-06 | HIGH | requirements.md §FR-005 / Clarifications；CHK001/002 | 「当前已安装版本」判定方式未定义；CLI 源与工作区脚本副本并存时权威未钉名 | 本文 § 2；源 W1。待独立验证 |
| W2-01 | HIGH | contracts/migrate-engine.md:15；data-model.md:121,124 | C-2「六个镜像对」与 E-8 按维度枚举的五个镜像对必有一处与 `MIRROR_PAIRS` 实际不符 | 本文 § 2；源 W2。待独立验证（集成读数见 § 5.1：owner 为 6 对，C-2 正确、E-8 词汇漂移） |
| W2-04 | HIGH | data-model.md:100；contracts/migrate-cli.md:50,77；migrate-template.md:26 | `error` 是否入 outcome 词表未统一：C-3 五行 vs C-4/C-6/T-2/plan XIX 四类 | 本文 § 2；源 W2。待独立验证 |
| W3-03 | HIGH | tasks.md DoD-1 L33 | DoD-1 的 FR 去重计数被追溯表与自身文本满足，删除行内引用也不转红（绿检查非证据） | 本文 § 2；源 W3。待独立验证 |

**C/H 合计**: CRITICAL 2 · HIGH 9。

---

## 1. CRITICAL（2 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W3-01 | D†（宪法对齐） | tasks 执行 → implement / closure（宪法 VII 载体） | CRITICAL | § Task State Sigil（tasks.md L77）× 宪法 VII Workflow Gates（constitution L224） | 本文件把 `[~]` 延迟原因的唯一载体定为 `verification.md` 的 `deferred_tasks=`，而宪法 VII 的不可协商工作流门要求延迟行携带行内 `<!-- deferred: reason -->`，按本文件执行将缺失宪法规定的标记。 | /speckit.tasks（若该 sigil 出自 create-tasks 模板，属机制侧冲突，需模板与宪法字面统一，不得在本特性内稀释） |
| W3-02 | D†（宪法对齐） | tasks / verification 载体 → closure gate（宪法 VII 载体） | CRITICAL | GATE-4（L51）/ DoD-7（L39）/ T048（L264）× 宪法 VII Pre-Status-Flip Gate（constitution L223） | 成功标准状态行的载体被定为 `verification.md`，而宪法该门要求写入 `verification.log`，两名字不同且本文件未声明等价或迁移，按本文件闭环无法满足宪法字面。 | /speckit.tasks 与验收加固/宪法字面统一（以显式宪法修订或门定义修订收敛，不在本特性内改判） |

---

## 2. HIGH（9 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W1-01 | F | requirements → clarify（SC 取证） | HIGH | requirements.md:116 §FR-006 / :134 §FR-018；checklist:33 CHK014 | FR-006 规定干跑 MUST NOT 写入、移动或删除任何文件与数据，FR-018 又要求干跑 MUST 产出落盘于 `.specify/memory/migrate/receipts/` 的逐运行回执，两条 MUST 直接冲突且无优先关系裁定。 | requirements.md（clarify：裁定干跑回执为仅输出流并改 FR-018，或把回执路径列为零写入的显式例外并补 SC）。 |
| W1-02 | F | requirements 字段清单 → 回执实现 / SC-004、SC-006 取证 | HIGH | requirements.md:134 §FR-018 / :133 §FR-017 / :175 §SC-004 / :177 §SC-006；checklist:53 CHK025、:54 CHK026 | FR-018 的回执字段不含 SC-004 要求的源版本与 FR-017/SC-006 续跑所需的运行状态、续跑标识，且源版本的读取来源与无 source stamp 项目的回退取值未定义。 | requirements.md（扩 FR-018 字段清单，并给 FR-020 补源版本读取来源与回退规则）。 |
| W1-03 | F | requirements FR-023 / SC-001 → 夹具与验收 | HIGH | requirements.md:145 §FR-023 / :172 §SC-001；checklist:63 CHK032 | FR-023 把纯旧版夹具的构成封闭为退役条目、旧代状态文件、平铺 internal 残留、旧锚点布局四类，未覆盖模板/镜像内容漂移与兼容链接缺失，而 SC-001 要求五维各自在移除收敛处置时转红，两处清单无法自洽。 | requirements.md（统一 FR-023 构成类与 SC-001 逐维变异要求）。 |
| W1-04 | F | requirements FR-019 → CLI 契约 / 实现与 SC-003 判定 | HIGH | requirements.md:135 §FR-019 / :174 §SC-003；checklist:29 CHK010 | FR-019 要求稳定区分四类运行结局，但 clean 与 applied 同为退出 0，且未规定机器可读 outcome token 或输出格式，SC-003 的结局判定因此没有判定基。 | requirements.md（补 outcome token 与输出格式，或改退出码映射）。 |
| W1-05 | F | requirements FR-014 / FR-019 → 结局聚合实现 | HIGH | requirements.md:130 §FR-014 / :135 §FR-019；checklist:30 CHK011 | FR-014 的逐项六值处置到 FR-019 的四类运行结局没有映射规则；部分项已应用而仍有 refuse/blocked 时，applied 与 blocked 两条定义同时成立。 | requirements.md（定义结局聚合规则与优先级）。 |
| W1-06 | B | requirements → plan / 实现（版本解析） | HIGH | requirements.md:115 §FR-005 / :211、:219 Clarifications；checklist:17 CHK001、:18 CHK002 | FR-005 未定义「当前已安装版本」的判定方式（wheel、可编辑安装、仓库检出），也未规定 CLI 源路径与工作区 `.specify/scripts/` 副本并存时哪一份为权威。 | requirements.md（clarify 钉名版本解析方式与副本权威）。 |
| W2-01 | F† | contracts / data-model → 实现镜像对清单 | HIGH | `contracts/migrate-engine.md:15`；`data-model.md:121,124` | C-2 声明消费 `sync-mirrors.py --check` 的「六个镜像对」，而 E-8 在五维中只按维度枚举了五个镜像对（templates/skills/agents + scripts/shared），两处必有一处与 `sync-mirrors.MIRROR_PAIRS` 的实际计数不符。 | 以 `sync-mirrors.MIRROR_PAIRS` 为唯一 owner 复核后修正 C-2 计数或 E-8 补漏的镜像对；校验波需实读 owner 列表定案。 |
| W2-04 | F† | contracts / plan → CLI 包络与模板转述 / 测试 | HIGH | `data-model.md:100`；`contracts/migrate-cli.md:50,77`；`contracts/migrate-template.md:26` | `error` 在 E-5 与 C-3 中被列为 outcome 并给出 exit 2，但 C-4 的 json `outcome` 枚举、C-6 的「四类结局」、T-2 的转述清单与 `plan.md:51`（XIX）均只含 clean/planned/applied/blocked 四类——`--format json` 在 error 情形是否输出包络、是否携带 `outcome=error` 无定义。 | migrate-cli C-3/C-4/C-6 统一（显式声明 error 不入包络，或补入枚举），T-2 与 plan XIX 跟随。 |
| W3-03 | E†（覆盖 / 可测性） | tasks DoD-1 → 验收门判别力 | HIGH | § Definition of Done DoD-1（tasks.md L33） | DoD-1 的检查命令对全文件做 FR 去重计数，追溯表（L334–L358）与 DoD-1 自身行内 `FR-001…FR-025` 文本已足以让计数恒为 25，因此被检查条件（每条 FR 至少在一条任务行中被点名）即使全部行内引用被删除也不会转红，属「绿色检查是主张不是证据」。 | /speckit.tasks（改为按任务行匹配，或补一条「删除某行 FR 引用应转红」的变异检查） |

---

## 3. MEDIUM（27 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W1-07 | C | requirements → 探测降级语义 / 实现 | MEDIUM | requirements.md:115 §FR-005 / :118 §FR-008 / :99 Edge Cases；checklist:19 CHK003、:46 CHK021 | 某个钉名 owner 缺席或执行报错、或维度不可评估时，需求未定义降级语义（中止、该维 refuse 或可见降级），现有覆盖只有「平台不支持符号链接」一例。 | requirements.md（补降级结局，并禁止把不可评估当作 clean）。 |
| W1-08 | B | requirements → 交互确认实现 | MEDIUM | requirements.md:131 §FR-015 / :93 Edge Cases；checklist:26 CHK007、:27 CHK008 | FR-015 的「一次单批确认提示」未定义覆盖范围与拒绝粒度，也未定义交互终端下 EOF、空回车、取消的结局。 | requirements.md（补确认交互契约与拒绝语义）。 |
| W1-09 | C | requirements / plan → 实现与漂移测试 | MEDIUM | requirements.md:131 §FR-015；checklist:28 CHK009 | FR-015 声明确认清单的 owner 是 confirmation-gates.md，但未要求命令从该 owner 派生或导入成员并以漂移测试钉住，命令内复制一份清单仍可通过现有验收。 | requirements.md / plan（补派生方式与漂移断言）。 |
| W1-10 | B | requirements → SC-001 测量与测试 | MEDIUM | requirements.md:116 §FR-006 / :172 §SC-001；checklist:32 CHK013、:43 CHK018、:48 CHK023 | 「零写入」「文件树哈希不变」「逐项零差异」未钉名比较单元（内容哈希、模式/可执行位、符号链接目标、空目录创建、权限变更），不同实现会得到不同判定。 | requirements.md § SC-001 / Measurement Sources（补比较单元与允许增量）。 |
| W1-11 | C | requirements → 失败处置映射 / 实现 | MEDIUM | requirements.md:130 §FR-014 / :133 §FR-017 / :135 §FR-019；checklist:31 CHK012 | 应用期 I/O 失败（归档写失败、目标写失败）未被映射到 FR-014 的六值处置或 FR-019 的四类结局，失败语义只有 FR-017 的前向续跑原则。 | requirements.md（补失败处置与结局映射）。 |
| W1-12 | F | requirements → E-8 归属与去重实现 | MEDIUM | requirements.md:117 §FR-007 / :130 §FR-014；checklist:21 CHK005 | 维度①（模板与生成物，含技能/代理镜像）与维度④（镜像一致性）会对同一镜像文件同时命中，需求未定义归属、去重与处置优先级。 | requirements.md（定义维度归属与去重规则）。 |
| W1-13 | C | requirements → plan 引用（owner 补齐） | MEDIUM | requirements.md:115 §FR-005 / :117 §FR-007；checklist:44 CHK019、:47 CHK022 | FR-005 的封闭 owner 清单不含 init 的模板复制、路径改写、命令生成机制，维度①的模板期望态缺少来源；平台资产变体（sh/ps、工具命令目录交集）的选择规则也未在需求层定义。 | requirements.md（补 owner，或明确由 plan 钉名并回填引用）。 |
| W1-14 | F | requirements / plan → 两帽子来源切换 | MEDIUM | requirements.md:115 §FR-005 / :229 §A4；checklist:45 CHK020 | FR-005 只定义「当前已安装版本」为期望态来源，未定义框架源仓库以工作区自身声明/脚本为源时的解析规则，与宪法 XI 的自举场景存在未裁定冲突。 | requirements.md / plan（定义两顶帽子的来源切换）。 |
| W1-15 | C | requirements → C-7 续跑判定 / SC-006 | MEDIUM | requirements.md:133 §FR-017 / :177 §SC-006 / :92 Edge Cases；checklist:55 CHK027、:56 CHK028 | FR-017/SC-006 只覆盖「已归档未写」与「已归档且已写」两个中断点，未枚举写入中、回执未更新等中断点，也未定义中断后工作区被用户改动时按旧回执续做还是重新探测或 refuse。 | requirements.md（补中断点集合与续跑判定）。 |
| W1-16 | C | requirements → 夹具映射与 SC-004 计数 | MEDIUM | requirements.md:145 §FR-023 / :175 §SC-004；checklist:58 CHK030、:62 CHK031、:65 CHK034 | FR-023 的构成类未映射到具名注册表条目或检查器发现，未规定夹具构建是实时读取来源还是抄写作者时名单，SC-004 的「两类以上历史代残留」也未定义「类」与「代」的计数单位。 | requirements.md（补映射、实时派生要求与计数单位）。 |
| W1-17 | B | requirements → latest 夹具构造基 | MEDIUM | requirements.md:145 §FR-023 / :174 §SC-003；checklist:64 CHK033 | FR-023/SC-003 未定义「已最新夹具」的构造基（init 现场投影树还是 migrate 收敛后的树），以后者构造会使 clean 断言循环取证。 | requirements.md（钉名构造基与独立 oracle）。 |
| W1-18 | E | requirements / tasks → T006 与 SC 取证 | MEDIUM | requirements.md:100 Edge Cases / :231 §A6 / :134 §FR-018；checklist:67 CHK036 | 两写者并发回执测试只出现在 Edge Cases 与假设 A6，没有 FR 承载其义务、也没有 SC 取证，无法进入验收门。 | requirements.md（在 FR-018 或 SC 中补可转红断言）；tasks 承接。 |
| W1-19 | B | requirements → SC-007 判定基 / tasks 断言 | MEDIUM | requirements.md:178 §SC-007 / :126 §FR-013；checklist:39 CHK017、:73 CHK039 | SC-007 的「sanitize 的迁移类检查」未指名具体检查器或动作集合，FR-013 的「静止指针」也没有字段或固定文本形态，零发现与指针存在断言因此不可机判。 | requirements.md（钉名检查器集合与静止指针形态）。 |
| W1-20 | E | requirements → SC / Measurement 覆盖 | MEDIUM | requirements.md:110 §FR-003 / :135 §FR-019 / :182-192 Measurement Sources | FR-003（缺 `.specify/` 拒绝并指向 init、零写入）与 FR-019 的输入错误退出 2 没有任何 SC 或 Measurement Source 覆盖。 | requirements.md（补 SC 与 measurement source）。 |
| W1-21 | E | requirements → 负向测试（tasks） | MEDIUM | requirements.md:115 §FR-005 / :175 §SC-004；checklist:20 CHK004 | FR-005 的三条禁令中只有「按源版本号选择路径」经 SC-004 变异转红；「不读 `.specify/version`」与「不按模板指纹猜测」没有可转红的负向断言。 | requirements.md § SC / tasks（补负向测试）。 |
| W1-22 | E | requirements → SC / tasks 台账不可变断言 | MEDIUM | requirements.md:123 §FR-010 / :172 §SC-001 | FR-010 的「MUST NOT 读写 sanitize 发现台账」没有对应 SC 或 Measurement Source；零写入哈希只能覆盖夹具树内写入，无法证明未读台账或未以 `--action collect` 触发台账写入。 | requirements.md § SC / tasks（补台账不可变断言）。 |
| W1-23 | C | requirements（Premises 引用） | MEDIUM | requirements.md:153-158 Runtime Stack & Dependency Ownership（Premises 列） | Runtime Stack 表的 Premises 列引用 EP-001…EP-004，但 requirements.md 内没有 Premises 定义或指向其 owner 的引用，四个前置件不可核验。 | requirements.md（补 Premises 节）或 plan（若 EP 定义在 plan，requirements 改为指针）。 |
| W2-02 | F† | data-model / contracts → 回执实现 | MEDIUM | `data-model.md:41,54-70`；`contracts/migrate-cli.md:62` | E-2 称 `workspace` 绝对路径「回执中记录」、C-4 把回执中的 `workspace` 列为易变字段，但 E-3 的 Receipt 字段表没有 `workspace` 字段（C-4 的 json 包络同样无此键）。 | data-model E-3 补字段（或同步修正 E-2/C-4 措辞）。 |
| W2-03 | C† | data-model / contracts → 回执状态实现 | MEDIUM | `data-model.md:59`；`contracts/migrate-engine.md:77` | Receipt `status` 枚举含 `aborted`，但全文未定义任何写 `aborted` 的触发条件（正常收束写 `completed`、崩溃留 `running`），且 `outcome=blocked` 的 apply 回执应记何种 `status` 也未声明。 | data-model E-3 定义触发或删 token；engine C-7 对齐。 |
| W2-05 | C† | data-model / contracts → 框架源写入实现 | MEDIUM | `data-model.md:23,121,124`；`contracts/migrate-engine.md:27-36` | E-1 的 `mechanism` 枚举预留了 `mirror-engine`，但 C-3 处置映射与 E-8 处置来源从未赋予该值，导致框架源模式下经 `sync-mirrors --write`/`generate_commands` 写入的项在回执 `items[].mechanism` 中应记何值未定义。 | migrate-engine C-3 增补框架源写入行（mechanism=mirror-engine），E-8 处置来源对齐。 |
| W3-04 | F† | tasks 追溯表 → 覆盖判据 | MEDIUM | § FR/SC → row traceability（L330–L358）× 行内引用 T005（L146）/T034（L238）/T038（L245）/T039（L246） | 追溯表与行内引用在 7 处不一致：表列而该行未点名 4 处（FR-002→T039、FR-021→T034、FR-022→T034、FR-025→T039），行点名而未入表 2 处（T034→FR-025、T039→SC-009），仅推断未点名 1 处（FR-007→T005）。 | /speckit.tasks |
| W3-05 | E† | tasks SC-007 覆盖 → 验收取证 | MEDIUM | § FR/SC → row traceability SC-007 行（L340）× T015（L171） | SC-007 在全文件任何任务行文本中都不出现，其唯一归属是追溯表把 T015 指为覆盖行，而 T015 的断言清单与引用清单均不含 SC-007，且 DoD-1 只约束 FR 侧、SC 侧没有命名级检查。 | /speckit.tasks（在 T015 文本点名 SC-007，或改映射到真实断言行） |
| W3-06 | E† | tasks 场景 0 执行 / 取证 | MEDIUM | 前置清单（L7）× DoD-9（L41）× T045（L261） | 前置清单声明 quickstart.md 含 scenarios 0–5，而 DoD-9 与 T045 只执行场景 1–5，场景 0 没有任何执行行或取证行，也未声明豁免。 | /speckit.tasks |
| W3-07 | E† | tasks US2 测试覆盖 | MEDIUM | T026（L201）/ T027（L202）× T023（L195）× § Environment Prerequisites（L62） | T026 的 `platform-no-symlink` 拒绝分支与 T027 的 `site/`、`.specify/memory/**`、项目扩展保护类，均未出现在唯一 US2 测试行 T023 的有界断言清单中，而环境节声称该平台降级「在此由模拟行使」却未指名模拟载体。 | /speckit.tasks（把两类行为写入 T023 或新增测试行，并指名模拟方式） |
| W3-08 | E† | tasks 测试归属（红先） | MEDIUM | § FR/SC → row traceability FR-004（L337）/ FR-005（L338）/ FR-011（L344）/ FR-012（L345） | 这四条 FR 只映射到实现/文档/镜像行（依次为 T016；T010/T011/T018；T019/T020；T041/T042），没有任何测试行点名它们，Tests Mode ON 下其红先测试归属不可见。 | /speckit.tasks（补测试行映射，或在测试行断言中点名 FR） |
| W3-09 | E† | tasks DoD-3 → 守卫判别力 | MEDIUM | § Definition of Done DoD-3（L35）× T013（L154） | DoD-3 声称源码守卫「在任一复制实现被移除时转红」，与其「no second engine」标题及 T013 所述守卫（禁止第二份实现）方向相反，且其 Check 只运行套件，无法验证该变异主张。 | /speckit.tasks（更正红条件方向，或补一条变异红测） |
| W3-10 | F†（并发安全） | tasks 写域 / 并发 → implement 派发 | MEDIUM | Tests 契约（L11）× Package Map 写域（L105–L115） | Tests 契约要求每条红先读数逐条落入 `notes/red-first-evidence.md`，但 pkg02–pkg06 的写域均未包含该文件，而 pkg05 与 pkg06 声明可重叠，两个执行者会同时写同一路径，违反「记录类数据一文一件」的并发写安全要求。 | /speckit.tasks（按条目分文件，或把重叠面串行化并补写域声明） |

---

## 4. LOW（13 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W1-24 | B | requirements / plan → CLI 旗标契约 | LOW | requirements.md:108 §FR-001 / :200 STR-003；checklist:25 CHK006 | FR-001/STR-003 未定义显式 `--dry-run` 与裸默认是否等价，以及 `--dry-run` 与 `--apply` 同时出现时的结局（输入错误退出 2 还是 apply 优先）。 | requirements.md / plan（补旗标组合契约）。 |
| W2-06 | Presentation† | none（仅排版，无下游行为） | LOW | `data-model.md:119`；`contracts/migrate-engine.md:62-65` | 两处 Markdown 表结构破损：E-8 的表头行与标题写在同一行（第 119 行），C-5 的复用边界表被「链接修复的职责说明」段落从中截断、后三行（镜像与生成副本、goal/team、周期治理）落在表外。 | Phase 1 制品作者修复排版，不改语义。 |
| W2-07 | F† | plan WP 表 → tasks 切分 | LOW | `plan.md:33,153-166` | WP 表 14 行的 FR 列覆盖 FR-001…FR-025 中除 FR-004、FR-013 之外的全部编号，而 Constitution Check 声称 25/25 可回溯（矩阵在被引用的 feature-ref.md，本波读域外）；其中 FR-013 的静止指针是 E-9 定义的显式交付物却无 WP 落点。 | plan WP 表补 FR-013 归属（如 WP02/WP06），或由 feature-ref 矩阵显式标注非 WP 承载。 |
| W2-08 | F† | plan / quickstart 注释 | LOW | `plan.md:100,199`；`quickstart.md` 全篇 | plan 的目录树注释称 quickstart 为「4 个用户旅程场景」，但同文件 Phase 1 汇总与 quickstart 实际内容均为 6 个场景（0–5）。 | plan.md 目录树注释。 |
| W2-09 | F† | plan / quickstart 交叉引用 | LOW | `plan.md:177`；`quickstart.md:68` | 跨引用失效/歧义：EP-006 指向 `contracts/migrate-engine.md`「§ 平台降级」而该契约无此章节（内容散见 C-3/C-4）；quickstart 场景 4 的「`refuse` 语义如 C-3」未限定文件，而 migrate-cli 与 migrate-engine 各有一节 C-3。 | plan EP-006 改指 C-3/C-4；quickstart 引用补文件名。 |
| W2-10 | F† | contracts / migrate-engine 头部 | LOW | `contracts/migrate-engine.md:3,23` | 契约头部的 Spec 行声明覆盖 `FR-005…FR-018、FR-023…FR-025`，但正文 C-2 两处引用 FR-020（不在该区间内），头部枚举与正文引用不一致。 | migrate-engine 头部补 FR-020 或复核正文引用。 |
| W2-11 | F† | plan WP03 → 规划器去重实现 | LOW | `plan.md:155`；`data-model.md:30` | 去重键不一致：WP03 写「按 target 去重」，E-1 的唯一性规则是 `(dimension, target)` 唯一，两入口若按不同键去重会产生不同计划（T-3 等价性风险）。 | plan WP03 对齐 E-1 的键。 |
| W2-12 | F† | data-model / contracts / plan / quickstart（不变量 owner） | LOW | `data-model.md:139-143`；`contracts/migrate-cli.md:83-86` | 「干跑零写入」「先归档后替换」不变量在 data-model I-1/I-2、migrate-cli C-7、plan Constraints 与 quickstart 多处重述且无唯一 owner 声明；I 集合（5 条）与 C-7 集合（4 条）成员不同，后续修订易漂移。 | 声明 data-model 不变量为 owner，C-7 标注为测试投影（或反向）。 |
| W2-13 | F† | quickstart 实测记录 | LOW | `quickstart.md:10-16` | 场景 0 的实测在仓库外 ad-hoc 目录 `~/tmp/speckit-migrate-quickstart` 执行，与 AGENTS.md 摘要的临时目录纪律（sanctioned temp root、禁 ad-hoc 目录）不一致。 | quickstart 作者：实测记录与建议目录改用已登记临时根，或明确表述为用户自选目录。 |
| W3-11 | C† | tasks T004 目的说明 | LOW | T004（L134）× § Premises（L98）× Notes（L376） | T004 要求对「本特性首次全树统计」执行 `--freeze`，但 § Premises 已记录同一命令在生成期（2026-11-10，640 names）执行过、Notes 亦称该冻结是本生成阶段制品，实现入口重跑同一冻结未说明目的。 | /speckit.tasks |
| W3-12 | B† | tasks 行文 | LOW | T041（L257）/ T043（L259） | 两行的 "its mirror pair see `.specify/...` is synced in T042/T044" 句子不合语法，读者无法判定它是声明一条同步动作还是指向一个文件。 | /speckit.tasks（改写为「镜像副本由 T042/T044 同步」） |
| W3-13 | E† | tasks Green Partition 可审计性 | LOW | § Green Partition（L362–L371）× Notes（L376） | 四个未声明条款（cli C-6/C-7、engine C-5/C-8）被描述为「由点名它们的测试行文本钉住」，但 Green Partition 表未列出任何钉住行，该主张在文件内不可审计。 | /speckit.tasks |
| W3-14 | B† | none（仅术语） | LOW | Notes（L376） | "The contractor's live delta" 使用了契约覆盖计数之外的生造主体（计数所有者为 clause-coverage accountant），读者会误认存在另一个计量主体。 | /speckit.tasks |

---

## 5. 跨制品一致性（串联读全 spec）

本节由集成者通读全 spec 目录（requirements → plan → research → data-model → contracts → quickstart → feature-ref → tasks → checklists）后写成；它不新增 finding，只把三路读域的结论接成可读的链，并记录只读核对读数。

### 5.1 集成者只读核对（本次实际执行）

| # | 命令 / 读点 | 读数 | 影响的 finding |
|---|-------------|------|----------------|
| R1 | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command`（未传 `--freeze`） | exit 1，`status: uncovered`；claimed clauses **11**；`[clause-uncovered]` 644（**4 beyond** the 640-name frozen baseline）；`[fr-uncovered]` 21（**4 of 25 FRs** cited from citation groups）；`[clause-unparsable]` 108（全 corpus 口径，含 1 处 parse doubt）；`[coverage-baseline-delta]` baseline 640 | § 6 Coverage；与 tasks § Notes 的「4/25」披露互证；W3-13 的「4 个未声明条款」= 4 own clauses beyond baseline |
| R2 | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/097-speckit-migrate-command` | exit 0，`status: ok`；6 个 label 全 pass（0 error/warning）；2 条记录（T-001/T-002）；`value_domain=HIGH-or-0, high=0` | I 通道机械零发现（W2 的 I 通道声明获得确定性裁决） |
| R3 | 实读 `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` | **6 对**：`templates`、`skills/external`、`skills/internal`、`agents`、`scripts`、`shared` | W2-01 证据落定：C-2 的「六」正确；E-8 把 skills 写成「一个镜像对」而 owner 为两对 → 词汇/计数漂移成立（C-2 无需改，E-8 需改） |
| R4 | 实读 `.specify/constitution.md` L220–L225 | L223 `verification.log`；L224 `[~]` 携带行内 `<!-- deferred: reason -->` | W3-01 / W3-02：宪法字面事实成立 |
| R5 | 实读机制侧（`templates/tasks-template.md:121`、`shared/workflow/acceptance-hardening.md:46`、`shared/workflow/feature-integration.md:44`） | 模板/验收加固用 `verification.md`（行内注释写作 "ideally"）；feature-integration 的 Pre-Status-Flip 步骤仍写行内 `<!-- deferred: <reason> -->` | W3-01 / W3-02 属**机制侧冲突**（模板与宪法字面分叉），非本特性独有措辞；本特性内不得稀释，修复方向只能二选一：机制修订或宪法修订 |
| R6 | 实读 `quickstart.md` 场景结构 | 场景 **0–5 共 6 个**（0 与清理已实测） | W2-08 成立（plan L100 写 4，L199 写 6）；W3-06 的场景 0 缺口成立，但 quickstart 自身持有场景 0 的实测记录（任务侧仍缺执行/引用行） |
| R7 | 实读 `feature-ref.md` FR→WP 矩阵 与 `plan.md` WP 表 | feature-ref 25/25（含 FR-004→WP01、FR-013→WP03）；plan WP 表 FR 列不见 FR-004、FR-013 | W2-07 成立；证据在 feature-ref 与 WP 表之间漂移 |
| R8 | 实读 `contracts/migrate-engine.md` 头部 vs C-2；`plan.md` EP-006 vs 契约章节名 | 头部区间不含 FR-020 而 C-2 引用 FR-020；EP-006 指向的「§ 平台降级」章节不存在（内容在 C-3 行与 C-4 降级事实） | W2-10、W2-09 成立 |
| R9 | 抽查 `tasks.md` 追溯表 ↔ 任务行文本 | T034 文本含 FR-002/FR-025 而表列 FR-021/FR-022；T039 文本含 FR-021/SC-009 而表列 FR-002/FR-025；T005 文本无 FR-007；SC-007 不出现于任何任务行 | W3-04、W3-05 成立 |
| R10 | 实读 `.specify/features.md` 024 行 与 `.specify/features/024-*.md` | 行：`Planned`，Spec Path `.specify/specs/097-speckit-migrate-command/requirements.md`，Last Updated `2026-11-10 (plan: …)`；详情：`Planned` / Last Updated 2026-11-10 | G 通道零 finding；观察：索引叙事仍写 "plan:"，状态/路径/日期均合规（见 § 7） |

### 5.2 七条制品链（断点归位）

**链 1 — 期望态来源链**（FR-005 / FR-007 → plan T-001/T-002 + engine C-2 → data-model E-7/E-8 → tasks T010/T011/T018）
一致事实：五维 token 顺序在 E-8、engine C-1、tasks T005 三处一致；双工作区语义（`skills/external/` guard）在 plan T-002、E-6、C-2 一致；两份钉名 owner 表互指。断点：W1-06（版本判定与副本权威）、W1-13（FR-005 owner 清单缺 init 复制机制——plan T-001 引入的机制在 requirements 无授权来源）、W1-14（框架源模式的来源切换与「唯一来源」未裁定）、W1-21（两条禁令无可转红断言）、W2-01（镜像对计数词汇）、W2-05（`mirror-engine` 无赋值行）、W2-11（去重键 plan vs E-1）、W3-08（FR-005 无测试行点名）。

**链 2 — 处置与结局链**（FR-014 / FR-019 → data-model E-5 + cli C-3/C-4 + engine C-3 → tasks T005/T013/T014/T016/T021）
一致事实：六值处置域在 engine C-3 与 FR-014 逐字对应；退出码数值五行在 E-5 与 C-3 一致（clean 0 / planned 1 / applied 0 / blocked 3 / error 2）。断点：W1-04（requirements 无 outcome token/格式；C-4 已有）、W1-05（聚合规则在 E-5 的 blocked 触发行**已给出**，但 requirements 层仍双成立）、W1-11（设计侧 E-5 已把执行期 I/O 失败并入 blocked，requirements 层未映射）、W2-04（error 是否入词表：C-3/E-5 五行 vs C-4/C-6/T-2/plan XIX 四类）。

**链 3 — 回执与续跑链**（FR-017 / FR-018 / FR-020 → E-3/E-4 + engine C-7 → tasks T006/T009/T029/T031）
一致事实：逐运行一文一件、run-id 形态、`running→completed`、续跑以旧回执为准且不二次搬移，在 E-3/E-4/C-7/T006/T031 一致；`source` 对象的 `unavailable` 回退在 R-5、EP-005、E-3 一致。断点：W1-01（干跑回执与零写入的 MUST 冲突，E-3「FR-018 解释记录」给出确定性解释但 requirements 未裁定）、W1-02（E-3 已含 source/target/resumedFrom/status 主体，requirements FR-018 字段清单仍缺）、W1-15（中断点集合与用户改动后的续跑判定，C-7 只覆盖部分）、W1-18（两写者测试有 T006 承接但无 FR/SC）、W2-02（E-3 缺 `workspace` 字段）、W2-03（`aborted` 无触发）、W3-10（红先证据账本单文件并发写）、W3-11（T004 重跑冻结目的）。

**链 4 — 安全与确认链**（FR-015 / FR-016 + confirmation-gates → cli C-5 + engine C-6 → tasks T023–T027）
一致事实：双键、非交互 blocked、无确认旗标、未确认破坏项零执行，在 C-5/C-6/T023/T024 一致；archive-not-delete 与用户内容保护在 C-3 补充规则、C-6、T025/T027 一致。断点：W1-08（单批确认范围与 EOF 语义）、W1-09（清单派生与漂移测试）、W1-10（零写入比较单元）、W3-07（T023 断言清单不含 platform-no-symlink 与保护类，模拟载体未指名）、W3-10（并发写面）。

**链 5 — 验收与夹具链**（FR-023/024/025 + SC-001/003 → engine C-8 → tasks T007 / T015 / T022 / T023 / T028 / T029 / T032 / T045 / T046）
一致事实：三类夹具的声明驱动构造（C-8）明确让五维各至少一项，覆盖 SC-001 的五维主张；latest 夹具的构造基由 C-8 钉为 init 复制机制产物。断点：W1-03（requirements FR-023 构成清单仍四类）、W1-16（映射与计数单位）、W1-17（requirements 层构造基缺失，设计侧已钉）、W1-20（输入错误分支无 SC）、W1-22（台账不可变断言）、W3-06（场景 0 无执行/引用行）、W3-08（四条 FR 无测试行）、W3-09（DoD-3 方向）、W3-13（未声明条款的可审计性）。

**链 6 — 分发与装配链**（FR-021 / FR-022 → template T-1…T-6 → tasks T033–T040）
一致事实：四副本树、`AUTO-GENERATED`、Qoder frontmatter、`COMMAND_BASELINE` 29→30、`.specify/templates/commands/` 退役面，在 T-4、T033、T036、T038、T039 一致。断点：W1-19（SC-007 检查器集合与指针形态）、W3-04/W3-05（追溯双轨漂移与 SC-007 未点名）、W2-07/08/09/10（WP 归属与交叉引用/计数）。

**链 7 — 宪法与流程链**（宪法 VII ↔ tasks sigil / GATE-4 载体）
一致事实：无。断点：W3-01（行内延迟标记缺失）、W3-02（`verification.log` vs `verification.md`）。两项均 CRITICAL，机制侧来源已由 R5 证实，修复不在本特性内自行稀释。

### 5.3 跨波主题簇（重叠登记，无字面重复）

三路读域的 id 无重复（机械核对）；以下为**同一底层议题被不同波次从不同制品面命中**的登记，供修复时成组处理：

| 簇 | 成员 | 议题 |
|----|------|------|
| K1 回执契约 | W1-01, W1-02, W1-11, W1-15, W1-18, W2-02, W2-03, W3-10, W3-11 | 回执字段/状态/续跑/并发账本 |
| K2 结局与处置词表 | W1-04, W1-05, W2-04 | 四类结局 vs error 第五行；聚合规则 |
| K3 期望态来源与归属 | W1-06, W1-12, W1-13, W1-14, W1-21, W2-01, W2-05, W2-11 | owner 清单、双帽子、维度重叠、去重键、镜像对计数 |
| K4 验收取证判别力 | W1-03, W1-10, W1-16, W1-17, W1-20, W1-21, W1-22, W3-03, W3-05, W3-08, W3-09, W3-13 | 可转红断言、比较单元、变异检查、DoD 判别力 |
| K5 宪法与门载体 | W3-01, W3-02 | 宪法 VII 字面 vs 机制模板 |
| K6 交叉引用与计数 | W2-07, W2-08, W2-09, W2-10, W3-04, W3-12, W3-14 | 引用失效、计数漂移、术语 |
| K7 安全与用户保护 | W1-07, W1-08, W1-09, W3-07 | 确认交互、降级、保护类断言 |
| K8 夹具与场景 | W1-16, W1-17, W3-06, W2-13 | 夹具构造基、场景覆盖、实测目录 |

### 5.4 归属不对称：requirements 层 vs 设计层（供修复排序）

通读后最显著的集成事实：K1/K2/K3 中相当一部分 W1 requirements 层 finding **在设计层已被确定性答复**——W1-01 ↔ E-3「FR-018 解释记录」；W1-02 ↔ E-3 source/target/resumedFrom/status + R-5/EP-005；W1-04 ↔ C-3/C-4 outcome token 与 json 包络；W1-05/W1-11 ↔ E-5 blocked 触发行；W1-17 ↔ C-8 `build_latest_project`；W1-03 的五维部分 ↔ C-8 五维构造。这不自动关闭任何 finding：契约要求需求层裁定（clarify 归属不变），但修复时应把设计侧答复作为**建议裁定文本**回收进 requirements，而不是让实现者在两层之间自行取舍。反之，设计层无法自救的是 K5（宪法载体）与 K2 的 `error` 词表统一（需要跨文件一次改齐）。

---

## 6. Coverage Summary

| Item | Reading |
|------|---------|
| FR / SC / STR | 25（FR-001…FR-025）/ 9（SC-001…SC-009）/ 4（STR-001…STR-004，全部 `[[STR-NNN]]` 引用可解析） |
| SC → FR 映射 | 9/9 SC 均可回指 FR，无孤立 SC（W1 读域） |
| FR → task（纸面） | 25/25 均在追溯表中有行；tasks 48 行、无缺号 |
| FR → task（行级机器证据） | 弱于纸面：W3-04（7 处表 ↔ 文本漂移）、W3-05（SC-007 零任务行点名）、W3-08（FR-004/005/011/012 无测试行点名）、W3-03（DoD-1 计数不可转红） |
| clause accountant（R1） | `status: uncovered`（exit 1）；claimed 11；4 own clauses beyond the 640-name baseline；FR-citation lane 4/25 |
| 无专属 SC 的 FR（W1 读域） | FR-003 与 FR-019 的 input-error 分支（W1-20）；FR-010 台账不可变（W1-22）；FR-002 由 FR-025 元要求钉测试；FR-022 由 SC-009 伞形覆盖 |
| 夹具覆盖 | 三类夹具与五维构造在 C-8 已具名；requirements 层清单一致性见 W1-03/W1-16/W1-17 |

## 7. Feature Linkage Summary

| 项 | 读数 |
|----|------|
| 绑定 | Feature 024（Specification Workspace Versioning）；requirements.md Related Feature 与 feature-ref.md 一致 |
| 索引行（R10） | `.specify/features.md` 024 行：`Planned`，Spec Path 指向本规格 requirements，Last Updated `2026-11-10 (plan: …)` |
| 详情文件 | `.specify/features/024-specification-workspace-versioning.md`：`Status: Planned`，Last Updated 2026-11-10，Key Changes/Implementation Notes 含 plan 阶段内容 |
| 状态合法性 | `/speckit.tasks` 与 `/speckit.checklist`（implement 前）按状态机均不翻转状态；`Planned` 合法持有，无回归 |
| G 通道结论 | **零 finding**（R10 证据）；观察（不升级为 finding）：索引行叙事仍写 "plan:"，而 tasks/checklist 工件已存在——日期与状态合规，仅叙事落后，建议下次 registry 触碰时顺带更新 |
| 待办恢复点 | requirements.md:17/:218 的 registry 集成待办在 plan 阶段已关闭（feature-ref.md 声明）；本波核对与之一致 |

## 8. Constitution Alignment Issues

- **CRITICAL × 2**：W3-01、W3-02（§ 1）。两项均以宪法字面（L223/L224）为对照，机制侧来源由 R5 证实；按契约，宪法冲突不得在本特性内稀释或降级，修复路径二选一（修订 tasks 载体以同时满足宪法字面，或走一次显式的宪法/机制修订）。
- 其余读域的 D 通道零发现声明：W1（requirements + checklist 域）——未发现 CRITICAL 级宪法冲突，FR-001/FR-022 绑定 XXI、FR-005/007/015 owner 声明对齐 XIV、FR-018 对齐 XVII；W2（plan + 设计制品域）——Constitution Check 22 行 Pass，T-001/T-002 decision tension 字段齐备（R2 机械复核：0 error）。
- 宪法 VII 的 Pre-Status-Flip 门（`verification.log`）与行内延迟标记在 tasks.md 的闭环方式上存在字面缺口——见 W3-01/W3-02，不在此重复。

## 9. Unmapped Tasks

- 未发现「无任何 FR/SC 锚点」的任务行：48 行均有阶段归属与至少一个 FR/SC 引用或追溯表映射（W3 机械前提）。
- 反向漂移登记：T034、T039 行内点名的 FR/SC 未全部入追溯表；T005 的 FR-007 属推断（W3-04）。

## 10. Systemic Observations（聚合，不提升任何单行严重度）

- **S-1 两层闭合不对称**：requirements 层 finding 与设计层的确定性答复并存（§ 5.4），修复归属须先裁定（clarify vs plan 回填），否则实现者面对两套文本。
- **S-2 封闭词表多处漂移**：结局词表四 vs 五（W1-04/W2-04）、镜像对五 vs 六（W2-01）、receipt status 的 `aborted`（W2-03）、去重键（W2-11）——共性是一份词表被多处复述而无「引用组」机制承接（accountant 的 FR-citation lane 4/25 同源）。
- **S-3 验收判别力**：W3-03、W3-09、W3-13 同属「绿色检查是主张不是证据」；建议以变异红测补齐（与框架 Fast Fail 纪律同向）。
- **S-4 证据账本并发**：W3-10 的红先证据单文件与「记录类数据一文一件」冲突，影响 implement 并行派发设计。
- **S-5 追溯双轨**：追溯表与行内引用互相漂移（W3-04/05/08），未指定哪一轨为判据。
- **S-6 机制侧与宪法字面冲突**：K5 需要在机制 owner 层收敛，不是本特性可自决事项。

## 11. Metrics

| 指标 | 读数 |
|------|------|
| 输入波次 | W1 24（0/6/17/1）· W2 13（0/2/3/8）· W3 14（2/1/7/4）〔CRITICAL/HIGH/MEDIUM/LOW〕 |
| **合计** | **51** 行：CRITICAL **2** · HIGH **9** · MEDIUM **27** · LOW **13** |
| 重复 id / 指针替代 / 丢弃 | 0 / 0 / 0（机械核对） |
| C/H 待独立验证 | 11（CRITICAL 2 + HIGH 9）；验证波完成前不构成 gate 通过证据 |
| H 问责 | unchecked 39 / dispositioned 39 / undispositioned 0；Gap 子集 15：12 raised / 3 covered-by / 0 undispositioned |
| clause accountant（R1） | `status: uncovered` (exit 1)；claimed 11；fr-uncovered 21（4/25 cited）；clause-uncovered 644（4 beyond baseline）；baseline 640 |
| decision tension（R2） | ok，2 记录，0 error |
| 覆盖 / 链接 | FR→task 纸面 25/25；行级证据缺口见 § 6；Feature 链接零 finding |
| 相对单通道 50 行上限的溢出 | 1 行：字典序末位 LOW `W3-14`，按确定性归并指令保留于正文，此处显式记账 |
| Rerun delta | 不适用——本特性首份合并报告，三波均为 Round 1；后续修复重跑按契约 § 6 输出 Resolved / New / carried-over 三向 delta |

## 12. Rerun Delta

不适用（首轮合并；无前序合并报告）。三路 worker 报告内亦无更早轮次。

---

## 附录 A — Checklist H 逐条 disposition ledger（源 W1，逐字保留）

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

## 附录 B — 确定性归并日志

- **分节**：CRITICAL（2）/ HIGH（9）/ MEDIUM（27）/ LOW（13）；每节按 ID 字典序排列（节内核对：`W1-01 < W1-02 < … < W2-01 < … < W3-14` 成立）。
- **重复 id**：脚本解析三份输入的 `| W#-NN | SEVERITY |` 表格行 → 51 行，`collections.Counter` 重复项 = 0 —— 无指针替代行。
- **逐行保真**：Summary 与 Recommendation 两列照抄 worker 原文；Location(s) 保留 worker 锚点。仅新增契约要求的 Category 与 propagation_surface 两列（`†` = 集成者归属）。
- **分类口径**：Category = analyze-artifacts 检测通道（A 重复 / B 歧义 / C 欠指定 / D 宪法 / E 覆盖 / F 不一致 / G 特性 / H checklist / I 决策张力）；W1 行取 W1 自报映射；W2/W3 行由集成者按 finding 性质归属并标 `†`；非八通道项记 `Presentation`（仅 W2-06）。
- **只读证据**：R1–R10（§ 5.1）均为只读命令/读点；未传 `--freeze`；未修改任何制品。
- **未做事项（明示）**：C/H 独立验证波（驱动后续派发）；任何修复（本阶段禁止）。
