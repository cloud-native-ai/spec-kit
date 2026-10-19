# Specification-Driven Development (SDD) Process Review Report: Humanize Command（人性化改写命令）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 062 |
| Requirement Key | 062-humanize-command |
| Requirement Name | Humanize Command（人性化改写命令） |
| Related Feature | 062 Humanize Command（人性化改写命令） — `.specify/memory/features/062.md`, status **Implemented** |
| Repository | spec-kit (distributed as `specify-cli`) |
| Repository URL | `origin` = `git@github.com:github/spec-kit.git` — this is the **UPSTREAM**, not the fork. The remotes that would hold these commits are `github` = `git@github.com:cloud-native-ai/spec-kit.git`, `gitee` = `git@gitee.com:cloud-native-ai/spec-kit.git`, `gitlab` = `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`. All three are SSH, none is HTTPS-web-accessible. |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` returns empty — HEAD is not on any remote. Cite absolute paths + `git show <sha>:<path>` instead of URLs. |
| Branch | 062-humanize-command |
| Commit SHA | e6696a0f9b5f5080722a8954ce5e78e68d715049 (short: e6696a0f) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-19 |
| Reviewer (Agent) | SDD Executor — fresh-context stage dispatch running `/speckit.review`, delegated to skill `review-sdd-process` (`/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/review-sdd-process/SKILL.md`) |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash; Python 3.11.11; pytest 8.4.2; `CWS_LIB_BASH_HOME=/storage/project/cloud-native-tools/cws-lib-bash` resolvable (**restored** — the tasks.md degradation record for it is expired, see § Environment Prerequisites of `/storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/tasks.md` line 41) |
| spec-kit Source Snapshot | This repository **is** the spec-kit source (self-hosting; see `/storage/project/cloud-native-ai/spec-kit/.specify/instructions.md` § Two Hats). Packaged version `0.0.22` per `/storage/project/cloud-native-ai/spec-kit/pyproject.toml` line 3. Every `templates/`, `shared/`, `scripts/`, `skills/` path cited below is a framework-source path, not a `.specify/` runtime copy. |

**Path convention used in this report.** Because §0 records the commit as **UNRESOLVABLE**, no remote-web permalink of the form `REPO_URL/blob/COMMIT_SHA/...` written here would resolve. Every path is therefore given as an absolute path on the checkout that produced this report **and**, in backticks immediately after it, the repo-relative form; a maintainer on any other checkout resolves the relative form against their own repo root. Absolute paths are checkout-local by nature — the relative form is the portable one, and `git show e6696a0f9b5f5080722a8954ce5e78e68d715049:<relative-path>` recovers the exact bytes on any clone that has the branch.

This convention is a deliberate correction of the prior report `/storage/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/review.md` (`061-subagent-cli-config/review.md`), which satisfied the absolute-path rule with **134** occurrences of a macOS root `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/...` and **zero** occurrences of the current root `/storage/project/...`. Its 22 recommendations therefore name targets that resolve nowhere on this machine — one of the two mechanisms behind F3.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 264 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/requirements.md | FR-001..FR-029, SC-001..SC-011, Shared Strings STR-001..004, two clarification sessions (`requirements.md`) |
| plan.md | 159 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/plan.md | Constitution Check (16 rows, IV = ⚠ Partial), Phase 0 D-1..D-7, same-author scoring record + repair-round addendum (`plan.md`) |
| tasks.md | 314 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/tasks.md | 33 tasks all `[X]`, DoD-1..8, GATE-1..8, § Environment Prerequisites, D-T1..D-T6, measured premises (`tasks.md`) |
| data-model.md | 158 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/data-model.md | Phase 1 design entities for the rewrite contract (`data-model.md`) |
| quickstart.md | 181 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/quickstart.md | S1–S8 verification recipe the implement stage actually ran (`quickstart.md`) |
| contracts/command-surface.md | 38 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/contracts/command-surface.md | C-1..C-10 structural surface clauses (`contracts/command-surface.md`) |
| contracts/rewrite-behavior.md | 49 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/contracts/rewrite-behavior.md | C-11..C-23 + C-35 behavioral clauses and traceability table (`contracts/rewrite-behavior.md`) |
| contracts/tone-input-file.md | 40 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/contracts/tone-input-file.md | C-24..C-34 tone / input / file-safety clauses (`contracts/tone-input-file.md`) |
| checklists/requirements.md | 39 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/checklists/requirements.md | 16/16 items checked, validator output quoted (`checklists/requirements.md`) |
| checklists/requirements-quality.md | 74 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/checklists/requirements-quality.md | CHK001..CHK040, **0/40 checked** — never answered by any stage (`checklists/requirements-quality.md`) |
| verification.md | 434 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/verification.md | SC-001..SC-011 all `pass`, E8 corpus tables, two/three-reviewer verdicts, § Deviation (4 items) (`verification.md`) |
| waivers.md | 15 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/waivers.md | One waiver: `requirements-quality.md` 0/40, gate probe `gate-implement-checklist-waiver` (`waivers.md`) |
| feature-ref.md | 91 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/feature-ref.md | FR→clause map (29 rows), SC→verification map (11 rows), 17-deliverable list, 5 baseline records (`feature-ref.md`) |
| notes/quickstart-run.md | 287 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/quickstart-run.md | S1–S8 real command outputs incl. the unplanned-change rollback experiment (`notes/quickstart-run.md`) |
| notes/pre-change-measurements.md | 45 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/pre-change-measurements.md | Pre-change capture of all four faces + ad-hoc §5 mirror-drift reconciliation (`notes/pre-change-measurements.md`) |
| notes/red-first-evidence.md | 39 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/red-first-evidence.md | RED run 8 failed / 2 passed with per-test first failing assertion (`notes/red-first-evidence.md`) |
| notes/source-requirement.md | 112 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/source-requirement.md | Original user ask as received (`notes/source-requirement.md`) |
| notes/baseline-*.txt (6 files) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/ | Frozen baselines: regen-check, mirror-check, compile-check, compile-unit-no-scope, failed-tests (71 names), test-run |
| notes/e8-run/ (13 entries) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/e8-run/ | Archived rewrite outputs s01–s11, `files/`, `files-branches.md`, `tone/` |
| features/062.md | — | /storage/project/cloud-native-ai/spec-kit/.specify/memory/features/062.md | Registry detail: status Implemented + four dated Latest Review entries |

**Same-author gate status** (owner: `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md`, `shared/workflow/objective-analysis-gate.md`). The gate **does not fire** on this run: its own firing rule reads "*Does not fire: the artifacts predate this session, or have a different author (another agent, a human, an upstream release)*", and every artifact in the inventory above was committed between 15:11 and 18:34 by five prior stage dispatches, none of them this reviewer. Detection was therefore performed directly by the reviewer. Gate rule 5 ("*Keep detection and validation disjoint — no agent validates a finding it produced*") was still honoured: all P0 candidates were handed to four independent read-only validation subagents that saw only the finding, never the reasoning or its siblings. Gate rule 6 requires the downgrade rate to be reported: **4 of 4 P0 candidates were downgraded** (see §7).

## 1. Process Execution Timeline

Reconstructed from `git log --grep=062-humanize-command` (17 commits, all 2026-10-19 15:11→18:34) plus in-artifact timestamps. No degradation to working-tree inspection was needed: the commit history is story/task-grouped.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | 15:11 `/speckit.requirements` — spec + requirements checklist land in one commit | `898aa02e` — `requirements.md` (243 L at landing) + `checklists/requirements.md` (38 L) | None |
| 2 | 15:18 `/speckit.clarify` — Feature 062 binding, registry row + detail | `318908fc` "clarify — bind Feature 062 and land registry row and detail" | None |
| 3 | 15:49 `/speckit.plan` — plan + Phase 1 design | `548c9b18`; `plan.md` Constitution Check row IV = ⚠ Partial, justified through the Principle VII template-only gate | None — partial is declared and justified |
| 4 | 16:05 `/speckit.tasks` — 33 dependency-ordered tasks, 4 baselines frozen | `e14d9a0a`; `tasks.md` DoD-1..8 / GATE-1..8; `notes/baseline-failed-tests.txt` = 71 sorted names | None |
| 5 | 16:13 `/speckit.checklist` — 40-item quality checklist authored, **all rows left `- [ ]`** | `f2fe4027` (73 insertions, one file). Line 17 as authored: `- [ ] CHK005 - 对外部文档中「看起来像指令的内容」（提示注入）是否规定按数据处理、不得改变命令行为？ [覆盖/安全, Gap]`. Line 26: `- [ ] CHK011 - 混合语言的「主语言」是否有可操作的判定规则（字符占比、句子占比、逐段判定）？ [术语/清晰性, Req §FR-013, §SC-003]` | None at authoring time — but the two `Gap`-tagged rows were written down here and re-discovered 19 minutes later (row 6) → **F2** |
| 6 | ~16:13–16:32 `/speckit.analyze` round 1 — gate verdict **HIGH=2**: H-01 (prompt-injection defense absent) and H-02 (main-language determination not operable) | `requirements.md` line 258: "H-01 落为 FR-029 与 SC-011（提示注入防线），H-02 落为 FR-013/SC-003 的主语言判定规则". H-01 is CHK005's subject; H-02 is CHK011's subject | **Yes** — analyze never opened the checklist. `grep -c checklist` = **0** in both `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` and `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md`; the skill's § load table enumerates requirements/plan/tasks/registry only → **F2** |
| 7 | 16:32 repair round 1a — requirements | `173c897d` "repair requirements per analyze gate round 1" | Prescribed (gate loop) |
| 8 | 16:49 repair round 1b — plan + Phase 1 design; new clause C-35 | `d0523cfe`; `plan.md` line 156 "Repair round 1 addendum（2026-10-19）" records a mixed-set same-author delegation: 16/16 constitution rows confirm, 0 overturns, 4 findings (2 corrected in place, 2 disclosed upward, 0 adjudications) | Prescribed |
| 9 | 16:58 repair round 1c — tasks + registry; analyze round 2 gate **HIGH=0** | `c831e7ec` "propagate analyze round 1 repairs into tasks and registry" | Prescribed — but the whole three-commit loop re-derived what row 5 had already recorded → **F2** |
| 10 | Checklist disposition after the repair: annotations updated, **no row flipped** | `checklists/requirements-quality.md` line 74: "Repair round 1 … 闭合了 CHK005 与 CHK008 原标注的 Gap——两处仅更新追溯标注，条款问题文本未删改". Current line 17 now reads `… [覆盖/安全, Req §FR-029, §SC-011]` and is still `- [ ]`. File stands at **0/40** | **Yes** — no stage owns answering checklist items → **F2** |
| 11 | 17:19 `/speckit.implement` attempt 1 opens with baseline re-capture | `notes/pre-change-measurements.md` header: "# Captured: 2026-10-19T17:19:43+08:00". § 2 capture = **113** mirror DIFF names; the frozen record `notes/baseline-mirror-check.txt` says **209** | **Yes** — the re-freeze duty is declared only on the producer side (`/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` § Re-freeze timing, line 375: "re-capture at the start of `/speckit.implement`"), with no matching consumer step in `skills/internal/implement-feature/SKILL.md` or `templates/commands/implement.md`. An ad-hoc "§5 Mirror-face premise note (honest drift accounting)" name-level reconciliation had to be invented on the spot → **F7** |
| 12 | 17:36 Phase 1–2 groundwork: fixtures, `rubric.md`, `diff_protected.py`, RED contract test | `7ade5ec7`; `notes/red-first-evidence.md` = 8 failed / 2 passed with per-test first failing assertion, and an honest explanation of why 2 tests pre-passed | Minor — `notes/red-first-evidence.md` line 39 binds the name-level baseline comparison to **GATE-7**, but `tasks.md` GATE-7 is "Structural validity"; the name-level gate is **GATE-1** → **F8** |
| 13 | 17:39 Phase 3 — thin command template + external humanize skill | `d4f07273` | None |
| 14 | 17:43 Phase 3 closure — E8 inline execution (T008) + two independent reviewers (T009) ALL-PASS | `71576e21`; `verification.md` § E8-US1 (s01..s08) and § T009 | None |
| 15 | 17:48 Phase 4 — file-behavior execution (T013) + s09/s10/s11 | `74d4af3d`; `verification.md` § E8-Files B01–B17 | None |
| 16 | Mid-run self-correction: a claimed sample had not actually been executed | `verification.md` line 180: "**s11 补正记录**：本节初稿曾声称 s11 已 PASS 而实际未执行——发现后立即补跑" | **Yes** — caught by executor self-disclosure only. `tasks.md` GATE-8 checks evidence existence, not evidence-to-claim binding: "GATE-8: 17 deliverables present — check: verify each path from `feature-ref.md` § 交付面清单 with `test -e`" → **F6** |
| 17 | 17:56 tone/audience matrix — real reviewer FAIL, then repair, then reversal | `5721752e`; `verification.md` § 语气与受众矩阵: T-audience judged **FAIL by both reviewers** → repair round → third reviewer → 翻案为 pass | None — this is the evaluation protocol working |
| 18 | 17:57 E8 evidence archived as `.md` records | `53efb354` "land e8-run evidence logs as md records (gitignore *.log)" | Minor — evidence file extension adapted to a repo-wide `*.log` ignore rule |
| 19 | **attempt 1 aborts at T031 (30/33)** with an upstream API error | `UnsupportedFinishReasonError`; Stop-hook fired, no completion sentinel emitted, the status record was judged FAILED, attempt 2 resumed from the breakpoint | Yes — external, not process-caused. The Stop-hook + status/sentinel **dual-signal** fallback is what made the abort recoverable rather than silent |
| 20 | Implement Step 2 checklist exemption gate fires; waiver written | `waivers.md` line 10: "The items remain formally unchecked because no stage owns flipping them post-analysis; requiring that here would block implement on a bookkeeping form, not on an open quality gap." Gate probe `gate-implement-checklist-waiver` | **Yes** — with the checklist at 0/40 this gate fires on *every* feature and *always* needs a waiver → **F2** |
| 21 | Unplanned runtime change proven necessary by a rollback experiment | `notes/quickstart-run.md` § 非计划改动复核: single-file `git checkout HEAD -- .specify/scripts/python/probe-utils.py` → `--action compile-embeds --check` **exit 2** `probe registry invalid`; restored → **exit 0** "74 units, zero drift". Kept and recorded in `verification.md` § Deviation | Yes — unplanned, but handled exactly as the fast-fail discipline prescribes (rollback-proven, disclosed, deviation recorded) |
| 22 | 18:33–18:34 attempt 2 closes: distribution surface, compiled Wrap-up faces, T031–T033 | `c7de21a0`, `92037f07`, `e6696a0f`; `notes/quickstart-run.md` S1–S8 all real outputs; `verification.md` SC-001..SC-011 all `pass`; suite 64 failed / 3951 passed with `comm -13` against the frozen 71-name list **empty** | None — frozen baselines were never relaxed even though 7 names turned green |
| 23 | Wrap-up engine calls run with incomplete flags in every stage of this run | The compiled face this reviewer is executing (`/storage/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.review.md` § Wrap-up) step 1 reads `run-determination.py --action determine --unit-id "/speckit.review" --unit-type command` (no `--run-id`, no `--complexity`, no source flag) and step 3 reads `feedback-utils.py --action record --unit-id … --unit-type command` (no `--run-id`, no `--review`). Known open since `/storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md` line 89, dated **2026-10-15**, route `direct-fix`, status **open**. Hit in **all 10** command-unit wrap-ups of this feature run — 13 feedback entries dated 2026-10-19, 10 of them `/speckit.*` units: `T071229Z-requirements`, `T072038Z-clarify`, `T075055Z-plan`, `T080718Z-tasks`, `T081434Z-checklist`, `T083518Z-clarify`, `T085059Z-plan`, `T085937Z-tasks`, `T103809Z-implement`, `T114446Z-review` | **Yes** → **F4** |
| 24 | Coverage lane run by this reviewer, not by any stage | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/062-humanize-command` → `status: baseline-missing`, `ERROR frozen baseline not found: …/coverage-baseline.txt`, `512 error(s), 0 warning(s)`, `[fr-uncovered] fail (16) — 13 of 29 FRs cited from citation groups`. `find .specify/specs -name coverage-baseline.txt` → **only 053** has one (dated Oct 5). `grep -rl account-clause-coverage templates/ skills/` → **zero hits** | **Yes** — the lane is dark for every feature after 053 → **F1** |
| 25 | Now: `/speckit.review` | Same-author gate does not fire (§0). 4 P0 candidates raised; **all 4 downgraded** by independent read-only validators (F1→P1, F2→P1, F3→P1, F5→P2) | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 3 |
| Workflow | 2 |
| Documentation | 1 |

