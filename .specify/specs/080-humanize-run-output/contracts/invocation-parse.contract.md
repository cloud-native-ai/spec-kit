# Contract: 调用与解析（invocation-parse）

**Feature**: 062 扩展 | **规格**: `.specify/specs/079-humanize-run-output/requirements.md`
**性质**: 结构 + 行为契约。判定入口语法、模式路由、拒绝面与入口态 fail-closed。
**覆盖**: 见文末可追溯性表（唯一权威映射；本文件头部不复制枚举）。
**字面量**: `[[STR-NNN]]` 的拥有者是 requirements § Shared Strings；本文件只引用，不复制值。

---

## 语法与确定性

- **IP-01**: 选项集为 `[[STR-008]]`、`[[STR-009]]`、`--tone`、`--audience`、`--output`、`--force`，只出现在指令之前；`--` 终止选项解析，其后全部逐字进入指令；无 `--` 时第一个不可识别为选项的 token 即指令起点。解析 MUST 是纯语法过程：同样的 argv 得到同样的结果，MUST NOT 读取指令内容来猜测意图（FR-001, FR-006）。
- **IP-02**: 选项之后的剩余文本整体是**待执行指令**（逐字，含换行与引号）；本命令 MUST NOT 改写、摘要或规范化它（FR-001, FR-013）。裸文本 MUST NOT 再被解释为待改写内容（A4 的破坏性变更）。
- **IP-03**: `--tone` 的取值集与拒收语义、`--audience` 的自由文本语义（空字符串或纯空白 = **未提供**：不拒收、不改变表达层缺省）、`--force` 的覆盖语义 MUST 与既有契约逐字一致；`--output` 的写入语义按模式分属——内容模式沿用既有契约，运行模式由 FR-024 独占拥有（见 IP-16 / IP-17）。本契约不新增取值、不改缺省（FR-004, FR-024）。
- **IP-04**: 解析结果 MUST 落入 `data-model.md` § E2 的字段集，且 `mode` 只能是 `run` / `content` / `reject`；不存在第四种或「模糊」形态（FR-006）。

## 模式路由（封闭判定表）

- **IP-05**: 路由 MUST 按 `data-model.md` § E2 判定表逐行求值，顺序不可调换：①内容源 + 非空指令 → 拒绝；②内容源 + 空指令 → 内容模式；③无内容源 + 非空指令 → 运行模式；④两者皆无 → 拒绝（FR-001, FR-002, FR-003）。
- **IP-06**: 内容源与非空指令同现 MUST 拒绝并**点名两者**（源名与指令前缀），MUST NOT 走「内容优先」或「指令优先」的任何猜测分支；该拒绝优先于其他路由判断（FR-002, FR-006）。
- **IP-07**: 既无内容源也无非空指令 MUST 拒绝，输出内容三项齐全：用法行、支持的内容源（`[[STR-008]]` / `[[STR-009]]`）、迁移提示整句（FR-003, FR-005）。
- **IP-08**: 空内容源（空文件、纯空白内联）MUST 拒绝为 `empty-input`，MUST NOT 因「有一个内容源参数」而落进内容模式（FR-002）。

## 迁移提示与裸文本

- **IP-09**: 运行模式且调用中**无**任何显式内容源时（即裸文本调用），MUST 在报告前置元数据块输出迁移提示整句一次；内容模式与拒绝路径不输出该行（FR-005, A4）。该整句的字面量拥有者是 requirements A4（`已按指令执行；改写文本请用 --file/--inline`）；此处逐字复写一次，作为「测试钉扎字面量」这一合法重复形态，owner 变更时本条随之失败（FR-005）。
- **IP-10**: 迁移提示的落点是 `data-model.md` § E7 `migration_hint`，位于载体标记行之后、五个 H2 之前，且 MUST NOT 构成第六节；同一运行至多一行（FR-005, FR-018）。

## 入口态 fail-closed（并发、占用、嵌套）

- **IP-11**: 运行模式在派发前 MUST 取得仓库级占位（`data-model.md` § E4）。已有未过期占位时 MUST 拒绝为 `active-run`，并点名冲突 `run_id` 与起始时间；MUST NOT 排队等待或复用他人占位（FR-030）。
- **IP-12**: 给出 `--output` 时 MUST 同时取得目标级占位。目标已被另一未过期运行占用时 MUST 拒绝为 `output-occupied`，点名目标路径与冲突 `run_id`（FR-030）。
- **IP-13**: 指令文本含本命令的调用 token 时 MUST 拒绝为 `nested-invocation` 并点名命中的字面量。判定采用**封闭 token 集**（`speckit.humanize`，大小写不敏感）：宁可误拒提及该名称的指令，也不放过一次真实嵌套；误拒在拒绝消息里说明这是保守判定（FR-030）。
- **IP-14**: 任何拒绝路径 MUST NOT 产生派发、MUST NOT 留下占位、MUST NOT 写入任何文件；拒绝消息 MUST 含原因码对应的点名要素（`data-model.md` § E2 `reject_code` 表）（FR-003, FR-030）。
- **IP-15**: 内容模式 MUST NOT 取得占位（并发约束只作用于运行模式）；同一仓库的两次内容模式调用互不影响（FR-023, FR-030）。

## 输出目标形态

- **IP-16**: 运行模式 `--output` 的扩展名封闭集（`.md` / `.markdown` / `.txt`，此处为测试钉扎字面量）与写入内容由 requirements FR-024 独占拥有；本条款只断言该集合生效、集合外拒绝为 `bad-extension`，其余写入语义（原子写、`--force`、目标已存在且未给 `--force`、不可写即拒绝且不留部分文件）同样按 FR-024——运行模式没有输入格式可对齐，MUST NOT 复用内容模式的「扩展名跟随输入」规则（FR-004, FR-024）。
- **IP-17**: 内容模式的 `--output` 语义完全不变：扩展名与输入格式族一致，文件只含改写文本（FR-023, FR-024）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| IP-01 | FR-001, FR-006 | `test_ip01_parse_is_pure_syntax` |
| IP-02 | FR-001, FR-013 | `test_ip02_instruction_is_verbatim` |
| IP-03 | FR-004, FR-024 | `test_ip03_option_domain_unchanged` |
| IP-04 | FR-006 | `test_ip04_parse_fields_closed` |
| IP-05 | FR-001, FR-002, FR-003 | `test_ip05_routing_table_order` |
| IP-06 | FR-002, FR-006 | `test_ip06_source_and_instruction_rejected` |
| IP-07 | FR-003, FR-005 | `test_ip07_no_input_usage_and_hint` |
| IP-08 | FR-002 | `test_ip08_empty_source_rejected` |
| IP-09 | FR-005 | `test_ip09_migration_hint_once` |
| IP-10 | FR-005, FR-018 | `test_ip10_hint_placement` |
| IP-11 | FR-030 | `test_ip11_active_run_rejected` |
| IP-12 | FR-030 | `test_ip12_output_occupied_rejected` |
| IP-13 | FR-030 | `test_ip13_nested_invocation_rejected` |
| IP-14 | FR-003, FR-030 | `test_ip14_reject_paths_write_nothing` |
| IP-15 | FR-023, FR-030 | `test_ip15_content_mode_unreserved` |
| IP-16 | FR-004, FR-024 | `test_ip16_run_output_extension` |
| IP-17 | FR-023, FR-024 | `test_ip17_content_output_unchanged` |
