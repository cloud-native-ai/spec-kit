# Contract — Reference Classification（扫描根、载体名册、分类谓词与解析定义）

**Feature**: 100-seal-slice-archive（bound Feature 099） | **Date**: 2026-11-11 | **Plan**: [plan.md](../plan.md)
**Owns**: 「活引用 vs 日期化记录」的**机械判定**——扫描根封闭集、引用形态封闭集、载体名册、章节/行谓词、日期化豁免四条件、解析定义与「未解析 = 0」。清单字段归 `archive-manifest.contract.md`；动作与写面归 `archive-actions.contract.md`。

**C-301** — 扫描根是封闭集，逐根全量扫描，不抽查。

解析检查 MUST 覆盖且只覆盖下列扫描根（仓库根相对）：

| 扫描根 | 分类归属 |
|--------|----------|
| `.specify/specs/<parent>/`（递归） | 正式活文档 = live；`notes/**`、`test-evidence/**`、`checklists/**` = dated；`slices/**`（归档后）= dated；`merge-manifest.json` = 仅路径形态值 live；`archive-manifest.json` 自身**排除**（它是映射 owner，不是引用载体） |
| `.specify/specs/<slug>/`（每个分片；归档后按其 `to` 位置） | dated（分片内部全部文件） |
| `.specify/register.md` | live |
| `.specify/features.md` | dated |
| `.specify/features/<ID>.md` | 混合（按 C-304 章节谓词） |
| `.specify/glossary.md`、`.specify/instructions.md` | live |
| `.specify/memory/**`、`.specify/history/**` | dated |
| `shared/**`（框架源）、`.specify/shared/**`（镜像） | live（源与镜像各记一行，同批改写） |
| `tests/**` | live（按 C-311 的构造行谓词） |
| `.specify/state/**` | 运行期载体（按 C-309 单独处理，不计入 `references.rows[]`） |

其他 `.specify/specs/<other>/` 的日期化记录（例如 099 的 `test-evidence/`）MUST NOT 计入本特性的扫描声明；它们保持原字节，归档清单的 `from → to` 映射对它们同样可用。检查 MUST NOT 只抽查已知载体——声明根上的全部命中都必须有一行台账。

(FR-012, FR-015)

**C-302** — 引用形态封闭为三类；裸 slug 不是引用。

一个「引用」是一次命中下列形态之一的文本：

- **F1（spec-root 全路径）**：`.specify/specs/<slug>`，可带 `/…` 尾巴。
- **F2（父 spec 内相对路径）**：`<slug>/…`，且前一字符不是标识符字符（字母、数字、`_`、`-`）。F2 只在载体位于 `.specify/specs/<parent>/` 子树内时被识别。
- **F3（测试构造行）**：仅在 `tests/**` 中，一个 slug 字符串字面量出现在同一行同时含 `.specify` 与 `specs` 的行上（路径构造式）。

裸 slug 出现（后方无 `/`、前方无 `.specify/specs/`）MUST NOT 计为引用：`slices[].slug`、`artifacts[].sources[]`、`artifacts[].per_slice[].slice`、`id_maps` 键、`<!-- source: <slug> -->` 标注一律保持原字节。落在三类之外的路径形态（绝对路径、`../<slug>`、跨行拼接等）在扫描根内命中 MUST 成为 `unclassified-reference` 阻断（fail closed）。

(FR-012)

**C-303** — 活载体名册（封闭集）。

