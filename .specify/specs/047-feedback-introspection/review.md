# Specification-Driven Development (SDD) Process Review Report: Feedback 自省流程(Feedback Introspection)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 047 |
| Requirement Key | 047-feedback-introspection |
| Requirement Name | Feedback 自省流程(Feedback Introspection) |
| Related Feature | 028 Feedback Mechanism |
| Repository | spec-kit |
| Repository URL | https://github.com/github/spec-kit.git |
| Branch | 047-feedback-introspection |
| Commit SHA | 3afd41e36f1ebf9102bffff906a3b92756b906c6 (short: 3afd41e3) — **feature uncommitted at review time** |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-08-28 |
| Reviewer (Agent) | Qoder (spec-kit SDD agent) |
| Environment | Linux 5.10 (container), bash, Python 3.13 + pytest, git 2.x |
| spec-kit Source Snapshot | https://github.com/github/spec-kit.git @ 3afd41e36f1ebf9102bffff906a3b92756b906c6 (working tree contains the reviewed changes) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 174 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/requirements.md | 3 用户故事 / 12 FR / 6 SC,零 NEEDS CLARIFICATION |
| plan.md | 124 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/plan.md | 技术上下文 + 13 原则宪法检查 + 镜像义务表 |
| data-model.md | 94 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/data-model.md | 4 实体 + 报告三态生命周期 + V-1..V-5 校验规则 |
| contracts/introspection-report.md | 64 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/contracts/introspection-report.md | 报告文件字节级 schema(C-1..C-12) |
| contracts/engine-cli.md | 47 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/contracts/engine-cli.md | 引擎动作契约(C-1..C-15) |
| contracts/command-mode.md | 34 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/contracts/command-mode.md | 命令模式契约(C-1..C-10) |
| quickstart.md | 74 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/quickstart.md | 端到端走查(⚙️已执行 / 📌契约钉标注) |
| tasks.md | 204 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/tasks.md | 21 任务 / 6 阶段 / DoD+Completion Gate |
| verification.md | 55 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/verification.md | SC 逐条状态(SC-005 deferred)+ 基线对照 |
| checklists/requirements.md | 37 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/checklists/requirements.md | 16 项质量清单全过 |
| feature-ref.md | 25 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/047-feedback-introspection/feature-ref.md | Feature 028 绑定映射 |

## 1. Process Execution Timeline

**git 证据缺口**: `git log` 对本特性目录为空——整个特性在评审时**完全未提交**(见 F1)。以下时间线由工作树状态、feedback 条目时间戳与 verification.md 自报重建,证据强度均为"产物状态推断,非提交轨迹"。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements + checklist + 术语登记 | feedback 条目 `20260827T033738Z-speckit-requirements`;requirements.md `Created: 2026-08-27` | 无 |
| 2 | clarify:2 问(Feature 绑定 028 + 入口形态)合并单次提问 | requirements.md `### Session 2026-08-27` 两行 Q→A;feedback 条目 `20260828T054156Z-speckit-clarify` | 无(符合"少而独立则合并"规则) |
| 3 | plan:Explore 子代理连续 2 次上游故障,降级为手工有界探查 | feedback 条目 `20260828T061407Z-speckit-plan`("对子代理上游故障无降级指引") | 有——预设路径失败,即兴降级(见 F2) |
| 4 | plan:quickstart 执行验证抓到真缺陷(registry-less 工作区 `--kind internal` 归零) | quickstart.md 步骤 2 注记:"执行验证 2026-08-28:registry 缺失时 `--kind internal` 会过滤掉全部遗留条目" | 无(纪律正向生效) |
| 5 | tasks:21 任务,机械校验(标签放置/DoD 前缀/单行)全过 | feedback 条目 `20260828T062345Z-speckit-tasks` | 无 |
| 6 | analyze:4 发现(1 HIGH 契约闭集冲突);子代理验证不可用,降级为直接原文复核 | feedback 条目 `20260828T063009Z-speckit-analyze`;contracts C-7/C-5 修复记录 | 有——§5.5 强制验证路径不可用(见 F2) |
| 7 | 用户批准后修复 4 发现(F-1 契约对齐/F-2 计数/F-3 测试钉/F-4 Excluded 语义) | contracts/introspection-report.md C-7 增 `建议处置` 行;tasks.md T006/T010/T014 扩钉 | 无(按协议) |
| 8 | implement:开工发现 plan/tasks 镜像义务误列已退役的 `.specify/templates/commands/` 镜像,先修正 3 处再动工 | sync-mirrors.py L58-62 注释("the .specify/templates/commands mirror is retired")vs 修订前 plan.md Mirror Obligations 行 | 有——规划期失真,实现期返工(见 F3) |
| 9 | implement:21/21 任务关闭;ENGINE_ACTIONS pin 同任务修订;quickstart E2E 真实执行通过 | verification.md `post_change_*`;测试运行 42 项新契约测试全绿 | 无 |
| 10 | 全量回归 2218P/44F,对 47F 基线按名零新增;3 个镜像漂移类基线失败因 sync 顺带转绿 | baseline-failed.txt(47)vs current-failed2.txt(44),`comm -13` 为空 | 无(但基线含义被 sync 改变,见 F4) |
| 11 | 特性整体未提交,等待用户批准提交命令 | `git status --short` 整列未提交变更;`git log` 对 spec 目录为空 | 有——见 F1 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 1 |
| Workflow | 1 |
| Documentation | 2 |

