# 跨领域复现的教训（Cross-Cutting Lessons）

来源：16 个有效会话中反复出现的模式（各主题细节见 [[01-draw-plantuml-optimization]]、[[02-sdd-feature-lifecycle]]、[[03-framework-mechanics]]）。

## 1. 环境与工具坑（≥6 个会话独立复现）

- **`cp` 被 alias 成 `cp -i`**：镜像覆盖时静默跳过 → 一律 `cp -f` / `\cp`。
- **root 属主目录/文件**：容器内 `mkdir` 建出的目录（`.specify/` 子目录、`.git/objects/<xx>/`、`.git/refs/heads/`、feedback `index.json`）可能 root 属主导致 EACCES；`mv` 重建后可能被环境回滚；可靠出路是暂存 `/tmp/` + 给用户精确的 `sudo cp -f && sudo chown -R` 命令回填。
- **umask 造成 `-rw-------`**：新增文件 chmod 644、脚本 chmod 755 对齐兄弟文件。
- **`.gitignore` 对已暂存文件无效**：需 `git rm --cached -r`（如 `.specify/history/.work/` 曾被外部进程 add 进索引）。
- **沙箱 exit=1 可能是环境假象**（如 `refresh-tools.sh` 缺依赖提前中止）——补齐脚本依赖再下结论。
- **Edit 前必须用 Read 工具读过文件**（bash `cat` 查看不算）；Bash 每次调用是新 shell，`source .venv/bin/activate` 不持久，需链式或绝对路径。
- **`.venv/.../site-packages/` 下的镜像是构建产物**：随包安装再生，永不手改。

## 2. 镜像双写与生成器纪律（本项目最高频返工源）

- 三层结构：canonical（`templates/` `skills/` `agents/` `shared/`）→ `.specify/` 镜像 → per-tool 命令副本（`.claude/commands/` `.qoder/commands/` 等 5+1 份）。
- per-tool 副本必须用生成器再生（`generate_commands` / `rewrite_paths()`），勿手改；qwen TOML 有 description 特例。
- 每对双写后 `diff -rq`（或 `diff -q`）校验字节一致。
- 含 `${...}` 字面量用 Python 精确匹配验证，shell grep 会展开造成假"路径缺失"。
- 命名/路径变更后全量 grep 陈旧引用：SKILL.md、references、assets、scripts、Overview 都可能残留。

## 3. 测试基线纪律

- 动手前跑全量并记录基线（失败数 + 具体失败集）；收尾 diff 失败集定位唯一回归。
- 长期存在的"基线失败"（usage.md / plan-template.md 字符串断言等）与本次改动无关时，正确口径是"无新增 history 相关失败"。
- 硬编码数量/名单的测试与 fixture 在扩容时全断（`test_five_official_assistants` 等）——新测试写成 count-agnostic。

## 4. Git 纪律（纠缠工作树中协作）

- 提交用 pathspec 精确限定（`git commit --only -- <paths>` / `-F` 消息文件）；`-m` 必须在 `--` 之前。
- 不照搬模板的 `git add -A`；索引预暂存的他人文件会被卷入 → `git reset --soft` + 显式 pathspec 重提；不用 `--amend` 以免卷入他人已暂存内容。
- **commit message 不可信，看 diff**（`sdd-workflow` 实际加入于标题误标 "fix gitignore" 的 `0207fdf`）。
- 条件删除必须逐条验证 AND 条件（引用存在且内容非独有才可删）；历史 spec/文档中的旧路径叙述是不变历史，只修活链接。
- 多数特性会话最终 commit 未 push 远端 —— push 属独立显式动作。

## 5. 依赖/引用移除的安全法

- 穷举所有引用形态再判定：env 变量、source 行、import、shell 命令调用、模板示例列表项；全部为零才可删。
- 条件式 source 看似无害，配套强制 `check_dependency` 才是真阻断点——两者一起审查。
- 修悬空引用先全仓扫同类（feedback 记 1 处实扫出 2 处）；禁止为补齐文档编造不存在的运行结果。

## 6. 多 Agent 编排经验

- 指南作为共享状态的闭环有效：optimize 改指南 → draw 重读最新指南 → score 评分循环。
- 单一评分器波动 ±2-3 分，单轮回退勿过度反应，看趋势；建议多评分器。
- 评分标准（rubric）先于第一轮固定（基线渲染 + 期望元素 checklist），否则多轮不可比；美观向 rubric 会系统性压低语义正确图，须随目标演进。
- 设计优化策略前先探测可用工具链，不围绕环境中不存在的能力（无 dot / 无 Playwright）设计方案。
- Stop hook 按字面条件执法："实质达标"申辩无效，必须真满足数值条件。

## 7. 用户↔模型分歧的稳定模式

- 用户推动更深语义/更严验证/更彻底清理；模型默认保守局部迭代。多轮中被用户纠正后落地的方案（语义布局规划、default-on、四层产物结构、全项目引用扫描）事后均被验证正确。
- 用户报告的归因可能错误（"init 覆盖 instructions"实为 generate-instructions.sh）——先追查所有写入路径再修。
- 执行前核查用户前提（"把重构更新进 skills"时两 skills 已含内容）——前提不成立时暂停陈述矛盾，勿在错误前提下覆写。