Four candidates were initially rated P0 and **all four were downgraded by independent validation** — see §7 for the per-finding validation notes and what the 4/4 downgrade rate means.

## 3. Findings (Problems & Improvement Targets)

### F1 — The clause-coverage rule's owner never declares the paren charset, so one corpus yields two self-consistent "measured" totals — the exact failure the owner's own rationale exists to prevent

- **Severity**: P1 `(validated: downgraded from P0)`
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md § 4 rule 2 (line 50); /storage/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py lines 125–140 (`parentheticals()`); /storage/project/cloud-native-ai/spec-kit/scripts/python/account-clause-coverage.py
- **Evidence** (verbatim quote):

  The owner states the rule and its rationale (`shared/definitions/contract-clause-definitions.md` lines 50 and 53):

  ```
  2. **引用组 (citation group)**:一条条款对 FR/SC 的**唯一**引用位置,是其块内**最后一个含 `FR-`/`SC-` 编号的括号组**。组外的同形字样一律按「提及 (mention)」处理,不构成引用……括号组 MUST 容忍一层嵌套(编号可带子项后缀,如 `(FR-018(a))`),MUST 支持区间写法 `FR-a…FR-b` 的展开。
  ```

  ```
  **为什么边界必须写下来**:不声明边界时,「条款引用了哪条 FR」取决于抽取器按行读还是按块读,同一份语料可得出相差数条的两个总数,而两者都自称实测。声明边界后,总数是规则的产物,不是读法的产物。
  ```

  The implementing extractor recognizes ASCII parentheses only (`scripts/python/clause_extract.py:125-140`):

  ```python
  def parentheticals(text: str):
      """All balanced parenthetical groups, tolerating one nesting level."""
      groups = []
      depth = 0
      start = None
      for i, ch in enumerate(text):
          if ch == "(":
              if depth == 0:
                  start = i
              depth += 1
          elif ch == ")":
  ```

  The owner declares block boundary and inline-code span, but **never declares which characters constitute a 括号组**. 062's contracts are written with full-width parentheses: measured `（FR-` = **30**, `(FR-` = **10** across the three contract files; feature 053's contracts measure **0** and **174** respectively. Running the owner's rule with the ASCII-only extractor over 062's 35 clause blocks yields `13 of 29 FRs cited from citation groups`; re-running the identical rule with full-width parens included yields **29/29, missing none** (only three FR occurrences — FR-002, FR-013, FR-028 — sit outside any group, and all three are also cited inside one). 062's plan recorded the discrepancy and deferred it (`plan.md` line 159, item ④):

  ```
  ④ `account-clause-coverage.py` 仅匹配 ASCII 括号引用组（本契约集用全角括号，13/29 不命中）——既有工具/书写惯例分歧，未产生虚假声明（门的覆盖核径为 `clause_blocks` 正文扫描），非本轮修复面，留作观察披露。
  ```

  The same class was already diagnosed and fixed once, at feature level, in `/storage/project/cloud-native-ai/spec-kit/.specify/specs/053-machine-decidable-artifacts/feature-ref.md` line 42:

  ```
  **(2026-10-03 第三处缺陷与本次重导)**:上面两张表此前由一条**没有写下来的规则**生成……并且对同一条款给出 190/192/193 三种总数中的一种。现在规则写在 `contracts/clause-coverage.md` C-2……
  ```

  The lane itself is unwired: `grep -rl account-clause-coverage` over `/storage/project/cloud-native-ai/spec-kit/templates/` and `/storage/project/cloud-native-ai/spec-kit/skills/` returns **zero hits** — no command template and no skill invokes it. On 062 it exits with `status: baseline-missing`, `ERROR frozen baseline not found: …/coverage-baseline.txt`, `512 error(s), 0 warning(s)`; `find .specify/specs -name coverage-baseline.txt` locates exactly one baseline, in 053, dated Oct 5.

