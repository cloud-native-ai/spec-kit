# Contract: Skill Structure（sdd-loop-driver 结构契约）

> 本契约钉死交付物 `skills/external/sdd-loop-driver/` 的结构与内容义务。条款 C-n 一条一断言，逐条映射到 `tests/contract/test_sdd_loop_driver_skill.py` 的一个测试函数（先例 `test_run_skills_wiring.py` 形态）；条款编号按**交付顺序**排列（与 tasks.md 相位序一致，[green:] 认领沿升序进行）。字符串引用 `[[STR-nnn]]` 在本文件 § Shared Strings 解析。B-n 为行为类条款（agent 执行期行为，不进测试钉死，显式标注）。

## Shared Strings

| String ID | Value (verbatim) | 消费条款 |
|-----------|------------------|----------|
| STR-001 | `-DONE` | C-5 |
| STR-002 | `requirements → clarify → plan → tasks → checklist → analyze → implement → review` | C-4, C-5 |
| STR-003 | `sdd-loop-driver` | C-1, C-2 |

## Artifact-class Clauses（C-1…C-13，编号 = 交付顺序）

- **C-1 frontmatter 四字段**: `SKILL.md` frontmatter 恰含 `name: sdd-loop-driver`（== [[STR-003]]）、非空 `description`（含触发词「使用SDD开发模式」「无人值守」）、`skill_id: "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"`、`classification: external`；无其余 frontmatter 字段。
- **C-2 分类张力注解**: `SKILL.md` frontmatter 之后的第一段正文为注解行，声明「分类依依赖轴判定为 external；内容编排 spec-kit SDD 流程的语义耦合在此显式声明」（clarify Q4 消解义务）。
- **C-3 SKILL.md 章节集**: `SKILL.md` 的 H2 章节集合恰为：`## What This Skill Does`、`## When to Load`、`## The Loop (U0–U6)`、`## Hard Requirements`、`## Discipline Defaults`、`## References`（路由到 references/ 两文件）、`## Boundary`，以及编译生成的 `## Wrap-up`（AUTO-GENERATED，probe-registry 驱动、含 Feedback 嵌入面——implement 期发现补充）。章节内为摘要+路由形态，命令细节不进 SKILL.md。
- **C-4 dispatch-recipes 内联五机制**: `references/dispatch-recipes.md` 存在且内联五大执行机制的命令形态——断点探测（`git branch --show-current` / `git log --oneline -3` / `ls .specify/specs/`）、heredoc 阶段提示词写入、runner 模板（`-p "$(cat ...)"`）与 sed 派生、后台执行 + 日志轮询（`su -` 执行 + `tail` 轮询 + 一线一连接）且**脱离模式为缺省**（用户 2026-10-15 运行中裁定：远端 `nohup`/`setsid` 脱离形态自跑 + 定时间隔检查，连接断开不中断子代理）、收尾纪律（合并回 main + 逐线汇总）。
- **C-5 阶段链与哨兵字面量内联**: 阶段链 [[STR-002]] 与哨兵约定（大写阶段名 + [[STR-001]]，如 PLAN-DONE）以字面量内联于 `references/dispatch-recipes.md`；**全文不出现 `MERGE-DONE`**（clarify Q2 裁决：合并完成 = git 状态判定，判据文本：特性分支提交已包含于集成分支且无未合并/冲突残留）。（2026-10-17 修订：STR-002 六阶段 → 八阶段，纳入 checklist/analyze 质量门——用户需求：无人值守循环必经全部质量门；门判据与一轮有界回环规则见 dispatch-recipes.md Recipe 4 质量门编排节。）
- **C-6 观测要求操作规则内联**: `references/dispatch-recipes.md` 内联 External Dispatch Visibility Contract 的操作规则（禁止 `qodercli -p ... > log 2>&1 &` 式缓冲至退出派发；观测点：流式/日志增长/liveness/label 溯源）及其到 ssh + su 远端形态的映射说明；对契约真源仅作「撰写底稿」注解。
- **C-7 G5 纪律行逐字内联**: `references/stage-prompts.md` 含 G5 默认纪律的执行要求段：直接执行不要确认；访谈式问题自行裁决并记录假设；只提交本特性产物；既有脏文件不提交不还原；不要 push（除非明确授权）。
- **C-8 派发注入义务内联**: `references/dispatch-recipes.md` 或 `references/stage-prompts.md` 内联子代理派发注入义务的操作文本——每次阶段派发的提示词骨架要求子代理**最后一行输出完成哨兵或显式异常行**（二者皆无 = 卡死信号，进 U5）；注入义务的对齐真源以注解行引用（宪法 XVI / `.specify/shared/guidelines/fast-fail.md` § 子代理派发注入——执行侧不解析框架路径，操作文本内联）。
- **C-9 卡死处置操作要点内联**: 上送件四要素与「MUST NOT 静默等待 / MUST NOT 静默修平异常后继续」以内联文本存在于 `references/stage-prompts.md`（执行侧不解析框架文档，FR-018）；对 052 的对齐以注解行引用其名。
- **C-10 stage-prompts 全构成段齐备**: `references/stage-prompts.md` 含全部构成段——三段骨架全文（背景与权威文档 / 执行要求 / 完成尾标与回传契约）、独立校验程序（尾标必要 + 产物核验 + 纪律抽查；校验者≠执行者）、已验证变体（本地简报先行 / 构建固化分线）、并发隔离与窄读法授权、卡死处置与状态脊程序（先写状态后派发；U2/U4/U5 转移点）——任一构成段缺失即本条不绿。
- **C-11 自包含断言**: SKILL.md 与 references/ 全文不构成对框架路径的运行时必读——对 `.specify/...` 的每次出现都处于「撰写底稿/背景注解」语境（以「底稿」「背景」「先例」邻接词判定），无「MUST 读 / 必须先读 <框架路径>」形态的运行时义务句。
- **C-12 镜像一致**: `.specify/skills/sdd-loop-driver/` 下 SKILL.md 与 references/*.md 与框架源逐字节一致（sync-mirrors 投影，禁手改）。
- **C-13 external 名册与目录**: `skills/external/` 存在 `sdd-loop-driver/` 目录（SKILL.md + references/）；`tests/contract/test_run_skills_wiring.py` 的 `BASELINE_EXTERNAL` 名册含 `sdd-loop-driver`（roster↔目录集合断言随之成立）。
- **C-14 前置检查族内联（2026-10-15 运行后扩展，FR-026）**: `references/dispatch-recipes.md` 存在「前置检查（Preflight）」章节且位于断点探测配方之前，内联五检查族的命令形态——① SSH 连通性（`ConnectTimeout` 限时；标注本地拓扑跳过）、② 非 root 运行用户存在性（`id <run-user>` 且 uid ≠ 0）、③ 子代理 CLI 可用性与版本（`--version`）、④ 大语言模型配置核验（模型 + context size + effort，形态因 CLI 而异）、⑤ spec-kit 框架可用性（`.specify/` 安装/初始化/必要结构/版本 provenance）；并内联「不确定即上送用户补充」程序与「结论写入线状态脊前置检查段」程序。注：本文件与 distribution-and-docs.md 的 C 编号各自文件内唯一（条款语法真源 §1），引用按文件限定。

## Behavior-class Clauses（B-1…B-4，不进测试钉死）

- **B-1 入口语义**: 宿主 agent 加载本 skill 后，对一遍性入口（只声明目标/起点/终态文档）执行 U1 断点探测起步，未声明阶段时禁止要求用户补充阶段信息（G6）。
- **B-2 自迭代语义**: U4 校验通过后立即派发下一阶段（FR-012），全程不产生等待用户「继续」的停顿点；用户中途插入指令时当前阶段完成后尊重新指令（循环可中断可改道，规格 Edge Case 10）。
- **B-3 并行隔离语义**: 多线并行时每线独立连接与状态脊；并发隔离声明与窄读法授权按规格 FR-021 执行。
- **B-4 目标项目侧依赖**: 仅当阶段命令需要在目标项目执行 /speckit.* 时才要求目标项目具备 `.specify/`；目标项目无 `.specify/` 时按规格 Edge Case 2 报告停线，不自动初始化。

## Mapping

| FR | 条款 |
|----|------|
| FR-001 | C-1, C-11, C-12 |
| FR-002 | C-3, C-4, C-10 |
| FR-005 | C-4 |
| FR-007/FR-008 | C-4, C-7, C-8, C-10 |
| FR-009 | C-5 |
| FR-010/FR-011 | C-4, C-6 |
| FR-012 | B-2 |
| FR-013 | C-5 |
| FR-015/FR-016 | C-10（校验程序内联）, B-2 |
| FR-017/FR-018/FR-019 | C-9, C-10 |
| FR-021 | B-3 |
| FR-022/FR-023 | C-10（变体内联） |
| FR-024 | C-12, C-13（+ distribution 契约 C-14…C-19） |
| FR-025 | C-11 |
| FR-026 | C-14 |
