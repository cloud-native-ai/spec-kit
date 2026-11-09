# Feature Reference: 需求 046 → Feature 048

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill(浏览器自动化能力本体)

## 绑定裁定(2026-08-23,/speckit.clarify)

新建 Feature 048 而非绑定既有特性:浏览器自动化能力为独立能力域;013 Skills Command 仅覆盖技能管理编排(创建/优化/路由),不含各技能能力内容。013 详情文件已加反向交叉引用。同轮决策:敏感字段脱敏落盘(Q2);site/ 数据归调用方归档、框架仓 gitignore/wheel/镜像三处排除(Q3)。

## US → FR → 设计工件映射

| 用户故事 | FR | 设计工件落点 |
|----------|----|--------------|
| US1 探索期留痕 | FR-003/004/006 | data-model §1/§3;contracts/site-memory-formats §3/§4(脱敏);contracts/site-memory-engine(init/append-record);SKILL.md 路由段探索分支 |
| US2 分层与双方向路由 | FR-001/002/006/010 | SKILL.md 策略选择扩展(状态路由 + 页面级/请求级方向指引);references/site-memory.md;references/request-level-patterns.md |
| US3 优化期蒸馏 | FR-007 | data-model §4;contracts/site-memory-formats §5(recipe schema);site-memory-engine(write-recipe) |
| US4 验证期与 sealed | FR-005/008/009/010 | data-model §2/§5(状态机/证据);site-memory-engine(transition/record-validation);contracts/site-memory-formats §6 |
| 分发边界(Q3) | FR-003 | contracts/framework-exclusions(.gitignore / sync-mirrors / hatch_build 三收口) |

## 对 Feature 048 的 key changes(登记进 features/048.md 的实现注记)

1. 引擎面:`skills/browser-utils/scripts/site-memory.py`(stdlib-only,7 actions)×2 镜像。
2. 机制面:SKILL.md 增"站点记忆与双方向路由"段;新增 references/site-memory.md 与 references/request-level-patterns.md。
3. 框架面:.gitignore 两行;sync-mirrors skills 对排除 `site` 分量;hatch_build.py 舞台拷贝替代 pyproject 静态 skills force-include。
4. 测试面:tests/contract/test_browser_site_memory.py(状态机/脱敏/格式/三处排除)。

## 交叉引用义务

- features/048.md:状态 Draft → Planned,Key Changes 增记本计划要点。
- features.md:索引行注记追加 plan 落地摘要。
- 013(Skills Command):反向引用已在 clarify 阶段落地,本阶段无新增义务。
