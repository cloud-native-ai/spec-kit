# Specification-Driven Development (SDD) Process Review Report: 078-bilingual-expression

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 078 |
| Requirement Key | 078-bilingual-expression |
| Requirement Name | 双语表述（Bilingual Expression） |
| Related Feature | 078 双语表述（Bilingual Expression） |
| Repository | spec-kit |
| Repository URL | remotes: `origin git@github.com:github/spec-kit.git`（上游世系）/ `github git@github.com:cloud-native-ai/spec-kit.git` / `gitee …` / `gitlab …`（均为 SSH，无 HTTPS web 形态） |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty（HEAD 未 push 到任何远端）— 本报告引用一律用绝对路径 + `git show <sha>:<path>`，不用 URL |
| Branch | 078-bilingual-expression |
| Commit SHA | 04b32f87bc7adcd555bf4dc0a73701d9413fd5f6 (short: 04b32f87；过程段报告生成时的运行起点 HEAD；修复轮提交在其后） |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-30 |
| Reviewer (Agent) | SDD Executor（本地原生子代理；同作者条件成立，检测按 objective-analysis-gate 降级为直接受限读，全部发现标注 `(detected: direct read, subagent unavailable)`） |
| Environment | Linux, Python 3.11.11, git 2.x |
| spec-kit Source Snapshot | same repo（自托管框架源 + 客户端运行时两帽仓） @ 04b32f87 |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 229 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/requirements.md | 18 FR / 5 SC / 双语约定需求与 Shared Strings |
| plan.md | 236 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/plan.md | 含 Document Structure 四子节的实现计划 + T-001…T-004 |
| research.md | 83 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/research.md | R-1…R-12 现状锚点与裁决 |
| data-model.md | 64 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/data-model.md | E1…E7 实体与规则 |
| contracts ×4 | 131 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/contracts/ | 35 条款（owner-document/checker/distribution/measurement） |
| quickstart.md | 64 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/quickstart.md | S1…S8 可执行场景 |
| tasks.md | 303 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/tasks.md | 19 任务（T001–T019），19/19 `[X]` |
| owner document | 113 | /storage/project/cloud-native-ai/spec-kit/shared/guidelines/bilingual-expression.md | 约定唯一 owner（六组事实） |
| checker | 636 | /storage/project/cloud-native-ai/spec-kit/scripts/python/bilingual-expression-check.py | scan/coverage/census 确定性守卫（修复轮后行数） |
| contract tests | 450 | /storage/project/cloud-native-ai/spec-kit/tests/contract/test_bilingual_expression.py | 16 腿漂移守卫 + 红先行 |
| verification.md | 99 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/verification.md | 5 SC 两面评估日志（review 后全 pass） |
| waivers.md | 65 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/waivers.md | checklist 豁免门 35/35 satisfied |
| test-evidence/ | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/test-evidence/ | 阶段证据（E2/E3、us2…us19、门禁输出） |
| review.md | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/review.md | 本报告（过程段） |
| code-review.md | 290 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/code-review.md | 代码段记录（triage=run） |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements attempt 0 预算触顶（40 回合），attempt 1 以 120 回合 SDD Executor 重入续跑 | `.specify/state/078-bilingual-expression.md` § requirements；提交 `2fc9f22f`/`bb138fa2` | 是（预算低估，重入已归因修复；框架观察） |
| 2 | clarify Mode A 补 Readers/Reading scenario + 5 条会话裁定 | `1b352d57` | 无 |
| 3 | plan 落 Document Structure 四子节 + 4 契约；plan_constraint=active 激活 | `5a4dc5a4` | 无 |
| 4 | tasks 19 任务 + red-first 契约测试占位 | `c07dde36` | 无 |
| 5 | checklist 表达类两算子 + 日期化质量清单 35 条 | `cc508bfe` | 无 |
| 6 | analyze 同作者降级直接读（子代理不可用），0 CRITICAL / 0 HIGH | 无提交（只读阶段） | 是（objective-analysis-gate 声明的降级分支；评审面建议复检） |
| 7 | implement 四段（baseline 全量槽位 1 次：6811 passed / 21 failed） | `cd57ed29`…`5aa7168a` + `04b32f87` | 无 |
| 8 | implement Part 2 一处 PLAN-EDIT minor（plan.md 事实 owner 单元格改单一路径），经 audit-plan-changes 判 declared | `d4429e3c`；`.specify/specs/078-bilingual-expression/test-evidence/implement-part2-gates.txt` | 无（按 plan 约束申报流程） |
| 9 | SC-002/SC-005 的 review 面按纪律不预支（verification.md 记 unknown） | `5aa7168a` | 无（声明的分面纪律） |
| 10 | review 过程段 + 代码段（triage=run，77/77 覆盖，0 blocking）；代码段 important 1 条（S1 解析缺口） | `code-review.md`（本运行） | 无 |
| 11 | review 修复轮：检查器 S1 header ≥5 列修复 + 红先行契约腿 + 镜像同步；E6 追加 26 行存量清单 | `us18-sc002-review-recheck.txt`；定向集 16/16 | 无（review 阶段授权内的修复） |
| 12 | analyze 阶段缺 E3 stage-status 行（只读阶段未落证据文件） | `.specify/state/078-bilingual-expression.md` 测试预算审计 | 是（记账缺口，已披露，closure 前由驱动补齐） |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 1 |
| Documentation | 0 |

P0 校验状态：No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.（同作者条件的检测委派因子代理不可用降级为直接受限读，全部发现带 `(detected: direct read, subagent unavailable)`。）

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 7c835ba60705bf30f82bffa1cde50d845a015ccc | `git-delta-review.sh base`（feature-first-commit 层） |
| Head commit | 04b32f87bc7adcd555bf4dc0a73701d9413fd5f6（运行起点固定） | `start` 记录头 |
| Base source | feature-first-commit | 记录头 |
| Renderer mode | renderer: text | 记录头（非交互调用） |
| Changed / judged / skipped / gap files | 77 / 77 / 0 / 0 | 回执块逐字抄录 |
| Segment verdict | pass | 回执 `verdict=pass` |
| Gate verdict | allow（`blocking_entries=0`；存在 1 条 `important`，已逐条答复并在本轮修复轮落地：S1 解析缺口修复 + 红先行契约腿 + 镜像同步，定向集 16/16 绿） | `report --summary --file` |
| Reason, when one applies | none | — |
| Uncommitted scope | 24 个未提交路径未纳入评审对象（工作区脏文件：glossary.md / state 脊 / session / feedback / exec-quant / todo 等），不作通过结论 | 回执 `uncommitted_scope=24` 与本报告同句披露 |
| Record | .specify/specs/078-bilingual-expression/code-review.md | 本运行所写 |
| Archive | none（首次运行） | `start` 输出 |

本小节只承载结论与指针：意见正文、六级计数（blocking 0 / important 1 / suggestion 1 / nitpick 0 / question 0 / praise 1）在 `code-review.md` 内读取。两段结论不合并、不换算。

## 3. Findings (Problems & Improvement Targets)

### F1 — red-first 契约腿只钉夹具形状，机械守卫缺「真实注册输入」的 scan 腿

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: tests/contract/test_bilingual_expression.py（绝对：/storage/project/cloud-native-ai/spec-kit/tests/contract/test_bilingual_expression.py）
- **Evidence** (verbatim quote, tests/contract/test_bilingual_expression.py 第 56–58 行):

  ```
  GLOSSARY_UTILS = REPO_ROOT / "scripts" / "python" / "glossary-utils.py"
  REAL_GLOSSARY = REPO_ROOT / ".specify" / "memory" / "glossary.md"
  FIXTURES = REPO_ROOT / "tests" / "fixtures" / "bilingual"
  ```

  scan 三腿（test_scan_compliant_fixture / test_scan_fullwidth_fixture_red / test_scan_same_language_fixture_red）全部只跑 `FIXTURE_*`；`REAL_GLOSSARY` 仅被 census 腿（test_census_action，第 271–283 行）消费。真实词汇表的形状是「`## Column Definitions` 两列表 + `## Glossary` 五列表」：

  ```
  | Canonical | The agreed project term (unique, case-insensitive). |
  ...
  ## Glossary

  | Canonical | Variants | Meaning | Origin | Status |
  ```

- **Why it's a problem**: 检查器 `scan_file` 的 S1 header 正则 `^\|\s*Canonical\s*\|` 撞上 Column Definitions 的两列行后于 `## Glossary` 处 `break`，真实词条表从未被判定——`missing-bilingual` 的机械落点对真实输入整体静默失效（实测：修复前 scan 真词汇表 rc=0；修复后 rc=1、26 行存量命中）。红先行四字段全绿却挡不住「夹具形状 ≠ 真实形状」这一类缺口；本次仅因 SC-002 评审抽样有一行落在词汇表上才暴露。
- **Proposed fix**: Tests Mode 纪律（templates/tasks-template.md § Tests 与 constitution IV 的红先行指引）增一条可判定要求：凡消费「注册输入」（词汇表/登记表等既有存储）的机械守卫，每个 action 至少一条契约腿钉**真实输入形状**（或经程序派生的同形状合成夹具），不得只用简化夹具；同批把 census 已钉真词汇表的做法立为范例。
- **Detected**: direct read, subagent unavailable

### F2 — 测量契约的「每个交付里程碑后各测一次」没有落到 tasks.md 的收口任务上

- **Severity**: P2
- **Category**: Workflow
- **Location**: .specify/specs/078-bilingual-expression/contracts/measurement.md（绝对：/storage/project/cloud-native-ai/spec-kit/.specify/specs/078-bilingual-expression/contracts/measurement.md）；tasks.md
- **Evidence** (verbatim quote):

  ```
  - **C-003** 测量 MUST 用检查器 `scan --scope changed` ... 每个交付里程碑后各测一次（SC-002 Source）。(SC-002, FR-016)
  ```

  tasks.md 中 changed-scope 测量任务只有 Part 3 的 T010/T011；Part 4（`5aa7168a`）收口门禁（`implement-part4-gates.txt`）无 changed-scope 复跑；`features.md` 078 行翻转内容（Part 4 新写）直到 review 修复轮复跑（`us18`，11:58:46Z）才被测量——该文件带入的 14 条 finding 全部落在其它特性的存量行上、可分类，但若带入了真违规， implement 收口时不会被看见。

- **Why it's a problem**: 测量 cadence 写在契约里但没有任务化，长 implement（分段）只在中间段测一次；收口段的合规率测量缺口要等 review 才补上。
- **Proposed fix**: 契约测量任务模板（或 templates/tasks-template.md 的 Polish/Closure 分组提示）增一行默认项：「每段收口复跑 changed-scope 测量并落 test-evidence」；或把 C-003 的「交付里程碑」收窄定义为「最终交付」，消除两读法。
- **Detected**: direct read, subagent unavailable

### F3 — `git-delta-review.sh receipt` 无显式 base 时按 `main` 合并基解析，与记录头不一致并拒绝写块

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: .specify/skills/internal/code-review/scripts/git-delta-review.sh（框架源：skills/internal/code-review/scripts/git-delta-review.sh）
- **Evidence** (verbatim quote):

  ```
  $ git-delta-review.sh receipt --review-file .specify/specs/078-bilingual-expression/code-review.md
  行数无法测量 (binary): .specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png
  不可量测的数字字段意味着不写块 (C-41 / V16)   （退出 2）
  ```

  本仓 `git merge-base HEAD main` = `926836e0`（上游世系），而记录头与 `base` 子命令解析出的评审基是 `7c835ba6`（feature-first-commit 层）；`926836e0..HEAD` 引入无关二进制文件使 numstat 出 `-` 字段。

- **Why it's a problem**: 非交互五步路径的第 4 步在「记录已携带 base/head」的常见情形下仍要调用方显式传参，否则解析到错误世系并退出 2；每个在本仓跑 review 的使用者都要踩一次。
- **Proposed fix**: `cmd_receipt` 在 `--base`/`--head` 缺省时优先复用记录头已登记的 base/head（记录头即同脚本 `start` 所写，来源已声明），世系不一致时再要求显式覆盖。
- **Detected**: direct read, subagent unavailable

## 4. What Worked — Preserve (Brief)

- review 抽样由程序给出（`sample_lines`，k=⌈n/10⌉）——C-004 的设计本轮实证抓到一个真缺陷（F1/代码段 important），评审自选样本做不到这种不可操纵性。
- SC 分面纪律（implement 面 pass 不预支 review 面）+ verification.md 逐面四键记账，review 阶段有据可依、无回溯性编造。
- 程序派生而非硬编码：SC-001 关键词表由 owner 文档列表项派生、镜像清单由 `sync-mirrors.py MIRROR_PAIRS` 派生（`test_drift_mirror_identity_derived_from_mirror_pairs`）。
- E6 存量差异清单 append-only、dated run 头（`<!-- run: … files_scanned=… findings=… -->`），修复后复跑自然追加新 run 而不改写历史。
- 镜像同步由 `sync-mirrors.py --write` 单点执行，修复轮未手改 `.specify/` 镜像。

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **REC-078-01（真实输入形状契约腿）** — Target: `templates/tasks-template.md` § Tests（绝对补充：/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md）。Change: Tests Mode 要求增一条——消费既有注册输入（词汇表/登记表/状态脊等）的机械守卫，每个 action 至少一条契约腿钉真实输入形状或程序派生的同形状合成夹具。Source: F1。Expected impact: 堵住「夹具全绿、真实输入静默失效」一类缺口，不需要再靠评审抽样兜底。
- **REC-078-03（receipt 复用记录基）** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` `cmd_receipt`（绝对补充：/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh）。Change: `--base`/`--head` 缺省时优先读记录头登记的 base/head，世系不符再要求显式覆盖。Source: F3。Expected impact: 非交互五步路径第 4 步在常见情形下零摩擦通过。

### 5.4 Workflow Improvements

- **REC-078-02（测量 cadence 任务化）** — Target: `shared/workflow/` 测量契约惯例（本特性载体：`.specify/specs/078-bilingual-expression/contracts/measurement.md` C-003；推广落点为后续特性的 measurement 契约模板与 tasks 模板）。Change: 「每个交付里程碑后各测一次」改为可任务化的默认收口项（每段复跑 changed-scope 测量并落 test-evidence），或把「交付里程碑」收窄定义为最终交付。Source: F2。Expected impact: 分段 implement 的收口段合规率测量不再依赖 review 兜底。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-078-01 真实输入形状契约腿 | `templates/tasks-template.md` § Tests | F1 |
| P2 | REC-078-02 测量 cadence 任务化 | `shared/workflow/` 测量契约惯例 | F2 |
| P2 | REC-078-03 receipt 复用记录基 | `skills/internal/code-review/scripts/git-delta-review.sh` | F3 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
