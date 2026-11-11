# Requirements Specification: /speckit.migrate 一次性迁移收尾命令（旧版 specify 项目 → 新版预期态）

**Requirement Branch**: `097-speckit-migrate-command`
**Created**: 2026-11-10
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（实现与维护 `specify migrate` 子命令、`/speckit.migrate` 模板与迁移引擎的作者）；从旧版本升级而来的下游项目维护者（按 install → init → migrate 三步操作的用户）；审阅本规格的 agent——读者基准按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「migrate 命令的入口形态、期望态来源、处置安全边界、与 init/sanitize 的职责边界、跨版本路径」时打开本规格，据 FR-001…FR-025 与 SC-001…SC-009 决定 plan 与后续实现是否放行
**Input**: User description: "创建一个 speckit.migrate 命令：用户在 specify install 装好新版 CLI、再执行 specify init 安装 .specify 基础设施后，项目里的 .specify 可能是新旧版本混杂态；migrate 命令做一次性收尾，把混杂状态收敛为最新版本的期望状态。复用 init 既有迁移逻辑、/speckit.sanitize 的 Migration wrap-up lane（sanitize-materials）与 anchor-layout-migrate.py，不新造第二套迁移逻辑；命令是用户面向的一次性收尾入口，sanitize 仍为周期性治理。入口形态（/speckit.migrate 运行期模板 + specify migrate CLI 的关系）先调查再定；--dry-run 默认；不可逆动作保留确认门。期望态判据覆盖模板/生成物/锚点布局/兼容链接/镜像，来源以仓库声明为准；支持跨版本 N→N+k 渐进路径。"

## Related Feature *(mandatory)*

**Feature ID**: 024
**Feature Name**: Specification Workspace Versioning

**绑定说明（2026-11-10 clarify）**: 本规格是 Feature 024 的首个子规格，实现其「跨 CLI 版本的 `.specify/` 工作区安全升级」能力。024 详情中原设想的 `.specify/version` 标记、版本→迁移注册表与 `specify upgrade` 命令不作为实现形态——本规格以「当前已安装版本的声明与资产即期望态、一次直达」取代（FR-005、FR-020）。该演进的 registry 集成（024 详情 related-specifications、索引行 Last Updated）受本阶段「只改 requirements.md」约束，记为待办恢复点。

## Overview

`specify install`（安装新版 CLI）与 `specify init`（安装 `.specify` 基础设施）是两条既有入口，但 `init` 的合并策略是**有意的部分刷新**：锚点与用户记忆 no-clobber、框架文件覆盖、退役资产按白名单删除。因此第二步完成后，项目里的 `.specify` 可能是「新旧版本混杂」的状态——旧位置的锚点、前代安装形态的残留、过期生成物、失修或缺失的兼容链接、以及框架源与镜像之间的漂移，都可能继续存在。

本特性新增 `specify migrate` 子命令与 `/speckit.migrate` 运行期模板，作为用户三步流程（install → init → migrate）的**第三步、一次性收尾入口**：以**当前已安装版本**的声明与资产为期望态，只读探测出混杂态的逐项差异，给出逐项处置计划（默认干跑、零写入），经确认后应用收敛；凡移动、替换、移除皆 archive-not-delete，并留下逐运行回执。它是既有迁移机制的**组合者**，不是第二套迁移逻辑：init 的迁移分支、sanitize 的 Migration wrap-up lane 检查器与 `anchor-layout-migrate.py` 继续拥有各自的确定性动作；`/speckit.sanitize` 保持周期性治理的定位不变。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 安装后的一次性收尾 (Priority: P1)

用户刚完成 `specify install` 与 `specify init`，项目里的 `.specify` 是旧版与新版混杂的状态。用户运行 `specify migrate`，先看到完整、逐项的差异计划（零写入）；审阅后以显式应用模式执行，全部差异收敛到当前安装版本的期望态；再次运行得到 clean 计划。

**Why this priority**: 这是本特性的主用户旅程——没有它，命令不存在，其余故事都失去载体。

**Independent Test**: 用一个携带旧布局与历史残留的合成夹具，先干跑、后应用，断言收敛后逐项零差异、应用前干跑零写入、应用后第二次运行零写入。

**Acceptance Scenarios**:

1. **Given** 一个旧版布局的夹具（含旧锚点位置、平铺 internal 技能目录、退役资产残留），**When** 运行 `specify migrate`（默认干跑），**Then** 输出逐项计划且整棵文件树哈希不变。
2. **Given** 同一夹具与已审阅的计划，**When** 以 `--apply` 应用，**Then** 全部差异收敛到期望态，回执逐项可枚举。
3. **Given** 已收敛的树，**When** 再次运行，**Then** 报告 clean 且零写入。