## 3. Findings (Problems & Improvement Targets)

### F1 — implement 的提交纪律自相矛盾,特性整体未提交进入评审

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md(Step 6 "Commit discipline" / Step 8 "Commit gate" / "Optional: Git Commit" 三节)
- **Evidence** (verbatim quote):

  ```
  Commit gate: commit after each task or logical group; in multi-phase runs the
  phase boundary is the default commit unit — commit only after that phase's
  name-level regression diff ... is empty
  ```
  与同一文件:
  ```
  ### Optional: Git Commit
  ... Display `git add -A && git commit -m "{msg}"` — only execute on explicit user approval
  ```

- **Why it's a problem**: "阶段边界为默认提交单元"与"仅经用户显式批准才提交"在无人值守/单次会话执行中直接冲突,结果是本特性 21 个任务全部完成后**零提交**(`git log` 对 `.specify/specs/047-feedback-introspection/` 为空),评审只能走工作树重建降级路径;同时违反同文件"The spec dir MUST NOT be left entirely uncommitted"的自身红线。
- **Proposed fix**: 在 implement.md 中明确裁决规则——把"阶段边界提交"标注为**默认建议**,将"用户批准"门改为阶段末的一次性批量确认(例如每个阶段 boundary 呈现一条待批准提交命令),或显式允许 agent 自主提交阶段边界;消除三节文字的并存歧义。

### F2 — 子代理派发故障无降级路径(plan Outline 与 analyze §5.5)

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md(Phase 0 "Codebase exploration pass")与 /storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md(§5.5 Finding Validation)
- **Evidence** (verbatim quote):

  plan.md:
  ```
  run a dedicated exploration pass (use an Explore subagent when available)
  ```
  analyze.md:
  ```
  every CRITICAL and HIGH finding MUST be confirmed by an independent read-only validation subagent
  ```
  本会话实测:Agent 工具连续 4 次返回 `Error in upstream response`(plan 阶段 2 次、analyze 阶段 2 次),两条命令均无书面降级路径,只能即兴改用"有界手工探查"/"直接原文复核 + 报告内标注"。

- **Why it's a problem**: "when available" 未定义"不可用"的判定与替代流程;analyze 的 MUST 级验证在子代理通道故障时形成流程卡点(要么违反 MUST,要么即兴降级且无留痕规范)。同一故障模式跨两个命令重复出现,是结构性缺口而非偶发。
- **Proposed fix**: 两处各补一句降级协议——plan.md:"子代理不可用时(连续 2 次派发失败)降级为摘要优先的手工探查清单(grep 标题/结构 + 定点读)";analyze.md §5.5:"子代理不可用时允许直接原文复核代替,并在报告该行标注 `(validated: direct re-read, subagent unavailable)`"。

### F3 — plan 模板未提示 `.specify/templates/commands/` 镜像已退役,规划期误列镜像义务

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/plan.md(Mirror Obligations 节)与 /storage/project/cloud-native-ai/spec-kit/scripts/python/sync-mirrors.py L58-62
- **Evidence** (verbatim quote):

  sync-mirrors.py:
  ```
  # the templates pair excludes
  # commands/ because the .specify/templates/commands mirror is retired (per-tool
  # copies come straight from templates/commands/ via regen-command-copies.py).
  ```
  而 plan.md 的 Mirror Obligations 示例行仍写:
  ```
  | [e.g. `templates/commands/x.md`] | [e.g. `.specify/templates/commands/x.md`; `.claude/commands/speckit.x.md`; ...
  ```
  本特性规划期按示例列出已退役镜像,实现开工时发现目标目录不存在,返工修订 plan/tasks/GATE-2 共 3 处。

