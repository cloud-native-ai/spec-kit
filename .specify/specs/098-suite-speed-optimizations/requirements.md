# Requirements Specification: 测试套件提速五项优化（xdist 验证 / slow 分档 / 会话缓存 / 去固定 sleep / 进程内直调）

**Requirement Branch**: `098-suite-speed-optimizations`
**Created**: 2026-11-10
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（维护 `scripts/bash/run-tests.sh`、`pyproject.toml` marker 注册、`tests/conftest.py` 共享夹具与 `tests/contract/`、`tests/integration/` 测试的作者）、SDD 驱动者（baseline / closure 两槽位全量运行的执行与记账者）、以及下游项目中经同一 runner 运行测试的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 在判定「缺省测试运行选择哪一档」「哪些测试可以打 slow marker、判据是什么」「两槽位全量预算如何保持完整」「全语料扫描能否跨测试复用」「哪些固定 sleep 必须去掉、换成什么确定性与同步机制」「哪些 subprocess 调用应改为进程内直调、哪些必须保留」时打开本规格，据 FR-001…FR-022 与 SC-001…SC-011 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "测试套件提速五项优化：1) 引入 pytest-xdist -n auto（先只并行 tests/contract 验证）；2) 给慢测试打 slow marker（integration 进程/队列类 + 少数全语料扫描型 contract），PR 默认 -m 「not slow」，全量留给每日或 closure；3) 会话级缓存全语料扫描结果：coverage_receipt / clause_coverage 的仓库遍历改为 session fixture；4) 去固定 sleep：client_metrics 的 1.1s×8 换成注入时钟/单调序号，runner 测试用事件文件替代固定等待；5) 能走进程内 API 的不要起子进程：subprocess.run 中的 specify CLI / 纯 Python 引擎调用改直调。约束：不改测试覆盖选择与判据；两槽位全量预算（implement 起点 + closure）与 runner 入口 scripts/bash/run-tests.sh 不变；xdist 已是缺省形态，本特性验证并固化 -m 「not slow」缺省与 marker 分档。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

测试套件的成本已是本项目的质量属性（宪法 XX · Efficient Test Execution）：runner 的缺省形态是进程并行（`-n <effective> --dist load`，owner：`.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md`，下文简称「runner 契约」），串行只作为显式、嵌套或没有 xdist 时的完整回退。但剩余成本仍集中在四类可消除的重复上，且没有正式的分档：

1. **没有档位**：全部测试在一个选择里运行；慢的进程/队列类 integration 测试与少数全语料扫描型 contract 测试拖慢每一次反馈循环，用户期望「PR 默认不跑慢档、全量留给每日或 closure」。
2. **按测试重复扫描**：需要遍历仓库或全语料的两处 contract 测试（`tests/contract/test_coverage_receipt.py`、`tests/contract/test_clause_coverage.py`）在多个用例中重复做同样的只读遍历；当前测试树中 session 级夹具数量为零。
3. **固定 sleep 充当同步与语义**：2026-11-10 只读探针在 `tests/` 下测得 `time.sleep` 20 处（8 个文件），其中 `tests/contract/test_client_metrics.py` 的 8 处 `time.sleep(1.1)` 以真实时间差制造入口顺序确定性，runner 相关 integration 测试以固定等待等待状态文件出现。
4. **子进程替代进程内调用**：同一探针测得 `tests/` 下 499 处 `subprocess.run` 源码引用（contract 340 / integration 89 / unit 46，另有 fixtures 与嵌套树），其中一批只是以子进程方式调用纯 Python 引擎或 specify CLI 的 Python 行为，解释器启动成本被重复支付。

本特性按用户五项要求收敛这些成本，同时**不改变测试覆盖的选择与判据**：提速不得以缩小选择、跳过、宣告 flaky 或重试到绿换取（宪法 XX）。xdist 已是缺省形态，本特性**验证并固化** `-m "not slow"` 缺省与 marker 分档，而不是重新引入并行机制；两槽位全量预算（implement 起点 baseline + review 后 closure）与 runner 入口 `scripts/bash/run-tests.sh` 保持不变。

现状基线（2026-11-10 只读探针，证据：`test-evidence/requirements-baseline-probe.txt`）：xdist 3.8.0 可导入；runner 缺省并行；已注册 marker 为 `contract` / `integration` / `serial`，`slow` 未注册且使用数为 0；session 级夹具 0 个；`time.sleep` 20 处 / 8 文件；`subprocess.run` 源码引用 499 处。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 缺省反馈循环只跑快档，且排除被明示 (Priority: P1)

