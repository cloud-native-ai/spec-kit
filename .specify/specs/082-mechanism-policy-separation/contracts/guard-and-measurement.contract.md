# Contract — 守护测试与测量契约（Guard & Measurement）

**Status**: designed（本阶段）；`/speckit.implement` 按本契约先写测试、再改元技能（Constitution IV）。

**边界**：本契约**不引入**新的确定性门禁脚本（C8 / FR-016）。它定义的是**既有 pytest 契约测试**与**既有命令**的组合，用来让 SC-001…SC-009 可复算。任何新增脚本的提议必须先在 `plan.md` § Design Decisions D2 / § D11 里推翻「零新脚本」的结论。

**两段结构（scope update，2026-11-05）**：GM-01…GM-09 是机制/策略侧（SC-001…SC-005），原文未改一行；GM-10…GM-14 是技能引用侧（SC-006…SC-009），按 `plan.md` § Measurement Plan 追加。两侧共用同一条纪律：可判定的形态进 pytest，不可判定的语义落 `test-evidence/` 的样本记录（GM-02）。**编号不重排**——重排会让已提交的 `skill-wiring.contract.md` / `data-model.md` 的交叉引用静默指错。

## GM-01 — 契约测试清单（六个模块，全部在 `tests/contract/`）

| 模块 | 守护对象 | 主要断言 |
|---|---|---|
| `test_mechanism_policy_owner_doc.py` | owner 文档形态 | OD-01…OD-10 每条至少一条断言；文档存在且 `.specify/` 镜像逐字节一致 |
| `test_mechanism_policy_ownership.py` | 一源与边界 | owner 之外零复制（GM-03）；边界表六个相邻 owner 的规则字面不在本文出现；`dogfooding-definitions.md` § 1 未被改写 |
| `test_mechanism_policy_skill_wiring.py` | 元技能接线 | SW-01…SW-03 的判定行在正确位置存在、每面只一条、含 owner 路径引用；`create-skills` 引用文档存在且有判定步骤 |
| `test_mechanism_policy_guard.py` | SC-003 逐字节封闭集 | GM-04 的四条要件全部可判 |
| `test_mechanism_policy_missing_policy.py` | SC-004 | GM-05 的零写入与逐字节一致 |
| `test_mechanism_policy_decidability.py` | SC-001 / SC-005 分母 | owner § Worked Examples 题集可解析、每条有标准答案与依据、依据只引 OD-02 判据 |

**红先行形态**：六个模块在元技能与 owner 文档落地前 MUST 以「artifact missing」红，MUST NOT 以 import error 或 collection error 红（既有 `tests/contract/test_bilingual_expression.py` 的同一约定）。

## GM-02 — 判定的**写出**与**判定**分离

- 契约测试的职责是把**形态**变成可判事实（章节存在、字面存在/不存在、字节相等、题集可解析）；**语义**判定（这条内容归哪一层）由 SC-001 的双判定者与 SC-002 的流程实录承担。
- 任何断言 MUST NOT 试图用正则判定「这段文字是机制还是策略」——那是判据本身，正则化会变成一个不可靠的第二判据点。

## GM-03 — SC-003 封闭集声明（`closed-set-claims.md` 五要件）

`SC-003` 是一条包含性声明（「成员表之外 … 逐字节未变」），按 `.specify/shared/guidelines/closed-set-claims.md` 逐要件落成：

