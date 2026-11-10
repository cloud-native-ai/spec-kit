# Quickstart — /speckit.migrate 一次性迁移收尾

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Contracts**: `contracts/` · **Date**: 2026-11-10

本页给出用户视角的四段旅程。**执行状态声明（逐例生效）**：本命令已随仓库源码实现并注册为 `specify migrate` 子命令（截至 2026-11-10 已安装的 0.0.22 发行版不含该命令）。场景 1–5 已于 2026-11-10 以仓库源码调用形态（`PYTHONPATH=src python3 -c "...; from specify_cli import main; main()"`，见 `notes/quickstart-run.md` § Execution form and disclosure）真实执行，逐例的原始输出与退出码记录在该文件（driver `all_pass=True`）；各例仍由下列钉住测试与契约共同约束。凡标记「已实测」的命令均在 2026-11-10 本 worktree 执行并粘贴真实结果。

## 场景 0 — 准备一个真实项目（前置条件，已实测）

```bash
mkdir -p ~/tmp/speckit-migrate-quickstart
cd ~/tmp/speckit-migrate-quickstart
specify init demo --ai claude --script sh --no-git --ignore-agent-tools
echo $?
```

实测（2026-11-10，在 `~/tmp/speckit-migrate-quickstart/` 内执行）：退出 0；`demo/.specify/` 含 `agents constitution.md features features.md memory scripts shared skills source.json templates tools.md workflow`，`.specify/source.json` 存在。该临时树已由文末清理步骤删除（本页只在删除前主张其内容）。

## 场景 1 — 已最新：干跑即 clean（已实测：仓库源码形态，测试钉住）

```bash
specify migrate --workspace demo
echo $?
```

预期：输出「无差异」计划；**退出 0**（`clean`）；工作区文件树哈希不变；不产生回执文件。

**前提清单（实现后必须重测）**：`--workspace` 与 `--dry-run` 缺省语义如 `contracts/migrate-cli.md` C-1；退出码映射如 C-3；已最新工作区由 `tests/fixtures/migrate-097/builders.py` 的 `build_latest_project` 生成（等价于场景 0 的 init 产物）；零写入断言如 C-7 不变式 1。
**钉住测试**：`tests/integration/test_migrate_us1_converge.py`。

## 场景 2 — 旧版项目：审阅计划 → 应用 → 再跑 clean（已实测：仓库源码形态，测试钉住）

```bash
# 1) 默认干跑，零写入
specify migrate --workspace legacy-demo --format json
echo $?

# 2) 审阅后应用（交互终端下会出现一次单批确认；拒绝则破坏项 blocked）
specify migrate --workspace legacy-demo --apply

# 3) 收敛后复检
specify migrate --workspace legacy-demo
echo $?
```

预期：第 1 步退出 **1**（`planned`），逐项列出维度/当前态/期望态/拟处置/依据路径；第 2 步退出 **0**（`applied`），回执落 `.specify/memory/migrate/receipts/<run-id>.json`，归档落 `.specify/archive/migrate/<run-id>/`；第 3 步退出 **0**（`clean`）且零写入。

**前提清单**：`legacy-demo` 由 `build_legacy_project` 生成（构造只取自 FR-005 钉名的声明：`_OBSOLETE_*`、旧代 git-workflow 状态文件、`.specify/tools/`、平铺 internal 残留、旧锚点布局、一个缺失/被改的框架文件、一个缺失链接）；五项维度各有差异项；干跑哈希不变；第二次 apply 无二次搬移。
**钉住测试**：`tests/integration/test_migrate_us1_converge.py`、`tests/integration/test_migrate_us3_crossversion.py`、`contracts/migrate-engine.md` C-8。

## 场景 3 — 无交互环境：破坏项 blocked，可逆项照常（已实测：仓库源码形态，测试钉住）

```bash
specify migrate --workspace legacy-demo --apply < /dev/null
echo $?
```

预期：不出现确认提问；破坏性项（替换/移动/归档）零执行并标 `blocked`，可逆项（缺失文件补齐、链接建立）照常执行；**退出 3**；回执 `outcome=blocked` 并写明未执行原因。

**前提清单**：非交互判定以 stdin 非 TTY 为准（`contracts/migrate-cli.md` C-5）；不存在任何非交互确认旗标（`--yes` / `--force` / `--non-interactive` 均 exit 2）；归档缺失即测试转红（FR-024）。
**钉住测试**：`tests/integration/test_migrate_us2_safety.py`。

## 场景 4 — 冲突与中断（已实测：仓库源码形态，测试钉住）

**冲突**：锚点迁移目标已被占用且内容不等价。干跑 `specify migrate --workspace legacy-demo` 以 **`planned`（退出 1）** 列出该 `refuse` 项并指名两个候选（现状文件、期望目标）；随后 `specify migrate --workspace legacy-demo --apply` 拒绝覆盖、结局 `blocked`、**退出 3**。不覆盖、不择一胜出。

**中断续跑**：在「对象已归档、目标尚未写入」处中断应用；再次执行 `specify migrate --workspace legacy-demo --apply` 时报告中断阶段（回执 `status=running` 与 `resumedFrom`），完成收尾，归档对象不被二次搬移（计数与存在性断言）。

**前提清单**：冲突夹具 = 旧锚点 + 已存在的 `.specify/features.md`（内容不等价）；中断夹具 = 应用后人为删除目标、保留归档与 `status=running` 回执；续跑语义如 `contracts/migrate-engine.md` C-7；`refuse` 语义如 C-3。
**钉住测试**：`tests/integration/test_migrate_us2_safety.py`、`tests/integration/test_migrate_us3_crossversion.py`。

## 场景 5 — 代理会话：`/speckit.migrate`（已实测：仓库源码形态，测试钉住）

在代理会话中调用 `/speckit.migrate`：模板先运行干跑计划并呈现，得到用户同意后调用 `--apply`；两个入口在同一棵树上的计划逐项一致；非交互执行环境下模板如实转述 `blocked`，不宣称成功。

**前提清单**：模板只含 `specify migrate` / `specify migrate --apply` 两条命令面、无任何检查实现（`contracts/migrate-template.md` T-2）；等价性比较对象的确定性部分为 `items` + `summary`（`contracts/migrate-cli.md` C-4）。
**钉住测试**：`tests/contract/test_migrate_template.py`、`tests/integration/test_migrate_us4_equivalence.py`。

## 清理（已实测）

```bash
rm -rf ~/tmp/speckit-migrate-quickstart
```

实测（2026-11-10）：删除后目录不存在，本页示例不残留临时项目。