框架维护者在日常开发/PR 式循环中运行规范 runner（`bash scripts/bash/run-tests.sh`），得到一次并行运行：慢档测试被排除，运行耗时显著低于全量；runner 在运行形态行中披露排除了多少条慢档测试，使这次运行不可能被误读为完整全量。

**Why this priority**: 这是五项优化对日常体验的主要收益来源；没有明示的排除披露，「更快」就会以「少了测试」的代价被静默兑现，直接违反宪法 XX。

**Independent Test**: 在同一棵树上分别运行缺省档与全量档，用 `--collect-only -q` 证明两者的测试 id 集合差恰等于 `slow` 标记集合，用墙钟记录证明缺省档更快；在缺省运行中注入一条新的 `slow` 测试，断言被排除数递增。

**Acceptance Scenarios**:

1. **Given** 测试树中存在 `slow` 标记的测试，**When** 以规范 runner 无参数运行，**Then** 运行的收集集合等于全量集合减去 `slow` 集合，且 stderr 的运行形态行披露被排除条数。
2. **Given** 一个不含任何 `slow` 标记的树，**When** 缺省运行，**Then** 选择等于全量集合，运行形态行披露排除数为 0。
3. **Given** 调用方自带 `-m "contract"`，**When** 缺省运行，**Then** runner 原样转交该选择，缺省的 `not slow` 排除 MUST NOT 重写或合并调用方的 `-m`。

---

### User Story 2 - 全量档与两槽位预算仍然完整 (Priority: P1)

维护者需要一次覆盖含慢档在内全部测试的运行（每日、调试、closure）；SDD 驱动的两个预算槽位（implement 起点 `baseline`、review 通过后的 `closure`）继续以全量档执行并用 `--names-out` 做名称级失败名单比较，槽位数、时点与顺序不变。

**Why this priority**: 分档一旦让全量路径消失或让两槽位静默地只跑快档，覆盖判据就被改写——这正是宪法 XX 禁止的「缩小选择换速度」。

**Independent Test**: 以全量档运行一次，断言收集集合等于变更前的全量集合（仅允许本特性新增测试与逐条列明的显式处置）；检查驱动者两槽位命令均显式请求全量档，并用一次故障注入验证 `--names-out` 名单比较仍然转红。

**Acceptance Scenarios**:

1. **Given** 存在 `slow` 标记，**When** 以全量档运行，**Then** 收集集合包含全部 `slow` 测试，退出码与失败名单语义与既有 runner 契约一致。
2. **Given** 任一预算槽位，**When** 执行槽位命令，**Then** 命令显式请求全量档，产出 `--names-out` 名单并记录到状态脊，比较规则不变。
3. **Given** 变更前后的同一棵树，**When** 比较全量档 `--collect-only -q` 的测试 id 集合，**Then** 差集仅包含本特性新增测试与逐条列明的显式处置，没有删除或改名的既有测试。

---

### User Story 3 - 全语料扫描每个会话只算一次 (Priority: P2)

维护者运行涉及 `coverage_receipt` 与 `clause_coverage` 的契约测试时，仓库/语料的只读遍历每个测试会话（每个并行 worker）至多发生一次，多个用例复用同一份只读结果；需要改写被扫描内容的用例改用自己的每测试夹具，互不污染。

**Why this priority**: 这是纯浪费——同样的只读扫描按用例重复；但它不影响选择与判据，所以低于两条 P1 的完整性要求。

**Independent Test**: 以带计数探针的默认档运行这两个测试文件，断言仓库遍历次数与 worker 数同阶、与用例数无关；缓存前后断言集合等价；篡改被扫描内容后相应测试仍能转红。

**Acceptance Scenarios**:

1. **Given** 一个并行会话，**When** 运行这两个测试文件，**Then** 每个 worker 对每个受管扫描面至多执行一次仓库遍历。
2. **Given** 共享缓存已建立，**When** 某用例修改自己的夹具树，**Then** 该用例不消费共享缓存，其他用例的断言不受影响。
3. **Given** 被扫描的源内容被篡改，**When** 运行相应断言，**Then** 测试转红——缓存 MUST NOT 把扫描结果变成恒定绿。

---

### User Story 4 - 等待与顺序不再靠固定 sleep (Priority: P2)

