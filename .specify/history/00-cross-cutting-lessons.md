# 跨领域复现的教训（Cross-Cutting Lessons）

来源：124 个有效会话（Claude 纪元 16 个 + Qoder 纪元 108 个）中反复出现的模式。Claude 轮主题见 [[01-draw-plantuml-optimization]]、[[02-sdd-feature-lifecycle]]、[[03-framework-mechanics]]；Qoder 轮五线程见 [[05-agents-skills-tools]]、[[06-anchoring-goal-team]]、[[07-archive-history-session]]、[[08-derive-review-interview]]、[[09-memory-state]]。

## 1. 环境与工具坑（≥6 个会话独立复现）

- **`cp`/`rm`/`mv` 被 alias 成交互式**：镜像覆盖时静默跳过，且 `cp -i` 可能返回成功 → 一律 `cp -f` / `\cp`、`\rm`、`/bin/cp -f`；删除/覆盖后重跑校验，别信退出码。
- **root 属主目录/文件**：容器内 `mkdir` 建出的目录（`.specify/` 子目录、`.git/objects/<xx>/`、`.git/refs/heads/`、feedback `index.json`）可能 root 属主导致 EACCES；`mv` 重建后可能被环境回滚；可靠出路是暂存 sanctioned 临时根 + 给用户精确的 `sudo cp -f && sudo chown -R` 命令回填。root 属主文件可用"临时文件 + 同目录 `mv`"原子替换（rename 只需目录写权限）；`.git/objects` 反复被 root 写者再生成时，持久修复是默认 ACL `setfacl -R -m u:<user>:rwX -m d:u:<user>:rwX`——同内容哈希落同桶，重试无效。
- **scratch 只落 sanctioned 临时根**：裸 `/tmp`、`$HOME/.cache/`、repo-root `tmp/` 都曾违反临时目录纪律；用 `.specify/.tmp/`（或声明的 `~/tmp/<project>/`），记录后即清理。
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
- **probe/embed 编译顺序固定**：`registry 对同步 → 源侧 compile → regen → feature 作用域 sync`。引擎读 `.specify` 镜像 registry；镜像未重投影时 compile 会生成 `.specify/.specify/...` 并把"绿色"校验变成真空。（≥4 个 Qoder 会话独立复现）
- **`sync-mirrors --only` 有粒度陷阱**：`--only scripts` 是 scope 级、会拖带继承漂移；`--only skills` 对两层布局的 `skills/internal` 是静默 no-op。优先文件级 `--only`，改完全量 `--check`。
- **生成的 Wrap-up 面孔长期缺引擎参数**（`--run-id`/`--complexity`/`--review`）：跨 71→74→79 单元反复出现；修复方向是渲染从引擎 `args-manifest` 读取，不是逐次手补。
- 扁平 glob（`skills/*/SKILL.md`）在两层布局下匹配 0——测试/脚本的"全绿"可能只是没扫到。

## 3. 测试基线纪律

- 动手前跑全量并记录基线（失败数 + 具体失败集）；收尾 diff 失败集定位唯一回归。
- 长期存在的"基线失败"（usage.md / plan-template.md 字符串断言等）与本次改动无关时，正确口径是"无新增 history 相关失败"。
- 硬编码数量/名单的测试与 fixture 在扩容时全断（`test_five_official_assistants` 等）——新测试写成 count-agnostic。
- 测试**意图**质量（真空绿、自指断言、慢构造）是独立问题，见 §9；基线只保证"同集合"，不保证"测得动"。

## 4. Git 纪律（纠缠工作树中协作）

- 提交用 pathspec 精确限定（`git commit --only -- <paths>` / `-F` 消息文件）；`-m` 必须在 `--` 之前。`git add <paths> && git commit` 提交的是**整个 index**——两次实测吞入 52 / 23 个他人暂存文件；用 `git commit -m msg -- <paths>`。
- 不照搬模板的 `git add -A`；索引预暂存的他人文件会被卷入 → `git reset --soft` + 显式 pathspec 重提；不用 `--amend` 以免卷入他人已暂存内容。
- **commit message 不可信，看 diff**（`sdd-workflow` 实际加入于标题误标 "fix gitignore" 的 `0207fdf`）。
- 条件删除必须逐条验证 AND 条件（引用存在且内容非独有才可删）；历史 spec/文档中的旧路径叙述是不变历史，只修活链接。**dated 读数保值**——复算写在旁边并注明日期，绝不改写旧读数。
- **`git merge-tree` 不报告 modify/delete 冲突**——真实合并必须实跑；镜像冲突先投影源侧再 `sync-mirrors --check`。
- **并发写者先归因再信用/否定**：同树可能有其他会话/fork 在写（`trigger/index.json`、`UU→M.` 翻转、staged 快照）；按 mtime + `git log` 归因，只提交显式路径，不把别人的改动算进本次门读数。
- **未 push 的 HEAD 使可达性 UNRESOLVABLE**：报告用绝对路径 + `git show <sha>:<path>`，不伪造 URL。
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
- **用户会以授权改变规则来替代机械妥协**：082 的任务上限 40→60、`TASK_CEILING`/`TASK_MAX` 是用户裁决的框架变更；模型负责披露"用户方案 vs 现有规则"的张力，不自行折中。
- **用户的"流程没走对"是入口缺陷信号**：一次跳过 U0–U6 直接编辑的质问，最终落成 skill 的入口路由 guard（U0 声明 + 流程不可替换），而不是一次性道歉。
- **纠错可以推翻用户断言**：`docs/git-workflow.md` 声称不存在（实际存在、mode 600）、"单分支开发"与实际 trunk+短分支不符——先测量再纠正术语。
- **用户问根因时，迁移不等于修复**：`tmp/` 处置是"迁移 + 写纪律"，在用户批准前不删除。

