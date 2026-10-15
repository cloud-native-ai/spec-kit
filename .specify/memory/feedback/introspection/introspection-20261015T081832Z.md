---
id: "introspection-20261015T081832Z"
created: "2026-10-15T08:18:32Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 (all kinds; framework hat ⇒ no outward side; --disposition open 单参读取受已知截断缺陷 M-1(batch-3 登记项)影响,实际以 --limit 0 全量 33 条为准)"
scope_entries: ["20261013T063920Z-speckit-requirements", "20261013T075025Z-speckit-clarify", "20261013T085446Z-speckit-plan", "20261013T092225Z-speckit-tasks", "20261013T161312Z-speckit-implement", "20261013T170150Z-speckit-feedback", "20261014T032305Z-speckit-requirements", "20261014T114130Z-speckit-clarify", "20261014T114233Z-speckit-goal", "20261014T121936Z-speckit-team", "20261014T123025Z-speckit-plan", "20261014T135407Z-speckit-tasks", "20261014T144015Z-speckit-requirements", "20261014T145111Z-speckit-implement", "20261014T160808Z-skill-manage-instructions", "20261014T160808Z-skill-memory-recall", "20261014T160808Z-skill-memory-record", "20261014T160808Z-speckit-instructions", "20261014T173237Z-skill-run-team", "20261014T173428Z-skill-draw-diagram", "20261014T173528Z-skill-run-team", "20261015T020937Z-speckit-clarify", "20261015T020938Z-skill-clarify-artifact", "20261015T024608Z-skill-improve-skills", "20261015T031340Z-skill-create-plan", "20261015T031340Z-speckit-plan", "20261015T034643Z-skill-create-tasks", "20261015T034643Z-speckit-tasks", "20261015T044233Z-speckit-implement", "20261015T044234Z-skill-implement-feature", "20261015T054947Z-speckit-implement", "20261015T054948Z-skill-implement-feature", "20261015T061745Z-skill-manage-feedback"]
supersedes: null
confirmed_at: "2026-10-15T09:06:20Z"
---

# Introspection Report: introspection-20261015T081832Z

范围:本地库 **33** 条 open 条目(全部 `kind: internal`,external_count: 0;`--limit 0` 全量实测)+ 入站目录 **5** 个包(77 条包内物料)。本仓戴**框架帽子**(root 实测 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五源目录俱在),不存在上行侧 —— 11 个问题的分流决定恒为 `local-sink(<channel>)`;Path B 未被路由选择。

**入站包身份(A1/A2,均无 consume-log 行,经用户裁定为一批新输入)**:`feedback-20260813T143655Z.zip`(4 条,2026-08-13 生成 @ f5416ce7,git-tracked@69d86e81);`feedback-20261008T140841Z.zip`(13 条,2026-10-08T14:08:41Z 生成 = 本库 submitted_at 时间戳,即本仓 Oct-8 mark-submitted 批次交付回自体,**孤儿** —— untracked 且 `git log --all` 零命中,删除不可恢复);`feedback-20261014T071321Z.zip`(28 条,git-tracked@dc181327,随 2026-10-15 merge 入树);`feedback-20261015T061707Z.zip`(16 条,本仓当日 06:17Z package 的 outbox 包交付回自体,**自投递副本** —— 16/16 文件名与本库 16 条 open 条目逐一同名,物料按本地条目计一次,**孤儿**);`feedback-20261015T070947Z.zip`(16 条,另一工作区生成 @ 9dbf37b9,git-tracked@69d86e81,Aug 旧条目 7 + Sep 1 + Oct-8 7 + 当日 sanitize 1)。五包互不为副本(条目集两两比对不等)。

**为何 bundle 条目不进 scope 名单**:同前批口径 —— 引擎 V-3 要求成员条目存在于本库索引;61 条 bundle-only 物料以**证据与复现**形态进入各问题证据锚点与 M 级元观察,由 A4 逐项写入 backlog;`scope_entries` 只含本库 33 条。

