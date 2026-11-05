# Requirements Specification: Self-Explanatory Framework Integration（不言自明的框架集成）

**Requirement Branch**: `082-self-explanatory-integration`  
**Created**: 2026-11-04  
**Status**: Draft  
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "把这份定义落成框架集成的特性规格（宪章/instructions 输出、镜像、测试）。依据本轮访谈收敛的三份制品：shared/definitions/self-explanatory-definitions.md、shared/guidelines/self-explanatory.md、shared/workflow/best-practice-optimization.md。"

## Related Feature *(mandatory)*

**Feature ID**: 082  
**Feature Name**: Self-Explanatory Framework Integration（不言自明的框架集成）

## Assumptions（clarify 阶段逐条裁决；每条给出裁决、证据与对产物的影响）

裁决语法：**ratified** = 原假设成立、证据在仓内可复核；**revised** = 前提成立但表述或边界需改写，改写内容即该条正文；**superseded** = 该假设要交给后续阶段做的事已在本阶段完成。没有一条被静默丢弃。

- **A1（类别判定 = execution，basis = mixed-oracle）— 裁决：ratified**。主交付物是治理文本、模板、生成器与镜像/测试的组合：治理文本由读者判，模板生成、镜像一致性与契约测试由机器判。按 `shared/definitions/flow-class-definitions.md` § 判据，两面都必须签字 → `mixed-oracle` → 类别取 `execution`，`Flow Type` 写 `-`。缺陷最先在机器面暴露（模板缺失原则、镜像漂移、测试不红），故本规格至少一条 `final` 路径 SC 是合理的。
- **A2（输入与概念 owner）— 裁决：ratified**。本特性的输入是访谈收敛的三份制品：`shared/definitions/self-explanatory-definitions.md`（概念 owner）、`shared/guidelines/self-explanatory.md`（实践 owner）、`shared/workflow/best-practice-optimization.md`（优化工作流 owner）。本特性只做框架集成，不重定义概念；任何输出面 MUST 以指针或摘要引用 owner，MUST NOT 复制 owner 的完整定义。
- **A3（Two Hats）— 裁决：ratified**。框架源是 `templates/`、`skills/`、`shared/`；`.specify/` 同名文件是生成镜像或本仓运行时。宪章模板与指令模板属于框架源；`.specify/memory/constitution.md` 与 `.specify/instructions.md` 是本仓运行时输出，由命令/生成器刷新，MUST NOT 用手改镜像代替源修复。机制与拓扑归 `shared/definitions/dogfooding-definitions.md` § 2.1，此处不复述。
- **A4（编号差异）— 裁决：ratified**。宪章模板当前有 17 条原则，本仓 live 宪章当前有 18 条；新原则在各自表面取“下一个可用编号”，MUST NOT 把模板编号硬编码到 live 或测试。`tests/contract/test_constitution_double_landing.py` 的计数常量 MUST 各自 +1，并保持“数值不参与标题匹配”的既有形态。
- **A5（`/speckit.improve` 接线不在本特性）— 裁决：ratified**。访谈 D23 要求每次 `/speckit.improve` 参考优化工作流；本特性只把 `shared/workflow/best-practice-optimization.md` 纳入镜像与分发，MUST NOT 声称已完成 `/speckit.improve` 的接线。该接线已登记为 `OI-082-01`（见 `.specify/memory/register.md`），作为后续 `/speckit.improve` 改进项处理。
- **A6（术语登记）— 裁决：ratified**。概念的中文规范名是“不言自明”，英文规范名是“Self-explanatory”；旧名“望文生义”仅作为退役变体保留。glossary 条目按 `origin=auto`、`status=proposed` 登记，用户确认后再提升为 `confirmed`；MUST NOT 让旧名成为第二个 canonical 条目。
- **A7（文档页）— 裁决：ratified**。访谈收尾已创建 `docs/concepts/self-explanatory.md` 指针页；本特性只保证该页引用的 owner 路径在源与镜像中存在，MUST NOT 把 owner 正文复制进文档页。
- **A8（零 clarification marker）— 裁决：ratified**。本规格不含 `[NEEDS CLARIFICATION]` 标记；所有取舍均可在访谈台账（`.specify/memory/session/interview-wangwenshengyi.md`）与三份 owner 制品中复核。
- **A9（containment 声明）— 裁决：ratified**。FR-005 与 FR-009 的“既有内容不被覆盖 / 符号链接不变”是 containment claim：baseline = 生成前 live instructions 的文件内容与符号链接目标；allowed delta = 新注入的 [[STR-001]] 小节与生成器备份文件；测试按 baseline 快照 + allowed-delta 断言，超出即失败。
- **A10（instructions 预算裁决）— 裁决：ratified（clarify 2026-11-04）**。live `.specify/instructions.md` 当前 32,739 B，预算常量 32,768 B，余量仅 29 B；新增小节必然超预算。裁决：在新增小节的同一变更中把 `INSTRUCTIONS_BUDGET_BYTES` 提高**最小必要幅度**并记录理由；MUST NOT 通过删除既有小节腾空间，也 MUST NOT 静默接受超预算。预算数字的 owner 仍是 `scripts/bash/generate-instructions.sh`。
- **A11（客户面向指针路径）— 裁决：ratified（clarify 2026-11-04）**。宪章/instructions 模板会被原样复制到客户项目；客户端只有 `.specify/shared/...`，没有框架源的 `shared/...`。故客户端面向输出 MUST 使用运行时路径 [[STR-004]]；`shared/...`（[[STR-002]]）只作为框架源 owner 路径。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 宪章生成后，原则自动出现在框架与客户项目 (Priority: P1)

