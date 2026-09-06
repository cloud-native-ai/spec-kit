# Contract: /speckit.derive 命令模板结构(需求 048 / Feature 049)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**交付物**: `templates/commands/derive.md`(源)→ 4 份工具副本(`regen-command-copies.py` 传播)
**概念真源**: `shared/definitions/derivation-definitions.md`;执行面见 `contracts/derivation-model.md`、`contracts/derive-engine.md`、`contracts/move-library.md`
**消费方**: `tests/contract/test_derive_command_surface.py`、`tests/contract/test_docs_step_injection.py`、`tests/contract/test_feedback_command_classification.py`、`tests/contract/test_qoder_command_frontmatter.py`、`tests/contract/test_confirmation_gates_sweep.py`、`shared/definitions/probe-definitions.md`

## 1. Frontmatter

- C-1 模板 MUST 以 `---\n` 开头,frontmatter 键集恰为 `description` / `short-description` / `handoffs`,MUST NOT 含 `scripts:` 或 `agent_scripts:`。
- C-2 `description` MUST 为**英文单句**,陈述命令的触发意图与产物形态(照 `templates/commands/research.md`、`goal.md` 先例),MUST NOT 复述工作流阶段、MUST NOT 内嵌路径、MUST NOT 出现 `Feature 049` / `048` 一类编号。**为何禁止复述工作流**:`generate_commands()` 把该值原样写进 Codex/Copilot 侧的 `description` 字段且**不经** `rewrite_paths()`(该函数只作用于 body,见 `src/specify_cli/__init__.py` 第 1543 行),故其中的根相对路径会在副本里指向不存在的位置;而阶段清单会与 `## Outline` 形成第二处真源。
- C-3 `short-description` MUST ≤ 50 个字符 —— `tests/contract/test_qoder_command_frontmatter.py::test_every_template_has_short_description` 逐模板钉死该上限,且该值 MUST 与 `.qoder/commands/speckit.derive.md` 的 frontmatter `description` 逐字相等(同文件 `test_qoder_frontmatter_matches_template`)。中文按 `len()` 码点计,不按字节。
- C-4 MUST NOT 有 `scripts:` 键。该机制在 `src/specify_cli/__init__.py` 中只支持**一个 bash 安装脚本**:`SCRIPT_TYPE_CHOICES = {"sh": ...}`(第 1212 行,仅 POSIX shell)、`body.replace("{SCRIPT}", script_command)`(第 1539 行,单一命令串替换)、且 `scripts:` 块在生成副本时被整段剥除(第 1501–1528 行)。一个六动作 Python 引擎无法经它表达,故引擎调用 MUST 像 `templates/commands/sanitize.md` 那样**内联**为字面 `python3 .specify/scripts/python/derive-utils.py --action <a> ...` 代码块。
- C-5 `handoffs` MUST 至少给出 `After` 方向的一条(建议指向 `/speckit.plan`,因为 Plan MAY 以 `A-<k>` 身份引用架构元素);每条 MUST 含 `label` / `agent` / `prompt` / `send` 四键,与既有模板同形。

## 2. 正文章节次序(结构性,逐项可测)

- C-6 正文 `##` 级章节 MUST 恰按此序出现,且 MUST NOT 出现该表之外的 `##` 章节:

`## User Input` → `## Glossary` → `## Outline` → `## Behavior Rules` → `## Feedback` → `## Documentation` → `## Handoffs`

