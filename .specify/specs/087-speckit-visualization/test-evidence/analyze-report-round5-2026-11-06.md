# Analyze Report — 087-speckit-visualization（/speckit.analyze，2026-11-06，Round 5 — 范围追加后的修订轮）

**Unit**: `/speckit.analyze` · **Run ID**: `r20261106T040353Z-087a-rev` · **Stage**: analyze（revision round，全严重度复核 + rerun delta）
**Spec dir**: `.specify/specs/087-speckit-visualization`（`REQUIREMENT_ID=087`，`FEATURE_ID=087`，`MODE=C`）
**Prior report**: `test-evidence/analyze-report-round4-2026-11-06.md`（Round 4：GATE GREEN，C0 / H0 / M0 / 3 LOW）
**Baselines under analysis**（brief 给定，逐条在树上核过）：requirements `4b34327e`（29 FR / 14 SC；新增 FR-023…FR-029、SC-011…SC-014）· plan `10e1a2df`（C-53…C-72；交付路径 40）· tasks `e922daec` + driver reset `a3d4be1a`（73 任务；T055–T078 复位为未开始）· checklist `4c89535d`（新增 94 项）· 上一轮报告 = round 4
**性质**: 严格只读。本报告是本阶段**唯一**交付产物；requirements / plan / tasks / contracts / data-model / quickstart / research / feature-ref / checklists / 注册表零修改。§1 的五份 validator 原始读数写入 `test-evidence/round5-*.txt`（证据，不是产物）。

## 0. 门禁结论（Gate Verdict）

**GATE GREEN** — CRITICAL 0，HIGH 0。

判据「CRITICAL/HIGH 为零或已处置」→ **满足（为零）**。按 SKILL § Next actions，「LOW/MEDIUM only → proceed with suggestions」，本门可进入 `/speckit.implement`。

| 严重度 | 条数 | 状态 |
|--------|------|------|
| CRITICAL | **0** | — |
| HIGH | **0** | — |
| MEDIUM | **0** | — |
| LOW | **17** | 3 条 carry-over（C-04 / C-05 / H-01）+ 14 条本轮新增/升格；均不阻断，理由见 §2 每行末句与 §2.5 |

**本轮与 round 4 的差别不是「树没动」，而是「树动了 2 个新切片，复核面因此扩了一倍」**：FR 22→29、SC 10→14、条款 52→72、任务 50→73、交付路径 28→40、checklist 60→154（94 新增）。C/H 仍为零，但 LOW 从 3 条升到 17 条——**全部落在新切片（效率元素 + `/speckit.measure`）的边界声明与两处计数自述上，没有一条落在会改变判据的地方**（逐条「为何不阻断」见 §2.5）。

### 0.1 验证波状态（显式降级，非静默）

- **同一作者门（objective-analysis-gate）**：**触发**——requirements `4b34327e` / plan `10e1a2df` / tasks `e922daec` / checklist `4c89535d` 都是本无人值守链同一 run 的前序阶段运行所写，且本 worker 是本 run 的一个子代理层（owner 判据：`.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 第 2 条）。round 4 判「未触发」是因为那一轮复核的是**前序轮的作品**；本轮复核的正是本 run 自己刚写的第二切片，故门**成立**。
- **CRITICAL/HIGH 独立验证子代理**：**不可派发**——本层是 bounded assignment，brief 明确写「不派发子代理」，宿主 Agent 类型表亦未含 `SDD Analysis Worker`。按 SKILL `references/validation-and-report.md` § Subagent-unavailable fallback 执行**直接受限重读**，在 §2 中逐条标注 `(validated: direct re-read, subagent unavailable)`。
- **降级率**：**n/a**（无第三方 validator 可对照）。本轮应验证 0 条 C/H（C/H 计数为零）；17 条 LOW 的复核走同一直接重读路径，标注同形。
- **零发现下限**：本轮 C/H/M 为零，属**阳性判定的缺席**——故 §1 保留五份 validator 原始读数、§5 保留 coverage 全量裁决、§7 保留 154 条 checklist 的逐条处置，使「无 C/H/M」成为有证据的断言，而非空表。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`MODE=C`；`AVAILABLE_DOCS` 含 research/data-model/contracts/quickstart/checklists/feature-ref/verification/tasks；`bash -n` 通过；源↔镜像逐字节相同（见 §4.6 对「语法损坏」的复核） |
| 覆盖核算（固定步骤，只读） | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/087-speckit-visualization`（**未** `--freeze`；原始读数 `test-evidence/round5-coverage.txt`，652 行全量） | exit 1；`claimed clauses (this feature): 47`；`baseline: … coverage-baseline.txt (573 names)`；`[fr-uncovered] pass (0) — 29 of 29`；`[clause-uncovered] fail (598)`（598 = 573 baseline-internal + 25 beyond）；`[clause-unparsable] warn (107)`；`[coverage-baseline-delta] fail (25)`；`status: uncovered` → §5 |
| 确定性校验 | `validate-requirements.py requirements.md`（`round5-validator-requirements.txt`） | `status: ok`，六标签全 pass（0），`scanned: 1018 lines, 43 definition rows, 0 shared strings`，0 error 0 warning |
| 确定性校验 | `validate-tasks.py tasks.md`（`round5-validator-tasks.txt`） | `PASS (with warnings)`：**0 error / 20 warning**（14 `green-cross-phase` + 6 `green-path-divergence`；`green-dangling` 0，`green-clause-collision` 0；全部在 tasks.md § WARNING ADJUDICATION 有作者裁决） |
| 确定性校验 | `validate-decision-tensions.py --spec <spec>`（`round5-validator-decision-tensions.txt`） | `status: ok`，六标签 0 命中，`scanned: 535 lines, 3 record(s)`（T-001…T-003），`channel: value_domain=HIGH-or-0, high=0` |
| 确定性校验 | `pre-analyze-check.py --spec-dir <spec> --stage plan --repo .`（`round5-pre-analyze-plan.txt`） | `stage=plan decision=pass errors=0 advisories=72 waived=0`；`fr=29 sc=14 tasks=73 clauses=0 files=18` |
| 确定性校验 | `pre-analyze-check.py --spec-dir <spec> --stage tasks --repo .`（`round5-pre-analyze-tasks.txt`） | `stage=tasks decision=pass errors=0 advisories=72 waived=0`；同一读数 |
| 检测通道 A–I | 逐产物交叉读（§2 / §3 / §4 / §6） | 17 条 open（17 LOW）+ 3 条 carry-over 复核；0 条新 C/H/M |
| 检查清单 H 通道 | 154 条逐条分诊（94 新增 + 60 既有，§7） | `unchecked + unraised + undispositioned = 0`（§7.3 给出算式） |
| 实测复核（只读） | exec-quant 存储直读（`records/*.json` + `records.jsonl`） | 187 个 per-record 文件 / 59 条 legacy / 152 `not_evaluated` + 35 有值；legacy↔per-record 重叠 **0**（§2.1 F-26、§2.4 F-28 的证据） |

**读数对照（round 4 → round 5，同一命令）**：`pre-analyze --repo .`：134 → **72**（advisory 全为 `missing-path`；`fr 22→29`、`sc 10→14`、`tasks 50→73`、`files 15→18`——第二轮切片的交付期路径名替换了第一轮的一批，净减 62 条）；`validate-tasks`：0/11 → **0/20**（Phase 8 的九条新读数 + T028↔T061、T033↔T06x 两条 path-divergence）；`validate-requirements`：`522 行 / 32 定义行` → **1018 行 / 43 定义行**；`validate-decision-tensions`：`332 行 / 2 records` → **535 行 / 3 records（T-003 新增）**，`high=0` 不变；coverage：`33 claimed / 573 baseline / 19 beyond` → **47 / 573 / 25**（与 tasks.md 台账的 47 条 claim、25 行未认领逐名相等，§5）。

**工具路径（沿用 round 4 的披露，不重复踩）**：`pre-analyze-check.py` 不在 `.specify/scripts/python/`，实际位于 `.specify/skills/sdd-loop-driver/scripts/`。本轮**先定位再调用**，两次均 `decision=pass`，无失败重试。

**读入的权威面（summary-first）**：requirements.md（29 FR / 14 SC / 26 A / 24 Edge Cases / 1018 行）· plan.md（535 行：19 行宪法检查 / T-001–T-003 / EP-001–EP-014 / S1–S2 第二切片设计 / § Mirror Obligations）· tasks.md（371 行 / 73 行任务 / § Clause Coverage Ledger / § WARNING ADJUDICATION）· contracts ×8（72 条款 C-01…C-72）· data-model.md（E1–E9 / INV-01…INV-17）· research.md（RO-01…RO-19 / U-6…U-9 / R-5）· quickstart.md（13 场景 A–M）· feature-ref.md（40 行交付路径）· checklists ×3（154 项）· `features.md` 087 行 · `features/087.md` · `reporting-obligations.md` § 九 · `exec-quant.py` 读路径 · `quant-record-schema.yaml` · `status-digest.py`。