作为框架维护者，我运行 `/speckit.constitution` 或使用宪章模板时，希望“不言自明”作为一条编号原则出现，并指向 shared 层的概念 owner；这样框架自身与客户项目都获得同一份治理规则，而不是各自维护一份定义。

**Why this priority**: 宪章是最高权威面；如果原则只在 shared 文档里存在、没有进入宪章输出，客户项目不会把它当作治理规则。

**Independent Test**: 在临时夹具中断言 `templates/constitution-template.md` 本身包含 [[STR-001]] 与 [[STR-002]]；并通过 `manage-constitution` 技能的模板引导路径断言生成后的 live 宪章包含该原则。不要求新建一个宪章生成器。

**Acceptance Scenarios**:

1. **Given** 一个没有宪章的项目夹具，**When** `manage-constitution` 从 `templates/constitution-template.md` 引导生成宪章，**Then** 输出包含 [[STR-001]] 条目，并指向 [[STR-002]]。
2. **Given** 本仓现有的 `.specify/memory/constitution.md`，**When** 本特性落地后读取它，**Then** 它包含 [[STR-001]]，且版本号高于落地前的版本。

---

### User Story 2 - instructions 输出后，代理能看见规则并到达 owner (Priority: P1)

作为框架维护者，我运行 `/speckit.instructions` 或使用 instructions 模板时，希望出现一个“不言自明”的常驻小节，指向 shared 层 owner；这样每个客户项目的代理在启动时就能看到规则摘要，并知道去哪里读完整定义。

**Why this priority**: instructions 是代理的常驻上下文；只有宪章原则而没有 instructions 摘要，规则不会进入日常执行面。

**Independent Test**: 在一个已有 live instructions 的临时夹具上运行 `scripts/bash/generate-instructions.sh`；断言 [[STR-001]] 小节被增量注入，且该小节包含 [[STR-002]]。

**Acceptance Scenarios**:

1. **Given** 一个已有自定义 instructions 的项目夹具，**When** 生成器运行，**Then** 新小节被追加/注入，既有自定义内容保持不变。
2. **Given** 本仓的 `.specify/instructions.md` 与兼容符号链接，**When** 本特性落地后检查，**Then** live 文件包含 [[STR-001]]，且 `CLAUDE.md` / `QODER.md` / `AGENTS.md` 仍是指向 live 文件的符号链接，而不是被手写复制。

---

### User Story 3 - shared owner 被镜像并随 init 分发 (Priority: P1)

作为客户项目维护者，我执行 `specify init` 后，希望在 `.specify/shared/` 下看到三份 owner 文档；这样宪章与 instructions 中的指针在客户运行时是可解析的，而不是指向框架源里才存在的路径。

**Why this priority**: 指针如果落空，宪章/instructions 的输出就只是装饰；镜像与分发是“指针可达”的前提。

