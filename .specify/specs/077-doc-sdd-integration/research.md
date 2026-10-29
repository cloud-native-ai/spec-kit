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

- **文法**：位于 `## Related Feature` 之前的头部区，恰一行，逐字 `^\*\*Flow Class\*\*: (execution|expression)$`
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
- **resolution 顺序不可变**：owner 先解析（与既有 `action_lookup` 一致），再判键族，再读声明行。owner 不可解析时
  任何键都走退出码 2，不会因为键是新族而给出不同的降级标签。
- **Evidence**: 同一文件（`plan-resolution-baseline.txt`）记录了现在 `spec:` 键的退出码与降级记录形态。

## R-3 记录形态：与单元键逐字段同形，退出码 1 的记录不带类别值

- 字段集沿用 `action_lookup` 现有八项（`action` / `checked_at` / `unit_id` / `flow_class` / `source` / `marker` /
  `basis` / `neutral` / `error`），`spec:` 键不新增字段：`unit_id` 取键原文、`source` ∈ {`declaration`, `default`}、
  `basis` 为 `null`、`neutral` 为 `false`。
- **退出码 1 的取值裁决**：记录里 `flow_class` 写 `null`（不是 `execution`）。理由：既有 `owner_degradation()`
  在退出码 2 时返回「默认类 + `source: default`」是安全的，因为 FR-009 允许那条路径保持执行类；而退出码 1 若也返回
  `execution`，任何只看记录不看退出码的消费方都会把作者笔误读成一个判定。`null` 让「类别不存在」在字段面上可见。
- **文件与行号走 stderr**：`invalid-class: <repo 相对路径>:<行号> carries '<值>', outside the closed set (...)`
  一行，满足 FR-005「点名文件、行号与越界取值」，同时不往记录里塞第九个字段。
- **不写台账**：`spec:` 键 MUST NOT 进入 § 逐流程台账。`--action check` 的行集对照的是**框架单元清单**
  （`templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md`），spec 目录不在该清单里，写入即产生
  `unknown` 发现（requirements FR-003 已钉）。

## R-4 `Document Structure`：四子节语法落既有检查器的新动作

- **动作名**：`doc-consistency-check.py --action structure`，`--action` 的 choices 从 `("verify",)` 扩为
  `("verify", "structure")`；`--faces` 的四面取值集与 `--faces` 的解析器**一律不动**（FR-013 的「不新增第七面」）。
  实测现状：`--action structure` 今天报 `invalid choice` 退出码 2（`plan-resolution-baseline.txt`）。
- **主体与作用域**：本动作的判定对象是**指定 spec 目录的 `plan.md`**（`--spec-dir`）。类别解析复用 R-2 的同一条路径。
  - 解析为表达类 → 进入四面检查；
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

- `selection_basis=docs-gate-full`；`command` 记该次文档门禁命令串；`passed` 记 verdict ∈ {pass, not-applicable}
  的 blocking 算子数，`failed` 记 verdict ∈ {fail, not-evaluated} 的算子数；closure 的 `baseline_compare` 写成
  算子 id 名称级差集（`comm -13 <基线算子名单> <收口算子名单>`）；`failed_names_path` 指向**失败算子 id 名单**文件。
- **实测结论**：`audit-test-budget.py` 对 `selection_basis` **不做枚举校验**（只校验在场），对 `passed` / `failed`
  只校验可解析为整数，closure 的 `baseline_compare` 只校验「名称级」形态（接受 `comm -13` / JSON 数组 /
  `new failures:` 三种写法之一）。因此 `docs-gate-full` 与算子计数**无需改审计脚本**，FR-020 的「审计判定不变」可兑现。
  证据：`test-evidence/plan-audit-test-budget-docs-gate-probe.txt`（正样本 `baseline:1 closure:1` 零槽位违规，
  负样本追加第二个 baseline 后转红，证明该探针不是空绿）。

## R-6 驱动载荷与 U4：三元组、四项 blocking、两槽位替代

- **载荷三元组**：`flow_class=<值>` / `source=<declaration|default>` / `marker=<默认标记或空>`，写进第①段
  「背景与权威文档」，因此本地原生派发与远端 CLI 派发携带的是同一份文本（提示词是唯一载体，环境变量不参与）。
