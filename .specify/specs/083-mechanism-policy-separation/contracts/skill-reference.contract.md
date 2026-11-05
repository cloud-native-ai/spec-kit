# Contract — 技能引用 owner 文档与五消费方接线（Skill Reference）

**Status**: designed（本阶段）；由 `/speckit.implement` 落地
**产物**:
- `shared/definitions/skill-reference-definitions.md`（框架源；[[STR-004]] 是它的唯一 owner 路径）→ 镜像 `.specify/shared/definitions/skill-reference-definitions.md`（`sync-mirrors.py` 生成，MUST NOT 手改）
- 五个消费方的 `SKILL.md` 各一段接线（SR-01…SR-06）

**判据 owner**: [[STR-004]]。本契约是**形态契约**：owner 文档必须具备哪些章节与值域（GR-01…GR-10），五个消费方各自必须声明什么、MUST NOT 声明什么（SR-01…SR-06）。本契约不拥有任何接受形式、归一化顺序或失败语义——那些事实全在 owner 正文，本契约只断言它们存在、闭合且可复算（FR-019 / C9 / FR-015）。

**与相邻契约的分界**：机制/策略侧的 owner 形态归 `contracts/owner-document.contract.md`（OD-01…OD-10），其接线归 `contracts/skill-wiring.contract.md`（SW-01…SW-08）；本契约的 SR 组只陈述**技能引用侧**的接线，SW-05 只陈述机制/策略侧的收紧形态，两者 MUST NOT 互相替代（C9 的同一句）。测量与测试载体归 `contracts/guard-and-measurement.contract.md`（GM-11…GM-14）。

## 共用形态（全部 GR 条款的前提）

- owner 文档 MUST 在前 **12 行**内声明它**拥有什么**（接受形式、归一化顺序、消歧规则、失败语义）与**不拥有什么**（位置阶梯 → `skills/internal/run-skills/SKILL.md` § 1；镜像生成 → `scripts/python/sync-mirrors.py`）（FR-019）。
- owner 文档 MUST 含字面 `single source of truth` 与 `MUST NOT`，并写明「消费方以路径引用，MUST NOT 复制接受形式清单、归一化顺序或失败语义表」（FR-015 / FR-026）。
- 两份 owner 互不复制：本文 MUST NOT 出现机制/策略侧的判据表、症状表、提示骨架或成员表（C9）。

## GR-01 — 头部所有权声明

- 前 12 行 MUST 逐项点名**四个**由本文拥有的事实组，且每组在正文有一个落点章节：① 接受形式集合；② 归一化顺序与输出形态；③ 消歧规则；④ 失败语义。
- 前 12 行 MUST 逐条点名**两个**不由本文拥有的事实并给出 owner 路径：「按名称解析时哪个位置优先」→ `skills/internal/run-skills/SKILL.md` § 1 的位置阶梯（FR-022）；「镜像怎么生成」→ `scripts/python/sync-mirrors.py`（FR-028）。
- 声明了却无落点章节 = 悬空所有权声明（判红）。

## GR-02 — § Accepted forms：封闭接受形式集合

- 六个形式 MUST 各占一行，形态固定为 `| form | 示例 | 含义 |`，行集与 `data-model.md` E-8 的六行**字面相等**（bare name / slash reference / at reference / labelled reference / canonical path / directory path）（FR-020）。
- 每个示例 MUST 是一个**可被归一化接受**的字符串；`labelled reference` 的标签 MUST 逐字为 [[STR-005]]。
- form 集合 MUST 声明为**封闭**：新增一个形式是一次对本文的修订，MUST NOT 由某个消费方就地扩展（FR-020 末句 / FR-029）。
- 每个示例 MUST 在 SC-006 的矩阵 fixture 里有一行期望输出（GR-06 的要件）。

## GR-03 — § Normalization：确定性顺序与输出形态

- 顺序 MUST 写成**编号步骤**，步集与 `data-model.md` § E-9 的 NP-1…NP-8 一一对应；步骤之间的关系 MUST 是**不可交换**的偏序，尤其 NP-3 / NP-4（剥标签与前缀）MUST 先于 NP-6（通道判定）。
- 归一化 MUST 是**确定性**的：同一输入同一输出，MUST NOT 依赖上下文的偶然状态，MUST NOT 访问网络，MUST NOT 要求交互（FR-021）。
- 输出形态 MUST 规定为「名称」或「路径 + 层级」，且 MUST 明写**不含被剥掉的前缀或后缀**（前缀与后缀在识别之后丢弃，不留给下游再猜）（FR-021）。
- 交互报告形态 MUST **成对**：原始标识 + 归一化后的标识 + **判定类**（三值之一）三者同时出现；只报命名不报判定类 = SC-006 无法逐项复算（FR-025）。
- 大小写 MUST 写成两轮：先精确匹配，**仅当零命中**才做一次不分大小写的比较；不分大小写命中多于一个时按 `dual-layer` 失败关闭（不得任选其一）。
- 形态判定（cli / invocation）MUST 是**显式步骤**（NP-1），不是散落在各消费方正文里的一句说明（C11）。

