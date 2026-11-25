---
id: "introspection-20261124T151412Z"
created: "2026-11-24T15:14:12Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (29 entries; framework hat; 5 inbound bundles digested separately as bundle material)"
scope_entries: ["20261124T081434Z-skill-sdd-loop-driver", "20261124T080150Z-skill-code-review", "20261124T080150Z-skill-review-feature-quality", "20261124T080150Z-skill-review-sdd-process", "20261124T080150Z-speckit-review", "20261124T075305Z-speckit-implement", "20261124T065225Z-speckit-analyze", "20261124T063845Z-skill-create-checklist", "20261124T063839Z-speckit-checklist", "20261124T063204Z-speckit-tasks", "20261124T061959Z-speckit-plan", "20261124T055722Z-speckit-clarify", "20261124T055026Z-speckit-requirements", "20261124T054130Z-skill-sdd-loop-driver", "20261124T045428Z-skill-code-review", "20261124T045428Z-skill-review-feature-quality", "20261124T045428Z-skill-review-sdd-process", "20261124T045428Z-speckit-review", "20261124T044509Z-speckit-implement", "20261124T035115Z-speckit-analyze", "20261124T034111Z-speckit-checklist", "20261124T033621Z-speckit-tasks", "20261124T032631Z-speckit-plan", "20261124T031033Z-skill-clarify-artifact", "20261124T031029Z-speckit-clarify", "20261124T030159Z-speckit-requirements", "20261124T025611Z-skill-create-requirements", "20261124T025602Z-speckit-requirements", "20261123T122840Z-speckit-feedback"]
supersedes: ""
confirmed_at: "2026-11-24T16:02:00Z"
---

# Introspection Report: introspection-20261124T151412Z

范围:本地库 **29** 条 open 条目(全部 `kind: internal`,`external_count: 0`)。本仓戴**框架帽子**(root 实测 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五个源目录俱在),故不存在上行侧,分流恒为 `local-sink(...)`;Path B 未被选中,也未被显式请求。

**覆盖核算**:10 个 Findings 含 23 条成员,Excluded 含 6 条,合计 29 条且互不重叠。本轮另有 5 个入站包共 185 条;其中 162 条与 2026-11-23 已消费包的条目逐字节相同,23 条新或变更条目按 A2/A4 单独核验与路由,不进入本报告成员(引擎 V-3)。

**执行形态**:4 个只读核验组请求并发,但 `concurrency-check.py capability` 返回 `owner-unavailable`(协调者派发裁决未裁定),故实际串行,理由码 `mechanism-not-yet-landed`。所有核验以 root 框架源为准,未以 `.specify/` 镜像为权威。

## Findings

### F-01: driver 的一次性阶段、retry 身份与执行证据生命周期不闭合

