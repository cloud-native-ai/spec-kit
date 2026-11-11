# 债务审计 D5 — scripts / templates / workflow / skills / agents / teams / anchoring / shared / 根层文件

- **审计席位**：SDD Debt Governor（只读；唯一写入 = 本报告）
- **审计日期**：2026-11-11（HEAD `733ac70e8f3efd44d232425b660d003f9eb28dad`）
- **范围**：`.specify/scripts/`、`.specify/templates/`、`.specify/workflow/`、`.specify/skills/`、`.specify/agents/`、`.specify/teams/`、`.specify/anchoring/`、`.specify/shared/`，以及根层文件 `.specify/features.md`、`.specify/constitution.md`、`.specify/instructions.md`、`.specify/.gitignore`、`.specify/source.json`
- **不覆盖（其它域所有）**：`.specify/specs/**`、`.specify/memory/**`、`.specify/history/**`、`.specify/archive/**`、`.specify/state/**`、`.specify/review/**`、`.specify/project/**`
- **并发记录**：requested=1（本域单席位）；effective=1；effective_reason=`single-unit`（可表示单元集大小为 1，无可并发对象，见 `shared/declarations/facts/serial-reason.yaml`）
- **证据纪律**：每条发现都带路径 + 实测数字；引擎退出码与关键命令见 §5

## 0. 绑定与复核方法

按 `shared/definitions/framework-map.md`、`non-disposable-definitions.md`（处置四值 + sanitize 五值桥接）、`confirmation-gates.md`（破坏性动作门）、`one-source-of-truth.md` 执行；机械信号一律取自确定性引擎，不取自印象：

| 引擎/命令 | 用途 | 退出码 |
|---|---|---|
| `sync-mirrors.py --check` | 源↔镜像一致性（含 projected 对） | **2**（1 处漂移） |
| `sync-mirrors.py --check --only scripts` | 脚本镜像单独复核 | 0 |
| `regen-command-copies.py --check` | 每工具命令副本再生成校验 | 0 |
| `goal-utils.py list / validate` | 14 个 goal 定义枚举与校验 | 14/14 valid |
| `goal-utils.py run-checks <team>` | 20 个 team 的五项前置检查 | 见 D5-10/11 |
| `doc-consistency-check.py --faces duplicate` | shared 重复面（75 个文件） | pass（0 findings） |
| `git rev-list --count b3da3a2..HEAD` | source.json 落后量 | 240 |
| `find` / `wc` / `sha256` | 计数、尺寸、清单哈希 | — |

## 1. 基线逐条复核

