# Line State — 078-bilingual-expression

<!-- loop-state:begin -->
spine_state: completed
run_id: r20261030T081645Z-078a
slice: 078
stage: done
stage_started_at: 1793362200
stage_deadline_epoch: 1793367600
stage_base_commit: 878c03ab
attempt: 0
retry_limit: 2
last_verdict: MERGED to master at 308c7bef; closure rerun 21 failed / 6829 passed (exact baseline, zero new); budget audit status=ok (baseline:1 closure:1 reruns:1, stages=6 complete=6); line deregistered; Feature 078 = Ready for Review
<!-- plan-fence: decomposition=auto (plan/implement/review; slot_cap=2) test-budget=baseline@implement-start + closure@post-review; fast-lane=off (entry lacks fast-lane=opt-in) -->
<!-- loop-state:end -->

- line_id: `078-bilingual-expression`
- run_id: `r20261030T081645Z-078a`
- project_dir: `/storage/project/cloud-native-ai/spec-kit`
- repo_root: `/storage/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，单工作区）`
- base_sha: `7c835ba6`（master HEAD，077a 收尾后）
- trunk: `master`（`docs/git-workflow.md`；`main` 为上游世系，不参与合并）
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/storage/project/cloud-native-ai/spec-kit`）
- **执行拓扑**：本地（宿主原生子代理）
- **终态权威文档**：用户本轮需求（"双语表述"：所有核心概念、关键流程在定义名词和动词时使用中英双语形式，中文(English) 或 English(中文)，以在不同 context 与大语言模型中锚定语义）+ `.specify/memory/constitution.md` + `.specify/instructions.md` + `.specify/shared/workflow/glossary.md` + `.specify/memory/glossary.md` + `docs/`
- **特性切片**：Feature 078 —— **双语表述（Bilingual Expression）**：为核心概念与关键流程的定义建立双语表述约定（术语定义处中文(English) / English(中文)，括号语言随文档主语言），锚定跨 context / 跨模型的语义。**不拆片**：预期 FR ≤30、任务 ≤40；若拆分门判 `split-required` 再议。
- **用户裁决（2026-10-30）**：原文「中问」按「中文」理解（笔误）。既有框架已包含该概念、许多核心文档已实践（如 `Reserved Filenames (保留文件名)`、`**SDD 开发流程**（development flow）`、`程序优先 (Program-First)`）；本特性把该实践固化为可执行的约定与守卫。
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure（review 后全量）→ 工作树归档清扫 → 本地合并 master`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链（checklist / analyze / review 均必经）
- **拆解开关**：`decomposition: auto`；`decomposition_stages: plan=auto, implement=auto, review=auto`；`decomposition_slot_cap: 2`
- **测试预算**：implement 起点一次全量（baseline）、review 后一次 closure；中间用 `targeted-set-v1` 定向集
- **合并**：本地合并（缺省）；**不 push**（用户未授权）

## Preflight（run-agent dispatch-preflight）

| # | 检查 | 结论 |
|---|------|------|
| ① | SSH 连通性 | skip（本地拓扑） |
| ② | 非 root 运行用户 | skip（本地拓扑） |
| ③ | 子代理 CLI 可用性 | skip（本地拓扑；不启动外部 CLI） |
| ④ | 模型配置（execution-config resolve） | ok — `config_id=86c36fa253b12a57`，`mode=native`（host 原生子代理） |
| ⑤ | spec-kit 框架可用性 | ok — `.specify/` 与 `constitution.md` 在位（v1.15.0） |

## U1 断点探测（2026-10-30 08:16 UTC）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `master`（工作树干净） |
| 近期提交 | `7c835ba6 fix(instructions): slim template and live to the 32768 B budget` |
| Feature 注册 | 最大 077；**078 未登记** |
| spec 目录 | `.specify/specs/078*` 不存在 |
| 结论 | **断点 = requirements** |

## 类别观测（带日期，不充当取值来源）

- 2026-10-30 08:16 UTC：`flow-class-check.py --action lookup --unit-id "spec:078-bilingual-expression"` → exit 2，`flow_class: null`，`source: default`，`error: owner-unavailable`（spec 输入尚未创建）。requirements 派发载荷按此写：`flow_class=null; source=default; marker=; error=owner-unavailable`。
- requirements 完成后须重新解析本线声明行，与观测比对；不一致记 re-baseline。

## 阶段记录

### requirements

- attempt 0（2026-10-30 08:17 UTC）：dispatched → SDD Requirements Executor（40 回合预算）。
- attempt 0 结果：**预算触顶（U5）**。已落地：分支 `078-bilingual-expression`、spec 目录、未填充的模板 `requirements.md`；无提交、无 checklist、无登记。
- 可归因修复：执行者预算 40 → 改用 120 回合的 SDD Executor 容量；重入时跳过脚手架（脚本只运行一次），原地填充既有 requirements.md。
- attempt 1（2026-10-30 08:25 UTC）：dispatched → SDD Executor（120 回合），续跑 requirements。
- 简报：`.specify/.tmp/sdd-loop/tmp/078-bilingual-expression/brief-requirements.md`
- 哨兵：`REQUIREMENTS-DONE`
- **U4（驱动独立校验，2026-10-30 08:42 UTC）：PASS**
  - 哨兵：返回最后一行 `REQUIREMENTS-DONE`。
  - 产物：`requirements.md`（26 KB，Flow Class=expression / Flow Type=technique-document）、`checklists/requirements.md`、`features/078.md`、`features.md` 078 登记行；提交 `2fc9f22f` + `bb138fa2`。
  - 纪律：仅特性产物入提交；运行时记录（session/feedback/exec-quant）与状态脊保持未跟踪；无 push（分支无 upstream）。
  - 记账：`session/…run-determination-speckit-requirements-r20261030t081645z-078.md`、`feedback/20261030T083930Z-speckit-requirements.md`（`feature: 078-bilingual-expression`）、exec-quant 记录齐备。
  - 确定性门：`validate-requirements.py` status ok；`pre-analyze-check.py --stage requirements` decision=pass（errors=0 / advisories=3 均为 owner 文档尚未创建）；`decomposition-check.py --mode plan` proceed（fr=18 ≤ 30）。
  - 表达类四项：派发载荷 `error=owner-unavailable`（声明行尚未存在）→ 按 C-004(c) 走 `owner-unavailable` 降级分支：记降级观测、保持既有执行类门禁集，MUST NOT 按表达类四项校验。
  - 类别 re-baseline：U1 观测 `null/owner-unavailable` → 现解析 `expression / technique-document / source=declaration`（exit 0）；属声明落地后的正常差异，已记录。