## 8. 重命名债与机器绿的真空（Qoder 轮新增，≥6 个会话复现）

- **一次重命名会留下三类残留**：活规范文本（contracts/quickstart/data-model/tasks）、owner 面文档（framework-map、definitions、driver SKILL）、以及**断言旧根的测试**。第三类最危险：文档与测试一起陈旧时双双全绿。
- 已确认的重命名：`.specify/goal` → `.specify/anchoring`（全局树动、spec-local `goal/` 与文件名不动）、`humanize` → `humanize-conclusion`、`export-session` → `archive-session`、docs 六类重组。
- 判读规则：**活路径改正，dated 读数保值**（复算加日期注记）；`identity`（文件名/身份）与 `location`（路径）分开处理；重命名后先分类 live / dated / removed，再定有界修复波。
- 防御动作：重命名落地后全仓扫活规范与测试 pin；`directory-governance`/`framework-map` 这类"注册表测试"必须与 owner 文档同源；freeze 只覆盖一个名字，上游 merge 会在 freeze 后引入新名字。
- spec 目录号与 feature registry 号是两条偏移序列（020→006、031→032、080→062…）——这不是错配，判陈旧要按 spec 路径映射，不按编号相等。

## 9. 测试意图质量：真空绿谱系（Qoder 轮新增，≥5 个会话复现）

- **不可失败的断言形态**：`or True`、`f(x) == f(x)`、grep 自己引入的字面量、"模块存在"型形状测试、已被行为测试覆盖的 accessor 默认值。
- **假红/假绿**：`--baseline` 读错键层（violation 为空但退出 0）；"空真"被当红基线；静态验证（无法执行）被当成已执行；空 fixture 的排除测试。
- **覆盖幻觉**：扁平 glob 匹配 0、mirror-parity 家族重复、test-about-tests、completed-feature pin、parametrized 严格子集。
- **慢构造**：真实 worktree 队列、venv + `pip install -e`、`time.sleep(1.1)`、全量 subagent/driver 模拟器；审计时点名到构造，不按模块平均。
- **审计只读**：keep / rework / delete-candidate 每项带一行理由，删除与改写归 owner；审计产物（junit `tests="0"`、中途日志）不得用于通过/失败计数。
- mutation 用删除形态（子串断言对后缀追加免疫）；先 grep 标记词再断言。

## 10. 计数、登记与状态的证据纪律（Qoder 轮新增，≥5 个会话复现）

- **计数必须程序派生**：FR/SC/clause/task 数字用 `clause_extract`/validator/coverage 工具现算，绝不手写进正文或 registry；叙述计数与机械计数冲突时以机械为准（11 vs "10 Gap"）。
- **状态按证据判读**：registry `Implemented` 可以与 closure `block` 并存（090）；header 与 body 可以相反（056）；仅 requirements 也可能标 Implemented（073）。`status-unreadable` 的判读是 registry-status × closure-verdict，输入缺失时保持不可读，不补造。
- **登记在铸号那一刻**：D/OI/S/T/F/B/REC 未入 `register.md` 就是不可解释的孤儿；`register.md` hand-maintained、无引擎无 guard——"被引用但未登记"是已知漏点。
- **Feature registry 纪律**：spec 侧先、registry 后；详情文件/index 行数提交前核对；状态只前进不回退；registry 行巨大，只解析 ID/status/links。
- **基线冻结失败名集**：re-freeze 必须记账（63→21 会留下 42 个 ghost name）；pre-existing 归因要在旧 worktree 复现。

## 11. 机制不可用时阻断而非伪造（Qoder 轮新增，≥3 个会话复现）

- **机制惰性要如实报告**：豁免通道从未被 `class_deferral_marker` 消费、E-3 fact 形状被 declaration schema 拒绝（exit 2）→ G1 BLOCKED；closure-verdict 输入契约晚于 51 个 dated spec → G5 0/52 BLOCKED。正确动作是把机制决策交回 owner，不是补数据。
- **有界波次超界即停**：live bucket 153 > 150 上界时，只完成分类、0 修复 0 声称；下一波按逐条计划执行。
- **不要给"契约会自我证伪"的机制打补丁**：add-only generator 若被强改，其 pin 测试会立即证伪——在 T018/C-12 处 fast-fail 停止，把四个封闭处置选项交给用户。
- **绿是主张不是证据**：`[x]` 勾选、`Implemented` 行、"all green" 声明都必须能落到一次可复现的测量；不能时保持 `not_evaluated` / `partial` / `block`。