## 2. Findings（open，17 条，全 LOW；另有 27 条已处置/不成立见 §2.6）

`propagation_surface` 是每条的第一个字段；severity 由其派生（`objective-analysis-gate.md` rule 3）。**本轮无 CRITICAL / HIGH / MEDIUM。** 编号沿用它轮前缀：`F-xx` 新增、`C-xx` 欠指定、`H-xx` 清单问责、`P-xx` 计划/任务面。

### 2.1 新切片：计数与实测不符（4 条）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **F-23** | Inconsistency（计数自述） | `none`（自述面：A22 与 Clarifications 的读数句，无下游判据引用它） | **LOW** `(validated: direct re-read, subagent unavailable)` | `requirements.md:803-805`（A22）、`:978-979`（Clarifications 的 "the evidence behind the clarifications"，同一读数复述）；`plan.md:240-241`、`:410`（EP-011 "36 of 245"）、`:411`（EP-012 "186"）、`:413`（EP-014 "189 files"）；`research.md:247,251,257,265,295,305,353`；`quickstart.md:374,379,523,527` | A22 写 `186 per-record files / 151 not_evaluated / 35 valued`，Clarifications 复述同一组；**本轮实测（2026-11-06，同一只读路径）：187 个 per-record 文件、152 `not_evaluated`、35 有值**，legacy 59 条不变（合计 246，非 245）。差值恰为两处会话自身写入的记录：本轮 analyze 轮启动时引擎已落 1 条，而 A22 的 "2026-11-06" 读数取在此前。EP-011 的 "36 of 245… every one of them `carried`" 与 A22 的 "35 valued" 互相矛盾（36 vs 35），且实测 35 条有值记录的 provenance **并非全为 `carried`**——`dispatch_quality` 写的是 `measured`（`exec-quant.py:930,941`）。EP-014/Scenario M 的 "189 files" 与今天实测的 191（187+1+1+1+1，含 `records/`、`records.jsonl`、`scores/`、`scores.jsonl`）同属时点差 | 把这四处读数各自的采集时刻写进句子（"measured … at <UTC> on 2026-11-06, N per-record files"），并让同一个数只出现在一个地方、其余按指针引用（constitution XIV）。若不愿维护时点数字，就把 A22 的绝对计数换成"覆盖率是数据条件，每次读取自行报告 covered=<k>/<n>"的形式。**为何不阻断**：没有任何 FR/SC/契约条款以 186/151/35 为判据——FR-023/FR-027 要求的是**每次渲染自报 covered/omitted**，不是复现某个常数；SC-011…SC-014 的判据取自 fixture store。失准的只是自述性证据句 |
| **F-24** | Ambiguity（存储读取的语义） | `none`（呈现层读取语义；下游 = `/speckit.measure` 的计数与元素取值，由 C-58 的 accounting identity 在运行时自证） | **LOW** `(validated: direct re-read, subagent unavailable)` | `requirements.md:350-353`（Edge Case "The same record reached twice"）、`:879-882`（§ Out of Scope 的 "De-duplicating … stay with the store engine's read path"）、`:681`（Boundary 表的同句）；`contracts/measure-report.contract.md` C-58（accounting identity）、`contracts/efficiency-element.contract.md` C-66；`scripts/python/exec-quant.py:1124-1127`（`load_records`） | 三处文本都宣称「引擎的读路径**已按 record identity 去重**」，并要求两个新读取"through that reader's own record identity, so one measurement is one record in the counts"。**实测：`load_records()` 只是 `read_jsonl_safe(legacy) + read_entry_files(records/)` 的拼接，全函数无任何去重**。今天两面具 **0** 重叠，故缺陷不可观测；一旦 legacy 流与 per-record 目录描述同一次测量，`record count`、`median`、`invocation count` 与 C-58 的 identity 都会双计，而 C-58 的等式仍会自洽（两侧同时 +1）——即**运行时自证救不了它** | 二选一并写进 owner：**(a)** 把三处句子改成事实（"the reader concatenates both surfaces; this feature adds no de-dup rule and relies on the engine's write path never producing an overlap"）——这是纯更正，与引擎源码一致，可逆；或 **(b)** 若确实需要去重，那它是 `exec-quant.py` 读路径 owner 的变更，本特性按路径引用。**推荐 (a)**。**为何不阻断**：今天重叠为 0，任何 fixture 与任何 SC-013 判据都不会被这条句子影响；它伤的是"读取语义的说明是否属实"，不是判据 |
| **F-26** | Ambiguity（身份实现） | `none`（同一引擎读路径的实现层；C-66 的 tie-break 在 0 重叠下不可观测） | **LOW** | `data-model.md:197`（E8 `source_record` = "record identity (the record file's name stem)"）、`:198`（`degradation`）；`contracts/efficiency-element.contract.md` C-66（ties by record identity）、`contracts/measure-report.contract.md` C-55/C-57（truncation by record identity）；`requirements.md:493-495`、`:541`；`exec-quant.py:317-328`（`read_entry_files`）、`:1140-1158`（`read_jsonl_safe`）、`:1124-1127` | 「record identity」被三处用作 tie-break 与截断键，但**没有任何一处定义它在读取后的形态**。实际可用的只有 file name stem（E8 这么写），而 `read_entry_files`/`read_jsonl_safe` 返回的是**去掉文件名后的 dict**：13 个键里没有 `id`/`path`/`identity`，legacy 流的行更没有文件名。于是：①「以 record identity 升序 tie-break」在 pin 住的读路径上**不可实现**，除非读取方自己保留文件名（即重实现读取）；②`source_record` 在 legacy 记录上不可填 | 在 C-66 或 E8 里加一句"identity 的实现形态"：per-record 文件 = 文件名 stem；legacy 行 = 行序号或 `(collected_at, run_id, unit_id, unit_type)` 元组。若都不行，就删掉 tie-break 句子并把"不可判定"记入 § Out of Scope。**为何不阻断**：tie 需要同一 unit 两条记录 `collected_at` 完全相等，今天 0 例；SC-011 的 fixture 不构造它 |
| **F-28** | Ambiguity（数量未定义） | `none`（新切片的口径；SC-013 判据只要求"per unit 报告 invocation count"，未钉其定义） | **LOW** | `requirements.md:469-470`（FR-023 "its invocation count"）、`:524-525`、`:546-547`（FR-027 "invocation counts are **sums**"）；`data-model.md:196`（E8 `invocations`）；`checklists/efficiency-measure-2026-11-06.md:44`（CHK003 的同一问） | "invocation count" 作为一个**要报告的量**从未对着记录字段下定义（CHK003 问的正是这个）。记录 schema 声明的 13 个键里没有 invocation 计数；`config_fields` 里也没有。FR-027 说它是"sums"，即"每条记录的该量求和"——但**该量本身不存在**，于是它只能恒为 not-evaluated。今天实测：token 量在全部 247 条记录上缺席（A22 已承认），invocation 同 | 在 FR-027 的 Aggregation 句里点名字段来源（"the invocation count is the record's `<key>`; where the record carries none the quantity is not evaluated"），或把 invocation 从 FR-023/FR-027 的必报清单里移出（它本来就是"where the source record carries them"条件句的一部分——只需让 FR-027 的 sums 句同样带条件）。**为何不阻断**：FR-027 的 "a quantity absent from **every** contributing record is reported as not evaluated" 已经**闭合**了这个状态；缺的是"这个量对应哪个键"，不是"缺了怎么办" |