- C-7 **为何是这个序**:`tests/contract/test_docs_step_injection.py::test_c3_c4_documentation_section_position_and_reference` 对每个复杂命令断言 (a) `## Feedback` 出现在 `## Documentation` 之前,(b) 二者**相邻**(其间不得有任何 `^## ` 非 Feedback 章节),(c) `## Documentation` 在 `## Handoffs` 之前,(d) `## Documentation` 正文含字面 `docs-step.md`,(e) 正文长度 < 1500 字符,(f) 正文同时含 `需记录` 与 `无需记录`。
- C-8 `templates/commands/sanitize.md` 的次序是**反的**(其第 101 行 `## Documentation` 先于第 105 行 `## Feedback`),因此它不在该测试的 `COMPLEX_COMMANDS` 名单里。derive MUST NOT 抄它的节序;本命令 MUST 被加进该名单(15 → 16,SC-006 的 docs-step 分类计数 +1),同时加进 `tests/contract/test_feedback_command_classification.py` 的 `COMPLEX_COMMANDS`(18 → 19)。
- C-9 `## Documentation` 正文 MUST 是**引用而非复制**:一句话指向 `shared/workflow/docs-step.md`,声明增量判定、非阻塞、需移动/归档级变更时改荐 `/speckit.docs`,并以「结论 MUST 恰为 `需记录(目标文档 + 要点)` 或 `无需记录` 之一」收束。(c)–(f) 四项断言共用这一段文本,长度上限 1500 字符即「引用不复制」的机械形态。
- C-10 `## Glossary` MUST 指向 `.specify/memory/glossary.md` 与 `shared/workflow/glossary.md`,MUST NOT 内嵌术语表;Derivation / Reasoning Move / Provenance Grade 三词的定义归概念锚与词汇表,模板 MUST 只引用。
- C-11 `## Outline` MUST 给出阶段化执行流(Preflight → Ground(probe-links)→ Grade → Moves(moves-list / 抽取 / moves-add)→ Chain → Assemble → Terminate(填 [[STR-008]] 两行)→ Validate + 自审背书 → Report),每阶段 MUST 内联其引擎调用或明确标注为 agent 动作;阶段与引擎动作 MUST 一一对应 [[STR-003]] 六值,不得出现无对应动作的阶段或未被任何阶段调用的动作。
- C-12 `## Behavior Rules` MUST 逐条列出红线:概念锚引用纪律(C-13)、零阻塞门控与三要素执行报告(C-16…C-20)、能力降级(C-21)、投影而非复写、`moves.md` 只经 `moves-add` 写、**产物只记本次运行的处置(`new`/`reused`/`reinforced`),MUST NOT 写库的持久 `status` 列**(该列只有 `active`/`superseded`,概念锚 §Move Record)、**跨主题的来源引用 MUST 写限定形式 `<topic-slug>.S-<nnn>`**(概念锚 §Move Record)、**终止条件 (a)|(b) 由 agent 在 [[STR-008]] 中声明并背书,步数对预算的计数归引擎**(A12 的两半,概念锚 §Self-Audit)、引擎检查为红时不得把架构当作已推导呈现、绝不用听起来合理的猜测填空。

## 3. 概念锚引用纪律

- C-13 模板 MUST 以**根相对**形式至少一次引用 `shared/definitions/derivation-definitions.md`(不带 `.specify/` 前缀)。**为何**:`rewrite_paths()`(`src/specify_cli/__init__.py` 第 1360–1369 行)对 body 中起始位置的 `memory/` `scripts/` `templates/` `shared/` 四段统一升级为 `.specify/<段>/`,其 lookbehind `(?<![\w./-])` 使已带前缀的写法不被二次改写 —— 故根相对写法在源与四份副本中都指向真实文件,而手写前缀虽同样稳定,却会让「源模板按仓根书写」这一惯例出现第二种形态。
- C-14 模板 MUST 显式声明 link-not-restate 规则,正文 MUST 含字面短语 `never restate`(照 `templates/commands/goal.md` 第 19 行先例,`tests/contract/test_goal_command_surface.py::test_command_does_not_restate_the_concept` 即以该短语为锚)。声明 MUST 覆盖:四类 record schema、四级等级、C1–C7、A1–A14、封闭禁用集、降级规则 —— 六者一律「link, never restate」。
- C-15 模板 MUST NOT 复述概念锚的表格、枚举或阈值字面量(禁用集、等级名、`access` / `resolved_via` / `confidence` / 算子 `status` 各枚举、小文件阈值)。需要它们时 MUST 写「以 `derive-utils.py` 输出与 `--help` 为准」并指向锚(照 sanitize 模板第 20 行的同形措辞)。

## 4. 零阻塞门控(硬性预算约束)

- C-16 模板新增的阻塞门控匹配数 MUST 为 **0**。**为何是 0 而非「不超基线」**:`tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target` 的上限是 `baseline["total"] * 0.25` = 93 × 0.25 = **23.25**,而扫描器当前实测 `total` = **23** —— 预算余量为 0.25 条,**任何一条新匹配都会使该测试失败**;同时该匹配若被判为 `reversible`,`test_no_reversible_gates_remain_blocking` 会二次失败。
- C-17 `scripts/python/scan-confirmation-gates.py` 的 `BLOCKING_RE`(第 46–65 行)逐行匹配 `templates/commands/` 下每个文件(第 35、121–123 行),故模板 MUST 避开以下**推导语汇天然会踩的字面量地雷**:

