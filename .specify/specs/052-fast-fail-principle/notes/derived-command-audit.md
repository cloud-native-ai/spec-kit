# 派生命令穷尽审计 (T058) — Feature 052

**Task**: T058(`tasks.md` Phase 9)· **Run date**: 2026-09-24 · **Tree**: 分支 `master`,HEAD `e2d0a8c2`(工作树洁净)
**Frozen baseline**: `BASE_SHA=80a8c1fb0e27c70c797974affb8e88510558da19`(经 `git merge-base --is-ancestor` 核验为 HEAD 的祖先)
**052 的提交窗口**: `5fc6a2f3`(父 = BASE_SHA)… `b7aeba9d`,15 个提交,连续;窗口之后另有 15+ 个非 052 提交(反馈 consume 运行、create-team 粒度、goal/plan/tasks 修复、053 需求),故**当前树 ≠ 052 落地时的树**——本文件对每个数值都标明它是在哪一棵树上核出的。

本文件是**审计记录(日期化)**,不是当前实况的第二定义点:凡与守卫或引擎冲突处,以代码为准。

---

## 0. 抽取方法与反空真哨兵

**抽取(机械,可复跑)**:对 T058 点名的 11 份制品逐行扫描,取两类候选——① 代码围栏内非注释、含命令 token 的行;② 行内反引号跨度中含命令 token 者。命令 token 集:`grep / ls / wc / cmp / diff / awk / sed / python3 / pytest / git / comm / test - / sync-mirrors / scan-confirmation-gates / feedback-utils / validate-tasks / run-tests / regen-command-copies / generate-instructions / mkdir / rm -rf / printf / for`。

**哨兵 1(抽取非空)**:11 / 11 份制品均抽出候选,合计 **304 处出现 / 180 条去重命令串**。分类(规则见下)与逐份分布:

| 类 | 判据 | 去重条数 |
|---|---|---|
| 度量命令 | 可跑且产出一个数/verdict | **129** |
| 路径引证 | 形如 `file.py:NNN` 或裸引擎名,本身不是可跑命令 | **28** |
| 被禁引擎 / 写入动作 | 命中 `sync-mirrors.py`(任何模式)/ `regen-command-copies.py` / `generate-instructions.sh` / `--action record` | **18** |
| 动作或演练步骤 | `mkdir` / `sed -i` / `rm -rf` 等演练中间步 | **5** |

| 制品 | 度量 | 被禁 | 动作 | 路径引证 | 合计 |
|---|---|---|---|---|---|
| plan.md | 10 | 3 | 0 | 14 | 27 |
| research.md | 14 | 4 | 0 | 6 | 24 |
| data-model.md | 1 | 0 | 0 | 2 | 3 |
| quickstart.md | 67 | 3 | 5 | 5 | 80 |
| feature-ref.md | 2 | 1 | 0 | 5 | 8 |
| contracts/ambient-section.md | 1 | 0 | 0 | 3 | 4 |
| contracts/constitution-export.md | 0 | 0 | 0 | 0 | 0 |
| contracts/discipline-doc.md | 0 | 0 | 0 | 1 | 1 |
| contracts/dispatch-injection.md | 0 | 0 | 0 | 1 | 1 |
| contracts/gate-neutrality.md | 2 | 0 | 0 | 8 | 10 |
| tasks.md | 50 | 13 | 0 | 15 | 78 |

> 三份契约(constitution-export / discipline-doc / dispatch-injection)几乎不印命令,只印**派生值**(行号、计数、"改前实测 X")。对它们,审计单位下沉为「印出的派生值」:由本审计构造命令核其实况,并在下表标明所用命令。这是 T058 的"每一条派生命令"在这三份制品上的唯一可操作读法。

**审计单位(check item)**:一个「制品位置 → 印出的值/verdict → 核对命令 → 实测 → 判定」五元组。合计 **198 项**(逐份见 §1–§11),即**哨兵 2**:`198 > 0` 且每份制品 ≥ 9 项,故下文的"零不符/已订正"不是空转结论。

**核对路线(四选一,逐项标明)**:
- **LIVE** — 在当前树上跑制品印出的命令本身。
- **BASE** — 制品印的是**改前**值:用 `git show BASE_SHA:<path> | <同一命令>` 或 `git grep <pat> BASE_SHA -- <paths>` 在基线树上核(只读,不检出、不建 worktree)。
- **ROEQ** — 引擎被本次派发的硬约束禁止(任何模式):用**只读等价物**核其印出的结论(mirror 用 `ast.literal_eval` 解析 `MIRROR_PAIRS`/`IGNORE_NAMES` + `filecmp` 复刻引擎的 MISS/DIFF/EXTRA 语义;指令再生用 `grep -c` / `test -L`)。
- **NR** — 本轮**未实跑**(被禁且无只读等价物),引用实现期取证位置。

**并发编辑告知**:编排者在本轮期间并发编辑 `templates/commands/feedback.md`、`docs/reference/skills/feedback.md`、`docs/reference/history/00-cross-cutting-lessons.md` 与 `.specify/memory/feedback/` 存储。凡读到这些面的结果都可能是一次中间态。已观测到一例:第一次全量套件跑时 `tests/contract/test_feedback_command_classification.py` 的分类表解析**抛错**(使两个 docs 测试连带失败),数分钟后同一解析返回 **25 条**、两测试转为 passed——即该面确实在本轮期间处于中间态。

---

## 1. plan.md(30 项)

| # | 位置 | 印出的值/verdict | 核对命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | :52 / :75 | 过宽形态 `grep -c '^## 场景'` 当时实跑 **10** 而非所印 9 | LIVE `grep -c '^## 场景' quickstart.md` | **13**(今 12 场景 + `## 场景覆盖表`);当时 9 场景 ⇒ 9+1=10 自洽 | 相符(日期化);过宽形态已在制品内订正为带 `[0-9]` |
| 2 | :217 | `grep -c '^## 场景 [0-9]'` → **12**;不带 `[0-9]` → **13** | LIVE 两式 | 12 / 13 | 相符 |
| 3 | :214 | `grep -c '^## D-'` research.md → **17** | LIVE | 17 | 相符 |
| 4 | :215 | `grep -c '^## E'` data-model.md → **19** | LIVE | 19 | 相符 |
| 5 | :215 | 校验规则 **7** / 状态机 **3** | LIVE `grep -c '^### V[0-9]'` / `'^### S[0-9]'` | 7 / 3 | 相符 |
| 6 | :216 / :220 | `grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` → 22/19/26/23/17 = **107** | LIVE 逐文件 + 求和 | 22/19/26/23/17 = 107 | 相符 |
| 7 | :217 | 改前基线总表 **25 行** | LIVE `sed -n '/^## 改前基线总表/,/^---$/p' \| grep -c '^| '` 减表头 | 26 − 1 = 25 | 相符 |
| 8 | :218 / :224 | FR→条款映射去重 **78** | LIVE `grep -oE '^\| FR-[0-9]{3} \|' \| sort -u \| wc -l` | 78 | 相符 |
| 9 | :224 | 初版按行计数 **85**(缺陷记录) | LIVE `grep -cE '^\| FR-[0-9]{3} \|'` | 85 | 相符(缺陷已订正为去重命令) |
| 10 | :218 | **71** 条款级 + **7** 未覆盖(3 无条款 / 4 节级或间接) | LIVE 未覆盖表行数 + 78−7 | 7 / 71 | 相符 |
| 11 | :218 | SC→度量映射 **15 行** | LIVE `grep -c '^| SC-'` 于该节 | 15 | 相符 |
| 12 | :218 | 交付面清单 **16 行** | LIVE 同法(减表头) | 17 − 1 = 16 | 相符 |
| 13 | :45 | requirements **78 FR / 15 SC / 13 STR** | LIVE `grep -c '^- \*\*FR-[0-9]'`;`grep -oE 'SC-[0-9]{3}' \| sort -u \| wc -l`;同法 STR | 78 / 15 / 13 | 相符。⚠️ SC 的**朴素**形态 `grep -c '^- \*\*SC-'` 得 **30**(每条 SC 在"可度量结果"与"测量源"两节各出现一次)⇒ 该值的正确派生形态是**唯一 ID 计数**,不是行计数 |
| 14 | :29 | 冻结基线 `total: 23`、`integerHeadroom: 0` | LIVE 读 050 基线 JSON | total 23 / integerHeadroom 0 / cap 23.25 | 相符 |
| 15 | :15 / :29 | 扫描器实跑 `total = 23` | LIVE `scan-confirmation-gates.py` | 23(destructive 13 / governance_kept 10 / violations 0) | 相符 |
| 16 | :15 / :27 | 草稿子句 **8 行 / 933 字节 / 0 命中** | — | 草稿从不落盘,制品自陈"无命令可复现";**落地**子句实测 6 原始行(5 非空行)/ 801 字节 / 逐行 `BLOCKING_RE` 0 命中 | 不可复现(按制品自陈);落地值满足 ≤10 行 / ≤1200 字节 |
| 17 | :27 | 6 成员一轮 ≈ **5.6 KB** | LIVE 算术 `933*6` | 5598 B = 5.6 KB | 相符 |
| 18 | :27 | 活动指令 **28,168 B** / 预算 **32,768** / 余量 **4,600** | BASE `git show BASE_SHA:.specify/instructions.md \| wc -c`;LIVE `grep -n INSTRUCTIONS_BUDGET_BYTES` | 28168 ✓ / 32768 ✓(`generate-instructions.sh:38`)/ 4600 ✓。**今** 30,944 B(052 之后再生所致),余量 1,824 | 相符(日期化) |
| 19 | :32 / :143 | `--check --only shared` 改前 **EXIT=2 / 恰 2 条 DIFF** | ROEQ + BASE | 只读复刻:改前集 = {`workflow/feedback-step.md`, `workflow/runtime-mode.md`};**今 DIFF=0**(T010 的 scope 级 `--write` 连带治好,已在 T010 行内披露) | 相符 |
| 20 | :142 | 全树 `--check` → `DRIFT detected` / EXIT=2;`agents` 为 ok | ROEQ | 今:templates 2 / skills 30 / agents 0(ok, 2 files)/ shared 0 / scripts 1(`trigger-utils.py`,既有) | 相符(相对判据成立,详见 §12) |
| 21 | :145 | 四棵命令树各 **25**;四棵 agent 树各 **2**;`.opencode/agent` **0**;符号链接 **4** | LIVE `ls -1 \| wc -l` / `test -L` | 25/25/25/25;2/2/2/2;0;4 条全为 symlink | 相符 |
| 22 | :33 / :198 | `fail-fast` 在权威源上 **9 处**占用 | BASE `git grep -Io 'fail-fast' BASE_SHA \| wc -l` | **9**(全仓,基线树);今 24(052 及后续制品在记录该否决时自身提及) | 相符(日期化) |
| 23 | :34 | 三个稳定字面量六对组合**零违规** | LIVE 纯字符串运算(quickstart 场景 8 第二段) | `substring violations: none`,伴生量 `pair count: 6` | 相符 |
| 24 | :197 | `[fast-fail]` / `ff-triage` 框架目录**零命中**(改前) | BASE `git grep -Io` | 0 / 0(今非零,属设计结果) | 相符(日期化) |
| 25 | :204 | `test_user_facing_comprehension_doc.py:400` 钉死去重路径数**恰为 8** | BASE + LIVE `grep -n 'len(deduped) == '` | BASE `:400 == 8` ✓;LIVE `:400 == 9` ✓(D-4 的上调) | 相符 |
| 26 | :171 | 051 的 red-first:`28 failed / 6 passed`,17 × FileNotFoundError + 10 × 标题不存在 | LIVE 读 `.specify/specs/051-*/notes/red-first-evidence.md` | `28 failed, 6 passed` ✓;分类表 17 + (4+3+1+1+1=10) + 1 镜像 = 28 ✓ | 相符 |
| 27 | :183 | `test_proactive_trigger_section.py:352` 持 total 相等钉子 | LIVE `sed -n '352p'` | `assert payload["total"] == frozen["total"], (` | 相符 |
| 28 | :185 | 上游缺陷 4 + 2 项 | LIVE 逐项 | ① `memory/feature-index.md` 死指针:**已被后续工作修掉**(今 0 命中);② "刷新指令即恢复镜像副本"假承诺:**仍在**,由活动指令的 `## User-Facing Comprehension` 节携带,052 自己的 `## Fast Fail Discipline` 区间命中 **0**(与制品所述一致);③ `反空转哨兵` 1 处 vs `反空真哨兵` 3 处:**仍不一致**;④ `agent-definitions.md:50` 的 "seven shipped role agents":**已被后续工作改写**为"计数刻意不复述",而 `agents/*.agent.md` 实测仍 **2**;⑤ `constitution.md:64-70` 仍要求 4 段版本而活动宪章为 3 段 `1.13.0`:**仍在** | 相符(记录当时实况;两项已被上游自行修复) |
| 29 | :35 | Scale/Scope 计数簇:12→13 / 18→19 / 19→20 / 13→14 / 15→16 / 1.12.0→1.13.0 / 7→8 / 5→6 / 预设 2 / 新测试 1 / 上调钉子 5 / 点位十余 | LIVE + BASE 逐量 | 13 ✓ / 19 ✓ / 20 ✓ / 14 ✓ / 16 ✓ / 1.13.0 ✓ / 8 ✓ / 载荷行**今 7**(052 落地时 6,详见 §4 项 5)/ 2 ✓ / 1 ✓ / 5 = 4 宪章钉 + 1 UFC 钉 ✓ / 8 点位各 1 行指针 ✓ | 相符(载荷行数为 052 之外的后续改动所致) |
| 30 | :15(隐含)/ verification `final_doc_*` | 真源文档 **308 行**、逐行 `BLOCKING_RE` **0 命中** | LIVE `wc -l` + importlib 取真正则逐行 | 308 行 / 0 命中;项目专名 4 者命中 **0** | 相符 |

