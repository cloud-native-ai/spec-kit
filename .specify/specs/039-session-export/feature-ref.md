# Feature Reference: 039-session-export

**Requirement**: `039-session-export`(Session 导出与导出侧重命名)
**Bound Feature**: Feature 043 Session Export(Draft → Planned by /speckit.plan)
**Binding Decision**: `/speckit.clarify` 2026-08-12 裁决新建(非绑定 022/026——消费关系而非组成关系)。

## 映射关系

| 需求面 | Feature 043 能力面 |
|--------|--------------------|
| US1 导出为用户命名目录(P1) | 核心能力:导出侧命名(宿主无命名机制的降级路线落地) |
| US2 技能收敛六家 + 通用化(P1) | 执行面:`export-session` 从 10 产品私有技能收敛为框架通用技能 |
| US3 会话描述文档(P2) | 资产化:会话成为可检索项目资产(元信息 + 结构化总结) |
| US4 团队 run 追溯(P3) | 集成延伸:与 Visibility Contract 派发 label / run report 映射表衔接 |

## 相邻 Feature 关系

- **022 AI Tools Support / 021 Claude Code Support / 020 Qoder Support**:本 Feature 消费其支持的 CLI 会话存储,不修改其支持面。
- **026 Agent Skill Enablement**:export-session 改造遵循技能规范(SKILL.md frontmatter / references 纪律)。
- **027 Team Management**:US4 衔接 `/speckit.team` 外部派发追溯链(只读消费,不改派发机制)。
- **039 Harvested Harness Improvements / 038 Evidence Infrastructure**:描述文档是会话级证据资产的呈现,与 evidence 泳道无直接数据耦合(未来可评估接入,不在本需求)。
