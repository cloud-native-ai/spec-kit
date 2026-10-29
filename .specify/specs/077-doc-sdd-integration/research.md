# Research: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Feature**: 077-doc-sdd-integration → Feature 077 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）
**Spec**: [requirements.md](requirements.md)
**Note**: 本文件只登记**形制裁决**（requirements § Assumptions A11 把「命令、退出码、字段子结构、检查器文件名、模板文本」留给 plan）与
其证据。语义、判据、取值与所有权归 requirements 与两份 owner；本文件不重定义、不复述。

所有「实测」行都在本次规划会话内以 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` 跑过，
原始输出落在 `test-evidence/`（文件名见各条 `Evidence`）。

## 实测基线（改动前）

| 项 | 实测 | Evidence |
|----|------|----------|
| `lookup --unit-id "spec:077-doc-sdd-integration"` | `invalid unit id`（stderr）+ `flow_class: execution` / `source: default` / `marker: null`，退出码 **2** | `test-evidence/plan-resolution-baseline.txt` |
| 正控 `lookup --unit-id "/speckit.implement"` | `execution` / `source: ledger` / `basis: mixed-oracle`，退出码 0（证明同一命令对既有键族确实生效，上面的红不是命令坏了） | 同上 |
| `doc-consistency-check.py --action structure` | `invalid choice: 'structure' (choose from 'verify')`，退出码 **2** | 同上 |
| 七个阶段模板的三类 token 命中数 | 七个全 `0`；正控 `docs 3` / `humanize 2` | `test-evidence/plan-stage-template-zero-hit.txt` |
| `sync-mirrors.py --check` | 退出码 **0**，六对全 `ok`（406 / 136 / 3 / 117 / 60 与 templates 对） | `test-evidence/plan-sync-mirrors-baseline.txt` |
| `regen-command-copies.py --check` | 退出码 **0**，全部 per-tool 副本与源模板一致 | `test-evidence/plan-regen-command-copies-baseline.txt` |
| 定向测试集（14 个既有测试文件） | **1015 passed**，退出码 0 | `test-evidence/plan-targeted-tests-baseline.txt` |
| `scan-confirmation-gates.py --summary` | blocking gates **27**（destructive 20 / governance_kept 7），violations 0 —— 该预算**零整数余量** | 见 R-12 |
| `audit-test-budget.py` 对 `selection_basis=docs-gate-full` 的两槽位夹具 | 槽位计数 `baseline:1 closure:1` **零违规**（其余 `status=fail` 全部来自夹具未提供六阶段 E3 证据，与槽位无关）；负控（追加第二个 baseline 行）转红 | `test-evidence/plan-audit-test-budget-docs-gate-probe.txt` |

## R-1 声明行的判定面：一行文法 + 三个作者错误码，全部归退出码 1

- **文法**：位于 `## Related Feature` 之前的头部区，**至多一行**（缺省合法，缺省按 `execution` 解析），逐字 `^\*\*Flow Class\*\*: (execution|expression)$`
  （半角冒号 + 一个空格 + 值，行尾无空白，字段名与取值大小写敏感）。
- **四个判定结果**，只由形态决定，MUST NOT 读正文语义：
  1. 命中规范形态且取值在封闭集内 → `source: declaration`，退出码 0；
  2. 整个文件无该字段 → `source: default` + 069 登记的默认标记，退出码 0；
  3. 字段在场、取值在封闭集外 → `invalid-class`，退出码 1；
  4. 字段在场但形态不合规范（全角冒号 / 字段名大小写变体 / 尾随空白 / 行内附加注释）→ `declaration-malformed`；
     同一文件出现第二行 → `declaration-duplicate`；字段位于 `## Related Feature` 之后 → `declaration-misplaced`。
- **裁决：4 类中的三种形态错误与 `invalid-class` 同归退出码 1（阻断），不归 2。**
  判据来自 requirements FR-005 的原则而非新语义：作者输入错误 MUST NOT 被降级成默认类；而退出码 2 在 FR-009 里
  被明确定义为「保持既有 execution 门禁集」的可见降级路径。若把一处笔误（例如把字段写成小写）判成 2，
  这条线就会在没有任何提示的情况下按执行类跑完——正是 FR-005 要禁的事。
  `declaration-malformed` 是 requirements 未点名、但由 FR-001「全角冒号、大小写变体、行内附加注释一律不合语法」
  直接蕴含的码：不合语法却静默落到「无该字段」会把它读成未声明。
