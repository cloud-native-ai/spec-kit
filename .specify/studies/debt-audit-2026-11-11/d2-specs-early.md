# 债务审计 D2 — specs 001–074（含 074a/074b/074）

**审计角色**：SDD Debt Governor（只读审计 + 治理设计，无执行授权）
**审计日期**：2026-11-11
**范围**：`.specify/specs/` 下 001–074 号段共 **60 个目录**（含 065a、074a、074b；075–099 不在本域）
**规模读数**：1,326 文件 / 16.3 MiB
**并发读数**：requested=1 / effective=1 / effective_reason=`single-unit`（可表示单元集 = {D2 单一有界域}，size=1；证据 = 本节范围清单）
**路径口径**：下文所有证据路径均相对 `.specify/`。

## 0. 口径（本次钉死，替代"待定"）

| 口径项 | 定义 |
|---|---|
| 标准文档集 | `requirements.md`、`plan.md`、`tasks.md`、`verification.md`、`research.md`、`data-model.md`、`quickstart.md`、`feature-ref.md` + 评审产物 `review.md` / `code-review.md` / `waivers.md` |
| 根级非标准文件 | spec 目录根层、文件名不在标准文档集内的文件（含 `contracts/`、`checklists/`、`notes/`、`test-evidence/` 之内的文件不算） |
| 证据/残留名 | 文件名匹配 `baseline｜failed｜current｜coverage-baseline｜docs-suite｜phaseN｜final-｜pre-repair｜rerun｜merge-manifest｜state-spine｜embed-inventory` |
| 旧锚（dangling） | `.specify/memory/<path>` 且解析目标不存在；**不等于**"所有 `.specify/memory/` 提及" |

## 1. 基线逐条复核

状态取值：resolved（已消失）/ still（仍存在）/ changed（读数或判读变化）/ new（新增发现）。

| # | 基线断言 | 状态 | 实测读数与判读 |
|---|---|---|---|
| B1 | 缺 verification.md 9 个（001/006/009/012/013/055/065/069/073） | **still** | 计数精确成立。但处置分四类：001/006/009/073 为已完成/直实现的证据缺口；012/013 已被 030 代表取代（030 自声明 Feature 013）；055 有用户裁定"轻量记录"；065 为 Planned 未到 tasks 阶段，缺失属预期；069 父壳的验证在归档切片 069a/069b |
| B2 | 缺 tasks.md 5 个 | **still** | 精确成立：001/055/065/069/073 |
| B3 | 空文件 16 | **changed** | 计数精确成立，但**判读改变**：16 个全部是"空输出"语义（10 个失败/名单列表 + 6 个 stderr/stdout）；`specs/056-probe-handler-system/verification.md:35` 明确把零字节 `baseline-failed.txt` + `phase7-current.txt` 读作"0 failures"。无证据失真；债务是约定未文档化，不是数据损坏 |
| B4 | 根级非标准文件 72 非标准 / 142 残名 | **changed** | "72"精确成立（61 evidence-log + 5 machine-artifact + 6 authored-side-doc；54 个被本 spec 标准文档引用，属承重证据）。"残名"现测 **143**（67 根级 + 33 notes + 41 test-evidence + 2 contracts）；基线 142 无法逐字复现（差 1，口径未钉）；备选口径：排除 contracts/ 后为 141 |
| B5 | md5 重复 21 组 | **still** | 以"≥2 个 in-scope 成员"为口径精确成立：21 组（20 组非空 + 1 组为空文件组），冗余 in-scope 文件 **47**；全 specs 树为 93 组。非空重复均为跨 spec 的 dated evidence 副本 |
| B6 | 旧锚 `.specify/memory/*` 680 处 / 277 文件 | **changed** | 全部 `.specify/memory/` 提及为 3,040 处 / 400 文件；其中 dangling 为 **935 处 / 329 文件**；排除 074 三目录后为 **685 处 / 289 文件**（最接近基线，差 +5 处 / +12 文件）；规范性文档（requirements/plan/tasks/research/data-model/quickstart/feature-ref）子集为 **443 处 / 182 文件**。基线读的是"dangling 子集（排除 074 三目录）"，不是全部提及 |
| B7 | 069a/069b 在 archive/specs；注册表指 live Draft | **still** | 归档成立（`features/069-execution-expression-sdd.md:119` 记 2026-11-09 consolidation）。注册表 `features.md:78` 行 069 状态 Implemented、Spec Path 指向 live 父 spec；该父 `specs/069-execution-expression-sdd/requirements.md:6` 的 **Status 仍是 Draft**，且父目录只有 requirements.md；交付证据在归档切片 |
| B8 | 注册表漂移（006/009/012/013 名称、013 Spec→030、065a/067 缺行） | **changed** | 判读需分三层：① 006/009/012 是"spec 编号 ≠ Feature ID"的双命名空间现象（spec 006/009 属 Feature 020/021，012/013 属 Feature 013），不是数据损坏；② `013 → 030-summarize-project` 是 Feature 013 的**合法代表指针**（030 自声明 Feature ID 013），不是错指；③ 065a/067 "缺行"是两 spec 自己声明的设计（065a 为 065 切片、067 为 058 演化，均明确"不新建 Feature ID/行"）。**真正的缺陷另列**：行 048 指向已归档 spec 的 live 路径（P1）；14 个 in-scope 目录无机器可读的注册关系（P2）；50 个 Draft 内部状态与注册行状态矛盾（P2） |
| B9 | 074a/074b 待线 100 归档 | **still** | 合并已应用：`specs/074-goal-team-sdd-unification/merge-manifest.json`（seal-utils 0.0.22，merge=merged，slices retention=`pending-review`），提交 `8460536ca`（2026-11-11）；线 100 worktree 存在；074a 32/32、074b 26/26、父 58/58 均 `[X]`。归档尚未发生 |
| B10 | 074 详情 stale 句 | **still** | `features/074-goal-team-sdd-unification.md:30` 仍写"状态保持 `Planned`：…074b 未实现前不擅自推进"，与文件头 `Status: Ready for Review`（第 6 行）矛盾；`Last Updated`（第 8 行）止于 2026-10-29，全文 **0 处** 2026-11-11 记录 |

