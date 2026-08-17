# Feature Reference: 042-goal-team-creation

**Bound Feature**: Feature 027 Team Management(`.specify/memory/features/027.md`)  
**Binding rationale**(2026-08-17 `/speckit.clarify` 裁定):主体改动面在团队域——`/speckit.team` create 路径、`team.md` 新增 `focus_target` 字段、创建期 territory 提议;goal 侧零新增操作面(分解批准复用既有 `targets --add`,不动 `goal.md` 结构与 goal 引擎的既有动作),与 036(team summary)扩展 Feature 027 的先例一致。

## 映射(本需求 → Feature 027 的能力面)

| 本需求交付 | Feature 027 能力面 |
|------------|---------------------|
| goal-based 创建分支(识别/加载/分析/路径裁决) | `/speckit.team` create 模式扩展(单一入口不变) |
| 分解提议集 + 成组批准(`--check` 干跑 → 逐条 `--add`) | create 模式的 goal 建立步骤获得"引用已定义 goal"形态(引用优先,内联可选) |
| 每 Target 一个团队(同 `goal_slug`、`focus_target`、slug 派生) | 团队静态/动态结构派生 + 持久化 schema 扩展(一个可选字段) |
| 创建期 territory 两两不相交校验 + coordinate 移交 | 团队级 territory 纪律(037 引入)从 summary 期检测前移到创建期预防 |
| run 侧解析(显式 > `focus_target` > 无)与披露 | run 模式 preview 门禁扩展一层输入解析(五查不变) |

## 概念真源(不在 Feature 027,不在本 spec 复述)

- Goal / Target / Goal–Team Binding / Target Decomposition:`shared/definitions/goal-definitions.md`(Feature 041 域)
- 本需求不修改 goal-definitions.md;若实现期发现概念表述缺口,回 `/speckit.goal` 域(Feature 041)处理

## 对相邻 Feature 的影响

- **Feature 041 Goal Registry**:零改动——`goal-utils.py` 只**新增** `--check` 动作与 `resolve_effective_target` 函数,既有动作/退出码/渲染逐字不变;`goal.md` 结构零变化。
- **Feature 036(team summary,经 027)**:零改动——切片轴卷积、里程碑、roster 均消费既有 `target_ref`/`focus_target` 不参与;summary 交付目录不变。

## 状态口径

Feature 027 维持 **Implemented**(no-status-regression gate,036 先例);本需求在其上叠加扩展,实现完成后由 `/speckit.implement` 在 027 的索引行/详情页追加"Extended by requirement 042 …(implemented)"记录,Feature 状态不回退、不升级。
