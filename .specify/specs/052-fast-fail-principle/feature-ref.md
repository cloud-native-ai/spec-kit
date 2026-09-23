# Feature Reference: 快速失败纪律(Fast Fail)

**Date**: 2026-09-23  
**Requirement**: `052-fast-fail-principle`  
**Bound Feature**: **052** 快速失败纪律(Fast Fail)  
**Feature Detail**: `.specify/memory/features/052.md`  
**Index Row**: `.specify/memory/features.md` — 由 `/speckit.clarify`(2026-09-22)创建,`Total Features` 51 → **52**(手工编辑;`update-feature-index.sh` 与 `AGENTS.md` 对其行为的描述矛盾,属上游缺陷,051 亦全程手工编辑)

## 绑定摘要

**新建 Feature 052,不绑定既有 Feature**(用户于 clarify 2026-09-22 裁定)。同胞吸收启发式逐个核验 6 个候选后,无既有 Feature 拥有本需求引入的能力:028(同胞吸收最强,但其 3 个同胞讲的都是反馈机制本身,而 FR-040/043/046 明令不扩展其引擎、probe 与自省路径)、046(经 FR-028 判定与本纪律**正交**,且明令不向其治理保留清单增行)、051(被消费的拥有者,非超集)、040 与 032(**归属判定的决定性先例**:同为"纪律真源 + 常驻章节 + 契约守卫"形态却各自成 Feature,确立"以指令段形式嵌入是投递事实、不是归属事实")、以及四份无注册 Feature 行的纪律真源文档。完整候选表与理由见 `requirements.md` › `## Related Feature`。

**状态推进**: `Draft` → **`Planned`**(本轮 `/speckit.plan` 推进;MUST NOT 落 `Implemented`,该转换归 `/speckit.implement`)。

**状态取值的上游分歧**:`feature-integration.md:33` 状态机规定 `/speckit.requirements` → `Draft`,而 `:68` 整合职责规定 `keep Status at least Planned`。clarify 轮取更具体的一方(状态机逐命令列出了该行)记为 `Draft`;本轮按状态机 `Draft → Planned` 推进。该矛盾属上游拥有者文档缺陷,已记入 `features/052.md` › Future Evolution Suggestions,MUST NOT 由本特性顺手改写。

---

## FR → 契约条款映射

条款引用形态为 `<contract-file> C-N`;测试文件缩写:**DF** = `test_fast_fail_discipline.py`(新增,承载 discipline-doc / ambient-section / dispatch-injection / gate-neutrality 四份的条款,函数名前缀分别为 `test_cN_*` / `test_aN_*` / `test_iN_*` / `test_gN_*`);**CD** = `test_constitution_double_landing.py`(既有,上调四钉);**UD** = `test_user_facing_comprehension_doc.py`(既有,上调 C-14 一钉)。

