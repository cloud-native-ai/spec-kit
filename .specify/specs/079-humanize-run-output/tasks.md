# Tasks: Humanize Run Output（动作输出的人类友好化） — 079

**Requirement ID**: 079
**Requirement Key**: `079-humanize-run-output`
**Branch**: `079-humanize-run-output`（本阶段禁止切换或新建分支；不 push）
**Related Feature**: Feature 062 — Humanize Command（动作输出人类友好化）, status `Implemented`（扩展不回退；本文件任何行不得改状态，只在登记面追加扩展记录）
**Input**: Design documents from `.specify/specs/079-humanize-run-output/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required；30 FR / 10 SC / 4 用户故事 / 10 Shared Strings）、`data-model.md`（8 实体 + 26 校验规则 + 1 运行状态机）、`contracts/`（5 份文件 / 88 条条款）、`quickstart.md`（7 场景）、`feature-ref.md`（Feature 062 绑定）

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」把测试定为先写后实现；本特性无运行时，按 Principle VII 的 **template-only 门**下判 Partial（正当化），测试形态是**结构契约测试**（命令模板与技能正文的条款断言、夹具记录集的正/反例判定、坐标与名册计数、镜像与副本零漂移、门禁新增行判据），不是 unit/integration 测。

**Tests**: 红先行行 T005 / T013 / T019 / T024 / T036 各自先在未改动的树上跑出**记录在案的失败**（命令、真实输出、退出码、失败计数四字段，落入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`），主载体是 `tests/contract/test_humanize_command_surface.py`（WC-12）。T036 覆盖 WC-05…WC-15 与「条款 id ↔ 测试名」机器核对；其中不依赖实现产物的不变量守卫（WC-14 冻结面、WC-15 夹具存在性）可先绿，逐条标注为守卫、不作红先行声称。`tests/contract/test_stage_class_wiring.py` 的模板字节钉扎属**实现后守卫**（迁移/回归例外，WC-13），排在模板改写之后，不作红先行声称。