---

### User Story 2 - 安全收尾：不可逆动作有确认门、数据可找回 (Priority: P1)

用户信任迁移不会丢数据：凡删除、移动、覆盖、合并，先归档、留回执、可找回；归档优先使这些动作成为可逆动作并按可逆性自动执行，只有没有归档路径的不可逆动作才保留前置确认；旧新文件冲突由命令合并并保留双方，只有无法合并的结构性冲突才停住并指名双方。

**Why this priority**: 收尾命令直接改写用户项目，安全边界是它可被信任的前提；只有主旅程而无可找回性，命令不可发布。

**Independent Test**: 构造含用户手改文件与旧新冲突的夹具，断言非交互应用执行归档优先处置、每个被替换/合并/归档对象均可找回、可合并冲突保留双方、不可合并冲突拒绝并指名双方。

**Acceptance Scenarios**:

1. **Given** 计划中含归档优先的破坏性处置且无交互输入，**When** 运行应用模式，**Then** 这些项自动执行，回执逐项记录归档与恢复路径，结局为 applied（除非仍有 refused/failed 项）。
2. **Given** 已执行的应用，**When** 检查每个被替换、合并或归档的对象，**Then** 均可在回执指名的归档位置找回。
3. **Given** 目标已存在且内容不等价，**When** 应用，**Then** 可合并的旧新内容被合并并保留双方；不可合并的结构性冲突拒绝覆盖并在计划与回执中指名两个候选。

---

### User Story 3 - 跨版本一次直达，中断可续跑 (Priority: P2)

项目落后多个版本时，用户不需要逐版本升级或安装中间版本：一次 migrate 收敛到当前期望态；若应用中断，第二次运行从回执续做，不重复搬移已归档对象。

**Why this priority**: 真实用户往往跨多个版本升级；逐版本路径会让「收尾」退化成链式操作，但它排在主旅程与安全之后。

**Independent Test**: 用模拟 N→N+k 的多代残留夹具一次收敛；在「已归档、未写目标」处中断，第二次运行完成收尾且不二次搬移。

**Acceptance Scenarios**:

1. **Given** 携带两类以上历史代残留的夹具，**When** 运行一次 migrate 并应用，**Then** 收敛成功且回执载明源版本与目标版本，过程中无中间版本步骤。
2. **Given** 在归档与写入之间被中断的应用，**When** 再次运行，**Then** 报告中断阶段并完成收尾，归档对象不被二次搬移。

---

### User Story 4 - 代理会话与 CLI 走同一引擎 (Priority: P2)

用户在代理会话中用 `/speckit.migrate` 完成同样的收尾：模板驱动同一确定性引擎，计划与结果和 CLI 一致；模板不复制任何检查或处置逻辑。

**Why this priority**: 代理引导是框架的既有使用方式，但它是 CLI 主入口的投影，价值依赖主旅程先成立。

**Independent Test**: 同一夹具上比较两个入口的干跑计划，断言逐项一致；结构测试断言模板只委派、不复制实现。

**Acceptance Scenarios**:

1. **Given** 同一棵混杂树，**When** 分别经 CLI 与模板获得干跑计划，**Then** 两份计划逐项相同。
2. **Given** 模板路径产生计划后，**When** 应用，**Then** 结果与 CLI 应用一致，回执载明同一引擎产物。

---

### Edge Cases

- **目标已存在且内容不等价**（如锚点迁移的目标文件已占用）：普通文件的旧新内容由命令合并并保留双方（两个原件先归档）；只有无法合并的结构性目标（非空目录、损坏链接、不可读内容）才 MUST 拒绝并指名双方，不得静默择一或清空。
- **应用中途崩溃**：已归档对象与已写目标并存时，重跑 MUST 识别已完成的阶段并续做，不重复搬移。
- **无 tty / 无人值守**：归档优先的可逆处置与交互终端行为一致，自动执行并由回执记录恢复路径；没有归档路径的不可逆动作不自动执行并以 blocked 收束；命令不抛出确认提问，也不提供非交互确认旗标。
- **用户手改过框架文件**：替换前必须先归档；不得静默丢弃用户改动。
- **项目未执行过 init（缺 `.specify/`）**：命令拒绝并指向 `specify init`，不得隐式初始化。
- **已是最新**：计划为空、退出码可判定、零写入。
- **用户自建技能与项目专属扩展**：永不入选残留清单（沿用 sanitize 的既有边界）。
- **非 git 目录或 detached HEAD**：命令不依赖 git，探测与处置仍须可用。
- **平台不支持符号链接**：链接维度报告降级事实，不得崩溃或静默当作已收敛。
- **两个 migrate 并发**：回执一文一件、处置幂等，不得依赖单一可变聚合文件。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 入口形态与命令面