## 2. 债项登记

排序：严重度优先（P0 → P1 → P2），同严重度按主证据路径。**无 P0**。处置取自已处置集：keep / archive / delete / regenerate / dedupe / normalize / consolidate；lane 为 SDD 修复 / sanitize 回收 / 保持并立政策。

### P1（结构性）

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | lane |
|---|---|---|---|---|---|---|
| D2-01 | 注册表坏指针 | `features.md:57`（行 048）；`archive/specs/046-browser-site-memory/` | 行 048 状态 Relocated，Spec Path 仍写 `specs/046-browser-site-memory/requirements.md`；live 目录不存在，spec 只在 archive。任何按 Spec Path 解析的消费者得到 ENOENT | P1 | normalize（改指 archive 路径或置 `-`） | SDD 修复 |
| D2-02 | 旧锚引用腐烂 | 443 处 / 182 个规范性文档；热点：`specs/029-glossary-mechanism/plan.md` 12 处、`specs/050-proactive-flow-trigger/{requirements,tasks}.md` 各 10 处、`specs/051-user-facing-comprehension/{requirements,tasks}.md` 各 10 处 | 规范性文档引用不存在的 `.specify/memory/*` 路径；Top 目标：`memory/features.md` 110 处、`memory/constitution.md` 103 处、`memory/glossary.md` 34 处、`memory/feedback/probes/` 17 处、`memory/features/074.md` 15 处。现 owner 为 `features.md`、`constitution.md`、`glossary.md`、`features/<ID>.md`；`memory/feedback/probes/` 无现等价物（probe owner 为 `shared/definitions/probe-definitions.md`） | P1 | normalize（确定性映射 + 日期性叙述 allowlist） | SDD 修复 |
| D2-03 | 注册表/状态矛盾 | `features.md:78`（行 069）；`specs/069-execution-expression-sdd/requirements.md:6` | 行 069 为 Implemented，Spec Path 指向 live 父 spec；父 spec 只有 requirements.md，内部 Status=Draft；交付在归档切片 069a/069b。机器入口与状态互相矛盾 | P1 | normalize（推进/标注父状态并加归档切片指针） | SDD 修复 |

