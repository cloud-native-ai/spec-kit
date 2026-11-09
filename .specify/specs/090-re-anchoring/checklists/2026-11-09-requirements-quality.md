# Re-Anchoring 需求质量检查清单（requirements quality）

**Purpose**: 检验 Feature 090「Re-Anchoring（不忘初心 · 温故而知新）」**需求文本的写作质量**——方向锚是否可判定、五问的规则优先是否被钉住、T0/T1/T2 分层与触发是否可重算、五处面与守护面是否被点名到可验证、计数与基线主张是否可复算、clarify 裁定是否真正落回需求正文。每一条都是对需求文本（或它点名的 owner）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-09
**Feature (Requirement Scope)**: `.specify/memory/features/090.md`（Feature 090 Re-Anchoring）
**Requirements (What)**: [../requirements.md](../requirements.md) — 10 FR / 4 SC / 2 RS / A1–A6 / 1 个 clarify session（8 组 Q/A）
**Specifications (How, context only)**: [../plan.md](../plan.md)、[../data-model.md](../data-model.md)、[../contracts/](../contracts/)（4 页 / 31 条款）、[../tasks.md](../tasks.md)、[../feature-ref.md](../feature-ref.md)、[../quickstart.md](../quickstart.md)、[../research.md](../research.md) —— 只用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「本特性的需求是否已足以进入实现与评审」的复核者——评审者、`/speckit.analyze` 的检测者、以及本线的下一阶段执行者；他们**不会**重读 owner 文档或测试源码，只依据本清单与被引用的需求行。
**Reading scenario**: 复核者打开本文件，要决定两件事：(1) 哪几条需求缺陷必须在 analyze/implement 之前修掉；(2) 哪些 `fail` 条目可以登记为「已裁定、由下游行承载」而放行。他们按条目末尾的判定位（pass / fail / 观察）取结论，并沿 `[Req §…]` 锚回到需求正文逐字核对。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner）给出了答案；答「否」产出的是对 `requirements.md`（或该条目点名的 owner）的 finding，不是一条实现任务。判定位三值：**pass** = 需求文本已给出可判定的答案；**fail** = 需求文本未给出、或给出的答案与另一处权威冲突；**观察** = 需求文本可判，但判据落在需求之外（下游文档/工具），本阶段只登记记录点。
**Detection path**: 本清单的缺口发现按 `.specify/shared/workflow/objective-analysis-gate.md` 规则 7 的**降级路径**执行——本执行拓扑（stage worker，无派发权）无法派发只读子代理，故为单上下文受限直读；每一行的这一弱点在此一次性声明，适用于下面全部条目。规则 8（派发前提须机械导出）在降级路径下同样遵守：本清单引用的每个计数与命中都来自本轮实跑，逐字读数见 `../test-evidence/checklist-self-check.txt` 与 `../test-evidence/checklist-readings-2026-11-09.txt`。

## 一、方向锚与规则锚的可判定性

- [ ] CHK001 - 方向锚的「任务锚 ↔ 规则锚」二分为封闭集、且「只有任务锚即视为不完整」这条判定是写在需求正文（而非只写在 data-model 的 V-1）吗？[Completeness, Clarity, Req §FR-004] — **fail**：FR-004 只规定「MUST 同时包含」，未规定只含一半时的判定；该判定只存在于 `data-model.md` V-1 与 `contracts/direction-audit.contract.md` C-4，属需求缺口。
- [ ] CHK002 - 规则锚的成员是否有一份**可数、可命名**的清单，使「规则锚完整」不依赖读者自行展开「等」字？[Completeness, Measurability, Req §FR-004] — **fail**：FR-004 列 8 项（无人值守 / 不征求继续 / U4→下一阶段 / 先写脊后行动 / workspace guard / fast-fail / 确认门 / 预算）但无「封闭、共 N 项」声明；owner 页 §1.1 在同 8 项后追加「与报告纪律**等**」，`checkpoint-protocol.md` § 5 的 Q1（:45-46）写第 8 项为「the gate discipline」而非「确认门」。三处枚举不可互换，需求未指定哪一处为成员 owner。
- [ ] CHK003 - 「任何与方向锚冲突的动作 MUST 先停下」这条拦截规则是否有需求层锚点，还是只存在于 owner 页 §1.1 末尾？[Traceability, Gap, Req §FR-001] — **fail**：FR-001 只授权 owner 文档拥有「两个概念、重载分层与 agent 义务」，未点名这条停机规则；它在 owner 页存在而在 `requirements.md` 无对应 FR，属覆盖缺口。
- [ ] CHK004 - 「核心步骤」的四类触发在需求正文里是否被声明为**封闭集**，并给出不属于该集合的动作的判定？[Completeness, Clarity, Req §FR-005] — **fail**：FR-005 只写「每个核心步骤后」，四类触发（阶段 U4 / 包边界 / 检查点 / 子代理返回）只出现在 owner 页 §1.2 与 `data-model.md` E-2；需求正文既未枚举也未声明封闭，故「一次工具调用算不算核心步骤」在需求层不可判。

