# 00 · 跨会话通用经验与踩坑

> 从 15+ 个开发会话中反复出现的经验沉淀。这些坑与约定与具体功能无关,几乎每个会话都会遇到,是本项目"最该先看"的一页。

## 一、镜像同步:改一处必改多处

本项目存在大量"同源不同路径"的镜像文件,**只改源不改镜像会导致运行时行为与源码不一致**,是最高频的返工来源。

| 源(权威) | 运行时镜像 | 说明 |
|-----------|-----------|------|
| `templates/` | `.specify/templates/` | 模板改动必须双写 |
| `skills/<name>/` | `.specify/skills/<name>/` | **两者都是独立 git 副本,不是 symlink**;改完用 `diff -rq` 或目录树 md5 校验字节一致 |
| `templates/commands/<cmd>.md` | `.claude/commands/speckit.<cmd>.md`、`.github/prompts/*.prompt.md`、`.qoder/commands/*.md` | 运行时命令 = 源模板去 frontmatter + 路径重写(`templates/`→`.specify/templates/`),约 25 行差异;各工具一份,需分别改 |

- `.github/skills`、`.github/agents` **才是** 指向 `.specify/` 的 symlink;而 `.specify/skills/`、`.specify/agents/` 本身是实体副本。
- `.venv/.../site-packages/specify_cli/skills/...` 是安装构建产物(非 git 跟踪),装包时重生成,**不要手改**。
- 改完 skill/agent 后无需登记——instructions.md 的 Resource Registry 已于 2026-08-17 退役（发现机制=目录扫描，说明见 `.specify/skills.md`/`.specify/tools.md`）；跑 `python3 scripts/python/sync-mirrors.py --write` 落镜像即可。

## 二、脚本名是复数:`create-new-requirements.sh`

命令模板里多处写成单数 `create-new-requirement.sh`,**实际文件是复数** `create-new-requirements.sh`。几乎每个走 `/speckit.requirements` 的会话都先跑错一次。**运行任何脚本前先确认真实路径**,不要照抄模板里的名字。

## 三、root 属主的目录/文件不可写

容器环境里,`mkdir` 出的目录(如 `docs/summary/`、`docs/team/`)以及 `.specify/agents/`、部分 guide 目录会变成 **root 属主**,当前用户无法写入或删除。表现:写文件报权限错、`rm` 交互式确认或失败。处理:重建为当前用户属主(755/644),或经 Docker 修复 ownership 后再操作。

**延伸到镜像文件**:同一成因会让 `sync-mirrors.py --write` 逐文件失败。下面这条来自 `.specify/instructions.md` 的常驻节,2026-09-20 按 Route R2 迁入本节(原文逐字保留,便于与旧快照对照):

- Container dirs created via `mkdir` can become root-owned and unwritable — recreate as current user before editing. This extends to **mirror files**: root-owned leftovers under `.specify/` make `sync-mirrors.py --write` fail per file — the engine now collects failures, keeps syncing the rest, and exits 1 with a `FAIL` summary (`sudo chown -R $USER <dir>` then re-run); a green-looking pass with stale mirrors is the defect this guard exists to prevent.

同类还有 **git 对象库**:见 § 二十(root 属主的 `.git/objects/<xx>/` 桶阻塞提交,修法与目录不同)。

## 四、Bash 工具每次是全新 shell

`source .venv/bin/activate` 等**不跨调用持久**。要么用绝对路径解释器,要么在同一次调用内 `source && cmd` 串联。

## 五、`cp` 可能被 alias 成交互模式

mirror 文件时 `cp` 被 alias 成 `cp -i`,遇到已存在目标会**静默跳过覆盖**。用 `cp -f` 或 `\cp` 绕过。

## 六、验证含 `${}` / 特殊字符的字面量别用 shell grep

用 `grep` 找 `${SKILL_HOME}/references/` 这类字面量时,`${}` 会被 shell 展开,导致误判"路径缺失"。**用 Python 精确字符串匹配**。同理 `ugrep` 的正则转义 quirk 也会造成 SC 检查假失败,改用 fixed-string 匹配。

## 七、先建测试基线,区分"基线遗留失败"与"本次引入回归"

