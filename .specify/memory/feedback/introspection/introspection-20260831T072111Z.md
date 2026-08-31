---
id: "introspection-20260831T072111Z"
created: "2026-08-31T07:21:11Z"
status: "confirmed"
scope_filter: "disposition=open, kind=internal"
scope_entries: ["20260820T062957Z-skill-improve-skills", "20260820T075028Z-skill-improve-skills", "20260820T081055Z-speckit-feedback", "20260820T083201Z-speckit-feedback", "20260820T135721Z-speckit-sanitize", "20260820T135804Z-speckit-sanitize", "20260820T155821Z-skill-create-team", "20260821T032029Z-skill-improve-skills", "20260822T044605Z-skill-improve-skills", "20260823T145827Z-speckit-requirements", "20260824T021636Z-speckit-clarify", "20260824T030224Z-speckit-plan", "20260824T033222Z-speckit-tasks", "20260824T054639Z-speckit-implement", "20260824T125539Z-speckit-feedback", "20260827T033738Z-speckit-requirements", "20260828T054156Z-speckit-clarify", "20260828T061407Z-speckit-plan", "20260828T062345Z-speckit-tasks", "20260828T063009Z-speckit-analyze", "20260828T075753Z-speckit-implement", "20260828T140121Z-speckit-review", "20260831T033547Z-skill-git-workflow"]
supersedes: null
confirmed_at: "2026-08-31T09:34:43Z"
---

# Introspection Report: introspection-20260831T072111Z

## Findings

### F-01: improve-skills 的契约冲突处理只认「命名标题」且绑定编辑期，缺「修订条款」出口

