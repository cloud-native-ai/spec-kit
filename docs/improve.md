# 技能迭代优化记录：browser-utils & improve-skills

> 本文档完整记录一次以 **多智能体（planner / executor / reviewer）迭代循环** 对两个
> SpecKit 技能进行的优化：`browser-utils` 与 `improve-skills`。内容包括优化目标、方法论、
> 每轮使用的 **prompt**、过程记录、评分演进与最终结果。
>
> - 优化日期：2026-07-08
> - 编排者：Claude Code（Opus 4.8），串行编排 3 个 `general-purpose` subagent 角色
> - 最终结果：**5 轮迭代，分数单调递增 79 → 90 → 94 → 96 → 99 / 100**

---

## 1. 优化目标

通过反复迭代，同时优化两个技能，并以一个真实的浏览器任务作为「基准测试载体」来暴露技能缺陷：

| 技能 | 优化侧重（定位） |
|---|---|
| **improve-skills** | 通用目标——「**该如何优化任意一个技能**」（方法论层面） |
| **browser-utils** | 定制目标——「**该如何正确地用浏览器执行前端相关任务**」（工程实践层面） |

**基准测试任务（executor 执行）**：复用 `~/data/chrome/agent` 这个含登录态的 Chrome
data 目录与 profile，遍历内部 SPA `http://xuan-ji.alibaba-inc.com`，抓取全部功能模块，
输出设计文档 `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-ui/docs/legacy.md`。

**硬性约束**：至少 5 轮「不劣化」（分数逐步升高）的迭代。

**追加需求（第 2 轮中途提出）**：`legacy.md` 中，除 iframe 嵌入的页面外，其余原生页面
都需细化到 **组件级别**（详细的按钮与输入框说明），以便后续对齐遗留系统的用户使用习惯与体验。

---

## 2. 方法论

### 2.1 三角色迭代循环

每一轮由 3 个 subagent 角色 **串行** 执行（存在数据依赖 + Chrome profile 单实例独占，
无法并行）：

```
┌─────────────────────────────────────────────────────────────────┐
│  Round N                                                          │
│                                                                   │
│  ① PLANNER ──用 improve-skills 方法论优化 browser-utils──▶ 技能改进 │
│         │  (依据上一轮 reviewer 的 Top-3 弱项)                      │
│         ▼                                                          │
│  ② EXECUTOR ──用 browser-utils 驱动真实浏览器遍历站点──▶ legacy.md  │
│         │  (Tier 3 / Mode 2：真实 Chrome profile 复用登录态)       │
│         ▼                                                          │
│  ③ REVIEWER ──按固定 rubric 打分──▶ 分数 + 同时优化两个技能         │
│            └─▶ 产出下一轮 Top-3 弱项                                │
└─────────────────────────────────────────────────────────────────┘
```

- **PLANNER**：只编辑 `browser-utils`（用 improve-skills 的方法：证据驱动、最小化、
  根因修复；SKILL.md 保持契约级，how-to 下沉到 references）。
- **EXECUTOR**：只读技能、驱动浏览器、写 `legacy.md`；把踩到的技能缺陷作为一等证据反馈。
- **REVIEWER**：按固定 rubric 打分（自行 grep/读文件核验，不轻信报告），然后同时优化
  两个技能（browser-utils 偏工程实践，improve-skills 偏通用方法论），并给出下一轮弱项。

### 2.2 源目录与分发目录

- **权威源（source of truth）**：`.specify/skills/<name>/`（由 `create-new-skill.sh`
  规定）。所有 planner/executor/reviewer 均读写此目录，确保 executor 测试的永远是
  planner 最新改动。
- **分发目录**：`skills/<name>/`（用户指定的合入目标）。每轮结束后由编排者将权威源
  的 `.md` 变更镜像到此目录（保留 `skills/` 独有的额外文件与 node_modules）。

### 2.3 固定评分 rubric（跨轮可比）

满分 100，子项与配额全程固定，保证「分数逐步升高」有可比性。要求 reviewer 每个子项
附证据（引用/文件行号/计数），且第 1 轮留出 headroom。