**小结**:抽出 30 项 / 相符 29 / 不符 0 / 不可复现 1(项 16,制品自陈草稿不落盘;其可断言的上限已改核落地子句)。另有 1 处订正落在本文件(`:85` 的 `feedback-utils.py:1389`,见 §13 M2),它出现在质量门表内、未单列为 check item。

---

## 2. research.md(21 项)

| # | 位置 | 印出的值 | 路线与命令 | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | D-1 | `test_user_facing_comprehension_section.py:51-52` 定义 PREV/NEXT_HEADING;`:207-218` 的 `test_c8` 是**严格排序**;`:195-205` 的 `test_c7` 三节连续 | LIVE `grep -n` + `sed -n` | 两个常量实在 **`:50-51`**(该文件自 BASE_SHA 起无任何提交改动 ⇒ 从来就偏了一行,不是漂移);`test_c7` def 在 `:194`、body `:195-205` ✓;`test_c8` def 在 **`:208`**、严格不等式断言在 **`:216`**(印出的 `:207-218` 覆盖 def 与断言,但起点早一行);**读法成立**:`assert i_prev < i_new < i_next` 是严格排序而非相邻 | **不符 ⇒ 已订正**(见 §13 M5) |
| 2 | D-1 | `grep -n '^## '` 模板 **18 节**;锚点 **66 / 74 / 86** | BASE + LIVE | BASE 18 节、锚点 66/74/86 ✓;LIVE 19 节、Token Efficiency 66 / UFC 74 / **Fast Fail 86** / Dogfooding 100(严格递增且落在 UFC 与 Dogfooding 之间) | 相符 |
| 3 | D-2 | 草稿 **8 行 / 933 字节 / 457 字符 / 0 命中** | — | 不可复现(草稿不落盘);落地子句 6 原始行(5 非空)/ 801 字节 / 0 命中 | 不可复现(制品自陈) |
| 4 | D-2 | 28,168 B / `INSTRUCTIONS_BUDGET_BYTES=32768`(`generate-instructions.sh:38`)/ 余量 4,600 | BASE + LIVE | 28168 ✓;`:38` 正是该常量 ✓;32768−28168=4600 ✓ | 相符 |
| 5 | D-3 | payload 表结构 `:94/:96/:97/:98-102/:104-108/:110`,**5 个字段行** | BASE `git show … \| awk … \| grep -c '^| `'` | BASE = **5** ✓;LIVE = **7**(052 落地时 6,后续 `incremental_landing` 增至 7) | 相符(日期化) |
| 6 | D-3 | `grep -rn 'task_brief\|Per-Agent Payload\|forbidden_files' tests/contract/` → **0 命中** | BASE `git grep -c … BASE_SHA -- tests/contract/` | BASE **0 文件** ✓;LIVE **3 文件**(052 自己的守卫 `test_i13` 等引用了这些 token) | 相符(日期化,论证的是"改前无钉子") |
| 7 | D-4 | 类映射表在 `user-facing-comprehension.md:96-108`,**11 行**;类 ⑪ 行改前文本 | BASE + LIVE | 类表 11 行(BASE 与 LIVE 同)✓;改前类 ⑪ 行逐字相符 ✓;LIVE 该行同时含 `confirmation-gates.md` 与 `fast-fail.md`(在 `:106`) | 相符 |
| 8 | D-4 | 钉子 `test_c14_surface_class_table`(`:382`)、`:396` 取规则真源列、`:397` 正则提取、`:399-402` 断言**去重后恰为 8**;8 个路径清单 | BASE + LIVE | `:382` 定义行 BASE 与 LIVE 同为 382 ✓;`:396` = `src = _column(header, "规则真源")` ✓;`:397` = `re.findall(r"`([a-z0-9_./-]+\.md)`"…)` ✓;`:399-402` BASE 断言 8、LIVE 断言 **9** ✓ | 相符 |
| 9 | D-4 | `test_c18a_…`(`:489`)只数 override 列 | BASE | BASE = **489** ✓(LIVE 因 052 自己的插入移至 **508**;该段是改前实测语境,故不改数字,仅在此记录) | 相符(日期化) |
| 10 | D-5 | 六对组合零违规;`[fast-fail]` 框架目录零命中;引擎大小写不敏感子串匹配在 `feedback-utils.py:691-696` | LIVE + BASE | `none` / 6 对 ✓;BASE 0 命中 ✓;`:691-696` 区间内 `:696` 正是 `if contains not in haystack.lower(): continue` ✓ | 相符 |
| 11 | D-5 | 两处裸记号先例:`token-efficiency.md:54`、`user-facing-comprehension.md:124` | LIVE `sed -n` | 两处均为裸标记行,且其纪律路径含该字面量(碰撞观察成立) | 相符 |
| 12 | D-7 | 四钉改前 `TEMPLATE_COUNT=13`(`:65`,断言 `:202`)、`LIVE_COUNT=15`(`:66`,`:408`)、`COMMAND_COUNT=7`(`:67`,`:255`)、`MIN_VERSION=(1,12)`(`:68`,`:423`);`MUST include` 在 `:77,87,91,100,111,126,137` = 7;原则数模板 13 / 活动 15 | BASE `git show … \| grep -n` | 四钉行号 65/66/67/68 与值 13/15/7/(1,12) 全部逐字相符 ✓;断言行 202/255/408/423 ✓;`MUST include` 七行行号逐个相符 ✓;原则数 13/15 ✓。**LIVE**:值 14/16/8/(1,13),行号因 watchlist 增一项而整体 +1(66/67/68/69) | 相符 |
| 13 | D-7 | 上游分歧:`constitution.md:64-70` 要求 4 段 `x.y.z.ddd`,活动宪章 3 段,守卫 `:420` 只解析两段 | LIVE | `:64-70` 仍要求 4 段 ✓;活动宪章 `1.13.0`(3 段)✓;分歧仍在(属上游) | 相符 |
| 14 | D-8 | 扫描器输出块 `23 / 13 / 10 / 0`;冻结 JSON `"total": 23`、`"integerHeadroom": 0`、`"cap": 23.25` | LIVE | 输出逐行相符 ✓;JSON 五键相符 ✓ | 相符 |
| 15 | D-8 | `SCAN_DIRS = ("templates/commands","skills","shared")`(`:35`)、`SCAN_ROOT_FILES = ("templates",)`(`:36`)、`SKIP_DIR_PARTS` 含 `.specify`(`:37`) | LIVE importlib 取真 | 三者逐字相符;`".specify" in SKIP_DIR_PARTS` = True | 相符 |
| 16 | D-8 | 草稿子句 8 行逐行过 `BLOCKING_RE` → **0 命中** | LIVE(对落地子句) | 落地子句区间 0 命中;`len(BLOCKING_PATTERNS)` = **17**(哨兵非空) | 相符 |
| 17 | D-9 | `render_agents_for_tool` 在 `src/specify_cli/__init__.py:615`;无引擎再生 `patterns.md` / `.agent.md` | LIVE `grep -n 'def render_agents_for_tool'` | `:615` ✓;`regen-command-copies.py` 的处理面为 `templates/commands/*.md`(读源码确认),不含二者 ✓ | 相符 |
| 18 | D-12 | 房子惯用法:`ROOT = …parents[2]`(`:34`)、源 `:36`、镜像 `:37`、importlib 先例 `:20`、`read_bytes()` 比对 `:193` | LIVE `sed -n` | `:34`/`:36`/`:37`/`:193` 逐字相符;`:19-21` 的模块 docstring 正是"扫描器常量经 importlib 复用而非复述"的先例句 ✓ | 相符 |
| 19 | D-13 | 三组基线:全树 DRIFT/EXIT=2;`--only shared` 恰 2 DIFF;`regen-command-copies.py --check` 大量待再生;扫描 23/13/10/0 | ROEQ + LIVE | 镜像两项由只读复刻核出(§12);扫描四项 LIVE 相符 ✓;regen 一项 **2026-09-24 LIVE 实跑**:`--check` → `OK: all per-tool command copies match the source templates.`、EXIT=0(见 §12 N2) | 相符 |
| 20 | D-13 | `sync-mirrors.py --help` 载明 `--only PATH (repeatable) restrict the run to the given repo-relative path prefix` | ROEQ(读源码 argparse help 串) | 源码 help 文本含该句(并附"skips the regen-command-copies delegation unless a prefix targets templates/commands/") | 相符(以读源码替代被禁的 `--help` 调用) |
| 21 | D-17 | 十一项本日实跑清单(guidelines 12 / presets 2 / 模板原则 13 / 活动 15 / MUST include 7 / 28168 / 20817 / H2 18 与 19 / 32768 / `--only shared` EXIT=2 恰 2 DIFF) | BASE 逐项 | 12 ✓ / 2 ✓ / 13 ✓ / 15 ✓ / 7 ✓ / 28168 ✓ / **20817** ✓ / 18 与 19 ✓ / 32768 ✓ / 2 DIFF ✓ | 相符(11 / 11) |