| 地雷模式(源码逐字) | 推导工作流中会诱发的措辞 | 必须改用的措辞 |
|---|---|---|
| `confirmation gate` \| `确认门[禁控]` | 「本命令零确认门禁」「no confirmation gate」—— **声明零门控本身就会命中** | 「no blocking user-confirmation step」;引用判据文档时写路径 `shared/guidelines/confirmation-gates.md`(连字符不匹配该模式) |
| `显式用户确认` \| `explicit user confirmation` | A11/A14 需要「显式背书」,极易写成「explicit user confirmation」 | 「explicit **agent** attestation」——背书主体是 agent,不是用户 |
| `after user confirmation` \| `after confirmation` | 「after confirmation, write the archive」 | 「auto-execute, then report」 |
| `[Cc]onfirm before` | 「confirm before writing `derive.md`」 | 「validate before writing」 |
| `stop and confirm` | 「stop and confirm the grade」 | 「stop and report the degradation」 |
| `等待用户确认` \| `等待确认` \| `用户确认后才` \| `确认后才(?:执行\|写入\|落盘\|启动\|持久化)` | 中文阶段描述里的「等待确认后写入算子库」 | 「自动写入并出具执行报告」 |
| `Confirm and persist` \| `确认并落盘` \| `合并确认` | `moves-add` 的去重-合并语义极易写成「合并确认」 | 「dedup and refuse, returning the existing `move_id`」 |
| `MUST NOT execute before confirmation` | 红线段直译 | 「MUST report the failure honestly」 |
| `[Pp]roceed[^\n]{0,40}yes/no` | 「Proceed anyway? (yes/no)」式预算触顶追问 | 「report the budget cap as reached」 |
| `preview\s*(?:→\|->)\s*confirm\s*(?:→\|->)\s*execute` | 阶段流程图写成 preview → confirm → execute | 「probe → grade → derive → validate」 |
| `interactive confirmation` \| `wait for user confirmation` \| `Execute on Confirmation` | 交互说明 | 「non-interactive; auto-execute」 |
| `inviting the user to submit collected feedback` | Feedback 步的阈值提交提示 | 「inviting submission」(既有模板即此措辞,故 23 条中无 Feedback 步命中) |

- C-18 `--force` 覆盖脚手架是唯一带破坏性的动作,它 MUST 由**用户在参数中显式给出**而非由命令追问产生;模板 MUST NOT 为它设任何等待步骤,`init` 的 no-clobber 拒绝(退出码 2)本身即前置保护。
- C-19 命令产物(新建档案、追加库行)均为可逆写入,故全程 MUST 自动执行,并在收尾出具**三要素执行报告**,判据与三要素定义见 `.specify/shared/guidelines/confirmation-gates.md` §执行报告(引用,不复述):① 执行内容 ② 产出/变更工件(逐项可定位路径)③ 修改途径。
- C-20 琐碎写入(如一条 `moves-add` 追加)MUST 并入收尾报告逐项列明,MUST NOT 各出一份完整三要素报告(判据文档「琐碎并入」条);仅本命令主要产出(`derive.md`)独立出完整报告。

## 5. 能力降级条款(强制)

- C-21 模板 MUST 含一条独立的能力降级条款,声明:宿主 CLI 不具备任何线上检索或抓取能力时,命令 MUST NOT 编造核实 —— 全部来源标 `unverified` 且理由为 [[STR-007]],可锚定步骤数为 0,运行在建链前停止并输出降级说明,MUST NOT 产出任何架构(FR-007 / SC-005)。
- C-22 该条款 MUST 明示「降级是诚实的空产物,不是失败」,并 MUST NOT 提供任何绕过路径(如「无线上能力时可依据既有知识推导」);措辞 MUST 避开 C-17 的地雷(用「stop and report」而非「stop and confirm」)。
- C-23 Preflight 阶段 MUST 探测三态:`python3` 可用、引擎脚本存在、线上能力是否存在;第三项缺失 MUST 走 C-21 的降级路径而非中止,前两项缺失 MUST 给出 actionable 提示后停止(引擎三态探测惯例)。

## 6. 分发面客户中性

- C-24 随框架分发的文件(`templates/` 与 `shared/`)MUST 保持客户中性(FR-037):模板 MUST NOT 含特性或需求编号(`Feature 049`、`048-derive-command`),MUST NOT 含真实语料的 URL 或标题。
- C-25 模板中出现的示例 MUST 为**槽位化合成形式**(`S-001` / `M-001` / `D-1` / `A-1` / `Q-1`、`<topic-slug>`、`https://example.invalid/<path>`),MUST NOT 引入 handed-in 阅读清单里的任何真实条目。**理由**:真实 URL 与标题一旦进入 `templates/` 就随包分发一份会腐烂的语料(该清单已含一个死链),并预判了本应保持中性的领域(见 `requirements.md` §Clarifications 末条设计裁定)。
- C-26 同一中性约束适用于概念锚 `shared/definitions/derivation-definitions.md`:锚中的示例形状 MUST 保持槽位化(其 `inference_form` 示例以 `P` / `D` 为槽位即合规形态),契约测试 MUST 对 `templates/commands/derive.md` 与 `shared/definitions/derivation-definitions.md` 两文件同时断言不含 `http://`/`https://` 真实域(允许 `example.invalid`)与不含 `Feature \d{3}` / `\b04[89]\b` 编号形态。

