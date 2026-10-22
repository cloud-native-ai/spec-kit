# Contract: 兼容性与安全边界（Compatibility & Security Boundary）

**Feature**: 068 | **FR served**: FR-015 ~ FR-019 | **Scope**: 三腿横切

- **C-24** 零自动传输（子句拆分保留）

- 打包（用户手动触发）、接收（用户已投递包的本地解出）、汇总（用户显式动作）
  全部纯本地执行；三腿 MUST 零网络操作（FR-016）。
- 059 FR-011「结构性排除于反馈打包」子句的修订仅限**手动触发打包**腿；「排除于
  一切上送路径」子句原样保留——任何流程 MUST NOT 将记录传送到任何外部目的地
  （FR-016，零整条放宽）。
- 本特性零守护进程、零常驻连接、零定时器（Explicit Exclusions）。

- **C-25** 凭据零出现

- 打包产物、聚合层、汇总产物中凭据型值（API 密钥、token、鉴权头）MUST 零出现
  （FR-015）。依据：记录在采集侧已经 059 遮蔽（D9 端点白名单 + D9 凭据形态
  掩码，`exec-quant.py:110-119`），载荷只携带已遮载数据；068 三腿不新增采集面、
  不削弱遮蔽与封顶。
- 验收形态（SC-005）：对产物 zip、`aggregated/` 目录、汇总产物分别执行凭据型
  变量名/形态扫描，命中计数 = 0。
- 引用组：(FR-015)

- **C-26** 既有引擎行为零回归

- feedback 引擎既有动作 record / list / status / dispose / mark-submitted /
  reindex / cleanup / upstream / migrate-legacy / introspect-register /
  args-manifest：语义、参数、输出零变化（FR-017）；`package` 仅按 C-PL 扩展，
  其 feedback 条目处理语义不变。
- exec-quant 引擎既有动作 collect / list-records / score / collect-dispatch /
  args-manifest：语义零变化（FR-017）；`ACTIONS` 元组仅追加 `aggregate`。
- 判据形态（FR-018 / SC-006）：实现前冻结既有 feedback/exec-quant 契约+集成
  套件失败 nodeid 排序名单，实现后全量重跑、逐名比对零新增（名字级，非计数级）。
- 引用组：(FR-017, FR-018)

- **C-27** 无载荷包零差异

- 不含 `exec-quant/` 前缀的入站包：接收流程 feedback 面输出、MANIFEST 语义、
  清理与对账动作与 068 之前完全一致（FR-009）；`ingest-exec-quant` 对其返回
  零计数、exit 0、零存储写入。
- feedback 条目为空 + 载荷为空：`package` 行为与 068 前一致（不产包，显式说明，
  C-8）。

- **C-28** 版本/布局/形态容忍

- 打包与接收 MUST 同时容忍：逐条 `records/` 目录与遗留 jsonl 流、schema v1/v2、
  `{value, provenance}` 与裸 `[[STR-002]]`（FR-007 / A4）。
- 未知新字段原样保留进聚合层（零丢弃）；未知形态按未测处理；零版本号硬编码
  （Edge Cases）。
- 遗留单体流只读回退，永不重写（并发开发安全纪律既有约束）。

- **C-29** 确认门零新增

- 三腿全部为可逆动作（只读 + 派生新文件），零阻断式确认门（Explicit Exclusions /
  确认门治理：可逆动作自动执行 + 执行报告）；任何退出开关只能是非阻断可选参数
  （clarify A1 裁决固化）。

- **C-30** 存储分界

- exec-quant 载荷记录零条混入 feedback store（FR-006）；聚合层只存在于
  `exec-quant/aggregated/`；两 store 的清点口径互不引用。

- **C-31** 文档与镜像同步顺序

- 改动先落框架源（scripts/、skills/internal/、templates/commands/、shared/、
  docs/），再 `sync-mirrors.py --write` 同步镜像；MUST NOT 手改 `.specify/`
  运行时镜像（两顶帽子，宪法 XI；C-PL/IN/AG 的 file scope 均以框架源为编辑对象）。
- Mirror 对以 `scripts/python/sync-mirrors.py MIRROR_PAIRS` 为准；plan.md
  § Mirror Obligations 表为逐文件权威清单。