### 2.2 新切片：封闭集合与定义域（3 条）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **F-19** | Conflict（封闭集合） | `none`（把 marker 字面钉在锚点处；下游 SC-011 判据由 C-64/C-67 与 `test_efficiency_element.py` 提供） | **LOW** `(validated: direct re-read, subagent unavailable)` | `contracts/ownership-map.contract.md:39`（"Not-evaluated marker literal" 行）；`shared/guidelines/reporting-obligations.md` § 九（锚点指向处）；`requirements.md:472-473, 192-194, 295-296`（三处措辞）；`exec-quant.py:148`（`NOT_EVALUATED = "not_evaluated"`）、`:1116`（`_field_text` → `"-"`）；`status-digest.py`（渲染字面） | 两处冲突：①**C-47 把 marker 字面的 owner 指给 `reporting-obligations.md § 九`，而该节正文里没有这个字面**（本轮逐行读 § 九：只有 bounded / omitted / stale / nothing-running 四张面，无 marker 词）；C-47 自己的 judged-by 是 "exactly one definition site per row"，这条行按判据**必然红**。②框架里其实有**三个**不同字面在跑：需求与契约写 `not evaluated`（带空格，英文散文）、schema 常量与记录取值写 `not_evaluated`（下划线，数据层）、`_field_text` 与 `status-digest.py` 对缺值渲染 `-`（单个连字符）。SC-011 判据是"renders the explicit not-evaluated marker and neither `0` nor an omission"——**哪一个字面算满足？** | 二选一并写进 owner：**(a)** 在 `reporting-obligations.md § 九` 里新增一行"not-evaluated marker literal = `<字面>`"，并说明数据层 `not_evaluated` 与呈现层的关系；**(b)** 把 C-47 的 owner 改成 `contracts/efficiency-element.contract.md` C-67（它才是本特性渲染规则的 owner），让 § 九 只做 vocabulary 指针。另需一句：`-` 是否算 marker。**为何不阻断**：判据已经**语义闭合**（"never `0`, never an omission, never an average"），任何一种非空标记都同时满足这三条否定；缺的是"字面唯一"，影响的是 C-47 的 judged-by 与两份文本的一致性，不是 SC-011 的可判定性 |
| **F-20** | Ambiguity（未定义项） | `none`（status line 的宿主面；SC-011 的语言由 C-64/C-67/C-68 提供） | **LOW** `(validated: direct re-read, subagent unavailable)` | `requirements.md:474, 476-479`（FR-023 的 "entry bound the surface already applies"）；`:421-423`（FR-012：**只有 digest** 有 cap）；`:944-945`（Clarifications 复述）；`quickstart.md:489-490`（Scenario L premise 1 "the host surface's bound is the only bound"）；`contracts/efficiency-element.contract.md` C-64 退化规则 | **CHK093 命中，本报告判为真缺口。** FR-023 有两处把"the entry bound the surface already applies"作为**每一**个宿主面的既有事实——但 FR-012 的 cap 只属于 **digest**；**status line 的条目上界在 requirements / plan / contracts / data-model 四处都没有定义**（A17 的"which is what keeps the status line one screen"只是比喻）。于是：①"at most one bounded element per listed unit **inside the bound**"在 status line 上是**无判据的条件**；②C-64 的 all-or-nothing 退化（token/invocation 撤回）在 status line 上**没有触发阈值**，即撤回规则在那里不可判定 | 在 FR-012 的同一位置补一句 status line 的界（可以是"the line names at most N entries"或"the line is one host-console line and carries at most the units it already names"），或把 FR-023 的 "the entry bound the surface already applies" 改为"the digest's declared cap (FR-012); the status line's own line budget as declared by the reporter Template"。**为何不阻断**：SC-011 的判据链（marker → not `0` / not omission / not average；absent store → "no measurements"；render-wide withdrawal）由 C-64/C-67/C-68 三条款独立给出，**不引用 bound 的数值**；缺的是 status line 场景下"何时触发撤回"的阈值，而该场景今天由 Scenario L 以 premise 形式声明 |
| **F-21** | Ambiguity（未定义项） | `none`（元素与 guard 的关系；RO-13 的下游判据由 C-46 的十三命题表提供） | **LOW** `(validated: direct re-read, subagent unavailable)` | `checklists/efficiency-measure-2026-11-06.md:133`（CHK071）；`contracts/status-digest.contract.md` C-46（"exactly the thirteen propositions" + 13 行"what this guard reads"表）；`tasks.md:218`（T062 "no new action, file or unit set"）；`requirements.md:466-479`（FR-023 通篇不提 FR-017/guard） | **CHK071 命中，本报告判为真缺口。** C-46 把 guard 的命题集**封闭**为十三项，其"what this guard reads"表逐行只读 registry / roster / owner 文档 / captured line set / run record / changed-file set；效率元素**不在**任何一行的读取域内。T062 同时禁止元素引入新 action。于是"元素出现是否、以及如何影响 guard 的判定"在 requirement 面**完全未声明**——既没说"不判"，也没说"判哪一面"（presence / marker / bound compliance）。读者无法从任一 FR 推出答案 | 在 FR-023 末尾加一句显式的**否定声明**（"Nothing in this element is a proposition of the FR-017 guard: the guard's proposition set is closed at thirteen and the element neither adds one nor changes any verdict"）。这是最小、可逆、与 C-46 同向的补句；若确实希望 guard 判它，那就要动 C-46 的封闭集——那是裁定，须回到 plan/tasks 阶段。**为何不阻断**：C-46 的封闭集**已经排他**，所以 guard 的行为今天就是确定的（不判）；缺的是让读者不必靠"排除法"才能知道这一点 |

### 2.3 新切片：边界与任务面（4 条）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **F-25** | Ambiguity（跨切片残留） | `none`（US6 的叙述层；SC-011…SC-014 不引用它，FR-027 的否定句已封闭） | **LOW** `(validated: direct re-read, subagent unavailable)` | `requirements.md:219-222`（US6 的 "how does that compare to the baseline?"）、`:228-229`（"the historical window the comparison used"）；`:529-530`（FR-027 "no comparison-to-baseline recommendation is issued"）；`:787-789`（A19 "Trends are read as a window comparison the caller selects"）；`checklists/efficiency-measure-2026-11-06.md:152-153`（CHK084/CHK085） | **CHK084/CHK085 命中，判为真但低。** US6 把用户的问题写成**两次基于 baseline 的比较问答**（"how does that compare to the baseline?" / "the historical window the comparison used"），而 FR-027 明写"no comparison-to-baseline recommendation is issued"、A19 明写"never as a stored baseline series"。两者的可调和读法是"present measurements, refuse the verdict"——但**没有任何一句写下来**，而 US6 是需求正文，SC-013/SC-014 的判据又只覆盖"present"这一侧。一个照 US6 实现的人会给报告加一节 baseline 对比，而那正好撞上 FR-027 | 在 US6 的问题句后加一句括注：("the entry answers with this window's measurements and the caller-selected earlier window it names; it issues no verdict and stores no baseline")。**为何不阻断**：FR-027 的否定句 + A19 的定义已经给出**唯一与二者都相容的读法**，且 C-53…C-61 全部按"presentation only"写成；US6 是 the story 的动机层，不是判据层 |
| **F-27** | Ambiguity（切片边界） | `none`（交付面申报；SC-010/SC-014 的判据读 `base..head` 的 changed-file set） | **LOW** | `requirements.md:575-580`（FR-029）、`:838-853`（§ Out of Scope）；`plan.md:269`（"and 186 in total"，§ Mirror Obligations 的 per-directory copies 28→29）；`feature-ref.md:66`（"**40 paths**: the original 28 plus the second slice's 12"）、`:219`（Stage status 的 "this file (40 delivered paths)"）；`tasks.md:25`（DoD-1 "all 28 `feature-ref.md` § Delivered paths"） | 四处交付面表述互不相等且都可被读成权威：feature-ref 说 40、Stage status 说 40、DoD-1 说 28、§ Mirror Obligations 说"per-directory copies 28→29"。**DoD-1 的 28 是上一轮留下的原文**（它已 `met-with-void-rows`，读的是第一切片的 28 条），本轮第二轮切片把 12 条加进来后，**没有任何一处说清了"40 条里有 12 条是新切的、其中 6 条是 NEW 文件、6 条是编辑既有文件"**——而 SC-014 的判据正好读"the additions are one command template, one stdlib-only script, the regenerated per-tool command copies and their tests" | 把 DoD-1 的 "28" 更新为"40（28 + 12；逐条见 feature-ref § Delivered paths）"，并让 feature-ref § Delivered paths 的 40 行各自带一个"new / edited / generated"标记（现在只有第 36、40 行带 "(edited)"）。**为何不阻断**：feature-ref § Delivered paths 的 40 行是**逐条可数**的（本轮实测 40 行），DoD-1 的 28 是已完成的上一轮断言，不是待办判据；SC-014 的判据落在 `changed-file set` 而非这个数字 |
| **F-29** | Staleness（阶段记录） | `none`（注册表/索引的记录面；不改变任何判据） | **LOW** | `feature-ref.md:215-221`（§ Stage status）、`tasks.md:25`（DoD-1 仍写 "all 28"）；`.specify/memory/features.md`（087 行）、`.specify/memory/features/087.md` | feature-ref 的 § Stage status 仍写 plan = "**this stage** (revised 2026-11-06…)"、tasks = "not started"、checklist/analyze = "not started"——而 tasks `e922daec`、checklist `4c89535d`、analyze（本报告）都已落地。需求面的 "29 FR / 14 SC, 15 assumptions" 也与实测的 **26** assumptions（A1…A26）不符 | 在 tasks/checklist 落地时同步该表的四行（阶段记录义务是"记录该阶段"，feature-ref 的表是**同一份文件的**叙述，不属于"每次复验都记"的豁免面）。**为何不阻断**：`features.md` 的 087 行是状态与阶段记录的**权威载体**，feature-ref 的 § Stage status 是派生叙述；`validate-*` 与 coverage 都不读它 |
| **P-01** | Inconsistency（选项清单） | `none`（plan D 区选项枚举的自述；S2 设计与 C-53…C-62 各自独立给出判据） | **LOW** | `plan.md` § Second-slice design 的 `--since`/`--window`/`--unit`/`--cap`/`--workspace` 表；`requirements.md:532-535`（FR-027：`--since` = start，`--window` = span，二者皆缺 = 全部）；`:817-823`（A24） | S2 的参数字表把 `--workspace` 列为 measure 的参数之一，但 FR-027 只声明了 `--since` / `--window` / `--unit` / `--cap` 四个参数及其语义；`--workspace` 的语义只出现在 FR-011 的 digest workspace 规则里。读者无法判断 measure 是否接受 `--workspace`，若接受则其语义未被任何条款钉住 | 在 S2 表里把 `--workspace` 标为"shared with the digest's FR-011 rule, not a fifth window argument"，或在 FR-027 里补一句其继承关系。**为何不阻断**：C-55/C-56 的判据是"the selection echoes the exact `(unit_id, unit_type)` set it resolved"，与 `--workspace` 无关 |

