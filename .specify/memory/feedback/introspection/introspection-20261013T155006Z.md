---
id: "introspection-20261013T155006Z"
created: "2026-10-13T15:50:06Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 (all kinds; framework hat ⇒ no outward side)"
scope_entries: ["20261006T143136Z-speckit-feedback", "20261006T150118Z-speckit-team", "20261006T170532Z-speckit-team", "20261006T172913Z-speckit-instructions", "20261008T033549Z-speckit-team", "20261008T061227Z-speckit-instructions", "20261008T073541Z-speckit-team", "20261008T073805Z-speckit-requirements", "20261008T090856Z-speckit-team", "20261008T093319Z-speckit-clarify", "20261008T121234Z-speckit-plan", "20261008T124946Z-speckit-tasks", "20261008T132002Z-speckit-implement", "20261008T133457Z-speckit-review", "20261008T133825Z-speckit-implement", "20261008T135121Z-speckit-review", "20261008T140013Z-speckit-feedback", "20261009T032137Z-speckit-team", "20261009T034653Z-speckit-team", "20261009T064957Z-speckit-team", "20261009T081108Z-speckit-team", "20261009T181710Z-speckit-team", "20261011T021048Z-speckit-team", "20261011T025327Z-speckit-goal", "20261011T130143Z-speckit-team", "20261011T135147Z-skill-improve-skills", "20261011T144800Z-speckit-team", "20261012T074736Z-skill-merge-skills", "20261012T081732Z-speckit-team", "20261012T115637Z-speckit-team", "20261012T123030Z-skill-summarize-project", "20261012T140155Z-speckit-sanitize"]
supersedes: null
confirmed_at: "2026-10-13T16:22:12Z"
---

# Introspection Report: introspection-20261013T155006Z

范围:本地库 **32** 条 open 条目(全部 `kind: internal`,`external_count: 0`)+ 入站目录 **3** 个包。本仓戴**框架帽子**(root 实测 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五个源目录俱在),故不存在上行侧 —— 12 个问题的分流决定恒为 `local-sink(<channel>)`;Path B 未被选中,也未被显式请求。

**入站包身份(A1/A2)**:`feedback-20260807T113350Z.zip`(12 条,git-tracked,`manifest.md` 自陈「rebuilt from archived entries after local package deletion」,**新物料**);`feedback-20261008T140028Z.zip`(12 条,git-tracked,**自我投递副本** —— 12/12 文件名与本库 12 条 open 条目逐一同名,即本仓 2026-10-08 自己 package 出的 outbox 包落回了入站点,物料按本地条目计一次);`feedback-20261013T124502Z.zip`(14 条,**孤儿** —— 未被 git 跟踪且 `git log --all -- feedback/<zip>` 零命中,删除后内容不可恢复)。三包在 `consume-log.md` 均无 `Bundles` 行,故非重投;最后一次 consume(2026-10-06)实测入站为空,故三者都是该轮之后新到达的物料,非中断续跑。

**为何 bundle 条目不进气泡围名单**:引擎 V-3 要求成员条目存在于本库索引,入站包条目不属于本库存储(它们由报告方项目记录),故 26 条 bundle 物料以**证据与复现**形态进入各问题的 `证据锚点`,并由 A4 逐条写入 backlog;`scope_entries` 只含本库 32 条。

核验由 **4 个并行只读子代理**按亲和度与体积分组执行(G1 team ×15 / G2 其余本地 ×17 / G3 2026-08 包 ×12 / G4 2026-10 包 ×14,每组 22–43 KB,禁止整库注入),全部对**框架源**取证、未以 `.specify/` 镜像为权威。4 次派发**均注入 `shared/guidelines/fast-fail.md` 的 owner 子句**并要求显式异常行 → 回报 **11 条 `ANOMALY`、0 条静默**;其中 5 条判为裁定、4 条判为纠正但越出只读范围、2 条属子代理自身副作用,全部上交本层并在下方元观察逐条处置,无一条被就地修平后隐瞒。

**same-author 条件**:本批 32 条全部由**既往会话**的编排者写下,非本会话;`shared/workflow/objective-analysis-gate.md` 的强制委派条件(同一作者在本次会话内产出又被同一作者分析)不成立,故委派是 A2 大批量纪律的选择而非该门的硬性要求 —— 如实标注,不夸称过了该门。

**覆盖核对(反空转哨兵)**:范围条目 **32** = 问题成员 **24** + Excluded **8**,**恰好覆盖一次**。8 条 Excluded 的原因逐条列于文末排除小节(3 条 `## Optimization Points` 为空、4 条全部点为 NOT-OURS、1 条全部点为 ALREADY-FIXED),无任何条目全部点既属 LIVE 又被排除于问题之外。

**分流分布合计 12**:`improve-skills` **3**(F-01、F-03、F-08)、`direct-fix` **3**(F-02、F-05、F-11)、`improve-docs` **2**(F-04、F-10)、`speckit-requirements` **3**(F-06、F-07、F-09)、`improve-team` **1**(F-12)。`improve-tools` / `improve-agent` / `acknowledge-only` 作为主分流各 **0**,仅以次生根或问题内已修部分出现。

## 元观察(不属任何单一条目,故不入 Findings;每条由 A4 单独分流并落 backlog 行)

