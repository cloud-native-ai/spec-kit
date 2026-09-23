---
id: "introspection-20260923T120035Z"
created: "2026-09-23T12:00:35Z"
status: "draft"
scope_filter: "disposition=open (all kinds; framework hat ⇒ no outward side)"
scope_entries: ["20260914T022757Z-speckit-feedback", "20260914T062401Z-speckit-feedback", "20260914T180702Z-skill-draw-echarts", "20260914T180923Z-skill-draw-plantuml", "20260914T181701Z-skill-draw-d3js", "20260915T065348Z-skill-create-skills", "20260916T032108Z-speckit-goal", "20260916T053329Z-skill-create-team", "20260916T061041Z-skill-create-team", "20260916T075612Z-skill-improve-team", "20260916T102352Z-skill-create-team", "20260916T135237Z-speckit-goal", "20260917T113354Z-speckit-goal", "20260917T121200Z-skill-create-team", "20260917T123109Z-speckit-requirements", "20260917T130112Z-speckit-clarify", "20260917T135437Z-speckit-plan", "20260917T145341Z-speckit-tasks", "20260917T180529Z-speckit-analyze", "20260918T065831Z-speckit-analyze", "20260918T114151Z-speckit-implement", "20260919T022511Z-speckit-implement", "20260920T064646Z-speckit-instructions", "20260922T070724Z-speckit-requirements", "20260922T101630Z-speckit-requirements", "20260922T131753Z-speckit-clarify", "20260923T023816Z-speckit-plan", "20260923T035059Z-speckit-tasks", "20260923T063219Z-speckit-analyze", "20260923T102013Z-speckit-implement", "20260923T110528Z-speckit-implement", "20260923T113303Z-speckit-feedback"]
supersedes: null
confirmed_at: null
---

# Introspection Report: introspection-20260923T120035Z

范围:本地库 32 条 open 条目(全部 `kind: internal`;入站目录 `feedback/` 零包)。本仓戴**框架帽子**,故不存在上行侧——21 个问题的分流决定恒为 `local-sink(<channel>)`。核验由 5 个并行只读子代理按亲和度分组执行(每组 ≤43 KiB,禁止整库注入),全部对**框架源**取证,未以 `.specify/` 镜像为权威。

**两条贯穿全批的元观察**(不属于任何单一条目,故不入 Findings,但影响处置方式):

- **路由死信已复发一次。** `.specify/memory/feedback/consume-log.md` 的 `2026-09-14 (batch 2)` 行记录了「22 queued direct-fix(下一轮执行)」,其中 create-skills 的「Step 6 缺测试基线纪律」经本轮实测**从未执行**(该技能自 b4fb16cb/09-11 后仅有 889b7cb4/09-20 的 feedback 指针重构,`SKILL.md:164` 的套件行源自 79080d35/07-29,全目录 `baseline|基线` 零命中)——即 F-21 是它的复发。日志行是持久记录,但没有任何机制把「排期到下一轮」的项带到下一轮。
- **子代理注入首次实跑生效。** 5 个派发均携带 `shared/guidelines/fast-fail.md` 的 owner 子句并要求显式异常行;回报 3 条 `ANOMALY`、2 条 `未发现异常` 之外的静默为零。3 条异常全部是**裁定**而非纠正,子代理停在本层上交,未就地修平——正是该纪律设计要拦的形态。逐条处置见 F-01(帽子归属)、F-02(`feedback-step.md` 自相矛盾)、F-09(前提已被既有 owner 覆盖)。

**覆盖核对(反空转哨兵)**:范围条目 32 = 问题成员 31 + Excluded 1,**恰好覆盖一次**,无条目跨问题重复归属。21 个问题、0 个空问题(每个问题至少 1 个成员条目)、0 个无证据锚点的问题。分流分布合计 21:`direct-fix` **13**(F-01,02,04,06,07,08,09,10,11,12,13,14,18)、`improve-skills` **6**(F-15,16,17,19,20,21)、`speckit-requirements` **2**(F-03,05)、`improve-docs` 与 `acknowledge-only` **各 0** 作为主分流(二者仅以次生根或问题内已修部分的形态出现:F-14 与 F-17 的次生根走 improve-docs,F-08 与 F-20 的已修部分记 acknowledge-only)。跨组复发已升优先级 2 处:F-18(两个独立报告者实测同一浏览器视口差)、F-21(与 09-14 已分流未执行项同根)。

## Findings

### F-01: `update-feature-index.sh` 以 `cat >` 整体重写索引,发出 6 列表头,而活动索引是 7 列且带 52 行逐行审计注记——照文档说法运行它会摧毁数据

