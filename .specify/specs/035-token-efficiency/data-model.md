# Data Model: 035-token-efficiency

**Source**: [requirements.md](requirements.md) Key Entities | **Date**: 2026-08-02

## 1. Token 效率纪律文档(Token-Efficiency Discipline Doc)

单一事实源:canonical `shared/guidelines/token-efficiency.md`(镜像 `.specify/shared/guidelines/`)。

| 字段/节 | 内容 | 约束 |
|---------|------|------|
| 程序优先(Program-First) | 固定规则判断类型清单(模式匹配、结构校验、计数、去重、排序、比对)+ MUST 交程序规则 | 与 Tool 复用门(宪法 XII)互引,不复制其定义 |
| 摘要优先(Summary-First) | 机器管理数据文件清单 + 原文整读禁令 + 例外情形 (a)(b)(c) | 例外三情形与 FR-003 逐字对齐 |
| 升级阶梯(Escalation Ladder) | 摘要 → 定向节选 → 有界整读;整读须例外情形或记录理由 | 三级顺序不可跳级(小文件/编辑目标除外) |
| 小文件阈值 | 默认 ≤ 100 行 且 ≤ 10 KB(双条件同时满足);允许场景覆盖 | 唯一定义点;他处仅引用 |
| 判定边界 | 何为"语义级判断"(归 LLM)与存疑时的处理(允许 LLM + 记观察) | 防过度应用 |
| 消耗观察 | 自评三问(原文转储?LLM 代做确定性工作?重复读取?)+ 标记 [[STR-001]] 约定 + 不编造数值规则 | 与 feedback-step.md 扩展互引 |

## 2. 违规清单(Violations Inventory,`audit.md`)

实施期产物,落本 spec 目录。行模式:

| 字段 | 类型 | 约束 |
|------|------|------|
| ID | `V-NNN` | 唯一,递增 |
| 单元 | 命令/技能/共享工作流路径 | canonical 路径(非镜像/副本) |
| 违规纪律 | `program-first` \| `summary-first` | 二选一;双违规拆两行 |
| 证据 | `file:line` + 违规指令原句摘录 | 可复核 |
| 注入量代理 | 行数 + 字节(被整读文件的实测值) | `wc -l` / `wc -c` 实测,不估算 |
| 触发频率 | `high`(每次 SDD 流程) \| `medium`(常用命令) \| `low`(边缘) | 按单元调用场景判定 |
| 严重度 | 触发频率 × 注入量的排序名次 | 排序依据,全清单唯一名次 |
| 状态 | `open` → `remediated`(top 5) \| `backlogged`(其余) | 状态机见下 |

**状态机**: `open` —(本期整改,附前后注入量对比)→ `remediated`;`open` —(名次 > 5)→ `backlogged`(留档后续迭代)。禁止:清单冻结后新增/删除行(与证据纪律"候选冻结"同向)。

## 3. Token 观察反馈条目(Token-Efficiency Self-Assessment)

复用既有反馈条目结构(frontmatter: id/unit_id/unit_type/run_id/scope/feature/partial/created/summary + `## Review` + `## Optimization Points`),零新字段。

| 约定 | 规则 |
|------|------|
| 标记 | Token 观察类优化点的条目行 MUST 内嵌字面量 `token-efficiency`([[STR-001]]) |
| 干净运行 | 无可避免消耗时 MUST NOT 追加 Token 观察点(沿用"无显著优化点"句式) |
| 数值口径 | 定性描述或行/字节代理;MUST NOT 出现编造的 Token 计数 |
| 检索 | `feedback-utils.py --action list --contains token-efficiency`(程序侧全文匹配,见 contracts/feedback-marker.md) |
| 聚合 | 证据 feedback 泳道照常消费;重复观察呈现 recurrence 信号(复用 038 机制,零改动) |

## 4. 引擎摘要能力矩阵(Engine Summary-Mode Matrix)

审计输入基线(Phase 0 实测;审计时以动态探测复核):

| 引擎 | 摘要/查询模式 | 缺口判定 |
|------|---------------|----------|
| feedback-utils.py | `list`(summary 字段 + unit/since/limit 过滤) | 本期补 `--contains` 文本过滤 |
| memory-utils.py | `recall` 评分检索 | 无缺口(参考范式) |
| evidence-utils.py | `list`/`latest`/`compare` | 无缺口 |
| docs-utils.py | `scan`/`stats` | 无缺口 |
| history-utils.py | 仅 `extract` 整会话转储 | **缺摘要模式**——列入审计候选,是否本期整改由 top-5 名次定 |
| glossary-utils.py | `list` 全表 | 小文件豁免候选(glossary 通常低于阈值) |
| tools-utils.py / skills-utils.py | `record-load`/`skill-read` 全文 | 多为编辑目标(例外 (a)),按审计逐项判定 |

## 5. 创作门槛检查项(Authoring Gate Items)

| 落点 | 形式 |
|------|------|
| `skills/create-skills/references/skill-creation-quality-checklist.md` | 新检查组:确定性步骤交程序?数据访问摘要化?(引用纪律文档) |
| `skills/improve-skills/references/skill-quality-checklist.md` | 同上(改进侧对偶) |
| `skills/create-agent/SKILL.md`、`skills/create-team/SKILL.md`、`skills/create-tools/SKILL.md` | 各自验证步骤加一行检查项引用(不复制定义) |

**关系图**: 纪律文档 ←引用— feedback-step 扩展 / 创作检查单 / instructions-template ambient 节;纪律文档 —判据→ audit.md 违规行;audit.md top-5 —整改→ 命令模板(经镜像扇出);反馈条目 —[[STR-001]] 标记→ `list --contains` 检索 → improve-* 消费。