- **Why it's a problem**: The owner doc's stated purpose is to make the total "规则的产物,不是读法的产物", yet the one parameter it leaves undeclared — the paren charset — is sufficient to produce two self-consistent totals (13/29 vs 29/29) from the same 35 clause blocks, both claimable as measured. 062's published `covered 29 / missing NONE` (`feature-ref.md` line 41, `notes/quickstart-run.md` line 157) is **correct** under the full-width reading and `plan.md` line 159 is right that no false claim was published; the defect is the undeclared axis plus a checker lane that no stage calls and that cannot run green on any feature after 053. This is 053's "没有写下来的规则" recurring one level up, in the shared owner that 053's fix was promoted into.
- **Proposed fix**: (a) In `/storage/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md` § 4 rule 2, add one sentence declaring the charset explicitly — an opening group delimiter is `(` **or** `（`, its matching closer `)` **or** `）`, nesting matched within the same width — so the total stops depending on the extractor's implementation choice. (b) In `/storage/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py` `parentheticals()` (lines 125–140), accept both widths and add a self-test sample with a full-width group. (c) Wire the lane: add an `account-clause-coverage.py` invocation to `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` and freeze a `coverage-baseline.txt` per feature the way `create-tasks` freezes the other four baselines, so `status: baseline-missing` cannot be the steady state.

### F2 — No stage is accountable for answering checklist items, and `/speckit.analyze` is checklist-blind, so a gap written down at 16:13 was re-discovered at 16:32 and the checklist still stands at 0/40

- **Severity**: P1 `(validated: downgraded from P0)`
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md; /storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md (§ artifact load table); /storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md lines 44–54 (§ Step 2 — Checklist exemption gate)
- **Evidence** (verbatim quote):

  The checklist recorded the gap explicitly at 16:13 (commit `f2fe4027`, `checklists/requirements-quality.md` line 17 **as authored**):

  ```
  - [ ] CHK005 - 对外部文档中「看起来像指令的内容」（提示注入）是否规定按数据处理、不得改变命令行为？ [覆盖/安全, Gap]
  ```

  and line 26 as authored:

  ```
  - [ ] CHK011 - 混合语言的「主语言」是否有可操作的判定规则（字符占比、句子占比、逐段判定）？ [术语/清晰性, Req §FR-013, §SC-003]
  ```

  Nineteen minutes later `/speckit.analyze` round 1 raised the same two subjects as its only HIGH findings, and `requirements.md` line 258 records the outcome:

  ```
  H-01 落为 FR-029 与 SC-011（提示注入防线），H-02 落为 FR-013/SC-003 的主语言判定规则
  ```

  Analyze cannot see the checklist: `grep -c checklist` returns **0** for both `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` and `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md`, and the skill's § load table enumerates requirements / plan / tasks / registry only. The repair cost three commits — `173c897d` (16:32), `d0523cfe` (16:49), `c831e7ec` (16:58) — bounded at ≤19 minutes after the gap was already written down by the two commit timestamps `f2fe4027` 16:13 → `173c897d` 16:32 (no direct analyze timestamp exists in the artifacts).

  The checklist was never answered. Its own closing note (`checklists/requirements-quality.md` line 74) states the disposition:

  ```
  Repair round 1 … 闭合了 CHK005 与 CHK008 原标注的 Gap——两处仅更新追溯标注，条款问题文本未删改
  ```

  The file stands at **0/40**, so implement's gate always fires and always needs a waiver (`waivers.md` line 10):

  ```
  The items remain formally unchecked because no stage owns flipping them post-analysis; requiring that here would block implement on a bookkeeping form, not on an open quality gap.
  ```

  The gate that fires (`skills/internal/implement-feature/SKILL.md` lines 44–54) offers only STOP → ask "Proceed anyway?" → waiver; it has **no branch for refreshing or closing a checklist whose questions a later stage actually resolved**. And the closure procedure is not merely missing here — it was prescribed for a prior feature and never landed. `/storage/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/review.md` line 541:

  ```
  - **REC-C5 — Make checklists append-only and evidence-quoted.** Target: `…/skills/internal/create-checklist/SKILL.md:94`. Change: new recheck file per run; every `[x]` quotes the requirement line; no in-place refresh. Source: F5. Expected impact: checklist evidence stays truthful and auditable.
  ```

  and line 542:

  ```
  - **REC-C6 — Define the waiver closure format.** Target: `…/skills/internal/implement-feature/SKILL.md` § Checklist exemption gate. Change: `Scope` / `Basis` / `Disposition` / `Closed`; list upstream artifact edits. Source: F13. Expected impact: waivers stop being stale open-ended records.
  ```

  Neither is present in its named target. 061 did in fact refresh its own checklists in place (`/storage/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/waivers.md` line 9 "the implement wrap-up refreshed both checklists (M-03)"; `checklists/config-quant.md` = 36/36 checked, closed 2026-10-18) — but 061's own review F5 (P1) judged that in-place refresh defective, which is why REC-C5 exists. 062's annotate-don't-flip choice is therefore at least as defensible as 061's; the framework simply has no rule either way.

- **Why it's a problem**: A checklist that no stage owns answering produces a permanent 0/N artifact whose only downstream effect is to fire a gate that must be waived every single feature. Meanwhile the *content* it produces is real — CHK005 and CHK011 named the two defects analyze would independently escalate to HIGH — but nothing routes that content to analyze, so the same ground is covered twice and the second pass pays for it in a three-commit repair loop. `templates/commands/checklist.md` § Handoffs does route *failures* "Back to Plan / Back to Tasks", and analyze round 1 did consume checklist-adjacent content; the precise defect is **accountability**, not total absence of a consumer.
- **Proposed fix**: (a) Add the feature's `checklists/*.md` to the artifact load table in `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md` and one line to `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` requiring every unchecked item tagged `Gap` to be either raised as a finding or explicitly dispositioned — so a written-down gap can never be silently re-discovered. (b) In `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` § Step 2 — Checklist exemption gate, add the missing third branch: when a later stage has resolved an item's subject, that stage records the answer (append-only recheck file per REC-C5) instead of leaving the row permanently `- [ ]`; and adopt REC-C6's `Scope` / `Basis` / `Disposition` / `Closed` waiver format so a waiver states what closed it.

### F3 — The review→improvement loop is a dead letter: recommendations have no owner, no intake path, and (in the prior report) no resolvable target paths

