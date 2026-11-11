# Contract — Merge-Back（分片合并回写的确定性规则）

**Feature**: 099-speckit-seal | **Date**: 2026-11-10 | **Plan**: [plan.md](../plan.md)
**Owns**: 分片集合与顺序的派生规则、15 项输出件宇宙与动作分类、编号重排、语义/词汇对齐、冲突、归属记录与写面。

**C-011** — 分片集合由两个条件**同时**成立确定，单条件命中即冲突。

集合成员必须同时满足：(a) 目录名形如 `<父编号><一个或多个字母>-<slug>` 且与父级同处一个 `.specify/specs/`；
(b) 该分片 `requirements.md` 以**封闭二形**之一声明父规格——`## Parent Mapping` 章节，或 `**Parent spec**:`
头部字段。只命中一个条件的目录 MUST NOT 进入集合，MUST 作为冲突项（`slice-candidate-unconfirmed`，
点名未满足的条件）呈现。所用集合与两个条件的判定结果 MUST 写入合并清单。

(FR-011)

**C-012** — 分片顺序取声明顺序；回退必须留痕。

顺序 MUST 取父级拆分记录的 `proposed_slices` 有序列表（来源：`.specify/state/<parent-slug>.md`
§ 拆分记录；`074` 的实证形态见 research R-11）。拆分记录缺席时 MUST 取字母后缀字典序，并在 manifest 的
`order_basis` / `order_source` 写明所用依据。MUST NOT 依赖运行期目录列举顺序或文件系统时间。

(FR-011)

**C-013** — 合并宇宙是 15 项封闭集，动作四值，流程唯一。

候选宇宙恰为：`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`、`research.md`、
`quickstart.md`、`feature-ref.md`、`verification.md`、`review.md`、`code-review.md`、`checklists/`、
`checkpoints/`、`test-evidence/`、`notes/`。**目录型候选**（`contracts/`、`checklists/`、`checkpoints/`、
`test-evidence/`、`notes/`）的合并单位是**文件**：按文件名在父级与全部分片间取并集，逐文件处置——两侧
同名 → 该文件为合并单元（`merge`；内容按其声明结构归并，无法确定性归并或同一锚点双端编辑 → 冲突）；
仅分片有 → `create`；仅父级有 → `keep`。`test-evidence/`、`checkpoints/` 内的既有日期化测量文件属
dated record（C-020）：MUST NOT 复制或改写原件；同名时父级文件维持 `keep` 并在合并清单记录指向分片原件的
指针，仅分片有时以父级指针视图（汇总行 + 指针）`create`，分片原件字节不变。**必选下限**：`tasks.md` 无论
是否产出都必须被处置；分片集合非空时，父 `verification.md`（聚合指针视图，缺席新建）、父 `review.md`
（分片 review 记录的汇总指针视图，缺席新建）、父 `code-review.md`（分片 code-review 记录的汇总指针视图，
缺席新建）与 `merge-manifest.json` MUST 产出。该汇总指针视图（逐分片汇总行 + 指针）不承载 finding 块，
且**不改变 seal 的 P0 / `blocking` 判定读取面**——判定 MUST 读取各分片原始 `review.md` / `code-review.md`
（waiver 形态见 `records-and-boundaries.contract.md` C-044）。其余候选按实际产出枚举：两侧皆有 → `merge`；仅分片有 →
`create`；仅父级有 → `keep`（并接受同一套对齐检查）；两侧皆无 → `not-applicable`。MUST NOT 为单个输出件
发明第二套合并流程；输出件差异只体现在其声明的 ID 家族与结构单元上。

(FR-012)

**C-014** — 确定性是合并的硬约束。

同一输入 MUST 产生逐字节一致的合并产物与合并清单；成功 `merge-apply` 后的重跑 MUST 零 diff、零重复行、
零重复 ID。任何决策 MUST NOT 依赖返回时刻、目录枚举顺序、随机源或「最后写入者胜出」。无法确定性归并的
差异 MUST 进入冲突清单，MUST NOT 由启发式择一。