### P2（计划性）

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | lane |
|---|---|---|---|---|---|---|
| D2-04 | 详情 stale | `features/074-goal-team-sdd-unification.md:30`，对照第 6/8 行 | 第 30 行"状态保持 Planned…074b 未实现前不擅自推进"与头部 Ready for Review 矛盾；Last Updated 止于 2026-10-29；无 2026-11-11 review/seal 记录 | P2 | normalize（追加 dated 记录，标注旧句被后续翻转取代，不改写 dated 文本） | SDD 修复 |
| D2-05 | 已完成/直实现记录缺验证 | `specs/001-unify-command-handoffs/`、`specs/006-add-qoder-support/`、`specs/009-claude-code-support/`、`specs/073-record-retention-and-housekeeping/` | 001（Completed）只有 plan+requirements（注册表有 audit 注记）；006/009（Implemented）有 plan/tasks 无 verification；073（Implemented）只有 requirements，detail 记录直实现。计数成立，但属历史证据缺口 | P2 | keep（登记表加 closure 注记；不回填不可验证的 verification） | 保持并立政策 |
| D2-06 | 被取代的 live Draft | `specs/012-skill-home-workdir/requirements.md`、`specs/013-portable-skill-creation/requirements.md`、`specs/062-humanize-command/requirements.md` | 012/013 自声明 Feature 013，代表 spec 已是 030（行 013 → 030）；062 自声明 Feature 062，行 062 → 080（080 自声明 Feature 062，由 079 重编号而来）。三者仍 live、Status Draft、无 Superseded 标记 | P2 | archive（先加取代标记，再归档） | sanitize 回收 |
| D2-07 | 需求文件状态字段未治理 | 54/60 个 in-scope `requirements.md` 为 Draft；其中 50 个对应注册行已是 Implemented / Ready for Review / Completed | 模板只定义 `Status: Draft`；`feature-integration.md` 的状态机治理的是 features.md，不是需求文件字段。6 个 spec 自行推进了该字段（037/041/042/043/055/073），其余未推进；切片两侧都有先例，语义未声明 | P2 | normalize（先裁定字段语义：冻结于撰写 vs 跟随 Feature；再批量归一） | SDD 修复 |
| D2-08 | 切片/演化无机器可读关系 | 14 个目录：012/013/018/024/038/041/042/047/049/062/065a/067/074a/074b | 均为某 Feature 的切片/演化（自声明 Feature ID 分别为 013×2、022×2、041、028×2、027、037、062、065、058、074×2），但 features.md 的 Spec Path 单值列无法表达；仅散文里提及。无孤儿 spec，缺的是关系字段 | P2 | normalize（增加切片/演化关系列或每行关系句） | SDD 修复 |
| D2-09 | 详情/模式缺口 | `features/` 无 067 详情、无 065a 详情；`specs/001-.../requirements.md`、`specs/006-.../requirements.md` 无 `**Feature ID**` 行（grep=0） | 067 只在 058 散文演化中出现；065a 只在 065 行散文中出现；001/006 为早期 schema。三个可追溯面缺失 | P2 | regenerate（补详情或在注册行显式声明"无详情/设计"；补 Feature ID 行） | SDD 修复 |
| D2-10 | 055 轻量记录未在登记面记录 | `specs/055-conflict-free-stores/requirements.md`（Status Implemented…direct implementation per user ruling ③） | 用户裁定"不走完整 SDD 仪式"已写进 spec，但 features.md 的 055 行未记录该豁免；与 073 的直实现同类但仅 055 有显式裁定 | P2 | keep（把豁免写进注册行，避免后来者误判缺件） | 保持并立政策 |
| D2-11 | 根级证据附件无政策 | 72 个根级非标准文件：61 evidence-log、5 machine-artifact、6 authored-side-doc；54 个被本 spec 标准文档引用（例：`specs/044-reduce-confirmation-flows/baseline.json` 34,747 B、`specs/074-goal-team-sdd-unification/merge-manifest.json` 95,572 B） | 证据附件承重但无声明式放置/命名政策；framework map 只列 requirements/plan/tasks/verification 四件。移动会打断 54 个引用 | P2 | keep（先声明附件政策；是否迁移待裁决 Q2） | 保持并立政策 |
| D2-12 | md5 重复 | 21 组 / 47 个冗余 in-scope 文件；例：`specs/052-fast-fail-principle/current-failed.txt` = `specs/053-machine-decidable-artifacts/{baseline,current}-failed.txt` + `notes/clarify-current-failed.txt`；`specs/074b-nested-governance/test-evidence/implement-targeted-part{1..4}-failed.txt` 四份相同 | 非空重复均为 dated evidence 副本；按 non-disposable owner 属允许的"日期性记录重复"。债务是体积与检索噪声，不是正确性 | P2 | keep（保留 dated 记录；仅在 retention 授权后 dedupe 为指针） | 保持并立政策 |
| D2-13 | 空输出约定未文档化 | 16 个零字节文件：`specs/033-docs-command/docs-suite-failed.txt`；`specs/056-probe-handler-system/{baseline-failed,phase4..7-current}.txt`；`specs/065a-state-awareness/baseline-failed.txt` + 5 个 stderr/stdout；`specs/068-exec-quant-feedback-channel/test-evidence/log-final-post-sync-names.txt`；`specs/071-review-code-integration/test-evidence/decomposition-check.stderr`；`specs/074a-authorized-routing/notes/{part5-failed,targeted-set-v1-failed}.txt` | 空=0 failures / 0 errors / 0 names 的语义成立（056 verification:35 直接以此作判据）；但约定未写入任何 owner，读者无法区分"空即零"与"采集失败"；phase4/5/6-current 未被引用 | P2 | keep（把约定写进证据规范；不删） | 保持并立政策 |
| D2-14 | 损坏相对链接 | `specs/006-add-qoder-support/plan.md:3`、`specs/009-claude-code-support/plan.md:3`、`specs/033-docs-command/tasks.md:86` | 006/009 把仓库根相对路径写进 markdown 链接（在 spec 目录解析为 ENOENT）；033 的 `](commands/docs.md)` 真实文件在 `templates/commands/docs.md`。共 3 处 live 文档坏链 | P2 | normalize（修正链接目标） | SDD 修复 |
| D2-15 | 超大文件 | `specs/067-loop-efficiency-hardening/test-evidence/post-test-ids-2026-10-22.txt` 611,262 B；同目录 `baseline-test-ids.txt` 466,673 B；`specs/074-goal-team-sdd-unification/notes/closure-full-run.txt` 147,796 B；`specs/052-fast-fail-principle/requirements.md` 143,178 B；`specs/051-user-facing-comprehension/requirements.md` 128,143 B | 5 个 >100KB in-scope 文件，集中在测试 node-id 日志与需求正文；token/检索成本高，但均为 dated 证据或已交付需求 | P2 | keep（证据保留；需求正文的体积纪律另立；不回写历史） | 保持并立政策 |

