# 同构映射、迁移兼容与度量仪器 Checklist: Feature 069 / Slice 069b

**Purpose**: 对 069b 的**需求（What）**做质量审查——8 阶段 × 3 面的映射是否真的可逐行核对、四类不可同构边界是否真的绑到门禁、台账扩展是否可证伪、迁移与分发判据是否真的能在快照上跑起来、三项度量是否只用既有仪器且无样本不记零、14 FR / 5 SC / 51 条款是否被 29 个任务真实覆盖。本清单不评判实现好坏，只评判要求写得是否可判定、可测量、可追溯。

**Created**: 2026-10-25
**Feature (Requirement Scope)**: Feature 069「执行/表达二元分类与文档型 SDD 同构」（`.specify/memory/features.md` 第 77 行 / `.specify/memory/features/069.md`）；本清单只覆盖切片 `069b-isomorphism-migration-metrics`
**Requirements (What)**: [requirements.md](../requirements.md)（14 FR / 5 SC / 3 Shared Strings）
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[data-model.md](../data-model.md)、[contracts/](../contracts/)（51 条款：14 + 16 + 11 + 10）、[quickstart.md](../quickstart.md)、[research.md](../research.md)、[feature-ref.md](../feature-ref.md)、[notes/](../notes/)
**Depth / Audience / Focus**: Standard-plus（风险优先）/ Reviewer / ① 映射真实性 ② 台账、迁移与分发的可执行判据 ③ 度量仪器口径

**Note**: 本清单由 `/speckit.checklist` 生成，用于校验 **需求（What）** 的质量。**规格（How）** 只在两种情况下被引用：暴露需求缺口 / 歧义 / 冲突，或核对关键设计决策能否回溯到需求——不用于测试实现行为。

**Same-author gate**: 本运行无子代理派发工具，按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 降级为直接有界复核（`detected: direct read, subagent unavailable`）。补偿措施：本清单出现的一切事实前提均由本轮命令重新测量（见下表），不沿用 069b 文档内的既有数字。

**勾选语义（本次评审的 disposition）**：`[x]` = 要求本身成立，且（如原为问题）已在规格中处置并留可复算证据，行尾以 `→ 已核:` / `→ 已处置:` 标注；`[ ]` = 仍待处置但**必须带 disposition**：`→ disposition: verify-in-implementation: <核对点>` 或 `→ disposition: out-of-slice: <理由>`。本清单**不允许**无 disposition 的 `[ ]`。

---

## 实测前提（本轮重测，2026-10-25，HEAD `84dd63e5`）

