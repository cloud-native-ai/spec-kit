# Analyze Report — 087-speckit-visualization（/speckit.analyze，2026-11-06，Round 4）

**Unit**: `/speckit.analyze` · **Run ID**: `r20261106T040353Z-087a` · **Stage**: analyze（Round 4，全严重度复核 + rerun delta）
**Spec dir**: `.specify/specs/087-speckit-visualization`（`REQUIREMENT_ID=087`，`FEATURE_ID=087`，`MODE=C`）
**Flow class**: `execution` / `source=declaration`（`flow-class-check.py --action lookup --unit-id "spec:087-speckit-visualization"` → exit 0；非表达类，既有门禁集逐字不变）
**Prior report**: `test-evidence/analyze-report-round3-2026-11-06.md`（Round 3，8 条 open findings：2 HIGH / 1 MEDIUM / 5 LOW）
**Baselines under analysis**: requirements `b2c044e0` / plan `e14b10a2` / contracts `e14b10a2` / data-model `e14b10a2` / tasks `0d97dfd3` / driver fix `c047740d`（HEAD）
**性质**: 严格只读。本报告是本阶段唯一交付产物；requirements / plan / tasks / contracts / data-model / quickstart / checklists / 注册表零修改。§1 的五份 validator 原始读数写入 `test-evidence/round4-*.txt`（证据，不是产物）。

## 0. 门禁结论（Gate Verdict）

**GATE GREEN** — CRITICAL 0，HIGH 0。Round 3 的 2 条 HIGH（F-10 / F-11）与 1 条 MEDIUM（F-12）**全部关闭**，2 条 LOW（F-13 / G-02）**全部关闭**；本轮全量复核**未识别任何新的 CRITICAL/HIGH/MEDIUM**。剩余 3 条 LOW（C-04 / C-05 / H-01，均为 carry-over）不阻断。

| 严重度 | 条数 | 状态 |
|--------|------|------|
| CRITICAL | **0** | — |
| HIGH | **0** | Round 3 的 F-10 / F-11 已关闭，逐条证据见 §4.1 |
| MEDIUM | **0** | Round 3 的 F-12 已关闭（证据见 §4.1） |
| LOW | 3 | C-04 / C-05 / H-01 仍 open（carry-over），不阻断，理由见 §2 与 §2.4 |

**判据核对**：「CRITICAL/HIGH 为零或已处置」→ **满足（为零）**。按 SKILL § Next actions 第 2 条，「LOW/MEDIUM only → proceed with suggestions」，本门可进入 `/speckit.implement`。

### 0.1 验证波状态（显式降级，非静默）

- **同一作者门（objective-analysis-gate）**：**未触发**——requirements / plan / tasks / contracts 由本无人值守链的**其它阶段运行**产出，本 worker 未在本次会话撰写它们（owner 判据：`.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 第 2 条）。
- **CRITICAL/HIGH 独立验证子代理**：**不可派发**（本层为 bounded assignment，brief 明确禁止派发子代理；宿主 Agent 类型表亦未含 `SDD Analysis Worker`）。按 SKILL `references/validation-and-report.md` § Subagent-unavailable fallback 执行**直接受限重读**，在本报告 §4.1 中以 `(validated: direct re-read, subagent unavailable)` 标注。
- **降级率**：n/a（无第三方 validator）。本轮应验证 0 条 C/H（因为 C/H 计数为零）；3 条 carry-over LOW 的复核走同一直接重读路径。
- **零发现下限**：本轮 C/H/M 为零，属**阳性判定的缺席**——故 §1 保留五份 validator 原始读数、§5 保留 coverage 全量裁决、§6 保留各通道计数，使「无 C/H/M」成为一个有证据的断言，而非空表。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`MODE=C`；`AVAILABLE_DOCS` 含 research/data-model/contracts/quickstart/checklists/feature-ref/tasks |
| 类别读取（一次读取） | `flow-class-check.py --action lookup --unit-id "spec:087-speckit-visualization"` | `flow_class: execution`，`source: declaration`，exit 0 |
| 覆盖核算（固定步骤，只读） | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/087-speckit-visualization`（**未** `--freeze`；原始读数 `test-evidence/round4-coverage.txt`，640 行全量） | exit 1；`claimed clauses (this feature): 33`；`baseline: coverage-baseline.txt (573 names)`；`[fr-uncovered] pass (0) — 22 of 22`；`[clause-uncovered] fail (592)`；`[coverage-baseline-delta] fail (19)`；`[clause-unparsable] warn (107)`；`status: uncovered` → §5 |
| 确定性校验 | `validate-requirements.py requirements.md`（`round4-validator-requirements.txt`） | `status: ok`，六标签全 pass（0），`scanned: 522 lines, 32 definition rows, 0 shared strings`，0 error 0 warning |
| 确定性校验 | `validate-tasks.py tasks.md`（`round4-validator-tasks.txt`） | `PASS (with warnings)`：0 error / **11 warning**（7 `green-cross-phase` + 4 `green-path-divergence`；全部在 tasks.md § WARNING ADJUDICATION 有作者裁决） |
| 确定性校验 | `validate-decision-tensions.py --spec <spec>`（`round4-validator-decision-tensions.txt`） | `status: ok`，六标签 0 命中，`scanned: 332 lines, 2 record(s)`，`channel: value_domain=HIGH-or-0, high=0` |
| 确定性校验 | `pre-analyze-check.py --spec-dir <spec> --stage plan --repo .`（`round4-pre-analyze-plan.txt`） | `decision=pass errors=0 advisories=134 waived=0`；`fr=22 sc=10 tasks=50 clauses=0 files=15` |
| 确定性校验 | `pre-analyze-check.py --spec-dir <spec> --stage tasks --repo .`（`round4-pre-analyze-tasks.txt`） | `decision=pass errors=0 advisories=134 waived=0`；同读数 |
| 相关门 | `sync-mirrors.py --check` / `regen-command-copies.py --check` | 六对镜像 `ok`；命令副本 `OK` |
| 相关门 | `scan-confirmation-gates.py --root . --summary` | `blocking confirmation gates: 27`（destructive 20 / governance_kept 7）；`violations: 0` — 与 C-48 记录的 27 一致 |
| 检测通道 A–I | 逐产物交叉读（§2、§3、§4） | 3 条 open（全 LOW）+ 8 条本轮关闭 |
| 检查清单 H 通道 | 60 条逐条分诊（§3） | 17 条 unchecked `[Gap]`：10 covered-by + 7 raised，`undispositioned=0`；3 条已 `[x]` |

