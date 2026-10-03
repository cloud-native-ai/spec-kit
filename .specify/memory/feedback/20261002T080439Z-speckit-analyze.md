---
id: "20261002T080439Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "053-analyze-20261002T080427Z"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "053-machine-decidable-artifacts"
partial: false
created: "2026-10-02T08:04:39Z"
summary: "本轮按 §4 同作者委托把检测拆成三个互不重叠的界面(spec↔plan↔research / plan↔contracts↔data-model↔tasks / 特性登记与宪法对齐),交 3 个 fresh-context 只读子代理执行,共回传 52 行发现;再由 16 个与检测者互不相交的校验子代理逐条复测全部 CRITICAL/HIGH。检出 1 项宪法 MUST 违规(Feature 0"
---

## Review
本轮按 §4 同作者委托把检测拆成三个互不重叠的界面(spec↔plan↔research / plan↔contracts↔data-model↔tasks / 特性登记与宪法对齐),交 3 个 fresh-context 只读子代理执行,共回传 52 行发现;再由 16 个与检测者互不相交的校验子代理逐条复测全部 CRITICAL/HIGH。检出 1 项宪法 MUST 违规(Feature 052 的 Planned→Implemented 翻转证据未记入特性详情文件,而其正文仍在声明状态未翻转)与 6 项 HIGH,其中 4 项落在 053 自己的完成门闸上:GATE-7 与 T045 的 requirements.md#FR-NNN 认领目标与 green-dangling 条款直接冲突(不可满足)、GATE-8/T046/DoD-7 的自举核算因基线冻结早于认领落地而永不变红(不可证伪)、GATE-9 的阈值与它自己印的分解式相互矛盾、quickstart 场景 3 的循环漏跑 b2.md 使 SC-001 的 4/4 证据实际只有 3/4。命令本身运作良好:只读约束全程守住(无一次写盘)、无文件产物、门闸预算与镜像状态未受影响;主要成本在派发规模——16 次校验派发中 9 次结论为降档,暴露 §4 只要求委托检测、未要求检测者逐行证明自己查过继承关系。

## Optimization Points
- §4 的 same-author 委托只规定"必须委托检测",未要求检测者在每行证明它查过继承关系;本轮 16 行送校验、9 行被降档(56%),九条降级理由全是同一个未做的事实:「这条错误前提被哪个下游工件消费」——门 rule 3 的 2026-09-18 基线(12 送 10 降)在本仓复现,说明缺的是判据形式而非判据内容:每行 MUST 附"消费方 + 引用该行的那个位置",给不出就不得升过 MEDIUM。
- §5.5 把校验波定位成"检测之上更便宜的一层过滤",但本轮校验者交付了检测没有的新事实(全树 mirror DIFF 实测 33 而非记录的 3、b2.md 在 quickstart 循环里被漏、同一错误前提实际散在 5 个界面而非 3 个):该步的真实定位是独立复测,建议把定位词从"过滤"改为"复测",并把"允许校验者上送新事实"写进回传契约。
- DO-NOT-FLAG 清单缺「被任务行命名的落点证据文件在本轮尚不存在」这一类:`notes/pre-change-measurements.md` 由 T001/T002 创建,校验者却把它当异常上送;该豁免条件已由 tasks 模板的 runtime-evidence landing points 规则定义,analyze 的噪声清单应同样点名,否则每轮都要花一次校验去确认"文件还没建是正常的"。