**核验方式**:4 个并行只读子代理按亲和度分组(G-A Aug 时代 12 条 / G-B Oct-8 时代 21 条 / G-C Sep–Oct 技能族 28 条 / G-D 本地库 33 条),全部对**框架根级源**取证(`path:line` 证据入 verdict 表 `/tmp/speckit-feedback-digest-IDGB/verdict-group-{A,B,C,D}.md`),未以 `.specify/` 镜像为权威。4 次派发均注入 fast-fail owner 子句并要求显式异常行 → 回报 ANOMALY 3 条(全部纠正类已披露)、`未发现异常` 2 条,无静默。合计核验 159 判定点:STILL-VALID 93 / PARTIAL 21 / ALREADY-FIXED 16 / NOT-OURS 15 / ack 14。

**same-author 条件**:本批 33 条由既往会话与本会话混合写下(本会话 4 条:20261014T173x×3、20261015T061745Z);本会话写下又被本会话分析的同作者对**存在**,但核验已委派给新鲜上下文只读子代理(客观化分析门的委派形态),且 4 条本会话条目的核验结论与本会话运行报告互证一致 —— 如实标注。

**覆盖核对(反空转哨兵)**:范围条目 **33** = 问题成员 **29** + Excluded **4**,**恰好覆盖一次**;Excluded 原因逐条列于文末,无任何条目同时属于问题与排除。

**分流分布合计 11**:`direct-fix` **5**(F-01、F-03、F-05、F-09、F-10)、`improve-skills` **4**(F-04、F-06、F-07、F-11)、`requirements` **2**(F-02、F-08)。

## 元观察(不属任何单一条目,由 A4 单独分流并落 backlog)

- **M-1(本批最高优先,盲检类)**:`scripts/bash/generate-instructions.sh` 调用的 `gitignore_add_pattern` 与 `git_repo_root` **在任何 shipped 文件中均无定义**(根级与镜像 common.sh 皆无,`git log -S` 历史亦无;实测 `bash -c 'type gitignore_add_pattern'` → not found),脚本仅靠操作者 shell 预导出的函数才能运行;叠加 `:2` `set -e` 下 `:50,201` 两处裸调在 .gitignore 不可写时**中止全脚本**(渲染/词表/符号链接全跳过)且不降级 warning。契约测试在本机绿**纯因环境继承** —— 典型「基线恒等于被比对象」盲检(FF-3 类)。同族:legacy `.ai/` 布局无 pre-check(条目 A-E1.2)。分流 `direct-fix`(补函数定义或内联 + warning 降级 + legacy pre-check),owner `scripts/bash/generate-instructions.sh`。
- **M-2:并发会话卷入获得第二次独立目击,且就在本批消化进行时。** 本轮运行期间实测另一会话在同一工作区并行作业:提交 `69d86e81`(15:27:41 +0800)把 3 个 zip 纳入 git、向本库写入新条目(20261014T144015Z、20261015T02xxxx–06xxxx 系列)、本地 master 在编排者最终核验后前移。与 G-B 条目 6 P1(artifact-commit-step 缺路径限定提交/staged 属核)及条目 3 P1(整文件 staging 卷入)**同根互证** —— F-01(bundle)路由的优先级因此上调。
- **M-3:孤儿字节码残留** `scripts/python/__pycache__/docs-utils.cpython-311.pyc`(源已迁 `skills/external/create-docs/scripts/`),不影响运行判定,留给 sanitize 路径消化。
- **M-4:run_id 时间戳 +8h 系统性偏移**(G-D 实测:条目 created(UTC)早于 run_id 内时间戳恒 8 小时,如 `20261015T020937Z` vs run_id `20261015T100920Z`)—— 疑调用方以本地时间传 run_id 与引擎 UTC 惯例混用;不影响本批判定,记为引擎/caller 约定观察,路由 acknowledge-only。

## Findings

### F-01: Wrap-up 编译嵌入行不含 `--run-id`/必填参数全集,而两个引擎逐参报错 —— 每个编译单元的每次收尾都要经历多轮试错