## GR-04 — 三值输出与通道判定

- 输出 MUST 恰为三值之一且值域封闭：`command-surface` / `skill` / `failure`（FR-030）。任何「原样返回、下游再猜」「保留原值」类结果 MUST NOT 成为第四值。
- 通道判定 MUST 由**单一判据**决定：剥完之后**余值是否含 `/`**（`/` 只可能来自未被剥掉的部分）——含 → path 通道，否则 → name 通道。
- name 通道 MUST NOT 再对字符类另作断言：`speckit.skills` 是合法的点号名（否则一条本应报命令面的输入会变成失败，与 FR-023(b) 冲突）。
- `.md`（非 `SKILL.md`）MUST NOT 被归一化剥除；「省略扩展名」MUST 被写成**结算约定**而不是归一化步骤，从而与 `run-skills` § 1 的既有说法不重叠（FR-022）。
- 名字落成路径 MUST NOT 出现在归一化结果里：`skill` 的 payload 只 MAY 携带一个**指向**位置阶梯的引用（FR-022）。
- `speckit.skills` 与 `speckit.skills/SKILL.md` 两种写法 MUST 收敛到同一个 `command-surface` 判定（NP-3/NP-4 先于 NP-6 的直接后果）。

## GR-05 — § Disambiguation rules：消歧四條

- 必须覆盖四条，每条至少一个示例输入：
  - (a) 前导 `/` 只标记该技能的**斜杠命令面**，MUST NOT 被读成「调用方应直接执行它而不是当前流程」（FR-023(a)）。
  - (b) 归一化后命中 `/speckit.*` 命令名的，MUST 报告为**命令面**并指向对应命令，MUST NOT 当作 Skill 解析、MUST NOT 强行执行；若确实存在同名技能，两者是两类不同对象，报告须同时点明、MUST NOT 二选一后静默继续（FR-023(b)）。
  - (c) dev 规范层与其安装镜像中的同名两处命中算**一处**；只有两个**不同层**各自的命中才算两处（FR-023(c)）。
  - (d) 被操作的元技能处理「改进/合并/创建某个技能」这类请求时，该请求 MUST NOT 被重分类为「不是真的工作项」，调用方也 MUST NOT 代它执行其步骤（FR-023(d)）。
- (c) MUST 明写「源 + 镜像 = 一处」的判据是**层**，不是路径字面（按路径字面比较会把同一技能的源目录与它的 `.specify/` 镜像目录读成两处）。

## GR-06 — § Failure semantics：四类失败与成对报告

- 失败表 MUST 恰四行，行集与 `data-model.md` E-10 **字面相等**（`zero-hit` / `out-of-ladder` / `unreadable` / `dual-layer`），每行的**必需报告项**逐项可核对（FR-024）。
- 每类失败的必需报告项 MUST 含**原始标识与归一化后标识**（FR-025）；缺一即视为未报告。
- 失败 MUST **关闭**（停住）：MUST NOT 出现「先试一个」「挑最近的一个继续」类恢复边；从用户侧改写成另一个引用是**一次新的归一化**，MUST NOT 复用上一次的失败结论。
- 四类 MUST 互斥：越界 MUST NOT 被报成零命中，目录不可读 MUST NOT 被报成越界（SC-009 的「不串味」断言对象）。
- CLI 形态下 `@name` 的处置 MUST 写成「归入 `zero-hit`，并增记『该形式在 CLI 形态下不可达』」，MUST NOT 为救回它另造语法（C11）。

## GR-07 — 起点核验（FR-027）