## 二、五问的规则优先与判定值

- [ ] CHK005 - 五问的**顺序**是否被写成需求级的不变量（Q1 必须是规则问），而不是只在 SC-002 与协议正文里描述？[Clarity, Consistency, Req §FR-005, Req §SC-002] — **pass**：FR-005 逐条列出五个方向且以「MUST **规则优先**」定序；SC-002 与 `contracts/direction-audit.contract.md` C-4/C-6 一致，未发现冲突。
- [ ] CHK006 - 第二问的禁止清单是否闭合——「以汇报代替执行」「把子代理轮次上限当作交回理由」这两项是全部禁止形态，还是示例？[Clarity, Completeness, Req §FR-005] — **fail**：FR-005 用顿号并列两项而无「仅限 / 例如」限定；owner 页 §1.2 Q2 与协议 Q2 逐字复述同两项，三处一致但都未声明闭合性，故一个不属于这两项的新漂移形态是否落在 Q2 内不可判。
- [ ] CHK007 - 第三问「下一步是否为计划命名的那一步」在无阶段计划（如子代理无 brief 的场合）时如何判定，需求是否给出分支？[Edge Case, Gap, Req §FR-005] — **fail**：FR-005 只说「计划命名的那一步」；「计划」在无 brief 的子代理、或被派发形态不清（需升到 T2）时不存在，需求未给出此时 Q3 的取道。
- [ ] CHK008 - `correction-applied` 这一判定值是否在需求正文被定义为可观察事件（做了什么动作即取该值），而不是留给协议解释？[Clarity, Measurability, Req §FR-005, Req §FR-007] — **fail**：FR-005 只列三值字面，FR-007 只规定「只有 `decision-needed` 上送」；三值中 `on-track` 与 `correction-applied` 的分界在需求层无定义，只由协议与 `data-model.md` E-4 承载。
- [ ] CHK009 - 「审计结论是陈述、MUST NOT 以征求用户『继续』收尾」是否被量化到可判的收尾形态（例如允许/禁止的句子形态），使两位复核者对同一段收尾给出同一判定？[Measurability, Clarity, Req §FR-007] — **fail**：FR-007 以禁令表述，未给出「什么算征求继续」的判据；相邻的 fast-fail 与 confirmation-gates owner 都采用封闭清单形态，本处无对应形态。

## 三、重载分层 T0/T1/T2

- [ ] CHK010 - T0 / T1 的**成本上限**（≈1 KB / ≈5 KB）在需求正文出现吗，且「约」的容差被定义了吗？[Measurability, Ambiguity, Req §FR-006] — **fail**：FR-006 只列三层与其触发，成本上限只出现在 owner 页 §2、`data-model.md` E-3 与 `plan.md` § Performance Goals；三处都写「≈/约」而无容差，需求层既无上限也无容差的判定口径。
- [ ] CHK011 - T1 的四类触发在需求正文是否与 owner 页、协议逐项一致（尤其「连续两次同向漂移」）？[Consistency, Req §FR-006] — **fail**：FR-006 只写「阶段边界/压缩后/子代理轮次上限后」，缺「连续两次同向漂移」；owner 页 §2 的 T1 行与 `data-model.md` E-3 均含该项，协议侧只在 `checkpoint-protocol.md:58` 以「two consecutive audits…escalate」把它写成升级规则、未列为 T1 触发。于是同一项在四处文本里有「是 T1 触发 / 不是 T1 触发 / 需求未提」三种状态，需求未裁定哪个是权威。
- [ ] CHK012 - 「MUST NOT 每工具调用重载全文」的**作用对象**是否明确（禁的是「全文」还是「每工具调用时的任何重载」）？[Ambiguity, Clarity, Req §FR-006] — **pass**：FR-006 的禁令宾语是「全文（每工具调用重载全文）」，阶梯本身由同条前半句定义，两读法在同一句内被排除其一的依据充分；不构成缺陷。
- [ ] CHK013 - T2 的触发条件「派发形态不清 / 处置卡死」有可判的判据 owner 吗，还是需求把一句自然语言当作可执行触发？[Ambiguity, Gap, Req §FR-006] — **fail**：FR-006 写在括号内两短语；owner 页 §2、`data-model.md` E-3、协议三处逐字复述同两短语，全树无一处给出「形态不清 / 卡死」的判据，需求层的可判定性未建立。