| Premise | Re-derivation | 实测值 |
|---------|---------------|--------|
| 流程单元 / 台账分母 | `ls templates/commands/*.md \| wc -l`；`ls -d skills/external/*/`；`ls -d skills/internal/*/`；`comm -12 <(ls skills/external) <(ls skills/internal)` | 27 / 14 / 37 → 78；`comm -12` 空（零同名） |
| 契约条款 | `grep -ohE '^\- \*\*C-[0-9]+\*\*' contracts/*.md \| wc -l` + 逐文件 | 51 = 14 + 16 + 11 + 10，编号连续 |
| FR / SC / STR / 任务 | `grep -cE '^\- \*\*FR-\d+\*\*'` / 同法 SC / STR / 任务行 | 14 / 5 / 3 / 29（3 + 6 + 4 + 10 + 6） |
| 8 支新测试 | 逐个 `test -e` | 8/8 ABSENT（红先前提） |
| 阶段名册 | `STAGE_ARTIFACTS` 顶层键 | 8：requirements / clarify / plan / tasks / checklist / analyze / implement / review |
| 六面 + 阶段算子 | `expression-gates.md` 二级章节 / § 六面 / § 阶段算子表 | 16 章节；6 面；16 行；blocking 按阶段 2/2/2/2/2/2/1(+1 advisory)/2 |
| 委托边 | 模板正则 `(?:\.specify/)?skills/(?:external/\|internal/)?<name>/SKILL.md` + 台账比对 | 26/27 模板有边；41 条边；0 类不一致；6 条类中立豁免；类中立清单 5 成员 |
| 六面 owner 路径 | `doc-consistency-check.py` 的 `OWNER_PATHS` + 锚 grep | 9 条路径（6 个绑定格）；5 个 `§` 锚全部命中 |
| 台账 / mixed-oracle | owner 台账行 + `basis` 列 | 78 行；8 行 `mixed-oracle`，全部 `execution` |
| 「069b 承接」 | `grep -n '069b 承接'` / `grep -c '由 069b 承接'` | 12 处；`由 069b 承接` 3 处（`:19` `:35` `:88`） |
| 分发路径 | `pyproject.toml` / `src/specify_cli/__init__.py` / `src/hatch_build.py` | `:34 scripts`、`:37 shared`；`:2462` shared 复制段；`:42 _stage_skills` |
| 镜像 / 命令副本 | `sync-mirrors.py --check`；`regen-command-copies.py --check` | 六对 ok + 命令副本 OK（两次 exit 0） |
| 结构面 | `docs-utils.py --action validate --root .` | 3 violations（broken-link 2 + note-frontmatter 1） |
| 被否决备选 | `test -e shared/definitions/isomorphism-map.md` | ABSENT |
| 三个客户快照 | `git -C <p> rev-parse --short HEAD` / `branch` / `test -f owner` | `3f68b62@master`、`a0c476d@xuanji/develop`、`a2fad18@main`，三者 owner=no |
| 度量通道 | 四条命令 `--help` / 实跑 | exec-quant `list-records --since`、feedback-utils `list --since`、run-determination `history --target`、`git log --format=%as` 全部存在 |
| 预装 `specify` 包 | `ls .../profiles/.venv/.../specify_cli/shared/{definitions,workflow}/` | 无 `flow-class-definitions.md`、无 `expression-gates.md`（包旧于 069a；不可作刷新入口） |
| 自建 wheel 载荷 | `pip wheel . --no-deps --no-build-isolation` + 解压检查 | wheel 含 `flow-class-definitions.md` / `expression-gates.md` / 两个引擎；27 命令 / 51 技能 |
| 刷新探针 | xuanji-agent 快照 + `specify init . --here --force --ai claude --no-git --ignore-agent-tools` | 四载荷到位（owner / expression-gates / 两个引擎）；27 命令 / 52 技能（含项目自有 1） |

## Validators（本轮实跑，规格修正后）

| Gate | Command | Result |
|------|---------|--------|
| requirements | `python3 scripts/python/validate-requirements.py <slice>/requirements.md` | `status: ok`；五项全 pass；0 error / 0 warning；284 行 / 19 定义行 / 3 STR |
| tasks | `python3 .specify/scripts/python/validate-tasks.py <slice>/tasks.md` | PASS；0 error / 0 warning |
| pre-analyze | `pre-analyze-check.py --spec-dir <slice> --stage requirements\|plan\|tasks --repo .` | 三阶段均 `decision=pass`、errors=0、advisories=27（18 处未创建测试文件引用：8 个文件在 tasks/feature-ref 的 10 + 8 处；5 处 plan/tasks/research 的被否决备选路径；本清单自身的 4 处同类引用：1 个客户测试路径 + 3 处被否决路径）、waived=0 |
| decomposition | `decomposition-check.py --mode plan\|tasks` | 两次 `proceed`：fr_count=14；task_count=29 ≤ 40 |
| 条款覆盖 | `account-clause-coverage.py <slice>` | claimed=51；FR 14/14 cited、0 uncovered；`status: ok`（基线于 2026-10-25 analyze 轮冻结：495 条基线内 / 0 beyond-baseline；此前一轮记 `baseline-missing` 时基线的冻结义务在 tasks 阶段，已补齐） |
| 进程观察 | `bash scripts/bash/check-prerequisites.sh --json` | 因分支前缀 `069` 解析到父规格 `069-execution-expression-sdd`（切片共用数字前缀），本清单直接使用绝对路径 `.specify/specs/069b-isomorphism-migration-metrics`；属框架工具对切片分支的既有局限，不是 069b 需求缺陷 |

## 本清单运行所做的必要规格修正（不实现代码）