**Independent Test**: 运行 `python3 scripts/python/sync-mirrors.py --check` 断言退出 0；在一个临时目录执行 `specify init`，断言三份文档出现在 `.specify/shared/` 对应位置。

**Acceptance Scenarios**:

1. **Given** 三份源文档已存在于 `shared/`，**When** 运行 `sync-mirrors.py --check`，**Then** 退出 0，且三对源/镜像逐字节一致。
2. **Given** 一个临时空项目，**When** 执行 `specify init`，**Then** 概念、实践与优化工作流三份文档都出现在 `.specify/shared/` 下。

---

### User Story 4 - 测试与词汇表把集成钉住 (Priority: P2)

作为框架维护者，我希望契约测试和 glossary 条目把这次集成钉住：删掉原则、删掉 instructions 小节、或让镜像漂移，都会有测试变红；新术语也能被词汇表检索到。

**Why this priority**: 本次改动主要是治理文本与镜像，最容易在一段时间后被静默改回；测试是唯一的回归防线。

**Independent Test**: 在临时副本中分别删除宪章原则、instructions 小节、镜像文件，运行对应契约测试并断言失败；在真实树上运行同一测试并断言通过。

**Acceptance Scenarios**:

1. **Given** 真实树，**When** 运行 `tests/contract/test_constitution_double_landing.py`、`tests/contract/test_instructions_section_propagation.py` 与镜像一致性测试，**Then** 全部通过。
2. **Given** 一个被删掉宪章原则的临时副本，**When** 运行 double-landing 测试，**Then** 测试失败并点名缺失的原则。
3. **Given** 词汇表，**When** 检索 [[STR-003]]，**Then** 条目存在，旧名仅作为变体出现，且状态为 `proposed`。

### Edge Cases

