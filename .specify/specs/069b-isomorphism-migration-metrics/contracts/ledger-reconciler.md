# Contract: 台账对账、委托核验与六面绑定（Ledger Reconciliation, Delegation & Face Bindings）

**Feature**: 069b（父 069） | **File scope**: `scripts/python/flow-class-check.py`、`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md` | **FR served**: FR-009、FR-010、FR-011、FR-012、FR-013；SC-003、SC-004、SC-005

- **C-1** 反空真下限：解析出的行数低于下限即失败

`--action check` MUST 在解析出的台账行数低于**解析侧反空真下限**时产出 finding `ledger-truncated`，
MUST NOT 让「解析出 0 行」以零 finding 结束。该下限 MUST 由清单侧常量推导：
`LEDGER_FLOOR = ⌊(FLOOR_COMMANDS + FLOOR_SKILLS) / 2⌋`（27 + 51 → **39**；2026-10-25 按 `flow-class-check.py`
输出的 `inventory.floors` 实测），MUST NOT 取自被检查的台账自身（即 MUST NOT 用「当前解析出的行数」当分母），
MUST NOT 引入第三份手写单元计数。
下限是**解析侧**的下限：它与 069a 既有 `inventory-truncated`（清单侧下限）同时存在，任一单独满足都不够。
它是**材料性 / 反空真**阈值，不是完整性判据——完整性由 C-2 的 `matched == inventory_units ∧ gaps == 0` 承担。
因此删掉一行台账（78 → 77 行）MUST 仍判 `gap`（SC-003 注入 A），只有表被解析成不足一半（含 0 行）才是 `parse-failure`；
把下限设成期望行数 78 会让「删一行」同时触发 `ledger-truncated`，两红不可区分，且会破 069a 的 77 行夹具（见 C-4）。

（FR-010；SC-003）

- **C-2** 覆盖率断言：零缺口必须可与「一行都没解析出来」区分

`--action check` 的 JSON MUST 含 `coverage` 块：
`{"ledger_rows": <int>, "inventory_units": <int>, "matched": <int>, "gaps": <int>, "parse_errors": <int>, "floor": <int>}`。
`clean` 判定 MUST 同时满足 `matched == inventory_units`、`gaps == 0`、`parse_errors == 0`、`ledger_rows >= floor`。
`gaps` MUST 等于 `missing` + `unknown` finding 数；`parse_errors` MUST 等于 `row-malformed` + `ledger-truncated` finding 数
（`parse_errors` 只计**台账解析侧**；`inventory-truncated` 属清单侧，按 C-3 落 `parse-failure` 桶但不计入本计数）。
文本输出 MUST 在空集旁边同时打印 `matched` 与 `inventory_units` 两个数（反空真伴生量），MUST NOT 只打印「0 findings」。

（FR-010；SC-003）

- **C-3** 两种红可区分：`red_kind` 与退出码

`--action check` 的 JSON MUST 含 `red_kind`，取值与优先级（高→低）：
`owner-unavailable` > `framework-source-required` > `parse-failure` > `gap` > `clean`。
判定规则：
- `owner-unavailable`：owner 文档缺失或不可解析（退出码 2，不产出 findings）；
- `framework-source-required`：仓库形态为载荷根（见 C-14，退出码 2，不产出 findings）；
- `parse-failure`：存在 **`gap` 桶之外**的任何 finding（当前 = `row-malformed` / `ledger-truncated` /
  `inventory-truncated`；退出码 1）；
- `gap`：存在 finding 且**全部**落在这个封闭集合内——`missing` / `unknown` / `duplicate` / `dual-class` /
  `invalid-class` / `neutral-unlisted` / `mixed-oracle-class` / `ledger-version-missing`（退出码 1）；
- `clean`：零 finding（退出码 0）。
两个桶 MUST 构成对 `check` 全部 kind 的**穷尽划分**（`gap` 集合之外一律 `parse-failure`），因此
`red_kind = clean` ⟺ `findings == []` MUST 恒成立——`inventory-truncated` 单独出现时也 MUST 落 `parse-failure`，
MUST NOT 落到 `clean`。新增 kind 时 MUST 同时落进其中一个桶，MUST NOT 留空档。
「缺口」与「解析失败」两种红 MUST 在 `red_kind` 上不同；仅靠 finding 数量相同不算可区分。
SC-003 的两次注入 MUST 分别落到 `gap` 与 `parse-failure`（或 `owner-unavailable`），且两值不同。

（FR-010；SC-003）

- **C-4** finding kind 的封闭扩展与 069a 兼容