### clarify

- 状态：dispatched（2026-10-30 08:42 UTC）
- 执行者：SDD Executor（本地原生子代理）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 哨兵：`CLARIFY-DONE`
- attempt 0（2026-10-30 08:48 UTC）：**完成**。
  - Mode A（plan.md 不存在 → 目标 requirements.md）；WRITABLE=true；prerequisites JSON 正常。
  - 覆盖扫描（fresh-context 委派读者执行，含 brief 重点复核六项：定义处机械可识别性 / 唯一形态全半角·空格·大小写 / glossary Canonical 关系 / jargon 白名单交界 / ambient 传播路径 / 存量迁移边界——后四项规格已覆盖，前两项经裁决补齐）。
  - 产物：requirements.md 头部补 `**Readers**`/`**Reading scenario**`（G-clarify-reader 修复）；`## Clarifications` Session 2026-10-30 追加 5 行 Q/A（3→8，append-only 校验通过）；Assumptions 追加 A9。零 `[NEEDS CLARIFICATION]` 残留。
  - 门禁：reader face pass（0 findings）；`pre-analyze-check.py --stage requirements` pass（errors=0，3 advisories 均为 owner 文档未创建，与基线一致）；`validate-requirements.py` ok（0/0，23 definition rows 不变 → checklist 计数无需刷新，doc-order pass）。
  - E3：test-evidence/clarify.jsonl `stage-status` 行 status=not-run-docs-only（六项缩减字段集 + rc/passed/failed）。
  - 提交：`1b352d57`（requirements.md + test-evidence/clarify.jsonl，显式路径）；运行时记录（state/session/feedback/exec-quant）不入提交；无 push。
  - wrap-up：run-determination + exec-quant + feedback（--feature 078-bilingual-expression）随本阶段收尾执行。

- **U4（驱动独立校验）：PASS** — 哨兵 CLARIFY-DONE；提交 `1b352d57`（仅 requirements.md + clarify.jsonl）；运行时记录未提交；无 push；证据 `clarify.jsonl` 在场（stage-status 完整）；`overlap-check.py` decision=clear（0 overlap）。

### plan

- 状态：dispatched（2026-10-30 08:52 UTC）
- 执行者：SDD Executor（本地原生子代理）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 哨兵：`PLAN-DONE`
- 约束：表达类须产出 `## Document Structure`（章节树 / 基准读者与阅读场景 / 证据清单 / 事实 owner 清单）；U4 后登记 `plan_constraint=active`。
- attempt 0 结果：**完成**。产物 plan.md（18 项 Constitution Check 全 Pass、T-001…T-004、Document Structure 四子节）、research.md（R-1…R-12）、data-model.md（E1…E7）、contracts ×4（35 条款）、quickstart.md（S1…S8）、feature-ref.md、coverage-baseline.txt、10 份证据；提交 `5a4dc5a4`（24 文件）；无 push。
- **U4（驱动独立校验）：PASS** — 哨兵 PLAN-DONE；`## Document Structure` 在场；`pre-analyze-check.py --stage plan` decision=pass（errors=0；19 条 advisory 均为 implement 期交付物路径）；`validate-decision-tensions.py` 0 error/0 warning（4 records）；`docs-utils validate` 违规 4 == 基线 4（零新增）；wrap-up 记账齐备。
- **plan_constraint=active**（activated_at 2026-10-30 09:28 UTC；plan_commit=5a4dc5a4；approved_baseline_commit=5a4dc5a4）。下游 tasks/analyze/implement/review 派发携带只小修块。
- **拆解门（070）**：`wp-gate.py --check plan` → verdict=`single-package`，findings=0，plan_hash `sha256:063092d3…6263`；decision=single-package（reason=not-beneficial）。
- 注意：`.specify/memory/glossary.md` 被 plan 阶段追加 auto/proposed 词条「双语表述 (Bilingual Expression)」，保持未提交，收尾时按运行记录归档。

<!-- wp-plan:begin stage=plan stage_attempt=1 -->
{
  "schema_version": 1,
  "line_id": "078-bilingual-expression",
  "run_id": "r20261030T081645Z-078a",
  "stage": "plan",
  "stage_attempt": 1,
  "decision": "single-package",
  "gate_verdict": "single-package",
  "reason": "one bounded write package (plan body + Phase 1 design artifacts); no parallel benefit (WG-13 not-beneficial)",
  "rule": null,
  "source_artifacts": [
    "requirements.md",
    "plan.md"
  ],
  "required_outputs": [
    "plan.md",
    "research.md",
    "data-model.md",
    "contracts/",
    "quickstart.md",
    "feature-ref.md"
  ],
  "integrator_outputs": [],
  "pattern": "serial",
  "tie_break": "wp_id-lexicographic",
  "slot_cap": 1,
  "packages": [
    {
      "wp_id": "plan-wp01",
      "stage": "plan",
      "objective": "Produce plan.md with Document Structure and the Phase 1 design artifacts from the clarified requirements",
      "kind": "write",
      "source_refs": [
        "requirements.md#Functional Requirements",
        "plan.md#Document Structure"
      ],
      "inputs": [
        "requirements.md",
        ".specify/memory/constitution.md"
      ],
      "outputs": [
        "plan.md",
        "research.md",
        "data-model.md",
        "contracts/",
        "quickstart.md",
        "feature-ref.md"
      ],
      "intermediate_outputs": [],
      "owned_paths": [
        "plan.md",
        "research.md",
        "data-model.md",
        "contracts/",
        "quickstart.md",
        "feature-ref.md"
      ],
      "read_only_paths": [
        "requirements.md",
        ".specify/memory/constitution.md"
      ],
      "depends_on": [],
      "parallel_safe": false,
      "max_turns": 120,
      "bounded_by": {
        "unit": "artifacts",
        "count": 6
      },
      "acceptance": [
        {
          "id": "A1",
          "check": "plan.md and Phase 1 artifacts exist and Document Structure has four subsections",
          "evidence": "plan.md"
        }
      ],
      "sentinel": "PLAN-DONE",
      "evidence": "test-evidence/plan.jsonl",
      "seat": {
        "role": "stage-worker",
        "stage": "executor",
        "type": "Worker"
      },
      "resources": {
        "ports": "none",
        "tmp_dir": "none",
        "cache_dir": "none",
        "shared_readonly": []
      }
    }
  ],
  "plan_hash": "sha256:063092d3e634b50af433f02c04e3b11d09a33f257b59b012ada0b426b9d16263"
}
<!-- wp-plan:end -->

