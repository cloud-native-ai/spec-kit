---
id: "introspection-20261106T084116Z"
created: "2026-11-06T08:41:16Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (33 entries; framework hat; 0 pending bundles); the 5 entries digested in introspection-20261106T081504Z are already processed and out of scope"
scope_entries: ["20261105T034201Z-speckit-requirements", "20261105T034532Z-speckit-clarify", "20261105T041200Z-speckit-plan", "20261105T063435Z-speckit-tasks", "20261105T064151Z-speckit-checklist", "20261105T064532Z-speckit-analyze", "20261105T070132Z-speckit-analyze", "20261105T075137Z-speckit-requirements", "20261105T080203Z-speckit-clarify", "20261105T082017Z-speckit-plan", "20261105T083530Z-speckit-tasks", "20261105T084312Z-speckit-checklist", "20261105T085248Z-speckit-feedback", "20261105T085423Z-speckit-analyze", "20261105T094516Z-speckit-analyze", "20261105T111730Z-speckit-analyze", "20261105T133004Z-speckit-sanitize", "20261105T160210Z-speckit-review", "20261105T160214Z-skill-review-sdd-process", "20261105T160219Z-skill-review-feature-quality", "20261105T160226Z-skill-code-review", "20261105T071236Z-skill-improve-skills", "20261105T094753Z-skill-sdd-loop-driver", "20261105T130648Z-skill-sdd-house-keeping", "20261105T133034Z-skill-sanitize-materials", "20261106T040443Z-skill-create-requirements", "20261106T041131Z-skill-clarify-artifact", "20261106T042146Z-skill-create-plan", "20261106T044156Z-skill-create-tasks", "20261106T044619Z-skill-create-checklist", "20261106T045642Z-skill-analyze-artifacts", "20261106T041131Z-speckit-clarify", "20261106T042143Z-speckit-plan"]
supersedes: ""
confirmed_at: "2026-11-06T08:49:22Z"
---

# Introspection Report: introspection-20261106T084116Z

范围：本地库 33 条 open 条目（全部 `kind: internal`；0 个待处理入站包；框架帽子，Path A）。5 条更早的 open 条目已在 `introspection-20261106T081504Z` 处置，不在本报告范围。
核验方式：按亲和度分 6 组，派 fresh-context 只读 verifier 逐条回读根级框架源（`templates/`、`skills/`、`shared/`、`scripts/`、`src/specify_cli/`；`.specify/` 仅作运行时镜像）；22 条有可执行的根因，11 条为已修复/运行记录/非框架问题，列入 Excluded。

## Findings

### F-01: Deterministic validators disagree on clause, SC and stage forms and can pass unreadable input

