# Contract: `requirements.md` 检查器(US1)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-006…FR-014  
**Subject**: `scripts/python/validate-requirements.py`(新建,D-4)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md` 的约定([制品类] / [行为类])。

---

## 检查面

**C-1** [制品类] 系统 MUST 提供一个校验 `requirements.md` 的确定性检查器,其检查面**至少**覆盖四类命题:FR/SC 编号连续、编号按**文档出现序**、交叉引用可解析、活动标记计数。判据:该脚本 docstring 的枚举段含 5 个标签(见 C-2),且 `EXPECTED_CHECKS` 与之集合相等。(FR-006)

**C-2** [制品类] 检查项标签集 MUST 恰为 `id-contiguous`、`doc-order`、`ref-resolvable`、`marker-count`、`dup-id` 五项,逐项对应 FR-007…FR-011。判据:`re.findall(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", docstring, re.M)` 的集合 == 上述五项集合。(FR-006…FR-011、D-5)

**C-3** [制品类] 每项检查发出的消息 MUST 以 `<lineno>: <label>: ` 起首(与 `validate-tasks.py:140,161,167,191,223,249` 同形),使调用方能定位到行。判据:对每条 error/warning 做前缀正则匹配。(FR-006、D-5)

## 编号连续性

**C-4** [制品类] 编号连续性检查 MUST 按前缀**分序列独立**进行(`FR-` 与 `SC-` 各自成序),MUST NOT 跨前缀比较序号。判据:一份 `FR-001…FR-003` + `SC-001…SC-002` 的制品 exit 0;一份 `FR-001, FR-003` 的制品报 `id-contiguous` 并点名缺号。(FR-007)

**C-5** [制品类] 定义行的识别式 MUST 为 `^- \*\*(FR|SC)-(\d+)\*\*`(行首项目符号 + 粗体 ID),即**只认定义行**,不认散文里的提及。判据:一份在散文里引用 `FR-009` 的规格不因该提及被计入序列。(FR-007、FR-008)

**C-6** [行为类] 补零不一致(`FR-7` vs `FR-007`)与字母后缀(`FR-003a`)MUST 判为**形态违例**并点名两种写法,MUST NOT 自行归一化后放行——归一化会掩盖作者的编号意图。依据:本规格撰写期即写出过 `FR-003a` 并被自己的边界情形判为违例(`requirements.md` § Edge Cases)。(边界情形)

## 文档出现序

**C-7** [制品类] 文档序检查 MUST 锚定在**定义行**上,而不是在 ID 的每次出现上。判据:对一份干净的既有规格跑,`doc-order` 命中数为 **0**;实测按「每次出现」比对会在同一份规格上报出 **5** 条假违例(交叉引用合法地乱序)。(FR-008)

**C-8** [制品类] `## Clarifications` 一节 MUST 被排除。判据:把该节的追加历史(其中引用了重编号前的定义行)计入后,MUST 仍为 0 命中;实测计入会多出第 **6** 条假违例。(FR-008)

**C-9** [制品类] 违例输出形态 MUST 为 STR-002 `ORDER BREAK: <ID> after <ID>`。判据:对一份把 `SC-002` 定义行移到 `SC-005` 之后的副本跑,输出含该字面量并点名两个 ID。(FR-008)

**C-10** [行为类] C-7 与 C-8 的两个锚点**都是承重的**,不是装饰:契约测试 MUST 断言二者的理由被真源文档载明,否则下一次编辑会「简化」抽取式并重新引入假违例。该义务的直接先例是 `tests/contract/test_clarify_semantic_completeness.py:330` 的 `assert "load-bearing" in rules`。(FR-008)

## 引用可解析

**C-11** [制品类] 引用可解析检查 MUST 覆盖 `FR-\d+`、`SC-\d+` 与 `[[STR-\d+]]` 三种形态;每条不可解析的引用 MUST 报出**引用出现的行号**与**被引用的 ID**。(FR-009)

**C-12** [制品类] **被反引号包裹**的引用形态属「提及」而非「引用」,MUST NOT 计入。判据:一份讨论引用机制的规格(必然大量出现 `` `FR-\d+` `` 与 `` `[[STR-\d+]]` ``)的 `ref-resolvable` 命中数为 **0**。(FR-009)

**C-13** [制品类] 同一 ID 被定义两次 MUST 报 `dup-id`(**ERROR**),且与「引用不可解析」**分列**——二者修法相反(一个要删,一个要补)。判据:两个标签各自独立命中,合并计数即违例。(FR-011)

**C-14** [制品类] 检查 MUST **双向**:`[[STR-NNN]]` 引用集与 Shared Strings 表的定义集之差在两个方向都 MUST 为空——正向(引用 → 定义)不可解析数为 0,**反向**(定义 → 引用)未被引用数亦为 0。判据:对本规格实跑得 `defined 10 / referenced 10 / 双向差集均空`。(FR-009 的完备化)

**C-15** [制品类] `Consumed by` 列的**反向**一致性 MUST 被检查:该列点名的每个 `FR-NNN` / `SC-NNN` 所在行 MUST 确有 `[[STR-NNN]]` 引用。判据:实测本规格在 clarify 轮有 **7** 处不符(其中 2 处是把字面量**重打**了一遍),订正后为 **0**;该检查即为守住这个 0。依据:`templates/requirements-template.md:173-176` 的引用公约明写「Downstream artefacts MUST cite by `<string-id>` rather than re-typing the text」。(FR-009、clarify 轮实测)

## 活动标记计数

**C-16** [制品类] 活动标记计数 MUST 只统计**带冒号且未被反引号包裹**的实例。判据:一份讨论澄清机制的规格(必然大量出现被反引号包裹的标记名)的计数与人工核对一致;实测字面匹配对它给出虚高计数。(FR-010)

**C-17** [制品类] 计数的正则形态 MUST 为否定后视的 `(?<!` + 反引号 + `)\[NEEDS CLARIFICATION:`,即冒号在模式内、反引号前缀被排除。判据:对本规格实跑,`/speckit.clarify` 回写前为 **1**、回写后为 **0**。(FR-010)

## 命令接线

**C-18** [行为类] `/speckit.requirements` MUST 在写完规格后调用该检查器,并在其报出任一 ERROR 时**停止**,MUST NOT 进入下一阶段。落点:`templates/commands/requirements.md` 的验证步骤(实测当前为 step 7,`:62-66`)。(FR-012)

**C-19** [行为类] 停止时 MUST **原样呈现**检查器输出,MUST NOT 复述或概括。判据:命令模板的该步骤文本含「原样呈现 / verbatim」一类义务表述,且不含「summarize the findings」一类反向表述。(FR-012)

**C-20** [制品类] `shared/guidelines/requirements-guidelines.md` § Validation Process(实测 `:50-56`)MUST 写明「计数与引用解析由该检查器派生,MUST NOT 手打」,并 MUST 把清单更新的时机明确置于澄清回写**之后**。判据:对该节 grep 检查器路径命中数 ≥ 1,且「之后 / after」一类时序词在场。(FR-013)

**C-21** [行为类] FR-013 的落点 MUST NOT 假称既有 owner 已定义计数集:实测 `clarify-taxonomy.md:95,104` 声称「the full count set」的 owner 是 `requirements-guidelines.md` § Create Spec Quality Checklist,而**该节(`:9-48`)不定义任何计数字段**(它是一个固定 16 项清单)。该 owner 指针悬挂已上送(`research.md` A-1),本特性只在自己范围内写明「计数由检查器派生」,MUST NOT 顺手改写上游 owner 归属。(FR-013、A-1)

## FR-014 的债务:移除过渡副本

**C-22** [制品类] US1 落地后,`shared/constants/clarify-taxonomy.md` 里本轮加入的过渡期 awk 抽取式(实测位于 `:108-112`,该节起于 `:106`、锚点理由在 `:114`)MUST **已不存在**。判据:`grep -c` 对该文件的 awk 围栏块命中数为 **0**。(FR-014、SC-002)

**C-23** [制品类] 「Until that validator ships」一句 MUST 被删除。判据:对该文件 grep 该字面量命中数为 **0**;实测该句**未被任何测试钉住**(`grep -rn "Until that validator" tests/` 无命中),故可自由移除。(FR-014、SC-002、D-9)

**C-24** [制品类] 该处的文档序不变量 MUST 改为**指向检查器**。判据:该节对检查器路径的命中数 ≥ 1。(FR-014、SC-002)

**C-25** [制品类] SC-002 的取证 MUST 配一条反空真哨兵:该文件非空且文档序不变量小节仍在场,使「0 因为已移除」与「0 因为整节丢失」可区分。(FR-040、SC-002 Source)

**C-26** [制品类] 移除过渡副本 MUST 在**同一提交内**改写 `tests/contract/test_clarify_semantic_completeness.py` 的两个测试:`test_c4_extraction_is_definition_anchored_and_history_excluded`(`:311-333`,其 `:324` 的断言消息逐字为 "the interim extraction block is gone from the document-order invariant",即**当前把副本的在场当作通过条件**)与 `test_c4_shared_implementation_with_the_requirements_validator_is_declared`(`:336-342`,钉住 `:338` 的 "shares one implementation" 与 `:341` 的 "/speckit.requirements")。改写方向是把「宣告将来共享」换成「指名现在共享的实现」。(FR-014、D-9)

**C-27** [行为类] C-26 的改写 MUST NOT 削弱该测试原本守住的两个锚点(定义行锚定、排除 `## Clarifications`)——它们在新形态下由检查器承担,故测试改为断言**检查器**具备这两个锚点,而不是断言散文里的 awk 文本具备。(FR-014、D-9)

**C-28** [制品类] C-12 的「被反引号包裹者属提及」MUST 按 **CommonMark 的代码跨度规则**实现:一段代码跨度以 **N 个**反引号开启、在下一处**恰为 N 个**反引号处闭合;未闭合的串按字面处理。MUST NOT 以「单个反引号的奇偶位置」近似——实测该近似在正文含**行内围栏标记**(连续多个反引号)时会**反相**,把它之后的真实引用误判为代码内而漏掉。取证:本特性的 `feature-ref.md` 生成器初版即用奇偶近似,导致 `contracts/green-point-claim.md` C-8 行尾的 `(FR-020)` 被吞、FR-020 一度显示为**零覆盖**;改为按串解析后配一条自检样本(形如「写在 4 反引号围栏内的 `(FR-020)` 与单反引号包裹的 `FR-9` 提及」→ 只抽出 `FR-020`)。(FR-009)

**C-29** [制品类] 引用抽取 MUST 先做**提及/引用**判定(C-12)、再做**代码跨度**判定(本条 C-28),二者顺序不可交换;且抽取结果 MUST 按 `(文档, 条款 id)` **对**去重后再计数,MUST NOT 以「引用出现次数」充当「被覆盖条款数」。依据:本特性生成 `feature-ref.md` 时同时踩到两个缺陷——把反引号内的示例 `` `FR-7` `` 与 `` `FR-007` `` 当成对 FR-007 的两次引用(多算),以及吞掉 FR-020 的真实引用(少算)——二者在**总数上恰好互相抵消**,故只有按对去重后**逐行**核对才暴露得出来,单看总数看不出来。(FR-009、FR-011)