### tasks

- 状态：dispatched（2026-10-30 09:29 UTC）
- 执行者：SDD Executor（本地原生子代理）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 只小修块：plan_constraint=active
- 哨兵：`TASKS-DONE`
- attempt 0 结果：**完成**。`tasks.md` 19 任务（T001–T019；Setup / US1–US4 / Polish），12 行 `[green:]` 认领 35 条款；Tests Mode ON；提交 `c07dde36`（8 文件）；无 push。
- **U4（驱动独立校验）：PASS** —
  - 哨兵 TASKS-DONE；`tasks.md` 19 条任务行；提交 `c07dde36` 仅含特性产物。
  - `decomposition-check.py --mode tasks` → proceed（task_count=19 ≤ 40）。
  - `pre-analyze-check.py --stage tasks` → pass（errors=0；31 条 advisory 均为 implement 期交付物路径）。
  - `validate-tasks.py` → PASS（0 error / 1 warning）；warning 经独立复核为伪阳性：T004/T005 仅**引用** `.specify/memory/glossary.md` 作只读输入，实际写目标为 `us2-glossary-drill.txt` / `us2-census-denominator.txt`，两任务无真实写重叠。已记入框架观察。
  - wrap-up 记账齐备（feedback --feature 078）。
- **快车道裁决点**：入口未携带 `fast-lane=opt-in` → `decision=full-chain`；不调用 admission-check、不产生 E1 记录；照常派发 checklist。

### checklist

- 状态：dispatched（2026-10-30 09:50 UTC）
- 执行者：SDD Executor（本地原生子代理）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 只小修块：plan_constraint=active
- 哨兵：`CHECKLIST-DONE`
- attempt 0 结果：**完成**。表达类两项算子全绿：G-checklist-reader（`doc-consistency-check.py --faces reader` → reader=not-applicable，findings=0，RC=0）与 G-checklist-duplicate（`--faces duplicate` → duplicate=pass，findings=0，RC=0），原始输出留档 `test-evidence/checklist-doc-consistency-{reader,duplicate}.txt`。
- 产物：NEW 日期化清单 `checklists/bilingual-convention-2026-10-30.md`（35 条 CHK001…CHK035，全部携带可追溯引用，35/35 ≥ 80% 规则满足；与既有 `checklists/requirements.md` 互补不覆盖——前者答「格子填没填」，本清单答「文字质量经不经得起追问」）。plan_constraint 遵守：零 plan 属主文件触碰，无 PLAN-EDIT。
- **U4（驱动独立校验）：PASS** — 哨兵 CHECKLIST-DONE；提交 `cc508bfe`（仅清单 + 3 份证据）；35 条目；两项 blocking 算子均有结果且无 `not-evaluated`：duplicate=pass，reader=not-applicable（该算子对清单制品无读者声明可核，RC=0、0 findings——记为框架观察，不阻断）；证据文件非空；`stage-status` 行在场；wrap-up 记账齐备；无 push。

### analyze

- 状态：dispatched（2026-10-30 09:52 UTC）
- 执行者：SDD Executor（本地原生子代理；只读阶段，产物面只读、Wrap-up 记账例外）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 只小修块：plan_constraint=active
- 判据：CRITICAL/HIGH 为零或已处置；同一门最多回环一轮
- 哨兵：`ANALYZE-DONE`
- 同作者条件成立（requirements→tasks 同会话链）；子代理派发工具不可用，按 `objective-analysis-gate.md` § 7 降级为直接受限读，35 条全部标记 `(detected: direct read, subagent unavailable)`；评审阶段建议委派路径复检校准假阴性率。
- E3：`test-evidence/checklist.jsonl` stage-status 行 status=not-run-docs-only（targeted-set-v1，六项缩减字段集 + rc/passed/failed）。
- 提交：`cc508bfe`（4 文件：新清单 + checklist.jsonl + 两份门禁输出）；运行时记录（state/session/feedback/exec-quant）不入提交；无 push。
- wrap-up：run-determination（complex，四量 not_evaluated 如实记录）+ exec-quant + feedback（--feature 078-bilingual-expression）齐备；阈值提示 should_prompt=true（198 ≥ 10）仅记录不传达。
- 条目满足判定不属本阶段：由 implement 的 checklist 豁免门接管；plan 已裁决的三处分流点（100% census / --scope changed / 退出码 0/1/2）作为「需求文字滞后」观察输入登记于清单 Notes。

- **U4（驱动独立校验，analyze 门）：PASS**
  - 哨兵 ANALYZE-DONE；报告正文在本阶段输出（只读阶段无提交，符合 U4 产物定义）。
  - 门判据：**0 CRITICAL / 0 HIGH**；8 MEDIUM + 6 LOW 不阻断，转入 implement 指引。
  - G-analyze-fact 已执行；G-analyze-review 归 review 阶段（按算子表登记）。
  - 只读纪律：除获准的 session/feedback/exec-quant 记账外零产物写入；`glossary.md` 修改为 plan 阶段遗留，非本阶段所为。
  - 记账：run-determination + exec-quant + feedback（--feature 078）齐备。
  - ANOMALY 行仅报告一条 feedback 计数笔误并已自我更正（第二条条目），不构成阻塞。