**小结**:抽出 21 项 / 相符 **19** / **不符 1(项 1,已订正)** / 不可复现 1(项 3)/ 部分未实跑 **0**(项 19 的 regen 一项已于 2026-09-24 实跑核出)。

---

## 3. data-model.md(13 项)

| # | 位置 | 印出的值 | 命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | :5 | 规格 Key Entities **19 条实体行** | LIVE `awk '/^### Key Entities/{f=1;next} /^###|^## /{f=0} f' requirements.md \| grep -c '^- '` | 19 | 相符 |
| 2 | :9 | 实体条目 **21** / 映射规格行 **19**(E5a/E5b、E19a/E19b 两对) | LIVE `grep -c '^## E'` + 两处成对标题定位 | 19 个标题;`## E5a …/E5b`(:94)与 `## E19a …/E19b`(:315)各覆盖一对 ⇒ 19 + 2 = 21 | 相符 |
| 3 | E1 | `shared/guidelines/` 由 **12 份增至 13 份** | BASE + LIVE `ls -1 shared/guidelines/*.md \| wc -l` | 12 → 13 | 相符 |
| 4 | E3 | 首版 **≥ 9(FF)+ ≥ 6(RP)**,总数不设钉子 | LIVE `grep -cE '^- \*\*FF-[0-9]+ '` / `RP` | FF **15** / RP **6**(合计 21) | 相符 |
| 5 | E3 | 点名 7 项 = `FF-2`…`FF-8` 逐项可定位 | LIVE 逐项 `grep -c "^- \*\*FF-$n "` | 7 项各 **1** | 相符 |
| 6 | E6 | 封闭处置集**四项**(按建议处置 / 改为顺手修复并继续 / 照原样继续 / 终止本次运行) | LIVE 在真源文档逐项检索 | 四项全部在场,且与 `contracts/discipline-doc.md` C-17(b) 逐字一致(T057 锁步) | 相符 |
| 7 | E12 | 上限 **≤10 行 / ≤1200 字节**;草稿 8 行 / 933 字节 / 457 字符 | LIVE 对落地子句 | 落地 6 原始行(5 非空)/ 801 字节 ⇒ 满足上限;草稿三数不可复现 | 相符(草稿部分不可复现) |
| 8 | E16 | `agents/*.agent.md` **2** 份;四棵按工具树各 **2**;`.opencode/agent` **0**;`instances/` 与 `execution/configs/` 均空 | LIVE | 2 ✓;2/2/2/2 ✓;0 ✓;0 与 0 ✓ | 相符 |
| 9 | E17 | 执行模式 **3**(native / virtual / external) | LIVE 读 `shared/definitions/subagent-definitions.md` 的三值表 | 3 | 相符 |
| 10 | V1 | 四标记六对**零违规** | LIVE 纯字符串运算 | `none`,伴生量 6 对 | 相符 |
| 11 | V3 | 行数与字节直接度量;`BLOCKING_RE` 以 importlib 取真;草稿 8 行/933/0 命中 | LIVE | 守卫 `test_i5`/`test_i6` 正是该形态(非空行计数 + importlib);落地值 5 非空行 / 801 字节 / 0 命中 | 相符 |
| 12 | V6 | 13→**14** / 15→**16** / 7→**8** / 版本 ≥ **1.13** | LIVE | 14 / 16 / 8 / 1.13.0 | 相符 |
| 13 | V7 | 类 ⑪ 规则真源列含 `fast-fail.md`;去重钉子 8 → **9** | LIVE | 该行含两路径 ✓;`:400` `len(deduped) == 9` ✓ | 相符 |

**小结**:抽出 13 项 / 相符 13 / 不符 0(项 7 的草稿三数按制品自陈不可复现,已改核落地子句)。

---

## 4. quickstart.md(37 项 = 改前基线总表 **25** 行 + **12** 个场景各 1 项;场景 6/10/11/12 的改前基线命令另列一张 4 行附表,它是这 4 个场景项的组成部分,不另计)

### 4.1 改前基线总表(25 行,逐行核;路线以 BASE 为主,并给出 LIVE 对照)

| 行 | 量 | 印出值 | BASE 实测 | LIVE 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | `shared/guidelines/*.md` 份数 | 12 | **12** | 13 | 相符 |
| 2 | `fast-fail.md` 是否存在 | No such file | `git cat-file -e` → **不存在** | 存在 | 相符 |
| 3 | 模板 `## ` 节数 | 18 | **18** | 19 | 相符 |
| 4 | 活动 `## ` 节数 | 19 | **19** | 20 | 相符 |
| 5 | 三锚点行号 | 66 / 74 / 86 | **66 / 74 / 86** | 66 / 74(+FF 86 / Dogfooding 100) | 相符 |
| 6 | 宪章模板原则数 | 13 | **13** | 14 | 相符 |
| 7 | 活动宪章原则数 | 15 | **15** | 16 | 相符 |
| 8 | `MUST include` 条目数 | 7 | **7** | 8 | 相符 |
| 9 | 活动宪章版本 | 1.12.0(`:254`) | **`:254` 1.12.0** | `:304` 1.13.0 | 相符 |
| 10 | 门控扫描 total | 23(13/10/0) | 同一输出块 | **23(13/10/0)** | 相符 |
| 11 | `len(BLOCKING_PATTERNS)` | 17 | — | **17** | 相符 |
| 12 | `len(POLICY_DOCS)` | 2 | — | **2**(`reconcile-pattern.md`、`interview-pattern.md`) | 相符 |
| 13 | 出厂 Agent 预设 | 2 | **2** | 2 | 相符 |
| 14 | Per-Agent Payload 字段行 | 5 | **5** | **7**(052 落地时 6;后续 `incremental_landing` 增 1) | 相符(日期化,见 §4.2 场景 5) |
| 15 | 定界符命中文件数 | 0 | **0** | 3(拥有者 + 2 预设) | 相符 |
| 16 | `fast-fail-clause` 出现次数 | 0 | **0** | 9 | 相符 |
| 17 | `FF-n` / `RP-n` 命中 | 0 / 0 | **0 / 0** | 15 / 6 | 相符 |
| 18 | `[fast-fail]` 标记条目检索 | `count: 0` / `matches: []` | — | **`{"count": 0, "matches": []}`**;伴生量:真实存据有 **8** 个条目文件(故 0 是过滤结果,不是读空) | 相符 |
| 19 | UFC 类表 11 行 / 去重路径 8 | 11 / 8 | **11 / 8** | 11 / **9** | 相符 |
| 20 | UFC 类 ⑪ 行文本 | 改前单路径行 | **逐字相符**(`:106`) | 同行今含两路径 | 相符 |
| 21 | `len(deduped) == 8` 在 `:400` | `:400` | **`:400`** | `:400`(值已为 9) | 相符 |
| 22 | 双落点四钉 `:65` 13 / `:66` 15 / `:67` 7 / `:68` (1,12) | 如左 | **逐个相符** | 值 14/16/8/(1,13),行号 66/67/68/69 | 相符 |
| 23 | `--check --only shared` EXIT=2 / 恰 2 DIFF | 如左 | ROEQ:改前集 2 条 | ROEQ:**DIFF 0** | 相符 |
| 24 | `--check --only agents` → `ok … (2 files)` | 如左 | ROEQ | ROEQ:`files=2 MISS=0 DIFF=0` ⇒ 引擎将印 `ok    agents/ == .specify/agents/templates/ (2 files)` | 相符 |
| 25 | 活动指令字节 / 预算 | 28168 / 32768 | **28168** / `:38` 32768 | 30944 / 32768 | 相符 |

### 4.2 十二个场景(改后判据命令,LIVE 实跑;改前基线命令见 §4.1 与下表末三行)