| # | 要件 | 本特性的取值 | 断言形态 |
|---|---|---|---|
| 1 | 基线参照物 | [[STR-002]] = `3ffeb26e`（实现起点提交，`aaee504c` 的祖先；本仓 `base_sha`） | 测试读取 `git ls-tree -r 3ffeb26e -- skills/ templates/commands/`，MUST NOT 从变量读一个「当前」「最新」 |
| 2 | 比较单元 | **按产物类**两族：`skills/`（技能资产：`SKILL.md` + `references/` + `scripts/` + `assets/`）与 `templates/commands/`（命令模板） | 单元 = 框架**源**路径；`.specify/` 是生成镜像，由 `sync-mirrors.py --check` 单独判（GM-06） |
| 3 | 允许差异集来源 | **一条封闭登记表，路径的唯一落点是 `data-model.md` § GM-03 允许差异集**（比较单元内 **10** 条：**1 条新增 + 7 条特性改写 + 2 条吸收的 coaching skill-reference 文件** = 该节第 1–8 行 + 第 19–20 行；单元外 **10** 条为本实现期新增测试模块与矩阵 fixture = 该节第 9–18 行），并由 owner 成员表交叉核对（`included` 恰 3）；MUST NOT 使用「其余 / 叶子 / 未受影响」一类聚合词，也 MUST NOT 在本文件再抄一份路径清单 | 守卫断言：成员表 `included` 集合 == 允许差异集的流程子集；差集为空 |
| 4 | 补集断言 + 结构不变量 | 补集 = 基线路径集 − 允许差异路径集 − 新增路径；断言为（a）补集内**每个**路径在 HEAD 的内容与基线逐字节相等（`git cat-file blob <base>:<path>` vs 工作树读取），（b）路径集相等（`git diff --name-status 3ffeb26e..HEAD -- skills/ templates/commands/` 的行只落在允许集内） | 两侧都在：字节侧与路径集侧 |
| 5 | 未定义聚合词清零 | 本契约与 `data-model.md` MUST NOT 出现「其余 / 其它 / 未受影响 / untouched / everything else」作为比较范围的表述 | 契约测试扫这两个文件 |

**允许差异集**：封闭的 20 条路径登记在 `data-model.md` § GM-03 允许差异集（单一路径落点，本文件不手抄任何与表不符的总数）；其中比较单元内的第 1–8 行 + 第 19–20 行 = 1 条新增（`create-skills` 的 `references/mechanism-policy-check.md`）+ 7 条改写（五个消费方的 `SKILL.md`：`create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` / `run-skills`，加 `improve-skills` 与 `merge-skills` 各一份 `references/`）+ 2 条吸收的 coaching skill-reference 文件；比较单元之外的第 9–18 行 = 10 条，全部落在 `tests/`（1 份矩阵 fixture、1 个 test-only 辅助、8 个 pytest 模块，其中第 18 行登记 4 个一组的引用侧模块）。条数以该节表格的行为准。本文件 MUST NOT 重复这份路径清单（One Source of Truth）。**本轮变更（SU-01）**：要件 3 的原值「单元内 6 条」写于「`coaching-skills` / `run-skills` 零改动」仍成立时，该前提被 FR-026 证伪，故按 `data-model.md` 的实测登记值改为 8；本轮吸收（用户裁定 2026-11-05，CL-04）再 +2 条 coaching skill-reference 文件，比较单元内共 **10** 条。

## GM-04 — SC-003 的**比较单元规模**（实测，非预设）

本阶段实测（`test-evidence/plan2026-11-05-baseline.txt`）：基线 `3ffeb26e` 的 `skills/` + `templates/commands/` 共 **575** 个文件（`skills/` 548 + `templates/commands/` 27），`.pyc` 不计；工作树同区 `git status --porcelain` 为空，即当前零差异。**scope update 复核（2026-11-05）**：`compared=575` 与 `complement=570 / allowed_in_unit=5 / frozen_mismatches=0` 在本轮复跑中不变（`plan.md` § Post-Generation Quality Gate 的 S4 行）；`allowed_in_unit` 的上限随允许差异集在比较单元内的行数而变（见 GM-03 要件 3：该节的第 1–8 行，条数以表为准），但**比较单元规模 575 不动**——它只由基线路径集决定。

- 断言 MUST 报告被比较的文件数（575 形态），MUST NOT 只报告「无差异」——一个比较了 0 个文件的守卫会永远绿（Constitution XVI 的「绿是声明不是证据」）。
- 守卫 MUST 自带反向用例：在 `tmp_path` 造一个「补集内文件被改一个字节」的假工作树，断言守卫转红（GM-07）。

## GM-05 — SC-004：零写入 + 补齐后逐字节一致

两个可执行面，选其一为**主面**，另一个为**支撑面**，两者都要有记录：

