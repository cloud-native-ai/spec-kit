# Tasks: Humanize Command（人性化改写命令）

**Requirement ID**: 062 (from branch `062-humanize-command`)
**Requirement Key**: `062-humanize-command`
**Related Feature**: Feature 062 Humanize Command（人性化改写命令） (from `.specify/memory/features.md`)
**Input**: Design documents from `.specify/specs/062-humanize-command/` — plan.md, requirements.md, data-model.md, contracts/ ×3, quickstart.md, feature-ref.md, notes/ ×6
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md, feature-ref.md, notes/ frozen baselines

**Tests Mode**: ON — Constitution Principle IV “Test-First & Contract-Driven Implementation” is test-mandating; this feature is template-only (Markdown command/skill/docs artifacts), so per Principle VII’s template-only gate the automated layer is **structural contract tests** (`tests/contract/test_humanize_command_surface.py` + two downstream pinning tests) and the behavioral layer is the E8 evaluation protocol (fixed corpus + `rubric.md` + two independent reviewers + deterministic protected-content diff script), not unit/integration tests against a runtime.

**Tests**: Structural contract tests are MANDATORY and red-first (the asserted paths/literals do not exist yet). Behavioral criteria are carried by the E8 protocol and recorded in `verification.md`; no runtime unit tests are applicable because the feature ships no executable runtime.

**Organization**: Tasks are grouped by user story. This is a **doc-feature** (deliverables are command template, skill body, docs page, registry rows, generated copies, mirrors, fixtures), so the within-story order follows **author-section → mirror-parity → render-verify → refresh-verify** rather than Models → Services → Endpoints. US1 establishes the shared command template and skill core; US2–US3 extend the same skill file, so their phases are serialized by `[blockedBy:]` even though each story has an independent checkpoint.

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]` (or `[~]` with a recorded deferral reason); zero `[ ]` / `[>]` rows remain.
- DoD-2: All 17 deliverables in `feature-ref.md` exist at their canonical paths and are listed with evidence in `verification.md`.
- DoD-3: All 34 contract clauses C-1..C-34 are claimed exactly once by a `[green:]` row, and every claimed check passes.
- DoD-4: `tests/contract/test_humanize_command_surface.py`, `tests/contract/test_feedback_command_classification.py`, and `tests/contract/test_skill_layer_visibility_guards.py` are green.
- DoD-5: The E8 evaluation record covers ≥8 samples, two independent review sheets, and deterministic diff results (invariant changes 0, fabrications 0); `verification.md` carries the records.
- DoD-6: Generation face has zero NEW drift vs `notes/baseline-regen-check.txt`; the two touched mirror pairs are byte-identical after feature-scoped sync; `skill:humanize` is registered and compiled with the current fingerprint with zero NEW drift attribution against `notes/baseline-compile-check.txt`.
- DoD-7: Name-level test comparison shows zero NEW failures vs `notes/baseline-failed-tests.txt`; the `cws-lib-bash` environment caveat in § Environment Prerequisites is applied honestly (no green claim while the dependency is unavailable).
- DoD-8: `verification.md` lists SC-001..SC-010 with status and evidence paths; no new external service, network call, model API, third-party dependency, or background daemon exists.

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW test failures by name — check: use the canonical runner and name-level comparison owned by `.specify/skills/internal/implement-feature/SKILL.md` § Test runs; current names `comm -13 .specify/specs/062-humanize-command/notes/baseline-failed-tests.txt <current>` MUST be empty. MUST run with `CWS_LIB_BASH_HOME` resolvable (see § Environment Prerequisites); otherwise record a blocked/degraded verdict, never a green one.
- GATE-2: Per-tool copies clean — check: `python3 scripts/python/regen-command-copies.py --check` reports zero NEW drift vs `notes/baseline-regen-check.txt` and the four `speckit.humanize.*` copies exist with the generated warning header.
- GATE-3: Touched mirrors byte-identical — check: `diff -q skills/external/humanize/SKILL.md .specify/skills/humanize/SKILL.md` and `diff -q shared/definitions/probe-definitions.md .specify/shared/definitions/probe-definitions.md` both exit 0; `python3 scripts/python/sync-mirrors.py --check | grep -E 'humanize|probe-definitions'` yields no touched-pair DIFF.
- GATE-4: Compile face — check: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` does not list `skill:humanize`, and the drift-unit set has zero NEW attribution vs `notes/baseline-compile-check.txt`.
- GATE-5: Contract tests green — check: `python3 -m pytest tests/contract/test_humanize_command_surface.py tests/contract/test_feedback_command_classification.py tests/contract/test_skill_layer_visibility_guards.py -q` exits 0.
- GATE-6: No open/claimed rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/062-humanize-command/tasks.md` returns 0 (deferred `[~]` rows, if any, are listed in `verification.md`).
- GATE-7: Structural validity — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/062-humanize-command/tasks.md` exits 0 with 34 green claims and no collision; `python3 .specify/scripts/python/validate-requirements.py .specify/specs/062-humanize-command/requirements.md` exits 0.
- GATE-8: 17 deliverables present — check: verify each path from `feature-ref.md` § 交付面清单 with `test -e`; report any missing path as a gate failure.

