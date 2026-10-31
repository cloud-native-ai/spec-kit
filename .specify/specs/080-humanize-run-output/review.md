# Specification-Driven Development (SDD) Process Review Report: Humanize Run Output（动作输出的人类友好化）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 079 |
| Requirement Key | `080-humanize-run-output` |
| Requirement Name | Humanize Run Output（动作输出的人类友好化） |
| Related Feature | 062 Humanize Command（动作输出人类友好化） |
| Repository | `spec-kit` (repo root `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`) |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (remote name `gitlab`; SSH-only, so `blob/` URLs cannot be rendered for this remote) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the whole feature line is unpushed. Every citation below uses absolute paths plus `git show <sha>:<path>` recovery. |
| Branch | `080-humanize-run-output` |
| Commit SHA | `cad4bda7b359b3cc684f736065c3d695b21ae816` (short: `cad4bda7`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-31（本地日期；UTC `2026-10-30T16:23Z`。系统日期已跨日，这正是本特性 § 环境日期边界的成因） |
| Reviewer (Agent) | Qoder agent — `review-sdd-process` segment only; the `code-review` segment was **not** dispatched in this run (see § 2.1) |
| Environment | macOS (arm64); system `Python 3.9.6`; repo `.venv` `Python 3.14.6` / `pytest 9.2.0`; `git 2.54.0`; no coverage/`git-delta` reporter used |
| spec-kit Source Snapshot | local framework repo @ `cad4bda7`; `pyproject.toml` version `0.0.22` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| `requirements.md` | 270 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/requirements.md` | 30 FR / 10 SC / 4 US / 15 STR；含 A11 接线封闭集、失败禁用词表、3 轮 analyze 的 Clarifications 记录 |
| `plan.md` | 240 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/plan.md` | 18 行宪法检查（IV = Partial/正当化）、3 条 Decision Tensions、Phase 0 八条设计发现 |
| `data-model.md` | 232 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/data-model.md` | E1–E8、26 条 V 规则、1 个运行状态机 |
| `contracts/` (5 files) | 322 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/contracts/` | 88 条款：IP 17 / EX 21 / RP 20 / CM 10 / WC 20；各带可追溯性表 |
| `quickstart.md` | 245 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/quickstart.md` | S1–S7 + §0 基线读数 + §8 完成判据（含 H-06 补入的 S6-B） |
| `tasks.md` | 372 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/tasks.md` | 36 任务 / 7 相位 / 31 行条款指派 / DoD 9 条 / GATE 7 条 |
| `verification.md` | 268 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/verification.md` | canonical SC 块（8 pass / 2 partial）+ T031–T034 实测 + SC 收口表 |
| `feature-ref.md` | 61 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/feature-ref.md` | Feature 062 扩展绑定与登记面映射 |
| `checklists/run-then-report-2026-10-30.md` | 85 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/checklists/run-then-report-2026-10-30.md` | 39 项需求质量清单（traceability 39/39） |
| `checklists/requirements.md` | 42 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/checklists/requirements.md` | requirements 阶段清单（未被覆盖） |
| `notes/pre-change-measurements.md` | 128 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/notes/pre-change-measurements.md` | 改动前唯一落点：计数 / 接线 164 / 四条基线 / 技能预算 / 覆盖基线复核 |
| `notes/red-first-evidence.md` | 244 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/notes/red-first-evidence.md` | 五个红先行行的真实失败读数（T005/T013/T019/T024/T036） |
| `notes/quickstart-run.md` | 321 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/notes/quickstart-run.md` | S1–S7 运行记录 + teardown + 三条 `not-reproducible` 声明 |
| `notes/report-sample.md` | 26 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/notes/report-sample.md` | S7-B 的 `--output` 样本（901 bytes） |
| `test-evidence/` (34 files) | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/test-evidence/` | 逐阶段 E3 状态、analyze 三轮门禁、修复简报、验证器简报、接线 pin、覆盖基线 |
| `review.md` | this file | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/review.md` | 本报告 |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | clarify 完成（30 FR / 10 SC / 4 US / 15 STR；绑定 Feature 062，状态不回退） | `requirements.md` § Clarifications；`bd8648b7` | none |
| 2 | plan：plan / data-model / 5 contracts / quickstart / feature-ref 落盘；基线 `35ff11bc` | `plan.md`；`70dd9e78` | 宪法自评与质量自查为同作者且未委派（`plan.md:65`，已披露） |
| 3 | tasks：35 行 → 修复后 36 行；88 条款人工指派 31 行 | `tasks.md`；`c0135989` | 条款/FR 机器通道对本特性失明（`form=md-none`；已记录） |
| 4 | checklist：39 项需求质量清单 | `checklists/run-then-report-2026-10-30.md`；`test-evidence/checklist-*.txt` | gap-finding 单上下文（清单 `:78` 已披露） |
| 5 | analyze r1：C0 / H5；9 个只读验证器（5 confirm / 4 downgrade = 44.4%） | `test-evidence/analyze-stage-status.txt:7-8` | none |
| 6 | requirements-fix：H-01…H-04 + 17 条 M | `test-evidence/requirements-fix-status.txt`；`bd8648b7` | none |
| 7 | plan-fix：H-05 + M-04/07/17/19；decision-tensions 0 | `test-evidence/validate-decision-tensions.txt`；`70dd9e78` | none |
| 8 | tasks-fix：H-02、M-03、M-21；接线发现 pin 164（7/4/1/114/38/0） | `test-evidence/tasks-fix-wiring-check.txt`；`c0135989` | none |
| 9 | analyze r2：C0 / H1（H-06）；1 个验证器 confirm；`gate_release=blocked`，停线上送 | `test-evidence/analyze-r2-stage-status.txt:7-11` | none（停线纪律被遵守） |
| 10 | tasks-fix-2（人工授权传播修复）：`denied` 夹具/断言/SC-004 行/quickstart S6-B | `test-evidence/tasks-h06-fix-status.txt`；`9dfa8b2a` | **deviation**: 第二轮仍有 HIGH 后未自动继续，而由人工授权第三轮（规则允许的显式例外） |
| 11 | analyze r3：C0 / H0；验证器派发两次失败（151 s error / 71 min hang）→ 同作者直读兜底；L-03/L-04 结转 | `test-evidence/analyze-r3-stage-status.txt:8-14` | **deviation**: 独立校验腿未跑通，按既定 fallback 记录 |
| 12 | implement 起点 E2：全量 6881 passed / 17 failed / 7 skipped / 998 s；17 条失败名落 `baseline-failed.txt` | 状态脊 test-budget 块；`test-evidence/implement-part1-status.txt:43` | none（预算槽位正确消耗） |
| 13 | implement part 1–5：T001–T036；每段 E3 状态 + `new_failures` 归属表 + 就地修正披露 | `test-evidence/implement-part1..5-status.txt`；提交 `83c4629a`…`6ea12a49` | 首红缺陷在段内改正（T036 4 红中 3 条为测试自身缺陷；见 F6） |
| 14 | verification canonical SC 块 + 回填 `post_change_commit` | `verification.md:3-55`；`46394dd4`、`cad4bda7` | **deviation (unrecorded)**: `gate-implement-evidence-binding` 未执行，也无 any firing evidence（F1） |
| 15 | review（本次）：过程段；定向集 172 passed | `test-evidence/review-targeted.txt`、`review-stage-status.txt` | **deviation**: `code-review` 段未派发，`code-review.md` 不存在（F9） |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 8 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 4 |
| Workflow | 4 |
| Documentation | 2 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `cad4bda7` | driver-supplied `stage_base` (the previous stage commit); the feature's own delta would resolve from `35ff11bc` |
| Head commit | `cad4bda7` | run-start `HEAD`, fixed for this run |
| Base source | driver stage base (explicit) | run directive |
| Renderer mode | `n/a (no code record)` | no `code-review.md` exists |
| Changed / judged / skipped / gap files | `n/a / n/a / n/a / n/a` | no coverage receipt was produced — the code segment did not run |
| Segment verdict | `not-evaluated` | reason: this stage's directive limits the review object to the SDD process; the `code-review` skill was not loaded and no subagent was dispatched |
| Gate verdict | `not-evaluated` | the `Implemented → Ready for Review` transition was not judged; no `code-review.md` existence test was performed |
| Reason, when one applies | `not-evaluated`: 本阶段指令把评审对象限定为 SDD 过程（process segment only），code segment 未派发，故无 coverage receipt、无合并门判定 | run directive; `templates/commands/review.md:31,105` |
| Uncommitted scope | 工作树未被评审：`M .specify/memory/session/20261029T101833Z-run-determination-speckit-checklist-r20261029t172918z-076a-c.md`（既有脏文件，未触碰）、`?? .specify/specs/080-humanize-run-output/baseline-failed.txt`、`?? .specify/state/080-humanize-run-output.md`（驱动状态脊）。本报告不据此作出任何通过结论。 | `git status --short` at review time |
| Record | `not written` | triage value is not `run` |
| Archive | `none` | first review run for this feature |

## 3. Findings (Problems & Improvement Targets)

### F1 — 证据绑定门 `gate-implement-evidence-binding` 未执行：8 条 `pass` 按模板定义为 unverified（P0）

- **Severity**: P0 (validated: direct re-read, subagent unavailable — the stage directive prohibits dispatch)
- **Category**: Automation
- **Location**: `.specify/specs/080-humanize-run-output/verification.md:12-50`（绝对路径：`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/080-humanize-run-output/verification.md`）；owner：`templates/verification-log-template.md:54-66`；gate 义务：`skills/internal/implement-feature/SKILL.md:319`
- **Evidence** (verbatim quote):

  ```
  SC-008_status=pass
  ...
  deferred_tasks=
  ```

  ```
  # Rules: a `pass` verdict REQUIRES a complete evidence row — all four keys, no
  # blanks. ... A `pass` without a complete evidence row is `unverified` and MUST
  # NOT be cited as passing evidence anywhere downstream.
  ```

  ```
  > Gate probe: gate-implement-evidence-binding — after populating the evidence
  > records, run the binding check per the template's declared rules: every sample
  > recorded `pass` MUST have a complete evidence row whose archived artifact
  > exists, is non-empty, and whose computed SHA-256 equals the recorded hash
  ```

  实测（本次 review 复算）：`grep -c 'sample_id=' .specify/specs/080-humanize-run-output/verification.md` → `0`；同文件 `grep -c '_status=pass'` → `8`、`_status=partial` → `2`。相邻特性均按四键落行（076 = 8 行、077 = 8 行、078 = 9 行）。
- **Why it's a problem**: `verification.md` 的 8 条 `pass` 没有 `sample_id` / `evidence_path` / `evidence_sha256` / `verdict` 四键证据行，模板把这种状态明确定义为 `unverified`，并禁止下游把它当作通过证据引用；而 closure 与合并正是它的下游。`gate-implement-evidence-binding` 是注册过的 command-gate，本轮既没有执行记录，也没有「未触发」的 disclosure——这是一次**静默跳过的门**，而不是已披露的降级。该文件同时是 SC 的唯一索引（`verification.md:59`），因此缺口不会被别的产物自动暴露。
- **Proposed fix**: 在 closure 前为每条 `pass` SC 补一行四键证据（指向已提交的 `test-evidence/*.txt` 或 `notes/quickstart-run.md`，计算 SHA-256），并复跑绑定检查；同时在 `skills/internal/implement-feature/SKILL.md` § Step 9 增加一条可直接执行的检查命令，把「未记录」与「记录但哈希不符」合并为同一种 RED。

### F2 — 同一份 `verification.md` 对 SC-001 / SC-004 给出两个相反判定（P1）

- **Severity**: P1
- **Category**: Documentation
- **Location**: `.specify/specs/080-humanize-run-output/verification.md:12,24,57,187,190`
- **Evidence** (verbatim quote):

  ```
  SC-001_status=partial
  ...
  SC-004_status=partial
  ...
  **指针**：canonical 状态以上方 `SC-NNN_status=` 块为准；下方表格是逐条证据正文。
  ...
  | **SC-001** | 达成（五节 5/5；派发记录的原生 `1` 腿受宿主限制，降级载体取 `0`） | ...
  | **SC-004** | 达成（无副作用 1/1；`denied` + `aborted` + 拒绝原因/未执行范围 2/2）。运行腿 `not-reproducible` ...
  ```
- **Why it's a problem**: canonical 块与收口表对同一条 SC 分别写 `partial` 与「达成」。虽然文件声明 canonical 块优先，但收口表是读者与 closure 最先浏览的「逐条证据正文」，两个判定并列会让“到底过没过”取决于读哪一段。这是典型的 One-Source-Of-Truth 漂移，且发生在本特性唯一的 SC 索引里。
- **Proposed fix**: 让表格的状态列从 canonical 块派生（或直接删掉状态词，只留证据指针）；在 `templates/verification-log-template.md` 里禁止第二处用自然语言重述 SC 状态。

### F3 — 条款与 FR 两条机器覆盖通道对本特性完全失明，覆盖改由每特性手写的判定器承担（P1）

- **Severity**: P1
- **Category**: Automation
- **Location**: `.specify/specs/080-humanize-run-output/tasks.md:55,369`；`scripts/python/clause_extract.py`；`scripts/python/account-clause-coverage.py`
- **Evidence** (verbatim quote):

  ```
  **不使用 `[green:]` 绿点标签**: 本特性的契约条款使用 `IP` / `EX` / `RP` / `CM` / `WC` 两字母命名空间，
  `.specify/scripts/python/clause_extract.py` 只识别 `C-<n>` 形态 ... 同一做法见 066 / 067 的 tasks.md。
  ```

  ```
  `clause_extract.py` 实测 `form=md-none`，因而 `account-clause-coverage.py` 的条款车道与 FR 车道都看不见这 88 条（FR 车道 0/30）
  ```
- **Why it's a problem**: `account-clause-coverage.py` 的两条机器覆盖通道（条款车道、FR 车道）对 88 条条款与 30 条 FR 都返回 0；覆盖只能靠 `§ Contract Coverage Map` 人工指派 + 每特性自写的 `test_wc12_clause_test_map_is_total`。本特性的判定器要反过来解析 `tasks.md` 的 31 行与五份契约的可追溯性表，等于把「规划制品的措辞」变成测试输入。tasks.md 自己写明 066 / 067 用了同一做法——这不是一次性成本，而是复用中的固定税。
- **Proposed fix**: 让 `clause_extract.py` / `contract-clause-definitions.md` 接受可配置的条款命名空间（或在校验期把 `IP-01` 归一化为 `C-<n>`），使 `account-clause-coverage.py` 能看见非 `C-<n>` 契约；在迁移完成前，把「自写判定器」登记为已知债务而不是每个特性重新发明。

### F4 — quickstart 的「真实执行」只执行了内层命令，报告正文由实现者撰写，来源清单无观测（P1）

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/080-humanize-run-output/notes/quickstart-run.md:8,20-48`；`.specify/specs/080-humanize-run-output/verification.md:75`
- **Evidence** (verbatim quote):

  ```
  **记录口径**: 每条给出调用原文、真实执行的命令、真实输出与退出码；报告只摘录判定行与证据行，
  全文形态由 `tests/contract/test_humanize_command_surface.py` 的五节断言承载。
  ...
  $ python3 -c "print('humanize-fixture-ok')"
  humanize-fixture-ok
  exit=0
  ...
  - 来源清单：instructions / constitution / glossary / features(062 行投影) / 本次会话（均 read）；缺失来源：无。
  ```

  ```
  S1 成功 / S2 失败 / ... 均以 `mode: in-session-degraded` 真实执行并记录。
  ```
- **Why it's a problem**: 被真实执行的是指令的内层 shell 命令；`/speckit.humanize` 的解析、占位、报告装配没有作为一个端到端调用发生，报告行是事后按 SKILL 文本写的（文件自己说“只摘录判定行”）。S1 声称“五节标题逐字按序”，但记录的样本只含 Conclusion / Evidence / Risks 三节；“来源清单均 read”没有任何读取观测支撑。verification 又把整段概括为“真实执行并记录”。这使 SC-001/SC-002 的验收证据在“执行过”与“照规范写过”之间不可区分——而本特性的交付物恰恰是提示词行为，二者的差别就是证据的全部价值。
- **Proposed fix**: 在 implement 的 quickstart 证据规范里引入封闭的「执行级别」枚举（`end-to-end` / `inner-command-only` / `fixture-substituted`），逐场景标注，并禁止对非 `end-to-end` 使用“真实执行”措辞；来源清单这类断言必须绑定可观察的读取痕迹（例如本轮实际打开的文件列表）。

### F5 — analyze 第三轮的独立校验腿两次失败（含 71 分钟挂起），H-06 的关闭退回同作者直读（P1）

- **Severity**: P1
- **Category**: Automation
- **Location**: `.specify/specs/080-humanize-run-output/test-evidence/analyze-r3-stage-status.txt:8`
- **Evidence** (verbatim quote):

  ```
  validation_wave=H-06 closure review: 2 read-only external dispatches attempted (qodercli -p, --tools Read Grep Glob Bash --permission-mode auto --no-session-persistence). Dispatch 1 exited error_during_execution after 5 turns / 151s; dispatch 2 hung after its last tool result (83 stream events, no verdict) and was killed at 71 min. Two consecutive failures -> documented fallback: direct evidence re-read by the analyzing agent (validated: direct re-read, subagent unavailable).
  ```
- **Why it's a problem**: H-06 是 analyze 第二轮唯一 HIGH、也是 implement 放行的唯一阻断项；它的关闭本应由独立上下文复核。派发层在 151 秒报错、在 71 分钟无输出地挂起，最终由同作者直读兜底。外部校验的价值因此在这一轮归零，而失败只以一行文字留在证据文件里，没有超时、重试上限或无进展检测的机制化处理。71 分钟的静默也直接违反 Progress Reporting Discipline 的 15 分钟上限。
- **Proposed fix**: 给派发 helper 加墙钟上限（例如 10–15 分钟）与「连续 N 个 stream event 无 verdict」的判死条件；把 fallback 率作为派发层的一个可观测量；在 fallback 发生时自动在阶段状态里写入 `validated: direct re-read`，而不是靠人记得写。

### F6 — 红先行的首红质量不足：4 条中 3 条是测试自身构造缺陷，1 条在任何实现下都不可能为真（P1）

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/080-humanize-run-output/test-evidence/implement-part4-status.txt:58-59`；`implement-part5-status.txt:83`；`notes/red-first-evidence.md:14`
- **Evidence** (verbatim quote):

  ```
  1. `tests/contract/test_humanize_command_surface.py::test_cm03_no_report_scaffold_in_content_mode`：... 该断言在任何实现下都不可能为真。
  2. 同文件 `test_cm10_content_mode_wording_intact`：锚点要求文本含「不是兼容垫片」，而禁用词表又禁止子串「兼容垫片」，两者互斥。
  ```

  ```
  1. T036 首次运行 4 红中 3 条是测试自身构造缺陷 ...
  ```

  ```
  为取得真实红态，运行时临时移出该文件、跑完即还原；这是红态的如实重建，不是删产物。
  ```
- **Why it's a problem**: 红先行的信号是「测试因缺少目标行为而红」。本特性出现了不可能为真的断言、互相矛盾的锚点、以及靠临时移出实现文件重建的红态。这些都在段内被就地改正并披露（这一点值得保留），但它们说明首红的分类没有被机器把关：一个永远不可能转绿的测试与一个真实红先行测试在首次运行时长得一模一样。T005 的红态还是事后重建的，执行顺序因此只能靠补记，不能从运行本身证明。
- **Proposed fix**: 在红先行行里要求记录「红的原因」枚举（`missing-artifact` / `wrong-assertion` / `contradictory-anchor`），并在声明红先行前用一个最小合规样本跑一次「该测试能否转绿」；把临时移出实现文件的做法列为禁止的重建方式（它破坏执行顺序证据）。

### F7 — 技能正文停在 4999 / 5000 tokens，任何后续一行都会让门变红（P1）

- **Severity**: P1
- **Category**: Template
- **Location**: `skills/external/humanize/SKILL.md`（154 行）；判定器 `skills/external/improve-skills/scripts/skill-shape.py`
- **Evidence** (verbatim quote):

  ```
  正文估算     ≈4999 tokens 可控 / 预算 5000（154 行）
  最大章节     Workflow
  发现：
    ! [oversized-section] Workflow=59行（单章节建议上限 40 行）
  ```

  plan 阶段的实测是 4090 / 5000，并据此决定把运行模式细则放进 `references/`：
  ```
  因为正文已经 ≈4090 tokens / 预算 5000，把载荷字段与报告形态塞进正文会直接超预算（WC-07）
  ```
- **Why it's a problem**: 设计期的 910 token 余量在实现期被消耗到只剩 1 token。预算是一个硬门，却没有任何“保留余量”的规则；下一个想改 humanize 正文的特性一开始就是红的。同时 `Workflow` 59 行、45 个 flag 出现在非约束章节，说明正文已经在承担手册职责，只是被 references 拆分暂时压住了。
- **Proposed fix**: 给 `skill-shape.py` 增加“接近上限”的分级（例如 >95% 报 warning，且不允许以 1 token 余量通过），或在技能模板中规定正文上限的 90% 作为实际写作目标、把余量留给下一次修改。

### F8 — analyze 修复简报没有「传播面」字段，M-09 在 requirements 关闭后没有下游义务（P1）

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/080-humanize-run-output/test-evidence/analyze-fix-brief.md:23,39`；`test-evidence/analyze-r2-stage-status.txt:11`
- **Evidence** (verbatim quote):

  ```
  - **M-09**：用户拒绝确认时无 `denied` 状态 → 增加 `denied` 并给出 verdict 映射（建议 `aborted` + 文案）。
  ...
  - **requirements 轮**：H-01、H-02、H-03、H-04、M-01、...、M-09、...
  ```

  ```
  round1_medium=all 21 M rows dispositioned: 20 closed on their owning artifact, 1 (M-09 denied) closed on requirements but its tasks-side propagation is missing → raised as H-06
  ```
- **Why it's a problem**: M-09 的修复归属只写了 requirements，没有要求把新状态传播到 tasks 的 T004/T010/T019、quickstart S6 与 SC-004 覆盖行。第一轮因此“关闭”了它，第二轮又以 H-06 的形式重新发现，触发停线、人工授权与第三轮 analyze。修复简报缺一个「本条改动必须传播到哪些制品」的字段，是这三轮成本的可归因部分。
- **Proposed fix**: 在 analyze 的修复简报模板里为每条 finding 增加 `propagation` 字段（owner → plan → contracts → tasks → quickstart → SC 覆盖行），并要求修复轮按该字段逐项声明关闭位置；没有传播面的条目必须显式写 `none`。

### F9 — `/speckit.review` 的固定双段组合在无人值守 review 阶段只跑了过程段（P1）

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `templates/commands/review.md:31,105`；实测缺失 `.specify/specs/080-humanize-run-output/code-review.md`
- **Evidence** (verbatim quote):

  ```
  `/speckit.review` runs exactly two segments in a fixed order. There is no parallel mode, no single merged report, and no parameter — `$ARGUMENTS` included — that selects one segment over the other: the order is a property of this template, so neither delegated skill may reverse or skip the other.
  ```

  ```
  The criteria — three conjunctive conditions, the third an existence test over the current `code-review.md` — are owned by `templates/feature-details-template.md` § Canonical Status State Machine.
  ```

  实测：`ls .specify/specs/080-humanize-run-output/code-review.md` → `No such file or directory`。
- **Why it's a problem**: 命令模板把双段写成不可选择、不可跳过；无人值守的 review 阶段却只派发了过程段，所以第三个条件（`code-review.md` 存在）从未被检验，`Implemented → Ready for Review` 的迁移也没有被判定。模板允许 `not-evaluated` 的代码段不阻塞迁移，但前提是它被显式记录；本特性连 `code-review.md` 与代码段记录都不存在，读者无法区分“代码段没跑”与“跑了但没发现问题”。该缺口已在 078 评审登记为 **REC-078-07**（`.specify/memory/register.md`，`open`），本特性再次命中——这是复发，不是新发现。
- **Proposed fix**: 执行已登记的 **REC-078-07**：为 `/speckit.review` 增加一个非阻断的 process-only triage 值，并把未判定的迁移门写进 § 2.1。若该行短期不落地，至少由驱动侧在 review 阶段补写 `not-evaluated` 的代码段记录。

### F10 — plan 与 checklist 的同作者自评没有独立复核，只有 analyze 阶段补上了（P2）

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/080-humanize-run-output/plan.md:65`；`checklists/run-then-report-2026-10-30.md:78`
- **Evidence** (verbatim quote):

  ```
  本 plan 的评分与 § Post-Generation 质量自查由同一 agent 完成；按 `.specify/shared/workflow/objective-analysis-gate.md`，同作者条件成立时评分应委派 fresh-context 只读子代理。本线的执行约束明确禁止派发子代理，因此此处**未委派**
  ```

  ```
  This line's execution constraint forbids dispatching subagents, so the gap-finding pass was single-context. Recorded here as a methodological limitation for `/speckit.analyze` (read-only, independent context) to re-check; it is not a claim of coverage.
  ```
- **Why it's a problem**: 两条框架规则直接冲突：objective-analysis-gate 要求同作者时委派独立上下文，而无人值守驱动禁止派发子代理。本特性用“披露 + 交给 analyze 复核”化解，但 plan 的 18 行宪法评分与 checklist 的 39 项 gap 发现因此在产生它们的阶段没有任何独立证据；analyze 第一轮用 9 个 qodercli 验证器补上了，说明这条腿本来是可行的——冲突只是没有被规则化。该缺口已在 078 评审登记为 **REC-078-06**（`open`），本轮再次命中。
- **Proposed fix**: 执行已登记的 **REC-078-06**：在 `objective-analysis-gate` 增加 `operating-constraint` 降级理由与规定标记，并把禁派发阶段的 analyze handoff 行清单写成固定形态，替代每阶段各写一段说明。

### F11 — `tasks.md` 的 DoD Status 停在 `pending`，36/36 任务已完成却无人翻绿（P2）

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/080-humanize-run-output/tasks.md:28`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: pending
  ```

  实测：`grep -cE '^- \[X\] T[0-9]{3}'` → `36`；`grep -cE '^- \[( |>)'` → `0`；同仓其他 `tasks.md` 的 DoD Status 大多已翻为 `green` / `complete` / `done`（`grep -h 'DoD Status' .specify/specs/*/tasks.md`，21 行 `green` 之外还有 `complete` / `done` / `implemented` 等终态）。
- **Why it's a problem**: 任务全绿、verification 已收口，DoD 状态却仍是 `pending`。这不是业务缺陷，而是流程缺少一个明确的“翻绿”所有者：本特性的 T035 只写“SC 收口与留档”，没有一行负责 DoD Status；其他特性通常由 Polish 行显式翻绿。closure 若扫描 DoD Status，会读到一个与事实相反的信号。
- **Proposed fix**: 在 `templates/tasks-template.md` 的 Polish 相位固定一行“逐条核对 DoD-N 并把 DoD Status 翻为 green/complete”，或让 `validate-tasks.py` 在所有 `[X]` 且 `verification.md` 存在时对 `pending` 报 warning。

### F12 — Feature 062 的 `## Overview` 仍只描述旧的文本改写定位，与新名称/描述及扩展记录漂移（P2）

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/memory/features/062.md:10-12`（绝对路径：`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/062.md`）
- **Evidence** (verbatim quote):

  ```
  ## Overview

  机器生成的内容、结论与报告常带套话、密集段落与机械句式 ... 本 Feature 为框架新增通用内容能力 `/speckit.humanize`：在保真底线 ... 从四个维度改写调用者提供的内容
  ```

  同文件头部已改成：
  ```
  **Description**: `/speckit.humanize` 是动作输出的人类友好化命令——调用者给一条指令，命令派发恰好一个执行体跑完它 ...
  ```
- **Why it's a problem**: 扩展登记（`## Latest Review` / `## Key Changes`）完整记录了 079，但任何只读 `## Overview` 的读者会得到旧定位：humanize 是一个内容改写命令。名称、描述、索引行都已迁移，Overview 成为唯一的反向事实源。
- **Proposed fix**: 在 `templates/feature-details-template.md` 或 manage-features 技能里规定：当扩展改变 Feature 的定位时，`## Overview` 必须同步或在开头加一行“本节保留原始定位，079 扩展见 Key Changes”；由扩展登记任务承担该义务。

## 4. What Worked — Preserve (Brief)

- **A11 封闭接线面**：无限制发现 + 五类有序规则 + 四项闭环守卫，分母钉在基线提交 `35ff11bc` 上（164 = 7+4+1+114+38，unclassified 0），实现后重跑 `comm -3` 仍为空；新增的 spec/证据文件不会污染分母。
- **analyze 三轮的停线纪律**：第二轮仍有 HIGH 时没有自动继续修复，而是停线上送并给出三个处置选项；第三轮由人工授权执行，属于显式例外而非静默放行。
- **逐段 E3 + `new_failures` 归属**：implement 五段各自记录命令、rc、passed/failed、新失败归因（预期红先行 / owner-row / 既有基线），并如实声明“全量未重跑”。
- **就地修正的披露形态**：段内改正的测试缺陷、矛盾锚点、夹具措辞都逐条写明“原断言为何不可能成立 / 改了什么 / 强度是否变化”。
- **canonical SC 块承认 partial**：SC-001 与 SC-004 没有被粉饰成 pass，`not-reproducible` 的三条限制（并发、用户拒绝、原生载体）逐条落到台账。
- **机器可判定优先**：T036 的 `test_wc12_clause_test_map_is_total` 真正解析 88 条条款、31 行指派与测试函数，而不是靠人工表声明“零缺口”；`UNCHANGED_SHA256["humanize"]` 重测保留 `strip_wiring()` 基线判定。
- **测试预算未被透支**：全量套件只在 implement 起点跑过一次（998 s，17 条既有失败落 `baseline-failed.txt`），后续全部定向集；review 本次复跑两个契约文件 172 passed。
- **Feature 062 登记不回退**：状态保持 `Implemented`，`## Latest Review` / `## Key Changes` / 索引行三处同步，未新建 Feature 行。

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-080-01 — 技能正文预算保留余量** — Target: `skills/external/improve-skills/scripts/skill-shape.py`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/improve-skills/scripts/skill-shape.py`），并同步 `templates/` 的技能写作说明。Change: 在 100% 硬上限之外增加 95% warning 档，或把“写作目标”定义为上限的 90%，禁止以个位数 token 余量通过。Source: F7. Expected impact: 下一个改 humanize 正文的特性不会一开始就红。

### 5.2 Command Prompt Improvements

- **REC-078-07（已登记，未落地）— 为 `/speckit.review` 增加非阻断的 process-only triage 值** — Target: `templates/commands/review.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/review.md`）。Change: 按已登记行的原意落地：调用方限定只跑过程段时，§ 2.1 写 `not-evaluated` 与缺席证据，迁移门保持未判定。Source: F9. Expected impact: 读者不再需要从“没有 `code-review.md`”反推代码段是否跑过。

### 5.3 Automation / Script Improvements

- **REC-080-02 — 让证据绑定门可执行、可失败** — Target: `scripts/python/` 新增一个 `check-verification-evidence.py`（或把等价逻辑并入 `gate-implement-evidence-binding` 的调用行），由 `skills/internal/implement-feature/SKILL.md` § Step 9 显式调用。Change: 解析 `verification.md` 的 SC 状态与四键证据行，重算 SHA-256；任何 `pass` 缺行 / 空文件 / 哈希不符即 RED，并输出 sample id。Source: F1. Expected impact: F1 这一类“门存在但没跑”不会再静默通过。
- **REC-080-03 — 让条款/FR 覆盖通道识别非 `C-<n>` 命名空间** — Target: `scripts/python/clause_extract.py` 与 `shared/definitions/contract-clause-definitions.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md`）。Change: 支持按契约声明的命名空间前缀（如 `IP/EX/RP/CM/WC`），或在扫描期归一化为 `C-<n>`；迁移前把“每特性自写判定器”登记为已知债务。Source: F3. Expected impact: 88 条款与 30 FR 不再对机器车道隐形，066/067/079 不再各自重写判定器。
- **REC-080-04 — 派发层加墙钟与无进展判死** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md` 的验证器派发 helper（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/stage-prompts.md`），并同步 analyze 的 fallback 条款。Change: 单次派发设 10–15 分钟墙钟上限；“连续 N 个 stream event 无 verdict”判死；fallback 自动写入 `validated: direct re-read` 并上报 fallback 率。Source: F5. Expected impact: 71 分钟静默挂起与“靠人记得写 fallback”同时消失。
- **REC-080-05 — 让 DoD Status 有明确翻绿所有者** — Target: `templates/tasks-template.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md`）。Change: Polish 相位固定一行“逐条核对 DoD-N 并翻绿”；或 `validate-tasks.py` 在 36/36 `[X]` 且 `verification.md` 存在时对 `pending` 报 warning。Source: F11. Expected impact: closure 不再读到与事实相反的 DoD 信号。

### 5.4 Workflow Improvements

- **REC-080-06 — analyze 修复简报增加 `propagation` 字段** — Target: `skills/internal/analyze-artifacts/SKILL.md` 与 `templates/commands/analyze.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md`）。Change: 每条 finding 的修复行必须列出 owner → plan → contracts → tasks → quickstart → SC 覆盖行的传播面；无传播面显式写 `none`，修复轮逐项声明关闭位置。Source: F8. Expected impact: M-09 这类“需求侧关闭、下游未接”的 HIGH 不会在下一轮才被发现。
- **REC-080-07 — quickstart 证据引入封闭的执行级别** — Target: `skills/internal/implement-feature/SKILL.md` 的 quickstart 证据规范（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`）。Change: 逐场景强制标注 `end-to-end` / `inner-command-only` / `fixture-substituted`；非 `end-to-end` 禁止写“真实执行”；来源清单类断言必须绑定可观察读取痕迹。Source: F4. Expected impact: SC-001/SC-002 的执行证据不再与“照规范写的样本”混同。
- **REC-080-08 — 红先行增加“该测试能否转绿”的自检** — Target: `skills/internal/implement-feature/SKILL.md` 与 `templates/tasks-template.md`。Change: 红先行行记录红的枚举原因，并在声明前用最小合规样本验证该测试可转绿；禁止用“临时移出实现文件”重建红态。Source: F6. Expected impact: 首红从“看起来红”变成“因缺目标行为而红”。
- **REC-078-06（已登记，未落地）— 同作者门禁增加 operating-constraint 标记** — Target: `shared/workflow/objective-analysis-gate.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/workflow/objective-analysis-gate.md`）。Change: 按已登记行的原意落地：定义 `operating-constraint` 降级标记与固定的 analyze handoff 行清单。Source: F10. Expected impact: 同作者缺口的披露位置与复核范围可机器核对。

### 5.5 Documentation Improvements

- **REC-080-09 — 一份 verification 只允许一个 SC 判定源** — Target: `templates/verification-log-template.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`）。Change: 禁止收口表用自然语言重述 SC 状态；状态列必须从 canonical 块派生，或只保留证据指针。Source: F2. Expected impact: 同一 SC 不再同时是 `partial` 与“达成”。
- **REC-080-10 — 扩展改变定位时强制同步 Feature Overview** — Target: `templates/feature-details-template.md`（absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/feature-details-template.md`）与 manage-features 技能。Change: 扩展若改变 Feature 定位，`## Overview` 必须同步，或在开头声明“保留原始定位，扩展见 Key Changes”。Source: F12. Expected impact: Feature 详情不再出现“头部新定位、正文旧定位”的反向事实源。

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-080-02 证据绑定门可执行、可失败 | `scripts/python/` + `skills/internal/implement-feature/SKILL.md` | F1 |
| P1 | REC-080-03 条款/FR 通道识别非 `C-<n>` 命名空间 | `scripts/python/clause_extract.py` + `shared/definitions/contract-clause-definitions.md` | F3 |
| P1 | REC-080-06 修复简报增加 `propagation` 字段 | `skills/internal/analyze-artifacts/SKILL.md` | F8 |
| P1 | REC-080-04 派发层墙钟与无进展判死 | `skills/external/sdd-loop-driver/references/stage-prompts.md` | F5 |
| P1 | REC-080-07 quickstart 证据执行级别 | `skills/internal/implement-feature/SKILL.md` | F4 |
| P1 | REC-080-08 红先行“能否转绿”自检 | `skills/internal/implement-feature/SKILL.md` + `templates/tasks-template.md` | F6 |
| P1 | REC-080-01 技能预算保留余量 | `skills/external/improve-skills/scripts/skill-shape.py` | F7 |
| P1 | REC-078-07（已登记）review 的 process-only triage | `templates/commands/review.md` | F9 |
| P1 | REC-080-09 一份 verification 只允许一个 SC 判定源 | `templates/verification-log-template.md` | F2 |
| P2 | REC-078-06（已登记）同作者门 operating-constraint 标记 | `shared/workflow/objective-analysis-gate.md` | F10 |
| P2 | REC-080-05 DoD Status 翻绿所有者 | `templates/tasks-template.md` | F11 |
| P2 | REC-080-10 扩展时同步 Feature Overview | `templates/feature-details-template.md` | F12 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason — none needed here.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report — a manual scan found none; the only bracketed literals are the `[x]` checkboxes in this checklist.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status**: 1 P0 raised (F1). It was validated by a direct evidence re-read — `grep -c 'sample_id=' …/verification.md` → `0`, `grep -c '_status=pass'` → `8`, `ls …/code-review.md` → absent — with the snapshot captured at diagnosis time (`verification.md:40`, `:52`; `templates/verification-log-template.md:57-62`). Recorded as `(validated: direct re-read, subagent unavailable)` because the stage directive prohibits subagent dispatch; the weaker evidence path stays visible.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

## 9. 结论：是否可进入 closure 与合并

**暂不可进入 closure 与合并。** 阻塞项只有一条：

- **F1（P0）**——`verification.md` 的 8 条 `pass` 没有四键证据行，按 `templates/verification-log-template.md` 的定义均为 `unverified`，且 `gate-implement-evidence-binding` 无执行记录。closure 不得引用这 8 条 `pass` 作为通过证据。修复成本低（补 8 行指向已提交证据文件的记录并复算 SHA-256），但必须在 closure 之前完成，否则合并门建立在未验证的 SC 上报上。

P1 不构成硬阻塞，但其中 **F2（同一文件两个相反判定）** 与 **F4（quickstart“真实执行”结论过强）** 直接决定 closure 读到什么，建议与 F1 同批处理；其余 P1（F3/F5/F6/F7/F8/F9）可登记为框架债务并进入下一轮改进。P2 可留到 sanitize/下一特性。

**合并面的事实**：分支 `080-humanize-run-output` 未 push（`git branch -r --contains HEAD` 为空），本线只可能做本地合并；合并动作本身未被本次评审授权，本次也未执行。**状态迁移**：`Implemented → Ready for Review` 未被判定（code segment 未派发，见 § 2.1 / F9），因此不得提前翻状态。

**本次复算的通过面**（供 closure 参考，不替代 F1 要求的四键证据行）：`.venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py tests/contract/test_stage_class_wiring.py` → `172 passed, 1 warning`，rc=0；`regen-command-copies.py --check` rc=0；`sync-mirrors.py --check` 六对全 ok；`skill-shape.py` 判 `pass`（≈4999 / 5000 tokens）。完整输出见 `test-evidence/review-targeted.txt`。

## Post-review repair (2026-10-31)

修复范围仅限本文件的同批处置对象 **F1（P0）/ F2（P1）/ F4（P1）**；实现代码与 `requirements.md` / `plan.md` / `contracts/` / `tasks.md` 未改动。修复只落在 `.specify/specs/080-humanize-run-output/verification.md`、本文件与新增证据 `test-evidence/review-repair-binding-check.txt`。

### F1（P0）— 8 条 `pass` 的证据绑定已补，绑定自检 rc=0

在 `verification.md` 的 canonical 块中新增 8 条四键 Evidence record（`sample_id` / `evidence_path` / `evidence_sha256` / `verdict=pass`），每个 `sample_id` 唯一；`SC-001` / `SC-004` 仍为 `partial`，未补记录、未升为 `pass`。`evidence_path` 均为仓库相对路径，`evidence_sha256` 为文件字节的 SHA-256（`shasum -a 256` 同值）：

| sample_id | evidence_path（仓库相对） | evidence_sha256 |
|---|---|---|
| `SC-002_quickstart_s1` | `.specify/specs/080-humanize-run-output/notes/quickstart-run.md` | `c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b` |
| `SC-003_quickstart_s2` | `.specify/specs/080-humanize-run-output/notes/quickstart-run.md` | `c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b` |
| `SC-005_quickstart_s4` | `.specify/specs/080-humanize-run-output/notes/quickstart-run.md` | `c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b` |
| `SC-006_wiring_inventory` | `.specify/specs/080-humanize-run-output/test-evidence/wiring-inventory-baseline.txt` | `867c9be042f75eb54394355ecba0eac01967d1b2fa35754cccf5db4e36f7a514` |
| `SC-007_implement_part4` | `.specify/specs/080-humanize-run-output/test-evidence/implement-part4-status.txt` | `6a5fbcc8991711c822fad995f2779329b66209ed4286d3126e713852585ac91b` |
| `SC-008_implement_part5` | `.specify/specs/080-humanize-run-output/test-evidence/implement-part5-status.txt` | `b2f25d0b6bd715efb072f6cdbbd17df4fb7eb90c794b181e78cddff453bb1744` |
| `SC-009_quickstart_s3_s7` | `.specify/specs/080-humanize-run-output/notes/quickstart-run.md` | `c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b` |
| `SC-010_implement_part4` | `.specify/specs/080-humanize-run-output/test-evidence/implement-part4-status.txt` | `6a5fbcc8991711c822fad995f2779329b66209ed4286d3126e713852585ac91b` |

同一文件被多条记录复用，但每条记录 `sample_id` 唯一（自检读数 `unique_sample_ids=true`）。绑定自检的检查器源码与逐条读数落盘在 `test-evidence/review-repair-binding-check.txt`：`records=8`，8 条全部 `exists=true`、`bytes>0`、`hash_match=true`，`pass_records_cover=SC-002,SC-003,SC-005,SC-006,SC-007,SC-008,SC-009,SC-010`，`pass_sc_without_record=none`，`RESULT=PASS failures=0`，命令 rc=0。

### F2（P1）— SC 收口表与 canonical 块的判定已统一

`verification.md` § SC 收口表的 SC-001 / SC-004 状态词由「达成（…）」改为「**部分达成（partial）**（…）」，与 canonical 块的 `SC-001_status=partial` / `SC-004_status=partial` 一致；括号内的读数与证据路径原样保留。其余 8 行的状态词与内容未改。

### F4（P1）— quickstart「真实执行」的证据级别已在限制节声明

`verification.md` § 未跑与限制新增一条明确声明：quickstart 中被真实执行的只是内层命令（退出码与 stdout）；`/speckit.humanize` 的解析、占位与五节报告装配未作为端到端调用发生，五节报告正文由实现者在同一会话内按 SKILL 规范撰写；宿主原生派发通道（`mode: subagent` / `dispatches: 1`）未实测。该限制注明与 **SC-001 的 partial**（原生派发腿不可复现）及 **SC-004 的 partial**（用户拒绝确认腿 `not-reproducible`）对应。F4 提出的框架侧整改（执行级别枚举）仍归 REC-080-07，不在本次 review 修复内落地。