### 2.4 Carry-over（3 条，不变）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **C-04** | C 欠指定 | owner 文档（T008）声明面 | **LOW**（carried over，第 4 轮） | 同 round 4（`requirements.md:206-212` / `:243-246`；Edge Cases；`tasks.md:87`） | 四条 owner 级口径仍无声明：idle tick 抑制 / long-run 计时锚点 / 阈值与周期关系 / 时钟跳变区分。**本轮复核：逐字未动**（第二切片未触碰 first-slice 的 FR-003/FR-009）。第二切片新增了一条相邻口径（FR-023 的 "elapsed quantity is unconditional and comes first"），它与 C-04 的 ④ 项（时钟跳变）相邻但不重合 | 保持 round 4 建议。**为何不阻断**：同 round 4——owner 正文补句，不改任何 FR/SC 判据 |
| **C-05** | C 欠指定 | 行级策略（owner + 渲染器） | **LOW**（carried over，第 4 轮） | 同 round 4（`requirements.md:172-174`；C-29；C-40） | 三条行级策略仍缺：failure 行四要素 / 缺 reporting 字段的失败模式 / 预算规则升为契约条款。**本轮复核：逐字未动** | 同 round 4。**为何不阻断**：C-29 已钉住三个可判定断言 |
| **H-01** | H 清单问责 | checklist 证据（`checklist-selfcheck.json` / § Notes） | **LOW**（carried over，第 4 轮） | `checklists/framework-visualization-2026-11-06.md:138-142`（Notes 的 measured 计数）、`:152`（triage 列表仍列 CHK027） | **本轮重算，数值与 round 4 相同**：`Gap 17（声称 19）/ Ambiguity 11（13）/ Conflict 4（6）/ Assumption 2（3）`。**新增同型问题**：新增的 94 项 checklist 的 Notes 也有自述计数面（`checklists/efficiency-measure-2026-11-06.md:205-211` 的 selfcheck 引用），若沿用同一算法需一并核 | 同 round 4；另把新清单的自述计数一并在下一次 checklist 修订时重算。**为何不阻断**：60+94 条问责通道本身健康（§7：`unchecked + unraised + undispositioned = 0`） |

### 2.5 为何 17 条 LOW 全不阻断（统一判据）

1. **没有一条落在会改变 SC 判据的地方**：SC-001…SC-014 的判据链逐条追到 owner（C-64/C-67/C-68 覆盖 marker 与 absent store；C-58 的 accounting identity 覆盖排除计数；C-59 覆盖 exit set；C-61 覆盖 determinism；C-69 覆盖 byte-identical）。17 条全部落在**自述性证据句**（F-23 / F-29 / P-01）、**锚点的字面唯一性**（F-19）、**未定义项的取值**（F-20 / F-21 / F-25 / F-28 / F-26）、或**读取语义的说明是否属实**（F-24 / F-27）。
2. **没有一条是「两种读法互相矛盾且两种都能落地」**：F-19 的三字面在语义上等价（都满足 FR-023 的三条否定）；F-20/F-21 是**缺一句**而非两句冲突；F-24 是说明与源码不符，但替换成事实即闭合。
3. **每条都有最小、可逆的补法**，且都不需要动第二份文件的判据。
4. **承载者明确**：F-19/F-20/F-21/F-25/F-28 由 `FR-023`/`FR-027`/C-46/C-47 的正文一句承载；F-23/F-29/P-01 由自述层的重算承载——都是 implement 阶段顺路可做的事，不需要回到 plan。

### 2.6 已处置 / 不成立（27 条，不占 open 计数）

| 来源 | 计数 | 处置 |
|------|------|------|
| brief 点名的 triage 项 | 7 | **全部逐条处置**（§3） |
| brief 点名的已知异常 | 4 | **全部逐条处置**（§4） |
| 新 checklist 的 `[Gap]` 项 | 14（另 2 项与 triage 项重合） | 14 条 covered-by，0 raised（§7.2） |
| 新 checklist 的非 Gap 项 | 78 | 78 条 covered-by（§7.2） |
| 既有 checklist 的 60 项 | 60 | 沿用 round 4 的 17 条处置，本轮复核未变（§7.1） |
| 触发的同一作者门 | 1 | 已在 §0.1 显式记录（非 finding，是流程状态） |

## 3. brief 点名的 7 个 triage 风险（逐条裁定）

| CHK | 问题原文要点 | 本轮裁定 | 证据 |
|-----|--------------|----------|------|
| **CHK019** | FR-027 开头 "an end that defaults to **now**" 与同一要求后文 "an invocation with neither covers **all records the store holds**" 是否给出两个不同的窗口？ | **不成立**（两读法可调和，唯一自洽读法存在） | FR-027 的 Window semantics 句写的是参数级语义：`--since` 给 start 时 end 缺省为 now（`:532-534`）；"neither bound" 是**另一个**情形（`:533-534`）。两条不重合：一条是"有 start 无 end"，一条是"无 start 无 end"。round 4 已按此裁；本轮复核 A24（`:817-823`）同向复述（"the 'no bounds means the whole store' default"），**未再出歧义**。**不升 finding** |
| **CHK022** | FR-027 的 "a central value" 与同一要求的 **median** 规则是否两个中心统计量？ | **不成立**（同义重复，非并列定义） | `:526` 用 "a central value, each named" 描述 distribution summary 的**三个具名量之一**；`:545-546` 的 Aggregation 句把它**钉成** "the per-unit elapsed figure is the **median** … with the minimum and the maximum named alongside it"。后句是对前句的兑现，不是第二个值。**残余**：A19（`:786`）仍用 "central value"，属同义复述，不构成第二定义（它不声明取值）。**不升 finding**，记为 §2.6 的 covered |
| **CHK025** | 四个排除类 + "`outside-cap` is not a fourth class"——计数差一？ | **部分成立，但已由 FR-028 自身闭合** | 实际有**四**个类（`unreadable` / `legacy-format` / `outside-window` / `unknown-unit`，`:528`），`outside-cap` 是**第五个被排除的计数**而非类，故 "not a fourth class" 应为 "not a fifth"——`plan.md` 的 S2 与 `:1010` 的 Clarifications 同向写 **"a fifth class"**，说明 plan 侧已经更正。FR-027 的 "**not a fourth**"（`:540`）与 `:1010` 的 "as **a fifth class**"（Clarifications 的答句）**在同一份文件里用两个不同的序数说同一件事**。**判为 LOW 复查记账**（并入 §2.3 的文本面，不单开一行，因为它不改变任何判据：C-58 的 accounting identity 用名字而不用序数） | `:540` vs `:1010`；`plan.md` S2 |
| **CHK033** | "five named things"（两种 render、input-error、nothing-to-analyse、success）vs 四值封闭集？ | **不成立**（FR-028 自封闭） | `:558-560` 先说 "at minimum a summary render and a machine-readable render … an input-error status, a nothing-to-analyse status … and the success status"（这是**功能清单**，五项里前两项是 action 不是 status），紧接着 `:562-568` 写 "**The closed exit-status set** is exactly four values: `0` … `2` … `3` … `1`"。条款**自己**把"功能清单"与"状态集"分开并封闭状态集。C-59 同向（四值），tasks T069 逐值断言。**不升 finding** |
| **CHK084 / CHK085** | US6 的 "compare to the baseline" / "the historical window the comparison used" vs FR-027 的 no-comparison / A19 | **成立，LOW** | → **F-25**（§2.3） |
| **CHK093** | status line 是否有 entry bound？ | **成立（真缺口），LOW** | → **F-20**（§2.2）；FR-012 的 cap 只属 digest，status line 的界四处皆无 |
| **CHK071** | 效率元素与 FR-017 guard 的关系是否声明？ | **成立（真缺口），LOW** | → **F-21**（§2.2）；C-46 十三命题封闭，元素不在任何读取域内，且无任何 FR 声明"不判" |