| 维度 | 子项 | 配额 | 说明 |
|---|---|---|---|
| **A. improve-skills 质量**（通用） | A1 证据驱动/最小化/根因 | 10 | |
| | A2 SKILL.md 契约化（瘦身） | 5 | how-to 下沉 references |
| | A3 提升下一次优化的可靠性/复用性 | 10 | |
| **B. browser-utils 质量**（定制） | B1 运行模式选择+健壮启动+失败处理 | 10 | Mode1/Mode2 |
| | B2 指导可执行、减少后续错误 | 10 | 预检/等待/清理 |
| | B3 前端任务专用性 | 5 | 遍历/登录态复用/SPA |
| **C. executor 产物 legacy.md** | C1 覆盖度（枚举全部模块/子模块） | 12 | |
| | C2 深度（**原生页面组件级** 硬性要求；iframe 仅需 src/标题/面板/变量名） | 18 | 用户指令 |
| | C3 结构与可用性（TOC/一致分节/可导航） | 10 | |
| **D. 过程严谨性** | D1 可复现（profile 预检/脚本卫生） | 5 | |
| | D2 证据（截图/计数/登录态断言） | 5 | |

> 注：C2 在第 2 轮随用户「组件级」追加需求从 15 提到 18（C1 相应从 15 调到 12），并对
> 第 1 轮按新配额重算，确保 79→90 仍单调。

---

## 3. 每轮使用的 Prompt

以下为实际下发给各角色 subagent 的 prompt（保留关键结构；每轮的差异主要在「上一轮弱项」
与「本轮目标」两段）。

### 3.1 PLANNER prompt 模板

```
You are the PLANNER in round N. Use the `improve-skills` methodology to optimize
the `browser-utils` skill, targeting the specific weaknesses round N-1 exposed.

## Canonical paths
- Methodology to FOLLOW: .specify/skills/improve-skills/SKILL.md (+ references/)
- Skill to OPTIMIZE (edit ONLY here): .specify/skills/browser-utils/ (SKILL.md + references/)
Read the CURRENT state first — do NOT duplicate prior rounds' fixes.

## Round N-1 outcome (score ..) and the weaknesses YOU must address
<上一轮 reviewer 的 Top-3 弱项，逐条给出根因与期望修复方向>

## Method
improve-skills: evidence-driven, minimal, root-cause. SKILL.md contract-only;
code/how-to goes in references/playwright-patterns.md. delete-and-absorb if moving.
Validate any JS with `node --check`.

## Constraints
- Edit ONLY under .specify/skills/browser-utils/. Do NOT run the browser.
  Do NOT touch docs/legacy.md or improve-skills.

## Return (final message = report)
- Each edit: file, change, which weakness it addresses.
- SKILL.md line count before/after; confirm contract-level.
- node --check result. What the executor can now do better.
```

### 3.2 EXECUTOR prompt 模板

```
You are the EXECUTOR in round N. Using the `browser-utils` skill, drive the real
logged-in browser to traverse/refine the design doc docs/legacy.md.

## Read and FOLLOW the skill FIRST
- .specify/skills/browser-utils/SKILL.md
- .../references/playwright-patterns.md ("Run Modes", "SPA Site Traversal & Module
  Extraction"). READ current docs/legacy.md first so you extend, not duplicate/regress.
You are Tier 3, Mode 2 (real Chrome profile).

## Environment
- Login-state profile: ~/data/chrome/agent (preflight it's free; ALWAYS close context
  in finally to release the single-instance lock).
- App root: http://xuan-ji.alibaba-inc.com/dashboard/#/ (hash SPA).
- Runner: .../scripts/js/run.js (install-integrity preflight first).

## Mode 2 launch recipe (proven)
launchPersistentContext(~/data/chrome/agent, { headless:false, channel:'chrome',
  ignoreDefaultArgs:['--use-mock-keychain'], viewport:{...} })
- After first nav, assert URL is NOT login*.alibaba-inc.com.

## GOALS THIS ROUND
<本轮目标：如 组件级深化 / Grafana 面板抓取 / 证明上限 / Mode1 净测 等>

## Scope split (user directive)
- NATIVE pages → COMPONENT level (每个按钮+输入/下拉 穷举).
- IFRAME/Grafana → src + title + panel count/titles + template-variable NAMES + dashboardState.

## Constraints
- Scripts + screenshots to /tmp only. One browser at a time. No coverage regression.
  Don't fabricate — only observed content.

## Return (final message = report)
- Login proof (authenticated landing URL, not a login host).
- Counts (groups/routes/visited/failed). legacy.md new line count.
- Specific skill feedback for the reviewer.
```

### 3.3 REVIEWER prompt 模板

