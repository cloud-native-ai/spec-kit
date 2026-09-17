---
id: "20260917T180529Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "051-user-facing-comprehension:2026-09-18:analyze"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "051-user-facing-comprehension"
partial: false
created: "2026-09-17T18:05:29Z"
summary: "严格只读,零制品修改。因全部工件均为同一会话内自己撰写(经 requirements/clarify/plan/tasks 四次命令),自审证据力弱,故按 Feature 050 先例把检测与验证都委派 fresh-context 子代理:3 个检测代理(规格↔计划↔研究一致性 / 计划↔契约↔任务覆盖 / Feature 链接与宪章对齐)+ 12 个验证代理(每个 CRITICAL/HIGH 一"
---

## Review
严格只读,零制品修改。因全部工件均为同一会话内自己撰写(经 requirements/clarify/plan/tasks 四次命令),自审证据力弱,故按 Feature 050 先例把检测与验证都委派 fresh-context 子代理:3 个检测代理(规格↔计划↔研究一致性 / 计划↔契约↔任务覆盖 / Feature 链接与宪章对齐)+ 12 个验证代理(每个 CRITICAL/HIGH 一个,只收 finding 与证据位置,不收检测推理,且不验证自己产出的发现)。结果 46 条发现(0 CRITICAL / 3 HIGH / 30 MEDIUM / 13 LOW)。验证波次改写了严重度分布:12 条送验中 2 confirm、10 downgrade(1 CRITICAL→HIGH、4 HIGH→MEDIUM、5 HIGH→LOW)——检测代理系统性高估,而每次降级都附可核查理由(缺陷未向下传播 / 既有测试已兜住 / 免责句被误读为主张 / 归属错误但覆盖实际存在);若直接上报检测结果会把 1 CRITICAL + 11 HIGH 交给用户,其中 10 条不成立。三条确认的 HIGH 都只有独立复核才抓得到:G-4(T056 的 git diff --stat | grep '\.(py|sh)$' 永远匹配不到任何东西,验证者在真实提交上跑了两种形式对照并在 6 个提交上循环 stat_matches 恒 0 ⇒ FR-033/SC-011/DoD-7/gate-neutrality C-5 全部空真)、G-1(FR-008 被 feature-ref 与契约映射表双向声称由 discipline-doc C-13 覆盖,但 C-13 正文无任何消费单元断言,该词在 tasks.md 与 contracts/ 零命中、V1.1–V1.6 无一条断言它 ⇒ 映射自洽而被映射对象不存在)、I-01(第三轮订正改了 FR-035/SC-015/SC-015 Source 却漏掉 US3 验收场景 7 与同故事 Independent Test,后者是验证代理额外发现的第二处 ⇒ 订正未扫全引用面)。另检出 4 条映射真值类缺陷(G-3/T-2/T-3/G-5)与一个簇级系统性缺口:gate-neutrality 这份契约 7 条几乎全部未落 CI,而它守护的正是门控预算整数余量=0 这一最脆约束。I-05 追到根因是机制缺口而非作者疏忽(clarify-taxonomy.md Mode A 的 13 项集成义务无一触及 checklists/,唯一再校验义务被关在 Scope Revision Protocol 里而本轮是 Mode A;并在 041 的清单找到同型证据 17 FR vs 实际 21)。Feature 链接与宪章对齐经独立复核全部干净:索引 51 行=表头计数、7 列齐、ID 001–051 无缺号、051 索引↔详情零分歧、四个阶段在两个表面均记录完整、状态正确保持 Planned、8 个绑定候选的 Status 与同胞数逐条准确、14 行宪章逐字同序、版本 1.11.0→1.12.0 的 MINOR 判定正确、零模板占位符残留。K-01 经验证判定为 Principle XIV 的计数纪律失误而非 Principle V 的 MUST 违规(计划未增删或重分类任何 agent),故宪章carve-out 不适用、降级成立。本轮无同需求的前次分析,故无 rerun delta。上一轮被 .git/objects 12 个 root 桶阻断的两个提交已于本轮开头补做(用户已自行 sudo chown),删除面审计均干净。