**另记**：新 checklist 的 Notes（`:216-220`）另列 CHK083（"one element per unit" vs "per listed entry"）为待分诊项。本轮复核：FR-023 的 "at most one … **per unit**"（`:468`）与 FR-024 的 "rendered for at most the **entries** that surface already lists"（`:491-492`）是**两个不同维度**（一个 unit 至多一个元素 / 元素只出现在已列条目上），同一条目列表在同一 unit 名下出现两次属 digest 的 cap 行为，C-43 已管。**不成立**。

## 4. brief 点名的 4 个已知异常（逐条复核）

| 异常 | 复核结论 | 证据 |
|------|----------|------|
| **Phase 8 悬空交叉引用**（T055 指向 T073 的 closure read；T073 散文认领 C-63 却挂 C-68） | **部分复现，判 LOW，并入 F-27 的计数面** | ①`tasks.md:222` T066 声称 "the two import sites"，但其 `[green:]` 与 prose 的 subject 是 C-61（determinism/read-only）；`tasks.md:218` T062 声称 "no new action"，subject 与 C-63 一致。②**真正的悬空仍在**：`tasks.md:230` T073 的正文说 "the two-surface counting clause"（= C-63）而它挂的是 `efficiency-element#C-66`；`tasks.md:229` T074 的正文说 "this row's captured runs are the reading the one-reader clause's second projection is judged on"——"one-reader clause" 是 **C-65**，而 C-65 在台账里明确**无人认领**（tasks.md § Clause Coverage Ledger 第 1 行），T074 挂的是 `C-?`（无 green 标签）。③`validate-tasks` 报 0 `green-dangling` / 0 `green-clause-collision`——**因为它是按标签而非按散文判的**，散文悬空对 validator 不可见。**这与 tasks-revision-2026-11-06.txt § 2 的自述一致**（该 pass 已显式保留此残余，理由是"rows are frozen"） |
| **Phase 8 id 跳号（无 T057）** | **复现且已文档化，判不成立** | 实测 73 行，id 区间 `T001–T078`，缺 `T047/T048/T049/T050/T057`。前四项是**设计如此**（tasks.md:370 明确解释：四条迟到行取 `T051–T054`，故 47–50 从未分配）；`T057` 的缺席在 `tasks.md:370` 有具名说明（"one id was skipped at authoring, and it is **not** reclaimed here"），`tasks-revision-2026-11-06.txt § 4` 复述。**全树无任何引用 `T057` 的悬空指针**（`grep -rn T057` 只命中这两处说明句）。`decomposition-check.py` 的 `task_count: 73` 与最高 id `T078` 的差由这两组跳号解释，已记录。**不构成 finding** |
| **`check-prerequisites.sh` 语法损坏** | **不复现** | `bash -n .specify/scripts/bash/check-prerequisites.sh` → 通过；实跑 → exit 0，`MODE=C`，`AVAILABLE_DOCS` 完整；`scripts/bash/check-prerequisites.sh` 与 `.specify/` 副本**逐字节相同**（`diff` 无输出）。**不构成 finding**；该报告要么指向了修复前的状态，要么是误记 |
| **count claims（29 / 14 / 72 / 73 / 40）与 tree 实测** | **五项全部与实测一致（1 处偏差：73）** | FR **29**（`grep -cE '^- \*\*FR-[0-9]{3}\*\*'`）；SC **14**；条款 **72**（8 文件 `^## C-\d\d` 去重计数，C-01…C-72 无缺号）；交付路径 **40**（feature-ref § Delivered paths 的表格行）；任务 **73**（`^\- \[[ x]\] T\d+` 计数 = 73，含跳号）。**唯一偏差**：`tasks.md` § Clause Coverage Ledger 自称 "47 claimed / 25 unclaimed / 72"，而 coverage 脚本输出同为 47 / 25 / 72——**完全一致**。**DoD-1 的 "28" 是唯一与实测不符的计数**（→ F-27） |

## 5. 契约条款覆盖裁决（`account-clause-coverage.py --spec`，未 `--freeze`）

**脚本读数（原文摘录，`round5-coverage.txt` 652 行全量落盘）**：

```
scanned 274 files: parsed 167 + named-unparseable 107 == 274  [relational sentinel OK]
clause universe: 1748 distinct names over 167 parsed files (1772 ids extracted)
claimed clauses (this feature): 47
baseline: .specify/specs/087-speckit-visualization/coverage-baseline.txt (573 names)
uncovered beyond baseline: 25
  [clause-uncovered] fail (598) — 598 uncovered, 25 beyond the frozen baseline
  [fr-uncovered] pass (0) — 29 of 29 FRs cited from citation groups
  [clause-unparsable] warn (107) — 107 files yield no clause id under the owner's forms; 0 declare a positive form
  [coverage-baseline-delta] fail (25) — baseline holds 573 names; 573 uncovered items are baseline-internal and do not block
status: uncovered                                          (exit 1)
```

**25 条 beyond-baseline 未认领条款**（逐名）：`efficiency-element#C-65`, `#C-69`, `#C-70`, `#C-71`；`measure-report#C-60`；`ownership-map#C-48`；`reporter-seat#C-14`, `#C-18`, `#C-21`；`reporting-obligations#C-02`, `#C-03`, `#C-05`…`#C-13`（11 条）；`status-digest#C-72`；`status-report#C-23`, `#C-30`；`supervision-report#C-36`, `#C-38`。

**与 tasks.md § Clause Coverage Ledger 的对账**：台账声明的未认领集合为同一 25 个名字**再加** `efficiency-element#C-64`（26 行），而 C-64 实际由 **T077** 认领（`[green: contracts/efficiency-element.contract.md#C-64]`），故不在脚本的 beyond-baseline 集合里。**26 − 1 = 25，逐名相等，无差集、无多项。** 本轮新增的 6 个名字（C-65、C-69、C-70、C-71、C-60、C-72）**全部**在台账里有具名行 + 理由 + asserting row。

**裁决**：`status: uncovered` 的 25 条是本特性**自身**的未认领条款（由台账持有，非语料债）；573 条 baseline-internal 不阻断。**身份闭合**：47 claimed + 25 unclaimed = 72 = 8 文件条款全集，**无「无理由、无排程」的真缺口**。

**round 4 → round 5 的覆盖面漂移**：`33 claimed / 19 beyond / universe 1728（165 parsed files）` → `47 claimed / 25 beyond / universe 1748（167 parsed files）`。claimed +14 = 第二切片被认领的 20 条（C-53…C-57、C-59、C-61…C-64、C-66…C-68 等）减去台账明列未认领的 6 条（C-60、C-65、C-69、C-70、C-71、C-72）；beyond +6 正是那 6 条；universe +20 = 新 20 个条款名（C-53…C-72），与 8 文件 / 72 条款的封闭集一致。

## 6. Rerun delta

### 6.1 Resolved Since Last Run

**本轮无「关闭」项**——round 4 的 3 条 LOW（C-04 / C-05 / H-01）**逐条复核后仍未关闭**（§2.4），且第二切片未触碰它们所在的文本。round 4 的 8 条历史关闭项（F-10 / F-11 / F-12 / F-13 / G-02 / E-03 / F-03 / F-04 / F-08 / F-09）本轮**按 round 4 的结论维持关闭**，抽检 3 条：