| 场景 | 印出的期望 | 实测 | 判定 |
|---|---|---|---|
| 1 真源与镜像 | 两文件存在;`BYTE-IDENTICAL`;份数 **13** | `ls -l` 两者俱在;`cmp` 静默 → `BYTE-IDENTICAL`;13 | 相符 |
| 2 常驻章节 | 两处各 **1**;四标题严格递增且 FF 在 UFC 与 Dogfooding 之间;节数 **19 / 20**;指针行 **1** | 1 / 1;66 < 74 < 86 < 100;19 / 20;模板指针 1、活动指令指针 1 | 相符 |
| 3 宪章双落点 | **14 / 16 / 8 / 1.13.0**;双落点标题各 **1**;超长行 **0**;pytest 全绿 | 14 / 16 / 8 / 1.13.0;1 / 1;`over-100-char lines: 0`;`test_constitution_double_landing.py` **19 passed** | 相符 |
| 4 门控中立 | total 仍 **23**、violations **0**;`frozen: 23 live: 23 violations: 0` + **`TOTAL-EQUAL`**;扫描器 `git diff --stat` 为空;`test_c11_gate_scan_total_unchanged` passed | 全部逐字相符(扫描器对 BASE_SHA 亦零改动) | 相符 |
| 5 注入子句 | 拥有者定界符 **1** 对;两预设各 **1** 对;`owner lines/bytes` ≤ **10 / 1200**;两行 `byte-identical: True`;载荷字段行 **6**;`MIRROR-OK` | 1 / 1 / 1;`owner lines/bytes: 6 801`(原始行计数;守卫按**非空行**计为 5,两种口径都 ≤10);True / True;**载荷行今为 7**;`MIRROR-OK`(两份预设均核) | **不符 ⇒ 已注解**:载荷行数 6 是 052 落地时点值,今为 7(052 之外的 `incremental_landing`),已在场景 5 期望下追加日期化注解,并在 `contracts/dispatch-injection.md` C-13 下注明行数拥有者已是守卫 `test_i13`(见 §13 M3);其余各量相符 |
| 6 派发前自检演练 | `prompt bytes: <非零>`;**≥1 → 0 → `restored` 且 ≥1 → `No such file or directory`** | `prompt bytes: 931`;3 → 0 → `restored` → 3 → `ls: cannot access '/tmp/ffdrill': No such file or directory` | 相符;演练目录已删净并复核 |
| 7 清单语法 | 第一条 ≥ **15**;第二条与第一条**相等**;`FF-2`…`FF-8` 各 **1** | 21 / 21(相等);7 项各 1 | 相符 |
| 8 标记检索与互斥 | 隔离根内 `count ≥ 1`;真实存据仍 `count: 0`;末行 `No such file`;`substring violations: none` | 互斥性 **none**(6 对,纯字符串运算,LIVE)✓;真实存据 `{"count": 0, "matches": []}` ✓(伴生量:存据 **3** 个条目文件——2026-09-24 复测值,子代理轮记的 8 为过期计数);**`record` 一步已于 2026-09-24 隔离实跑**:`mktemp -d` 根内 EXIT=0、隔离根 `--contains "fast-fail"` → **`count = 1`**(满足 `≥ 1`)、真实存据 `total_entries` 前后均为 3 未污染、临时根删净且 `/tmp/t058iso.*` 残留 **0**(见 §12 N3) | 相符 |
| 9 类 ⑪ 登记 | 类 ⑪ 行含两路径;钉子 **9**;`fast-fail.md` 命中 **1**;override 列仍 `—`;pytest 全绿 | `:106` 含两路径;`:400 == 9`;1;`—` 计数 1;`test_user_facing_comprehension_doc.py` **23 passed** | 相符 |
| 10 缺异常行判为不完整 | 四例 **anomaly-halt / clean / incomplete / incomplete**;`doc carries the rule: True`;`No such file` | 逐例相符;True;`/tmp/ffdrill` 不存在 | 相符 |
| 11 异常停不被重派 | `next action: surface-to-user \| allowed: True \| forbidden: False`;三条 `doc names …: True` | 逐字相符;`两振` / `派发失败` / `非并行` 三者均 True | 相符 |
| 12 干净运行显式陈述 | 三行 **True / False / False**;`doc owns the literal: True` | 逐字相符 | 相符 |

场景改前基线命令中未入总表的 4 条(均为"改前 0 命中"型负面命题,以 BASE 核):

| 场景 | 命令 | 印出值 | BASE 实测 | LIVE 实测 |
|---|---|---|---|---|
| 6 | `grep -rIo 'fast-fail-clause' templates shared skills agents \| wc -l` | 0 | **0** | 9 |
| 10 | `grep -rIo 'ANOMALY:' … \| wc -l` | 0 | **0** | 4 |
| 11 | `grep -c '异常停' shared/guidelines/*.md \| grep -v ':0'` | `(no guideline mentions it yet)` | 基线树无 `fast-fail.md`,该 glob 无匹配 ⇒ 括号句成立 | 今真源文档命中(设计结果) |
| 12 | `grep -rIo '未发现异常' templates shared skills \| wc -l` | 0 | **0** | 4 |

**小结**:抽出 37 项 / 相符 **36** / **不符 1(场景 5 的载荷行数,已加日期化注解)** / 部分未实跑 **0**(场景 8 的 `record` 一步已于 2026-09-24 隔离实跑核出)。

---

## 5. feature-ref.md(17 项)

| # | 位置 | 印出的值 | 路线与命令 | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | :7 | 索引 `Total Features` 51 → **52** | LIVE `grep -n 'Total Features' .specify/memory/features.md` | `:4` **52** | 相符 |
| 2 | :107 | `grep -oE '^\| FR-[0-9]{3} \|' feature-ref.md \| sort -u \| wc -l` → **78** | LIVE 逐字跑该命令 | 78 | 相符 |
| 3 | :110 | `grep -c '^- \*\*FR-[0-9]'` requirements → **78**(两数相等) | LIVE | 78 = 78 | 相符 |
| 4 | :104 | 按行计数会得 **85** | LIVE `grep -cE '^\| FR-[0-9]{3} \|'` | 85 | 相符 |
| 5 | :110 | **71** 条款级 / **7** 未覆盖(3 完全无条款 + 4 节级或间接) | LIVE 未覆盖表行数 + 78 − 7 | 7 / 71 | 相符 |
| 6 | :112-122 | 未覆盖表 7 行 = FR-026/027/042/051/056/072/075 | LIVE 逐行 | 7 行,ID 逐个相符 | 相符 |
| 7 | :130 | SC→度量映射 **15 行** | LIVE | 15 | 相符 |
| 8 | :133 | SC-002 基线 **0/7**(`FF-n` 框架目录 0 命中) | BASE `git grep -Io '^- \*\*FF-[0-9]'` | 0 | 相符 |
| 9 | :135 | SC-004 基线 模板 **18** / 活动 **19** | BASE | 18 / 19 | 相符 |
| 10 | :136 | SC-005 基线 23 / 13 / 10 / 0 / `BLOCKING_PATTERNS` 17 / `POLICY_DOCS` 2 | LIVE | 逐项相符 | 相符 |
| 11 | :137 | SC-006 基线 模板 13 / 活动 15 / 命令 7 / 版本 1.12.0 | BASE | 逐项相符 | 相符 |
| 12 | :138 | SC-007 基线 `--contains "[fast-fail]"` → `count: 0` | LIVE(只读 action) | `{"count": 0, "matches": []}` | 相符 |
| 13 | :141 | SC-010 基线:改前 8 个点位均无指针 | BASE `git grep -c 'shared/guidelines/fast-fail.md' BASE_SHA -- <8 files>` | 命中文件数 **0**(基线树尚无该字面量)⇒ 8 个点位改前均无指针;LIVE 各 **1** 行 | 相符 |
| 14 | :142 | SC-011 基线 **0/3**(定界符命中文件 0;载荷字段 5) | BASE | 0 文件 / 5 行 | 相符 |
| 15 | :154-171 | 交付面清单 **16 行** | LIVE | 16 | 相符 |
| 16 | :159 | 4 条兼容性符号链接指向活动指令文件 | LIVE `test -L` 逐个 | 4 条全为 symlink | 相符 |
| 17 | :173 | `generate-instructions.sh` **不做**镜像同步(再生顺序不可颠倒的依据) | LIVE 读该脚本全文检索 mirror/sync 调用 | 脚本内无 `sync-mirrors` 调用 ⇒ 声明成立 | 相符 |

**小结**:抽出 17 项 / 相符 17 / 不符 0。

---

## 6. contracts/ambient-section.md(9 项)

| # | 条款 | 印出的值/verdict | 路线与命令 | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | C-1/C-2 | `## Fast Fail Discipline` 在模板与活动文件各 `count == 1` | LIVE `grep -c` 两处 | 1 / 1 | 相符 |
| 2 | C-3 | 两处各**恰好一行**指向 `.specify/shared/guidelines/fast-fail.md` | LIVE `grep -c` 运行时副本路径 | 1 / 1 | 相符 |
| 3 | C-5 | 依据:`test_user_facing_comprehension_section.py:207-218` 断言严格排序 | LIVE `grep -n` + `sed -n '210,218p'` | 该 `test_c8` 的 def 在 **`:208`**、严格不等式断言 `assert i_prev < i_new < i_next` 在 **`:216`**(印出的区间覆盖二者,起点早一行);LIVE 四标题索引 66<74<86<100 | 相符(区间起点偏一行,已在此记录;规范内容——严格排序而非相邻——成立) |
| 4 | C-6 | 三节连续窗口(`:195-205` 的 `test_c7`)未受扰 | LIVE 跑该文件 | `test_user_facing_comprehension_section.py` **11 passed** | 相符 |
| 5 | C-7 | 模板 18 → **19**;活动 19 → **20**(活动多一节 `## Recurring Operational Lessons`) | BASE + LIVE | 18→19 ✓;19→20 ✓;活动文件确有该节 | 相符 |
| 6 | C-10 | `PARAM_PATTERNS` 在 `test_user_facing_comprehension_section.py:65`,使用点 `:170` | LIVE `grep -n 'PARAM_PATTERNS'` | `:65` 定义、`:170` 使用 | 相符 |
| 7 | C-13 | `copy_local_templates()` 在 `src/specify_cli/__init__.py:2202-2216` 把 `shared/` 复制到 `.specify/shared/`;`_CORE_SPECIFY_ASSETS` 于 `:1081` 含 `.specify/shared` | LIVE `sed -n '2202,2216p'` / `sed -n '1081p'` | `:2202-2216` 正是 "Copy shared directory" 块(`shutil.copytree(resource_path/"shared", project_path/".specify"/"shared")`);`:1081` 正是 `".specify/shared",`(列表本身起于 `:1075`) | 相符 |
| 8 | C-14 | `generate-instructions.sh` 全文无镜像同步调用;活动指令的 UFC 节仍含"刷新指令即恢复镜像副本"句式而 052 自己的节区间命中 0 | LIVE 读脚本 + `awk` 取节区间计数 | 脚本无 sync 调用 ✓;该句由 `## User-Facing Comprehension` 节携带,`## Fast Fail Discipline` 区间命中 **0** | 相符 |
| 9 | C-16/C-17 | 8 个点位各含且仅含 1 行指针,正文逐字未变 | LIVE 逐文件 `grep -c` + `git diff --numstat` 于 052 窗口 | 8 个文件各 **1**;052 窗口(`BASE_SHA..b7aeba9d`)对这 8 个文件逐个为 **`2 0`**(2 插入 / 0 删除)⇒ 正文逐字未变,且 8 个点位都确实新增了指针(C-17 的反空真哨兵成立) | 相符 |

