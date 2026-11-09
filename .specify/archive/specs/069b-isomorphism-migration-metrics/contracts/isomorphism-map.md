# Contract: 同构映射与不可同构边界（Isomorphism Map & Non-Isomorphism Boundaries）

**Feature**: 069b（父 069） | **File scope**: `shared/definitions/flow-class-definitions.md` | **FR served**: FR-001、FR-002、FR-003、FR-004、FR-005；SC-001

- **C-1** 载体唯一

同构映射与不可同构边界 MUST 只存在于分类所有者 `shared/definitions/flow-class-definitions.md`，落为两个二级章节：
`## 同构映射（8 阶段 × 3 面）` 与 `## 不可同构边界`。该文档开篇的 owns 列表 MUST 同时列出这两项。
仓库内 MUST NOT 出现第二份映射表（表格、YAML、JSON 或代码常量形式），MUST NOT 出现第二个声称拥有映射的文档。
本契约本身只定义形态与判据，MUST NOT 成为映射的发布副本。
该文档开篇同时声明它拥有映射与边界（与本切片的归属收敛合为一次编辑）。

（FR-001、FR-003、FR-009）

- **C-2** 表形与行集

映射表 MUST 是 Markdown 表，表头逐字为
`| 阶段 | 结构（实体 / 关系 / 边界） | 流程（阶段与门禁角色） | 逻辑（证据 / 契约 / 验收 / 版本 / 所有权） | 强制门禁 | 强制门禁引用 | 强制状态 |`，
恰好 8 个数据行、零空行。`强制门禁` 写 face id；`强制门禁引用` 写 `gate:<算子 id>`，算子 id 取自门禁 owner
§ 阶段算子表的 `算子 id` 列（该列是全表唯一的稳定标识，2026-10-25 review-fix 为把强制声明做成可证伪而新增）。行首格（阶段名）集合 MUST 等于阶段名册 owner 的阶段集合：从
`skills/external/sdd-loop-driver/scripts/loop-state.py` 的 `STAGE_ARTIFACTS` 字典顶层键解析（离线、确定性），
期望集合为 `requirements` / `clarify` / `plan` / `tasks` / `checklist` / `analyze` / `implement` / `review`。
名册不可解析时检查 MUST 以 `roster-unavailable` 退出码 2 结束，MUST NOT 用一张内置列表冒充名册。
映射 MUST NOT 声明自己的阶段版本或复制名册内容。

（FR-001）

- **C-3** 24 格的格语法

三个面列（第 2–4 列）的每一格 MUST 形如 `代码型：<产物或判定面> ↔ 文档型：<产物或判定面>`：
含且仅含一个 `↔`；两侧各以 `代码型：` / `文档型：` 起头，且各 ≥ 8 个字符。
任一格缺失、无 `↔`、多于一个 `↔` 或任一侧过短 → `cell-malformed`。
面的含义（结构 = 实体 / 关系 / 边界；流程 = 阶段与门禁角色；逻辑 = 证据 / 契约 / 验收 / 版本 / 所有权）
MUST 在表前用一段 legend 声明一次，MUST NOT 在 24 个格里重复。

（FR-001）

- **C-4** 强制状态的封闭取值

`强制状态` 格 MUST 取 `已强制` 或 `已声明未强制` 之一，其他取值 → `status-invalid`。
`已强制` 行的 `强制门禁` 格 MUST 写出 ≥1 个 face id，face id MUST 存在于门禁 owner
`shared/workflow/expression-gates.md` § 六面 的封闭六面表；出现未知 face id → `gate-unknown`。
同行的 `强制门禁引用` 格 MUST 写出 ≥1 个 `gate:<算子 id>` 引用；无引用 → `gate-ref-missing`，
非 `gate:` 前缀 → `gate-ref-malformed`，`<算子 id>` 不在 § 阶段算子表 → `gate-ref-unknown`。
`已声明未强制` 行的 `强制门禁` 与 `强制门禁引用` 两格 MUST 为空（或各仅一个 `—`），出现任一 → `status-invalid`。

（FR-002）

- **C-5** `已强制` 必须为真

一行标 `已强制` 时，其 `强制门禁` 格点名的每个 `(阶段, face)` 对 MUST 在门禁 owner § 阶段算子表中
存在一行 `阻断级别 = blocking` 的算子行，**且** `强制门禁引用` 中 MUST 有一个引用解析到该
`(阶段, face)` 的那一行。任一被点名的 face 在该阶段只有 advisory 算子、或没有算子行
→ `annotation-false-enforced`；引用解析到别的 stage / 未被本行点名的 face → `gate-ref-mismatch`；
引用解析到 advisory 算子 → `gate-ref-not-blocking`；被点名的 face 没有覆盖它的引用 → `gate-ref-missing`。
检查 MUST NOT 接受「该 face 在别的阶段有 blocking 算子」作为替代，也 MUST NOT 接受「该阶段有任一 blocking 算子」作为行的替代。
可证伪粒度是**引用级**：引用可解析、指向 blocking、且与 `(阶段, face)` 一致即为通过；24 格自由文本是否真的在描述那个门禁
归评审面（C-10），检查器 MUST NOT 声称能判定语义真实性。

（FR-002）

