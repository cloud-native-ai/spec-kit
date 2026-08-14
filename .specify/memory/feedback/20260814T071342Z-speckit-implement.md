---
id: "20260814T071342Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "040-agent-metadata-portability-implement-2026-08-14"
scope: "local"
feature: "040-agent-metadata-portability"
feature_id: "044"
partial: false
created: "2026-08-14T07:13:42Z"
summary: "43 任务按 8 个 phase 边界提交全部完成(T036 因术语表协议需用户确认而 [~] 延迟):中立元信息核心 + 校验器、19 文件词汇中立化、渲染管线真实替代软链接(含 e2e init 验证)、迁移安全(R-7/R-8 两个缺陷由新契约测试红→绿驱动修复)、Worker/Meta 目录划分落位(7 角色迁移 + 2 Meta 预置 + 三目录分类法成文)。SC-001~008 全 p"
---

## Review
43 任务按 8 个 phase 边界提交全部完成(T036 因术语表协议需用户确认而 [~] 延迟):中立元信息核心 + 校验器、19 文件词汇中立化、渲染管线真实替代软链接(含 e2e init 验证)、迁移安全(R-7/R-8 两个缺陷由新契约测试红→绿驱动修复)、Worker/Meta 目录划分落位(7 角色迁移 + 2 Meta 预置 + 三目录分类法成文)。SC-001~008 全 pass(含 SC-004/006/007 三个实做演练),终态回归 37 failed = 基线 39 − 2(零新增,name-level comm 为空),sync-mirrors --check exit 0。Feature 044 Planned→Implemented 通过 Pre-Status-Flip Gate。

## Optimization Points
- **临时探针/演练脚本必须 finally 还原**:SC-004 演练第一次把探针注入错了锚点(命中 AGENT_CONFIG 的 hermes 而非映射表的 hermes),断言失败后未执行还原行,污染延续到下一轮演练才被 git diff 发现 —— 两次返工。教训:任何"注入-断言-还原"的演练脚本必须 try/finally 包裹还原,且锚点要用多行唯一上下文;tasks 里凡涉及"临时修改验证后还原"的演练(SC-004/SC-006 类)值得把这条写成固定注意事项。
- **sync-mirrors 的宽容模式不删镜像侧孤儿**:agents/ 删除 7 个文件后镜像残留,靠手工 \rm 清理(仓库经验已有记载,但每次迁移仍会踩)。建议给 sync-mirrors.py 增加一个显式 `--prune-orphans <pair>` 选项,把"迁移类变更"的孤儿清理从手工操作变成引擎能力。
- **generate-instructions.sh 不重建 Resource Registry 的 Agents 表**:迁移后注册表指向已删路径,生成器不修、/speckit.agents 不在场,只能手工补表 —— 生成物与手工维护的边界在这里是模糊的。建议在 registry 管理块注释里写明"谁负责刷新此表"(/speckit.agents 或 instructions 生成器),或让生成器对指向不存在路径的行给出警告。
- **token-efficiency**:本轮大量使用 python heredoc 做批量替换并当场 grep 验证新形态存在(符合 bulk-substitution 纪律);两处失败归因(断言侧 vs 被测侧)均先判定再动手,未发生错误方向的修复。可避免开销:docs 联动阶段多次 sed 读上下文才拼出精确替换串,若先用 Python 打印 repr 再替换可省往返(SC-004 第三次才成功的部分原因即拼串试错)。