- **主面（确定性，入测试）**：`tests/contract/test_mechanism_policy_missing_policy.py` 用 `tmp_path` 造一个假的技能目录与运行目录，运行 owner § Consumption Contract 的检查（以**文本契约**为被检对象：断言 owner 的检查三步在文本上就是「读-判-停」且不含任何写动作），并断言：缺策略路径下 `tmp_path` 快照前后**逐文件**相等（含 mtime 之外的内容哈希与目录集合）；补齐策略路径下产物哈希等于基线产物哈希。
- **支撑面（执行面，入证据）**：一个受支持 agent 宿主上一次真实流程（SW-04 接线之后的 `create-skills`）的实录：缺策略 → 输出提示、零文件写入；补齐 → 产物与改动前同一输入逐字节一致。证据落 `test-evidence/sc-004-*.txt`，含宿主名 + 版本。
- **前提**：主面之所以可以入测试，是因为它判的是 **owner 契约文本 + 文件系统快照**，不判 AI 行为；支撑面才判行为，因此它是证据而非测试（与 A6「不预设脚本」一致）。
- **SC-004 的「补齐后逐字节一致」分母**：同一输入 = 同一技能草稿 + 同一策略值；断言对象 = 产物集合的路径集 + 每个文件的 sha256。

## GM-06 — 镜像与命令副本

- `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` MUST 在本特性关闭时仍 exit 0（基线实测二者均 exit 0 / 零漂移，见 `test-evidence/plan2026-11-05-baseline.txt`）。
- `.specify/` 与 `.claude/`、`.github/`、`.qoder/`、`.opencode/` 侧**不是** SC-003 的比较单元：镜像不一致归 `sync-mirrors.py --check`，第二定义点归 GM-03（两条规则不互相遮蔽，见 `plan.md` § Design Decisions D8）。

## GM-07 — 守卫的判别力（反例断言）

- 每个新增契约测试模块 MUST 至少有一条反例断言：把被检查的形态破坏一个字符/一行，断言模块转红。落法：在同一模块内以 `tmp_path` 复制被检文件、注入破坏、调用同一断言函数（不运行 pytest 子进程）。
- 反例 MUST NOT 靠「注释掉测试」或 `skip` 达成；MUST NOT 引入 `pytest.mark.xfail` 来「表示」判别力。

## GM-08 — 定向测试集与基线差集（TEST BUDGET）

- 本阶段的定向集 = 10 个受本特性改动的路径的直接影响模块，**实测基线** 892 passed / 0 failed，模块清单与命令逐字落在 `test-evidence/plan2026-11-05-baseline.txt`。
- 实现期 MUST 以同一清单 + 六个新模块运行，判据是**差集**：`实现后失败集 − 基线失败集` 为空，且六个新模块全绿；MUST NOT 使用绝对「全部通过」判据（`tests/contract/test_expression_compatibility.py` 等模块含与本特性无关的冻结哈希，其红绿须逐条归因）。
- 全量套件在 implement 起点做一次 E2 基线；本特性实现期只消费定向集（TEST BUDGET 明令）。

## GM-09 — SC-002 的执行载体与记录

- 载体：一个**受支持 agent 宿主**（`docs/reference/cli/supported-agent-tools.md` 的 roster），对同一技能草稿在**改动前 / 改动后**各跑一次纳入的元技能流程。
- 样本：误置样本 2 个（策略误置：正文含一个绝对路径；机制误置：一段判定规则住在用户目录说明里）、正确分层样本 2 个。
- 判据：改动后 2/2 误置被点名（含文件与位置），2/2 正确样本零误报；改动前同流程对正确样本同样零误报（基线）。
- 记录 MUST 含：宿主名 + 版本原文、两次运行的输入草稿路径、输出原文、逐样本 verdict 表。

## GM-10 — 技能引用侧的测量纪律（SC-006…SC-009 的共同前提）

第二段（技能引用归一化）的四条 SC 有一条与第一段不同的性质：它们**全部可判**——不需要模型判断「这段内容归哪一层」，只需要一台机器对给定输入复算归一化结果。因此本段的纪律是把 GM-01…GM-02 的分配原则按同一判据落到引用侧：

| # | 纪律 | 落点 |
|---|---|---|
| 1 | 可判定的形态与结果 MUST 进 pytest，MUST NOT 落成 `test-evidence/` 的人工记录 | GM-11 的五个 pytest 模块（+ 一个 test-only 辅助 `skill_reference_matrix.py`） |
| 2 | 唯一可执行实现是 `tests/contract/skill_reference_matrix.py`（stdlib-only 纯函数），MUST NOT 在元技能运行时被调用；执行期归一化仍按 owner 正文现场进行（D11） | GR-03 / plan.md § D11 |
| 3 | 期望值的唯一来源是 `tests/fixtures/skill-reference/normalization-matrix.json`；MUST NOT 在测试里内联第二份期望表 | GM-13 |
| 4 | 「owner 正文所规定的过程可被机器逐行复现」与「每个宿主执行体确实照做」是两条不同断言，前者由矩阵复算证明，后者只有 SC-002 式的宿主实录能证明 | plan.md § Measurement Plan 的「测试 vs 运行」缺口段 |
| 5 | 本段 MUST NOT 新增确定性门禁脚本（C8 / FR-016）；任何新增提议须先推翻 D2 / D11 | 本契约边界段 |