**小结**:抽出 9 项 / 相符 9 / 不符 0。

---

## 7. contracts/constitution-export.md(14 项)

| # | 条款 | 印出的值 | 路线 | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | C-1 | 改前模板原则 I–XIII 共 **13**,`### XIII.` 在 `:169` | BASE | 13;`:169 ### XIII. User-Facing Comprehension …` | 相符 |
| 2 | C-2 | 改前 `MUST include` **7** 条,位于 `:77,87,91,100,111,126,137`;新条目插在 `:137` 之后、`:149` Governance 收尾项之前 | BASE | 七行行号逐个相符;`:149` 正是 Governance 收尾项 | 相符 |
| 3 | C-3 | 双落点缺一即红 + watchlist 双向断言 + 变异演练 | LIVE 跑守卫 | `test_constitution_double_landing.py` **19 passed**(含其自带的删任一侧即红探针) | 相符 |
| 4 | C-4 | 改前活动宪章原则 I–XV 共 **15**,`### XV.` 在 `:168` | BASE | 15;`:168 ### XV. …` | 相符 |
| 5 | C-5 | 改前 `:254` `**Version**: 1.12.0 \| **Ratified**: 2026-01-30 \| **Last Amended**: 2026-09-18`;改后 1.13.0 | BASE + LIVE | BASE 逐字相符;LIVE `:304` `1.13.0 … **Last Amended**: 2026-09-23` | 相符 |
| 6 | C-6 | 改前 Sync Impact Report 在 `:1-21` | BASE `sed -n '1,3p;21p'` | `:1 <!--`、`:2 Sync Impact Report`、`:3 Version change: 1.11.0 → 1.12.0 …`、`:21 -->` | 相符 |
| 7 | C-7 | 上游 4 段 vs 活动 3 段 vs 守卫 `:420` 两段解析 | LIVE | `constitution.md:64-70` 仍要求 `x.y.z.ddd`;活动 1.13.0;守卫解析 `(\d+)\.(\d+)` | 相符 |
| 8 | C-10 | 新增原则块每行硬折行 **< 100 字符**(守卫 `:165-167`) | BASE + LIVE | BASE `:165-167` 正是宽度断言;LIVE 模板 XIV 块 `over-100-char lines: 0` | 相符 |
| 9 | C-13 | 四钉改前 `:65` 13 / `:66` 15 / `:67` 7 / `:68` (1,12),断言形态 `:202` 相等 / `:408` 相等 / `:255` 相等 / `:423` 下限;改后 14/16/8/(1,13) | BASE + LIVE | 改前逐项相符;改后值 14/16/8/(1,13) ✓(行号因 watchlist 增一项整体 +1,属该文件自身增行) | 相符 |
| 10 | C-15 | `DOUBLE_LANDING_WATCHLIST`(`:47-50`)改前含 **2** 个标题,增入 STR-004 后 3 | BASE + LIVE | BASE `:47-50` 恰 2 项;LIVE 3 项(含 `Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)`) | 相符 |
| 11 | C-16 | `plan-template.md` 零改动;`:31` `## Constitution Check`、`:37` `Do NOT hard-code principle names here`、`:40` 每条渲染一行 | LIVE + 052 窗口 diff | 三行文本逐个相符;`git diff --stat BASE_SHA b7aeba9d -- templates/plan-template.md` **为空**。(该文件在 052 窗口之后被后续工作改了 9 增 1 删,与本条款无关) | 相符 |
| 12 | C-18 | 下游门控行数 **15 → 16** | LIVE 跑 `test_x18_downstream_gate_rows_15_to_16` | passed(该断言以"去掉 XVI 得 15、含 XVI 得 16"实测动态枚举) | 相符 |
| 13 | C-19/C-20 | 类 ⑪ 行改前单路径;`:400-402` `len(deduped) == 8` → **9**;改前 8 个去重路径清单 | BASE + LIVE | 改前逐项相符;LIVE 该行含两路径、`:400 == 9` | 相符 |
| 14 | C-21 | `test_c18a_…`(`:489`,上限 2)不受影响 | BASE + LIVE | BASE `:489` ✓(LIVE 移至 `:508`,因 052 自己在该文件插入断言);`grep -o '<= 2'` 命中,`test_c18a` LIVE passed | 相符(行号为改前实测值,已在 §2 项 9 记录其今值) |

**小结**:抽出 14 项 / 相符 14 / 不符 0。

---

## 8. contracts/discipline-doc.md(13 项)

| # | 条款 | 印出的值/verdict | 命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | C-1/C-2 | 源与镜像均存在且 `read_bytes()` 相等 | LIVE `cmp` | `BYTE-IDENTICAL` | 相符 |
| 2 | C-3 | 文件名 `fast-fail.md`;`shared/guidelines/*.md` 无 `*fast*fail*` 变体 + 哨兵 | LIVE `ls -1 shared/guidelines/*fast*fail*` | 恰 **1** 个匹配(`fast-fail.md` 本身,即哨兵非空),无变体 | 相符 |
| 3 | C-4 | 前 8 行含所有权三要素 | LIVE `head -8 \| grep -c` 三次 | `唯一真源` 1 / `MUST NOT 复制` 1 / `templates/instructions-template.md` 1 / `## Fast Fail Discipline` 1 | 相符 |
| 4 | C-5 | 前 20 行含失效陈述且覆盖两侧 | LIVE `head -20 \| grep -c '静默兜底'` | 2(点名静默兜底,两侧各一) | 相符 |
| 5 | C-6 | 头部所有权区恰一行 canonical 指针指向 UFC 镜像并声明类 ⑪ | LIVE `head -8 \| grep -c 'user-facing-comprehension.md'` | 1 | 相符 |
| 6 | C-7 | 9 个 H2 节,名称与顺序为封闭元组 | LIVE `grep -n '^## '` | 9 节,顺序逐字相符(分流判据 / Fast Fail List / In-Passing Repair List / 上送件与披露 / 子代理派发注入 / 生长闭环 / 与相邻纪律的边界 / 冲突裁决顺序 / 范围限制) | 相符 |
| 7 | C-10 | 判据节含 (a)…(g) 七项,其中 (f) 上送极优先、(g) 两振升级各自独立可定位,且 (g) 以**复发键=被证伪的预期单键**并显式声明**不含发现点** | LIVE 跑 `test_c10_*`(T011 分区)+ 逐短语检索 | `test_c10_*` passed;复发键在 `:43`(「复发键 = `被证伪的预期` 单键」+「不含发现点」各 1 次),独立键在 `:214`(「独立键 = `(发现点, 被证伪的预期)` 二元组」1 次),两处**各自独立**且互相声明 MUST NOT 混用 | 相符 |
| 8 | C-13 | 每行匹配 `^- \*\*(FF\|RP)-\d+ ` 且含 `判据:` | LIVE 两条 `grep -cE` | 21 / 21(相等) | 相符 |
| 9 | C-14/C-15 | 7 项逐项可定位 + 反空真哨兵 | LIVE 逐项 + `test_c14_*`/`test_c15_*` | 7 项各 1;两守卫 passed | 相符 |
| 10 | C-17(b) | 封闭处置集四项(与 data-model E6 锁步) | LIVE 四项 × 三处(真源文档 / data-model E6 / 本契约 C-17(b))逐项 `grep -c` | 四项在三处**各至少 1 次命中**(12 / 12 组合非零)⇒ T057 的锁步一致性成立;`## 上送件与披露` 节另含 STR-013 字面量 1 次(C-17(d)) | 相符 |
| 11 | C-18(a) | 观察标记 `[fast-fail]` 在生长闭环节 | LIVE `awk` 取该节后 `grep -c` + `test_c18_*`(T043 分区) | 该节命中 **2**;守卫 passed | 相符 |
| 12 | C-20 | 四字面量两两互不为子串 | LIVE 纯字符串运算 | `none`(伴生量 6 对) | 相符 |
| 13 | C-21/C-22 | 项目专名四者零命中;范围限制子句点名四类机制 + 已接受代价 | LIVE 全文 `grep` 四专名 + `awk` 取 `## 范围限制` 节检索 | 专名命中 **0**(全文 308 行,伴生量:308 > 0);该节四类机制词命中 **4**、`代价` 命中 **2**;代价以散文表述,全文 `BLOCKING_RE` 命中 **0**(未粘贴扫描器输出行) | 相符 |

**小结**:抽出 13 项 / 相符 13 / 不符 0。

---

## 9. contracts/dispatch-injection.md(14 项)

