# Feature Reference — Requirement 041 → Feature 028

**Requirement**: `041-refactor-feedback-probe`(Feedback 机制的 Probe 化重构)  
**Bound Feature**: Feature 028 Feedback Mechanism(Implemented;本需求为其核心模型重构,绑定裁定见 requirements.md `## Clarifications` Session 2026-08-14)  
**绑定依据**:Probe 概念仍属反馈域、消费方即反馈机制自身(027/036 扩展绑定、016 重构绑定先例);028 描述在交付时扩展覆盖 Probe 化模型。

## 映射表

| Feature 028 既有能力面 | 本需求的演进 | 承载 FR |
|------------------------|--------------|---------|
| 隐式 `## Feedback` 步(31 skills + 18 复杂命令) | 显式 Probe Class/Object 真源,49 埋点重构为 Object 并归类 | FR-001~004 |
| 条目自由文本、无切片 | 条目经 Object→Class 继承切片,可按切片/probe 过滤 | FR-005~007 |
| 无用户管理接口(只能手工调引擎) | `/speckit.feedback` 三模式命令(总览/处理含清理/注入) | FR-008~011 |
| 结构图缺位(只能通读模板归纳) | 派生 Probe 结构图,重建零漂移 | FR-012~013 |
| 旧条目永久留存 | 一次性整体 review 收敛(删除/重登记,留痕) | FR-014~015 |
| 四条红线(全局) | 按内外类别分级;外部 probe 面向宿主项目(Loop B) | FR-016~017 |
| 反馈仅覆盖框架自身 | 外部 probe 注入:宿主自定义 Skill/Agent/Command 本地反馈环 | FR-018~021 |

## Feature 记账义务

- `features/028.md`:追加「Planned(2026-08-14)」条目(本计划摘要);Status 保持 Implemented(无状态回退,036 先例)。
- `features.md` 行:Last Updated → 2026-08-14;Notes 增补 requirement 041 绑定记录。
- 交付时(`/speckit.implement`):028 Description 与 Key Changes 扩展 Probe 化模型;`docs/reference/skills/feedback.md` 同步。
