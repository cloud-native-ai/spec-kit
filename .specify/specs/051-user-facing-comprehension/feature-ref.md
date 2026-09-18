# Feature Reference: 051 面向用户可理解性纪律

**Date**: 2026-09-17  
**Requirement**: `.specify/specs/051-user-facing-comprehension/requirements.md`(`051-user-facing-comprehension`)  
**Bound Feature**: **051 — 面向用户可理解性纪律(User-Facing Comprehension)**  
**Feature Detail**: `.specify/memory/features/051.md`  
**Index Row**: `.specify/memory/features.md`(Total Features 50 → **51**,手工编辑)

---

## 绑定摘要

`/speckit.clarify` Mode A 于 2026-09-17 裁定**新建 Feature 051**,不绑定既有 Feature。依据 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 的同胞吸收启发式,逐个核验 **8 个候选**后结论是无既有 Feature 拥有本能力。决定性先例是 **032 Task Complexity Rubric** 与 **040 Token Efficiency Discipline**——两者与本 Feature 形状完全相同(`shared/guidelines/` 纪律文档 + 指令模板常驻章节 + 契约测试守卫),都各自成为独立 Feature 而非绑到投递载体(008 Instructions Command),确立"以指令段形式嵌入是**投递事实、不是归属事实**"。

完整的 8 候选核验表见规格 `## Related Feature`;8 个候选以**消费关系**(交叉引用)记入 `.specify/memory/features/051.md` § 交叉引用,不构成归属。反向交叉引用已写入 `.specify/memory/features/040.md`(最接近的结构先例)。

**状态**: `Draft → **Planned**`(本命令拥有该转移,依 `.specify/templates/feature-details-template.md` § Canonical Status State Machine)。`/speckit.plan` MUST NOT 落 `Implemented`——那由 `/speckit.implement` 拥有。

**索引编辑方式**: **手工编辑**。`scripts/bash/update-feature-index.sh:150` 是 `cat > "$FEATURE_INDEX"` 整体重写,且 `:164` 输出的表头只有 **6 列**(缺活动索引实际使用的 `Spec Path` 列)⇒ 运行它会摧毁 Spec Path 列与全部手写散文。承 Feature 049/050 的既有记录,本轮已源码复核确认。
> **附带发现(不属本特性,已报告未修)**:`AGENTS.md` 的 Documentation Map 称 `Total Features` 计数"由 `scripts/bash/update-feature-index.sh` 维护",与脚本实际行为矛盾。目标文档 = `templates/instructions-template.md` 的 Feature Index 行(及其生成镜像 `.specify/instructions.md` / 根 `AGENTS.md`)。

---

## FR → 契约条款映射(38 条 FR 全覆盖)

