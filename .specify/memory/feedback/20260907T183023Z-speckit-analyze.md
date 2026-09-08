---
id: "20260907T183023Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "050-proactive-flow-trigger-analyze-20260907"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "050-proactive-flow-trigger"
partial: false
created: "2026-09-07T18:30:23Z"
summary: "只读约束全程遵守:未修改任何工件,唯一的写操作是本 feedback 条目(命令明示的 sanctioned exception)。"
---

## Review
只读约束全程遵守:未修改任何工件,唯一的写操作是本 feedback 条目(命令明示的 sanctioned exception)。

Step 1 用 check-prerequisites.sh --json --require-tasks --include-tasks 解析出 REQUIREMENTS_DIR 与 AVAILABLE_DOCS(data-model.md / contracts/ / quickstart.md / checklists/ / feature-ref.md / tasks.md 全在),Feature 绑定上下文取自 spec 的 Related Feature(Feature 050,高置信:ID/Name 双匹配 + 索引行 + 详情文件齐备)。

按 token 效率纪律分两段执行。第一段 Program-First:用一段脚本做确定性交叉引用与计数核对(26 FR / 15 SC 全部在 requirements.md 之外有提及;SC 在 tasks.md 中 15/15 被点名;契约条款 12+18+10+7=47 与各工件声称一致;data-model 7 实体、quickstart 6 场景、14 命名情境、51 任务行均与声称一致),脚本即发现两处线索:18 个 FR 未在 tasks.md 中出现(设计上由 feature-ref 的 FR→契约映射承担传递覆盖,需逐条核验该映射是否成立)、以及 FR-020 疑似无处落条款。第二段把语义检测委派给三个 fresh-context 子代理(覆盖度与一致性 / 契约与数据模型内一致性 / 注册表与宪法对齐),原因是本会话内这些工件全部由我撰写,自检存在结构性偏差。

三个检测通道共提出 37 条去重后候选,其中 10 条 CRITICAL/HIGH 按 step 5.5 交第四波 fresh-context 验证子代理(验证者只收到 finding 与证据位置,未收到检测推理,且非原检测者)。验证结果:1 条 CRITICAL confirm、7 条 HIGH confirm、3 条 downgrade(F-01 CRITICAL→HIGH:C-8 不受影响且 9 条中 7 条可通过改指 provenance.file 修复,仅 /speckit.feedback 在全部 25 个 Handoffs 段中零出现,才是真正不可满足的一对;F-05 HIGH→MEDIUM:三段式执行报告的义务其实由 confirmation-gates.md L54–60 拥有并已被 test_confirmation_gates_execution_report.py 机械断言,discipline-doc C-4 恰恰禁止复述,故属映射错误 + 新表面未纳入该测试的 AUTO_EXEC_SURFACES,而非孤儿义务;F-10 HIGH→MEDIUM:依赖缺口真实且比初判更宽(T023 同样未约束),但 T027 同时被 T024 与 T026 阻塞且断言 C-2 的 sync-mirrors exit 0,故会在同一故事内响亮失败,后果是返工而非交付陈旧镜像)。零条 reject,故无 Unvalidated Findings 附录。

最重要的两条:① CRITICAL —— plan.md 把 Principle XIV 记为 Pass,理由是种子 JSON 属 one-source-of-truth.md 的"a literal pinned in a test to detect drift"合法副本类别;验证子代理逐字核对该指南 L35–43 后判定该分类**文本上不成立**(guard copy 的定义是"pinned inside a test"且"serves the build, never the reader",而种子是 templates/ 下随包分发、被引擎每回合消费的运行时制品,守卫它的测试是另一个文件),三类合法副本全不符,按其 rule of thumb"改一个事实需编辑多个文件即纪律已破"成立;且 features/050.md 自身 L49 写着"另撰一份即造出第二真源,违反 Principle XIV"而 L22 又称其为合法副本,项目自有记录内部矛盾。按本命令 Operating Constraints,宪法冲突自动 CRITICAL 且不得重新解释,故 plan.md 应改记 XIV 为 Partial 并补 Complexity Tracking 论证(当前写的是 N/A,连带错误)。设计本身可站(分歧被 C-7 变成响亮失败、散文不可确定性解析使替代方案确实被封死),错的只是归类与门禁记账。② HIGH —— 14 条 seed provenance anchor 中 9 条不成立,使 FR-022 的"派生"前提、SC-013 的"100% 派生 / 0 新撰写"与 seed-derivation C-6/C-7 在实现期不可满足。两条同根:受控词表与种子派生是从 8 条已核实的 Handoffs 逐字样例**外推**到 14 行而未逐条核验其余各行造成的。