| # | 给定基线 | 复核结论 | 实测证据 |
|---|---|---|---|
| B1 | `sync-mirrors --check` exit=2；唯一真实漂移=`gitignore-specify-template` 缺 `state/` 块；`--only scripts` exit=0 | **确认** | 全量输出仅 `DIFF .specify/templates/gitignore-specify-template`；源 `templates/gitignore-specify-template` 有 `state/` 块（自 L31），镜像止于 `.tmp/`；其余 6 对镜像 + 6 个 projected 对全绿；`--only scripts` exit=0 |
| B2 | projected 报告语义缺陷仍在 | **确认**（代码级） | `sync-mirrors.py:523-566` 的 `project_for()` 只回答“投影能否计算”；`:792-799` 对每个 projected 对无条件打印 `: ok`，与镜像是否等于投影无关。一个已漂移的 projected 镜像会同时出现 `DIFF[projected] …` 与 `projected[…] …: ok` 的矛盾两行；契约 C-35（`specs/089-script-interface-contract/contracts/mirror-projection.contract.md:40-47`）只要求点名 kind，测试 `tests/contract/test_script_interface_contract.py:3013-3017` 只钉住行格式，未钉住同步判定 |
| B3 | 4 个死脚本 | **修正：5 个零调用脚本** | 见 D5-04；`detect-feature-context.sh` 全仓活跃面 0 引用；`skills-utils.py` 仅测试/文档/证据引用；`common-todo.sh`、`implement-plan.sh`、`run-tests-shards.sh` 仅自引用或历史 spec/归档引用 |
| B4 | pyc 131/9.6MB（.tmp 内 117） | **修正：137/9.68MB，.tmp 119，非 .tmp 18** | `.specify` 实测；审计自身的只读引擎会新增少量 pyc，故该数是移动靶；另发现 9 个遗留 checker 沙箱 ≈129MB（见 D5-05） |
| B5 | features.md 125 行 / 241KB / 最长 14,097 字符 | **确认（精确）** | 125 行；241,145 B；最长行 = 第 60 行（Feature 051），14,097 字符；92 数据行 ↔ `.specify/features/` 92 个详情文件，双向零孤儿 |
| B6 | instructions 38,301B（余 99B） | **确认** | `wc -c`=38,301；预算 `INSTRUCTIONS_BUDGET_BYTES=38400`（`generate-instructions.sh:170`）；余量 99 B；超限仅告警不失败（脚本自行声明 advisory、恒 exit 0） |
| B7 | source.json 落后 240 提交 | **确认** | stamp commit `b3da3a2`（2026-11-10 13:42 +0800），HEAD 2026-11-11 10:25；`rev-list --count`=240（11-10：188，11-11：52） |
| B8 | regen 31⇄31 OK | **确认** | `regen-command-copies.py --check` exit=0；`templates/commands/` 31 个模板 ↔ `.claude/commands`、`.qoder/commands`、`.github/prompts`、`.opencode/command` 各 31 |
| B9 | skills 18 external / 39 internal（+seal-artifact） | **修正：18 external / 40 internal（含 seal-artifact）** | `find skills/external -name SKILL.md`=18；`skills/internal`=40；`seal-artifact` 由 099 于 2026-11-11 00:59 落地，现已在 40 内 |
| B10 | agents templates 19 / instances 3；manifest 88/88 | **确认** | 19/3；`.specify/agents/.render-manifest.json` 88 条 = 22 个 agent × 4 个宿主目录（`.qoder`/`.claude`/`.github`/`.opencode`）；88 目标全部存在且 sha256 全部匹配 |
| B11 | `.backups/qoder` 15 份被跟踪 | **确认** | 15 个 `.md`（2026-11-06），git 已跟踪，合计 68KB；与当前 19 个模板逐一比对全部 DIFFERS（均为旧版快照） |
| B12 | 8 个受跟踪 jsonl（7 队） | **确认** | 7 个团队目录下 8 个 jsonl；其中 `viz-skill-arena/items.jsonl` 为 0 B；最后提交 2026-07-30～2026-10-15 |
| B13 | 4 队无 goal、2 goal_slug 无档案 | **确认（引擎双重佐证）** | 4 队无 `goal_slug`：cws-workspace-cluster、draw-plantuml-optimizer、requirement-implement-monitor、summarize-project-optimizer；2 队 goal_slug 悬空：demo-seat-dispatch、viz-skill-arena→visualization-skill-selection；`run-checks` 对 6 队一致给出 `no-goal-definition` |
| B14 | 3 处名称漂移 | **确认（口径：goal_slug ≠ team slug）** | 088-reporting-dogfood→088-speckit-visualization；089-script-interface-contract→script-interface-contract；viz-skill-arena→visualization-skill-selection |
| B15 | 3 处 team.md 旧锚 | **确认（archive-tree 锚）** | 090/091/094 的权威定义行指向 `.specify/archive/goal-team/trees/…/goal.md`（3 处文件均存在，但活定义在 `.specify/anchoring/<slug>/goal.md`）；另查出 6 处更旧的 `.specify/goal/…` 权威行（36 行总引用），见 D5-13 |
| B16 | shared 1 条重复行 | **未复现为缺陷** | `doc-consistency-check --faces duplicate` 对 75 个 shared 文件判 pass、0 findings；唯一完全重复的正文行是 `clarify-taxonomy.md` 的 `- Append: …`（3 个 Mode 各 1 次，属分模式模板）；其余重复是 YAML 行字段（`carrier:`/`owner:` 每行一个排除项）。按“证据不可解析即 `unverified`”记为未验证，不立债项 |

## 2. 债项表（按严重度，同度按路径序）