(FR-013)

**C-015** — 编号重排：父映射复用、分片独有追加。

对每个在案的 ID 家族（至少 FR、SC、STR、契约条款、任务行、实体、阶段/检查点标识）：分片本地 ID 有父映射的
MUST 改用父 ID；无父映射的分片独有 ID MUST 按合并顺序追加到父序列（连续、无空洞、无重复），映射（`kind:
mapped | appended | localization`）写入 manifest 的 `id_maps`。合并产物内的一切引用 MUST 改写为合并后 ID；
映射后不可解析的引用 MUST 判为冲突。契约条款家族的追加使用父文件内的下一个空闲 `C-N`（条款 id 只在单文件
内唯一，见 `shared/definitions/contract-clause-definitions.md` § 1），不发明新的 id 形态。同一家族两次运行
MUST 得到同一映射。

(FR-014)

**C-016** — 语义对齐只信分片声明的映射表。

每个分片需求/判据条目 MUST 有且仅有一个父目标，除非分片显式声明多对一合并。无映射、映射目标不存在、
两分片条目映射到同一父目标而无声明合并，三者 MUST 判为冲突。MUST NOT 用模型转述判断「意思相同」，
MUST NOT 发明映射。父级与分片对同一映射单元的文本差异属**合法本地化**（`kind: localization`），
不构成冲突——冲突只在映射层发生。

(FR-015)

**C-017** — 词汇表对齐：共享字符串解析到合并后的唯一父级注册表。

合并后每个 `[[STR-NNN]]` 引用 MUST 解析到父级唯一注册表。同一 ID 在分片与父级指向不同字面量（同号不同义）
MUST 判为冲突，两侧字面量并列呈现，MUST NOT 静默重编号。**token→注册表绑定**：`[[STR-NNN]]` 的解析域由其
声明登记处决定——spec 文档以自身 `requirements.md` § Shared Strings 为登记处（口径 owner：
`shared/definitions/sdd-routing-definitions.md` § 字面量登记处）；spec 之外的出厂文档 MUST 显式声明所用登记处
（spec 路径 + 节锚）。未声明登记处的引用 MUST 做跨登记处解析检查：恰好一个分片注册表命中且字面量一致 →
按该分片本地 ID 检出并按本条记录解决方式；零命中、或多处命中且字面量不同 → 判为冲突，MUST NOT 猜测归属。
出厂文档（框架源与镜像）中对分片本地 ID 的引用
MUST 被检出：在合并后语义下解析会改变含义的引用，MUST 逐条记录解决方式（重指向合并后 ID / 改用逐字字面量 /
用户豁免），并写入 manifest 的 `factory_doc_resolutions[]`（`{path, line, before, after, kind}`，
`kind` ∈ `repoint | literal | user-waiver`）；`after` MUST 可核实（重跑不再复现该引用缺陷）。新术语 MUST 经 `.specify/glossary.md` 既有协议进入词汇表，MUST NOT 在 spec 内联定义第二份术语表。

(FR-016)

**C-018** — 冲突是一等记录；开放即阻断。

每条冲突 MUST 含：输出件、单元（ID/标题/行区间）、两侧内容摘录、候选处置与状态（`open` / `resolved`）。
任一 `open` 冲突 MUST 阻断 `seal`。解决 MUST 显式且留痕，且只有三种封闭形式：`canonical-map`（分片映射表声明的重指向）、
`recheck-clean`（用户修复输入后重跑不再复现）、`user-waiver`（C-044 的用户裁定行）。MUST NOT 静默择一，
MUST NOT 造成内容丢失；引擎 MUST NOT 以「较新/较全/较大/较后」任一单侧截断作为解决。

(FR-017)

**C-019** — 归属记录由合并清单承载；父级成为唯一现行权威。

