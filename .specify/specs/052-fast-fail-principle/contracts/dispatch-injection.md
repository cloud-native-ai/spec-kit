# Contract: 子代理派发注入 (dispatch-injection)

**Feature**: 052 快速失败纪律(Fast Fail)  
**Guards**: `requirements.md` FR-047…FR-062, FR-066, FR-071  
**Test file**: `tests/contract/test_fast_fail_discipline.py`(函数名 `test_iN_*`;条款号在本文件内独立编号,跨文件引用 MUST 写作 `dispatch-injection.md C-N`)  
**Date**: 2026-09-23

**可测性声明(诚实标注,FR-062)**:本文件的条款分两类。**制品类**条款断言落盘文本(注入子句的拥有者字面量、三份制品的副本、两处创作要求、一处载荷模式行、派发期义务节),可由契约测试断言。**行为类**条款描述编排者与子代理在运行期的动作(派发前自检、回传异常行、异常停不得重派、逐跳重新注入),其中**通道一的行为无制品可断言**,只能由真源文档载明义务 + 评审强制 + `quickstart.md` 的实跑场景取证。下表逐条标注类别,MUST NOT 声称行为类条款"由守卫覆盖"。

---

## 注入子句的拥有者字面量

**C-1** 真源文档 MUST 含**恰好一对**成对定界符 `<!-- fast-fail-clause:begin -->` / `<!-- fast-fail-clause:end -->`,且区间内文本非空。〔制品类〕

**C-2** 定界区间内的文本 MUST 含子句标识 [[STR-009]] = `fast-fail-clause`,使"子句是否在场"成为一次子串判定而非语义判断(FR-049)。〔制品类〕

**C-3** 区间内文本 MUST 同时承载三项必备内容,缺任一即红(FR-048):(a) 二值分流判据(纠正 / 裁定);(b) "需裁定时停在本层并回抛编排者、MUST NOT 就地修平"的义务;(c) 回传前缀 [[STR-010]] 及其**行首**判据。〔制品类〕

**C-4** 区间内文本 MAY 含真源文档路径 [[STR-002]],但 MUST NOT 以该路径**替代** C-3 的三项;守卫形态为 C-3 的三项各自独立断言,不因路径在场而短路(FR-048 / FR-051)。〔制品类〕

**C-5** 区间内文本 MUST **≤ 10 行 且 ≤ 1,200 字节**(D-2)。两个条件 MUST 同时满足。〔制品类〕

> *上限的来历:计划期的一份**草稿**子句实测为 8 行 / 933 字节 / 457 字符,上限取其向上留余量。该草稿不落盘、无命令可复现,故这三个数**不是可断言的判据**,只是上限的推导依据;可断言的判据只有 ≤10 行与 ≤1,200 字节两条。*

**C-6** 区间内文本的每一行 MUST NOT 命中 `BLOCKING_RE`。正则 MUST 以 `importlib` 从 `scripts/python/scan-confirmation-gates.py` 载入取真,MUST NOT 重抄其 17 条模式(重抄即副本,会漂移)。实测草稿 **0 命中**。〔制品类〕

**C-7** 反空真哨兵:C-5 与 C-6 均为"上界/空集"型断言,故 MUST 各配一条伴生非空断言——C-5 侧断言区间行数 ≥ 3(否则"≤10 行"可被空区间满足),C-6 侧断言 `len(BLOCKING_PATTERNS) == 17`(否则"0 命中"可被一个空正则满足)。〔制品类〕

## 三条通道的落点

**C-8** **通道二 · 制作者要求(命令侧)**:`templates/commands/agents.md` 的 `### Run Mode (subagent dispatch)` 节 MUST 含一条注入义务,指向真源文档;该节既有的 4 步序列(Resolve / Present & dispatch / Dispatch / Report)与 `**Scope boundary**` 段 MUST **逐字未变**。〔制品类〕

**C-9** **通道二 · 制作者要求(技能侧)**:`skills/create-agent/SKILL.md` 的创作契约 MUST 含一条"注入子句 MUST 在场"的要求;其既有的"六个必备正文节"与"`## Self-Improvement Contract` 恰好一次"要求 MUST 逐字未变。〔制品类〕