- **模板与 live 的编号不同**：模板 17 条、live 18 条；新原则各自取下一个编号。测试必须按标题集合匹配，不得按固定罗马数字断言。
- **已有客户项目**：live 宪章/instructions 可能已有自定义内容；生成器必须增量注入，MUST NOT 覆盖或删除既有小节。
- **instructions 体积预算**：新增小节可能推高 live 文件体积；生成器必须报告体积，owner 是 `scripts/bash/generate-instructions.sh` 的预算常量；本特性不得为通过预算而删减既有小节。
- **镜像漂移**：缺少镜像或镜像与源不一致时 `--check` 必须退出 2；镜像独有文件不得被静默当作有效源。
- **词汇表冲突**：旧名“望文生义”不得成为第二个 canonical 条目；它只能作为“不言自明”的变体。
- **init 分发**：只存在于镜像、没有源的文件不会被 `specify init` 分发；三份文档必须同时存在于源与镜像。
- **工作流接线**：优化工作流文档会被镜像，但 `/speckit.improve` 的接线不在本特性；任何验收不得把“文档已镜像”误读为“命令已接线”。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `templates/constitution-template.md` MUST 在下一个可用编号处新增标题为 [[STR-001]] 的原则；正文 MUST 以规范语句覆盖：① 用户视角/以人为本；② 上限是直接看到、下限是一个简单命令，且下限满足即可支持一次改造；③ 不是预防性优化，必须有具体用户信息需求；④ 每个优化任务最多增加一个维度，调协是实现该维度的手段；⑤ 被编码属性保留原真源，名称/路径是投影并最终一致。正文 MUST 指向客户端运行时可解析的 [[STR-004]] 获取完整定义；框架源 owner 仍是 [[STR-002]]。正文 MUST NOT 复制 owner 的完整正文。
- **FR-002**: `skills/internal/manage-constitution/SKILL.md` 的必含原则清单 MUST 加入 [[STR-001]]，使生成器把该原则视为 mandatory；命令模板 MUST 继续保持委派形态，MUST NOT 形成第二份原则清单。
- **FR-003**: `.specify/memory/constitution.md` MUST 通过 `/speckit.constitution`（`manage-constitution` 技能）增加 [[STR-001]] 原则并推进版本号；版本推进的 Sync Impact Report MUST 记录该新增。live 原则的编号 MUST 取该表面的下一个可用编号，MUST NOT 从模板复制编号。
- **FR-004**: `templates/instructions-template.md` MUST 新增一个以 [[STR-001]] 命名的常驻小节；小节 MUST 只承载摘要 + 指向客户端运行时可解析的 [[STR-004]] 的指针（其源 owner 是 [[STR-002]]），MUST NOT 复制 owner 的完整定义或实践步骤。小节 MUST 遵守 instructions 体积预算；鉴于当前余量仅 29 B，本特性 MUST 在同一变更中把 `INSTRUCTIONS_BUDGET_BYTES` 提高**最小必要幅度**并记录理由，MUST NOT 通过删除既有小节腾空间，也 MUST NOT 静默接受超预算。预算数字的 owner 仍是 `scripts/bash/generate-instructions.sh`。
- **FR-005**: `.specify/instructions.md` MUST 通过 `scripts/bash/generate-instructions.sh`（`/speckit.instructions` 的生成步骤）刷新，使 live 文件包含 [[STR-001]]；该生成器的既有行为是向已有 live 文件增量注入缺失模板小节，MUST NOT 覆盖或删除既有内容；兼容符号链接 MUST 继续指向 live 文件，MUST NOT 被改写为独立副本。
- **FR-006**: 三份 shared 源文档 MUST 通过 `scripts/python/sync-mirrors.py --write` 镜像到 `.specify/shared/definitions/self-explanatory-definitions.md`、`.specify/shared/guidelines/self-explanatory.md` 与 `.specify/shared/workflow/best-practice-optimization.md`；`sync-mirrors.py --check` MUST 退出 0，且三对文件逐字节一致。[[STR-002]] 是其中概念 owner 的源路径。
- **FR-007**: `specify init` 的分发结果 MUST 包含三份文档；在一个临时空项目上初始化后，三份文档 MUST 出现在 `.specify/shared/` 对应位置。只存在于镜像、没有源的文件 MUST NOT 被当作已分发。[[STR-002]] 是概念 owner 的源路径。
- **FR-008**: `tests/contract/test_constitution_double_landing.py` MUST 把 [[STR-001]] 加入 `DOUBLE_LANDING_WATCHLIST`，并把 `TEMPLATE_COUNT`、`LIVE_COUNT`、`COMMAND_COUNT` 各加一；测试 MUST 在模板、live 宪章或生成器必含清单任一缺失该原则时失败，MUST 在真实树上通过。
- **FR-009**: instructions 契约测试 MUST 断言 live `.specify/instructions.md` 包含 [[STR-001]] 小节，且该小节包含 [[STR-004]] 指针（在客户端解析到 [[STR-002]] 的镜像副本）；测试 MUST 使用临时夹具验证“已有 live 文件时增量注入、既有内容不被覆盖”，并 MUST 在移除**模板侧**小节时直接断言模板/生成器输入缺失而失败；不得只依赖 live 文件断言，因为 live 可能保留旧小节而让变异空转。
- **FR-010**: 镜像契约测试 MUST 覆盖三份新文档：断言源与镜像逐字节一致、`sync-mirrors.py --check` 退出 0，并 MUST 在镜像缺失或漂移时失败。既有 `tests/contract/test_mirror_parity_suite.py` 已按 `MIRROR_PAIRS` 动态覆盖新文件；本特性 MUST 复用该套件，MUST NOT 复制一份新的对表。[[STR-002]] 是概念 owner 的源路径。
- **FR-011**: `.specify/memory/glossary.md` MUST 登记 [[STR-003]]，`origin=auto`、`status=proposed`；旧名“望文生义”MUST 只作为该条目的退役变体出现，MUST NOT 成为第二个 canonical 条目。`tests/contract/test_glossary_mechanism.py` MUST 通过。
- **FR-012**: `docs/concepts/self-explanatory.md` MUST 保持为指针页，MUST 指向 [[STR-002]] 与优化工作流 owner；本特性 MUST 提供一个链接检查或契约断言，确保该页引用的路径在源与镜像中存在；该检查 MUST 复用既有 pytest/镜像/链接检查面，MUST NOT 新建独立链接检查引擎。信息内容 MUST NOT 从 owner 复制成一页新定义。

### Key Entities