| FR | 主题 | 契约条款 | 测试文件 |
|---|---|---|---|
| FR-001 | 真源文档与命名 | discipline-doc C-1, C-2, C-3, C-9 | DF |
| FR-002 | 所有权三要素 | discipline-doc C-4 | DF |
| FR-003 | 失效陈述 | discipline-doc C-5 | DF |
| FR-004 | 镜像逐字节相等 | discipline-doc C-2;gate-neutrality C-17 | DF |
| FR-005 | 常驻顶级章节 | ambient-section C-1, C-2, C-5, C-6, C-7 | DF |
| FR-006 | 摘要+指针,不内联 | ambient-section C-3, C-8, C-9 | DF |
| FR-007 | 房子骨架 + 范围限制 | discipline-doc C-7, C-8, C-9, C-22 | DF |
| FR-008 | 项目中立 | discipline-doc C-21;ambient-section C-11;constitution-export C-12 | DF, CD |
| FR-009 | 二值判据 | discipline-doc C-10(b) | DF |
| FR-010 | 四条必要条件 | discipline-doc C-10(c) | DF |
| FR-011 | 机械测试 STR-005 | discipline-doc C-10(a) | DF |
| FR-012 | 存疑从严 | discipline-doc C-10(e) | DF |
| FR-013 | 上送极优先 | discipline-doc C-10(f) | DF |
| FR-014 | 两振升级 | discipline-doc C-10(g) | DF |
| FR-015 | 机器给出的绿 + STR-006 | discipline-doc C-12 | DF |
| FR-016 | fast fail 清单 + 7 项点名 | discipline-doc C-13, C-14, C-16 | DF |
| FR-017 | 顺手修复清单 | discipline-doc C-13 | DF |
| FR-018 | 封闭集 | discipline-doc C-13(d) | DF |
| FR-019 | 每条携判据 | discipline-doc C-13(c) | DF |
| FR-020 | 条数不设钉子 | discipline-doc C-14 | DF |
| FR-021 | 引用教训而非复述 | discipline-doc C-12, C-16 | DF |
| FR-022 | 四要素 | discipline-doc C-17(a) | DF |
| FR-023 | 上下文自足,引用可理解性纪律 | discipline-doc C-17 | DF + SC-008 读者测试 |
| FR-024 | 界面类 ⑪,排除 ① | discipline-doc C-6, C-17(c);constitution-export C-19…C-23 | DF, UD |
| FR-025 | 披露与粒度引用 | discipline-doc C-17(e) | DF |
| FR-026 | 停止粒度 | **无契约条款** — 见下"未覆盖的 FR" | 评审 |
| FR-027 | 无用户通道时落盘 | **无契约条款** — 见下 | 评审 |
| FR-028 | 五处边界 | discipline-doc C-7(节在场) | DF(节级)+ 评审(内容级) |
| FR-029 | 既有实例点位收敛 | ambient-section C-16, C-17 | DF |
| FR-030 | 收敛范围有界 | ambient-section C-18 | DF |
| FR-031 | 宪章双落点 | constitution-export C-1, C-2, C-3, C-8…C-12 | CD, DF |
| FR-032 | 活动宪章 + 四钉同批 | constitution-export C-4, C-5, C-6, C-13, C-14, C-15 | CD |
| FR-033 | plan 模板零改动 | constitution-export C-16, C-17, C-18 | CD |
| FR-034 | 援引而非复述 | constitution-export C-11 | CD |
| FR-035 | 守卫的 22 项封闭枚举 | 全部四份契约文件(DF 的**存在**即其载体) | DF |
| FR-036 | 逐行零命中 + 相邻纪律以路径指称 | gate-neutrality C-3…C-8 | DF |
| FR-037 | 扫描器零改动 | gate-neutrality C-2, C-16 | DF |
| FR-038 | total 相等 | gate-neutrality C-9, C-10, C-10(a), C-11 | DF + 既有钉子(集合由 gate-neutrality C-10 单点拥有) |
| FR-039 | 镜像与副本由引擎产出 | gate-neutrality C-16, C-17 | DF |
| FR-040 | 观察标记 | discipline-doc C-18(a) | DF |
| FR-041 | 两条红线 | discipline-doc C-18(b) | DF |
| FR-042 | 决定信号词汇引用 | **无专门条款** — 见下 | 评审 |
| FR-043 | 复用既有 probe | discipline-doc C-18(f) | DF |
| FR-044 | 双向生长规则 | discipline-doc C-18(c) | DF |
| FR-045 | 留痕 | discipline-doc C-18(d), (e) | DF |
| FR-046 | 自省入口复用 | discipline-doc C-18(f) | DF |
| FR-047 | 派发期义务,不复述可见性契约 | dispatch-injection C-17, C-18 | DF |
| FR-048 | 子句三项内容 + 长度上限 | dispatch-injection C-3, C-4, C-5 | DF |
| FR-049 | 子句标识字面量 | dispatch-injection C-2 | DF |
| FR-050 | 三条通道 + 通道二绑定制作者要求 | dispatch-injection C-8…C-16 | DF |
| FR-051 | 不新增共享前导文件 | dispatch-injection C-4(间接) | DF + 评审 |
| FR-052 | 守卫钉死的副本 + 成对定界符 | dispatch-injection C-1, C-10 | DF |
| FR-053 | 派发前自检 + 时点分流 | dispatch-injection C-19, C-24 | DF + 变异演练 |
| FR-054 | 回传显式异常行 | dispatch-injection C-20 | DF |
| FR-055 | 异常停 ≠ 普通失败 | dispatch-injection C-21 | DF |
| FR-056 | 上送件所有权分层 | dispatch-injection C-20(间接) | DF + 评审 |
| FR-057 | 三模式同等成立 | dispatch-injection C-22 | DF |
| FR-058 | 调用方义务,不改包装器 | dispatch-injection C-22;gate-neutrality C-16 | DF |
| FR-059 | 派发链逐跳 | dispatch-injection C-23 | DF |
| FR-060 | 子句优先于定义正文 | dispatch-injection C-23 | DF |
| FR-061 | 守卫增断言 + 有界集合 | dispatch-injection C-12 | DF |
| FR-062 | 收敛有界 + 诚实标注不可测面 | dispatch-injection C-26;ambient-section C-18, C-19 | DF |
| FR-063 | 三标记互斥 | discipline-doc C-20 | DF(red-first 期即可断言) |
| FR-064 | 不得为躲模式改语义 | gate-neutrality C-12 | DF |
| FR-065 | 规避改写触发复跑并留痕 | gate-neutrality C-13 | DF |
| FR-066 | 缺异常行即不完整 | dispatch-injection C-20, C-24 | DF + 变异演练 |
| FR-067 | 干净运行显式陈述 | discipline-doc C-17(d);dispatch-injection C-24 | DF + 变异演练 |
| FR-068 | 封闭处置集 | discipline-doc C-17(b) | DF |
| FR-069 | 上送件自身携标记 | discipline-doc C-18(a) | DF |
| FR-070 | 判据优先于清单命中 | discipline-doc C-10(d) | DF |
| FR-071 | 排除既有全部失败规则 | dispatch-injection C-21 | DF |
| FR-072 | 两条孤儿边界情形获载体 | discipline-doc C-7(`## 冲突裁决顺序` 节在场) | DF(节级)+ 评审 |
| FR-073 | 爆炸半径可判定定义 | discipline-doc C-11 | DF |
| FR-074 | canonical 指针行 | discipline-doc C-6 | DF |
| FR-075 | 四条缺失处置规则 | discipline-doc C-7(`## 冲突裁决顺序` 节在场) | DF(节级)+ 评审 |
| FR-076 | 清单条目语法 | discipline-doc C-13(b) | DF |
| FR-077 | 不得声称假的恢复路径 | ambient-section C-13, C-14, C-15 | DF |
| FR-078 | 已接受代价显式记录 | discipline-doc C-22;gate-neutrality C-14, C-15 | DF |

