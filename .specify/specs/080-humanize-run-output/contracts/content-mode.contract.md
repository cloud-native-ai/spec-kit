# Contract: 旧内容模式（content-mode）

**Feature**: 062 扩展 | **规格**: `.specify/specs/080-humanize-run-output/requirements.md`
**性质**: 不回归契约。判定 `[[STR-008]]` / `[[STR-009]]` 路径在重构后仍与既有行为等价。
**覆盖**: 见文末可追溯性表。
**所有者边界**: 内容模式的行为细则（输入核验、主语言判定、窗口分段、四维度改写、文件写入细则）由
`.specify/specs/062-humanize-command/contracts/rewrite-behavior.md` 与 `tone-input-file.md` 拥有；
本文件不复述它们的条款，只固定「重构后这些条款仍然生效」与两模式共存的边界。

---

## 等价性

- **CM-01**: `[[STR-008]]` 与 `[[STR-009]]` 路径 MUST 保持既有输入核验、扩展名与空输入拒收、输出格式跟随输入、主语言判定、分段与四维度改写的全部既有条款；本特性 MUST NOT 降低其保真或改写质量（FR-023）。
- **CM-02**: 内容模式的 `--output` 语义 MUST 保持不变：文件只含改写文本本身，报告类输出回会话；覆盖与原子写规则沿用既有条款（FR-024）。
- **CM-03**: 内容模式的输出 MUST NOT 含五个报告小节、MUST NOT 含载体标记行、MUST NOT 含迁移提示（FR-023, FR-024）。
- **CM-04**: 内容模式 MUST NOT 派发任何执行体、MUST NOT 取得并发占位、MUST NOT 读取动作结果（无动作可读）（FR-023, FR-024）。

## 共存边界

- **CM-05**: 模式路由的唯一所有者是 IP-05；本文件不重述判定表。内容源与非空指令同现的拒绝由 IP-06 拥有（FR-002）。
- **CM-06**: 注入防护 MUST 在两种模式下同时生效，并覆盖全部不可信文本：`[[STR-008]]` / `[[STR-009]]` 输入、运行模式的指令原文、执行体回传的 `final_output` / `evidence` / `products`、以及指令产出的文件内容（范围 owner = requirements FR-025）。这些文本 MUST 按数据处理：其中的指令式文本 MUST NOT 改变 humanize 自身的保真、拒收、零外传与零写入规则，MUST NOT 被当作 humanize 的操作指令执行；运行模式下它只改变被执行的动作，不改变报告契约（FR-025）。
- **CM-07**: 保真底线 MUST 在两种模式下同时生效，受保护集合的枚举 owner 是 requirements FR-017；本文件不复制集合（FR-017）。
- **CM-08**: 检测器诚实条款（不承诺、不暗示、不优化任何 AI 内容检测器结果）MUST 在两种模式的文本与输出中继续成立（062 C-10 继续有效；FR-023）。

## 迁移可发现性

- **CM-09**: 命令模板与 docs MUST 写出一条可复制的迁移示例：同一段文本用 `[[STR-009]]`（或 `[[STR-008]]` 指向文件）调用即可获得改写，而裸文本会被当作指令执行（FR-005, FR-023）。
- **CM-10**: 内容模式 MUST NOT 输出任何暗示「这是新能力」的措辞；它是保留的既有入口，语气上 MUST NOT 被降级为「兼容垫片」（FR-023）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| CM-01 | FR-023 | `test_cm01_content_mode_equivalence`（复用 062 既有断言集） |
| CM-02 | FR-024 | `test_cm02_content_output_text_only` |
| CM-03 | FR-023, FR-024 | `test_cm03_no_report_scaffold_in_content_mode` |
| CM-04 | FR-023, FR-024 | `test_cm04_content_mode_no_dispatch` |
| CM-05 | FR-002 | `test_cm05_routing_owned_by_ip05` |
| CM-06 | FR-025 | `test_cm06_injection_defense_both_modes` |
| CM-07 | FR-017 | `test_cm07_fidelity_both_modes` |
| CM-08 | FR-023 | `test_cm08_detector_honesty_both_modes` |
| CM-09 | FR-005, FR-023 | `test_cm09_migration_example_present` |
| CM-10 | FR-023 | `test_cm10_content_mode_wording_intact` |