维护者运行 `client_metrics` 与 runner 相关测试时，入口顺序确定性来自注入时钟或单调序号，完成等待来自可观察事件（事件/状态文件），测试不再按固定常量睡眠，机器变快时测试自然变快、机器变慢时不因「没等够」而假红。

**Why this priority**: 固定 sleep 同时是耗时与 flakiness 来源；它与选择无关，但直接决定去固定等待的可判定性。

**Independent Test**: 程序化扫描断言两个作用域内不再存在承担同步职责的 `time.sleep`；测量 `test_client_metrics.py` 的墙钟不再包含 8×1.1 秒的固定等待；对 runner 测试注入更快的完成事件，断言测试提前结束而不是等满固定时限。

**Acceptance Scenarios**:

1. **Given** 两个入口记录需要确定的先后顺序，**When** 以注入时钟/单调序号生成时间戳，**Then** 顺序断言与原先一致，且测试不依赖真实 1.1 秒时间差。
2. **Given** runner 的完成状态以事件文件可观察，**When** 事件先于固定轮询出现，**Then** 测试在观察到事件后立即继续，不额外固定等待。
3. **Given** 一个真正依赖真实时间语义的用例（如 TTL），**When** 保留其等待，**Then** 该保留逐条记录理由，不计入「同步性 sleep」清零的违约。

---

### User Story 5 - 非边界的引擎调用改为进程内直调 (Priority: P2)

维护者运行测试时，只为验证纯 Python 引擎或 specify CLI 的 Python 行为而发起的子进程改为进程内直调，省掉解释器启动；当被验证对象就是进程边界（CLI 契约、退出码、信号/超时、隔离、git 外部命令）时仍以子进程验证。

**Why this priority**: 它带来的是调用点级别的稳定节省，且必须逐点判定进程边界，误改会削弱契约测试的验证强度，所以放在 P1 完整性之后。

**Independent Test**: 对转换清单逐条核对：非边界调用点不再出现 `subprocess.run`；保留点每条有进程边界理由；转换前后同一组断言全绿；把一条已转换调用临时改回子进程时，清单断言转红（证明清单是判别面）。

**Acceptance Scenarios**:

1. **Given** 一个只验证引擎 JSON 输出的用例，**When** 改为进程内直调，**Then** 断言与原先等价，且该用例不再启动解释器。
2. **Given** 一个验证 `--help` / `--version` / 未知选项退出码的用例，**When** 实施本特性后运行，**Then** 它仍以子进程验证，理由记录为「进程边界即被测对象」。
3. **Given** 转换清单中存在未逐条记录的删除，**When** 运行清单断言，**Then** 转红并指名缺失条目。

---

### Edge Cases

- **没有 xdist 的解释器（如 Python 3.8）**：档位选择与 `slow` marker MUST 仍然成立，运行以 `reason=no-xdist` 完整串行完成，退出码与失败名单语义不变；MUST NOT 因缺少并行引擎而报错或空跑。
- **缺省档排除后选择为空**：若全部测试都被标为 `slow`，缺省档 MUST 以具名错误与非零退出报告「排除后选择为空」，MUST NOT 以退出 0 静默通过。
- **调用方选择与档位的组合**：调用方自带 `-m` / 路径 / `-k` 时，档位不得改写其 `-m`；全量档与调用方选择同时出现时，执行一个不含缺省排除的完整选择。
- **同一测试同时标记 `serial` 与 `slow`**：缺省档的两遍组合 MUST 都排除它（并行遍与串行遍均不含），全量档 MUST 在串行遍执行它——两个 marker 正交，不互相吞并。
- **并行 worker 与会话缓存**：xdist 的会话夹具是每 worker 一次；缓存遍历次数的上限按 worker 数计，MUST NOT 按测试数计。
- **名称级比较的时点**：并行/串行名称级一致性比较 MUST 在同一棵树上进行；跨树比较结果不得当作隔离性证据。
- **被保留的子进程边界**：CLI 契约、信号/超时/中断、git 与外部命令、以子进程隔离为被测对象的用例，转换 MUST 保留其进程边界。
- **测量噪声**：墙钟门槛 MUST 在同主机、同日、同一 runner 形态下比较，并记录完整命令、退出码、完整输出与时长；不得用不同机器或不同选择的口径互相比较。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 并行形态验证（xdist 已为缺省，本特性验证并固化）