- **Why it's a problem**: 模板示例把已退役的镜像形态列为首选示例,直接误导规划;退役事实只存在于 sync-mirrors.py 的注释里,规划者不可见。
- **Proposed fix**: 修订 templates/plan.md 的 Mirror Obligations 示例与注释,显式注明 `.specify/templates/commands/` 已退役、命令模板的副本面 = regen-command-copies.py 生成的 per-tool 副本;或在注释中链接 sync-mirrors.py 的 MIRROR_PAIRS 定义作为单一事实源。

### F4 — sync-mirrors.py --write 全量扇出把无关 drift 带入特性变更面

- **Severity**: P2
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/sync-mirrors.py
- **Evidence** (verbatim quote):

  本运行 `git status --short` 中与 047 无关的变更:
  ```
   M .specify/skills/browser-utils/SKILL.md
  ?? .specify/skills/browser-utils/references/trusted-browser-launch.md
  ?? .specify/skills/browser-utils/scripts/chrome_open_trust.sh
  ```
  这些是 skills/ 源与镜像间**预先存在**的漂移,被本特性的镜像同步任务(T004/T009 等)一并收敛。

- **Why it's a problem**: 全量扇出使特性运行的 diff 混入无关修复,破坏阶段提交的可 bisect 性,也改变了回归基线的含义(3 个镜像漂移类基线失败顺带转绿,基线 47→44)。
- **Proposed fix**: 为 sync-mirrors.py 增加按路径子集同步的选项(如 `--only scripts/python/feedback-utils.py`),或在 implement 的镜像任务指引中要求先 `--check` 报告全部漂移、与本次无关的漂移显式分流到独立提交。

### F5 — 引擎动作表文档漂移存量:skills/feedback.md 缺 041 的 6 个动作

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/docs/reference/skills/feedback.md(Engine 表)
- **Evidence** (verbatim quote):

  047 实施前该表仅 7 行(`record/status/list/mark-submitted/reindex/package/upstream`),而引擎自 041 起已有 13 个动作——缺 `dispose/cleanup/probes/map/migrate-legacy/probe-inject`:
  ```
  | `record` | ... |
  | `status` | ... |
  | `list` | ... |
  | `mark-submitted` | ... |
  | `reindex` | ... |
  | `package` | ... |
  | `upstream` | ... |
  ```

- **Why it's a problem**: 机制参考文档的引擎表面表落后实现 6 个动作(整个 041 周期未同步),读者无法从文档发现 dispose/cleanup 等管理能力;047 只补了本特性那行,存量漂移仍在。
- **Proposed fix**: 对 docs/reference/skills/feedback.md 引擎表做一次性补齐(经 improve-docs 或下一个 feedback 相关需求顺带),并考虑给引擎 `--help` 输出与文档表之间加一条轻量契约测试(动作清单对账)。

### F6 — implement 可写性预探针混淆"目录不存在"与"无写权限"

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md(Step 4 "Writability pre-probe")
- **Evidence** (verbatim quote):

  ```
  Writability pre-probe (fail fast): walk every directory named in plan.md's
  Source Code tree and Mirror Obligations rows and write-bit-probe each (touch-test);
  report ALL unwritable paths (e.g. root-owned container dirs) ... with the
  `sudo chown -R $USER <dir>` remedy
  ```
  本运行对 `.specify/templates/commands/` 触探失败,报为 UNWRITABLE——实际原因是**目录不存在**(F3 的退役镜像),按指引走 `sudo chown` 将是错误处置。

- **Why it's a problem**: 探针指引把两类失败混为一谈,给出的唯一补救(chown)对"不存在"场景是错的;在退役镜像这类场景下会误导出无谓的权限变更。
- **Proposed fix**: implement.md Step 4 的探针描述补一句分流:"touch 失败先区分 ENOENT(目录不存在——核对计划是否引用了已退役路径)与 EACCES(权限——才考虑 chown)"。

## 4. What Worked — Preserve (Brief)

- quickstart 执行验证门(plan Post-Generation Gate)在规划期抓到真实缺陷(`--kind internal` 在 registry-less 工作区归零),成本是一次编辑而非实现期返工。
- 基线按名冻结(`--names-out`)+ `comm -13` 比对,使"零新增失败"成为机械可证,并顺带识别出 3 个镜像漂移类基线失败转绿。
- TDD 红序 + blockedBy 拓扑在 21 任务规模下无冲突;confirm 路径前置落地经 front-loading 证据确认,无需返工重演。
- analyze 的交叉产物检查在实现前捕获契约闭集冲突(C-7 vs C-5),修复成本为一行。
- 引擎既有先例(SUBMISSION-NOTES 附加文件、dispose 的 index+frontmatter 双写)使新扩展点设计零发明。

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **plan.md 镜像示例更正** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/templates/plan.md(Mirror Obligations 节)。Change: 示例与注释注明 `.specify/templates/commands/` 已退役,命令模板的副本面仅为 regen-command-copies.py 生成物。Source: F3。Expected impact: 消除规划期误列退役镜像的返工。
- **implement.md 探针语义分流** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/templates/commands/implement.md(Step 4)。Change: 补 ENOENT vs EACCES 分流句。Source: F6。Expected impact: 避免对不存在路径执行错误 chown。