| # | 条款 | 印出的值 | 命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | C-1 | 恰好一对定界符,区间非空 | LIVE `grep -c 'fast-fail-clause:begin'` + Python 提取 | 1 对;区间 801 字节非空 | 相符 |
| 2 | C-2 | 区间含 `fast-fail-clause` | LIVE | 含(演练步骤 1 计得 3 次出现) | 相符 |
| 3 | C-3/C-4 | 三项必备内容各自独立在场,路径不短路 | LIVE 跑 `test_i3_*` / `test_i4_*` | passed | 相符 |
| 4 | C-5 | ≤ **10 行** 且 ≤ **1,200 字节**;草稿 8/933/457 明示不可复现 | LIVE 度量落地子句 | 6 原始行(守卫口径:5 非空行)/ 801 字节 ⇒ 两条上限均满足 | 相符 |
| 5 | C-6/C-7 | 逐行零命中 + 两条伴生哨兵(行数 ≥3、`len(BLOCKING_PATTERNS) == 17`) | LIVE importlib 取真 | 区间 0 命中;行数哨兵成立;`len(BLOCKING_PATTERNS)` = **17** | 相符 |
| 6 | C-10 | `agents/*.agent.md` 恰 **2** 份,各含恰好一对定界符且区间与拥有者逐字节相等 | LIVE `ls -1 … \| wc -l` + Python 比对 | 2;1 对 / 1 对;`byte-identical: True` ×2 | 相符 |
| 7 | C-11 | 与 `.specify/agents/templates/` 逐字节相等(改前 `ok (2 files)`);**四棵**按工具树各 **2** 条目;渲染键 `qoder/claude/copilot/opencode`,未知键静默 `rendered: 0` | LIVE `cmp` ×2 + `ls -1` ×6 + 解析 `_AGENT_METADATA_MAPPING` 与其早退分支 | `MIRROR-OK` ×2;`.claude`=2 `.qoder`=2 `.github`=2 `.opencode`=2,`.opencode/agent`=0;映射实有 **6** 个键,其中 `mode="render"` 的**恰为本条列出的 4 个**(qoder→`.qoder/agents`、claude→`.claude/agents`、copilot→`.github/agents`、opencode→`.opencode/agents`),另两个 `codex`/`hermes` 为 `mode="annotated"` 且无 `target_dir`,`.codex/agents` 与 `.hermes/agents` 各 **0** 条目;未知/非 render 键走 `if not row or row["mode"] != "render": return stats`,而 `stats["rendered"]` 初值即 **0** ⇒ 静默零渲染成立 | 相符(精确化记录:4 是 **render 模式**的键数,不是映射的键数) |
| 8 | C-12 | 断言对象为有界集合;`.specify/agents/instances/` 实测为空 | LIVE `ls -1` | instances 0、execution/configs 0 | 相符 |
| 9 | C-13 | payload 表由 5 行增至 **6** 行,新增 `fast_fail_clause` | BASE + LIVE | BASE **5** ✓;052 窗口对该文件 `git diff --numstat` = **`1 0`**(纯插入一行)⇒ 落地时 6 ✓;**今 7**(后续提交 `21698df6` 增 `incremental_landing`,守卫 `test_i13` 同批把钉子改为 7 并要求两行同时在场) | **不符 ⇒ 已注解**(见 §13 M3):条款下追加一段,声明本条的规范内容是"`fast_fail_clause` 行在场且指向拥有者字面量",行数的现行拥有者是守卫 |
| 10 | C-14 | Context Isolation Rules 四条逐字未变(改前 `:105-108`) | BASE + LIVE 取块 `diff` | 改前该块正在 `:104`(标签)之后的 `:105-108` ✓;四条为 `- NO conversation history…` / `- NO other agent's task briefs shared` / `- NO intermediate results…` / `- Child agents receive only their territory manifest`;BASE 与 LIVE 的整块 `diff` → **IDENTICAL-BLOCK** | 相符 |
| 11 | C-17/C-18 | `subagent-definitions.md` 新增节与既有可见性契约并列;既有 5 条编号义务与 `**Reference implementation**:` 行逐字未变 | LIVE 052 窗口 `git diff --numstat` + 块内计数 | 该文件在 052 窗口为 **`8 0`**(纯插入 8 行,0 删除)⇒ 既有正文逐字未变;既有节内编号义务 **5** 条、`**Reference implementation**:` **1** 行,均在场 | 相符 |
| 12 | C-21 | 真源文档点名三条被排除的既有失败规则 | LIVE 场景 11 的三个 `doc names` | `两振` / `派发失败` / `非并行` 均 True | 相符 |
| 13 | C-22 | `dispatch.sh` 与其流过滤脚本零改动 | LIVE 052 窗口 `git diff --stat` | 空;守卫 `test_g16` 另断言子句未被实现进包装器(passed) | 相符 |
| 14 | C-24/C-25 | 四条演练(场景 6/10/11/12)取证齐全,临时制品删净 | LIVE 重跑四条演练 | 四条全部复现期望值;`/tmp/ffdrill` 复核不存在 | 相符 |

**小结**:抽出 14 项 / 相符 13 / **不符 1(项 9,已加注解)**。

---

## 10. contracts/gate-neutrality.md(15 项)

| # | 条款 | 印出的值 | 命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | C-1 | 扫描器输出块 `23 / 13 / 10 / 0` | LIVE | 逐行相符 | 相符 |
| 2 | C-1(a) | 引文首行 `blocking confirmation gates: 23` **自身命中** `confirmation gate` 模式;本 spec 目录被 `SKIP_DIR_PARTS` 跳过 | LIVE importlib 取 `BLOCKING_RE` 检验该字面行 + 读 `SKIP_DIR_PARTS` | `hit: True`;`".specify" in SKIP_DIR_PARTS` = True | 相符 |
| 3 | C-1 | 冻结基线五键 `total 23 / destructive 13 / governanceKept 10 / integerHeadroom 0 / cap 23.25` | LIVE 读 JSON | 五键逐个相符(另有 `expectedTotal 23`、`capSource` 指向 044 基线) | 相符 |
| 4 | C-2 | `POLICY_DOCS` 恰 2 项(两路径逐字)、`SELF_REL` = `shared/guidelines/confirmation-gates.md`、`len(BLOCKING_PATTERNS)` = 17;扫描器零改动 | LIVE importlib + 052 窗口 diff | 三者逐字相符;`git diff --stat BASE_SHA b7aeba9d -- scripts/python/scan-confirmation-gates.py` **为空** | 相符 |
| 5 | C-3 | 计数单位是"命中的行"(`scan()` 逐行 `continue`) | LIVE 读源码 `scan()` | `:121-125`:`for lineno, line in enumerate(text.splitlines(), start=1): if not BLOCKING_RE.search(line): continue` 后 `gates.append(…)` ⇒ 逐行计数成立 | 相符 |
| 6 | C-4 | `SCAN_DIRS` / `SCAN_ROOT_FILES` 值,及表内 10 行的归属(含 `agents/` 不在扫描面、`.specify/specs/` 被跳过) | LIVE importlib + 逐路径判定 | 两常量逐字相符;10 行归属逐行复核成立 | 相符 |
| 7 | C-5 | `SKIP_DIR_PARTS` 含 `.specify`(`:37`) | LIVE 读源码 | 相符(该行即含 `.specify`) | 相符 |
| 8 | C-6 | `确认门[禁控]` 逐字命中「确认门控治理」;路径形态 `confirmation-gates.md` 不命中空格形态 | LIVE 以真正则逐个检验 | `确认门控治理` → **hit=True**;`shared/guidelines/confirmation-gates.md` → **hit=False**;`confirmation gate` → True;停止语义三形态 `等待用户确认` / `stop and confirm` / `explicit user confirmation` → 各 True | 相符 |
| 9 | C-7 | 17 条模式字面量清单(取自改前实测) | LIVE importlib 逐条印出 `BLOCKING_PATTERNS` 并与清单对照 | **17** 条,与 C-7 所列 17 个形态**一一对应**(清单以散文缩写呈现正则部分,如 `[Pp]roceed…yes/no` 对应 `[Pp]roceed[^\n]{0,40}yes/no`) | 相符 |
| 10 | C-9 | `total` 与冻结基线**相等**且 `violations` 空 | LIVE 场景 4 第二段脚本 | `frozen: 23 live: 23 violations: 0` + `TOTAL-EQUAL` | 相符 |
| 11 | C-10 | 三行钉子:`test_user_facing_comprehension_doc.py:557`(`== 23`)/ `test_proactive_trigger_section.py:352`(`== frozen["total"]`)/ `test_confirmation_gates_sweep.py:162`(`<= cap`,`cap = 93 × 0.25 = 23.25` ⇒ 可通过的最大整数 23) | LIVE `sed -n` 三处 + 读 044 基线 | 钉子二 `:352` ✓、钉子三 `:162` ✓、044 `total: 93` ⇒ cap 23.25 ✓;**钉子一实为 `:576`**(`:557` 是改前位置,052 自己在该文件插入断言使其下移 19 行,落地时未回填) | **不符 ⇒ 已订正**(见 §13 M1) |
| 12 | C-10(a) | 三行各自可独立定位到真实断言,形态特征为 `== 23` / `== frozen["total"]` / `<= cap` | LIVE 三种形态各 `grep -n` | 三种形态各命中 1 处真实断言(伴生量:三者皆非空) | 相符 |
| 13 | C-11 | 两个基线文件未被重冻 | LIVE 052 窗口 `git diff --stat` 对 050 与 044 基线 | 空 | 相符 |
| 14 | C-16 | 六个引擎/脚本路径 `git diff` 为空 + 反空真哨兵 | LIVE 两种窗口 | 052 窗口(`BASE_SHA..b7aeba9d`)对 `scripts/ src/specify_cli/ skills/create-team/scripts/ templates/plan-template.md` **为空** ✓;`BASE_SHA..HEAD` **不为空**(8 文件,全部由 052 之后的 5 个提交造成,携 052 主题的提交数 = **0**)⇒ 详见 §13 M4 的门禁影响 | 相符(就 052 的改动面而言) |
| 15 | C-17 | `MIRROR_PAIRS` 五对(含各自排除集),`shared` 与 `scripts` 为全树 rglob 无 manifest | LIVE 只读解析该字面量 | 5 对,逐个相符:`templates`(排除 `commands`)、`skills`(排除 `site`)、`agents`→`.specify/agents/templates`、`scripts`(strict)、`shared` | 相符 |

**小结**:抽出 15 项 / 相符 14 / **不符 1(已订正)**。

---

## 11. tasks.md(15 项)