| # | 文件 | 修正 | 触发项 |
|---|------|------|--------|
| 1 | `requirements.md` | SC-001 增「标注失真的行 = 0」（`annotation-false-enforced` / `annotation-false-unenforced`） | CHK005 |
| 2 | `requirements.md` | SC-002 Source 改为「按套件原生失败输出提取 nodeid 名集」；`--names-out` 只留作框架仓通道 | CHK027 |
| 3 | `requirements.md` | SC-004 增「独立 = 不同的人 / 会话 / 互不可见，结论分别落盘」 | CHK017 |
| 4 | `requirements.md` | SC-005 Source 的「六个 owner 路径」更正为 S3 比较集 9 条路径 / 6 个绑定格 | CHK021 |
| 5 | `requirements.md` | FR-006 点名刷新入口（`specify init` 覆盖式合并；无独立 refresh 子命令） | CHK023 |
| 6 | `contracts/ledger-reconciler.md` | C-5 的重复版本声明改为复用 `row-malformed`（不新增第六个 check kind） | CHK016 |
| 7 | `contracts/ledger-reconciler.md` | C-8 / C-11 增 `commands_scanned` / `faces` 顶层字段；C-9 / C-12 封闭扫描范围；C-13 改为 9 条 owner 路径；C-14 补 owner 同时缺失时的优先级 | CHK016 / CHK020 / CHK021 / CHK023 |
| 8 | `contracts/measurement-instruments.md` | C-2 的 clarify 轮次仪器改为「仅在存在 clarify 运行记录时取 `grep -c '^- Q:'`；自裁决 Q/A 记 0」 | CHK033 |
| 9 | `contracts/migration-distribution.md` | C-2 / C-7 / C-8：点名 `specify init` 安装器入口并要求刷新包由本切片源码构建 wheel（预装 CLI 包内无 069a 载荷）；客户套件按原生输出提取；禁止人工 `cp` | CHK023 / CHK027 / CHK028 |
| 10 | `tasks.md` | T011 的「12 行统一指向 C-7」更正为三类处置（P2 删除 / P3 重写 / P4 的 10 处指向 C-7）；T012 删除「同一发行包载荷复制」并改为「自建 wheel + 临时 venv」；T014 重复版本按 `row-malformed`；FR-010 覆盖补 T018 | CHK016 / CHK023 / CHK028 / CHK034 |
| 11 | `plan.md` / `research.md` / `data-model.md` / `feature-ref.md` / `quickstart.md` / `notes/migration-samples.md` | 同步上述口径；补 069a fixture 的 A-1 例外；`notes/migration-samples.md` 追加「2026-10-25 跑测机制更正」（`.venv` 不在 archive、editable 安装、原生 name 提取、自建 wheel、`specify init` 全参） | CHK021 / CHK022 / CHK027 / CHK028 / CHK036 |

---

## A. 映射载体、行集与 24 格

- [x] CHK001 映射的 8 个阶段行是否被要求等于既有名册 owner（`loop-state.py` 的 `STAGE_ARTIFACTS`）的键集，且名册不可解析时有具名失败、并明确禁止第二份名册或映射自带版本？[Completeness, Req §FR-001; contract C-2] → 已核: 实测 8 键；C-2 定 `roster-unavailable` 与「不得用内置列表冒充」；research R2 记被否的「映射自建阶段清单 / 加 `version`」。
- [x] CHK002 映射与边界的载体是否唯一落在分类所有者，且 069a 的交接行被**实体章节**取代、owns 列表同步——而不是新建第二份文档或复制一份映射？[Consistency, Req §FR-001 / §FR-009; C-1] → 已核: 实测 `shared/definitions/flow-class-definitions.md:19` 交接行；`shared/definitions/isomorphism-map.md` ABSENT；T006 删除交接行并加 owns 两项；`contracts/isomorphism-map.md` 只是契约形态，tasks §Path Conventions 明示不得与映射副本混淆。
- [x] CHK003 24 格是否被要求每格同时写出代码型与文档型两侧，并有可判定的格语法（恰好一个 `↔`、两侧各 ≥ 8 字符），而不是只以「8 行 × 3 列」计数成立？[Clarity, Req §FR-001; C-3] → 已核: FR-001 写 8 × 3 = 24 且每行是「代码型产物 ↔ 文档型产物」；C-3 把每格语法与 `cell-malformed` 固定，并要求三面含义由表前 legend 声明一次（不在 24 格重复）。

## B. 强制标注的真实性