## 7. 与 /speckit.research 的边界

- C-27 模板 MUST 含一条显式边界声明:本命令产出**方法层**(可跨领域重放的推理模式),`/speckit.research` 产出**结论层**(特性范围内的决策与理由);需要特性范围内的证据与选型时用 `/speckit.research`,需要从一个主题推导架构时用本命令。边界表归概念锚 §Derivation vs Research vs Plan,模板 MUST 引用而非复述。
- C-28 边界声明 MUST 含依赖方向:Plan MAY 以 `A-<k>` 身份引用架构元素;Derivation MUST NOT 引用 Plan(依赖单向,由特性绑定物指向主题绑定物)。
- C-29 `## Handoffs` MUST NOT 把 `/speckit.research` 列为后继(二者是替代关系而非接续关系),避免把方法层产物洗成结论层输入。

## 8. 接线与登记义务

- C-30 命令属**复杂命令**:MUST 携带 `## Feedback` 步(引用 `shared/workflow/feedback-step.md`,内联 `feedback-utils.py --action record` 调用,`--unit-id "/speckit.derive"` `--unit-type command`),MUST 携带字面 `feedback-utils.py`(分类测试的稳定标记)。
- C-31 `shared/definitions/probe-definitions.md` 的 Objects 表 MUST 新增一行,四列格式逐字为 `| speckit-derive-wrapup | command-wrapup | /speckit.derive | wrap-up |`([[STR-005]]);`feedback-utils.py --action probes --validate` MUST 退出 0,internal 计数较基线 +1(72 → 73),`--action probes --reconcile` 的错误集 MUST NOT 因本命令扩大。
- C-32 实现批次 MUST 完成:`regen-command-copies.py` 传播 4 份副本(`.claude/commands/speckit.derive.md`、`.github/prompts/speckit.derive.prompt.md`、`.qoder/commands/speckit.derive.md`、`.opencode/command/speckit.derive.md`),每份 MUST 携带指向 `templates/commands/derive.md` 的 `AUTO-GENERATED` 标记;`sync-mirrors.py --check` 退出 0;`docs/reference/commands/derive.md` 用户文档;`.specify/memory/tools/derive-utils.py.md` Tool 记录;`shared/definitions/framework-map.md` 新增 `.specify/derive/` 一行(FR-038,行形见 `contracts/move-library.md` C-35)。
- C-33 AGENTS.md 的 Documentation Map MUST NOT 新增行(Command Reference 整目录已由单行覆盖);`.specify/instructions.md` 由 `/speckit.instructions` 再生成,MUST NOT 手改。

## 9. 契约测试锚点

- C-34 `tests/contract/test_derive_command_surface.py` MUST 断言:C-1 键集与 `scripts:` 缺席;C-3 的 ≤50 字符;C-6 七章节恰序且无多余 `##`;C-11 的终止阶段与 [[STR-008]] 引用存在;C-12 的三条新红线(处置非库状态、限定 `anchor` 形式、A12 两半)各有可匹配文本;C-13 根相对引用存在;C-14 含字面 `never restate`;C-21/C-22 降级条款与 [[STR-007]] 字面量存在;C-24/C-25 中性断言;C-26 对模板与概念锚两文件的中性断言(FR-037 的度量面);C-27 边界声明存在;四份副本存在且含 `AUTO-GENERATED`;C-11 的六动作与阶段一一对应;`shared/definitions/framework-map.md` 含恰一行 `.specify/derive/`(FR-038 的度量面,行形见 `contracts/move-library.md` C-35)。
- C-35 门控零匹配 MUST 由**真实扫描器**断言(不得用自建正则):运行 `scan-confirmation-gates.py --root . --json`,过滤 `file == "templates/commands/derive.md"` 的 gates MUST 为空列表;`total` MUST ≤ 23.25。
- C-36 节序断言 MUST 复用 `test_docs_step_injection.py` 的既有断言路径(把 `derive` 加进其 `COMPLEX_COMMANDS`),MUST NOT 在新测试里另写一套节序逻辑 —— 第二套逻辑就是第二处真源。