## 四、五处面、指针与覆盖

- [ ] CHK014 - 「五处面」在需求正文里是否被逐一点名到路径级，使 SC-001 的存在性可直接判定？[Completeness, Measurability, Req §SC-001] — **fail**：SC-001 写「owner 文档、两侧宪法、两侧指令面、agent 条款五处」——「两侧」两字承担了两条路径的指认，加上 owner 文档与 agent 条款共 5 个面，但 `data-model.md` E-5 列的是 **6** 个面（owner / 模板宪法 / 本仓宪法 / 模板指令 / 本仓指令 / agent 定义）。同一集合在两处给出 5 与 6 两种计数，需求未裁定哪个是权威计数。
- [ ] CHK015 - FR-008 要求的方向锚简报内容（入口复述 + 锚摘要）是否与 FR-004 的任务锚/规则锚两半分建立可判的对齐，使「简报携带锚摘要」不产生第二个格式定义？[Consistency, Clarity, Req §FR-008, Req §FR-004] — **fail**：FR-008 只说「派发简报携带锚摘要」；「锚摘要」在需求层无形态定义，`data-model.md` E-1 则把简报列为 `task_anchor` / `rule_anchor` 的第二载体。摘要的字段集与两份锚的字段集之间无映射规则。
- [ ] CHK016 - 指令面常驻段的「摘要 + owner 指针」是否被量化到可判边界（多少算摘要、哪些内容禁止在此复述），使 FR-003 与 FR-001 的「唯一 owner」不互相牵制？[Clarity, Consistency, Req §FR-003, Req §FR-001] — **fail**：FR-003 只写「摘要 + owner 指针」；宪法 XXII 与 `expression-gates.md` § 事实一致性都要求「≥2 处手写即缺陷」，但需求未给出摘要侧的机械下限（该下限由 `expression-gates.md` 自持且仅用于文本比对），故「摘要写到什么程度算第二定义点」不可判。
- [ ] CHK017 - 守护面的**成员**是否在需求正文闭合——FR-010 的括号内点两个测试，A5 又追加两个计数守卫测试，共 2 + 2；这是「本特性的守护面」的完整集合吗？[Completeness, Consistency, Req §FR-010] — **pass**：FR-010 括注（clarify C-4）明确「本特性实际使用两个守护测试文件」，A5 明确「共两个文件 + 两个计数守卫测试」，两处一致且 A5 逐一点名路径。
- [ ] CHK018 - RS-002 的联合验收句只列两条测试名（`test_constitution_double_landing` / `test_fast_fail_discipline`），而 FR-010 / A5 说守护面含四条测试——clarify 已把这条裁定为「枚举不全、不是事实错误」，这个裁定本身在需求正文留下了处置痕迹吗？[Traceability, Consistency, Req §RS-002, Req §A5] — **fail**：clarify Q/A（Session 2026-11-09）明确裁定「不在 clarify 改写 RS 行，交由 plan 的 Premises/验收口径统一」，但 RS-002 行本身至今未标注该裁定指针；单读 RS-002 的复核者会得到「两条测试」的结论。需求正文未承载自己作出的处置。

## 五、成功标准的可测量性与可复算