- [x] CHK004 「实际强制」是否有可观测结构定义——每个被点名的 `(阶段, face)` 在门禁 owner § 阶段算子表存在 `blocking` 行，且 advisory-only 或「别阶段有 blocking」不被接受？[Measurability, Req §FR-002; C-5 / C-6] → 已核: FR-002 要求标注反映实际；C-5 / C-6 把实际落到 16 行算子表的 blocking 存在性；实测 8 阶段均有 blocking（implement 为 1 blocking + 1 advisory），research R4 记该代理与被否的人工判断方案。
- [x] CHK005 「标注失真」是否被一条可测量的成功判据覆盖，而不只停留在 FR-002 的规范句（SC-001 原先只数「未标注行」）？[Coverage, Req §SC-001] → 已处置: SC-001 增「标注失真的行 = 0（`annotation-false-enforced` / `annotation-false-unenforced`）」；feature-ref §2 的 SC-001 判据同步；`--action isomorphism` 的 findings=0 测量源已覆盖两类失真。
- [x] CHK006 `slogan-row` 是否是要求级缺陷，`已声明未强制` 是否只是如实标注而非豁免——并写明当前树上没有阶段能合法取该值？[Consistency, Req §FR-002 / §SA-8; C-6 / C-7] → 已核: FR-002 把失真行与未标注行同等处理；C-7 定口号行；SA-8 明确「不是通过、不是新增许可、不免除既有门禁」；实测 8 阶段都有 blocking，故真实树 8 行都 `已强制`，另一取值由 fixture 覆盖（R4），不空转。

## C. 不可同构边界

- [x] CHK007 四类边界（a–d）是否各恰好一次，且四个轴（验收 oracle / 验证算子 / 失败可见性 / 语义 oracle）被固定？[Completeness, Req §FR-003; C-8] → 已核: FR-003 列四项；C-8 定逐字表头、`a`–`d` 各一次、缺/重 → `boundary-missing`、空「为什么」→ `boundary-malformed`。
- [x] CHK008 「至少一处门禁设计指出对应处理」是否被量化为「≥ 1 个封闭 face id + 处理说明」，且只写 face id 的行被拒？[Measurability, Req §FR-003; C-9] → 已核: C-9 要求 face id + 处理说明；无 face id → `boundary-unbound`，只写 id 无说明 → `boundary-malformed`；语义是否充分归评审面（C-10 明说检查器不判自由文本）。
- [x] CHK009 映射与边界是否被要求同属一个 owner 文档，并对「拆成两份各自漂移」定义缺陷？[Consistency, Req §FR-003; C-1 / C-9] → 已核: FR-003 明写同属一个所有者文档；C-1 断言唯一载体；C-9 记 `boundary-split`；T006 的 owns 列表同步覆盖两项。

## D. 判据非移植与主张落地

- [x] CHK010 「不得整套移植代码型门禁」是否被机械封边（代码型算子闭集），且跨类复用必须指名复用的**不变量**而非复用判定算子？[Clarity, Req §FR-004; C-11] → 已核: C-11 闭集 `pytest` / `--cov` / `coverage` / `go test` / `mvn test` / `npm test` / `jest`；FR-004 点名契约、证据、所有权、版本等不变量；T007 对阶段算子表做只读闭集扫描。
- [x] CHK011 「同构主张必须落到一行（阶段 + 面）或一条边界」是否可判定，机械下限是否够用，剩余语义判断是否显式交给评审面？[Measurability, Req §FR-005; C-10 / C-12] → 已核: FR-005 以「能否指向一行或一条边界」判定，不按措辞；C-10 给三个下限（24 格两侧成对 / 模板与技能的许可句闭集 / 介质短语闭集）并明说检查器不声称能判自由文本；C-12 把介质判据短语闭集化。

## E. 台账形态与生效版本

- [x] CHK012 台账是否是所有者内的一份声明式行集，列按表头名解析，且禁止用命令模板元数据或技能 frontmatter 等分散载体承载类别？[Completeness, Req §FR-010; C-6] → 已核: 实测 78 行（27 命令 + 51 技能）；表头含机器键 `flow_class`；C-6 沿用 069a 的按表头解析、不新增必选列；FR-010 明写分散载体即第二副本。
- [x] CHK013 反空真下限是否是**解析侧**下限、与被检查台账自身无关、且与 069a 的**清单侧**下限并存；下限的维护规则是否写明？[Clarity, Req §FR-010; C-1] → 已处置: 2026-10-25 analyze 轮把 C-1 的下限从「期望行数 78」改为由清单侧 floor 推导的 `LEDGER_FLOOR = ⌊(27+51)/2⌋ = 39`——78 会让「删一行」同时触发 `ledger-truncated`，使 SC-003 两种注入都落 `parse-failure`（两红不可区分），并破 069a 的 `test_missing_ledger_row_reports_missing`（77 行、断言 `kinds ⊆ EIGHT_KINDS`，本切片不得改写）；下限仍不取自被检查台账、仍与 `inventory-truncated` 并存，完整性由 C-2 的 `matched == inventory_units` 承担；T014 / T018 / T019 与 data-model E5 已同步。
- [x] CHK014 生效版本是否只在所有者内声明一次，且与 069a 的「表头 / 列集合与解析器期望不符 = 版本不兼容」判据兼容——没有行级版本列、`version` 字段或第三个版本信号？[Consistency, Req §FR-010; C-5] → 已核: C-5 固定 `**台账版本**: <整数>（<YYYY-MM-DD>）` + 既有 `## 变更记录`；T019 落一次；plan R6 记被否的行级 `effective_version` 列；C-5 明禁 `version` 字段 / 行级列 / 第三信号。