- **FR-001**: 框架 MUST 提供用户面向的一次性迁移收尾命令 [[STR-001]]（CLI 子命令），作为本特性全部探测与收敛动作的唯一确定性可执行入口；默认运行形态 MUST 是零写入的干跑（[[STR-003]] 语义，计划呈现），写入 MUST 只在显式应用模式（[[STR-004]]）发生。命令 MUST 拒绝未声明的选项，并满足宪法 XXI 的脚本/CLI 接口契约（`--help` 零副作用应答）。
- **FR-002**: 框架 MUST 提供运行期命令模板 [[STR-002]]，它 MUST 是同一引擎的薄投影：探测与处置 MUST 全部经 FR-001 的入口执行，模板 MUST NOT 实现第二份检查、第二份计划或第二份处置逻辑；同一棵树上两个入口的干跑计划 MUST 逐项一致。
- **FR-003**: 命令的前置条件 MUST 是项目已经执行过 `specify init`（`.specify/` 基础设施存在）；前置条件不满足时 MUST 以可判定的错误（见 FR-019 的输入错误退出形态）拒绝并指向 `specify init`，MUST NOT 隐式执行 init，MUST NOT 在缺少 `.specify/` 的目录上创建或修改任何文件。
- **FR-004**: 命令 MUST NOT 承担安装与初始化职责：新版本包安装（`specify install`）与 `.specify` 基础设施建立/刷新（`specify init`）留在既有入口；本命令只做两者之后、以当前已安装版本为期望态的收尾。用户三步流程（install → init → migrate）中前两步的产物 MUST 被视为本命令的输入，而非可重做的步骤。

#### B. 期望态与只读探测

- **FR-005**: 期望态的唯一来源 MUST 是当前已安装版本随包分发的声明与资产；「当前已安装版本」MUST 判定为运行本命令的 CLI 进程所加载的包资源（`get_resource_path()` 解析的已安装副本），框架源工作区（`skills/external/` 为目录）以其自身声明与脚本副本为源（宪法 XI 自举），客户端模式 MUST NOT 读取工作区可能过期的 `.specify/scripts/` 副本。具体读取入口 MUST 固定为以下既有 owner，不得另立来源：退役清单＝CLI 源内 `OBSOLETE-ASSET-REGISTRY` 标记块（`src/specify_cli/__init__.py`；`sanitize-utils.py` 侧为受漂移测试钉住的镜像）、残留/镜像/链接/索引/死引用＝`sanitize-utils.py` 的确定性检查器、锚点布局＝`anchor-layout-migrate.py` 的 check 动作、生成副本与镜像一致性＝`regen-command-copies.py --check` 与 `sync-mirrors.py --check`、框架资产刷新与退役处置＝init 的既有 `cleanup_obsolete_framework_assets` / `migrate_flat_internal_skills`。命令 MUST NOT 按源项目版本号选择迁移路径，MUST NOT 读取或引入 `.specify/version` 类版本标记作为判据（当前不存在且本特性不新增），MUST NOT 以模板指纹或命令内置的旧结构清单猜测旧版本。新增或修改一个期望态维度 MUST 经修订声明层或既有引擎完成，MUST NOT 在命令内加入一次性检查。
- **FR-006**: 探测 MUST 只读且确定性：同一棵树上的重复干跑 MUST 产出逐项相同的计划（稳定顺序与内容）；干跑 MUST NOT 写入、移动或删除任何文件与数据。计划 MUST 逐项承载「维度、当前态、期望态、拟处置、依据路径」，使每个差异项可独立审阅。
- **FR-007**: 期望态覆盖维度 MUST 至少包含五类：①模板与生成物（含命令副本、技能与代理镜像）；②锚点布局（`anchor-layout-migrate.py` 的判定对象）；③兼容链接（符号链接模型）；④镜像一致性（框架源与 `.specify/` 镜像）；⑤迁移残留（前代安装形态的残余类）。各维度的检查项集合以既有声明与引擎为唯一 owner，本规格不复述其清单。
- **FR-008**: 探测 MUST NOT 产生假绿：每个维度 MUST 具备可转红断言——移除该维度的收敛处置、或在夹具中注入一处差异时，对应检查 MUST 报出该项；「计划为空」只允许在真实无差异时出现。

#### C. 复用与职责边界