- **Severity**: P1 `(validated: downgraded from P0)`
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/review.md line 52 (§ Handoffs "After"); /storage/project/cloud-native-ai/spec-kit/templates/instructions-template.md § ID Register; /storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md lines 79–81 (§ Scope guard); /storage/project/cloud-native-ai/spec-kit/.specify/memory/register.md; /storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md
- **Evidence** (verbatim quote):

  The handoff that is supposed to carry this report's output names no owner (`templates/commands/review.md` lines 48–52):

  ```
  ## Handoffs

  **Before**: Run after `/speckit.implement` for complete artifact chain.

  **After**: Apply improvements to spec-kit templates/commands/scripts. Optionally iterate requirements/plan.
  ```

  "Apply improvements" is an instruction to nobody. Ten prior `review.md` reports exist (022, 032, 033, 035, 045, 047, 050, 054, 059, 061); 061 alone emitted **22** distinct `REC-` recommendations. The ID register — whose stated rule is that every durable identifier is recorded "**at the moment the ID is coined**" (`/storage/project/cloud-native-ai/spec-kit/.specify/instructions.md` § ID Register) — holds **20** data rows and `grep -c 'REC-\|review\.md'` over it returns **0**. The feedback backlog, the only other plausible intake, cites `review.md` **0** times, and its scope guard closes that door by design (`shared/workflow/feedback-step.md` lines 79–81):

  ```
  3. **Scope guard.** Keep strictly to *this* unit's operation. Do NOT produce a
     global/whole-project assessment — that is `/speckit.review`'s job. Every entry is
     `scope: local`.
  ```

  Review RECs are global/whole-project assessments by definition, so they are structurally **ineligible** for the backlog that would otherwise track them. The one framework-level item from this run that *did* reach the backlog got there through a different door — `/speckit.feedback` Mode 5 自省, which the scope guard explicitly exempts — and has sat **open** since 2026-10-15 (`backlog.md` line 89, "Wrap-up 编译嵌入缺 `--run-id`/必填参数全集…", route `direct-fix`, four target files named).

  The second failure mode is path portability. `/storage/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/review.md` line 541 names its target as:

  ```
  Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-checklist/SKILL.md:94`
  ```

  That report contains **134** occurrences of the `/Users/liuqiming.lqm/…` root and **zero** of the current root `/storage/project/…`; all nine other prior reviews use the current root. Its 22 RECs therefore point at paths that resolve on no machine but the one that wrote them.

  Genuine same-class recurrences reached 062 anyway, by re-diagnosis rather than by retrieval. `/storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/review.md` line 86:

  ```
  ### F1 — implement 期纠正只向证据注记披露、不向设计制品回写:HEAD 上留有 7 处已知陈旧事实
  ```

  and line 216:

  ```
  ### F4 — 任务超面交付使 red-first 纪律静默塌陷:仅靠执行者自披露发现,无机械边界
  ```

  059-F4's shape recurs exactly in 062's s11 incident (F6 below); 059-F1's shape recurs only partially — 062's stale premise is a single qualified row (F5), not seven unqualified assertions, because 062's authoritative § Environment Prerequisites did get corrected in place.

- **Why it's a problem**: The most expensive artifact in the whole lifecycle — a full critical process review — produces recommendations that no stage reads, no register indexes, no backlog can accept, and (in the last instance) no other machine can resolve. Every subsequent feature re-diagnoses the same defects from scratch. This is not a missing-carrier problem: the carriers exist (`register.md`, `backlog.md`, `probe-definitions.md` gate rows); only the wiring from `review.md` into them is absent. It is **not** P0: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/constitution.md` Principle XIII "adds orientation, **not machinery**" and "MUST NOT be used to justify new scoring systems, maturity reports, **recording engines**" — so no new tracking subsystem may be invented to fix this, and nothing here blocks correct use of the tool or risks silent corruption.
- **Proposed fix**: (a) In `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md` § Handoffs "After", replace the ownerless sentence with a named owner and a machine-checkable duty: every `REC-` id coined in a review is registered in `.specify/memory/register.md` in the same commit, per the ID Register rule. (b) In `/storage/project/cloud-native-ai/spec-kit/templates/instructions-template.md` § ID Register, add `REC-` to the enumerated durable-identifier list (`D-…`, `OI-…`, `S…`, `T-…`, `F-…`, `B-…`) so the duty is discoverable from the ambient layer, not only from the review command. (c) In `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md` § Scope guard, add one clause opening a framework-scope intake for review RECs (or naming the exempt path that already exists — Mode 5 自省 — as the route), so a global recommendation has somewhere legal to land. (d) In `/storage/project/cloud-native-ai/spec-kit/templates/review-template.md` § 5 and Replacement Rule 3, require each REC target to carry the **repo-relative** path as the primary form with the absolute path parenthetical — the inverse of what 061 did — since a relative path resolves on every checkout and an absolute one resolves on exactly one. (e) In `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feature-integration.md`, give `/speckit.review` its own row in the transition table (see the addendum below) so the stage that produces the review evidence is also the stage that records it.

- **Post-validation addendum (found after the validation wave; NOT independently validated)** — a third failure mode of the same root, discovered while running this stage's own wrap-up: `/speckit.review` has no declared downstream duty **at all**, and that includes the feature registry. `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md` states "Each command owns exactly one transition" and its table lists five commands — `/speckit.requirements`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, `/speckit.checklist` — with `Implemented → Ready for Review` owned by `/speckit.checklist` and **no row for `/speckit.review`**. Meanwhile the per-feature status criteria in `/storage/project/cloud-native-ai/spec-kit/.specify/memory/features/062.md` § Status Tracking line 72 define the target state by exactly what this stage produces:

  ```
  - **Ready for Review**: deferred 解决/豁免；review 证据产出。
  ```

  Both conditions are now met for 062 — 33/33 tasks `[X]` with zero `[~]`, the single open item waived in `waivers.md`, and `review.md` committed — yet the registry still reads `**Status**: Implemented`, because the only command that owns that transition (`/speckit.checklist`) ran at 16:13, *before* implement, and cannot fire it retroactively. Feature 036 shows the intended end state (`/storage/project/cloud-native-ai/spec-kit/.specify/memory/features.md` line 45): status `Ready for Review`, notes cell recording "review.md produced 2026-07-25: 0 P0 / 3 P1 / 4 P2 process findings". 062's four prior stages each landed a dated `## Latest Review` entry in `features/062.md`; this stage has no rule telling it to. The reviewer did **not** write the registry, because the two recorded readings conflict (the workflow owner withholds the transition from review; the feature's own criteria doc says the state is satisfied) and resolving that requires inventing a duty no artifact declares — it is thrown back to the orchestrator instead.