动手前先跑全量测试记录基线(如 `375 passed / 7 pre-existing failures`)。本项目长期存在一批**与改动无关的预存失败测试**,典型是断言 `docs/usage.md`(已是空 redirect stub)、`templates/plan-template.md` 含 "Claude Code"/"Qoder" 字符串的用例,以及 `test_create_new_skill_contract`。判断回归时务必对照 baseline,别把它们误算作自己引入的。

两条配套纪律(2026-09-23 反馈消化轮补):

- **同口径才可求差**。仓库存在长期既存失败时,绝对通过数不可比;独立验证的最小充分形式是**同一条命令、同一过滤口径**跑 A/B,只对失败集的差集逐项归因。任何回归数字 MUST 标注它是全量还是过滤子集(含 `-k` 表达式)——子集数字不得当整体基线陈述。基线 MUST 记**名字**而非只记计数(`run-tests.sh --names-out` + `comm -13`),否则"零新增失败"只能靠数数考古,而计数相等会掩盖成员变化。
- **套件红先按被测单元归因**。多个同族单元被并行编辑时,先 `pytest --tb=line` 读每条断言指向哪个单元,区分既有负债与本次回归,并把归因命令与结论一起写进完成报告——只说"套件红了"等于把归因义务推给读者。owner:`skills/create-skills/SKILL.md` §6。

## 八、命名带数字的测试是脆弱信号

`test_five_official_assistants`(硬编码 5)、coexistence 测试里硬编码的 profile dict、fixture 里硬编码的工具列表——工具数从 5→6 时全线打破(`KeyError: 'codex'`)。**测试名/断言里出现具体数字,就是未来扩展会踩的雷**。

## 九、SDD 工作流的固定关卡与约定

- **Feature 绑定优先复用既有 Feature 而非新建**:many-specs-to-one-feature 模型。重构/演进类改动挂到对应已有 Feature(如 016/019/013/022)下。
- **不使 Feature 状态倒退**:给已 `Implemented` 的 feature 追加演进 spec 时,状态保持 Implemented,不回退为 Planned(即使命令模板默认描述是 Draft→Planned)。
- **Pre-Status-Flip Gate**:允许 Planned→Implemented 的门禁 = 零 `[ ]` 开放任务 + 每个成功标准(SC)在 `verification.log` 有状态行。
- **Deferred 任务是一等公民**:无法在本次运行执行的(需实时跑命令、需运行时生成、需干净环境交互、需发布后数据)标 `[~]` + `<!-- deferred: reason -->`,而非留 `[ ]` 假装没做。
- **纯模板/prompt 类 feature 的 Test-First 判为 Partial(justified)**:无可执行运行时代码,"测试"改为校验模板内容指向正确 canonical 路径 + 结构化验证 + reference-session,pytest 判 N/A。
- **`tools: []` ≠ 省略 `tools`**:前者=纯对话无工具,后者=继承平台默认(全工具)。给 agent 全权限应**省略** `tools` 字段。

## 十、批量文件生成用并行 subagent

多份文档/文件(如 8 份 references + 4 份 SKILL.md、3 个独立 skill 目录)彼此独立时,用并行 subagent 生成,主流程边等边标记任务。注意**并行 subagent 有配额上限**,过多需分批启动(如 7 个分 4+3)。

## 十一、编辑注册表(Registry)时小心 copy-paste 串行(已随 Registry 退役)

往 `.specify/instructions.md` 的 Skills/Agents 表写新行时,容易误改到相邻行(如把 git-workflow 的 Canonical Path 改错)。写完回查该表。*(2026-08-17 起 Registry 已退役,本条仅作历史参考;同理适用任何机器维护表格的手工编辑。)*

## 十二、验证命令"绿"不等于"证明了命题"(盲检类)

本项目最贵的一类缺陷:一个检查跑完给出了输出(空集 / `EXIT=0` / `1 passed`),但那个输出**不是关于它被写来判定的那个命题**的。看着绿的假通过比红着更贵——红会被人修,绿会被下游当证据引用。

写完任何断言**负面命题**(某物不存在 / 未变化 / 未泄漏 / 未悬空)的检查后,先自问一句:**被守物真的坏掉时,这条会不会变红?** 答不上来就是没写完。