处置词表：**ND 四值** = `archive` / `supersede` / `correct` / `exempt`（`.specify/shared/definitions/non-disposable-definitions.md` §Disposition Set）；材料卫生候选用 **sanitize 五值** = `delete` / `archive` / `repair` / `delegate` / `dismiss`（两者经该文档 §Disposition Bridge 映射，不混用）。

### P1

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | 责任 lane |
|---|---|---|---|---|---|---|
| D5-01 | 镜像漂移（CI 门禁红） | `.specify/templates/gitignore-specify-template` | 缺 `state/` 块（源 L31-L33 有；活文件 `.specify/.gitignore` 也有）。`sync-mirrors --check` 因此恒 exit=2 | P1 | `correct`（跑 `sync-mirrors.py --write`，仅这 1 个文件应变化） | 机制修复（先经 `sdd-route.py` 裁决；候选直改） |
| D5-02 | 预算濒临溢出 | `.specify/instructions.md` | 38,301 B / 预算 38,400 B，余 99 B。预算规则要求下一次增节后至少留 1,024 B（`generate-instructions.sh` 的 raise 记录），当前连一次小增节都放不下 | P1 | `correct`（按 owner 规则压缩既有节，或走文档化 raise；不得静默超限） | SDD 修复（`/speckit.instructions` Action 5） |