### F4 — Compiled Wrap-up faces omit required engine flags, so every stage's wrap-up starts by failing; the fix has been a named open backlog row since 2026-10-15

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/probe-utils.py (`--action compile-embeds` renderer); /storage/project/cloud-native-ai/spec-kit/shared/definitions/probe-definitions.md (§ Handler / § HandlerBinding — the compiled-face truth source); consumers `/storage/project/cloud-native-ai/spec-kit/scripts/python/run-determination.py` and `/storage/project/cloud-native-ai/spec-kit/scripts/python/feedback-utils.py`
- **Evidence** (verbatim quote):

  The compiled face this reviewer is executing right now (`/storage/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.review.md` § Wrap-up, itself an AUTO-GENERATED block whose header reads "*truth source: .specify/shared/definitions/probe-definitions.md … fingerprint: 7877db82c58c — do not edit; edit the registry, then recompile*"):

  ```
  1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "/speckit.review" --unit-type command`
  2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "/speckit.review" --unit-type command`
  3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "/speckit.review" --unit-type command`
  ```

  Steps 1 and 3 carry only `--unit-id` / `--unit-type`; both engines require more and fail one missing parameter at a time. The defect is already diagnosed, targeted and routed — `/storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md` line 89, dated **2026-10-15**, status **open**:

  ```
  | 2026-10-15 | introspection-20261015T081832Z#F-01(15 条成员 + G-D 聚类) | **Wrap-up 编译嵌入缺 `--run-id`/必填参数全集,两引擎逐参单错**:`templates/commands/plan.md:55-56`、`clarify.md:44-45` 嵌入行仅 unit-id/unit-type;`run-determination.py:1390-1397` 与 `feedback-utils.py:716-728` 逐参顺序抛错;`probe-utils.py` compile-embeds 无占位约定(058 T033 只修注册缺口) | direct-fix | `scripts/python/probe-utils.py`(渲染占位约定)、`scripts/python/run-determination.py`、`scripts/python/feedback-utils.py`(缺参一次全列)、`templates/commands/**`(重编译) | open(修复须同步全部编译单元重编译 + `--reconcile` 收口;15 条本地条目 + 全部命令单元同面) | — |
  ```

  It fired in **all ten command-unit wrap-ups of this one feature run**. Measured from `/storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/`: 2026-10-19 holds 13 entry files, of which 10 are `/speckit.*` command units — `20261019T071229Z-speckit-requirements.md`, `T072038Z-speckit-clarify.md`, `T075055Z-speckit-plan.md`, `T080718Z-speckit-tasks.md`, `T081434Z-speckit-checklist.md`, `T083518Z-speckit-clarify.md` and `T085059Z-speckit-plan.md` and `T085937Z-speckit-tasks.md` (the analyze repair round re-ran clarify/plan/tasks), `T103809Z-speckit-implement.md`, and `T114446Z-speckit-review.md` (this stage). Each of the ten files exists only because its executor supplied the flags the compiled face omits — an unrecorded in-passing repair every time. The store as a whole holds 78 entry files, 49 of them `/speckit.*` unit wrap-ups, spanning 2026-10-13 → 2026-10-19, with 72 pending since the last submission.

  This stage reproduced the defect first-hand and surfaced a second-order consequence the backlog row does not record. Running the face verbatim: step 1 exits **2** with `error: --run-id is required: the key is (unit_id, run_id)`; supplying `--run-id` yields exit **2** again with `error: --complexity is required: it is a caller declaration, never an engine derivation`; step 3 exits **2** with `error: --run-id is required.`, then exit **2** again with `error: record requires a non-empty --review / --review-file.` — four round-trips to discover one call's required set, because each engine reports one missing parameter at a time. Then, once the minimum is supplied, the determination record lands with `token_consumption not_evaluated (source_unavailable)`, `elapsed not_evaluated (source_unavailable)`, `artifact_correctness not_evaluated (no_declared_checks)` — the face names no source flag (`--session-file`, `--session-rows`, `--declared-check`, `--green-check`), so a verbatim executor measures nothing. And the record cannot be re-sourced afterwards: `/storage/project/cloud-native-ai/spec-kit/scripts/python/run-determination.py` lines 1411–1413 make the key idempotent by design,

  ```python
      existing = load_determinations(workspace_root, unit_id)
      if any(item["record"].get("run_id") == args.run_id for item in existing):
          return {"duplicate": True, "unit_id": unit_id, "run_id": args.run_id,
                  "note": "this (unit_id, run_id) was already determined"}, EXIT_OK
  ```

  so a re-run with the full source set returns `duplicate: /speckit.review speckit-review-20261019T114047Z was already determined`. The idempotency is correct design ("每轮一条"); the defect is that the face guarantees the first, under-sourced call is the only one.

- **Why it's a problem**: A compiled face that cannot be executed as written trains executors to treat AUTO-GENERATED blocks as approximate — the opposite of the discipline that makes them safe to regenerate. Worse, the face's omission is not merely inconvenient: it silently degrades the 运行判定 sensor to three `not_evaluated` axes and then locks that state in, so the improve flow receives no measurement for the run at all. The registry is the declared truth source and `probe-utils.py` is the only renderer, so the fix has exactly one landing point; leaving it open means every unit's wrap-up on every feature pays the toll and silently diverges from the compiled text.
- **Proposed fix**: Land `backlog.md` line 89 as written. Concretely: add a rendering-placeholder convention to the `compile-embeds` renderer in `/storage/project/cloud-native-ai/spec-kit/scripts/python/probe-utils.py` so a handler line can carry its full required-flag set (including run-scoped values like `--run-id`), make `/storage/project/cloud-native-ai/spec-kit/scripts/python/run-determination.py` and `/storage/project/cloud-native-ai/spec-kit/scripts/python/feedback-utils.py` report **all** missing required parameters in one error instead of one at a time, then recompile every unit and close with `--reconcile`. Flip the backlog row's status in the same commit.

### F5 — A superseded environment premise survives in `tasks.md` § Assumptions with no date stamp and no cross-reference to the row that corrected it

- **Severity**: P2 `(validated: downgraded from P0)`
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/tasks.md line 281 (D-T2), read against line 41 (§ Environment Prerequisites) and line 301 (§ Measured premises); fix targets /storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md lines 202–206 (§ Environment probe rules, item 2 "Single landing point") and /storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md line 85 (§ Environment Prerequisites)
- **Evidence** (verbatim quote):

  `tasks.md` line 281 still asserts the pre-restoration state as present fact:

  ```
  - **D-T2 (environment degradation)**: the plan-frozen 71-name baseline remains authoritative; the current 94-name capture is 23 environment-induced additions caused by the missing `cws-lib-bash` dependency. T026/GATE-1 must record a blocked/degraded verdict while the dependency is unavailable and MUST NOT relax or rewrite the baseline.
  ```

  The authoritative row, `tasks.md` line 41, was corrected in place at implement time and says so:

  ```
  - `cws-lib-bash` (`CWS_LIB_BASH_HOME`): **restored**（2026-10-19 implement 阶段实测更正——先前的「unavailable」降级记录已过期）— probe: `bash scripts/bash/run-tests.sh --names-out` @ 2026-10-19 → `71 failed, 3929 passed`……
  ```

  Line 301 handles the same fact correctly — it is a dated re-capture with an explicit cross-reference:

  ```
  - Current suite re-capture: `bash scripts/bash/run-tests.sh --names-out /tmp/humanize-tasks-current-failed.txt` → `94 failed, 3906 passed`; `comm -13 notes/baseline-failed-tests.txt /tmp/humanize-tasks-current-failed.txt` → 23 added names, all in the `cws-lib-bash`-dependent cluster (see § Environment Prerequisites).
  ```

  D-T2's heading `### Assumptions and decisions` carries no date stamp, and unlike line 301 the row has no `(see § Environment Prerequisites)` pointer. `notes/pre-change-measurements.md` § 4 states the verdict plainly: "The tasks.md § Environment Prerequisites degradation record … is **expired**".

  The rule that should have caught it enumerates only two carriers (`/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` lines 202–206):

  ```
  2. **Single landing point**: record every probe conclusion exactly ONCE, in the generated
     tasks.md's `## Environment Prerequisites` section (see
     `.specify/templates/tasks-template.md`). Per-phase prerequisites and `[~]` task notes
     MUST reference that section instead of restating verdicts — two hand-synced copies of
     the same conclusion drift apart.
  ```

  A free-prose `**D-Tn**` assumption row is neither a per-phase prerequisite nor a `[~]` task note, so it falls outside the enumeration — even though the rule's own stated rationale ("two hand-synced copies of the same conclusion drift apart") describes exactly what happened. Note also that `### Assumptions and decisions` appears nowhere in `/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md` (its section list runs DoD → Completion Gate → Environment Prerequisites → Format → Path Conventions → Phases → Dependencies), so the section itself is an ad-hoc carrier no template governs.

- **Why it's a problem**: An auditor reading § Assumptions top-down meets a present-tense factual claim ("the missing `cws-lib-bash` dependency") that the same file's authoritative section contradicts, with nothing on the row to signal which one is current. The mechanism is a closed carrier list in the single-landing-point rule: any restatement of an environment verdict in a carrier the list does not name escapes the "MUST reference that section" duty. This is audit friction only, not a compliance break: the re-freeze owner rule (`/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` § Re-freeze timing, lines 373–378) governs the frozen `notes/` files and **task rows**, not § Notes prose; the cross-artifact drift check at `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` lines 211–214 is satisfied (`plan.md` and `requirements.md` carry zero stale copies of this claim); DoD-7 (line 23) and GATE-1 (line 30) are correctly written as conditionals and were discharged by the restoration. The residual is narrower than a discipline violation — which is why validation downgraded it.
- **Proposed fix**: Open the carrier list rather than adding a new rule. (a) In `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` lines 202–206 item 2, replace "Per-phase prerequisites and `[~]` task notes" with "Per-phase prerequisites, `[~]` task notes, **and any assumption/decision or free-prose row**", so the "MUST reference that section instead of restating verdicts" duty covers every carrier. (b) In `/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md` line 85 § Environment Prerequisites, extend the ACTION REQUIRED comment's "Per-phase prerequisite notes and …" sentence the same way, and add: any row restating an environment verdict MUST carry an ISO date stamp and a `(see § Environment Prerequisites)` pointer. That makes a superseded row self-announcing without forcing a rewrite of a legitimate dated record.

### F6 — Nothing binds a claimed evaluation sample to its archived evidence, so "we ran s11" was falsifiable only by the executor's own honesty

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/verification.md line 180; /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/tasks.md line 37 (GATE-8); fix target /storage/project/cloud-native-ai/spec-kit/shared/definitions/probe-definitions.md (§ command-gate rows) + `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`
- **Evidence** (verbatim quote):

  The incident, self-recorded at `verification.md` line 180:

  ```
  **s11 补正记录**：本节初稿曾声称 s11 已 PASS 而实际未执行——发现后立即补跑
  ```

  The only mechanical check that touches this surface is an existence test (`tasks.md` line 37):

  ```
  - GATE-8: 17 deliverables present — check: verify each path from `feature-ref.md` § 交付面清单 with `test -e`; report any missing path as a gate failure.
  ```

  `test -e` passes for a stale file, an empty file, or a file written by a different sample. The archived corpus at `/storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/e8-run/` holds 13 entries (`s01`–`s06`, `s08`–`s11`, `files/`, `files-branches.md`, `tone/`), and nothing asserts that the row claiming `s11 PASS` in `verification.md` § E8 corresponds to the bytes in `notes/e8-run/s11-rewritten.txt`, or that those bytes postdate the claim.

  The reason nothing can assert it is that the verification artifact has no structured slot for behavioral evidence. `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md` (`templates/verification-log-template.md`) is a flat key-value log — its declared sections are `# -- Baseline …--`, `# -- /speckit.implement results --`, `# -- Success Criteria evaluation --` ("*One block per SC from requirements.md. Status values: pass | fail | partial | deferred | unknown*"), `# -- Deferred tasks …--` and `# -- Free-form notes --`. There is no per-sample evidence record anywhere in it. 062's 434-line `verification.md` consequently invented its own evidence tables (§ E8-US1, § E8-Files B01–B17, § 语气与受众矩阵), which is why the s11 claim had no machine-readable counterpart to check against. The same shape was already reported once, for a different mechanism — `/storage/project/cloud-native-ai/spec-kit/.specify/specs/059-exec-quant-recording/review.md` line 216:

  ```
  ### F4 — 任务超面交付使 red-first 纪律静默塌陷:仅靠执行者自披露发现,无机械边界
  ```