**读数对照（round 3 → round 4，同一命令）**：`pre-analyze --repo .`：134 → **134**（不变，13 个交付期路径名与 `files=15` 均不变）；`validate-tasks`：0 error / 11 warning → **0 error / 11 warning**（不变）；`validate-requirements`：`scanned 522 lines / 32 定义行` → **不变**；`validate-decision-tensions`：`scanned 330 lines` → **332 lines**（F-10/F-13 的文本修复使行数 +2），`2 record(s)` 与 `high=0` 不变；coverage：`33 claimed / 573 baseline / 19 beyond / status uncovered` → **逐字节相同**。

**工具路径纠正（就地修复并披露）**：§1 的两条 `pre-analyze-check.py` 首次以 `../../scripts/python/…` 相对路径调用，引擎实际位于 `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`，两次调用报 `No such file or directory`（exit 2）。按 fast-fail 判据：只有一种与已知意图一致的读法（brief 指定的就是该引擎）、改动局部可逆、未证伪任何下游前提 ⇒ **就地纠正**为从仓库根目录调用真实路径，两次均 `decision=pass`。**这不是 spec 产物的漂移，不构成 finding。**

**读入的权威面**：requirements.md（22 FR / 10 SC / 15 A / 12 Edge Cases / 522 行）、plan.md（19 行宪法检查 / T-001–T-002 / EP-001–EP-010 / D1–D12 / 9 行 Mirror Obligations）、tasks.md（50 行，T001–T046 + T051–T054 / § Clause Coverage Ledger）、contracts ×6（52 条款 C-01…C-52）、data-model.md（E1–E7 + INV-01…INV-12）、quickstart.md（A–H）、checklists ×2、feature-ref.md（28 行交付路径）、`features.md` 087 行、`features/087.md`、`constitution.md` v1.16.0（19 原则）。

## 2. Findings（open，3 条，全 LOW）

`propagation_surface` 是每条的第一个字段；severity 由它派生（owner: `objective-analysis-gate.md` rule 3）。**本轮无 CRITICAL / HIGH / MEDIUM。**

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| C-04 | C 欠指定 | owner 文档（T008）声明面 | **LOW**（carried over，第 3 轮） | `requirements.md:206-212`（FR-003）、`:243-246`（FR-009）、`:157-176`（Edge Cases 只覆盖相邻概念）；`tasks.md:87`（T008 清单） | 四个 owner 级口径仍无声明：① idle tick 是否可抑制；② long-run 档的计时锚点；③ 阈值与周期的数量关系；④ 宿主时钟跳变/挂起时「tick 序列缺口」与「reporter 停滞」如何区分。T008 的作者清单未新增这四项 | 在 owner 文档把这四条各写一句声明（T008 的作者清单相应加 4 项）。**为何不阻断**：四项均为 owner 文档正文的补充句子，不改变任何 FR/SC 的判据，也不改变任何契约条款的可判定性；`account-clause-coverage` 与两份 validator 均不受影响 |
| C-05 | C 欠指定 | 行级策略（owner + 渲染器） | **LOW**（carried over，第 3 轮） | `requirements.md:172-174`（预算耗尽只在 Edge Case）、`contracts/status-report.contract.md:108-114`（C-29）、`contracts/supervision-report.contract.md:110-121`（C-40） | 三条行级策略仍缺：① `reporter-failure` 行是否也须携带四要素（INV-01 说 "every Status Report"，C-29 未点名）；② 派发载荷缺 reporting 字段时的失败模式（C-40 只说 "carries by injecting"）；③ 预算耗尽「仍然报告」只有 Edge Case，无 FR/契约条款 | 同 round 2/3 建议：C-29 明确 failure 行的最小内容；C-40 增加一个具名失败条件；把预算规则升为一句契约条款。**为何不阻断**：C-29 已钉住「state what failed / MUST NOT claim healthy / no-line-is-never-progressing」三个可判定断言，C-40 的注入通道已由 `tests/contract/test_reporting_obligations.py` 断言；缺的是补充性细化，不是互相矛盾的第二个定义 |
| H-01 | H 清单问责 | checklist 证据（`checklist-selfcheck.json` / § Notes） | **LOW**（carried over，第 3 轮） | `checklists/framework-visualization-2026-11-06.md:138-142`（Notes 的 measured 计数）、`:152`（"Gaps worth triaging first" 仍列 CHK027） | 清单 Notes 自称 "measured" 的维度计数仍与文件不符：**实测 `Gap` 17（声称 19）、`Ambiguity` 11（13）、`Conflict` 4（6）、`Assumption` 2（3）**；`test-evidence/checklist-selfcheck.json` 的 `dimension_hits` 与 Notes 同错。60 items / 100% 可追溯 / 0 非问句 / 0 禁用前缀四项成立；CHK027 已 `[x]`，Notes 仍把它列在待分诊 gaps | 重算四个数字并就地加一行更正（复算命令：`for d in Gap Ambiguity …; do grep -E "^- \[[ x]\] CHK" <file> | grep -c "\b$d\b"; done`）；同步 `checklist-selfcheck.json` 的 `dimension_hits`；把 Notes 的 CHK027 行标注为 resolved。**为何不阻断**：60 条问责通道本身健康（`unchecked + unraised + undispositioned = 17 + 0 + 0`，§3），失准的只是 Notes 的自述统计，不影响任何 `[Gap]` 的处置归属 |