### P2

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | 责任 lane |
|---|---|---|---|---|---|---|
| D5-03 | 报告的语义缺陷 | `.specify/scripts/python/sync-mirrors.py:792-799`（`project_for` 见 :523-566） | projected 行 `: ok` 只表示“投影可计算”，不表示镜像等于投影；镜像漂移时会同屏出现 `DIFF[projected]` 与 `projected[…]: ok` | P2 | `correct`（判定改为 `mirror == expected`，补一条漂移变异腿测试） | SDD 修复（引擎 + contract 测试） |
| D5-04 | 零调用脚本 ×5 | `.specify/scripts/bash/detect-feature-context.sh`、`.specify/scripts/python/skills-utils.py`、`.specify/scripts/bash/common-todo.sh`、`.specify/scripts/bash/implement-plan.sh`、`.specify/scripts/bash/run-tests-shards.sh` | 活跃面（templates/commands、skills、agents、workflow、shared、src、其它 scripts）0 调用；仅被历史 specs/归档/生成清单引用。`implement-plan.sh:279-284` 调用未定义的 `json_escape`（全仓仅 `common-todo.sh` 定义 `json_escape_string`），JSON 模式运行必失败；`run-tests-shards.sh` 已被 `run-tests.sh` 内建 `-n --dist load` 取代；5 个脚本 2026-11-09/10 仍被 089 接口守卫改过（死而维护） | P2 | `archive`（archive-not-delete；先由用户授权删除/归档；若保留则先修 `json_escape`） | `/speckit.sanitize` |
| D5-05 | 运行时缓存与沙箱残留 | `.specify/scripts/python/__pycache__/`；`.specify/.tmp/script-interface-*` | `.specify` pyc 137 个 / 9.68MB（119 在 `.tmp`，18 在 scripts 缓存）；`script-interface-check.py` 中止后遗留 9 个历史沙箱（2026-11-10，≈129MB）；`.tmp` 内 root 属主条目 520 个，清理受权限阻挡（见 ANOMALY） | P2 | sanitize `delete`（可再生缓存）/ `archive` 不适用；沙箱清理需先解决 root 属主 | `/speckit.sanitize`（与 D1 的 `.tmp` 域协同；`.tmp` 总量 649MB 归 D1 计量） |
| D5-06 | 单文件超大行 | `.specify/features.md` | 241,145 B；92 数据行 ↔ 92 详情文件（零孤儿）；第 60 行（Feature 051）14,097 字符，另有 4 行 >7,000 字符。单文件注册表本身是顶层例外，但超长行是合并冲突与 token 热点 | P2 | `correct`（经 `/speckit.feature` 把行体收敛为一行指针；不改注册表单文件形态） | SDD 修复（`/speckit.feature`） |
| D5-07 | 安装基线陈旧 | `.specify/source.json` | `commit=b3da3a2`，落后 HEAD **240** 提交；`stamped_at=20261110T055525Z`。消费者：`src/specify_cli/__init__.py`（写入 / migrate 读取）与 `run-agent` 预检 | P2 | `correct`（经 `specify init`/迁移流程重盖章，不手改） | SDD 修复（setup/refresh） |
| D5-08 | 被跟踪的旧备份 | `.specify/agents/.backups/qoder/*.md` | 15 份、68KB，全部被 git 跟踪且全部与当前模板 DIFFERS（旧渲染快照）。版本历史已承担备份职责 | P2 | sanitize `archive`（授权后归档；若宿主渲染会再生成，则在源侧补 ignore 规则） | `/speckit.sanitize` |
| D5-09 | 共享追加式存储（并发热点） | `.specify/teams/{command-logic-as-classified-skills,draw-diagram-interactive,post-refactor-mechanism-integrity,skill-layer-install-separation,viz-skill-arena}/items.jsonl`；`.specify/teams/{cws-workspace-cluster,requirement-implement-monitor,viz-skill-arena}/run-log.jsonl` | 8 个被跟踪 jsonl（7 队），其中 `viz-skill-arena/items.jsonl` 为 0 B；`create-team` 技能仍把它们声明为追加式台账。与 AGENTS「记录类数据一文一件」MUST 冲突：两条分支跑同一队会写同一路径 | P2（MUST 级规则违例，但当前团队休眠、爆炸半径低） | `supersede`（create-team 改为逐条文件/派生索引；旧文件由 sanitize 归档） | SDD 修复（`skills/internal/create-team`）+ `/speckit.sanitize` |
| D5-10 | 团队无可用 goal 定义 | `.specify/teams/{cws-workspace-cluster,draw-plantuml-optimizer,requirement-implement-monitor,summarize-project-optimizer}/team.md`（无 goal_slug）；`.specify/teams/{demo-seat-dispatch,viz-skill-arena}/team.md`（悬空：demo-seat-dispatch、visualization-skill-selection） | `goal-utils.py run-checks` 对 6 队均判 `no-goal-definition`（4 无 goal_slug + 2 悬空），6 队全部无法通过运行前置 | P2 | `correct`（经 `/speckit.goal migrate` 把内联 goal 落为定义）或 `archive`（休眠队退役）；逐队裁决 | `/speckit.goal` + `/speckit.team` |
| D5-11 | 终态 goal 的壳团队 | `.specify/teams/{087-arch-diagram-docs,draw-two-layer-structure,post-refactor-mechanism-integrity,session-driven-self-improvement,skill-layer-install-separation}/team.md` | 5 队对应 goal 状态 `achieved`；`run-checks` 判 `goal-terminal` 且 `blocked=true`，团队定义仍留在活跃层 | P2 | `archive`（退役团队定义）或 `exempt`（写明理由 + 到期条件）；逐队裁决 | `/speckit.team` |
| D5-12 | 团队元数据非法 YAML | `.specify/teams/command-logic-as-classified-skills/team.md`（第 74 行流映射）、`.specify/teams/viz-skill-arena/team.md`（第 3 行 `description` 含未引号 `: `） | 两文件 frontmatter 过不了严格 YAML 解析（本审计用 PyYAML 实测失败）；行扫描式读取器仍可工作，掩盖了缺陷 | P2 | `correct`（引号化 / 修流映射） | SDD 修复（sanitize `repair` 同义） |
| D5-13 | 团队定义旧锚 | 090/091/094 三处 archive-tree 锚 + command-logic、draw-diagram-interactive、draw-two-layer-structure、post-refactor-mechanism-integrity、session-driven-self-improvement、skill-layer-install-separation 六处 `.specify/goal/…` 权威行；共 12 文件 / 36 行含 `.specify/goal/` | 活定义在 `.specify/anchoring/<slug>/goal.md`；团队文件仍宣告 `.specify/goal/`（该层已不存在）或 `.specify/archive/goal-team/trees/…`（归档树，非读取面） | P2 | `correct`（指向 `.specify/anchoring/<slug>/goal.md`） | SDD 修复（`/speckit.team`） |
| D5-14 | 无消费者的模板 | `.specify/templates/gate-template.yaml`（源 `templates/gate-template.yaml`） | 命令 / 技能 / 脚本 / src 均 0 引用；唯一提及是历史 Feature 039 文档。活载体是 `.specify/gate.yaml`（`gate-check.py` + 两处技能消费） | P2 | `correct`/`supersede`（要么在流程中接上引用，要么经 SDD 退役） | SDD 修复（先做取舍裁决） |
| D5-15 | 空层与 root 属主 | `.specify/agents/execution/scripts/`（空、root 属主）、`.specify/agents/execution/logs/`（空、root 属主） | 框架图声明 execution 层含 tracked `configs/` + `scripts/`；实际 scripts 为空（技能文档说明为 optional）；两目录 root 属主，agent 用户不可写；`.tmp` 内 root 属主条目 520 个 | P2 | `correct`（确认 optional 后保留空层或删层；`chown` 恢复可写） | `/speckit.sanitize` / 机制修复 |
| D5-16 | workflow 观察块陈旧 | `.specify/workflow/git.md`（`GIT_OBSERVED_START` 块） | 观察时间 2026-11-10T02:33:38Z，记“1 个非声明分支 `rename-anchors`”；当前本地分支为 `master`/`main`/`100-seal-slice-archive`，`rename-anchors` 已不存在 | P2 | `correct`（经 `git-utils` scope A 重新观察；不手改 managed block） | git-utils |
| D5-17 | 指令备份残留 | `.specify/instructions.md-*`（7 份） | 252KB：2026-07-11 1 份 + 2026-11-10 6 份；全被 `.specify/.gitignore` 的 `instructions.md-*` 忽略；最新一份 38,301B 与当前文件同尺寸 | P2 | sanitize `delete`（可再生；保留策略由用户定 0 或 1 份） | `/speckit.sanitize` |
| D5-18 | 生成事实与本机不符 | `.specify/instructions.md:254` | 生成物写 `Root Path: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`；本仓实际根为 `/storage/project/cloud-native-ai/spec-kit`（模板 `instructions-template.md:241` 用 `{{PROJECT_ROOT}}` 渲染） | P2 | `correct`（在本机重渲染，或声明跨主机事实） | SDD 修复（`/speckit.instructions`） |
| D5-19 | goal/team slug 分歧 | `.specify/teams/088-reporting-dogfood/team.md`、`089-script-interface-contract/team.md`、`viz-skill-arena/team.md` | 3 处 goal_slug ≠ team slug；088/089 看起来是有意命名，viz 的目标档案缺失（并入 D5-10） | P2 | `correct`（把有意分歧写成显式声明；viz 随 D5-10 迁移） | `/speckit.team` |

