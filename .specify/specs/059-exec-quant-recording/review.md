# Specification-Driven Development (SDD) Process Review Report: Agent+LLM 执行量化记录(Execution Quant Recording)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 059 |
| Requirement Key | 059-exec-quant-recording |
| Requirement Name | Agent+LLM 执行量化记录(Execution Quant Recording) |
| Related Feature | 059 Agent+LLM 执行量化记录(Execution Quant Recording) |
| Repository | spec-kit |
| Repository URL | Work remotes: `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`(全部 SSH,无 HTTPS web remote);`origin` = `git@github.com:github/spec-kit.git` 指向**上游**而非本 fork——任何以 origin 构造的 `{REPO_URL}@{COMMIT_SHA}` 引用都指向一个**不含本提交**的仓库 |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` 为空(HEAD = f75cab06 未推送到任何 remote;`github/main` 停留在 2026-06-17 的 2dd1ca4f)。本报告全部引用使用绝对路径;提交内容可用 `git show f75cab0610a57d35ffa27ae7245fefc8054b8860:<repo-relative-path>` 在持有本分支的检出中恢复。**本报告不可伪装为可移植 URL 报告** |
| Branch | 059-exec-quant-recording |
| Commit SHA | f75cab0610a57d35ffa27ae7245fefc8054b8860 (short: f75cab06) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-16 |
| Reviewer (Agent) | Qoder(无人值守 SDD 循环 review 阶段派发的独立会话;与全部被评审制品**零作者重叠**——9 个特性提交均先于本会话) |
| Environment | Linux 5.10.134-15.2.al8.x86_64 / bash / Python 3.11.11 / Node v26.3.0;working tree 携带 15 个未提交运行存储条目(`.specify/memory/` 下 feedback / session / exec-quant / glossary.md,按运行约束不提交不还原) |
| spec-kit Source Snapshot | specify-cli 0.0.22(pyproject.toml)@ f75cab06(本仓库即 spec-kit 源;`.specify/` 运行时面由同树 init/refresh 流投影) |

**同作者门禁判定**(objective-analysis-gate):**不触发**。被评审制品(requirements→clarify→plan→tasks→implement 全链)由驱动循环按阶段分派的各自独立会话产出,全部先于本评审会话;独立作者身份已提供门禁所要的新鲜上下文,检测由本代理直接执行,未派发检测子代理。P0 验证波:本次评审 **P0 = 0**,验证波空满足(见 §7 标准表述)。执行历史重建走**提交轨迹路径**(提交链完整按阶段/故事分组,未触发 working-tree 降级)。

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 177 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/requirements.md | 15 FR / 4 SC / 3 US;A1–A6 假设裁决 + Shared Strings 双锚点 + clarify 两问裁决记录 |
| checklists/requirements.md | 37 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/checklists/requirements.md | 15 项全绿清单(validator exit 0)——见 F6 |
| plan.md | 147 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/plan.md | Constitution 16/16 + Phase 0 实测 10 条 + D1–D12 裁决 + Mirror Obligations |
| data-model.md | 142 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/data-model.md | 6 实体 / V1–V8 校验规则 / 非回归基面 25 测试文件清单 |
| contracts/exec-quant-cli.md | 62 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/contracts/exec-quant-cli.md | 引擎三动作 CLI 契约(退出码/幂等/打分前置) |
| contracts/probe-registration.md | 79 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/contracts/probe-registration.md | 注册表逐字目标行 + `_ENGINE_SIBLINGS` + 056 对账面 + 传播顺序——见 F1/F2 |
| quickstart.md | 78 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/quickstart.md | 5 场景 + 逐示例免责 + 前提清单①–⑬——见 F1 |
| feature-ref.md | 46 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/feature-ref.md | 15 FR → 落点映射 / 4 SC → 验证映射 |
| tasks.md | 237 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/tasks.md | 16 任务(T001–T016)/ DoD + GATE-1..6 / A-tasks-1..7 裁决 |
| verification.md | 52 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/verification.md | SC-001..004 全 pass + 5 项偏差披露——见 F2/F4 证据 |
| notes/red-first-evidence.md | 67 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md | 三节红先取证(US1 born-red 25 failed;US2 born-green + 变异演练)——见 F4 |
| notes/pre-change-measurements.md | 51 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/notes/pre-change-measurements.md | PM-1..5 改前实测(431 行/72 面/双 --check 0) |
| notes/quickstart-run.md | 114 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/notes/quickstart-run.md | 五场景实跑留痕 + 三处前提勘正——见 F1 |
| baseline-failed.txt | 10 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/baseline-failed.txt | 冻结失败名单(既有 10 名;非本特性产物缺陷,不评审) |

## 1. Process Execution Timeline

全部时间取自 `git log --format='%h|%ci|%s'`(时区 +0800);每阶段均伴随独立的 run-determination session 记录与 feedback 记录(如 `/storage/project/cloud-native-ai/spec-kit/.specify/memory/session/20261016T025557Z-run-determination-speckit-requirements-059-exec-quant-record.md`),互相印证。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | 10:17 分支基座提交「improve skills」(驱动层技能自改进,先于特性;12 文件全为 improve-skills/sdd-loop-driver 及其镜像) | `git show 289be39d --stat` | 无(特性外工作,但不属于任何 /speckit.* 命令的产物——驱动环境自备) |
| 2 | 10:55 requirements 提交:仅 `requirements.md`(180 行)+ `checklists/requirements.md`(37 行);**features.md 未动**——特性注册义务未履行 | `git show 4166a5be --stat`(2 文件,无 `.specify/memory/features.md`) | **是**:feature-integration.md § Feature Binding Rules 要求 requirements 期落 Draft 行(根因见 F3) |
| 3 | 11:12 clarify 提交:注册行补落(features.md 行 67 + `features/059.md` 57 行)+ requirements 修订(27 处)+ 清单更新;Q1 绑定自身、Q2 引擎定名锁定;注册顺延被记为「上游偏差并披露」 | `git show c9a1e646 --stat`;requirements.md Clarifications:「requirements 会话仅提交规格 + 清单、未落注册行，登记义务顺延本轮补齐，记为上游偏差并披露」 | 恢复性偏差;偏差标签本身由 F3 的所有权矛盾制造 |
| 4 | 12:03 plan 提交:plan + data-model + 2 契约 + quickstart + feature-ref 同批落盘;Constitution 16/16 Pass;同作者委托复评 3 处缺陷就地修复(动作名同名/union 机制误述/常量重复) | plan.md § Constitution Check Re-check 段 | 无(同作者复评按门禁执行且修复在制品内——此处回写做到了,F1 是 implement 期 counterpart 缺失) |
| 5 | 12:28 tasks 提交:16 任务 / DoD / GATE-1..6 / A-tasks-1..7(含 `[green:]` 不可用实测与 D11 收窄) | `git show 94f344a1 --stat`(单文件 237 行) | 无(A-tasks-2 是对框架缺口的**记录**,缺口本身见 F5) |
| 6 | 12:37 setup 提交:T001 改前实测(431 行/72 面/双 --check exit 0)+ T002 基线冻结(10 失败名) | `git show b7ce174e --stat`;notes/pre-change-measurements.md | 无 |
| 7 | 13:21 US1 提交:引擎 + 注册 + 72 编译面再生 + 镜像;red-first 25 failed 留痕;**实际执行顺序偏离文档**:注册表投影 sync 先行于 compile(披露于 verification.md,四份制品的顺序文档未改,见 F2) | `git show b2e5ef6b --stat`;verification.md notes:「(2) compile-embeds reads the .specify mirror registry, so the registry projection sync precedes compile in the fixed propagation chain」 | **是**(向制品披露、未向根因制品回写) |
| 8 | 13:30 US2 提交:list/score 落地;T010 born-red 因 T005 超面交付而不可后补,以变异演练替代取证(见 F4) | notes/red-first-evidence.md §3:「T005 引擎一次成型时已包含 list-records/score 实现（超出 T005「spine + collect」任务面）……born-red 不可后补」 | **是**(诚实披露 + 判别力替代证明) |
| 9 | 13:38 US3 提交:边界隔离 + 零回归(comm 双向空、3240 passed);比对面在第 7/8/9 步提交门各跑一次共 4 次 | `git show a02b0175 --stat`;notes/quickstart-run.md 场景 5 | 无 |
| 10 | 13:44 polish 提交:GATE-1..6 重验、verification.md 落盘(SC-001..004 全 pass)、features.md 状态翻转 Implemented、tasks.md DoD 块 | `git show f75cab06 --stat` | 无 |
| 11 | 运行存储全程未提交:15 个脏项(feedback ×6 / session ×7 / exec-quant store / glossary.md)按「只提交本特性产物」约束留在工作树 | `git status --short` | 观察项:逐命令提交纪律只覆盖命令自身制品,glossary 富集等横切写入无归属提交点(本次按运行约束显式排除,不作 finding) |
| 12 | 提交链全程按阶段/故事分组(9 commit = requirements/clarify/plan/tasks/setup/US1/US2/US3/polish),无混相提交 | 本表 #2–#10 的 SHA 序列 | 无(良好的 story-grouped 纪律,历史重建未降级) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 2 |
| Automation / Scripts | 2 |
| Workflow | 2 |
| Documentation | 1 |

## 3. Findings (Problems & Improvement Targets)

> 本节只列问题、摩擦、歧义与具体改进目标。每条含逐字引文与具体修复提案。排序:P1 → P2,同severity内按类别。

### F1 — implement 期纠正只向证据注记披露、不向设计制品回写:HEAD 上留有 7 处已知陈旧事实

- **Severity**: P1
- **Category**: Workflow
- **Location**: 多文件(7 实例逐条列于 Evidence;全部位于 /storage/project/cloud-native-ai/spec-kit/ 下)
- **Evidence**(7 个实例,逐字引文 + 回写落点):

  (a) **契约动作名笔误未回写**。`.specify/specs/059-exec-quant-recording/contracts/probe-registration.md` §3 现文:

  ```
  新增 `test_exec_quant_action_set_exact()`（双向钉:choices == {collect, list, score}）;既有 `test_probe_utils_action_set_exact` / `test_feedback_utils_action_set_exact` 断言不动。
  ```

  与同文件 §1 Handler 行(`action=collect`)、plan D1、tasks T004 相矛盾。勘正只存在于 `.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md` §2:「契约勘正（probe-registration.md §3 行内 `{collect, list, score}` 系笔误）:exact-pin 按 D1 已裁决动作名钉 `{collect, list-records, score}`」——契约文件本身未改。

  (b) **行号引用过期未回写(两处)**。`contracts/probe-registration.md` §2:「`scripts/python/probe-utils.py` `_ENGINE_SIBLINGS`（L620–621）追加」;`plan.md` Phase 0 #2:「**`_ENGINE_SIBLINGS` 为显式元组**（L620–621:feedback/run-determination/probe/trigger 四引擎）」。实测(`sed -n '615,625p' scripts/python/probe-utils.py`)赋值行起于 **L619**。勘正只在 tasks.md A-tasks-4:「plan 记 L620–621,2026-10-16 grep 实测赋值行起于 `scripts/python/probe-utils.py` L619;以实测为准」——plan 与契约文件本身未改。

  (c) **quickstart 打包产物路径过期未回写**。`.specify/specs/059-exec-quant-recording/quickstart.md` 场景 4 现文:

  ```
  unzip -l feedback/feedback-*.zip | grep -c "exec-quant"   # 期望:0
  ```

  实际产物落 `.specify/memory/feedback/packages/feedback-<ts>.zip`(056 迁移后行为)。勘正只在 `notes/quickstart-run.md` 场景 4:「**quickstart 路径前提勘正**:场景 4 所写 `unzip -l feedback/feedback-*.zip` 已过时——package 实际产物落 `.specify/memory/feedback/packages/feedback-<ts>.zip`」——quickstart.md 未改。

  (d) **quickstart 凭据扫描 jq 形态按字面不可能通过自身期望**。quickstart.md 场景 4 现文:

  ```
  | jq '[.[] | tostring | test("(?i)(api[_-]?key|token|secret|authorization)")]' \
  | jq 'any'                                              # 期望:false
  ```

  `tostring` 序列化含键名,任何记录的 `quality.tokens` 键都命中 `token` → `any` 恒为 true,「期望 false」结构性不可达。勘正只在 notes:「quickstart 的 jq 形态按字面会命中**字段名**（`quality.tokens` 含 "token"）而非值级……勘正记录于此」——quickstart.md 未改。

  (e) **quickstart 基线冻结形态与 canonical owner 矛盾且自称「仓库标准」**。quickstart.md 场景 5 现文:

  ```
  python3 -m pytest tests/contract tests/integration -q 2>&1 \
    | grep "^FAILED" | sort > /tmp/baseline-failed.txt
  ```

  及其免责:「pytest 调用形态为仓库标准」。而 tasks.md T002 声明 canonical 形态归他处所有:「capture form, flag, and name-level comparison form are owned by `.specify/skills/internal/implement-feature/SKILL.md` § Test runs (canonical runner `scripts/bash/run-tests.sh` + `--names-out` + `comm -13`; not restated here)」——quickstart 给出的裸 pytest + grep 形态与 canonical runner 形态不同,实跑用的是后者。

  (f) **dangling 交叉引用**。`notes/quickstart-run.md` 场景 1 前置④:「④ compile→regen→sync 顺序（实测三步 exit 0,注册表投影先行——见 tasks T008 备注）」——tasks.md T008 现文**不含任何此类备注**(该行自 94f344a1 创建后未增此注),引用悬空。

  (g) plan.md 镜像义务表虽已按 One Source of Truth 收敛,但 Phase 0 行号(见 b)与其余过期事实同批滞留,说明 plan 自身的 re-check 回写只覆盖了 plan 期发现的缺陷,implement 期发现的事实修正没有对应的回写义务。

- **Why it's a problem**: 实现期对设计制品的事实纠正全部落在 dated 证据注记(notes/)里,而注记按其定位是「日期化记录、不作为现行事实」——耐用面(spec artifacts)继续携带与已裁决事实相矛盾的内容。下一个读者(未来 /speckit.analyze、后续特性实现者、或按 quickstart 复跑验证的人)从 HEAD 制品出发会继承错误路径、错误形态与悬空引用,重复付出本轮已付过的发现成本。快速失败纪律要求 correction「就地修复并于收尾披露」,本运行只做到了后半。
- **Proposed fix**: 在 `.specify/skills/internal/implement-feature/SKILL.md` 的 wrap-up/收尾义务中新增一条**设计制品回写义务**:实现期对 plan/contract/quickstart 事实内容的每处纠正,必须同步写回被纠正制品本体(附勘正日期),notes/ 只留日期化记录;与既有 docs-step 裁定义务(T016 形态)同批执行。验证面:可在实现收尾加机械检查——notes 中每处「勘正/已过时/系笔误」字样必须能在对应制品中找到改写痕迹或显式不回写理由。

### F2 — 文档化的固定传播顺序与引擎实际读源矛盾:按文档逐字执行产生一轮静默陈旧编译

- **Severity**: P1
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_compile_propagation_order.py(顺序真源);复制面包括 /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/contracts/probe-registration.md §4、plan.md(tasks T008、quickstart.md 场景 1 步骤 0 同文)
- **Evidence**:

  引擎实际读源(probe-utils.py L17 docstring 与 L130 常量,评审时机械核验):

  ```
  is read from ``<workspace_root>/.specify/shared/definitions/probe-definitions.md``.
  ```

  ```
  PROBE_DEFS_REL = Path(".specify") / "shared" / "definitions" / "probe-definitions.md"
  ```

  文档化顺序(四处同文,以 probe-registration.md §4 为例):

  ```
  1. `probe-utils.py --action compile-embeds` → 72 面（23 命令模板 + 49 技能 SKILL.md）的 `## Wrap-up` 各 +1 行
  ```

  顺序测试自身的 docstring 与失败提示同向:

  ```
  registry/units change → ``probe-utils.py --action compile-embeds`` (framework-source faces)
  ```

  ```
  "run probe-utils.py --action compile-embeds BEFORE regen/sync"
  ```

  本运行的实际执行与披露(verification.md notes):

  ```
  (2) compile-embeds reads the .specify mirror registry, so the registry projection sync precedes compile in the fixed propagation chain (final-state pin of test_compile_propagation_order.py unchanged and green);
  ```

- **Why it's a problem**: 实现者刚编辑框架源注册表(`shared/definitions/probe-definitions.md`)后按文档顺序执行 compile-first,引擎读的是**尚未投影的 `.specify` 镜像**——渲染出缺新行的陈旧编译面,compile/regen/sync 全部 exit 0,无任何报错;唯一能红的是指纹链契约测试(GATE-6 内),受治理流程可拦截,但脱离门禁的手工执行是静默污染路径。测试 docstring 的「framework-source faces」表述同样误述读源。这是 056 时代遗留的心智模型错误,本特性在实现中撞上并以偏差披露吸收,四处制品文档与测试提示词均未修正——下一个 probe 注册类特性会原样再撞一次。
- **Proposed fix**: 在顺序真源(`tests/contract/test_compile_propagation_order.py` docstring 与失败提示文案,以及 056 契约的对应节)修正为真实可执行顺序:**注册表投影 sync(`sync-mirrors.py --write` 限定注册表对)→ compile-embeds → regen-command-copies → sync-mirrors 全量**;或为 compile-embeds 增加框架源模式读源覆盖(需权衡 AGENTS.md § Two Hats 的引擎自定位约束——引擎读 `.specify` 是运行时面自定位的刻意设计,改读源属机制变更,须走特性)。两案择一,禁止让四处复制面继续与引擎行为矛盾。

### F3 — 特性注册义务所有权矛盾:工作流协议与受委托技能对「谁在 requirements 期落注册行」各执一词

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md § Feature Binding Rules vs /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/create-requirements/SKILL.md § Feature Integration
- **Evidence**:

  feature-integration.md(协议侧,把注册分配给 requirements):

  ```
  ## Feature Binding Rules (requirements phase)

  When `/speckit.requirements` creates a new spec:
  ...
  2. **Bind or Create**:
     - If NO match → create new Feature from `.specify/templates/feature-details-template.md`, add row to index
  ...
     - Update `memory/features.md`: set Status to the transition this command owns (§ Status State Machine — the requirements phase lands `Draft`, never `Planned`), update Spec Path, refresh date
  ```

  create-requirements SKILL.md(执行侧,把注册整体推迟给 clarify):

  ```
  **Binding timing**: this skill does NOT create or bind Features itself — it always initializes
  `Related Feature` with `Need clarification` values (steps 5.3/6) and defers the actual
  Feature lookup/creation/binding to the `/speckit.clarify` checkpoint, where the Binding
  Rules are applied.
  ```

  本运行的产出(被评审制品 requirements.md Clarifications):

  ```
  编号已由分支 `059-exec-quant-recording` 与规格目录预分配;注册表当时无 059 行(requirements 会话仅提交规格 + 清单、未落注册行,登记义务顺延本轮补齐,记为上游偏差并披露)。
  ```

- **Why it's a problem**: 两个 owner 直接矛盾:协议说 requirements 创建行(状态机行 33 也写 `/speckit.requirements | (none) → Draft`),技能说一律初始化为 Need clarification 并推迟到 clarify。命令模板 `templates/commands/requirements.md` 对此沉默(仅在 Before 注中提 /speckit.feature 可选)。执行代理按技能走(推迟),clarify 补注册时又按协议把它记为「上游偏差」——偏差记录是矛盾本身制造的:同一行为,按协议读是偏差、按技能读是合规。状态机所有权表在推迟读法下也失去落点(Draft 转换无执行者)。每个新建特性都会经过这处分叉。
- **Proposed fix**: 收敛为单 owner(二选一,由维护者裁定):(1) 保持推迟语义——修订 feature-integration.md § Feature Binding Rules 与状态机行 33,把行创建 + Draft 落定明确移交给 clarify 的绑定步骤,requirements 只保留 Need clarification 初始化;(2) 保持 requirements 落行——在 create-requirements SKILL.md § Feature Integration 中执行协议的 Bind-or-Create 步骤(行 + Draft + 表头计数同批)。无论哪案,同步修订 `templates/commands/requirements.md` 的 Before/After 注,使命令面与协议一致。

### F4 — 任务超面交付使 red-first 纪律静默塌陷:仅靠执行者自披露发现,无机械边界

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/implement-feature/SKILL.md(任务认领与完成判定义务);对照组:/storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/tasks.md T005/T010/T011
- **Evidence**:

  tasks.md 将引擎按故事拆分以保住 US2 的出生红(T005 限定动作一,T011 另行实现动作二/三):

  ```
  - [X] T005 [US1] [blockedBy: T003,T004] Implement `scripts/python/exec-quant.py` — spine + collect per `contracts/exec-quant-cli.md` 动作一 and data-model.md §1.1
  ```

  实现期 T005 超面交付,US2 的 born-red 结构性不可能,披露只能事后补救(notes/red-first-evidence.md §3):

  ```
  **偏差披露(born-green)**:T005 引擎一次成型时已包含 list-records/score 实现(超出 T005「spine + collect」任务面),US2 分区测试落笔时行为面已存在——**born-red 不可后补**,不以演练输出冒充出生红。作为替代,按仓库变异演练纪律(exec-quant 同类先例)证明分区判别力
  ```

- **Why it's a problem**: 任务行对实现范围的约束是纯散文(且本特性 `[green:]` 机器归因不可用,见 F5,跨相位分区只剩行内命名),没有任何机制在**认领或完成时**检出「实现超出该任务声明的契约节」。后果:后续故事的 red-first 义务静默失效,修复只能靠变异演练这类事后判别力证明——纪律的强度从「测试先于实现失败」降级为「执行者事后诚实」。凡把一个引擎的动作面按故事拆分的特性(常见拆法)都会暴露在同一风险下。
- **Proposed fix**: 在 implement-feature SKILL 的任务完成判据中加一条范围检查:关闭任务行前,对照该任务行内命名的契约节/校验规则清单,产出物若覆盖了**未分配给本任务**的契约节,即记为范围超面偏差并强制走披露路径(如同 born-green 处理),或在认领时刻显式合并后续任务并同步注记其 red 义务失效。配套:tasks 命令在拆分动作面时,为后续故事的测试行生成显式「MUST NOT be implemented by T00x」边界注记。

### F5 — `[green:]` 归因机制对 md-none 形态契约整体失效:机制与其解析器覆盖的契约形态脱节

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py;消费方 tasks 命令(A-tasks-2 记录)
- **Evidence**:

  tasks.md A-tasks-2(评审时以同命令复跑证实,两份契约均 `form=md-none clauses=0`):

  ```
  **A-tasks-2 `[green:]` 归因标签未使用**:2026-10-16 实测两份契约经 `clause_extract.py` 为 `form=md-none, clauses=0`(非 C-N 机器可判定条款形态),声明标签即 green-dangling ERROR;按技能规则的 fallback 改为「每条测试行行内命名其负责的契约节」完成同一文件跨相位分区（见 Format 节与 T003/T010/T013）。
  ```

  而框架内存在可解析先例(051 特性五个契约共 60 条款被解析;features.md 行 60:「contracts/ ×5 共 **60 条款**(discipline-doc 16 / ambient-section 11 / …)」)——即条款形态是既有约定,但 plan/契约撰写指引未把「要归因就写可解析形态」传到作者面。

- **Why it's a problem**: 任务模板提供的机器归因机制,对本框架自身常规产出的散文契约一律失效;每个散文契约特性都要在 tasks 期撞一次才回退到散文命名,而散文命名正是 F4 中超面交付无从机械检出的推手之一。检测点也放错了位置——形态在 plan 撰写期已定,tasks 期才发现为时已晚。
- **Proposed fix**: (1) plan 命令/契约撰写指引:若该契约将被 `[green:]` 归因消费,撰写时即按 clause_extract 可解析形态成文,或在契约头部声明 `form=md-none` 使下游免探测;(2) tasks 命令:生成期先跑一次 clause_extract 探测,按结果选择 `[green:]` 或散文命名路径,把 A-tasks-2 式的运行期发现前移为生成期分支。

### F6 — 语义型清单项的同会话全绿自证:机械校验器不覆盖的项提供虚假保证感

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/checklists/requirements.md(对照 /storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/requirements.md)
- **Evidence**:

  清单对以下两项打勾:

  ```
  - [x] No implementation details (languages, frameworks, APIs)
  - [x] Written for non-technical stakeholders
  ```

  同一 HEAD 的 requirements.md 却含刻意保留的实现级内容,例如:

  ```
  - **A5 引擎定名 `exec-quant.py`(scripts 层,框架源 → 运行时镜像)。** 2026-10-16 clarify Q2 锁定…
  ```

  及现状锚点节的宿主实测细节。清单 Notes 自述:「简报四个开放点……均已在规格 Assumptions 节(A1–A4)裁决并记录理由,故零澄清标记、checklist 一次全绿(in-session 先行裁决合规路径)」。

- **Why it's a problem**: 不是断言清单项客观为假——A5 等技术内容有明确裁决理由,属规格的合法组成;问题在于**证据形态**:「No implementation details」「Written for non-technical stakeholders」这类语义项没有机械对应物(validate-requirements.py 只查标记/计数/结构),全绿由撰写代理同会话自证,绿信号的置信度与机械项(validator exit 0)完全不同却不加区分地并列呈现。读者把「16/16 通过」读作同质保证时,语义项的绿是虚假保证感。本运行尚属诚实标注(Notes 披露了 in-session 路径),但纪律未要求这种披露。
- **Proposed fix**: create-checklist 技能:语义型清单项的通过判定必须附**逐项证据指针**(指向支撑其判定的规格节或裁决记录),无法附证据的项显式标注 `self-attested`;清单头部区分「机械校验项(validator 可复跑)」与「语义判定项(同会话自证)」两个证据等级。

### F7 — requirements-template 的 `**Status**: Draft` 头字段无任何更新所有者:Implemented 特性的规格头仍写 Draft

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md(L5);实例:/storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/requirements.md(L5)
- **Evidence**:

  同一 HEAD(f75cab06)上两处事实并存:

  ```
  **Status**: Draft
  ```
  (.specify/specs/059-exec-quant-recording/requirements.md L5)

  ```
  | Implemented | .specify/memory/features/059.md | .specify/specs/059-exec-quant-recording/requirements.md | 2026-10-16 …implemented via /speckit.implement (Planned → **Implemented**…
  ```
  (.specify/memory/features.md 行 67,同提交翻转)

  评审时 grep 全部命令模板与 scripts/python:无任何命令或脚本更新该头字段——它是只写一次的僵字段。

- **Why it's a problem**: 特性生命周期状态在 features.md 有唯一权威注册行,requirements 头的 Status 是一份永远滞后的副本——与 One Source Of Truth 纪律冲突(改变该事实需要编辑多个文件,正是纪律定义的坏味道),且对只读规格头的读者持续误报生命周期阶段。
- **Proposed fix**: 二选一:(1) 从 templates/requirements-template.md 删除 Status 头行,生命周期唯一权威 = features.md;(2) 保留但指定所有者——implement 收尾在翻转 features.md 的同一提交里同步翻转规格头(并在模板注明「由 /speckit.implement 维护,勿手改」)。推荐 (1),少一个可漂移面。

### F8 — check-prerequisites.sh 的 AVAILABLE_DOCS 是固定文件名清单:implement 期证据制品对下游清单不可见

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/check-prerequisites.sh(「# Build list of available documents」块,约 L222–249;框架源 scripts/bash/check-prerequisites.sh 同文)
- **Evidence**:

  枚举块只认固定名单(research/data-model/contracts/quickstart/checklists/feature-ref/verification 等),对目录不做遍历。本评审实际收到的 AVAILABLE_DOCS:

  ```
  {"REQUIREMENTS_DIR":"…/059-exec-quant-recording",…,"AVAILABLE_DOCS":["requirements.md","plan.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md","verification.md","tasks.md"],…}
  ```

  而实现期落盘的证据面 `notes/`(3 文件)与 `baseline-failed.txt` 不在清单内——它们恰是本评审 F1/F4 的一手证据来源。

- **Why it's a problem**: 一切以 AVAILABLE_DOCS 为制品面真源的下游消费者(评审/分析/回放类命令)会系统性漏掉 implement 期证据;本次评审靠人工目录遍历补救,但机制上清单承诺的「available docs」与实际制品集不符。
- **Proposed fix**: check-prerequisites.sh(框架源 scripts/bash/ 与 .specify/scripts/ 同批)在枚举块追加两条:`[[ -d "$REQUIREMENTS_DIR/notes" ]] && [[ -n "$(ls -A "$REQUIREMENTS_DIR/notes" 2>/dev/null)" ]] && docs+=("notes/")` 与 `[[ -f "$REQUIREMENTS_DIR/baseline-failed.txt" ]] && docs+=("baseline-failed.txt")`;或改为对 REQUIREMENTS_DIR 的一层目录遍历 + 已知文件合并。

## 4. What Worked — Preserve

- 提交链完整按阶段/故事分组(9 commit 对应 9 个流程相),实现历史可全量重建、无需降级推断——`/speckit.implement` 的逐任务/逐组提交纪律在本特性执行到位。
- 红先取证 + born-green 诚实披露 + 变异演练替代证明(notes/red-first-evidence.md 三节):纪律失效时**不伪造红色证据**、以判别力演练补位,该模式值得固化为 implement 技能的一等路径。
- quickstart 的 route b 前提清单机制(逐示例免责 + ①–⑬ + 指名钉定测试):新引擎命令在实现前不可执行的前提下,把验证义务显式转移到实现期且逐条可核对。
- 基线冻结 + never-cache 重探 + name-level `comm` 房式判据,SC-003 比对跨相位提交门共执行 4 次全部为空。
- plan 期同作者委托复评发现 3 处缺陷**全部就地修复在制品内**(plan.md re-check 段)——F1 缺的是 implement 期的对应回写义务,不是 plan 期这道工序本身。
- 偏差披露纪律:verification.md 5 项偏差全部带证据、带替代验证、带根因,无一静默吸收。

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **T1: 删除或指定 requirements 模板 Status 头的所有者** — Target: /storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md(L5)。Change: 删除 `**Status**: Draft` 行(features.md 为生命周期唯一权威),或在模板注明由 /speckit.implement 收尾与 features.md 同批翻转。Source: F7. Expected impact: 消除一份永远滞后的状态副本,规格头不再误报生命周期。

### 5.2 Command Prompt Improvements

- **C1: implement-feature 技能增加任务范围边界检查** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/implement-feature/SKILL.md(任务完成判据节;框架源同步)。Change: 关闭任务行前对照该任务命名的契约节清单检出超面覆盖,超面即走披露路径或显式合并后续任务并注记其 red 义务失效。Source: F4. Expected impact: red-first 不再依赖执行者事后自披露;后续故事测试行的出生红可保住。
- **C2: create-checklist 技能区分证据等级** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/create-checklist/SKILL.md(判定记录义务节)。Change: 语义型清单项要求逐项证据指针,不可附证据的项标 `self-attested`;清单头部区分机械项与语义项。Source: F6. Expected impact: 全绿清单不再为语义项提供同质保证感。
- **C3: quickstart 撰写义务——既有引擎命令形取自 canonical owner** — Target: /storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md(委托的 create-plan 技能内 quickstart 撰写节)。Change: quickstart 中调用既有引擎的命令,形态必须引用其 canonical owner(implement-feature § Test runs、feedback-step 等)或声明借用,禁止凭记忆复写裸形态(实例:场景 5 的 pytest 形态 + 「仓库标准」误称)。Source: F1(e). Expected impact: 消除设计制品与 canonical 形态的矛盾复写。

### 5.3 Automation / Script Improvements

- **A1: clause_extract 形态探测前移到契约撰写期** — Target: /storage/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py 的消费接线:templates/commands/plan.md 与 templates/commands/tasks.md(委托技能)。Change: plan/契约指引声明 `[green:]` 目标契约须为可解析形态或头部声明 md-none;tasks 生成期先探测再选归因路径。Source: F5. Expected impact: 归因机制对散文契约不再整链失效,运行期意外改为生成期分支。
- **A2: AVAILABLE_DOCS 覆盖实现期证据面** — Target: /storage/project/cloud-native-ai/spec-kit/scripts/bash/check-prerequisites.sh(同步 .specify/scripts/ 镜像)。Change: 枚举块追加 `notes/`(非空时)与 `baseline-failed.txt`(存在时)。Source: F8. Expected impact: 下游消费者不再系统性漏读 implement 期证据。

### 5.4 Workflow Improvements

- **W1: 收敛特性注册义务的单一所有权** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md § Feature Binding Rules(及状态机行 33)与 /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/create-requirements/SKILL.md § Feature Integration(框架源对应 templates/ 与 skills/ 源)。Change: 二选一收敛(推迟语义 → 修协议与状态机;requirements 落行 → 修技能),并同步 templates/commands/requirements.md 的 Before/After 注。Source: F3. Expected impact: 每个新建特性不再在 requirements/clarify 间经历「义务悬空 → 补落 → 贴偏差标签」的三步浪费。
- **W2: implement 收尾增加设计制品回写义务** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/implement-feature/SKILL.md(wrap-up/收尾义务节;框架源同步)。Change: 实现期对 plan/contract/quickstart 的每处事实纠正必须写回制品本体(附勘正日期),notes/ 只留日期化记录;配机械检查:notes 中「勘正/已过时/系笔误」命中必须能在对应制品找到改写或显式不回写理由。Source: F1. Expected impact: HEAD 制品不再携带已知错误事实;下游读者不再重复付出发现成本。

### 5.5 Documentation Improvements

- **D1: 修正固定传播顺序文档与测试提示词** — Target: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_compile_propagation_order.py(docstring 与两处失败提示文案)为顺序真源;056 契约对应节同步。Change: 顺序修正为「注册表投影 sync → compile-embeds → regen-command-copies → sync-mirrors」(或在 compile-embeds 增加框架源读源覆盖,须评估 Two Hats 引擎自定位约束后走特性)。Source: F2. Expected impact: 下一个 probe 注册类特性不再按文档撞出静默陈旧编译面。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | 设计制品回写义务(implement 收尾) | .specify/skills/internal/implement-feature/SKILL.md + 框架源 | F1 |
| P1 | 传播顺序文档与测试提示词修正 | tests/contract/test_compile_propagation_order.py + 056 契约 | F2 |
| P1 | 特性注册义务单一所有权收敛 | shared/workflow/feature-integration.md + create-requirements SKILL | F3 |
| P1 | 任务范围边界检查(implement) | .specify/skills/internal/implement-feature/SKILL.md | F4 |
| P2 | clause_extract 形态探测前移 | plan/tasks 命令委托技能 | F5 |
| P2 | 清单证据等级区分 | create-checklist SKILL | F6 |
| P2 | requirements Status 头处置 | templates/requirements-template.md | F7 |
| P2 | AVAILABLE_DOCS 覆盖证据面 | scripts/bash/check-prerequisites.sh | F8 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`。本报告按 §0 Reachability 判定全程使用绝对路径 + `git show` 恢复指引(HEAD 未推送且 remotes 全为 SSH,URL 形态不可用)。
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**(同作者门禁亦判定不触发:被评审制品先于本评审会话、作者不相交,检测无需委托;执行历史重建走提交轨迹路径,未降级。)

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