- [ ] CHK019 - SC-003 的「绿」与「零新增失败」是哪一种读数——`test_fast_fail_discipline` 在本分支基线上有 2 条**既有失败**（`tasks.md` § Environment Prerequisites 实测 2 failed / 129 passed），SC-003 写「绿」是否会与该基线冲突？[Conflict, Measurability, Req §SC-003] — **fail**：SC-003 逐字要求「`test_constitution_double_landing` 与 `test_fast_fail_discipline` 绿」，而 `plan.md` EP-003 / `tasks.md` DoD-4 / GATE-1 一律把验收口径改为「no NEW failure against the frozen baseline」。需求层与下游三处对同一判据给出互斥读法，且需求未登记这一修偏。
- [ ] CHK020 - SC-002 的收紧判据（「同一测试内同时断言 Q1 问规则**且**判定/动作先于目标」）是否足以排除「只断言字面 `Q1`」与「三值判定存在」两种伪证，使这条成功标准可在落地后不回退？[Measurability, Req §SC-002] — **pass**：SC-002 以括号明写两种不得代偿的伪证，且 `contracts/guard-tests.contract.md` C-7 给出 red control（Q1 改写为目标问时必须转红），判据可复现。
- [ ] CHK021 - SC-004 的「T0/T1/T2 在 owner 文档与 checkpoint 协议中一致」是否点名了比较对象与差异判定（逐项比触发、还是只比三层字面）？[Measurability, Clarity, Req §SC-004] — **观察**：SC-004 Source 已指定「owner §2 的 T0/T1/T2 表与 `checkpoint-protocol.md` §5 的 reload tier 行逐项比对，记录两侧路径与行号」，比较对象明确；但「一致」的容差（措辞不同是否算冲突，如 CHK011 的触发项缺失）未定义，记录点为 `../test-evidence/`。
- [ ] CHK022 - SC-001 的「以指针互引」在需求正文有可判形态吗（指针是否等于路径引用、是否需带章节锚）吗？[Measurability, Clarity, Req §SC-001] — **观察**：`contracts/re-anchoring-faces.contract.md` C-7 定义「every consumer is a pointer, never a copy」，可判形态由该条款承担；需求正文只写「以指针互引」。记录点：该条款 + `../test-evidence/`。

## 六、运行时栈、前提与依赖

- [ ] CHK023 - RS-001 / RS-002 的 `Premises` 列引用 `EP-001`，而 `requirements.md` 未定义该前提；需求正文是否给出了悬空前提的处置规则？[Dependency, Traceability, Req §RS-001, Req §A3] — **pass**：A3 明写「EP-001 是本特性将在 `plan.md` 定义的执行前提，当前悬空属预期；plan 阶段 MUST 把它写成可验证行」，处置规则在需求层有名。实测 `plan.md` § Execution Premises EP-001 已落地为 verified 行（`../test-evidence/` 记录）。
- [ ] CHK024 - RS-002 的 pin `pytest 9.0.3` 自带「closure 比较前须重新核对」这一时限条件，需求是否说明了核对动作由谁在哪一阶段执行？[Clarity, Traceability, Req §RS-002] — **观察**：RS-002 与 A1 两处都在文本层声明了复核时点（closure 比较前 / plan、implement 阶段重新测量），但没有点名执行动作的阶段行；记录点：`../test-evidence/` 的 closure 读数。
- [ ] CHK025 - 「本特性零新增第三方依赖」这条 pin 在需求正文有可复算的判据吗（比对哪一文件、哪一类行）？[Measurability, Req §RS-001] — **pass**：RS-001 把 Contract 列指向 `pyproject.toml` 并写明 pin 为既有 `requires-python >= "3.8"`，clarify Q/A 已实跑复算（`pyproject.toml:5` 无新增依赖行）。

## 七、术语、命名与跨面一致性

- [ ] CHK026 - 「方向锚」在需求层是否被绑定到唯一英文/中文术语（`task_anchor` / `task anchor` / `任务锚`），使跨面引用不产生第三个名字？[Consistency, Clarity, Req §FR-004] — **pass**：FR-004 与 owner 页 §1.1 一致用「任务锚 / 规则锚」；`data-model.md` E-1 用 `task_anchor` / `rule_anchor` 字段名，是同一实体的字段投影，非新术语。
- [ ] CHK027 - 「本特性已预先落地」这一事实状态是否在需求正文被显式声明为范围前提（即：契约面多为「验证既有实现」而非「新建」），使 SC 的「存在性」判据不被读成新建义务？[Assumption, Clarity, Req §Note] — **pass**：§ Note 明写「本特性的实现在本分支上预先落地（提交 `5a1041e4`、`55776937`）」，实测六个提交对象在本仓均存在（`git cat-file -t` 全部为 commit）。
- [ ] CHK028 - `Flow Class: execution` 与 `Flow Type: -` 的声明行是否满足特性线声明面文法（`## Related Feature` 之前、至多一行）？[Consistency, Req §Header] — **pass**：两行位于 `## Related Feature` 之前且各一行；`flow-class-check.py --action lookup --unit-id "spec:090-re-anchoring"` 实测取回 `flow_class: execution` / `flow_type: -` / `source: declaration` / exit 0。
- [ ] CHK029 - 五个 owner 指针面在需求层的授权口径是否一致（FR-001 owner 文档 / FR-002 宪法 / FR-003 指令 / FR-008 agent / FR-009 生成器），不产生「谁是唯一 owner」的歧义？[Consistency, Req §FR-001, Req §FR-009] — **pass**：FR-001 唯一授权 owner 文档拥有概念/分层/义务，其余各条只要求新增条目并「以指针引用 owner 文档」；FR-009 的生成器条目是 mandate 清单成员，非 owner。

