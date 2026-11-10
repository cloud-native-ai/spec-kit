# Analyze Findings — Round 2 — W3（tasks.md）

- **Unit**: W3 · **Round**: 2（C/H 修复轮后的重过门；本切片执行全严重度检测 + round-1 残差复核）· **flow_class**: execution · **Date**: 2026-11-10
- **Read domain**: 仅 `.specify/specs/097-speckit-migrate-command/tasks.md`；宪法 `.specify/constitution.md` 作为阶段权威用于 D 通道；分析契约及其引用的 owner 判据（closed-set-claims / one-source-of-truth）用于定级。requirements.md / plan.md / contracts/ / data-model.md / checklists/ / 特性注册表不在本单元读域（由 W1/W2 或阶段合成覆盖）。round-1 W3 报告与修复处置记录作为自家工作记录用于 delta 复核。
- **Method**: analyze-artifacts 检测通道 A–F 静态执行；G（特性注册表）、H（checklist 问责）、I（plan decision tension）超出读域，未执行（不代表通过）。严格只读，未做任何修复。
- **Severity**: 按传播面规则赋值；承载 DoD/验证门的不可测断言按 closed-set-claims § 处置判 HIGH。CRITICAL/HIGH 行仍需阶段级独立验证波确认后方可进入阶段报告；MEDIUM/LOW 免验证。
- **Mechanical premises（本轮实测）**: 任务行 `^- \[[ xX>~]\] T[0-9]{3} ` 计数 **48**（T001…T048 无重号、无缺号）；DoD-1 的 Check 命令（仅任务行 FR 去重）输出 **25**；任务行内 `[green:]` 声明 **11** 条；任务行内 SC token 无 SC-007，`grep -n SC-007` 仅命中追溯表 L340；任务行 FR 多重度：仅 FR-004、FR-008 各由 1 行点名，其余 23 条 FR 各由 ≥2 行点名。

## A. Round-1 findings 重裁

| ID | Round-1 严重度 | 状态 | 重裁事实与证据 |
|----|----------------|------|----------------|
| W3-01 | CRITICAL | **fixed** | L77 sigil 已改为行内 `<!-- deferred: reason -->` 承载原因，`deferred_tasks=` 降为不替代行内标记的汇总索引；宪法 VII（L224）字面满足。 |
| W3-02 | CRITICAL | **fixed** | DoD-7 L39 / GATE-4 L51 / T048 L264 载体均已是 `verification.log`；但 Package Map pkg07 写域 L113 仍写 `verification.md`，传播残差另立 **W3-16**。 |
| W3-03 | HIGH | **fixed** | L33 Check 已改为先过滤任务行再取 FR token，实测返回 25；但修复句新增的变异判据机械不成立，残差另立 **W3-15**。 |
| W3-09 | MEDIUM | **open（升格 HIGH）** | DoD-3 L35 的 "源码守卫在任一复制实现被移除时转红" 仍与 no-second-engine 方向相反，且其 Check 只运行套件、无法验证该变异主张；该断言承载 DoD-3，按 closed-set-claims § 处置（DoD/验证门承载的不可测断言 → HIGH）升格。 |

## B. Round-1 未处置残差（open MEDIUM/LOW，status=open，disposition=deferred）

> 修复轮仅处置 C/H；以下逐条在修复后的文件上复现，disposition 为 `deferred`（本重过门不修复，留待后续 remediation；不静默丢弃）。

| ID | 严重度 | 状态 | 复现事实（当前文件） |
|----|--------|------|----------------------|
| W3-04 | MEDIUM | open / deferred | 追溯表与行内引用漂移仍在：表列而该行未点名 4 处（FR-002→T039、FR-021→T034、FR-022→T034、FR-025→T039），行点名而未入表 2 处（T034→FR-025、T039→SC-009），仅推断 1 处（FR-007→T005）；本轮另见 SC-009→T038 表列而 T038 文本只点名 FR-021。 |
| W3-05 | MEDIUM | open / deferred | SC-007 在任务行文本中 0 次出现，唯一归属为追溯表 L340 指向 T015；Phase Map 的 US1 criteria（L23）只列 SC-001/SC-003；`tasks-validator.txt` 的 "distinct SC cited: 9" 由表行贡献，不是行级覆盖证据。 |
| W3-06 | MEDIUM | open / deferred | 前置清单 L7 声明 quickstart.md 含 scenarios 0–5，DoD-9（L41）与 T045（L261）只执行场景 1–5；场景 0 无执行行、无取证行，也无豁免声明。 |
| W3-07 | MEDIUM | open / deferred | T026（L201）的 `platform-no-symlink` 拒绝分支与 T027（L202）的 `site/`、`.specify/memory/**`、项目扩展保护，仍未进入唯一 US2 测试行 T023（L195）的有界断言清单；环境节 L62 称该平台降级"由模拟行使"却未指名模拟载体。 |
| W3-08 | MEDIUM | open / deferred | FR-004 / FR-005 / FR-011 / FR-012 仍只映射到实现、文档、镜像行（依次 T016；T010/T011/T018；T019/T020；T041/T042），无任何测试行点名；Tests Mode ON 下红先测试归属不可见。 |
| W3-10 | MEDIUM | open / deferred | Tests 契约（L11）仍要求 red-first 读数集中写入 `notes/red-first-evidence.md`，但 pkg02–pkg06 写域（L105–L115）均未声明该路径；pkg05 与 pkg06 声明可重叠，两个执行者会并发写同一账本，违反"记录类数据一文一件"。 |
| W3-11 | LOW | open / deferred | T004（L134）仍在实现入口对同一 spec 再次 `--freeze`，而 § Premises（L98）已记录生成期冻结（640 names），重跑目的未说明。 |
| W3-12 | LOW | open / deferred | T041（L257）/ T043（L259）的 "its mirror pair see `.specify/...` is synced in T042/T044" 句法仍不成立；T033（L237）存在同型句 "see `tests/contract/test_qoder_command_frontmatter.py`"。 |
| W3-13 | LOW | open / deferred | 四个未声明条款（cli C-6/C-7、engine C-5/C-8）与 template T-1…T-6 被描述为"由点名它们的测试行文本钉住"，但 Green Partition（L360–L371）仍未列出任何钉住行，主张在文件内不可审计。 |
| W3-14 | LOW | open / deferred | Notes（L376）仍使用 "The contractor's live delta" 这一计量主体之外的生造主体（计数所有者为 clause-coverage accountant）。 |

