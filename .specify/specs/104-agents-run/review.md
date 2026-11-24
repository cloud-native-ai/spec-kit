# Specification-Driven Development (SDD) Process Review Report: /speckit.agents run（104-agents-run）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 104 |
| Requirement Key | 104-agents-run |
| Requirement Name | /speckit.agents run — 显式 run 子命令与 superagent/subagent 架构自动应用（Agents Run） |
| Related Feature | 019 Agents Command |
| Repository | spec-kit (`/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | SSH-only remotes: `gitee:cloud-native-ai/spec-kit.git`, `github:cloud-native-ai/spec-kit.git`, `gitlab:cloud-native-ai/spec-kit.git`; `origin` is the upstream `github:github/spec-kit.git`. No HTTPS web form is configured. |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (0 remotes contain the commit). Citations below use absolute paths plus `git show 8fb64953a:<path>` recovery instructions, never URLs. |
| Branch | `104-agents-run` |
| Commit SHA | `8fb64953a174f1713d96a4f5f2e1c14f2771a655` (short: `8fb64953a`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-24 |
| Reviewer (Agent) | Qoder agent (unattended SDD loop, review stage, attempt 1) |
| Environment | Linux x86_64 (5.10.134-15.2.al8), bash, CPython 3.11.11, pytest 8.4.2, parallel runner via `scripts/bash/run-tests.sh` |
| spec-kit Source Snapshot | same repository @ `8fb64953a` (`pyproject.toml` version `0.0.22`) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 280 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/requirements.md` | 24 FR / 7 SC / 8 shared strings; A-1…A-14, five user stories, three clarification sessions |
| plan.md | 159 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/plan.md` | 23-principle Constitution Check, Decision Tensions N/A, Project Structure, mirrors, execution premises, inherited blockers |
| tasks.md | 308 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/tasks.md` | 33 dependency-ordered rows, 35 `[green:]` claims, DoD / Completion Gate, measured premises |
| research.md | 42 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/research.md` | B-01…B-13 baseline measurements, R-01…R-10 decisions, U-01…U-03 resolved unknowns |
| data-model.md | 163 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/data-model.md` | E1–E9 projections, one attempt state machine, INV-01…INV-12 |
| contracts/agents-run-command.contract.md | 58 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/contracts/agents-run-command.contract.md` | C-01…C-10 (template + skill input + docs syntax) |
| contracts/agents-run-dispatch.contract.md | 54 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/contracts/agents-run-dispatch.contract.md` | C-11…C-22 (run-agent wiring; behavior-class labels) |
| contracts/agents-run-docs.contract.md | 72 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/contracts/agents-run-docs.contract.md` | C-23…C-35 (documentation same-source, closed stale-literal table) |
| quickstart.md | 94 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/quickstart.md` | S-0 executed; S-1…S-7 chat-instruction scenarios with per-example premises and pinning tests |
| feature-ref.md | 71 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/feature-ref.md` | Feature 019 binding basis, delivery surface, unit-registration verdict |
| checklists/requirements.md | 45 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/checklists/requirements.md` | requirements-stage quality checklist |
| checklists/run-command-2026-11-24.md | 83 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/checklists/run-command-2026-11-24.md` | 40 requirement-quality items across seven dimensions |
| verification.md | 97 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/verification.md` | smoke record, seven SC status rows with sha256-bound evidence, RS-008 joint acceptance |
| notes/red-first-evidence.md | 501 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/notes/red-first-evidence.md` | per-task red/green readings, guard and structural-audit transcripts |
| test-evidence/ | 32 files | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/test-evidence/` | stage E3 rows, baseline names, audit/drill readings, review run outputs |
| code-review.md | 455 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/code-review.md` | code segment record (fourth segment), coverage receipt, six-level notes |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements stage landed for `104-agents-run` | `ab17ea620` + `ac67a3927` + `0552904df`; 24 FR / 7 SC / 8 STR; `validate-requirements` 0/0 | None (stage-runner dispatch, sentinel `REQUIREMENTS-DONE`) |
| 2 | clarify bound Feature 019 without creating a Feature | `9c4007db3`; `.specify/features.md:28` row 019 note; requirements § Clarifications | None |
| 3 | plan attempt 1 produced every artifact but ended its turn while waiting for two internal audit subagents | `.specify/state/104-agents-run.md:80` — "子代理在「等待两个内部审计返回」时结束回合（一次性子进程无法恢复）→ 无哨兵、无提交、无 E3、无记账" | **Yes** — one-shot process ended without sentinel; full retry required |
| 4 | plan attempt 2 completed the same artifacts + same-author audit disposition | `d6a9f1cbb` (artifacts + FR-020 amendment) + `a02705a3c`; `pre-analyze --stage plan` pass | None (bounded completion retry) |
| 5 | requirements amended upstream before the fifth enumeration face was edited | `d6a9f1cbb`; FR-020 closed list + SC-005 parenthetical; `research.md` R-10 | None — the correction followed FR-020's own procedure |
| 6 | tasks landed and the clause-coverage baseline frozen | `021044e94` + `593063bca`; 33 rows / 35 claims; `account-clause-coverage` ok | None; two `PLAN-EDIT` citation-level touches declared (minor) |
| 7 | checklist landed before implement | `25818367f` + `0d5970a66` + `0412749af`; 40 items; E3 `not-run-docs-only` | None; stage correctly took no status transition |
| 8 | analyze Round 1 found 2 HIGH / 4 MEDIUM | `0412749af` tree; `.specify/specs/104-agents-run/test-evidence/analyze-report.md` | None — gate held before implement |
| 9 | analyze-repair fixed all six findings | `b6907ee53`; six `fixed` rows in the analyze report | None |
| 10 | analyze Round 2 (incremental) cleared with 0 open | report § Round 2; touched-loci + reused-domain hashes recorded | None |
| 11 | implement P1: baseline full suite (slot), template + skill wiring, US1 | `93ff582b6` + `2a0b27ec9`; baseline rc=1 / 222 failed names (spine seq=1) | None; planned mirror-ordering transient disclosed; `targeted-set-v1` selected 381 files and the package deviated to named sets (finding F1) |
| 12 | implement P2: package verifier failed one item, repaired, re-verified | `1e39ef9f4`; verifier fail → `01006ca5f` (team-parameter clause pinned) → 9 passed | None — independent verification worked as designed |
| 13 | implement P3: tutorials, routing scenario, US5 paths, regeneration, audits, mutation drill 4/4 | `8c39cdec0` + `00074fdb3`; `verification.md`; `test-evidence/mutation-drill.md` | None; evidence captured through bare `/tmp` sinks and one rc-masking pipe (finding F4) |
| 14 | implement close-out | `8fb64953a` (journal, observer instance, analyze/P2-repair evidence) | None |
| 15 | review (this run): four segments + ARC | smoke re-run rc 0 (10 passed); targeted nine-module set 216 passed / 3 baseline failures, `comm -13` empty; ARC `final_path` 2/2 pass, verdict `accept` | Status transition judged **allowed** (four conditions met) but landing intentionally not performed under this run's commit scope — see §2.4 disclosure and finding F7 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 2 |
| Automation / Scripts | 3 |
| Workflow | 2 |
| Documentation | 1 |

> The counts include the artifact segment's one P2 finding (F8). The code segment's six-level findings are its own family and are **not** counted here; they live in `code-review.md` and are summarized in §2.1 as the record's gate counts.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `e61df738af0513858414fee27ed9e6aa8092fdfe` | `git-delta-review.sh base --spec .specify/specs/104-agents-run` |
| Head commit | `8fb64953a174f1713d96a4f5f2e1c14f2771a655` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the base step's resolution tier |
| Renderer mode | `renderer: text` | record header marker |
| Changed / judged / skipped / gap files | 99 / 14 / 85 / 0 | copied from the record's coverage-receipt block, never recomputed |
| Segment verdict | `pass` | one of the four values the `code-review` skill owns |
| Gate verdict | `allow` | `report --summary --file .specify/specs/104-agents-run/code-review.md` exit 0 |
| Reason, when one applies | `none` | — |
| Uncommitted scope | Three pre-existing dirty files and eight pre-existing untracked runtime records were outside the review object (`.specify/skills/coaching-skills/SKILL.md`, `.specify/skills/coaching-skills/references/trainee-resolution.md`, `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`, plus `.specify/memory/{session,feedback,exec-quant}/…` entries); the receipt gives no conclusion over them. | the same sentence lives in `code-review.md` |
| Record | `.specify/specs/104-agents-run/code-review.md` | written because the triage value is `run` |
| Archive | `none` | first run |

Gate counts, copied from the record: blocking 0 · important 0 · suggestion 2 · nitpick 2 · question 0 · praise 1. The findings themselves are read in `code-review.md`; they are not repeated here.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `verification.md`, `contracts/agents-run-command.contract.md`, `contracts/agents-run-dispatch.contract.md`, `contracts/agents-run-docs.contract.md`, `checklists/requirements.md`, `checklists/run-command-2026-11-24.md`, `test-evidence/`, `notes/` | stage rules + `plan.md` § Project Structure (plan declares research / feature-ref / test-evidence; the stage rules add checklists / notes) |
| Coverage line | 15 / 15 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | — |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `docs/reference/commands/agents.md` | 9 | none | Residual no-argument generation paraphrase survives outside the C-34 closed predicate set — see F8. |

Dimensions walked: completeness (every member exists and carries its template's sections; no placeholder tokens), internal consistency (counts/literals/paths checked: 24 FR / 7 SC / 8 STR / 35 clauses / 33 task rows / 23 principles / 100 feature rows all match their carriers; evidence hashes recomputed — all six sampled sha256 values match `verification.md`), traceability (every FR reaches a task row; every SC reaches an existing evidence path; `comm -13` on the failed-name lists is empty), dependency and premise ownership (RS-001…RS-008 → EP-001…EP-003 verified; Inherited Blockers `none` with its basis), acceptance honesty (smoke record present and re-run; red-first records carry command + real output + rc; behavior-class clauses are not claimed as contract-covered).

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `e61df738af0513858414fee27ed9e6aa8092fdfe` | `git-delta-review.sh base --spec .specify/specs/104-agents-run` |
| Head commit | `8fb64953a174f1713d96a4f5f2e1c14f2771a655` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q --names-out .specify/specs/104-agents-run/test-evidence/smoke-failed.txt` | recorded verbatim in `verification.md`, re-run at the review head |
| Smoke exit code | 0 | 10 passed in 6.55s |
| Smoke evidence path | `.specify/specs/104-agents-run/test-evidence/review-smoke.txt` | exists and is non-empty |
| Scope and regression verdict | scope pass — the delta stays inside the declared closure (scope module 9/9 green; `flow-class-check` 92 units / 0 findings; mirrors and copies `--check` rc 0); regression pass — nine-module set 216 passed / 3 failed, all three are implement-entry baseline members (`test_fast_fail_discipline` g9 / i10 / x22), `comm -13 baseline review-failed` empty | `test-evidence/review-targeted.txt`, `review-failed.txt`, `baseline-failed.txt` |
| Segment verdict | `pass` | — |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| none | — | — | no finding | No implementation finding: correctness, scope and regression are all satisfied; the residual test-precision observations are the code segment's conclusions in `code-review.md` and are not restated as this segment's verdict. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/features/019-agents-command.md` and `.specify/features.md:28` (the two carriers agree) |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/104-agents-run --repo . --feature-detail .specify/features/019-agents-command.md --json` → `verdict: accept` |
| Comparison verdict | `agree` | `accept` agrees with the `Implemented` claim |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition judgement (checkpoint after all four segments).** The four conjunctive conditions of `Implemented → Ready for Review` all hold: (a) 0 deferred tasks (33 closed); (b) review evidence produced (`review.md` + `code-review.md`); (c) the current code record carries 0 `blocking` entries (`gate: allow`); (d) both `final`-path criteria are `pass` (SC-001, SC-002). Gate verdict: **allow**.

**Landing disclosure.** Under this run's dispatch commit scope ("only `review.md` and the E3 rows"), the status carriers were deliberately **not** written: `.specify/features.md` remains `Implemented`, `.specify/features/019-agents-command.md` remains `Implemented`, and its `## Latest Review` entry carries no review-stage record yet. The transition is judged and permitted; its landing (both carriers) is left to the driver/integration step that follows this record, exactly as the line's review stage did not claim a second deliverable. This is also reported as process finding F7.

## 3. Findings (Problems & Improvement Targets)

### F1 — `targeted-set-v1` over-selects on generic module stems, forcing an ad-hoc deviation

- **Severity**: P1
- **Category**: Automation
- **Location**: `skills/external/sdd-loop-driver/references/efficiency-model.md:112` (algorithm owner's carrier), with the in-run reading at `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/notes/red-first-evidence.md:150-159`
- **Evidence** (verbatim quote):

  ```
  - **(a) 改动路径覆盖**：候选 = `find <test_roots> -type f -name 'test_*.py' | LC_ALL=C sort`；对每个不在 `test_roots` 下的 `changed_path`，选中内容包含该仓库相对路径或其模块 stem（basename 去扩展名）的候选文件（`grep -lF` 固定字符串）。
  ```

  ```
  Note on `targeted-set-v1` sufficiency: the literal algorithm (module stem `SKILL` and short
  name `agents-run`) selects 381 test files, i.e. nearly the whole contract/integration surface,
  which would collide with the one-full-suite budget.
  ```

- **Why it's a problem**: every skill edit presents the baseline stem `SKILL`, which matches hundreds of unrelated test modules; the stage must then either blow the one-full-suite budget or silently substitute a hand-picked set. This line chose the substitution and recorded it, but the deviation has no reason code or machine-checkable shape, so the next runner may choose differently.
- **Proposed fix**: in `skills/external/sdd-loop-driver/references/efficiency-model.md` § 2.3 (a), exclude a closed set of generic stems (`SKILL`, `README`, `index`, `__init__`) from stem matching and require the full repository-relative path for those subjects; add a named deviation code (e.g. `selection-over-budget`) whose row shape the stage must record, so a substitute set is auditable rather than ad hoc.

### F2 — `audit-plan-changes.py` matches basenames in both the pathspec and the declaration check

- **Severity**: P1
- **Category**: Automation
- **Location**: `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py:63-65` and `:103-107`; the false positive it produced at `/storage/project/cloud-native-ai/spec-kit/.specify/state/104-agents-run.md:213`
- **Evidence** (verbatim quote):

  ```
              specs.append(":(glob)**/%s" % name)
              specs.append(":(glob)**/%s/**" % name)
  ```

  ```
  def covered(path, declarations):
      basename = path.rsplit("/", 1)[-1]
      for line in declarations:
          if path in line or basename in line:
              return True
  ```

  ```
  - plan audit（b6907ee53..HEAD）：唯一命中 `docs/tutorials/quickstart.md`（交付面文档，与 plan-owned `quickstart.md` basename 碰撞的误报）；实际 plan-owned 六类零改动 → 语义分类 = none（披露）
  ```

- **Why it's a problem**: a plan-owned basename such as `quickstart.md` matches every same-named file in the repository, so the audit reports product-doc edits as plan-owned touches. The same basename tolerance in `covered()` runs the other way: a declaration line that mentions `quickstart.md` can mark an unrelated `docs/tutorials/quickstart.md` as covered, so an undeclared plan edit could escape the `undeclared` verdict. The audit's answer is unreliable in both directions.
- **Proposed fix**: resolve plan-owned name-only entries against the spec directory (`:(glob)<spec-dir>/**/<name>`), never repository-wide, and make `covered()` match full repository-relative paths only. Add a fixture to the script's tests with a same-basename file outside the spec directory.

### F3 — the stage prompt skeleton lacks a permanent one-shot process clause

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `.specify/state/104-agents-run.md:80` and `:97` (the in-run observation); the owner surface is the driver's stage-prompt skeleton (`skills/external/sdd-loop-driver/references/stage-prompts.md`)
- **Evidence** (verbatim quote):

  ```
  - watcher verdict: INCOMPLETE（exit 15；status exit=0 sentinel=0）；子代理在「等待两个内部审计返回」时结束回合（一次性子进程无法恢复）→ 无哨兵、无提交、无 E3、无记账
  ```

  ```
  - framework_observation: stage prompts MUST 显式声明「你是一次性进程，不得以等待结束回合」；stage-runner 重试前不清理上一轮 status（须由驱动归档）
  ```

- **Why it's a problem**: a stage dispatch is a one-shot process. Ending the turn to wait for anything (a subagent return, a slow command, an approval) destroys the executor, the sentinel never appears, and an entire stage dispatch is wasted. This run paid for a full plan retry; the correction landed only because the driver wrote the clause into later dispatch prompts by hand.
- **Proposed fix**: make the one-shot clause a permanent, single-owner block in `skills/external/sdd-loop-driver/references/stage-prompts.md` (copied into every stage prompt, not improvised per dispatch), and state in the same block that the driver archives the previous attempt's status before a retry. This run's prompt already carries it — the finding is that the carrier, not the dispatcher, must own it.

### F4 — evidence captured into bare `/tmp`, and one run masked its exit code behind a pipe

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/104-agents-run/notes/red-first-evidence.md:191` (and the T015 / T016 / T017–T020 / Package-2 / T021–T023 / T024–T026 entries); the rc-masking note is in `.specify/specs/104-agents-run/test-evidence/implement.jsonl` (T012 row)
- **Evidence** (verbatim quote):

  ```
  $ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_skill_wiring.py -q > /tmp/p2-us2-run.txt 2>&1; rc=$?
  ```

  ```
  A first invocation piped its output through tail and masked rc; the reported rc was re-captured directly on a second invocation (same selection, same result).
  ```

- **Why it's a problem**: `AGENTS.md` § Temporary Directory Discipline forbids bare system temp for agent-created scratch, and Single-Run Evidence Discipline requires the run's complete output to be persisted at execution time. `/tmp` is outside the repository, unversioned, and survives by accident; the decisive text only survived because the implementer later pasted it into `notes/`. The same run also lost one exit code to a `| tail` pipeline — a masked rc is precisely the "green check that proves nothing" shape.
- **Proposed fix**: name the sanctioned capture root in the implement skill's test-run section (`skills/internal/implement-feature/SKILL.md` § Test runs): capture into `<spec-dir>/test-evidence/` directly, or into `.specify/.tmp/` when transient, and forbid piping the runner's output (`| tail`, `| head`, `| tee` without `PIPESTATUS`) when the rc is being recorded.

### F5 — an integration test rewrites a committed evidence file, dirtying every full-suite run

- **Severity**: P2
- **Category**: Automation
- **Location**: `tests/integration/test_acceptance_smoke.py:27` and `:219`
- **Evidence** (verbatim quote):

  ```
  ``.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt``. It is written **before** the
  assertions, so a failing sub-check is still recorded rather than leaving the previous run's green
  evidence in place — an evidence file that only exists when the run passed proves nothing.
  ```

  Working-tree reading at review time (`git diff .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`):

  ```
  -  generated: .specify/.gitignore, .specify/agents, .specify/constitution.md, …
  +  generated: <none>
  ```

- **Why it's a problem**: the test intentionally writes into a sealed feature's committed evidence file, so every full-suite run leaves a dirty tree. The next close-out must remember to exclude it, and any broad `git add` would commit a mutated historical evidence record. The write is by design for 081's determinism, so the defect is placement, not intent.
- **Proposed fix**: write to `tmp_path` and reproduce the committed file only through an explicit regeneration path (or add the generated evidence file to `.gitignore` with a committed template of its expected shape). Keep the "written before the assertions" property — only move the sink.

### F6 — plan and tasks stages emitted no close-out receipt

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/state/104-agents-run.md:132`; owner surface `shared/workflow/artifact-commit-step.md` § Close-out
- **Evidence** (verbatim quote):

  ```
  - 上游偏差（子代理记录）：plan / tasks 阶段缺 close-out receipt（artifact-commit-step 每运行一份）——如实记录，未代补
  ```

- **Why it's a problem**: the per-run close-out receipt is the accounting unit for run-level traceability and retention. Two stages committed artifacts and E3 rows without it, leaving a hole the next stage had to report rather than repair. Nothing in the stage prompts requires the receipt, so the omission is silent by construction.
- **Proposed fix**: add the close-out receipt to the stage prompt's wrap-up checklist (both the plan and tasks blocks) and have U4 verify its presence as a completion condition; a missing receipt then fails the stage instead of being disclosed downstream.

### F7 — the review stage prompt's commit scope is narrower than the composed command's deliverables

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `templates/commands/review.md:139` (deliverable carriers) and the review stage prompt block in `skills/external/sdd-loop-driver/references/stage-prompts.md` (which carries only the test-budget block, no deliverable list). The dispatch instruction itself is external to the repository: `review stage dispatch 2026-11-24T07:53Z`, verbatim "评审不自动修复制品；只提交 review.md 与 E3 行".
- **Evidence** (verbatim quote):

  ```
  **Where the conclusions land.** Both segment conclusions appear on two verifiable carriers: the report's code subsection (`### 2.1`) and the bound feature detail's existing `## Latest Review` review-record entry.
  ```

- **Why it's a problem**: `/speckit.review` writes two records (`review.md`, `code-review.md`), lands the transition on two carriers, and requires the feature detail's `## Latest Review` entry; the stage prompt constrains commits to `review.md` + E3. A compliant runner leaves the code record untracked and the carriers stale, or over-commits. This run took the first path by design — the record is complete and the landing is disclosed — but the mismatch forces every unattended review to improvise and leaves the second carrier unfilled until the driver acts.
- **Proposed fix**: give the review stage prompt an explicit deliverable block listing `review.md`, `code-review.md`, the E3 rows, and stating **who lands the status transition and the feature-detail `Latest Review` entry** (recommended: the driver, immediately after U4). Until then the command and the prompt will keep disagreeing.

### F8 — a residual no-argument generation paraphrase survives outside the closed stale-literal set

- **Severity**: P2
- **Category**: Documentation
- **Location**: `docs/reference/commands/agents.md:9`; the predicate gap is visible at `.specify/specs/104-agents-run/contracts/agents-run-docs.contract.md:63`
- **Evidence** (verbatim quote):

  ```
  - After `specify init` to generate project-aware role-based agents
  ```

  ```
  | case-insensitive `generate role-based agents` | commands ref, quickstart, installation | 0 |
  ```

- **Why it's a problem**: the same document now states, under `## Default Behavior (No Arguments)`, that with empty arguments the command lists agents and suggestions — and that it "creates, refines, or runs no agent without an explicit user instruction". The `When to Use` bullet still tells the reader to run the command to "generate project-aware role-based agents"; the C-34 predicate misses it because `project-aware` is inserted between `generate` and `role-based agents`. The closed set is honest about its members, but the drift class survives in a variant the set cannot see.
- **Proposed fix**: reword the bullet to match the current mode set (e.g. "after `specify init` to list the project-aware role-based agents, or create / refine / run one"), and add the `generate project-aware role-based agents` variant to the C-34 table so the next same-class edit is caught rather than reviewed by eye.

## 4. What Worked — Preserve (Brief)

- Four segments delegated by path with separate vocabularies; no segment answered another's question, and the code family stayed unconverted.
- Behavior-class vs artifact-class split (FR-023) stated in contracts, tests' docstrings, and a guard that scans the new modules for coverage overclaims.
- Red-first evidence records carry the command, the real red output and the exit code, with the authoring defects disclosed rather than hidden.
- Independent verification: the P2 verifier failed a genuinely unpinned clause, the repair was minimal, and the re-verification passed — the fail was useful, not noise.
- Mutation drill 4/4 with exact reverse-restore and an empty `git diff` after each restore.
- Evidence honesty: all six sampled `evidence_sha256` values recomputed identical, and the smoke re-ran green at the review head.
- Mirrors and per-tool copies regenerated, never hand-edited; `sync-mirrors --check` and `regen-command-copies --check` both rc 0 at the review head.
- Same-author gate respected: stage sessions were disjoint, and the plan stage delegated its two self-audits to fresh-context readers.

## 5. spec-kit / SDD Improvement Recommendations

> No `REC-…` identifier is coined by this report: each recommendation is carried by its target path and source finding IDs, so `.specify/register.md` owes no new durable id from this run (the same convention the 103 review used). Remediation is a follow-up run's work; this review does not modify the sources.

### 5.2 Command Prompt Improvements

- **Codify the one-shot clause in the stage-prompt skeleton** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md`. Change: add a permanent "one-shot process" block (never end the turn to wait; emit the sentinel before returning) and a retry clause that archives the previous attempt's status. Source: F3. Expected impact: plan-stage dispatch waste disappears; retries stop re-litigating stale status.
- **Give the review stage an explicit deliverable block** — Target: `skills/external/sdd-loop-driver/references/stage-prompts.md`. Change: list `review.md`, `code-review.md`, the E3 rows, and name the landing owner for the status transition and the feature-detail `## Latest Review` entry. Source: F7. Expected impact: unattended reviews stop improvising their commit scope and the second carrier is filled deterministically.

### 5.3 Automation / Script Improvements

- **Make `targeted-set-v1` stem matching safe** — Target: `skills/external/sdd-loop-driver/references/efficiency-model.md` § 2.3. Change: exclude generic stems (`SKILL`, `README`, `index`, `__init__`) from stem matching; require the full repository-relative path; add a `selection-over-budget` deviation row shape. Source: F1. Expected impact: skill edits no longer expand the targeted set to ~400 files, and deviations become auditable.
- **Scope the plan-change audit to the spec directory** — Target: `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`. Change: prefix name-only pathspecs with the spec directory and match declarations by full path. Source: F2. Expected impact: no more same-basename false positives, and no declaration can cover an unrelated path.
- **Move the 081 smoke evidence sink out of the committed tree** — Target: `tests/integration/test_acceptance_smoke.py`. Change: write to `tmp_path`; regenerate the committed evidence only through an explicit path (or ignore the generated file). Source: F5. Expected impact: full-suite runs stop dirtying a sealed feature's evidence and close-out stops needing a manual exclusion.

### 5.4 Workflow Improvements

- **Pin the evidence-capture rules in the implement skill** — Target: `skills/internal/implement-feature/SKILL.md` § Test runs. Change: name the sanctioned capture root (`<spec-dir>/test-evidence/` or `.specify/.tmp/`) and forbid piping the runner when the rc is recorded. Source: F4. Expected impact: evidence survives the run, and a masked rc can no longer be reported as a verdict.
- **Require the close-out receipt at U4** — Target: `shared/workflow/artifact-commit-step.md` § Close-out (and the plan/tasks stage-prompt wrap-up blocks). Change: state that the receipt is verified at stage completion, not merely expected. Source: F6. Expected impact: no stage closes without its per-run accounting unit.

### 5.5 Documentation Improvements

- **Close the residual no-argument paraphrase** — Target: `docs/reference/commands/agents.md`. Change: reword the `When to Use` bullet at line 9 to the list / create / refine / run surface, and extend the C-34 predicate table with the measured variant. Source: F8. Expected impact: the closed set stops being blind to the inserted-adjective variant, and the page stops contradicting its own Default Behavior section.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Make `targeted-set-v1` stem matching safe | `skills/external/sdd-loop-driver/references/efficiency-model.md` § 2.3 | F1 |
| P1 | Scope the plan-change audit to the spec directory | `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py` | F2 |
| P1 | Codify the one-shot clause in the stage-prompt skeleton | `skills/external/sdd-loop-driver/references/stage-prompts.md` | F3 |
| P1 | Pin the evidence-capture rules in the implement skill | `skills/internal/implement-feature/SKILL.md` § Test runs | F4 |
| P2 | Move the 081 smoke evidence sink out of the committed tree | `tests/integration/test_acceptance_smoke.py` | F5 |
| P2 | Require the close-out receipt at U4 | `shared/workflow/artifact-commit-step.md` § Close-out | F6 |
| P2 | Give the review stage an explicit deliverable block | `skills/external/sdd-loop-driver/references/stage-prompts.md` | F7 |
| P2 | Close the residual no-argument paraphrase | `docs/reference/commands/agents.md` | F8 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary); the one target with no repo-relative form (the review dispatch instruction) is marked `external` with its reason in F7. No `REC-…` id was coined, so no register entry is owed by this report — repo-relative target paths replace them.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.** All findings are P1/P2, so no independent validator wave was required (and the same-author gate did not fire: the reviewed artifacts were produced by separate stage sessions, not this one).

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