### implement

- 状态：dispatched（2026-10-30 09:55 UTC）
- 执行者：SDD Executor（本地原生子代理；长阶段，分段写文件）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 只小修块：plan_constraint=active
- 测试预算：implement 起点 `baseline` 全量一次（`run-tests.sh --names-out .../baseline-failed.txt`），写入状态脊 E2 围栏；中间一律 `targeted-set-v1` 并留 E3 `stage-status`
- 表达类实现证据：`G-implement-structure`（docs-utils validate 零新增）+ 四面 `reader/evidence/duplicate/count` + 结构子步 + `face=build` 子行
- 简报：`.specify/.tmp/sdd-loop/tmp/078-bilingual-expression/brief-implement.md`
- 分段：Part1 T001–T003 / Part2 T004–T007 / Part3 T008–T013 / Part4 T014–T019（每段 ≤8 任务）
- 哨兵：`IMPLEMENT-DONE`（各段回传 `PARTn-DONE`）

- **Part 1（T001–T003）U4：PASS**
  - 哨兵 PART1-DONE；提交 `cd57ed29`（12 文件，仅特性产物）；T001–T003 已勾 `[X]`。
  - **baseline 槽位已消耗（唯一一次全量）**：6811 passed / 21 failed / 1 skipped，rc=1，364s；E2 行写入 test-budget 围栏；失败名单 `baseline-failed.txt` 21 条。
  - 红先行四字段入档；定向集 6 passed / 9 failed，失败腿归后续段（ambient ×2 / checker ×6 / mirror ×1）。
  - 表达类面：reader/evidence/duplicate/count 全 pass；Chapter Tree 两向比对 0 chapter finding；`docs-utils validate` 4 == 基线；build 记 `not-applicable`。structure 子步 10 finding 已分类：9 条为 spec boilerplate（plan/tasks/checklist 阶段既有），1 条 owner-path-missing 属 plan P1 排期内预期（T007 即消）——记入框架观察。
  - 纪律：无 PLAN-EDIT、无 push、既有脏文件未动；wrap-up 记账齐备。
- **Part 2（T004–T007）U4：PASS**
  - 哨兵 PART2-DONE；提交 `d4429e3c`（11 文件）；T004–T007 已勾 `[X]`。
  - 检查器 `scripts/python/bilingual-expression-check.py` 落地（scan/coverage/census、退出码 0/1/2、码集四值）；ambient 小节落地；census 分母 7（M-7 差异如实上报）。
  - 定向集 15 collected / 14 passed / 1 failed（唯一失败 = 镜像漂移腿，归 T008）。
  - 表达类面：四面 pass、structure 子步 owner-path-missing 已消、`docs-utils validate` 4 == 基线、build N/A。
  - **PLAN-EDIT minor 已审计**：`plan.md` +1/-1（事实 owner 单元格改单一可解析路径）；`audit-plan-changes.py` → declared，undeclared=false。
  - 全量槽位未再消耗（baseline 行仍为 1）；无 push；wrap-up 齐备。
- **Part 3（T008–T013）U4：PASS** — 哨兵 PART3-DONE；提交 `840153fa`；镜像六对一致、instructions 刷新 32,600 B < 32,768、定向腿 15/15 绿、全量未再跑、无 PLAN-EDIT。
- **Part 4（T014–T019）U4：PASS** — 哨兵 IMPLEMENT-DONE；提交 `5aa7168a` + `04b32f87`；19/19 任务 `[X]`；verification.md 5 SC 行（SC-001/003/004 pass，SC-002/005 review 面 unknown）；waivers.md 35/35 satisfied；features 078 → Implemented（Pre-Status-Flip Gate 满足）；plan 改动仍仅 Part 2 的已声明 minor；无 push。
- **测试预算审计（implement）**：`slots=baseline:1 closure:0 reruns=0 exceptions=0 unknown=2`，`stages=6 complete=4`，`status=fail` —— **两处记账缺口**：(i) E2 行 `seq` 曾写成字符串 `"E2"`，已修正为正整数 `1`（驱动侧运行时记录，correction）；(ii) `analyze` 阶段缺 E3 `stage-status` 行（只读阶段未落 evidence 文件），`review` 行待本阶段产出。analyze 行将在 closure 前由驱动补齐并在收尾汇总披露。

### review

- 状态：dispatched（2026-10-30 11:05 UTC）
- 执行者：SDD Executor（本地原生子代理）
- 派发类别：`flow_class=expression; source=declaration; marker=; error=-`
- 只小修块：plan_constraint=active
- 代码段基线：特性分支基线 `7c835ba6`（implement 段基线 `cc508bfe` 供参考）
- 必须评估：SC-002 的 review 抽样面（`us11-review-sample.txt`）、SC-005 的真实词汇表 census（quickstart S8）
- 门禁：G-review-review（调用率 100%）、G-review-fact（`doc-consistency-check.py --action verify`）、G-analyze-review（评审基线确认）
- 哨兵：`REVIEW-DONE`
- **结果：完成** — 过程段 0 P0 / 1 P1 / 2 P2（P0 空集）；代码段 triage=run，base `7c835ba6`..`04b32f87`，回执 77/77/0/0，六级 blocking 0 / important 1 / suggestion 1 / praise 1，gate=allow；important（检查器 S1 header 撞 Column Definitions）本轮修复 + 红先行腿 + E6 append-only；SC-002 review 面 pass（9/9 抽样，1 分歧登记并修根因）、SC-005 review 面 pass（真实词汇表 census rc=0 / total=7 / findings=0）；提交 `878c03ab`。
- **U4（驱动独立校验）：PASS** — 哨兵 REVIEW-DONE；`review.md` + `code-review.md` 齐备；`review.jsonl` stage-status 在场；`verification.md` 5/5 SC 行含 `pass`；`features.md` / `features/078.md` = **Ready for Review**；表达类门禁全绿（G-review-review / G-review-fact / G-analyze-review）；无 push；无 PLAN-EDIT；wrap-up 三单元记账齐备。

### closure（驱动侧）