- **重复与错位的差别**：`declaration-duplicate` 只看行数（不论两次取值是否相同），`declaration-misplaced`
  只看位置（`## Related Feature` 之后），两者同时成立时报 `declaration-duplicate`（同一根因只报一次，与门禁 owner
  的跨标签优先级同源纪律）。
- **Evidence**: `test-evidence/plan-resolution-baseline.txt`（当前键族尚未接受该键时的实测红）。

## R-2 键族：`spec:<spec 目录名>`，解析在既有一处引擎内

- **键形态**：`^spec:[a-z0-9][a-z0-9-]*$`；取值是 spec 目录的 **basename**（`077-doc-sdd-integration`、
  `069a-flow-classification-docs-gates`），不是路径、不是 Feature 号。裸目录名与 `feature:<ID>` 都保持 `invalid-unit-id`。
- **解析位置**：`<repo>/.specify/specs/<name>/requirements.md`；`--repo` 指向 `.specify` 自身时退化为
  `<repo>/specs/<name>`（与 `owner_candidates()` 的两顶帽子处理同源）。spec 目录不存在 → 退出码 2（FR-003）。
- **为何是 basename 而不是路径**：`spec:` 键的唯一消费者是阶段命令与驱动，二者都从 spec 目录出发；用 basename
  让同一台机器上「源仓 `.specify/specs/<name>`」与「客户项目 `.specify/specs/<name>`」两顶帽子解析出同一个键，
  而绝对路径会让同一个特性线在不同环境下拿到两个键（跨环境漂移）。
- **resolution 顺序（本特性登记的一次变更）**：owner 先解析，再判键族，再读声明行。**既有 `action_lookup` 并不是这个顺序**——它先 `UNIT_ID_RE` 再 `parse_owner`；本特性把 owner 提前，因此「键非法 **且** owner 不可解析」这一输入从 `invalid-unit-id` 改报 `owner-unavailable`（同为退出码 2、门禁集不变），差异登记为 requirements FR-011 的豁免①。owner 不可解析时
  任何键都走退出码 2，不会因为键是新族而给出不同的降级标签。
- **Evidence**: 同一文件（`plan-resolution-baseline.txt`）记录了现在 `spec:` 键的退出码与降级记录形态。

## R-3 记录形态：与单元键逐字段同形，退出码 1 的记录不带类别值

- 字段集沿用 `action_lookup` 现有**九项**（`action` / `checked_at` / `unit_id` / `flow_class` / `source` / `marker` /
  `basis` / `neutral` / `error`），`spec:` 键不新增字段：`unit_id` 取键原文、`source` ∈ {`declaration`, `default`}、
  `basis` 为 `null`、`neutral` 为 `false`、`error` 取 `{label, detail}` 或 `null`（`default_lookup_record` 今天正是九键，
  所以「九项」不是本特性的新增，而是既有形态的原文）。
- **退出码 1 的取值裁决**：记录里 `flow_class` 写 `null`（不是 `execution`）。理由：既有 `owner_degradation()`
  在退出码 2 时返回「默认类 + `source: default`」是安全的，因为 FR-009 允许那条路径保持执行类；而退出码 1 若也返回
  `execution`，任何只看记录不看退出码的消费方都会把作者笔误读成一个判定。`null` 让「类别不存在」在字段面上可见。
- **文件与行号走 stderr**：`invalid-class: <repo 相对路径>:<行号> carries '<值>', outside the closed set (...)`
  一行，满足 FR-005「点名文件、行号与越界取值」，同时不往记录里塞第十个字段。
- **不写台账**：`spec:` 键 MUST NOT 进入 § 逐流程台账。`--action check` 的行集对照的是**框架单元清单**
  （`templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md`），spec 目录不在该清单里，写入即产生
  `unknown` 发现（requirements FR-003 已钉）。

## R-4 `Document Structure`：四子节语法落既有检查器的新动作

- **动作名**：`doc-consistency-check.py --action structure`，`--action` 的 choices 从 `("verify",)` 扩为
  `("verify", "structure")`；`--faces` 的四面取值集与 `--faces` 的解析器**一律不动**（FR-013 的「不新增第七面」）。
  实测现状：`--action structure` 今天报 `invalid choice` 退出码 2（`plan-resolution-baseline.txt`）。