## 八、边界、例外与非目标

- [ ] CHK030 - 本特性的**非目标**是否在需求正文被写下（哪怕以「MUST NOT 引入」形式），使 review 能判「未越界」？[Completeness, Gap, Req §FR-001] — **fail**：`requirements.md` 无 Non-Goals 节；非目标只存在于 `plan.md`（no new store/ledger/scorer/scheduler）、`data-model.md` 末段与状态脊 `direction_contract.non_goals`。需求层的边界判据缺位，且状态脊不是需求面。
- [ ] CHK031 - 「MUST NOT 引入新的评分系统 / 日志服务 / 调度器」这条禁令的需求锚是否可解析到某条 FR 编号，而不是只存在于宪法 XXII 与 plan 正文？[Traceability, Gap, Req §FR-001] — **fail**：FR-001 只界定 owner 文档的管辖内容；「不引入新机制」在 `requirements.md` 无独立 FR 行，只在 `plan.md` T-002 / 宪法 XXII 末条出现。以 FR 编号检索不到该禁令。
- [ ] CHK032 - 与 fast-fail 的**边界**是否被写成互不重定义的两条判据（何时用 fast-fail 的纠正/裁定二分、何时用方向审计三值）？[Clarity, Consistency, Req §FR-007] — **观察**：FR-003/FR-005 与 owner 页把 fast-fail 列为规则锚成员，边界说明落在 `plan.md` 宪法 XVI 行与 owner 页；需求正文未单列边界句，记录点为 owner 页 §1.1。
- [ ] CHK033 - 「只有 `decision-needed` 上送」与「审计是陈述」是否覆盖了上送之后的**处置义务**（由谁裁定、记录在哪）？[Completeness, Edge Case, Req §FR-007] — **fail**：FR-007 只规定上送条件；`decision-needed` 之后由谁处置、写入哪个载体，需求层无对应句（`data-model.md` E-4 只写 `surfaced=true` 的载体为 checkpoint / fast-fail 通道，处置主体缺位）。

## 九、跨产物一致性与可追溯性（需求自身视角）

- [ ] CHK034 - 需求编号空间是否闭合且引用可解析——`FR-001…FR-010`、`SC-001…SC-004`、`RS-001/002`、`A1…A6` 无跳号、无重号、无悬空引用？[Traceability, Req §Functional Requirements] — **pass**：`validate-requirements.py` 实测六项结构检查（id-contiguous / doc-order / ref-resolvable / marker-count / dup-id / path-marker）全部 pass，0 error / 0 warning（逐字读数见 `../test-evidence/checklist-validate-requirements.txt`）。
- [ ] CHK035 - 需求是否声明了自己的**读者**与阅读场景（文档型交付物的读者声明义务），使「谁是基准读者」不由下游推断？[Completeness, Gap, Req §Header] — **fail**：`requirements.md` 头部只有 Branch / Created / Status / Flow Class / Flow Type 五行，无 `**Readers**` / `**Reading scenario**` 两行；`doc-consistency-check.py --faces reader --path requirements.md` 实测报 `reader-declaration-missing`（逐字读数见 `../test-evidence/checklist-gates-2026-11-09.txt`）。
- [ ] CHK036 - 五问的文本在需求（FR-005）、owner 页 §1.2、`checkpoint-protocol.md` §5 三处逐字复述，「唯一 owner」纪律下的合法副本类型是否被点名？[Consistency, Req §FR-005, Req §FR-001] — **观察**：三处措辞不完全相同（owner 页 Q4「状态载体是否比最后一次提交/检查点更新」vs 协议 Q4「Is the state spine fresher than the last checkpoint/commit (HR4)?」），存在措辞漂移；副本合法性由 `shared/guidelines/one-source-of-truth.md` 的三类例外判，需求正文未点名哪一类。记录点：该 owner 文档。
- [ ] CHK037 - 需求是否声明了本特性的**制品计数口径**（10 FR / 4 SC / 5 面 / 31 条款 / 4 测试），使下游不得手工计数？[Traceability, Measurability, Req §Overview] — **观察**：计数散落在 plan/tasks/checkpoints 三处并各自可复算（本轮实测 10 FR、4 SC、31 条款 = 8+9+6+8、4 个测试文件）；需求正文不自持计数，按程序优先原则由各 checker 报告，非缺陷。

