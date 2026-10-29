# Contract: 驱动接入（Driver Integration）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：阶段序列、哨兵、watcher、卡死处置与快车道归 `skills/external/sdd-loop-driver/`（载体 owner 058）；
两槽位时点与审计口径归 `references/efficiency-model.md` §2（owner 067）；证据四键口径归
`templates/verification-log-template.md` 的 `gate-implement-evidence-binding`。本契约只登记**类别分支**。

## 派发载荷

- **C-001** 每次阶段派发 MUST 在第①段携带类别**四元组**：`flow_class=<值>`、`source=<declaration|default>`、
  `marker=<默认标记或空>`、`error=<E3 登记的码或 ->`。本地原生子代理与远端 CLI 两种拓扑 MUST 同规——
  提示词是类别的唯一载体。`error` 位存在的理由是把「机制降级」与「作者未声明」在载荷上分开
  （两者都可能出现 `source=default`）。(FR-018)

- **C-002** 载荷缺任一元组键 MUST 判为派发构造缺陷，U4 MUST NOT 放行。子代理 MUST NOT 自行推断、补默认或按介质
  猜测类别。(FR-018)

- **C-003** 取值的唯一来源 MUST 是该线 `requirements.md` 的声明行，经 `class-resolution.md` 的同一条解析入口取得，
  且在**每次阶段派发前**解析一次。状态脊中的类别行 MUST NOT 充当取值来源；重入时 MUST 重新解析并与观测比对，
  不一致 MUST 记 re-baseline 事件并更新观测。(FR-018)

## U4 增补校验

- **C-004** 表达类特性线的 U4 MUST 在既有四条件（哨兵、产物、纪律、记账）之外增补四项**全部 blocking**的校验：
  (a) 本阶段**在门禁 owner 阶段算子表中登记的 blocking 行**各有一条结果记录，且无 `not-evaluated`——计数分母 MUST
  只取该表（表达类 implement 为 1 行，即 `G-implement-structure`；四个 CLI 门禁面 MUST NOT 各自被当作算子重复计入）；
  (b) 该记录指向的证据文件存在且非空——**不做哈希比对、不新增加记账字段**：既有 `gate-implement-evidence-binding`
  的 `evidence_sha256` 只约束 `verification.md` 的 SC 样本行，且其 owner 明写非 `pass` 判定不承担绑定义务；
  verdict 只由 (a) 读记录取得，MUST NOT 由「文件存在」反推；
  (c) 载荷类别与 U4 当场解析值一致，不一致判派发构造缺陷；**且载荷 `error` 位非 `-`（即 `owner-unavailable`）时
  MUST 走 `owner-unavailable` 分支**——记一条降级观测、保持既有执行类门禁集，MUST NOT 按表达类四项校验，
  也 MUST NOT 当作「作者未声明」放行；(d) 本阶段的 `stage-status` 行在场。(FR-019)

- **C-005** 哨兵与产物具备而门禁证据缺失时 MUST 判未完成，MUST NOT 以「产物看起来对」放行；MUST NOT 派发下一阶段。(FR-019)

## 两槽位内容

- **C-006** 表达类特性线的两槽位 MUST 换为两个文档门禁槽位，时点不变（implement 起点 `baseline`、review 通过后
  `closure`），槽位记录 MUST 落在既有状态脊围栏内。`selection_basis` MUST 取 `docs-gate-full`；`command` MUST 记
  该次文档门禁的命令串（一次四面调用 `--action verify --faces reader,evidence,duplicate,count` + 结构子步
  `--action structure --spec-dir <dir> --path <落文>`；站点层存在时加构建算子）；`rc` MUST 是该命令串的**聚合退出码**——
  逐命令取非零优先（任一非零则非零，全为 0 才 0），逐命令原始 rc MUST 记在 `evidence_ptr` 指向的门禁输出里，
  MUST NOT 为此新增聚合脚本（接线面封闭）。(FR-020)

- **C-007** `passed` MUST 记 verdict = `pass` 的 blocking 算子数；`failed` MUST 记 verdict ∈ {`fail`, `not-evaluated`}
  的算子数；**`not-applicable` MUST 单列**——MUST NOT 计入 `passed`、MUST NOT 计入 `failed`（与
  `shared/workflow/expression-gates.md` § 结构/链接/构建「不得记为通过」一致），其条数 MUST 从 `evidence_ptr` 指向的
  门禁输出读出，且「算子总数 − (`passed` + `failed`)」MUST 等于该条数（U4 校验该等式）。closure 的 `baseline_compare`
  MUST 是算子 id 集合的**名称级**差集。逐面的 `not-evaluated` 原因 MUST 写在 `evidence_ptr` 指向的门禁输出里，
  MUST NOT 并入 `passed`，MUST NOT 以 0 表示未运行。(FR-020)

- **C-008** 槽位 MUST NOT 静默跳过，MUST NOT 在未运行时写槽位行。槽位数、时点、槽位顺序、closure 名称级差集与
  `audit-test-budget.py` 的判定 MUST NOT 改变；非槽位阶段的定向集记录义务不因类别免除——仅文档改动亦 MUST 留
  `stage-status` 行。(FR-020)

## 不变量

- **C-009** 驱动 MUST NOT 因类别改变阶段序列、哨兵字面量、watcher 判定与退出码、卡死处置、快车道判据或
  analyze / review 调用率。类别只改变两件事：用哪套算子证明同一不变量、预算槽位里装什么。(FR-021)

- **C-010** `analyze` 与 `review` 的调用率 MUST 保持 100%；任何以「本线属表达类」为由跳过、缩短或改判阶段的请求
  MUST 被拒绝。(FR-021, FR-025)

- **C-011** 本特性 MUST NOT 回退 069 的 `Implemented` 状态、MUST NOT 改写其正文或其切片规格；承接关系 MUST 记录在
  `features/077.md` 与 requirements § Related Feature，MUST NOT 反向写入 069 的详情文件。(FR-025)
