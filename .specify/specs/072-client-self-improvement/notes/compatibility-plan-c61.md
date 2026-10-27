# C-61 Compatibility Plan — Feature 072 guard-suite interactions (T026, 2026-10-27)

> 触发: T026 守护网定向运行发现两条 071/069 时代的守护断言与 Feature 072 的
> 计划授权编辑面正面冲突，产生两条相对 T002 基线的新失败名。本文档是 C-61 要求的
> 书面兼容计划;同类变更不得以本文档为先例(C-61: 本条款永不被引用为第二次例外的基础)。

## 背景判据

C-61: 不得删除/弱化/语义漂移任何既有契约断言;具名守护套件保持全绿且断言只增。
实现若认定某变更无法避免, 必须带书面兼容计划、理由, 并在特性详情声明不为例外先例。

裁决: **纠正级**。冲突双方都是已记录意图——072 计划(plan_commit 6dca65a5)的
C-56 编辑面明确列出受影响的四个非布线源文件与反馈引擎;守护断言的失败是两条冻结
面在新计划下的机械冲突, 不存在两种以上读法, 改动局部可逆。

## 变更一: `test_dogfooding_practice.py::FEEDBACK_ENGINE_ACTIONS`

- **冲突**: 该冻结闭集(063/068 两次同批修订过)未含 `client-metrics`;072 按
  C-62 在反馈引擎新增唯一只读动作 `client-metrics` 后, `test_c4_engine_action_set_unchanged` 失败。
- **理由**: C-62 明文授权该动作("exactly two faces … one read-only `client-metrics`
  action on the feedback engine"), 且 C-47 要求它接线进 `_ACTIONS` 与
  `args-manifest`。撤销动作 = 违抗已批准计划, 不可选。
- **变更形态**: 闭集按同批修订先例(args-manifest / ingest-exec-quant 两次)增一
  个成员并留日期化注释; 注释同时声明对任何**其它**未申报动作仍红。断言形态
  (集合相等、双向)不变 —— 只增不改。
- **钉住**: `tests/contract/test_client_metrics.py` C-40…C-50 与
  `test_client_guard_sweep.py::test_c55_engine_faces_grow_by_exactly_the_two_authorized`
  保证不会有第三个动作越过此门。

## 变更二: `test_expression_compatibility.py::ALLOWED_POST_BASELINE_CHANGES`(C-5 冻结哈希)

- **冲突**: C-5 的非布线冻结哈希清单要求 069a 切片之外的字节不变;072 的 C-56
  编辑面授权四个非布线源文件新增客户段落, 哈希漂移使
  `test_c5_non_wiring_files_keep_their_frozen_hashes` 失败。
- **理由**: 四个文件(templates/commands/feedback.md、improve.md,
  skills/internal/manage-feedback/SKILL.md、self-improvement/SKILL.md)全部在
  C-56 枚举的编辑面内; 每个漂移段都有 072 契约套件钉住内容形态(见各条目的
  pinned-by 与 markers)。071 当年对同清单的两处修订(templates/commands/review.md、
  code-review SKILL.md)是本机制的既有先例。
- **变更形态**: 只使用该测试自带的 ALLOWED_POST_BASELINE_CHANGES 机制 —— 每条
  记录漂移理由 + 内容标记(markers 逐文件独立断言, 一个文件的标记不能为另一个
  文件担保); 哈希冻结本身不刷新(漂移仍被记录, 只是具名), 未具名漂移照旧全红。
  断言只增不改。
- **钉住**: markers 由各 072 契约套件(cited per entry)与
  `test_client_guard_sweep.py::test_c56_*` 双重约束。

## 不为例外先例声明

上述两个变更均为"计划授权编辑面 × 前序特性冻结面"的一次性机械冲突解决, 依据是
072 已批准计划的 C-56/C-62 与 C-61 自带的逃逸条款。后续特性不得引用本文档作为
修改守护断言的依据; 再发生冲突须各自走 C-61 书面计划并在特性详情声明。
