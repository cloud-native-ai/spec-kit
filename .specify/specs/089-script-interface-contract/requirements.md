# Requirements Specification: 脚本接口契约（Script Interface Contract）

**Requirement Branch**: `089-script-interface-contract`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "为了避免后续再出现『我执行 generate-instructions.sh --help 想看接口，该脚本没有 --help 处理，直接把一次 reconcile 跑了起来——向 .specify/instructions.md 追加了 11 个缺失的模板章节（diff 为 +70 行、0 行删除）』这样的问题，需要在 constitution 中增加所有的 *.sh/*.py 脚本都需要默认添加 --help/--version 参数。"（补充裁定：落点为 `templates/constitution-template.md` + `templates/instructions-template.md` + 本仓宪法 + 生成器 + 镜像/契约测试 pin；这是随 `specify init` 分发的通用规则，不只服务本仓库。）

## Related Feature *(mandatory)*

**Feature ID**: 086
**Feature Name**: 脚本接口契约（Script Interface Contract）

## Overview

用户在执行 `generate-instructions.sh --help` 想查看脚本接口时，该脚本没有参数解析：`--help` 被当作普通参数忽略，脚本继续执行其主动作（reconcile），把 11 个缺失的模板章节追加进 `.specify/instructions.md`（+70 行 / 0 行删除）。这是一次**只读意图被解释为写入意图**的事故：用户想知道的只是接口，得到的却是一次不可预期的写盘。

根因不是这一个脚本写错了，而是框架里从来没有一条规则要求「可执行脚本必须声明自己的接口」。结果有三层：

1. **接口不可发现**：脚本没有 `--help`，用户与 AI agent 只能读源码猜参数；`--version` 缺失使「这份脚本是哪个版本、是否已被下游项目改写」无法回答。
2. **未知参数被静默吞掉**：无参数解析的脚本把无法识别的选项当位置参数，继续执行主动作——`--help` 不是被拒绝，而是被执行。
3. **帮助路径本身有副作用**：即使有 `--help` 的脚本，也没有约束要求「帮助与版本判定先于任何副作用」，于是帮助信息与写盘可能同时发生。

本特性新增一条**框架级通用治理规则**：所有可直接执行的 `*.sh` / `*.py` 脚本 MUST 支持 `-h` / `--help` 与 `--version`，两者为零副作用，未知选项 MUST 以非零退出码报错并给出用法。规则同时落在五处：框架宪法模板（下游项目经 `specify init` 获得）、指令模板的常驻段落（summary + pointer）、本仓宪法、`manage-constitution` 的 MUST include 清单，以及镜像与契约测试 pin。规则之外，本特性必须把**本仓现存适用脚本**补齐到该契约，而不是只新增一段规则文字。

规则只约束「脚本的入口契约」，不约束脚本内部实现；不新建命令、不新建运行时服务、不新增第二道确认门。

> **七个承重定义已裁定，正文不重复**（2026-11-06 clarify）：候选面 / 豁免判据（bash 与 python 各一条）/ 第三方来源 / `--version` 形态 / 已声明例外登记 / 零副作用取证 / 标志判定前置的可实施形态。逐条 Q/A 与理由见 § Clarifications，约束条款见 FR-024 … FR-031（其中 **FR-028 是墓碑**：内容并入 FR-027，编号不复用）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 用 `--help` 看接口不再触发任何写盘（Priority: P1）

用户（或 AI agent）想确认一个脚本能做什么。执行 `--help`（或 `-h`）后，输出用法、参数、该脚本是否产生副作用与退出码含义，进程随即以成功码退出；脚本的主动作没有执行，工作树与运行时目录逐字节未变。

**Why this priority**: 这正是事故本身。帮助路径一旦可能有副作用，用户就再也不能安全地「先看看接口」，而只能读源码——接口发现成本永久性地转移给读者。

**Independent Test**: 在一个有未提交改动的工作树上，对每个适用脚本执行 `-h` 与 `--help`，比较执行前后的 `git status --porcelain` 与受管目录的文件指纹；断言两者完全一致、退出码为 0，且输出包含该脚本的用法文本。

**Acceptance Scenarios**:

1. **Given** 一份有未提交改动的工作树，**When** 对任一适用脚本执行 `--help`，**Then** 输出该脚本的用法、参数、副作用说明与退出码含义，退出码为 0，且工作树指纹不变。
2. **Given** 同一脚本，**When** 分别执行 `-h` 与 `--help`，**Then** 两者输出同一份用法信息，行为无差别。
3. **Given** 一个会产生写入的脚本（如 `generate-instructions.sh`），**When** 执行 `--help`，**Then** 目标文件不被创建、不被修改、不被追加，且不出现备份文件。

---

### User Story 2 - `--version` 让脚本身份可回答（Priority: P1）

用户或下游项目想知道「这份脚本是哪一版」。执行 `--version` 输出一个版本标识，进程以成功码退出，同样不执行主动作、不写盘。

**Why this priority**: 脚本会随 `specify init` 分发到下游项目并被本地改写；没有版本标识，下游无法判断自己的副本是否已经落后或已被改坏，框架也无法在反馈里定位问题版本。

**Independent Test**: 对每个适用脚本执行 `--version`，断言退出码为 0、输出非空且形如单行标识符、执行前后工作树指纹不变。

**Acceptance Scenarios**:

1. **Given** 任一适用脚本，**When** 执行 `--version`，**Then** 输出一行版本标识、退出码为 0，且不执行主动作。
2. **Given** 同一脚本的 `--version` 与 `--help`，**When** 两者在同一状态下执行，**Then** 版本标识与帮助中的声明一致（版本只有一个来源）。
3. **Given** 一个携带 `--version` 之外的未知选项的调用，**When** 该选项无法识别，**Then** `--version` 不因该选项被忽略而改变语义（见 US3：未知选项先报错）。

---

### User Story 3 - 未知选项被拒绝，而不是被执行（Priority: P1）

用户把 `--dry-run`、`--help-me`、`--output` 之类脚本并不认识的选项传给脚本。脚本 MUST 拒绝：向标准错误输出「该选项不可识别」与用法提示，以非零退出码结束，并且不执行主动作、不写盘。

**Why this priority**: 这是本次事故的直接根因。`--help` 之所以危险，不是因为帮助本身，而是因为「不认识就忽略」把任何拼错的选项都变成了「照常执行主动作」。缺少这条，US1 只能保护恰好拼对的 `--help`。

**Independent Test**: 对一个会产生写入的脚本传入一个不存在的长选项，断言退出码非零、标准错误包含可识别的错误信息与用法、目标文件未被创建或修改。

**Acceptance Scenarios**:

1. **Given** 一个会产生写入的脚本，**When** 传入一个未定义的选项（如 `--no-such-flag`），**Then** 退出码非零、标准错误说明该选项不被识别并给出用法，主动作不执行、不写盘。
2. **Given** 同一脚本，**When** 传入未定义选项的同时还传入了它认识的选项，**Then** 仍然拒绝，不因存在合法选项而放行。
3. **Given** 一个按位置参数接收自由文本的脚本，**When** 传入以 `--` 开头的、它没有声明的 token，**Then** 该 token 被当作未知选项拒绝（MUST NOT 静默降级为自由文本），而 `--` 之后的内容按声明的约定处理。

---

### User Story 4 - 规则随框架分发给下游项目（Priority: P1）

另一个用 `specify init` 初始化的项目（与 spec-kit 自身无关）拿到的不只是本仓的一条改动，而是这条通用规则：它的宪法里有对应原则，它的 `instructions.md` 由生成器产出后含有对应的常驻段落，用 `/speckit.constitution` 生成或修订宪法时该原则是必须存在项。

**Why this priority**: 用户明确要求这是通用规则而非本仓自用。规则只落本仓宪法时，下游项目永远收不到，事故会在每个下游项目重演。

**Independent Test**: 在一个没有 `.specify/` 的干净临时目录里执行项目初始化与宪法生成，断言生成的宪法含该原则、生成的 `instructions.md` 含对应段落且该段落是「摘要 + 指针」形态（正文由 owner 文档拥有）。

**Acceptance Scenarios**:

1. **Given** 一个干净的下游项目目录，**When** 执行项目初始化，**Then** 下发项目获得的框架模板中，宪法模板含该原则、指令模板含对应的常驻段落。
2. **Given** 下游项目执行 `/speckit.constitution`，**When** 生成或修订宪法，**Then** 生成器把该原则列为必须存在的原则之一，缺则补齐或报错，而不是静默跳过。
3. **Given** 一次宪法修订，**When** 修订落盘，**Then** 产出 Sync Impact Report，版本号按 `x.y.z` 递增（新增原则 = MINOR 增量），并更新「Last Amended」日期。

---

### User Story 5 - 本仓现存脚本补齐到契约（Priority: P1）