**C-10** **通道二 · 出厂预设**:`agents/skill-verifier.agent.md` 与 `agents/structure-adjuster.agent.md`(实测 `agents/*.agent.md` 恰为 **2** 份)MUST 各含**恰好一对** C-1 的定界符,且区间内文本与真源文档拥有者区间**逐字节相等**(V2)。〔制品类〕

**C-11** **通道二 · 镜像与按工具副本**:C-10 的两份源文件 MUST 与 `.specify/agents/templates/` 下的同名文件逐字节相等(改前实测该对为 `ok (2 files)`);**四棵**按工具 agent 树(`.claude/agents/`、`.qoder/agents/`、`.github/agents/`、`.opencode/agents/`,实测各 **2** 条目)由既有渲染路径再生,MUST NOT 手工编辑。渲染入口是 `src/specify_cli/__init__.py` 的 `render_agents_for_tool(project_path, tool)`,其 `tool` 键取自 `_AGENT_METADATA_MAPPING`:**`qoder` / `claude` / `copilot` / `opencode`**——注意 `.github/agents` 的键是 **`copilot`** 而不是 `github`,且该函数对未知键**静默返回 `rendered: 0` 而不报错**,故传错键会表现为"渲染成功但副本没变"。实现期订正:实为**四棵**(`.claude/agents`、`.qoder/agents`、`.github/agents`、`.opencode/agents`,各 2 条目);规划期误记为三棵,且把第四棵路径写成单数 `.opencode/agent` 而测得 0。〔制品类〕

**C-12** **通道二 · 有界性**:守卫的断言对象 MUST 是 C-10 枚举的**有界集合**(2 份出厂预设 + C-8/C-9 的两处创作要求文本),MUST NOT 试图枚举 `.specify/agents/instances/`(实测为空且由用户日后创建)。枚举一个无界集合的守卫要么漏要么恒红(FR-061 / D-3 裁定)。〔制品类〕

**C-13** **通道三 · 团队载荷**:`skills/create-team/references/patterns.md` 的 Per-Agent Payload 表 MUST 由 5 个字段行增至 **6** 个,新增行字段名为 `fast_fail_clause`,其内容规则 MUST 指向真源文档的拥有者字面量(D-3)。〔制品类〕

**C-14** 同文件的 Context Isolation Rules 四条 MUST **逐字未变**(实测改前为 `:105-108` 四条:不传对话历史 / 不共享其他 agent 的任务简报 / 不可见其他 agent 的中间结果 / 只接收自己的 territory manifest)。〔制品类〕

**C-15** **通道一 · 内联提示**:真源文档 MUST 规定子句在编排者当场撰写的提示中的落点与形态。该规定本身可断言〔制品类〕;**其运行期履行不可断言**(提示不落盘)〔行为类,见 C-24〕。

**C-16** 三条通道 MUST **不互斥**:真源文档 MUST 载明一次派发可同时经由通道一撰写提示并携带通道二的制品,且派发链的后续跳亦然(FR-050)。〔制品类〕

## 派发期义务与三个控制点

**C-17** `shared/definitions/subagent-definitions.md` MUST 新增一节派发期义务,与既有 `## External Dispatch Visibility Contract` **并列**;该既有节的 5 条编号义务与 `**Reference implementation**:` 行 MUST 逐字未变。〔制品类〕

**C-18** 新增节 MUST 载明二者的分工:可见性契约拥有"这次派发是否**可观测**",本节拥有"这次派发是否**受治理**";MUST NOT 复述可见性契约的任何一条(FR-047)。〔制品类〕

**C-19** 真源文档 MUST 载明**派发前自检**义务,含**按发现时点分流**的两条处置(FR-053 / D-2 裁定):派发前发现 → 顺手修复(补齐 + 收尾披露);派发后才发现 → 快速失败(MUST NOT 把该子代理产出当作可信证据继续消费)。〔制品类〕

**C-20** 真源文档 MUST 载明**回传显式异常行**义务:有异常则以行首 [[STR-010]] 逐条列出,无异常则明写 [[STR-013]];并 MUST 载明**缺行即一次异常**、判为不完整、MUST NOT 消费其结论(FR-054 / FR-066)。〔制品类〕

