# Contract — `specify migrate` 命令面

**Spec**: `requirements.md` FR-001、FR-003、FR-019、FR-022 · **Plan**: `plan.md` WP01 · **Date**: 2026-11-10

本契约固定命令面的可判定行为。处置值域由 requirements FR-014 拥有、五维语义由 FR-007 拥有，本文件只以 machine token 引用，不复述其清单。

## C-1 命令与选项（封闭集）

```text
specify migrate [--dry-run | --apply] [--workspace PATH] [--format text|json]
```

| 选项 | 取值 | 缺省 | 语义 |
|------|------|------|------|
| `--dry-run` | flag | **默认** | 只读探测并输出计划；显式传入与默认等价，供脚本自述 |
| `--apply` | flag | 关 | 进入写入模式（唯一写入授权）；archive-first 项自动执行并可由回执恢复；与 `--dry-run` 互斥 |
| `--workspace` | PATH | `.` | 目标工作区根；必须已含 `.specify/` |
| `--format` | `text` \| `json` | `text` | `json` 输出机器可读包络（C-4） |
| `--help` | flag | — | 零副作用应答（C-6） |

**MUST NOT** 提供任何形态的额外确认旗标（`--yes`、`--force`、`--non-interactive`、`--confirm` 等）；出现即契约违约（C-5）。
未声明的选项 MUST 被拒绝（非零退出，退出码 2，Typer 缺省行为），MUST NOT 落到主流程。

## C-2 前置条件

- `<workspace>/.specify/` 必须存在；否则：stderr 指名 `specify init` 为修复入口、退出 2、**零文件创建或修改**（不写回执、不建目录、不隐式初始化）。
- 工作区不含 `.specify/` 时不得把 `--workspace` 指向父目录兜底。

## C-3 结局与退出码（封闭映射）

| outcome | 条件 | exitCode |
|---------|------|----------|
| `clean` | 计划为空（干跑或 apply 均可） | 0 |
| `planned` | 干跑且存在差异项 | 1 |
| `applied` | apply 完成，且无 `refused` / `blocked` / `failed` 项 | 0 |
| `blocked` | apply 后仍存在 `refused` / `blocked` / `failed` 项（`failed` = 执行期 I/O 失败；`blocked` = 无归档路径的破坏性处置被安全网拒绝），绝不报 applied | 3 |
| `error` | 前置条件/输入错误（含非法选项） | 2 |

同一结局的退出码恒定；MUST NOT 用 0 掩盖未完成的处置。映射与 requirements FR-019 逐项对应，契约测试从 requirements 提取该表比对。`error` 不是 outcome token：输入/前置条件错误以 stderr 报文 + 退出 2 收束，不输出计划包络、不产生回执；`outcome` 的取值域为 `clean` / `planned` / `applied` / `blocked`（C-4）。

## C-4 stdout 包络

`--format json` 输出单个 JSON 对象：

```json
{
  "planVersion": 1,
  "mode": "dry-run | apply",
  "workspaceKind": "framework-source | client",
  "outcome": "clean | planned | applied | blocked",
  "exitCode": 0,
  "items": [],
  "summary": {"total": 0, "byDimension": {}, "byDisposition": {}},
  "notes": [],
  "pointers": [],
  "receipt": {},
  "receiptPath": ".specify/memory/migrate/receipts/<run-id>.json | null"
}
```

- `items` 与 `summary` 构成**确定性部分**：同一棵树重复干跑逐字节相同（稳定顺序 = 维度固定序 + target 字典序）。
- `receipt` 的易变字段（`runId`、`startedAt`、`finishedAt`、`workspace` 绝对路径）不参与确定性比较。
- `--format text`：按维度分组呈现逐项「当前态 → 期望态 + 拟处置 + 依据路径」，末尾给出结局与下一步提示；同一信息量，不省略任何 item。
- 干跑：`receiptPath=null`，回执体在 `receipt` 字段（零写入）。
- apply：写入回执后 `receiptPath` 为该文件相对路径。
- 输入/前置条件错误（`error`）不输出本包络：stderr 报文 + 退出 2，无 `outcome` 键、无回执。

## C-5 确认门（命令面部分）

- `--apply` 是唯一写入授权；本命令不提供第二把钥匙，也不提供 `--yes` / `--force` / `--confirm` / `--non-interactive` 等确认旗标。
- 破坏性处置 MUST archive-first：原件先复制进逐运行归档根，回执逐项记录 `recover` 路径；因此这些处置是可逆动作，交互与非交互环境都自动执行，不抛出确认提问。
- 没有归档路径的破坏性处置 MUST NOT 自动执行：执行器安全网将其判为 `blocked`，结局 `blocked`、退出 3。
- 破坏性/不可逆动作的判据与清单 owner 是 `.specify/shared/guidelines/confirmation-gates.md`；本契约不复述。

## C-6 接口契约（宪法 XXI 面）

- `specify migrate --help`：零副作用（不写文件、不探测工作区、不弹确认），退出 0。
- help 文本 MUST 声明四类结局及其退出码（C-3），使下游项目无需本契约即可判定脚本行为。
- 未声明选项：退出 2 + 可识别错误信息。
- 本命令为 CLI 子命令（非独立 `*.py`/`*.sh` 脚本），不进入 `script-interface-check.py` 的必答集合；引擎保持进程内库形态。

## C-7 不变式（测试断言）

1. 干跑对工作区文件树哈希零变化（含 `.specify/.tmp/`、回执目录、归档目录）。
2. `--apply --dry-run` 同时出现 → exit 2，零写入。
3. `items[].disposition` 落在 FR-014 的封闭域内（测试从 requirements.md 提取 token 比对）。
4. 不存在确认类旗标（C-5）：对 `--yes`、`--force`、`--non-interactive` 逐个断言 exit 2。