- **M-1(本批最高优先,且是一条回归):probe 注册表与 `skills/internal/` 分层脱钩,20 个 internal 技能的 `## Feedback` 步在记录时必然失败。** `--action probes --reconcile` 本轮 **exit 2**,逐条报 `embed without probe object`,命中 20 个技能(`analyze-artifacts`、`clarify-artifact`、`create-checklist`、`create-plan`、`create-requirements`、`create-tasks`、`derive-architecture`、`implement-feature`、`manage-constitution`、`manage-features`、`manage-feedback`、`manage-goal`、`manage-history`、`manage-instructions`、`manage-todo`、`research-feature`、`review-sdd-process`、`run-agent`、`run-interview`、`sanitize-materials`,全部落在 `skills/internal/<name>/SKILL.md`)。`--validate` 仍 **exit 0**(72 internal + 0 external),即 schema 合法而集合不闭合。后果已核到代码:`scripts/python/feedback-utils.py:714-725` —— 注册表可用时 `resolve_probe` 返回 `None` 即 `raise FeedbackError`,故这 20 个技能每一次 `--action record` 都非零退出,**技能正文写了记录步、引擎拒绝记录**。这是 2026-10-11 `1adfa49a` 把命令逻辑下沉为 internal 技能时未同步登记对象所致。**并证伪上一轮的记载**:`introspection-20261006T140432Z` 的 M-3 记「注册表已零缺口,84 internal objects」;当前为 72 objects + 20 无主 embed,计数与缺口**同时移动**,旧记载只作为 dated record 保留。**次生**:唯一能看见该缺口的 `--reconcile` 不在任何命令/测试的阻断面内 —— `templates/commands/feedback.md` 的 inventory 步只带一行 `# embed audit` 注释(该缺口本身已复现于 backlog `:43` F-04,本轮第二次独立发现,优先级上调)。分流 `direct-fix`(补 20 个 Object + 把 `--reconcile` 接进阻断面),owner `shared/definitions/probe-definitions.md`、`scripts/python/feedback-utils.py`、`templates/commands/feedback.md`。
- **M-2:两顶帽子违规,且现成的绿守卫看不见它。** `git_fleet.py` 的两个修复(GBK 解码容错 `e86ba244`、`run_git` 捕获 `TimeoutExpired` `6e341d7b`)**只落运行镜像** `.specify/skills/git-workspace/scripts/git_fleet.py`;框架源 `skills/external/git-workspace/scripts/git_fleet.py:630-647` 两者皆无。编排者独立复现:`diff` 出该 hunk,`sync-mirrors.py --check` 现 **exit 2**(DRIFT),故下一次 `--write` 会静默回退这两个修复,而每个走 publish→install→refresh 的客户项目将重新踩「单个远端超时中断整轮 fleet」。根面即 AGENTS.md「Path-resolution trap」与 Two Hats 段所预告的形态。分流 `direct-fix`(把两 hunk 回灌源、再 `--write`),owner `skills/external/git-workspace/scripts/git_fleet.py`。
- **M-3:退役技能在镜像里留下 git 不可见、且 `--check` 也不报的空壳。** `.specify/skills/git-fleet/`、`.specify/skills/git-server-init/` 存在(源侧已无,`skills/external/` 仅余 `git-workspace`),内部只剩空 `scripts/` 目录;两目录 git 不可见,`sync-mirrors.py --check` 本轮仍报它们 `ok`,即**四技能 merge 的退役回收面在机器上是不可见的**。与 backlog `:47`、G3 报告的 `skills/external/` 残留同族。分流 `direct-fix` + 与 F-03 合并设计(见该行)。
- **M-4:`sanitize-utils.py` 对「已完结 spec」有两个互斥归档目的地。** 引擎内 `scripts/python/sanitize-utils.py:317`、`:338` 用 `.specify/specs/.archive/`,而 `:60`、`:1005-1016` 的 apply lane 迁往 `.specify/archive/`;`skills/internal/sanitize-materials/SKILL.md:157` 只记录后者,而 spec 编号扫描 `scripts/bash/create-new-requirements.sh:140-156` 与 `skills/internal/create-requirements/SKILL.md:45-47` 只读前者 ⇒ 经引擎归档的 spec 对「下一个编号」推导不可见,**编号撞车**。属**裁定**(哪个为权威),非纠正。分流 `speckit-requirements`,owner 同上四处。
- **M-5:thin-pointer 重构(`62bbaf7d`)留下三处失效 owner 指针。** `skills/internal/create-requirements/SKILL.md:17-19` 自称真源在 `templates/commands/requirements.md` § "Outline 1–8"、`skills/internal/clarify-artifact/SKILL.md:17-19` 自称在 `templates/commands/clarify.md` § "Phase 0",而两个模板都已不含这些小节;`templates/tasks-template.md:105` 把「每任务一行」规则指向 `.specify/templates/commands/tasks.md`,规则实际在 `skills/internal/create-tasks/SKILL.md:267`。属**裁定**(每处指针的正确目标是模板还是技能,是一个无工件记录的出处主张)。分流 `direct-fix`(裁定后),owner 三文件。
- **M-6:客户项目侧的框架级发现(bundle A/C,无本库条目承载,逐条落 backlog)。** (a) SDD 各阶段普遍缺「谁消费了这条被改动的共享声明」的枚举能力 —— `skills/internal/create-requirements/SKILL.md:97-100`(只检新标识符)、`skills/internal/clarify-artifact/SKILL.md:92` + `shared/constants/clarify-taxonomy.md:76-105`(逐条自洽、无跨答案一致性趟)、`skills/internal/analyze-artifacts/references/detection-and-severity.md:34-66`(7 趟全为 artifact-to-artifact,无仓外消费者趟)三处同根;(b) 文档引擎对非普通文件系统形态失明 —— `skills/external/create-docs/scripts/docs-utils.py:212` 链接校验纯 `exists()` 不识 submodule(未初始化 submodule 的活链接被判死,`:295` 的 `fix-links` 可据此删活链接)、`:224-244` 保留名扫描 `is_symlink` 零命中(而 `--allow-special` 已存在,故条目所称「设计上不可修」一半不成立)、`skills/external/create-pages/scripts/scaffold-hugo.py:240-241` mounts 只按目录计算 ⇒ **本仓活例**:`docs/git-workflow.md` 不在 `docs/hugo.toml` 生成的 mounts 里;(c) `skills/external/git-workspace/references/execute-commands.md:7-29` 无 submodule 壳健康探测、`references/troubleshooting.md:5-14` 无 `git stash push -u` 遇符号链接整体失败一行;(d) `skills/internal/create-team/references/summary-mapping.md:26,29` + `scripts/build-summary-input.py:1030` 仍无轻量 goal 级摘要档(空台账直接拒出摘要)—— **即 backlog `:27` F-E14 的第二次目击**;(e) `skills/internal/code-review/scripts/git-delta-review.sh:403-412,437-455` `report` 子命令 append-only 故门永不自我收敛、`:79-86` `--worktree` 跳过未跟踪文件;(f) `skills/internal/create-team/references/create-mode.md:27` 仍叫 agent「via `parse_goal`」读 goal,而 `scripts/python/goal-utils.py:1175-1242` 无该 CLI 动作 —— **backlog F-16 的姊妹**;(g) `skills/external/improve-docs/SKILL.md:55` 无「复核对其他文档的 staleness/quality 主张」一步(只复核被编辑文档自身的路径/旗标/计数/版本)。
- **M-7:`--action list` 的 `count` 仍是截断后计数(backlog `:47` M-1 未修,本轮再次咬到编排者)。** 编排者独立复现:`scripts/python/feedback-utils.py:857-858`(`matches = items if limit is None else items[:limit]` 之后 `return {"count": len(matches), …}`)与 `:2013`(`--limit` 默认 **5**)。本轮第一次 inventory 读得 `count 5`,真实 open 为 **32** —— 不复核即会对 5 条做自省并声称覆盖全量。命令模板 `templates/commands/feedback.md` 的 inventory 步与 A3 范围快照仍不带 `--limit 0`(2026-10-06 报告点名的 `(a)`/`(b)` 二选一裁定仍未裁定)。**跨三轮未动,按命令纪律本身即是一条 finding**。
- **M-8:执行副作用需处置。** G2 核验子代理为确认 C-12/C-23 判定跑了 `sanitize-utils.py --action collect`,造出 `.specify/memory/sanitize/findings.json`(**1 196 475 B**,目录 `.specify/memory/sanitize/` 本轮前不存在,文件被 `.gitignore:70` 覆盖)。该命令带写副作用,已在我派发的只读约束之外 ⇒ 属子代理越界,由编排者按 A5 收尾一并清除并在此披露,不作为 finding。