- **为何不需要宿主实录**：本段的判定对象是字符串变换，不是语义归类；矩阵复算与现场执行使用同一份 owner 正文规则，故复算成立即等价于过程成立（GM-02 同一判据的反面用法）。
- **编号封闭**：GM-10…GM-14 五条覆盖本段全部测量面；新增第六条须先改 `plan.md` § Measurement Plan，MUST NOT 就地追加。

## GM-11 — 技能引用侧的契约测试清单（五个模块 + 一个测试辅助）

全部在 `tests/contract/`；五个 pytest 模块共同承载 SC-006…SC-009 的可判部分（辅助文件不带断言），并兑现 GM-07 的「每个模块至少一条反例断言」。

| 模块 | 守护对象 | 主要断言 | SC |
|---|---|---|---|
| `skill_reference_matrix.py` | 归一化的**唯一可执行实现**（stdlib-only 纯函数，**不是** pytest 模块，被其余五个 import；D11） | 输入 = (原始串, 形态) → 输出 = 三值之一 + 归一化标识 + 成对报告字段；模块顶层 MUST NOT 有断言或 I/O | — |
| `test_skill_reference_grammar.py` | owner 章节形态（GR-01…GR-06 / GR-08 的文本面） | 头部所有权两列表齐备；`§ Accepted forms` 六行与 `data-model.md` E-8 字面相等；`§ Normalization` 步集与 NP-1…NP-8 一一对应且 NP-3/NP-4 先于 NP-6；输出恰三值；两轮大小写匹配与多命中关闭 | SC-006 形态前置 |
| `test_skill_reference_matrix.py` | SC-006 矩阵复算 | 逐行比对 `expect` 的判定类与「原始 + 归一化」成对形态；**分母 = fixture 行数（≥ 12）**，任一行不匹配即失败（GM-13） | SC-006 |
| `test_skill_reference_consumers.py` | SC-007 五消费方接线 + 包含性扫描 | 每份 `SKILL.md` **恰一条**指向 [[STR-004]] 源路径的引用；`.specify/shared/definitions/` 前缀串零命中；全仓扫描除 owner 外零份复制（GM-12 五要件） | SC-007 |
| `test_skill_reference_command_surface.py` | SC-008 命令面消歧 | 正例 ≥ 2 行（`speckit.skills` / `/speckit.skills`）判定 `command-surface` 且指向命令模板；**负例 ≥ 1 行**（与命令同形但不是命令的名字）证明判定不是「带点/带斜杠一律当命令」 | SC-008 |
| `test_skill_reference_failures.py` | SC-009 失败语义 | 四类失败各一条断言；每条同时断言报告含原始与归一化标识；四类 `failure_class` **互斥**（越界不得报成零命中） | SC-009 |

- **红先行形态**：五个 pytest 模块在 owner 定稿与五份接线落地前 MUST 以「artifact missing」红，MUST NOT 以 import error 或 collection error 红（与 GM-01 同一约定）。
- **模块集封闭**：五个 pytest 模块 + 一个测试辅助，任何第六个 pytest 模块或第七个辅助文件都必须先推翻 `plan.md` § D11。
- **反例落法**：每个模块在 `tmp_path` 内**字符串级**注入破坏（把归一化步骤换序、删一行接受形式、把一个 `expect` 改一值、把一条源路径引用改回镜像路径）并复用同一断言函数；MUST NOT 用 `skip` / `xfail` / 注释掉测试来「表示」判别力（GM-07 原文）。

## GM-12 — SC-007 包含性扫描的五要件

SC-007 的第二半（「除 owner 以外零份」）是一条包含性声明，按 `.specify/shared/guidelines/closed-set-claims.md` 逐要件落成：