**C-21** 真源文档 MUST 载明**异常停 ≠ 普通失败**,且该排除 MUST 覆盖既有的**全部**失败规则——两振停滞、"连续两次派发失败即降级"、以及"非并行任务失败即停 / 并行任务成功者继续、失败者上报"(FR-055 / FR-071)。守卫形态为三个被排除规则各自的关键短语在真源文档中命中。〔制品类〕

**C-22** 真源文档 MUST 载明:注入义务对 native / virtual / external **三种执行模式同等成立**,且 virtual 模式 MUST NOT 因"会话本身持有常驻层"而豁免(FR-057);注入 MUST 是**调用方**的内容义务,MUST NOT 被实现进派发包装器(FR-058),据此 `skills/create-team/scripts/dispatch.sh` 与其流过滤脚本 MUST 零改动。〔制品类〕

**C-23** 真源文档 MUST 载明**派发链逐跳重新注入**(FR-059)与**注入子句优先于 Agent 定义正文**的裁决顺序,且该冲突本身 MUST 作为异常回抛、MUST NOT 由子代理自行择一(FR-060)。〔制品类〕

## 行为类条款的取证方式

**C-24** 下列义务**无制品可断言**,MUST 由 `quickstart.md` 的实跑场景取证,且其取证形态 MUST 为**变异演练**而非仅"当前树上通过":〔行为类〕

| 义务 | FR | 取证场景 |
|---|---|---|
| 派发前自检确实在派发之前发生 | FR-053 | quickstart 场景:从 outgoing 提示移除 [[STR-009]] → 自检 MUST 报缺失 → 复原 → MUST 通过 |
| 缺异常行的回传被判为不完整 | FR-066 | quickstart 场景:构造一条无异常行的回传 → 处置逻辑 MUST 判为不完整且 MUST NOT 消费其结论 |
| 异常停 MUST NOT 被原样重派 | FR-055 | quickstart 场景:构造一条行首 [[STR-010]] 的回传 → 后续动作 MUST 为"上送"或"记为未决项",MUST NOT 为重派 |
| 干净运行也显式说一句 | FR-067 | quickstart 场景:一次无异常无修复的运行,其收尾报告 MUST 含 [[STR-013]] 起首的陈述 |

**C-25** 变异演练的临时制品 MUST 删净并复核(计数归零);演练取证 MUST 记入实现期的 `notes/red-first-evidence.md`,MUST NOT 只在会话里口头声明。〔行为类〕

**C-26** 通道一的内联提示合规性由**评审**强制。真源文档与 `plan.md` MUST 如实标注这一边界;MUST NOT 出现"三条通道均由守卫覆盖"一类表述(FR-062;自陈条款见 `ambient-section.md` C-19)。声称覆盖了实际覆盖不到的东西,正是本纪律要治理的盲检类失效。〔制品类:断言该自陈在场〕

---

## 条款 → FR / SC 映射

| 条款 | FR | SC | 类别 |
|---|---|---|---|
| C-1…C-7 | FR-048, FR-049, FR-052, FR-063 | SC-011, SC-012 | 制品 |
| C-8…C-12 | FR-050, FR-061 | SC-011 | 制品 |
| C-13, C-14 | FR-050 | SC-011 | 制品 |
| C-15, C-16 | FR-050 | SC-011 | 制品(规定)/ 行为(履行) |
| C-17, C-18 | FR-047 | — | 制品 |
| C-19 | FR-053 | SC-012 | 制品(义务)/ 行为(履行) |
| C-20 | FR-054, FR-066 | SC-013 | 制品 / 行为 |
| C-21 | FR-055, FR-071 | SC-014 | 制品 / 行为 |
| C-22 | FR-057, FR-058 | SC-011 | 制品 |
| C-23 | FR-059, FR-060 | — | 制品 |
| C-24, C-25 | FR-053, FR-055, FR-066, FR-067 | SC-012, SC-013, SC-014, SC-009 | 行为(变异演练取证) |
| C-26 | FR-062 | — | 制品(自陈在场) |