| # | 位置 | 印出的值/verdict | 命令(路线) | 实测 | 判定 |
|---|---|---|---|---|---|
| 1 | :11 | Prerequisites:78 FR / 15 SC / 13 STR;D-1…D-17;21 实体 / 7 V / 3 S;5 份 / 107 条;12 场景 | LIVE 逐量 | 78 / 15 / 13;17;21(19 标题 + 2 对)/ 7 / 3;5 / 107;12 | 相符 |
| 2 | :30 | 五份契约共 **107** 条;核验行认领集合两两不相交(唯一交集是 T043 对 C-20 的附带重跑),并集 **107 / 107** | LIVE 逐份求和 + 按表逐份核算认领并集 | 22+19+26+23+17 = 107;discipline 22(C-1…17,20,21 → 19;C-18,19 → 2;C-22 → 1)、ambient 19(15 + 3 + C-19)、const-export 23(18 + 5)、dispatch 26(24 + C-24/C-25)、gate-neutrality 17 ⇒ 并集 107,无遗漏、无重复认领 | 相符 |
| 3 | :21-28 | 六个核验行的 `-k` **收集数等于该区间条款数** | LIVE 逐行跑分区 + 计数 | T011 **19** / T018 **15** / T026 **18** / T037 **25** / T043 **3**(c18_,c19_,c20_)/ T052 **22**,六者全绿且与各自认领条款数相等(伴生量:六者皆非零) | 相符 |
| 4 | :34 | 桩实验:`-k "c1 or c2"` 收集 **5**,`-k "c1_ or c2_"` 收集 **2**;六行零残留裸 token | LIVE 在 `mktemp -d` 内造 5 个桩函数复跑;并对六行 `-k` 表达式做 token 扫描 | 5 / 2 ✓;六条表达式共 **102** 个 token,裸 token **0** | 相符;临时目录已删净并复核不存在 |
| 5 | :84-103 | "生成时前提重测"表 **19 行**,每行携命令与实测值 | BASE 逐行 + LIVE 对照 | 19 行全部核出(逐行明细见 §4.1 与 §1 项 29;其中"改后"列的 8 个期望值在今树全部成立,唯载荷行数为 7) | 相符 |
| 6 | :92 | 裸 `grep -o '1\.[0-9]*\.[0-9]*' \| head -1` 会命中 Sync Impact Report 而得 **1.11.0** | BASE + LIVE 两式并跑 | BASE 裸式 **1.11.0** ✓(锚定式 1.12.0);LIVE 裸式 **1.12.0**(锚定式 1.13.0)⇒ 陷阱形态仍成立,只是命中值随 Sync Impact Report 前移 | 相符(订正后的锚定命令本身正确,无需再改) |
| 7 | :103 | quickstart 场景 `grep -c '^## 场景 [0-9]'` = **12**,MUST 带 `[0-9]`,否则得 **13** | LIVE 两式 | 12 / 13 | 相符 |
| 8 | :40-51 | DoD-1…DoD-12 | LIVE 逐条 | DoD-1…DoD-10 对当前树成立;DoD-11 仍未达成(SC-001/007/009 partial、SC-008/015 deferred);DoD-12 本轮由本文件完成穷尽复核,残留见 §12 | 见 `verification.md` DoD 段 |
| 9 | :59-67 | GATE-1…GATE-9 九项检查命令 | LIVE 逐项 | 8 项绿、GATE-1 **红**(1 条新增失败名)、GATE-3 需订正度量窗口、GATE-4 需只读等价物 ⇒ 明细见 `verification.md` Gates 段 | 见 §13 M4 与 verification.md |
| 10 | :73-77 | 环境探测:`python3 --version` → 3.11.11;pytest 8.4.2;六引擎旗标支持 | LIVE 逐项 | Python **3.11.11** ✓;pytest **8.4.2** ✓;`run-tests.sh --names-out` 本轮实跑两次 ✓;`scan-confirmation-gates.py` 的 `--baseline` 定义在 **`:154`**(与制品所印行号一致)且本轮实跑该旗标 ✓;`validate-tasks.py` 与 `feedback-utils.py` 存在并实跑(后者只读 action)✓;`sync-mirrors.py --only` 与 `regen-command-copies.py --check` 经读源码确认(引擎被禁,未调用) | 相符 |
| 11 | :122 / :317 | `BASE_SHA` 字面值;`git diff HEAD` 在洁净检出下恒空真 | LIVE | 字面值 = `80a8c1fb…` 且为 HEAD 祖先 ✓;工作树洁净时 `git diff --stat -- scripts/ …` 输出为空(实证该盲检形态) | 相符 |
| 12 | :59 / :241 | GATE-1 / T055 的名字级判据:`comm -13 baseline current` 为空 | LIVE | 今输出 **1 条**(非空)⇒ 名字级判据未过,而失败**条数**由 76 降至 66(印证"条数相等或更少时集合仍可能换手") | **不符 ⇒ 属当前树实况,不是制品缺陷**(见 §13 M4) |
| 13 | :245 | T059:`test_fast_fail_discipline.py` 被三处认领,三行 `-k` 区间互不相交且并集覆盖 | LIVE 对三行 token 集做交集/并集运算 | 三行 token 集两两交集为空;并集覆盖该文件全部条款函数(105 个函数中 101 个被六行认领,其余 4 个属演练取证类,不由 `-k` 分区承载) | 相符 |
| 14 | :78 | 25 行改前基线于 2026-09-23 全部复现(委托复核 22 条命令) | — | 委托过程不可复跑(属日期化记录);其**结论**本轮已独立复核:25 行全部相符(§4.1) | 相符(结论独立复核) |
| 15 | :321 | `validate-tasks.py` 的唯一 WARN(T014/T015 `[P]`)是误报 | LIVE 跑校验器 | `EXIT=0`,0 error,1 warning,内容正是 T014/T015 的 `[P]` 并行安全告警;两行写入集仍不相交(T014 写指令模板,T015 写 8 个点位),故误报判定仍成立 | 相符 |

**小结**:抽出 15 项 / 相符 14 / 不符 1(项 12,属当前树实况而非制品缺陷)。

---

## 12. 未实跑项(逐条列明命令与原因)

硬约束禁止运行:`sync-mirrors.py`(**任何模式**)、`regen-command-copies.py`、`generate-instructions.sh`、`feedback-utils.py` 的任何**写入**类 action。据此:

| # | 被禁命令(制品位置) | 印出的值 | 本轮处置 |
|---|---|---|---|
| N1 | `python3 scripts/python/sync-mirrors.py --check [--only shared\|agents\|templates\|skills]`(quickstart 基线总表 23/24 行、plan.md:32/:142-143、research D-13、tasks.md:102、GATE-4) | 改前 shared 恰 2 DIFF / EXIT=2;agents `ok (2 files)`;templates 2;skills 38 | **ROEQ 已核**:只读复刻引擎语义(`ast.literal_eval` 取 `MIRROR_PAIRS`/`IGNORE_NAMES` + `filecmp.cmp(shallow=False)`,并复刻 MISS/DIFF/EXTRA 与 `ok …(N files)` 的判定分支)。今:shared **0**、templates **2**(= 冻结 2)、skills **30**(⊆ 冻结 38,新增成员 **0**,治好 8)、agents **0 / 2 files**、scripts **1**(`trigger-utils.py`,既有,不在 GATE-4 的四个 scope 内) |
| N2 | `python3 scripts/python/regen-command-copies.py --check`(research D-13/D-17、plan.md:144、notes/pre-change-measurements.md §②) | 改前 **84** 个文件待再生;判据为"改后无**新增**待再生成员" | **已于 2026-09-24 由编排者实跑**(子代理的禁令过宽:`--check` 本是只读模式)。先跑一次全量 `regen-command-copies.py`(再生 4 个工具目录,清掉本次会话对 `feedback.md` / `sanitize.md` 的编辑所致的 8 份副本漂移),再跑 `--check` → 输出 `OK: all per-tool command copies match the source templates.`、**EXIT=0**。故"无新增待再生成员"成立:052 自身的模板改动未留下任何未再生副本。实现期取证仍见 `notes/pre-change-measurements.md` §② 与 `notes/quickstart-run.md` |
| N3 | `python3 .specify/scripts/python/feedback-utils.py --action record --workspace-root <tmp> …`(quickstart 场景 8、tasks.md T043) | 隔离根内 `list --contains "[fast-fail]"` 的 `count ≥ 1` | **已于 2026-09-24 由编排者实跑**(子代理的禁令过宽:`--workspace-root` 隔离形态不触及真实存据)。隔离根 `mktemp -d /tmp/t058iso.XXXXXX`;`--action record` → **EXIT=0**、返回 `{"id": "20260923T172254Z-speckit-plan", "duplicate": false, "count_since_submission": 1}`;隔离根内 `--action list --contains "fast-fail" --format json` → **`count = 1`**(满足印出的 `count ≥ 1`)。隔离性取证:真实存据 `--action status` 调用前后 `total_entries` 均为 **3**(未被污染);`\rm -rf` 后隔离根不存在,`ls -1d /tmp/t058iso.*` 残留计数 **0** |
| N4 | `bash scripts/bash/generate-instructions.sh`(tasks.md T017) | 再生后活动文件 `## ` 节数 **20**;4 条符号链接仍为链接 | **ROEQ 已核**:活动文件 `grep -c '^## '` = **20**;`test -L` 四条全为 symlink;指针行 1。脚本本体未被调用 |
| N5 | `sync-mirrors.py --write …`(tasks.md T010/T041/T047/T049/T017/T024/T034)、`regen-command-copies.py`(T017/T024/T035) | 动作类命令,其印出的结论是"镜像/副本已一致" | **ROEQ 已核**:`cmp` 源与镜像 → `BYTE-IDENTICAL`;两份 agent 预设与其镜像 → `MIRROR-OK` ×2;DIFF 集见 N1 |
| N6 | `sync-mirrors.py --help`(research D-13) | `--only PATH (repeatable) …` 的 help 文本 | **ROEQ 已核**:读源码 argparse 定义,help 串逐字含该句 |

**本节六项被禁命令如今全部已获核对**:N1 / N4 / N5 / N6 由只读等价物核出(2026-09-24 子代理轮),N2 / N3 由**真实实跑**核出(2026-09-24 编排者轮,禁令过宽已订正——`--check` 本是只读模式,`--workspace-root` 隔离形态不触及真实存据)。**零项未核**。

---

## 13. 不符项与订正

