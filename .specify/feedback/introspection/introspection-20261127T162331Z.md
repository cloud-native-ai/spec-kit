---
id: "introspection-20261127T162331Z"
created: "2026-11-27T16:23:31Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (108 entries; framework hat; 5 inbound bundles digested separately as bundle material)"
scope_entries: ["20261127T112506Z-speckit-review", "20261127T102915Z-speckit-review", "20261127T100546Z-speckit-implement", "20261127T094647Z-speckit-analyze", "20261127T092907Z-speckit-analyze", "20261127T091735Z-speckit-checklist", "20261127T091457Z-skill-code-review", "20261127T091456Z-skill-review-feature-quality", "20261127T091456Z-skill-review-sdd-process", "20261127T091450Z-speckit-review", "20261127T090930Z-speckit-tasks", "20261127T085805Z-skill-implement-feature", "20261127T085649Z-speckit-plan", "20261127T084443Z-speckit-implement", "20261127T084128Z-speckit-clarify", "20261127T082913Z-speckit-requirements", "20261127T082900Z-speckit-analyze", "20261127T082707Z-skill-analyze-artifacts", "20261127T081350Z-speckit-analyze", "20261127T081312Z-skill-create-checklist", "20261127T081047Z-speckit-review", "20261127T080505Z-speckit-checklist", "20261127T080418Z-skill-create-tasks", "20261127T075958Z-speckit-implement", "20261127T075556Z-speckit-tasks", "20261127T074856Z-skill-create-plan", "20261127T074304Z-speckit-plan", "20261127T074122Z-speckit-implement", "20261127T073341Z-skill-clarify-artifact", "20261127T073252Z-speckit-clarify", "20261127T073155Z-speckit-implement", "20261127T072628Z-skill-create-requirements", "20261127T072303Z-speckit-requirements", "20261127T071725Z-speckit-implement", "20261127T070457Z-speckit-implement", "20261127T065038Z-speckit-analyze", "20261127T063453Z-speckit-checklist", "20261127T062316Z-speckit-tasks", "20261127T060931Z-speckit-plan", "20261127T055653Z-skill-clarify-artifact", "20261127T054453Z-skill-create-requirements", "20261127T032610Z-skill-git-utils", "20261126T131456Z-skill-code-review", "20261126T131456Z-skill-review-feature-quality", "20261126T131456Z-skill-review-sdd-process", "20261126T131456Z-speckit-review", "20261126T125545Z-skill-implement-feature", "20261126T094007Z-skill-analyze-artifacts", "20261126T092426Z-skill-analyze-artifacts", "20261126T090913Z-skill-analyze-artifacts", "20261126T085303Z-speckit-checklist", "20261126T084451Z-speckit-tasks", "20261126T083347Z-speckit-plan", "20261126T082001Z-speckit-clarify", "20261126T072656Z-speckit-requirements", "20261126T071950Z-skill-create-team", "20261126T071950Z-skill-manage-features", "20261126T071950Z-skill-sdd-loop-driver", "20261126T071947Z-skill-analyze-artifacts", "20261126T071947Z-skill-create-requirements", "20261126T071947Z-skill-sdd-loop-driver", "20261126T071944Z-skill-sdd-loop-driver", "20261126T062923Z-skill-code-review", "20261126T062923Z-skill-review-feature-quality", "20261126T062916Z-skill-review-sdd-process", "20261126T061400Z-skill-implement-feature", "20261126T033532Z-skill-review-sdd-process", "20261126T032257Z-skill-implement-feature", "20261126T020919Z-skill-analyze-artifacts", "20261125T180117Z-skill-analyze-artifacts", "20261125T174002Z-skill-analyze-artifacts", "20261125T173633Z-skill-create-plan", "20261125T163801Z-skill-analyze-artifacts", "20261125T162329Z-skill-analyze-artifacts", "20261125T160807Z-skill-create-checklist", "20261125T143223Z-skill-create-tasks", "20261125T142034Z-skill-create-plan", "20261125T140714Z-skill-clarify-artifact", "20261125T135929Z-speckit-requirements", "20261125T134023Z-skill-analyze-artifacts", "20261125T132404Z-skill-analyze-artifacts", "20261125T125926Z-skill-analyze-artifacts", "20261125T125200Z-skill-analyze-artifacts", "20261125T123559Z-speckit-checklist", "20261125T122816Z-speckit-tasks", "20261125T121425Z-speckit-plan", "20261125T115512Z-speckit-clarify", "20261125T114609Z-speckit-requirements", "20261125T074209Z-skill-code-review", "20261125T074209Z-skill-review-feature-quality", "20261125T074209Z-skill-review-sdd-process", "20261125T074203Z-speckit-review", "20261125T062654Z-skill-run-agent", "20261125T062650Z-skill-sdd-loop-driver", "20261125T062647Z-skill-create-team", "20261125T062643Z-skill-sdd-loop-driver", "20261125T055151Z-skill-implement-feature", "20261125T053110Z-skill-implement-feature", "20261125T050056Z-skill-create-team", "20261125T041018Z-speckit-analyze", "20261125T035124Z-skill-create-checklist", "20261125T035124Z-speckit-checklist", "20261125T032813Z-speckit-tasks", "20261125T031441Z-speckit-plan", "20261125T024952Z-skill-clarify-artifact", "20261125T024126Z-speckit-requirements", "20261124T160649Z-skill-manage-feedback", "20261124T160649Z-speckit-feedback"]
supersedes: ""
confirmed_at: "2026-11-27T16:28:08Z"
---