- **根因**: 条款/SC/阶段形态在多个确定性引擎间没有单一文法；部分引擎对不可读或未覆盖输入仍打印 pass/0，且 requirements 模板缺 Runtime Stack 表，使跨产物门禁各按自己的字面量判定。
- **证据锚点**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:56,58,61,316`（SC 定义冒号、条款前缀、阶段名）；`scripts/python/validate-requirements.py:82`（无冒号要求）；`skills/external/sdd-loop-driver/scripts/audit-test-budget.py:41,316-319`（阶段名按 jsonl stem）；`scripts/python/validate-tasks.py:454-462`（md-none 契约无 green 声明面）；`scripts/python/account-clause-coverage.py:103,202`；`scripts/python/doc-consistency-check.py:1578-1591`（无逐事实 selector）；`templates/requirements-template.md:184` 与 `shared/workflow/acceptance-hardening.md:270`（Runtime Stack 表缺失）；`scripts/python/validate-decision-tensions.py:431-441`（不可读输入仍 pass/0）。
- **成员条目**: 20261105T034201Z-speckit-requirements(成立), 20261105T063435Z-speckit-tasks(部分成立), 20261105T082017Z-speckit-plan(成立), 20261105T083530Z-speckit-tasks(部分成立), 20261105T064532Z-speckit-analyze(部分成立), 20261105T085423Z-speckit-analyze(成立), 20261106T040443Z-skill-create-requirements(部分成立), 20261106T044156Z-skill-create-tasks(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 统一 SC/条款/阶段文法到单一声明并让每个引擎引用它；不可读输入与未覆盖项一律非零退出（禁止 pass/0）；pre-analyze 输出 `changed_paths[]`；requirements 模板补 Runtime Stack 表；GM 计数改为脚本行数断言；doc-consistency 增加逐事实 selector。
- **建议处置**: 20261105T034201Z-speckit-requirements:processed, 20261105T063435Z-speckit-tasks:processed, 20261105T082017Z-speckit-plan:processed, 20261105T083530Z-speckit-tasks:processed, 20261105T064532Z-speckit-analyze:processed, 20261105T085423Z-speckit-analyze:processed, 20261106T040443Z-skill-create-requirements:processed, 20261106T044156Z-skill-create-tasks:processed

### F-02: Test-budget fence and stage-status naming are not machine-enforced

- **根因**: plan 阶段不落两槽预算 fence，`audit-test-budget.py` 的阶段名按 `*.jsonl` stem 推导且只认六阶段，与八阶段序列不一致；ledger 行没有运行身份可自证。
- **证据锚点**: `skills/external/sdd-loop-driver/scripts/audit-test-budget.py:75-84,316-319`；`skills/external/sdd-loop-driver/references/efficiency-model.md:117`（六阶段）与 `shared/declarations/facts/driver-stage-sequence.yaml:14`（八阶段）；`skills/external/sdd-loop-driver/` 无 fence-seeding 规则。
- **成员条目**: 20261105T041200Z-speckit-plan(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: plan U4 写入预算 fence；阶段名改读 driver-stage-sequence；ledger 行增加 run-id/exit-code 字段并由写入器校验。
- **建议处置**: 20261105T041200Z-speckit-plan:processed

### F-03: Checklist cap and dispatch fallback are prose-only

- **根因**: checklist 的 40 条软上限无法覆盖 11 维 × 11 风险面，超出只能手写理由；objective-analysis gate 的无派发工具回退以「两次失败」为键，不认「本宿主无 dispatch 工具」；内联自检程序未产品化。
- **证据锚点**: `skills/internal/create-checklist/SKILL.md:89-117`（自检仅内联，目录只有 SKILL.md）；`skills/internal/create-checklist/SKILL.md:104` 与 `templates/commands/checklist.md:44`（上限未变）；`shared/workflow/objective-analysis-gate.md:27`（回退键）。
- **成员条目**: 20261105T064151Z-speckit-checklist(成立), 20261105T084312Z-speckit-checklist(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把自检程序落为脚本；允许 overage declaration 并纳入门禁输出；回退条件改为「宿主无 dispatch 工具」或「连续两次失败」两者之一。
- **建议处置**: 20261105T064151Z-speckit-checklist:processed, 20261105T084312Z-speckit-checklist:processed

### F-04: Owner criteria and completed-feature cross-references are incomplete

- **根因**: closed-set 声明的 3-conjunct 判据未进入 owner 指南；TB-05 的模块 stem 条款对 `.md` 路径退化；feature-details 的交叉引用规则只覆盖 `Implemented`，不覆盖 `Completed`。
- **证据锚点**: `shared/guidelines/closed-set-claims.md:14-31`；`skills/external/sdd-loop-driver/references/efficiency-model.md:108`；`templates/feature-details-template.md:96`。
- **成员条目**: 20261105T080203Z-speckit-clarify(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把 3-conjunct 封闭测试写入 owner；TB-05 条款限定 `.py`；交叉引用规则扩展到 `Completed`。
- **建议处置**: 20261105T080203Z-speckit-clarify:processed

### F-05: Feedback skill documents actions the engine lacks and the default list truncates

- **根因**: `manage-feedback` 的 routing flow 调用 `--action probes`/`map`，而 `feedback-utils.py` 没有这些 action；`list --disposition open` 默认每页 5 条，A1/A3 未强制 `--limit 0`，导致盘点静默截断。
- **证据锚点**: `skills/internal/manage-feedback/SKILL.md:93-96`；`scripts/python/feedback-utils.py:2596-2599`（action 闭集）与 `:2668`（默认 limit）；`scripts/python/probe-utils.py:1422`（probe 能力在另一引擎）；`skills/internal/manage-feedback/references/path-a-digest.md:126`。
- **成员条目**: 20261105T085248Z-speckit-feedback(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 删除/替换 probes/map 引用，指向 probe-utils 的真实入口；A1/A3 的盘点命令固定 `--limit 0`；把报告 schema 的严格性写入 skill。
- **建议处置**: 20261105T085248Z-speckit-feedback:processed

### F-06: Harness and sanitize engines print constants or misclassify paths

- **根因**: `harness-triple-check.py` 的 residual-literal 读数恒为常量；`closure-acceptance-check.py` 仍有内联 class 字面量；`sanitize-utils.py` 的 REPO_PATH_RE 未做边界锚定、`apply()` 把 dismiss 置为 resolved、占位符在 `<` 处被截断。
- **证据锚点**: `scripts/python/harness-triple-check.py:440-441,524`；`scripts/python/closure-acceptance-check.py:200,648,657`；`scripts/python/sanitize-utils.py:348,803-804,1020,364-365`；`.specify/specs/084-harness-triple-structure/contracts/harness-triple-check.contract.md:29-33,49-50`。
- **成员条目**: 20261105T160210Z-speckit-review(成立), 20261105T133034Z-skill-sanitize-materials(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 打印真实 residual literals 而非常量；把 class 字面量移入声明；REPO_PATH_RE/SKILL_REF_RE 加边界；修正 dismiss 状态机；占位符按完整 token 读取。
- **建议处置**: 20261105T160210Z-speckit-review:processed, 20261105T133034Z-skill-sanitize-materials:processed

### F-07: Clarify materiality bound lacks framework-observation routing

- **根因**: clarify 技能有 materiality bound，但没有把框架级观察路由到 improve 流的条款，观察只能留在运行记录里。
- **证据锚点**: `skills/internal/clarify-artifact/SKILL.md:79,88,132`。
- **成员条目**: 20261106T041131Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 增加「materiality 之外的框架观察 → improve 通道」路由条款，并给出记录位置。
- **建议处置**: 20261106T041131Z-speckit-clarify:processed

### F-08: Engine cross-run attribution and clause prefix handling

- **根因**: `exec-quant.py` 无 feature 标志且 arg 域为重复的封闭字面量；`run-determination.py` 会跨运行 settle 一个 tracked 记录；`pre-analyze-check.py` 的条款前缀不认规范 `C-NNN`；质量门在范围冲突后缺少语义裁定路径。
- **证据锚点**: `scripts/python/exec-quant.py:135,1441-1443,1466-1474`；`scripts/python/run-determination.py:1487-1491,1536-1544`；`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:58,61`；`skills/external/sdd-loop-driver/references/dispatch-recipes.md:168`。
- **成员条目**: 20261105T094753Z-skill-sdd-loop-driver(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: exec-quant 增加 feature 标志并消除重复字面量；跨运行 settle 需显式 opt-in；条款前缀接受 `C-NNN`；补语义冲突裁定路径。
- **建议处置**: 20261105T094753Z-skill-sdd-loop-driver:processed

### F-09: House-keeping surfaces lag and file reads truncate mid-token

- **根因**: `search-todo.py` 只解码前 8 KiB，跨多字节字符会抛 `UnicodeDecodeError`；history manifest 落后于会话；docs 根入口缺失且无声明。
- **证据锚点**: `scripts/python/search-todo.py:133-142`；`.specify/history/.manifest.json`（最后 processed_at 2026-08-15）；`docs/` 无根 index/README。
- **成员条目**: 20261105T130648Z-skill-sdd-house-keeping(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 按字节流解码或在截断处回退到字符边界；刷新 history manifest；为 docs 补根入口或把缺失登记为有意状态。
- **建议处置**: 20261105T130648Z-skill-sdd-house-keeping:processed

### F-10: Review record and receipt admit acknowledgement as judgement

- **根因**: receipt 默认把每个改动文件标为 `reviewed`，跳过调用方输入；code-review help 说四步而技能正文说五步；smoke 只有一个证据路径而 SC-001(i) 要求两次可比的运行；verification 的 baseline 未从 spine E2 复制；supporting 行永不关闭；finding-name 闭集与任务行缺失 carrier 无机械检查。
- **证据锚点**: `skills/internal/code-review/scripts/git-delta-review.sh:1067,1085-1086,1117-1125,1443`；`skills/internal/code-review/SKILL.md:67-77`；`shared/workflow/acceptance-hardening.md:93-101,73,244-246`；`templates/verification-log-template.md:73-75`；`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:30-32,1266-1268`；`.specify/specs/084-harness-triple-structure/tasks.md:31,166`。
- **成员条目**: 20261105T160214Z-skill-review-sdd-process(成立), 20261105T160219Z-skill-review-feature-quality(成立), 20261105T160226Z-skill-code-review(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: receipt 不默认 reviewed，要求逐文件 basis；help 与正文统一为五步；smoke 记录两次可比读数或说明为何只有一次；baseline 从 spine E2 复制；定义 supporting 行的关闭条件；finding-name 集合可配置；carrier 缺失即门禁红。
- **建议处置**: 20261105T160214Z-skill-review-sdd-process:processed, 20261105T160219Z-skill-review-feature-quality:processed, 20261105T160226Z-skill-code-review:processed

### F-11: Analyze method lacks dual-site and memory-write guard rules

- **根因**: analyze 的 remediation 段没有「双根因必须同时点名两个站点」规则；对 `.specify/memory` 的写入未要求运行 expression-compatibility guard。
- **证据锚点**: `skills/internal/analyze-artifacts/SKILL.md:152-158`；`skills/external/sdd-loop-driver/references/efficiency-model.md:107-116`；`tests/contract/test_expression_compatibility.py:70`。
- **成员条目**: 20261105T094516Z-speckit-analyze(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 增加 dual-site remediation 规则；在 memory 写入前强制 expression-compatibility guard。
- **建议处置**: 20261105T094516Z-speckit-analyze:processed

## Excluded

- 20261105T034532Z-speckit-clarify — 绑定与 wrap-up 已修复（`shared/workflow/feature-integration.md:73,78`；`templates/commands/clarify.md:48-62`）；advisory 增长是 pre-analyze 的预期行为。
- 20261105T075137Z-speckit-requirements — 运行质量自述，无可执行的框架缺陷。
- 20261105T133004Z-speckit-sanitize — 门禁观察记录，无改进请求。
- 20261105T071236Z-skill-improve-skills — ssh-utils 四项均已落地（`skills/external/ssh-utils/scripts/ssh-exec.py`）。
- 20261105T070132Z-speckit-analyze — 三项均已修复（`shared/guidelines/single-run-evidence.md:21-26,45-49`；`scripts/python/account-clause-coverage.py:311-315,610`）。
- 20261105T111730Z-speckit-analyze — clause (b) 按设计 base-independent，非缺陷。
- 20261106T041131Z-skill-clarify-artifact — 载体模式由宿主决定；并发为按阶段重算的设计。
- 20261106T042146Z-skill-create-plan — 优化点仅为裸数字「4」，无可核验命题。
- 20261106T042143Z-speckit-plan — 优化点仅为裸数字「4」，无可核验命题。
- 20261106T044619Z-skill-create-checklist — 纯运行记录，无框架缺陷。
- 20261106T045642Z-skill-analyze-artifacts — 条目记录的是该特性内部的 analyze 发现，非框架源缺陷。