- **Principle entry**: 标题 [[STR-001]]、所在编号、指向 [[STR-002]] 的指针、在模板/live/生成器清单三处的存在形态。
- **Owner docs**: 概念定义、实践指南、优化工作流三份 shared 文档；概念定义是唯一 owner，其余两份是实践与工作流 owner。
- **Output surfaces**: 宪章模板/live 宪章、instructions 模板/live instructions、兼容符号链接。
- **Mirror twins**: `.specify/shared/` 下与三份源文档逐字节一致的运行时副本。
- **Contract tests**: double-landing、instructions propagation、mirror parity、glossary mechanism 四类守卫。
- **Glossary entry**: canonical [[STR-003]]、退役变体“望文生义”、`origin=auto`、`status=proposed`。

### Runtime Stack & Dependency Ownership

本特性交付的运行时能力是 `specify init` 分发（RS-004）；其余是外部供给、本仓只消费的能力，按 `signed-contract` 记录。零散文行：每一行都必须可机械判。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（跑 validator、镜像检查与契约测试） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin） | `pyproject.toml` | 本特性全部确定性检查在 `>=3.8` 解释器上通过；静态 import 清单为空 | FR-008, FR-009, FR-010 | EP-001 |
| RS-002 | pytest（契约/单元测试运行器） | signed-contract | pytest 上游（本仓只消费） | `pytest --version` 原文记录在 `test-evidence/` | `scripts/bash/run-tests.sh` | 定向集与全量在记录的 pin 上复现；新增测试全绿 | FR-008, FR-009, FR-010 | EP-001 |
| RS-003 | `git`（提交、状态与基线比较） | signed-contract | git 上游（本仓只消费） | `git --version` 原文记录在 `test-evidence/` | `scripts/bash/common.sh` | 阶段提交与 `git status --porcelain` 判定成功 | FR-008 | EP-001 |
| RS-004 | `specify init` 分发（三份 owner 文档随 init 到达客户项目） | in-scope | 本仓 `src/` + `scripts/python/sync-mirrors.py` | 仓内 commit（同一变更） | `src/specify_cli/__init__.py` | 临时夹具执行 `specify init` 后三份文档出现在 `.specify/shared/` | FR-007 | EP-002 |

**Contract-cell note**: each `Contract` cell carries exactly one repo-relative path; secondary references are evidence, not a second contract.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 宪章模板与 live 宪章都包含 [[STR-001]]，且两者都指向客户端运行时可解析的 [[STR-004]]（其源 owner 是 [[STR-002]]）；生成器必含清单也包含该标题。**Path**: final
- **SC-002**: live 宪章的版本号高于 baseline（`git show HEAD:.specify/memory/constitution.md` 的版本行，当前 1.15.0），且 Sync Impact Report 记录了新增原则；baseline 与结果都记录在证据中。[[STR-001]] **Path**: supporting
- **SC-003**: instructions 模板与 live 文件都包含 [[STR-001]] 小节，且该小节包含客户端运行时可解析的 [[STR-004]] 指针（其源 owner 是 [[STR-002]]）；在已有 live 文件的夹具上增量注入成功。**Path**: final
- **SC-004**: `sync-mirrors.py --check` 退出 0，三对源/镜像逐字节一致，镜像一致性测试覆盖三份新文档。[[STR-002]] **Path**: final
- **SC-005**: 临时空项目执行 `specify init` 后，三份文档出现在 `.specify/shared/` 对应位置。[[STR-002]] **Path**: final
- **SC-006**: 变异演练中，删除宪章原则、删除 instructions 小节、或让镜像漂移，至少各有一个契约测试变红；真实树上同一组测试全绿。**Path**: supporting
- **SC-007**: glossary 中存在 [[STR-003]]，旧名仅作为变体，状态为 `proposed`。**Path**: supporting
- **SC-008**: `docs/concepts/self-explanatory.md` 中指向 [[STR-002]] 与工作流 owner 的链接可解析。**Path**: supporting
- **SC-009**: 新增小节落地后，`generate-instructions.sh` 报告 live instructions 体积不超过**修订后的** `INSTRUCTIONS_BUDGET_BYTES`；新常量与理由记录在同一变更的证据中。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: `pytest tests/contract/test_constitution_double_landing.py`，以及 `grep -F` 检查模板/live/生成器清单；每次运行记录命令、退出码与命中行。
- **SC-002 Source**: `git show HEAD:.specify/memory/constitution.md` 取 baseline 版本行，与落地后的 `.specify/memory/constitution.md` 版本行及 Sync Impact Report 比较；记录两条命令与输出。
- **SC-003 Source**: 在临时夹具上运行 `bash scripts/bash/generate-instructions.sh`；随后 `grep -F` live 文件；再运行 `pytest tests/contract/test_instructions_section_propagation.py`。
- **SC-004 Source**: `python3 scripts/python/sync-mirrors.py --check` 的退出码；`pytest tests/contract/test_mirror_parity_suite.py` 的三组新参数。
- **SC-005 Source**: 在临时目录运行 `specify init`，列出 `.specify/shared/` 下的三份文件；记录初始化命令、退出码与文件清单。
- **SC-006 Source**: 在临时副本上做三组变异（删原则、删小节、改镜像），分别运行对应 pytest 并记录非零退出；真实树同组测试记录零退出。
- **SC-007 Source**: `grep -F` `.specify/memory/glossary.md` 的 canonical/变体/status 字段；`pytest tests/contract/test_glossary_mechanism.py`。
- **SC-008 Source**: 对 `docs/concepts/self-explanatory.md` 的链接目标做 `test -e` 或等价链接检查。
- **SC-009 Source**: 运行 `bash scripts/bash/generate-instructions.sh`，读取体积报告与新常量值；记录命令、退出码、报告行与调高理由。