### 2.4 LOW 证据（复核读数）

- **C-04**：`requirements.md:206-212`（FR-003 只有「MUST emit … the cadence MUST remain configurable」，「names no interval value」，无 idle/tick-up 抑制语）；`:243-246`（FR-009 只说「**declared** stall threshold」「not a per-run guess」，无阈值与周期的数量关系）；Edge Cases 的 "Cadence versus atomic steps" / "Stall versus slow" 各覆盖一个相邻概念，未覆盖时钟跳变。`tasks.md:87` T008 的作者清单无这四项。
- **C-05**：`contracts/status-report.contract.md:108-114` C-29 全文（「MUST surface that as a named condition」「MUST state what failed and MUST NOT claim the run is healthy」），不点名四要素；`contracts/supervision-report.contract.md:110-121` C-40 全段（「carries the same obligation by injecting the reporting duty into its dispatch payload」），无缺字段的失败条件；`requirements.md:172-174` 的预算规则仍只在 Edge Cases。
- **H-01**：本轮复算（`grep -E "^- \[[ x]\] CHK" <file> | grep -c "\b<Dimension>\b"`）得 `Gap 17 / Ambiguity 11 / Conflict 4 / Clarity 6 / Measurability 6 / Consistency 5 / Completeness 4 / Assumption 2 / Dependency 3 / Coverage 2`；Notes `:139-141` 与 `checklist-selfcheck.json.dimension_hits` 声称 `19 / 13 / 6 / … / 3`。`:152` 的 triage 列表仍含 CHK027（`framework-visualization-2026-11-06.md:66` 已标 `[x]`）。

## 3. 检查清单问责（§ H pass）

`unchecked [Gap] 17 + unraised 0 + undispositioned 0`——**`undispositioned = 0`，不阻断**。60 条中 57 条未勾选、3 条已 `[x]`（CHK002 / CHK027 / CHK054，均为 analyze 前几轮的 resolved 标注，不进 Gap 集）。

| CHK | disposition |
|-----|-------------|
| CHK003 | `CHK003 disposition: covered-by requirements.md § FR-021 + § Clarifications 第 4 问` |
| CHK005 | `CHK005 disposition: covered-by requirements.md § FR-011 workspace rule + data-model.md § E5` |
| CHK006 | `CHK006 disposition: covered-by plan.md D2 + contracts/reporter-seat.contract.md C-14/C-19` |
| CHK007 | `CHK007 disposition: covered-by requirements.md § Edge Cases "Two cadence profiles in one session" + C-30 + data-model.md E6` |
| CHK009 | `CHK009 disposition: covered-by contracts/status-digest.contract.md C-44 + C-47 stale-bound 行 + data-model.md E5` |
| CHK017 | `CHK017 disposition: raised-as-finding C-04` |
| CHK018 | `CHK018 disposition: raised-as-finding C-04` |
| CHK021 | `CHK021 disposition: covered-by contracts/reporter-seat.contract.md C-16（four fixtures / 三个具名缺陷含 two-seats）+ tasks.md T011/T013 + data-model.md E1` |
| CHK023 | `CHK023 disposition: covered-by contracts/reporter-seat.contract.md C-15 + data-model.md E1` |
| CHK032 | `CHK032 disposition: raised-as-finding C-04` |
| CHK034 | `CHK034 disposition: raised-as-finding C-05` |
| CHK036 | `CHK036 disposition: raised-as-finding C-04` |
| CHK039 | `CHK039 disposition: covered-by contracts/status-digest.contract.md C-45 + C-42 + tasks.md T027` |
| CHK040 | `CHK040 disposition: covered-by data-model.md E5 profile_summary + contracts/status-digest.contract.md C-41` |
| CHK044 | `CHK044 disposition: covered-by requirements.md § FR-006 population + contracts/reporting-obligations.contract.md C-04 + tasks.md T003/T035` |
| CHK046 | `CHK046 disposition: raised-as-finding C-05` |
| CHK058 | `CHK058 disposition: raised-as-finding C-05` |

**落点统计**：covered-by 10 条（CHK003/005/006/007/009/021/023/039/040/044），raised-as-finding 7 条（C-04×4、C-05×3）——与 round 3 **完全一致**（本轮无 checklist 文本变更，README 侧零 diff）。四项 adjudicated 不变：CHK012 不构成 finding；CHK027 已按修复后的 SC-003 关闭；CHK052 的 normative 半边已由 FR-003/SC-006 修复；CHK056 由 FR-016 的 "emitting flow's own" 限定关闭。

