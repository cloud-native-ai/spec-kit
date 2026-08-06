---
id: "20260805T185310Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-local-store-review-20260806"
scope: "local"
partial: false
created: "2026-08-05T18:53:10Z"
summary: "本地 feedback 存储首次审阅闭环:99 条(19 单元)程序化 digest 后按复发度与证据强度分拣,覆盖检查剔除已吸收项,冻结 6 项候选全部落地(2 脚本缺陷修复 + 4 命令模板条款),sync-mirrors 一致、全量测试零回归;其余单次性/外仓项如实留待各单元下次运行。随后 mark-submitted 归零计数器。"
---

## Review
本地 feedback 存储首次审阅闭环:99 条(19 单元)程序化 digest 后按复发度与证据强度分拣,覆盖检查剔除已吸收项,冻结 6 项候选全部落地(2 脚本缺陷修复 + 4 命令模板条款),sync-mirrors 一致、全量测试零回归;其余单次性/外仓项如实留待各单元下次运行。随后 mark-submitted 归零计数器。

## Optimization Points
- 本地存储审阅闭环(99 条)采用「程序化提取 Optimization Points 段 → 分单元复发度分拣 → 覆盖检查(防写入已吸收规则) → 冻结候选 → 最小化落地」流程,只读优化点不读全文 Review,99 条 digest 约 94KB 一次分拣完成;该流程可固化为 feedback-utils.py 的 digest 动作(按 unit 分组输出 points),避免每次手写提取脚本。
- 覆盖检查命中多处已吸收教训(regen-command-copies fail-fast、run-tests --names-out、可运行 runner 探测、writability 探测、资产迁移相形、左列隐藏轴),证明「先 grep 再写」纪律必要——否则会产生重复/冲突规则。
- 落地 6 项:create-new-plan.sh 存在性守卫+--force、gate-check.py 镜像副本 REPO_ROOT 修复(两副本均实测 exit 0)、implement.md 三条(批量替换验新形、失败归属、相位边界提交门)、clarify-taxonomy.md 两条(Feature 新建绑定义务、删除与重编号)、tasks.md 镜像对共享写任务裁剪、requirements.md 归档目录编号扫描。全量测试失败集与基线 diff 一致(零回归)。
- 单次性观察项(未达复发阈值或属外仓)未落地:plan Phase 0 验收标准可行性探测、tasks 格式校验器脚本化、analyze 机械路径存在性 Pass、create-team 多项(权重档位/断路器留痕/run-log schema)等,留待各单元下一次真实运行触发。
