---
id: "20260917T123109Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "051-user-facing-comprehension:2026-09-17:requirements"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "051-user-facing-comprehension"
partial: false
created: "2026-09-17T12:31:09Z"
summary: "原则级概念输入按 guidelines 的概念型输入规则先蒸馏为可落地切片(框架自身 vs 下游项目两个落地层级),再分片为 5 个 story(3xP1+2xP2),未抄写用户原话句式。有界调研(单次 Explore 委派 + summary-first + 定向 peek 050 头尾)产出带 file:line 的现状清单,核心基线「38 处独立措辞 / 0 真源 / 0 统一名字」为实测值"
---

## Review
原则级概念输入按 guidelines 的概念型输入规则先蒸馏为可落地切片(框架自身 vs 下游项目两个落地层级),再分片为 5 个 story(3xP1+2xP2),未抄写用户原话句式。有界调研(单次 Explore 委派 + summary-first + 定向 peek 050 头尾)产出带 file:line 的现状清单,核心基线「38 处独立措辞 / 0 真源 / 0 统一名字」为实测值并被 SC-003 用作可验证目标;预留标识符核查在起草前执行(候选文档名冲突 0);STR-006 逐字核对活动宪章 :155 并用 grep -c 复测「两个模板文件零命中」后才写入。两处真正的范围决策(界面类接入广度、Principle XIV 既有缺口处置)按判据以选项形式提交而非猜测,裁定回写时同步删除被取代的两条旧假设,未在 Assumptions 留双份说法。产物已按 Artifact Commit 约定单独提交(60a75ae9),删除面审计干净,未混入他命令产物。

## Optimization Points
- # `/speckit.requirements` run optimization points — 051-user-facing-comprehension (2026-09-17)
- ## Review
- 输入是原则级的概念材料("without jargon, with context"应被形式化并扩散),按 `requirements-guidelines.md` 的「概念/理念型输入先蒸馏为可落地切片」规则处理:先识别落地层级(框架自身 = 真源 + 扩散 + 守卫;下游项目 = 宪章导出),再按层级分片,而不是把用户原话的句式抄成 spec 结构。得到 5 个 story(3×P1 + 2×P2),每片独立可测。
- 有界调研(一次 Explore 委派 + summary-first)产出了带 file:line 的现状清单,使规格能引用实测证据而非猜测:核心基线「38 处独立措辞 / 0 份真源文档 / 0 个统一名字」是实测值,并被 SC-003 直接用作可验证目标。预留标识符核查在起草前执行(候选文档名冲突数 0);`STR-006` 逐字核对活动宪章 `:155`,并把「两个模板文件零命中」这一断言用 `grep -c` 复测后才写入规格。
- 两处真正的范围决策(界面类接入广度、Principle XIV 既有缺口处置)按判据以选项形式提交而非猜测;裁定回写时同时删除了被取代的两条旧假设,未在 Assumptions 里留下双份说法。
- ## 优化点
- ### 1. FR 中途插号导致交叉引用手工追逐,无完整性校验
- 把新 FR 插入既有编号组中部(在守卫组新增 FR-035),迫使原 FR-035 顺延为 FR-036,并需手工追改所有引用它的地方:Shared Strings 的 `Consumed by` 列、Key Entities 的关系句、SC 行、Clarifications、Assumptions。本次靠事后 `grep FR-035 / FR-036` 才确认无残留错引。
- 命令要求 FR「可测且无歧义」,但不提供任何引用完整性检查。建议:或约定新增 FR 一律追加到所属组末尾(避免插号),或提供一个轻量校验断言「FR 编号连续 + 每个 `FR-NNN` 引用都解析到一条已定义的 FR + 每个 `[[STR-NNN]]` 都解析到 Shared Strings 某一行」。后者与本规格 FR-029 要求的守卫同形,可复用。
- ### 2. 清单项「No [NEEDS CLARIFICATION] markers remain」对本领域的规格是 grep-敌对的
- 本规格合法地含两处**反引号包裹的标记名引用**——因为 FR-020 的作用对象本身就是 `requirements-guidelines.md:72-88` 定义的那个 `[NEEDS CLARIFICATION]` 提示模板。按字面计数会报「残留 2 处标记」,与实际的 0 处活动标记矛盾。
- 本次靠在清单证据格里显式写明区分来兜住,但这是人工补救。建议验证步骤区分**活动标记**(`[NEEDS CLARIFICATION: …]`,带冒号与问题正文、未包裹)与**对标记名的引用**(反引号包裹、无问题正文)。否则任何以 clarify/requirements 机制本身为对象的规格都会在这一项上假失败——而这类"框架自指"规格在本仓并不罕见(需求 041/044/050 均属此类)。
- ### 3. 大纲顺序使清单首轮的计数在提交前就已过期
- 大纲顺序是「写 spec → 建清单 → 验证 → 处理澄清」。清单的 Validation Record 因此在澄清回写**之前**填入了计数(35 FR / 14 SC / 22 场景 / 13 假设),而回写把实际值改成 36 / 16 / 26 / 14,导致六行证据需重写。
- 两个可选修正:① 把 Validation Record 的计数类证据推迟到澄清回写之后再写(清单骨架仍可先建);② 计数由 shell 机械派生而非手打——本次最终的「计数机械核验」段就是这么做的,它一次通过而手打的六处全部过期。
- ## Token 消耗观察 (token-efficiency)
- 一处可避免的返工:清单里手打的结构性计数(FR/SC/场景/假设/edge case 数)在澄清回写后全部过期,六行证据重写一遍。这属输出侧的重复劳动而非上下文注入侧的浪费——本轮的上下文注入是有界的(单次 Explore 委派 + 定向节选 peek 050 的头尾,未整读任何大文件),59 KB 的调研产物只在需要引用其 file:line 锚点时整读一次,该次整读是规格的 ~40 处锚点引用的直接来源,属「编辑目标」例外而非可避免消耗。修正方向即上文优化点 3 的②:计数机械派生。