- **FR-001**: 测试执行 MUST 继续以 `scripts/bash/run-tests.sh` 为唯一入口；在 xdist 可导入、调用方未给 `-n`、未给 `--serial`、且 `PYTEST_XDIST_WORKER` 未设时，缺省形态 MUST 保持 `-n <effective> --dist load`，三种串行回退（`explicit` / `nested` / `no-xdist`）行为 MUST 逐字保持。本特性 MUST NOT 新增第二个 runner、第二套选择逻辑或新的并行机制。〔执行模型 owner 为 runner 契约，本条只引用不重述〕
- **FR-002**: 并行正确性 MUST 以名称级证据判定：同一棵树上，runner 缺省并行运行与 `--serial` 运行经 `--names-out` 产出的 FAILED 名单 MUST 双向一致（两个方向的名单差均为空）；不一致时 MUST 修复隔离缺陷，或按既有 `serial` marker 登记为声明例外并记录证据，MUST NOT 以忽略、重试或改断言处置。〔宪法 XX：先隔离后并行，按名称测量而非阅读测试〕
- **FR-003**: 验证顺序 MUST 自 `tests/contract` 开始：先证明 `tests/contract` 在缺省并行下达到 FR-002 的名单一致，再把同一判据扩大到全量选择；每一阶段的命令、退出码、名单差异 MUST 记录到 `test-evidence/`。MUST NOT 只验证子集就宣称全量并行安全。
- **FR-004**: xdist 缺席的完整性 MUST 保持：不能导入 xdist 的解释器（如 `>=3.8` 中的 3.8）MUST 以 `reason=no-xdist` 完成一次完整串行运行，退出码与失败名单语义不变，MUST NOT 空跑或报错退出。

#### B. slow marker 分档与两槽位全量预算

- **FR-005**: `pyproject.toml` MUST 注册名为 [[STR-001]] 的 marker 并给出语义描述；注册缺失或 marker 名不符 MUST 使对应契约测试转红，MUST NOT 只靠文档约定。
- **FR-006**: [[STR-001]] 的成员判据 MUST 可判定：只允许两类——(a) 需要拉起、等待或终止外部进程/队列的 integration 类测试；(b) 少数需要遍历全语料（整仓或多 spec 目录）的 contract 测试。每一条标记 MUST 在 `test-evidence/` 记录所属类别与理由；MUST NOT 仅凭单次耗时噪声或主观感受归档，MUST NOT 把普通单元测试成批标慢来换取数字。
- **FR-007**: 缺省档 MUST 排除慢档：当调用方没有自带选择时，runner MUST 以等价 [[STR-002]] 的选择运行，并与既有 `serial` 两遍模型正交组合（并行遍排除 `serial` 与慢档，串行遍只取 `serial` 中未被排除者）；排除条数 MUST 由 stderr 的运行形态行披露，使部分运行不能伪装成完整。排除后选择为空时 MUST 具名报错并非零退出。
- **FR-008**: 全量档 MUST 可用且显式：runner MUST 提供一个声明的全量开关 [[STR-003]]，使一次运行覆盖含慢档的完整选择；`--help` MUST 记录该开关，未知选项仍 MUST 按宪法 XXI 非零拒绝；该开关 MUST NOT 改变其他既有参数的语义。
- **FR-009**: 调用方选择 MUST 优先：调用方自带 `-m` / 路径 / `-k` 时，runner MUST 原样转交，缺省慢档排除 MUST NOT 重写、合并或拆解调用方的 `-m`；[[STR-003]] 与调用方选择同时出现时，执行一个不含缺省排除的完整选择。档位与执行形态（并行/串行）正交，`--serial` 不改变档位语义。
- **FR-010**: 两槽位预算 MUST 保持全量：implement 起点 `baseline` 与 review 通过后的 `closure` MUST 经同一 runner 以全量档（含 [[STR-003]]）运行，并继续用 `--names-out` 做名称级名单比较；驱动者文档中的两槽位命令 MUST 显式请求全量档，使缺省档变更不可能静默缩小预算覆盖面。槽位数、时点与顺序 MUST 不变。
- **FR-011**: 全量选择 MUST 不回归（封闭清单声明）：全量档可收集的测试 id 集合在变更前后 MUST 相等，除本特性新增测试与逐条列明的显式处置外无差异；基线取 implement 起点 `--collect-only -q` 读数，允许差集与判据按 `.specify/shared/guidelines/closed-set-claims.md` 声明。MUST NOT 删除、改名或参数化缩减既有测试来提速。