## Environment Prerequisites

- `cws-lib-bash` (`CWS_LIB_BASH_HOME`): **unavailable** — probe: `bash scripts/bash/run-tests.sh --names-out /tmp/humanize-tasks-current-failed.txt` @ 2026-10-19 → `94 failed, 3906 passed`; all 23 names added over the frozen 71-name baseline are in the `cws-lib-bash`-dependent cluster, e.g. `Error: cws-lib-bash is not correctly installed. File not found: /storage/project/cloud-native-tools/cws-lib-bash/bin/cws_bash_env` from `scripts/bash/common.sh`’s dependency check. Affected phases/tasks: US4 C-9 row (T026), GATE-1. While unavailable, T026/GATE-1 MUST report the comparison as blocked/degraded rather than claim zero-new-failures.
- Python / pytest: **available** — probe: `python3 --version` → `Python 3.11.11`; `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-19; affected: all automated checks.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different write targets, no incomplete dependency).
- **[Story]**: `[US1]`..`[US4]` only inside User Story phases; Setup / Foundational / Polish rows carry no story label.
- **[blockedBy: Txxx,Tyyy]**: explicit dependency; the task MUST NOT start until every listed row is `[X]`.
- **[green: <contract>#<clause>]**: the row is the one that turns that contract clause green. A row may declare several. Each clause is claimed exactly once; never delete a tag to silence a warning.
- One line per task, including paths and tags; use repository-relative paths.

### Task State Sigil (REQUIRED)

- `- [ ]` open; `- [>]` claimed/in-progress; `- [X]` closed; `- [~]` deferred with a recorded reason.

## Path Conventions

- Framework source: `templates/`, `skills/`, `shared/`, `docs/`, `tests/`.
- Runtime mirrors: `.specify/skills/`, `.specify/shared/`.
- Feature evidence: `.specify/specs/062-humanize-command/` (`notes/`, `verification.md`).
- `templates/commands/` has **no** `.specify/templates/commands/` mirror (retired); per-tool copies are the distribution face.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze the pre-change side of every diff premise and record the environment verdict before any artifact is written.

- [ ] T001 捕获改前侧证据到 `.specify/specs/062-humanize-command/notes/pre-change-measurements.md`：逐项实跑并粘贴命令/日期/真实输出——`python3 scripts/python/regen-command-copies.py --check`、`python3 scripts/python/sync-mirrors.py --check`、`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check`、并按 `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 的规范 runner 采集名字级失败名单；环境判据按本文件 § Environment Prerequisites 记录，不在此复述。

**Checkpoint**: pre-change measurements exist; every later `diff against pre-change` premise has a dated baseline.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Author the red structural test and the E8 evaluation assets that every story verification depends on.

**⚠️ CRITICAL**: No user story verification can close until this phase is complete.

- [ ] T002 [P] Author 结构契约测试 `tests/contract/test_humanize_command_surface.py`（`test_c01`..`test_c10` 逐条覆盖 C-1..C-10：薄模板/无 `## Wrap-up`/唯一技能委派/技能 frontmatter 与自足/四副本/docs 内容/注册行/probe 行与编译面/无新增运行时/检测器诚实措辞），在当前树先红，并把命令、真实红输出与退出码记入 `.specify/specs/062-humanize-command/notes/red-first-evidence.md`。
- [ ] T003 [P] Author E8 评估语料 `tests/fixtures/humanize/`：≥8 个样本覆盖中文/英文/混合语言、内联/文件、受保护内容、矛盾陈述、已自然文本、长多章节文档与非法输入；在 `tests/fixtures/humanize/README.md` 记录 sample-id → 用途 → SC/条款对照清单。
- [ ] T004 [P] Author `tests/fixtures/humanize/rubric.md`：四维度各自通过判据、“适用维度失败即样本失败”规则、缺省 `professional` 判据，以及两位独立评审的独立记录表单。
- [ ] T005 [P] Author 确定性受保护内容差异脚本 `tests/fixtures/humanize/diff_protected.py`：逐项比对 invariant set 与 protected set、输出逐项结论与 0/1 退出码、仅用标准库且无 LLM 调用；用 `tests/fixtures/humanize/selftest/` 的最小样本对实跑并记录输出。