本仓库自己就是最大的使用方。规则落地后，本仓所有适用脚本 MUST 满足契约：`scripts/bash/*.sh`（及其 `.specify/` 镜像）、`scripts/python/*.py`（及其镜像）、`skills/**/scripts/` 下具备独立执行入口的脚本，逐个具备 `-h/--help`、`--version`、未知选项拒绝与零副作用；被 `source` / `import` 的纯库文件按下述豁免判据排除。

**Why this priority**: 只新增规则文字而不补齐现存脚本，等于让规则从第一天起就是假的；而且下一个被用户按 `--help` 探索的脚本仍会执行主动作。

**Independent Test**: 运行一次全量判定，输出每个适用脚本的四项结论（help / version / 未知选项拒绝 / 零副作用），断言违规计数为 0；同时打印豁免清单及其逐条判据证据。

**Acceptance Scenarios**:

1. **Given** 本仓 `scripts/bash/` 下的每个 `.sh`，**When** 逐个执行 `--help`、`--version` 与一个未知选项，**Then** 前两者退出码为 0 且输出非空，后者退出码非零，且三者都不改变工作树。
2. **Given** 本仓 `scripts/python/` 下的每个 `.py`，**When** 以同样方式探测，**Then** 结论同上；`argparse` 产生的 `--help` 之外的实现同样可接受，判据是**外部可观察行为**，不是实现方式。
3. **Given** `scripts/bash/common.sh` 这类只被 `source` 的库文件，**When** 判定其是否适用，**Then** 它落入豁免清单并给出可机械复核的判据证据（无独立执行入口 / 仅在被 source 时定义符号）。
4. **Given** 一个新增的适用脚本，**When** 它没有实现契约，**Then** 现行检查在提交前报红并点名该脚本与缺失项，而不是等到下一次用户误触发才发现。

---

### User Story 6 - 豁免判据可机械判定，不被当逃生门（Priority: P2)

被 `source` / `import` 的纯库模块（如 `scripts/bash/common.sh`、`scripts/python/declaration_reader.py` 这类无独立入口的模块）不要求 `--help` / `--version`。豁免 MUST 由机械判据决定：脚本是否具备独立执行入口（bash 顶层执行语句，python 的 `if __name__ == "__main__"` 块），而不是由作者声称。

**Why this priority**: 规则没有豁免就会制造无意义的机械改动（给纯库加 help 无意义）；豁免不可机械判定，规则就会被「我声明它是库」绕开。

**Independent Test**: 对副本树做变异——给一个纯库文件加上顶层执行语句（或 `__main__` 块）——断言它随即被判定为适用并从豁免清单移出；去掉即回到豁免。

**Acceptance Scenarios**:

1. **Given** 一个被 `source` 的 bash 库文件，**When** 判定适用性，**Then** 判为豁免，并记录判定依据（无顶层执行入口）。
2. **Given** 一个 python 模块，**When** 移除其 `if __name__ == "__main__"` 块，**Then** 它从适用集迁到豁免集；恢复则迁回。
3. **Given** 一个同时具备独立入口与库用途的文件，**When** 判定适用性，**Then** 判为适用（有独立入口即须支持契约），豁免 MUST NOT 以「它也被 import」为由成立。

---

### User Story 7 - 契约检查进入既有门禁，而非新增一道门（Priority: P2）

规则落地后，违规在既有验证面上可见：脚本接口契约的检查由确定性程序判定并接入既有的测试/门禁集合，输出逐脚本结论与违规计数；宪法与指令模板的双落地由既有的双落地守卫的计数 pin 与 watchlist 覆盖。

**Why this priority**: 没有检查的规则会在几周内退化成文字；但新增一道独立门禁又会增加流程摩擦。目标是复用既有面，只加判据不加步骤。

**Independent Test**: 在副本树上把一个已合规脚本的 help 分支删掉，断言检查报红并点名该脚本；把新原则从宪法模板中删掉，断言双落地守卫报红。

**Acceptance Scenarios**:

1. **Given** 一个已合规脚本，**When** 从副本树中删除其 `--help` 处理，**Then** 确定性检查报红并点名该脚本。
2. **Given** 宪法模板已合入新原则，**When** 在副本树中删除该原则，**Then** 双落地守卫的计数 pin 与 watchlist 断言报红。
3. **Given** 契约检查的运行结果，**When** 与基线比较，**Then** 违规数为 0 且豁免清单逐条带判据证据，无「未评估」条目被当作通过。

---

### Edge Cases

- **帮助与主动作同时被请求**（`script.sh --help --write`）：帮助 MUST 获胜——判定先于任何副作用，主动作不执行。用户不应需要知道选项顺序才能安全地看接口。
- **`-h` 与 `--help` 冲突**：两个形式必须等价；若脚本已把 `-h` 用作其他含义（如 host），则该脚本 MUST 让 `--help` 可用，并在帮助中显式说明 `-h` 的既有含义。**本仓实测（clarify）**：全部 71 个 `.sh` 与 207 个带 `__main__` 块的 `.py` 中，**零**个把 `-h` 用于其他含义——唯一以 `-h)` 形式出现的场合都是与 `--help` 合并的既有帮助分支（`check-prerequisites.sh`、`create-new-plan.sh`、`create-new-requirements.sh`、`create-new-skill.sh`、`create-new-tools.sh`、`implement-plan.sh`、`research-project.sh`）。该 Edge Case 因此对**本仓现存脚本**不适用，只作为规则文本的边界保留，供下游项目使用。
- **`--version` 与下游改写的副本**：下游改了脚本但没有改版本标识时，检查 MUST NOT 声称版本「正确」；它只断言版本标识存在且可解析，副本漂移由别的面负责。
- **脚本需要参数才能确定主动作**：无参数调用 MUST 打印用法并以非零退出码结束（或按既有约定的缺省动作），MUST NOT 在没有任何参数时意外执行一个写动作。
- **纯库文件被直接执行**：`bash common.sh` / `python declaration_reader.py` 被当作脚本运行时，判定 MUST 归入豁免并说明理由，而不是要求作者加 help；若判定为适用，则以非零退出码与用法信息结束。
- **包装脚本（thin wrapper）**：只把参数转发给引擎的 `.sh` 包装脚本同样适用；它的 `--help` MUST 输出自己的用法（至少转发说明），而 `--version` MUST 给出自己的版本标识，不得声称这是被包装引擎的版本。
- **第三方/上游获取的脚本**：随技能分发的第三方脚本（如绘图渲染脚本）仍在适用范围内，但 MUST NOT 被就地改写其上游实现——只允许在入口处加最小的标志处理层；若无法在不改上游的情况下满足契约，则该例外 MUST 以点名记录登记并在检查中作为已声明例外出现。
- **生成物与镜像**：`.specify/scripts/` 是镜像，判定对象以框架源为准，镜像漂移由既有镜像检查负责；不得只在镜像里改而源不改。**复核（clarify）**：`.specify/` 下确有 81 个 `.sh` / `.py` 找不到同路径源文件（其中 73 个是技能目录改名所致，另有 8 个是 `075-sdd-loop-efficiency/notes/` 下的 stub），但它们不是漏同步——镜像机制只投射 `scripts/`、`skills/external/<name>/`、`skills/internal/<name>/`、`shared/`、`templates/`，而这些路径在源树中对应的技能目录名不同（如 `.specify/skills/document-utils/` ↔ `skills/external/document-utils/`）。因此镜像侧 MUST NOT 按路径反查去重来缩短候选面（见 FR-024(d)）。
- **上游来源判定**：`skills/external/` 下技能的上游来源 MUST 以其 `SKILL.md` 自身声明为准。本仓实测（2026-11-06，plan 阶段复核）：`create-skills`、`coaching-skills` 均声明 `classification: external`——requirements 初稿曾误记为 `internal`，以实测为准更正。按 FR-027 二者判为第三方来源；实测其下没有 `*.sh` / `*.py` 脚本，故本特性不修改它们；若将来出现脚本，走 FR-020 的最小入口层或已声明例外。
- **契约与既有的只读约束冲突**：`--help` 必须在任何「需要确认」的前置检查之前返回，否则查接口本身就会被要求确认。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 框架 MUST 提供一条通用治理规则（下称「脚本接口契约」），规定所有可直接执行的 `*.sh` 与 `*.py` 脚本的入口契约；该规则 MUST 作为本项目宪法（框架模板与本仓宪法两侧）中的一条原则存在，并以摘要 + 指针形态出现在指令模板的常驻段落中。

- **FR-002**: 契约的判定对象 MUST 由机械候选屏产生，而不是由一份手写文件名清单。候选面 MUST **既**由范围派生**又**由覆盖断言校验，缺一不可：扫描根集合只由「版本控制枚举」与「`.gitignore` 排除」两个机器可读来源派生（MUST NOT 手写目录名单）；同时扫描结果 MUST 覆盖仓库内全部 `*.sh` 与 `*.py`，集合外若有任何 `*.sh` / `*.py` 存在则检查 MUST 报错并点名（版本控制缺席时这条覆盖断言代替枚举，MUST NOT 退化为「什么都没扫到，于是全过」）。每个候选按「是否具备独立执行入口」判定适用或豁免，并输出两侧清单。MUST NOT 用「作者声明它是库」作为豁免依据。派生规则与覆盖断言的可判定形式见 FR-024。