```
You are the REVIEWER in round N. Score against the FIXED rubric, verify, then improve
BOTH skills, and write feedback for round N+1.

## Fixed rubric: /tmp/skill-iter/RUBRIC.md
Previous scores: /tmp/skill-iter/scores.md (Round N-1 TOTAL = ..). Append your Round N
block. Round N must be >= previous (monotonic non-decreasing).

## What happened this round
<planner 与 executor 的产出摘要 + executor 反馈的可折叠技能缺陷>

## Tasks (in order)
1. SCORE vs rubric; append block with per-sub-score evidence. VERIFY by reading/greping
   docs/legacy.md and the skills yourself (don't trust the reports).
2. IMPROVE browser-utils (定制目标): fold in the executor's proven fixes.
3. IMPROVE improve-skills (通用目标): distill the round's meta-lesson.
4. VALIDATE (re-read; SKILL.md contract-level; anchors/paths resolve; node --check).

## Constraints
- Edit ONLY the two skill dirs. Do NOT edit docs/legacy.md. Minimal, root-cause.

## Return: full score block (TOTAL + delta) + each skill edit + Top 3 weaknesses next round.
```

---

## 4. 过程记录（逐轮）

### 前置准备
- 确认 `.specify/skills/` 为权威源；`skills/` 为独立分发副本（85 文件 vs 14 追踪文件）。
- 确认 Chrome profile `~/data/chrome/agent` 空闲（0 进程、无 singleton 锁）。
- 建立固定 rubric（`/tmp/skill-iter/RUBRIC.md`）与评分日志（`/tmp/skill-iter/scores.md`）。

### Round 1 — 打基线（TOTAL = 79）
- **Planner**：为 browser-utils 新增「SPA Site Traversal & Module Extraction」参考章节
  （enumerateRoutes/gotoRoute/extractModule/可恢复 traverse）；SKILL.md 加约定指针；
  收紧 Strict Req #4（预检 + finally 释放 profile 锁）。
- **Executor**：首次跑通——20 个导航组、54 条叶子路由、54 访问 / 0 失败 → `legacy.md` 625 行。
  暴露缺陷：① 两处 runner `node_modules` 损坏；② `enumerateRoutes` 把已展开菜单点回收起
  导致返回 0 路由；③ `extractModule` 未遍历 `page.frames()`，漏掉约 60% 的 Grafana iframe 页。
- **Reviewer**：折叠上述修复（open-state 感知的展开、iframe 钻取、安装完整性自检）；
  improve-skills 增补「运行时失败为一等证据」「引用代码须实际可运行」。

### Round 2 — 组件级深化（TOTAL = 90，Δ+11）
- 用户中途追加「原生页面需组件级」需求 → 编排者据此更新 rubric C2（15→18）。
- **Planner**：新增 Step 0（登录断言 + run log）、Step 2.5（settleDynamicContent +
  revealTabsAndRows）、synthesizePurpose、截图强制；SKILL.md Strict Req #12。
- **Executor**：`legacy.md` 626→1148 行；**28 个原生页面细化到组件级**（按钮+动作、
  输入/下拉+标签/placeholder/类型/选项、表格、tab），26 个 iframe 页识别。
  反馈：Ant `<Select>` 选项需展开才在 DOM；Grafana 模板变量选择器过时；按钮噪声。
- **Reviewer**：折叠 readSelectOptions、修正 Grafana 变量选择器、按钮噪声过滤、macOS
  长任务后台运行说明；improve-skills 增补「静默漏抽也算缺陷」「交互门控/版本漂移」两类根因。

### Round 3 — Grafana 深度（TOTAL = 94，Δ+4）
- **Planner**：重写 settleDynamicContent（滚动 iframe 强制懒加载面板挂载）、面板标题
  抓「分组+单面板」、模板变量按 **名称** 抓取、synthesizePurpose 用区分性信号、新增
  「组装成单文件运行」小节。
- **Executor**：有面板的 dashboard 10→17/26（如 lingjun_monitor 229 面板）、变量名正确、
  原生组件级深度保留、purpose 信号化；`legacy.md` 1180 行。
  反馈：行头「(0 panels)」与 DOM 实测矛盾；表格型面板标题拼接了正文；需识别合法零面板情形。
- **Reviewer**：DOM panelCount 设为权威、面板标题限定表头节点、新增 dashboardState 识别
  3 种合法零面板情形；improve-skills 增补「优先 ground-truth 信号，避免抓到兄弟节点内容」。

### Round 4 — 消缺陷 + 瘦身（TOTAL = 96，Δ+2）
- **Planner**：对 browser-utils SKILL.md 做 delete-and-absorb 瘦身 310→252 行（Agent-Specific
  Configuration 移入新 reference）；验证 Grafana 修复可组装运行。