**覆盖统计(派生,不手写)**:主映射表与下方"未覆盖"表**各含一次**这 7 条 FR,故按行计数会得 85;唯一 FR 数 MUST 以去重命令派生:

```bash
grep -oE '^\| FR-[0-9]{3} \|' feature-ref.md | sort -u | wc -l   # → 78
```

**78** 与 `requirements.md` 的 FR 总数(`grep -c '^- \*\*FR-[0-9]'` → 78)**相等**,且无遗漏、无多余、无重复。其中 **71 条**有条款级承载,**7 条**列入下表——该 7 条再分两档:**3 条完全无契约条款**(FR-026 / FR-027 / FR-042),**4 条只有节级或间接承载**(FR-051 / FR-056 / FR-072 / FR-075,由 `discipline-doc.md` C-7 的节在场断言或 C-4/C-12 间接覆盖,内容级需语义判断)。

### 未由契约条款覆盖的 FR(7 条),各有其理由

| FR | 为何不可由契约测试覆盖 | 替代取证 |
|---|---|---|
| FR-026 | 停止粒度是**运行期行为**,无落盘制品可断言;且其规则本身是"引用既有并行规则",而既有规则已由其自己的守卫覆盖 | 评审 + `quickstart.md` 场景 6 的演练形态 |
| FR-027 | "无用户通道时落盘失败报告"是**运行期分支**,其触发条件(宿主无交互通道)在契约测试环境中不可构造 | 评审 |
| FR-042 | 决定信号词汇归既有门控观察协议拥有,本纪律只**引用**;断言其内容会构成对该拥有者的复述 | 评审(断言"引用在场"已由 discipline-doc C-7 的节级断言间接覆盖) |
| FR-051 | "MUST NOT 新增共享前导文件"是**负面命题且对象不存在**——断言一个不存在的目录不被创建,等价于断言 `agents/` 下无新增共享资产目录,可由 C-12 的有界集合断言间接达成 | dispatch-injection C-4 + C-12(间接)+ 评审 |
| FR-056 | 上送件所有权分层是**角色间约定**,无单一方制品可断言 | 评审 + data-model E19 |
| FR-072 | 两条孤儿边界情形的**内容**在真源文档的 `## 冲突裁决顺序` 节内,节级断言可覆盖其存在,内容级需语义判断 | discipline-doc C-7(节级)+ 评审 |
| FR-075 | 同上:四条处置规则的**内容**需语义判断 | discipline-doc C-7(节级)+ 评审 |