已实测到的四种成因(均来自特性 051 与其前置的 analyze 整改):

1. **命令的输出形态与后续过滤不匹配**。`git diff --stat … | grep -E '\.(py|sh)$'` 恒零命中:`--stat` 的行尾是变更直方图、长路径还被省略成 `.../name`,任何按路径的正则都碰不到它。实测在 6 个提交、16 个真实新增 `.py` 上命中数恒为 0。改用 `--name-only`。
2. **比对基线在 CI 里恒等于被比对象**。`git diff HEAD` 比较工作树与 HEAD;CI 是洁净检出,工作树恒等于 HEAD ⇒ "断言其输出为空"**无条件通过**,不论本次改了什么。中途运行的门禁 MUST 以开工时冻结的**字面 SHA** 为基线。
3. **命令的可达范围小于命题的范围**。`git diff <sha>` 只达**受跟踪**路径,而特性自己的制品在 Phase 边界提交前全是未跟踪的,于是"本特性新增了哪些可执行脚本"这个问题在唯一能起作用的窗口内看不见任何答案(一个新增的 `.sh` 会被静默放过)。修法:并入 `git ls-files --others --exclude-standard`。
4. **断言瞄准了错误的树**。指针文本写的是运行时副本 `.specify/shared/guidelines/<name>.md`(读者解析的就是它),而守卫去校验框架源树 `shared/guidelines/<name>.md`。本仓两棵树都在,故二者偶然同真;下游项目只有运行时副本,于是该守卫对**它被写来防的那一种失效**结构性不可见。实测:移走运行时副本后该用例仍报 `1 passed`。这是「两顶帽子」陷阱(见 AGENTS.md 同名节)在测试侧的变体。

**实现期新增的两种成因(Feature 052,2026-09-23)**:上列四种之外的同族形态,一并归入盲检类。

5. **选择器按子串工作,却被当作按标识符工作**。`pytest -k` 的每个 token 按**子串**匹配测试 id,且**同时匹配 slug**:裸 `c1` 会选中 `test_c10_*`…`test_c19_*`,而名为 `test_g8_c6_c7_...` 的函数会因 slug 含 `c6_` 被另一阶段的 token 选中。实测(5 个桩)`-k "c1 or c2"` 收集 5 个,`-k "c1_ or c2_"` 收集 2 个。修法:token 一律带尾下划线、函数名一律 `test_<前缀><编号>_<描述>`(编号后紧跟下划线),并**断言收集数等于认领的条款数**——否则空选恒绿,而空选正是"分区表达式写错"的默认结果。
6. **自指哨兵被自己的诊断文本触发**。一个"扫描自身源码断言不含某禁用字面量"的守卫,若把该字面量逐字写进自己的失败消息,就会在自己的报错文案上恒红。修法:needle 由片段拼出(`"agents" + "/" + "instances"`),诊断消息改用不含该字面量的散文,并为哨兵再配一条伴生断言(源码长度非零、被扫常量仍在场)。

**消费期新增的三种成因(反馈消化轮,2026-09-23)**:同族形态,来自对 32 条历史反馈条目的核验与 16 项修复。

7. **"非空白即通过"的证据关**。渲染证明关只校验截图存在且非空白,而无头 Chrome 的布局视口比 `--window-size` 声明值矮 ~87–88px,底部被裁时该关照样绿——两个绘图引擎各自独立实测到同一差值,是本轮唯一有**两个独立报告者**的缺陷。修法:窗口高 = 内容高 + 余量,或先读回绘制 bbox 再判裁切;余量数值的 owner 是 `skills/draw-diagram/references/delivery-contract.md` D6「渲染证据几何」行,其余处只写指针。
8. **A/B 两侧对 git-ignored 路径天然不对称**。worktree 不复制被忽略的文件(运行工作区、构建产物、本地缓存),于是差集里混进环境差异,被记成改动效果(假阳)。修法:差集项归因前 MUST 先排除 ignored 残留。
9. **用过滤后的视图当作内容命题的证据**。要断言一个工件的内容,就读那个文件本身;`git diff -- <path>`、`grep -A/-B`、`--stat` 只呈现被筛过的子集,其形状与被筛集合并不匹配(即上面第 1 条的一般形态)。用它取证等于让过滤器替你决定什么算证据——diff 用来定位改动范围,文件用来判定内容命题。

