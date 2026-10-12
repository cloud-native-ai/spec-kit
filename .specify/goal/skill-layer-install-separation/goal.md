---
status: achieved
created: 2026-10-09
updated: 2026-10-12
---

# Goal: skill-layer-install-separation

## Objective

spec-kit 的技能完成 internal/external 分层落地与安装分流:源树按内外两层组织、全仓引用一致;客户项目只获得并注册 external 技能,internal 技能以 .specify/skills/internal/ 嵌套下发、对客户 agent 不可见、仅供 /speckit.* 工作流按显式路径消费;框架自身两态齐备,镜像、安装、打包与测试工具链整链适配。

## Success Criteria

1. 源树与运行时双布局按内外两层一致落地:全仓引用与所在层匹配;镜像、安装、打包三引擎按两层映射工作,各自 --check 退出 0
2. 分流行为可验证:平铺发现面只注册 external 技能、internal 技能经 .specify/skills/internal/ 显式路径可解析(两条守卫测试为证);全量测试同口径 A/B 零新增失败,门控扫描 total ≤ 23

## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | create-skills 与 improve-skills 完成去 .specify 化,技能以通用 skills 根为主、Spec Kit 集成为可选 | done |
| T-002 | 技能源树完成 internal/external 双层重家(32 实体各归其位),重家后引用面完成全量适配 | done |
| T-003 | 镜像、安装与打包工具链完成两层映射与旧装迁移,两布局各自自洽 | done |
| T-004 | 测试适配、两条守卫测试与本仓自用运行时刷新全部落地 | done |

## History

- 2026-10-09 — created.
- 2026-10-09 — criteria changed; prior value: None provided.
- 2026-10-09 — criteria changed; prior value: 源树与运行时双布局按内外两层一致落地:全仓引用与所在层匹配;镜像、安装、打包三引擎按两层映射工作,各自 --check 退出 0
- 2026-10-09 target T-001 added: create-skills 与 improve-skills 完成去 .specify 化,技能以通用 skills 根为主、Spec Kit 集成为可选
- 2026-10-09 target T-002 added: 技能源树完成 internal/external 双层重家(32 实体各归其位),重家后引用面完成全量适配
- 2026-10-09 target T-003 added: 镜像、安装与打包工具链完成两层映射与旧装迁移,两布局各自自洽
- 2026-10-09 target T-004 added: 测试适配、两条守卫测试与本仓自用运行时刷新全部落地
- 2026-10-09 — criteria changed; prior value: 分流行为可验证:平铺发现面只注册 external 技能、internal 技能经 .specify/skills/internal/ 显式路径可解析(两条守卫测试为证);全量测试同口径 A/B 零新增失败,门控扫描 total ≤ 23
- 2026-10-12 target T-001 open→done
- 2026-10-12 target T-002 open→done
- 2026-10-12 target T-003 open→done
- 2026-10-12 target T-004 open→done
- 2026-10-12 — status active -> achieved.