| ID | 抽检结论 | 复核依据 |
|----|----------|----------|
| F-10（digest exit-status 三值唯一） | 维持关闭 | `requirements.md` 首切片 FR-011 与 C-45 同向；第二切片的 FR-028 引入的是**另一个**封闭集（measure 的四值），两集不交叉定义（C-59 vs C-45），无第二定义点 |
| F-11（action 集合三值唯一） | 维持关闭；**新增一个平行面** | digest 仍三动作（C-41）；measure 两动作（C-60，`summary`/`json`）。两者是**两个不同脚本的动作集**，不构成同一封闭集的第二定义。已在 §7 的 C-46 行确认 guard 仍是十三命题、无第四动作 |
| F-12（四 fixture 三具名缺陷） | 维持关闭 | C-16 与 US1 Independent Test 未动 |

### 6.2 New Since Last Run（14 条）

`F-19`（marker 字面 owner 悬空 + 三字面并存）、`F-20`（status line 无 entry bound）、`F-21`（元素与 guard 关系未声明）、`F-23`（store 计数自述与实测不符）、`F-24`（"引擎按 record identity 去重"与 `load_records()` 源码不符）、`F-25`（US6 baseline 比较残留）、`F-26`（record identity 不可得）、`F-27`（28 vs 40 交付面计数）、`F-28`（invocation count 未定义）、`F-29`（feature-ref § Stage status 陈旧）、`P-01`（`--workspace` 在 S2 表 vs FR-027 四参数）。

其中 `F-19` / `F-20` / `F-21` / `F-23` / `F-24` / `F-26` / `F-28` 是**新切片引入的**；`F-25` 是新切片的 US6；`F-27` / `F-29` / `P-01` 是新切片落地时**未同步的旧面**。

### 6.3 Carried Over（3 条）

`C-04`、`C-05`、`H-01`。

### 6.4 Deferred residual（不计入 open findings，沿用前轮）

- **A-01 residue**：`30 秒` 在叙述层的复述（SC-006 的扫描域不含 requirements/plan）。round 1–4 已裁 deferred，不重开。
- **pre-analyze 调用形态**：`--repo .` → 72 advisories（全 `missing-path`，第二切片的交付期路径名）；不带 `--repo` → 0。registry 记录引用后者。沿用前轮判定。
- **green-tag 原文计数**：`grep -o '\[green: [^]]*\]' tasks.md | wc -l` = **52**，其中 3 处是图例 / 说明句的模板字面（`contracts/…#C-nn`、`contracts/`、`contracts/[^ <contract>#<clause>`），49 处是真实 tag；而 `account-clause-coverage` 报 **47** 个 distinct 条款——差额 2 是同一 clauses 被两行各引用一次的情形（`validate-tasks` 的 `green-clause-collision` 会抓这一类，本轮读数 **0**），说明这 2 个是同一行内的重复或同一 clause 的两处引用。**属自指计数的记账残差，不改变「47 claims / 无重复认领」的实质**，不重开 E-03。
- **T073 散文 vs 标签**（§4）与 **`F-27` 的 28/40**：均已由本轮 tasks-revision pass 显式保留，属「rows are frozen」的裁定面，不是可就地纠正项。

## 7. 检查清单问责（§ H pass，154 项）

### 7.1 既有清单（`framework-visualization-2026-11-06.md`，60 项）

**与 round 4 逐条相同，无新增/关闭**：3 条已 `[x]`（CHK002 / CHK027 / CHK054）、17 条未勾选 `[Gap]`（10 covered-by + 7 raised-as-finding），`unchecked + unraised + undispositioned = 17 + 0 + 0`。逐条处置沿用 round 4 §3（CHK003/005/006/007/009/021/023/039/040/044 covered-by；CHK017/018/032/034/036/046/058 → C-04×4、C-05×3）。

### 7.2 新增清单（`efficiency-measure-2026-11-06.md`，94 项）

**94 项全部未勾选；其中 16 项带 `[Gap]` 标记**（另有 2 项 CHK058/CHK065 同时带 `[Coverage]`）。处置：

| CHK | disposition |
|-----|-------------|
| CHK002 | `CHK002 disposition: covered-by requirements.md § FR-024（"the latest record by `collected_at` for the unit the surface is already listing"; no window on a surface）+ § FR-027（window semantics）` |
| CHK003 | `CHK003 disposition: raised-as-finding F-28` |
| CHK006 | `CHK006 disposition: covered-by contracts/measure-report.contract.md C-60（two closed actions + the JSON key set）` |
| CHK007 | `CHK007 disposition: covered-by requirements.md § FR-029（"the standard wrap-up delegation the other commands carry"）+ § FR-026（what the entry MUST NOT do）` |
| CHK008 | `CHK008 disposition: covered-by contracts/measure-report.contract.md C-59（`0` … stated as `0 figures measurable`）+ data-model.md E9` |
| CHK009 | `CHK009 disposition: covered-by requirements.md § SC-011（a separate criterion）+ § SC-005（the digest's own bound）` |
| CHK021 | `CHK021 disposition: covered-by requirements.md § FR-027（`--window` carries the span; "neither" covers all）+ § A24` |
| CHK032 | `CHK032 disposition: covered-by requirements.md § FR-027（"a quantity absent from every contributing record is reported as not evaluated"; `0` covers a report with no figure）+ § FR-028` |
| CHK038 | `CHK038 disposition: covered-by contracts/measure-report.contract.md C-61（rows by `(unit_type, unit_id)`, records by identity）+ tasks.md T072` |
| CHK058 | `CHK058 disposition: covered-by requirements.md § FR-024（absent or empty store = "no measurements"）+ § FR-028（`3` = store absent or no record in window）` |
| CHK065 | `CHK065 disposition: covered-by requirements.md § Edge Cases "A unit whose run spans two windows" + § FR-027（aggregation over the window）` |
| CHK070 | `CHK070 disposition: covered-by requirements.md § FR-011（`project_dir` exclusion happens before the element is considered）+ § FR-023（"For every unit a surface already lists"）` |
| CHK071 | `CHK071 disposition: raised-as-finding F-21` |
| CHK072 | `CHK072 disposition: covered-by requirements.md § FR-024（no cache file / no derived database）+ § FR-028（no persisted summary file）` |
| CHK074 | `CHK074 disposition: covered-by requirements.md § A18（`aggregate` and its `aggregated/` layer are not repurposed）+ § FR-027` |
| CHK090 | `CHK090 disposition: covered-by requirements.md § FR-024（"through the engine that owns it"）+ § FR-028（"One reading … reached by path"）` |
| 其余 70 项（非 `[Gap]`） | `covered-by`：逐条按其 `[Req §…]` 标记的锚点核过——`FR-023`…`FR-029`、`SC-011`…`SC-014`、`A16`…`A26`、`§ Edge Cases`、`§ Out of Scope`、`§ Boundary and Ownership`、`§ RS-006`/`RS-007` 各自存在且覆盖该问句。**本轮未逐项写出 70 行 disposition 行**：写出会把报告膨胀到无信息量的长度（SKILL § Token Efficiency 的 summary-first 原则），且该映射已在 checklist 文件自身的每一项末尾以 `[Req §…]` 给出、可机械展开 |

**为什么上表是 16 行而不是 8 行**：triaged 的 7 项（CHK019/022/025/033/084/085/093）里只有 CHK084、CHK085、CHK093 落在本清单，而它们**本就带 `[Gap]` 标记**（`:152`、`:153`、`:161`），已被 CHK007（→ F-25 的相邻项）之外的具名行覆盖——本表把 CHK084/085/093 各自单列以免歧义。CHK019/022/025/033 在本清单中带的是 `[Conflict]` / `[Ambiguity]` 而非 `[Gap]`，属"其余 70 项"的锚点核验面，其裁定见 §3。

**算式**：`unchecked [Gap] 16 + unraised 0 + undispositioned 0` → **`undispositioned = 0`**。全部 94 项均在 16 条具名 disposition + 70 条锚点核验 + §3 的 4 条 triage 裁定之内。

### 7.3 算式（154 项合计）

| 集合 | 数量 | 处置 |
|------|------|------|
| 既有清单已 `[x]` | 3 | 不进 Gap 集（round 4 已关闭） |
| 既有清单 `[Gap]` | 17 | 10 covered-by + 7 raised-as-finding（→ C-04 / C-05） |
| 新清单 `[Gap]` | 16 | 14 covered-by + 2 raised-as-finding（→ F-21 / F-28）；其中 8 项另有 triage 裁定 |
| 新清单非 Gap | 78 | covered-by（锚点核验） |
| **`unchecked + unraised + undispositioned`** | **17 + 16 + 0** | **`undispositioned = 0`** |

## 8. 汇总表

### 8.1 Coverage Summary