## 4. Rerun delta

### 4.1 Resolved Since Last Run（8 条，逐条关闭核验）

| ID | Round-3 严重度 | 本轮结论 | 关闭证据（逐条复核） |
|----|----------------|----------|----------------------|
| **F-10** | **HIGH** | **已关闭** —— `(validated: direct re-read, subagent unavailable)` | `plan.md:292` D10 现写「`0` = a digest was rendered **with at least one entry**, `3` = nothing active — … carried by the explicit `nothing-running` rendering (**an empty entry set MUST NOT render an empty digest with status `0`**)」——round-3 的两处互斥已被消除：`0` 行不再包含 nothing-running，且显式加入与 C-45 同方向的 MUST NOT。`contracts/status-digest.contract.md:77-78,84-85` 未变且与 D10 逐字同向。**四侧一致性复核全绿**：`quickstart.md:123`（status `3`）、`quickstart.md:132`（premise 4：`3` distinct from `0`）、`data-model.md:125`（E5：exit status `3`, never an empty result）、`research.md:228`（U-4：`0` rendered / `3` nothing active / `2` input error）。SC-005 的「declared exit status」现只有**一个**声明值。 |
| **F-11** | **HIGH** | **已关闭** —— `(validated: direct re-read, subagent unavailable)` | action 集合已单向统一到**三动作**（round-3 建议的 (A)）：`contracts/status-digest.contract.md:5`「with **three** actions」、`:12` 标题「One command, one script, **three** actions, one reading」、`:15`「MUST implement **exactly three** actions」、`:19` 列出 `--action report`、`:24` judged-by 改为「the script exposes **exactly these three** actions」（原为 "exposes both"）；`plan.md:282-283` D8「One script, **three** actions」并展开 `--action report`；`tasks.md:88` T009「exposing **exactly the three actions** C-41 fixes」并显式写「the action set is **exactly** this three — neither a fourth action nor a missing one satisfies C-41」；`tasks.md:153` T029「the **three actions** (digest / guard / report)」；`tasks.md:110` T016「the third action (`--action report`, whose entry point and shared reader T009 establishes)」——不再是孤立的第三值。全 spec 目录 `grep -rniE "\btwo actions\b|\btwo-action\b"`（排除 test-evidence）**零命中**。C-41 的 "A second parser or a second renderer is a defect" 与 T016「Author the status-line renderer **into** `scripts/python/status-digest.py`」不冲突（同一文件内的第三个 action，不是第二个渲染器）。 |
| **F-12** | **MEDIUM** | **已关闭** | `tasks.md:99`（US1 Independent Test）改为「over the **four** roster fixtures (compliant / missing-seat / unresolvable-agent / two-seats — the compliant one plus **the closed defect set of three** … C-16 fixes)」；`tasks.md:273`（Parallel Example）同步为 four；`tasks.md:105`（T011）措辞已改为「**four fixtures (three named defects + compliant)**」，round-3 指出的「four **defect** fixtures」命名小疵一并修掉；`contracts/reporter-seat.contract.md:62-63`（C-16 judged-by「four fixtures … (compliant, missing-seat, unresolvable-agent, two-seats)」）与 `quickstart.md:72-73`（同四类 + 「three named defects plus the compliant case」）同向。**三处副本 + 两处指导文本 + owner 全部一致**。 |
| **F-13** | LOW | **已关闭** | `data-model.md:108` 现写 `` `.specify/shared/guidelines/one-source-of-truth.md` is the discipline ``；原断链 `storage/guidelines/one-source-of-truth.md` 在全 spec 目录 `grep -rn "storage/guidelines"` **零命中**；目标路径在树中存在。 |
| **G-02** | LOW | **已关闭** | `features.md:94`（087 行 plan 记录）现写 `EP-001…EP-010`（round-3 为 `EP-001…EP-009`）；`features/087.md:20` 现写 `EP-001…EP-010 全 verified（EP-010 =「无 docker/hugo 套件可 deselect」，round-1 为消解 GATE-1 占位新增，2026-11-06 补记）`——数字更正**并**补了 dated 说明，round-3 给出的两条修复建议都落了。`grep -on "EP-010" features/087.md` → 2 命中（`:20` 两处），与 `plan.md:225` 的 EP-010 行对应；`EP-001…EP-010` 在 `plan.md:216-225` 为 10 行全 `verified`。 |

**round-3 报告的其余 MEDIUM/LOW 复核（brief 点名的 E-03/F-03/F-04/F-08/F-09/C-04/C-05/H-01）**：