#### C. 全语料扫描的会话级缓存

- **FR-012**: `tests/contract/test_coverage_receipt.py` 与 `tests/contract/test_clause_coverage.py` 中对仓库/全语料的一次性只读遍历 MUST 收敛为 session 级夹具：每个会话（并行下为每个 worker）至多计算一次并跨测试复用；重复遍历 MUST NOT 随用例数线性增长。
- **FR-013**: 共享缓存 MUST 只读且隔离：任何会改动被扫描树的用例 MUST NOT 消费共享缓存（改用自己的每测试夹具）；一个用例的写入 MUST NOT 改变另一个用例的断言输入；缓存结构 MUST NOT 在用例之间被就地修改。
- **FR-014**: 缓存 MUST 等义：同一组断言在缓存前后 MUST 全绿且断言强度不变；MUST 以突变实测证明缓存没有把扫描变成恒定绿——篡改被扫描内容后，相应断言 MUST 转红。

#### D. 去固定 sleep

- **FR-015**: `tests/contract/test_client_metrics.py` 中承担入口顺序语义的固定等待 MUST 移除：顺序确定性 MUST 由注入时钟或单调序号提供，MUST NOT 依赖真实 `time.sleep(1.1)` 制造时间差；顺序敏感指标（如同源重复项、入口排序）的断言集合 MUST 保持不变。
- **FR-016**: runner 相关测试的完成等待 MUST 改为可观察事件：等待 MUST 以事件/状态文件等可观察信号为准并带明确截止，MUST NOT 用固定 sleep 充当同步；轮询若保留，MUST 在观察到事件后立即继续，MUST NOT 以「等够久」替代判据。
- **FR-017**: 去 sleep 的可判定性 MUST 由程序化扫描断言：FR-015 与 FR-016 的作用域内，承担同步或顺序语义的 `time.sleep` 数量 MUST 为零；确实依赖真实时间语义（如 TTL）的保留 MUST 逐条记录理由并列入豁免清单。MUST NOT 以人工阅读代替扫描。

#### E. 进程内直调与度量

- **FR-018**: 进程内优先 MUST 按被测对象判定：当测试以子进程调用纯 Python 引擎或 specify CLI 只为验证其 Python 行为（返回值、JSON、文件效果）时，MUST 改为进程内直调；当被验证对象就是进程边界（CLI 契约、`--help` / `--version`、未知选项与退出码、信号/超时/中断、进程隔离、git 与外部命令）时 MUST 保留子进程。
- **FR-019**: 转换清单 MUST 完备可审：每个转换点与每个保留点在 `test-evidence/` MUST 有一条记录（文件、调用点、转换或保留理由）；转换 MUST NOT 弱化断言（同等行为断言，MUST NOT 以「能 import 即算通过」替代）；清单断言 MUST 在任一已转换点被改回子进程时转红。
- **FR-020**: 度量 MUST 完整捕获并可溯源：本特性 MUST 在同主机、同日、同一 runner 形态下记录全量档与缺省档的墙钟耗时、运行期子进程调用数、固定等待数、全量档收集 id 数；基线取 implement 起点 `baseline` 槽位读数与 2026-11-10 只读探针（证据：`test-evidence/requirements-baseline-probe.txt`）；每次测量 MUST 记录命令、退出码、完整输出与时长。MUST NOT 为度量新增第三次全量运行——组件级测量以定向证据记录在 `test-evidence/`。
- **FR-021**: 被禁止的提速方式 MUST 判红：重试至绿、随机丢参、引入 `skip` / `xfail`、缩小参数化、放宽时限掩盖挂起、无上限 worker 数，任一出现即 MUST 判红；本特性 MUST NOT 以这些方式兑现任何 SC。
- **FR-022**: 既有接口 MUST 不变：runner 入口路径、`--names-out` 文件格式与计数行、退出码语义、`serial` 两遍组合、`--workers` 解析顺序 MUST 保持不变；新增档位开关 MUST 满足宪法 XXI（`-h` / `--help` / `--version` 零副作用、未声明选项非零拒绝），且既有的 runner 契约用例 MUST 保持全绿。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖——它消费既有的 pytest 运行器、既有的 xdist 并行引擎与 CPython 标准库，`pyproject.toml` 只新增 marker 注册。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | 规范测试运行器与选择语义 | signed-contract | runner 契约（`.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md`） | `pyproject.toml` 既有 `pytest` 依赖；本特性零新增第三方依赖 | `scripts/bash/run-tests.sh` 与 runner 契约 | 既有 C-001…C-016 对应用例保持全绿；新增档位行为另有契约用例 | FR-001, FR-002, FR-007, FR-008, FR-009, FR-022 | EP-001 |
| RS-002 | 进程并行引擎（pytest-xdist） | signed-contract | pytest-xdist 上游（本仓只消费） | `pyproject.toml` 既有 `pytest-xdist; python_version >= '3.9'` 声明；探针实测可导入版本 3.8.0 | `pyproject.toml` | 缺省并行在 contract 子集与全量上达到名称级一致；3.8 无 xdist 时完整串行 | FR-001, FR-002, FR-003, FR-004 | EP-002 |
| RS-003 | CPython `>=3.8` 标准库（子进程、时钟、文件系统）与 pytest session 夹具模型 | signed-contract | CPython / pytest 上游（本仓只消费） | `pyproject.toml` 既有 `requires-python` 声明 | `pyproject.toml` | 会话夹具在 `>=3.8` 与并行 worker 下行为一致；注入时钟不依赖第三方库 | FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018 | EP-003 |
| RS-004 | 本特性修订的测试基础设施面（runner 档位、marker 注册、共享夹具、转换清单） | in-scope | 本特性自身 | 不适用（无外部版本面） | `scripts/bash/run-tests.sh`、`pyproject.toml`、`tests/conftest.py`、受管测试文件 | 档位、缓存、去 sleep 与直调四组断言在 `>=3.8` 与缺省并行下全绿 | FR-005, FR-006, FR-010, FR-011, FR-019, FR-020, FR-021 | EP-004 |