**Checkpoint**: the structural test is red for the expected reason; corpus, rubric, and diff script are ready.

---

## Phase 3: User Story 1 - 内联内容的人性化改写 (Priority: P1) 🎯 MVP

**Goal**: `/speckit.humanize` accepts inline text/conclusion/report and applies all four rewrite dimensions while preserving facts, numbers, conclusions, citations, and protected content; default tone is professional and output language follows the input.

**Independent Test**: Run the fixed bilingual inline fixtures directly, score the four dimensions with the rubric, and diff every protected item with the deterministic script.

### Implementation for User Story 1

- [ ] T006 [P] [US1] Author 薄命令模板 `templates/commands/humanize.md`（C-1/C-2）：frontmatter 含 `description`（触发词列表）与 `short-description`，无 `scripts:` 块；正文含 `## User Input`（`$ARGUMENTS` 接线 + User Input Protocol 引用 + 输入形态声明）、`## Glossary`、Delegation 节指向 `.specify/skills/humanize/SKILL.md`、`## Handoffs`；无 `## Wrap-up`，以 [[STR-001]] 标识命令身份，正文不复述四维度工作流。
- [ ] T007 [US1] Author `skills/external/humanize/SKILL.md` 核心执行流：frontmatter（`name: humanize`、`description` 触发词、`classification: external`、`skill_id: <SKILL:.specify/skills/humanize/SKILL.md>`）；四维度完整工作流且无跳过分支（C-11..C-15）；保真/受保护内容/最小改动/矛盾保留（C-16..C-19）；内联输入与空内容拒收；缺省 `professional` 语气；完整改写文本为主输出且语言跟随输入（C-21/C-22 的实现面）；检测器诚实措辞。

### Verification for User Story 1

