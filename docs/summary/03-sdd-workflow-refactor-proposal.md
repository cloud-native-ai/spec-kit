# 提议：把 `sdd-workflow` 从「技能」重构为「共享参考目录」

> 本文评估一个提议：`sdd-workflow` 用「技能」实现不合适，应改为**安装前 `share/workflow`、安装后 `.specify/share/workflow`** 的共享知识目录，在 `init` 时拷贝到目标位置，供整个 speckit 命令与技能引用。

## 1. 背景：`sdd-workflow` 是什么、何时/为何加入

- **加入时间**：2026-07-10，提交 `0207fdf`（提交信息误标为 "fix gitignore"，实际引入了整个技能：`SKILL.md` + 8 个参考文档，共 11 文件 +925 行），次日 `09ea0bf`（"chore: upgrade specify … sdd-workflow shared skill"）继续完善。看起来是随 `specify` 批量升级/同步引入，而非专门的 feature 提交。
- **加入原因**（`SKILL.md` 自述）：作为 `/speckit.*` 命令的**共享知识库 / 去重层**——把公共协议（`$ARGUMENTS` 处理、feature 集成、agent 配置、clarify 分类、DfX 目录、ignore 模式、tool 定义等）放一处，命令用 `See ${SKILL_HOME}/references/<file>.md` 按需加载，从而**避免在每个命令里重复公共逻辑**。

## 2. 评估结论：诊断成立 —— 它本就不是一个「技能」

提议的**诊断是对的**，证据充分：

- `SKILL.md` 自己写着 **"This skill is NOT invoked directly."**——而技能的契约是「**模型可调用的能力**，靠 `description` 触发调用」。`sdd-workflow` 没有任何这种行为，只是被动的参考文档束，借技能的安装/镜像管线把文件塞进 `.specify/`。
- 由此产生的真实代价：
  - 它**出现在可调用技能清单里**，agent 有可能**误调用**它；
  - 污染 **CLAUDE.md 的 Skills 注册表**与技能命名空间；
  - 被**软链**进 `.github/skills` 和各 `.<agent>/skills`，被每个工具的技能发现当成真技能；
  - 对维护者概念混淆（「这到底是技能还是文档库？」）。

**所以把它移出 `skills/` 是正确方向。**

## 3. 对提议方案的评估：可行，且与现有安装模型一致

`share/workflow`（源）→ `.specify/share/workflow`（安装），在 `init` 时拷贝——这与现有每个核心资产完全相同的 **源 → `.specify` 模式**（`memory/`、`scripts/`、`templates/`、`skills/`、`agents/`）。概念新颖度低，且干净地消除了「伪技能」。**予以认可**，并附两点细化建议。

## 4. 改动面（明确成本）

| 区域 | 需要做什么 |
|------|-----------|
| **源码树** | 把 `skills/sdd-workflow/references/*` 移到 `share/workflow/*`；删除 `sdd-workflow` 技能目录 |
| **Wheel 打包** | `pyproject.toml` 的 `[tool.hatch.build.targets.wheel.force-include]` 增加：`"share" = "specify_cli/share"`（与现有 `templates`/`skills` 并列） |
| **CLI `init`** | `src/specify_cli/__init__.py`（约 1118 行、scripts/templates 拷贝附近）新增拷贝块：`resource_path/share` → `.specify/share` |
| **保留策略** | 把 `.specify/share` 加入 `_CORE_SPECIFY_ASSETS`（第 308 行），使重复 init 不覆盖 |
| **路径改写** | `_rewrite_paths`（约 680 行）新增规则：`share/` → `.specify/share/`（仿照 memory/scripts/templates） |
| **引用改写** | 把 **约 100 处** `sdd-workflow` 引用（源里约 50 处在 `templates/` + `skills/`，其余在自动再生的 `.specify/` 镜像）从 `skills/sdd-workflow/references/...` 改为 `share/workflow/...` |
| **注册表/文档** | 从 CLAUDE.md 的 Skills 表与技能计数（"20 total"）移除 `sdd-workflow`；同步 `docs/` 中提及处 |
| **发布脚本** | 检查 `scripts/` 里的打包逻辑——若按工具枚举 `skills/`，需同样纳入 `share/` |

引用改写量大但**机械**；真正的风险是**漏改**导致运行时死链——因此**终验门槛**是 `grep -rn sdd-workflow` 期望为零。

## 5. 两点细化建议

1. **命名**：`share/` 像 Unix `/usr/share`，略泛。可考虑 **`.specify/shared/`**（英文更清晰）或更具描述性的 **`.specify/references/`**、**`.specify/protocols/`**。无论选哪个，`workflow/` 子目录都好——为未来其他共享参考族留出空间。（次要，若偏好 `share/workflow` 亦可。）
2. **引用形式**：沿用现有约定——**命令模板用根相对路径**（`share/workflow/...`）交给 `_rewrite_paths` 加 `.specify/` 前缀；**技能里今天硬编码 `.specify/skills/sdd-workflow/...` 的**改成硬编码 `.specify/share/workflow/...`。**不要混用两种形式。**

## 6. 备选方案对比（为何选此方案）

- **保持现状**：最省事，但语义问题与误调用风险仍在。**否决。**
- **并入 `.specify/memory/`**：memory 有逐文件特殊拷贝逻辑，且面向**演进中的项目知识**，不是静态共享协议。**语义不符。**
- **并入 `.specify/templates/`**：templates 已被整体拷贝（新增管线最少），但「template」≠「协议/参考」，只是把一种命名谎言换成另一种。

**独立的共享参考目录（本提议）最诚实、最可扩展。**

## 7. 建议推进方式

采纳本提议（命名可再定）。因为这是**结构性框架改动**，触及 CLI、打包与约 100 处引用，适合走 **SDD 流程**：`/speckit.feature` → `plan` → `tasks`，把「引用清扫 + 零引用 grep 验收」纳入任务跟踪，而非零散手改。

**待用户拍板**：
1. 目录命名：`.specify/share/workflow` / `.specify/shared/workflow` / 其他？
2. 推进形式：走 spec-driven feature，还是直接实现 + 零引用 grep 验收？
