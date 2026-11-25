---
id: "introspection-20261021T133447Z"
created: "2026-10-21T13:34:47Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (70 entries; framework hat; 0 pending bundles; excludes 20261021T130319Z-speckit-plan created during the run)"
scope_entries: ["20261015T090816Z-skill-manage-feedback", "20261016T025641Z-skill-create-requirements", "20261016T025641Z-speckit-requirements", "20261016T031322Z-speckit-clarify", "20261016T040553Z-speckit-plan", "20261016T043010Z-speckit-tasks", "20261016T054516Z-speckit-implement", "20261016T061443Z-speckit-review", "20261016T061518Z-skill-review-sdd-process", "20261016T080252Z-skill-git-utils", "20261016T083949Z-speckit-requirements", "20261016T102726Z-speckit-clarify", "20261016T110804Z-speckit-plan", "20261016T112548Z-speckit-tasks", "20261016T122911Z-speckit-analyze", "20261016T174959Z-speckit-implement", "20261016T180912Z-skill-improve-skills", "20261018T002011Z-speckit-requirements", "20261018T002912Z-speckit-clarify", "20261018T002921Z-skill-clarify-artifact", "20261018T011402Z-speckit-plan", "20261018T013204Z-speckit-tasks", "20261018T014641Z-speckit-checklist", "20261018T015912Z-speckit-analyze", "20261018T030254Z-skill-implement-feature", "20261018T034058Z-speckit-review", "20261019T063816Z-skill-improve-skills", "20261019T063837Z-skill-improve-skills", "20261019T065041Z-skill-improve-skills", "20261019T071229Z-speckit-requirements", "20261019T072038Z-speckit-clarify", "20261019T075055Z-speckit-plan", "20261019T080718Z-speckit-tasks", "20261019T081434Z-speckit-checklist", "20261019T083518Z-speckit-clarify", "20261019T085059Z-speckit-plan", "20261019T085937Z-speckit-tasks", "20261019T103809Z-speckit-implement", "20261019T114446Z-speckit-review", "20261019T122920Z-skill-sdd-loop-driver", "20261019T125018Z-speckit-clarify", "20261019T131539Z-speckit-plan", "20261019T133435Z-speckit-tasks", "20261019T134009Z-speckit-checklist", "20261019T140016Z-speckit-analyze", "20261019T163355Z-speckit-requirements", "20261019T164049Z-speckit-clarify", "20261019T164539Z-speckit-instructions", "20261019T170645Z-speckit-plan", "20261019T172529Z-speckit-checklist", "20261019T184312Z-speckit-implement", "20261019T190639Z-speckit-review", "20261019T191328Z-skill-sdd-loop-driver", "20261020T023920Z-skill-git-utils", "20261020T031448Z-skill-improve-skills", "20261020T033719Z-speckit-requirements", "20261020T034718Z-speckit-clarify", "20261020T041125Z-speckit-plan", "20261020T042203Z-speckit-tasks", "20261020T043644Z-speckit-checklist", "20261020T044640Z-speckit-analyze", "20261020T050419Z-speckit-analyze", "20261020T130450Z-speckit-review", "20261020T131909Z-speckit-implement", "20261021T090002Z-speckit-requirements", "20261021T092729Z-speckit-clarify", "20261021T105335Z-skill-improve-skills", "20261021T111429Z-speckit-requirements", "20261021T111631Z-skill-improve-skills", "20261021T115006Z-speckit-clarify"]
supersedes: "introspection-20261021T130154Z"
confirmed_at: "2026-10-21T13:51:54Z"
---

# Introspection Report: introspection-20261021T133447Z

范围：本地库 **70** 条 open 条目（全部 `kind: internal`；0 个待处理入站包）。本仓戴**框架帽子**——根级 `templates`、`skills`、`shared`、`scripts`、`src/specify_cli` 五源目录俱在；全部分流恒为 `local-sink(<channel>)`。本报告 **supersedes introspection-20261021T130154Z**：首次盘点误用 `--action list --disposition open` 的默认 limit，只读到 5/70 条；用 `--limit 0` 取全量后以本报告纠正。运行期间新写入的 `20261021T130319Z-speckit-plan` 不进入本次范围。