| # | 要件 | 本特性的取值 | 断言形态 |
|---|---|---|---|
| 1 | 基线参照物 | [[STR-002]] = `3ffeb26e`（与 GM-03 同一个，MUST NOT 另钉第二个基线） | 扫描器对「基线存在性」只用于定位历史命中，不用于断言当前内容；当前内容由文件读取 |
| 2 | 比较单元 | `skills/**/SKILL.md`（框架源树；镜像层 `.specify/skills/**` **不计入**分母，由 `sync-mirrors.py --check` 另证一致） | 分母 MUST 被报出（`scanned=<N> skills/**`），MUST NOT 只报「零命中」 |
| 3 | 允许差异集来源 | **三类且仅三类**（`requirements.md` § SC-007 Source；此「三类」是**允许差异集的来源分类**，与失败类数无关，见下表后的口径声明）：① owner 自身 `shared/definitions/skill-reference-definitions.md`；② owner 的生成镜像 `.specify/shared/definitions/skill-reference-definitions.md`；③ 既有测试里以字面量钉住的 fixture 行（`tests/fixtures/skill-reference/`）。差异集**不是**本契约的私有清单，MUST NOT 在此再抄一份路径 | 扫描器把三类写成具名常量并在报告里逐类打印计数 |
| 4 | 补集断言 + 结构不变量 | 补集 = 比较单元 − 允许差异集；断言为「补集内零命中归一化步骤字面，且零命中 `requirements.md` FR-024 的**四类失败名**」——失败类的唯一 owner 是 FR-024，本契约不另立第三类或第四类的说法（裁定见 `plan.md` § Clarifications 的 CL-01）。结构不变量：五份消费方各**恰一条** owner 源路径引用（SR-01…SR-06）。**断言字面形态（M-06 的规范形态）**：四个失败名以**反引号代码跨**形态逐字取自 FR-024 的括注原文，扫描时**忽略代码跨定界符本身**（即 `\`零命中\`` 与 `零命中` 视为同一命中，不得因反引号差异而漏计），以及首尾空白与全角/半角标点；MUST NOT 只凭「三字」或正则片段匹配 | 两侧都在：命中计数 + 每份接线条数 |
| 5 | 未定义聚合词清零 | 本契约与 `data-model.md` / `contracts/skill-reference.contract.md` MUST NOT 出现「其余 / 其它 / 未受影响 / untouched / everything else」作为**比较范围**的表述 | 契约测试扫这三份文件 |

- **失败类数的口径声明（CL-01）**：本表要件 3 的「三类」**只**指允许差异集的来源分类；失败类的数量与名字**只**由 `requirements.md` FR-024 给出（四类：零命中 / 路径越界 / 目录无 `SKILL.md` 或 frontmatter 无效 / 两层不同命中），并由 `SC-009` 逐类断言。本契约与 `data-model.md` 的 E-10 不得出现「三类失败」一类表述。
- 扫描 MUST 报出**命中路径与行号**（SC-007 的原文要求）；只报总数 = 不可定位的结论。
- 扫描 MUST NOT 把「镜像层」算成第二个命中：dev 规范层与其安装镜像的同名命中是一处（GR-05(c) 的同一判据）。

## GM-13 — SC-006 的矩阵复算与分母

- 矩阵 fixture 的唯一落点是 `tests/fixtures/skill-reference/normalization-matrix.json`（`data-model.md` § GM-03 第 9 行的同一路径；本契约 MUST NOT 再抄一份路径清单）。
- **分母 = fixture 行数**，下限 ≥ 12（SC-006 原文）；起点 = clarify 的 14 行探针（`test-evidence/clarify-scope-update-fixture.json`），扩展覆盖六种接受形式、大小写变体、包裹引号、`/` 与 `@` 前缀变形、`SKILL.md` 路径、目录路径、零命中、路径越界、两层不同命中。
- 运行 MUST 打印 `rows=N matched=N failed=0` 形态的计数；**任一行不匹配即失败**，MUST NOT 以「其余项通过」结案（SC-006 末句）。
- 每行 MUST 同时携带 `raw` 与 `expect.normalized`（成对），并有 `expect.outcome` ∈ {`command-surface`, `skill`, `failure`}；`failure` 行 MUST 携带 `failure_class` ∈ E-10 的四值。
- 矩阵 MUST 按 `surface` / `normalize` / `failure` 三段组织（SC-008 与 SC-009 各自读自己的子段），分段 MUST NOT 让某行同时属于两段。
- 复算方式 = 同一 fixture + 同一 `skill_reference_matrix.py` 重跑，逐项结果相等。