## 3. 治理计划（波次有序）

### Wave 1 — 机制修复（先做，无删除；每项独立门禁）

| 项 | 动作 | 可测结果 | 中止条件 | 门 |
|---|---|---|---|---|
| W1.1 | `sync-mirrors.py --write`（仅 templates 对） | `--check` exit=0；diff 仅 `gitignore-specify-template` 1 文件 | 出现第 2 个文件变化 | 直改/路由裁决（D5-01） |
| W1.2 | 修 `project_for` 报告判定 + 变异腿测试 | 漂移 projected 镜像时输出不再出现 `ok`；全绿时输出稳定 | 需改契约 C-35 文本 | SDD 运行 |
| W1.3 | `/speckit.instructions` Action 5 压缩到 ≥1,024B 余量，或按 raise 规则记录 | `wc -c` ≤ 37,376（38,400−1,024）或 raise 记录落盘 | 压缩引入语义丢失 | SDD 运行 |
| W1.4 | 刷新 `source.json` | 新 stamp = 未来 HEAD；`rev-list` 落后 0 | 刷新带入无关大 diff | SDD/setup |
| W1.5 | 处置 5 个死脚本（归档或补文档 + 修 `json_escape`） | 活跃面 0 调用清单为空；或脚本进入归档并在 owner 中登记 | 发现隐藏调用者 | 需裁决 Q2 |
| W1.6 | create-team 存储布局改为逐条文件（`supersede`） | 两分支同时跑同一队不再写同一路径；有并发测试 | 需改动团队运行协议 | SDD 运行 |
| W1.7 | 团队/goal 收敛：6 无 goal、5 壳团队、2 非法 YAML、12 文件旧锚 | `run-checks` 20 队全部 `ok` 或显式 `exempt`；PyYAML 全通过 | 退役误伤活跃队 | 需裁决 Q3/Q4 |
| W1.8 | `git-utils` 重观察 workflow | observed 块分支集合与 `git branch` 一致 | — | git-utils |
| W1.9 | `/speckit.feature` 行体收敛（可选） | 最长行 ≤ 2,000 字符，行数不增 | 需重写历史状态列 | 需裁决 Q6 |