- **C-6** `已声明未强制` 必须为真

一行标 `已声明未强制` 时，该阶段 MUST 在门禁 owner § 阶段算子表中**没有任何** `blocking` 算子行
（advisory 行不算强制）。存在任一 blocking 算子行 → `annotation-false-unenforced`。
`已声明未强制` 只是「此刻未被任何门禁执行」的如实标注：它 MUST NOT 被读作通过、MUST NOT 构成
新增未强制行的许可、MUST NOT 免除任何既有门禁。

（FR-002）

- **C-7** 口号行即缺陷

既无可解析 face id 又无 `已声明未强制` 标注的行 MUST 判为缺陷（`slogan-row`）。
行级强制状态是缺陷判定的单位：同一行内「部分 face 被强制、部分没有」MUST 由该行点名的 face 集合整体承载，
MUST NOT 用「至少有一个 face 被强制」来给未强制的面背书。

（FR-002、FR-005）

- **C-8** 不可同构边界：四条封闭行

`## 不可同构边界` MUST 是一张 4 行表，表头逐字为
`| 边界 | 不可互换的判定面 | 为什么不能互换 | 门禁处理 |`，`边界` 列取 `a` / `b` / `c` / `d` 各恰好一次：
(a) 验收 oracle（执行行为 vs 阅读理解）；(b) 验证算子（测试 vs 构建 / 链接 / 一致性检查）；
(c) 失败可见性（运行期偏差 vs 构建通过而事实陈旧的静默失败）；(d) 语义 oracle 缺失（文档无编译器）。
缺行 / 重复 → `boundary-missing`；`为什么不能互换` 为空 → `boundary-malformed`。

（FR-003）

- **C-9** 边界必须绑到门禁

每条边界的 `门禁处理` 格 MUST 含 ≥1 个封闭 face id（同 C-4 的六面表），且 MUST 说明该面如何处理这条边界
（例如「评审面按读者基准判定」）。无 face id → `boundary-unbound`；只写 face id 而无处理说明 → `boundary-malformed`。
边界与映射 MUST 同属 C-1 的同一文档；把它们拆成两份各自漂移 → `boundary-split`。

（FR-003）

- **C-10** 同构主张必须落地

任何「同构」主张 MUST 落到映射表的一行（阶段 + 面）或边界表的一条；无法落地的表述 MUST NOT 进入需求、门禁或模板文本。
机械下限：(i) 映射表每格必须写出两侧产物（C-3）；(ii) 模板与技能 MUST NOT 出现以「文档即代码」为理由的许可句
（正则命中 `文档即代码` / `docs? (?:is|are) code` 且同段无 owner 指针）；(iii) 其余语义判断归评审面（`review`），
由 `shared/workflow/expression-gates.md` § 评审 的读者基准判定。检查器 MUST NOT 声称能判定自由文本的可判定性。

（FR-005）

- **C-11** 禁止整套移植代码型门禁

映射与边界文档 MUST NOT 把代码型门禁的判定算子整套移植到文档型流程。机械下限：门禁 owner § 阶段算子表的
「执行算子」列 MUST NOT 出现代码型算子闭集 `pytest` / `--cov` / `coverage` / `go test` / `mvn test` /
`npm test` / `jest` 中任一词（大小写不敏感）；出现即 `code-operator-in-expression-gates`。
跨类复用 MUST 指名所复用的**不变量**（契约、证据、所有权、版本），MUST NOT 复用其判定算子本身。

（FR-004）

- **C-12** 判据不是介质轴

映射格与边界行 MUST NOT 以文件扩展名、自然语言种类、是否含代码块或是否由脚本生成作为分类理由。
机械下限：两张表内 MUST NOT 出现 `按扩展名` / `by extension` / `\.md 即` / `\.yaml 即` 等介质判据短语
（闭集，大小写不敏感）；出现即 `medium-axis-in-map`。同内容换介质改判 MUST 由评审面判为判据缺陷。

（FR-003、FR-005）

- **C-13** 检查器行为与作用域

映射检查 MUST 由 `scripts/python/flow-class-check.py --action isomorphism` 执行：只读、零写入、
退出码 `0` = 零 finding / `1` = 有 finding / `2` = 输入错误（owner 缺失、名册不可解析、门禁 owner 不可解析、
算子 id 缺失或重复）。JSON MUST 含 `action`、`checked_at`、`stages`（行数）、`gates`（六面数）、
`findings[]`（每项含 `kind` / `stage` / `message`）。
该动作只在**框架源仓**运行（存在 `templates/commands/` 或可解析的 `skills/{external,internal}/`）；
载荷根（客户项目 `.specify/` 形态）MUST 以 `framework-source-required` 退出码 2 结束，MUST NOT 产出 findings、MUST NOT 判绿。

（FR-001、FR-005；SC-001）

- **C-14** 既有判定不被本契约改写

本契约 MUST NOT 修改分类判据、两个取值的含义、台账行语法或六面门禁判据——它们的 owner 分别是
`shared/definitions/flow-class-definitions.md` § 判据 与 `shared/workflow/expression-gates.md`。
映射只**引用**这些判定，不重新定义；判据变更时映射随之复核，MUST NOT 另立映射版本。

（FR-001、FR-004）
