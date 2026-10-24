# Phase 0 Research — 069a Flow Classification & Document-Form Gates

**Phase 0 output** (`/speckit.plan`, 2026-10-24). 本文件只记录**决策与其可复算证据**；判据正文归各自 owner，本文件不复制。

**证据路径**: 本运行无子代理派发工具（无 Agent/Task 工具可用），同作者检测门按
`.specify/shared/workflow/objective-analysis-gate.md` § 7 降级为**直接有界复核**，标记
`scored: direct read, subagent unavailable`。全部事实以仓库文件 + 实跑命令为准，行号/路径可复查。

---

## R1 — 分类所有者：单一文件、单一目录

**Decision**: 所有者落在 `shared/definitions/flow-class-definitions.md`；不新增第二个分类数据文件。

**Evidence**:
- 目录惯例：`shared/definitions/` 现有 10 份 `<域>-definitions.md`（`ls shared/definitions/` 实测：agent / contract-clause / derivation / dogfooding / framework-map / goal / probe / self-improvement / subagent / tool）。
- 落点已由 clarify 裁定并写入 `.specify/memory/features/069.md` § Implementation Notes；
  `.specify/memory/glossary.md` 的两行（`流程分类 (Flow Class)` / `执行类流程`）已把该路径登记为 owner。
- `shared/definitions/framework-map.md` 只按**目录**描述 `.specify/shared/`（第 21 行），不逐文件登记，故新增定义文件不需要改该 map。

**Rejected**: 放进 `shared/workflow/`。理由：workflow 目录拥有的是可执行步骤（如 `evidence-step.md`），分类是**定义性事实**，与 `tool-definitions.md` 同类。

---

## R2 — 两个取值，类中立不是第三个取值

**Decision**: 台账每行 `flow_class ∈ {execution, expression}`；**类中立**是「豁免命令↔技能同类约束」的封闭清单，
不引入第三个类别值。

**Evidence**:
- FR-008（每个流程单元恰好属于一类，双命中/双落空为缺陷）与 FR-010（命令与其委托技能同类，例外仅限封闭的类中立清单）若用第三值实现，会同时违反 FR-008 且让「未声明默认」的取值域不再是二值。
- 机械事实：命令↔技能委托关系可解析（`grep -o 'skills/\(external\|internal\)/[a-z0-9-]*/SKILL.md' templates/commands/*.md` 实测，27 个模板中 25 个显式声明委托技能；`humanize.md` 用 `.specify/skills/humanize/SKILL.md` 形式，解析器必须同时接受两种前缀）。
- 交叉验证：`skills/external` 14 个与 `skills/internal` 37 个目录**无同名冲突**（`comm -12` 输出为空），故 `skill:<name>` 作为单元 id 在两类层间唯一。

**Rejected**: `flow_class: neutral`。会让「恰好两类」在数据层不成立，并迫使每个读取点处理三值。

---

## R3 — 台账形态：所有者内手写声明式行集 + 确定性对账

**Decision**: 台账是 owner 文件内的一张 Markdown 表（一行一个流程单元），由 `flow-class-check.py` 解析并与流程单元清单机械对账；不引入 YAML/JSON 侧车文件。

**Evidence**:
- 先例：`.specify/specs/027-feedback-mechanism/contracts/command-classification.md` + `tests/contract/test_feedback_command_classification.py`（`MIN_COMMANDS` 反空真下限、表完整与「没解析出行」可区分）。
- 规模实测（2026-10-24，本仓）：`templates/commands/*.md` = 27；`skills/external/*/` = 14；`skills/internal/*/` = 37 → **流程单元 78**。
- 反空真下限取实测值：命令 27、技能 51；清单扫描低于下限即报 `inventory-truncated`，使「缺口为 0 因为表完整」与「缺口为 0 因为没解析到」永远可区分（同 `MIN_COMMANDS` 纪律）。

**Rejected**: 单独 `flow-class.json`。会形成「判据在 A、数据在 B」的双文件所有权，且 JSON 无法承载边界例与判据叙述。

---

## R4 — 读取路径：解析引擎，不是模板内副本

