# Specification-Driven Development (SDD) Process Review Report: 大模型 Token 使用效率纪律(035-token-efficiency)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
> **User-directed focus**: 本次评审按用户指示聚焦——feedback 承载的 Token 优化在整套开发流程中的**实际效果可视性**:如何用 agent 工具 / 大模型侧的真实 Token 计量(而非行/字节代理)做真实记录。

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 035 |
| Requirement Key | 035-token-efficiency |
| Requirement Name | 大模型 Token 使用效率纪律(程序优先 + 摘要优先 + 消耗观察反馈) |
| Related Feature | 040 Token Efficiency Discipline |
| Repository | spec-kit |
| Repository URL | https://github.com/github/spec-kit (origin; local fork with divergence per docs/concepts/upstream.md) |
| Branch | 035-token-efficiency |
| Commit SHA | eb41605bc671ea0fd82546d0c692e5f0615bd4fa (short: eb41605b) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-08-02 |
| Reviewer (Agent) | Qoder CLI agent (/speckit.review) |
| Environment | Linux 5.10.134-15.2.al8.x86_64 (x64), bash, Python 3.11.11 + pytest, Node v26.3.0 |
| spec-kit Source Snapshot | https://github.com/github/spec-kit @ eb41605bc671ea0fd82546d0c692e5f0615bd4fa (specify-cli 0.0.22) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 157 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/requirements.md | 三纪律三故事,9 FR,5 SC,STR-001 标记 |
| plan.md | 108 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/plan.md | 纪律文档 + 引擎过滤 + top-5 审计法,宪法 13 项全过 |
| tasks.md | 182 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/tasks.md | 30 任务,doc-feature 分类法,审计冻结为单一裁决点 |
| data-model.md | 69 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/data-model.md | 5 实体(纪律文档/违规清单/自评条目/摘要模式/升级阶梯) |
| contracts/ (3 files) | ~150 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/contracts/ | C-D/C-M/C-A 三合同,60 项测试钉扎 |
| audit.md | 42 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/audit.md | 冻结 9 违规,top-5 remediated 附实测前后对比 |
| verification.md | 61 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/verification.md | SC-001/002/003/005 pass,SC-004 partial |
| quickstart.md | 46 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/quickstart.md | 五步验证走查(实施期全部执行通过) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | /speckit.requirements 建规格,0 澄清标记 | 6f22e1a2 "add 035-token-efficiency requirements" | none |
| 2 | /speckit.clarify 绑定新 Feature 040 + top-5 配额 | 117f47ee "bind new Feature 040, fix top-5 remediation quota" | none |
| 3 | /speckit.plan(Explore 子代理一轮摸清触点)| 7cd62df6 "plan 035…top-5 audit method" | none |
| 4 | /speckit.tasks 30 任务 | bc26d0d3 "30 tasks, audit-freeze as single arbiter" | none |
| 5 | implement Phase 1-2:基线 + 纪律文档 + 审计冻结 | a8aac8e3 "discipline doc…frozen audit (T001-T008)" | 摩擦:audit.md 初稿预写 remediated 状态,提交前重置为 open(见 F5) |
| 6 | implement US1(TDD RED→GREEN)| fdae6603 "(T009-T016)…20 contract tests green" | 摩擦:gate-check 经 .specify 镜像调用返回 exit 3(见 F4) |
| 7 | implement US2 | a6c3ddf7 "(T017-T021)…16 pin tests green" | 摩擦:root 属主 .git/objects 桶阻断提交,按已知台账修复(既有环境问题,非本特性引入) |
| 8 | implement US3 + Polish,Feature → Implemented | 66f6c128、4f64e81a;五道完成门重验输出 | none |
| 9 | 全程按故事分组提交(9 commits) | git log --oneline -- .specify/specs/035-token-efficiency/ | none — 提交纪律良好 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Automation / Scripts | 2 |
| Workflow | 2 |

## 3. Findings (Problems & Improvement Targets)

### F1 — 本地会话存储已含真实 Token 计量字段,框架零消费(效果不可"直观看到")

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /home/agent/.qoder/projects/-storage-project-cloud-native-ai-spec-kit/fbf764b4-a5bc-4959-b818-598c23b496ad.jsonl(本机实测);/storage/project/cloud-native-ai/spec-kit/scripts/js/better-harness/session-analysis/
- **Evidence** (verbatim quote):

  ```
  "usage":{"input_tokens":0,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":0,...}
  (本会话该文件含 137 条 usage 记录;本环境网关回填 0 值,字段结构完整)
  ```

  同时 requirements.md Assumptions:"精确 Token 计数不可得为常态:八种受支持 AI 工具不统一暴露每次运行的 Token 用量;自评采用定性描述与注入量代理指标(行/字节)"。而 grep 全部托管的 session-analysis 引擎源码,不存在任何 `input_tokens`/`usage` 提取逻辑(仅 asset-eval 有 token *估算* 预算检查)。