- **Why it's a problem**: Behavioral-evaluation evidence is the load-bearing proof for every clause a structural contract test cannot pin. 062's `/storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/contracts/rewrite-behavior.md` carries 14 such clauses and declares its own channel in its header: "行为验证主通道为 E8 评估协议（语料 + 量规 + 两位独立评审 + 确定性差异脚本）；结构面由契约测试钉扎". If the only thing standing between "claimed PASS" and "actually executed" is the executor's self-disclosure, then a green SC row is a claim rather than evidence — precisely the anti-pattern named in `/storage/project/cloud-native-ai/spec-kit/.specify/shared/guidelines/fast-fail.md` ("A green check is a claim, not evidence"). 062 caught it; the process did not. And because the evidence tables are ad-hoc per feature, no cross-feature tooling could ever check them even if one existed.
- **Proposed fix**: Two changes, both reusing existing machinery. (a) Add a structured evidence-record section to `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md` between `# -- /speckit.implement results --` and `# -- Success Criteria evaluation --`: one row per evaluation sample, carrying sample id → archived artifact path → content hash → verdict, so a `pass` claim has a machine-readable counterpart. (b) Register a new gate row in `/storage/project/cloud-native-ai/spec-kit/shared/definitions/probe-definitions.md` alongside the existing `gate-implement-checklist-waiver` row (line 116) — e.g. `gate-implement-evidence-binding`, class `command-gate`, object `/speckit.implement` — whose check reads: for every sample recorded `pass`, the archived artifact exists, is non-empty, and its hash matches the recorded hash. Reference the new gate from `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` next to GATE-8. This extends the existing gate-probe mechanism rather than adding a subsystem.

### F7 — The baseline re-freeze duty is declared on the producer side only, so implement meets a stale frozen number and must invent a reconciliation procedure

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md lines 373–378 (§ Re-freeze timing); missing counterpart in /storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md and /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md
- **Evidence** (verbatim quote):

  The producer declares a duty for a stage it does not run (`skills/internal/create-tasks/SKILL.md` lines 373–378):

  ```
  somewhere to write. **Re-freeze timing**: these files are frozen measurements, so they
  inherit the never-cache rule the Environment Prerequisites probes above already state —
  re-capture on every generation and every rerun of this command, and re-capture at the
  start of `/speckit.implement` whenever the tree has advanced since generation. A row whose
  re-capture yields a different value carries the new value; MUST NOT keep citing the stale
  frozen one.
  ```

  Neither `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` nor `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md` carries a corresponding step — the consumer never learns it has this duty. The consequence in 062 (`notes/pre-change-measurements.md` § 2 and § 5): the frozen mirror record says **209** DIFF names, the implement-time capture says **113**, and the gap had to be explained by a reconciliation procedure invented for the occasion under a heading that exists in no template:

  ```
  ## 5. Mirror-face premise note (honest drift accounting)

  The frozen mirror baseline records 209 DIFF lines; the pre-change capture reports **113**. Name-level comparison:
  - NEW vs frozen baseline: exactly **1** — `.specify/skills/internal/manage-feedback/SKILL.md`. Provenance check (git log): source last touched by b2e5ef6b (059 era), mirror last landed by af70a81c ("update specify version") — divergence predates this implement run and is NOT attributable to this feature…
  - Fixed since baseline: 97 names (mirror syncs landed between plan-time freeze and implement start — upstream repairs, out of 062 scope).
  ```

  The same capture also had to declare a tasks.md premise expired on its own initiative (§ 4): "The tasks.md § Environment Prerequisites degradation record … is **expired**: the current run reproduces the frozen 71-name set exactly."

- **Why it's a problem**: 96 of 113 vs 209 differences were upstream repairs and one was inherited — none attributable to this feature — but establishing that required a per-feature `git log` provenance investigation and a bespoke §5 write-up that no template asks for and no later feature will know to reproduce. The tiered criterion 062 applied (untouched pairs relative / touched pairs absolute) is sound; the problem is that arriving at it was ad-hoc rather than prescribed, so the next feature starts from a number it cannot interpret.
- **Proposed fix**: Mirror the duty onto the consumer. Add a pre-flight step to `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` (immediately before its Step 1) reading: re-capture every frozen baseline in `notes/baseline-*` ; where a re-capture differs, write the new value into the row that cites it, and classify each difference as *upstream repair* / *inherited* / *attributable to this feature* using `git log` provenance before any drift verdict is issued. State the same step in `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md` so it reaches the command face, and have `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` § Re-freeze timing point at that consumer step instead of describing a duty it cannot enforce.

### F8 — Red-first evidence binds the name-level baseline gate to the wrong GATE id

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/notes/red-first-evidence.md line 39, read against /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/tasks.md lines 30 and 36
- **Evidence** (verbatim quote):

  `notes/red-first-evidence.md` line 39:

  ```
  Baseline comparison stays a runtime gate: full-suite name-level `comm -13` vs `notes/baseline-failed-tests.txt` must be empty at **GATE-7** (C-9)
  ```

  But `tasks.md` line 36 defines GATE-7 as a structural check, not a baseline check:

  ```
  - GATE-7: Structural validity — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/062-humanize-command/tasks.md` exits 0 with 35 green claims and no collision; `python3 .specify/scripts/python/validate-requirements.py .specify/specs/062-humanize-command/requirements.md` exits 0.
  ```

  The name-level baseline comparison is **GATE-1**, and `/storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/feature-ref.md` § SC-008 independently confirms the criterion belongs there: "`comm -13 notes/baseline-failed-tests.txt <新名单>` 为空".

- **Why it's a problem**: Small, but it is the class of error that makes cross-artifact citation untrustworthy: a reader following the pointer lands on a gate that checks something else entirely and has no way to tell whether the note or the task list is authoritative. GATE ids are renumbered when a tasks list is edited, and nothing requires a note that cites one to be re-derived.
- **Proposed fix**: In `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`, wherever the red-first evidence note's shape is prescribed, require the note to quote the gate row **verbatim** (id + name + check command) rather than citing a bare id, so a renumbering produces a visible mismatch instead of a silent wrong pointer. Repair the 062 instance by correcting line 39 to GATE-1 — a one-token fix in a `notes/` record, not in a governed artifact.

## 4. What Worked — Preserve (Brief)

- Story/task-grouped commits (17 commits, 15:11→18:34) made a full git-based timeline reconstruction possible with no working-tree fallback.
- Red-first evidence was honest about its own exceptions: `notes/red-first-evidence.md` reports 8 failed / 2 passed and explains *why* the 2 pre-passed, instead of hiding them.
- Contract clauses genuinely express their mapped FRs. Verified by quoting clause bodies C-11..C-23 and C-35 against the FR texts, not by checking that both ids resolve — the mapping-table trap in `objective-analysis-gate.md` rule 4 does not apply here.
- `diff_protected.py` had real discriminating power: it caught the s02 `cost-effective` loss and the s09 dropped `tags:` frontmatter line, producing genuine red-green loops rather than decorative passes. Its `--selftest` (clean pair exit 0 / mutated pair exit 1) proves the checker would go red when its subject breaks.
- The tone/audience matrix produced a real reviewer **FAIL** on the T-audience leg, a repair, and a third-reviewer reversal — the evaluation protocol can fail a sample and recover.
- The unplanned `probe-utils.py` change was proven necessary by an actual rollback experiment (`--check` exit 2 `probe registry invalid` → exit 0 `74 units, zero drift`) instead of being asserted, then recorded as a deviation. Textbook fast-fail handling.
- Frozen baselines were never relaxed or rewritten, even though 7 previously-failing names turned green and `comm -23` would have flattered the run. The verdict was judged on `comm -13` only.
- Baseline criteria tiering (untouched pairs relative / touched pairs absolute byte-equality) was principled and stated before measurement.
- Inline self-corrections were left visible rather than silently edited out: the s11 补正记录, the B11 basename typo, the T013 engine hardening.
- The Stop-hook + status/sentinel **dual-signal** fallback survived a real API crash: the hook fired, no sentinel was emitted, the status record was judged FAILED, and attempt 2 resumed from the breakpoint at 30/33 without redoing completed work.

## 5. spec-kit / SDD Improvement Recommendations

> Every target below is a **framework-source** path (`templates/`, `shared/`, `scripts/`, `skills/`), never a `.specify/` runtime copy, per `/storage/project/cloud-native-ai/spec-kit/.specify/instructions.md` § Two Hats. The parenthesised relative form is the portable one; the absolute form is this checkout's root.

### 5.1 Template Improvements

- **Open the single-landing-point carrier list** — Target: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` (`skills/internal/create-tasks/SKILL.md`) lines 202–206 item 2, and `/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md` (`templates/tasks-template.md`) line 85 § Environment Prerequisites ACTION REQUIRED comment. Change: replace the closed carrier enumeration "Per-phase prerequisites and `[~]` task notes" with one that also names any assumption/decision or free-prose row, and require any row restating an environment verdict to carry an ISO date stamp plus a `(see § Environment Prerequisites)` pointer. Source: F5. Expected impact: a superseded premise announces itself instead of contradicting the same file's authoritative section silently, and no restatement can escape the rule by sitting in an unlisted carrier.
- **Add a structured evidence-record section to the verification log** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md` (`templates/verification-log-template.md`), between `# -- /speckit.implement results --` and `# -- Success Criteria evaluation --`. Change: add a per-sample evidence record — sample id → archived artifact path → content hash → verdict — so a `pass` claim has a machine-readable counterpart; the template today is a flat key-value log with no such slot, which is why 062 invented its own § E8-US1 / § E8-Files / § 语气与受众矩阵 tables. Source: F6. Expected impact: makes the claim-to-evidence binding mechanically checkable, which is the precondition for the evidence-binding gate probe in §5.3.
- **Make REC targets repo-relative-first** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/review-template.md` (`templates/review-template.md`), § 5 and Replacement Rule 3. Change: each REC names the repo-relative path as primary and the absolute path parenthetically. Source: F3. Expected impact: recommendations stay resolvable on any checkout — 061's 134 machine-local paths made its 22 RECs unactionable here.

### 5.2 Command Prompt Improvements

- **Make `/speckit.analyze` checklist-aware** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` (`templates/commands/analyze.md`) and `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md` (`skills/internal/analyze-artifacts/SKILL.md`) § artifact load table. Change: add the feature's `checklists/*.md` to the load table, and require every unchecked item tagged `Gap` to be either raised as a finding or explicitly dispositioned in the gate report. Source: F2. Expected impact: a gap already written down cannot be re-discovered 19 minutes later at the cost of a three-commit repair loop.
- **Name an owner in review's Handoffs** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md` (`templates/commands/review.md`) line 52, § Handoffs "After". Change: replace "Apply improvements to spec-kit templates/commands/scripts" with a named duty — every `REC-` id coined in the report is registered in `.specify/memory/register.md` in the same commit. Source: F3. Expected impact: the review artifact stops being terminal.