- [ ] T008 [US1] [blockedBy: T006,T007] 执行 E8 内联样本（中文/英文/单句/受保护内容/矛盾/已自然）并逐例记录输入、输出与量规判定到 `.specify/specs/062-humanize-command/verification.md`；受保护内容 per `tests/fixtures/humanize/diff_protected.py` 逐项比对；认领 C-11..C-19。 [green: contracts/rewrite-behavior.md#C-11] [green: contracts/rewrite-behavior.md#C-12] [green: contracts/rewrite-behavior.md#C-13] [green: contracts/rewrite-behavior.md#C-14] [green: contracts/rewrite-behavior.md#C-15] [green: contracts/rewrite-behavior.md#C-16] [green: contracts/rewrite-behavior.md#C-17] [green: contracts/rewrite-behavior.md#C-18] [green: contracts/rewrite-behavior.md#C-19]
- [ ] T009 [US1] [blockedBy: T008] 由两位 fresh-context 只读评审 per `tests/fixtures/humanize/rubric.md` 独立评分 US1 内联样本（适用维度失败即样本失败）；两份评分表与修复复跑结论记入 `verification.md`；任一失败先修技能并重跑 T008 后再关闭本行。

**Checkpoint**: US1 is independently functional: inline rewriting meets the four dimensions and fidelity on the fixed corpus; default tone and language behavior are verified.

---

## Phase 4: User Story 2 - 外部文档的安全改写 (Priority: P1)

**Goal**: Accept one Markdown or plain-text file, rewrite the full document without modifying the source by default, write only to an explicit output path, require explicit overwrite confirmation, reject unsupported/invalid inputs, and cover long multi-chapter documents without silent truncation.

**Independent Test**: In a temp directory, exercise Markdown/plain-text/frontmatter/long/invalid fixtures; compare source and existing targets byte-for-byte and inspect write/refusal/error branches.

### Implementation for User Story 2

- [ ] T010 [US2] [blockedBy: T009] 扩展 `skills/external/humanize/SKILL.md` 的文件输入/输出行为：支持格式 [[STR-003]]、路径解析与拒收分支、二进制/空文件拒收、frontmatter 逐字保留、输出格式跟随输入、默认零写入、显式输出路径/覆盖确认/写入失败报告、长文档章节完整性与重组（C-17/C-20/C-28..C-34 的实现面）。
- [ ] T011 [P] [US2] [blockedBy: T003] 在 `tests/fixtures/humanize/files/` 增加文件行为夹具：带 frontmatter 的 Markdown、纯文本、长多章节文档、空文件、二进制替身、目录路径、已存在输出目标、不可写输出路径；在 `tests/fixtures/humanize/files/README.md` 记录夹具清单与覆盖条款。
- [ ] T012 [P] [US2] [blockedBy: T004] 扩展 `tests/fixtures/humanize/rubric.md` 的文件安全协议：运行前后逐字节哈希、目录快照、覆盖确认分支、写入失败分支、长文档章节对应表。

### Verification for User Story 2

- [ ] T013 [US2] [blockedBy: T010,T011,T012] 在临时目录执行全部文件行为场景（源文件逐字节不变、零隐式创建、覆盖拒绝/确认、显式写入成功、错误分支、frontmatter/格式、长文档完整性），结果记入 `.specify/specs/062-humanize-command/verification.md`；协议 per `tests/fixtures/humanize/rubric.md`，受保护内容 per `tests/fixtures/humanize/diff_protected.py`；认领 C-20。 [green: contracts/rewrite-behavior.md#C-20]

**Checkpoint**: US2 is independently functional: source files are never modified implicitly; write/overwrite/refusal/error branches are verified; long documents are complete. The file-safety clauses C-28..C-34 are implemented here and formally closed by the final cross-cutting row T030 (see § Notes → Clause partition).

---

## Phase 5: User Story 3 - 语气与受众控制 (Priority: P2)

**Goal**: Support `professional`, `humorous`, `empathetic`, `colloquial`, and free-text audience descriptions; tone/audience affect only the expression layer and never override fidelity; unsupported tone values are rejected with the supported set.

**Independent Test**: Run the same fixture under the four tones and the default; two independent reviewers judge distinguishability and appropriateness, and protected content is diffed item by item.

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T013] 扩展 `skills/external/humanize/SKILL.md` 的语气/受众面：封闭集合 [[STR-002]]、缺省 `professional`、自由文本受众、仅作用表达层、集合外取值拒收并列出支持集合、语气与保真冲突时保真优先并报告限制（C-24..C-27 的实现面）。
- [ ] T015 [P] [US3] [blockedBy: T003] 在 `tests/fixtures/humanize/tone/` 增加语气矩阵：同一基样本 ×4 语气 + 缺省、集合外取值、语气-保真冲突；并落 `tests/fixtures/humanize/tone/rubric.md`（可区分性/得体性判据 + 两位独立评审记录表单）。

### Verification for User Story 3

- [ ] T016 [US3] [blockedBy: T014,T015] 执行语气矩阵并由两位 fresh-context 只读评审独立判定（四语气 + 缺省可区分且得体、事实/结论零改变、集合外取值被拒且不声称已应用）；两份评分表与结论记入 `.specify/specs/062-humanize-command/verification.md`；判定 per `tests/fixtures/humanize/tone/rubric.md`；认领 C-24..C-27。 [green: contracts/tone-input-file.md#C-24] [green: contracts/tone-input-file.md#C-25] [green: contracts/tone-input-file.md#C-26] [green: contracts/tone-input-file.md#C-27]

**Checkpoint**: US3 is independently functional: all four tones and the default are distinguishable and appropriate, with fidelity intact.

---

## Phase 6: User Story 4 - 框架集成、分发与可发现性 (Priority: P2)

**Goal**: Ship the command through the template source, four per-tool generated copies, one external execution skill plus its mirror, a docs page, the classification registry row, the probe/compile face, the feature registry, and the structural/pinning tests, with zero new runtime surface.

**Independent Test**: Inspect the template, generated copies, docs page, registry rows, and skill delegation; run generation/mirror/compile checks and compare the test failure-name set to the frozen baseline.

### Implementation for User Story 4

- [ ] T017 [P] [US4] [blockedBy: T006] 在 `.specify/specs/027-feedback-mechanism/contracts/command-classification.md` 新增 `humanize` 的 **Simple** 行（(a)(b)(c) 均不命中）；同步把分类表标题 26→27、首段陈旧计数 25→27、**Result** 行 23 complex/3 simple→23/4。
- [ ] T018 [P] [US4] [blockedBy: T007] 在 `shared/definitions/probe-definitions.md` 新增 `skill-humanize-wrapup | skill-wrapup | skill:humanize | wrap-up` 对象行（external 技能块）与 `h-docs-sync-eval @point:wrap-up` 绑定行；源侧限定，镜像留给 T021。
- [ ] T019 [US4] [blockedBy: T018] 运行 `python3 .specify/scripts/python/probe-utils.py --action compile-embeds` 生成/刷新 `skills/external/humanize/SKILL.md` 的 `## Wrap-up` 编译面；确认 `skill:humanize` 单元落位且带当前指纹、绑定行长出的步骤与 C-7 一致；若引擎不能为新技能创建该节，先补骨架再重跑，仍失败则以异常行上抛，不得删绑定行。
- [ ] T020 [P] [US4] [blockedBy: T006] 运行 `python3 scripts/python/regen-command-copies.py` 生成四个副本 `.claude/commands/speckit.humanize.md`、`.github/prompts/speckit.humanize.prompt.md`、`.opencode/command/speckit.humanize.md`、`.qoder/commands/speckit.humanize.md`；确认生成头存在、无手改，并以 `--check` 对照 `notes/baseline-regen-check.txt` 判零 NEW drift。
- [ ] T021 [US4] [blockedBy: T019] 运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/humanize --only shared/definitions/probe-definitions.md` 落位 `.specify/skills/humanize/SKILL.md` 与 `.specify/shared/definitions/probe-definitions.md`；确认两个触碰对字节一致且未拖入其他对。
- [ ] T022 [P] [US4] [blockedBy: T007] Author `docs/reference/commands/humanize.md`（C-5）：输入形态（内联/文件）、默认不写文件、支持语气集以 [[STR-002]] 引用、保真边界、不承诺 AI 内容检测器结果的明确声明；命令身份用 [[STR-001]]。

### Verification for User Story 4

- [ ] T023 [US4] [blockedBy: T017,T020] 验证 C-1..C-4 并认领：运行/修正 `tests/contract/test_humanize_command_surface.py` 的 `test_c01`..`test_c04`，核对薄模板与单一委派、技能 frontmatter 自足、四个生成副本与 `regen --check`、分类行；把通过输出记入 `.specify/specs/062-humanize-command/verification.md`。 [green: contracts/command-surface.md#C-1] [green: contracts/command-surface.md#C-2] [green: contracts/command-surface.md#C-3] [green: contracts/command-surface.md#C-4]
- [ ] T024 [US4] [blockedBy: T019,T022] 验证 C-5..C-7 并认领：核对 docs 页内容、062 注册行与详情文件、probe 对象/绑定行、编译面与固定次序（注册→编译→regen→sync）；把检查输出记入 `verification.md`。 [green: contracts/command-surface.md#C-5] [green: contracts/command-surface.md#C-6] [green: contracts/command-surface.md#C-7]
- [ ] T025 [US4] [blockedBy: T021] 验证 C-8 并认领：对比依赖清单与改动面，检索新增外部服务/网络调用/模型 API/后台常驻进程与 `src/specify_cli/`、`scripts/` 的改动，确认零新增运行时面；结果记入 `verification.md`。 [green: contracts/command-surface.md#C-8]
- [ ] T026 [US4] [blockedBy: T020,T021] 更新并验证 C-9：在 `tests/contract/test_feedback_command_classification.py` 加入 humanize=Simple（simple 3→4、docstring 同步）并在 `tests/contract/test_skill_layer_visibility_guards.py` 加入 humanize（external 13→14、census 注释同步）；运行三份契约测试并用规范 runner 做名字级全量对比（消费判据见 `.specify/skills/internal/implement-feature/SKILL.md` § Test runs；冻结名单为 `.specify/specs/062-humanize-command/notes/baseline-failed-tests.txt`），零新增失败才认领；环境判据见 § Environment Prerequisites。 [green: contracts/command-surface.md#C-9]
- [ ] T027 [US4] [blockedBy: T022] 验证 C-10 并认领：对 `templates/commands/humanize.md`、`skills/external/humanize/SKILL.md`、`docs/reference/commands/humanize.md` 与技能输出指令做检测器措辞全量检索——零通过保证/规避声明，每处提及均伴随不承诺表述；结果记入 `verification.md`。 [green: contracts/command-surface.md#C-10]

**Checkpoint**: US4 is independently verifiable: all distribution surfaces exist, generated/mirror/compile checks are green under their relative criteria, and no runtime surface was added.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Close the cross-cutting output/language/evaluation/file-safety evidence, run the quickstart end-to-end, and advance the feature status.

- [ ] T028 最终输出/语言核验：对 E8 全样本核对输出主语言跟随输入、技术术语/专有名词/代码标识符原样保留、完整改写文本为主输出；结果记入 `.specify/specs/062-humanize-command/verification.md`；认领 C-21/C-22。 [green: contracts/rewrite-behavior.md#C-21] [green: contracts/rewrite-behavior.md#C-22]
- [ ] T029 [blockedBy: T028] 评估协议收口（C-23）：汇总 ≥8 样本、两份独立评审表、确定性差异结果（invariant 改变 0、编造 0）、语言矩阵、语气矩阵、文件行为与长文档记录，写入 `verification.md`；受保护内容 per `tests/fixtures/humanize/diff_protected.py`，量规 per `tests/fixtures/humanize/rubric.md`；认领 C-23。 [green: contracts/rewrite-behavior.md#C-23]
- [ ] T030 [blockedBy: T013,T029] 最终文件安全核验（C-28..C-34）：在全新临时目录重跑源文件逐字节不变、零隐式文件、双源/空内联/非法路径/不支持格式/二进制/空文件拒收、覆盖确认、显式写入成功与失败、格式跟随、frontmatter、敏感内容零外传；结果记入 `verification.md`；文件夹具 against `tests/fixtures/humanize/files/`，协议 per `tests/fixtures/humanize/rubric.md`；认领 C-28..C-34。 [green: contracts/tone-input-file.md#C-28] [green: contracts/tone-input-file.md#C-29] [green: contracts/tone-input-file.md#C-30] [green: contracts/tone-input-file.md#C-31] [green: contracts/tone-input-file.md#C-32] [green: contracts/tone-input-file.md#C-33] [green: contracts/tone-input-file.md#C-34]
- [ ] T031 [blockedBy: T029] 按 `quickstart.md` 实跑 S1–S8 端到端管线（注册→编译→regen→sync，含逐单元证据隔离与 teardown），把命令、真实输出与退出码记入 `.specify/specs/062-humanize-command/notes/quickstart-run.md`。
- [ ] T032 [blockedBy: T030,T031] 汇总 SC-001..SC-010 状态与证据路径到 `verification.md`，并运行 `python3 .specify/scripts/python/validate-requirements.py .specify/specs/062-humanize-command/requirements.md` 与 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/062-humanize-command/tasks.md` 确认 exit 0、34 绿点无 collision。
- [ ] T033 [blockedBy: T032] 按 `.specify/shared/workflow/feature-integration.md` 将 Feature 062 从 `Planned` 推进到 `Implemented`：同步 `.specify/memory/features.md` 注册行与 `.specify/memory/features/062.md` 详情/Latest Review，记录本次实现证据路径。

---

## Feature Integration Review

- 2026-10-19, tasks phase: `.specify/memory/features.md` registers **61** features; Feature 062 exists with status `Planned`, and `.specify/memory/features/062.md` exists with the plan record. The task breakdown exposes no new Feature and invalidates no existing Feature; no registry edit is required in this phase. Status remains `Planned`; T033 advances it to `Implemented` after the gates pass.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependency; runs first.
- **Foundational (Phase 2)**: depends on Setup; blocks every story verification.
- **US1 (Phase 3)**: depends on Foundational; establishes the command template and skill core.
- **US2 (Phase 4)**: depends on US1 (the same `skills/external/humanize/SKILL.md` is extended); independently testable once its phase completes.
- **US3 (Phase 5)**: depends on US2 (same skill file) and its checkpoint; independently testable once its phase completes.
- **US4 (Phase 6)**: depends on US1–US3 artifacts; distributes the final content and closes the command-surface clauses.
- **Polish (Phase 7)**: depends on all story verifications; closes cross-cutting evidence and feature status.

### User Story Dependencies

- **US1 (P1)**: the MVP slice; no dependency on US2–US4 behavior.
- **US2 (P1)**: adds file input/output on top of the US1 skill; its checkpoint is independent, but the shared skill file serializes the write.
- **US3 (P2)**: adds tone/audience on top of the US1/US2 skill; its checkpoint is independent, but the shared skill file serializes the write.
- **US4 (P2)**: requires the final template/skill content from US1–US3; its independent test inspects distribution rather than behavior.

### Within Each User Story

- Author the artifact section first, then mirror/rendering where applicable, then verify.
- Structural tests are authored red before implementation; behavioral records are produced only after the skill body is complete.
- A verification row that writes `verification.md` is never marked `[P]` with another row writing the same file.

### Parallel Opportunities

- Phase 2: T002/T003/T004/T005 write disjoint files and may run in parallel.
- US1: T006 and T007 are sequenced in the checklist because T007’s required `skill_id` literal names the same mirror path the validator classifies as a write target; the two actual write targets (`templates/commands/humanize.md` and `skills/external/humanize/SKILL.md`) are disjoint, but only T006 carries `[P]` (no parallel partner in the phase).
- US2: T011 (file fixtures) and T012 (rubric extension) may run in parallel after their blockers; T010 serializes on the skill file.
- US3: T015 (tone fixtures/rubric) may run in parallel with T014 once its blocker is satisfied.
- US4: T017 (classification contract), T018 (probe source), T020 (generated copies), and T022 (docs page) write disjoint files and may run in parallel; T019/T021 serialize the compile/mirror order.
- Verification rows T023–T027 and Polish T028–T033 are sequential because they share `verification.md` or downstream feature-state files.

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 only** (plus Setup and Foundational). `requirements.md` explicitly calls US1 “the core value and the minimal viable slice”; it is independently testable with inline fixtures and does not require file I/O or tone options. US2 is also P1 but is a separate independently testable increment (external-document safety), so it follows the MVP rather than expanding it.

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete US1 (Phase 3).
3. **STOP and VALIDATE**: run the US1 independent test and record the MVP checkpoint.
4. Continue with US2 → US3 → US4 → Polish.

### Incremental Delivery

1. Setup + Foundational → measurement and evaluation assets ready.
2. US1 → inline humanization works; demo the MVP.
3. US2 → external documents can be rewritten safely; demo file input.
4. US3 → tone/audience controls work; demo the tone matrix.
5. US4 → the command is distributed, documented, registered, and pinned by tests.
6. Polish → cross-cutting evidence, quickstart run, and Feature 062 status.

### Parallel Team Strategy

- The shared skill file (`skills/external/humanize/SKILL.md`) is the serialization point: US1 → US2 → US3 must not be worked in parallel by different writers.
- Distribution work (US4) can be split by file: classification contract, probe registry, generated copies, and docs page are disjoint while respecting the compile → regen → sync order.

---

## Notes

### Clause partition (each clause claimed exactly once)

| Contract | Claiming row | Clauses |
|----------|--------------|---------|
| `contracts/rewrite-behavior.md` | T008 (US1) | C-11..C-19 |
| `contracts/rewrite-behavior.md` | T013 (US2) | C-20 |
| `contracts/rewrite-behavior.md` | T028 (Polish) | C-21..C-22 |
| `contracts/rewrite-behavior.md` | T029 (Polish) | C-23 |
| `contracts/tone-input-file.md` | T016 (US3) | C-24..C-27 |
| `contracts/tone-input-file.md` | T030 (Polish) | C-28..C-34 |
| `contracts/command-surface.md` | T023 (US4) | C-1..C-4 |
| `contracts/command-surface.md` | T024 (US4) | C-5..C-7 |
| `contracts/command-surface.md` | T025 (US4) | C-8 |
| `contracts/command-surface.md` | T026 (US4) | C-9 |
| `contracts/command-surface.md` | T027 (US4) | C-10 |

Total: 34 clauses, each claimed exactly once. The partition follows the phase order so a contract’s clause ordinals never run backwards; C-28..C-34 are formally closed by the final cross-cutting file-safety row (T030) while US2 owns their implementation and checkpoint verification.

### Assumptions and decisions

- **D-T1 (C-7 literal reading)**: C-7 explicitly requires both the `skill-humanize-wrapup` object row and an `h-docs-sync-eval @point:wrap-up` binding row. T018 adds both; T019 compiles. This may produce a 6-step Wrap-up face for `humanize` (the existing skill faces carry five steps). Follow the frozen contract literally; if the engine cannot express it, T019 reports an anomaly instead of dropping the binding row.
- **D-T2 (environment degradation)**: the plan-frozen 71-name baseline remains authoritative; the current 94-name capture is 23 environment-induced additions caused by the missing `cws-lib-bash` dependency. T026/GATE-1 must record a blocked/degraded verdict while the dependency is unavailable and MUST NOT relax or rewrite the baseline.
- **D-T3 (MVP)**: MVP = US1, as stated in `requirements.md` § User Story 1 “Why this priority” (the minimal viable slice). US2 is P1 but a separate increment.
- **D-T4 (classification contract counts)**: the same owner file carries stale counts (`25` in the intro, `26` in the table heading) against a 26-template tree. T017 updates both to `27` together with the `**Result**` line, so the owner is internally consistent before the conformance test derives from it.
- **D-T5 (skill registry census)**: measured `skill-*-wrapup` object rows = **48**, while the compile-unit baseline is **73 = 23 Complex commands + 50 skills**. `sdd-loop-driver` and `sdd-project-setup` carry compiled Wrap-up faces without registry object rows (pre-existing gap). T018 adds exactly one row for `humanize`; this task list does not rely on the “50/50 registry rows” claim. Disclosed as a pre-existing observation, not repaired here.

### Measured premises (commands actually run at generation time, 2026-10-19)

- Contract clauses: `python3 -c "... clause_extract ..."` → `command-surface.md 10 C-1..C-10`; `rewrite-behavior.md 13 C-11..C-23`; `tone-input-file.md 11 C-24..C-34`; `TOTAL 34`.
- Deliverables: `awk '/^```text$/{inblock=1;next} /^```$/{if(inblock){inblock=0;exit}} inblock && NF' .specify/specs/062-humanize-command/feature-ref.md | wc -l` → `17`.
- External skills: `find skills/external -mindepth 1 -maxdepth 1 -type d | wc -l` → `13`; flat mirror face: `find .specify/skills -mindepth 1 -maxdepth 1 -type d -not -name internal | wc -l` → `13`; internal: `find skills/internal -mindepth 1 -maxdepth 1 -type d | wc -l` → `37`.
- Compile units: `grep -cE '^- ' .specify/specs/062-humanize-command/notes/baseline-compile-check.txt` → `73`; after adding `skill:humanize` → `74`.
- Skill wrap-up object rows: `grep -cE '^\| skill-[a-z0-9-]+-wrapup \|' shared/definitions/probe-definitions.md` → `48` (trap: this is **not** the 50-skill compile-unit count; see D-T5).
- Mirror baseline: `grep -c '^DIFF' .specify/specs/062-humanize-command/notes/baseline-mirror-check.txt` → `209`.
- Frozen failed-name baseline: `wc -l < .specify/specs/062-humanize-command/notes/baseline-failed-tests.txt` → `71`.
- Command templates: `find templates/commands -maxdepth 1 -name '*.md' | wc -l` → `26`; after `humanize` → `27`. Docs command pages: `find docs/reference/commands -maxdepth 1 -name '*.md' | wc -l` → `25`; after `humanize` → `26` (traps: template count ≠ docs-page count because `improve` has no docs page).
- Copy directories: `.claude/commands`, `.github/prompts`, `.opencode/command`, `.qoder/commands` all present (4/4).
- Initial state: `templates/commands/humanize.md`, `skills/external/humanize/SKILL.md`, `.specify/skills/humanize/SKILL.md`, `docs/reference/commands/humanize.md`, `tests/contract/test_humanize_command_surface.py`, and `tests/fixtures/humanize/` are all absent.
- Current suite re-capture: `bash scripts/bash/run-tests.sh --names-out /tmp/humanize-tasks-current-failed.txt` → `94 failed, 3906 passed`; `comm -13 notes/baseline-failed-tests.txt /tmp/humanize-tasks-current-failed.txt` → 23 added names, all in the `cws-lib-bash`-dependent cluster (see § Environment Prerequisites).

### Runtime-evidence landing points

- `.specify/specs/062-humanize-command/notes/red-first-evidence.md` — T002 records the red command, real output, and exit status.
- `.specify/specs/062-humanize-command/notes/quickstart-run.md` — T031 records the real S1–S8 run and teardown.
- `.specify/specs/062-humanize-command/notes/pre-change-measurements.md` — T001 records the pre-change side of every diff premise, the command, and the capture date.
- `.specify/specs/062-humanize-command/verification.md` — verification rows T008, T009, T013, T016, T023–T029, and T032 record behavior, structural, and SC evidence.
- The failing-test baseline path, capture flag, and name-level comparison form are owned by `.specify/skills/internal/implement-feature/SKILL.md` § Test runs; this file only names the feature-frozen list and does not restate the owner’s procedure.

### Pre-existing observations (not repaired here)

- The 73/73 compile-face drift, the 209 mirror DIFFs, and the 71 test failures are pre-existing master debt frozen in `notes/`; this feature uses relative criteria except for the two touched pairs, which require absolute byte equality after feature-scoped sync.
- `features.md` and `features/062.md` describe the compile baseline as “50 skills”; the measured registry object-row count is 48. No edit is made to those plan-phase records; D-T5 records the discrepancy so downstream rows do not inherit it as a task premise.