- **主体与作用域**：本动作的判定对象是**指定 spec 目录的 `plan.md`**（`--spec-dir`）。类别解析复用 R-2 的同一条路径。
  - 解析为表达类 → 进入四子节与四族码检查（结构语法 / 两向比对 / 证据面 / owner 面）；
  - 解析为执行类或未声明 → `status: not-applicable`，并打印 `class=<值> source=<来源>` 与一个非空伴生量
    （被检查的文件数），使「不适用」不可被读成「0 违规通过」。
- **基线**：按 clarify 第四条，基线 = 该线首次声明那一次实测出的违规集，判据是「当前违规集 ⊆ 基线集」按
  `文件 + 违规码 + 节名` 三元组比对（差集为空）。落盘形态沿用同族先例 `<spec-dir>/structure-baseline.txt`
  （与 `coverage-baseline.txt`、`baseline-failed.txt` 同命名面），由 `--freeze` 打印、脚本自身永不写文件
  （与 `account-clause-coverage.py --freeze` 同一纪律）。文件不存在 = 基线为空集 = 绝对判定，不是豁免。
- **为何不是新检查器**：该检查器已持有读者标记（`**Readers**:` / `**Reading scenario**:`）、证据三件套语法与副本下限
  三项；另置检查器会造出第二套同义解析，与 FR-013 的裁决直接冲突。
- **`## Document Structure` 在 `plan.md` 的锚点**：四个三级子节标题逐字取 [[STR-003]]…[[STR-006]]；本节不重抄字面量，
  它们在 requirements § Shared Strings 有唯一登记处，检查器以常量持有（code-first owner），测试从常量读取。

## R-5 两槽位：只换内容，审计与字段集不动（已用夹具实测）

- `selection_basis=docs-gate-full`；`command` 记该次文档门禁命令串；`rc` 记该串的**聚合退出码**（逐命令非零优先，
  逐命令原始 rc 留在 `evidence_ptr` 指向的门禁输出里——这是「`rc` 无单一进程」的解法，不引入聚合脚本）；
  `passed` 记 verdict = `pass` 的 blocking 算子数，`failed` 记 verdict ∈ {`fail`, `not-evaluated`} 的算子数，
  `not-applicable` **单列**（不计 `passed`、不计 `failed`；它只出现在 `G-implement-structure` 的 `build` 子行，按面级读，
  与门禁 owner「不得记为通过」一致；MUST NOT 用「算子总数 − (`passed`+`failed`)」跨级等式反推——子行与算子级行不是同一计量单位）；closure 的 `baseline_compare` 写成算子 id 名称级差集
  （`comm -13 <基线算子名单> <收口算子名单>`）；`failed_names_path` 指向**失败算子 id 名单**文件。
- **实测结论**：`audit-test-budget.py` 对 `selection_basis` **不做枚举校验**（只校验在场），对 `passed` / `failed`
  只校验可解析为整数，closure 的 `baseline_compare` 只校验「名称级」形态（接受 `comm -13` / JSON 数组 /
  `new failures:` 三种写法之一）。因此 `docs-gate-full` 与算子计数**无需改审计脚本**，FR-020 的「审计判定不变」可兑现。
  证据：`test-evidence/plan-audit-test-budget-docs-gate-probe.txt`（正样本 `baseline:1 closure:1` 零槽位违规，
  负样本追加第二个 baseline 后转红，证明该探针不是空绿）。

## R-6 驱动载荷与 U4：四元组、四项 blocking、两槽位替代

- **载荷四元组**：`flow_class=<值>` / `source=<declaration|default>` / `marker=<默认标记或空>` /
  `error=<owner-unavailable|->`（值域恰为这两项；`declaration-absent` 是 advisory 码、不进载荷），写进第①段「背景与权威文档」，因此本地原生派发与远端 CLI 派发携带的是同一份文本
  （提示词是唯一载体，环境变量不参与）。`error` 位的用途是把「机制降级（`owner-unavailable`）」与
  「作者没写声明」在载荷上分开——两者都可能是 `source=default`。