### 5.2 Command Prompt Improvements

- **子代理降级协议** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/templates/commands/plan.md(Phase 0)与 …/templates/commands/analyze.md(§5.5)。Change: 各补一条"子代理不可用时"的书面降级路径与留痕格式。Source: F2。Expected impact: 子代理通道故障不再造成流程卡点或即兴降级。

### 5.3 Automation / Script Improvements

- **sync-mirrors 路径子集同步** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/scripts/python/sync-mirrors.py。Change: 增 `--only <path>` 选项(或在 implement 指引中要求先 `--check` 分流无关漂移)。Source: F4。Expected impact: 特性 diff 不再混入无关镜像修复,阶段提交保持可 bisect。

### 5.4 Workflow Improvements

- **implement 提交纪律裁决** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/templates/commands/implement.md(Step 6/Step 8/Optional Git Commit)。Change: 明确"阶段边界提交"与"用户批准门"的裁决顺序(建议:阶段末批量呈现待批准提交命令)。Source: F1。Expected impact: 特性不再以零提交状态进入评审;review 的 git 重建路径恢复可用。

### 5.5 Documentation Improvements

- **feedback 引擎表补齐存量漂移** — Target: https://github.com/github/spec-kit.git/blob/3afd41e36f1ebf9102bffff906a3b92756b906c6/docs/reference/skills/feedback.md(Engine 表)。Change: 补齐 041 的 6 个动作行;考虑加动作清单对账契约测试。Source: F5。Expected impact: 机制参考文档与引擎表面恢复一致。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | implement 提交纪律裁决 | templates/commands/implement.md | F1 |
| P1 | 子代理降级协议 | templates/commands/plan.md + analyze.md | F2 |
| P2 | plan.md 镜像示例更正 | templates/plan.md | F3 |
| P2 | sync-mirrors --only 子集同步 | scripts/python/sync-mirrors.py | F4 |
| P2 | feedback 引擎表补齐 | docs/reference/skills/feedback.md | F5 |
| P2 | implement 探针语义分流 | templates/commands/implement.md | F6 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

---

## Remediation (2026-08-28, same-day user-directed fix round)

All six findings were fixed in framework sources immediately after this review:

| Finding | Fix landed in | Verification |
|---------|---------------|--------------|
| F1 | `templates/commands/implement.md`(Commit gate 增 Approval routing;Optional Git Commit 改为 fallback 定位) | regen 4 副本;parity 测试绿 |
| F2 | `templates/commands/plan.md`(Phase 0 降级句)+ `templates/commands/analyze.md`(§5.5 fallback 条款) | regen 4 副本;`sync-mirrors --check` exit 0 |
| F3 | `templates/plan-template.md`(Mirror Obligations 注释 + 示例行,指向 MIRROR_PAIRS 为真源) | `.specify/templates/` 镜像经 `--only` 同步 |
| F4 | `scripts/python/sync-mirrors.py` 增 `--only PATH`(可重复;非 templates/commands 前缀时跳过 regen 委托;未知前缀 exit 2) | 新契约 `tests/contract/test_sync_mirrors_only.py` 3/3 绿(先红后绿) |
| F5 | `docs/reference/skills/feedback.md` 引擎表补齐 041 的 6 个动作行 | 人工比对引擎 `--help` 动作集 |
| F6 | `templates/commands/implement.md` Step 4 探针分流(ENOENT→修正 plan 引用;EACCES→chown) | 同 F1 文件,一并扇出 |

回归:`run-tests.sh` 2221P/44F,对 047 基线(47F)按名零新增失败(comm -13 为空);`sync-mirrors.py --check` exit 0。附带观察:`tests/contract/test_token_efficiency_remediation_summary_first.py` 的 4 个 `test_mirror_identical[V-00x]` 基线失败属同类"退役镜像陈旧 pin"(断言已退役的 `.specify/templates/commands/` 目录)——超出本评审清单,建议列入下次 sanitize。