- **FR-003**: 每个适用脚本 MUST 支持 `-h` 与 `--help`，输出至少包含：用法（调用形态）、可识别的选项及其含义、该脚本是否产生副作用（写哪些路径或调用哪些写型外部命令）、退出码含义。`-h` 与 `--help` MUST 行为等价。

- **FR-004**: 每个适用脚本 MUST 支持 `--version`，输出一行可解析的版本标识并成功退出；版本标识 MUST 只有一个来源，MUST NOT 与其 `--help` 文本或另一处声明漂移。

- **FR-005**: 任一标志（`-h` / `--help` / `--version`）在场时，脚本 MUST NOT 执行主动作、MUST NOT 写文件、MUST NOT 调用写入型外部命令、MUST NOT 创建备份；判定 MUST 先于任何副作用，且先于任何可能要求用户确认的前置检查。

- **FR-006**: 适用脚本遇到未识别的选项 MUST 以非零退出码结束，并在标准错误输出可识别的错误信息与用法提示；MUST NOT 静默忽略该选项后继续执行主动作。存在合法选项 MUST NOT 使未识别选项被放过。

- **FR-007**: 未知选项的判定 MUST 覆盖以 `--` 开头的 token，即使该脚本按位置参数接收自由文本；`--` 之后的参数按脚本声明的约定处理，不被视为未知选项。

- **FR-008**: 无参数调用一个需要参数才能确定主动作的适用脚本时，MUST 打印用法并以非零退出码结束；MUST NOT 在无参数情况下意外执行写入型主动作。

- **FR-009**: 豁免判据 MUST 是机械可判定的，且判据 MUST 只回答「该文件是否具备独立执行入口」。该问题 MUST 以运行语义回答，MUST NOT 以源码字面回答——源码字面在两侧都会误判（bash：被 source 的库把顶层依赖检查写在 source 包装里，按「有无顶层执行语句」会误判为适用；python：被 import 的模块即使带 `__main__` 块也不执行它，按「有无 `__main__` 块」会误判为适用）。可判定定义见 FR-025（bash）与 FR-026（python）。同时具备独立入口与库用途的文件 MUST 判为适用；「它也被 import / 也被 source」MUST NOT 作为豁免依据。

- **FR-010**: 一个确定性的仓库检查 MUST 消费 FR-002 的判定，对每个候选输出四项结论（是否适用、help 是否可用、version 是否可用、未知选项是否被拒绝）与违规计数；其退出码 MUST 区分「全部合规」与「存在违规」，违规 MUST 点名脚本与缺失项。

- **FR-011**: 契约 MUST 追加落地到 `templates/constitution-template.md`，作为新的一条原则；该原则 MUST 以「指向 owner 文档的指针 + 不可让渡的规则要点」形态书写，MUST NOT 复制 owner 文档的正文。

- **FR-012**: 契约 MUST 落地到 `templates/instructions-template.md`，作为一条常驻顶级段落，形态为摘要 + 指针（与既有常驻段落一致）；本仓 `.specify/instructions.md` MUST 同构落地同一段落。

- **FR-013**: 契约 MUST 落地到本仓 `.specify/memory/constitution.md`，作为新增的一条原则并按本仓编号顺延；该修订 MUST 产出 Sync Impact Report、按 `x.y.z` 递增版本号（新增原则 = MINOR）、更新「Last Amended」日期。

- **FR-014**: `skills/internal/manage-constitution/SKILL.md` 的 `MUST include` 清单 MUST 新增该原则条目，使下游项目用生成器修订宪法时该原则成为必须存在项。

- **FR-015**: 规则 MUST 只有一个 owner 文档，承载可判定的判据、必备内容、豁免判据与检查入口；上述四处落点 MUST 以路径引用它，MUST NOT 各自复写判据文本。

- **FR-016**: 五处落点 MUST 彼此一致：宪法模板与本仓宪法的原则标题一致；生成器 MUST-include 清单与两侧宪法的关系是**集合包含 + pin 同步**——清单 MUST 含 `DOUBLE_LANDING_WATCHLIST` 所列的每个原则标题（标题集合包含，**不是**条目计数相等：清单现有 11 条对两侧宪法 18 / 19 条原则，计数按设计就不相等）；同时双落地守卫的三条计数 pin（template / live / mandate）与 watchlist MUST 在同一提交内从 18 / 19 / 11 / 6 同步移到 19 / 20 / 12 / 7；指令侧段落指向同一 owner。一致性 MUST 由既有双落地守卫的计数 pin 与 watchlist 断言覆盖，MUST NOT 依赖人工比对，且 MUST NOT 被读成「清单条目数 == 宪法原则数」。

- **FR-017**: 本仓现有适用脚本 MUST 全部补齐到契约（FR-003 … FR-008），补齐范围 MUST 覆盖 `scripts/bash/*.sh`、`scripts/python/*.py`、`skills/**/scripts/` 下具备独立入口的脚本；补齐后 FR-010 的违规计数 MUST 为 0，豁免清单 MUST 逐条带判据证据。补**哪一侧**由 FR-027 的两顶帽子规则决定。

- **FR-018**: 补齐现存脚本时 MUST 保持其既有接口语义不变：已声明的选项、输出格式（含 JSON 模式）、退出码语义与副作用 MUST 逐字不变；MUST NOT 借补齐之机改名、改默认值或增加新的行为分支。

- **FR-019**: 契约 MUST 对范例中的事故脚本成立：`scripts/bash/generate-instructions.sh` 的 `--help` MUST 输出用法且不触发其 reconcile 主动作，未知选项 MUST 被拒绝；该脚本是实现本契约时的首个验收对象。

- **FR-020**: 随技能分发的第三方/上游脚本 MUST 遵守同一契约，但 MUST NOT 被就地改写其上游实现。**处置顺序是唯一且强制的**：**(a)** 第三方脚本 MUST 先走**最小入口层**——在文件入口处加一段入口守卫块（FR-029 的「bash 可实施形态」，python 侧为解析 argv 前的显式 `print` + `sys.exit(0)`），版本号由该入口层自身打印（A4 形态），不改动上游函数体与参数结构；**(b)** 只有无法在不改上游结构的前提下实现契约时（入口层无法插入，或入口层与上游自身的参数解析互斥），该脚本才 MAY 登记为 `## Declared Exceptions` 的一行；该行 MUST 同时点名**路径**、**技能名**、**未满足的条款号**与**处置**（保留在入口层 / 停止分发该脚本 / 待上游修复），缺任一列即复算不成立、检查报错；**(c)** 登记的事实 MUST 在 FR-010 的输出中可见，MUST NOT 静默排除。「第三方来源」的机械判据见 FR-027；登记载体与列形态见 § Clarifications Q6 与 § Key Entities「已声明例外」。

- **FR-021**: FR-010 的检查 MUST 接入既有的验证面（既有测试集合与契约测试），MUST NOT 新增独立的确认门或独立的门禁步骤；一次提交若引入违规脚本，既有面 MUST 报红。落点与命名 MUST 按 FR-031 的接线面裁定执行。

- **FR-022**: 镜像与派生副本 MUST 与框架源同步：`.specify/scripts/`、`.specify/templates/`、`.specify/skills/` 的对应文件由既有镜像机制重新投影，MUST NOT 手改镜像；同步后既有镜像检查 MUST 报零漂移。

- **FR-023**: 规则文本 MUST 与其自身的适用范围一致：框架自身脚本、下游项目脚本与第三方脚本都在范围内；规则 MUST NOT 以「仅适用于本仓库」的措辞写就。

#### 承重定义条款（2026-11-06 clarify 裁定）

以下条款把 § Clarifications 中的七条裁定落成约束。它们不新增用户故事，全部挂在既有 US5 / US6 / US7 之下。

- **FR-024**: （候选面边界，承 FR-002）：候选面 MUST 由两条互相校验的规则派生，MUST NOT 由手写目录名单派生。**(a) 派生**：候选集 = 版本控制枚举出的全部 `*.sh` / `*.py` 减去 `.gitignore` 判为忽略者。该规则由这两个机器可读来源自动容纳 `__pycache__/`、`node_modules/`、`.venv/` 等被忽略的 vendored 与生成目录，因而不需要点名它们，也不会随目录增删而失效。**(b) 覆盖断言**：检查 MUST 遍历工作树全部 `*.sh` / `*.py`；任一文件不在候选集中、也不在 `.gitignore` 忽略集中时，检查 MUST 以非零退出码报错并点名该文件（判为「遗漏的候选」），MUST NOT 静默略过。**(c) 静默排除禁止**：`tests/`、`scripts/`、`skills/**/scripts/`、`.specify/scripts/`、`src/` MUST NOT 被任何目录级排除跳过——它们各自按 FR-025 / FR-026 逐文件判定；排除只允许来自 `.gitignore`（文件被忽略）或 FR-027（第三方来源），两者都必须以点名或规则可复算的形式出现在检查输出中。**(d) 交付物覆盖面**：`.specify/` 下的镜像副本 MUST NOT 因此被漏判——它们是运行时可执行的，MUST 至少接受 FR-030 的「已投射源副本一致」验证。