| ID | Round-3 状态 | 本轮结论 | 复核依据 |
|----|--------------|----------|----------|
| E-03 | 已于 round 3 关闭 | **保持关闭** | `tasks.md:225-247` 的 § Clause Coverage Ledger 19 行；本轮 coverage 的 19 条 beyond-baseline 名单（`ownership-map#C-48`；`reporter-seat#C-14/C-18/C-21`；`reporting-obligations#C-02…C-13`；`status-report#C-23/C-30`；`supervision-report#C-36/C-38`）与台账逐名相等（§5）。`tasks.md:255` 的「33 / 34」口径见 §4.4 的残余记录 |
| F-03 | 已于 round 3 关闭 | **保持关闭** | `tasks.md:152` T028 的 green point 仍为 C-42，与 C-42 的「projection / no write」主题一致；T009（`:88`）保留 C-41。`validate-tasks` 的 4 条 `green-path-divergence` 均在 § WARNING ADJUDICATION 有作者裁决 |
| F-04 | 已于 round 3 关闭 | **保持关闭** | `tasks.md:28` GATE-1 仍写「no `--deselect` … there is no docker or hugo suite in this repository（plan.md EP-010 states the premise）」；EP-010 现亦在 registry 中与 plan 同数（G-02 关闭的副产品） |
| F-08 | 已于 round 3 关闭 | **保持关闭** | `contracts/ownership-map.contract.md:37-38`「exactly one of **five** forms」并列出 `extends`；关系表 10 行（`awk '/^\| Owner \| Relation \|/,/^$/'` 计数 = 10）；`feature-ref.md:121-133` 的 10 行**同序同词**；`feature-ref.md:135` 自述「the same relation set … (ten rows, same order and same relation words)」 |
| F-09 | 已于 round 3 关闭 | **保持关闭** | `quickstart.md:72-73` four fixtures（含 two-seats）+ C-17 的 reason 值域 fixture；措辞已与 F-12 的修复同向（「three named defects plus the compliant case」） |
| C-04 | open LOW | **仍 open，LOW** | §2 / §2.4 |
| C-05 | open LOW | **仍 open，LOW** | §2 / §2.4 |
| H-01 | open LOW | **仍 open，LOW** | §2 / §2.4；本轮实测计数见 §2.4 |

### 4.2 New Since Last Run（0 条）

**本轮全量复核未识别任何新的 finding。** 为使这一断言可核查，本轮按 round-3 §7.3 的建议对**全部封闭集合措辞**做了系统重扫（`exactly (one|two|three|four|five|six|seven|eight|nine|ten|[0-9]+) …` 与 `closed (set|at|three|four|five|defect)`），逐项找第二定义点：

| 封闭集合 | 定义点 | 其余出现处 | 结论 |
|----------|--------|------------|------|
| 八条 owned facts | `contracts/reporting-obligations.contract.md` C-01（owner） | `requirements.md` FR-001、`tasks.md:83,87`（按 clause id + count 断言，不重列）、`feature-ref.md:123` | 一致（F-07 关闭态保持） |
| 三动作 | `contracts/status-digest.contract.md` C-41（owner） | `plan.md` D8、`tasks.md` T009/T016/T029、contract 文件头 | 一致（F-11 关闭态保持） |
| 三值 exit-status | `contracts/status-digest.contract.md` C-45（owner） | `plan.md` D10、`quickstart.md` D、`data-model.md` E5、`research.md` U-4 | 一致（F-10 关闭态保持） |
| 四 fixture / 三具名缺陷 | `contracts/reporter-seat.contract.md` C-16（owner） | `tasks.md:99,105,273`、`quickstart.md:72`、`data-model.md:31`（"closed defect set"） | 一致（F-12 关闭态保持） |
| 五种关系形式 | `contracts/ownership-map.contract.md` C-48（owner） | `feature-ref.md:121-133`（10 行同序同词） | 一致（F-08 关闭态保持） |
| 两集合 population | `requirements.md` FR-006（owner） | `contracts/reporting-obligations.contract.md` C-04、`feature-ref.md:83`、`data-model.md:35` | 一致（"exactly two sets and no third" 四处同向） |
| 两 escape paths | `contracts/reporting-obligations.contract.md` C-04（owner） | `requirements.md` FR-006（recorded reason + FR-021 channel） | 一致 |
| 十三 RO 命题 | `contracts/reporting-obligations.contract.md` C-01…C-13（owner） | `contracts/status-digest.contract.md` C-46「exactly the thirteen」+ 13 行表 + `tasks.md` T009「the thirteen RO propositions」 | 一致（RO-01…RO-13 全树 `grep -rhoE "RO-[0-9]+"` 得 13 个不同 id） |

**另做的机械交叉核（负结果，均无命中）**：`[green:]` 悬空 0（33 个 task-row 标签全部解析到真实条款）；同一条款被两行认领 0；`[covers:]` 悬空 FR 0；FR 覆盖 22/22；六对镜像 `ok`；命令副本 `OK`；confirmation gates 27/0 violation（与 C-48 记录一致）。

### 4.3 Carried Over（3 条）

C-04、C-05（LOW，欠指定，均收窄到 owner 文档的声明面）、H-01（LOW，checklist Notes 计数与 CHK027 标注）。

### 4.4 Deferred residual（不计入 open findings）

- **A-01 residue**：`requirements.md` 的叙述层仍复述 30 秒，`contracts/ownership-map.contract.md:19` 的 "Long-run cadence default (30 s)" 也带数值。SC-006 的扫描域是 `shared/ templates/ skills/ agents/`，requirements/plan 不在域内；round 1/2/3 已裁为 deferred，本轮不重开。
- **pre-analyze 读数的调用形态**：`--repo .` → advisories 134（全 `missing-path`，13 个交付期路径名，`files=15`）；不带 `--repo` → advisories 0（跳过路径存在性检查）。registry 记录引用的是后者（`advisories=0`）；round 2 起记为 deferred，本轮沿用（§1 已复跑并全量落盘）。
- **green-tag 的原文计数**：`tasks.md:255` 写「`33` 是 claim 数 … `34` 是 raw textual occurrence count」。本轮实测：task-row 上的 `[green:]` 标签 **33** 个（与 `claimed clauses (this feature): 33` 相等，grep 复核 33 实例 / 34 个不同文本含 1 个模板），而 `grep -o "\[green: [^]]*\]" tasks.md | wc -l` 得 **35**——差额来自模板字面 `[green: <contract>#<clause>]` 在 `:48`（§ Format 图例）与 `:255`（该说明句自身）**两处**出现，而 `:255` 只计了 `:48` 一处。属自指计数的一处 +1 记账残差，不改变「33 claims / 无重复认领」的实质，不重开 E-03。
- **round-3 报告的 advisory 对照**：round-3 §1 记 134、round-2 记 124（正文 126）；本轮实测仍 134。历史记账笔误，不影响结论。
- **registry 的 analyze 记录**：`features.md:94` 的 analyze 阶段记录仍指向首轮报告；round 2/3/4 的复验记录在本报告与 `test-evidence/` 中。阶段记录义务是「记录该阶段」，不是「记录每次复验」——设计如此（round-3 §4.4 同判）。