## GM-14 — 镜像、命令副本与被改技能的收口计数

- 引用侧的镜像面由 `sync-mirrors.py` 覆盖：owner 镜像 + 五份 `SKILL.md` 镜像一起再生成，`--check` MUST exit 0（基线实测六对全 `ok`；本轮 `shared/` 由 62 → 63，`plan.md` § Mirror Obligations）。MUST NOT 把任何文件计数钉进断言。
- `regen-command-copies.py --check` MUST exit 0 且命令副本**零变化**：这是 SW-06 / FR-011 的机械证据，也是 SC-008 的标杆（`/speckit.skills` 仍是命令面）不受本特性影响的事实依据。
- **「测试 vs 运行」缺口（显式披露，MUST NOT 留白）**：`skill_reference_matrix.py` 是**测试侧**的可执行实现；元技能执行时仍按 owner 正文**现场**归一化。因此 SC-006…SC-009 证明的是「owner 正文所规定的过程可以被一台机器逐行复现且结果一致」，**不**证明每个宿主执行体真的照做了。第二个能力**没有**被排进宿主实录（GM-09）的测量面——它不需要模型判断。若将来要把引用侧纳入宿主实录，那是一次新的测量面决策，MUST NOT 由本契约默许。
- **被改技能的体积计数**沿用 GM-01 / EP-003 的同一条形态：每个被改 `SKILL.md` 记录 `skill-shape.py` 的 before / after `est_tokens_controllable` 与 delta；`references/` 文件不计（它们不在 5000 预算的判据面内）。

## 引用侧与机制/策略侧的合流点

- 两份允许差异集**共用一张表**（`data-model.md` § GM-03），MUST NOT 出现「按能力各开一张」的第二份（SC-003 的分母唯一）。
- `coaching-skills` / `run-skills` 在 GM-03 的逐字节断言里**失效**（它们被引用接线改写）；补偿判据是**同一个模块**里的两条断言各占一半：`tests/contract/test_skill_reference_consumers.py`（tasks T027）既持 SW-05 的行形态/字面零命中断言，也持 GM-12 的接线条数断言。**owner 唯一性**：该文件的持有点由 tasks T027 与 GATE-6 钉定，`test_mechanism_policy_guard.py`（tasks T020）**不**断言 `coaching-skills` / `run-skills` 的引用侧零命中（它只断言机制/策略判定字面与 GM-03 的流程子集），两处 MUST NOT 互相重复或互相推诿。
- 两侧的测试模块都落在 `tests/contract/`，`tests/` **不在**比较单元内，故模块数量的增长不影响 SC-003 的分母（`data-model.md` § GM-03 第 10–18 行登记为「否」）。

## 可追溯性

| FR / SC | 条款 |
|---|---|
| FR-011 | GM-03（允许差异集封闭）、GM-06、GM-14 |
| FR-015 | GM-03（要件 5）、GM-01（`test_mechanism_policy_ownership.py`）、GM-12（要件 5） |
| FR-016 | GM-01（零新脚本）、GM-03（不新增第二套分类文件）、GM-11（模块集封闭） |
| FR-019 | GM-11（`test_skill_reference_grammar.py` 的 owner 章节断言）+ `contracts/skill-reference.contract.md` GR-01 |
| FR-021 | GM-13（确定性顺序的矩阵复算） |
| FR-025 | GM-11 / GM-13（成对形态是矩阵每行的必填字段） |
| FR-026 | GM-12（要件 2 / 4）、GM-11（`test_skill_reference_consumers.py`） |
| FR-028 | GM-14（镜像再生成 + `--check`） |
| FR-029 | GM-11（模块集封闭）、GM-14（命令副本零变化） |
| FR-030 | GM-13（三值封闭 + 四类失败互斥） |
| SC-001 | GM-01（`test_mechanism_policy_decidability.py`）+ `test-evidence/sc-001-*.txt` |
| SC-002 | GM-09 |
| SC-003 | GM-03, GM-04, GM-07 |
| SC-004 | GM-05, GM-07 |
| SC-005 | GM-01 + `test-evidence/sc-005-*.txt` |
| SC-006 | GM-11, GM-13 |
| SC-007 | GM-11, GM-12 |
| SC-008 | GM-11（正负例成对） |
| SC-009 | GM-11（`test_skill_reference_failures.py`）、GM-13（`failure` 子段） |