### Key Entities *(include if requirement involves data)*

- **测试档位（Test tier）**: 封闭两值——缺省档（排除慢档，供日常/PR 循环）与全量档（含慢档，供每日与两槽位预算）；由 runner 的选择组合实现，不新增第二份测试清单。
- **慢档标记（Slow marker）**: 单一 marker 名 [[STR-001]]；成员判据是进程/队列类 integration 与全语料扫描型 contract，逐条理由为证据，不是规则表。
- **会话级扫描缓存（Session scan cache）**: 每个会话（并行下每 worker）计算一次的只读语料快照；跨测试复用，可突变验证的输入源保持不变。
- **注入时钟 / 单调序号（Injected clock / monotonic sequence）**: 代替真实时间差制造确定顺序的测试夹具输入；只影响测试内时间戳来源，不改产品语义。
- **事件文件（Event file）**: runner 测试等待完成的可观察信号；以出现为准继续，可不依赖固定等待。
- **进程边界分类（Process boundary classification）**: 每个子进程调用点的二值归类——「边界即被测对象」保留，或「仅调用 Python 行为」转换；转换清单是其唯一载体。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 全量档收集不回归：变更前后的全量档 `--collect-only -q` 测试 id 集合差集只含本特性新增测试与逐条列明的显式处置，删除与改名数为零；删掉任一既有测试或改其 id 时该断言转红。基线取 implement 起点读数（FR-011）。 **Path**: final
- **SC-002**: `tests/contract` 并行与串行名称级一致：同一棵树上缺省并行与 `--serial` 的 `--names-out` FAILED 名单双向差为空；注入一个写共享路径的非并行安全夹具时该比较转红（证明比较是判别面而非绿标签）。证据含命令、退出码与耗时（FR-002、FR-003）。 **Path**: final
- **SC-003**: 全量档并行与串行名称级一致：closure 同树比较双向差为空（既存失败按名称相等处理）；新增失败名数为零（FR-002、FR-010、FR-022）。 **Path**: final
- **SC-004**: 缺省档显著提速：缺省档墙钟 ≤ implement 起点基线（同 runner 缺省并行、全量选择）的 50%，同主机同日测量并完整捕获；把慢档重新并入缺省档时读数应回退，作为反度量记录（FR-007、FR-020）。 **Path**: final
- **SC-005**: 全量档不回归且两槽位完整：全量档墙钟 ≤ 基线的 110%；`baseline` 与 `closure` 两槽位均以全量档执行并产出 `--names-out` 名单，closure 比较新增失败名为零（FR-008、FR-010）。 **Path**: final
- **SC-006**: 分档可判定：缺省档收集 id 集合 = 全量档收集 id 集合 − [[STR-001]] 集合（集合差为零）；每条 [[STR-001]] 成员带类别与理由；三组夹具（无调用方 `-m`、调用方 `-m contract`、[[STR-003]] 与调用方 `-m contract` 并用）分别证明 [[STR-002]] 的缺省行为、调用方选择优先与全量档覆盖（FR-005…FR-009）。 **Path**: final
- **SC-007**: 会话缓存按会话而非按用例：带计数探针的缺省档运行中，`test_coverage_receipt.py` 与 `test_clause_coverage.py` 的受管仓库遍历各发生次数 ≤ worker 数，用例数大于遍历次数；缓存前后断言等价，篡改被扫描内容时相应测试转红（FR-012…FR-014）。 **Path**: final
- **SC-008**: 固定同步 sleep 清零：`test_client_metrics.py` 与 runner 测试作用域内承担同步/顺序语义的 `time.sleep` 数量为零（程序化扫描），豁免清单为空或逐条带理由；`test_client_metrics.py` 的墙钟不再包含 8×1.1 秒固定等待（前后定向测量记录）（FR-015…FR-017）。 **Path**: final
- **SC-009**: 进程内直调清单闭合：纯 Python 引擎与 specify CLI 的非边界调用点在转换清单中为零，保留点每条有进程边界理由；转换前后同一断言集合全绿；把任一已转换点改回子进程时清单断言转红（FR-018、FR-019）。 **Path**: final
- **SC-010**: 禁止捷径缺席：全量档收集集合无删除（由 SC-001 承载），变更 diff 中新增的 `skip` / `xfail` / 重试装饰器数为零，参数化条目数不减少（FR-021）。 **Path**: supporting
- **SC-011**: runner 接口不变：既有 runner 契约用例（C-001…C-016 对应）全绿，`--help` / `--version` / 未知选项三组用例全绿，`--names-out` 计数行格式不变（FR-022）。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: implement 起点与实现完成时的全量档 `bash scripts/bash/run-tests.sh --full --collect-only -q` 输出（完整捕获），以及逐条显式处置表；记录在 `test-evidence/`。突变：删除/改名一个既有测试时集合差集断言转红。
- **SC-002 Source**: `tests/contract` 子树的两组运行（缺省并行 / `--serial`）各带 `--names-out`，用 `comm -13` / `comm -23` 双向比较；命令、退出码、耗时与名单差全文记录；非并行安全夹具的突变实测一并记录。
- **SC-003 Source**: closure 槽位的全量档 `--names-out` 名单与 baseline 槽位名单的 `comm -13` 比较，附两槽位命令、退出码与耗时；名单写入状态脊与 `test-evidence/`。
- **SC-004 Source**: implement 起点 baseline 槽位的墙钟（全量选择、缺省并行）与缺省档运行墙钟，同主机同日；完整命令、退出码、完整输出与时长；反度量（慢档并入缺省档）记录。
- **SC-005 Source**: baseline 与 closure 两槽位的全量档读数与名单比较记录；`--names-out` 计数行（`# failed-name list written: …`）全文保留。
- **SC-006 Source**: 三组档位夹具的收集集合与退出码；`slow` 成员逐条理由表；集合差计算脚本输出记录在 `test-evidence/`。
- **SC-007 Source**: 带遍历计数探针的一次缺省档运行记录（探针实现与计数输出全文），加上篡改突变实测与缓存前后断言对照。
- **SC-008 Source**: 程序化扫描输出（扫描命令与命中清单）与豁免清单；`test_client_metrics.py` 的前后定向墙钟测量（同主机同日）。
- **SC-009 Source**: 转换/保留清单（文件、调用点、理由）与逐点断言结果；已转换点改回子进程的突变实测记录。
- **SC-010 Source**: 变更 diff 的程序化扫描（装饰器与参数化计数）与 SC-001 的收集比较记录。
- **SC-011 Source**: 既有 runner 契约测试与脚本接口契约测试的运行记录（命令、退出码、完整输出）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `slow` | FR-005, FR-006, SC-006 |
| `STR-002` | `not slow` | FR-007, SC-006 |
| `STR-003` | `--full` | FR-008, FR-009, FR-010, SC-006 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