## 5. 契约条款覆盖裁决（`account-clause-coverage.py --spec`，未 `--freeze`）

**脚本读数据（原文摘录，`round4-coverage.txt`，640 行全量落盘）**：`claimed clauses (this feature): 33`；`baseline: … coverage-baseline.txt (573 names)`；`baseline-internal existing uncovered: 573`；`uncovered beyond baseline: 19`；`[fr-uncovered] pass (0) — 22 of 22 FRs cited from citation groups`；`[clause-uncovered] fail (592)`；`[clause-unparsable] warn (107)`；`[coverage-baseline-delta] fail (19)`；`status: uncovered`；exit 1。

**19 条 beyond-baseline 未认领条款**：`ownership-map#C-48`；`reporter-seat#C-14/C-18/C-21`；`reporting-obligations#C-02/C-03/C-05/C-06/C-07/C-08/C-09/C-10/C-11/C-12/C-13`；`status-report#C-23/C-30`；`supervision-report#C-36/C-38`。

**裁决**：19 个名字与 tasks.md § Clause Coverage Ledger 的 19 行**逐名相等**，每行都有理由 + 具名 asserting row。**结论：无「无理由、无排程」的真缺口**；`status: uncovered` 的 19 条是本特性自身的未认领条款（由台账持有），573 条 baseline-internal 不阻断。**本轮读数与 round 3 逐字节相同**——修复轮未改动任何 `[green:]` 标签，故覆盖面无漂移。

## 6. 汇总表

### 6.1 Coverage Summary

| 通道 | 全集 | 已覆盖 | 裁决 |
|------|------|--------|------|
| FR → 任务行 `[covers:]` | 22 | 22（100%） | E-02 保持关闭（36 个 covers 出现，含 § Format 的图例） |
| FR → 契约 citation group | 22 | 22（100%） | `[fr-uncovered] pass (0)`；E-05 保持关闭 |
| 契约条款 → 任务 `[green:]` | 52 | 33（63.5%） | 19 未认领**全部**有台账行（E-03 关闭）；悬空 0，重复 0 |
| SC → 任务行显式 id | 10 | 6（60%） | SC-002…SC-005 由 T042 区间覆盖；SC-009 显式 `not-measured`（E-06 保持关闭） |
| Checklist `[Gap]` 处置 | 17 | 17 | 0 undispositioned（§3） |
| 冻结基线差集 | — | — | `status: uncovered`；19 beyond-baseline 全是本特性自身的未认领条款，非语料债 |

### 6.2 Feature Linkage Summary

| 信号 | 读数 | 置信度 |
|------|------|--------|
| Index 行 087 | 存在；Name/Description/Status=Planned/Details/Spec Path 齐全；Last Updated 含 requirements+clarify+plan+tasks+checklist+analyze(首轮)；**plan 记录的 EP 计数已与 plan 同数（EP-001…EP-010）** | high |
| Detail 文件 | 存在；Latest Review 与 Status Tracking 与 index 一致；EP-010 带 dated 补记；Status 维持 `Planned` | high |
| Requirement ↔ Feature 意图 | 需求主题与 Feature 描述逐句对应 | high |
| 状态合法性 | `Planned` 合法：tasks/checklist/analyze 都不拥有状态跃迁，且不得回退 | high |
| 阶段记录 | tasks + checklist + analyze 已记录；plan 记录的 EP 计数不再是 stale（**G-02 关闭**，round-3 的 G-01 不回退） | high |

### 6.3 Constitution Alignment

| 原则 | 判定 | 说明 |
|------|------|------|
| **XIV One Source of Truth**（`:230`） | **Pass** | round-3 的两个部分不符合项已消除：exit-status 三值集现只在 C-45 定义、D10 同向重述（F-10 关闭）；action 集合现只在 C-41 定义，D8/T009/T016/T029 同向（F-11 关闭）。其余封闭集合（八 facts / 四 fixture / 五 relation / 两 population / 两 escape path / 十三 RO）逐一核过，各有唯一 owner（§4.2） |
| **IV Test-First & Contract-Driven**（`:124`） | **Pass** | T009 以 C-41 判绿，而 C-41 现已声明三动作、T016 落地的是同一文件内的第三个 action ⇒ 绿点不再被后续行证伪。red-first 结构完整（T007 按 clause id + count 断言；C-16 的 four fixtures 由 T011 断言） |
| **VII SDD 工作流（Feature Index 每阶段校验/更新）**（`:158`） | **Pass** | 阶段记录齐备；plan 记录内 EP 计数已对齐（G-02 关闭） |
| **IX / X / XVII / XVIII**（框架范围 / 文档命名 / 目录治理 / 命名） | **Pass** | 零新顶层目录；registry 命名按既有兄弟；交付面 28 路径全部落在既有五棵源树 |
| **VI 持续质量与可观测性**（`:144`） | **Pass** | 本特性本身即该原则的应用；本轮的 5 份 validator + coverage 读数均为可重放证据 |
| **XV / XVI**（用户可读性 / Fast Fail） | **Pass** | 本轮 §4.1 的闭环由「改 owner 同时改全部副本」完成；本层的工具路径纠正在 §1 显式披露 |
| 其余 12 条 | **Pass**（无证据冲突） | `validate-decision-tensions` status=ok（2 records，high=0）；plan 19 行检查与产物一致 |

