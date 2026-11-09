---
id: "introspection-20261108T192504Z"
created: "2026-11-08T19:25:04Z"
status: "confirmed"
scope_filter: "disposition=open --limit 0 --format json (33 entries; framework hat; 0 pending bundles)"
scope_entries: ["20261106T105455Z-skill-review-sdd-process", "20261106T105450Z-speckit-review", "20261106T103903Z-speckit-review", "20261106T101220Z-skill-code-review", "20261106T101220Z-skill-review-feature-quality", "20261106T101220Z-skill-review-sdd-process", "20261106T101205Z-speckit-review", "20261106T093919Z-speckit-implement", "20261106T093856Z-speckit-implement", "20261106T090634Z-speckit-analyze", "20261106T085558Z-speckit-checklist", "20261106T084954Z-skill-manage-feedback", "20261106T084949Z-speckit-feedback", "20261106T080417Z-speckit-review", "20261106T075313Z-speckit-analyze", "20261106T074439Z-speckit-checklist", "20261106T074249Z-speckit-checklist", "20261106T073834Z-speckit-tasks", "20261106T073737Z-speckit-tasks", "20261106T071933Z-speckit-plan", "20261106T071005Z-speckit-plan", "20261106T065222Z-speckit-plan", "20261106T063214Z-speckit-clarify", "20261106T062511Z-skill-create-requirements", "20261106T062127Z-speckit-requirements", "20261106T062117Z-speckit-requirements", "20261106T045013Z-speckit-analyze", "20261106T043933Z-speckit-checklist", "20261106T043324Z-speckit-tasks", "20261106T042459Z-speckit-plan", "20261106T041409Z-speckit-clarify", "20261106T041358Z-speckit-clarify", "20261106T040836Z-speckit-requirements"]
supersedes: ""
confirmed_at: "2026-11-09T01:56:19Z"
---

# Introspection Report: introspection-20261108T192504Z

范围：本地反馈库全部 33 条 open 条目（`--limit 0`；全部 `kind: internal`；0 个待处理入站包；框架帽子，Path A）。本轮同时修正初次盘点因默认 `--limit 5` 造成的范围截断。
核验方式：按 unit 亲和性分 5 组只读核验，逐条对照当前框架源码与活规格（2026-11-06 之后的 087/088 交付）；一条目只归属一个问题，次要根因写入该问题的优化方案。

## Findings

