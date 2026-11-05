# Contract — 守护测试与测量契约（Guard & Measurement）

**Status**: designed（本阶段）；`/speckit.implement` 按本契约先写测试、再改元技能（Constitution IV）。

**边界**：本契约**不引入**新的确定性门禁脚本（C8 / FR-016）。它定义的是**既有 pytest 契约测试**与**既有命令**的组合，用来让 SC-001…SC-005 可复算。任何新增脚本的提议必须先在 `plan.md` § Design Decisions D2 里推翻「零新脚本」的结论。

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
| 3 | 允许差异集来源 | **一条封闭登记表，路径的唯一落点是 `data-model.md` § GM-03 允许差异集**（比较单元内 6 条：2 新增 + 4 改写；单元外 6 条为本实现期新增测试模块），并由 owner 成员表交叉核对（`included` 恰 3）；MUST NOT 使用「其余 / 叶子 / 未受影响」一类聚合词，也 MUST NOT 在本文件再抄一份路径清单 | 守卫断言：成员表 `included` 集合 == 允许差异集的流程子集；差集为空 |
| 4 | 补集断言 + 结构不变量 | 补集 = 基线路径集 − 允许差异路径集 − 新增路径；断言为（a）补集内**每个**路径在 HEAD 的内容与基线逐字节相等（`git cat-file blob <base>:<path>` vs 工作树读取），（b）路径集相等（`git diff --name-status 3ffeb26e..HEAD -- skills/ templates/commands/` 的行只落在允许集内） | 两侧都在：字节侧与路径集侧 |
| 5 | 未定义聚合词清零 | 本契约与 `data-model.md` MUST NOT 出现「其余 / 其它 / 未受影响 / untouched / everything else」作为比较范围的表述 | 契约测试扫这两个文件 |

**允许差异集**：封闭的 12 条路径登记在 `data-model.md` § GM-03 允许差异集（单一路径落点）；其中落在比较单元内的 6 条 = `create-skills` 一条新增引用文档、三个纳入元技能的 `SKILL.md` 改写、`improve-skills` 与 `merge-skills` 各一份 `references/` 改写。本文件 MUST NOT 重复这份路径清单（One Source of Truth）。

## GM-04 — SC-003 的**比较单元规模**（实测，非预设）

本阶段实测（`test-evidence/plan2026-11-05-baseline.txt`）：基线 `3ffeb26e` 的 `skills/` + `templates/commands/` 共 **575** 个文件（`skills/` 548 + `templates/commands/` 27），`.pyc` 不计；工作树同区 `git status --porcelain` 为空，即当前零差异。

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

## 可追溯性

| FR / SC | 条款 |
|---|---|
| FR-011 | GM-03（允许差异集封闭）、GM-06 |
| FR-015 | GM-03（要件 5）、GM-01（`test_mechanism_policy_ownership.py`） |
| FR-016 | GM-01（零新脚本）、GM-03（不新增第二套分类文件） |
| SC-001 | GM-01（`test_mechanism_policy_decidability.py`）+ `test-evidence/sc-001-*.txt` |
| SC-002 | GM-09 |
| SC-003 | GM-03, GM-04, GM-07 |
| SC-004 | GM-05, GM-07 |
| SC-005 | GM-01 + `test-evidence/sc-005-*.txt` |