- 启动：2026-10-30 12:10 UTC
- review 后唯一一次全量：`bash scripts/bash/run-tests.sh --names-out .specify/specs/078-bilingual-expression/final-failed.txt`（后台运行，日志 `.specify/.tmp/sdd-loop/tmp/078-bilingual-expression/closure-run.log`）
- 计划：名称级 `comm -13` 比较 → E2 closure 行写入围栏 → `audit-test-budget.py --stage-check closure` → 工作树归档清扫 → 本地合并 master（不 push）→ 删分支 → 注销 line registry → 状态脊 completed
- 已知待补：analyze E3 行（已补 `test-evidence/analyze.jsonl` + `analyze-report.md`，待归档提交）；E3 完整性分母 6 阶段（clarify/plan/tasks/checklist/analyze/review）
- **首轮 closure 结果（E2 seq 2）**：24 failed / 6826 passed / 1 skipped（365.56s），对比 baseline 21 → **3 个新增失败**：
  1. `test_c57_shipped_text_adds_no_fresh_neutrality_violation`（owner 文档含 `.specify/specs/078-` 运行时路径）
  2. `test_a7_section_counts_20_to_21_and_21_to_22`（模板 31 / live 32，pin 仍为 30/31）
  3. `test_c11_no_dangling_guideline_pointer_on_either_instruction_surface`（ambient 小节写 `[[STR-001]]` 令牌而非字面路径，指针扫描看不到 `bilingual-expression.md`）
- **收口修复（closure-repair）**：提交 `4e23dad2`（11 文件）——owner 文档去运行时路径；模板 ambient 改字面路径；特性测试断言改字面路径且禁 `[[STR-`；fast-fail 计数 pin 更新为 31/32；`generate-instructions.sh` + `sync-mirrors.py --write` 后七对零漂移。定向 19 passed。
  - **偏差披露**：生成器为 additive reconcile，live `.specify/instructions.md` 的一行旧令牌按 `manage-instructions` Action 5 就地修正（生成器不回刷既有小节正文）——记入框架观察。
- **in-slot-rerun**：同套件全量重跑（日志 `closure-rerun.log`，`--names-out final-failed.txt`），后台运行中。
- 首轮 closure 证据保留为 `final-failed.closure1.txt`。

- **attempt 0 结果（2026-10-30 11:51–12:05 UTC）：完成**。
  - 过程段（review-sdd-process）：0 P0 / 1 P1 / 2 P2；P0 校验空集（标准措辞）；同作者降级直接读全标注。F1（P1）red-first 缺真实输入形状腿；F2（P2）测量 cadence 未任务化；F3（P2）receipt 默认基按 `main` 合并基解析与记录头不一致。REC-078-01…03 登记 register.md（同提交）。
  - 代码段（code-review）：`base` 解析 `7c835ba6`（feature-first-commit）；triage=run（changed 77，code paths = 检查器+测试）；记录头 head 固定 `04b32f87`（运行起点）；回执 77/77 judged / 0 skipped / 0 gap；六级计数 blocking 0 / important 1 / suggestion 1 / nitpick 0 / question 0 / praise 1；`report --summary` gate=allow。未提交作用域 24 路径双载体披露，不作通过结论。
  - **important 答复与修复轮（本阶段内落地，仅本特性产物）**：S1 词汇表解析缺口——scan_file header 正则撞上 Column Definitions 两列行后 break，真实词条表从未判定（glossary.md:48/:52 等 26 行存量漏报）。修复 = header 判定要求 ≥5 列（scripts/python/bilingual-expression-check.py）+ 红先行契约腿 `test_scan_glossary_shape_skips_column_definitions_decoy`（先红后绿）+ sync-mirrors --write 同步 `.specify/` 镜像（零手改）+ E6 append-only 追加 11:58:46Z run（+26 行）。定向集 16/16（targeted-set-v1，未消耗全量槽位）。suggestion 1 条（半角松括号无机械落点）登记为未来契约修订候选，不扩封闭码集。
  - SC 面补齐：SC-002 review 面 = pass（9/9 抽样复核，分歧 1 条登记处置于 us18；修复后 changed-scope 复跑 68 findings 全归类非新写内容，新写合规率维持 100%）；SC-005 review 面 = pass（S8 原命令实跑真实词汇表 rc=0 / census_total=7 / findings=0 / 0.275s，us19）。verification.md 五行全 pass。
  - 表达类门禁：G-review-review = 本轮 100%；G-review-fact = verify（reader=not-applicable / evidence=pass / duplicate=pass / count=pass，findings=0，13 文件）；docs-utils validate 4==基线零新增。
  - 状态门：三条件全满足（零 `[~]`；review.md + code-review.md 在场；当前记录 0 blocking）→ `features.md` / `features/078.md` `Implemented → Ready for Review`，Latest Review 双载体回填。
  - E3：`test-evidence/review.jsonl` 5 行（stage-status / 2×sc-verdict / code-segment / status-gate）。
  - 无 PLAN-EDIT；无 push；既有脏文件（glossary.md / session / feedback / exec-quant / todo）未提交未还原。