核验方式：按亲和度分 6 组（requirements / clarify / plan+tasks / checklist+analyze+instructions / implement+review / skills），派 6 个新鲜上下文只读 verifier，逐条回读框架根级源并给 `path:line` 证据；5 组回报“未发现异常”，2 条 ANOMALY 已分别落入 F-03/F-04 与元观察 M-2。未以 `.specify/` 镜像为权威。

覆盖核对：范围 **70** = 问题成员 **27** + Excluded **43**，恰好覆盖一次。分流分布：`direct-fix` 1（F-02，已执行）、`speckit-requirements` 1（F-01）、`improve-skills` 14（其余 findings）。

## 元观察（不属任何单一条目，由 A4 单独分流并落 backlog）

- **M-1（本轮最高优先，流程缺陷）**：`feedback-utils.py --action list --disposition open` 的默认 limit 会把 70 条截成 5 条；A3 的盘点命令未带 `--limit 0`，本轮因此先产出 5 条报告并误处置 2 条。需把 open 盘点默认改为全量，或在 A3 命令与技能中强制 `--limit 0` 并加反截断哨兵。路由 `improve-skills`（feedback 引擎/消化流程），owner `scripts/python/feedback-utils.py`、`skills/internal/manage-feedback/references/path-a-digest.md`。
- **M-2**：`shared/workflow/objective-analysis-gate.md:39` 的绑定发现命令 `grep templates/commands/` 在当前树返回空集，实际指针在 `skills/`；`tests/contract/test_objective_analysis_gate.py:56-65` 仍钉住该形态。路由 `improve-docs`，owner 上述两文件。

## Findings

### F-01: 父规格 FR 引用被 pre-analyze-check 一律判为 dangling，而 validate-requirements 又禁止切片复用父编号