### 5.3 Automation / Script Improvements

- **Declare the citation-group paren charset in the owner and honour it in the extractor** — Target: `/storage/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md` (`shared/definitions/contract-clause-definitions.md`) § 4 rule 2, and `/storage/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py` (`scripts/python/clause_extract.py`) `parentheticals()` lines 125–140. Change: the owner declares `(`/`（` and `)`/`）` as the group delimiters with same-width nesting; the extractor accepts both and gains a full-width self-test sample. Source: F1. Expected impact: one corpus yields one total, which is the property § 4's rationale claims to guarantee.
- **Wire the clause-coverage lane and freeze its baseline** — Target: `/storage/project/cloud-native-ai/spec-kit/scripts/python/account-clause-coverage.py` (`scripts/python/account-clause-coverage.py`) + a caller in `/storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md` (`templates/commands/analyze.md`) + `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` (`skills/internal/create-tasks/SKILL.md`) § Re-freeze timing (add `coverage-baseline.txt` as a fifth frozen baseline). Source: F1. Expected impact: `status: baseline-missing` / `512 error(s)` stops being the steady state for every feature after 053.
- **Emit the full required-flag set in compiled Wrap-up faces** — Target: `/storage/project/cloud-native-ai/spec-kit/scripts/python/probe-utils.py` (`scripts/python/probe-utils.py`) `compile-embeds` renderer, plus all-parameter-at-once error reporting in `/storage/project/cloud-native-ai/spec-kit/scripts/python/run-determination.py` (`scripts/python/run-determination.py`) and `/storage/project/cloud-native-ai/spec-kit/scripts/python/feedback-utils.py` (`scripts/python/feedback-utils.py`); then recompile all units and close with `--reconcile`. Change: land `/storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md` line 89 as written and flip its status, and extend it in one respect the row does not yet cover — the rendered face must also name the **source** flags (`--session-file`, `--session-rows`, `--tool`, `--declared-check`, `--green-check`), not only the required ones, because `(unit_id, run_id)` idempotency at `run-determination.py:1411-1413` makes the first under-sourced call permanent. Source: F4. Expected impact: AUTO-GENERATED faces become executable as written; the ten per-run wrap-up failures on this feature disappear, and the 运行判定 sensor stops landing three `not_evaluated` axes per run.
- **Add an evidence-binding gate probe** — Target: `/storage/project/cloud-native-ai/spec-kit/shared/definitions/probe-definitions.md` (`shared/definitions/probe-definitions.md`) § command-gate rows (next to `gate-implement-checklist-waiver`, line 116), consumed from `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` (`skills/internal/implement-feature/SKILL.md`) beside GATE-8. Change: new `gate-implement-evidence-binding` — for each sample claimed `pass`, the archived artifact exists, is non-empty, and its hash matches the hash recorded in the row. Source: F6. Expected impact: "claimed but never executed" becomes a red gate instead of a self-disclosure.

### 5.4 Workflow Improvements

- **Give checklist items an accountable answering stage and define the closure format** — Target: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` (`skills/internal/implement-feature/SKILL.md`) lines 44–54 § Step 2 — Checklist exemption gate. Change: add the missing third branch (a stage that resolved an item's subject records the answer, append-only recheck file per 061's REC-C5) and adopt 061's REC-C6 waiver format `Scope` / `Basis` / `Disposition` / `Closed`. Source: F2, F3. Expected impact: checklists stop being permanent 0/N artifacts whose only effect is a gate that must be waived every feature; two prior recommendations finally land.
- **Register every `REC-` id at coinage** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/instructions-template.md` (`templates/instructions-template.md`) § ID Register (编号登记). Change: add `REC-…` to the enumerated durable-identifier list alongside `D-…`, `OI-…`, `S…`, `T-…`, `F-…`, `B-…`. Source: F3. Expected impact: recommendations become retrievable by the ambient layer, so a later feature can find a prior diagnosis instead of repeating it (059-F4 → 062-F6 is the recurrence this closes).
- **Open a framework-scope intake for review recommendations** — Target: `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md` (`shared/workflow/feedback-step.md`) lines 79–81 § Scope guard. Change: keep the local-scope rule for wrap-up entries but state explicitly which intake a global review REC uses (the Mode 5 自省 exemption already provides one), so "that is `/speckit.review`'s job" no longer means "and therefore nothing tracks it". Source: F3. Expected impact: closes the structural ineligibility that leaves `backlog.md` citing `review.md` zero times.
- **Give `/speckit.review` a row in the feature status transition table** — Target: `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feature-integration.md` (`shared/workflow/feature-integration.md`) § transition table. Change: add `| /speckit.review | Implemented → Ready for Review | Requires review.md committed and every deferred item resolved or waived |`, and note in the `/speckit.checklist` row that its transition applies only when checklist runs after implement. Source: F3 (post-validation addendum). Expected impact: the stage that produces the review evidence records it, so a reviewed feature stops sitting at `Implemented` — the state 036 reached and 062 cannot.
- **Mirror the re-freeze duty onto the consumer side** — Target: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` (`skills/internal/implement-feature/SKILL.md`), new pre-flight step before Step 1, plus one line in `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md` (`templates/commands/implement.md`); then have `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` (`skills/internal/create-tasks/SKILL.md`) § Re-freeze timing point at that consumer step. Change: re-capture every `notes/baseline-*`, write the new value into the citing row, and classify each difference as upstream repair / inherited / attributable-to-this-feature via `git log` provenance before issuing any drift verdict. Source: F7. Expected impact: implement stops meeting an uninterpretable frozen number and stops inventing a per-feature reconciliation write-up.

### 5.5 Documentation Improvements

- **Require red-first notes to quote the gate row they bind to** — Target: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` (`skills/internal/implement-feature/SKILL.md`), red-first evidence prescription. Change: quote the gate id + name + check command verbatim rather than citing a bare id, so a later renumbering produces a visible mismatch. Source: F8. Expected impact: cross-artifact gate citations stay trustworthy when `tasks.md` is edited.

## 6. Priority Roadmap