「live」载体恰为：`<parent>` 的正式文档（`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`research.md`、`quickstart.md`、`feature-ref.md`、`verification.md`、`review.md`、`code-review.md`、`contracts/**`、父级 `seal.md` 若未来存在）；`merge-manifest.json` 的路径形态值；`.specify/register.md`；`.specify/features/<ID>.md` 的 `## Related Specifications/Requirements` 章节；`.specify/glossary.md`；`.specify/instructions.md`；`shared/**` 源与 `.specify/shared/**` 镜像；`tests/**`。MUST NOT 在本名单外新增 live 载体而不修订本条款。

(FR-013)

**C-304** — 日期化载体名册与混合载体的章节谓词。

「dated」载体恰为：每个分片的全部文件（移动后仍为 dated，字节不变）；`.specify/memory/**`；`.specify/history/**`；`.specify/features.md`；`.specify/features/<ID>.md` 中 `## Related Specifications/Requirements` **以外**的全部章节（至少 `## Latest Review`、`## Key Changes`、`## Implementation Notes` 与时间线）；`<parent>/notes/**`、`<parent>/test-evidence/**`、`<parent>/checklists/**`。混合载体 `features/<ID>.md` 的判定顺序：先按 H2 章节切分，`## Related Specifications/Requirements` 归 live，其余归 dated；一个命中同时满足 live 与 dated、或两个都不满足，均判 `unclassified-reference`。

(FR-014)

**C-305** — 分类顺序固定为「先载体、后谓词、再解析」，全部由程序执行。

一次命中的判定 MUST 按序执行：① 按载体路径落入 live 或 dated 封闭集（混合载体再按章节）；② 混合载体在章节内按行谓词细分；③ apply 后执行解析测试（C-307）。判定 MUST 只依据路径、行前缀、章节边界或文件谓词，MUST NOT 依赖模型对语义的转述判断。封闭集之外的载体出现命中 → `unclassified-reference`（exit `1`，`archive-plan` 同样阻断）。

(FR-012)

**C-306** — 日期化豁免的四条件同时成立才是 `dated-preserved`。

一个命中被计为 `dated-preserved`，当且仅当：(a) 其载体 ∈ dated 封闭集，或位于混合载体的 dated 章节；(b) 命中文本包含清单映射中的某个 `from` 前缀（或其父内相对形态）；(c) 该文件归档前后 sha256 相等；(d) 映射后的目标在树上存在。四条之外 MUST NOT 记 `dated-preserved`；MUST NOT 以「读起来像历史」、文件名直觉或任何模型判断替代上述四条。

(FR-012, FR-014)

**C-307** — 「未解析引用 = 0」的唯一定义与 fail closed。

一条引用被判定为**已解析**，当且仅当：(a) 其目标路径在树上存在；或 (b) 它是 `dated-preserved` 行，其旧前缀命中归档清单的 `from → to` 映射并落到存在的归档路径。两者之外即未解析。`archive-plan` MUST 报告未解析数；`archive-apply` MUST 在未解析数大于 0 时拒绝（`unresolved-references`，exit `1`）；apply 成功后复验 MUST 仍为 0。

(FR-015)

**C-308** — 改写机制：前缀替换、整行记录、dated 文件哈希不变。

`live-rewrite` 的改写 MUST 是确定性前缀替换：F1 的 `.specify/specs/<slug>` → `.specify/specs/<parent>/slices/<slug>`；F2 的 `<slug>/` → `slices/<slug>/`（仅父 spec 子树内的 live 载体）；F3 把 slug 字面量替换为 `<parent>/slices/<slug>`（保持原有引号与其余字符）。每条改写 MUST 在台账记录 `before` / `after` 整行与 `carrier` / `line`。所有 `dated-preserved` 载体 MUST 在运行前后保持 sha256 相等；任一日 dated 文件哈希变化 MUST 使 apply 以 `2` 结束并按原字节恢复。

(FR-013, FR-014)

**C-309** — 运行期载体的声明集与缺席语义。

声明的运行期载体恰为 `.specify/state/<parent>.md` 与每个分片的 `.specify/state/<slug>.md`（合计 1 + 分片数）。每个载体 MUST 各记一条 `runtime-updated`（状态根可解析且记录存在时，其中的分片路径引用在同一批次更新，逐条记 `line` / `before` / `after`）或 `absent`（状态根不可解析或记录缺席，附原因）。该更新 MUST NOT 进入版本库提交范围，MUST NOT 改变任何 line 的 `spine_state` 或阶段读数；`absent` MUST NOT 阻断。

(FR-017)

**C-310** — 框架 owner 文档与镜像同批处理。

`shared/**` 源与 `.specify/shared/**` 镜像是两个独立 live 载体：同一逻辑引用在两处各记一行台账，且 MUST 在同一 apply 批次内被改写为相同文本。MUST NOT 只改一侧；镜像侧的写入 MUST 与 `sync-mirrors.py` 的逐字节一致纪律相容（源与镜像最终同字节）。

(FR-013)

**C-311** — 测试载体按构造行谓词判定。

`tests/**` 中的 F3 命中 MUST 由引擎把 slug 字面量改写为 `<parent>/slices/<slug>`，使路径构造式在归档后仍指向存在的目录。仅作 identity 使用的 slug 常量（例如断言合并清单 `slug` 字段的常量）MUST NOT 被改写。测试文件的改写在台账中按 `live-rewrite` 记录；改写后该测试 MUST 仍能解析其声明的载体路径。

(FR-013)

**C-312** — 声明之外无声明：不建派生索引、不做语义解析。

解析检查 MUST 在每次 `archive-plan` / `archive-apply` 时按声明根重新执行，MUST NOT 建立缓存索引、派生映射文件或第二份「旧路径 → 新路径」表。清单是唯一映射载体（C-210）。扫描与分类 MUST 是只读的；只有 `archive-apply` 的写入批次可以写声明集合内的路径。

(FR-015)