<!-- 本阶段无待澄清项；访谈式问题已按假设自行裁决并记录于 § Assumptions，答案将由 /speckit.clarify 按需补记。 -->

## Assumptions

- **A1（Flow Class 判定理由）**: 本特性判为 `execution`——交付物是测试基础设施代码、marker 注册、共享夹具与 runner 行为，验收由机器执行与解析（测试运行、收集集合、名单比较）；没有「交给人阅读的文档」作为交付主体，故 `Flow Type` 写 `-`。用户显式要求头部携带 `**Flow Class**: execution`，与判定一致。
- **A2（「引入 xdist」按现状纠正为「验证并固化」）**: 用户原文第 1 条以「引入 pytest-xdist」表述，但 086 已把 xdist 设为 runner 缺省并行形态（探针：xdist 3.8.0 可导入，runner 解析 `MODE="parallel"` 并传 `-n <effective> --dist load`）。按宪法 VIII（代码是现状事实源），本特性落成「在 `tests/contract` 先行验证名称级一致、再扩到全量」，MUST NOT 重建并行机制。
- **A3（档位缺省的裁决）**: 「PR 默认 `-m "not slow"`，全量留给每日或 closure」裁决为：runner 缺省档排除慢档；全量档由显式开关 [[STR-003]] 请求；两槽位命令改为显式全量。理由：缺省值变化不得静默缩小两槽位全量预算（宪法 XX），槽位数/时点/顺序保持不变。若 plan 阶段证明「缺省全量 + 显式 fast 档」更优，须以否定面和证据重开本假设，不能静默翻转。
- **A4（`--full` 标识符冲突检查）**: 全仓检索（2026-11-10）发现 `--full` 已存在于 `scripts/python/history-utils.py`（语义：提取全部会话），那是另一个脚本的局部 flag；CLI flag 的作用域是脚本级，不构成共享标识符冲突，故采用 [[STR-003]] 作为 runner 的全量开关。若 plan 改用其他名字，MUST 同步更新 [[STR-003]] 的值与其消费行。
- **A5（`slow` 命名冲突检查）**: 仓库内 `pytest.mark.slow` 使用数为 0；`tests/contract/test_measure.py` 中的字符串 "slow" 属于度量词汇禁用表，与本 marker 无关。pyproject 现有 marker 为 `contract` / `integration` / `serial`，新增 [[STR-001]] 不冲突。
- **A6（成员清单是数据，不是规则）**: `slow` 的逐测试清单与 subprocess 转换清单在 plan/implement 由测量产生，本规格只钉判据与证据要求，MUST NOT 在需求中固化逐文件清单（同理：2026-11-10 探针读数 499 处 `subprocess.run`、20 处 `time.sleep`、0 个 session 夹具、0 个 `slow` marker 是**基线读数**，不是未来必须达到的常量）。
- **A7（并行隔离前置以名称级证据判定）**: 是否可并行 MUST 按宪法 XX 用「同一棵树、串行 vs 并行、失败名单按名称比较」判定，MUST NOT 通过阅读测试源码推断；不满足的测试修复隔离缺陷，修不好才登记 `serial` 例外。
- **A8（xdist 的会话粒度）**: pytest-xdist 下 session 级夹具是每 worker 一份，因此「会话级缓存」的遍历次数上限按 worker 数计，而不是全局一次；这仍然消除了「按用例重复扫描」这一主要浪费，且不改变断言语义。
- **A9（测量预算）**: 耗时与名单的对外比较只使用两槽位读数（baseline / closure）与定向证据，不新增第三次全量运行（遵守 sdd-loop-driver efficiency-model 的两槽位纪律与 Single-Run Evidence 纪律）。缺省档墙钟、遍历计数、子进程计数等组件级测量以定向运行记录在 `test-evidence/`。
- **A10（「PR 默认」在本仓的载体）**: 本仓 `.github/workflows/` 下没有运行测试的 CI 工作流；「PR 默认」按「缺省档 = 开发者/本地/PR 一类交互循环的缺省选择」理解，由 runner 缺省值承载，本特性不新增 CI 工作流。
- **A11（保留子进程的边界清单）**: CLI 契约（`--help` / `--version` / 未知选项 / 退出码）、信号/超时/中断、git 与外部命令、以子进程隔离为被测对象的用例保留子进程；这是分类判据的实例化方向，具体逐点清单由变换记录承载。
- **A12（范围外）**: 不改变测试选择判据，不改变两槽位数/时点/顺序，不新增 CI 工作流，不新增第三方依赖；`pyproject.toml` 仅新增 marker 注册。
- **A13（下游 3.8 兼容）**: 无 xdist 的下游解释器仍完整串行（runner 契约 C-006）；`slow` marker 是 pytest 原生能力，不引入新的解释器门槛。