`merge-manifest.json` MUST 逐输出件记录来源与动作、逐单元/逐 ID 记录来源（分片 slug + 原 ID）与重映射。
合并完成后父 spec MUST 为唯一现行权威；每个分片目录 MUST 被标注 `merged into <父 spec>`（**恰好一行**
`**Merged into**:` 头部字段，落在分片 `requirements.md`），其内容作为 dated record 保留，MUST NOT 被 seal
删除或改写（归档是一次移动：内容原样保留，仅位置改变）。分片承载物的后续处置已由
`100-seal-slice-archive` 以 non-disposable 处置集的 `archive` 决定：目的地 = 所属父 spec 的
`slices/<原分片目录名>/`，处置记录 = 父 spec 的 `archive-manifest.json` 逐片 `{from, to}` 行；MUST NOT
默认沉默保留，MUST NOT 再建第二份保留/退役记录。

(FR-018)

**C-020** — dated-record 红线。

分片的 `review.md`、`code-review.md`、`verification.md`、`test-evidence/` 与其它既有日期化测量 MUST NOT 被
改写；父级合并视图 MUST 以「汇总行 + 指针」形态引用它们（与 074 父 `verification.md` 聚合指针形态同构）。
目录型候选内的 dated-record 文件按**指针纳入**处置：同名文件父级保持 `keep` 并在合并清单留指针，仅分片
有时父级生成指针视图，MUST NOT 复制分片原件为父级副本。引擎 MUST 在运行前后对上述文件取哈希并断言一致；
MUST NOT 制造第二份测量。

(FR-019)

**C-021** — 散文类产物的合并规则。

`plan.md`、`research.md`、`data-model.md`、`quickstart.md`、`feature-ref.md` 以父级文本为权威、保持原文本
不变；分片独有章节（父级不存在同名标题）MUST 进入 `## Merged from slices` 附录区块并带 `<!-- source:
<slice> -->` 来源标注；同名标题的差异按 C-016 归入 `localization`，不构成冲突。父级 `review.md` / `code-review.md` /
`verification.md` 的合并视图按 C-013 / C-020 的「汇总 + 指针」形态生成。

(FR-012, FR-019)

**C-022** — 拆前行按 `supersede` 处置，原行保留。

父 `tasks.md` 中因拆分而失效的未勾选行 MUST 按 `supersede` 处置：原行文本保留在「Superseded pre-split
record」块内并以 `> ` 引用前缀呈现（使 `^\s*- \[(.)\]` 不再命中），块内逐条记录 `superseded`（原位置）与
`superseded_by`。`superseded_by` MUST 指向**合并清单自身**（`{path: merge-manifest.json, line: 0}`，
line 0 = 整文件事实），由 `slices[].carrier_tasks` 列出真正接手的分片 `tasks.md`——拆分声明只有 FR 范围、
没有逐行映射，引擎 MUST NOT 发明逐行目标（C-016）。每条处置记录 MUST 带 `evidence[]`（分片任务文件路径）
与 `guard_status`（`retired | replaced | unchanged-with-reason`）。合并后父 `tasks.md` 的未勾选行数 MUST 为 0。MUST NOT 静默覆盖、MUST NOT 伪勾选、MUST NOT 删除。

(FR-018)

**C-023** — 写面与并发边界。

`merge-apply` 只写父 spec 目录、分片的 `merged into` 标注与 C-017 记录过解决方式的出厂文档引用修正；
MUST NOT 归档、移动或删除 spec 目录（分片归档归 `100-seal-slice-archive` 的独立动作 `archive-apply`，
MUST NOT 并入 `merge-apply`——`merge-apply` 保持纯合并），MUST NOT 触碰 goal/team 树（归 `/speckit.goal`
的 `migrate-archive`），MUST NOT push。并发安全 MUST 按「一 spec 一记录文件」满足：两条并行线封装不同
spec 时写入不同路径，MUST NOT 引入共享可变聚合文件。

(FR-020)