## Notes

- **本轮的意图默认值（无人值守，未访谈）**：Depth = Standard · Audience = Reviewer · Focus = 派发简报与需求文本共同点名的四个高风险簇——(1) 方向锚/规则锚的可判定性与五问规则优先的钉住；(2) 重载分层与触发的可重算性；(3) 五处面 + 守护面 + 计数基线的可验证性；(4) clarify 裁定是否真正落回需求正文。三个意图问题被跳过，因为派发简报已固定范围、深度与读者；没有用户自定条目被并入。
- **可追溯性**：37/37 条（100%）带至少一个 `Req §…` 锚（高于 80% 下限）；其中 11 条另带问题标记 `Gap` (6) / `Traceability` (7) / `Ambiguity` (3) / `Conflict` (1) / `Dependency` (1) / `Assumption` (1)，其余 26 条只按质量维度标记（Clarity 15 / Measurability 11 / Consistency 11 / Completeness 9 / Edge Case 2；一条可带两个维度，故合计大于 37）。全部 37 条为问句形态，无一以「Verify / Test / Confirm / Check + 实现行为」开头；37 条全部以问句收束（`吗？` / `？`）后才进入判定位。
- **判定分布**：pass 11 · fail 20 · 观察 6 —— 合计 37，与 CHK001–CHK037 编号连续一致，无重号。**fail 不等于实现坏掉**：本特性实现已预落地且四个守护测试在树上可跑；这些 fail 全部是**需求文本自身**的可判定性/一致性缺口（计数 5 vs 6、T1 触发缺项、规则锚枚举三处不一致、SC-003「绿」与基线冲突等），按本清单的边界它们不描述实现缺陷。
- **与 `.specify/skills/internal/analyze-artifacts/` 的关系**：本清单的 `[Gap]` 标记条目按该技能 § 5 的 H 面（checklist accountability）会在 analyze 阶段被逐条要求「raised-as-finding 或 disposition」。本清单**未**预写 `disposition:` 行——那是 analyze 门的产物；本阶段只把缺口登记为条目。
- **不修改任何非本阶段产物**：本轮只新增本文件与 `../test-evidence/checklist-*.txt`，未触碰 `requirements.md` / `plan.md` / `tasks.md` / `contracts/` / `research.md` / `data-model.md` / `feature-ref.md` / `quickstart.md`，也未修改任何实现面（owner 页、宪法、指令、agent 定义、协议、测试）。凡「需要改需求」的结论都写成条目，而不是就地编辑。
- **若只能先回答三条，先答这三条**：CHK014（同一「五处面」集合在 SC-001 与 `data-model.md` E-5 给出 5 与 6 两种计数——SC-001 是本特性唯一的最终验收句式）、CHK019（SC-003 写「绿」，而本分支基线实测 2 条既有失败，下游三处已改为「零新增失败」，需求层仍未登记该修偏）、CHK002（规则锚的成员在三处枚举不一致，含一个开放的「等」字——它正是本特性要防的「规则丢失」问题的需求侧镜像）。
- **降级路径披露**：同作者缺口发现按 `.specify/shared/workflow/objective-analysis-gate.md` 规则 7 降级为单上下文受限直读，理由是本执行拓扑无派发权。这不是覆盖性主张；`/speckit.analyze`（独立上下文、只读）应复核本清单未命中的缺口。
- **门禁读数（G-checklist-reader / G-checklist-duplicate，blocking）**：`--faces duplicate --spec-dir` → `pass`（12 个文件，0 条 finding，exit 0）；`--faces reader --path <本文件>` → `pass`（读者两行在前 40 非空行的第 8–9 行）；`--faces reader --spec-dir` → `not-applicable`，因为 `check_reader()` 只在显式 `--path` 下执行（`doc-consistency-check.py:879-885`），`--spec-dir` 分支恒返回 `not-applicable`。后者是本阶段发现的一处**门禁形态缺陷**（算子行的命令形态与判据覆盖面对不上），按本阶段边界不改脚本、只登记，逐字读数见 `../test-evidence/checklist-gates-2026-11-09.txt`。
- **类别读取（本阶段唯一一次）**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:090-re-anchoring"` → `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null` / exit 0，故本阶段门禁集逐字不变、零新增阻断项（`expression-gates.md` § 特性线阶段命令的 checklist 行只对表达类追加算子）。