- part 3/4（2026-10-30T11:17 UTC）完成：T008–T013 勾 `[X]`；E3 `implement-part3.jsonl` 落 test-evidence/；提交见下段。T008 `sync-mirrors.py --write` 后六对全 ok，三件镜像 sha256 逐字一致，`.specify/` 零手改；镜像漂移腿转绿（定向集 15 passed / 0 failed）。T009 SC-001：关键词表程序派生（四组枚举 22 个字面量），扫描 17,307 文件，复制位置数 = 0（E7 快照 us9）。T010 SC-002：changed-scope 205 信号行 / 22 findings 全部分类为非新写内容（夹具标本 2 / 约定前 boilerplate 7 / 存量模板与镜像 12 / 状态脊 1），新写内容合规率 100%；E6 全量清单落 us10（454 文件 / 732 findings，只清单化不改写）。T011：`sample_lines` n=205、k=21、抽样 9 行（程序选择）。T012：live instructions 32,600 B < 32,768 预算，ambient 两态（.specify/instructions.md + 根 AGENTS.md）断言全过，blocking 27 == 基线。T013 SC-003：pilot 管道 rc=0，产物 ambient 三断言全过，pilot 已 rm -rf。表达类四面全 pass、structure 子步 9 findings 与 Part 1/2 同类 boilerplate 无新增、docs-utils 4 == 基线、build N/A。全量槽位未再消耗（E2 围栏仍 1 行）。无 PLAN-EDIT；无 push。
- part 1/4（2026-10-30T10:29 UTC）完成：T001–T003 勾 `[X]`；E2 baseline 已入上方围栏（6811 passed / 21 failed / 364s）；E3 `implement-part1.jsonl` 落 test-evidence/；提交 `cd57ed29`（12 文件，仅特性产物）。红先行四字段齐备（rc=1 / 14 failed / 1 passed）；owner 文档结构腿 6 passed，余 9 failed 归 T006/T007/T008。四面 reader/evidence/duplicate/count 全 pass；Chapter Tree 两向比对 0 chapter finding；structure 子步余 10 finding 已分类（9 条 spec boilerplate 既有重复 + 1 条 plan P1 声明的 owner-path-missing 待 T007）；face=build=not-applicable；docs-utils 违规 4 == 基线。无 PLAN-EDIT。
- **Part 4（T014–T019，2026-10-30T12:05–12:20 UTC）完成（implement 收口段）**：T014–T019 全勾 `[X]`，19/19 `[X]`，DoD complete；E3 `implement-part4.jsonl` 落 test-evidence/；提交 `5aa7168a`（18 文件）+ `04b32f87`（verification.md post_change_commit 回填）。T014 SC-004 审计：7c835ba6..HEAD 69 文件全落六类白名单、白名单外修改行数 0（5a4dc5a4..HEAD 44 文件同判）。T015 受控语料 census A/B/C：rc=0/1/0、census_total=3，负控证中文侧逐字比对真实执行；T018 S8 依该 deferral 以受控语料实跑（真实词汇表实跑归 review）。T016 登记复核通过（指针形态合规、零未登记 durable ID）。T017 漂移守卫 15/15 绿。T018 S1–S8 全实跑留档 notes/quickstart-run.md（S4 pilot 已拆）。T019 五条门禁全绿（validate-tasks 0 err / 1 条 tasks 期已裁决伪阳性 warn）；checklist 豁免门 35/35 satisfied、0 waiver（waivers.md，I-01 处置在 CHK030 成文）；零新命令/零运行时/零第三方依赖复核通过；verification.md 五行齐备（SC-001/003/004 pass；SC-002/005 unknown——review 面 not-evaluated 不预支）。表达类四面全 pass、structure 子步 9 findings 与前段同源 boilerplate、docs-utils 4==基线、build N/A。Pre-Status-Flip Gate 满足 → features.md / features/078.md `Planned → Implemented`，G-01 implement 阶段记录已回填。全量槽位未再消耗（E2 围栏仍 1 行）。本段无 PLAN-EDIT；无 push；既有脏文件（glossary.md / state / session / feedback / exec-quant / todo）未提交未还原。wrap-up：exec-quant 与 run-determination 均报 duplicate（(unit,run) 记录 Part 1 已建，不重复写行）；feedback 条目已记（should_prompt=true 仅记录不传达）。
- part 2/4（2026-10-30T11:10 UTC）完成：T004–T007 勾 `[X]`；E3 `implement-part2.jsonl` 落 test-evidence/；定向集 15 collected / 14 passed / 1 failed（唯一 failed = `test_drift_mirror_identity_derived_from_mirror_pairs`，T008 镜像腿，Part 3 转绿；其 2-tuple 解包瑕疵已带内修复）。T004 词汇表演练（临时根 `.specify/.tmp/078-bilingual-expression/us2-drill`，真词汇表 sha256 前后一致 8447bdab…，已拆卸）；T005 census 分母冻结 7（紧贴口径；M-7 锚点 132/161 差异已如实上报于 us2-census-denominator.txt：M-7 宽松正则含带空格形态，现测宽松口径 92/157，HEAD 91/156）；T006 ambient 小节四断言全过（blocking 27 == 基线）；T007 检查器三动作 + 退出码 0/1/2 + 码集四值 + `sample_lines` 全绿。表达类四面全 pass；structure 子步 owner-path-missing 经 PLAN-EDIT 小修消除（plan.md 事实 owner 单元格双路径「`a` + `b`」不可解析，改单一路径 + 契约指针入 anchor；分类=minor），余 9 条 boilerplate 与 Part 1 同；docs-utils 4 == 基线。owner 文档增补「机械判定边界」 prose 一段（C-12 成文，correction 级披露）。**Part 3（T008–T013）T010 前置提醒**：(i) 夹具 fullwidth/same-language 是指定违规标本，changed-scope 扫描必命中，SC-002 分母须分类排除（测试数据非内容）；(ii) checklists/bilingual-convention-2026-10-30.md 的 `## Measurability (Acceptance Criteria Quality)` 等 en 标题含同向半角括号，机械判定为 same-language-bracket（checklist 阶段先于约定成文的 boilerplate），T010 需分类裁决；(iii) 词汇表 150 条带空格形态不在紧贴口径 census 分母内（宽松口径 92 已上报）。无 push。

### closure-repair（修复轮，2026-10-30 12:2x UTC）

- 触发：closure 全量（review 后）24 failed / 6826 passed，较 baseline 21 failed 新增 3 个失败，全部归因本特性 closure 修复轮处理。
- 根因与修复（逐条）：
  1. C-57 框架运行时引用：`shared/guidelines/bilingual-expression.md` L96 删 `.specify/specs/078-bilingual-expression/test-evidence/` 路径（改「dated record、append-only，由运行面按日期落盘；本文件只指针，不承载清单」）；L107 删 `.specify/specs/078-bilingual-expression/contracts/checker.md` 指针，改指已分发检查器 `scripts/python/bilingual-expression-check.py`（行为说明 = `--help` + 模块 docstring）。
  2. ambient 指针字面量（FR-008/C-003）：`templates/instructions-template.md` Bilingual Expression 小节 `[[STR-001]]` → 字面值 `shared/guidelines/bilingual-expression.md`；live `.specify/instructions.md` 同步收敛（generate-instructions.sh 为纯 additive reconcile，既有小节不内容回刷，按 manage-instructions Action 5「drifted/stale → 只修过期事实」就地改一行；根 AGENTS.md 为符号链接自动跟随）。
  3. `tests/contract/test_bilingual_expression.py` L390 断言改为「ambient 含字面 owner 路径 + 无 `[[` 令牌」；docstring 同步。
  4. `tests/contract/test_fast_fail_discipline.py::test_a7` stale pin 30/31 → 31/32，docstring 追加 dated 记录（2026-10-30，078 ambient 小节）。