**Decision**: 类别只能经 `scripts/python/flow-class-check.py --action lookup` 读取；命令模板与技能 MUST NOT 内嵌类别字面量。

**Evidence**:
- `templates/commands/docs.md` 有 `## Wrap-up`（第 54 行），`templates/commands/humanize.md` **没有** `## Wrap-up`（实测章节序列：User Input → Glossary → Outline → Handoffs）——把读取点挂在 wrap-up 上会让 humanize 不可读，正是 FR-015 的动机。
- 复杂度轴（决定 wrap-up 面有无）与类别轴正交：docs 复杂、humanize 简单，但两者同为表达类（FR-004；`shared/workflow/feedback-step.md` 开篇的复杂度判据）。
- 模板内副本无法与所有者同步（无生成步骤），属 `shared/guidelines/one-source-of-truth.md` § Reference, don't copy 明令禁止的重复形态。

**Rejected**: 在两份命令模板里各写一行 `flow_class: expression`。除了复制即漂移，还会把 062 的 C-1..C-10 表面断言（`tests/contract/test_humanize_command_surface.py`）暴露在无关改动下。

---

## R5 — 命名空间：`flow_class`，与 Agent Execution 消歧

**Decision**: 机器键 = `flow_class`；owner 内设 § 命名空间 小节；`execution` 取值只出现在 `flow_class` 上下文。

**Evidence**:
- 同词异义实证：`.specify/memory/glossary.md` 第 54 行 `Agent Execution`（Agent 三层分类法第三层）与第 173/177 行（`执行类流程` / `流程分类`）并存，后者已登记 owner 与机器键。
- 仓库占用实测：`expression` 与 `flow_class` 作标识符零占用（父 requirements § 现状锚点，2026-10-24 实测记录）。

**Rejected**: 裸 `class` / `type` 作键——与 Python 关键字和既有字段名冲突面过大。

---

## R6 — 六面门禁的落点：每面一个既有 owner，只补两面

**Decision**: 门禁算子集 owner = 新文件 `shared/workflow/expression-gates.md`；六面各自指向既有 owner，仅「证据分级与 as-of」「事实一致性」两面由本切片新增实现。

