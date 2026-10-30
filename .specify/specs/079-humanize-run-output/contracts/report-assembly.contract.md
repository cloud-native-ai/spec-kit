# Contract: 上下文装配与报告（report-assembly）

**Feature**: 062 扩展 | **规格**: `.specify/specs/079-humanize-run-output/requirements.md`
**性质**: 结构 + 内容契约。判定五节报告的形态、来源清单、语言与保真。
**覆盖**: 见文末可追溯性表。
**字面量**: 五个小节标题与两个载体标记的拥有者是 requirements § Shared Strings（`[[STR-001]]`…`[[STR-007]]`）；本文件只引用。
**保真底线**: 受保护集合的枚举拥有者是 requirements FR-017（承 062 FR-007）；本文件只声明它在此生效。

---

## 报告结构

- **RP-01**: 报告 MUST 恰含五个 H2 小节，顺序固定：`[[STR-001]]` → `[[STR-002]]` → `[[STR-003]]` → `[[STR-004]]` → `[[STR-005]]`；标题逐字，不加编号、不翻译、不合并。缺任一小节即不合格（FR-018）。
- **RP-02**: 五个 H2 之前 MUST 只有一条载体标记行（`[[STR-006]]` 或 `[[STR-007]]`，二选一）；裸文本调用时其后再加一条迁移提示行（仅会话面：写入 `--output` 文件时 MUST NOT 含该行，见 RP-19）。该元数据块 MUST NOT 用标题、MUST NOT 构成第六节、MUST NOT 混入其他内容（FR-005, FR-011, FR-018, FR-024）。
- **RP-03**: 报告由 humanize 主会话撰写；执行体 MUST NOT 写最终报告。撰写者与执行者是两个角色，报告里 MUST NOT 出现「我执行了」式以执行体身份的自述（A6, FR-009）。
- **RP-04**: 报告 MUST 只在会话内呈现，或在显式 `--output` 时写入该路径；MUST NOT 写隐式副本、MUST NOT 写到默认位置（A9, FR-024）。

## 逐节义务

- **RP-05**: `[[STR-001]]` MUST 先于一切细节给出可直接行动的总判断：首行是 `[[STR-012]] <token>` 的机器可判定行，token 取 requirements FR-019 的封闭集（FR-019 是 verdict 集合与 status→verdict 映射的唯一 owner，本文件与 `data-model.md` 只引用）；token 恒为英文原样，其后正文 MUST 用报告语言写出对应措辞；`not-an-action` 按 FR-019 的同一映射取 `success` 并以「未执行任何动作」表述，MUST NOT 称为执行成功；MUST NOT 在失败时使用成功措辞（FR-019, SC-003）。
- **RP-06**: `[[STR-002]]` MUST 按影响降序列出关键变化或结果；无变化时 MUST 明写「无变化」而不是留空；指令造成的写入 MUST 在此可见（FR-019, FR-024）。
- **RP-07**: `[[STR-003]]` MUST 为每条关键结论给出可定位指针（产物路径、命令与退出码、测试读数、可定位引用），MUST NOT 只写形容词；指令造成的写入 MUST 逐项列出；无可报告输出时 MUST 写 `[[STR-010]]`（FR-020, SC-002, SC-009）。
- **RP-08**: `[[STR-003]]` MUST 含一行派发记录元数据：键名是 `[[STR-011]]`（字面量 owner = requirements § Shared Strings），值只计 humanize 发起的顶层派发（原生 `1` / 降级 `0`）；计数口径的唯一 owner 是 EX-21（FR-007）。
- **RP-09**: `[[STR-004]]` MUST 列出风险、限制、未验证项与缺失上下文；无已知风险时 MUST 用报告语言显式写出该判断（英文 `no known risks`），该节不得省略或留空（FR-021, SC-009）。
- **RP-10**: `[[STR-004]]` MUST 含来源清单，只列**实际读取**的来源；读取失败或未读取的来源 MUST 作为缺失项同节声明；MUST NOT 列出来源却未使用。来源状态（`read` / `not-read` / `unavailable`）的语义与判定 owner 是 FR-014，本条款只断言清单与缺失声明的形态（FR-014, FR-015, SC-002）。
- **RP-11**: `[[STR-005]]` MUST 给出可执行的下一步，或显式写「无下一步」；MUST NOT 用泛泛建议充数（FR-022）。