- **U4 的四项**（在既有四条件之外，全部 blocking）：(a) 本阶段 blocking 算子各有一条结果记录且无 `not-evaluated`；
  (b) 该记录的 `evidence_path` 指向的文件存在、非空、SHA-256 与 `evidence_sha256` 一致（复用既有
  `gate-implement-evidence-binding` 的四键口径，owner 为 `templates/verification-log-template.md` 与
  `skills/internal/implement-feature/SKILL.md` 的同一门）；(c) 载荷类别与 U4 当场解析值一致；(d) 本阶段
  `stage-status` 行在场。
- **不缓存**：类别在**每次派发前**解析一次；状态脊里的类别行只是带日期的观测，重入时重新解析并与观测比对，
  不一致记 re-baseline。这条同时封住「跨阶段缓存」与「从脊读值」两个口子。

## R-7 七模板的接线形态：一个子节、一次 lookup、零副本

- 形态取既有先例 `templates/commands/docs.md` 的 `### 类别读取与文档型门禁` 子节：一个三级子节，内含
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
- **本特性落点**：上述改动只落 `templates/commands/*.md`（框架源），`.claude/` / `.github/` / `.qoder/` /
  `.opencode/` / `.codex/` / `.hermes/` 六套副本由 `regen-command-copies.py` 产出。

## R-8 七模板接线会让既有闭合集守卫转红：同一次改动内修订该守卫（实证）

- `tests/contract/test_expression_gate_wiring.py::test_a6_wiring_set_is_closed` 断言「除 `docs.md` / `humanize.md`
  外的 25 个模板与 49 个技能都不出现引擎与门禁 owner」。本次接线必然让它转红。
- **实测（mutation probe）**：向 `templates/commands/plan.md` 追加一行 `flow-class-check.py` 后，该断言报
  `- templates/commands/plan.md → flow-class-check.py` 并 FAILED；文件随后原样恢复（`git status` 干净）。
  证据：`test-evidence/plan-a6-mutation-probe.txt`。
- **裁决**：该守卫是「闭合集」这一命题的载体，不是本次要废除的命题。修订方式是把七个模板加入**已接线名册**
  （与 docs/humanize 并列），其余模板与技能仍零命中；分母断言（27 模板 / 52 技能）不动。
  「删掉断言」与「整体放宽」都是把命题删掉，MUST NOT 采用。

## R-9 execution 零变化的反向守卫：剥离子节后与基线提交逐字相同

- 判据形态：对七个模板，删去新增子节（以子节标题为界、到下一个 `##` 或 `###` 为止）后的文本，MUST 与基线提交
  `c1cd4600` 的同名文件**逐字相同**（SHA-256 相等）。这把「零行为变化」从印象变成可复算的字节相等。
- **不把哈希预先写死**：基线 blob 的哈希在实现期由 `git show c1cd4600:<path> | sha256sum` 实测后钉进测试常量
  （合法的「测试内冻结字面量」形态）。本 plan 只钉判据与方法，不预写数字——预写的期望值会与实际碰撞。
- **子节边界**是判据的一部分：若子节没有明确终止边界，剥离就不可复算，测试会随排版漂移。故模板里该子节 MUST
  以固定标题起头、并位于它自己的 `##`/`###` 块内，不与既有条款混排。

## R-10 测试布局：按被测对象拆三个契约文件 + 一个单元文件

| 文件 | 被测对象 | 红先行的起点 |
|------|----------|--------------|
| `tests/unit/test_flow_class_spec_key.py` | 引擎的 `spec:` 键族（键文法、记录形态、三段退出码、不写台账、owner 先于键解析） | 现状退出码 2（R-2 实测） |
| `tests/contract/test_flow_class_spec_declaration.py` | 声明行文法与四个码（`invalid-class` / `malformed` / `duplicate` / `misplaced`）、模板字段位置、索引与详情不存取值 | 模板与引擎都不认识该字段 |
| `tests/contract/test_stage_class_wiring.py` | 七模板的一次 lookup、零副本、execution 反向守卫（R-9）、闭合集名册修订（R-8）、命令副本携带 | 七模板零命中（实测） |
| `tests/contract/test_document_structure_gate.py` | `--action structure` 的四子节、列语义、`chapter-*` / `owner-*` / `evidence-*` 码、主体集合与 `not-applicable`、`--faces` 不变 | `--action structure` 退出码 2（实测） |
| `tests/contract/test_docs_gate_driver.py` | 载荷三元组、U4 四项、两槽位内容、阶段序列与 100% 调用率不变 | 驱动技能零命中 |