### 6.4 Unmapped Tasks

50 行中 15 行无 `[covers:]`：8 行以 `[green:]` 映射契约（T012/T019/T026/T032/T033/T041/T042/T043），7 行两皆无（T002/T005/T025/T040/T044/T045/T046）——均为基线采集、证据、test-pin 或基础设施行，**不欠 FR**；与 round 2/3 的 15 行一致。

### 6.5 Metrics

| 指标 | 值 |
|------|-----|
| Requirements | 22 FR / 10 SC / 15 A / 12 Edge Cases；522 行 / 32 定义行 |
| Tasks | 50 行（T001–T046 + T051–T054；Setup 5 / Foundational 5 / US1 11 / US2 10 / US3 5 / US4 7 / Polish 8） |
| Contracts | 6 文件 / 52 条款（C-01…C-52，六族前缀 RO／RS／SR／MV／DG／OM） |
| Data model | E1–E7 + INV-01…INV-12；13 个 RO 命题（C-01…C-13） |
| Clause claim | 33 / 52（63.5%），重复认领 0，悬空认领 0（`validate-tasks` 0 error） |
| Findings | **Round-4 open 3（0 / 0 / 0 / 3）**；本轮关闭 8；新增 0；carried 3；跨轮 distinct 30 |
| 分布（open） | Underspecification 2（C-04 / C-05）· Checklist 1（H-01）· Inconsistency **0** · Feature linkage **0** |
| Validation | 应验证 0 条 C/H；第三方 0；直接重读 3 条 carry-over LOW；降级率 n/a |
| Gate readings | `validate-requirements` 0/0；`validate-tasks` 0 error / 11 warning；`validate-decision-tensions` 0/0（2 records）；`pre-analyze --stage plan|tasks` pass / 0 error / 134 advisory（`--repo .`）；coverage exit 1 / status `uncovered`；mirrors 六对 ok；regen ok；confirmation gates 27 / 0 violation |

## 7. 系统性观察（不抬高任何单行 severity）

1. **round-3 的两条 HIGH 是「封闭集合的第二定义点」的教科书案例，而这一轮把它们彻底清掉了**：F-10（exit-status 三值）与 F-11（action 集合）在修复后不仅 owner 侧正确，而且是**同向重述**而非复制——D10 加了与 C-45 同方向的 MUST NOT，T009 加了「neither a fourth action nor a missing one satisfies C-41」的显式闭锁句。这比「删掉重复」更稳：后来的编辑者若再加第四个 action，会直接撞上 T009 的闭锁语。
2. **「四个副本一次性对齐」的修复质量显著高于前几轮**：F-12 的关闭覆盖了 owner（C-16）、两个执行面指导文本（US1 Independent Test / Parallel Example）、T011 的措辞、quickstart 的 route(b) 与 data-model 的一处引用——六处同向。round-3 §7.4 指出的「副本修复清单需覆盖指导文本」已被采纳。
3. **rebuild 检测面仍然有效但边际收益在下降**：本轮用 round-3 §7.3 的「封闭措辞全扫」法在 8 个封闭集合上重扫，**零新发现**——这既说明修复彻底，也说明该特征的分析面已接近饱和。若下一轮仍是 0 新发现，建议把 analyze 的固定步骤从「逐条对读」转向「只看本轮 diff 触碰的文件 + 全树封闭措辞扫描」，以守住 token 效率。
4. **三份 carry-over LOW 已经连续三轮不变**：C-04 / C-05 是 owner 文档的补充声明，H-01 是 checklist Notes 的自述统计。它们都不是「两种读法互相矛盾」，而是「尚缺一句话」。三轮不变说明它们是**真实的低优先级债务**而非被忽略的缺陷；把它们带进 implement 并在 owner 文档落地的成本最低。
5. **工具路径在派发简报中是错的**：brief 写 `pre-analyze-check.py`，实际位于 `.specify/skills/sdd-loop-driver/scripts/`。这不是 spec 缺陷，但它是一个**框架级摩擦**（见 §9.2 的 Feedback 要点）——analyze 模板只引用命令名而未钉住路径，下一位执行者仍会踩。
6. **零 C/H 不等于零工作**：本轮仍执行了 5 份 validator + coverage + 两个相关门，全部读数落盘。若只交一张空表就判绿，「GATE GREEN」会退化成一个无证据的断言——这与 SKILL 的零发现下限纪律正相反。

## 8. Next actions