- **FR-025**: （bash 独立入口判据）：一个 `.sh` 文件 MUST 判为「具备独立执行入口」，当且仅当它按脚本方式运行（`bash <file>`，而不是被 `source`）时，**入口守卫块之后的代码会被执行**。「入口守卫块」指脚本在产生任何写型副作用之前必须出现的那一段参数判定（FR-029），其存在与否 MUST NOT 影响本判定。以下三项 MUST NOT 作为判据：顶层是否存在 `exit` / 执行语句、文件头声明的是 `bash` 还是 `sh`、作者在文件里怎么自我描述。可判定定义：对脚本施加一次变异——把守卫块之后的第一个写型副作用替换为一条「已执行」标记——然后按脚本方式运行并带一个**已声明**的选项；标记出现即判适用，不出现即判豁免。被 `source` 的纯库（其顶层代码只在 source 时求值）因此落在豁免侧，而其顶层写了依赖检查这一事实不改变判定。

- **FR-026**: （python 独立入口判据）：一个 `.py` 文件 MUST 判为「具备独立执行入口」，当且仅当它拥有一个执行后必然产生副作用的入口载体：一个带 `__main__` 守卫的块（`if __name__ == "__main__":`），或该文件的 `main()` 可经稳定的命令行约定抵达且退出码非零**不**来自「参数解析失败」。判据 MUST NOT 只看「有没有 `__main__` 块」——带 `__main__` 块而被 import 的模块并不执行该块，据此会误判为适用；判断必须落在「作为脚本运行时会不会真的做事」上。只被 import 的模块、以及剥离 `__main__` 块后什么都不发生的模块 MUST 判为豁免。变异实验须覆盖两个方向（加 `__main__` 块 → 移入适用集；删 `__main__` 块 → 移回豁免集），见 US6 独立测试。

- **FR-027**: （第三方来源判据与两顶帽子）：一个候选 MUST 判为「第三方/上游脚本」，当且仅当它满足两条**同时成立**的机械条件：**其一**，它位于该技能的分发源之下（`skills/external/<name>/`，而非 `.specify/skills/` 镜像）；**其二**，该技能的 `SKILL.md` 声明 `classification: external`——**这是第三方来源的唯一机器标记**，MUST NOT 用「目录内存在上游许可/来源文件」等第二个分支替代或补充（那会让同一事实有两个定义点，且二者不同步时判据自相矛盾）。对**本仓**而言——`.specify/` 是本仓运行时、`skills/` 是框架源——凡 `SKILL.md` 声明 `classification: internal` 的技能（无论它落在 `skills/internal/` 还是 `skills/external/` 目录下）**MUST 判为框架源**，走 FR-017 就地补齐，MUST NOT 走已声明例外。该判定理由 MUST 写进 owner 文档的第三方章节，MUST NOT 留给读者推断。

- **FR-028**: （墓碑，不承载任何约束）：此编号曾拟用于「第三方来源判据」，该内容在 2026-11-06 clarify 阶段并入 FR-027，编号留空且 MUST NOT 被复用。本行 MUST 只作说明出现在此处；除覆盖统计所需的一次墓碑登记引用外，MUST NOT 在正文其他位置被当作有效条款引用——登记引用 MUST 原文点名它是墓碑、不承载约束。

- **FR-029**: （零副作用取证与标志判定前置）：**取证**：对每个适用脚本，在受测仓库的一个**副本树**上执行 `-h`、`--help`、`--version` 与一次未知选项调用，前后各做一次取证快照，断言两快照逐字节相同：快照 = `git status --porcelain` 输出 + 受测树内全部 `*.sh` / `*.py` 的 `sha256` + `.specify/` 下的文件清单与其哈希。副本树在受测仓库之外，故受测仓库自身的 `.specify/.tmp/` 与 `$TMPDIR` 下的运行时临时文件不计入断言；MUST NOT 在受测仓库内直接执行这些调用，否则一次可回滚的写入会被掩盖或误报。**前置**：标志判定 MUST 出现在脚本内**所有**写型副作用之前（含镜像 refresh、日志目录创建、工具 manifest 生成），并在任何可能要求用户确认的检查之前。**bash 的可实施形态（唯一）**：在 source 共享库之前设一个扫描 `"$@"` 并把内部 `--` 当终止符的守卫块，命中 `-h` / `--help` / `--version` 即输出并 `exit 0`，命中未声明的 `-*` 即报告并以非零码退出；MUST NOT 用 getopts（其遇 `--` 即停，且不拒未知长选项却不消费参数），MUST NOT 放在 source 之后（共享库自身有顶层依赖检查，会把 `--help` 变成一次退出 1）。**python 的可实施形态**：`--version` MUST 在**每条子命令上**可解析（顶层 `action="version"` 在带必填 subparsers 的命令上于「首选项即 `--version`」位置以退出码 2 被拒），或在解析 argv 之前以显式 `print` + `sys.exit(0)` 实现。

- **FR-030**: （镜像副本一致性）：镜像副本 MUST 按投射状态分两类判定，两类条件不同、MUST NOT 合并为一条：**(a) 未被投射的镜像** MUST 与分发源**逐字节相同**（检查 `SOURCE ≡ MIRROR`）；**(b) 被投射的镜像** MUST 等于 **`source + declared projection`**——投射集合只在一处声明（`sync-mirrors.py` 的那张投射表），由 `--check-projection` 断言（幂等、锚点缺失即退出 1 并点名该对，MUST NOT 在文件尾部静默追加）。下游项目侧无法校验（`SOURCE` 不存在），此时该下游项目的镜像侧 MUST 自足合规——它的 `.specify/scripts/` 副本自身满足 FR-003 … FR-008。

- **FR-031**: （检查落点与命名，承 FR-010 / FR-021）：契约检查 MUST 是一个**新增的**标准库单文件引擎 `scripts/python/script-interface-check.py`（与 `scan-confirmation-gates.py` / `gate_check.py` 同类同目录同形态：`argparse`、只读、退出码 0 = 全部合规 / 1 = 存在违规 / 2 = 参数或环境错误、stdout 人读 + `--json` 机器读），其镜像由既有镜像机制生成；引擎 MUST NOT 挂在任何既有脚本里，以免把无关脚本变成契约的一部分。它 MUST 由**新增的**契约测试 `tests/contract/test_script_interface_contract.py`（`pytestmark = pytest.mark.contract`）消费——这是 FR-021「接入既有验证面」的具体形态：既有面是 pytest 契约测试集合，不是某一条既有测试文件。该测试 MUST 至少含一次变异断言：从副本树里删掉一个已合规脚本的 help 分支，断言检查报红并点名该脚本（SC-008）。driver 阶段门禁 MUST **不**接线（opt-in 决策留待计划阶段，见 US7 与 § Out of Scope）。

### Key Entities *(include if data involved)*

- **脚本接口契约（Script Interface Contract）**：一条治理规则，拥有者是唯一的 owner 文档；它拥有五件东西：判定对象（适用集 / 豁免集）、必备标志及其必备内容、零副作用边界、未知选项的拒绝要求、豁免判据。四处落点都是它的投影，不是第二定义点。

- **适用集 / 豁免集**：由机械候选屏对仓库内全部 `*.sh` / `*.py` 计算的互斥划分；每个成员带一条判据证据（独立入口在哪里 / 为什么没有）。豁免集不是白名单，而是判据的结果。

- **已声明例外（Declared Exception）**：无法在不改上游结构的前提下实现契约（FR-020(a) 的最小入口层不成立）的第三方脚本；带脚本路径、技能名、未满足的具体条款与处置。它必须在检查输出中可见。**登记载体（clarify 裁定）**：本仓唯一的例外记录是 owner 文档 `shared/definitions/script-interface-definitions.md` 的 `## Declared Exceptions` 章节（四列表格 `path` / `skill` / `unsatisfied clause` / `handling`，空表合法且只写字面 `none`）；下游项目把同一章节放在其 `.specify/shared/definitions/` 的同名文件里。**维护者**：人与 `/speckit.implement` 都能改——宪法侧条款是「意图」，该章节是「据以放行的凭据」，后者由提交引入该例外的计划/任务所属特性维护。**读取者**：唯一读者是检查器 `scripts/python/script-interface-check.py`；它 MUST 逐条复算该章节里每一行的机器判据（路径存在？位于 `skills/external/<name>/`？该技能 `SKILL.md` 声明 `classification: external`？四列齐备？），复算不成立即报 `exception-unverifiable` 并以退出码 1 结束（不是默认放行，也不是默认排除）；`classification: external` 是第三方来源的**唯一**机器标记（FR-027），MUST NOT 增设备用分支；对**不在**该章节里的第三方候选，它 MUST 按普通候选判红，MUST NOT 自动豁免。