**两个配套手法**:

- **变异演练(mutation drill)**:凡守卫负面命题的用例,取证 MUST 含一次「把被守物弄坏 → 确认变红 → 复原 → 确认恢复绿」的实跑,而不是只看它在当前树上通过。"今天绿"只证明当前树没问题,不证明该用例能发现问题。演练用的临时文件 MUST 删净并复核(计数归零)。
- **反空转哨兵(anti-vacuity sentinel)**:凡断言"过滤后的集合为空",在同处再断言一个**必须非空**的伴生量,使"空因为对"与"空因为盲"可区分。实例:断言"新增可执行脚本集为空"的同时,断言"本特性自己的测试文件出现在新增集里"——正是这条哨兵在首次运行就抓出了上面第 3 种成因,一次回本。

## 十三、`git diff` 取"本次改了什么"的三个形态陷阱

同一条命题("本特性没有碰 X")在三种写法下分别**过严、空真、有盲区**:

- `git diff --stat <base> -- <path>` 接路径正则 → **过严到恒空**(成因见 § 十二 第 1 条)。用 `--name-only`。
- `git diff HEAD -- <path>` → 在 CI 洁净检出下**无条件空真**(第 2 条)。用冻结的字面 SHA:开工时写进基线文件,之后以 `sed -n 's/^BASE_SHA=//p' <基线文件>` 取回,不要手写。
- `git diff <sha> -- <path>` → 对**未跟踪**的新增文件是盲区(第 3 条)。并入 `git ls-files --others --exclude-standard -- <path>`。

另两条配套约束:**MUST NOT 按扩展名过滤代替按路径过滤**——`templates/plan-template.md` 是 `.md`,而 `scripts/` 下另有 70 个非 `.py`/`.sh` 的受跟踪文件,扩展名过滤会让它们结构性逃逸;**MUST NOT 在 `&&` 链里把合法结果为"零"的命令(`grep -c`、`diff -q`、`comm`、`test -d`)放在必须执行的命令之前**——`grep -c` 零命中时退出码为 1,链会静默中断,其后的提交动作根本不会发生,而检查本身还报告成功。用 `;` 或补 `|| true`,并确认链尾真的执行了。

## 十四、改既有 spec 用追加,不要重跑覆盖式脚手架

- **In-place amend ≠ re-scaffold**: `create-new-plan.sh` unconditionally overwrites `plan.md`; do NOT run overwrite scaffolding when amending existing specs. Append tasks (e.g. T032–T057) instead of regenerating, to preserve history.

## 十五、`templates/` 保持项目中立

- **Template neutrality**: keep generic `templates/` (esp. `constitution-template.md`) project-agnostic; do NOT push spec-kit-specific content into shared scaffolding. Project-specific rules belong in `.specify/memory/constitution.md` or this file.

## 十六、文档引用方向是单向的

- **Documentation reference direction is one-way**: `README.md` → `docs/tutorials/quickstart.md` → `docs/reference/commands/*.md`. Sink detail into `docs/`; keep README a lean entry point. Avoid reverse/circular references.

## 十七、删除前两步核验,AND 条件缺一不可

- **Removal safety**: before removing a dependency or deleting a file, verify it is truly unused in two steps (no code `import`, no shell invocation) and that any stated delete conditions ALL hold — when conditions are an AND, any one failing means do NOT delete.

## 十八、重命名/退役必须登记 init 回收

- **Rename/retire → register init reclaim**: whenever a command, skill, or script is renamed or deprecated, register the old name in the matching obsolete-asset registry in `src/specify_cli/__init__.py` (`_OBSOLETE_SKILLS` / `_OBSOLETE_COMMANDS` / `_OBSOLETE_TEMPLATES`, inside the `OBSOLETE-ASSET-REGISTRY` markers), extend `tests/contract/test_cleanup_obsolete_assets.py` to cover it, and remove the stale mirror directory under `.specify/skills/` (sync-mirrors never deletes). Init's additive copytree never deletes stale files, so an unregistered rename leaves dead structure in every upgraded workspace (e.g. `extension-e2e-test→browser-extension`).