本切片新增 finding kind 恰好五个：`ledger-truncated`、`ledger-version-missing`、`mixed-oracle-class`、
`delegation-mismatch`、`delegation-unknown-skill`（`delegation-hand-list` 与 `faces-*` / `isomorphism` 的 kind
只出现在各自动作里，不计入 `check` 的 kind 集）。
069a 的 8 个 kind（`missing` / `unknown` / `duplicate` / `dual-class` / `invalid-class` / `row-malformed` /
`neutral-unlisted` / `inventory-truncated`）的语义、触发条件与退出码 MUST 保持不变；
`--action lookup` 的输出字段、降级标签与退出码 MUST 保持不变（含 `owner-unavailable` 与默认标记的互斥）。
在 78 行完整台账的树上，`check` MUST 继续返回 `units = 78` 与零 finding。
C-1 的解析侧下限 MUST 定在 77 行以下，使 069a 的 77 行夹具（`test_missing_ledger_row_reports_missing`、
`test_inventory_truncated_below_*` 的 `commands=26` / `skills=50` 两种）MUST NOT 新增 `ledger-truncated`
——它们的 `kinds ⊆ EIGHT_KINDS` 断言是本切片 MUST NOT 改写的既有断言（唯一例外见 tasks A-1）。

（FR-010；SC-003）

- **C-5** 台账「生效版本」的承载形态声明一次

所有者文档 MUST 在 § 逐流程台账 内声明**一次** `**台账版本**: <整数>（<YYYY-MM-DD>）`，
并写明生效版本由该文档版本与既有 `## 变更记录` 共同承载、行级不设版本列。
声明缺失 → `ledger-version-missing`；出现多于一次 → 复用 `row-malformed`（不新增 kind，计入 `parse_errors`）。
版本不兼容的判据 MUST 继续是「表头 / 列集合与解析器期望不符」（069a C-4 / C-5），本契约 MUST NOT 引入
`version` 字段、行级版本列或第三个版本信号。

（FR-009、FR-010）

- **C-6** 列头与解析口径沿用，不重开

台账列头 MUST 逐字含机器键 `flow_class`（[[STR-003]]），解析 MUST 按表头名而非列位置——
这两条沿用 069a `contracts/flow-class-ledger.md` C-4 与 C-5，本契约只做**引用**，不复制其正文。
本切片新增的检查 MUST NOT 要求新的必选列（例如不得为版本检查新增列）。

（FR-009、FR-010）

- **C-7** 混合 oracle 的台账一致性

台账中 `basis = mixed-oracle` 的行，其 `flow_class` MUST 为 `execution`（[[STR-001]]）并叠加表达类门禁；
不一致 → `mixed-oracle-class`，判为台账缺陷并修台账，MUST NOT 逐案裁定、MUST NOT 取 `expression`（[[STR-002]]）后省略执行侧门禁。
该判定 MUST 只依据主交付物的消费方与失败可见性，MUST NOT 依据交付物数量比例或文件类型占比。
台账行 `notes` 保留的父指针不构成第二判据来源。

（FR-011；SC-004）

- **C-8** 委托关系的解析语法

`--action delegation` MUST 从命令模板文本解析委托边，语法为
`(?:\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md` → `skill:<name>`；同一模板内重复出现的同名技能 MUST 去重。
捕获出的 `<name>` MUST 满足台账单元 id 语法 `skill:[a-z0-9][a-z0-9-]*`：占位 / 模板形态（如
`skills/<name>/SKILL.md`——2026-10-25 实测出现在 `templates/commands/skills.md`）MUST NOT 构成委托边，也 MUST NOT 因此产出 finding。
每条边 MUST 产出 `{command, skill, command_class, skill_class, verdict, source_line}`，`verdict` 的裁决顺序 MUST 固定为：
技能不在台账 → `unknown-skill`；技能在所有者 § 类中立清单 → `neutral-exempt`（**不论两侧类别是否相同**——清单成员一律按豁免记录，
2026-10-25 实测 6 条边命中，其中仅 `docs → memory-record` 两侧类别不同）；否则类别相同 → `same-class`、不同 → `mismatch`。
JSON 顶层 MUST 含 `commands_scanned`（被扫描模板数）。
`mismatch` → finding `delegation-mismatch`；台账中不存在的技能 → `delegation-unknown-skill`。
模板未声明任何技能路径时不构成委托边，MUST NOT 产出 finding。

（FR-012）

- **C-9** 委托核验不得依赖人工清单

委托关系 MUST 只由图中的命令模板与技能目录解析，MUST NOT 读取任何手工维护的「命令 → 技能」映射表；
仓库内出现此类清单（≥3 行命令 id 与技能 id 的对应表，且不属于命令模板自身）→ `delegation-hand-list`。
扫描范围 MUST 封闭为 `shared/`、`templates/commands/`、`skills/` 与本 spec 的 formal artifacts。
类中立豁免 MUST 取自所有者 § 类中立清单（069a C-8 的封闭清单），MUST NOT 在本契约或引擎里复制一份清单副本。

（FR-012）

- **C-10** 类中立清单的封闭性沿用

类中立清单 MUST 保持封闭，成员判据 MUST 是「交付物被两类流程共同消费且无类特定验收」；类中立 MUST NOT 免除任何门禁，
也 MUST NOT 改变该单元自身的类别键。本切片 MUST NOT 新增、删除或改判清单成员——清单内容归所有者（069a 已落）。

