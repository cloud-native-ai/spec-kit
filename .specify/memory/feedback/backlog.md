# Feedback Routing Backlog

> **Single carrier for findings a `/speckit.feedback` consume run routed but did not execute.**
>
> `consume-log.md` records what a batch *contained* and where each finding was *sent*. This file
> records what is still **owed**. A routing that exists only in a consume-log row is a dead letter:
> nothing carries it forward, and it has already been proven to recur — the `2026-09-14 (batch 2)`
> row sent "create-skills Step 6 lacks test-baseline discipline" to `improve-skills`, and a
> 2026-09-23 measurement found it had never been executed (that skill had no `baseline` string
> anywhere, and its suite line predated the entry). See
> `docs/reference/history/00-cross-cutting-lessons.md` § 二十三.
>
> **Closure rule (the whole point of this file)**: a row closes only on evidence that the **named
> owner file actually changed** — a commit, or a measurement of the owner showing the defect is
> gone. A row never closes on its own existence, on "it was routed", or on a plan to do it later.
>
> **`open-unverified` means**: the routing was recorded in a consume-log row, but nobody has
> re-checked whether the underlying defect still exists. Many were probably fixed by Features
> 050–053 or by later runs. Such a row MUST be verified against current framework source **before**
> anyone acts on it — acting on a stale point wastes a whole improvement cycle.