- **U4 的四项**（在既有四条件之外，全部 blocking）：(a) 本阶段**算子表登记的 blocking 行**各有一条结果记录且无
  `not-evaluated`（计数分母只取算子表：implement 为 1 行 `G-implement-structure`，四个 CLI 面不各自算算子）；
  (b) 该记录的 `evidence_path` 指向的文件存在且非空——**不做哈希比对**（既有 `gate-implement-evidence-binding` 的
  哈希只约束 `verification.md` 的 SC 样本行，且其 owner 明写非 `pass` 不承担绑定义务，给算子记录加哈希会反转它）；
  (c) 载荷类别与 U4 当场解析值一致，且载荷 `error` 位非 `-` 时走 `owner-unavailable` 分支（记降级观测、保持既有门禁集）；
  (d) 本阶段 `stage-status` 行在场。
- **不缓存**：类别在**每次派发前**解析一次；状态脊里的类别行只是带日期的观测，重入时重新解析并与观测比对，
  不一致记 re-baseline。这条同时封住「跨阶段缓存」与「从脊读值」两个口子。

## R-7 七模板的接线形态：一个子节、一次 lookup、零副本

- 形态取既有先例 `templates/commands/docs.md` 的**子节形态**（该文件的标题带后缀，属另一条入口，MUST NOT 照抄，也不得与本节混为一谈）；本特性子节的标题**逐字取 R-9 登记的唯一字面量**（登记处只有 R-9 一处，本行不复述字面量）：一个三级子节，内含
  **一次** lookup 调用（`--unit-id "spec:<spec 目录名>"`）、两条 owner 指针（判据 owner、门禁 owner）、
  一个分支句（表达类 → 按阶段算子表执行本阶段登记的行；其余 → 既有门禁集逐字不变）、一条降级可见句。
- **文本卫生**（沿用 069a A5 的纪律）：子节内 MUST NOT 出现
  - 任何 `G-` 算子 id（算子表副本），
  - 任何六面 face id 表，
  - 任何类别取值赋值形（`flow_class=` / `flow_class:`），
  - 任何按特性号、路径、关键词的允许列表。
  分支句用中文语义词（「表达类」「执行类」）表达，机器取值只出现在 lookup 的输出里。
- **读一次的实现位置**：命令模板是 agent 读的指令，因此「读一次」写在模板里；委派技能不再读（FR-008）。
  六个阶段的读取点是阶段入口；`requirements` 阶段的读取点是类别行写入之后、`validate-requirements.py` 之前
  （FR-006 的特例，由 requirements 模板独立一句话承载）。
- **本特性落点**：上述改动只落 `templates/commands/*.md`（框架源），per-tool 副本由 `regen-command-copies.py` 产出
  （该脚本的 `_ASSISTANT_COMMAND_DIRS` 最多登记六个目标，只为**本仓已存在**的目标目录产出；本仓当前四个：
  `.claude/` / `.github/` / `.qoder/` / `.opencode/`，`.codex/` 与 `.hermes/` 目录不存在故不产出）。

## R-8 七模板接线会让既有闭合集守卫转红：同一次改动内修订该守卫（实证）

- `tests/contract/test_expression_gate_wiring.py::test_a6_wiring_set_is_closed` 断言「除 `docs.md` / `humanize.md`
  外的 25 个模板与 49 个技能都不出现引擎与门禁 owner」。本次接线必然让它转红。
- **实测（mutation probe）**：向 `templates/commands/plan.md` 追加一行 `flow-class-check.py` 后，该断言报
  `- templates/commands/plan.md → flow-class-check.py` 并 FAILED；文件随后原样恢复（`git status` 干净）。
  证据：`test-evidence/plan-a6-mutation-probe.txt`。
- **裁决**：该守卫是「闭合集」这一命题的载体，不是本次要废除的命题。修订方式是把七个模板加入**已接线名册**
  （与 docs/humanize 并列），其余模板与技能仍零命中；分母断言（27 模板 / 52 技能）不动。
  「删掉断言」与「整体放宽」都是把命题删掉，MUST NOT 采用。

## R-9 execution 零变化的反向守卫：剥离子节后与基线提交逐字相同（标题字面量与剥离算法的唯一登记处）

- **子节标题字面量（唯一登记处 = 本节）**：`### 类别读取与文档型门禁`——逐字、无后缀、无变体。它是
  「每模板恰一个子节」的计数锚、剥离器的起点，也是执行类反向守卫边界的一半；模板、契约、测试与剥离器
  MUST 从这里取值，MUST NOT 各自复制一份（`templates/commands/docs.md` 的既有标题带后缀，属另一条入口，
  不得照抄它的形态，也不得把两者混为一谈）。登记处选在本节而不是 requirements § Shared Strings，
  是为了不改变该表的行数（6 行）：本字面量的消费者只有 stage-wiring 契约与两个测试文件，不是跨规格共享词汇。