**Organization**: 按 `requirements.md` 的四个用户故事分组（US1、US2 为 P1；US3、US4 为 P2）。Foundational 只放四份故事都必须落地的两件事：技能的模式分叉（运行模式 / 内容模式）与运行夹具集——没有它们，四个故事的正文都无处落笔。88 条条款的覆盖由 § Contract Coverage Map 与各行内的条款 id 承担，并由 T036 的 `test_wc12_clause_test_map_is_total` 做「条款 id ↔ 测试名」机器核对（未转绿前不得称零缺口），不使用 `[green:]` 标签（原因见 § Format）。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/079-humanize-run-output/verification.md` 的 `deferred_tasks=`。
- DoD-2: 88 条条款各被 § Contract Coverage Map 指派给恰一行，且该行正文显式引用这些条款 id；T036 的 `test_wc12_clause_test_map_is_total` 转绿——每个条款 id 在契约可追溯性表里有非空测试名，且该名字被套件函数或 § Clause Test Waivers 的显式 waiver + remedy 认领；机器断言未绿前，人工表不得称「零缺口」。`python3 scripts/python/validate-tasks.py .specify/specs/079-humanize-run-output/tasks.md` 退出 0。
- DoD-3: 运行模式的全部行为落在 `skills/external/humanize/SKILL.md`（路由与不可协商项）与其 `references/run-mode.md`、`references/report-shape.md`（细则）；技能正文 `skill-shape.py` 判 `pass`（≤ 5000 tokens）；命令模板保持薄入口（恰好命名一个技能、frontmatter 无 `scripts:`、正文无 `## Wrap-up`）。
- DoD-4: 报告面契约成立——五个 H2 逐字且按序、载体标记行恰一个且与真实载体一致、裸文本迁移提示整句恰一次、`## Evidence` 含派发记录行、无风险时显式写「无已知风险」/`no known risks`、无可报告输出时 `## Evidence` 写 `none`。
- DoD-5: 四个派生面再生成后零漂移：`regen-command-copies.py --check` 与 `sync-mirrors.py --check` 均 exit 0，`probe-utils.py --action compile-embeds --check` 报 `75 units, zero drift`。
- DoD-6: 零新增阻断式确认门（`git diff 35ff11bc` 的扫描面新增行对 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS` 0 命中）；命令名册仍为 27 条模板；`src/specify_cli/` 与 `scripts/` 零改动。
- DoD-7: Feature 062 保持 `Implemented`；`features/062.md` 的 `## Latest Review` 与 `## Key Changes` 追加 079 扩展记录；`features.md` 的 062 行 `Last Updated` 追加 tasks 阶段标记；062 行名称/描述已是「动作输出人类友好化」口径。
- DoD-8: `verification.md` 为 SC-001…SC-010 各记一条状态行与证据路径，无一条留空。
- DoD-9: `notes/quickstart-run.md` 记录 quickstart S1–S7 的真实运行（每条给命令、真实输出、退出码或「本宿主不可复现 + 夹具替代」的如实标注），含 teardown 后 `.specify/.tmp/humanize/` 为空。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 scripts/python/validate-tasks.py .specify/specs/079-humanize-run-output/tasks.md` 退出 0，0 error。
- GATE-2: 跨制品一致 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/079-humanize-run-output --stage tasks --repo .` 报 `decision=pass`、`errors=0`；`missing-path` advisory 只允许命名本特性将要新建的路径（`notes/**`、`verification.md`、`coverage-baseline.txt`、`tests/fixtures/humanize/run/**`、`references/**`），其它路径的 advisory 是缺陷。
- GATE-3: 拆解尺度 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/079-humanize-run-output/requirements.md --tasks .specify/specs/079-humanize-run-output/tasks.md` 报 `decision=proceed`（任务行数不超过该脚本的 `TASK_CEILING`）。
- GATE-4: 条款指派完整且可机器核对 — check: 分区辅助为 `grep -ohE '\b(IP|EX|RP|CM|WC)-[0-9]{2}\b' .specify/specs/079-humanize-run-output/contracts/*.md | sort -u` 的每个 id 在 § Contract Coverage Map 出现恰一次；**真正判据**是 T036 的 `test_wc12_clause_test_map_is_total` 转绿：88 条条款↔测试名全量认领，未认领项只能以 § Clause Test Waivers 的显式 waiver + remedy 出现。人工表本身不构成「零缺口」证明。
- GATE-5: 契约套件转绿且既有守卫无新增失败 — check（经仓库 `.venv` 的 `python -m pytest -q`）：`tests/contract/test_humanize_command_surface.py` 与 `tests/contract/test_stage_class_wiring.py` 全绿，且既有套件的失败名集合相对实现期基线（捕获形式归 `/speckit.implement` 的 `**Test runs**` bullet，此处引用不重述）无新增。
- GATE-6: 派生面与门禁 — check: `python3 scripts/python/regen-command-copies.py --check`、`python3 scripts/python/sync-mirrors.py --check`、`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 均 exit 0；`git diff 35ff11bc -- templates/commands skills docs shared 'templates/*.md' | grep '^+' | grep -v '^+++'` 逐行对照 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`，`blocking_hits=0`。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/079-humanize-run-output/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器、镜像、集群、注册表或特殊硬件依赖；全部工作为本地文件、本地 git 与本地 pytest。

- Python（系统解释器）: **available** — probe: `python3 --version` → `Python 3.9.6` @ 2026-10-30；affected: T001–T036 的全部确定性脚本行（只要求 ≥3.8 与标准库）。
- pytest（仓库 `.venv`）: **available** — probe: `.venv/bin/python -m pytest --version` → `pytest 9.2.0`（解释器 `Python 3.14.6`）@ 2026-10-30；affected: T005、T013、T019、T024、T032、T035、T036。
- pytest（profiles venv，备用）: **available** — probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` → `pytest 9.1.1` @ 2026-10-30；affected: 同上（`.venv` 不可用时改用该解释器，两处基线需一致记录）。
- Git: **available** — probe: `git --version` → `git 2.54.0 (Apple Git-157)` @ 2026-10-30；affected: T001、T031、T033、T034。
- 受制裁临时根: **available** — probe: `git check-ignore -v .specify/.tmp/humanize/x.run` → `.specify/.gitignore:30:.tmp/` 命中，exit 0 @ 2026-10-30；affected: T023（并发占位）、T031（teardown 断言）。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 `[P]` 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US4]`；故事相位每行必有且仅有一个，Setup / Foundational / Polish 行禁止出现。
- **[blockedBy: T003,T004]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **不使用 `[green:]` 绿点标签**: 本特性的契约条款使用 `IP` / `EX` / `RP` / `CM` / `WC` 两字母命名空间，`.specify/scripts/python/clause_extract.py` 只识别 `C-<n>` 形态，对五份契约实测报 `form=md-none`（读数见 § Measured Premises），声明 `[green: contracts/<file>#IP-01]` 会被 `validate-tasks.py` 判 `green-dangling`（ERROR）。因此条款覆盖由 § Contract Coverage Map 与各行正文的条款 id 引用承担——同一做法见 066 / 067 的 tasks.md。
- 任务状态符（`- [ ]` / `- [>]` / `- [X]` / `- [~]`）归 `.specify/templates/tasks-template.md` § Task State Sigil，本文件不复述。
- 每行必须单行完成（含文件路径），不得换行续写；测试行写明它写入的证据槽，实现行写明它让哪一组断言转绿。

## Measured Premises（2026-10-30 生成时实测，HEAD `7b61789f`；tasks-fix 轮在 `70dd9e78` 上重测 § Wiring Surface 发现与任务行预算，分支 `079-humanize-run-output`）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/079-humanize-run-output/requirements.md` | `30` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/079-humanize-run-output/requirements.md` | `10` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/079-humanize-run-output/requirements.md` | `4`（US1/US2 为 P1，US3/US4 为 P2） |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/079-humanize-run-output/requirements.md` | `10` |
| 契约条款定义（按行首标记） | `grep -cE '^- \*\*[A-Z]{2}-[0-9]{2}\*\*' .specify/specs/079-humanize-run-output/contracts/*.md` | `content-mode 10 / execution-dispatch 21 / invocation-parse 17 / report-assembly 20 / wiring-compat 20`，合计 `88` |
| 条款计数陷阱形 | `grep -ohE '\b(IP\|EX\|RP\|CM\|WC)-[0-9]{2}\b' .specify/specs/079-humanize-run-output/contracts/*.md \| wc -l` | `191`——这是条款 id 的**提及**数（互引、可追溯性表），单位是条款**定义**时正确答案是 88；两数并记，表明测量是有意取的 |
| 条款可解析形态 | `python3 scripts/python/clause_extract.py .specify/specs/079-humanize-run-output/contracts/invocation-parse.contract.md` | `form=md-none clauses=0` + `UNPARSABLE-NAMED`——两字母命名空间不在 `shared/definitions/contract-clause-definitions.md` § 2 的 `C-<n>` 形态集内，故本条特性不用 `[green:]`、不改契约（061/066/067 先例） |
| 接线面发现（A11，无限制） | `git grep -l -i humanize 35ff11bc` | `164` 行命中。按 requirements § Wiring Surface — A11 Closed Set 的五类有序规则重算（规则 owner 在 requirements，本文件不复制判据）：活源 `7` / 派生副本 `4` / 镜像 `1` / dated record `114` / 冻结验证 `38`，未分类 `0`。逐文件清单（class + path）pin 在 `test-evidence/wiring-inventory-baseline.txt`（派生记录，不是白名单，也不是人工挑选的路径清单） |
| 接线面计数陷阱形 | `git grep -l -i humanize` | `190`——这是当前工作树的命中数，含本特性新增的 spec / 证据 / state 与既有 dated record；单位是「需手改的活接线面」时正确答案由基线提交上的无限制发现 + 分类得出（`7`），不是当前树命中数 |
| 派生面基线 | `python3 scripts/python/regen-command-copies.py --check`；`python3 scripts/python/sync-mirrors.py --check` | `OK: all per-tool command copies match the source templates.`（exit 0）；`skills/external/ == .specify/skills/ (406 files)` 等六对全 ok（exit 0）——判据为绝对 exit 0 |
| 编译面基线 | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` | `compile-embeds --check: 75 units, zero drift`（exit 0） |
| 技能正文预算 | `python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/humanize/SKILL.md` | `判定 pass`，`≈4090 tokens 可控 / 预算 5000（123 行）`；两条 warning（`oversized-section` Workflow=59 行、`flags-outside-contract` 38 flag） |
| 门禁基线 | `python3 scripts/python/scan-confirmation-gates.py --summary` | `blocking confirmation gates: 27`（destructive 20 + governance_kept 7），`violations 0` |
| 命令名册 | `ls templates/commands/*.md \| wc -l` | `27`（WC-16 的判据是名册不变，不是新增） |
| 历史语料 | `git diff --stat 35ff11bc -- tests/fixtures/humanize` | 空输出——`tests/fixtures/humanize/` 的既有语料自基线以来未变，本特性 MUST NOT 改写它（WC-15） |
| 待建路径 | `ls .specify/specs/079-humanize-run-output/notes tests/fixtures/humanize/run skills/external/humanize/references` | 三条都是 `No such file or directory`：`notes/` 由 T001 建，`tests/fixtures/humanize/run/` 由 T004 建，`skills/external/humanize/references/` 由 T006 建。条款覆盖基线不再待建：`coverage-baseline.txt` 已在 tasks 阶段冻结（497 行，`frozen-from` 头记录 base-sha `70dd9e78`） |
| 任务行预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/079-humanize-run-output/tasks.md` | 本文件 36 行（T001–T036，T036 为本轮新增的 WC 覆盖守卫行），不超过 `decomposition-check.py` 的 `TASK_CEILING`（40） |
| 任务行预算陷阱形 | `grep -oE 'T[0-9]{3}' .specify/specs/079-humanize-run-output/tasks.md \| wc -l` | 远大于 36——这是任务标识的**提及**数（`[blockedBy:]`、覆盖表、相位说明都在引用），单位是任务**行**时用行首锚定 `^- \[ \] T` |

## Contract Coverage Map

88 条条款各指派给恰一行；本表是人工指派，**机器核对由 T036 的 `test_wc12_clause_test_map_is_total` 承担**——它解析五份契约的条款定义与可追溯性表（条款 → 测试名）和本表（条款 → 行），断言分区完备且每个测试名可被套件函数认领（或出现在 § Clause Test Waivers）。在该断言转绿之前，本表只是候选指派，MUST NOT 被表述为「零缺口」。行正文重复引用其条款 id。测试行（T005 / T013 / T019 / T024 / T036）与指派行是两回事：测试行先写、先红，指派行是把它转绿的那一行。

| Contract | Clauses | Row |
|---|---|---|
| `contracts/invocation-parse.contract.md` | IP-01、IP-02、IP-03、IP-04 | T006 |
| `contracts/invocation-parse.contract.md` | IP-05、IP-06、IP-07、IP-08、IP-09、IP-10 | T007 |
| `contracts/invocation-parse.contract.md` | IP-11、IP-12、IP-13、IP-14 | T023 |
| `contracts/invocation-parse.contract.md` | IP-15 | T025 |
| `contracts/invocation-parse.contract.md` | IP-16、IP-17 | T027 |
| `contracts/execution-dispatch.contract.md` | EX-01、EX-02、EX-03、EX-04、EX-05 | T008 |
| `contracts/execution-dispatch.contract.md` | EX-06、EX-07、EX-08 | T009 |
| `contracts/execution-dispatch.contract.md` | EX-09、EX-10 | T010 |
| `contracts/execution-dispatch.contract.md` | EX-11、EX-12、EX-13、EX-14 | T020 |
| `contracts/execution-dispatch.contract.md` | EX-15、EX-16 | T021 |
| `contracts/execution-dispatch.contract.md` | EX-17、EX-18、EX-19 | T022 |
| `contracts/execution-dispatch.contract.md` | EX-20、EX-21 | T023 |
| `contracts/report-assembly.contract.md` | RP-01、RP-02、RP-03、RP-04 | T011 |
| `contracts/report-assembly.contract.md` | RP-05、RP-06 | T014 |
| `contracts/report-assembly.contract.md` | RP-07、RP-08 | T015 |
| `contracts/report-assembly.contract.md` | RP-09、RP-10 | T016 |
| `contracts/report-assembly.contract.md` | RP-11、RP-12、RP-13、RP-14 | T017 |
| `contracts/report-assembly.contract.md` | RP-15、RP-16、RP-17、RP-18 | T018 |
| `contracts/report-assembly.contract.md` | RP-19、RP-20 | T027 |
| `contracts/content-mode.contract.md` | CM-01、CM-02、CM-03、CM-04 | T025 |
| `contracts/content-mode.contract.md` | CM-05、CM-06、CM-07、CM-08 | T026 |
| `contracts/content-mode.contract.md` | CM-09 | T029 |
| `contracts/content-mode.contract.md` | CM-10 | T030 |
| `contracts/wiring-compat.contract.md` | WC-01、WC-02、WC-03、WC-04 | T012 |
| `contracts/wiring-compat.contract.md` | WC-05、WC-06、WC-07 | T028 |
| `contracts/wiring-compat.contract.md` | WC-08、WC-09 | T029 |
| `contracts/wiring-compat.contract.md` | WC-10、WC-11 | T030 |
| `contracts/wiring-compat.contract.md` | WC-12、WC-13 | T032 |
| `contracts/wiring-compat.contract.md` | WC-14、WC-15 | T033 |
| `contracts/wiring-compat.contract.md` | WC-16、WC-17、WC-18、WC-19 | T034 |
| `contracts/wiring-compat.contract.md` | WC-20 | T033 |

**Partition check**: 17（IP）+ 21（EX）+ 20（RP）+ 10（CM）+ 20（WC）= 88；31 行指派，无条款落在两行，无条款无行。IP-15（内容模式不取占位）实质落在内容模式，故随 CM-04 归 T025；WC-20（命令保持 `Simple`）由 `test_feedback_command_classification.py` 承载，故归 T033。

### Clause Test Waivers (M-21)

T036 的 `test_wc12_clause_test_map_is_total` 只认两种认领：套件里可解析的测试函数名（含参数化 id），或本表的显式 waiver 行。本表初始为空；实现期若某个契约可追溯性表里的测试名确实无法落在测试套件中，MUST 追加一行并带 remedy 与证据槽：

| 条款 | 测试名 | 不能落地的原因 | remedy（谁在何时补上） | 证据槽 |
|------|--------|----------------|------------------------|--------|

**空表不等于「零缺口」**：零缺口只由 `test_wc12_clause_test_map_is_total` 转绿证明，不由本表的行数或人手核对证明。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Rows | Requirement | Rows |
|-------------|------|-------------|------|
| FR-001 | T006, T007, T012 | FR-016 | T018 |
| FR-002 | T007, T025 | FR-017 | T018, T025 |
| FR-003 | T007 | FR-018 | T011, T017 |
| FR-004 | T006, T027 | FR-019 | T014 |
| FR-005 | T012, T029 | FR-020 | T015 |
| FR-006 | T005, T006, T007 | FR-021 | T016 |
| FR-007 | T008, T023 | FR-022 | T017, T018 |
| FR-008 | T009, T021 | FR-023 | T025, T026 |
| FR-009 | T010, T011 | FR-024 | T027, T029 |
| FR-010 | T020, T022 | FR-025 | T026 |
| FR-011 | T022 | FR-026 | T012, T028, T029, T036 |
| FR-012 | T020 | FR-027 | T034 |
| FR-013 | T006, T009 | FR-028 | T032, T033, T036 |
| FR-014 | T016 | FR-029 | T030, T036 |
| FR-015 | T016 | FR-030 | T023 |

| Success Criterion | Rows |
|-------------------|------|
| SC-001 | T005, T011, T031 |
| SC-002 | T015, T016, T031 |
| SC-003 | T020, T031 |
| SC-004 | T021, T031 |
| SC-005 | T025, T029, T031 |
| SC-006 | T028, T029, T033, T035 |
| SC-007 | T019, T023, T027, T031 |
| SC-008 | T030, T034 |
| SC-009 | T007, T016, T022, T031 |
| SC-010 | T026 |

**SC-006 闭环**: T035 按 pin 的 `test-evidence/wiring-inventory-baseline.txt` 做补集断言（重跑无限制发现 + 分类后 `comm -3` 为空；冻结验证类每个文件 `git diff --quiet 35ff11bc` 差异集合为空）与结构不变量（命令名册 27、门禁新增行 0 命中、Feature 062 状态不变），不以 T033 已列出的九个测试文件为全部分母。

**SC-007 审计仪器**: ① **静态扫描**——对 `templates/commands/humanize.md` 与 `skills/external/humanize/**` 做网络调用字面量扫描（`curl` / `wget` / `httpx` / `requests.` / `urllib` / `fetch(`），要求 0 命中（URL 文本不算调用）；② **`git status`**——运行前后 `git status --porcelain` 对比，无 `--output` 时无报告/副本写入，指令造成的写入逐项在 [[STR-003]] 披露；③ **派发记录行**——报告中的 `dispatches:` 行是派发计数与重试计数的唯一来源（重试 = 同一次调用出现第二个顶层派发；不以散文叙述为源）。T019 承载网络与重试断言（EX-11…EX-19），T023/T027 承载占位与写入边界，T031 产出真实运行读数。

**证据行与执行行**: T001、T002、T003、T004、T031、T035 为证据与执行行，不指派条款——T031 服务 SC-001…SC-009 的可复现验收，T035 把 SC 逐条收口并执行 SC-006 的闭环守卫。不构成漏映射。

## Mirror Obligations

镜像对的清单所有者是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`，命令副本的扇出目标所有者是 `scripts/python/regen-command-copies.py`；范围登记见 `plan.md` § Mirror Obligations，本文件不复述其行内容。落地形态：源编辑分散在 T012（`templates/commands/humanize.md`）、T003 / T025 / T026（`skills/external/humanize/SKILL.md`）、T006–T011 / T016 / T020–T023 / T027（`skills/external/humanize/references/`）；**T028 是唯一的再生成行**（`regen-command-copies.py` 扇出四份按工具副本、`sync-mirrors.py --write --only skills/external` 重建技能镜像，随后逐对陈述零漂移）；T033 与 T035 的终局核对只读不写。`shared/definitions/*` 本特性不改，`sync-mirrors.py --check` 仍须 exit 0（防止误改）。派生面 MUST 由再生成入口产出，MUST NOT 手改。

## Test Budget

- **本阶段（tasks）不运行任何测试套件**（docs-only 预算）：`validate-tasks` / `decomposition-check` / `pre-analyze-check` 的输出留档 `test-evidence/tasks-*.txt`，预算判定留档 `test-evidence/tasks-test-budget.txt`（`status=not-run-docs-only`）；接线面 pin 清单留档 `test-evidence/wiring-inventory-baseline.txt`，条款覆盖基线留档 `coverage-baseline.txt`（两者都是本阶段产物，不是测试运行）。
- **实现期基线（恰好一次）**: 实现开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获失败名基线；本文件任何行不得重捕获或刷新。
- **中间阶段**: 定向集——逐故事只跑本故事新增/更新的测试文件（T005 / T013 / T019 / T024 / T036 各自的行），不跑全量。
- **闭环节点**: review 之后由驱动者跑一次全量并按名比较；本特性任何行不得预支。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 证据槽与改动前读数——后续每一相位都往这两个落点写，先建好它。

- [ ] T001 建证据槽并采改动前读数：创建 `.specify/specs/079-humanize-run-output/notes/` 并把六类命令的真实输出（命令、日期、退出码一并）写进 `.specify/specs/079-humanize-run-output/notes/pre-change-measurements.md` —— ①四组计数（FR / SC / 用户故事 / Shared Strings）；②五份契约逐份条款行首计数；③A11 接线面发现：在基线提交 `35ff11bc` 上跑**无限制** `git grep -l -i humanize`，按 requirements § Wiring Surface — A11 Closed Set 的五类有序规则（活源 / 派生副本 / 镜像 / dated record / 冻结验证）为每个命中归类，未分类须为 0；把「class + path」清单与 tasks-fix 阶段 pin 的 `test-evidence/wiring-inventory-baseline.txt` 做 `LC_ALL=C comm -3`（差异为空；该文件是派生记录，不是白名单）；④`regen-command-copies.py --check`、`sync-mirrors.py --check`、`probe-utils.py --action compile-embeds --check`、`scan-confirmation-gates.py --summary` 四条基线；⑤`skill-shape.py skills/external/humanize/SKILL.md` 的正文预算读数；⑥`git diff --stat 35ff11bc -- tests/fixtures/humanize` 与 `git check-ignore -v .specify/.tmp/humanize/x.run`；该文件是全特性「改动前侧」的唯一落点。
- [ ] T002 复核已在 tasks 阶段冻结的条款覆盖基线：`coverage-baseline.txt` 由 `python3 scripts/python/account-clause-coverage.py .specify/specs/079-humanize-run-output --freeze > .specify/specs/079-humanize-run-output/coverage-baseline.txt` 在 tasks 阶段产出（497 行，头部记录 `base-sha 70dd9e78`；它是派生记录，不是本文件 Coverage Map 的副本）；实现起点只**不带 `--freeze`** 重算一次，把两车道读数（`claimed clauses`、`UNCOVERED` 中属于本特性的条数、`FR uncovered`）与冻结基线的差值追加进 `.specify/specs/079-humanize-run-output/notes/pre-change-measurements.md`；MUST NOT 重写基线，读数漂移即记录为差异并交 `/speckit.analyze` 裁定。并注明：本特性的 5 份契约在 `clause_extract.py` 下实测 `form=md-none`，故条款车道看不见这 88 条，该缺口按 § Format 由本文件的 Coverage Map + T036 的机器核对承担、不靠基座豁免。

**Checkpoint**: 两个证据落点存在且写着真实读数——后续任何行引用「改动前」时只指向 `notes/pre-change-measurements.md` 与 `coverage-baseline.txt`。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 让四个故事都有可落笔的坐标——技能的模式分叉与运行夹具集。没有模式分叉，运行模式正文会与内容模式正文抢同一个所有者；没有夹具，四个故事的契约测试都只能空手断言。

- [ ] T003 [P] 建技能模式分叉骨架：改 `skills/external/humanize/SKILL.md` 的 frontmatter description（保留全部内容模式触发词，追加「跑一条指令 → 五节报告」定位与 `--file`/`--inline` 迁移提示触发词）与 `## Overview`（新定位一句话 + 两个分支）；新增 `## Modes` 小节，只写两件事——运行模式的行为细则在 `references/run-mode.md` 与 `references/report-shape.md`（正文不复制），内容模式仍走既有 Stage 1–Stage 7（正文保留、逐字不动）；在 `## Non-negotiables` 追加两条：①零写入范围收窄为 humanize 自身（指令造成的写入按报告披露，A9）②执行体负责动作、humanize 只负责执行后的报告（A6）；改完跑 `python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/humanize/SKILL.md` 确认正文仍 `pass` 且 ≤ 5000 tokens。
- [ ] T004 [P] 建运行夹具集：在 `tests/fixtures/humanize/run/` 下写 `success/envelope.md`（`status: completed`、`final_output: humanize-fixture-ok`、`evidence` 含命令与退出码 0、`anomaly_line` 为无异常写法）、`failure/envelope.md`（退出码 3、`status: failed`、`failures` 含坐标）、`non-action/envelope.md`（`status: not-an-action`、`final_output: null`、`products: []`）、`needs-confirmation/envelope.md`（`status: needs-confirmation`、`blocked_at` 非空）、`degraded/envelope.md`（会话内执行的可观察结果）、`nested/instruction.txt`（含 `speckit.humanize` 调用 token 的指令原文）、`reservations/run-a.run` 与 `reservations/run-b.run`（两个未过期占位，字段集按 `data-model.md` § E4）、`governance/`（instructions / constitution / glossary / features 的摘要投影桩，供来源清单断言）与 `README.md`（记录格式说明，逐字段回指 `data-model.md` § E5 / § E4）；`tests/fixtures/humanize/` 的既有语料 MUST NOT 被改写。

**Checkpoint**: 技能有两个分支且正文仍自足、夹具集九件齐备——四个故事可以各自开工。

---

## Phase 3: User Story 1 - 一条指令跑完，拿回一份人读得懂的报告 (Priority: P1) — MVP 的一半

**Goal**: 裸文本被确定性地解析为待执行指令，经既有 `run-agent` 载体派发恰好一个执行体，回传结果信封，主会话按五个固定小节产出报告。

**Independent Test**: `tests/contract/test_humanize_command_surface.py` 的 US1 断言组全绿：`success/envelope.md` 驱动一次报告，五个 H2 逐字按序、载体标记行恰一个、`dispatches: 1` 一行、`products` 逐项列出；反例（两次派发、缺失异常行、标题顺序颠倒）逐条判红。

### Tests for User Story 1 (MANDATORY)

- [ ] T005 [US1] [blockedBy: T003,T004] 红先行扩展 `tests/contract/test_humanize_command_surface.py`：把模块 docstring 的归属改为 062 C-1..C-10 + 079 条款集两段，并按 `contracts/invocation-parse.contract.md` IP-01…IP-10、`contracts/execution-dispatch.contract.md` EX-01…EX-10、`contracts/report-assembly.contract.md` RP-01…RP-04、`contracts/wiring-compat.contract.md` WC-01…WC-04 组织断言（纯语法解析与判定表逐行求值、指令逐字进入载荷、恰好一次派发且载体二选一、载荷六项与顺序、信封缺异常行即不得消费、五节标题逐字按序、薄入口三条不变式、模板无阻断字面量）；用 `tests/fixtures/humanize/run/` 与 `tmp_path` 构造合规集与反例集（反例必须被判红），并把 `python -m pytest -q tests/contract/test_humanize_command_surface.py` 的真实失败（命令、输出、退出码、失败计数）记入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T006 [US1] [blockedBy: T005] 写 `skills/external/humanize/references/run-mode.md` 的 § Parse：选项集与「只出现在指令之前」、`--` 终止规则、第一个不可识别 token 即指令起点、指令逐字（含换行与引号）且不被摘要或规范化、解析是纯语法过程（同 argv 同结果、不读内容猜意图）、解析结果落入 `data-model.md` § E2 的字段集且 `mode` 只有 `run` / `content` / `reject` 三值、`--tone` 取值域与 `--audience` / `--output` / `--force` 语义逐字沿用 062（IP-01、IP-02、IP-03、IP-04）。
- [ ] T007 [US1] [blockedBy: T006] 写同一文件的 § Mode Routing 与 § Migration Hint：按 `data-model.md` § E2 判定表四行求值且顺序不可调换（内容源+非空指令→拒绝并点名两者；内容源+空指令→内容模式；无内容源+非空指令→运行模式；两者皆无→拒绝）、空内容源落 `empty-input` 而非内容模式、无输入时输出用法行 + 支持的内容源 + 迁移提示整句三项齐全、运行模式且无任何显式内容源时在载体标记行之后输出迁移提示整句一次（字面量 owner 是 requirements A4，本处逐字复写一次作为测试钉扎字面量）、该行不构成第六节且同一运行至多一行；`reject_code` 封闭集与点名要素按 `data-model.md` § E2 表（IP-05、IP-06、IP-07、IP-08、IP-09、IP-10）。
- [ ] T008 [US1] [blockedBy: T007] 写同一文件的 § Dispatch：每次调用恰好一个顶层执行体（一次调用两次派发或「先试一个再补一个」都判违反）、经既有 `run-agent` 的 Run Mode 派发且不引入第二套机制、执行体是会话级临时执行体（不写 `.specify/agents/`、不产生 `.agent.md`、不占 Agent 席位、不声明 SDD 执行席位、不因为按名解析不适用就在磁盘上造定义）、载体按宿主能力二选一（`native` / `in-session`，排除独立 CLI 进程模式）、载体标记与真实载体一致且恰一个（`native` → `mode: subagent`，`in-session` → `mode: in-session-degraded`，不冒充不双写不漏写）（EX-01、EX-02、EX-03、EX-04、EX-05）。
- [ ] T009 [US1] [blockedBy: T008] 写同一文件的 § Payload：载荷按序携带六项（快速失败注入子句逐字节相等且置于开头独立段落 → 指令原文逐字 → 回传信封字段与封闭取值 → 不得撰写最终报告 → 不得重试且不得代替用户答复 → 指令自身再调用本命令即拒绝并回传）、不把指令改写成步骤清单或预先挑选实现路径、声明指令自身的确认步骤与权限边界优先并于无法取得答复时停在该步（EX-06、EX-07、EX-08）；快速失败子句的拥有者字面量只引用 `shared/guidelines/fast-fail.md` § 子代理派发注入，MUST NOT 在此改写或摘要。
- [ ] T010 [US1] [blockedBy: T009] 写同一文件的 § Envelope：回传是 `data-model.md` § E5 的消息而非报告文件（零写入）、逐字段语义（`status` 六值、`products`、`evidence`、`failures`、`blocked_at`、`anomaly_line`）与其不变量（`needs-confirmation` ⇒ `blocked_at` 非空；`completed` 且无输出无产物 ⇒ 报告写「无可报告输出」且 `## Evidence` 写 `none`）、缺显式异常行即判信封不完整且其结论不得被消费、报告记失败并点名缺失项（EX-09、EX-10）。
- [ ] T011 [US1] [blockedBy: T005] 写 `skills/external/humanize/references/report-shape.md` 的 § Metadata Block 与 § Sections：五个 H2 逐字按序（字面量 owner 是 requirements § Shared Strings）、五节之前只有一条载体标记行（裸文本时其后加一条迁移提示行）且不构成第六节、报告由 humanize 主会话撰写且不得出现以执行体身份的自述、默认只在会话内呈现且不写隐式副本或默认位置（RP-01、RP-02、RP-03、RP-04）。
- [ ] T012 [US1] [blockedBy: T006] 改写 `templates/commands/humanize.md`：入口处声明破坏性变更（裸文本 = 待执行指令；改写既有文本 MUST 用 `--file` 或 `--inline`）并给出一条可复制的迁移示例；委派节仍恰好命名一个技能且 frontmatter 无 `scripts:` 块、正文无 `## Wrap-up`（薄入口不变式）；`## Outline` 内 077 的类别接线小节逐字保留；不复述技能的 Stage 表或报告五节细则；改完用 `python3 scripts/python/scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS` 对新增行判定为 0 命中（模式集以该脚本为准，不手抄）（WC-01、WC-02、WC-03、WC-04）。

**Checkpoint**: US1 可独立验证——一条夹具指令走完「解析 → 派发 → 信封 → 五节报告骨架」，且反例集逐条判红。

---

## Phase 4: User Story 2 - 报告要"友好"：结论先行、证据可查、来源可追 (Priority: P1) — MVP 的另一半

**Goal**: 报告不是原始日志套壳：结论先行、关键变化按影响排序、每条结论有可定位证据、风险与缺失来源摊开、下一步可执行，并声明本次实际读取的上下文来源。

**Independent Test**: `tests/contract/test_humanize_command_surface.py` 的 US2 断言组全绿：同一信封生成两份报告时结论均先于细节；来源清单只列实际读取的源，缺失项进 `## Risks & Limits`；无风险时显式写「无已知风险」/`no known risks`；`--audience`/`--tone` 只改表达层。

### Tests for User Story 2 (MANDATORY)

- [ ] T013 [US2] [blockedBy: T005] 红先行补 `tests/contract/test_humanize_command_surface.py` 的 US2 组：按 `contracts/report-assembly.contract.md` RP-05…RP-18 断言（结论五值文案面、关键变化排序与「无变化」显式、证据指针可定位且无形容词充数、派发记录行、风险节不得省略、来源清单与实际读取一致、下一步或显式「无下一步」、正文语言三顺位、标题恒英文、标识符不随语言漂移、保真底线、不得编造、表达四维与检测器诚实、面向读者可理解性）；用 `tests/fixtures/humanize/run/governance/` 造「部分来源不可得」与「全可得」两态，并把真实失败记入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`。

### Implementation for User Story 2

- [ ] T014 [US2] [blockedBy: T013] 写 `skills/external/humanize/references/report-shape.md` 的 § Conclusion 与 § Key Changes：结论先于一切细节且取值封闭为 `success` / `partial` / `failure` / `aborted` / `needs-confirmation` 的文案面、失败时禁用成功措辞（允许「部分完成」）、`status=not-an-action` 的结论文案是「未执行任何动作」而非「执行成功」；关键变化按影响降序、无变化时明写「无变化」、指令造成的写入在此可见（RP-05、RP-06）。
- [ ] T015 [US2] [blockedBy: T014] 写同一文件的 § Evidence：每条关键结论配可定位指针（产物路径、命令与退出码、测试读数、可定位引用），指令造成的写入逐项列出，无可报告输出时写 `none`；含一行派发记录元数据（顶层派发次数，成功路径为 1），口径只计 humanize 发起的顶层派发、指令自身再发起的派发不重复计数（RP-07、RP-08）。
- [ ] T016 [US2] [blockedBy: T010,T015] 写 `skills/external/humanize/references/run-mode.md` 的 § Context Assembly 与 `report-shape.md` 的 § Risks & Limits：报告前装配三类上下文（动作输出/证据、项目治理四件、本次会话），读取按摘要优先（注册表取行投影、治理文档取相关段落，不整文件注入）；风险节列风险、限制、未验证项与缺失上下文，无已知风险时用报告语言显式写出该判断且不得省略；来源清单只列实际读取的源，读取失败或未读取的源作为缺失项同节声明（RP-09、RP-10）。
- [ ] T017 [US2] [blockedBy: T016] 写同一文件的 § Next Steps 与 § Language：下一步可执行或显式「无下一步」、不用泛泛建议充数；正文语言先取指令主语言、不可判时回退项目治理（instructions / glossary）、两者都不可得时用调用会话语言并在风险节声明回退；五节标题与两个键名（载体标记、派发记录）恒英文原样；语言适配不得改事实层（术语、专有名词、代码标识符、路径、命令原样）（RP-11、RP-12、RP-13、RP-14）。
- [ ] T018 [US2] [blockedBy: T017] 写同一文件的 § Fidelity & Honesty：保真底线全文生效（受保护集合的枚举 owner 是 requirements FR-017，不复制集合）、上下文补全只用已蕴含或可严格推出的信息、不得编造未发生的工作/未读取的来源/未出现的读数/不存在的路径、核对不上的证据记为「未能核实」、表达层只应用四维自然化中适用的部分并服从 `--tone`/`--audience`、不承诺也不暗示任何 AI 内容检测器结果、内部引擎调用形式不得出现在给读者的正文里（RP-15、RP-16、RP-17、RP-18）。

**Checkpoint**: US2 可独立验证——单看一份报告就能判断结论是否先行、证据是否可点开、来源是否与实际读取一致。

---

## Phase 5: User Story 3 - 安全与诚实：不绕过确认、不掩饰失败、不自动重试 (Priority: P2)

**Goal**: 指令含破坏性动作时走它自己的确认；被拒绝或无法询问就停住并如实记录；失败不重试、不粉饰；humanize 自身不联网、不写隐式文件；并发与嵌套 fail-closed 并点名冲突。

**Independent Test**: `tests/contract/test_humanize_command_surface.py` 的 US3 断言组全绿：`needs-confirmation` 夹具在卡点处停下且报告记卡点、`failure` 夹具的报告全文无成功措辞且无第二次派发、两个占位夹具下后到者点名冲突 `run_id`、`nested/instruction.txt` 被拒并点名 `speckit.humanize` 字面量、拒绝路径不产生任何文件。

### Tests for User Story 3 (MANDATORY)

- [ ] T019 [US3] [blockedBy: T013] 红先行补 `tests/contract/test_humanize_command_surface.py` 的 US3 组：按 `contracts/execution-dispatch.contract.md` EX-11…EX-21 与 `contracts/invocation-parse.contract.md` IP-11…IP-14 断言（不补发、失败坐标与不重试、中止如实、证据可定位性核对、确认缺失 fail-closed 与不代答、降级诚实、降级不改报告契约、零外发、占位全出口释放、派发记录只计顶层；仓库级占位、目标级占位、嵌套 token、拒绝路径零写入）；用 `tests/fixtures/humanize/run/reservations/`、`needs-confirmation/`、`nested/`、`degraded/` 造正反例；「零外发」与「不重试」的判定仪器写死在本行断言里——静态扫描（模板与技能源对 `curl` / `wget` / `httpx` / `requests.` / `urllib` / `fetch(` 0 命中，URL 文本不算调用）、运行前后 `git status --porcelain` 对比无未授权写入、报告 `dispatches:` 行作为派发与重试计数的唯一来源（同一次调用出现第二个顶层派发即判重试，不以散文叙述为源）；并把真实失败记入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T020 [US3] [blockedBy: T019] 写 `skills/external/humanize/references/run-mode.md` 的 § Failure & No Retry：失败不自动重试（每次运行至多一次执行尝试）、载荷发出后才发现缺快速失败子句即停止消费并按失败报告且不得以「补发一次」修复、派发失败/超时/中止记录失败坐标（载体、阶段、错误信息）与已完成部分且不得改写为成功、用户中止记录中止点与已完成部分且口径为「已中止」、回传的证据逐项核对可定位性、核对不上的项不作证据并记为「未能核实」（EX-11、EX-12、EX-13、EX-14）。
- [ ] T021 [US3] [blockedBy: T020] 写同一文件的 § Confirmation Missing：执行到需用户确认的步骤而执行体无法询问时不执行该步、`blocked_at` 记卡点、结论写「需要确认，未获答复」、其余已完成部分照常报告；主会话不得代替用户回答、不得以「用户可能同意」继续、不得换等价动作绕开（EX-15、EX-16）。
- [ ] T022 [US3] [blockedBy: T021] 写同一文件的 § Degradation & Boundaries：降级为会话内执行时声明降级且只把可观察结果当事实、不把推断描述为子代理的观测、不声称独立上下文或独立工具集、降级不改五节与证据义务与保真底线；humanize 自身不发起网络请求、不调用外部服务或模型 API，指令自身按其契约产生的联网行为在报告中披露且不计作 humanize 的外发（EX-17、EX-18、EX-19）。
- [ ] T023 [US3] [blockedBy: T022] 写同一文件的 § Reservation & Nesting 与出口记账：派发前在 `.specify/.tmp/humanize/<run_id>.run` 建立仓库级占位（一文一件，仓库级与目标级各至多一个未过期占位）、已有未过期占位按 `active-run` 拒绝并点名冲突 `run_id` 与起始时间、给 `--output` 时同时取得目标级占位、被占用按 `output-occupied` 拒绝并点名路径与冲突 `run_id`、超过 24h 视为遗弃且只点名不删他人文件、指令含 `speckit.humanize`（大小写不敏感）按 `nested-invocation` 拒绝并点名命中字面量并说明这是保守判定、任何拒绝路径不派发不留占位不写文件、任一出口（正常/失败/中止/异常）释放本人占位；同节补一行派发记录口径指针到 `report-shape.md` § Evidence（只计 humanize 发起的顶层派发）（IP-11、IP-12、IP-13、IP-14、EX-20、EX-21）。

**Checkpoint**: US3 可独立验证——失败仍是失败、确认缺失无副作用、两个并发占位只有先到者继续、嵌套被点名拒绝。

---

## Phase 6: User Story 4 - 旧的文本改写入口仍可用，迁移路径清楚 (Priority: P2)

**Goal**: `--file` / `--inline` 仍是完整的改写入口且行为与保真底线不降级；裸文本被执行而非被改写；模板、docs、副本、镜像与本页 Feature 登记同步到新定位。

**Independent Test**: `tests/contract/test_humanize_command_surface.py` 的 US4 断言组全绿：`--inline` / `--file` 各跑一次输出改写文本、无五节无载体标记无迁移提示、无派发；同一段文本以裸文本调用被执行；docs 页可抄到迁移写法；`regen-command-copies.py --check` 与 `sync-mirrors.py --check` exit 0。

### Tests for User Story 4 (MANDATORY)

- [ ] T024 [US4] [blockedBy: T019] 红先行补 `tests/contract/test_humanize_command_surface.py` 的 US4 组：按 `contracts/content-mode.contract.md` CM-01…CM-10、`contracts/invocation-parse.contract.md` IP-15…IP-17、`contracts/report-assembly.contract.md` RP-19…RP-20 断言（内容模式等价与输出只含改写文本、无报告脚手架、无派发无占位、路由 owner 不重述、注入与保真与检测器诚实两模式同时生效、迁移示例可在模板与 docs 中抄到、内容模式措辞不被写成兼容垫片；运行模式 `--output` 扩展名封闭集、写完整报告并回显摘要、原子写与 `--force`、不可写即拒绝且不留部分文件）；用 `tests/fixtures/humanize/files/`、`inline/` 的既有语料与 `tmp_path` 造正反例，并把真实失败记入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`。
- [ ] T036 [US4] [blockedBy: T024] 红先行补 WC-05…WC-15 组与「条款 id ↔ 测试名」机器核对（同一主契约套件 `tests/contract/test_humanize_command_surface.py`，不新增文件）：①派生面 WC-05/06/07（四份副本与镜像只由再生成入口产出、`--check` exit 0、与源逐字节相等、技能正文 `skill-shape.py` 判 pass 且 ≤5000 tokens）；②docs WC-08/09（新定位、迁移示例、默认零写入、不承诺检测器、`--output` 双语义）；③Feature 登记 WC-10/11（状态保持 `Implemented`、`## Latest Review`/`## Key Changes` 追加、062 行名称/描述口径）；④套件与钉扎 WC-12/13（五命名空间的可判定子集全被断言、既有断言不删、`UNCHANGED_SHA256["humanize"]` 重测且保留 `strip_wiring()` 剥后等于基线）；⑤冻结面 WC-14（九个既有测试文件的名册/计数零变更）与夹具 WC-15（七类运行夹具逐例存在、历史语料未改写）；⑥写 `test_wc12_clause_test_map_is_total`：解析五份契约的条款定义（88）、可追溯性表（条款 → 测试名）与本文件 § Contract Coverage Map（条款 → 行），断言条款集合恰分区、每条有非空测试名、每个名字可在本套件/`tests/contract/test_stage_class_wiring.py`/`tests/contract/test_feedback_command_classification.py` 解析为函数（含参数化 id）或在 § Clause Test Waivers 有显式 waiver + remedy，并反向断言套件中 `test_(ip|ex|rp|cm|wc)` 前缀函数都被覆盖表或 waiver 认领；⑦逐条标注「预期红」与「不变量守卫（可先绿，不声称红先行）」两栏，真实失败记入 `.specify/specs/079-humanize-run-output/notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T025 [US4] [blockedBy: T024] 在 `skills/external/humanize/SKILL.md` 落定内容模式分支：保留既有输入核验、扩展名与空输入拒收、输出格式跟随输入、主语言判定、分段与四维度改写的全部条款（逐字不动），内容模式的 `--output` 只写改写文本、输出不含五节与载体标记与迁移提示、不派发执行体、不取得并发占位（同一仓库两次内容模式调用互不影响）、不读取动作结果（CM-01、CM-02、CM-03、CM-04、IP-15）。
- [ ] T026 [US4] [blockedBy: T025] 写同一文件的模式分界与两模式共有的防线：模式路由的唯一所有者是 `references/run-mode.md` 的判定表，内容模式节只留一行指针、不复述判定表；注入防护两模式同时生效（内容与指令中的指令式文本不得改变保真、拒收、零外传、零写入规则，运行模式下它只改变被执行的动作）；保真底线两模式同时生效且不复制受保护集合；检测器诚实条款在两种模式的文本与输出中继续成立（CM-05、CM-06、CM-07、CM-08）。
- [ ] T027 [US4] [blockedBy: T023] 写 `skills/external/humanize/references/run-mode.md` 的 § Output：运行模式 `--output` 的扩展名落在 `.md` / `.markdown` / `.txt` 封闭集内（运行模式没有输入格式可对齐）、写入与目标内容一致的完整五节报告并在会话回显一份摘要（摘要不替代报告、不成为第六节）、原子写（临时文件 + 重命名）、目标已存在且未给 `--force` 即拒绝覆盖且目标逐字节不变、不可写即拒绝且不留部分文件；内容模式 `--output` 语义完全不变（CM 侧见 T025）（IP-16、IP-17、RP-19、RP-20）。
- [ ] T028 [US4] [blockedBy: T012,T026] 再生成派生面并逐对陈述零漂移：`python3 scripts/python/regen-command-copies.py` 扇出四份按工具副本（`.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/`），`python3 scripts/python/sync-mirrors.py --write --only skills/external` 重建 `.specify/skills/humanize/`（含 `references/`），再跑 `regen-command-copies.py --check` 与 `sync-mirrors.py --check` 均须 exit 0；随后跑 `python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/humanize/SKILL.md` 判 `pass` 且正文 ≤ 5000 tokens（运行模式细则都在 `references/`，不塞正文）；全程不手改派生文件（WC-05、WC-06、WC-07）。
- [ ] T029 [US4] [blockedBy: T028] 改写 `docs/reference/commands/humanize.md`：新定位（跑一条指令 → 五节报告）＋保留旧内容模式的调用方式、一条可复制的迁移示例（同一段文本用 `--inline` 或 `--file` 调用即得改写，裸文本会被当作指令执行）、默认零写入、不承诺检测器结果、输入按数据处理；写明 `--output` 在运行模式写完整报告并回显摘要、在内容模式只写改写文本（WC-08、WC-09、CM-09）。
- [ ] T030 [US4] [blockedBy: T029] 收口措辞并登记 Feature 062：核对模板与 docs 未把内容模式写成「兼容垫片」或暗示它是新能力的向下兼容层（它是保留的既有入口）；在两处登记面做**追加**（不改既有段落）——`.specify/memory/features/062.md` 的 `## Latest Review` 追加 tasks 阶段扩展记录（本规格 36 行任务、88 条款人工指派 + T036 机器核对、五个红先行行、主契约套件载体）与 `## Key Changes` 追加一条，`.specify/memory/features.md` 的 062 行 `Last Updated` 追加 tasks 阶段标记；状态列保持 `Implemented`，不新建 Feature 行，并核对 062 行的名称/描述已是「动作输出人类友好化」口径（WC-10、WC-11、CM-10）。

**Checkpoint**: US4 可独立验证——两个旧入口给出改写文本、裸文本被执行、docs 可抄到迁移写法、四份副本与技能镜像零漂移、Feature 062 状态未动。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 把「真的跑过」留成证据，并把 SC 逐条收口。

- [ ] T031 [blockedBy: T028,T030] 跑 quickstart S1–S7 并记录：按 `.specify/specs/079-humanize-run-output/quickstart.md` 逐场景真实调用 `/speckit.humanize`（S1 成功、S2 失败、S3 非动作、S4 内容模式两入口 + 裸文本、S5 A 同现拒绝 / C 嵌套拒绝、S6 确认缺失、S7 B 写出报告 / C 不可写目标），每条记录命令、真实输出与退出码；S5 B（两会话并发）与 S7 A（无子代理通道的宿主）在本宿主不可复现，如实标注 `not-reproducible in this host` 并改用 `tests/fixtures/humanize/run/reservations/` 与 `degraded/` 的夹具断言替代；全部真实输出写入 `.specify/specs/079-humanize-run-output/notes/quickstart-run.md`，并记录 teardown 后 `ls .specify/.tmp/humanize/` 为空与 `git status --porcelain` 无新增。
- [ ] T032 [blockedBy: T031] 主契约套件转绿并重测字节钉扎：跑 `python -m pytest -q tests/contract/test_humanize_command_surface.py` 全绿（覆盖 IP-01…IP-17、EX-01…EX-21、RP-01…RP-20、CM-01…CM-10、WC-01…WC-15 的可判定部分），既有断言一条不删、不以「计数变了」为由放宽；把 `tests/contract/test_stage_class_wiring.py` 的 `UNCHANGED_SHA256["humanize"]` 按新模板重新度量，在该行注明日期与理由（模板已按 079 改写），并保留「剥掉接线小节后等于基线」的判定形态（`strip_wiring()` 剥后的字节对冻结基线断言），跑该文件全绿（WC-12、WC-13）。
- [ ] T033 [blockedBy: T032] 核对冻结面与夹具集：逐项跑 `tests/contract/test_expression_gate_wiring.py`、`test_expression_gates_doc.py`、`test_expression_compatibility.py`、`test_flow_class_ledger.py`、`test_flow_class_correctness.py`、`test_feedback_command_classification.py`、`test_migration_distribution.py`、`test_run_skills_wiring.py`、`test_skill_layer_visibility_guards.py` 并记录「无需改动且仍绿」的实测（名册/计数零变更）；WC-20 的判据落在 `test_feedback_command_classification.py` 的 `test_simple_command_omits_feedback_step[humanize]`（模板无 `## Feedback` 步）与 `test_table_covers_every_command_template`（027 分类表仍覆盖全部模板），须记录这两个测试 id 的实测，不只声明「仍为 Simple」；断言 `tests/fixtures/humanize/run/` 七类夹具（成功、失败、非动作、需确认、嵌套、降级、并发）逐例存在，且 `git diff --stat 35ff11bc -- tests/fixtures/humanize ':!tests/fixtures/humanize/run'` 为空（历史语料未改写）；实测写入 `.specify/specs/079-humanize-run-output/verification.md`（WC-14、WC-15、WC-20）。
- [ ] T034 [blockedBy: T033] 门禁、名册与零运行时核对：`ls templates/commands/*.md | wc -l` 仍为 27（无新增命令）；`git diff --stat 35ff11bc -- src/specify_cli scripts` 为空（零新增运行时与依赖）；`python3 scripts/python/flow-class-check.py --action lookup --unit-id "skill:humanize"` 仍报 `expression` / `reader-oracle`，`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 仍报 `75 units, zero drift`（无新增注册行）；按**新增行**判定确认门预算：`git diff 35ff11bc -- templates/commands skills docs shared 'templates/*.md' | grep '^+' | grep -v '^+++'` 逐行对照 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`，要求 `blocking_hits=0`，并与 `test-evidence/gate-newline-baseline.txt` 的改动前读数（`added_lines=0` / `blocking_hits=0`）并列记录（WC-16、WC-17、WC-18、WC-19）。
- [ ] T035 [blockedBy: T034] SC 收口与留档：把 T031–T034 的真实输出贴入 `.specify/specs/079-humanize-run-output/verification.md`，为 SC-001…SC-010 各记一条状态行与证据路径（无一条留空）；跑 SC-006 **闭环守卫**——在基线提交 `35ff11bc` 上重跑无限制 `git grep -l -i humanize`，按 requirements § Wiring Surface — A11 Closed Set 的五类有序规则重新分类，与 pin 的 `test-evidence/wiring-inventory-baseline.txt` 做 `LC_ALL=C comm -3`（输出为空：无新增命中、无未分类项），再对冻结验证类的**每个**文件跑 `git diff --quiet 35ff11bc -- <path>`（差异集合为空 = 补集为空；不得只核对 T033 已列出的九个测试文件），并逐项记录结构不变量（命令名册 27、门禁新增行 0 命中、Feature 062 状态 `Implemented`）；跑 T036 的 `test_wc12_clause_test_map_is_total` 并记录 `clause-test-map=total`（任何未认领的测试名必须出现在 § Clause Test Waivers 且带 remedy），未经该断言不得把人工表称为「零缺口」；最后跑一次 `python3 scripts/python/validate-tasks.py .specify/specs/079-humanize-run-output/tasks.md` 与 `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/079-humanize-run-output --stage tasks --repo .` 留档。

**Checkpoint**: SC-001…SC-010 每条都有可复现的证据来源，`verification.md` 是它们的唯一索引；quickstart 的真实运行在 `notes/quickstart-run.md`。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，先做——T001 与 T002 都写 `notes/pre-change-measurements.md`，故串行。
- **Foundational (Phase 2)**: 依赖 Setup；**阻塞全部故事**。T003（技能骨架）与 T004（夹具集）写目标不同，可并行。
- **User Stories (Phase 3–6)**: 依赖 Foundational 完成。US1 与 US2 共用 `report-shape.md`，按 `[blockedBy:]` 串行；US3 续写 `run-mode.md`；US4 落定内容模式分支与派生面。
- **Polish (Phase 7)**: 依赖 T030 与 T028 完成（接线与登记都落定后才跑真实运行）。

### User Story Dependencies

- **US1 (P1)**: Foundational 之后可独立开工；不依赖 US2/US3/US4 的产物（它只消费夹具与技能骨架）。
- **US2 (P1)**: Foundational 之后可开工；它与 US1 同写 `report-shape.md`，故在 US1 的报告骨架之后落笔。
- **US3 (P2)**: 两个 P2 故事中先做——它的安全条款写在 US1 已建好的 `run-mode.md` 上，且 US4 的拒绝路径（IP-06…IP-08）与它共用同一个点名要素表；两个 P2 同级，先安全后接线。
- **US4 (P2)**: 依赖 US3（`run-mode.md` 已定稿才写 § Output 的边界）与 T012（模板改完才再生成副本）；其测试小节有两行（T024 覆盖 CM/IP-15…17/RP-19…20，T036 覆盖 WC-05…WC-15 与条款↔测试名机器核对），两行都先于 T025 起的实现行落笔。

### Within Each User Story

- 测试先写、先红、先留证；实现行随后让它转绿。T036 虽编号在 35 之后，却与 T024 同处 US4 的测试小节、按行序先于 T025 起的实现行执行；编号是标识，执行序由小节的 blockedBy 与行序给出。
- 同一文件的多行按行序串行（`SKILL.md`、`references/run-mode.md`、`references/report-shape.md` 各有多个写入行）。
- 每个故事在自己的 Checkpoint 处可独立验证，不靠后续故事补齐。

### Parallel Opportunities

- Foundational 的 T003（`SKILL.md`）与 T004（`tests/fixtures/humanize/run/`）写目标互不相交，可并行。
- 本文件其余段落零 `[P]`：`notes/red-first-evidence.md` 是五个测试行（含 T036）共用的追加落点，`notes/quickstart-run.md` 与 `verification.md` 是多个 Polish 行共用的追加落点，`SKILL.md`、`run-mode.md`、`report-shape.md`、`docs/reference/commands/humanize.md` 各被多行写入——共享 sink 与同文件即同写目标，按行序串行，不靠删路径消警。

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2（两个 P1 故事）。理由按模板的 MVP 规则：只有 US1 而没有 US2，报告只有骨架而不「友好」——结论先行、证据可查、来源可追正是本特性的定义性要求；两者合起来才是可独立交付的最小增量。

1. 完成 Phase 1 与 Phase 2（证据槽 + 模式分叉与夹具）。
2. 完成 US1 与 US2，在每个 Checkpoint 独立验证。
3. **STOP and VALIDATE**: 跑定向集，确认 US1/US2 的断言组转绿且反例集判红。
4. 继续 US3（安全）、US4（内容模式与接线），最后 Phase 7 收口。

### Incremental Delivery

1. Foundational → 技能有两个分支、夹具九件齐备。
2. US1 + US2 → 「跑一条指令 → 五节友好报告」成立（MVP）。
3. US3 → 失败、确认缺失、并发与嵌套全部 fail-closed 且如实。
4. US4 → 旧入口与迁移路径成立、派生面零漂移、Feature 登记完成。
5. Polish → 真实运行证据与 SC 收口。

---

## Notes

- [P] 只标在写目标不同、无未完依赖的行；共享追加落点（`notes/*.md`、`verification.md`）与同文件多写行一律串行。
- **PLAN-EDIT 声明（本阶段实际发生）**: 无。本阶段未修改任何 plan 属主制品（`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md` 均未触碰），因此没有 `PLAN-EDIT:` 行。
- **Analyze 回环修复（tasks 轮，本阶段实际发生）**: ①H-02——§ Measured Premises 的「7 条显式路径 grep」换成基线提交上的**无限制发现 + 五类分类规则**，结果集 pin 在 `test-evidence/wiring-inventory-baseline.txt`（派生记录，不是白名单；规则 owner 是 requirements § Wiring Surface），T035 增加补集为空 + 结构不变量的闭环守卫；②M-03——SC-007 覆盖行加入 T019，审计仪器写为静态扫描 + `git status` + 报告 `dispatches:` 行，重试计数以派发记录为源；③M-21——`coverage-baseline.txt` 在 tasks 阶段冻结，IP-15 改归 T025（实质 CM-04）、WC-20 改归 T033（`test_feedback_command_classification.py`），新增 T036 覆盖 WC-05…WC-15 与「条款 id ↔ 测试名」机器核对，并在 § Clause Test Waivers 定义显式 waiver 机制。
- **条款核算缺口（如实记录）**: 五份契约使用 `IP` / `EX` / `RP` / `CM` / `WC` 两字母条款命名空间，`clause_extract.py` 实测 `form=md-none`，因而 `account-clause-coverage.py` 的条款车道与 FR 车道都看不见这 88 条（FR 车道 0/30）；`coverage-baseline.txt` 已在 tasks 阶段冻结，实现起点只复核、不重写。覆盖由 § Contract Coverage Map 人工指派 + T036 的机器核对承担；机器断言转绿前，本表不是「零缺口」证明。把 88 条改名为 `C-<n>` 属 plan 属主制品变更，本阶段不做。
- **历史不改写**: `.specify/specs/**` 的既有特性、`memory/evidence/**`、`features/<ID>.md` 的既有段落（只追加）、reviews、eval-baseline、`tests/fixtures/humanize/` 既有语料都是 dated record，本文件任何行不得回填。
- **临时目录**: 只有运行模式的并发占位落 `.specify/.tmp/humanize/`（已被 `.specify/.gitignore` 的 `.tmp/` 规则匹配，`git check-ignore` 实测命中）；运行结束即释放，残留即判违反。
- **零写入边界**: humanize 自身不写报告与副本（除显式 `--output`）；指令自身产生的写入是执行结果的一部分，必须在报告中逐项披露，不视为违反零写入。