- **契约检查（Contract Check）**：消费划分结果、输出逐脚本四项结论与违规计数的确定性程序；它是契约被判定的唯一入口。

- **常驻段落（Ambient Section）**：`instructions-template.md` 中的摘要 + 指针段落；它携带「读者在入口处需要知道的那一句话」并把正文交还 owner 文档。

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | POSIX shell + `bash` 4+ 的参数解析与退出码语义（被 bash 侧修复脚本依赖） | signed-contract | 宿主操作系统提供的 shell 运行时 | 以 CI 与开发机实跑的 `bash --version` 为准（实施阶段测量） | `docs/concepts/security.md` | `bash --version` + 一次 bash 脚本 help 实跑 | FR-003, FR-004, FR-006, FR-017 | EP-002 |
| RS-002 | Python 3 解释器与标准库 `argparse`（被 python 侧修复脚本与检查器依赖） | signed-contract | 宿主 Python 发行版 | `pyproject.toml` 声明 `>=3.8` | `pyproject.toml` | `python3 --version` + 一次检查器实跑 | FR-004, FR-010, FR-017 | EP-003 |
| RS-003 | 机械候选屏与逐脚本判定（本特性交付的检查能力） | in-scope | 本特性 | — | — | FR-010 检查的实跑结果 | FR-002, FR-009, FR-010 | EP-001 |
| RS-004 | 单文件镜像投影机制（`.specify/` 与源一一对应） | in-scope | 本特性复用并扩展其判定面 | — | — | `sync-mirrors.py` 检查实跑 | FR-022 | EP-004 |
| RS-005 | 宪法与指令模板的双落地守卫（计数 pin + watchlist） | in-scope | 本特性维护其 pin | — | — | 双落地守卫与 fast-fail 计数一致性测试实跑 | FR-011, FR-012, FR-013, FR-014, FR-016 | EP-005 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在干净工作树上对适用集中每个脚本执行 `-h`、`--help` 与 `--version`，100% 返回成功码且输出非空；执行前后工作树 `git status --porcelain` 输出恒为空、受管目录文件指纹零差异。**Path**: final

- **SC-002**: 范例脚本 `scripts/bash/generate-instructions.sh` 执行 `--help` 时，对 `.specify/instructions.md` 的字节改动为 0（对比执行前后的文件哈希），且不产生任何备份文件；同一脚本执行未知选项时退出码非零。**Path**: final

- **SC-003**: 契约检查对仓库内全部 `*.sh` / `*.py` 候选给出判定，违规计数为 0，且豁免集中的每个成员都带一条可机械复核的判据证据；无成员处于「未判定」状态。**Path**: final

- **SC-004**: 一个用框架初始化的干净下游项目，其生成的宪法含该原则、生成的 `instructions.md` 含对应常驻段落；两者均由生成流程产出而非手工补写。**Path**: final

- **SC-005**: 在一次宪法修订中，版本号产生 MINOR 增量、Sync Impact Report 存在、Last Amended 日期更新；三者在同一提交中同时可见。**Path**: supporting

- **SC-006**: 五处落点的一致性由既有守卫判定，拆成两条可判定断言，任一失败即判红：**(a) pin 同步**——双落地守卫的三条计数 pin 与 watchlist 在同一提交内按 18→19（template 原则数）、19→20（live 原则数）、11→12（生成器 MUST-include 条目数）、6→7（watchlist 条目数）同步移动；**(b) 集合包含**——生成器清单 MUST **包含** watchlist 所列的每一个原则标题（按标题做集合包含判定，MUST NOT 用条目计数相等判定：清单 12 条对宪法 19 / 20 条原则，计数按设计就不相等）。**Path**: final

- **SC-007**: 补齐现存脚本的提交中，已声明选项、JSON 输出形态与退出码语义零回归：补齐前后对同一组既有调用的输出差异为 0（仅新增标志路径允许出现新输出）。**Path**: supporting

- **SC-008**: 对任一适用脚本删掉其 `--help` 处理的副本树变异，契约检查报红并点名该脚本；红线在 100% 的抽样变异上触发，无误绿。**Path**: final

- **SC-009**: 候选面的完整性可被机械证伪：在候选集之外人为放置一个 `*.sh`（未被 `.gitignore` 覆盖），检查 MUST 报错并点名它；把它加入 `.gitignore` 后同一检查 MUST 转绿且不点名。**Path**: final

- **SC-010**: 豁免判定在两侧各可被一次变异推翻：给一个豁免 bash 库补上守卫块 + 守卫后的写型主动作后，它 MUST 从豁免集移入适用集；在一个被 import 的 python 模块上删掉其 `__main__` 块后，它 MUST 停留在豁免集（判定不因字面块存在而变化），而给它补一个真正执行动作的 `__main__` 块后 MUST 移入适用集。**Path**: final

- **SC-011**: `--version` 的单一来源可被一次发版证明：仅修改 `pyproject.toml` 的 `version` 字段后重跑全部适用脚本的 `--version`，100% 的输出行随之改变且仍为 `<script-name> <version>` 单行；仓库内 `grep` 字面版本号在脚本中的命中数为 0。**Path**: final

- **SC-012**: 已声明例外不可被伪造、也不可被误登记：**(a)** 在 owner 文档 `## Declared Exceptions` 下写入一条路径不存在、或技能未声明 `classification: external` 的条目后，检查 MUST 报错；**(b)** 在副本树上**注入**一条看似合法但复算不成立的例外行（路径位于 `skills/external/<name>/` 且存在，但该技能 `SKILL.md` **不**声明 `classification: external`），检查 MUST 报 `exception-unverifiable` 并以退出码 1 结束——该断言不依赖「登记表里恰好存在一条真实例外行」；**(c)** 登记表合法为空时，`## Declared Exceptions` MUST 只写字面 `none` 且检查 MUST 判绿（退出码 0）。**Path**: final

### Measurement Sources & Collection Methods

- **SC-001 Source**: 契约检查的 `--probe` 式实跑输出（逐脚本退出码与输出摘要）+ 执行前后 `git status --porcelain` 与 `find .specify -newer` 指纹快照；证据落盘到 `test-evidence/`。每次提交前与 closure 各测一次。
- **SC-002 Source**: 对目标文件执行 `sha256sum` 前后对比，并在执行后 `git status --porcelain .specify/instructions.md` 判空；`ls` 检查备份文件缺失。一次性采集，落盘 `test-evidence/`。
- **SC-003 Source**: 契约检查的 `--json` 汇总输出（candidates / applicable / violations / exemptions），豁免清单逐条带判据证据；镜像一致性取两条独立读数——未投射镜像由既有 `sync-mirrors.py --check` 的逐字节相等断言（零漂移），被投射镜像由同一引擎 `--check-projection` 的 `source + declared projection` 断言（含幂等性与锚点缺失的报红），两者分开记录。closure 时采集。
- **SC-004 Source**: 在干净临时目录执行框架初始化与宪法生成，检查生成物中的原则标题与常驻段落标题；证据为生成文件片段与命令输出。
- **SC-005 Source**: 修订提交中的宪法 diff（版本行、Sync Impact Report、Last Amended）三处同现；由 `git show --stat` 与文件片段取证。
- **SC-006 Source**: 双落地守卫与计数一致性测试的实跑输出（退出码与计数读数），读数须同时给出四个 pin 值（template / live / mandate / watchlist）与一次 watchlist 标题对生成器清单的集合包含判定结果，二者分开记录，MUST NOT 合并成一句「计数一致」。
- **SC-007 Source**: 补齐前后对既有调用集合（取每个脚本当前已声明的选项组合）的输出捕获对比，差异清单为空。
- **SC-008 Source**: 副本树变异脚本（在临时目录复制、删除 help 分支、运行检查）的输出；抽样覆盖全部适用脚本——本阶段实测该集合规模可控，故取全量而非分层抽样。
- **SC-009 Source**: 在一个副本树里 `touch` 一个 `probe.sh` 并运行检查（记录退出码与点名行），随后把它写进该副本树的 `.gitignore` 再运行一次；两段输出落盘 `test-evidence/`。
- **SC-010 Source**: 三次副本树变异（bash 补主动作、python 删 `__main__` 块、python 补真正动作）前后的检查 `--json` 输出对比，看该文件的 `applicable` 布尔值翻转。
- **SC-011 Source**: 在副本树里改 `pyproject.toml` 的版本字面量，重跑全部 `--version` 并与改前逐行 diff；另有 `grep -rn` 证明脚本中零字面版本号。
- **SC-012 Source**: 三次对副本树 `## Declared Exceptions` 的变异——(a) 伪造一条路径不存在的条目、(b) 注入一条路径存在但技能未声明 `classification: external` 的条目、(c) 留空（只写 `none`）——每次读检查的退出码与 `--json` 的 `findings[]` / `exceptions[]` 段；其中 (b) 断言 `findings[]` 含 `exception-unverifiable`，(c) 断言退出码 0。真实登记表是否为空不影响该取证。