- 工作树中已有的未提交实现是本能力的**起点**，MUST 逐条核验是否满足 GR-01…GR-06，MUST NOT 以「规格要求重写」为由推倒既有正文。
- 核验 MUST 落证据：逐份对照结论 + 缺口清单写进 `test-evidence/`（本 plan 期已落的两处缺陷见 `plan.md` § Scope Update Record 的 SU-02 / SU-03 与 § D12）。
- 本阶段实测的三处起点缺口（实现期 MUST 关闭）：① 归一化顺序把「通道判定」提前到「剥前缀/后缀」之前，产生只有 NAME / PATH 两类且无 FAILURE（`research.md` § R10）；② 五份 `SKILL.md` 的 8 处引用串写的是 `.specify/` 镜像路径（`research.md` § R11）；③ `tests/` 对 `skill-reference` 零命中，SC-006…SC-009 尚无断言（`research.md` § R12）。

## GR-08 — 引用坐标：源路径，不引用镜像

- 消费方引用 [[STR-004]] 的**框架源路径** `shared/definitions/skill-reference-definitions.md`，MUST NOT 引用 `.specify/shared/definitions/…` 镜像路径（clarify 裁决 ② / T-004）。
- standalone 部署（无 `.specify/`）下消费方 MUST NOT 写出第二种拼写：以「相对框架根」解析，同一技能在两种模式下指向同一坐标（FR-028 的 standalone 降级条款，前提见 EP-007(a)）。
- 镜像 MUST 继续由 `sync-mirrors.py` 再生成并由 `--check` 证明一致；「不进引用面」不等于「不进镜像面」（FR-028）。

## GR-09 — 不拥有位置阶梯与其他 owner 的事实

- 「按名称解析时哪个位置优先」MUST 只用**路径引用**交出到 `skills/internal/run-skills/SKILL.md` § 1；本文 MUST NOT 内联或改写该阶梯的顺序，MUST NOT 新增位置（FR-022）。
- 本文 MUST NOT 包含归属其它 owner 的规则字面：目录治理（`shared/guidelines/directory-governance.md`）、同族概念锚点（`shared/definitions/derivation-definitions.md` 等）、机制/策略判据（`shared/definitions/mechanism-policy-definitions.md`）（C9）。
- 「不写位置阶梯」的可判形态：本文 MUST NOT 出现 `skills/external/` / `skills/internal/` 作为**优先顺序**的表述；`skills/external/merge-skills/SKILL.md` 这类路径只 MAY 作为接受形式的示例出现（GR-02 的 canonical path 行）。

## GR-10 — 零新机器

- 本能力 MUST NOT 新增：`/speckit.*` 命令、门禁脚本、目录根、环境变量、第二套分类数据文件（FR-029 / C4 / C8 / FR-016）。
- 接受形式集合的增长是一次**对本文的修订**，不是一次新命令、也不是某个消费方的一次局部扩展（FR-029 末句）。
- 归一化的**可执行实现**只 MAY 以 test-only 形态存在（`tests/contract/skill_reference_matrix.py`，`plan.md` § D11），MUST NOT 进入 `scripts/`、MUST NOT 成为门禁。

## SR-01 — `run-skills`（`skills/internal/run-skills/SKILL.md`）

- 接线落点：§ Input Contract（`Target` 参数声明）+ § 1 的**第 0 步**（归一化先于位置阶梯）。
- MUST 只声明自己的参数名与含义（`Target`），并以一个**源路径**引用指向 [[STR-004]]。
- § 1 的**位置阶梯（第 1–4 步）与信任边界段 MUST 逐字节不变**（FR-022）；第 0 步 MUST NOT 自述归一化顺序，MUST 收敛为「按 owner 归一化并披露原始标识与判定类」。
- MUST NOT 复制接受形式清单或失败语义表；MUST NOT 内联位置阶梯进 owner（FR-026）。

## SR-02 — `create-skills`（`skills/external/create-skills/SKILL.md`）

- 接线落点：§ 1 Case A（技能名的定义处）——声明 `Skill name` 参数 + 一条源路径引用。
- MUST 写明**特殊形态**：`create-skills` 只**命名**一个尚不存在的新技能、不解析既有技能；MUST NOT 因此复制一份「新建时也照此归一化」的第二套规则（FR-026 末句）。
- MUST NOT 复制接受形式清单或失败语义表。

## SR-03 — `improve-skills`（`skills/external/improve-skills/SKILL.md`）

- 接线落点：§ Input Contract 的 `Target identifier` ——声明参数名与含义 + 一条源路径引用。
- MUST NOT 复制接受形式清单或失败语义表；归一化顺序 MUST 只以引用出现（FR-019 唯一 owner）。
- 机制/策略侧的 § 2 / § 3 判定归 SW-02，本行不陈述、不替代（C9）。

## SR-04 — `merge-skills`（`skills/external/merge-skills/SKILL.md`）