| 面 | 既有 owner（不改写） | 本切片新增 |
|----|---------------------|-----------|
| 需求清晰度 | `scripts/python/validate-requirements.py`（5 项结构检查）+ `shared/guidelines/requirements-guidelines.md` | 无（复用） |
| 读者/目的/边界 | `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议（基准读者唯一来源）；`skills/external/create-docs/SKILL.md` § Authoring Flow R0/R4（写作前必须回答受众） | 声明形态（可机械校验的两行） |
| 证据分级与 as-of | 无（新增面） | 语法与配对规则 |
| 结构/链接/构建 | `skills/external/create-docs/SKILL.md` § Desired-State Baseline + `scripts/docs-utils.py --action validate|fix-links`；站点层存在时 `improve-docs` § Verify 的构建 | 无（复用，且「构建通过≠内容正确」作为负向条款） |
| 事实一致性 | `shared/guidelines/one-source-of-truth.md`（判据） | 检查器 |
| 评审 | 既有 `/speckit.review` 流程 + `skills/internal/review-sdd-process` | 「按读者基准判定」的接口约束 |

**Evidence**:
- `docs-utils.py` 动作面实测：`scan / expire / clean / archive-check / stats / validate / fix-links`。
- 结构面基线实测（2026-10-24 本仓）：`docs-utils.py --action validate --root .` → exit 0，`violations=3`（`broken-link` 2 + `note-frontmatter` 1）。**基线不为零**，故结构面的判据只能写成「零**新增**」——写成「全绿」会在实现期撞上既有违规。
- 证据分词边界：`shared/workflow/evidence-step.md` 的七态词汇描述**机制证据**（机制存在/接线/被使用），`shared/guidelines/single-run-evidence.md` 描述**一次昂贵执行的记录留存**；二者都不是「文档断言的证据等级」，新增面 MUST NOT 重定义或收窄其取值域。

**Rejected**: 新建六份 guideline。四份既有 owner 已覆盖判据，重建即第二副本。

---

## R7 — 证据等级与 as-of 的语法（新面）

**Decision**: 等级取封闭三值 `实测 / 推断 / 引用`；`as-of` 取 ISO 日期 `YYYY-MM-DD`；**成对规则**——
一条事实性断言只要出现等级或 `as-of` 任一项，另一项必须同时出现。

**Evidence**:
- 判据可机械化的最小集合：三值封闭枚举可校验（不在集合内即 `grade-invalid`）；ISO 日期可解析；「成对」使「只写 as-of 不写等级」和「只写等级不写 as-of」都成为可报缺陷。
- `as-of` 的既有先例：`.specify/memory/glossary.md`「易变测量值」条要求基线值带时间；本切片把它收敛为单一语法，不新建第二套时间标记。

**Rejected**: 要求每句都标注。不可判定（什么算「事实性断言」是语义判断），会把门禁变成噪声源，违反「更少更准」。

---

## R8 — 事实一致性检查器：跨文件手写副本 + 计数委派

**Decision**: 新脚本 `scripts/python/doc-consistency-check.py`，三面（`reader` / `evidence` / `duplicate`）；
`duplicate` 面检测**跨文件归一化行重复**，`count` 面**委派**给 `pre-analyze-check.py` 而不重写规则。

**Evidence**:
- 注入式演练（SC-007）三类注入点中，「把一处引用改为手写副本」「把一处 as-of 改旧」都是**跨文件/时间戳**可判的；
  「把一处计数改为手打」正是 `pre-analyze-check.py` 既有 `COUNT_CLAIMS` 的判定对象（该脚本 docstring 明示 count claims disagreeing with actual definitions 属于其职责）。
- 委派可行：脚本实测存在两处（`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 与 `.specify/skills/...` 镜像），CLI 为 `--spec-dir --stage --json-out`。
- 归一化与排除项必须写死，否则同一语料会得出多个自圆其说的计数（与 `contract-clause-definitions.md` § 4 的教训同构）。

**Rejected**: 在检查器内重写计数比对。同一规则两个实现 = 必然漂移的两份真源。

---

## R9 — 三项基线的冻结与对照（FR-024）

**Decision**: 基线记录 = 表达式特性自己的 `<spec-dir>/notes/expression-baseline.md`（每特性一份、带 as-of 与冻结 commit），
三项值全部从**既有通道**导出；本切片不新增采集器。

**Evidence（命令实跑，2026-10-24）**:
- 门禁调用：`python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json` → 返回记录数组（exit 0），字段含 `unit_id` / `collected_at`，可按门禁单元集过滤计数。
- 单次运行判定：`python3 scripts/python/run-determination.py --action history --target /speckit.plan --limit 3 --json` → 返回 `target` + `counts` + `records[]`（含 `determined_at`），可作阶段完成时间戳与耗时来源。
- 人工确认：`feedback-utils.py --action record --lifecycle-point gate-<slug>` 是既有门控观察通道（`--action list --since` 可读）。
- 墙钟：`git log -1 --format=%cs -- <path>` 实测可用（本仓返回 `2026-10-24`）。

**Boundary**: 仪器口径与 `not-evaluated` 降级的**规范条款**是父编号 041，由 `069b` 承接；本切片只要求「开工前冻结、收尾逐项对照」，且基线缺失判为不可验收（FR-024）。前瞻样本不足 3 个真实表达类特性时记 `not-evaluated` 并说明原因，不记达成——该处置与 069b 的降级条款同向，但规范权归 069b。

---

## R10 — 分发与兼容

**Decision**: 新 owner 文档、gate 文档、两个引擎全部落**框架源**（`shared/`、`scripts/`），经 `sync-mirrors.py` 投影到 `.specify/`；
客户项目经既有 `specify init` 的 shared/scripts 拷贝获得，不新增项目侧存储。