- **Executor**：grep 验证两处 Grafana 缺陷 **归零**（「(N panels)」标签、标题拼接正文）；
  有面板 dashboard 诚实停在 17/26（4 个 os-grafana 需独立 SSO、2 个失效）；原生深度保留；
  `legacy.md` 1186 行。反馈：Grafana scenes 版需读表头 `data-testid` **属性值** 才得干净标题。
- **Reviewer**：**终于完成 improve-skills 自身瘦身 151→100 行**（连续 3 轮被标记的 A2）；
  折叠 data-testid 属性标题修复；improve-skills 增补「优先权威信号、限定叶子节点」。

### Round 5 — 收口（TOTAL = 99，Δ+3）
- **Planner**：把 Mode 1（净测浏览器）做成一等——新增快速上手（localhost 变体 +
  零依赖 `file://` 变体），node --check 通过。
- **Executor**：① Mode 1 净测跑通（bundled Chromium、无 profile、默认 mock keychain，
  截图 `/tmp/mode1-selftest.png`）——补上 B1 数据点；② 证明 Grafana 17/26 为 **真实环境上限**
  （os-grafana 两个域名均 302→/login，4 个板需独立 SSO；2 个板确认失效）；`legacy.md` 1187 行、
  一致性核验无回退。
- **Reviewer**：新增 improve-skills `references/hardening-examples.md`（两个前后对比实战范例，
  A1/A3 收口）；修 Mode 1 注释缺 `cd` 前缀的小瑕疵；确认 5 轮趋势单调。

---

## 5. 评分演进

| 轮次 | A(25) | B(25) | C(40) | D(10) | **TOTAL** | Δ |
|---|---|---|---|---|---|---|
| R1 | 18 | 19 | 34 | 8 | **79** | 基线 |
| R2 | 20 | 23 | 37 | 10 | **90** | +11 |
| R3 | 21 | 24 | 39 | 10 | **94** | +4 |
| R4 | 22 | 24 | 40 | 10 | **96** | +2 |
| R5 | 24 | 25 | 40 | 10 | **99** | +3 |

**趋势：79 → 90 → 94 → 96 → 99，单调不劣化，满足 ≥5 轮要求。**

子项收口路径（headroom 逐轮消化）：
- C 维度（覆盖/深度/结构）R4 起满分 40/40；D 维度 R2 起满分 10/10。
- A2（契约瘦身）R4 收口；A3（前后对比范例）R5 满分；A1 R5 至 9。
- B2/B3 R3 起满分；B1（补 Mode 1 净测）R5 收口至 10。

---

## 6. 技能改动汇总（最终状态）

### browser-utils（定制：如何正确用浏览器执行前端任务）
- **SKILL.md**：310 → **252 行**，契约级（Agent-Specific Configuration 下沉到
  `references/agent-configuration.md`）。含两种运行模式契约（Mode 1 净测 / Mode 2 真实 profile）。
- **references/playwright-patterns.md**（**1149 行**）：Run Modes 两模式配方与失败症状表；
  Mode 1 快速上手（localhost + 零依赖 file://）；SPA 遍历与组件级提取
  （enumerateRoutes 开合感知、gotoRoute、settleDynamicContent 滚动强制挂载、readSelectOptions、
  extractModule iframe 钻取、DOM 权威 panelCount、表头 `data-testid` 干净标题、dashboardState、
  synthesizePurpose、可恢复 traverse、安装完整性自检）。
- **references/agent-configuration.md**（新增）：智能体识别与反馈模板。

### improve-skills（通用：如何优化任意技能）
- **SKILL.md**：151 → **100 行**，契约级。
- 新增证据/验证类指导：运行时失败为一等证据、引用代码须实际可运行、优先 ground-truth 信号、
  限定叶子/表头节点、交互门控与版本漂移两类根因。
- **references/agent-configuration.md**（新增，delete-and-absorb 瘦身产物）。
- **references/hardening-examples.md**（新增）：两个前后对比实战范例（enumerateRoutes 盲切换、
  Grafana 标题 textContent→data-testid 属性）+ 复用清单。

---

## 7. 最终产物