| FR | 主题 | 契约条款 | 测试文件 |
|---|---|---|---|
| FR-001 | 唯一真源 + 所有权声明 | `discipline-doc` C-1, C-4, C-5 | `_doc` |
| FR-002 | 镜像逐字节相等 | `discipline-doc` C-2 | `_doc` |
| FR-003 | 常驻章节暴露(非表格行) | `ambient-section` C-1, C-2, C-3, C-7, C-8 | `_section` |
| FR-004 | 房子骨架 + RFC-2119 + 范围限制 | `discipline-doc` C-6, C-7, C-8 | `_doc` |
| FR-005 | 许可行话白名单(≥5 条) | `discipline-doc` C-9 | `_doc` |
| FR-006 | 禁用行话黑名单(≥4 条) | `discipline-doc` C-10 | `_doc` |
| FR-007 | "不能杜绝 jargon"落为可判定条件 | `discipline-doc` C-9(含"白名单之外一律违规") | `_doc` |
| FR-008 | 消费单元定义 | `discipline-doc` C-13 | `_doc` |
| FR-009 | 上下文下限(≥3 项) | `discipline-doc` C-11 | `_doc` |
| FR-010 | 上下文上限(≥3 约束) | `discipline-doc` C-12 | `_doc` |
| FR-011 | 定性上限 + 已接受代价成文 | `discipline-doc` C-12(含代价与升级路径) | `_doc` |
| FR-012 | 裁决顺序(≥2 条) | `discipline-doc` C-12 | `_doc` |
| FR-013 | 第三方可复现机械判据 | `discipline-doc` C-13 | `_doc` |
| FR-014 | 11 类界面封闭枚举 | `discipline-doc` C-14;`surface-pointers` C-1 | `_doc` / `_pointers` |
| FR-015 | 每类真源单行指针 | `surface-pointers` C-1, C-2 | `_pointers` |
| FR-016 | 全量同批接入(含两处搬家) | `surface-pointers` C-1…C-14 全体;`gate-neutrality` C-7 | `_pointers` |
| FR-017 | 门控判据各节逐字冻结 | `surface-pointers` C-4, C-5 | `_pointers` |
| FR-018 | `:68` 反馈专属规则提升为一般规则 | `surface-pointers` C-10;`discipline-doc` C-10(黑名单 ①) | `_pointers` / `_doc` |
| FR-019 | `feedback-step.md` 三处规则保留为实例 | `surface-pointers` C-10 | `_pointers` |
| FR-020 | 澄清补齐行话半侧 | `surface-pointers` C-1(clarify.md + requirements-guidelines.md 两行) | `_pointers` |
| FR-021 | 访谈模式收敛 + 两规则保留 + `:255` 清单 | `surface-pointers` C-6, C-7, C-8, C-9 | `_pointers` |
| FR-022 | 项目总结黑名单提升 | `discipline-doc` C-10;`surface-pointers` C-11, C-12 | `_doc` / `_pointers` |
| FR-023 | 机械副本走再生,不手工批改 | `surface-pointers` C-14 | `_pointers` |
| FR-024 | 宪章模板新原则结构 | `constitution-export` C-1, C-2, C-3, C-4 | `_double_landing` |
| FR-025 | 命令 `MUST include` 双落点 | `constitution-export` C-5, C-6 | `_double_landing` |
| FR-026 | 下游动态枚举自动传导(**实测验证**) | 不由契约断言 —— `quickstart` 场景 5b/5c | — |
| FR-027 | 活动宪章 + 版本 MINOR + Sync Impact Report | `constitution-export` C-11, C-12 | `_double_landing` |
| FR-028 | Principle XIV 回流 | `constitution-export` C-1, C-7, C-10 | `_double_landing` |
| FR-029 | 五表面守卫 + 同批加守卫 | 全部 5 份契约;`gate-neutrality` C-7 | 全部 |
| FR-030 | 项目中立性 | `discipline-doc` C-15;`ambient-section` C-9 | `_doc` / `_section` |
| FR-031 | 单源扫描(内容形态复述 = 0) | `surface-pointers` C-13 | `_pointers` |
| FR-032 | 扫描器豁免登记(**条件前提不成立**) | `gate-neutrality` C-1, C-2, C-3, C-4 | `_doc` / `_section` |
| FR-033 | 零新机制 | `discipline-doc` C-8;`gate-neutrality` C-5 | `_doc` |
| FR-034 | `:68` 提升后获契约断言 | `surface-pointers` C-10 + 扩展 `test_confirmation_gates_execution_report.py` | 既有文件扩展 |
| FR-035 | 具名双落点观察名单 | `constitution-export` C-7, C-8, C-9, C-10 | `_double_landing` |
| FR-036 | 观察标记 | `discipline-doc` **C-17**(断言观察约定存在 + STR-005 字面量 + 三条红线);标记的**实际内嵌**属运行时行为,不由契约断言 | `_doc` |
| FR-037 | 基准读者 + 按类覆盖协议 | `discipline-doc` C-13, C-14 | `_doc` |
| FR-038 | 同批抵达 + 悬空指针提示 | `ambient-section` C-11;`gate-neutrality` C-6 | `_section` |

**测试文件名缩写**: `_doc` = `test_user_facing_comprehension_doc.py`;`_section` = `test_user_facing_comprehension_section.py`;`_pointers` = `test_user_facing_comprehension_pointers.py`;`_double_landing` = `test_constitution_double_landing.py`。

**未由契约条款覆盖的 FR(1 条),有其理由**:
- **FR-026**(下游动态枚举自动传导)—— 需真实 bootstrap 一个下游项目,是端到端演练而非结构断言 ⇒ 落 `quickstart.md` 场景 5b/5c。FR-026 本身要求"实测验证而非假定",故不入契约。

> FR-036 曾在此列为第二条(理由是"属运行时行为"),经 `/speckit.analyze` 发现该说法与同表声称的"C-6 钉死该节存在"互相矛盾——C-6 的七节封闭元组内并无观察节。现已新增 `discipline-doc` **C-17** 专门断言观察约定,FR-036 移出本清单。

---

## SC → 产出与度量映射(18 条)

