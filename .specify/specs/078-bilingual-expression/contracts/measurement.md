# Contract: 成功标准测量（Measurement）

**Feature**: 078-bilingual-expression
**Spec**: [requirements.md](../requirements.md)（SC-001…SC-005 与其 Measurement Sources 为判据 owner，本契约钉测量程序，不复述 SC 正文）

## SC-001 复制位置数 = 0

- **C-001** 关键词表 MUST 由程序机械派生：读取 [[STR-001]] 的四组枚举列表项（`owner-document.md` C-002 的列表形态），逐项取字面量构成关键词表；关键词表 MUST NOT 手写。检索范围：`shared/`、`templates/`、`.specify/`（排除 `.specify/specs/` 与 `.specify/history/`），与需求基线同口径。(SC-001)

- **C-002** 命中行 MUST 排除两类后计数：(i) owner 文档自身（[[STR-001]]）；(ii) 含 owner 路径指针的行（「路径 + 锚」引用形态，One Source of Truth 合法消费面）。其余命中即复制位置。交付日冻结快照（E7）：逐关键词命中清单落 `test-evidence/`，文件级清单随 SC-001 Source 留档；判定在 review 阶段执行一次。(SC-001, FR-001)

## SC-002 新写内容合规率 100%

- **C-003** 测量 MUST 用检查器 `scan --scope changed`（`contracts/checker.md` C-010）：输入 = 本特性全部提交相对 stage base 的改动路径并集；分母 = 改动路径上的信号行数；分子 = 其中零 finding 的信号行。全量扫描的存量输出只进入 E6 差异清单，MUST NOT 进入合规率分母。每个交付里程碑后各测一次（SC-002 Source）。(SC-002, FR-016)

- **C-004** 评审面复核抽样 MUST 存在且独立：`/speckit.review` 评审面从改动路径信号行中抽样复核检查器判定（抽样行数 ≥ 10 或全量若 < 10），抽样选择 MUST 由程序给出（每隔 k 行取 1，k = 行数/10 上取整），MUST NOT 由评审自选；复核分歧逐条登记到 review 产物。(SC-002 Source)

## SC-003 下游 ambient 实测 ≥ 1

- **C-005** 测量 MUST 在临时目录（受认可临时根，`.specify/.tmp/` 或 `mktemp -d` 于系统临时区并在用后即毁）对已安装框架执行 instructions 生成，断言产物含 ambient 小节且为「摘要 + 指针」形态（小节内四组枚举关键词零命中、含 [[STR-001]] 指针）。implement 与 review 各执行一次，产物检查输出落 `test-evidence/`。(SC-003)

## SC-004 追溯重写 = 0

- **C-006** 测量 MUST 对本特性全部提交做 diff 文件清单审计：除 [[STR-001]]、登记文件（`features.md`、`features/078.md`、`register.md`）、ambient 载体（`templates/instructions-template.md` 及其镜像与生成产物）、检查器与其测试、规格产物（`.specify/specs/078-bilingual-expression/`）外，既有文档的修改行数 MUST 为 0；测量命令 = `git diff --stat <base>..HEAD` 对照 FR-006/FR-016 白名单，原始输出落 `test-evidence/`。(SC-004)

## SC-005 跨文档一致性不一致处数 = 0

- **C-007** 测量 MUST 用检查器 `census` 动作（`contracts/checker.md` C-011）：总体 = 词汇表全部双语 Canonical 词条（无抽样，100% census，R-11）；范围 = owner 文档覆盖面清单内的定义面；判定 = 第二处定义的中文侧用词与 Canonical 中文侧逐字一致。单次 census 墙钟 > 60s（检查器自报）即触发 R-11 的抽样决策重开条件，重开动作登记于本契约修订。(SC-005)

## 登记面

- **C-008** 本特性产出的 durable identifier（T-001…T-004 决策张力记录、四份契约的 C- 条款号：owner-document C-001…C-009 / checker C-001…C-012 / distribution C-001…C-006 / measurement C-001…C-008）MUST 在 plan 阶段首次 coin 时登记 `.specify/memory/register.md`（指针形态：编号 → 一行含义 → 权威路径 → 状态）。(FR-017, FR-018)