## 3. 治理计划

顺序：机制修复 → 数据回收 → 结构收敛。每波独立确认门，前一波不绿不启动下一波。

### Wave A — 注册表与状态真实性（机制修复）

- **范围**：D2-01、D2-03、D2-04、D2-06（标记部分）、D2-07、D2-08、D2-09。
- **确认门**：`/speckit.feature` reconcile 的 dry-run diff；注册表为单一所有者产物，写入前呈现逐行 diff（治理保留清单，不新增确认门）。
- **可测成果**：Spec Path 悬空数 **1 → 0**；001–074 带内状态矛盾 **50 → 0**；被取代 live spec 带标记率 **0/3 → 3/3**；14 个切片/演化目录全部有机器可读关系或在行内显式声明。
- **中止条件**：任一行的正确代表 spec 无法从 spec 自声明 + 状态唯一确定（例如行 048 的目标应取 archive 路径还是 `-`）→ 停下交裁决 Q1/Q5。

### Wave B — 规范性文档旧锚归一（机制修复）

- **范围**：D2-02 的 443 处 / 182 文件；`memory/feedback/probes/` 单独处理。
- **确认门**：SDD 修复批（按 spec 分批）+ 只读链接检查器作为完成门；日期性证据叙述（review/verification/notes/test-evidence）不重写，只进 allowlist。
- **可测成果**：规范性文档 dangling 旧锚 **443 → 0**（或 allowlist 有界且逐条有理由）；Top 目标 `memory/features.md`、`memory/constitution.md`、`memory/glossary.md` 清零。
- **中止条件**：`.specify/memory/feedback/probes/` 的映射不能唯一确定（现 owner 是 `shared/definitions/probe-definitions.md`，但历史文本可能指旧目录）→ 交裁决 Q4，不对该前缀做批量替换。