- **剥离算法（钉死，两个实现者必须算出同一结果）**：
  1. **起点** = 子节标题行（含）；
  2. **终点** = 该行之后第一个同级或更高级标题行（匹配 `^#{1,3} `，即 `#` / `##` / `###`）的**前一行**（含）；
     其后无任何标题行时，终点 = 文件最后一行（含）；
  3. 删除起点至终点，**不额外插入也不删除空行**。
- **块内标题纪律（防提前截断）**：块内出现**任何同级或更高级标题（含 `###`）一律视为块结束**——剥离器 MUST NOT 采用「跳过小标题继续吃」的启发式；
  因此子节正文 MUST NOT 嵌 `###` 小标题，需要分层时用 `####`（不匹配 `^#{1,3} `，不会提前截断）。判定由同一守卫断言，
  违反即判接线形态违规——否则「块尾恰一个空行」的前提会在块内 `###` 处塌陷，剥离结果不可复算。
- **成立前提（作者义务）**：子节块 MUST 以**恰一个空行**收尾——块末与下一个标题之间不得出现两个及以上空行。
  这样端点必然落在「一个空行」上，删除后剩下的分隔空行与插入前的基线逐字相同；违反该形态即判接线形态违规
  （由 `test_stage_class_wiring.py` 断言），否则剥离不可复算。
- **可复算样例（两份实现都应得到同一结果）**：

  ```text
  插入后（行号只是说明，不进入文件）          剥离后
  1  ## User Input                            1  ## User Input
  2  （既有正文）                              2  （既有正文）
  3  （空行）                                  3  （空行）
  4  ### 类别读取与文档型门禁                  4  ## Outline
  5  （子节第 1 段）
  6  （子节第 n 段）
  7  （空行）
  8  ## Outline
  ```

  端点：起点 = 4；4 之后第一个 `^#{1,3} ` 行是 8，故终点 = 7；删除 4–7 后剩 `## User Input` / 正文 / 空行 / `## Outline`，
  与插入前的基线逐字相同。若把第 7 行写成两个空行，终点仍为 7 的下一行、删除后留下一个多余空行，
  字节判据立即失效——这正是要把它写成作者义务的原因。
- **判据形态**：对七个模板，按上述算法剥离后的文本 MUST 与基线提交 `c1cd4600` 的同名文件**逐字相同**
  （SHA-256 相等），**且**同时断言子节在场（只断言「剥离后相等」会在无接线时空转）。
- **不把哈希预先写死**：基线 blob 的哈希在实现期由 `git show c1cd4600:<path> | shasum -a 256` 实测后钉进测试常量
  （合法的「测试内冻结字面量」形态）。本 plan 只钉判据、算法与样例，不预写数字——预写的期望值会与实际碰撞。

## R-10 测试布局：按被测对象拆四个契约文件 + 一个单元文件

| 文件 | 被测对象 | 红先行的起点 |
|------|----------|--------------|
| `tests/unit/test_flow_class_spec_key.py` | 引擎的 `spec:` 键族（键文法、记录形态、三段退出码、不写台账、owner 先于键解析） | 现状退出码 2（R-2 实测） |
| `tests/contract/test_flow_class_spec_declaration.py` | 声明行文法与四个码（`invalid-class` / `malformed` / `duplicate` / `misplaced`）、模板字段位置、索引与详情不存取值 | 模板与引擎都不认识该字段 |
| `tests/contract/test_stage_class_wiring.py` | 七模板的一次 lookup、零副本、execution 反向守卫（R-9）、闭合集名册修订（R-8）、命令副本携带 | 七模板零命中（实测） |
| `tests/contract/test_document_structure_gate.py` | `--action structure` 的四子节、列语义、`chapter-*` / `owner-*` / `evidence-*` 码、主体集合与 `not-applicable`、`--faces` 不变 | `--action structure` 退出码 2（实测） |
| `tests/contract/test_docs_gate_driver.py` | 载荷四元组、U4 四项、两槽位内容、阶段序列与 100% 调用率不变 | 驱动技能零命中 |

五个文件都是 red-first；负样本只留在测试里，不进任何 owner 文档（与 069a/076 同纪律）。

## R-11 镜像与命令副本：基线为零漂移，判据写成「无新增」

