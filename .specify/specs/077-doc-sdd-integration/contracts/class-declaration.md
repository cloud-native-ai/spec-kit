# Contract: 特性线类别声明（Class Declaration）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：判据与取值归 `shared/definitions/flow-class-definitions.md`；默认标记字面量归 069 § Shared Strings；
声明行字面量 `**Flow Class**` 归 requirements § Shared Strings（[[STR-001]]）。本契约不复制判据正文。

## 声明行

- **C-001** 每条特性线 MUST 在其 `requirements.md` 头部区（`## Related Feature` 标题之前）**至多**声明一行类别字段。行形态逐字为「`**Flow Class**` + 半角冒号 + 一个空格 + 取值」，行尾 MUST NOT 有尾随空白。字段名与取值均大小写敏感；全角冒号、字段名大小写变体、行内附加注释一律不合语法。**作用域 = 新增声明线**：本特性落地前已存在的特性线不承担回填义务，它们按 C-008 的缺省路径解析并可获 advisory 码 `declaration-absent`（见 C-008）；存量条数取 `.specify/specs/*` 的实际目录集，本契约不记数。(FR-001)

- **C-002** 取值 MUST 为封闭二值 `execution` / `expression`。取值 MUST 只由作者判定；脚本 MUST NOT 从路径、文件名、
  扩展名、内容或提交信息推断类别。(FR-001)

- **C-003** `templates/requirements-template.md` MUST 在头部区携带该字段行，位置为 `**Status**:` 行之后、
  `**Input**:` 行之前，值 MUST 以占位形态出现（由作者替换），MUST NOT 预填某个类别。模板 MUST NOT 携带判据句、
  取值定义或任何「如何判定」的说明——只出现字段行本身。(FR-001, FR-023)

- **C-004** 该行在**整个文件**内出现第二次，不论两次取值是否相同，MUST 报 `declaration-duplicate`。判定 MUST 只读行数，
  MUST NOT 读取两次取值是否一致。(FR-001)

- **C-005** 该行位于 `## Related Feature` 标题之后时 MUST 报 `declaration-misplaced`。判定 MUST 只读位置，
  MUST NOT 依赖评审阅读。(FR-001)

- **C-006** 字段在场而形态不合 C-001 时 MUST 报 `declaration-malformed`，MUST NOT 落成「无该字段」。
  三种形态错误（全角冒号、字段名大小写变体、行内附加注释或尾随空白）各产生该码一次，
  MUST NOT 合并成一句无定位的警告。(FR-001, FR-005)

## 单一真源

- **C-007** 类别取值 MUST 只存在于声明行。`.specify/memory/features.md` MUST NOT 新增类别列，
  `.specify/memory/features/<ID>.md` MUST NOT 保存该取值；两处至多留一条指向声明行的指针。
  同一特性线出现第二处声明 MUST 判缺陷并由确定性检查报出，MUST NOT 依赖人工阅读发现。(FR-002)

## 缺省与阻断

- **C-008** 无该字段的特性线 MUST 按 `execution` 运行，`source` MUST 标为 `default`，并在每个消费点显示
  069 登记的默认标记。未声明 MUST NOT 被呈现为已判定，也 MUST NOT 被读作表达类。未声明 MUST 分两种可区分形态：
  **存量缺省**（头部区无该行，属 C-001 作用域之外）可附 advisory 码 `declaration-absent`——退出码 0、不计缺陷、
  不进判定集合；**机制降级**（owner 不可解析 / 调用方无法执行引擎，见 `class-resolution.md` C-012）记录
  `error.label = owner-unavailable`，MUST NOT 被标 `declaration-absent`。(FR-004)

- **C-009** 取值在封闭集之外 MUST 按阻断处理：解析侧退出码 1，声明所在阶段的门禁 MUST 以非零退出阻断，
  并点名文件、行号与越界取值。MUST NOT 静默回落默认类，MUST NOT 继续以 `execution` 运行。**阶段侧的呈现 MUST 是「停下」**：
  阶段命令的接线子节 MUST 要求本阶段在解析退出码为 1 时停止后续动作，并以阶段协议的异常行形态
  （owner：`skills/external/sdd-loop-driver/references/stage-prompts.md`）作最后一行输出；
  MUST NOT 落入「其余既有门禁集逐字不变」那一支继续执行。(FR-005)

- **C-010** 作者输入错误（C-004 / C-005 / C-006 / C-009 四个码）MUST 全部归退出码 1，MUST NOT 归退出码 2。
  判据：退出码 2 的语义是「机制缺席、保持既有门禁集」（见 `class-resolution.md` C-006），把作者笔误判成 2
  会让该线在没有提示的情况下按执行类跑完，正是 C-009 要禁的事。(FR-005, FR-009)

## 时点与作用域

- **C-011** 类别 MUST 在任何阶段作出第一次门禁判定之前可读，包括 requirements 自身。requirements 阶段的读取
  MUST 发生在声明行写入之后、`validate-requirements.py` 之前。(FR-006)

- **C-012** 声明行在 requirements 阶段门禁通过之后被写入、修改或删除的，MUST 记为 re-baseline 事件（写入阶段记录）
  并按新类别重跑 requirements 门禁集。MUST NOT 静默翻转。(FR-006)

- **C-013** 声明单位 MUST 是特性线（一条 spec 目录）。同一 Feature 的多个切片各自声明、允许不同类别，
  注册表 MUST NOT 把它们汇总为一个取值；`feature:<ID>` MUST NOT 作为类别解析的键。(FR-007)