- 再生成与镜像：`generate-instructions.sh` + `sync-mirrors.py --write` + `--check` 零新增漂移（7 对全 ok）。
- 定向验证（closure-repair 槽位，未跑全量）：3 个原失败 + test_bilingual_expression.py + test_instructions_section_propagation.py = **21/21 passed**；证据 `test-evidence/closure-repair-{three-failures,bilingual-propagation,guard-files,targeted}.txt`。
- 附带观测：`test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` 在修复前树上同样失败（gate 扫描 total 27 vs 冻结 23，命中文件均非本特性改动面）——属 baseline 既有 21 failed 之一，非本修复轮新增，不在本轮范围。
- 纪律：零 PLAN-EDIT（未触碰 plan 属主产物）；无 push；既有脏文件未提交未还原；`.specify/state` 不入提交。

### closure 终局（2026-10-30 12:40 UTC）

- **in-slot-rerun（同套件，closure 槽位内）**：21 failed / 6829 passed / 1 skipped（364.31s）；`comm -13` 与 `comm -23` 均空 → **零新增失败、零修复差**；E2 seq 3 记 `in-slot-rerun`。
- **预算审计**：`slots=baseline:1 closure:1 reruns:1 exceptions=0 unknown=0`，`stages=6 complete=6`，`status=ok`。
  - 记账修复 2 处（均为格式，非事实改写）：(i) E2 baseline 行 `seq` 从 `"E2"` 改为正整数 `1`；(ii) review `stage-status` 从自造值 `review-targeted` 规范为 `ran` 并补齐 command/sufficiency/selected_paths/new_failures。
  - analyze 阶段缺 E3 行：由驱动在收口前补 `test-evidence/analyze.jsonl` + `analyze-report.md`（报告正文如实转录；`not-run-docs-only` 行的 `changed_paths` 列被检查的文件并在 selection_basis 说明，已披露）。
- **最终表达类门禁（修复后树）**：四面 reader=not-applicable / evidence / duplicate / count → 0 findings；结构子步 0 chapter finding（9 条为 spec boilerplate，同前）；`docs-utils validate` 4 == 基线；build N/A。
- **工作树归档清扫**：
  1. 特性产物 → `4e23dad2`（closure-repair）+ 证据提交（analyze 证据、final-failed 两份、review.jsonl 规范化）；
  2. 运行记录 → `586c9de4 chore(archive)`（session ×10 / feedback ×10 / exec-quant ×10 / glossary 增补 / todo 寄存 / closure-repair-names）；
  3. 状态脊 → 本提交（master 上）；
  4. `.specify/.tmp/` 由 `.gitignore` 覆盖（未跟踪）；
  5. 判定：`git status --porcelain` 仅余状态脊 → 归零后合并。
- **合并**：`308c7bef merge(078): land bilingual expression convention …`（`--no-ff`，自 `master@7c835ba6`）；**本地合并，不 push**（未授权）。
- **分支清理**：`git branch -d 078-bilingual-expression`（was `586c9de4`，已合并且祖先校验通过）。
- **Feature 状态**：`features.md` / `features/078.md` = **Ready for Review**（`Completed` 属人工/治理终验）。

## 测试预算（E2/E3）

<!-- test-budget:begin -->
{"seq":1,"slot":"baseline","stage":"implement","purpose":"implement-start full-suite baseline (single permitted full run)","trigger":"implement-part1-first-task","at":"2026-10-30T10:18:46Z","command":"bash scripts/bash/run-tests.sh --names-out .specify/specs/078-bilingual-expression/baseline-failed.txt","selection_basis":"full-suite (implement start baseline slot)","rc":1,"passed":6811,"failed":21,"failed_names_path":".specify/specs/078-bilingual-expression/baseline-failed.txt","baseline_compare":"na (this run IS the baseline)","evidence_ptr":".specify/specs/078-bilingual-expression/baseline-failed.txt","merge_source":"na","merged_at":"na"}
{"seq": 2, "slot": "closure", "stage": "closure", "purpose": "post-review closure full suite (first run)", "trigger": "review-passed", "at": "2026-10-30T12:26:52Z", "command": "bash scripts/bash/run-tests.sh --names-out .specify/specs/078-bilingual-expression/final-failed.closure1.txt", "selection_basis": "full-suite (closure slot)", "rc": 1, "passed": 6826, "failed": 24, "failed_names_path": ".specify/specs/078-bilingual-expression/final-failed.closure1.txt", "baseline_compare": "comm -13 baseline-failed.txt final-failed.closure1.txt; new failures: 3 (test_c57_shipped_text_adds_no_fresh_neutrality_violation, test_a7_section_counts_20_to_21_and_21_to_22, test_c11_no_dangling_guideline_pointer_on_either_instruction_surface)", "evidence_ptr": ".specify/specs/078-bilingual-expression/final-failed.closure1.txt + .specify/.tmp/sdd-loop/tmp/078-bilingual-expression/closure-run.log", "merge_source": "na", "merged_at": "na"}
{"seq": 3, "slot": "in-slot-rerun", "stage": "closure", "purpose": "closure full suite rerun after closure-repair", "trigger": "closure-repair 4e23dad2 (3 new failures: C-57 neutrality, A-7 section counts, C-11 dangling pointer)", "at": "2026-10-30T12:33:12Z", "command": "bash scripts/bash/run-tests.sh --names-out .specify/specs/078-bilingual-expression/final-failed.txt", "selection_basis": "full-suite (in-slot rerun of the closure slot)", "rc": 1, "passed": 6829, "failed": 21, "failed_names_path": ".specify/specs/078-bilingual-expression/final-failed.txt", "baseline_compare": "comm -13 baseline-failed.txt final-failed.txt = empty (0 new); comm -23 = empty (0 fixed)", "evidence_ptr": ".specify/specs/078-bilingual-expression/final-failed.txt + .specify/.tmp/sdd-loop/tmp/078-bilingual-expression/closure-rerun.log", "merge_source": "na", "merged_at": "na"}
<!-- test-budget:end -->