- **根因**: 脚本把索引当作纯派生产物整体重写,而活动索引早已是**手工策展**产物(第 7 列 `Spec Path`、`Last Updated` 列内嵌审计结论如 `2026-08-15 (audit: delivered — ## Handoffs section present on all 23 command templates; row was stale-Planned)`、标题带 `🌱`)。二者对「谁是 owner」无单一归属点:脚本认为自己是,索引的实际形态说不是。同时本仓客户端实例 `.specify/instructions.md:11` 明文告诉读者「authoritative count 由该脚本维护」,把陷阱写进了每条命令都会读的常驻面。
- **证据锚点**: `scripts/bash/update-feature-index.sh:150`(`cat > "$FEATURE_INDEX"`)、`:164`(6 列表头 `ID|Name|Description|Status|Feature Details|Last Updated`)、`.specify/memory/features.md:8`(7 列,含 `Spec Path`)、`:10`(逐行审计注记实例)、`.specify/instructions.md:11`(归属说法,仅存于客户端实例)、`templates/instructions-template.md:14`(框架源对应行只写 `List of project features`,`git log -S "update-feature-index.sh"` 对该模板**零命中**——该说法从未进框架源)
- **成员条目**: 20260917T135437Z-speckit-plan(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 两半分别落,不可只做一半。**框架源半**(随包分发,影响每个下游项目):`scripts/bash/update-feature-index.sh` 二选一——(a) 改为增量更新,保留既有列结构与逐行注记,只刷新 `Total Features` 与确实变化的行;(b) 删除脚本,并在 `templates/instructions-template.md` 与 `.specify/shared/definitions/framework-map.md` 明写索引行为手工维护。留一个与文档说法相反的破坏性脚本比没有脚本更糟。**客户端实例半**:修正 `.specify/instructions.md:11` 的归属说法使其与实际 owner 一致(该行是生成器保留的自定义内容,不会被再生覆盖,但也永不下传)。**其中含一个待裁定项(上送用户,本轮未动)**:帽子归属本身已由子代理上交、经我复核确认——归属说法只存于客户端实例,故修复拆成上述两半,两半各自读法唯一,属纠正;但 (a) 与 (b) 之间是**裁定**,取决于是否还要保留「一键重算」能力,工件无记录。**默认建议 (b)**,因为 7 列 + 逐行注记的形态已经不可能由该脚本再生。
- **建议处置**: 20260917T135437Z-speckit-plan:processed

### F-02: 被每条命令逐字引用的 `shared/` owner 文档没有漂移守卫——失效路径、失实计数、不安全 shell 形态、以及一处自相矛盾的分类

- **根因**: 命令按 owner 的路径、计数与调用形态执行,而 owner 自身的路径存在性、实体计数、shell 形态从不由任何测试或生成器核对,于是失效指针与不安全形态被每条命令继承。`feedback-step.md` 更进一步:同一文件内判据与枚举互相否定。
- **证据锚点**: `shared/workflow/feature-integration.md:33,58,68`(`memory/feature-index.md` 为失效路径——实测 `memory/` 只有 constitution/features/knowledge/session;且 :33 状态机起点 Draft 与 :68「至少 Planned」矛盾)、`shared/definitions/agent-definitions.md:50`("seven shipped role agents" 失实——`agents/` 与 `.specify/agents/templates/` 实测各 2 个)、`shared/workflow/feedback-step.md:87`(散文反思走内联 `--review`,而引擎已支持 `--review-file`,见 `scripts/python/feedback-utils.py:1863`)、`:6-8` vs `:220` vs `:125`(复杂/简单命令判据与枚举互斥)、`templates/commands/clarify.md:97-100`(Validation 不重算计数、STR 引用检查未双向)
- **成员条目**: 20260922T131753Z-speckit-clarify(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`feature-integration.md:58,68` 的 `memory/feature-index.md` 改为真实注册表 `memory/features.md`,并消除 :33 与 :68 的状态机矛盾;②`agent-definitions.md:50` 的硬编码数量改为按目录派生的表述(与 `AGENTS.md` § Documentation Map 对 features 计数采取的「以自动派生的头部为准」同形);③`feedback-step.md:87` 把 `--review-file` 定为散文反思的默认形态、内联 `--review` 限一句话摘要(draw-* 技能已是该形态,可引为先例);④`clarify.md:97-100` 增「集成写入的计数 MUST 由工件重新导出」与「STR 引用检查双向跑」,并在 `### Question Generation` 约束列表补一行指向 `shared/guidelines/fast-fail.md:13-14` 的纠正/裁定分流(该 split 已由 Feature 052 落地,clarify 侧仅缺队列形态句)。**次生根**:为 `shared/` 下被命令引用的路径与计数建一个漂移守卫(`tests/contract/` 下新增),使本条的四个点位不再靠人肉巡检——该守卫是新增能力,与 F-03 的校验器同批设计更省。**其中含一个待裁定项(子代理上交,本轮未动)**:`feedback-step.md` 自相矛盾——按 `:6-8` 判据(调用脚本 / 产出被另一流程消费的制品即为复杂命令),`/speckit.team` 是**复杂**命令(`templates/commands/team.md` 有 9 处 `.py` 调用并产出 team.md),而 `:220` 的枚举把它与 `agents`/`constitution`/`feature`(各 0 处脚本调用)并列为 simple,`:125` 又称「四个 simple 命令」;该枚举写于 2026-07-14(999ea737),早于 2026-08-17 给 team.md 加入脚本调用。改判会**新增一个 command 探针**并改动「四个 simple 命令」这一计数,故属裁定:是补探针把 team 纳入反馈面,还是收窄 `:6-8` 的判据把 team 留在 simple,工件无记录。**默认建议前者**(判据是 owner,枚举是派生;枚举过期应以判据为准),但它会改变探针注册表,须用户确认后执行。
- **建议处置**: 20260922T131753Z-speckit-clarify:processed

### F-03: `requirements.md` 没有确定性校验器——计数与 FR/SC/STR 引用解析全靠目测,而字面标记匹配对「引用标记名」的规格自身是 grep-敌对的

- **根因**: `requirements-guidelines.md` 的 Validation Checklist 只给勾选项不给检查器;Program-First 已落到 tasks(`validate-tasks.py`)却未落到 requirements。同时活动标记的字面匹配无法区分「带问题正文的活动标记」与「反引号包裹的标记名引用」,而一份讨论澄清机制的规格必然大量出现后者。
- **证据锚点**: `shared/guidelines/requirements-guidelines.md:29,67`、`templates/commands/requirements.md:64-68`(清单计数在澄清回写**之前**更新,序自 3a2a6da8/2026-07-07 未变)、`scripts/python/validate-tasks.py:1-25`(同型先例,仅覆盖 tasks.md)、`shared/constants/clarify-taxonomy.md:85`(仅覆盖删除侧,插入侧无引用完整性校验)
- **成员条目**: 20260917T123109Z-speckit-requirements(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 新增 `scripts/python/validate-requirements.py`(照 `validate-tasks.py` 的 docstring 体例声明 Program-First 归属),检查:FR/SC 编号连续且按**文档出现序**、每个 `FR-\d+` / `SC-\d+` / `[[STR-\d+]]` 引用可解析、活动标记计数只数「带冒号且未被反引号包裹」的实例。在 `shared/guidelines/requirements-guidelines.md` § Validation Process 写成 MUST(计数与引用由脚本派生,MUST NOT 手打),并把 `templates/commands/requirements.md:64-68` 的清单更新明确置于澄清回写**之后**。
- **建议处置**: 20260917T123109Z-speckit-requirements:processed

### F-04: plan/tasks 要求制品携带派生数字与可复跑命令,却不要求机器在写入那一刻产出它们

- **根因**: 「作者声明 + 一条印出的命令」被当作充分证据;实跑要求只点名了个别点位(plan 的 quickstart/contracts、tasks 的结构校验),未点名的点位于是以记忆形态进入制品,命令本身过宽或错误也无人发现。
- **证据锚点**: `templates/plan-template.md:164-172`、`templates/commands/plan.md:156`(execution-verify 作用域不含 plan.md 自身的摘要表与 Mirror Obligations 的 Verify 列;`premise` 全文件零命中)、`templates/commands/tasks.md:76,137`(107/107 覆盖核算系自陈;前提重测命令自身的正确性无要求)、`scripts/python/validate-tasks.py:133,189-205`(`[P]` 启发式把**指针目标**当**写入目标**,两个只读引用同一 owner 的任务被误报并行冲突)
- **成员条目**: 20260923T023816Z-speckit-plan(成立)、20260923T035059Z-speckit-tasks(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`templates/plan-template.md` 的 Phase 1 ACTION REQUIRED 注增一句「凡印出的派生命令 MUST 实跑并贴真实输出,计数取该输出;含正则者 MUST 说明会否匹配非目标行」;②`templates/commands/plan.md:156` 把 execution-verify 作用域从 quickstart/contracts 扩到本命令**全部**制品,补「多步场景的 teardown 与 setup 同等实跑;清理步骤涉及引擎 action 者先核参数前置条件」,并加一句要求逐条免责**同时列出该例依赖的前提**(使下一阶段知道该重新探测什么);③`templates/commands/tasks.md:137` 补「前提重测命令 MUST 在生成期实跑并贴输出;存在更 naive 写法会给不同答案时 MUST 把陷阱形态一并写出」,步骤 5/6 之间新增机器覆盖核算(contracts 每条条款与每条 FR 恰被一行认领,由脚本印出未覆盖集);④`scripts/python/validate-tasks.py:189-205` 的 `[P]` 启发式区分写入目标与指针目标,`tasks.md:76` 在「justify each WARN」处补「按各行实际写入目标裁定,MUST NOT 靠删除被引用路径消音」。**次生根**:③的覆盖核算需 `validate-tasks.py` 接受制品目录,是本问题内唯一的新能力,与 F-03 同批实现。
- **建议处置**: 20260923T023816Z-speckit-plan:processed, 20260923T035059Z-speckit-tasks:processed

### F-05: 「条款由哪个任务转绿」这一归属关系对结构校验器不可见,跨 Phase 的绿点依赖无人报警

- **根因**: `validate-tasks.py` 的五项检查全部基于任务→任务图(ID 形态、唯一性、blockedBy、并行安全、story 标签);条款→任务归属只存在于契约散文里,无声明面可解析,故 MVP 截断时结构性不可满足的验收条件静默通过。
- **证据锚点**: `scripts/python/validate-tasks.py:10-24`、`templates/tasks-template.md`(无归属声明面)
- **成员条目**: 20260918T114151Z-speckit-implement(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 需要新能力而非小编辑——先在 `templates/tasks-template.md` 定义条款归属的声明面(行内 `[green: <contract>#<clause>]` 标记),再给 `scripts/python/validate-tasks.py` 增 WARN 级检查:解析该标记,若归属任务集中任一任务所处 Phase 晚于本行则报「绿点跨阶段」。把本批的处置形态(提前执行半前置 + 在两行写明被推翻前提)写进模板注释作为先例。
- **建议处置**: 20260918T114151Z-speckit-implement:processed

### F-06: analyze 的检测契约只以散文规则存在——无发射字段,故编排者无法机检检测代理是否真的应用了它们;跨轮 ID 方案也未钉死

- **根因**: `objective-analysis-gate.md` 的规则 3/4 是新增的**判定义务**,但报告表列(ID/Category/Severity/Location/Summary/Recommendation)没有对应**发射字段**;规则靠代理自觉。检测简报自身的前提(计数、结构)无机械导出要求,错前提会让整路检测瞄错方向;跨轮 ID 无约束,于是同一命令两轮用不同前缀,rerun delta 无法匹配。
- **证据锚点**: `shared/workflow/objective-analysis-gate.md:21-27`(传播面上限为散文,无 `propagation_surface` 字段)、`templates/commands/analyze.md:129,131`(检测代理指令未给「合法重复」判定测试)、`:203,206,210`(报告骨架无 Systemic Observations 槽位;ID 方案未禁 scope 前缀)
- **成员条目**: 20260923T063219Z-speckit-analyze(部分成立)、20260918T065831Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`templates/commands/analyze.md` §6 表增 `propagation_surface` 列(具名下游制品或字面 `none`),§5.5 增一条 intake 规则:`none` 的 CRITICAL/HIGH 行不得派发验证;②`shared/workflow/objective-analysis-gate.md` 规则 3 增产出形态句(发现行第一字段为传播面,严重度由其**派生**),并新增规则「简报中一切计数与结构前提 MUST 由编排者派发前机械导出;无法导出者写成待核实的开放问题,不写成断言」;③§4 检测代理指令点名 `shared/guidelines/one-source-of-truth.md` 的三条合法重复条件为「过期副本类」发现的判定测试(引用不改写);④§6 明确 ID 恒以 category initial 前缀、scope 记入 Category 列,MUST NOT 以 scope 字母编号;⑤报告骨架增设 **Systemic Observations** 槽位(聚合指向同一薄弱面的多条 MEDIUM,不抬单条 severity),使簇级观察有处落笔。`analyze.md` 侧只保留指针与本地参数,不复述 owner 规则。
- **建议处置**: 20260923T063219Z-speckit-analyze:processed, 20260918T065831Z-speckit-analyze:processed

### F-07: clarify Mode A 把「形式完备」当「语义完备」,且从不回访自己改号所影响的派生产物

- **根因**: Mode A 的机械核验只断言 ID 集合连续与 `- Q:` 行数递增,不含**出现顺序**;11 类 taxonomy 无一类去读 Assumptions 并问「这是裁定还是推断」,`Misc / Placeholders` 只扫 TODO 与未量化形容词,于是「推迟给后续阶段的假设」扫描结果为 Clear。集成义务清单枚举了 13 项 spec/registry 写回,无一项指向 `checklists/`;唯一再校验义务被关在 Scope Revision Protocol(前提是 plan/tasks 已存在),Mode A 永不触发;`/speckit.checklist` 每次只新建文件,重跑也不刷新旧的。
- **证据锚点**: `shared/constants/clarify-taxonomy.md:63-65`(Assumptions 仅 Mode B `:133`)、`:67-90`(Mode A 集成义务无 checklists 项)、`:85-86`(仅 ID 集 + 行数,无文档序)、`templates/commands/clarify.md:58-62,121,128`、`templates/commands/checklist.md:60`
- **成员条目**: 20260917T130112Z-speckit-clarify(成立)、20260917T180529Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`shared/constants/clarify-taxonomy.md` Mode A 增第 12 类 **Deferred-by-assumption**(命中条件:具名替代方案间的选择 / 指名后续阶段为决策者 / 含「若…则升级路径…」推迟子句);②§ Mode A Integration Rules 的 append-only 不变量旁增文档序断言(按出现顺序比对 `FR-\d+`,报 ORDER BREAK)——与 F-03 的 `validate-requirements.py` 共用实现,由脚本输出裁定,不新增人工目测;③「Removal & renumbering」义务后加一条:改号/增删 FR 后 MUST 复核 `checklists/requirements.md` 的计数断言(存在即刷新,不存在则记为待生成),并以 grep 断言零残留旧计数。
- **建议处置**: 20260917T130112Z-speckit-clarify:processed, 20260917T180529Z-speckit-analyze:processed

### F-08: implement 的收尾门禁不接纳「诚实的非绿」——合法瞬态红、穷尽式任务留开放、被实测推翻的门控前提都无合法表达

- **根因**: 阶段边界提交门只规定「名字级差集为空」,任务状态只规定 `[X]` 与 `[~]`(资源不可用),Step 8 只规定「按当前树重跑既定检查」而把检查所引用的前提当作恒真;升级计数器写在同一句散文里未说明生命周期;Step 9 同时写两个词汇表面却不点名拥有者。执行者于是被推向三种坏选择:合并前的红提交、改判据、或缩小任务描述。
- **证据锚点**: `templates/commands/implement.md:59,74,80,82`、`templates/commands/analyze.md:195`(`[~]` 豁免的证据绑定形态)、`shared/workflow/feature-integration.md:42,48-50`(void 规则仅覆盖 DoD 行)、`templates/feature-details-template.md:70`(`pass|deferred`)与 `templates/verification-log-template.md:22-26`(词汇拥有者)冲突、`docs/reference/history/00-cross-cutting-lessons.md:139`(阶段边界例外已记为经验,规则未引)
- **成员条目**: 20260923T102013Z-speckit-implement(部分成立)、20260923T110528Z-speckit-implement(部分成立)、20260919T022511Z-speckit-implement(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`implement.md:80` 的阶段边界提交规则加例外句并引用 `lessons:139`——既有守卫因任务排序**合法瞬态**变红时,两阶段合成一个提交单元,判据是合并后 `comm -13` 为空;②`:74` 的 `[~]` 理由域从「资源不可用」扩到「穷尽式要求本轮不可完成」,并明写由此导致的 Completion Gate fail 是**预期**结果、MUST NOT 靠改写任务描述或判据变绿;③Step 8 增具名动作 **Gate-premise decay**:门控/DoD 行引用的前提(冻结 SHA、行号、计数)被实测推翻时 MUST 重新引用、量测新形式**更严而非更松**、并在该行内联标注被证伪的前提(把 `feature-integration.md:48-50` 的 void 规则从 DoD 行扩到 `## Completion Gate` 项);同句声明「3 次连续拒绝」计数器按 run 归零并把值写入 `verification.md`;④`templates/feature-details-template.md:70` 的 `pass|deferred` 改为引用 `templates/verification-log-template.md:22-26`(词汇拥有者),Step 9 点名该拥有者;⑤演练复原形态写进 `:59` 或 `lessons:90`——精确反向替换 + `assert count == 1`,复核用「重跑该用例 + 该文件 `git diff` 为空」,不以 `cp` 退出码为准。**已修部分(acknowledge-only,同批结案)**:20260923T102013Z 的另 5 点已由 Feature 052 自身落地——`pytest -k` 子串/分区 token 规则(`lessons:85`)、管道吞退出码与凭记忆写 node id(`implement.md:64,66`)、自指哨兵探针串同形(`lessons:86`)、混用再生引擎需集合判据(`lessons:137-138`)、渲染入口静默返回 `rendered: 0`(`lessons:138`)。
- **建议处置**: 20260923T102013Z-speckit-implement:processed, 20260923T110528Z-speckit-implement:processed, 20260919T022511Z-speckit-implement:processed

### F-09: 运行期证据(baseline 名单、red-first 取证、quickstart 实跑输出)没有成文落点,每轮 tasks 各自发明路径

- **根因**: 路径约定只写在下游 `implement.md`,`templates/commands/tasks.md` 对 `baseline` / `notes` 零命中,于是 tasks 轮靠模仿邻 spec 推断;plan 质量门要求逐条免责却不要求列出该例依赖的前提,免责免掉执行义务的同时把前提真实性一并放过。
- **证据锚点**: `templates/commands/implement.md:64,82`(`<spec-dir>/baseline-failed.txt` + `--names-out` + `comm -13` 已 pin 死于 a996dc4a)、`templates/commands/tasks.md:105`(零命中)、`shared/workflow/feature-integration.md:60,76`(无 `notes/` 约定)、`docs/reference/history/00-cross-cutting-lessons.md:127-129,31`(`.git/objects` 桶可写性:经验已记,提交前探测一步未成文)
- **成员条目**: 20260917T145341Z-speckit-tasks(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`templates/commands/tasks.md` 的 Setup/Foundational 段 pin 死证据落点:`<spec-dir>/baseline-failed.txt`(**以指针指向 `implement.md:64`,不复制路径字面量**)与 `<spec-dir>/notes/{red-first-evidence,quickstart-run,pre-change-measurements}.md`,并写明再冻结时机;②`lessons` §二十 补「提交前 `test -w` 探测 `.git/objects` 桶可写性,比一次失败提交 + 三轮诊断便宜」。**异常处置**:子代理回报本条前提部分失实——条目称 baseline-failed.txt「无权威副本/位置不一致」,但 `implement.md:64` 早在 a996dc4a(先于本条目记录日)已 pin 死该路径与 `--names-out` + `comm -13` 形态;故判 PARTIAL,缺口收窄为「tasks 侧无指针与再冻结时机」。同条又称索引脚本丢的是 `Spec Path` 列,经先前 consume 轮已修正为 `Feature Details` 列——本轮按当前源码采信后者(实测 7 列索引中 `Spec Path` 确实存在且脚本不发,故**本条语境下反而是 `Spec Path` 会丢**;两处说法各自成立于一侧,已并入 F-01 的证据锚点,不再单列冲突)。
- **建议处置**: 20260917T145341Z-speckit-tasks:processed

### F-10: requirements 命令要求「照房子约定落笔」,却不给出约定的定位入口

- **根因**: 工件名、概念拥有者文档、词汇表的**约束侧**、收尾后到达的追加输入的处置,都未在任何步骤点名,代理只能猜路径或按训练知识写,ENOENT 与结构性错误要到下游阶段才暴露。
- **证据锚点**: `templates/commands/requirements.md:28,49-55`(`:53` 未点名工件文件名)、`shared/workflow/glossary.md:17-33`(无「约束侧读取」义务)、`shared/workflow/user-input-protocol.md:21-30`(§ Mid-Run Addendum Input 未覆盖**收尾后**到达的输入)
- **成员条目**: 20260922T070724Z-speckit-requirements(成立)、20260922T101630Z-speckit-requirements(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`requirements.md:53` 直接点名工件文件 `requirements.md`(或令其从模板名派生);②步骤 5 新增「概念拥有者核查」——需求引入或约束既有框架概念时 MUST 先定位 `shared/definitions/` 下的 owner 文档并据其定义落笔;③`glossary.md` §1 增「约束侧读取」义务(按主题域读已登记的机械上限、既定处置、已命名反模式),命令侧 `## Glossary` 只留指针;④`user-input-protocol.md` § Mid-Run Addendum Input 增一条**收尾后到达**的处置:重开上游工件、验证门重跑一次、三个收尾副作用各按增量重跑、不新起一次调用。
- **建议处置**: 20260922T070724Z-speckit-requirements:processed, 20260922T101630Z-speckit-requirements:processed

### F-11: instructions 的体积预算控制以散文消费一份不完整的脚本报告,测量与收尾记账都退回目测

- **根因**: `report_instructions_budget()` 只发射 live 文件的前 8 节字节数,缺 template 字节 / delta / placeholder 标记 / project-owned 分类;Action 2 的清单因此只能由眼判,R1/R2 各自再推导一次;命令尾部又缺 Artifact Commit 嵌入与备份保留规则。
- **证据锚点**: `scripts/bash/generate-instructions.sh:32,76-116`、`templates/commands/instructions.md:118,120,124,146-147,178`(无 artifact-commit 嵌入,而其余五命令均有)、`shared/workflow/artifact-commit-step.md`
- **成员条目**: 20260920T064646Z-speckit-instructions(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①扩 `scripts/bash/generate-instructions.sh` 的预算报告为一张脚本表(section / live bytes / template bytes / delta / placeholder-token present / project-owned);②`templates/commands/instructions.md:120` 的 Action 2 改为**强制消费该表**为观察工件,R1/R2 只从表上取候选;③R1 把占位符过滤前置为路由首句(判别式 `[`+`]`、`{{VAR}}` 机检化);④命令尾部按其余五命令同形嵌入 `shared/workflow/artifact-commit-step.md`(删除面审计 → 显式路径 → 禁 `git add -A` → 非本轮残留按上游偏差上报);⑤Action 3 加保留规则(保留最新 N 份 + 仍持有 live 缺失标题的备份,其余在残留报告中列名)。
- **建议处置**: 20260920T064646Z-speckit-instructions:processed

### F-12: `feedback.md` 的生命周期契约两端都有缺口——Path B 的收尾清理帽子盲,Path A 的确认后序列无中断/续跑规则

- **根因**: 技能已声明框架项目的 Path B 只由**显式请求**进入(因为此处的包没有收件人),但第 5 步的清理没有对应的帽子分支,于是「默认收尾动作」在框架帽子下会清空一个从未被 Path A 消化过的库,把条目的唯一可操作形态留进一个无法送达的 zip。另一端的确认→preserve→删除→追加日志行没有被定义为一个不可插入其他工作的序列,而唯一的持久标记(日志行)恰恰是序列的最后一步。
- **证据锚点**: `templates/commands/feedback.md:185`(Path B 第 5 步)、`:71,145,147,148,171`(A1 交叉核对、A5 原子性与 preserve-first)、`scripts/python/feedback-utils.py:1430-1437`(cleanup dry-run 只发裸 id 数组 + `removed` + `remaining_entries`,无计数字段)
- **成员条目**: 20260923T113303Z-speckit-feedback(成立)、20260914T062401Z-speckit-feedback(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`feedback.md:185` 改为**帽子感知**——框架项目仅当用户同时要求 `mark-submitted`(即该批确已了结)时才清理,否则保留并在报告中列为待定;客户项目维持现默认;②`feedback-utils.py` 的 cleanup 输出顶层补 `would_remove_count` 与 `remaining_after`,使 dry-run 可作摘要消费而不必先吞下整个 id 列表;③Path A Step 4 增一句:确认后 preserve / 删除 / 追加日志行 MUST 作为一个**不间断序列**执行,其间不插入任何其他工作;并规定续跑识别规则——intake 有包而 consume-log 无对应行时 MUST 先向用户确认是否为「已确认待清理」的续跑(不得默认按新输入重路由),确认结论写入该批次日志行。
- **建议处置**: 20260923T113303Z-speckit-feedback:processed, 20260914T062401Z-speckit-feedback:processed

### F-13: `goal-utils.py criteria` 在缺参时以空值静默覆盖,且引擎的读/写性在任何文档面上都未标注

- **根因**: 逐个追加 action 时只给了 `status` 必参守卫;`criteria` 的 `--criterion` 缺省 `[]` 直接进 `set_criteria`,而命令文档只列命令、不分读写,于是「查看判据」与「清空判据」共用一个入口——破坏性动作既未上确认门清单,也未 fail-fast。
- **证据锚点**: `scripts/python/goal-utils.py:753-754`(criteria 无守卫)vs `:748-749`(status 有 `required=True`)、`:800-806,441-457`(覆盖路径)、`templates/commands/goal.md:52-64`(命令块不分读写)、`shared/guidelines/confirmation-gates.md:16,39,47`(破坏性桶与存疑从严条)
- **成员条目**: 20260917T113354Z-speckit-goal(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ①`scripts/python/goal-utils.py` 给 `criteria` 加空值守卫(无 `--criterion` 且无显式 `--clear` → exit 2);②`--help` 与 `templates/commands/goal.md` 的命令块按**读/写分组**标注;③破坏性桶登记进 `shared/guidelines/confirmation-gates.md` 清单(存疑从严条已要求)。**注意**:③会改动门控扫描器的命中集合,而该扫描器的 total 上限被三处不同形态的断言钉死且整数余量为 0——须按 `shared/guidelines/fast-fail.md:306` 与 `tests/contract/test_fast_fail_discipline.py:1814` 的**零命中文本**手法措辞,不得放宽 `POLICY_DOCS`(该约束的 owner 归属见 F-01 次生根与 F-02)。
- **建议处置**: 20260917T113354Z-speckit-goal:processed

### F-14: goal 定义文档里的语义规则与修改侧能力都没有引擎/制品形态

- **根因**: 引擎只实现词面与结构层校验(GD-2 词表、Targets 表文法),而 `shared/definitions/goal-definitions.md` 的语义规则(Target 为无序集)与 authored 侧需求(改 objective、可读标题、承载排除项、判据主体可程序指代)无对应 action 或 section,于是「引擎通过」被误读为「定义合规」,且 objective 一经 create 即不可改。
- **证据锚点**: `scripts/python/goal-utils.py:76-77`(GD-2 词面漏掉阶段化措辞)、`:233-251`(无 scope-boundary/排除节)、`:397,415,730-733`(create 无 `--title`,标题即 slug)、`:715-776`(无 `objective` action / `set_objective`)、`:857`(`targets --check` 只回 `{"verdict":"ok"}`,缺 `check-statement` 已有的 scope 声明)、`shared/definitions/goal-definitions.md:10`(判据主体无「目录指代」形)、`:86`
- **成员条目**: 20260916T032108Z-speckit-goal(成立)、20260916T135237Z-speckit-goal(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: `scripts/python/goal-utils.py` 增 `objective` action(语义照 `set_criteria`:替换 + History 留痕 + bump updated + 终态只读)、`create --title`(缺省回落 slug)、`_render` 增可选 `## Boundaries`;`_STEP_VERBS` / `_bad_shape` 补阶段化探测(`阶段|第[一二三]步|phase \d|stage \d`);`targets --check` 的 verdict 补 scope 声明。**次生根(走 speckit-requirements)**:判据主体靠成员枚举太脆弱,需要一个新概念「目录指代形」,owner 为 `shared/definitions/goal-definitions.md`;另 `20260916T135237Z` 的「断言文件内容而非过滤后的 diff」一点,其同族形态(过滤形态与被过滤集不匹配)已由 `shared/guidelines/fast-fail.md:64`(FF-2)与 `lessons:78,92` 记录,但「读文件优先于读 diff」这一正面规则仍缺,归 improve-docs 一并落 `lessons`。
- **建议处置**: 20260916T032108Z-speckit-goal:processed, 20260916T135237Z-speckit-goal:processed

### F-15: create-team 的派生判据是词面的,且三处规则互不接线,冲突只能靠 agent 人工识别后绕开

- **根因**: preset 打分把 pattern 关键词与领域信号**等权相加**、`confidence_of` 只在 score≤0 时回 none;pattern 决策树 Q1 与 optimization-goals 的「持续/长期」词面判定都把有界交付物工作导向 continuous,而 operating-loops 强制 L1 起步(`max_subagents_per_cycle: 0`)形成死角;Type 准则与 serial 模板的「每席皆 Worker」各自成立却无消解条款。
- **证据锚点**: `skills/create-team/scripts/match-team-preset.py:39-44,91-96,99-108,160`、`skills/create-team/scripts/verify-territory-disjoint.py:73-82,124-136`(自比较假阳性)、`skills/create-team/references/patterns.md:12-16`、`references/optimization-goals.md:14`、`references/operating-loops.md:46,50,176,183`、`references/create-mode.md:14`、`templates/agents/agent-serial-orchestration-template.md:8`、`references/conceptual-model.md:32-52`、`shared/workflow/feedback-step.md:6-8,220`
- **成员条目**: 20260916T053329Z-skill-create-team(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 经 improve-skills 改 `skills/create-team`:①`matchedSignals` 为空 → confidence 压到 `none`,或输出加 `patternKeywordsOnly` 标注;②`patterns.md` Q1 增判据「工作主体为一次性交付物改动、长期性只在目标不设终止阈值 → Q1 判否,长期性由 Goal lifecycle 承载」,并与 `optimization-goals.md:14` 的词面判定互引;③在 `conceptual-model.md` 或 serial 模板其一显式消解 Worker/Meta 冲突(Worker 只产补丁到工作区,唯一 Meta supervisor 落 canonical);④`verify-territory-disjoint.py:124-136` 跳过 `a.slug == b.slug` 的自比较对(direct-fix,可先行)。**次生根**:`team.md` 有 9 处脚本调用却无 Feedback/Documentation 段,与 `feedback-step.md:6-8` 的判据相符而与 `:220` 的枚举矛盾——该矛盾的裁定见 F-02 异常处置,本条不重复主张。
- **建议处置**: 20260916T053329Z-skill-create-team:processed

### F-16: serial stage 的粒度与单次派发预算无对齐要求,stage 协议只查产物存在性

- **根因**: `create-mode` 步骤 5 与 `patterns.md` 的「Derive Stages from Intent」只要求列 stage/agent/依赖/outputs,不要求按受影响规模校验粒度,也不限制一个 stage 承载几种任务类型;Stage Execution Protocol 的 INVOKE 是单数、VALIDATE 只查「outputs exist」,于是 1476 字节的桩文件可通过;增量落盘只是 brief 里一句不可判定的话;多次派发累积与 retry 无区分。
- **证据锚点**: `skills/create-team/references/create-mode.md:15`、`references/patterns.md:185-192,220-232,224,96-103`、`references/execution-guide.md`(Interruption recovery 与 structured returns 仅限 iteration + continuous)、`skills/improve-team/SKILL.md:27-28,36-52`(`:41` Refinement Map 无「交付粒度超预算」行)、`scripts/python/goal-utils.py:552,605,715-776`(`preview_target_check` / `resolve_effective_target` 无 CLI 入口)、`templates/commands/team.md:114`
- **成员条目**: 20260916T061041Z-skill-create-team(成立)、20260916T102352Z-skill-create-team(成立)、20260916T075612Z-skill-improve-team(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 经 improve-skills 改 `skills/create-team` 与 `skills/improve-team`:①`create-mode.md` 步骤 5 + `patterns.md` Serial Chain 增 stage 设计纪律——落盘前对 `outputs` 涉及目录做**文件计数**,超单次派发规模即拆分,或在 team.md 声明「本 stage 由 N 次派发累积」;一个 stage 只承载一种任务类型(attribution 与 reconciliation 预算量级不同,MUST NOT 同 stage);②VALIDATE 增可程序判定的最小实质性检查(产物字节下限,或「每个已声明判定的目录名在产物中可检索」),派发载荷表增「增量落盘」必填项;③整批判定必须附 ≥2 个实读文件证据(接线 `shared/guidelines/fast-fail.md:45-51` 的机器绿条款);④`improve-team` Refinement Map 补一行「stage 反复撞派发轮次上限、产物只覆盖目标一小部分 → 交付粒度超预算 → 按目录规模拆 stage 或降为目录级 + 例外清单」,Behavior 步骤 3 补「归因量化必须可复算,产物条目数不是覆盖度」(对照 `operating-loops.md:62` 的不可自标绿条)。**次生根(direct-fix)**:`goal-utils.py` 增 `run-checks <team-slug> [--target]`,一次输出五项检查的 JSON verdict,使 `team.md:114` 的 run 前置不必依赖无入口的内部函数。
- **建议处置**: 20260916T061041Z-skill-create-team:processed, 20260916T102352Z-skill-create-team:processed, 20260916T075612Z-skill-improve-team:processed

### F-17: team run 模式的验证结论是散文自评,缺可复算的口径契约

- **根因**: Report 契约只有 Result Summary / Deliverables / Execution Detail 等自由段,无验证证据字段;「实跑校验 + 命令与结果片段」只写在 continuous L2+ 的独立验证者节里,有界 pattern 的 run 无对应要求,于是 `-k` 子集数字可当整体基线陈述、A/B 求差不是默认手段、worktree 不复制 git-ignored 文件的盲点无人披露、无复写检查以「我以为写了的短语」为查询集而假阴。
- **证据锚点**: `skills/create-team/SKILL.md:51-58`、`references/operating-loops.md:62,125-135`、`references/patterns.md:115`(isolation 仅提隔离,未提 ignored 文件不随 worktree)、`shared/guidelines/one-source-of-truth.md:23-29`(机械判据已存在但未被接线)、`docs/reference/history/00-cross-cutting-lessons.md:45-47,70-92`
- **成员条目**: 20260917T121200Z-skill-create-team(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 经 improve-skills 在 `skills/create-team/SKILL.md` 的 Report 契约增 **Verification** 必填段:①回归数字须注明全量或过滤子集(含 `-k` 表达式),子集数字不得当整体基线;②仓库存在长期既存失败时,独立验证的最小充分形式为「**同口径** A/B 失败集求差 + 差集逐项归因」(worktree A/B 的差集项须先排除 git-ignored 残留归因);③One-Source-Of-Truth 类验收先从**落盘产物**提取实际短语再反向计数,附 `one-source-of-truth.md:29` 的机械判据。**次生根(improve-docs)**:ignored-path 盲点与同口径规则宜同时落 `lessons` §七 / §十二,避免只在技能内可见。
- **建议处置**: 20260917T121200Z-skill-create-team:processed

### F-18: 技能把 `--window-size` 规定为等于内容高度,但无头 Chrome 的布局视口矮 ~87–88px,渲染证据截图底部被静默裁掉

- **根因**: 渲染证明关只校验「截图存在且非空白」,未把浏览器 chrome 的高度差纳入窗口尺寸预算,也没有「先读回绘制 bbox 再判裁切」一步;各引擎技能各自内联同一条命令,无人持有**跨技能**的证据几何规则。
- **证据锚点**: `skills/draw-echarts/SKILL.md:207`、`skills/draw-echarts/references/sds-realization.md:50`、`skills/draw-echarts/references/echarts-guide.md:682`、`skills/draw-d3js/SKILL.md:192`、`skills/draw-diagram/references/delivery-contract.md:77-91`(D6 无渲染证据行)
- **成员条目**: 20260914T180702Z-skill-draw-echarts(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 在七技能统一契约 `skills/draw-diagram/references/delivery-contract.md` 的 D6 增一行「**渲染证据几何**」:窗口高 = 内容高 + ≥100px 余量,或先量绘制 bbox 再判裁切;由 `draw-echarts/SKILL.md:207`、其 `sds-realization.md:50`、`draw-d3js/SKILL.md:192` **以指针引用**(数值不得三处复写)。**复发证据(本批最强信号)**:`draw-echarts` 实测 88px 与 `draw-d3js` 实测 87px 是**同一条摩擦的两个独立报告者**(同任务、同浏览器、各自实测),按 A4 的复发规则升优先级;`draw-d3js` 条目按「一条目一问题」归入 F-19,其 headless 视口点由本条覆盖。
- **建议处置**: 20260914T180702Z-skill-draw-echarts:processed

### F-19: 复刻保真只固化了输入侧(源图量测),验证侧与例外侧缺失,忠实度只能靠肉眼声明

- **根因**: `sds-realization.md` §3.4 把量测写成单向步骤(源图 → SDS),§4 校验只比对 SDS 内部一致性,没有一关把渲染读回的像素与源图连通域对齐;同时交付清单把所有条目写成**无条件项**,复刻下「图例色块 / 边标签常显开关」与源图忠实度直接冲突却无豁免通道。
- **证据锚点**: `skills/draw-d3js/references/sds-realization.md:130-142`(仅单向量测)、`:144-181`、`skills/draw-d3js/references/cycle4-improvements.md:3,5`(仍为待办)、`skills/draw-d3js/SKILL.md:252,258`
- **成员条目**: 20260914T181701Z-skill-draw-d3js(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ①`skills/draw-d3js/references/sds-realization.md` §4 增「关三:渲染读回 ↔ 源图差量」(连通域/像素 diff 迭代收敛 + 量化命中容差),并把 `cycle4-improvements.md:3,5` 的两条待办收编为该关的检查项;②`skills/draw-d3js/SKILL.md` 清单区加总则——`fidelity_intent=reproduction` 时不适用条目 MUST 显式标 **N/A** 并写明由谁承载该语义(如面板标题),MUST NOT 为凑清单偏离源图。**次生根**:本条目的 headless 视口点归 F-18。
- **建议处置**: 20260914T181701Z-skill-draw-d3js:processed

### F-20: 隐藏脚手架只记了「能做什么」,未记「叠加在已有可见边上会翻车」,而 layout 指南反而在邀请该组合

- **根因**: `sds-realization.md` §2.1 的表以「意图 → 手段 → 实测边界」组织,只覆盖**单条**隐藏边的效果;两条边(一可见一隐藏)构成的**图结构性质**不在表的表达范围内,而 `layout.md:201` 建议对回边用 `-[hidden]-`,等于邀请该组合(dot 对 2-环的反转不确定)。
- **证据锚点**: `skills/draw-plantuml/references/sds-realization.md:92-100`(表无此行)、`skills/draw-plantuml/references/guide/layout.md:201`、`skills/draw-plantuml/references/guide/large-diagram-playbook.md:108-117`
- **成员条目**: 20260914T180923Z-skill-draw-plantuml(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 `skills/draw-plantuml/references/sds-realization.md` §2.1 表后加一条与 §1.3 同形的硬规则:「同一节点对已有可见边时 MUST NOT 再叠加反向 hidden 边(构成 2-环,dot 反转不确定);要表达 rank 差改用不可见锚点列 + hidden down 链」,并在 `guide/layout.md:201` 的回边行加指针到该规则以免口径分叉。**良性事实精修(非冲突)**:条目称远端服务器「完全忽略 `<style>` 块」,现行源 `sds-realization.md:67` 记的是「嵌套选择器与单行冒号写法不可靠,扁平选择器 + 多行属性有效」——两者可完全调和(该次失败正是紧凑写法),不影响判定。同条目另两点已由 §1.2/§1.3/§2.1 固化,acknowledge-only。
- **建议处置**: 20260914T180923Z-skill-draw-plantuml:processed

### F-21: create-skills 的验证关只规定「要跑」,不规定「跑得能判别 / 红了怎么归因」——且它是 2026-09-14 已分流却从未执行的一项的复发

- **根因**: `pressure-testing.md` §0 只在两臂已跑出同结果**之后**要求判 inconclusive 并重设计(事后补救),缺前门/路由类技能的**事前选题规则**(选下层 description 线索指向错误方向的请求);`SKILL.md:164` 只规定跑哪个套件与无 `tests/` 时的回退,缺「同族并行编辑时先按技能归因 + 在完成报告引用归因命令」。
- **证据锚点**: `skills/create-skills/references/pressure-testing.md:11-19,26`、`skills/create-skills/SKILL.md:164`(源自 79080d35/2026-07-29,早于本条目)、`skills/create-skills/references/name-collision-and-layering.md:55`、`.specify/memory/feedback/consume-log.md`(2026-09-14 batch 2 行的 improve-skills 分流)
- **成员条目**: 20260915T065348Z-skill-create-skills(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ①`pressure-testing.md` §0 增**事前**选题规则——被测技能为前门/路由层时,场景 MUST 选下层 description 线索指向错误方向的请求,否则记 inconclusive(与 `name-collision-and-layering.md` §2 互指);②`SKILL.md:164` 增归因步:套件红时先 `pytest --tb=line` 读断言的技能清单按技能归因,区分既有负债与新技能回归,并把命令与结论写进完成报告。**复发标注**:本条与 2026-09-14 (batch 2) 已分流给 improve-skills 的「create-skills Step 6 缺测试基线纪律」同根,该分流经实测从未执行(全目录 `baseline|基线` 零命中)。按 A4 的复发规则升优先级,并作为「路由死信」元观察的唯一实证。
- **建议处置**: 20260915T065348Z-skill-create-skills:processed

## Excluded

- 20260914T022757Z-speckit-feedback — 条目自述 `No significant optimization points identified this run.`(规范形态),无可核验主张,不构成问题成员;建议处置 ignored,理由 clean-run-no-points