- **基线实测**：`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均为退出码 0（六对 `ok`、
  副本全一致）。因此本次的判据是「相对该基线**无新增漂移**」——可以写成绝对相等，但仍按「无新增」表述，
  以便同时覆盖「本特性未触达的对意外变红」这种上游噪声。
- **受影响的对**：`templates/` → `.specify/templates/`（`requirements-template.md`、`plan-template.md`）；
  `shared/` → `.specify/shared/`（两份 owner 的类条件追加）；`scripts/` → `.specify/scripts/`（两个引擎）；
  `skills/external` → `.specify/skills/`（驱动技能及其 `references/`）。`templates/commands/**` **不在**
  templates 对的镜像范围内（`commands` 被排除），只走 `regen-command-copies.py` 的 per-tool 副本——套数以该脚本实际
  产出的目标目录为准（注册表最多六个，本仓当前四个），契约与任务都 MUST NOT 写死套数。

## R-12 零新增确认门：子节措辞必须避开阻断式确认语，且预算必须被**重新测量**

- 实测 `scan-confirmation-gates.py --summary` = blocking gates **27**，violations 0；该预算是整数、零余量。
- **判据可判定化**：既有守卫的总量断言是 `cap = baseline["total"] * 0.25`，因此 `+1` **不会**让它转红——
  「没有任何门会响」正是这条发现的实质。故 requirements FR-022 把该预算写成可判定条款：改动前后各跑一次
  `scan-confirmation-gates.py --summary`，两次 `blocking confirmation gates` 计数 MUST 相等；T021 含一次该扫描器运行
  （证据落 `test-evidence/tasks-scope-set-difference.txt`）。SC-006 同列该项。
- 因此七模板子节的措辞**不得**新增「问用户是否继续 / 等待确认 / 批准后执行」一类阻断句；表达方式一律用
  「读数 → 按 owner 执行算子 → 未通过即报未通过」的陈述句。降级句写「显示标签并保持既有门禁集」，
  不写「提示用户选择」。

## R-13 本轮不做的事（防止范围蔓延）

- 不新增 `/speckit.*` 命令、不新增门禁面（`--faces` 四面不变）、不新增持久化载体（槽位落既有状态脊围栏、
  结构基线落既有 spec 目录命名面）、不新增第三方依赖、不引入常驻进程。
- 不回写 069 的正文/状态，不在 069 的详情文件里补写承接关系（承接关系记在 `features/077.md` 与本 plan 的
  `feature-ref.md`）。
- 不修 `provisioner`-类遗留问题、不动 `069` 的三条切片规格、不改 `coverage-baseline.txt` 的冻结内容（该文件已由
  tasks 阶段按 77 条款认领冻结；只有条款认领变化时才重冻结，本轮不变）。

## 偏差与披露（disclosed, not silent）

1. **脚手架**：`create-new-plan.sh` 在 `CWS_LIB_BASH_HOME` 未设时以非零退出且不产出 `plan.md`；派发同时禁止切分支。
   故按调用方允许的偏差路径，`plan.md` 由 `.specify/templates/plan-template.md` 就地填写，分支保持
   `077-doc-sdd-integration`。该脚本被抑制的动作是「模板复制」，不是分支操作。
2. **clause 车道**：本阶段写下时该车道报 `baseline-missing`（`account-clause-coverage.py` 要求
   `<spec-dir>/coverage-baseline.txt` 冻结**其它 spec** 的既有未覆盖条款名，它是一个豁免清单；当时尚未冻结）。
   **该判断已被后续阶段推翻，特此更正（见 `plan.md` § Plan Edits 的 PLAN-EDIT: minor）**：tasks 阶段已按 77 条款认领
   冻结 `coverage-baseline.txt`（只冻结他线既有未覆盖名，base-sha `06c31b1d`），当前该车道实测
   `claimed=77`、`beyond baseline=0`、`status: ok`。本条目保留为「当时的判断 + 何时被更正」的记录，不再作为现状引用。
3. **同作者门（objective-analysis-gate）**：本 run 从 requirements 到 plan 无断点，被评分的工件由同一 agent 产出。
   本执行环境未向执行 agent 暴露子代理派发工具（工具面为文件读写、检索与命令执行），按该 owner 的
   subagent-unavailable 降级形态，评分走直接受限读，并在 plan 的 Constitution Check 段逐行标注
   `(detected: direct read, subagent unavailable)`。