（FR-012）

- **C-11** 六面绑定完整性

`--action faces` MUST 解析 `shared/workflow/expression-gates.md` § 六面 表：恰好 6 个数据行、face id 唯一、
每行**一个** `owner_pointer` 格。一个格内 MAY 用 `+` 连接多个路径，仍计为**一个绑定**（主机制 + 执行件）。
每个路径 MUST 在仓库内可解析（源码根或 `.specify/` 镜像）；格内带 `§ <anchor>` 时，该文件 MUST 存在标题文本包含该锚的
`#` 标题行。违规分别记 `faces-count`（行数 ≠ 6）、`faces-duplicate`（face id 重复）、
`faces-pointer-missing`（空格）、`faces-unresolvable`（路径或锚不可解析）。JSON 顶层 MUST 含 `faces`（解析出的面数）。

（FR-013；SC-005）

- **C-12** 第二绑定表禁止

六面之外的文件 MUST NOT 出现把 ≥3 个 face id 与 owner 路径成对列出的表（Markdown 表格或 YAML 形态）。
扫描范围 MUST 封闭为 `shared/`（S3 比较集除外）、`templates/commands/`、`skills/` 与本 spec 的 formal artifacts。
命中 → `faces-second-table`。S3 比较集的 9 条 owner 路径不在扫描范围内；命令模板与技能 MUST NOT 复制面表。

（FR-013；SC-005）

- **C-13** 判据正文副本计数：复用既有 duplicate 面，主体面封闭为四棵树

SC-005 的「判据正文在 owner 之外出现 0 次」MUST 由既有
`scripts/python/doc-consistency-check.py --faces duplicate` 测量，比较侧 MUST 收窄为分类 owner 单文件
（`--owner-path shared/definitions/flow-class-definitions.md`；该选项同时把 owners 从主体集中排除，
并把测量语义定为「这些 owner 的文本是否被复制」，主体↔主体副本不属本测量）。
主体集 MUST 封闭为 `shared/`、`templates/commands/`、`skills/`、`docs/` 四棵树（`--path` 传目录，递归 `*.md`）
加上本 spec 的 formal artifacts。要求 `findings = 0`。

命令模板、技能与文档树 MUST 在扫描面内——这正是 069a F12「owner↔owner 盲区」的下一步：
窄到「分类 owner + spec artifacts」的主体集会让模板/技能/文档里的副本不可见，MUST NOT 再用。
`shared/workflow/expression-gates.md` 不再充当比较侧（它是另一个 fact 的 owner），但作为主体仍受本测量约束。
该口径 MUST NOT 被读成全仓 grep 等价物（`.specify/` 镜像、`notes/` dated 记录与构建产物不在主体面内）。
副本注入的转红证明落在 `tests/contract/test_expression_faces.py`
（`templates/commands`、`skills`、`docs` 三面各一条）。

（FR-013；SC-005）

- **C-14** 作用域：框架源仓专有动作与载荷根的具名状态

`check` / `delegation` / `faces` / `isomorphism` MUST 只在框架源仓运行：仓库存在 `templates/commands/` 目录，
或存在可解析的 `skills/{external,internal}/*/SKILL.md`。
两者皆不满足（客户 payload 根，包括 `--repo <project>` 与 `--repo <project>/.specify` 两种传法）时，
MUST 以退出码 2 + `error.label = framework-source-required` 结束，MUST NOT 产出 findings、MUST NOT 退出 0、MUST NOT 报 `inventory-truncated`。
若 owner 同时缺失，按 C-3 的优先级报 `owner-unavailable`（两者都是具名的非绿状态，MUST NOT 退出 0）。
`--action lookup` MUST 继续支持双帽子解析（源码根与载荷根），其行为不受本条影响。

（FR-010、FR-013）

- **C-15** 只读与确定性

四个动作 MUST 只读：MUST NOT 写文件、MUST NOT 建缓存、MUST NOT 调网络、MUST NOT 读环境变量决定判定。
同一输入重复运行 MUST 产出相同的 findings 集合（`checked_at` 是唯一允许变化的时间字段）。
所有路径 MUST 由 `--repo` 或脚本自身位置解析，MUST NOT 依赖调用方 cwd。

（FR-010、FR-012、FR-013）

- **C-16** 测试面

四项检查各自 MUST 有正反两侧的机械证据：完整树 → 零 finding；注入一处缺陷 → 该 kind 出现且退出码正确。
委托核验的证伪夹具 MUST 把一个技能改成反类（转红）并把一个类中立边设为 `neutral-exempt`（仍绿）。
faces 检查 MUST 包含「删一行」「复制一行」「把指针指向不存在路径」三种注入。
所有新测试 MUST 在实现前先红（引擎无该动作时以「动作缺失」为红，MUST NOT 以 import/collection error 为红）。

（FR-010、FR-012、FR-013；SC-003、SC-005）
