---
id: "20261016T180912Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "run-improve-skills-20261017-020911"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-16T18:09:12Z"
summary: "improve-skills sdd-project-setup: 用户两要求全落地——①幂等/调协:SKILL.md 幂等契约+HR-6 收敛条目,setup-recipes 新增'幂等与重入语义'节(收敛契约 N 次=1 次+9 命令逐条重入语义表+--force 破坏性守卫+稳定态快路径);研究发现其 S3+ 强化序列已有每命令触发条件(缺什么才跑),真正缺的是整体收敛契约成文与 --for"
---

## Review
improve-skills sdd-project-setup: 用户两要求全落地——①幂等/调协:SKILL.md 幂等契约+HR-6 收敛条目,setup-recipes 新增'幂等与重入语义'节(收敛契约 N 次=1 次+9 命令逐条重入语义表+--force 破坏性守卫+稳定态快路径);研究发现其 S3+ 强化序列已有每命令触发条件(缺什么才跑),真正缺的是整体收敛契约成文与 --force 重入守卫;②并发冲突检查:他會話的强化序列分层建立在本 session 已提交态之上(委派节/S4 引用完好保留,neutrality 字面他们同向修复),50/50 钉住测试实证零语义冲突,唯一交叉点 Discipline 命令清单扩展为子串包含(断言不破);shape exit 0/redline PASS/契约 50 绿/镜像同步

## Optimization Points
- 并发 session 对同一技能的增量分层(强化序列)与本 session 的委派化坍缩天然正交——分层式协作下冲突面收窄到交叉引用一行;skill-shape 的 flags-outside-contract 警告为基线既有(Loop 块 --force/--here)未新增