- **根因**: `probe-utils.py --action compile-embeds` 渲染的 Wrap-up 面只写 `--unit-id/--unit-type` 两个参数,不载明 `--run-id`(及 feedback 侧 `--review/--points`)必填全集;`run-determination.py:1390-1397` 与 `feedback-utils.py:716-728` 校验时逐参数顺序抛错 —— 契约两端脱节,摩擦被转嫁给每次运行。
- **证据锚点**: `templates/commands/plan.md:55-56`、`templates/commands/clarify.md:44-45`(嵌入行仅两参;同一 fingerprint 面覆盖全部编译单元);`scripts/python/run-determination.py:1390-1397`(--run-id → --complexity 顺序抛)、`scripts/python/feedback-utils.py:716-728`(--run-id → --review → --points 顺序抛);`scripts/python/probe-utils.py` grep run_id 零命中(渲染面无占位约定)。058 的 T033 只修了注册缺口(计数钉 71→72),渲染面未动。
- **成员条目**: 20261014T114233Z-speckit-goal(成立)、20261015T020937Z-speckit-clarify(成立)、20261015T020938Z-skill-clarify-artifact(成立)、20261015T031340Z-skill-create-plan(成立)、20261015T031340Z-speckit-plan(成立)、20261015T034643Z-skill-create-tasks(成立)、20261015T034643Z-speckit-tasks(成立)、20261015T044233Z-speckit-implement(成立)、20261015T044234Z-skill-implement-feature(成立)、20261015T054947Z-speckit-implement(成立)、20261015T054948Z-skill-implement-feature(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 三选一或组合 —— ① compile-embeds 渲染时内联该单元实际可派生的 `--run-id` 占位约定(如 `<run-id>` 显式占位 + 说明);② 两引擎缺参时**一次性**校验并列出全部缺失必填项(单错改全错);③ feedback-utils 的 record 在缺 review/points 时给出模板行示例。修复须同步全部既有编译单元重编译(fingerprint 变更),并跑 `--action probes --reconcile` 收口。次生根(本批 22–32 条目同时携带):instructions 超预算点归 F-02,不在此重复开方。
- **建议处置**: 20261014T114233Z-speckit-goal:processed, 20261015T020937Z-speckit-clarify:processed, 20261015T020938Z-skill-clarify-artifact:processed, 20261015T031340Z-skill-create-plan:processed, 20261015T031340Z-speckit-plan:processed, 20261015T034643Z-skill-create-tasks:processed, 20261015T034643Z-speckit-tasks:processed, 20261015T044233Z-speckit-implement:processed, 20261015T044234Z-skill-implement-feature:processed, 20261015T054947Z-speckit-implement:processed, 20261015T054948Z-skill-implement-feature:processed

### F-02: `.specify/instructions.md` 33898 B 超 32768 B 预算,而 R1/R2 收敛路径对「项目填充型大章节」均无合法候选 —— 机制性无解,需用户裁定

- **根因**: manage-instructions 的预算收敛两级路由覆盖不了当前形态:R1 排除 placeholder=yes/project-owned 章节,`skills/internal/manage-instructions/SKILL.md:286-303`;R2 仅收 project-owned > 4KB,`:310-317`;实际超标源是「placeholder 填充型 + project-owned 未达阈」的大章节 —— 两级皆不命中。今日实测 `.specify/instructions.md` = 33898 B(wc -c),超 1130 B。
- **证据锚点**: 同上三处 + `.specify/instructions.md`(现值实测)。
- **成员条目**: 20261014T160808Z-skill-manage-instructions(成立)、20261014T160808Z-skill-memory-recall(成立)、20261014T160808Z-skill-memory-record(成立)、20261014T160808Z-speckit-instructions(成立)
- **分流决定**: local-sink(requirements)
- **优化方案**: 需**用户裁定**取舍 —— a) 上调预算字面量(改 owner 判据,连锁全部钉值测试);b) 为「项目填充型大章节」增设 R3(如 highest-water-mark 章节整体外迁指针文件);c) 章节内容瘦身边际裁剪。走 `/speckit.requirements` 立项前先出三个方案的量化解。
- **建议处置**: 20261014T160808Z-skill-manage-instructions:processed, 20261014T160808Z-skill-memory-recall:processed, 20261014T160808Z-skill-memory-record:processed, 20261014T160808Z-speckit-instructions:processed