- **设计文档**：`kangaroo-xuanji/xuanji-ui/docs/legacy.md`（**1187 行**）
  - 54 个功能模块，含 TOC / 一致分节 / Coverage 全路由表。
  - **原生页面组件级**：每个按钮（标签+推断动作）、每个输入/下拉（标签/placeholder/类型/选项）、
    表格列、tab、分页、关键交互——满足「对齐遗留系统 UX/用户习惯」诉求。
  - **iframe/Grafana 页面**：嵌入 src + dashboard 标题 + 面板数（DOM 实测，权威）+ 面板标题 +
    模板变量名 + dashboardState（合法零面板情形按原因标注）。
  - 诚实标注：有面板 dashboard 17/26 为 **已证明的外部环境上限**（os-grafana 需独立 SSO、
    2 个板失效），非抓取失败。
- **两个技能已合入分发目录 `skills/`**：所有 `.md` 与新增 references 均与权威源
  `.specify/skills/` 一致（`skills/` 独有的额外文件与 node_modules 保留未动）。

---

## 8. 关键经验（可复用）

1. **技能 + 基准任务 + 评审 的三角闭环**：用一个真实任务把技能缺陷「逼」出来，比空想改进更有效。
   executor 反馈的运行时缺陷是技能改进最高价值的证据来源。
2. **固定 rubric 是「单调递增」的前提**：配额/子项全程不变，分数才可比；中途新增需求（组件级）
   需同步调整配额并对历史轮重算，避免破坏单调性。
3. **契约与手册分离（slimming）**：SKILL.md 只留契约（frontmatter/流程骨架/strict reqs/资源索引），
   how-to 与代码进 references；「宣扬瘦身的技能自己必须先瘦」（improve-skills 151→100）。
4. **浏览器复用登录态的三条硬约束**：profile 无占用（单实例锁）+ `channel:'chrome'` +
   `ignoreDefaultArgs:['--use-mock-keychain']`，三者缺一即静默跳登录页。
5. **抓取要用 ground-truth 信号**：DOM 元素计数优于框架自报的「(N panels)」标签；干净标题读
   表头 `data-testid` 属性而非 textContent；下拉选项需先展开；同时兼容旧/新 DOM 形态。
6. **诚实标注 > 编造覆盖**：不可达内容用 dashboardState 据实标注为环境限制，不伪造。

---

## 9. 勘误与修正（2026-07-08，迭代后复查）

**问题**：第 4 轮把 `## Agent-Specific Configuration`（含 `### Step 1/2/3`）从 `browser-utils`
与 `improve-skills` 的 `SKILL.md` 中「瘦身」移入 `references/agent-configuration.md`，仅留指针。
但该章节由 speckit 特性 `021-agent-specific-config` 引入，其**契约 C-002 有自动化测试**
（`tests/contract/test_agent_specific_config_skills.py`）**强制要求这四个标题内联存在于
SKILL.md**。此次瘦身导致这两个技能的 C-002 契约测试 **失败** —— 属于用通用启发式（slimming）
覆盖了显式特性契约的错误。

**修正**：
- 将完整的 `## Agent-Specific Configuration`（Step 1/2/3 + 检测表 + 反馈模板）**恢复内联**到
  两个 `SKILL.md`（源 `spec-kit/skills/` 与生成副本 `spec-kit/.specify/skills/` 同步）。
- 删除冗余的 `references/agent-configuration.md` 及其在 Resources 索引中的引用（改回单一来源=内联）。
- 契约测试复跑：`test_agent_specific_config_skills.py` **24/24 通过**（4 个目标技能 C-002/C-003/C-004 全绿）。
  > 注：全量套件另有 6 个 **既有** 失败，属 C-001 命令模板（`templates/commands/{agents,skills,tools}.md`
  > 在 git HEAD 基线即缺该章节），与本次技能改动无关，未由本次引入。

**对第 6 节的影响**：browser-utils/improve-skills 的「Agent-Specific Configuration 瘦身」一项已回退；
其余瘦身（如 improve-skills 其他 how-to 下沉）与所有功能性优化保持不变。

**已加固 improve-skills 以防复发**（通用「如何优化技能」教训）：
- slimming 指南新增红线——移出任何带标题的章节前，先 grep `.specify/specs/**` 与 `tests/contract/**`，
  若有契约断言其内联存在则**保持内联**，改从别处瘦身。
- 验证步骤新增——对 SKILL.md/references 做**结构性改动（移动/改名/删除章节或文件）后必须运行相关
  契约测试**，而非仅 grep 标题。

**经验修订**：第 3 条「契约与手册分离」需加限定——**瘦身不得越过显式特性契约**；契约要求内联的
内容即属技能契约的一部分，不可下沉。
```