## Boundary and Ownership (non-duplication)

- **本特性拥有**：脚本入口契约的判据、必备内容、豁免判据、已声明例外的形态，以及契约检查的判定入口。
- **本特性引用而不拥有**：One Source of Truth（指针纪律）、Grounded Naming（命名来源）、Directory Governance（目录登记）、Fast Fail（异常上送）、Confirmation Gates（确认门分类）、Single-Run Evidence（证据捕获）、Self-Explanatory Structure（入口信息可达性）。上述纪律的判据全部由其 owner 文档拥有，本特性只按路径引用。
- **本特性不拥有**：脚本内部实现规范、代码风格、测试框架选择、命令（`/speckit.*`）的行为契约、镜像机制本身的实现、宪法版本号的通用规则（由 `manage-constitution` 拥有）。
- **与既有落点的边界**：宪法与指令模板的「双落地」判据由 Feature 051 / 082 的守卫拥有；本特性只维护其计数 pin 与 watchlist 条目，不改判据。

## Assumptions

- **A1 — 类别判定的 oracle 与理由**：本特性判为 `execution`（`Flow Type: -`）。验收 oracle 是「交付物被机器执行/解析/消费」：契约检查是被机器跑出 verdict 的程序，五处落点是机器可解析的模板与清单，SC 以程序读数判定。即便其中一部分交付物是文档段落，缺陷也只在程序判定失效时暴露，因此不判为 `expression`。
- **A2 — 事故前提复核（事实层）**：用户所述事故以既有记录为依据。本阶段对仓库现状做了实测，读数记在下方 A2 的测量清单里；其中「本次事故未被 git 记录」这一条是**实测结论**，用于说明为何本规格把 SC-002 写成「自指的可复现实验」而不是「与事故当次 diff 比对」。
- **A3 — 规则的唯一 owner 文档形态（clarify 已裁定，不再是开放项）**：契约的正文落在 `shared/definitions/script-interface-definitions.md`（本仓运行时投影为 `.specify/shared/definitions/script-interface-definitions.md`）。选择 `definitions/` 而非 `guidelines/` 的理由是命名惯例：`definitions/` 拥有「契约的机器可判定条目」（`contract-clause-definitions.md`、`flow-class-definitions.md`、`probe-definitions.md`、`sdd-routing-definitions.md` 均是判据 + 取值域的形态），`guidelines/` 拥有「纪律与实践方法」（`fast-fail.md`、`one-source-of-truth.md` 等）。本契约的主体是可被程序复算的判据表，故归 `definitions/`。文件顶部 MUST 声明它所拥有的条目（对应 § Key Entities 的五件东西）。宪法与指令模板只放摘要 + 指针。

- **A4 — 版本标识的粒度（clarify 已裁定，只保留一种形态）**：`--version` 输出 **`<script-name> <framework-version>`** 一行（例：`sync-mirrors.py 0.0.22`）。`<framework-version>` MUST 从 `pyproject.toml` 的 `version` 字段**运行时动态读取**，MUST NOT 把字面版本写进任何脚本——后者是第二定义点，会在下一次发版时静默漂移。读取失败（`pyproject.toml` 不可达，例如下游项目）时 MUST 输出 `<script-name> unknown` 并**以成功码退出（exit 0）**：版本查询本身不该成为一条能挂住用户的路径，也因此 MUST NOT 改变退出码。「不可解析」这一状态由执行者从输出行观察（检查器在 `candidates[].version` 字段给出同一读数的投影），不改变退出码。MUST NOT 引入每脚本 `version` 文件或第二套版本系统（与 § Out of Scope 一致）。

- **A5 — 现存脚本的补齐范围以实测为准**：本阶段实测基线见下表。规格中的计数是**基线参照物**，不是验收阈值；验收阈值是「违规计数为 0」（SC-003），计数本身由检查在 plan / tasks / implement 阶段重算。

- **A6 — 第三方脚本的处置（clarify 已裁定，plan 阶段实测更正）**：第三方判定 MUST 用 FR-027 的两条件机械判据，MUST NOT 按目录名或作者描述判定。本仓实测（2026-11-06）：`skills/external/create-skills/` 与 `skills/external/coaching-skills/` 的 `SKILL.md` 均声明 `classification: external`（初稿误记为 `internal`，以实测为准），故按 FR-027 判为第三方来源；实测两者名下没有 `*.sh` / `*.py` 脚本，本特性无需修改它们，若将来出现脚本则走 FR-020 的最小入口层或已声明例外。其余 `skills/external/<name>/` 技能按 FR-027 判为第三方，以 § Clarifications Q6 的登记形态出现。不允许用目录级排除静默绕过。

- **A7 — 检查的接线面（clarify 已裁定）**：契约检查落在 FR-031 指定的新增标准库引擎 + 新增 pytest 契约测试两个新文件上。它们虽是**新文件**，但接入的仍是既有面（`pytest -m contract` 与既有 `scripts/python/` 引擎目录约定），故不违反 FR-021 的「不新增门禁步骤」；**不**接 driver 阶段门禁。

- **A8 — 帮助文本的语言**：帮助文本以英文为主（与被检查脚本一致），不要求双语；双语表述纪律只约束定义处的核心概念，本契约的原则名与 owner 文档走该纪律。

- **A9 — 不追溯改写历史记录**：`test-evidence/`、`.specify/state/`、dated review 与既有 spec 的 `requirements.md` 是输入而非编辑对象；本特性不改写它们。

- **A10 — 本条澄清使用的实测基线（clarify 阶段）**：候选面 737 个文件（`.sh` 71 + `.py` 666），与版本控制枚举数逐字相同，说明本仓「版本控制枚举」与「工作树全量」在当前离线状态下重合。目录分布：`tests/` 449、`.specify/` 146、`skills/` 87、`scripts/` 51、`src/` 3、`install.sh` 1。python 侧带 `__main__` 块 207 个、无 `__main__` 块 459 个。`.specify/` 下 73 个 `.sh` / `.py` 没有对应的 `skills/` 或 `scripts/` 源（镜像机制只投射 `scripts/`、`skills/external/<name>/`、`skills/internal/<name>/`、`shared/`、`templates/`；`.specify/skills/document-utils/` 等 skill 在源树中的名字不同，故不是漏同步），这直接支持 FR-024(d) 与 § Clarifications Q1 的「不按路径去重」。**本特性同时更正 requirements 阶段的两条错误读数**，见 § Clarifications Q8 与 Q8 附注。**analyze 回环 1 计数更正（唯一一条）**：`scripts/python/` 的脚本数初稿记为 **38**，本轮实测为 **37**（`ls scripts/python/*.py | wc -l`），已同步更正 A2 的测量清单；本段其余读数（含「带 `__main__` 块的 `.py` **207** 个」）经本轮复测保持不变，MUST NOT 被当作待改项。

**A2 的实测基线（2026-11-06，本阶段在仓库根实跑，命令与读数如下）**:

- `ls scripts/bash/*.sh` → **14** 个文件；其中无 `--help` 处理的 **6** 个：`collect-history.sh`、`common-todo.sh`、`common.sh`、`detect-feature-context.sh`、`generate-instructions.sh`、`run-tests.sh`；`refresh-tools.sh` **有** `usage()` 与 `--help` 分支（任务简报里把它列为「无 help」与实测不符，以实测为准）。
- 14 个 bash 脚本中带 `--version` 的仅 **1** 个：`run-tests.sh`；带未知选项拒绝的仅 **1** 个：`check-prerequisites.sh`（其余把未知 token 归入位置参数或忽略）。
- `ls scripts/python/*.py` → **37** 个文件（analyze 回环 1 实测更正：初稿记的 38 为误读，以 `ls scripts/python/*.py | wc -l` 的 37 为准）；全部具备 `if __name__ == "__main__"` 块；**35** 个使用 `argparse`，**2** 个自行解析（`clause_extract.py`、`gate-check.py`）。`clause_extract.py` 给 `--help` 只返回 usage 与退出码 2，`--version` 不可用；`gate-check.py` 无 `argparse`。
- 37 个 python 文件中带自身 `--version` 的为 **0** 个（见下方「更正 1」：`evidence-utils.py`、`exec-quant.py` 里的 `--version` 是探测别的程序）；即其余 **37** 个全部不支持。**计数更正（analyze 回环 1）**：本行与上一行的 `scripts/python/` 文件数由初稿的 **38** 更正为实测 **37**（同时 `argparse` 计数 36 → 35）；本仓 **207** 个带 `__main__` 块的 `.py` 读数经本轮复测仍为 207，保持不变。
- 实测样例：`python3 scripts/python/sync-mirrors.py --version` → `error: unrecognized arguments: --version`（argparse 的未知选项拒绝生效，但 `--version` 未实现）；`python3 scripts/python/flow-class-check.py --help` → 正常输出用法（help 可用，version 不可用）。
- `find . -name '*.sh'`（排除 `.git`）→ **71** 个；`find . -name '*.py'` → **666** 个（含 `tests/` 与虚拟环境外的全部 python 文件）。这解释了为什么判定对象必须由机械候选屏产生而不是手写清单：候选面比「脚本目录」大两个数量级，手写清单必然遗漏。
- `skills/**/scripts/` 下 **16** 个 `.sh`：**6** 个带 `--help`、**1** 个带 `--version`。
- `git log --oneline -- .specify/instructions.md` → 最近一次改动是 `02fd6db5`（Feature 082 的 reconcile），**不存在**与本次事故对应的「+70 行 / 0 删除」提交；故事故未进入版本历史，SC-002 以可复现实验取证。
- 保留阅读：`scripts/bash/generate-instructions.sh` 共 391 行，**无参数解析**，开头即 source `common.sh`、解析模板路径，随后进入 reconcile 分支（`INJECTED_SECTIONS` / `STRIPPED_SECTIONS` 输出即为追加证据）——与该事故的机制描述一致。