**Evidence**:
- `scripts/python/sync-mirrors.py:82` `MIRROR_PAIRS` 实测：`shared → .specify/shared`、`scripts → .specify/scripts`（strict extras）、`templates → .specify/templates`（排除 `commands`）。
- `src/specify_cli/__init__.py:2462` 起为 `shared` 拷贝段；`pyproject.toml` 的 `[tool.hatch.build.targets.wheel.force-include]` 显式包含 `scripts` 与 `shared`。
- 镜像基线实测：`python3 scripts/python/sync-mirrors.py --check` → 六对全部 `ok`、命令副本 `OK`（exit 0）。故镜像判据可写「零新增漂移」。
- 未刷新项目行为不变：无任何命令/技能消费新引擎（R4 决定不改模板），因此客户项目里新引擎缺席时没有调用点。

**Rejected**: 在客户项目写入分类数据。与父 A7（旧项目不迁移、只降级）冲突。

---

## R11 — 测试面与基线

**Decision**: 契约测试四支 + 单元测试两支（清单见 plan § Test Strategy）；测试基线取**名字级**。

**Evidence（本机实测）**:
- 采集：`/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --collect-only -q tests` → `5361 tests collected`（exit 0）。
- 仓库 `.venv` 无 pytest（`No module named pytest`），本机唯一可用 pytest 在 `profiles/.venv`；该事实必须写进 plan 的 Technical Context，否则实现阶段会误以为 `python3 -m pytest` 可用。
- 静态交叉核对（不依赖 pytest）：`tests/` 下 `test_*.py` 文件 307 个，顶层 `test_*` 函数 2915 个；`tests/contract/` 189 个文件 / 1974 个函数（AST 统计，脚本见 plan § Test Strategy）。参数化使 collected 数大于函数数，两者都记录以免用错分母。

---

## R12 — 069a 自身的类别（自应用）

**Decision**: 069a 按自有判据属 **`execution`**：主交付物中包含必须被机器运行并观测行为的两个检查器（红/绿可判），
文档只是承载。不适用 FR-024 的三项基线（那是表达类特性的门禁成本口径）。

**Evidence**: 判据 = 主交付物的验收 oracle（FR-002）；本切片 SC-001/SC-002/SC-007 全部由**运行检查器**判定，属行为验收。
**Disclosed**: 若评审认为 069a 应按表达类自适用基线，则需在 069b 的仪器落地后补测——此处记为实现期可复核的前提，不静默略过。

---

## R13 — 脚手架偏差（in-passing 修复，已披露）

`bash .specify/scripts/bash/create-new-plan.sh --json` 在本分支解析出**父**规格目录
`069-execution-expression-sdd`（`common.sh` 的 `find_feature_dir_by_prefix` 只按 `069-*` 匹配，切片目录 `069a-*` 不在其 glob 内），
把模板复制到了父目录并新建了 `plan.md`。处置：删除该误生成文件（本运行创建、未跟踪、无下游依赖），
改为把 `.specify/templates/plan-template.md` 复制到切片目录。这是一次**纠正**而非决策：唯一符合记录意图的读法是切片计划必须落在切片目录。
副作用：本运行未使用脚本输出的 `SPECS_DIR`，改用显式路径；`CWS_LIB_BASH_HOME` 未在环境中设置也被如实记录（脚本需该变量才能启动）。

---

## R14 — 边界自查（不越界到 069b）

| 069b 条目 | 本切片是否触碰 | 处置 |
|-----------|----------------|------|
| 同构映射 8 行 × 3 面 + 四类不可同构边界（父 018–022） | 否 | owner 只留「本节由 069b 承接」的指针占位，不写映射行 |
| 迁移与分发机制（父 033–035） | 仅以「无新项目侧存储」的否定约束出现 | 细则不写 |
| 落地口径：owner 落点（036）、台账形态（037）、混合 oracle（038）、命令↔技能机械核验（039）、六面 owner 指针（040）、基线仪器（041） | **部分** | 036/037 已由 clarify 裁定并被本 plan 消费（不是重新裁定）；038 只以「按父 §Edge Cases 首条取 `execution`」的**指针**出现；039 的机械核验、040 的六面指针表、041 的仪器细则均留给 069b，本切片只给最小可执行面 |

**说明**: 上表「部分」行是对已裁定的**消费**，不是重新定义；若 069b 后续收紧口径，以 069b 为准。