### Wave 2 — 数据回收（sanitize，须用户授权）

| 项 | 目标 | 可测结果 | 中止条件 |
|---|---|---|---|
| W2.1 | pyc + checker 沙箱 + 备份 | `.specify` pyc 137→0；沙箱 ≈129MB→0；root 属主条目清零 | 沙箱内含未提交的他人工作 |
| W2.2 | 指令备份 / 旧备份 / 空台账 | 252KB + 68KB + 0B 释放 | 需要保留最近 1 份 |
| W2.3 | 遗留 jsonl 归档 | 8 个 tracked jsonl 退出跟踪面 | 活跃队仍写入 |

### Wave 3 — 结构收敛

- 空层与属主：`execution/scripts` 的 optional 地位写实（保留或删层）；`chown` 修复 root 属主。
- `gate-template.yaml` 的取舍落地（接引用或退役）。
- 若宿主渲染会重建 `.backups/`，在源侧补 ignore 规则（同一变更内落模板与安装副本）。
- `shared` 重复面维持 pass；`clarify-taxonomy.md` 的 3 处分模式重复行确认属结构性，不处置。

## 4. 裁决点（封闭问题，须用户回答）

1. **W2 授权**：是否批准 `/speckit.sanitize` 回收 pyc + 9 个 checker 沙箱 + 7 份指令备份 + 15 份旧备份 + 1 个 0B 台账？（是 / 否；否时请给保留集）
2. **死脚本**：5 个零调用脚本选 `archive`（推荐，可逆）还是选“保留 + 补文档 + 修 `json_escape`”？
3. **6 个无 goal 团队**：全部经 `/speckit.goal migrate` 迁为定义（推荐对仍有运行的队），还是把休眠队直接 `archive`？
4. **5 个 achieved-goal 壳团队**：退役（`archive`）还是逐个写 `exempt`（需理由 + 到期条件）？
5. **instructions 预算**：先压缩（推荐）还是调高预算？若调高，按 owner 规则给出升后仍 ≥1,024B 余量的值。
6. **source.json**：现在刷新，还是等下一次 `specify init`/迁移窗口？
7. **gate-template.yaml**：接上流程引用还是退役？

## 5. 方法与痕迹

- 只读边界：本席未修改、移动、删除任何项目文件；唯一写入为本报告。审计中出现过一次 in-passing 修复：中止的 `script-interface-check.py` 生成 2.7GB 沙箱，作者自建的 `.specify/.tmp/script-interface-xxrtqrxn` 已删除至 312KB（余下为 root 属主文件，agent 用户无权删除）。
- 关键读数：`sync-mirrors --check` 全量 exit=2 / `--only scripts` exit=0；`regen --check` exit=0；`goal-utils validate` 14/14；`run-checks` 6×`no-goal-definition`、5×`goal-terminal`（blocked）。
- 未复核项：`.specify/specs/**`、`memory/**` 等其它域的数据；B16 的“shared 重复行”按 `unverified` 保留，不立债项。
- 覆盖缺口：`.specify/.tmp` 总量（649MB）主要由其它域资产构成，本报告只认领 checker 沙箱与 root 属主部分。

ANOMALY: `script-interface-check.py` 被中止后不清理沙箱——2026-11-10 遗留 9 个（≈129MB），本次审计新产生 1 个（2.7GB，已回收至 312KB）；残留文件为 root 属主（`.specify/.tmp` 内 root 属主条目 520 个），agent 用户无法完成清理，需 root/授权处置。

DEBT-DONE