- **FR-009**: 框架资产刷新与退役 MUST 复用 `init` 的既有迁移分支能力（含 obsolete 资产处置与平铺 internal 目录收敛语义），MUST NOT 存在第二份实现：两个入口 MUST 由同一可执行体或同一共享函数承载，并以等价性测试钉住「同一维度、同一结论」。
- **FR-010**: 迁移残留、镜像与链接维度的确定性检查 MUST 消费 `/speckit.sanitize` 既有引擎（`sanitize-utils.py`）的检查器与发现格式，MUST NOT 复制一份检查实现；migrate MUST 以这些检查器的只读发现作为计划输入。只读消费 MUST 采用进程内导入检查器或经引擎新增的只读动作完成；MUST NOT 以 `--action collect` 作为计划输入（该动作会写 `findings.json` 台账），MUST NOT 读写 sanitize 的发现台账——pending 台账是周期治理状态，只归 sanitize 所有。
- **FR-011**: 锚点布局维度 MUST 由既有 `anchor-layout-migrate.py` 的 check/apply 动作唯一承载；migrate MUST NOT 另写布局迁移逻辑，MUST NOT 绕过该引擎的拒绝覆盖与幂等语义。
- **FR-012**: 职责边界 MUST 为「migrate = 一次性收尾；sanitize = 周期性治理」：migrate MUST NOT 吸收 sanitize 的周期性职责（保留期回收、跨运行的 pending 台账、序号重排等）；一次成功的 migrate 之后，用户 MUST NOT 被要求再运行 sanitize 才能达到迁移后的预期态；sanitize MUST 继续可用，其 Migration wrap-up lane 的检查器与处置语义 MUST 保持不变。该 lane 现状声明「本 lane 即 init 后的指定收尾步骤」，MUST 在同一变更内收敛为：一次性收尾主入口是 migrate，本 lane 保持周期复检兜底。
- **FR-013**: goal/team 档案迁移的唯一入口 MUST 仍是既有 `/speckit.goal` 的 `migrate-archive`；本命令 MUST NOT 吸收或重复该迁移，只在计划与回执中以静止指针列出责任方，不探测、不处置。

#### D. 处置、安全与回执

- **FR-014**: 每个差异项的处置结果 MUST 落入封闭六值集：`converged`（已收敛，零写入）、`write`（可逆安全写，自动执行）、`replace`（先归档后写入或合并）、`archive`（移动或移除并归档，可找回）、`refuse`（冲突或歧义，停住并指名双方）、`blocked`（破坏性且无归档路径，或执行被阻止）。锚点旧新冲突由 `replace` 的合并机制承载（双方内容保留、原件先归档）；`refuse` 只留给不可合并的结构性冲突。`refuse` MUST NOT 择一胜出，任何处置 MUST NOT 静默跳过差异项。
- **FR-015**: [[STR-004]]（`--apply`）是本命令唯一的写入授权。破坏性动作 MUST archive-first：原件先复制进逐运行归档根，回执逐项记录 `recover` 路径；因此这些动作是可逆动作，MUST 在交互与非交互环境下自动执行，MUST NOT 要求第二次确认，MUST NOT 提供 `--yes` / `--force` / `--confirm` / `--non-interactive` 等确认旗标。没有归档路径的不可逆动作 MUST NOT 自动执行，以 `blocked` 收束并报告原因；判据与清单的唯一 owner 是 `.specify/shared/guidelines/confirmation-gates.md`，本规格不复述清单。无 tty 或无人值守环境与本条一致：可逆项照常执行，只报告真正无法完成或无法合并的项。
- **FR-016**: 用户内容保护 MUST 成立：用户自建技能、项目专属扩展、用户手改的框架文件 MUST NOT 被当作残留删除；替换用户内容的处置 MUST 先归档再写，并在回执中给出恢复路径；旧新同位置普通文件的冲突 MUST 合并而不是择一，双方内容都保留，两个原件都先归档；替换、合并与归档 MUST 沿用 reconcile 家族的 archive-not-delete 语义。
- **FR-017**: 幂等与可续跑 MUST 成立：成功应用后再次运行 MUST 为 clean 计划且零写入；应用中断后再次运行 MUST 能从已落盘的回执与计划续做，MUST NOT 二次搬移已归档对象；同一对象的重复处置 MUST 收敛为 no-op。失败语义 MUST 为前向续跑 + 逐项经归档位置找回（FR-016、FR-018）；命令 MUST NOT 提供全局回滚/undo 动作，回滚能力不在本特性范围内。
- **FR-018**: 每次运行（干跑与应用）MUST 产出一份逐运行回执，承载运行时间、源版本与目标版本、运行状态、续跑标识（续跑时指向被接续的运行）、差异项清单、逐项处置、归档位置、拒绝原因、恢复途径与最终结果；回执 MUST 是一文一件的逐条目记录（并发开发安全纪律），MUST NOT 写入单一可变聚合文件。干跑回执 MUST 以输出流承载、不落盘（FR-006 零写入的适用形态）；应用回执的落点 MUST 为 `.specify/memory/migrate/receipts/` 下的独立文件（文件名含运行时间戳/运行 ID），该目录须按目录治理在同一变更内登记。
- **FR-019**: 命令 MUST 稳定区分四类运行结局并给出可脚本判定的退出码：`clean`（无差异，退出 0）、`planned`（有差异的干跑，退出 1）、`applied`（应用完成或已无剩余差异，退出 0）、`blocked`（因结构性冲突、无归档路径或执行失败未完成，退出 3）；输入或前置条件错误退出 2。应用模式的结局 MUST 按优先级聚合：存在任一 `refuse` / `blocked` 项或执行期 I/O 失败时结局为 `blocked`（退出 3），否则为 `applied`（退出 0）；干跑按计划是否为空取 `clean` / `planned`。结局 MUST 以机器可读 token 载明（文本输出与 `--format json` 包络均含该词），使脚本无需解析自然语言即可判定。同一结局的退出码 MUST 稳定，MUST NOT 用退出 0 掩盖未完成的处置。

