# Specification-Driven Development (SDD) Process Review Report: sanitize-command(框架资料卫生)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 045 |
| Requirement Key | 045-sanitize-command |
| Requirement Name | 框架资料卫生治理——残留冗余清理与关键资料正确性检查(Sanitize Command) |
| Related Feature | 047 Framework Material Hygiene(框架资料卫生) |
| Repository | spec-kit |
| Repository URL | git@github.com:github/spec-kit.git |
| Branch | 045-sanitize-command |
| Commit SHA | e6f4da981e1bfdbe3787b1ce29f23ab4f7307ccc (short: e6f4da98) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-08-20 |
| Reviewer (Agent) | Qoder (implementing agent, self-review per /speckit.review) |
| Environment | Linux 5.10.134 x86_64, bash, Python 3.8+ (stdlib-only engine), Node 24.3.0, git |
| spec-kit Source Snapshot | git@github.com:github/spec-kit.git @ e6f4da981e1bfdbe3787b1ce29f23ab4f7307ccc |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 144 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/requirements.md | 3 US / 12 FR / 5 SC;report-persistence + pending 状态模型;两级门控清理 |
| plan.md | 107 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/plan.md | 技术上下文/宪法 12 Pass + 1 Partial(IX)/镜像义务 3 行 |
| tasks.md | 223 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/tasks.md | 32 任务 6 阶段;DoD 6 + Completion Gate 6 |
| data-model.md | 119 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/data-model.md | 5 实体:Finding/Store/Cleanup Plan/Material Root/Execution Report |
| contracts/ (4 files) | 610 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/contracts/ | engine CLI / findings schema / 命令模板结构 / 检测规则 |
| quickstart.md | 70 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/quickstart.md | 3 走查(检出/确认清理/正确性) |
| feature-ref.md | 28 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/feature-ref.md | US→FR→工件映射 + 实现批次义务 |
| verification.md | 83 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/verification.md | SC-001..005 全 pass;事故记录;机制修订台账 |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` — branch numbering required manual disambiguation (namespaced remote branches matched `[0-9]{3}-`) | feedback entry `20260820T032230Z-speckit-requirements.md`: "远端分支 origin/community/4059-*、origin/fix/4198-* 的尾部数字会被 `[0-9]{3}-` 模式误匹配为规格编号" | No(人工纠正) |
| 2 | `/speckit.clarify` — 3 decisions;the adopted report-form answer was only expressible via "Other" | feedback `20260820T041251Z-speckit-clarify.md`: "三个候选...都未包含'持久化 + pending 状态生命周期'混合形态...用户只能经 Other 表达" | No |
| 3 | `/speckit.plan` — plan integrity gate false-positived on the template's own self-referential Note line | feedback `20260820T060028Z-speckit-plan.md`: "完整性门对模板自指说明行(含字面 [PLACEHOLDER] 的 Note)会误报残留占位符" | No(按 044 惯例手工删除该行) |
| 4 | `/speckit.tasks` — story-label rule discovered only at validation | feedback `20260820T060750Z-speckit-tasks.md`: "修正一处 [US-none] 标签后复验" | No |
| 5 | implement Phase 1-2 — scripts-parity contract test caught the unsynced engine mirror (1 new failure, fixed by immediate `sync-mirrors --write`) | commit d5c8e8dd;failure `test_repo_has_no_orphan_or_drifted_scripts` in phase-boundary regression | No(门生效,但见 F2) |
| 6 | implement Phase 3 — **unconfirmed deletion of `.specify/memory/todo/20260812-evidence-session-backlog.md` entered commit a0197299 via `git add -A`**;undetected until Phase 6 | commit a0197299 `--diff-filter=D`;verification.md incident record | **Yes — 破坏性动作未经门控入册(F1)** |
| 7 | implement Phase 4 — checker landings;symlink "missing" semantics needed expectation-conditioning to avoid client-workspace false positives;3 transient test failures traced to real-repo mirror state, not test logic | commit 9ed19628: "修订:缺失仅在对应工具面存在时报——单一 CLI 客户工作区零误报" | No(契约 C-10 同步修订) |
| 8 | implement Phase 5 — the designed destructive gate was INVISIBLE to the governance scanner until the template wording was changed to a countable blocking pattern;2 client-neutrality violations fixed by iteration | scanner totals 22 → 23 across two runs;commits 7d7927a3 | No(但暴露 F8 反向激励) |
| 9 | implement Phase 6 — dogfood run produced 926 findings (917 dead-refs, mostly by-design-exempt frozen history);5 mechanism revisions landed as contract/engine edits NOT tracked as task rows;the Phase-3 deletion discovered and restored | commit e6f4da98: "dogfood 驱动 5 项机制修订:冻结历史豁免..."、"事故:恢复 Phase 3 意外提交的 0801 todo 删除" | **Yes — 中途设计修订未走任务台账(F3)** |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 3 |
| Automation / Scripts | 3 |
| Workflow | 2 |
| Documentation | 0 |

## 3. Findings (Problems & Improvement Targets)

### F1 — Unconfirmed file deletion rides a phase commit; the commit gate audits tests only, and the commit template itself conceals the deletion surface

- **Severity**: P0 (validated: confirmed by independent subagent)
- **Category**: Automation / Scripts (command-template rule)
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md (commit gate, ~line 68; Optional Git Commit, line 101);incident evidence at commit a0197299 and /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/verification.md
- **Evidence** (verbatim quote):

  ```
  commit only after that phase's name-level regression diff (`comm -13 baseline current`) is empty
  ```

  ```
  - Display `git add -A && git commit -m "{msg}"` — only execute on explicit user approval
  ```

  ```
  Phase 3 提交(a0197299)意外包含 .specify/memory/todo/20260812-evidence-session-backlog.md 的删除——未经过用户确认,违背确认门控纪律
  ```

- **Why it's a problem**: The phase-boundary commit gate verifies the test regression diff but never audits the staged DELETION surface, while the prescribed commit command is `git add -A` — so any unattributed working-tree deletion is silently committed as a destructive action with no confirmation and no commit-message declaration. In this run the motivating material was deleted this way and only detected three phases later, by luck of the dogfood task targeting that exact file.
- **Proposed fix**: In templates/commands/implement.md, extend the commit-gate rule with a mechanical deletion audit: before each phase commit, run `git diff --cached --diff-filter=D --name-only` (plus the same for the working tree) and require every listed deletion to reconcile against a task row / confirmed cleanup plan; unreconciled deletions abort the commit for human review.

### F2 — Engine subprocess tests couple to the real repository's mirror state; mid-phase engine edits cause transient failures that look like logic defects

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/sanitize-utils.py (`run_sync_mirrors_check` docstring);failure sequence across phases 2-5 of this run
- **Evidence** (verbatim quote):

  ```
  sync-mirrors resolves its repo from its own script location, so the lane only runs when the workspace IS
  that repo (framework dogfood or an installed client copy); against any other workspace it would inspect
  the wrong tree — skip instead.
  ```

- **Why it's a problem**: Before this locality rule landed, three separate test failures (`test_record_accepts_valid_semantic_finding`, two US1 integration tests) were caused not by test logic but by the engine's strict mirror being momentarily stale after an in-repo engine edit — each cost a diagnostic cycle and mimics a regression. The precondition (mirrors synced before engine test batteries) is nowhere stated; agents rediscover it per phase.
- **Proposed fix**: Add to templates/commands/implement.md's test-run guidance: when the feature touches a mirrored engine, run `sync-mirrors.py --write` before re-running engine test batteries (or promote this to a conftest fixture that skips mirror-lane tests when drift is detected).

### F3 — Self-discovered mid-run design refinements bypass the task ledger (Mid-Run protocol covers only USER directives)

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md ("Mid-Run User Directives (scope changes DURING implement)" section);commit e6f4da98
- **Evidence** (verbatim quote):

  ```
  When the user changes scope or adds a design constraint while this command is running, do NOT improvise:
  apply the Scope Revision Protocol
  ```

  ```
  dogfood 驱动 5 项机制修订:冻结历史豁免(archive/history 不做引用检查)、feedback 簿记文件豁免(时间戳命名形态)、
  孤儿检测收窄 skills 对(agents 含合法运行时结构)、证据包重设计(无日期过滤+计数截断+文件名片段 glob,两条真实
  案例回归测试)、守卫测试豁免 sanitize 台账(RUNTIME_CACHE_PREFIXES)
  ```

- **Why it's a problem**: Five contract/engine scope changes (checker exemption classes, evidence-pack semantics, guardrail exemptions) were performed during Phase 6 without corresponding appended `T` rows — the per-task audit trail that `/speckit.review` and bisect rely on silently stops covering part of the delivered work. The Mid-Run protocol governs user-driven scope changes only, leaving agent-discovered refinements in a governance vacuum.
- **Proposed fix**: Extend the Mid-Run section to cover agent-discovered design refinements: any contract/data-model change made mid-run (including dogfood-driven corrections) MUST land as appended `T0NN` rows in the same commit, with the affected contract rule IDs named in the row description.

### F4 — plan.md template's self-referential Note line false-positives the plan integrity gate

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md (step 5, plan integrity gate);feedback entry 20260820T060028Z-speckit-plan.md
- **Evidence** (verbatim quote):

  ```
  完整性门对模板自指说明行(含字面 [PLACEHOLDER] 的 Note)会误报残留占位符;本次按 044 惯例删除该行通过,
  但命令指引未写明该行的处置(保留会卡门、删除靠 agent 自行回忆惯例)
  ```

- **Why it's a problem**: Every `/speckit.plan` run hits the same gate false positive and resolves it by recalling an undocumented house convention (delete the Note line), or fails the integrity check.
- **Proposed fix**: State the disposition explicitly in templates/commands/plan.md step 5 (plan integrity gate): "the template's self-referential **Note** line is removed when filling; a residual `[PLACEHOLDER]` check must exclude nothing else".

### F5 — tasks.md story-label rule is failure-discovered, not guidance-encoded

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md ("Format" rules);feedback `20260820T060750Z-speckit-tasks.md`
- **Evidence** (verbatim quote):

  ```
  修正一处 [US-none] 标签后复验
  ```

- **Why it's a problem**: The rule "Setup/Foundational/Polish phases carry NO story label" exists only as a format-table footnote; agents naturally invent placeholder labels (`[US-none]`) and only learn the rule from a failed self-check.
- **Proposed fix**: Add a machine-checkable item to tasks.md's validation step: `grep -c '\[US' ` within non-story phase ranges must be 0 (the inverse of the existing story-label checks).

### F6 — Requirements branch-numbering step is misled by namespaced remote branches

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/requirements.md (Outline step 2);feedback `20260820T032230Z-speckit-requirements.md`
- **Evidence** (verbatim quote):

  ```
  远端分支 origin/community/4059-*、origin/fix/4198-* 的尾部数字会被 `[0-9]{3}-` 模式误匹配为规格编号,
  导致"下一编号"被高估(本次人工甄别为 045 而非 200)
  ```

- **Why it's a problem**: Upstream/community namespaced branches inflate the derived next-number (200 vs 045 here); without manual disambiguation the spec would have been numbered 200, colliding with the registry's convention.
- **Proposed fix**: In requirements.md step 2, scope the numbering scan to `.specify/specs/` (incl. `.archive`) and top-level `<NNN>-<slug>` branch names only — explicitly excluding slash-namespaced branches.

### F7 — clarify option tables exclude patterns the repo itself already embodies

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/clarify.md (Question Generation);feedback `20260820T041251Z-speckit-clarify.md`
- **Evidence** (verbatim quote):

  ```
  报告形态问题的三个候选(零写入/纯会话内/持久化工件)都未包含"持久化 + pending 状态生命周期"混合形态,
  而本仓 feedback/evidence 存储均为此形态,属可预见的候选空间;用户只能经 Other 表达
  ```

- **Why it's a problem**: When the answer space is "already bounded" the command may propose options — but composing options without scanning existing store patterns in the repo systematically omits the most likely choice, forcing the user through the free-text escape hatch.
- **Proposed fix**: Add to clarify.md's question-generation constraints: before composing a storage/UX options table, enumerate the repo's existing store shapes (feedback/evidence/history) as candidate options.

### F8 — A new confirmation gate is invisible to governance unless worded in scanner-blocked language

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/scan-confirmation-gates.py (BLOCKING_PATTERNS);/storage/project/cloud-native-ai/spec-kit/templates/commands/sanitize.md line 66
- **Evidence** (verbatim quote):

  ```
  r"用户确认后才",
  ```

  ```
  删除与移动/归档属破坏性桶,等待用户确认后才执行(引擎对 `confirmed != true` 的 apply 一律退出码 2 拒绝,零执行)。
  ```

- **Why it's a problem**: The first template phrasing ("未经确认绝不执行") expressed the same gate but matched no BLOCKING pattern, so the governance inventory total stayed 22 — the gate existed but was uncounted. It only entered the inventory after rewording to a countable pattern. Governance observability therefore depends on the gate author happening to phrase the gate in blocked-language form — an inverted incentive.
- **Proposed fix**: In shared/guidelines/confirmation-gates.md, ship a canonical countable phrasing snippet for new destructive gates (e.g. "……等待用户确认后才执行" plus the single-line gate probe pointer), or teach scan-confirmation-gates.py to anchor gate counting on gate-probe pointer lines as a second recognition channel.

### F9 — Detection-grammar precision (noise budget) is untestable by fixtures; only a real-repo dogfood run exposes scope-policy errors

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/045-sanitize-command/verification.md (mechanism notes);dogfood run sequence 926 → 692 findings
- **Evidence** (verbatim quote):

  ```
  首轮 dogfood 926 项死引用中绝大多数来自 .specify/archive/spec/ 与 .specify/history/——引用描述归档时点的历史状态,
  "失效"按设计。修订后死引用 917→691
  ```

- **Why it's a problem**: Fixture tests verified the grammar's recall (each rule had a positive case) but nothing pinned its precision on real corpora — the first true run produced ~917 dead-reference findings of which the large majority were by-design-exempt classes (frozen history, bookkeeping files, runtime structure). All five exemption refinements had to be discovered live.
- **Proposed fix**: In /speckit.plan guidance for detection-type features, require the detection contract to pin an expected-noise section (exemption classes with rationale) BEFORE implementation, so precision policy is reviewed at design time rather than retrofitted mid-run.

## 4. What Worked — Preserve (Brief)

- Phase-grouped commits carrying task IDs in messages — every increment independently bisectable.
- Failure-attribution-first discipline (subject vs assertion side stated before each fix) prevented assertion-driven corruption of correct engine behavior.
- Name-level baseline diff (`comm -13 baseline current`) made "zero new failures" a mechanical claim, not a count archaeology.
- The mandatory dogfood task (T031) surfaced 5 mechanism defects invisible to fixtures and closed the motivating real case with commit-level evidence.
- Independent P0 validation caught an additional gap the diagnostic pass had missed (the `git add -A` display in the commit template itself).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Audited phase-commit recipe** — Target: git@github.com:github/spec-kit.git, templates/commands/implement.md ("Commit gate" + "Optional: Git Commit"). Change: replace the displayed `git add -A && git commit` with a deletion-surface-audited sequence (`git diff --cached --diff-filter=D --name-only` reconciliation against task rows / confirmed plans, abort on unreconciled deletions). Source: F1. Expected impact: closes the silent-destruction path for every future implement run.
- **Plan Note-line disposition** — Target: templates/commands/plan.md (step 5, integrity gate). Change: document that the template's self-referential Note line is removed on fill. Source: F4. Expected impact: removes a guaranteed per-run gate false positive.

### 5.2 Command Prompt Improvements

- **Numbering scan scope** — Target: templates/commands/requirements.md (Outline step 2). Change: exclude slash-namespaced remote branches from the next-number derivation. Source: F6. Expected impact: prevents registry-number inflation (045 vs 200).
- **Story-label machine check** — Target: templates/commands/tasks.md (validation step). Change: add the inverse grep item (zero `[US` markers in non-story phases). Source: F5. Expected impact: format rule becomes checkable, not failure-discovered.
- **Options grounded in repo store shapes** — Target: templates/commands/clarify.md (question-generation constraints). Change: enumerate existing store patterns (feedback/evidence/history) before composing storage/UX option tables. Source: F7. Expected impact: fewer "Other"-only escapes for foreseeable answers.

### 5.3 Automation / Script Improvements

- **Mirror-sync precondition for engine test batteries** — Target: templates/commands/implement.md (test-run guidance) or tests/conftest.py. Change: sync mirrors (or skip mirror-lane tests) before re-running engine subprocess tests after engine edits. Source: F2. Expected impact: eliminates a class of transient false-regression failures.
- **Countable gate phrasing canon** — Target: shared/guidelines/confirmation-gates.md and/or scripts/python/scan-confirmation-gates.py. Change: provide a canonical countable phrasing snippet for new destructive gates, or count gates anchored on gate-probe pointer lines as a second channel. Source: F8. Expected impact: governance inventory completeness stops depending on blocked-language phrasing luck.

### 5.4 Workflow Improvements

- **Mid-run refinement ledger rule** — Change: extend implement.md's Mid-Run section so agent-discovered design refinements also land as appended task rows naming affected contract rule IDs. Source: F3. Expected impact: the task audit trail covers all delivered work.
- **Detection noise budget at design time** — Change: /speckit.plan guidance requires detection contracts to pin expected-noise exemption classes before implementation. Source: F9. Expected impact: precision policy reviewed at design time instead of retrofitted mid-run.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Audited phase-commit recipe (deletion-surface reconciliation) | templates/commands/implement.md | F1 |
| P1 | Mid-run refinement ledger rule | templates/commands/implement.md (Mid-Run section) | F3 |
| P1 | Mirror-sync precondition for engine tests | templates/commands/implement.md / tests/conftest.py | F2 |
| P2 | Countable gate phrasing canon | shared/guidelines/confirmation-gates.md, scan-confirmation-gates.py | F8 |
| P2 | Numbering scan scope + story-label check + options grounding | templates/commands/{requirements,tasks,clarify}.md | F6, F5, F7 |
| P2 | Plan Note-line disposition; detection noise budget | templates/commands/plan.md; /speckit.plan guidance | F4, F9 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as a repo-identifiable reference (repository URL + SHA).
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