## F. 对账红、覆盖率与混合 oracle

- [x] CHK015 「缺口」与「解析失败」是否被定义为两种不同的红，带优先级与退出码，且「静默绿」在构造上不可能？[Measurability, Req §SC-003; C-2 / C-3] → 已核: C-3 五值优先级 `owner-unavailable > framework-source-required > parse-failure > gap > clean` 与退出码；C-2 的 `clean` 充要条件（`matched == inventory_units`、`gaps == 0`、`parse_errors == 0`、`ledger_rows ≥ floor`）；T014 双注入。
- [x] CHK016 每个 finding kind 是否恰好落进一个红桶，使 `clean` 不可能与 findings 共存——包括「重复的版本声明」？[Consistency, Req §FR-010; C-2 / C-3 / C-4] → 已处置: C-5 的重复版本声明改为复用 `row-malformed`（不新增第六个 check kind，计入 `parse_errors`），使 C-4 的「恰好五个新 kind」、C-2 的 `parse_errors` 与 data-model E5 的 `clean` 不变量闭合；T014 同步为「声明重复（按 `row-malformed`）」。2026-10-25 analyze 轮补齐此前漏掉的一个 kind：`inventory-truncated` 原不在任何桶内（在「台账与清单同时截断」的夹具上会算出 `red_kind = clean` 而 findings 非空），C-3 已改为「`gap` 集合之外一律 `parse-failure`」的穷尽划分，并写明新增 kind 必须落桶。
- [x] CHK017 混合 oracle 的规范正文是否在本切片（不是只留指针），并同时定义台账一致性（`basis: mixed-oracle ⟹ flow_class: execution`）、只按消费方与失败可见性判定、以及两名判定者的「独立」含义？[Completeness / Measurability, Req §FR-011 / §SC-004; C-7] → 已核: FR-011 是本片规范正文；C-7 定台账一致性且不看数量比例 / 文件类型；实测 8 行 `mixed-oracle` 全部 `execution`；SC-004 增「独立 = 不同的人 / 不同的会话 / 判定时互不可见，结论分别落盘后比对」。

## G. 委托核验与类中立

- [x] CHK018 委托关系是否由命令模板里可解析的语法定义、同模板同名去重，且人工维护的「命令 → 技能」清单被明确排除为核验依据；`delegation-hand-list` 的扫描范围是否封闭？[Clarity, Req §FR-012; C-8 / C-9] → 已核: C-8 定语法与 `skill:<name>`；C-9 禁止人工清单（≥ 3 行成对表 → `delegation-hand-list`）并把扫描范围封闭为 `shared/` + `templates/commands/` + `skills/` + 本 spec formal artifacts；实测 27 模板 26 有边、41 条边、0 类不一致、6 条类中立豁免；`/speckit.tools` 无边不产 finding。
- [x] CHK019 类中立清单是否封闭、成员判据是否写明，且类中立不免除任何门禁、也不改变该单元自身的类别键？[Completeness, Req §FR-012; C-9 / C-10] → 已核: 所有者清单 5 成员（`memory-record` / `memory-recall` / `manage-feedback` / `collect-evidence` / `archive-session`）；C-10 明写封闭、不免门禁、不改键；FR-012 的成员判据是「交付物被两类流程共同消费且无类特定验收」。

## H. 六面绑定与判据不搬家