五个文件都是 red-first；负样本只留在测试里，不进任何 owner 文档（与 069a/076 同纪律）。

## R-11 镜像与命令副本：基线为零漂移，判据写成「无新增」

- **基线实测**：`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均为退出码 0（六对 `ok`、
  副本全一致）。因此本次的判据是「相对该基线**无新增漂移**」——可以写成绝对相等，但仍按「无新增」表述，
  以便同时覆盖「本特性未触达的对意外变红」这种上游噪声。
- **受影响的对**：`templates/` → `.specify/templates/`（`requirements-template.md`、`plan-template.md`）；
  `shared/` → `.specify/shared/`（两份 owner 的类条件追加）；`scripts/` → `.specify/scripts/`（两个引擎）；
  `skills/external` → `.specify/skills/`（驱动技能及其 `references/`）。`templates/commands/**` **不在**
  templates 对的镜像范围内（`commands` 被排除），只走 `regen-command-copies.py` 的六套 per-tool 副本。

## R-12 零新增确认门：子节措辞必须避开阻断式确认语

- 实测 `scan-confirmation-gates.py --summary` = blocking gates **27**，violations 0；该预算是整数、零余量。
- 因此七模板子节的措辞**不得**新增「问用户是否继续 / 等待确认 / 批准后执行」一类阻断句；表达方式一律用
  「读数 → 按 owner 执行算子 → 未通过即报未通过」的陈述句。降级句写「显示标签并保持既有门禁集」，
  不写「提示用户选择」。

## R-13 本轮不做的事（防止范围蔓延）

- 不新增 `/speckit.*` 命令、不新增门禁面（`--faces` 四面不变）、不新增持久化载体（槽位落既有状态脊围栏、
  结构基线落既有 spec 目录命名面）、不新增第三方依赖、不引入常驻进程。
- 不回写 069 的正文/状态，不在 069 的详情文件里补写承接关系（承接关系记在 `features/077.md` 与本 plan 的
  `feature-ref.md`）。
- 不修 `provisioner`-类遗留问题、不动 `069` 的三条切片规格、不冻结 `coverage-baseline.txt`（见下条偏差）。

## 偏差与披露（disclosed, not silent）

1. **脚手架**：`create-new-plan.sh` 在 `CWS_LIB_BASH_HOME` 未设时以非零退出且不产出 `plan.md`；派发同时禁止切分支。
   故按调用方允许的偏差路径，`plan.md` 由 `.specify/templates/plan-template.md` 就地填写，分支保持
   `077-doc-sdd-integration`。该脚本被抑制的动作是「模板复制」，不是分支操作。
2. **clause 车道的 `baseline-missing` 是设计内红**：`account-clause-coverage.py` 要求
   `<spec-dir>/coverage-baseline.txt` 冻结**其它 spec** 的既有未覆盖条款名（它是一个豁免清单）。本特性不消费
   该车道（条款为新建、非派生），冻结它会顺手把 495 条历史未覆盖条款登记成「本特性的豁免」，属伪造基线。
   故如实记录 `status: baseline-missing`，并在证据里保留原始输出。FR 车道则必须是全覆盖（25/25），它才是本特性的门。
3. **同作者门（objective-analysis-gate）**：本 run 从 requirements 到 plan 无断点，被评分的工件由同一 agent 产出。
   本执行环境未向执行 agent 暴露子代理派发工具（工具面为文件读写、检索与命令执行），按该 owner 的
   subagent-unavailable 降级形态，评分走直接受限读，并在 plan 的 Constitution Check 段逐行标注
   `(detected: direct read, subagent unavailable)`。