| SC | 度量对象 | 产出/验证任务 | 基线(实测) |
|---|---|---|---|
| SC-001 | 门控提示抽样通过率 100% | 人工评审(未参与实现者),`quickstart` 未覆盖 ⇒ `verification.md` | 0/13 门控附措辞义务 |
| SC-002 | 引擎调用形态泄漏 = 0 | `surface-pointers` C-13 单源扫描 + 人工抽样 | 规则仅覆盖 1 类界面 |
| SC-003 | 真源 1 份;内容形态复述 = 0 | `discipline-doc` C-1/C-2;`surface-pointers` C-13 | **38 处 / 0 真源 / 0 名字** |
| SC-004 | 8 文件各含且仅含 1 行指针 | `surface-pointers` C-1;`quickstart` 场景 4 | **0 / 8** |
| SC-005 | 下游含两条原则 100%;`plan-template.md` 改 0 行 | `constitution-export` C-1…C-6, C-11;`quickstart` 场景 5 | STR-003 0%、STR-006 0% |
| SC-006 | 双评审一致率 ≥90%(≥20 条样本) | 人工盲测 ⇒ `verification.md` | 不适用(今天无判据) |
| SC-007 | 建议行零长度膨胀 | `ambient-section` C-4(≤25 行)+ 改前后长度分布比对 | 既有单行约束已生效(防回归) |
| SC-008 | 裁决顺序覆盖 100%;空白类 = 0 | `discipline-doc` C-12(≥2 条,逐条对应已点名冲突) | 0 处和解成文 |
| SC-009 | 五表面守卫 100% + 变异式有效 | 全部 5 份契约;`constitution-export` C-10 变异抽查 | 0 表面受守 |
| SC-010 | 专有名称泄漏 = 0 | `discipline-doc` C-15;`ambient-section` C-9 | 不适用(文件尚不存在) |
| SC-011 | 新检查器/评分器/台账 = 0 | `gate-neutrality` C-5 | 0 |
| SC-012 | 门控计数完全不变 | `gate-neutrality` C-1…C-4;`quickstart` 场景 3 | **total 23 / 余量 0** |
| SC-013 | `:68` 提升后获断言 | `surface-pointers` C-10 + 扩展既有测试 | 0 条断言覆盖该子句 |
| SC-014 | 黑名单全框架可达 100%;独立副本 = 0 | `surface-pointers` C-11, C-12 | 1 份搁浅、0 处外部可达 |
| SC-015 | 观察名单两侧同时存在 100% + 变异式有效 | `constitution-export` C-7…C-10 | 0 条原则受此守卫 |
| SC-016 | 两处搬家既有行为回归 = 0 | `surface-pointers` C-4…C-9, C-14;`gate-neutrality` C-2, C-7;`quickstart` 场景 4/6 | 不适用(度量回归) |
| SC-017 | 悬空且无提示 = 0(覆盖全部 guideline) | `ambient-section` C-11;`quickstart` 场景 2 遍历核验 | 窗口存在但从未受测 |
| SC-018 | 读者基准声明总数 ≤3 | `discipline-doc` C-13, C-14 | 3 种并存、0 处声明为全局/覆盖 |

**人工度量项(3 条)**: SC-001、SC-006 需未参与实现的评审者;SC-007 的长度分布比对需改前抽样。三者的方法记在规格 `### Measurement Sources & Collection Methods`,结果落 `verification.md`。

---

## 交付面清单(本计划产出 → 实现期落地)

| 圈 | 落地物 | 数量 |
|---|---|---|
| 规范圈 | `shared/guidelines/user-facing-comprehension.md`(新)+ 8 个规则真源文件各加 1 行指针 + 3 处内容搬家 | 1 新 / 8 改 / 3 搬家 |
| 投递圈 | `templates/instructions-template.md` 新章节(17→18)、`templates/constitution-template.md` 两原则(11→13)、`templates/commands/{clarify,interview,constitution}.md`、`.specify/memory/constitution.md`(14→15,1.11.0→1.12.0) | 6 改 |
| 守卫圈 | `contracts/` 5 份(条款编号区间以各文件头部声明为准;跨文件总数 MUST 派生而非手写,派生方式见 `plan.md` § Phase 1 摘要)、`tests/contract/` 4 新 + 1 扩展 | 5 + 5 |
| 文档空间 | `docs/reference/` 3 处手写复述收敛(`docs/public/**` 由 Hugo 重建,不手改) | 3 改 |
| **零改动** | `src/specify_cli/`、`scripts/`(含 `scan-confirmation-gates.py`、`generate-instructions.sh`)、`templates/plan-template.md`、4 棵按工具树(仅再生) | 0 |

**再生目标(非编辑目标)**: `.specify/shared/`、`.specify/templates/`、`.specify/skills/`、`.specify/instructions.md`、`.claude/` `.github/` `.qoder/` `.opencode/` 的命令副本。全部经 `sync-mirrors.py --write` + `generate-instructions.sh` + `regen-command-copies.py`,MUST NOT 手改(两顶帽子纪律,Principle XI)。
