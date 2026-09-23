---
id: "20260923T123804Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "feedback-consume-20260923T120035Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-09-23T12:38:04Z"
summary: "本轮 /speckit.feedback 以显式 `consume` 参数进入,按 Routing flow 判为 Path A(就地消化),非 package、非探针注入。帽子取证:根级五个源目录实测存在且 `src/specify_cli` 仅在根级 ⇒ 框架项目,故 32 条条目**全部**归 Path A、零条归 Path B。入站目录 `feedback/feedback-*.zip` "
---

## Review
本轮 /speckit.feedback 以显式 `consume` 参数进入,按 Routing flow 判为 Path A(就地消化),非 package、非探针注入。帽子取证:根级五个源目录实测存在且 `src/specify_cli` 仅在根级 ⇒ 框架项目,故 32 条条目**全部**归 Path A、零条归 Path B。入站目录 `feedback/feedback-*.zip` 实测零包,A1/A2 无对象,故无 re-delivered / second-copy / orphan 标记可命名,consume-log 交叉核对无可匹配项。清单实跑:32 条全部 `kind: internal`、slice = commands 23 + skills 9、`external_count: 0`、`introspection_ref` 命中 0、`partial` 1 条、阈值 32/10。A3 自省按 Token 效率纪律执行:154 KiB 条目**从未整体注入**,改为 5 个并行只读核验器按亲和度分组(每组 4–9 条、≤43 KiB),各自读全条目并对**框架源**取证(未以 `.specify/` 镜像为权威)。**Feature 052 的子代理注入首次实跑生效**:5 次派发均逐字携带 `shared/guidelines/fast-fail.md` 的 owner 子句并要求显式异常行,回报 3 条 `ANOMALY` + 2 条 `未发现异常`,静默为零;3 条异常全部被子代理判为**裁定**并停在本层上交,无一条就地修平——正是该纪律设计要拦的形态,可作 SC-007/SC-009 的首批真实样本。核验结果聚为 21 个问题,恰好一次覆盖 32 条(31 成员 + 1 排除),分流 13 direct-fix / 6 improve-skills / 2 speckit-requirements。报告落盘并经 4 次引擎 exit-2 迭代后 `introspect-register` exit 0、linked 31;用户确认后 `--confirm` 置 confirmed 并 dispose 31 条 processed,排除条目另按 A6 dispose 为 ignored(引擎拒 `--ref ...#Excluded`,出处降级进 `--reason`)。用户四项裁定:确认全部 / **删除**索引脚本 / **补探针**把 team 判为复杂 / 本轮只修 F-01 + 文档漂移。已执行并逐项取证:F-01 删除 `update-feature-index.sh` 双副本(第三次独立发现该陷阱,Feature 051 的 followup_2 早已建议「要么修要么删」,本轮关闭)+ 三处 live 引用同步;F-02①② 把 `feature-integration.md` 的失效路径与状态机矛盾纠真并明写索引手工维护、`agent-definitions.md` 的失实计数改为按目录派生(实测 2);F-02 裁定项落地 team 重分类——实测三判据全中且其中 4 个脚本**早于本轮改动**,故重分类基于既有事实;probe 83→84、per-tool 副本再生 `--check` OK、probe-map 重建、分类契约表按其自身 § Maintenance 同步、5 个测试文件的枚举与计数随之移动。失败归因:改后首跑新增 5 条红全在**断言侧**(team 的 simple 参数化)+ 1 条跨模块计数复制,修断言并引用用户裁定;其中 `test_docs_command_template.py:168-169` 的两条计数复制**删除而非改数**(owner 是 `test_classification_counts`)。变异演练:植入 `## Feedbak` → 新守卫变红 → 精确反向替换复原 → `diff -q` 与备份 BYTE-IDENTICAL。回归:名字级 `comm -13` 对冻结基线**为空**(69→68,唯一差异是一条套件顺序依赖的既有失败本轮转绿,单独跑该文件 16/16)。三次提交按逻辑分组(b8562122 / 7d571f39 / 6c0a7b1d),每次提交前跑删除面审计,B 组的 2 条删除逐项对账到用户的删脚本裁定。零网络行为。

## Optimization Points
- `--action probes --reconcile` 是清单步骤里唯一**会以 exit 2 报「registry invalid」却不说明后果**的一项。本轮它回报 6 条违规(3 个技能有 embed 无 probe 对象、2 个已删技能的对象仍在、1 个技能有对象无 embed),而命令文本没有说这是否阻断 Path A 消化。实测不阻断——32 条条目的 kind/slice 在记录时就已解析完毕,注册表漂移只影响**此后**的新记录——但这个判断只能由执行者自行做出,属命令未规定的裁定。建议:在清单步的 `--reconcile` 行后加一句判据(红 reconcile 是**可报告的发现**而非 Path A 的阻断条件,归注册表 owner `.specify/shared/definitions/probe-definitions.md` 与 `/speckit.instructions`),使下一轮不必重新推导。
- A3 的报告 schema 只能靠**读一份旧报告**或**连撞引擎 exit 2**才能得知,而命令明文写「本文不复制引擎内部规则,写报告前不必先读引擎源码」——两者相加等于把 schema 变成只有引擎知道的秘密。本轮为此付了 4 次往返:C-7 两次(自造 `**上送件性质**` 与 `**异常处置**` 字段行、以及 `**已修部分**`,均须折进 `优化方案`)、C-8 一次(Excluded 行给条目 id 加了粗体)、以及一次**未被任何错误码命名**的形态陷阱——`## Excluded` 之后的一切都被当作 Excluded 行解析,故我把反空转哨兵写成 `## 覆盖核对` 小节时,引擎报的是「malformed Excluded row: '## 覆盖核对(反空转哨兵)'」,而不是「未知小节」。建议命令侧给出 schema 的**闭集**字段名清单 + 一句「`## Excluded` 必须是最后一个小节,其后不得再有任何 `## `」,或在 `.specify/templates/` 放一份报告骨架;否则每轮都要重付这笔学费。
- `--action dispose --ref` 只接受 `introspection-<ts>#F-<nn>`,拒绝 `#Excluded`,于是 A6 明写的「被排除条目也要处置」无法带上指向自己报告小节的出处。本轮只能把出处降级塞进 `--reason` 散文里(理由串变成 `clean-run-no-points (introspection-...Z Excluded)`),使机器可读的关联丢失。建议 `--ref` 接受 `#Excluded` 作为合法锚点形态,与 A6 的义务对齐。
