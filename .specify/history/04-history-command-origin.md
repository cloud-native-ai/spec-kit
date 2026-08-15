# 主题：/speckit.history 命令自身的诞生（Feature 030）

覆盖会话：03cf50d0 (2026-07-14)。本文件是该命令的设计决策记录——即产出本知识库的机制自身的"出生证明"。

## 1. 关键决策与理由

- **蒸馏策略**（用户选定）：25 个 session（~28MB JSONL）先脚本去噪（~98 万字符）再提炼；按**主题聚合**（非逐 session）存储；内容按**五维度**组织（关键决策/可复用经验/待办/交互流程/用户↔模型冲突）。
- **分派策略**：>18K 字符的 13 个大会话委派并行 subagent，6 个小会话直接读——控制上下文成本。
- **命令化两项关键设计**（用户确认两个推荐项）：
  - **Claude 先行 + 可扩展**：工具→存储解析走 `history-utils.py` 的 `STORE_RESOLVERS` 插件点；未适配工具返回 `supported:false` 诚实降级，绝不猜测存储格式盲解析。
  - **增量更新**：`.manifest.json` 记录已处理 session，重跑只处理新增。
- **运行时命令生成**：放弃手写转换规则，直接 import 生成器的 `rewrite_paths()` 复制转换；只生成 history 的 4 个文件（避免全量重刷 stale 命令出大 diff）。工具识别复用 `agent-configuration.md` Step 1 表；命令模板仿 `research.md`。
- **纠缠工作树提交策略**：pathspec 精确提交只含 history 文件；`features.md` 030 索引行与 029 行同文件无法拆分，**有意不提交**。
- Claude Code 存储编码规律：`~/.claude/projects/<编码路径>/*.jsonl`，`[/._]→-`；精确匹配项目根以排除 `--specify` 子目录变体。

## 2. 可复用经验 / 踩坑

- manifest 匹配必须用完整 uuid（`sid`），8 位短 id 不匹配导致 `pending` 不减少。
- `.gitignore` 对已暂存文件无效：`.specify/history/.work/*.txt` 曾被外部进程 add 进索引，需 `git rm --cached -r`。
- 生成器并不删除 `## Feedback` 段——runtime 命令缺该段是 stale 未重生成，非设计；`rewrite_paths()` 只重写 `memory/ scripts/ templates/ shared/`，不含 `skills/`。
- `git commit -m` 必须在 `--` pathspec 之前；用 `-F` 消息文件更稳妥。
- 并发协作纪律：他Feature 的引用改写扫描会影响新文件；并发进程可能删除你的产物（从 git 索引恢复 + 追加提交，不用 `--amend`）；提交后核对交付文件确在磁盘。
- dev 环境下 `get_canonical_command_stems()` 返回 0 是因 `get_resource_path()` 找打包资源而非仓库，非缺陷。
- root 属主坑两处：`.specify/history` 子目录（删空重建）、`.git/refs/heads/` reflog（删 root 属主 reflog 后 git 自动重建）。

## 3. 未完成 / 待办

- `features.md` 的 Feature 030 索引行当时未提交（与 029 索引行纠缠）。
- 提出 but 未做：命令 contract 测试（断言模板/脚本存在 + `locate` schema）；向 `.specify/memory/knowledge/` 写结构化条目供 memory-recall 检索。
- 其他 AI 工具的 `STORE_RESOLVERS` 实现均未落地（仅 Claude Code）——本知识库 2026-08-15 首跑时仍然如此（`supported_tools: ["claude"]`）。

## 4. 关键交互流程

- 蒸馏流水线：JSONL → 脚本剥噪 → 主题分组 → 大会话并行 subagent 五维提炼 → 主题文档 + README 索引。
- `/speckit.history` 六步：①识别工具与项目 ②`collect-history.sh` 提取干净会话 ③逐会话五维提炼（大者并行 subagent）④按主题聚合生成/合并 `.specify/history/` ⑤更新 manifest ⑥报告。
- 新命令落地清单：模板 `templates/commands/history.md` → 生成器转换产出 4 工具 runtime 命令 → 镜像脚本到 `.specify/scripts/` → `docs/commands/history.md` + `.gitignore` + Feature 登记。

## 5. 用户 ↔ 模型的冲突/分歧点

- 无（设计要点均以"推荐项 + 用户确认"方式收敛）。