- 接线落点：§ Input Contract 的 `Source` / `Target` 两参数——各声明参数名与含义 + 同一份源路径引用（一份引用覆盖两个参数，MUST NOT 写两遍规则）。
- MUST NOT 复制接受形式清单或失败语义表。
- 机制/策略侧的 § 5 / § 8 判定归 SW-03，本行不陈述、不替代（C9）。

## SR-05 — 源路径口径的执行面（跨消费方）

- 五个消费方共 **8 处**引用串（`research.md` § R11 的逐坐标读数：`create-skills` 1 / `improve-skills` 1 / `merge-skills` 1 / `coaching-skills` 3 / `run-skills` 2）MUST 全部改写为源路径；改写的可判形态是**文件 + 引用串内容**，MUST NOT 钉行号（行号随编辑漂移）。
- 改写 MUST 落**框架源**（`skills/…`），镜像由 `sync-mirrors.py` 再生成（FR-028 / GR-08）。
- 本行同时是 EP-007(a) 的闭合点：安装态下「以相对框架根解析」能把源路径解析到一份镜像，由实现期一次安装态实跑记录。
- 守卫形态：`test_skill_reference_consumers.py` 断言每个消费方**恰一条**指向源路径的引用、且以 `.specify/shared/definitions/` 为前缀的引用串**零命中**。

## SR-06 — `coaching-skills`（`skills/external/coaching-skills/SKILL.md`）与 `/speckit.skills` 标杆

- `coaching-skills` 接线落点：§ Inputs（参数声明）+ § 2 解析一行 + § Nested 一节；MUST 只声明自己的参数并以源路径引用 owner。
- `coaching-skills` 是机制/策略侧的 `excluded` 成员：本行**只**加引用接线，MUST NOT 引入机制/策略判定的字面（SW-05 的收紧形态）；其 `§ Improvement Plan` 的「真实改写仍经 `improve-skills`」通道句 MUST NOT 被本行改写（FR-014）。
- `/speckit.skills`（`templates/commands/skills.md`）是**命令面标杆**：MUST **不改**，且 MUST 在 SC-008 的正例里作为「归一化后落在 `/speckit.*` 命名空间 → `command-surface`」的实测对象（SW-06 / FR-011）。
- `/speckit.skills` 的实现者 MUST NOT 把命令面判定复制进命令模板：命令面判定归 owner 正文（GR-05(b)），模板只被**指向**。

## 可追溯性

| FR / SC | 条款 | 测试载体 |
|---|---|---|
| FR-019 | GR-01, GR-09 | `tests/contract/test_skill_reference_grammar.py` |
| FR-020 | GR-02 | 同上 |
| FR-021 | GR-03, GR-04 | 同上 |
| FR-022 | GR-04（名字落成路径不内联）, GR-09, SR-01 | `test_skill_reference_grammar.py` + `skills/internal/run-skills/SKILL.md` § 1 第 1–4 步逐字节断言 |
| FR-023 | GR-05（a–d）, GR-04（命令面出口） | `test_skill_reference_grammar.py` + `test_skill_reference_command_surface.py` |
| FR-024 | GR-06 | `test_skill_reference_failures.py` |
| FR-025 | GR-03（成对报告）, GR-06（失败类的成对报告） | `test_skill_reference_grammar.py` + `test_skill_reference_failures.py` |
| FR-026 | SR-01…SR-04, SR-06 | `test_skill_reference_consumers.py` |
| FR-027 | GR-07 | `test-evidence/` 的起点核验记录（逐份对照结论 + 缺口清单） |
| FR-028 | GR-08, SR-05 | `test_skill_reference_consumers.py` + `sync-mirrors.py --check` |
| FR-029 | GR-10 | `test_skill_reference_grammar.py`（形式集封闭）+ `test_skill_reference_consumers.py`（零复制） |
| FR-030 | GR-04（三值封闭）, GR-06（失败互斥） | `test_skill_reference_matrix.py`（矩阵逐行复算，GM-13） |
| SC-006 | GR-02, GR-03, GR-04, GR-06 | `tests/contract/test_skill_reference_matrix.py` + `test-evidence/sc-006-*.txt` |
| SC-007 | GR-08, SR-01…SR-06 | `tests/contract/test_skill_reference_consumers.py` + `test-evidence/sc-007-*.txt` |
| SC-008 | GR-05(b), GR-05(a), SR-06 | `tests/contract/test_skill_reference_command_surface.py` + `test-evidence/sc-008-*.txt` |
| SC-009 | GR-06 | `tests/contract/test_skill_reference_failures.py` + `test-evidence/sc-009-*.txt` |