- **根因**: `pre-analyze-check.py` 的 `check_references` 只把本地 `requirements.md` 定义的 `FR-NNN` 视为已定义；`FR` 前缀被排除在契约条款的 `external-clause` advisory 之外，切片正文里的父规格 `#FR-NNN` 一律报 `dangling-id` error；同时 `validate-requirements.py` 的 `id-contiguous` 要求本地 FR 编号自 001 连续，切片不能复用父编号，只能把精确映射降级到 notes（066 的实际绕行）。
- **证据锚点**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:181-185,201-203`；`scripts/python/validate-requirements.py:119-146`；`.specify/specs/066-loop-state-awareness-a/notes/parent-fr-mapping.md:6-18`。
- **成员条目**: 20261021T111429Z-speckit-requirements(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 为 `pre-analyze-check.py` 增加父规格输入（如 `--parent-requirements`）或声明式 `Parent FR` 映射段，把父 FR 引用降为 `external-fr` advisory（与 `external-clause` 同构），并同步 `efficiency-model.md` §6 与单测；次生根 token-efficiency：以既有 slice spec 为惯例样本时只读目标 heading/FR 摘录，不整篇注入上下文。
- **建议处置**: 20261021T111429Z-speckit-requirements:processed

### F-02: Feature bind-or-create 归属在 feature-integration.md 与 create-requirements/clarify 之间未收敛

- **根因**: `feature-integration.md` 仍把 bind-or-create 归 `/speckit.requirements`（标题 “requirements phase”、状态表 Notes “Feature binding only”），而 `create-requirements/SKILL.md` 明确本技能不绑定、推迟到 `/speckit.clarify`，`clarify-taxonomy.md` 的 Feature Linkage 又要求 clarify 提案绑定——三处对“谁绑定”未收敛；同一条目的拆分门点已由 `stage-prompts.md:79` 落实，属执行遗漏而非源缺口。
- **证据锚点**: `shared/workflow/feature-integration.md:33,55-70`；`skills/internal/create-requirements/SKILL.md:146-151`；`shared/constants/clarify-taxonomy.md:11-15,83-85`；`skills/external/sdd-loop-driver/references/stage-prompts.md:79`。
- **成员条目**: 20261021T092729Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 本 run 已把 `feature-integration.md` § Feature Binding Rules 改为 clarify checkpoint、状态表 requirements 行注明 binding deferred to `/speckit.clarify` Mode A，并同步 shared 镜像；`test_review_p1_review_loop.py` 通过，`test_neutrality_budget.py` 的 3 个失败与干净基线一致（零回归）；拆分门无需改源。
- **建议处置**: 20261021T092729Z-speckit-clarify:processed

### F-03: compile-embeds 读 .specify 镜像早于 sync，且镜像漂移已累积

- **根因**: `compile-embeds` 从 `.specify` 镜像注册表读取，而 `probe.md` 的固定顺序把 compile 排在 sync 之前；源侧更新后若未先 sync，会编译旧内容；实测 HEAD 与镜像在 shared/skills 大量文件上不一致，漂移会持续放大。
- **证据锚点**: `scripts/python/probe-utils.py:131,167-168,226`；`docs/reference/skills/probe.md:28-32`；`scripts/python/sync-mirrors.py:125`；`skills/internal/implement-feature/SKILL.md:207-210`。
- **成员条目**: 20261020T041125Z-speckit-plan(部分成立), 20261016T054516Z-speckit-implement(部分成立), 20261019T184312Z-speckit-implement(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把文档工序改为 sync → regen → compile（或让 compile 读规范源而非镜像）；在 implement/tasks 的 U4 增加镜像一致性前置检查；对已漂移的镜像执行一次受控 sync 并加 `--check` 回归测试。
- **建议处置**: 20261020T041125Z-speckit-plan:processed, 20261016T054516Z-speckit-implement:processed, 20261019T184312Z-speckit-implement:processed

### F-04: create-tasks 仍把 Test runs 指向不存在的 implement.md 锚点

- **根因**: `create-tasks` 的 `**Test runs**` 仍指向 `templates/commands/implement.md`，该文件 0 处匹配；`.specify/templates/commands` 已退役，正确 owner 是 `skills/internal/implement-feature/SKILL.md`；契约测试还钉住了错指针。
- **证据锚点**: `skills/internal/create-tasks/SKILL.md:364-365,432-433`；`templates/commands/implement.md`（0 匹配）；`skills/internal/implement-feature/SKILL.md:178`；`tests/contract/test_validate_tasks_parallel_safety.py:66`。
- **成员条目**: 20261016T043010Z-speckit-tasks(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把指针改到 `skills/internal/implement-feature/SKILL.md` 的 Test runs 节，并同步更新契约测试；加一条 grep 断言防止再次指向退役目录。
- **建议处置**: 20261016T043010Z-speckit-tasks:processed

### F-05: 契约条款形态前置缺失，C-EC 子句对覆盖核算不可见

- **根因**: `create-plan` 的 contracts 指引只讲 OpenAPI/GraphQL，未声明 clause id 必须为 `C-\d+`；`clause_extract.py` 只认 `C-N`，非 C-N 前缀会被 downstream 拒绝；`account-clause-coverage.py` 又不把 `C-EC-xx` 类子句纳入覆盖。
- **证据锚点**: `skills/internal/create-plan/SKILL.md:227-236`；`scripts/python/clause_extract.py:46-56`；`scripts/python/account-clause-coverage.py:381-384`；`tests/contract/test_validate_tasks_parallel_safety.py`。
- **成员条目**: 20261016T112548Z-speckit-tasks(成立), 20261018T013204Z-speckit-tasks(部分成立), 20261018T034058Z-speckit-review(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 `create-plan` Phase 1/后置门增加“clause id 形态以 clause owner 为准（C-N）”的前置提示；扩展 `clause_extract.py`/`account-clause-coverage.py` 支持 C-EC-xx（作为 `/speckit.requirements` 候选）并补测试。
- **建议处置**: 20261016T112548Z-speckit-tasks:processed, 20261018T013204Z-speckit-tasks:processed, 20261018T034058Z-speckit-review:processed

### F-06: validate-tasks 的 PATH_TOKEN 把 URL/版本号/百分比/中文枚举误判为路径，导致 parallel-safe 误报

- **根因**: `PATH_TOKEN` 的正则把含 `/` 的 `URL/版本号`、`百分比/版本号/...` 等文本当路径（`\w` 含 CJK），默认判为写目标，触发 parallel-safe 误报。
- **证据锚点**: `scripts/python/validate-tasks.py:83-84,243`。
- **成员条目**: 20261019T085937Z-speckit-tasks(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 收紧启发式——排除 CJK 斜杠枚举、URL、版本号与百分比，或要求扩展名/已知目录前缀；补正反例单测。
- **建议处置**: 20261019T085937Z-speckit-tasks:processed

### F-07: checklist 仍整读 requirements、缺最小投影与机械锚点/排序检查

- **根因**: 按 FR 分派时每个检查项仍读同一份完整 `requirements.md`，重复发现且烧 token；`create-checklist` 步骤 4 无最小加载/投影；锚点漂移与 risk/impact 排序只有散文规则，无机械检查；确定性证据包未接入。
- **证据锚点**: `shared/workflow/objective-analysis-gate.md:21`；`skills/internal/create-checklist/SKILL.md:66-83,104`；`scripts/python/account-clause-coverage.py:31-39`；`shared/guidelines/checklist-methodology.md:95`。
- **成员条目**: 20261018T014641Z-speckit-checklist(成立), 20261019T134009Z-speckit-checklist(成立), 20261019T172529Z-speckit-checklist(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 按 FR 生成最小投影（只带该 FR 及其引用），增加锚点存在性与排序的机械检查，并把证据包接入 checklist 输出。
- **建议处置**: 20261018T014641Z-speckit-checklist:processed, 20261019T134009Z-speckit-checklist:processed, 20261019T172529Z-speckit-checklist:processed

### F-08: common.sh 硬依赖 cws-lib-bash，缺少宿主时脚本直接失败

- **根因**: `common.sh` 在无 cws-lib-bash 的环境下无法运行，checklist 等命令因此失败；没有可移植 fallback 或显式前置检查。
- **证据锚点**: `scripts/bash/common.sh:13-29`。
- **成员条目**: 20261019T081434Z-speckit-checklist(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 增加可移植 fallback 或明确的前置检查与错误信息，并在无 cws-lib-bash 的宿主上补一条集成测试。
- **建议处置**: 20261019T081434Z-speckit-checklist:processed

### F-09: AVAILABLE_DOCS 不含 notes/ 与 baseline-*，review 只能手工遍历

- **根因**: `check-prerequisites.sh` 构造的 AVAILABLE_DOCS 没有 `notes/` 与 `baseline-*`；`review-sdd-process` 需要这些实现期证据时只能手工 walk，遗漏风险高。
- **证据锚点**: `scripts/bash/check-prerequisites.sh:244-251`；`skills/internal/review-sdd-process/SKILL.md:51,91-92`。
- **成员条目**: 20261016T061443Z-speckit-review(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把 `notes/` 与 `baseline-*` 纳入 AVAILABLE_DOCS（或让 review 显式消费），并更新 preflight 输出契约。
- **建议处置**: 20261016T061443Z-speckit-review:processed

### F-10: feedback/probe 收尾契约缺报告骨架、记账边界与执行顺序

- **根因**: `path-a-digest.md` 只给报告 schema 的散文，没有可复制的骨架，消费方需从引擎文法反推；Create-Requirements 的 Feedback Record 面与命令模板的记账单元描述不一致；编译面 Handler order 把 Record(20) 排在 Reflection(40) 之前，与“先自省再 Persist”相反；教训文档只写了 `cp` 别名安全，未覆盖 `rm` 变体。
- **证据锚点**: `skills/internal/manage-feedback/references/path-a-digest.md:102`；`scripts/python/feedback-utils.py:481`；`docs/reference/history/00-cross-cutting-lessons.md:38-40`；`shared/workflow/feedback-step.md:88,141`；`shared/definitions/probe-definitions.md:203,205`；`skills/internal/create-requirements/SKILL.md:165,175`。
- **成员条目**: 20261015T090816Z-skill-manage-feedback(部分成立), 20261016T025641Z-skill-create-requirements(部分成立), 20261016T025641Z-speckit-requirements(部分成立), 20261018T002011Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 `path-a-digest.md` 内嵌一份可直接复制的报告骨架；统一 Create-Requirements 的记账边界措辞；把 Record 调整到 Reflection 之后或明确记录例外；教训文档补齐 `rm` 变体并加反向用例。
- **建议处置**: 20261015T090816Z-skill-manage-feedback:processed, 20261016T025641Z-skill-create-requirements:processed, 20261016T025641Z-speckit-requirements:processed, 20261018T002011Z-speckit-requirements:processed

### F-11: run-determination 的 (unit_id, run_id) 幂等锁使漏源记录无法补测

- **根因**: 同一 `(unit_id, run_id)` 的重复记录会被直接拒绝；当首次运行缺少 session/source 参数时，后续拿到源也无法补测，只能保留 `not_evaluated`。
- **证据锚点**: `scripts/python/run-determination.py:1413-1442,1482-1483`。
- **成员条目**: 20261019T114446Z-speckit-review(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 增加仅补 source 的 settle/append 路径（不重跑判定），或允许显式 `--refresh-sources` 并保留原记录审计；补幂等测试。
- **建议处置**: 20261019T114446Z-speckit-review:processed

### F-12: create-requirements 缺分支复用开关与 Assumptions/重叠模板槽

- **根因**: `create-new-requirements.sh` 无条件 `git checkout -b`，无复用开关；`requirements-template.md` 没有 Assumptions 槽，也没有跨特性重叠节；guidelines 引用了不存在的节。
- **证据锚点**: `scripts/bash/create-new-requirements.sh:265`；`templates/requirements-template.md:1,6`；`shared/guidelines/requirements-guidelines.md:117`。
- **成员条目**: 20261019T163355Z-speckit-requirements(部分成立), 20261020T033719Z-speckit-requirements(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 增加 `--reuse-branch` 与显式创建/复用二选一；模板补可选 Assumptions 与跨特性重叠节；补脚手架与模板测试。
- **建议处置**: 20261019T163355Z-speckit-requirements:processed, 20261020T033719Z-speckit-requirements:processed

### F-13: implement-feature 的 P0 门只在触发时留证，计划前提被证伪时无处置程序

- **根因**: P0 审计只在存在未解决项时要求证据，门控未触发时没有“必须留下执行证据”的义务；计划前提被证伪时只覆盖 gate/DoD 行与用户指令，没有声明的处置程序。
- **证据锚点**: `skills/internal/implement-feature/SKILL.md:61-76,262,330`。
- **成员条目**: 20261019T191328Z-skill-sdd-loop-driver(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 无论门控是否触发都记录一次审计证据（分母/比较结果）；增加“计划前提被证伪”的显式分支与状态脊字段。
- **建议处置**: 20261019T191328Z-skill-sdd-loop-driver:processed

### F-14: manage-instructions 可控正文约 7860 tokens 超 5000，跨技能 R3 归属未决

- **根因**: `manage-instructions` 超出 skill-shape 的 5000 预算；sdd-project-setup 的 R3 回退只覆盖 project-filled 章节，跨技能 R3 的 owner 未裁定。
- **证据锚点**: `skills/external/sdd-project-setup/SKILL.md:67,78`；`skills/external/sdd-project-setup/references/setup-recipes.md:98-109`；`skills/external/improve-skills/scripts/skill-shape.py:27`。
- **成员条目**: 20261020T031448Z-skill-improve-skills(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 裁定 R3 的单一 owner（manage-instructions 或 setup），对 `manage-instructions` 做一次定向瘦身/外迁，并补跨技能预算契约测试。
- **建议处置**: 20261020T031448Z-skill-improve-skills:processed

### F-15: clarify/create-plan 仍规定全量索引 grep，无人值守说明缺失

- **根因**: `clarify-artifact` 与 `create-plan` 仍有“grep 全量索引”的步骤，与 token-efficiency 的定向检索纪律冲突；clarify 的无人值守运行形态没有说明。
- **证据锚点**: `skills/internal/clarify-artifact/SKILL.md:65-66`；`skills/internal/create-plan/SKILL.md:180-181`。
- **成员条目**: 20261019T164049Z-speckit-clarify(部分成立), 20261020T034718Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把全量索引 grep 改为按 feature/unit 的定向检索，并补一段无人值守（自裁决 + 记录假设）形态说明。
- **建议处置**: 20261019T164049Z-speckit-clarify:processed, 20261020T034718Z-speckit-clarify:processed

### F-16: implement 模板仍允许整文件转储 records.jsonl

- **根因**: `templates/commands/implement.md` 的量化采集段允许整行读取 `records.jsonl`，而不是走 `exec-quant.py` 的 `list-records` 投影，违反摘要优先纪律。
- **证据锚点**: `templates/commands/implement.md:52-55`；`scripts/python/exec-quant.py:1082-1140`。
- **成员条目**: 20261019T103809Z-speckit-implement(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 改为只调用 `list-records`/摘要投影，明确禁止整文件转储，并补一条 token-efficiency 检查。
- **建议处置**: 20261019T103809Z-speckit-implement:processed

## Excluded

- 20261016T083949Z-speckit-requirements — Consumed-by 校验的正面记录，条目自述无需改判据。
- 20261019T071229Z-speckit-requirements — 条目自述无显著优化点。
- 20261021T090002Z-speckit-requirements — 条目自述无显著优化点。
- 20261016T031322Z-speckit-clarify — 编译 Wrap-up 参数缺口已由后续提交修复。
- 20261016T102726Z-speckit-clarify — 5 候选合并 4 问属既有上限内的批处理，无缺陷。
- 20261018T002912Z-speckit-clarify — 条目自述零优化点。
- 20261018T002921Z-skill-clarify-artifact — 条目自述零优化点。
- 20261019T072038Z-speckit-clarify — 一次畸形 grep 重试属运行级操作，无框架缺陷。
- 20261019T083518Z-speckit-clarify — 唯一摩擦与已修的引擎参数条目同源。
- 20261019T125018Z-speckit-clarify — 必填参数已修；simple 跳过属设计；双语检索属通用实践。
- 20261021T115006Z-speckit-clarify — 优化点栏是绑定 065 与五项裁决冻结的运行记录。
- 20261016T040553Z-speckit-plan — 三点均为运行期自我纠偏，Summarize-after 规则已在位。
- 20261016T110804Z-speckit-plan — 仅未来条款计数由测试派生的增强意向，无当前缺陷。
- 20261018T011402Z-speckit-plan — 本机缺 pytest 属环境供给，runner 已有解释器阶梯与显式报错。
- 20261019T075055Z-speckit-plan — 编译 Wrap-up 调用已与引擎契约一致。
- 20261019T080718Z-speckit-tasks — tasks 命令/技能编译面均已带全参数。
- 20261019T085059Z-speckit-plan — 全角括号引用组已由双宽度扫描支持。
- 20261019T131539Z-speckit-plan — 条目明示无显著优化点。
- 20261019T133435Z-speckit-tasks — 063 quickstart 已改用 --complexity complex。
- 20261019T170645Z-speckit-plan — 评审结果记录，22 项已原位关闭。
- 20261020T042203Z-speckit-tasks — 仅记录 tasks 落盘与提交，无缺陷。
- 20261016T122911Z-speckit-analyze — 效果实证，非缺陷。
- 20261018T015912Z-speckit-analyze — 编译面参数缺口已由后续提交修复。
- 20261019T140016Z-speckit-analyze — 同族参数缺口已修复；[P] 漂移属 063 产物级。
- 20261019T164539Z-speckit-instructions — 执行策略/权限分类器观察，非框架源缺陷。
- 20261020T043644Z-speckit-checklist — 均为 064 需求产物级 gate findings。
- 20261020T044640Z-speckit-analyze — 064 规格内发现；I-11 前提不成立（sync-mirrors 已有 --only）。
- 20261020T050419Z-speckit-analyze — 064 复跑结果/遗留项，无框架级缺陷。
- 20261016T061518Z-skill-review-sdd-process — 条目自述无独立摩擦。
- 20261016T174959Z-speckit-implement — 规则已在任务面且执行到位。
- 20261018T030254Z-skill-implement-feature — compile-embeds --write 前提错误，该 flag 从不存在。
- 20261020T130450Z-speckit-review — P0 分母缺陷已修并补测试。
- 20261020T131909Z-speckit-implement — 分解门/重叠预检/TIMEOUT 纪律均已在 driver 落地。
- 20261019T190639Z-speckit-review — P0 审计分母已修；F2–F9 为 063 特性本地发现。
- 20261016T080252Z-skill-git-utils — 纯运行结果，无框架级缺陷。
- 20261016T180912Z-skill-improve-skills — 仅观察结论；flags-outside-contract 属 warn 级信号。
- 20261019T063816Z-skill-improve-skills — 窗口 RUNNING/deadline/TIMEOUT 与 PID+start ticks 规则均已落地。
- 20261019T063837Z-skill-improve-skills — probe object 已注册；命名沿用旧 id 属遗留观察。
- 20261019T065041Z-skill-improve-skills — U0/U0.5/HR7/误路由表已在位。
- 20261019T122920Z-skill-sdd-loop-driver — 模板收尾已带占位参数；术语/REC/证据/基线均有归属。
- 20261020T023920Z-skill-git-utils — 纯合并/推送操作记录。
- 20261021T105335Z-skill-improve-skills — S0 缺省表与本地拓扑已在位（C-15）。
- 20261021T111631Z-skill-improve-skills — U0 缺省表与本地 MUST NOT qodercli 已在位（C-23）。