**A2 的两条读数在 clarify 阶段被实测更正（2026-11-06）**：

- **更正 1**：`scripts/python/` 下带 `--version` 的不是 **2** 个，是 **0** 个。`evidence-utils.py` 与 `exec-quant.py` 里的 `--version` 都是它们**探测别的程序**（`node --version`、`<binary> --version`）的 `subprocess` 参数，不是自身接口。误读的成因是「grep 到 `--version` 就认为实现了」——正是本特性要治的同一种病在取证环节的复现。全仓 `add_argument(..., action="version")` 命中数 = **0**。
- **更正 2**：`scripts/bash/refresh-tools.sh` 的应用是「**有** `usage()` 函数（第 53 行）且在 `*)` 分支调用 `usage`，但 CLI **没有** `--help|-h` 分支」——它`--help` 落入未知选项分支被拒，即行为已接近合规、缺的是显式 `--help` 与 `--version`。同理，`run-tests.sh` 里唯一的 `--version` 是 `"$candidate" -m pytest --version`，仍是探测 pytest 而非自身版本。
- **加强事实（支持 Q3 裁定）**：`scripts/python/declaration_reader.py` 带 `__main__` 块**却**只被 import（`validate-requirements.py` 由它读出定义行）；它既是纯库、又落在「有 `__main__` 块即适用」这一字面判据的**适用侧**——两个方向都说明字面判据不足以裁决，必须按 FR-026 追问「作为脚本运行时是否真的做事」。`scripts/bash/check-prerequisites.sh` 同时具备 `--help` 分支与未知选项拒绝分支，说明两者在本仓既有脚本中不互斥。

## Out of Scope

- 给纯库文件（`common.sh`、`declaration_reader.py` 等）加 `--help` / `--version`。
- 脚本内部实现的重构、统一的参数解析框架或 CLI 库替换（例如强制所有 bash 脚本改用某个 parser）。
- `src/specify_cli/` 的 Typer CLI 本身（它已具备 `--help`；`--version` 的形态归 CLI 自己的规范）。
- 为 `--version` 引入独立的版本管理系统或每脚本 `version` 文件。
- 修改确认门分类、SDD 阶段数、命令清单，或新增 `/speckit.*` 命令。
- 对既有 spec、dated review、`test-evidence/` 与 `.specify/state/` 的追溯改写。
- 把契约检查做成默认开启的 driver 阶段越界门禁（留给 plan 阶段裁定，且默认不改变既有 finding 名集合的前提由 plan 验证）。

## Clarifications

<!-- 由 /speckit.clarify 填充：- Q: <question> → A: <answer> -->

### Session 2026-11-06

本会话模式 **A（post-requirements）**，目标文件 `requirements.md`。无人值守运行：九条问题全部由本代理自行裁定，裁定依据是仓库实测 + 既有纪律，不向用户提问。每条裁定都同步落进正文（见行尾的落点）。

- Q: 候选面的根目录集合怎么定——手写目录名单，还是按 `git ls-files '*.sh' '*.py'`，还是全工作树？`tests/`、`scripts/`、`skills/**/scripts/`、`.specify/scripts/`、`src/` 与 vendored 目录分别如何处置？ → A: **裁定：版本控制枚举 —— 候选面 = `git ls-files '*.sh' '*.py'` 减去 `.gitignore` 忽略者，另加一条覆盖断言防静默漏检。** 具体：`tests/`、`scripts/`、`skills/**/scripts/`、`.specify/scripts/`、`src/`、`install.sh` **全部在候选面内逐文件判定**，不做任何目录级豁免；vendored / 生成目录不点名，由 `.gitignore` 自动容纳（`__pycache__/`、`.venv/`、`node_modules/` 已在 `.gitignore` 中，`git check-ignore` 实测生效）；`.specify/` 下的镜像副本与源**各自**是候选，不按路径去重（实测有 73 个镜像文件没有同名源）。理由与机械形式见 FR-024。**Why**：手写目录名单会在下一次新增目录时静默漏检，而「漏检」在本特性里正是缺陷本身（FR-002）；两个机器可读来源（版本控制 + `.gitignore`）让候选面随仓库自更新，再配一条「工作树里不在候选集也不在忽略集的文件即报错」的断言，漏检就从「静默」变成「报红」。**落点**：FR-002、FR-024、SC-009、Edge Cases「生成物与镜像」、A10。

- Q: bash 的独立入口判据用什么？既然 `scripts/bash/common.sh` 顶层就有 `if ! check_dependency; then … exit 1; fi`，按「存在顶层执行语句」会把它误判为适用——判据需要怎样的形态才能同时解释「库文件有顶层依赖检查仍应豁免」与「真可执行脚本必须适用」？ → A: **裁定：判据问「按脚本方式运行时守卫块之后的代码会不会执行」，不问「源码里有没有顶层语句」。** 纯 `source` 库的顶层代码只在被 source 时求值，直接 `bash common.sh` 时它自己的依赖检查只是执行一次然后结束——它没有任何「主动作」，故判豁免。可判定的取证是变异实验：把守卫块之后的第一个写型副作用替换成一条「已执行」标记，带一个**已声明**的选项按脚本方式运行，标记出现即适用。以下三项 MUST NOT 作判据：顶层是否有 `exit`/执行语句、shebang 是 `bash` 还是 `sh`、作者自述。见 FR-025。**Why**：`common.sh` 的顶层检查是**依赖报错**而非**主动作**，字面判据把两者混为一谈；把判据从「源码形态」移到「运行语义」后，同一问题在两侧都有了同一个答案（python 侧见下一题）。实测证据：`env -u CWS_LIB_BASH_HOME bash scripts/bash/common.sh` → 退出 1 并打印依赖错误，无任何主动作；`bash -c 'source scripts/bash/common.sh'` 才是它的用法。**落点**：FR-009、FR-025、SC-010。

- Q: python 侧 `if __name__ == "__main__"` 是不是唯一判据？`tests/` 下的测试模块、`conftest.py`、`scripts/` 下仅被 import 的模块如何判？ → A: **裁定：不是唯一判据；改用「入口载体在执行时是否真的做事」这一运行语义判据。** 三类：**(1) 只被 import 的模块** → 豁免；**(2) 带 `__main__` 块且该块真的做事** → 适用；**(3) 带 `__main__` 块但只被 import** → 按字面判据会判适用，而运行语义上它作为脚本跑时几乎不做事，判为**适用仍需补齐**（FR-026 要求「执行后必然产生副作用」的入口载体）——本仓实例是 `scripts/python/declaration_reader.py`（被 `validate-requirements.py` import，同时自带 `__main__` 块）。`tests/**` 是**真实的 pytest 模块**，`import` 它们就会跑收集与 fixture 求值、可能写 `.pytest_cache`，故 MUST 判为适用并**由实现阶段的实测数据**确定补齐或登记豁免；`conftest.py` 同理不得被默认豁免。**Why**：题面给的机械判据在 python 侧有两个反例（模块被 import 时不执行 `__main__` 块；`__main__` 块可能只是无害 demo），机械判据不能只靠字面命中；把它们统一成「运行时会不会真的做事」后，bash 与 python 用的是同一个问题，而不是两套词汇。`tests/` 不得因「它是测试目录」被默认豁免——那是 FR-002 明令禁止的「作者声明它是库」。**落点**：FR-009、FR-026、SC-010、A2 加强事实段。

  > **更正（2026-11-06，analyze 回环 1，superseded）**：上文第 **(3)** 类「带 `__main__` 块但只被 import … 判为**适用仍需补齐**」与 FR-026 相反，作废。按运行语义，带 `__main__` 块但只被 import 的模块作为脚本运行时几乎不做事，**判为豁免**（本仓实例 `declaration_reader.py`）；这与 FR-026 的「执行后必然产生副作用」判据一致。上文原文保留以留痕，但在本句覆盖范围内 MUST NOT 被引用为依据；权威表述是 FR-009 / FR-026。