## 框架观察

（U4/U6 时补记：现象 / 框架位置 / 对驱动的影响。）
- 2026-10-30（implement Part 4）：census 抽取中文侧剥除 `**` 但不剥除行首 `## `/`- ` 结构标记，`## 锚定语义(Anchored Semantics)` / `- **样例概念**(x)` 形态会把标记计入中文侧而误报。位置：`scripts/python/bilingual-expression-check.py` action_census。影响：本特性 SC 判据不受影响（契约腿 test_census_action 钉真树 rc=0；受控语料按机械语义构造）；后续改进候选 = 抽取前剥除行首结构标记。
- 2026-10-30（implement Part 4）：S5 镜像比对相对 plan 基线的唯一差异是 scripts/shared 计数行 117→118、60→61（本特性新增源+镜像各一）；基线冻结早于特性新增时计数差是预期形态，「无新增漂移」判据应比对差异行而非绝对计数。位置：sync-mirrors 基线比对惯例。影响：无（T008 已裁决）。
- 2026-10-30（implement Part 4）：wrap-up 三件套（exec-quant / run-determination / feedback）中前两件以 (unit_id, run_id) 为幂等键，分段执行时仅首段写行、后续段报 duplicate——属设计内行为，不补写、不视为异常。
- 2026-10-30（driver，requirements attempt 0）：`sdd-requirements-executor` 实例 `run-turn-budget: 40` 在 19 FR 规模的特性上只够读完简报 + 脚手架即耗尽；改用 120 回合的 `sdd-executor` 容量后一次跑完。位置：`.specify/agents/instances/sdd-requirements-executor.agent.md`。影响：requirements 阶段一律用 40 会产生一次必然的重试。
- 2026-10-30（driver，implement/closure）：`doc-consistency-check.py --action structure --spec-dir <dir> --path <doc>` 会扫描整个 spec 目录，把 requirements/plan/tasks 的既有 boilerplate（标题、分支行、契约头）报成 duplicate-fact；交付文档的 Chapter Tree 两向比对本身是 0 finding。位置：`scripts/python/doc-consistency-check.py` structure 动作。影响：表达类 implement 的 structure 子步每次都会带 9–10 条非本阶段噪音，需人工分类；建议按 `--path` 限定扫描面或提供基线。
- 2026-10-30（driver，checklist U4）：表达类 checklist 阶段登记的 blocking 算子 `G-checklist-reader` 对清单制品返回 `not-applicable`（算子级而非 `face=build` 子行），与「`not-applicable` 只出现在 build 子行」的表述存在张力。位置：`shared/workflow/expression-gates.md` checklist 行 + `stage-prompts.md` U4 四项 (a)。影响：U4 需额外人工裁决，不能机械按算子表放行。
- 2026-10-30（driver，tasks U4）：`validate-tasks.py` 把「只读引用同一共享路径」判成两个 `[P]` 任务的写冲突（T004/T005 均引用 `.specify/memory/glossary.md`，实际写目标不同）。位置：`scripts/python/validate-tasks.py` parallel-safe 检查。影响：伪阳性 warning 需逐条裁决；建议按行内写目标而非引用路径判定。
- 2026-10-30（driver，closure 预算审计）：E2 `seq` 与 E3 `status` 是封闭取值域，但派发简报未点明合法值，执行者分别写成 `"E2"` 与自造值 `review-targeted`，closure 审计才暴露。位置：`references/efficiency-model.md` §2.2/§2.4 与 `stage-prompts.md` Test Budget Blocks。影响：建议在派发块的字段说明中直接列出 `seq` 为正整数、`status ∈ {ran, not-run-docs-only, empty-selection-escalated}`。
- 2026-10-30（driver，closure 预算审计）：analyze 是只读阶段，E3 状态域没有「只读分析」取值；077 与本线都缺 analyze 行，审计把该阶段计入 unknown 分母。位置：`audit-test-budget.py` `E3_STAGES` / `stage_status_complete`。影响：收口前必须补一行（本次以 `not-run-docs-only` + 被检文件清单 + 说明表示，已披露）；建议为只读阶段定义专用状态或豁免。
- 2026-10-30（driver，closure 修复）：`generate-instructions.sh` 是 additive reconcile，不回刷既有小节正文；模板中一节正文变更后 live `.specify/instructions.md` 保留旧文本，只能按 `manage-instructions` Action 5 手改一行。位置：`scripts/bash/generate-instructions.sh`。影响：与「mirrors are generated, never hand-edited」存在张力；建议生成器对小节正文提供 drift 修复模式。
- 2026-10-30（driver，closure 修复）：spec 局部引用令牌 `[[STR-001]]` 被写进**分发模板**，导致 3 个 closure 新增失败（C-57 中立性、C-11 指针、A-7 小节计数）；契约措辞「指针值 = [[STR-001]]」在「令牌 vs 字面值」上有歧义。位置：`templates/instructions-template.md`、`contracts/distribution.md` C-003、`FR-008`。影响：分发文本必须写字面值；建议在表达类 implement 门禁增加一条「shipped text carries no `[[STR-` tokens」的机械检查。
- 2026-10-30（driver，closure）：首轮 closure 24 failed vs baseline 21 的 3 个新增失败全部由「新增 ambient 小节」触发（计数 pin、指针扫描、中立性扫描），说明新增分发性文档的连带契约面（三处守卫）未被 implement 期定向集覆盖。位置：closure 修复路径。影响：新增 ambient 小节时，定向集应显式包含 `test_fast_fail_discipline` / `test_client_guard_sweep` / `test_user_facing_comprehension_section`。