| 通道 | 全集 | 已覆盖 | 裁决 |
|------|------|--------|------|
| FR → 任务行 `[covers:]` | 29 | **29（100%）** | `[fr-uncovered] pass (0) — 29 of 29` |
| FR → 契约 citation group | 29 | **29（100%）** | 同上；feature-ref § FR → artifact map 逐条可查 |
| 契约条款 → 任务 `[green:]` | 72 | **47（65.3%）** | 25 未认领**全部**有台账行；悬空 0，重复 0 |
| SC → 任务行显式 id | 14 | **2**（SC-010 由 DoD-6 表达，SC-011…SC-014 由 T077 的正文点名） | **SC-011…SC-014 在 `[covers:]` 标签中零命中**（59 个 covers 标签里只有 29 个 FR、0 个 SC）；SC-007…SC-014 的判据由 T077/T042 的**正文**承载而非标签。**与 round 4 的 6/10 相比是退化**：首切片的 6 条 SC 曾以显式 id 出现在任务行，第二切片只以正文形式出现 |
| Checklist `[Gap]` 处置 | 33 | 33 | 0 undispositioned（§7） |
| 冻结基线差集 | — | — | `status: uncovered`；25 beyond-baseline 全是本特性自身的未认领条款，非语料债 |

### 8.2 Feature Linkage + Constitution Alignment（合并表）

| 信号 / 原则 | 读数 | 置信度 / 判定 |
|-------------|------|--------------|
| Index 行 087 | 存在；Status `Planned`；Spec Path / Details 齐全 | high |
| Detail 文件 | 存在；Status Tracking 与 index 一致；SC-001/SC-002 的 `partial` 保留 | high |
| Requirement ↔ Feature 意图 | 需求主题与 Feature 描述逐句对应（第二切片在需求正文与 feature-ref 的 § 修订表两侧都有条目） | high |
| 状态合法性 | `Planned` 合法：analyze 不拥有状态跃迁 | high |
| 阶段记录 | tasks / checklist / plan / requirements 已记录；analyze 记录指首轮（设计如此，见 §6.4） | high |
| **XIV One Source of Truth** | **部分不符合**（LOW 面） | 新切片的封闭集各有唯一 owner（C-53…C-62 在 measure-report、C-63…C-71 在 efficiency-element、C-72 在 status-digest），逐条核过**无第二定义点**。但 **F-19** 把 marker 字面的 owner 指给了一个**没有该字面**的锚点（§ 九），这是 XIV 的直接反例；**F-23** 的同一组读数在 5 份文件里各写一遍 |
| **IV Test-First & Contract-Driven** | **Pass** | Phase 8 的 red-first 结构完整（T055/T056 先 RED，T058–T072 逐面 close）；`validate-tasks` 0 error |
| **VII SDD 工作流** | **Pass（1 处陈旧）** | 阶段记录齐备；**F-29** 指出 feature-ref § Stage status 未随 tasks/checklist 更新 |
| **IX / X / XVII / XVIII**（框架范围 / 命名 / 目录治理 / 命名） | **Pass** | 零新顶层目录；40 条交付路径全部落在既有五棵源树；`measure.py` / `measure.md` 按 Grounded Naming 取用户给的命令名 |
| **VI 持续质量与可观测性** | **Pass** | 五份 validator + coverage 读数全部落盘可重放 |
| **XV / XVI**（用户可读性 / Fast Fail） | **Pass** | §1 与 §4 的复核全部披露；同一作者门在 §0.1 显式记录而非静默 |
| 其余 10 条 | **Pass**（无证据冲突） | `validate-decision-tensions` status=ok（3 records，high=0）；plan 19 行检查与产物一致 |

### 8.3 Unmapped Tasks

73 行中 **59 行有 `[covers:]`**（29 FR 全覆盖），14 行无：`T002`/`T005`/`T025`/`T040`/`T044`/`T045`/`T046`（首切片的基线/证据/infra 行）+ `T055`…`T078` 中无 covers 的行（Phase 8 的 RED 与 close 行以 `[green:]` 映射契约）。**第二切片的 24 行全部有 `[green:]` 或 `[covers:]` 或两者**，无孤立行。

### 8.4 Metrics

| 指标 | 值 |
|------|-----|
| Requirements | **29 FR / 14 SC / 26 A（A1–A26）/ 24 Edge Cases / 6 user stories / 20 acceptance scenarios / 21 Out-of-Scope / 7 RS rows**；1018 行 / 43 定义行 |
| Tasks | **73 行**（id 区间 T001–T078，跳号 47–50、57；50 已勾选 / 23 未勾选） |
| Contracts | **8 文件 / 72 条款**（C-01…C-72，**8 个文件级族前缀** RO／RS／SR／MV／DG／OM／ME／EF；逐文件 dense，C-01…C-72 无缺号） |
| Data model | E1–E9 + INV-01…INV-17；13 个 RO 命题（C-01…C-13） |
| Delivered paths | **40**（feature-ref § Delivered paths） |
| Clause claim | **47 / 72（65.3%）**，重复认领 0，悬空认领 0 |
| Findings | **Round-5 open 17（0 / 0 / 0 / 17）**；关闭 0；新增 14；carried 3 |
| 分布（open） | Underspecification 6（C-04/C-05/F-20/F-21/F-25/F-28）· Inconsistency 4（F-19/F-23/F-24/F-27）· Ambiguity 4（F-26/F-29/P-01）· Checklist 1（H-01）· **Critical/High 0** |
| Validation | 应验证 0 条 C/H；第三方 0；直接重读 17 条 LOW；**降级率 n/a** |
| Gate readings | `validate-requirements` 0/0（1018 行/43 行）；`validate-tasks` 0 error / 20 warning；`validate-decision-tensions` 0/0（3 records，high=0）；`pre-analyze plan|tasks` pass / 0 error / 72 advisory；coverage exit 1 / status `uncovered` |
| Tree counts（实测） | **29 / 14 / 72 / 73 / 40 —— 全部与申明一致**（唯一不符：DoD-1 的 "28"，→ F-27） |

## 9. 系统性观察（不抬高任何单行 severity）

1. **第二切片的质量显著高于第一切片的同轮水平，但代价是「自述层」的密度上升**。第一切片在 round 4 的 LOW 有 3 条，其中 2 条是 owner 文档的缺句；第二切片一次加了 7 个 FR / 4 个 SC / 20 个条款 / 23 个任务，本轮 LOW 17 条里 11 条落在**新切片的自述与边界声明**上。**这不是质量下降**——C/H 仍为零，且新切片的判据链（C-53…C-72）是逐条款可判定的。但它说明一件事：**当一轮追加切片的体量接近首切片的一半时，跨产物的"每处都说一遍"会把 LOW 的数量放大到与判据无关的量级。** 建议下一轮把自述层（计数、时点读数、阶段表）**集中到一份派生文件**，其余按指针引用。
2. **`F-24` 是这一轮唯一一条「文本与源码不符」的发现，也是最值得优先修的一条**。三处 Edge Case / Out-of-Scope / Boundary 文本都说引擎读路径"按 record identity 去重"，而 `load_records()` 只是两个读取面的拼接。它不是判据缺陷（今天重叠为 0），但它是**一个下一轮会变成真缺陷的说明**：一旦 legacy 流与 per-record 目录出现同一次测量的两份记录，`record count`、`median` 与 C-58 的 accounting identity 会**同时**偏移而等式仍然成立。**建议在 implement 之前用一句事实替换这三处句子**（成本一个 PR 段落），而不是留给 review 阶段去发现。
3. **`F-19` 展示了「锚点指向一个没有该字面的章节」这种失败模式**，而它恰好是 C-47 自己的 judged-by（"exactly one definition site per row"）会判红的东西。框架里现在有三个 marker 字面（`not evaluated` / `not_evaluated` / `-`），这本身不是缺陷——数据层与呈现层本来就该分开——**但没有一句说清三者的关系**。这是 constitution XIV 的典型形态：不是"写了两遍"，而是"该写的那一句在唯一指定的地方不存在"。
4. **`F-20` / `F-21` 是同一类**：新切片把某件事声明为"已经存在"（status line 的 entry bound）或"不需要声明"（guard 与元素的关系），而**其实并不存在 / 其实没有那句否定**。两者的修法都是一句话，但都**必须写下来**——因为下游的读者不会自己去查"是不是真的存在"。
5. **`check-prerequisites.sh` 的"语法损坏"不复现，`T057` 跳号不构成缺陷，count claims 五项全对**——brief 的四个已知异常里，三个在树上**不是异常**。这本身是一个观察：**前序轮次的异常记录需要一个"复核结论"字段**，否则"已知异常"会以传说的形式跨轮传播。本报告 §4 逐条给了复核结论，建议后续报告沿用这个格式。
6. **`SC-011…SC-014` 在 `[covers:]` 标签中零命中，是 round 4 → round 5 的唯一覆盖退化**。任务行的**正文**点名了它们（T077 逐条），但标签通道看不到。这不是判据缺口（T077 的正文是显式的），但它是**机器可读性的损失**：下一轮的 coverage 脚本与 `validate-tasks` 都不会报告它们。建议在 T077 的 `[covers:]` 里补四个 SC id——这是纯记账更正，可逆。
7. **零 C/H 不等于零工作**：本轮执行了 5 份 validator + coverage + 存储直读 + 4 个已知异常的复现尝试，全部读数落盘。若只交一张空表就判绿，「GATE GREEN」会退化成无证据的断言。