### F-01: Review 的逐维结论与闭包分母缺少可读槽位
- **根因**: review 模板只提供 coverage 与单一 segment verdict；逐维 verdict 行、从 changed files 派生闭包套件集、以及 run-determination 接受同键补充证据都只存在于散文，执行者只能手工复核。
- **证据锚点**: `templates/review-template.md:98-107`；`skills/internal/review-feature-quality/SKILL.md:58`；`skills/internal/code-review/SKILL.md:59-85`；`scripts/python/closure-acceptance-check.py:1776-1795,218-231`；`scripts/python/run-determination.py:1483,1519-1548`。
- **成员条目**: 20261106T080417Z-speckit-review(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 在 review 模板增加「每维一行 verdict」与段级闭包分母字段；closure 检查接受 changed-files 派生的套件集；run-determination 接受同键补充证据（次生根，标注）；若需新机制而非模板修补，转 speckit-requirements。
- **建议处置**: 20261106T080417Z-speckit-review:processed

### F-02: verification.md 是收尾产物而非阶段前置
- **根因**: implement 在 Step 9 才填充 verification.md，expression-gates 又声明它 never a stage input，review 的 U4 没有可消费的种子。
- **证据锚点**: `skills/internal/implement-feature/SKILL.md:319-331`；`shared/workflow/expression-gates.md:38`。
- **成员条目**: 20261106T101205Z-speckit-review(成立), 20261106T101220Z-skill-review-sdd-process(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 在 implement 起点 seed verification.md 骨架，并把「review U4 读取 seed」写入 gate；同步 review-sdd-process 的前置检查。
- **建议处置**: 20261106T101205Z-speckit-review:processed, 20261106T101220Z-skill-review-sdd-process:processed

### F-03: quickstart S3 的 mtime 步骤只写在注释、未进入可执行命令
- **根因**: S3 step 3 打印的 `mktemp -d` + `cp -R` 不调用 `helpers.apply_mtime_step`，三面 mtime 相同，实际返回 satisfied 而块内预期 stale；`mktemp -d` 还使用了裸系统临时根。初次报告 F-02 的「已过时」结论过宽，该残差仍在。
- **证据锚点**: `.specify/specs/087-arch-diagram-docs/quickstart.md:169-175`；`.specify/specs/087-arch-diagram-docs/review.md:39,85`；`tests/fixtures/docs-obligation/conftest.py:71`。
- **成员条目**: 20261106T105450Z-speckit-review(部分成立), 20261106T093856Z-speckit-implement(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 在 S3 step 3 的可执行命令中插入显式 mtime 步骤（调用 `apply_mtime_step` 或等价的 `touch -d` 序列），并把 `mktemp -d` 改为 `.specify/.tmp/` 或 `~/tmp/<project>/` 的受制裁根；同时修正初次报告 F-02 的结论。
- **建议处置**: 20261106T105450Z-speckit-review:processed, 20261106T093856Z-speckit-implement:processed

### F-04: plan-edit 声明面缺失（review-sdd-process 观察）
- **根因**: scratch 根规则已在 temp-directory-discipline 在位；但 review-sdd-process 要求「plan-edit declarations current」时没有对应声明面或检查器。
- **证据锚点**: `shared/guidelines/temp-directory-discipline.md:12,53`；`skills/internal/review-sdd-process/SKILL.md`（无 plan-edit 指针）；`grep -r "plan-edit\|plan-owned"` 零命中。
- **成员条目**: 20261106T105455Z-skill-review-sdd-process(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 review-sdd-process 增加对 loop-driver `PLAN-EDIT:` 声明面的读取义务与缺失处置；若声明面应由 loop-driver 提供，作为 improve-skills 的 loop-driver 子项。
- **建议处置**: 20261106T105455Z-skill-review-sdd-process:processed

### F-05: 缺少「出厂技能必须经分发引用触达规范 schema」的作者规则
- **根因**: create-skills 只约束 `${SKILL_HOME}` 与 standalone `.specify/**`，没有要求 shipped skill 通过分发引用（而非 spec-local 链接）触达 normative schema；create-docs 的 F26 实例已修，但规则未立。
- **证据锚点**: `skills/external/create-skills/SKILL.md:70,166`；`skills/external/create-docs/SKILL.md:61,75`；`skills/external/create-docs/references/diagram-obligation.md:10`。
- **成员条目**: 20261106T101220Z-skill-review-feature-quality(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 create-skills 增加「normative-schema reachability」规则：shipped skill 只能通过 `references/` 分发面引用规范，禁止 spec-local 链接；补一条契约守卫。
- **建议处置**: 20261106T101220Z-skill-review-feature-quality:processed

### F-06: runtime-stack 义务未在 requirements 调用面显形
- **根因**: `validate-requirements.py` 不判 runtime-stack 表；`pre-analyze-check` 在 requirements 阶段阻塞但 create-requirements 只调 validator；gate 错误只报「缺 §」不报行 schema；create-requirements 无 runtime-stack 指针。
- **证据锚点**: `scripts/python/validate-requirements.py:79,484`；`shared/workflow/expression-gates.md:44`；`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:587,1319`；`skills/internal/create-requirements/SKILL.md`（无 runtime-stack 指针）；`shared/workflow/acceptance-hardening.md:267-330`。
- **成员条目**: 20261106T040836Z-speckit-requirements(部分成立), 20261106T062511Z-skill-create-requirements(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 让 validator 的 label 集与 gate 错误文本指向 acceptance-hardening 的 runtime-stack 行 schema；create-requirements 增加 summary-first 指针；`--help` 注明 path-marker 触发条件；编号 override 入口作为次生根标注。
- **建议处置**: 20261106T040836Z-speckit-requirements:processed, 20261106T062511Z-skill-create-requirements:processed

### F-07: owner 文档与测试整读、重复读
- **根因**: create-requirements 只对 sample spec 限定了 bounded reading；token-efficiency 没有 owner 文档/测试的 outline-first 规则；069a 测试按 slice 重开。
- **证据锚点**: `skills/internal/create-requirements/SKILL.md:80-86`；`shared/guidelines/token-efficiency.md:52`；`skills/internal/create-plan/SKILL.md:65-67`。
- **成员条目**: 20261106T062127Z-speckit-requirements(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 token-efficiency 增加「owner 文档/测试先 outline 后定点读」的 rung，并在 create-requirements/create-plan 接线。
- **建议处置**: 20261106T062127Z-speckit-requirements:processed

### F-08: clarify taxonomy 缺少「既有 owner 文档与义务冲突」类目
- **根因**: same-author 检测已要求委托，但 `clarify-taxonomy.md` 没有该冲突类，导致该类问题只能靠自由裁量。
- **证据锚点**: `skills/internal/clarify-artifact/SKILL.md:81-90`；`shared/constants/clarify-taxonomy.md:67-75`；`shared/workflow/objective-analysis-gate.md`。
- **成员条目**: 20261106T041358Z-speckit-clarify(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 clarify taxonomy 增加 conflict 类目与判定句式；同步 clarify-artifact 的扫描步骤。
- **建议处置**: 20261106T041358Z-speckit-clarify:processed

### F-09: 调用面前置条件/参数不可见（裸解释器、编译行省略 --feature）
- **根因**: sync-mirrors/regen 用 `sys.executable` 委托子进程，裸解释器缺依赖时伪造 DRIFT exit 2；compiled wrap-up 行省略可选 `--feature/--feature-id`，引擎接受空值，条目丢失归属。
- **证据锚点**: `scripts/python/sync-mirrors.py:215-224`；`scripts/python/regen-command-copies.py:35-40`；`src/specify_cli/__init__.py:36,39-40`；`templates/commands/tasks.md:74`；`skills/internal/create-tasks/SKILL.md:448`；`scripts/python/feedback-utils.py:2657-2661`。
- **成员条目**: 20261106T065222Z-speckit-plan(成立), 20261106T073834Z-speckit-tasks(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 在 sync-mirrors/regen 委托前加依赖/import preflight（失败给出显式 `preflight-missing`，不伪造 DRIFT）；在编译行渲染 `--feature/--feature-id` 或明确的可选占位；requirements 整读作为次生根并入 F-07。
- **建议处置**: 20261106T065222Z-speckit-plan:processed, 20261106T073834Z-speckit-tasks:processed

### F-10: 咨询式检查（WARN/软上限/清单前提）没有机器可判的闭包
- **根因**: task checker 的 `green-*` WARN 每次要求人工散文裁决；checklist 40 项软上限无溢出规则；CHK052 断言的需求字面量经核验不存在。
- **证据锚点**: `scripts/python/validate-tasks.py:39-52,558-568`；`templates/tasks-template.md:110`；`skills/internal/create-tasks/SKILL.md:111`；`.specify/specs/088-speckit-visualization/tasks.md:263`；`skills/internal/create-checklist/SKILL.md:104`；`shared/patterns/checklist-methodology.md:95`；`.specify/specs/088-speckit-visualization/requirements.md:655`；`.specify/specs/088-speckit-visualization/checklists/framework-visualization-2026-11-06.md:103,153`。
- **成员条目**: 20261106T043324Z-speckit-tasks(成立), 20261106T043933Z-speckit-checklist(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 给 WARN 增加结构化裁决块（decision + evidence + close 条件）；为 checklist 软上限增加 overflow 声明行；修正或删除 CHK052 的假前提；run-determination 参数形状并入 F-09。
- **建议处置**: 20261106T043324Z-speckit-tasks:processed, 20261106T043933Z-speckit-checklist:processed

### F-11: 条款覆盖按父名计数，而非按主题/头部声明
- **根因**: `account-clause-coverage.py` 与 `clause_extract.py` 只读 per-clause 引用括号；FR 声明在 contract 头部/代码段时被漏计；analyze skill 只要求「每个声称的映射为真」，未要求按主题映射。
- **证据锚点**: `scripts/python/account-clause-coverage.py:221-241,259-271`；`scripts/python/clause_extract.py:299,305-308`；`skills/internal/analyze-artifacts/SKILL.md:68-79`；`skills/internal/analyze-artifacts/references/detection-and-severity.md:28-30`；`.specify/specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md:5`。
- **成员条目**: 20261106T045013Z-speckit-analyze(部分成立), 20261106T075313Z-speckit-analyze(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 把条款覆盖从 name-keyed 改为 subject/header-keyed（或双读）；在 analyze skill 增加 heading-first contract index 与 subject-mapping 义务。
- **建议处置**: 20261106T045013Z-speckit-analyze:processed, 20261106T075313Z-speckit-analyze:processed

### F-12: 088 规格文本对 owner 侧事实的声明漂移
- **根因**: 088 requirements 声称 reader 按 record identity 去重，但 `exec-quant.py` 只是拼接；FR-023/FR-017 依赖未被 owner 声明的状态行/元素关系；8 份 088 contracts 头部仍写 `Feature: 087`（重编号残留）。
- **证据锚点**: `.specify/specs/088-speckit-visualization/requirements.md:697,488,445-450`；`scripts/python/exec-quant.py:1124-1127,1161-1174`；`.specify/specs/088-speckit-visualization/contracts/reporting-obligations.contract.md:3`。
- **成员条目**: 20261106T090634Z-speckit-analyze(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 修正 de-dup 声明或实现去重（二选一，需裁决）；为 FR-023/FR-017 补 owner 侧边界声明；批量修正 088 contracts 的 `Feature: 087` 残留（次生根，标注）。
- **建议处置**: 20261106T090634Z-speckit-analyze:processed

### F-13: check-prerequisites 缺显式 spec 选择（且条目前提有误）
- **根因**: `check-prerequisites.sh` 在 master 上回退到最高编号 spec，087/088 无法被选中；条目声称的「SyntaxError line 49」是把 bash 当 Python 解析的误判。
- **证据锚点**: `scripts/bash/check-prerequisites.sh`；`scripts/bash/common.sh:61-85`；`bash -n` 通过（含 `bd872308`）。
- **成员条目**: 20261106T085558Z-speckit-checklist(部分成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 为 check-prerequisites 增加显式 `--spec`/`SPECIFY_FEATURE` 选择并报错而非回退；在条目/报告中记录「SyntaxError」前提不成立。
- **建议处置**: 20261106T085558Z-speckit-checklist:processed

### F-14: implement 未消费 obligation JSON 的 summary-first 投影
- **根因**: implement 有通用 summary-first 规则，但没有 obligation 载荷的专用投影指令。
- **证据锚点**: `skills/internal/implement-feature/SKILL.md:78-84`；`skills/external/create-docs/scripts/docs-utils.py`（obligation payload）。
- **成员条目**: 20261106T093919Z-speckit-implement(部分成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 implement-feature 增加 obligation payload 的摘要投影（documents[].verdict 汇总 + 红项指针）。
- **建议处置**: 20261106T093919Z-speckit-implement:processed

### F-15: feedback 命令/技能执行面与引擎不一致
- **根因**: skill 把探针盘点写成 `feedback-utils.py --action probes/map`（实际属于 `probe-utils.py`）；inventory 命令省略 `--limit 0`，默认 5 条静默截断；Excluded 段条目没有处置通道；`introspect-register` 结构校验遇首个错误即停；finding 块不接受 notes 字段。
- **证据锚点**: `skills/internal/manage-feedback/SKILL.md:93-98`；`skills/internal/manage-feedback/references/path-a-digest.md:126`；`scripts/python/feedback-utils.py:2668,951,987-988,546,601,620-688,585-608`；`shared/definitions/probe-definitions.md:63`；`docs/reference/commands/feedback.md:29-33`；`docs/reference/skills/feedback.md:30`。
- **成员条目**: 20261106T084954Z-skill-manage-feedback(成立), 20261106T084949Z-speckit-feedback(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: ① 把探针命令改为 `probe-utils.py`（skill、probe-definitions、两份 docs）；② inventory/A3 快照加 `--limit 0`；③ 为 Excluded 条目增加 `建议处置` 通道或显式 A6 步骤（转 speckit-requirements 设计）；④ `introspect-register` 聚合全部结构违规后再退出（转 speckit-requirements）；⑤ finding 块增加 notes 字段（转 speckit-requirements）。次生根标注。
- **建议处置**: 20261106T084954Z-skill-manage-feedback:processed, 20261106T084949Z-speckit-feedback:processed

## Excluded

- 20261106T103903Z-speckit-review — 五点全部 ALREADY-FIXED（create-docs 死链、owner 双写、post_change_commit、FR-001 例外、S3/S5 记录名）。
- 20261106T101220Z-skill-code-review — fixture-builder `--check` 字节比较与未知 flag exit 2 已落地。
- 20261106T062117Z-speckit-requirements — 069a allowlist 条目已在位。
- 20261106T041409Z-speckit-clarify — features.md 投影读取已在 clarify-artifact 落地。
- 20261106T063214Z-speckit-clarify — 正向记录，无优化点。
- 20261106T042459Z-speckit-plan — 六门读数与修复已在 088 证据中。
- 20261106T071005Z-speckit-plan — attempt-2 修复已 closes。
- 20261106T071933Z-speckit-plan — attempt-3 已 closes。
- 20261106T073737Z-speckit-tasks — 76 行 / Tests Mode ON / gates exit 0，正向记录。
- 20261106T074249Z-speckit-checklist — OI-087-01 已 resolved。
- 20261106T074439Z-speckit-checklist — 规则已在位；残余是 compiled 行省略可选 flag（已由 F-09 承载）。