## C. Round-2 新发现

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|----|----------|------|------------|----------|
| W3-15 | **HIGH** | DoD-1（L33） | 修复后新增的可转红判据"删除任一任务行的 FR 引用必须使该计数小于 25"机械不成立：25 个 FR 中 23 个由 ≥2 条任务行点名，实删 T014 行的 FR-001 后计数仍为 25（`sed '170s/FR-001//' … \| wc -l` → 25），只有删掉单点 FR-004/FR-008（T016/T015）才降到 24；声称的"任一"红条件无法按字面满足。 | /speckit.tasks（改为"删除某 FR 的全部行内引用后该 FR 必须消失"的变异，或按每条 FR 的引用行清单执行删除；保留实测读数） |
| W3-16 | **HIGH** | Package Map pkg07 写域（L113）× T048（L264）/ DoD-7（L39）/ GATE-4（L51） | W3-02 的载体修复未传播完：pkg07 写域仍列 `verification.md`，而 T048 实际写、DoD-7/GATE-4 实际查的是 `verification.log`；pkg07 执行者按声明写域无权写真正的闭包载体，同一事实在文件内出现两个名字（冲突声明）。 | /speckit.tasks |
| W3-17 | MEDIUM | T023（L195）× DoD-4（L36） | T023 的第四个变异 "weaken the assertion to existence-only" 是测试侧弱化，弱化断言不会让套件转红，与 "four mutations turn the file red" 矛盾；DoD-4 又要求 T028 记录"四个变异结果"。 | /speckit.tasks（改为实现侧变异——如归档内容失真、仅复制不搬移——并保留四条红读数） |
| W3-18 | MEDIUM | T048（L264）× 修复处置记录的 `.gitignore` 残差 | T048 选定的宪法 VII 载体 `verification.log` 被仓库 `.gitignore` 的 `*.log` 规则忽略（修复处置记录已记该残差），而 T048 行文本未要求负规则、强制纳入或等价受控载体，闭包记录可能在版本库中消失。 | /speckit.tasks（把"载体须受版本控制"写进行文本，与 W3-16 一并收敛） |
| W3-19 | MEDIUM | T035（L242）× T033（L237）/ T034（L238）/ T039（L246） | T035 要求模板 "verbatim restatement" 四类结局与退出码，但三条钉住行都不断言模板内的表：T033 只断言两个字面量与禁用词，T034 比较运行期行为，T039 断言装配形态，模板内的结局表可无守卫漂移（One Source of Truth 的漂移副本风险）。 | /speckit.tasks（在 T033/T039 增一条"模板结局表与 owner 逐字一致"的断言，或让模板改为引用 `specify migrate --help`） |

## D. 待独立验证的 C/H 清单（3 条）

- W3-09（升格 HIGH，DoD-3 变异方向 + 无验证）
- W3-15（HIGH，DoD-1 变异判据机械不成立）
- W3-16（HIGH，pkg07 写域载体名与 T048/GATE-4 冲突）

## E. 系统观察（仅聚合，不单独提级）

- **修复传播不闭合**（W3-02→W3-16；W3-03→W3-15）：C/H 修复只改了三处字面锚点，同一事实的第四处副本（Package Map）与新增的可转红判据未同步校验，回修本身成为新的漂移源。
- **DoD 检查判别力**（W3-15、W3-09、W3-17）：DoD-1/DoD-3/DoD-4/DoD-10 仍有"声称会转红但机制上不会"的子句；"行数 48""记录非空"等子句仍无逐条测量命令。
- **覆盖证据双轨**（W3-04、W3-05、W3-08）：FR/SC 覆盖同时由追溯表与行文本承载且继续漂移；SC-007 行级覆盖为 0。
- **单文件账本**（W3-10）：并行包共享红先证据账本，写域声明不覆盖共享路径。

## F. 边界说明

- G（特性注册表/索引）、H（checklist 问责）、I（plan decision tension，判读对象为 plan.md）不在本单元读域，未执行；其结论由 W1/W2 或阶段合成给出。
- tasks.md Notes 的 "accountant FR-citation lane reads 4/25""4 own clauses beyond the frozen baseline" 是文件内继承披露，其对象在 contracts/ 与 accountant 读数（超出本单元读域），建议合成阶段单列为 contracts 侧发现。
- 本单元无修复动作；tasks.md 未改动。既有证据文件未触碰。
