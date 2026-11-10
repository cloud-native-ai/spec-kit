# Analyze Findings — W3（tasks.md）

- **Unit**: W3 · **Round**: 1（无先前 W3 报告）· **flow_class**: execution
- **Read domain**: 仅 `.specify/specs/097-speckit-migrate-command/tasks.md`；宪法 `.specify/constitution.md` 作为阶段权威用于 D 通道比对。requirements.md / plan.md / contracts/ / checklists/ / 特性注册表不在本单元读域（由 W1/W2 或阶段合成覆盖）。
- **Method**: analyze-artifacts 检测通道 A–F 静态执行；G/H/I 超出读域未执行（不代表通过）。严格只读，未做任何修复。
- **Severity**: 按分析契约的传播面规则赋值；CRITICAL/HIGH 行仍需阶段级独立验证波确认后方可进入阶段报告，MEDIUM/LOW 免验证。
- **机械前提**: 任务行 48 条（T001…T048，无重号、无缺号，`^- \[ \] T[0-9]{3} ` 计数 48）；`[green:]` 声明 11 条，与 DoD-2 的"15 条可判条款中已声明 11"一致。

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W3-01 | CRITICAL | § Task State Sigil（tasks.md L77）× 宪法 VII Workflow Gates（constitution L224） | 本文件把 `[~]` 延迟原因的唯一载体定为 `verification.md` 的 `deferred_tasks=`，而宪法 VII 的不可协商工作流门要求延迟行携带行内 `<!-- deferred: reason -->`，按本文件执行将缺失宪法规定的标记。 | /speckit.tasks（若该 sigil 出自 create-tasks 模板，属机制侧冲突，需模板与宪法字面统一，不得在本特性内稀释） |
| W3-02 | CRITICAL | GATE-4（L51）/ DoD-7（L39）/ T048（L264）× 宪法 VII Pre-Status-Flip Gate（constitution L223） | 成功标准状态行的载体被定为 `verification.md`，而宪法该门要求写入 `verification.log`，两名字不同且本文件未声明等价或迁移，按本文件闭环无法满足宪法字面。 | /speckit.tasks 与验收加固/宪法字面统一（以显式宪法修订或门定义修订收敛，不在本特性内改判） |
| W3-03 | HIGH | § Definition of Done DoD-1（L33） | DoD-1 的检查命令对全文件做 FR 去重计数，追溯表（L334–L358）与 DoD-1 自身行内 `FR-001…FR-025` 文本已足以让计数恒为 25，因此被检查条件（每条 FR 至少在一条任务行中被点名）即使全部行内引用被删除也不会转红，属"绿色检查是主张不是证据"。 | /speckit.tasks（改为按任务行匹配，或补一条"删除某行 FR 引用应转红"的变异检查） |
| W3-04 | MEDIUM | § FR/SC → row traceability（L330–L358）× 行内引用 T005（L146）/T034（L238）/T038（L245）/T039（L246） | 追溯表与行内引用在 7 处不一致：表列而该行未点名 4 处（FR-002→T039、FR-021→T034、FR-022→T034、FR-025→T039），行点名而未入表 2 处（T034→FR-025、T039→SC-009），仅推断未点名 1 处（FR-007→T005）。 | /speckit.tasks |
| W3-05 | MEDIUM | § FR/SC → row traceability SC-007 行（L340）× T015（L171） | SC-007 在全文件任何任务行文本中都不出现，其唯一归属是追溯表把 T015 指为覆盖行，而 T015 的断言清单与引用清单均不含 SC-007，且 DoD-1 只约束 FR 侧、SC 侧没有命名级检查。 | /speckit.tasks（在 T015 文本点名 SC-007，或改映射到真实断言行） |
| W3-06 | MEDIUM | 前置清单（L7）× DoD-9（L41）× T045（L261） | 前置清单声明 quickstart.md 含 scenarios 0–5，而 DoD-9 与 T045 只执行场景 1–5，场景 0 没有任何执行行或取证行，也未声明豁免。 | /speckit.tasks |
| W3-07 | MEDIUM | T026（L201）/ T027（L202）× T023（L195）× § Environment Prerequisites（L62） | T026 的 `platform-no-symlink` 拒绝分支与 T027 的 `site/`、`.specify/memory/**`、项目扩展保护类，均未出现在唯一 US2 测试行 T023 的有界断言清单中，而环境节声称该平台降级"在此由模拟行使"却未指名模拟载体。 | /speckit.tasks（把两类行为写入 T023 或新增测试行，并指名模拟方式） |
| W3-08 | MEDIUM | § FR/SC → row traceability FR-004（L337）/ FR-005（L338）/ FR-011（L344）/ FR-012（L345） | 这四条 FR 只映射到实现/文档/镜像行（依次为 T016；T010/T011/T018；T019/T020；T041/T042），没有任何测试行点名它们，Tests Mode ON 下其红先测试归属不可见。 | /speckit.tasks（补测试行映射，或在测试行断言中点名 FR） |
| W3-09 | MEDIUM | § Definition of Done DoD-3（L35）× T013（L154） | DoD-3 声称源码守卫"在任一复制实现被移除时转红"，与其"no second engine"标题及 T013 所述守卫（禁止第二份实现）方向相反，且其 Check 只运行套件，无法验证该变异主张。 | /speckit.tasks（更正红条件方向，或补一条变异红测） |
| W3-10 | MEDIUM | Tests 契约（L11）× Package Map 写域（L105–L115） | Tests 契约要求每条红先读数逐条落入 `notes/red-first-evidence.md`，但 pkg02–pkg06 的写域均未包含该文件，而 pkg05 与 pkg06 声明可重叠，两个执行者会同时写同一路径，违反"记录类数据一文一件"的并发写安全要求。 | /speckit.tasks（按条目分文件，或把重叠面串行化并补写域声明） |
| W3-11 | LOW | T004（L134）× § Premises（L98）× Notes（L376） | T004 要求对"本特性首次全树统计"执行 `--freeze`，但 § Premises 已记录同一命令在生成期（2026-11-10，640 names）执行过、Notes 亦称该冻结是本生成阶段制品，实现入口重跑同一冻结未说明目的。 | /speckit.tasks |
| W3-12 | LOW | T041（L257）/ T043（L259） | 两行的 "its mirror pair see `.specify/...` is synced in T042/T044" 句子不合语法，读者无法判定它是声明一条同步动作还是指向一个文件。 | /speckit.tasks（改写为"镜像副本由 T042/T044 同步"） |
| W3-13 | LOW | § Green Partition（L362–L371）× Notes（L376） | 四个未声明条款（cli C-6/C-7、engine C-5/C-8）被描述为"由点名它们的测试行文本钉住"，但 Green Partition 表未列出任何钉住行，该主张在文件内不可审计。 | /speckit.tasks |
| W3-14 | LOW | Notes（L376） | "The contractor's live delta" 使用了契约覆盖计数之外的生造主体（计数所有者为 clause-coverage accountant），读者会误认存在另一个计量主体。 | /speckit.tasks |

## 系统观察（仅聚合，不单独提级）

- **DoD 检查判别力**（W3-03、W3-09）：多条 DoD 的 Check 与其声称条件不同构；另有"行数 48""记录非空"等子句未给出可执行测量命令。
- **覆盖证据双轨**（W3-04、W3-05、W3-08）：FR/SC 覆盖同时由"追溯表"和"行文本引用"承载且互相漂移，未指定哪一轨为判据。
- **单文件证据**（W3-10）：并行包共享同一证据账本，写域声明未覆盖共享路径。

## 边界说明

- H（checklist 问责）、I（decision tension，判读对象为 plan.md）、G（特性注册表/索引）不在本单元读域，未执行；其结论由 W1/W2 或阶段合成给出。
- tasks.md § Notes 的"accountant FR-citation lane reads 4/25"是文件内继承披露，其对象在 contracts/（超出本单元读域），建议合成阶段单列为 contracts 侧发现。
- 本单元无修复动作；tasks.md 未改动。