- Q: 契约正文的唯一 owner 文档落在哪个 shared 层路径（`shared/guidelines/` 还是 `shared/definitions/`，文件名是什么）？ → A: **裁定：`shared/definitions/script-interface-definitions.md`**（本仓运行时投影 `.specify/shared/definitions/script-interface-definitions.md`）。**Why**：`definitions/` 在既有惯例中拥有「机器可判定的判据 + 取值域」（`contract-clause-definitions.md`、`flow-class-definitions.md`、`probe-definitions.md`、`sdd-routing-definitions.md`），`guidelines/` 拥有「纪律与实践方法」（`fast-fail.md`、`one-source-of-truth.md`）。本契约的主体是一张可被程序复算的判据表，故归 `definitions/`；文件名以 `-definitions.md` 结尾，与同目录全部兄弟一致（Grounded Naming 的 sibling imitation 档）。文件顶部 MUST 声明它拥有的五件东西。**落点**：A3、FR-015、Key Entities「已声明例外」的登记载体。

- Q: `--version` 输出什么形态（框架版本 + 脚本名？独立语义版本？）以及版本的事实来源？ → A: **裁定：单行 `<script-name> <framework-version>`，版本从 `pyproject.toml` 的 `version` 字段运行时读取。** 例：`sync-mirrors.py 0.0.22`。脚本里 MUST NOT 出现字面版本号（那是第二定义点）；读取失败时输出脚本名 + `unknown` 并保持成功退出——版本查询不应该变成一条能挂住的路径。**Why**：脚本没有独立生命周期，随 `specify init` 分发，唯一真实的版本事实是框架自身的版本；把框架版本写进每个脚本会在下一次发版时静默漂移，而漂移的版本号正是本特性要消灭的「身份不可回答」。这也与 § Out of Scope「不引入每脚本 `version` 文件」一致。实测佐证：全仓 `add_argument(..., action="version")` 命中数为 0，没有任何既有实现需要兼容。**落点**：A4、FR-004、SC-011。

- Q: 已声明例外（FR-020）登记在哪里、谁维护、检查器怎么读，才既可机械判定又不成为逃生门？ → A: **裁定：登记在 owner 文档 `shared/definitions/script-interface-definitions.md` 的 `## Declared Exceptions` 章节；人与 `/speckit.implement` 都可改；检查器是唯一读者，且 MUST 逐条复算机器判据。** 每一行必须同时满足：路径存在、位于 `skills/external/<name>/`、该技能 `SKILL.md` 声明 `classification: external`；三者任一不成立 → 检查**报错**（既不默认放行，也不默认排除）。不在该章节里的第三方候选一律按普通候选判红。**Why**：「例外写在宪法里」会让检查器无法读；「例外写在检查器的代码常量里」会把判据和凭据混在一起，且改凭据要改代码。把它放进 owner 文档，既符合 One Source of Truth（登记载体只有一个），又让检查器保留「复算而不信任」的能力——伪造的例外无法通过复算。实测判据：`skills/external/create-skills/` 与 `coaching-skills/` 声明 `classification: internal`，因此**不能**登记为例外。**落点**：FR-020、FR-027、Key Entities、SC-012、A6。

  > **更正（2026-11-06，plan 阶段实测）**：上句的事实读数有误——两个技能实际声明 `classification: external`（见 A6 与 Edge Cases「上游来源判定」的更正）。按 FR-027 它们因此落在第三方侧；由于其实测无 `*.sh` / `*.py` 脚本，本特性无需修改它们。原裁定「登记形态」不变。

  > **更正（2026-11-06，analyze 回环 1）**：本条正文末句「`skills/external/create-skills/` 与 `coaching-skills/` 声明 `classification: internal`，因此**不能**登记为例外」的**事实读数**同样作废，以实测为准：两者声明的是 `classification: external`（`grep` 实测 16 个 `skills/external/<name>/SKILL.md` 全部为 `external`），且实测名下无 `*.sh` / `*.py`，故不存在需要登记的例外行。Q6 的**其余裁定全部不变**：登记载体唯一（owner 文档 `## Declared Exceptions`）、列形态为 `path` / `skill` / `unsatisfied clause` / `handling` 四列、检查器逐条复算、`internal` 声明者 MUST NOT 登记为例外。**复算描述随 FR-027 收敛为单一判据**：第三方来源的机器标记只有 `SKILL.md` 的 `classification: external` 一条，不再有「目录内存在上游许可/来源文件」的第二个分支。

- Q: 零副作用怎么取证（工作树指纹？受管目录快照？临时目录？），帮助路径是否允许读环境（如 `git_repo_root`）？ → A: **裁定：在受测仓库之外的副本树上取证，前后两次快照断言逐字节相同；帮助路径 MUST 允许读环境、MUST NOT 允许写。** 快照 = `git status --porcelain` + 全部 `*.sh`/`*.py` 的 `sha256` + `.specify/` 的文件清单与哈希。四条不变量互相牵制：`--help` 允许读环境（`git_repo_root` 等）以生成准确的用法文本，但读环境不得产生写；**MUST NOT 在真实工作树里直接跑**这些调用，因为脚本会在 `.specify/.tmp/` 或 `$TMPDIR` 下建临时目录，直接在原地跑会掩蔽或误报一次真实写入；**标志判定 MUST 前置到所有写型副作用之前**（含镜像 refresh、日志目录、工具 manifest），这是「零副作用」的唯一实现方式——判定在写之后，就变成了「写完才帮助」；bash 侧 MUST 用一个扫描 `"$@"` 的守卫块，且在 source 共享库**之前**——source 之后会把 `--help` 变成一次退出 1。python 侧 `--version` MUST 在每条子命令上可解析，或解析前 `print` + `exit 0`。**Why**：这些细节都有实测反例支撑：`getopts` 遇 `--` 即停且不拒未知长选项；顶层 `action="version"` 在带必填 subparsers 的 `goal-utils.py` 上以退出码 2 拒绝 `--version`；`refresh-tools.sh` 的 `*)` 分支在 `usage` 之后继续执行并写入 `.specify/.tmp/`。**落点**：FR-005、FR-029、Edge Cases「包装脚本」「契约与既有的只读约束冲突」、SC-001/SC-002 的取证方式。

- Q: 三个可能把本契约变成「假绿」的事实前提需要复核：(a) `scripts/python/` 里到底有几个脚本真的实现了 `--version`？(b) `refresh-tools.sh` 到底有没有 `--help`？(c) 本仓有没有脚本把 `-h` 用作其他含义？ → A: **(a) 0 个——requirements 阶段记的「2 个」是误读；(b) 有 `usage()` 和 `*)` 调用，但没有 `--help|-h` 分支；(c) 0 个——没有脚本把 `-h` 用于其他含义。** (a) `evidence-utils.py`、`exec-quant.py` 里的 `--version` 都是它们**探测别的程序**（`node --version`、`<binary> --version`）时传给 `subprocess` 的参数，不是自身接口；全仓 `action="version"` 命中 0。(b) `refresh-tools.sh` 第 53 行有 `usage()`、`*)` 分支调用它，所以 `--help` **会**被当作未知选项拒绝并打印用法——行为上已接近合规，缺的是显式 `--help`/`--version` 分支；同理 `run-tests.sh` 里唯一的 `--version` 是 `"$candidate" -m pytest --version`。(c) 全部 `.sh` 与带 `__main__` 的 `.py` 中，`-h)` 只出现在与 `--help` **合并**的既有帮助分支（7 个脚本），无一把它用于其他含义。**Why**：若把「grep 命中 `--version`」当作「已实现」，验收会把 2 个违规脚本记成合规（假绿），而这正是本特性要治的取证病；`-h` 冲突一旦被想当然地写进规格，实现阶段就会去找一个不存在的案例。三条都已改写进正文（A2 的更正段与 Edge Cases 的 `-h` 条）。**落点**：A2 更正段、Edge Cases（`-h` 冲突条）。

- Q: 契约检查落在哪个既有面（A7 遗留）——新增 pytest 契约测试文件，还是加进某条既有测试？是否接 driver 阶段门禁？ → A: **裁定：新增标准库引擎 `scripts/python/script-interface-check.py` + 新增契约测试 `tests/contract/test_script_interface_contract.py`（`pytest.mark.contract`），不接 driver 阶段门禁。** 引擎形态与既有 `scan-confirmation-gates.py` / `gate-check.py` 同构（`argparse`、只读、退出码 0/1/2、stdout + `--json`）；镜像由既有 `sync-mirrors.py` 生成。**Why**：引擎不能挂进任何既有脚本——那会把无关脚本拖成契约的一部分，违反「规则只约束脚本入口契约，不约束内部实现」；测试必须新增，因为既有测试文件各自守护各自的对象，塞进去会让一个测试文件拥有两个不相关的主题。二者都落在既有面上（`pytest -m contract`、`scripts/python/` 目录约定），故不违反 FR-021 的「不新增门禁步骤」。driver 阶段门禁不接线：接上去就多了一道门，与「复用既有面」的目标相反。**落点**：A7、FR-021、FR-031、SC-008。