# Introspection Report: introspection-20261127T162331Z

范围:本地库 **108** 条 open 条目(全部 `kind: internal`,`external_count: 0`)。本仓戴**框架帽子**(root 实测 templates、skills、shared、scripts、src/specify_cli 五个源目录俱在),故不存在上行侧,分流恒为 `local-sink(...)`;Path B 未被选中,也未被显式请求。

**覆盖核算**:39 个 Findings 含 87 条成员,Excluded 含 21 条,合计 108 条且互不重叠。本轮入站物料 194 条(180 条与已消费的 2026-11-23 包逐字节相同 + 14 条新条目)按 A2/A4 单独路由,不进入本报告成员(引擎 V-3)。

**执行形态**:10 个只读核验组并发派发(1 组因上限失败后拆两组重试),全部核验以 root 框架源为准,未以 `.specify/` 镜像为权威;主会话只消费各组判定表,未整库注入原文。

## Findings

### F-01: feedback 消化缺确定性的批次身份投影与清理后验

- **根因**: A1/A2 的批次身份启发式写在散文里且发生在 verifier 派发之后;引擎没有 bundle→store/history 的确定性身份动作,本条 batch 只能靠 git 历史手工哈希才把 194 条入站物料缩减为 14 条新条目。A5 的 rm→写日志没有删除后验,长跑也无登记义务指针。
- **证据锚点**: skills/internal/manage-feedback/references/path-a-digest.md:25-42,64-92,256-284;scripts/python/feedback-utils.py:577,630,2504;shared/guidelines/reporting-obligations.md:163-164;docs/reference/skills/feedback.md:166-180
- **成员条目**: 20261124T160649Z-skill-manage-feedback(部分成立), 20261124T160649Z-speckit-feedback(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 新增引擎级身份动作:输入当前包、local store 与 git 历史,输出 self-delivery/re-delivery/new/changed/orphan 与逐条目内容哈希,并在 verifier 分组前执行;A5 在写日志前断言包已不存在;长跑在首个 verifier 之前登记;作者骨架写明成员条目行文法。
- **建议处置**: 20261124T160649Z-skill-manage-feedback:processed, 20261124T160649Z-speckit-feedback:processed

### F-02: team 报告命名与工作区声明缺单一文法

- **根因**: 报告文件名文法在 SKILL.md 仍为自由占位符,读侧已落文法而写侧无校验;工作区文件仅声明清单,不写空占位,缺失与为空无法区分。
- **证据锚点**: skills/internal/create-team/SKILL.md:74,206;scripts/python/team-view.py:129-131,154-172;skills/internal/create-team/references/create-mode.md:17
- **成员条目**: 20261126T071950Z-skill-create-team(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 固定一条报告文件名文法并在写时校验(保留一份 legacy 容忍清单);创建时写空占位文件,使 missing 与 empty 可判。
- **建议处置**: 20261126T071950Z-skill-create-team:processed

### F-03: 团队并发上限缺少封闭 serial-reason 词表与 effective 读数面

- **根因**: serial-reason 封闭集只有六个单单元理由,team pattern/max_parallel 无对应码;effective 并发在 settle 时算得重叠却不在 status/measure 投影,未结算时也无警告。
- **证据锚点**: shared/declarations/facts/serial-reason.yaml:22-57;skills/internal/run-team/SKILL.md:64;scripts/python/concurrency-check.py:939-987;scripts/python/status-digest.py;scripts/python/measure.py
- **成员条目**: 20261125T062647Z-skill-create-team(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 为 team 上限/模式补充封闭理由码;把 effective 并发读数投影到 status/measure,未结算 run 显式告警。
- **建议处置**: 20261125T062647Z-skill-create-team:processed

### F-04: territory 预检只在逐路径检查,首个 executor 派发前无全量 diff

- **根因**: territory-check 是逐路径检查;create-team/improve-team/implement 均无「首派发前把全部任务写路径与 territory 求差」的程序步骤,territory 扩张后也只验证授权侧。
- **证据锚点**: skills/internal/create-team/scripts/territory-check.py:1-24;skills/internal/improve-team/SKILL.md:53-57;skills/internal/implement-feature/SKILL.md:125;tests/contract/test_handoff_territory.py:100-140
- **成员条目**: 20261125T050056Z-skill-create-team(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 首派发前执行一次全量 territory diff;扩张后同时复验授权与禁止两类路径。
- **建议处置**: 20261125T050056Z-skill-create-team:processed

### F-05: 注册表行与特性详情状态的双载体漂移无单一原子写者

- **根因**: manage-features 的校验路径没有行状态与详情状态等值检查;等值判定只散在 seal 的状态漂移守卫,状态翻转也非单写者原子完成。
- **证据锚点**: skills/internal/manage-features/SKILL.md:122-125;scripts/python/seal-utils.py:3373-3382,3744-3753;templates/commands/implement.md:59;shared/workflow/feature-integration.md:9-20
- **成员条目**: 20261126T071950Z-skill-manage-features(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 update/reconcile 路径加入行↔详情等值检查;把状态翻转收敛为一个命令/写者的原子双载体更新。
- **建议处置**: 20261126T071950Z-skill-manage-features:processed

### F-06: 派发遥测存在双路径且 driver 路径未接 collect-dispatch

- **根因**: collect-dispatch 只在 run-agent 内接线,driver 的派发路径不调用;subagent 定义暗示每次派发一条记录,但两条路径的边界与记录责任未成文,契约测试也未断言记录与报告行。
- **证据锚点**: skills/internal/run-agent/SKILL.md:152-160;skills/external/sdd-loop-driver/SKILL.md:284;shared/definitions/subagent-definitions.md:136;scripts/python/exec-quant.py:13-14,1060-1072
- **成员条目**: 20261125T062654Z-skill-run-agent(成立), 20261125T062643Z-skill-sdd-loop-driver(部分成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 二选一:统一派发路径,或把 reporter/measure/quant 接线移植到 driver;写明路径边界;补契约测试断言 agent 记录与报告行。
- **建议处置**: 20261125T062654Z-skill-run-agent:processed, 20261125T062643Z-skill-sdd-loop-driver:processed

### F-07: worktree/state-root 身份冲突与 chdir 前后相对路径失效

- **根因**: 注册表拒绝一切仓内 worktree 而治理规则与 dispatch recipe 却把仓内 .specify/.tmp worktree 声明为受制裁默认;stage-runner 先 chdir 后打开相对 prompt-file;worktree 运行的 state-root 未具名绝对路径。
- **证据锚点**: skills/external/sdd-loop-driver/scripts/line-registry.py:476-483,482;skills/external/sdd-loop-driver/references/dispatch-recipes.md:299,62-68;skills/external/sdd-loop-driver/scripts/stage-runner.sh:195-202,320-321,334,378;shared/guidelines/directory-governance.md:71;tests/contract/test_workspace_isolation_contract.py:591-606
- **成员条目**: 20261126T071947Z-skill-sdd-loop-driver(成立), 20261126T071944Z-skill-sdd-loop-driver(部分成立), 20261126T131456Z-skill-review-sdd-process(部分成立), 20261126T062916Z-skill-review-sdd-process(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 把注册表改为放行受制裁仓内前缀并补准入测试(现测试断言相反);prompt-file 在 chdir 前绝对化并做派发前存在性预检;dispatch 一律使用绝对 state-root。
- **建议处置**: 20261126T071947Z-skill-sdd-loop-driver:processed, 20261126T071944Z-skill-sdd-loop-driver:processed, 20261126T131456Z-skill-review-sdd-process:processed, 20261126T062916Z-skill-review-sdd-process:processed

### F-08: workspace 签名缺派发前快照、自证与记录槽

- **根因**: stage-runner 无派发前快照步骤,「before」只在协议散文中存在;check 与任意自带文件比较,新鲜自快照可读成干净;DRIFT 在 git 不可读时以空 refs 输出,无降级裁决。
- **证据锚点**: skills/external/sdd-loop-driver/references/checkpoint-protocol.md:159,168-200;scripts/python/workspace-guard.py:46-52,85-109,37-52,99
- **成员条目**: 20261126T071950Z-skill-sdd-loop-driver(成立), 20261125T115512Z-speckit-clarify(成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 在 stage-runner 增加派发前快照与前后标记;快照/记录携带 attestation 与 workspace-signature 槽;git 不可读时输出显式 degraded 裁决而非 DRIFT。
- **建议处置**: 20261126T071950Z-skill-sdd-loop-driver:processed, 20261125T115512Z-speckit-clarify:processed

### F-09: baseline 冻结归属错位与 fr-uncovered 车道无 plan-only 处置

- **根因**: 冻结 owner 对 tasks 已声明,但 baseline 仍列在 Setup 行落地点,诱导推迟到 implement;fr-uncovered 车道无 baseline 与 plan-only 处置,且 analyze 的 gate 仍是散文而非单一机器值。
- **证据锚点**: skills/internal/create-tasks/SKILL.md:364-391;scripts/python/account-clause-coverage.py:34-35,391-397;tests/contract/test_clause_coverage.py:1100-1125;skills/internal/analyze-artifacts/SKILL.md:165
- **成员条目**: 20261127T092907Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 把 baseline 冻结物移到 freeze owner 项下并补反例;给 fr-uncovered 车道补 baseline 与 plan-only 处置;analyze 输出单一机器 gate 值供 driver 消费。
- **建议处置**: 20261127T092907Z-speckit-analyze:processed

### F-10: prompt-adherence 的空 run_id 身份与 --check-coverage/--json 组合未定义

- **根因**: 阅读态 token 与重复键规则已声明,但空 run_id 的身份未定义;--check-coverage 忽略 --json 且组合语义未声明。
- **证据锚点**: shared/definitions/prompt-adherence-definitions.md:40-43,139-151;scripts/python/prompt-adherence.py:1264,1579
- **成员条目**: 20261127T065038Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 定义空 run_id 的生成/拒绝规则;声明 --check-coverage 与 --json 的组合语义并在引擎内实现或拒绝。
- **建议处置**: 20261127T065038Z-speckit-analyze:processed

### F-11: 封闭集合断言的判定在作者期与校验期都缺机械执行

- **根因**: requirements/clarify 只有散文级 containment 指引,validator 无判定检查;tasks 阶段也无 containment 动词的 baseline/比较单位检查;analyze 只有散文判定,无 SC 与 allowlist 的机械 diff。
- **证据锚点**: shared/guidelines/requirements-guidelines.md:31,109-111;scripts/python/validate-requirements.py:8;scripts/python/validate-tasks.py:34;skills/internal/analyze-artifacts/references/detection-and-severity.md:67-73;tests/contract/test_closed_set_claims.py
- **成员条目**: 20261126T071947Z-skill-create-requirements(成立), 20261126T094007Z-skill-analyze-artifacts(部分成立), 20261125T041018Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 五要素判定前移:作者期预检 + validate-requirements 检查 + 一个故意不可判定的红样例;tasks 阶段补 containment 动词检查;clarify 增判定类别;analyze 增机械 diff。
- **建议处置**: 20261126T071947Z-skill-create-requirements:processed, 20261126T094007Z-skill-analyze-artifacts:processed, 20261125T041018Z-speckit-analyze:processed

### F-12: pre-analyze/validator 覆盖缺口与缺失路径告警噪声

- **根因**: 缺失路径告警按每次交付物提及重复且无 plan Source-Code 允许清单;validator 无枚举叉积、territory 行、claim 顺序与 requirements 阶段合并门等检查;告警不分阶段重复。
- **证据锚点**: skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:547-565,1274;scripts/python/validate-requirements.py:8;scripts/python/validate-tasks.py:51-58,97-108;shared/workflow/expression-gates.md:44
- **成员条目**: 20261126T092426Z-skill-analyze-artifacts(部分成立), 20261126T090913Z-skill-analyze-artifacts(部分成立), 20261127T080418Z-skill-create-tasks(成立), 20261125T122816Z-speckit-tasks(部分成立), 20261125T135929Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 以 plan Source-Code allow-list 压制缺失路径噪声;补枚举叉积检查、team 禁止路径的 tasks 行检查、claim-order advisor;requirements 阶段合并为单一 gate 信封;告警按阶段分档或豁免。
- **建议处置**: 20261126T092426Z-skill-analyze-artifacts:processed, 20261126T090913Z-skill-analyze-artifacts:processed, 20261127T080418Z-skill-create-tasks:processed, 20261125T122816Z-speckit-tasks:processed, 20261125T135929Z-speckit-requirements:processed

### F-13: clause/ID 命名空间冲突与写前文法缺失

- **根因**: INV-NN 等计划内标识被外部 clause 规则误读;POINTER_CONTEXT 不认 git show/cat-file 只读取证;合约定稿前无 clause 文法检查;表格字面管道符会断行。
- **证据锚点**: shared/definitions/contract-clause-definitions.md:42;skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:66-67;scripts/python/validate-tasks.py:115-116;templates/plan-template.md:176-180;skills/internal/create-tasks/SKILL.md:386-391
- **成员条目**: 20261125T121425Z-speckit-plan(部分成立), 20261125T032813Z-speckit-tasks(部分成立), 20261126T084451Z-speckit-tasks(成立), 20261126T083347Z-speckit-plan(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: plan 写入前执行 clause 文法检查并记录限制;为计划内标识保留命名空间/允许清单;POINTER_CONTEXT 增加只读 git 取证;模板警示表格管道符;给出仅读 coverage-baseline 头的指引。
- **建议处置**: 20261125T121425Z-speckit-plan:processed, 20261125T032813Z-speckit-tasks:processed, 20261126T084451Z-speckit-tasks:processed, 20261126T083347Z-speckit-plan:processed

### F-14: owner 变更/修复后的传播扫掠未成规

- **根因**: OSOT 只要求修副本,没有「owner 内容变更即扫掠描述性复述」条款;跨制品 baseline 修正不会同趟传播到 feature detail;修复传播只覆盖单一 DoD 命名,不覆盖第二副本与兄弟门;class-gate 矛盾无 requirements 阶段交叉检查。
- **证据锚点**: shared/guidelines/one-source-of-truth.md:23-29;shared/workflow/feature-integration.md:84;skills/internal/analyze-artifacts/SKILL.md:188-193;shared/definitions/decision-definitions.md:250-252
- **成员条目**: 20261127T082900Z-speckit-analyze(成立), 20261127T085649Z-speckit-plan(部分成立), 20261127T084128Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 补 owner-change sweep 条款与同趟 baseline 传播规则;修复传播扩到第二副本/兄弟门;requirements 阶段增 class-gate 交叉检查。
- **建议处置**: 20261127T082900Z-speckit-analyze:processed, 20261127T085649Z-speckit-plan:processed, 20261127T084128Z-speckit-clarify:processed

### F-15: 仍由人手完成的确定性盘点与投影

- **根因**: port-target surface、Feature 绑定候选评分、路径引用盘点、carrier probe 表与 feature→verification 索引都靠 agent grep/手写;无引擎投影,导致重复读取与漏项。
- **证据锚点**: skills/internal/create-requirements/SKILL.md:104-110;shared/workflow/feature-integration.md:75;skills/internal/create-plan/SKILL.md:196-204,74-76;templates/feature-details-template.md:89
- **成员条目**: 20261127T073252Z-speckit-clarify(成立), 20261125T140714Z-skill-clarify-artifact(成立), 20261125T024126Z-speckit-requirements(成立), 20261127T074304Z-speckit-plan(成立), 20261127T074856Z-skill-create-plan(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 提供只读确定性投影:port surface probe、绑定候选评分、路径引用盘点(含 legacy 字面量允许清单)、carrier probe 表、feature verification 索引;artifact 一律由程序生成、agent 只消费摘要。
- **建议处置**: 20261127T073252Z-speckit-clarify:processed, 20261125T140714Z-skill-clarify-artifact:processed, 20261125T024126Z-speckit-requirements:processed, 20261127T074304Z-speckit-plan:processed, 20261127T074856Z-skill-create-plan:processed

### F-16: 阶段派发未声明注册表/spine 越界边界

- **根因**: plan 阶段必须推进 features.md,但 dispatch brief 只写「不许编辑注册表」而不点名具体越界文件,执行者无法判断哪些写属越界。
- **证据锚点**: skills/external/sdd-loop-driver/references/stage-prompts.md:37-42
- **成员条目**: 20261127T060931Z-speckit-plan(成立)
- **分流决定**: local-sink(improve-agent)
- **优化方案**: dispatch brief 以具名默认值列出越界注册表/spine 文件,并声明本阶段允许的注册表写集。
- **建议处置**: 20261127T060931Z-speckit-plan:processed

### F-17: checklist 阶段无程序化门与 roster 条目

- **根因**: gate roster 只有 requirements/plan/tasks;checklist 调用退 2,阶段以临时 heredoc 自检,无确定性阶段门;skill 也未标注 canonical-source 路径。
- **证据锚点**: shared/declarations/facts/driver-gate-roster.yaml:23-32;shared/workflow/expression-gates.md:52-53;skills/internal/create-checklist/SKILL.md:20
- **成员条目**: 20261127T091735Z-speckit-checklist(部分成立), 20261127T063453Z-speckit-checklist(成立), 20261126T085303Z-speckit-checklist(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 为 checklist 增 stage operator 与 roster 行,替换临时自检;SKILL 标注源与运行时镜像的路径归属。
- **建议处置**: 20261127T091735Z-speckit-checklist:processed, 20261127T063453Z-speckit-checklist:processed, 20261126T085303Z-speckit-checklist:processed

### F-18: checklist 作者侧自动化缺失(页脚矩阵/合并图/抽取图)

- **根因**: 页脚覆盖矩阵仍手写、soft-cap 合并图不出现在 Notes、证据节无 pattern-first 抽取图,导致整文件读取与人工对齐。
- **证据锚点**: skills/internal/create-checklist/SKILL.md:93-108,68-79;templates/checklist-template.md:39-44;shared/guidelines/checklist-methodology.md:46-71
- **成员条目**: 20261125T160807Z-skill-create-checklist(成立), 20261125T035124Z-skill-create-checklist(成立), 20261125T123559Z-speckit-checklist(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 提供页脚矩阵解析器与合并图投影;补 pattern-first 抽取图与按节问题库。
- **建议处置**: 20261125T160807Z-skill-create-checklist:processed, 20261125T035124Z-skill-create-checklist:processed, 20261125T123559Z-speckit-checklist:processed

### F-19: port 适配清单与 Feature 绑定缺确定性查找

- **根因**: port 适配清单靠 grep 发现而非缺失传感器盘点;Feature 候选以 spec 序号而非解析后的 Feature ID 命名;clarify 复用扫描不查 features.md;dispatch 不命名协议必备文件与越界路径。
- **证据锚点**: skills/internal/create-requirements/SKILL.md:104-110,92-99;shared/workflow/feature-integration.md:10-11,75;.specify/glossary.md:75;skills/external/sdd-loop-driver/references/stage-prompts.md:368,379
- **成员条目**: 20261127T073341Z-skill-clarify-artifact(部分成立), 20261127T072628Z-skill-create-requirements(部分成立), 20261127T055653Z-skill-clarify-artifact(部分成立), 20261126T082001Z-speckit-clarify(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 以缺失传感器盘点生成 port 适配清单;写前把 Feature ID 对注册表解析;brief 一律使用解析后的 Feature ID 并点名协议必备/越界文件。
- **建议处置**: 20261127T073341Z-skill-clarify-artifact:processed, 20261127T072628Z-skill-create-requirements:processed, 20261127T055653Z-skill-clarify-artifact:processed, 20261126T082001Z-speckit-clarify:processed

### F-20: code-review 覆盖额度与回执形状使结论失真

- **根因**: 任何合法 skip 都被折成 not-evaluated,回执分母取全变更集而非代码路径集;回执不携带记录的 base/head;每文件三行回执永不压缩;未提交范围披露只覆盖两个前缀。
- **证据锚点**: skills/internal/code-review/scripts/git-delta-review.sh:1286-1287,1261,1164-1166,1323-1332,1125-1129
- **成员条目**: 20261127T091457Z-skill-code-review(成立), 20261127T081047Z-speckit-review(成立), 20261126T131456Z-skill-code-review(成立), 20261126T131456Z-speckit-review(成立), 20261126T062923Z-skill-code-review(成立), 20261125T074209Z-skill-code-review(成立), 20261126T062923Z-skill-review-feature-quality(部分成立), 20261126T033532Z-skill-review-sdd-process(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 引入按类覆盖读数与 triage 驱动分母;回执携带记录范围并在失配时告警;回执改为集合等值摘要+文件清单哈希;扩大未提交范围披露。
- **建议处置**: 20261127T091457Z-skill-code-review:processed, 20261127T081047Z-speckit-review:processed, 20261126T131456Z-skill-code-review:processed, 20261126T131456Z-speckit-review:processed, 20261126T062923Z-skill-code-review:processed, 20261125T074209Z-skill-code-review:processed, 20261126T062923Z-skill-review-feature-quality:processed, 20261126T033532Z-skill-review-sdd-process:processed

### F-21: closure 记录(DoD/验证注记)无更新者与证据出处

- **根因**: tasks DoD Status 行无脚本/技能在关闭后更新;verification SC_note 自由文本,不要求注明读数所属 run;containment 读数在最后三次提交前就标 final;red-first 前载纪律无 owner。
- **证据锚点**: templates/tasks-template.md:52;templates/verification-log-template.md:155-157,63-69;skills/internal/implement-feature/SKILL.md:322-329
- **成员条目**: 20261127T091456Z-skill-review-feature-quality(部分成立), 20261125T074209Z-skill-review-feature-quality(部分成立), 20261125T074203Z-speckit-review(部分成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 为 DoD Status 指定更新者与时机;verification 注记强制注明 producing run;读数 final 须在冻结树之后;补 red-first owner;review 日志默认落在仓外。
- **建议处置**: 20261127T091456Z-skill-review-feature-quality:processed, 20261125T074209Z-skill-review-feature-quality:processed, 20261125T074203Z-speckit-review:processed

### F-22: 阶段完成条件与门可满足性未闭合

- **根因**: U4 验收不要求干净工作树或显式路径提交;全量测量无冻结树前置;close-out 只提交记录、不再开制品提交;GATE 要求执行席位无法通过的检查;U4 记录类别未点名;tasks 无中途 addendum 车道。
- **证据锚点**: skills/external/sdd-loop-driver/references/stage-prompts.md:84-88,103;shared/guidelines/test-execution-efficiency.md:121;shared/workflow/artifact-commit-step.md:88;templates/tasks-template.md:74;skills/internal/create-team/references/handoff-contract-template.md:104
- **成员条目**: 20261125T031441Z-speckit-plan(部分成立), 20261127T091456Z-skill-review-sdd-process(成立), 20261125T074209Z-skill-review-sdd-process(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: U4 增干净树或显式路径提交前置;全量测量要求冻结树;close-out 再开制品提交;逐条校正不可满足的门;U4 点名四类记录;tasks 增 addendum 车道。
- **建议处置**: 20261125T031441Z-speckit-plan:processed, 20261127T091456Z-skill-review-sdd-process:processed, 20261125T074209Z-skill-review-sdd-process:processed

### F-23: run-determination 对非测试绿门与计划内瞬态红无表示

- **根因**: artifact-correctness 在逐检查绿证据之前即返回 no_baseline,非测试阶段绿门恒为 not_evaluated/regressed;计划内 pending/known-transient 红无取值,非空 diff 即判 regressed。
- **证据锚点**: scripts/python/run-determination.py:637-643,141,165,931-945;scripts/bash/run-tests.sh:319,345,399
- **成员条目**: 20261126T072656Z-speckit-requirements(部分成立), 20261127T084443Z-speckit-implement(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 为绿的非测试声明类检查提供 artifact-correctness 车道;增加 planned/transient 红取值与理由;修复 runner 未加引号的 ${ARGS[*]} 回显。
- **建议处置**: 20261126T072656Z-speckit-requirements:processed, 20261127T084443Z-speckit-implement:processed

### F-24: dated 证据文件被整套重写且缺失夹具用空目录表达

- **根因**: acceptance smoke 无条件覆盖同一 dated evidence 文件;absence 夹具指导缺失,空目录无法入库,0 字节文件才承载该案例。
- **证据锚点**: tests/integration/test_acceptance_smoke.py:49,212-233;shared/definitions/context-management-definitions.md:78
- **成员条目**: 20261125T055151Z-skill-implement-feature(成立), 20261125T053110Z-skill-implement-feature(成立), 20261127T085805Z-skill-implement-feature(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 每次运行写独立证据路径或隔离临时树并保留显式再生入口;补「absence 用 0 字节文件、不用空目录」的夹具规则。
- **建议处置**: 20261125T055151Z-skill-implement-feature:processed, 20261125T053110Z-skill-implement-feature:processed, 20261127T085805Z-skill-implement-feature:processed

### F-25: implement 侧 verdict 摘要投影与 writeback 后验缺失

- **根因**: integrator 整份读取 verdict JSON,wp-report 不投影 task_id/result/verdict;worktree 运行的 main-repo state root 未具名;证据注记计数无机器推导;package close 无逐任务写回存在性检查。
- **证据锚点**: skills/external/sdd-loop-driver/scripts/wp-report.py:596-611;skills/external/sdd-loop-driver/references/decomposition-model.md:95;skills/external/sdd-loop-driver/SKILL.md:126;skills/external/sdd-loop-driver/references/dispatch-recipes.md:67;skills/internal/create-team/references/handoff-contract-template.md:82-88
- **成员条目**: 20261126T125545Z-skill-implement-feature(成立), 20261126T061400Z-skill-implement-feature(成立), 20261126T032257Z-skill-implement-feature(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: wp-report 增 per-package 摘要(task_id/result/verdict);dispatch 使用绝对 state-root;证据注记计数由程序生成;package close 增写回存在性断言。
- **建议处置**: 20261126T125545Z-skill-implement-feature:processed, 20261126T061400Z-skill-implement-feature:processed, 20261126T032257Z-skill-implement-feature:processed

### F-26: requirements 脚手架编号计数与就地模式缺失

- **根因**: 脚手架把当前分支名计入编号候选后无条件 checkout -b;已位于目标特性分支时失败;无 --number 或 in-place 模式,107/108/111 连续复发。
- **证据锚点**: scripts/bash/create-new-requirements.sh:368-392,525,531-532
- **成员条目**: 20261127T082913Z-speckit-requirements(成立), 20261127T072303Z-speckit-requirements(成立), 20261127T054453Z-skill-create-requirements(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 提供 --number/--feature-id 与就地模式;编号只从必要来源推导;补含 --short-name 的端到端回归(选项不得混入 description)。
- **建议处置**: 20261127T082913Z-speckit-requirements:processed, 20261127T072303Z-speckit-requirements:processed, 20261127T054453Z-skill-create-requirements:processed

### F-27: requirements 检查清单缺强制 Runtime Stack 项

- **根因**: acceptance-hardening 要求 § Runtime Stack & Dependency Ownership 表,但 requirements 模板与检查清单均未列该强制项,交付易漏。
- **证据锚点**: shared/workflow/acceptance-hardening.md:315;templates/requirements-template.md
- **成员条目**: 20261125T114609Z-speckit-requirements(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 requirements 模板与检查清单加入该强制表项及空表反例。
- **建议处置**: 20261125T114609Z-speckit-requirements:processed

### F-28: 安装态与源码态 CLI 运行形式未成文

- **根因**: 文档只说明 editable install vs 裸 checkout,未给出源码态运行(PYTHONPATH=src / python -m)的演练形式。
- **证据锚点**: docs/tutorials/installation.md:122
- **成员条目**: 20261127T075556Z-speckit-tasks(部分成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 补源码态运行与验证命令,并与 editable 安装的差异并列。
- **建议处置**: 20261127T075556Z-speckit-tasks:processed

### F-29: TB-05 对 docs-only 变更先算全量候选

- **根因**: TB-05 在判定 docs-only 之前先计算全量候选,零可执行变更仍产出数百候选噪声。
- **证据锚点**: skills/external/sdd-loop-driver/references/efficiency-model.md:117
- **成员条目**: 20261125T173633Z-skill-create-plan(成立), 20261125T142034Z-skill-create-plan(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 把 docs-only 早筛前置到候选计算之前,并在输出中标注跳过原因。
- **建议处置**: 20261125T173633Z-skill-create-plan:processed, 20261125T142034Z-skill-create-plan:processed

### F-30: 写只读治理器未按实际写类判定

- **根因**: 共享测试行的只读措辞已有指引,但治理器仍按字面路径把引用型读取判为写;无通用 per-path 读写分类。
- **证据锚点**: skills/internal/create-tasks/SKILL.md:331-343;scripts/python/validate-tasks.py:97-108
- **成员条目**: 20261127T090930Z-speckit-tasks(部分成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 为治理器引入按调用形态的读写分类(如 git show/cat-file、只读 pytest 参数),并补反例。
- **建议处置**: 20261127T090930Z-speckit-tasks:processed

### F-31: review 入口解释器阶梯与 analyzer gate/路径包含性缺口

- **根因**: run-tests 解释器阶梯只解析 PATH/相对 python,无绝对解释器探测;analyze 仍报散文门;decision-batch 的 pointer 解析接受 .. 段而无工作区包含约束。
- **证据锚点**: scripts/bash/run-tests.sh:56-77;skills/internal/analyze-artifacts/SKILL.md:165;scripts/python/decision-batch.py:448-458,560-563
- **成员条目**: 20261127T112506Z-speckit-review(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 补绝对解释器探测;analyze 输出单一机器 gate 值;pointer/显式路径解析拒绝逃逸工作区的 .. 段。
- **建议处置**: 20261127T112506Z-speckit-review:processed

### F-32: implement→review 交接缺闭集制品清单与 Pinning 解析器

- **根因**: 交接只点名 checker 与 verification.md,无闭集制品枚举;validate-tasks 只解析合同 clause,不解析 *_test.py::test_* Pinning;review 模板占位无注册期断言。
- **证据锚点**: templates/commands/implement.md:50,58-59;scripts/python/validate-tasks.py:501-532;templates/feature-details-template.md:19-21
- **成员条目**: 20261127T102915Z-speckit-review(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 交接声明闭集制品清单;validate-tasks 增 Pinning token 解析;注册期断言 Latest Review 占位被替换。
- **建议处置**: 20261127T102915Z-speckit-review:processed

### F-33: code-review 基线与阶段注册缺声明式 tier

- **根因**: 基线 tier 只有 explicit/feature-first-commit/trunk-merge-base,无声明式 baseline;driver 阶段序列无注册阶段。
- **证据锚点**: skills/internal/code-review/scripts/git-delta-review.sh:761-793,781-789;shared/declarations/facts/driver-stage-sequence.yaml:14-23
- **成员条目**: 20261127T091450Z-speckit-review(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 增加 declared-baseline tier 并在记录中携带;把注册并入阶段序列或实现完整收敛。
- **建议处置**: 20261127T091450Z-speckit-review:processed

### F-34: feedback record 的 --notes 被声明却静默忽略

- **根因**: record 动作全局声明 --notes 但实现不消费,属于静默忽略的选项。
- **证据锚点**: scripts/python/feedback-utils.py:808-812,832-856
- **成员条目**: 20261127T081350Z-speckit-analyze(成立)
- **分流决定**: local-sink(improve-tools)
- **优化方案**: 按动作限定选项集,或在 record 中消费 --notes(写入notes字段);未消费的选项必须拒绝。
- **建议处置**: 20261127T081350Z-speckit-analyze:processed

### F-35: analyze 轮次记录未记录实际输出预算

- **根因**: 输出预算已约束 worker,但轮次记录字段不含 applied budget,无法复核预算是否执行。
- **证据锚点**: skills/internal/analyze-artifacts/SKILL.md:47
- **成员条目**: 20261126T071947Z-skill-analyze-artifacts(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 轮次记录增 applied-budget 字段并由程序写入。
- **建议处置**: 20261126T071947Z-skill-analyze-artifacts:processed

### F-36: 决策三受保护路径缺 facts 单一所有者与裁定检查

- **根因**: decision-definitions 仍以 <三路径>/<有效基线> 占位书写,无 facts 文件拥有该集合;裁定提交是否触及三路径只靠评审,无 checker。
- **证据锚点**: shared/definitions/decision-definitions.md:668-669
- **成员条目**: 20261126T020919Z-skill-analyze-artifacts(成立), 20261125T180117Z-skill-analyze-artifacts(成立)
- **分流决定**: local-sink(improve-docs)
- **优化方案**: 由 facts 声明拥有三路径与有效基线/替换规则;增加裁定提交路径覆盖 checker。
- **建议处置**: 20261126T020919Z-skill-analyze-artifacts:processed, 20261125T180117Z-skill-analyze-artifacts:processed

### F-37: 验证边界在报告与记录中逐字复制

- **根因**: validation-and-report 仍要求把 validator 边界逐字复制到报告与 verdicts 记录,无共享文件引用形态,产生重复源。
- **证据锚点**: skills/internal/analyze-artifacts/references/validation-and-report.md:59-60
- **成员条目**: 20261125T125200Z-skill-analyze-artifacts(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 改为引用共享边界文件(wp-report 或 facts 文件),记录只存路径与哈希。
- **建议处置**: 20261125T125200Z-skill-analyze-artifacts:processed

### F-38: runtime-store-layout 消费者清单靠手工增长

- **根因**: triple-check 无法从声明推导消费者清单,新增消费者需三处手工核对。
- **证据锚点**: scripts/python/harness-triple-check.py:15-16,314;shared/declarations/facts/runtime-store-layout.yaml:115-121
- **成员条目**: 20261127T075958Z-speckit-implement(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 从声明与代码扫描自动派生消费者清单,并与 triple-check 共用单一提取器。
- **建议处置**: 20261127T075958Z-speckit-implement:processed

### F-39: plan 期测试名与 tasks 期实际命名无对账

- **根因**: plan 的 S-7 命名了不存在的测试,plan 期测试名与 tasks 期落地命名无对账步骤。
- **证据锚点**: skills/internal/create-tasks/SKILL.md:255-270;skills/internal/review-sdd-process/SKILL.md:163-166
- **成员条目**: 20261126T131456Z-skill-review-feature-quality(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: tasks 期以程序对账 plan 期测试名,失配即阻断或在 plan 注记。
- **建议处置**: 20261126T131456Z-skill-review-feature-quality:processed

## Excluded

- 20261127T082707Z-skill-analyze-artifacts — 全部点为 feature-110 合同/data-model/tasks 内容与注册表延后项,不在框架源
- 20261125T174002Z-skill-analyze-artifacts — 完成式修复陈述与实践注记,无待办缺陷
- 20261125T163801Z-skill-analyze-artifacts — 唯一点已由 decision-definitions.md:149-203 的字段所有权表覆盖
- 20261125T162329Z-skill-analyze-artifacts — 唯一点已由 dated checklist 快照规则覆盖(create-checklist/SKILL.md:98-103)
- 20261125T134023Z-skill-analyze-artifacts — 完成式修复陈述与实践注记
- 20261125T132404Z-skill-analyze-artifacts — 实践注记;逗号拼接参数受引擎 repeatable 支持
- 20261125T125926Z-skill-analyze-artifacts — 正向实践与已由 pre-analyze 覆盖的预检;日期化重复属 OSOT 合法例外
- 20261127T100546Z-speckit-implement — 全部点已修、计数维护或一次性任务编排
- 20261127T074122Z-speckit-implement — 仅 dated baseline 记录与回放说明,无缺陷
- 20261127T073155Z-speckit-implement — 运行状态叙事,无框架主张
- 20261127T071725Z-speckit-implement — 证据叙事/暂态披露,无可行动点
- 20261127T070457Z-speckit-implement — 引擎 pin 已满足,无缺陷
- 20261125T024952Z-skill-clarify-artifact — 已修与运行本地排序观察,无待办
- 20261127T081312Z-skill-create-checklist — 全部点为 feature-110 规格内容,不属框架源
- 20261127T080505Z-speckit-checklist — token 消耗叙事与已携带的 CHK023,无可行动点
- 20261127T062316Z-speckit-tasks — 共享测试修复已落地;brief 枚举漂移非框架
- 20261125T143223Z-skill-create-tasks — 已修与正向观察
- 20261125T035124Z-speckit-checklist — 已修与 Summary-First 正向观察
- 20261127T094647Z-speckit-analyze — 4/5 点为 feature-112 设计制品;第 5 点(baseline 冻结归属)并入 F-09
- 20261125T062650Z-skill-sdd-loop-driver — 两点均已被 wp-report/concurrency-check 实现
- 20261127T032610Z-skill-git-utils — 条目自述无显著优化点