#### E. 跨版本与分发

- **FR-020**: 跨版本路径 MUST 为期望态直达：任意旧版本项目（N）一次收敛到当前期望态（N+k），MUST NOT 要求逐版本安装或运行中间版本，MUST NOT 依赖源版本号识别；源版本信息只用于回执记录，MUST NOT 决定处置。源版本 MUST 从工作区 `.specify/source.json` 读取；文件缺失或不可读时 MUST 记 `unavailable` 并写明原因，MUST NOT 推断或猜测。
- **FR-021**: 新命令 MUST 经既有命令装配面分发：源模板 `templates/commands/`、四个运行期副本树的再生、`docs/reference/commands/` 文档与分发基线契约测试 MUST 同步更新；副本 MUST 由再生脚本生成，MUST NOT 手写或绕过。
- **FR-022**: 命令 MUST 满足既有接口契约：CLI 子命令满足宪法 XXI；模板 frontmatter 与副本形态满足既有命令契约测试（含 Qoder 副本 frontmatter 契约）。

#### F. 验收取证

- **FR-023**: 验收 MUST 至少包含三类夹具：纯旧版夹具（旧布局与历史残留）、新旧混杂夹具（部分 init 后）、已最新夹具；纯旧版与混杂夹具 MUST 在干跑报 `planned`、应用后收敛；已最新夹具 MUST 在干跑与再次运行时都报 `clean` 且零写入。旧布局夹具的构成 MUST 只由 FR-005 钉名的声明与检查器已知的残留/布局类合成（退役清单条目、旧代状态文件、平铺 internal 残留、旧锚点布局、已编辑的模板文件、被删除的镜像脚本文件、缺失或断链的兼容链接），并 MUST 覆盖 SC-001 的全部五类维度，MUST NOT 取自历史发行快照，MUST NOT 按命令内猜测清单构造——夹具与探测共享同一来源。
- **FR-024**: 安全取证 MUST 以可转红断言覆盖：确认门缺失时破坏性处置 MUST 被测试判红；归档缺失或回执不可枚举时 MUST 判红；把「全量删除」注入处置时 MUST 判红。
- **FR-025**: 等价性、幂等与续跑取证 MUST 以可转红断言覆盖：两个入口同树同计划（FR-002）；第二次运行零写入（FR-017）；中断续跑不二次搬移。复制或移除其中任一检查实现时，结构测试 MUST 转红。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 Python CLI、既有 pytest 运行器与既有迁移/卫生引擎。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库文件系统与路径解析（差异枚举、归档移动、回执写入、只读探测） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 中既有的 `requires-python` 声明；本特性零新增第三方依赖 | `pyproject.toml` | 干跑与应用在同一解释器上跑通，夹具仓库内路径解析可复现 | FR-006, FR-014, FR-017, FR-018 | EP-001 |
| RS-002 | `typer` CLI 框架（`specify migrate` 子命令面与退出码契约） | signed-contract | Typer 上游（本仓只消费） | `pyproject.toml` 中既有的 `typer` 依赖声明；本特性零新增依赖 | `pyproject.toml` | `specify migrate --help` 零副作用、未知选项拒绝、四类结局退出码被契约测试钉住 | FR-001, FR-019, FR-022 | EP-002 |
| RS-003 | `pytest` 测试运行器（夹具与契约测试执行） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh` 的 contract/integration 子集在 `>=3.8` 上通过 | FR-023, FR-024, FR-025 | EP-003 |
| RS-004 | 既有迁移与卫生引擎的扩展面（init 迁移分支、`sanitize-utils.py`、`anchor-layout-migrate.py`） | in-scope | 本特性自身（扩展既有可执行体，不新增第二份迁移逻辑） | 不适用（无外部版本面） | `scripts/python/anchor-layout-migrate.py`, `scripts/python/sanitize-utils.py`, `src/specify_cli/__init__.py` | 复用等价性结构测试；各引擎 `--help` / `--version` 仍满足宪法 XXI；干跑与幂等读数记录在 `test-evidence/` | FR-009, FR-010, FR-011, FR-012 | EP-004 |

### Key Entities *(include if requirement involves data)*

- **差异项（Diff item）**: 一个可独立审阅的最小差异单元——维度、当前态、期望态、拟处置、依据路径；计划的最小组成单位，也是回执的逐项载体。
- **处置（Disposition）**: 差异项的封闭结果（FR-014 的六值）；回执逐项记录它，不另设第二套状态机。
- **迁移回执（Migration receipt）**: 一次运行的事实记录（FR-018），逐运行一文一件；归档位置与恢复途径的唯一可枚举载体。
- **期望态（Expected state）**: 由当前已安装版本的声明与资产投影出的目标树形；版本无关判据（FR-005），不随项目侧文件变化。
- **前代残留（Legacy residue）**: 早期安装形态在新版下不再有归属的目录、文件或链接形态；其类别清单由声明与既有 sanitize 检查器拥有（FR-010）。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 纯旧版夹具经一次 [[STR-001]] 干跑与 [[STR-004]] 应用后，与当前安装版本的期望态逐项零差异——五类维度（模板与生成物、锚点布局、兼容链接、镜像、迁移残留）的差异项全部闭环；应用前干跑零写入（应用前后文件树哈希对照），应用后第二次运行报告 `clean` 且零写入。把任一维度的收敛处置移除时该测试转红。 **Path**: final
- **SC-002**: 安全闭环：非交互应用执行归档优先的破坏性处置；每个被替换、合并、归档或移除的对象都能在回执指名的归档位置找回（逐条存在性断言），回执可枚举全部处置与恢复路径；可合并的旧新冲突保留双方内容。把归档动作移除时该测试转红。 **Path**: final
- **SC-003**: 新旧混杂夹具经一次应用后逐项零差异；已最新夹具在干跑与再次运行时均为 `clean` 且零写入；三类夹具（纯旧版、混杂、最新）的 `planned` / `applied` / `clean` 结局均可判定。把夹具的期望态断言从「逐项等价」改成「存在性」时该测试转红。 **Path**: final
- **SC-004**: 跨版本直达：一个携带两类以上历史代残留的夹具（模拟 N→N+k）在一次运行内收敛成功，回执载明源版本与目标版本，过程中没有任何中间版本安装或运行步骤。把期望态判据改成按源版本号选择迁移路径时该测试转红。 **Path**: final
- **SC-005**: 冲突安全：目标已存在且内容不等价时，普通文件旧新内容被合并并保留双方；不可合并的结构性冲突由 [[STR-004]] 应用拒绝覆盖，并在计划与回执中指名两个候选与阻止原因；夹具转绿。把「静默择一」或「清空目标」注入处置时该测试转红。 **Path**: supporting
- **SC-006**: 中断续跑：在「对象已归档、目标尚未写入」处中断一次应用，第二次运行报告该阶段并完成收尾，已归档对象不被二次搬移（存在性与计数断言）。把第二次运行改成重新搬移时该测试转红。 **Path**: supporting
- **SC-007**: 职责边界可判定：一次成功 migrate 后运行 sanitize 的迁移类检查，迁移残留发现为零；migrate 的计划面不出现 goal/team 档案迁移项，只出现指向 `/speckit.goal` `migrate-archive` 的静止指针。把该档案迁移吸收进 migrate 时该测试转红。 **Path**: supporting
- **SC-008**: 用户内容保护：夹具中的用户自建技能与手改框架文件在收敛后仍存在且内容逐字节不变；凡被替换的既有内容均先归档再写。把处置改成「全量删除」时该测试转红。 **Path**: supporting
- **SC-009**: 分发完整：[[STR-001]] 子命令与 [[STR-002]] 模板出现在标准装配面——源模板、四个副本树、命令文档与分发基线契约；副本再生脚本的 `--check` 无漂移。把任一装配面缺失时该测试转红。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/` 下新增的迁移夹具测试与 `test-evidence/` 中的干跑/应用记录：文件树哈希对照（干跑前后、应用后二次运行）、逐维度差异清单、变异实测（移除任一维度处置后转红）。
- **SC-002 Source**: 安全夹具的实测记录：无交互应用的退出码与 applied/blocked 报告、归档位置逐条存在性清单、回执枚举读数、合并双方内容保留断言；归档动作的变异实测。
- **SC-003 Source**: 三类夹具的实测记录：每次运行的结局词与退出码、零写入断言（哈希不变）、变异实测（弱化断言后转红）。
- **SC-004 Source**: 多代残留夹具的迁移前后读数与回执中的源版本/目标版本字段；路径选择判据的变异实测。
- **SC-005 Source**: 冲突夹具的实测记录：计划与回执中指名的两个候选、拒绝文本与退出码；「择一胜出」变异实测。
- **SC-006 Source**: 中断夹具的复现记录（中断点、第二次运行退出码、归档对象计数与存在性）；二次搬移变异实测。
- **SC-007 Source**: migrate 后 sanitize 迁移检查的零发现读数（引擎输出）与计划面检索（goal/team 迁移项为零、静止指针存在）；吸收变异实测。
- **SC-008 Source**: 用户内容夹具的字节哈希对照（收敛前后）与归档记录；「全量删除」变异实测。
- **SC-009 Source**: 装配面清单检索（源模板、四副本树、命令文档、分发基线契约）与 `regen-command-copies.py --check` 的退出码；缺失装配面变异实测。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"specify migrate"` | FR-001, SC-001, SC-009 |
| `STR-002` | `"/speckit.migrate"` | FR-002, SC-009 |
| `STR-003` | `"--dry-run"` | FR-001 |
| `STR-004` | `"--apply"` | FR-001, SC-001, SC-005 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-10（无人值守 requirements，自行裁决并记录）

- Q: 入口形态——只做 `/speckit.migrate` 运行期模板，还是同时提供 `specify migrate` CLI 子命令？ → A: 双面一引擎：`specify migrate` 是唯一确定性可执行体，`/speckit.migrate` 是驱动同一引擎的薄投影。依据（2026-11-10 只读调查）：现行 CLI 仅有 init / check / render-agents，无 migrate / upgrade 类子命令；init 是唯一收尾路径且无 dry-run、无独立迁移确认门；既有安全默认先例是 `goal-utils.py migrate-archive --dry-run|--apply` 与 sanitize 的确认后 apply。用户三步流程本身处于 CLI 上下文。见 A2。
- Q: `--dry-run` 默认的具体形态？ → A: 默认运行即干跑、零写入；写入只经 `--apply` 显式进入；干跑与应用共享同一份计划。见 A3。
- Q: 期望态从哪里读？ → A: 当前已安装版本的随包声明与资产，由 CLI 自身与安装产物回答；不按源项目版本号分支，不内置旧结构猜测。见 A4。
- Q: 处置结果是否需要封闭集？ → A: 需要；FR-014 给出六值封闭集并作为唯一 owner，机器 token 即该条列出的取值，plan 的契约只引用不复述。
- Q: 回执落点在哪里？ → A: 逐运行一文一件；候选落点 `.specify/memory/migrate/`，最终路径由 plan 在并发开发安全约束下定名，并配两写者不同路径的测试。见 A6。
- Q: 无人值守时破坏性动作怎么办？ → A: 归档优先的可逆动作自动执行并由回执记录恢复路径；没有归档路径的不可逆动作不自动执行、以 `blocked` 收束并给出报告（confirmation-gates 的可逆/不可逆两级判据）。见 A9。

### Session 2026-11-10（clarify，无人值守自我裁决）

- Q: Feature 绑定——本规格归入既有 Feature 还是新建？ → A: 绑定既有 Feature 024（Specification Workspace Versioning，Draft）；其能力域正是「跨 CLI 版本的 `.specify/` 工作区安全升级」，且当前没有已绑定规格（Spec Path 为 `-`）。024 早先设想的 `.specify/version` 标记、版本→迁移注册表与 `specify upgrade` 命令由本规格的「声明驱动期望态 + 一次直达」取代（FR-005、FR-020）；依据：仓库当前不存在 `.specify/version`，而声明/引擎面均已就绪。候选对照：015 CLI Interface 仅泛化终端界面、047 框架材料卫生仅周期治理，均不如 024 贴合。registry 集成（024 详情 related-specifications、索引行 Last Updated）受本阶段「只改 requirements.md」约束，记为待办恢复点。
- Q: 混杂态判定清单的确定性来源是什么，是否使用版本标记/模板指纹？ → A: 钉名五个既有 owner 作为唯一来源（退役清单＝CLI 的 `OBSOLETE-ASSET-REGISTRY`；检查器＝`sanitize-utils.py`；锚点布局＝`anchor-layout-migrate.py` check；副本/镜像一致性＝`regen-command-copies.py --check` / `sync-mirrors.py --check`；刷新退役＝init 的 `cleanup_obsolete_framework_assets` / `migrate_flat_internal_skills`），见 FR-005；不使用 `.specify/version` 标记（不存在且不新增）、项目侧版本号或模板指纹识别旧版本。`--dry-run` 默认维持既有裁定（默认即干跑、零写入；A3）。
- Q: 与 sanitize 的复用方式与写面边界？ → A: 只读消费检查器（进程内导入或引擎只读动作扩展）；MUST NOT 以 `--action collect` 作计划输入（它写 `findings.json` 台账），MUST NOT 读写 sanitize 台账（FR-010）；sanitize-materials 的 Migration wrap-up lane 定位声明在同一变更内改为「周期复检兜底，一次性收尾主入口是 migrate」，其检查器与处置语义不变（FR-012）。migrate 的唯一写面是自有逐运行回执，落点定名 `.specify/memory/migrate/receipts/`（FR-018）。
- Q: 确认门形态与失败回滚语义？ → A: 单授权——[[STR-004]] 是唯一写入开关；归档优先使破坏性处置成为可逆动作，交互与非交互环境都自动执行并由回执记录恢复路径（FR-015、FR-019），不提供任何确认旗标。没有归档路径的不可逆动作不自动执行、以 blocked 收束。失败语义为前向续跑（从回执续做）加逐项归档找回，不提供全局回滚/undo（FR-017）；跨版本 N→N+k 一次直达维持 FR-020/A5。
- Q: 旧布局夹具的构成从哪来？ → A: 只由 FR-005 钉名的声明与检查器已知的残留/布局类合成（退役清单条目、旧代状态文件、平铺 internal 残留、旧锚点布局），不得取自历史发行快照或命令内猜测清单；夹具与探测共享同一来源（FR-023）。

## Assumptions

- **A1（类别判定：execution）**: 本特性判定为 `execution` 类：交付物是机器执行、解析与消费的命令面（CLI 子命令、运行期模板、迁移引擎与契约测试），验收 oracle 是运行命令得到的退出码、计划与文件树差异，而不是读者阅读；`Flow Type` 写 `-`。
- **A2（入口形态裁定：双面一引擎）**: 用户简报要求入口形态先调查再定。调查结论见 Clarifications 第一条与 A2 引用的事实；裁为「CLI 子命令为唯一确定性可执行体，模板为薄投影」。理由：三步流程处于 CLI 上下文；代理会话需要同一入口；单一引擎满足宪法 XIV（一个事实一个 owner）与 XII（复用优先于新造）。
- **A3（dry-run 默认）**: 默认运行即干跑、零写入；写入只经显式应用旗标进入；干跑与应用共享同一计划。与 sanitize 需确认后 apply、migrate-archive 需互斥旗标的既有安全默认一致。
- **A4（期望态来源）**: 期望态取「当前已安装版本」的声明与资产，不从项目侧文件猜测版本；具体读取入口已于 clarify 钉入 FR-005，不再留给 plan 选型。
- **A5（跨版本直达）**: 期望态判据与源版本无关，故 N→N+k 一次收敛；本特性不产出按版本号的迁移脚本链，也不要求中间版本。
- **A6（回执落点）**: 回执逐运行一文一件，落点于 clarify 定名为 `.specify/memory/migrate/receipts/`（FR-018）；目录登记与两写者不同路径测试随实现落地。
- **A7（不在本命令重做 install/init）**: 缺 `.specify/` 时拒绝并指向 init；命令不下载包、不重建基础设施。
- **A8（goal/team 档案迁移排除）**: 沿用 sanitize 模板既有声明——该迁移唯一入口是 `/speckit.goal` 的 `migrate-archive`；migrate 以静止指针列出责任方，不探测、不处置。
- **A9（无人值守行为）**: 依 `.specify/shared/guidelines/confirmation-gates.md` 的决策门矩阵「无人值守」行：可逆写自动执行并记录；不可逆动作停住并给 blocked 报告，不产生确认提问。
- **A10（不依赖 git）**: 探测与处置只依赖文件系统；非 git 目录与 detached HEAD 下命令仍可用。
- **A11（用户内容保护优先于收敛完备）**: 当「收敛到期望态」与「不删除用户内容」冲突时，后者优先——该项以 `refuse` 或 `replace`（先归档）处置并报告残余，不用删除换取计划全绿。