- **Why it's a problem**: 规格把"精确计数不可得"当常态假设,但**agent 工具的本地会话落盘逐消息携带 usage 计量字段**——真实计量的数据通道结构上已存在(部分环境回填 0 需如实降级)。框架已托管的 session 证据泳道解析的正是这些文件,却不提取 usage,导致优化效果只能靠 wc 代理呈现,用户无法"直观看到融入优化后的真实差异"。
- **Proposed fix**: 在 session 泳道(scripts/js/better-harness/session-analysis/ 的会话适配器)提取逐会话 usage 聚合(input/cache_read/cache_creation/output),经 evidence-utils.py 落入 findings 证据(计数只路由不产生结论,零值/缺失如实标 Unobserved);feedback 侧 Token 自评在计量可得时引用真实数字并标注 `source=billing`,不可得时保持代理口径 `source=proxy`。

### F2 — partial 状态的 SC 没有强制落点,活体验证可静默烂尾

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/verification.md;/storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md
- **Evidence** (verbatim quote):

  ```
  SC-004_status=partial
  SC-004_note=full >=3-flow live spot-check requires fresh command runs post-merge; instruction-level compliance verified via 16 pin tests instead
  deferred_tasks=
  ```

- **Why it's a problem**: 模板只对 `status=deferred` 要求 `deferred_reason`,对 `partial` 无任何后续动作要求——SC-004 的"合并后 ≥3 流程活体抽查"没有任务、没有 owner、没有提醒,恰好是用户关心的"实际效果"验证环节,极易永久搁置。
- **Proposed fix**: verification-log-template.md 增加规则:`status=partial` MUST 附 `SC-NNN_followup=`(指向 todo/backlog 任务或下轮 spec),/speckit.implement 的 Pre-Status-Flip Gate 校验该字段非空。

### F3 — Token 观察条目纯自由文本,无法承载"真实计量"的机器可读记录

- **Severity**: P1
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md(Reflect 步骤扩展);/storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/data-model.md §3
- **Evidence** (verbatim quote):

  ```
  复用既有反馈条目结构(frontmatter: id/unit_id/.../summary + ## Review + ## Optimization Points),零新字段。
  量化口径:定性描述或行/字节代理指标
  ```

- **Why it's a problem**: 标记 `token-efficiency` 只支持子串检索(list --contains),观察值嵌在自由文本里——无法按命令聚合总量、画趋势、或与 F1 的真实计量对账;"真实记录"要求结构化数值字段。
- **Proposed fix**: 在 feedback-step.md 定义可选结构化尾注文法(如 `token-efficiency [source=billing|proxy] [in=N] [out=N] [saved≈N]`),feedback-utils.py list 增 `--parse-metrics` 输出结构化聚合;向后兼容纯文本条目。

### F4 — gate-check.py 镜像副本把 gate 路径解析成 `.specify/.specify/gate.yaml`

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/gate-check.py(line 31)及其镜像 /storage/project/cloud-native-ai/spec-kit/.specify/scripts/python/gate-check.py
- **Evidence** (verbatim quote):

  ```
  $ python3 .specify/scripts/python/gate-check.py <paths>
  gate file not found: /storage/project/cloud-native-ai/spec-kit/.specify/.specify/gate.yaml
  gate-exit=3
  ```

  源码:`GATE_FILE = REPO_ROOT / ".specify" / "gate.yaml"`(REPO_ROOT 取自脚本自身位置)。

- **Why it's a problem**: implement 命令要求"if `.specify/gate.yaml` exists, run gate-check.py"却未指明用哪一侧副本;镜像副本(下游项目安装获得的恰是这一侧)必然 exit 3,把机械门变成常态噪音。
- **Proposed fix**: gate-check.py 的 REPO_ROOT 改为向上查找 `.git`/`.specify` 的 walk-up 解析;或 templates/commands/implement.md 明示调用 canonical `scripts/python/gate-check.py`(下游场景仍需前者)。

### F5 — 审计清单可先声称后执行,模板未禁止"预写 remediated"

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/20260801T174725Z-speckit-implement.md
- **Evidence** (verbatim quote):

  ```
  审计清单一度预写 remediated 状态与预估降幅(先声称后执行),违反证据闭环,已当场重置为 open 并在整改后以实测回填
  ```

- **Why it's a problem**: 合同 C-A2 只规定"整改只改状态列",没有规定**状态翻转必须由证据触发**;本次靠执行者自纠,下次未必。审计类工件天然诱导"把设计目标写成完成状态"。
- **Proposed fix**: 在 tasks-template.md 的 Notes(或 audit 类合同模板)加一条:"清单状态列 MUST 仅在对应验证命令输出到手后翻转;预填完成态视同缺陷"。