1. **门禁**：**GATE GREEN**（C 0 / H 0）。可进入 `/speckit.implement`。
2. **不阻断的建议（3 条，均为 LOW）**
   - **owner 文档（T008 的交付面）**：C-04 的四条声明（idle tick 抑制 / long-run 计时锚点 / 阈值与周期关系 / 时钟跳变的区分）与 C-05 的三条行级策略（failure 行的最小内容 / 缺 reporting 字段的失败模式 / 预算规则升为契约条款）在 T008 / C-29 / C-40 落地时一并写入。
   - **checklist（H-01）**：重算 Notes 的四个数字（实测 `Gap 17 / Ambiguity 11 / Conflict 4 / Assumption 2`），同步 `checklist-selfcheck.json` 的 `dimension_hits`，并把 CHK027 从 triage 列表移出。
3. **判据保持**：若 implement / review 阶段再出现「封闭集合的第二定义点」，按 F-07 / F-10 / F-11 同一模式处理（先改 owner，再让副本引用它），不要逐条重开等级讨论。
4. **下一轮 analyze 的基线**：本报告的 3 条 LOW 成为 Round 5 的 carried-over 基线；本轮的 8 条关闭记录不再重开。

## 9. Wrap-up 记录（Run Determination / Exec Quant / Feedback / Threshold / Token / Docs）

| 步骤 | 执行 | 结果 |
|------|------|------|
| Run Determination | `run-determination.py --action determine --unit-id "/speckit.analyze" --unit-type command --run-id r20261106T040353Z-087a --complexity complex --feature 087-speckit-visualization --feature-id 087 --declared-check "C/H zero or disposed" --green-check "analyze round4: C=0 H=0; GATE GREEN" …` | **duplicate**：该 `(unit, run_id)` 的确定记录已由 round 1 落盘（`20261106T044954Z-…-087a.md`），引擎按「一轮一条」拒绝第二行；未伪造新记录 |
| Exec Quant | `exec-quant.py --action collect --unit-id "/speckit.analyze" --run-id r20261106T040353Z-087a` | **duplicate**：round 1 已采集（`20261106T044957654772Z-98988b68.json`），未写第二行 |
| Feedback Record | `feedback-utils.py --action record --unit-id "/speckit.analyze" --run-id r20261106T040353Z-087a --feature 087-speckit-visualization --feature-id 087 --review … --points …` | **duplicate: true**（`20261106T045013Z-speckit-analyze.md`）：dedup guard 按同一 `(unit_id, run_id)` 不强制重复；本轮 review/points 因而不入库，要点已落在本报告 §0 / §7 / §9 |
| Threshold Notice | `feedback-utils.py --action status` | `should_prompt: true`（287 条未提交，阈值 10）→ §9.1 的单条非阻塞通知（不暂停、不自动传输） |
| Token Reflection | 三问自评（原文转储 / LLM 代做确定性工作 / 重复读取） | ① **无**机器管理数据文件整体注入（`features.md` 只读 087 行、`checklist-selfcheck.json` 单文件、exec-quant/feedback 只读单条状态）；② 所有计数由程序得出（`grep -c` / `awk` / python 交叉核 + 五个 validator），无固定规则代做；③ **一处重复执行**：两份 `pre-analyze-check.py` 先以错误相对路径失败（§1 纠正记录），随后以真实路径重跑——第二次是必要的，第一次是路径误判造成的浪费，记为 `token-efficiency` 教训「调用前先 `find` 定位引擎，不要按目录名推断」；④ 六份合同正文全量读入（约 40 KB），本轮为闭环复核需要逐条款对读，成本合理 |
| Docs Sync Eval | 对照 `docs/concepts/documentation-model.md` 的所有权边界 | **无需记录**：本阶段只读 spec 链，未改变 `docs/` 或根入口，未产生新的用户可见能力或结构变更 |

### 9.1 Threshold Notice（非阻塞，单条）

反馈库累积已超过提交阈值。可以运行 `/speckit.feedback`（无参数）让命令自行判断去向；也可以显式要求 `package` 打包后手动发送；或选择本次跳过——不回复即视为跳过，本轮不暂停等待，也不会自动传输。

### 9.2 框架观察（供后续 feedback / 改进，不入本特性的 findings）

- **现象**：`/speckit.analyze` 的模板与 SKILL §3 只写 `python3 scripts/python/account-clause-coverage.py --spec <spec-dir>`，而 `pre-analyze-check.py` **不在** `.specify/scripts/python/`，实际位于 `.specify/skills/sdd-loop-driver/scripts/`。brief、模板正文与派发者都在用命令名而非钉住的路径。
- **摩擦**：本层按目录名推断路径，两次调用均 exit 2（`No such file or directory`），一次工具调用被浪费；下一位执行者仍会踩。
- **建议**：在 analyze 模板（`templates/commands/analyze.md`）或 SKILL §3 的固定步骤里钉住 `pre-analyze-check.py` 的完整路径，或把它登记为 sdd-loop-driver 技能的表面入口并在 analyze 侧引用。**本轮未就地修改任何框架文件**（只读约束 + 归属不明），仅在此记录。

---

**Evidence integrity**: 本报告所有计数与定位均可由 §1 的命令重放；未运行任何写命令（本文件与九份 `round4-*` 原始读数除外）；`git status --porcelain` 的既有脏文件集合（session / exec-quant / feedback / `.specify/state/`）未被触碰；未 `--freeze`、未改状态脊、未提交任何运行记录；spec 产物面（requirements / plan / tasks / contracts / data-model / quickstart / checklists / features.md / features/087.md）**零修改**（`git status --short` 对 spec 目录只显示新增的 `test-evidence/round4-*` 与本报告）。