| Routed | Source | Finding | Channel | Owner file(s) | Status | Closed by |
|--------|--------|---------|---------|---------------|--------|-----------|
| 2026-09-14 | consume-log `2026-09-14 (batch 2)` | create-skills Step 6 lacks test-baseline discipline | improve-skills | `skills/create-skills/SKILL.md` | **open** (defect proven live 2026-09-23; recurred as introspection-20260923T120035Z#F-21, whose own fix landed 2026-09-23 in commit `67d2e2cf` — this row is the *earlier* routing of the same root cause, kept so the dead letter stays visible) | — |
| 2026-09-11 | consume-log `2026-09-11` | 7 improve-skills findings (create-agent template-authoring prescribes 4 forbidden metadata keys; create-agent teaches the retired per-file symlink model; no discipline for derived/decomposed doc emission; no named evidence path when a standalone target's lanes are empty; no pattern separating entry-knowledge from discovery-method; create-skills pre-scaffold conflict scan is name-keyed only; split/derive lacks reuse-first + byte-diff/idempotency gate) | improve-skills | `skills/create-agent/**`, `skills/create-skills/**`, `skills/improve-skills/**` | open-unverified | — |
| 2026-09-11 | consume-log `2026-09-11` | 1 improve-docs finding (token-efficiency has no subagent-delegation rung) | improve-docs | `shared/guidelines/token-efficiency.md` | open-unverified | — |
| 2026-09-11 | consume-log `2026-09-11` | 8 requirements-candidates (F-E01 package/cleanup/mark-submitted zeroing semantics; F-E03 no receipt path so refutations never reach reporters; F-E05 Mode 5 projection omits `## Optimization Points` and truncates summary at 200 chars; F-D01 analyze deterministic validator; F-C06 mirror-parity gate presumes a zero-drift baseline; F-E11 hard-coded constitution principle numbers ship in ≥5 framework sources with zero drift detection; F-E14 create-team lightweight summary tier; F-D05 analyze content-signature reuse — WONTFIX candidate) | speckit-requirements | 见各行 | open-unverified（注:F-E01/F-E05 与 2026-09-23 的两条 feedback 命令优化点同源;F-D01 与 Feature 053 的 US1 同族） | — |
| 2026-09-14 | consume-log `2026-09-14 (batch 2)` | 22 queued direct-fix（明写「下一轮执行」,owner 已锚定:requirements/clarify/plan/tasks/analyze 命令模板 ×14、implement/review/sanitize/skills 模板 ×8） | direct-fix | `templates/commands/**` | open-unverified（其中相当一部分很可能已由 Feature 050–052 与 2026-09-23 的 16 项修复覆盖;逐条核验前 MUST NOT 当作待办执行） | — |
| 2026-09-14 | consume-log `2026-09-14 (batch 2)` | 11 improve-skills（git-workflow 单层/降级模式设计簇 ×3、create-skills ×4、improve-skills ×4） | improve-skills | `skills/git-workflow/**`, `skills/create-skills/**`, `skills/improve-skills/**` | open-unverified | — |
| 2026-09-14 | consume-log `2026-09-14 (batch 2)` | 1 improve-docs（`/speckit.skills` 命令接线义务清单单一事实源）+ 6 requirements-candidate（feedback 引擎:组合 package 预检 action、cleanup 对 git 跟踪条目的感知、确定性 consume-scan 投影;sanitize:已完结未归档 spec 的 dead-ref 政策、引擎拒删非空目录 vs Stage-6 回退、`.migration-backups` 复发源） | improve-docs / speckit-requirements | `docs/reference/skills/skills.md`, `scripts/python/feedback-utils.py`, `scripts/python/sanitize-utils.py` | open-unverified | — |
| 2026-08-31 | consume-log `2026-08-31` | 6 local-sink 维持自省原分流（improve-skills ×4:契约冲突出口 / HC7 断言对象 / 接线清单变更单位 / git-workflow 单主干形状与远端解析;improve-team ×1;直修 ×1） | improve-skills / improve-team | `skills/improve-skills/**`, `skills/improve-team/**`, `skills/git-workflow/**` | open-unverified（注:前三项对应已 confirmed 的 `introspection-20260831T072111Z` F-01/F-02/F-03;git-workflow 的两项已由 2026-09-14 首个 batch 的 direct fix 部分覆盖） | — |
| 2026-09-23 | introspection-20260923T120035Z#F-04③ | 机器覆盖核算:contracts 每条条款与每条 FR 恰被一行任务认领,由脚本印出未覆盖集（未实现,因契约条款语法无 owner 且认领声明面属 F-05） | speckit-requirements | `scripts/python/validate-tasks.py`, `templates/tasks-template.md` | **carried-by-spec-053**（US3 / FR-022…FR-028） | `.specify/specs/053-machine-decidable-artifacts/requirements.md` |
| 2026-09-23 | introspection-20260923T120035Z#F-05 | 条款→任务绿点归属无可声明面,跨 Phase 绿点静默通过 | speckit-requirements | `templates/tasks-template.md`, `scripts/python/validate-tasks.py` | **carried-by-spec-053**（US2 / FR-015…FR-021） | 同上 |
| 2026-09-23 | introspection-20260923T120035Z#F-03 | requirements.md 无确定性校验器 | speckit-requirements | `scripts/python/validate-requirements.py`(待建), `shared/guidelines/requirements-guidelines.md` | **carried-by-spec-053**（US1 / FR-006…FR-014） | 同上 |
| 2026-09-23 | introspection-20260923T120035Z#F-14 次生根 | goal 判据主体靠成员枚举,不可程序指代（「目录指代形」为新概念） | speckit-requirements | `shared/definitions/goal-definitions.md`, `scripts/python/goal-utils.py` | **carried-by-spec-053**（US5 / FR-035…FR-038） | 同上 |
| 2026-09-23 | introspection-20260923T120035Z#F-16 次生根 | `goal-utils.py` 缺 `run-checks`:五项 run 前置检查依赖无 CLI 入口的内部函数 | speckit-requirements | `scripts/python/goal-utils.py`, `templates/commands/team.md` | **carried-by-spec-053**（US4 / FR-029…FR-034） | 同上 |
| 2026-09-23 | 修复波子代理上送 | `verify-territory-disjoint.py` 跳过同 slug 自比较对的同时,也掩盖了「同一 proposals.json 内两团队撞 slug」这一真实输入错误;区分二者需要新的输入校验语义,报告未记录该意图 | direct-fix | `skills/create-team/scripts/verify-territory-disjoint.py` | open（裁定已上送,等用户定语义） | — |
| 2026-09-23 | 修复波子代理上送 | `docs/reference/commands/goal.md` 未记录本轮新增的 `objective` action、`create --title` / `--boundary`、`criteria --clear` 与 read/write 分组标注 | improve-docs | `docs/reference/commands/goal.md` | open | — |
| 2026-09-23 | 修复波子代理上送 | `.specify/specs/051-user-facing-comprehension/checklists/requirements.md:75` 记 FR 36 / SC 16,而活规格实测 FR 38 / SC 18 —— F-07③ 所描述缺陷的一次真实发生（属已交付特性的制品,故未回溯修改） | acknowledge-only | `.specify/specs/051-user-facing-comprehension/checklists/requirements.md` | open（客户实例侧,是否回溯订正待定） | — |