> The Target column carries the **repo-relative** form per the §0 path convention; every one of these targets is resolved to its absolute path in the matching §5 recommendation above. Rows are ordered by the sequencing §5 implies (a recommendation that another depends on comes first), then by severity.

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Emit the full required-flag set in compiled Wrap-up faces (land the 2026-10-15 backlog row) | `scripts/python/probe-utils.py` + `scripts/python/run-determination.py` + `scripts/python/feedback-utils.py`, then recompile all units | F4 |
| P1 | Make `/speckit.analyze` checklist-aware | `templates/commands/analyze.md` + `skills/internal/analyze-artifacts/SKILL.md` | F2 |
| P1 | Give checklist items an accountable answering stage + waiver closure format (lands 061 REC-C5/REC-C6) | `skills/internal/implement-feature/SKILL.md` lines 44–54 § Step 2 | F2, F3 |
| P1 | Declare the citation-group paren charset and honour it in the extractor | `shared/definitions/contract-clause-definitions.md` § 4 rule 2 + `scripts/python/clause_extract.py:125-140` | F1 |
| P1 | Wire the clause-coverage lane; freeze `coverage-baseline.txt` as a fifth baseline | `scripts/python/account-clause-coverage.py` + `templates/commands/analyze.md` + `skills/internal/create-tasks/SKILL.md` § Re-freeze timing | F1 |
| P1 | Name an owner in review's Handoffs and register every `REC-` id at coinage | `templates/commands/review.md:52` + `templates/instructions-template.md` § ID Register | F3 |
| P1 | Open a framework-scope intake for review recommendations | `shared/workflow/feedback-step.md:79-81` § Scope guard | F3 |
| P1 | Give `/speckit.review` a row in the feature status transition table | `shared/workflow/feature-integration.md` § transition table | F3 (post-validation addendum) |
| P1 | Add a structured evidence-record section, then an evidence-binding gate probe | `templates/verification-log-template.md` + `shared/definitions/probe-definitions.md` (new `gate-implement-evidence-binding`) | F6 |
| P1 | Mirror the baseline re-freeze duty onto the implement consumer side | `skills/internal/implement-feature/SKILL.md` (new pre-flight step) + `templates/commands/implement.md` | F7 |
| P2 | Open the single-landing-point carrier list; date-stamp degradation rows | `skills/internal/create-tasks/SKILL.md:202-206` item 2 + `templates/tasks-template.md:85` | F5 |
| P2 | Require red-first notes to quote the gate row they bind to | `skills/internal/implement-feature/SKILL.md` | F8 |
| P2 | Make REC targets repo-relative-first | `templates/review-template.md` § 5 + Replacement Rule 3 | F3 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`. — **Absolute throughout.** The URL form is deliberately not used: §0 records `Reachability of COMMIT_SHA` as `UNRESOLVABLE` (`git branch -r --contains HEAD` returns empty) and all three fork remotes are SSH, so no `/blob/` permalink written here would resolve. Recovery instruction for any cited byte: `git show e6696a0f9b5f5080722a8954ce5e78e68d715049:<relative-path>`. Two declared exceptions, both with absolute context present: (i) the repo-relative form in backticks that §0's path convention pairs with each absolute path — including the §6 Target column, whose rows are each resolved to an absolute path in the matching §5 recommendation and whose table carries a note saying so; (ii) relative paths inside fenced **verbatim quotations** of source text, which reproduce the source's own wording and must not be altered.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file. — F1..F8 each quote the offending text verbatim, with Chinese originals preserved un-translated. Where the defect is a contradiction between two texts, the finding quotes **both** sides: F1 (owner rule + extractor code + plan disclosure + 053 precedent), F2 (CHK005/CHK011 as authored + the analyze outcome + the checklist's own closing note + the waiver + 061's unlanded REC-C5/REC-C6), F3 (the ownerless handoff + the scope guard + 061's machine-local target path + 059's two finding titles), F5 (the stale row + the authoritative row + the correct sibling row + the carrier-list rule), F6 (the self-correction + the `test -e` gate + the template's actual section list + 059-F4), F7 (the producer-side duty + the invented reconciliation), F8 (the note's claim + GATE-7's actual definition + the independent SC-008 confirmation).
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document. — Every cross-reference names an absolute path plus a line number, commit SHA, or section heading.
- [x] No placeholder tokens remain anywhere in the report. — Machine-scanned. The bracketed literals that survive are: the markdown checkboxes in this section; the template's own §7 criterion wording reproduced verbatim in boxes 1 and 4 above (altering it would make the check unverifiable against the template); checklist item text quoted verbatim from source in F2 (`[覆盖/安全, Gap]`, `[术语/清晰性, Req §FR-013, §SC-003]`); and the finding-id notation `F[N]` where this section describes the template's convention rather than naming a finding. No unfilled token from the template's Placeholder Glossary appears anywhere.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in. — 10 bullets, one to three sentences each.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID. — **15** recommendations (3 Template, 2 Command Prompt, 4 Automation, 5 Workflow, 1 Documentation); each carries at least one framework-source target path with its line number or section heading, and a `Source:` field naming the finding. Every target is a framework source (`templates/`, `shared/`, `scripts/`, `skills/`) rather than a `.specify/` runtime copy, per the Two Hats rule.
- [x] P0 validation status is stated explicitly. — **The standard "vacuously satisfied" wording does NOT apply here, because P0 findings were raised and then downgraded.** Four candidates were rated P0 at detection and each was handed to an independent read-only validation subagent that received only the finding text — never the reasoning that produced it, never its siblings — per `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/review-sdd-process/SKILL.md` step 5 and `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md` rule 5. Result: **4 downgraded, 0 confirmed, 0 rejected — a 4/4 downgrade rate**, reported here as gate rule 6 requires. Per-finding validation notes:
  - **F1 → P1** `(validated: downgraded)`. The reviewer's original claim was that 13/29 was the owner-compliant total and 29/29 the favourable one. The validator re-applied the owner's last-paren-group rule with both ASCII and full-width delimiters over the same 35 clause blocks and obtained **29/29, missing none** (only FR-002, FR-013 and FR-028 occur outside any group, and all three also occur inside one). Root cause relocated from "wrong number published" to "undeclared charset axis + unwired lane"; 062's published figure is correct.
  - **F2 → P1** `(validated: downgraded)`. The reviewer's original claim (c) — that 061 had a settled checklist-closure procedure 062 failed to find — was one-sided. The validator surfaced that 061's own review F5 (P1) judged that same in-place refresh defective and prescribed append-only recheck files instead (REC-C5, unlanded), and that `/storage/project/cloud-native-ai/spec-kit/templates/commands/checklist.md` § Handoffs does route failures "Back to Plan / Back to Tasks". The finding was restated around **accountability** rather than absence of any consumer, and the "~17 minutes" figure was replaced with the commit-bounded "≤19 minutes" (no direct analyze timestamp exists).
  - **F3 → P1** `(validated: downgraded)`. The reviewer's P0 rating partly rested on Constitution Principle XIII. The validator read `/storage/project/cloud-native-ai/spec-kit/.specify/memory/constitution.md`: XIII "adds orientation, **not machinery**" and "MUST NOT be used to justify new scoring systems, maturity reports, **recording engines**" — it obliges no tracking artifact. The validator also downgraded one recurrence pair: 053's defect *did* publish wrong counts (190 vs 188/165) whereas 062's plan explicitly recorded "未产生虚假声明", so only the "deferred with no landing point" half of the pairing verifies.
  - **F5 → P2** `(validated: downgraded)`. The reviewer's normative anchor was mis-scoped. The validator established that `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` § Re-freeze timing governs the frozen `notes/` files and **task rows**, not § Notes prose; that all three cited mandates are conditional and were discharged by the authoritative § Environment Prerequisites (which the owner designates as the single landing point); that line 301 is a legitimate dated record; and that the cross-artifact drift check at `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` lines 211–214 **is** satisfied (`plan.md` and `requirements.md` carry zero stale copies). The claimed 059-F1 recurrence fails — 059's seven instances were *unqualified* stale assertions with corrections living only in `notes/`, a different shape. Reduced to the residual: line 281's superseded premise, undated heading, no cross-reference.
  - **F4, F6, F7, F8** were rated P1/P1/P1/P2 at detection and were not escalated to P0, so they did not enter the validation wave.
  - **Post-validation material, marked as such.** F3 carries one addendum (the missing `/speckit.review` row in the feature-status transition table) discovered while running this stage's own wrap-up, i.e. after the validation wave closed. It is labelled `Post-validation addendum (found after the validation wave; NOT independently validated)` in §3, and its recommendation in §5.4 and its §6 roadmap row both carry the same marker. It is evidence for an already-validated finding, not a new severity claim, and it does not change F3's rating.

  Reading the 4/4 rate honestly, per gate rule 6 ("*A downgrade rate near zero on a self-authored set is itself a signal worth reading*" — and its converse): this artifact set was authored by five prior dispatches, not by this reviewer, so the downgrades are not self-review leniency. All four shared one shape — **a normative anchor asserted from memory rather than read** (an owner rule's scope, a constitution principle's actual text, a prior feature's verdict on its own procedure). The corrective is a detection-side rule, not an artifact-side one: quote the governing text before assigning a severity, which is what §3 now does for every finding.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
