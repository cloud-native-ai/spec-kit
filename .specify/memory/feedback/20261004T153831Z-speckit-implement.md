---
id: "20261004T153831Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "053-implement-20261004T153824Z"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature_id: "053"
disposition: "processed"
partial: false
created: "2026-10-04T15:38:31Z"
summary: "本轮 `/speckit.implement` 在 Feature 053(机器可判定的制品命题)上跑完 49 项任务 / 8 个 Phase,十项 Completion Gate 对当前树逐项重跑全绿,状态 `Planned → Implemented`(翻转提交 `cc9ce52c`)。命令达成其声明目的,且**本特性通过了它自己造出来的工具**(DoD-7 自举):它自己的 182 条契约条"
introspection_ref: "introspection-20261006T140432Z#F-07"
disposition_reason: "introspection:introspection-20261006T140432Z#F-07"
---

## Review
本轮 `/speckit.implement` 在 Feature 053(机器可判定的制品命题)上跑完 49 项任务 / 8 个 Phase,十项 Completion Gate 对当前树逐项重跑全绿,状态 `Planned → Implemented`(翻转提交 `cc9ce52c`)。命令达成其声明目的,且**本特性通过了它自己造出来的工具**(DoD-7 自举):它自己的 182 条契约条款恒在覆盖基线之外(基线面排除本特性 spec 目录),只能被认领不能被豁免,而 182 条全部被钉住它们的七行认领;`validate-tasks.py` 对这份 tasks.md exit 0 且零 `green-*` 发现。自举查出了七项被证伪的继承前提中的**四项**——包括「本特性自己的定义行撞坏本特性自己的门」那一条。

四项执行期摩擦,均非本命令独有但都在本轮真实发生:

**① 一份制品的字段名与它自己的定义互相矛盾,而链路上无任何东西检查这一点。** `data-model.md` 的 E-4 把 `test_paths` 定义成"全部写入目标",而 FR-018(b)、契约 C-16 与该检查项的起源散文都说**测试路径**。按定义的字面实现,在 T045 落下 182 条认领的那一刻就对本特性自己的 tasks.md 产出 3 条假 `green-path-divergence`(三行共同追加同一份证据日志)。**名字是对的、定义是错的**,而归因需要一次完整的失败归因流程(被测物 / 断言 / 与已澄清需求矛盾 / 外部来源)才落到"制品自身的定义过宽"这一档——它不在既有四轴里,勉强归到"断言与已澄清需求矛盾",但矛盾的双方都是上游制品。

**② `LC_ALL=C` 是承重条件,却不在"名字级比对"这条房式判据的任何拥有者文档里。** glibc 的 `en_US.UTF-8` 排序规则忽略 `#`、`/`、`.`,于是覆盖核算的 `comm -13` 给出 delta **665** 而不是 **182**,同时打印 `file 1 is not in sorted order`——一行极易被读成噪声的警告,实际上就是答案错了的原因。名字级比对已是词汇表条目,但排序区域设置不是它的一部分;本轮把它写进 GATE-8 与契约 C-19,教训本身却只落在本特性里。

**③ 写门的裁定可观测性是散文规则,而我在写入量最大的那个 Phase 上漏了它。** 模板 step 6 已明写"Make the verdict observable"、step 7 已明写"没有记录裁定的 Phase 视为未闭合",而 Phase 3 的 `gate-check.py` 仍在编辑**之后**才跑。回溯裁定为 6/6 `allow`、EXIT=0,故没有写入任何门本会拦下的东西,但顺序错了,已披露并单独成提交(`26bd2feb`)。规则在场而仍被漏掉,说明它缺少机械形态:目前没有任何东西会因为一份进度报告没有引用门的退出码而变红。

**④ Token 效率:每个 Phase 边界跑一次 3232 项全量套件是本轮的主要开销,而其中五个 Phase 的改动不可能影响到另外约 3100 项。** 名字级判据只需要"变更切片 + 收尾时一次全量"即可满足;本轮按房式惯例逐 Phase 全量,是纪律而非必要。记为消耗观察,不是缺陷。

一处**上送而非就地修**的既有缺陷值得单列,因为它与本命令的 step 6 直接相关:`goal-utils.py` 的共享父解析器**并不**使 `--json`/`--repo-root` 位置无关——argparse 让子解析器的默认值静默覆盖顶层值,故 `--json list` 输出人读形(A-9)。源码注释与 Tool 记录里各有一行假陈述,均已订正、C-11 的被证伪前提已内联注解、两个方向都钉住;修法会改变全部十个 action 的旗标优先级,超出 FR-022…FR-048 的声明范围。

## Optimization Points
- **`templates/commands/implement.md` step 6 的"写门裁定可观测"需要机械形态**(而非散文提醒):把"该 Phase 首份进度报告 MUST 引用 `gate-check.py` 的退出码与受检路径数"写成一条可判定的闭合条件,并在 step 7 的闭合判定里增一行——报告里没有该引用的 Phase 视为未闭合。理由:该规则本轮已在场而仍被漏掉(Phase 3),说明"记得做"不是可靠形态;step 7 已有"无裁定记录即未闭合"的语义,缺的只是让它可被第三人复核的判据。
- **`LC_ALL=C` MUST 写进"名字级基线"判据的拥有者处**(词汇表条目 `名字级基线 (Name-Level Baseline)` 指向的 `run-tests.sh --names-out` + `comm -13` 形态),并注明 glibc 的 UTF-8 排序忽略 `#`/`/`/`.`、其外部症状是 `file N is not in sorted order` 这一行警告而非一个错误退出码。理由:本轮同一判据在两个 locale 下给出 182 与 665 两个答案,而错的那一路只印一行警告;覆盖核算、回归比对、镜像集合比对三处都依赖它,只在本特性的 GATE-8 里修等于留下三个未修的调用点。
- **`/speckit.analyze` 增一项候选检查:实体字段名与其定义的辖域是否一致。** 形态:字段名含收窄性名词(`test_`、`contract_`、`goal_`、`spec_`)而其定义量词覆盖更宽的集合("every write target"、"all paths")即报。理由:E-4 的 `test_paths` 定义为"全部写入目标"直接产出 3 条假发现,而这类矛盾在 requirements/plan/data-model/tasks 四份制品之间无任何既有检测覆盖——它不是术语漂移(§4.F 查的是同一个词在多处含义不同),而是**同一个字段的名字与定义各说一套**。
- **`data-model.md` / 契约撰写纪律:两轮不同来源的 FR 治理同一个面时,后者 MUST 声明它是收窄还是继承前者。** 本轮 FR-020(围栏代码块)与 FR-009(提及规则,含行内代码跨度)分别写于 clarify 与 implement 两轮,前者读起来像后者的完整陈述而实际只覆盖其一半,于是"定义一个标记的那一行"被自己的检查器判为对该标记的悬空认领——本特性自己的 tasks.md 撞坏本特性自己的 GATE-7。落点建议:`templates/plan-template.md` 的 data-model 指引或 `shared/definitions/contract-clause-definitions.md` 的条款撰写节。
- **逐 Phase 全量套件跑不是名字级判据的必要条件**(token-efficiency 消耗观察):判据可由"变更切片 + 收尾一次全量"满足。建议在 `templates/commands/implement.md` step 8 的 Commit gate 一句里显式允许按切片跑,同时保留"收尾 MUST 一次全量、且以名字级 `comm -13` 双向为空为准"的硬条件,以免切片跑被当成全量跑的替代。