## Constraints（落地约束，判据在外部 owner）

- **Two Hats**：本特性改框架源（`templates/`、`skills/`、`shared/`）；`.specify/` 同名文件是运行时输出或镜像。机制归 `shared/definitions/dogfooding-definitions.md` § 2.1，此处不复述（承载 FR-001—FR-007）。
- **One Source of Truth**：判据归 `shared/guidelines/one-source-of-truth.md`；概念 owner 是 [[STR-002]]，宪章/instructions 只持有摘要或指针，MUST NOT 复制完整定义（承载 FR-001、FR-004、FR-012）。
- **Program-First / Token Efficiency**：判据归 `shared/guidelines/token-efficiency.md`；本特性的验收以确定性测试、`grep`、镜像检查与 init 夹具为主，不依赖模型目测（承载 FR-008—FR-010）。
- **Fast Fail**：判据归 `shared/guidelines/fast-fail.md`；镜像漂移、缺失原则、缺失小节都必须让测试变红并阻断，不得静默跳过（承载 FR-008—FR-010）。
- **Instructions size budget**：预算数字的 owner 是 `scripts/bash/generate-instructions.sh`；本规格不复制该数字，只要求新增小节遵守它，并在 29 B 余量不足时以最小必要幅度上调常量、记录理由（承载 FR-004、A10、SC-009）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `Self-Explanatory Structure (不言自明)` | FR-001, FR-002, FR-003, FR-004, FR-005, FR-008, FR-009, SC-001, SC-002, SC-003 |
| `STR-002` | `shared/definitions/self-explanatory-definitions.md` | FR-001, FR-004, FR-006, FR-007, FR-009, FR-010, FR-012, SC-001, SC-003, SC-004, SC-005, SC-008 |
| `STR-003` | `不言自明 (Self-explanatory)` | FR-011, SC-007 |
| `STR-004` | `.specify/shared/definitions/self-explanatory-definitions.md` | FR-001, FR-004, FR-009, SC-001, SC-003 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-11-04

- Q: 082 的 `Related Feature` 如何绑定？ → A: 创建新 Feature 082（复核 079/051/052/029 后无归属），落索引行与 `features/082.md`。
- Q: live instructions 距预算仅 29 B，新增小节必然超预算；如何处理？ → A: 在新增小节同一变更中把 `INSTRUCTIONS_BUDGET_BYTES` 提高**最小必要幅度**并记录理由；不删既有小节、不静默超预算。
- Q: 客户项目只有 `.specify/shared/...`，输出中的 owner 指针用哪种路径？ → A: 客户端面向输出使用运行时路径 [[STR-004]]；`shared/...`（[[STR-002]]）仅作为框架源 owner 路径。
- Q: `/speckit.improve` 接线如何登记？ → A: 登记为 `OI-082-01`，作为后续 `/speckit.improve` 改进项。