## 语言

- **RP-12**: 正文语言 MUST 按 requirements A7 的封闭域（`zh` / `en`）与固定顺位判定：① 指令主语言 → ② 项目治理（instructions / glossary）主语言 → ③ 回退 `en`；每一次回退 MUST 在 `[[STR-004]]` 声明；第三书写系统在 ①② 均不可判时按 ③ 处理，其原文逐字引用、不翻译（FR-018, A7）。
- **RP-13**: 五个小节标题 MUST 始终为英文原样，与正文语言无关；载体标记行与派发记录行的键名同为英文原样（FR-018, A7）。
- **RP-14**: 语言适配 MUST NOT 改变事实层：术语、专有名词、代码标识符、路径与命令保持原样（FR-017, FR-018）。

## 保真与诚实

- **RP-15**: 保真底线（requirements FR-017 的受保护集合）MUST 在报告全文生效；上下文补全 MUST 只使用动作结果与会话已蕴含的信息（FR-016, FR-017）。
- **RP-16**: 报告 MUST NOT 编造未发生的工作、未读取的来源、未出现的读数或不存在的路径；核对不上的证据按 EX-14 记为「未能核实」（FR-015, FR-020）。
- **RP-17**: 表达层 MUST 应用四维度自然化中适用的部分（去套话、补过渡、格式可读、语言一致），并服从 `--tone` / `--audience`；MUST NOT 承诺或暗示任何 AI 内容检测器结果（FR-022；062 检测器诚实条款继续生效）。
- **RP-18**: 报告面 MUST 遵守面向读者可理解性的既有 owner（术语白名单/黑名单、上下文上下界）；内部引擎调用形式 MUST NOT 出现在给读者的正文里（宪法 XV；owner `shared/guidelines/user-facing-comprehension.md`）。

## 输出目标

- **RP-19**: 运行模式给 `--output` 时 MUST 写入与 `target` 内容一致的完整五节报告，并含五个 H2 之前的载体标记行、`[[STR-012]]` 行与 `[[STR-011]]` 行，MUST NOT 写入迁移提示行；会话 MUST 回显一份摘要，摘要 MUST NOT 替代报告、MUST NOT 成为报告的第六节（FR-024，clarify 裁决）。
- **RP-20**: 写入 MUST 是原子写（临时文件 + 重命名）；目标已存在且未给 `--force` → 拒绝覆盖、目标逐字节不变；不可写 → 拒绝且不留部分文件（FR-024）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| RP-01 | FR-018 | `test_rp01_five_sections_in_order` |
| RP-02 | FR-005, FR-011, FR-018, FR-024 | `test_rp02_metadata_block` |
| RP-03 | FR-009 | `test_rp03_main_session_writes_report` |
| RP-04 | FR-024 | `test_rp04_zero_write_default` |
| RP-05 | FR-019, SC-003 | `test_rp05_conclusion_verdict` |
| RP-06 | FR-019, FR-024 | `test_rp06_key_changes_by_impact` |
| RP-07 | FR-020, SC-002, SC-009 | `test_rp07_evidence_pointers` |
| RP-08 | FR-007 | `test_rp08_dispatch_record_line` |
| RP-09 | FR-021, SC-009 | `test_rp09_no_known_risks_explicit` |
| RP-10 | FR-014, FR-015, SC-002 | `test_rp10_sources_read_list` |
| RP-11 | FR-022 | `test_rp11_next_steps_or_none` |
| RP-12 | FR-018 | `test_rp12_language_priority` |
| RP-13 | FR-018 | `test_rp13_headings_stay_english` |
| RP-14 | FR-017, FR-018 | `test_rp14_language_keeps_identifiers` |
| RP-15 | FR-016, FR-017 | `test_rp15_fidelity_floor` |
| RP-16 | FR-015, FR-020 | `test_rp16_no_fabrication` |
| RP-17 | FR-022 | `test_rp17_expression_and_detector_honesty` |
| RP-18 | FR-022 | `test_rp18_reader_comprehension` |
| RP-19 | FR-024 | `test_rp19_output_full_report_and_summary` |
| RP-20 | FR-024 | `test_rp20_atomic_write_and_force` |