## Findings

### F-01: 声称先于证据、绿无法证伪 —— SDD 门禁与守卫两侧的「已通过/已覆盖/已判定」状态行都没有绑定到产生它的实际执行;同一根因跨 plan/tasks/implement/review/improve-skills 五个本库单元、并与 2026-08 入站包的四处主张跨批复现

- **根因**: 「可证伪性(红)」在本仓已有 owner(`shared/guidelines/fast-fail.md:51` 的两个配套技术 + 变异演练 + 反空真哨兵),但**对偶的「可满足性(绿)」义务不存在** —— 没有任何条款要求一条 GREEN 断言在变绿之前被真正跑过一次,也没有任何条款要求门禁填充前执行文档化的 test/build 入口;执行验证面 `skills/internal/create-plan/SKILL.md:258-291` 只覆盖制品生成之后。
- **证据锚点**: Phase 0 严格只读、无执行义务 —— `skills/internal/create-plan/SKILL.md:185-193`(执行职责在 `:258-291`)。Constitution Check 在 Phase 0 之前填充,仅「Re-check after Phase 1」,无 provisional 标记 —— `templates/plan-template.md:33,59`。「summarize after, not before」只进了技能正文(`skills/internal/create-plan/SKILL.md:119-125`,`62bbaf7d` 于 2026-10-12 入,晚于该条目),未成通用条款;`templates/plan-template.md:60` 的 post-design re-check 行仍无 run-then-write/PENDING 约束 ⇒ 条目的「已过时」一半不成立、「通用条款仍缺」一半成立。`validate-tasks.py:529-543` 的 green-path-divergence 提示给出两种补救而代码两者都不守(`:534` 相等即跳过、`blockedBy` 从不参与、不相交的 claim 集仍 WARN)。新守卫写断言前无 marker 选择规则(「当前零命中」),`docs/reference/history/00-cross-cutting-lessons.md:80-108` §十二 九成因不含此项,活证 `.specify/specs/054-agent-registration-wiring/notes/red-first-evidence.md:32`。SC 状态行只记 status/value/note、无义务复引该 SC 的 Measurement Source —— `templates/verification-log-template.md:57-65` vs Source 定义在 `templates/requirements-template.md:148-151`。`-m contract` 结构上漏掉 **30** 个无 marker 的测试文件(含 `tests/contract/test_fast_fail_discipline.py`、`test_confirmation_gates_sweep.py`、`test_trigger_engine.py`)⇒ 该 A/B 门对它们恒不可见。improve-skills 侧:`skills/external/improve-skills/references/loop-playbook.md:42-51` 在引擎只给项目级信号时不指名每目标证据来源(`scripts/python/evidence-utils.py:27,375-396` 的 lanes 本就是 project-level),**与 backlog `:25` 2026-09-11 行同源、第二次目击**;压测矩阵只落报告(`skills/external/create-skills/references/pressure-testing.md:69-71`)而反空真读取者是字面子串(`scripts/python/run-determination.py:534,539-558`)。跨批复现(bundle A 2026-08-07 四条目,现行源逐条仍成立):`/tmp/fb-consume.0lwJ/feedback-20260807T113350Z/` 的 `20260807T035918Z-speckit-plan`(Phase 0 不跑)、`041236Z-speckit-tasks`(环境探针无对照趟、既有测试枚举缺)、`052023Z-speckit-analyze`(ID 引用计数被当覆盖报)、`092520Z-speckit-review`(不复用 implement 已落盘的稳定证据位置)。
- **成员条目**: 20261008T121234Z-speckit-plan(部分成立)、20261008T124946Z-speckit-tasks(部分成立)、20261008T132002Z-speckit-implement(成立)、20261008T133457Z-speckit-review(成立)、20261008T133825Z-speckit-implement(成立)、20261008T135121Z-speckit-review(部分成立)、20261011T135147Z-skill-improve-skills(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 按**一个工作流**修,不做七处零敲。① 在 `fast-fail.md` § 两个配套技术 增补**对偶义务**(绿侧可满足性):一条 GREEN 断言 MUST 附「该检查曾在当前树上报过红,或刻意做坏的样本已证其可变红」,与 backlog `:44` F-05④ 的「绿证人」同源,两处措辞 MUST **互指**而非各写一份。② `create-plan` 的 Phase 0 增「执行义务前置」一步:Constitution Check 填充前 MUST 跑文档化 test/build 入口并记录 exit,Phase 0 的 refutation 主张 MUST 有写回 requirements 的落点(`:188` 现在只说「confirm or refute」而无处写回)。③ `templates/plan-template.md:60` 的 re-check 行补 run-then-write/PENDING 约束,使「先总结后验证」从技能正文升为模板条款。④ `validate-tasks.py:529-543`:提示与实现二选一 —— 要么实现所述两种补救,要么把提示收窄到代码真正做的事。⑤ `verification-log-template.md` 的 SC 行增 `Measurement Source` 复引字段,并在 `implement-feature/SKILL.md` 的对应步要求逐字复引。⑥ marker 选择规则与 `-m contract` 的 30 个无 marker 文件:前者补进 `00-cross-cutting-lessons.md` §十二(附反例),后者属**逐文件裁定**、按 M 级单独走 `speckit-requirements`(见该行),不在本问题内偷改。⑦ improve-skills 侧补「每目标证据来源」档:引擎只给 project-level 信号时,MUST 显式声明该目标无 lane 证据并按 `loop-playbook.md:42-51` 的降级形态取证。**次生根(improve-docs)**:`templates/plan-template.md:80,82` 的 research.md 独立/内联阈值仍是行数(~50 行),与「按内容而非度量」的既有口径冲突。**acknowledge-only**:三条 token 自评点(propagation surface `none`)。

- **建议处置**: 20261008T121234Z-speckit-plan:processed, 20261008T124946Z-speckit-tasks:processed, 20261008T132002Z-speckit-implement:processed, 20261008T133457Z-speckit-review:processed, 20261008T133825Z-speckit-implement:processed, 20261008T135121Z-speckit-review:processed, 20261011T135147Z-skill-improve-skills:processed

### F-02: 记录面与派生面静默吞错并降级产出 —— 解析失败不报、输入形态不校验,产物带着错误身份继续下游流转

- **根因**: 「解析失败」与「解析得到空」在代码里不可区分,且记录器的输入形态无任何校验 ⇒ 缺陷以降级产出形态存活,不以任何退出码形态现身。
- **证据锚点**: `skills/internal/create-team/scripts/build-summary-input.py:103-107` 捕获 `ParserError` 后 `return {}`,身份在 `:150-155` 被推断、roster 在 `:694` 落「未声明」;两个活输入 —— `.specify/teams/command-logic-as-classified-skills/team.md`(flow-map 行含「空格+冒号」)、`.specify/teams/viz-skill-arena/team.md:4`。记录器侧 `scripts/python/feedback-utils.py:228-236` 的 `compose_entry` 把调用方字符串逐字加前缀、无形态校验,后果活在本库条目 `20261012T123030Z-skill-summarize-project` 自身:`- ## Feedback` 与 `- marker: correctness` 被当成优化点写进了 `## Optimization Points`(17 条中 1 条,该条点数因此虚增 2)。
- **成员条目**: 20261012T123030Z-skill-summarize-project(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① `split_frontmatter` 解析失败 MUST 抛(或返回 `(None, error)` 并在调用点计入 degraded 集),使「frontmatter 语法不可解析」与「无 frontmatter」在产物与报告两侧可区分;`team.md` 的 `## ` 前行 MUST 在 `create-mode.md:74` 的 schema 里给出引用写法约定(字面量标题禁入正文,与 backlog `:42` F-03④ 同源)。② `compose_entry` 对每条 point 做最小形态校验(拒以 `## ` 开头、拒以已知元数据键 `marker:`/`probe:` 开头),把本次的「条目自污」变成一次 exit 2。③ 修 `20261012T123030Z` 的两条伪点须走 dispose/reason 记录,不手改存储文件(存储只经引擎写)。**次生根(improve-docs)**:`.specify/teams/*/team.md` 是消费方而 `skills/internal/create-team/references/create-mode.md:128` 承诺的 team.md 校验器仍不存在(backlog `:42` F-03 第三次目击)。

- **建议处置**: 20261012T123030Z-skill-summarize-project:processed

### F-03: 退役与回收面失明 —— 删除不传播、忽略清单不全、被并技能在镜像留空壳,四组同根:「加性合并,无回收」

- **根因**: 镜像同步与退役流程都只做加性写;没有任何一步枚举「已被删除/并入的名字在消费面上还剩哪些引用」,也没有任何检查要求「退役名在 git 与 `--check` 两侧同时不可见」这件事本身是可发现的。
- **证据锚点**: `scripts/python/sync-mirrors.py:40,84-85,207-212` 无删除传播路径;`:91` 的 `IGNORE_NAMES` 不含 `*.orig`/`*.rej`。活例见 M-3(`.specify/skills/git-fleet/`、`git-server-init/` 只剩空 `scripts/`,`--check` 仍报 ok)。退役侧 `skills/external/merge-skills/references/decommission-and-wiring.md:22-52`(6 个去接线界面,无一行命名 goal/criterion 类治理工件)、`:65-77`(不要求在删名之前 grep `tests/` 里钉死的 census/字面量,活 census:`tests/contract/test_skill_layer_visibility_guards.py:25-27,86`、`test_shared_reference_rewrite.py:75`)、`:32-43`(两个改名危险未具名:词边界改写撞进 team slug、`skills:` 列表需去重;活残留 `.specify/teams/draw-plantuml-optimizer/`)。
- **成员条目**: 20261009T064957Z-speckit-team(成立)、20261008T090856Z-speckit-team(成立)、20261012T074736Z-skill-merge-skills(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: ① `sync-mirrors.py` 增删除传播(源侧不存在 ⇒ 镜像侧回收),并把 `*.orig`/`*.rej`/`*.bak` 纳入 `IGNORE_NAMES`;新增一条 `--check` 断言:镜像里任何「源侧无对应目录」的非镜像专有目录 MUST 报 DRIFT(否则 M-3 那类空壳永远隐形)。② `decommission-and-wiring.md` 的去接线界面清单补两类:治理工件(goal/criteria/backlog 行的 owner 列)与测试钉死字面量(`grep -rn` 退役 slug 于 `tests/`,先取 census 再删),并把两个改名危险写成具名条款。③ **次生根(speckit-requirements)**:删除传播是幂等/收敛语义变更、波及所有消费方,宜按一条需求走(与 M-3、与 backlog `:30` 「cleanup 对 git 跟踪条目的感知」同族);本问题只做镜像侧可安全直修的一半。④ **acknowledge-only**:`20261012T074736Z` 的 reverse-probe「非强制」一半被证伪(`skills/external/merge-skills/SKILL.md:84` + `references/coverage-verification.md:37-49` 已写「Both directions must reach exit 0 before Phase 7」),成立的一半是「每次 merge 需自有 allow 文件」的审计面仍缺。

- **建议处置**: 20261009T064957Z-speckit-team:processed, 20261008T090856Z-speckit-team:processed, 20261012T074736Z-skill-merge-skills:processed

### F-04: 并发会话下的提交与暂存面纪律缺失 —— 制品提交步只规范「按路径 add」,未规范 path-limited commit 与 staged-ownership 复核;跨流暂存把兄弟会话的行一起提交

- **根因**: `shared/workflow/artifact-commit-step.md:33-38` 规定 staging-by-path 与 deletion audit,未规定 commit 本身带路径限定、也未规定提交前复核 staged 集合是否只含本会话的产物;`docs/reference/history/00-cross-cutting-lessons.md` 无「共享文件提交前取外部内容检查」一行。
- **证据锚点**: `shared/workflow/artifact-commit-step.md:33-38`(无 path-limited commit / staged-ownership 义务);`docs/reference/history/00-cross-cutting-lessons.md:38-40` §五 只覆盖 `cp` 别名静默失败,**未泛化到 `rm`/删除或 python `os.remove`**(故该条「已有教训」一半成立、一半过窄);活证据:本轮 `20261008T073541Z` 记录的 S5 抓出 `70721de7` 夹带并行会话导览行,同族已在本库出现 ≥3 次。
- **成员条目**: 20261008T093319Z-speckit-clarify(成立)、20261008T073541Z-speckit-team(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: ① `artifact-commit-step.md` 补两条:提交 MUST 路径限定(`git commit -- <paths>`),且 staged 集合 MUST 在提交前逐路径核对归属;与既有 `comm -13` 基线纪律并置而非另立。② `00-cross-cutting-lessons.md` 增一行「共享文件提交前对外部内容做检查」,并把 §五 的别名陷阱从 `cp` 泛化为「任何被 alias 遮蔽的删除类命令 + `os.remove`」。③ **次生根(direct-fix)**:`skills/internal/manage-instructions/SKILL.md:389-392` 的 Action 7 点名的可删备份其实 `.specify/instructions.md-2026-07-11` 仍被 `git ls-files` 跟踪(尽管 `.gitignore:56`),该备份属本问题的归属复核活例。

- **建议处置**: 20261008T093319Z-speckit-clarify:processed, 20261008T073541Z-speckit-team:processed

### F-05: goal 引擎读写面缺口 —— 判据整档替换语义无告警、`boundary` 无可达动作,且文档指认的引擎函数无 CLI 入口(与 backlog `:36` F-16 同族第三次目击)

- **根因**: 引擎的动作名册与散文主张各自演化:写入路径以整档替换语义落地却不告知调用方,读取路径只在 Python 层存在而 CLI 名册不含,文档遂写出一个跑不通的调用式。
- **证据锚点**: `scripts/python/goal-utils.py:665-680`(`set_criteria` 整档替换,docstring `:29` 亦然)且 `skills/internal/manage-goal/SKILL.md:89,99` 无「一次传多条判据会替换全集」的告警;`goal-utils.py:1175-1252` 的 action 名册无 `boundary` 读写动作(boundary 仅 `create` 时置,`:1182`),该点在 `20261009T034653Z` 与 `20261006T170532Z` 两条条目独立复现 ⇒ 复发升优先级;`skills/internal/create-team/references/create-mode.md:27` 仍指示「via `parse_goal`」读 goal,而 `goal-utils.py:1175-1242` 的 subparsers 无该动作(`skills/internal/manage-goal/SKILL.md:80` 自己记着「no `view` action」)⇒ 与 backlog `:36` F-16 同根。
- **成员条目**: 20261009T034653Z-speckit-team(成立)、20261009T081108Z-speckit-team(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① `criteria` 写入路径在替换非空判据集时 MUST 打印被替换条数并需显式旗标(或在 `manage-goal/SKILL.md` 与 `goal-utils.py` 的 `--help` 双处明写整档语义)。② 补 `boundary` 的 read/modify 动作,接进 `templates/commands/goal.md`。③ 立一条通用规则「文档与技能正文 MUST NOT 指认无 CLI 入口的引擎函数」,把 `create-mode.md:27` 改指真实动作;该规则与 M-6(f) 的 `parse_goal` 实例、backlog F-16 的 `run-checks` 实例同根,**一处立规、两处回改**。④ **次生根(improve-docs)**:`20261009T081108Z` 的第二点(新渲染席位在同会话内不可派发)不属 goal 面,归入 F-06 的注册链缺口,已在那行的方案内标注。

- **建议处置**: 20261009T034653Z-speckit-team:processed, 20261009T081108Z-speckit-team:processed

### F-06: agent 定义 → 宿主注册面三处断裂,且承载该裁定的两行 backlog 在其裁定所依赖的 spec 合并之后仍记 `open`

- **根因**: 两层缺口叠在一起 —— 机制层:定义/渲染/注册三面之间无安装与触发步骤(可达性、触发面、模板教退役模型);记账层:`backlog.md` 的 `carried-by-spec-*` 前进指针约定**已有先例却从未被应用**,于是行不随 spec 关闭。
- **证据锚点**: 机制层三断点(与 backlog `:49` 完全同根,该行的三处断点本轮逐处复核仍成立):`src/specify_cli/__init__.py:310-322` 只读 `.specify/agents/{templates,instances}`、`skills/create-team/templates/agents/` 与 capacity 类无安装步骤、`render_agents_for_tool`(`:615`)只被 CLI 内 `:2283` 调用;`templates/commands/agents.md` 的退役 symlink 说法现由 `skills/internal/run-agent/SKILL.md` 的 Delegation 表承载真实文件模型(该半已修)。版本地板半:`specify render-agents` 于 `src/specify_cli/__init__.py:3267` 由 `3e673e16`(2026-10-08)加入,而 `pyproject.toml:3` 仍 `0.0.22`,该子命令却被教进 `skills/internal/create-team/SKILL.md:34`、`references/create-mode.md:18`、`skills/external/improve-team/SKILL.md:33`、`docs/reference/cli/supported-agent-tools.md:37` ⇒ 每个仍装 0.0.22 的客户项目照文档跑不存在的命令。记账半:`.specify/memory/feedback/backlog.md:49,50` 两行(2026-10-07,正是裁定 (b) 的来源)仍 `open`,而 spec 054 已实现合并并反向引用它们(`.specify/specs/054-agent-registration-wiring/requirements.md:6,17`);前进指针约定在 `backlog.md:32-36` 以 `carried-by-spec-053` 形态已存在 ⇒ 约定有、执行缺、A4 无预检(`skills/internal/manage-feedback/references/path-a-digest.md` § A4 不要求在写新行前查既有行)。
- **成员条目**: 20261006T170532Z-speckit-team(成立)、20261008T061227Z-speckit-instructions(成立)、20261008T073805Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: ① 三处断点按 backlog `:49` 已列的 (a)/(b)/(c) 三选一裁定推进,本轮**不重复裁定**(用户在该行已裁 (b)、spec 054 已实现 (b)),而是做记账关闭:把 `:49`/`:50` 改 `carried-by-spec-054` + Closed-by 指向 `.specify/specs/054-agent-registration-wiring/`,再按 owner 文件实测复核该行是否可关。② `path-a-digest.md` § A4 增一条预检:写新行之前 MUST 先对既有行做「同一 root cause 扫描」,命中则更新状态而不是新增行(本次两条同根主张(`:43` F-04 与 F-11)即预检缺位的产物)。③ 版本地板:要么把 `pyproject.toml:3` 随 `render-agents` 一起 bump 并重新发布,要么在五处教学点明写「需 ≥ 下一发布版本,当前 0.0.22 无此子命令」—— 二选一属**裁定**(发布动作不由本消化授权)。④ **次生根(improve-docs)**:`20261009T081108Z` 的「同会话新渲染席位不可派发,无任何流程交代」MUST 在同一处教学里补一行(渲染后需新会话生效),owner `skills/internal/create-team/references/create-mode.md:18,130`。

- **建议处置**: 20261006T170532Z-speckit-team:processed, 20261008T061227Z-speckit-instructions:processed, 20261008T073805Z-speckit-requirements:processed

### F-07: `/speckit.team` run 预览不诚实 —— 五项引擎检查只回答「可以开始吗」,从不回答「一共多少步、已完成多少、跨团队前置是谁」

- **根因**: 预览的判据集被定义为放行门而非进度视图;`blocked` 是唯一的停止字段,于是「进度分母」与「跨团队前置」两类事实无承载形态。
- **证据锚点**: `templates/commands/team.md:76-79`(五项 run-checks,无 k-of-N)/`:76`(前置只在本团队内);`.specify/teams/command-logic-as-classified-skills/team.md:204,77,264`(跨团队前置只以散文存在,`blockedBy` 只指本团队阶段)。
- **成员条目**: 20261012T081732Z-speckit-team(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: ① 预览输出增批次分母(总阶段数 / 已完成 / 剩余,程序派生而非 LLM 估读)。② 给跨团队阶段前置一个声明形态(team.md schema 增一字段,run-checks 增一项判定),否则「等谁」永远靠读散文。③ 与 backlog `:41` F-02 的 engine-verdict-vs-agent-side-gate 缺口同族:`run-checks` 的 `blocked:false` 不等于可派发,该行已记同一事实,本行只做增量。**次生根(improve-team)**:一行 territory/预览裁定无轻量入口,路由全归带强制证据步的 `improve-team`(backlog `:41` 已记,不另立行)。

- **建议处置**: 20261012T081732Z-speckit-team:processed

### F-08: 双树读取无纪律 —— 团队 run 同时消费框架源与运行镜像/渲染副本,却无规则要求引用权威面,也无规则防止同一命令正文被读两遍

- **根因**: 两顶帽子规则(Constitution XI、AGENTS.md Two Hats)管的是**编辑归属**,未管**读取与引用归属**;全仓 grep 无「行引用 MUST 指向权威源而非渲染副本」一行。
- **证据锚点**: `skills/internal/create-team/references/execution-guide.md:36-59`(无单次读取权威面的交代,命令正文被渲染副本 + canonical 双读)、`templates/commands/team.md`、`skills/create-team/references/patterns.md`、`skills/internal/create-team/references/create-mode.md` 四处对「引用哪一棵树」零命中。该缺陷已被本轮实证两次:M-2(修复落镜像不落源)与 `tests/contract/test_scripts_distribution_parity.py:74` 因 DRIFT 而红。
- **成员条目**: 20261009T032137Z-speckit-team(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: ① 在 `.specify/shared/definitions/dogfooding-definitions.md` § 2.1(两顶帽子真源)增「读取面」一段:任何 `path:line` 引用 MUST 指向框架源;产物与报告不得引用渲染副本。② `execution-guide.md` 增「命令正文只从 canonical 读一次」的落点,附 token 理由。③ 与 M-2 同源:读取纪律缺失与写入纪律违规是同一枚币的两面,两处措辞 MUST 互指 owner。

- **建议处置**: 20261009T032137Z-speckit-team:processed

### F-09: 新命令/新技能的注册链无机检 —— 分类表、闭合计数测试、docs-step 清单、probe 名册四处必须同批改,却无任何落地约束或程序检查覆盖它

- **根因**: 注册面是四份彼此独立的清单,靠人记住;而唯一能发现不闭合的 `--reconcile` 不在阻断面内(见 M-1)。
- **证据锚点**: 活证即 M-1(20 个 embed 无 probe 对象、`--validate` 仍 exit 0、`--reconcile` exit 2 而无门禁);`templates/commands/team.md` 的落地步与 `skills/internal/create-team/references/create-mode.md` 的落盘校验均不含「分类表 + 计数测试 + probe 名册」三项同批核对;`shared/workflow/feedback-step.md` 的 simple/complex 枚举与 `templates/commands/*.md` 的 embed 集合之间无程序等式。
- **成员条目**: 20261008T033549Z-speckit-team(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: ① 立一条需求:一个确定性校验器(暂名 `validate-registration-chain.py`)枚举 embed 集合、probe 名册、命令分类表与计数测试断言,输出差集并不等即红;接进 `tests/contract/` 与 `/speckit.instructions` 的退出门。② 与 M-1 的直修半合并:M-1 先补 20 个 Object 让注册表闭合,本行负责让「下次不再静默脱钩」成为机器义务。③ **acknowledge-only**:`20261008T033549Z` 的报告↔摘要形状点(契约内联 `· **Outcome**` 与 `build-summary-input.py:257,266,303` 的行锚正则不兼容;活报告 `…/runs/20261012T115331Z-report.md:9,22` 两者皆无)归 F-12。

- **建议处置**: 20261008T033549Z-speckit-team:processed

### F-10: 团队载荷与中间制品无纪律 —— 逐轮截断无 skeleton-first 载荷约定、中间制品作为唯一下游设计源时无升格/指纹档、`Summary:` 行的写入时机未标注

- **根因**: `create-team` 的载荷与制品生命周期只规定终态形状,未规定「被逐轮截断时如何组织载荷」与「一份只活在 `.work/` 的中间件如何成为可交接的权威」。
- **证据锚点**: `skills/internal/create-team/references/patterns.md:204`(计数纪律已有、载荷组织档无)、`skills/internal/create-team/references/create-mode.md:110`(truncation recovery 存在 ⇒ 条目「无处置」一半不成立);`skills/internal/create-team/references/execution-guide.md:9-23` 与 `skills/internal/create-team/SKILL.md:167`(无「唯一设计源的中间制品 MUST 升格/指纹」一档);`skills/internal/create-team/references/summary-mapping.md:171`(部分覆盖 who/when,未标 backfill ⇒ 条目「无标注」一半成立)。
- **成员条目**: 20261009T181710Z-speckit-team(部分成立)、20261006T150118Z-speckit-team(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: ① `patterns.md` 增载荷组织档:跨轮载荷 MUST skeleton-first(先骨架后细节),使截断只损失末节。② `execution-guide.md` 增中间制品升格规则:某 `.work/` 文件若为下游唯一设计源,MUST 落进可交接路径并指纹化。③ `summary-mapping.md:171` 补 backfill 时机标注。④ **次生根(improve-team)**:与 F-07 同一轻量入口缺口。⑤ **acknowledge-only**:`20261006T150118Z` 的「委派无本地度量」一半被证伪(`shared/workflow/objective-analysis-gate.md:23` 已带 2026-09-18 的 dated measurement)。

- **建议处置**: 20261009T181710Z-speckit-team:processed, 20261006T150118Z-speckit-team:processed

### F-11: 反馈存储自身的记账与可发现性缺口 —— package/mark-submitted 不留 consume-log 行、路径文档的审计面主张已过期、报告 schema 无骨架只能靠 exit 2 反推

- **根因**: 引擎把「记账」只实现为本地元数据翻转,没有任何一步为**上送侧**留下批次审计;而报告 schema 的权威面在引擎校验里,既无骨架模板也无指针形态约定。
- **证据锚点**: `scripts/python/feedback-utils.py` 内 `write_package`(MANIFEST `:1053-1088`、SUBMISSION-NOTES `:1118-1124`)与 `mark_submitted`(`:900-936`)对 `consume-log.md` **零写入**;`skills/internal/manage-feedback/references/path-b-and-probe.md:6` 声称「`cleanup-log.md` plus MANIFEST 仍是审计面」,而 `cleanup-log.md` 在框架源与镜像两侧均不存在、被引的 outbox zip(`.specify/memory/feedback/packages/`)目录实测为空 ⇒ 该句为不可达引用。schema 侧:无 `templates/*introspection*` 骨架,三约束只写在 `docs/reference/skills/feedback.md:155-169`;`20261006T143136Z` 所引引擎行号已漂移(`_MEMBER_RE` 现 `:462` 非 `:313`;`无` 哨兵现 `:599` 非 `:450`)⇒ 该点「缺骨架」成立、「无文档」一半不成立。**与 backlog `:43` F-04 完全同根,为该行的第二次目击。**
- **成员条目**: 20261006T143136Z-speckit-feedback(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① 修 `path-b-and-probe.md:6`:要么由 `mark-submitted` 真写一行审计记录,要么把该句改为如实描述(MANIFEST + `submitted-at.json` 才是审计面)。② 落一份 `templates/introspection-report-template.md` 骨架(七字段 + 发现区 + 排除区 + 成员/建议处置行形),使 A3  drafting 不必靠 exit 2 反推 —— 这条同时关闭 backlog `:43` 的 schema 半。③ 两处指针行 MUST 各配一条契约测试钉住(先例 `tests/contract/test_feedback_step_reference_form.py`),按 ask-record-repeat.md 三房面补齐。

- **建议处置**: 20261006T143136Z-speckit-feedback:processed

### F-12: `/speckit.instructions` 生成/保留面的三处未闭合 —— 点名的可删备份仍被 git 跟踪、keep-set 钉住已废标题、Documentation Map 的数字事实仍手工再生

- **根因**: `manage-instructions` 的 Action 3/6/7 各自规定了保留与比较策略,但策略的字面量目标(标题名、备份文件名、小节计数)没有从生成器派生,于是每加一次 supersede 名单就多一处会腐烂的副本。
- **证据锚点**: Action 7 点名的 `.specify/instructions.md-2026-07-11` 仍在 `git ls-files` 内(尽管 `.gitignore:56`)—— `skills/internal/manage-instructions/SKILL.md:389-392`;keep-set 规则(SAME `:224-227`)仍钉住 `## Resource Registry` 等已被 `scripts/bash/generate-instructions.sh:243` 的 `SUPERSEDED_BY` 与 Action 5 `:330-341` 判废的标题(活备份剩 1 个,其中 `## Resource Registry` 命中 1、活文件命中 0),而该改动还被 `tests/contract/test_instructions_size_budget.py:485-500` 钉了字面量;Map 数字事实仍手工 diff —— `skills/internal/manage-instructions/SKILL.md:270-272` vs 生成器唯一机器表 `scripts/bash/generate-instructions.sh:82-135`(只有尺寸/占位旗标)。跨批复现:bundle A 的 `20260730T082133Z-speckit-instructions`(Map 数字事实无 facts manifest)与 `20260801T145445Z-speckit-instructions`(Action 5 存在性检查与 partial-update「只碰被要求项」边界仍未裁定;`SKILL.md:269-270` 的「修移动过的路径」vs `:106` + `:350-351`)现行源逐条仍成立 ⇒ **与 backlog `:39`、`:46` F-07、`:52` 三行同一接缝**。
- **成员条目**: 20261006T172913Z-speckit-instructions(成立)
- **分流决定**: local-sink(improve-team)
- **优化方案**: ① Action 7 的备份处置改为从 `git ls-files` 派生可删集(而非点名字面量),并把仍被跟踪的活文件按 F-04 的归属复核处理。② keep-set 与 `SUPERSEDED_BY` 合一:同一份名单两侧各写一遍即漂移源;改后 MUST 同步 `test_instructions_size_budget.py:485-500` 的钉死字面量。③ Map 的数字事实(尺寸、行数、计数)由生成器输出 facts manifest,技能只读不推 —— 此为本行与 bundle A 两条主张的共同解,按一条改进推进而非三处零修。④ **为何落 improve-team 而非 improve-skills**:本轮 `improve-skills` 已分配 3 个问题且本行的可执行半(名单合一 + facts manifest)属工具化改造,与 F-04 的 lessons 面同批;若用户改判,覆盖方向应为 `local-sink(improve-skills)`。**次生根(improve-docs)**:`.specify/instructions.md` 的 Documentation Map 表内加行对既有项目永不生效(backlog `:52` 已裁定,该行仍 `open`,本行只作交叉引用不重复裁定)。

- **建议处置**: 20261006T172913Z-speckit-instructions:processed

## Excluded

- 20261012T115637Z-speckit-team — 唯一一条点为 NOT-OURS(编排者读整份 team.md 的 harness 行为,无框架制品可改);其余全部为运行观察且自评精确度被子代理证伪两处
- 20261011T144800Z-speckit-team — `## Optimization Points` 为空(clean run,无点)
- 20261011T130143Z-speckit-team — `## Optimization Points` 为空(clean run,无点)
- 20261011T021048Z-speckit-team — 唯一一条点为 NOT-OURS(`/tmp/specify-skills-*` 残留与 4 个 root-owned 目录属瞬态环境, remedies 已在 `sync-mirrors.py:232-234` 记录)
- 20261012T140155Z-speckit-sanitize — 全部点 ALREADY-FIXED(C-12/C-22 同目标双报边界已实现、已进契约并有负例:`scripts/python/sanitize-utils.py:670-677`、`.specify/specs/045-sanitize-command/contracts/sanitize-detection-rules.md:36,44`、`tests/unit/test_sanitize_checks_migration.py:73,97`)
- 20261011T025327Z-speckit-goal — `## Optimization Points` 为空(clean run,无点)
- 20261008T140013Z-speckit-feedback — 全部点 NOT-OURS(054↔055 的 `index.json` modify/delete 合并已完成、该文件已退役;残余的「git merge-tree 盲区无教训行」另记于 M 级,不构成本条目的可改制品)