### Wave C — 证据附件政策与回收（数据回收）

- **范围**：D2-11（72 个根级附件）、D2-12（47 个冗余文件）、D2-13（16 个空文件）、D2-15（5 个 >100KB 文件）。
- **确认门**：先声明政策（Q2），再 `/speckit.sanitize` dry-run；archive-not-delete；删除/移动需用户显式授权；移动必须同步改写 54 个引用。
- **可测成果**：根级附件政策 1 条落 owner；冗余文件数 **47 → 0 或 allowlist**；空输出约定 1 条落证据规范；超大文件保留但可派生摘要。
- **中止条件**：任一被 54 个引用覆盖的文件将被移动/删除而未先改写引用 → 中止该批。

### Wave D — 结构收敛（计划性）

- **范围**：D2-05（001/006/009/073 的 closure 注记）、D2-10（055 豁免入册）、D2-06（012/013/062 归档）、D2-09 的详情补齐。
- **确认门**：`/speckit.feature` 再收敛 + sanitize archive 执行；归档前置取代标记。
- **可测成果**：4 条薄记录在注册行有 closure/豁免注记；3 个被取代 live Draft 完成归档或显式保留；067/065a 的详情缺口关闭或声明"无详情由设计"。
- **中止条件**：补验证需要虚构未发生的证据 → 改为 keep + 注记，不执行 regenerate。

## 4. 裁决点（封闭问题，未自答）

- **Q1（行 048 目标）**：归档 spec 的 Spec Path 取 (A) `.specify/archive/specs/046-browser-site-memory/requirements.md`，还是 (B) 置 `-` 并把归档路径写进描述？
- **Q2（根级证据附件）**：(A) 保留根级并声明政策，还是 (B) 迁入 `test-evidence/` 并改写 54 个引用？
- **Q3（被取代 live spec 012/013/062）**：(A) 加 Superseded 标记后归档，还是 (B) 保留 live 并加标记？
- **Q4（`memory/feedback/probes/` 旧锚）**：(A) 统一改指 `shared/definitions/probe-definitions.md`，还是 (B) 视为日期性历史并加入 allowlist？
- **Q5（069 父 spec）**：(A) 保留为 live 索引并标注 Draft/归档切片，还是 (B) 另选 live 代表（当前无候选）并改行 069 指针？
- **Q6（薄记录 001/006/009/073/055）**：(A) 注册行记 closure/豁免，不回填，还是 (B) 要求补 plan/tasks/verification？（B 会产生不可验证的追溯证据）
- **Q7（074a/074b 归档时机）**：(A) 线 100 seal 关闭后立即归档，还是 (B) 等线 100 全部对象关闭后统一归档？
- **Q8（需求文件 Status 字段）**：(A) 冻结于撰写（Draft 为历史值，注册行为权威），还是 (B) 跟随 Feature 状态批量推进 50 个文件？

## 5. 边界、异常与未验证项

- **写入边界**：本次未删除、移动、归档或改写任何项目文件；唯一写入为本报告。未执行 git 写操作。
- **快速失败**：无异常需要上抛；无就地修复。审计中发生一次判读纠正：零字节证据初判为"空文件债务"，经 `specs/056-probe-handler-system/verification.md:35` 复核后改判为"空=零的合法语义"，已写入 B3/D2-13，未按原判升级。
- **未验证项**：无。所有发现均有路径与机械读数。唯一不可逐字复现的是基线"142 残名"（现测 143，已给出 141/143 两种口径与差值 1）。
- **跨域不越界**：`.specify/archive/` 的两套命名（`spec/` 与 `specs/`）归 D3；`memory/`、`register.md` 的消费者归 D4；`.specify/state/` 与线 100 运行态归 D1。本报告只在 spec 侧引用它们作为证据。

DEBT-DONE