- **根因**: 阶段骨架缺少 one-shot 进程不得为等待而结束回合的永久条款;runner/watcher 的身份模型只有 line/run/stage,缺少 run/attempt 完整键,默认本地 runner 甚至不写 `run=`,所以跨 run 防护不能保证同 run retry 安全。执行证据生产者与消费者未同步演进,基线捕获纪律也只落在 implement 而未进入 driver brief。
- **证据锚点**: `skills/external/sdd-loop-driver/references/stage-prompts.md:33-53,161-174`; `skills/external/sdd-loop-driver/scripts/stage-runner.sh:52-70,204-231,392-394`; `skills/external/sdd-loop-driver/scripts/run-stage.sh:221-231,295-296`; `skills/external/sdd-loop-driver/scripts/watch-target.sh:395-409,626-629`; `skills/external/sdd-loop-driver/scripts/loop-state.py:883-892`; `skills/internal/implement-feature/SKILL.md:181-189`。
- **成员条目**: 20261124T054130Z-skill-sdd-loop-driver(部分成立), 20261124T081434Z-skill-sdd-loop-driver(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 定义并实现 one-shot 子进程生命周期与 run/attempt 身份契约:骨架明确等待时不得结束一次性进程;pid/heartbeat/status 四件套携带 run+attempt;retry 前归档旧 status,watcher 只接受当前 attempt;默认 runner 与 watcher 同步增加契约断言。driver 基线 brief 引用 implement 的禁止管道捕获规则,保证完整 stdout/stderr 与真实 rc 同步落盘。root-owned `.git/config` 是环境处置而非框架自动 chown,框架只做可读/可写预检与快速失败。
- **建议处置**: 20261124T054130Z-skill-sdd-loop-driver:processed, 20261124T081434Z-skill-sdd-loop-driver:processed

### F-02: review 的排除项、证据锚点与 smoke 证据所有权使覆盖率结论失真

- **根因**: review 工具把任何合法排除都折叠成二值 `not-evaluated`,skip 只能逐个正向 glob,发现表又缺 Evidence 列;smoke 固定重写同一 tracked evidence 路径。排除项与证据因此不能同时被如实表达,覆盖率与复现性都被削弱。
- **证据锚点**: `skills/internal/code-review/scripts/git-delta-review.sh:134-156,523-535,1131-1149,1281-1290`; `templates/review-template.md:105-107,131-133`; `tests/integration/test_acceptance_smoke.py:198-219`; `shared/workflow/acceptance-hardening.md:670-680`; `shared/declarations/facts/driver-stage-artifacts.yaml:46-50`; `templates/plan-template.md:84-98`。
- **成员条目**: 20261124T045428Z-skill-code-review(成立), 20261124T045428Z-skill-review-feature-quality(部分成立), 20261124T045428Z-speckit-review(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 设计「已审且有披露排除」的 verdict,保留 zero-gap 证据而不抹掉合法排除;支持 option-like note comment 与代码路径反向排除选择;finding 表增加 Evidence 列;smoke 改为每次运行独立证据路径或隔离临时树并保留显式再生入口。补齐 `notes/` 的 Project Structure 归属;`checklists/` 与 expected-set 并集已修,作为回归证据保留。外部改名 `ai-harness`/`.ah/` 与当前 `specify` smoke 不匹配属 NOT-OURS,不进入框架修复。
- **建议处置**: 20261124T045428Z-skill-code-review:processed, 20261124T045428Z-skill-review-feature-quality:processed, 20261124T045428Z-speckit-review:processed

### F-03: FR/task 覆盖与分析发现缺少 baseline-independent 的闭环门

- **根因**: FR accountant 只核合同引用而不核完整 FR→task 引用,plan 又没有不依赖 tasks baseline 的 FR-only 模式;analyze 能发现问题,但 carried MEDIUM/LOW 的处置、baseline freeze 状态与 registry 证据路径未全部成为后续门禁的必填输入,导致预测缺陷可以继续向下游流动。
- **证据锚点**: `scripts/python/account-clause-coverage.py:21-25,212-274,344-369,448-471,628-639`; `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:764-800`; `skills/internal/analyze-artifacts/SKILL.md:28-47,104-117,182-188`; `skills/internal/create-plan/SKILL.md:140-148`; `skills/internal/create-tasks/SKILL.md:386-402`; `shared/workflow/feature-integration.md:87-92`。
- **成员条目**: 20261124T045428Z-skill-review-sdd-process(部分成立), 20261124T035115Z-speckit-analyze(部分成立), 20261124T063204Z-speckit-tasks(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 给 accountant 增加显式只读、baseline-independent 的 plan/FR-citation 模式,在 plan integrity gate 前列出未引用 FR;保留 tasks 的完整 clause+baseline 门并补全 FR→task 检查。修正 analyze 示例 `--spec` 为 `--spec-dir`;stage-status 增加 baseline freeze 状态;每个携带 MEDIUM/LOW 必须有 fixed/deferred/rejected+reason;registry stage notes 必须给证据路径。当前 pre-analyze stdout 为 JSON、summary 在 stderr,freeze header 为两行,消费侧按事实分别读取,不再传播旧描述。
- **建议处置**: 20261124T045428Z-skill-review-sdd-process:processed, 20261124T035115Z-speckit-analyze:processed, 20261124T063204Z-speckit-tasks:processed

### F-04: plan/tasks/checklist/clarify 缺少确定性的派生后果检查与查询投影

- **根因**: 作者侧提示只描述当前制品,没有同步投影新 probe 注册、path governor、fixture 计数、checklist 阶段门、owner 字段索引和候选 Feature 行等机器可派生后果;读取又以宽文本搜索代替候选键查询,使问题迟至 implement/repair 才暴露并造成重复读取。
- **证据锚点**: `skills/internal/create-plan/SKILL.md:68-76,140-148,187-195,251-302`; `scripts/python/validate-tasks.py:93-123,242-267`; `shared/declarations/facts/driver-gate-roster.yaml:23-32`; `skills/internal/create-checklist/SKILL.md:121-124`; `skills/internal/clarify-artifact/SKILL.md:65-69`; `skills/external/sdd-loop-driver/references/stage-prompts.md:188-199`; `skills/external/sdd-loop-driver/scripts/audit-test-budget.py:334-359`。
- **成员条目**: 20261124T034111Z-speckit-checklist(部分成立), 20261124T033621Z-speckit-tasks(部分成立), 20261124T032631Z-speckit-plan(部分成立), 20261124T061959Z-speckit-plan(部分成立), 20261124T055722Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 建立作者侧派生后果清单与只读投影:plan 自审新 probe Object;tasks Format 指向 governor 真源并定义 fixture/test-file 计数;checklist 增加歧义→clarify 回路与确定性阶段门;driver brief 给出六字段 E3 的实际字段名;按候选 Feature ID 精确匹配整行并只投影 ID/name/status/details;生成 team 字段→owner 小节索引。附带补 Constitution 具体引用示例、mode-aware argument-hint 指引、`.git/config` 只读预检与共享 cleared-locus digest。checklist 合并规则、run governor、pre-analyze `--json-out` 与 measured carrier maps 已修,保持为回归证据。
- **建议处置**: 20261124T034111Z-speckit-checklist:processed, 20261124T033621Z-speckit-tasks:processed, 20261124T032631Z-speckit-plan:processed, 20261124T061959Z-speckit-plan:processed, 20261124T055722Z-speckit-clarify:processed

### F-05: requirements/clarify 的执行类义务分散在模板、生成器与后续修复轮

- **根因**: Runtime Stack、Assumptions、强制可执行路径与 checker 新鲜度没有在 requirements 生产端一次投影完整;clarify 的 Feature Linkage 与 deferral 扫描也没有依赖顺序和聚合字段查询,导致本可一次生成的内容靠后续修复轮补齐。
- **证据锚点**: `templates/requirements-template.md:105-190`; `shared/guidelines/requirements-guidelines.md:119-123`; `skills/internal/create-requirements/SKILL.md:72-154`; `skills/internal/clarify-artifact/SKILL.md:65-93`; `shared/constants/clarify-taxonomy.md:11-15,67-74`。
- **成员条目**: 20261124T031033Z-skill-clarify-artifact(部分成立), 20261124T031029Z-speckit-clarify(部分成立), 20261124T025611Z-skill-create-requirements(部分成立), 20261124T025602Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 requirements 模板与生成技能加入 class-conditional Runtime Stack 和 Assumptions,且在 requirements 阶段定稿强制可执行路径;每次 spec write-back 后都重跑 checker,而非仅 clarification 后。clarify 先完成 Feature Linkage 再做 deferral 扫描,并按字段聚合 owner grep 后再点读。flow-class 读取时机、Feature 注册/详情 deferral、Archive Layers owner 与 bounded/grep-led convention read 已修,作为防回归边界保留。
- **建议处置**: 20261124T031033Z-skill-clarify-artifact:processed, 20261124T031029Z-speckit-clarify:processed, 20261124T025611Z-skill-create-requirements:processed, 20261124T025602Z-speckit-requirements:processed

### F-06: feedback 入口缺少前置批次身份、点形态与完整计数核算

- **根因**: 批次身份启发式散在 A1/A2 文档且发生在 verifier 分组前后不一致的位置,引擎没有 bundle→store/history 的确定性身份动作;record/package 只复制点文本而不验形态或重复;list 在截断后计算 count,页面大小与真实匹配总数被混为一谈。
- **证据锚点**: `skills/internal/manage-feedback/references/path-a-digest.md:25-42,64-92`; `scripts/python/feedback-utils.py:291-298,1019-1021,2367-2371,2862-2868,2950-2951`。
- **成员条目**: 20261123T122840Z-speckit-feedback(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 在 verifier 分组前提供确定性批次身份动作,输入当前包、local store 与可用的 git 历史,输出 self-delivery/re-delivery/exact-subset/orphan 与逐条目内容哈希;本轮以该方式把 185 条入站物料缩减为 23 条新或变更条目,可作为目标场景。record/package 增加 heading/table-separator/bare-token/exact-duplicate 点形态校验;list 分列 `total`、`returned`、`truncated`,并为 >5 条 open 的反向用例补契约断言。
- **建议处置**: 20261123T122840Z-speckit-feedback:processed

### F-07: targeted-set 与 plan audit 用无损路径之外的 stem/basename 充当身份

- **根因**: generic skill stem 与 plan-owned basename 都没有仓库或 spec-dir 作用域,一个会近乎全套过选,另一个既误报同名 quickstart 又允许错误 declaration 覆盖;名称匹配代替了完整 repo-relative 路径身份。
- **证据锚点**: `skills/external/sdd-loop-driver/references/efficiency-model.md:107-117`; `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py:57-66,103-107`; `skills/internal/implement-feature/SKILL.md:181-189`; `shared/guidelines/temp-directory-discipline.md:7-20`。
- **成员条目**: 20261124T080150Z-skill-review-sdd-process(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: targeted-set 对 generic stem 只接受完整 repo-relative path,超预算替代集必须给具名可审计理由;plan audit 的 pathspec 与 declaration 都限到当前 spec-dir 并使用完整路径,增加同 basename 反例。implement 的 Test runs 明确完整证据落在 `<spec-dir>/test-evidence/` 或受制裁 `.specify/.tmp/`;既有 rc-mask 禁令与临时根规则保持不变。one-shot/retry 部分归入 F-01,不重复改。
- **建议处置**: 20261124T080150Z-skill-review-sdd-process:processed

### F-08: decomposed close 未把完整交付面与恰好一次的阶段记账交给同一所有者

- **根因**: review 组合命令实际交付两份报告与状态判定,而 driver declaration/map 只列 `review.md`;implement integrator 只被赋予聚合、提交、哨兵,包完成后的 wrap-up 仍由 driver 临时补账。交付物清单与记录所有权没有随 decomposed 执行形状同步扩展。
- **证据锚点**: `templates/commands/review.md:131-149`; `shared/declarations/facts/driver-stage-artifacts.yaml:62-67`; `skills/external/sdd-loop-driver/scripts/loop-state.py:255-260`; `skills/external/sdd-loop-driver/references/decomposition-model.md:230-246`; `skills/external/sdd-loop-driver/references/stage-prompts.md:79-86`。
- **成员条目**: 20261124T080150Z-speckit-review(成立), 20261124T075305Z-speckit-implement(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: review map 将 `code-review.md` 声明为条件交付物;prompt 明确 integrator 拥有两份报告、E3 与恰好一次的阶段 wrap-up/close-out,U4 核验这些记录,worker 不重复记录。Latest Review 与状态两载体明确由 driver 在 U4 后落地。review 时状态未落地而 driver 随后完成是时间顺序,不作为事实冲突。
- **建议处置**: 20261124T080150Z-speckit-review:processed, 20261124T075305Z-speckit-implement:processed

### F-09: agents 文档语义与封闭字面量守卫脱节

- **根因**: 文档仍暗示 init 后生成 agents,而现役 no-argument 行为是 listing;测试只排除若干精确拼写,插入形容词即可绕过,文档 bullet 与行为守卫未同步更新。
- **证据锚点**: `docs/reference/commands/agents.md:9`; `skills/internal/run-agent/SKILL.md:251-272`; `tests/contract/test_agents_run_docs_contract.py:90-121`。
- **成员条目**: 20261124T080150Z-skill-review-feature-quality(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 将 bullet 改为 init 后列出既有 agents,或显式 create/refine/run;把已观测变体加入 C-34,并增加可覆盖插入形容词的有限模式或行为断言,保留历史资料豁免,避免把封闭清单扩成不可判定自然语言承诺。
- **建议处置**: 20261124T080150Z-skill-review-feature-quality:processed

### F-10: requirements 脚手架把 option channel 与 description channel 混线

- **根因**: 命令模板把完整 `$ARGUMENTS` 经 stdin 传入,而脚手架设计上会合并 argv 描述与 stdin,导致 `--short-name` 等选项同时污染 feature description;参数解析通道与描述通道没有分离。
- **证据锚点**: `templates/commands/requirements.md:13-18`; `scripts/bash/create-new-requirements.sh:55-88,119-134`。
- **成员条目**: 20261124T055026Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: argv 只传解析后的 `--short-name` 等选项,stdin 只传剥离选项后的 feature description;增加含 `--short-name` 的端到端回归,断言生成 Input 不含该标志且短名仍生效。该条另一节选纪律点已由现行 create-requirements 与 token-efficiency 规则覆盖,无需重复改文档。
- **建议处置**: 20261124T055026Z-speckit-requirements:processed

## Excluded

- 20261124T044509Z-speckit-implement — 唯一点已过时:package executor 不执行 monolithic stage wrap-up、driver 在 U4 补账是当前明确规定的设计,不是残余缺陷
- 20261124T030159Z-speckit-requirements — 两点均为现行 token-efficiency、bounded/grep-led reads 与 recent-spec convention reuse 已覆盖的正向实践
- 20261124T080150Z-skill-code-review — 唯一点是五步非交互 review 路径的正向验证,无可行动缺陷
- 20261124T065225Z-speckit-analyze — 声明点是确定性优先、程序计数、scoped diff 与透明降级的正向实践;核验期另见的 `--spec` 示例问题已并入 F-03 的优化方案
- 20261124T063845Z-skill-create-checklist — 两点均为预回答 intent、默认 meta 与 40 项 soft cap 的正向实践
- 20261124T063839Z-speckit-checklist — 三点均为预回答、确定性小程序计数与既有决策面复用的正向实践