- [x] CHK020 六面是否每面要求恰一个 owner 指针，格内 `+` 连接仍算一个绑定，且带 `§` 的锚必须在目标文件可解析？[Completeness, Req §FR-013; C-11] → 已核: 六面表 6 行；实测 9 条 owner 路径（`requirements-clarity` / `structure-links-build` / `review` 各含 2 条），5 个 `§` 锚全部命中；C-11 定 `faces-count` / `faces-duplicate` / `faces-pointer-missing` / `faces-unresolvable`；C-8 / C-11 补 `commands_scanned` / `faces` 顶层字段，与 quickstart / tasks 的期望对齐。
- [x] CHK021 「六面之外的第二绑定表」扫描范围是否封闭，SC-005 的排除集是否是实际的 S3 比较集（6 个绑定格 = 9 条 owner 路径）而不是「六个路径」，duplicate 面的主体集是否同样封闭？[Consistency / Measurability, Req §SC-005; C-12 / C-13] → 已处置: C-12 增扫描范围；C-13 / SC-005 Source / quickstart / T016 / research R10 把「六个 owner 路径」更正为「S3 比较集：9 条路径 / 6 个绑定格」，与 `doc-consistency-check.py` 的 `OWNER_PATHS` 实测一致；C-13 要求主体集只含 owner 文档与本 spec formal artifacts，不是全仓 grep。

## I. 未刷新 / 刷新与分发

- [x] CHK022 「未刷新行为不变」是否建立在可核验的「零新增调用点」论证上（模板与技能零改动 + 调用点表零改动），而不是一句声明？[Completeness, Req §FR-006; C-1 / C-3] → 已核: 实测 `templates/commands/` 27、技能 51；本切片零模板 / 零技能改动；`expression-gates.md` 调用点表 W1–W4 零改动；四个新动作未登记为任何调用点；`regen-command-copies.py --check` OK。
- [x] CHK023 刷新是否被要求从**同一个发行包**一次带来四类载荷，部分刷新是否被具名降级，且刷新入口是否被点名（不存在独立 refresh 子命令；且该发行包必须由本切片源码构建，不能是预装旧 CLI）？[Consistency, Req §FR-006 / §FR-008; C-2 / C-5] → 已核: C-2 / C-5 四类载荷同包；C-5 要求刷新包由本切片源码构建 wheel（实测预装 CLI 的包内无 069a 载荷）；C-2 的「有新引擎无新 owner」不是受支持态（`lookup` → `owner-unavailable`；框架源动作 → `framework-source-required`）；C-14 补「owner 同时缺失时按 C-3 报 `owner-unavailable`」；FR-006 增 `specify init` 覆盖式合并入口；实测 CLI 只有 init / check / render-agents。
- [x] CHK024 分发是否限定为既有路径（force-include + shared 复制 + hatch skills 阶段），且「零项目侧存储 / 读取点」是否完整覆盖路径、缓存、索引、注册表？[Dependency / Completeness, Req §FR-008; C-4 / C-5] → 已核: 实测 `pyproject.toml:34 scripts`、`:37 shared`、`src/specify_cli/__init__.py:2462` shared 复制段、`src/hatch_build.py:42 _stage_skills`；C-4 禁止项目侧新增路径 / 数据文件 / 缓存 / 索引 / 注册表；`--action lookup` 是唯一面向客户运行时的读取入口。
- [ ] CHK025 客户项目那份分类副本的「漂移检查」是否被指定了 owner 与仪器，还是只有框架源 ↔ 镜像的检查？[Gap, Req §FR-008] → disposition: **out-of-slice**（2026-10-25 review-fix F9 由 `verify-in-implementation` 改判）: 本切片范围内的漂移检查只有框架源 `sync-mirrors.py --check`（六对 ok 实测）；客户副本由 `specify init` 整文件覆盖，C-4 禁止新增客户侧检查器。实现期未、也无法在本切片内关闭该项——它是**需求缺口**（FR-008 没有指定客户副本的检查 owner），不是实现缺口。转交记录：owner = 后续修订 FR-008 的特性（尚未立项）；登记编号 `OI-069b-01`（`.specify/memory/register.md`）。解除条件 = 该特性为 FR-008 指定 owner 与仪器，或明确豁免。本项保持 `[ ]`，**不冒充完成**。

## J. 客户快照与名字级判据