**诚实标注(FR-062 / dispatch-injection C-26)**:上述 7 条加上通道一的运行期履行,构成本特性**不可由契约测试观测**的面。`plan.md` 与本文件 MUST 如实标注该边界,MUST NOT 声称"全部 FR 均由守卫覆盖"——声称覆盖了实际覆盖不到的东西,正是本纪律要治理的盲检类失效。

---

## SC → 产出与度量映射

| SC | 度量对象 | 产出 / 验证任务 | 基线(实测) |
|---|---|---|---|
| SC-001 | 双评审者分流结论一致率 100% | ≥10 个异常场景样本,两个互不共享上下文的只读子代理独立评审,逐场景对照表落盘 | 不适用(判据今天不存在) |
| SC-002 | 7 项已实测失效的清单覆盖率 7/7 | discipline-doc C-14 逐项断言 `FF-2`…`FF-8` | **0/7**(`FF-n` 前缀在框架目录 0 命中) |
| SC-003 | 独立措辞定义点数 = 1 | discipline-doc C-21 之外的单源扫描(形态同 `test_one_source_of_truth.py:142-153`)+ ambient-section C-18 余集断言 | 不适用 |
| SC-004 | 模板与活动文件顶级章节集合差 = 0 | ambient-section C-1…C-7;既有 `test_instructions_section_propagation.py` | 模板 **18** 节 / 活动 **19** 节 |
| SC-005 | total 与冻结基线相等、violations 0、扫描器零改动、新增文本 0 命中 | gate-neutrality C-1…C-11;`quickstart.md` 场景 4(**改前即可完整实跑**) | total **23** / destructive **13** / governance_kept **10** / violations **0** / `BLOCKING_PATTERNS` **17** / `POLICY_DOCS` **2** |
| SC-006 | 双落点各命中 1、活动宪章 +1、版本 ≥1.13、plan 模板 0 改动而门控行 +1 | constitution-export C-1…C-18;`quickstart.md` 场景 3 | 模板 **13** / 活动 **15** / 命令 **7** / 版本 **1.12.0** |
| SC-007 | 标记可检索;每次清单移动留痕率 100% | discipline-doc C-18, C-20;`quickstart.md` 场景 8 | `--contains "[fast-fail]"` → `count: 0` |
| SC-008 | 读者能选出一项处置并说明理由,100% | 独立子代理读者测试(以可理解性纪律的基准读者定义为准) | 不适用(上送件今天不存在) |
| SC-009 | 披露率 100%、打断 0、干净运行显式陈述在场率 100% | discipline-doc C-17(d);`quickstart.md` 场景 6 同款演练 | 不适用 |
| SC-010 | 既有实例点位各含且仅含 1 行指针,正文改写 0 行 | ambient-section C-16, C-17(按**文件名**定位,不按行号) | 改前 8 个点位均无指针 |
| SC-011 | 三通道覆盖率 3/3;副本字节相等率 100% | dispatch-injection C-1…C-16;`quickstart.md` 场景 5 | **0/3**(定界符命中文件数 0;载荷字段 5) |
| SC-012 | 派发前自检的变异演练四步取证齐全 | dispatch-injection C-24, C-25;`quickstart.md` 场景 6 | 不适用(今天无自检) |
| SC-013 | 编排者侧 100%(可断言);子代理侧度量不设阈值 | dispatch-injection C-20, C-24 | 不适用(今天回传无异常行) |
| SC-014 | 异常停被原样重派的次数 = 0 | dispatch-injection C-21, C-24 | 不适用 |
| SC-015 | 三个数(快速失败率 / 用户推翻率 / 清单净生长方向)可导出 | discipline-doc C-19;D-16 的导出方式;零新增机制 | 不适用 |