- **根因**: grep `.specify/specs/**` 与 `tests/contract/**` 的义务被锚定在「命名标题」上且绑定编辑动作，playbook 步骤 2 的必读清单不含契约与 spec 目录；契约冲突只有「呈报 + 用户裁决」两条出口，没有「撤回/收窄条款并同步改靶测试」的原子第三条
- **证据锚点**: skills/improve-skills/SKILL.md:57; skills/improve-skills/SKILL.md:62; skills/improve-skills/references/loop-playbook.md:15-22; skills/improve-skills/references/loop-playbook.md:240-244; tests/contract/test_skill_home_workdir_template.py:287-299
- **成员条目**: 20260821T032029Z-skill-improve-skills(成立), 20260822T044605Z-skill-improve-skills(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把 grep 义务从「标题」改为「条款关键词」并前移进步骤 2 的必读清单（与 tests/contract/**、.specify/specs/** 一并读）；为契约冲突增加第三出口——撤回或收窄条款 + 同步改靶测试作为一次原子编辑、编号保留。test_skill_home_workdir_template.py:287-299 已按关键词而非标题断言，可作为该纪律的既有先例引用
- **建议处置**: 20260821T032029Z-skill-improve-skills:processed, 20260822T044605Z-skill-improve-skills:processed

### F-02: improve-skills 的 HC7「执行而非目视」没有规定断言对象

- **根因**: HC7 只要求「跑起来 / 行级追踪」，未规定断言什么，于是两个反向失败同源——一边把脚本输出原文全量转储进上下文，一边只信 exit 0 而不看写出的产物本身
- **证据锚点**: skills/improve-skills/SKILL.md:73; skills/improve-skills/SKILL.md:131; skills/improve-skills/references/skill-quality-checklist.md:99; shared/guidelines/token-efficiency.md:16,30
- **成员条目**: 20260820T075028Z-skill-improve-skills(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: HC7 补两句断言规范并同时写入（只写一半会让下一轮过度纠偏到另一端）：(a) 默认断言面 = 退出码 + 字段投影，禁止原文转储；(b) 写文件类脚本必须断言产物内容本身（存在性、结尾换行、关键字段），exit 0 不作为通过依据
- **建议处置**: 20260820T075028Z-skill-improve-skills:processed

### F-03: improve-skills 接线清单的变更单位只有「整个技能目录」

- **根因**: 步骤 7 的五步接线清单全部以技能为单位；`_OBSOLETE_SKILL_FILES` 已存在于 init 回收代码却未进清单，被改名的「概念/术语」没有 grep 步，退役合并也没有「能力对等核对 + 无法迁移阻塞项」的落点
- **证据锚点**: skills/improve-skills/references/loop-playbook.md:257-278; skills/improve-skills/references/loop-playbook.md:262; src/specify_cli/__init__.py:776-782; src/specify_cli/__init__.py:1790-1796
- **成员条目**: 20260820T062957Z-skill-improve-skills(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 清单增三行——文件级迁移（登记 `_OBSOLETE_SKILL_FILES` + 显式删除败方技能下的镜像副本）、概念级改名（grep 旧术语覆盖 `.specify/specs/**` 与 `.specify/memory/**`）、退役合并（赢方覆盖败方特性的对等核对表 + 第三方阻塞项记录）
- **建议处置**: 20260820T062957Z-skill-improve-skills:processed

### F-04: create-team 的 Resources 清单手工维护，improve-team 侧无 preset-id 存在性校验

- **根因**: 预置退役清单已补齐且各接线面经核实（该点已过时），但 Resources 的引用文件名仍是手写散文、无任何生成器或契约测试守护；improve-team 加载实例时不校验 `preset:` 指向的 id 是否仍存在，唯一防线是人工扫描步骤
- **证据锚点**: skills/create-team/SKILL.md:162-164; skills/create-team/references/team-presets.md:62-71; skills/improve-team/SKILL.md; skills/create-team/scripts/match-team-preset.py:44
- **成员条目**: 20260820T155821Z-skill-create-team(部分成立)
- **分流决定**: local-sink(improve-team)
- **优化方案**: Resources 列表改为扫描预置目录生成，或补一条契约测试断言「列表 == 目录实际文件」；improve-team 加载实例时校验 `preset:` id 存在性，缺失即提示并给出 Lineage 记法。附带核查项：当前两个 continuous 预置互相压低置信度，project-cluster 匹配只到 medium（阈值见 match-team-preset.py:44），预置数量增长前值得复核
- **建议处置**: 20260820T155821Z-skill-create-team:processed

### F-05: git-workflow 只认三层分支形状，且参考命令把远端硬编码为 origin

- **根因**: 托管块 schema 只有 MAIN/PRE/DEV 三行，`None yet.` 占位行被一律解释为「需要建立三层」，没有单主干形状；execute-commands 的前置校验与操作 A-D 全部写死 `origin`；前置校验只 gate 工作区干净，不核对目标分支与其 upstream 的 ahead/behind
- **证据锚点**: skills/git-workflow/SKILL.md:22; skills/git-workflow/SKILL.md:65; skills/git-workflow/references/execute-commands.md:10; skills/git-workflow/references/execute-commands.md:36,52,83,101,113; skills/git-workflow/references/execute-commands.md:24
- **成员条目**: 20260831T033547Z-skill-git-workflow(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: (a) 托管块增单主干形状（PRE/DEV 记 `-` + shape 标注），使 Bootstrap 一问收敛且写入后不再重复触发；(b) 远端引用改用分支自身 upstream（`@{u}` 或托管块 Tracking 列），体检增「Tracking 远端 ≠ origin」提示；(c) 前置校验固定输出 `git rev-list --left-right --count <branch>@{u}...<branch>`。本轮实测佐证：本仓库四个远端中 origin 是上游 fork（github/spec-kit），主干 master 跟踪 gitlab/master，照命令执行会拉错源；本地 master 落后的 2 个提交恰好改动了与未提交改动重叠的三个文件
- **建议处置**: 20260831T033547Z-skill-git-workflow:processed

### F-06: Mode 4 消费侧把跨包去重与投影交给 LLM，Program-First 在 intake 边界失守

- **根因**: 引擎 `--action` 无 bundle 作用域动作，Mode 4 步骤 1-3 用散文要求 agent 手工解包读全文并「建 unit × finding × bundle 表」；047 契约 C-13 明确「引擎不为自省新增只读动作」，把该缺口固定下来，而 token-efficiency 纪律明写计数/去重/排序/比对 MUST 交由确定性程序
- **证据锚点**: scripts/python/feedback-utils.py:1799-1801; templates/commands/feedback.md:90-116; shared/guidelines/token-efficiency.md:9; .specify/specs/047-feedback-introspection/contracts/engine-cli.md:42
- **成员条目**: 20260820T083201Z-speckit-feedback(成立), 20260824T125539Z-speckit-feedback(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 补一个 bundle 作用域只读动作（读 MANIFEST + 包内清单，输出去重后的 unit × point × bundle 投影），并把「先机械去重再读正文」写进 Mode 4 步骤 1；给 MANIFEST 增条目集指纹，使 byte-duplicate 包在消费端一眼可判。根因上游还有一处：未跑 mark-submitted/cleanup 时 action_package 会重复选中同一批，天然产出重复包（scripts/python/feedback-utils.py:996-1004）
- **建议处置**: 20260820T083201Z-speckit-feedback:processed, 20260824T125539Z-speckit-feedback:processed

### F-07: 引擎早有 --format json，但命令面与文档从不示范，agent 反复自造需求

- **根因**: `--format` 自 Feature 028 起就是全局参数、`list` 支持 json 输出，但 Mode 2 指引与命令参考只示范裸 `--action list`，`--format json` 只出现在 Mode 1 与新增的 Mode 5，导致 agent 把「已有能力」记成「引擎缺口」
- **证据锚点**: scripts/python/feedback-utils.py:1886; scripts/python/feedback-utils.py:1954; templates/commands/feedback.md:50; docs/reference/commands/feedback.md:26-28
- **成员条目**: 20260820T081055Z-speckit-feedback(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 在 Mode 2 第 2 步与命令参考的 list 示例上补 `--format json`（摘要投影用法），并说明现行输出契约：机读动作恒 JSON、呈现动作默认文本 + 可选 json。不需要任何引擎改动——这是指引覆盖面缺口，不是能力缺口
- **建议处置**: 20260820T081055Z-speckit-feedback:processed

### F-08: sanitize 的处置语义与执行能力不匹配，且清理对象被产品脚本持续再生成

- **根因**: 检查器对未注册孤儿镜像目录发 `delete/high`，apply 又结构性拒绝删除非空目录，二者对撞且无 archive 兜底；同时 create-new-skill.sh 持续把 `.migration-backups` 填回来，使同一条不可机械执行的 high 发现每轮复现
- **证据锚点**: scripts/python/sanitize-utils.py:586-590; scripts/python/sanitize-utils.py:860-862; scripts/bash/create-new-skill.sh:250; scripts/python/sanitize-utils.py:253; templates/commands/sanitize.md:32
- **成员条目**: 20260820T135804Z-speckit-sanitize(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 三处同时收口：(a) 对非空孤儿目录改发 archive 处置，或在确认后允许目录级递归删除，消除「建议了但执行不了」；(b) `.migration-backups` 归入生成物白名单，或让 create-new-skill.sh 写到不受治理的位置，从源头止住复发；(c) 台账呈现改为落盘 + 字段投影，并修掉模板同时要求「列出 pending 目标列表」与「摘要优先」的自相矛盾（pendingTargets 当前无上限、已 680 项）。本轮实测佐证：该目录已再生 11 个 layout-int-* 桩，并使 tests/contract/test_no_nested_skills.py 在真实工作区变红
- **建议处置**: 20260820T135804Z-speckit-sanitize:processed

### F-09: 跨轮结论与同会话调研未被承认为一等 spec 输入

- **根因**: user-input-protocol 把上下文严格限定为 `$ARGUMENTS`；requirements 只从最高编号 spec 取「房屋惯例」样本，其验证条款又只覆盖移植外部代码库；命令也没有 memory-recall 挂载（对照 clarify 的 `skills: study-project`）
- **证据锚点**: templates/commands/requirements.md:53; templates/commands/requirements.md:55; shared/workflow/user-input-protocol.md:9-19; templates/commands/clarify.md:17-18
- **成员条目**: 20260823T145827Z-speckit-requirements(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 在 requirements 的输入采集步骤显式承认两类一等输入——同会话已达成的结论、上一轮特性的结论（经 memory-recall 或 feature 详情文件锚定），并要求以锚点方式引用而非重述，避免重复调研
- **建议处置**: 20260823T145827Z-speckit-requirements:processed

### F-10: 澄清答案与 spec 冲突时，分类学规则指向「替换」而非「调和」

- **根因**: Mode A 集成规则命令「invalidates earlier statement → replace it (no duplicates)」，对「仓库源 vs 已安装副本」这类双侧各自为真的事实没有调和条款；答案处理本身也只有「yes/recommended 用建议」与「否则校验」两分支
- **证据锚点**: shared/constants/clarify-taxonomy.md:66-83; shared/constants/clarify-taxonomy.md:80; templates/commands/clarify.md:86; templates/commands/clarify.md:89
- **成员条目**: 20260824T021636Z-speckit-clarify(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 集成规则补一条调和分支：当自定义答案与既有 spec 文本冲突且两侧各自为真（不同运行态/不同副本）时，MUST 在同一条 FR 内并存两侧并标注适用条件，禁止择一替换；仅当一侧被证伪时才走 replace
- **建议处置**: 20260824T021636Z-speckit-clarify:processed

### F-11: 「外部权威即断言」的执行验证纪律散落各命令，Phase 0 设计期无要求

- **根因**: 执行验证只在局部存在——plan 的对应门禁是 Phase 1 产出后对示例命令的校验，requirements 的验证条款只覆盖移植外部代码库，research 把实验推给开放问题桶；Phase 0 载入设计假设时没有任何「对外部工具行为先实测」的要求，也没有共享约定文档承载这条纪律
- **证据锚点**: templates/commands/plan.md:108-123; templates/commands/plan.md:155; templates/commands/requirements.md:55; templates/commands/research.md:47; templates/commands/research.md:77
- **成员条目**: 20260824T030224Z-speckit-plan(部分成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 把「外部权威（构建工具、第三方行为）在承重前必须最小实测」提升为共享约定（与宪法的 configured ≠ used 同源），再由 plan Phase 0 / research / requirements 各自引用；Phase 0 增一步：凡设计承重于外部工具行为者，建最小 scratch 工程跑一次并记录实测结论
- **建议处置**: 20260824T030224Z-speckit-plan:processed

### F-12: 实现期失败归因只有「主体 vs 断言」一轴，环境/入口与并发外因无处落

- **根因**: 归因段只覆盖 subject-vs-assertion，升级路径只有 3-strike；现实中至少还有两轴未编码——并行会话在制品（需外归因 + 范围化验收）与双入口脚本 REPO_ROOT 误解析。后者是具体代码缺陷：sync-mirrors.py 与 sanitize-utils.py 仍用硬编码 `parents[2]`，是三个已加固兄弟脚本中唯一的漏网者
- **证据锚点**: templates/commands/implement.md:53; templates/commands/implement.md:71; scripts/python/sync-mirrors.py:56; scripts/python/sanitize-utils.py:540; scripts/python/gate-check.py:31-41; scripts/python/regen-command-copies.py:23-32
- **成员条目**: 20260824T054639Z-speckit-implement(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: (a) 归因段补两轴——外部/并行会话在制品（证据 = 他会话产物时间戳）与入口/环境误解析（证据 = 脚本解析出的根路径），各自给出范围化验收出口，不再一律走 3-strike；(b) 把 gate-check.py:31-41 的 `_find_repo_root()` 移植进 sync-mirrors.py 与 sanitize-utils.py，这一半是可立即执行的直修、已有三处兄弟先例。本轮实测佐证：本次运行正是踩了 sync-mirrors 镜像副本误解析，假报 596 处漂移
- **建议处置**: 20260824T054639Z-speckit-implement:processed

### F-13: 条目 schema 无「本轮已修」状态，陈旧抱怨成为默认输出

- **根因**: 047 那一轮 plan/analyze/implement 三处摩擦在同一轮内即被修好（review.md 的 Finding | Fix landed in | Verification 表逐条闭合），但条目在修复提交之后才落盘，且 schema 只有事后 disposition、没有「本轮已修」状态，于是条目仍读作未解决——直接上行会向消费方重复上报框架已修问题
- **证据锚点**: .specify/specs/047-feedback-introspection/review.md:259-266; templates/commands/plan.md:113; templates/commands/analyze.md:182; templates/commands/implement.md:45; scripts/python/feedback-utils.py:179,287
- **成员条目**: 20260828T061407Z-speckit-plan(不成立), 20260828T063009Z-speckit-analyze(不成立), 20260828T075753Z-speckit-implement(不成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 给条目增 `fixed_in_run` 语义（记录同轮闭合的修复锚点），反馈步骤在记录前先自查「本轮是否已修」并直接落该状态，消费侧据此跳过已闭合项。三条成员经核验均为不成立（修复锚点见证据），其原始诉求本轮不再上行，只以本条元发现上行
- **建议处置**: 20260828T061407Z-speckit-plan:processed, 20260828T063009Z-speckit-analyze:processed, 20260828T075753Z-speckit-implement:processed

### F-14: 子代理强制门的降级路径按命令逐个补，review.md 仍无 unavailable 出口

- **根因**: 一次上游子代理通道故障同时卡住 plan/analyze/review 三个命令；修复以逐命令加措辞的方式落地（plan、analyze 已补），没有落到共享约定，于是 review 的「每条 P0 MUST 由独立只读验证子代理确认」至今没有不可用路径，subagent-definitions 也只定义 native/virtual/external 形态、无 dispatch 失败协议
- **证据锚点**: templates/commands/review.md:73-79; templates/commands/plan.md:113; templates/commands/analyze.md:182; shared/definitions/subagent-definitions.md
- **成员条目**: 20260828T140121Z-speckit-review(部分成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 把「强制子代理门的降级协议」写成一条共享约定（两次 dispatch 失败即降级为直接原文复核 + 报告标注降级证据路径），再由 plan/analyze/review 统一引用；review.md 先补齐 P0 的不可用路径。该条目自身未记录优化点，摩擦只写在 Review 正文里，属未立项的潜在问题
- **建议处置**: 20260828T140121Z-speckit-review:processed

## Excluded

- 20260820T135721Z-speckit-sanitize — 纯门控观察记录：门控观察协议只要求记录 gate_id / 触发点 / 用户决定信号，三条「points」实为决策信号的散文化，经核对事实全部为真且描述的都是合规行为、零改进诉求；其唯一信息增量（非空目录变通）已由 F-08 以可执行形式承载，重复计入会虚增簇权重
- 20260824T033222Z-speckit-tasks — 条目自述 `No significant optimization points identified this run.`，无可自省内容
- 20260827T033738Z-speckit-requirements — 同上，条目自述无优化点
- 20260828T054156Z-speckit-clarify — 同上，条目自述无优化点
- 20260828T062345Z-speckit-tasks — 同上，条目自述无优化点