### F-03: feedback 引擎哨兵缺位 —— package 无视 dry_run、reindex 门前破坏性 unlink 且不在破坏性集合、cleanup 不写 submitted_at、mark_submitted 在 null 时全选、record 无身份戳、A3 无小批量快路档

- **根因**: 引擎面「本仓身份、破坏性范围、相称性阈值」未机检化 —— 干跑语义与破坏性动作未对齐确认门,靠人读文档兜底(文档侧 path-b-and-probe.md 已有 hat-aware/dry-run 先行,缺口全在引擎)。
- **证据锚点**: `scripts/python/feedback-utils.py:1151-1184`(package 无 dry_run,径直 write_package)、`:957-971`+`:415`(reindex 经 migrate_legacy_index unlink index.json,且 reindex 不在 `:1584-1585` _DESTRUCTIVE_ACTIONS、无确认门)、`:1190-1259`(cleanup 全文无 submitted_at 写点)、`:934-937`(mark_submitted submitted_at=null ⇒ selected=list(entries) 全选)、`:780-795`(record meta 无 workspace/framework-hat 身份戳);`skills/internal/manage-feedback/references/path-a-digest.md:100-103`(A3 仅零条目免报告,无小批量档)。
- **成员条目**: 20261013T170150Z-speckit-feedback(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① package/reindex 读 dry_run;② reindex 加入 _DESTRUCTIVE_ACTIONS 并加确认门(或改为原子重建);③ cleanup 时同步写 submitted_at;④ mark_submitted 在 submitted_at=null 时要求显式 `--all` 或 --since 边界而非默认全选;⑤ record 写入 workspace 身份戳(仓库根路径哈希),A1 交叉核对时识别外来条目;⑥ path-a-digest.md 增 A3 小批量档(低于阈值且已核验 ⇒ dispose,不落完整报告)。
- **建议处置**: 20261013T170150Z-speckit-feedback:processed

### F-04: run-team 派发载荷规范未成文 —— 评审席位载体体量匹配、反馈记录归属声明、重型管线分段落盘三条款全树零命中

- **根因**: run-team 技能仅 SKILL.md(88 行)无 references/,gen-1 实测的三类派发摩擦(评审席位 12 轮上限零产物、副本 Wrap-up 反馈步骤与子代理领地冲突、总结管线单代理中断)无条款承载。
- **证据锚点**: `skills/internal/run-team/`(SKILL.md 88 行,grep 载体/体量/反馈归属/分段落盘 零命中);`skills/internal/create-team/references/execution-guide.md`(67 行,同零命中)。
- **成员条目**: 20261014T173237Z-skill-run-team(成立)、20261014T173528Z-skill-run-team(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ① 派发载荷增载体匹配条款(评审席位按任务体量选运行载体或拆分范围);② 载荷显式声明反馈记录归属(执行者领地不含反馈存储时由编排者合并执行);③ 重型管线子代理分段落盘 + 可续设计。
- **建议处置**: 20261014T173237Z-skill-run-team:processed, 20261014T173528Z-skill-run-team:processed

### F-05: STR 引用语法无生成期前置面 —— 模板无前置条款、示例自身用反引号误导、checker 静默剥码,跨 056/057/058 三轮复现

- **根因**: 「消费行内联 [[STR-NNN]] 裸写勿入反引号」只存在于 checker 报错文案,生成期(template/skill)零前置;模板示例 `[[STR-NNN]]` 自带反引号形成误导;checker `strip_code_spans` 后匹配,反引号内不算引用但报错后才被习得。
- **证据锚点**: `scripts/python/validate-requirements.py:246-251`(报错文案)、`:93,204,219`(剥码匹配);`templates/requirements-template.md:155-169,176`(泛化句 + 反引号示例);`skills/internal/create-requirements/SKILL.md`(grep STR 仅 description 命中)。
- **成员条目**: 20261013T063920Z-speckit-requirements(部分成立)、20261014T032305Z-speckit-requirements(部分成立)、20261014T144015Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① `templates/requirements-template.md` Shared Strings 注释补一句「消费行内联裸写,勿入反引号」并改示例呈现形态;② `create-requirements/SKILL.md` 生成期同款提醒一句。次生根(条目 7 携带,已标注):init/refresh/sanitize 增 root 属主探测哨兵一行(实例已愈、机制未建,`sanitize-utils.py` grep st_uid/chown 零命中)。
- **建议处置**: 20261013T063920Z-speckit-requirements:processed, 20261014T032305Z-speckit-requirements:processed, 20261014T144015Z-speckit-requirements:processed

### F-06: SDD 生成链技能防错指引缺确定性条款 —— checklist「- [」保留形状、plan 预写机械拦截、tasks 分区编号顺序

- **根因**: 三条 STILL-VALID 同属「防错指引只有散文/事后复查,无生成期确定性条款」:checklist 结构规则无任务行保留形状条款且无机检;plan 的反预写只有文本纪律无落盘前拦截;tasks 有分区指引无编号顺序条款。
- **证据锚点**: `skills/internal/create-checklist/SKILL.md:107-110`(无保留形状规则;validate-requirements.py:11-30 无 checklist 面);`skills/internal/create-plan/SKILL.md:119-126,240-291`(Summarize-after 文本纪律,Post-Generation Gate 为事后复查);`skills/internal/create-tasks/SKILL.md:321-333`(分区与 [green:] 指引,无编号顺序)。
- **成员条目**: 20261013T092225Z-speckit-tasks(成立)、20261014T123025Z-speckit-plan(成立)、20261014T135407Z-speckit-tasks(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ① create-checklist 增「`- [ ` 前缀为任务行保留形状,说明文字改形」条款;② create-plan Step 4 末增机械预写扫描(摘要表/检测记录非空即落盘前打回);③ create-tasks 分区指引补「先定分区,再按分区顺序编号」。
- **建议处置**: 20261013T092225Z-speckit-tasks:processed, 20261014T123025Z-speckit-plan:processed, 20261014T135407Z-speckit-tasks:processed

### F-07: 命令型前提无与数字型前提同权的实测义务 —— 任务行命令字面(--write 等 flag)与引擎契约漂移到 implement 期才暴露

- **根因**: `create-tasks` 的前提核实义务枚举不含命令字面/flag 类,写前参数前置检查仅覆盖 plan 期示例;generate-instructions 模板节文本传播仍 additive-only(PARTIAL 次生根,管理侧 directed 更新已在)。
- **证据锚点**: `skills/internal/create-tasks/SKILL.md:227-231`(枚举无 flag 类)、`skills/internal/create-plan/SKILL.md:285-287`;`scripts/bash/generate-instructions.sh:164,203`(additive-only)vs `skills/internal/manage-instructions/SKILL.md:33,84,106`(directed 更新已在)。
- **成员条目**: 20261013T161312Z-speckit-implement(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: create-tasks 前提核实义务枚举补「命令字面/flag:以引擎 `--help` 实测或脚本 grep 取证」一类;模板节文本传播在 create-plan 前提面引用 manage-instructions directed 模式。
- **建议处置**: 20261013T161312Z-speckit-implement:processed

### F-08: 含计数的 SC/断言缺算术自洽机检 —— 同作者门抓出计数错属人验,checker 无对应查项

- **根因**: token-efficiency 程序优先纪律已编码,但 validate-requirements 的检查清单无算术自洽检查;次生根:词汇表富化的提交时序义务未编码(富化发生在 Artifact Commit 之后即漂浮)。
- **证据锚点**: `scripts/python/validate-requirements.py:11-30`(检查清单无算术项);`.specify/shared/workflow/glossary.md:45-61`(Progressive enrichment 无提交时序)。
- **成员条目**: 20261014T114130Z-speckit-clarify(成立)
- **分流决定**: local-sink(requirements)
- **优化方案**: checker 增查项:含计数的 SC/断言行做Σ子项=总数类算术自洽核;glossary 富化纳入当轮 Artifact Commit 或紧随小提交的时序条款。
- **建议处置**: 20261014T114130Z-speckit-clarify:processed

### F-09: create-team 树内单一真源未闭合 —— 字段顺序双源(goal.md 自列第二源)+ 模板 home ID 解析面未落字

- **根因**: goal.md §持久化 自列字段顺序与 create-mode.md 相异成第二定义点;schema 注释解析面未把「模板 home ID」列为合法解析目标。
- **证据锚点**: `skills/internal/create-team/references/create-mode.md:57-58`(name→slug)vs `skills/internal/create-team/references/goal.md:29`(slug→name);`create-mode.md:130,81` + `conceptual-model.md:92-94`(解析面仅 .specify/agents/ 两目录)。
- **成员条目**: 20261014T121936Z-speckit-team(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: goal.md 字段顺序行改指向 create-mode.md(引用不复制);create-mode.md 解析面补「模板 home ID 视为合法解析目标」一句。
- **建议处置**: 20261014T121936Z-speckit-team:processed

### F-10: Mirror Obligations 「一源多镜像对各占一行」未点名,sync DIFF 无显式对名 —— 057 实测漏第二镜像面靠 sync --check 兜住

- **根因**: 模板注释只有泛化义务("list EVERY affected copy")无一源多对形态点名;sync-mirrors DIFF 输出走 `DIFF {dst_name}/{rel}` 可推断但无显式对名,人工核对靠路径推断。
- **证据锚点**: `templates/plan-template.md:127-131`;`scripts/python/sync-mirrors.py:189-191`。
- **成员条目**: 20261014T145111Z-speckit-implement(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: plan-template Mirror Obligations 注释补一句「同一源文件每个镜像对各占一行」;sync-mirrors DIFF 输出附受影响对名。
- **建议处置**: 20261014T145111Z-speckit-implement:processed

### F-11: draw-diagram D7 交互交付验收缺版面量测机检 —— measure-svg-layout 类工具仅 mermaid/plantuml 层有,echarts 层无同类

- **根因**: 版面量测工具未覆盖 echarts 引擎层,D7 的 bounds-fit/布局验收只能靠代码级证据;次生:两条 ALREADY-FIXED(实测回写已闭环)与两条 NOT-OURS(宿主环境)为确认性。
- **证据锚点**: `skills/external/draw-diagram/references/types/mermaid/scripts/measure-svg-layout.py`、`…/plantuml/scripts/measure-svg-layout.py` 在;`…/echarts/scripts/` 无同类;`…/echarts/references/sds-realization.md:25,65`(zoom 实测已回写)。
- **成员条目**: 20261014T173428Z-skill-draw-diagram(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: echarts 层移植/适配 measure-svg-layout 类 SSR 量测脚本,D7 验收判据补机检补充口径。
- **建议处置**: 20261014T173428Z-skill-draw-diagram:processed

## Excluded

- 20261013T075025Z-speckit-clarify — 两点均为**执行偏离**非框架缺口(列投影意识/简报取证,规则已编码、当轮已自纠):token-efficiency.md:14-24、objective-analysis-gate.md:28 均在位
- 20261013T085446Z-speckit-plan — 三点全为既有纪律的**正向实效记录**(前提复测/同作者门/快速失败合规),无缺陷可修
- 20261015T024608Z-skill-improve-skills — 三点合规正反馈 + 一点 ALREADY-FIXED(git-utils Resource ID 已对齐:SKILL.md:279-282 vs :5)
- 20261015T061745Z-skill-manage-feedback — 单点为框架帽待定态语义的正向确认(与 F-03 的 mark_submitted null 全选隐患交叉,以 F-03 路由为准)