**SC-001 / SC-008 的取证限制**:二者要求**未参与本特性实现的评审者**,单会话不可得。实现期 MUST 由独立子代理评审取证;若不可得,MUST 如实记为 `[~]` 并说明,**MUST NOT 编造通过率**(051 对同类 SC 记 `[~]` 是先例)。

---

## 交付面清单

| 交付面 | 落地物 | 再生方式 |
|---|---|---|
| 纪律真源 | `shared/guidelines/fast-fail.md`(**新**) | 手写;镜像由 `sync-mirrors.py` 产出 |
| 真源镜像 | `.specify/shared/guidelines/fast-fail.md` | `sync-mirrors.py --write`(**MUST NOT 手改**) |
| 常驻章节 | `templates/instructions-template.md` 新增 `## Fast Fail Discipline` | 活动文件由 `generate-instructions.sh` 再生 |
| 活动指令文件 | `.specify/instructions.md` | 再生;4 条兼容性符号链接(`AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md`)指向它,MUST NOT 手工重建 |
| 宪章模板原则 XIV | `templates/constitution-template.md` | 镜像由 `sync-mirrors.py` 产出 |
| 宪章命令条目 | `templates/commands/constitution.md` | 4 棵按工具树由 `regen-command-copies.py` 再生 |
| 活动宪章原则 XVI | `.specify/memory/constitution.md` + Sync Impact Report + 版本 1.13.0 | 手写(活动宪章不是镜像) |
| 通道二命令侧 | `templates/commands/agents.md` Run Mode | 4 棵按工具树再生 |
| 通道二技能侧 | `skills/create-agent/SKILL.md` 创作契约 | `.specify/skills/` 镜像 |
| 通道二制品 | `agents/skill-verifier.agent.md`、`agents/structure-adjuster.agent.md` | `.specify/agents/templates/` 镜像 + 3 棵按工具 agent 树渲染 |
| 通道三 | `skills/create-team/references/patterns.md` Per-Agent Payload 第六字段行 | `.specify/skills/` 镜像 |
| 派发期义务 | `shared/definitions/subagent-definitions.md` 新增节 | `.specify/shared/` 镜像 |
| 跨纪律登记 | `shared/guidelines/user-facing-comprehension.md` 类 ⑪ 行 | `.specify/shared/` 镜像 |
| 新守卫 | `tests/contract/test_fast_fail_discipline.py`(**新**) | 无镜像 |
| 上调既有钉子 | `test_constitution_double_landing.py`(四钉)、`test_user_facing_comprehension_doc.py`(C-14 8→9) | 无镜像 |
| **不改动** | `scripts/`、`src/specify_cli/`、`templates/plan-template.md`、`scan-confirmation-gates.py`、`dispatch.sh`、`feedback-utils.py` | — |

**再生顺序不可颠倒**:先 `sync-mirrors.py --write`(产出真源文档的 `.specify/` 副本),**再** `generate-instructions.sh`(再生活动指令文件)。反序会使常驻章节的指针在再生那一刻悬空——`generate-instructions.sh` 实测**不做**镜像同步(`research.md` D-17、FR-077)。