其余 MEDIUM/LOW 未走验证(按 step 5.5 规定跳过),多为计数漂移(校验规则组数 6 vs 实为 5、契约测试文件 3 vs 4、glossary 词条 5 vs 8、blockedBy 39 vs 37)、同一事实多处重述(门控预算字面量约 10 处)、以及若干可断言性缺口(status payload 键未钉、error code 声称封闭却只举 4 例、turnId/eventId 无 regex、proposals[] 无 schema、E6.config 缺 minSample)。另有三条设计层缺口值得实现前处理:complianceDone 无输入通道致 SC-012 空洞、s03/s13 同身份违反 V1.3、checklist-absent 越出封闭信号枚举致 s05 不可达(且 s14 与 quickstart 场景 3 直接矛盾)。

## Optimization Points
- **Step 4 的七个检测通道(A–G)全部是"工件之间"的一致性检查,没有一条是"工件与仓库事实"的核对——而本次最严重的发现恰恰属于后者**:三个独立检测通道里,最重的一条是 `data-model.md` §命名情境表的 **14 条 seed provenance anchor 中有 9 条不成立**(被引 `templates/commands/<x>.md` 的 `## Handoffs` 段里根本不含该行声称的目标流程名;`s14` 引的 L36/L41 甚至整段落在 Handoffs 之外)。这类缺陷让工件**内部完全自洽**(A–G 全过:契约条款互相引用一致、计数一致、术语一致),却建立在对仓库的错误陈述之上,实现期会直接让 `seed-derivation.md` C-6/C-7 与 SC-013 不可满足。step 4 现有的 C 通道叫「Underspecification: Tasks referencing undefined components」——但陈旧 anchor 既不是"未定义"也不是"歧义",它是**错的**,现有分类无处归。建议增设一个检测通道 **H. Repo-Fact Verification**:对工件中作为派生来源、现状锚点或判据出处而引用的仓库行号/文件/字面量,做抽样机械核对(本次这类引用共约 40 处,核对 14 条 anchor 就抓到了最严重的问题,成本很低);并把「工件与仓库事实分歧」显式加进 F 通道的清单。`/speckit.requirements` 有 reserved-identifier 核查、`/speckit.plan` Phase 0 有假设核实,而**实现前最后一道门 analyze 反而没有**,这个缺口的位置恰好最贵。
- **step 5.5 只要求"验证"独立,没要求"检测"独立;当分析者就是工件作者时,检测环节存在结构性自证偏差**:本次 requirements / plan / tasks / data-model / contracts / quickstart / feature-ref 全部由我在同一会话内撰写,随后由我执行 analyze。若按字面走流程(自己检测 → 仅把 CRITICAL/HIGH 交独立子代理验证),检测环节很可能根本产不出上述 9/14 anchor 失效、Principle XIV 分类错误这类"否定自己刚写的东西"的发现——而 step 5.5 的验证只能对**已被提出**的发现表态,无法补上未被发现的。实际做法是把检测本身也拆成三个 fresh-context 子代理(覆盖度/契约内一致性/注册表与宪法),结果 10 条 CRITICAL+HIGH 全部来自它们,其中 3 条被我自己的初判高估或低估(1 条 CRITICAL 降 HIGH、2 条 HIGH 降 MEDIUM),说明双向都在纠偏。建议在 step 4 增一条硬规则:**当分析代理在本会话内参与过被分析工件的撰写时,检测通道 MUST 委派给 fresh-context 子代理执行**(子代理只拿工件路径与检测清单,不拿分析代理的推理),分析代理只做汇总、定级与 step 5.5 的验证编排;并把该情形在报告里显式标注证据路径,与既有的「subagent-unavailable fallback 须标注 weaker evidence path」同构。