## Optimization Points
- # `/speckit.analyze` run optimization points — 051-user-facing-comprehension (2026-09-18)
- ## Review
- 只读分析,零制品修改。因**全部工件均为同一会话内自己撰写**(requirements.md 经三轮订正、plan.md、research.md、data-model.md、contracts/×5、quickstart.md、feature-ref.md、tasks.md 全部出自本轮之前的四次命令),自审证据力弱,故按 Feature 050 的先例把**检测与验证都委派给 fresh-context 子代理**:3 个检测代理(规格↔计划↔研究一致性 / 计划↔契约↔任务覆盖 / Feature 链接与宪章对齐)+ 12 个验证代理(每个 CRITICAL/HIGH 一个,只收到 finding 与证据位置,不收检测推理)。
- 结果:**46 条发现(0 CRITICAL / 3 HIGH / 30 MEDIUM / 13 LOW)**。验证波次改写了严重度分布——12 条送验中 **2 条 confirm、10 条 downgrade**(1 条 CRITICAL→HIGH,4 条 HIGH→MEDIUM,5 条 HIGH→LOW)。这个比例本身是最重要的信号:检测代理系统性地**高估**了严重度,而每一次降级都附带一条可核查的理由(缺陷未向下传播 / 已有既有测试兜住 / 免责句被误读为主张 / 归属错误但覆盖实际存在)。若直接上报检测结果,会把 1 条 CRITICAL 与 11 条 HIGH 交给用户,其中 10 条并不成立。
- 三条确认的高severity 发现,都是**只有独立复核才抓得到**的形态:
- **G-4**:T056 的验证命令 `git diff --stat --diff-filter=A … | grep -E '\.(py|sh)$'` **永远匹配不到任何东西**——`--stat` 的行尾是 `| N ++++`,且长路径被省略成 `.../name`。验证代理在一个真实提交(新增 `scripts/python/validate-tasks.py`)上跑了两种形式对照:`--stat` 形式零命中 exit 1,`--name-only` 形式正确命中;又在 6 个提交上循环,`stat_matches` 恒为 0。于是 FR-033 / SC-011 / DoD-7 / gate-neutrality C-5 全部是**空真**。
- **G-1**:FR-008(消费单元)被 `feature-ref.md` 与契约映射表**双向声称**由 discipline-doc C-13 覆盖,但 C-13 的正文里没有任何消费单元断言;该词在 `tasks.md` 与 `contracts/` 中零命中,`data-model.md` 的 V1.1–V1.6 也没有一条断言它。映射表自洽、被映射的对象不存在——这是"断言覆盖"与"实际覆盖"的典型分离。
- **I-01**:第三轮订正把 FR-035 / SC-015 / SC-015 Source 改成了具名观察名单,却漏掉 US3 的验收场景 7 与同故事的 Independent Test(后者是验证代理额外发现的、检测代理没报的第二处)。订正**没有扫全引用面**。
- ## 优化点
- ### 1. 检测代理的严重度需要一次强制的"传播面"追问
- 12 条送验里 10 条被降级,而降级理由高度同构:**缺陷是真的,但它没有到达任何下游制品**。I-01 的验证代理明确写了"the practical blast radius is confined to the spec's acceptance-scenario set";I-04 的验证代理跑了 `grep -n 'FR-020'` 遍历全部 7 个制品文件,证明 9 处命中里只有 2 处是错的、且没有任何任务或契约条款继承该误读;M-1 的验证代理证明那一行镜像义务被**两个**任务各验证了一次。
- 检测阶段的提示词里我要求了 evidence boundary,但没要求**先追传播面再定级**。建议在检测代理的指令里加一条强制追问:"在给出 severity 之前,列出这个缺陷会被哪些下游制品继承;若答案是零,severity 上限为 MEDIUM。"这一条能把 10 次降级里的大部分前移到检测阶段,省掉验证波次的一半开销。
- ### 2. 映射表是**断言**,不是证据;analyze 应当把"映射自洽性"与"映射真值"分开检查
- 本轮最贵的一类缺陷(G-1、G-3、T-2、T-3、G-5)有同一个形状:`feature-ref.md` 或契约文件里的映射表说"X 由 Y 覆盖",X 与 Y 都存在、编号都对得上,但**打开 Y 的正文,它并不表达 X**。G-1 是 FR-008↔C-13;G-3 是 SC-002↔surface-pointers C-13(该条款的判定针是"规则复述",与"引擎调用形态泄漏"是两个对象);T-3 是 FR-036↔discipline-doc C-6(C-6 钉死的七节里没有观察节);G-5 是 gate-neutrality C-1c 要求一条"宪章原则块零 BLOCKING_RE 命中"的测试,而 constitution-export 的 12 条里没有它。
- 这类缺陷靠读映射表**永远查不出来**,只能逐条打开被引用的条款正文比对。建议在 analyze 的覆盖检查里把它单列一个 pass:"对每个声称的 X→Y 映射,引用 Y 的正文并判定 Y 是否真的表达 X",而不是只检查 Y 是否存在。
- ### 3. 一个成簇的系统性缺口:最硬的约束反而最没有进 CI
- 把 Agent B 的 T-2、G-5 与 G-4 放在一起看,浮现一个簇:**gate-neutrality 这份契约(7 条)几乎全部没有落到 CI**。C-2/C-3/C-5/C-6/C-7 被声明"由 discipline-doc 测试承载",但 T003(该测试文件唯一的撰写任务)的范围只列了 discipline-doc C-1…C-16,于是这 5 条只剩手工 shell 核验;C-1c 要求的那条断言在 constitution-export 里根本不存在;C-5 的唯一执行任务 T056 用的命令是空真(G-4)。
- 而这正是**门控预算整数余量 = 0** 的那份契约——本特性最脆、一旦破就打爆两个既有测试的约束。逐条看每个都是 MEDIUM,合起来看是"最高风险的约束拿到了最弱的守卫"。建议在报告里允许**簇级观察**:单条 severity 不动(避免未经证据就抬级),但把同指一个薄弱面的若干条聚合成一条 systemic observation 上报。本轮我在报告的"系统性观察"节这么做了。
- ### 4. `checklists/requirements.md` 的过期是**机制缺口**,不是本轮的作者疏忽
- I-05 的验证代理追到了根因:`shared/constants/clarify-taxonomy.md:67-90` 的 Mode A 集成规则列了 13 项义务(含残留引用扫描),**没有一项**触及 `checklists/requirements.md`;唯一的再校验义务在 `templates/commands/clarify.md:122` 第 4 步,而它被关在 **Scope Revision Protocol** 里(前提是"plan/tasks 已存在"),本轮是 Mode A 故从未触发;`/speckit.checklist` 每次运行创建**新文件**,重跑也不会刷新旧的。
- 并且这不是孤例——验证代理在 `041-refactor-feedback-probe/checklists/requirements.md:26` 找到了同型证据(声称 17 FR、实际 21)。⇒ 这是**重复发生的机制缺口**,按 Principle XI(修复落机制侧)应当修 `clarify-taxonomy.md` 的 Mode A 集成规则,给"清单计数再核验"加一项义务,而不是逐个 spec 手工刷新。本轮只报告、不修改(只读)。
- ## Token 消耗观察 (token-efficiency)
- 本轮是**代理密集**的一次:3 个检测 + 12 个验证 = 15 次子代理调用。这是命令 §5.5 的硬性要求(每个 CRITICAL/HIGH 一个独立验证者、不得验证自己产出的发现),不是可省开销;但 12 条里有 10 条最终被降级,意味着**验证波次的产出主要是"否证"**。若按优化点 1 把传播面追问前移到检测阶段,送验数量可能从 12 降到 4–5,省下约 60% 的验证开销。这是本轮最大的可避免支出,且可避免的方式是改提示词而非少做事。
- 上下文注入侧本轮很省:三份检测报告我只读结论(其中 Agent B 的覆盖矩阵与机械核验清单是高密度证据,整读一次即够);12 份验证报告各 <450 词(提示词里限了字数)。**未**把 8 份工件重新整读进上下文——它们是本会话内自己写的,仍在上下文中,只有需要逐字比对时才定向重读(如 FR-020 的 9 处命中、C-13 的正文)。
- 一处不可预见但值得记录的浪费:上一轮 `/speckit.tasks` 的提交被 `.git/objects/` 的 12 个 root 桶阻断,本轮开头补做提交时才发现用户已修好权限。若在提交前先 `test -w` 探测各桶可写性,一次探测比一次失败提交 + 三轮诊断 + 一轮用户交互便宜得多。