## 十九、`yaml.safe_dump()` 默认把 CJK 转义成 `\uXXXX`

- `yaml.safe_dump()` defaults to `allow_unicode=False` (escapes CJK to `\uXXXX`) — pass `allow_unicode=True` for Chinese YAML frontmatter.

## 二十、root 属主的 `.git/objects/<xx>/` 桶会间歇性阻塞提交

- A root-owned `.git/objects/<xx>/` hash-bucket dir intermittently blocks commits (tree hashes land in buckets probabilistically). Root fix: `mv` the bucket aside, recreate it as the current user, copy the blobs back — do NOT mutate file content to dodge the hash.
- **提交前探测桶可写性,比一次失败提交 + 三轮诊断便宜**:`obj="$(git rev-parse --git-path objects)"`,对待写入的 hash 前缀桶 `b="$obj/<xx>"` 跑 `if [ -e "$b" ]; then test -w "$b"; else test -w "$(dirname "$b")"; fi`。桶**缺失是正常态**(git 按需创建),故必须回落父目录——裸 `test -w "$b"` 会误报。探测 MUST 在 `git add` 之前:一次失败的提交会把索引留在半写状态,诊断成本远高于一次 `test -w`。

## 二十一、重构命令/引擎必须端到端实跑其真实管线

- When restructuring a command/engine, **execute its real pipeline end-to-end** (create → view → invoke, or collect → compare) as a mandatory step — "files exist / headings present" checks miss latent defects that only surface at runtime (four such defects found in one tools restructure).

## 二十二、分区认领、渲染入口与阶段边界的三个形态陷阱(Feature 052 实现期实测)

- **一个测试文件被多阶段分区认领时,判据 MUST 写成"集合"而不是"条数"**。镜像与副本的既有漂移先于本特性存在,故判据只能是"触及的面上无**新增**成员";写成"DIFF 行数等于 N"会让一次**改善**反而判为失败——实测 `sync-mirrors.py --write --only shared` 同步的是**整个 scope**,把该 scope 的既有漂移一并治好(2 → 0),相等判据随即不成立。同族陷阱:`skills` 的 DIFF 条数改前改后都是 38,而**成员已换手**(一增一减相互抵消),只有集合比较能暴露。
- **对未知参数静默返回成功的渲染入口,其返回值 MUST 被断言**。`src/specify_cli/__init__.py` 的 `render_agents_for_tool(project_path, tool)` 对不存在的 tool 键返回 `rendered: 0` 而**不报错**;`.github/agents` 的键是 `copilot` 而不是 `github`。传错键的表现是"命令成功、副本没变",退出码与日志都不报警。凡调用此类入口,MUST 断言 `rendered > 0`(或逐一核对目标文件已变),MUST NOT 只看退出码。同类:`regen-command-copies.py` 只有全量模式,无窄作用域;而 `sync-mirrors.py --only <path>` 支持窄前缀,其文档明写该旗标的存在理由就是"避免把无关漂移拖进改动面"——两者混用时 MUST 对**每个**被编辑的源文件逐个核对其镜像已同步。
- **阶段边界不总能满足"回归差集为空"**。新建一个纪律真源文档、而其常驻指针要到下一阶段才落地时,既有的可达性守卫(`test_user_facing_comprehension_section.py::test_c11_no_dangling_guideline_pointer_on_either_instruction_surface`,其 C-11(b) 余集断言)会在这中间**合法地**变红——新文档在 `shared/guidelines/` 里,却还没有任何指令面指向它。此时 MUST 把两个阶段合成**一个**提交单元,而不是提交一个已知红的增量;归因也 MUST 写清"既不是被测物缺陷、也不是断言缺陷,而是任务排序产生的合法瞬态"。


---

**相关主题**:[[01-agent-system-evolution]] · [[02-commands-and-cli-tools]] · [[03-skills-system]] · [[04-draw-plantuml-optimization]] · [[05-docs-and-governance]]