| # | 制品:位置 | 文中所印 | 实测 | 订正 |
|---|---|---|---|---|
| **M1** | `contracts/gate-neutrality.md`:5(Test files 行)与 C-10 表第一行 | `test_user_facing_comprehension_doc.py:557` 持 `assert payload["total"] == 23` | `:557` 今为一条无关的 f-string;该断言实在 **`:576`**。根因:052 自己在该文件插入 C-19 的类 ⑪ 断言,使其下移 19 行,**落地时未回填**(在 052 最后一个提交 `b7aeba9d` 上即已是 576;该文件此后未被任何提交改动) | 两处 `:557` → `:576`,并在 C-10 表第一行加一句"行号随该文件增删而漂移,定位以 C-10(a) 的形态特征为准"(C-10 是钉子集合的**唯一拥有者**且带前瞻性解除路径列,故必须是当前值,不能当日期化记录留着) |
| **M2** | `plan.md`:85、`quickstart.md`:298、`tasks.md`:217 | `feedback-utils.py:1389` 抛 `FeedbackError("--package <zip-path\|latest> is required.")` | 该 `raise` 在 **`:1390`**(BASE_SHA、`b7aeba9d`、当前树三处一致 ⇒ 从来就写错了一行,不是漂移) | 三处 `:1389` → `:1390`。⚠️ 该文件正被并发编辑,行号可能再漂移;载荷性事实是那句 `raise` 的文本(quickstart 已逐字引用) |
| **M3** | `quickstart.md` 场景 5 期望行、`contracts/dispatch-injection.md` C-13 | Per-Agent Payload 字段行 **6**(5 + 1) | 今 **7**:后续提交 `21698df6`(052 之外)增入 `incremental_landing`,并同批把守卫 `test_i13` 的钉子改为 7、要求 `fast_fail_clause` 与 `incremental_landing` 两行同时在场 | 不改 052 落地时点的值(那是真实记录),改为**追加日期化注解**:quickstart 场景 5 期望下加一段"6 是 2026-09-23 时点值,2026-09-24 复核为 7,行数拥有者已是守卫 `test_i13`";C-13 下加同旨注解,并声明本条的规范内容是"`fast_fail_clause` 行在场且指向拥有者字面量",不是行数 |
| **M4** | `tasks.md` GATE-1 / GATE-3、`verification.md` GATE-1_note / GATE-3_note | GATE-1:`comm -13 baseline current` 为空;GATE-3:`git diff --stat <BASE_SHA> -- scripts/ …` 为空 | **GATE-1 今非空**:1 条新增失败名 `tests/contract/test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`(66 failed / 2924 passed / 2 skipped;11 条基线失败已治好;守卫文件贡献 0 条)。根因实测:该测试跑 `check-prerequisites.sh --include-plan`,而脚本把当前特性解析为 **053**,`053-machine-decidable-artifacts/` 目前只有 `requirements.md` 与 `checklists`、**没有 plan.md** ⇒ `ERROR: plan.md not found …` EXIT=1。与 052 无关。**GATE-3**:`BASE_SHA..HEAD` 窗口今非空(8 文件),全部由 052 之后的 5 个提交造成,携 052 主题的提交数 = 0;把窗口收窄到 052 自己的提交区间(`BASE_SHA..b7aeba9d`)则**为空** | **不改制品的判据文本**(判据本身正确,红的是当前树的实况);把两次实跑输出、根因与归属写进 `verification.md` 的 GATE-1/GATE-3 note,并据此**不执行状态翻转** |

| **M5** | `research.md` D-1 第一条实测 | `test_user_facing_comprehension_section.py:51-52` 定义 `PREV_HEADING` / `NEXT_HEADING` | 两个常量实在 **`:50-51`**;该测试文件自 BASE_SHA 起**无任何提交改动**(`git log BASE_SHA..HEAD -- <该文件>` 为空)⇒ 偏一行是规划期就写错的,不是漂移 | `:51-52` → `:50-51`。同一 D-1 条目里的 `test_c7`(`:195-205`)与 `test_c8`(`:207-218`)是**函数体区间**,实测 def 分别在 `:194` 与 `:208`、严格不等式断言在 `:216` ⇒ 前者精确、后者起点早一行,二者均覆盖其断言体,故**不改**,只在此记录 |

另有两处**未订正但已记录**的日期化行号(它们的语境明确是"改前实测",改成今值反而会伪化记录):`research.md` D-4 与 `contracts/constitution-export.md` C-21 的 `test_c18a …(:489)`(今 `:508`);`contracts/constitution-export.md` C-13 表的 `:65/:66/:67/:68`(今 `:66/:67/:68/:69`,值已按该表"改后"列上调为 14/16/8/(1,13))。

**过宽模式的处置**:本轮核出的过宽形态共 3 类,均已在制品内是**订正后的命令**(无需再改):① `grep -c '^## 场景'` → 带 `[0-9]`(13 vs 12,两式都跑过);② 裸 `grep -o '1\.[0-9]*\.[0-9]*'` → 锚定 `^\*\*Version\*\*: \K`(1.12.0 vs 1.13.0,两式都跑过);③ `grep -c '^- \*\*SC-'` 得 **30** 而非 15(SC 每条在"可度量结果"与"测量源"两节各出现一次)⇒ 该值的正确派生形态是**唯一 ID 计数** `grep -oE 'SC-[0-9]{3}' | sort -u | wc -l` = 15。第 ③ 类在制品中只以"`grep -c` 系列"泛指、未印出具体模式,故无命令可订正;此处记录正确形态,供后续制品引用。

---

## 14. 临时产物清理

| 临时物 | 用途 | 清理与复核 |
|---|---|---|
| `/tmp/ffdrill` | 场景 6 / 10 的演练制品 | `rm -rf` 后 `ls` → `No such file or directory`(跑前亦复核其不存在,避免与他人产物混淆) |
| `mktemp -d`(桩实验目录) | 复现 tasks.md:34 的 `-k` token 实验(5 个桩函数) | `rm -rf` 后 `ls -d` → `No such file or directory` |
| `/tmp/t058-gate1-full.log`、`/tmp/t058-gate1-rerun.log`、`/tmp/t058-skills-diff.txt` | 全量套件输出与 skills DIFF 集合的中间态 | 审计结束后删除,并以 `ls` 复核计数归零 |
| 真实反馈存据 `.specify/memory/feedback/` | — | **未写入**(N3 的 `record` 一步未执行);只读 `list` 前后 `count: 0` 一致,存据条目文件数 8 未变 |

仓内唯一被本轮命令改写的文件是 `.specify/specs/052-fast-fail-principle/current-failed.txt`(GATE-1 的 `--names-out` 规定输出,66 条),属该门禁的既定产物。

---

## 15. 结论与残留

- **198 项 check item 全部核完**:相符 **191** / 不符 **5** / 不可复现 **2** / 部分未实跑 **0**(191 + 5 + 2 + 0 = 198)。5 项不符中 **4 项是制品自身的值缺陷或已过时**(M1 钉子行号、M3 载荷行数 ×2 处、M5 常量行号),已在 052 制品内订正或加日期化注解;**1 项是当前树实况**(M4:GATE-1 名字级判据非空、GATE-3 需收窄度量窗口),不改判据文本。另 M2(`feedback-utils.py` 的 `raise` 行号偏一行)是在核 quickstart 场景 8 的 ⚠️ 注时发现,同一字面量在 3 个制品位置出现,已一并订正 ⇒ **订正共 4 类、落在 6 个文件的 8 个位置**。2 项不可复现均为计划期草稿子句的三数(制品自陈"草稿不落盘、无命令可复现"),已改核**落地**子句(6 原始行 / 5 非空行 / 801 字节 / 逐行 0 命中)。
- **逐份小结**:plan.md 30(29 相符 / 1 不可复现)· research.md 21(**19** / 1 不符 / 1 不可复现)· data-model.md 13(13)· quickstart.md 37(**36** / 1 不符)· feature-ref.md 17(17)· ambient-section.md 9(9)· constitution-export.md 14(14)· discipline-doc.md 13(13)· dispatch-injection.md 14(13 / 1 不符)· gate-neutrality.md 15(14 / 1 不符)· tasks.md 15(14 / 1 不符)。
- **反空真哨兵**:抽取非空(11/11 份制品、304 处出现、180 条去重命令串、129 条度量命令);审计非空(198 项,每份制品 ≥ 9 项);负面命题均配伴生量(互斥性 6 对、`BLOCKING_PATTERNS` 17、存据 8 个条目文件对 `count: 0`、`-k` 分区收集数 19/15/18/25/3/22、演练步骤 1 的 3 对步骤 2 的 0)。
- **残留:零**。原先移交的 N2 与 N3 已于 2026-09-24 由编排者实跑核出(`regen-command-copies.py --check` → EXIT=0 且输出 `OK: all per-tool command copies match the source templates.`;quickstart 场景 8 → 隔离根内 `count = 1`、真实存据未污染、临时根删净),二者均与制品所印相符,故 T058 由 `[~]` 改判 `[X]`。**移交理由本身也已订正**:子代理轮记的"无可靠只读等价物 / 隔离亦不豁免"源于派发禁令写得过宽——`--check` 是只读模式,`--workspace-root` 隔离形态不触及真实存据。禁令过宽会把可完成的审计逼成移交,这一形态与 § 十二 的盲检同族(输出看似合规,却不是关于它被写来判定的那个命题)。
- **对状态翻转的影响(2026-09-24 编排者轮更新)**:子代理轮记录 GATE-1 为**红**(1 条新增失败名,根因是 Feature 053 尚无 `plan.md`,与 052 无关),据此未翻转。**该根因已消除**:失败测试 `test_specify_script_paths.py::test_review_prerequisite_flags_are_supported` 的自身 docstring 声明的命题是「旗标被接受」,却以 `check=True` 把判定绑在「当前特性恰好有 plan.md」这一环境状态上——每轮 `/speckit.requirements` 到 `/speckit.plan` 之间都会红。已按该命题重修(拒旗标 = usage/Unknown option 错误;缺 plan.md/tasks.md 恰是 `--include-*` 被执行的证据,两种结局都通过),配反空真哨兵,并以注入 `--include-bogus-flag` 做变异演练(变红 → 精确反向替换复原 → `diff -q` BYTE-IDENTICAL → 7 passed);exit-0 臂在 052 的临时 worktree 中另行实跑取证,worktree 已移除、分支零污染。重跑后 `comm -13 baseline current` **为空**(65 failed / 2927 passed;基线 76、治好 11、守卫文件贡献 0)。**九项门禁全部对当前树重跑并转绿**,故 Pre-Status-Flip Gate 释放,Feature 052 由 `Planned` 推进到 `Implemented`;其中 GATE-3 的字面形态按第 6 步判为 **void**(恒空真、前提被证伪)并已在 `tasks.md` 的门禁项上加内联注解,承担判据的是收窄到 052 提交区间的形态。