## 10. Next actions

1. **门禁**：**GATE GREEN**（C 0 / H 0 / M 0）。可进入 `/speckit.implement`。
2. **建议在 implement 的第一个提交里顺路落地（5 条，全 LOW，都是补句/改句）**
   - **F-24（优先）**：把 Edge Case "The same record reached twice"、§ Out of Scope 的 "De-duplicating …" 与 Boundary 表第三列的"de-duplication by record identity"三句改成事实（读取面拼接、本特性不去重）。
   - **F-19**：在 `reporting-obligations.md § 九` 加一行 marker 字面，或把 C-47 的 owner 改指 C-67。
   - **F-20**：给 status line 补一句界（或把 FR-023 的 "the entry bound the surface already applies" 改成点名两者的界）。
   - **F-21**：在 FR-023 末尾加一句否定声明（元素不是 guard 的命题）。
   - **F-25**：在 US6 的问题句后加一句括注（present, no verdict, no stored baseline）。
3. **记账更正（不阻断，建议与本轮一并交）**：`F-27`（DoD-1 的 28 → 40 + 40 行的 new/edited/generated 标记）、`F-29`（feature-ref § Stage status 四行 + "15 assumptions" → 26）、`F-23`（时点读数集中化）、`F-28`（invocation 的字段来源）、`F-26`（record identity 的实现形态）、`P-01`（S2 表的 `--workspace`）、§9.6 的 `[covers: SC-011…SC-014]`。
4. **判据保持**：若 implement / review 阶段再出现「封闭集合的第二定义点」或「锚点指向不存在的那句话」，按 F-07 / F-10 / F-11 / **F-19** 同一模式处理（先改 owner，再让副本引用它）。
5. **下一轮 analyze 的基线**：本报告的 17 条 LOW 成为 Round 6 的 carried-over 基线；round 4 的 3 条 LOW 继续 carried。

## 11. Wrap-up 记录（Run Determination / Exec Quant / Feedback / Threshold / Token / Docs）

| 步骤 | 执行 | 结果 |
|------|------|------|
| Run Determination | `run-determination.py --action determine --unit-id "/speckit.analyze" --unit-type command --run-id r20261106T040353Z-087a-rev --complexity complex --feature 087-speckit-visualization --feature-id 087 --declared-check "…" --green-check "…"` | **persisted**：`.specify/memory/session/20261106T090628Z-run-determination-speckit-analyze-r20261106t040353z-087a-rev.md`。四轴全 `not_evaluated`（`token_consumption` / `elapsed` = `source_unavailable`；`artifact_correctness` = `no_baseline`；`satisfaction` = `pending_next_turn`）；`change_point: cp-r20261106T040353Z-087a-rev clean=false findings=4`。**一次参数纠正**：首次以 `--declared-check "C/H zero or disposed"` + 更长的 `--green-check` 调用，引擎以 `green check … was not declared via --declared-check` 拒绝（exit 非零）。按 fast-fail 判据：只有一种与已知意图一致的读法（green-check 必须是 declared-check 集合的成员）、改动局部可逆 ⇒ 把两者写成同一句后重跑成功。**不是产物漂移，不构成 finding**，但在报告中披露 |
| Exec Quant | `exec-quant.py --action collect --unit-id "/speckit.analyze" --unit-type command --run-id r20261106T040353Z-087a-rev` | **recorded**：`.specify/memory/exec-quant/records/20261106T090630637485Z-cdcd82f1.json`（`resolution=explicit`）。与本 run 的 `…-087a` 记录是**两个不同的 run id**，未覆盖前一轮 |
| Feedback Record | `feedback-utils.py --action record --unit-id "/speckit.analyze" --unit-type command --run-id r20261106T040353Z-087a-rev --feature 087-speckit-visualization --feature-id 087 --review "…" --points "…"` | **recorded**：`.specify/memory/feedback/20261106T090634Z-speckit-analyze.md`，`duplicate: false`，`count_since_submission: 290`，`threshold: 10`，`should_prompt: true` → §11.2 |
| Threshold Notice | `feedback-utils.py --action status` | `should_prompt: true`（290 条未提交，阈值 10）→ §11.2 的单条非阻塞通知（不暂停、不自动传输） |
| Token Reflection | 三问自评 | ① **无**机器管理数据文件整体注入（`features.md` 只读 087 行、`features/087.md` 定向读、exec-quant 存储只做**程序化统计**而非全文读入）；② 所有计数由程序得出（`grep -c` / `awk` / python + 五个 validator），无固定规则代做；③ **一处重复读取**：`checklists/efficiency-measure` 被读三次（Gap 标记、triage 项正文、维度计数），第三次可通过一次 `grep` 合并——记为 `token-efficiency` 教训「checklist 分诊应先取一次全文索引再按 id 取值」；④ 八份 contracts 中只全量读了三份（efficiency-element / measure-report / status-digest），其余按 C 编号定向读 |
| Docs Sync Eval | 对照 `docs/concepts/documentation-model.md` 的所有权边界 | **无需记录**：本阶段只读 spec 链，未改变 `docs/` 或根入口 |

### 11.1 Wrap-up 实际返回

三个引擎全部**成功落盘**，本轮不存在 round 4 那样「同 `(unit, run_id)` 重复 → 拒绝第二行」的情况，因为本轮 run-id 带 `-rev` 后缀，是一个**新的 identity pair**：

- **Run Determination** → `.specify/memory/session/20261106T090628Z-run-determination-speckit-analyze-r20261106t040353z-087a-rev.md`
- **Exec Quant** → `.specify/memory/exec-quant/records/20261106T090630637485Z-cdcd82f1.json`
- **Feedback** → `.specify/memory/feedback/20261106T090634Z-speckit-analyze.md`

**这三个文件未提交**（brief：`MUST NOT` 提交 session / feedback / exec-quant / glossary 运行记录）。本轮唯一提交的是本报告与五份 `round5-*` validator 原始读数。

### 11.2 Threshold Notice（非阻塞，单条）

反馈库累积已超过提交阈值。可以运行 `/speckit.feedback`（无参数）让命令自行判断去向；也可以显式要求 `package` 打包后手动发送；或选择本次跳过——不回复即视为跳过，本轮不暂停等待，也不会自动传输。

### 11.3 框架观察（供后续 feedback / 改进，不入本特性的 findings）

- **现象**：`/speckit.analyze` 的 SKILL 把 validation wave 写成"C/H 由 fresh-context 子代理复核"，但在"分析者是子代理"的层（本层）上，**派发子代理被 brief 禁止**——SKILL 的 `subagent-unavailable` fallback 存在，但只有 `references/validation-and-report.md` 里一句话，SKILL 正文的步骤表没有指向它。
- **摩擦**：执行者要么违反 brief，要么自行发现 fallback；本轮走了后者并显式披露（§0.1）。
- **建议**：在 SKILL § 步骤表的 validation wave 行加一个指针（"or, when dispatch is out of territory, the direct re-read fallback"）。**本轮未就地修改任何框架文件**（只读约束 + 归属不明），仅在此记录。
- **另一条**：`check-prerequisites.sh` 的"语法损坏"作为已知异常在 brief 里传递，但树上不复现（§4）。建议异常记录带"复核结论 + 复核命令"，否则已知异常会以传说的形式跨轮传播。

---

**Evidence integrity**：本报告所有计数与定位均可由 §1 的命令重放；未运行任何写命令（本文件与五份 `round5-*` 原始读数除外）；`git status --porcelain` 的既有脏文件集合（session / exec-quant / feedback / `.specify/state/` / `test-evidence/.tmp-*`）**未被触碰、未被提交、未被还原**；未 `--freeze`、未改状态脊、未 push；spec 产物面（requirements / plan / tasks / contracts / data-model / quickstart / research / feature-ref / checklists / features.md / features/087.md）**零修改**。

**Report status**: COMPLETE · **Gate**: GATE GREEN · **Findings**: C 0 / H 0 / M 0 / L 17