- [x] CHK026 三个客户快照是否在跑测前冻结，且字段（项目 / HEAD / 分支 / 脏文件数 / 载荷状态 / 套件命令）齐备、满足「未刷新 + 套件可启动 + 可从提交复现」？[Completeness, Req §SC-002; C-6] → 已核: `notes/migration-samples.md` 三行字段齐备（`3f68b62@master` / `a0c476d@xuanji/develop` / `a2fad18@main`；脏 195 / 548 / 28；owner=no）；实测三者 `.specify` 存在但 owner / engine 不在位；SA-12 要求事先落盘。
- [x] CHK027 名字级判据是否按套件类型定义，且框架仓专有的 `--names-out` 是否已从客户套件路径移除？[Clarity, Req §FR-007 / §SC-002; C-7] → 已处置: SC-002 Source、C-7、plan、feature-ref、data-model、research、notes 均改为「按套件原生失败输出提取」——pytest `FAILED <nodeid>`、Go `go test -json` 的 fail 事件 `<package>::<Test>`；`run-tests.sh --names-out` 只保留为框架仓基线通道。
- [x] CHK028 快照是否真的与原始工作树隔离，且刷新调用是否被精确指定（`.venv` 不在 archive、editable 安装指向原项目）？[Dependency, Req §FR-007; C-8] → 已处置: 实测 `git archive` 不含 `.venv`（两个 Python 项目的 `.gitignore` 排除它）；`xuanji-agent` 的 venv `.pth` 指向原项目 `src`，未设 `PYTHONPATH` 时快照测试导入原工作树（实测两条 import 路径：原项目 → `~/tmp/069b-probe-snap-1/src`）；`notes/migration-samples.md` 追加「2026-10-25 跑测机制更正」，固定「原项目绝对解释器 + `PYTHONPATH=<snapshot>/src`」并用 `tests/test_adapter_contract.py` 4 passed in 2.23s 实测；刷新包由本切片源码构建 wheel（预装 `specify` 的包内无 069a 载荷），`--target` 暂存后用 profiles 解释器 + `PYTHONPATH` 运行 `specify init`——实测 wheel 含四载荷、init 后快照四载荷到位（27 命令 / 52 技能，含项目自有 1）；C-8 / T012 同步。
- [x] CHK029 降级规则是否显式且不可替代（`not-evaluated` + reason；禁止人工拷贝冒充刷新；框架仓基线不等同客户快照基线）？[Edge Cases / Consistency, Req §FR-006 / §FR-007; C-8 / C-9] → 已核: C-8 两条降级（套件缺未跟踪文件 / `specify init` 不可执行）；C-9 明写两类基线对象不同、不得互相顶替；tasks A-4 与 T012 同步为「不记 0、不以人工 `cp` / 逐文件复制冒充刷新」。

## K. 三项度量仪器

- [x] CHK030 三项量与冻结点是否定义清楚、共用同一起点，且记录的行 / 量关系（`confirmations` 拆两行）是否写明？[Completeness, Req §FR-014; C-1 / C-4] → 已核: C-1 三项 + 冻结点 `f0df3d0b`（author date `2026-10-24`）；C-4 两分项分别记录；`notes/expression-baseline.md` 4 行（gate_calls / confirmations × 2 / wall_clock），每行 7 字段。
- [x] CHK031 仪器是否封闭于既有通道、没有新增采集器 / 插桩 / 手工补采？[Consistency, Req §FR-014; C-2 / C-10] → 已核: 四通道命令实存（exec-quant `list-records --since`、feedback-utils `list --since`、run-determination `history --target`、`git log --format=%as`）；C-10 禁止统计系统 / 评分体系 / 第二份基线；research R14 记被否的「新建映射台账 JSON / 度量采集脚本」。
- [x] CHK032 `gate_calls` 的过滤集合是否事先冻结并带归属规则，脚本级检查这类不可计部分是否被写明而不是记 0？[Measurability, Req §FR-014; C-3] → 已核: C-3 冻结 6 个检查类单元 + `run_id` 含 `069b`；baseline 窗口 6 条记录、检查类 2 条全部属 069a → 本片冻结 0；「不可计部分」（pre-analyze / validate / doc-consistency / decomposition / coverage / 测试）写明不是 0。
- [x] CHK033 `confirmations` 是否拆成门控观察与 clarify 轮次并排除自裁决 Q/A，`wall_clock` 是否定义两端与缺失时的 null 规则，`not-evaluated` 是否与 SC 五值词表互不顶替？[Clarity / Consistency, Req §FR-014; C-4 / C-5 / C-7 / C-9] → 已处置: measurement C-2 的 clarify 仪器改为「仅在存在本切片 clarify 运行记录时取 `grep -c '^- Q:'`；无记录或自裁决 Q/A 记 0」，与 C-4 一致；C-5 起点 / 终点 / null；C-7 五值 SC 词表不互替；C-8 verdict 仅 `not-evaluated|measured`；C-9 收尾同口径同集合同窗口。