### F6 — SC 的度量口径未在编写期锁定,V-003 的 36% 靠脚注自释

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/requirements.md(SC-003);/storage/project/cloud-native-ai/spec-kit/.specify/specs/035-token-efficiency/audit.md(V-003 行)
- **Evidence** (verbatim quote):

  ```
  SC-003: 对 top 整改项抽样重跑:…注入大模型上下文的相关内容量较整改前下降 ≥ 50%(行/字节代理口径)。
  audit.md: | V-003 | 57,559 B 预载 | 预载 tasks+plan = 36,851 B(实测,034 口径) | **36.0%**(预载口径;其余 4 工件 20,708 B 转按需,未计入) |
  ```

- **Why it's a problem**: "下降 ≥50%" 未写明按预载口径还是全生命周期口径;V-003 只有 36%(预载口径),靠审计备注补口径说明才与 SC 相容——同一数字换个口径读就是"未达标",验收争议前置到了脚注。
- **Proposed fix**: requirements-guidelines.md 的 Success Criteria Guidelines 增补:"含百分比阈值的 SC MUST 同时声明测量口径与适用范围(逐项 vs 抽样)",由 /speckit.requirements 质检清单项钉住。

## 4. What Worked — Preserve (Brief)

- 审计冻结(先测量、排序、冻结,再整改)+ 状态列单向翻转:top-5 裁决零争议。
- TDD RED→GREEN 四轮(12+20+16+12 合同测试)对文档型交付物同样有效(结构性钉扎)。
- sync-mirrors.py 单命令扇出 + regen 副本:8 类镜像触点零手工双写、零漂移。
- run-tests.sh `--names-out` + `comm` 基线比对:37 项存量失败与回归一刀切清。
- 消耗观察闭环当场自食(dogfood):4 条带标记条目一次检索命中,与 grep 对账 4/4。

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **partial-SC 强制落点** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/templates/verification-log-template.md. Change: `status=partial` MUST 携带 `SC-NNN_followup=`,implement 的 Pre-Status-Flip Gate 校验非空。Source: F2. Expected impact: 活体效果验证不再静默烂尾。
- **SC 度量口径锁定规则** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/shared/guidelines/requirements-guidelines.md. Change: Success Criteria Guidelines 增"百分比阈值 SC 必须声明测量口径与逐项/抽样范围"。Source: F6. Expected impact: 验收争议从脚注移回编写期。

### 5.2 Command Prompt Improvements

- **审计状态翻转证据规则** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/templates/tasks-template.md(Notes 节)。Change: 增"清单/台账状态列仅在验证输出到手后翻转;预填完成态视同缺陷"。Source: F5. Expected impact: 堵住"设计目标写成完成状态"的惯性通道。

### 5.3 Automation / Script Improvements

- **真实 Token 计量接入 session 证据泳道(用户核心诉求)** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/scripts/js/better-harness/session-analysis/(适配器)+ scripts/python/evidence-utils.py。Change: 会话适配器提取逐消息 `usage` 字段并按会话/按命令聚合入 findings 证据;零值/缺失如实标 Unobserved,绝不编造。Source: F1. Expected impact: 优化效果可用 agent 工具自身计量直观呈现(优化前后同流程真实对比),代理指标降级为兜底。
- **Token 观察结构化解析** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/scripts/python/feedback-utils.py + shared/workflow/feedback-step.md。Change: 定义 `token-efficiency [source=…] [in=N] [out=N]` 可选尾注文法与 `--parse-metrics` 聚合输出。Source: F3. Expected impact: 观察可聚合、可画趋势、可与计费对账。
- **gate-check 路径解析修复** — Target: https://github.com/github/spec-kit/blob/eb41605bc671ea0fd82546d0c692e5f0615bd4fa/scripts/python/gate-check.py. Change: REPO_ROOT 改 walk-up 解析(向上找 `.git`/`.specify`)。Source: F4. Expected impact: 镜像/下游安装侧机械门不再假阴性 exit 3。

### 5.4 Workflow Improvements

- **优化前后计量对照协议** — Change: 为 top-5 类整改定义"同一流程、同一输入、整改前后各一次真实运行"的计量对照窗口(计量来源:F1 的 session usage 聚合;不可得环境回退代理口径并显式标注),结果记入 audit.md 备注列与 feedback 条目。Source: F1, F3. Expected impact: "融入优化后效果如何"有直读答案。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | 真实 Token 计量接入 session 证据泳道 | scripts/js/better-harness/session-analysis/ + scripts/python/evidence-utils.py | F1 |
| P1 | partial-SC 强制落点 | templates/verification-log-template.md + /speckit.implement gate | F2 |
| P1 | Token 观察结构化解析 | scripts/python/feedback-utils.py + shared/workflow/feedback-step.md | F3 |
| P2 | gate-check walk-up 路径解析 | scripts/python/gate-check.py | F4 |
| P2 | 审计状态翻转证据规则 | templates/tasks-template.md | F5 |
| P2 | SC 度量口径锁定规则 | shared/guidelines/requirements-guidelines.md | F6 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