## L. 覆盖、任务契约与事实一致性

- [x] CHK034 14 FR / 5 SC 是否都映射到至少一个任务，51 条款是否每条恰好被认领一次且每契约内单调，29 个任务行是否每个要么被映射、要么被声明为流程行？[Traceability, Req §FR-001–§FR-014 / §SC-001–§SC-005] → 已处置: FR-010 覆盖补 T018；实测 51 条 `[green:]` 唯一、每契约单调递增、无重复；14 / 5 全部有映射；T018 原为唯一既未映射也未声明为流程行的任务。
- [x] CHK035 8 支新测试是否被要求先红、红形态是「动作 / 章节缺失」而非 import / collection error，Tests Mode ON 是否由可执行引擎扩展正当化而非 template-only 门？[Measurability, Constitution IV; tasks §Tests Mode] → 已核: 8 个测试文件（6 契约 + 2 单元）；tasks §Tests Mode ON 并写明理由；T004 / T005 / T010 / T014–T018 逐支红跑并写 `notes/red-first-evidence.md`；红形态明文禁止 import / collection error。
- [x] CHK036 Feature 069 是否保持 `Planned`（069a Implemented / 069b 进行中）、069a 是否除 A-1 的一行 fixture 外零改动、被否决的 `shared/definitions/isomorphism-map.md` 是否仍不存在，且文内计数（78 / 51 / 29 / 14 / 5 / 3 / 6 / 16 / 26-27 / 6 / 9）是否与实测一致、plan 的 `advisories=9` 与正文 10 是否已披露？[Consistency, Req §SA-5 / §SA-6; tasks §Path Conventions] → 已核: 清单阶段实测 `features.md` 069 = `Planned`；069a 规格 / 测试 `git status` 干净；A-1 仅允许 `_render_owner` 补一行版本声明（feature-ref §3、plan §4 已同步）；`shared/definitions/isomorphism-map.md` ABSENT；实测计数与文内一致；T011 的「12 处」更正为三类处置（P2 删除 / P3 重写 / P4 的 10 处指向 C-7）；plan 的 `advisories=9` vs 正文 10 已由 tasks §Generation-time premise corrections 披露，且当前重跑三阶段均为 27（tasks.md 与本清单已存在，属分母变化，非载荷错误）。**状态更新（2026-10-25 review-fix F2/F3）**：本项的两个前提已随时间失效——(a) 索引状态按 Pre-Status-Flip 门推进为 `Implemented`（069a/069b 均 Implemented，见 `features/069.md` § Slice-aware status）；(b) 069a 的测试被触碰第二处——`tests/contract/test_expression_gates_doc.py` 的仪器断言（授权与证据见 `tasks.md` § 跨切片一致性修正登记）。

---

## Notes

- `[x]` 项的行尾 `→ 已核:` / `→ 已处置:` 是可复算证据或本轮已落的规格修正；`[ ]` 项只有一条（CHK025），
  disposition 为 **`out-of-slice`**，已转交 `OI-069b-01`（`register.md`），不冒充完成。切片收口时对账见
  `verification.md` § Checklist 收口对账。
- 本清单不评判实现好坏：`--action isomorphism` / `delegation` / `faces` 的实际绿跑、三快照的 `comm -13`、双注入的 `red_kind` 属实现期取证（tasks T009 / T012 / T023 / T026 / T027），本清单只核对它们的判据、样本与非替代关系是否已经写死。
- 069a 的**规格与判据正文**零改动；069a 的测试文件触碰两处——`tests/unit/test_flow_class_check.py` 的 `_render_owner`
  补一行 `**台账版本**`（tasks A-1 的披露边界），与 `tests/contract/test_expression_gates_doc.py` 的仪器断言重编码
  （2026-10-25 review-fix F2 更正：原「唯一触碰是 A-1」不成立；授权见 `tasks.md` § 跨切片一致性修正登记）。
- 本清单运行未修改任何实现、模板、技能或 `.specify/` 镜像；规格修正只落在本切片的 requirements / plan / research / data-model / contracts / tasks / quickstart / feature-ref / notes。清单项本身在 2026-10-25 review-fix 轮按 F9 / F2 / F3 就地更正 disposition 与两处过期前提，未改任何判据。
